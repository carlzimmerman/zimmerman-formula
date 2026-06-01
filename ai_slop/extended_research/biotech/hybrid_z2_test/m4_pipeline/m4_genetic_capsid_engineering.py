#!/usr/bin/env python3
"""
================================================================================
M4 GENETIC CAPSID ENGINEERING
================================================================================

Open-source structural biology pipeline for severe monogenic and neuromuscular
disorders, focusing on:
1. AAV capsids for spinal muscular atrophy (SMA) - Zolgensma-type vectors
2. AAV capsids for Duchenne muscular dystrophy (DMD) - muscle-tropic variants
3. Immune evasion engineering (glycan shielding of antigenic epitopes)

================================================================================
DEFENSIVE PUBLICATION & PATENT PREVENTION NOTICE
================================================================================

This work is published under AGPL-3.0 + OpenMTA + CC BY-SA 4.0 with
PATENT DEDICATION to the public domain.

All sequences, methods, and capsid modifications herein are PUBLIC DOMAIN
for patent purposes. This publication establishes PRIOR ART.

License: AGPL-3.0 (code) + OpenMTA + CC BY-SA 4.0 (sequences) + Patent Dedication
================================================================================

SCIENTIFIC BASIS:
- AAV9 crosses blood-brain barrier (enables systemic delivery for SMA)
- AAVrh74 has excellent muscle tropism (ideal for DMD)
- Immune responses limit redosing - glycan shielding can help
- Y-to-F mutations improve transduction efficiency (published, peer-reviewed)
- Capsid engineering can improve tissue specificity while reducing off-target

VALIDATED APPROACHES:
- AAV9-SMN1 (Zolgensma) - FDA approved for SMA
- AAVrh74-micro-dystrophin (Elevidys) - FDA approved for DMD
- Capsid shuffling and directed evolution (published methods)
- Epitope mapping and glycan insertion (peer-reviewed)

================================================================================
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple

# =============================================================================
# NEUROMUSCULAR GENE THERAPY CAPSIDS
# =============================================================================
# Sources: UniProt, PDB, published literature, FDA labels

CAPSID_DATABASE = {
    # =========================================================================
    # AAV9 - CNS-tropic (Zolgensma uses AAV9)
    # UniProt: Q6JC40, PDB: 3UX1
    # =========================================================================
    "aav9_sma": {
        "name": "AAV9 VP1 (SMA/CNS-optimized)",
        "uniprot": "Q6JC40",
        "serotype": "AAV9",
        "tropism": "CNS, motor neurons, systemic distribution",
        "clinical_application": "Spinal Muscular Atrophy (SMA)",
        "reference_drug": "Zolgensma (onasemnogene abeparvovec)",
        "sequence": "MAADGYLPDWLEDNLSEGIREWWALKPGAPQPKANQQHQDNARGLVLPGYKYLGPGNGLDKGEPVNAADAAALEHDKAYDQQLKAGDNPYLKYNHADAEFQERLKEDTSFGGNLGRAVFQAKKRLLEPLGLVEEAAKTAPGKKRPVEQSPQEPDSSAGIGKSGAQPAKKRLNFGQTGDTESVPDPQPIGEPPAAPSGVGSLTMASGGGAPVADNNEGADGVGSSSGNWHCDSQWLGDRVITTSTRTWALPTYNNHLYKQISNSTSGGSSNDNAYFGYSTPWGYFDFNRFHCHFSPRDWQRLINNNWGFRPKRLNFKLFNIQVKEVTDNNGVKTIANNLTSTVQVFTDSDYQLPYVLGSAHEGCLPPFPADVFMIPQYGYLTLNDGSQAVGRSSFYCLEYFPSQMLRTGNNFQFSYEFENVPFHSSYAHSQSLDRLMNPLIDQYLYYLSKTINGSGQNQQTLKFSVAGPSNMAVQGRNYIPGPSYRQQRVSTTVTQNNNSEFAWPGASSWALNGRNSLMNPGPAMASHKEGEDRFFPLSGSLIFGKQGTGRDNVDADKVMITNEEEIKTTNPVATESYGQVATNHQSAQAQAQTGWVQNQGILPGMVWQDRDVYLQGPIWAKIPHTDGNFHPSPLMGGFGMKHPPPQILIKNTPVPADPPTAFNKDKLNSFITQYSTGQVSVEIEWELQKENSKRWNPEIQYTSNYYKSNNVEFAVNTEGVYSEPRPIGTRYLTRNL",
        "length": 736,
        # Key engineering targets
        "tyrosine_positions": [252, 272, 444, 500, 704, 708, 731],
        "galactose_binding": [267, 268, 269, 502, 503, 504],
        "immunogenic_epitopes": [
            (262, 275, "Neutralizing epitope A"),
            (453, 468, "Neutralizing epitope B"),
            (493, 510, "Neutralizing epitope C"),
            (585, 600, "T-cell epitope cluster"),
            (659, 680, "Neutralizing epitope D")
        ],
        "disease_info": {
            "name": "Spinal Muscular Atrophy (SMA)",
            "gene": "SMN1",
            "inheritance": "Autosomal recessive",
            "incidence": "1 in 10,000 live births",
            "mechanism": "Loss of SMN protein leads to motor neuron degeneration"
        }
    },

    # =========================================================================
    # AAVrh74 - Muscle-tropic (Elevidys uses AAVrh74)
    # Rhesus macaque isolate with excellent muscle transduction
    # =========================================================================
    "aavrh74_dmd": {
        "name": "AAVrh74 VP1 (Muscle-optimized)",
        "serotype": "AAVrh74",
        "tropism": "Skeletal muscle, cardiac muscle, diaphragm",
        "clinical_application": "Duchenne Muscular Dystrophy (DMD)",
        "reference_drug": "Elevidys (delandistrogene moxeparvovec)",
        "sequence": "MAADGYLPDWLEDTLSEGIRQWWKLKPGPPPPKPAERHKDDSRGLVLPGYKYLGPFNGLDKGEPVNAADAAALEHDKAYDQQLQAGDNPYLKYNHADAEFQERLQEDTSFGGNLGRAVFQAKKRVLEPLGLVEEGAKTAPGKKRPVDQSPQEPDSSSGVGKSGKQPARKRLNFGQTGDSESVPDPQPLGEPPATPASGVGSGTMAAGGGAPMADNNEGADGVGNASGNWHCDSTWLGDRVITTSTRTWALPTYNNHLYKQISSASTGGSTNDNTYFGYSTPWGYFDFNRFHCHFSPRDWQRLINNNWGFRPKKLSFKLFNIQVKEVTTNDGVTTIANNLTSTVQVFSDSEYVLPYVLGSAHQGCLPPFPADVFMIPQYGYLTLNNGSQAVGRSSFYCLEYFPSQMLRTGNNFTFSYTFEEVPFHSSYAHSQSLDRLMNPLIDQYLYYLNRTQNQSGSAQNKDLLFSRGSPAGMSVQPKNWLPGPCYRQQRVSKTLTQNNNSNFAWTGATKYHLNGRDSLVNPGVAMATHKDDEERFFPSNGILIFGKQNAARDNADYSDVMLTSEEEIKTTNPVATEEYGIVADNLQQQNTAPQIGTVNSQGALPGMVWQNRDVYLQGPIWAKIPHTDGNFHPSPLMGGFGLKHPPPQILIKNTPVPADPPTTFSQAKLASFITQYSTGQVSVEIEWELQKENSKRWNPEIQYTSNYYKSTSVDFAVNTEGTYSEPRPIGTRYLTRNL",
        "length": 737,
        "tyrosine_positions": [252, 272, 444, 500, 703, 707, 730],
        "muscle_tropism_residues": [(263, 275), (493, 508), (585, 598)],
        "immunogenic_epitopes": [
            (262, 278, "Neutralizing epitope A"),
            (452, 470, "Neutralizing epitope B"),
            (493, 512, "Neutralizing epitope C"),
            (580, 600, "T-cell epitope cluster"),
            (656, 678, "Neutralizing epitope D")
        ],
        "disease_info": {
            "name": "Duchenne Muscular Dystrophy (DMD)",
            "gene": "DMD (dystrophin)",
            "inheritance": "X-linked recessive",
            "incidence": "1 in 3,500-5,000 male births",
            "mechanism": "Lack of dystrophin causes muscle fiber instability"
        }
    },

    # =========================================================================
    # AAV8 - Liver-detargeted variant for muscle
    # Modified to reduce liver uptake while maintaining muscle tropism
    # =========================================================================
    "aav8_muscle": {
        "name": "AAV8 VP1 (Muscle-optimized, liver-detargeted)",
        "uniprot": "Q8JQF8",
        "serotype": "AAV8",
        "tropism": "Skeletal muscle (engineered liver-detargeting)",
        "clinical_application": "Limb-girdle muscular dystrophies",
        "sequence": "MAADGYLPDWLEDNLSEGIREWWALKPGAPKPKANQQKQDDGRGLVLPGYKYLGPFNGLDKGEPVNAADAAALEHDKAYDQQLQAGDNPYLRYNHADAEFQERLQEDTSFGGNLGRAVFQAKKRVLEPLGLVEEGAKTAPGKKRPVEPSPQRSPDSSTGIGKKGQQPARKRLNFGQTGDSESVPDPQPLGEPPAAPTSLGSNTMASGGGAPMADNNEGADGVGSSSGNWHCDSTWMGDRVVTKSTNRIALPTYNNHLYKQISSQSGASNDNHYFGYSTPWGYFDFNRFHCHFSPRDWQRLINNNWGFRPKRLSFKLFNIQVKEVTQNEGTTKTIANNLTSTIQVFTDSEYQLPYVLGSAHQGCLPPFPADVFMVPQYGYLTLNNGSQAVGRSSFYCLEYFPSQMLRTGNNFQFTYTFEDVPFHSSYAHSQSLDRLMNPLIDQYLYYLNRTQNQSGSAQNKDLLFSRGSPAGMSVQPKNWLPGPCYRQQRVSTTLSQNNNSNFAWTGATKYHLNGRDSLVNPGVAMATHKDDEERFFPSSGVLMFGKQGAGKDNVDYSSVMLTSEEEIKTTNPVATEQYGVVADNLQQQNAAPIVGAVNSQGALPGMVWQNRDVYLQGPIWAKIPHTDGNFHPSPLMGGFGLKNPPPQILIKNTPVPADPPTTFNQAKLASFITQYSTGQVSVEIEWELQKENSKRWNPEIQYTSNYYKSTSVDFAVNTEGVYSEPRPIGTRYLTRNL",
        "length": 738,
        "tyrosine_positions": [252, 272, 444, 500, 703, 707, 733],
        "liver_binding_residues": [263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273],
        "immunogenic_epitopes": [
            (262, 276, "Neutralizing epitope A"),
            (451, 470, "Neutralizing epitope B"),
            (494, 510, "Neutralizing epitope C"),
            (661, 680, "Neutralizing epitope D")
        ],
        "disease_info": {
            "name": "Limb-girdle Muscular Dystrophies",
            "gene": "Various (SGCA, SGCB, etc.)",
            "inheritance": "Autosomal recessive/dominant",
            "incidence": "1 in 14,500-45,000",
            "mechanism": "Mutations in sarcoglycan complex or related proteins"
        }
    }
}

# =============================================================================
# THERAPEUTIC TRANSGENES (for reference)
# =============================================================================
# These are the genes delivered by the AAV vectors

THERAPEUTIC_GENES = {
    "SMN1": {
        "name": "Survival Motor Neuron 1",
        "uniprot": "Q16637",
        "length": 294,
        "target system": "SMA",
        "notes": "Codon-optimized version used in Zolgensma"
    },
    "micro_dystrophin": {
        "name": "Micro-dystrophin",
        "description": "Truncated dystrophin retaining key functional domains",
        "length": 3500,  # ~138 kDa
        "target system": "DMD",
        "notes": "Multiple designs (deltaR4-R23, deltaR4-R24/deltaR17, etc.)"
    }
}

# =============================================================================
# ENGINEERING FUNCTIONS
# =============================================================================

def calculate_properties(sequence: str) -> Dict:
    """Calculate basic molecular properties."""
    aa_weights = {
        'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2,
        'E': 147.1, 'Q': 146.2, 'G': 75.1, 'H': 155.2, 'I': 131.2,
        'L': 131.2, 'K': 146.2, 'M': 149.2, 'F': 165.2, 'P': 115.1,
        'S': 105.1, 'T': 119.1, 'W': 204.2, 'Y': 181.2, 'V': 117.1
    }

    mw = sum(aa_weights.get(aa, 110) for aa in sequence) - (len(sequence) - 1) * 18
    return {
        "length": len(sequence),
        "mw_da": round(mw, 2),
        "mw_kda": round(mw / 1000, 2)
    }


def apply_tyrosine_mutations(sequence: str, positions: List[int]) -> Tuple[str, List[Dict]]:
    """
    Apply Y-to-F mutations to improve AAV transduction efficiency.

    Scientific basis:
    - Zhong et al., PNAS 2008: Y-F mutations prevent ubiquitination
    - Markusic et al., Mol Ther 2010: Improved transduction in muscle
    - Multiple clinical and preclinical validations
    """
    seq_list = list(sequence)
    mutations = []

    for pos in positions:
        idx = pos - 1  # Convert to 0-indexed
        if 0 <= idx < len(seq_list) and seq_list[idx] == 'Y':
            seq_list[idx] = 'F'
            mutations.append({
                "position": pos,
                "original": "Y",
                "mutated": "F",
                "rationale": "Prevent ubiquitination, improve transduction"
            })

    return ''.join(seq_list), mutations


def map_antigenic_epitopes(sequence: str, epitopes: List[Tuple]) -> List[Dict]:
    """Map antigenic epitopes on the capsid sequence."""
    mapped = []
    for epitope in epitopes:
        start, end, name = epitope
        if start < len(sequence) and end <= len(sequence):
            epitope_seq = sequence[start-1:end]
            mapped.append({
                "name": name,
                "start": start,
                "end": end,
                "sequence": epitope_seq,
                "length": len(epitope_seq)
            })
    return mapped


def add_glycan_shield(sequence: str, epitopes: List[Tuple],
                      sites_per_epitope: int = 1) -> Tuple[str, List[Dict]]:
    """
    Add N-linked glycosylation sites to mask immunogenic epitopes.

    Scientific basis:
    - Glycan shielding is used in C2_Homodimer_A Env, C4_Tetramer_D HA engineering
    - Giles et al., J Virol 2018; Mary et al., Microorganisms 2022: AAV glycan engineering
    - Reduces neutralizing antibody binding while maintaining function
    """
    seq_list = list(sequence)
    modifications = []

    for epitope in epitopes:
        start, end, name = epitope
        sites_added = 0

        # Find positions within epitope that can accommodate N-X-S/T
        for i in range(start - 1, min(end - 2, len(seq_list) - 2)):
            if sites_added >= sites_per_epitope:
                break

            # Skip if already N or if position i+1 is P (blocks glycosylation)
            if seq_list[i] in 'NCP' or seq_list[i + 1] == 'P':
                continue

            # Check if we can create a sequon without disrupting critical residues
            if seq_list[i] not in 'WMC':
                original = seq_list[i]
                seq_list[i] = 'N'

                # Ensure position i+2 is S or T
                if seq_list[i + 2] not in 'ST':
                    orig_plus2 = seq_list[i + 2]
                    seq_list[i + 2] = 'S'
                    modifications.append({
                        "epitope": name,
                        "position": i + 1,
                        "sequon": f"N-{seq_list[i+1]}-S",
                        "original_residues": f"{original}...{orig_plus2}",
                        "rationale": f"Glycan shielding of {name}"
                    })
                else:
                    modifications.append({
                        "epitope": name,
                        "position": i + 1,
                        "sequon": f"N-{seq_list[i+1]}-{seq_list[i+2]}",
                        "original_residues": original,
                        "rationale": f"Glycan shielding of {name}"
                    })

                sites_added += 1

    return ''.join(seq_list), modifications


def apply_liver_detargeting(sequence: str, positions: List[int]) -> Tuple[str, List[Dict]]:
    """
    Modify residues involved in liver tropism to reduce hepatic uptake.

    Scientific basis:
    - Lisowski et al., Nature 2014: Identified liver-binding residues
    - Pulicherla et al., Mol Ther 2011: Galactose binding mutations
    """
    seq_list = list(sequence)
    mutations = []

    # Common liver-detargeting mutations
    # Replace positively charged residues that interact with heparan sulfate
    detargeting_map = {
        'R': 'A',  # Arginine to Alanine
        'K': 'A',  # Lysine to Alanine
    }

    for pos in positions:
        idx = pos - 1
        if 0 <= idx < len(seq_list) and seq_list[idx] in detargeting_map:
            original = seq_list[idx]
            seq_list[idx] = detargeting_map[original]
            mutations.append({
                "position": pos,
                "original": original,
                "mutated": detargeting_map[original],
                "rationale": "Liver detargeting (reduce HSPG binding)"
            })

    return ''.join(seq_list), mutations


def engineer_capsid(capsid_data: Dict,
                    apply_y2f: bool = True,
                    apply_glycan: bool = True,
                    apply_detargeting: bool = False) -> Dict:
    """
    Full capsid engineering pipeline.

    Modifications:
    1. Y-to-F mutations for improved transduction
    2. Glycan shielding for reduced immunogenicity
    3. Optional liver detargeting for muscle-specific applications
    """
    sequence = capsid_data["sequence"]
    all_mutations = []
    glycan_mods = []
    detarget_mods = []

    # Y-to-F mutations
    if apply_y2f and "tyrosine_positions" in capsid_data:
        sequence, all_mutations = apply_tyrosine_mutations(
            sequence,
            capsid_data["tyrosine_positions"]
        )

    # Glycan shielding
    if apply_glycan and "immunogenic_epitopes" in capsid_data:
        sequence, glycan_mods = add_glycan_shield(
            sequence,
            capsid_data["immunogenic_epitopes"],
            sites_per_epitope=1
        )

    # Liver detargeting (for muscle applications)
    if apply_detargeting and "liver_binding_residues" in capsid_data:
        sequence, detarget_mods = apply_liver_detargeting(
            sequence,
            capsid_data["liver_binding_residues"]
        )

    props = calculate_properties(sequence)

    # Map epitopes on engineered sequence
    epitope_map = map_antigenic_epitopes(
        sequence,
        capsid_data.get("immunogenic_epitopes", [])
    )

    return {
        "name": f"{capsid_data['name']} (Immune-Evasive)",
        "serotype": capsid_data["serotype"],
        "tropism": capsid_data["tropism"],
        "application": capsid_data["clinical_application"],
        "original_length": capsid_data["length"],
        "engineered_sequence": sequence,
        "y_to_f_mutations": all_mutations,
        "glycan_modifications": glycan_mods,
        "liver_detargeting": detarget_mods,
        "epitope_map": epitope_map,
        "disease_info": capsid_data.get("disease_info", {}),
        "properties": props
    }


def generate_fasta_header(data: Dict) -> str:
    """Generate FASTA file with defensive publication headers."""
    timestamp = datetime.now().isoformat()
    seq = data.get("engineered_sequence", "")
    sha256 = hashlib.sha256(seq.encode()).hexdigest()

    target system = data.get("disease_info", {})

    header = f"""; ==============================================================================
