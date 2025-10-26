/**
 * API Reporter Module
 * Envía reportes de phishing al servidor Django
 */

class PhishingAPIReporter {
    constructor() {
        // URL del servidor Django (cambiar según configuración)
        this.API_URL = 'http://localhost:8000/api/phishing/report/';
        this.STATS_URL = 'http://localhost:8000/api/phishing/stats/';
    }

    /**
     * Determina el nivel de riesgo basado en la puntuación
     */
    getRiskLevel(riskScore) {
        if (riskScore >= 12) return 'CRITICAL';
        if (riskScore >= 8) return 'HIGH';
        if (riskScore >= 5) return 'MEDIUM';
        return 'LOW';
    }

    /**
     * Envía un reporte de phishing al servidor
     */
    async sendReport(analysisData) {
        try {
            const reportData = {
                url: analysisData.url,
                risk_score: analysisData.riskScore || 0,
                risk_level: this.getRiskLevel(analysisData.riskScore || 0),
                user_email: analysisData.userEmail || null,
                user_agent: navigator.userAgent,
                ip_address: null, // Se obtendrá en el servidor
                indicators: analysisData.indicators || {},
                nlp_analysis: analysisData.nlpAnalysis || {},
                page_content: analysisData.pageContent || ''
            };

            console.log('Enviando reporte a Django:', reportData);

            const response = await fetch(this.API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(reportData)
            });

            const result = await response.json();

            if (response.ok && result.success) {
                console.log('✅ Reporte enviado exitosamente:', result);
                return {
                    success: true,
                    reportId: result.report_id,
                    message: result.message
                };
            } else {
                console.error('❌ Error al enviar reporte:', result);
                return {
                    success: false,
                    error: result.message || 'Error desconocido'
                };
            }
        } catch (error) {
            console.error('❌ Error de conexión:', error);
            return {
                success: false,
                error: `Error de conexión: ${error.message}`
            };
        }
    }

    /**
     * Obtiene estadísticas del servidor
     */
    async getStats() {
        try {
            const response = await fetch(this.STATS_URL);
            const result = await response.json();

            if (response.ok && result.success) {
                return {
                    success: true,
                    stats: result.stats
                };
            } else {
                return {
                    success: false,
                    error: result.message || 'Error al obtener estadísticas'
                };
            }
        } catch (error) {
            console.error('Error al obtener estadísticas:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Configura la URL del servidor
     */
    setServerURL(url) {
        this.API_URL = `${url}/api/phishing/report/`;
        this.STATS_URL = `${url}/api/phishing/stats/`;
    }
}

// Exportar para uso en otros módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PhishingAPIReporter };
}
