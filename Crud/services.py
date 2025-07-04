import os
import json
import logging
import requests
import hashlib
import yara
import time
import shutil
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from .models import Empresas, Amenaza, RegistroActividad

logger = logging.getLogger(__name__)

# Configuración de YARA
YARA_RULES_DIR = os.path.join(settings.BASE_DIR, 'yara_rules')
YARA_RULES = {}

def _cargar_reglas_yara():
    """Carga las reglas YARA desde el directorio de reglas."""
    global YARA_RULES
    try:
        if not os.path.exists(YARA_RULES_DIR):
            os.makedirs(YARA_RULES_DIR)
            logger.warning(f"Directorio de reglas YARA creado en: {YARA_RULES_DIR}")
            return

        for archivo in os.listdir(YARA_RULES_DIR):
            if archivo.endswith('.yar') or archivo.endswith('.yara'):
                ruta_regla = os.path.join(YARA_RULES_DIR, archivo)
                try:
                    YARA_RULES[archivo] = yara.compile(ruta_regla)
                    logger.info(f"Regla YARA cargada: {archivo}")
                except Exception as e:
                    logger.error(f"Error al cargar regla YARA {archivo}: {str(e)}")
    except Exception as e:
        logger.error(f"Error al cargar reglas YARA: {str(e)}")

# Cargar reglas YARA al iniciar
_cargar_reglas_yara()

