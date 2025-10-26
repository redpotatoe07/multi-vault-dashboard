"""
Index all vaults sequentially
"""

import requests
import time

BASE_URL = "http://localhost:5001"

vaults = [
    "Business-Incubator",
    "Creative-Incubator",
    "Library",
    "Life-Systems",
    "Praxis",
    "Red-White",
    "SickRabbit",
    "Study"
]

print("=" * 80)
print("INDEXING ALL VAULTS")
print("=" * 80)

total_docs = 0
total_time = 0

for vault in vaults:
    print(f"\n{'=' * 80}")
    print(f"Indexing: {vault}")
    print("=" * 80)

    start = time.time()

    try:
        response = requests.post(
            f"{BASE_URL}/index",
            json={"vault_name": vault, "batch_size": 20},
            timeout=300
        )

        elapsed = time.time() - start

        if response.status_code == 200:
            data = response.json()
            stats = data.get("stats", {})

            successful = stats.get("successful", 0)
            total = stats.get("total", 0)
            index_time = stats.get("elapsed_seconds", 0)
            speed = stats.get("docs_per_second", 0)

            print(f"[SUCCESS] Status: {data.get('status')}")
            print(f"          Documents: {successful}/{total}")
            print(f"          Time: {index_time:.1f}s")
            print(f"          Speed: {speed:.1f} docs/s")

            total_docs += successful
            total_time += index_time
        else:
            print(f"[ERROR] HTTP {response.status_code}: {response.text}")

    except Exception as e:
        print(f"[ERROR] {e}")

print(f"\n{'=' * 80}")
print("SUMMARY")
print("=" * 80)
print(f"Total vaults indexed: {len(vaults)}")
print(f"Total documents: {total_docs}")
print(f"Total time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
print(f"Average speed: {total_docs/total_time:.1f} docs/s")
print()
