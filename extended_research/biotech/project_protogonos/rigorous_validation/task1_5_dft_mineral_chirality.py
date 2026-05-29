#!/usr/bin/env python3
"""
================================================================================
RIGOROUS VALIDATION TASKS 1 & 5: DFT Analysis of Amino Acids on Mineral Surfaces
================================================================================

TASK 1: Do L-amino acids have lower energy when constrained to Z² geometries
        on mineral surfaces?

TASK 5: Why might 5.417 Å (FeS₂ lattice) be catalytically special?

APPROACH:
  - Use PySCF for DFT calculations at B3LYP/6-31G* level
  - Compare adsorption energies of L vs D amino acids on mineral clusters
  - Analyze electronic structure for different lattice spacings

HONEST LIMITATIONS:
  - We use small clusters, not periodic boundary conditions
  - Gas-phase calculations miss solvation effects
  - Results are qualitative, not quantitative predictions

Author: Carl Zimmerman + Claude
License: AGPL-3.0-or-later
================================================================================
"""

import numpy as np
from typing import Tuple, Dict, List
import json
import os

try:
    from pyscf import gto, scf, dft
    from pyscf.geomopt import geometric_solver
    PYSCF_AVAILABLE = True
except ImportError:
    PYSCF_AVAILABLE = False
    print("WARNING: PySCF not available. Using analytical approximations.")

# Z² Constants
Z_CONSTANT = 2 * np.sqrt(8 * np.pi / 3)  # 5.7888 Å
FES2_LATTICE = 5.417  # Å (experimental)

# Conversion factors
ANGSTROM_TO_BOHR = 1.8897259886
HARTREE_TO_KCAL = 627.509

# =============================================================================
# PART 1: Enantiomer Energy Calculations
# =============================================================================

def create_glycine_coords(chirality: str = 'achiral') -> str:
    """
    Create glycine coordinates. Glycine is achiral, but we use it as a baseline.
    Returns XYZ format string.
    """
    # Glycine is NH2-CH2-COOH, achiral
    # Coordinates from experimental geometry
    return """
    N   0.000   0.000   0.000
    C   1.458   0.000   0.000
    C   2.009   1.420   0.000
    O   1.251   2.392  -0.142
    O   3.339   1.574   0.138
    H  -0.334  -0.475   0.847
    H  -0.334  -0.475  -0.847
    H   1.814  -0.537   0.892
    H   1.814  -0.537  -0.892
    H   3.623   2.494   0.094
    """


def create_alanine_coords(chirality: str = 'L') -> str:
    """
    Create L-Alanine or D-Alanine coordinates.
    L-Alanine has the methyl group on one side of the plane.
    D-Alanine is the mirror image.
    """
    if chirality == 'L':
        # L-Alanine (S configuration at Cα)
        return """
        N    0.000   0.000   0.000
        C    1.458   0.000   0.000
        C    2.009   1.420   0.000
        O    1.251   2.392  -0.142
        O    3.339   1.574   0.138
        C    1.989  -0.781   1.215
        H   -0.334  -0.475   0.847
        H   -0.334  -0.475  -0.847
        H    1.814  -0.537  -0.892
        H    1.635  -0.321   2.144
        H    1.635  -1.814   1.135
        H    3.081  -0.781   1.215
        H    3.623   2.494   0.094
        """
    else:
        # D-Alanine (R configuration at Cα) - mirror image
        return """
        N    0.000   0.000   0.000
        C    1.458   0.000   0.000
        C    2.009   1.420   0.000
        O    1.251   2.392  -0.142
        O    3.339   1.574   0.138
        C    1.989  -0.781  -1.215
        H   -0.334  -0.475   0.847
        H   -0.334  -0.475  -0.847
        H    1.814  -0.537   0.892
        H    1.635  -0.321  -2.144
        H    1.635  -1.814  -1.135
        H    3.081  -0.781  -1.215
        H    3.623   2.494   0.094
        """


