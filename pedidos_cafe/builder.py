from api_patrones.logger import Logger

class CafePersonalizadoBuilder:
    """
    Patrón Builder para construir cafés personalizados paso a paso.
    Permite agregar ingredientes y ajustar el tamaño de manera fluida.
    """
    
    def __init__(self, cafe_base):
        """
        Inicializa el builder con un café base.
        
        Args:
            cafe_base (CafeBase): Instancia de café base del Factory
        """
        self.base = cafe_base
        self.precio = cafe_base.precio_base()
        self.ingredientes = list(cafe_base.obtener_ingredientes_base())
        self.tamanio_aplicado = "pequeño"  # Tamaño por defecto
        
        # Precios de ingredientes adicionales
        self.precios_ingredientes = {
            "canela": 1.0,
            "chocolate": 2.0,
            "vainilla": 1.5,
            "azucar": 0.5,
            "leche extra": 2.0,
        }
        
        # Multiplicadores por tamaño
        self.multiplicadores_tamanio = {
            "pequeño": 1.0,
            "mediano": 1.25,
            "grande": 1.5,
        }
        
        logger = Logger()
        logger.registrar(f"Builder: Iniciado con café base '{cafe_base.obtener_nombre()}'")

    def agregar_ingrediente(self, ingrediente):
        """
        Agrega un ingrediente al café.
        
        Args:
            ingrediente (str): Nombre del ingrediente a agregar
            
        Returns:
            CafePersonalizadoBuilder: Retorna self para permitir method chaining
            
        Raises:
            ValueError: Si el ingrediente no es válido
        """
        logger = Logger()
        
        if ingrediente not in self.precios_ingredientes:
            ingredientes_validos = list(self.precios_ingredientes.keys())
            error_msg = f"Ingrediente '{ingrediente}' no válido. Ingredientes válidos: {ingredientes_validos}"
            logger.registrar(f"ERROR: {error_msg}")
            raise ValueError(error_msg)
        
        self.ingredientes.append(ingrediente)
        precio_ingrediente = self.precios_ingredientes[ingrediente]
        self.precio += precio_ingrediente
        
        logger.registrar(f"Builder: Agregado ingrediente '{ingrediente}' (+${precio_ingrediente})")
        return self

    def ajustar_tamanio(self, tamanio):
        """
        Ajusta el tamaño del café y recalcula el precio.
        
        Args:
            tamanio (str): Tamaño del café ("pequeño", "mediano", "grande")
            
        Returns:
            CafePersonalizadoBuilder: Retorna self para permitir method chaining
            
        Raises:
            ValueError: Si el tamaño no es válido
        """
        logger = Logger()
        
        if tamanio not in self.multiplicadores_tamanio:
            tamanios_validos = list(self.multiplicadores_tamanio.keys())
            error_msg = f"Tamaño '{tamanio}' no válido. Tamaños válidos: {tamanios_validos}"
            logger.registrar(f"ERROR: {error_msg}")
            raise ValueError(error_msg)
        
        # Revertir el multiplicador anterior
        self.precio /= self.multiplicadores_tamanio[self.tamanio_aplicado]
        
        # Aplicar nuevo multiplicador
        self.tamanio_aplicado = tamanio
        multiplicador = self.multiplicadores_tamanio[tamanio]
        self.precio *= multiplicador
        
        logger.registrar(f"Builder: Ajustado tamaño a '{tamanio}' (multiplicador: {multiplicador})")
        return self

    def obtener_precio(self):
        """Retorna el precio total del café personalizado"""
        return round(self.precio, 2)

    def obtener_ingredientes_finales(self):
        """Retorna la lista completa de ingredientes"""
        return self.ingredientes.copy()

    def obtener_tamanio(self):
        """Retorna el tamaño actual del café"""
        return self.tamanio_aplicado

    def obtener_resumen(self):
        """Retorna un resumen completo del café personalizado"""
        return {
            "base": self.base.obtener_nombre(),
            "ingredientes": self.ingredientes,
            "tamanio": self.tamanio_aplicado,
            "precio": self.obtener_precio()
        }

    def reset(self):
        """Reinicia el builder al estado inicial"""
        self.precio = self.base.precio_base()
        self.ingredientes = list(self.base.obtener_ingredientes_base())
        self.tamanio_aplicado = "pequeño"
        
        logger = Logger()
        logger.registrar("Builder: Reiniciado al estado inicial")
        return self


