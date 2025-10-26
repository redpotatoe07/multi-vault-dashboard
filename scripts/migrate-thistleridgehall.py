#!/usr/bin/env python3
"""
Migrate ThistleRidgeHall artwork files to hierarchical classification

This script:
1. Backs up each file before modification
2. Adds hierarchical classification (type, category, subcategory, domain)
3. Extracts searchable keywords from existing metadata
4. Preserves ALL existing YAML properties
5. Validates YAML syntax
"""

import re
import os
import sys
from pathlib import Path
from datetime import datetime
import json

# Paths
ARTWORKS_DIR = Path("C:/Users/redpo/repos/Obsidian/Multi-Vault/ThistleRidgeHall.vault/Artworks")
BACKUP_DIR = Path("C:/Users/redpo/repos/Obsidian/Multi-Vault-MIGRATION-BACKUPS/ThistleRidgeHall")
LOG_DIR = Path("c:/Users/redpo/repos/multi-vault-dashboard/logs")

def setup_logging():
    """Create log directory and file"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    log_file = LOG_DIR / f"migration-thistleridgehall-{timestamp}.log"
    return log_file

def log_message(log_file, message, also_print=True):
    """Write to log file and optionally print"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_line = f"[{timestamp}] {message}\n"

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_line)

    if also_print:
        # Replace unicode characters for console output
        console_message = message.replace('\u2713', 'OK').replace('\u26a0', 'WARN').replace('\u2717', 'X')
        print(console_message)

def backup_file(filepath, log_file):
    """Create backup before modification"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / filepath.name

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)

        log_message(log_file, f"  Backed up: {filepath.name}", False)
        return backup_path
    except Exception as e:
        log_message(log_file, f"  ERROR backing up {filepath.name}: {e}")
        return None

def determine_medium(yaml_content):
    """Determine artwork medium from existing content"""
    content_lower = yaml_content.lower()

    if 'watercolor' in content_lower or 'watercolour' in content_lower:
        return 'watercolor-style'
    elif 'photograph' in content_lower or 'photo' in content_lower or 'photography' in content_lower:
        return 'photography-style'
    elif 'digital-art' in content_lower or 'digital art' in content_lower:
        return 'digital-art'
    elif 'illustration' in content_lower:
        return 'illustration-style'
    else:
        return 'oil-painting-style'  # Default for most TRH artworks

def extract_searchable_keywords(yaml_content, log_file):
    """Extract keywords from etsy-subject and collection"""
    keywords = ['visual-art', 'digital-product']

    # Extract etsy-subject (multi-line array format)
    subject_section = re.search(r'etsy-subject:\s*\n((?:\s+-\s+[^\n]+\n?)+)', yaml_content)
    if subject_section:
        subjects = re.findall(r'-\s+"?([^"\n]+)"?', subject_section.group(1))
        for subject in subjects[:3]:  # Take up to 3
            # Clean and convert to keyword
            keyword = subject.strip().lower()
            keyword = keyword.replace(' & ', '-').replace(' ', '-')
            keyword = keyword.replace(',', '')
            if keyword and keyword not in keywords:
                keywords.append(keyword)

    # Extract from collection name
    collection_match = re.search(r'collection:\s*\n\s+-\s+"?([^"\n]+)"?', yaml_content)
    if collection_match:
        collection = collection_match.group(1).lower()
        # Add thematic keywords based on collection
        if 'borderland' in collection:
            if 'borderlands' not in keywords:
                keywords.append('borderlands')
        if 'meadow' in collection or 'mist' in collection:
            if 'pastoral' not in keywords:
                keywords.append('pastoral')
        if 'flora' in collection or 'flower' in collection:
            if 'botanical' not in keywords:
                keywords.append('botanical')

    # Extract from etsy-home-style
    style_section = re.search(r'etsy-home-style:\s*\n((?:\s+-\s+[^\n]+\n?)+)', yaml_content)
    if style_section:
        styles = re.findall(r'-\s+"?([^"\n]+)"?', style_section.group(1))
        for style in styles[:2]:  # Take up to 2
            keyword = style.strip().lower().replace(' ', '-')
            if keyword and keyword not in keywords and len(keywords) < 8:
                keywords.append(keyword)

    return keywords

def migrate_file(filepath, log_file, dry_run=False):
    """Add hierarchical classification to artwork file"""
    log_message(log_file, f"\n{'='*60}")
    log_message(log_file, f"Processing: {filepath.name}")

    # Backup first
    if not dry_run:
        backup_path = backup_file(filepath, log_file)
        if not backup_path:
            return False, "Backup failed"

    # Read file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        log_message(log_file, f"  ERROR reading file: {e}")
        return False, f"Read error: {e}"

    # Parse YAML
    yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not yaml_match:
        log_message(log_file, f"  ⚠ No YAML frontmatter found - skipping")
        return False, "No YAML"

    yaml_content = yaml_match.group(1)
    body = content[yaml_match.end():]

    # Check if already migrated
    if 'category:' in yaml_content and 'subcategory:' in yaml_content:
        log_message(log_file, f"  ✓ Already migrated - skipping")
        return False, "Already migrated"

    # Determine properties
    medium = determine_medium(yaml_content)
    keywords = extract_searchable_keywords(yaml_content, log_file)

    log_message(log_file, f"  Medium: {medium}")
    log_message(log_file, f"  Keywords: {', '.join(keywords)}")

    # Build new classification block
    classification = f"""type: content
