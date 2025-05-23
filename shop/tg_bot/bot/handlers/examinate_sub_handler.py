import sys

from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.fsm.context import FSMContext

from ..keyboards import menu_keyboard, examinate_keyboard
from ..states import Steps
from ..text import *

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

from shop import config
from shop.database.models import User


examinate = Router()

async def is_user_subscribed(chat_id: int, user_id: int, bot: Bot) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR
        ]
    except Exception as e:
        print(f'Ошибка при проверки подписки: {e}')
        return False
    
    
@examinate.message(CommandStart())
async def cmd_start(message: Message, user: User, state: FSMContext):
    in_channel = await is_user_subscribed(config.CHANEL_ID, user.id, message.bot)
    in_group = await is_user_subscribed(config.GROUP_ID, user.id, message.bot)
    
    if in_channel and in_group:
        await message.answer(
            f'MENU_TEXT {user.first_name}',
            reply_markup=menu_keyboard()
        )
        await state.set_state(Steps.menu)
        return
    
    await message.answer(
        EXAMINATION_SUB_TEXT,
        reply_markup=examinate_keyboard()
    )
    
    
@examinate.callback_query(F.data == 'submit')
async def exam_begin(callback: CallbackQuery, user: User, state: FSMContext):
    await callback.message.delete()
    await callback.answer('')
    in_channel = await is_user_subscribed(config.CHANEL_ID, user.id, callback.bot)
    in_group = await is_user_subscribed(config.GROUP_ID, user.id, callback.bot)
    
    if in_channel and in_group:
        await callback.message.answer(f'{MENU_TEXT} {user.first_name}', reply_markup=menu_keyboard())
        await state.set_state(Steps.menu)
        return
    
    await callback.message.answer(
        EXAMINATION_SUB_TEXT,
        reply_markup=examinate_keyboard()
    )
    