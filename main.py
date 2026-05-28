import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from database import init_db
from handlers import setup_routers


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


async def main():
    logger.info("🚀 Bot ishga tushmoqda...")

    await init_db()
    logger.info("✅ Database tayyor")

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=MemoryStorage())

    # ROUTERS FIX
    dp.include_router(setup_routers())

    await bot.delete_webhook(drop_pending_updates=True)

    me = await bot.get_me()
    logger.info(f"✅ Bot @{me.username} ishga tushdi!")

    try:
        # STREAMLIT SAFE MODE
        await dp.start_polling(bot, handle_signals=False)

    except Exception as e:
        logger.exception(f"Bot error: {e}")

    finally:
        await bot.session.close()


# 🔥 STREAMLIT SAFE RUNNER
def run_bot():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(main())


if __name__ == "__main__":
    run_bot()
