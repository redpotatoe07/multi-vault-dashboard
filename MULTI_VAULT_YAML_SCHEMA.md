# Multi-Vault YAML Schema & Standards

**Created:** 2025-10-21
**Version:** 1.0
**Purpose:** Unified YAML conventions for RAG optimization across all 9 vaults

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Vault Profiles](#vault-profiles)
3. [Core Schema (Cross-Vault)](#core-schema-cross-vault)
4. [Vault-Specific Extensions](#vault-specific-extensions)
5. [Property Dictionary](#property-dictionary)
6. [RAG Optimization Strategy](#rag-optimization-strategy)
7. [Migration Plan](#migration-plan)
8. [Validation Rules](#validation-rules)

---

## 🎯 Executive Summary

### Problem Identified
**Query:** "artworks" in ThistleRidgeHall
**Expected:** 47 files
**Actual:** 20 files found
**Root Cause:** Semantic gap between natural language queries and YAML metadata

### Vault Inventory
| Vault | Document Count | Primary Type | Key YAML Patterns |
|-------|---------------|--------------|-------------------|
| **ThistleRidgeHall** | 279 | Products (Art) | `type: product`, etsy-*, botanical-* |
| **Business-Incubator** | 326 | Projects/Images | `type: source-image`, project-*, copyright_status |
| **Library** | 183 | Notes/Ideas | `id`, `title`, timestamps |
| **Creative-Incubator** | 125 | Projects | `type: progress-tracking`, project-status |
| **Red-White** | 114 | Characters/Story | `Group`, character attributes |
| **Life-Systems** | 92 | Administration | Minimal/no YAML |
| **Study** | 84 | Lessons | `type: lesson-study`, hsk-level, completion-status |
| **SickRabbit** | 38 | Products/Concepts | `type: product`, category, project, note-type |
| **Praxis** | 28 | Content Planning | `type: schedule`, project, status, priority |

**Total Documents:** 1,269 across 9 vaults

---

## 🏛️ Vault Profiles

### ThistleRidgeHall (Etsy Art Business)
**Purpose:** Digital art product listings
**Document Types:** Artwork product pages
**YAML Sophistication:** ⭐⭐⭐⭐⭐ (Highly structured)

**Typical Structure:**
```yaml
type: [product]
category: artwork              # MISSING - should add
status: [listed | draft | archived]
collection: "Collection Name"
artist: "Artist Name"
SKU: TRH-Collection-###
cover: "[[image.jpg]]"
archive-note-id: ART.V.####.###
project: [bp-002]

# Etsy metadata (comprehensive)
etsy-type: "Digital item"
etsy-category: "Art & Collectibles > Prints > Digital Prints"
etsy-primary-color: Blue
etsy-secondary-color: Brown
etsy-home-style: [Rustic & primitive, Cottage]
etsy-subject: [Landscape & scenery]
etsy-occasion: Housewarming
etsy-room: "Living Room, Office"
etsy-orientation: Horizontal

# Botanical (when applicable)
botanical-common-names: "species name"
botanical-latin-names: "Latin name"

# Scheduling
etsy-schedule:
pinterest-schedule:
pinterest-uploaded: false
```

**Issues:**
- ❌ Missing `category: artwork` (causes "artworks" query to fail)
- ❌ No semantic `tags:` array for RAG
- ❌ No `content-type` or `medium` properties

---

### Business-Incubator (Business Projects)
**Purpose:** Business project management and source image cataloging
**Document Types:** Projects, source images, business planning
**YAML Sophistication:** ⭐⭐⭐⭐ (Structured)

**Typical Structure (Source Images):**
```yaml
type: [source-image]
id: IMG###
artwork_title:
year: "1930"
artist: Name
source_url: https://...
source_website: [Wikimedia]
subject: [sport, skiing]
category: [genre, documentary]
medium: [photograph]
copyright_status: [Creative Commons]
filename: image.jpg
tags: [source-image]
```

**Typical Structure (Projects):**
```yaml
type: [project]
project-status: [active | planning | archived]
status: [in-progress]
priority: [high | medium | low]
tags: [project-name]
```

---

### Study (Language Learning)
**Purpose:** Chinese language study materials
**Document Types:** Lessons, flashcards, practice materials
**YAML Sophistication:** ⭐⭐⭐⭐ (Structured)

**Typical Structure:**
```yaml
type: lesson-study
lesson-number: L01
lesson-title: "Lesson Name"
lesson-url: "https://..."
hsk-level: 3
completion-status: in-progress
sections-completed: 0
total-sections: 4
date-started:
date-completed:
active-lesson: false
tags: [chinese-study, lesson, hsk-3]
```

---

### Creative-Incubator (Creative Projects)
**Purpose:** Creative project tracking (writing, music, art)
**Document Types:** Dashboards, project notes
**YAML Sophistication:** ⭐⭐⭐ (Moderate)

**Typical Structure:**
```yaml
type: progress-tracking
vault: creative-incubator
system-type: progress-dashboard
created: 2024-09-28
tags: [creative-progress, dashboard, tracking]
```

---

### SickRabbit (Product Development)
**Purpose:** Art product concepts and development
**Document Types:** Product ideas, artwork series concepts
**YAML Sophistication:** ⭐⭐⭐⭐ (Structured)

**Typical Structure:**
```yaml
type: [product]
category: [projects]
project: [bp-001]
note-type: [idea | concept | execution]
status: [concept-dev | in-progress | completed]
claude-context: [brainstorming]
tags: []
created: 2025-08-23 09:20
```

---

### Praxis (Content Planning)
**Purpose:** Content creation schedule and planning
**Document Types:** Schedules, content calendars, theme planning
**YAML Sophistication:** ⭐⭐⭐ (Moderate)

**Typical Structure:**
```yaml
project: [Faceless-Videos]
type: [schedule | theme-calendar]
tags: [content-calendar, schedule]
created: 2025-10-16
updated: 2025-10-21
status: [active]
priority: [high]
```

---

### Red-White (Fiction Writing)
**Purpose:** Character development and story planning
**Document Types:** Character sheets, story elements
**YAML Sophistication:** ⭐ (Minimal)

**Typical Structure:**
```yaml
Group: Group Name
# Most metadata in body text, not YAML
```

---

### Library (Idea Collection)
**Purpose:** Brain dump, fleeting notes, idea capture
**Document Types:** Quick notes, ideas, references
**YAML Sophistication:** ⭐⭐ (Basic)

**Typical Structure:**
```yaml
id: "uuid"
title: "Note Title"
tags: []
source: ""
source_title: ""
source_description: ""
source_image_url: ""
created_date: "2025-10-20"
modified_date: "2025-10-20"
```

---

### Life-Systems (Personal Admin)
**Purpose:** Personal administration and daily operations
**Document Types:** Admin notes, daily notes
**YAML Sophistication:** ⭐ (Minimal/None)

**Typical Structure:**
```yaml
# Often no YAML at all - plain text documents
```

---

## 🌐 Core Schema (Cross-Vault)

### Tier 1: Universal Properties (All Vaults)

These properties should be present (or considered) for ALL documents:

```yaml
# === DOCUMENT CLASSIFICATION ===
type:                          # REQUIRED - Primary document type
  - [product | note | lesson | project | character | schedule | idea]

category:                      # RECOMMENDED - Secondary classification
  - [artwork | source-image | writing | reference | admin]

tags:                          # RECOMMENDED - Semantic keywords for RAG
  - keyword1
  - keyword2

# === METADATA ===
title:                         # OPTIONAL - Explicit title (if different from filename)
created:                       # RECOMMENDED - Creation date (YYYY-MM-DD or ISO)
updated:                       # OPTIONAL - Last update date
status:                        # RECOMMENDED - Document status
  - [draft | active | completed | archived | listed]

# === RELATIONSHIPS ===
related-notes:                 # OPTIONAL - Links to related documents
project:                       # OPTIONAL - Associated project(s)
  - project-name
```

### Tier 2: Content-Type Properties

For better RAG understanding of document nature:

```yaml
content-type:                  # NEW - What is this fundamentally?
  - [visual | textual | mixed | data | reference]

medium:                        # For creative works
  - [digital-print | photograph | oil-painting-style | text | video]
```

### Tier 3: RAG Optimization Properties

Properties specifically for improving search:

```yaml
searchable-tags:              # NEW - Synthetic tags for semantic search
  - natural-language-term
  - synonym
  - category-descriptor
```

---

## 🎨 Vault-Specific Extensions

### ThistleRidgeHall Extension

**Required additions to existing schema:**
```yaml
category: artwork              # ADD THIS to all product files
content-type: visual           # ADD THIS
medium: oil-painting-style     # ADD THIS (or appropriate style)
searchable-tags:               # ADD THIS for RAG
  - visual-art
  - digital-product
  - landscape                  # or appropriate subject
  - cottage                    # or appropriate theme
```

**Keep existing Etsy metadata** (etsy-*, botanical-*, SKU, etc.)

---

### Business-Incubator Extension

**For source-image files:**
```yaml
content-type: visual           # ADD THIS
searchable-tags:               # ADD THIS
  - historical-image
  - vintage-photo
  - source-material
  - [subject keywords from 'subject' field]
```

**For project files:**
```yaml
category: business-project     # ADD THIS
content-type: textual          # ADD THIS
```

---

### Study Extension

**Keep existing structure, add:**
```yaml
category: educational-material # ADD THIS
content-type: textual          # ADD THIS (or mixed if has audio)
searchable-tags:               # ADD THIS
  - language-learning
  - chinese
  - hsk-[level]
```

---

### SickRabbit Extension

**Add to product concept files:**
```yaml
category: product-concept      # ADD THIS (in addition to existing 'category')
content-type: textual          # ADD THIS
searchable-tags:               # ADD THIS
  - artwork-concept
  - product-development
  - [theme keywords]
```

---

### Praxis Extension

**Add to content planning files:**
```yaml
category: content-planning     # ADD THIS
content-type: textual          # ADD THIS
searchable-tags:               # ADD THIS
  - content-calendar
  - video-production
  - [project name]
```

---

### Library, Creative-Incubator, Red-White Extensions

**Minimal additions (low priority):**
```yaml
category: [appropriate type]
content-type: textual
searchable-tags: [relevant keywords]
```

---

## 📚 Property Dictionary

### Complete Property Reference

| Property | Type | Usage | Vaults | Purpose |
|----------|------|-------|--------|---------|
| `type` | array | REQUIRED | All | Primary document classification |
| `category` | array | REQUIRED* | All | Secondary classification (NEW) |
| `tags` | array | RECOMMENDED | All | Obsidian tags |
| `searchable-tags` | array | NEW | All | RAG semantic keywords |
| `content-type` | string | NEW | All | Visual/textual/mixed |
| `medium` | string | OPTIONAL | TRH, BR, SR | Artwork medium/style |
| `status` | array | RECOMMENDED | Most | Document state |
| `created` | date | RECOMMENDED | All | Creation timestamp |
| `updated` | date | OPTIONAL | All | Last modification |
| `project` | array | OPTIONAL | Most | Project association |
| `title` | string | OPTIONAL | All | Explicit title |
| | | | | |
| **ThistleRidgeHall Specific** |
| `collection` | array | REQUIRED | TRH | Art collection name |
| `artist` | array | REQUIRED | TRH | Artist name |
| `SKU` | string | REQUIRED | TRH | Product SKU |
| `etsy-*` | various | REQUIRED | TRH | Etsy listing metadata |
| `botanical-*` | string | OPTIONAL | TRH | Botanical metadata |
| `archive-note-id` | string | REQUIRED | TRH | Archive reference |
| | | | | |
| **Study Specific** |
| `lesson-number` | string | REQUIRED | Study | Lesson identifier |
| `hsk-level` | number | REQUIRED | Study | HSK proficiency level |
| `completion-status` | string | REQUIRED | Study | Lesson progress |
| | | | | |
| **Business-Incubator Specific** |
| `id` | string | REQUIRED | BI (images) | Image ID |
| `source_url` | string | REQUIRED | BI (images) | Source URL |
| `copyright_status` | array | REQUIRED | BI (images) | License info |
| | | | | |
| **General** |
| `priority` | array | OPTIONAL | Projects | Task priority |
| `related-notes` | string | OPTIONAL | All | Document links |

\* REQUIRED for documents where classification matters for search (products, projects, etc.)

---

## 🔧 RAG Optimization Strategy

### Strategy 1: Synthetic Content Generation

**Problem:** "artworks" doesn't appear in YAML property names
**Solution:** Generate searchable synthetic content from YAML

**Implementation in `metadata_extractor.py`:**

```python
def generate_synthetic_content(metadata, content):
    """
    Create searchable text from YAML metadata to bridge semantic gaps
    """
    synthetic = []

    # Type-based descriptions
    if 'type' in metadata:
        types = metadata['type'] if isinstance(metadata['type'], list) else [metadata['type']]
        for t in types:
            if t == 'product':
                synthetic.append("This is a product artwork listing.")
            elif t == 'lesson-study':
                synthetic.append("This is a language learning lesson.")
            elif t == 'source-image':
                synthetic.append("This is a source image for creative work.")

    # Category descriptions
    if 'category' in metadata:
        categories = metadata['category'] if isinstance(metadata['category'], list) else [metadata['category']]
        for cat in categories:
            if cat == 'artwork':
                synthetic.append("This file represents an artwork.")
            elif cat == 'product-concept':
                synthetic.append("This is a product concept and idea.")

    # Collection/Project context
    if 'collection' in metadata:
        coll = metadata['collection'][0] if isinstance(metadata['collection'], list) else metadata['collection']
        synthetic.append(f"Part of the {coll} collection.")

    # Searchable tags
    if 'searchable-tags' in metadata:
        tags = metadata['searchable-tags']
        synthetic.append(f"Keywords: {', '.join(tags)}.")

    # Etsy subjects (ThistleRidgeHall)
    if 'etsy-subject' in metadata:
        subjects = metadata['etsy-subject']
        synthetic.append(f"Subjects: {', '.join(subjects)}.")

    # Artist
    if 'artist' in metadata:
        artist = metadata['artist'][0] if isinstance(metadata['artist'], list) else metadata['artist']
        synthetic.append(f"Created by {artist}.")

    # Combine with actual content
    synthetic_text = " ".join(synthetic)
    return f"{synthetic_text}\n\n{content}"
```

### Strategy 2: Query Router Enhancement

**Add category query type to `query_router.py`:**

```python
CATEGORY_QUERIES = {
    # Natural language → YAML filters
    'artworks': {'type': 'product', 'category': 'artwork'},
    'artwork': {'type': 'product', 'category': 'artwork'},
    'art': {'type': 'product', 'category': 'artwork'},
    'products': {'type': 'product'},
    'listings': {'status': 'listed'},
    'lessons': {'type': 'lesson-study'},
    'characters': {'type': 'character'},
    'source images': {'type': 'source-image'},
    'projects': {'type': 'project'},
    'concepts': {'note-type': 'idea'},
}

def detect_category_query(query_text):
    """Check if query is asking for a category"""
    query_lower = query_text.lower()
    for keyword, filters in CATEGORY_QUERIES.items():
        if keyword in query_lower:
            return 'category', filters
    return None, None
```

### Strategy 3: Metadata-Aware Search

**Enhance `hybrid_search.py`:**

```python
def search_with_category_filter(vault_name, query, filters, limit=50):
    """
    Search with metadata filters for category queries
    Uses metadata filtering instead of just vector similarity
    """
    collection = vector_store.get_collection(vault_name)

    # Build ChromaDB where clause
    where_clause = {}
    for key, value in filters.items():
        where_clause[key] = value

    # Query with filters
    results = collection.query(
        query_texts=[query],
        where=where_clause,
        n_results=limit
    )

    return results
```

---

## 🚀 Migration Plan

### Phase 1: Schema Documentation (COMPLETE ✅)
- [x] Investigate all vaults
- [x] Document current patterns
- [x] Design unified schema
- [x] Create this document

### Phase 2: Priority Vault Updates (Week 1)

**Target: ThistleRidgeHall** (Highest impact, 47 artwork files)

**Script: `add-artwork-metadata.py`**
```python
#!/usr/bin/env python3
"""
Add semantic metadata to ThistleRidgeHall artwork files
"""
import os
import re
from pathlib import Path

ARTWORKS_DIR = "C:/Users/redpo/repos/Obsidian/Multi-Vault/ThistleRidgeHall.vault/Artworks"

def add_semantic_metadata(filepath):
    """Add category, content-type, medium, searchable-tags to artwork file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse existing YAML
    yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not yaml_match:
        print(f"No YAML found in {filepath}")
        return False

    yaml_content = yaml_match.group(1)
    body = content[yaml_match.end():]

    # Check if already has category
    if 'category:' in yaml_content:
        print(f"Already updated: {filepath}")
        return False

    # Extract etsy-subject for searchable-tags
    subject_match = re.search(r'etsy-subject:\s*\n\s*-\s*"?([^"\n]+)"?', yaml_content)
    subjects = []
    if subject_match:
        # Parse multi-line array
        subjects_block = re.findall(r'-\s*"?([^"\n]+)"?', yaml_content[subject_match.start():])
        subjects = [s.strip().lower().replace(' & ', '-').replace(' ', '-') for s in subjects_block]

    # Determine medium from etsy-style or default
    medium = "oil-painting-style"  # Default
    if 'watercolor' in yaml_content.lower():
        medium = "watercolor-style"
    elif 'photograph' in yaml_content.lower():
        medium = "photography-style"

    # Build additions
    additions = f"""category:
  - artwork
content-type: visual
medium: {medium}
searchable-tags:
  - visual-art
  - digital-product"""

    if subjects:
        for subj in subjects[:3]:  # Add up to 3 subject tags
            additions += f"\n  - {subj}"

    # Insert after 'type' property
    type_match = re.search(r'(type:.*?)(\n[a-z])', yaml_content, re.DOTALL)
    if type_match:
        updated_yaml = yaml_content[:type_match.end(1)] + "\n" + additions + type_match.group(2) + yaml_content[type_match.end(2):]
    else:
        updated_yaml = yaml_content + "\n" + additions

    # Reconstruct file
    new_content = f"---\n{updated_yaml}\n---{body}"

    # Write backup
    backup = filepath + ".backup"
    os.rename(filepath, backup)

    # Write updated file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✓ Updated: {filepath}")
    return True

def main():
    artworks_path = Path(ARTWORKS_DIR)
    files_updated = 0

    for md_file in artworks_path.glob("*.md"):
        if add_semantic_metadata(md_file):
            files_updated += 1

    print(f"\n=== Migration Complete ===")
    print(f"Files updated: {files_updated}")
    print(f"Location: {ARTWORKS_DIR}")

if __name__ == "__main__":
    main()
```

**Steps:**
1. Create backup of Artworks folder
2. Run `add-artwork-metadata.py`
3. Manually review 2-3 files
4. Verify YAML validity
5. Re-index ThistleRidgeHall vault
6. Test "artworks" query → should return 47 files

---

### Phase 3: Secondary Vaults (Week 2)

**Target: Business-Incubator, SickRabbit, Study**

- Similar scripts for each vault type
- Add `category`, `content-type`, `searchable-tags`
- Preserve existing metadata
- Re-index each vault

---

### Phase 4: RAG Service Enhancement (Week 2-3)

**Updates to RAG service:**

1. **`metadata_extractor.py`**
   - Implement `generate_synthetic_content()`
   - Index new properties

2. **`query_router.py`**
   - Add `CATEGORY_QUERIES` dictionary
   - Implement `detect_category_query()`

3. **`hybrid_search.py`**
   - Add `search_with_category_filter()`
   - Integrate metadata filtering

4. **Re-index all vaults**
   - Full re-index with enhanced extraction
   - Verify document counts

---

### Phase 5: Testing & Validation (Week 3)

**Test Cases:**

| Query | Vault | Expected | Current | After Fix |
|-------|-------|----------|---------|-----------|
| "artworks" | ThistleRidgeHall | 47 | 20 | 47 ✓ |
| "listed artworks" | ThistleRidgeHall | ~45 | ? | ~45 ✓ |
| "cottage artworks" | ThistleRidgeHall | ~15 | ? | ~15 ✓ |
| "source images" | Business-Incubator | ~300 | ? | ~300 ✓ |
| "lessons" | Study | ~84 | ? | ~84 ✓ |
| "product concepts" | SickRabbit | ~20 | ? | ~20 ✓ |

---

## ✅ Validation Rules

### YAML Validation Script

```python
#!/usr/bin/env python3
"""
Validate YAML consistency across vaults
"""
import yaml
from pathlib import Path

REQUIRED_PROPS = {
    'all': ['type'],
    'ThistleRidgeHall': ['type', 'category', 'status', 'SKU', 'collection'],
    'Study': ['type', 'lesson-number', 'hsk-level'],
    'Business-Incubator': ['type'],
}

def validate_file(filepath, vault_name):
    """Check if file has required YAML properties"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract YAML
    yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not yaml_match:
        return False, "No YAML frontmatter"

    try:
        metadata = yaml.safe_load(yaml_match.group(1))
    except yaml.YAMLError as e:
        return False, f"Invalid YAML: {e}"

    # Check required properties
    required = REQUIRED_PROPS.get(vault_name, REQUIRED_PROPS['all'])
    missing = [prop for prop in required if prop not in metadata]

    if missing:
        return False, f"Missing properties: {', '.join(missing)}"

    return True, "Valid"

# Run validation on all vaults
```

---

## 📊 Success Metrics

**Phase Complete When:**

- ✅ All ThistleRidgeHall artwork files have `category: artwork`
- ✅ "artworks" query returns 47/47 files (100%)
- ✅ Synthetic content generation working
- ✅ Category query routing implemented
- ✅ No regression in existing search quality
- ✅ All vaults re-indexed successfully
- ✅ Validation script passes 100%

---

## 🎓 Key Principles

### 1. **Backward Compatibility**
- Never remove existing YAML properties
- Only add new properties
- Preserve vault-specific metadata

### 2. **Semantic Clarity**
- `type` = what it IS (product, lesson, project)
- `category` = how to CLASSIFY it (artwork, source-image, concept)
- `searchable-tags` = how users SEARCH for it

### 3. **Minimal Disruption**
- Start with highest-impact vault (ThistleRidgeHall)
- Test thoroughly before expanding
- Keep backups of all files

### 4. **RAG Optimization**
- Synthetic content bridges semantic gaps
- Metadata filters for category queries
- Vector search for content similarity
- Hybrid approach for best results

---

## 📈 Next Steps

**Immediate (Today):**
1. ✅ Complete this schema document
2. ⏳ Review and approve schema
3. ⏳ Create migration script for ThistleRidgeHall

**Short-term (This Week):**
1. ⏳ Run migration on ThistleRidgeHall
2. ⏳ Update RAG metadata_extractor.py
3. ⏳ Re-index ThistleRidgeHall
4. ⏳ Test "artworks" query

**Medium-term (Next Week):**
1. ⏳ Migrate other priority vaults
2. ⏳ Implement query router enhancements
3. ⏳ Full system re-index
4. ⏳ Comprehensive testing

**Long-term (Month 1):**
1. ⏳ Migrate all 9 vaults
2. ⏳ Create YAML validation automation
3. ⏳ Document best practices
4. ⏳ User acceptance testing

---

## 📚 Reference Documents

- [YAML_STRATEGY.md](YAML_STRATEGY.md) - Original ThistleRidgeHall analysis
- [PRD.md](PRD.md) - Product requirements
- [RESEARCH.md](RESEARCH.md) - RAG implementation research
- [PHASE_3B_COMPLETE.md](docs/PHASE_3B_COMPLETE.md) - RAG system documentation

---

**Status:** 🟡 **Design Complete - Ready for Implementation**
**Priority:** 🔴 **High** (Core search accuracy improvement)
**Complexity:** 🟡 **Medium-High** (Well-defined, requires careful execution)
**Impact:** 🟢 **Very High** (Fixes fundamental RAG accuracy issue)

---

**Version History:**
- v1.0 (2025-10-21) - Initial comprehensive schema design
