
from aiogram import types
from utils.db_api.db_commands import add_item, get_item_by_name
from aiogram.dispatcher import FSMContext
from data.config import admin_id
from loader import dp, bot
from states.admin_states import NewItem
from utils.db_api.models import Item


@dp.message_handler(user_id=admin_id, commands=["cancel"], state=NewItem)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили создание товара")
    await state.reset_state()


@dp.message_handler(user_id=admin_id, commands=['add_item'])
async def add_item(message: types.Message):
    await message.answer("Введите название товара или нажмите /cancel для отмены")
    await NewItem.Name.set()


@dp.message_handler(user_id=admin_id, state=NewItem.Name)
async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    q_item = await get_item_by_name(name)
    if name in q_item.name:
        await message.answer("Извините, товар с этим названием уже существует в базе\n"
                             "Чтобы отменить нажмите /cancel")
    else:
        item = Item()
        item.name = name
        await message.answer(f"Название товара: <i>{name}</i>\n"
                             "Пришлите фотографию товара (не документ) или нажмите /cancel для отмены")
        await NewItem.Photo.set()
        await state.update_data(item=item)


@dp.message_handler(user_id=admin_id, state=NewItem.Photo, content_types=types.ContentType.PHOTO)
async def add_photo(message: types.Message, state=FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    item: Item = data.get("item")
    item.photo = photo
    await message.answer_photo(photo=photo,
                               caption=f"Название: {item.name}"
                                       "\nВведите цену товара"
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
        await message.answer("Неверное значение, введите число")
        return
    item.price = price

    await message.answer(text=f"Цена: {price:,}\n")
    markup = types.InlineKeyboardMarkup(row_width=2,
                                        inline_keyboard=[[
                                            types.InlineKeyboardButton(
                                                text="Python",
                                                callback_data='py'
                                            ),

                                            types.InlineKeyboardButton(
                                                text="Javascript",
                                                callback_data='js'
                                            )
                                        ]]

                                        )
    await bot.send_message(chat_id=message.chat.id, text="Выберите категорию товара"
                                                         "\nЕсли нету такой категории то напишите мне, я добавлю",
                           reply_markup=markup)
    await state.update_data(item=item)
    await NewItem.CategoryName.set()

    @dp.callback_query_handler(user_id=admin_id, text_contains='change', state=NewItem.Confirm)
    async def change_price(call: types.CallbackQuery):
        await call.message.edit_reply_markup()
        await call.message.answer("Введите заново цену товара в копейках")


@dp.callback_query_handler(user_id=admin_id, text_contains='py', state=NewItem.CategoryName)
async def category_py(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    category_name = 'python'
    data = await state.get_data()
    item: Item = data.get('item')
    item.category_name = category_name

    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Да",
                callback_data='confirm'
            ),

            types.InlineKeyboardButton(
                text="Ввести заново",
                callback_data='change'
            )
        ]]

    )
    await bot.send_message(text="Добавить товар в базу ?", chat_id=call.message.chat.id, reply_markup=markup)
    await NewItem.AddItem.set()


@dp.callback_query_handler(user_id=admin_id, text_contains='confirm', state=NewItem.AddItem)
async def add_to_db(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item: Item = data.get('item')
    await add_item(name=item.name,
                   category_name='Python', category_code="Electronics",
                   price=item.price, photo=item.photo)
    await bot.send_message(chat_id=call.message.chat.id, text=f'Товар {item.name}\n'
                                                              'успешно создан')
    await state.reset_state()
