from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_n_cancel() :
    return ReplyKeyboardBuilder().button(text='Cancel').as_markup()