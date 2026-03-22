from celery import shared_task
from django.utils import timezone
import requests
from django.conf import settings

from .models import Habit


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    max_retries=3
)
def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"

    response = requests.post(url, data={
        "chat_id": chat_id,
        "text": text
    })

    response.raise_for_status()


@shared_task
def send_habit_reminder():
    now = timezone.localtime()

    habits = Habit.objects.select_related('user').filter(
        time__hour=now.hour,
        user__telegram_chat_id__isnull=False
    )

    for habit in habits:
        send_telegram_message.delay(
            habit.user.telegram_chat_id,
            f"Напоминание: {habit.action} в {habit.place}"
        )
