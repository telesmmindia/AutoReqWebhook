from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.InlineKeyboard import get_keyboard, yesno, get_cancel, defaultn
from core.helpers import is_bot_admin
from core.states import AddChannel
from core.texts import WHT_IS_GRT_MSG, BOT_NOT_ADMIN, CHNL_ALRDY_ADDED, FRWD_POST_FRM_CHNL_ONLY, GRT_SET_2_DEF
from models.database import channel_checker, channel_data_inserter

router = Router(name="add_channel")

@router.callback_query(F.data=="Add Channel")
async def add_channel(message: types.CallbackQuery,state:FSMContext) -> None:
    await state.set_state(AddChannel.channel_id)
    await message.message.edit_text('Forward a post from your channel')

@router.message(AddChannel.channel_id)
async def channel_id_get(message: types.Message,state: FSMContext):
    if message.forward_from_chat and message.forward_from_chat.type == 'channel':
        find = channel_checker(message.forward_from_chat.id)
        if len(find)==0:
            await state.update_data(channel_id=message.forward_from_chat.id,channel_name=message.forward_from_chat.title)
            if await is_bot_admin(message.forward_from_chat.id,message.bot):
                await state.set_state(AddChannel.greet_msg_confirm)
                await message.answer(WHT_IS_GRT_MSG,reply_markup=defaultn(),parse_mode='Markdown')
            else:
                await message.reply(BOT_NOT_ADMIN.format(message.forward_from_chat.title))
        else:
            await message.answer(CHNL_ALRDY_ADDED,reply_markup=get_keyboard())
            await state.clear()
    else:
        await message.answer(FRWD_POST_FRM_CHNL_ONLY)

@router.callback_query(AddChannel.greet_msg_confirm)
async def channel_greet_get(callback: types.CallbackQuery,state:FSMContext):
    await callback.answer('choose')
    data = await state.get_data()
    if callback.data == 'default':
        data['greet_msg'] = '0'
        await callback.message.answer(GRT_SET_2_DEF,parse_mode='Markdown')
        channel_data_inserter(bot_id=callback.bot.id,channel_id=data['channel_id'], user_id=callback.from_user.id, greet_msg=data['greet_msg'],channel_name=data['channel_name'])
        await callback.message.answer('Channel Data Successfully ✅📊', reply_markup=get_keyboard())
        await callback.message.delete()
        await state.clear()
    elif callback.data == 'custom':
        await state.set_state(AddChannel.greet_msg)
        await callback.message.answer('Send a Greeting Message')

@router.message(AddChannel.greet_msg)
async def channel_greet_get(message: types.Message,state:FSMContext):
    await state.update_data(greet_message_id = message.message_id,
                            greet_message_chat_id = message.chat.id,greet_buttons = message.reply_markup.inline_keyboard)
    await state.set_state(AddChannel.btn_check)
    await message.bot.copy_message(message.chat.id, message.chat.id, message.message_id,reply_markup=message.reply_markup)
    await message.answer('Are you sure you want to set this Message',reply_markup=yesno())

@router.callback_query(AddChannel.btn_check)
async def channel_btn_get(callback: types.CallbackQuery,state:FSMContext):
    await callback.answer('choose')
    if callback.data == 'Yes':
        data = await state.get_data()
        channel_data_inserter(bot_id=callback.bot.id,channel_id=data['channel_id'], user_id=callback.from_user.id, greet_msg=data['greet_message_id'],channel_name=data['channel_name'],greet_msg_chat=data['greet_message_chat_id'],btns=data['greet_buttons'])
        await callback.message.reply('Added Data Successfully ✅📊', reply_markup=get_keyboard())
        await callback.message.delete()
        await state.clear()

    elif callback.data=='No':
        await callback.message.reply('Cancelled', reply_markup=get_keyboard())
        await callback.message.delete()
        await state.clear()
    else:
        await callback.message.answer('Unknown Choice')