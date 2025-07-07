from django.db import models
from django.core.exceptions import ValidationError

class PedidoCafe(models.Model):
    cliente = models.CharField(max_length=100)
    tipo_base = models.CharField(
        max_length=20,
        choices=[
            ("espresso", "Espresso"),
            ("americano", "Americano"),
            ("latte", "Latte"),
        ],
    )
    ingredientes = models.JSONField(default=list)
    tamanio = models.CharField(
        max_length=10,
        choices=[
            ("pequeño", "Pequeño"),
            ("mediano", "Mediano"),
            ("grande", "Grande"),
        ],
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Validación de ingredientes permitidos"""
        ingredientes_validos = [
            "canela", "chocolate", "vainilla", "azucar", "leche extra"
        ]
        
        if self.ingredientes:
            for ingrediente in self.ingredientes:
                if ingrediente not in ingredientes_validos:
                    raise ValidationError(
                        f"El ingrediente '{ingrediente}' no está permitido. "
                        f"Ingredientes válidos: {', '.join(ingredientes_validos)}"
                    )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido de {self.cliente} - {self.tipo_base} {self.tamanio}"

    class Meta:
        verbose_name = "Pedido de Café"
        verbose_name_plural = "Pedidos de Café"