"""
Обработка нажатий по inline-кнопкам размеров.
"""
import random

from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from src.commands.cheatsheet import build_cheatsheet_text
from src.commands.start import START_TEXT, start_keyboard
from src.content.meters import METERS, get_main_example, get_meter, get_random_example
from src.keyboards.glossary import glossary_inline_keyboard
from src.keyboards.quiz import QUIZ_CALLBACK_PREFIX, quiz_options_keyboard
from src.keyboards.sizes import (
    BACK_CALLBACK_DATA,
    CALLBACK_PREFIX,
    MORE_EXAMPLE_PREFIX,
    WIKI_DESC_PREFIX,
    meter_details_keyboard,
    sizes_inline_keyboard,
)
from src.services.wiki import get_wiki_summary_for_meter

router = Router(name="callbacks")

START_CALLBACK_PREFIX = "start_"
START_BACK = "start_back"


@router.callback_query(
    lambda c: c.data and c.data.startswith(START_CALLBACK_PREFIX)
)
async def process_start_shortcuts(callback: CallbackQuery) -> None:
    data = callback.data
    if data == START_BACK:
        await callback.message.edit_text(
            START_TEXT,
            reply_markup=start_keyboard(),
        )
        await callback.answer()
        return
    if data == "start_cheatsheet":
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="← В начало", callback_data=START_BACK)]
            ]
        )
        await callback.message.edit_text(
            build_cheatsheet_text(),
            reply_markup=kb,
        )
        await callback.answer()
        return
    if data == "start_guess":
        if not METERS:
            await callback.answer("Размеры пока не настроены.", show_alert=True)
            return
        key = random.choice(list(METERS.keys()))
        example = get_random_example(key)
        if not example:
            await callback.answer("Пока не могу подобрать пример.", show_alert=True)
            return
        text = (
            "Попробуй угадать размер строки:\n\n"
            f"<i>«{example}»</i>\n\n"
            "Выбери вариант:"
        )
        quiz_kb = quiz_options_keyboard(key)
        back_row = [
            [InlineKeyboardButton(text="← В начало", callback_data=START_BACK)]
        ]
        full_kb = InlineKeyboardMarkup(
            inline_keyboard=quiz_kb.inline_keyboard + back_row
        )
        await callback.message.edit_text(text, reply_markup=full_kb)
        await callback.answer()
        return
    if data == "start_glossary":
        gloss_kb = glossary_inline_keyboard()
        back_row = [
            [InlineKeyboardButton(text="← В начало", callback_data=START_BACK)]
        ]
        full_kb = InlineKeyboardMarkup(
            inline_keyboard=gloss_kb.inline_keyboard + back_row
        )
        await callback.message.edit_text(
            "Мини-словарик по стихосложению.\n\nВыбери термин:",
            reply_markup=full_kb,
        )
        await callback.answer()
        return
    await callback.answer()


def format_meter_message(key: str) -> str | None:
    meter = get_meter(key)
    if not meter:
        return None
    example = get_main_example(key)
    if not example:
        return None
    return (
        f"<b>{meter['name']}</b>\n\n"
        f"Схема стопы: <code>{meter['scheme']}</code>\n\n"
        f"{meter['description']}\n\n"
        f"<i>{meter['mnemonic']}</i>\n\n"
        f"Пример:\n<i>«{example}»</i>"
    )


def format_meter_message_with_example(key: str, example: str) -> str | None:
    meter = get_meter(key)
    if not meter:
        return None
    return (
        f"<b>{meter['name']}</b>\n\n"
        f"Схема стопы: <code>{meter['scheme']}</code>\n\n"
        f"{meter['description']}\n\n"
        f"<i>{meter['mnemonic']}</i>\n\n"
        f"Пример:\n<i>«{example}»</i>"
    )


@router.callback_query(lambda c: c.data and c.data.startswith(QUIZ_CALLBACK_PREFIX))
async def process_quiz_callback(callback: CallbackQuery) -> None:
    data = callback.data
    payload = data.replace(QUIZ_CALLBACK_PREFIX, "", 1)
    try:
        correct_key, chosen_key = payload.split(":", 1)
    except ValueError:
        await callback.answer("Не удалось разобрать ответ.", show_alert=True)
        return

    is_correct = chosen_key == correct_key
    meter_text = format_meter_message(correct_key)
    if not meter_text:
        await callback.answer("Размер не найден.", show_alert=True)
        return

    result_text = (
        "Верно! Это действительно этот размер."
        if is_correct
        else "Не угадал. Вот разбор строки:"
    )

    await callback.message.edit_text(
        f"{result_text}\n\n{meter_text}",
        reply_markup=meter_details_keyboard(correct_key),
    )
    await callback.answer("Отлично!" if is_correct else "В следующий раз получится!")


@router.callback_query(lambda c: c.data and c.data.startswith(MORE_EXAMPLE_PREFIX))
async def process_more_example(callback: CallbackQuery) -> None:
    data = callback.data
    key = data.replace(MORE_EXAMPLE_PREFIX, "", 1)
    example = get_random_example(key)
    if not example:
        await callback.answer("Не удалось подобрать пример.", show_alert=True)
        return

    text = format_meter_message_with_example(key, example)
    if not text:
        await callback.answer("Размер не найден.", show_alert=True)
        return

    await callback.message.edit_text(
        text,
        reply_markup=meter_details_keyboard(key),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith(WIKI_DESC_PREFIX))
async def process_wiki_description(callback: CallbackQuery) -> None:
    data = callback.data
    key = data.replace(WIKI_DESC_PREFIX, "", 1)

    summary = await get_wiki_summary_for_meter(key)
    if not summary:
        await callback.answer(
            "Пока не удалось получить описание из Википедии.", show_alert=True
        )
        return

    meter = get_meter(key)
    if not meter:
        await callback.answer("Размер не найден.", show_alert=True)
        return

    text = (
        f"<b>{meter['name']}</b>\n\n"
        f"{summary}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=meter_details_keyboard(key),
    )
    await callback.answer()


@router.callback_query(
    lambda c: c.data
    and c.data.startswith(CALLBACK_PREFIX)
    and not c.data.startswith(MORE_EXAMPLE_PREFIX)
    and not c.data.startswith(WIKI_DESC_PREFIX)
)
async def process_size_callback(callback: CallbackQuery) -> None:
    data = callback.data
    if data == BACK_CALLBACK_DATA:
        await callback.message.edit_text(
            "Выбери стихотворный размер:",
            reply_markup=sizes_inline_keyboard(),
        )
        await callback.answer()
        return

    key = data.replace(CALLBACK_PREFIX, "", 1)
    text = format_meter_message(key)
    if not text:
        await callback.answer("Размер не найден.", show_alert=True)
        return

    await callback.message.edit_text(
        text,
        reply_markup=meter_details_keyboard(key),
    )
    await callback.answer()
