from django.contrib import admin
from .models import Categoria, Contato


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'telefone', 'email', 'data_criacao', 'categoria', 'mostrar')
    list_display_links = ('nome', 'sobrenome')
    list_editable = ('telefone', 'mostrar')
    list_per_page = 10



admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)


