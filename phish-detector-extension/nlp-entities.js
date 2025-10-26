/**
 * Aegis Code - Named Entity Recognition (NER) Module
 * Lightweight entity detection for phishing brand impersonation
 */

class PhishingEntityDetector {
  constructor() {
    // Base de datos de marcas legítimas y sus variaciones comunes
    this.legitimateBrands = {
      // Bancos españoles y latinoamericanos
      banks: {
        'santander': ['santander', 'banco santander', 'santander bank'],
        'bbva': ['bbva', 'banco bbva', 'bbva bancomer'],
        'bancolombia': ['bancolombia', 'banco de colombia'],
        'banorte': ['banorte', 'banco banorte'],
        'banamex': ['banamex', 'citibanamex'],
        'scotiabank': ['scotiabank', 'banco scotia'],
        'itau': ['itaú', 'banco itaú', 'itau'],
        'bradesco': ['bradesco', 'banco bradesco']
      },
      
      // Servicios tecnológicos
      tech: {
        'google': ['google', 'gmail', 'google pay'],
        'microsoft': ['microsoft', 'outlook', 'hotmail', 'office 365'],
        'apple': ['apple', 'icloud', 'app store', 'itunes'],
        'amazon': ['amazon', 'aws', 'amazon prime'],
        'facebook': ['facebook', 'meta', 'instagram', 'whatsapp'],
        'paypal': ['paypal', 'paypal holdings'],
        'netflix': ['netflix'],
        'spotify': ['spotify'],
        'uber': ['uber', 'uber eats'],
        'airbnb': ['airbnb']
      },
      
      // Servicios gubernamentales
      government: {
        'hacienda': ['hacienda', 'agencia tributaria', 'aeat'],
        'seguridad_social': ['seguridad social', 'inss'],
        'dgt': ['dgt', 'dirección general de tráfico'],
        'sat': ['sat', 'servicio de administración tributaria']
      }
    };

    // Patrones de typosquatting comunes
    this.typosquattingPatterns = {
      'character_substitution': {
        'o': ['0', 'ο', 'о'], // o, zero, greek omicron, cyrillic o
        'a': ['@', 'α', 'а'], // a, at, greek alpha, cyrillic a
        'e': ['3', 'ε', 'е'], // e, three, greek epsilon, cyrillic e
        'i': ['1', 'l', 'ι', 'і'], // i, one, L, greek iota, cyrillic i
        'u': ['υ', 'μ'], // greek upsilon, mu
        'n': ['η', 'п'], // greek eta, cyrillic p
        'm': ['м'], // cyrillic m
        'p': ['ρ', 'р'], // greek rho, cyrillic p
        'c': ['с'], // cyrillic c
        'x': ['х'], // cyrillic x
        'y': ['у'], // cyrillic y
        'h': ['н'], // cyrillic h
        'b': ['в'], // cyrillic b
        'k': ['к'], // cyrillic k
        't': ['т'], // cyrillic t
        'r': ['г'] // cyrillic r
      },
      
      'common_misspellings': {
        'paypal': ['paypall', 'paypa1', 'paypai', 'payapl', 'paipal'],
        'google': ['goggle', 'gooogle', 'g00gle', 'go0gle', 'googel'],
        'microsoft': ['micr0soft', 'micros0ft', 'microsooft', 'microsft'],
        'facebook': ['facebok', 'facebo0k', 'facebock', 'faceebook'],
        'amazon': ['amaz0n', 'amazom', 'amazone', 'ammazon'],
        'netflix': ['netflex', 'netflx', 'netflixx', 'neflix'],
        'santander': ['santandar', 'santader', 'santanderr', 'santanderr']
      }
    };

    // Patrones de contexto sospechoso
    this.suspiciousContexts = [
      /(?:soporte|servicio|atención)\s+(?:al\s+)?cliente/gi,
      /departamento\s+de\s+seguridad/gi,
      /centro\s+de\s+verificación/gi,
      /equipo\s+de\s+soporte/gi,
      /servicio\s+técnico/gi,
      /centro\s+de\s+ayuda/gi
    ];
  }

