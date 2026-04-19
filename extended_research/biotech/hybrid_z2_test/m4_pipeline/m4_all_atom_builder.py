#!/usr/bin/env python3
"""
M4 All-Atom System Builder: Publication-Quality Preparation

SPDX-License-Identifier: AGPL-3.0-or-later

Prepares a scientifically rigorous all-atom system for molecular dynamics:
1. Add all missing heavy atoms
2. Add hydrogens appropriate for pH 7.4
3. Solvate with explicit TIP3P water (1.0 nm padding)
4. Neutralize with 0.15M NaCl (physiological salinity)

This produces a system suitable for peer-reviewed publication.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import os
import sys
from datetime import datetime
from typing import Dict, Optional
import warnings
warnings.filterwarnings('ignore')


def build_all_atom_system(
    input_pdb: str,
    output_dir: str = "all_atom_system",
    padding: float = 1.0,  # nm
    ionic_strength: float = 0.15,  # M (physiological)
    ph: float = 7.4
) -> Dict:
    """
    Build a fully solvated, neutralized all-atom system.

    Args:
        input_pdb: Path to input PDB (can be Cα-only or all-atom)
        output_dir: Output directory
        padding: Water box padding in nm
        ionic_strength: NaCl concentration in M
        ph: pH for protonation states

    Returns:
        Dictionary with system information
    """
    print("=" * 70)
    print("M4 ALL-ATOM SYSTEM BUILDER")
    print("=" * 70)
    print(f"Input: {input_pdb}")
    print(f"pH: {ph}")
    print(f"Padding: {padding} nm")
    print(f"Ionic strength: {ionic_strength} M NaCl")

    os.makedirs(output_dir, exist_ok=True)

    result = {
        "timestamp": datetime.now().isoformat(),
        "input_pdb": input_pdb,
        "ph": ph,
        "padding_nm": padding,
        "ionic_strength_M": ionic_strength,
        "status": "started"
    }

    try:
        from pdbfixer import PDBFixer
        from openmm.app import PDBFile, Modeller, ForceField
        from openmm import unit
        import openmm as mm

        # =====================================================================
        # STEP 1: Load and fix the structure
        # =====================================================================
        print(f"\n{'='*60}")
        print("STEP 1: STRUCTURE PREPARATION")
        print("=" * 60)

        fixer = PDBFixer(filename=input_pdb)

        # Count original atoms
        original_atoms = len(list(fixer.topology.atoms()))
        print(f"Original atoms: {original_atoms}")

        # Find and add missing residues (for incomplete structures)
        print("\nFinding missing residues...")
        fixer.findMissingResidues()
        if fixer.missingResidues:
            print(f"  Found {len(fixer.missingResidues)} missing residue segments")
            # Don't add terminal missing residues (common in crystal structures)
            keys_to_remove = []
            for key in fixer.missingResidues:
                chain_id, res_id = key
                if res_id == 0 or res_id == len(list(fixer.topology.residues())):
                    keys_to_remove.append(key)
            for key in keys_to_remove:
                del fixer.missingResidues[key]

        # Find and add missing atoms (heavy atoms)
        print("\nFinding missing heavy atoms...")
        fixer.findMissingAtoms()
        if fixer.missingAtoms or fixer.missingTerminals:
            n_missing = len(fixer.missingAtoms) + len(fixer.missingTerminals)
            print(f"  Found {n_missing} missing atoms/terminals")
            fixer.addMissingAtoms()
            print("  ✓ Added missing heavy atoms")

        # Add hydrogens at specified pH
        print(f"\nAdding hydrogens (pH {ph})...")
        fixer.addMissingHydrogens(ph)

        atoms_after_h = len(list(fixer.topology.atoms()))
        print(f"  ✓ Atoms after hydrogens: {atoms_after_h}")

        result["atoms_after_fixing"] = atoms_after_h
        result["hydrogens_added"] = atoms_after_h - original_atoms

        # Save fixed structure
        fixed_pdb = os.path.join(output_dir, "structure_fixed.pdb")
        with open(fixed_pdb, 'w') as f:
            PDBFile.writeFile(fixer.topology, fixer.positions, f)
        print(f"  ✓ Saved: {fixed_pdb}")

        # =====================================================================
        # STEP 2: Solvation with explicit water
        # =====================================================================
        print(f"\n{'='*60}")
        print("STEP 2: EXPLICIT SOLVATION")
        print("=" * 60)

        # Load force field for solvation
        forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')

        # Create modeller
        modeller = Modeller(fixer.topology, fixer.positions)

        print(f"\nAdding TIP3P-FB water box (padding: {padding} nm)...")

        # Add solvent
        modeller.addSolvent(
            forcefield,
            model='tip3p',
            padding=padding * unit.nanometer,
            ionicStrength=ionic_strength * unit.molar,
            positiveIon='Na+',
            negativeIon='Cl-'
        )

        # Count atoms
        total_atoms = len(list(modeller.topology.atoms()))
        n_waters = sum(1 for r in modeller.topology.residues() if r.name == 'HOH')
        n_na = sum(1 for r in modeller.topology.residues() if r.name == 'NA')
        n_cl = sum(1 for r in modeller.topology.residues() if r.name == 'CL')

        print(f"  ✓ Total atoms: {total_atoms:,}")
        print(f"  ✓ Water molecules: {n_waters:,}")
        print(f"  ✓ Na+ ions: {n_na}")
        print(f"  ✓ Cl- ions: {n_cl}")

        result["total_atoms"] = total_atoms
        result["water_molecules"] = n_waters
        result["na_ions"] = n_na
        result["cl_ions"] = n_cl

        # Compute box dimensions
        positions = modeller.getPositions()
        pos_array = [[p.x, p.y, p.z] for p in positions]
        import numpy as np
        pos_array = np.array(pos_array)
        box_min = pos_array.min(axis=0)
        box_max = pos_array.max(axis=0)
        box_size = box_max - box_min

        print(f"\n  Box dimensions: {box_size[0]:.2f} x {box_size[1]:.2f} x {box_size[2]:.2f} nm")
        result["box_size_nm"] = box_size.tolist()

        # =====================================================================
        # STEP 3: Save solvated system
        # =====================================================================
        print(f"\n{'='*60}")
        print("STEP 3: SAVING SOLVATED SYSTEM")
        print("=" * 60)

        solvated_pdb = os.path.join(output_dir, "system_solvated.pdb")
        with open(solvated_pdb, 'w') as f:
            PDBFile.writeFile(modeller.topology, modeller.positions, f)

        print(f"  ✓ Saved: {solvated_pdb}")
        print(f"  File size: {os.path.getsize(solvated_pdb) / 1024:.1f} KB")

        result["output_pdb"] = solvated_pdb
        result["status"] = "success"

        # =====================================================================
        # SUMMARY
        # =====================================================================
        print(f"\n{'='*70}")
        print("SYSTEM PREPARATION COMPLETE")
        print("=" * 70)
        print(f"""
