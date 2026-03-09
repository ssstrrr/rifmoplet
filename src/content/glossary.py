"""
Мини-словарик терминов стихосложения.
"""
from typing import TypedDict


class TermInfo(TypedDict):
    name: str
    definition: str


GLOSSARY: dict[str, TermInfo] = {
    "foot": {
        "name": "Стопа",
        "definition": "Минимальная ритмическая единица стиха: сочетание ударных и безударных слогов, которое повторяется в строке.",
    },
    "two_foot_iamb": {
        "name": "Двустопный ямб",
        "definition": "Строка, построенная из двух ямбических стоп (˘ ¯ ˘ ¯). Часто даёт короткий, пружинящий ритм.",
    },
    "caesura": {
        "name": "Цезура",
        "definition": "Пауза внутри стихотворной строки, которая делит её на части и усиливает интонационный рисунок.",
    },
}


def get_term(key: str) -> TermInfo | None:
    return GLOSSARY.get(key)


def get_all_terms() -> dict[str, TermInfo]:
    return GLOSSARY

