#!/usr/bin/env python3
"""
exec_02_pmf_analysis.py - Potential of Mean Force Analysis for BBB Permeation

Extracts thermodynamic telemetry from the SMD membrane simulation to determine
if our TAT-tagged peptide can cross the Blood-Brain Barrier.

THEORY:
The Potential of Mean Force (PMF) represents the free energy profile along
a reaction coordinate (here, the Z-axis through the membrane). We calculate
this using:

1. Simple Integration: W = ∫ F(z) dz (work done against pulling force)
2. Jarzynski Equality: exp(-βΔG) = <exp(-βW)> for non-equilibrium work

The energy barrier at the hydrophobic core tells us if BBB crossing is feasible:
- ΔG < 5 kcal/mol: Good permeability
- ΔG 5-15 kcal/mol: Moderate, may need optimization
- ΔG > 15 kcal/mol: Poor permeability, need different delivery mechanism

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later

DISCLAIMER: Computational research only. Not peer reviewed. Not medical advice.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

try:
    import mdtraj as md
    print(f"MDTraj version: {md.__version__}")
except ImportError:
    print("WARNING: MDTraj not available, using CSV-only analysis")
    md = None

# =============================================================================
# CONSTANTS
# =============================================================================
Z2 = 32 * np.pi / 3
R_NATURAL = (Z2 ** 0.25) * 3.8  # 9.14 Å

# Thermodynamic constants
KB = 0.001987204  # kcal/(mol·K)
TEMPERATURE = 310  # K
BETA = 1 / (KB * TEMPERATURE)  # 1/kcal/mol

# Membrane parameters (typical POPC bilayer)
MEMBRANE_THICKNESS = 4.0  # nm (hydrophobic core)
HEADGROUP_REGION = 1.0  # nm (polar headgroups on each side)

print(f"Z² = {Z2:.4f}, r_natural = {R_NATURAL:.4f} Å")
print(f"Temperature = {TEMPERATURE} K, β = {BETA:.4f} mol/kcal")
print()


# =============================================================================
# DATA LOADING
# =============================================================================

def load_force_profile(csv_path: Path) -> dict:
    """
    Load the force profile from SMD simulation.

    Returns dict with arrays: step, time, z_com, z_target, force
    """
    print(f"Loading force profile: {csv_path}")

    data = {
        'step': [],
        'time': [],
        'z_com': [],
        'z_target': [],
        'force': []
    }

    with open(csv_path, 'r') as f:
        header = f.readline()  # Skip header
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 5:
                try:
                    data['step'].append(int(parts[0]))
                    data['time'].append(float(parts[1]))
                    data['z_com'].append(float(parts[2]))
                    data['z_target'].append(float(parts[3]))
                    data['force'].append(float(parts[4]))
                except ValueError:
                    continue

    for key in data:
        data[key] = np.array(data[key])

    print(f"  Loaded {len(data['step'])} data points")
    print(f"  Z range: {data['z_com'].min():.3f} to {data['z_com'].max():.3f} nm")
    print(f"  Time range: {data['time'].min():.1f} to {data['time'].max():.1f} ps")

    return data


def load_trajectory(dcd_path: Path, topology_path: Path = None) -> dict:
    """
    Load trajectory using MDTraj for detailed analysis.
    """
    if md is None:
        print("MDTraj not available, skipping trajectory analysis")
        return None

    print(f"Loading trajectory: {dcd_path}")

    # Try to load with topology if available
    try:
        if topology_path and topology_path.exists():
            traj = md.load(str(dcd_path), top=str(topology_path))
        else:
            # Try loading without topology (limited analysis)
            print("  No topology file, attempting load...")
            return None
    except Exception as e:
        print(f"  Could not load trajectory: {e}")
        return None

    print(f"  Frames: {traj.n_frames}")
    print(f"  Atoms: {traj.n_atoms}")

    return {'trajectory': traj}


# =============================================================================
# PMF CALCULATION
# =============================================================================

def calculate_pmf_integration(force_data: dict) -> dict:
    """
    Calculate PMF using simple numerical integration.

    W(z) = -∫ F(z') dz' from z_start to z

    The force from SMD is the restraining force, so the PMF is the
    negative integral.
    """
    print("\nCalculating PMF via numerical integration...")

    z = force_data['z_com']
    force = force_data['force']

    # Sort by Z coordinate
    sort_idx = np.argsort(z)
    z_sorted = z[sort_idx]
    force_sorted = force[sort_idx]

    # Numerical integration using trapezoidal rule
    # PMF = -∫ F dz (negative because F is restoring force)
    pmf = np.zeros_like(z_sorted)
    for i in range(1, len(z_sorted)):
        dz = z_sorted[i] - z_sorted[i-1]
        avg_force = (force_sorted[i] + force_sorted[i-1]) / 2
        pmf[i] = pmf[i-1] - avg_force * dz  # Integrate -F

    # Convert to kcal/mol (from kJ/mol)
    pmf_kcal = pmf / 4.184

    # Find barrier
    pmf_min = np.min(pmf_kcal)
    pmf_max = np.max(pmf_kcal)
    barrier = pmf_max - pmf_min

    # Find position of maximum (should be in hydrophobic core)
    barrier_idx = np.argmax(pmf_kcal)
    barrier_z = z_sorted[barrier_idx]

    print(f"  PMF range: {pmf_min:.2f} to {pmf_max:.2f} kcal/mol")
    print(f"  Energy barrier: {barrier:.2f} kcal/mol at z = {barrier_z:.3f} nm")

    return {
        'z': z_sorted,
        'pmf': pmf_kcal,
        'barrier': barrier,
        'barrier_z': barrier_z,
        'method': 'numerical_integration'
    }


def calculate_pmf_jarzynski(force_data: dict, n_bootstrap: int = 100) -> dict:
    """
    Calculate PMF using Jarzynski's equality.

    exp(-βΔG) = <exp(-βW)>

    Where W is the non-equilibrium work from the pulling simulation.

    This requires multiple trajectories ideally, but we can estimate
    from a single trajectory using block averaging.
    """
    print("\nCalculating PMF via Jarzynski equality...")

    z = force_data['z_com']
    force = force_data['force']

    # Sort by Z
    sort_idx = np.argsort(z)
    z_sorted = z[sort_idx]
    force_sorted = force[sort_idx]

    # Bin the data along Z
    n_bins = 50
    z_bins = np.linspace(z_sorted.min(), z_sorted.max(), n_bins + 1)
    z_centers = (z_bins[:-1] + z_bins[1:]) / 2

    # Calculate cumulative work at each bin
    work = np.zeros_like(z_sorted)
    for i in range(1, len(z_sorted)):
        dz = z_sorted[i] - z_sorted[i-1]
        work[i] = work[i-1] + force_sorted[i] * dz  # Work = F · dz

    # Convert to kcal/mol
    work_kcal = work / 4.184

    # Bin-average the Jarzynski exponential
    pmf_jarzynski = np.zeros(n_bins)

    for i in range(n_bins):
        mask = (z_sorted >= z_bins[i]) & (z_sorted < z_bins[i+1])
        if np.sum(mask) > 0:
            work_in_bin = work_kcal[mask]
            # Jarzynski average
            exp_avg = np.mean(np.exp(-BETA * work_in_bin))
            if exp_avg > 0:
                pmf_jarzynski[i] = -np.log(exp_avg) / BETA
            else:
                pmf_jarzynski[i] = pmf_jarzynski[i-1] if i > 0 else 0

    # Normalize to start at 0
    pmf_jarzynski -= pmf_jarzynski[0]

    barrier = np.max(pmf_jarzynski) - np.min(pmf_jarzynski)
    barrier_idx = np.argmax(pmf_jarzynski)
    barrier_z = z_centers[barrier_idx]

    print(f"  Jarzynski PMF barrier: {barrier:.2f} kcal/mol at z = {barrier_z:.3f} nm")

    return {
        'z': z_centers,
        'pmf': pmf_jarzynski,
        'barrier': barrier,
        'barrier_z': barrier_z,
        'method': 'jarzynski'
    }


# =============================================================================
# ANALYSIS AND INTERPRETATION
# =============================================================================

def analyze_permeation_feasibility(pmf_result: dict) -> dict:
    """
    Interpret PMF results for BBB permeation feasibility.
    """
    barrier = pmf_result['barrier']

    # Permeability classification
    if barrier < 5:
        classification = "EXCELLENT"
        prognosis = "High passive permeability expected. TAT tag is effective."
        recommendation = "Proceed to in vitro BBB assay validation."
    elif barrier < 10:
        classification = "GOOD"
        prognosis = "Moderate permeability. May achieve therapeutic levels."
        recommendation = "Consider optimization or receptor-mediated delivery."
    elif barrier < 15:
        classification = "MODERATE"
        prognosis = "Limited passive permeability. Active transport may be needed."
        recommendation = "Consider RVG conjugation for receptor-mediated transcytosis."
    elif barrier < 25:
        classification = "POOR"
        prognosis = "Low passive permeability. Unlikely to cross BBB passively."
        recommendation = "Switch to RVG or transferrin receptor targeting."
    else:
        classification = "VERY POOR"
        prognosis = "Passive permeation essentially impossible."
        recommendation = "Abandon passive delivery. Use nanoparticle or target macromolecule vectors."

    # Estimate permeability coefficient (rough)
    # P ≈ D/h * exp(-ΔG/RT) where D~1e-6 cm²/s, h~40 Å
    D = 1e-6  # cm²/s diffusion coefficient
    h = 4e-7  # cm membrane thickness
    permeability = D / h * np.exp(-barrier / (KB * TEMPERATURE))

    return {
        'barrier_kcal_mol': barrier,
        'classification': classification,
        'prognosis': prognosis,
        'recommendation': recommendation,
        'estimated_permeability_cm_s': permeability
    }


def identify_membrane_regions(pmf_result: dict) -> dict:
    """
    Identify membrane regions from PMF profile.
    """
    z = pmf_result['z']
    pmf = pmf_result['pmf']

    # Find the center (minimum before barrier or inflection)
    z_center = z[len(z)//2]  # Approximate center

    # Estimate regions
    z_range = z.max() - z.min()

    regions = {
        'water_upper': {'start': z.max() - z_range * 0.1, 'end': z.max()},
        'headgroup_upper': {'start': z.max() - z_range * 0.3, 'end': z.max() - z_range * 0.1},
        'hydrophobic_core': {'start': z.max() - z_range * 0.7, 'end': z.max() - z_range * 0.3},
        'headgroup_lower': {'start': z.max() - z_range * 0.9, 'end': z.max() - z_range * 0.7},
        'water_lower': {'start': z.min(), 'end': z.max() - z_range * 0.9}
    }

    return regions


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_pmf_analysis(force_data: dict, pmf_result: dict,
                       feasibility: dict, output_dir: Path):
    """
    Generate comprehensive PMF analysis plots.
    """
    print("\nGenerating PMF analysis plots...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Plot 1: Force profile over time
    ax1 = axes[0, 0]
    ax1.plot(force_data['time'], force_data['force'], 'b-', alpha=0.7, linewidth=0.5)
    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax1.set_xlabel('Time (ps)', fontsize=12)
    ax1.set_ylabel('Pulling Force (kJ/mol/nm)', fontsize=12)
    ax1.set_title('SMD Pulling Force vs Time', fontsize=14)
    ax1.grid(True, alpha=0.3)

    # Plot 2: Z-coordinate over time
    ax2 = axes[0, 1]
    ax2.plot(force_data['time'], force_data['z_com'], 'g-', linewidth=1, label='Peptide COM')
    ax2.plot(force_data['time'], force_data['z_target'], 'r--', linewidth=1, label='Target')
    ax2.set_xlabel('Time (ps)', fontsize=12)
    ax2.set_ylabel('Z-coordinate (nm)', fontsize=12)
    ax2.set_title('Peptide Trajectory Through Membrane', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Plot 3: PMF Profile
    ax3 = axes[1, 0]
    ax3.plot(pmf_result['z'], pmf_result['pmf'], 'b-', linewidth=2)
    ax3.axhline(y=0, color='k', linestyle='--', alpha=0.3)

    # Mark barrier
    barrier_idx = np.argmax(pmf_result['pmf'])
    ax3.scatter([pmf_result['z'][barrier_idx]], [pmf_result['pmf'][barrier_idx]],
                color='red', s=100, zorder=5, label=f"Barrier: {pmf_result['barrier']:.1f} kcal/mol")

    # Shade membrane regions (approximate)
    z_range = pmf_result['z'].max() - pmf_result['z'].min()
    z_mid = (pmf_result['z'].max() + pmf_result['z'].min()) / 2

    ax3.axvspan(z_mid - z_range*0.2, z_mid + z_range*0.2,
                alpha=0.2, color='yellow', label='Hydrophobic core')

    ax3.set_xlabel('Z-coordinate (nm)', fontsize=12)
    ax3.set_ylabel('Free Energy (kcal/mol)', fontsize=12)
    ax3.set_title('Potential of Mean Force', fontsize=14)
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Plot 4: Analysis Summary
    ax4 = axes[1, 1]
    ax4.axis('off')

    summary_text = f"""
    BBB PERMEATION ANALYSIS SUMMARY
    {'='*45}

    METHOD: {pmf_result['method'].replace('_', ' ').title()}

    ENERGY BARRIER: {pmf_result['barrier']:.2f} kcal/mol
    BARRIER LOCATION: z = {pmf_result['barrier_z']:.3f} nm

    CLASSIFICATION: {feasibility['classification']}

    PROGNOSIS:
    {feasibility['prognosis']}

    RECOMMENDATION:
    {feasibility['recommendation']}

    ESTIMATED PERMEABILITY: {feasibility['estimated_permeability_cm_s']:.2e} cm/s

    {'='*45}
    Z² Framework: r_natural = {R_NATURAL:.2f} Å
    """

    ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes,
             fontsize=11, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()

    # Save
    output_path = output_dir / "pmf_analysis.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"  Saved: {output_path}")
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run complete PMF analysis on membrane simulation results.
    """
    print("=" * 70)
    print("POTENTIAL OF MEAN FORCE ANALYSIS")
    print("Blood-Brain Barrier Permeation Thermodynamics")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Find results directory
    base_dir = Path(__file__).parent

    # Check both full and half-load directories
    results_dirs = [
        base_dir / "membrane_results_halfload",
        base_dir / "membrane_results"
    ]

    results_dir = None
    for d in results_dirs:
        if d.exists() and (d / "permeation_force_profile.csv").exists():
            results_dir = d
            break

    if results_dir is None:
        print("ERROR: No membrane simulation results found!")
        print("Run exec_01_membrane_permeation.py first.")
        return

    print(f"Using results from: {results_dir}")

    # Load force profile
    force_path = results_dir / "permeation_force_profile.csv"
    force_data = load_force_profile(force_path)

    if len(force_data['step']) < 10:
        print("ERROR: Insufficient data points in force profile")
        print("Simulation may still be running or failed early")
        return

    # Calculate PMF using both methods
    pmf_integration = calculate_pmf_integration(force_data)
    pmf_jarzynski = calculate_pmf_jarzynski(force_data)

    # Use integration result (more robust for single trajectory)
    pmf_result = pmf_integration

    # Analyze feasibility
    feasibility = analyze_permeation_feasibility(pmf_result)

    # Print results
    print("\n" + "=" * 70)
    print("BBB PERMEATION FEASIBILITY")
    print("=" * 70)
    print(f"\n  Energy Barrier: {feasibility['barrier_kcal_mol']:.2f} kcal/mol")
    print(f"  Classification: {feasibility['classification']}")
    print(f"\n  Prognosis: {feasibility['prognosis']}")
    print(f"\n  Recommendation: {feasibility['recommendation']}")
    print(f"\n  Est. Permeability: {feasibility['estimated_permeability_cm_s']:.2e} cm/s")

    # Generate plots
    plot_pmf_analysis(force_data, pmf_result, feasibility, results_dir)

    # Save JSON results
    results = {
        'timestamp': datetime.now().isoformat(),
        'z2_natural': float(R_NATURAL),
        'pmf_method': pmf_result['method'],
        'barrier_kcal_mol': float(pmf_result['barrier']),
        'barrier_z_nm': float(pmf_result['barrier_z']),
        'classification': feasibility['classification'],
        'prognosis': feasibility['prognosis'],
        'recommendation': feasibility['recommendation'],
        'permeability_cm_s': float(feasibility['estimated_permeability_cm_s']),
        'data_points': len(force_data['step']),
        'z_range_nm': [float(force_data['z_com'].min()), float(force_data['z_com'].max())],
        'jarzynski_barrier_kcal_mol': float(pmf_jarzynski['barrier'])
    }

    json_path = results_dir / "pmf_analysis_results.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved: {json_path}")

    print("\n" + "=" * 70)
    print("PMF ANALYSIS COMPLETE")
    print("=" * 70)

    return results


if __name__ == "__main__":
    main()
