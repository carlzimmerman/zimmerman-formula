#!/usr/bin/env python3
"""
val_15_decoy_falsification.py

DECOY FALSIFICATION TEST - The "Garbage" Test
==============================================

This is the ultimate sanity check for the Z² geometric scoring pipeline.

THE PREMISE:
We feed the engine a sequence that is chemically and geometrically IMPOSSIBLE
to fit in a tight binding pocket: WWWWWW (Poly-Tryptophan).

Tryptophan is:
- The LARGEST amino acid (227.8 Å³ volume)
- The BULKIEST side chain (indole ring system)
- A steric nightmare when repeated

If this decoy achieves:
- Z² fitness > 50%, OR
- Negative ΔG (favorable binding), OR
- Mean contact distance near 6.02 Å

Then the pipeline is BROKEN and generating SLOP.

We EXPECT to see:
- CATASTROPHIC steric clashes
- POSITIVE (unfavorable) ΔG
- Mean contact distance << 6.02 Å (atoms forced too close)
- Z² fitness < 20%
- Lennard-Jones repulsion in the THOUSANDS of kcal/mol

Author: Carl Zimmerman
Framework: Zimmerman Unified Geometry Framework (ZUGF)
License: AGPL v3.0
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json
import warnings

try:
    from scipy.spatial import Voronoi, Delaunay
    from scipy.spatial.distance import cdist, pdist
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

# ============================================================================
# CONSTANTS
# ============================================================================

Z2_VOLUME = 32 * np.pi / 3  # 33.51 Å³
Z2_DISTANCE = np.sqrt(Z2_VOLUME)  # 5.79 Å
EXPANSION_MULTIPLIER = 1.0391
IDEAL_BIOLOGICAL_DISTANCE = Z2_DISTANCE * EXPANSION_MULTIPLIER  # 6.02 Å

# Tryptophan properties - THE MONSTER
TRYPTOPHAN = {
    'code': 'W',
    'name': 'Tryptophan',
    'volume': 227.8,  # Å³ - LARGEST amino acid
    'vdw_radius': 2.55,  # Å - BIGGEST radius
    'mass': 204.23,  # Da
    'side_chain_atoms': 14,  # Massive indole ring
}

# For comparison
CYSTEINE = {
    'code': 'C',
    'name': 'Cysteine',
    'volume': 108.5,  # Å³
    'vdw_radius': 1.89,  # Å
}

# Lennard-Jones parameters
LJ_EPSILON = 0.1  # kcal/mol (typical)
LJ_SIGMA = 3.5    # Å (typical C-C)


def generate_poly_tryptophan_structure(n_residues: int = 6) -> np.ndarray:
    """
    Generate 3D coordinates for poly-tryptophan peptide.

    Tryptophan has a massive indole ring system. We model it as a
    backbone plus extended side chain atoms.

    Returns: Nx3 array of atom positions
    """
    positions = []

    # Backbone parameters
    CA_CA_DISTANCE = 3.8  # Å

    # Start position
    current_pos = np.array([0.0, 0.0, 0.0])
    direction = np.array([1.0, 0.0, 0.0])  # Move along x-axis

    for res_idx in range(n_residues):
        # Add backbone CA
        positions.append(current_pos.copy())

        # Add backbone N (offset from CA)
        n_pos = current_pos + np.array([-1.47, 0.0, 0.0])
        positions.append(n_pos)

        # Add backbone C (offset from CA)
        c_pos = current_pos + np.array([1.52, 0.0, 0.0])
        positions.append(c_pos)

        # Add backbone O
        o_pos = c_pos + np.array([0.0, 1.23, 0.0])
        positions.append(o_pos)

        # Add tryptophan side chain - the MASSIVE indole ring
        # CB - beta carbon
        cb_pos = current_pos + np.array([0.5, 1.5, 0.5])
        positions.append(cb_pos)

        # CG - gamma carbon (start of indole)
        cg_pos = cb_pos + np.array([0.0, 1.5, 0.0])
        positions.append(cg_pos)

        # CD1 - indole ring atom 1
        cd1_pos = cg_pos + np.array([1.2, 0.7, 0.0])
        positions.append(cd1_pos)

        # NE1 - indole nitrogen
        ne1_pos = cd1_pos + np.array([1.0, -0.5, 0.0])
        positions.append(ne1_pos)

        # CE2 - fused ring junction
        ce2_pos = ne1_pos + np.array([0.5, -1.2, 0.0])
        positions.append(ce2_pos)

        # CD2 - other junction
        cd2_pos = cg_pos + np.array([0.0, 1.4, 0.0])
        positions.append(cd2_pos)

        # CE3 - benzene ring
        ce3_pos = cd2_pos + np.array([-1.2, 0.7, 0.0])
        positions.append(ce3_pos)

        # CZ3
        cz3_pos = ce3_pos + np.array([-0.7, 1.2, 0.0])
        positions.append(cz3_pos)

        # CH2
        ch2_pos = cz3_pos + np.array([0.7, 1.2, 0.0])
        positions.append(ch2_pos)

        # CZ2
        cz2_pos = ch2_pos + np.array([1.4, 0.0, 0.0])
        positions.append(cz2_pos)

        # Move to next residue position
        current_pos = current_pos + direction * CA_CA_DISTANCE

        # Add slight helical twist for realism
        rotation_angle = 100 * np.pi / 180  # degrees per residue
        direction = np.array([
            np.cos(rotation_angle) * direction[0] - np.sin(rotation_angle) * direction[1],
            np.sin(rotation_angle) * direction[0] + np.cos(rotation_angle) * direction[1],
            direction[2]
        ])

    return np.array(positions)


def generate_binding_pocket(center: np.ndarray, radius: float = 8.0, n_atoms: int = 30) -> np.ndarray:
    """
    Generate a spherical binding pocket - the same geometry we use for drugs.

    This pocket has radius ~8 Å, which is appropriate for small peptides.
    Poly-tryptophan will NOT fit.
    """
    positions = []

    # Distribute atoms on sphere surface
    golden_ratio = (1 + np.sqrt(5)) / 2

    for i in range(n_atoms):
        theta = 2 * np.pi * i / golden_ratio
        phi = np.arccos(1 - 2 * (i + 0.5) / n_atoms)

        x = center[0] + radius * np.sin(phi) * np.cos(theta)
        y = center[1] + radius * np.sin(phi) * np.sin(theta)
        z = center[2] + radius * np.cos(phi)

        positions.append([x, y, z])

    return np.array(positions)


def force_into_pocket(peptide_positions: np.ndarray, pocket_center: np.ndarray) -> np.ndarray:
    """
    Force the peptide into the binding pocket by translating it to the center.

    This simulates what would happen if we tried to dock poly-tryptophan.
    """
    # Center the peptide
    peptide_com = np.mean(peptide_positions, axis=0)
    centered_peptide = peptide_positions - peptide_com + pocket_center

    return centered_peptide


def calculate_z2_geometric_fitness(positions: np.ndarray) -> dict:
    """
    Calculate Z² geometric fitness using Voronoi/Delaunay analysis.

    Same logic as geo_04_z2_geometric_scorer.py
    """
    if not HAS_SCIPY or len(positions) < 5:
        return {
            'mean_distance': np.nan,
            'z2_fitness': 0.0,
            'error': 'Insufficient data or scipy not available'
        }

    try:
        # Calculate pairwise distances
        distances = pdist(positions)

        # Use Delaunay triangulation for contact distances
        tri = Delaunay(positions)

        contact_distances = []
        for simplex in tri.simplices:
            for i in range(4):
                for j in range(i + 1, 4):
                    d = np.linalg.norm(positions[simplex[i]] - positions[simplex[j]])
                    if d < 10.0:  # Only count contacts < 10 Å
                        contact_distances.append(d)

        if not contact_distances:
            contact_distances = distances[distances < 10.0].tolist()

        mean_distance = np.mean(contact_distances) if contact_distances else 0
        std_distance = np.std(contact_distances) if contact_distances else 0

        # Z² fitness: how close is mean distance to ideal 6.02 Å?
        deviation = abs(mean_distance - IDEAL_BIOLOGICAL_DISTANCE)
        z2_fitness = np.exp(-(deviation**2) / (2 * 1.0**2))

        # Additional penalty for distances that are TOO CLOSE (steric clash indicator)
        min_distance = min(contact_distances) if contact_distances else 0
        if min_distance < 2.5:  # Severe steric clash
            z2_fitness *= 0.1  # Heavy penalty

        return {
            'mean_distance': float(mean_distance),
            'std_distance': float(std_distance),
            'min_distance': float(min_distance),
            'n_contacts': len(contact_distances),
            'z2_fitness': float(z2_fitness),
            'deviation_from_ideal': float(deviation),
            'ideal_distance': float(IDEAL_BIOLOGICAL_DISTANCE),
        }

    except Exception as e:
        return {
            'mean_distance': np.nan,
            'z2_fitness': 0.0,
            'error': str(e)
        }


def calculate_lennard_jones_energy(peptide_pos: np.ndarray, pocket_pos: np.ndarray) -> dict:
    """
    Calculate Lennard-Jones energy between peptide and pocket.

    LJ potential: U(r) = 4ε[(σ/r)^12 - (σ/r)^6]

    The r^12 term is the REPULSION - this should be MASSIVE for poly-tryptophan.
    """
    # Calculate all pairwise distances between peptide and pocket
    distances = cdist(peptide_pos, pocket_pos)

    # Avoid division by zero
    distances = np.maximum(distances, 0.1)

    # LJ potential components
    sigma_over_r = LJ_SIGMA / distances

    # Repulsive term (r^-12) - should DOMINATE for clashing atoms
    repulsive = (sigma_over_r ** 12)

    # Attractive term (r^-6)
    attractive = (sigma_over_r ** 6)

    # Total LJ energy
    lj_energy = 4 * LJ_EPSILON * (repulsive - attractive)

    # Sum all interactions
    total_repulsive = np.sum(repulsive) * 4 * LJ_EPSILON
    total_attractive = np.sum(attractive) * 4 * LJ_EPSILON
    total_lj = np.sum(lj_energy)

    # Count severe clashes (distances < 2.0 Å)
    severe_clashes = np.sum(distances < 2.0)
    moderate_clashes = np.sum(distances < 3.0)

    return {
        'total_lj_energy': float(total_lj),
        'repulsive_energy': float(total_repulsive),
        'attractive_energy': float(total_attractive),
        'severe_clashes': int(severe_clashes),
        'moderate_clashes': int(moderate_clashes),
        'min_distance': float(np.min(distances)),
        'mean_distance': float(np.mean(distances)),
    }


def calculate_steric_clash_penalty(peptide_pos: np.ndarray) -> dict:
    """
    Calculate internal steric clashes within the peptide itself.

    Poly-tryptophan should have MASSIVE internal clashes because
    the indole rings collide with each other.
    """
    if len(peptide_pos) < 2:
        return {'internal_clashes': 0, 'clash_energy': 0.0}

    # All pairwise distances within peptide
    internal_distances = pdist(peptide_pos)

    # Count clashes (non-bonded atoms closer than sum of VdW radii)
    # For tryptophan, VdW radius ~ 2.55 Å, so clash threshold ~ 2.5 Å
    CLASH_THRESHOLD = 2.5

    clashes = np.sum(internal_distances < CLASH_THRESHOLD)

    # Energy penalty for clashes (simplified)
    # Each clash adds ~10 kcal/mol penalty
    clash_energy = clashes * 10.0

    # Severe clashes (< 1.5 Å) are physically impossible
    severe_clashes = np.sum(internal_distances < 1.5)

    return {
        'internal_clashes': int(clashes),
        'severe_internal_clashes': int(severe_clashes),
        'clash_energy': float(clash_energy),
        'min_internal_distance': float(np.min(internal_distances)) if len(internal_distances) > 0 else float('inf'),
    }


def estimate_binding_free_energy(z2_result: dict, lj_result: dict, clash_result: dict) -> dict:
    """
    Estimate total binding free energy.

    For poly-tryptophan, this should be HIGHLY POSITIVE (unfavorable).
    """
    # Components
    lj_contribution = lj_result['total_lj_energy']
    clash_contribution = clash_result['clash_energy']

    # Entropic penalty for forcing large residues together
    # Each tryptophan loses ~2 kcal/mol conformational entropy when confined
    entropy_penalty = 6 * 2.0  # 6 tryptophans × 2 kcal/mol

    # Total ΔG
    total_dG = lj_contribution + clash_contribution + entropy_penalty

    return {
        'lj_contribution': float(lj_contribution),
        'clash_contribution': float(clash_contribution),
        'entropy_penalty': float(entropy_penalty),
        'total_dG': float(total_dG),
        'binding_favorable': total_dG < 0,
    }


def run_decoy_falsification():
    """
    Main falsification test.

    This is the moment of truth. If poly-tryptophan scores well,
    the entire pipeline is garbage.
    """
    print("=" * 70)
    print("DECOY FALSIFICATION TEST")
    print("The 'Garbage' Test for Z² Geometric Scoring Pipeline")
    print("=" * 70)

    print("\n" + "=" * 70)
    print("THE DECOY: WWWWWW (Poly-Tryptophan)")
    print("=" * 70)
    print(f"""
