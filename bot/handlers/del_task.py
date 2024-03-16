from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.config import bot
from bot.db import tasks
from bot.handlers.view_task import view

router = Router()


@router.callback_query(F.data.contains('delTask'))
async def del_task(message: CallbackQuery):
    id_task = int(message.data.replace("delTask_", ""))
    del tasks[id_task]
    await bot.answer_callback_query(callback_query_id=message.id, text="Задача удалена")
    await view(message, from_delete=True)


del_task_rt = router
