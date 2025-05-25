from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from ..text import *
from ..states import Steps
from ..keyboards import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

from shop.database.models import User, Item, Subcategory, UserBucked, MessageStatus

catalog = Router()


@catalog.callback_query(F.data == 'catalog')
async def in_catalog(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text(text=CATALOG_TEXT, reply_markup=await categoty_keyboard())
    
    
@catalog.callback_query(F.data == 'menu')
async def go_menu(callback: CallbackQuery, user: User):
    await callback.answer('')
    await callback.message.edit_text(
        text=f'{MENU_TEXT} {user.first_name}',
        reply_markup=menu_keyboard()
    )
    
    
@catalog.callback_query(F.data.startswith('categorychange_'))
async def change_catalog(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(
        text=CATALOG_TEXT,
        reply_markup=await categoty_keyboard(int(callback.data.split('_')[1]))
    )
    
    
@catalog.callback_query(F.data.startswith('Category_'))
async def subcategory(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    category_name = callback.data.split('_')[1]
    await state.update_data(catalog_name=category_name)
    await callback.message.edit_text(
        text=f'{SUBCATEGORY_TEXT}{category_name}',
        reply_markup=await subcategory_intkeyboard(category_name=category_name)
    )
        
    
@catalog.callback_query(F.data.startswith('subcatchange_'))
async def change_subcategories(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    data = await state.get_data()
    await callback.message.edit_text(
        text=f'{SUBCATEGORY_TEXT}{data.get("catalog_name")}',
        reply_markup=await subcategory_intkeyboard(
            category_name=data.get("catalog_name"),
            page=int(callback.data.split('_')[1])
        )
    )


@catalog.callback_query(F.data.startswith('subcategory_'))
async def items_show(callback: CallbackQuery, state: FSMContext, user: User):
    await callback.answer('')
    subcategory_name = callback.data.split('_')[1]
    subcategory = await Subcategory.objects.aget(name=subcategory_name)
    await state.update_data(item_count=1)
    async for item in Item.objects.filter(subcategory=subcategory):
        msg = await callback.message.answer_photo(
            photo=FSInputFile(item.image.path),
            caption=item.caption,
            reply_markup=item_keyboard(item.name)
        )
        
        await MessageStatus.objects.acreate(
            user=user,
            message_id=msg.message_id,
            item=item,
            count=1
        )


@catalog.callback_query(F.data.startswith('item_'))
async def item_in_bucked(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    bot = callback.bot
    message_item = await MessageStatus.objects.aget(
        message_id=callback.message.message_id
    )
    try:
        msgs = await sync_to_async(lambda: list(MessageStatus.objects.all()))()
        for msg in msgs:
            if msg.message_id != message_item.message_id:
                await bot.delete_message(
                    chat_id=callback.message.chat.id,
                    message_id=msg.message_id
                )
                await sync_to_async(MessageStatus.objects.filter(message_id=msg.message_id).delete)()
    except Exception as e:
        print(e)
    item = await sync_to_async(lambda: message_item.item)()
    count = message_item.count
    await callback.message.edit_caption(
        caption=f'Товар: {item.name}\nКоличество: {count}\nОбщая стоимость: {item.price * count}',
        reply_markup=item_count_keyboard()
    )
    
    
@catalog.callback_query(F.data == 'downcount')
async def down_count(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    message_item = await MessageStatus.objects.aget(
        message_id=callback.message.message_id
    )
    item = await sync_to_async(lambda: message_item.item)()
   
    item_count = message_item.count
    
    if item_count <= 1:
        return
    
    await sync_to_async(lambda: setattr(message_item, 'count', item_count - 1))()
    await sync_to_async(message_item.save)()
    await callback.message.edit_caption(
        caption=f'Товар: {item.name}\nКоличество: {item_count-1}\nОбщая цена: {(item_count-1) * item.price}',
        reply_markup=item_count_keyboard()
    )
    
    
@catalog.callback_query(F.data == 'upcount')
async def down_count(callback: CallbackQuery, state: FSMContext):
    message_item = await MessageStatus.objects.aget(
        message_id=callback.message.message_id
    )
    item = await sync_to_async(lambda: message_item.item)()
    item_count = message_item.count
    
    await sync_to_async(lambda: setattr(message_item, 'count', item_count + 1))()
    await sync_to_async(message_item.save)()
    await callback.message.edit_caption(
        caption=f'Товар: {item.name}\nКоличество: {item_count+1}\nОбщая цена: {(item_count+1) * item.price}',
        reply_markup=item_count_keyboard()
    )
    
@catalog.callback_query(F.data == 'iteminbucked')
async def submit_item(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_reply_markup(reply_markup=submit_item_keyboard())
    
    
@catalog.callback_query(F.data == 'change_item_count')
async def item_in_bucked(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    message_item = await MessageStatus.objects.aget(
        message_id=callback.message.message_id
    )
      
    item = await sync_to_async(lambda: message_item.item)()
    count = message_item.count
    await callback.message.edit_caption(
        caption=f'Товар: {item.name}\nКоличество: {count}\nОбщая стоимость: {item.price * count}',
        reply_markup=item_count_keyboard()
    )
    

@catalog.callback_query(F.data == 'items_in_backed')
async def do_bucked_model(callback: CallbackQuery, state: FSMContext, user: User):
    
    message_item = await MessageStatus.objects.aget(
        message_id=callback.message.message_id
    )
      
    item = await sync_to_async(lambda: message_item.item)()
 
    
    await UserBucked.objects.acreate(
        user=user,
        item=item,
        count=message_item.count
    )
    
    
    await callback.answer('Товар добавлен в корзину')
    await state.clear()
    await state.update_data(item_count=1)
    await callback.message.delete()
    
    await callback.message.answer(
            f'{MENU_TEXT} {user.first_name}',
            reply_markup=menu_keyboard()
        )
    
