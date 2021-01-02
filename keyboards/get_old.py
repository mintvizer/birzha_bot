from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_old = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Показать старые')
        ],
        [
            KeyboardButton('Добавить тикет'),
            KeyboardButton('Удалить тикет'),
        ],
    ],
    resize_keyboard=True
)