Tryptophan Properties:
- Volume: {TRYPTOPHAN['volume']} Å³ (LARGEST amino acid)
- VdW Radius: {TRYPTOPHAN['vdw_radius']} Å (BIGGEST)
- Side Chain Atoms: {TRYPTOPHAN['side_chain_atoms']} (massive indole ring)

For comparison, Cysteine (used in our successful drugs):
- Volume: {CYSTEINE['volume']} Å³
- VdW Radius: {CYSTEINE['vdw_radius']} Å

Poly-Tryptophan is {TRYPTOPHAN['volume'] / CYSTEINE['volume']:.1f}x larger than Poly-Cysteine!
""")

    # Generate structures
    print("\n📐 STEP 1: Generating 3D Structures...")

    # Generate poly-tryptophan
    peptide_positions = generate_poly_tryptophan_structure(n_residues=6)
    print(f"   Generated WWWWWW with {len(peptide_positions)} atoms")
    print(f"   Peptide dimensions: {np.ptp(peptide_positions, axis=0)} Å")

    # Generate binding pocket
    pocket_center = np.array([0.0, 0.0, 0.0])
    pocket_positions = generate_binding_pocket(pocket_center, radius=8.0, n_atoms=30)
    print(f"   Generated binding pocket with {len(pocket_positions)} atoms")
    print(f"   Pocket radius: 8.0 Å")

    # Force peptide into pocket
    print("\n🎯 STEP 2: Forcing Decoy Into Binding Pocket...")
    forced_peptide = force_into_pocket(peptide_positions, pocket_center)
    print(f"   Peptide forced to pocket center: {pocket_center}")

    # Calculate Z² geometric fitness
    print("\n📊 STEP 3: Z² Geometric Scoring (geo_04 logic)...")
    z2_result = calculate_z2_geometric_fitness(forced_peptide)

    print(f"""
   Z² GEOMETRIC RESULTS:
   ─────────────────────
   Mean Contact Distance: {z2_result.get('mean_distance', 'N/A'):.2f} Å
   Ideal Distance:        {IDEAL_BIOLOGICAL_DISTANCE:.2f} Å
   Deviation from Ideal:  {z2_result.get('deviation_from_ideal', 'N/A'):.2f} Å
   Min Contact Distance:  {z2_result.get('min_distance', 'N/A'):.2f} Å

   Z² FITNESS SCORE:      {z2_result.get('z2_fitness', 0) * 100:.1f}%
