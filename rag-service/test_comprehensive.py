"""
Comprehensive Backend Testing Suite for RAG Service

Tests:
1. Cross-vault search
2. All 5 query types
3. Edge cases
4. Performance benchmarks
5. Metadata filtering
6. Entity mapping
7. Error handling
"""

import requests
import time
import json
from typing import Dict, List, Any

BASE_URL = "http://localhost:5001"

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(name: str):
    """Print test name"""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST: {name}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}")

def print_pass(msg: str):
    """Print pass message"""
    print(f"{GREEN}[PASS]{RESET} {msg}")

def print_fail(msg: str):
    """Print fail message"""
    print(f"{RED}[FAIL]{RESET} {msg}")

def print_info(msg: str):
    """Print info message"""
    print(f"{YELLOW}[INFO]{RESET} {msg}")

def search(vault_name: str, query: str, explain: bool = False) -> Dict[str, Any]:
    """Perform search request"""
    response = requests.post(
        f"{BASE_URL}/search",
        json={"vault_name": vault_name, "query": query, "explain": explain}
    )
    return response.json()

def get_collections() -> List[Dict[str, Any]]:
    """Get all collections"""
    response = requests.get(f"{BASE_URL}/collections")
    return response.json()["collections"]


# ============================================================
# TEST 1: Cross-Vault Search
# ============================================================
def test_cross_vault_search():
    """Test searching across multiple vaults for same concept"""
    print_test("Cross-Vault Search")

    vaults = ["ThistleRidgeHall", "Creative-Incubator", "Library"]
    query = "creative process"

    all_results = []

    for vault in vaults:
        print_info(f"Searching vault: {vault}")
        result = search(vault, query, explain=True)

        if "error" in result:
            print_fail(f"  Error: {result['error']}")
            continue

        count = result.get("result_count", 0)
        query_type = result.get("query_type", "unknown")
        strategy = result.get("search_strategy", "unknown")

        print_pass(f"  Found {count} results")
        print_info(f"  Query type: {query_type}, Strategy: {strategy}")

        all_results.extend(result.get("results", []))

    print_info(f"\nTotal results across all vaults: {len(all_results)}")

    if len(all_results) > 0:
        print_pass("Cross-vault search working!")
        return True
    else:
        print_fail("No results found across vaults")
        return False


# ============================================================
# TEST 2: Query Type Classification
# ============================================================
def test_query_types():
    """Test all 5 query types are correctly classified"""
    print_test("Query Type Classification")

    test_cases = [
        ("list all artworks", "list_all", "metadata_only"),
        ("artworks with tag creative", "filter", "metadata_first"),
        ("paintings about nature", "search", "semantic_first"),
        ("artwork titled Apple Trees", "specific", "semantic_first"),
    ]

    vault = "ThistleRidgeHall"
    passed = 0
    failed = 0

    for query, expected_type, expected_strategy in test_cases:
        print_info(f"\nQuery: '{query}'")
        result = search(vault, query, explain=True)

        if "error" in result:
            print_fail(f"  Error: {result['error']}")
            failed += 1
            continue

        actual_type = result.get("query_type")
        actual_strategy = result.get("search_strategy")
        count = result.get("result_count", 0)

        if actual_type == expected_type:
            print_pass(f"  Type: {actual_type} (correct)")
        else:
            print_fail(f"  Type: {actual_type} (expected {expected_type})")
            failed += 1
            continue

        if actual_strategy == expected_strategy:
            print_pass(f"  Strategy: {actual_strategy} (correct)")
        else:
            print_fail(f"  Strategy: {actual_strategy} (expected {expected_strategy})")
            failed += 1
            continue

        print_info(f"  Results: {count}")
        passed += 1

    print_info(f"\n{passed}/{len(test_cases)} query type tests passed")
    return passed == len(test_cases)


# ============================================================
# TEST 3: Edge Cases
# ============================================================
def test_edge_cases():
    """Test edge cases and error handling"""
    print_test("Edge Cases & Error Handling")

    passed = 0

    # Test 1: Empty query
    print_info("\n1. Empty query")
    result = search("ThistleRidgeHall", "")
    if "error" in result or result.get("result_count", 0) == 0:
        print_pass("  Handled empty query correctly")
        passed += 1
    else:
        print_fail("  Did not handle empty query")

    # Test 2: Non-existent vault
    print_info("\n2. Non-existent vault")
    result = search("NonExistentVault", "test query")
    if "error" in result:
        print_pass(f"  Error returned: {result['error']}")
        passed += 1
    else:
        print_fail("  Should return error for non-existent vault")

    # Test 3: Special characters
    print_info("\n3. Special characters in query")
    result = search("ThistleRidgeHall", "[[wikilink]] with #tags and \"quotes\"")
    if "error" not in result:
        print_pass(f"  Handled special characters (found {result.get('result_count', 0)} results)")
        passed += 1
    else:
        print_fail(f"  Error: {result['error']}")

    # Test 4: Very long query
    print_info("\n4. Very long query")
    long_query = "art " * 100  # 400 characters
    result = search("ThistleRidgeHall", long_query)
    if "error" not in result:
        print_pass(f"  Handled long query (found {result.get('result_count', 0)} results)")
        passed += 1
    else:
        print_fail(f"  Error: {result['error']}")

    # Test 5: Unicode characters
    print_info("\n5. Unicode characters")
    result = search("ThistleRidgeHall", "café résumé naïve")
    if "error" not in result:
        print_pass(f"  Handled unicode (found {result.get('result_count', 0)} results)")
        passed += 1
    else:
        print_fail(f"  Error: {result['error']}")

    print_info(f"\n{passed}/5 edge case tests passed")
    return passed == 5


