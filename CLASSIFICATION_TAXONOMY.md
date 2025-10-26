# Multi-Vault Classification Taxonomy

**Created:** 2025-10-21
**Version:** 1.0
**Purpose:** Hierarchical classification system from broad → specific for RAG optimization

---

## 🎯 Design Philosophy

### The Problem
Current YAML is inconsistent:
- Some notes use `type: product`
- Others use `type: lesson-study`
- No clear hierarchy: is "product" a type? A category? Both?
- Hard for RAG to understand relationships

### The Solution: Three-Level Hierarchy

```
Level 1: TYPE (Broad)          → What fundamental category?
Level 2: CATEGORY (Medium)     → What specific domain?
Level 3: SUBCATEGORY (Narrow)  → What exact variant?
```

**Example:**
```yaml
type: content              # Level 1: Broad classification
category: product          # Level 2: It's a sellable product
subcategory: artwork       # Level 3: Specifically, it's art
```

**Benefits:**
- ✅ Clear hierarchy for RAG understanding
- ✅ Consistent across all vaults
- ✅ Easy to query at any level
- ✅ Supports progressive refinement
- ✅ Future-proof (add new subcategories without breaking structure)

---

## 📊 The Complete Taxonomy

### Level 1: TYPE (Foundation)

**7 fundamental types across all knowledge:**

```yaml
type:
  - content        # Created material (products, writings, art)
  - knowledge      # Learning and reference material
  - project        # Work in progress, planning
  - tracking       # Progress, status, dashboards
  - personal       # Life, admin, daily operations
  - creative       # Ideas, concepts, brainstorming
  - reference      # External sources, citations
```

#### TYPE Definitions:

| Type | Description | Use When |
|------|-------------|----------|
| **content** | Finished or publishable material | Products, artworks, completed writings, videos |
| **knowledge** | Educational or reference material | Lessons, tutorials, how-tos, research |
| **project** | Active work and planning | Project plans, WIP, roadmaps |
| **tracking** | Status and progress monitoring | Dashboards, schedules, progress reports |
| **personal** | Life administration | Bills, admin, daily notes |
| **creative** | Ideation and exploration | Brainstorms, concepts, rough ideas |
| **reference** | External information | Source material, citations, links |

---

### Level 2: CATEGORY (Domain)

**Categories organized by TYPE:**

#### TYPE: content
```yaml
category:
  - product              # Sellable items
  - writing              # Written works
  - video                # Video content
  - audio                # Podcasts, music
  - visual-art           # Images, graphics
  - documentation        # Technical docs
```

#### TYPE: knowledge
```yaml
category:
  - lesson               # Structured learning
  - tutorial             # How-to guides
  - research             # Deep-dive studies
  - note                 # Quick captures
  - archive              # Historical records
```

#### TYPE: project
```yaml
category:
  - business             # Business projects
  - creative-project     # Creative endeavors
  - learning-project     # Educational projects
  - development          # Software/product dev
```

#### TYPE: tracking
```yaml
category:
  - dashboard            # Overview displays
  - schedule             # Time-based planning
  - progress             # Status tracking
  - analytics            # Data analysis
```

#### TYPE: personal
```yaml
category:
  - administration       # Life admin
  - daily-note           # Daily captures
  - journal              # Personal reflection
```

#### TYPE: creative
```yaml
category:
  - idea                 # Raw ideas
  - concept              # Developed concepts
  - brainstorm           # Brainstorming sessions
  - inspiration          # Inspiration collection
```

#### TYPE: reference
```yaml
category:
  - source-material      # Raw sources
  - citation             # Referenced works
  - external-link        # Web resources
```

---

### Level 3: SUBCATEGORY (Specific)

**Subcategories organized by CATEGORY:**

#### CATEGORY: product
```yaml
subcategory:
  - digital-print        # Digital art prints
  - physical-product     # Physical items
  - digital-download     # Downloadable files
  - service              # Service offerings
  - course               # Educational courses
```

#### CATEGORY: visual-art
```yaml
subcategory:
  - photograph           # Photography
  - painting             # Paintings
  - illustration         # Illustrations
  - digital-art          # Digital artwork
  - mixed-media          # Mixed media
```

