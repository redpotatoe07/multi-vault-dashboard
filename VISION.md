# Multi-Vault Dashboard - Vision & Long-Term Goals

**Last Updated:** 2025-10-23
**Status:** Active Development → Evolving to Custom Knowledge Management System

---

## 🎯 The Big Vision

**Build a custom, web-based knowledge management and project organization system** that serves as a high-level command center for managing multiple vaults of interconnected markdown files.

### What We're Building

**Short-term (Current):** A web dashboard that overlays on top of 9 Obsidian vaults, providing search, visualization, and management capabilities.

**Long-term (Evolution):** A full-featured custom knowledge base and project management web app that:
- Replaces Obsidian as primary interface (while keeping files Obsidian-compatible)
- Enables editing markdown files directly from web browser
- Provides custom project management views (timelines, kanban, calendars)
- Hosts on cloud (Vercel/GitHub Pages) with Git-backed version control
- Accessible anywhere (web, mobile, tablet)
- Fully tailored to your specific workflow and needs

---

## 🏗️ Core Philosophy

### 1. **Data Ownership & Portability**

**Your data is yours, forever:**
- All content stored as **plain markdown files** (`.md`)
- **YAML frontmatter** for structured metadata
- **Git repository** as source of truth
- **No proprietary formats** - readable in any text editor
- **No vendor lock-in** - can switch tools anytime

**This means:**
- ✅ Obsidian can still read files (optional backup viewer)
- ✅ VS Code can edit files (alternative editor)
- ✅ Any markdown tool works (Notion, Typora, etc.)
- ✅ Files live locally + in Git (double backup)
- ✅ Future-proof (markdown will outlive any app)

### 2. **Incremental Evolution, Not Revolution**

**Don't rebuild from scratch - evolve what exists:**
- Start with dashboard (view + search)
- Add editor (enables file modification)
- Add Git integration (version control)
- Add advanced features (project views, timelines)
- Eventually: Custom app that does everything

**Why this approach:**
- ✅ Get value immediately (usable today)
- ✅ Learn what you actually need (not what you think you need)
- ✅ Course-correct as you go (no big upfront commitment)
- ✅ No wasted work (features transfer to next version)

### 3. **Local Backup + Cloud Access**

**Best of both worlds:**
- **Local files** on computer (C:/Users/redpo/repos/Obsidian/Multi-Vault/)
  - Fast access
  - Works offline
  - Readable by Obsidian (fallback viewer)

- **Git repository** (GitHub/GitLab/self-hosted)
  - Version control (every change tracked)
  - Cloud backup (never lose data)
  - Collaboration potential (share with others)

- **Web app** (Vercel/Netlify deployment)
  - Access anywhere (laptop, phone, tablet)
  - Edit from browser
  - No installation required

**Sync workflow:**
1. Edit in web app
2. Web app commits to Git
3. Local files pull from Git (auto-sync)
4. Obsidian can read local files (if needed)

### 4. **Command Center, Not Granular Editor**

**This app is for high-level management:**
- **Overview Mode:** See all vaults at a glance (stats, activity, projects)
- **Project Focus Mode:** Deep-dive into specific project (timeline, tasks, files)
- **Quick Actions:** Search, create tasks, update timelines, manage deadlines
- **Top-Level Interactions:** Manage the vault ecosystem, not individual paragraphs

**For deep writing/editing:**
- Can still use web app editor (Monaco)
- Or use Obsidian (if preferred for long-form writing)
- Or use VS Code (if preferred for technical docs)

**The goal:** Switch between overview (dashboard) and focus (editing) seamlessly

---

## 📊 Current State (As of 2025-10-23)

### What We Have ✅

**Multi-Vault Architecture (Complete):**
- 9 Obsidian vaults with hierarchical YAML taxonomy
- 1,269 markdown files with consistent frontmatter
- 7 fundamental types (content, knowledge, project, tracking, personal, creative, reference)
- 5 vault types (Business, Knowledge, Creative, Personal, Hybrid)
- Comprehensive vault configuration documents

**RAG System (Complete):**
- ChromaDB vector database (all 1,269 files indexed)
- Hybrid search (semantic + metadata + keyword)
- Intelligent query routing (5 query types)
- Flask REST API (8 endpoints)
- Real-time file watcher (auto-indexing)
- 100% search coverage across all vaults

**Dashboard (v0.4.0 - In Progress):**
- Vault grid displaying 9 vaults
- Unified search interface (RAG Search, Claude Pro, Ollama modes)
- Real-time vault statistics
- Chat interface with streaming responses
- Mobile-responsive design
- Debug mode for query diagnostics

