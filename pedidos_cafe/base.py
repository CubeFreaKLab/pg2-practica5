class CafeBase:
    """
    Clase base abstracta para todos los tipos de café.
    Define la interfaz común que deben implementar todos los tipos de café.
    """
    def __init__(self):
        self.ingredientes = []
        self.precio = 0
        self.nombre = ""

    def inicializar(self):
        """
        Define los ingredientes y el precio base.
        Debe ser implementado por las subclases.
        """
        raise NotImplementedError("Debe implementar el método inicializar")

    def obtener_ingredientes_base(self):
        """Retorna los ingredientes base del café"""
        return self.ingredientes.copy()

    def precio_base(self):
        """Retorna el precio base del café"""
        return self.precio

    def obtener_nombre(self):
        """Retorna el nombre del tipo de café"""
        return self.nombre

    def __str__(self):
        return f"{self.nombre} - Precio base: ${self.precio}"


class Espresso(CafeBase):
    """Implementación concreta para café Espresso"""
    
    def inicializar(self):
        self.nombre = "Espresso"
        self.ingredientes = ["café concentrado"]
        self.precio = 10.0


class Americano(CafeBase):
    """Implementación concreta para café Americano"""
    
    def inicializar(self):
        self.nombre = "Americano"
        self.ingredientes = ["café filtrado", "agua caliente"]
        self.precio = 12.0


class Latte(CafeBase):
    """Implementación concreta para café Latte"""
    
    def inicializar(self):
        self.nombre = "Latte"
        self.ingredientes = ["café concentrado", "leche vaporizada", "espuma"]
        self.precio = 15.0