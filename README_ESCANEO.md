# Sistema de Escaneo Manual de Archivos - Aegis Code

## Descripción

Este sistema permite a los usuarios escanear archivos específicos en busca de malware de forma manual. El sistema utiliza reglas YARA locales y consultas a VirusTotal para detectar amenazas.

## Características

- **Escaneo Manual**: El usuario selecciona qué archivo escanear
- **Un proceso a la vez**: Solo se permite un escaneo simultáneo
- **Reglas YARA**: Detección local usando reglas YARA personalizadas
- **VirusTotal**: Consulta a la API de VirusTotal para análisis adicional
- **Interfaz Moderna**: UI responsive con Bootstrap 5
- **Registro de Actividades**: Todas las actividades se registran en la base de datos

## Flujo de Trabajo

1. **Selección de Archivo**: El usuario navega a "Escanear Archivo" y selecciona un archivo
2. **Procesamiento**: El sistema calcula el hash SHA-256 del archivo
3. **Escaneo YARA**: Se aplican las reglas YARA locales
4. **Consulta VirusTotal**: Si YARA no detecta nada, se consulta VirusTotal
5. **Resultado**: Se muestra el resultado y se registra en la base de datos

## Tecnologías Utilizadas

- **Django**: Framework web
- **YARA**: Motor de detección de malware
- **VirusTotal API**: Análisis de amenazas en la nube
- **Bootstrap 5**: Interfaz de usuario
- **SQLite**: Base de datos

## Instalación y Configuración

### Requisitos

```bash
pip install -r requirements.txt
```

### Configuración de VirusTotal

1. Obtener una API key de VirusTotal
2. Actualizar la variable `virustotal_api_key` en `Crud/services.py`

### Reglas YARA

Las reglas YARA se encuentran en el directorio `yara_rules/`:
- `malware_basic.yar`: Detección básica de malware
- `ransomware.yar`: Detección de ransomware

## Uso del Sistema

### 1. Acceso al Escaneo

Navegar a: `http://localhost:8000/escanear/`

### 2. Selección de Archivo

- Hacer clic en "Seleccionar Archivo"
- Elegir el archivo a escanear
- Hacer clic en "Iniciar Escaneo"

### 3. Proceso de Escaneo

El sistema mostrará:
- Progreso del escaneo
- Estado actual (calculando hash, escaneando YARA, consultando VirusTotal)
- Tiempo estimado

### 4. Resultado

- **Archivo Seguro**: Mensaje verde de confirmación
- **Malware Detectado**: Alerta roja con detalles de la amenaza

## Estructura del Código

### Servicios (`Crud/services.py`)

- `ServicioEscaneo`: Clase principal para el escaneo
- `escanear_archivo()`: Método principal de escaneo
- `_escanear_yara_archivo()`: Escaneo con reglas YARA
- `_consultar_virustotal()`: Consulta a VirusTotal

### Vistas (`Crud/views.py`)

- `escanear_archivo()`: Vista para el formulario de escaneo
- `obtener_estado_escaneo()`: API para obtener estado del escaneo

### Plantillas

- `escanear_archivo.html`: Interfaz de escaneo
- `home.html`: Dashboard principal actualizado

## Limitaciones

- **Tamaño de archivo**: Máximo 32MB (límite de VirusTotal)
- **Rate limit**: 4 consultas por minuto a VirusTotal
- **Un escaneo**: Solo un archivo puede ser escaneado a la vez
- **Conexión internet**: Requerida para consultas a VirusTotal

## Seguridad

- Validación de tipos de archivo
- Sanitización de nombres de archivo
- Rate limiting para evitar abuso
- Registro de todas las actividades

## Monitoreo y Logs

Todas las actividades se registran en:
- `RegistroActividad`: Actividades del sistema
- `Amenaza`: Amenazas detectadas
- Logs del sistema para debugging

## Personalización

### Agregar Reglas YARA

1. Crear archivo `.yar` en `yara_rules/`
2. El sistema cargará automáticamente las nuevas reglas
3. Reiniciar el servidor para aplicar cambios

### Modificar Configuración

- Cambiar API key de VirusTotal en `services.py`
- Ajustar límites de tamaño de archivo
- Modificar intervalos de rate limiting

## Troubleshooting

### Error: "Ya hay un escaneo en progreso"
- Esperar a que termine el escaneo actual
- Reiniciar el servidor si es necesario

### Error: "Rate limit de VirusTotal alcanzado"
- Esperar 15 segundos entre consultas
- Considerar actualizar a API premium

### Error: "Archivo no encontrado"
- Verificar que el archivo existe
- Comprobar permisos de lectura

## Contribución

Para agregar nuevas funcionalidades:
1. Crear rama feature
2. Implementar cambios
3. Agregar tests
4. Crear pull request

## Licencia

Este proyecto está bajo la licencia MIT. 

# Notas sobre ejecución de scripts en Windows

## 1. Abrir los archivos en un IDE

Los archivos descargados con extensión `.ps1` (PowerShell), `.py` (Python) u otros scripts deben abrirse en un **IDE** (como VS Code, PyCharm, etc.) o en un editor de texto avanzado. Esto es importante porque estos archivos contienen **código** y no deben abrirse como documentos de texto plano o con programas de ofimática.

---

## 2. Permitir la ejecución de scripts en PowerShell

Por seguridad, Windows PowerShell no permite ejecutar scripts por defecto. Si al intentar ejecutar un script ves un error como:

> "File ... cannot be loaded because running scripts is disabled on this system."

Sigue estos pasos para permitir la ejecución **solo en la sesión actual** (recomendado para desarrollo):

### Pasos:

1. **Abre PowerShell como administrador**  
   Haz clic derecho en el icono de PowerShell y selecciona "Ejecutar como administrador".

2. **Ejecuta este comando:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
   ```
   Esto permite ejecutar scripts solo en la ventana de PowerShell abierta. Cuando la cierres, la política vuelve a la original.

3. **Ejecuta tu script normalmente:**
   ```powershell
   .\nombre_del_script.ps1
   ```

---

**Nota:** No cambies la política de ejecución global salvo que sepas lo que haces. Si tienes dudas, consulta con el responsable del proyecto.

--- 