"""
URL configuration for api_patrones project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    """Vista raíz de la API que muestra los endpoints disponibles"""
    return JsonResponse({
        "mensaje": "API de Patrones de Diseño - Pedidos de Café",
        "endpoints": {
            "admin": "/admin/",
            "pedidos": "/api/pedidos/",
            "tipos_cafe": "/api/pedidos/tipos_cafe/",
            "ingredientes": "/api/pedidos/ingredientes_disponibles/",
            "tamanios": "/api/pedidos/tamanios_disponibles/",
            "logs": "/api/pedidos/logs_sistema/",
            "estadisticas": "/api/pedidos/estadisticas/"
        },
        "patrones_implementados": [
            "Factory Pattern",
            "Builder Pattern", 
            "Singleton Pattern"
        ]
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api_root'),
    path('', include('pedidos_cafe.urls')),
]