#### CATEGORY: lesson
```yaml
subcategory:
  - language-learning    # Language lessons
  - technical-skill      # Technical tutorials
  - creative-skill       # Creative learning
  - academic             # Academic study
```

#### CATEGORY: business
```yaml
subcategory:
  - ecommerce            # Online selling
  - content-creation     # Content business
  - consulting           # Consulting work
  - saas                 # Software as service
```

#### CATEGORY: source-material
```yaml
subcategory:
  - image                # Source images
  - text                 # Source text
  - data                 # Source data
  - inspiration          # Inspirational sources
```

#### CATEGORY: idea
```yaml
subcategory:
  - product-idea         # Product concepts
  - content-idea         # Content concepts
  - business-idea        # Business concepts
  - creative-idea        # Creative concepts
```

---

## 🗂️ Vault Mapping to Taxonomy

### ThistleRidgeHall (Etsy Art Business)

**Current structure:**
```yaml
type: [product]
```

**NEW hierarchical structure:**
```yaml
type: content
category: product
subcategory: digital-print
domain: visual-art          # NEW - cross-cutting domain
medium: oil-painting-style  # Existing - kept
```

**All 47 artwork files would have:**
- Same `type: content` (searchable as "content")
- Same `category: product` (searchable as "products")
- Same `subcategory: digital-print` (searchable as "digital prints")
- Different `domain` values based on subject (landscape, botanical, architecture)

---

### Business-Incubator (Projects & Sources)

**Source Images:**
```yaml
type: reference
category: source-material
subcategory: image
domain: historical-photography  # or vintage-art, etc.
```

**Project Files:**
```yaml
type: project
category: business
subcategory: ecommerce
domain: print-on-demand
```

---

### Study (Language Learning)

**Lessons:**
```yaml
type: knowledge
category: lesson
subcategory: language-learning
domain: chinese
specialization: hsk-3       # Existing - kept
```

**Flashcards:**
```yaml
type: knowledge
category: lesson
subcategory: language-learning
domain: chinese
format: flashcard           # NEW
```

---

### Creative-Incubator (Creative Projects)

**Dashboards:**
```yaml
type: tracking
category: dashboard
subcategory: progress-tracker
domain: creative-work
```

**Project Notes:**
```yaml
type: project
category: creative-project
subcategory: writing         # or music, art
domain: fiction              # or composition, illustration
```

---

### SickRabbit (Product Development)

**Concept Pitches:**
```yaml
type: creative
category: concept
subcategory: product-idea
domain: visual-art
stage: concept-development   # Existing - kept
```

**Artwork Series:**
```yaml
type: content
category: product
subcategory: digital-art
domain: occult-theme         # or specific series
series: digital-occult       # Existing - kept
```

---

### Praxis (Content Planning)

**Content Schedules:**
```yaml
type: tracking
category: schedule
subcategory: content-calendar
domain: video-content
platform: tiktok             # NEW
```

**Launch Plans:**
```yaml
type: project
category: creative-project
subcategory: content-creation
domain: video-production
```

---

### Red-White (Fiction Writing)

**Character Sheets:**
```yaml
type: creative
category: writing
subcategory: character-development
domain: fiction
genre: historical-fiction    # NEW
```

**Story Elements:**
```yaml
type: creative
category: writing
subcategory: worldbuilding
domain: fiction
genre: historical-fiction
```

---

### Library (Idea Collection)

**Fleeting Notes:**
```yaml
type: knowledge
category: note
subcategory: fleeting
domain: general              # or specific topic
capture-method: voice-note   # NEW
```

**Brain Dumps:**
```yaml
type: creative
category: idea
subcategory: raw-capture
domain: varies
```

---

### Life-Systems (Personal Admin)

**Admin Notes:**
```yaml
type: personal
category: administration
subcategory: household
domain: utilities            # or finance, maintenance
```

**Daily Notes:**
```yaml
type: personal
category: daily-note
subcategory: daily-log
date: 2025-10-21
```

---

## 🎯 Complete Property Hierarchy

### Standard Structure (All Documents)

