#!/usr/bin/env python3
"""
Quick Z-scan: Focused binding energy scan around Z and 2Z values.
Project Potimos
"""

import numpy as np
import subprocess
from pathlib import Path

Z_CONSTANT = np.sqrt(32 * np.pi / 3)  # 5.7888 Å

def write_xyz(atoms, filename, comment=""):
    with open(filename, 'w') as f:
        f.write(f"{len(atoms)}\n{comment}\n")
        for elem, x, y, z in atoms:
            f.write(f"{elem:2s} {x:12.6f} {y:12.6f} {z:12.6f}\n")

def generate_pore(diameter, n_rings=4, length=20.0):
    atoms = []
    radius = diameter / 2
    for ring in range(n_rings):
        z = (ring / (n_rings - 1)) * length - length / 2
        for i in range(8):
            theta = 2 * np.pi * i / 8
            atoms.append(('O', radius * np.cos(theta), radius * np.sin(theta), z))
    return atoms

def generate_pfba():
    """Simple PFBA: C4F7COOH"""
    atoms = []
    cc, cf = 1.54, 1.35
    x = 0.0
    for i in range(3):
        atoms.append(('C', x, 0, 0))
        atoms.append(('F', x, cf, 0))
        atoms.append(('F', x, -cf, 0))
        x += cc
    # Terminal CF3
    atoms.append(('C', x, 0, 0))
    atoms.append(('F', x + cf*0.5, cf*0.866, 0))
    atoms.append(('F', x + cf*0.5, -cf*0.866, 0))
    atoms.append(('F', x + cf, 0, 0))
    # COOH
    atoms.append(('C', -cc, 0, 0))
    atoms.append(('O', -cc - 1.23, 0.5, 0))
    atoms.append(('O', -cc - 0.5, -1.2, 0))
    atoms.append(('H', -cc - 0.5, -2.17, 0))
    return atoms

def run_xtb(xyz_file, charge=0):
    try:
        result = subprocess.run(
            ['xtb', xyz_file, '--gfn', '2', '--sp', '--chrg', str(charge)],
            capture_output=True, text=True, timeout=120
        )
        for line in result.stdout.split('\n'):
            if 'TOTAL ENERGY' in line:
                return float(line.split()[3])
    except Exception as e:
        print(f"  Error: {e}")
    return None

def main():
    out_dir = Path("quick_scan")
    out_dir.mkdir(exist_ok=True)

    # Test diameters: focused around Z and 2Z
    diameters = [
        5.0, 5.5, 5.79, 6.0, 6.5, 7.0, 7.5, 8.0, 8.68,  # around Z
        9.0, 10.0, 10.5, 11.0, 11.58, 12.0, 12.5, 13.0, 14.0  # around 2Z
    ]

    print(f"Z = {Z_CONSTANT:.4f} Å, 2Z = {2*Z_CONSTANT:.4f} Å")
    print(f"1.5Z = {1.5*Z_CONSTANT:.4f} Å")
    print("\nScanning pore diameters for PFBA...\n")

    # Generate PFBA
    pfba = generate_pfba()
    pfba_file = out_dir / "pfba.xyz"
    write_xyz(pfba, str(pfba_file), "PFBA")

    # Get isolated PFBA energy
    print("Calculating isolated PFBA energy...")
    e_pfba = run_xtb(str(pfba_file), charge=-1)
    if e_pfba is None:
        print("Failed to calculate PFBA energy!")
        return
    print(f"  E_PFBA = {e_pfba:.6f} Hartree\n")

    results = []

    for d in diameters:
        # Pore
        pore = generate_pore(d)
        pore_file = out_dir / f"pore_{d:.2f}.xyz"
        write_xyz(pore, str(pore_file), f"Pore d={d}")

        e_pore = run_xtb(str(pore_file))
        if e_pore is None:
            print(f"  d={d:.2f} Å: PORE FAILED")
            continue

        # Complex
        complex_atoms = list(pore) + list(pfba)
        complex_file = out_dir / f"complex_{d:.2f}.xyz"
        write_xyz(complex_atoms, str(complex_file), f"PFBA@pore d={d}")

        e_complex = run_xtb(str(complex_file), charge=-1)
        if e_complex is None:
            print(f"  d={d:.2f} Å: COMPLEX FAILED")
            continue

        # Binding energy
        e_bind = (e_complex - e_pore - e_pfba) * 627.509  # kcal/mol
        ratio = d / Z_CONSTANT

        marker = ""
        if abs(ratio - 1.0) < 0.02:
            marker = " <-- Z"
        elif abs(ratio - 1.5) < 0.02:
            marker = " <-- 1.5Z"
        elif abs(ratio - 2.0) < 0.02:
            marker = " <-- 2Z"

        print(f"  d={d:5.2f} Å (d/Z={ratio:.2f}): E_bind = {e_bind:8.2f} kcal/mol{marker}")
        results.append((d, ratio, e_bind))

    # Analysis
    if results:
        print("\n" + "="*60)
        print("ANALYSIS")
        print("="*60)

        diams, ratios, energies = zip(*results)
        min_idx = np.argmin(energies)

        print(f"\nOptimal pore: d = {diams[min_idx]:.2f} Å (d/Z = {ratios[min_idx]:.2f})")
        print(f"Binding energy: {energies[min_idx]:.2f} kcal/mol")

        # Check for local minima
        print("\nLooking for local minima (peaks in binding strength)...")
        for i in range(1, len(energies)-1):
            if energies[i] < energies[i-1] and energies[i] < energies[i+1]:
                print(f"  Local minimum at d = {diams[i]:.2f} Å (d/Z = {ratios[i]:.2f})")

if __name__ == "__main__":
    main()
