import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import MenuButtonType
from aiogram import F
# from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
import aiohttp



# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot('6937107637:AAFarU8swL-mp7oLC0sMz44A7-F3q0QuD4Y')
# Диспетчер
dp = Dispatcher()
got_user = ""

@dp.message(Command(commands="start"))
async def start(message: types.Message):
    username = message.from_user.username
    
    async with aiohttp.ClientSession() as session:
        async with session.get('https://bookish-happiness-7xvx747jrrwfx65-8000.app.github.dev/user/' + username) as resp:
            got_user = await resp.text()
            got_user_json = json.loads(got_user)
            if(resp.status == 200 and got_user == '[]'):
                kb = [[types.KeyboardButton(text="ПОДЕЛИТЬСЯ КОНТАКТОМ", request_contact=True)]]
                builder = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
                await message.answer("Нажмите на кнопку, чтобы отправить номер телефона", reply_markup=builder)
                @dp.message(F.contact)
                async def got_contact(message: types.Message):
                    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
                        msg = message
                        data = {"name": msg.contact.first_name, "tel": msg.contact.phone_number, "address": "string", "orders": "string", "nickname": msg.from_user.username}
                        print(data)
                        async with session.post('https://bookish-happiness-7xvx747jrrwfx65-8000.app.github.dev/user', json=data) as resp:
                            print(resp.status)
                        await session.close()
                    await message.answer("Введите свое имя:")
                    @dp.message(F.text != "")
                    async def username_requested(message: types.Message):
                        async with aiohttp.ClientSession() as session:
                            async with session.patch('https://bookish-happiness-7xvx747jrrwfx65-8000.app.github.dev/user/' + message.from_user.username, json={"name": message.text}) as resp:
                                kb2 = [[
                                    types.KeyboardButton(text="ОТКРЫТЬ МЕНЮ", web_app=types.WebAppInfo(url="https://fuzzy-invention-r9qx5q45wqp2prwx-5173.app.github.dev/"))
                                ]
                                ]
                                builder2 = types.ReplyKeyboardMarkup(keyboard=kb2, resize_keyboard=True)
                                await message.answer("Регистрация пройдена! Можете заказывать, нажав кнопку МЕНЮ", reply_markup=builder2)
                                await bot.set_chat_menu_button(chat_id=message.chat.id, menu_button=types.MenuButtonWebApp(type=MenuButtonType.WEB_APP, text="Меню", web_app=types.WebAppInfo(url="https://fuzzy-invention-r9qx5q45wqp2prwx-5173.app.github.dev/")))
                            await session.close()

            elif (resp.status == 200 and got_user != '[]'):
                kb2 = [[
                    types.KeyboardButton(text="ОТКРЫТЬ МЕНЮ", web_app=types.WebAppInfo(url="https://fuzzy-invention-r9qx5q45wqp2prwx-5173.app.github.dev/"))
                ],
                ]
                await bot.set_chat_menu_button(chat_id=message.chat.id, menu_button=types.MenuButtonWebApp(type=MenuButtonType.WEB_APP, text="Меню", web_app=types.WebAppInfo(url="https://fuzzy-invention-r9qx5q45wqp2prwx-5173.app.github.dev/")))
                builder2 = types.ReplyKeyboardMarkup(keyboard=kb2, resize_keyboard=True)
                await message.answer("Имя: " + got_user_json[0]["User"]["name"] + "\nТел: " + got_user_json[0]["User"]["tel"], reply_markup=builder2)
        await session.close()

# @dp.message(F.text != "")
# async def error_msg(message: types.Message):
#     message.reply("Осторожно, не сломай меня!")

# Поллинг бота
async def main():
    await dp.start_polling(bot)
# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())