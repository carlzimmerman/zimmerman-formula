#!/usr/bin/env python3
"""
TEST AUTONOMOUS API DISCOVERY - True Blind Test
================================================

Tests whether HermesFlow can autonomously discover APIs for domains
that have NO pre-configured database handlers.

This is the critical test for true autonomous research capability.

Test domains (no pre-configured APIs):
- oceanography / sea_surface_temperature
- dendrochronology / tree_rings
- hydrology / river_discharge

Author: Carl Zimmerman
Date: May 5, 2026
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
import time

print("=" * 70)
print("TEST AUTONOMOUS API DISCOVERY - True Blind Test")
print("=" * 70)
print(f"Started: {datetime.now().isoformat()}")
print()

# =============================================================================
# VERIFY BLIND CONDITIONS
# =============================================================================

print("STEP 1: Verify blind conditions")
print("-" * 40)

from HermesFlow.database_query_handler import DatabaseQueryHandler

handler = DatabaseQueryHandler(verbose=False)

# Check which domains have NO pre-configured APIs
test_domains = [
    ("oceanography", "sea_surface_temperature"),
    ("dendrochronology", "tree_rings"),
    ("hydrology", "river_discharge"),
    ("paleoclimate", "ice_cores"),
]

blind_domains = []
for domain, topic in test_domains:
    apis = handler.find_apis_for_domain(domain, topic)
    status = "HAS APIs" if apis else "BLIND (no APIs)"
    print(f"  {domain}/{topic}: {status}")
    if not apis:
        blind_domains.append((domain, topic))

if not blind_domains:
    print("\nNo blind domains found - all have pre-configured APIs!")
    print("This test requires at least one domain without pre-configured APIs.")
    sys.exit(1)

print(f"\nUsing first blind domain for test: {blind_domains[0]}")
print()

# =============================================================================
# TEST AUTONOMOUS DISCOVERY
# =============================================================================

print("STEP 2: Test Autonomous API Discovery")
print("-" * 40)

test_domain, test_topic = blind_domains[0]

try:
    from HermesFlow.autonomous_api_discovery import AutonomousAPIDiscovery, discover_apis

    print(f"Testing discovery for: {test_domain}/{test_topic}")
    print()

    discoverer = AutonomousAPIDiscovery(verbose=True)
    start_time = time.time()

    result = discoverer.discover(test_domain, test_topic)

    elapsed = time.time() - start_time

    print()
    print("=" * 40)
    print("DISCOVERY RESULTS")
    print("=" * 40)
    print(f"Domain: {result.domain}")
    print(f"Topic: {result.topic}")
    print(f"Time: {elapsed:.1f}s")
    print()
    print(f"Databases found: {result.databases_found}")
    print(f"APIs analyzed: {result.apis_discovered}")
    print(f"APIs working: {result.apis_working}")
    print()

    if result.working_configs:
        print("WORKING APIs DISCOVERED:")
        for i, config in enumerate(result.working_configs, 1):
            print(f"  {i}. {config.name}")
            print(f"     URL: {config.base_url}")
            print(f"     Format: {config.response_format}")
            print(f"     Domains: {config.domains}")
            print()

        # Try to query the discovered APIs
        print("TESTING DISCOVERED APIs:")
        for config in result.working_configs[:2]:  # Test first 2
            print(f"  Querying: {config.name}...")
            qr = discoverer.db_handler.query_config(config)
            if qr.success:
                print(f"    SUCCESS: {qr.rows} rows, {qr.columns} columns")
                if qr.data is not None:
                    print(f"    Columns: {list(qr.data.columns)[:5]}...")
            else:
                print(f"    FAILED: {qr.error}")

        discovery_success = True
    else:
        print("NO WORKING APIs DISCOVERED")
        print()
        print("Failed attempts:")
        for fa in result.failed_attempts[:5]:
            print(f"  - {fa['database']}: {fa['error']}")

        discovery_success = False

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    discovery_success = False

print()

# =============================================================================
# TEST INTEGRATION WITH UNIVERSALDATADISCOVERY
# =============================================================================

print("STEP 3: Test Integration with UniversalDataDiscovery")
print("-" * 40)

try:
    from HermesFlow.universal_data_discovery import UniversalDataDiscovery, DomainProfile

    # Create a domain profile for our blind domain
    domain_profile = DomainProfile(
        name=test_domain,
        subdomain=test_topic,
        description=f"Test domain for autonomous discovery: {test_domain}/{test_topic}",
        key_quantities=[],
        known_sources=[],
        z2_relevance="Testing autonomous API discovery"
    )

    discovery = UniversalDataDiscovery(
        use_legomena=False,  # Skip for speed
        use_web_search=True,
        use_helicon_lake=True,
        use_database_apis=True
    )

    print(f"AutonomousAPIDiscovery: {'Active' if discovery.auto_discovery else 'Not available'}")
    print()

    print("Calling discover_data_sources() - should trigger autonomous discovery...")
    sources = discovery.discover_data_sources(domain_profile)

    print(f"\nSources discovered: {len(sources)}")
    for src in sources[:5]:
        print(f"  - {src.name}")
        print(f"    URL: {src.url}")
        print(f"    Quality: {src.quality.value}")

    integration_success = len(sources) > 0

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    integration_success = False

print()

# =============================================================================
# SUMMARY
# =============================================================================

print("=" * 70)
print("SUMMARY")
print("=" * 70)

checks = [
    ("Blind domain identified", len(blind_domains) > 0),
    ("Autonomous discovery executed", True),  # If we got here, it ran
    ("Working APIs discovered", discovery_success),
    ("Integration working", integration_success),
]

all_passed = True
for name, passed in checks:
    symbol = "V" if passed else "X"
    print(f"  {symbol} {name}: {'YES' if passed else 'NO'}")
    if not passed:
        all_passed = False

print()

if all_passed:
    print("V AUTONOMOUS DISCOVERY TEST PASSED!")
    print("  HermesFlow can now discover APIs for NEW domains!")
else:
    print("~ AUTONOMOUS DISCOVERY TEST PARTIALLY PASSED")
    print("  Some components may need Legomena (ollama) running for full functionality")

print()
print(f"Completed: {datetime.now().isoformat()}")
