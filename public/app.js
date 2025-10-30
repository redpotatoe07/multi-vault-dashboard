// Multi-Vault Dashboard - Client Side JavaScript

const API_BASE = '';

// Global state for debug mode (toggle with Debug button)
let debugMode = false;

// DOM Elements
const vaultGrid = document.getElementById('vault-grid');
const statusText = document.getElementById('status-text');
const lastUpdated = document.getElementById('last-updated');

// AI Chat Elements
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('chat-send');
const vaultSelector = document.getElementById('vault-selector');
const modelSelector = document.getElementById('model-selector');
const ollamaStatusText = document.getElementById('ollama-status-text');
const ollamaStatus = document.getElementById('ollama-status');

// Initialize
loadVaults();
loadActiveProjects();
checkAIStatus();

// Debug mode toggle button
const debugToggle = document.getElementById('debug-toggle');
debugToggle.addEventListener('click', () => {
  debugMode = !debugMode;
  const status = debugMode ? 'ON' : 'OFF';
  console.log(`Debug Mode: ${status}`);
  
  // Update button appearance
  if (debugMode) {
    debugToggle.style.background = '#27AE60';
    debugToggle.style.color = 'white';
    debugToggle.textContent = 'Debug: ON';
  } else {
    debugToggle.style.background = '';
    debugToggle.style.color = '';
    debugToggle.textContent = 'Debug';
  }
});

/**
 * Load vault data from API
 */
async function loadVaults() {
  try {
    const response = await fetch(`${API_BASE}/api/vaults`);
    const data = await response.json();

    if (data.success) {
      renderVaults(data.vaults);
      updateStatus('Connected', true);
      updateLastUpdated(data.timestamp);
    } else {
      showError('Failed to load vaults: ' + data.error);
    }
  } catch (error) {
    showError('Cannot connect to server: ' + error.message);
  }
}

/**
 * Load active projects from API
 */
async function loadActiveProjects() {
  try {
    const response = await fetch(`${API_BASE}/api/projects`);
    const data = await response.json();

    if (data.success) {
      renderProjects(data.projects);
    } else {
      showProjectsError('Failed to load projects');
    }
  } catch (error) {
    showProjectsError('Cannot connect to server');
  }
}

/**
 * Render project cards
 */
function renderProjects(projects) {
  const projectsContainer = document.getElementById('active-projects');

  if (!projects || projects.length === 0) {
    projectsContainer.innerHTML = '<div class="no-projects">No active projects found</div>';
    return;
  }

  projectsContainer.innerHTML = '';

  projects.forEach(project => {
    const card = createProjectCard(project);
    projectsContainer.appendChild(card);
  });
}

/**
 * Create a project card element
 */
function createProjectCard(project) {
  const card = document.createElement('div');
  card.className = 'project-card';

  // Status badge color
  const statusColors = {
    'active': '#2ECC71',
    'in-progress': '#3498DB',
    'pending': '#F39C12',
    'completed': '#95A5A6',
    'on-hold': '#E74C3C'
  };
  const statusColor = statusColors[project.status.toLowerCase()] || '#3498DB';

  // Format deadline
  let deadlineText = '';
  if (project.deadline) {
    try {
      const deadline = new Date(project.deadline);
      const now = new Date();
      const daysUntil = Math.ceil((deadline - now) / (1000 * 60 * 60 * 24));
      if (daysUntil > 0) {
        deadlineText = `<span class="project-deadline">📅 ${daysUntil} days</span>`;
      } else if (daysUntil === 0) {
        deadlineText = `<span class="project-deadline urgent">📅 Due today!</span>`;
      } else {
        deadlineText = `<span class="project-deadline overdue">📅 Overdue</span>`;
      }
    } catch (e) {
      deadlineText = `<span class="project-deadline">📅 ${project.deadline}</span>`;
    }
  }

  card.innerHTML = `
    <div class="project-header">
      <div class="project-title">
        <span class="project-icon">${project.icon}</span>
        <span class="project-name">${project.name}</span>
      </div>
      <span class="project-status" style="background: ${statusColor}88; color: ${statusColor};">
        ${project.status}
      </span>
    </div>
    <div class="project-progress-section">
      <div class="project-progress-bar">
        <div class="project-progress-fill" style="width: ${project.progress}%; background: ${statusColor};"></div>
      </div>
      <span class="project-progress-text">${project.progress}%</span>
    </div>
    <div class="project-footer">
      <span class="project-vault">🗂️ ${project.vault}</span>
      ${deadlineText}
    </div>
  `;

  // Make clickable (future: navigate to project focus page)
  card.style.cursor = 'pointer';
  card.addEventListener('click', () => {
    console.log('Project clicked:', project.name);
    // TODO: Navigate to project focus page in Stage 5
  });

  return card;
}

