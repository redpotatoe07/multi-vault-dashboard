// Project Focus Page - Client Side JavaScript

const API_BASE = '';

// Get project ID from URL parameters
const urlParams = new URLSearchParams(window.location.search);
const projectName = urlParams.get('name');
const projectVault = urlParams.get('vault');

// DOM Elements
const statusText = document.getElementById('status-text');
const projectHeaderSection = document.getElementById('project-header-section');
const projectTimeline = document.getElementById('project-timeline');
const projectFiles = document.getElementById('project-files');
const projectStats = document.getElementById('project-stats');
const projectTasks = document.getElementById('project-tasks');

// Initialize
if (!projectName && !projectVault) {
  showError('No project specified. Please select a project from the overview page.');
} else {
  loadProjectData();
}

/**
 * Load all project data
 */
async function loadProjectData() {
  try {
    updateStatus('Loading project...', true);

    // Fetch detailed project data from new endpoint
    const identifier = projectName || projectVault;
    const type = projectName ? 'name' : 'vault';
    const response = await fetch(`${API_BASE}/api/project/${encodeURIComponent(identifier)}?type=${type}`);
    const data = await response.json();

    if (data.success && data.project) {
      const project = data.project;
      renderProjectHeader(project);
      renderProjectTimeline(project);
      renderProjectFiles(project);
      renderProjectStats(project);
      renderProjectTasks(project);
      updateStatus('Connected', true);
    } else {
      showError(data.error || `Project not found: ${identifier}`);
    }
  } catch (error) {
    showError('Cannot connect to server: ' + error.message);
  }
}

/**
 * Render project header with name, status, progress, deadline
 */
function renderProjectHeader(project) {
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
  let deadlineInfo = '';
  if (project.deadline) {
    try {
      const deadline = new Date(project.deadline);
      const now = new Date();
      const daysUntil = Math.ceil((deadline - now) / (1000 * 60 * 60 * 24));
      if (daysUntil > 0) {
        deadlineInfo = `<div class="deadline-info">📅 <strong>${daysUntil} days</strong> until deadline</div>`;
      } else if (daysUntil === 0) {
        deadlineInfo = `<div class="deadline-info urgent">⚠️ Due today!</div>`;
      } else {
        deadlineInfo = `<div class="deadline-info overdue">⚠️ Overdue by ${Math.abs(daysUntil)} days</div>`;
      }
    } catch (e) {
      deadlineInfo = `<div class="deadline-info">📅 ${project.deadline}</div>`;
    }
  }

  projectHeaderSection.innerHTML = `
    <div class="project-header-content">
      <div class="project-title-row">
        <div class="project-icon-large">${project.icon}</div>
        <div class="project-title-info">
          <h1 class="project-title">${project.name}</h1>
          <div class="project-meta">
            <span class="project-vault-badge">🗂️ ${project.vault}</span>
            <span class="project-status-badge" style="background: ${statusColor}88; color: ${statusColor};">
              ${project.status}
            </span>
          </div>
        </div>
      </div>

      <div class="project-progress-section">
        <div class="progress-info">
          <span class="progress-label">Overall Progress</span>
          <span class="progress-percentage">${project.progress}%</span>
        </div>
        <div class="progress-bar-large">
          <div class="progress-fill-large" style="width: ${project.progress}%; background: ${statusColor};"></div>
        </div>
        ${deadlineInfo}
      </div>
    </div>
  `;
}

/**
 * Render project timeline with phases
 */
function renderProjectTimeline(project) {
  if (!project.timeline || project.timeline.length === 0) {
    projectTimeline.innerHTML = `
      <div class="timeline-empty">
        <p>No timeline data available</p>
        <p class="empty-note">Add phases to PROJECT-STATUS.md to see timeline</p>
      </div>
    `;
    return;
  }

  const phasesHTML = project.timeline.map(phase => {
    const statusColors = {
      'completed': '#2ECC71',
      'in-progress': '#3498DB',
      'pending': '#95A5A6'
    };
    const statusColor = statusColors[phase.status] || '#95A5A6';

    const statusIcons = {
      'completed': '✓',
      'in-progress': '▶',
      'pending': '○'
    };
    const statusIcon = statusIcons[phase.status] || '○';

    return `
      <div class="timeline-phase">
        <div class="phase-header">
          <div class="phase-title">
            <span class="phase-icon" style="color: ${statusColor};">${statusIcon}</span>
            <span class="phase-name">Phase ${phase.number}: ${phase.name}</span>
          </div>
          <span class="phase-progress">${phase.progress}%</span>
        </div>
        <div class="phase-progress-bar">
          <div class="phase-progress-fill" style="width: ${phase.progress}%; background: ${statusColor};"></div>
        </div>
      </div>
    `;
  }).join('');

  projectTimeline.innerHTML = phasesHTML;
}

