from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Vistas principales
    path('', views.home, name='home'),
    path('landing/', views.landing, name='landing'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Escaneo de archivos
    path('escanear/', views.escanear_archivo, name='escanear_archivo'),
    path('estado-escaneo/', views.obtener_estado_escaneo, name='estado_escaneo'),
    
    # Dashboard y reportes
    path('dashboard/', views.dashboard_seguridad, name='dashboard_seguridad'),
    path('actividad/', views.registro_actividad, name='registro_actividad'),
    
    # Gestión de empresas
    path('empresas/', views.lista_empresas, name='lista_empresas'),
    path('empresas/crear/', views.crear_empresa, name='crear_empresa'),
    path('empresas/<int:pk>/', views.detalle_empresa, name='detalle_empresa'),
    path('empresas/<int:pk>/editar/', views.editar_empresa, name='editar_empresa'),
    path('empresas/<int:pk>/eliminar/', views.eliminar_empresa, name='eliminar_empresa'),
    path('crud/', views.crud_empresas, name='crud_empresas'),
    
    # Foro de Ciberseguridad
    path('foro/', views.foro_ciberseguridad, name='foro_ciberseguridad'),
    path('foro/crear/', views.crear_reporte_foro, name='crear_reporte_foro'),
    path('foro/<int:pk>/', views.detalle_reporte_foro, name='detalle_reporte_foro'),
    path('foro/<int:pk>/reanalizar/', views.reanalizar_reporte, name='reanalizar_reporte'),
    path('foro/mis-reportes/', views.mis_reportes_foro, name='mis_reportes_foro'),
    path('foro/analizar-pendientes/', views.analizar_reportes_pendientes, name='analizar_reportes_pendientes'),
    
    # Análisis con Stanza
    path('analisis-texto/', views.analisis_texto_stanza, name='analisis_texto_stanza'),
    
    # Documentación
    path('manual/', views.manual_usuario, name='manual_usuario'),
] 