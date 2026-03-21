from rest_framework.exceptions import ValidationError


def validate_habit(data):
    reward = data.get("reward")
    related = data.get("related_habit")
    is_pleasant = data.get("is_pleasant")
    execution_time = data.get("execution_time")
    periodicity = data.get("periodicity")

    # нельзя reward + related
    if reward and related:
        raise ValidationError("Укажите либо reward, либо related_habit")

    # max 120 сек
    if execution_time and execution_time > 120:
        raise ValidationError("Время выполнения не более 120 секунд")

    # только pleasant можно связывать
    if related and not related.is_pleasant:
        raise ValidationError("Связанная привычка должна быть приятной")

    # pleasant не может иметь reward/related
    if is_pleasant and (reward or related):
        raise ValidationError("Приятная привычка не имеет награды или связи")

    # периодичность ≤ 7
    if periodicity and periodicity > 7:
        raise ValidationError("Нельзя реже 1 раза в 7 дней")
