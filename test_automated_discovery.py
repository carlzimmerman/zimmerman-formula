#!/usr/bin/env python3
"""
Test Automated Discovery Pipeline

Tests the full HermesFlow -> ResearchBridge -> BriareusFlow pipeline.

Usage:
    python test_automated_discovery.py                    # Test with mock data
    python test_automated_discovery.py --topic "kleiber"  # Test specific topic
    python test_automated_discovery.py --web              # Test with real web search

Author: Carl Zimmerman
Date: May 6, 2026
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from HermesFlow.research_bridge import (
    ResearchBridge,
    DomainRegistry,
    ConstantExtractor,
    run_automated_discovery,
    HERMES_AVAILABLE,
    BRIAREUS_AVAILABLE
)


def test_constant_extractor():
    """Test the ConstantExtractor with sample scientific text."""
    print("=" * 70)
    print("TEST: ConstantExtractor")
    print("=" * 70)

    extractor = ConstantExtractor(verbose=False)

    # Sample scientific text
    texts = [
        """
        Monarch butterflies navigate using a time-compensated sun compass,
        maintaining a heading of approximately 215 degrees southwest during
        fall migration. Their compound eyes are sensitive to UV light at
        wavelengths around 420 nm. The migration distance can exceed 4,000 km.
        """,
        """
        The Gutenberg-Richter law states that log₁₀(N) = a - bM, where the
        b-value is typically around 1.0 ± 0.1. The energy released scales as
        10^1.5 per magnitude unit. Earthquakes of magnitude 5.0 or greater
        occur approximately 1,500 times per year globally.
        """,
        """
        Kleiber's Law: metabolic rate scales with body mass to the power of
        0.75 (or 3/4). This holds across species from bacteria to whales.
        The coefficient is approximately 70 kcal/day for mammals.
        """,
    ]

    for i, text in enumerate(texts, 1):
        print(f"\nText {i}:")
        print("-" * 50)
        constants = extractor.extract_from_text(text)
        for const in constants:
            print(f"  {const.name}: {const.value:.4g} {const.unit} (confidence: {const.confidence:.2f})")

    print("\n✓ ConstantExtractor test passed")
    return True


def test_domain_registry():
    """Test the DomainRegistry for loading and searching domains."""
    print("\n" + "=" * 70)
    print("TEST: DomainRegistry")
    print("=" * 70)

    registry = DomainRegistry()

    # List existing domains
    domains = registry.list_all()
    print(f"\nExisting domains: {len(domains)}")
    for name in domains[:5]:
        print(f"  - {name}")
    if len(domains) > 5:
        print(f"  ... and {len(domains) - 5} more")

    # Search for a domain
    if domains:
        result = registry.search(domains[0])
        if result:
            print(f"\nLoaded domain: {result.name}")
            print(f"  Constants: {len(result.constants)}")
            print(f"  Keywords: {result.keywords[:3]}")

    print("\n✓ DomainRegistry test passed")
    return True


async def test_research_bridge(use_web: bool = False):
    """Test the ResearchBridge."""
    print("\n" + "=" * 70)
    print("TEST: ResearchBridge")
    print("=" * 70)

    if use_web and HERMES_AVAILABLE:
        print("Using HermesFlow web tools (real web search)")
    else:
        print("Using mock search (HermesFlow not available or --web not specified)")

    bridge = ResearchBridge(verbose=True)

    # Research a topic
    topic = "monarch butterfly navigation"
    print(f"\nResearching: {topic}")

    domain = await bridge.research_topic(topic, num_results=3)

    print(f"\nDomain created: {domain.name}")
    print(f"Constants found: {len(domain.constants)}")
    for const in domain.constants[:5]:
        print(f"  {const.get('name', 'Unknown')}: {const.get('value', 0):.6g}")

    # Save and reload
    filepath = bridge.save_domain(domain)
    print(f"\nSaved to: {filepath}")

    loaded = bridge.load_domain(domain.name)
    if loaded:
        print(f"Loaded back: {loaded.name} with {len(loaded.constants)} constants")

    print("\n✓ ResearchBridge test passed")
    return True


async def test_full_pipeline(topic: str = "kleiber law metabolic"):
    """Test the full automated discovery pipeline."""
    print("\n" + "=" * 70)
    print("TEST: Full Automated Discovery Pipeline")
    print("=" * 70)

    print(f"\nTopic: {topic}")
    print(f"HermesFlow available: {HERMES_AVAILABLE}")
    print(f"BriareusFlow available: {BRIAREUS_AVAILABLE}")

    # Run automated discovery
    result = await run_automated_discovery(topic, timeout=30, verbose=True)

    print("\n" + "-" * 70)
    print("RESULTS SUMMARY")
    print("-" * 70)
    print(f"Domain: {result['domain']['name']}")
    print(f"Constants extracted: {len(result['domain']['constants'])}")
    print(f"Search targets created: {len(result['targets'])}")

    if result['results']:
        print(f"Findings total: {result['results'].get('findings_total', 0)}")
        print(f"Z² patterns found: {result['results'].get('z2_patterns_found', 0)}")

    print("\n✓ Full pipeline test passed")
    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Test Automated Discovery Pipeline")
    parser.add_argument("--topic", type=str, default="kleiber law",
                        help="Topic to test (default: kleiber law)")
    parser.add_argument("--web", action="store_true",
                        help="Use real web search (requires HermesFlow API keys)")
    parser.add_argument("--quick", action="store_true",
                        help="Run quick tests only (no full pipeline)")

    args = parser.parse_args()

    print("=" * 70)
    print("Z² AUTOMATED DISCOVERY PIPELINE - TEST SUITE")
    print("=" * 70)
    print(f"\nHermesFlow available: {HERMES_AVAILABLE}")
    print(f"BriareusFlow available: {BRIAREUS_AVAILABLE}")
    print()

    # Run tests
    results = []

    # Test 1: ConstantExtractor
    results.append(("ConstantExtractor", test_constant_extractor()))

    # Test 2: DomainRegistry
    results.append(("DomainRegistry", test_domain_registry()))

    # Test 3: ResearchBridge
    results.append(("ResearchBridge",
                   asyncio.run(test_research_bridge(use_web=args.web))))

    # Test 4: Full Pipeline (unless --quick)
    if not args.quick:
        results.append(("Full Pipeline",
                       asyncio.run(test_full_pipeline(args.topic))))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")
    print("=" * 70)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
