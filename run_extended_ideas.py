#!/usr/bin/env python3
"""
EXTENDED IDEAS GENERATOR
========================

Takes the top discoveries from autonomous research and generates
4-5 extended/related research ideas from each, then runs them
through OlympusFlow for derivation.

Author: Carl Zimmerman
Date: May 6, 2026
"""

import os
import sys
import json
import math
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from OlympusFlow.autonomous_controller import AutonomousController, DerivationTarget

# Z² constant
Z_SQUARED = 32 * math.pi / 3  # ≈ 33.510...

# Top discoveries to extend (selected for physical significance)
TOP_DISCOVERIES = [
    # (name, value, formula, domain, why_interesting)
    ("fine_structure_inverse", 137.036, "4Z² + 3", "particle_physics",
     "Fundamental coupling constant - 4 dimensions + 3 generations?"),

    ("solar_constant", 1361, "41Z² - 13", "atmospheric",
     "41 = prime, 13 = generations? Energy flux at Earth"),

    ("greenhouse_emissivity", 0.612, "1 - 13/Z²", "atmospheric",
     "Planetary energy balance - 13 appears again"),

    ("neutron_lifetime", 879.4, "26Z² + 8", "nuclear_physics",
     "Beta decay timescale - fundamental nuclear physics"),

    ("critical_rayleigh", 1708, "50Z² + 32", "fluid_dynamics",
     "Onset of convection - 50 = 2×25, 32 = 2⁵"),

    ("magic_number_82", 82, "2Z² + 15", "nuclear_physics",
     "Nuclear shell closure - stability magic"),

    ("hubble_constant", 73.0, "2Z² + 6", "cosmology",
     "Universe expansion rate - 2 dimensions + 6 compactified?"),

    ("l_cone_wavelength", 564, "16Z² + 28", "optics",
     "Human color vision - 16 = 2⁴, 28 = 4×7"),

    ("water_bond_angle", 104.5, "3Z² + 4", "chemistry",
     "Most important molecule - 3 dimensions + 4 spacetime?"),

    ("rainbow_angle", 42, "2Z² - 25", "optics",
     "Light refraction geometry - Douglas Adams was right!"),

    ("dna_base_pairs", 10.5, "Z² - 23", "biology",
     "Genetic information carrier - fundamental life constant"),

    ("dunbar_number", 150, "4Z² + 16", "networks",
     "Social group size limit - cognitive constraint"),
]


def generate_extended_ideas(discovery: Tuple) -> List[Dict]:
    """
    Generate 4-5 extended research ideas from a discovery.

    For each discovery, we look for:
    1. Related constants in same domain
    2. Dimensional variations
    3. Ratio/product relationships
    4. Other domains with similar structure
    5. Inverse/complement relationships
    """
    name, value, formula, domain, reason = discovery
    ideas = []

    # Parse the formula to extract coefficients
    # Formats: "aZ² + b", "a + b/Z²", "aZ² - b", etc.
    a, b = 0, 0
    if "Z² +" in formula:
        parts = formula.replace(" ", "").split("Z²+")
        a = int(parts[0]) if parts[0] else 1
        b = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    elif "Z² -" in formula:
        parts = formula.replace(" ", "").split("Z²-")
        a = int(parts[0]) if parts[0] else 1
        b = -int(parts[1]) if len(parts) > 1 and parts[1] else 0
    elif "/Z²" in formula:
        # Handle 1 - 13/Z² type
        pass

    # Idea 1: Related constant (±1 from coefficient)
    if a != 0:
        related_val_1 = (a+1) * Z_SQUARED + b
        related_val_2 = (a-1) * Z_SQUARED + b if a > 1 else None
        ideas.append({
            "name": f"{name}_plus_one_z2",
            "value": related_val_1,
            "domain": domain,
            "reason": f"Adjacent to {name}: ({a+1})Z² + {b}",
            "priority": 0.7
        })
        if related_val_2:
            ideas.append({
                "name": f"{name}_minus_one_z2",
                "value": related_val_2,
                "domain": domain,
                "reason": f"Adjacent to {name}: ({a-1})Z² + {b}",
                "priority": 0.7
            })

    # Idea 2: Ratio relationship
    ideas.append({
        "name": f"{name}_ratio_pi",
        "value": value / math.pi,
        "domain": domain,
        "reason": f"{name}/π - looking for pure rational",
        "priority": 0.6
    })

    # Idea 3: Complement to unity/power
    ideas.append({
        "name": f"{name}_complement",
        "value": 1 - (1/value) if value > 1 else value,
        "domain": domain,
        "reason": f"Complement: 1 - 1/{name}",
        "priority": 0.5
    })

    # Idea 4: Cross-domain analog
    other_domains = ["particle_physics", "cosmology", "nuclear_physics",
                     "chemistry", "fluid_dynamics"]
    other_domain = [d for d in other_domains if d != domain][0]
    ideas.append({
        "name": f"{name}_cross_domain",
        "value": value,
        "domain": other_domain,
        "reason": f"Same value in {other_domain} domain",
        "priority": 0.4
    })

    # Idea 5: Dimensional analysis (square, square root)
    if value > 1:
        ideas.append({
            "name": f"{name}_sqrt",
            "value": math.sqrt(value),
            "domain": domain,
            "reason": f"√{name} - dimensional reduction",
            "priority": 0.5
        })

    return ideas[:5]  # Return top 5


