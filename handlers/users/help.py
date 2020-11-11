from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from data.config import admin_id

from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку',
        '/menu - Посмотреть категории товаров',
        '/purchases - Мои покупки',
        '/review - Оставить свой отзыв'
    ]
    await message.answer('\n'.join(text))
