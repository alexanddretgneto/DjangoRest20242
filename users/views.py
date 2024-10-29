# users/views.py
from rest_framework import generics
from .serializers import UserCreateSerializer
from rest_framework.decorators import action
from users.serializers import UserUpdateSerializer
from rest_framework import viewsets, permissions
from users.models import CustomUser
from rest_framework.response import Response

from rest_framework import status
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    
class UserUpdateSerializer(DjoserUserSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']  # Campos que queremos permitir atualização

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request):
        user = request.user  # O usuário autenticado

        if request.method == 'GET':
            # serializer = UserUpdateSerializer(user)
            serializer = DjoserUserSerializer(user)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = DjoserUserSerializer(user, data=request.data, partial=True)  # Atualizações parciais
            if serializer.is_valid():
                serializer.save()

                # Reemite o token com os dados atualizados do usuário
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)