class ServicioEscaneo:
    def __init__(self):
        # Configuración de VirusTotal
        self.virustotal_api_key = "50090cdca66602e767ea1d42a05135b418779e8a6f84e347bbfb39e894d5431b"
        self.virustotal_base_url = "https://www.virustotal.com/api/v3"
        self.virustotal_headers = {
            "x-apikey": self.virustotal_api_key,
            "Accept": "application/json"
        }
        
        # Estado del escaneo actual
        self.escaneo_actual = None
        self._ultima_consulta_vt = 0
        
        logger.info("ServicioEscaneo inicializado")

    def escanear_archivo(self, archivo_subido, empresa_id=None, usuario=None):
        """
        Escanea un archivo específico subido por el usuario o empresa.
        Args:
            archivo_subido: Archivo subido por el usuario
            empresa_id: ID de la empresa que realiza el escaneo (opcional)
            usuario: Usuario que realiza el escaneo (opcional)
        Returns:
            dict: Resultado del escaneo
        """
        try:
            # Verificar que no hay otro escaneo en progreso
            if self.escaneo_actual and self.escaneo_actual.get('estado') == 'procesando':
                return {
                    'error': 'Ya hay un escaneo en progreso. Espere a que termine.'
                }
            empresa = None
            if empresa_id:
                try:
                    empresa = Empresas.objects.get(id=empresa_id)
                except Empresas.DoesNotExist:
                    empresa = None
            # Inicializar estado del escaneo
            nombre_archivo = archivo_subido.name
            self.escaneo_actual = {
                'archivo': nombre_archivo,
                'empresa': empresa,
                'estado': 'procesando',
                'inicio': timezone.now(),
                'progreso': 0
            }
            logger.info(f"Iniciando escaneo de archivo: {nombre_archivo}")
            # Paso 1: Calcular hash del archivo
            self.escaneo_actual['progreso'] = 25
            try:
                hash_sha256 = self._calcular_hash_archivo(archivo_subido)
            except Exception as e:
                logger.error(f"Error al calcular hash del archivo: {str(e)}")
                self.escaneo_actual = None
                return {'error': f'No se pudo leer el archivo correctamente para calcular el hash. Puede estar corrupto o no ser accesible. Detalle: {str(e)}'}
            logger.info(f"Hash calculado: {hash_sha256[:16]}...")
            time.sleep(1)
            # Paso 2: Escanear con YARA
            self.escaneo_actual['progreso'] = 50
            resultado_yara = self._escanear_yara_archivo(archivo_subido)
            es_malware_yara = resultado_yara['detectado']
            logger.info(f"Resultado YARA: {'MALWARE' if es_malware_yara else 'SEGURO'}")
            time.sleep(1)
            # Paso 3: Consultar VirusTotal (siempre)
            self.escaneo_actual['progreso'] = 75
            resultado_vt = self._consultar_virustotal(hash_sha256)
            es_malware = False
            razon_amenaza = None
            detectores = {}
            # YARA detecta malware
            if resultado_yara['detectado']:
                es_malware = True
                razon_amenaza = 'Detectado por YARA'
                detectores['yara'] = resultado_yara['resultados']
            # VirusTotal detecta malware
            vt_stats = {}
            if resultado_vt:
                vt_stats = resultado_vt.get('data', {}).get('attributes', {}).get('stats', {})
                malicious = vt_stats.get('malicious', 0)
                suspicious = vt_stats.get('suspicious', 0)
                if malicious > 0 or suspicious > 5:
                    es_malware = True
                    razon_amenaza = 'Detectado por VirusTotal'
                    detectores['virustotal'] = vt_stats
                    logger.info("VirusTotal detectó amenaza - marcando como malware")
            else:
                logger.info("No se pudo consultar VirusTotal o hash no encontrado")
            # Si no hay detectores, forzar archivo seguro y registrar como actividad segura
            if not detectores:
                logger.info(f"[Escaneo] Archivo seguro: {nombre_archivo}. No se detectó ninguna amenaza por YARA ni VirusTotal.")
                resultado = {
                    'archivo': nombre_archivo,
                    'hash_sha256': hash_sha256,
                    'es_malware': False,
                    'estado': 'completado',
                    'yara': resultado_yara,
                    'virustotal': resultado_vt,
                    'razon_amenaza': None,
                    'timestamp': timezone.now().isoformat(),
                    'severidad': 'NO_EXISTE',
                    'detectores': detectores
                }
                self._registrar_actividad(nombre_archivo, resultado, empresa, usuario)
                self.escaneo_actual = None
                return resultado
            # Si hay detectores, registrar como amenaza
            logger.info(f"[Escaneo] Archivo AMENAZA: {nombre_archivo}. Detectores: {detectores}")
            resultado = {
                'archivo': nombre_archivo,
                'hash_sha256': hash_sha256,
                'es_malware': True,
                'estado': 'completado',
                'yara': resultado_yara,
                'virustotal': resultado_vt,
                'razon_amenaza': razon_amenaza,
                'timestamp': timezone.now().isoformat(),
                'severidad': None,
                'detectores': detectores
            }
            self._registrar_amenaza(nombre_archivo, resultado, empresa, usuario)
            self.escaneo_actual = None
            return resultado
        except Exception as e:
            logger.error(f"Error en escaneo de archivo: {str(e)}")
            self.escaneo_actual = None
            return {'error': f'Error durante el escaneo: {str(e)}'}

    def obtener_estado_escaneo(self):
        """Obtiene el estado actual del escaneo."""
        if not self.escaneo_actual:
            return {'estado': 'sin_escaneo'}
        
        return {
            'estado': self.escaneo_actual['estado'],
            'archivo': self.escaneo_actual['archivo'],
            'progreso': self.escaneo_actual['progreso'],
            'inicio': self.escaneo_actual['inicio'].isoformat()
        }

    def _calcular_hash_archivo(self, archivo_subido):
        """Calcula el hash SHA-256 de un archivo subido."""
        try:
            sha256_hash = hashlib.sha256()
            for chunk in archivo_subido.chunks():
                sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.error(f"Error al calcular hash: {str(e)}")
            raise

    def _escanear_yara_archivo(self, archivo_subido):
        """Escanea un archivo subido usando reglas YARA locales."""
        try:
            resultados = []
            
            # Asegurarse de que las reglas estén cargadas
            if not YARA_RULES:
                _cargar_reglas_yara()
                logger.info(f"Reglas YARA cargadas: {len(YARA_RULES)} reglas")
            
            # Crear archivo temporal en el directorio temporal del sistema
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{archivo_subido.name}") as temp_file:
                temp_path = temp_file.name
                # Escribir el contenido del archivo subido
                for chunk in archivo_subido.chunks():
                    temp_file.write(chunk)
                temp_file.flush()
            
            logger.info(f"Archivo temporal creado: {temp_path}")
            
            # Escanear el archivo con cada regla
            for nombre_regla, regla in YARA_RULES.items():
                try:
                    logger.info(f"Escaneando con regla: {nombre_regla}")
                    matches = regla.match(temp_path)
                    if matches:
                        logger.info(f"¡Coincidencia encontrada en regla {nombre_regla}!")
                        for match in matches:
                            resultados.append({
                                'regla': nombre_regla,
                                'strings': match.strings,
                                'metadatos': match.meta,
                                'namespace': match.namespace
                            })
                except Exception as e:
                    logger.error(f"Error al escanear con regla {nombre_regla}: {str(e)}")
                    continue
            
            # Limpiar archivo temporal
            try:
                os.remove(temp_path)
                logger.info(f"Archivo temporal eliminado: {temp_path}")
            except Exception as e:
                logger.warning(f"No se pudo eliminar archivo temporal {temp_path}: {str(e)}")
            
            logger.info(f"Escaneo YARA completado. Resultados: {len(resultados)}")
            
            return {
                'detectado': len(resultados) > 0,
                'resultados': resultados,
                'total_reglas': len(YARA_RULES),
                'reglas_aplicadas': list(YARA_RULES.keys())
            }
            
        except Exception as e:
            logger.error(f"Error en escaneo YARA: {str(e)}")
            raise

    def _consultar_virustotal(self, hash_sha256):
        """Consulta el hash en VirusTotal."""
        try:
            # Verificar rate limit (4 requests por minuto para API pública)
            tiempo_actual = time.time()
            tiempo_desde_ultima = tiempo_actual - self._ultima_consulta_vt
            if tiempo_desde_ultima < 15:  # Esperar 15 segundos entre consultas
                time.sleep(15 - tiempo_desde_ultima)
            
            # Realizar la consulta
            url = f"{self.virustotal_base_url}/files/{hash_sha256}"
            response = requests.get(url, headers=self.virustotal_headers)
            
            # Actualizar timestamp de última consulta
            self._ultima_consulta_vt = time.time()
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logger.info(f"Hash no encontrado en VirusTotal: {hash_sha256}")
                return None
            elif response.status_code == 429:
                logger.warning("Rate limit de VirusTotal alcanzado")
                time.sleep(60)  # Esperar 1 minuto antes de reintentar
                return self._consultar_virustotal(hash_sha256)
            else:
                logger.error(f"Error en consulta VirusTotal: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error al consultar VirusTotal: {str(e)}")
            return None

    def _registrar_amenaza(self, nombre_archivo, resultado, empresa=None, usuario=None):
        """Registra una amenaza detectada."""
        try:
            detectores = resultado.get('detectores', {})
            if not detectores:
                logger.info(f"[Registrar Amenaza] No se registró amenaza para {nombre_archivo} porque detectores está vacío.")
                return
            vt_data = resultado.get("virustotal")
            if vt_data:
                stats = vt_data.get("data", {}).get("attributes", {}).get("stats", {})
            else:
                stats = {}
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            if malicious > 5 or suspicious > 10:
                severidad = 'ALTA'
            elif malicious > 2 or suspicious > 5:
                severidad = 'MEDIA'
            else:
                severidad = 'BAJA'
            # Solo crear Amenaza si hay empresa
            if empresa:
                Amenaza.objects.create(
                    empresa=empresa,
                    tipo='MALWARE',
                    severidad=severidad,
                    descripcion=f"Archivo malicioso detectado: {nombre_archivo}",
                    detalles_tecnicos={
                        'hash_sha256': resultado.get("hash_sha256"),
                        'detectores': stats,
                        'reporte_completo': resultado
                    }
                )
            # Registrar actividad (siempre)
            RegistroActividad.objects.create(
                empresa=empresa if empresa else None,
                tipo='ALERTA',
                descripcion=f"Archivo malicioso detectado: {nombre_archivo}",
                detalles={
                    'archivo': nombre_archivo,
                    'severidad': severidad,
                    'detectores': stats
                },
                usuario=usuario if usuario else (empresa.usuario if empresa else None)
            )
        except Exception as e:
            logger.error(f"Error al registrar amenaza: {str(e)}")

    def _registrar_actividad(self, nombre_archivo, resultado, empresa=None, usuario=None):
        """Registra una actividad de escaneo."""
        try:
            RegistroActividad.objects.create(
                empresa=empresa if empresa else None,
                tipo='ESCANEO',
                descripcion=f"Archivo escaneado: {nombre_archivo} - SEGURO" if resultado.get('severidad') == 'NO_EXISTE' else f"Archivo escaneado: {nombre_archivo}",
                detalles={
                    'archivo': nombre_archivo,
                    'hash_sha256': resultado.get("hash_sha256"),
                    'resultado': resultado
                },
                usuario=usuario if usuario else (empresa.usuario if empresa else None)
            )
        except Exception as e:
            logger.error(f"Error al registrar actividad: {str(e)}")

