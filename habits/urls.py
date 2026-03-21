from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import HabitViewSet, PublicHabitListAPIView

router = DefaultRouter()
router.register("habits", HabitViewSet, basename="habit")

urlpatterns = [
    path("public/", PublicHabitListAPIView.as_view()),
] + router.urls
