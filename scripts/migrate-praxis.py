from pathlib import Path
import re
import yaml

praxis_path = Path('C:/Users/redpo/repos/Obsidian/Multi-Vault/Praxis.vault')

def extract_folder_from_path(file_path, base_path):
    """Extract top-level folder name"""
    try:
        rel_path = file_path.relative_to(base_path)
        return rel_path.parts[0]
    except:
        return None

def classify_file(file_path, base_path):
    """Determine classification based on folder and filename"""
    folder = extract_folder_from_path(file_path, base_path)
    filename = file_path.stem.lower()

    # Classification map
    classifications = {
        '00_Home': {
            'type': 'project',
            'category': 'overview',
            'domain': 'business',
            'keywords': ['project-overview', 'praxis-dashboard', 'content-creation']
        },
        '01_Planning': {
            'type': 'project',
            'category': 'planning',
            'subcategory': 'schedule' if 'schedule' in filename or 'calendar' in filename else 'business-plan',
            'domain': 'business',
            'keywords': ['planning', 'strategy']
        },
        '02_Content': {
            'type': 'reference',
            'category': 'documentation',
            'subcategory': 'content-strategy',
            'domain': 'content-creation',
            'keywords': ['content-framework', 'content-strategy']
        },
        '02_Research': {
            'type': 'reference',
            'category': 'research',
            'subcategory': 'market',
            'domain': 'business',
            'keywords': ['research', 'analysis']
        },
        '03_Strategy': {
            'type': 'project',
            'category': 'planning',
            'subcategory': 'brand',
            'domain': 'business',
            'keywords': ['strategy', 'branding']
        },
        '04_Development': {
            'type': 'content',
            'category': 'script',
            'subcategory': 'video-script' if 'script' in str(file_path).lower() else 'concept',
            'domain': 'content-creation',
            'keywords': ['video-script', 'content-production'] if 'script' in str(file_path).lower() else ['concept', 'idea']
        },
        '05_Assets': {
            'type': 'reference',
            'category': 'resource',
            'subcategory': 'library',
            'domain': 'content-creation',
            'keywords': ['resources', 'assets']
        },
        '06_Archive': {
            'type': 'reference',
            'category': 'documentation',
            'status': 'archived',
            'domain': 'business',
            'keywords': ['archived']
        },
        '08_Resources': {
            'type': 'reference',
            'category': 'template',
            'domain': 'content-creation',
            'keywords': ['template', 'resources']
        }
    }

    return classifications.get(folder, {
        'type': 'reference',
        'category': 'documentation',
        'domain': 'business',
        'keywords': ['document']
    })

def infer_keyword_from_filename(filename):
    """Extract meaningful keyword from filename"""
    name = filename.lower()
    name = re.sub(r'[-_]', ' ', name)
    words = [w for w in name.split() if len(w) > 3 and w not in ['readme', 'guide', 'document']]
    return '-'.join(words[:2]) if words else 'document'

def migrate_yaml(file_path, base_path):
    """Migrate file YAML to new hierarchical format"""
    try:
        content = file_path.read_text(encoding='utf-8')

        # Get classification
        classification = classify_file(file_path, base_path)

        # Extract existing YAML if present
        old_yaml = {}
        body_content = content

        if content.strip().startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    old_yaml = yaml.safe_load(parts[1]) or {}
                    body_content = parts[2].lstrip('\n')
                except:
                    pass

        # Build new YAML
        new_yaml_dict = {
            'type': classification['type'],
            'category': classification['category']
        }

        if 'subcategory' in classification:
            new_yaml_dict['subcategory'] = classification['subcategory']

        new_yaml_dict['domain'] = classification['domain']
        new_yaml_dict['content-type'] = 'text'

        # Status
        if '06_Archive' in str(file_path):
            new_yaml_dict['status'] = 'archived'
        elif isinstance(old_yaml.get('status'), list):
            new_yaml_dict['status'] = old_yaml['status'][0] if old_yaml['status'] else 'active'
        elif old_yaml.get('status'):
            new_yaml_dict['status'] = old_yaml['status']
        else:
            new_yaml_dict['status'] = 'draft' if classification['category'] == 'script' else 'active'

        # searchable-keywords
        keywords = classification['keywords'].copy()
        keyword_from_file = infer_keyword_from_filename(file_path.stem)
        if keyword_from_file and keyword_from_file not in keywords:
            keywords.append(keyword_from_file)

        new_yaml_dict['searchable-keywords'] = keywords

        # Preserve old tags if they exist
        if old_yaml.get('tags'):
            new_yaml_dict['tags'] = old_yaml['tags']

        # Write new YAML
        yaml_lines = ['---']
        for key, value in new_yaml_dict.items():
            if isinstance(value, list):
                yaml_lines.append(f'{key}:')
                for item in value:
                    yaml_lines.append(f'  - {item}')
            else:
                yaml_lines.append(f'{key}: {value}')
        yaml_lines.append('---')
        yaml_lines.append('')

        new_content = '\n'.join(yaml_lines) + body_content

        file_path.write_text(new_content, encoding='utf-8')
        return True

    except Exception as e:
        print(f'ERROR migrating {file_path.name}: {str(e)}')
        return False

# Migrate all files
all_md_files = list(praxis_path.rglob('*.md'))
migrated = 0
errors = 0

print('=== PRAXIS YAML MIGRATION ===\n')

for file_path in all_md_files:
    # Skip .obsidian folder
    if '.obsidian' in str(file_path):
        continue

    if migrate_yaml(file_path, praxis_path):
        migrated += 1
        rel_path = file_path.relative_to(praxis_path)
        print(f'OK {rel_path}')
    else:
        errors += 1

print(f'\n=== MIGRATION COMPLETE ===')
print(f'Total files: {len(all_md_files)}')
print(f'Migrated: {migrated}')
print(f'Errors: {errors}')
