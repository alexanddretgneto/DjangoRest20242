from urllib import request
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



from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from users.models import CustomUser


class MenuItemViewSet(ModelViewSet):
    
    serializer_class = serializers.MenuItemSerializer
    queryset = models.MenuItem.objects.all()
    
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category', 'featured']
    ordering_fields = ['id', 'price', 'title']
    search_fields = ['category__title', 'title']
    
    
    def get_permissions(self):
        # Permissões específicas para métodos
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            # Negar acesso para clientes e equipe de entrega
            if self.request.user.groups.filter(name='Customer').exists() or \
               self.request.user.groups.filter(name='DeliveryCrew').exists():
                return [ReadOnly()]  # Retorna 403 Forbidden para POST, PUT, PATCH, DELETE
            elif self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_staff:
                return [IsManager()]

        return super().get_permissions()

    # Para permitir o acesso apenas de leitura
    def list(self, request, *args, **kwargs):
        self.permission_classes = [ReadOnly]  # Apenas leitura para todos
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [ReadOnly]  # Apenas leitura para todos
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['patch'], url_path='set-daily-special')
    def set_daily_special(self, request, pk=None):
        item = self.get_object()
        item.is_daily_special = True
        item.save()
        return Response({'message': 'Item do dia atualizado com sucesso!'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='add-to-cart')
    def add_to_cart(self, request, pk=None):
        menuitem = self.get_object()
        quantity = request.data.get('quantity', 1)  # Define a quantidade padrão como 1

        # Validação da quantidade
        if not isinstance(quantity, int) or quantity <= 0:
            return Response({'error': 'A quantidade deve ser um número inteiro maior que zero.'}, status=status.HTTP_400_BAD_REQUEST)

        # Adiciona o item ao carrinho do usuário autenticado
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            menuitem=menuitem,
            defaults={
                'quantity': quantity,
                'unit_price': menuitem.price,  # Preço unitário do menu item
                'price': menuitem.price * quantity  # Total
            }
        )
        if not created:
            # Se o item já existe, atualiza a quantidade e o preço
            cart_item.quantity += quantity
            cart_item.price = cart_item.unit_price * cart_item.quantity
            cart_item.save()

        return Response(
            {
                'message': 'Item adicionado ao carrinho com sucesso!',
                'cart_item': serializers.CartSerializer(cart_item).data
            },
            status=status.HTTP_201_CREATED
        )
        

