"""
Inline-клавиатура для режима «Угадай размер».
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.content.meters import METERS

QUIZ_CALLBACK_PREFIX = "quiz_"


def quiz_options_keyboard(correct_key: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=meter["name"],
                callback_data=f"{QUIZ_CALLBACK_PREFIX}{correct_key}:{key}",
            )
        ]
        for key, meter in METERS.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

