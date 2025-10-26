# Multi-Vault Dashboard - Development Roadmap

**Last Updated:** 2025-10-23
**Current Phase:** Phase 1 (Dashboard UI Design)

---

## Overview

This roadmap outlines the incremental evolution from **dashboard** (view-only) to **custom knowledge management system** (full-featured web app).

**Strategy:** Build incrementally, get value at each stage, learn what's needed before committing to next phase.

---

## Phase 1: Dashboard UI Polish ⏳ IN PROGRESS

**Goal:** Professional, minimalist dashboard for viewing and searching vaults

**Timeline:** 1-2 weeks
**Status:** 60% complete

### Current Progress

**✅ Completed:**
- Vault grid displaying 9 vaults
- RAG search integration (ChromaDB, hybrid search)
- Unified search interface (RAG, Claude, Ollama modes)
- Real-time vault statistics
- Chat interface with streaming responses
- Mobile-responsive design
- Debug mode toggle
- Multi-Vault Architecture migration (all 1,269 files with hierarchical YAML)
- Design sub-agents created (dashboard-ui-designer, dashboard-design-reviewer)

**⏳ In Progress:**
- UI/UX design with dashboard-ui-designer agent
- Overview mode layout
- Project focus mode (separate page)
- Aesthetic polish (Tailwind CSS integration)

**📋 Remaining Tasks:**
- [ ] Finalize overview page layout
- [ ] Create project focus page
- [ ] Implement navigation between modes
- [ ] Apply minimalist design principles
- [ ] Accessibility review (WCAG 2.1 AA)
- [ ] Performance optimization
- [ ] Cross-browser testing

### Deliverables

1. **Overview Mode:**
   - Vault status grid (9 vaults with stats)
   - Active projects list
   - Recent activity feed
   - Quick search interface

2. **Project Focus Mode (Separate Page):**
   - Project header (name, status, progress)
   - Timeline visualization
   - Related files list (from RAG)
   - Active tasks display
   - Project analytics

3. **Navigation:**
   - Tab or sidebar navigation
   - Clear routing between overview ↔ project pages
   - Breadcrumbs for context

4. **Design Quality:**
   - Speed: <2 second load time
   - Information density: Show relevant data without clutter
   - Clear visualization: Charts, timelines communicate instantly
   - Minimalist aesthetic: 2025 best practices

### Success Criteria

- ✅ All 9 vaults displayed with accurate stats
- ✅ RAG search returns relevant results (<1s response time)
- ✅ Can navigate to project focus page from vault click
- ✅ UI passes accessibility review (WCAG 2.1 AA)
- ✅ User can understand vault status at a glance
- ✅ Mobile-responsive (works on phone/tablet)

---

## Phase 2: Markdown Editor 📝 NEXT PRIORITY

**Goal:** Enable editing markdown files directly from web browser

**Timeline:** 1-2 weeks
**Status:** Not started

### Features to Implement

