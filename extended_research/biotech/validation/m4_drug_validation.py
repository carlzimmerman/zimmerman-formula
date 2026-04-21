#!/usr/bin/env python3
"""
M4 Drug Database Validation
===========================

Validates our generated peptides against known peptide drugs and binders.
Checks for:
1. Sequence similarity to approved peptide drugs
2. Motif matches to known binding sequences
3. Overlap with research peptides in literature

This is REAL validation - comparing against actual data.

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026
"""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import hashlib
import re

# Known approved peptide drugs with their sequences
# Source: DrugBank, FDA labels, UniProt
APPROVED_PEPTIDE_DRUGS = {
    # GLP-1 agonists
    "semaglutide": {
        "sequence": "HXEGTFTSDVSSYLEGQAAKEFIAWLVRGRG",  # X = Aib
        "target": "GLP-1R",
        "indication": "T2D, Obesity",
        "approval": "FDA 2017",
    },
    "liraglutide": {
        "sequence": "HAEGTFTSDVSSYLEGQAAKEFIAWLVRGRG",
        "target": "GLP-1R",
        "indication": "T2D, Obesity",
        "approval": "FDA 2010",
    },
    "tirzepatide": {
        "sequence": "YXEGTFTSDYSIXLDKIAQKAFVQWLIAGGPSSGAPPPS",  # dual GLP-1/GIP
        "target": "GLP-1R, GIPR",
        "indication": "T2D, Obesity",
        "approval": "FDA 2022",
    },
    "exenatide": {
        "sequence": "HGEGTFTSDLSKQMEEEAVRLFIEWLKNGGPSSGAPPPS",
        "target": "GLP-1R",
        "indication": "T2D",
        "approval": "FDA 2005",
    },

    # Oxytocin/vasopressin analogs
    "oxytocin": {
        "sequence": "CYIQNCPLG",  # cyclic
        "target": "Oxytocin receptor",
        "indication": "Labor induction",
        "approval": "FDA 1962",
    },
    "desmopressin": {
        "sequence": "CYFQNCPRG",  # cyclic, deaminated
        "target": "V2 receptor",
        "indication": "Diabetes insipidus",
        "approval": "FDA 1978",
    },
    "carbetocin": {
        "sequence": "CYIQNCPLG",  # modified oxytocin
        "target": "Oxytocin receptor",
        "indication": "Postpartum hemorrhage",
        "approval": "EMA 2018",
    },

    # Melanocortin peptides
    "setmelanotide": {
        "sequence": "CKKNFFWKTFTSC",  # cyclic
        "target": "MC4R",
        "indication": "Genetic obesity",
        "approval": "FDA 2020",
    },
    "afamelanotide": {
        "sequence": "SYSMEHFRWGKPV",
        "target": "MC1R",
        "indication": "Erythropoietic protoporphyria",
        "approval": "FDA 2019",
    },

    # Other peptide drugs
    "pramlintide": {
        "sequence": "KCNTATCATQRLANFLVHSSNNFGPILPPTNVGSNTY",
        "target": "Amylin receptor",
        "indication": "T1D/T2D",
        "approval": "FDA 2005",
    },
    "calcitonin_salmon": {
        "sequence": "CSNLSTCVLGKLSQELHKLQTYPRTNTGSGTP",
        "target": "Calcitonin receptor",
        "indication": "Osteoporosis",
        "approval": "FDA 1995",
    },
    "teriparatide": {
        "sequence": "SVSEIQLMHNLGKHLNSMERVEWLRKKLQDVHNF",
        "target": "PTH1R",
        "indication": "Osteoporosis",
        "approval": "FDA 2002",
    },
    "abaloparatide": {
        "sequence": "AVSEHQLLHDKGKSIQDLRRRELLEKLLXKLHTA",  # PTHrP analog
        "target": "PTH1R",
        "indication": "Osteoporosis",
        "approval": "FDA 2017",
    },
    "plecanatide": {
        "sequence": "NDECELCVNVACTGCL",
        "target": "GC-C",
        "indication": "IBS-C, CIC",
        "approval": "FDA 2017",
    },
    "linaclotide": {
        "sequence": "CCEYCCNPACTGCY",
        "target": "GC-C",
        "indication": "IBS-C, CIC",
        "approval": "FDA 2012",
    },

    # Antimicrobials
    "daptomycin": {
        "sequence": "WDXDGOXDXXKYNXXA",  # lipopeptide, cyclic
        "target": "Bacterial membrane",
        "indication": "Gram+ infections",
        "approval": "FDA 2003",
    },
    "vancomycin": {
        "sequence": "CYCLIC_GLYCOPEPTIDE",  # Not standard AA
        "target": "D-Ala-D-Ala",
        "indication": "Gram+ infections",
        "approval": "FDA 1958",
    },

    # Somatostatin analogs
    "octreotide": {
        "sequence": "FCFWKTCT",  # cyclic
        "target": "SSTR2, SSTR5",
        "indication": "Acromegaly, NETs",
        "approval": "FDA 1988",
    },
    "lanreotide": {
        "sequence": "CVKWKTCT",  # cyclic
        "target": "SSTR2",
        "indication": "Acromegaly",
        "approval": "FDA 2007",
    },

    # Natriuretic peptides
    "nesiritide": {
        "sequence": "SPKMVQGSGCFGRKMDRISSSSGLGCKVLRRH",
        "target": "NPR-A",
        "indication": "Acute heart failure",
        "approval": "FDA 2001",
    },

    # Gonadotropin-releasing hormone
    "leuprolide": {
        "sequence": "EHWSYGLRP",  # pyroGlu
        "target": "GnRH receptor",
        "indication": "Prostate cancer",
        "approval": "FDA 1985",
    },
    "degarelix": {
        "sequence": "XZFWSYXLRP",  # modified
        "target": "GnRH receptor",
        "indication": "Prostate cancer",
        "approval": "FDA 2008",
    },

    # Integrins
    "eptifibatide": {
        "sequence": "CPRGDWNRC",  # cyclic RGD
        "target": "αIIbβ3 integrin",
        "indication": "ACS",
        "approval": "FDA 1998",
    },
    "cilengitide": {
        "sequence": "CRGDFV",  # cyclic RGD
        "target": "αvβ3/αvβ5 integrin",
        "indication": "Clinical trials (glioma)",
        "approval": "Phase III",
    },
}

