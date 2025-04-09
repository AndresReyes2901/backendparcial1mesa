from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.conf import settings
from .models import Rol, Usuario
from .serializers import RolSerializer, UsuarioSerializer
from .permissions import IsStaffOrSuperUser
from rest_framework.response import Response


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsStaffOrSuperUser]


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsStaffOrSuperUser]


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"detail": "Logout exitoso."}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "Error al cerrar sesión."}, status=status.HTTP_400_BAD_REQUEST)


class CustomPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('correo')
        if not email:
            return Response({"error": "Email es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Usuario.objects.get(correo=email)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f"http://127.0.0.1:8000/api/reset-password-confirm/{uid}/{token}/"

        send_mail(
            subject="Recuperación de contraseña",
            message=f"Para recuperar tu contraseña, haz click aquí: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.correo],
            fail_silently=False,
        )

        return Response({"detail": "Correo de recuperación enviado."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:

            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Usuario.objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)

            new_password = request.data.get("new_password")
            if not new_password:
                return Response({"error": "Debe proporcionar una nueva contraseña."},
                                status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"detail": "Contraseña actualizada exitosamente."})

        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            return Response({"error": "Link inválido."}, status=status.HTTP_400_BAD_REQUEST)
