"""
Обработчик команды /start: приветствие и список размеров (inline-кнопки).
"""
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.keyboards.sizes import sizes_inline_keyboard

router = Router(name="start")

START_TEXT = (
    "Привет! Я бот <b>Рифмоплёт</b>.\n\n"
    "Выбери стихотворный размер — покажу схему стопы и пример строки."
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        START_TEXT,
        reply_markup=sizes_inline_keyboard(),
    )