# Instancia global del servicio
servicio_escaneo = ServicioEscaneo()

class MLModelManager:
    """Gestor de modelos de Machine Learning con descarga dinámica"""
    
    def __init__(self):
        self.models_dir = os.path.join(settings.BASE_DIR, 'media', 'ml_models')
        self.stanza_dir = os.path.join(self.models_dir, 'stanza')
        self.nltk_dir = os.path.join(self.models_dir, 'nltk_data')
        
        # Crear directorios si no existen
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.stanza_dir, exist_ok=True)
        os.makedirs(self.nltk_dir, exist_ok=True)
        
        logger.info(f"MLModelManager inicializado. Directorio: {self.models_dir}")
    
    def ensure_stanza_models(self):
        """Asegura que los modelos de Stanza estén disponibles"""
        try:
            import stanza
            
            # Verificar si el modelo español ya existe
            es_model_path = os.path.join(self.stanza_dir, 'es')
            if not os.path.exists(es_model_path):
                logger.info("Descargando modelo Stanza para español...")
                stanza.download('es', model_dir=self.stanza_dir)
                logger.info("Modelo Stanza descargado exitosamente")
            else:
                logger.info("Modelo Stanza ya existe")
            
            return True
            
        except ImportError:
            logger.warning("Stanza no está instalado")
            return False
        except Exception as e:
            logger.error(f"Error descargando Stanza: {str(e)}")
            return False
    
    def ensure_nltk_models(self):
        """Asegura que los modelos de NLTK estén disponibles"""
        try:
            import nltk
            
            # Agregar directorio personalizado a NLTK
            nltk.data.path.append(self.nltk_dir)
            
            # Modelos necesarios
            models_to_download = ['punkt', 'stopwords', 'wordnet']
            
            for model in models_to_download:
                try:
                    nltk.data.find(f'tokenizers/{model}')
                    logger.info(f"Modelo NLTK {model} ya existe")
                except LookupError:
                    logger.info(f"Descargando modelo NLTK {model}...")
                    nltk.download(model, download_dir=self.nltk_dir)
                    logger.info(f"Modelo NLTK {model} descargado")
            
            return True
            
        except ImportError:
            logger.warning("NLTK no está instalado")
            return False
        except Exception as e:
            logger.error(f"Error descargando NLTK: {str(e)}")
            return False
    
    def get_models_status(self):
        """Obtiene el estado de los modelos ML"""
        status = {
            'stanza': False,
            'nltk': False,
            'yara': False,
            'models_dir': self.models_dir
        }
        
        # Verificar Stanza
        try:
            es_model_path = os.path.join(self.stanza_dir, 'es')
            status['stanza'] = os.path.exists(es_model_path)
        except:
            pass
        
        # Verificar NLTK
        try:
            nltk_data_path = os.path.join(self.nltk_dir, 'tokenizers')
            status['nltk'] = os.path.exists(nltk_data_path)
        except:
            pass
        
        # Verificar YARA
        yara_rules_dir = os.path.join(settings.BASE_DIR, 'yara_rules')
        status['yara'] = os.path.exists(yara_rules_dir) and len(os.listdir(yara_rules_dir)) > 0
        
        return status
    
    def cleanup_old_models(self):
        """Limpia modelos antiguos para ahorrar espacio"""
        try:
            # Limpiar archivos temporales de descarga
            temp_patterns = ['*.tmp', '*.download', '*.part']
            for pattern in temp_patterns:
                for root, dirs, files in os.walk(self.models_dir):
                    for file in files:
                        if file.endswith(pattern.replace('*', '')):
                            file_path = os.path.join(root, file)
                            try:
                                os.remove(file_path)
                                logger.info(f"Archivo temporal eliminado: {file_path}")
                            except:
                                pass
            
            return True
        except Exception as e:
            logger.error(f"Error limpiando modelos: {str(e)}")
            return False

