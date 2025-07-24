from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Usuario, Ingreso
from .serializers import UsuarioSerializer, IngresoSerializer


# Create your views here.
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        if Usuario.objects.filter(email=email).exists():
            return Response({"error": "El email ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "message": "Usuario creado con éxito.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        usuario = self.get_object()
        serializer = self.get_serializer(usuario, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "message": "Usuario actualizado con éxito.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        usuario = self.get_object()
        usuario.delete()

        return Response({
            "message": "Usuario y sus ingresos eliminados con éxito."
        }, status=status.HTTP_204_NO_CONTENT)

class IngresoViewSet(viewsets.ModelViewSet):
    queryset = Ingreso.objects.all()
    serializer_class = IngresoSerializer

    def create(self, request, *args, **kwargs):
        usuario_id = request.data.get("usuario")

        if not usuario_id:
            return Response({'error': 'Debe enviar el ID del usuario.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(pk=usuario_id)
        except Usuario.DoesNotExist:
            return Response({'error': 'El usuario especificado no existe.'}, status=status.HTTP_400_BAD_REQUEST)

        ahora = timezone.now()
        salida = ahora + timedelta(hours=5)

        ingreso = Ingreso.objects.create(
            usuario=usuario,
            fecha_entrada=ahora,
            fecha_salida=salida
        )

        serializer = self.get_serializer(ingreso)
        return Response({
            'message': 'Ingreso registrado con éxito.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)