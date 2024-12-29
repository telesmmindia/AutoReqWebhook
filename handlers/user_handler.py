from aiogram import Router, F
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from core.states import set_welcome
from core.texts import CHOOSE, CANCELLED, SEND_NEW_WELCOME_MSG, \
    GRT_SET_2_DEF, EDIT_OPTIONS, DEFAULT_ACCEPTTED_TXT, CONFIRM_SET_GREETING_MESSAGE, \
    GREET_MESSAGE_UPDATED, ALL_REQUEST_ACCEPT_DICT, DONT_KNOW_HOW_TO, BOT_WELCOME_DICT, GRT_MSG_DEFAULT
from keyboards.InlineKeyboard import get_keyboard, yesno, main_buttons, edit_btns, tutorial_link, promo_btn2
from keyboards.Replykeyboard import get_n_cancel
from models.database import bot_fetcher, udpate_welcome


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        bot_token = message.bot.token
        print(bot_token)
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
@router.callback_query(F.data == 'back')
async def add_channel(callback: CallbackQuery,state:FSMContext) -> None:
    await callback.message.edit_text(CHOOSE,reply_markup=main_buttons())
@router.message(AdminFilter())
async def start_admin_handler(message:Message,state:FSMContext):
    await state.clear()
    await message.answer(CHOOSE,reply_markup=main_buttons())

@router.callback_query(F.data=='request')
async def reqquest_handlersdaasdf(callback:CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.edit_text(DONT_KNOW_HOW_TO, reply_markup=tutorial_link(ALL_REQUEST_ACCEPT_DICT))
    await callback.message.answer(CHOOSE, reply_markup=get_keyboard())

@router.callback_query(F.data=='back-2_main')
async def back_to_ad(callback:CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.edit_text(CHOOSE,reply_markup=main_buttons())

@router.message(UserFilter())
async def start_user_handler(message:Message):
    details = bot_fetcher(message.bot.token)
    buttons = eval(details['btns'])
    try:
        buttons.append(promo_btn2(details['user_id']))
    except:
        buttons=InlineKeyboardMarkup(inline_keyboard=[promo_btn2(details['user_id'])])
    try:
        await message.bot.copy_message(message.from_user.id, details['user_id'], details['u_w_msg_id'],
                                   reply_markup=None if details['btns'] == 'None' else InlineKeyboardBuilder(buttons).as_markup())
    except:
        await message.answer(GRT_MSG_DEFAULT.format(message.from_user.first_name),reply_markup=buttons)


@router.callback_query(F.data=="welcome")
async def set_welcome_of_bot(message:Message,state:FSMContext):
    details = bot_fetcher(message.bot.token)
    await state.set_state(set_welcome.change_post)
    await message.bot.send_message(text=DONT_KNOW_HOW_TO,chat_id=message.from_user.id,reply_markup=tutorial_link(BOT_WELCOME_DICT))
    try:
        message_to_cum_on = await message.bot.copy_message(message.from_user.id,details['user_id'],details['u_w_msg_id'],
                                                       reply_markup = None if details['btns'] == 'None' else InlineKeyboardBuilder(eval(details['btns'])).as_markup())
        await message.bot.send_message(chat_id=message.from_user.id,text=EDIT_OPTIONS, reply_markup=edit_btns())
    except:
        await message.bot.send_message(chat_id=message.from_user.id,text=DEFAULT_ACCEPTTED_TXT)
        await message.bot.send_message(chat_id=message.from_user.id,text=EDIT_OPTIONS, reply_markup=edit_btns())

@router.callback_query(set_welcome.change_post)
async def change_post_fuinc(callback:CallbackQuery,state:FSMContext):
    if callback.data=='cancel':
        await callback.message.edit_text(CHOOSE,reply_markup=main_buttons())
        await state.clear()
    else:
        await callback.message.delete()
        await callback.message.answer(SEND_NEW_WELCOME_MSG,reply_markup=get_n_cancel())
        await state.set_state(set_welcome.get_welcome)

@router.message(set_welcome.get_welcome)
async def get_welcome_msg(message: Message,state:FSMContext):
    if message.text:
        if 'cancel' not in message.text.lower() :
            await state.set_state(set_welcome.confirmation)
            await state.update_data(message_id = message.message_id)
            if message.reply_markup:
                await state.update_data(buttons = message.reply_markup.inline_keyboard)
            else:
                await state.update_data(buttons = None)
            testis = await message.send_copy(chat_id=message.from_user.id,reply_markup=message.reply_markup)
            await testis.reply(CONFIRM_SET_GREETING_MESSAGE,reply_markup=yesno())
        else:
            await message.answer(CANCELLED,reply_markup=ReplyKeyboardRemove())
            await message.answer(CHOOSE,reply_markup=main_buttons())
            await state.clear()
    else:
        await state.set_state(set_welcome.confirmation)
        await state.update_data(message_id=message.message_id)
        if message.reply_markup:
            await state.update_data(buttons=message.reply_markup.inline_keyboard)
        else:
            await state.update_data(buttons=None)
        testis = await message.send_copy(chat_id=message.from_user.id, reply_markup=message.reply_markup)
        await testis.reply(CONFIRM_SET_GREETING_MESSAGE, reply_markup=yesno())

@router.callback_query(set_welcome.confirmation)
async def confirm_welcome(callback:CallbackQuery,state:FSMContext):
    if callback.data == 'Yes':
        data = await state.get_data()
        udpate_welcome(callback.bot.id,data['message_id'],str(data['buttons']).replace('\'','"'))
        await callback.message.delete()
        await callback.message.answer(GREET_MESSAGE_UPDATED,reply_markup=ReplyKeyboardRemove())
        await callback.message.answer(CHOOSE,reply_markup=main_buttons())
    else:
        await callback.message.edit_text(CANCELLED, reply_markup=main_buttons())
    await state.clear()






