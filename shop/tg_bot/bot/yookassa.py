import json
import logging
from pathlib import Path
import sys
import uuid
import time

from aiohttp import web
from aiogram import Bot
from asgiref.sync import sync_to_async
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotificationFactory

from .exel import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

from shop.database.models import User, UserBucked, YookassaInfo
from shop import config

Configuration.account_id = config.YOOKASSA_SHOP_ID
Configuration.secret_key = config.YOOKASSA_SECRET_KEY

async def get_link(user: User, bucked_id: int, bot: Bot, number, adress) -> str:
    bucked = await sync_to_async(
        lambda: UserBucked.objects.select_related('item').get(id=bucked_id)
    )()
    item_price = bucked.item.price
    total_amount = item_price * bucked.count
    
    bot_info = await bot.get_me()
    payment = Payment.create({
        "amount": {
            "value": f"{total_amount}.00",
            "currency": "RUB"
        },
        'metadata': {
            'user_id': user.id
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"{bot_info.url}"
        },
        "capture": True,
        "description": f"Оплата товара через бота @{bot_info.username}"
    }, uuid.uuid4())

    await YookassaInfo.objects.acreate(
        user=user,
        payment_id=payment.id,
        number=number,
        adress=adress,
        bucked_id=bucked_id,
    )

    return payment.confirmation['confirmation_url']


async def kassa_webhook(request: web.Request, bot: Bot):
    try:
        body = await request.text()
        event_dict = json.loads(body)

        notification = WebhookNotificationFactory().create(event_dict)
        payment_id = notification.object.id
        status = notification.object.status

        if status == "succeeded":
            yookassa_info = await sync_to_async(
                lambda: YookassaInfo.objects.select_related('user').get(payment_id=str(payment_id))
            )()
            await bot.send_message(
                chat_id=yookassa_info.user.id,
                text="✅ Ваш платеж успешно завершен! Спасибо за покупку!"
            )
            try:
                bucked = await sync_to_async(
                    lambda: UserBucked.objects.select_related('item').get(id=yookassa_info.bucked_id)
                )()
                
                await sync_to_async(create_excel_if_not_exists)(BASE_DIR)
                
                await sync_to_async(add_payment_to_excel)(
                    BASE_DIR=BASE_DIR,
                    user_id=yookassa_info.user.id,
                    item=bucked.item.name,
                    amount=bucked.item.price * bucked.count,
                    number=yookassa_info.number,
                    adress=yookassa_info.adress,
                )
                
                await sync_to_async(bucked.delete)()
            except Exception as e:
                logging.error(f'Error: {e}', exc_info=True)
        elif status == "canceled":
            pass

        return web.Response(status=200, text="ok")

    except Exception as e:
        print(f"Webhook error: {e}")
        return web.Response(status=500, text="Server error")
