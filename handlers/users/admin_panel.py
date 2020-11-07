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

@dp.message_handler(user_id=admin_id, state=NewItem.Name)
async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    item = Item()
    item.name = name
    await message.answer(f"Название {name}Пришлите мне фотографию товара (не документ) или нажмите /cancel")
                            
    await NewItem.Photo.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewItem.Photo, content_types=types.ContentType.PHOTO)
async def add_photo(message: types.Message, state=FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    item: Item = data.get("item")
    item.photo = photo
    await message.answer_photo(
        photo=photo,
        caption=(f"Название: {item.name}"
                "\nПришлите мне цену товара или нажмите /cancel")
    )
    await NewItem.Price.set()
    await state.update_data(item=item)

@dp.message_handler(user_id=admin_id, state=NewItem.Price)
async def enter_price(message: types.Message, state=FSMContext):
    data = await state.get_data()
    item: Item = data.get('item')
    try:
        price = int(message.text)
    except ValueError:
        await message.answer('Неверное значение, введите число')
        return
    item.price = price
    markup = types.InlineKeyboardMarkup(
			inline_keyboard = [[
				types.InlineKeyboardButton(
						text = "Да",
						callback_data='confirm'
				),


				types.InlineKeyboardButton(
						text = "Ввести заново",
						callback_data='change'
				)
			]],

		)
    await message.answer(text=f"Цена: {price}Потверждаете? Нажмите /cancel чтобы отменить", reply_markup=markup)
                        
    await state.update_data(item=item)
    await NewItem.Confirm.set()


@dp.callback_query_handler(user_id=admin_id, text_contains='change', state=NewItem.Confirm)
async def change_price(call: types.CallbackQuery):
	await call.message.edit_reply_markup()
	await call.message.answer("Введите заново цену товара в копейках")


@dp.callback_query_handler(user_id=admin_id, text_contains="confirm", state=NewItem.Confirm)
async def confirm(call: types.CallbackQuery, state:FSMContext):
	await call.message.edit_reply_markup()
	data = await state.get_data()
	item: Item = data.get("item")
	await item.create()
	await call.message.answer("Товар удачно создан")
	await state.reset_state()