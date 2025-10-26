from pathlib import Path
import re

library_path = Path('C:/Users/redpo/repos/Obsidian/Multi-Vault/Library.vault')

def classify_file(file_path, base_path):
    """Determine classification based on folder"""
    try:
        rel_path = file_path.relative_to(base_path)
        folder = rel_path.parts[0]
    except:
        folder = None

    # Classification map
    if 'Brain-Dump' in str(file_path):
        return {
            'type': 'knowledge',
            'category': 'note',
            'subcategory': 'fleeting',
            'domain': 'general',
            'keywords': ['fleeting-note', 'brain-dump']
        }
    elif 'Research' in str(file_path):
        return {
            'type': 'reference',
            'category': 'research',
            'subcategory': 'topic',
            'domain': 'general',
            'keywords': ['research']
        }
    elif 'Resources' in str(file_path):
        if 'Template' in str(file_path):
            return {
                'type': 'reference',
                'category': 'template',
                'domain': 'general',
                'keywords': ['template', 'resources']
            }
        else:
            return {
                'type': 'reference',
                'category': 'resource',
                'domain': 'general',
                'keywords': ['resources', 'reference']
            }
    else:
        return {
            'type': 'knowledge',
            'category': 'note',
            'domain': 'general',
            'keywords': ['note']
        }

def infer_keyword(filename):
    """Extract keyword from filename"""
    name = filename.lower()
    name = re.sub(r'[-_]', ' ', name)
    words = [w for w in name.split() if len(w) > 3]
    return '-'.join(words[:2]) if words else 'document'

def migrate_yaml(file_path, base_path):
    """Migrate file to hierarchical YAML"""
    try:
        content = file_path.read_text(encoding='utf-8')

        # Get classification
        classification = classify_file(file_path, base_path)

        # Extract body (skip old YAML if present)
        body_content = content
        if content.strip().startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                body_content = parts[2].lstrip('\n')

        # Build new YAML
        yaml_lines = ['---']
        yaml_lines.append(f'type: {classification["type"]}')
        yaml_lines.append(f'category: {classification["category"]}')
        if 'subcategory' in classification:
            yaml_lines.append(f'subcategory: {classification["subcategory"]}')
        yaml_lines.append(f'domain: {classification["domain"]}')
        yaml_lines.append('content-type: text')
        yaml_lines.append('status: draft' if classification['category'] == 'note' and classification.get('subcategory') == 'fleeting' else 'status: active')

        # Keywords
        keywords = classification['keywords'].copy()
        keyword_from_file = infer_keyword(file_path.stem)
        if keyword_from_file and keyword_from_file not in keywords:
            keywords.append(keyword_from_file)

        yaml_lines.append('searchable-keywords:')
        for kw in keywords[:5]:  # Limit to 5 keywords
            yaml_lines.append(f'  - {kw}')

        yaml_lines.append('---')
        yaml_lines.append('')

        new_content = '\n'.join(yaml_lines) + body_content
        file_path.write_text(new_content, encoding='utf-8')
        return True

    except Exception as e:
        print(f'ERROR: {file_path.name}: {str(e)}')
        return False

# Migrate all files
all_md_files = [f for f in library_path.rglob('*.md') if '.obsidian' not in str(f)]
migrated = 0

print('=== LIBRARY YAML MIGRATION ===\n')

for file_path in all_md_files:
    if migrate_yaml(file_path, library_path):
        migrated += 1
        if migrated % 20 == 0:
            print(f'Progress: {migrated}/{len(all_md_files)}')

print(f'\n=== MIGRATION COMPLETE ===')
print(f'Total files: {len(all_md_files)}')
print(f'Migrated: {migrated}')
print(f'Errors: {len(all_md_files) - migrated}')
