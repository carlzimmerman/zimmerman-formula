#!/usr/bin/env python3
"""
Test Dehydration Prediction: Does Z² Resonance Require Hydration?

SPDX-License-Identifier: AGPL-3.0-or-later

THE HYPOTHESIS:
Z² resonance in protein vibrational modes comes from water-protein coupling.
The hydration shell has collective modes at ~0.3 THz that couple to protein
normal modes, and this coupling is quantized by Z².

THE PREDICTION:
- HYDRATED protein → strong Z² resonance (p < 10⁻⁶)
- DEHYDRATED protein → weak or no Z² resonance (p > 0.05)

THE TEST:
1. Compute normal modes of protein WITH implicit solvation (effective mass)
2. Compute normal modes of protein WITHOUT solvation (vacuum)
3. Compare Z² alignment between conditions

METHODS:
- ANM (Anisotropic Network Model) for normal modes
- Implicit solvation: increase effective mass by hydration shell contribution
- Vacuum: use bare atomic masses

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# CONSTANTS
# ==============================================================================

Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
Z = np.sqrt(Z_SQUARED)       # ≈ 5.7888

# Z² harmonic frequencies (dimensionless, normalized to lowest mode)
def z2_harmonics(n_max: int = 20) -> np.ndarray:
    """Generate Z² harmonic series: f_n = n / Z²"""
    return np.array([n / Z_SQUARED for n in range(1, n_max + 1)])

# Hydration parameters
WATERS_PER_RESIDUE = 8.5  # Average hydration shell waters per residue
WATER_MASS_DA = 18.015    # Daltons
RESIDUE_MASS_DA = 110.0   # Average amino acid mass

# ==============================================================================
# PDB PARSING
# ==============================================================================

def fetch_pdb(pdb_id: str) -> str:
    """Fetch PDB file from RCSB."""
    import urllib.request
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {pdb_id}: {e}")
        return None

def parse_ca_coords(pdb_content: str) -> Tuple[np.ndarray, int]:
    """Extract Cα coordinates from PDB content."""
    coords = []
    for line in pdb_content.split('\n'):
        if line.startswith('ATOM') and line[12:16].strip() == 'CA':
            try:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                coords.append([x, y, z])
            except ValueError:
                pass
    return np.array(coords), len(coords)

# ==============================================================================
# ANISOTROPIC NETWORK MODEL
# ==============================================================================

def build_anm_hessian(coords: np.ndarray, cutoff: float = 15.0,
                       gamma: float = 1.0) -> np.ndarray:
    """
    Build the ANM Hessian matrix.

    H_ij = -γ × (r_ij ⊗ r_ij) / |r_ij|² for |r_ij| < cutoff
    """
    n_atoms = len(coords)
    n_dof = 3 * n_atoms
    H = np.zeros((n_dof, n_dof))

    for i in range(n_atoms):
        for j in range(i + 1, n_atoms):
            r_ij = coords[j] - coords[i]
            dist = np.linalg.norm(r_ij)

            if dist < cutoff:
                # Normalized direction
                r_hat = r_ij / dist

                # 3x3 block: -γ × (r̂ ⊗ r̂)
                block = -gamma * np.outer(r_hat, r_hat)

                # Off-diagonal blocks
                H[3*i:3*i+3, 3*j:3*j+3] = block
                H[3*j:3*j+3, 3*i:3*i+3] = block

                # Diagonal blocks (negative sum of off-diagonals)
                H[3*i:3*i+3, 3*i:3*i+3] -= block
                H[3*j:3*j+3, 3*j:3*j+3] -= block

    return H

def compute_normal_modes(H: np.ndarray, masses: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute normal mode frequencies from mass-weighted Hessian.

    Returns eigenvalues (ω²) and eigenvectors, sorted by frequency.
    """
    n_atoms = len(masses)

    # Build mass matrix M^(-1/2)
    M_inv_sqrt = np.zeros((3 * n_atoms, 3 * n_atoms))
    for i, m in enumerate(masses):
        for j in range(3):
            M_inv_sqrt[3*i + j, 3*i + j] = 1.0 / np.sqrt(m)

    # Mass-weighted Hessian: H_mw = M^(-1/2) H M^(-1/2)
    H_mw = M_inv_sqrt @ H @ M_inv_sqrt

    # Diagonalize
    eigenvalues, eigenvectors = np.linalg.eigh(H_mw)

    # Sort by eigenvalue (ascending)
    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Skip first 6 (translations + rotations)
    # Take positive eigenvalues only
    positive = eigenvalues > 1e-6
    eigenvalues = eigenvalues[positive]
    eigenvectors = eigenvectors[:, positive]

    # Skip trivial modes
    if len(eigenvalues) > 6:
        eigenvalues = eigenvalues[6:]
        eigenvectors = eigenvectors[:, 6:]

    return eigenvalues, eigenvectors

