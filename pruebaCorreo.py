import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCartBackend.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"EMAIL_HOST_PASSWORD: {settings.EMAIL_HOST_PASSWORD}")

send_mail(
    subject='Prueba de correo desde Django',
    message='Este es un correo de prueba.',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['capry1503@gmail.com'],
    fail_silently=False,
)
print("Correo enviado con éxito.")
