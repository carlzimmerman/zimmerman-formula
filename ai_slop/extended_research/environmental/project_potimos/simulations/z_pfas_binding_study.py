#!/usr/bin/env python3
"""
Z²-PFAS Binding Energy Study
Project Potimos - Novel PFAS Remediation Research

This script investigates whether MOF pore diameters related to the
Z constant (Z = √(32π/3) ≈ 5.7888 Å) show enhanced PFAS binding.

Author: Carl Zimmerman
License: AGPL-3.0
Date: May 2026
"""

import numpy as np
from pathlib import Path
import json
import subprocess
from dataclasses import dataclass
from typing import List, Tuple, Optional
import os

# =============================================================================
# Z² FRAMEWORK CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # = 33.510...
Z_CONSTANT = np.sqrt(Z_SQUARED)  # = 5.7888... Å

print(f"Z² = {Z_SQUARED:.6f}")
print(f"Z  = {Z_CONSTANT:.6f} Å")
print(f"2Z = {2*Z_CONSTANT:.6f} Å")
print(f"Z/2 = {Z_CONSTANT/2:.6f} Å")

# =============================================================================
# PFAS MOLECULAR STRUCTURES
# =============================================================================

@dataclass
class PFASMolecule:
    """Represents a PFAS compound with its geometry."""
    name: str
    formula: str
    chain_length: int  # Number of perfluorinated carbons
    estimated_length_A: float  # Extended chain length in Angstroms
    atoms: List[Tuple[str, float, float, float]]  # (element, x, y, z)

def generate_pfas_chain(n_carbons: int) -> List[Tuple[str, float, float, float]]:
    """
    Generate approximate coordinates for a linear perfluoroalkyl chain.
    CnF(2n+1)COOH structure.

    Uses standard bond lengths:
    - C-C: 1.54 Å
    - C-F: 1.35 Å
    - C=O: 1.23 Å
    - C-O: 1.43 Å
    - O-H: 0.97 Å
    """
    atoms = []

    # Build perfluorinated backbone along x-axis
    cc_bond = 1.54  # Å
    cf_bond = 1.35  # Å

    x = 0.0
    for i in range(n_carbons):
        # Carbon atom
        atoms.append(('C', x, 0.0, 0.0))

        # Two fluorines per carbon (except terminal which has 3)
        if i < n_carbons - 1:
            atoms.append(('F', x, cf_bond, 0.0))
            atoms.append(('F', x, -cf_bond, 0.0))
        else:
            # Terminal CF3
            atoms.append(('F', x + cf_bond * 0.5, cf_bond * 0.866, 0.0))
            atoms.append(('F', x + cf_bond * 0.5, -cf_bond * 0.866, 0.0))
            atoms.append(('F', x + cf_bond, 0.0, 0.0))

        x += cc_bond

    # Carboxylic acid group (-COOH)
    x_carboxyl = -cc_bond
    atoms.append(('C', x_carboxyl, 0.0, 0.0))  # Carboxyl carbon
    atoms.append(('O', x_carboxyl - 1.23, 0.5, 0.0))  # Carbonyl O
    atoms.append(('O', x_carboxyl - 0.5, -1.2, 0.0))  # Hydroxyl O
    atoms.append(('H', x_carboxyl - 0.5, -2.17, 0.0))  # Hydroxyl H

    return atoms

