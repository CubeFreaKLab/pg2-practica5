from django.contrib import admin
from pedidos_cafe.models import PedidoCafe

@admin.register(PedidoCafe)
class PedidoCafeAdmin(admin.ModelAdmin):
    """
    Configuración del admin para PedidoCafe.
    Muestra información relevante y permite filtrar por diferentes campos.
    """
    list_display = ('id', 'cliente', 'tipo_base', 'tamanio', 'fecha', 'mostrar_ingredientes')
    list_filter = ('tipo_base', 'tamanio', 'fecha')
    search_fields = ('cliente', 'tipo_base')
    readonly_fields = ('fecha',)
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('cliente',)
        }),
        ('Detalles del Pedido', {
            'fields': ('tipo_base', 'ingredientes', 'tamanio')
        }),
        ('Información del Sistema', {
            'fields': ('fecha',),
            'classes': ('collapse',)
        }),
    )
    
    def mostrar_ingredientes(self, obj):
        """Muestra los ingredientes de forma legible en la lista"""
        if obj.ingredientes:
            return ', '.join(obj.ingredientes)
        return 'Sin ingredientes adicionales'
    
    mostrar_ingredientes.short_description = 'Ingredientes'
    
    def get_queryset(self, request):
        """Optimiza las consultas del admin"""
        return super().get_queryset(request)
    
    def save_model(self, request, obj, form, change):
        """Personaliza el guardado desde el admin"""
        from api_patrones.logger import Logger
        
        logger = Logger()
        if change:
            logger.registrar(f"Admin: Actualizado pedido {obj.id} por usuario {request.user.username}")
        else:
            logger.registrar(f"Admin: Creado nuevo pedido por usuario {request.user.username}")
        
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        """Personaliza la eliminación desde el admin"""
        from api_patrones.logger import Logger
        
        logger = Logger()
        logger.registrar(f"Admin: Eliminado pedido {obj.id} por usuario {request.user.username}")
        
        super().delete_model(request, obj)

# Personalizar el admin site
admin.site.site_header = "Administración de Pedidos de Café"
admin.site.site_title = "Pedidos de Café"
admin.site.index_title = "Panel de Administración"