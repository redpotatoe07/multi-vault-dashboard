from pathlib import Path
import re

# Define all remaining vaults
vaults = {
    'Study': {
        'path': Path('C:/Users/redpo/repos/Obsidian/Multi-Vault/Study.vault'),
        'type': 'knowledge',
        'category': 'lesson',
        'domain': 'language-learning',
        'keywords': ['language-learning', 'study']
    },
    'Creative-Incubator': {
        'path': Path('C:/Users/redpo/repos/Obsidian/Multi-Vault/Creative-Incubator.vault'),
        'type': 'creative',
        'category': 'project',
        'domain': 'creative',
        'keywords': ['creative-project', 'incubator']
    },
    'Red-White': {
        'path': Path('C:/Users/redpo/repos/Obsidian/Multi-Vault/Red-White.vault'),
        'type': 'creative',
        'category': 'writing',
        'domain': 'fiction',
        'keywords': ['fiction-writing', 'creative']
    },
    'SickRabbit': {
        'path': Path('C:/Users/redpo/repos/Obsidian/Multi-Vault/SickRabbit.vault'),
        'type': 'creative',
        'category': 'concept',
        'domain': 'visual-art',
        'keywords': ['art-concept', 'creative']
    },
    'Life-Systems': {
        'path': Path('C:/Users/redpo/repos/Obsidian/Multi-Vault/Life-Systems.vault'),
        'type': 'personal',
        'category': 'administration',
        'domain': 'personal',
        'keywords': ['personal', 'life-admin']
    }
}

def infer_keyword(filename):
    name = filename.lower()
    name = re.sub(r'[-_]', ' ', name)
    words = [w for w in name.split() if len(w) > 3]
    return '-'.join(words[:2]) if words else 'document'

def migrate_file(file_path, vault_config):
    try:
        content = file_path.read_text(encoding='utf-8')

        # Extract body
        body_content = content
        if content.strip().startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                body_content = parts[2].lstrip('\n')

        # Build YAML
        yaml_lines = ['---']
        yaml_lines.append(f'type: {vault_config["type"]}')
        yaml_lines.append(f'category: {vault_config["category"]}')
        yaml_lines.append(f'domain: {vault_config["domain"]}')
        yaml_lines.append('content-type: text')
        yaml_lines.append('status: active')

        # Keywords
        keywords = vault_config['keywords'].copy()
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
        return False

# Migrate all vaults
print('=== BATCH MIGRATION: REMAINING 5 VAULTS ===\n')

total_migrated = 0
total_files = 0

for vault_name, vault_config in vaults.items():
    vault_path = vault_config['path']

    if not vault_path.exists():
        print(f'{vault_name}: SKIP (not found)')
        continue

    all_md = [f for f in vault_path.rglob('*.md') if '.obsidian' not in str(f)]
    migrated = 0

    print(f'{vault_name}: Migrating {len(all_md)} files...')

    for file_path in all_md:
        if migrate_file(file_path, vault_config):
            migrated += 1

    total_migrated += migrated
    total_files += len(all_md)

    print(f'  OK {migrated}/{len(all_md)} files migrated')

print(f'\n=== BATCH MIGRATION COMPLETE ===')
print(f'Total vaults: 5')
print(f'Total files: {total_files}')
print(f'Migrated: {total_migrated}')
print(f'Success rate: {total_migrated/total_files*100:.1f}%')
