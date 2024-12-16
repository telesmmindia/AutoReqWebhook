import asyncio
from threading import Thread

from aiogram import Router, types, Bot, F
from aiogram.fsm.context import FSMContext

from keyboards.InlineKeyboard import get_keyboard, my_users_btn, yesno, channels_new, get_cancel
from keyboards.Replykeyboard import get_n_cancel
from core.helpers import n
from core.states import my_users
from models.database import get_channels, all_clients

router = Router(name="broadcast_router")

@router.callback_query(F.data=="Broadcast Message")
async def add_channel(message: types.CallbackQuery,state:FSMContext) -> None:
    await state.set_state(my_users.channels)
    clients = all_clients(message.from_user.id)[0]
    await message.message.edit_text(f'You have total of {clients["count(*)"]} Users!')
    await message.message.answer('Choose',reply_markup=my_users_btn())


@router.callback_query(my_users.channels)
async def schedule_handle(message: types.CallbackQuery,state: FSMContext):
    if message.data == 'all_user':
        await state.set_state(my_users.all_users)
        await state.update_data(users = 'all')
        await message.message.delete()
        await message.message.answer('For how many users you want to Broadcast the Message?')

    elif message.data == 'channel_wise':
        await state.set_state(my_users.channels_run)
        await state.update_data(users='channel')
        await message.message.edit_text('Select a channel to get user count',reply_markup=channels_new(get_channels(message.from_user.id)))

    elif message.data == 'Cancel':
        await message.message.edit_text('Choose', reply_markup=get_keyboard())
        await state.clear()

@router.callback_query(my_users.user_count)
async def schedule_handle(callback: types.CallbackQuery,state: FSMContext):
    if callback.data == 'cancel':
        await state.set_state(my_users.channels)
        await callback.message.edit_text('Choose', reply_markup=my_users_btn())
    else:
        await callback.message.answer(f'You have {all_clients(callback.from_user.id, callback.data)[0]["count(*)"]} users in this channel')
        await state.update_data(channel = callback.data)
        await state.set_state(my_users.channels_run)
        await callback.message.answer('Send message to how many users?')

@router.message( my_users.all_users)
async def schedule_handle(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data['users'] == 'all':
        if message.text.isnumeric():
            await state.update_data(users_count = message.text)
            await state.set_state(my_users.channels_run_send_con)
            await message.answer('Send a message you want to run.')
        else:
            await message.answer('Please enter a number only')
    else:
        await state.update_data(channel=message.text)
        await state.set_state(my_users.channels_run)
        await message.answer('Send message to how many users?')

@router.callback_query(my_users.channels_run)
async def schedule_handle(callback: types.CallbackQuery,state: FSMContext):
    if callback.data == 'cancel':
        await state.set_state(my_users.channels)
        await callback.message.edit_text('Choose', reply_markup=my_users_btn())
    else:
        await state.update_data(users = [i['user_id'] for i in all_clients(callback.from_user.id, callback.data, 'user_id')])
        await state.set_state(my_users.channels_run_send)
        await callback.message.answer(f'You have {all_clients(callback.from_user.id, callback.data)[0]["count(*)"]} users in this channel\nEnter amount on how much users you want to Broadcast',reply_markup=get_n_cancel())
        await callback.message.delete()


@router.message( my_users.channels_run_send)
async def schedule_handle(message: types.Message,state: FSMContext):
    if message.text.isnumeric():
        await state.update_data(users_count=message.text)
        await state.set_state(my_users.channels_run_send_con)
        await message.answer('Send a message you want to run.')

    elif message.text=='Cancel':
        await state.set_state(my_users.channels)
        await message.reply('Cancelled', reply_markup=my_users_btn())
    else:
        await message.answer('Enter a number only\nTry Again')

@router.message( my_users.channels_run_send_con)
async def edit_message(message: types.Message,state: FSMContext):
    await state.update_data(message_id=message.message_id,forward_from=message.from_user.id,buttons= message.reply_markup)
    await state.set_state(my_users.channels_run_send_conf)
    await message.bot.copy_message(message.from_user.id, message.from_user.id, message.message_id,reply_markup=message.reply_markup)
    await message.answer('Are you sure you want to run this message', reply_markup=yesno())

@router.callback_query(my_users.channels_run_send_conf)
async def edit_message(callback: types.CallbackQuery,state: FSMContext):
    await callback.answer('choose')
    if callback.data == 'Yes':
        data = await state.get_data()
        if data['users'] != 'all':
            await callback.message.edit_text('Broadcasting Started 📢', reply_markup=get_keyboard())
            thread = Thread(target=n, args=(data['users'],data['forward_from'],data['message_id'],data['buttons'],data['users_count'],callback.bot))
            thread.start()
        else:
            clients = all_clients(owner=callback.from_user.id, col= '*')
            clients_ids = [i['user_id'] for i in clients]
            if len(clients) == 0:
                await callback.message.edit_text('🚫👥 You don\'t have any users', reply_markup=get_keyboard())
            else:
                await callback.message.edit_text('Broadcasting Started 📢', reply_markup=get_keyboard())
                thread = Thread(target=n,args=(clients_ids, data['forward_from'], data['message_id'], data['buttons'],data['users_count'],callback.bot))
                thread.start()
        await state.clear()

    elif callback.data == 'No':
        await callback.message.edit_text('Cancelled', reply_markup=get_keyboard())
        await state.clear()



