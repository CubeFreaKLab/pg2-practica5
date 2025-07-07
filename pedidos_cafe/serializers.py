from rest_framework import serializers
from pedidos_cafe.models import PedidoCafe
from pedidos_cafe.factory import CafeFactory
from pedidos_cafe.builder import CafePersonalizadoBuilder, CafeDirector
from api_patrones.logger import Logger

class PedidoCafeSerializer(serializers.ModelSerializer):
    """
    Serializer para PedidoCafe que calcula atributos dinámicos usando patrones de diseño.
    """
    precio_total = serializers.SerializerMethodField()
    ingredientes_finales = serializers.SerializerMethodField()
    resumen_construccion = serializers.SerializerMethodField()

    class Meta:
        model = PedidoCafe
        fields = [
            "id",
            "cliente",
            "tipo_base",
            "ingredientes",
            "tamanio",
            "fecha",
            "precio_total",
            "ingredientes_finales",
            "resumen_construccion",
        ]

    def get_precio_total(self, obj):
        """
        Calcula el precio total del pedido usando los patrones Factory y Builder.
        
        Args:
            obj (PedidoCafe): Instancia del modelo PedidoCafe
            
        Returns:
            float: Precio total calculado
        """
        try:
            # Patrón Factory: Crear el café base
            cafe_base = CafeFactory.obtener_base(obj.tipo_base)
            
            # Patrón Builder: Construir el café personalizado
            builder = CafePersonalizadoBuilder(cafe_base)
            director = CafeDirector(builder)
            
            # Construir con los ingredientes y tamaño del pedido
            director.construir(obj.ingredientes, obj.tamanio)
            
            precio_final = builder.obtener_precio()
            
            # Patrón Singleton: Registrar la operación
            logger = Logger()
            logger.registrar(
                f"Serializer: Calculado precio total ${precio_final} para pedido {obj.id} "
                f"(Cliente: {obj.cliente}, Tipo: {obj.tipo_base}, Tamaño: {obj.tamanio})"
            )
            
            return precio_final
            
        except Exception as e:
            logger = Logger()
            logger.registrar(f"ERROR en cálculo de precio para pedido {obj.id}: {str(e)}")
            return 0.0

    def get_ingredientes_finales(self, obj):
        """
        Obtiene la lista completa de ingredientes finales del pedido.
        
        Args:
            obj (PedidoCafe): Instancia del modelo PedidoCafe
            
        Returns:
            list: Lista de ingredientes finales
        """
        try:
            # Patrón Factory: Crear el café base
            cafe_base = CafeFactory.obtener_base(obj.tipo_base)
            
            # Patrón Builder: Construir el café personalizado
            builder = CafePersonalizadoBuilder(cafe_base)
            director = CafeDirector(builder)
            
            # Construir con los ingredientes y tamaño del pedido
            director.construir(obj.ingredientes, obj.tamanio)
            
            ingredientes_finales = builder.obtener_ingredientes_finales()
            
            # Patrón Singleton: Registrar la operación
            logger = Logger()
            logger.registrar(
                f"Serializer: Obtenidos ingredientes finales para pedido {obj.id}: "
                f"{ingredientes_finales}"
            )
            
            return ingredientes_finales
            
        except Exception as e:
            logger = Logger()
            logger.registrar(f"ERROR en obtención de ingredientes para pedido {obj.id}: {str(e)}")
            return []

    def get_resumen_construccion(self, obj):
        """
        Obtiene un resumen completo de la construcción del café.
        
        Args:
            obj (PedidoCafe): Instancia del modelo PedidoCafe
            
        Returns:
            dict: Resumen de la construcción
        """
        try:
            # Patrón Factory: Crear el café base
            cafe_base = CafeFactory.obtener_base(obj.tipo_base)
            
            # Patrón Builder: Construir el café personalizado
            builder = CafePersonalizadoBuilder(cafe_base)
            director = CafeDirector(builder)
            
            # Construir con los ingredientes y tamaño del pedido
            director.construir(obj.ingredientes, obj.tamanio)
            
            resumen = builder.obtener_resumen()
            
            # Agregar información adicional
            resumen.update({
                "precio_base": cafe_base.precio_base(),
                "ingredientes_agregados": obj.ingredientes,
                "fecha_pedido": obj.fecha,
                "cliente": obj.cliente,
            })
            
            # Patrón Singleton: Registrar la operación
            logger = Logger()
            logger.registrar(f"Serializer: Generado resumen para pedido {obj.id}")
            
            return resumen
            
        except Exception as e:
            logger = Logger()
            logger.registrar(f"ERROR en generación de resumen para pedido {obj.id}: {str(e)}")
            return {}

    def validate_ingredientes(self, value):
        """
        Valida que los ingredientes enviados sean válidos.
        
        Args:
            value (list): Lista de ingredientes a validar
            
        Returns:
            list: Lista de ingredientes validados
            
        Raises:
            serializers.ValidationError: Si algún ingrediente no es válido
        """
        ingredientes_validos = ["canela", "chocolate", "vainilla", "azucar", "leche extra"]
        
        for ingrediente in value:
            if ingrediente not in ingredientes_validos:
                raise serializers.ValidationError(
                    f"El ingrediente '{ingrediente}' no es válido. "
                    f"Ingredientes válidos: {', '.join(ingredientes_validos)}"
                )
        
        return value

    def validate_tipo_base(self, value):
        """
        Valida que el tipo de café base sea válido.
        
        Args:
            value (str): Tipo de café base a validar
            
        Returns:
            str: Tipo de café validado
            
        Raises:
            serializers.ValidationError: Si el tipo no es válido
        """
        tipos_validos = CafeFactory.obtener_tipos_disponibles()
        
        if value not in tipos_validos:
            raise serializers.ValidationError(
                f"El tipo de café '{value}' no es válido. "
                f"Tipos válidos: {', '.join(tipos_validos)}"
            )
        
        return value

    def create(self, validated_data):
        """
        Crea un nuevo pedido y registra la operación.
        
        Args:
            validated_data (dict): Datos validados
            
        Returns:
            PedidoCafe: Instancia creada
        """
        pedido = super().create(validated_data)
        
        # Registrar la creación
        logger = Logger()
        logger.registrar(
            f"Serializer: Creado nuevo pedido {pedido.id} para cliente {pedido.cliente}"
        )
        
        return pedido

    def update(self, instance, validated_data):
        """
        Actualiza un pedido existente y registra la operación.
        
        Args:
            instance (PedidoCafe): Instancia a actualizar
            validated_data (dict): Datos validados
            
        Returns:
            PedidoCafe: Instancia actualizada
        """
        pedido = super().update(instance, validated_data)
        
        # Registrar la actualización
        logger = Logger()
        logger.registrar(
            f"Serializer: Actualizado pedido {pedido.id} para cliente {pe