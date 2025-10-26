# Phish Detector Extension

Extensión para navegadores que ayuda a detectar posibles intentos de phishing en correos electrónicos y páginas web.

## Características

- Análisis de texto seleccionado en busca de indicadores de phishing
- Detección de patrones comunes en correos de phishing
- Interfaz simple y fácil de usar
- Resultados en tiempo real

## Instalación

1. Clona o descarga este repositorio
2. Abre tu navegador Chrome/Edge/Brave
3. Ve a `chrome://extensions/`
4. Activa el "Modo desarrollador" en la esquina superior derecha
5. Haz clic en "Cargar descomprimida"
6. Selecciona la carpeta `phish-detector-extension`

## Uso

1. Navega a cualquier página web o correo electrónico
2. Selecciona el texto que deseas analizar
3. Haz clic derecho y selecciona "Analizar si es phishing"
4. Revisa los resultados en la esquina superior derecha

## Indicadores de phishing que detecta

- Palabras clave de urgencia (urgente, inmediato, verifique, etc.)
- Nombres de servicios comunes (banco, PayPal, Netflix, etc.)
- Solicitudes de credenciales
- Direcciones IP en el texto
- Enlaces HTTP inseguros
- Direcciones de correo electrónico

## Personalización

Puedes modificar los patrones de detección en el archivo `background.js` en la variable `phishingIndicators`.

## Seguridad

Esta extensión solo analiza el texto que seleccionas y no envía información a servidores externos. Todo el procesamiento se realiza localmente en tu navegador.

## Licencia

MIT
