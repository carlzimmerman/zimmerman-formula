#!/usr/bin/env python3
"""
M4 Eye/Vision Pipeline Controller
===================================

Orchestrates the complete eye/vision therapeutic peptide pipeline:
1. Target extraction and validation
2. De novo peptide design
3. Simulation and validation
4. Results synthesis

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026
"""

import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


def run_complete_pipeline():
    """Run the complete eye/vision pipeline."""

    print("=" * 80)
    print("M4 EYE/VISION THERAPEUTIC PIPELINE")
    print("=" * 80)
    print(f"Started: {datetime.now().isoformat()}")
    print()
    print("This pipeline designs therapeutic peptides for:")
    print("  - Age-Related Macular Degeneration (wet and dry)")
    print("  - Diabetic Retinopathy")
    print("  - Glaucoma")
    print("  - Cataracts")
    print("  - Dry Eye target system")
    print("  - Uveitis")
    print("  - Retinitis Pigmentosa")
    print("  - Corneal Disorders")
    print()
    print("=" * 80)

    # Stage 1: Target Extraction
    print("\n" + "=" * 80)
    print("STAGE 1: TARGET EXTRACTION")
    print("=" * 80)

    from m4_eye_target_extraction import run_target_extraction
    targets = run_target_extraction()

    if not targets:
        print("ERROR: Target extraction failed!")
        return None

    print(f"\nExtracted {len(targets)} validated therapeutic targets")

    # Stage 2: Peptide Design
    print("\n" + "=" * 80)
    print("STAGE 2: PEPTIDE DESIGN")
    print("=" * 80)

    from m4_eye_peptide_design import run_peptide_design
    peptides = run_peptide_design(peptides_per_target=15)

    if not peptides:
        print("ERROR: Peptide design failed!")
        return None

    print(f"\nDesigned {len(peptides)} therapeutic peptides")

    # Stage 3: Simulation & Validation
    print("\n" + "=" * 80)
    print("STAGE 3: SIMULATION & VALIDATION")
    print("=" * 80)

    from m4_eye_simulation_validation import run_validation
    validation_results = run_validation()

    if not validation_results:
        print("ERROR: Validation failed!")
        return None

    # Final Summary
    print("\n" + "=" * 80)
    print("PIPELINE COMPLETE")
    print("=" * 80)
    print(f"Completed: {datetime.now().isoformat()}")
    print()
    print("SUMMARY:")
    print(f"  Targets extracted: {len(targets)}")
    print(f"  Peptides designed: {len(peptides)}")
    print(f"  Binding validations: {len(validation_results.get('binding', []))}")
    print(f"  PK predictions: {len(validation_results.get('pk', []))}")
    print(f"  Efficacy predictions: {len(validation_results.get('efficacy', []))}")
    print()

    # Count high priority
    high_priority = sum(1 for b in validation_results.get('binding', [])
                       if b.development_priority == "HIGH")
    print(f"HIGH PRIORITY CANDIDATES: {high_priority}")
    print()

    print("Output files saved to:")
    print(f"  - targets/")
    print(f"  - peptides/")
    print(f"  - validation/")
    print()

    print("=" * 80)
    print("LICENSE: AGPL-3.0-or-later")
    print("All sequences published as prior art for defensive purposes")
    print("=" * 80)

    return {
        "targets": targets,
        "peptides": peptides,
        "validation": validation_results,
    }


if __name__ == "__main__":
    run_complete_pipeline()