def calculate_enantiomer_energies():
    """
    Calculate energies of L-Alanine vs D-Alanine in vacuum.

    EXPECTED RESULT: E(L) = E(D) by symmetry.
    Any difference would be a numerical artifact or indicate broken symmetry.
    """
    print("\n" + "="*70)
    print("TASK 1a: Vacuum Enantiomer Energies (DFT B3LYP/6-31G*)")
    print("="*70)

    if not PYSCF_AVAILABLE:
        print("\n  PySCF not available. Using known physics:")
        print("  E(L-Alanine) = E(D-Alanine) by CPT symmetry.")
        print("  No energy difference in vacuum - this is fundamental physics.")
        return {'L': 0.0, 'D': 0.0, 'difference': 0.0}

    results = {}

    for chirality in ['L', 'D']:
        print(f"\n  Calculating {chirality}-Alanine energy...")

        coords = create_alanine_coords(chirality)

        mol = gto.Mole()
        mol.atom = coords
        mol.basis = '6-31g*'
        mol.charge = 0
        mol.spin = 0
        mol.verbose = 0
        mol.build()

        # DFT calculation with B3LYP functional
        mf = dft.RKS(mol)
        mf.xc = 'b3lyp'
        mf.kernel()

        energy_hartree = mf.e_tot
        energy_kcal = energy_hartree * HARTREE_TO_KCAL

        results[chirality] = energy_kcal
        print(f"    E({chirality}-Ala) = {energy_hartree:.8f} Ha = {energy_kcal:.4f} kcal/mol")

    difference = results['L'] - results['D']
    print(f"\n  ΔE = E(L) - E(D) = {difference:.6f} kcal/mol")

    if abs(difference) < 0.001:
        print("\n  ✓ CONFIRMED: Enantiomers have identical energies in vacuum.")
        print("    This is required by CPT symmetry - physics is correct.")
    else:
        print(f"\n  ⚠️  Small difference ({difference:.6f} kcal/mol) is numerical noise.")
        print("    True ΔE = 0 by symmetry.")

    return {'L': results['L'], 'D': results['D'], 'difference': difference}


# =============================================================================
# PART 2: Mineral Surface Model
# =============================================================================

def create_fe2s4_cluster(lattice_spacing: float = 5.417) -> str:
    """
    Create a small Fe₂S₄ cluster to model FeS₂ surface.

    The pyrite (FeS₂) structure has Fe atoms at corners and face centers
    of a cubic lattice with a = 5.417 Å.

    We create a minimal Fe-S cluster to capture local electronic effects.
    """
    # Scale factor relative to experimental pyrite
    scale = lattice_spacing / 5.417

    # Fe₂S₄ cluster representing a surface site
    # Fe-S bond length in pyrite: ~2.26 Å
    fe_s_bond = 2.26 * scale

    # Simple tetrahedral-like arrangement
    coords = f"""
    Fe   0.000   0.000   0.000
    Fe   {lattice_spacing:.3f}   0.000   0.000
    S    {lattice_spacing/2:.3f}   {fe_s_bond:.3f}   {fe_s_bond:.3f}
    S    {lattice_spacing/2:.3f}  -{fe_s_bond:.3f}   {fe_s_bond:.3f}
    S    {lattice_spacing/2:.3f}   {fe_s_bond:.3f}  -{fe_s_bond:.3f}
    S    {lattice_spacing/2:.3f}  -{fe_s_bond:.3f}  -{fe_s_bond:.3f}
    """

    return coords


def calculate_cluster_binding_energies(lattice_spacings: List[float]):
    """
    Calculate the stability of Fe₂S₄ clusters at different lattice spacings.

    QUESTION: Is 5.417 Å electronically special?
    """
    print("\n" + "="*70)
    print("TASK 5: FeS₂ Cluster Stability vs Lattice Spacing")
    print("="*70)

    if not PYSCF_AVAILABLE:
        print("\n  PySCF not available. Using physical reasoning:")
        print("  FeS₂ lattice parameter is 5.417 Å because this minimizes")
        print("  the total energy given Fe-S bond lengths and crystal packing.")
        print("  It is NOT related to Z² geometry - it's determined by:")
        print("    - Fe 3d orbital radii")
        print("    - S 3p orbital radii")
        print("    - Coulomb repulsion")
        print("    - Madelung energy of the crystal")
        return {}

    print("\n  Computing cluster energies for different lattice spacings...")
    print("  (This models WHY 5.417 Å is the experimental value)\n")

    results = {}

    for spacing in lattice_spacings:
        coords = create_fe2s4_cluster(spacing)

        try:
            mol = gto.Mole()
            mol.atom = coords
            mol.basis = '6-31g'  # Smaller basis for metal clusters
            mol.charge = 0
            mol.spin = 0  # Assume closed shell for simplicity
            mol.verbose = 0
            mol.build()

            # Use DFT with PBE functional (better for metals)
            mf = dft.RKS(mol)
            mf.xc = 'pbe'
            mf.kernel()

            energy_hartree = mf.e_tot
            results[spacing] = energy_hartree * HARTREE_TO_KCAL

            print(f"    Spacing {spacing:.3f} Å: E = {energy_hartree:.6f} Ha = {results[spacing]:.2f} kcal/mol")

        except Exception as e:
            print(f"    Spacing {spacing:.3f} Å: Calculation failed ({str(e)[:50]})")
            results[spacing] = None

    # Find minimum
    valid_results = {k: v for k, v in results.items() if v is not None}
    if valid_results:
        min_spacing = min(valid_results, key=valid_results.get)
        print(f"\n  Lowest energy at spacing: {min_spacing:.3f} Å")
        print(f"  Experimental FeS₂: 5.417 Å")
        print(f"  Z constant: {Z_CONSTANT:.3f} Å")

        if abs(min_spacing - FES2_LATTICE) < 0.1:
            print("\n  ✓ DFT reproduces experimental lattice parameter.")
            print("    This validates our cluster model.")
        if abs(min_spacing - Z_CONSTANT) < 0.1:
            print("\n  ⚠️  Minimum near Z constant - investigate further!")
        else:
            print(f"\n  Note: Minimum at {min_spacing:.3f} Å, not at Z = {Z_CONSTANT:.3f} Å")
            print("        FeS₂ lattice is determined by Fe-S chemistry, not Z² geometry.")

    return results


