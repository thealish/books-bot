from asyncio import sleep

from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import admins
from loader import dp, bot
from states import NewItem, Mailing
from database import Item, User

@dp.message_handler(user_id=admin_id, commands=['cancel'], state=NewItem)
async def cancel(message: types.Message, state=FSMContext):
    await message.answer("Вы отменили создание товара")
    await state.reset_state()


@dp.message_handler(user_id=admin_id, commands=['add_item'])
async def add_item(message: types.Message):
	await message.answer("Введите название товара или нажмите /cancel")
	await NewItem.Name.set()



@dp.message_handler(user_id=admin_id, state=NewItem.Name)
async def enter_name(message: types.Message, state:FSMContext):
	name = message.text
	item = Item()
	item.name = name
	await message.answer("Название {name}"
							"\nПришлите мне фотографию товара (не документ) или намите /cancel").format(name=name)
	await NewItem.Photo.set()
	await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewItem.Photo, content_types= types.ContentType.PHOTO)
async def add_photo(message: types.Message, state= FSMContext):
	photo = message.photo[-1].file_id
	data = await state.get_data()
	item: Item = data.get("item")
	item.photo = photo
	await message.answer_photo(
		photo=photo,
		caption=("Название: {name}"
			"\nПришлите мне цену товара в копейках или нажмите /cancel").format(name=item.name)

	await NewItem.Price.set()
	await state.update_data(item=item)

@dp.message_handler(user_id=admin_id, state=NewItem.Price)
async def enter_price(message: types.Message, state= FSMContext):
	data = await state.get_data()
	item: Item = data.get('item')
	try:
		price = int(message.text)
	except ValueError:
		await message.answer("Неверное значение, введите число")
		return
	item.price = price

	markup = types.InlineKeyboardMarkup(
			inline_keyboard = [[
				types.InlineKeyboardButton(
						text = ("Да"),
						callback_data='confirm'
				),


				types.InlineKeyboardButton(
						text = _("Ввести заново"),
						callback_data='change'
				)
			]],

		)
	await message.answer("Цена: {price:,}\n"
							"Потверждаете? Нажмите /cancel чтобы отменить").format(price=price),reply_markup=markup
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


@dp.message_handler(user_id=admin_id, commands=['tell_everyone'])
async def mailing(message: types.Message):
	await message.answer("Пришлите текст рассылки")
	await Mailing.Text.set()


@dp.message_handler(user_id=admin_id, state=Mailing.Text)
async def enter_text(message: types.Message, state: FSMContext):
	text = message.text
	await state.update_data(text=text)
	markup = types.InlineKeyboardMarkup(
			inline_keyboard = [
				types.InlineKeyboardButton(
						text = "Русский",
						callback_data='ru'
				),


				types.InlineKeyboardButton(
						text = "Узбекций",
						callback_data='uz'
				)
			],

		)

	await message.answer("Пользователям на каком языке разослать это сообщение?\n\n"
							"Текст:\n"
							"{text}").format(text=text),
							reply_markup=markup
