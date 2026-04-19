#!/usr/bin/env python3
"""
Batch Z² Alignment Test - Multi-Protein Analysis

SPDX-License-Identifier: AGPL-3.0-or-later

Tests multiple proteins to determine if Z² alignment pattern is universal.

Author: Carl Zimmerman
Date: April 2026
"""

import os
import sys
import json
import time
import requests
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.7888
Z2 = Z ** 2  # ≈ 33.51
THETA_Z2 = np.pi / Z  # ≈ 0.5427 rad ≈ 31.09°
THETA_Z2_DEG = np.degrees(THETA_Z2)
F_Z2 = 1.0 / Z2
Z2_HARMONICS = [n * F_Z2 for n in range(1, 20)]

# ==============================================================================
# PDB FETCHING
# ==============================================================================

PDB_API_URL = "https://files.rcsb.org/download/{}.pdb"

def fetch_pdb(pdb_id: str, output_dir: str) -> str:
    """Fetch PDB with rate limiting."""
    time.sleep(0.5)  # Polite rate limiting

    pdb_id = pdb_id.upper()
    url = PDB_API_URL.format(pdb_id)

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    os.makedirs(output_dir, exist_ok=True)
    pdb_path = os.path.join(output_dir, f"{pdb_id}.pdb")

    with open(pdb_path, 'w') as f:
        f.write(response.text)

    return pdb_path

# ==============================================================================
# BACKBONE ANGLE ANALYSIS
# ==============================================================================

def parse_ca_coords(pdb_path: str) -> Tuple[np.ndarray, List[str]]:
    """Parse CA coordinates from PDB file."""
    coords = []
    residues = []

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM') and line[12:16].strip() == 'CA':
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    resname = line[17:20].strip()

                    coords.append([x, y, z])
                    residues.append(resname)
                except ValueError:
                    pass

    return np.array(coords), residues

def calculate_dihedral(p1, p2, p3, p4):
    """Calculate dihedral angle between 4 points."""
    b1 = p2 - p1
    b2 = p3 - p2
    b3 = p4 - p3

    n1 = np.cross(b1, b2)
    n2 = np.cross(b2, b3)

    n1_norm = np.linalg.norm(n1)
    n2_norm = np.linalg.norm(n2)

    if n1_norm < 1e-10 or n2_norm < 1e-10:
        return None

    n1 = n1 / n1_norm
    n2 = n2 / n2_norm

    m1 = np.cross(n1, b2 / np.linalg.norm(b2))

    x = np.dot(n1, n2)
    y = np.dot(m1, n2)

    return np.arctan2(y, x)

def analyze_backbone_angles(pdb_path: str) -> Dict:
    """Analyze backbone pseudo-dihedral angles for Z² alignment."""
    coords, residues = parse_ca_coords(pdb_path)
    n = len(coords)

    if n < 4:
        return {'error': 'Too few residues'}

    # Calculate pseudo-dihedral angles (CA trace)
    angles = []
    for i in range(n - 3):
        angle = calculate_dihedral(coords[i], coords[i+1], coords[i+2], coords[i+3])
        if angle is not None:
            angles.append(np.degrees(angle))

    angles = np.array(angles)

    # Z² alignment analysis
    z2_deviations = []
    for angle in angles:
        angle_mod = abs(angle) % THETA_Z2_DEG
        deviation = min(angle_mod, THETA_Z2_DEG - angle_mod)
        z2_deviations.append(deviation)

    mean_z2_deviation = np.mean(z2_deviations)
    random_expected = THETA_Z2_DEG / 4  # ~7.77°
    alignment_ratio = random_expected / mean_z2_deviation if mean_z2_deviation > 0 else 0

    # Verdict
    if alignment_ratio > 1.5:
        verdict = 'ALIGNED'
    elif alignment_ratio > 1.1:
        verdict = 'MARGINAL'
    else:
        verdict = 'NO_ALIGNMENT'

    return {
        'n_residues': n,
        'n_angles': len(angles),
        'mean_angle': float(np.mean(np.abs(angles))),
        'std_angle': float(np.std(angles)),
        'mean_z2_deviation': float(mean_z2_deviation),
        'random_expected': float(random_expected),
        'alignment_ratio': float(alignment_ratio),
        'verdict': verdict
    }

# ==============================================================================
# NORMAL MODE ANALYSIS
# ==============================================================================

def build_anm_hessian(coords: np.ndarray, cutoff: float = 15.0) -> np.ndarray:
    """Build ANM Hessian matrix."""
    n = len(coords)
    hessian = np.zeros((3*n, 3*n))

    for i in range(n):
        for j in range(i+1, n):
            r_vec = coords[j] - coords[i]
            r_mag = np.linalg.norm(r_vec)

            if r_mag < cutoff:
                r_hat = r_vec / r_mag
                sub_block = np.outer(r_hat, r_hat)

                hessian[3*i:3*i+3, 3*j:3*j+3] = -sub_block
                hessian[3*j:3*j+3, 3*i:3*i+3] = -sub_block
                hessian[3*i:3*i+3, 3*i:3*i+3] += sub_block
                hessian[3*j:3*j+3, 3*j:3*j+3] += sub_block

    return hessian

