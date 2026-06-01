#!/usr/bin/env python3
"""
M4 CRISPR-Cas9 Minimization Screener
=====================================

Computationally minimizes SpCas9 for AAV vector delivery.

THE PROBLEM:
SpCas9 is 1368 amino acids (~4.1 kb coding sequence). AAV vectors have a
packaging limit of ~4.7 kb total, leaving almost no room for:
- Guide RNA scaffold
- Promoter
- Poly-A signal
- ITRs

THE SOLUTION:
Systematically truncate non-catalytic domains while preserving:
- HNH nuclease domain (cuts target strand)
- RuvC nuclease domain (cuts non-target strand)
- Minimal guide RNA binding capability

TARGET: <1000 amino acids with pLDDT > 85 and preserved catalytic function

SpCas9 DOMAIN ARCHITECTURE:
==========================
Position    Domain          Function                    Essential?
--------    ------          --------                    ----------
1-60        RuvC-I          Nuclease (part 1)           YES
61-93       Bridge helix    Connects to REC             Partial
94-179      REC1            Guide RNA binding           Partial
180-307     REC2            Guide RNA binding           Minimal
308-713     REC3            Target DNA recognition      Partial
714-717     Linker          -                           No
718-765     RuvC-II         Nuclease (part 2)           YES
766-780     Linker          -                           No
781-906     HNH             Nuclease (target strand)    YES
907-1098    RuvC-III        Nuclease (part 3)           YES
1099-1200   WED             PAM recognition             Partial
1201-1368   PI              PAM interacting             Partial

LICENSE: AGPL-3.0-or-later + OpenMTA + CC-BY-SA-4.0
AUTHOR: Carl Zimmerman
DATE: April 2026

PRIOR ART: Released to prevent corporate capture of Cas9 minimization.
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import urllib.request

# =============================================================================
# CONSTANTS
# =============================================================================

# SpCas9 reference (Streptococcus pyogenes)
SPCAS9_PDB = "4UN3"
SPCAS9_UNIPROT = "Q99ZW2"
SPCAS9_LENGTH = 1368

# AAV packaging constraints
AAV_MAX_GENOME = 4700  # bp
AAV_OVERHEAD = 1500    # ITRs, promoter, polyA, sgRNA scaffold
AAV_AVAILABLE = AAV_MAX_GENOME - AAV_OVERHEAD  # ~3200 bp for Cas9
MAX_AA_FOR_AAV = AAV_AVAILABLE // 3  # ~1066 aa

# Target size
TARGET_MAX_AA = 1000
TARGET_MIN_PLDDT = 85.0

# SpCas9 domain boundaries (1-indexed, inclusive)
DOMAINS = {
    'RuvC_I': (1, 60, True, "Nuclease domain part 1 - ESSENTIAL"),
    'Bridge': (61, 93, True, "Bridge helix - needed for structure"),
    'REC1': (94, 179, False, "Recognition lobe 1 - partially dispensable"),
    'REC2': (180, 307, False, "Recognition lobe 2 - dispensable"),
    'REC3': (308, 713, False, "Recognition lobe 3 - partially dispensable"),
    'Linker1': (714, 717, False, "Linker - dispensable"),
    'RuvC_II': (718, 765, True, "Nuclease domain part 2 - ESSENTIAL"),
    'Linker2': (766, 780, False, "Linker - dispensable"),
    'HNH': (781, 906, True, "HNH nuclease - ESSENTIAL"),
    'RuvC_III': (907, 1098, True, "Nuclease domain part 3 - ESSENTIAL"),
    'WED': (1099, 1200, True, "Wedge domain - needed for PAM"),
    'PI': (1201, 1368, True, "PAM-interacting - needed for PAM"),
}

# Essential domains (must keep)
ESSENTIAL_DOMAINS = ['RuvC_I', 'Bridge', 'RuvC_II', 'HNH', 'RuvC_III', 'WED', 'PI']

# Dispensable domains (can truncate)
DISPENSABLE_DOMAINS = ['REC1', 'REC2', 'REC3', 'Linker1', 'Linker2']

# SpCas9 sequence (from UniProt Q99ZW2)
SPCAS9_SEQUENCE = """
MDKKYSIGLDIGTNSVGWAVITDEYKVPSKKFKVLGNTDRHSIKKNLIGALLFDSGETAE
ATRLKRTARRRYTRRKNRICYLQEIFSNEMAKVDDSFFHRLEESFLVEEDKKHERHPIFG
NIVDEVAYHEKYPTIYHLRKKLVDSTDKADLRLIYLALAHMIKFRGHFLIEGDLNPDNSD
VDKLFIQLVQTYNQLFEENPINASGVDAKAILSARLSKSRRLENLIAQLPGEKKNGLFGN
LIALSLGLTPNFKSNFDLAEDAKLQLSKDTYDDDLDNLLAQIGDQYADLFLAAKNLSDAI
LLSDILRVNTEITKAPLSASMIKRYDEHHQDLTLLKALVRQQLPEKYKEIFFDQSKNGYA
GYIDGGASQEEFYKFIKPILEKMDGTEELLVKLNREDLLRKQRTFDNGSIPHQIHLGELH
AILRRQEDFYPFLKDNREKIEKILTFRIPYYVGPLARGNSRFAWMTRKSEETITPWNFEE
VVDKGASAQSFIERMTNFDKNLPNEKVLPKHSLLYEYFTVYNELTKVKYVTEGMRKPAFL
SGEQKKAIVDLLFKTNRKVTVKQLKEDYFKKIECFDSVEISGVEDRFNASLGTYHDLLKI
IKDKDFLDNEENEDILEDIVLTLTLFEDREMIEERLKTYAHLFDDKVMKQLKRRRYTGWG
RLSRKLINGIRDKQSGKTILDFLKSDGFANRNFMQLIHDDSLTFKEDIQKAQVSGQGDSL
HEHIANLAGSPAIKKGILQTVKVVDELVKVMGRHKPENIVIEMARENQTTQKGQKNSRER
MKRIEEGIKELGSQILKEHPVENTQLQNEKLYLYYLQNGRDMYVDQELDINRLSDYDVDH
IVPQSFLKDDSIDNKVLTRSDKNRGKSDNVPSEEVVKKMKNYWRQLLNAKLITQRKFDNL
TKAERGGLSELDKAGFIKRQLVETRQITKHVAQILDSRMNTKYDENDKLIREVKVITLKS
KLVSDFRKDFQFYKVREINNYHHAHDAYLNAVVGTALIKKYPKLESEFVYGDYKVYDVRK
MIAKSEQEIGKATAKYFFYSNIMNFFKTEITLANGEIRKRPLIETNGETGEIVWDKGRDF
ATVRKVLSMPQVNIVKKTEVQTGGFSKESILPKRNSDKLIARKKDWDPKKYGGFDSPTVA
YSVLVVAKVEKGKSKKLKSVKELLGITIMERSSFEKNPIDFLEAKGYKEVKKDLIIKLPK
YSLFELENGRKRMLASAGELQKGNELALPSKYVNFLYLASHYEKLKGSPEDNEQKQLFVE
QHKHYLDEIIEQISEFSKRVILADANLDKVLSAYNKHRDKPIREQAENIIHLFTLTNLGA
PAAFKYFDTTIDRKRYTSTKEVLDATLIHQSITGLYETRIDLSQLGGD
""".replace('\n', '').replace(' ', '')


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Cas9Variant:
    """A Cas9 minimization variant."""
    name: str
    sequence: str
    length: int
    domains_kept: List[str]
    domains_removed: List[str]
    truncation_strategy: str
    estimated_plddt: float
    catalytic_intact: bool
    aav_compatible: bool
    score: float


# =============================================================================
# SEQUENCE MANIPULATION
# =============================================================================

def get_domain_sequence(sequence: str, domain_name: str) -> str:
    """Extract a domain's sequence."""
    start, end, _, _ = DOMAINS[domain_name]
    return sequence[start-1:end]  # Convert to 0-indexed