  /**
   * Detecta entidades y analiza posible suplantación de marca
   * @param {string} text - Texto a analizar
   * @returns {Object} Análisis de entidades y riesgo de suplantación
   */
  analyzeEntities(text) {
    const analysis = {
      detectedBrands: [],
      suspiciousBrands: [],
      typosquattingAttempts: [],
      contextualRisk: 0,
      overallRisk: 0,
      indicators: []
    };

    // Detectar marcas legítimas mencionadas
    this.detectLegitimateEntities(text, analysis);
    
    // Detectar posibles intentos de typosquatting
    this.detectTyposquatting(text, analysis);
    
    // Analizar contexto sospechoso
    this.analyzeContext(text, analysis);
    
    // Calcular riesgo general
    this.calculateEntityRisk(analysis);
    
    return analysis;
  }

  /**
   * Detecta menciones de marcas legítimas
   */
  detectLegitimateEntities(text, analysis) {
    const lowerText = text.toLowerCase();
    
    Object.entries(this.legitimateBrands).forEach(([category, brands]) => {
      Object.entries(brands).forEach(([brandKey, variations]) => {
        variations.forEach(variation => {
          const regex = new RegExp(`\\b${this.escapeRegExp(variation)}\\b`, 'gi');
          const matches = text.match(regex);
          
          if (matches) {
            analysis.detectedBrands.push({
              brand: brandKey,
              category: category,
              variation: variation,
              matches: matches,
              count: matches.length,
              positions: this.findPositions(text, variation)
            });
          }
        });
      });
    });
  }

  /**
   * Detecta intentos de typosquatting
   */
  detectTyposquatting(text, analysis) {
    const lowerText = text.toLowerCase();
    
    // Buscar misspellings comunes
    Object.entries(this.typosquattingPatterns.common_misspellings).forEach(([legitimate, misspellings]) => {
      misspellings.forEach(misspelling => {
        const regex = new RegExp(`\\b${this.escapeRegExp(misspelling)}\\b`, 'gi');
        const matches = text.match(regex);
        
        if (matches) {
          analysis.typosquattingAttempts.push({
            type: 'common_misspelling',
            detected: misspelling,
            legitimate: legitimate,
            matches: matches,
            count: matches.length,
            riskScore: 2.5
          });
        }
      });
    });

    // Buscar sustituciones de caracteres
    this.detectCharacterSubstitution(text, analysis);
  }

  /**
   * Detecta sustituciones de caracteres sospechosas
   */
  detectCharacterSubstitution(text, analysis) {
    Object.entries(this.legitimateBrands).forEach(([category, brands]) => {
      Object.keys(brands).forEach(brandKey => {
        // Generar variaciones con sustitución de caracteres
        const suspiciousVariations = this.generateSuspiciousVariations(brandKey);
        
        suspiciousVariations.forEach(variation => {
          const regex = new RegExp(`\\b${this.escapeRegExp(variation)}\\b`, 'gi');
          const matches = text.match(regex);
          
          if (matches) {
            analysis.typosquattingAttempts.push({
              type: 'character_substitution',
              detected: variation,
              legitimate: brandKey,
              matches: matches,
              count: matches.length,
              riskScore: 3.0
            });
          }
        });
      });
    });
  }

  /**
   * Genera variaciones sospechosas de una marca usando sustitución de caracteres
   */
  generateSuspiciousVariations(brand) {
    const variations = [];
    const substitutions = this.typosquattingPatterns.character_substitution;
    
    // Generar hasta 5 variaciones por marca para no sobrecargar
    let count = 0;
    for (let i = 0; i < brand.length && count < 5; i++) {
      const char = brand[i].toLowerCase();
      if (substitutions[char]) {
        substitutions[char].forEach(substitute => {
          if (count < 5) {
            const variation = brand.substring(0, i) + substitute + brand.substring(i + 1);
            variations.push(variation);
            count++;
          }
        });
      }
    }
    
    return variations;
  }

