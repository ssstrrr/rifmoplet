"""
Обработка нажатий по inline-кнопкам мини-словарика.
"""
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from src.content.glossary import get_term
from src.keyboards.glossary import (
    GLOSSARY_BACK_CALLBACK_DATA,
    GLOSSARY_CALLBACK_PREFIX,
    glossary_inline_keyboard,
)

router = Router(name="glossary_callbacks")

START_BACK = "start_back"


def glossary_keyboard_with_start() -> InlineKeyboardMarkup:
    kb = glossary_inline_keyboard()
    return InlineKeyboardMarkup(
        inline_keyboard=kb.inline_keyboard
        + [[InlineKeyboardButton(text="← В начало", callback_data=START_BACK)]]
    )


def format_term_message(key: str) -> str | None:
    term = get_term(key)
    if not term:
        return None
    return f"<b>{term['name']}</b>\n\n{term['definition']}"


@router.callback_query(lambda c: c.data and c.data == GLOSSARY_BACK_CALLBACK_DATA)
async def process_glossary_back(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Мини-словарик по стихосложению.\n\nВыбери термин:",
        reply_markup=glossary_keyboard_with_start(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith(GLOSSARY_CALLBACK_PREFIX))
async def process_glossary_term(callback: CallbackQuery) -> None:
    data = callback.data
    key = data.replace(GLOSSARY_CALLBACK_PREFIX, "", 1)
    text = format_term_message(key)
    if not text:
        await callback.answer("Термин не найден.", show_alert=True)
        return

    await callback.message.edit_text(
        text,
        reply_markup=glossary_keyboard_with_start(),
    )
    await callback.answer()

