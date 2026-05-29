#!/usr/bin/env python3
"""
================================================================================
RIGOROUS VALIDATION TASK 3: First-Principles Backbone Angle Derivation
================================================================================

GOAL: Derive α-helix backbone angles (φ, ψ) from 5D Kaluza-Klein geometry
      WITHOUT post-hoc integer fitting.

CURRENT CLAIM:
  φ_L = -(11/6) × θ_Z ≈ -57°
  ψ_L = -(9/6) × θ_Z ≈ -47°
  where θ_Z = π/Z = π/(2√(8π/3)) ≈ 31.09°

PROBLEM: The factors 11/6 and 9/6 were chosen SPECIFICALLY to match experimental
values. This is numerology, not derivation.

THIS SCRIPT ATTEMPTS: To derive these ratios from first principles using
Kaluza-Klein compactification geometry.

Author: Carl Zimmerman + Claude
License: AGPL-3.0-or-later
================================================================================
"""

import numpy as np
from typing import Tuple, List, Dict
from dataclasses import dataclass

# =============================================================================
# Z² FUNDAMENTAL CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
Z_CONSTANT = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.7888
THETA_Z = np.pi / Z_CONSTANT  # ≈ 0.5428 rad ≈ 31.09°

# Experimental values from PDB statistics (Lovell et al. 2003, Hovmöller et al. 2002)
PHI_EXPERIMENTAL = -64.0  # degrees, ±7° standard deviation
PSI_EXPERIMENTAL = -41.0  # degrees, ±7° standard deviation
PHI_EXPERIMENTAL_SD = 7.0
PSI_EXPERIMENTAL_SD = 7.0

# =============================================================================
# APPROACH 1: Attempt derivation from S¹ compactification geometry
# =============================================================================

def attempt_s1_compactification_derivation():
    """
    In Kaluza-Klein theory, the 5th dimension is compactified on a circle S¹.
    The circumference of this circle is related to the coupling constant.

    Question: Does the Z² compactification geometry naturally produce
    specific angles that correspond to backbone torsions?
    """
    print("\n" + "="*70)
    print("APPROACH 1: S¹ Compactification Geometry")
    print("="*70)

    # In standard KK theory, the 5th dimension has circumference 2πR
    # where R is the compactification radius.
    #
    # For Z² theory, we hypothesize: R = Z/2π (so circumference = Z)

    R_z = Z_CONSTANT / (2 * np.pi)
    print(f"\nHypothesized compactification radius: R = Z/(2π) = {R_z:.4f} Å")

    # The natural angle divisions of a circle are:
    # - Full circle: 2π
    # - Half circle: π
    # - Quarter circle: π/2
    # - Sixth of circle: π/3

    # What angles does the Z² geometry naturally produce?
    natural_angles = {
        "2π/Z²": 2*np.pi / Z_SQUARED,
        "π/Z": np.pi / Z_CONSTANT,
        "Z/2π": Z_CONSTANT / (2*np.pi),
        "2π/Z": 2*np.pi / Z_CONSTANT,
        "Z²/2π": Z_SQUARED / (2*np.pi),
    }

    print("\nNatural angles from Z² geometry (radians → degrees):")
    for name, angle_rad in natural_angles.items():
        angle_deg = angle_rad * 180 / np.pi
        print(f"  {name:12s} = {angle_rad:.4f} rad = {angle_deg:.2f}°")

    # Check if any natural angle or simple combination matches φ or ψ
    print("\nChecking simple combinations against experimental values:")
    print(f"  Target φ = {PHI_EXPERIMENTAL}° ± {PHI_EXPERIMENTAL_SD}°")
    print(f"  Target ψ = {PSI_EXPERIMENTAL}° ± {PSI_EXPERIMENTAL_SD}°")

    # The fundamental Z angle is θ_Z = π/Z ≈ 31.09°
    theta_z_deg = THETA_Z * 180 / np.pi

    # What integer or simple rational multiples of θ_Z give φ and ψ?
    phi_ratio = abs(PHI_EXPERIMENTAL) / theta_z_deg
    psi_ratio = abs(PSI_EXPERIMENTAL) / theta_z_deg

    print(f"\n  |φ|/θ_Z = {phi_ratio:.4f}")
    print(f"  |ψ|/θ_Z = {psi_ratio:.4f}")

    # The current claim uses 11/6 ≈ 1.833 and 9/6 = 1.5
    # Let's see what these actually are
    print(f"\n  Claimed ratios: 11/6 = {11/6:.4f}, 9/6 = {9/6:.4f}")
    print(f"  Actual ratios:  {phi_ratio:.4f}, {psi_ratio:.4f}")

    # CRITICAL ANALYSIS: These don't match!
    # The claim used 11/6 ≈ 1.833 for φ, but actual ratio is ~2.06
    # This means the original claim is INCORRECT even as numerology!

    print("\n  ⚠️  DISCREPANCY DETECTED:")
    print(f"      Original claim: φ = -(11/6)×θ_Z = {-(11/6)*theta_z_deg:.1f}°")
    print(f"      Experimental:   φ = {PHI_EXPERIMENTAL}°")
    print(f"      Error: {abs(-(11/6)*theta_z_deg - PHI_EXPERIMENTAL):.1f}°")

    return False  # No first-principles derivation found