def remove_domain(sequence: str, domain_name: str) -> str:
    """Remove a domain from the sequence."""
    start, end, _, _ = DOMAINS[domain_name]
    return sequence[:start-1] + sequence[end:]


def keep_only_domains(sequence: str, domains_to_keep: List[str]) -> str:
    """Construct sequence keeping only specified domains."""
    result = ""
    for domain in DOMAINS.keys():
        if domain in domains_to_keep:
            result += get_domain_sequence(sequence, domain)
    return result


def add_linker(seq1: str, seq2: str, linker: str = "GSGS") -> str:
    """Add a flexible linker between two sequences."""
    return seq1 + linker + seq2


# =============================================================================
# STABILITY PREDICTION
# =============================================================================

def estimate_stability(sequence: str, domains_kept: List[str]) -> float:
    """
    Estimate structural stability of a Cas9 variant.

    Factors:
    1. Essential domain integrity
    2. Sequence composition
    3. Known functional requirements

    This is a heuristic; ESMFold validation recommended for top candidates.
    """
    score = 50.0  # Base score

    # Bonus for keeping essential domains
    for domain in ESSENTIAL_DOMAINS:
        if domain in domains_kept:
            score += 5.0

    # Penalty for breaking RuvC continuity
    ruvc_parts = ['RuvC_I', 'RuvC_II', 'RuvC_III']
    ruvc_kept = sum(1 for d in ruvc_parts if d in domains_kept)
    if ruvc_kept < 3:
        score -= 20.0  # Broken RuvC is bad

    # Check for HNH
    if 'HNH' not in domains_kept:
        score -= 30.0  # No HNH = no target strand cleavage

    # Length penalty (very short = likely unstable)
    if len(sequence) < 500:
        score -= 15.0
    elif len(sequence) < 700:
        score -= 5.0

    # Composition check (hydrophobic balance)
    hydrophobic = sum(1 for aa in sequence if aa in 'AILMFVW')
    hydrophobic_frac = hydrophobic / len(sequence) if sequence else 0
    if 0.25 <= hydrophobic_frac <= 0.40:
        score += 5.0  # Good balance

    # Cap at reasonable pLDDT range
    return max(30.0, min(95.0, score))


