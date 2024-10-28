# users/views.py
from rest_framework import generics
from .serializers import UserCreateSerializer

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

