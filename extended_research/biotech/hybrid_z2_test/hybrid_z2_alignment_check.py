#!/usr/bin/env python3
"""
Hybrid Z² Alignment Check - The Moment of Truth

SPDX-License-Identifier: AGPL-3.0-or-later

This script compares the Z²-constrained hybrid structure against
the standard AMBER empirical result to determine:

1. Did the Z² metric LOWER the overall thermodynamic energy?
   (Would indicate Z² captures real physics)

2. What is the RMSD divergence between classical 3D physics
   and our 8D hybrid physics?
   (Shows how much the structures differ)

THE CRITICAL QUESTION:
If Z² = 32π/3 and θ_Z² = π/Z encode fundamental geometry that
extends to biology, then Z²-constrained proteins should:
- Have LOWER or SIMILAR energy to pure AMBER
- Show backbone angles that naturally cluster at Z² multiples

If Z² BREAKS the physics:
- Energy will be HIGHER (structure is stressed)
- RMSD will be large (structure is distorted)

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import os
import sys
import json
import numpy as np
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.7888
Z2 = Z ** 2  # ≈ 33.51
THETA_Z2 = np.pi / Z  # ≈ 31.09°
THETA_Z2_DEG = np.degrees(THETA_Z2)

# ==============================================================================
# STRUCTURE COMPARISON
# ==============================================================================

class StructureAnalyzer:
    """
    Compare two protein structures.

    Calculates:
    - RMSD (Root Mean Square Deviation)
    - Energy comparison
    - Backbone angle analysis
    """

    def __init__(self, pdb_path: str, name: str = "structure"):
        self.pdb_path = pdb_path
        self.name = name
        self.atoms = []
        self.ca_coords = []
        self.backbone_coords = []
        self._parse()

    def _parse(self):
        """Parse PDB file."""
        with open(self.pdb_path, 'r') as f:
            for line in f:
                if line.startswith('ATOM'):
                    try:
                        atom = {
                            'serial': int(line[6:11]),
                            'name': line[12:16].strip(),
                            'resname': line[17:20].strip(),
                            'chain': line[21],
                            'resid': int(line[22:26]),
                            'x': float(line[30:38]),
                            'y': float(line[38:46]),
                            'z': float(line[46:54])
                        }
                        self.atoms.append(atom)

                        if atom['name'] == 'CA':
                            self.ca_coords.append([atom['x'], atom['y'], atom['z']])

                        if atom['name'] in ['N', 'CA', 'C', 'O']:
                            self.backbone_coords.append([atom['x'], atom['y'], atom['z']])

                    except (ValueError, IndexError):
                        pass

        self.ca_coords = np.array(self.ca_coords)
        self.backbone_coords = np.array(self.backbone_coords)

    def get_ca_coords(self) -> np.ndarray:
        """Get CA atom coordinates."""
        return self.ca_coords

    def get_backbone_coords(self) -> np.ndarray:
        """Get backbone atom coordinates."""
        return self.backbone_coords


def calculate_rmsd(coords1: np.ndarray, coords2: np.ndarray) -> float:
    """
    Calculate RMSD between two coordinate sets.

    Uses Kabsch algorithm for optimal superposition.
    """
    if len(coords1) != len(coords2):
        # Truncate to common length
        min_len = min(len(coords1), len(coords2))
        coords1 = coords1[:min_len]
        coords2 = coords2[:min_len]

    if len(coords1) == 0:
        return float('inf')

    # Center coordinates
    center1 = coords1.mean(axis=0)
    center2 = coords2.mean(axis=0)

    coords1_centered = coords1 - center1
    coords2_centered = coords2 - center2

    # Kabsch algorithm for optimal rotation
    H = coords1_centered.T @ coords2_centered
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    # Handle reflection
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T

    # Rotate coords2
    coords2_rotated = coords2_centered @ R

    # Calculate RMSD
    diff = coords1_centered - coords2_rotated
    rmsd = np.sqrt(np.mean(np.sum(diff ** 2, axis=1)))

    return rmsd


def calculate_energy(pdb_path: str) -> Optional[float]:
    """
    Calculate potential energy using OpenMM.
    """
    try:
        from openmm.app import PDBFile, ForceField, Modeller, Simulation, NoCutoff, HBonds
        from openmm import LangevinMiddleIntegrator, Platform, unit

        pdb = PDBFile(pdb_path)
        modeller = Modeller(pdb.topology, pdb.positions)

        forcefield = ForceField('amber14-all.xml', 'implicit/obc2.xml')

        try:
            modeller.addHydrogens(forcefield)
        except Exception:
            pass

        system = forcefield.createSystem(
            modeller.topology,
            nonbondedMethod=NoCutoff,
            constraints=HBonds
        )

        integrator = LangevinMiddleIntegrator(
            300 * unit.kelvin,
            1.0 / unit.picoseconds,
            2.0 * unit.femtoseconds
        )

        simulation = Simulation(modeller.topology, system, integrator)
        simulation.context.setPositions(modeller.positions)

        state = simulation.context.getState(getEnergy=True)
        energy = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)

        return energy

    except ImportError:
        return None
    except Exception as e:
        print(f"    Energy calculation error: {e}")
        return None


def analyze_backbone_angles(analyzer: StructureAnalyzer) -> Dict:
    """
    Analyze backbone dihedral angles and Z² alignment.
    """
    ca_coords = analyzer.ca_coords

    if len(ca_coords) < 4:
        return {'error': 'Not enough CA atoms'}

    # Calculate pseudo-dihedrals from CA trace
    angles = []
    for i in range(1, len(ca_coords) - 2):
        p1, p2, p3, p4 = ca_coords[i-1:i+3]

        # Dihedral calculation
        b1 = p2 - p1
        b2 = p3 - p2
        b3 = p4 - p3

        n1 = np.cross(b1, b2)
        n2 = np.cross(b2, b3)

        n1_norm = np.linalg.norm(n1)
        n2_norm = np.linalg.norm(n2)

        if n1_norm > 1e-8 and n2_norm > 1e-8:
            n1 = n1 / n1_norm
            n2 = n2 / n2_norm

            cos_angle = np.clip(np.dot(n1, n2), -1, 1)
            angle = np.degrees(np.arccos(cos_angle))
            angles.append(angle)

    if not angles:
        return {'error': 'No angles calculated'}

    # Z² alignment
    def z2_deviation(angle_deg):
        n = round(angle_deg / THETA_Z2_DEG)
        return abs(angle_deg - n * THETA_Z2_DEG)

    deviations = [z2_deviation(a) for a in angles]
    mean_dev = np.mean(deviations)
    random_expected = THETA_Z2_DEG / 4  # ~7.8°

    return {
        'n_angles': len(angles),
        'mean_angle': float(np.mean(angles)),
        'std_angle': float(np.std(angles)),
        'mean_z2_deviation': float(mean_dev),
        'random_expected': float(random_expected),
        'z2_alignment_ratio': float(random_expected / mean_dev) if mean_dev > 0 else 0
    }


# ==============================================================================
# MAIN COMPARISON
# ==============================================================================

def compare_structures(
    standard_pdb: str,
    hybrid_pdb: str,
    output_dir: str = "."
) -> Dict:
    """
    Compare standard AMBER structure with Z² hybrid structure.

    Args:
        standard_pdb: Path to standard AMBER-relaxed structure
        hybrid_pdb: Path to Z² hybrid-relaxed structure
        output_dir: Output directory for results

    Returns:
        Comparison results dictionary
    """
    print("\n" + "="*70)
    print("Z² ALIGNMENT CHECK - THE MOMENT OF TRUTH")
    print("="*70)
    print(f"Standard (AMBER): {standard_pdb}")
    print(f"Hybrid (Z² + AMBER): {hybrid_pdb}")
    print("="*70)

    results = {
        'standard_pdb': standard_pdb,
        'hybrid_pdb': hybrid_pdb,
        'Z': float(Z),
        'Z2': float(Z2),
        'theta_Z2_deg': float(THETA_Z2_DEG),
        'timestamp': datetime.now().isoformat(),
        'license': 'AGPL-3.0-or-later'
    }

    # Load structures
    print("\n  [1] Loading structures...")

    standard = StructureAnalyzer(standard_pdb, "Standard AMBER")
    hybrid = StructureAnalyzer(hybrid_pdb, "Z² Hybrid")

    print(f"      Standard: {len(standard.ca_coords)} CA atoms")
    print(f"      Hybrid: {len(hybrid.ca_coords)} CA atoms")

    # Calculate RMSD
    print("\n  [2] Calculating RMSD...")

    ca_rmsd = calculate_rmsd(standard.ca_coords, hybrid.ca_coords)
    backbone_rmsd = calculate_rmsd(standard.backbone_coords, hybrid.backbone_coords)

    print(f"      CA RMSD: {ca_rmsd:.3f} Å")
    print(f"      Backbone RMSD: {backbone_rmsd:.3f} Å")

    results['rmsd'] = {
        'ca_rmsd_angstrom': float(ca_rmsd),
        'backbone_rmsd_angstrom': float(backbone_rmsd)
    }

    # Calculate energies
    print("\n  [3] Calculating energies...")

    standard_energy = calculate_energy(standard_pdb)
    hybrid_energy = calculate_energy(hybrid_pdb)

    if standard_energy is not None and hybrid_energy is not None:
        energy_diff = hybrid_energy - standard_energy
        print(f"      Standard energy: {standard_energy:.2f} kJ/mol")
        print(f"      Hybrid energy: {hybrid_energy:.2f} kJ/mol")
        print(f"      Difference: {energy_diff:+.2f} kJ/mol")

        results['energy'] = {
            'standard_kJ': float(standard_energy),
            'hybrid_kJ': float(hybrid_energy),
            'difference_kJ': float(energy_diff)
        }
    else:
        print("      Energy calculation not available (OpenMM not installed)")
        results['energy'] = {'error': 'OpenMM not available'}

    # Analyze backbone angles
    print("\n  [4] Analyzing backbone angles...")

    standard_angles = analyze_backbone_angles(standard)
    hybrid_angles = analyze_backbone_angles(hybrid)

    if 'error' not in standard_angles:
        print(f"\n      Standard structure:")
        print(f"        Mean Z² deviation: {standard_angles['mean_z2_deviation']:.2f}°")
        print(f"        Z² alignment ratio: {standard_angles['z2_alignment_ratio']:.2f}x")

    if 'error' not in hybrid_angles:
        print(f"\n      Hybrid structure:")
        print(f"        Mean Z² deviation: {hybrid_angles['mean_z2_deviation']:.2f}°")
        print(f"        Z² alignment ratio: {hybrid_angles['z2_alignment_ratio']:.2f}x")

    results['backbone_analysis'] = {
        'standard': standard_angles,
        'hybrid': hybrid_angles
    }

    # ==============================================================================
    # THE VERDICT
    # ==============================================================================
    print("\n" + "="*70)
    print("THE VERDICT")
    print("="*70)

    verdict = {
        'energy_test': 'UNKNOWN',
        'rmsd_test': 'UNKNOWN',
        'z2_alignment_test': 'UNKNOWN',
        'overall': 'UNKNOWN'
    }

    # Test 1: Energy
    if 'energy' in results and 'difference_kJ' in results['energy']:
        diff = results['energy']['difference_kJ']
        if diff < -10:
            verdict['energy_test'] = 'Z² LOWERS energy significantly'
            print(f"\n  ENERGY TEST: ✓ Z² IMPROVED energy by {-diff:.1f} kJ/mol")
        elif diff < 10:
            verdict['energy_test'] = 'Z² has similar energy'
            print(f"\n  ENERGY TEST: ~ Z² has similar energy (±{abs(diff):.1f} kJ/mol)")
        else:
            verdict['energy_test'] = 'Z² RAISES energy (unfavorable)'
            print(f"\n  ENERGY TEST: ✗ Z² RAISED energy by {diff:.1f} kJ/mol")
    else:
        print("\n  ENERGY TEST: ? Cannot calculate (need OpenMM)")

    # Test 2: RMSD
    if ca_rmsd < 1.0:
        verdict['rmsd_test'] = 'Very similar structures'
        print(f"\n  RMSD TEST: ✓ Structures are very similar (RMSD = {ca_rmsd:.2f} Å)")
    elif ca_rmsd < 3.0:
        verdict['rmsd_test'] = 'Moderate structural difference'
        print(f"\n  RMSD TEST: ~ Moderate structural difference (RMSD = {ca_rmsd:.2f} Å)")
    else:
        verdict['rmsd_test'] = 'Large structural divergence'
        print(f"\n  RMSD TEST: ✗ Large structural divergence (RMSD = {ca_rmsd:.2f} Å)")

    # Test 3: Z² alignment improvement
    if 'error' not in standard_angles and 'error' not in hybrid_angles:
        std_ratio = standard_angles['z2_alignment_ratio']
        hyb_ratio = hybrid_angles['z2_alignment_ratio']

        if hyb_ratio > std_ratio * 1.1:
            verdict['z2_alignment_test'] = 'Z² constraints improved alignment'
            print(f"\n  Z² ALIGNMENT TEST: ✓ Hybrid shows better Z² alignment")
            print(f"      Standard ratio: {std_ratio:.2f}x")
            print(f"      Hybrid ratio: {hyb_ratio:.2f}x")
        else:
            verdict['z2_alignment_test'] = 'Z² constraints did not improve alignment'
            print(f"\n  Z² ALIGNMENT TEST: ✗ No improvement in Z² alignment")
    else:
        print("\n  Z² ALIGNMENT TEST: ? Cannot analyze backbone")

    # Overall verdict
    print("\n" + "-"*70)
    print("OVERALL CONCLUSION")
    print("-"*70)

    # Count positive results
    positives = sum(1 for v in verdict.values() if '✓' in str(v) or 'LOWER' in str(v))
    negatives = sum(1 for v in verdict.values() if '✗' in str(v) or 'RAISE' in str(v))

    if positives >= 2:
        verdict['overall'] = 'Z² shows alignment with empirical physics'
        print("\n  *** Z² SHOWS ALIGNMENT WITH EMPIRICAL PROTEIN PHYSICS ***")
        print("  The 8D Kaluza-Klein geometry appears to capture real physical constraints.")
    elif negatives >= 2:
        verdict['overall'] = 'Z² does NOT align with empirical physics'
        print("\n  *** Z² does NOT align with empirical protein physics ***")
        print("  The 8D geometry may not extend to molecular biology.")
    else:
        verdict['overall'] = 'Inconclusive - more testing needed'
        print("\n  *** INCONCLUSIVE - More testing needed ***")
        print("  Results are mixed. Try different proteins and longer simulations.")

    results['verdict'] = verdict

    # Save results
    results_file = os.path.join(output_dir, "z2_alignment_verdict.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results saved: {results_file}")

    return results


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Run alignment check on Z² hybrid vs standard structures."""
    print("\n" + "="*70)
    print("HYBRID Z² ALIGNMENT CHECK")
    print("="*70)
    print("Question: Does Z² geometry align with empirical protein physics?")
    print("License: AGPL-3.0-or-later")
    print("="*70)

    output_dir = "hybrid_z2_test"

    # Check for required files
    standard_pdb = os.path.join(output_dir, "1IYT_md_ready.pdb")
    hybrid_pdb = os.path.join(output_dir, "z2_hybrid_relaxed.pdb")

    # If hybrid doesn't exist, use the same as standard for testing
    if not os.path.exists(hybrid_pdb):
        print(f"\n  WARNING: Hybrid structure not found: {hybrid_pdb}")
        print("  Run hybrid_z2_openmm_engine.py first")

        # Check if raw structure exists
        if os.path.exists(os.path.join(output_dir, "1IYT.pdb")):
            standard_pdb = os.path.join(output_dir, "1IYT.pdb")
            hybrid_pdb = standard_pdb  # Compare to self for testing
            print(f"  Using {standard_pdb} for both (self-comparison test)")
        else:
            print("\n  Run api_polite_structure_fetcher.py first")
            return {'error': 'No structures found'}

    if not os.path.exists(standard_pdb):
        print(f"\n  ERROR: Standard structure not found: {standard_pdb}")
        return {'error': 'Standard structure not found'}

    try:
        results = compare_structures(standard_pdb, hybrid_pdb, output_dir)
        return results

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}


if __name__ == '__main__':
    main()
