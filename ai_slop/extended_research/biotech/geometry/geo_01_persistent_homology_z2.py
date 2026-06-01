#!/usr/bin/env python3
"""
geo_01_persistent_homology_z2.py - Rigorous TDA Validation of Z² Length Scale

Uses Ripser (state-of-the-art persistent homology) to compute the exact
filtration radius where topological loops (β₁) die in protein structures.

THE TEST: If Z² = 32π/3 encodes real protein geometry, the maximum
topological persistence should crash at exactly r ≈ 9.14 Å.

Mathematical Framework:
- Vietoris-Rips filtration on Cα point clouds
- Persistent homology H₀ (components), H₁ (loops), H₂ (voids)
- Death radius analysis vs Z² natural length scale

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later

DISCLAIMER: Theoretical computational research only. Not peer reviewed.
"""

import numpy as np
from scipy import stats
from ripser import ripser
from persim import plot_diagrams
import matplotlib.pyplot as plt
import biotite.structure as struc
import biotite.structure.io.pdb as pdb
import biotite.database.rcsb as rcsb
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# Z² FRAMEWORK CONSTANTS
# =============================================================================
Z2 = 32 * np.pi / 3  # ≈ 33.51
R_NATURAL = (Z2 ** 0.25) * 3.8  # ≈ 9.14 Å

print(f"Z² = 32π/3 = {Z2:.6f}")
print(f"r_natural = (Z²)^(1/4) × 3.8 Å = {R_NATURAL:.4f} Å")
print()

# =============================================================================
# FUNCTIONS
# =============================================================================

def fetch_protein_structure(pdb_id: str) -> Optional[np.ndarray]:
    """
    Fetch Cα coordinates from RCSB PDB using Biotite.
    """
    try:
        # Download PDB file
        pdb_file = rcsb.fetch(pdb_id, "pdb")

        # Parse structure
        structure = pdb.PDBFile.read(pdb_file)
        atom_array = structure.get_structure(model=1)

        # Filter for Cα atoms only
        ca_mask = atom_array.atom_name == "CA"
        ca_atoms = atom_array[ca_mask]

        if len(ca_atoms) < 20:
            return None

        return ca_atoms.coord

    except Exception as e:
        print(f"    Error fetching {pdb_id}: {e}")
        return None

def compute_persistent_homology(coords: np.ndarray,
                                  max_dim: int = 1,
                                  max_radius: float = 15.0) -> Dict:
    """
    Compute persistent homology using Ripser.

    Returns:
        Dict with persistence diagrams and analysis
    """
    # Compute Vietoris-Rips filtration
    result = ripser(coords, maxdim=max_dim, thresh=max_radius)

    diagrams = result['dgms']

    # H0: Connected components (birth, death)
    h0 = diagrams[0]

    # H1: 1-dimensional loops/cycles (birth, death)
    h1 = diagrams[1] if len(diagrams) > 1 else np.array([])

    # Analyze H1 (the key for Z² validation)
    h1_analysis = {}

    if len(h1) > 0:
        # Filter out infinite deaths
        finite_h1 = h1[np.isfinite(h1[:, 1])]

        if len(finite_h1) > 0:
            # Compute persistence (lifetime) of each loop
            lifetimes = finite_h1[:, 1] - finite_h1[:, 0]

            # Find the most persistent loop
            max_idx = np.argmax(lifetimes)
            most_persistent = finite_h1[max_idx]

            # Death radii statistics
            death_radii = finite_h1[:, 1]

            h1_analysis = {
                'n_loops': len(finite_h1),
                'max_persistence': float(lifetimes[max_idx]),
                'most_persistent_birth': float(most_persistent[0]),
                'most_persistent_death': float(most_persistent[1]),
                'mean_death_radius': float(np.mean(death_radii)),
                'median_death_radius': float(np.median(death_radii)),
                'std_death_radius': float(np.std(death_radii)),
                'death_radii': death_radii.tolist(),
            }

    return {
        'h0': h0,
        'h1': h1,
        'h1_analysis': h1_analysis,
    }