# ==============================================================================
# Z² ANALYSIS
# ==============================================================================

def analyze_z2_alignment(frequencies: np.ndarray, n_modes: int = 10) -> Dict[str, float]:
    """
    Analyze how well the lowest normal mode frequencies align with Z² harmonics.

    Returns alignment metrics.
    """
    # Normalize frequencies to lowest mode
    if len(frequencies) < n_modes:
        n_modes = len(frequencies)

    freqs = frequencies[:n_modes]
    freqs_normalized = freqs / freqs[0]  # Normalize to f_1 = 1

    # Z² harmonics normalized the same way
    z2_harm = z2_harmonics(n_modes)
    z2_normalized = z2_harm / z2_harm[0]  # Also normalize

    # For each mode, find closest Z² harmonic
    deviations = []
    for i, f in enumerate(freqs_normalized):
        # Distance to nearest Z² harmonic
        min_dev = np.min(np.abs(z2_normalized - f))
        deviations.append(min_dev)

    mean_deviation = np.mean(deviations)

    # Pearson correlation with mode index
    # If Z² scaling holds: f_n ∝ n means perfect linear correlation
    mode_indices = np.arange(1, n_modes + 1)
    r, p_value = stats.pearsonr(mode_indices, freqs_normalized)

    # Compare to random expectation
    # Random frequencies would have mean deviation ~0.25 (uniform on [0, 0.5])
    random_expectation = 0.25
    alignment_ratio = random_expectation / mean_deviation if mean_deviation > 0 else 0

    return {
        'n_modes_analyzed': n_modes,
        'mean_deviation': mean_deviation,
        'random_expectation': random_expectation,
        'alignment_ratio': alignment_ratio,
        'pearson_r': r,
        'p_value': p_value,
        'frequencies_normalized': freqs_normalized.tolist()
    }

# ==============================================================================
# HYDRATION CONDITIONS
# ==============================================================================

def get_masses_vacuum(n_residues: int) -> np.ndarray:
    """Get masses for vacuum (dehydrated) condition."""
    # Each Cα represents one residue with average mass
    return np.full(n_residues, RESIDUE_MASS_DA)

def get_masses_hydrated(n_residues: int) -> np.ndarray:
    """
    Get effective masses for hydrated condition.

    The hydration shell adds ~8.5 waters per residue that move with the protein.
    This increases the effective mass of protein motions.
    """
    # Effective mass = residue mass + hydration shell mass
    hydration_mass = WATERS_PER_RESIDUE * WATER_MASS_DA
    effective_mass = RESIDUE_MASS_DA + hydration_mass
    return np.full(n_residues, effective_mass)

def get_masses_partial_hydration(n_residues: int, hydration_fraction: float) -> np.ndarray:
    """Get masses for partial hydration (0 = vacuum, 1 = fully hydrated)."""
    hydration_mass = hydration_fraction * WATERS_PER_RESIDUE * WATER_MASS_DA
    effective_mass = RESIDUE_MASS_DA + hydration_mass
    return np.full(n_residues, effective_mass)

# ==============================================================================
# MAIN TEST
# ==============================================================================

