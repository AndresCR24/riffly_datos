from django.contrib import admin
from .models import Producto, Cliente

# Register your models here.

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('-fecha_creacion',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'telefono', 'fecha_registro')
    list_filter = ('fecha_registro',)
    search_fields = ('nombre', 'email', 'telefono')
    ordering = ('nombre',)
