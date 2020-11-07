from asyncio import sleep

from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import admin_id
from loader import dp, bot
from states.admin_states import NewItem, Mailing
from utils.db_api.models import Item, User


@dp.message_handler(user_id=admin_id, commands=["cancel"], state=NewItem)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer(_("Вы отменили создание товара"))
    await state.reset_state()


@dp.message_handler(user_id=admin_id, commands=["add_item"])
async def add_item(message: types.Message):
    await message.answer("Введите название товара или нажмите /cancel")
    await NewItem.Name.set()

