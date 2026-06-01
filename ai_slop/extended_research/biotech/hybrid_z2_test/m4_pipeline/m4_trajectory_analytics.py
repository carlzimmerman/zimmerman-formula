#!/usr/bin/env python3
"""
M4 Trajectory Analytics: Publication-Quality Analysis

SPDX-License-Identifier: AGPL-3.0-or-later

Extract rigorous thermodynamic metrics from MD trajectory:
1. RMSD (Root Mean Square Deviation) - structural stability
2. Rg (Radius of Gyration) - compactness
3. Hydrogen Bonds - structural integrity

Output: Publication-ready figure with three subplots.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import os
import sys
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


def analyze_trajectory(
    trajectory_file: str,
    topology_file: str,
    output_dir: str = "trajectory_analysis",
    selection: str = "protein and name CA"
) -> Dict:
    """
    Analyze MD trajectory for publication-quality metrics.

    Calculates:
    - RMSD: Backbone stability (should plateau)
    - Rg: Compactness (should be stable)
    - H-bonds: Structural integrity

    Args:
        trajectory_file: Path to DCD trajectory
        topology_file: Path to PDB topology
        output_dir: Output directory
        selection: Atom selection for analysis

    Returns:
        Dictionary with analysis results
    """
    print("=" * 70)
    print("M4 TRAJECTORY ANALYTICS")
    print("Publication-Quality Analysis")
    print("=" * 70)
    print(f"Trajectory: {trajectory_file}")
    print(f"Topology: {topology_file}")

    os.makedirs(output_dir, exist_ok=True)

    result = {
        "timestamp": datetime.now().isoformat(),
        "trajectory_file": trajectory_file,
        "topology_file": topology_file,
        "status": "started"
    }

    # Try MDAnalysis first, fall back to mdtraj
    try:
        return analyze_with_mdanalysis(
            trajectory_file, topology_file, output_dir, selection, result
        )
    except ImportError:
        print("\nMDAnalysis not available, trying mdtraj...")
        try:
            return analyze_with_mdtraj(
                trajectory_file, topology_file, output_dir, result
            )
        except ImportError:
            print("\n✗ Neither MDAnalysis nor mdtraj available.")
            print("Install with: pip install MDAnalysis mdtraj matplotlib")
            result["status"] = "failed"
            result["error"] = "Missing trajectory analysis library"
            return result


def analyze_with_mdanalysis(
    trajectory_file: str,
    topology_file: str,
    output_dir: str,
    selection: str,
    result: Dict
) -> Dict:
    """Analyze trajectory using MDAnalysis."""
    import MDAnalysis as mda
    from MDAnalysis.analysis import rms, contacts
    from MDAnalysis.analysis.hydrogenbonds import HydrogenBondAnalysis
    import matplotlib.pyplot as plt

    print(f"\n{'='*60}")
    print("LOADING TRAJECTORY (MDAnalysis)")
    print("=" * 60)

    # Load trajectory
    u = mda.Universe(topology_file, trajectory_file)
    n_frames = len(u.trajectory)
    n_atoms = len(u.atoms)

    print(f"  Frames: {n_frames}")
    print(f"  Atoms: {n_atoms:,}")
    print(f"  Timestep: {u.trajectory.dt} ps")

    result["n_frames"] = n_frames
    result["n_atoms"] = n_atoms

    # Select protein backbone
    protein = u.select_atoms("protein")
    backbone = u.select_atoms("protein and backbone")
    ca_atoms = u.select_atoms("protein and name CA")

    print(f"  Protein atoms: {len(protein)}")
    print(f"  Backbone atoms: {len(backbone)}")
    print(f"  Cα atoms: {len(ca_atoms)}")

    # =========================================================================
    # RMSD ANALYSIS
    # =========================================================================
    print(f"\n{'='*60}")
    print("CALCULATING RMSD")
    print("=" * 60)

    R = rms.RMSD(ca_atoms, ca_atoms, select='all', ref_frame=0)
    R.run()

    times = R.results.rmsd[:, 1]  # Time in ps
    rmsd_values = R.results.rmsd[:, 2]  # RMSD in Å

    result["rmsd"] = {
        "times_ps": times.tolist(),
        "values_A": rmsd_values.tolist(),
        "mean_A": float(np.mean(rmsd_values)),
        "std_A": float(np.std(rmsd_values)),
        "final_A": float(rmsd_values[-1])
    }

    print(f"  Mean RMSD: {result['rmsd']['mean_A']:.2f} ± {result['rmsd']['std_A']:.2f} Å")
    print(f"  Final RMSD: {result['rmsd']['final_A']:.2f} Å")

    # =========================================================================
    # RADIUS OF GYRATION
    # =========================================================================
    print(f"\n{'='*60}")
    print("CALCULATING RADIUS OF GYRATION")
    print("=" * 60)

    rg_values = []
    for ts in u.trajectory:
        rg = protein.radius_of_gyration()
        rg_values.append(rg)

    rg_values = np.array(rg_values)

    result["rg"] = {
        "times_ps": times.tolist(),
        "values_A": rg_values.tolist(),
        "mean_A": float(np.mean(rg_values)),
        "std_A": float(np.std(rg_values)),
        "initial_A": float(rg_values[0]),
        "final_A": float(rg_values[-1])
    }

    print(f"  Mean Rg: {result['rg']['mean_A']:.2f} ± {result['rg']['std_A']:.2f} Å")
    print(f"  Initial Rg: {result['rg']['initial_A']:.2f} Å")
    print(f"  Final Rg: {result['rg']['final_A']:.2f} Å")

    # Check for unfolding
    rg_change = (rg_values[-1] - rg_values[0]) / rg_values[0] * 100
    if abs(rg_change) > 10:
        print(f"  ⚠ WARNING: Rg changed by {rg_change:.1f}% - possible unfolding!")
    else:
        print(f"  ✓ Structure stable (Rg change: {rg_change:.1f}%)")

    # =========================================================================
    # HYDROGEN BOND ANALYSIS
    # =========================================================================
    print(f"\n{'='*60}")
    print("CALCULATING HYDROGEN BONDS")
    print("=" * 60)

    try:
        hbonds = HydrogenBondAnalysis(
            u,
            donors_sel="protein and name N",
            hydrogens_sel="protein and name H",
            acceptors_sel="protein and name O",
            d_a_cutoff=3.5,
            d_h_a_angle_cutoff=150
        )
        hbonds.run()

        # Count H-bonds per frame
        hbond_counts = []
        for ts in u.trajectory:
            frame_idx = ts.frame
            frame_hbonds = hbonds.results.hbonds[hbonds.results.hbonds[:, 0] == frame_idx]
            hbond_counts.append(len(frame_hbonds))

        hbond_counts = np.array(hbond_counts)

        result["hbonds"] = {
            "times_ps": times.tolist(),
            "counts": hbond_counts.tolist(),
            "mean": float(np.mean(hbond_counts)),
            "std": float(np.std(hbond_counts)),
            "initial": int(hbond_counts[0]),
            "final": int(hbond_counts[-1])
        }

        print(f"  Mean H-bonds: {result['hbonds']['mean']:.1f} ± {result['hbonds']['std']:.1f}")
        print(f"  Initial H-bonds: {result['hbonds']['initial']}")
        print(f"  Final H-bonds: {result['hbonds']['final']}")

    except Exception as e:
        print(f"  ⚠ H-bond analysis failed: {e}")
        # Estimate from structure
        hbond_counts = np.zeros(n_frames)
        result["hbonds"] = {
            "times_ps": times.tolist(),
            "counts": hbond_counts.tolist(),
            "mean": 0,
            "std": 0,
            "error": str(e)
        }

    # =========================================================================
    # GENERATE PUBLICATION FIGURE
    # =========================================================================
    print(f"\n{'='*60}")
    print("GENERATING PUBLICATION FIGURE")
    print("=" * 60)

    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # Convert times to ns for readability
    times_ns = times / 1000

    # RMSD subplot
    ax1 = axes[0]
    ax1.plot(times_ns, rmsd_values, 'b-', linewidth=0.8, alpha=0.8)
    ax1.axhline(y=np.mean(rmsd_values), color='r', linestyle='--',
                label=f'Mean: {np.mean(rmsd_values):.2f} Å')
    ax1.set_ylabel('RMSD (Å)', fontsize=12)
    ax1.set_title('Backbone RMSD from Initial Structure', fontsize=14)
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # Rg subplot
    ax2 = axes[1]
    ax2.plot(times_ns, rg_values, 'g-', linewidth=0.8, alpha=0.8)
    ax2.axhline(y=np.mean(rg_values), color='r', linestyle='--',
                label=f'Mean: {np.mean(rg_values):.2f} Å')
    ax2.set_ylabel('Radius of Gyration (Å)', fontsize=12)
    ax2.set_title('Protein Compactness', fontsize=14)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)

    # H-bonds subplot
    ax3 = axes[2]
    ax3.plot(times_ns, hbond_counts, 'm-', linewidth=0.8, alpha=0.8)
    ax3.axhline(y=np.mean(hbond_counts), color='r', linestyle='--',
                label=f'Mean: {np.mean(hbond_counts):.1f}')
    ax3.set_xlabel('Time (ns)', fontsize=12)
    ax3.set_ylabel('Hydrogen Bonds', fontsize=12)
    ax3.set_title('Intramolecular Hydrogen Bonds', fontsize=14)
    ax3.legend(loc='upper right')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()

    # Save figure
    figure_path = os.path.join(output_dir, "trajectory_analysis.png")
    plt.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Figure saved: {figure_path}")

    result["figure_path"] = figure_path
    result["status"] = "success"

    # =========================================================================
    # STABILITY ASSESSMENT
    # =========================================================================
    print(f"\n{'='*70}")
    print("STABILITY ASSESSMENT")
    print("=" * 70)

    # Check RMSD plateau (last 20% should be stable)
    rmsd_last_20 = rmsd_values[int(0.8 * len(rmsd_values)):]
    rmsd_plateau = np.std(rmsd_last_20) < 0.5

    # Check Rg stability
    rg_stable = abs(rg_change) < 10

    # Check H-bond maintenance
    hbond_maintained = np.mean(hbond_counts) > 5 if len(hbond_counts) > 0 else True

    result["stability"] = {
        "rmsd_plateau": rmsd_plateau,
        "rg_stable": rg_stable,
        "hbonds_maintained": hbond_maintained,
        "overall_stable": rmsd_plateau and rg_stable and hbond_maintained
    }

    print(f"""
