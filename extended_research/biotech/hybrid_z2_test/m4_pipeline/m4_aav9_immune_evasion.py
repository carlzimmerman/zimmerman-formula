#!/usr/bin/env python3
"""
M4 AAV9 Immune Evasion Engineering
===================================

Computationally model glycan shielding on the AAV9 capsid to reduce immunogenicity
for improved in vivo gene therapy delivery.

Target: AAV9 target macromolecule capsid (PDB: 3UX1)
Approach: N-linked glycosylation motif introduction at immunogenic epitopes

Gene therapy applications:
- Spinal muscular atrophy (CNS delivery)
- Limb-girdle muscular dystrophy
- Lysosomal storage disorders
- Inherited retinal diseases

License: AGPL-3.0 + OpenMTA + CC-BY-SA-4.0 (Open Science Prior Art)
"""

import json
import hashlib
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
import re

# N-linked glycosylation sequon: Asn-X-Ser/Thr (X != Pro)
GLYCAN_MOTIF = "N-X-S/T"  # NXS or NXT where X != P

# AAV9 VP1 hypervariable regions (antibody epitopes)
# These loops are the primary targets for neutralizing antibodies
AAV9_HYPERVARIABLE_REGIONS = {
    'HVR_I': (261, 268),      # Loop I
    'HVR_II': (328, 336),     # Loop II
    'HVR_III': (380, 391),    # Loop III
    'HVR_IV': (450, 475),     # Loop IV (major epitope)
    'HVR_V': (492, 506),      # Loop V
    'HVR_VI': (526, 540),     # Loop VI
    'HVR_VII': (580, 590),    # Loop VII
    'HVR_VIII': (660, 674),   # Loop VIII
    'HVR_IX': (704, 720),     # Loop IX
}

# Known AAV9 neutralizing antibody epitopes
AAV9_NAB_EPITOPES = [
    {'region': 'HVR_IV', 'residues': [453, 455, 456, 458, 459, 460], 'importance': 'high'},
    {'region': 'HVR_V', 'residues': [493, 496, 498, 500], 'importance': 'high'},
    {'region': 'HVR_VI', 'residues': [527, 529, 531, 533], 'importance': 'medium'},
    {'region': 'HVR_VIII', 'residues': [661, 663, 665, 667], 'importance': 'medium'},
]

# Amino acid properties for RSA calculation
AA_RSA_SCALE = {
    'A': 113, 'R': 241, 'N': 158, 'D': 151, 'C': 140,
    'Q': 189, 'E': 183, 'G': 85, 'H': 194, 'I': 182,
    'L': 180, 'K': 211, 'M': 204, 'F': 218, 'P': 143,
    'S': 122, 'T': 146, 'W': 259, 'Y': 229, 'V': 160,
}

# AAV9 VP1 reference sequence (canonical)
AAV9_VP1_SEQUENCE = """
MAADGYLPDWLEDTLSEGIRQWWKLKPGPPPPKPAERHKDDSRGLVLPGYKYLGPFNGLDKGEPVNEADAAALEHDKAYDRQLDSGDNPYLKYNHADAEFQERLKEDTSFGGNLGRAVFQAKKRVLEPLGLVEEPVKTAPGKKRPVEHSPVEPDSSSGTGKAGQQPARKRLNFGQTGDADSVPDPQPLGQPPAAPSGLGTNTMATGSGAPMADNNEGADGVGNSSGNWHCDSTWMGDRVITTSTRTWALPTYNNHLYKQISSQSGASNDNHYFGYSTPWGYFDFNRFHCHFSPRDWQRLINNNWGFRPKRLNFKLFNIQVKEVTQNDGTTTIANNLTSTVQVFTDSEYQLPYVLGSAHQGCLPPFPADVFMVPQYGYLTLNNGSQAVGRSSFYCLEYFPSQMLRTGNNFTFSYTFEDVPFHSSYAHSQSLDRLMNPLIDQYLYYLSRTNTPSGTTTQSRLQFSQAGASDIRDQSRNWLPGPCYRQQRVSKTSADNNNSEYSWTGATKYHLNGRDSLVNPGPAMASHKDDEEKFFPQSGVLIFGKQGSEKTNVDIEKVMITDEEEIRTTNPVATEQYGSVSTNLQRGNRQAATADVNTQGVLPGMVWQDRDVYLQGPIWAKIPHTDGHFHPSPLMGGFGLKHPPPQILIKNTPVPANPSTTFSAAKFASFITQYSTGQVSVEIEWELQKENSKRWNPEIQYTSNYNKSVNVDFTVDTNGVYSEPRPIGTRYLTRNL
"""