def test_dehydration_prediction(pdb_id: str = "1UBQ") -> Dict[str, any]:
    """
    Test whether dehydration removes Z² resonance.

    Compare normal mode Z² alignment between:
    1. Vacuum (dehydrated)
    2. Fully hydrated
    3. Partial hydration levels
    """

    print(f"\n{'='*70}")
    print(f"TESTING DEHYDRATION PREDICTION: {pdb_id}")
    print(f"{'='*70}")

    # Fetch and parse structure
    print("\n1. Fetching structure...")
    pdb_content = fetch_pdb(pdb_id)
    if pdb_content is None:
        return {'error': f'Could not fetch {pdb_id}'}

    coords, n_residues = parse_ca_coords(pdb_content)
    print(f"   Parsed {n_residues} Cα atoms")

    # Build Hessian (same for both conditions - only masses change)
    print("\n2. Building ANM Hessian...")
    H = build_anm_hessian(coords, cutoff=15.0, gamma=1.0)
    print(f"   Hessian size: {H.shape}")

    results = {
        'pdb_id': pdb_id,
        'n_residues': n_residues,
        'timestamp': datetime.now().isoformat(),
        'conditions': {}
    }

    # Test different hydration levels
    hydration_levels = [0.0, 0.25, 0.5, 0.75, 1.0]

    print("\n3. Computing normal modes for each hydration level...")
    print("-" * 60)

    for h in hydration_levels:
        condition = f"hydration_{int(h*100)}pct"

        if h == 0.0:
            label = "VACUUM (dehydrated)"
            masses = get_masses_vacuum(n_residues)
        elif h == 1.0:
            label = "FULLY HYDRATED"
            masses = get_masses_hydrated(n_residues)
        else:
            label = f"{int(h*100)}% hydrated"
            masses = get_masses_partial_hydration(n_residues, h)

        # Compute modes
        eigenvalues, eigenvectors = compute_normal_modes(H, masses)
        frequencies = np.sqrt(np.abs(eigenvalues))  # ω = √(eigenvalue)

        # Analyze Z² alignment
        z2_analysis = analyze_z2_alignment(frequencies, n_modes=10)

        print(f"\n   {label}:")
        print(f"      Effective mass: {masses[0]:.1f} Da")
        print(f"      Mean Z² deviation: {z2_analysis['mean_deviation']:.4f}")
        print(f"      Alignment ratio: {z2_analysis['alignment_ratio']:.1f}×")
        print(f"      Pearson r: {z2_analysis['pearson_r']:.4f}")
        print(f"      p-value: {z2_analysis['p_value']:.2e}")

        results['conditions'][condition] = {
            'label': label,
            'hydration_fraction': h,
            'effective_mass': float(masses[0]),
            'n_modes': len(frequencies),
            'z2_analysis': z2_analysis
        }

    # Analyze trend
    print("\n" + "="*70)
    print("RESULTS ANALYSIS")
    print("="*70)

    vacuum = results['conditions']['hydration_0pct']
    hydrated = results['conditions']['hydration_100pct']

    vacuum_ratio = vacuum['z2_analysis']['alignment_ratio']
    hydrated_ratio = hydrated['z2_analysis']['alignment_ratio']

    vacuum_p = vacuum['z2_analysis']['p_value']
    hydrated_p = hydrated['z2_analysis']['p_value']

    print(f"\n   VACUUM (dehydrated):")
    print(f"      Z² alignment: {vacuum_ratio:.1f}× random")
    print(f"      p-value: {vacuum_p:.2e}")

    print(f"\n   FULLY HYDRATED:")
    print(f"      Z² alignment: {hydrated_ratio:.1f}× random")
    print(f"      p-value: {hydrated_p:.2e}")

    # Determine verdict
    print("\n" + "="*70)
    print("PREDICTION TEST")
    print("="*70)

    prediction_text = """
    HYPOTHESIS: Z² resonance requires hydration shell coupling

    PREDICTION:
    - Hydrated → strong Z² resonance (alignment >> 1, p < 0.01)
    - Dehydrated → weak/no Z² resonance (alignment ~ 1, p > 0.05)
    """
    print(prediction_text)

    # Check if prediction holds
    hydrated_has_z2 = hydrated_ratio > 5 and hydrated_p < 0.01
    vacuum_lacks_z2 = vacuum_ratio < 5 or vacuum_p > 0.01

    if hydrated_has_z2 and vacuum_lacks_z2:
        verdict = "PREDICTION_CONFIRMED"
        verdict_text = """
    *** PREDICTION CONFIRMED ***

    Hydration DOES affect Z² resonance!
    - Hydrated protein shows strong Z² alignment
    - Dehydrated protein shows weaker alignment

    This supports the hydration shell resonance hypothesis:
    Z² emerges from water-protein coupling.
        """
    elif hydrated_has_z2 and not vacuum_lacks_z2:
        verdict = "PREDICTION_REFUTED"
        verdict_text = """
    *** PREDICTION REFUTED ***

    Both conditions show Z² resonance!
    - Hydrated AND dehydrated proteins align with Z² harmonics

    This suggests Z² is INTRINSIC to protein geometry,
    not dependent on hydration shell.
        """
    elif not hydrated_has_z2:
        verdict = "INCONCLUSIVE"
        verdict_text = """
    *** INCONCLUSIVE ***

    Even hydrated protein doesn't show strong Z² resonance.
    Need to check analysis method or try different protein.
        """
    else:
        verdict = "PARTIAL"
        verdict_text = """
    *** PARTIAL SUPPORT ***

    Mixed results. Hydration affects Z² resonance but
    the effect is not as strong as predicted.
        """

    print(verdict_text)

    results['verdict'] = verdict
    results['hydrated_has_z2'] = hydrated_has_z2
    results['vacuum_lacks_z2'] = vacuum_lacks_z2
    results['hydration_effect'] = hydrated_ratio / vacuum_ratio if vacuum_ratio > 0 else float('inf')

    return results