1. **Monaco Editor Integration:**
   - Add Monaco editor (VS Code's editor)
   - Markdown syntax highlighting
   - Auto-save functionality
   - File tree navigation
   - Recent files list

2. **Split View:**
   - Editor on left, preview on right
   - Live markdown rendering
   - Synchronized scrolling
   - Toggle view mode (edit only, preview only, split)

3. **YAML Frontmatter Editor:**
   - Visual form for editing YAML metadata
   - Dropdown for `type`, `category`, `subcategory`
   - Tag picker with autocomplete
   - Date pickers for deadlines/dates
   - Save frontmatter → update file

4. **File Operations:**
   - Create new file (with template selection)
   - Delete file (with confirmation)
   - Rename file
   - Move file between folders
   - Duplicate file

5. **Backend API Endpoints:**
   ```javascript
   POST /api/save-file        // Write content to file
   POST /api/create-file      // Create new file
   DELETE /api/delete-file    // Delete file
   PUT /api/rename-file       // Rename/move file
   GET /api/read-file         // Read file content
   ```

### Technical Implementation

**Frontend:**
```javascript
// Add Monaco editor CDN
<script src="https://cdn.jsdelivr.net/npm/monaco-editor@latest/min/vs/loader.js"></script>

// Initialize editor
require(['vs/editor/editor.main'], function() {
  const editor = monaco.editor.create(container, {
    value: fileContent,
    language: 'markdown',
    theme: 'vs-dark',
    minimap: { enabled: false },
    wordWrap: 'on',
    lineNumbers: 'on'
  });
});
```

**Backend (server.js):**
```javascript
const fs = require('fs').promises;
const path = require('path');

app.post('/api/save-file', async (req, res) => {
  try {
    const { filePath, content } = req.body;
    const fullPath = path.join(VAULT_ROOT, filePath);

    // Atomic write (temp file + rename)
    const tempPath = `${fullPath}.tmp`;
    await fs.writeFile(tempPath, content, 'utf8');
    await fs.rename(tempPath, fullPath);

    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### Success Criteria

- ✅ Can open any markdown file in editor
- ✅ Can edit and save changes (atomic writes, no corruption)
- ✅ YAML frontmatter editable via visual form
- ✅ Can create new files with templates
- ✅ Can delete files (with undo via Git later)
- ✅ Split view works (edit + preview synchronized)
- ✅ Editor is fast and responsive (no lag)

### Dependencies

- monaco-editor (CDN or npm package)
- marked.js or similar (markdown → HTML rendering)

### Risks & Mitigations

**Risk:** File corruption if write fails mid-operation
**Mitigation:** Use atomic writes (temp file + rename)

**Risk:** Editing same file in Obsidian + web app = conflicts
**Mitigation:** File lock detection (warn if file open elsewhere)

**Risk:** Large files slow down editor
**Mitigation:** Lazy loading, virtual scrolling for large files

---

## Phase 3: Git Integration 🔄 FUTURE

**Goal:** Version control, cloud backup, collaboration foundation

**Timeline:** 1 week
**Status:** Not started

### Features to Implement

1. **Auto-Commit on Save:**
   - Every file save = Git commit
   - Commit message: "Update [filename]" or custom message
   - Push to remote after commit (optional, configurable)

2. **Commit History:**
   - View file history (list of commits)
   - See diff between versions
   - Rollback to previous version (git checkout)

3. **Git Status UI:**
   - Show modified files (red dot indicator)
   - Show untracked files
   - Show sync status (ahead/behind remote)

4. **Sync Controls:**
   - Manual push button (sync to cloud)
   - Manual pull button (get latest from cloud)
   - Auto-sync toggle (enable/disable auto-push)

5. **Conflict Resolution:**
   - Detect merge conflicts
   - Show diff view (local vs. remote)
   - Let user choose version or manually merge

### Technical Implementation

**Use simple-git npm package:**

```javascript
const simpleGit = require('simple-git');
const git = simpleGit(VAULT_ROOT);

// Commit on save
app.post('/api/save-file', async (req, res) => {
  // ... save file ...

  // Git commit
  await git.add(filePath);
  await git.commit(`Update ${filePath}`);

  // Optional: auto-push
  if (AUTO_PUSH_ENABLED) {
    await git.push();
  }

  res.json({ success: true });
});

// Get commit history
app.get('/api/git/history/:filePath', async (req, res) => {
  const log = await git.log({ file: req.params.filePath });
  res.json(log.all);
});

// Rollback to commit
app.post('/api/git/checkout', async (req, res) => {
  const { filePath, commitHash } = req.body;
  await git.checkout(commitHash, ['--', filePath]);
  res.json({ success: true });
});
```

### Success Criteria

- ✅ Every save creates Git commit
- ✅ Can view commit history for file
- ✅ Can rollback to previous version
- ✅ Can push/pull from remote (GitHub/GitLab)
- ✅ Conflict detection works (alerts user)
- ✅ Never lose data (Git = safety net)

### Dependencies

- simple-git (npm package)
- Git installed on server
- GitHub/GitLab repository (remote)

### Configuration

```javascript
// Add to server.js config
const GIT_CONFIG = {
  autoCommit: true,         // Commit on every save
  autoPush: false,          // Don't auto-push (manual only)
  remote: 'origin',         // Remote name
  branch: 'main',           // Branch name
  commitMessage: (file) => `Update ${file}` // Message template
};
```

---

## Phase 4: Project Management Views 📊 FUTURE

**Goal:** Custom views for timelines, tasks, deadlines, kanban

**Timeline:** 2-3 months (iterative)
**Status:** Not started

### Features to Implement

#### 4.1: Timeline View (Month 1)

**Goal:** Visual Gantt chart for project milestones

**Features:**
- Horizontal timeline (Chart.js Timeline or FullCalendar)
- Milestones as points on timeline
- Tasks as bars (start date → end date)
- Color coding by status (active, completed, overdue)
- Drag to reschedule (update YAML deadline)
- Click milestone → edit details

**Data Source:**
- Parse PROJECT-STATUS.md files
- Query RAG for files with `deadline:` YAML field
- Aggregate across vaults

**Example:**
```
Project: Multi-Vault Architecture
├─ Phase 1: Framework Design    ████████ (Oct 22 - Complete)
├─ Phase 2: Vault Audits        ████████ (Oct 23 - Complete)
├─ Phase 3: Migration           ████████ (Oct 23 - Complete)
├─ Phase 4: Validation          ░░░░░░░░ (Oct 24-25 - Pending)
└─ Phase 5: Documentation       ░░░░░░░░ (Oct 26-27 - Pending)
```

#### 4.2: Kanban Board (Month 2)

**Goal:** Drag-and-drop task management

**Features:**
- Columns: To Do, In Progress, Done (customizable)
- Cards = tasks (title, description, assignee, deadline)
- Drag card between columns (updates `status:` YAML field)
- Create new task (adds to vault as markdown file)
- Filter by vault, project, tag

**Data Source:**
- Query RAG for `type: task` or `status:` field
- Task files in vaults (e.g., `Tasks/Task-001.md`)

**Technical:**
- Use react-beautiful-dnd or @dnd-kit (drag-and-drop)
- Update YAML on drag (auto-save + Git commit)

#### 4.3: Calendar View (Month 2)

**Goal:** Deadline tracking and scheduling

**Features:**
- Month/week/day views (FullCalendar)
- Events = files with `deadline:` YAML field
- Color coded by vault or priority
- Click date → create new task/event
- Drag event → reschedule (update YAML)

#### 4.4: Project Analytics (Month 3)

**Goal:** Insights and productivity metrics

**Features:**
- Project progress (% complete based on tasks)
- Velocity chart (tasks completed per week)
- Vault activity (files created/modified over time)
- Tag cloud (most used tags)
- Burndown chart (tasks remaining vs. time to deadline)

**Technical:**
- Aggregate data from RAG queries
- Chart.js for visualizations
- Cache calculations (performance)

### Architectural Decisions Needed

**Question 1: How to define a "project"?**

**Options:**
- **A)** Vault = Project (ThistleRidgeHall.vault = project)
- **B)** YAML metadata (`type: project`)
- **C)** Special files (PROJECT-STATUS.md)
- **D)** Hybrid (B + C)

**Recommendation:** Hybrid approach
- Tag project files with `type: project`
- Parse PROJECT-STATUS.md for timeline/milestones
- Aggregate tasks with `project:` field linking to project

**Question 2: How to aggregate tasks across vaults?**

**Approach:**
```javascript
// Query RAG for all tasks
const tasks = await ragSearch({
  query: "type:task OR status:pending OR status:in-progress",
  vaults: ["all"],
  limit: 1000
});

// Group by project
const tasksByProject = tasks.reduce((acc, task) => {
  const project = task.metadata.project || 'Unassigned';
  acc[project] = acc[project] || [];
  acc[project].push(task);
  return acc;
}, {});

// Display in UI (kanban, timeline, calendar)
```

### Success Criteria

- ✅ Can view project timeline (all milestones visible)
- ✅ Can drag tasks between kanban columns (updates YAML)
- ✅ Calendar shows all deadlines
- ✅ Analytics provide useful insights (not just vanity metrics)
- ✅ Fast performance (visualizations load <1s)

---

## Phase 5: Full Custom App 🚀 LONG-TERM

**Goal:** Production-ready knowledge management system

**Timeline:** 4-6 months
**Status:** Not started (far future)

### Potential Features

**Authentication & Multi-User:**
- User accounts (email/password or OAuth)
- Workspace sharing (invite collaborators)
- Permissions (read-only, edit, admin)

**Real-Time Collaboration:**
- See who's editing which file
- Live cursors (like Google Docs)
- Operational Transform or CRDT for conflict-free editing

**Mobile App:**
- Progressive Web App (PWA) for app-like experience
- Or React Native for native iOS/Android apps
- Optimized mobile UI (simplified for small screens)

**Advanced Integrations:**
- Zapier webhooks (automate workflows)
- API for third-party integrations
- Browser extension (clip web pages to vault)
- Email to vault (forward emails → create notes)

**AI Features:**
- Auto-tagging (AI suggests tags based on content)
- Smart summaries (summarize long documents)
- Related files (AI finds connections)
- Writing assistance (Claude helps draft content)

**Public Knowledge Base:**
- Option to publish select vaults publicly
- Custom domain (e.g., knowledge.yourname.com)
- SEO optimization (Google-indexed)
- Comments/discussions (if desired)

### Tech Stack Migration (If Needed)

**Current:** Express + Vanilla JS
**Future:** Next.js + React

**Migration Path:**
1. Keep Flask RAG service (microservice)
2. Rebuild frontend in Next.js (component-based)
3. Port features incrementally (not big-bang)
4. Deploy to Vercel (free tier, auto-deploy)

**Timeline:** 2-3 weeks for migration (when/if needed)

---

## Success Metrics

### Phase 1 Success (Dashboard)
- ✅ Can view all 9 vaults at a glance
- ✅ Search finds relevant files (<1s)
- ✅ UI is fast and minimalist
- ✅ Works on mobile

### Phase 2 Success (Editor)
- ✅ Can edit files from web browser
- ✅ No data loss or corruption
- ✅ YAML frontmatter editable
- ✅ File creation/deletion works

### Phase 3 Success (Git)
- ✅ Every save creates commit
- ✅ Can rollback to previous version
- ✅ Cloud backup working (GitHub)
- ✅ Never lose data

### Phase 4 Success (Project Management)
- ✅ Timeline shows project milestones
- ✅ Kanban board for task management
- ✅ Calendar displays deadlines
- ✅ Analytics provide insights

### Ultimate Success (Custom App)
- ✅ Obsidian is optional (web app is primary)
- ✅ Accessible anywhere (laptop, phone, tablet)
- ✅ Project management replaces external tools (Notion, Trello)
- ✅ Complete control over workflow
- ✅ Data is yours forever (markdown + Git)

---

## Decision Log

### 2025-10-23: Evolution Strategy
**Decision:** Evolve dashboard → custom app (don't rebuild from scratch)
**Rationale:** Get value incrementally, learn needs before committing to tech stack
**Impact:** Faster time to value, less risk

### 2025-10-23: Keep Vault Structure
**Decision:** Keep markdown files in vault folders (don't migrate to database)
**Rationale:** Portability, Obsidian compatibility, Git-friendly
**Impact:** Simple file operations, no migration risk

### 2025-10-23: Git as Backbone
**Decision:** Use Git for version control + cloud backup
**Rationale:** Industry standard, free hosting (GitHub), never lose data
**Impact:** Every edit is versioned, collaboration possible later

---

## Next Session Quick Start

**When resuming work on this project:**

1. **Read [VISION.md](VISION.md)** - Understand long-term goals
2. **Check this roadmap** - See current phase and tasks
3. **Review Phase 1 tasks** - Continue where left off
4. **Invoke dashboard-ui-designer agent** - If working on UI
5. **Check [.claude/agents/README.md](.claude/agents/README.md)** - Agent documentation

**Current Focus:** Phase 1 - Dashboard UI design (overview + project focus modes)

---

**This roadmap is living - update after each phase completion!**

**Last Updated:** 2025-10-23
**Next Review:** After Phase 1 completion
