from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from bot import keyboards as kb
from bot.config import bot
from bot.db import tasks
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query(F.data == "view_task")
async def view(message: CallbackQuery, from_delete: bool = None):
    id = message.from_user.id
    data = tasks.get_tasks_user(id)
    if data is None:
        if from_delete:
            await bot.edit_message_text(chat_id=id,
                                        message_id=message.message.message_id,
                                        text=get_mes("start"),
                                        reply_markup=kb.start_kb)
            return 200
        await bot.answer_callback_query(callback_query_id=message.id, text="У Вас нет созданных задач")
        return 200
    buttons = {}
    for task in data:
        buttons.update({task.title: f"task_{task.id}"})
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("view_task"),
                                reply_markup=kb.create_keyboard(buttons))


@router.callback_query(F.data.contains('task_'))
async def view_task(message: CallbackQuery):
    id = message.from_user.id
    id_task = int(message.data.replace("task_", ""))
    task = tasks.get(id_task)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=f"{task.title}\n\n{task.description}",
                                reply_markup=kb.create_keyboard({"Удалить задачу": f"delTask_{id_task}",
                                                                 "Изменить задачу": f"changeTask_{id_task}",
                                                                 "Назад": "view_task"}, 2, 1))


view_task_rt = router
