#!/usr/bin/env python3
"""
Z² DISCOVERY ENGINE - Simple Entry Point
==========================================

Ask a simple question, get full autonomous research.

Usage:
    python run_discovery.py "Eddington luminosity ratio"
    python run_discovery.py "Roche limit coefficient"
    python run_discovery.py "Titius-Bode law"

The engine handles everything:
1. Research the topic → extract constants
2. BriareusFlow → brute-force pattern search
3. OlympusFlow → rigorous validation
4. Report findings

Author: Carl Zimmerman
Date: May 6, 2026
"""

import sys
import math
import argparse
from typing import List, Dict, Any
from dataclasses import dataclass

from BriareusFlow import (
    BriareusController,
    SearchConfig,
    SearchTarget,
    SearchPriority,
    OlympusBridge,
    integrate_with_olympusflow,
    Z_SQUARED,
    Z
)


# =============================================================================
# KNOWLEDGE BASE - Known constants by topic
# =============================================================================

TOPIC_KNOWLEDGE = {
    "eddington": {
        "description": "Eddington luminosity and stellar radiation limits",
        "constants": [
            {"name": "Thomson coefficient (8π/3)", "value": 8*math.pi/3, "uncertainty": 0.0001, "source": "QED exact"},
            {"name": "Schwarzschild ISCO E/mc²", "value": 2*math.sqrt(2)/3, "uncertainty": 0.0001, "source": "GR exact"},
            {"name": "Schwarzschild efficiency η", "value": 1 - 2*math.sqrt(2)/3, "uncertainty": 0.0001, "source": "GR exact"},
            {"name": "Extreme Kerr efficiency η", "value": 1 - 1/math.sqrt(3), "uncertainty": 0.0001, "source": "GR exact"},
            {"name": "Lane-Emden ξ₁ (n=3)", "value": 6.8968, "uncertainty": 0.0001, "source": "Polytrope theory"},
            {"name": "Lane-Emden ω₃", "value": 2.01824, "uncertainty": 0.0001, "source": "Polytrope theory"},
            {"name": "Bondi coefficient (4π)", "value": 4*math.pi, "uncertainty": 0.0001, "source": "Hydrodynamics"},
            {"name": "Mass-luminosity exponent", "value": 3.5, "uncertainty": 0.1, "source": "Stellar observations"},
        ]
    },
    "roche": {
        "description": "Roche limit - tidal disruption of satellites",
        "constants": [
            {"name": "Roche limit coefficient (rigid)", "value": 1.26, "uncertainty": 0.01, "source": "Celestial mechanics"},
            {"name": "Roche limit coefficient (fluid)", "value": 2.44, "uncertainty": 0.01, "source": "Celestial mechanics"},
            {"name": "Roche lobe L1 coefficient", "value": 0.49, "uncertainty": 0.01, "source": "Binary star theory"},
            {"name": "Roche lobe volume coefficient", "value": 0.38, "uncertainty": 0.01, "source": "Binary star theory"},
            {"name": "Mass ratio critical q", "value": 0.0256, "uncertainty": 0.001, "source": "Roche geometry"},
            {"name": "Darwin instability ratio", "value": 3.0, "uncertainty": 0.1, "source": "Tidal theory"},
        ]
    },
    "titius-bode": {
        "description": "Titius-Bode law of planetary spacing",
        "constants": [
            {"name": "Titius-Bode base (0.4 AU)", "value": 0.4, "uncertainty": 0.01, "source": "Empirical"},
            {"name": "Titius-Bode ratio", "value": 2.0, "uncertainty": 0.1, "source": "Empirical"},
            {"name": "Titius-Bode offset (0.3)", "value": 0.3, "uncertainty": 0.01, "source": "Empirical"},
            {"name": "Mercury period ratio", "value": 0.387, "uncertainty": 0.001, "source": "Orbital mechanics"},
            {"name": "Venus/Earth period ratio", "value": 0.615, "uncertainty": 0.001, "source": "Orbital mechanics"},
            {"name": "Mars/Earth period ratio", "value": 1.524, "uncertainty": 0.001, "source": "Orbital mechanics"},
            {"name": "Jupiter/Saturn resonance", "value": 2.48, "uncertainty": 0.01, "source": "Orbital mechanics"},
            {"name": "Kirkwood gap 3:1", "value": 2.5, "uncertainty": 0.01, "source": "Asteroid belt"},
        ]
    },
    "geodynamo": {
        "description": "Earth's magnetic field generation",
        "constants": [
            {"name": "Critical magnetic Reynolds Rm", "value": 40, "uncertainty": 10, "source": "Dynamo theory"},
            {"name": "Elsasser number Λ", "value": 1.0, "uncertainty": 0.1, "source": "Geophysics"},
            {"name": "Earth dipole tilt", "value": 11.5, "uncertainty": 0.1, "source": "Geomagnetic data"},
            {"name": "Secular variation rate", "value": 0.05, "uncertainty": 0.01, "source": "Geomagnetic data"},
            {"name": "Core-mantle boundary ratio", "value": 0.546, "uncertainty": 0.001, "source": "Seismology"},
            {"name": "Inner/outer core ratio", "value": 0.351, "uncertainty": 0.001, "source": "Seismology"},
        ]
    },
    "golden": {
        "description": "Golden ratio and related constants",
        "constants": [
            {"name": "Golden ratio φ", "value": (1+math.sqrt(5))/2, "uncertainty": 0.0001, "source": "Mathematics"},
            {"name": "1/φ", "value": 2/(1+math.sqrt(5)), "uncertainty": 0.0001, "source": "Mathematics"},
            {"name": "φ²", "value": ((1+math.sqrt(5))/2)**2, "uncertainty": 0.0001, "source": "Mathematics"},
            {"name": "ln(φ)", "value": math.log((1+math.sqrt(5))/2), "uncertainty": 0.0001, "source": "Mathematics"},
        ]
    }
}


