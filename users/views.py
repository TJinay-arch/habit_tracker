from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class SaveTelegramAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        chat_id = request.data.get("chat_id")

        if not chat_id:
            return Response({"error": "chat_id required"}, status=400)

        request.user.telegram_chat_id = chat_id
        request.user.save()

        return Response({"status": "chat_id saved"})
