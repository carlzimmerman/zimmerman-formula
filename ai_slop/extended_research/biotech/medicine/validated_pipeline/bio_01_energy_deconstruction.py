#!/usr/bin/env python3
"""
bio_01_energy_deconstruction.py

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

bio_01_energy_deconstruction.py - Quantum-to-Classical Energy Deconstructor

Breaks down the Gibbs Free Energy (ΔG = ΔH - TΔS) of a folded protein into
its fundamental physical force components:

1. Coulomb Electrostatics - U(1) gauge interactions (charge-charge)
2. Lennard-Jones Attractive - London dispersion forces (induced dipoles)
3. Lennard-Jones Repulsive - Pauli exclusion (electron cloud overlap)
4. Solvation Free Energy - Cost of displacing structured water

Biology is applied electromagnetism. Before we hack it, we must understand
which force dictates the geometric shape.

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import csv
import urllib.request

try:
    from openmm import *
    from openmm.app import *
    from openmm.unit import *
    OPENMM_AVAILABLE = True
except ImportError:
    OPENMM_AVAILABLE = False
    print("WARNING: OpenMM not available. Using analytical approximations.")

OUTPUT_DIR = Path(__file__).parent / "results" / "energy_deconstruction"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("QUANTUM-TO-CLASSICAL ENERGY DECONSTRUCTOR")
print("Breaking Biology into Fundamental Physical Forces")
print("=" * 80)
print()

# =============================================================================
# PHYSICAL CONSTANTS (from Z² framework where applicable)
# =============================================================================

# Fundamental constants
BOLTZMANN_KJ = 0.008314463  # kJ/(mol·K)
TEMPERATURE = 310.0  # K (physiological)
RT = BOLTZMANN_KJ * TEMPERATURE  # ~2.58 kJ/mol

# Conversion factors
KJ_TO_KCAL = 0.239006
KCAL_TO_KJ = 4.184

# Dielectric constants
VACUUM_DIELECTRIC = 1.0
WATER_DIELECTRIC = 78.5  # at 310K
PROTEIN_INTERIOR_DIELECTRIC = 4.0  # hydrophobic core

print(f"Temperature: {TEMPERATURE} K")
print(f"RT = {RT:.4f} kJ/mol = {RT * KJ_TO_KCAL:.4f} kcal/mol")
print()


# =============================================================================
# PDB HANDLING
# =============================================================================

def download_pdb(pdb_id: str) -> Path:
    """Download PDB file from RCSB."""
    pdb_path = OUTPUT_DIR / f"{pdb_id}.pdb"
    if not pdb_path.exists():
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        print(f"Downloading {pdb_id} from RCSB...")
        urllib.request.urlretrieve(url, pdb_path)
    return pdb_path


def parse_pdb_for_analysis(pdb_path: Path) -> dict:
    """Parse PDB for energy analysis."""
    atoms = []
    coords = []

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                try:
                    atom_name = line[12:16].strip()
                    res_name = line[17:20].strip()
                    res_num = int(line[22:26])
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    element = line[76:78].strip() or atom_name[0]

                    # Skip hydrogens for heavy-atom analysis
                    if element == 'H':
                        continue

                    atoms.append({
                        'name': atom_name,
                        'res_name': res_name,
                        'res_num': res_num,
                        'element': element,
                        'coords': np.array([x, y, z])
                    })
                    coords.append([x, y, z])
                except (ValueError, IndexError):
                    continue

    return {
        'atoms': atoms,
        'coords': np.array(coords),
        'n_atoms': len(atoms)
    }


# =============================================================================
# FORCE FIELD PARAMETERS (Amber ff14SB approximations)
# =============================================================================

# Partial charges (elementary charge units)
PARTIAL_CHARGES = {
    # Backbone
    'N': -0.4157, 'H': 0.2719, 'CA': 0.0337, 'HA': 0.0823,
    'C': 0.5973, 'O': -0.5679,
    # Common sidechains (simplified)
    'CB': -0.0825, 'CG': -0.0061, 'CD': -0.0086,
    'NE': -0.5295, 'CZ': 0.8076, 'NH1': -0.8627, 'NH2': -0.8627,
    'OG': -0.6546, 'OG1': -0.6761, 'OD1': -0.8014, 'OD2': -0.8014,
    'NZ': -0.3854, 'CE': -0.0176, 'SD': -0.2737,
}

# Lennard-Jones parameters (sigma in Å, epsilon in kcal/mol)
LJ_PARAMS = {
    'C': {'sigma': 3.40, 'epsilon': 0.086},
    'N': {'sigma': 3.25, 'epsilon': 0.170},
    'O': {'sigma': 2.96, 'epsilon': 0.210},
    'S': {'sigma': 3.56, 'epsilon': 0.250},
    'H': {'sigma': 2.50, 'epsilon': 0.020},
}

# Atomic solvation parameters (kcal/mol/Å²)
SOLVATION_PARAMS = {
    'C': 0.012,   # Hydrophobic, costs energy to expose
    'N': -0.068,  # Polar, favorable to solvate
    'O': -0.082,  # Polar, favorable to solvate
    'S': 0.012,   # Mildly hydrophobic
}

# Approximate surface areas per atom type (Å²)
ATOM_SASA = {
    'C': 15.0, 'N': 12.0, 'O': 10.0, 'S': 18.0
}


# =============================================================================
# ENERGY CALCULATION FUNCTIONS
# =============================================================================

def calculate_coulomb_energy(atoms: list, coords: np.ndarray) -> dict:
    """
    Calculate Coulomb electrostatic energy.

    E_coulomb = (1/4πε₀) × Σᵢⱼ (qᵢqⱼ)/(εᵣ × rᵢⱼ)

    This is the U(1) gauge interaction - the fundamental electromagnetic force.
    """
    n = len(atoms)
    COULOMB_CONST = 332.0636  # kcal·Å/(mol·e²)

    total_coulomb = 0.0
    favorable = 0.0  # Opposite charges
    unfavorable = 0.0  # Like charges

    for i in range(n):
        qi = PARTIAL_CHARGES.get(atoms[i]['name'], 0.0)

        for j in range(i + 1, n):
            qj = PARTIAL_CHARGES.get(atoms[j]['name'], 0.0)

            if qi == 0 or qj == 0:
                continue

            rij = np.linalg.norm(coords[i] - coords[j])
            if rij < 1.0:  # Skip bonded atoms
                continue

            # Use distance-dependent dielectric
            if rij < 4.0:
                epsilon_r = PROTEIN_INTERIOR_DIELECTRIC
            else:
                epsilon_r = WATER_DIELECTRIC

            E_pair = COULOMB_CONST * qi * qj / (epsilon_r * rij)
            total_coulomb += E_pair

            if E_pair < 0:
                favorable += E_pair
            else:
                unfavorable += E_pair

    return {
        'total_kcal': total_coulomb,
        'favorable_kcal': favorable,
        'unfavorable_kcal': unfavorable,
        'description': 'Coulomb electrostatics (U(1) gauge)'
    }


def calculate_lennard_jones(atoms: list, coords: np.ndarray) -> dict:
    """
    Calculate Lennard-Jones energy (van der Waals).

    E_LJ = Σᵢⱼ 4ε[(σ/r)¹² - (σ/r)⁶]

    The r⁻¹² term is Pauli repulsion (electron cloud overlap).
    The r⁻⁶ term is London dispersion (induced dipole attraction).
    """
    n = len(atoms)

    total_lj = 0.0
    attractive = 0.0  # r⁻⁶ term (London dispersion)
    repulsive = 0.0   # r⁻¹² term (Pauli exclusion)

    for i in range(n):
        elem_i = atoms[i]['element']
        params_i = LJ_PARAMS.get(elem_i, LJ_PARAMS['C'])

        for j in range(i + 1, n):
            elem_j = atoms[j]['element']
            params_j = LJ_PARAMS.get(elem_j, LJ_PARAMS['C'])

            # Lorentz-Berthelot combining rules
            sigma = (params_i['sigma'] + params_j['sigma']) / 2
            epsilon = np.sqrt(params_i['epsilon'] * params_j['epsilon'])

            rij = np.linalg.norm(coords[i] - coords[j])

            # Skip bonded (< 1.6 Å) and very close atoms
            if rij < 1.6:
                continue

            ratio = sigma / rij
            ratio6 = ratio ** 6
            ratio12 = ratio6 ** 2

            E_repulsive = 4 * epsilon * ratio12
            E_attractive = -4 * epsilon * ratio6

            total_lj += E_repulsive + E_attractive
            repulsive += E_repulsive
            attractive += E_attractive

    return {
        'total_kcal': total_lj,
        'attractive_kcal': attractive,  # London dispersion
        'repulsive_kcal': repulsive,    # Pauli exclusion
        'description': 'Lennard-Jones (VdW)'
    }


def calculate_solvation_energy(atoms: list, coords: np.ndarray) -> dict:
    """
    Estimate solvation free energy using implicit solvent model.

    ΔG_solv ≈ Σᵢ (γᵢ × SASA_i)

    This represents the thermodynamic cost of displacing structured water.
    Hydrophobic atoms cost energy to solvate; polar atoms gain energy.
    """
    n = len(atoms)

    total_solvation = 0.0
    hydrophobic_penalty = 0.0
    polar_gain = 0.0

    # Simple exposure calculation (neighbor counting)
    for i in range(n):
        elem = atoms[i]['element']
        gamma = SOLVATION_PARAMS.get(elem, 0.012)
        base_sasa = ATOM_SASA.get(elem, 15.0)

        # Count neighbors to estimate burial
        neighbors = 0
        for j in range(n):
            if i != j:
                rij = np.linalg.norm(coords[i] - coords[j])
                if rij < 5.0:
                    neighbors += 1

        # Burial fraction (more neighbors = more buried)
        burial = min(1.0, neighbors / 12.0)
        exposed_sasa = base_sasa * (1 - burial)

        E_solv = gamma * exposed_sasa
        total_solvation += E_solv

        if gamma > 0:
            hydrophobic_penalty += E_solv
        else:
            polar_gain += E_solv

    return {
        'total_kcal': total_solvation,
        'hydrophobic_penalty_kcal': hydrophobic_penalty,
        'polar_gain_kcal': polar_gain,
        'description': 'Solvation free energy'
    }


def calculate_hydrogen_bonds(atoms: list, coords: np.ndarray) -> dict:
    """
    Estimate hydrogen bond energy.

    Strong H-bonds: -2 to -5 kcal/mol each
    Typical in protein: backbone N-H...O=C
    """
    n = len(atoms)

    total_hbond = 0.0
    n_hbonds = 0

    # Find potential donors (N) and acceptors (O)
    donors = [(i, a) for i, a in enumerate(atoms) if a['element'] == 'N']
    acceptors = [(i, a) for i, a in enumerate(atoms) if a['element'] == 'O']

    for di, donor in donors:
        for ai, acceptor in acceptors:
            # Must be different residues
            if abs(donor['res_num'] - acceptor['res_num']) < 2:
                continue

            r = np.linalg.norm(coords[di] - coords[ai])

            # H-bond distance criterion: 2.5-3.5 Å for N...O
            if 2.5 < r < 3.5:
                # Approximate H-bond energy based on distance
                # Optimal at ~2.9 Å
                E_hbond = -3.0 * np.exp(-((r - 2.9) ** 2) / 0.5)
                total_hbond += E_hbond
                n_hbonds += 1

    return {
        'total_kcal': total_hbond,
        'n_hbonds': n_hbonds,
        'avg_per_hbond': total_hbond / n_hbonds if n_hbonds > 0 else 0,
        'description': 'Hydrogen bonds'
    }


# =============================================================================
# OPENMM ENERGY DECOMPOSITION (if available)
# =============================================================================

def openmm_energy_decomposition(pdb_path: Path) -> dict:
    """
    Use OpenMM for rigorous force field energy decomposition.
    """
    if not OPENMM_AVAILABLE:
        return None

    print("  Running OpenMM energy decomposition...")

    # Load structure
    pdb = PDBFile(str(pdb_path))

    # Create force field
    forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')

    # Create system
    modeller = Modeller(pdb.topology, pdb.positions)
    modeller.addHydrogens(forcefield)

    system = forcefield.createSystem(
        modeller.topology,
        nonbondedMethod=NoCutoff,
        constraints=None
    )

    # Create separate systems for each force component
    energies = {}

    # Get all forces
    for i, force in enumerate(system.getForces()):
        force_name = force.__class__.__name__

        # Create a copy of the system with only this force
        test_system = System()
        for j in range(system.getNumParticles()):
            test_system.addParticle(system.getParticleMass(j))

        # Clone the force
        if isinstance(force, NonbondedForce):
            # Decompose NonbondedForce
            nb = NonbondedForce()
            nb.setNonbondedMethod(NonbondedForce.NoCutoff)

            for j in range(force.getNumParticles()):
                charge, sigma, epsilon = force.getParticleParameters(j)
                nb.addParticle(charge, sigma, epsilon)

            for j in range(force.getNumExceptions()):
                p1, p2, chargeProd, sigma, epsilon = force.getExceptionParameters(j)
                nb.addException(p1, p2, chargeProd, sigma, epsilon)

            test_system.addForce(nb)
            force_name = 'NonbondedForce'
        else:
            continue  # Skip other forces for now

        # Calculate energy
        integrator = VerletIntegrator(0.001 * picoseconds)
        context = Context(test_system, integrator)
        context.setPositions(modeller.positions)

        state = context.getState(getEnergy=True)
        energy = state.getPotentialEnergy().value_in_unit(kilocalories_per_mole)
        energies[force_name] = energy

        del context

    return energies


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def analyze_protein(pdb_id: str) -> dict:
    """
    Complete energy deconstruction for a protein.
    """
    print(f"\nAnalyzing: {pdb_id}")
    print("-" * 60)

    # Download/load PDB
    pdb_path = download_pdb(pdb_id)
    data = parse_pdb_for_analysis(pdb_path)

    print(f"  Loaded {data['n_atoms']} heavy atoms")

    result = {
        'pdb_id': pdb_id,
        'n_atoms': data['n_atoms'],
        'timestamp': datetime.now().isoformat(),
    }

    # Calculate each energy component
    atoms = data['atoms']
    coords = data['coords']

    # 1. Coulomb (electromagnetic)
    coulomb = calculate_coulomb_energy(atoms, coords)
    result['coulomb'] = coulomb
    print(f"\n  COULOMB ELECTROSTATICS (U(1) gauge):")
    print(f"    Total: {coulomb['total_kcal']:.2f} kcal/mol")
    print(f"    Favorable (opposite charges): {coulomb['favorable_kcal']:.2f} kcal/mol")
    print(f"    Unfavorable (like charges): {coulomb['unfavorable_kcal']:.2f} kcal/mol")

    # 2. Lennard-Jones
    lj = calculate_lennard_jones(atoms, coords)
    result['lennard_jones'] = lj
    print(f"\n  LENNARD-JONES (Van der Waals):")
    print(f"    Total: {lj['total_kcal']:.2f} kcal/mol")
    print(f"    Attractive (London dispersion): {lj['attractive_kcal']:.2f} kcal/mol")
    print(f"    Repulsive (Pauli exclusion): {lj['repulsive_kcal']:.2f} kcal/mol")

    # 3. Solvation
    solv = calculate_solvation_energy(atoms, coords)
    result['solvation'] = solv
    print(f"\n  SOLVATION FREE ENERGY:")
    print(f"    Total: {solv['total_kcal']:.2f} kcal/mol")
    print(f"    Hydrophobic penalty: {solv['hydrophobic_penalty_kcal']:.2f} kcal/mol")
    print(f"    Polar gain: {solv['polar_gain_kcal']:.2f} kcal/mol")

    # 4. Hydrogen bonds
    hbond = calculate_hydrogen_bonds(atoms, coords)
    result['hydrogen_bonds'] = hbond
    print(f"\n  HYDROGEN BONDS:")
    print(f"    Total: {hbond['total_kcal']:.2f} kcal/mol")
    print(f"    Number: {hbond['n_hbonds']}")
    print(f"    Average per bond: {hbond['avg_per_hbond']:.2f} kcal/mol")

    # Summary
    total = (coulomb['total_kcal'] + lj['total_kcal'] +
             solv['total_kcal'] + hbond['total_kcal'])

    result['total_energy_kcal'] = total

    print(f"\n  {'=' * 50}")
    print(f"  TOTAL POTENTIAL ENERGY: {total:.2f} kcal/mol")
    print(f"  {'=' * 50}")

    # Breakdown percentages
    components = {
        'Coulomb': abs(coulomb['total_kcal']),
        'LJ Attractive': abs(lj['attractive_kcal']),
        'LJ Repulsive': abs(lj['repulsive_kcal']),
        'Solvation': abs(solv['total_kcal']),
        'H-bonds': abs(hbond['total_kcal']),
    }
    total_magnitude = sum(components.values())

    print(f"\n  FORCE CONTRIBUTION (% of total magnitude):")
    for name, val in sorted(components.items(), key=lambda x: -x[1]):
        pct = 100 * val / total_magnitude if total_magnitude > 0 else 0
        bar = '#' * int(pct / 2)
        print(f"    {name:15s}: {pct:5.1f}% {bar}")

    result['force_percentages'] = {k: 100 * v / total_magnitude
                                   for k, v in components.items()}

    return result


def main():
    """
    Run energy deconstruction on reference proteins.
    """
    # Test proteins
    proteins = [
        ('1PGB', 'Protein G B1 domain (56 residues, stable fold)'),
        ('1UBQ', 'Ubiquitin (76 residues, highly stable)'),
        ('1VII', 'Villin headpiece (36 residues, fast folder)'),
    ]

    all_results = []

    for pdb_id, description in proteins:
        print(f"\n{'=' * 80}")
        print(f"{pdb_id}: {description}")
        print("=" * 80)

        result = analyze_protein(pdb_id)
        result['description'] = description
        all_results.append(result)

    # Save results
    json_path = OUTPUT_DIR / "energy_deconstruction_results.json"
    with open(json_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    # Save CSV summary
    csv_path = OUTPUT_DIR / "energy_breakdown.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['PDB', 'Coulomb_kcal', 'LJ_Attractive_kcal',
                        'LJ_Repulsive_kcal', 'Solvation_kcal', 'HBonds_kcal',
                        'Total_kcal'])

        for r in all_results:
            writer.writerow([
                r['pdb_id'],
                f"{r['coulomb']['total_kcal']:.2f}",
                f"{r['lennard_jones']['attractive_kcal']:.2f}",
                f"{r['lennard_jones']['repulsive_kcal']:.2f}",
                f"{r['solvation']['total_kcal']:.2f}",
                f"{r['hydrogen_bonds']['total_kcal']:.2f}",
                f"{r['total_energy_kcal']:.2f}",
            ])

    print(f"\n\nResults saved:")
    print(f"  JSON: {json_path}")
    print(f"  CSV:  {csv_path}")

    # Final summary
    print("\n" + "=" * 80)
    print("ENERGY DECONSTRUCTION SUMMARY")
    print("=" * 80)
    print("\nWhich physical force dominates biological geometry?")

    avg_contributions = {}
    for key in ['Coulomb', 'LJ Attractive', 'LJ Repulsive', 'Solvation', 'H-bonds']:
        vals = [r['force_percentages'].get(key, 0) for r in all_results]
        avg_contributions[key] = np.mean(vals)

    print("\nAverage force contributions across test proteins:")
    for name, pct in sorted(avg_contributions.items(), key=lambda x: -x[1]):
        bar = '#' * int(pct / 2)
        print(f"  {name:15s}: {pct:5.1f}% {bar}")

    dominant = max(avg_contributions, key=avg_contributions.get)
    print(f"\nDOMINANT FORCE: {dominant}")
    print("=" * 80)

    return all_results


if __name__ == "__main__":
    main()