/**
 * Show error in projects section
 */
function showProjectsError(message) {
  const projectsContainer = document.getElementById('active-projects');
  projectsContainer.innerHTML = `<div class="error-message">${message}</div>`;
}

/**
 * Render vault cards
 */
function renderVaults(vaults) {
  vaultGrid.innerHTML = '';

  vaults.forEach(vault => {
    const card = createVaultCard(vault);
    vaultGrid.appendChild(card);
  });
}

/**
 * Create a vault card element
 */
function createVaultCard(vault) {
  const card = document.createElement('div');
  card.className = 'vault-card';
  card.style.borderTopColor = vault.color;

  if (!vault.exists) {
    card.innerHTML = `
      <div class="vault-header">
        <span class="vault-icon">${vault.icon}</span>
        <h2 class="vault-title">${vault.name}</h2>
      </div>
      <div class="vault-not-found">Vault not found</div>
    `;
    return card;
  }

  card.innerHTML = `
    <div class="vault-header">
      <span class="vault-icon">${vault.icon}</span>
      <h2 class="vault-title">${vault.name}</h2>
    </div>

    <div class="vault-stats">
      <div class="stat-box">
        <span class="stat-value">${vault.fileCount}</span>
        <span class="stat-label">Files</span>
      </div>
      <div class="stat-box">
        <span class="stat-value">${vault.topFolders.length}</span>
        <span class="stat-label">Folders</span>
      </div>
    </div>

    ${vault.topFolders.length > 0 ? `
      <div class="vault-section">
        <h3 class="section-title">Top Folders</h3>
        <ul class="folder-list">
          ${vault.topFolders.map(folder => `
            <li class="folder-item">
              <span class="file-name">📁 ${folder.name}</span>
              <span class="folder-count">${folder.fileCount}</span>
            </li>
          `).join('')}
        </ul>
      </div>
    ` : ''}

    ${vault.recentFiles.length > 0 ? `
      <div class="vault-section">
        <h3 class="section-title">Recent Files</h3>
        <ul class="file-list">
          ${vault.recentFiles.slice(0, 5).map(file => `
            <li class="file-item">
              <span class="file-name" title="${file.relativePath}">📄 ${file.name}</span>
              <span class="file-time">${formatTimeAgo(file.modified)}</span>
            </li>
          `).join('')}
        </ul>
      </div>
    ` : ''}
  `;

  return card;
}

/**
 * Update status indicator
 */
function updateStatus(text, isConnected) {
  statusText.textContent = text;
  const dot = document.querySelector('.status-dot');
  if (dot) {
    dot.style.background = isConnected ? 'var(--success)' : '#E74C3C';
  }
}

/**
 * Update last updated timestamp
 */
function updateLastUpdated(timestamp) {
  const date = new Date(timestamp);
  lastUpdated.textContent = date.toLocaleTimeString();
}

/**
 * Show error message
 */
function showError(message) {
  vaultGrid.innerHTML = `
    <div class="loading" style="color: #E74C3C;">
      ⚠️ ${message}
      <br><br>
      <button onclick="location.reload()" style="padding: 10px 20px; background: var(--accent); border: none; border-radius: 6px; color: white; cursor: pointer; font-size: 1rem;">
        Retry
      </button>
    </div>
  `;
  updateStatus('Disconnected', false);
}

/**
 * Format time ago (e.g., "5 min ago")
 */
function formatTimeAgo(timestamp) {
  const now = new Date();
  const date = new Date(timestamp);
  const seconds = Math.floor((now - date) / 1000);

  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;

  return date.toLocaleDateString();
}

/**
 * Check AI availability (both Ollama and Claude)
 */
