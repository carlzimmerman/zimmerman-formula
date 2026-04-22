#!/usr/bin/env python3
"""
bio_05_thermal_breathing_nma.py

Copyright (C) 2026 Carl Zimmerman
Zimmerman Unified Geometry Framework (ZUGF)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

bio_05_thermal_breathing_nma.py - Thermal Breathing Analysis

Proteins are not static structures - they are vibrating machines.
This script calculates their resonant frequencies using Normal Mode Analysis.

Methods:
1. Anisotropic Network Model (ANM) / Elastic Network Model (ENM)
2. Hessian matrix construction (force constants)
3. Eigenvalue decomposition for normal modes
4. Visualization of principal thermal fluctuations

The lowest-frequency modes represent global "breathing" motions -
how the protein geometrically deforms under 310K thermodynamic heat.

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import urllib.request
from typing import Dict, List, Tuple
from scipy import linalg

OUTPUT_DIR = Path(__file__).parent / "results" / "thermal_breathing"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("THERMAL BREATHING - NORMAL MODE ANALYSIS")
print("Understanding Protein Vibrations at 310K")
print("=" * 80)
print()

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

# Boltzmann constant
KB = 0.001987  # kcal/(mol·K)
TEMPERATURE = 310.0  # K

# ANM parameters
CUTOFF_DISTANCE = 15.0  # Å - interaction cutoff
SPRING_CONSTANT = 1.0   # kcal/(mol·Å²) - uniform spring constant

print(f"Temperature: {TEMPERATURE} K")
print(f"kT = {KB * TEMPERATURE:.4f} kcal/mol")
print(f"ANM cutoff: {CUTOFF_DISTANCE} Å")
print()


# =============================================================================
# PDB HANDLING
# =============================================================================

def download_pdb(pdb_id: str) -> Path:
    """Download PDB file from RCSB."""
    pdb_path = OUTPUT_DIR / f"{pdb_id}.pdb"
    if not pdb_path.exists():
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        print(f"Downloading {pdb_id}...")
        urllib.request.urlretrieve(url, pdb_path)
    return pdb_path


def parse_ca_atoms(pdb_path: Path) -> Tuple[np.ndarray, List[Dict]]:
    """
    Parse C-alpha atoms from PDB for coarse-grained NMA.
    """
    coords = []
    residues = []

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                atom_name = line[12:16].strip()
                if atom_name == 'CA':
                    try:
                        res_name = line[17:20].strip()
                        chain = line[21]
                        res_num = int(line[22:26])
                        x = float(line[30:38])
                        y = float(line[38:46])
                        z = float(line[46:54])

                        coords.append([x, y, z])
                        residues.append({
                            'res_name': res_name,
                            'chain': chain,
                            'res_num': res_num,
                        })
                    except (ValueError, IndexError):
                        continue

    return np.array(coords), residues


# =============================================================================
# ANISOTROPIC NETWORK MODEL
# =============================================================================

def build_kirchhoff_matrix(coords: np.ndarray, cutoff: float = 15.0) -> np.ndarray:
    """
    Build the Kirchhoff (connectivity) matrix for ANM.

    K_ij = -1 if |r_i - r_j| < cutoff and i ≠ j
    K_ii = -Σⱼ K_ij (degree of node i)
    """
    N = len(coords)
    K = np.zeros((N, N))

    for i in range(N):
        for j in range(i + 1, N):
            dist = np.linalg.norm(coords[i] - coords[j])
            if dist < cutoff:
                K[i, j] = -1
                K[j, i] = -1

    # Diagonal elements
    for i in range(N):
        K[i, i] = -np.sum(K[i, :])

    return K


def build_hessian_matrix(coords: np.ndarray, cutoff: float = 15.0,
                          gamma: float = 1.0) -> np.ndarray:
    """
    Build the 3N × 3N Hessian matrix for ANM.

    H_ij = -γ × (r_ij ⊗ r_ij) / |r_ij|² for i ≠ j and |r_ij| < cutoff
    H_ii = -Σⱼ H_ij

    This represents the force constant matrix for all pairwise interactions.
    """
    N = len(coords)
    H = np.zeros((3*N, 3*N))

    for i in range(N):
        for j in range(i + 1, N):
            r_ij = coords[j] - coords[i]
            dist = np.linalg.norm(r_ij)

            if dist < cutoff:
                # Unit vector
                r_hat = r_ij / dist

                # Outer product gives directional coupling
                H_block = -gamma * np.outer(r_hat, r_hat)

                # Fill in the 3x3 blocks
                H[3*i:3*i+3, 3*j:3*j+3] = H_block
                H[3*j:3*j+3, 3*i:3*i+3] = H_block

    # Diagonal blocks (sum of off-diagonal)
    for i in range(N):
        H_diag = np.zeros((3, 3))
        for j in range(N):
            if i != j:
                H_diag -= H[3*i:3*i+3, 3*j:3*j+3]
        H[3*i:3*i+3, 3*i:3*i+3] = H_diag

    return H


def compute_normal_modes(H: np.ndarray, n_modes: int = 20) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute normal modes by diagonalizing the Hessian.

    Returns eigenvalues (frequencies²) and eigenvectors (mode shapes).
    """
    print("  Diagonalizing Hessian matrix...")

    # Eigenvalue decomposition
    eigenvalues, eigenvectors = linalg.eigh(H)

    # First 6 modes are rigid-body (translation + rotation) with λ ≈ 0
    # Skip these and return the next n_modes
    return eigenvalues[6:6+n_modes], eigenvectors[:, 6:6+n_modes]


