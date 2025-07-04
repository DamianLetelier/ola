from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from .models import Empresas, Amenaza, RegistroActividad, ForoCiberseguridad, RespuestaForo
from .forms import UserRegisterForm, EmpresasForm, EmpresaForm, ForoCiberseguridadForm, RespuestaForoForm, AnalisisTextoForm
from .services import servicio_escaneo, servicio_analisis_stanza
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging
import time

logger = logging.getLogger(__name__)

def landing(request):
    """Vista para la landing page."""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')

# Actualizar la configuración de login
settings.LOGIN_REDIRECT_URL = 'home'
settings.LOGIN_URL = 'login'

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def home(request):
    """Vista principal que muestra amenazas y actividades recientes."""
    if request.user.is_authenticated:
        empresas = Empresas.objects.filter(usuario=request.user)
        if not empresas.exists():
            # Mostrar página vacía o mensaje, pero no redirigir ni mostrar error
            context = {
                'empresa': None,
                'amenazas': [],
                'actividades': [],
            }
            return render(request, 'home.html', context)
        # Unir datos de todas las empresas
        amenazas = Amenaza.objects.filter(empresa__in=empresas).order_by('-fecha_deteccion')[:10]
        actividades = RegistroActividad.objects.filter(empresa__in=empresas).order_by('-fecha')[:10]
        paginator_amenazas = Paginator(amenazas, 5)
        page_number_amenazas = request.GET.get('page_amenazas')
        page_obj_amenazas = paginator_amenazas.get_page(page_number_amenazas)
        paginator_actividades = Paginator(actividades, 5)
        page_number_actividades = request.GET.get('page_actividades')
        page_obj_actividades = paginator_actividades.get_page(page_number_actividades)
        context = {
            'empresa': empresas.first(),
            'amenazas': page_obj_amenazas,
            'actividades': page_obj_actividades,
        }
        return render(request, 'home.html', context)
    else:
        return redirect('login')

@login_required
def crear_empresa(request):
    """Crea una nueva empresa."""
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.usuario = request.user
            empresa.save()
            messages.success(request, 'Empresa creada exitosamente.')
            return redirect('lista_empresas')
    else:
        form = EmpresaForm()
    
    return render(request, 'empresas/crear_empresa.html', {'form': form})

