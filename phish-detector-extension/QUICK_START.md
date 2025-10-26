# 🚀 GUÍA RÁPIDA - AEGIS SECURITY SUITE

## ⚡ Instalación Rápida (2 minutos)

1. Abre Chrome o Edge
2. Escribe en la barra: `chrome://extensions/`
3. Activa el switch "Modo de desarrollador" (arriba a la derecha)
4. Clic en "Cargar extensión sin empaquetar"
5. Selecciona la carpeta: `phish-detector-extension`
6. ✅ ¡Listo! Verás el ícono de Aegis en la barra de herramientas

---

## 🎯 Uso Básico

### 1️⃣ Analizar Texto Sospechoso

```
1. Selecciona cualquier texto en una página web
2. Clic derecho sobre el texto
3. Selecciona "Analizar si es phishing"
4. Aparecerá un panel premium en la esquina superior derecha
```

**Ejemplo de texto para probar:**
```
URGENTE: Su cuenta de banco será suspendida.
Haga clic aquí para verificar: http://g00gle.com/verify
Ingrese su contraseña y número de tarjeta inmediatamente.
```

---

### 2️⃣ Enviar Reporte

```
1. En el panel de análisis, clic en "📨 Enviar Reporte Detallado"
2. Completa el formulario:
   - Tu email (opcional)
   - Descripción de lo que encontraste
   - Categoría del ataque
3. Clic en "📨 Enviar Reporte"
4. Se abre tu cliente de correo con el reporte listo
5. El reporte se guarda automáticamente en tu navegador
```

---

### 3️⃣ Ver Reportes Guardados

```
1. Clic en el ícono de Aegis en la barra de herramientas
2. Verás estadísticas:
   - Total de reportes
   - Reportes de alto riesgo
3. Clic en "📋 Ver Reportes Guardados"
4. Se abre una ventana con todos tus reportes
```

---

### 4️⃣ Exportar Datos

```
1. Clic en el ícono de Aegis
2. Clic en "💾 Exportar Datos"
3. Se descarga un archivo JSON con todos tus reportes
```

---

## 🔍 Qué Detecta la Extensión

### ✅ Análisis NLP (Procesamiento de Lenguaje Natural)
- 🚨 **Urgencia artificial**: "urgente", "inmediato", "ahora"
- ⚠️ **Amenazas**: "suspender cuenta", "bloquear", "eliminar"
- 🔐 **Solicitud de credenciales**: "contraseña", "usuario", "pin"
- 💰 **Información financiera**: "tarjeta", "cvv", "cuenta bancaria"
- 🎭 **Manipulación emocional**: "última oportunidad", "ganador"

### ✅ Typosquatting (Dominios Falsos)
- 🌐 **Sustitución de caracteres**: g00gle.com, micr0soft.com
- 📝 **Errores ortográficos**: paypall.com, netflex.com
- 🔤 **Caracteres cirílicos**: usando letras que parecen latinas
- 🔗 **URLs sospechosas**: direcciones IP, URLs muy largas

### ✅ Marcas Monitoreadas
- 🏦 Bancos: Santander, BBVA, Bancolombia
- 💻 Tech: Google, Microsoft, PayPal, Netflix, Amazon
- 🏛️ Gobierno: Hacienda, Seguridad Social

---

## 📧 Email de Reportes

**Todos los reportes se envían a:** `codeaegis1@gmail.com`

**El email incluye:**
- Fecha y hora del reporte
- Tu email (si lo proporcionaste)
- Categoría del ataque
- URL donde encontraste el phishing
- Nivel de riesgo calculado
- Tu descripción del problema
- Indicadores detectados automáticamente
- Análisis NLP completo
- Texto analizado
- Información técnica del navegador

---

## 💾 Base de Datos Local

**Ubicación:** Almacenada en tu navegador (IndexedDB)

**Qué se guarda:**
- Todos los reportes que envías
- Análisis completos
- Estadísticas
- Timestamps

**Privacidad:**
- ✅ Todo se guarda localmente en tu navegador
- ✅ No se envía nada a servidores externos
- ✅ Puedes exportar y borrar cuando quieras

---

## 🎨 Características Premium

### UI Moderna
- ✨ Animaciones suaves
- 🎨 Gradientes profesionales
- 📊 Barra de progreso animada
- 🎯 Badges de riesgo dinámicos
- 💫 Efectos de blur y sombras

### Dashboard
- 📊 Estadísticas en tiempo real
- 📋 Visualización de reportes
- 💾 Exportación de datos
- 🛡️ Indicador de protección activa

---

## 🐛 Solución de Problemas

### La extensión no aparece
```
✓ Verifica que "Modo de desarrollador" esté activado
✓ Recarga la extensión en chrome://extensions/
✓ Reinicia el navegador
```

### El análisis no funciona
```
✓ Asegúrate de seleccionar texto antes de hacer clic derecho
✓ Verifica que la página haya cargado completamente
✓ Revisa la consola del navegador (F12) para errores
```

### No se guardan los reportes
```
✓ Verifica que el navegador permita IndexedDB
✓ Asegúrate de completar el campo "Descripción"
✓ Revisa que no estés en modo incógnito
```

### El email no se abre
```
✓ Configura un cliente de correo predeterminado
✓ O copia manualmente el contenido del reporte
✓ El reporte se guarda localmente de todas formas
```

---

## 📚 Archivos Importantes

### Para Revisar el Código:
- `content.js` - UI Premium y modal de reporte
- `background.js` - Análisis de phishing y email
- `database.js` - Sistema de base de datos
- `nlp-sentiment.js` - Análisis de sentimiento
- `nlp-entities.js` - Detección de entidades
- `popup.html` / `popup.js` - Dashboard

### Para Documentación:
- `FEATURES.md` - Características detalladas
- `RESUMEN.md` - Resumen de implementación
- `QUICK_START.md` - Esta guía

---

## 🎓 Para Demostración

### Texto de Prueba 1 (Alto Riesgo):
```
URGENTE - ACCIÓN REQUERIDA
Su cuenta de Santander será suspendida en 24 horas.
Verifique sus datos aquí: http://santandar-seguridad.com
Ingrese su contraseña y número de tarjeta de crédito.
```

### Texto de Prueba 2 (Medio Riesgo):
```
Felicidades! Has ganado un iPhone 15 Pro gratis.
Haz clic aquí para reclamar tu premio.
Solo tienes 2 horas para aprovechar esta oferta exclusiva.
```

### Texto de Prueba 3 (Bajo Riesgo):
```
Hola, te escribo para recordarte la reunión de mañana.
Nos vemos a las 10:00 AM en la oficina.
Saludos!
```

---

## ✅ Checklist de Demostración

- [ ] Extensión instalada y visible
- [ ] Probar análisis con texto de alto riesgo
- [ ] Mostrar UI premium con animaciones
- [ ] Demostrar indicadores detectados
- [ ] Abrir modal de reporte
- [ ] Completar y enviar reporte
- [ ] Mostrar dashboard con estadísticas
- [ ] Ver reportes guardados
- [ ] Exportar datos

---

## 🆘 Soporte

**Email:** codeaegis1@gmail.com

**Desarrollado por:** Aegis Code Team

**Versión:** 1.0 Premium Edition

---

**¡Listo para usar! 🚀**
