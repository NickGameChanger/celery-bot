import functools
from typing import Callable, Optional

from telegram.ext import CallbackContext
from telegram import Update


def tg_handler() -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper_func(
            update: Update, context: CallbackContext
        ) -> None:
            chat = update.effective_chat

            if not chat:
                raise ValueError('No chat in update')

            res = func(chat, update, context)
            return res

        return wrapper_func

    return decorator