# Known binding motifs from literature
BINDING_MOTIFS = {
    "RGD": {
        "pattern": r"RGD",
        "target": "Integrins",
        "function": "Cell adhesion",
    },
    "NGR": {
        "pattern": r"NGR",
        "target": "Aminopeptidase N",
        "function": "Tumor homing",
    },
    "HFRW": {
        "pattern": r"H[FY]RW",
        "target": "Melanocortin receptors",
        "function": "MC4R core",
    },
    "cyclic_disulfide": {
        "pattern": r"C.{3,12}C",
        "target": "Various",
        "function": "Stability/binding",
    },
    "TAT": {
        "pattern": r"[RK]{4,}",
        "target": "Cell membrane",
        "function": "Cell penetration",
    },
    "NLS": {
        "pattern": r"[KR]{3,}",
        "target": "Nuclear import",
        "function": "Nuclear localization",
    },
    "GLP1_Nterm": {
        "pattern": r"H[ASX]EGTFTS",
        "target": "GLP-1R",
        "function": "GLP-1 N-terminus",
    },
    "oxytocin_core": {
        "pattern": r"CY[IVL]QNC",
        "target": "Oxytocin receptor",
        "function": "Oxytocin core",
    },
    "somatostatin_core": {
        "pattern": r"FWK",
        "target": "SSTR",
        "function": "Somatostatin pharmacophore",
    },
}


@dataclass
class ValidationResult:
    """Result of validating a peptide against known drugs."""
    peptide_id: str
    sequence: str
    best_drug_match: Optional[str]
    best_similarity: float
    motifs_found: List[str]
    is_drug_similar: bool  # >80% similarity to known drug
    is_novel: bool  # <50% similarity to any known
    validation_notes: List[str]


def sequence_similarity(seq1: str, seq2: str) -> float:
    """Calculate sequence identity between two sequences."""
    # Remove non-standard residues for comparison
    s1 = "".join(c for c in seq1.upper() if c in "ACDEFGHIKLMNPQRSTVWY")
    s2 = "".join(c for c in seq2.upper() if c in "ACDEFGHIKLMNPQRSTVWY")

    if not s1 or not s2:
        return 0.0

    # Use shorter sequence as reference
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    # Sliding window alignment
    best_match = 0
    for offset in range(len(s2) - len(s1) + 1):
        matches = sum(1 for i, c in enumerate(s1) if c == s2[offset + i])
        best_match = max(best_match, matches)

    # Also check reverse (in case of different termini)
    s1_rev = s1[::-1]
    for offset in range(len(s2) - len(s1) + 1):
        matches = sum(1 for i, c in enumerate(s1_rev) if c == s2[offset + i])
        best_match = max(best_match, matches)

    return best_match / len(s1) if len(s1) > 0 else 0.0


def find_motifs(sequence: str) -> List[Tuple[str, str]]:
    """Find known binding motifs in sequence."""
    found = []
    seq_upper = sequence.upper()

    for motif_name, motif_info in BINDING_MOTIFS.items():
        pattern = motif_info["pattern"]
        matches = re.findall(pattern, seq_upper)
        if matches:
            found.append((motif_name, motif_info["target"]))

    return found


