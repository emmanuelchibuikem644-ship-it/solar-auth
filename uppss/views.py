from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)

        return Response({
            "user": {
                "username": user.username,
                "email": user.email
            },
            "access": tokens['access'],
            "refresh": tokens['refresh']
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        tokens = get_tokens_for_user(user)

        return Response({
            "user": {
                "username": user.username,
                "email": user.email
            },
            "access": tokens['access'],
            "refresh": tokens['refresh']
        })

    return Response({"detail": "Invalid credentials"}, status=401)