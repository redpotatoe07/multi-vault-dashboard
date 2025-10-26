# Migration Quick Start Guide

**Updated:** 2025-10-21 (v1.1)
**For:** Hierarchical Classification Migration

---

## 🎯 Migration Order (USER PRIORITIES)

### Phase 1: HIGHEST Priority (Week 1)
1. **ThistleRidgeHall** (279 docs)
   - Business critical
   - Fixes "artworks" search issue (20 → 47 results)
   - Rich metadata already exists

2. **Praxis** (28 docs)
   - Active content project
   - High daily usage
   - Content planning and scheduling

3. **Library** (183 docs)
   - Heavy usage for idea capture
   - Brain dump and fleeting notes
   - UUID-based system

### Phase 2: Medium Priority (Week 2)
4. **Business-Incubator** (326 docs - largest!)
5. **Study** (84 docs)
6. **Creative-Incubator** (125 docs)
7. **SickRabbit** (38 docs)

### Phase 3: Low Priority (Week 2-3)
8. **Red-White** (114 docs)
9. **Life-Systems** (92 docs)

---

## 📋 What Gets Updated

### For EVERY Vault:

✅ **All existing .md files** (add classification hierarchy)
✅ **All templates** (update with new schema)
✅ **Re-index in RAG** (with enhanced metadata)
✅ **Test queries** (verify search accuracy)

---

## 🔧 Classification Added to Each File

### ThistleRidgeHall Artworks:
```yaml
type: content
category: product
subcategory: digital-print
domain: visual-art
content-type: visual
medium: oil-painting-style
searchable-keywords:
  - visual-art
  - digital-product
  - landscape  # extracted from etsy-subject
```

### Praxis Content Schedules:
```yaml
type: tracking
category: schedule
subcategory: content-calendar
domain: video-production
content-type: textual
platform: tiktok
searchable-keywords:
  - content-planning
  - video-schedule
  - tiktok
```

### Library Fleeting Notes:
```yaml
type: knowledge
category: note
subcategory: fleeting
domain: general
content-type: textual
capture-method: quick-note
searchable-keywords:
  - fleeting-note
  - idea-capture
```

---

## 🚀 How Migration Works

### Step-by-Step for Each Vault:

**1. Backup** (automatic)
```bash
# Full vault backup created
ThistleRidgeHall.vault → ThistleRidgeHall.vault-BACKUP-pre-migration/
```

**2. Update Templates** (manual/automated)
- Add new classification hierarchy
- Preserve all existing properties
- Future files start correct

**3. Migrate Documents** (automated script)
```bash
python migrate-thistleridgehall.py

# Script does:
# - Backs up each file individually
# - Reads existing YAML
# - Adds classification hierarchy
# - Extracts keywords from content
# - Preserves ALL existing metadata
# - Writes updated file
```

**4. Validate** (automated)
```bash
python validate-classification.py ThistleRidgeHall.vault

# Checks:
# ✅ Valid YAML syntax
# ✅ Required properties present
# ✅ Category valid for type
# ✅ No data loss
```

**5. Re-index** (API call)
```bash
curl -X POST http://localhost:5001/index \
  -H "Content-Type: application/json" \
  -d '{"vault_name": "ThistleRidgeHall", "batch_size": 50, "force_reindex": true}'
```

**6. Test** (API call)
```bash
curl "http://localhost:3000/api/search?q=artworks&vault=ThistleRidgeHall"
# Expected: 47 results (was 20 before)
```

---

## 🛡️ Safety Features

### Triple-Layer Backups:
1. Full Multi-Vault system backup (before starting)
2. Per-vault backup (before each vault migration)
3. Per-file backup (during script execution)

### Rollback:
```bash
# If anything goes wrong:
rm -rf Multi-Vault/ThistleRidgeHall.vault
mv ThistleRidgeHall.vault-BACKUP-pre-migration Multi-Vault/ThistleRidgeHall.vault
```

### Validation Gates:
- ❌ Migration stops if validation fails
- ❌ Re-index only after validation passes
- ❌ No overwrites without backup

---

## 📊 Expected Results

### Search Improvements:

