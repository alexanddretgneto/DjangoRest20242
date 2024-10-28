from django.contrib.auth.models import Group
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

    class Meta:
        model = models.MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_name']  # Inclui category e category_name
        
    def create(self, validated_data):
        # A categoria é obtida automaticamente através do validated_data
        return super().create(validated_data)
