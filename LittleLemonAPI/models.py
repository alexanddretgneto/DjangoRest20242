from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User


def today():
    return timezone.now().date()

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self) -> str:
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

        
    # class Meta:
    #     unique_together = ['menuitem', 'user']
    def __str__(self):
        return f"{self.menuitem.title} - {self.quantity} (User: {self.user.username})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('in_progress', 'Em Preparação'),
        ('delivered', 'Entregue'),
        ('canceled', 'Cancelado'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    date = models.DateField(db_index=True, default=today)

    def calculate_total(self):
        # Calcula o total com base nos itens de pedido
        self.total = sum(item.price for item in self.orderitem_set.all())
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ['order', 'menuitem']
