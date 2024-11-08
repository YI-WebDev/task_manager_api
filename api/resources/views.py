from django.db import transaction
from .models import UserAuthority
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class CreateUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializer.ValidationError(f'Username {username} is already taken.')
        serializer.save()


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "success": True,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            if not User.objects.filter(username=username).exists():
                return Response(
                    {"detail": "ユーザーが存在しません。"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            return Response(
                {"detail": "パスワードが正しくありません。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_authority = UserAuthority.objects.get(user=user)
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "role": user_authority.role,
            },
            status=status.HTTP_200_OK,
        )
