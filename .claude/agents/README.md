# Dashboard Design Sub-Agents

Two specialized agents for designing and reviewing the Multi-Vault Dashboard UI/UX.

## Agents

### 1. **dashboard-ui-designer**
**Purpose:** Design and implement minimalist, information-dense dashboard interfaces

**Use when:**
- Starting new dashboard design work
- Need to create layouts, wireframes, mockups
- Implementing functionality (data display, interactions)
- Adding aesthetic polish (styling, animations)

**Workflow:**
1. **Phase 1 - Layout:** Structure and information architecture
2. **Phase 2 - Functionality:** Wire up data, implement interactions
3. **Phase 3 - Aesthetics:** Polish visuals, responsive design, accessibility

**Design Philosophy:**
- Speed (fast loading, responsive)
- Information density (no clutter)
- Clear visualization (charts, timelines)
- Practical use (enable real actions)
- Minimalist aesthetic (2025 best practices)

---

### 2. **dashboard-design-reviewer**
**Purpose:** Review designs for accessibility, performance, usability, and quality

**Use when:**
- Designer completes a milestone (Layout, Functionality, or Aesthetics)
- Need objective validation against standards
- Want to check WCAG 2.1 accessibility compliance
- Testing responsive design across viewports
- Validating performance and usability

**Review Checkpoints:**
1. **Milestone 1 - Layout:** Information architecture, visual hierarchy, structure
2. **Milestone 2 - Functionality:** Interactions, performance, data display
3. **Milestone 3 - Aesthetics:** Visual polish, accessibility (WCAG 2.1 AA), responsive design

**Validation Criteria:**
- User requirements (speed, information, clarity, practicality)
- Accessibility standards (WCAG 2.1 Level AA)
- Performance metrics (load times, responsiveness)
- Minimalist principles (clean, purposeful design)
- Usability heuristics (intuitive navigation, error prevention)

---

## How to Use

### Using the `/agents` Command
```bash
# In Claude Code, type:
/agents

# This opens the agent management interface where you can:
# - View available agents
# - Edit agent configurations
# - Create new agents
```

### Invoking Agents Directly

**Option 1: Use Task tool with agent name**
```
I want the dashboard-ui-designer agent to start working on the layout for the overview page
```

**Option 2: Reference by file**
The agent system will automatically find agents in `.claude/agents/` folder.

### Recommended Workflow

```
1. User → dashboard-ui-designer: "Start Phase 1 - Create layout for overview page"
   ├─ Designer asks for design references
   ├─ Designer creates wireframe/mockup
   └─ Designer presents layout for review

2. User → dashboard-design-reviewer: "Review the layout milestone"
   ├─ Reviewer tests with Playwright
   ├─ Reviewer provides detailed feedback
   └─ Reviewer approves or requests changes

3. If changes needed → dashboard-ui-designer: "Address reviewer feedback"
   └─ Designer implements fixes

4. User → dashboard-ui-designer: "Proceed to Phase 2 - Implement functionality"
   ├─ Designer wires up RAG integration
   ├─ Designer implements data display
   └─ Designer presents functional dashboard

5. User → dashboard-design-reviewer: "Review the functionality milestone"
   └─ [repeat review cycle]

6. User → dashboard-ui-designer: "Proceed to Phase 3 - Add aesthetic polish"
   └─ [repeat design → review → refine cycle]

7. Final approval → Dashboard complete!
```

---

## Tech Stack (Configured in Agents)

**Frontend:**
- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Data visualization charts
- **Vanilla JavaScript** - Fast, no heavy frameworks

**Backend (Existing):**
- **Node.js (Express)** - Main server (port 3000)
- **Python (Flask)** - RAG service (port 5001), Chat service (port 5000)
- **ChromaDB** - Vector database (1,269 indexed documents)

**Testing:**
- **Playwright (MCP)** - Browser automation for visual testing

---

## User Criteria (Success Metrics)

Both agents are configured to validate against these user requirements:

✅ **Speed** - Fast loading, responsive interactions, minimal lag
✅ **Information Density** - Show relevant data without clutter
✅ **No Clutter** - Every element must serve a purpose
✅ **Clear Visualization** - Charts, timelines that communicate instantly
✅ **Practical Use** - Enable real actions (add tasks, edit timelines, manage projects)

---

## Design References

The designer agent will ask for your reference images/URLs before starting work. Have ready:
- Screenshots of dashboards you like
- URLs to inspiring designs
- Sketches or wireframes (if you have them)
- Color schemes or style guides

---

## Architectural Questions (To Be Addressed)

These are documented in the agents but require separate planning:

### 1. Data Flow Architecture
How should dashboard read vault data?
- Parse PROJECT-STATUS.md files?
- Query RAG for specific YAML fields?
- Hybrid approach?

### 2. Project Definition
How does system identify "projects"?
- Vault = Project?
- YAML metadata (`type: project`)?
- Special project files (PROJECT-*.md)?

### 3. Vault Editing Capability
How to safely edit Obsidian vaults from dashboard?
- File system write operations
- YAML frontmatter updates
- Conflict resolution strategy
- Backup/rollback procedures

**Note:** Agents will design UI/UX for these features, but backend architecture needs separate planning session.

---

## Files Created

```
.claude/agents/
├── dashboard-ui-designer.md         # Designer agent configuration
├── dashboard-design-reviewer.md     # Reviewer agent configuration
└── README.md                        # This file
```

---

## Next Steps

1. ✅ **Agents Created** - Both agents are ready to use
2. ⏳ **Start Design** - Invoke dashboard-ui-designer to begin Phase 1 (Layout)
3. ⏳ **Share References** - Provide designer with reference images/URLs
4. ⏳ **Iterate** - Work through milestones: Layout → Functionality → Aesthetics
5. ⏳ **Review** - Use dashboard-design-reviewer at each milestone
6. ⏳ **Plan Architecture** - Decide on data flow, project definition, vault editing strategy
7. ⏳ **Implement Backend** - Build necessary API endpoints for vault editing
8. ⏳ **Launch** - Deploy dashboard for production use

---

**Ready to start! Invoke the dashboard-ui-designer agent when you're ready to begin the layout phase.**
