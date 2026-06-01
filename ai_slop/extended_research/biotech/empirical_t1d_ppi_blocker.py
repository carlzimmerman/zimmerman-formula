#!/usr/bin/env python3
"""
Empirical Type 1 Diabetes PPI Blocker

SPDX-License-Identifier: AGPL-3.0-or-later

This script models the autoimmune synapse in Type 1 Diabetes to identify
"cloaking" peptides that can block T-cell recognition of pancreatic beta
cell autoantigens without systemic immunosuppression.

Target System:
- MHC Class II (HLA-DR4) presenting GAD65 autoantigen
- T-Cell Receptor (TCR) recognition of peptide-MHC complex
- Goal: Block TCR-pMHC interaction with competitive inhibitor

Key Features:
- Real PDB structures from RCSB
- Interface residue identification (hotspots)
- Binding surface area calculation
- Peptide competitor design framework

References:
- Stadinski et al. (2010) PNAS: GAD65 recognition in T1D
- Concannon et al. (2009) NEJM: T1D genetics
- Atkinson et al. (2014) Lancet: T1D pathogenesis

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import os
import sys
import json
import requests
import numpy as np
from datetime import datetime
from typing import Optional, Dict, List, Tuple, Set
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# REAL DATA SOURCES
# ==============================================================================

PDB_API_URL = "https://files.rcsb.org/download/{}.pdb"
UNIPROT_API_URL = "https://rest.uniprot.org/uniprotkb/{}.fasta"

# ==============================================================================
# T1D RELEVANT STRUCTURES (REAL PDB IDs)
# ==============================================================================

T1D_STRUCTURES = {
    # MHC-peptide-TCR complexes
    'DR4_GAD65': {
        'pdb_id': '1J8H',  # HLA-DR4 with bound peptide (representative)
        'description': 'HLA-DR4 (DRB1*0401) MHC Class II',
        'role': 'Presents GAD65 autoantigen to T-cells'
    },
    'TCR_pMHC': {
        'pdb_id': '3TOE',  # TCR-pMHC complex
        'description': 'Human TCR bound to peptide-MHC',
        'role': 'Models diabetogenic T-cell recognition'
    },
    'HLA_DR3': {
        'pdb_id': '1A6A',  # HLA-DR3 structure
        'description': 'HLA-DR3 (DRB1*0301) - T1D risk allele',
        'role': 'Alternative MHC presenting autoantigen'
    },

    # Autoantigens
    'GAD65': {
        'uniprot_id': 'Q05329',  # Human GAD65
        'description': 'Glutamic Acid Decarboxylase 65kDa',
        'role': 'Major autoantigen in T1D',
        'epitopes': ['206-220', '247-266', '555-567']  # Known immunodominant epitopes
    },
    'Insulin': {
        'pdb_id': '4INS',
        'uniprot_id': 'P01308',
        'description': 'Human Insulin',
        'role': 'Autoantigen, self-tolerance target'
    },
    'IA2': {
        'uniprot_id': 'Q16849',  # Human IA-2
        'description': 'Islet Antigen 2 (ICA512)',
        'role': 'Transmembrane autoantigen in T1D'
    }
}

# Known GAD65 epitope sequences (immunodominant regions)
GAD65_EPITOPES = {
    '206-220': 'IATLKTFNQKIASLAR',
    '247-266': 'NMYAMMIARFKMFPEVKEKG',
    '555-567': 'PLGDKVNFFRMV'
}

# ==============================================================================
# DATA FETCHING
# ==============================================================================

def fetch_pdb_structure(pdb_id: str, output_dir: str = ".") -> str:
    """Fetch real PDB structure from RCSB."""
    pdb_id = pdb_id.upper()
    url = PDB_API_URL.format(pdb_id)

    print(f"  Fetching PDB: {pdb_id}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        os.makedirs(output_dir, exist_ok=True)
        pdb_path = os.path.join(output_dir, f"{pdb_id}.pdb")

        with open(pdb_path, 'w') as f:
            f.write(response.text)

        print(f"  Downloaded: {pdb_path}")
        return pdb_path

    except requests.exceptions.RequestException as e:
        print(f"  ERROR: Failed to fetch PDB {pdb_id}: {e}")
        raise


def fetch_uniprot_fasta(uniprot_id: str, output_dir: str = ".") -> Tuple[str, str]:
    """Fetch protein sequence from UniProt."""
    url = UNIPROT_API_URL.format(uniprot_id)

    print(f"  Fetching UniProt: {uniprot_id}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        fasta = response.text
        # Parse sequence
        lines = fasta.strip().split('\n')
        sequence = ''.join(lines[1:])

        os.makedirs(output_dir, exist_ok=True)
        fasta_path = os.path.join(output_dir, f"{uniprot_id}.fasta")

        with open(fasta_path, 'w') as f:
            f.write(fasta)

        print(f"  Downloaded: {fasta_path}")
        return fasta_path, sequence

    except requests.exceptions.RequestException as e:
        print(f"  ERROR: Failed to fetch UniProt {uniprot_id}: {e}")
        raise


# ==============================================================================
# STRUCTURE ANALYSIS
# ==============================================================================

class PDBParser:
    """Simple PDB file parser."""

    def __init__(self, pdb_path: str):
        self.pdb_path = pdb_path
        self.atoms = []
        self.residues = {}
        self.chains = set()
        self._parse()

    def _parse(self):
        """Parse PDB file."""
        with open(self.pdb_path, 'r') as f:
            for line in f:
                if line.startswith('ATOM') or line.startswith('HETATM'):
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
                        self.chains.add(atom['chain'])

                        res_key = (atom['chain'], atom['resid'])
                        if res_key not in self.residues:
                            self.residues[res_key] = {
                                'resname': atom['resname'],
                                'chain': atom['chain'],
                                'resid': atom['resid'],
                                'atoms': []
                            }
                        self.residues[res_key]['atoms'].append(atom)

                    except (ValueError, IndexError):
                        pass

    def get_coordinates(self, chain: str = None) -> np.ndarray:
        """Get all atom coordinates."""
        coords = []
        for atom in self.atoms:
            if chain is None or atom['chain'] == chain:
                coords.append([atom['x'], atom['y'], atom['z']])
        return np.array(coords) if coords else np.array([])

    def get_ca_coordinates(self, chain: str = None) -> Tuple[List, np.ndarray]:
        """Get CA atom coordinates and residue info."""
        residues = []
        coords = []
        for atom in self.atoms:
            if atom['name'] == 'CA':
                if chain is None or atom['chain'] == chain:
                    residues.append({
                        'chain': atom['chain'],
                        'resid': atom['resid'],
                        'resname': atom['resname']
                    })
                    coords.append([atom['x'], atom['y'], atom['z']])
        return residues, np.array(coords) if coords else np.array([])


class InterfaceAnalyzer:
    """
    Analyze protein-protein interfaces.

    Identifies interface residues (hotspots) between chains.
    """

    def __init__(self, pdb_parser: PDBParser):
        self.parser = pdb_parser

    def find_interface_residues(
        self,
        chain_a: str,
        chain_b: str,
        distance_cutoff: float = 4.5
    ) -> Dict:
        """
        Find interface residues between two chains.

        Args:
            chain_a: First chain ID
            chain_b: Second chain ID
            distance_cutoff: Distance cutoff for contacts (Angstroms)

        Returns:
            Dictionary with interface residues from each chain
        """
        print(f"\n  Finding interface between chains {chain_a} and {chain_b}")
        print(f"  Distance cutoff: {distance_cutoff} Å")

        # Get atoms for each chain
        atoms_a = [a for a in self.parser.atoms if a['chain'] == chain_a]
        atoms_b = [a for a in self.parser.atoms if a['chain'] == chain_b]

        print(f"  Chain {chain_a}: {len(atoms_a)} atoms")
        print(f"  Chain {chain_b}: {len(atoms_b)} atoms")

        if not atoms_a or not atoms_b:
            return {'chain_a': [], 'chain_b': [], 'contacts': []}

        # Find contacting residues
        interface_a = set()
        interface_b = set()
        contacts = []

        for atom_a in atoms_a:
            coord_a = np.array([atom_a['x'], atom_a['y'], atom_a['z']])

            for atom_b in atoms_b:
                coord_b = np.array([atom_b['x'], atom_b['y'], atom_b['z']])
                distance = np.linalg.norm(coord_a - coord_b)

                if distance < distance_cutoff:
                    res_a = (atom_a['chain'], atom_a['resid'], atom_a['resname'])
                    res_b = (atom_b['chain'], atom_b['resid'], atom_b['resname'])

                    interface_a.add(res_a)
                    interface_b.add(res_b)

                    contacts.append({
                        'atom_a': atom_a['name'],
                        'res_a': f"{atom_a['resname']}{atom_a['resid']}",
                        'atom_b': atom_b['name'],
                        'res_b': f"{atom_b['resname']}{atom_b['resid']}",
                        'distance': distance
                    })

        # Sort and format results
        interface_a = sorted(interface_a, key=lambda x: x[1])
        interface_b = sorted(interface_b, key=lambda x: x[1])

        print(f"\n  Interface residues (chain {chain_a}): {len(interface_a)}")
        print(f"  Interface residues (chain {chain_b}): {len(interface_b)}")
        print(f"  Total atomic contacts: {len(contacts)}")

        return {
            'chain_a': [{'chain': r[0], 'resid': r[1], 'resname': r[2]}
                       for r in interface_a],
            'chain_b': [{'chain': r[0], 'resid': r[1], 'resname': r[2]}
                       for r in interface_b],
            'contacts': contacts[:100]  # Limit for output
        }

    def compute_interface_area(
        self,
        chain_a: str,
        chain_b: str,
        probe_radius: float = 1.4
    ) -> Dict:
        """
        Compute buried surface area at interface.

        Uses simplified solvent-accessible surface area (SASA) calculation.

        Args:
            chain_a: First chain ID
            chain_b: Second chain ID
            probe_radius: Solvent probe radius (Angstroms)

        Returns:
            Dictionary with interface area metrics
        """
        print(f"\n  Computing interface surface area...")

        # Get CA coordinates as proxy
        _, coords_a = self.parser.get_ca_coordinates(chain_a)
        _, coords_b = self.parser.get_ca_coordinates(chain_b)

        if len(coords_a) == 0 or len(coords_b) == 0:
            return {'error': 'Insufficient coordinates'}

        # Simplified BSA calculation
        # Approximate each residue as sphere with radius ~3.5 Å

        residue_radius = 3.5
        all_coords = np.vstack([coords_a, coords_b])

        # Surface area of isolated chains (approximation)
        n_a = len(coords_a)
        n_b = len(coords_b)

        sasa_a_alone = n_a * 4 * np.pi * residue_radius**2
        sasa_b_alone = n_b * 4 * np.pi * residue_radius**2

        # Buried surface due to contacts
        buried_area = 0.0
        for i, ca in enumerate(coords_a):
            for j, cb in enumerate(coords_b):
                d = np.linalg.norm(ca - cb)
                if d < 2 * residue_radius + probe_radius:
                    # Approximation: burial proportional to overlap
                    overlap = max(0, 2 * residue_radius + probe_radius - d)
                    buried_area += np.pi * overlap * residue_radius

        # Interface area is buried area
        interface_area = buried_area

        print(f"  Chain {chain_a} SASA (alone): {sasa_a_alone:.1f} Å²")
        print(f"  Chain {chain_b} SASA (alone): {sasa_b_alone:.1f} Å²")
        print(f"  Buried surface area: {interface_area:.1f} Å²")

        return {
            'sasa_chain_a': sasa_a_alone,
            'sasa_chain_b': sasa_b_alone,
            'buried_surface_area': interface_area,
            'interface_score': interface_area / (sasa_a_alone + sasa_b_alone)
        }


# ==============================================================================
# CLOAKING PEPTIDE DESIGN
# ==============================================================================

class CloakingPeptideDesigner:
    """
    Design competitive peptide inhibitors to block TCR-pMHC interaction.

    Strategy:
    1. Identify interface hotspots on MHC that bind TCR
    2. Design peptides that competitively bind these hotspots
    3. Prevent T-cell recognition without systemic immunosuppression
    """

    def __init__(self, interface_residues: List[Dict]):
        self.hotspots = interface_residues
        self.candidates = []

    def identify_hotspots(self) -> List[Dict]:
        """
        Rank interface residues by importance.

        Hotspots are residues that contribute most to binding.
        """
        print("\n  Identifying binding hotspots...")

        # Residue types known to be important for protein-protein interactions
        HOTSPOT_RESIDUES = {
            'TRP': 3.0,  # Tryptophan - large aromatic
            'TYR': 2.5,  # Tyrosine - aromatic + H-bond
            'PHE': 2.0,  # Phenylalanine - aromatic
            'ARG': 2.0,  # Arginine - charge + H-bond
            'HIS': 1.5,  # Histidine - pH-sensitive
            'LYS': 1.5,  # Lysine - charge
            'GLU': 1.5,  # Glutamate - charge
            'ASP': 1.5,  # Aspartate - charge
        }

        ranked_hotspots = []
        for res in self.hotspots:
            score = HOTSPOT_RESIDUES.get(res['resname'], 1.0)
            ranked_hotspots.append({
                **res,
                'hotspot_score': score
            })

        # Sort by score
        ranked_hotspots.sort(key=lambda x: x['hotspot_score'], reverse=True)

        print(f"  Top hotspot residues:")
        for res in ranked_hotspots[:10]:
            print(f"    {res['resname']}{res['resid']} (score: {res['hotspot_score']:.1f})")

        return ranked_hotspots

    def design_blocking_peptides(
        self,
        epitope_sequence: str,
        n_variants: int = 5
    ) -> List[Dict]:
        """
        Design peptide variants that could block autoantigen presentation.

        Strategy: Modify autoantigen epitope to maintain MHC binding
        but ablate TCR recognition (altered peptide ligands).

        Args:
            epitope_sequence: Original immunodominant epitope
            n_variants: Number of variants to generate

        Returns:
            List of candidate blocking peptides
        """
        print(f"\n  Designing blocking peptide variants...")
        print(f"  Original epitope: {epitope_sequence}")

        candidates = []

        # TCR-contact positions (typically positions 5, 7, 8 in MHC groove)
        # These are the residues that contact TCR, not MHC anchors
        TCR_CONTACT_POSITIONS = [4, 5, 6, 7]  # 0-indexed

        # MHC anchor positions (keep these to maintain MHC binding)
        MHC_ANCHOR_POSITIONS = [0, 1, 8, len(epitope_sequence)-1]

        # Conservative substitutions for TCR ablation
        ABLATION_SUBS = {
            'L': ['A', 'G'],  # Large hydrophobic -> small
            'I': ['A', 'G'],
            'V': ['A', 'G'],
            'F': ['A', 'Y'],  # Aromatic changes
            'Y': ['F', 'A'],
            'W': ['F', 'A'],
            'K': ['R', 'A'],  # Charged
            'R': ['K', 'A'],
            'E': ['D', 'A'],
            'D': ['E', 'A'],
        }

        seq = list(epitope_sequence)

        for i in range(n_variants):
            variant = seq.copy()
            modifications = []

            # Modify TCR-contact positions
            for pos in TCR_CONTACT_POSITIONS:
                if pos < len(variant):
                    original = variant[pos]
                    subs = ABLATION_SUBS.get(original, ['A'])
                    if subs:
                        new_aa = subs[i % len(subs)]
                        variant[pos] = new_aa
                        modifications.append(f"{original}{pos+1}{new_aa}")

            variant_seq = ''.join(variant)

            candidates.append({
                'original': epitope_sequence,
                'variant': variant_seq,
                'modifications': modifications,
                'strategy': 'TCR contact ablation',
                'mhc_anchors_preserved': True
            })

        self.candidates = candidates

        print(f"\n  Generated {len(candidates)} blocking peptide candidates:")
        for i, cand in enumerate(candidates):
            print(f"    {i+1}. {cand['variant']} (mods: {', '.join(cand['modifications'])})")

        return candidates


# ==============================================================================
# MAIN PIPELINE
# ==============================================================================

def analyze_t1d_immune_synapse(output_dir: str = "t1d_ppi_analysis") -> Dict:
    """
    Analyze the T1D autoimmune synapse and design cloaking peptides.

    Pipeline:
    1. Fetch MHC-peptide and TCR structures
    2. Identify TCR-pMHC interface residues
    3. Compute binding surface area
    4. Design blocking peptides

    Returns:
        Complete analysis results
    """
    os.makedirs(output_dir, exist_ok=True)

    print("\n" + "="*70)
    print("TYPE 1 DIABETES PPI BLOCKER PIPELINE")
    print("="*70)
    print("Target: MHC-Autoantigen-TCR immune synapse")
    print("Goal: Block T-cell recognition of beta cell autoantigens")
    print("Strategy: Altered peptide ligands for competitive geometrically stabilize")
    print("="*70)

    results = {
        'pipeline': 'T1D PPI Blocker',
        'timestamp': datetime.now().isoformat(),
        'license': 'AGPL-3.0-or-later'
    }

    # Step 1: Fetch structures
    print("\n  [1] Fetching relevant structures...")

    # Fetch HLA-DR4 MHC structure
    mhc_info = T1D_STRUCTURES['DR4_GAD65']
    mhc_pdb = fetch_pdb_structure(mhc_info['pdb_id'], output_dir)

    # Parse structure
    parser = PDBParser(mhc_pdb)
    print(f"\n  Structure contains chains: {sorted(parser.chains)}")

    results['structure'] = {
        'pdb_id': mhc_info['pdb_id'],
        'description': mhc_info['description'],
        'chains': sorted(parser.chains),
        'n_atoms': len(parser.atoms),
        'n_residues': len(parser.residues)
    }

    # Step 2: Identify interface
    print("\n  [2] Analyzing protein-protein interface...")

    analyzer = InterfaceAnalyzer(parser)

    # Find interface between MHC chains (typically A and B are alpha/beta)
    # and peptide (typically chain C or P)
    chains = sorted(parser.chains)

    interface_results = {}
    if len(chains) >= 2:
        # Analyze primary interface
        chain_a = chains[0]
        chain_b = chains[1]

        interface = analyzer.find_interface_residues(chain_a, chain_b)
        interface_results[f'{chain_a}-{chain_b}'] = interface

        # Compute surface area
        area = analyzer.compute_interface_area(chain_a, chain_b)
        interface_results[f'{chain_a}-{chain_b}_area'] = area

    results['interface_analysis'] = interface_results

    # Step 3: Identify hotspots
    print("\n  [3] Identifying binding hotspots...")

    # Get interface residues for peptide binding groove
    all_interface_residues = []
    for key, data in interface_results.items():
        if not key.endswith('_area'):
            all_interface_residues.extend(data.get('chain_a', []))
            all_interface_residues.extend(data.get('chain_b', []))

    designer = CloakingPeptideDesigner(all_interface_residues)
    hotspots = designer.identify_hotspots()

    results['hotspots'] = hotspots[:20]  # Top 20

    # Step 4: Design blocking peptides
    print("\n  [4] Designing cloaking peptide candidates...")

    # Use GAD65 epitope 206-220 as template
    epitope = GAD65_EPITOPES['206-220']

    candidates = designer.design_blocking_peptides(epitope, n_variants=5)

    results['blocking_peptides'] = candidates

    # Step 5: Summary
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)

    print(f"\n  Structure: {results['structure']['pdb_id']}")
    print(f"  Chains analyzed: {results['structure']['chains']}")
    print(f"  Interface hotspots: {len(results['hotspots'])}")
    print(f"  Blocking peptide candidates: {len(results['blocking_peptides'])}")

    if results['hotspots']:
        print(f"\n  Top 5 binding hotspots (target for geometrically stabilize):")
        for res in results['hotspots'][:5]:
            print(f"    - {res['resname']}{res['resid']} (chain {res['chain']})")

    if results['blocking_peptides']:
        print(f"\n  Lead blocking peptide candidates:")
        for i, pep in enumerate(results['blocking_peptides'][:3]):
            print(f"    {i+1}. {pep['variant']}")
            print(f"       Strategy: {pep['strategy']}")

    # Save results
    results_file = os.path.join(output_dir, "t1d_ppi_analysis.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Full results saved: {results_file}")

    return results


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Run T1D PPI blocker analysis."""
    print("\n" + "="*70)
    print("EMPIRICAL T1D PPI BLOCKER")
    print("="*70)
    print("Indication: Type 1 Diabetes autoimmune targeting")
    print("Data: RCSB PDB + UniProt")
    print("License: AGPL-3.0-or-later")
    print("="*70)

    try:
        results = analyze_t1d_immune_synapse(output_dir="t1d_ppi_analysis")
        return results

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}


if __name__ == '__main__':
    main()
