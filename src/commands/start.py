"""
Обработчик команды /start: приветствие и список размеров (inline-кнопки).
"""
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.keyboards.sizes import sizes_inline_keyboard

router = Router(name="start")

START_TEXT = (
    "Привет! Я бот <b>Рифмоплёт</b>.\n\n"
    "Выбери стихотворный размер — покажу схему стопы и пример строки.\n\n"
    "Ещё: <b>Шпаргалка</b> — все размеры сразу, <b>Угадай размер</b> — игра, "
    "<b>Словарик</b> — термины."
)


def start_keyboard() -> InlineKeyboardMarkup:
    sizes = sizes_inline_keyboard()
    extra_row = [
        InlineKeyboardButton(text="📋 Шпаргалка", callback_data="start_cheatsheet"),
        InlineKeyboardButton(text="🎯 Угадай размер", callback_data="start_guess"),
        InlineKeyboardButton(text="📖 Словарик", callback_data="start_glossary"),
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[extra_row] + sizes.inline_keyboard
    )


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        START_TEXT,
        reply_markup=start_keyboard(),
    )
