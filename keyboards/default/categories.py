from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Python'),
            KeyboardButton(text='JavaScript'),
        ],
        [
            KeyboardButton(text='Java'),
            KeyboardButton(text='Golang'),
        ],
        [
            KeyboardButton(text='Linux'),
            KeyboardButton(text='C#'),
        ],
        [
            KeyboardButton(text='Kotlin'),
            KeyboardButton(text='Flutter'),
        ],

    ], resize_keyboard=True
)