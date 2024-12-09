import logging
import asyncio
import os
import sys

from aiogram import Bot
from dotenv import load_dotenv

import parsers.variety as variety
import parsers.indiewire as indiewire


load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")




bot = Bot(token=BOT_TOKEN)


async def main() -> None:
   await variety.fetch_articles(bot)
   await indiewire.fetch_articles(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())





