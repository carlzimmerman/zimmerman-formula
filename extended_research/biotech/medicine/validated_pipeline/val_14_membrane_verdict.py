#!/usr/bin/env python3
"""
val_14_membrane_verdict.py

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

val_14_membrane_verdict.py - Blood-Brain Barrier Permeability Verdict

Analyzes the Z-axis trajectory from membrane permeability simulations
to determine if peptides can cross the Blood-Brain Barrier.

MEMBRANE GEOMETRY (POPC bilayer):
  Z > 20 Å  : Water phase (extracellular)
  Z = 15-20 Å: Headgroup region (phosphocholine)
  Z = 5-15 Å : Interface region
  Z = -5 to 5 Å: Hydrophobic core (acyl chains)
  Z < -5 Å  : Opposite leaflet

BBB VERDICTS:
  Stays Z > 15 Å          → BOUNCED (fails BBB)
  Enters Z = 5-15 Å       → SURFACE_INTERACTION (marginal)
  Enters Z = -5 to 5 Å    → CORE_PENETRATION (passes BBB)
  Translocates to Z < -5 Å → FULL_TRANSLOCATION (excellent)

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Optional
import csv

OUTPUT_DIR = Path(__file__).parent / "results" / "membrane_verdict"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MEMBRANE_DIR = Path(__file__).parent / "results" / "membrane_permeability"

print("=" * 80)
print("BLOOD-BRAIN BARRIER PERMEABILITY VERDICT")
print("Analyzing Membrane Penetration Trajectories")
print("=" * 80)
print()

# =============================================================================
# MEMBRANE GEOMETRY CONSTANTS (in nm, converted from simulation)
# =============================================================================

# Membrane center is at Z = 0
# Headgroups at approximately ±2.0 nm (±20 Å)
# Hydrophobic core within ±1.5 nm (±15 Å)

# Z-coordinate thresholds (in nm, matching simulation output)
Z_WATER = 2.0  # Above this = pure water phase
Z_HEADGROUP = 1.5  # Interface with headgroups
Z_INTERFACE = 0.5  # Deep interface
Z_CORE = 0.0  # Hydrophobic core center

print("Membrane Geometry (Z-axis, nm):")
print(f"  Z > {Z_WATER} nm : Water phase (no interaction)")
print(f"  Z = {Z_HEADGROUP}-{Z_WATER} nm : Headgroup region")
print(f"  Z = {Z_INTERFACE}-{Z_HEADGROUP} nm : Interface region")
print(f"  Z = 0-{Z_INTERFACE} nm : Hydrophobic core")
print(f"  Z < 0 nm : Opposite leaflet")
print()


# =============================================================================
# LOAD TRAJECTORY DATA
# =============================================================================

def load_z_trajectory(csv_path: Path) -> Optional[Dict]:
    """
    Load Z-coordinate trajectory from CSV file.
    """
    if not csv_path.exists():
        return None

    times = []
    z_values = []

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            times.append(float(row['time_ns']))
            z_values.append(float(row['z_nm']))

    return {
        'times_ns': np.array(times),
        'z_nm': np.array(z_values),
    }


def load_membrane_results() -> Optional[Dict]:
    """
    Load membrane permeability results from JSON.
    """
    json_path = MEMBRANE_DIR / "membrane_permeability_results.json"

    if json_path.exists():
        with open(json_path, 'r') as f:
            return json.load(f)

    return None


# =============================================================================
# TRAJECTORY ANALYSIS
# =============================================================================

def analyze_z_trajectory(z_values: np.ndarray, times: np.ndarray) -> Dict:
    """
    Analyze Z-coordinate trajectory for membrane penetration.
    """
    analysis = {
        'n_frames': len(z_values),
        'duration_ns': float(times[-1] - times[0]) if len(times) > 1 else 0,
    }

    # Basic statistics
    analysis['z_mean'] = float(np.mean(z_values))
    analysis['z_std'] = float(np.std(z_values))
    analysis['z_min'] = float(np.min(z_values))
    analysis['z_max'] = float(np.max(z_values))
    analysis['z_initial'] = float(z_values[0])
    analysis['z_final'] = float(z_values[-1])

    # Time spent in each region
    n_total = len(z_values)

    n_water = np.sum(z_values > Z_WATER)
    n_headgroup = np.sum((z_values > Z_HEADGROUP) & (z_values <= Z_WATER))
    n_interface = np.sum((z_values > Z_INTERFACE) & (z_values <= Z_HEADGROUP))
    n_core = np.sum((z_values >= -Z_INTERFACE) & (z_values <= Z_INTERFACE))
    n_opposite = np.sum(z_values < -Z_INTERFACE)

    analysis['time_fractions'] = {
        'water': float(n_water / n_total),
        'headgroup': float(n_headgroup / n_total),
        'interface': float(n_interface / n_total),
        'core': float(n_core / n_total),
        'opposite_leaflet': float(n_opposite / n_total),
    }

    # Penetration depth (how deep did it go?)
    analysis['max_penetration_depth'] = float(Z_WATER - np.min(z_values))

    # Did it reach the core?
    analysis['reached_core'] = bool(np.min(z_values) <= Z_INTERFACE)

    # Did it translocate?
    analysis['translocated'] = bool(np.min(z_values) < -Z_INTERFACE)

    # Drift analysis (is it moving deeper over time?)
    if len(z_values) > 10:
        # Linear regression for drift
        slope, _ = np.polyfit(times, z_values, 1)
        analysis['z_drift_nm_per_ns'] = float(slope)

        # Is it trending toward membrane?
        analysis['trending_inward'] = slope < -0.01  # Moving into membrane
    else:
        analysis['z_drift_nm_per_ns'] = 0.0
        analysis['trending_inward'] = False

    return analysis


def assign_bbb_verdict(analysis: Dict) -> Dict:
    """
    Assign Blood-Brain Barrier verdict based on trajectory analysis.
    """
    z_min = analysis['z_min']
    time_in_core = analysis['time_fractions']['core']
    time_in_interface = analysis['time_fractions']['interface']
    translocated = analysis['translocated']
    reached_core = analysis['reached_core']

    # Decision tree for BBB permeability
    if translocated:
        verdict = "FULL_TRANSLOCATION"
        bbb_status = "EXCELLENT"
        recommendation = "Strong BBB penetration capability"
        emoji = "✓✓"

    elif reached_core and time_in_core > 0.1:
        verdict = "CORE_PENETRATION"
        bbb_status = "PASS"
        recommendation = "Likely to cross BBB"
        emoji = "✓"

    elif time_in_interface > 0.2 or time_in_core > 0.05:
        verdict = "SURFACE_INTERACTION"
        bbb_status = "MARGINAL"
        recommendation = "Some membrane interaction, may need CPP modification"
        emoji = "~"

    elif z_min < Z_WATER:
        verdict = "WEAK_INTERACTION"
        bbb_status = "POOR"
        recommendation = "Minimal penetration, consider lipidation"
        emoji = "?"

    else:
        verdict = "BOUNCED"
        bbb_status = "FAIL"
        recommendation = "No membrane penetration, not suitable for CNS"
        emoji = "✗"

    return {
        'verdict': verdict,
        'bbb_status': bbb_status,
        'recommendation': recommendation,
        'emoji': emoji,
    }


# =============================================================================
# PLOTTING
# =============================================================================

def plot_z_trajectory(times: np.ndarray, z_values: np.ndarray,
                       peptide_id: str, verdict: str) -> Optional[Path]:
    """
    Plot Z-coordinate vs time with membrane regions.
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot trajectory
        ax.plot(times, z_values, 'b-', linewidth=1.5, label='Peptide Z-coordinate')

        # Mark membrane regions
        ax.axhspan(Z_WATER, 4.0, alpha=0.1, color='blue', label='Water')
        ax.axhspan(Z_HEADGROUP, Z_WATER, alpha=0.2, color='yellow', label='Headgroups')
        ax.axhspan(Z_INTERFACE, Z_HEADGROUP, alpha=0.2, color='orange', label='Interface')
        ax.axhspan(-Z_INTERFACE, Z_INTERFACE, alpha=0.3, color='red', label='Hydrophobic core')
        ax.axhspan(-Z_HEADGROUP, -Z_INTERFACE, alpha=0.2, color='orange')
        ax.axhspan(-Z_WATER, -Z_HEADGROUP, alpha=0.2, color='yellow')
        ax.axhspan(-4.0, -Z_WATER, alpha=0.1, color='blue')

        # Membrane center line
        ax.axhline(0, color='red', linestyle='--', alpha=0.5, label='Membrane center')

        ax.set_xlabel('Time (ns)', fontsize=12)
        ax.set_ylabel('Z-coordinate (nm)', fontsize=12)
        ax.set_title(f'{peptide_id}: Membrane Penetration\nVerdict: {verdict}', fontsize=14)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)

        # Set reasonable y-limits
        y_min = min(-3.0, z_values.min() - 0.5)
        y_max = max(4.0, z_values.max() + 0.5)
        ax.set_ylim(y_min, y_max)

        plot_path = OUTPUT_DIR / f"{peptide_id}_membrane_trajectory.png"
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close()

        return plot_path

    except ImportError:
        return None


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def analyze_peptide(peptide_id: str, data: Dict) -> Dict:
    """
    Full membrane permeability analysis for one peptide.
    """
    print(f"\n{'=' * 60}")
    print(f"Analyzing: {peptide_id}")
    print(f"{'=' * 60}")

    result = {
        'peptide_id': peptide_id,
        'timestamp': datetime.now().isoformat(),
    }

    # Check if simulation was successful
    if not data.get('success', False):
        result['success'] = False
        result['error'] = data.get('error', 'Unknown error')
        result['verdict'] = 'SIMULATION_FAILED'
        print(f"  Simulation failed: {result['error']}")
        return result

    # Get trajectory data
    if 'z_trajectory' in data:
        times = np.array([d['time_ns'] for d in data['z_trajectory']])
        z_values = np.array([d['z_nm'] for d in data['z_trajectory']])
    else:
        # Try loading from CSV
        csv_path = MEMBRANE_DIR / f"{peptide_id}_z_trajectory.csv"
        traj_data = load_z_trajectory(csv_path)
        if traj_data is None:
            result['success'] = False
            result['error'] = 'No trajectory data found'
            result['verdict'] = 'NO_DATA'
            print(f"  No trajectory data found")
            return result
        times = traj_data['times_ns']
        z_values = traj_data['z_nm']

    print(f"  Trajectory: {len(z_values)} frames, {times[-1]:.2f} ns")

    # Analyze trajectory
    analysis = analyze_z_trajectory(z_values, times)
    result['analysis'] = analysis

    print(f"\n  Z-coordinate statistics:")
    print(f"    Initial: {analysis['z_initial']:.3f} nm")
    print(f"    Final:   {analysis['z_final']:.3f} nm")
    print(f"    Min:     {analysis['z_min']:.3f} nm")
    print(f"    Max:     {analysis['z_max']:.3f} nm")
    print(f"    Mean:    {analysis['z_mean']:.3f} ± {analysis['z_std']:.3f} nm")

    print(f"\n  Time in each region:")
    for region, fraction in analysis['time_fractions'].items():
        pct = fraction * 100
        print(f"    {region}: {pct:.1f}%")

    print(f"\n  Penetration depth: {analysis['max_penetration_depth']:.2f} nm")
    print(f"  Reached core: {analysis['reached_core']}")
    print(f"  Translocated: {analysis['translocated']}")

    # Assign verdict
    verdict_info = assign_bbb_verdict(analysis)
    result['verdict'] = verdict_info['verdict']
    result['bbb_status'] = verdict_info['bbb_status']
    result['recommendation'] = verdict_info['recommendation']
    result['success'] = True

    print(f"\n  VERDICT: {verdict_info['emoji']} {verdict_info['verdict']}")
    print(f"  BBB Status: {verdict_info['bbb_status']}")
    print(f"  {verdict_info['recommendation']}")

    # Plot
    plot_path = plot_z_trajectory(times, z_values, peptide_id, verdict_info['verdict'])
    if plot_path:
        result['plot_path'] = str(plot_path)
        print(f"\n  Plot: {plot_path}")

    return result


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Analyze all membrane permeability simulations.
    """
    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Blood-Brain Barrier Permeability Analysis',
        'membrane_geometry': {
            'z_water_nm': Z_WATER,
            'z_headgroup_nm': Z_HEADGROUP,
            'z_interface_nm': Z_INTERFACE,
            'z_core_nm': Z_CORE,
        },
        'peptides': {},
    }

    # Load membrane simulation results
    membrane_data = load_membrane_results()

    if membrane_data is None:
        print("No membrane permeability results found.")
        print("Run val_12_membrane_permeability.py first.")

        # Check for individual CSV files
        csv_files = list(MEMBRANE_DIR.glob("*_z_trajectory.csv"))
        if csv_files:
            print(f"\nFound {len(csv_files)} trajectory files, analyzing...")
            for csv_path in csv_files:
                peptide_id = csv_path.stem.replace("_z_trajectory", "")
                traj_data = load_z_trajectory(csv_path)
                if traj_data:
                    # Create mock data dict
                    mock_data = {
                        'success': True,
                        'z_trajectory': [
                            {'time_ns': t, 'z_nm': z}
                            for t, z in zip(traj_data['times_ns'], traj_data['z_nm'])
                        ]
                    }
                    result = analyze_peptide(peptide_id, mock_data)
                    results['peptides'][peptide_id] = result
        else:
            return results
    else:
        # Analyze each peptide
        for peptide_id, data in membrane_data.get('peptides', {}).items():
            result = analyze_peptide(peptide_id, data)
            results['peptides'][peptide_id] = result

    # Summary
    print("\n" + "=" * 80)
    print("BLOOD-BRAIN BARRIER PERMEABILITY SUMMARY")
    print("=" * 80)

    excellent = []
    passing = []
    marginal = []
    failing = []

    for pid, res in results['peptides'].items():
        status = res.get('bbb_status', 'UNKNOWN')
        if status == 'EXCELLENT':
            excellent.append(pid)
        elif status == 'PASS':
            passing.append(pid)
        elif status == 'MARGINAL':
            marginal.append(pid)
        else:
            failing.append(pid)

    print(f"\n  EXCELLENT BBB PENETRATION: {len(excellent)}")
    for p in excellent:
        print(f"    ✓✓ {p}")

    print(f"\n  PASS BBB: {len(passing)}")
    for p in passing:
        print(f"    ✓ {p}")

    print(f"\n  MARGINAL: {len(marginal)}")
    for p in marginal:
        print(f"    ~ {p}")

    print(f"\n  FAIL BBB: {len(failing)}")
    for p in failing:
        print(f"    ✗ {p}")

    results['summary'] = {
        'excellent': excellent,
        'pass': passing,
        'marginal': marginal,
        'fail': failing,
    }

    # CNS drug viability
    cns_viable = excellent + passing
    if cns_viable:
        print("\n" + "=" * 80)
        print("CNS DRUG CANDIDATES (BBB PERMEABLE)")
        print("=" * 80)
        for p in cns_viable:
            print(f"  ✓ {p} - Suitable for CNS targets (Parkinson's, Alzheimer's)")

    # Save results
    json_path = OUTPUT_DIR / "bbb_verdict_results.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results: {json_path}")

    return results


if __name__ == "__main__":
    main()
