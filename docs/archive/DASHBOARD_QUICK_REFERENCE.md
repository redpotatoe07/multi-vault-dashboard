# Dashboard UI Redesign - Quick Reference

**TL;DR**: Transform your multi-vault dashboard into a visual task & project management system

---

## 🎯 What We're Building

**Current**: Static vault statistics + AI chat
**Future**: Dynamic task board + timeline + deadline tracking + progress visualization

---

## 🎨 Three Layout Options

### Option 1: Three-Column (Recommended) ⭐

```
┌──────────────────────────────────────────────┐
│ [Sidebar]  [Main Content]  [Details Panel]  │
│  Vaults    Task Board      Task Details     │
│  Filters   or Timeline     Calendar          │
│  Stats     or List         Activity          │
└──────────────────────────────────────────────┘
```
**Best for**: Balanced workflow, maximum information density

### Option 2: Full-Width Kanban

```
┌──────────────────────────────────────────────┐
│ [     TO DO     ] [  IN PROGRESS  ] [ DONE ] │
│  Drag and drop tasks between columns         │
└──────────────────────────────────────────────┘
```
**Best for**: Pure task management, Trello-like simplicity

### Option 3: Timeline-First

```
┌──────────────────────────────────────────────┐
│ Project 1  ██████████░░░░░░  Oct 25          │
│ Project 2  ████░░░░░░░░░░░░  Nov 5           │
│ [Calendar with deadline markers]             │
└──────────────────────────────────────────────┘
```
**Best for**: Deadline-focused, project timeline visualization

---

## 📁 How Tasks Work in Vaults

### Task File Example

**Location**: `Red-White.vault/Tasks/active/Review-Chapter-5.md`

```yaml
---
title: "Review Chapter 5"
type: task
status: in-progress
priority: high
due: 2025-10-20
progress: 80
vault: red-white
tags: [writing, chapter-5]
subtasks:
  - text: "Read draft"
    completed: true
  - text: "Revise dialogue"
    completed: false
---

# Review Chapter 5

Description and notes go here...
```

### What You Can Track

- ✅ **Status**: To Do → In Progress → Complete
- ✅ **Priority**: High / Medium / Low
- ✅ **Due dates**: With countdown and urgency colors
- ✅ **Progress**: Percentage and visual bars
- ✅ **Vault**: Which vault the task belongs to
- ✅ **Tags**: Custom categorization
- ✅ **Subtasks**: Break down complex tasks
- ✅ **Dependencies**: Link related tasks

---

## 🛠️ Implementation Path

### Phase 1: Backend (1 week)
- Define task YAML format
- Update RAG service to index tasks
- Create task API endpoints

### Phase 2: Basic List (1 week) → **MVP**
- Display tasks in simple list
- Add filters (vault, status, priority)
- Create/edit/complete tasks

### Phase 3: Kanban Board (1 week)
- Add drag-and-drop columns
- Visual task cards
- Quick status updates

### Phase 4: Timeline View (1 week)
- Calendar with tasks
- Gantt-style project view
- Deadline visualization

### Phase 5: Polish (1 week)
- Search, bulk actions
- Analytics widgets
- Export features

**Total MVP**: 2 weeks
**Full Implementation**: 5-6 weeks

---

## 🎨 Visual Design

### Task Card

```
┌─────────────────────────────────┐
│ 📖 Review Chapter 5             │
│ ─────────────────────────────── │
│ 🟢 High Priority                │
│ 📅 Due: Oct 20 (2 days!)        │
│ #red-white #writing             │
│ ████████░░ 80%                  │
│ [View] [Edit] [Complete]        │
└─────────────────────────────────┘
```

### Color System

**Vaults**:
- Red-White: `#E2904A` (orange)
- ThistleRidgeHall: `#9B59B6` (purple)
- Study: `#3498DB` (blue)

**Priority**:
- High: `#E74C3C` (red)
- Medium: `#F39C12` (amber)
- Low: `#27AE60` (green)

**Status**:
- To Do: Gray
- In Progress: Blue
- Completed: Green
- Overdue: Red (with alert icon)

---

## 🔑 Key Features

### For You
- 📊 **Dashboard widgets**: See task stats at a glance
- 🔍 **Smart filters**: Find tasks by vault, status, priority, deadline
- 📅 **Multiple views**: Board, Timeline, List, Calendar
- 🎯 **Deadline tracking**: Visual countdown and alerts
- 📈 **Progress tracking**: See completion percentages
- 🏷️ **Tags & organization**: Custom categorization

