#!/usr/bin/env python3
"""
geo_05_allosteric_spring_network.py - Elastic Network Models & Allostery

Treats proteins as Anisotropic Network Models (ANM) where Cα atoms are nodes
connected by uniform springs at Z² contact distance. Performs Normal Mode
Analysis (NMA) to identify allosteric communication pathways.

Mathematical Framework:
- Hessian matrix construction from Z² contact network
- Eigendecomposition for normal modes
- Perturbation response at binding site
- Allosteric signal propagation

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later

DISCLAIMER: Theoretical computational research only. Not peer reviewed.
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.linalg import eigh
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path
from datetime import datetime

# Z² Framework constants
Z2 = 32 * np.pi / 3  # ≈ 33.51
R_NATURAL = (Z2 ** 0.25) * 3.8  # ≈ 9.14 Å
SPRING_CONSTANT = 1.0  # Uniform spring constant (arbitrary units)

def build_hessian_matrix(coords: np.ndarray,
                          cutoff: float = None,
                          gamma: float = SPRING_CONSTANT) -> np.ndarray:
    """
    Build the Hessian matrix for the Anisotropic Network Model (ANM).

    H_ij = -γ * (r_ij ⊗ r_ij) / |r_ij|² for |r_ij| < cutoff
    H_ii = -Σ_{j≠i} H_ij

    Returns 3N × 3N Hessian matrix.
    """
    if cutoff is None:
        cutoff = R_NATURAL

    n = len(coords)
    H = np.zeros((3*n, 3*n))

    for i in range(n):
        for j in range(i+1, n):
            r = coords[j] - coords[i]
            dist = np.linalg.norm(r)

            if dist < cutoff and dist > 1e-6:
                # Off-diagonal block (3x3)
                r_outer = np.outer(r, r) / (dist * dist)
                H_ij = -gamma * r_outer

                # Fill symmetric positions
                H[3*i:3*i+3, 3*j:3*j+3] = H_ij
                H[3*j:3*j+3, 3*i:3*i+3] = H_ij

    # Diagonal blocks: H_ii = -Σ H_ij
    for i in range(n):
        H_ii = np.zeros((3, 3))
        for j in range(n):
            if j != i:
                H_ii -= H[3*i:3*i+3, 3*j:3*j+3]
        H[3*i:3*i+3, 3*i:3*i+3] = H_ii

    return H

def compute_normal_modes(H: np.ndarray, n_modes: int = 20) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute normal modes from Hessian matrix.

    Returns:
        eigenvalues: Frequencies squared (first 6 are ~0 for rigid body)
        eigenvectors: Mode shapes (3N × n_modes)
    """
    eigenvalues, eigenvectors = eigh(H)

    # Sort by eigenvalue (ascending)
    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Return first n_modes (skip first 6 zero modes for rigid body motion)
    return eigenvalues[6:6+n_modes], eigenvectors[:, 6:6+n_modes]

def compute_bfactors(eigenvectors: np.ndarray,
                      eigenvalues: np.ndarray) -> np.ndarray:
    """
    Compute theoretical B-factors (atomic fluctuations) from normal modes.

    B_i = (8π²/3) * Σ_k (1/λ_k) * |e_ik|²

    Returns B-factors per residue.
    """
    n_residues = len(eigenvectors) // 3
    n_modes = len(eigenvalues)

    bfactors = np.zeros(n_residues)

    for k in range(n_modes):
        if eigenvalues[k] > 1e-6:
            mode = eigenvectors[:, k].reshape(-1, 3)
            mode_sq = np.sum(mode ** 2, axis=1)
            bfactors += mode_sq / eigenvalues[k]

    return bfactors * (8 * np.pi ** 2 / 3)

def compute_perturbation_response(H: np.ndarray,
                                   perturbation_site: int,
                                   perturbation_direction: np.ndarray = None) -> np.ndarray:
    """
    Compute linear response to perturbation at a specific site.

    Uses pseudo-inverse of Hessian to compute response:
    Δr = H⁺ · F

    Where F is force applied at perturbation site.

    Returns displacement vector for all residues.
    """
    n_residues = len(H) // 3

    if perturbation_direction is None:
        perturbation_direction = np.array([1, 0, 0])
    perturbation_direction = perturbation_direction / np.linalg.norm(perturbation_direction)

    # Force vector
    F = np.zeros(3 * n_residues)
    F[3*perturbation_site:3*perturbation_site+3] = perturbation_direction

    # Compute response using pseudo-inverse
    # First compute eigendecomposition
    eigenvalues, eigenvectors = eigh(H)

    # Pseudo-inverse (skip zero eigenvalues)
    response = np.zeros(3 * n_residues)
    for k in range(6, len(eigenvalues)):  # Skip rigid body modes
        if eigenvalues[k] > 1e-6:
            v = eigenvectors[:, k]
            response += np.dot(v, F) / eigenvalues[k] * v

    return response.reshape(-1, 3)

