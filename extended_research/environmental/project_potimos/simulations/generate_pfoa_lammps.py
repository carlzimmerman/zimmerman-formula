#!/usr/bin/env python3
"""
Generate PFOA structure in LAMMPS data format for ReaxFF simulation.
Project Potimos - PFAS Mineralization Research

PFOA: Perfluorooctanoic acid (C8F17COOH)
Chain length ~11.6 Å ≈ 2Z (where Z = 5.79 Å)

Author: Carl Zimmerman
License: AGPL-3.0
Date: May 2026
"""

import numpy as np
from pathlib import Path

# Bond lengths (Angstroms)
CC_BOND = 1.54
CF_BOND = 1.35
CO_BOND_SINGLE = 1.43
CO_BOND_DOUBLE = 1.23
OH_BOND = 0.97

# Atomic masses
MASSES = {
    'C': 12.011,
    'H': 1.008,
    'O': 15.999,
    'F': 18.998
}

def generate_pfoa_coords():
    """
    Generate PFOA coordinates.
    Structure: CF3-(CF2)6-COOH

    Returns list of (element, x, y, z, charge)
    """
    atoms = []

    # Build perfluorinated chain along x-axis
    x = 0.0

    # 7 CF2 groups + 1 CF3 terminal
    for i in range(7):
        # Carbon
        atoms.append(('C', x, 0.0, 0.0, 0.0))

        # Two fluorines (alternating up/down for tetrahedral geometry)
        angle = np.pi/3 if i % 2 == 0 else -np.pi/3
        atoms.append(('F', x, CF_BOND * np.cos(angle), CF_BOND * np.sin(angle), -0.25))
        atoms.append(('F', x, CF_BOND * np.cos(-angle), CF_BOND * np.sin(-angle), -0.25))

        x += CC_BOND

    # Terminal CF3 group
    atoms.append(('C', x, 0.0, 0.0, 0.0))
    atoms.append(('F', x + CF_BOND * 0.5, CF_BOND * 0.866, 0.0, -0.25))
    atoms.append(('F', x + CF_BOND * 0.5, -CF_BOND * 0.433, CF_BOND * 0.75, -0.25))
    atoms.append(('F', x + CF_BOND * 0.5, -CF_BOND * 0.433, -CF_BOND * 0.75, -0.25))

    # Carboxylic acid group at other end
    x_carboxyl = -CC_BOND
    atoms.append(('C', x_carboxyl, 0.0, 0.0, 0.5))  # Carboxyl carbon
    atoms.append(('O', x_carboxyl - CO_BOND_DOUBLE, 0.7, 0.0, -0.4))  # Carbonyl O
    atoms.append(('O', x_carboxyl - CO_BOND_SINGLE * 0.7, -1.0, 0.0, -0.4))  # Hydroxyl O
    atoms.append(('H', x_carboxyl - CO_BOND_SINGLE * 0.7, -1.0 - OH_BOND, 0.0, 0.3))  # Hydroxyl H

    return atoms

def write_lammps_data(atoms, filename, box_size=50.0):
    """
    Write atoms to LAMMPS data file format.

    Parameters:
    - atoms: list of (element, x, y, z, charge)
    - filename: output file path
    - box_size: cubic box dimension in Angstroms
    """

    # Map elements to type IDs
    element_types = {'C': 1, 'H': 2, 'O': 3, 'F': 4}

    # Center molecule in box
    coords = np.array([(a[1], a[2], a[3]) for a in atoms])
    center = coords.mean(axis=0)
    box_center = box_size / 2
    offset = box_center - center

    with open(filename, 'w') as f:
        f.write("LAMMPS data file for PFOA (C8F17COOH) - Project Potimos\n\n")

        f.write(f"{len(atoms)} atoms\n")
        f.write("4 atom types\n\n")

        f.write(f"0.0 {box_size:.1f} xlo xhi\n")
        f.write(f"0.0 {box_size:.1f} ylo yhi\n")
        f.write(f"0.0 {box_size:.1f} zlo zhi\n\n")

        f.write("Masses\n\n")
        f.write(f"1 {MASSES['C']:.3f}  # C\n")
        f.write(f"2 {MASSES['H']:.3f}  # H\n")
        f.write(f"3 {MASSES['O']:.3f}  # O\n")
        f.write(f"4 {MASSES['F']:.3f}  # F\n\n")

        f.write("Atoms  # charge\n\n")
        for i, (elem, x, y, z, q) in enumerate(atoms, 1):
            type_id = element_types[elem]
            f.write(f"{i} {type_id} {q:.4f} {x + offset[0]:.6f} {y + offset[1]:.6f} {z + offset[2]:.6f}\n")

    print(f"Written {len(atoms)} atoms to {filename}")

    # Print molecule statistics
    chain_length = max(a[1] for a in atoms) - min(a[1] for a in atoms)
    n_fluorine = sum(1 for a in atoms if a[0] == 'F')
    n_carbon = sum(1 for a in atoms if a[0] == 'C')

    print(f"\nMolecule statistics:")
    print(f"  Chain length: {chain_length:.2f} Å")
    print(f"  Z constant: 5.79 Å")
    print(f"  Chain/Z ratio: {chain_length/5.79:.2f}")
    print(f"  Carbons: {n_carbon}")
    print(f"  Fluorines: {n_fluorine}")
    print(f"  C-F bonds to monitor: {n_fluorine}")

