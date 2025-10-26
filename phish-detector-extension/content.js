// Inject premium CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideInRight {
    from {
      opacity: 0;
      transform: translateX(100px) scale(0.95);
    }
    to {
      opacity: 1;
      transform: translateX(0) scale(1);
    }
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
  }
  
  @keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
  }
  
  #phish-detector-result::-webkit-scrollbar {
    width: 8px;
  }
  
  #phish-detector-result::-webkit-scrollbar-track {
    background: rgba(0,0,0,0.05);
    border-radius: 10px;
  }
  
  #phish-detector-result::-webkit-scrollbar-thumb {
    background: rgba(0,0,0,0.2);
    border-radius: 10px;
  }
  
  #phish-detector-result::-webkit-scrollbar-thumb:hover {
    background: rgba(0,0,0,0.3);
  }
`;
document.head.appendChild(style);

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'showPhishingResult') {
    showPhishingResult(request);
  }
});

// Helper function to create element with attributes
function createElement(tag, attributes = {}, text = '') {
  const el = document.createElement(tag);
  Object.entries(attributes).forEach(([key, value]) => {
    el[key] = value;
  });
  if (text) el.textContent = text;
  return el;
}

// Helper function to get risk level color
function getRiskColor(riskLevel) {
  const colors = {
    'Muy Alto': { bg: '#ffebee', border: '#f44336', text: '#d32f2f' },
    'Alto': { bg: '#ffebee', border: '#f44336', text: '#d32f2f' },
    'Medio': { bg: '#fff3e0', border: '#ff9800', text: '#f57c00' },
    'Bajo': { bg: '#e8f5e9', border: '#4caf50', text: '#388e3c' },
    'Mínimo': { bg: '#e8f5e9', border: '#4caf50', text: '#388e3c' }
  };
  return colors[riskLevel] || colors['Bajo'];
}

// Show the phishing analysis result with PREMIUM UI
function showPhishingResult(data) {
  // Remove any existing results
  const existingResult = document.getElementById('phish-detector-result');
  if (existingResult) {
    existingResult.remove();
  }

  // Get risk level colors
  const colors = getRiskColor(data.riskLevel);
  
  // Create main container with PREMIUM styling
  const result = createElement('div', {
    id: 'phish-detector-result',
    style: `
      position: fixed;
      top: 20px;
      right: 20px;
      width: 420px;
      max-height: 85vh;
      overflow: hidden;
      background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
      border: 1px solid rgba(0,0,0,0.08);
      border-left: 5px solid ${colors.border};
      border-radius: 16px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.25), 0 0 0 1px rgba(255,255,255,0.5) inset;
      z-index: 10000;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
      font-size: 14px;
      line-height: 1.6;
      color: #1a1a1a;
      backdrop-filter: blur(10px);
      animation: slideInRight 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    `
  });

  // Create PREMIUM header with gradient
  const header = createElement('div', {
    style: `
      display: flex;
      align-items: center;
      padding: 18px 20px;
      background: linear-gradient(135deg, ${colors.bg} 0%, ${colors.bg}dd 100%);
      border-top-left-radius: 15px;
      border-top-right-radius: 15px;
      border-bottom: 2px solid ${colors.border}40;
      position: relative;
      overflow: hidden;
    `
  });
  
  // Add premium shine effect
  const shine = createElement('div', {
    style: `
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
      animation: shimmer 3s infinite;
    `
  });
  header.appendChild(shine);
  
  // Add Aegis logo with premium styling
  const logo = createElement('img', {
    src: chrome.runtime.getURL('images/icon48.png'),
    style: `
      width: 36px;
      height: 36px;
      margin-right: 14px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      border: 2px solid rgba(255,255,255,0.8);
      position: relative;
      z-index: 1;
    `
  });
  
  // Add premium title with badge
  const titleContainer = createElement('div', {
    style: 'flex: 1; position: relative; z-index: 1;'
  });
  
  const title = createElement('h3', {
    style: `
      margin: 0 0 4px 0;
      font-size: 18px;
      color: ${colors.text};
      font-weight: 700;
      letter-spacing: -0.3px;
    `,
    textContent: 'Aegis Security Suite'
  });
  
  const badge = createElement('div', {
    style: `
      display: inline-block;
      padding: 3px 10px;
      background: ${colors.border};
      color: white;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      box-shadow: 0 2px 8px ${colors.border}60;
    `,
    textContent: `${data.riskLevel} Riesgo`
  });
  
  titleContainer.append(title, badge);
  
  // Add premium close button
  const closeButton = createElement('button', {
    style: `
      background: rgba(0,0,0,0.05);
      border: none;
      font-size: 24px;
      cursor: pointer;
      color: #666666;
      padding: 0;
      line-height: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 32px;
      height: 32px;
      border-radius: 8px;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      z-index: 1;
    `,
    textContent: '×',
    onclick: () => {
      result.style.animation = 'slideInRight 0.3s cubic-bezier(0.4, 0, 1, 1) reverse';
      setTimeout(() => result.remove(), 300);
    }
  });
  
  closeButton.onmouseover = () => {
    closeButton.style.backgroundColor = 'rgba(244, 67, 54, 0.1)';
    closeButton.style.color = '#f44336';
    closeButton.style.transform = 'rotate(90deg) scale(1.1)';
  };
  
  closeButton.onmouseout = () => {
    closeButton.style.backgroundColor = 'rgba(0,0,0,0.05)';
    closeButton.style.color = '#666666';
    closeButton.style.transform = 'rotate(0deg) scale(1)';
  };
  
  header.append(logo, titleContainer, closeButton);
  
  // Create PREMIUM content container with scrolling
  const contentWrapper = createElement('div', {
    style: `
      max-height: calc(85vh - 100px);
      overflow-y: auto;
      overflow-x: hidden;
    `
  });
  
  const content = createElement('div', {
    style: `
      padding: 20px;
      background-color: #ffffff;
    `
  });
  
  // Add PREMIUM score visualization with gradient progress bar
  const scoreText = createElement('div', {
    style: 'margin-bottom: 24px;',
    innerHTML: `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <span style="font-size: 15px; color: #333; font-weight: 600;">📊 Puntuación de Riesgo</span>
        <span style="font-weight: 700; font-size: 24px; color: ${colors.text}; text-shadow: 0 2px 4px ${colors.border}40;">${data.score.toFixed(1)}<span style="font-size: 14px; opacity: 0.7;">/10</span></span>
      </div>
      <div style="height: 12px; background: linear-gradient(90deg, #e0e0e0 0%, #f5f5f5 100%); border-radius: 20px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1), 0 1px 0 rgba(255,255,255,0.8); position: relative;">
        <div style="
          width: ${Math.min(100, (data.score / 10) * 100)}%; 
          height: 100%; 
          background: linear-gradient(90deg, ${colors.border} 0%, ${colors.border}dd 50%, ${colors.border} 100%);
          background-size: 200% 100%;
          animation: shimmer 2s infinite;
          border-radius: 20px;
          box-shadow: 0 0 10px ${colors.border}80;
          transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        "></div>
      </div>
      <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 0.5px;">
        <span>Seguro</span>
        <span>Peligroso</span>
      </div>
    `
  });
  
  // Add indicators section with improved styling
  const indicatorsSection = createElement('div');
  
  if (data.indicators && data.indicators.length > 0) {
    const indicatorsTitle = createElement('div', {
      style: 'font-size: 15px; font-weight: 600; margin: 16px 0 12px 0; color: #333; padding-bottom: 6px; border-bottom: 1px solid #eee;',
      textContent: '🔍 Indicadores de phishing encontrados:'
    });
    
    const indicatorsList = createElement('div', {
      style: 'margin-bottom: 12px; max-height: 250px; overflow-y: auto; padding-right: 4px;'
    });
    
    // Group indicators by category
    const indicatorsByCategory = data.indicators.reduce((acc, indicator) => {
      if (!acc[indicator.category]) {
        acc[indicator.category] = [];
      }
      acc[indicator.category].push(indicator);
      return acc;
    }, {});
    
    // Create category sections
    Object.entries(indicatorsByCategory).forEach(([category, items]) => {
      const categoryEl = createElement('div', {
        style: 'margin-bottom: 12px; background: #f9f9f9; border: 1px solid #eee; border-radius: 6px; overflow: hidden;'
      });
      
      const categoryHeader = createElement('div', {
        style: `background: ${colors.bg}40; padding: 8px 12px; font-weight: 600; font-size: 13px; color: ${colors.text}; border-bottom: 1px solid #eee;`,
        textContent: `${category} (${items.length})`
      });
      
      const itemsList = createElement('ul', {
        style: 'margin: 0; padding: 0; list-style: none;'
      });
      
      items.forEach((item, index) => {
        const li = createElement('li', {
          style: `padding: 8px 12px; font-size: 13px; border-bottom: ${index < items.length - 1 ? '1px solid #f0f0f0' : 'none'};`,
          textContent: item.text
        });
        itemsList.appendChild(li);
      });
      
      categoryEl.append(categoryHeader, itemsList);
      indicatorsList.appendChild(categoryEl);
    });
    
    indicatorsSection.append(indicatorsTitle, indicatorsList);
  } else {
    indicatorsSection.innerHTML = `
      <div style="
        padding: 16px; 
        background: #f8f9fa; 
        border-radius: 6px; 
        text-align: center; 
        color: #666;
        border: 1px dashed #ddd;
        margin: 16px 0;
      ">
        <div style="font-size: 24px; margin-bottom: 8px;">✅</div>
        <div style="font-weight: 500; margin-bottom: 4px;">No se encontraron indicadores de phishing</div>
        <div style="font-size: 12px; opacity: 0.8;">El texto analizado parece seguro</div>
      </div>
    `;
  }
  
  // Add footer with branding
  const footer = createElement('div', {
    style: `
      padding: 12px 20px;
      background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
      border-top: 1px solid rgba(0,0,0,0.08);
      font-size: 11px;
      color: #666;
      text-align: center;
      border-bottom-left-radius: 15px;
      border-bottom-right-radius: 15px;
    `,
    innerHTML: '<strong>Aegis Security Suite</strong> 2025'
  });
  
  // Assemble the result
  content.append(scoreText, indicatorsSection);
  contentWrapper.appendChild(content);
  result.append(header, contentWrapper, footer);
  
  // Add to document
  document.body.appendChild(result);
  
  // Auto-remove after 30 seconds
  setTimeout(() => {
    if (document.body.contains(result)) {
      result.style.opacity = '1';
      result.style.transition = 'opacity 0.5s ease-out';
      result.style.opacity = '0';
      setTimeout(() => result.remove(), 500);
    }
  }, 30000);
}

// Add animations to style
const additionalStyle = document.createElement('style');
additionalStyle.textContent = `
  @keyframes slideInRight {
    from {
      opacity: 0;
      transform: translateX(100px) scale(0.95);
    }
    to {
      opacity: 1;
      transform: translateX(0) scale(1);
    }
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
  }
  
  @keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
  }
`;
document.head.appendChild(additionalStyle);
