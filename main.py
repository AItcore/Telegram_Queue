import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import KeyboardButton


TOKEN = '1255745151:AAGkabC6ChlteBK1wgzl9hSjf96A60aiRzY'

Queue = []
comm = sqlite3.connect('Users.db')
cursor = comm.cursor()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def create_db():
    cursor.execute("""CREATE TABLE IF NOT EXISTS  users(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_USER NVARCHAR(20),
        Name NVARCHAR(50)
        )""")
    comm.commit()


@dp.message_handler(commands = "add")
async def Add_user(message):
    name = ""
    try:
        name = message.from_user.first_name + " " + message.from_user.last_name
    except:
        name = message.from_user.first_name
    if (str(message.from_user.id), name) not in cursor.execute("SELECT ID_USER, Name FROM users").fetchall():
        cursor.execute(f"INSERT INTO users(ID_USER, Name) VALUES ({message.from_user.id}, '{name}')")
        comm.commit()
        await message.answer("Вы были добавлены")
    else:
        await message.answer("Вы уже были добавлены")
        
@dp.message_handler(commands = "enter")
async def Enter(message):
    name = ""
    try:
        name = message.from_user.first_name + " " + message.from_user.last_name
    except:
        name = message.from_user.first_name
    if (str(message.from_user.id), name) in cursor.execute("SELECT ID_USER, Name FROM users").fetchall() and name not in Queue:
        Queue.append(name)
        await message.answer("Вы были добавлены в очередь")
    else:
        await message.answer("Вы уже были добавлены в очередь или не зарегистрировались")
        
@dp.message_handler(commands = "exit")
async def Exit(message):
    name = ""
    try:
        name = message.from_user.first_name + " " + message.from_user.last_name
    except:
        name = message.from_user.first_name
    if (str(message.from_user.id), name)in cursor.execute("SELECT ID_USER, Name FROM users").fetchall() and name in Queue:
        Queue.remove(name)
        await message.answer("Вы были удалены из очередь")
    else:
        await message.answer("Вы уже были удалены из очередь или не зарегистрировались")
          
                
@dp.message_handler(commands = "list")
async def List(message):
    Names = ""
    if len(Queue) == 0:
        Names = "Никого нету в очереди"
    for i in Queue:
        Names += i + "\n"
    await message.answer(Names)

if __name__ == "__main__":
    create_db()
    executor.start_polling(dp)