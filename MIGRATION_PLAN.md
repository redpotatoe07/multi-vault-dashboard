# Multi-Vault Classification Migration Plan

**Created:** 2025-10-21
**Version:** 1.0
**Scope:** Migrate 1,269 documents + all templates to new hierarchical classification

---

## 📊 Migration Scope

### Documents to Update

| Vault | Documents | Templates Found | Priority |
|-------|-----------|----------------|----------|
| **ThistleRidgeHall** | 279 | 1 (Daily Note) | 🔴 **HIGHEST** (Business Critical) |
| **Praxis** | 28 | TBD | 🔴 **HIGHEST** (Active Project) |
| **Library** | 183 | TBD | 🔴 **HIGHEST** (Heavy Usage) |
| **Business-Incubator** | 326 | 1 (Business Note) | 🟡 MEDIUM |
| **Study** | 84 | 3 (Chinese, Guitar, Piano) | 🟡 MEDIUM |
| **Creative-Incubator** | 125 | TBD | 🟡 MEDIUM |
| **SickRabbit** | 38 | TBD | 🟡 MEDIUM |
| **Red-White** | 114 | TBD | 🟢 LOW |
| **Life-Systems** | 92 | TBD | 🟢 LOW |
| **TOTAL** | **1,269** | **~10-15** | - |

### Template Locations Found

```
./ThistleRidgeHall.vault/Resources/Templates/
  - Daily Note Template.md

./Study.vault/Resources/Templates/
  - TEMPLATE - Chines Study.md
  - TEMPLATE - Guitar-Practice-Session.md
  - TEMPLATE - Piano-Practice-Session.md

./Business-Incubator.vault/Resources/Templates/
  - Business Note Template.md

./Creative-Incubator.vault/Resources/Templates/
  - [To be discovered]

./Library.vault/Resources/Templates/
  - [To be discovered]

... (etc for each vault)
```

---

## 🎯 Migration Strategy

### Phase 1: Preparation (Week 1, Days 1-2)

#### 1.1 Full Backup
```bash
# Create timestamped backup of entire Multi-Vault system
cd C:/Users/redpo/repos/Obsidian
cp -r Multi-Vault Multi-Vault-BACKUP-2025-10-21
```

**Verification:**
- ✅ Backup size matches original
- ✅ All 9 vaults present
- ✅ Random file check shows content intact

#### 1.2 Template Discovery
**Script: `discover-templates.py`**
```python
#!/usr/bin/env python3
"""
Find all template files across vaults
"""
from pathlib import Path
import json

VAULT_ROOT = Path("C:/Users/redpo/repos/Obsidian/Multi-Vault")

def find_templates(vault_path):
    """Find all template files in a vault"""
    templates = []

    # Common template locations
    template_dirs = [
        vault_path / "Resources" / "Templates",
        vault_path / ".obsidian" / "templates",
        vault_path / "Templates",
    ]

    for template_dir in template_dirs:
        if template_dir.exists():
            for md_file in template_dir.rglob("*.md"):
                templates.append({
                    'path': str(md_file),
                    'name': md_file.name,
                    'vault': vault_path.name
                })

    # Also search for files with "template" in name
    for md_file in vault_path.rglob("*[Tt]emplate*.md"):
        if not any(t['path'] == str(md_file) for t in templates):
            templates.append({
                'path': str(md_file),
                'name': md_file.name,
                'vault': vault_path.name,
                'note': 'Found by filename search'
            })

    return templates

def main():
    all_templates = []

    for vault_dir in VAULT_ROOT.glob("*.vault"):
        print(f"\n=== Scanning {vault_dir.name} ===")
        templates = find_templates(vault_dir)
        all_templates.extend(templates)
        print(f"Found {len(templates)} templates")

    # Save results
    with open('template-inventory.json', 'w') as f:
        json.dump(all_templates, f, indent=2)

    print(f"\n=== TOTAL: {len(all_templates)} templates found ===")
    print("Saved to: template-inventory.json")

if __name__ == "__main__":
    main()
```

**Output:** `template-inventory.json` with complete template list

