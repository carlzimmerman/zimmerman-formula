#!/usr/bin/env python3
"""
Z² target system Protein Folding

Apply Z² protein folder to target system-associated proteins:
- Tau (Alzheimer's, frontotemporal dementia)
- Amyloid-β (Alzheimer's)
- α-Synuclein (Parkinson's)
- Huntingtin (Huntington's target system)
- Prion protein (CJD, mad cow)
- SOD1 (ALS)
- TDP-43 (ALS, FTD)

Copyright (C) 2026 Carl Zimmerman
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import numpy as np
from typing import Dict, List
import json
from pathlib import Path
from z2_protein_folder_BEST import Z2ProteinFolderBest

# =============================================================================
# target system PROTEINS
# =============================================================================

DISEASE_PROTEINS = {
    # ---------------------------------------------------------------------
    # ALZHEIMER'S target system
    # ---------------------------------------------------------------------
    "abeta40": {
        "name": "Amyloid-β 1-40",
        "target system": "Alzheimer's target system",
        "role": "Forms amyloid plaques",
        "sequence": "DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVV",
        "notes": "Shorter form, less toxic than Aβ42",
    },
    "abeta42": {
        "name": "Amyloid-β 1-42",
        "target system": "Alzheimer's target system",
        "role": "Primary component of plaques, more aggregation-prone",
        "sequence": "DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVVIA",
        "notes": "Additional Ile-Ala makes it more hydrophobic and aggregation-prone",
    },
    "tau_repeat1": {
        "name": "Tau microtubule binding repeat 1",
        "target system": "Alzheimer's, Tauopathies",
        "role": "Core of tau tangles",
        "sequence": "VQIINKKLDLSNVQSKCGSKDNIKHVPGGGS",
        "notes": "One of 4 repeats that binds microtubules and forms PHF",
    },
    "tau_phf_core": {
        "name": "Tau PHF core (306-378)",
        "target system": "Alzheimer's",
        "role": "Paired helical filament core",
        "sequence": "VQIVYKPVDLSKVTSKCGSLGNIHHKPGGGQVEVKSEKLDFKDRVQSKIGSLDNITHVPGGGNKKIETHKLTFRENAKAKTDHGAEIV",
        "notes": "Core region that forms the cross-β structure in tangles",
    },

    # ---------------------------------------------------------------------
    # PARKINSON'S target system
    # ---------------------------------------------------------------------
    "alpha_synuclein": {
        "name": "α-Synuclein (full)",
        "target system": "Parkinson's target system",
        "role": "Forms Lewy bodies",
        "sequence": "MDVFMKGLSKAKEGVVAAAEKTKQGVAEAAGKTKEGVLYVGSKTKEGVVHGVATVAEKTKEQVTNVGGAVVTGVTAVAQKTVEGAGSIAAATGFVKKDQLGKNEEGAPQEGILEDMPVDPDNEAYEMPSEEGYQDYEPEA",
        "notes": "N-terminal forms helix when bound to membranes",
    },
    "alpha_syn_nac": {
        "name": "α-Synuclein NAC region (61-95)",
        "target system": "Parkinson's target system",
        "role": "Non-Amyloid-β Component, aggregation core",
        "sequence": "EQVTNVGGAVVTGVTAVAQKTVEGAGSIAAATGFV",
        "notes": "Highly hydrophobic, essential for aggregation",
    },

    # ---------------------------------------------------------------------
    # HUNTINGTON'S target system
    # ---------------------------------------------------------------------
    "huntingtin_polyQ": {
        "name": "Huntingtin exon 1 with polyQ",
        "target system": "Huntington's target system",
        "role": "Forms aggregates when Q repeat > 36",
        "sequence": "MATLEKLMKAFESLKSFQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQPPPPPPPPPPPQLPQPPPQAQPLLPQPQPPPPPPPPPPGPAVAEEPLHRP",
        "notes": "36 Q repeats shown (HD threshold ~36-40)",
    },
    "huntingtin_17": {
        "name": "Huntingtin N17 domain",
        "target system": "Huntington's target system",
        "role": "Targets Htt to membrane, affects toxicity",
        "sequence": "MATLEKLMKAFESLKSFQ",
        "notes": "Amphipathic helix, membrane association",
    },

    # ---------------------------------------------------------------------
    # PRION DISEASES
    # ---------------------------------------------------------------------
    "prion_121_231": {
        "name": "Prion protein structured domain",
        "target system": "CJD, Fatal insomnia, Mad cow",
        "role": "Misfolding creates PrPSc infectious form",
        "sequence": "HGGGWGQPHGGGWGQPHGGGWGQPHGGGWGQPHGGGWGQGGGTHSQWNKPSKPKTNMKHMAGAAAAGAVVGGLGGYMLGSAMSRPIIHFGSDYEDRYYRENMHRYPNQVYYRPMDEYSNQNNFVHDCVNITIKQHTVTTTTKGENFTETDVKMMERVVEQMCITQYERESQAYYQRGSSMVLFSSPPVILLISFLIFLIVG",
        "notes": "Octapeptide repeats + globular domain + GPI anchor",
    },
    "prion_helix2_3": {
        "name": "Prion helices 2-3",
        "target system": "Prion diseases",
        "role": "Core folded region that misfolds",
        "sequence": "HRYPNQVYYRPMDEYSNQNNFVHDCVNITIKQHTVTTTTKGENFTETDVKMMERVVEQMCITQYER",
        "notes": "Contains S-S bond Cys179-Cys214",
    },

    # ---------------------------------------------------------------------
    # ALS
    # ---------------------------------------------------------------------
    "sod1": {
        "name": "Superoxide dismutase 1 (partial)",
        "target system": "ALS (familial)",
        "role": "Misfolding causes motor neuron death",
        "sequence": "ATKAVCVLKGDGPVQGIINFEQKESNGPVKVWGSIKGLTEGLHGFHVHEFGDNTAGCTSAGPHFNPLSRKHGGPKDEERHVGDLGNVTADKDGVADVSIEDSVISLSGDHCIIGRTLVVHEKADDLGKGGNEESTKTGNAGSRLACGVIGIAQ",
        "notes": "Cu/Zn binding, ~170 known mutations cause ALS",
    },
    "tdp43_lcd": {
        "name": "TDP-43 low complexity domain",
        "target system": "ALS, FTD",
        "role": "Aggregates in cytoplasmic inclusions",
        "sequence": "GFGFVRFTEYETQVKVMSQRHMIDGRWCDCKLPNSKQSQDEPLRSRKVFVGRCTEDMTEDELREFFSQYGDVMDVFIPKPFRAFAFVTFADDQIAQSLCGEDLIIKGISVHISNAEPKHNSNRQLERSGRFGGNSSSS",
        "notes": "Glycine-rich, intrinsically disordered, prion-like",
    },

    # ---------------------------------------------------------------------
    # OTHER NEURODEGENERATIVE
    # ---------------------------------------------------------------------
    "fus_lcd": {
        "name": "FUS low complexity domain",
        "target system": "ALS, FTD",
        "role": "LLPS and aggregation",
        "sequence": "MASNDYTQQATQSYGAYPTQPGQGYSQQSSQPYGQQSYSGYSQSTDTSGYGQSSYSSYGQSQNTGYGTQSTPQGYGSTGGYGSSQSSQSSYGQQSSYPGYGQQPAPSSTSGSYGSSSQSSSYGQPQSGSYSQQPSYGGQQQSYGQQQSYNPPQGYGQQNQYNS",
        "notes": "QGSY-rich, forms hydrogels and aggregates",
    },
}


def analyze_disease_proteins():
    """Fold and analyze all target system proteins."""
    print("=" * 78)
    print("Z² target system PROTEIN FOLDING")
    print("=" * 78)

    folder = Z2ProteinFolderBest()
    results = {}

    for protein_id, data in DISEASE_PROTEINS.items():
        print(f"\n{'='*78}")
        print(f"{data['name']}")
        print(f"target system: {data['target system']}")
        print(f"{'='*78}")

        result = folder.fold(data['sequence'], protein_id)
        ss = result['secondary_structure']

        # Calculate composition
        h_count = ss.count('H')
        e_count = ss.count('E')
        c_count = ss.count('C')
        total = len(ss)

        h_frac = 100 * h_count / total
        e_frac = 100 * e_count / total
        c_frac = 100 * c_count / total

        print(f"\nSequence ({total} aa):")
        # Print in blocks of 50
        for i in range(0, total, 50):
            seq_block = data['sequence'][i:i+50]
            ss_block = ss[i:i+50]
            print(f"  {i+1:4d}: {seq_block}")
            print(f"        {ss_block}")

        print(f"\nSecondary Structure Composition:")
        print(f"  α-helix: {h_count:3d} ({h_frac:5.1f}%)")
        print(f"  β-sheet: {e_count:3d} ({e_frac:5.1f}%)")
        print(f"  Coil:    {c_count:3d} ({c_frac:5.1f}%)")

        # Identify structural features
        print(f"\nStructural Features:")

        # Find helices
        helix_regions = []
        i = 0
        while i < total:
            if ss[i] == 'H':
                start = i
                while i < total and ss[i] == 'H':
                    i += 1
                helix_regions.append((start+1, i, i-start))
            else:
                i += 1

        if helix_regions:
            print(f"  α-helices: ", end="")
            print(", ".join([f"{s}-{e} ({l}aa)" for s, e, l in helix_regions[:5]]))
            if len(helix_regions) > 5:
                print(f"              ... and {len(helix_regions)-5} more")

        # Find sheets
        sheet_regions = []
        i = 0
        while i < total:
            if ss[i] == 'E':
                start = i
                while i < total and ss[i] == 'E':
                    i += 1
                sheet_regions.append((start+1, i, i-start))
            else:
                i += 1

        if sheet_regions:
            print(f"  β-strands: ", end="")
            print(", ".join([f"{s}-{e} ({l}aa)" for s, e, l in sheet_regions[:5]]))
            if len(sheet_regions) > 5:
                print(f"              ... and {len(sheet_regions)-5} more")

        # Store results
        results[protein_id] = {
            'name': data['name'],
            'target system': data['target system'],
            'length': total,
            'secondary_structure': ss,
            'composition': {
                'helix': h_frac,
                'sheet': e_frac,
                'coil': c_frac,
            },
            'helix_regions': helix_regions,
            'sheet_regions': sheet_regions,
        }

    # Summary statistics
    print(f"\n{'='*78}")
    print("SUMMARY: target system PROTEIN STRUCTURAL PREDICTIONS")
    print("=" * 78)

    print("\n{:<25} {:>6} {:>8} {:>8} {:>8}".format(
        "Protein", "Length", "Helix%", "Sheet%", "Coil%"))
    print("-" * 60)

    for pid, r in results.items():
        print("{:<25} {:>6} {:>8.1f} {:>8.1f} {:>8.1f}".format(
            r['name'][:25], r['length'],
            r['composition']['helix'],
            r['composition']['sheet'],
            r['composition']['coil']))

    # Save results
    output_path = Path(__file__).parent / "z2_disease_folding_results.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_path}")

    return results


def compare_aggregation_prone_regions():
    """Analyze regions prone to aggregation across diseases."""
    print("\n" + "=" * 78)
    print("AGGREGATION-PRONE REGION ANALYSIS")
    print("=" * 78)

    folder = Z2ProteinFolderBest()

    # Key aggregation-prone sequences
    aggregation_sequences = {
        "Abeta_KLVFF": ("KLVFFAEDVGSNK", "Aβ fibril core motif"),
        "Abeta_GAIIGL": ("GAIIGLMVGGVV", "Aβ C-terminal β-sheet"),
        "Tau_PHF6": ("VQIVYK", "Tau aggregation nucleation"),
        "Tau_PHF6star": ("VQIINK", "Tau alternative nucleation"),
        "aSyn_NAC_core": ("GAVVTGVTAVAQK", "α-Syn NAC hydrophobic core"),
        "Prion_106_126": ("KTNMKHMAGAAAAGAVVGGLG", "Prion neurotoxic peptide"),
        "PolyQ_stretch": ("QQQQQQQQQQQQQQQQ", "Huntingtin polyQ"),
    }

    print("\nKey aggregation motifs and predicted structure:")
    print("-" * 60)

    for name, (seq, desc) in aggregation_sequences.items():
        result = folder.fold(seq, name)
        ss = result['secondary_structure']
        print(f"\n{name}: {desc}")
        print(f"  Sequence:  {seq}")
        print(f"  Structure: {ss}")

        # Interpret
        h_frac = 100 * ss.count('H') / len(ss)
        e_frac = 100 * ss.count('E') / len(ss)

        if e_frac > 50:
            print(f"  → Predicted β-strand ({e_frac:.0f}% sheet) - HIGH AGGREGATION POTENTIAL")
        elif h_frac > 50:
            print(f"  → Predicted α-helix ({h_frac:.0f}% helix) - may unfold during aggregation")
        else:
            print(f"  → Mostly disordered - may adopt β upon aggregation")


if __name__ == "__main__":
    results = analyze_disease_proteins()
    compare_aggregation_prone_regions()
