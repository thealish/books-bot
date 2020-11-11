from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import (Message)
from utils.db_api.db_commands import add_new_user
from loader import dp
from loader import bot
from asyncpg.exceptions import UniqueViolationError


@dp.message_handler(CommandStart())
async def register_user(message: Message):
    try:
        await add_new_user(user_id=message.from_user.id, full_name=message.chat.full_name,
                           username=message.chat.username)
        await message.answer("Приветствую вас в нашем боте!\n"
                             "Чтобы купить книгу нажмите /menu \n"
                             "Чтобы посмотреть историю покупок /purchases ")
        await bot.send_message(chat_id=message.chat.id,
                               text=f"{message.chat.first_name}: Вы уже зарегистрированы")
    except UniqueViolationError:
        await bot.send_message(chat_id=message.chat.id, text="<i>Вы уже регистрировались</i> \n"
                                                             "<b>Чтобы купить книгу нажмите</b> /menu\n"
                                                             "<b>Чтобы посмотреть историю покупок</b> /purchases\n"
                                                             "<b>Если хотите оставить отзыв нажмите</b> /review")
