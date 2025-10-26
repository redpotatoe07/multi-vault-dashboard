# YAML Strategy & Metadata Schema

**Created:** 2025-10-21
**Purpose:** Define unified YAML conventions for RAG optimization across Multi-Vault System

---

## 🔍 Problem Statement

**Current Issue:**
- Query: "artworks" in ThistleRidgeHall → RAG returns 20 results
- **Actual count:** 47 artwork files exist
- **Root cause:** Semantic gap - files tagged as `type: product`, not "artwork"

**Why This Matters:**
RAG vector search looks for **content similarity**, but structured metadata queries require **property-based filtering**. The term "artwork" doesn't appear in file content—it's a **category** expressed through YAML properties.

---

## 📊 Current YAML Patterns (ThistleRidgeHall Artworks)

### Standard Properties Found:
```yaml
type:
  - product                    # All artworks = product
status:
  - listed                     # or: draft, unlisted, archived
collection:
  - "At Borderlands Forgotten" # Collection name
  - "On Morning Mist and Meadow"
artist:
  - "Thomas Whitmore"
  - "Cerys ferch Rhys"
cover: "[[filename.jpg]]"
archive-note-id: ART.V.3306.089
project:
  - bp-002
SKU: TRH-Borderlands-004

# Etsy-specific metadata
etsy-type: "Digital item"
etsy-category: "Art & Collectibles > Prints > Digital Prints"
etsy-primary-color: Blue
etsy-secondary-color: Brown
etsy-home-style:
  - "Rustic & primitive"
  - Cottage
etsy-subject:
  - "Landscape & scenery"
  - "Architecture & cityscape"
etsy-occasion: Housewarming
etsy-room: "Living Room, Office, Bedroom"
etsy-orientation: Horizontal

# Botanical metadata
botanical-common-names: "apple trees"
botanical-latin-names: "Malus domestica"

# Scheduling
etsy-schedule:
pinterest-schedule:
pinterest-uploaded: false
```

---

## 🎯 Proposed YAML Schema

### Core Categories

#### 1. **Document Classification**
```yaml
type:              # REQUIRED - Primary document type
  - product        # Etsy listings (artworks)
  - note           # General notes
  - reference      # Reference material
  - project        # Project documentation
  - archive        # Archived content

category:          # NEW - Secondary classification
  - artwork        # Add this to all products that are art
  - writing        # Stories, articles
  - research       # Research notes
  - business       # Business planning
```

**Recommendation:** Add `category: artwork` to all product files in Artworks folder.

#### 2. **Semantic Tags for RAG**
```yaml
tags:              # NEW - Semantic keywords for search
  - visual-art
  - landscape
  - digital-product
  - cottage-theme
  - british-countryside
```

**Purpose:** Bridge gap between formal metadata and natural language queries.

#### 3. **Content Type Identifiers**
```yaml
content-type:      # NEW - What is this fundamentally?
  - visual         # Images, artworks
  - textual        # Writing, documentation
  - mixed          # Both

medium:            # For artworks specifically
  - digital-print
  - oil-painting-style
  - watercolor-style
  - photography-style
```

---

## 🔧 RAG Optimization Strategies

### Strategy 1: **Metadata Extraction Enhancement**

**File:** `rag-service/metadata_extractor.py`

**Current:** Extracts basic YAML properties
**Proposed:** Add semantic indexing of YAML values

```python
def extract_semantic_tags(metadata):
    """Convert YAML properties to searchable tags"""
    tags = []

    # Type-based tagging
    if 'type' in metadata:
        if 'product' in metadata['type']:
            tags.extend(['product', 'artwork', 'for-sale', 'digital-download'])

    # Collection-based tagging
    if 'collection' in metadata:
        collection = metadata['collection'][0] if isinstance(metadata['collection'], list) else metadata['collection']
        # "At Borderlands Forgotten" → ["borderlands", "forgotten", "landscape"]
        tags.extend(collection.lower().split())

    # Subject-based tagging
    if 'etsy-subject' in metadata:
        for subject in metadata['etsy-subject']:
            tags.extend(subject.lower().split(' & '))

    return tags
```

### Strategy 2: **Query Router Enhancement**

**File:** `rag-service/query_router.py`

**Add new query type:**
```python
CATEGORY_QUERIES = {
    'artworks': {'type': 'product', 'category': 'artwork'},
    'products': {'type': 'product'},
    'listed items': {'type': 'product', 'status': 'listed'},
    'drafts': {'status': 'draft'},
    'botanical': {'botanical-common-names': {'$exists': True}},
}
```

### Strategy 3: **Hybrid Search Enhancement**

**File:** `rag-service/hybrid_search.py`

