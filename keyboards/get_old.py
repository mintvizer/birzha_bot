from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_old = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Показать старые')
        ]
    ],
    resize_keyboard=True
)