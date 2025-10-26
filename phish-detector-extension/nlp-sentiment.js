/**
 * Aegis Code - NLP Sentiment Analysis Module
 * Lightweight sentiment analysis for phishing detection
 * Focuses on detecting artificial urgency and emotional manipulation
 */

class PhishingSentimentAnalyzer {
  constructor() {
    // Palabras que indican urgencia artificial (común en phishing)
    this.urgencyWords = {
      high: ['urgente', 'inmediato', 'ahora', 'ya', 'rápido', 'pronto', 'inmediatamente', 'cuanto antes'],
      medium: ['importante', 'necesario', 'requerido', 'debe', 'tiene que', 'obligatorio'],
      temporal: ['hoy', 'mañana', '24 horas', 'esta semana', 'antes de', 'hasta', 'plazo', 'vence', 'expira']
    };

    // Palabras que indican amenazas (típicas del phishing)
    this.threatWords = {
      direct: ['suspender', 'bloquear', 'cerrar', 'eliminar', 'cancelar', 'desactivar'],
      consequences: ['perder', 'pérdida', 'problema', 'inconveniente', 'multa', 'penalización'],
      legal: ['legal', 'demanda', 'tribunal', 'abogado', 'policía', 'autoridades']
    };

    // Palabras que indican solicitud de información sensible
    this.sensitiveRequestWords = {
      credentials: ['contraseña', 'password', 'clave', 'pin', 'código', 'usuario', 'login'],
      financial: ['tarjeta', 'cuenta', 'banco', 'dinero', 'pago', 'transferencia', 'cvv', 'número'],
      personal: ['dni', 'cedula', 'pasaporte', 'seguro social', 'fecha nacimiento', 'dirección']
    };

    // Palabras positivas que pueden ser usadas para manipular
    this.manipulativePositiveWords = [
      'gratis', 'regalo', 'premio', 'ganador', 'felicidades', 'seleccionado', 'exclusivo', 'especial'
    ];

    // Patrones de manipulación emocional
    this.emotionalManipulationPatterns = [
      /su cuenta (será|va a ser|se) (suspendida|bloqueada|cerrada)/gi,
      /última (oportunidad|advertencia|aviso)/gi,
      /acción (inmediata|urgente) requerida/gi,
      /verificar? (inmediatamente|ahora|ya)/gi,
      /problema (grave|serio|importante) con su cuenta/gi
    ];
  }

  /**
   * Analiza el sentimiento y detecta manipulación emocional en el texto
   * @param {string} text - Texto a analizar
   * @returns {Object} Análisis completo del sentimiento y manipulación
   */
  analyzeSentiment(text) {
    const lowerText = text.toLowerCase();
    const words = lowerText.split(/\s+/);
    
    const analysis = {
      urgencyScore: 0,
      threatScore: 0,
      manipulationScore: 0,
      sensitiveRequestScore: 0,
      overallRisk: 0,
      indicators: [],
      emotionalManipulation: [],
      wordCount: words.length,
      sentenceCount: text.split(/[.!?]+/).length
    };

    // Analizar urgencia
    this.analyzeUrgency(words, lowerText, analysis);
    
    // Analizar amenazas
    this.analyzeThreats(words, lowerText, analysis);
    
    // Analizar solicitudes de información sensible
    this.analyzeSensitiveRequests(words, lowerText, analysis);
    
    // Analizar manipulación emocional
    this.analyzeEmotionalManipulation(text, analysis);
    
    // Calcular puntuación general
    this.calculateOverallRisk(analysis);
    
    return analysis;
  }

  /**
   * Analiza indicadores de urgencia artificial
   */
  analyzeUrgency(words, text, analysis) {
    let urgencyCount = 0;
    let urgencyWords = [];

    // Contar palabras de urgencia alta
    this.urgencyWords.high.forEach(word => {
      const count = (text.match(new RegExp(`\\b${word}\\b`, 'gi')) || []).length;
      if (count > 0) {
        urgencyCount += count * 2; // Peso alto
        urgencyWords.push({ word, count, weight: 'high' });
      }
    });

    // Contar palabras de urgencia media
    this.urgencyWords.medium.forEach(word => {
      const count = (text.match(new RegExp(`\\b${word}\\b`, 'gi')) || []).length;
      if (count > 0) {
        urgencyCount += count * 1.5;
        urgencyWords.push({ word, count, weight: 'medium' });
      }
    });

    // Contar indicadores temporales
    this.urgencyWords.temporal.forEach(word => {
      const count = (text.match(new RegExp(`\\b${word}\\b`, 'gi')) || []).length;
      if (count > 0) {
        urgencyCount += count;
        urgencyWords.push({ word, count, weight: 'temporal' });
      }
    });

    analysis.urgencyScore = Math.min(urgencyCount / words.length * 100, 10);
    
    if (urgencyWords.length > 0) {
      analysis.indicators.push({
        type: 'urgency',
        score: analysis.urgencyScore,
        words: urgencyWords,
        description: `Detectadas ${urgencyWords.length} palabras de urgencia artificial`
      });
    }
  }

