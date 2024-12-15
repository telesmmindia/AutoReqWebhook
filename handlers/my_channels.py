from threading import Thread
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from keyboards.InlineKeyboard import get_keyboard, edit_btns, get_cancel, yesno, channels_btns, \
    channels_new  # channels_new import this later when button is fixed
from keyboards.Replykeyboard import get_n_cancel

from core.states import MyChannels
from core.texts import GRT_SET_2_DEF
from models.database import get_channels, all_clients, channel_remover, editor
from core.helpers import n

router = Router(name="my_channel")


@router.callback_query(F.data == "My Channels")
async def my_channels(message: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(MyChannels.show)
    await message.message.edit_text('Your Channels', reply_markup=channels_new(get_channels(message.from_user.id)))


@router.callback_query(MyChannels.show)
async def channel_details(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'back':
        await callback.message.edit_text('choose', reply_markup=get_keyboard())
        await state.clear()
    else:
        await state.set_state(MyChannels.edit)
        details = get_channels(callback.from_user.id, callback.data)
        await state.update_data(editing_channel=details)
        await callback.message.edit_text(
            f"Channel Name:    {details[0]['channel_name']}\nChannel id:    `{details[0]['channel_id']}`",
            reply_markup=channels_btns(), parse_mode='Markdown')


@router.callback_query(MyChannels.edit)
async def channel_edit(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if callback.data == 'message':
        await callback.message.edit_text('Your Greeting Message for this Channel is 👇')
        await state.set_state(MyChannels.btn_edit)
        print(data)
        if data['editing_channel'][0]['greet_msg'] != 0:
            print((data['editing_channel'][0]['btns']).replace('\"', '\''))
            await callback.bot.copy_message(callback.from_user.id, data['editing_channel'][0]['greet_msg_chat'],
                                   data['editing_channel'][0]['greet_msg'],
                                   reply_markup=None if data['editing_channel'][0][
                                                            'btns'] == 'None' else InlineKeyboardBuilder(
                                       eval(data['editing_channel'][0]['btns'])).as_markup())
        else:
            await callback.message.answer(GRT_SET_2_DEF)

        await callback.message.edit_text('Edit Options', reply_markup=edit_btns())

    elif callback.data == 'post':
        if data['create_post']:
            await callback.message.answer(data['create_post'])
        else:
            await callback.message.answer('No post created')

    elif callback.data == 'promo':
        await state.set_state(MyChannels.count)
        await callback.message.edit_text(
            f'You have {all_clients(callback.from_user.id, data["editing_channel"][0]["channel_id"])[0]["count(*)"]} users in this channel')
        await callback.message.answer('Enter Number of Users you want to Broadcast Message',
                                      reply_markup=get_n_cancel())

    elif callback.data == 'remove':
        await state.set_state(MyChannels.remove)
        await callback.message.edit_text('Are you sure you want to remove this Channel', reply_markup=yesno())

    elif callback.data == 'back':
        await state.set_state(MyChannels.show)
        await callback.message.edit_text('📡📈 Your Channels',
                                         reply_markup=channels_new(get_channels(callback.from_user.id)))


@router.callback_query(MyChannels.remove)
async def edit_message(message: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if message.data == 'Yes':
        await state.set_state(MyChannels.show)
        channel_remover(message.from_user.id, data['editing_channel'][0]['channel_id'])
        await message.message.edit_text('Channel removed successfully')
        await message.message.answer('📡📈 Your Channels', reply_markup=channels_new(get_channels(message.from_user.id)))
    elif 'No' in message.data:
        await state.set_state(MyChannels.show)
        await message.message.edit_text('📡📈 Your Channels',
                                        reply_markup=channels_new(get_channels(message.from_user.id)))
    else:
        await message.answer('Unknown Choice\nTry again')


@router.message(MyChannels.count)
async def edit_message(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        await state.set_state(MyChannels.promo)
        await state.update_data(users_count=message.text)
        await message.answer('Send your message or post for broadcast', reply_markup=get_cancel())
    elif message.text == 'Cancel':
        data = await state.get_data()
        details = get_channels(message.from_user.id, data['editing_channel'][0]['channel_id'])
        await state.update_data(editing_channel=details)
        await message.answer(
            f"Channel Name:    {details[0]['channel_name']}\nChannel id:    `{details[0]['channel_id']}`",
            reply_markup=channels_btns(), parse_mode='Markdown')

    else:
        await message.answer('Please enter a number only')


@router.message(MyChannels.promo)
async def edit_message(message: types.Message, state: FSMContext):
    await state.set_state(MyChannels.run_promo)
    await state.update_data(message_id=message.message_id, forward_from=message.from_user.id,
                            buttons=message.reply_markup)
    await message.bot.copy_message(message.from_user.id, message.from_user.id, message.message_id,
                           reply_markup=message.reply_markup)
    await message.answer('Are you sure you want to broadcast this message', reply_markup=yesno())


@router.callback_query(MyChannels.run_promo)
async def edit_message(calback: types.CallbackQuery, state: FSMContext):
    await calback.message.delete()
    if calback.data == 'Yes':
        data = await state.get_data()
        clients = all_clients(calback.from_user.id, data['editing_channel'][0]['channel_id'], 'user_id')
        clients_ids = [i['user_id'] for i in clients]
        # bal = get_bal(calback.from_user.id)[0]['bal']
        if len(clients) == 0:
            await calback.message.answer('🚫👥 You don\'t have any user in this channel', reply_markup=get_keyboard())
        else:
            await calback.message.answer('Sending message to users 📤👥 ', reply_markup=get_keyboard())
            thread = Thread(target=n, args=(
            clients_ids, data['forward_from'], data['message_id'], data['buttons'], data['users_count'],calback.bot))
            thread.start()
        await state.clear()


    elif calback.data == 'No':
        await calback.message.answer('Cancelled', reply_markup=get_keyboard())
        await state.clear()


@router.callback_query(MyChannels.btn_edit)
async def edit_message(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'change':
        await state.set_state(MyChannels.greet_msg_edit)
        await callback.message.edit_text('Send New Post')

    elif callback.data == 'cancel':
        await state.set_state(MyChannels.edit)
        details = get_channels(callback.from_user.id)
        await state.update_data(editing_channel=details)
        await callback.message.edit_text(
            f"Channel Name:    {details[0]['channel_name']}\nChannel id:    `{details[0]['channel_id']}`",
            reply_markup=channels_btns(), parse_mode='Markdown')
    else:
        await callback.message.answer('Unknown choice')


@router.message(MyChannels.greet_msg_edit)
async def edit_message(message: types.Message, state: FSMContext):
    await state.set_state(MyChannels.greet_btn_edit)
    await message.answer(f'Greet message stored 📥')
    if message.reply_markup:
        await state.update_data(buttons=message.reply_markup.inline_keyboard)
    else:
        await state.update_data(buttons=None)

    await state.update_data(message_id=message.message_id,
                            message_chat=message.from_user.id)
    await message.bot.copy_message(message.chat.id, message.chat.id, message.message_id, reply_markup=message.reply_markup)
    await message.answer('Are you sure you want to set this Message', reply_markup=yesno())


@router.callback_query(MyChannels.greet_btn_edit)
async def edit_message(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'Yes':
        data = await state.get_data()
        editor('cm_channel_data', 'greet_msg', str(data['message_id']), data['editing_channel'][0]['channel_id'])
        editor('cm_channel_data', 'greet_msg_chat', str(callback.from_user.id),
               data['editing_channel'][0]['channel_id'])
        editor('cm_channel_data', 'btns', str(data['buttons']).replace('\'', '"'),
               data['editing_channel'][0]['channel_id'])

        await callback.message.edit_text('Greet Message Updated Successfully ✅📊')
        details = get_channels(callback.from_user.id, data['editing_channel'][0]['channel_id'])
        await state.update_data(editing_channel=details)
        await callback.message.answer(
            f"Channel Name:    {details[0]['channel_name']}\nChannel id:    `{details[0]['channel_id']}`",
            reply_markup=channels_btns(), parse_mode='Markdown')

        await state.set_state(MyChannels.edit)

    elif callback.data == 'No':
        await callback.message.edit_text('Cancelled', reply_markup=get_keyboard())
        await state.clear()
    else:
        await callback.message.answer('Unknown Choice')