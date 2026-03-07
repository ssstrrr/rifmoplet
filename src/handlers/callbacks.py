"""
Обработка нажатий по inline-кнопкам размеров.
"""
from aiogram import Router
from aiogram.types import CallbackQuery

from src.content.meters import get_meter
from src.keyboards.sizes import CALLBACK_PREFIX, back_to_list_keyboard, sizes_inline_keyboard

router = Router(name="callbacks")


def format_meter_message(key: str) -> str | None:
    meter = get_meter(key)
    if not meter:
        return None
    return (
        f"<b>{meter['name']}</b>\n\n"
        f"Схема стопы: <code>{meter['scheme']}</code>\n\n"
        f"{meter['description']}\n\n"
        f"Пример:\n<i>«{meter['example']}»</i>"
    )


@router.callback_query(lambda c: c.data and c.data.startswith(CALLBACK_PREFIX))
async def process_size_callback(callback: CallbackQuery) -> None:
    data = callback.data
    if data == "size_back":
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
        reply_markup=back_to_list_keyboard(),
    )
    await callback.answer()