class CartViewSet(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer
    permission_classes = [IsAuthenticated]

    # Retorna os itens atuais no carrinho para o usuário autenticado
    def list(self, request, *args, **kwargs):
        cart_items = self.queryset.filter(user=request.user)
        serializer = self.serializer_class(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Adiciona o item de menu ao carrinho para o usuário autenticado
    def create(self, request, *args, **kwargs):
        menuitem_id = request.data.get('menuitem')
        quantity = request.data.get('quantity', 1)

        if menuitem_id is None:
            return Response({'error': 'O ID do item do menu é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        menuitem = get_object_or_404(models.MenuItem, id=menuitem_id)

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return Response({'error': 'A quantidade deve ser um número inteiro.'}, status=status.HTTP_400_BAD_REQUEST)

        if quantity <= 0:
            return Response({'error': 'A quantidade deve ser maior que zero.'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = models.Cart.objects.get_or_create(
            user=request.user,
            menuitem=menuitem,
            defaults={'quantity': quantity, 'unit_price': menuitem.price, 'price': menuitem.price * quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.price = cart_item.unit_price * cart_item.quantity
            cart_item.save()

        return Response(
            {'message': 'Item adicionado ao carrinho.', 'cart_item': serializers.CartSerializer(cart_item).data},
            status=status.HTTP_201_CREATED
        )

    # Exclui todos os itens de menu do carrinho para o usuário autenticado
    def destroy(self, request, *args, **kwargs):
        cart_items = self.queryset.filter(user=request.user)
        if not cart_items.exists():
            return Response({'message': 'Nenhum item no carrinho para deletar.'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_items.delete()
        return Response({'message': 'Todos os itens do carrinho foram removidos.'}, status=status.HTTP_204_NO_CONTENT)
class CategoryViewSet(ModelViewSet):
    # permission_classes = [IsAdminUser|IsManager|ReadOnly]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()

    def get_permissions(self):
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_staff:
            self.permission_classes = [IsAuthenticated]  # Admin e Manager podem fazer todas as operações
        elif self.request.user.groups.filter(name='DeliveryCrew').exists():
            self.permission_classes = [ReadOnly]  # DeliveryCrew apenas visualizar
        else:
            self.permission_classes = [ReadOnly]  # Apenas leitura para não autenticados
        return super().get_permissions()

class DeliveryCrewViewSet(ModelViewSet):
    queryset = User.objects.filter(groups__name='DeliveryCrew')
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]  # Todos autenticados podem ver

    @action(detail=True, methods=['post'])
    def add_user(self, request, pk=None):
        # Checa se o usuário tem permissão antes de adicionar um usuário à equipe de entrega
        self.check_permissions(request)  # Isso agora está dentro de um método de instância
        user = get_object_or_404(User, pk=pk)
        delivery_group = Group.objects.get(name='DeliveryCrew')
        delivery_group.user_set.add(user)
        return Response({'message': f'{user.username} adicionado à equipe de entrega.'}, status=status.HTTP_200_OK)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])  # Gerentes podem atribuir pedidos a um usuário da equipe de entrega
    def assign_to_delivery_crew(self, request, pk=None):
        order = self.get_object()
        user_id = request.data.get('user_id')
        
        # Verifica se o usuário existe e se está no grupo DeliveryCrew
        delivery_user = get_object_or_404(User, id=user_id, groups__name='DeliveryCrew')
        order.delivery_crew = delivery_user
        order.save()

        return Response({'message': f'Pedido atribuído a {delivery_user.username}.'}, status=status.HTTP_200_OK)

    def get_queryset(self):  # A equipe de entrega pode acessar os pedidos atribuídos a ela
        if self.request.user.groups.filter(name='DeliveryCrew').exists():
            return self.queryset.filter(delivery_crew=self.request.user)
        return self.queryset

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])  # A equipe de entrega pode atualizar um pedido como entregue
    def mark_as_delivered(self, request, pk=None):
        order = self.get_object()
        
        # Verifica se o usuário atual é parte do grupo DeliveryCrew
        if not self.request.user.groups.filter(name='DeliveryCrew').exists():
            return Response({'error': 'Você não tem permissão para marcar este pedido como entregue.'}, status=status.HTTP_403_FORBIDDEN)

        # Atualiza o status do pedido
        order.status = 'delivered'  # Atualiza o status para "Entregue"
        order.save()

        return Response({'message': 'Pedido marcado como entregue.'}, status=status.HTTP_200_OK)





class ManagerViewSet(viewsets.ModelViewSet):
    """
    A ViewSet para listar, adicionar e remover usuários do grupo de gerentes.
    """
    permission_classes = [IsAuthenticated, IsManager] 
    serializer_class = serializers.UserSerializer
    
    # def get_permissions(self):
    #     # Permissões específicas para métodos
    #     if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
    #         # Negar acesso para clientes e equipe de entrega
    #         if self.request.user.groups.filter(name='Customer').exists() or \
    #            self.request.user.groups.filter(name='DeliveryCrew').exists():
    #             return [ReadOnly()]  # Retorna 403 Forbidden para POST, PUT, PATCH, DELETE
    #         elif self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_staff:
    #             return [IsManager()]

    #     return super().get_permissions()

    def get_queryset(self):
        # Filtra os usuários que estão no grupo "Manager"
        
        managers_group = get_object_or_404(Group, name='Manager')
        return managers_group.user_set.all()

    def create(self, request, *args, **kwargs):
        # Adiciona um usuário ao grupo "managers"
        user_id = request.data.get('userId')
        if user_id:
            user = get_object_or_404(CustomUser, id=user_id)  # Usando CustomUser
            managers_group = get_object_or_404(Group, name='managers')
            managers_group.user_set.add(user)  # Adiciona o usuário ao grupo
            return Response(
                {'message': f'{user.username} successfully added to managers group'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'userId is required'},
            status=status.HTTP_400_BAD_REQUEST
        )


    def destroy(self, request, *args, **kwargs):
        # Remove um usuário do grupo "managers"
        user_id = self.kwargs.get('pk')  # Obtém o ID do usuário a ser removido
        user = get_object_or_404(CustomUser, id=user_id)  # Usando CustomUser
        managers_group = get_object_or_404(Group, name='managers')
        managers_group.user_set.remove(user)  # Remove o usuário do grupo
        return Response(
            {'message': f'{user.username} successfully removed from managers group'},
            status=status.HTTP_200_OK
        )
        