def run_multi_protein_test(pdb_ids: List[str] = None) -> Dict[str, any]:
    """Test dehydration prediction on multiple proteins."""

    if pdb_ids is None:
        pdb_ids = ["1UBQ", "1LYZ", "5PTI", "1MBN"]

    print("\n" + "="*70)
    print("MULTI-PROTEIN DEHYDRATION TEST")
    print("="*70)

    all_results = {
        'timestamp': datetime.now().isoformat(),
        'proteins': {},
        'summary': {}
    }

    for pdb_id in pdb_ids:
        result = test_dehydration_prediction(pdb_id)
        all_results['proteins'][pdb_id] = result

    # Summarize across proteins
    verdicts = [r['verdict'] for r in all_results['proteins'].values() if 'verdict' in r]

    print("\n" + "="*70)
    print("MULTI-PROTEIN SUMMARY")
    print("="*70)

    print(f"\nProteins tested: {len(pdb_ids)}")
    print(f"Verdicts: {verdicts}")

    if all(v == "PREDICTION_CONFIRMED" for v in verdicts):
        overall = "STRONG_SUPPORT"
        print("\n*** STRONG SUPPORT FOR HYDRATION HYPOTHESIS ***")
    elif all(v == "PREDICTION_REFUTED" for v in verdicts):
        overall = "REFUTED"
        print("\n*** HYPOTHESIS REFUTED - Z² IS INTRINSIC ***")
    else:
        overall = "MIXED"
        print("\n*** MIXED RESULTS - NEEDS MORE INVESTIGATION ***")

    all_results['summary']['overall_verdict'] = overall
    all_results['summary']['verdicts'] = verdicts

    # Save results
    output_path = 'extended_research/biotech/hybrid_z2_test/dehydration_test_results.json'
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\nResults saved to: {output_path}")

    return all_results


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == '__main__':
    # Run multi-protein test
    results = run_multi_protein_test(["1UBQ", "1LYZ", "5PTI", "1MBN"])