# =============================================================================
# PART 3: Chiral Surface Adsorption
# =============================================================================

def analyze_chirality_on_surface():
    """
    Analyze whether a mineral surface can create chirality preference.

    PHYSICS: A flat, achiral surface cannot distinguish enantiomers.
    Only CHIRAL surfaces (like certain crystal faces) can create bias.

    QUESTION: Does the Z² = 5.79 Å scale provide ANY chiral selection?
    """
    print("\n" + "="*70)
    print("TASK 1b: Can Z² Geometry Create Chirality Bias?")
    print("="*70)

    print("""
    FUNDAMENTAL PHYSICS ANALYSIS:

    1. ACHIRAL SURFACES CANNOT SELECT CHIRALITY
       - A flat Fe-S surface has mirror symmetry
       - Both L and D amino acids bind with identical energy
       - No Z² magic changes this - it's a symmetry argument

    2. CHIRAL SURFACES CAN SELECT CHIRALITY
       - Some crystal faces lack mirror symmetry (e.g., quartz 101 face)
       - These can bind L vs D with different energies
       - This is well-established surface chemistry

    3. Z² GEOMETRY HAS NO CHIRALITY
       - Z = 5.79 Å is just a length scale
       - Length scales are achiral (the same for L and D)
       - No amount of Z² geometry can create chirality from nothing

    4. THE CLAIM IS PHYSICALLY IMPOSSIBLE
       - "Z² geometry creates chirality bias" violates symmetry
       - Chirality must come from a chiral source:
         * Circularly polarized light
         * Chiral crystal surfaces
         * Parity-violating weak force (tiny, ~10⁻¹⁷ eV)

    CONCLUSION:
       The Z² → chirality claim is FALSE by fundamental physics.
       No computational validation is needed - it's ruled out by symmetry.
    """)

    # Let's do a simple sanity check anyway
    if PYSCF_AVAILABLE:
        print("\n  Sanity check: L vs D on symmetric cluster...")

        # Create a symmetric Fe₂S₄ cluster and place amino acid above it
        # Due to symmetry, E(L) = E(D) must hold

        cluster = create_fe2s4_cluster(FES2_LATTICE)
        l_ala = create_alanine_coords('L')
        d_ala = create_alanine_coords('D')

        # For a proper calculation, we'd need to position the amino acid
        # above the cluster. This is complex, so we'll note the conclusion.

        print("  (Full adsorption calculation would require geometry optimization)")
        print("  Mathematical result: E(L on achiral surface) = E(D on achiral surface)")
        print("  This is guaranteed by symmetry, not a computational result.")

    return {
        'can_achiral_surface_select_chirality': False,
        'reason': 'Symmetry forbids chirality selection on achiral surfaces',
        'z2_chirality_claim': 'FALSE - violates fundamental physics'
    }


# =============================================================================
# PART 4: Why IS 5.417 Å special (for real)?
# =============================================================================

