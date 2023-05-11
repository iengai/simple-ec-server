# accounts/views.py
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # 设置权限类为 AllowAny

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        username = request.data.get('username')
        user = User.objects.filter(username=username).first()
        refresh_token = RefreshToken.for_user(user)
        response_data = {
            'access': str(refresh_token.access_token),
            'refresh': str(refresh_token),
        }
        response.data = response_data
        return response

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh_token = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
            }
            return Response(response_data, status=200)

        return Response({'detail': 'Invalid credentials'}, status=401)
