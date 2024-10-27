# models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    nome = models.CharField(max_length=100, default='Nome Padrão')
    sobrenome = models.CharField(max_length=100, default='Sobrenome Padrão')


    groups = models.ManyToManyField(
        Group,
        related_name='little_lemon_user_set',  # Altere o nome aqui para evitar conflitos
        blank=True,
        help_text='Os grupos aos quais este usuário pertence.',
        verbose_name='grupos'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='little_lemon_user_permissions_set',  # Altere o nome aqui para evitar conflitos
        blank=True,
        help_text='Permissões específicas para este usuário.',
        verbose_name='permissões de usuário'
    )

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome}"  # Retorna o nome completo

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relacionamento com o usuário
    score = models.IntegerField()  # Campo para a pontuação
    comment = models.TextField(blank=True)  # Campo para comentários

    def __str__(self):
        return f'Rating {self.score} by {self.user.username}'
