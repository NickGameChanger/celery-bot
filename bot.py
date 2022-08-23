import logging

from telegram import Update, Chat
from telegram.ext import (ApplicationBuilder, CallbackContext, CommandHandler,
                          MessageHandler, filters)

import config
from celery_worker import send_reminder
from decorators import tg_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


@tg_handler()
async def remind(chat: Chat, update: Update, context: CallbackContext) -> None:
    error_text = '/remind 1 text // 1 - кол-во секунд через которое будет выслано напоминание, text - то что мам нужно напомнить'
    if not context.args or len(context.args) < 2:
        await context.bot.send_message(chat_id=chat.id, text=error_text)
        return
    try:
        time = int(context.args[0])
        text = ' '.join(context.args[1:])
    except ValueError:
        await context.bot.send_message(chat_id=chat.id, text=error_text)
        return

    send_reminder.apply_async((text, chat.id), countdown=time)


@tg_handler()
async def start(chat: Chat, update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(
        chat_id=chat.id, text=(
            'Hello boi! here you can make reminder\n\n'
            '/remind — выбери время и напиши, что тебе напомнить'
            )
    )


@tg_handler()
async def unknown(chat: Chat, update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TOKEN).build()

    start_handler = CommandHandler('start', start)
    remind_handler = CommandHandler('remind', remind)
    application.add_handler(remind_handler)
    application.add_handler(start_handler)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