**Improve metadata filtering:**
```python
def search_by_category(vault_name, category, limit=50):
    """Search by semantic category, not just exact YAML match"""

    # Map natural language to YAML properties
    category_map = {
        'artwork': {'type': 'product'},
        'artworks': {'type': 'product'},
        'products': {'type': 'product'},
        'paintings': {'type': 'product', 'medium': 'oil-painting-style'},
        'cottage art': {'type': 'product', 'etsy-home-style': {'$contains': 'Cottage'}},
    }

    filters = category_map.get(category.lower(), {})
    return collection.query(where=filters, n_results=limit)
```

---

## 📝 Proposed YAML Conventions

### For ThistleRidgeHall Artworks:

**Add these properties to ALL artwork files:**
```yaml
type:
  - product
category:              # NEW
  - artwork
tags:                  # NEW - for RAG semantic search
  - visual-art
  - digital-product
  - {{ primary-subject }}  # e.g., "cottage", "landscape", "botanical"
content-type: visual   # NEW
medium: {{ style }}    # e.g., "oil-painting-style", "watercolor-style"
```

### Example Updated File:
```yaml
---
type:
  - product
category:              # NEW
  - artwork
tags:                  # NEW
  - visual-art
  - digital-product
  - landscape
  - cottage
  - marshland
content-type: visual
medium: oil-painting-style
status:
  - listed
collection:
  - At Borderlands Forgotten
artist:
  - Thomas Whitmore
# ... rest of existing metadata
---
```

---

## 🚀 Implementation Plan

### Phase 1: Schema Definition (DONE ✅)
- [x] Document current patterns
- [x] Design enhanced schema
- [x] Propose new properties

### Phase 2: Metadata Normalization (Next)
1. **Script to add semantic properties:**
   - Add `category: artwork` to all `/Artworks/*.md` files
   - Add `tags:` array with semantic keywords
   - Add `content-type:` and `medium:` where applicable

2. **Validate YAML:**
   - Ensure no syntax errors
   - Check for property consistency

### Phase 3: RAG Service Enhancement
1. **Update `metadata_extractor.py`:**
   - Extract new semantic properties
   - Index tags for vector search
   - Create synthetic content from YAML for better matching

2. **Update `query_router.py`:**
   - Add category query detection
   - Map natural language to YAML filters

3. **Update `hybrid_search.py`:**
   - Implement category-aware search
   - Add synonym mapping (artwork = product with category: artwork)

### Phase 4: Re-indexing
1. Re-index all vaults with enhanced metadata extraction
2. Verify "artworks" query returns all 47 files
3. Test other category queries

---

## 🧪 Test Cases

### Expected Results After Implementation:

| Query | Vault | Expected | Current | Status |
|-------|-------|----------|---------|--------|
| "artworks" | ThistleRidgeHall | 47 | 20 | ❌ FAIL |
| "products" | ThistleRidgeHall | 47 | ? | ⏳ TBD |
| "listed items" | ThistleRidgeHall | ~45 | ? | ⏳ TBD |
| "cottage artworks" | ThistleRidgeHall | ~15 | ? | ⏳ TBD |
| "botanical art" | ThistleRidgeHall | ~8 | ? | ⏳ TBD |

---

## 🎓 Key Insights

### 1. **Metadata is Data**
YAML properties are not just organization—they're **queryable data** that RAG must understand semantically.

### 2. **Natural Language ≠ Property Names**
Users say "artworks", metadata says `type: product`. We need **semantic mapping**.

### 3. **Hybrid Approach**
- **Vector search:** For "cottage in mist" (content similarity)
- **Metadata filters:** For "list all artworks" (property matching)
- **Combined:** For "show me listed cottage artworks" (both)

### 4. **Synthetic Content**
To improve vector matching, we can create **synthetic searchable text** from YAML:
```
"This is a product artwork in the At Borderlands Forgotten collection by Thomas Whitmore, featuring landscape scenery with cottage architecture in blue and brown colors."
```

This gets indexed alongside actual content, making "artworks" match `type: product` files.

---

## 📚 Next Steps

**Immediate Action Items:**

1. ✅ **Document YAML patterns** (this file)
2. ⏳ **Create YAML normalization script**
   - Scan all ThistleRidgeHall artwork files
   - Add missing semantic properties
   - Preserve existing metadata
3. ⏳ **Enhance metadata extractor**
   - Add synthetic content generation
   - Improve property indexing
4. ⏳ **Update query router**
   - Add category detection
   - Implement synonym mapping
5. ⏳ **Re-index and test**
   - Verify all 47 artworks found
   - Test edge cases

---

## 🎯 Success Criteria

**Phase Complete When:**
- ✅ "artworks" query returns all 47 files
- ✅ "products" query returns correct count
- ✅ Category queries work (listed/draft/etc.)
- ✅ Natural language maps to YAML properties
- ✅ No loss of existing search quality

---

**Status:** 🟡 **In Progress**
**Priority:** 🔴 **High** (Core search accuracy)
**Complexity:** 🟢 **Medium** (Clear solution, moderate implementation)
