from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from pedidos_cafe.models import PedidoCafe
from pedidos_cafe.serializers import PedidoCafeSerializer, LoggerSerializer
from pedidos_cafe.factory import CafeFactory
from api_patrones.logger import Logger


class PedidoCafeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar todas las operaciones CRUD de PedidoCafe.
    Incluye endpoints adicionales para demostrar el uso de los patrones.
    """
    queryset = PedidoCafe.objects.all()
    serializer_class = PedidoCafeSerializer

    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo pedido de café.
        
        Returns:
            Response: Respuesta con el pedido creado o errores de validación
        """
        logger = Logger()
        logger.registrar(f"API: Recibida solicitud de creación de pedido")
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.registrar(f"API: Pedido creado exitosamente ID: {serializer.data['id']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            logger.registrar(f"API: Error en validación de pedido: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Actualiza un pedido existente.
        
        Returns:
            Response: Respuesta con el pedido actualizado o errores
        """
        logger = Logger()
        logger.registrar(f"API: Recibida solicitud de actualización de pedido ID: {kwargs.get('pk')}")
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.registrar(f"API: Pedido actualizado exitosamente ID: {instance.id}")
            return Response(serializer.data)
        else:
            logger.registrar(f"API: Error en actualización de pedido: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Elimina un pedido existente.
        
        Returns:
            Response: Respuesta de confirmación de eliminación
        """
        logger = Logger()
        instance = self.get_object()
        pedido_id = instance.id
        
        logger.registrar(f"API: Eliminando pedido ID: {pedido_id}")
        self.perform_destroy(instance)
        logger.registrar(f"API: Pedido eliminado exitosamente ID: {pedido_id}")
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def tipos_cafe(self, request):
        """
        Endpoint para obtener los tipos de café disponibles.
        Demuestra el uso del patrón Factory.
        
        Returns:
            Response: Lista de tipos de café disponibles
        """
        logger = Logger()
        logger.registrar("API: Consultando tipos de café disponibles")
        
        tipos = CafeFactory.obtener_tipos_disponibles()
        
        # Obtener información detallada de cada tipo
        tipos_detallados = []
        for tipo in tipos:
            try:
                cafe_base = CafeFactory.obtener_base(tipo)
                tipos_detallados.append({
                    "nombre": tipo,
                    "nombre_display": cafe_base.obtener_nombre(),
                    "precio_base": cafe_base.precio_base(),
                    "ingredientes_base": cafe_base.obtener_ingredientes_base()
                })
            except Exception as e:
                logger.registrar(f"ERROR al obtener info de {tipo}: {str(e)}")
        
        logger.registrar(f"API: Enviando información de {len(tipos_detallados)} tipos de café")
        
        return Response({
            "tipos_disponibles": tipos_detallados,
            "total_tipos": len(tipos_detallados)
        })

    @action(detail=False, methods=['get'])
    def ingredientes_disponibles(self, request):
        """
        Endpoint para obtener los ingredientes disponibles.
        
        Returns:
            Response: Lista de ingredientes disponibles con precios
        """
        logger = Logger()
        logger.registrar("API: Consultando ingredientes disponibles")
        
        # Obtener precios de ingredientes del builder
        from pedidos_cafe.builder import CafePersonalizadoBuilder
        from pedidos_cafe.factory import CafeFactory
        
        cafe_base = CafeFactory.obtener_base("espresso")  # Usar uno cualquiera para obtener precios
        builder = CafePersonalizadoBuilder(cafe_base)
        
        ingredientes = []
        for ingrediente, precio in builder.precios_ingredientes.items():
            ingredientes.append({
                "nombre": ingrediente,
                "precio_adicional": precio
            })
        
        logger.registrar(f"API: Enviando información de {len(ingredientes)} ingredientes")
        
        return Response({
            "ingredientes_disponibles": ingredientes,
            "total_ingredientes": len(ingredientes)
        })

    @action(detail=False, methods=['get'])
    def tamanios_disponibles(self, request):
        """
        Endpoint para obtener los tamaños disponibles.
        
        Returns:
            Response: Lista de tamaños disponibles con multiplicadores
        """
        logger = Logger()
        logger.registrar("API: Consultando tamaños disponibles")
        
        # Obtener multiplicadores del builder
        from pedidos_cafe.builder import CafePersonalizadoBuilder
        from pedidos_cafe.factory import CafeFactory
        
        cafe_base = CafeFactory.obtener_base("espresso")
        builder = CafePersonalizadoBuilder(cafe_base)
        
        tamanios = []
        for tamanio, multiplicador in builder.multiplicadores_tamanio.items():
            tamanios.append({
                "nombre": tamanio,
                "multiplicador": multiplicador
            })
        
        logger.registrar(f"API: Enviando información de {len(tamanios)} tamaños")
        
        return Response({
            "tamanios_disponibles": tamanios,
            "total_tamanios": len(tamanios)
        })

    @action(detail=True, methods=['get'])
    def calcular_precio(self, request, pk=None):
        """
        Endpoint para recalcular el precio de un pedido específico.
        Demuestra el uso de todos los patrones.
        
        Returns:
            Response: Información detallada del cálculo de precio
        """
        logger = Logger()
        pedido = self.get_object()
        logger.registrar(f"API: Recalculando precio para pedido ID: {pedido.id}")
        
        try:
            # Usar el serializer para obtener los datos calculados
            serializer = self.get_serializer(pedido)
            datos_calculados = {
                "pedido_id": pedido.id,
                "cliente": pedido.cliente,
                "tipo_base": pedido.tipo_base,
                "ingredientes_solicitados": pedido.ingredientes,
                "tamanio": pedido.tamanio,
                "precio_total": serializer.data['precio_total'],
                "ingredientes_finales": serializer.data['ingredientes_finales'],
                "resumen_construccion": serializer.data['resumen_construccion']
            }
            
            logger.registrar(f"API: Precio recalculado exitosamente para pedido ID: {pedido.id}")
            return Response(datos_calculados)
            
        except Exception as e:
            logger.registrar(f"ERROR al recalcular precio para pedido ID: {pedido.id}: {str(e)}")
            return Response(
                {"error": f"Error al calcular precio: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def logs_sistema(self, request):
        """
        Endpoint para obtener los logs del sistema.
        Demuestra el uso del patrón Singleton.
        
        Returns:
            Response: Logs del sistema
        """
        logger = Logger()
        logger.registrar("API: Consultando logs del sistema")
        
        serializer = LoggerSerializer(data={})
        return Response(serializer.to_representation(None))

    @action(detail=False, methods=['post'])
    def limpiar_logs(self, request):
        """
        Endpoint para limpiar los logs del sistema.
        
        Returns:
            Response: Confirmación de limpieza
        """
        logger = Logger()
        logs_anteriores = logger.contar_logs()
        logger.limpiar_logs()
        logger.registrar("API: Logs del sistema limpiados")
        
        return Response({
            "mensaje": "Logs limpiados exitosamente",
            "logs_eliminados": logs_anteriores
        })

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Endpoint para obtener estadísticas generales.
        
        Returns:
            Response: Estadísticas del sistema
        """
        logger = Logger()
        logger.registrar("API: Consultando estadísticas del sistema")
        
        # Estadísticas básicas
        total_pedidos = PedidoCafe.objects.count()
        
        # Estadísticas por tipo de café
        tipos_stats = {}
        for tipo in ['espresso', 'americano', 'latte']:
            count = PedidoCafe.objects.filter(tipo_base=tipo).count()
            tipos_stats[tipo] = count
        
        # Estadísticas por tamaño
        tamanios_stats = {}
        for tamanio in ['pequeño', 'mediano', 'grande']:
            count = PedidoCafe.objects.filter(tamanio=tamanio).count()
            tamanios_stats[tamanio] = count
        
        logger.registrar(f"API: Estadísticas generadas - Total pedidos: {total_pedidos}")
        
        return Response({
            "total_pedidos": total_pedidos,
            "estadisticas_por_tipo": tipos_stats,
            "estadisticas_por_tamanio": tamanios_stats,
            "total_logs": logger.contar_logs()
        })