#### 1.3 Document Inventory
**Script: `analyze-documents.py`**
```python
#!/usr/bin/env python3
"""
Analyze all documents to understand current YAML structure
"""
import re
from pathlib import Path
from collections import defaultdict
import json

VAULT_ROOT = Path("C:/Users/redpo/repos/Obsidian/Multi-Vault")

def analyze_yaml(filepath):
    """Extract YAML frontmatter and analyze"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None

    yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not yaml_match:
        return {'has_yaml': False}

    yaml_content = yaml_match.group(1)
    properties = re.findall(r'^([a-z_-]+):', yaml_content, re.MULTILINE)

    return {
        'has_yaml': True,
        'properties': properties,
        'has_type': 'type' in properties,
        'has_category': 'category' in properties,
    }

def main():
    stats = defaultdict(lambda: {
        'total': 0,
        'with_yaml': 0,
        'with_type': 0,
        'with_category': 0,
        'needs_migration': 0
    })

    for vault_dir in VAULT_ROOT.glob("*.vault"):
        vault_name = vault_dir.name.replace('.vault', '')
        print(f"\n=== Analyzing {vault_name} ===")

        for md_file in vault_dir.rglob("*.md"):
            # Skip hidden files
            if '/.obsidian/' in str(md_file) or '/.smart-env/' in str(md_file):
                continue

            stats[vault_name]['total'] += 1
            analysis = analyze_yaml(md_file)

            if analysis and analysis['has_yaml']:
                stats[vault_name]['with_yaml'] += 1

                if analysis['has_type']:
                    stats[vault_name]['with_type'] += 1

                if analysis['has_category']:
                    stats[vault_name]['with_category'] += 1

                # Needs migration if has type but not full hierarchy
                if analysis['has_type'] and not analysis['has_category']:
                    stats[vault_name]['needs_migration'] += 1

    # Print summary
    print("\n" + "="*60)
    print("MIGRATION SUMMARY")
    print("="*60)

    for vault, data in sorted(stats.items()):
        print(f"\n{vault}:")
        print(f"  Total files: {data['total']}")
        print(f"  With YAML: {data['with_yaml']}")
        print(f"  Has 'type': {data['with_type']}")
        print(f"  Has 'category': {data['with_category']}")
        print(f"  Needs migration: {data['needs_migration']}")

    # Save detailed stats
    with open('migration-stats.json', 'w') as f:
        json.dump(dict(stats), f, indent=2)

if __name__ == "__main__":
    main()
```

**Output:** Migration statistics by vault

---

### Phase 2: Highest-Priority Vaults (Week 1, Days 3-5)

**Priority Order (USER-SPECIFIED):**
1. **ThistleRidgeHall** (Business critical, 279 docs, artworks search issue)
2. **Praxis** (Active content project, 28 docs, high usage)
3. **Library** (Heavy usage, idea collection, 183 docs)

#### 2.1 ThistleRidgeHall Migration

**Step 1: Update Artwork Template**
```yaml
# File: ThistleRidgeHall.vault/Resources/Templates/Artwork-Template.md
---
# === CLASSIFICATION HIERARCHY ===
type: content
category: product
subcategory: digital-print
domain: visual-art
content-type: visual
medium: oil-painting-style  # or watercolor-style, photography-style

# === STATUS & LIFECYCLE ===
status:
  - draft
collection:
  - [Collection Name]
artist:
  - [Artist Name]

# === PRODUCT METADATA ===
SKU:
cover: "[[image.jpg]]"
archive-note-id:
project:
  - bp-002

# === ETSY METADATA ===
etsy-type: "Digital item"
etsy-category: "Art & Collectibles > Prints > Digital Prints"
etsy-primary-color:
etsy-secondary-color:
etsy-home-style:
  -
etsy-subject:
  -
etsy-occasion:
etsy-room:
etsy-orientation:

# === BOTANICAL (if applicable) ===
botanical-common-names:
botanical-latin-names:

# === SCHEDULING ===
etsy-schedule:
pinterest-schedule:
pinterest-uploaded: false

# === SEARCHABILITY ===
searchable-keywords:
  - visual-art
  - digital-product
  - [subject-keywords]
tags:
  -
---

# [Artwork Title]

## Artwork Information
... (rest of template)
```

**Step 2: Migrate Existing Artwork Files**

