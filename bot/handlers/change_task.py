from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.config import bot
from bot.db import tasks
from bot.handlers.create_task import create_task
from bot.states import States

router = Router()


@router.callback_query(F.data.contains('changeTask'))
async def del_task(message: CallbackQuery, state: FSMContext):
    id_task = int(message.data.replace("changeTask_", ""))
    del tasks[id_task]
    await create_task(message, state)


change_task_rt = router
