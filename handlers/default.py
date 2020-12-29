from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from config import ADMIN_ID
from keyboards import get_old
from loader import dp, bot


@dp.message_handler()
async def echo(message: Message):
    if message.chat.id == ADMIN_ID:
        await message.answer('Класс', reply_markup=get_old)
    await message.answer(message.text)

