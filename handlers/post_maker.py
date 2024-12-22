import ast
import re
from secrets import token_hex
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, CallbackQuery

from keyboards.InlineKeyboard import  main_buttons, edit_msg, get_cancel, inline_back_button, share_save
from keyboards.Replykeyboard import back_button, get_n_cancel
from core.states import post_create
from core.texts import FWD_POST_FR_BTN, HOW_2_USE_POST_MKR, LNK_FRMT, INCRT_BTN_URL, CHOOSE, START_TEXT, \
    CANNOT_EDIT_STICKERS, YOUR_POST, CANCELLED, SEND_TEXT_FOR_BUTTON, NO_BUTTONS_ADDED, ENTER_TEXT_ONLY, BUTTON_SAVED, \
    MAX_BUTTONS_LIMIT, SHARE_POST
from models.database import insert_posts

router = Router(name="post_maker")


@router.callback_query(F.data == 'post-land')
async def schedule_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(post_create.check_message)
    await callback.message.answer(FWD_POST_FR_BTN, reply_markup=back_button())
    await callback.message.delete()


@router.message(post_create.check_message)
async def schedule_handle(message: types.Message, state: FSMContext):
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
                    elif media_type == 'animation':
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
        if data['file_id']:
            to_reply = await media_handlers[data['media_type']](callback.from_user.id, data['file_id'],
                                                                caption=data['caption'],
                                                                reply_markup=InlineKeyboardMarkup(
                                                                    inline_keyboard=keyboard))
        else:
            to_reply = await callback.message.answer(data['text'],
                                                     reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
        unique_button_id = token_hex(4)
        bot_ka_details = await callback.bot.get_me()
        await to_reply.reply(SHARE_POST.format(bot_ka_details.username,unique_button_id), reply_markup=share_save(f'share {unique_button_id}'))
        insert_posts(bot_ka_details.id,callback.from_user.id, unique_button_id, data['text'], data['file_id'], unique_button_id,
                     str(keyboard).replace('\"', '\''))

        await callback.message.answer(CHOOSE, reply_markup=main_buttons())
        await callback.message.delete()


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
            await message.answer(LNK_FRMT, reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer(ENTER_TEXT_ONLY)


@router.message(post_create.button_link)
async def button_adder(message: types.Message, state: FSMContext):
    li = list(message.text)
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
            await message.answer(BUTTON_SAVED)
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
                print('after everything', keyboard)
                await message.answer(data['text'], reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
        else:
            await message.answer(MAX_BUTTONS_LIMIT)
    else:
        await message.answer(INCRT_BTN_URL)

