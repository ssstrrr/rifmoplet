"""
Данные по стихотворным размерам: название, схема стопы, описание, примеры, мнемоника.
"""
from typing import TypedDict


class MeterInfo(TypedDict):
    name: str
    scheme: str
    description: str
    examples: list[str]
    mnemonic: str
    cheatsheet: str
    wiki_url: str
    wiki_title: str


METERS: dict[str, MeterInfo] = {
    "iamb": {
        "name": "Ямб",
        "scheme": "˘ ¯ (та-та́)",
        "description": "Двусложный размер: безударный слог перед ударным. Восходящая интонация, разговорная динамика.",
        "examples": [
            "Мороз и солнце, день чудесный",
            "Люблю грозу в начале мая",
        ],
        "mnemonic": "Я́мб — та-та́: сначала тихо, потом удар по второму слогу.",
        "cheatsheet": "Безударный + ударный слоги (˘ ¯). Часто звучит как естественная русская речь.",
        "wiki_url": "https://ru.wikipedia.org/wiki/Ямб_(стихосложение)",
        "wiki_title": "Ямб_(стихосложение)",
    },
    "trochee": {
        "name": "Хорей",
        "scheme": "¯ ˘ (та́-та)",
        "description": "Двусложный размер: ударение на первый слог стопы. Нисходящий шаг, песенная упругость.",
        "examples": [
            "Буря мглою небо кроет",
            "Белой ночью думы грустные",
        ],
        "mnemonic": "Хорей — ТА-та: начинаем с сильного шага и скатываемся вниз.",
        "cheatsheet": "Ударный + безударный слоги (¯ ˘). Даёт маршевый, напевный ритм.",
        "wiki_url": "https://ru.wikipedia.org/wiki/Хорей",
        "wiki_title": "Хорей",
    },
    "dactyl": {
        "name": "Дактиль",
        "scheme": "¯ ˘ ˘",
        "description": "Трёхсложный размер: один ударный слог, за ним два безударных. Мягкая развёрнутость образа.",
        "examples": [
            "Тучки небесные, вечные странники",
            "Све́жий и зы́бкий над морем туман густой",
        ],
        "mnemonic": "Да́ктиль — ТА-та-та: как длинный шаг с плавным затуханием.",
        "cheatsheet": "Ударный + два безударных (¯ ˘ ˘). Тянет фразу вперёд, делая её размашистой.",
        "wiki_url": "https://ru.wikipedia.org/wiki/Дактиль_(стихосложение)",
        "wiki_title": "Дактиль_(стихосложение)",
    },
    "amphibrach": {
        "name": "Амфибрахий",
        "scheme": "˘ ¯ ˘",
        "description": "Трёхсложный размер: ударение на средний слог между двумя безударными. Длинный синтаксис, качающийся ритм.",
        "examples": [
            "Есть женщины в русских селеньях",
            "Горят огни, и гаснут свечи",
        ],
        "mnemonic": "Амфибра́хий — та-ТА-та: ударение спрятано посередине трёхсложной волны.",
        "cheatsheet": "Безударный + ударный + безударный (˘ ¯ ˘). Часто используется в описательных рассказах.",
        "wiki_url": "https://ru.wikipedia.org/wiki/Амфибрахий",
        "wiki_title": "Амфибрахий",
    },
    "anapaest": {
        "name": "Анапест",
        "scheme": "˘ ˘ ¯",
        "description": "Трёхсложный размер: два безударных слога, затем ударный. Наращивает движение к финалу.",
        "examples": [
            "О, весна без конца и без краю",
            "И опять предо мной, как вчера, возникает",
        ],
        "mnemonic": "Анапе́ст — та-та-ТА: разбег на двух лёгких слогах и прыжок в конце.",
        "cheatsheet": "Два безударных + ударный (˘ ˘ ¯). Даёт ощущение разгона и выстрела в конце строки.",
        "wiki_url": "https://ru.wikipedia.org/wiki/Анапест_(стихосложение)",
        "wiki_title": "Анапест_(стихосложение)",
    },
}


def get_meter(key: str) -> MeterInfo | None:
    return METERS.get(key)


def get_main_example(key: str) -> str | None:
    meter = METERS.get(key)
    if not meter or not meter["examples"]:
        return None
    return meter["examples"][0]


def get_random_example(key: str) -> str | None:
    import random

    meter = METERS.get(key)
    if not meter or not meter["examples"]:
        return None
    return random.choice(meter["examples"])


def get_all_meters() -> dict[str, MeterInfo]:
    return METERS
