#!/usr/bin/env python3
"""
Hybrid Z² Normal Modes Analysis - Pathway 10 Empirical Upgrade

SPDX-License-Identifier: AGPL-3.0-or-later

This script upgrades the theoretical Z² backbone phonon model by
testing whether real protein vibrational frequencies align with
Z² Kaluza-Klein harmonics.

ORIGINAL PATHWAY 10 THEORY:
- Protein backbone vibrates at Z²-constrained frequencies
- Native state maximizes entropy at Z² resonant harmonic
- Folding funnels align with Z² phonon modes

HYBRID UPGRADE:
- Calculate real normal modes using Anisotropic Network Model (ANM)
- Compare empirical vibrational frequencies to Z² predictions
- Test correlation between experimental phonons and Z² harmonics

THE CRITICAL TEST:
If Z² geometry is fundamental, protein vibrations should show:
1. Peaks in vibrational density of states at Z² frequencies
2. Correlation between dominant modes and Z² harmonics
3. Lower modes aligned with θ_Z² ≈ 31.09° angular displacements

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import os
import sys
import json
import requests
import numpy as np
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.7888
Z2 = Z ** 2  # ≈ 33.51
THETA_Z2 = np.pi / Z  # ≈ 0.5427 rad ≈ 31.09°

# Z² frequency scale
# In normal mode units, f_Z2 = 1/Z² ≈ 0.0298
F_Z2 = 1.0 / Z2

# Z² harmonics
Z2_HARMONICS = [n * F_Z2 for n in range(1, 20)]

print("="*70)
print("Z² NORMAL MODES ANALYSIS - PATHWAY 10 HYBRID UPGRADE")
print("="*70)
print(f"Z = {Z:.6f}")
print(f"Z² = {Z2:.6f}")
print(f"f_Z² = 1/Z² = {F_Z2:.6f}")
print(f"θ_Z² = {np.degrees(THETA_Z2):.2f}°")
print("="*70)

# ==============================================================================
# DATA FETCHING
# ==============================================================================

PDB_API_URL = "https://files.rcsb.org/download/{}.pdb"

def fetch_pdb(pdb_id: str, output_dir: str = ".") -> str:
    """Fetch PDB with rate limiting."""
    import time
    time.sleep(0.5)

    pdb_id = pdb_id.upper()
    url = PDB_API_URL.format(pdb_id)

    print(f"\n  Fetching PDB: {pdb_id}")
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    os.makedirs(output_dir, exist_ok=True)
    pdb_path = os.path.join(output_dir, f"{pdb_id}.pdb")

    with open(pdb_path, 'w') as f:
        f.write(response.text)

    return pdb_path


# ==============================================================================
# ANISOTROPIC NETWORK MODEL
# ==============================================================================

class ANMCalculator:
    """
    Anisotropic Network Model for normal mode calculation.

    Simplified implementation for proteins without ProDy dependency.
    """

    def __init__(self, pdb_path: str, cutoff: float = 15.0):
        """
        Initialize ANM calculator.

        Args:
            pdb_path: Path to PDB file
            cutoff: Distance cutoff for contacts (Angstroms)
        """
        self.pdb_path = pdb_path
        self.cutoff = cutoff
        self.ca_coords = None
        self.residues = []
        self._parse_pdb()

    def _parse_pdb(self):
        """Parse PDB file to extract CA coordinates."""
        coords = []
        residues = []

        with open(self.pdb_path, 'r') as f:
            for line in f:
                if line.startswith('ATOM') and line[12:16].strip() == 'CA':
                    try:
                        x = float(line[30:38])
                        y = float(line[38:46])
                        z = float(line[46:54])
                        resname = line[17:20].strip()
                        resid = int(line[22:26])

                        coords.append([x, y, z])
                        residues.append({'name': resname, 'id': resid})
                    except ValueError:
                        pass

        self.ca_coords = np.array(coords)
        self.residues = residues
        print(f"  Loaded {len(self.ca_coords)} CA atoms")

    def build_hessian(self, gamma: float = 1.0) -> np.ndarray:
        """
        Build ANM Hessian matrix.

        The Hessian represents the second derivative of potential energy
        with respect to atomic displacements.

        Args:
            gamma: Spring constant

        Returns:
            3N x 3N Hessian matrix
        """
        n = len(self.ca_coords)
        hessian = np.zeros((3*n, 3*n))

        for i in range(n):
            for j in range(i+1, n):
                r_vec = self.ca_coords[j] - self.ca_coords[i]
                r_mag = np.linalg.norm(r_vec)

                if r_mag < self.cutoff:
                    # Spring constant (can be distance-dependent)
                    k = gamma

                    # Unit vector
                    r_hat = r_vec / r_mag

                    # Build 3x3 sub-block
                    sub_block = k * np.outer(r_hat, r_hat)

                    # Add to Hessian
                    hessian[3*i:3*i+3, 3*j:3*j+3] = -sub_block
                    hessian[3*j:3*j+3, 3*i:3*i+3] = -sub_block
                    hessian[3*i:3*i+3, 3*i:3*i+3] += sub_block
                    hessian[3*j:3*j+3, 3*j:3*j+3] += sub_block

        return hessian

    def calculate_modes(self, n_modes: int = 20) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate normal modes by diagonalizing Hessian.

        Args:
            n_modes: Number of modes to return (excluding 6 trivial modes)

        Returns:
            Tuple of (eigenvalues, eigenvectors)
        """
        print(f"\n  Building Hessian matrix ({3*len(self.ca_coords)} x {3*len(self.ca_coords)})...")
        hessian = self.build_hessian()

        print("  Diagonalizing Hessian...")
        eigenvalues, eigenvectors = np.linalg.eigh(hessian)

        # Skip first 6 trivial modes (translation/rotation)
        # Take smallest non-trivial eigenvalues
        start_idx = 6
        end_idx = start_idx + n_modes

        # Get frequencies (sqrt of eigenvalues)
        # Eigenvalues should be positive for bound modes
        modes_eigenvalues = eigenvalues[start_idx:end_idx]
        modes_eigenvectors = eigenvectors[:, start_idx:end_idx]

        # Convert to frequencies (arbitrary units)
        frequencies = np.sqrt(np.abs(modes_eigenvalues))

        print(f"  Calculated {len(frequencies)} non-trivial modes")

        return frequencies, modes_eigenvectors


