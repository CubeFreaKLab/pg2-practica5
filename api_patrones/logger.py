from datetime import datetime
from threading import Lock

class Logger:
    """
    Patrón Singleton para logging de operaciones del sistema.
    Garantiza que solo exista una instancia del logger en toda la aplicación.
    """
    _instancia = None
    _lock = Lock()

    def __new__(cls):
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None:
                    cls._instancia = super(Logger, cls).__new__(cls)
                    cls._instancia.logs = []
                    cls._instancia.inicializado = False
        return cls._instancia

    def __init__(self):
        if not self.inicializado:
            self.logs = []
            self.inicializado = True

    def registrar(self, mensaje):
        """Registra un mensaje con timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {mensaje}"
        self.logs.append(log_entry)

    def obtener_logs(self):
        """Retorna todos los logs registrados"""
        return self.logs

    def limpiar_logs(self):
        """Limpia todos los logs"""
        self.logs = []

    def obtener_ultimo_log(self):
        """Retorna el último log registrado"""
        return self.logs[-1] if self.logs else None

    def contar_logs(self):
        """Retorna el número total de logs"""
        return len(self.logs)