; OPEN GENE THERAPY CAPSID - IMMUNE-EVASIVE ENGINEERING
; ==============================================================================
;
; LICENSE: AGPL-3.0 (code) + OpenMTA + CC BY-SA 4.0 (sequences)
; PATENT DEDICATION: All methods and sequences PUBLIC DOMAIN for patent purposes
;
; NAME: {data.get('name', 'Unknown')}
; SEROTYPE: {data.get('serotype', 'Unknown')}
; TROPISM: {data.get('tropism', 'Unknown')}
; APPLICATION: {data.get('application', 'Gene therapy')}
;
; TARGET target system: {target system.get('name', 'N/A')}
; AFFECTED GENE: {target system.get('gene', 'N/A')}
; INCIDENCE: {target system.get('incidence', 'N/A')}
;
; ENGINEERING MODIFICATIONS:
; - Y-to-F mutations: {len(data.get('y_to_f_mutations', []))} sites (improved transduction)
; - Glycan shielding: {len(data.get('glycan_modifications', []))} sites (immune evasion)
; - Liver detargeting: {len(data.get('liver_detargeting', []))} mutations
;
; SCIENTIFIC BASIS:
; Y-to-F: Zhong et al., PNAS 2008; Markusic et al., Mol Ther 2010
; Glycan shielding: Giles et al., J Virol 2018; Mary et al., Microorganisms 2022
;
; PRIOR ART NOTICE:
; Publication Date: {timestamp}
; SHA-256: {sha256}
;
; This capsid sequence is published to PREVENT PATENT ENCLOSURE.
; Anyone can fabricate sequence, test, and use this sequence.
;
; ==============================================================================

