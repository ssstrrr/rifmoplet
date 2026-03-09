"""
Inline-клавиатура со списком стихотворных размеров.
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.content.meters import METERS

CALLBACK_PREFIX = "size_"
BACK_CALLBACK_DATA = "size_back"
MORE_EXAMPLE_PREFIX = "size_more_"
WIKI_DESC_PREFIX = "size_wiki_"


def sizes_inline_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=data["name"], callback_data=f"{CALLBACK_PREFIX}{key}")]
        for key, data in METERS.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_list_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="← К списку размеров", callback_data=BACK_CALLBACK_DATA)]
        ]
    )


def meter_details_keyboard(key: str) -> InlineKeyboardMarkup:
    meter = METERS.get(key)
    keyboard: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text="← К списку размеров", callback_data=BACK_CALLBACK_DATA)]
    ]

    keyboard.append(
        [
            InlineKeyboardButton(
                text="Ещё пример", callback_data=f"{MORE_EXAMPLE_PREFIX}{key}"
            ),
            InlineKeyboardButton(
                text="Ещё описание (Вики)", callback_data=f"{WIKI_DESC_PREFIX}{key}"
            ),
        ]
    )

    if meter and meter.get("wiki_url"):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="Подробнее в Википедии", url=meter["wiki_url"]
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
