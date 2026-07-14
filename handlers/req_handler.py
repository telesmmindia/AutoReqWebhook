import traceback

from aiogram import types, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.texts import get_default_accepted_txt
from keyboards.InlineKeyboard import promo_btn, promo_btn2
from models.database import unlinked_users, all_channels_id, all_channels_details, find_client, insert_clients, check_premium

router = Router(name="request_handler")

@router.chat_join_request()
async def handle_join_request(message: types.message):
    await message.bot.approve_chat_join_request(message.chat.id, message.from_user.id)
    try:
        print(message)
        find = all_channels_id()
        if int(message.chat.id) in find:
            details = all_channels_details(message.chat.id)
            print(f"[DEBUG join_request] channel_id={message.chat.id} row={details[0]}")
            if details[0]['greet_msg']!=0:
                if find_client(message.chat.id,message.from_user.id,details[0]['user_id'])==0:
                    insert_clients(message.bot.id,message.chat.id, message.from_user.id, details[0]['channel_name'],details[0]['user_id'])
                else:
                    print('User Already in database')

                if details[0]['btns'] !=0 and details[0]['btns']  not in ['None','0']:
                    try:
                        try:
                            buttons = eval(details[0]['btns'])
                        except Exception as eval_err:
                            print(f"[DEBUG join_request] eval(btns) FAILED: {eval_err!r} raw_btns={details[0]['btns']!r}")
                            raise
                        if str(details[0]['bot_id']) != '8130984037':
                            buttons.append(promo_btn2(details[0]['user_id']))
                            # Remove empty lists appended by promo_btn2 if premium
                            buttons = [b for b in buttons if b]
                        try:
                            await message.bot.copy_message(message.from_user.id,details[0]['greet_msg_chat'],details[0]['greet_msg'],
                                               reply_markup= None if details[0]['btns']=='None' else InlineKeyboardBuilder(buttons).as_markup()
                                               )
                        except Exception as copy_err:
                            print(f"[DEBUG join_request] copy_message FAILED: {copy_err!r} greet_msg_chat={details[0]['greet_msg_chat']!r} greet_msg={details[0]['greet_msg']!r}")
                            raise
                    except Exception as e:
                        print(traceback.format_exc())
                        is_premium = check_premium(details[0]['user_id'])
                        promo_buttons = promo_btn2(details[0]['user_id'])
                        reply_markup = InlineKeyboardMarkup(inline_keyboard=[promo_buttons]) if promo_buttons else None
                        await message.bot.send_message(message.from_user.id,
                                                       get_default_accepted_txt(message.from_user.first_name,
                                                                                    message.chat.title, is_premium),
                                                       disable_web_page_preview=True, parse_mode='html',reply_markup=reply_markup)

                else:
                    try:
                        await message.bot.copy_message(message.from_user.id, details[0]['greet_msg_chat'], details[0]['greet_msg'])
                    except:
                        is_premium = check_premium(details[0]['user_id'])
                        promo_buttons = promo_btn2(details[0]['user_id'])
                        reply_markup = InlineKeyboardMarkup(inline_keyboard=[promo_buttons]) if promo_buttons else None
                        await message.bot.send_message(message.from_user.id,
                                                       get_default_accepted_txt(message.from_user.first_name,
                                                                                    message.chat.title, is_premium),
                                                       disable_web_page_preview=True, parse_mode='html',reply_markup=reply_markup)

            elif details[0]['greet_msg']==0:
                if find_client(message.chat.id, message.from_user.id, details[0]['user_id']) == 0:
                    insert_clients(message.bot.id,message.chat.id, message.from_user.id, details[0]['channel_name'],details[0]['user_id'])
                else:
                    print('User Already in database')
                is_premium = check_premium(details[0]['user_id'])
                await message.bot.send_message(message.from_user.id, get_default_accepted_txt(message.from_user.first_name,message.chat.title, is_premium),disable_web_page_preview=True,parse_mode='html')
                pass
        else:
            is_premium = False # Not found in DB, assume non-premium or doesn't matter
            await message.bot.send_message(message.from_user.id, get_default_accepted_txt(message.from_user.first_name,message.chat.title, is_premium),disable_web_page_preview=True,parse_mode='html')
            unlinked_users(message.from_user.id, message.chat.id, message.chat.title)
            pass
    except Exception as e:
        print(traceback.format_exc())
        print('Channel not in database')
        unlinked_users(message.from_user.id,message.chat.id,message.chat.title)
        pass