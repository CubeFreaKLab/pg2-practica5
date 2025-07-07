from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pedidos_cafe.views import PedidoCafeViewSet

# Crear el router para las APIs REST
router = DefaultRouter()
router.register(r'pedidos', PedidoCafeViewSet, basename='pedidos')

urlpatterns = [
    path('api/', include(router.urls)),
]

# URLs disponibles:
# GET /api/pedidos/ - Lista todos los pedidos
# POST /api/pedidos/ - Crea un nuevo pedido
# GET /api/pedidos/{id}/ - Obtiene un pedido específico
# PUT /api/pedidos/{id}/ - Actualiza un pedido específico
# DELETE /api/pedidos/{id}/ - Elimina un pedido específico
# GET /api/pedidos/tipos_cafe/ - Lista tipos de café disponibles
# GET /api/pedidos/ingredientes_disponibles/ - Lista ingredientes disponibles
# GET /api/pedidos/tamanios_disponibles/ - Lista tamaños disponibles
# GET /api/pedidos/{id}/calcular_precio/ - Recalcula precio de un pedido
# GET /api/pedidos/logs_sistema/ - Obtiene logs del sistema
# POST /api/pedidos/limpiar_logs/ - Limpia los logs del sistema
# GET /api/pedidos/estadisticas/ - Obtiene estadísticas generales