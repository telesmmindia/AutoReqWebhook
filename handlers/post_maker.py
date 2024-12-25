import ast
import re
from secrets import token_hex
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery, ReplyKeyboardRemove
from colorama import Fore,Style
import traceback


from keyboards.InlineKeyboard import main_buttons, edit_msg, get_cancel, inline_back_button, share_save, buttons_btn, \
    btns_list, select_channels, share_ata_attach_btn, PROMO_BTN
from keyboards.Replykeyboard import back_button, get_n_cancel
from core.states import post_create
from core.texts import FWD_POST_FR_BTN, HOW_2_USE_POST_MKR, LNK_FRMT, INCRT_BTN_URL, CHOOSE, START_TEXT, \
    CANNOT_EDIT_STICKERS, YOUR_POST, CANCELLED, SEND_TEXT_FOR_BUTTON, NO_BUTTONS_ADDED, ENTER_TEXT_ONLY, BUTTON_SAVED, \
    MAX_BUTTONS_LIMIT, SHARE_POST, UR_BTN, UR_BTN_IS, SND_POST_FR_BTN_ADD, MSG_SNT_TO_CHANNEL, SELECT_CHANNELS, \
    ENTER_A_NAME_FOR_BUTTON_SET, BUTTON_INSERTED, MSG_SNT_TO_CHANNEL_ALL
from models.database import insert_posts, fetch_buttons, fetch_btn, insert_buttons, get_channels
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

router = Router(name="post_maker")


@router.callback_query(F.data == 'post-land')
async def schedule_handler(callback: types.CallbackQuery,state:FSMContext):
    inline_mode=(await callback.bot.get_me()).supports_inline_queries
    if inline_mode:
        await callback.answer()
        await state.set_state(post_create.what_do_you_mean)
        await callback.message.edit_text(CHOOSE,reply_markup=buttons_btn())
    else:
        await callback.message.edit_text("Please Enable Inline Mode!")
        await callback.message.answer(CHOOSE,reply_markup=main_buttons())

@router.callback_query(post_create.what_do_you_mean)
async def soemthign(callback:types.CallbackQuery,state:FSMContext):
    if callback.data == 'add-button':
        await state.set_state(post_create.check_message)
        await callback.message.delete()
        await callback.message.answer(FWD_POST_FR_BTN, reply_markup=get_n_cancel())
    elif callback.data == 'my-buttons':
        await state.set_state(post_create.add_button_to_post)
        user_buttons = fetch_buttons(callback.from_user.id)
        await callback.message.edit_text(UR_BTN, reply_markup=btns_list(user_buttons))
    elif 'back' in callback.data:
        await callback.message.edit_text(CHOOSE,reply_markup=main_buttons())



@router.callback_query(post_create.add_button_to_post)
async def add_btn_to_post(callback: CallbackQuery,state:FSMContext):
    try:
        if callback.data =='back':
            await state.set_state(post_create.what_do_you_mean)
            await callback.message.edit_text(CHOOSE, reply_markup=buttons_btn())
        else:
            btn = fetch_btn(callback.data)
            await state.update_data(btns_to_attach = eval(btn['buttons']),btn_id = btn['button_id'])
            await state.set_state(post_create.kaunsa_post_may_daalna_btn)
            await callback.message.edit_text(UR_BTN_IS,reply_markup=InlineKeyboardMarkup(inline_keyboard=eval(btn['buttons'])))
            await callback.message.answer(SND_POST_FR_BTN_ADD,reply_markup=get_n_cancel())

    except Exception as error:
        print(Fore.RED + str(error) + Style.RESET_ALL)
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)


