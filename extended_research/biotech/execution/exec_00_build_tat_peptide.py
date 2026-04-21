#!/usr/bin/env python3
"""
exec_00_build_tat_peptide.py - Build TAT-tagged ZIM-D2R-001 for Membrane Simulation

This script prepares the input structure for the membrane permeation simulation:
1. Takes the ZIM-D2R-001 D2R agonist peptide sequence
2. Appends the TAT Cell-Penetrating Peptide (CPP) sequence
3. Generates a 3D structure using OpenMM
4. Outputs a PDB file ready for CHARMM-GUI membrane building

TAT Sequence: YGRKKRRQRRR (11 residues)
- Derived from HIV-1 TAT protein (residues 47-57)
- Highly cationic (+8 charge at physiological pH)
- Well-characterized BBB penetration

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later

DISCLAIMER: Computational research only. Not peer reviewed. Not medical advice.
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

try:
    import openmm as mm
    from openmm import app, unit
    from openmm.app import PDBFile, ForceField, Modeller
    from pdbfixer import PDBFixer
    print(f"OpenMM version: {mm.__version__}")
except ImportError:
    print("ERROR: OpenMM/PDBFixer not installed")
    print("Run: mamba install -c conda-forge openmm pdbfixer")
    exit(1)

# =============================================================================
# SEQUENCES
# =============================================================================

# ZIM-D2R-001: Cyclic D2R agonist peptide (from our design)
# This is a representative sequence - adjust based on actual design
ZIM_D2R_001_SEQUENCE = "CYIQVDPYITC"  # Cyclic via C1-C11 disulfide

# TAT Cell-Penetrating Peptide (HIV-1 TAT 47-57)
TAT_CPP_SEQUENCE = "YGRKKRRQRRR"

# Flexible linker (Gly-Ser)
LINKER_SEQUENCE = "GGSG"

# Full construct: TAT-linker-ZIM-D2R-001
def build_full_sequence():
    """Build the complete TAT-tagged peptide sequence."""
    # N-terminus: TAT (for membrane penetration)
    # Linker: Flexible GGSG
    # C-terminus: ZIM-D2R-001 (the therapeutic)

    full_seq = TAT_CPP_SEQUENCE + LINKER_SEQUENCE + ZIM_D2R_001_SEQUENCE

    print("Peptide Design:")
    print(f"  TAT CPP:        {TAT_CPP_SEQUENCE} (11 aa)")
    print(f"  Linker:         {LINKER_SEQUENCE} (4 aa)")
    print(f"  ZIM-D2R-001:    {ZIM_D2R_001_SEQUENCE} (11 aa)")
    print(f"  Full construct: {full_seq} ({len(full_seq)} aa)")
    print()

    return full_seq


# =============================================================================
# STRUCTURE GENERATION
# =============================================================================

def sequence_to_pdb_string(sequence: str, chain_id: str = 'A') -> str:
    """
    Convert a peptide sequence to a minimal PDB string.

    This creates an extended chain that OpenMM can then fold.
    """
    # Amino acid 3-letter codes
    aa_codes = {
        'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
        'Q': 'GLN', 'E': 'GLU', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
        'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
        'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL'
    }

    pdb_lines = []
    atom_num = 1
    res_num = 1

    # Generate extended chain (3.8 Å per residue along X)
    for i, aa in enumerate(sequence):
        resname = aa_codes.get(aa, 'ALA')
        x = i * 3.8  # Extended chain
        y = 0.0
        z = 0.0

        # Add backbone atoms (simplified - just CA for now)
        # PDBFixer will add the rest
        line = f"ATOM  {atom_num:5d}  CA  {resname} {chain_id}{res_num:4d}    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C"
        pdb_lines.append(line)

        atom_num += 1
        res_num += 1

    pdb_lines.append("END")

    return '\n'.join(pdb_lines)


def build_peptide_structure(sequence: str, output_path: Path):
    """
    Build a 3D peptide structure from sequence.

    Uses PDBFixer to add missing atoms and OpenMM to minimize.
    """
    print("Building 3D structure...")

    # Create temporary PDB with CA trace
    temp_pdb_content = sequence_to_pdb_string(sequence)
    temp_pdb_path = output_path.parent / "temp_ca_trace.pdb"

    with open(temp_pdb_path, 'w') as f:
        f.write(temp_pdb_content)

    print(f"  Created CA trace: {temp_pdb_path}")

    # Use PDBFixer to add missing atoms
    print("  Running PDBFixer to add missing atoms...")

    fixer = PDBFixer(str(temp_pdb_path))
    fixer.findMissingResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(7.4)  # pH 7.4

    print(f"  Added missing atoms and hydrogens")

    # Set up force field
    print("  Setting up AMBER force field...")
    forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')

    # Create modeller and add solvent (small box for minimization)
    modeller = Modeller(fixer.topology, fixer.positions)

    # Don't add water yet - we'll do that in CHARMM-GUI with the membrane
    # Just minimize in vacuum

    # Create system
    print("  Creating OpenMM system...")
    system = forcefield.createSystem(
        modeller.topology,
        nonbondedMethod=app.NoCutoff,  # Vacuum
        constraints=app.HBonds
    )

    # Integrator
    integrator = mm.LangevinMiddleIntegrator(
        300 * unit.kelvin,
        1.0 / unit.picosecond,
        2.0 * unit.femtoseconds
    )

    # Simulation
    simulation = app.Simulation(modeller.topology, system, integrator)
    simulation.context.setPositions(modeller.positions)

    # Minimize
    print("  Minimizing structure...")
    simulation.minimizeEnergy(maxIterations=2000)

    # Short equilibration
    print("  Running short equilibration (10 ps)...")
    simulation.step(5000)

    # Get final positions
    state = simulation.context.getState(getPositions=True, getEnergy=True)
    positions = state.getPositions()

    print(f"  Final potential energy: {state.getPotentialEnergy()}")

    # Save PDB
    print(f"  Saving structure: {output_path}")
    with open(output_path, 'w') as f:
        PDBFile.writeFile(modeller.topology, positions, f)

    # Clean up temp file
    temp_pdb_path.unlink()

    print("  Structure building complete!")

    return output_path


def add_disulfide_annotation(pdb_path: Path):
    """
    Add SSBOND record for the cyclic disulfide in ZIM-D2R-001.

    The C1 and C11 cysteines in ZIM-D2R-001 form a disulfide bridge.
    """
    print("\nAdding disulfide bond annotation...")

    # Read PDB
    with open(pdb_path, 'r') as f:
        lines = f.readlines()

    # Find cysteine residues
    # In our construct: TAT(11) + linker(4) + ZIM(11) = 26 total
    # ZIM starts at residue 16
    # C1 of ZIM = residue 16
    # C11 of ZIM = residue 26

    cys_residues = []
    for line in lines:
        if line.startswith('ATOM') and ' CYS ' in line:
            res_num = int(line[22:26].strip())
            if res_num not in cys_residues:
                cys_residues.append(res_num)

    print(f"  Found CYS residues at positions: {cys_residues}")

    if len(cys_residues) >= 2:
        # Add SSBOND record
        ssbond_line = f"SSBOND   1 CYS A {cys_residues[0]:4d}    CYS A {cys_residues[1]:4d}\n"

        # Insert before first ATOM line
        for i, line in enumerate(lines):
            if line.startswith('ATOM'):
                lines.insert(i, ssbond_line)
                break

        # Write updated PDB
        with open(pdb_path, 'w') as f:
            f.writelines(lines)

        print(f"  Added SSBOND: CYS {cys_residues[0]} - CYS {cys_residues[1]}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Build the TAT-tagged ZIM-D2R-001 peptide."""

    print("=" * 70)
    print("TAT-TAGGED ZIM-D2R-001 PEPTIDE BUILDER")
    print("Preparing input for membrane permeation simulation")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Build full sequence
    full_sequence = build_full_sequence()

    # Output path
    output_dir = Path(__file__).parent
    output_pdb = output_dir / "TAT_ZIM_D2R_001.pdb"

    # Build structure
    build_peptide_structure(full_sequence, output_pdb)

    # Add disulfide annotation
    add_disulfide_annotation(output_pdb)

    # Summary
    print()
    print("=" * 70)
    print("STRUCTURE READY")
    print("=" * 70)
    print()
    print(f"Output PDB: {output_pdb}")
    print()
    print("NEXT STEPS:")
    print("-" * 70)
    print("""
1. Go to CHARMM-GUI Membrane Builder (https://charmm-gui.org)

2. Upload TAT_ZIM_D2R_001.pdb

3. Configure membrane:
   - Lipid type: POPC (brain-like)
   - Lipids per leaflet: 64 (128 total)
   - Water thickness: 22.5 Å above/below

4. Configure ions:
   - Ion type: NaCl
   - Concentration: 0.15 M

5. Position peptide:
   - Place ~30 Å ABOVE the membrane center
   - The TAT tag should face the membrane

6. Download the equilibrated system as 'system_equilibrated.pdb'

7. Run: python exec_01_membrane_permeation.py
""")
    print("=" * 70)

    return output_pdb


if __name__ == "__main__":
    main()