| Query | Vault | Before | After | Impact |
|-------|-------|--------|-------|--------|
| "artworks" | ThistleRidgeHall | 20 | **47** | +135% ✅ |
| "products" | ThistleRidgeHall | ? | **47** | Complete ✅ |
| "content schedules" | Praxis | 0 | **28** | Fixed ✅ |
| "fleeting notes" | Library | ? | **~150** | Found ✅ |
| "source images" | Business-Incubator | ? | **~300** | Complete ✅ |
| "lessons" | Study | ? | **84** | Complete ✅ |

---

## ⏱️ Timeline

### Week 1:
- **Day 1-2:** Preparation (backups, discovery, planning)
- **Day 3:** ThistleRidgeHall migration
- **Day 4:** Praxis migration
- **Day 5:** Library migration

### Week 2:
- **Days 1-5:** Medium-priority vaults (Business-Incubator, Study, Creative-Incubator, SickRabbit)

### Week 3:
- **Days 1-2:** Low-priority vaults (Red-White, Life-Systems)
- **Days 3-4:** RAG service updates
- **Day 5:** Final testing and validation

**Total: ~15 working days (3 weeks)**

---

## 📁 Scripts Created

### Discovery & Analysis:
- `discover-templates.py` - Find all templates
- `analyze-documents.py` - Analyze current YAML

### Migration Scripts (per vault):
- `migrate-thistleridgehall.py` - TRH artworks
- `migrate-praxis.py` - Praxis schedules/plans
- `migrate-library.py` - Library notes
- `migrate-business-incubator.py` - BI sources/projects
- `migrate-study.py` - Study lessons
- (etc. for each vault)

### Validation:
- `validate-classification.py` - Check single vault
- `validate-all-vaults.py` - Check entire system
- `generate-report.py` - Migration summary

---

## ✅ When Is Migration Complete?

### Technical Checkpoints:
- ✅ All 1,269 files have `type` + `category`
- ✅ All templates updated
- ✅ YAML validation 100% pass rate
- ✅ All vaults re-indexed in RAG
- ✅ Test queries return correct counts
- ✅ No files lost or corrupted

### User Experience:
- ✅ Search accuracy improved
- ✅ Consistent structure across vaults
- ✅ Easy to classify new notes
- ✅ Documentation complete

---

## 🎯 First Steps

### Option A: Start Today (Recommended)
```bash
# 1. Full backup
cd C:/Users/redpo/repos/Obsidian
cp -r Multi-Vault Multi-Vault-BACKUP-2025-10-21

# 2. Run discovery
cd C:/Users/redpo/repos/multi-vault-dashboard
python discover-templates.py
python analyze-documents.py

# 3. Review results, then proceed to ThistleRidgeHall
```

### Option B: Pilot Test (Safer)
```bash
# Test on just ThistleRidgeHall/Artworks folder (47 files)
python migrate-thistleridgehall.py --dry-run  # preview changes
python migrate-thistleridgehall.py            # execute
python validate-classification.py ThistleRidgeHall.vault/Artworks

# If successful, proceed with full migration
```

---

## 📞 Quick Reference

### Migration Order:
1. **ThistleRidgeHall** - Fix artwork search (HIGHEST)
2. **Praxis** - Active project (HIGHEST)
3. **Library** - Heavy usage (HIGHEST)
4. Business-Incubator, Study, Creative-Incubator, SickRabbit (MEDIUM)
5. Red-White, Life-Systems (LOW)

### Key Files:
- **[MIGRATION_PLAN.md](MIGRATION_PLAN.md)** - Full detailed plan
- **[CLASSIFICATION_TAXONOMY.md](CLASSIFICATION_TAXONOMY.md)** - Complete taxonomy
- **[MULTI_VAULT_YAML_SCHEMA.md](MULTI_VAULT_YAML_SCHEMA.md)** - YAML standards
- **This file** - Quick start guide

### Support:
- See full migration plan for detailed steps
- All scripts include `--help` flag
- Dry-run mode available for testing
- Comprehensive logging and reporting

---

**Status:** 🟢 **Ready to Begin**
**Risk:** 🟢 **Low** (comprehensive backups + validation)
**Impact:** 🔴 **High** (fixes search accuracy, enables future growth)

---

**Last Updated:** 2025-10-21 v1.1
**Priority Updated By:** User specification
