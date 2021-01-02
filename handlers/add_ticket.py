from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from asyncpg import Connection

from loader import dp, db
from states import Ticket


class DBCommand:
    pool: Connection = db
    ADD_TICKET = 'INSERT INTO ticket_sale (ticket) VALUES ($1)'

    async def add_ticket(self, ticket):
        await self.pool.execute(self.ADD_TICKET, ticket)

db = DBCommand()

@dp.message_handler(Text(equals='Добавить тикет'))
async def add_ticket(message: Message):
    await Ticket.add.set()
    await message.answer('Отправите название тикета')


@dp.message_handler(state=Ticket.add)
async def adding_ticket(message: Message, state=FSMContext):
    await db.add_ticket(message.text.strip())
    await message.answer('Тикет добавлен!')
    await state.finish()