def compute_fluctuations(eigenvalues: np.ndarray, eigenvectors: np.ndarray,
                          temperature: float = 310.0) -> np.ndarray:
    """
    Compute mean-square fluctuations from normal modes.

    <Δr²_i> = kT × Σₖ (v_ik² / λ_k)
    """
    N = eigenvectors.shape[0] // 3
    n_modes = len(eigenvalues)

    fluctuations = np.zeros(N)
    kT = KB * temperature

    for i in range(N):
        fluct = 0.0
        for k in range(n_modes):
            if eigenvalues[k] > 1e-6:  # Skip near-zero eigenvalues
                # Sum of squared components for atom i
                v_ik_sq = (eigenvectors[3*i, k]**2 +
                          eigenvectors[3*i+1, k]**2 +
                          eigenvectors[3*i+2, k]**2)
                fluct += v_ik_sq / eigenvalues[k]

        fluctuations[i] = kT * fluct

    return fluctuations


def compute_b_factors(fluctuations: np.ndarray) -> np.ndarray:
    """
    Convert fluctuations to crystallographic B-factors.

    B = (8π²/3) × <Δr²>
    """
    return (8 * np.pi**2 / 3) * fluctuations


def compute_collectivity(eigenvector: np.ndarray) -> float:
    """
    Compute collectivity index (how many atoms participate in a mode).

    κ = (1/N) × exp(-Σᵢ pᵢ ln(pᵢ))

    where pᵢ = |vᵢ|² / Σⱼ|vⱼ|²
    """
    N = len(eigenvector) // 3

    # Compute squared magnitudes per atom
    magnitudes = np.zeros(N)
    for i in range(N):
        magnitudes[i] = (eigenvector[3*i]**2 +
                        eigenvector[3*i+1]**2 +
                        eigenvector[3*i+2]**2)

    # Normalize to probabilities
    total = np.sum(magnitudes)
    if total < 1e-10:
        return 0.0

    p = magnitudes / total

    # Entropy
    entropy = 0.0
    for pi in p:
        if pi > 1e-10:
            entropy -= pi * np.log(pi)

    # Collectivity
    return np.exp(entropy) / N


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def identify_hinge_regions(eigenvector: np.ndarray, threshold: float = 0.5) -> List[int]:
    """
    Identify hinge regions (nodes with minimal displacement between domains).
    """
    N = len(eigenvector) // 3

    magnitudes = np.zeros(N)
    for i in range(N):
        magnitudes[i] = np.sqrt(eigenvector[3*i]**2 +
                               eigenvector[3*i+1]**2 +
                               eigenvector[3*i+2]**2)

    # Normalize
    max_mag = np.max(magnitudes)
    if max_mag > 0:
        magnitudes /= max_mag

    # Hinges are regions with low displacement
    hinges = [i for i in range(N) if magnitudes[i] < threshold]

    return hinges


