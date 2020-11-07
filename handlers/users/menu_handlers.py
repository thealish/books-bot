from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from keyboards.inline.menu_keyborards import categories_keyboard
from loader import dp

@dp.message_handler(Command("menu"))
async def show_menu(message:types.Message):
    await list_categories(message)

async def list_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await categories_keyboard()

    if isinstance(message, types.Message):
        await message.answer("Cмотри что у нас есть",reply_markup=markup)

    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)

async def list_subcategories(callback: types.CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)
    await callback.message.edit_reply_markup(markup)

async def list_items(callback: types.CallbackQuery, categories, subcategories, **kwargs):
    await items_keyboard(category=category, subcategory=subcategory)
    await callback.message.edit_text("Смотри что у нас есть", reply_markup=markup)

async def show_item(callback: types.CallbackQuery, category, subcategory, item_id):
    markup = item_keyboard(category,subcategory, item_id)

    item = await get_item(item_id)
    text = f"Купи {item.name}"
    await callback.message.edit_text(text, reply_markup=markup)



@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data:dict):
    current_level = callback_data.get('level')
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    item_id = callback_data.get('item_id')

    levels = {
        "0": list_categories,
        "1": list_subcategories,
        "2": list_items,
        "3": show_item
    }
    current_level_function = veles[current_level]

    await current_level_function(call,category=category, subcategory, item_id)
    
    
    