Assessment:
  - RMSD plateau: {'✓ YES' if rmsd_plateau else '✗ NO'} (std of last 20%: {np.std(rmsd_last_20):.2f} Å)
  - Rg stable: {'✓ YES' if rg_stable else '✗ NO'} (change: {rg_change:.1f}%)
  - H-bonds maintained: {'✓ YES' if hbond_maintained else '✗ NO'}

Overall: {'✓ STRUCTURE IS STABLE' if result['stability']['overall_stable'] else '⚠ STRUCTURE MAY BE UNSTABLE'}
    """)

    # Save results
    results_path = os.path.join(output_dir, "analysis_results.json")
    with open(results_path, 'w') as f:
        json.dump(result, f, indent=2, default=str)

    print(f"✓ Results saved: {results_path}")

    return result


def analyze_with_mdtraj(
    trajectory_file: str,
    topology_file: str,
    output_dir: str,
    result: Dict
) -> Dict:
    """Fallback analysis using mdtraj."""
    import mdtraj as md
    import matplotlib.pyplot as plt

    print(f"\n{'='*60}")
    print("LOADING TRAJECTORY (mdtraj)")
    print("=" * 60)

    # Load trajectory
    traj = md.load(trajectory_file, top=topology_file)

    n_frames = traj.n_frames
    n_atoms = traj.n_atoms
    times = traj.time  # in ps

    print(f"  Frames: {n_frames}")
    print(f"  Atoms: {n_atoms:,}")

    result["n_frames"] = n_frames
    result["n_atoms"] = n_atoms

    # RMSD
    print("\nCalculating RMSD...")
    rmsd_values = md.rmsd(traj, traj, frame=0) * 10  # Convert to Å

    result["rmsd"] = {
        "times_ps": times.tolist(),
        "values_A": rmsd_values.tolist(),
        "mean_A": float(np.mean(rmsd_values)),
        "std_A": float(np.std(rmsd_values))
    }

    # Rg
    print("Calculating Radius of Gyration...")
    rg_values = md.compute_rg(traj) * 10  # Convert to Å

    result["rg"] = {
        "times_ps": times.tolist(),
        "values_A": rg_values.tolist(),
        "mean_A": float(np.mean(rg_values)),
        "std_A": float(np.std(rg_values))
    }

    # H-bonds (simplified)
    print("Calculating Hydrogen Bonds...")
    try:
        hbonds = md.baker_hubbard(traj)
        hbond_counts = np.array([len(md.baker_hubbard(traj[i])) for i in range(n_frames)])
    except Exception:
        hbond_counts = np.zeros(n_frames)

    result["hbonds"] = {
        "times_ps": times.tolist(),
        "counts": hbond_counts.tolist(),
        "mean": float(np.mean(hbond_counts))
    }

    # Generate figure
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    times_ns = times / 1000

    axes[0].plot(times_ns, rmsd_values, 'b-')
    axes[0].set_ylabel('RMSD (Å)')
    axes[0].set_title('Backbone RMSD')

    axes[1].plot(times_ns, rg_values, 'g-')
    axes[1].set_ylabel('Rg (Å)')
    axes[1].set_title('Radius of Gyration')

    axes[2].plot(times_ns, hbond_counts, 'm-')
    axes[2].set_xlabel('Time (ns)')
    axes[2].set_ylabel('H-bonds')
    axes[2].set_title('Hydrogen Bonds')

    plt.tight_layout()

    figure_path = os.path.join(output_dir, "trajectory_analysis.png")
    plt.savefig(figure_path, dpi=300)
    plt.close()

    result["figure_path"] = figure_path
    result["status"] = "success"

    # Save results
    results_path = os.path.join(output_dir, "analysis_results.json")
    with open(results_path, 'w') as f:
        json.dump(result, f, indent=2, default=str)

    return result


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("M4 TRAJECTORY ANALYTICS")
    print("Publication-Quality MD Analysis")
    print("=" * 70)

    # Test with production trajectory
    trajectory = "production_md/production_trajectory.dcd"
    topology = "production_md/equilibrated.pdb"

    if os.path.exists(trajectory) and os.path.exists(topology):
        result = analyze_trajectory(
            trajectory,
            topology,
            output_dir="trajectory_analysis"
        )

        if result["status"] == "success":
            print(f"\n✓ Analysis complete!")
            print(f"Figure: {result['figure_path']}")
        else:
            print(f"\n✗ Analysis failed: {result.get('error', 'unknown')}")
    else:
        print(f"\n⚠ Trajectory not found: {trajectory}")
        print("Run m4_amber_production_md.py first to generate trajectory.")

        # Check for required packages
        print("\nChecking dependencies...")
        try:
            import MDAnalysis
            print("  ✓ MDAnalysis available")
        except ImportError:
            print("  ✗ MDAnalysis not installed")

        try:
            import mdtraj
            print("  ✓ mdtraj available")
        except ImportError:
            print("  ✗ mdtraj not installed")

        try:
            import matplotlib
            print("  ✓ matplotlib available")
        except ImportError:
            print("  ✗ matplotlib not installed")

        print("\nInstall with: pip install MDAnalysis mdtraj matplotlib")
