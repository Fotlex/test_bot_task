import asyncio
import logging
import sys, os
import django

from functools import partial
from aiohttp import web
from pathlib import Path

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.app.settings')
django.setup()

from bot.middlewares import UserMiddleware

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from shop import config 
from shop.tg_bot.bot.handlers.examinate_sub_handler import examinate
from shop.tg_bot.bot.handlers.catalog_handler import catalog
from shop.tg_bot.bot.handlers.bucked_handler import bucked
from shop.tg_bot.bot.handlers.FAQ_handler import faq
from shop.tg_bot.bot.yookassa import kassa_webhook


dp = Dispatcher()

dp.message.middleware(UserMiddleware())
dp.callback_query.middleware(UserMiddleware())


async def start_webhook(bot: Bot):
    app = web.Application()
    app.router.add_post('/yookassa/webhook', partial(kassa_webhook, bot=bot))
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080) 
    await site.start()
    print("Webhook server started")    


async def main():
    bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await start_webhook(bot=bot)
    dp.include_routers(
        examinate,
        catalog,
        bucked,
        faq,
    )
    
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass