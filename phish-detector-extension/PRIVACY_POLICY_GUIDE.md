# 🔒 Guía para Agregar la Política de Privacidad a Chrome Web Store

## ✅ Violación a Resolver

**ID del Elemento:** fccnaojadcdeokngngdlbaanojodicea  
**Infracción:** Purple Nickel - Enlace a la política de privacidad no disponible  
**Problema:** El enlace a la política de privacidad no está en el campo designado

---

## 📋 Archivo Creado

✅ **privacy-policy.html** - Política de privacidad completa y profesional en español

**Ubicación:**  
```
herramientas/phish-detector-extension/privacy-policy.html
```

---

## 🌐 PASO 1: Hospedar la Política de Privacidad

Necesitas hacer que el archivo `privacy-policy.html` esté disponible públicamente en internet. Tienes 3 opciones:

### Opción A: GitHub Pages (GRATIS y RECOMENDADO) 🎯

1. **Sube el archivo a tu repositorio GitHub:**
   ```bash
   cd "C:\Users\Usuario\OneDrive\Escritorio\Carpeta para leo\2025repequipo09-main"
   git add herramientas/phish-detector-extension/privacy-policy.html
   git commit -m "Add privacy policy for Chrome Web Store"
   git push
   ```

2. **Activa GitHub Pages:**
   - Ve a tu repositorio en GitHub
   - Settings → Pages (menú izquierdo)
   - Source: Deploy from branch
   - Branch: main / (root)
   - Click Save

3. **Tu URL será:**
   ```
   https://[tu-usuario].github.io/2025repequipo09/herramientas/phish-detector-extension/privacy-policy.html
   ```
   
   Por ejemplo:
   ```
   https://feriasw.github.io/2025repequipo09/herramientas/phish-detector-extension/privacy-policy.html
   ```

4. **Espera 2-5 minutos** para que GitHub Pages publique el sitio

5. **Verifica** abriendo la URL en tu navegador

---

### Opción B: Google Drive (Rápido pero menos profesional)

1. Sube `privacy-policy.html` a Google Drive
2. Clic derecho → Compartir
3. Cambiar a "Cualquier persona con el enlace"
4. Copiar el enlace
5. Usa este enlace en Chrome Web Store

**Nota:** El enlace será largo y poco profesional, por eso GitHub Pages es mejor.

---

### Opción C: Tu Propio Servidor/Hosting

Si tienes hosting web, simplemente sube el archivo y usa la URL directa:
```
https://tu-dominio.com/privacy-policy.html
```

---

## 🏪 PASO 2: Agregar la URL a Chrome Web Store

1. **Ve a Chrome Web Store Developer Dashboard:**
   ```
   https://chrome.google.com/webstore/devconsole
   ```

2. **Selecciona tu extensión:**
   - Busca "Aegis Code Phish Detector"
   - ID: fccnaojadcdeokngngdlbaanojodicea

3. **Ve a la pestaña "Privacy"** (Privacidad)

4. **Busca el campo "Privacy Policy"** (Política de Privacidad)

5. **Pega tu URL pública:**
   ```
   Ejemplo: https://feriasw.github.io/2025repequipo09/herramientas/phish-detector-extension/privacy-policy.html
   ```

6. **Guarda los cambios**

7. **NO publiques todavía** - Chrome revisará primero

---

## 📨 PASO 3: Responder a Chrome Web Store

Una vez agregada la URL:

1. **Ve a tu correo** donde recibiste la notificación de infracción

2. **O en el Developer Dashboard** verás la violación activa

3. **Indica que has corregido el problema:**
   - "He agregado la política de privacidad en el campo designado"
   - "La URL es: [tu-url-aquí]"

4. **Espera la revisión** (puede tomar 1-3 días hábiles)

---

## ✅ Verificación de la Política

La política de privacidad creada incluye:

### ✅ Información Requerida:
- [x] Identificación del desarrollador
- [x] Correo de contacto: codeaegis1@gmail.com
- [x] Descripción de la funcionalidad
- [x] Datos que NO se recopilan
- [x] Explicación de permisos
- [x] Medidas de seguridad
- [x] Derechos del usuario
- [x] Información de contacto

### ✅ Características:
- [x] Diseño profesional y responsive
- [x] En español (idioma de tu audiencia)
- [x] Fácil de leer
- [x] Completa y transparente
- [x] Cumple con políticas de Chrome Web Store

---

## 🎯 Contenido de la Política

La política explica claramente que tu extensión:

### ❌ NO Recopila:
- Información personal
- Credenciales
- Historial de navegación
- Datos financieros
- Cookies o tracking
- Geolocalización

### ✅ SÍ Hace:
- Análisis LOCAL de texto seleccionado
- Muestra resultados en tu navegador
- Permite reportes VOLUNTARIOS por email
- No almacena datos

### 🔑 Permisos Explicados:
- **contextMenus:** Menú "Analizar si es phishing"
- **activeTab:** Acceder al texto seleccionado
- **notifications:** Mostrar resultados
- **scripting:** Insertar interfaz de resultados
- **host_permissions:** Funcionar en cualquier sitio

---

## 🚨 Importante

1. **NO edites la descripción de la extensión** para agregar la política
   - Chrome rechaza esto específicamente
   - SOLO usa el campo designado "Privacy Policy"

2. **La URL debe ser pública y accesible**
   - No uses URLs locales (localhost)
   - No uses URLs que requieran autenticación
   - Verifica que funcione en modo incógnito

3. **Mantén la política actualizada**
   - Si cambias la funcionalidad, actualiza la política
   - Mantén la misma URL

---

## 📞 Soporte

Si tienes problemas:

1. **Verifica que la URL funcione:**
   - Abre en modo incógnito
   - Prueba desde otro dispositivo
   - Confirma que carga rápido

2. **Contacta a Chrome Web Store Support:**
   - Si la revisión toma más de 5 días
   - Si rechazan después de agregar la política

3. **Email del proyecto:**
   - codeaegis1@gmail.com

---

## 📊 Timeline Esperado

| Paso | Tiempo Estimado |
|------|----------------|
| 1. Hospedar en GitHub Pages | 5-10 minutos |
| 2. Agregar URL a Chrome Web Store | 2 minutos |
| 3. Responder a la notificación | 2 minutos |
| 4. Revisión de Chrome | 1-3 días hábiles |
| 5. Aprobación y publicación | 1 día |

**Total:** 2-5 días desde que agregas la URL

---

## ✅ Checklist Final

Antes de enviar:

- [ ] Archivo `privacy-policy.html` está subido a GitHub
- [ ] GitHub Pages está activado
- [ ] URL pública funciona (probada en navegador)
- [ ] URL agregada en campo "Privacy Policy" de Chrome Web Store
- [ ] Cambios guardados en Developer Dashboard
- [ ] Respuesta enviada a notificación de violación (si aplica)

---

## 🎉 ¡Listo!

Una vez completados estos pasos, tu extensión cumplirá con los requisitos de Chrome Web Store y podrás publicarla sin problemas.

**Recuerda:** La política es transparente y honesta sobre tu extensión, lo cual es exactamente lo que Chrome Web Store requiere.

---

**Última actualización:** Enero 2025  
**Versión:** 1.0
