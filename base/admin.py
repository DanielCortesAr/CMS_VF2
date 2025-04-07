from django.contrib import admin
from .models import Vehiculo

# Registrar el modelo Vehiculo
@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    # Personalizar cómo se muestran los campos en la lista del admin
    list_display = ('placas', 'marca', 'modelo', 'color', 'año')
    
    # Agregar un campo de búsqueda
    search_fields = ('placas', 'marca', 'modelo')
    
    # Agregar filtros laterales
    list_filter = ('marca', 'año')
    
    # Personalizar el formulario de edición/creación
    fieldsets = (
        ('Información General', {
            'fields': ('fotografia_vehiculo', 'placas', 'marca', 'modelo')
        }),
        ('Detalles Adicionales', {
            'fields': ('color', 'año')
        }),
    )

    