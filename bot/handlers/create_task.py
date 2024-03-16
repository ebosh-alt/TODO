from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot import keyboards as kb
from bot.config import bot
from bot.db.models import ModelTask
from bot.states import States
from bot.db import tasks, Task
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query(F.data.in_(("create_task", "change_title")))
async def create_task(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    if message.data == "change_title":
        await state.clear()
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Введите заголовок",
                                reply_markup=kb.create_keyboard("Назад": "main_menu"))
    await state.set_state(States.create_task)
    await state.update_data(message_id=message.message.message_id)


@router.callback_query(F.data == "change_description")
async def change_description(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id,
                                text="Введите описание",
                                reply_markup=kb.confirm_description_kb)


@router.message(States.create_task)
async def input_data(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    task = data.get("task")
    if task is None:
        task = ModelTask(title=message.text)
        keyboard = kb.confirm_title_kb
        text = f"Вы ввели: {message.text}\nВведите описание"

    else:
        task.description = message.text
        keyboard = kb.confirm_description_kb
        text = f"Ваша задача\nЗаголовок: {task.title}\nОписание: {task.description}"
    await state.update_data(task=task)
    await message.delete()
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id,
                                text=text,
                                reply_markup=keyboard)


@router.callback_query(F.data == "confirm_task")
async def confirm_task(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    task = data["task"]
    tasks.add(Task(id=tasks.new_id + 1,
                   user_id=id,
                   title=task.title,
                   description=task.description))
    await bot.answer_callback_query(callback_query_id=message.id, text="Задача создана")
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id,
                                text=get_mes("start"),
                                reply_markup=kb.start_kb)
    await state.clear()


creat_rt = router
