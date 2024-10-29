from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import serializers
from LittleLemonAPI import models

class CategorySerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        write_only=True,  # Apenas para gravação
        source='group'  # Nome do campo no modelo, se necessário
    )
    group = serializers.StringRelatedField(read_only=True)  # Para mostrar o nome do grupo no retorno

    class Meta:
        model = models.Category
        fields = '__all__'
        read_only_fields = ['id']

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=models.Category.objects.all())  # Permite a seleção da categoria
    category_name = serializers.CharField(source='category.title', read_only=True)  # Mostra o nome da categoria ao exibir
    add_to_cart_url = serializers.SerializerMethodField()
    
    class Meta:
        model = models.MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_name', 'add_to_cart_url']  # Inclui category e category_name
        

    def get_add_to_cart_url(self, obj):
        # Retorna o URL para a ação `add_to_cart`
        request = self.context.get('request')
        return request.build_absolute_uri(f'/menu-items/{obj.id}/add-to-cart/')    
        
    def create(self, validated_data):
        # A categoria é obtida automaticamente através do validated_data
        return super().create(validated_data)

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['id', 'user', 'unit_price', 'price']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order  # Substitua pelo seu modelo de pedido
        fields = '__all__'  # Ou especifique os campos que deseja incluir
        
    
    