```yaml
# === CLASSIFICATION HIERARCHY (Broad → Specific) ===
type: content                    # REQUIRED - Level 1: Fundamental type
category: product                # REQUIRED - Level 2: Domain
subcategory: digital-print       # RECOMMENDED - Level 3: Specific variant

# === CROSS-CUTTING DIMENSIONS ===
domain: visual-art               # OPTIONAL - Subject domain
medium: oil-painting-style       # OPTIONAL - Creation method
format: digital                  # OPTIONAL - Output format

# === STATUS & LIFECYCLE ===
status: listed                   # RECOMMENDED - Current state
stage: published                 # OPTIONAL - Workflow stage
priority: high                   # OPTIONAL - Importance

# === TEMPORAL ===
created: 2025-10-21             # RECOMMENDED - Creation date
updated: 2025-10-21             # OPTIONAL - Last update
published: 2025-10-21           # OPTIONAL - Publication date

# === RELATIONSHIPS ===
project: [project-name]         # OPTIONAL - Associated project
series: [series-name]           # OPTIONAL - Series membership
collection: [collection-name]   # OPTIONAL - Collection membership
related-notes: "[[Link]]"       # OPTIONAL - Related documents

# === SEARCHABILITY (RAG Optimization) ===
tags: [tag1, tag2]              # RECOMMENDED - Obsidian tags
searchable-keywords:            # NEW - Natural language keywords
  - artwork
  - landscape
  - cottage
  - moody-atmosphere

# === CONTENT METADATA ===
content-type: visual            # RECOMMENDED - Visual/textual/mixed
title: "Explicit Title"         # OPTIONAL - If different from filename
```

---

## 🔍 RAG Query Examples

### How the Hierarchy Enables Better Search

#### Example 1: "Show me all artworks"
```yaml
# RAG understands multiple levels:
type: content → category: product → subcategory: digital-print + domain: visual-art

# Returns: All files matching this path
# ThistleRidgeHall: 47 artworks ✓
# SickRabbit: Product concepts (filtered out - wrong subcategory)
```

#### Example 2: "List all products"
```yaml
# Matches at category level:
category: product

# Returns: All products regardless of subcategory
# ThistleRidgeHall: 47 digital prints
# SickRabbit: Some product listings
# Business-Incubator: None (has source-material, not products)
```

#### Example 3: "Find language lessons"
```yaml
# Matches path:
type: knowledge → category: lesson → subcategory: language-learning

# Returns: Only language lessons
# Study: 84 Chinese lessons ✓
# Other vaults: 0 (no language lessons)
```

#### Example 4: "Show creative concepts"
```yaml
# Matches type + category:
type: creative → category: concept

# Returns: All concept documents
# SickRabbit: Product concepts
# Creative-Incubator: Project concepts
# Library: Raw ideas (category: idea, not concept)
```

---

## 🛠️ Implementation Strategy

### Phase 1: Define Taxonomy (COMPLETE ✅)
- [x] Create hierarchical classification
- [x] Define all types, categories, subcategories
- [x] Map existing vaults
- [x] This document

### Phase 2: Migration Script Enhancement

**Updated migration script with hierarchy:**

