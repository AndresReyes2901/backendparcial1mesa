import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCartBackend.settings')
django.setup()

from orders.models import Order, OrderStatusHistory

# Lista de estados en flujo lógico
ESTADOS = ['Pendiente', 'Procesando', 'Enviado', 'Entregado']

def poblar_historial_estados():
    print("📦 Poblando historial de estados...")

    ordenes = Order.objects.all()
    total_actualizadas = 0

    for orden in ordenes:
        # Saltar si ya tiene historial
        if OrderStatusHistory.objects.filter(order=orden).exists():
            continue

        # Generar estados progresivos para cada orden
        num_cambios = random.randint(2, len(ESTADOS))  # entre 2 y 4 estados
        estados_secuencia = ESTADOS[:num_cambios]

        fecha_inicio = getattr(orden, 'created_at', timezone.now())
        previous_status = estados_secuencia[0]

        for estado in estados_secuencia[1:]:
            fecha_inicio += timedelta(hours=random.randint(6, 24))

            historial = OrderStatusHistory(
                previous_status=previous_status,
                new_status=estado,
                changed_at=fecha_inicio,
                order_id=orden.id  # FK directa
            )
            historial.save()

            previous_status = estado

        total_actualizadas += 1

    print(f"✅ Historial creado para {total_actualizadas} órdenes.")

if __name__ == '__main__':
    poblar_historial_estados()
