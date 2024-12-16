from aiogram import Router, F
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from core.states import set_welcome
from core.texts import CHOOSE
from keyboards.InlineKeyboard import get_keyboard, yesno
from keyboards.Replykeyboard import get_n_cancel
from models.database import bot_fetcher, udpate_welcome


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        bot_token = message.bot.token
        bot_details = bot_fetcher(bot_token)
        return message.text == '/start' and message.from_user.id == bot_details['user_id'] and bot_details['bot_status'] ==1

class UserFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        bot_token = message.bot.token
        bot_details = bot_fetcher(bot_token)
        return message.text == '/start' and message.from_user.id != bot_details['user_id'] and bot_details['bot_status'] == 1

class SetWelcomeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        bot_token = message.bot.token
        bot_details = bot_fetcher(bot_token)
        return message.text == '/set_welcome' and message.from_user.id == bot_details['user_id'] and bot_details['bot_status'] ==1

router = Router(name="user_router")

@router.message(AdminFilter())
async def start_admin_handler(message:Message,state:FSMContext):
    await message.answer(CHOOSE,reply_markup=get_keyboard())

@router.message(UserFilter())
async def start_user_handler(message:Message):
    details = bot_fetcher(message.bot.token)
    await message.bot.copy_message(message.from_user.id, details['user_id'], details['u_w_msg_id'],
                                   reply_markup=None if details['btns'] == 'None' else InlineKeyboardBuilder(eval(details['btns'])).as_markup())


@router.message(SetWelcomeFilter())
async def set_welcome_of_bot(message:Message,state:FSMContext):
    details = bot_fetcher(message.bot.token)
    await message.answer('Your current welcome message is 👇')
    message_to_cum_on = await message.bot.copy_message(message.from_user.id,details['user_id'],details['u_w_msg_id'],
                                                       reply_markup = None if details['btns'] == 'None' else InlineKeyboardBuilder(eval(details['btns'])).as_markup())
    await message.bot.send_message(chat_id=message.from_user.id,text='Send New Welcome Message',reply_to_message_id=message_to_cum_on.message_id,reply_markup=get_n_cancel())
    await state.set_state(set_welcome.get_welcome)

@router.message(set_welcome.get_welcome)
async def get_welcome_msg(message: Message,state:FSMContext):
    if message.text:
        if message.text.lower() != 'cancel':
            await state.set_state(set_welcome.confirmation)
            await state.update_data(message_id = message.message_id)
            if message.reply_markup:
                await state.update_data(buttons = message.reply_markup.inline_keyboard)
            else:
                await state.update_data(buttons = None)
            testis = await message.send_copy(chat_id=message.from_user.id,reply_markup=message.reply_markup)
            await testis.reply('Are You Sure You want to set this message as welcome message',reply_markup=yesno())
        else:
            await message.answer('Cancelled Process',reply_markup=get_keyboard())
            await state.clear()
    else:
        await state.set_state(set_welcome.confirmation)
        await state.update_data(message_id=message.message_id)
        if message.reply_markup:
            await state.update_data(buttons=message.reply_markup.inline_keyboard)
        else:
            await state.update_data(buttons=None)
        testis = await message.send_copy(chat_id=message.from_user.id, reply_markup=message.reply_markup)
        await testis.reply('Are You Sure You want to set this message as welcome message', reply_markup=yesno())

@router.callback_query(set_welcome.confirmation)
async def confirm_welcome(callback:CallbackQuery,state:FSMContext):
    if callback.data == 'Yes':
        data = await state.get_data()
        udpate_welcome(callback.bot.id,data['message_id'],data['buttons'])
        await callback.message.edit_text('Updated Welcome Text',reply_markup=get_keyboard())
    else:
        await callback.message.edit_text('Cancelled Process', reply_markup=get_keyboard())
    await state.clear()