def check_catalytic_integrity(domains_kept: List[str]) -> bool:
    """Check if catalytic domains are intact."""
    required = ['RuvC_I', 'RuvC_II', 'RuvC_III', 'HNH']
    return all(d in domains_kept for d in required)


# =============================================================================
# MINIMIZATION STRATEGIES
# =============================================================================

def strategy_remove_rec2(sequence: str) -> Cas9Variant:
    """
    Strategy 1: Remove REC2 only (most conservative).

    REC2 is the most dispensable domain for basic function.
    """
    domains_kept = [d for d in DOMAINS.keys() if d != 'REC2']
    new_seq = remove_domain(sequence, 'REC2')

    return Cas9Variant(
        name="Cas9-ΔREC2",
        sequence=new_seq,
        length=len(new_seq),
        domains_kept=domains_kept,
        domains_removed=['REC2'],
        truncation_strategy="Remove REC2 (128 aa)",
        estimated_plddt=estimate_stability(new_seq, domains_kept),
        catalytic_intact=check_catalytic_integrity(domains_kept),
        aav_compatible=len(new_seq) <= TARGET_MAX_AA,
        score=0.0,
    )


def strategy_remove_rec2_rec3_partial(sequence: str) -> Cas9Variant:
    """
    Strategy 2: Remove REC2 and partial REC3.

    Keep first 100 aa of REC3 for minimal guide binding.
    """
    # Custom truncation
    domains_kept = [d for d in DOMAINS.keys() if d not in ['REC2', 'REC3']]

    # Keep partial REC3 (first 100 aa)
    rec3_start, rec3_end, _, _ = DOMAINS['REC3']
    partial_rec3 = sequence[rec3_start-1:rec3_start-1+100]

    # Construct new sequence
    new_seq = (
        sequence[:179] +  # Through REC1
        partial_rec3 +    # Partial REC3
        sequence[713:]    # From linker1 onwards
    )

    domains_kept.append('REC3_partial')

    return Cas9Variant(
        name="Cas9-ΔREC2-ΔpREC3",
        sequence=new_seq,
        length=len(new_seq),
        domains_kept=domains_kept,
        domains_removed=['REC2', 'REC3 (partial)'],
        truncation_strategy="Remove REC2, truncate REC3 to 100aa",
        estimated_plddt=estimate_stability(new_seq, domains_kept),
        catalytic_intact=check_catalytic_integrity(domains_kept),
        aav_compatible=len(new_seq) <= TARGET_MAX_AA,
        score=0.0,
    )


