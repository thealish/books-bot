from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

req_phone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Номер телефона',request_contact=True)

        ]
    ],
    resize_keyboard=True,one_time_keyboard=True
)

req_location = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Адрес доставки', request_location=True)
        ]
    ]
)