**Script: `migrate-thistleridgehall.py`**
```python
#!/usr/bin/env python3
"""
Migrate ThistleRidgeHall artwork files to new classification
"""
import re
import os
from pathlib import Path
from datetime import datetime

ARTWORKS_DIR = Path("C:/Users/redpo/repos/Obsidian/Multi-Vault/ThistleRidgeHall.vault/Artworks")
BACKUP_DIR = Path("C:/Users/redpo/repos/Obsidian/Multi-Vault-MIGRATION-BACKUPS/ThistleRidgeHall")

def backup_file(filepath):
    """Create backup before modification"""
    backup_path = BACKUP_DIR / filepath.name
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return backup_path

def determine_medium(yaml_content):
    """Determine medium from existing content"""
    content_lower = yaml_content.lower()

    if 'watercolor' in content_lower:
        return 'watercolor-style'
    elif 'photograph' in content_lower or 'photo' in content_lower:
        return 'photography-style'
    elif 'digital' in content_lower:
        return 'digital-art'
    else:
        return 'oil-painting-style'  # Default

def extract_searchable_keywords(yaml_content):
    """Extract keywords from etsy-subject and other fields"""
    keywords = ['visual-art', 'digital-product']

    # Extract etsy-subject
    subject_pattern = r'etsy-subject:\s*\n((?:\s*-\s*"[^"]+"\s*\n?)+)'
    subject_match = re.search(subject_pattern, yaml_content)

    if subject_match:
        subjects = re.findall(r'-\s*"([^"]+)"', subject_match.group(1))
        for subject in subjects[:3]:  # Take up to 3
            # Clean and convert to keyword
            keyword = subject.lower().replace(' & ', '-').replace(' ', '-')
            if keyword not in keywords:
                keywords.append(keyword)

    # Extract from collection name
    collection_pattern = r'collection:\s*\n\s*-\s*"?([^"\n]+)"?'
    collection_match = re.search(collection_pattern, yaml_content)

    if collection_match:
        collection = collection_match.group(1).lower()
        if 'borderland' in collection:
            keywords.append('borderlands')
        if 'meadow' in collection or 'mist' in collection:
            keywords.append('pastoral')

    return keywords

def migrate_file(filepath):
    """Add hierarchical classification to artwork file"""
    print(f"\nProcessing: {filepath.name}")

    # Backup first
    backup_path = backup_file(filepath)
    print(f"  Backed up to: {backup_path}")

    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse YAML
    yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not yaml_match:
        print(f"  ⚠ No YAML found - skipping")
        return False

    yaml_content = yaml_match.group(1)
    body = content[yaml_match.end():]

    # Check if already migrated
    if 'category:' in yaml_content and 'subcategory:' in yaml_content:
        print(f"  ✓ Already migrated - skipping")
        return False

    # Determine properties
    medium = determine_medium(yaml_content)
    keywords = extract_searchable_keywords(yaml_content)

    # Build new classification block
    classification = f"""type: content
category: product
subcategory: digital-print
domain: visual-art
content-type: visual
medium: {medium}"""

    # Check if we need to update existing 'type' or add new
    if re.search(r'^type:', yaml_content, re.MULTILINE):
        # Replace existing type line
        yaml_content = re.sub(
            r'^type:.*?(?=\n[a-z_-]+:|\n\n|\Z)',
            classification,
            yaml_content,
            count=1,
            flags=re.MULTILINE | re.DOTALL
        )
    else:
        # Add at beginning
        yaml_content = classification + "\n" + yaml_content

    # Add searchable-keywords if not present
    if 'searchable-keywords:' not in yaml_content:
        keywords_block = "searchable-keywords:\n"
        for kw in keywords:
            keywords_block += f"  - {kw}\n"

        # Add before tags or at end of YAML
        if re.search(r'^tags:', yaml_content, re.MULTILINE):
            yaml_content = re.sub(
                r'^tags:',
                keywords_block + 'tags:',
                yaml_content,
                count=1,
                flags=re.MULTILINE
            )
        else:
            yaml_content = yaml_content.rstrip() + "\n" + keywords_block

    # Reconstruct file
    new_content = f"---\n{yaml_content}\n---{body}"

    # Write updated file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✓ Migrated successfully")
    print(f"    Medium: {medium}")
    print(f"    Keywords: {', '.join(keywords)}")

    return True

def main():
    print("="*60)
    print("ThistleRidgeHall Artwork Migration")
    print("="*60)

    if not ARTWORKS_DIR.exists():
        print(f"ERROR: Artworks directory not found: {ARTWORKS_DIR}")
        return

    files_migrated = 0
    files_skipped = 0
    files_error = 0

    for md_file in sorted(ARTWORKS_DIR.glob("*.md")):
        try:
            if migrate_file(md_file):
                files_migrated += 1
            else:
                files_skipped += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            files_error += 1

    print("\n" + "="*60)
    print("MIGRATION COMPLETE")
    print("="*60)
    print(f"Files migrated: {files_migrated}")
    print(f"Files skipped: {files_skipped}")
    print(f"Files with errors: {files_error}")
    print(f"\nBackups saved to: {BACKUP_DIR}")

    # Create migration log
    log_path = BACKUP_DIR / f"migration-log-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    with open(log_path, 'w') as f:
        f.write(f"Migration completed: {datetime.now()}\n")
        f.write(f"Files migrated: {files_migrated}\n")
        f.write(f"Files skipped: {files_skipped}\n")
        f.write(f"Files with errors: {files_error}\n")

    print(f"Log saved to: {log_path}")

if __name__ == "__main__":
    main()
```