category: product
subcategory: digital-print
domain: visual-art
content-type: visual
medium: {medium}"""

    # Handle existing 'type' property
    if re.search(r'^type:', yaml_content, re.MULTILINE):
        # Replace existing type property and its value(s)
        yaml_content = re.sub(
            r'^type:.*?(?=\n[a-z_-]+:|\Z)',
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

        # Add before 'tags:' if it exists, otherwise before body
        if re.search(r'^tags:', yaml_content, re.MULTILINE):
            yaml_content = re.sub(
                r'^tags:',
                keywords_block + 'tags:',
                yaml_content,
                count=1,
                flags=re.MULTILINE
            )
        else:
            # Add at end of YAML
            yaml_content = yaml_content.rstrip() + "\n" + keywords_block

    # Reconstruct file
    new_content = f"---\n{yaml_content}\n---{body}"

    # Dry run - just show what would change
    if dry_run:
        log_message(log_file, f"  [DRY RUN] Would add classification:")
        log_message(log_file, f"    type: content")
        log_message(log_file, f"    category: product")
        log_message(log_file, f"    subcategory: digital-print")
        log_message(log_file, f"    domain: visual-art")
        log_message(log_file, f"    medium: {medium}")
        log_message(log_file, f"    searchable-keywords: {keywords}")
        return True, "Dry run success"

    # Write updated file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        log_message(log_file, f"  ✓ Migration successful")
        return True, "Success"
    except Exception as e:
        log_message(log_file, f"  ERROR writing file: {e}")
        return False, f"Write error: {e}"

def validate_yaml(filepath, log_file):
    """Basic YAML validation"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for YAML frontmatter
        yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not yaml_match:
            return False, "No YAML frontmatter"

        yaml_content = yaml_match.group(1)

        # Check required properties
        required = ['type:', 'category:', 'subcategory:']
        missing = [prop for prop in required if prop not in yaml_content]

        if missing:
            return False, f"Missing: {', '.join(missing)}"

        # Check YAML structure (basic)
        if yaml_content.count('---') > 0:
            return False, "Malformed YAML (extra ---)"

        return True, "Valid"
    except Exception as e:
        return False, f"Validation error: {e}"

def main():
    """Main migration function"""
    import argparse

    parser = argparse.ArgumentParser(description='Migrate ThistleRidgeHall artwork files')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying files')
    args = parser.parse_args()

    # Setup logging
    log_file = setup_logging()

    log_message(log_file, "="*60)
    log_message(log_file, "ThistleRidgeHall Artwork Migration")
    log_message(log_file, "="*60)
    log_message(log_file, f"Mode: {'DRY RUN' if args.dry_run else 'LIVE MIGRATION'}")
    log_message(log_file, f"Log file: {log_file}")
    log_message(log_file, "="*60)

    if not ARTWORKS_DIR.exists():
        log_message(log_file, f"ERROR: Artworks directory not found: {ARTWORKS_DIR}")
        return 1

    # Count files
    md_files = list(ARTWORKS_DIR.glob("*.md"))
    log_message(log_file, f"\nFound {len(md_files)} markdown files in Artworks/")

    if args.dry_run:
        log_message(log_file, "\n[!] DRY RUN MODE - No files will be modified [!]\n")
    else:
        response = input(f"\nProceed with migration of {len(md_files)} files? (yes/no): ")
        if response.lower() != 'yes':
            log_message(log_file, "Migration cancelled by user")
            return 0

    # Migrate files
    stats = {
        'total': 0,
        'migrated': 0,
        'skipped': 0,
        'errors': 0
    }

    results = []

    for md_file in sorted(md_files):
        stats['total'] += 1
        success, message = migrate_file(md_file, log_file, args.dry_run)

        if success:
            stats['migrated'] += 1
        elif "skipping" in message.lower() or "already" in message.lower():
            stats['skipped'] += 1
        else:
            stats['errors'] += 1

        results.append({
            'file': md_file.name,
            'success': success,
            'message': message
        })

    # Validation phase (only if not dry run and files were migrated)
    if not args.dry_run and stats['migrated'] > 0:
        log_message(log_file, "\n" + "="*60)
        log_message(log_file, "VALIDATION PHASE")
        log_message(log_file, "="*60)

        validation_errors = 0
        for md_file in sorted(md_files):
            valid, message = validate_yaml(md_file, log_file)
            if not valid:
                log_message(log_file, f"  ✗ {md_file.name}: {message}")
                validation_errors += 1

        if validation_errors == 0:
            log_message(log_file, f"  ✓ All {len(md_files)} files validated successfully")
        else:
            log_message(log_file, f"  ⚠ {validation_errors} validation errors found")

    # Summary
    log_message(log_file, "\n" + "="*60)
    log_message(log_file, "MIGRATION SUMMARY")
    log_message(log_file, "="*60)
    log_message(log_file, f"Total files: {stats['total']}")
    log_message(log_file, f"Migrated: {stats['migrated']}")
    log_message(log_file, f"Skipped: {stats['skipped']}")
    log_message(log_file, f"Errors: {stats['errors']}")

    if not args.dry_run and stats['migrated'] > 0:
        log_message(log_file, f"\nBackups saved to: {BACKUP_DIR}")

    log_message(log_file, f"Log saved to: {log_file}")

    # Save detailed results
    results_file = LOG_DIR / f"migration-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump({
            'stats': stats,
            'results': results,
            'dry_run': args.dry_run
        }, f, indent=2)

    log_message(log_file, f"Results saved to: {results_file}")

    log_message(log_file, "\n" + "="*60)
    if args.dry_run:
        log_message(log_file, "DRY RUN COMPLETE - No files modified")
    else:
        log_message(log_file, "MIGRATION COMPLETE")
    log_message(log_file, "="*60)

    return 0 if stats['errors'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