/**
 * Render related files
 */
function renderProjectFiles(project) {
  if (!project.relatedFiles || project.relatedFiles.length === 0) {
    projectFiles.innerHTML = `
      <div class="files-empty">
        <p>No related files found</p>
      </div>
    `;
    return;
  }

  const filesHTML = project.relatedFiles.slice(0, 15).map(file => {
    const timeAgo = formatTimeAgo(file.modified);
    const sizeKB = (file.size / 1024).toFixed(1);

    return `
      <div class="file-item-card">
        <div class="file-info">
          <div class="file-icon">📄</div>
          <div class="file-details">
            <div class="file-name">${file.name}</div>
            <div class="file-meta">
              <span class="file-path" title="${file.path}">${file.path}</span>
            </div>
          </div>
        </div>
        <div class="file-stats">
          <span class="file-time">${timeAgo}</span>
          <span class="file-size">${sizeKB} KB</span>
        </div>
      </div>
    `;
  }).join('');

  projectFiles.innerHTML = filesHTML;
}

/**
 * Render project stats
 */
function renderProjectStats(project) {
  const stats = project.stats || {};

  projectStats.innerHTML = `
    <div class="stat-card">
      <div class="stat-value">${project.progress}%</div>
      <div class="stat-label">Complete</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${stats.totalFiles || 0}</div>
      <div class="stat-label">Files</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${stats.totalPhases || 0}</div>
      <div class="stat-label">Phases</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${stats.completedTasks || 0}/${stats.totalPhases || 0}</div>
      <div class="stat-label">Completed</div>
    </div>
  `;
}

/**
 * Render active tasks
 */
function renderProjectTasks(project) {
  if (!project.timeline || project.timeline.length === 0) {
    projectTasks.innerHTML = `
      <div class="tasks-empty">
        <p>No tasks available</p>
      </div>
    `;
    return;
  }

  // Show incomplete phases as tasks
  const tasks = project.timeline
    .filter(phase => phase.status !== 'completed')
    .map(phase => ({
      name: `Complete ${phase.name}`,
      progress: phase.progress,
      status: phase.status
    }));

  if (tasks.length === 0) {
    projectTasks.innerHTML = `
      <div class="tasks-complete">
        <p>✓ All tasks complete!</p>
      </div>
    `;
    return;
  }

  const tasksHTML = tasks.map(task => {
    const statusColors = {
      'in-progress': '#3498DB',
      'pending': '#95A5A6'
    };
    const statusColor = statusColors[task.status] || '#95A5A6';

    return `
      <div class="task-item">
        <div class="task-info">
          <span class="task-checkbox" style="border-color: ${statusColor};"></span>
          <span class="task-name">${task.name}</span>
        </div>
        <span class="task-progress">${task.progress}%</span>
      </div>
    `;
  }).join('');

  projectTasks.innerHTML = tasksHTML;
}

/**
 * Format time ago helper
 */
function formatTimeAgo(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);
  const diffWeek = Math.floor(diffDay / 7);
  const diffMonth = Math.floor(diffDay / 30);

  if (diffSec < 60) return 'Just now';
  if (diffMin < 60) return `${diffMin}m ago`;
  if (diffHour < 24) return `${diffHour}h ago`;
  if (diffDay < 7) return `${diffDay}d ago`;
  if (diffWeek < 4) return `${diffWeek}w ago`;
  return `${diffMonth}mo ago`;
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
 * Show error message
 */
function showError(message) {
  projectHeaderSection.innerHTML = `
    <div class="error-message-large">
      <h2>⚠️ Error</h2>
      <p>${message}</p>
      <a href="index.html" class="back-button">← Back to Overview</a>
    </div>
  `;
  updateStatus('Error', false);
}
