#!/usr/bin/env python3
"""
Z² DISCOVERY ENGINE - Simple Entry Point
==========================================

Ask a simple question, get full autonomous research.

Usage:
    python run_discovery.py "Eddington luminosity ratio"
    python run_discovery.py "Roche limit coefficient"
    python run_discovery.py "Titius-Bode law"
    python run_discovery.py "monarch butterfly navigation" --research  # Web research

The engine handles everything:
1. Research the topic → extract constants (via HermesFlow if --research)
2. BriareusFlow → brute-force pattern search
3. OlympusFlow → rigorous validation
4. Report findings

Author: Carl Zimmerman
Date: May 6, 2026
Updated: May 6, 2026 - Added HermesFlow integration via ResearchBridge
"""

import sys
import math
import asyncio
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

# Try to import HermesFlow ResearchBridge for web research
try:
    from HermesFlow.research_bridge import (
        ResearchBridge,
        DomainRegistry,
        run_automated_discovery,
        HERMES_AVAILABLE
    )
    RESEARCH_BRIDGE_AVAILABLE = True
except ImportError:
    RESEARCH_BRIDGE_AVAILABLE = False
    HERMES_AVAILABLE = False


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
    },
    "river-network": {
        "description": "River network scaling laws - Hack's law, Horton's laws, fractal geometry",
        "constants": [
            # Hack's Law: L = C * A^h
            {"name": "Hack exponent h (original)", "value": 0.6, "uncertainty": 0.02, "source": "Hack 1957"},
            {"name": "Hack exponent h (mean)", "value": 0.57, "uncertainty": 0.02, "source": "Global average"},
            {"name": "Hack exponent h (Mueller)", "value": 0.55, "uncertainty": 0.02, "source": "Mueller large basins"},
            {"name": "Hack exponent h (theoretical)", "value": 0.568, "uncertainty": 0.01, "source": "Percolation theory"},
            # Horton's Bifurcation Ratio R_B
            {"name": "Bifurcation ratio R_B (mean)", "value": 4.0, "uncertainty": 0.5, "source": "Horton's law"},
            {"name": "Bifurcation ratio R_B (min)", "value": 3.0, "uncertainty": 0.2, "source": "Horton's law"},
            {"name": "Bifurcation ratio R_B (max)", "value": 5.0, "uncertainty": 0.2, "source": "Horton's law"},
            {"name": "Bifurcation ratio R_B (random)", "value": 3.618, "uncertainty": 0.1, "source": "Random network theory"},
            # Horton's Length Ratio R_L
            {"name": "Length ratio R_L", "value": 2.0, "uncertainty": 0.3, "source": "Horton's law"},
            {"name": "Length ratio R_L (typical)", "value": 2.3, "uncertainty": 0.3, "source": "Empirical"},
            # Horton's Area Ratio R_A
            {"name": "Area ratio R_A", "value": 4.5, "uncertainty": 0.5, "source": "Horton's law"},
            # Fractal Dimensions
            {"name": "Fractal dimension D_T (min)", "value": 1.7, "uncertainty": 0.05, "source": "Tokunaga networks"},
            {"name": "Fractal dimension D_T (max)", "value": 1.8, "uncertainty": 0.05, "source": "Tokunaga networks"},
            {"name": "Fractal dimension D_T (mean)", "value": 1.75, "uncertainty": 0.05, "source": "River networks"},
            {"name": "Stream branch fractal", "value": 1.84, "uncertainty": 0.05, "source": "Measured"},
            # Drainage density exponents
            {"name": "Drainage density fractal", "value": 0.71, "uncertainty": 0.05, "source": "Measured"},
            # Dimensionless ratios
            {"name": "h × 2 (Hack doubled)", "value": 1.14, "uncertainty": 0.04, "source": "Computed"},
            {"name": "R_B / R_L (ratio of ratios)", "value": 4.0/2.0, "uncertainty": 0.2, "source": "Computed"},
            {"name": "ln(R_B)/ln(R_L) (fractal)", "value": math.log(4)/math.log(2), "uncertainty": 0.1, "source": "Fractal dimension"},
        ]
    },
    "turbulence": {
        "description": "Turbulence constants - empirically observed, no first-principles derivation",
        "constants": [
            # von Kármán constant
            {"name": "von Kármán κ", "value": 0.41, "uncertainty": 0.01, "source": "Turbulent boundary layers"},
            {"name": "von Kármán κ (Bailey 2014)", "value": 0.40, "uncertainty": 0.02, "source": "Bailey et al 2014"},
            {"name": "von Kármán κ (Nagib)", "value": 0.384, "uncertainty": 0.01, "source": "Nagib & Chauhan 2008"},
            # Strouhal number
            {"name": "Strouhal St (cylinder)", "value": 0.21, "uncertainty": 0.01, "source": "Vortex shedding"},
            {"name": "Strouhal St (universal)", "value": 0.20, "uncertainty": 0.01, "source": "Bluff bodies"},
            {"name": "Strouhal St* (wake)", "value": 0.178, "uncertainty": 0.01, "source": "Roshko 1954"},
            # Critical Reynolds numbers
            {"name": "Re_crit (pipe)", "value": 2300, "uncertainty": 100, "source": "Pipe flow transition"},
            {"name": "Re_crit (Schiller)", "value": 2320, "uncertainty": 50, "source": "Schiller lower critical"},
            {"name": "Re_crit (theoretical)", "value": 1840, "uncertainty": 50, "source": "Axisymmetric stability"},
            {"name": "Re_crit (flat plate)", "value": 500000, "uncertainty": 50000, "source": "Boundary layer transition"},
            # Kolmogorov constants
            {"name": "Kolmogorov C_K", "value": 1.5, "uncertainty": 0.1, "source": "Energy spectrum"},
            {"name": "Kolmogorov C_2", "value": 2.0, "uncertainty": 0.1, "source": "Structure function"},
            # Turbulence exponents
            {"name": "Kolmogorov -5/3 exponent", "value": -5/3, "uncertainty": 0.01, "source": "Inertial range"},
            {"name": "Richardson 4/3 exponent", "value": 4/3, "uncertainty": 0.01, "source": "Eddy diffusion"},
            # Other empirical constants
            {"name": "Sphere drag C_d", "value": 0.47, "uncertainty": 0.02, "source": "Sphere at Re>1000"},
            {"name": "Critical Weber We_crit", "value": 12, "uncertainty": 1, "source": "Droplet breakup"},
            {"name": "Smagorinsky C_s", "value": 0.17, "uncertainty": 0.02, "source": "LES modeling"},
            # Dimensionless ratios
            {"name": "1/κ (log law slope)", "value": 1/0.41, "uncertainty": 0.05, "source": "Wall law"},
            {"name": "κ²", "value": 0.41**2, "uncertainty": 0.01, "source": "Squared von Kármán"},
        ]
    },
    "snowflake": {
        "description": "Snowflake and ice crystal structure (Ice Ih)",
        "constants": [
            # Exact geometric values
            {"name": "Hexagonal arm angle", "value": 60.0, "uncertainty": 0.0001, "source": "Hexagonal symmetry"},
            {"name": "Internal hexagon angle", "value": 120.0, "uncertainty": 0.0001, "source": "Hexagonal symmetry"},
            {"name": "Tetrahedral angle arccos(-1/3)", "value": math.degrees(math.acos(-1/3)), "uncertainty": 0.0001, "source": "Exact geometry"},
            {"name": "-cos(tetrahedral) = 1/3", "value": 1/3, "uncertainty": 0.0001, "source": "Exact"},
            {"name": "Number of arms", "value": 6, "uncertainty": 0.0001, "source": "Hexagonal symmetry"},
            # Bond angles
            {"name": "H-O-H angle in ice", "value": 109.47, "uncertainty": 0.01, "source": "Ice Ih structure"},
            {"name": "H-O-H angle in water", "value": 104.5, "uncertainty": 0.1, "source": "Liquid water"},
            {"name": "Water/ice angle ratio", "value": 104.5/109.47, "uncertainty": 0.001, "source": "Computed"},
            # Bond lengths (Angstroms)
            {"name": "O-O hydrogen bond", "value": 2.76, "uncertainty": 0.01, "source": "Ice Ih neutron diffraction"},
            {"name": "O-H covalent bond", "value": 1.01, "uncertainty": 0.01, "source": "Ice Ih structure"},
            {"name": "O-H/O-O bond ratio", "value": 1.01/2.76, "uncertainty": 0.005, "source": "Computed"},
            # Density
            {"name": "Ice Ih density", "value": 0.917, "uncertainty": 0.001, "source": "Ice physics"},
            {"name": "Ice/water density ratio", "value": 0.917, "uncertainty": 0.001, "source": "Ice physics"},
            # Lattice spacings
            {"name": "Interlayer spacing (nm)", "value": 0.276, "uncertainty": 0.001, "source": "Ice Ih crystallography"},
            {"name": "Inter-plane spacing (nm)", "value": 0.0923, "uncertainty": 0.001, "source": "Ice Ih crystallography"},
            {"name": "Plane/layer spacing ratio", "value": 0.0923/0.276, "uncertainty": 0.005, "source": "Computed"},
            # Dimensionless angles as fractions of circle
            {"name": "60°/360° = 1/6", "value": 1/6, "uncertainty": 0.0001, "source": "Hexagonal fraction"},
            {"name": "120°/360° = 1/3", "value": 1/3, "uncertainty": 0.0001, "source": "Hexagonal fraction"},
            {"name": "Tetrahedral/360°", "value": math.degrees(math.acos(-1/3))/360, "uncertainty": 0.0001, "source": "Computed"},
        ]
    },
    "earthquake-aftershock": {
        "description": "Earthquake aftershock decay - Omori's law, Båth's law, Gutenberg-Richter",
        "constants": [
            # Omori's Law: n(t) = K / (c + t)^p
            {"name": "Omori p-value (universal)", "value": 1.0, "uncertainty": 0.1, "source": "Omori 1894"},
            {"name": "Omori p-value (California)", "value": 1.22, "uncertainty": 0.03, "source": "California sequences"},
            {"name": "Omori p-value (Morocco 2023)", "value": 1.56, "uncertainty": 0.02, "source": "Morocco earthquake study"},
            {"name": "Omori p-value (global mean)", "value": 1.1, "uncertainty": 0.1, "source": "Global average"},
            {"name": "Omori c (time delay)", "value": 0.02, "uncertainty": 0.01, "source": "Days, typical"},
            # Båth's Law: ΔM = M_mainshock - M_largest_aftershock
            {"name": "Båth law ΔM", "value": 1.2, "uncertainty": 0.1, "source": "Båth 1965"},
            {"name": "Båth law (precise)", "value": 1.18, "uncertainty": 0.05, "source": "Global catalog"},
            # Gutenberg-Richter Law: log₁₀(N) = a - b*M
            {"name": "Gutenberg-Richter b-value", "value": 1.0, "uncertainty": 0.05, "source": "Gutenberg-Richter"},
            {"name": "G-R b-value (global)", "value": 0.95, "uncertainty": 0.05, "source": "Global seismicity"},
            {"name": "G-R b-value (subduction)", "value": 0.85, "uncertainty": 0.1, "source": "Subduction zones"},
            {"name": "G-R b-value (volcanic)", "value": 1.3, "uncertainty": 0.1, "source": "Volcanic regions"},
            # Energy-magnitude relationship: log₁₀(E) = 1.5*M + 4.8
            {"name": "Energy-magnitude factor", "value": 1.5, "uncertainty": 0.01, "source": "Kanamori 1977"},
            {"name": "Energy constant 4.8", "value": 4.8, "uncertainty": 0.1, "source": "Joules convention"},
            # Aftershock productivity: log₁₀(N) = α*M + β
            {"name": "Aftershock productivity α", "value": 1.0, "uncertainty": 0.1, "source": "Felzer et al"},
            {"name": "Aftershock zone L/rupture", "value": 1.5, "uncertainty": 0.2, "source": "Rupture scaling"},
            # Dimensionless ratios
            {"name": "10^(ΔM) energy ratio", "value": 10**1.2, "uncertainty": 1, "source": "Computed from Båth"},
            {"name": "Energy ratio 10^(1.5)", "value": 10**1.5, "uncertainty": 0.5, "source": "Per magnitude step"},
            {"name": "Omori p - 1 (departure)", "value": 0.1, "uncertainty": 0.1, "source": "Deviation from unity"},
            {"name": "b/p ratio", "value": 1.0/1.1, "uncertainty": 0.05, "source": "Scaling connection"},
        ]
    },
    "kleiber": {
        "description": "Kleiber's law metabolic scaling - quarter-power biology",
        "constants": [
            # Kleiber's Law: B ∝ M^α where α ≈ 3/4
            {"name": "Kleiber exponent (observed)", "value": 0.75, "uncertainty": 0.01, "source": "Kleiber 1932"},
            {"name": "Kleiber exponent (mammals)", "value": 0.74, "uncertainty": 0.02, "source": "Mammalian data"},
            {"name": "Kleiber exponent (birds)", "value": 0.72, "uncertainty": 0.02, "source": "Avian data"},
            {"name": "Kleiber exponent (fish)", "value": 0.79, "uncertainty": 0.03, "source": "Fish metabolic data"},
            {"name": "Kleiber exponent (plants)", "value": 0.75, "uncertainty": 0.02, "source": "Plant growth"},
            # West-Brown-Enquist theoretical derivation
            {"name": "WBE theoretical 3/4", "value": 3/4, "uncertainty": 0.001, "source": "West-Brown-Enquist 1997"},
            # Related quarter-power scaling laws
            {"name": "Heart rate exponent", "value": -0.25, "uncertainty": 0.01, "source": "Heart rate ~ M^-1/4"},
            {"name": "Lifespan exponent", "value": 0.25, "uncertainty": 0.02, "source": "Lifespan ~ M^1/4"},
            {"name": "Circulation time exp", "value": 0.25, "uncertainty": 0.01, "source": "Blood circuit time"},
            {"name": "Aorta radius exponent", "value": 0.375, "uncertainty": 0.01, "source": "Aorta ~ M^3/8"},
            # Surface area scaling (alternative theory)
            {"name": "Surface area exponent", "value": 2/3, "uncertainty": 0.01, "source": "Rubner isometry"},
            {"name": "Rubner 2/3 law", "value": 0.667, "uncertainty": 0.01, "source": "Rubner 1883"},
            # Dimensionless ratios
            {"name": "3/4 exact", "value": 0.75, "uncertainty": 0.0001, "source": "Quarter-power exact"},
            {"name": "1/4 exact", "value": 0.25, "uncertainty": 0.0001, "source": "Quarter-power exact"},
            {"name": "3/8 exact", "value": 0.375, "uncertainty": 0.0001, "source": "Eighth-power exact"},
            {"name": "Kleiber/Rubner ratio", "value": 0.75/0.667, "uncertainty": 0.01, "source": "Computed"},
            {"name": "4 × Kleiber exp", "value": 3.0, "uncertainty": 0.01, "source": "Dimensionality"},
            {"name": "1 - Kleiber exp", "value": 0.25, "uncertainty": 0.01, "source": "Complementary"},
            {"name": "Kleiber exp squared", "value": 0.5625, "uncertainty": 0.01, "source": "Computed"},
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
    if "snowflake" in query_lower or "ice crystal" in query_lower or "ice ih" in query_lower:
        return "snowflake"
    if "turbulence" in query_lower or "karman" in query_lower or "kármán" in query_lower or "strouhal" in query_lower or "reynolds" in query_lower:
        return "turbulence"
    if "river" in query_lower or "hack" in query_lower or "horton" in query_lower or "drainage" in query_lower or "stream" in query_lower or "bifurcation" in query_lower:
        return "river-network"
    if "earthquake" in query_lower or "aftershock" in query_lower or "omori" in query_lower or "seism" in query_lower or "gutenberg" in query_lower or "richter" in query_lower or "båth" in query_lower or "bath" in query_lower:
        return "earthquake-aftershock"
    if "kleiber" in query_lower or "metabolic" in query_lower or "allometric" in query_lower or "quarter-power" in query_lower or "3/4 law" in query_lower:
        return "kleiber"

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


async def run_web_research(query: str, verbose: bool = True, timeout: float = 60) -> Dict[str, Any]:
    """
    Run discovery with web research via HermesFlow ResearchBridge.

    This is used for topics not in the hardcoded TOPIC_KNOWLEDGE.
    It uses HermesFlow web tools to search for scientific data.

    Args:
        query: Topic to research
        verbose: Print progress
        timeout: Search timeout

    Returns:
        Full results dict
    """
    if not RESEARCH_BRIDGE_AVAILABLE:
        print("Error: HermesFlow ResearchBridge not available")
        print("Install HermesFlow or use a known topic from TOPIC_KNOWLEDGE")
        return {"error": "ResearchBridge not available"}

    # Use the automated discovery pipeline
    return await run_automated_discovery(query, timeout=timeout, verbose=verbose)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Z² Discovery Engine")
    parser.add_argument("query", nargs="?", default="Eddington luminosity ratio",
                        help="Topic to research (e.g., 'Eddington luminosity ratio')")
    parser.add_argument("--timeout", type=float, default=60, help="Search timeout")
    parser.add_argument("--quiet", action="store_true", help="Less output")
    parser.add_argument("--research", action="store_true",
                        help="Use HermesFlow web research for unknown topics")

    args = parser.parse_args()

    # Check if topic is in knowledge base
    topic = find_topic(args.query)

    if topic:
        # Use hardcoded knowledge base
        run_discovery(args.query, verbose=not args.quiet, timeout=args.timeout)
    elif args.research and RESEARCH_BRIDGE_AVAILABLE:
        # Use web research
        print(f"Topic not in knowledge base, using HermesFlow web research...")
        asyncio.run(run_web_research(args.query, verbose=not args.quiet, timeout=args.timeout))
    else:
        print(f"Unknown topic: {args.query}")
        print(f"Available topics: {list(TOPIC_KNOWLEDGE.keys())}")
        if RESEARCH_BRIDGE_AVAILABLE:
            print(f"\nTip: Use --research to search the web for unknown topics")
        else:
            print(f"\nNote: Install HermesFlow to enable web research for unknown topics")
