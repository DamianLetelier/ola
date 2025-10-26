// Import NLP modules using importScripts (service worker compatible)
try {
  importScripts('nlp-sentiment.js', 'nlp-entities.js');
  console.log('NLP modules loaded');
} catch (error) {
  console.error('Error loading NLP modules:', error);
}

let sentimentAnalyzer = null;
let entityDetector = null;

// Initialize NLP modules
function initializeNLP() {
  try {
    if (typeof PhishingSentimentAnalyzer !== 'undefined') {
      sentimentAnalyzer = new PhishingSentimentAnalyzer();
    }
    if (typeof PhishingEntityDetector !== 'undefined') {
      entityDetector = new PhishingEntityDetector();
    }
    
    if (!sentimentAnalyzer || !entityDetector) {
      sentimentAnalyzer = { analyzeSentiment: () => ({ overallRisk: 0, indicators: [] }) };
      entityDetector = { analyzeEntities: () => ({ overallRisk: 0, indicators: [] }) };
    }
    console.log('NLP analyzers initialized');
  } catch (error) {
    console.error('Error initializing NLP:', error);
    sentimentAnalyzer = { analyzeSentiment: () => ({ overallRisk: 0, indicators: [] }) };
    entityDetector = { analyzeEntities: () => ({ overallRisk: 0, indicators: [] }) };
  }
}

// Create context menu item
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'analyzePhishing',
    title: 'Analizar si es phishing',
    contexts: ['selection']
  });
  
  initializeNLP();
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'analyzePhishing') {
    analyzeText(info.selectionText, tab);
  }
});

// Common misspellings in phishing emails
const COMMON_MISSPELLINGS = {
  // Common Spanish misspellings
  'verificacion': 'verificación',
  'actualizacion': 'actualización',
  'iniciar sesion': 'iniciar sesión',
  'contraseña': ['constraseña', 'contrasea', 'contraseña', 'contrasena', 'contraseña'],
  'usuario': ['usurio', 'usuairo', 'usurario'],
  'banco': ['vancos', 'bancos', 'banco'],
  'seguridad': ['segurida', 'seguridada', 'seguridadd'],
  'importante': ['inportante', 'importanet', 'importnte'],
  'urgente': ['urgente', 'urgentes', 'urgencia', 'urgentee'],
  'soporte': ['soporte', 'soporte técnico', 'soportetecnico'],
  
  // Common brand names with common misspellings
  'paypal': ['paypal', 'paypall', 'paypal', 'paypai', 'paypa1'],
  'netflix': ['netflix', 'netflex', 'netflx', 'netflix'],
  'microsoft': ['microsoft', 'micr0soft', 'micros0ft', 'microsoft'],
  'facebook': ['facebook', 'facebok', 'facebo0k', 'facebook'],
  'santander': ['santander', 'santander', 'santander'],
  'bbva': ['bbva', 'bva', 'bbva'],
  'bancolombia': ['bancolombia', 'bancolombia', 'bancolombia'],
  
  // Common phishing phrases with misspellings
  'actualice sus datos': ['actualice sus datos', 'actualize sus datos', 'actualice su informacion'],
  'iniciar sesión': ['iniciar sesion', 'iniciar secion', 'iniciar sesión'],
  'verifique su cuenta': ['verifique su cuenta', 'verifique su cuentas', 'verifique su cuenta'],
  'seguridad de la cuenta': ['seguridad de la cuenta', 'seguridad de su cuenta', 'seguridad cuenta'],
  'acceso no autorizado': ['acceso no autorizado', 'acceso no autorizado', 'acceso no autorizado'],
  'soporte técnico': ['soporte tecnico', 'soporte técnico', 'soporte'],
  'problemas de seguridad': ['problemas de seguridad', 'problemas seguridad', 'problemas con seguridad'],
  'cuenta suspendida': ['cuenta suspendida', 'cuenta suspendida temporalmente', 'cuenta bloqueada'],
  'confirmar información': ['confirmar informacion', 'confirmar datos', 'confirmar información'],
  'datos personales': ['datos personales', 'información personal', 'datos personales'],
  'tarjeta de crédito': ['tarjeta de credito', 'tarjeta credito', 'tarjeta de crédito'],
  'número de cuenta': ['numero de cuenta', 'nº de cuenta', 'número de cuenta'],
  'contraseña expirada': ['contraseña expirada', 'contraseña vencida', 'contraseña caducada'],
  'inicio de sesión inusual': ['inicio de sesion inusual', 'acceso inusual', 'inicio de sesión inusual'],
  'verificación de seguridad': ['verificacion de seguridad', 'verificación seguridad', 'verificación de seguridad'],
  'actualizar información': ['actualizar informacion', 'actualizar datos', 'actualizar información'],
  'problema con su cuenta': ['problema con su cuenta', 'problemas con su cuenta', 'problema en su cuenta'],
  'soporte al cliente': ['soporte al cliente', 'servicio al cliente', 'atención al cliente']
};

