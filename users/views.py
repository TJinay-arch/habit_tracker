from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import TelegramSerializer, UserSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class TelegramUpdateView(UpdateAPIView):
    serializer_class = TelegramSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