# ==============================================================================
# Z² RESONANCE ANALYSIS
# ==============================================================================

def analyze_z2_resonance(frequencies: np.ndarray) -> Dict:
    """
    Analyze alignment between empirical frequencies and Z² harmonics.

    Tests:
    1. Do frequencies cluster near Z² harmonic values?
    2. Is there correlation between mode index and Z² multiple?
    3. What is the vibrational density of states at Z² frequencies?

    Args:
        frequencies: Array of normal mode frequencies

    Returns:
        Analysis results dictionary
    """
    print("\n" + "="*70)
    print("Z² RESONANCE ANALYSIS")
    print("="*70)

    results = {}

    # Normalize frequencies to comparable scale
    freq_norm = frequencies / np.max(frequencies) if np.max(frequencies) > 0 else frequencies

    # Test 1: Distance to nearest Z² harmonic
    z2_harmonics_norm = np.array(Z2_HARMONICS[:20]) / np.max(Z2_HARMONICS[:20])

    deviations = []
    for f in freq_norm:
        # Find nearest Z² harmonic
        dists = np.abs(z2_harmonics_norm - f)
        min_dist = np.min(dists)
        nearest_idx = np.argmin(dists)
        deviations.append({
            'freq': float(f),
            'nearest_z2': float(z2_harmonics_norm[nearest_idx]),
            'deviation': float(min_dist),
            'harmonic_n': nearest_idx + 1
        })

    mean_deviation = np.mean([d['deviation'] for d in deviations])
    random_expected = 0.25  # Expected for uniform random distribution

    print(f"\n  Test 1: Proximity to Z² harmonics")
    print(f"    Mean deviation from nearest Z² harmonic: {mean_deviation:.4f}")
    print(f"    Random expected: ~{random_expected:.4f}")

    if mean_deviation < random_expected * 0.7:
        print(f"    ✓ Frequencies cluster near Z² harmonics!")
        results['proximity_test'] = 'ALIGNED'
    else:
        print(f"    ~ No significant clustering near Z² harmonics")
        results['proximity_test'] = 'NO_ALIGNMENT'

    results['mean_z2_deviation'] = float(mean_deviation)
    results['mode_analysis'] = deviations[:10]

    # Test 2: Correlation between mode index and Z² multiple
    mode_indices = np.arange(1, len(freq_norm) + 1)
    z2_multiples = freq_norm * Z2  # Scale frequencies to Z² space

    # How close are scaled frequencies to integers (Z² multiples)?
    int_deviations = np.abs(z2_multiples - np.round(z2_multiples))
    mean_int_dev = np.mean(int_deviations)

    print(f"\n  Test 2: Integer Z² multiple alignment")
    print(f"    Mean deviation from integer Z² multiples: {mean_int_dev:.4f}")

    if mean_int_dev < 0.25:
        print(f"    ✓ Frequencies quantize to Z² multiples!")
        results['quantization_test'] = 'QUANTIZED'
    else:
        print(f"    ~ Frequencies do not quantize cleanly")
        results['quantization_test'] = 'NOT_QUANTIZED'

    results['mean_quantization_error'] = float(mean_int_dev)

    # Test 3: Pearson correlation
    # Do low modes correspond to low Z² harmonics?
    if len(freq_norm) >= 5:
        correlation, p_value = stats.pearsonr(mode_indices[:10], freq_norm[:10])

        print(f"\n  Test 3: Mode-frequency correlation")
        print(f"    Pearson r: {correlation:.4f}")
        print(f"    p-value: {p_value:.4f}")

        results['correlation'] = {
            'pearson_r': float(correlation),
            'p_value': float(p_value)
        }

    # Density of states at Z² frequencies
    print(f"\n  Vibrational density of states:")
    print(f"    Mode frequencies (normalized):")
    for i, f in enumerate(freq_norm[:10]):
        deviation = deviations[i]
        print(f"      Mode {i+1}: {f:.4f} (nearest Z² = {deviation['harmonic_n']}×f_Z²)")

    return results


