from django.contrib import admin
from .models import Empresas, Amenaza, RegistroActividad, ForoCiberseguridad, RespuestaForo

@admin.register(Empresas)
class EmpresasAdmin(admin.ModelAdmin):
    list_display = ('Nombre_Empresa', 'Cant_Empleados', 'representante', 'nivel_seguridad', 'estado_monitoreo', 'fecha_creacion', 'usuario')
    list_filter = ('nivel_seguridad', 'estado_monitoreo', 'fecha_creacion')
    search_fields = ('Nombre_Empresa', 'representante', 'usuario__username')
    readonly_fields = ('fecha_creacion',)
    ordering = ('-fecha_creacion',)

@admin.register(Amenaza)
class AmenazaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'severidad', 'empresa', 'fecha_deteccion', 'resuelta')
    list_filter = ('tipo', 'severidad', 'resuelta', 'fecha_deteccion')
    search_fields = ('descripcion', 'empresa__Nombre_Empresa')
    readonly_fields = ('fecha_deteccion',)
    ordering = ('-fecha_deteccion',)

@admin.register(RegistroActividad)
class RegistroActividadAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'empresa', 'usuario', 'fecha')
    list_filter = ('tipo', 'fecha', 'empresa')
    search_fields = ('descripcion', 'empresa__Nombre_Empresa', 'usuario__username')
    readonly_fields = ('fecha',)
    ordering = ('-fecha',)

@admin.register(ForoCiberseguridad)
class ForoCiberseguridadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'estado', 'usuario', 'tipo_ataque_detectado', 'confianza_analisis', 'fecha_creacion')
    list_filter = ('categoria', 'estado', 'tipo_ataque_detectado', 'fecha_creacion', 'fecha_analisis')
    search_fields = ('titulo', 'descripcion', 'usuario__username', 'empresa__Nombre_Empresa')
    readonly_fields = ('fecha_creacion', 'fecha_analisis', 'fecha_resolucion')
    ordering = ('-fecha_creacion',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'categoria', 'estado')
        }),
        ('Usuario y Empresa', {
            'fields': ('usuario', 'empresa')
        }),
        ('Análisis con IA', {
            'fields': ('analisis_stanza', 'tipo_ataque_detectado', 'confianza_analisis'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_analisis', 'fecha_resolucion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usuario', 'empresa')

@admin.register(RespuestaForo)
class RespuestaForoAdmin(admin.ModelAdmin):
    list_display = ('reporte', 'usuario', 'es_solucion', 'fecha_creacion')
    list_filter = ('es_solucion', 'fecha_creacion')
    search_fields = ('contenido', 'reporte__titulo', 'usuario__username')
    readonly_fields = ('fecha_creacion',)
    ordering = ('-fecha_creacion',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('reporte', 'usuario')