def strategy_minimal_rec(sequence: str) -> Cas9Variant:
    """
    Strategy 3: Minimal REC lobe.

    Keep only essential portions of REC for guide binding.
    Similar to SaCas9 and CjCas9 architecture.
    """
    # Keep: RuvC_I, Bridge, minimal REC1, RuvC_II, HNH, RuvC_III, WED, PI
    # Remove: REC2, REC3, linkers

    new_seq = (
        sequence[0:93] +      # RuvC_I + Bridge
        sequence[93:140] +    # Partial REC1 (guide contact residues)
        "GSGS" +              # Flexible linker
        sequence[717:1368]    # RuvC_II through PI
    )

    domains_kept = ['RuvC_I', 'Bridge', 'REC1_minimal', 'RuvC_II',
                   'HNH', 'RuvC_III', 'WED', 'PI']

    return Cas9Variant(
        name="Cas9-miniREC",
        sequence=new_seq,
        length=len(new_seq),
        domains_kept=domains_kept,
        domains_removed=['REC1 (partial)', 'REC2', 'REC3', 'Linker1', 'Linker2'],
        truncation_strategy="Minimal REC lobe with linker",
        estimated_plddt=estimate_stability(new_seq, domains_kept),
        catalytic_intact=True,  # Catalytic domains intact
        aav_compatible=len(new_seq) <= TARGET_MAX_AA,
        score=0.0,
    )


def strategy_split_intein(sequence: str) -> Cas9Variant:
    """
    Strategy 4: Design for split-intein reconstitution.

    Split Cas9 at natural split point (573/574) for dual-AAV delivery.
    Each half is AAV-compatible, reconstitutes via intein.
    """
    split_point = 573

    # N-terminal half
    n_half = sequence[:split_point]
    # C-terminal half
    c_half = sequence[split_point:]

    # For this variant, we report the larger half
    larger = n_half if len(n_half) >= len(c_half) else c_half

    domains_kept = list(DOMAINS.keys())  # All domains kept (just split)

    return Cas9Variant(
        name="Cas9-split573",
        sequence=sequence,  # Full sequence, but split
        length=len(sequence),
        domains_kept=domains_kept,
        domains_removed=[],
        truncation_strategy=f"Split at 573/574 for dual-AAV (N={len(n_half)}, C={len(c_half)})",
        estimated_plddt=estimate_stability(sequence, domains_kept),
        catalytic_intact=True,
        aav_compatible=True,  # Each half fits AAV
        score=0.0,
    )