  /**
   * Analiza indicadores de amenazas
   */
  analyzeThreats(words, text, analysis) {
    let threatCount = 0;
    let threatWords = [];

    // Amenazas directas
    this.threatWords.direct.forEach(word => {
      const count = (text.match(new RegExp(`\\b${word}\\b`, 'gi')) || []).length;
      if (count > 0) {
        threatCount += count * 2;
        threatWords.push({ word, count, type: 'direct' });
      }
    });

    // Consecuencias negativas
    this.threatWords.consequences.forEach(word => {
      const count = (text.match(new RegExp(`\\b${word}\\b`, 'gi')) || []).length;
      if (count > 0) {
        threatCount += count * 1.5;
        threatWords.push({ word, count, type: 'consequences' });
      }
    });

    // Referencias legales
    this.threatWords.legal.forEach(word => {
      const count = (text.match(new RegExp(`\\b${word}\\b`, 'gi')) || []).length;
      if (count > 0) {
        threatCount += count * 1.8;
        threatWords.push({ word, count, type: 'legal' });
      }
    });

    analysis.threatScore = Math.min(threatCount / words.length * 100, 10);
    
    if (threatWords.length > 0) {
      analysis.indicators.push({
        type: 'threats',
        score: analysis.threatScore,
        words: threatWords,
        description: `Detectadas ${threatWords.length} palabras amenazantes`
      });
    }
  }

  /**
   * Analiza solicitudes de información sensible
   */
  analyzeSensitiveRequests(words, text, analysis) {
    let sensitiveCount = 0;
    let sensitiveWords = [];

    Object.entries(this.sensitiveRequestWords).forEach(([category, wordList]) => {
      wordList.forEach(word => {
        const count = (text.match(new RegExp(`\\b${word}\\b`, 'gi')) || []).length;
        if (count > 0) {
          const weight = category === 'credentials' ? 2.5 : category === 'financial' ? 2 : 1.5;
          sensitiveCount += count * weight;
          sensitiveWords.push({ word, count, category });
        }
      });
    });

    analysis.sensitiveRequestScore = Math.min(sensitiveCount / words.length * 100, 10);
    
    if (sensitiveWords.length > 0) {
      analysis.indicators.push({
        type: 'sensitive_requests',
        score: analysis.sensitiveRequestScore,
        words: sensitiveWords,
        description: `Detectadas ${sensitiveWords.length} solicitudes de información sensible`
      });
    }
  }

  /**
   * Analiza patrones de manipulación emocional
   */
  analyzeEmotionalManipulation(text, analysis) {
    let manipulationScore = 0;
    let patterns = [];

    // Buscar patrones de manipulación
    this.emotionalManipulationPatterns.forEach((pattern, index) => {
      const matches = text.match(pattern);
      if (matches) {
        manipulationScore += matches.length * 2;
        patterns.push({
          pattern: pattern.source,
          matches: matches,
          count: matches.length
        });
      }
    });

    // Buscar palabras manipulativas positivas (ofertas falsas)
    this.manipulativePositiveWords.forEach(word => {
      const count = (text.toLowerCase().match(new RegExp(`\\b${word}\\b`, 'gi')) || []).length;
      if (count > 0) {
        manipulationScore += count * 1.5;
        patterns.push({
          type: 'false_positive',
          word: word,
          count: count
        });
      }
    });

    analysis.manipulationScore = Math.min(manipulationScore, 10);
    analysis.emotionalManipulation = patterns;
    
    if (patterns.length > 0) {
      analysis.indicators.push({
        type: 'emotional_manipulation',
        score: analysis.manipulationScore,
        patterns: patterns,
        description: `Detectados ${patterns.length} patrones de manipulación emocional`
      });
    }
  }

  /**
   * Calcula la puntuación general de riesgo
   */
  calculateOverallRisk(analysis) {
    // Pesos para cada tipo de análisis
    const weights = {
      urgency: 0.25,
      threats: 0.30,
      manipulation: 0.25,
      sensitiveRequests: 0.20
    };

    analysis.overallRisk = (
      analysis.urgencyScore * weights.urgency +
      analysis.threatScore * weights.threats +
      analysis.manipulationScore * weights.manipulation +
      analysis.sensitiveRequestScore * weights.sensitiveRequests
    );

    // Ajustar por densidad (textos cortos con muchos indicadores son más sospechosos)
    if (analysis.wordCount < 50 && analysis.indicators.length > 2) {
      analysis.overallRisk *= 1.3;
    }

    // Ajustar por múltiples tipos de manipulación
    if (analysis.indicators.length > 3) {
      analysis.overallRisk *= 1.2;
    }

    analysis.overallRisk = Math.min(analysis.overallRisk, 10);
  }

  /**
   * Obtiene una interpretación legible del análisis
   */
  getReadableAnalysis(analysis) {
    let riskLevel = 'Bajo';
    let description = '';

    if (analysis.overallRisk > 7) {
      riskLevel = 'Muy Alto';
      description = 'El texto presenta múltiples indicadores de manipulación emocional típicos del phishing.';
    } else if (analysis.overallRisk > 5) {
      riskLevel = 'Alto';
      description = 'El texto contiene varios patrones sospechosos de manipulación.';
    } else if (analysis.overallRisk > 3) {
      riskLevel = 'Medio';
      description = 'Se detectaron algunos indicadores de posible manipulación.';
    } else if (analysis.overallRisk > 1) {
      riskLevel = 'Bajo';
      description = 'Pocos indicadores de riesgo detectados.';
    } else {
      riskLevel = 'Mínimo';
      description = 'El texto no presenta indicadores significativos de manipulación.';
    }

    return {
      riskLevel,
      description,
      score: analysis.overallRisk,
      mainConcerns: analysis.indicators.map(i => i.description)
    };
  }
}

// Exportar para uso en la extensión (compatible con service workers)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PhishingSentimentAnalyzer;
}
// En service workers no hay window, la clase ya esta en el scope global
