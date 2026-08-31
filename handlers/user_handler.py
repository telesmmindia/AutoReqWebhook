from aiogram import Router, F
from aiogram.filters import BaseFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LinkPreviewOptions
from core.greetings import send_stored_message, snapshot_message
from core.states import set_welcome
from core.texts import CHOOSE, CANCELLED, SEND_NEW_WELCOME_MSG, \
    GRT_SET_2_DEF, EDIT_OPTIONS, get_default_accepted_txt, CONFIRM_SET_GREETING_MESSAGE, \
    GREET_MESSAGE_UPDATED, ALL_REQUEST_ACCEPT_DICT, DONT_KNOW_HOW_TO, BOT_WELCOME_DICT, GRT_MSG_DEFAULT, \
    get_owner_help_text, get_user_help_text
from keyboards.InlineKeyboard import get_keyboard, yesno, main_buttons, edit_btns, tutorial_link, promo_btn2, \
    owner_support_btn
from keyboards.Replykeyboard import get_n_cancel
from models.database import bot_fetcher, udpate_welcome, all_clients_count, check_premium, set_welcome_data


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
@router.callback_query(F.data == 'back')
async def add_channel(callback: CallbackQuery,state:FSMContext) -> None:
    await callback.message.edit_text(CHOOSE, reply_markup=main_buttons(), disable_web_page_preview=True)
@router.message(AdminFilter())
async def start_admin_handler(message:Message,state:FSMContext):
    await state.clear()
    await message.answer(CHOOSE, reply_markup=main_buttons(), disable_web_page_preview=True)


async def _owner_username(bot, owner_id):
    """The clone bot's owner @username, so support points at them and not at us.
    The owner has always started their own bot, so get_chat resolves."""
    try:
        chat = await bot.get_chat(owner_id)
        return chat.username
    except Exception:
        return None


@router.message(Command('help'))
async def help_handler(message: Message, state: FSMContext):
    bot_details = bot_fetcher(message.bot.token)
    if not bot_details or bot_details['bot_status'] != 1:
        return
    me = await message.bot.get_me()
    if message.from_user.id == bot_details['user_id']:
        await state.clear()
        await message.answer(get_owner_help_text(me.username), disable_web_page_preview=True)
        await message.answer(CHOOSE, reply_markup=main_buttons(), disable_web_page_preview=True)
    else:
        owner = await _owner_username(message.bot, bot_details['user_id'])
        await message.answer(
            get_user_help_text(me.username, owner),
            reply_markup=owner_support_btn(owner, bot_details['user_id']),
            disable_web_page_preview=True,
        )


