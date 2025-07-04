from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import os
import logging
from .download_manager import DownloadManager

logger = logging.getLogger(__name__)

@login_required
def download_app_view(request):
    """Vista para descargar la aplicación completa"""
    try:
        download_manager = DownloadManager()
        
        # Crear el paquete descargable
        zip_path = download_manager.create_local_package()
        
        # Leer el archivo ZIP
        with open(zip_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="aegis_code_local.zip"'
        
        # Limpiar archivos temporales después de un tiempo
        # (se puede implementar con Celery o similar)
        
        messages.success(request, 'Descarga iniciada. El archivo contiene la aplicación completa para uso local.')
        return response
        
    except Exception as e:
        logger.error(f"Error en descarga de aplicación: {str(e)}")
        messages.error(request, f'Error al crear el paquete de descarga: {str(e)}')
        return redirect('home')

@login_required
def download_models_view(request):
    """Vista para descargar modelos ML manualmente"""
    try:
        from .services import ml_model_manager
        
        # Descargar modelos ML usando el gestor
        stanza_success = ml_model_manager.ensure_stanza_models()
        nltk_success = ml_model_manager.ensure_nltk_models()
        
        if stanza_success and nltk_success:
            messages.success(request, 'Todos los modelos de ML descargados exitosamente.')
        elif stanza_success or nltk_success:
            messages.warning(request, 'Algunos modelos se descargaron, pero otros fallaron. Revisa los logs.')
        else:
            messages.error(request, 'No se pudieron descargar los modelos de ML.')
        
        return redirect('downloads')
        
    except Exception as e:
        logger.error(f"Error descargando modelos ML: {str(e)}")
        messages.error(request, f'Error al descargar modelos ML: {str(e)}')
        return redirect('downloads')

@login_required
def download_status_view(request):
    """Vista para verificar el estado de los modelos ML"""
    try:
        from .services import ml_model_manager
        
        # Obtener estado usando el gestor de modelos
        models_status = ml_model_manager.get_models_status()
        
        return JsonResponse({
            'status': 'success',
            'models': models_status
        })
        
    except Exception as e:
        logger.error(f"Error verificando estado de modelos: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@login_required
def download_page_view(request):
    """Página principal de descargas"""
    context = {
        'title': 'Descargas - Aegis Code',
        'downloads_available': [
            {
                'name': 'Aplicación Completa',
                'description': 'Descarga la aplicación completa para uso local',
                'size': '~500MB',
                'includes': ['Django', 'Modelos ML', 'Reglas YARA', 'Scripts de instalación'],
                'url_name': 'download-app',
                'icon': '📦'
            },
            {
                'name': 'Modelos ML',
                'description': 'Descarga manual de modelos de machine learning',
                'size': '~200MB',
                'includes': ['Stanza (español)', 'NLTK', 'Modelos de análisis'],
                'url_name': 'download-models',
                'icon': '🤖'
            }
        ]
    }
    
    return render(request, 'downloads.html', context) 