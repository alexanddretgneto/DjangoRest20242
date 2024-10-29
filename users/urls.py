# users/urls.py
from django.urls import include, path
from .views import UserCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [

    path('', include('djoser.urls')),  # Incluir as URLs do Djoser
    path('', include('djoser.urls.jwt')),  # Para autenticação baseada em token JWT, se necessário
    path('', include('djoser.urls.authtoken')),  # Para autenticação baseada em token DRF, se necessário
    
]