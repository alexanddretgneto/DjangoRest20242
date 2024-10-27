# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from .models import Rating
# from .serializers import RatingSerializer

from .serializers import UserSerializer
from .models import User
from rest_framework import  viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('usuario').all()
    serializer_class = UserSerializer

# class RatingsView(generics.ListCreateAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer


        
# # views.py
# from django.http import HttpResponse

# def home(request):
#     return HttpResponse("Bem-vindo ao Little Lemon API!")