@router.message(post_create.kaunsa_post_may_daalna_btn)
async def attach_btn(message:types.Message,state:FSMContext):
    if message.text == '❌ Cancel':
        await state.set_state(post_create.add_button_to_post)
        user_buttons = fetch_buttons(message.from_user.id)
        await message.answer(CANCELLED, reply_markup=types.ReplyKeyboardRemove())
        await message.answer(UR_BTN, reply_markup=btns_list(user_buttons))
    else:
        data = await state.get_data()
        file_id = None
        caption = None
        text = None
        if message.sticker:
            await message.answer(CANNOT_EDIT_STICKERS)
        else:
            for media_type in ['photo', 'video', 'audio', 'animation', 'document', 'voice']:
                media = getattr(message, media_type, None)
                if media:
                    if media_type == 'photo':
                        file_id = media[0].file_id
                        break
                    elif media_type in ['animation','audio','voice','video','document']:
                        file_id = media.file_id
                        break
                    else:
                        file_id = media['file_id']
                        break
        if file_id is None:
            text = message.text
        else:
            caption = message.caption

        media_handlers = {
            'photo': message.answer_photo,
            'video': message.answer_video,
            'audio': message.answer_audio,
            'animation': message.answer_animation,
        }
        if file_id:
            for media_type, handler in media_handlers.items():
                if getattr(message, media_type, None):
                    x = await handler(file_id, caption=caption,
                                      reply_markup=InlineKeyboardMarkup(inline_keyboard=data['btns_to_attach']))
                    break
        else:
            x = await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=data['btns_to_attach']))

        await state.update_data(to_reply=x)
        print(data['btn_id'])
        await x.reply(SHARE_POST.format("BOT NAME",data['btn_id']), reply_markup=share_ata_attach_btn(f'share {data["btn_id"]}'))
        await state.update_data(button_id=data['btn_id'], buttons=str(data['btns_to_attach']), to_copy_if=x.message_id)
        await state.set_state(post_create.after_hour)


