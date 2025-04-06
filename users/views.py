from rest_framework import viewsets
from .models import Rol, Usuario
from .serializers import RolSerializer, UsuarioSerializer
from .permissions import IsSuperUser, IsStaffOrSuperUser

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsStaffOrSuperUser]

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsStaffOrSuperUser]