def analyze_protein(pdb_id: str) -> Optional[Dict]:
    """
    Complete TDA analysis for a single protein.
    """
    coords = fetch_protein_structure(pdb_id)
    if coords is None:
        return None

    n_residues = len(coords)

    # Compute persistent homology
    ph = compute_persistent_homology(coords)

    if not ph['h1_analysis']:
        return None

    h1 = ph['h1_analysis']

    # Compare death radius to Z² prediction
    death_radius = h1['most_persistent_death']
    z2_deviation = abs(death_radius - R_NATURAL)
    z2_error_pct = (z2_deviation / R_NATURAL) * 100

    return {
        'pdb_id': pdb_id,
        'n_residues': n_residues,
        'n_h1_loops': h1['n_loops'],
        'max_persistence': h1['max_persistence'],
        'most_persistent_death': death_radius,
        'mean_death_radius': h1['mean_death_radius'],
        'median_death_radius': h1['median_death_radius'],
        'z2_natural': R_NATURAL,
        'z2_deviation': z2_deviation,
        'z2_error_pct': z2_error_pct,
        'death_radii': h1['death_radii'],
    }

def main():
    """
    Run rigorous persistent homology analysis.
    """
    print("=" * 70)
    print("PERSISTENT HOMOLOGY: Z² LENGTH SCALE VALIDATION")
    print("Using Ripser for Rigorous Topological Data Analysis")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Z² Natural Length Scale: {R_NATURAL:.4f} Å")
    print()

    # Test proteins (diverse, well-resolved structures)
    test_pdbs = [
        '1UBQ',  # Ubiquitin (76 res)
        '1CRN',  # Crambin (46 res)
        '2GB1',  # Protein G B1 domain (56 res)
        '1VII',  # Villin headpiece (36 res)
        '1L2Y',  # Trp-cage (20 res)
        '1IGD',  # Immunoglobulin domain (61 res)
        '2RNM',  # Ribonuclease (104 res)
        '1TEN',  # Tenascin (90 res)
    ]

    results = {
        'timestamp': datetime.now().isoformat(),
        'z2_value': float(Z2),
        'r_natural': float(R_NATURAL),
        'proteins': [],
        'summary': {},
    }

    print("Analyzing protein topology with Ripser...")
    print("-" * 70)

    death_radii_all = []
    max_persistence_deaths = []

    for pdb_id in test_pdbs:
        print(f"  {pdb_id}...", end=" ", flush=True)

        analysis = analyze_protein(pdb_id)

        if analysis:
            results['proteins'].append(analysis)
            death_radii_all.extend(analysis['death_radii'])
            max_persistence_deaths.append(analysis['most_persistent_death'])

            print(f"✓ {analysis['n_residues']} res, "
                  f"{analysis['n_h1_loops']} loops, "
                  f"death={analysis['most_persistent_death']:.2f} Å "
                  f"(Δ={analysis['z2_error_pct']:.1f}%)")
        else:
            print("✗ Failed")

    # Statistical analysis
    if max_persistence_deaths:
        death_array = np.array(max_persistence_deaths)

        mean_death = np.mean(death_array)
        std_death = np.std(death_array)
        sem_death = std_death / np.sqrt(len(death_array))

        # One-sample t-test: is mean death radius = R_NATURAL?
        t_stat, p_value = stats.ttest_1samp(death_array, R_NATURAL)

        # Effect size (Cohen's d)
        cohens_d = (mean_death - R_NATURAL) / std_death if std_death > 0 else 0

        results['summary'] = {
            'n_proteins': len(max_persistence_deaths),
            'mean_death_radius': float(mean_death),
            'std_death_radius': float(std_death),
            'sem_death_radius': float(sem_death),
            'ci_95_low': float(mean_death - 1.96 * sem_death),
            'ci_95_high': float(mean_death + 1.96 * sem_death),
            'z2_natural': float(R_NATURAL),
            'deviation': float(abs(mean_death - R_NATURAL)),
            'percent_error': float(abs(mean_death - R_NATURAL) / R_NATURAL * 100),
            't_statistic': float(t_stat),
            'p_value': float(p_value),
            'cohens_d': float(cohens_d),
            'validated': p_value > 0.05,  # Cannot reject H₀: μ = R_NATURAL
        }

        print()
        print("=" * 70)
        print("RESULTS: TOPOLOGICAL DEATH RADIUS vs Z² PREDICTION")
        print("=" * 70)
        print()
        print(f"  Proteins analyzed: {len(max_persistence_deaths)}")
        print(f"  Total H₁ loops tracked: {len(death_radii_all)}")
        print()
        print(f"  TOPOLOGICAL DEATH RADIUS (most persistent loop):")
        print(f"    Mean:   {mean_death:.4f} ± {sem_death:.4f} Å")
        print(f"    95% CI: [{mean_death - 1.96*sem_death:.4f}, {mean_death + 1.96*sem_death:.4f}] Å")
        print()
        print(f"  Z² PREDICTION:")
        print(f"    r_natural = {R_NATURAL:.4f} Å")
        print()
        print(f"  COMPARISON:")
        print(f"    Deviation: {abs(mean_death - R_NATURAL):.4f} Å ({abs(mean_death - R_NATURAL)/R_NATURAL*100:.2f}%)")
        print(f"    t-statistic: {t_stat:.4f}")
        print(f"    p-value: {p_value:.6f}")
        print(f"    Cohen's d: {cohens_d:.4f}")
        print()

        if p_value > 0.05:
            print("  ╔══════════════════════════════════════════════════════════════╗")
            print("  ║  RESULT: CANNOT REJECT H₀                                    ║")
            print("  ║  The topological death radius is NOT significantly           ║")
            print("  ║  different from the Z² natural length scale.                 ║")
            print("  ║                                                              ║")
            print("  ║  Protein loops close at ~9 Å, matching Z² = 32π/3 prediction!║")
            print("  ╚══════════════════════════════════════════════════════════════╝")
        else:
            print("  ╔══════════════════════════════════════════════════════════════╗")
            print(f"  ║  RESULT: REJECT H₀ (p = {p_value:.4f})                           ║")
            print(f"  ║  Death radius ({mean_death:.2f} Å) differs from Z² ({R_NATURAL:.2f} Å)       ║")
            print("  ╚══════════════════════════════════════════════════════════════╝")

        # Generate visualization
        print()
        print("Generating persistence diagram...")

        # Re-run for visualization on one protein
        coords = fetch_protein_structure('1UBQ')
        if coords is not None:
            result = ripser(coords, maxdim=1, thresh=15.0)

            fig, axes = plt.subplots(1, 2, figsize=(14, 6))

            # Persistence diagram
            ax1 = axes[0]
            plot_diagrams(result['dgms'], ax=ax1, show=False)
            ax1.axhline(y=R_NATURAL, color='red', linestyle='--', linewidth=2,
                       label=f'Z² = {R_NATURAL:.2f} Å')
            ax1.axvline(x=R_NATURAL, color='red', linestyle='--', linewidth=2)
            ax1.set_title('Persistence Diagram (1UBQ)\nH₀ (blue), H₁ (orange)', fontsize=12)
            ax1.legend()

            # Death radius histogram
            ax2 = axes[1]
            ax2.hist(death_radii_all, bins=30, alpha=0.7, color='steelblue',
                    edgecolor='black', label='All H₁ death radii')
            ax2.axvline(x=R_NATURAL, color='red', linestyle='--', linewidth=2,
                       label=f'Z² prediction = {R_NATURAL:.2f} Å')
            ax2.axvline(x=mean_death, color='green', linestyle='-', linewidth=2,
                       label=f'Mean death = {mean_death:.2f} Å')
            ax2.set_xlabel('Death Radius (Å)', fontsize=12)
            ax2.set_ylabel('Count', fontsize=12)
            ax2.set_title('Distribution of H₁ Loop Death Radii', fontsize=12)
            ax2.legend()

            plt.tight_layout()

            output_dir = Path(__file__).parent / "results"
            output_dir.mkdir(exist_ok=True)
            fig_path = output_dir / "z2_topological_proof.png"
            plt.savefig(fig_path, dpi=300, bbox_inches='tight')
            print(f"  Saved: {fig_path}")
            plt.close()

    # Save results
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)

    # Remove numpy arrays for JSON
    for p in results['proteins']:
        if 'death_radii' in p:
            p['death_radii'] = p['death_radii'][:20]  # Truncate for JSON

    output_path = output_dir / "geo_01_z2_persistent_homology_results.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"  Results saved: {output_path}")
    print()
    print("=" * 70)
    print("PERSISTENT HOMOLOGY ANALYSIS COMPLETE")
    print("=" * 70)

    return results

if __name__ == "__main__":
    main()