"""
    return header


def save_capsid(data: Dict, output_dir: str, filename: str):
    """Save engineered capsid to FASTA file."""
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, f"{filename}.fasta")
    header_text = generate_fasta_header(data)
    seq = data["engineered_sequence"]

    target system = data.get("disease_info", {})
    fasta_header = f">{filename}|serotype={data['serotype']}|target system={target system.get('name', 'N/A')}|mw={data['properties']['mw_kda']}kDa|license=AGPL3+OpenMTA+CC-BY-SA-4.0"

    with open(filepath, 'w') as f:
        f.write(header_text)
        f.write(fasta_header + "\n")
        for i in range(0, len(seq), 70):
            f.write(seq[i:i+70] + "\n")

    return filepath


def main():
    """Main pipeline execution."""
    print("="*80)
    print("M4 GENETIC CAPSID ENGINEERING")
    print("Neuromuscular Gene Therapy Vector Optimization")
    print("="*80)
    print("""
TARGET DISEASES:
  1. Spinal Muscular Atrophy (SMA) - AAV9 vectors
  2. Duchenne Muscular Dystrophy (DMD) - AAVrh74 vectors
  3. Limb-girdle Muscular Dystrophies - AAV8 variants

ENGINEERING APPROACH:
  1. Map highly exposed antigenic epitopes
  2. Apply Y-to-F mutations (improved transduction)
  3. Add N-linked glycosylation (glycan shielding)
  4. Optional liver detargeting for muscle specificity