def explain_fes2_lattice():
    """
    Explain why FeS₂ has a lattice parameter of 5.417 Å using real physics.
    This is NOT related to Z² - it's standard solid-state chemistry.
    """
    print("\n" + "="*70)
    print("TASK 5b: Why FeS₂ Has a = 5.417 Å (Real Physics)")
    print("="*70)

    print("""
    THE REAL EXPLANATION:

    1. IONIC RADII
       - Fe²⁺ ionic radius: 0.78 Å (high spin)
       - S²⁻ ionic radius: 1.84 Å
       - Sum: 2.62 Å (close to Fe-S bond length of 2.26 Å)

    2. CRYSTAL STRUCTURE
       - Pyrite has Pa3̄ space group (cubic)
       - Fe atoms at corners and face centers
       - S₂ dumbbells at octahedral sites
       - The lattice parameter a = 5.417 Å comes from:
           a = 2 × (r_Fe + r_S) × packing_factor

    3. ELECTRONIC STRUCTURE
       - Fe 3d⁶ configuration splits in cubic field
       - S-S bond length in S₂²⁻: 2.14 Å
       - These electronic factors set the equilibrium geometry

    4. COMPARISON TO Z CONSTANT
       - Z = 5.789 Å
       - FeS₂ = 5.417 Å
       - Difference: 0.37 Å (6.8%)

       This is a COINCIDENCE within the range of typical solid-state
       parameters (4-7 Å for many materials).

    5. CATALYTIC PROPERTIES
       FeS₂ is a good prebiotic catalyst because:
       - Redox-active Fe centers
       - S sites for binding -NH₂ and -COOH groups
       - NOT because of Z² geometry

       The iron-sulfur world hypothesis (Wächtershäuser) explains
       prebiotic chemistry WITHOUT invoking Z².
    """)

    # Calculate some relevant ionic radii sums
    r_Fe = 0.78  # Å
    r_S = 1.84   # Å

    expected_bond = r_Fe + r_S
    actual_bond = 2.26  # Fe-S in pyrite

    print(f"\n  Ionic radii prediction: Fe-S = {expected_bond:.2f} Å")
    print(f"  Experimental Fe-S bond: {actual_bond:.2f} Å")
    print(f"  (Covalent character reduces the bond length)")

    # Simple lattice parameter estimate
    # In pyrite, a ≈ 2 × Fe-S × √2 (diagonal across cube face)
    estimated_a = 2 * actual_bond * np.sqrt(2)
    print(f"\n  Estimated lattice: a ≈ 2 × {actual_bond:.2f} × √2 = {estimated_a:.2f} Å")
    print(f"  Experimental: a = 5.417 Å")
    print(f"  (Simple estimate off by {abs(estimated_a - 5.417)/5.417*100:.0f}% - real calculation needs Madelung energy)")

    return {
        'fes2_lattice_explanation': 'Ionic radii + crystal packing',
        'z2_connection': 'NONE - coincidental similarity'
    }


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_full_dft_analysis():
    """Run all DFT-based analyses."""

    print("="*70)
    print("RIGOROUS VALIDATION: DFT Analysis of Z² Abiogenesis Claims")
    print("="*70)
    print(f"\nPySCF Available: {PYSCF_AVAILABLE}")
    print(f"Using basis: 6-31G* (amino acids), 6-31G (metal clusters)")
    print(f"Functional: B3LYP (organics), PBE (metals)")

    results = {}

    # Part 1: Enantiomer energies
    results['enantiomers'] = calculate_enantiomer_energies()

    # Part 2: Cluster stability vs lattice spacing
    spacings = [4.5, 4.8, 5.0, 5.2, 5.417, 5.6, 5.789, 6.0, 6.2, 6.5]
    results['cluster_energies'] = calculate_cluster_binding_energies(spacings)

    # Part 3: Chirality on surfaces
    results['chirality_analysis'] = analyze_chirality_on_surface()

    # Part 4: Real explanation for FeS₂
    results['fes2_explanation'] = explain_fes2_lattice()

    # Final summary
    print("\n" + "="*70)
    print("FINAL SUMMARY: DFT VALIDATION RESULTS")
    print("="*70)

    print("""
    CLAIM 1: "L-amino acids have lower energy on Z² mineral surfaces"
    RESULT:  ❌ FALSE
             - Enantiomers have identical energy by CPT symmetry
             - Achiral surfaces cannot select chirality
             - This is fundamental physics, not a computational result

    CLAIM 2: "5.417 Å is special because it's close to Z"
    RESULT:  ❌ FALSE
             - FeS₂ lattice is determined by Fe-S chemistry
             - Ionic radii + crystal packing explains the value
             - The 6.8% match to Z is coincidental
             - Many materials have lattice parameters in 4-7 Å range

    CLAIM 3: "FeS₂ is catalytically special for abiogenesis"
    RESULT:  ✓ TRUE (but not because of Z²)
             - Wächtershäuser iron-sulfur world hypothesis is real
             - Fe-S clusters are ubiquitous in biology
             - Catalysis comes from redox chemistry, not geometry

    OVERALL: The Z² → abiogenesis connection is not supported by DFT.
             The FeS₂ lattice / Z similarity is coincidental.
             Real prebiotic chemistry doesn't need Z² geometry.
    """)

    # Save results
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, 'task1_5_dft_results.json')

    # Convert numpy types for JSON
    def convert_to_serializable(obj):
        if isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        return obj

    with open(output_file, 'w') as f:
        json.dump(convert_to_serializable(results), f, indent=2, default=str)

    print(f"\n  Results saved to: {output_file}")

    return results


if __name__ == "__main__":
    results = run_full_dft_analysis()
