import asyncio
from threading import Thread

from aiogram import Router, types, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from core.texts import TOTAL_USERS_MESSAGE, BROADCAST_USER_COUNT, BROADCAST_MESSAGE_PROMPT, SELECT_CHANNEL_PROMPT, \
    CHOOSE, USER_COUNT_MESSAGE, USER_COUNT_BROADCAST, SEND_TO_USERS_PROMPT, SEND_MESSAGE_PROMPT, ENTER_NUMBER_ONLY, \
    CANCELLED, NOT_ENOUGH_PEOPLE, CONFIRM_RUN_MESSAGE, SENDING_MESSAGE_TO_USERS, FORWARD_YOUR_POST
from keyboards.InlineKeyboard import get_keyboard, my_users_btn, yesno, channels_new, get_cancel
from keyboards.Replykeyboard import get_n_cancel
from core.helpers import  send_message_broad
from core.states import my_users
from models.database import get_channels, all_clients

router = Router(name="broadcast_router")

@router.callback_query(F.data=="Broadcast Message")
async def add_channel(message: types.CallbackQuery,state:FSMContext) -> None:
    await state.set_state(my_users.channels)
    clients = all_clients(message.from_user.id)[0]
    await message.message.edit_text(TOTAL_USERS_MESSAGE.format(clients["count(*)"]),reply_markup=my_users_btn())


@router.callback_query(my_users.channels)
async def schedule_handle(message: types.CallbackQuery,state: FSMContext):
    if message.data == 'all_user':
        await state.set_state(my_users.all_users)
        await state.update_data(users = 'all')
        await message.message.delete()
        await message.message.answer(BROADCAST_MESSAGE_PROMPT,reply_markup=get_n_cancel())

    elif message.data == 'channel_wise':
        await state.set_state(my_users.channels_run)
        await state.update_data(users='channel')
        await message.message.edit_text(SELECT_CHANNEL_PROMPT,reply_markup=channels_new(get_channels(message.from_user.id)))

    elif message.data == 'cancel':
        await message.message.edit_text(CHOOSE, reply_markup=get_keyboard())
        await state.clear()

@router.callback_query(my_users.user_count)
async def schedule_handle(callback: types.CallbackQuery,state: FSMContext):
    if callback.data == 'cancel':
        await state.set_state(my_users.channels)
        await callback.message.edit_text(CHOOSE, reply_markup=my_users_btn())
    else:
        await callback.message.answer(USER_COUNT_BROADCAST.format(all_clients(callback.from_user.id, callback.data)[0]["count(*)"]))
        await state.update_data(channel = callback.data)
        await state.set_state(my_users.channels_run)

@router.message( my_users.all_users)
async def schedule_handle(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "cancel" in message.text.lower():
        clients = all_clients(message.from_user.id)[0]
        await message.answer(CANCELLED,reply_markup=ReplyKeyboardRemove())
        await message.answer(TOTAL_USERS_MESSAGE.format(clients["count(*)"]), reply_markup=my_users_btn())
        await state.set_state(my_users.channels)
    elif data['users'] == 'all':
        if message.text.isnumeric():
            await state.update_data(users_count = message.text)
            await state.set_state(my_users.channels_run_send_con)
            await message.answer(SEND_MESSAGE_PROMPT,reply_markup=get_n_cancel())
        else:
            await message.answer(ENTER_NUMBER_ONLY)
    else:
        await state.update_data(channel=message.text)
        await state.set_state(my_users.channels_run)
        await message.answer(SEND_TO_USERS_PROMPT)

@router.callback_query(my_users.channels_run)
async def schedule_handle(callback: types.CallbackQuery,state: FSMContext):
    if callback.data == 'back':
        await state.set_state(my_users.channels)
        await callback.message.edit_text(CHOOSE, reply_markup=my_users_btn())
    else:
        await state.update_data(users = [i['user_id'] for i in all_clients(callback.from_user.id, callback.data, 'user_id')])
        await state.set_state(my_users.channels_run_send)
        await callback.message.answer(USER_COUNT_BROADCAST.format(all_clients(callback.from_user.id, callback.data)[0]["count(*)"]),reply_markup=get_n_cancel())
        await callback.message.delete()


@router.message( my_users.channels_run_send)
async def schedule_handle(message: types.Message,state: FSMContext):
    if message.text.isnumeric():
        await state.update_data(users_count=message.text)
        await state.set_state(my_users.channels_run_send_con)
        await message.answer(FORWARD_YOUR_POST)

    elif "cancel" in message.text.lower():
        await state.set_state(my_users.channels)
        await message.reply(CANCELLED, reply_markup=ReplyKeyboardRemove())
        await message.answer(CHOOSE,reply_markup=my_users_btn())
    else:
        await message.answer(ENTER_NUMBER_ONLY)

@router.message( my_users.channels_run_send_con)
async def edit_message(message: types.Message,state: FSMContext):
    if "cancel" in message.text.lower():
        clients = all_clients(message.from_user.id)[0]
        await message.answer(CANCELLED, reply_markup=ReplyKeyboardRemove())
        await message.answer(TOTAL_USERS_MESSAGE.format(clients["count(*)"]), reply_markup=my_users_btn())
        await state.set_state(my_users.channels)
    else:
        await state.update_data(message_id=message.message_id,forward_from=message.from_user.id,buttons= message.reply_markup)
        await state.set_state(my_users.channels_run_send_conf)
        await message.bot.copy_message(message.from_user.id, message.from_user.id, message.message_id,reply_markup=message.reply_markup)
        await message.answer(CONFIRM_RUN_MESSAGE, reply_markup=yesno())

@router.callback_query(my_users.channels_run_send_conf)
async def edit_message(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.delete()
    if callback.data == 'Yes':
        data = await state.get_data()
        if data['users'] != 'all':
            await callback.message.answer(SENDING_MESSAGE_TO_USERS,reply_markup=ReplyKeyboardRemove())
            await callback.message.answer(CHOOSE,reply_markup=get_keyboard())
            task = asyncio.create_task(send_message_broad(clients=data['users'], forward_from=data['forward_from'], message_id=data['message_id'], btn=data['buttons'], usr_count=data['users_count'],bot=callback.bot))

        else:
            clients = all_clients(owner=callback.from_user.id, col= '*')
            clients_ids = [i['user_id'] for i in clients]
            if len(clients) == 0:
                await callback.message.edit_text(NOT_ENOUGH_PEOPLE, reply_markup=get_keyboard())
            else:
                await callback.message.answer(SENDING_MESSAGE_TO_USERS, reply_markup=ReplyKeyboardRemove())
                await callback.message.answer(CHOOSE, reply_markup=get_keyboard())
                task = asyncio.create_task(send_message_broad(clients=clients_ids, forward_from=data['forward_from'],
                                                              message_id=data['message_id'], btn=data['buttons'],
                                                              usr_count=data['users_count'],bot=callback.bot))
        await state.clear()

    elif callback.data == 'No':
        await callback.message.edit_text(CANCELLED, reply_markup=get_keyboard())
        await state.clear()



