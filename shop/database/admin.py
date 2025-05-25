from pathlib import Path
import sys
from django.contrib import admin

from .models import *


BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from shop.config import BOT_TOKEN


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Item)
admin.site.register(UserBucked)
admin.site.register(MessageStatus)
admin.site.register(YookassaInfo)
admin.site.register(FAQ)


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.send:
            from threading import Thread
            Thread(target=self.send_broadcast, args=(obj.id,)).start()

    def send_broadcast(self, broadcast_id):
        import os
        import django
        
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.app.settings')
        django.setup()
        
        from shop.database.models import Broadcast, User
        from aiogram import Bot
        import asyncio

        broadcast = Broadcast.objects.get(id=broadcast_id)
        user_ids = list(User.objects.values_list('id', flat=True))
        
        async def async_send():
            bot = Bot(token=BOT_TOKEN)
            success = 0
            failed = 0
            
            for user_id in user_ids:
                try:
                    await bot.send_message(
                        chat_id=user_id,
                        text=broadcast.message
                    )
                    success += 1
                except Exception as e:
                    print(f"Failed to send to {user_id}: {str(e)}")
                    failed += 1
                await asyncio.sleep(0.1)  
            
            from asgiref.sync import sync_to_async
            
            @sync_to_async
            def update_broadcast():
                Broadcast.objects.filter(id=broadcast_id).update(
                    send=True,
                )
            
            await update_broadcast()
            await bot.session.close()
        
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(async_send())
        finally:
            loop.close()