from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Empresas(models.Model):
    Nombre_Empresa = models.CharField(max_length=100)
    Cant_Empleados = models.IntegerField()
    representante = models.CharField(max_length=100, verbose_name='Representante Legal')
    imagen = models.ImageField(upload_to='empresas/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # Nuevos campos para ciberseguridad
    nivel_seguridad = models.CharField(
        max_length=20,
        choices=[
            ('BAJO', 'Bajo'),
            ('MEDIO', 'Medio'),
            ('ALTO', 'Alto'),
        ],
        default='MEDIO'
    )
    ultimo_escaneo = models.DateTimeField(null=True, blank=True)
    estado_monitoreo = models.BooleanField(default=True)

    def __str__(self):
        return self.Nombre_Empresa

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

class Amenaza(models.Model):
    TIPOS_AMENAZA = [
        ('MALWARE', 'Malware'),
        ('PHISHING', 'Phishing'),
        ('RANSOMWARE', 'Ransomware'),
        ('DOS', 'Denegación de Servicio'),
        ('OTRO', 'Otro'),
    ]

    NIVEL_SEVERIDAD = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]

    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, related_name='amenazas')
    tipo = models.CharField(max_length=20, choices=TIPOS_AMENAZA)
    severidad = models.CharField(max_length=20, choices=NIVEL_SEVERIDAD)
    descripcion = models.TextField()
    fecha_deteccion = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    resuelta = models.BooleanField(default=False)
    detalles_tecnicos = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.empresa.Nombre_Empresa}"

    class Meta:
        verbose_name = 'Amenaza'
        verbose_name_plural = 'Amenazas'
        ordering = ['-fecha_deteccion']

class RegistroActividad(models.Model):
    TIPOS_ACTIVIDAD = [
        ('ESCANEO', 'Escaneo de Sistema'),
        ('ACTUALIZACION', 'Actualización de Seguridad'),
        ('ALERTA', 'Alerta de Seguridad'),
        ('CONFIGURACION', 'Cambio de Configuración'),
    ]

    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, related_name='actividades', null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_ACTIVIDAD)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    detalles = models.JSONField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.empresa.Nombre_Empresa}"

    class Meta:
        verbose_name = 'Registro de Actividad'
        verbose_name_plural = 'Registros de Actividad'
        ordering = ['-fecha']

class ForoCiberseguridad(models.Model):
    """Modelo para el foro de ciberseguridad donde los usuarios pueden reportar problemas"""
    
    CATEGORIAS = [
        ('MALWARE', 'Malware'),
        ('PHISHING', 'Phishing'),
        ('RANSOMWARE', 'Ransomware'),
        ('DOS', 'Denegación de Servicio'),
        ('INTRUSION', 'Intrusión'),
        ('ROBO_DATOS', 'Robo de Datos'),
        ('OTRO', 'Otro'),
    ]
    
    ESTADOS = [
        ('PENDIENTE', 'Pendiente de Análisis'),
        ('ANALIZADO', 'Analizado'),
        ('RESUELTO', 'Resuelto'),
        ('CERRADO', 'Cerrado'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Título del Problema')
    descripcion = models.TextField(verbose_name='Descripción Detallada')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='OTRO')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    
    # Información del usuario
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reportes_foro')
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, related_name='reportes_foro', null=True, blank=True)
    
    # Análisis con Stanza
    analisis_stanza = models.JSONField(null=True, blank=True, verbose_name='Análisis de Stanza')
    tipo_ataque_detectado = models.CharField(max_length=50, null=True, blank=True, verbose_name='Tipo de Ataque Detectado')
    confianza_analisis = models.FloatField(null=True, blank=True, verbose_name='Confianza del Análisis (%)')
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_analisis = models.DateTimeField(null=True, blank=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    
    # Respuestas y comentarios
    respuestas = models.ManyToManyField('RespuestaForo', blank=True, related_name='reporte_principal')
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
    
    def get_tipo_ataque_detectado_display(self):
        mapping = dict(self.CATEGORIAS)
        return mapping.get(self.tipo_ataque_detectado, self.tipo_ataque_detectado or "No determinado")
    
    class Meta:
        verbose_name = 'Reporte del Foro'
        verbose_name_plural = 'Reportes del Foro'
        ordering = ['-fecha_creacion']

class RespuestaForo(models.Model):
    """Modelo para las respuestas en el foro"""
    
    reporte = models.ForeignKey(ForoCiberseguridad, on_delete=models.CASCADE, related_name='respuestas_detalle')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    es_solucion = models.BooleanField(default=False, verbose_name='¿Es una solución?')
    
    def __str__(self):
        return f"Respuesta de {self.usuario.username} en {self.reporte.titulo}"
    
    class Meta:
        verbose_name = 'Respuesta del Foro'
        verbose_name_plural = 'Respuestas del Foro'
        ordering = ['fecha_creacion']
