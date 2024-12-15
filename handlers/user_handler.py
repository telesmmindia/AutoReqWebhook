from aiogram import Router, F
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.texts import CHOOSE
from keyboards.InlineKeyboard import get_keyboard
from models.database import bot_fetcher


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        bot_token = message.bot.token
        bot_details = bot_fetcher(bot_token)
        return message.text == '/start' and message.from_user.id == bot_details['user_id'] and bot_details['bot_status'] ==1

router = Router(name="user_router")

@router.message(AdminFilter())
async def start_handler(message:Message,state:FSMContext):
    await message.answer(CHOOSE,reply_markup=get_keyboard())





