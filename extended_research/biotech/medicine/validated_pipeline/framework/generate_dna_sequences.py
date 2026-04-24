#!/usr/bin/env python3
"""
generate_dna_sequences.py - DNA Sequence Generator for Z² Lead Peptides

Generates codon-optimized DNA sequences for peptide synthesis.
Supports E. coli and Human (mammalian) codon optimization.

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


# =============================================================================
# CODON TABLES
# =============================================================================

# E. coli optimized codons (high expression)
ECOLI_CODONS = {
    'A': 'GCG',  # Ala - most common in E. coli
    'R': 'CGT',  # Arg
    'N': 'AAC',  # Asn
    'D': 'GAT',  # Asp
    'C': 'TGC',  # Cys
    'Q': 'CAG',  # Gln
    'E': 'GAA',  # Glu
    'G': 'GGT',  # Gly
    'H': 'CAC',  # His
    'I': 'ATC',  # Ile
    'L': 'CTG',  # Leu
    'K': 'AAA',  # Lys
    'M': 'ATG',  # Met (start)
    'F': 'TTC',  # Phe
    'P': 'CCG',  # Pro
    'S': 'AGC',  # Ser
    'T': 'ACC',  # Thr
    'W': 'TGG',  # Trp (only codon)
    'Y': 'TAC',  # Tyr
    'V': 'GTG',  # Val
    '*': 'TAA',  # Stop
}

# Human/Mammalian optimized codons
HUMAN_CODONS = {
    'A': 'GCC',  # Ala
    'R': 'AGG',  # Arg
    'N': 'AAC',  # Asn
    'D': 'GAC',  # Asp
    'C': 'TGC',  # Cys
    'Q': 'CAG',  # Gln
    'E': 'GAG',  # Glu
    'G': 'GGC',  # Gly
    'H': 'CAC',  # His
    'I': 'ATC',  # Ile
    'L': 'CTG',  # Leu
    'K': 'AAG',  # Lys
    'M': 'ATG',  # Met (start)
    'F': 'TTC',  # Phe
    'P': 'CCC',  # Pro
    'S': 'AGC',  # Ser
    'T': 'ACC',  # Thr
    'W': 'TGG',  # Trp (only codon)
    'Y': 'TAC',  # Tyr
    'V': 'GTG',  # Val
    '*': 'TGA',  # Stop (preferred in humans)
}

# Standard genetic code (for reverse translation verification)
GENETIC_CODE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}


# =============================================================================
# SEQUENCE GENERATION
# =============================================================================

def peptide_to_dna(peptide: str, codon_table: Dict[str, str]) -> str:
    """Convert peptide sequence to codon-optimized DNA."""
    dna = ""
    for aa in peptide.upper():
        if aa in codon_table:
            dna += codon_table[aa]
        else:
            raise ValueError(f"Unknown amino acid: {aa}")
    return dna


def dna_to_peptide(dna: str) -> str:
    """Translate DNA back to peptide (verification)."""
    peptide = ""
    for i in range(0, len(dna) - 2, 3):
        codon = dna[i:i+3].upper()
        if codon in GENETIC_CODE:
            aa = GENETIC_CODE[codon]
            if aa == '*':
                break
            peptide += aa
        else:
            raise ValueError(f"Unknown codon: {codon}")
    return peptide


def reverse_complement(dna: str) -> str:
    """Generate reverse complement of DNA sequence."""
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join(complement[base] for base in reversed(dna.upper()))


def gc_content(dna: str) -> float:
    """Calculate GC content percentage."""
    gc = sum(1 for base in dna.upper() if base in 'GC')
    return 100 * gc / len(dna) if dna else 0


def check_restriction_sites(dna: str) -> List[str]:
    """Check for common restriction enzyme sites that may interfere."""
    sites = {
        'EcoRI': 'GAATTC',
        'BamHI': 'GGATCC',
        'HindIII': 'AAGCTT',
        'XhoI': 'CTCGAG',
        'NdeI': 'CATATG',
        'NcoI': 'CCATGG',
        'XbaI': 'TCTAGA',
        'SalI': 'GTCGAC',
    }
    found = []
    for name, site in sites.items():
        if site in dna.upper():
            found.append(name)
    return found


# =============================================================================
# LEAD PEPTIDES
# =============================================================================

Z2_LEADS = [
    {
        'id': 'Z2-OPT-001',
        'target': 'Oxytocin Receptor (OXTR)',
        'disease': 'Social/Anxiety Disorders',
        'sequence': 'QLNWKWQKLKA',
        'mechanism': 'Dual Trp Clamp on TRP203/TRP99',
        'predicted_kd': '200 nM',
        'z2_alignment': 0.932,
    },
    {
        'id': 'Z2-OPT-006',
        'target': 'HIV Protease',
        'disease': 'HIV/AIDS',
        'sequence': 'LEWTYEWTLTE',
        'mechanism': 'Dual Trp Clamp on PHE53/ILE50',
        'predicted_kd': '200 nM',
        'z2_alignment': 0.967,
    },
    {
        'id': 'PHF6-Z2-001',
        'target': 'Tau PHF6 Fibril',
        'disease': "Alzheimer's Disease",
        'sequence': 'WVIEYW',
        'mechanism': 'Aromatic Cap + Charge Disruption (ARG349/LYS)',
        'predicted_kd': '100 nM',
        'z2_alignment': 0.957,
    },
]


# =============================================================================
# MAIN GENERATION
# =============================================================================

def generate_synthesis_orders():
    """Generate DNA sequences for all Z² leads."""

    print("=" * 80)
    print("Z² LEAD PEPTIDES - DNA SEQUENCE GENERATION FOR SYNTHESIS")
    print("=" * 80)
    print(f"    Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"    Z² Biological Constant: 6.015152508891966 Å")
    print()

    results = []

    for lead in Z2_LEADS:
        peptide = lead['sequence']

        # Generate DNA for both expression systems
        dna_ecoli = peptide_to_dna(peptide, ECOLI_CODONS)
        dna_human = peptide_to_dna(peptide, HUMAN_CODONS)

        # Verify translation
        verify_ecoli = dna_to_peptide(dna_ecoli)
        verify_human = dna_to_peptide(dna_human)

        assert verify_ecoli == peptide, f"E. coli translation mismatch: {verify_ecoli} != {peptide}"
        assert verify_human == peptide, f"Human translation mismatch: {verify_human} != {peptide}"

        # Calculate properties
        gc_ecoli = gc_content(dna_ecoli)
        gc_human = gc_content(dna_human)

        # Check restriction sites
        sites_ecoli = check_restriction_sites(dna_ecoli)
        sites_human = check_restriction_sites(dna_human)

        # Store results
        result = {
            'lead_id': lead['id'],
            'target': lead['target'],
            'disease': lead['disease'],
            'peptide_sequence': peptide,
            'peptide_length': len(peptide),
            'mechanism': lead['mechanism'],
            'predicted_kd': lead['predicted_kd'],
            'z2_alignment': lead['z2_alignment'],
            'dna_ecoli': dna_ecoli,
            'dna_human': dna_human,
            'dna_length': len(dna_ecoli),
            'gc_content_ecoli': gc_ecoli,
            'gc_content_human': gc_human,
            'restriction_sites_ecoli': sites_ecoli,
            'restriction_sites_human': sites_human,
            'reverse_complement_ecoli': reverse_complement(dna_ecoli),
            'reverse_complement_human': reverse_complement(dna_human),
        }
        results.append(result)

        # Print details
        print("-" * 80)
        print(f"  LEAD: {lead['id']}")
        print("-" * 80)
        print(f"    Target: {lead['target']}")
        print(f"    Disease: {lead['disease']}")
        print(f"    Mechanism: {lead['mechanism']}")
        print(f"    Z² Alignment: {lead['z2_alignment']:.3f}")
        print(f"    Predicted Kd: {lead['predicted_kd']}")
        print()
        print(f"    PEPTIDE SEQUENCE ({len(peptide)} aa):")
        print(f"    {peptide}")
        print()
        print(f"    DNA SEQUENCE - E. coli Optimized ({len(dna_ecoli)} bp):")
        print(f"    5'-{dna_ecoli}-3'")
        print(f"    GC Content: {gc_ecoli:.1f}%")
        if sites_ecoli:
            print(f"    ⚠ Contains restriction sites: {', '.join(sites_ecoli)}")
        print()
        print(f"    DNA SEQUENCE - Human/Mammalian Optimized ({len(dna_human)} bp):")
        print(f"    5'-{dna_human}-3'")
        print(f"    GC Content: {gc_human:.1f}%")
        if sites_human:
            print(f"    ⚠ Contains restriction sites: {', '.join(sites_human)}")
        print()

    # IDT Order Format
    print("=" * 80)
    print("IDT (Integrated DNA Technologies) ORDER FORMAT")
    print("=" * 80)
    print()
    print("Copy the following for direct ordering:")
    print()
    print("─" * 40)
    print("OPTION A: E. coli Expression")
    print("─" * 40)
    for r in results:
        print(f">{r['lead_id']}_Ecoli")
        print(f"{r['dna_ecoli']}")
    print()
    print("─" * 40)
    print("OPTION B: Mammalian Expression")
    print("─" * 40)
    for r in results:
        print(f">{r['lead_id']}_Human")
        print(f"{r['dna_human']}")
    print()

    # FASTA format for bioinformatics
    print("=" * 80)
    print("FASTA FORMAT (for bioinformatics pipelines)")
    print("=" * 80)
    print()
    for r in results:
        print(f">{r['lead_id']}|{r['target'].replace(' ', '_')}|peptide")
        print(f"{r['peptide_sequence']}")
        print(f">{r['lead_id']}|{r['target'].replace(' ', '_')}|dna_ecoli")
        print(f"{r['dna_ecoli']}")
        print(f">{r['lead_id']}|{r['target'].replace(' ', '_')}|dna_human")
        print(f"{r['dna_human']}")
    print()

    # Synthesis company recommendations
    print("=" * 80)
    print("SYNTHESIS COMPANY OPTIONS")
    print("=" * 80)
    print("""
    1. PEPTIDE SYNTHESIS (direct peptide ordering):
       ├─ GenScript: https://www.genscript.com/peptide-synthesis.html
       ├─ Thermo Fisher: https://www.thermofisher.com/peptide-synthesis
       └─ Sigma-Aldrich: Custom peptide synthesis

       → Order the PEPTIDE sequences directly (faster, purer)
       → Recommended purity: >95% for binding assays
       → Include N-terminal acetylation and C-terminal amidation

    2. DNA SYNTHESIS (for recombinant expression):
       ├─ IDT (Integrated DNA Technologies): https://www.idtdna.com
       ├─ Twist Bioscience: https://www.twistbioscience.com
       └─ GenScript: Gene synthesis service

       → Use for cloning into expression vectors
       → Consider adding His-tag for purification
       → Add restriction sites for cloning (NdeI/XhoI recommended)

    3. RECOMMENDED CLONING STRATEGY:

       NdeI─ATG─[PEPTIDE_DNA]─STOP─XhoI

       Insert into pET28a or pET21a for E. coli expression
       Insert into pcDNA3.1 for mammalian expression
    """)

    # Summary table
    print("=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print()
    print(f"{'Lead ID':<15}{'Peptide':<15}{'Length':<8}{'DNA (bp)':<10}{'GC% (E.coli)':<12}{'Disease'}")
    print("-" * 80)
    for r in results:
        print(f"{r['lead_id']:<15}{r['peptide_sequence']:<15}{r['peptide_length']:<8}{r['dna_length']:<10}{r['gc_content_ecoli']:.1f}%{'':<7}{r['disease']}")
    print()

    # Save to JSON
    output_dir = Path("../synthesis_orders")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "z2_lead_dna_sequences.json"
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'z2_constant': 6.015152508891966,
            'leads': results,
        }, f, indent=2)

    # Save FASTA files
    fasta_peptide = output_dir / "z2_leads_peptides.fasta"
    fasta_dna_ecoli = output_dir / "z2_leads_dna_ecoli.fasta"
    fasta_dna_human = output_dir / "z2_leads_dna_human.fasta"

    with open(fasta_peptide, 'w') as f:
        for r in results:
            f.write(f">{r['lead_id']}|{r['target']}|{r['disease']}\n")
            f.write(f"{r['peptide_sequence']}\n")

    with open(fasta_dna_ecoli, 'w') as f:
        for r in results:
            f.write(f">{r['lead_id']}_Ecoli|{r['target']}|GC={r['gc_content_ecoli']:.1f}%\n")
            f.write(f"{r['dna_ecoli']}\n")

    with open(fasta_dna_human, 'w') as f:
        for r in results:
            f.write(f">{r['lead_id']}_Human|{r['target']}|GC={r['gc_content_human']:.1f}%\n")
            f.write(f"{r['dna_human']}\n")

    print("=" * 80)
    print("FILES SAVED")
    print("=" * 80)
    print(f"    JSON:         {output_file}")
    print(f"    FASTA (pep):  {fasta_peptide}")
    print(f"    FASTA (E.c):  {fasta_dna_ecoli}")
    print(f"    FASTA (Hum):  {fasta_dna_human}")
    print("=" * 80)

    return results


if __name__ == '__main__':
    generate_synthesis_orders()
