from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_n_cancel() :
    return ReplyKeyboardBuilder().button(text='❌ Cancel').as_markup()

def back_button():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='⬅️ Back')
    return keyboard_builder.as_markup(resize_keyboard=True)