def analyze_normal_modes(pdb_path: str, n_modes: int = 20) -> Dict:
    """Calculate and analyze normal modes for Z² resonance."""
    coords, _ = parse_ca_coords(pdb_path)
    n = len(coords)

    if n < 10:
        return {'error': 'Too few residues for ANM'}

    # Build and diagonalize Hessian
    hessian = build_anm_hessian(coords)
    eigenvalues, _ = np.linalg.eigh(hessian)

    # Skip 6 trivial modes, get frequencies
    start_idx = 6
    end_idx = min(start_idx + n_modes, len(eigenvalues))
    modes_eigenvalues = eigenvalues[start_idx:end_idx]
    frequencies = np.sqrt(np.abs(modes_eigenvalues))

    # Normalize frequencies
    freq_norm = frequencies / np.max(frequencies) if np.max(frequencies) > 0 else frequencies

    # Z² resonance analysis
    z2_harmonics_norm = np.array(Z2_HARMONICS[:20]) / np.max(Z2_HARMONICS[:20])

    deviations = []
    for f in freq_norm:
        dists = np.abs(z2_harmonics_norm - f)
        min_dist = np.min(dists)
        nearest_idx = np.argmin(dists)
        deviations.append({
            'freq': float(f),
            'nearest_z2': float(z2_harmonics_norm[nearest_idx]),
            'deviation': float(min_dist),
            'harmonic_n': int(nearest_idx + 1)
        })

    mean_deviation = np.mean([d['deviation'] for d in deviations])
    random_expected = 0.25

    # Quantization test
    z2_multiples = freq_norm * Z2
    int_deviations = np.abs(z2_multiples - np.round(z2_multiples))
    mean_int_dev = np.mean(int_deviations)

    # Correlation test
    mode_indices = np.arange(1, len(freq_norm) + 1)
    if len(freq_norm) >= 5:
        correlation, p_value = stats.pearsonr(mode_indices[:10], freq_norm[:10])
    else:
        correlation, p_value = 0, 1

    # Verdict
    proximity_pass = mean_deviation < random_expected * 0.7
    quantization_pass = mean_int_dev < 0.25

    if proximity_pass or quantization_pass:
        verdict = 'Z2_RESONANCE_DETECTED'
    else:
        verdict = 'NO_Z2_RESONANCE'

    return {
        'n_modes': len(frequencies),
        'frequencies': frequencies.tolist(),
        'mean_z2_deviation': float(mean_deviation),
        'random_expected': float(random_expected),
        'proximity_test': 'ALIGNED' if proximity_pass else 'NO_ALIGNMENT',
        'quantization_test': 'QUANTIZED' if quantization_pass else 'NOT_QUANTIZED',
        'mean_quantization_error': float(mean_int_dev),
        'pearson_r': float(correlation),
        'p_value': float(p_value),
        'mode_analysis': deviations[:10],
        'verdict': verdict
    }

# ==============================================================================
# COMPLETE PROTEIN ANALYSIS
# ==============================================================================

