from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api.db_commands import get_categories

menu_cd = CallbackData("category", 'item_id')


def make_callback_data(category='0', item_id='0'):
    return menu_cd.new(category=category, item_id=item_id)


async def categories_keyboard():
    markup = InlineKeyboardMarkup()
    categories = await get_categories()
    for category in categories:
        button_text = f"{category.category_name}"
        callback_data = make_callback_data(category=category.category_code)

        markup.insert(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    return markup