```python
#!/usr/bin/env python3
"""
Apply hierarchical classification to all vaults
"""
import os
import re
from pathlib import Path

# Vault → Classification mapping
VAULT_CLASSIFICATIONS = {
    'ThistleRidgeHall.vault/Artworks': {
        'type': 'content',
        'category': 'product',
        'subcategory': 'digital-print',
        'domain': 'visual-art',
        'content-type': 'visual',
    },
    'Business-Incubator.vault/Active Projects/Revival Prints/01_Sourcing/Images': {
        'type': 'reference',
        'category': 'source-material',
        'subcategory': 'image',
        'content-type': 'visual',
    },
    'Study.vault/Language/Chinese/Active-Lessons': {
        'type': 'knowledge',
        'category': 'lesson',
        'subcategory': 'language-learning',
        'domain': 'chinese',
        'content-type': 'mixed',
    },
    # ... etc for all vaults
}

def apply_classification(filepath, vault_path):
    """Apply hierarchical classification based on vault location"""

    # Determine which classification to apply
    classification = None
    for path_pattern, props in VAULT_CLASSIFICATIONS.items():
        if path_pattern in str(filepath):
            classification = props
            break

    if not classification:
        print(f"⚠ No classification defined for: {filepath}")
        return False

    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse YAML
    yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not yaml_match:
        # No YAML - create it
        yaml_content = ""
        body = content
    else:
        yaml_content = yaml_match.group(1)
        body = content[yaml_match.end():]

    # Check if already classified
    if 'type:' in yaml_content and 'category:' in yaml_content:
        print(f"✓ Already classified: {filepath}")
        return False

    # Build classification block
    new_props = f"""type: {classification['type']}
category: {classification['category']}
subcategory: {classification['subcategory']}"""

    if 'domain' in classification:
        new_props += f"\ndomain: {classification['domain']}"

    if 'content-type' in classification:
        new_props += f"\ncontent-type: {classification['content-type']}"

    # Generate searchable keywords from classification
    keywords = [
        classification['type'],
        classification['category'],
        classification['subcategory'],
    ]
    if 'domain' in classification:
        keywords.append(classification['domain'])

    new_props += f"\nsearchable-keywords:\n"
    for kw in keywords:
        new_props += f"  - {kw}\n"

    # Merge with existing YAML or create new
    if yaml_content:
        # Insert at top of existing YAML
        updated_yaml = new_props + "\n" + yaml_content
    else:
        updated_yaml = new_props

    # Reconstruct file
    new_content = f"---\n{updated_yaml}\n---{body}"

    # Backup
    backup = str(filepath) + ".backup"
    os.rename(filepath, backup)

    # Write
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✓ Classified: {filepath}")
    return True

def main():
    vault_root = Path("C:/Users/redpo/repos/Obsidian/Multi-Vault")

    for vault_pattern in VAULT_CLASSIFICATIONS.keys():
        vault_path = vault_root / vault_pattern
        if not vault_path.exists():
            continue

        print(f"\n=== Processing: {vault_pattern} ===")
        count = 0

        for md_file in vault_path.glob("*.md"):
            if apply_classification(md_file, vault_pattern):
                count += 1

        print(f"Files classified: {count}")

if __name__ == "__main__":
    main()
```

---

### Phase 3: RAG Service Update

**Query Router with Hierarchical Understanding:**

```python
def parse_hierarchical_query(query_text):
    """
    Understand queries at different hierarchy levels
    """
    query_lower = query_text.lower()

    # Level 1: TYPE queries
    TYPE_QUERIES = {
        'content': ['content', 'created content', 'finished work'],
        'knowledge': ['knowledge', 'learning', 'educational'],
        'project': ['projects', 'work in progress', 'planning'],
        'creative': ['ideas', 'concepts', 'brainstorms'],
        'personal': ['personal', 'admin', 'daily'],
    }

    # Level 2: CATEGORY queries
    CATEGORY_QUERIES = {
        'product': ['products', 'items', 'listings'],
        'lesson': ['lessons', 'courses', 'tutorials'],
        'artwork': ['artworks', 'art', 'pieces'],  # SUBCATEGORY actually
        'source-material': ['sources', 'references', 'source images'],
    }

    # Level 3: SUBCATEGORY queries
    SUBCATEGORY_QUERIES = {
        'digital-print': ['digital prints', 'printables', 'downloads'],
        'language-learning': ['language lessons', 'language learning'],
        'product-idea': ['product concepts', 'product ideas'],
    }

    # Match query to hierarchy level
    filters = {}

    for type_key, keywords in TYPE_QUERIES.items():
        if any(kw in query_lower for kw in keywords):
            filters['type'] = type_key

    for cat_key, keywords in CATEGORY_QUERIES.items():
        if any(kw in query_lower for kw in keywords):
            # Some keywords are actually subcategories
            if cat_key == 'artwork':
                filters['subcategory'] = 'digital-print'  # or visual-art domain
            else:
                filters['category'] = cat_key

    for subcat_key, keywords in SUBCATEGORY_QUERIES.items():
        if any(kw in query_lower for kw in keywords):
            filters['subcategory'] = subcat_key

    return filters

# Example usage:
query = "show me all artworks"
filters = parse_hierarchical_query(query)
# Returns: {'subcategory': 'digital-print'} or {'domain': 'visual-art'}

query = "list products"
filters = parse_hierarchical_query(query)
# Returns: {'category': 'product'}

query = "find creative ideas"
filters = parse_hierarchical_query(query)
# Returns: {'type': 'creative'}
```

