#!/usr/bin/env python3
"""
M4 Oral Health Pipeline Controller

Master orchestrator for the oral health bacteria targeting pipeline.
Runs all stages sequentially and generates comprehensive output including
prior art manifest for defensive publication.

Pipeline Stages:
1. Target Extraction - Fetch virulence factor structures
2. Peptide Design - Generate antivirulence peptides
3. Selectivity Check - Screen against commensal bacteria
4. Oral Cavity Validation - Ensure survival in oral environment
5. Output Generation - Archive with prior art hashes

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later
"""

import json
import hashlib
import os
import shutil
import zipfile
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

# Import pipeline stages
from m4_oral_pathogen_target_extraction import main as extract_targets
from m4_antivirulence_peptide_designer import main as design_peptides
from m4_commensal_selectivity_checker import main as check_selectivity
from m4_oral_cavity_validator import main as validate_oral

# ==============================================================================
# CONFIGURATION
# ==============================================================================

PIPELINE_VERSION = "1.0.0"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "results")

# Pipeline metadata
PIPELINE_METADATA = {
    "name": "M4 Oral Health Bacteria Targeting Pipeline",
    "version": PIPELINE_VERSION,
    "author": "Carl Zimmerman & Claude Opus 4.5",
    "date": "April 2026",
    "license": "AGPL-3.0-or-later",
    "description": "Designs selective antivirulence peptides targeting pathogenic "
                   "oral bacteria while preserving beneficial commensals.",
    "targets": [
        "Glucosyltransferase GtfC (S. mutans) - Dental caries",
        "Gingipain RgpB (P. gingivalis) - Periodontitis",
        "FadA adhesin (F. nucleatum) - Gingivitis/Cancer link",
        "Sortase A (S. mutans) - Biofilm formation",
    ],
    "approach": "Antivirulence (disarm, don't kill) to minimize resistance pressure",
    "validation": [
        "Commensal selectivity screening (15+ species)",
        "pH stability (5.5-7.5)",
        "Protease resistance (trypsin, chymotrypsin, pepsin, elastase)",
        "Biofilm penetration assessment",
    ],
}


# ==============================================================================
# PIPELINE ORCHESTRATION
# ==============================================================================

@dataclass
class PipelineResult:
    """Complete pipeline result."""
    success: bool
    stages_completed: List[str]
    stages_failed: List[str]
    total_peptides_designed: int
    peptides_validated: int
    peptides_rejected: int
    top_candidates: List[Dict]
    prior_art_manifest: Dict
    output_archive: str
    timestamp: str
    elapsed_seconds: float


def run_stage(stage_name: str, stage_func) -> Optional[any]:
    """Run a pipeline stage with error handling."""
    print("\n" + "="*70)
    print(f"STAGE: {stage_name}")
    print("="*70)

    try:
        result = stage_func()
        print(f"\n[{stage_name}] COMPLETED")
        return result
    except Exception as e:
        print(f"\n[{stage_name}] FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def collect_top_candidates(design_results: Dict, selectivity_reports: List,
                           validation_reports: List) -> List[Dict]:
    """Collect top candidates that passed all stages."""

    candidates = []

    # Build lookup tables
    selectivity_by_id = {r.peptide_id: r for r in selectivity_reports} if selectivity_reports else {}
    validation_by_id = {r.peptide_id: r for r in validation_reports} if validation_reports else {}

    # Iterate through designed peptides
    for target_id, peptides in design_results.items():
        for pep in peptides[:5]:  # Top 5 per target
            peptide_id = pep.peptide_id

            # Get selectivity result
            sel_result = selectivity_by_id.get(peptide_id)
            sel_verdict = sel_result.overall_verdict if sel_result else "NOT_SCREENED"

            # Get validation result
            val_result = validation_by_id.get(peptide_id)
            val_verdict = val_result.verdict if val_result else "NOT_VALIDATED"

            # Only include if passed or warned (not rejected)
            if sel_verdict != "REJECT" and val_verdict != "REJECTED":
                candidate = {
                    "peptide_id": peptide_id,
                    "sequence": pep.sequence,
                    "target": pep.target_id,
                    "length": pep.length,
                    "design_score": pep.overall_score,
                    "selectivity_verdict": sel_verdict,
                    "selectivity_index": sel_result.minimum_selectivity_index if sel_result else None,
                    "oral_viability_verdict": val_verdict,
                    "oral_viability_score": val_result.overall_oral_viability_score if val_result else None,
                    "sha256": pep.sha256_hash,
                }
                candidates.append(candidate)

    # Sort by combined score
    def combined_score(c):
        design = c.get("design_score", 0) or 0
        oral = c.get("oral_viability_score", 0) or 0
        return design * 0.5 + oral * 0.5

    candidates.sort(key=combined_score, reverse=True)

    return candidates[:20]  # Top 20 overall


