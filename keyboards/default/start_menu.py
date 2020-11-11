from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='меню'),
            KeyboardButton(text='мои покупки'),

        ],
        [
            KeyboardButton(text='Адрес'),
            KeyboardButton(text='Телефонный номер')
        ],
        [
            KeyboardButton(text='Способ платежа')
        ]
    ],
    resize_keyboard=True
)