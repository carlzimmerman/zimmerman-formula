#!/usr/bin/env python3
"""
M4 Neurological Disorders Pipeline Controller
===============================================

Orchestrates the complete neurological disorders therapeutic peptide pipeline.

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def run_complete_pipeline():
    """Run the complete neurological disorders pipeline."""

    print("=" * 80)
    print("M4 NEUROLOGICAL DISORDERS THERAPEUTIC PIPELINE")
    print("=" * 80)
    print(f"Started: {datetime.now().isoformat()}")
    print()
    print("This pipeline designs therapeutic peptides for:")
    print("  - Alzheimer's target system (Aβ, Tau, BACE1, TREM2)")
    print("  - Parkinson's target system (α-synuclein, LRRK2, GBA1)")
    print("  - ALS (SOD1, TDP-43, C9orf72)")
    print("  - Huntington's target system (polyQ aggregation)")
    print("  - Multiple Sclerosis (α4-integrin, CD20, MOG)")
    print("  - Stroke/Neuroprotection (NMDAR, PSD-95, BDNF)")
    print()
    print("BBB crossing strategies included: Angiopep-2, TAT, Penetratin")
    print()
    print("=" * 80)

    # Stage 1: Target Extraction
    print("\n" + "=" * 80)
    print("STAGE 1: TARGET EXTRACTION")
    print("=" * 80)

    from m4_neuro_target_extraction import run_target_extraction
    targets = run_target_extraction()

    if not targets:
        print("ERROR: Target extraction failed!")
        return None

    print(f"\nExtracted {len(targets)} validated therapeutic targets")

    # Stage 2: Peptide Design
    print("\n" + "=" * 80)
    print("STAGE 2: PEPTIDE DESIGN")
    print("=" * 80)

    from m4_neuro_peptide_design import run_peptide_design
    peptides = run_peptide_design(peptides_per_target=12)

    if not peptides:
        print("ERROR: Peptide design failed!")
        return None

    print(f"\nDesigned {len(peptides)} therapeutic peptides")

    # Final Summary
    print("\n" + "=" * 80)
    print("PIPELINE COMPLETE")
    print("=" * 80)
    print(f"Completed: {datetime.now().isoformat()}")
    print()
    print("SUMMARY:")
    print(f"  Targets extracted: {len(targets)}")
    print(f"  Peptides designed: {len(peptides)}")
    print()

    # Count by target system
    diseases = {}
    for p in peptides:
        t = p.target
        if "Amyloid" in t or "Tau" in t or "BACE" in t or "TREM" in t:
            d = "Alzheimer's"
        elif "Synuclein" in t or "LRRK" in t or "GBA" in t or "GDNF" in t:
            d = "Parkinson's"
        elif "SOD1" in t or "TDP" in t or "C9orf" in t:
            d = "ALS"
        elif "Huntingtin" in t:
            d = "Huntington's"
        elif "Integrin" in t or "CD20" in t or "MOG" in t:
            d = "MS"
        else:
            d = "Neuroprotection"
        diseases[d] = diseases.get(d, 0) + 1

    print("PEPTIDES BY target system:")
    for d, c in sorted(diseases.items()):
        print(f"  {d}: {c}")
    print()

    better = sum(1 for p in peptides if p.fold_improvement > 1)
    bbb = sum(1 for p in peptides if p.bbb_strategy)
    print(f"Better than benchmark: {better}")
    print(f"BBB-crossing enabled: {bbb}")
    print()

    print("Output files saved to:")
    print(f"  - targets/")
    print(f"  - peptides/")
    print()

    print("=" * 80)
    print("LICENSE: AGPL-3.0-or-later")
    print("All sequences published as prior art for defensive purposes")
    print("=" * 80)

    return {
        "targets": targets,
        "peptides": peptides,
    }


if __name__ == "__main__":
    run_complete_pipeline()
