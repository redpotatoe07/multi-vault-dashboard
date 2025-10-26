# Dashboard UI Redesign: Task & Project Visualization

**Date**: 2025-10-17
**Version**: 1.0
**Status**: 📋 Design Proposal

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current State Analysis](#current-state-analysis)
3. [Design Goals](#design-goals)
4. [Layout Options](#layout-options)
5. [Component Breakdown](#component-breakdown)
6. [Vault File Structure](#vault-file-structure)
7. [Technology Stack](#technology-stack)
8. [Implementation Phases](#implementation-phases)
9. [Inspiration & References](#inspiration--references)

---

## Executive Summary

**Goal**: Transform the multi-vault dashboard into a comprehensive project management interface that visualizes tasks, deadlines, and project timelines across all vaults.

**Key Features to Add**:
- 📋 **Task Board View** - Kanban-style organization by status
- 📅 **Timeline/Gantt View** - Visual project scheduling
- 🎯 **Deadline Tracker** - At-a-glance upcoming deadlines
- 🗂️ **Vault Organization** - Color-coded, vault-specific tasks
- 📊 **Progress Indicators** - Visual task completion tracking

---

## Current State Analysis

### What We Have Now

```
┌─────────────────────────────────────────────────┐
│  Multi-Vault Dashboard                          │
│  ┌───────────────────────────────────────────┐  │
│  │ Vault Statistics                          │  │
│  │ - Red-White: 127 files                    │  │
│  │ - ThistleRidgeHall: 98 files              │  │
│  │ - Study: 45 files                         │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  ┌───────────────────────────────────────────┐  │
│  │ AI Chat Interface                         │  │
│  │ [Ask questions about your vaults...]      │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**Limitations**:
- ❌ No task visualization
- ❌ No deadline tracking
- ❌ No project timeline view
- ❌ No progress indicators
- ❌ Tasks buried in vault files

---

## Design Goals

### Primary Objectives

1. **Visibility**: See all tasks across all vaults at a glance
2. **Organization**: Group tasks by vault, status, priority, and deadline
3. **Clarity**: Visual indicators for urgency, completion, and dependencies
4. **Actionability**: Quick actions to create, update, and complete tasks
5. **Context**: Easy access to full task details in vault files

### User Needs

- ✅ "Show me what's due this week"
- ✅ "What tasks are in my Red-White vault?"
- ✅ "What's the progress on Project X?"
- ✅ "When is the Chapter 5 draft due?"
- ✅ "What's blocking this task?"

---

## Layout Options

### Option 1: **Three-Column Dashboard** (Recommended)

**Best for**: Balanced view of tasks, timeline, and details

```
┌──────────────────────────────────────────────────────────────────┐
│  Multi-Vault Dashboard                        🔔 📊 ⚙️  [@User]  │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌──────────────────────────┐  ┌─────────────┐ │
│  │             │  │                          │  │             │ │
│  │  LEFT       │  │       CENTER             │  │   RIGHT     │ │
│  │  SIDEBAR    │  │       MAIN               │  │   PANEL     │ │
│  │             │  │       CONTENT            │  │             │ │
│  │  - Vaults   │  │                          │  │  - Details  │ │
│  │  - Filters  │  │  [Task Board/Timeline]   │  │  - Calendar │ │
│  │  - Views    │  │                          │  │  - Activity │ │
│  │  - Quick    │  │                          │  │             │ │
│  │    Stats    │  │                          │  │             │ │
│  │             │  │                          │  │             │ │
│  │             │  │                          │  │             │ │
│  └─────────────┘  └──────────────────────────┘  └─────────────┘ │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

**Breakdown**:

**Left Sidebar (240px)**:
- Vault selector with icons
- View switcher (Board/Timeline/List/Calendar)
- Filters (Status, Priority, Assignee, Tags)
- Quick stats (Total tasks, Overdue, This week)

**Center Panel (Flexible)**:
- Main workspace (Kanban board, Gantt chart, or list)
- Search and sort controls
- Bulk actions toolbar

**Right Panel (320px, Collapsible)**:
- Task details on selection
- Mini calendar with deadline highlights
- Recent activity feed
- Related tasks/files

---

### Option 2: **Full-Width Kanban** (Alternative)

**Best for**: Maximum focus on task organization

```
┌──────────────────────────────────────────────────────────────────┐
│  Multi-Vault Dashboard              [Board] [Timeline] [List]    │
├──────────────────────────────────────────────────────────────────┤
│  Filters: [All Vaults ▼] [This Week ▼] [All Priorities ▼]  🔍   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   TO DO     │  │ IN PROGRESS │  │  COMPLETED  │             │
│  │   (12)      │  │    (5)      │  │    (48)     │             │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤             │
│  │ 📖 Task 1   │  │ 📖 Task 6   │  │ ✓ Task 9    │             │
│  │ Due: Oct 20 │  │ 50% done    │  │ Completed   │             │
│  │ #red-white  │  │ #thistle... │  │             │             │
│  ├─────────────┤  ├─────────────┤  │             │             │
│  │ 🎯 Task 2   │  │ 📖 Task 7   │  │             │             │
│  │ URGENT      │  │ Due: Oct 18 │  │             │             │
│  │ #study      │  │             │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

### Option 3: **Timeline-First View** (Alternative)

**Best for**: Project management with deadlines

```
┌──────────────────────────────────────────────────────────────────┐
│  Project Timeline                   [Week] [Month] [Quarter]     │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  📖 Red-White Vault                                              │
│  ├─ Chapter 5 Draft  ████████░░░░  80%  Due: Oct 25            │
│  └─ Character Bios   ████░░░░░░░░  40%  Due: Nov 5             │
│                                                                   │
│  🎯 ThistleRidgeHall Vault                                       │
│  ├─ Artwork Catalog  ██████████░░  85%  Due: Oct 22            │
│  └─ Description Tags ██░░░░░░░░░░  20%  Due: Nov 10            │
│                                                                   │
│  📚 Study Vault                                                  │
│  └─ Research Notes   ███████░░░░░  70%  Due: Oct 30            │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  OCTOBER 2025                                              │  │
│  │  Mon  Tue  Wed  Thu  Fri  Sat  Sun                        │  │
│  │        1    2    3    4    5    6                          │  │
│  │   7    8    9   10   11   12   13                          │  │
│  │  14   15   16   17🔴 18   19   20   ← Today               │  │
│  │  21   22🔵 23   24   25🔵 26   27                          │  │
│  │  28   29   30   31                                         │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Task Card

**Compact View** (Kanban):
```
┌─────────────────────────────────┐
│ 📖 Review Chapter 5             │ ← Icon + Title
│ ─────────────────────────────── │
│ 🟢 High Priority                │ ← Priority indicator
│ 📅 Due: Oct 20 (2 days)         │ ← Deadline with countdown
│ 👤 John Doe                     │ ← Assignee (if multi-user)
│ #red-white #writing             │ ← Tags (vault + custom)
│ ████████░░ 80%                  │ ← Progress bar
│ ─────────────────────────────── │
│ [View] [Edit] [Complete]        │ ← Quick actions
└─────────────────────────────────┘
```

**Expanded View** (Right panel):
```
┌─────────────────────────────────┐
│ 📖 Review Chapter 5             │
│ ─────────────────────────────── │
│                                 │
│ Status: In Progress             │
│ Priority: High                  │
│ Created: Oct 1, 2025            │
│ Due: Oct 20, 2025 (2 days!)    │
│ Vault: 📖 Red-White             │
│                                 │
│ Description:                    │
│ Review the draft of chapter 5   │
│ and make necessary revisions.   │
│ Focus on character development  │
│ in the third act.               │
│                                 │
│ Subtasks: [2/5 complete]        │
│ ✓ Read initial draft            │
│ ✓ Mark problem areas            │
│ □ Revise dialogue               │
│ □ Polish descriptions           │
│ □ Final proofread               │
│                                 │
│ Linked Files:                   │
│ → Chapter-5-Draft.md            │
│ → Character-Development-Mode.md │
│                                 │
│ [Open in Vault] [Edit Task]    │
└─────────────────────────────────┘
```

### 2. Vault Badge

```
┌──────────────────┐
│ 📖 Red-White     │  ← Icon + Name
│ 12 tasks         │  ← Task count
│ 3 overdue        │  ← Alert count
└──────────────────┘
```

### 3. Timeline Row (Gantt-style)

```
Project Name        Oct 15      Oct 22      Oct 29      Nov 5
─────────────────────────────────────────────────────────────
Chapter 5           ████████████░░░░░░░░░░░  80%  [Oct 25]
  ├─ Draft          ████████████████████████ 100% [Oct 18] ✓
  ├─ Review         ████████░░░░░░░░░░░░░░░░  60% [Oct 22]
  └─ Revisions      ░░░░░░░░░░░░░░░░░░░░░░░░   0% [Oct 25]
```

### 4. Filter Panel

```
┌─────────────────────────────┐
│ FILTERS                     │
├─────────────────────────────┤
│                             │
│ Vaults                      │
│ ☑ Red-White (12)            │
│ ☑ ThistleRidgeHall (8)      │
│ ☑ Study (5)                 │
│                             │
│ Status                      │
│ ☑ To Do (10)                │
│ ☑ In Progress (5)           │
│ ☐ Completed (48)            │
│                             │
│ Priority                    │
│ ☑ High (3)                  │
│ ☑ Medium (7)                │
│ ☑ Low (5)                   │
│                             │
│ Timeline                    │
│ ⚫ All time                  │
│ ⚪ This week                 │
│ ⚪ This month                │
│ ⚪ Overdue                   │
│                             │
│ [Clear Filters]             │
└─────────────────────────────┘
```

### 5. Quick Stats Widget

```
┌─────────────────────────────┐
│ OVERVIEW                    │
├─────────────────────────────┤
│                             │
│  25  Total Tasks            │
│  ─                          │
│  12  To Do                  │
│  ─                          │
│   5  In Progress            │
│  ─                          │
│   3  Overdue ⚠️             │
│  ─                          │
│  48  Completed ✓            │
│                             │
└─────────────────────────────┘
```

---

## Vault File Structure

### How Tasks Are Stored in Vaults

**Option A: Dedicated Tasks Folder** (Recommended)

```
Red-White.vault/
├── Tasks/
│   ├── active/
│   │   ├── Review-Chapter-5.md
│   │   ├── Character-Development.md
│   │   └── Plot-Revision.md
│   ├── completed/
│   │   ├── Chapter-4-Draft.md
│   │   └── Outline-Revision.md
│   └── archived/
│       └── Old-Ideas.md
├── Characters/
├── Locations/
└── ...
```

**Task File Format**:

```yaml
---
title: "Review Chapter 5"
type: task
status: in-progress
priority: high
created: 2025-10-01
due: 2025-10-20
progress: 80
vault: red-white
tags:
  - writing
  - chapter-5
  - high-priority
assignee: John Doe
estimated_hours: 8
actual_hours: 6.5
dependencies:
  - Chapter-4-Draft
subtasks:
  - text: "Read initial draft"
    completed: true
  - text: "Mark problem areas"
    completed: true
  - text: "Revise dialogue"
    completed: false
  - text: "Polish descriptions"
    completed: false
  - text: "Final proofread"
    completed: false
---

# Review Chapter 5

## Description

Review the draft of chapter 5 and make necessary revisions. Focus on character development in the third act.

## Notes

- The pacing feels rushed in the middle section
- Captain Novák's dialogue needs refinement
- Consider adding a scene with Běla

## Related Files

- [[Chapter-5-Draft]]
- [[Character-Development-Mode]]
- [[Captain Václav Novák]]

## Activity Log

- 2025-10-15: Started review, identified 12 areas for improvement
- 2025-10-17: Completed dialogue revisions (60% done)
```

**Option B: Inline Tasks** (Simpler, but less structured)

Tasks can live anywhere in the vault with a specific format:

```markdown
## Chapter 5 Progress

- [ ] Review Chapter 5 #task #high-priority due:2025-10-20 progress:80%
  - [x] Read initial draft
  - [x] Mark problem areas
  - [ ] Revise dialogue
  - [ ] Polish descriptions
  - [ ] Final proofread
```

**Option C: Hybrid Approach** (Most Flexible)

- Important project tasks → Dedicated task files in `Tasks/` folder
- Quick todos → Inline checkboxes in relevant files
- Dashboard indexes both types

---

## Technology Stack

### Frontend (Dashboard UI)

**Recommended**: Keep existing stack, add visualization libraries

```javascript
// Current
- Express.js (Node.js backend)
- Vanilla JavaScript (frontend)
- Marked.js (markdown rendering)

// Add for new features
- React or Vue.js (component-based UI)
  └─ Or: Web Components (lightweight alternative)

// Visualization Libraries
- React Beautiful DnD (Kanban drag-and-drop)
- FullCalendar (Calendar/timeline views)
- DHTMLX Gantt or SVAR Gantt (Gantt charts)
- Chart.js (Progress charts/analytics)
```

### Backend Enhancements

```python
# New endpoints in RAG service (Phase 3B)

/api/tasks/list                 # Get all tasks
/api/tasks/get/{id}             # Get specific task
/api/tasks/create               # Create new task
/api/tasks/update/{id}          # Update task
/api/tasks/complete/{id}        # Mark task complete
/api/tasks/delete/{id}          # Delete task

/api/tasks/by-vault/{vault}     # Filter by vault
/api/tasks/by-status/{status}   # Filter by status
/api/tasks/by-priority/{pri}    # Filter by priority
/api/tasks/overdue              # Get overdue tasks
/api/tasks/upcoming             # Get upcoming tasks

/api/tasks/stats                # Get task statistics
/api/tasks/timeline             # Get timeline data
```

### Data Indexing

**With ChromaDB (Phase 3B)**:

```python
# Task metadata stored in ChromaDB
{
  "id": "task_review_chapter_5",
  "type": "task",
  "title": "Review Chapter 5",
  "status": "in-progress",
  "priority": "high",
  "due_date": "2025-10-20",
  "vault": "red-white",
  "file_path": "Tasks/active/Review-Chapter-5.md",
  "progress": 80,
  "tags": ["writing", "chapter-5", "high-priority"],
  "created": "2025-10-01",
  "modified": "2025-10-17",
  "subtasks_total": 5,
  "subtasks_completed": 2
}
```

**Query Examples**:

```python
# Get tasks due this week
tasks = collection.query(
    where={
        "$and": [
            {"type": "task"},
            {"due_date": {"$gte": "2025-10-17"}},
            {"due_date": {"$lte": "2025-10-24"}}
        ]
    }
)

# Get high-priority tasks in Red-White vault
tasks = collection.query(
    where={
        "$and": [
            {"type": "task"},
            {"vault": "red-white"},
            {"priority": "high"},
            {"status": {"$ne": "completed"}}
        ]
    }
)
```

---

## Implementation Phases

### Phase 1: Data Structure & Backend (Week 1)

**Goal**: Establish task file format and backend API

**Tasks**:
1. Define task YAML schema
2. Create sample task files in test vault
3. Update RAG service to recognize task files
4. Add task-specific metadata extraction
5. Create task API endpoints
6. Test task CRUD operations

**Deliverables**:
- Task file format specification
- Task indexing in ChromaDB
- REST API for task operations
- Unit tests

---

### Phase 2: Basic Task List View (Week 2)

**Goal**: Display tasks in simple list format

**Tasks**:
1. Create task list component (React/Vue)
2. Add basic filters (vault, status, priority)
3. Implement task card component
4. Add "Create Task" button
5. Wire up to backend API
6. Test data loading and filtering

**Deliverables**:
- Task list page
- Filter controls
- Task detail view
- Create task form

**UI Mockup**:
```
┌──────────────────────────────────────────────────┐
│  Tasks                        [+ New Task]       │
├──────────────────────────────────────────────────┤
│  Filters: [All Vaults ▼] [Active ▼] [All Pri ▼] │
├──────────────────────────────────────────────────┤
│                                                   │
│  📖 Review Chapter 5              🟢 High        │
│  Due: Oct 20 (2 days) • Red-White • 80% done    │
│  ─────────────────────────────────────────────── │
│                                                   │
│  🎯 Artwork Catalog Update        🟡 Medium      │
│  Due: Oct 22 (4 days) • ThistleRidgeHall • 85%  │
│  ─────────────────────────────────────────────── │
│                                                   │
│  📚 Research Notes                 🔵 Low        │
│  Due: Oct 30 (12 days) • Study • 70% done       │
│                                                   │
└──────────────────────────────────────────────────┘
```

---

### Phase 3: Kanban Board View (Week 3)

**Goal**: Add drag-and-drop task board

**Tasks**:
1. Install react-beautiful-dnd (or alternative)
2. Create Kanban board component
3. Implement 3-column layout (To Do, In Progress, Complete)
4. Add drag-and-drop functionality
5. Update task status on drag
6. Add "Add task" to each column

**Deliverables**:
- Kanban board view
- Drag-and-drop task reordering
- Visual status updates

**Libraries**:
```bash
npm install react-beautiful-dnd
# or
npm install @dnd-kit/core @dnd-kit/sortable
```

---

### Phase 4: Timeline/Calendar View (Week 4)

**Goal**: Add deadline-focused views

**Tasks**:
1. Install calendar library (FullCalendar)
2. Create calendar view component
3. Display tasks on calendar by due date
4. Add color coding by vault
5. Create timeline/Gantt view
6. Add zoom controls (week/month/quarter)

**Deliverables**:
- Calendar view with tasks
- Timeline view with progress bars
- Deadline highlighting

**Libraries**:
```bash
npm install @fullcalendar/react @fullcalendar/daygrid
# or for Gantt
npm install dhtmlx-gantt
# or
npm install @svar/gantt
```

---

### Phase 5: Polish & Advanced Features (Week 5)

**Goal**: Enhance UX and add power features

**Tasks**:
1. Add task search
2. Implement bulk actions
3. Add task templates
4. Create dashboard widgets (stats, charts)
5. Add notifications for overdue tasks
6. Implement task dependencies visualization
7. Add export functionality (CSV, PDF)

**Deliverables**:
- Search and bulk actions
- Analytics widgets
- Task templates
- Export features

---

## Inspiration & References

### Design References (from Research)

**1. Modern Task Management Dashboards**

Key Patterns Observed:
- **Card-based layouts** - Tasks as draggable cards with rich metadata
- **Color coding** - Visual distinction by project, priority, or status
- **Progress indicators** - Bars, percentages, and checkmarks for quick scanning
- **Clean, minimalist design** - Whitespace, clear typography, muted colors
- **Context on hover** - Additional details appear without navigation

**2. Kanban Board Best Practices**

From Dribbble examples:
- **3-column minimum** - To Do, In Progress, Done
- **Task count badges** - Show items in each column
- **Compact card design** - Title, due date, assignee, tags
- **Quick actions** - Edit, delete, archive on hover
- **Add button per column** - Easy task creation in correct status

**3. Gantt Chart Patterns**

From SVAR Gantt and Syncfusion research:
- **Hierarchical structure** - Parent tasks with sub-tasks
- **Progress bars on timeline** - Visual completion status
- **Dependency lines** - Show task relationships
- **Zoom levels** - Day, week, month, quarter views
- **Today marker** - Clear indication of current date

**4. Dashboard Layout Trends (2024-2025)**

From design research:
- **Dark mode support** - Essential for modern apps
- **Responsive grid systems** - Adapt to screen sizes
- **Sticky headers** - Keep navigation visible when scrolling
- **Collapsible sidebars** - More workspace when needed
- **Keyboard shortcuts** - Power user efficiency

### Real-World Examples

**Influenced by**:
- **Notion** - Flexible views (Board, Table, Timeline, Calendar)
- **Trello** - Simple, intuitive Kanban interface
- **Asana** - Multiple project views with excellent UX
- **Monday.com** - Color-coded, visual project management
- **Linear** - Clean, fast, keyboard-first task management

---

## Color Palette Recommendations

### Vault Color Coding

Use distinct, accessible colors for each vault:

```
Red-White:       #E2904A (warm orange)
ThistleRidgeHall: #9B59B6 (purple)
Study:           #3498DB (blue)
```

### Priority Colors

Standard traffic light system:

```
High:     #E74C3C (red)
Medium:   #F39C12 (amber)
Low:      #27AE60 (green)
```

### Status Colors

```
To Do:        #95A5A6 (gray)
In Progress:  #3498DB (blue)
Completed:    #27AE60 (green)
Overdue:      #E74C3C (red)
Archived:     #7F8C8D (muted gray)
```

### UI Theme

**Light Mode** (Default):
```
Background:    #FFFFFF
Card:          #F8F9FA
Border:        #E9ECEF
Text:          #2C3E50
Text Light:    #7F8C8D
```

**Dark Mode** (Optional):
```
Background:    #1E1E1E
Card:          #2D2D2D
Border:        #3D3D3D
Text:          #ECEFF4
Text Light:    #A0A0A0
```

---

## Typography

**Font Stack**:
```css
/* Primary */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Monospace (for dates, IDs) */
font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
```

**Type Scale**:
```
H1 (Page title):      32px / 2rem / Bold
H2 (Section):         24px / 1.5rem / Semibold
H3 (Card title):      18px / 1.125rem / Semibold
Body:                 16px / 1rem / Regular
Small (metadata):     14px / 0.875rem / Regular
Tiny (badges):        12px / 0.75rem / Medium
```

---

## Accessibility Considerations

1. **Color Contrast**: All text meets WCAG AA standards (4.5:1 ratio)
2. **Keyboard Navigation**: Full keyboard support for all interactions
3. **Screen Readers**: Proper ARIA labels and semantic HTML
4. **Focus Indicators**: Clear visual focus states
5. **Color Independence**: Don't rely solely on color (use icons + text)

---

## Mobile Considerations

**Responsive Breakpoints**:
```
Desktop:  1200px+  (Three-column layout)
Tablet:   768-1199px  (Two-column, collapsible sidebar)
Mobile:   < 768px  (Single column, bottom nav)
```

**Mobile Adaptations**:
- Collapse sidebar to bottom navigation
- Stack task cards vertically
- Use slide-out panels for details
- Optimize touch targets (44x44px minimum)
- Swipe gestures for quick actions

---

## Next Steps

### Immediate Actions

1. **Review this document** - Discuss layout preferences and feature priorities
2. **Choose layout option** - Select between three-column, Kanban-first, or timeline-first
3. **Define task schema** - Finalize YAML frontmatter structure
4. **Create mockups** - Use Figma or similar to visualize the design
5. **Prototype** - Build a simple HTML/CSS mockup before full implementation

### Questions to Answer

1. **Single-user or multi-user?** - Affects assignee features
2. **Task dependencies?** - Do tasks block other tasks?
3. **Time tracking?** - Track estimated vs actual hours?
4. **Recurring tasks?** - Daily/weekly repeating tasks?
5. **Task comments/notes?** - Collaboration features?
6. **File attachments?** - Beyond wikilinks to vault files?
7. **Email/notifications?** - Remind users of deadlines?

---

## Estimated Timeline

**Minimum Viable Product (MVP)**:
- Phase 1 (Backend): 1 week
- Phase 2 (List View): 1 week
- **Total MVP**: 2 weeks

**Full Implementation**:
- Phases 1-5: 5 weeks
- Polish & Testing: 1 week
- **Total**: 6 weeks

**Phased Release**:
- Week 2: Basic task list (usable but limited)
- Week 3: Kanban board (major UX upgrade)
- Week 4: Timeline/calendar views (complete feature set)
- Week 5-6: Polish and advanced features

---

## Resources

### Libraries & Tools

**Kanban/Drag-and-Drop**:
- [react-beautiful-dnd](https://github.com/atlassian/react-beautiful-dnd)
- [dnd-kit](https://dndkit.com/) (modern alternative)

**Calendar/Timeline**:
- [FullCalendar](https://fullcalendar.io/)
- [React Big Calendar](https://github.com/jquense/react-big-calendar)

**Gantt Charts**:
- [SVAR Gantt](https://svar.dev/react/gantt/) (open source)
- [DHTMLX Gantt](https://dhtmlx.com/docs/products/dhtmlxGantt/)
- [Syncfusion Gantt](https://www.syncfusion.com/react-components/react-gantt-chart)

**UI Components**:
- [shadcn/ui](https://ui.shadcn.com/) (React components)
- [Radix UI](https://www.radix-ui.com/) (headless components)
- [Tailwind CSS](https://tailwindcss.com/) (utility-first CSS)

### Design Resources

- [Dribbble Dashboard Designs](https://dribbble.com/tags/task-management-dashboard)
- [Figma Community Files](https://www.figma.com/community/search?resource_type=mixed&sort_by=relevancy&query=dashboard&editor_type=all)

---

**Status**: 📋 Ready for Review and Discussion
**Next Step**: Review and decide on layout option and feature priorities
**Created**: 2025-10-17
**Version**: 1.0