# =============================================================================
# APPROACH 2: Geodesics on T³ torus with Z² scaling
# =============================================================================

def attempt_t3_geodesic_derivation():
    """
    The Z² theory proposes that particles trace geodesics on a T³ torus
    with characteristic length Z. Can backbone angles emerge from
    the geometry of geodesics on this manifold?
    """
    print("\n" + "="*70)
    print("APPROACH 2: T³ Torus Geodesic Geometry")
    print("="*70)

    # A geodesic on a flat torus T³ wraps around the three circles
    # with winding numbers (n₁, n₂, n₃).
    #
    # The "slope" of the geodesic in the (θ₁, θ₂) plane is n₂/n₁
    # which corresponds to an angle arctan(n₂/n₁).

    print("\nSearching for winding numbers that produce backbone angles...")

    best_matches = []

    # Try all simple winding number combinations
    for n1 in range(1, 10):
        for n2 in range(-10, 10):
            if n1 == 0:
                continue

            # Geodesic angle in radians
            geodesic_angle_rad = np.arctan2(n2, n1)
            geodesic_angle_deg = geodesic_angle_rad * 180 / np.pi

            # Check against φ and ψ
            phi_error = abs(geodesic_angle_deg - PHI_EXPERIMENTAL)
            psi_error = abs(geodesic_angle_deg - PSI_EXPERIMENTAL)

            if phi_error < PHI_EXPERIMENTAL_SD:
                best_matches.append({
                    'winding': (n1, n2),
                    'angle': geodesic_angle_deg,
                    'matches': 'φ',
                    'error': phi_error
                })
            if psi_error < PSI_EXPERIMENTAL_SD:
                best_matches.append({
                    'winding': (n1, n2),
                    'angle': geodesic_angle_deg,
                    'matches': 'ψ',
                    'error': psi_error
                })

    if best_matches:
        print("\n  Matches found (within 1σ of experimental):")
        for m in best_matches:
            print(f"    Winding {m['winding']}: {m['angle']:.1f}° matches {m['matches']} (error: {m['error']:.1f}°)")
    else:
        print("\n  No matches found with simple winding numbers.")

    # ANALYSIS: Even if we find winding numbers that work, this is still
    # post-hoc fitting unless we can explain WHY those specific winding
    # numbers are preferred.

    print("\n  ⚠️  PROBLEM: Even if matches exist, we have no explanation for")
    print("      why specific winding numbers should be selected.")
    print("      This remains parameter fitting, not derivation.")

    return False


# =============================================================================
# APPROACH 3: Tetrahedral angle from sp³ hybridization
# =============================================================================

