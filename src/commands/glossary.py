"""
Команда /glossary: список терминов и мини-словарик.
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.keyboards.glossary import glossary_inline_keyboard

router = Router(name="glossary")


@router.message(Command("glossary"))
async def cmd_glossary(message: Message) -> None:
    await message.answer(
        "Мини-словарик по стихосложению.\n\nВыбери термин:",
        reply_markup=glossary_inline_keyboard(),
    )

