# users/serializers.py
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from rest_framework import serializers
from .models import CustomUser
from djoser.serializers import UserSerializer as DjoserUserSerializer

class UserCreateSerializer(DjoserUserCreateSerializer):
    password2 = serializers.CharField(write_only=True, label='Confirmação de Senha')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'nome', 'sobrenome']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, attrs):
        # Verifica se as senhas coincidem
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        if password != password2:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        
        # Adicione validação para o email se necessário
        if CustomUser.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"email": "Este email já está em uso."})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remover a confirmação de senha
        user = CustomUser(**validated_data)  # Criar a instância do usuário
        user.set_password(validated_data['password'])  # Definir a senha
        user.save()  # Salvar o usuário
        return user  # Retornar a instância do usuário




class UserUpdateSerializer(DjoserUserSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email'] 