@router.message(post_create.check_message)
async def schedule_handle(message: types.Message, state: FSMContext):
    if "cancel" in message.text.lower():
        await state.set_state(post_create.what_do_you_mean)
        await message.answer(CANCELLED,reply_markup=ReplyKeyboardRemove())
        await message.answer(CHOOSE, reply_markup=buttons_btn())
    else:
        if message.text != '⬅️ Back':
            if message.sticker:
                await message.answer(CANNOT_EDIT_STICKERS)
            else:
                await state.set_state(post_create.post_edit)
                file_id = None
                caption = None
                text = None
                for media_type in ['photo', 'video', 'audio', 'animation', 'document', 'voice']:
                    media = getattr(message, media_type, None)
                    if media:
                        await state.update_data(media_type=media_type)
                        if media_type == 'photo':
                            print(media)
                            file_id = media[0].file_id
                            break
                        elif media_type in ['animation','audio','voice','video','document']:
                            file_id = media.file_id
                            break
                        else:
                            file_id = media['file_id']
                            break

                if file_id is None:
                    text = message.text
                    await state.update_data(text=text, file_id=None, caption=None)
                else:
                    caption = message.caption
                    await state.update_data(text=None, file_id=file_id, caption=caption)
                await state.update_data(url_post=[])
                await message.answer(YOUR_POST, reply_markup=types.ReplyKeyboardRemove())
                media_handlers = {
                    'photo': message.reply_photo,
                    'video': message.reply_video,
                    'audio': message.reply_audio,
                    'animation': message.reply_animation,
                }

                if message.reply_markup:
                    keyboard = edit_msg(buttons=message.reply_markup.inline_keyboard,
                                        is_it_the_very_first_with_reply_markup=True)
                else:
                    keyboard = edit_msg(buttons=[])
                await state.update_data(keyboard=keyboard)

                if file_id:
                    for media_type, handler in media_handlers.items():
                        if getattr(message, media_type, None):
                            x = await handler(file_id, caption=caption,
                                              reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
                            break
                else:
                    x = await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

        else:
            await message.answer(CANCELLED, reply_markup=types.ReplyKeyboardRemove())
            await message.answer(START_TEXT, reply_markup=main_buttons())
            await state.clear()


@router.callback_query(post_create.post_edit)
async def schedule_handle(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('choose')
    data = await state.get_data()
    if '-' in callback.data:
        add_to_row, add_to_column = callback.data.split('-')
        # print('when you click',add_to_row,add_to_column)
        await state.update_data(add_to_row=add_to_row, add_to_column=add_to_column)
        await state.set_state(post_create.button_text)
        await callback.message.answer(SEND_TEXT_FOR_BUTTON, reply_markup=get_n_cancel())

    elif callback.data == 'post':
        media_handlers = {
            'photo': callback.bot.send_photo,
            'video': callback.bot.send_video,
            'audio': callback.bot.send_audio,
            'animation': callback.bot.send_animation,
        }
        keyboard = data['keyboard']
        for row in keyboard:
            if row:
                row.pop()
        keyboard = keyboard[:-2]
        keyboard.append(PROMO_BTN)
        unique_button_id = token_hex(4)
        bot_ka_details = await callback.bot.get_me()
        if data['file_id']:
            to_reply = await media_handlers[data['media_type']](callback.from_user.id, data['file_id'],
                                                                caption=data['caption'],
                                                                reply_markup=InlineKeyboardMarkup(
                                                                    inline_keyboard=keyboard))
            insert_posts(bot_ka_details.id, callback.from_user.id, unique_button_id, data['caption'], data['file_id'],
                         unique_button_id,
                         str(keyboard).replace('\"', '\''))
        else:
            to_reply = await callback.message.answer(data['text'],
                                                     reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
            insert_posts(bot_ka_details.id, callback.from_user.id, unique_button_id, data['text'], data['file_id'],
                         unique_button_id,
                         str(keyboard).replace('\"', '\''))

        await to_reply.reply(SHARE_POST.format(bot_ka_details.username,unique_button_id), reply_markup=share_save(f'share {unique_button_id}'))

        await state.update_data(button_id =unique_button_id,buttons = str(keyboard),to_copy_if = to_reply.message_id)
        await callback.message.delete()
        await state.set_state(post_create.after_hour)

@router.message(post_create.button_text)
async def button_adder(message: types.Message, state: FSMContext):
    if message.text:
        if message.text.lower() == 'cancel':
            await message.answer(CANCELLED, reply_markup=types.ReplyKeyboardRemove())
            await message.answer(START_TEXT, reply_markup=main_buttons())
            await state.clear()
        else:
            await state.set_state(post_create.button_link)
            await state.update_data(a=message.text)
            await message.answer(LNK_FRMT, reply_markup=get_n_cancel())
    else:
        await message.answer(ENTER_TEXT_ONLY)


@router.message(post_create.button_link)
async def button_adder(message: types.Message, state: FSMContext):
    li = list(message.text)
    if "cancel" in message.text.lower():
        await message.answer(CANCELLED, reply_markup=ReplyKeyboardRemove())
        await state.set_state(post_create.what_do_you_mean)
        await message.answer(CHOOSE, reply_markup=buttons_btn())
    else:
        if li[0] == "@":
            url = message.text
            match = 1
        else:
            substrings = message.text.split("-")
            url = substrings[-1].strip()
            pattern = r'^https?://[\w\-]+(\.[\w\-]+)+[/#?]?.*$'
            match = re.match(pattern, url)

        if match or li[0] == '@':
            data = await state.get_data()
            if len(data['url_post']) <= 5:
                data['url_post'].append({f"{data['a']}": f"{url}"})
                await message.answer(BUTTON_SAVED,reply_markup=ReplyKeyboardRemove())
                await state.set_state(post_create.post_edit)
                if data['file_id']:  # if it has a photo or video
                    media_handlers = {
                        'photo': message.reply_photo,
                        'video': message.reply_video,
                        'audio': message.reply_audio,
                        'animation': message.reply_animation,
                    }
                    keyboard = data['keyboard']
                    keyboard = edit_msg(ast.literal_eval(str(data['url_post'])), keyboard, data['add_to_row'],
                                        data['add_to_column'])
                    await state.update_data(keyboard=keyboard)
                    await state.update_data(url_post=[])
                    await media_handlers[data['media_type']](data['file_id'], caption=data['caption'],
                                                             reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

                else:
                    keyboard = data['keyboard']
                    keyboard = edit_msg(ast.literal_eval(str(data['url_post'])), keyboard, data['add_to_row'],
                                        data['add_to_column'])
                    await state.update_data(keyboard=keyboard)
                    await state.update_data(url_post=[])
                    await message.answer(data['text'], reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
            else:
                await message.answer(MAX_BUTTONS_LIMIT)
        else:
            await message.answer(INCRT_BTN_URL)

@router.callback_query(post_create.after_hour)
async def save_bttn(callback:types.CallbackQuery,state:FSMContext):
    if callback.data=='save':
        await callback.message.answer(ENTER_A_NAME_FOR_BUTTON_SET,reply_markup=get_n_cancel())
        await state.set_state(post_create.save_button)
    elif callback.data == 'channel':
        await state.set_state(post_create.handle_channel_send)
        channels = get_channels(callback.from_user.id)
        to_send = []
        for channel in channels:
            to_send.append({channel['channel_name'] : f'{channel["channel_id"]}/0'})
        await state.update_data(to_send = to_send)
        await callback.message.answer(SELECT_CHANNELS,reply_markup=select_channels(to_send))

    elif callback.data == 'main':
        await callback.message.delete()
        await callback.message.answer(CHOOSE, reply_markup=main_buttons())
        await state.clear()

@router.callback_query(post_create.handle_channel_send)
async def handle_channel_sng(callback:CallbackQuery,state:FSMContext):
    await callback.answer()
    if callback.data == 'done':
        data = await state.get_data()
        to_send = data['to_send']
        for dictionary in to_send:
            for key, value in dictionary.items():
                channel_id, statee = value.split('/')
                if statee == '1':
                    try:
                        await callback.bot.copy_message(
                            chat_id=int(channel_id),
                            from_chat_id=callback.from_user.id
                            , message_id=int(data['to_copy_if']),
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=eval(data['buttons'])))
                    except Exception as e:
                        print(Fore.RED + str(e) + Style.RESET_ALL)
                        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
                        await callback.message.answer(f'Cannot Send to {key}\nERROR : {e}')

        await callback.message.edit_text(MSG_SNT_TO_CHANNEL)
        await callback.message.answer(CHOOSE, reply_markup=main_buttons())
        await state.clear()
    elif callback.data == 'all':
        data = await state.get_data()
        to_send = data['to_send']
        for dictionary in to_send:
            for key, value in dictionary.items():
                channel_id, statee = value.split('/')
                try:
                    await callback.bot.copy_message(
                        chat_id=int(channel_id),
                        from_chat_id=callback.from_user.id
                        , message_id=int(data['to_copy_if']),
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=eval(data['buttons'])))
                except Exception as e:
                    print(Fore.RED + str(e) + Style.RESET_ALL)
                    print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
                    await callback.message.answer(f'Cannot Send to {key}\nERROR : {e}')

        await callback.message.edit_text(MSG_SNT_TO_CHANNEL_ALL)
        await callback.message.answer(CHOOSE, reply_markup=main_buttons())
        await state.clear()

    elif callback.data == 'cancel':
        await callback.message.answer(CANCELLED, reply_markup=ReplyKeyboardRemove())
        await callback.message.answer(CHOOSE, reply_markup=main_buttons())
        await state.clear()
    else:
        data = await state.get_data()
        to_send = data['to_send']
        channel_id,current_state = callback.data.split('/')
        for dictionary in to_send:
            for key, value in dictionary.items():
                if channel_id in value:
                    dictionary[key] = f"{channel_id}/{'0' if current_state =='1' else '1'}"
                    break
        await callback.message.edit_text(SELECT_CHANNELS,reply_markup=select_channels(to_send))


@router.message(post_create.save_button)
async def saving_Btn(message:types.Message,state:FSMContext):
    data = await state.get_data()
    if "cancel" in message.text.lower():
        await message.answer(CANCELLED,reply_markup=ReplyKeyboardRemove())
        await message.answer(CHOOSE,reply_markup=main_buttons())
        await state.clear()
    else:
        insert_buttons(message.from_user.id,data['button_id'],message.text,data['buttons'])
        await message.answer(BUTTON_INSERTED,reply_markup=ReplyKeyboardRemove())
        await message.answer(CHOOSE, reply_markup=main_buttons())
        await state.clear()