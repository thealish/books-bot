from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from data.config import admin_id
from loader import dp, bot
from states.admin_states import NewItem
from utils.db_api.models import Item
from keyboards.default.categories import menu


@dp.message_handler(user_id=admin_id, commands="cancel", state=NewItem)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили создание заказа")
    await state.reset_state()


@dp.message_handler(user_id=admin_id, commands="add_item")
async def add_item(message: types.Message):
    await message.answer("Введите название товара или нажмите /cancel")
    await NewItem.Name.set()


@dp.message_handler(user_id=admin_id, state=NewItem.Name)
async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    item = Item()
    item.name = name

    await message.answer(f"Название: {name}"
                         f"\nПришлите мне цену товара или нажмите /cancel")
    await NewItem.Price.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewItem.Price)
async def enter_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item: Item = data.get("item")

    try:
        price = int(message.text)
    except ValueError:
        await message.answer("Неверное значение введите число")
        return
    item.price = price
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="Да", callback_data="confirm")],
            [InlineKeyboardButton(text="Ввести заново", callback_data="change")],
        ]
    )
    sent_message = await bot.send_message(reply_markup=markup, chat_id=message.chat.id, text=f"Цена: {price}\n"
                                                                                             "Потверждаете? Нажмите /cancel чтобы отменить")
    item.sent_message = sent_message
    await state.update_data(item=item)
    await NewItem.Confirm.set()


@dp.callback_query_handler(user_id=admin_id, text_contains="change", state=NewItem.Confirm)
async def change_price(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Введите цену заново")
    await NewItem.Price.set()


@dp.callback_query_handler(user_id=admin_id, text_contains='confirm', state=NewItem.Confirm)
async def confirm_price(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item: Item = data.get('item')
    await bot.delete_message(message_id=item.sent_message.message_id, chat_id=call.message.chat.id)
    await call.message.answer('Отправьте фотографию товара (не документ) или нажмите /cancel')
    await state.update_data(item=item)
    await NewItem.Photo.set()


@dp.message_handler(user_id=admin_id, state=NewItem.Photo, content_types=types.ContentType.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    item: Item = data.get('item')
    item.photo = photo

    await message.answer_photo(photo=photo,
                               caption=f"Название {item.name}\n"
                                       f"Теперь отправьте описание для товара")
    await state.update_data(data=data)
    await NewItem.Description.set()


@dp.message_handler(user_id=admin_id, state=NewItem.Description)
async def get_description(message: types.Message, state: FSMContext):
    description = message.text
    data = await state.get_data()
    item: Item = data.get('item')
    item.description = description
    await message.answer("Теперь выберите категорию товара", reply_markup=menu)

    await state.update_data(item=item)
    await NewItem.CategoryName.set()


@dp.message_handler(Text(equals=['Python', 'Java', 'JavaJcript', 'Kotlin', 'Golang', 'Linux', 'C#', 'Flutter']),
                    user_id=admin_id, state=NewItem.CategoryName)
async def add_category(message: types.Message, state: FSMContext):
    category_name = message.text
    await message.answer(f'Вы выбрали категорию <i>{category_name}</i>', reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    item: Item = data.get('item')
    item.category_name = category_name
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да', callback_data='dbConfirm'),
                InlineKeyboardButton(text='Нет', callback_data='dbCancel'),
            ]
        ]
    )
    await message.answer_photo(photo=item.photo,
                               caption=f"Название: <b>{item.name}</b>\n"
                                       f"Цена: <b>{item.price}</b>\n"
                                       f"Описание: <i>{item.description}</i>\n"
                                       f"Категория: {category_name}\n"
                                       f"Добавить в базу"
                               , reply_markup=markup)
    await NewItem.DBConfirm.set()


@dp.callback_query_handler(user_id=admin_id, text_contains='dbConfirm', state=NewItem.DBConfirm)
async def add_to_database(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item: Item = data.get("item")
    await item.create()
    await call.message.answer('Товар удачно создан\n'
                              '<i>Чтобы добавить ещё товар нажмите</i> /add_item')

    await state.reset_state()


@dp.callback_query_handler(user_id=admin_id, text_contains="dbCancel", state=NewItem.Confirm)
async def change_price(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Создание товара отменено")
    await NewItem.Price.set()
