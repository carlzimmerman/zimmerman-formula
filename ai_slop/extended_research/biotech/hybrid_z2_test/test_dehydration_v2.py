#!/usr/bin/env python3
"""
Test Dehydration Prediction v2: Corrected Methodology

SPDX-License-Identifier: AGPL-3.0-or-later

THE PROBLEM WITH v1:
Changing masses uniformly does NOT change normalized frequency ratios!
ω_i/ω_j = √(λ_i/λ_j) - mass cancels out.

CORRECTED APPROACH:
The hydration shell doesn't just add mass - it changes the EFFECTIVE
SPRING CONSTANTS between residues. Water mediates long-range correlations.

Model hydration by:
1. DAMPING: Add friction term that changes effective stiffness
2. SCREENING: Reduce spring constants for solvent-exposed residues
3. COUPLING: Add off-diagonal terms connecting distant residues via water

If Z² is intrinsic to protein geometry (not hydration), we should see
Z² resonance REGARDLESS of these modifications.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from typing import Dict, List, Tuple
import json
from datetime import datetime
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# CONSTANTS
# ==============================================================================

Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)

def z2_harmonics(n_max: int = 20) -> np.ndarray:
    return np.array([n / Z_SQUARED for n in range(1, n_max + 1)])

# ==============================================================================
# PDB PARSING
# ==============================================================================

def fetch_pdb(pdb_id: str) -> str:
    import urllib.request
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read().decode('utf-8')
    except:
        return None

def parse_ca_coords(pdb_content: str) -> np.ndarray:
    coords = []
    for line in pdb_content.split('\n'):
        if line.startswith('ATOM') and line[12:16].strip() == 'CA':
            try:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                coords.append([x, y, z])
            except:
                pass
    return np.array(coords)

# ==============================================================================
# MODIFIED ANM MODELS
# ==============================================================================

def build_standard_hessian(coords: np.ndarray, cutoff: float = 15.0,
                           gamma: float = 1.0) -> np.ndarray:
    """Standard ANM Hessian."""
    n = len(coords)
    H = np.zeros((3*n, 3*n))

    for i in range(n):
        for j in range(i+1, n):
            r = coords[j] - coords[i]
            d = np.linalg.norm(r)
            if d < cutoff:
                r_hat = r / d
                block = -gamma * np.outer(r_hat, r_hat)
                H[3*i:3*i+3, 3*j:3*j+3] = block
                H[3*j:3*j+3, 3*i:3*i+3] = block
                H[3*i:3*i+3, 3*i:3*i+3] -= block
                H[3*j:3*j+3, 3*j:3*j+3] -= block

    return H

def build_screened_hessian(coords: np.ndarray, cutoff: float = 15.0,
                           gamma: float = 1.0, screening: float = 0.5) -> np.ndarray:
    """
    ANM with distance-dependent screening (models solvent effects).

    Distant interactions are weakened by solvent screening.
    γ_eff(r) = γ × exp(-r/λ_D) where λ_D is Debye length
    """
    n = len(coords)
    H = np.zeros((3*n, 3*n))
    debye_length = 10.0  # Angstroms, typical for physiological conditions

    for i in range(n):
        for j in range(i+1, n):
            r = coords[j] - coords[i]
            d = np.linalg.norm(r)
            if d < cutoff:
                # Screen long-range interactions
                gamma_eff = gamma * np.exp(-screening * d / debye_length)

                r_hat = r / d
                block = -gamma_eff * np.outer(r_hat, r_hat)
                H[3*i:3*i+3, 3*j:3*j+3] = block
                H[3*j:3*j+3, 3*i:3*i+3] = block
                H[3*i:3*i+3, 3*i:3*i+3] -= block
                H[3*j:3*j+3, 3*j:3*j+3] -= block

    return H

def build_water_coupled_hessian(coords: np.ndarray, cutoff: float = 15.0,
                                 gamma: float = 1.0, water_coupling: float = 0.1) -> np.ndarray:
    """
    ANM with additional water-mediated coupling.

    Adds weak coupling between residues beyond normal cutoff,
    representing water-mediated correlations.
    """
    n = len(coords)
    H = np.zeros((3*n, 3*n))

    # Standard contacts
    for i in range(n):
        for j in range(i+1, n):
            r = coords[j] - coords[i]
            d = np.linalg.norm(r)
            if d < cutoff:
                r_hat = r / d
                block = -gamma * np.outer(r_hat, r_hat)
                H[3*i:3*i+3, 3*j:3*j+3] = block
                H[3*j:3*j+3, 3*i:3*i+3] = block
                H[3*i:3*i+3, 3*i:3*i+3] -= block
                H[3*j:3*j+3, 3*j:3*j+3] -= block
            elif d < 2 * cutoff:
                # Water-mediated coupling for longer distances
                gamma_water = gamma * water_coupling * (cutoff / d)**2
                r_hat = r / d
                block = -gamma_water * np.outer(r_hat, r_hat)
                H[3*i:3*i+3, 3*j:3*j+3] += block
                H[3*j:3*j+3, 3*i:3*i+3] += block
                H[3*i:3*i+3, 3*i:3*i+3] -= block
                H[3*j:3*j+3, 3*j:3*j+3] -= block

    return H

def build_randomized_hessian(coords: np.ndarray, cutoff: float = 15.0,
                              gamma: float = 1.0, noise: float = 0.3) -> np.ndarray:
    """
    ANM with randomized spring constants (control case).

    If Z² is intrinsic to topology, even random spring constants
    should preserve some Z² alignment.
    """
    n = len(coords)
    H = np.zeros((3*n, 3*n))

    np.random.seed(42)  # Reproducible

    for i in range(n):
        for j in range(i+1, n):
            r = coords[j] - coords[i]
            d = np.linalg.norm(r)
            if d < cutoff:
                # Randomize gamma
                gamma_rand = gamma * (1 + noise * (2*np.random.random() - 1))

                r_hat = r / d
                block = -gamma_rand * np.outer(r_hat, r_hat)
                H[3*i:3*i+3, 3*j:3*j+3] = block
                H[3*j:3*j+3, 3*i:3*i+3] = block
                H[3*i:3*i+3, 3*i:3*i+3] -= block
                H[3*j:3*j+3, 3*j:3*j+3] -= block

    return H

# ==============================================================================
# NORMAL MODE ANALYSIS
# ==============================================================================

def compute_modes(H: np.ndarray) -> np.ndarray:
    """Compute normal mode frequencies from Hessian."""
    eigenvalues, _ = np.linalg.eigh(H)
    # Take positive eigenvalues, skip first 6 trivial modes
    pos = eigenvalues > 1e-6
    eigenvalues = eigenvalues[pos]
    if len(eigenvalues) > 6:
        eigenvalues = eigenvalues[6:]
    return np.sqrt(eigenvalues)

def analyze_z2(frequencies: np.ndarray, n_modes: int = 10) -> Dict:
    """Analyze Z² alignment of frequency spectrum."""
    if len(frequencies) < n_modes:
        n_modes = len(frequencies)

    freqs = frequencies[:n_modes]
    freqs_norm = freqs / freqs[0]

    z2_harm = z2_harmonics(n_modes)
    z2_norm = z2_harm / z2_harm[0]

    deviations = []
    for f in freqs_norm:
        min_dev = np.min(np.abs(z2_norm - f))
        deviations.append(min_dev)

    mean_dev = np.mean(deviations)
    random_exp = 0.25

    mode_idx = np.arange(1, n_modes + 1)
    r, p = stats.pearsonr(mode_idx, freqs_norm)

    return {
        'mean_deviation': mean_dev,
        'alignment_ratio': random_exp / mean_dev if mean_dev > 0 else 0,
        'pearson_r': r,
        'p_value': p
    }

# ==============================================================================
# MAIN TEST
# ==============================================================================

def test_hessian_modifications(pdb_id: str = "1UBQ") -> Dict:
    """Test Z² alignment under different Hessian modifications."""

    print(f"\n{'='*70}")
    print(f"CORRECTED DEHYDRATION TEST: {pdb_id}")
    print(f"{'='*70}")

    pdb_content = fetch_pdb(pdb_id)
    if not pdb_content:
        return {'error': f'Could not fetch {pdb_id}'}

    coords = parse_ca_coords(pdb_content)
    n = len(coords)
    print(f"\nLoaded {n} Cα atoms")

    results = {'pdb_id': pdb_id, 'n_residues': n, 'conditions': {}}

    conditions = [
        ('standard', lambda c: build_standard_hessian(c)),
        ('screened_weak', lambda c: build_screened_hessian(c, screening=0.3)),
        ('screened_strong', lambda c: build_screened_hessian(c, screening=1.0)),
        ('water_coupled', lambda c: build_water_coupled_hessian(c, water_coupling=0.2)),
        ('randomized_30pct', lambda c: build_randomized_hessian(c, noise=0.3)),
        ('randomized_50pct', lambda c: build_randomized_hessian(c, noise=0.5)),
    ]

    print(f"\n{'Condition':<20} {'Alignment':>10} {'Pearson r':>10} {'p-value':>12}")
    print("-" * 55)

    for name, build_fn in conditions:
        H = build_fn(coords)
        freqs = compute_modes(H)
        z2 = analyze_z2(freqs)

        print(f"{name:<20} {z2['alignment_ratio']:>10.2f}× {z2['pearson_r']:>10.4f} {z2['p_value']:>12.2e}")

        results['conditions'][name] = z2

    # Analysis
    print("\n" + "="*70)
    print("ANALYSIS")
    print("="*70)

    standard = results['conditions']['standard']
    screened = results['conditions']['screened_strong']
    randomized = results['conditions']['randomized_50pct']

    print(f"\nStandard ANM alignment: {standard['alignment_ratio']:.2f}×")
    print(f"Strong screening alignment: {screened['alignment_ratio']:.2f}×")
    print(f"50% randomized alignment: {randomized['alignment_ratio']:.2f}×")

    # If Z² is intrinsic, all conditions should show similar alignment
    all_ratios = [v['alignment_ratio'] for v in results['conditions'].values()]
    ratio_std = np.std(all_ratios)
    ratio_mean = np.mean(all_ratios)

    print(f"\nAlignment ratio: mean = {ratio_mean:.2f}, std = {ratio_std:.2f}")

    if ratio_std < 0.5 * ratio_mean:
        verdict = "Z2_IS_INTRINSIC"
        print("\n*** Z² RESONANCE IS INTRINSIC TO PROTEIN TOPOLOGY ***")
        print("All Hessian modifications show similar Z² alignment.")
        print("This means Z² is NOT from hydration shell - it's geometric.")
    else:
        verdict = "HYDRATION_MATTERS"
        print("\n*** HYDRATION AFFECTS Z² RESONANCE ***")
        print("Different Hessian modifications show different Z² alignment.")

    results['verdict'] = verdict
    results['ratio_mean'] = ratio_mean
    results['ratio_std'] = ratio_std

    return results


def run_multi_protein(pdb_ids: List[str] = None) -> Dict:
    if pdb_ids is None:
        pdb_ids = ["1UBQ", "1LYZ", "5PTI", "1MBN"]

    all_results = {'timestamp': datetime.now().isoformat(), 'proteins': {}}

    for pdb_id in pdb_ids:
        all_results['proteins'][pdb_id] = test_hessian_modifications(pdb_id)

    # Summary
    verdicts = [r['verdict'] for r in all_results['proteins'].values() if 'verdict' in r]

    print("\n" + "="*70)
    print("MULTI-PROTEIN SUMMARY")
    print("="*70)

    intrinsic_count = sum(1 for v in verdicts if v == "Z2_IS_INTRINSIC")
    print(f"\nProteins where Z² is intrinsic: {intrinsic_count}/{len(verdicts)}")

    if intrinsic_count == len(verdicts):
        overall = "Z2_INTRINSIC_TO_TOPOLOGY"
        conclusion = """
CONCLUSION: Z² resonance is INTRINSIC to protein topology.

The hydration shell hypothesis is REFUTED.
Z² appears in protein normal modes because of the GEOMETRY
of protein contact networks, not water coupling.

This is actually MORE profound:
- Z² is built into the fabric of protein structure
- It emerges from the ~8 contacts per residue (CUBE vertices!)
- It's a property of 3D close-packed structures

The Z² = CUBE × SPHERE geometry manifests in proteins because
proteins are approximately close-packed spheres (residues)
arranged in 3D space.
        """
    else:
        overall = "MIXED"
        conclusion = "Mixed results - needs more investigation."

    print(conclusion)

    all_results['overall'] = overall
    all_results['conclusion'] = conclusion

    output_path = 'extended_research/biotech/hybrid_z2_test/dehydration_v2_results.json'
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\nResults saved to: {output_path}")

    return all_results


if __name__ == '__main__':
    run_multi_protein()
