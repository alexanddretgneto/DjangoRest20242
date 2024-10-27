# admin.py
from django.contrib import admin
from .models import Rating

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'comment')  # Mostra os campos na listagem do admin
    search_fields = ('user__username', 'score')  # Permite busca por usuário e score
