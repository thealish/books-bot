
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import (Message, InlineKeyboardButton, InlineKeyboardMarkup)
from utils.db_api import database
from loader import dp



@dp.message_handler(CommandStart())
async def register_user(message: Message):
    
    