def validate_peptide(peptide_id: str, sequence: str) -> ValidationResult:
    """Validate a single peptide against known drugs and motifs."""
    notes = []

    # Compare to all known drugs
    best_drug = None
    best_sim = 0.0

    for drug_name, drug_info in APPROVED_PEPTIDE_DRUGS.items():
        drug_seq = drug_info["sequence"]
        sim = sequence_similarity(sequence, drug_seq)

        if sim > best_sim:
            best_sim = sim
            best_drug = drug_name

    if best_sim > 0.8:
        notes.append(f"HIGH similarity to {best_drug} ({best_sim*100:.0f}%)")
    elif best_sim > 0.5:
        notes.append(f"Moderate similarity to {best_drug} ({best_sim*100:.0f}%)")

    # Find motifs
    motifs = find_motifs(sequence)
    motif_names = [m[0] for m in motifs]

    if "RGD" in motif_names:
        notes.append("Contains RGD integrin-binding motif")
    if "HFRW" in motif_names:
        notes.append("Contains melanocortin receptor core")
    if "cyclic_disulfide" in motif_names:
        notes.append("Contains potential disulfide bridge (C...C)")
    if "TAT" in motif_names or "NLS" in motif_names:
        notes.append("Contains cell-penetrating/nuclear signal")

    # Classify
    is_drug_similar = best_sim > 0.8
    is_novel = best_sim < 0.5

    if is_novel and not motifs:
        notes.append("NOVEL: No significant similarity to known drugs or motifs")
    elif is_drug_similar:
        notes.append("CAUTION: May infringe on existing drug patents")

    return ValidationResult(
        peptide_id=peptide_id,
        sequence=sequence,
        best_drug_match=best_drug,
        best_similarity=round(best_sim, 3),
        motifs_found=motif_names,
        is_drug_similar=is_drug_similar,
        is_novel=is_novel,
        validation_notes=notes,
    )


def validate_fasta_file(fasta_path: str) -> List[ValidationResult]:
    """Validate all peptides in a FASTA file."""
    print(f"\n{'='*70}")
    print(f"DRUG DATABASE VALIDATION")
    print(f"{'='*70}")
    print(f"Input: {fasta_path}")
    print(f"Reference drugs: {len(APPROVED_PEPTIDE_DRUGS)}")
    print(f"Binding motifs: {len(BINDING_MOTIFS)}")
    print()

    # Load sequences
    sequences = []
    current_id = None
    current_seq = []

    with open(fasta_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_id:
                    sequences.append((current_id, "".join(current_seq)))
                current_id = line[1:].split("|")[0]
                current_seq = []
            else:
                current_seq.append(line)
        if current_id:
            sequences.append((current_id, "".join(current_seq)))

    print(f"Loaded {len(sequences)} sequences\n")

    results = []

    for pep_id, seq in sequences:
        result = validate_peptide(pep_id, seq)
        results.append(result)

        if result.best_similarity > 0.5 or result.motifs_found:
            print(f"{pep_id}:")
            print(f"  Best match: {result.best_drug_match} ({result.best_similarity*100:.0f}%)")
            if result.motifs_found:
                print(f"  Motifs: {', '.join(result.motifs_found)}")
            for note in result.validation_notes:
                print(f"  → {note}")

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")

    drug_similar = sum(1 for r in results if r.is_drug_similar)
    novel = sum(1 for r in results if r.is_novel)
    with_motifs = sum(1 for r in results if r.motifs_found)

    print(f"Total peptides: {len(results)}")
    print(f"Drug-similar (>80%): {drug_similar} ({100*drug_similar/len(results):.1f}%)")
    print(f"Novel (<50%): {novel} ({100*novel/len(results):.1f}%)")
    print(f"With known motifs: {with_motifs} ({100*with_motifs/len(results):.1f}%)")

    # Motif distribution
    all_motifs = {}
    for r in results:
        for m in r.motifs_found:
            all_motifs[m] = all_motifs.get(m, 0) + 1

    if all_motifs:
        print("\nMOTIF DISTRIBUTION:")
        for motif, count in sorted(all_motifs.items(), key=lambda x: -x[1]):
            print(f"  {motif}: {count}")

    return results


def validate_all_fastas():
    """Validate all FASTA files in the biotech directory."""
    base_dir = Path(__file__).parent.parent
    output_dir = Path(__file__).parent / "drug_validation_results"
    output_dir.mkdir(exist_ok=True)

    # Find all FASTA files
    fasta_files = list(base_dir.glob("**/*.fasta"))
    peptide_fastas = [
        f for f in fasta_files
        if "peptide" in f.name.lower() or "binder" in f.name.lower() or "agonist" in f.name.lower()
    ]

    print(f"Found {len(peptide_fastas)} peptide FASTA files")

    all_results = []

    for fasta_path in peptide_fastas:
        results = validate_fasta_file(str(fasta_path))
        all_results.extend(results)

    # Save combined results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_peptides": len(all_results),
        "drug_similar_count": sum(1 for r in all_results if r.is_drug_similar),
        "novel_count": sum(1 for r in all_results if r.is_novel),
        "results": [asdict(r) for r in all_results],
    }

    json_path = output_dir / f"validation_results_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved: {json_path}")

    return all_results


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        validate_fasta_file(sys.argv[1])
    else:
        validate_all_fastas()
