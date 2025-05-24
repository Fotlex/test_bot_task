import asyncio
import sys, os
import django

from pathlib import Path

from aiogram import Bot, Dispatcher

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.app.settings')
django.setup()

from bot.middlewares import UserMiddleware

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from shop import config 
from shop.tg_bot.bot.handlers.examinate_sub_handler import examinate
from shop.tg_bot.bot.handlers.catalog_handler import catalog


dp = Dispatcher()

dp.message.middleware(UserMiddleware())
dp.callback_query.middleware(UserMiddleware())

async def main():
    bot = Bot(config.BOT_TOKEN)
    
    dp.include_routers(
        examinate,
        catalog,
    )
    
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass