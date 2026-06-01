#!/usr/bin/env python3
"""
================================================================================
THE DECISIVE TEST: Galena (PbS) vs Pyrite (FeS₂)
================================================================================

This is the key experiment that could validate or falsify Z² abiogenesis.

SETUP:
  - Galena (PbS):  a = 5.94 Å  → 2.6% from Z = 5.79 Å (CLOSER)
  - Pyrite (FeS₂): a = 5.417 Å → 6.8% from Z = 5.79 Å (FARTHER)

PREDICTION IF Z² GEOMETRY MATTERS:
  Galena should be as good or BETTER than Pyrite for prebiotic catalysis
  because it's geometrically closer to the "ideal" Z spacing.

PREDICTION IF CHEMISTRY MATTERS:
  Pyrite should be MUCH BETTER than Galena because:
  - Fe²⁺/Fe³⁺ is redox-active (can transfer electrons)
  - Pb²⁺ is NOT redox-active (6s² inert pair effect)
  - Iron-sulfur clusters are ubiquitous in biology
  - Lead is toxic to all life

This script computes electronic and structural properties to predict outcomes.

Author: Carl Zimmerman + Claude
License: AGPL-3.0-or-later
================================================================================
"""

import numpy as np
from typing import Dict, List, Tuple
import json
import os

try:
    from pyscf import gto, scf, dft
    PYSCF_AVAILABLE = True
except ImportError:
    PYSCF_AVAILABLE = False

# Z² Constants
Z_CONSTANT = 2 * np.sqrt(8 * np.pi / 3)  # 5.7888 Å

# Mineral data
MINERALS = {
    'Galena (PbS)': {
        'formula': 'PbS',
        'lattice_a': 5.94,  # Å
        'structure': 'Rock salt (Fm3m)',
        'deviation_from_Z': abs(5.94 - Z_CONSTANT) / Z_CONSTANT * 100,
        'metal_oxidation_states': ['Pb²⁺'],
        'redox_active': False,
        'reason': '6s² inert pair effect - Pb²⁺ is very stable',
        'biological_relevance': 'TOXIC - no biological iron-sulfur analog',
        'prebiotic_literature': 'Not associated with prebiotic chemistry',
    },
    'Pyrite (FeS₂)': {
        'formula': 'FeS2',
        'lattice_a': 5.417,  # Å
        'structure': 'Pyrite (Pa3)',
        'deviation_from_Z': abs(5.417 - Z_CONSTANT) / Z_CONSTANT * 100,
        'metal_oxidation_states': ['Fe²⁺', 'Fe³⁺'],
        'redox_active': True,
        'reason': 'Fe has accessible d-orbitals for electron transfer',
        'biological_relevance': 'Fe-S clusters in ALL life forms',
        'prebiotic_literature': 'Wächtershäuser iron-sulfur world hypothesis',
    },
    'Mackinawite (FeS)': {
        'formula': 'FeS',
        'lattice_a': 3.67,  # Å (tetragonal, a-parameter)
        'structure': 'Tetragonal (P4/nmm)',
        'deviation_from_Z': abs(3.67 - Z_CONSTANT) / Z_CONSTANT * 100,
        'metal_oxidation_states': ['Fe²⁺'],
        'redox_active': True,
        'reason': 'Fe has accessible d-orbitals',
        'biological_relevance': 'Precursor to FeS clusters',
        'prebiotic_literature': 'Russell submarine vent hypothesis',
    },
    'Sphalerite (ZnS)': {
        'formula': 'ZnS',
        'lattice_a': 5.41,  # Å
        'structure': 'Zinc blende (F43m)',
        'deviation_from_Z': abs(5.41 - Z_CONSTANT) / Z_CONSTANT * 100,
        'metal_oxidation_states': ['Zn²⁺'],
        'redox_active': False,  # Zn is d¹⁰, no redox
        'reason': 'd¹⁰ configuration - Zn²⁺ is stable',
        'biological_relevance': 'Zn in enzymes (not redox)',
        'prebiotic_literature': 'Some studies on ZnS photocatalysis',
    },
}


def analyze_electronic_structure():
    """
    Analyze why redox activity matters more than geometry.
    """
    print("\n" + "="*70)
    print("ELECTRONIC STRUCTURE ANALYSIS")
    print("="*70)

    print("""
    WHY REDOX ACTIVITY MATTERS FOR PREBIOTIC CATALYSIS:

    1. AMINO ACID SYNTHESIS requires electron transfer:
       - Reduction of CO₂ or CO to organic carbon
       - Reductive amination (adding NH₃ to ketoacids)
       - These reactions NEED a redox-active metal

    2. IRON (Fe) electronic configuration:
       - Ground state: [Ar] 3d⁶ 4s²
       - Fe²⁺: [Ar] 3d⁶  → can lose more electrons
       - Fe³⁺: [Ar] 3d⁵  → can gain electrons back
       - The d-orbitals are PARTIALLY FILLED = redox active

    3. LEAD (Pb) electronic configuration:
       - Ground state: [Xe] 4f¹⁴ 5d¹⁰ 6s² 6p²
       - Pb²⁺: [Xe] 4f¹⁴ 5d¹⁰ 6s²  → "inert pair" effect
       - The 6s² electrons are VERY STABLE (relativistic contraction)
       - Pb²⁺ → Pb⁴⁺ requires extreme conditions
       - Pb is NOT a biological catalyst

    4. THE KILLER ARGUMENT:
       - If Z² geometry mattered, Galena (closer to Z) would be catalytic
       - But Galena is NOT used in any biological system
       - Iron-sulfur clusters are in ALL life forms
       - This is because CHEMISTRY (redox), not GEOMETRY (lattice), matters
    """)


def compare_minerals():
    """
    Compare all minerals and their Z² deviations.
    """
    print("\n" + "="*70)
    print("MINERAL COMPARISON: GEOMETRY vs CHEMISTRY")
    print("="*70)

    print(f"\n  Z constant: {Z_CONSTANT:.4f} Å\n")

    # Sort by deviation from Z
    sorted_minerals = sorted(MINERALS.items(),
                            key=lambda x: x[1]['deviation_from_Z'])

    print("  Minerals sorted by GEOMETRIC proximity to Z:")
    print("  " + "-"*66)
    print(f"  {'Mineral':<20} {'Lattice (Å)':<12} {'Deviation':<12} {'Redox?':<8} {'Bio?':<8}")
    print("  " + "-"*66)

    for name, data in sorted_minerals:
        redox = "YES" if data['redox_active'] else "NO"
        bio = "YES" if "Fe-S" in data['biological_relevance'] or "ubiquitous" in data['biological_relevance'].lower() else "NO"
        print(f"  {name:<20} {data['lattice_a']:<12.3f} {data['deviation_from_Z']:<12.1f}% {redox:<8} {bio:<8}")

    print("  " + "-"*66)

    print("""
  OBSERVATION:
    - Galena is CLOSEST to Z (2.6% deviation)
    - But Galena has NO biological relevance and is TOXIC
    - Pyrite is FARTHER from Z (6.8% deviation)
    - But Pyrite is the BASIS of iron-sulfur world hypothesis

  CONCLUSION:
    If geometry (Z²) mattered, Galena would be biologically important.
    It isn't. Therefore, geometry doesn't determine catalytic activity.
    """)


def predict_catalytic_activity():
    """
    Predict catalytic activity based on electronic structure.
    """
    print("\n" + "="*70)
    print("CATALYTIC ACTIVITY PREDICTION")
    print("="*70)

    predictions = []

    for name, data in MINERALS.items():
        # Catalytic activity factors
        redox_score = 1.0 if data['redox_active'] else 0.0

        # Electron transfer capability
        if 'Fe' in data['formula']:
            electron_transfer = 0.9  # Fe is excellent
        elif 'Zn' in data['formula']:
            electron_transfer = 0.3  # Zn can coordinate but not transfer
        elif 'Pb' in data['formula']:
            electron_transfer = 0.1  # Pb is inert
        else:
            electron_transfer = 0.5

        # Biological precedent
        if 'Fe-S' in data['biological_relevance']:
            bio_score = 1.0
        elif 'enzyme' in data['biological_relevance'].lower():
            bio_score = 0.5
        else:
            bio_score = 0.0

        # Overall predicted activity (chemistry-based)
        activity_chemistry = (redox_score * 0.5 + electron_transfer * 0.3 + bio_score * 0.2)

        # If Z² geometry mattered (hypothetical)
        z_proximity = 1.0 - (data['deviation_from_Z'] / 100)
        activity_z2 = z_proximity

        predictions.append({
            'name': name,
            'lattice': data['lattice_a'],
            'z_deviation': data['deviation_from_Z'],
            'activity_chemistry': activity_chemistry,
            'activity_z2': activity_z2,
            'redox': data['redox_active'],
        })

    print("\n  Predicted catalytic activity for prebiotic amino acid synthesis:\n")
    print(f"  {'Mineral':<20} {'If Chemistry':<15} {'If Z² Geometry':<15} {'Redox':<8}")
    print("  " + "-"*58)

    for p in predictions:
        chem_bar = "█" * int(p['activity_chemistry'] * 10)
        z2_bar = "█" * int(p['activity_z2'] * 10)
        redox = "YES" if p['redox'] else "NO"
        print(f"  {p['name']:<20} {chem_bar:<15} {z2_bar:<15} {redox:<8}")

    print("  " + "-"*58)

    print("""
  INTERPRETATION:
    - "If Chemistry" column: Activity predicted by redox/electronic factors
    - "If Z² Geometry" column: Activity predicted by proximity to Z

    If Z² hypothesis is correct:
      Galena (PbS) should have HIGHEST activity
      Mackinawite (FeS) should have LOWEST activity

    If standard chemistry is correct:
      Pyrite (FeS₂) and Mackinawite (FeS) should have HIGHEST activity
      Galena (PbS) should have near-ZERO activity

  EXPERIMENTAL PREDICTION:
    Run identical prebiotic synthesis experiments with each mineral.
    Measure amino acid yield.
    If Galena >> Pyrite: Z² geometry matters (revolutionary!)
    If Pyrite >> Galena: Chemistry matters (expected)
    """)

    return predictions


