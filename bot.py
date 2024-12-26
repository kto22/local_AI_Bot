import asyncio      # тут импортируем встроенные библиотеки
import logging
import sys
import os
from dotenv import load_dotenv

load_dotenv()       #тут получаем токен для бота из файлика .env
BOT_TOKEN = os.getenv('BOT_TOKEN')


from openai import OpenAI       # тут импортируем апи для взаимодействия с нейронкой и библиотеку для бота
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

import message_router       # здесь импортим файлик message_router.py


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    await bot.delete_webhook(drop_pending_updates=True)

    client = OpenAI(base_url="http://docker.internal.host:8000/v1", api_key="not-needed")       # тут подключаемся к локальному llama-cpp серверу и нейронке
    client2 = OpenAI(base_url="http://docker.internal.host:8003/v1", api_key="not-needed")
    dp = Dispatcher(client=client, client2=client2)        # передаём клиенты в диспетчер бота
    dp.include_routers(message_router.router)

    await dp.start_polling(bot)


if __name__ == "__main__":  # точка входа (точка запуска приложения, требуемая библиотекой aiogram)
    if BOT_TOKEN is None:       # проверка токена
        raise ValueError("BOT_TOKEN is not set")

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main()) # запуск функции main через asyncio