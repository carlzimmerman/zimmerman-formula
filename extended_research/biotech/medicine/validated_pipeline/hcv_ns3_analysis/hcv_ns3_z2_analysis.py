#!/usr/bin/env python3
"""
Monomeric_Cleft_C NS3 Protease Z² Distance Analysis
======================================
Author: Carl Zimmerman
Date: 2026-04-24

Analyzes aromatic residue distances in the Monomeric_Cleft_C NS3 protease structure
to identify Z² matches and potential peptide binding hotspots.

Z² Biological Constant: 6.015152508891966 Å
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import defaultdict
import json

# =============================================================================
# CONSTANTS
# =============================================================================

Z2_BIOLOGICAL_CONSTANT = 6.015152508891966  # Angstroms
TOLERANCE_STRICT = 0.01    # 0.01 Å = "atomic engineering" precision
TOLERANCE_MODERATE = 0.10  # 0.10 Å = strong validation
TOLERANCE_LOOSE = 0.50     # 0.50 Å = general support

# Aromatic residues
AROMATICS = {'PHE', 'TRP', 'TYR', 'HIS'}

# Ring atoms for centroid calculation
RING_ATOMS = {
    'PHE': ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'],
    'TYR': ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'],
    'TRP': ['CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2'],
    'HIS': ['CG', 'ND1', 'CD2', 'CE1', 'NE2'],
}

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class Atom:
    """Single atom with coordinates"""
    name: str
    residue: str
    chain: str
    resnum: int
    x: float
    y: float
    z: float

    @property
    def coords(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])

@dataclass
class AromaticResidue:
    """Aromatic residue with ring centroid"""
    resname: str
    chain: str
    resnum: int
    centroid: np.ndarray
    atoms: List[Atom]

    def __repr__(self):
        return f"{self.chain}:{self.resname}{self.resnum}"

@dataclass
class AromaticPair:
    """Pair of aromatic residues with distance"""
    res1: AromaticResidue
    res2: AromaticResidue
    distance: float
    deviation_from_z2: float

    @property
    def is_z2_match(self) -> bool:
        return abs(self.deviation_from_z2) < TOLERANCE_STRICT

    @property
    def match_quality(self) -> str:
        d = abs(self.deviation_from_z2)
        if d < TOLERANCE_STRICT:
            return "ATOMIC PRECISION"
        elif d < TOLERANCE_MODERATE:
            return "Strong match"
        elif d < TOLERANCE_LOOSE:
            return "Moderate match"
        else:
            return "No match"

# =============================================================================
# PDB PARSER
# =============================================================================

def parse_pdb(pdb_path: str) -> List[Atom]:
    """Parse atoms from PDB file"""
    atoms = []

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                try:
                    atom_name = line[12:16].strip()
                    resname = line[17:20].strip()
                    chain = line[21].strip()
                    resnum = int(line[22:26].strip())
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())

                    atoms.append(Atom(
                        name=atom_name,
                        residue=resname,
                        chain=chain,
                        resnum=resnum,
                        x=x, y=y, z=z
                    ))
                except (ValueError, IndexError):
                    continue

    return atoms

# =============================================================================
# AROMATIC ANALYSIS
# =============================================================================

def find_aromatic_residues(atoms: List[Atom]) -> List[AromaticResidue]:
    """Find all aromatic residues and calculate ring centroids"""
    aromatics = []

    # Group atoms by residue
    residue_atoms: Dict[Tuple[str, str, int], List[Atom]] = defaultdict(list)

    for atom in atoms:
        if atom.residue in AROMATICS:
            key = (atom.chain, atom.residue, atom.resnum)
            residue_atoms[key].append(atom)

    # Calculate centroids
    for (chain, resname, resnum), res_atoms in residue_atoms.items():
        ring_atom_names = RING_ATOMS.get(resname, [])

        ring_coords = []
        for atom in res_atoms:
            if atom.name in ring_atom_names:
                ring_coords.append(atom.coords)

        if len(ring_coords) >= 4:
            centroid = np.mean(ring_coords, axis=0)
            aromatics.append(AromaticResidue(
                resname=resname,
                chain=chain,
                resnum=resnum,
                centroid=centroid,
                atoms=res_atoms
            ))

    return aromatics

def calculate_all_distances(aromatics: List[AromaticResidue]) -> List[AromaticPair]:
    """Calculate all pairwise aromatic distances"""
    pairs = []

    for i, res1 in enumerate(aromatics):
        for j, res2 in enumerate(aromatics):
            if i >= j:
                continue

            distance = np.linalg.norm(res1.centroid - res2.centroid)
            deviation = distance - Z2_BIOLOGICAL_CONSTANT

            pairs.append(AromaticPair(
                res1=res1,
                res2=res2,
                distance=distance,
                deviation_from_z2=deviation
            ))

    pairs.sort(key=lambda p: abs(p.deviation_from_z2))
    return pairs

def analyze_interface_distances(aromatics: List[AromaticResidue]) -> List[AromaticPair]:
    """Calculate aromatic distances between different chains"""
    pairs = []

    for i, res1 in enumerate(aromatics):
        for j, res2 in enumerate(aromatics):
            if i >= j:
                continue
            if res1.chain == res2.chain:
                continue

            distance = np.linalg.norm(res1.centroid - res2.centroid)
            deviation = distance - Z2_BIOLOGICAL_CONSTANT

            pairs.append(AromaticPair(
                res1=res1,
                res2=res2,
                distance=distance,
                deviation_from_z2=deviation
            ))

    pairs.sort(key=lambda p: abs(p.deviation_from_z2))
    return pairs

def find_active_site_aromatics(aromatics: List[AromaticResidue],
                               catalytic_residues: List[int]) -> List[AromaticResidue]:
    """Find aromatics near the catalytic site"""
    active_site = []

    for res in aromatics:
        # Check if near any catalytic residue
        for cat_res in catalytic_residues:
            if abs(res.resnum - cat_res) < 20:  # Within 20 residues
                active_site.append(res)
                break

    return active_site

def compute_z2_contact_density(aromatics: List[AromaticResidue]) -> Dict[str, int]:
    """Count Z² contacts for each aromatic residue"""
    contacts = defaultdict(int)

    for i, res1 in enumerate(aromatics):
        for j, res2 in enumerate(aromatics):
            if i >= j:
                continue

            distance = np.linalg.norm(res1.centroid - res2.centroid)
            if abs(distance - Z2_BIOLOGICAL_CONSTANT) < TOLERANCE_LOOSE:
                contacts[str(res1)] += 1
                contacts[str(res2)] += 1

    return dict(contacts)

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_hcv_ns3_analysis(pdb_path: str):
    """Run complete Z² analysis on Monomeric_Cleft_C NS3"""

    print("=" * 80)
    print("  Monomeric_Cleft_C NS3 PROTEASE Z² DISTANCE ANALYSIS")
    print("=" * 80)
    print(f"\nPDB File: {pdb_path}")
    print(f"Z² Biological Constant: {Z2_BIOLOGICAL_CONSTANT:.12f} Å")
    print(f"Precision thresholds:")
    print(f"  - Atomic precision: ±{TOLERANCE_STRICT:.3f} Å")
    print(f"  - Strong match:     ±{TOLERANCE_MODERATE:.3f} Å")
    print(f"  - Moderate match:   ±{TOLERANCE_LOOSE:.3f} Å")

    # Parse structure
    print("\n" + "-" * 60)
    print("PARSING STRUCTURE")
    print("-" * 60)
    atoms = parse_pdb(pdb_path)
    print(f"Total atoms parsed: {len(atoms)}")

    # Find aromatics
    aromatics = find_aromatic_residues(atoms)
    print(f"Aromatic residues found: {len(aromatics)}")

    # Group by chain
    by_chain = defaultdict(list)
    for res in aromatics:
        by_chain[res.chain].append(res)

    print("\nAromatic inventory by chain:")
    for chain in sorted(by_chain.keys()):
        residues = by_chain[chain]
        print(f"\n  Chain {chain}: {len(residues)} aromatic residues")
        for res in sorted(residues, key=lambda r: r.resnum):
            print(f"    {res.resname}{res.resnum}")

    # Monomeric_Cleft_C NS3 catalytic triad: His57, Asp81, Ser139 (protease domain)
    # Key aromatic residues near active site
    print("\n" + "-" * 60)
    print("Monomeric_Cleft_C NS3 PROTEASE ACTIVE SITE CONTEXT")
    print("-" * 60)
    print("""
    Catalytic Triad: His57 - Asp81 - Ser139
    Key Substrate Pockets:
      S1: Phe154 (aromatic recognition)
      S2: His57 (catalytic)
      S3: Ala157 region
      S4: Phe43, Val55 region

    NS4A Cofactor binding region: residues 21-34
    """)

    # Calculate all distances
    print("\n" + "-" * 60)
    print("Z² DISTANCE ANALYSIS - ALL AROMATIC PAIRS")
    print("-" * 60)

    all_pairs = calculate_all_distances(aromatics)

    z2_matches = [p for p in all_pairs if p.is_z2_match]
    strong_matches = [p for p in all_pairs if abs(p.deviation_from_z2) < TOLERANCE_MODERATE]
    moderate_matches = [p for p in all_pairs if abs(p.deviation_from_z2) < TOLERANCE_LOOSE]

    print(f"\nTotal aromatic pairs analyzed: {len(all_pairs)}")
    print(f"Z² matches (±{TOLERANCE_STRICT} Å): {len(z2_matches)}")
    print(f"Strong matches (±{TOLERANCE_MODERATE} Å): {len(strong_matches)}")
    print(f"Moderate matches (±{TOLERANCE_LOOSE} Å): {len(moderate_matches)}")

    print("\nTop 20 closest matches to Z² constant:")
    print("-" * 80)
    print(f"{'Residue 1':<15} {'Residue 2':<15} {'Distance (Å)':>12} {'Δ from Z² (Å)':>14} {'Quality':<20}")
    print("-" * 80)

    for pair in all_pairs[:20]:
        print(f"{str(pair.res1):<15} {str(pair.res2):<15} "
              f"{pair.distance:>12.6f} {pair.deviation_from_z2:>+14.6f} {pair.match_quality:<20}")

    # Interface analysis (if multiple chains)
    if len(by_chain) > 1:
        print("\n" + "-" * 60)
        print("Z² DISTANCE ANALYSIS - INTER-CHAIN (Interface)")
        print("-" * 60)

        interface_pairs = analyze_interface_distances(aromatics)

        z2_interface = [p for p in interface_pairs if p.is_z2_match]
        strong_interface = [p for p in interface_pairs if abs(p.deviation_from_z2) < TOLERANCE_MODERATE]

        print(f"\nInter-chain aromatic pairs: {len(interface_pairs)}")
        print(f"Z² matches: {len(z2_interface)}")
        print(f"Strong matches: {len(strong_interface)}")

        if interface_pairs:
            print("\nTop 10 interface pairs closest to Z²:")
            print("-" * 80)
            for pair in interface_pairs[:10]:
                print(f"{str(pair.res1):<15} {str(pair.res2):<15} "
                      f"{pair.distance:>12.6f} {pair.deviation_from_z2:>+14.6f} {pair.match_quality:<20}")

    # Active site analysis
    print("\n" + "-" * 60)
    print("ACTIVE SITE AROMATIC ANALYSIS")
    print("-" * 60)

    # Key residues in Monomeric_Cleft_C NS3 active site region
    active_site_region = list(range(40, 180))  # Protease domain
    active_aromatics = [r for r in aromatics if r.resnum in active_site_region]

    print(f"\nAromatics in protease domain (40-180): {len(active_aromatics)}")
    for res in sorted(active_aromatics, key=lambda r: r.resnum):
        print(f"  {res}")

    # Calculate distances within active site
    active_pairs = []
    for i, res1 in enumerate(active_aromatics):
        for j, res2 in enumerate(active_aromatics):
            if i >= j:
                continue
            distance = np.linalg.norm(res1.centroid - res2.centroid)
            deviation = distance - Z2_BIOLOGICAL_CONSTANT
            active_pairs.append(AromaticPair(res1, res2, distance, deviation))

    active_pairs.sort(key=lambda p: abs(p.deviation_from_z2))

    print("\nActive site aromatic pairs closest to Z²:")
    print("-" * 80)
    for pair in active_pairs[:10]:
        print(f"{str(pair.res1):<15} {str(pair.res2):<15} "
              f"{pair.distance:>12.6f} {pair.deviation_from_z2:>+14.6f} {pair.match_quality:<20}")

    # Z² contact density
    print("\n" + "-" * 60)
    print("Z² CONTACT DENSITY (HOTSPOTS)")
    print("-" * 60)

    contacts = compute_z2_contact_density(aromatics)
    sorted_contacts = sorted(contacts.items(), key=lambda x: -x[1])

    print("\nResidues with most Z² contacts (potential binding hotspots):")
    print("-" * 40)
    for res, count in sorted_contacts[:15]:
        print(f"  {res:<20} {count} Z² contacts")

    # Key findings
    print("\n" + "=" * 80)
    print("  KEY FINDINGS FOR PEPTIDE DESIGN")
    print("=" * 80)

    # Identify best hotspots
    if sorted_contacts:
        top_hotspot = sorted_contacts[0][0]
        print(f"\n1. PRIMARY HOTSPOT: {top_hotspot}")
        print(f"   - Highest Z² contact density")
        print(f"   - Target for Trp/Tyr placement in peptide")

    # Best Z² match
    if all_pairs:
        best_match = all_pairs[0]
        print(f"\n2. BEST Z² DISTANCE MATCH:")
        print(f"   {best_match.res1} ↔ {best_match.res2}")
        print(f"   Distance: {best_match.distance:.6f} Å")
        print(f"   Deviation: {best_match.deviation_from_z2*1000:+.3f} milliÅ")
        print(f"   Quality: {best_match.match_quality}")

    # Active site recommendations
    print(f"\n3. PEPTIDE DESIGN RECOMMENDATIONS:")
    print(f"   - Position aromatic (W/Y/F) to contact PHE154 at Z² distance")
    print(f"   - Include HIS for catalytic triad mimicry")
    print(f"   - Target S1-S4 pockets with appropriate sidechains")

    # Comparison to C2_Homodimer_A
    print(f"\n4. COMPARISON TO VALIDATED C2_Homodimer_A PROTEASE:")
    print(f"   - C2_Homodimer_A PHE53: Z² match at -1.3 milliÅ (VALIDATED)")
    print(f"   - Monomeric_Cleft_C best match: {all_pairs[0].deviation_from_z2*1000:+.3f} milliÅ")

    if abs(all_pairs[0].deviation_from_z2) < TOLERANCE_MODERATE:
        print(f"   - STATUS: COMPARABLE TO C2_Homodimer_A - GOOD CANDIDATE")
    else:
        print(f"   - STATUS: Weaker match than C2_Homodimer_A, may need different approach")

    # Save results
    results = {
        'pdb': pdb_path,
        'z2_constant': Z2_BIOLOGICAL_CONSTANT,
        'total_aromatics': len(aromatics),
        'total_pairs': len(all_pairs),
        'z2_matches': len(z2_matches),
        'strong_matches': len(strong_matches),
        'moderate_matches': len(moderate_matches),
        'best_match': {
            'res1': str(all_pairs[0].res1),
            'res2': str(all_pairs[0].res2),
            'distance': float(all_pairs[0].distance),
            'deviation_angstrom': float(all_pairs[0].deviation_from_z2),
            'deviation_milliangstrom': float(all_pairs[0].deviation_from_z2 * 1000)
        } if all_pairs else None,
        'hotspots': sorted_contacts[:10],
        'aromatics_by_chain': {
            chain: [str(r) for r in residues]
            for chain, residues in by_chain.items()
        },
        'top_20_pairs': [
            {
                'res1': str(p.res1),
                'res2': str(p.res2),
                'distance': float(p.distance),
                'deviation': float(p.deviation_from_z2),
                'quality': p.match_quality
            }
            for p in all_pairs[:20]
        ]
    }

    json_path = pdb_path.replace('.pdb', '_z2_analysis.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {json_path}")

    print("\n" + "=" * 80)

    return results


if __name__ == "__main__":
    results = run_hcv_ns3_analysis("1CU1.pdb")
