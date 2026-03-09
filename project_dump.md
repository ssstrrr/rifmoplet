# Project dump

## Дерево проекта

```
рифмоплет/
├── .cursor/
│   └── rules/
│       └── file-size-and-splitting.mdc
├── src/
│   ├── commands/
│   │   ├── __init__.py
│   │   └── start.py
│   ├── content/
│   │   ├── __init__.py
│   │   └── meters.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   └── callbacks.py
│   ├── keyboards/
│   │   ├── __init__.py
│   │   └── sizes.py
│   ├── __init__.py
│   └── bot.py
├── .env.example
├── .gitignore
├── export_project.py
├── main.py
├── README.md
└── requirements.txt
```

--- START OF FILE .cursor/rules/file-size-and-splitting.mdc ---

```text
---
description: Дробление кодовой базы — файлы не более 500 строк при добавлении функций
alwaysApply: true
---

# Лимит размера файлов и дробление кода

## Правило

- **Максимум 500 строк в одном файле.** Ни один исходный файл (`.py`, `.js`, `.ts` и т.п.) не должен превышать 500 строк.
- При **добавлении новых функций** сначала проверять размер затронутых файлов. Если после добавления файл превысит 500 строк — перед коммитом **разбить** его на несколько файлов.

## Как дробить

1. **По ответственности:** один модуль/файл — одна зона ответственности (например: только команды, только клавиатуры, только контент).
2. **По домену:** группировать по фичам или сущностям (например: `handlers/start.py`, `handlers/sizes.py` вместо одного огромного `handlers.py`).
3. **Вынос данных/конфигов:** большие словари, константы, контент — в отдельные файлы (например `content/meters.py`, `content/constants.py`).
4. **Публичный API:** в разбитом модуле оставлять в `__init__.py` только реэкспорт того, что нужно снаружи; реализацию держать в отдельных файлах.

## Проверка перед завершением задачи

- Для каждого изменённого или нового файла: число строк ≤ 500.
- Если файл > 500 строк: спланировать разбиение (по разделам выше) и выполнить его в той же задаче.

## Исключения

- Сгенерированные файлы, lock-файлы, миграции БД можно не дробить по этому правилу, если иное не оговорено в проекте.

```

--- END OF FILE .cursor/rules/file-size-and-splitting.mdc ---

--- START OF FILE .env.example ---

```text
# Получить токен: @BotFather в Telegram
BOT_TOKEN=your_bot_token_here

```

--- END OF FILE .env.example ---

--- START OF FILE .gitignore ---

```text
.env
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
.env.local
*.log

```

--- END OF FILE .gitignore ---

--- START OF FILE export_project.py ---