def generate_prior_art_manifest(design_results: Dict, candidates: List[Dict]) -> Dict:
    """Generate prior art manifest with cryptographic hashes."""

    manifest = {
        "title": "Prior Art Manifest: Oral Health Antivirulence Peptides",
        "generated": datetime.now().isoformat(),
        "generator": "M4 Oral Health Pipeline v" + PIPELINE_VERSION,
        "license": "AGPL-3.0-or-later",
        "purpose": "Defensive publication to establish prior art and prevent "
                   "patent claims on these peptide sequences.",
        "legal_notice": "These sequences are published under AGPL-3.0-or-later license. "
                        "Any derivative works must be released under the same license. "
                        "This manifest serves as evidence of prior disclosure.",
        "sequences": {},
        "manifest_hash": ""
    }

    # Add all designed sequences with their hashes
    for target_id, peptides in design_results.items():
        for pep in peptides:
            manifest["sequences"][pep.peptide_id] = {
                "sequence": pep.sequence,
                "target": pep.target_id,
                "sha256": pep.sha256_hash,
                "timestamp": pep.timestamp,
            }

    # Compute manifest hash
    manifest_content = json.dumps(manifest["sequences"], sort_keys=True)
    manifest["manifest_hash"] = hashlib.sha256(manifest_content.encode()).hexdigest()

    return manifest


def create_output_archive(timestamp: str) -> str:
    """Create ZIP archive of all results."""

    archive_name = f"oral_health_pipeline_{timestamp}.zip"
    archive_path = os.path.join(OUTPUT_DIR, archive_name)

    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all result files
        for root, dirs, files in os.walk(OUTPUT_DIR):
            for file in files:
                if file.endswith(('.json', '.fasta', '.md')) and not file.endswith('.zip'):
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, OUTPUT_DIR)
                    zipf.write(filepath, arcname)

        # Add README
        readme_path = os.path.join(os.path.dirname(__file__), "README.md")
        if os.path.exists(readme_path):
            zipf.write(readme_path, "README.md")

    return archive_path


def run_pipeline() -> PipelineResult:
    """Run the complete oral health targeting pipeline."""

    start_time = datetime.now()
    timestamp = start_time.strftime("%Y%m%d_%H%M%S")

    print("="*70)
    print("M4 ORAL HEALTH BACTERIA TARGETING PIPELINE")
    print("="*70)
    print(f"Version: {PIPELINE_VERSION}")
    print(f"Started: {start_time.isoformat()}")
    print("="*70)

    stages_completed = []
    stages_failed = []

    # Stage 1: Target Extraction
    extraction_result = run_stage("Target Extraction", extract_targets)
    if extraction_result:
        stages_completed.append("Target Extraction")
    else:
        stages_failed.append("Target Extraction")

    # Stage 2: Peptide Design
    design_result = run_stage("Peptide Design", design_peptides)
    if design_result:
        stages_completed.append("Peptide Design")
        total_designed = sum(len(peptides) for peptides in design_result.values())
    else:
        stages_failed.append("Peptide Design")
        total_designed = 0
        design_result = {}

    # Stage 3: Selectivity Check
    selectivity_result = run_stage("Selectivity Check", check_selectivity)
    if selectivity_result:
        stages_completed.append("Selectivity Check")
    else:
        stages_failed.append("Selectivity Check")
        selectivity_result = []

    # Stage 4: Oral Cavity Validation
    validation_result = run_stage("Oral Cavity Validation", validate_oral)
    if validation_result:
        stages_completed.append("Oral Cavity Validation")
        validated = sum(1 for r in validation_result if r.verdict == "VALIDATED")
        rejected = sum(1 for r in validation_result if r.verdict == "REJECTED")
    else:
        stages_failed.append("Oral Cavity Validation")
        validation_result = []
        validated = 0
        rejected = 0

    # Collect top candidates
    top_candidates = collect_top_candidates(design_result, selectivity_result, validation_result)

    # Generate prior art manifest
    prior_art = generate_prior_art_manifest(design_result, top_candidates)

    # Save prior art manifest
    manifest_path = os.path.join(OUTPUT_DIR, "PRIOR_ART_MANIFEST.json")
    with open(manifest_path, 'w') as f:
        json.dump(prior_art, f, indent=2)
    print(f"\nPrior art manifest saved: {manifest_path}")

    # Save top candidates summary
    candidates_path = os.path.join(OUTPUT_DIR, "TOP_CANDIDATES.json")
    with open(candidates_path, 'w') as f:
        json.dump({
            "pipeline": PIPELINE_METADATA,
            "timestamp": timestamp,
            "candidates": top_candidates,
        }, f, indent=2)
    print(f"Top candidates saved: {candidates_path}")

    # Create archive
    archive_path = create_output_archive(timestamp)
    print(f"Results archive created: {archive_path}")

    # Calculate elapsed time
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()

    # Determine overall success
    success = len(stages_failed) == 0

    result = PipelineResult(
        success=success,
        stages_completed=stages_completed,
        stages_failed=stages_failed,
        total_peptides_designed=total_designed,
        peptides_validated=validated,
        peptides_rejected=rejected,
        top_candidates=top_candidates,
        prior_art_manifest=prior_art,
        output_archive=archive_path,
        timestamp=timestamp,
        elapsed_seconds=elapsed
    )

    return result


