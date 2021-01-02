from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from asyncpg import Connection

from loader import dp, db
class DBCommand:
    pool: Connection = db
    GET_SALE_TICKET = 'SELECT * FROM ticket_sale;'
    DEL_TICKET = 'DELETE FROM ticket_sale WHERE id=$1'

    async def get_sale_ticket(self):
        return await self.pool.fetch(self.GET_SALE_TICKET)

    async def delete_ticket(self, id):
        await self.pool.execute(self.DEL_TICKET, id)


db = DBCommand()
cd = CallbackData('del', 'filter', 'id')


@dp.message_handler(Text(equals='Удалить тикет'))
async def get_tickets(message: Message):
    tickets = await db.get_sale_ticket()
    if tickets == []:
        await message.answer('У вас пока нет тикетов на отслеживание sell')
    for ticket in tickets:
        markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Удалить', callback_data=cd.new(filter='delete', id=ticket[0]))]])
        await message.answer(ticket[1], reply_markup=markup)


@dp.callback_query_handler(cd.filter(filter='delete'))
async def delete_ticket(call: CallbackQuery, callback_data=dict):
    id = int(callback_data.get('id'))
    await db.delete_ticket(id)


    await call.answer(text='Тикет удален', cache_time=.5)
    await call.message.edit_reply_markup()