def calculate_binding_site_geometry():
    """
    Analyze binding site geometry for amino acid precursors.
    """
    print("\n" + "="*70)
    print("BINDING SITE GEOMETRY ANALYSIS")
    print("="*70)

    print("""
    For amino acid synthesis, precursors (CO₂, NH₃, CH₄) must BIND to surface.

    KEY QUESTION: Does the Z-scale lattice provide optimal binding sites?

    BINDING CONSIDERATIONS:
    1. Metal-ligand distances:
       - Fe-N (ammonia): ~2.0-2.2 Å
       - Fe-O (CO₂): ~2.0-2.3 Å
       - Fe-S (surface): ~2.2-2.4 Å

    2. Surface site spacing:
       - Pyrite (100) surface: Fe-Fe = 5.417 Å (lattice parameter)
       - Galena (100) surface: Pb-Pb = 5.94 Å

    3. For BIDENTATE binding (molecule bridges two metal sites):
       - Ideal spacing depends on molecule size
       - Glycine (smallest amino acid): ~4-5 Å between binding groups
       - This is SMALLER than either lattice parameter

    ANALYSIS:
    """)

    # Glycine geometry
    glycine_n_to_o = 3.8  # Å, approximate distance between NH₂ and COOH in glycine

    for name, data in MINERALS.items():
        lattice = data['lattice_a']
        fit = "POSSIBLE" if abs(lattice - glycine_n_to_o) < 2.0 else "STRETCHED"
        print(f"    {name}: lattice = {lattice:.2f} Å, glycine span = {glycine_n_to_o:.1f} Å → {fit}")

    print("""
    CONCLUSION:
      Neither Galena nor Pyrite has lattice spacing matched to glycine geometry.
      Both require the molecule to stretch or bind at angles.
      The ~0.5 Å difference between them is NOT the determining factor.

      What matters is:
      1. Can the metal ACTIVATE the substrate (redox)?
      2. Can the metal COORDINATE multiple substrates simultaneously?
      3. Is the surface chemistry favorable (not toxic)?

      Pyrite wins on all counts. Galena fails.
    """)


