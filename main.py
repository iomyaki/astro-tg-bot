import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
import script
from app import database as db
from router import r


logging.basicConfig(
    format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d [%(filename)s])", datefmt="%d/%m/%Y %I:%M:%S %p",
    level=logging.INFO,
    filename="bot_logs.log",
    filemode="w",
)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(r)


async def on_startup() -> None:
    await db.db_start()
    logging.info("Database started")


async def on_shutdown() -> None:
    await bot.session.close()
    await script.bot.session.close()
    logging.info("Bot session closed")


async def main() -> None:
    scheduler = AsyncIOScheduler(timezone=config.TIMEZONE)
    scheduler.add_job(db.reset_sent_today, "cron", hour="0")
    scheduler.add_job(script.daily_horoscope, "cron", hour="10")
    scheduler.start()

    dp.startup.register(on_startup)
    await script.set_bot_commands()
    await dp.start_polling(bot, skip_updates=False, on_shutdown=on_shutdown)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.info("Bot launched")
    asyncio.run(main())
    logging.info("Bot shut down")