```python
#!/usr/bin/env python3
"""
Скрипт экспорта проекта в единый Markdown-файл project_dump.md.
Сканирует текущую директорию, строит дерево и включает содержимое текстовых файлов.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from collections import defaultdict

# --- Константы ---
OUTPUT_FILE = "project_dump.md"
MAX_FILE_SIZE_BYTES = 1024 * 1024  # 1 МБ

# Директории, которые полностью игнорируются
IGNORED_DIRS = {
    "node_modules",
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    ".idea",
    ".vscode",
}

# Файлы по точному имени (без учёта регистра пути)
IGNORED_FILES = {
    "package-lock.json",
    "yarn.lock",
    ".env",
    "project_dump.md",
}

# Расширения файлов для игнорирования
IGNORED_EXTENSIONS = {
    ".log", ".pyc", ".cache", ".ds_store",
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".mp4", ".mov", ".ico", ".avif",
    ".woff", ".woff2", ".ttf", ".eot",
    ".zip", ".gz", ".tar",
}

# Суффикс директорий для игнорирования
IGNORED_DIR_SUFFIX = ".egg-info"


def should_ignore_dir(name: str) -> bool:
    """Проверяет, нужно ли игнорировать директорию."""
    if name in IGNORED_DIRS:
        return True
    if name.lower().endswith(IGNORED_DIR_SUFFIX):
        return True
    return False


def should_ignore_file(name: str, path: Path) -> bool:
    """Проверяет, нужно ли игнорировать файл по имени и расширению."""
    if name in IGNORED_FILES:
        return True
    if name.lower() in {f.lower() for f in IGNORED_FILES}:
        return True
    ext = path.suffix.lower()
    if ext in IGNORED_EXTENSIONS:
        return True
    return False


def is_text_file(path: Path) -> tuple[bool, str | None]:
    """
    Пытается прочитать файл как UTF-8. Возвращает (True, content) или (False, error_msg).
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return True, f.read()
    except UnicodeDecodeError as e:
        return False, f"не UTF-8: {e}"
    except OSError as e:
        return False, str(e)


def build_tree(root: Path, prefix: str = "", dirs_only: bool = False) -> list[str]:
    """
    Строит список строк для дерева (как tree). Учитывает игнорирование.
    """
    lines = []
    try:
        entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    except OSError:
        return lines

    # Разделяем директории и файлы, отфильтровывая игнорируемые
    dirs = []
    files = []
    for p in entries:
        if p.name.startswith(".") and p.name not in (".env", ".git", ".idea", ".vscode"):
            # Уже в IGNORED_DIRS или обрабатываем отдельно
            pass
        if p.is_dir():
            if not should_ignore_dir(p.name):
                dirs.append(p)
        else:
            if not should_ignore_file(p.name, p):
                if not dirs_only:
                    files.append(p)
                else:
                    pass  # для дерева включаем только имена файлов

    # Сначала директории
    for i, d in enumerate(dirs):
        is_last_dir = i == len(dirs) - 1 and not files
        connector = "└── " if is_last_dir and not files else "├── "
        lines.append(prefix + connector + d.name + "/")
        extension = "    " if is_last_dir and not files else "│   "
        lines.extend(build_tree(d, prefix + extension, dirs_only=False))

    # Затем файлы
    for i, f in enumerate(files):
        is_last = i == len(files) - 1
        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + f.name)

    return lines


def collect_files(root: Path) -> list[Path]:
    """Собирает все файлы для включения в дамп (с учётом игнорирования)."""
    result = []
    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        # Удаляем игнорируемые директории из обхода
        dirnames[:] = [d for d in dirnames if not should_ignore_dir(d)]
        path_dir = Path(dirpath)
        for name in filenames:
            fp = path_dir / name
            if should_ignore_file(name, fp):
                continue
            result.append(fp)
    return sorted(result, key=lambda p: str(p).lower())


def get_language(path: Path) -> str:
    """Возвращает язык для блока кода по расширению."""
    ext_to_lang = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "javascript",
        ".tsx": "typescript",
        ".md": "markdown",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".html": "html",
        ".css": "css",
        ".scss": "scss",
        ".sh": "bash",
        ".bat": "batch",
        ".ps1": "powershell",
        ".sql": "sql",
        ".toml": "toml",
        ".ini": "ini",
        ".cfg": "ini",
        ".txt": "text",
        ".xml": "xml",
        ".csv": "csv",
    }
    return ext_to_lang.get(path.suffix.lower(), "text")


def main() -> None:
    root = Path(".").resolve()
    print(f"Сканирование: {root}")
    print()

    # Статистика
    stats = defaultdict(int)
    stats["included"] = 0
    stats["skipped_binary"] = 0
    stats["skipped_size"] = 0
    stats["skipped_other"] = 0

    # 1. Строим дерево
    tree_lines = [root.name + "/"] + build_tree(root)
    tree_md = "\n".join(tree_lines)

    # 2. Собираем файлы
    files = collect_files(root)
    # Относительные пути от root
    rel_files = [f.relative_to(root) for f in files]

    output_lines = [
        "# Project dump",
        "",
        "## Дерево проекта",
        "",
        "```",
        tree_md,
        "```",
        "",
    ]

    for rel_path in rel_files:
        full_path = root / rel_path
        path_str = str(rel_path).replace("\\", "/")

        # Проверка размера
        try:
            size = full_path.stat().st_size
        except OSError:
            stats["skipped_other"] += 1
            print(f"  [ПРОПУСК] {path_str} (ошибка доступа)")
            continue

        if size > MAX_FILE_SIZE_BYTES:
            stats["skipped_size"] += 1
            print(f"  [ПРОПУСК] {path_str} (размер > 1 МБ)")
            continue

        print(f"  [ОБРАБОТКА] {path_str}")

        is_text, content_or_error = is_text_file(full_path)
        if not is_text:
            stats["skipped_binary"] += 1
            print(f"    -> бинарный/не UTF-8: {content_or_error}")
            continue

        content = content_or_error
        lang = get_language(full_path)

        output_lines.append(f"--- START OF FILE {path_str} ---")
        output_lines.append("")
        output_lines.append(f"```{lang}")
        output_lines.append(content)
        output_lines.append("```")
        output_lines.append("")
        output_lines.append(f"--- END OF FILE {path_str} ---")
        output_lines.append("")

        stats["included"] += 1

    # Запись в файл
    with open(root / OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print()
    print("--- Статистика ---")
    print(f"  Включено в дамп:     {stats['included']}")
    print(f"  Пропущено (бинарные/не UTF-8): {stats['skipped_binary']}")
    print(f"  Пропущено (размер > 1 МБ):     {stats['skipped_size']}")
    print(f"  Пропущено (прочее):  {stats['skipped_other']}")
    print(f"  Итоговый файл:       {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    sys.exit(0)

```

--- END OF FILE export_project.py ---

--- START OF FILE main.py ---

```python
"""
Точка входа. Запуск long polling с корректным завершением (graceful shutdown).
"""
import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.bot import create_dispatcher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не задан. Создайте файл .env по образцу .env.example")

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = create_dispatcher()

    try:
        logger.info("Бот запущен")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Остановка бота")

```

--- END OF FILE main.py ---

--- START OF FILE README.md ---

```markdown
# Рифмоплёт — Telegram-бот про стихотворные размеры

По команде **Start** бот показывает список стихотворных размеров (ямб, хорей, дактиль, амфибрахий, анапест). По нажатию на размер — схема стопы и пример строки.

## Запуск

1. **Python 3.10+** и виртуальное окружение:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # или: source .venv/bin/activate  # Linux/macOS
   ```

2. **Зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Токен бота:**
   - Напиши [@BotFather](https://t.me/BotFather) в Telegram, создай бота, скопируй токен.
   - Создай файл `.env` в корне проекта (по образцу `.env.example`):
     ```
     BOT_TOKEN=123456:ABC-DEF...
     ```

4. **Запуск:**

   ```bash
   python main.py
   ```

Остановка: `Ctrl+C` (корректное завершение).

## Структура проекта

- `main.py` — точка входа, long polling, graceful shutdown
- `src/bot.py` — создание диспетчера, роутеры, глобальный обработчик ошибок
- `src/commands/start.py` — команда /start и приветствие
- `src/handlers/callbacks.py` — обработка нажатий по размерам
- `src/keyboards/sizes.py` — inline-клавиатура со списком размеров
- `src/content/meters.py` — данные по размерам (схема, описание, пример)

## Практики (по скиллу telegram-bot-builder)

- Inline-клавиатуры для выбора размера
- Async (aiogram 3), без блокирующих операций
- Глобальный error handler и логирование
- Токен из переменной окружения, не в коде
- Корректное завершение по SIGINT/SIGTERM

Скилл: [telegram-bot-builder](https://github.com/sickn33/antigravity-awesome-skills/blob/main/skills/telegram-bot-builder/SKILL.md) из коллекции [awesome-agent-skills](https://github.com/AlexProTg/awesome-agent-skills).

```

--- END OF FILE README.md ---

--- START OF FILE requirements.txt ---

```text
aiogram>=3.14
python-dotenv>=1.0.0

```

--- END OF FILE requirements.txt ---

--- START OF FILE src/__init__.py ---

```python


```

--- END OF FILE src/__init__.py ---

--- START OF FILE src/bot.py ---

```python
"""
Инициализация бота и диспетчера, регистрация роутеров и глобального обработчика ошибок.
"""
import logging

from aiogram import Dispatcher
from aiogram.types import ErrorEvent

from src.commands.start import router as start_router
from src.handlers.callbacks import router as callbacks_router

logger = logging.getLogger(__name__)


async def on_error(event: ErrorEvent) -> None:
    logger.exception("Ошибка при обработке апдейта: %s", event.exception)
    err_msg = "Произошла ошибка. Попробуй ещё раз или напиши /start."
    try:
        update = event.update
        if update.message:
            await update.message.answer(err_msg)
        elif update.callback_query and update.callback_query.message:
            await update.callback_query.answer("Ошибка. Попробуй снова.", show_alert=True)
    except Exception:
        pass


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(callbacks_router)
    dp.error.register(on_error)
    return dp

```

--- END OF FILE src/bot.py ---

--- START OF FILE src/commands/__init__.py ---

```python


```

--- END OF FILE src/commands/__init__.py ---

--- START OF FILE src/commands/start.py ---

```python
"""
Обработчик команды /start: приветствие и список размеров (inline-кнопки).
"""
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.keyboards.sizes import sizes_inline_keyboard

router = Router(name="start")

START_TEXT = (
    "Привет! Я бот <b>Рифмоплёт</b>.\n\n"
    "Выбери стихотворный размер — покажу схему стопы и пример строки."
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        START_TEXT,
        reply_markup=sizes_inline_keyboard(),
    )

```

--- END OF FILE src/commands/start.py ---

--- START OF FILE src/content/__init__.py ---

```python


```

--- END OF FILE src/content/__init__.py ---

--- START OF FILE src/content/meters.py ---

```python
"""
Данные по стихотворным размерам: название, схема стопы, описание, пример.
"""
from typing import TypedDict


class MeterInfo(TypedDict):
    name: str
    scheme: str
    description: str
    example: str


METERS: dict[str, MeterInfo] = {
    "iamb": {
        "name": "Ямб",
        "scheme": "˘ ¯ (та-та́)",
        "description": "Двусложный размер: ударение на второй слог стопы. Восходящая интонация, динамичная речь.",
        "example": "Мороз и солнце, день чудесный",
    },
    "trochee": {
        "name": "Хорей",
        "scheme": "¯ ˘ (та́-та)",
        "description": "Двусложный размер: ударение на первый слог стопы. Нисходящий шаг, песенная упругость.",
        "example": "Буря мглою небо кроет",
    },
    "dactyl": {
        "name": "Дактиль",
        "scheme": "¯ ˘ ˘",
        "description": "Трёхсложный размер: один ударный слог, за ним два безударных. Мягкая развёрнутость образа.",
        "example": "Тучки небесные, вечные странники",
    },
    "amphibrach": {
        "name": "Амфибрахий",
        "scheme": "˘ ¯ ˘",
        "description": "Трёхсложный размер: ударение на средний слог между двумя безударными. Длинный синтаксис.",
        "example": "Есть женщины в русских селеньях",
    },
    "anapaest": {
        "name": "Анапест",
        "scheme": "˘ ˘ ¯",
        "description": "Трёхсложный размер: два безударных слога, затем ударный. Наращивает движение к финалу.",
        "example": "О, весна без конца и без краю",
    },
}


def get_meter(key: str) -> MeterInfo | None:
    return METERS.get(key)

```

--- END OF FILE src/content/meters.py ---

--- START OF FILE src/handlers/__init__.py ---

```python


```

--- END OF FILE src/handlers/__init__.py ---

--- START OF FILE src/handlers/callbacks.py ---

```python
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

```

--- END OF FILE src/handlers/callbacks.py ---

--- START OF FILE src/keyboards/__init__.py ---

```python


```

--- END OF FILE src/keyboards/__init__.py ---

--- START OF FILE src/keyboards/sizes.py ---

```python
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

```

--- END OF FILE src/keyboards/sizes.py ---
