from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from bot import keyboards as kb
from bot.config import bot
from bot.db import tasks
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query(F.data == "main_menu")
@router.message(Command("start"))
async def start(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.clear()
    await bot.send_message(chat_id=id,
                           text=get_mes("start"),
                           reply_markup=kb.start_kb)


start_rt = router
