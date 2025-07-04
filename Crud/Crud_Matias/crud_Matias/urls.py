from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.lista_empleado, name='lista_empleados'),  # <- usa este nombre
    path('crear/', views.crear_empleado, name='crear_empleado'),
    path('editar/<int:id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('eliminar/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),
]