**Step 3: Validation**
```bash
# Run validation on migrated files
python validate-classification.py ThistleRidgeHall.vault/Artworks
```

**Step 4: Re-index in RAG**
```bash
curl -X POST http://localhost:5001/index \
  -H "Content-Type: application/json" \
  -d '{"vault_name": "ThistleRidgeHall", "batch_size": 50, "force_reindex": true}'
```

**Step 5: Test**
```bash
# Test the critical query
curl -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"q": "artworks", "vault": "ThistleRidgeHall"}'

# Should return 47 results!
```

---

#### 2.2 Praxis Vault Migration

**Classification for Praxis files:**

**Content Schedules:**
```yaml
type: tracking
category: schedule
subcategory: content-calendar
domain: video-production
content-type: textual
platform: tiktok
```

**Launch Plans:**
```yaml
type: project
category: creative-project
subcategory: content-creation
domain: video-production
content-type: textual
```

**Migration approach:** Similar to ThistleRidgeHall - automated script with content-based classification

---

#### 2.3 Library Vault Migration

**Classification for Library files:**

**Fleeting Notes / Brain Dumps:**
```yaml
type: knowledge
category: note
subcategory: fleeting
domain: general  # or specific topic if identifiable
content-type: textual
capture-method: quick-note
```

**Structured Ideas:**
```yaml
type: creative
category: idea
subcategory: raw-capture
domain: varies
content-type: textual
```

**Notes:** Library vault has UUID-based IDs already - preserve these while adding classification

---

#### 2.4 Study Vault Migration (MOVED TO PHASE 3)

**Step 1: Update Templates**

Update `TEMPLATE - Chines Study.md`:
```yaml
---
# === CLASSIFICATION HIERARCHY ===
type: knowledge
category: lesson
subcategory: language-learning
domain: chinese
content-type: mixed

# === LESSON METADATA ===
lesson-number: [NUMBER]
lesson-title: "[TITLE]"
lesson-url: "[URL]"
hsk-level: [LEVEL]
completion-status: in-progress
sections-completed: 0
total-sections: 4
date-started: [DATE]
date-completed:
active-lesson: false

# === SEARCHABILITY ===
searchable-keywords:
  - language-learning
  - chinese-study
  - hsk-[LEVEL]
  - lesson
tags:
  - chinese-study
  - lesson
  - hsk-[LEVEL]
---
```

**Step 2: Migrate lesson files** (similar script pattern)

---

---

### Phase 3: Medium-Priority Vaults (Week 2)

**These vaults follow after the 3 highest-priority vaults are complete:**

- **Business-Incubator** (326 docs - largest vault)
- **Study** (84 docs - well-structured)
- **Creative-Incubator** (125 docs)
- **SickRabbit** (38 docs)

**Business-Incubator has two document types:**

