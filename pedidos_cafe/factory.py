from pedidos_cafe.base import Espresso, Americano, Latte, CafeBase
from api_patrones.logger import Logger

class CafeFactory:
    """
    Patrón Factory para crear instancias de diferentes tipos de café.
    Encapsula la lógica de creación y permite agregar nuevos tipos fácilmente.
    """
    
    # Registro de tipos de café disponibles
    _tipos_cafe = {
        "espresso": Espresso,
        "americano": Americano,
        "latte": Latte,
    }

    @staticmethod
    def obtener_base(tipo):
        """
        Crea y retorna una instancia del tipo de café especificado.
        
        Args:
            tipo (str): Tipo de café a crear ("espresso", "americano", "latte")
            
        Returns:
            CafeBase: Instancia del tipo de café solicitado
            
        Raises:
            ValueError: Si el tipo de café no es válido
        """
        logger = Logger()
        
        # Validar tipo de café
        if tipo not in CafeFactory._tipos_cafe:
            tipos_validos = list(CafeFactory._tipos_cafe.keys())
            error_msg = f"Tipo de café '{tipo}' no válido. Tipos válidos: {tipos_validos}"
            logger.registrar(f"ERROR: {error_msg}")
            raise ValueError(error_msg)
        
        # Crear instancia del café
        clase_cafe = CafeFactory._tipos_cafe[tipo]
        cafe = clase_cafe()
        cafe.inicializar()
        
        # Registrar la creación
        logger.registrar(f"Factory: Creado café base '{tipo}' con precio ${cafe.precio_base()}")
        
        return cafe

    @staticmethod
    def obtener_tipos_disponibles():
        """Retorna una lista de todos los tipos de café disponibles"""
        return list(CafeFactory._tipos_cafe.keys())

    @staticmethod
    def registrar_tipo(nombre, clase):
        """
        Permite registrar un nuevo tipo de café dinámicamente.
        
        Args:
            nombre (str): Nombre del tipo de café
            clase (class): Clase que implementa CafeBase
        """
        if not issubclass(clase, CafeBase):
            raise TypeError("La clase debe heredar de CafeBase")
        
        CafeFactory._tipos_cafe[nombre] = clase
        Logger().registrar(f"Factory: Registrado nuevo tipo de café '{nombre}'")

# Ejemplo de uso para testing
if __name__ == "__main__":
    # Crear diferentes tipos de café
    espresso = CafeFactory.obtener_base("espresso")
    americano = CafeFactory.obtener_base("americano")
    latte = CafeFactory.obtener_base("latte")
    
    print(f"Espresso: {espresso}")
    print(f"Americano: {americano}")
    print(f"Latte: {latte}")
    
    # Ver logs
    logger = Logger()
    for log in logger.obtener_logs():
        print(log)