def propose_experiment():
    """
    Propose the decisive experiment.
    """
    print("\n" + "="*70)
    print("PROPOSED DECISIVE EXPERIMENT: THE GALENA TEST")
    print("="*70)

    print("""
    EXPERIMENTAL DESIGN:

    1. MATERIALS:
       - Galena (PbS) powder, 99% pure, ~1 μm particle size
       - Pyrite (FeS₂) powder, 99% pure, ~1 μm particle size
       - Sphalerite (ZnS) powder (control), ~1 μm particle size
       - Quartz (SiO₂) powder (negative control)

    2. PREBIOTIC SOUP:
       - 100 mM NH₄Cl (ammonia source)
       - 50 mM NaHCO₃ (CO₂ source)
       - 10 mM Na₂S (sulfur source)
       - pH 7.0 buffer
       - Degassed, anaerobic conditions

    3. CONDITIONS:
       - Temperature: 80°C (prebiotic hydrothermal)
       - Pressure: 1 atm N₂
       - Duration: 7 days
       - 1 g mineral per 100 mL solution

    4. ANALYSIS:
       - Extract amino acids by acid hydrolysis
       - Quantify by HPLC with fluorescence detection
       - Measure total yield and relative abundances

    5. PREDICTED OUTCOMES:

       If Z² GEOMETRY matters:
       ┌─────────────────┬────────────────┬───────────────┐
       │ Mineral         │ Z deviation    │ Amino acid    │
       │                 │                │ yield         │
       ├─────────────────┼────────────────┼───────────────┤
       │ Galena (PbS)    │ 2.6% (BEST)    │ HIGHEST       │
       │ Sphalerite (ZnS)│ 6.6%           │ MEDIUM        │
       │ Pyrite (FeS₂)   │ 6.8%           │ MEDIUM        │
       │ Quartz (SiO₂)   │ 15% (control)  │ LOW           │
       └─────────────────┴────────────────┴───────────────┘

       If CHEMISTRY matters (expected):
       ┌─────────────────┬────────────────┬───────────────┐
       │ Mineral         │ Redox activity │ Amino acid    │
       │                 │                │ yield         │
       ├─────────────────┼────────────────┼───────────────┤
       │ Pyrite (FeS₂)   │ HIGH (Fe²⁺/³⁺) │ HIGHEST       │
       │ Sphalerite (ZnS)│ LOW (d¹⁰)      │ LOW-MEDIUM    │
       │ Galena (PbS)    │ NONE (6s²)     │ VERY LOW      │
       │ Quartz (SiO₂)   │ NONE           │ LOWEST        │
       └─────────────────┴────────────────┴───────────────┘

    6. INTERPRETATION:
       - If Galena ≥ Pyrite: Z² geometry is relevant (MAJOR DISCOVERY)
       - If Pyrite >> Galena: Chemistry dominates (expected)

    7. COST AND FEASIBILITY:
       - Estimated cost: $5,000-10,000
       - Time: 2-4 weeks
       - Equipment: Standard prebiotic chemistry lab
       - Novelty: HIGH - no prior study has isolated lattice parameter effect

    This experiment has NEVER been done. It would be a genuine
    contribution to origin-of-life research, regardless of outcome.
    """)


def run_full_comparison():
    """Run complete Galena vs Pyrite analysis."""

    print("="*70)
    print("THE DECISIVE TEST: Can Z² Geometry Explain Prebiotic Catalysis?")
    print("="*70)
    print(f"""
    Z constant: {Z_CONSTANT:.4f} Å

    The Test:
      - Galena (PbS):  a = 5.94 Å  → 2.6% from Z (CLOSER)
      - Pyrite (FeS₂): a = 5.417 Å → 6.8% from Z (FARTHER)

    If Z² geometry matters, Galena should be the better catalyst.
    If chemistry matters, Pyrite should be far superior.
    """)

    analyze_electronic_structure()
    compare_minerals()
    predictions = predict_catalytic_activity()
    calculate_binding_site_geometry()
    propose_experiment()

    # Final summary
    print("\n" + "="*70)
    print("FINAL ASSESSMENT")
    print("="*70)

    print("""
    WHAT WE CAN SAY WITH CONFIDENCE:

    1. Galena (PbS) is CLOSER to Z than Pyrite (FeS₂)
       - Galena: 2.6% deviation
       - Pyrite: 6.8% deviation

    2. Pyrite IS the key catalyst in iron-sulfur world hypothesis
       - Supported by decades of experimental work
       - Fe-S clusters are universal in biology

    3. Galena is NOT associated with prebiotic chemistry
       - No experimental support
       - Lead is toxic to all known life
       - No Fe-S cluster analogs contain Pb

    4. The reason is CHEMISTRY, not GEOMETRY:
       - Fe is redox-active (d-orbital chemistry)
       - Pb is NOT redox-active (inert pair effect)
       - Catalysis requires electron transfer

    CONCLUSION:
    The Galena vs Pyrite comparison ALREADY falsifies Z² abiogenesis
    at the conceptual level. Experimental confirmation would be definitive,
    but the electronic structure argument is compelling.

    HOWEVER - the experiment would still be valuable because:
    1. It would be the first direct test of lattice parameter effects
    2. A surprise result (Galena works) would be revolutionary
    3. Even a null result contributes to origin-of-life literature
    """)

    # Save results
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, 'galena_vs_pyrite_results.json')

    with open(output_file, 'w') as f:
        json.dump({
            'minerals': MINERALS,
            'z_constant': Z_CONSTANT,
            'predictions': predictions,
            'conclusion': 'Chemistry (redox activity) dominates over geometry (lattice parameter)'
        }, f, indent=2, default=str)

    print(f"\n  Results saved to: {output_file}")

    return predictions


if __name__ == "__main__":
    results = run_full_comparison()