**Type 1: Source Images**
```yaml
type: reference
category: source-material
subcategory: image
content-type: visual
domain: historical-photography
```

**Type 2: Project Files**
```yaml
type: project
category: business
subcategory: ecommerce
domain: print-on-demand
content-type: textual
```

Same process for all: Templates → Documents → Validation → Re-index → Test

---

### Phase 4: Low-Priority Vaults (Week 2-3)

- **Red-White** (minimal YAML, low impact)
- **Life-Systems** (often no YAML, low impact)

---

### Phase 5: RAG Service Updates (Week 3)

#### 5.1 Update `metadata_extractor.py`

Add synthetic content generation:
```python
def generate_synthetic_content(metadata, content):
    """Create searchable text from hierarchical classification"""
    synthetic = []

    # Type description
    type_desc = {
        'content': "This is created content.",
        'knowledge': "This is educational knowledge material.",
        'project': "This is a project document.",
        'tracking': "This is a progress tracking document.",
        'creative': "This is a creative ideation document.",
        'reference': "This is reference material.",
        'personal': "This is personal administrative content."
    }

    if 'type' in metadata:
        doc_type = metadata['type']
        synthetic.append(type_desc.get(doc_type, f"This is a {doc_type} document."))

    # Category description
    if 'category' in metadata:
        category = metadata['category']
        synthetic.append(f"It is categorized as {category.replace('-', ' ')}.")

    # Subcategory
    if 'subcategory' in metadata:
        subcategory = metadata['subcategory']
        synthetic.append(f"Specifically, it is {subcategory.replace('-', ' ')}.")

    # Domain
    if 'domain' in metadata:
        domain = metadata['domain']
        synthetic.append(f"The domain is {domain.replace('-', ' ')}.")

    # Searchable keywords
    if 'searchable-keywords' in metadata:
        keywords = metadata['searchable-keywords']
        if isinstance(keywords, list):
            synthetic.append(f"Keywords: {', '.join(keywords)}.")

    # Combine
    synthetic_text = " ".join(synthetic)
    return f"{synthetic_text}\n\n{content}"
```

#### 5.2 Update `query_router.py`

Add hierarchical query detection (as shown in CLASSIFICATION_TAXONOMY.md)

#### 5.3 Update `hybrid_search.py`

Add metadata filtering for category queries

---

### Phase 6: Validation & Testing (Week 3)

#### 6.1 Automated Validation

```python
#!/usr/bin/env python3
"""
Validate all migrations
"""

def validate_all_vaults():
    """Run validation on all vaults"""
    vaults = [
        'ThistleRidgeHall',
        'Study',
        'Business-Incubator',
        'Creative-Incubator',
        'SickRabbit',
        'Praxis',
        'Library',
        'Red-White',
        'Life-Systems'
    ]

    results = {}

    for vault in vaults:
        print(f"\n=== Validating {vault} ===")
        stats = validate_vault(vault)
        results[vault] = stats

    # Generate report
    generate_validation_report(results)
```

#### 6.2 Test Cases

| Test | Query | Vault | Expected | Pass? |
|------|-------|-------|----------|-------|
| 1 | "artworks" | ThistleRidgeHall | 47 | ⏳ |
| 2 | "products" | ThistleRidgeHall | 47 | ⏳ |
| 3 | "content" | ThistleRidgeHall | 279 | ⏳ |
| 4 | "lessons" | Study | 84 | ⏳ |
| 5 | "source images" | Business-Incubator | ~300 | ⏳ |
| 6 | "projects" | Business-Incubator | ~50 | ⏳ |
| 7 | "creative concepts" | SickRabbit | ~30 | ⏳ |
| 8 | "knowledge" | all | ~300 | ⏳ |

---

## 🛡️ Safety Measures

### Backup Strategy

**Three levels of backups:**

1. **Full system backup** (before starting)
   ```bash
   cp -r Multi-Vault Multi-Vault-BACKUP-2025-10-21
   ```

2. **Per-vault backups** (before each vault migration)
   ```bash
   cp -r ThistleRidgeHall.vault ThistleRidgeHall.vault-BACKUP-pre-migration
   ```

