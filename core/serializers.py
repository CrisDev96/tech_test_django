from rest_framework import serializers
from .models import Usuario, Ingreso


class IngresoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingreso
        fields = ['id','usuario','fecha_entrada','fecha_salida','created_at','updated_at']

class UsuarioSerializer(serializers.ModelSerializer):

    ingresos = IngresoSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = ['id','email','first_name','last_name','created_at','updated_at','ingresos']

