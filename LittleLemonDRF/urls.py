from django.urls import include, path 
from . import views 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [ 
#    path('', views.RatingsView.as_view()), 
    # path('auth/', include('djoser.urls')),  # Incluir as URLs do Djoser
    # path('auth/', include('djoser.urls.authtoken')),  # Para autenticação baseada em token, se necessário
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Para login
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Para renovar token
    
    
] 