def strategy_compact_nuclease(sequence: str) -> Cas9Variant:
    """
    Strategy 5: Compact nuclease core.

    Aggressive minimization keeping only catalytic machinery.
    May require additional engineering for guide binding.
    """
    # Keep only: RuvC (all parts), Bridge, HNH, minimal WED/PI
    new_seq = (
        sequence[0:93] +      # RuvC_I + Bridge
        "GS" +                # Short linker
        sequence[717:780] +   # RuvC_II + Linker2
        sequence[780:906] +   # HNH
        sequence[906:1098] +  # RuvC_III
        "GSGS" +              # Linker
        sequence[1098:1250]   # WED + partial PI
    )

    domains_kept = ['RuvC_I', 'Bridge', 'RuvC_II', 'HNH', 'RuvC_III',
                   'WED', 'PI_partial']

    return Cas9Variant(
        name="Cas9-compact",
        sequence=new_seq,
        length=len(new_seq),
        domains_kept=domains_kept,
        domains_removed=['REC1', 'REC2', 'REC3', 'Linker1', 'PI (partial)'],
        truncation_strategy="Compact nuclease core only",
        estimated_plddt=estimate_stability(new_seq, domains_kept),
        catalytic_intact=True,
        aav_compatible=len(new_seq) <= TARGET_MAX_AA,
        score=0.0,
    )


def strategy_sgrna_dependent(sequence: str) -> Cas9Variant:
    """
    Strategy 6: sgRNA-dependent minimal Cas9.

    Relies on extended sgRNA scaffold for some REC functions.
    Requires co-engineering of guide RNA.
    """
    # Remove REC2, most of REC3, keep guide-contact residues
    new_seq = (
        sequence[0:179] +     # RuvC_I + Bridge + REC1
        sequence[600:713] +   # Last part of REC3 (guide contacts)
        sequence[713:1368]    # Everything from linker1 onwards
    )

    domains_kept = ['RuvC_I', 'Bridge', 'REC1', 'REC3_partial',
                   'Linker1', 'RuvC_II', 'Linker2', 'HNH', 'RuvC_III', 'WED', 'PI']

    return Cas9Variant(
        name="Cas9-sgRNA+",
        sequence=new_seq,
        length=len(new_seq),
        domains_kept=domains_kept,
        domains_removed=['REC2', 'REC3 (partial)'],
        truncation_strategy="Minimal Cas9 + extended sgRNA scaffold",
        estimated_plddt=estimate_stability(new_seq, domains_kept),
        catalytic_intact=True,
        aav_compatible=len(new_seq) <= TARGET_MAX_AA,
        score=0.0,
    )


# =============================================================================
# SCORING
# =============================================================================

def score_variant(variant: Cas9Variant) -> float:
    """
    Score a Cas9 variant for AAV delivery suitability.

    Factors:
    1. Size (smaller = better, but not too small)
    2. Stability (higher pLDDT = better)
    3. Catalytic integrity (essential)
    4. AAV compatibility
    """
    score = 0.0

    # Size score (0-30 points)
    # Optimal: 850-950 aa
    if variant.length <= TARGET_MAX_AA:
        if 850 <= variant.length <= 950:
            size_score = 30.0
        elif variant.length < 850:
            size_score = 30.0 - (850 - variant.length) / 20
        else:
            size_score = 30.0 - (variant.length - 950) / 10
        score += max(0, size_score)
    else:
        score += max(0, 20 - (variant.length - TARGET_MAX_AA) / 50)

    # Stability score (0-40 points)
    if variant.estimated_plddt >= TARGET_MIN_PLDDT:
        score += 40.0
    else:
        score += (variant.estimated_plddt / TARGET_MIN_PLDDT) * 40

    # Catalytic integrity (0 or 20 points)
    if variant.catalytic_intact:
        score += 20.0

    # AAV compatibility bonus (0 or 10 points)
    if variant.aav_compatible:
        score += 10.0

    return score


# =============================================================================
# OUTPUT
# =============================================================================

