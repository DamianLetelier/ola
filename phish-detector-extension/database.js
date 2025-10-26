/**
 * Aegis Code - IndexedDB Database Manager
 * Local storage for phishing reports
 */

class AegisDatabase {
  constructor() {
    this.dbName = 'AegisPhishingReports';
    this.version = 1;
    this.db = null;
  }

  /**
   * Initialize the database
   */
  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);

      request.onerror = () => {
        console.error('❌ Error opening database:', request.error);
        reject(request.error);
      };

      request.onsuccess = () => {
        this.db = request.result;
        console.log('✅ Database initialized successfully');
        resolve(this.db);
      };

      request.onupgradeneeded = (event) => {
        const db = event.target.result;

        // Create reports object store
        if (!db.objectStoreNames.contains('reports')) {
          const objectStore = db.createObjectStore('reports', {
            keyPath: 'id',
            autoIncrement: true
          });

          // Create indexes
          objectStore.createIndex('timestamp', 'timestamp', { unique: false });
          objectStore.createIndex('url', 'url', { unique: false });
          objectStore.createIndex('riskLevel', 'riskLevel', { unique: false });
          objectStore.createIndex('category', 'category', { unique: false });

          console.log('📦 Object store "reports" created');
        }
      };
    });
  }

  /**
   * Save a report to the database
   */
  async saveReport(reportData) {
    if (!this.db) {
      await this.init();
    }

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['reports'], 'readwrite');
      const objectStore = transaction.objectStore('reports');

      // Add metadata
      const report = {
        ...reportData,
        savedAt: new Date().toISOString(),
        synced: false
      };

      const request = objectStore.add(report);

      request.onsuccess = () => {
        console.log('✅ Report saved to database with ID:', request.result);
        resolve(request.result);
      };

      request.onerror = () => {
        console.error('❌ Error saving report:', request.error);
        reject(request.error);
      };
    });
  }

  /**
   * Get all reports
   */
  async getAllReports() {
    if (!this.db) {
      await this.init();
    }

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['reports'], 'readonly');
      const objectStore = transaction.objectStore('reports');
      const request = objectStore.getAll();

      request.onsuccess = () => {
        resolve(request.result);
      };

      request.onerror = () => {
        reject(request.error);
      };
    });
  }

  /**
   * Get reports by risk level
   */
  async getReportsByRiskLevel(riskLevel) {
    if (!this.db) {
      await this.init();
    }

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['reports'], 'readonly');
      const objectStore = transaction.objectStore('reports');
      const index = objectStore.index('riskLevel');
      const request = index.getAll(riskLevel);

      request.onsuccess = () => {
        resolve(request.result);
      };

      request.onerror = () => {
        reject(request.error);
      };
    });
  }

  /**
   * Get recent reports (last N days)
   */
  async getRecentReports(days = 7) {
    if (!this.db) {
      await this.init();
    }

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['reports'], 'readonly');
      const objectStore = transaction.objectStore('reports');
      const index = objectStore.index('timestamp');
      const request = index.openCursor(null, 'prev');

      const results = [];

      request.onsuccess = (event) => {
        const cursor = event.target.result;
        if (cursor) {
          const report = cursor.value;
          const reportDate = new Date(report.timestamp);
          
          if (reportDate >= cutoffDate) {
            results.push(report);
            cursor.continue();
          } else {
            resolve(results);
          }
        } else {
          resolve(results);
        }
      };

      request.onerror = () => {
        reject(request.error);
      };
    });
  }

  /**
   * Delete a report by ID
   */
  async deleteReport(id) {
    if (!this.db) {
      await this.init();
    }

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['reports'], 'readwrite');
      const objectStore = transaction.objectStore('reports');
      const request = objectStore.delete(id);

      request.onsuccess = () => {
        console.log('✅ Report deleted:', id);
        resolve();
      };

      request.onerror = () => {
        reject(request.error);
      };
    });
  }

  /**
   * Get database statistics
   */
  async getStats() {
    if (!this.db) {
      await this.init();
    }

    const allReports = await this.getAllReports();
    
    const stats = {
      total: allReports.length,
      byRiskLevel: {
        'Muy Alto': 0,
        'Alto': 0,
        'Medio': 0,
        'Bajo': 0,
        'Mínimo': 0
      },
      byCategory: {},
      lastReport: null
    };

    allReports.forEach(report => {
      // Count by risk level
      if (stats.byRiskLevel[report.riskLevel] !== undefined) {
        stats.byRiskLevel[report.riskLevel]++;
      }

      // Count by category
      if (report.category) {
        stats.byCategory[report.category] = (stats.byCategory[report.category] || 0) + 1;
      }

      // Find last report
      if (!stats.lastReport || new Date(report.timestamp) > new Date(stats.lastReport.timestamp)) {
        stats.lastReport = report;
      }
    });

    return stats;
  }

  /**
   * Export all reports as JSON
   */
  async exportReports() {
    const reports = await this.getAllReports();
    const dataStr = JSON.stringify(reports, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `aegis-reports-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    
    URL.revokeObjectURL(url);
  }

  /**
   * Clear all reports (with confirmation)
   */
  async clearAllReports() {
    if (!this.db) {
      await this.init();
    }

    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(['reports'], 'readwrite');
      const objectStore = transaction.objectStore('reports');
      const request = objectStore.clear();

      request.onsuccess = () => {
        console.log('✅ All reports cleared');
        resolve();
      };

      request.onerror = () => {
        reject(request.error);
      };
    });
  }
}

// Create global database instance
const aegisDB = new AegisDatabase();

// Initialize on load
aegisDB.init().catch(err => {
  console.error('Failed to initialize database:', err);
});

// Export for use in content script
if (typeof window !== 'undefined') {
  window.aegisDB = aegisDB;
}

// Helper function for content script
async function saveReportToDatabase(reportData) {
  try {
    const id = await aegisDB.saveReport(reportData);
    console.log('📊 Report saved to local database with ID:', id);
    return id;
  } catch (error) {
    console.error('❌ Error saving to database:', error);
    throw error;
  }
}

// Export helper
if (typeof window !== 'undefined') {
  window.saveReportToDatabase = saveReportToDatabase;
}
