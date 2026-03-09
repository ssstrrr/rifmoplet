"""
Команда /guess_meter: режим «Угадай размер».
"""
import random

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.content.meters import METERS, get_random_example
from src.keyboards.quiz import quiz_options_keyboard

router = Router(name="guess")


@router.message(Command("guess_meter", "guess"))
async def cmd_guess_meter(message: Message) -> None:
    if not METERS:
        await message.answer("Размеры пока не настроены.")
        return

    key = random.choice(list(METERS.keys()))
    example = get_random_example(key)
    if not example:
        await message.answer("Пока не могу подобрать пример для игры.")
        return

    text = (
        "Попробуй угадать размер строки:\n\n"
        f"<i>«{example}»</i>\n\n"
        "Выбери вариант:"
    )
    await message.answer(text, reply_markup=quiz_options_keyboard(key))