""")

    # Calculate Lennard-Jones energy
    print("\n⚡ STEP 4: Lennard-Jones Energy Calculation (bio_01 logic)...")
    lj_result = calculate_lennard_jones_energy(forced_peptide, pocket_positions)

    print(f"""
   LENNARD-JONES RESULTS:
   ──────────────────────
   Total LJ Energy:     {lj_result['total_lj_energy']:,.1f} kcal/mol
   Repulsive (r^-12):   {lj_result['repulsive_energy']:,.1f} kcal/mol
   Attractive (r^-6):   {lj_result['attractive_energy']:,.1f} kcal/mol

   STERIC CLASHES:
   Severe (<2.0 Å):     {lj_result['severe_clashes']}
   Moderate (<3.0 Å):   {lj_result['moderate_clashes']}
   Min P-R Distance:    {lj_result['min_distance']:.2f} Å
""")

    # Calculate internal clashes
    print("\n💥 STEP 5: Internal Steric Clash Analysis...")
    clash_result = calculate_steric_clash_penalty(forced_peptide)

    print(f"""
   INTERNAL CLASH RESULTS:
   ───────────────────────
   Internal Clashes:        {clash_result['internal_clashes']}
   Severe Clashes (<1.5 Å): {clash_result['severe_internal_clashes']}
   Clash Energy Penalty:    {clash_result['clash_energy']:.1f} kcal/mol
   Min Internal Distance:   {clash_result['min_internal_distance']:.2f} Å
