import os
import zipfile
import json
import shutil
import tempfile
from pathlib import Path
from django.conf import settings
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

class DownloadManager:
    """Gestor de descargas para la aplicación local"""
    
    def __init__(self):
        self.base_dir = settings.BASE_DIR
        self.temp_dir = os.path.join(self.base_dir, 'temp_downloads')
        self.models_dir = os.path.join(self.base_dir, 'media', 'ml_models')
        
    def create_local_package(self):
        """Crea un paquete descargable para uso local"""
        try:
            # Crear directorio temporal
            os.makedirs(self.temp_dir, exist_ok=True)
            
            # Lista de archivos y carpetas a incluir
            include_paths = [
                'Crud/',
                'Crud_Damian/',
                'crud_Matias/',
                'manage.py',
                'requirements-dev.txt',
                'README.md',
                'yara_rules/',
                'media/',
                '.gitignore',
                'install-dev.ps1',
                'install_local.ps1',
                'check_size.ps1'
            ]
            
            # Crear archivo ZIP
            zip_path = os.path.join(self.temp_dir, 'aegis_code_local.zip')
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for path in include_paths:
                    full_path = os.path.join(self.base_dir, path)
                    if os.path.exists(full_path):
                        if os.path.isdir(full_path):
                            for root, dirs, files in os.walk(full_path):
                                for file in files:
                                    file_path = os.path.join(root, file)
                                    arc_name = os.path.relpath(file_path, self.base_dir)
                                    zipf.write(file_path, arc_name)
                        else:
                            arc_name = os.path.relpath(full_path, self.base_dir)
                            zipf.write(full_path, arc_name)
            
            # Crear archivo de instrucciones
            instructions = self._create_instructions()
            instructions_path = os.path.join(self.temp_dir, 'INSTRUCCIONES_INSTALACION.txt')
            with open(instructions_path, 'w', encoding='utf-8') as f:
                f.write(instructions)
            
            # Agregar instrucciones al ZIP
            with zipfile.ZipFile(zip_path, 'a', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(instructions_path, 'INSTRUCCIONES_INSTALACION.txt')
            
            return zip_path
            
        except Exception as e:
            logger.error(f"Error creando paquete local: {str(e)}")
            raise
    
    def _create_instructions(self):
        """Crea las instrucciones de instalación"""
        return """
=== AEGIS CODE - INSTALACIÓN LOCAL ===

Este paquete contiene la aplicación Aegis Code completa para uso local.

📋 REQUISITOS PREVIOS:
- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para control de versiones)

🚀 PASOS DE INSTALACIÓN:

1. DESCOMPRIMIR:
   - Extrae todos los archivos en una carpeta de tu elección
   - Ejemplo: C:\\AegisCode\\

2. ABRIR TERMINAL:
   - Abre PowerShell o CMD en la carpeta donde extrajiste los archivos
   - Ejecuta: cd C:\\AegisCode\\

3. INSTALAR DEPENDENCIAS:
   - Ejecuta: .\\install_local.ps1 (recomendado)
   - O manualmente: pip install -r requirements-dev.txt

4. CONFIGURAR BASE DE DATOS:
   - Ejecuta: python manage.py migrate
   - Ejecuta: python manage.py createsuperuser

5. EJECUTAR LA APLICACIÓN:
   - Ejecuta: python manage.py runserver
   - Abre: http://127.0.0.1:8000/

📁 ESTRUCTURA DEL PROYECTO:
- Crud/ - Aplicación principal
- Crud_Damian/ - Configuración Django
- crud_Matias/ - Aplicación adicional
- media/ - Archivos multimedia
- yara_rules/ - Reglas de detección de malware

🔧 FUNCIONALIDADES INCLUIDAS:
- Escaneo de archivos con YARA
- Análisis de texto con Stanza
- Dashboard de seguridad
- Gestión de empresas
- Foro de ciberseguridad

⚠️ NOTAS IMPORTANTES:
- La primera ejecución descargará automáticamente los modelos de ML
- Los archivos de media se crearán automáticamente
- Para desarrollo, usa requirements-dev.txt
- Para producción, usa requirements-prod.txt

🆘 SOLUCIÓN DE PROBLEMAS:
- Si hay errores de dependencias: pip install --upgrade pip
- Si hay errores de migración: python manage.py makemigrations
- Si hay errores de modelos ML: Los modelos se descargarán automáticamente

📞 SOPORTE:
- Revisa los logs en la consola para errores específicos
- Verifica que todas las dependencias estén instaladas

¡Disfruta usando Aegis Code localmente!
        """
    
    def download_ml_models(self):
        """Descarga los modelos de ML necesarios"""
        try:
            os.makedirs(self.models_dir, exist_ok=True)
            
            # Descargar modelos de Stanza
            self._download_stanza_models()
            
            # Descargar modelos de NLTK
            self._download_nltk_models()
            
            return True
            
        except Exception as e:
            logger.error(f"Error descargando modelos ML: {str(e)}")
            return False
    
    def _download_stanza_models(self):
        """Descarga modelos de Stanza"""
        try:
            import stanza
            
            stanza_dir = os.path.join(self.models_dir, 'stanza')
            os.makedirs(stanza_dir, exist_ok=True)
            
            # Descargar modelo español si no existe
            es_model_path = os.path.join(stanza_dir, 'es')
            if not os.path.exists(es_model_path):
                logger.info("Descargando modelo Stanza para español...")
                stanza.download('es', model_dir=stanza_dir)
                logger.info("Modelo Stanza descargado exitosamente")
            else:
                logger.info("Modelo Stanza ya existe")
                
        except ImportError:
            logger.warning("Stanza no está instalado, omitiendo descarga")
        except Exception as e:
            logger.error(f"Error descargando Stanza: {str(e)}")
    
    def _download_nltk_models(self):
        """Descarga modelos de NLTK"""
        try:
            import nltk
            
            nltk_dir = os.path.join(self.models_dir, 'nltk_data')
            os.makedirs(nltk_dir, exist_ok=True)
            
            # Agregar directorio personalizado a NLTK
            nltk.data.path.append(nltk_dir)
            
            # Descargar modelos necesarios
            models_to_download = ['punkt', 'stopwords', 'wordnet']
            
            for model in models_to_download:
                try:
                    nltk.data.find(f'tokenizers/{model}')
                    logger.info(f"Modelo NLTK {model} ya existe")
                except LookupError:
                    logger.info(f"Descargando modelo NLTK {model}...")
                    nltk.download(model, download_dir=nltk_dir)
                    logger.info(f"Modelo NLTK {model} descargado")
                    
        except ImportError:
            logger.warning("NLTK no está instalado, omitiendo descarga")
        except Exception as e:
            logger.error(f"Error descargando NLTK: {str(e)}")
    
    def cleanup_temp_files(self):
        """Limpia archivos temporales"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            logger.error(f"Error limpiando archivos temporales: {str(e)}") 