def print_final_summary(result: PipelineResult):
    """Print final pipeline summary."""

    print("\n" + "="*70)
    print("PIPELINE COMPLETE")
    print("="*70)

    status = "SUCCESS" if result.success else "PARTIAL (some stages failed)"
    print(f"\nStatus: {status}")
    print(f"Elapsed time: {result.elapsed_seconds:.1f} seconds")

    print(f"\nStages completed: {len(result.stages_completed)}")
    for stage in result.stages_completed:
        print(f"  [+] {stage}")

    if result.stages_failed:
        print(f"\nStages failed: {len(result.stages_failed)}")
        for stage in result.stages_failed:
            print(f"  [-] {stage}")

    print(f"\n--- SUMMARY ---")
    print(f"Total peptides designed: {result.total_peptides_designed}")
    print(f"Validated for oral cavity: {result.peptides_validated}")
    print(f"Rejected: {result.peptides_rejected}")
    print(f"Top candidates identified: {len(result.top_candidates)}")

    if result.top_candidates:
        print("\n--- TOP 5 CANDIDATES ---")
        for i, c in enumerate(result.top_candidates[:5], 1):
            print(f"\n{i}. {c['peptide_id']}")
            print(f"   Sequence: {c['sequence']}")
            print(f"   Target: {c['target']}")
            print(f"   Design score: {c['design_score']:.3f}")
            print(f"   Selectivity: {c['selectivity_verdict']}")
            print(f"   Oral viability: {c['oral_viability_verdict']}")
            if c.get('oral_viability_score'):
                print(f"   Oral score: {c['oral_viability_score']:.2f}")

    print(f"\n--- OUTPUT FILES ---")
    print(f"Archive: {result.output_archive}")
    print(f"Prior art manifest: {os.path.join(OUTPUT_DIR, 'PRIOR_ART_MANIFEST.json')}")
    print(f"Top candidates: {os.path.join(OUTPUT_DIR, 'TOP_CANDIDATES.json')}")

    print("\n" + "="*70)
    print("Prior Art Notice:")
    print(f"  Manifest hash: {result.prior_art_manifest.get('manifest_hash', 'N/A')[:32]}...")
    print("  All sequences are published under AGPL-3.0-or-later")
    print("  This constitutes defensive publication establishing prior art")
    print("="*70)


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Main entry point."""

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Run pipeline
    result = run_pipeline()

    # Print summary
    print_final_summary(result)

    # Save pipeline result
    result_path = os.path.join(OUTPUT_DIR, f"pipeline_result_{result.timestamp}.json")
    with open(result_path, 'w') as f:
        result_dict = asdict(result)
        # Convert non-serializable items
        result_dict["top_candidates"] = result.top_candidates
        result_dict["prior_art_manifest"] = {"hash": result.prior_art_manifest.get("manifest_hash")}
        json.dump(result_dict, f, indent=2, default=str)

    print(f"\nPipeline result saved: {result_path}")

    return result


if __name__ == "__main__":
    main()