  /**
   * Analiza el contexto para detectar patrones sospechosos
   */
  analyzeContext(text, analysis) {
    let contextRisk = 0;
    const contextIndicators = [];

    this.suspiciousContexts.forEach(pattern => {
      const matches = text.match(pattern);
      if (matches) {
        contextRisk += matches.length * 1.5;
        contextIndicators.push({
          pattern: pattern.source,
          matches: matches,
          count: matches.length
        });
      }
    });

    // Si hay marcas detectadas + contexto sospechoso = mayor riesgo
    if (analysis.detectedBrands.length > 0 && contextIndicators.length > 0) {
      contextRisk *= 1.8; // Multiplicador por combinación peligrosa
    }

    analysis.contextualRisk = Math.min(contextRisk, 10);
    
    if (contextIndicators.length > 0) {
      analysis.indicators.push({
        type: 'suspicious_context',
        score: analysis.contextualRisk,
        patterns: contextIndicators,
        description: `Detectado contexto sospechoso de suplantación`
      });
    }
  }

  /**
   * Calcula el riesgo general de suplantación de entidades
   */
  calculateEntityRisk(analysis) {
    let risk = 0;

    // Riesgo por typosquatting
    analysis.typosquattingAttempts.forEach(attempt => {
      risk += attempt.riskScore;
    });

    // Riesgo por contexto
    risk += analysis.contextualRisk * 0.6;

    // Riesgo adicional si hay múltiples marcas mencionadas (inusual)
    if (analysis.detectedBrands.length > 2) {
      risk += analysis.detectedBrands.length * 0.5;
    }

    // Riesgo adicional si hay typosquatting + marcas legítimas
    if (analysis.typosquattingAttempts.length > 0 && analysis.detectedBrands.length > 0) {
      risk *= 1.4;
    }

    analysis.overallRisk = Math.min(risk, 10);

    // Agregar indicadores principales
    if (analysis.typosquattingAttempts.length > 0) {
      analysis.indicators.push({
        type: 'typosquatting',
        score: analysis.typosquattingAttempts.reduce((sum, att) => sum + att.riskScore, 0),
        attempts: analysis.typosquattingAttempts,
        description: `Detectados ${analysis.typosquattingAttempts.length} intentos de typosquatting`
      });
    }

    if (analysis.detectedBrands.length > 0) {
      analysis.indicators.push({
        type: 'brand_mentions',
        score: analysis.detectedBrands.length * 0.8,
        brands: analysis.detectedBrands,
        description: `Detectadas ${analysis.detectedBrands.length} menciones de marcas conocidas`
      });
    }
  }

  /**
   * Encuentra las posiciones de una palabra en el texto
   */
  findPositions(text, word) {
    const positions = [];
    const regex = new RegExp(`\\b${this.escapeRegExp(word)}\\b`, 'gi');
    let match;
    
    while ((match = regex.exec(text)) !== null) {
      positions.push({
        start: match.index,
        end: match.index + match[0].length,
        context: text.substring(Math.max(0, match.index - 20), match.index + match[0].length + 20)
      });
    }
    
    return positions;
  }

  /**
   * Escapa caracteres especiales para regex
   */
  escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  /**
   * Obtiene una interpretación legible del análisis de entidades
   */
  getReadableAnalysis(analysis) {
    let riskLevel = 'Bajo';
    let description = '';

    if (analysis.overallRisk > 7) {
      riskLevel = 'Muy Alto';
      description = 'Detectados múltiples intentos de suplantación de marca.';
    } else if (analysis.overallRisk > 5) {
      riskLevel = 'Alto';
      description = 'Posible intento de suplantación de marca detectado.';
    } else if (analysis.overallRisk > 3) {
      riskLevel = 'Medio';
      description = 'Algunas inconsistencias en nombres de marca detectadas.';
    } else if (analysis.overallRisk > 1) {
      riskLevel = 'Bajo';
      description = 'Menciones de marcas detectadas, contexto normal.';
    } else {
      riskLevel = 'Mínimo';
      description = 'No se detectaron intentos de suplantación.';
    }

    return {
      riskLevel,
      description,
      score: analysis.overallRisk,
      mainFindings: [
        ...analysis.typosquattingAttempts.map(att => `Posible typosquatting: "${att.detected}" (debería ser "${att.legitimate}")`),
        ...analysis.detectedBrands.map(brand => `Marca detectada: ${brand.brand} (${brand.category})`)
      ]
    };
  }
}

// Exportar para uso en la extensión (compatible con service workers)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PhishingEntityDetector;
}
// En service workers no hay window, la clase ya esta en el scope global