# Clean the sequence
AAV9_VP1 = re.sub(r'\s+', '', AAV9_VP1_SEQUENCE)


class AAV9ImmuneEvasionEngineer:
    """
    Engineers AAV9 capsid variants with reduced immunogenicity through
    strategic glycan shielding at neutralizing antibody epitopes.
    """

    def __init__(self, output_dir: str = "aav9_engineered"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.pdb_cache = {}

    def fetch_pdb_structure(self, pdb_id: str) -> Optional[str]:
        """Fetch AAV9 capsid structure from RCSB."""
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"

        try:
            print(f"  Fetching AAV9 capsid structure: {pdb_id}...")
            with urllib.request.urlopen(url, timeout=60) as response:
                pdb_data = response.read().decode('utf-8')
                self.pdb_cache[pdb_id] = pdb_data
                return pdb_data
        except urllib.error.URLError as e:
            print(f"  Warning: Could not fetch {pdb_id}: {e}")
            return None

    def parse_pdb_atoms(self, pdb_data: str) -> List[Dict]:
        """Parse ATOM records from PDB."""
        atoms = []
        for line in pdb_data.split('\n'):
            if line.startswith('ATOM'):
                try:
                    atom = {
                        'serial': int(line[6:11].strip()),
                        'name': line[12:16].strip(),
                        'resname': line[17:20].strip(),
                        'chain': line[21],
                        'resnum': int(line[22:26].strip()),
                        'x': float(line[30:38].strip()),
                        'y': float(line[38:46].strip()),
                        'z': float(line[46:54].strip()),
                        'bfactor': float(line[60:66].strip()) if len(line) > 66 else 0,
                    }
                    atoms.append(atom)
                except (ValueError, IndexError):
                    continue
        return atoms

    def calculate_rsa(self, atoms: List[Dict], sequence: str) -> Dict[int, float]:
        """
        Calculate relative solvent accessibility (RSA) for each residue.

        Higher RSA = more exposed = better glycosylation site candidate.
        Uses simplified spherical probe model.
        """
        # Group atoms by residue
        residues = {}
        for atom in atoms:
            resnum = atom['resnum']
            if resnum not in residues:
                residues[resnum] = []
            residues[resnum].append(atom)

        rsa_values = {}

        for resnum, res_atoms in residues.items():
            # Count neighboring atoms (simplified accessibility)
            ca_atoms = [a for a in res_atoms if a['name'] == 'CA']
            if not ca_atoms:
                continue

            ca = ca_atoms[0]

            # Count atoms within 10Å (buried if many, exposed if few)
            neighbors = sum(
                1 for a in atoms
                if a['resnum'] != resnum and
                ((a['x']-ca['x'])**2 + (a['y']-ca['y'])**2 + (a['z']-ca['z'])**2) < 100
            )

            # Normalize to RSA (0-1 scale)
            # Fewer neighbors = more exposed
            max_neighbors = 150  # Typical for buried residue
            rsa = max(0, 1 - (neighbors / max_neighbors))
            rsa_values[resnum] = rsa

        return rsa_values

    def identify_epitope_positions(self, sequence: str, rsa_values: Dict[int, float]) -> List[Dict]:
        """
        Identify positions within hypervariable regions that are
        surface-exposed and targeted by neutralizing antibodies.
        """
        epitope_candidates = []

        for region_name, (start, end) in AAV9_HYPERVARIABLE_REGIONS.items():
            for pos in range(start, end + 1):
                if pos < len(sequence):
                    rsa = rsa_values.get(pos, 0.5)  # Default to moderate exposure

                    # Check if in known NAb epitope
                    is_nab_target = any(
                        pos in ep['residues']
                        for ep in AAV9_NAB_EPITOPES
                    )

                    if rsa > 0.3:  # Surface exposed
                        epitope_candidates.append({
                            'position': pos,
                            'residue': sequence[pos-1] if pos <= len(sequence) else 'X',
                            'region': region_name,
                            'rsa': rsa,
                            'is_nab_target': is_nab_target,
                            'priority': 'high' if is_nab_target else 'medium',
                        })

        # Sort by RSA and NAb targeting
        epitope_candidates.sort(key=lambda x: (-x['is_nab_target'], -x['rsa']))

        return epitope_candidates

    def design_glycosylation_sites(self, sequence: str, epitopes: List[Dict], max_sites: int = 5) -> List[Dict]:
        """
        Algorithmically introduce N-linked glycosylation motifs (Asn-X-Ser/Thr)
        at exposed hypervariable positions.

        Constraints:
        - X position cannot be Pro (breaks motif)
        - Must not disrupt receptor binding regions
        - Space sites at least 10 residues apart
        """
        glycan_sites = []
        used_positions = set()

        # Receptor binding regions to avoid (galactose binding)
        receptor_regions = [(271, 280), (499, 505)]  # LamR binding sites

        for epitope in epitopes:
            if len(glycan_sites) >= max_sites:
                break

            pos = epitope['position']

            # Check spacing
            if any(abs(pos - used) < 10 for used in used_positions):
                continue

            # Check not in receptor binding region
            in_receptor_region = any(
                start <= pos <= end
                for start, end in receptor_regions
            )
            if in_receptor_region:
                continue

            # Design NXS/NXT motif
            # Replace position with N, position+2 with S or T
            if pos + 2 <= len(sequence):
                original_aa = sequence[pos-1]
                position_plus1 = sequence[pos] if pos < len(sequence) else 'A'
                position_plus2 = sequence[pos+1] if pos+1 < len(sequence) else 'S'

                # Skip if position+1 is Pro (breaks glycosylation)
                if position_plus1 == 'P':
                    continue

                # Create mutation
                glycan_site = {
                    'position': pos,
                    'region': epitope['region'],
                    'original_sequence': sequence[pos-1:pos+2] if pos+2 <= len(sequence) else 'XXX',
                    'new_sequence': f"N{position_plus1}S",  # Introduce NXS
                    'mutations': [
                        f"{original_aa}{pos}N",  # Primary mutation to Asn
                        f"{position_plus2}{pos+2}S" if position_plus2 not in ['S', 'T'] else None,
                    ],
                    'glycan_type': 'N-linked_complex',
                    'expected_shielding_radius': 12.0,  # Å, typical N-glycan
                    'rsa': epitope['rsa'],
                    'is_nab_target': epitope['is_nab_target'],
                }
                glycan_site['mutations'] = [m for m in glycan_site['mutations'] if m]

                glycan_sites.append(glycan_site)
                used_positions.add(pos)

        return glycan_sites

    def apply_mutations(self, sequence: str, glycan_sites: List[Dict]) -> str:
        """Apply glycan site mutations to create engineered sequence."""
        seq_list = list(sequence)

        for site in glycan_sites:
            pos = site['position'] - 1  # Convert to 0-indexed

            if pos < len(seq_list):
                seq_list[pos] = 'N'  # Introduce Asn

            # Set +2 position to Ser if not already S/T
            if pos + 2 < len(seq_list) and seq_list[pos + 2] not in ['S', 'T']:
                seq_list[pos + 2] = 'S'

        return ''.join(seq_list)

    def generate_fasta(self, sequence: str, name: str, metadata: Dict) -> str:
        """Generate FASTA with comprehensive metadata."""

        seq_hash = hashlib.sha256(sequence.encode()).hexdigest()[:8]

        header = (f">{name}|type=aav_capsid|serotype=AAV9_engineered"
                  f"|modification=glycan_shielding")

        meta_lines = [
            f"; length={len(sequence)}|mw={len(sequence)*110:.1f}Da",
            f"; glycan_sites={metadata.get('glycan_count', 0)}",
            f"; target_regions={metadata.get('target_regions', [])}",
            f"; immunogenicity_reduction=estimated_{metadata.get('shield_coverage', 0):.0f}%",
            f"; hash={seq_hash}",
            f"; license=AGPL-3.0+OpenMTA+CC-BY-SA-4.0",
            f"; generated={datetime.now().isoformat()}",
        ]

        return header + '\n' + '\n'.join(meta_lines) + '\n' + sequence + '\n'

    def generate_pdb_mutations(self, pdb_data: str, glycan_sites: List[Dict]) -> str:
        """
        Generate modified PDB with glycan site mutations annotated.
        Returns PDB with REMARK records describing mutations.
        """
        remarks = [
            "REMARK  99 M4 AAV9 IMMUNE EVASION ENGINEERING",
            "REMARK  99 GLYCAN SHIELDING MUTATIONS:",
        ]

        for i, site in enumerate(glycan_sites):
            remarks.append(f"REMARK  99   Site {i+1}: {site['region']} pos {site['position']}")
            remarks.append(f"REMARK  99     Mutations: {', '.join(site['mutations'])}")
            remarks.append(f"REMARK  99     Expected shielding: {site['expected_shielding_radius']} A")

        remarks.append("REMARK  99 LICENSE: AGPL-3.0 + OpenMTA + CC-BY-SA-4.0")

        return '\n'.join(remarks) + '\n' + pdb_data

    def run_engineering_pipeline(self, pdb_id: str = "3UX1") -> List[Dict]:
        """
        Run full AAV9 immune evasion engineering pipeline.

        1. Fetch AAV9 capsid structure
        2. Calculate surface accessibility
        3. Identify immunogenic epitopes
        4. Design glycan shielding sites
        5. Generate engineered variants
        6. Export results
        """
        print("=" * 70)
        print("M4 AAV9 IMMUNE EVASION ENGINEERING PIPELINE")
        print("Target: AAV9 capsid hypervariable regions")
        print("Strategy: N-linked glycan shielding of antibody epitopes")
        print("=" * 70)
        print()

        sequence = AAV9_VP1

        # Fetch structure
        print(f"[1/6] Fetching AAV9 capsid structure ({pdb_id})...")
        pdb_data = self.fetch_pdb_structure(pdb_id)

        if pdb_data:
            print(f"  Retrieved {len(pdb_data)} bytes")
            pdb_path = self.output_dir / f"{pdb_id}.pdb"
            pdb_path.write_text(pdb_data)
            atoms = self.parse_pdb_atoms(pdb_data)
            print(f"  Parsed {len(atoms)} atoms")
        else:
            print("  Using sequence-based analysis (structure fetch failed)")
            atoms = []

        # Calculate RSA
        print(f"\n[2/6] Calculating surface accessibility (RSA)...")
        rsa_values = self.calculate_rsa(atoms, sequence) if atoms else {}
        if rsa_values:
            avg_rsa = sum(rsa_values.values()) / len(rsa_values)
            print(f"  Analyzed {len(rsa_values)} residues | Mean RSA: {avg_rsa:.2f}")
        else:
            # Use default RSA for HVR regions
            for region, (start, end) in AAV9_HYPERVARIABLE_REGIONS.items():
                for pos in range(start, end + 1):
                    rsa_values[pos] = 0.7  # Assume HVR loops are exposed
            print(f"  Using predicted RSA for {len(rsa_values)} HVR positions")

        # Identify epitopes
        print(f"\n[3/6] Identifying neutralizing antibody epitope positions...")
        epitopes = self.identify_epitope_positions(sequence, rsa_values)
        high_priority = sum(1 for e in epitopes if e['is_nab_target'])
        print(f"  Found {len(epitopes)} exposed positions, {high_priority} known NAb targets")

        # Design glycan sites
        print(f"\n[4/6] Designing glycan shielding sites...")
        results = []

        # Generate variants with different numbers of glycan sites
        for n_sites in [3, 5, 7]:
            glycan_sites = self.design_glycosylation_sites(sequence, epitopes, max_sites=n_sites)
            print(f"\n  Variant with {len(glycan_sites)} glycan sites:")

            for site in glycan_sites:
                print(f"    {site['region']} pos {site['position']}: "
                      f"{site['original_sequence']} → {site['new_sequence']} "
                      f"({'NAb target' if site['is_nab_target'] else 'surface'})")

            # Apply mutations
            engineered_seq = self.apply_mutations(sequence, glycan_sites)
            mutations_count = sum(len(s['mutations']) for s in glycan_sites)

            # Calculate metrics
            target_regions = list(set(s['region'] for s in glycan_sites))
            shield_coverage = len(glycan_sites) * 12.0 * 3.14 / (4 * 3.14 * 25**2) * 100  # % of capsid surface

            variant_name = f"AAV9_glycan_shield_{len(glycan_sites)}sites"

            results.append({
                'name': variant_name,
                'sequence': engineered_seq,
                'length': len(engineered_seq),
                'glycan_sites': glycan_sites,
                'glycan_count': len(glycan_sites),
                'mutations_count': mutations_count,
                'target_regions': target_regions,
                'shield_coverage': min(shield_coverage, 100),
                'nab_epitopes_shielded': sum(1 for s in glycan_sites if s['is_nab_target']),
            })

        # Export
        print(f"\n[5/6] Exporting engineered sequences...")

        final_results = []
        for variant in results:
            name = variant['name']

            # Generate FASTA
            fasta = self.generate_fasta(variant['sequence'], name, variant)
            fasta_path = self.output_dir / f"{name}.fasta"
            fasta_path.write_text(fasta)

            # Generate annotated PDB if available
            if pdb_data:
                mod_pdb = self.generate_pdb_mutations(pdb_data, variant['glycan_sites'])
                pdb_out_path = self.output_dir / f"{name}.pdb"
                pdb_out_path.write_text(mod_pdb)

            result = {
                'name': name,
                'sequence': variant['sequence'],
                'length': variant['length'],
                'glycan_count': variant['glycan_count'],
                'mutations_count': variant['mutations_count'],
                'target_regions': variant['target_regions'],
                'shield_coverage_percent': variant['shield_coverage'],
                'nab_epitopes_shielded': variant['nab_epitopes_shielded'],
                'therapeutic_class': 'gene_therapy_vector',
                'indication': 'genetic_disorders',
                'fasta_path': str(fasta_path),
                'sha256': hashlib.sha256(variant['sequence'].encode()).hexdigest(),
                'timestamp': datetime.now().isoformat(),
                'license': 'AGPL-3.0 + OpenMTA + CC-BY-SA-4.0',
            }
            final_results.append(result)
            print(f"  Saved: {fasta_path}")

        # Generate wild-type reference
        wt_fasta = f">AAV9_VP1_wildtype|type=aav_capsid|serotype=AAV9\n{sequence}\n"
        wt_path = self.output_dir / "AAV9_VP1_wildtype.fasta"
        wt_path.write_text(wt_fasta)
        print(f"  Saved: {wt_path} (reference)")

        # Manifest
        print(f"\n[6/6] Generating manifest...")
        manifest = {
            'pipeline': 'M4_AAV9_Immune_Evasion',
            'version': '1.0.0',
            'target_pdb': pdb_id,
            'parent_serotype': 'AAV9',
            'strategy': 'N-linked_glycan_shielding',
            'mechanism': 'Steric occlusion of neutralizing antibody epitopes',
            'therapeutic_applications': [
                'Spinal muscular atrophy (SMA)',
                'Limb-girdle muscular dystrophy',
                'Pompe target system',
                'MPS disorders',
                'Inherited retinal diseases',
            ],
            'engineering_approach': {
                'epitope_identification': 'RSA-based surface accessibility',
                'glycan_motif': 'N-X-S/T (Asn-X-Ser/Thr)',
                'site_selection': 'HVR loops with known NAb targeting',
                'spacing_constraint': '>=10 residues between sites',
            },
            'generated': datetime.now().isoformat(),
            'license': 'AGPL-3.0 + OpenMTA + CC-BY-SA-4.0',
            'prior_art_declaration': 'Published as prior art to prevent patenting',
            'variants': final_results,
        }
        manifest_path = self.output_dir / "aav9_immune_evasion_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2))
        print(f"  Manifest: {manifest_path}")

        print("\n" + "=" * 70)
        print(f"PIPELINE COMPLETE: Generated {len(final_results)} AAV9 immune-evasive variants")
        print("=" * 70)

        return final_results


def main():
    """Main entry point."""
    engineer = AAV9ImmuneEvasionEngineer(output_dir="aav9_engineered")
    results = engineer.run_engineering_pipeline(pdb_id="3UX1")
    return results


if __name__ == "__main__":
    main()
