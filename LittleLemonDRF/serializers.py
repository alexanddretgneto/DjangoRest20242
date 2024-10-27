
from rest_framework import serializers
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, label='Confirmação de Senha')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'nome', 'sobrenome']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remover a confirmação de senha
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Definir a senha
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nome', 'sobrenome']


