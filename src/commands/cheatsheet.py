"""
Команда /cheatsheet: шпаргалка по всем стихотворным размерам.
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.content.meters import get_all_meters

router = Router(name="cheatsheet")


def build_cheatsheet_text() -> str:
    meters = get_all_meters()
    parts: list[str] = []
    for meter in meters.values():
        parts.append(
            f"<b>{meter['name']}</b> — <code>{meter['scheme']}</code>\n"
            f"{meter['cheatsheet']}"
        )
    header = "Шпаргалка по стихотворным размерам:\n\n"
    return header + "\n\n".join(parts)


@router.message(Command("cheatsheet"))
async def cmd_cheatsheet(message: Message) -> None:
    await message.answer(build_cheatsheet_text())

