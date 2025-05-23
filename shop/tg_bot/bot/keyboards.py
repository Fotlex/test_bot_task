import sys

from pathlib import Path
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .text import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

from shop import config


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
    