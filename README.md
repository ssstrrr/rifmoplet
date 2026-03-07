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