def create_pfas_molecules() -> dict:
    """Create dictionary of PFAS molecules for study."""

    molecules = {}

    # PFBA - Perfluorobutanoic acid (C4)
    # Chain length approximately Z
    pfba_atoms = generate_pfas_chain(3)  # C3F7COOH
    molecules['PFBA'] = PFASMolecule(
        name='PFBA',
        formula='C4HF7O2',
        chain_length=4,
        estimated_length_A=5.8,  # Close to Z!
        atoms=pfba_atoms
    )

    # PFHxA - Perfluorohexanoic acid (C6)
    pfhxa_atoms = generate_pfas_chain(5)
    molecules['PFHxA'] = PFASMolecule(
        name='PFHxA',
        formula='C6HF11O2',
        chain_length=6,
        estimated_length_A=8.7,
        atoms=pfhxa_atoms
    )

    # PFOA - Perfluorooctanoic acid (C8)
    # Chain length approximately 2Z
    pfoa_atoms = generate_pfas_chain(7)
    molecules['PFOA'] = PFASMolecule(
        name='PFOA',
        formula='C8HF15O2',
        chain_length=8,
        estimated_length_A=11.6,  # Close to 2Z!
        atoms=pfoa_atoms
    )

    return molecules

# =============================================================================
# MOF PORE MODELS (Simplified Cylindrical Cavity)
# =============================================================================

def generate_cylindrical_pore(diameter_A: float, length_A: float = 20.0,
                              n_rings: int = 4) -> List[Tuple[str, float, float, float]]:
    """
    Generate a simplified cylindrical pore model using oxygen atoms.
    This represents the inner surface of a MOF channel.

    Parameters:
    - diameter_A: Pore diameter in Angstroms
    - length_A: Pore length along z-axis
    - n_rings: Number of oxygen rings defining the pore
    """
    atoms = []
    radius = diameter_A / 2

    # 8 oxygens per ring (simplified MOF-like environment)
    n_per_ring = 8

    for ring in range(n_rings):
        z = (ring / (n_rings - 1)) * length_A - length_A / 2
        for i in range(n_per_ring):
            theta = 2 * np.pi * i / n_per_ring
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            atoms.append(('O', x, y, z))

    return atoms

def generate_pore_sizes() -> List[float]:
    """
    Generate pore sizes to test, centered around Z-related values.

    Key diameters:
    - Z/2 = 2.89 Å (too small for PFAS)
    - Z = 5.79 Å (optimal for PFBA?)
    - 2Z = 11.58 Å (optimal for PFOA?)
    """
    # Scan from 4 Å to 14 Å in 0.5 Å steps
    pore_sizes = np.arange(4.0, 14.5, 0.5)

    # Add exact Z-related values
    z_values = [Z_CONSTANT/2, Z_CONSTANT, 1.5*Z_CONSTANT, 2*Z_CONSTANT]
    pore_sizes = np.unique(np.concatenate([pore_sizes, z_values]))
    pore_sizes.sort()

    return pore_sizes.tolist()

# =============================================================================
# XYZ FILE GENERATION
# =============================================================================

def write_xyz(atoms: List[Tuple[str, float, float, float]],
              filename: str, comment: str = "") -> None:
    """Write atoms to XYZ format file."""
    with open(filename, 'w') as f:
        f.write(f"{len(atoms)}\n")
        f.write(f"{comment}\n")
        for element, x, y, z in atoms:
            f.write(f"{element:2s} {x:12.6f} {y:12.6f} {z:12.6f}\n")

def combine_structures(pore_atoms: List[Tuple[str, float, float, float]],
                       pfas_atoms: List[Tuple[str, float, float, float]],
                       offset: Tuple[float, float, float] = (0, 0, 0)) -> List[Tuple[str, float, float, float]]:
    """Combine pore and PFAS structures, placing PFAS at center of pore."""
    combined = list(pore_atoms)
    for element, x, y, z in pfas_atoms:
        combined.append((element, x + offset[0], y + offset[1], z + offset[2]))
    return combined

# =============================================================================
# xTB CALCULATION INTERFACE
# =============================================================================