System Statistics:
  - Protein atoms: {atoms_after_h:,}
  - Water molecules: {n_waters:,} ({n_waters * 3:,} atoms)
  - Ions: {n_na} Na+, {n_cl} Cl-
  - Total atoms: {total_atoms:,}
  - Box size: {box_size[0]:.1f} x {box_size[1]:.1f} x {box_size[2]:.1f} nm

Output files:
  - Fixed structure: {fixed_pdb}
  - Solvated system: {solvated_pdb}

This system is ready for equilibration and production MD.
        """)

        # Save results JSON
        import json
        results_path = os.path.join(output_dir, "system_info.json")
        with open(results_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)

        return result

    except ImportError as e:
        print(f"\n✗ Missing dependency: {e}")
        print("Install with: pip install pdbfixer openmm")
        result["status"] = "failed"
        result["error"] = str(e)
        return result

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        result["status"] = "failed"
        result["error"] = str(e)
        return result


def check_ca_only(pdb_path: str) -> bool:
    """Check if PDB is Cα-only (needs rebuilding)."""
    atom_names = set()
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                atom_name = line[12:16].strip()
                atom_names.add(atom_name)
    return atom_names == {'CA'}


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("M4 ALL-ATOM SYSTEM BUILDER")
    print("Publication-Quality Molecular Dynamics Preparation")
    print("=" * 70)

    # Test with de novo Z² structure
    test_pdb = "pipeline_output_denovo/esm_prediction/z2_compact_60_esm.pdb"

    if os.path.exists(test_pdb):
        # Check if Cα-only
        if check_ca_only(test_pdb):
            print(f"\n⚠ Input is Cα-only: {test_pdb}")
            print("PDBFixer will attempt to rebuild all atoms.")
            print("For best results, use ESMFold or AlphaFold for full structure.")

        result = build_all_atom_system(
            test_pdb,
            output_dir="all_atom_system",
            padding=1.0,
            ionic_strength=0.15,
            ph=7.4
        )

        if result["status"] == "success":
            print(f"\n✓ System ready for MD: {result['output_pdb']}")
        else:
            print(f"\n✗ Build failed: {result.get('error', 'unknown')}")
    else:
        print(f"\n⚠ Test PDB not found: {test_pdb}")
        print("Run the pipeline first to generate a structure.")
