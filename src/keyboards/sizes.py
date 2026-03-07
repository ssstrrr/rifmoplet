"""
Inline-клавиатура со списком стихотворных размеров.
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.content.meters import METERS

CALLBACK_PREFIX = "size_"


def sizes_inline_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=data["name"], callback_data=f"{CALLBACK_PREFIX}{key}")]
        for key, data in METERS.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_list_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="← К списку размеров", callback_data="size_back")]
        ]
    )
