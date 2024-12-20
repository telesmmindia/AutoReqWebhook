from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='📂 My Channels',callback_data='My Channels')
    keyboard_builder.button(text='➕ Add Channel',callback_data='Add Channel')
    keyboard_builder.button(text='👥 Broadcast Message',callback_data='Broadcast Message')
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


