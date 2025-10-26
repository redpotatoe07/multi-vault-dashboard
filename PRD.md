# Multi-Vault Dashboard - Product Requirements Document (PRD)

## Project Overview

A locally-hosted web dashboard for accessing and managing multiple Obsidian vaults with AI-powered intelligence, providing mobile access and eventually cloud deployment capabilities.

**Current Status:** Phase 1 Complete - Basic local dashboard with dual AI integration

---

## Core Goals

1. **Mobile Access**: View and interact with vaults from iPhone/iPad when PC is on
2. **AI Intelligence**: Query vault contents using Claude Pro and Ollama
3. **Unified View**: See all vaults at once without opening each separately
4. **Future Cloud**: Deploy to cloud for access when PC is off
5. **File Operations**: Eventually support creating and editing files

---

## Technical Architecture

### Current Setup (Local)
- **Backend**: Node.js + Express server (port 3000)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **AI Integration**: Claude Code CLI + Ollama (local)
- **Vault Location**: `C:\Users\redpo\repos\Obsidian\Multi-Vault`
- **Code Location**: `C:\Users\redpo\repos\multi-vault-dashboard`

### Future Setup (Cloud)
- **Hosting**: Vercel/Netlify or Hostinger
- **Vault Storage**: GitHub repository
- **AI**: Claude API + Ollama (local fallback)
- **Authentication**: GitHub OAuth or similar

---

## Feature Roadmap

## ✅ Phase 1: Basic Dashboard (COMPLETED)

### Core Features
- [x] Node.js/Express server setup
- [x] Vault scanning and statistics
- [x] Responsive web UI (desktop + mobile)
- [x] Mobile access via local network IP
- [x] Cross-vault search functionality
- [x] Real-time vault statistics display
- [x] 8 vault support (Study, Creative-Incubator, Business-Incubator, Red-White, ThistleRidgeHall, SickRabbit, Library, Life-Systems)

### Vault Display
- [x] File count per vault
- [x] Top folders with file counts
- [x] Recent files list
- [x] Vault icons and color coding
- [x] "Vault not found" error handling

### UI/UX
- [x] Dark theme with gradient background
- [x] Responsive grid layout
- [x] Mobile-optimized design (no horizontal scroll)
- [x] iPhone/iPad compatible styling
- [x] Status indicators (connected/disconnected)
- [x] Auto-refresh every 60 seconds

---

## ✅ Phase 2: AI Integration (COMPLETED)

### Dual AI System
- [x] Ollama integration (local, fast)
- [x] Claude Code CLI integration (local, powerful)
- [x] Model selector dropdown in UI
- [x] AI status indicators (online/offline)
- [x] Vault-specific queries (filter by vault)

### Chat Interface
- [x] Chat message display with icons
- [x] User input field
- [x] Send button with loading states
- [x] Markdown rendering for AI responses
- [x] Error handling and display
- [x] Chat history in session

### AI Context & Intelligence
- [x] Deep file content reading (up to 15 files)
- [x] Folder-specific content loading
- [x] Keyword-based folder detection
- [x] Recursive file reading through nested folders
- [x] Content truncation (3000 chars per file)
- [x] Recent files with full content

---

## 🚧 Phase 3: Enhanced AI Intelligence (IN PROGRESS)
We have an issue that ollama doesn't natively read files, but we should be able to do this with python. check this video 
https://youtu.be/IsEYXyMkRF8?si=PqroRbweLHIdhMEJ
Also look at the smart chat plugin in obsidian where ollama can read the .md files
Python ollama libary: https://github.com/ollama/ollama-python
For GUI: https://github.com/open-webui/open-webui
Github page: https://github.com/ollama/ollama

### Smart Context Loading
- [ ] Remove keyword hardcoding
- [ ] Load 30-50 files by default when vault selected
- [ ] Smarter file selection algorithm:
  - [ ] Recent files (by modification date)
  - [ ] Frequently accessed files
  - [ ] Files with most links/references
  - [ ] Proportional sampling from each folder
- [ ] File content preview (first 500 chars) in listings
- [ ] Full file tree with metadata sent to AI

### Improved AI Responses
- [ ] Better prompt engineering for file discovery
- [ ] Include file structure in AI context
- [ ] AI suggests relevant files to explore
- [ ] Multi-turn conversations (remember context)
- [ ] Session-based chat history

---

## 📋 Phase 4: Advanced Features (PLANNED)

### Search & Discovery
- [ ] Semantic search (AI-powered)
- [ ] Tag-based filtering
- [ ] Date range filters
- [ ] Full-text search with snippets
- [ ] Search within specific folders
- [ ] Saved search queries

### File Operations (Read-Only First)
- [ ] View full file contents in UI
- [ ] Syntax highlighting for markdown
- [ ] Image preview support
- [ ] PDF viewer integration
- [ ] Link navigation between files

### Analytics & Insights
- [ ] File creation timeline
- [ ] Most edited files
- [ ] Vault growth over time
- [ ] Folder size visualization
- [ ] Link graph visualization
- [ ] Daily/weekly activity stats

---

## 🚀 Phase 5: Cloud Deployment (FUTURE)

### Prerequisites
- [ ] Push vaults to GitHub private repo
- [ ] Set up CI/CD pipeline
- [ ] Environment variable management
- [ ] API key storage (secrets)

### Cloud Infrastructure
- [ ] Deploy to Vercel/Netlify OR Hostinger
- [ ] Configure custom domain
- [ ] SSL/HTTPS setup
- [ ] GitHub integration for file access