def analyze_protein(pdb_id: str, output_dir: str) -> Dict:
    """Run complete Z² analysis on a protein."""
    print(f"\n{'='*70}")
    print(f"ANALYZING: {pdb_id}")
    print(f"{'='*70}")

    results = {
        'pdb_id': pdb_id.upper(),
        'Z': float(Z),
        'Z2': float(Z2),
        'theta_Z2_deg': float(THETA_Z2_DEG),
        'timestamp': datetime.now().isoformat(),
        'license': 'AGPL-3.0-or-later'
    }

    # Fetch PDB
    try:
        print(f"  Fetching {pdb_id}...")
        pdb_path = fetch_pdb(pdb_id, output_dir)
        print(f"  Downloaded: {pdb_path}")
    except Exception as e:
        print(f"  ERROR fetching {pdb_id}: {e}")
        return {'pdb_id': pdb_id, 'error': str(e)}

    # Backbone angle analysis
    print(f"  Running backbone angle analysis...")
    backbone = analyze_backbone_angles(pdb_path)
    results['backbone_analysis'] = backbone
    print(f"    Residues: {backbone.get('n_residues', 'N/A')}")
    print(f"    Mean Z² deviation: {backbone.get('mean_z2_deviation', 'N/A'):.2f}°")
    print(f"    Alignment ratio: {backbone.get('alignment_ratio', 'N/A'):.2f}x")
    print(f"    Verdict: {backbone.get('verdict', 'N/A')}")

    # Normal mode analysis
    print(f"  Running normal mode analysis...")
    modes = analyze_normal_modes(pdb_path)
    results['normal_modes'] = modes
    print(f"    Modes: {modes.get('n_modes', 'N/A')}")
    print(f"    Mean Z² deviation: {modes.get('mean_z2_deviation', 'N/A'):.4f}")
    print(f"    Proximity test: {modes.get('proximity_test', 'N/A')}")
    print(f"    Quantization test: {modes.get('quantization_test', 'N/A')}")
    print(f"    Pearson r: {modes.get('pearson_r', 'N/A'):.4f}")
    print(f"    p-value: {modes.get('p_value', 'N/A'):.2e}")
    print(f"    Verdict: {modes.get('verdict', 'N/A')}")

    # Combined verdict
    backbone_aligned = backbone.get('verdict') in ['ALIGNED', 'MARGINAL']
    modes_aligned = modes.get('verdict') == 'Z2_RESONANCE_DETECTED'

    if modes_aligned and backbone_aligned:
        results['combined_verdict'] = 'STRONG_Z2_ALIGNMENT'
    elif modes_aligned:
        results['combined_verdict'] = 'DYNAMICS_ONLY_Z2'
    elif backbone_aligned:
        results['combined_verdict'] = 'STRUCTURE_ONLY_Z2'
    else:
        results['combined_verdict'] = 'NO_Z2_ALIGNMENT'

    print(f"\n  COMBINED VERDICT: {results['combined_verdict']}")

    # Save individual results
    results_file = os.path.join(output_dir, f"{pdb_id.upper()}_z2_analysis.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"  Results saved: {results_file}")

    return results

# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Run batch Z² analysis on multiple proteins."""
    print("="*70)
    print("BATCH Z² ALIGNMENT TEST")
    print("="*70)
    print(f"Z = {Z:.6f}")
    print(f"Z² = {Z2:.6f}")
    print(f"θ_Z² = {THETA_Z2_DEG:.2f}°")
    print("="*70)

    # Test proteins
    proteins = sys.argv[1:] if len(sys.argv) > 1 else ['1LYZ', '5PTI', '1MBN']

    output_dir = 'hybrid_z2_test'
    os.makedirs(output_dir, exist_ok=True)

    all_results = []

    for pdb_id in proteins:
        try:
            results = analyze_protein(pdb_id, output_dir)
            all_results.append(results)
        except Exception as e:
            print(f"\nERROR analyzing {pdb_id}: {e}")
            import traceback
            traceback.print_exc()
            all_results.append({'pdb_id': pdb_id, 'error': str(e)})

    # Summary
    print("\n" + "="*70)
    print("MULTI-PROTEIN SUMMARY")
    print("="*70)

    print(f"\n{'Protein':<10} {'Residues':<10} {'Backbone':<15} {'Modes':<20} {'Combined':<20}")
    print("-"*75)

    for r in all_results:
        if 'error' in r:
            print(f"{r['pdb_id']:<10} ERROR: {r['error']}")
            continue

        backbone = r.get('backbone_analysis', {})
        modes = r.get('normal_modes', {})

        print(f"{r['pdb_id']:<10} "
              f"{backbone.get('n_residues', 'N/A'):<10} "
              f"{backbone.get('verdict', 'N/A'):<15} "
              f"{modes.get('verdict', 'N/A'):<20} "
              f"{r.get('combined_verdict', 'N/A'):<20}")

    # Statistical summary
    backbone_verdicts = [r.get('backbone_analysis', {}).get('verdict') for r in all_results if 'error' not in r]
    modes_verdicts = [r.get('normal_modes', {}).get('verdict') for r in all_results if 'error' not in r]

    backbone_aligned = sum(1 for v in backbone_verdicts if v in ['ALIGNED', 'MARGINAL'])
    modes_aligned = sum(1 for v in modes_verdicts if v == 'Z2_RESONANCE_DETECTED')

    print(f"\n  Backbone Z² alignment: {backbone_aligned}/{len(backbone_verdicts)} proteins")
    print(f"  Normal mode Z² resonance: {modes_aligned}/{len(modes_verdicts)} proteins")

    # Pattern check
    if modes_aligned == len(modes_verdicts) and backbone_aligned < len(backbone_verdicts) / 2:
        print("\n  *** PATTERN CONFIRMED: Z² governs DYNAMICS, not STATICS ***")
    elif modes_aligned == len(modes_verdicts) and backbone_aligned == len(backbone_verdicts):
        print("\n  *** STRONG Z² ALIGNMENT in both structure and dynamics ***")
    elif modes_aligned == 0:
        print("\n  No evidence for Z² alignment in protein physics")

    # Save combined results
    combined_file = os.path.join(output_dir, 'batch_z2_results.json')
    with open(combined_file, 'w') as f:
        json.dump({
            'proteins': all_results,
            'summary': {
                'backbone_aligned': backbone_aligned,
                'modes_aligned': modes_aligned,
                'total': len(all_results)
            },
            'timestamp': datetime.now().isoformat()
        }, f, indent=2, default=str)

    print(f"\n  Combined results: {combined_file}")

    return all_results

if __name__ == '__main__':
    main()