def export_fasta(variants: List[Cas9Variant], output_file: str) -> None:
    """Export variants to FASTA format."""
    lines = [
        "# CRISPR-Cas9 Minimized Variants",
        "# Designed by M4 Cas Minimization Screener",
        f"# Generated: {datetime.now().isoformat()}",
        "#",
        "# LICENSE: AGPL-3.0-or-later + OpenMTA + CC-BY-SA-4.0",
        "# PRIOR ART established April 20, 2026",
        "#",
        "# WARNING: Computational designs require experimental validation.",
        "# Guide RNA co-engineering may be required for function.",
        "#",
    ]

    for i, v in enumerate(variants, 1):
        header = (
            f">MiniCas9_{i:02d}_{v.name} "
            f"length={v.length} "
            f"pLDDT={v.estimated_plddt:.1f} "
            f"score={v.score:.1f} "
            f"| {v.truncation_strategy}"
        )
        lines.append(header)

        # Wrap sequence
        seq = v.sequence
        for j in range(0, len(seq), 60):
            lines.append(seq[j:j+60])

    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))


def export_report(variants: List[Cas9Variant], output_file: str) -> Dict:
    """Export detailed report as JSON."""
    report = {
        'metadata': {
            'generator': 'M4 Cas Minimization Screener',
            'timestamp': datetime.now().isoformat(),
            'license': 'AGPL-3.0-or-later + OpenMTA + CC-BY-SA-4.0',
            'reference': f'SpCas9 PDB: {SPCAS9_PDB}, UniProt: {SPCAS9_UNIPROT}',
        },
        'constraints': {
            'aav_max_genome_bp': AAV_MAX_GENOME,
            'target_max_aa': TARGET_MAX_AA,
            'target_min_plddt': TARGET_MIN_PLDDT,
            'original_length': SPCAS9_LENGTH,
        },
        'variants': [],
    }

    for v in variants:
        entry = {
            'name': v.name,
            'length': v.length,
            'reduction': f"{(1 - v.length/SPCAS9_LENGTH)*100:.1f}%",
            'domains_kept': v.domains_kept,
            'domains_removed': v.domains_removed,
            'strategy': v.truncation_strategy,
            'estimated_plddt': v.estimated_plddt,
            'catalytic_intact': v.catalytic_intact,
            'aav_compatible': v.aav_compatible,
            'score': v.score,
        }
        report['variants'].append(entry)

    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    return report


# =============================================================================
# MAIN
# =============================================================================