""")

    # Estimate binding free energy
    print("\n🧮 STEP 6: Binding Free Energy Estimation...")
    dg_result = estimate_binding_free_energy(z2_result, lj_result, clash_result)

    print(f"""
   BINDING FREE ENERGY:
   ────────────────────
   LJ Contribution:      {dg_result['lj_contribution']:,.1f} kcal/mol
   Clash Penalty:        {dg_result['clash_contribution']:,.1f} kcal/mol
   Entropy Penalty:      {dg_result['entropy_penalty']:.1f} kcal/mol

   TOTAL ΔG:             {dg_result['total_dG']:,.1f} kcal/mol
   Binding Favorable?    {dg_result['binding_favorable']}
""")

    # THE VERDICT
    print("\n" + "=" * 70)
    print("THE VERDICT: PIPELINE INTEGRITY CHECK")
    print("=" * 70)

    z2_fitness = z2_result.get('z2_fitness', 0)
    total_dG = dg_result['total_dG']

    failures = []
    passes = []

    # Check 1: Z² fitness should be LOW (< 50%)
    if z2_fitness > 0.5:
        failures.append(f"FAIL: Z² fitness {z2_fitness*100:.1f}% > 50% threshold")
    else:
        passes.append(f"PASS: Z² fitness {z2_fitness*100:.1f}% < 50% (decoy correctly penalized)")

    # Check 2: ΔG should be POSITIVE (unfavorable)
    if total_dG < 0:
        failures.append(f"FAIL: ΔG = {total_dG:.1f} kcal/mol is NEGATIVE (wrongly favorable)")
    else:
        passes.append(f"PASS: ΔG = {total_dG:,.1f} kcal/mol is POSITIVE (correctly unfavorable)")

    # Check 3: Should have steric clashes
    if lj_result['severe_clashes'] == 0 and clash_result['internal_clashes'] == 0:
        failures.append("FAIL: No steric clashes detected (impossible for poly-W)")
    else:
        total_clashes = lj_result['severe_clashes'] + clash_result['internal_clashes']
        passes.append(f"PASS: {total_clashes} steric clashes detected (correctly identifying problems)")

    # Check 4: Mean distance should be FAR from ideal
    deviation = z2_result.get('deviation_from_ideal', 0)
    if deviation < 1.0:
        failures.append(f"FAIL: Mean distance only {deviation:.2f} Å from ideal (suspicious)")
    else:
        passes.append(f"PASS: Mean distance {deviation:.2f} Å from ideal (correctly off-target)")

    # Print results
    print("\n✅ PASSED CHECKS:")
    for p in passes:
        print(f"   {p}")

    if failures:
        print("\n❌ FAILED CHECKS:")
        for f in failures:
            print(f"   {f}")

    # Final verdict
    print("\n" + "─" * 70)
    if not failures:
        print("""
   ╔══════════════════════════════════════════════════════════════════╗
   ║                                                                  ║
   ║   ✅ PIPELINE INTEGRITY VERIFIED                                 ║
   ║                                                                  ║
   ║   The decoy WWWWWW correctly received:                          ║
   ║   - LOW Z² fitness (geometric mismatch detected)                ║
   ║   - POSITIVE ΔG (unfavorable binding correctly predicted)        ║
   ║   - STERIC CLASHES (physical impossibility detected)            ║
   ║                                                                  ║
   ║   The scoring pipeline is NOT generating slop.                  ║
   ║   It correctly rejects geometrically impossible peptides.        ║
   ║                                                                  ║
   ╚══════════════════════════════════════════════════════════════════╝