**Backend Services (Running):**
- Node.js Express server (port 3000)
- Flask RAG service (port 5001)
- Flask Chat service (port 5000)

**Design Agents (Complete):**
- dashboard-ui-designer agent (layout → functionality → aesthetics)
- dashboard-design-reviewer agent (validates quality at each milestone)

### What's Missing (Next Steps) ⏳

**Critical Features:**
- ❌ Markdown editor (can't edit files from dashboard yet)
- ❌ File creation/deletion (can only view, not modify)
- ❌ YAML frontmatter editor (can't update metadata)
- ❌ Git integration (no version control from app)
- ❌ Project timeline views (no visual timelines/kanban)
- ❌ Advanced project management (tasks, deadlines, calendars)

**These are the 20% that turn dashboard → custom app**

---

## 🚀 Evolution Path: Dashboard → Custom App

### Phase 1: Current Dashboard (✅ ~80% Complete)
**Goal:** Usable dashboard for viewing and searching vaults

**What we have:**
- ✅ Vault overview (9 vaults, stats, status)
- ✅ RAG search (hybrid search across all files)
- ✅ File browsing (view files, folders, structure)
- ✅ Real-time data display
- ✅ Mobile-responsive UI

**What we're finishing:**
- ⏳ UI/UX design polish (using dashboard-ui-designer agent)
- ⏳ Overview mode layout
- ⏳ Project focus mode (separate page for project deep-dives)

**Timeline:** 1-2 weeks

---

### Phase 2: Add Editor (⏳ Next Priority)
**Goal:** Enable file editing from web interface

**What to add:**
- Monaco editor component (VS Code's editor in browser)
- Split view (edit + markdown preview)
- YAML frontmatter editor (visual form for metadata)
- File creation/deletion
- Auto-save functionality
- `/api/save-file` endpoint (write to filesystem)

**Technical approach:**
```javascript
// Frontend: Monaco editor
const editor = monaco.editor.create(container, {
  value: fileContent,
  language: 'markdown',
  theme: 'vs-dark'
});

// Backend: Save endpoint
app.post('/api/save-file', async (req, res) => {
  await fs.writeFile(req.body.path, req.body.content);
  res.json({ success: true });
});
```

**Timeline:** 1-2 weeks
**Complexity:** Low (well-documented libraries)

---

### Phase 3: Git Integration (⏳ After Editor)
**Goal:** Version control, cloud backup, collaboration

**What to add:**
- Git commit on save (every edit = commit)
- Push to GitHub/GitLab
- Pull updates from Git
- View commit history
- Rollback to previous versions (git checkout)
- Conflict detection/resolution

**Technical approach:**
```javascript
// Use simple-git npm package
const git = require('simple-git')();

await git.add(filePath);
await git.commit(`Update ${filePath}`);
await git.push();
```

**Timeline:** 1 week
**Complexity:** Medium (Git basics are simple, conflict resolution is harder)

---

### Phase 4: Advanced Project Management (⏳ Future)
**Goal:** Custom views for timelines, tasks, deadlines

**What to add:**
- **Timeline View:** Gantt chart for project milestones (Chart.js Timeline)
- **Kanban Board:** Drag-and-drop task management (react-beautiful-dnd)
- **Calendar View:** Deadline tracking (FullCalendar)
- **Project Analytics:** Stats, progress tracking, insights
- **Task Management:** Create, assign, complete tasks
- **Deadline Alerts:** Notifications for upcoming deadlines

**Data source:**
- Parse PROJECT-STATUS.md files
- Query RAG for files with `deadline:` YAML field
- Aggregate tasks across vaults
- Real-time updates (WebSocket or polling)

**Timeline:** 2-3 months (iterative feature additions)
**Complexity:** High (requires design + backend work)

---

### Phase 5: Full Custom App (⏳ Long-term)
**Goal:** Production-ready knowledge management system

**Potential features:**
- Authentication (if multi-user)
- Real-time collaboration (Operational Transform or CRDT)
- Mobile app (PWA or React Native)
- API for integrations (Zapier, webhooks)
- Advanced analytics (vault insights, productivity metrics)
- AI assistance (Claude/GPT integration for summarization, suggestions)
- Public knowledge base option (share select vaults publicly)

**Timeline:** 4-6 months
**Complexity:** Very High (full product development)

---

## 🔄 Tech Stack Evolution

### Current Stack (Dashboard v0.4.0)
- **Frontend:** Vanilla JavaScript + HTML + CSS
- **Backend:** Node.js (Express) + Python (Flask)
- **Database:** ChromaDB (vector store)
- **Deployment:** Local (ports 3000, 5000, 5001)

**Pros:**
- ✅ Simple, fast to develop
- ✅ No build step
- ✅ Easy to understand

**Cons:**
- ⚠️ Hard to scale (vanilla JS gets messy)
- ⚠️ No component reusability
- ⚠️ Manual DOM manipulation

---

### Future Stack (Custom App - Recommended)

**When current stack feels limiting (Phase 4+), consider migration to:**

**Frontend:**
- **Next.js 14** (React framework)
  - Server-side rendering (SSR) for speed
  - File-based routing (pages = vault structure)
  - API routes (no separate backend)
  - Built-in markdown rendering
  - Vercel deployment (one-click)

**Backend:**
- **Next.js API Routes** (replace Express)
- **Keep Flask RAG service** (microservice for vector search)
- **Postgres or SQLite** (metadata index for fast queries)

**Editor:**
- **Monaco Editor** (same as current plan)

**Visualization:**
- **Chart.js** → **Recharts** (React-native charts)
- **react-beautiful-dnd** (drag-and-drop kanban)
- **FullCalendar** (calendar view)

**Deployment:**
- **Vercel** (free tier: unlimited bandwidth, auto-deploy)
- **ChromaDB** hosted separately (Fly.io, Railway, or Pinecone)

**Migration Strategy:**
- ✅ Reuse RAG backend (Flask service stays)
- ✅ Port features incrementally (not big-bang rewrite)
- ✅ Keep data format (markdown + YAML, no changes)
- ✅ Rebuild UI in React (component-based, scalable)

**Timeline for migration:** 2-3 weeks (if/when needed)

---

## 📋 Key Architectural Decisions

### 1. Data Flow Architecture

**Question:** How does dashboard read vault data?

**Current Answer (To Be Validated):**
- **Vault metadata:** Scan filesystem, count files, extract stats
- **File content:** Read directly from filesystem on-demand
- **Search:** Query ChromaDB vector database (RAG service)
- **Project data:** TBD (need to design project detection system)

**Options for Project Detection:**
- **Option A:** Vault = Project (e.g., ThistleRidgeHall.vault = ThistleRidgeHall project)
- **Option B:** YAML metadata (`type: project` in frontmatter)
- **Option C:** Special files (PROJECT-STATUS.md, PROJECT-OVERVIEW.md)
- **Option D:** Hybrid (combination of above)

**Decision Pending:** Will design during Phase 4 (Project Management features)

---

### 2. Vault Editing Safety

**Question:** How to safely edit Obsidian vaults from web app?

**Critical Requirements:**
- ✅ No data loss (backups, version control)
- ✅ No file corruption (atomic writes)
- ✅ Conflict resolution (if editing same file in Obsidian + web app)
- ✅ Undo/rollback (Git history)

**Proposed Approach:**
1. **Atomic writes:** Use `fs.writeFile` with temp file + rename (never partial writes)
2. **Git commits:** Every save = Git commit (instant version history)
3. **File locking:** Detect if file open in Obsidian (warn user)
4. **Conflict UI:** If Git pull has conflicts, show diff + let user choose version
5. **Backup strategy:** Local files + Git remote = double backup

**Implementation:** Phase 2 (Editor) + Phase 3 (Git)

---

### 3. Project Definition System

**Question:** How does system identify what's a "project"?

**Current Thinking:**
- **Projects span multiple files** (not just one document)
- **Projects have timelines** (start date, milestones, deadlines)
- **Projects have tasks** (actionable items with status)
- **Projects have scope** (clear boundaries, deliverables)

**Potential Detection Methods:**

**Method 1: Vault = Project**
- Simple, clear boundaries
- Works for dedicated vaults (ThistleRidgeHall, Praxis)
- Doesn't work for multi-project vaults (Business-Incubator)

**Method 2: YAML Metadata**
```yaml
---
type: project
project-name: Multi-Vault Architecture Migration
start-date: 2025-10-22
deadline: 2025-11-15
status: in-progress
---
```
- Flexible, works across vaults
- Requires manual tagging
- Easy to aggregate (query RAG for `type: project`)

**Method 3: Special Files**
- Look for PROJECT-STATUS.md, PROJECT-OVERVIEW.md
- Parse structured sections (phases, milestones, tasks)
- Auto-detect project from file patterns

**Recommended: Hybrid (Method 2 + 3)**
- Use YAML `type: project` for project files
- Parse PROJECT-*.md files for timeline/task data
- Aggregate across vaults using RAG queries

**Decision Pending:** Will finalize during Phase 4 design

---

## 🎨 Design Principles

### User Requirements (Success Criteria)

**Every feature must satisfy:**
1. ✅ **Speed** - Fast loading, responsive interactions, minimal lag
2. ✅ **Information Density** - Show relevant data without clutter
3. ✅ **No Clutter** - Every element must serve a purpose
4. ✅ **Clear Visualization** - Charts, timelines that communicate instantly
5. ✅ **Practical Use** - Enable real actions (not just viewing)

### Minimalist Aesthetic (2025 Best Practices)

**Design Standards:**
- **Data-Ink Ratio:** Remove anything that doesn't contribute to understanding (Tufte)
- **Visual Hierarchy:** Most important info stands out (size, color, position)
- **Limited Color Palette:** 2-3 primary colors + neutrals
- **Simple Charts:** Bar, line, pie, timeline (no 3D, no dual-axis)
- **Whitespace:** Generous spacing, not cramped
- **Typography:** Clear hierarchy (H1 > H2 > H3), readable sizes (14px+ body)

**Accessibility (WCAG 2.1 AA):**
- Color contrast ≥4.5:1 (text), ≥3:1 (large text)
- Keyboard navigation (all features accessible via Tab/Enter)
- ARIA labels (screen reader support)
- Skip to content link
- No keyboard traps

---

## 🗺️ Roadmap Summary

| Phase | Goal | Timeline | Status |
|-------|------|----------|--------|
| **Phase 1** | Polish dashboard UI | 1-2 weeks | ⏳ In Progress |
| **Phase 2** | Add markdown editor | 1-2 weeks | ⏳ Next |
| **Phase 3** | Git integration | 1 week | ⏳ Future |
| **Phase 4** | Project management views | 2-3 months | ⏳ Future |
| **Phase 5** | Full custom app | 4-6 months | ⏳ Long-term |

**Current Focus:** Phase 1 (UI design with dashboard-ui-designer agent)

---

## 💡 Why This Approach Works

### 1. **No Data Migration Risk**
- Keep existing markdown files
- Obsidian still works (fallback)
- Can switch between tools anytime
- Git = ultimate safety net

### 2. **Incremental Value**
- Dashboard useful today (view + search)
- Editor makes it more useful (edit files)
- Git makes it safer (version control)
- Project views make it powerful (custom workflows)

### 3. **Learn as You Build**
- Use dashboard for 2 weeks → learn what you need
- Add editor → see how editing workflow feels
- Add project views → discover what views matter most
- **No big upfront commitment**, iterate based on reality

### 4. **Future-Proof**
- Markdown files outlive any app
- Git = open standard (works with any tool)
- Web-based = accessible anywhere
- Can migrate to different tech stack later (data is separate from app)

---

## 🎯 Success Definition

**This project succeeds when:**

**Short-term (3 months):**
- ✅ Dashboard replaces Obsidian for overview tasks
- ✅ Can edit files from web browser
- ✅ Git commits happen automatically (version control working)
- ✅ Projects visible with timelines/tasks
- ✅ Accessible from phone/tablet (mobile-responsive)

**Long-term (6-12 months):**
- ✅ Obsidian is optional (only used for deep writing if preferred)
- ✅ Custom app is primary interface (80% of work happens here)
- ✅ Project management features replace external tools (Notion, Trello)
- ✅ Knowledge base is accessible anywhere (cloud-hosted)
- ✅ System is fast, reliable, tailored to your exact workflow

**Ultimate Success:**
- ✅ You have complete control over your knowledge system
- ✅ It works exactly how you want (no compromises)
- ✅ Data is yours forever (markdown + Git)
- ✅ Can evolve indefinitely (add features as needed)

---

## 📚 Related Documentation

- **[README.md](README.md)** - Project overview, quick start, current features
- **[ROADMAP.md](ROADMAP.md)** - Detailed roadmap with milestones
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture decisions (to be created)
- **[.claude/agents/README.md](.claude/agents/README.md)** - Design agent documentation

---

**This vision document is living - update as the project evolves!**

**Last Updated:** 2025-10-23
**Next Review:** After Phase 1 completion (dashboard UI polish)