def run_minimization_screen(output_dir: str = "cas9_minimization") -> Dict:
    """Run the full Cas9 minimization screen."""

    print("="*70)
    print("M4 CRISPR-Cas9 MINIMIZATION SCREENER")
    print("="*70)
    print(f"\nReference: SpCas9 (PDB: {SPCAS9_PDB})")
    print(f"Original length: {SPCAS9_LENGTH} aa")
    print(f"Target: <{TARGET_MAX_AA} aa with pLDDT >{TARGET_MIN_PLDDT}")
    print(f"AAV packaging limit: ~{MAX_AA_FOR_AAV} aa")

    # Create output directory
    out_path = Path(output_dir)
    out_path.mkdir(exist_ok=True)

    # Generate variants
    print("\nGenerating minimization variants...")

    strategies = [
        strategy_remove_rec2,
        strategy_remove_rec2_rec3_partial,
        strategy_minimal_rec,
        strategy_split_intein,
        strategy_compact_nuclease,
        strategy_sgrna_dependent,
    ]

    variants = []
    for strategy in strategies:
        try:
            variant = strategy(SPCAS9_SEQUENCE)
            variant.score = score_variant(variant)
            variants.append(variant)
            print(f"  Generated: {variant.name} ({variant.length} aa)")
        except Exception as e:
            print(f"  Failed: {strategy.__name__}: {e}")

    # Sort by score
    variants.sort(key=lambda x: x.score, reverse=True)

    # Display results
    print("\n" + "="*70)
    print("MINIMIZATION RESULTS")
    print("="*70)
    print(f"\n{'Rank':<5} {'Name':<20} {'Length':<8} {'Reduction':<10} {'pLDDT':<8} {'AAV?':<6} {'Score':<8}")
    print("-"*70)

    for i, v in enumerate(variants, 1):
        reduction = f"{(1 - v.length/SPCAS9_LENGTH)*100:.1f}%"
        aav = "YES" if v.aav_compatible else "NO"
        print(f"{i:<5} {v.name:<20} {v.length:<8} {reduction:<10} {v.estimated_plddt:<8.1f} {aav:<6} {v.score:<8.1f}")

    # Export results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    fasta_file = out_path / f"cas9_mini_variants_{timestamp}.fasta"
    export_fasta(variants, str(fasta_file))
    print(f"\nFASTA exported: {fasta_file}")

    json_file = out_path / f"cas9_mini_report_{timestamp}.json"
    report = export_report(variants, str(json_file))
    print(f"Report exported: {json_file}")

    # Summary
    print("\n" + "="*70)
    print("TOP CANDIDATE")
    print("="*70)

    top = variants[0]
    print(f"\nName: {top.name}")
    print(f"Length: {top.length} aa (reduced from {SPCAS9_LENGTH})")
    print(f"Reduction: {(1 - top.length/SPCAS9_LENGTH)*100:.1f}%")
    print(f"Strategy: {top.truncation_strategy}")
    print(f"Estimated pLDDT: {top.estimated_plddt:.1f}")
    print(f"Catalytic intact: {'YES' if top.catalytic_intact else 'NO'}")
    print(f"AAV compatible: {'YES' if top.aav_compatible else 'NO'}")
    print(f"Score: {top.score:.1f}/100")

    print("\n" + "="*70)
    print("AAV PACKAGING ANALYSIS")
    print("="*70)
    print(f"""
SpCas9 original: {SPCAS9_LENGTH} aa × 3 = {SPCAS9_LENGTH * 3} bp coding
AAV capacity:    {AAV_MAX_GENOME} bp total
  - ITRs:        ~300 bp
  - Promoter:    ~500 bp
  - sgRNA:       ~100 bp
  - PolyA:       ~250 bp
  - Available:   ~{AAV_AVAILABLE} bp = ~{MAX_AA_FOR_AAV} aa

Top candidate:   {top.length} aa × 3 = {top.length * 3} bp coding
Margin:          {AAV_AVAILABLE - top.length * 3} bp remaining
""")

    # AAV-compatible variants
    aav_compatible = [v for v in variants if v.aav_compatible and v.catalytic_intact]

    print("="*70)
    print("AAV-COMPATIBLE VARIANTS (single-vector delivery)")
    print("="*70)

    if aav_compatible:
        for v in aav_compatible:
            print(f"  - {v.name}: {v.length} aa, pLDDT={v.estimated_plddt:.1f}")
    else:
        print("  No single-vector compatible variants found.")
        print("  Consider: Split-intein dual-AAV delivery")

    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("""
1. ESMFold validation - Confirm structure prediction for top candidates
2. Molecular dynamics - Assess stability over time
3. In vitro cleavage - Test catalytic activity on target DNA
4. Guide RNA engineering - Optimize scaffold for minimal Cas9
5. AAV packaging test - Confirm encapsidation efficiency
6. Cell culture - Test editing efficiency in mammalian cells
""")

    print("="*70)
    print("LICENSE & PRIOR ART")
    print("="*70)
    print("""
These Cas9 minimization designs are released under:
  - AGPL-3.0-or-later (code)
  - OpenMTA (materials)
  - CC-BY-SA-4.0 (documentation)

PRIOR ART ESTABLISHED: April 20, 2026

This prevents patenting of these specific truncation strategies.
Any derivative work must remain open-source.
""")

    return {
        'variants': variants,
        'fasta_file': str(fasta_file),
        'json_file': str(json_file),
        'report': report,
    }


if __name__ == "__main__":
    results = run_minimization_screen()
