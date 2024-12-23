import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')


from openai import OpenAI
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

import message_router


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    await bot.delete_webhook(drop_pending_updates=True)

    client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")
    client2 = OpenAI(base_url="http://localhost:8003/v1", api_key="not-needed")
    dp = Dispatcher(client=client, client2=client2)
    dp.include_routers(message_router.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    if BOT_TOKEN is None:
        raise ValueError("BOT_TOKEN is not set")

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())