import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCartBackend.settings')
django.setup()

from products.models import Product

# Lista con 50 nombres de productos tecnológicos
nombres_tecnologia = [
    "Laptop Dell Inspiron",
    "Monitor LED 24 pulgadas",
    "Teclado mecánico RGB",
    "Mouse inalámbrico Logitech",
    "Auriculares Bluetooth Sony",
    "Smartphone Samsung Galaxy",
    "Tablet Apple iPad",
    "Cable HDMI 2 metros",
    "Disco duro externo 1TB",
    "Cámara web HD",
    "Altavoz Bluetooth JBL",
    "Router WiFi AC1200",
    "Smart TV 55 pulgadas",
    "Impresora multifuncional",
    "Memoria USB 64GB",
    "Base enfriadora para laptop",
    "Micrófono USB",
    "Cargador portátil 10000mAh",
    "Soporte para monitor",
    "Teclado inalámbrico",
    "Smartwatch Fitbit",
    "Adaptador USB-C a HDMI",
    "Cable de carga rápido",
    "Batería externa para celular",
    "Mouse gamer RGB",
    "Pantalla LED 32 pulgadas",
    "Altavoces para PC",
    "Teléfono fijo inalámbrico",
    "Silla gamer ergonómica",
    "Tarjeta gráfica NVIDIA",
    "Procesador Intel Core i7",
    "Placa base ASUS",
    "Memoria RAM 16GB DDR4",
    "Fuente de poder 600W",
    "Disco SSD 512GB",
    "Hub USB 4 puertos",
    "Cámara deportiva GoPro",
    "Micrófono para podcast",
    "Lentes de realidad virtual",
    "Monitor curvo 27 pulgadas",
    "Smartphone Xiaomi Redmi",
    "Cámara IP de seguridad",
    "Cargador inalámbrico",
    "Auriculares con cancelación de ruido",
    "Cable Ethernet CAT6",
    "Soporte para laptop ajustable",
    "Alfombrilla para mouse grande",
    "Teclado numérico USB",
    "Bocinas portátiles",
    "Controlador para videojuegos",
    "Laptop MacBook Pro"
]

# Obtén los primeros 50 productos (ordenados por id)
productos = Product.objects.all().order_by('id')[:50]

for producto, nuevo_nombre in zip(productos, nombres_tecnologia):
    producto.name = nuevo_nombre
    producto.save()
    print(f"Cambiado producto ID {producto.id} a '{nuevo_nombre}'")

print("Actualización de nombres completada.")
