from django.contrib.auth import get_user_model
import os

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")

if not User.objects.filter(nombre=username,apelllido=username).exists():
    User.objects.create_superuser(nombre=username,apelllido=username, correo=email, password=password)
    print("✅ Superuser creado")
else:
    print("ℹ️ El superuser ya existe")