LICENSE: AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication
""")

    os.makedirs("genetic_capsids", exist_ok=True)
    all_results = []

    # =========================================================================
    # PROCESS ALL CAPSIDS
    # =========================================================================
    print("\n" + "="*80)
    print("ENGINEERING AAV CAPSIDS")
    print("="*80)

    for name, data in CAPSID_DATABASE.items():
        print(f"\n[{name.upper()}]")
        print("=" * 60)
        print(f"  Name: {data['name']}")
        print(f"  Serotype: {data['serotype']}")
        print(f"  Tropism: {data['tropism']}")
        print(f"  Application: {data['clinical_application']}")

        target system = data.get("disease_info", {})
        print(f"\n  Target target system: {target system.get('name', 'N/A')}")
        print(f"  Affected Gene: {target system.get('gene', 'N/A')}")
        print(f"  Incidence: {target system.get('incidence', 'N/A')}")

        # Apply liver detargeting only for muscle-specific vectors
        apply_detarget = "liver_binding_residues" in data

        result = engineer_capsid(
            data,
            apply_y2f=True,
            apply_glycan=True,
            apply_detargeting=apply_detarget
        )

        print(f"\n  ENGINEERING RESULTS:")
        print(f"  Y-to-F mutations: {len(result['y_to_f_mutations'])}")
        for mut in result['y_to_f_mutations'][:3]:
            print(f"    - Position {mut['position']}: Y -> F")
        if len(result['y_to_f_mutations']) > 3:
            print(f"    ... and {len(result['y_to_f_mutations']) - 3} more")

        print(f"  Glycan shield sites: {len(result['glycan_modifications'])}")
        for mod in result['glycan_modifications'][:3]:
            print(f"    - {mod['epitope']}: Position {mod['position']}, {mod['sequon']}")
        if len(result['glycan_modifications']) > 3:
            print(f"    ... and {len(result['glycan_modifications']) - 3} more")

        if result['liver_detargeting']:
            print(f"  Liver detargeting: {len(result['liver_detargeting'])} mutations")

        # Save
        filepath = save_capsid(result, "genetic_capsids", f"{name}_immune_evasive")
        print(f"\n  Saved: {filepath}")

        all_results.append({
            "name": name,
            "target system": target system.get('name', 'Unknown'),
            "data": result
        })

    # =========================================================================
    # SAVE SUMMARY
    # =========================================================================
    summary = {
        "timestamp": datetime.now().isoformat(),
        "pipeline": "m4_genetic_capsid_engineering",
        "license": "AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication",
        "capsids_engineered": len(all_results),
        "diseases_addressed": [
            "Spinal Muscular Atrophy (SMA)",
            "Duchenne Muscular Dystrophy (DMD)",
            "Limb-girdle Muscular Dystrophies"
        ],
        "engineering_methods": [
            "Y-to-F mutations (improved transduction)",
            "Glycan shielding (reduced immunogenicity)",
            "Liver detargeting (muscle specificity)"
        ],
        "results": all_results
    }

    summary_path = "genetic_capsids/engineering_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print("\n" + "="*80)
    print("PIPELINE COMPLETE")
    print("="*80)
    print(f"""
Capsids engineered: {len(all_results)}

DISEASES ADDRESSED:
  - Spinal Muscular Atrophy (SMA) - 1 in 10,000 births
  - Duchenne Muscular Dystrophy (DMD) - 1 in 3,500 male births
  - Limb-girdle Muscular Dystrophies - 1 in 14,500-45,000

CLINICAL IMPACT:
  These neuromuscular diseases affect thousands of children worldwide.
  Current gene therapies (Zolgensma, Elevidys) cost $1-3 million per dose.

  By publishing immune-evasive capsid designs as prior art, we:
  1. Prevent patent enclosure of these modifications
  2. Enable cheaper biosimilar development
  3. Allow academic researchers to build on this work

Output directory: genetic_capsids/
Summary: {summary_path}

PRIOR ART NOTICE:
  All capsid sequences published under defensive license.
  Cannot be patented. Free for all to use and develop.
""")


if __name__ == "__main__":
    main()
