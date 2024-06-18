import asyncio
import logging
from aiogram.methods import DeleteWebhook
from aiogram import types, F
from aiogram.filters import Command
import bd
from create_bot import dp, bot


logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher):
    print('Бот вышел в он-лайн')
    await bd.start()
    print('База данных активна!')

async def on_shutdown(dispatcher):
    await bd.finish()
    print('База данных отключена!')

@dp.message(Command("start","help"))
async def start(message: types.Message):
    kb = [[types.KeyboardButton(text="Инструкция"),
           types.KeyboardButton(text="Список компонентов")
           ]
          ]
    markup = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите действие")
    await message.answer(f'Приветстсвую вас, {message.from_user.first_name}!',reply_markup=markup)

@dp.message(F.text=="Инструкция")
@dp.message(Command("instr"))
async def instr(message: types.Message):
    print(Command("instr"))
#    if :
        #file = open('.\Список компонентов.xlsx','rb')
        #await bot.send_document(message.chat.id, file)
    await bd.ins(message)

@dp.message(F.text=="Список компонентов")
@dp.message(Command("comp"))
async def comp(message: types.Message):
    print(Command("comp"))
#    if :
        #file = open('.\Список компонентов.xlsx','rb')
        #await bot.send_document(message.chat.id, file)
    await bot.send_message(message.chat.id, str(message.from_user.id))
    await bot.send_message(message.chat.id, message.from_user.first_name)

@dp.message(Command("list"))
async def list(message: types.Message):
    await bd.list(message)

@dp.callback_query()
async def callback(call):
    await call.message.answer(call.data)

# Запуск процесса поллинга новых апдейтов

async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())