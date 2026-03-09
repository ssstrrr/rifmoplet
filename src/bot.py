"""
Инициализация бота и диспетчера, регистрация роутеров и глобального обработчика ошибок.
"""
import logging

from aiogram import Dispatcher
from aiogram.types import ErrorEvent

from src.commands.cheatsheet import router as cheatsheet_router
from src.commands.glossary import router as glossary_router
from src.commands.guess import router as guess_router
from src.commands.start import router as start_router
from src.handlers.callbacks import router as callbacks_router
from src.handlers.glossary import router as glossary_callbacks_router

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
    dp.include_router(cheatsheet_router)
    dp.include_router(guess_router)
    dp.include_router(glossary_router)
    dp.include_router(glossary_callbacks_router)
    dp.include_router(callbacks_router)
    dp.error.register(on_error)
    return dp
