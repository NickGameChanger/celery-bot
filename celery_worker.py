import requests

import config
from celery_app import app

URL_REMINDER = f'{config.API_URL}/api/send_reminder'

@app.task()
def send_reminder(text: str, chat_id: int) -> None:
    requests.post(URL_REMINDER, json={'text':text, 'chat_id': chat_id})
    return
