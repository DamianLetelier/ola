/**
 * Aegis Security Suite - Popup Dashboard
 * Reports are sent to API, not stored locally
 */

document.addEventListener('DOMContentLoaded', function() {
  console.log('🛡️ Aegis Security Suite loaded');
  
  // Setup event listeners
  document.getElementById('refresh-stats').addEventListener('click', refreshStats);
  
  // Show initial message
  updateStatsDisplay();
});

// Update stats display
function updateStatsDisplay() {
  // Since reports are sent to API and not stored locally,
  // we show a message that stats are managed server-side
  document.getElementById('total-reports').textContent = '-';
  document.getElementById('high-risk').textContent = '-';
}

// Refresh stats button
function refreshStats() {
  const btn = document.getElementById('refresh-stats');
  const originalText = btn.textContent;
  
  btn.textContent = '⏳ Actualizando...';
  btn.disabled = true;
  
  // Simulate refresh
  setTimeout(() => {
    updateStatsDisplay();
    btn.textContent = '✅ Actualizado';
    
    setTimeout(() => {
      btn.textContent = originalText;
      btn.disabled = false;
    }, 1000);
  }, 500);
}
