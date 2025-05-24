import sys

from itertools import batched

from pathlib import Path
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asgiref.sync import sync_to_async

from .text import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

from shop import config
from shop.database.models import Category


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