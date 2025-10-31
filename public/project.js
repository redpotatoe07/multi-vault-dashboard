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

    // For now, we'll load project info from the projects API
    // In Stage 6, we'll add more detailed project-specific endpoints
    const response = await fetch(`${API_BASE}/api/projects`);
    const data = await response.json();

    if (data.success) {
      // Find the project by name or vault
      let project;
      if (projectName) {
        project = data.projects.find(p => p.name === projectName);
      } else if (projectVault) {
        project = data.projects.find(p => p.vault === projectVault);
      }

      if (project) {
        renderProjectHeader(project);
        renderProjectTimeline(project);
        renderProjectFiles(project);
        renderProjectStats(project);
        renderProjectTasks(project);
        updateStatus('Connected', true);
      } else {
        showError(`Project not found: ${projectName || projectVault}`);
      }
    } else {
      showError('Failed to load project data');
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
 * Render project timeline (placeholder for Stage 6)
 */
function renderProjectTimeline(project) {
  projectTimeline.innerHTML = `
    <div class="timeline-placeholder">
      <p>Timeline view will be implemented in Stage 6</p>
      <p class="placeholder-note">This will show project phases, milestones, and completion status</p>
    </div>
  `;
}

/**
 * Render related files (placeholder for Stage 6)
 */
function renderProjectFiles(project) {
  projectFiles.innerHTML = `
    <div class="files-placeholder">
      <p>Related files will be loaded in Stage 6</p>
      <p class="placeholder-note">This will query RAG for files tagged with this project</p>
    </div>
  `;
}

/**
 * Render project stats (placeholder for Stage 6)
 */
function renderProjectStats(project) {
  projectStats.innerHTML = `
    <div class="stat-card">
      <div class="stat-value">${project.progress}%</div>
      <div class="stat-label">Complete</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">--</div>
      <div class="stat-label">Total Files</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">--</div>
      <div class="stat-label">Tasks</div>
    </div>
  `;
}

/**
 * Render active tasks (placeholder for Stage 6)
 */
function renderProjectTasks(project) {
  projectTasks.innerHTML = `
    <div class="tasks-placeholder">
      <p>Tasks will be loaded in Stage 6</p>
      <p class="placeholder-note">This will show tasks related to this project</p>
    </div>
  `;
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