def run_xtb_energy(xyz_file: str, charge: int = 0) -> Optional[float]:
    """
    Run xTB single-point energy calculation.
    Returns energy in Hartree, or None if calculation fails.

    Requires xTB to be installed: conda install -c conda-forge xtb
    """
    try:
        result = subprocess.run(
            ['xtb', xyz_file, '--gfn', '2', '--sp', '--chrg', str(charge)],
            capture_output=True,
            text=True,
            timeout=300
        )

        # Parse energy from output
        for line in result.stdout.split('\n'):
            if 'TOTAL ENERGY' in line:
                energy = float(line.split()[3])
                return energy

        return None

    except FileNotFoundError:
        print("ERROR: xTB not found. Install with: conda install -c conda-forge xtb")
        return None
    except subprocess.TimeoutExpired:
        print(f"ERROR: xTB calculation timed out for {xyz_file}")
        return None
    except Exception as e:
        print(f"ERROR: xTB calculation failed: {e}")
        return None

def calculate_binding_energy(e_complex: float, e_pore: float, e_pfas: float) -> float:
    """
    Calculate binding energy.
    E_binding = E_complex - E_pore - E_PFAS

    More negative = stronger binding.
    Returns energy in kcal/mol (converted from Hartree).
    """
    hartree_to_kcal = 627.509  # kcal/mol per Hartree
    e_binding_hartree = e_complex - e_pore - e_pfas
    return e_binding_hartree * hartree_to_kcal

# =============================================================================
# MAIN STUDY EXECUTION
# =============================================================================