### Power Features
- ⚡ **Keyboard shortcuts**: Fast task creation and navigation
- 📱 **Mobile responsive**: Works on phone/tablet
- 🌙 **Dark mode**: Easy on the eyes
- 🔄 **Real-time sync**: Changes reflected immediately
- 📤 **Export**: Download tasks as CSV/PDF
- 🔗 **Link to vault files**: Jump to full task details

---

## 💻 Tech Stack

### Frontend
- **Current**: Vanilla JS
- **Upgrade to**: React or Vue.js
- **Add**:
  - React Beautiful DnD (Kanban)
  - FullCalendar (Calendar view)
  - SVAR Gantt (Timeline)
  - Chart.js (Analytics)

### Backend
- **Keep**: Express.js (Node.js)
- **Add**: Task API endpoints
- **Use**: ChromaDB (from Phase 3B) for task indexing

---

## 🤔 Questions to Decide

Before starting, we need to answer:

1. **Which layout do you prefer?**
   - Three-column, Kanban-first, or Timeline-first?

2. **Single-user or multi-user?**
   - Do you need assignee/collaboration features?

3. **Task dependencies?**
   - Should tasks be able to block other tasks?

4. **Time tracking?**
   - Track estimated vs actual hours worked?

5. **Recurring tasks?**
   - Need daily/weekly repeating tasks?

6. **Priority?**
   - Implement alongside Phase 3B RAG, or wait until after?

---

## 📊 What It Looks Like

### Dashboard View (Three-Column)

```
┌───────────────────────────────────────────────────────────┐
│  Multi-Vault Dashboard                         [@User] ⚙️  │
├───────────────────────────────────────────────────────────┤
│                                                            │
│  ┌─────────┐  ┌──────────────────────┐  ┌──────────────┐ │
│  │ VAULTS  │  │    TO DO (10)        │  │ TASK DETAILS │ │
│  │         │  ├──────────────────────┤  │              │ │
│  │ 📖 Red  │  │ 📖 Review Ch 5       │  │ Review Ch 5  │ │
│  │   White │  │ Due: Oct 20  🟢 High │  │ ────────────│ │
│  │  (12)   │  │ ████████░░ 80%       │  │ In Progress  │ │
│  │         │  ├──────────────────────┤  │ Due: 2 days  │ │
│  │ 🎯 Thist│  │ 🎯 Artwork Update    │  │              │ │
│  │   leRid │  │ Due: Oct 22  🟡 Med  │  │ Subtasks:    │ │
│  │   ge (8)│  │ ██████████░ 85%      │  │ ☑ Read draft │ │
│  │         │  └──────────────────────┘  │ ☐ Revise     │ │
│  │ VIEWS   │                            │ ☐ Proofread  │ │
│  │ • Board │  ┌──────────────────────┐  │              │ │
│  │ • Time  │  │  IN PROGRESS (5)     │  │ [Open File]  │ │
│  │ • List  │  ├──────────────────────┤  └──────────────┘ │
│  │ • Cal   │  │ (Tasks here...)      │                   │
│  └─────────┘  └──────────────────────┘                   │
│                                                            │
│               ┌──────────────────────┐                    │
│               │   COMPLETED (48)     │                    │
│               ├──────────────────────┤                    │
│               │ ✓ Chapter 4 Draft    │                    │
│               │ ✓ Outline Revision   │                    │
│               └──────────────────────┘                    │
└───────────────────────────────────────────────────────────┘
```

---

## 🚀 Next Steps

1. **Read**: [DASHBOARD_UI_REDESIGN.md](DASHBOARD_UI_REDESIGN.md) (full spec)
2. **Review**: Layout options and features
3. **Decide**: Answer the questions above
4. **Discuss**: Any concerns or additional requirements
5. **Start**: When ready, we can begin Phase 1

---

## 📚 Related Documents

- **[DASHBOARD_UI_REDESIGN.md](DASHBOARD_UI_REDESIGN.md)** - Full design specification
- **[PHASE_3B_IMPLEMENTATION_PLAN.md](PHASE_3B_IMPLEMENTATION_PLAN.md)** - RAG system plan (synergistic with this)
- **[SESSION_SUMMARY.md](SESSION_SUMMARY.md)** - What we did this session

---

**Created**: 2025-10-17
**Status**: Ready for review
**Estimated Timeline**: 5-6 weeks for full implementation, 2 weeks for MVP