# Instancia global del gestor de modelos
ml_model_manager = MLModelManager()

class ServicioAnalisisStanza:
    """Servicio para análisis de texto usando Stanza (NLP)"""
    
    def __init__(self):
        self.nlp = None
        self._inicializar_stanza()
        
        # Patrones de palabras clave para detectar tipos de ataques (mejorados)
        self.patrones_ataques = {
            'MALWARE': [
                'virus', 'malware', 'troyano', 'spyware', 'adware', 'rootkit', 'backdoor',
                'archivo malicioso', 'programa malicioso', 'software malicioso',
                'descarga automática', 'instalación no autorizada', 'comportamiento extraño',
                'antivirus', 'detecta', 'archivo', 'descargué', 'descargue', 'descarga',
                'correo', 'email', 'link', 'enlace', 'no reconozco', 'no conozco',
                'persona desconocida', 'remitente desconocido', 'sospechoso'
            ],
            'PHISHING': [
                'phishing', 'suplantación', 'correo falso', 'email falso', 'sitio falso',
                'banco falso', 'credenciales', 'contraseña', 'datos bancarios',
                'enlace sospechoso', 'url falsa', 'página falsa', 'link sospechoso',
                'correo', 'email', 'link', 'enlace', 'no reconozco', 'no conozco',
                'persona desconocida', 'remitente desconocido', 'sospechoso',
                'banco', 'actualizar', 'verificar', 'confirmar', 'datos'
            ],
            'RANSOMWARE': [
                'ransomware', 'rescate', 'pago', 'bitcoin', 'encriptación', 'archivos bloqueados',
                'pantalla de rescate', 'mensaje de rescate', 'archivos encriptados',
                'no puedo acceder', 'archivos perdidos', 'rescate digital',
                'pantalla negra', 'archivos bloqueados', 'pago exigido'
            ],
            'DOS': [
                'denegación de servicio', 'dos', 'ddos', 'ataque distribuido', 'servidor caído',
                'sitio web caído', 'lentitud extrema', 'sobrecarga', 'tráfico excesivo',
                'servicio no disponible', 'timeout', 'error de conexión',
                'sitio web', 'servidor', 'lento', 'caído', 'no responde'
            ],
            'INTRUSION': [
                'intrusión', 'acceso no autorizado', 'login sospechoso', 'sesión extraña',
                'actividad sospechosa', 'acceso remoto', 'conexión desconocida',
                'usuario no reconocido', 'login desde ubicación extraña',
                'acceso', 'login', 'sesión', 'cuenta', 'usuario'
            ],
            'ROBO_DATOS': [
                'robo de datos', 'datos filtrados', 'información robada', 'base de datos comprometida',
                'datos personales', 'información personal', 'credenciales robadas',
                'filtración de datos', 'datos expuestos', 'brecha de seguridad',
                'datos', 'información', 'personal', 'privada', 'filtrada'
            ]
        }
        
        # Palabras de contexto que aumentan la probabilidad de ser un ataque
        self.palabras_contexto = [
            'sospechoso', 'extraño', 'desconocido', 'no reconozco', 'no conozco',
            'alerta', 'peligro', 'amenaza', 'problema', 'error', 'virus',
            'malicioso', 'falso', 'fraude', 'estafa', 'robo', 'intrusión'
        ]
        
        logger.info("ServicioAnalisisStanza inicializado")
    
    def _inicializar_stanza(self):
        """Inicializa Stanza con el modelo en español usando descarga dinámica"""
        try:
            import stanza
            
            # Usar el gestor de modelos para asegurar que los modelos estén disponibles
            if ml_model_manager.ensure_stanza_models():
                try:
                    # Cargar modelo usando el directorio personalizado
                    self.nlp = stanza.Pipeline('es', processors='tokenize,pos,lemma,ner', 
                                             model_dir=ml_model_manager.stanza_dir)
                    logger.info("Modelo Stanza en español cargado correctamente")
                except Exception as e:
                    logger.warning(f"No se pudo cargar modelo español: {str(e)}")
                    # Intentar con modelo en inglés como fallback
                    try:
                        self.nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,ner')
                        logger.info("Modelo Stanza en inglés cargado como fallback")
                    except Exception as e2:
                        logger.error(f"No se pudo cargar ningún modelo de Stanza: {str(e2)}")
                        self.nlp = None
            else:
                logger.error("No se pudieron descargar los modelos de Stanza")
                self.nlp = None
                
        except ImportError:
            logger.error("Stanza no está instalado. El análisis de texto no estará disponible.")
            self.nlp = None
    
    def analizar_texto(self, texto):
        """
        Analiza un texto para detectar tipos de ataques cibernéticos.
        
        Args:
            texto (str): Texto a analizar
            
        Returns:
            dict: Resultado del análisis
        """
        try:
            if not texto or not texto.strip():
                return {
                    'error': 'Texto vacío o inválido',
                    'tipo_ataque': None,
                    'confianza': 0.0,
                    'detalles': {}
                }
            
            texto = texto.lower().strip()
            resultado = {
                'tipo_ataque': None,
                'confianza': 0.0,
                'detalles': {},
                'palabras_clave_encontradas': [],
                'entidades_nombres': [],
                'analisis_linguistico': {}
            }
            
            # Análisis con patrones de palabras clave
            puntuaciones = {}
            palabras_encontradas = {}
            puntuacion_contexto = 0
            
            # Contar palabras de contexto
            for palabra_contexto in self.palabras_contexto:
                if palabra_contexto in texto:
                    puntuacion_contexto += 1
            
            for tipo_ataque, palabras_clave in self.patrones_ataques.items():
                puntuacion = 0
                palabras_tipo = []
                
                for palabra in palabras_clave:
                    if palabra in texto:
                        puntuacion += 1
                        palabras_tipo.append(palabra)
                
                if puntuacion > 0:
                    # Aumentar puntuación si hay palabras de contexto
                    puntuacion += puntuacion_contexto * 0.5
                    puntuaciones[tipo_ataque] = puntuacion
                    palabras_encontradas[tipo_ataque] = palabras_tipo
            
            # Determinar el tipo de ataque con mayor puntuación
            if puntuaciones:
                tipo_ataque_detectado = max(puntuaciones, key=puntuaciones.get)
                puntuacion_maxima = puntuaciones[tipo_ataque_detectado]
                total_palabras_tipo = len(self.patrones_ataques[tipo_ataque_detectado])
                
                # Calcular confianza basada en la proporción de palabras encontradas
                # Reducir el umbral para ser más sensible
                confianza = min((puntuacion_maxima / total_palabras_tipo) * 150, 100.0)
                
                resultado['tipo_ataque'] = tipo_ataque_detectado
                resultado['confianza'] = round(confianza, 2)
                resultado['palabras_clave_encontradas'] = palabras_encontradas
                
                # Si la confianza es muy baja, pero hay palabras de contexto, considerar como PHISHING
                if confianza < 15.0 and puntuacion_contexto > 0:
                    resultado['tipo_ataque'] = 'PHISHING'
                    resultado['confianza'] = 60.0  # Confianza media para casos sospechosos
                    logger.info("Texto sospechoso detectado - marcando como PHISHING")
            else:
                # Si no se detectó nada específico pero hay palabras de contexto
                if puntuacion_contexto > 0:
                    resultado['tipo_ataque'] = 'PHISHING'
                    resultado['confianza'] = 50.0
                    logger.info("Texto con contexto sospechoso - marcando como PHISHING")
                else:
                    resultado['tipo_ataque'] = 'OTRO'
                    resultado['confianza'] = 10.0
            
            # Análisis lingüístico con Stanza si está disponible
            if self.nlp:
                try:
                    doc = self.nlp(texto)
                    
                    # Extraer entidades nombradas
                    entidades = []
                    for sent in doc.sentences:
                        for ent in sent.ents:
                            entidades.append({
                                'texto': ent.text,
                                'tipo': ent.type,
                                'inicio': ent.start_char,
                                'fin': ent.end_char
                            })
                    
                    resultado['entidades_nombres'] = entidades
                    
                    # Análisis de tokens y POS
                    tokens_info = []
                    for sent in doc.sentences:
                        for token in sent.tokens:
                            for word in token.words:
                                tokens_info.append({
                                    'texto': word.text,
                                    'lemma': word.lemma,
                                    'pos': word.pos,
                                    'upos': word.upos
                                })
                    
                    resultado['analisis_linguistico'] = {
                        'tokens': tokens_info,
                        'total_tokens': len(tokens_info)
                    }
                    
                except Exception as e:
                    logger.error(f"Error en análisis lingüístico con Stanza: {str(e)}")
            
            # Análisis adicional de contexto
            resultado['detalles'] = {
                'longitud_texto': len(texto),
                'palabras_totales': len(texto.split()),
                'puntuaciones_por_tipo': puntuaciones,
                'palabras_contexto_encontradas': puntuacion_contexto,
                'texto_analizado': texto[:500] + "..." if len(texto) > 500 else texto
            }
            
            logger.info(f"Análisis completado. Tipo detectado: {resultado['tipo_ataque']}, Confianza: {resultado['confianza']}%")
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error en análisis de texto: {str(e)}")
            return {
                'error': f'Error durante el análisis: {str(e)}',
                'tipo_ataque': 'OTRO',
                'confianza': 0.0,
                'detalles': {}
            }
    
    def analizar_reportes_pendientes(self):
        """
        Analiza todos los reportes pendientes del foro.
        
        Returns:
            int: Número de reportes analizados
        """
        try:
            from .models import ForoCiberseguridad
            
            reportes_pendientes = ForoCiberseguridad.objects.filter(estado='PENDIENTE')
            reportes_analizados = 0
            
            for reporte in reportes_pendientes:
                try:
                    # Combinar título y descripción para el análisis
                    texto_completo = f"{reporte.titulo} {reporte.descripcion}"
                    
                    # Realizar análisis
                    resultado_analisis = self.analizar_texto(texto_completo)
                    
                    # Actualizar el reporte
                    reporte.analisis_stanza = resultado_analisis
                    reporte.tipo_ataque_detectado = resultado_analisis.get('tipo_ataque')
                    reporte.confianza_analisis = resultado_analisis.get('confianza')
                    reporte.estado = 'ANALIZADO'
                    reporte.fecha_analisis = timezone.now()
                    reporte.save()
                    
                    reportes_analizados += 1
                    logger.info(f"Reporte analizado: {reporte.titulo}")
                    
                except Exception as e:
                    logger.error(f"Error al analizar reporte {reporte.id}: {str(e)}")
                    continue
            
            logger.info(f"Análisis completado. {reportes_analizados} reportes analizados")
            return reportes_analizados
            
        except Exception as e:
            logger.error(f"Error en análisis de reportes pendientes: {str(e)}")
            return 0

# Instancia global del servicio de análisis
servicio_analisis_stanza = ServicioAnalisisStanza() 