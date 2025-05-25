import sys

from pathlib import Path

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram import Router, F, Bot

from ..yookassa import get_link
from ..keyboards import *
from ..text import *
from ..states import DeliveryData

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

from shop.database.models import User, Item, UserBucked, MessageStatus

bucked = Router()

@bucked.callback_query(F.data == 'bucked')
async def buccked_open(callback: CallbackQuery, user: User):
    try:
        bucked_items = await sync_to_async(
            lambda: list(
                UserBucked.objects.filter(user=user)
                .select_related('item') 
            )
        )()
        
        if not bucked_items:
            await callback.answer(EMPTY_BUCKED_TEXT)
            return
        
        await callback.answer('')
        
        for i, bucked_item in enumerate(bucked_items):
            price = bucked_item.item.price * bucked_item.count

            await callback.message.answer(
                text=f'{i + 1}. Товар: {bucked_item.item.name}, '
                     f'количество: {bucked_item.count}, '
                     f'общая цена: {price}',
                reply_markup=bucked_keyboard(bucked_item.id)
            )
        
            
    except Exception as e:
        print(f"Error in buccked_open: {e}")
        await callback.answer("Произошла ошибка при обработке корзины", show_alert=True)
        
        
@bucked.callback_query(F.data.startswith('deleteitemfrombucked_'))
async def get_user_data(callback: CallbackQuery):
    bucked_id = callback.data.split('_')[1]
    
    await sync_to_async(UserBucked.objects.filter(id=int(bucked_id)).delete)()
    await callback.answer('Товар удален')
    await callback.message.delete()
    
    
@bucked.callback_query(F.data.startswith('submititembuy_'))
async def submit_buy(callback: CallbackQuery, state: FSMContext):
    await state.update_data(bucked_id = callback.data.split('_')[1])
    await state.set_state(DeliveryData.phone)
    
    await callback.answer('')
    await callback.message.answer(text=NUMBER_TEXT)
    
    
@bucked.message(DeliveryData.phone)
async def phone_number(message: Message, state: FSMContext):
    await state.update_data(phone = message.text)
    await state.set_state(DeliveryData.adress)
    
    await message.answer(ADRESS_TEXT)
    
    
@bucked.message(DeliveryData.adress)
async def phone_number(message: Message, state: FSMContext):
    await state.update_data(adress = message.text)
    data = await state.get_data()  
    bucked_id = data.get("bucked_id")
    try:
        await message.answer(
            text=f'Ваш номер: {data.get("phone")}\nВаш адресс: {data.get("adress")}',
            reply_markup=await go_pay()
        )
    except Exception as e:
        print(e)
    
    
@bucked.callback_query(F.data == 'change_delivery_data')
async def change_data(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DeliveryData.phone)
    
    await callback.answer('')
    await callback.message.answer(text=NUMBER_TEXT)
    
    
@bucked.callback_query(F.data == 'get_pay_link')
async def get_pay_link(callback: CallbackQuery, state: FSMContext, user: User, bot: Bot):
    await callback.answer('')
    data = await state.get_data()  
    bucked_id = data.get("bucked_id")
    payment_url = await get_link(
        user=user,
        bucked_id=bucked_id,
        bot=bot,
        number=data.get("phone"),
        adress=data.get("adress")
    )
                                    
    await callback.message.edit_text(
        text=f'<a href="{payment_url}">Жми здесь чтобы оплатить!</a>',
        reply_markup=None
    )
    
    await state.clear()
    await callback.message.answer(
            f'{MENU_TEXT} {user.first_name}',
            reply_markup=menu_keyboard()
        )

    
    
    
    
    

    
    
    
    