---

## 📋 Quick Reference Guide

### Choosing Classification for New Notes

**Ask yourself 3 questions:**

1. **What fundamental type is this?**
   - Created material? → `type: content`
   - Learning material? → `type: knowledge`
   - Work in progress? → `type: project`
   - Tracking/monitoring? → `type: tracking`
   - Personal life? → `type: personal`
   - Brainstorming? → `type: creative`
   - External source? → `type: reference`

2. **What specific domain?**
   - Choose appropriate `category` from type's list

3. **Need more specificity?**
   - Add `subcategory` if available
   - Add `domain` for cross-cutting topic

**Example Decision Tree:**

```
"I'm creating a digital art print to sell on Etsy"
├─ Fundamental type? → Created material → type: content
├─ Domain? → It's a product I'm selling → category: product
├─ Specific variant? → It's a digital download → subcategory: digital-print
└─ Subject? → It's visual art → domain: visual-art

Result:
type: content
category: product
subcategory: digital-print
domain: visual-art
```

---

## ✅ Validation Rules

### Consistency Checks

```python
REQUIRED_BY_TYPE = {
    'content': ['category', 'subcategory'],
    'knowledge': ['category'],
    'project': ['category', 'status'],
    'tracking': ['category'],
    'personal': ['category'],
    'creative': ['category'],
    'reference': ['category'],
}

VALID_CATEGORIES_BY_TYPE = {
    'content': ['product', 'writing', 'video', 'audio', 'visual-art', 'documentation'],
    'knowledge': ['lesson', 'tutorial', 'research', 'note', 'archive'],
    'project': ['business', 'creative-project', 'learning-project', 'development'],
    # ... etc
}

def validate_classification(metadata):
    """Validate hierarchical consistency"""

    # Check type exists
    if 'type' not in metadata:
        return False, "Missing required 'type' property"

    doc_type = metadata['type']

    # Check required properties for this type
    required = REQUIRED_BY_TYPE.get(doc_type, [])
    for prop in required:
        if prop not in metadata:
            return False, f"Type '{doc_type}' requires '{prop}' property"

    # Check category is valid for type
    if 'category' in metadata:
        valid_cats = VALID_CATEGORIES_BY_TYPE.get(doc_type, [])
        if metadata['category'] not in valid_cats:
            return False, f"Category '{metadata['category']}' invalid for type '{doc_type}'"

    return True, "Valid classification"
```

---

## 🎯 Success Metrics

**System is successful when:**

- ✅ Every document has `type` + `category`
- ✅ All classifications follow hierarchy rules
- ✅ Query "artworks" returns 47/47 files
- ✅ Query "products" returns all products across vaults
- ✅ Query "lessons" returns only lessons
- ✅ RAG can search at any hierarchy level
- ✅ No ambiguous classifications
- ✅ Easy to classify new notes

---

## 📚 Benefits Summary

### For Users:
- 🎯 **Clearer organization** - Know exactly what type of note to create
- 🔍 **Better search** - Find content at broad or specific levels
- 📊 **Consistent structure** - Same system across all vaults

### For RAG:
- 🧠 **Semantic understanding** - Knows "artwork" is a type of "product" which is "content"
- 🎯 **Accurate filtering** - Can match at any hierarchy level
- 🔗 **Relationship mapping** - Understands note relationships
- 📈 **Better relevance** - Ranks results by hierarchy match

### For System:
- 🏗️ **Scalable** - Easy to add new subcategories
- 🔧 **Maintainable** - Clear rules for classification
- ✅ **Validatable** - Can check consistency automatically
- 🚀 **Future-proof** - Hierarchy supports growth

---

**Status:** 🟢 **Design Complete - Ready for Review**
**Next Step:** Review taxonomy, then update migration scripts
**Impact:** 🔴 **Critical** - Foundation for all RAG improvements

---

**Version History:**
- v1.0 (2025-10-21) - Initial hierarchical taxonomy design
