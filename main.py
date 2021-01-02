import asyncio

from aiogram import executor
from asyncpg import Connection

from config import ADMIN_ID
from db import create_db

from loader import bot, db
from parser import parse
import aioschedule as schedule


class DBCommand:
    pool: Connection = db
    GET_VALUES_DB = "SELECT * FROM birzha WHERE status='New';"

    SET_OLD = "UPDATE birzha SET status='Old' WHERE id=$1"
    async def get_new_news(self):
        return await self.pool.fetch(self.GET_VALUES_DB)

    async def set_old(self, id):
        await self.pool.execute(self.SET_OLD, id)

db = DBCommand()

async def on_shutdown(dp):
    await bot.close()

async def send_news_birzha():
    await parse()

    news = await db.get_new_news()
    if news == []:
        return

    for item in news:

        text =f'🟢 ${item[1]}\n' \
              f'<b>Гражданин:</b> {item[2]}\n' \
              f'<b>Должность:</b> {item[3]}\n' \
              f'<b>P:</b> {item[8]}\n' \
              f'<b>Дата:</b> {item[4]}\n' \
              f'<b>Средняя цена:</b> {item[5]}\n' \
              f'<b>Количество:</b> {item[6]}\n' \
              f'<b>Куплено на сумму</b>: {item[7]}\n' \
              f'<b>Осталось акций</b>: {item[9]} млн'

        if item[8] == 'Sale':
            text = f'🔴 ${item[1]}\n' \
                   f'<b>Гражданин:</b> {item[2]}\n' \
                   f'<b>Должность:</b> {item[3]}\n' \
                   f'<b>P:</b> {item[8]}\n' \
                   f'<b>Дата:</b> {item[4]}\n' \
                   f'<b>Средняя цена:</b> {item[5]}\n' \
                   f'<b>Количество:</b> {item[6]}\n' \
                   f'<b>Продано на сумму</b>: {item[7]}\n' \
                   f'<b>Осталось акций</b>: {item[9]} млн'
        await bot.send_message(ADMIN_ID, text)
        await db.set_old(item[0])
        await asyncio.sleep(10)


async def open_shedule():
    schedule.every(2).minutes.do(send_news_birzha)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(10)

async def on_startup(dp):
    # Подождем пока запустится база данных...
    await create_db()
    await asyncio.sleep(20)
    asyncio.create_task(open_shedule())
    await bot.send_message(ADMIN_ID, "Я запущен!")


if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=False)
