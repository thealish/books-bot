
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import (Message, InlineKeyboardButton, InlineKeyboardMarkup)
from utils.db_api import database
from loader import dp
from loader import bot



@dp.message_handler(CommandStart())
async def register_user(message: Message):
    await message.answer(f"Hi {message.chat.first_name}")


