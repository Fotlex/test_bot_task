from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states import Steps
from ..keyboards import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

from shop import config
from shop.database.models import User

catalog = Router()


@catalog.callback_query(F.data == 'catalog')
async def in_catalog(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text(text=CATALOG_TEXT, reply_markup=await categoty_keyboard())
    
    
@catalog.callback_query(F.data == 'menu')
async def go_menu(callback: CallbackQuery, user: User):
    await callback.message.edit_text(
        text=f'{MENU_TEXT} {user.first_name}',
        reply_markup=menu_keyboard()
    )
    
    
@catalog.callback_query(F.data.startswith('categorychange_'))
async def change_catalog(callback: CallbackQuery):
    await callback.message.edit_text(
        text=CATALOG_TEXT,
        reply_markup=await categoty_keyboard(int(callback.data.split('_')[1]))
    )
        
    

