from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_buttons():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='🤝 Request Accept Features',callback_data='request')
    keyboard_builder.button(text='Add Buttons To Your Posts 🔼',callback_data='post-land')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='➕ Add Channel',callback_data='Add Channel')
    keyboard_builder.button(text='📂 My Channels',callback_data='My Channels')
    keyboard_builder.button(text='👥 Broadcast Message',callback_data='Broadcast Message')
    keyboard_builder.button(text='⬅️ Back', callback_data='back-2_main')
    keyboard_builder.adjust(2,1)
    return keyboard_builder.as_markup()

def defaultn() :
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Default: Hi {username}\nWelcome to {channel_name}.Your Request has been accepted by {}',callback_data='default')
    keyboard_builder.button(text='Enter Custom Greeting Message',callback_data='custom')
    return keyboard_builder.as_markup()

def get_cancel() :
    return InlineKeyboardBuilder().button(text='❌ Cancel',callback_data='cancel').as_markup()

def yesno() :
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='✅ Yes',callback_data='Yes')
    keyboard_builder.button(text = '❌ No',callback_data='No')
    return keyboard_builder.as_markup()

def edit_btns():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='🔁Change Post', callback_data='change')
    keyboard_builder.button(text='⬅️ Back', callback_data='cancel')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

def channels_btns():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='👋 Show Greet Messsage',callback_data='message')
    keyboard_builder.button(text='📩 Send Message', callback_data='promo')
    keyboard_builder.button(text='🚫 Remove Channel', callback_data='remove')
    keyboard_builder.button(text='⬅️ Back', callback_data='back')
    keyboard_builder.adjust(2,1)
    return keyboard_builder.as_markup()

def channels_new(data):
    keyboard_builder = InlineKeyboardBuilder()
    for i in data:
        keyboard_builder.button(text=f"{i['channel_name']}", callback_data=f"{i['channel_id']}")

    keyboard_builder.button(text='⬅️ Back', callback_data='back')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

def my_users_btn() :
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='👥 Broadcast To All Users',callback_data='all_user'),
    keyboard_builder.button(text='📢 Broadcast Channel Wise',callback_data='channel_wise')
    keyboard_builder.button(text='⬅️ Back',callback_data='cancel')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

PROMO_BTN = [InlineKeyboardButton(text='Make your own bot ❤️', url='https://t.me/Channel_Guru_Bot'),]

def edit_msg(data='',buttons=0,add_to_row=0,add_to_column=0,is_it_the_very_first_with_reply_markup=False): #bitch ass nigga function
    add_to_row = int(add_to_row)
    add_to_column = int(add_to_column)
    if is_it_the_very_first_with_reply_markup:
        for index, row in enumerate(buttons):
            row.append(InlineKeyboardButton(text='➕',callback_data=f'{index}-{len(row)}'))

        buttons.append([InlineKeyboardButton(text='➕',callback_data=f'{len(buttons)}-0')])
        buttons.append([InlineKeyboardButton(text='Get Post', callback_data='post')])
    else:
        if len(buttons)==0:
            buttons = []
        if len(data) ==0:
            buttons.append([InlineKeyboardButton(text='➕',callback_data='0-0')])
        else:
            buttons[add_to_row].pop(add_to_column)
            for i in data:
                for j in i:
                    if '@' in i[j]:
                        buttons[add_to_row].append(InlineKeyboardButton(text=f'{j}', url=f'https://t.me/{i[j][1:]}'))
                    else:
                        buttons[add_to_row].append(InlineKeyboardButton(text=f'{j}', url=f'{i[j]}'))
                    buttons[add_to_row].append(InlineKeyboardButton(text='➕', callback_data=f'{add_to_row}-{len(buttons[add_to_row])}'))

            if len(buttons)<=1:
                buttons.append([InlineKeyboardButton(text='➕',callback_data=f'{len(buttons)}-0')])
                buttons.append([InlineKeyboardButton(text='Get Post',callback_data='post')])
            else:
                if buttons[-2][0].text != "➕":
                    buttons.insert(-1,[InlineKeyboardButton(text='➕',callback_data=f'{len(buttons)-1}-0')])
                if not any(
                button[0].text == "Get Post" and button[0].callback_data == 'post'
                for button in buttons):
                    buttons.append([InlineKeyboardButton(text='Get Post',callback_data=f'post')])
    return buttons

def inline_back_button():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='⬅️ Back',callback_data='back')
    return keyboard_builder.as_markup()

def share_save(query) :
    return InlineKeyboardBuilder().button(text='Share via inline',switch_inline_query=query).as_markup()