class CafeDirector:
    """
    Director que conoce cómo construir diferentes tipos de cafés personalizados.
    Encapsula las recetas y procesos de construcción complejos.
    """
    
    def __init__(self, builder):
        """
        Inicializa el director con un builder.
        
        Args:
            builder (CafePersonalizadoBuilder): Builder a utilizar
        """
        self.builder = builder
        logger = Logger()
        logger.registrar("Director: Inicializado con builder")

    def construir(self, ingredientes, tamanio):
        """
        Construye un café personalizado con ingredientes y tamaño específicos.
        
        Args:
            ingredientes (list): Lista de ingredientes a agregar
            tamanio (str): Tamaño del café
        """
        logger = Logger()
        logger.registrar(f"Director: Construyendo café con ingredientes {ingredientes} y tamaño '{tamanio}'")
        
        # Agregar ingredientes uno por uno
        for ingrediente in ingredientes:
            self.builder.agregar_ingrediente(ingrediente)
        
        # Ajustar tamaño
        self.builder.ajustar_tamanio(tamanio)
        
        logger.registrar(f"Director: Construcción completada - Precio final: ${self.builder.obtener_precio()}")

    def construir_paquete_1(self):
        """Construye el paquete especial 1: Canela + Chocolate + Mediano"""
        logger = Logger()
        logger.registrar("Director: Construyendo paquete especial 1")
        
        return (self.builder
                .agregar_ingrediente("canela")
                .agregar_ingrediente("chocolate")
                .ajustar_tamanio("mediano"))

    def construir_paquete_2(self):
        """Construye el paquete especial 2: Vainilla + Azúcar + Grande"""
        logger = Logger()
        logger.registrar("Director: Construyendo paquete especial 2")
        
        return (self.builder
                .agregar_ingrediente("vainilla")
                .agregar_ingrediente("azucar")
                .ajustar_tamanio("grande"))

    def construir_paquete_3(self):
        """Construye el paquete especial 3: Leche Extra + Canela + Pequeño"""
        logger = Logger()
        logger.registrar("Director: Construyendo paquete especial 3")
        
        return (self.builder
                .agregar_ingrediente("leche extra")
                .agregar_ingrediente("canela")
                .ajustar_tamanio("pequeño"))

    def construir_cafe_premium(self):
        """Construye un café premium con todos los ingredientes"""
        logger = Logger()
        logger.registrar("Director: Construyendo café premium")
        
        return (self.builder
                .agregar_ingrediente("chocolate")
                .agregar_ingrediente("vainilla")
                .agregar_ingrediente("canela")
                .agregar_ingrediente("leche extra")
                .ajustar_tamanio("grande"))


# Ejemplo de uso para testing
if __name__ == "__main__":
    from pedidos_cafe.factory import CafeFactory
    
    # Crear café base
    cafe_base = CafeFactory.obtener_base("latte")
    
    # Crear builder y director
    builder = CafePersonalizadoBuilder(cafe_base)
    director = CafeDirector(builder)
    
    # Construir paquete especial 1
    director.construir_paquete_1()
    
    print("Resumen del café:")
    resumen = builder.obtener_resumen()
    for key, value in resumen.items():
        print(f"{key}: {value}")
    
    # Ver logs
    logger = Logger()
    print("\nLogs:")
    for log in logger.obtener_logs():
        print(log)