def main():
    """Generate extended ideas and optionally run through OlympusFlow."""
    print("=" * 70)
    print("EXTENDED IDEAS GENERATOR")
    print("=" * 70)
    print(f"Time: {datetime.now().isoformat()}")
    print(f"Top discoveries: {len(TOP_DISCOVERIES)}")
    print()

    all_ideas = []

    for discovery in TOP_DISCOVERIES:
        name, value, formula, domain, reason = discovery
        print(f"\n{name} = {value} ({formula})")
        print(f"  Domain: {domain}")
        print(f"  Interest: {reason}")

        ideas = generate_extended_ideas(discovery)
        print(f"  Extended ideas: {len(ideas)}")
        for idea in ideas:
            print(f"    - {idea['name']}: {idea['value']:.4f} ({idea['domain']})")

        all_ideas.extend(ideas)

    print("\n" + "=" * 70)
    print(f"TOTAL EXTENDED IDEAS: {len(all_ideas)}")
    print("=" * 70)

    # Save ideas to JSON
    output_file = Path("OlympusFlow/discoveries/extended_ideas.json")
    with open(output_file, 'w') as f:
        json.dump({
            "generated": datetime.now().isoformat(),
            "source_discoveries": len(TOP_DISCOVERIES),
            "total_ideas": len(all_ideas),
            "ideas": all_ideas
        }, f, indent=2)
    print(f"\nSaved to: {output_file}")

    # Ask if user wants to run through pipeline
    print("\nTo run through OlympusFlow:")
    print("  python run_extended_ideas.py --run")

    if len(sys.argv) > 1 and sys.argv[1] == "--run":
        print("\n" + "=" * 70)
        print("RUNNING THROUGH OLYMPUSFLOW")
        print("=" * 70)

        # Create controller
        output_dir = Path("extended_ideas_results")
        output_dir.mkdir(exist_ok=True)

        controller = AutonomousController(output_dir=output_dir)

        # Add all ideas as targets
        for idea in all_ideas:
            target = DerivationTarget(
                constant_name=idea["name"],
                target_value=idea["value"],
                domain=idea["domain"],
                priority=idea["priority"]
            )
            controller.add_target(target)

        print(f"Added {len(all_ideas)} targets to queue")
        print("Running derivations...")

        # Run all
        controller.run_n(len(all_ideas))

        print("\n" + "=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"Processed: {controller.stats.total_targets_processed}")
        print(f"Successful: {controller.stats.successful_derivations}")
        print(f"First principles: {controller.stats.first_principles_found}")
        print(f"Numerology rejected: {controller.stats.numerology_rejected}")


if __name__ == "__main__":
    main()
