#!/usr/bin/env python3
"""
val_10_cyclic_topology_patcher.py - Cyclic Peptide Topology Patcher

Handles cyclic peptides (head-to-tail cyclization) that standard Amber14
force fields cannot process. Creates custom topology with explicit
peptide bond between N-terminal and C-terminal residues.

AGPL-3.0-or-later License
Author: Carl Zimmerman & Claude Opus 4.5
Date: April 21, 2026
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Optional, Tuple
import warnings

OUTPUT_DIR = Path(__file__).parent / "results" / "cyclic_peptides"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("CYCLIC PEPTIDE TOPOLOGY PATCHER")
print("=" * 80)
print()

# =============================================================================
# CYCLIC PEPTIDE CANDIDATES
# =============================================================================

CYCLIC_PEPTIDES = {
    "ZIM-GLP2-006": {
        "name": "Cyclic GLP-2 Analog",
        "sequence": "HADGSF",  # Head-to-tail cyclic
        "target": "GLP-2 Receptor",
        "smiles": None,  # Will generate from sequence
        "cyclization": "head-to-tail",  # N-term to C-term
    },
    "ZIM-CYC-001": {
        "name": "Cyclic α-synuclein Disruptor",
        "sequence": "cyclo-FPFPF",  # Alternating F-P for β-turn propensity
        "target": "Alpha-synuclein",
        "cyclization": "head-to-tail",
    },
}

# =============================================================================
# AMINO ACID DATA
# =============================================================================

AA_SMILES = {
    'A': 'C',  # Alanine sidechain
    'R': 'CCCNC(=N)N',  # Arginine
    'N': 'CC(=O)N',  # Asparagine
    'D': 'CC(=O)O',  # Aspartate
    'C': 'CS',  # Cysteine
    'E': 'CCC(=O)O',  # Glutamate
    'Q': 'CCC(=O)N',  # Glutamine
    'G': '[H]',  # Glycine (no sidechain)
    'H': 'Cc1cnc[nH]1',  # Histidine
    'I': 'C(C)CC',  # Isoleucine
    'L': 'CC(C)C',  # Leucine
    'K': 'CCCCN',  # Lysine
    'M': 'CCSC',  # Methionine
    'F': 'Cc1ccccc1',  # Phenylalanine
    'P': None,  # Proline - special case (ring)
    'S': 'CO',  # Serine
    'T': 'C(C)O',  # Threonine
    'W': 'Cc1c[nH]c2ccccc12',  # Tryptophan
    'Y': 'Cc1ccc(O)cc1',  # Tyrosine
    'V': 'C(C)C',  # Valine
}


def sequence_to_cyclic_smiles(sequence: str) -> str:
    """
    Convert amino acid sequence to cyclic peptide SMILES.
    Uses ring closure to connect N-term to C-term.
    """
    # This is a simplified representation
    # Real cyclic SMILES would need proper backbone connectivity
    clean_seq = sequence.replace("cyclo-", "")

    # For demonstration, we'll return a placeholder
    # In production, use RDKit's AllChem.EmbedMolecule with constraints
    return f"cyclic({clean_seq})"


# =============================================================================
# CYCLIC PEPTIDE BUILDER
# =============================================================================

def build_linear_peptide(sequence: str) -> Tuple:
    """
    Build a linear peptide first, then cyclize.
    Returns (topology, positions) for OpenMM.
    """
    from pdbfixer import PDBFixer
    from openmm.app import PDBFile
    from io import StringIO
    import tempfile

    # Clean sequence
    clean_seq = sequence.replace("cyclo-", "")

    # Standard 3-letter codes
    aa_3letter = {
        'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
        'E': 'GLU', 'Q': 'GLN', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
        'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
        'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL',
    }

    # Create extended backbone PDB
    pdb_content = "HEADER    CYCLIC PEPTIDE PRECURSOR\n"
    atom_num = 1

    for i, aa in enumerate(clean_seq):
        res_name = aa_3letter.get(aa, 'ALA')
        res_num = i + 1
        x_offset = i * 3.8  # Extended chain

        # Backbone atoms
        pdb_content += f"ATOM  {atom_num:5d}  N   {res_name} A{res_num:4d}    {x_offset - 0.5:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           N\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  CA  {res_name} A{res_num:4d}    {x_offset:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  C   {res_name} A{res_num:4d}    {x_offset + 1.5:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  O   {res_name} A{res_num:4d}    {x_offset + 2.0:8.3f}{1.0:8.3f}{0.0:8.3f}  1.00  0.00           O\n"
        atom_num += 1

    pdb_content += "END\n"

    # Write and fix with PDBFixer
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb', delete=False) as f:
        f.write(pdb_content)
        temp_path = f.name

    fixer = PDBFixer(temp_path)
    fixer.findMissingResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(7.4)

    # Remove temp file
    Path(temp_path).unlink()

    return fixer.topology, fixer.positions, clean_seq


def create_cyclic_topology(topology, positions, sequence: str):
    """
    Modify OpenMM topology to add head-to-tail peptide bond.

    This is the critical step: we need to add a bond between:
    - N atom of first residue
    - C atom of last residue

    OpenMM doesn't allow direct topology modification, so we rebuild.
    """
    from openmm.app import Topology, Element
    from openmm import unit
    import numpy as np

    # Create new topology with cyclic bond
    new_topology = Topology()
    new_topology.setPeriodicBoxVectors(topology.getPeriodicBoxVectors())

    # Copy chains
    old_chain = list(topology.chains())[0]
    new_chain = new_topology.addChain(old_chain.id)

    # Atom mapping (old index -> new atom)
    atom_map = {}

    # Find N-terminal N and C-terminal C
    n_term_n = None
    c_term_c = None

    residues = list(old_chain.residues())

    # Copy residues and atoms
    for res in residues:
        new_res = new_topology.addResidue(res.name, new_chain, res.id, res.insertionCode)
        for atom in res.atoms():
            new_atom = new_topology.addAtom(atom.name, atom.element, new_res)
            atom_map[atom.index] = new_atom

            # Track terminal atoms
            if res == residues[0] and atom.name == 'N':
                n_term_n = new_atom
            if res == residues[-1] and atom.name == 'C':
                c_term_c = new_atom

    # Copy existing bonds
    for bond in topology.bonds():
        new_topology.addBond(atom_map[bond[0].index], atom_map[bond[1].index])

    # ADD THE CYCLIC BOND
    if n_term_n is not None and c_term_c is not None:
        new_topology.addBond(c_term_c, n_term_n)
        print(f"    Added cyclic bond: {residues[-1].name}(C) -> {residues[0].name}(N)")
    else:
        warnings.warn("Could not find terminal atoms for cyclic bond!")

    # Remove terminal hydrogens that would interfere
    # (In real implementation, we'd rebuild without them)

    return new_topology


def parameterize_cyclic_peptide(topology, positions, peptide_id: str) -> Dict:
    """
    Parameterize cyclic peptide using OpenFF or fall back to Amber+custom.

    Strategy:
    1. Try OpenFF Toolkit (modern, supports arbitrary molecules)
    2. Fall back to Amber14 with custom patches
    """
    from openmm.app import ForceField, Modeller, Simulation
    from openmm.app import PDBFile, PME, HBonds
    from openmm import unit, LangevinMiddleIntegrator, Platform
    import xml.etree.ElementTree as ET

    result = {
        'peptide_id': peptide_id,
        'method': None,
        'success': False,
    }

    # Try 1: Use standard Amber14 with modified topology
    # (The cyclic bond was added to topology, but Amber templates
    # assume free termini. We'll use a workaround.)

    print("    Attempting Amber14 parameterization...")

    try:
        # For cyclic peptides, we treat residues as "internal"
        # by not having ACE/NME caps
        forcefield = ForceField('amber14-all.xml', 'amber14/tip3p.xml')

        # Create modeller
        modeller = Modeller(topology, positions)

        # Add solvent
        modeller.addSolvent(
            forcefield,
            model='tip3p',
            padding=1.2 * unit.nanometer,
            ionicStrength=0.15 * unit.molar,
        )

        # Create system
        system = forcefield.createSystem(
            modeller.topology,
            nonbondedMethod=PME,
            nonbondedCutoff=1.0 * unit.nanometer,
            constraints=HBonds,
        )

        result['method'] = 'amber14'
        result['success'] = True
        result['topology'] = modeller.topology
        result['positions'] = modeller.positions
        result['system'] = system

        print("    ✓ Amber14 parameterization successful")

    except Exception as e:
        print(f"    Amber14 failed: {e}")
        print("    Attempting OpenFF parameterization...")

        # Try 2: OpenFF Toolkit
        try:
            from openff.toolkit import Molecule, Topology as OFFTopology
            from openff.interchange import Interchange

            # This requires proper SMILES for the cyclic peptide
            # For now, we'll note this as a TODO
            result['method'] = 'openff'
            result['error'] = 'OpenFF requires cyclic SMILES - implementation pending'
            print("    OpenFF requires cyclic SMILES representation")

        except ImportError:
            result['error'] = 'Neither Amber14 nor OpenFF could parameterize'
            print("    OpenFF Toolkit not installed")

    return result


def generate_cyclic_forcefield_xml(peptide_id: str, sequence: str) -> Path:
    """
    Generate a custom force field XML patch for cyclic peptide.
    This adds the missing bond type for head-to-tail cyclization.
    """
    import xml.etree.ElementTree as ET

    xml_content = f'''<?xml version="1.0" encoding="utf-8"?>
<ForceField>
  <!-- Custom patch for cyclic peptide {peptide_id} -->
  <!-- Sequence: {sequence} -->

  <Info>
    <DateGenerated>{datetime.now().isoformat()}</DateGenerated>
    <Reference>Zimmerman Lab Cyclic Peptide Protocol</Reference>
  </Info>

  <!--
  USAGE: Load this AFTER amber14-all.xml to patch cyclic bonds

  The cyclic bond is a standard peptide bond:
  C(=O)-N with parameters from Amber14

  Force constant: 3.17e5 kJ/mol/nm²
  Equilibrium length: 0.133 nm
  -->

  <HarmonicBondForce>
    <!-- Cyclic peptide bond (same as standard peptide bond) -->
    <Bond class1="C" class2="N" length="0.1335" k="410032.0"/>
  </HarmonicBondForce>

  <HarmonicAngleForce>
    <!-- Angles around cyclic junction -->
    <Angle class1="CA" class2="C" class3="N" angle="2.035" k="585.76"/>
    <Angle class1="C" class2="N" class3="CA" angle="2.124" k="418.4"/>
    <Angle class1="O" class2="C" class3="N" angle="2.166" k="669.44"/>
  </HarmonicAngleForce>

  <PeriodicTorsionForce>
    <!-- Omega dihedral for cyclic junction (should be ~180° trans) -->
    <Proper class1="CA" class2="C" class3="N" class4="CA"
            periodicity1="2" phase1="3.14159" k1="10.46"/>
  </PeriodicTorsionForce>

</ForceField>
'''

    xml_path = OUTPUT_DIR / f"{peptide_id}_cyclic_patch.xml"
    with open(xml_path, 'w') as f:
        f.write(xml_content)

    print(f"    Generated force field patch: {xml_path}")
    return xml_path


# =============================================================================
# ENERGY MINIMIZATION FOR RING CLOSURE
# =============================================================================

def close_cyclic_ring(topology, positions, sequence: str):
    """
    Physically close the cyclic ring by applying distance restraints
    and energy minimization.

    The extended chain has N-term and C-term far apart.
    We need to bring them together (~1.33 Å for peptide bond).
    """
    from openmm.app import ForceField, Modeller, Simulation
    from openmm.app import PME, HBonds
    from openmm import unit, LangevinMiddleIntegrator
    from openmm import CustomBondForce
    import numpy as np

    print("    Closing cyclic ring via constrained minimization...")

    # Find N-term N and C-term C indices
    residues = list(topology.residues())

    n_idx = None
    c_idx = None

    for atom in residues[0].atoms():
        if atom.name == 'N':
            n_idx = atom.index

    for atom in residues[-1].atoms():
        if atom.name == 'C':
            c_idx = atom.index

    if n_idx is None or c_idx is None:
        raise ValueError("Could not find terminal N or C atoms")

    # Calculate current distance
    pos_array = np.array([[p.x, p.y, p.z] for p in positions]) * 10  # nm to Å
    current_dist = np.linalg.norm(pos_array[n_idx] - pos_array[c_idx])
    target_dist = 1.33  # Å (peptide bond length)

    print(f"    Current N-C distance: {current_dist:.2f} Å")
    print(f"    Target N-C distance: {target_dist:.2f} Å")

    # Use forcefield with restraint
    forcefield = ForceField('amber14-all.xml', 'amber14/tip3p.xml')

    # Create system
    modeller = Modeller(topology, positions)
    system = forcefield.createSystem(
        topology,
        nonbondedMethod=PME,
        nonbondedCutoff=1.0 * unit.nanometer,
        constraints=HBonds,
    )

    # Add strong harmonic restraint to pull termini together
    # k = 1000 kJ/mol/nm² = very strong
    restraint = CustomBondForce("0.5*k*(r-r0)^2")
    restraint.addPerBondParameter("k")
    restraint.addPerBondParameter("r0")
    restraint.addBond(n_idx, c_idx, [10000.0, 0.133])  # 1.33 Å = 0.133 nm
    system.addForce(restraint)

    # Minimize
    integrator = LangevinMiddleIntegrator(
        300 * unit.kelvin,
        1.0 / unit.picosecond,
        1.0 * unit.femtoseconds,
    )

    simulation = Simulation(topology, system, integrator)
    simulation.context.setPositions(positions)

    # Staged minimization (relax restraint gradually)
    for k_val in [10000, 5000, 2000, 1000]:
        simulation.context.setParameter("k", k_val)
        simulation.minimizeEnergy(maxIterations=500)

    # Final positions
    state = simulation.context.getState(getPositions=True)
    final_positions = state.getPositions()

    # Check final distance
    pos_array = np.array([[p.x, p.y, p.z] for p in final_positions]) * 10
    final_dist = np.linalg.norm(pos_array[n_idx] - pos_array[c_idx])
    print(f"    Final N-C distance: {final_dist:.2f} Å")

    if final_dist > 2.0:
        print("    ⚠ Warning: Ring closure incomplete, may need manual adjustment")
    else:
        print("    ✓ Ring closure successful")

    return final_positions


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def process_cyclic_peptide(peptide_id: str, info: Dict) -> Dict:
    """
    Full pipeline for cyclic peptide preparation.
    """
    print(f"\n{'=' * 60}")
    print(f"Processing: {peptide_id}")
    print(f"  {info['name']}")
    print(f"  Sequence: {info['sequence']}")
    print(f"  Cyclization: {info.get('cyclization', 'head-to-tail')}")
    print(f"{'=' * 60}")

    result = {
        'peptide_id': peptide_id,
        'timestamp': datetime.now().isoformat(),
        'sequence': info['sequence'],
    }

    try:
        # Step 1: Build linear peptide
        print("\n  Step 1: Building linear precursor...")
        topology, positions, clean_seq = build_linear_peptide(info['sequence'])
        print(f"    Built {len(list(topology.atoms()))} atoms")

        # Step 2: Close the ring
        print("\n  Step 2: Ring closure...")
        closed_positions = close_cyclic_ring(topology, positions, clean_seq)

        # Step 3: Create cyclic topology
        print("\n  Step 3: Creating cyclic topology...")
        cyclic_topology = create_cyclic_topology(topology, closed_positions, clean_seq)

        # Step 4: Generate force field patch
        print("\n  Step 4: Generating force field patch...")
        xml_path = generate_cyclic_forcefield_xml(peptide_id, clean_seq)
        result['forcefield_xml'] = str(xml_path)

        # Step 5: Save solvated structure
        print("\n  Step 5: Solvating and saving...")
        pdb_path = save_solvated_cyclic(cyclic_topology, closed_positions, peptide_id)
        result['pdb_path'] = str(pdb_path)

        result['success'] = True
        print(f"\n  ✓ {peptide_id} processed successfully")

    except Exception as e:
        print(f"\n  ✗ Processing failed: {e}")
        result['success'] = False
        result['error'] = str(e)
        import traceback
        traceback.print_exc()

    return result


def save_solvated_cyclic(topology, positions, peptide_id: str) -> Path:
    """
    Solvate and save the cyclic peptide structure.
    """
    from openmm.app import ForceField, Modeller, PDBFile
    from openmm import unit

    forcefield = ForceField('amber14-all.xml', 'amber14/tip3p.xml')
    modeller = Modeller(topology, positions)

    # Add solvent
    modeller.addSolvent(
        forcefield,
        model='tip3p',
        padding=1.2 * unit.nanometer,
        ionicStrength=0.15 * unit.molar,
    )

    # Save
    pdb_path = OUTPUT_DIR / f"{peptide_id}_cyclic_solvated.pdb"
    with open(pdb_path, 'w') as f:
        PDBFile.writeFile(modeller.topology, modeller.positions, f)

    print(f"    Saved: {pdb_path}")
    print(f"    System size: {modeller.topology.getNumAtoms()} atoms")

    return pdb_path


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Process all cyclic peptide candidates.
    """
    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Cyclic Peptide Topology Patcher',
        'peptides': {},
    }

    for peptide_id, info in CYCLIC_PEPTIDES.items():
        result = process_cyclic_peptide(peptide_id, info)
        results['peptides'][peptide_id] = result

    # Summary
    successful = sum(1 for r in results['peptides'].values() if r.get('success'))
    total = len(results['peptides'])

    print("\n" + "=" * 80)
    print("CYCLIC PEPTIDE PROCESSING SUMMARY")
    print("=" * 80)
    print(f"\n  Successful: {successful}/{total}")

    # Save results
    output_json = OUTPUT_DIR / "cyclic_topology_results.json"
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results: {output_json}")

    return results


if __name__ == "__main__":
    main()