def attempt_tetrahedral_constraint():
    """
    The α-carbon in amino acids has approximately tetrahedral geometry
    due to sp³ hybridization. The tetrahedral angle is arccos(-1/3) ≈ 109.47°.

    Can we derive backbone angles from Z² geometry + tetrahedral constraints?
    """
    print("\n" + "="*70)
    print("APPROACH 3: Tetrahedral Geometry + Z² Constraint")
    print("="*70)

    # Tetrahedral angle
    theta_tet = np.arccos(-1/3)  # ≈ 109.47°
    theta_tet_deg = theta_tet * 180 / np.pi

    print(f"\n  Tetrahedral angle: {theta_tet_deg:.2f}°")
    print(f"  Z angle θ_Z: {THETA_Z * 180 / np.pi:.2f}°")

    # The backbone angles φ and ψ are dihedral angles, not bond angles.
    # They describe rotation around N-Cα and Cα-C bonds respectively.

    # HONEST ANALYSIS: There is no clear geometric relationship between
    # the Z² compactification scale and dihedral rotation barriers.
    #
    # The tetrahedral geometry sets bond angles (~109.5°), not dihedrals.
    # Dihedral preferences come from:
    # 1. Steric clashes (Ramachandran allowed regions)
    # 2. Hydrogen bonding (helix stabilization)
    # 3. Electronic effects (hyperconjugation)

    # Let's check if any combination makes sense:
    combinations = [
        ("180 - θ_tet - θ_Z", 180 - theta_tet_deg - (THETA_Z * 180/np.pi)),
        ("θ_tet - 2θ_Z", theta_tet_deg - 2*(THETA_Z * 180/np.pi)),
        ("θ_tet/2 - θ_Z", theta_tet_deg/2 - (THETA_Z * 180/np.pi)),
        ("-θ_tet/2 - θ_Z", -theta_tet_deg/2 - (THETA_Z * 180/np.pi)),
    ]

    print("\n  Checking geometric combinations:")
    for name, value in combinations:
        phi_match = "✓" if abs(value - PHI_EXPERIMENTAL) < PHI_EXPERIMENTAL_SD else "✗"
        psi_match = "✓" if abs(value - PSI_EXPERIMENTAL) < PSI_EXPERIMENTAL_SD else "✗"
        print(f"    {name:25s} = {value:7.2f}°  φ:{phi_match} ψ:{psi_match}")

    print("\n  ⚠️  CONCLUSION: No natural geometric relationship found.")
    print("      Tetrahedral constraints don't connect to Z² compactification.")

    return False


# =============================================================================
# APPROACH 4: Hydrogen bond geometry constraints
# =============================================================================

def attempt_hydrogen_bond_derivation():
    """
    α-helices are stabilized by i→i+4 hydrogen bonds. The helix geometry
    (pitch, residues per turn) is determined by optimizing H-bond geometry.

    Question: Does Z² geometry predict optimal H-bond distances/angles?
    """
    print("\n" + "="*70)
    print("APPROACH 4: Hydrogen Bond Optimization")
    print("="*70)

    # Optimal hydrogen bond geometry:
    # - N-H...O distance: 2.8-3.2 Å (optimal ~2.9 Å)
    # - N-H...O angle: 160-180° (optimal ~170°)

    H_BOND_OPTIMAL_DISTANCE = 2.9  # Å
    H_BOND_OPTIMAL_ANGLE = 170.0  # degrees

    # α-helix parameters (experimental):
    HELIX_PITCH = 5.4  # Å
    RESIDUES_PER_TURN = 3.6
    HELIX_RADIUS = 2.3  # Å

    print(f"\n  Experimental α-helix pitch: {HELIX_PITCH} Å")
    print(f"  Z constant: {Z_CONSTANT:.3f} Å")
    print(f"  Helix pitch / Z: {HELIX_PITCH / Z_CONSTANT:.3f}")

    # This is actually a good match! Helix pitch ≈ 0.93 Z
    # But can we DERIVE this, or is it coincidence?

    print("\n  Analysis: The helix pitch (5.4 Å) is within 7% of Z (5.79 Å).")
    print("  This is a genuine interesting coincidence.")

    # Now, can backbone angles be derived from helix geometry?
    # For an ideal helix with n residues per turn and pitch p:
    # φ + ψ ≈ -105° (from helix closure constraint)

    phi_plus_psi_experimental = PHI_EXPERIMENTAL + PSI_EXPERIMENTAL
    print(f"\n  φ + ψ (experimental): {phi_plus_psi_experimental}°")
    print(f"  Helix closure requires φ + ψ ≈ -105° to -110°")

    # The individual values of φ and ψ are determined by:
    # 1. Minimizing steric clashes
    # 2. Optimizing H-bond geometry
    # 3. The constraint φ + ψ ≈ -105°

    print("\n  ⚠️  HONEST ASSESSMENT:")
    print("      - The helix pitch matching Z is interesting")
    print("      - But backbone angles are determined by H-bond optimization")
    print("      - There is no Z² geometric constraint on individual φ, ψ values")
    print("      - The helix pitch-Z match may be coincidental")

    return False


# =============================================================================
# APPROACH 5: Statistical analysis of "fits"
# =============================================================================

