from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, IngresoViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'ingresos', IngresoViewSet, basename='ingreso')

urlpatterns = [
    path('', include(router.urls)),
]