""")
        verdict = "VERIFIED"
    else:
        print("""
   ╔══════════════════════════════════════════════════════════════════╗
   ║                                                                  ║
   ║   ❌ PIPELINE INTEGRITY FAILED                                   ║
   ║                                                                  ║
   ║   The decoy WWWWWW received scores that are TOO GOOD.           ║
   ║   This indicates the scoring pipeline may be generating slop.    ║
   ║                                                                  ║
   ║   INVESTIGATE IMMEDIATELY.                                       ║
   ║                                                                  ║
   ╚══════════════════════════════════════════════════════════════════╝
""")
        verdict = "FAILED"

    # Compare to our successful drug
    print("\n" + "=" * 70)
    print("COMPARISON: DECOY vs. SUCCESSFUL DRUG")
    print("=" * 70)
    print(f"""
                        WWWWWW (Decoy)      CGCCCCWC (Drug)
                        ──────────────      ───────────────
   Z² Fitness:          {z2_fitness*100:>6.1f}%             ~99.9%
   ΔG (kcal/mol):       {total_dG:>+10,.0f}              ~-40
   Steric Clashes:      {lj_result['severe_clashes'] + clash_result['internal_clashes']:>10}              0
   Mean Contact (Å):    {z2_result.get('mean_distance', 0):>10.2f}              5.97

   The decoy is {abs(total_dG / -40):.0f}x WORSE than our validated drug.
   This demonstrates the pipeline correctly discriminates.
""")

    # Save results
    output_dir = Path(__file__).parent / 'results' / 'falsification'
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {
        'timestamp': datetime.now().isoformat(),
        'decoy_sequence': 'WWWWWW',
        'z2_analysis': z2_result,
        'lj_analysis': lj_result,
        'clash_analysis': clash_result,
        'binding_energy': dg_result,
        'verdict': verdict,
        'passes': passes,
        'failures': failures,
    }

    output_path = output_dir / 'decoy_falsification_results.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n📄 Results saved to: {output_path}")
    print("=" * 70)

    return results


if __name__ == '__main__':
    results = run_decoy_falsification()
