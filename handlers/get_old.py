from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from asyncpg import Connection

from config import ADMIN_ID
from loader import dp, db, bot


class DBCommand:
    pool: Connection = db

    GET_OLD_ = "SELECT * FROM birzha WHERE status='Old'"

    async def get_old_news(self):
        return await self.pool.fetch(self.GET_OLD_)


db = DBCommand()
@dp.message_handler(Text(equals='Показать старые'), user_id=ADMIN_ID)
async def get_old_(message: Message):
    text = ''
    olds = await db.get_old_news()
    if olds == []:
        await message.answer('Их нет:(')
    else:
        for item in olds:
            text += f'---------------------------------------' \
                    f'\n\n🟢 ${item[1]}\n' \
                   f'<b>Owner:</b> {item[2]}\n' \
                   f'<b>Relationship:</b> {item[3]}\n' \
                   f'<b>P:</b> покупка\n' \
                   f'<b>Date:</b> {item[4]}\n' \
                   f'<b>Cost:</b> {item[5]}\n' \
                   f'<b>Shares:</b> {item[6]}\n' \
                   f'<b>Value</b>: {item[7]}\n' \
                   f'<b>Shares_total</b>: {item[8]}млн\n\n' \
                    f'---------------------------------------'

        await message.answer(text)