def analyze_allosteric_pathway(coords: np.ndarray,
                                binding_site: List[int],
                                active_site: List[int]) -> Dict:
    """
    Analyze allosteric communication between binding and active sites.

    1. Build ANM from coordinates
    2. Apply perturbation at binding site
    3. Measure response at active site
    4. Identify communication pathway
    """
    n_residues = len(coords)

    # Build Hessian
    H = build_hessian_matrix(coords)

    # Compute normal modes
    eigenvalues, eigenvectors = compute_normal_modes(H)

    # Compute B-factors
    bfactors = compute_bfactors(eigenvectors, eigenvalues)

    # Perturb at binding site center
    binding_center = int(np.mean(binding_site))

    # Compute response
    response = compute_perturbation_response(H, binding_center)
    response_magnitude = np.linalg.norm(response, axis=1)

    # Measure response at active site
    active_response = np.mean(response_magnitude[active_site])
    binding_response = np.mean(response_magnitude[binding_site])

    # Allosteric coupling strength
    coupling = active_response / (binding_response + 1e-6)

    # Find pathway (residues with high response between sites)
    pathway_threshold = 0.5 * max(active_response, binding_response)
    pathway_residues = np.where(response_magnitude > pathway_threshold)[0]

    return {
        'n_residues': n_residues,
        'n_modes_computed': len(eigenvalues),
        'lowest_nonzero_freq': float(np.sqrt(eigenvalues[0])) if eigenvalues[0] > 0 else 0,
        'binding_site': binding_site,
        'active_site': active_site,
        'binding_site_response': float(binding_response),
        'active_site_response': float(active_response),
        'allosteric_coupling': float(coupling),
        'pathway_residues': pathway_residues.tolist(),
        'bfactors_mean': float(np.mean(bfactors)),
        'bfactors_std': float(np.std(bfactors)),
        'interpretation': (
            f'Allosteric coupling = {coupling:.2f}. '
            f'{"Strong" if coupling > 0.3 else "Weak"} communication between sites. '
            f'Pathway involves {len(pathway_residues)} residues.'
        ),
    }

def fetch_and_analyze_receptor(pdb_id: str,
                                binding_site: List[int],
                                active_site: List[int]) -> Optional[Dict]:
    """Fetch protein and perform allosteric analysis."""
    import requests

    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            return None

        coords = []
        for line in response.text.split('\n'):
            if line.startswith('ATOM') and ' CA ' in line:
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords.append([x, y, z])
                except ValueError:
                    continue

        if len(coords) < 20:
            return None

        coords = np.array(coords)

        # Adjust site indices if needed
        n = len(coords)
        binding_site = [i for i in binding_site if i < n]
        active_site = [i for i in active_site if i < n]

        if not binding_site or not active_site:
            # Use default sites
            binding_site = list(range(10, 20))
            active_site = list(range(n-20, n-10))

        return analyze_allosteric_pathway(coords, binding_site, active_site)

    except Exception as e:
        return {'error': str(e)}

def main():
    """Run elastic network model analysis."""
    print("=" * 70)
    print("GEO_05: ALLOSTERIC SPRING NETWORK ANALYSIS")
    print("Anisotropic Network Model (ANM) & Normal Mode Analysis")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Z² Contact Cutoff: {R_NATURAL:.2f} Å")
    print(f"Spring Constant: {SPRING_CONSTANT}")
    print()

    results = {
        'timestamp': datetime.now().isoformat(),
        'z2_value': float(Z2),
        'r_natural': float(R_NATURAL),
        'analyses': [],
    }

    # Test with ubiquitin
    print("Analyzing allosteric networks...")
    print("-" * 70)

    # Example: ubiquitin (small, well-studied)
    pdb_id = '1UBQ'
    binding_site = list(range(40, 50))  # Example binding region
    active_site = list(range(0, 10))    # Example active region

    print(f"\n  Analyzing {pdb_id}...")
    print(f"    Binding site residues: {binding_site[0]}-{binding_site[-1]}")
    print(f"    Active site residues: {active_site[0]}-{active_site[-1]}")

    analysis = fetch_and_analyze_receptor(pdb_id, binding_site, active_site)

    if analysis and 'error' not in analysis:
        results['analyses'].append({
            'pdb_id': pdb_id,
            'analysis': analysis,
        })

        print(f"\n  Results:")
        print(f"    Residues: {analysis['n_residues']}")
        print(f"    Normal modes computed: {analysis['n_modes_computed']}")
        print(f"    Lowest frequency: {analysis['lowest_nonzero_freq']:.4f}")
        print(f"    Binding site response: {analysis['binding_site_response']:.4f}")
        print(f"    Active site response: {analysis['active_site_response']:.4f}")
        print(f"    Allosteric coupling: {analysis['allosteric_coupling']:.3f}")
        print(f"    Pathway residues: {len(analysis['pathway_residues'])}")
        print(f"\n  Interpretation:")
        print(f"    {analysis['interpretation']}")
    else:
        print(f"  Error: {analysis.get('error', 'Unknown')}")

    # Summary
    print()
    print("=" * 70)
    print("ELASTIC NETWORK MODEL SUMMARY")
    print("=" * 70)
    print("""
    The Anisotropic Network Model (ANM) treats proteins as:

    1. Nodes: Cα atoms
    2. Edges: Uniform springs at Z² contact distance (~9.14 Å)
    3. Dynamics: Harmonic oscillations around equilibrium

    Normal Mode Analysis reveals:
    - Low-frequency modes: Large-scale functional motions
    - Allosteric pathways: Mechanical signal transmission
    - Binding effects: How ligand binding propagates changes

    DRUG DESIGN INSIGHT:
    Drugs that bind at sites with high allosteric coupling can
    influence distant functional sites through the spring network.
    This is how GPCRs transmit signals across the membrane!
    """)

    # Save results
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "geo_05_spring_network_results.json"

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"Results saved to: {output_path}")
    print("\n" + "=" * 70)
    print("GEO_05 COMPLETE")
    print("=" * 70)

    return results

if __name__ == "__main__":
    main()
