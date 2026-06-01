#!/usr/bin/env python3
"""
M4 Pituitary Target Extraction
==============================

Extracts structural data for prolactinoma therapeutic design:
- Dopamine D2 Receptor (D2R) - PRIMARY TARGET
- 5-HT2B Serotonin Receptor - NEGATIVE CONTROL (avoid binding)

PROLACTINOMA BIOLOGY:
====================
- Benign tumor of pituitary lactotroph cells
- Overproduces prolactin hormone
- Standard treatment: Dopamine agonists (Cabergoline, Bromocriptine)
- D2R activation → lactotroph apoptosis → tumor shrinkage

WHY A NEW DRUG?
===============
Current drugs (ergot-derived) can hit 5-HT2B receptor → cardiac valve issues
Goal: Design hyper-selective D2R agonist with ZERO 5-HT2B binding

ADVANTAGE:
==========
Pituitary sits OUTSIDE blood-brain barrier → direct drug access

LICENSE: AGPL-3.0-or-later + OpenMTA + CC-BY-SA-4.0
AUTHOR: Carl Zimmerman
DATE: April 2026
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import urllib.request

# =============================================================================
# CONSTANTS
# =============================================================================

# Target receptor
D2R_PDB = "6CM4"  # Human Dopamine D2 Receptor (active state with Gi)
D2R_NAME = "Dopamine D2 Receptor"
D2R_UNIPROT = "P14416"

# Off-target (negative control)
HT2B_PDB = "6DRX"  # Human 5-HT2B Serotonin Receptor
HT2B_NAME = "5-HT2B Serotonin Receptor"
HT2B_UNIPROT = "P41595"

# Binding pocket residues (from literature)
# D2R orthosteric pocket (dopamine binding site)
D2R_POCKET_RESIDUES = [
    ('D', 114),   # Asp114 - critical for amine binding
    ('V', 115),   # Val115
    ('C', 118),   # Cys118
    ('T', 119),   # Thr119
    ('W', 386),   # Trp386 - aromatic cage
    ('F', 389),   # Phe389 - aromatic cage
    ('F', 390),   # Phe390 - aromatic cage
    ('H', 393),   # His393
    ('Y', 408),   # Tyr408
    ('T', 412),   # Thr412
    ('S', 193),   # Ser193
    ('S', 197),   # Ser197 - H-bond to catechol
]

# 5-HT2B orthosteric pocket (to AVOID)
HT2B_POCKET_RESIDUES = [
    ('D', 135),   # Asp135 - amine binding
    ('V', 136),   # Val136
    ('S', 139),   # Ser139
    ('T', 140),   # Thr140
    ('W', 337),   # Trp337 - aromatic
    ('F', 340),   # Phe340 - aromatic
    ('F', 341),   # Phe341 - aromatic
    ('N', 344),   # Asn344
    ('Y', 370),   # Tyr370
    ('L', 209),   # Leu209
    ('M', 218),   # Met218
    ('L', 347),   # Leu347
]

# Pocket extraction parameters
POCKET_RADIUS = 10.0  # Angstroms from center


# =============================================================================
# PDB FETCHING
# =============================================================================

def fetch_pdb(pdb_id: str, output_dir: str = "structures") -> Optional[str]:
    """Fetch PDB structure from RCSB."""
    out_path = Path(output_dir)
    out_path.mkdir(exist_ok=True)

    pdb_file = out_path / f"{pdb_id}.pdb"

    if pdb_file.exists():
        print(f"  Using cached: {pdb_file}")
        return str(pdb_file)

    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    print(f"  Fetching: {url}")

    try:
        urllib.request.urlretrieve(url, pdb_file)
        print(f"  Saved: {pdb_file}")
        return str(pdb_file)
    except Exception as e:
        print(f"  ERROR fetching {pdb_id}: {e}")
        return None


# =============================================================================
# STRUCTURE PARSING
# =============================================================================

def parse_pdb_atoms(pdb_file: str) -> List[Dict]:
    """Parse ATOM records from PDB file."""
    atoms = []

    with open(pdb_file) as f:
        for line in f:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                atom = {
                    'record': line[:6].strip(),
                    'serial': int(line[6:11]),
                    'name': line[12:16].strip(),
                    'altloc': line[16].strip(),
                    'resname': line[17:20].strip(),
                    'chain': line[21].strip(),
                    'resseq': int(line[22:26]),
                    'x': float(line[30:38]),
                    'y': float(line[38:46]),
                    'z': float(line[46:54]),
                    'occupancy': float(line[54:60]) if line[54:60].strip() else 1.0,
                    'tempfactor': float(line[60:66]) if line[60:66].strip() else 0.0,
                    'element': line[76:78].strip() if len(line) > 76 else '',
                }
                atoms.append(atom)

    return atoms


def get_receptor_chain(atoms: List[Dict], pdb_id: str) -> str:
    """Identify the receptor chain (usually A or R)."""
    # For GPCRs, receptor is typically chain A or R
    chains = set(a['chain'] for a in atoms if a['record'] == 'ATOM')

    # D2R in 6CM4 is chain R
    if pdb_id == "6CM4" and 'R' in chains:
        return 'R'
    # 5-HT2B in 6DRX is chain A
    if pdb_id == "6DRX" and 'A' in chains:
        return 'A'

    # Default to first chain
    return sorted(chains)[0] if chains else 'A'


def extract_binding_pocket(
    atoms: List[Dict],
    pocket_residues: List[Tuple[str, int]],
    chain: str,
    radius: float = POCKET_RADIUS,
) -> Dict:
    """
    Extract binding pocket coordinates and properties.

    Returns pocket center, residue atoms, and geometric properties.
    """
    # Get atoms for pocket residues
    pocket_atoms = []
    residue_info = {}

    for aa, resnum in pocket_residues:
        res_atoms = [
            a for a in atoms
            if a['chain'] == chain and a['resseq'] == resnum and a['record'] == 'ATOM'
        ]

        if res_atoms:
            pocket_atoms.extend(res_atoms)
            residue_info[f"{aa}{resnum}"] = {
                'resname': res_atoms[0]['resname'],
                'n_atoms': len(res_atoms),
                'center': [
                    np.mean([a['x'] for a in res_atoms]),
                    np.mean([a['y'] for a in res_atoms]),
                    np.mean([a['z'] for a in res_atoms]),
                ],
            }

    if not pocket_atoms:
        print(f"  WARNING: No pocket atoms found for chain {chain}")
        return {}

    # Calculate pocket center
    coords = np.array([[a['x'], a['y'], a['z']] for a in pocket_atoms])
    center = coords.mean(axis=0)

    # Calculate pocket dimensions
    distances = np.linalg.norm(coords - center, axis=1)
    max_radius = distances.max()
    mean_radius = distances.mean()

    # Get pocket volume estimate (convex hull approximation)
    volume_estimate = (4/3) * np.pi * (mean_radius ** 3)

    # Identify key interaction points
    # Asp (D) for amine binding
    asp_atoms = [a for a in pocket_atoms if a['resname'] == 'ASP']
    asp_center = None
    if asp_atoms:
        asp_center = [
            np.mean([a['x'] for a in asp_atoms]),
            np.mean([a['y'] for a in asp_atoms]),
            np.mean([a['z'] for a in asp_atoms]),
        ]

    # Aromatic residues (Trp, Phe, Tyr) for pi-stacking
    aromatic_atoms = [a for a in pocket_atoms if a['resname'] in ['TRP', 'PHE', 'TYR']]
    aromatic_center = None
    if aromatic_atoms:
        aromatic_center = [
            np.mean([a['x'] for a in aromatic_atoms]),
            np.mean([a['y'] for a in aromatic_atoms]),
            np.mean([a['z'] for a in aromatic_atoms]),
        ]

    return {
        'center': center.tolist(),
        'max_radius': float(max_radius),
        'mean_radius': float(mean_radius),
        'volume_estimate_A3': float(volume_estimate),
        'n_pocket_atoms': len(pocket_atoms),
        'n_residues': len(residue_info),
        'residues': residue_info,
        'asp_amine_site': asp_center,
        'aromatic_cage_center': aromatic_center,
        'pocket_residue_list': [f"{aa}{num}" for aa, num in pocket_residues],
    }


def calculate_pocket_differences(d2r_pocket: Dict, ht2b_pocket: Dict) -> Dict:
    """
    Calculate structural differences between D2R and 5-HT2B pockets.

    These differences are what we exploit for selectivity.
    """
    if not d2r_pocket or not ht2b_pocket:
        return {}

    # Volume difference
    vol_diff = d2r_pocket['volume_estimate_A3'] - ht2b_pocket['volume_estimate_A3']

    # Radius difference
    radius_diff = d2r_pocket['mean_radius'] - ht2b_pocket['mean_radius']

    # Key differences for selectivity
    selectivity_notes = []

    # D2R has Ser193/197 for catechol H-bonding (5-HT2B has different residues)
    if 'S193' in d2r_pocket.get('residues', {}):
        selectivity_notes.append("D2R Ser193: H-bond donor for catechol (exploit for selectivity)")

    # 5-HT2B has Met218 creating different steric environment
    selectivity_notes.append("5-HT2B Met218: Creates steric clash opportunity (design bulky group)")

    # 5-HT2B has Leu347 vs D2R has different residue
    selectivity_notes.append("5-HT2B Leu347: Hydrophobic difference (exploit for selectivity)")

    return {
        'volume_difference_A3': vol_diff,
        'radius_difference_A': radius_diff,
        'd2r_larger': vol_diff > 0,
        'selectivity_notes': selectivity_notes,
        'design_strategy': [
            "1. Match D2R Asp114 for amine binding (conserved)",
            "2. Optimize for D2R Ser193/197 H-bonding",
            "3. Add steric bulk incompatible with 5-HT2B Met218",
            "4. Exploit aromatic cage differences (Phe vs Leu)",
        ],
    }


# =============================================================================
# OUTPUT
# =============================================================================

def save_pocket_data(
    pocket_data: Dict,
    receptor_name: str,
    pdb_id: str,
    output_dir: str,
) -> str:
    """Save pocket data to JSON."""
    out_path = Path(output_dir)
    out_path.mkdir(exist_ok=True)

    filename = out_path / f"{pdb_id}_pocket.json"

    output = {
        'receptor': receptor_name,
        'pdb_id': pdb_id,
        'extraction_date': datetime.now().isoformat(),
        'pocket_data': pocket_data,
    }

    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)

    return str(filename)


def save_pocket_pdb(
    atoms: List[Dict],
    pocket_residues: List[Tuple[str, int]],
    chain: str,
    output_file: str,
) -> None:
    """Save pocket residues as separate PDB file."""
    residue_nums = {num for _, num in pocket_residues}

    with open(output_file, 'w') as f:
        f.write(f"REMARK Binding pocket extraction\n")
        f.write(f"REMARK Chain: {chain}\n")
        f.write(f"REMARK Residues: {len(pocket_residues)}\n")

        for atom in atoms:
            if atom['chain'] == chain and atom['resseq'] in residue_nums:
                line = (
                    f"ATOM  {atom['serial']:5d} {atom['name']:4s} "
                    f"{atom['resname']:3s} {atom['chain']}{atom['resseq']:4d}    "
                    f"{atom['x']:8.3f}{atom['y']:8.3f}{atom['z']:8.3f}"
                    f"{atom['occupancy']:6.2f}{atom['tempfactor']:6.2f}\n"
                )
                f.write(line)

        f.write("END\n")


# =============================================================================
# MAIN
# =============================================================================

def run_target_extraction(output_dir: str = ".") -> Dict:
    """Run the complete target extraction pipeline."""

    print("="*70)
    print("M4 PITUITARY TARGET EXTRACTION")
    print("="*70)
    print("\nExtracting receptor structures for prolactinoma therapeutic design")
    print("\nTARGET: Dopamine D2 Receptor (D2R)")
    print("  - PDB: 6CM4 (active state with Gi protein)")
    print("  - Goal: Design agonist to activate D2R → tumor apoptosis")
    print("\nNEGATIVE CONTROL: 5-HT2B Serotonin Receptor")
    print("  - PDB: 6DRX")
    print("  - Goal: AVOID binding to prevent cardiac side effects")

    structures_dir = Path(output_dir) / "structures"
    structures_dir.mkdir(exist_ok=True)

    results = {
        'timestamp': datetime.now().isoformat(),
        'targets': {},
    }

    # ==========================================================================
    # FETCH D2R STRUCTURE
    # ==========================================================================
    print("\n" + "="*70)
    print("STEP 1: Dopamine D2 Receptor (TARGET)")
    print("="*70)

    d2r_file = fetch_pdb(D2R_PDB, str(structures_dir))

    if d2r_file:
        d2r_atoms = parse_pdb_atoms(d2r_file)
        d2r_chain = get_receptor_chain(d2r_atoms, D2R_PDB)
        print(f"  Receptor chain: {d2r_chain}")
        print(f"  Total atoms: {len(d2r_atoms)}")

        d2r_pocket = extract_binding_pocket(
            d2r_atoms, D2R_POCKET_RESIDUES, d2r_chain
        )

        if d2r_pocket:
            print(f"  Pocket atoms: {d2r_pocket['n_pocket_atoms']}")
            print(f"  Pocket center: ({d2r_pocket['center'][0]:.1f}, "
                  f"{d2r_pocket['center'][1]:.1f}, {d2r_pocket['center'][2]:.1f})")
            print(f"  Pocket radius: {d2r_pocket['mean_radius']:.1f} Å")
            print(f"  Volume estimate: {d2r_pocket['volume_estimate_A3']:.0f} Å³")

            # Save pocket data
            pocket_json = save_pocket_data(
                d2r_pocket, D2R_NAME, D2R_PDB, str(structures_dir)
            )
            print(f"  Saved: {pocket_json}")

            # Save pocket PDB
            pocket_pdb = structures_dir / f"{D2R_PDB}_pocket.pdb"
            save_pocket_pdb(d2r_atoms, D2R_POCKET_RESIDUES, d2r_chain, str(pocket_pdb))
            print(f"  Saved: {pocket_pdb}")

            results['targets']['D2R'] = {
                'pdb_id': D2R_PDB,
                'name': D2R_NAME,
                'uniprot': D2R_UNIPROT,
                'chain': d2r_chain,
                'pocket': d2r_pocket,
                'pocket_file': str(pocket_pdb),
                'role': 'PRIMARY_TARGET',
            }

    # ==========================================================================
    # FETCH 5-HT2B STRUCTURE
    # ==========================================================================
    print("\n" + "="*70)
    print("STEP 2: 5-HT2B Serotonin Receptor (NEGATIVE CONTROL)")
    print("="*70)

    ht2b_file = fetch_pdb(HT2B_PDB, str(structures_dir))

    if ht2b_file:
        ht2b_atoms = parse_pdb_atoms(ht2b_file)
        ht2b_chain = get_receptor_chain(ht2b_atoms, HT2B_PDB)
        print(f"  Receptor chain: {ht2b_chain}")
        print(f"  Total atoms: {len(ht2b_atoms)}")

        ht2b_pocket = extract_binding_pocket(
            ht2b_atoms, HT2B_POCKET_RESIDUES, ht2b_chain
        )

        if ht2b_pocket:
            print(f"  Pocket atoms: {ht2b_pocket['n_pocket_atoms']}")
            print(f"  Pocket center: ({ht2b_pocket['center'][0]:.1f}, "
                  f"{ht2b_pocket['center'][1]:.1f}, {ht2b_pocket['center'][2]:.1f})")
            print(f"  Pocket radius: {ht2b_pocket['mean_radius']:.1f} Å")
            print(f"  Volume estimate: {ht2b_pocket['volume_estimate_A3']:.0f} Å³")

            # Save pocket data
            pocket_json = save_pocket_data(
                ht2b_pocket, HT2B_NAME, HT2B_PDB, str(structures_dir)
            )
            print(f"  Saved: {pocket_json}")

            # Save pocket PDB
            pocket_pdb = structures_dir / f"{HT2B_PDB}_pocket.pdb"
            save_pocket_pdb(ht2b_atoms, HT2B_POCKET_RESIDUES, ht2b_chain, str(pocket_pdb))
            print(f"  Saved: {pocket_pdb}")

            results['targets']['5HT2B'] = {
                'pdb_id': HT2B_PDB,
                'name': HT2B_NAME,
                'uniprot': HT2B_UNIPROT,
                'chain': ht2b_chain,
                'pocket': ht2b_pocket,
                'pocket_file': str(pocket_pdb),
                'role': 'NEGATIVE_CONTROL',
            }

    # ==========================================================================
    # SELECTIVITY ANALYSIS
    # ==========================================================================
    print("\n" + "="*70)
    print("STEP 3: Selectivity Analysis")
    print("="*70)

    if 'D2R' in results['targets'] and '5HT2B' in results['targets']:
        d2r_pocket = results['targets']['D2R']['pocket']
        ht2b_pocket = results['targets']['5HT2B']['pocket']

        differences = calculate_pocket_differences(d2r_pocket, ht2b_pocket)
        results['selectivity_analysis'] = differences

        print(f"\n  Volume difference: {differences['volume_difference_A3']:.0f} Å³")
        print(f"  D2R pocket larger: {differences['d2r_larger']}")

        print("\n  SELECTIVITY DESIGN STRATEGY:")
        for note in differences.get('design_strategy', []):
            print(f"    {note}")

    # ==========================================================================
    # SUMMARY
    # ==========================================================================
    print("\n" + "="*70)
    print("EXTRACTION COMPLETE")
    print("="*70)

    print(f"\nStructures saved to: {structures_dir}")
    print("\nFiles created:")
    for target_id, target_data in results.get('targets', {}).items():
        print(f"  - {target_data['pdb_id']}.pdb (full structure)")
        print(f"  - {target_data['pdb_id']}_pocket.pdb (binding pocket)")
        print(f"  - {target_data['pdb_id']}_pocket.json (pocket analysis)")

    # Save master results
    results_file = Path(output_dir) / "target_extraction_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nMaster results: {results_file}")

    return results


if __name__ == "__main__":
    import os
    os.chdir(Path(__file__).parent)
    results = run_target_extraction()
