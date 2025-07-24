import os
import django
import random
from faker import Faker

# Configurar Django para usar settings correctamente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCartBackend.settings')
django.setup()

from users.models import Usuario
from products.models import Product

fake = Faker()

def create_users(n=10):
    print("Creando usuarios...")
    for _ in range(n):
        correo = fake.unique.email()
        nombre = fake.first_name()
        apellido = fake.last_name()
        password = '123456'
        if not Usuario.objects.filter(correo=correo).exists():
            user = Usuario.objects.create_user(correo=correo, nombre=nombre, apellido=apellido, password=password)
            user.save()
    print(f"Usuarios creados: {n}")

def create_products():
    print("Creando productos tecnológicos...")
    product_list = [
        {"name": "Teclado mecánico", "description": "Teclado mecánico RGB para gaming", "price": 75.99, "stock": 50},
        {"name": "Mouse inalámbrico", "description": "Mouse inalámbrico ergonómico", "price": 40.50, "stock": 80},
        {"name": "Monitor 24 pulgadas", "description": "Monitor LED 1080p", "price": 150.00, "stock": 30},
        {"name": "Cable HDMI 2 metros", "description": "Cable HDMI para conexión de alta definición", "price": 10.99, "stock": 200},
        {"name": "Audífonos Bluetooth", "description": "Audífonos inalámbricos con cancelación de ruido", "price": 120.00, "stock": 45},
        {"name": "Teléfono inteligente", "description": "Smartphone con cámara de 12MP", "price": 399.99, "stock": 25},
        {"name": "Radio portátil", "description": "Radio portátil con batería recargable", "price": 35.00, "stock": 60},
        {"name": "Mouse pad gaming", "description": "Mouse pad extra grande para gaming", "price": 15.00, "stock": 100},
        {"name": "Webcam HD", "description": "Cámara web para videoconferencias", "price": 55.00, "stock": 40},
        {"name": "Base para laptop", "description": "Base refrigerante para laptops de hasta 17 pulgadas", "price": 30.00, "stock": 35},
    ]

    for p in product_list:
        # Si ya existe producto con ese nombre, no lo crea
        if not Product.objects.filter(name=p['name']).exists():
            product = Product(
                name=p['name'],
                description=p['description'],
                price=p['price'],
                stock=p['stock'],
                is_active=True
            )
            product.save()
    print(f"Productos creados: {len(product_list)}")

if __name__ == '__main__':
    create_users(10)
    create_products()
    print("✔ Población completada.")
