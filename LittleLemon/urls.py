from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from LittleLemonAPI import views


router = DefaultRouter(trailing_slash=False)
router.register('menu-items', views.MenuItemViewSet)
router.register('categories', views.CategoryViewSet)
router.register('group/manager/users', views.ManagerViewSet, basename='managers')
router.register('group/delivery-crew/users', views.DeliveryCrewViewSet, basename='delivery-crew')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('carts/menu-items', views.CartViewSet, basename='carts')  # Registra o CartViewSet

urlpatterns = [ 
    path('admin/', admin.site.urls), 
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),  # Corrigido: fechando a linha corretamente
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # path('ll/', include('LittleLemonAPI.urls'))
    ]