def run_binding_study(output_dir: str = "results"):
    """
    Execute the full Z-PFAS binding study.

    1. Generate PFAS structures
    2. Generate MOF pores at various diameters
    3. Calculate binding energies
    4. Analyze correlation with Z
    """

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    structures_dir = Path(output_dir) / "structures"
    structures_dir.mkdir(exist_ok=True)

    print("\n" + "="*60)
    print("Z²-PFAS BINDING ENERGY STUDY")
    print("="*60)

    # Generate PFAS molecules
    print("\nGenerating PFAS structures...")
    pfas_molecules = create_pfas_molecules()

    for name, mol in pfas_molecules.items():
        xyz_file = structures_dir / f"{name}.xyz"
        write_xyz(mol.atoms, str(xyz_file), f"{name} - {mol.formula}")
        print(f"  {name}: chain length ≈ {mol.estimated_length_A:.2f} Å "
              f"(Z = {Z_CONSTANT:.2f} Å, ratio = {mol.estimated_length_A/Z_CONSTANT:.2f})")

    # Generate pore sizes
    print("\nGenerating MOF pore models...")
    pore_sizes = generate_pore_sizes()
    print(f"  Testing {len(pore_sizes)} pore diameters from {min(pore_sizes):.1f} to {max(pore_sizes):.1f} Å")
    print(f"  Z-related sizes: Z/2={Z_CONSTANT/2:.2f}, Z={Z_CONSTANT:.2f}, 2Z={2*Z_CONSTANT:.2f} Å")

    # Generate pore structures
    for diameter in pore_sizes:
        pore_atoms = generate_cylindrical_pore(diameter)
        xyz_file = structures_dir / f"pore_{diameter:.2f}A.xyz"
        write_xyz(pore_atoms, str(xyz_file), f"Cylindrical pore d={diameter:.2f} A")

    # Check if xTB is available
    print("\nChecking xTB availability...")
    test_result = subprocess.run(['which', 'xtb'], capture_output=True)
    xtb_available = test_result.returncode == 0

    if not xtb_available:
        print("  WARNING: xTB not found in PATH")
        print("  Install with: conda install -c conda-forge xtb")
        print("  Generating structure files only (no energy calculations)")

        # Save study parameters
        study_params = {
            'Z_constant': Z_CONSTANT,
            'Z_squared': Z_SQUARED,
            'pore_sizes_A': pore_sizes,
            'pfas_molecules': {name: {
                'formula': mol.formula,
                'chain_length': mol.chain_length,
                'estimated_length_A': mol.estimated_length_A,
                'Z_ratio': mol.estimated_length_A / Z_CONSTANT
            } for name, mol in pfas_molecules.items()},
            'status': 'structures_generated',
            'xtb_available': False
        }

        with open(Path(output_dir) / "study_parameters.json", 'w') as f:
            json.dump(study_params, f, indent=2)

        print(f"\nStructures saved to: {structures_dir}")
        print("Run xTB calculations manually or install xTB to continue.")
        return

    print("  xTB found! Running energy calculations...")

    # Run binding energy calculations
    results = {}

    for pfas_name, pfas_mol in pfas_molecules.items():
        print(f"\n  Calculating binding energies for {pfas_name}...")
        results[pfas_name] = []

        # Calculate isolated PFAS energy
        pfas_xyz = structures_dir / f"{pfas_name}.xyz"
        e_pfas = run_xtb_energy(str(pfas_xyz), charge=-1)  # Deprotonated carboxylate

        if e_pfas is None:
            print(f"    ERROR: Could not calculate {pfas_name} energy")
            continue

        for diameter in pore_sizes:
            # Calculate isolated pore energy
            pore_xyz = structures_dir / f"pore_{diameter:.2f}A.xyz"
            e_pore = run_xtb_energy(str(pore_xyz))

            if e_pore is None:
                continue

            # Generate and calculate complex
            pore_atoms = generate_cylindrical_pore(diameter)
            complex_atoms = combine_structures(pore_atoms, pfas_mol.atoms)
            complex_xyz = structures_dir / f"{pfas_name}_pore_{diameter:.2f}A.xyz"
            write_xyz(complex_atoms, str(complex_xyz), f"{pfas_name} in pore d={diameter:.2f} A")

            e_complex = run_xtb_energy(str(complex_xyz), charge=-1)

            if e_complex is None:
                continue

            e_binding = calculate_binding_energy(e_complex, e_pore, e_pfas)

            results[pfas_name].append({
                'pore_diameter_A': diameter,
                'binding_energy_kcal_mol': e_binding,
                'diameter_over_Z': diameter / Z_CONSTANT
            })

            print(f"    d={diameter:.2f} Å (d/Z={diameter/Z_CONSTANT:.2f}): "
                  f"E_bind = {e_binding:.2f} kcal/mol")

    # Save results
    with open(Path(output_dir) / "binding_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    # Analyze Z-correlation
    print("\n" + "="*60)
    print("Z-CORRELATION ANALYSIS")
    print("="*60)

    for pfas_name, data in results.items():
        if not data:
            continue

        diameters = [d['pore_diameter_A'] for d in data]
        energies = [d['binding_energy_kcal_mol'] for d in data]

        # Find optimal pore size
        min_idx = np.argmin(energies)
        optimal_d = diameters[min_idx]
        optimal_e = energies[min_idx]

        print(f"\n{pfas_name}:")
        print(f"  Optimal pore diameter: {optimal_d:.2f} Å")
        print(f"  Optimal binding energy: {optimal_e:.2f} kcal/mol")
        print(f"  Ratio to Z: {optimal_d/Z_CONSTANT:.3f}")
        print(f"  Ratio to 2Z: {optimal_d/(2*Z_CONSTANT):.3f}")

        # Check proximity to Z-values
        z_proximity = min(
            abs(optimal_d - Z_CONSTANT),
            abs(optimal_d - 2*Z_CONSTANT),
            abs(optimal_d - Z_CONSTANT/2)
        )
        print(f"  Closest Z-value offset: {z_proximity:.2f} Å")

if __name__ == "__main__":
    # Create output directory in project folder
    script_dir = Path(__file__).parent
    output_dir = script_dir / "binding_study_results"

    run_binding_study(str(output_dir))

    print("\n" + "="*60)
    print("STUDY COMPLETE")
    print("="*60)
    print(f"Results saved to: {output_dir}")
    print("\nNext steps:")
    print("1. If xTB not installed: conda install -c conda-forge xtb")
    print("2. Re-run this script to perform energy calculations")
    print("3. Analyze binding_results.json for Z-correlation")
