import os

import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {"chat_id": chat_id, "text": text}

    requests.post(url, data=data)
