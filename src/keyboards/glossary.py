"""
Inline-клавиатура для мини-словарика терминов.
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.content.glossary import GLOSSARY

GLOSSARY_CALLBACK_PREFIX = "gloss_"
GLOSSARY_BACK_CALLBACK_DATA = "gloss_back"


def glossary_inline_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=term["name"],
                callback_data=f"{GLOSSARY_CALLBACK_PREFIX}{key}",
            )
        ]
        for key, term in GLOSSARY.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def glossary_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="← К списку терминов", callback_data=GLOSSARY_BACK_CALLBACK_DATA
                )
            ]
        ]
    )

