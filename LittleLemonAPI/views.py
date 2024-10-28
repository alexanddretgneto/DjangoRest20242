from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import OrderingFilter, SearchFilter

from LittleLemonAPI import serializers, models
from LittleLemonAPI.permissions import IsManager, IsDeliveryCrew, IsCustomer, ReadOnly


class MenuItemViewSet(ModelViewSet):
    # permission_classes = [IsAdminUser|IsManager|ReadOnly]
    serializer_class = serializers.MenuItemSerializer
    queryset = models.MenuItem.objects.all()
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category', 'price', 'featured', 'title']
    ordering_fields = ['id', 'price', 'title']
    search_fields = ['category__title', 'title']


class CategoryViewSet(ModelViewSet):
    # permission_classes = [IsAdminUser|IsManager|ReadOnly]
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