@login_required
def editar_empresa(request, pk):
    """Edita una empresa existente."""
    empresa = get_object_or_404(Empresas, pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa actualizada exitosamente.')
            return redirect('detalle_empresa', pk=empresa.pk)
    else:
        form = EmpresaForm(instance=empresa)
    
    return render(request, 'empresas/editar_empresa.html', {'form': form, 'empresa': empresa})

@login_required
def eliminar_empresa(request, pk):
    """Elimina una empresa."""
    empresa = get_object_or_404(Empresas, pk=pk)
    if request.method == 'POST':
        empresa.delete()
        messages.success(request, 'Empresa eliminada exitosamente.')
        return redirect('lista_empresas')
    
    return render(request, 'empresas/eliminar_empresa.html', {'empresa': empresa})

@login_required
def detalle_empresa(request, pk):
    """Muestra los detalles de una empresa."""
    empresa = get_object_or_404(Empresas, pk=pk)
    return render(request, 'empresas/detalle_empresa.html', {'empresa': empresa})

@login_required
def escanear_archivo(request):
    """Vista para escanear un archivo específico."""
    if request.method == 'POST':
        if 'archivo' not in request.FILES:
            messages.error(request, 'Por favor seleccione un archivo para escanear.')
            return redirect('escanear_archivo')
        archivo = request.FILES['archivo']
        # Realizar el escaneo sin asociar a empresa
        resultado = servicio_escaneo.escanear_archivo(archivo, None, usuario=request.user)
        if 'error' in resultado:
            messages.error(request, resultado['error'])
        else:
            if resultado['es_malware']:
                messages.warning(request, f"¡ALERTA! El archivo '{resultado['archivo']}' ha sido detectado como malicioso.")
            else:
                messages.success(request, f"El archivo '{resultado['archivo']}' es seguro.")
        return redirect('escanear_archivo')
    # Mostrar historial de escaneos del usuario
    actividades = RegistroActividad.objects.filter(usuario=request.user).order_by('-fecha')[:20]
    return render(request, 'escanear_archivo.html', {'actividades': actividades})

@login_required
def obtener_estado_escaneo(request):
    """Obtiene el estado actual del escaneo."""
    estado = servicio_escaneo.obtener_estado_escaneo()
    return JsonResponse(estado)

@login_required
def dashboard_seguridad(request):
    """Dashboard de seguridad con estadísticas a nivel de usuario."""
    if request.user.is_authenticated:
        empresas = Empresas.objects.filter(usuario=request.user)
        amenazas = Amenaza.objects.filter(empresa__in=empresas)
        total_amenazas = amenazas.count()
        amenazas_altas = amenazas.filter(severidad='ALTA').count()
        amenazas_medias = amenazas.filter(severidad='MEDIA').count()
        amenazas_bajas = amenazas.filter(severidad='BAJA').count()
        actividades_recientes = RegistroActividad.objects.filter(usuario=request.user).order_by('-fecha')[:10]
        context = {
            'empresa': None,
            'total_amenazas': total_amenazas,
            'amenazas_altas': amenazas_altas,
            'amenazas_medias': amenazas_medias,
            'amenazas_bajas': amenazas_bajas,
            'actividades_recientes': actividades_recientes,
        }
        return render(request, 'dashboard_seguridad.html', context)
    else:
        return redirect('login')

@login_required
def lista_empresas(request):
    """Lista todas las empresas."""
    empresas = Empresas.objects.all()
    return render(request, 'empresas/lista_empresas.html', {'empresas': empresas})

@login_required
def registro_actividad(request):
    """Muestra el registro de actividades a nivel de usuario."""
    actividades = RegistroActividad.objects.filter(usuario=request.user).order_by('-fecha')
    paginator = Paginator(actividades, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'registro_actividad.html', {
        'actividades': page_obj,
        'empresa': None
    })

def login_view(request):
    """Vista de login."""
    from django import forms
    class LoginForm(forms.Form):
        username = forms.CharField(label='Usuario', max_length=150)
        password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor, complete todos los campos.')
    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    """Vista de registro."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente. Por favor inicie sesión.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    """Vista de logout."""
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente.')
    return redirect('login')

def manual_usuario(request):
    """Manual del usuario."""
    return render(request, 'manual_usuario.html')

# ===== VISTAS PARA EL FORO DE CIBERSEGURIDAD =====

@login_required
def foro_ciberseguridad(request):
    """Vista principal del foro de ciberseguridad."""
    # Obtener todos los reportes con paginación
    reportes = ForoCiberseguridad.objects.all().order_by('-fecha_creacion')
    
    # Filtros
    categoria = request.GET.get('categoria')
    estado = request.GET.get('estado')
    
    if categoria:
        reportes = reportes.filter(categoria=categoria)
    if estado:
        reportes = reportes.filter(estado=estado)
    
    # Paginación
    paginator = Paginator(reportes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estadísticas del foro
    total_reportes = ForoCiberseguridad.objects.count()
    reportes_pendientes = ForoCiberseguridad.objects.filter(estado='PENDIENTE').count()
    reportes_analizados = ForoCiberseguridad.objects.filter(estado='ANALIZADO').count()
    
    context = {
        'reportes': page_obj,
        'total_reportes': total_reportes,
        'reportes_pendientes': reportes_pendientes,
        'reportes_analizados': reportes_analizados,
        'categorias': ForoCiberseguridad.CATEGORIAS,
        'estados': ForoCiberseguridad.ESTADOS,
        'categoria_actual': categoria,
        'estado_actual': estado,
    }
    
    return render(request, 'foro/foro_ciberseguridad.html', context)

@login_required
def crear_reporte_foro(request):
    """Vista para crear un nuevo reporte en el foro."""
    if request.method == 'POST':
        form = ForoCiberseguridadForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = request.user
            # Asignar empresa si existe
            try:
                empresa = Empresas.objects.filter(usuario=request.user).first()
                reporte.empresa = empresa
            except Empresas.DoesNotExist:
                pass  # No es obligatorio tener empresa
            reporte.save()
            # Registrar actividad
            RegistroActividad.objects.create(
                empresa=reporte.empresa if reporte.empresa else None,
                tipo='ALERTA',
                descripcion=f"Nuevo reporte creado en el foro: {reporte.titulo}",
                detalles={
                    'reporte_id': reporte.id,
                    'titulo': reporte.titulo,
                    'categoria': reporte.categoria
                },
                usuario=request.user
            )
            # Realizar análisis automático con Stanza
            try:
                texto_completo = f"{reporte.titulo} {reporte.descripcion}"
                resultado_analisis = servicio_analisis_stanza.analizar_texto(texto_completo)
                reporte.analisis_stanza = resultado_analisis
                reporte.tipo_ataque_detectado = resultado_analisis.get('tipo_ataque')
                reporte.confianza_analisis = resultado_analisis.get('confianza')
                reporte.estado = 'ANALIZADO'
                reporte.fecha_analisis = timezone.now()
                reporte.save()
                messages.success(request, f'Reporte creado y analizado. Tipo de ataque detectado: {reporte.get_tipo_ataque_detectado_display() if reporte.tipo_ataque_detectado else "No determinado"}')
            except Exception as e:
                logger.error(f"Error en análisis automático: {str(e)}")
                messages.success(request, 'Reporte creado exitosamente. El análisis se realizará próximamente.')
            return redirect('detalle_reporte_foro', pk=reporte.pk)
    else:
        form = ForoCiberseguridadForm()
    return render(request, 'foro/crear_reporte.html', {'form': form})

@login_required
def detalle_reporte_foro(request, pk):
    """Vista para ver los detalles de un reporte."""
    reporte = get_object_or_404(ForoCiberseguridad, pk=pk)
    
    if request.method == 'POST':
        form = RespuestaForoForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.reporte = reporte
            respuesta.usuario = request.user
            respuesta.save()
            
            messages.success(request, 'Respuesta agregada exitosamente.')
            return redirect('detalle_reporte_foro', pk=reporte.pk)
    else:
        form = RespuestaForoForm()
    
    # Obtener respuestas del reporte
    respuestas = RespuestaForo.objects.filter(reporte=reporte).order_by('fecha_creacion')
    
    context = {
        'reporte': reporte,
        'respuestas': respuestas,
        'form_respuesta': form,
    }
    
    return render(request, 'foro/detalle_reporte.html', context)

@login_required
def analisis_texto_stanza(request):
    """Vista para análisis de texto con Stanza."""
    resultado_analisis = None
    
    if request.method == 'POST':
        form = AnalisisTextoForm(request.POST)
        if form.is_valid():
            texto = form.cleaned_data['texto']
            incluir_linguistico = form.cleaned_data['incluir_analisis_linguistico']
            
            # Realizar análisis
            resultado_analisis = servicio_analisis_stanza.analizar_texto(texto)
            
            if not incluir_linguistico:
                # Remover análisis lingüístico detallado si no se solicita
                resultado_analisis.pop('entidades_nombres', None)
                resultado_analisis.pop('analisis_linguistico', None)
            
            messages.success(request, f'Análisis completado. Tipo detectado: {resultado_analisis.get("tipo_ataque", "No determinado")}')
    else:
        form = AnalisisTextoForm()
    
    context = {
        'form': form,
        'resultado_analisis': resultado_analisis,
    }
    
    return render(request, 'foro/analisis_texto.html', context)

@login_required
def mis_reportes_foro(request):
    """Vista para ver los reportes del usuario actual."""
    reportes = ForoCiberseguridad.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    # Paginación
    paginator = Paginator(reportes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'reportes': page_obj,
        'total_reportes': reportes.count(),
    }
    
    return render(request, 'foro/mis_reportes.html', context)

@login_required
def analizar_reportes_pendientes(request):
    """Vista para analizar reportes pendientes (solo para administradores)."""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('foro_ciberseguridad')
    
    if request.method == 'POST':
        try:
            reportes_analizados = servicio_analisis_stanza.analizar_reportes_pendientes()
            messages.success(request, f'Se analizaron {reportes_analizados} reportes pendientes.')
        except Exception as e:
            messages.error(request, f'Error al analizar reportes: {str(e)}')
        
        return redirect('foro_ciberseguridad')
    
    # Mostrar reportes pendientes
    reportes_pendientes = ForoCiberseguridad.objects.filter(estado='PENDIENTE').order_by('fecha_creacion')
    
    context = {
        'reportes_pendientes': reportes_pendientes,
        'total_pendientes': reportes_pendientes.count(),
    }
    
    return render(request, 'foro/analizar_pendientes.html', context)

@login_required
def reanalizar_reporte(request, pk):
    """Re-analiza un reporte existente con Stanza."""
    reporte = get_object_or_404(ForoCiberseguridad, pk=pk)
    
    if request.method == 'POST':
        try:
            # Combinar título y descripción para el análisis
            texto_completo = f"{reporte.titulo} {reporte.descripcion}"
            
            # Realizar análisis
            resultado_analisis = servicio_analisis_stanza.analizar_texto(texto_completo)
            
            # Actualizar el reporte
            reporte.analisis_stanza = resultado_analisis
            reporte.tipo_ataque_detectado = resultado_analisis.get('tipo_ataque')
            reporte.confianza_analisis = resultado_analisis.get('confianza')
            reporte.fecha_analisis = timezone.now()
            reporte.save()
            
            messages.success(request, f'Reporte re-analizado. Tipo detectado: {reporte.get_tipo_ataque_detectado_display() if reporte.tipo_ataque_detectado else "No determinado"}')
            
        except Exception as e:
            logger.error(f"Error al re-analizar reporte {reporte.id}: {str(e)}")
            messages.error(request, f'Error al re-analizar: {str(e)}')
        
        return redirect('detalle_reporte_foro', pk=reporte.pk)
    
    return redirect('detalle_reporte_foro', pk=reporte.pk)

@login_required
def crud_empresas(request):
    """Vista unificada para CRUD de empresas."""
    from .forms import EmpresaForm
    from .models import Empresas
    empresas = Empresas.objects.all()
    form = EmpresaForm()
    edit_empresa = None
    edit_form = None
    delete_empresa = None
    # Crear empresa
    if request.method == 'POST' and 'crear_empresa' in request.POST:
        form = EmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.usuario = request.user
            empresa.save()
            messages.success(request, 'Empresa creada exitosamente.')
            return redirect('crud_empresas')
    # Editar empresa
    if request.method == 'POST' and 'editar_empresa' in request.POST:
        edit_empresa = Empresas.objects.get(pk=request.POST.get('empresa_id'))
        edit_form = EmpresaForm(request.POST, request.FILES, instance=edit_empresa)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Empresa actualizada exitosamente.')
            return redirect('crud_empresas')
    # Eliminar empresa
    if request.method == 'POST' and 'eliminar_empresa' in request.POST:
        delete_empresa = Empresas.objects.get(pk=request.POST.get('empresa_id'))
        delete_empresa.delete()
        messages.success(request, 'Empresa eliminada exitosamente.')
        return redirect('crud_empresas')
    # Si se va a editar, cargar el formulario con la empresa
    if request.method == 'GET' and 'edit' in request.GET:
        edit_empresa = Empresas.objects.get(pk=request.GET.get('edit'))
        edit_form = EmpresaForm(instance=edit_empresa)
    # Si se va a eliminar, cargar la empresa
    if request.method == 'GET' and 'delete' in request.GET:
        delete_empresa = Empresas.objects.get(pk=request.GET.get('delete'))
    return render(request, 'crud_empresas.html', {
        'empresas': empresas,
        'form': form,
        'edit_empresa': edit_empresa,
        'edit_form': edit_form,
        'delete_empresa': delete_empresa
    })