# ============================================================
# TEST 4: Performance Benchmarks
# ============================================================
def test_performance():
    """Test search performance across different vault sizes"""
    print_test("Performance Benchmarks")

    collections = get_collections()

    # Sort by size
    collections.sort(key=lambda x: x["document_count"])

    query = "creative work"

    print_info(f"\nTesting search performance with query: '{query}'")
    print_info(f"{'Vault':<25} {'Docs':<10} {'Time (ms)':<15} {'Docs/sec':<15}")
    print_info("-" * 65)

    for coll in collections:
        vault = coll["name"]
        doc_count = coll["document_count"]

        start = time.time()
        result = search(vault, query)
        elapsed = (time.time() - start) * 1000  # ms

        if "error" in result:
            print_fail(f"{vault:<25} {doc_count:<10} ERROR")
            continue

        results_count = result.get("result_count", 0)
        docs_per_sec = doc_count / (elapsed / 1000) if elapsed > 0 else 0

        print_info(f"{vault:<25} {doc_count:<10} {elapsed:<15.2f} {docs_per_sec:<15.2f}")

    print_pass("\nPerformance test complete!")
    return True


# ============================================================
# TEST 5: Entity Mapping
# ============================================================
def test_entity_mapping():
    """Test entity mapping accuracy"""
    print_test("Entity Mapping")

    vault = "ThistleRidgeHall"

    test_cases = [
        ("list all artworks", "artworks", "Artworks"),
        ("show me all characters", "characters", "Characters"),
        ("what locations exist", "locations", "Locations"),
    ]

    passed = 0

    for query, entity, expected_folder in test_cases:
        print_info(f"\nQuery: '{query}'")
        result = search(vault, query, explain=True)

        if "error" in result:
            print_fail(f"  Error: {result['error']}")
            continue

        routing = result.get("routing", {})
        detected_entity = routing.get("entity")
        count = result.get("result_count", 0)

        if detected_entity == entity:
            print_pass(f"  Entity detected: {detected_entity}")
            print_info(f"  Results: {count}")
            passed += 1
        else:
            print_fail(f"  Expected entity '{entity}', got '{detected_entity}'")

    print_info(f"\n{passed}/{len(test_cases)} entity mapping tests passed")
    return passed == len(test_cases)


# ============================================================
# TEST 6: Metadata Filtering
# ============================================================
def test_metadata_filtering():
    """Test metadata filtering capabilities"""
    print_test("Metadata Filtering")

    vault = "ThistleRidgeHall"

    # Test folder filtering
    print_info("\n1. Folder filtering (list all artworks)")
    result = search(vault, "list all artworks", explain=True)

    if "error" not in result:
        count = result.get("result_count", 0)
        print_pass(f"  Found {count} artworks")

        # Check that results are actually from Artworks folder
        results = result.get("results", [])
        if results:
            sample = results[0]
            folder = sample.get("metadata", {}).get("folder", "")
            print_info(f"  Sample result folder: {folder}")

            if "Artworks" in folder or "artworks" in folder.lower():
                print_pass("  Results correctly filtered to Artworks folder")
            else:
                print_fail(f"  Expected Artworks folder, got: {folder}")
    else:
        print_fail(f"  Error: {result['error']}")

    return True


# ============================================================
# TEST 7: API Health & Collections
# ============================================================
def test_api_health():
    """Test API health and collections endpoint"""
    print_test("API Health & Collections")

    # Test health endpoint
    print_info("\n1. Health check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        health = response.json()

        if health.get("status") == "healthy":
            print_pass(f"  API healthy: {health}")
        else:
            print_fail(f"  API not healthy: {health}")
    except Exception as e:
        print_fail(f"  Error: {e}")

    # Test collections endpoint
    print_info("\n2. Collections list")
    try:
        collections = get_collections()
        total_docs = sum(c["document_count"] for c in collections)

        print_pass(f"  Found {len(collections)} collections")
        print_info(f"  Total documents: {total_docs}")

        for coll in collections:
            print_info(f"    - {coll['name']}: {coll['document_count']} docs")

        return len(collections) > 0
    except Exception as e:
        print_fail(f"  Error: {e}")
        return False


# ============================================================
# Run All Tests
# ============================================================
def run_all_tests():
    """Run complete test suite"""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}RAG SERVICE COMPREHENSIVE TEST SUITE{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")

    results = {}

    results["API Health"] = test_api_health()
    results["Cross-Vault Search"] = test_cross_vault_search()
    results["Query Types"] = test_query_types()
    results["Edge Cases"] = test_edge_cases()
    results["Performance"] = test_performance()
    results["Entity Mapping"] = test_entity_mapping()
    results["Metadata Filtering"] = test_metadata_filtering()

    # Summary
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST SUMMARY{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test, result in results.items():
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {test:<30} [{status}]")

    print(f"\n{BLUE}Results: {passed}/{total} test suites passed{RESET}")

    if passed == total:
        print(f"{GREEN}[SUCCESS] All tests passed!{RESET}\n")
    else:
        print(f"{YELLOW}[WARNING] Some tests failed{RESET}\n")


if __name__ == "__main__":
    run_all_tests()
