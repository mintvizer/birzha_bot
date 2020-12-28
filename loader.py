from aiogram import Bot, Dispatcher
import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN_BOT
from db import create_pool

loop = asyncio.get_event_loop()

bot = Bot(
    token=TOKEN_BOT,
    parse_mode='HTML',
    loop=loop
    )

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = loop.run_until_complete(create_pool())