3. **Per-file backups** (during migration script)
   - Each file backed up to `Multi-Vault-MIGRATION-BACKUPS/` before modification

### Rollback Procedure

**If migration fails:**

```bash
# Stop all services
./stop-services.sh

# Restore from backup
rm -rf Multi-Vault
mv Multi-Vault-BACKUP-2025-10-21 Multi-Vault

# Or restore single vault
rm -rf Multi-Vault/ThistleRidgeHall.vault
mv ThistleRidgeHall.vault-BACKUP-pre-migration Multi-Vault/ThistleRidgeHall.vault

# Restart services
./start-services.sh
```

### Validation Gates

**Must pass before proceeding to next phase:**

- ✅ All files have valid YAML syntax
- ✅ Required properties present (type, category)
- ✅ Category valid for type
- ✅ Random sample of 10 files manually reviewed
- ✅ RAG query tests pass
- ✅ No files corrupted or lost

---

## 📅 Timeline

| Phase | Duration | Tasks | Deliverables |
|-------|----------|-------|--------------|
| **Phase 1** | 2 days | Backups, discovery, planning | Inventory files, stats |
| **Phase 2** | 3 days | High-priority vaults | TRH, Study, BI migrated |
| **Phase 3** | 5 days | Medium-priority vaults | 4 vaults migrated |
| **Phase 4** | 3 days | Low-priority vaults | All vaults migrated |
| **Phase 5** | 3 days | RAG service updates | Enhanced search |
| **Phase 6** | 2 days | Testing & validation | Validation report |
| **TOTAL** | **18 days** (~3.5 weeks) | | All systems migrated |

---

## ✅ Success Criteria

### Technical Success:
- ✅ All 1,269 documents have `type` + `category`
- ✅ All templates updated with new schema
- ✅ YAML validation passes 100%
- ✅ RAG service understands hierarchy
- ✅ All test queries return correct counts
- ✅ No data loss or corruption

### User Success:
- ✅ Search accuracy improved (artworks: 20 → 47 ✓)
- ✅ Consistent structure across vaults
- ✅ Easy to classify new notes
- ✅ Clear documentation for users

---

## 📚 Scripts Summary

**Created for this migration:**

1. `discover-templates.py` - Find all templates
2. `analyze-documents.py` - Analyze current state
3. `migrate-thistleridgehall.py` - Migrate TRH artworks
4. `migrate-study.py` - Migrate Study lessons
5. `migrate-business-incubator.py` - Migrate BI files
6. `migrate-vault.py` - Generic vault migrator
7. `validate-classification.py` - Validate YAML hierarchy
8. `validate-all-vaults.py` - Full system validation
9. `generate-report.py` - Create migration report

**All scripts include:**
- Automatic backups
- Error handling
- Progress logging
- Dry-run mode
- Detailed reporting

---

## 🎯 Next Steps

**Immediate (Today):**
1. ✅ Review this migration plan
2. ⏳ Approve approach and timeline
3. ⏳ Create full system backup

**This Week:**
1. ⏳ Run discovery scripts
2. ⏳ Verify inventory
3. ⏳ Start Phase 2 (ThistleRidgeHall)

**Next Week:**
1. ⏳ Complete high-priority vaults
2. ⏳ Begin medium-priority vaults
3. ⏳ Update RAG service

---

## 📞 Decision Points

**Need decisions on:**

1. **Migration pace:** Fast (1 week) vs. Careful (3 weeks)?
   - Recommendation: **Careful** - too important to rush

2. **Template updates:** Before or after document migration?
   - Recommendation: **Before** - prevents new files with old schema

3. **RAG updates:** During or after document migration?
   - Recommendation: **After** - documents first, then enhance RAG

4. **Validation rigor:** Spot-check or comprehensive?
   - Recommendation: **Comprehensive** - validate every file

---

**Status:** 🟡 **Plan Complete - Awaiting Approval**
**Risk Level:** 🟢 **Low** (with comprehensive backups and validation)
**Impact:** 🔴 **Critical** (Foundation for entire knowledge system)

---

**Version History:**
- v1.0 (2025-10-21) - Initial migration plan
- v1.1 (2025-10-21) - **Updated priorities per user:** ThistleRidgeHall → Praxis → Library (highest priority)
