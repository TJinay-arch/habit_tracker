from celery import shared_task
from django.utils import timezone

from telegram_bot.services import send_telegram_message

from .models import Habit


@shared_task
def send_habit_reminder():
    now = timezone.localtime().time()

    habits = Habit.objects.filter(time__hour=now.hour)

    for habit in habits:
        user = habit.user

        if user.telegram_chat_id:
            send_telegram_message(user.telegram_chat_id, f"Напоминание: {habit.action} в {habit.place}")
