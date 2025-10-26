"""
Test script for MetadataExtractor

This verifies that metadata extraction works with real Obsidian vault files.
"""

import sys
sys.path.insert(0, '.')

from metadata_extractor import MetadataExtractor
import json

def test_metadata_extractor():
    """Test metadata extraction with a real vault file"""
    print("=" * 60)
    print("Testing MetadataExtractor")
    print("=" * 60)

    # Path to a real vault
    vault_path = r"C:\Users\redpo\repos\Obsidian\Multi-Vault\ThistleRidgeHall.vault"

    print(f"\n1. Initializing MetadataExtractor...")
    print(f"   Vault: {vault_path}")

    try:
        extractor = MetadataExtractor(vault_path)
        print(f"   [OK] Extractor initialized")
    except Exception as e:
        print(f"   [ERROR] Failed to initialize: {e}")
        return

    # Get all vault files
    print(f"\n2. Discovering vault files...")
    files = extractor.get_vault_files()
    print(f"   Found {len(files)} markdown files")

    if len(files) == 0:
        print("   [WARNING] No files found! Check vault path.")
        return

    # Test single file extraction
    print(f"\n3. Testing single file extraction...")
    test_file = files[0]  # Use first file
    print(f"   File: {test_file}")

    try:
        metadata = extractor.extract(test_file)
        print(f"   [OK] Metadata extracted successfully!")
        print(f"\n   Extracted fields:")
        print(f"   - File path: {metadata['file_path']}")
        print(f"   - Filename: {metadata['filename']}")
        print(f"   - Folder: {metadata['folder']}")
        print(f"   - Word count: {metadata['word_count']}")
        print(f"   - Created: {metadata['created']}")
        print(f"   - Modified: {metadata['modified']}")
        print(f"   - Tags: {metadata['all_tags']}")
        print(f"   - Wikilinks: {metadata['wikilinks_count']} links")
        print(f"   - Headings: {metadata['heading_count']} headings")

        if metadata['frontmatter']:
            print(f"\n   Frontmatter fields:")
            for key, value in metadata['frontmatter'].items():
                print(f"   - {key}: {value}")

        # Show first 200 chars of content
        content_preview = metadata['content'][:200].replace('\n', ' ')
        print(f"\n   Content preview: {content_preview}...")

    except Exception as e:
        print(f"   [ERROR] Failed to extract metadata: {e}")
        import traceback
        traceback.print_exc()
        return

    # Test batch extraction (first 5 files)
    print(f"\n4. Testing batch extraction (first 5 files)...")
    test_files = files[:5]
    try:
        metadata_list = extractor.extract_batch(test_files)
        print(f"   [OK] Extracted metadata from {len(metadata_list)} files")

        for meta in metadata_list:
            print(f"   - {meta['file_path']} ({meta['word_count']} words)")

    except Exception as e:
        print(f"   [ERROR] Batch extraction failed: {e}")
        return

    # Save sample metadata to file for inspection
    print(f"\n5. Saving sample metadata to JSON...")
    output_file = "sample_metadata.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"   [OK] Saved to {output_file}")

    print("\n" + "=" * 60)
    print("[SUCCESS] All metadata extraction tests passed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_metadata_extractor()
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
