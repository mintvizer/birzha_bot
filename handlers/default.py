from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from loader import dp, bot


@dp.message_handler()
async def echo(message: Message):
    await message.answer(message.text)