### Authentication
- [ ] User login system
- [ ] GitHub OAuth integration
- [ ] Session management
- [ ] Access control per vault

### Claude API Integration
- [ ] Add Claude API support
- [ ] API key configuration
- [ ] Usage tracking/limits
- [ ] Fallback to local when available

### File Editing (Cloud)
- [ ] Edit file in browser
- [ ] Create new files
- [ ] Delete files
- [ ] Git commit on save
- [ ] Conflict resolution
- [ ] Version history

---

## 🎯 Phase 6: Advanced Cloud Features (FUTURE)

### Real-Time Sync
- [ ] WebSocket connection for live updates
- [ ] Multi-device sync
- [ ] Collaborative editing
- [ ] Conflict detection and resolution

### Mobile App
- [ ] Progressive Web App (PWA)
- [ ] Offline mode
- [ ] Mobile-optimized file editor
- [ ] Voice input for notes
- [ ] Photo upload to vaults

### Integrations
- [ ] Obsidian plugin compatibility
- [ ] Export to PDF/DOCX
- [ ] Import from Notion/Evernote
- [ ] Calendar integration
- [ ] Task management sync

---

## Known Issues & Limitations

### Current Limitations
1. **AI Context**: Claude/Ollama receive static snapshots, not live file access
2. **File Editing**: Read-only access currently
3. **Search**: Basic text search only (no semantic search)
4. **Performance**: Large vaults (>1000 files) may be slow
5. **Network**: Only accessible on local network when PC is on

### Technical Debt
- [ ] Add proper error logging
- [ ] Implement request rate limiting
- [ ] Add file caching for performance
- [ ] Optimize large file handling
- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Document API endpoints

---

## Configuration & Settings

### Current Settings
- **Port**: 3000
- **Vault Root**: `C:\Users\redpo\repos\Obsidian\Multi-Vault`
- **Max Files Per Query**: 15
- **Max Chars Per File**: 3000
- **Search Result Limit**: 20
- **Ollama Model**: gemma3
- **Claude**: Pro via CLI

### Future Configurable Settings
- [ ] Port number
- [ ] Vault locations (multiple roots)
- [ ] File limits per query
- [ ] AI model selection
- [ ] Theme customization
- [ ] Language settings

---

## Success Metrics

### Phase 1-2 (Achieved)
- ✅ Mobile access working on iPhone/iPad
- ✅ Dual AI integration functional
- ✅ All 8 vaults visible and searchable
- ✅ Markdown rendering in chat

### Phase 3 (Next Goals)
- [ ] AI responses contain actual file content 90%+ of the time
- [ ] Average query response time <5 seconds
- [ ] User can discover vault content without knowing file names

### Phase 4-5 (Future Goals)
- [ ] Cloud deployment with <2 second load time
- [ ] 99% uptime on cloud hosting
- [ ] File editing with <1 second save time
- [ ] Support for vaults up to 10,000 files

---

## Development Workflow

### Adding New Features
1. Update this PRD with feature details
2. Create feature branch if needed
3. Implement and test locally
4. Update documentation
5. Check off in PRD
6. Commit with descriptive message

### Testing Checklist
- [ ] Test on desktop (Chrome/Firefox)
- [ ] Test on mobile (iPhone Safari)
- [ ] Test with both Claude and Ollama
- [ ] Test with all 8 vaults
- [ ] Test error cases
- [ ] Check console for errors

---

## Resources & Dependencies

### Current Dependencies
```json
{
  "express": "^4.18.2"
}
```

### Future Dependencies (Planned)
- `marked` - Markdown parsing (if needed)
- `ws` - WebSocket support
- `dotenv` - Environment variables
- `@octokit/rest` - GitHub API
- `passport` - Authentication

### External Services
- **Claude Code CLI** (local)
- **Ollama** (local)
- **Claude API** (future, cloud)
- **GitHub** (future, cloud hosting)

---

## Questions & Decisions Needed

### Open Questions
1. **Cloud Hosting Choice**: Vercel vs Netlify vs Hostinger?
   - Vercel: Best for Next.js, serverless functions
   - Netlify: Similar to Vercel, good CI/CD
   - Hostinger: Traditional hosting, more control

2. **Authentication Method**: GitHub OAuth vs custom auth?
   - GitHub: Easy integration with repo access
   - Custom: More control, but more work

3. **File Storage**: Keep vaults in Git or use cloud storage?
   - Git: Version control, but large files issue
   - Cloud Storage: Better for large files, but harder sync

4. **AI Strategy**: Claude API only or keep Ollama option?
   - Claude API: Consistent, powerful, but paid
   - Ollama: Free, but requires local setup

### Decision Log
- **2025-01-12**: Chose dual AI system (Ollama + Claude Code CLI)
- **2025-01-12**: Decided on keyword-based folder detection (may revise)
- **2025-01-12**: Chose to improve context loading over multi-turn conversations

---

## Version History

- **v0.1.0** (2025-01-12): Initial prototype, basic dashboard
- **v0.2.0** (2025-01-12): Added Ollama integration
- **v0.3.0** (2025-01-12): Added Claude Code CLI integration
- **v0.4.0** (2025-01-12): Deep file content reading, markdown rendering

---

## Contact & Support

**Project Location**: `C:\Users\redpo\repos\multi-vault-dashboard`
**Documentation**: `Business-Incubator.vault/Projects/Multi-Vault-Dashboard/`
**Issues**: Track in this document or separate issue tracker (TBD)

---

*Last Updated: 2025-01-12*
*Status: Active Development - Phase 3*
