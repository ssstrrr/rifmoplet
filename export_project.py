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