// Advanced phishing detection functions
function checkForTyposquatting(domain) {
  // Common typos and variations of popular domains
  const commonTypos = {
    'g00gle': 'google',
    'go0gle': 'google',
    'goggle': 'google',
    'facebok': 'facebook',
    'facebo0k': 'facebook',
    'paypai': 'paypal',
    'paypa1': 'paypal',
    'micr0soft': 'microsoft',
    'micros0ft': 'microsoft'
  };
  
  for (const [typo, correct] of Object.entries(commonTypos)) {
    if (domain.includes(typo)) {
      return { isTyposquatting: true, original: typo, correct };
    }
  }
  return { isTyposquatting: false };
}

function checkUrlAnomalies(url) {
  // Check for URL shorteners
  const shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 'rebrand.ly', 't.co'];
  const isShortened = shorteners.some(shortener => url.includes(shortener));
  
  // Check for suspicious characters
  const hasSuspiciousChars = /[\u0430-\u044f]/.test(url); // Cyrillic characters
  
  // Check for HTTPS
  const hasHttps = url.startsWith('https://');
  
  return {
    isShortened,
    hasSuspiciousChars,
    hasHttps: !hasHttps // Higher risk if no HTTPS
  };
}

function checkForSpoofedElements(html) {
  // Check for hidden elements
  const hiddenElements = (html.match(/style=["'][^"']*(display:\s*none|visibility:\s*hidden|opacity:\s*0)/gi) || []).length;
  
  // Check for mouseover events that might hide the real URL
  const mouseoverEvents = (html.match(/onmouseover=["'][^"']*window\.status\s*=/gi) || []).length;
  
  return {
    hiddenElements,
    mouseoverEvents
  };
}

// Function to check for spelling mistakes in text
function checkSpellingMistakes(text) {
  const mistakes = [];
  const words = text.toLowerCase().split(/\s+/);
  
  // Check each word against common misspellings
  Object.entries(COMMON_MISSPELLINGS).forEach(([correct, variations]) => {
    const variationsList = Array.isArray(variations) ? variations : [variations];
    
    // Check both individual words and phrases
    variationsList.forEach(variation => {
      if (text.toLowerCase().includes(variation.toLowerCase())) {
        // Find the exact match with case sensitivity
        const regex = new RegExp(`\\b${escapeRegExp(variation)}\\b`, 'gi');
        const matches = text.match(regex);
        
        if (matches) {
          matches.forEach(match => {
            // Only add if the matched text is not exactly the correct version
            if (match.toLowerCase() !== correct.toLowerCase()) {
              mistakes.push({
                found: match,
                suggestion: correct,
                type: 'Falta ortográfica',
                severity: 'medium'
              });
            }
          });
        }
      }
    });
  });
  
  return mistakes;
}

// Helper function to escape special characters in regex
function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Function to analyze text for phishing indicators
async function analyzeText(text, tab) {
  // Ensure NLP modules are loaded
  if (!sentimentAnalyzer || !entityDetector) {
    await initializeNLP();
  }

  // Run NLP analysis
  let sentimentAnalysis = { overallRisk: 0, indicators: [] };
  let entityAnalysis = { overallRisk: 0, indicators: [] };
  
  try {
    sentimentAnalysis = sentimentAnalyzer.analyzeSentiment(text);
    entityAnalysis = entityDetector.analyzeEntities(text);
  } catch (error) {
    console.error('Error in NLP analysis:', error);
  }

  // Advanced phishing detection logic (existing patterns)
  const phishingIndicators = [
    // Urgency indicators
    { pattern: /\b(?:urgent|urgente|inmediato|verifique|actualice|cuenta|suspensión|bloqueo|acción requerida|actúe ahora)\b/gi, score: 1.2, category: 'Urgencia' },
    
    // Brand impersonation
    { pattern: /\b(?:banco|paypal|netflix|facebook|google|microsoft|amazon|apple|santander|bbva|bancolombia)\b/gi, score: 0.7, category: 'Suplantación de marca' },
    
    // Common phishing phrases with potential misspellings
    { pattern: /\b(?:verificaci[oó]n de (?:seguridad|cuenta)|iniciar sesi[oó]n|contrase[ñn]a ex?pira(?:da|r[áa])|actuali[zs]a(?:r|ci[oó]n)|soporte t[eé]cni[ck]o|cuenta (?:suspendida|bloqueada)|datos (?:personales|bancarios)|tarjeta de cr[eé]dito|n[uú]mero de cuenta|seguridad de la cuenta|acceso no autorizado|problemas? de seguridad|confirmar informaci[oó]n|inicio de sesi[oó]n inusual)\b/gi, score: 1.5, category: 'Frase de phishing común' },
    
    // Credential requests
    { pattern: /\b(?:contraseña|password|usuario|login|iniciar sesión|credenciales|clave|pin|seguridad)\b/gi, score: 1.3, category: 'Solicitud de credenciales' },
    
    // Suspicious URLs and domains
    { pattern: /\b(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b/g, score: 2.5, category: 'URL con dirección IP' },
    { pattern: /\b(?:http:\/\/|www\.)\S+\b/gi, score: 0.7, category: 'Enlace HTTP inseguro' },
    { pattern: /https?:\/\/[^\s/$.?#].[^\s]*\.[^\s/]{10,}/gi, score: 1.2, category: 'URL sospechosamente larga' },
    
    // Email patterns
    { pattern: /\b(?:\W|^)[\w.\-]{0,25}@(?:[\w\-]+\.)+[a-zA-Z]{2,7}(\s|$)/g, score: 0.6, category: 'Dirección de correo' },
    
    // Financial and personal information requests
    { pattern: /\b(?:tarjeta de crédito|número de seguro social|dni|cvv|código de seguridad|fecha de vencimiento|número de cuenta)\b/gi, score: 1.8, category: 'Información financiera' },
    
    // Grammar and spelling mistakes (common in phishing)
    { pattern: /\b(?:su cuenta a sido|haz clic aqui|actualize sus datos|su cuenta sera cerrada|su cuenta ha sido bloqueada)\b/gi, score: 1.5, category: 'Errores gramaticales' },
    
    // Threats and warnings
    { pattern: /\b(?:su cuenta será eliminada|será suspendida|tiene 24 horas|última advertencia|acción legal)\b/gi, score: 1.4, category: 'Amenazas' },
    
    // Unusual characters (possible obfuscation)
    { pattern: /[\u0430-\u044f]/g, score: 2.0, category: 'Caracteres sospechosos' }
  ];

  let totalScore = 0;
  let indicatorsFound = [];
  let categories = new Set();

  // Basic pattern matching
  phishingIndicators.forEach(indicator => {
    const matches = text.match(indicator.pattern);
    if (matches) {
      const score = matches.length * indicator.score;
      totalScore += score;
      indicatorsFound = [...indicatorsFound, ...matches.map(match => ({
        text: match,
        category: indicator.category,
        score: indicator.score
      }))];
      categories.add(indicator.category);
    }
  });

  // Check for spelling mistakes
  const spellingMistakes = checkSpellingMistakes(text);
  
  // Add spelling mistakes to indicators
  spellingMistakes.forEach(mistake => {
    indicatorsFound.push({
      text: `Posible falta ortográfica: "${mistake.found}" (sugerencia: "${mistake.suggestion}")`,
      category: 'Falta ortográfica',
      score: 0.8
    });
    totalScore += 0.8;
  });
  
  // Advanced checks
  const urlMatches = text.match(/https?:\/\/[^\s]+/gi) || [];
  let urlAnalysis = [];
  
  urlMatches.forEach(url => {
    try {
      const urlObj = new URL(url);
      const typosquatting = checkForTyposquatting(urlObj.hostname);
      const anomalies = checkUrlAnomalies(url);
      
      if (typosquatting.isTyposquatting) {
        totalScore += 2.5;
        indicatorsFound.push({
          text: `Dominio sospechoso: ${typosquatting.original} (parece ${typosquatting.correct})`,
          category: 'Typosquatting',
          score: 2.5
        });
        categories.add('Typosquatting');
      }
      
      if (anomalies.isShortened) {
        totalScore += 1.5;
        indicatorsFound.push({
          text: `URL acortada detectada: ${url}`,
          category: 'URL acortada',
          score: 1.5
        });
        categories.add('URL acortada');
      }
      
      if (anomalies.hasSuspiciousChars) {
        totalScore += 2.0;
        indicatorsFound.push({
          text: 'Caracteres sospechosos en URL',
          category: 'Caracteres sospechosos',
          score: 2.0
        });
      }
      
      if (anomalies.hasHttps) {
        totalScore += 1.0;
        indicatorsFound.push({
          text: 'Conexión no segura (HTTP)',
          category: 'Seguridad',
          score: 1.0
        });
      }
      
      urlAnalysis.push({
        url: urlObj.href,
        ...anomalies,
        typosquatting
      });
    } catch (e) {
      console.error('Error analyzing URL:', e);
    }
  });

  // HTML content analysis (if available)
  let htmlAnalysis = {};
  if (tab && tab.url && tab.url.startsWith('http')) {
    try {
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: () => document.documentElement.outerHTML
      }, (results) => {
        if (results && results[0]) {
          const html = results[0].result;
          const spoofed = checkForSpoofedElements(html);
          htmlAnalysis = spoofed;
          
          if (spoofed.hiddenElements > 0) {
            totalScore += spoofed.hiddenElements * 0.5;
            indicatorsFound.push({
              text: `${spoofed.hiddenElements} elementos ocultos detectados`,
              category: 'Elementos ocultos',
              score: spoofed.hiddenElements * 0.5
            });
          }
          
          if (spoofed.mouseoverEvents > 0) {
            totalScore += spoofed.mouseoverEvents * 1.0;
            indicatorsFound.push({
              text: `${spoofed.mouseoverEvents} eventos de mouseover sospechosos`,
              category: 'Comportamiento sospechoso',
              score: spoofed.mouseoverEvents * 1.0
            });
          }
        }
      });
    } catch (e) {
      console.error('Error analyzing HTML:', e);
    }
  }

  // Integrate NLP analysis results
  const nlpScore = (sentimentAnalysis.overallRisk + entityAnalysis.overallRisk) * 0.4; // Weight NLP at 40%
  totalScore += nlpScore;

  // Add NLP indicators to the main indicators list
  if (sentimentAnalysis.indicators) {
    sentimentAnalysis.indicators.forEach(indicator => {
      indicatorsFound.push({
        text: indicator.description,
        category: `NLP: ${indicator.type}`,
        score: indicator.score
      });
    });
  }

  if (entityAnalysis.indicators) {
    entityAnalysis.indicators.forEach(indicator => {
      indicatorsFound.push({
        text: indicator.description,
        category: `NLP: ${indicator.type}`,
        score: indicator.score
      });
    });
  }

  // Calculate risk level with more granularity (including NLP)
  let riskLevel = 'Bajo';
  let confidence = 'baja';
  
  if (totalScore > 10) {
    riskLevel = 'Muy Alto';
    confidence = 'muy alta';
  } else if (totalScore > 7) {
    riskLevel = 'Alto';
    confidence = 'alta';
  } else if (totalScore > 4) {
    riskLevel = 'Medio';
    confidence = 'media';
  } else if (totalScore > 2) {
    riskLevel = 'Bajo';
    confidence = 'baja';
  } else {
    riskLevel = 'Mínimo';
    confidence = 'mínima';
  }

  // Send result to content script with NLP data
  chrome.tabs.sendMessage(tab.id, {
    action: 'showPhishingResult',
    score: totalScore,
    riskLevel,
    indicators: [...new Set(indicatorsFound)],
    analyzedText: text,
    nlpAnalysis: {
      sentiment: sentimentAnalysis,
      entities: entityAnalysis,
      combinedScore: nlpScore
    }
  });

  // Enviar reporte a la API de Django si el riesgo es medio o superior
  if (totalScore >= 5) {
    sendReportToAPI(tab.url, totalScore, indicatorsFound, sentimentAnalysis, entityAnalysis, text);
  }
}

// Función para enviar reportes a la API de Django
async function sendReportToAPI(url, riskScore, indicators, sentimentAnalysis, entityAnalysis, pageContent) {
  try {
    const API_URL = 'http://localhost:8000/api/phishing/report/';
    
    // Determinar nivel de riesgo
    let riskLevel = 'LOW';
    if (riskScore >= 12) riskLevel = 'CRITICAL';
    else if (riskScore >= 8) riskLevel = 'HIGH';
    else if (riskScore >= 5) riskLevel = 'MEDIUM';
    
    // Preparar indicadores
    const indicatorsObj = {};
    indicators.forEach(ind => {
      const key = ind.category.toLowerCase().replace(/\s+/g, '_').replace(/:/g, '');
      indicatorsObj[key] = true;
    });
    
    // Preparar análisis NLP
    const nlpAnalysis = {
      urgency_score: sentimentAnalysis?.urgencyScore || 0,
      threat_language: sentimentAnalysis?.threatScore || 0,
      brand_impersonation: entityAnalysis?.brandDetected || null,
      manipulation_tactics: sentimentAnalysis?.tactics || []
    };
    
    const reportData = {
      url: url,
      risk_score: riskScore,
      risk_level: riskLevel,
      user_email: null,
      user_agent: navigator.userAgent,
      ip_address: null,
      indicators: indicatorsObj,
      nlp_analysis: nlpAnalysis,
      page_content: pageContent.substring(0, 500) // Limitar tamaño
    };
    
    console.log('📤 Enviando reporte a Django:', reportData);
    
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(reportData)
    });
    
    const result = await response.json();
    
    if (response.ok && result.success) {
      console.log('✅ Reporte enviado exitosamente:', result);
      // Mostrar notificación al usuario
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icon128.png',
        title: 'Reporte Enviado',
        message: `Reporte de phishing guardado (ID: ${result.report_id})`
      });
    } else {
      console.error('❌ Error al enviar reporte:', result);
    }
  } catch (error) {
    console.error('Error de conexion con la API:', error);
  }
}
