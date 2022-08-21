import os
from celery_app import app
import telegram
from telegram.ext import Defaults
import config
import requests

URL_REMINDER = f'{config.API_URL}/api/send_reminder'

@app.task()
def send_reminder(text: str, chat_id: int) -> None:
    requests.post(URL_REMINDER, json={'text':text, 'chat_id': chat_id})
    return
