import traceback

from aiogram import types, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.texts import DEFAULT_ACCEPTTED_TXT
from keyboards.InlineKeyboard import PROMO_BTN
from models.database import unlinked_users, all_channels_id, all_channels_details, find_client, insert_clients

router = Router(name="request_handler")

@router.chat_join_request()
async def handle_join_request(message: types.message):
    await message.bot.approve_chat_join_request(message.chat.id, message.from_user.id)
    try:
        print(message)
        find = all_channels_id()
        if int(message.chat.id) in find:
            details = all_channels_details(message.chat.id)
            #print(details)
            if details[0]['greet_msg']!=0:
                if find_client(message.chat.id,message.from_user.id,details[0]['user_id'])==0:
                    insert_clients(message.bot.id,message.chat.id, message.from_user.id, details[0]['channel_name'],details[0]['user_id'])
                else:
                    print('User Already in database')
                if details[0]['btns'] !=0 and details[0]['btns']  not in ['None','0']:
                    try:
                        buttons = eval(details[0]['btns'])
                        buttons.append(PROMO_BTN)
                        await message.bot.copy_message(message.from_user.id,details[0]['greet_msg_chat'],details[0]['greet_msg'],
                                           reply_markup= None if details[0]['btns']=='None' else InlineKeyboardBuilder(buttons).as_markup()
                                           )
                    except:
                        await message.bot.send_message(message.from_user.id,
                                                       DEFAULT_ACCEPTTED_TXT.format(message.from_user.first_name,
                                                                                    message.chat.title),
                                                       disable_web_page_preview=True, parse_mode='html',reply_markup=InlineKeyboardMarkup(inline_keyboard=PROMO_BTN))

                else:
                    try:
                        await message.bot.copy_message(message.from_user.id, details[0]['greet_msg_chat'], details[0]['greet_msg'])
                    except:
                        await message.bot.send_message(message.from_user.id,
                                                       DEFAULT_ACCEPTTED_TXT.format(message.from_user.first_name,
                                                                                    message.chat.title),
                                                       disable_web_page_preview=True, parse_mode='html',reply_markup=InlineKeyboardMarkup(inline_keyboard=PROMO_BTN))

            elif details[0]['greet_msg']==0:
                if find_client(message.chat.id, message.from_user.id, details[0]['user_id']) == 0:
                    insert_clients(message.bot.id,message.chat.id, message.from_user.id, details[0]['channel_name'],details[0]['user_id'])
                else:
                    print('User Already in database')
                await message.bot.send_message(message.from_user.id, DEFAULT_ACCEPTTED_TXT.format(message.from_user.first_name,message.chat.title),disable_web_page_preview=True,parse_mode='html')
                pass
        else:
            await message.bot.send_message(message.from_user.id, DEFAULT_ACCEPTTED_TXT.format(message.from_user.first_name,message.chat.title),disable_web_page_preview=True,parse_mode='html')
            unlinked_users(message.from_user.id, message.chat.id, message.chat.title)
            pass
    except Exception as e:
        print(traceback.format_exc())
        print('Channel not in database')
        unlinked_users(message.from_user.id,message.chat.id,message.chat.title)
        pass