def statistical_coincidence_analysis():
    """
    Given any geometric constant, how likely is it to find integer ratios
    that match biological angles? This tests whether the Z² match is
    meaningful or expected by chance.
    """
    print("\n" + "="*70)
    print("APPROACH 5: Statistical Coincidence Analysis")
    print("="*70)

    # Generate 1000 random "fundamental angles" between 10° and 60°
    np.random.seed(42)
    n_trials = 10000
    random_angles = np.random.uniform(10, 60, n_trials)

    # For each, search for simple rational multiples that match φ or ψ
    matches_found = 0

    for theta in random_angles:
        # Check multiples n/m for n,m in [-12, 12]
        for n in range(-12, 13):
            for m in range(1, 13):
                test_angle = (n/m) * theta

                # Check against φ and ψ
                if abs(test_angle - PHI_EXPERIMENTAL) < PHI_EXPERIMENTAL_SD:
                    matches_found += 1
                    break
            else:
                continue
            break

    match_probability = matches_found / n_trials

    print(f"\n  Random angle trial results:")
    print(f"    Trials: {n_trials}")
    print(f"    Matches found: {matches_found}")
    print(f"    Match probability: {match_probability:.1%}")

    print(f"\n  θ_Z = {THETA_Z * 180/np.pi:.2f}°")
    print(f"  Finding rational multiples that match backbone angles is")
    print(f"  expected ~{match_probability:.0%} of the time by chance.")

    if match_probability > 0.3:
        print("\n  ⚠️  CONCLUSION: The Z² → backbone angle correspondence is")
        print("      likely a statistical artifact, not a physical relationship.")

    return match_probability


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_full_derivation_analysis():
    """Run all derivation attempts and provide honest assessment."""

    print("="*70)
    print("RIGOROUS VALIDATION: First-Principles Backbone Angle Derivation")
    print("="*70)
    print("""
QUESTION: Can we derive α-helix backbone angles (φ ≈ -64°, ψ ≈ -41°)
          from Z² = 32π/3 geometry WITHOUT post-hoc integer fitting?

CURRENT CLAIM:
  φ = -(11/6) × θ_Z ≈ -57°
  ψ = -(9/6) × θ_Z ≈ -47°

PROBLEM: The integers 11 and 9 were chosen to fit the data.
         A true derivation must explain WHY these integers.
""")

    # Run all approaches
    results = {}

    results['s1_compactification'] = attempt_s1_compactification_derivation()
    results['t3_geodesic'] = attempt_t3_geodesic_derivation()
    results['tetrahedral'] = attempt_tetrahedral_constraint()
    results['hydrogen_bond'] = attempt_hydrogen_bond_derivation()
    match_prob = statistical_coincidence_analysis()

    # Final honest assessment
    print("\n" + "="*70)
    print("FINAL HONEST ASSESSMENT")
    print("="*70)

    print("""
RESULT: NO FIRST-PRINCIPLES DERIVATION FOUND

Approaches attempted:
  1. S¹ compactification geometry → No natural angle relationship
  2. T³ torus geodesics → No preferred winding numbers
  3. Tetrahedral + Z² constraints → No geometric connection
  4. H-bond optimization → Angles determined by chemistry, not Z²
  5. Statistical analysis → ~{:.0%} chance of random match

KEY FINDINGS:

  1. ORIGINAL CLAIM IS MATHEMATICALLY WRONG
     The claim φ = -(11/6)×θ_Z gives -57°, but PDB average is -64°.
     This is outside the claimed match, even with generous σ.

  2. HELIX PITCH MATCH IS INTERESTING
     α-helix pitch (5.4 Å) ≈ 0.93 × Z (5.79 Å)
     This 7% match is worth investigating but may be coincidence.

  3. NO PHYSICAL MECHANISM IDENTIFIED
     The Z² compactification scale (5.79 Å) has no known connection
     to dihedral torsion barriers in amino acids.

  4. BACKBONE ANGLES ARE DETERMINED BY CHEMISTRY
     - Steric repulsion (Ramachandran constraints)
     - Hydrogen bond optimization
     - Electronic effects
     None of these connect to extra-dimensional geometry.

HONEST CONCLUSION:
  The Z² → backbone angle claim cannot be derived from first principles.
  The integer factors (11/6, 9/6) are numerological fitting.
  The helix pitch matching Z is interesting but unexplained.

  STATUS: ❌ NOT VALIDATED
""".format(match_prob))

    return {
        'derivation_found': False,
        'original_claim_correct': False,
        'helix_pitch_match': True,
        'match_probability': match_prob,
        'conclusion': 'No first-principles derivation possible'
    }


if __name__ == "__main__":
    results = run_full_derivation_analysis()