def find_topic(query: str) -> str:
    """Match query to known topic."""
    query_lower = query.lower()

    # Direct matches
    if "eddington" in query_lower or "luminosity" in query_lower or "stellar" in query_lower:
        return "eddington"
    if "roche" in query_lower or "tidal" in query_lower:
        return "roche"
    if "titius" in query_lower or "bode" in query_lower or "planetary" in query_lower:
        return "titius-bode"
    if "geodynamo" in query_lower or "magnetic reynolds" in query_lower or "dynamo" in query_lower:
        return "geodynamo"
    if "golden" in query_lower or "fibonacci" in query_lower:
        return "golden"

    # Default to eddington for astrophysics queries
    if any(w in query_lower for w in ["black hole", "accretion", "thomson", "kerr"]):
        return "eddington"

    return None


def run_discovery(query: str, verbose: bool = True, timeout: float = 60) -> Dict[str, Any]:
    """
    Run full discovery pipeline on a simple query.

    Args:
        query: Natural language question (e.g., "Eddington luminosity ratio")
        verbose: Print progress
        timeout: Search timeout in seconds

    Returns:
        Full results dict
    """
    print("=" * 70)
    print("Z² DISCOVERY ENGINE")
    print("=" * 70)
    print(f"\nQuery: {query}")
    print()

    # 1. Find relevant topic
    topic = find_topic(query)
    if not topic:
        print(f"Unknown topic. Available: {list(TOPIC_KNOWLEDGE.keys())}")
        return {"error": "Unknown topic"}

    topic_data = TOPIC_KNOWLEDGE[topic]
    print(f"Topic: {topic}")
    print(f"Description: {topic_data['description']}")
    print(f"Constants to search: {len(topic_data['constants'])}")
    print()

    # 2. Build search targets
    targets = []
    for const in topic_data["constants"]:
        target = SearchTarget(
            target_id=const["name"].replace(" ", "_").replace("/", "_"),
            name=const["name"],
            value=const["value"],
            uncertainty=const["uncertainty"],
            source=const["source"],
            domain=topic,
            priority=SearchPriority.HIGH
        )
        targets.append(target)
        if verbose:
            print(f"  {const['name']:40} = {const['value']:.6f}")

    print()

    # 3. Run BriareusFlow
    print("-" * 70)
    print("PHASE 1: BriareusFlow Brute-Force Search")
    print("-" * 70)

    config = SearchConfig(
        max_error_percent=1.0,
        max_integer=50,
        max_denominator=50,
        num_threads=8,
        verbose=verbose,
        log_every_n=2
    )

    controller = BriareusController(config)
    controller.add_targets(targets)

    briareus_result = controller.run(timeout=timeout)

    print(f"\nBriareusFlow complete:")
    print(f"  Targets processed: {briareus_result.targets_processed}")
    print(f"  Total findings: {briareus_result.findings_total}")
    print(f"  Z² patterns: {briareus_result.z2_patterns_found}")
    print(f"  Runtime: {briareus_result.runtime_seconds:.1f}s")

    # 4. Get Z² findings
    z2_findings = controller.get_z2_findings()
    promising = controller.get_promising_findings()

    # 5. Integrate with OlympusFlow
    print()
    print("-" * 70)
    print("PHASE 2: OlympusFlow Integration")
    print("-" * 70)

    integration = integrate_with_olympusflow(briareus_result)
    print(f"  Promoted to OlympusFlow: {integration['summary']['promoted']}")
    print(f"  Z² candidates: {integration['summary']['z2_candidates']}")

    # 6. Report results
    print()
    print("=" * 70)
    print("DISCOVERY RESULTS")
    print("=" * 70)

    # Group findings by target
    by_target = {}
    for f in controller.all_findings:
        if f.name not in by_target:
            by_target[f.name] = []
        by_target[f.name].append(f)

    print("\nBEST MATCHES PER CONSTANT:")
    print("-" * 70)

    for target_name, findings in sorted(by_target.items()):
        best = min(findings, key=lambda x: x.percent_error)
        z2_marker = " [Z²]" if "Z²" in best.formula or "Z^2" in best.formula else ""
        pi_marker = " [π]" if "π" in best.formula else ""

        print(f"\n{target_name}")
        print(f"  Experimental: {best.experimental_value:.6f}")
        print(f"  Best match:   {best.formula} = {best.computed_value:.6f}{z2_marker}{pi_marker}")
        print(f"  Error:        {best.percent_error:.4f}%")

        # Show alternatives
        alts = sorted(findings, key=lambda x: x.percent_error)[1:4]
        if alts:
            print(f"  Alternatives: ", end="")
            print(", ".join(f"{a.formula}" for a in alts))

    # Z² specific findings
    if z2_findings:
        print()
        print("-" * 70)
        print("Z² PATTERN DISCOVERIES")
        print("-" * 70)
        for f in z2_findings[:10]:
            print(f"  {f.name}: {f.formula} = {f.computed_value:.6f} ({f.percent_error:.4f}%)")

    # Check for Z² connections
    print()
    print("-" * 70)
    print("Z² CONNECTION ANALYSIS")
    print("-" * 70)
    print(f"Z² = 32π/3 ≈ {Z_SQUARED:.6f}")
    print(f"Z = √(32π/3) ≈ {Z:.6f}")

    # Look for interesting ratios with Z²
    for target_name, findings in by_target.items():
        best = min(findings, key=lambda x: x.percent_error)
        value = best.experimental_value

        # Check ratio with Z²
        ratio = value / Z_SQUARED if value > 1 else Z_SQUARED / value
        inv_ratio = Z_SQUARED / value if value > 1 else value / Z_SQUARED

        # Check if ratio is close to a simple fraction
        for a in range(1, 20):
            for b in range(1, 20):
                if abs(ratio - a/b) / ratio < 0.01:
                    print(f"  {target_name}: value × {b}/{a} ≈ Z²")
                if abs(inv_ratio - a/b) / inv_ratio < 0.01:
                    print(f"  {target_name}: Z² × {b}/{a} ≈ value")

    print()
    print("=" * 70)
    print("DISCOVERY COMPLETE")
    print("=" * 70)

    return {
        "query": query,
        "topic": topic,
        "briareus_result": briareus_result,
        "z2_findings": z2_findings,
        "promising_findings": promising,
        "olympus_integration": integration,
        "by_target": by_target
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Z² Discovery Engine")
    parser.add_argument("query", nargs="?", default="Eddington luminosity ratio",
                        help="Topic to research (e.g., 'Eddington luminosity ratio')")
    parser.add_argument("--timeout", type=float, default=60, help="Search timeout")
    parser.add_argument("--quiet", action="store_true", help="Less output")

    args = parser.parse_args()

    run_discovery(args.query, verbose=not args.quiet, timeout=args.timeout)