def compute_mode_overlap(mode1: np.ndarray, mode2: np.ndarray) -> float:
    """
    Compute overlap between two modes (0-1).
    """
    dot = np.abs(np.dot(mode1, mode2))
    norm1 = np.linalg.norm(mode1)
    norm2 = np.linalg.norm(mode2)

    if norm1 > 0 and norm2 > 0:
        return dot / (norm1 * norm2)
    return 0.0


# =============================================================================
# VISUALIZATION
# =============================================================================

def save_mode_pdb(coords: np.ndarray, residues: List[Dict],
                   eigenvector: np.ndarray, output_path: Path,
                   scale: float = 10.0):
    """
    Save mode as displacement vectors in PDB format.
    """
    N = len(coords)

    with open(output_path, 'w') as f:
        f.write(f"REMARK Normal mode displacement vectors (scaled by {scale})\n")

        for i in range(N):
            res = residues[i]

            # Original position
            x, y, z = coords[i]
            f.write(f"ATOM  {2*i+1:5d}  CA  {res['res_name']:3s} {res['chain']}{res['res_num']:4d}    "
                   f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C\n")

            # Displaced position
            dx = eigenvector[3*i] * scale
            dy = eigenvector[3*i+1] * scale
            dz = eigenvector[3*i+2] * scale

            x2, y2, z2 = x + dx, y + dy, z + dz
            f.write(f"ATOM  {2*i+2:5d}  CB  {res['res_name']:3s} {res['chain']}{res['res_num']:4d}    "
                   f"{x2:8.3f}{y2:8.3f}{z2:8.3f}  1.00  0.00           C\n")

            # Connect with a bond (for visualization)
            f.write(f"CONECT{2*i+1:5d}{2*i+2:5d}\n")

        f.write("END\n")

    return output_path


def plot_fluctuations(residue_nums: List[int], fluctuations: np.ndarray,
                       output_path: Path):
    """
    Plot B-factor profile.
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(12, 5))

        b_factors = compute_b_factors(fluctuations)

        ax.plot(residue_nums, b_factors, 'b-', linewidth=1.5)
        ax.fill_between(residue_nums, 0, b_factors, alpha=0.3)

        ax.set_xlabel('Residue Number', fontsize=12)
        ax.set_ylabel('B-factor (Å²)', fontsize=12)
        ax.set_title('Thermal Fluctuations from Normal Mode Analysis', fontsize=14)
        ax.grid(True, alpha=0.3)

        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        return output_path

    except ImportError:
        return None


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def analyze_thermal_breathing(pdb_id: str, n_modes: int = 10) -> Dict:
    """
    Complete normal mode analysis for a protein.
    """
    print(f"\n{'=' * 60}")
    print(f"NORMAL MODE ANALYSIS: {pdb_id}")
    print("=" * 60)

    # Load structure
    pdb_path = download_pdb(pdb_id)
    coords, residues = parse_ca_atoms(pdb_path)
    N = len(coords)

    print(f"  Loaded {N} C-alpha atoms")

    result = {
        'pdb_id': pdb_id,
        'n_residues': N,
        'timestamp': datetime.now().isoformat(),
    }

    if N < 10:
        print("  ERROR: Too few residues for NMA")
        result['error'] = 'Too few residues'
        return result

    # Build Hessian
    print(f"  Building Hessian matrix ({3*N} × {3*N})...")
    H = build_hessian_matrix(coords, cutoff=CUTOFF_DISTANCE, gamma=SPRING_CONSTANT)

    # Compute normal modes
    eigenvalues, eigenvectors = compute_normal_modes(H, n_modes=n_modes)

    result['n_modes'] = n_modes
    result['eigenvalues'] = eigenvalues.tolist()

    print(f"\n  NORMAL MODE FREQUENCIES:")
    print(f"  {'Mode':>4s} {'Eigenvalue':>12s} {'Frequency':>12s} {'Collectivity':>12s}")
    print(f"  {'-'*44}")

    modes_info = []
    for k in range(min(n_modes, len(eigenvalues))):
        ev = eigenvalues[k]
        freq = np.sqrt(abs(ev)) if ev > 0 else 0
        collectivity = compute_collectivity(eigenvectors[:, k])

        modes_info.append({
            'mode': k + 1,
            'eigenvalue': float(ev),
            'frequency': float(freq),
            'collectivity': float(collectivity),
        })

        print(f"  {k+1:4d} {ev:12.4f} {freq:12.4f} {collectivity:12.3f}")

    result['modes'] = modes_info

    # Compute fluctuations
    fluctuations = compute_fluctuations(eigenvalues, eigenvectors, TEMPERATURE)
    b_factors = compute_b_factors(fluctuations)

    result['mean_fluctuation'] = float(np.mean(fluctuations))
    result['max_fluctuation'] = float(np.max(fluctuations))
    result['mean_b_factor'] = float(np.mean(b_factors))

    print(f"\n  THERMAL FLUCTUATIONS (310K):")
    print(f"    Mean <Δr²>: {np.mean(fluctuations):.4f} Å²")
    print(f"    Max <Δr²>:  {np.max(fluctuations):.4f} Å²")
    print(f"    Mean B-factor: {np.mean(b_factors):.2f} Å²")

    # Identify flexible and rigid regions
    rigid_threshold = np.percentile(fluctuations, 25)
    flexible_threshold = np.percentile(fluctuations, 75)

    rigid_residues = [residues[i]['res_num'] for i in range(N)
                      if fluctuations[i] < rigid_threshold]
    flexible_residues = [residues[i]['res_num'] for i in range(N)
                         if fluctuations[i] > flexible_threshold]

    result['rigid_residues'] = rigid_residues[:10]  # First 10
    result['flexible_residues'] = flexible_residues[:10]

    print(f"\n  RIGID REGIONS (low fluctuation): {rigid_residues[:5]}...")
    print(f"  FLEXIBLE REGIONS (high fluctuation): {flexible_residues[:5]}...")

    # Identify hinge regions in lowest mode
    hinges = identify_hinge_regions(eigenvectors[:, 0])
    hinge_residues = [residues[i]['res_num'] for i in hinges]
    result['hinge_residues'] = hinge_residues

    if hinge_residues:
        print(f"  HINGE REGIONS (mode 1): {hinge_residues[:10]}...")

    # Save mode visualization
    mode_path = OUTPUT_DIR / f"{pdb_id}_mode1.pdb"
    save_mode_pdb(coords, residues, eigenvectors[:, 0], mode_path)
    result['mode1_pdb'] = str(mode_path)
    print(f"\n  Mode 1 PDB: {mode_path}")

    # Plot fluctuations
    res_nums = [r['res_num'] for r in residues]
    plot_path = OUTPUT_DIR / f"{pdb_id}_fluctuations.png"
    saved = plot_fluctuations(res_nums, fluctuations, plot_path)
    if saved:
        result['plot'] = str(saved)
        print(f"  Fluctuation plot: {saved}")

    return result


def main():
    """
    Run normal mode analysis on reference proteins.
    """
    proteins = [
        ('1PGB', 'Protein G B1 domain'),
        ('1UBQ', 'Ubiquitin'),
        ('4AKE', 'Adenylate kinase (open)'),
    ]

    all_results = []

    for pdb_id, description in proteins:
        print(f"\n{description}")
        result = analyze_thermal_breathing(pdb_id, n_modes=10)
        result['description'] = description
        all_results.append(result)

    # Save results
    json_path = OUTPUT_DIR / "thermal_breathing_results.json"
    with open(json_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\n\nResults saved: {json_path}")

    # Summary
    print("\n" + "=" * 80)
    print("THERMAL BREATHING SUMMARY")
    print("=" * 80)
    print()
    print("Key findings:")
    print("  1. Lowest modes represent GLOBAL BREATHING motions")
    print("  2. High collectivity → many atoms move together (domain motions)")
    print("  3. Hinge regions connect moving domains (drug targets!)")
    print("  4. Flexible loops vs rigid cores dictate function")
    print()
    print("At 310K, proteins are NOT static structures.")
    print("They continuously sample conformational space within")
    print("the harmonic wells defined by their folded geometry.")
    print("=" * 80)

    return all_results


if __name__ == "__main__":
    main()