def generate_water_box(n_water=100, box_size=50.0, exclude_center=15.0):
    """
    Generate water molecules around PFOA.

    Parameters:
    - n_water: number of water molecules
    - box_size: box dimension
    - exclude_center: radius around center to exclude (for PFOA)
    """
    waters = []
    center = box_size / 2

    np.random.seed(42)  # Reproducibility

    for _ in range(n_water):
        while True:
            x = np.random.uniform(0, box_size)
            y = np.random.uniform(0, box_size)
            z = np.random.uniform(0, box_size)

            # Check if outside exclusion zone
            dist = np.sqrt((x - center)**2 + (y - center)**2 + (z - center)**2)
            if dist > exclude_center:
                break

        # TIP3P-like water geometry
        oh_bond = 0.9572
        hoh_angle = 104.52 * np.pi / 180

        # Oxygen at center
        waters.append(('O', x, y, z, -0.834))

        # Two hydrogens
        waters.append(('H', x + oh_bond, y, z, 0.417))
        waters.append(('H', x + oh_bond * np.cos(hoh_angle),
                       y + oh_bond * np.sin(hoh_angle), z, 0.417))

    return waters

def main():
    output_dir = Path(__file__).parent

    # Generate PFOA
    print("="*60)
    print("PFOA Structure Generator for LAMMPS")
    print("="*60)

    pfoa_atoms = generate_pfoa_coords()

    # Write PFOA only (gas phase)
    write_lammps_data(pfoa_atoms, output_dir / "pfoa_gas.data", box_size=30.0)

    # Generate with water (aqueous phase)
    print("\nGenerating aqueous system...")
    water_atoms = generate_water_box(n_water=200, box_size=50.0, exclude_center=12.0)

    # Combine PFOA and water
    # Need to adjust atom types for water (O=5, H=6 instead of 3, 2)
    combined = []
    for atom in pfoa_atoms:
        combined.append(atom)

    # Write combined system with adjusted types
    with open(output_dir / "pfoa_water.data", 'w') as f:
        total_atoms = len(pfoa_atoms) + len(water_atoms)

        f.write("LAMMPS data file for PFOA in water - Project Potimos\n\n")
        f.write(f"{total_atoms} atoms\n")
        f.write("6 atom types\n\n")

        f.write("0.0 50.0 xlo xhi\n")
        f.write("0.0 50.0 ylo yhi\n")
        f.write("0.0 50.0 zlo zhi\n\n")

        f.write("Masses\n\n")
        f.write(f"1 {MASSES['C']:.3f}  # C (PFOA)\n")
        f.write(f"2 {MASSES['H']:.3f}  # H (PFOA)\n")
        f.write(f"3 {MASSES['O']:.3f}  # O (PFOA)\n")
        f.write(f"4 {MASSES['F']:.3f}  # F (PFOA)\n")
        f.write(f"5 {MASSES['O']:.3f}  # O (water)\n")
        f.write(f"6 {MASSES['H']:.3f}  # H (water)\n\n")

        f.write("Atoms  # charge\n\n")

        # PFOA atoms (centered at 25, 25, 25)
        element_types = {'C': 1, 'H': 2, 'O': 3, 'F': 4}
        coords = np.array([(a[1], a[2], a[3]) for a in pfoa_atoms])
        center = coords.mean(axis=0)
        offset = np.array([25.0, 25.0, 25.0]) - center

        atom_id = 1
        for elem, x, y, z, q in pfoa_atoms:
            type_id = element_types[elem]
            f.write(f"{atom_id} {type_id} {q:.4f} {x + offset[0]:.6f} {y + offset[1]:.6f} {z + offset[2]:.6f}\n")
            atom_id += 1

        # Water atoms
        water_types = {'O': 5, 'H': 6}
        for elem, x, y, z, q in water_atoms:
            type_id = water_types[elem]
            f.write(f"{atom_id} {type_id} {q:.4f} {x:.6f} {y:.6f} {z:.6f}\n")
            atom_id += 1

    print(f"Written {total_atoms} atoms to pfoa_water.data")
    print(f"  PFOA atoms: {len(pfoa_atoms)}")
    print(f"  Water atoms: {len(water_atoms)}")

    print("\n" + "="*60)
    print("FILES GENERATED:")
    print("="*60)
    print(f"  pfoa_gas.data   - PFOA in vacuum (for initial testing)")
    print(f"  pfoa_water.data - PFOA in water box (for production)")
    print("\nNext steps:")
    print("  1. Download ReaxFF parameters: ffield.reax.CHOF")
    print("  2. Run: lmp -in lammps_cf_resonance.in")
    print("  3. Analyze bonds.reaxff for C-F dissociation")

if __name__ == "__main__":
    main()
