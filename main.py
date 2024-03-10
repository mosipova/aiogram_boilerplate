import logging
from logging.handlers import TimedRotatingFileHandler
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from config import TELEGRAM_BOT_TOKEN
from handlers.handler import router as main_router
from middlewares.analyticsmiddleware import AnalyticsMiddleware
from middlewares.throttling import ThrottlingMiddleware
from utils.database import get_db_connection


async def on_startup() -> None:
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.handlers.TimedRotatingFileHandler("bot_log.log", when="midnight", backupCount=7),
            logging.StreamHandler()
        ],
        format="%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(message)s",
    )


async def on_shutdown(dispatcher: Dispatcher) -> None:
    await dispatcher.storage.close()


async def main():
    con = await get_db_connection()
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
        dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)

        dp.message.middleware.register(ThrottlingMiddleware())
        dp.message.middleware.register(AnalyticsMiddleware(conn=con))

        dp.include_router(main_router)

        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

        await dp.start_polling(bot, skip_updates=True)
    finally:
        await con.close()


if __name__ == '__main__':
    asyncio.run(main())
