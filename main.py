import asyncio
import logging
import sys
from pathlib import Path

# Убеждаемся, что корневая директория в пути для импорта
root_dir = Path(__file__).parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.handlers import router
from bot.database import init_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден! Проверьте .env файл.")
        return
    
    bot = None
    try:
        await init_db()
        logger.info("База данных инициализирована")

        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        dp.include_router(router)

        logger.info("Бот запущен и ждёт сообщений...")
        await dp.start_polling(bot)
    
    except Exception as e:
        logger.exception(f"Критическая ошибка при запуске бота: {e}")
    finally:
        if bot:
            await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
