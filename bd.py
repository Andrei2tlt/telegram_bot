import sqlite3 as sq
from aiogram import types
from create_bot import bot
import datetime as dttm

conn = sq.connect('tg.db')
cur = conn.cursor()
async def start():
    cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
    conn.commit()

async def finish():
    cur.close()
    conn.close()
async def ins(message: types.Message):
    u = message.from_user
    cur.execute("""
    insert into users (id, name, last_date, cnt) 
    select {id}, '{name}', datetime('now','localtime'), 1
    ON CONFLICT(id) DO UPDATE 
    SET cnt = ifnull(cnt,0)+1,
        last_date = datetime('now','localtime')
    """.format(id = u.id, name = u.first_name))
    conn.commit()
    print('Запись добавлена')

async def list(message: types.Message):
        cur.execute('select * from users')
        users = cur.fetchall()

        info = ''
        for r in users:
            info += f'{r[0]} {r[1]}\n'

        await bot.send_message(message.chat.id, info)
