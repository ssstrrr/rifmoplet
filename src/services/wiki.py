"""
Получение кратких описаний размеров из Wikipedia API.
"""
from __future__ import annotations

from typing import Final
from urllib.parse import quote

import aiohttp

from src.content.meters import get_meter

_WIKI_CACHE: dict[str, str] = {}
_WIKI_TIMEOUT: Final[int] = 5


async def get_wiki_summary_for_meter(key: str) -> str | None:
    """
    Возвращает краткое описание размера из Википедии или None при ошибке.
    Результаты кэшируются в памяти процесса.
    """
    if key in _WIKI_CACHE:
        return _WIKI_CACHE[key]

    meter = get_meter(key)
    if not meter:
        return None

    title = meter.get("wiki_title")
    if not title:
        return None

    url = f"https://ru.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=_WIKI_TIMEOUT) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
    except Exception:
        return None

    extract = data.get("extract")
    if not extract:
        return None

    _WIKI_CACHE[key] = extract
    return extract

