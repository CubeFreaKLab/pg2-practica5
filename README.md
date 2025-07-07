# PG2: PRÁCTICA 5

## PATRONES DE DISEÑO EN UN API REST CON DJANGO Y DRF

### Descripción

Este proyecto implementa una API REST para gestionar pedidos de café utilizando **Django** y **Django REST Framework (DRF)**. La aplicación demuestra el uso de tres patrones de diseño fundamentales: **Factory**, **Builder** y **Singleton**.

## Instalación y Configuración

### Requisitos
- Python 3.8+
- Django 5.2.3
- Django REST Framework 3.16.0

### Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/CubeFreaKLab/pg2-practica5.git
   cd pg2-practica5
   ```

2. Crea un entorno virtual:
   ```bash
    python -m venv env
    .\env\Scripts\activate # En Windows
    source env/bin/activate  # En Linux
    ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta las migraciones:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Crea un superusuario:
   ```bash
   python manage.py createsuperuser
   ```

6. Ejecuta el servidor:
   ```bash
   python manage.py runserver
   ```

## Patrones de Diseño Implementados

### 1. Patrón Factory (Fábrica)

**¿Qué patrón se utilizó y por qué?**
- Se implementó el patrón Factory para crear instancias de diferentes tipos de café base (Espresso, Americano, Latte).
- Este patrón permite encapsular la lógica de creación y facilita la adición de nuevos tipos de café sin modificar el código cliente.

**¿Dónde está implementado en el código?**
- **Archivo**: `pedidos_cafe/factory.py`
- **Clase**: `CafeFactory`
- **Clases base**: `pedidos_cafe/base.py` (CafeBase, Espresso, Americano, Latte)
- **Método principal**: `CafeFactory.obtener_base(tipo)`

**¿Cómo se prueba o evidencia su uso?**
- Endpoint: `GET /api/pedidos/tipos_cafe/`
- En el serializador: `PedidoCafeSerializer.get_precio_total()`
- Ejemplo de uso:
  ```python
  cafe_base = CafeFactory.obtener_base("espresso")
  ```

### 2. Patrón Builder (Constructor)

**¿Qué patrón se utilizó y por qué?**
- Se implementó el patrón Builder para construir cafés personalizados paso a paso.
- Permite agregar ingredientes y ajustar el tamaño de manera fluida usando method chaining.
- Incluye un Director que conoce las recetas complejas.

**¿Dónde está implementado en el código?**
- **Archivo**: `pedidos_cafe/builder.py`
- **Clases**: `CafePersonalizadoBuilder` y `CafeDirector`
- **Métodos principales**: 
  - `agregar_ingrediente()`
  - `ajustar_tamanio()`
  - `construir()`

**¿Cómo se prueba o evidencia su uso?**
- En el serializador: `PedidoCafeSerializer.get_precio_total()` y `get_ingredientes_finales()`
- Endpoint: `GET /api/pedidos/{id}/calcular_precio/`
- Ejemplo de uso:
  ```python
  builder = CafePersonalizadoBuilder(cafe_base)
  director = CafeDirector(builder)
  director.construir(["canela", "chocolate"], "mediano")
  ```

### 3. Patrón Singleton

**¿Qué patrón se utilizó y por qué?**
- Se implementó el patrón Singleton para mantener un sistema de logging único en toda la aplicación.
- Garantiza que solo exista una instancia del logger y que todos los logs se centralicen.

**¿Dónde está implementado en el código?**
- **Archivo**: `api_patrones/logger.py`
- **Clase**: `Logger`
- **Implementación**: Thread-safe con locks para evitar problemas de concurrencia

**¿Cómo se prueba o evidencia su uso?**
- Endpoint: `GET /api/pedidos/logs_sistema/`
- Endpoint: `POST /api/pedidos/limpiar_logs/`
- Se usa en todo el sistema para registrar operaciones
- Ejemplo de uso:
  ```python
  logger = Logger()
  logger.registrar("Mensaje de log")
  ```

## Endpoints de la API

### Pedidos CRUD
- `GET /api/pedidos/` - Lista todos los pedidos
- `POST /api/pedidos/` - Crea un nuevo pedido
- `GET /api/pedidos/{id}/` - Obtiene un pedido específico
- `PUT /api/pedidos/{id}/` - Actualiza un pedido específico
- `DELETE /api/pedidos/{id}/` - Elimina un pedido específico

### Endpoints Adicionales
- `GET /api/pedidos/tipos_cafe/` - Lista tipos de café disponibles (Factory)
- `GET /api/pedidos/ingredientes_disponibles/` - Lista ingredientes disponibles (Builder)
- `GET /api/pedidos/tamanios_disponibles/` - Lista tamaños disponibles (Builder)
- `GET /api/pedidos/{id}/calcular_precio/` - Recalcula precio de un pedido (Factory + Builder)
- `GET /api/pedidos/logs_sistema/` - Obtiene logs del sistema (Singleton)
- `POST /api/pedidos/limpiar_logs/` - Limpia los logs del sistema (Singleton)
- `GET /api/pedidos/estadisticas/` - Obtiene estadísticas generales

## Ejemplo de Uso

### Crear un pedido
```bash
curl -X POST http://localhost:8000/api/pedidos/ \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": "Juan Pérez",
    "tipo_base": "latte",
    "ingredientes": ["canela", "chocolate"],
    "tamanio": "mediano"
  }'
```

### Respuesta esperada
```json
{
  "id": 1,
  "cliente": "Juan Pérez",
  "tipo_base": "latte",
  "ingredientes": ["canela", "chocolate"],
  "tamanio": "mediano",
  "fecha": "2025-07-07T15:30:00Z",
  "precio_total": 23.12,
  "ingredientes_finales": ["café concentrado", "leche vaporizada", "espuma", "canela", "chocolate"],
  "resumen_construccion": {
    "base": "Latte",
    "ingredientes": ["café concentrado", "leche vaporizada", "espuma", "canela", "chocolate"],
    "tamanio": "mediano",
    "precio": 23.12,
    "precio_base": 15.0,
    "ingredientes_agregados": ["canela", "chocolate"],
    "fecha_pedido": "2025-07-07T15:30:00Z",
    "cliente": "Juan Pérez"
  }
}
```


## Validaciones Implementadas

- **Ingredientes válidos**: canela, chocolate, vainilla, azucar, leche extra
- **Tipos de café válidos**: espresso, americano, latte
- **Tamaños válidos**: pequeño, mediano, grande
- **Validación a nivel de modelo y serializer**

## Características Adicionales

- **Admin personalizado** con filtros y visualización optimizada
- **Logging completo** de todas las operaciones
- **Cálculos dinámicos** de precios e ingredientes
- **Estadísticas** del sistema
- **Documentación** completa de la API
- **Manejo de errores** robusto
- **Thread-safe** Singleton implementation

## Licencia de Publicación

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo LICENSE para más detalles.