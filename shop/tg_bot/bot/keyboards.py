import sys

from itertools import batched

from pathlib import Path
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asgiref.sync import sync_to_async

from .text import *


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

from shop import config
from shop.database.models import Category, Subcategory


PAGES = 6

def examinate_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=EXAMINATION_CHANEL_TEXT, url=config.CHANEL_URL)],
            [InlineKeyboardButton(text=EXAMINATION_GROUP_TEXT, url=config.GROUP_URL)],
            [InlineKeyboardButton(text=EXAMINATION_SUBMIT_TEXT, callback_data='submit')],
        ]
    )


def menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=CATALOG_BUTTON_TEXT, callback_data='catalog')],
            [InlineKeyboardButton(text=BUCKED_BUTTON_TEXT, callback_data='bucked')],
            [InlineKeyboardButton(text=FAQ_BUTTON_TEXT, callback_data='faq')],
        ]
    )
    
    
async def categoty_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    keyboard = []
    
    categories = await sync_to_async(lambda: list(Category.objects.all()))()
    categories_count = await sync_to_async(len)(categories)
    categories = categories[page * PAGES:(page + 1) * PAGES]
    
    for pair_but in batched(categories, n=2):
        keyboard.append(list())
        for category in pair_but:
            keyboard[-1].append(InlineKeyboardButton(
                text=category.name,
                callback_data=f'Category_{category.name}'
            ))
            
    keyboard.append(list())
    if page != 0:
        keyboard[-1].append(InlineKeyboardButton(
            text=BACK_BUTTON_TEXT,
            callback_data=f'categorychange_{page - 1}'
        ))
        
    if (page + 1) * PAGES < categories_count:
        keyboard[-1].append(InlineKeyboardButton(
            text=FRONT_BUTTON_TEXT,
            callback_data=f'categorychange_{page + 1}'
        ))
        
    keyboard.append([
        InlineKeyboardButton(text=GO_MENU_TEXT, callback_data='menu')
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def subcategory_intkeyboard(category_name, page: int = 0):
    keyboard = []
    subcategories = []
    category = await Category.objects.aget(name=category_name)
    
    async for item in Subcategory.objects.filter(category=category):
        subcategories.append(item)
        
    subcategories_count = await sync_to_async(len)(subcategories)
    subcategories = subcategories[page * PAGES:(page + 1) * PAGES]
    
    for pair in batched(subcategories, n=2):
        keyboard.append(list())
        for item in pair:
            keyboard[-1].append(InlineKeyboardButton(
                text=item.name,
                callback_data=f'subcategory_{item.name}'
            ))
            
    keyboard.append(list())
    
    if page != 0:
        keyboard[-1].append(
            InlineKeyboardButton(
                text=BACK_BUTTON_TEXT,
                callback_data=f'subcatchange_{page - 1}'
            )
        )
        
    if (page + 1) * PAGES < subcategories_count:
        keyboard[-1].append(
            InlineKeyboardButton(
                text=FRONT_BUTTON_TEXT,
                callback_data=f'subcatchange_{page + 1}'
            )
        )
        
    keyboard.append([InlineKeyboardButton(
        text=GO_CATEGORYES_BTN_TEXT,
        callback_data='catalog'
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
        
        
def item_keyboard(item_name: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=GET_ITEM_IN_BUCKED, callback_data=f'item_{item_name}')],
    ])
    
    
def item_count_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=MINUS_ITEM_TEXT, callback_data='downcount'),
         InlineKeyboardButton(text=PLUS_ITEM_TEXT, callback_data='upcount')],
        [InlineKeyboardButton(text=SUBMIT_ITEM_TEXT, callback_data='iteminbucked')]
    ])
    
    
def submit_item_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=GET_ITEM_IN_BUCKED, callback_data='items_in_backed')],
        [InlineKeyboardButton(text=CHANGE_ITEM_TEXT, callback_data='change_item_count')]
    ])
    
    
def bucked_keyboard(bucked_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=BUCKED_SUBMIT_TEXT, callback_data=f'submititembuy_{bucked_id}')],
        [InlineKeyboardButton(text=BUCKED_DELETE_ITEM, callback_data=f'deleteitemfrombucked_{bucked_id}')]
    ])
    


async def go_pay():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=PAY_SUBMIT, callback_data='get_pay_link')],
        [InlineKeyboardButton(text=PAY_CHANGE_DATA, callback_data='change_delivery_data')]
    ])