@router.callback_query(F.data=='request')
async def reqquest_handlersdaasdf(callback:CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.edit_text(DONT_KNOW_HOW_TO, reply_markup=tutorial_link(ALL_REQUEST_ACCEPT_DICT), disable_web_page_preview=True)
    await callback.message.answer(CHOOSE, reply_markup=get_keyboard(), disable_web_page_preview=True)

@router.message(F.text=='/users',F.from_user.id ==7425140710)
async def back_to_ad(message:Message):
    users = all_clients_count()
    await message.answer(f'<b>{users[0]["distinct_user_count"]}</b> users are using this bot ')


@router.callback_query(F.data=='back-2_main')
async def back_to_ad(callback:CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.edit_text(CHOOSE, reply_markup=main_buttons(), disable_web_page_preview=True)

@router.message(UserFilter())
async def start_user_handler(message:Message):
    details = bot_fetcher(message.bot.token)
    raw_buttons = eval(details['btns'])
    if str(details['bot_id']) != '8130984037':
        promo = promo_btn2(details['user_id'])
        if promo:
            raw_buttons.append(promo)
    buttons = InlineKeyboardMarkup(inline_keyboard=raw_buttons)
    try:
        # Snapshot-first so the owner's premium / animated emoji survive; falls
        # back internally to copying their original message.
        await send_stored_message(message.bot, message.from_user.id, details.get('welcome_data'),
                                  details['user_id'], details['u_w_msg_id'], reply_markup=buttons)
    except:
        print(buttons)
        bot_details = await message.bot.get_me()
        await message.answer(GRT_MSG_DEFAULT.format(message.from_user.first_name, bot_details.username), reply_markup=buttons, disable_web_page_preview=True)


@router.callback_query(F.data=="welcome")
async def set_welcome_of_bot(message:Message,state:FSMContext):
    details = bot_fetcher(message.bot.token)
    await state.set_state(set_welcome.change_post)
    await message.bot.send_message(text=DONT_KNOW_HOW_TO, chat_id=message.from_user.id, reply_markup=tutorial_link(BOT_WELCOME_DICT), disable_web_page_preview=True)
    try:
        await send_stored_message(
            message.bot, message.from_user.id, details.get('welcome_data'),
            details['user_id'], details['u_w_msg_id'],
            reply_markup=None if details['btns'] == 'None'
            else InlineKeyboardBuilder(eval(details['btns'])).as_markup())
        await message.bot.send_message(chat_id=message.from_user.id, text=EDIT_OPTIONS, reply_markup=edit_btns(), disable_web_page_preview=True)
    except:
        is_premium = check_premium(details['user_id'])
        await message.bot.send_message(chat_id=message.from_user.id, text=get_default_accepted_txt(message.from_user.first_name, "your channel", is_premium), disable_web_page_preview=True)
        await message.bot.send_message(chat_id=message.from_user.id, text=EDIT_OPTIONS, reply_markup=edit_btns(), disable_web_page_preview=True)

@router.callback_query(set_welcome.change_post)
async def change_post_fuinc(callback:CallbackQuery,state:FSMContext):
    if callback.data=='cancel':
        await callback.message.edit_text(CHOOSE, reply_markup=main_buttons(), disable_web_page_preview=True)
        await state.clear()
    else:
        await callback.message.delete()
        await callback.message.answer(SEND_NEW_WELCOME_MSG, reply_markup=get_n_cancel(), disable_web_page_preview=True)
        await state.set_state(set_welcome.get_welcome)

@router.message(set_welcome.get_welcome)
async def get_welcome_msg(message: Message,state:FSMContext):
    if message.text:
        if 'cancel' not in message.text.lower() :
            await state.set_state(set_welcome.confirmation)
            await state.update_data(message_id = message.message_id,
                                    welcome_data = snapshot_message(message))
            if message.reply_markup:
                await state.update_data(buttons = message.reply_markup.inline_keyboard)
            else:
                await state.update_data(buttons = None)
            testis = await message.answer(
                message.html_text,
                reply_markup=message.reply_markup,
                parse_mode='HTML',
                link_preview_options=LinkPreviewOptions(is_disabled=True)
            )
            await testis.reply(CONFIRM_SET_GREETING_MESSAGE,reply_markup=yesno())
        else:
            await message.answer(CANCELLED, reply_markup=ReplyKeyboardRemove(), disable_web_page_preview=True)
            await message.answer(CHOOSE, reply_markup=main_buttons(), disable_web_page_preview=True)
            await state.clear()
    else:
        snapshot = snapshot_message(message)
        await state.set_state(set_welcome.confirmation)
        await state.update_data(message_id=message.message_id, welcome_data=snapshot)
        if message.reply_markup:
            await state.update_data(buttons=message.reply_markup.inline_keyboard)
        else:
            await state.update_data(buttons=None)
        # Echo it back the way users will receive it, premium emoji included.
        testis = await send_stored_message(message.bot, message.from_user.id, snapshot,
                                           message.chat.id, message.message_id,
                                           reply_markup=message.reply_markup)
        # copy_message (the no-snapshot fallback) hands back a MessageId, which
        # can't be replied to -- reply to the owner's own message instead.
        reply_target = testis if isinstance(testis, Message) else message
        await reply_target.reply(CONFIRM_SET_GREETING_MESSAGE, reply_markup=yesno())

@router.callback_query(set_welcome.confirmation)
async def confirm_welcome(callback:CallbackQuery,state:FSMContext):
    if callback.data == 'Yes':
        data = await state.get_data()
        udpate_welcome(callback.bot.id,data['message_id'],str(data['buttons']).replace('\'','"'))
        set_welcome_data(callback.bot.id, data.get('welcome_data'))
        await callback.message.delete()
        await callback.message.answer(GREET_MESSAGE_UPDATED, reply_markup=ReplyKeyboardRemove(), disable_web_page_preview=True)
        await callback.message.answer(CHOOSE, reply_markup=main_buttons(), disable_web_page_preview=True)
    else:
        await callback.message.edit_text(CANCELLED, reply_markup=main_buttons(), disable_web_page_preview=True)
    await state.clear()






