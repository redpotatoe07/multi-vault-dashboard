from pathlib import Path
import re

bi_path = Path('C:/Users/redpo/repos/Obsidian/Multi-Vault/Business-Incubator.vault')

def classify_file(file_path, base_path):
    """Determine classification"""
    path_str = str(file_path)

    if 'Active Projects' in path_str:
        return {
            'type': 'project',
            'category': 'business-project',
            'domain': 'business',
            'keywords': ['business-project', 'incubator']
        }
    elif 'Resource' in path_str:
        return {
            'type': 'reference',
            'category': 'resource',
            'domain': 'business',
            'keywords': ['resources', 'shared']
        }
    else:
        return {
            'type': 'project',
            'category': 'overview',
            'domain': 'business',
            'keywords': ['project']
        }

def infer_keyword(filename):
    name = filename.lower()
    name = re.sub(r'[-_]', ' ', name)
    words = [w for w in name.split() if len(w) > 3]
    return '-'.join(words[:2]) if words else 'document'

def migrate_yaml(file_path, base_path):
    try:
        content = file_path.read_text(encoding='utf-8')
        classification = classify_file(file_path, base_path)

        body_content = content
        if content.strip().startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                body_content = parts[2].lstrip('\n')

        yaml_lines = ['---']
        yaml_lines.append(f'type: {classification["type"]}')
        yaml_lines.append(f'category: {classification["category"]}')
        yaml_lines.append(f'domain: {classification["domain"]}')
        yaml_lines.append('content-type: text')
        yaml_lines.append('status: active')

        keywords = classification['keywords'].copy()
        keyword_from_file = infer_keyword(file_path.stem)
        if keyword_from_file and keyword_from_file not in keywords:
            keywords.append(keyword_from_file)

        yaml_lines.append('searchable-keywords:')
        for kw in keywords[:5]:
            yaml_lines.append(f'  - {kw}')

        yaml_lines.append('---')
        yaml_lines.append('')

        new_content = '\n'.join(yaml_lines) + body_content
        file_path.write_text(new_content, encoding='utf-8')
        return True

    except Exception as e:
        print(f'ERROR: {file_path.name}: {str(e)}')
        return False

all_md_files = [f for f in bi_path.rglob('*.md') if '.obsidian' not in str(f)]
migrated = 0

print('=== BUSINESS-INCUBATOR YAML MIGRATION ===\n')

for file_path in all_md_files:
    if migrate_yaml(file_path, bi_path):
        migrated += 1
        if migrated % 50 == 0:
            print(f'Progress: {migrated}/{len(all_md_files)}')

print(f'\n=== MIGRATION COMPLETE ===')
print(f'Total: {len(all_md_files)}')
print(f'Migrated: {migrated}')