async function checkAIStatus() {
  try {
    // Check both services
    const [ollamaRes, claudeRes] = await Promise.all([
      fetch(`${API_BASE}/api/ollama/status`),
      fetch(`${API_BASE}/api/claude/status`)
    ]);

    const ollamaData = await ollamaRes.json();
    const claudeData = await claudeRes.json();

    const indicator = ollamaStatus.querySelector('.status-indicator');
    const selectedModel = modelSelector.value;

    // Update status based on selected model
    if (selectedModel === 'search') {
      // RAG Search mode - always available
      ollamaStatusText.textContent = 'RAG Search Ready';
      indicator.className = 'status-indicator online';
      chatInput.disabled = false;
      chatSend.disabled = false;
      chatInput.placeholder = 'Search your vaults...';
    } else if (selectedModel === 'claude' && claudeData.available) {
      ollamaStatusText.textContent = 'Claude Pro Online';
      indicator.className = 'status-indicator online';
      chatInput.disabled = false;
      chatSend.disabled = false;
      chatInput.placeholder = 'Ask Claude about your vaults...';
    } else if (selectedModel === 'ollama' && ollamaData.available) {
      ollamaStatusText.textContent = 'Ollama Online';
      indicator.className = 'status-indicator online';
      chatInput.disabled = false;
      chatSend.disabled = false;
      chatInput.placeholder = 'Ask Ollama about your vaults...';
    } else {
      const modelName = selectedModel === 'claude' ? 'Claude' : 'Ollama';
      ollamaStatusText.textContent = `${modelName} Offline`;
      indicator.className = 'status-indicator offline';
      chatInput.disabled = true;
      chatSend.disabled = true;
      chatInput.placeholder = `${modelName} not available...`;
    }
  } catch (error) {
    ollamaStatusText.textContent = 'AI Status Unknown';
    console.error('Failed to check AI status:', error);
  }
}

// Update status when model changes
modelSelector.addEventListener('change', checkAIStatus);

/**
 * Send message to AI (NEW - with streaming support for Ollama)
 */
async function sendAIMessage() {
  const question = chatInput.value.trim();
  const vault = vaultSelector.value;
  const model = modelSelector.value;

  if (!question) return;

  // Add user message to chat
  addChatMessage(question, 'user');

  // Clear input and disable while processing
  chatInput.value = '';
  chatInput.disabled = true;
  chatSend.disabled = true;
  chatSend.classList.add('loading');
  const sendIcon = document.getElementById('send-icon');
  sendIcon.textContent = '';

  try {
    // Handle RAG Search mode
    if (model === 'search') {
      await handleSearchMode(question, vault);
    } else {
      // Choose API endpoint based on model
      const endpoint = model === 'claude' ? '/api/claude/ask' : '/api/ollama/ask';

      // For Ollama, use streaming
      if (model === 'ollama') {
        await handleStreamingResponse(endpoint, question, vault);
      } else {
        // For Claude, use non-streaming (legacy)
        await handleNonStreamingResponse(endpoint, question, vault);
      }
    }
  } catch (error) {
    addChatMessage(`Failed to get response: ${error.message}`, 'ai', true);
  } finally {
    chatInput.disabled = false;
    chatSend.disabled = false;
    chatSend.classList.remove('loading');
    sendIcon.textContent = 'Send';
    chatInput.focus();
  }
}

/**
 * Handle RAG Search mode
 */
async function handleSearchMode(question, vault) {
  try {
    // Build query params
    const params = new URLSearchParams({ q: question });
    if (vault && vault !== 'all') {
      params.append('vault', vault);
    }

    const response = await fetch(`${API_BASE}/api/search?${params}`);

    const data = await response.json();

    if (!data.success) {
      addChatMessage(`Search failed: ${data.error || 'Unknown error'}`, 'ai', true);
      return;
    }

    // Build response message
    let message = '';

    // Add debug info if enabled
    if (debugMode && data.query_type && data.search_strategy) {
      message += `**Debug Info:**\n`;
      message += `- Query Type: ${data.query_type}\n`;
      message += `- Strategy: ${data.search_strategy}\n`;
      message += `- Results: ${data.result_count}\n\n`;
    }

    // Format search results
    if (data.result_count === 0) {
      message += 'No results found for your search.';
    } else {
      message += `Found **${data.result_count} results**:\n\n`;

      data.results.forEach((result, index) => {
        const vaultIcon = getVaultIcon(result.vault);
        message += `${index + 1}. ${vaultIcon} **${result.metadata.filename}**\n`;
        message += `   _${result.vault}${result.metadata.folder ? ' / ' + result.metadata.folder : ''}_\n`;

        // Show relevance score in debug mode
        if (debugMode && result.relevance_score) {
          message += `   Score: ${result.relevance_score.toFixed(3)}\n`;
        }

        message += '\n';
      });
    }

    addChatMessage(message, 'ai');
  } catch (error) {
    console.error('Search error:', error);
    addChatMessage('Sorry, there was an error performing the search.', 'ai', true);
  }
}

/**
 * Get vault icon emoji
 */
