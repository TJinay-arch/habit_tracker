from django.conf import settings
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)

    is_pleasant = models.BooleanField(default=False)

    related_habit = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    periodicity = models.PositiveIntegerField(default=1)

    reward = models.CharField(max_length=255, blank=True, null=True)

    execution_time = models.PositiveIntegerField()

    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.action