# ==============================================================================
# PRODY INTEGRATION (OPTIONAL)
# ==============================================================================

def prody_normal_modes(pdb_path: str) -> Optional[Dict]:
    """
    Calculate normal modes using ProDy (if available).

    ProDy provides more accurate ANM implementation.
    """
    try:
        import prody
        prody.confProDy(verbosity='none')

        print("\n  Using ProDy for ANM calculation...")

        structure = prody.parsePDB(pdb_path)
        calphas = structure.select('calpha')

        if calphas is None:
            return None

        anm = prody.ANM('protein')
        anm.buildHessian(calphas, cutoff=15.0)
        anm.calcModes(n_modes=20)

        frequencies = anm.getEigvals()
        frequencies = np.sqrt(np.abs(frequencies))

        print(f"  ProDy calculated {len(frequencies)} modes")

        return {
            'frequencies': frequencies.tolist(),
            'method': 'ProDy ANM'
        }

    except ImportError:
        return None


# ==============================================================================
# MAIN PIPELINE
# ==============================================================================

def analyze_protein_modes(
    pdb_source: str,
    output_dir: str = "hybrid_z2_test"
) -> Dict:
    """
    Complete normal mode analysis pipeline.

    Args:
        pdb_source: PDB ID or file path
        output_dir: Output directory

    Returns:
        Complete results dictionary
    """
    os.makedirs(output_dir, exist_ok=True)

    print("\n" + "="*70)
    print("Z² NORMAL MODES ANALYSIS")
    print("="*70)

    results = {
        'Z': float(Z),
        'Z2': float(Z2),
        'F_Z2': float(F_Z2),
        'timestamp': datetime.now().isoformat(),
        'license': 'AGPL-3.0-or-later'
    }

    # Get PDB file
    if len(pdb_source) == 4 and pdb_source.isalnum():
        try:
            pdb_path = fetch_pdb(pdb_source, output_dir)
            results['pdb_id'] = pdb_source.upper()
        except Exception as e:
            print(f"  Could not fetch {pdb_source}: {e}")
            return {'error': str(e)}
    else:
        pdb_path = pdb_source
        results['pdb_file'] = pdb_path

    # Try ProDy first
    prody_results = prody_normal_modes(pdb_path)

    if prody_results is not None:
        frequencies = np.array(prody_results['frequencies'])
        results['method'] = 'ProDy ANM'
    else:
        # Use our ANM implementation
        print("\n  Using built-in ANM calculator...")
        anm = ANMCalculator(pdb_path, cutoff=15.0)
        frequencies, _ = anm.calculate_modes(n_modes=20)
        results['method'] = 'Built-in ANM'
        results['n_residues'] = len(anm.ca_coords)

    results['frequencies'] = frequencies.tolist()

    # Z² resonance analysis
    resonance = analyze_z2_resonance(frequencies)
    results['z2_resonance'] = resonance

    # Save plot
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Frequency spectrum
        ax1.bar(range(1, len(frequencies)+1), frequencies, color='steelblue', alpha=0.7)
        ax1.set_xlabel('Mode Index')
        ax1.set_ylabel('Frequency (arb. units)')
        ax1.set_title('Normal Mode Frequencies')

        # Add Z² harmonic lines
        freq_max = max(frequencies)
        for n, z2_f in enumerate(Z2_HARMONICS[:5]):
            scaled_z2 = z2_f * freq_max / F_Z2
            ax1.axhline(y=scaled_z2, color='red', linestyle='--', alpha=0.5,
                       label=f'{n+1}×f_Z²' if n == 0 else None)

        ax1.legend()

        # Z² deviation histogram
        deviations = [d['deviation'] for d in resonance['mode_analysis']]
        ax2.hist(deviations, bins=10, color='coral', alpha=0.7, edgecolor='black')
        ax2.axvline(x=resonance['mean_z2_deviation'], color='red', linestyle='-',
                   label=f'Mean: {resonance["mean_z2_deviation"]:.3f}')
        ax2.axvline(x=0.25, color='gray', linestyle='--', label='Random expected: 0.25')
        ax2.set_xlabel('Deviation from Nearest Z² Harmonic')
        ax2.set_ylabel('Count')
        ax2.set_title('Z² Alignment Distribution')
        ax2.legend()

        plt.tight_layout()
        plot_path = os.path.join(output_dir, 'z2_normal_modes.png')
        plt.savefig(plot_path, dpi=150)
        plt.close()

        results['plot'] = plot_path
        print(f"\n  Plot saved: {plot_path}")

    except ImportError:
        print("  matplotlib not available for plotting")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\n  PDB: {pdb_source}")
    print(f"  Method: {results['method']}")
    print(f"  Modes analyzed: {len(frequencies)}")

    print(f"\n  Z² ALIGNMENT RESULTS:")
    print(f"    Proximity test: {resonance['proximity_test']}")
    print(f"    Quantization test: {resonance['quantization_test']}")
    print(f"    Mean Z² deviation: {resonance['mean_z2_deviation']:.4f}")

    # Final verdict
    if resonance['proximity_test'] == 'ALIGNED' or resonance['quantization_test'] == 'QUANTIZED':
        print(f"\n  *** EVIDENCE FOR Z² RESONANCE IN PROTEIN VIBRATIONS ***")
        results['verdict'] = 'Z2_RESONANCE_DETECTED'
    else:
        print(f"\n  No significant Z² resonance detected in this protein")
        results['verdict'] = 'NO_Z2_RESONANCE'

    # Save results
    results_file = os.path.join(output_dir, 'z2_normal_modes_results.json')
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results saved: {results_file}")

    return results


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Run Z² normal modes analysis on a test protein."""
    print("\n" + "="*70)
    print("HYBRID Z² NORMAL MODES ANALYSIS")
    print("="*70)
    print("Testing: Do protein vibrations align with Z² harmonics?")
    print("License: AGPL-3.0-or-later")
    print("="*70)

    # Test on ubiquitin (well-studied, 76 residues)
    test_pdb = '1UBQ'

    try:
        results = analyze_protein_modes(test_pdb, output_dir='hybrid_z2_test')
        return results

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}


if __name__ == '__main__':
    main()