function getVaultIcon(vaultName) {
  const icons = {
    'Study': '📚',
    'Creative-Incubator': '🎨',
    'Business-Incubator': '💼',
    'Red-White': '📖',
    'ThistleRidgeHall': '🎯',
    'SickRabbit': '🐰',
    'Library': '📋',
    'Life-Systems': '⚙️',
    'Praxis': '🔧'
  };
  return icons[vaultName] || '📄';
}

/**
 * Handle streaming response from Ollama (NEW)
 */
async function handleStreamingResponse(endpoint, question, vault) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ question, vault })
  });

  if (!response.ok) {
    const error = await response.json();
    addChatMessage(`Error: ${error.error}`, 'ai', true);
    return;
  }

  // Create AI message container for streaming
  const messageDiv = document.createElement('div');
  messageDiv.className = 'chat-message ai-message';

  const icon = document.createElement('div');
  icon.className = 'message-icon';
  icon.textContent = '🤖';

  const content = document.createElement('div');
  content.className = 'message-content';
  content.textContent = ''; // Will be filled by streaming

  messageDiv.appendChild(icon);
  messageDiv.appendChild(content);
  chatMessages.appendChild(messageDiv);

  // Read streaming response
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let fullText = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value, { stream: true });
    const lines = chunk.split('\n');

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        try {
          const data = JSON.parse(line.slice(6));

          // Check for errors
          if (data.error) {
            content.style.background = '#E74C3C';
            content.style.color = 'white';
            content.textContent = `Error: ${data.error}`;
            return;
          }

          // Append content from streaming chunk
          if (data.message && data.message.content) {
            fullText += data.message.content;
            // Update display with markdown rendering
            content.innerHTML = parseMarkdown(fullText);
            // Auto-scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
          }
        } catch (e) {
          console.error('Failed to parse streaming chunk:', e);
        }
      }
    }
  }
}

/**
 * Handle non-streaming response from Claude (legacy)
 */
async function handleNonStreamingResponse(endpoint, question, vault) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ question, vault })
  });

  const data = await response.json();

  if (data.success) {
    addChatMessage(data.answer, 'ai');
  } else {
    addChatMessage(`Error: ${data.error}`, 'ai', true);
  }
}

/**
 * Simple markdown to HTML converter
 */
function parseMarkdown(text) {
  let html = text;

  // Headers (##, ###)
  html = html.replace(/^### (.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^## (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^# (.+)$/gm, '<h2>$1</h2>');

  // Bold **text**
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

  // Italic *text*
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Lists - convert to <li> tags
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
  html = html.replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>');

  // Wrap consecutive <li> in <ul> and remove newlines inside lists
  html = html.replace(/(<li>.*?<\/li>\n?)+/gs, (match) => {
    // Remove newlines between list items
    const cleanedList = match.replace(/\n/g, '');
    return '<ul>' + cleanedList + '</ul>';
  });

  // Line breaks (convert double newlines to paragraphs)
  const paragraphs = html.split('\n\n');
  html = paragraphs.map(para => {
    para = para.trim();
    if (!para) return '';
    // Don't wrap if already has HTML block tags
    if (para.startsWith('<h') || para.startsWith('<ul') || para.startsWith('<ol')) {
      return para;
    }
    return `<p>${para}</p>`;
  }).join('\n');

  // Single line breaks (but not inside HTML tags)
  html = html.replace(/\n(?![<])/g, '<br>');

  return html;
}

/**
 * Add message to chat display
 */
function addChatMessage(text, type, isError = false) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `chat-message ${type}-message`;

  const icon = document.createElement('div');
  icon.className = 'message-icon';
  icon.textContent = type === 'user' ? '👤' : '🤖';

  const content = document.createElement('div');
  content.className = 'message-content';

  if (isError) {
    content.style.background = '#E74C3C';
    content.style.color = 'white';
  }

  // Render markdown for AI messages, plain text for user
  if (type === 'ai' && !isError) {
    content.innerHTML = parseMarkdown(text);
  } else {
    content.textContent = text;
  }

  messageDiv.appendChild(icon);
  messageDiv.appendChild(content);
  chatMessages.appendChild(messageDiv);

  // Scroll to bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Event listeners for chat
chatSend.addEventListener('click', sendAIMessage);
chatInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter' && !chatInput.disabled) {
    sendAIMessage();
  }
});

/**
 * Auto-refresh every 60 seconds
 */
setInterval(() => {
  loadVaults();
  checkAIStatus();
}, 60000);
