#!/usr/bin/env python3
"""
M4 Prolactinoma Pipeline Controller
====================================

Master automation script for the complete prolactinoma therapeutic pipeline.

PIPELINE STAGES:
================
1. Target Extraction - Fetch D2R and 5-HT2B structures
2. Agonist Design - Generate D2R-selective cyclic peptides
3. Thermodynamics - MM/PBSA binding energy validation
4. Prior Art - Hash and archive validated candidates

LICENSE: AGPL-3.0-or-later + OpenMTA + CC-BY-SA-4.0
AUTHOR: Carl Zimmerman
DATE: April 2026

PRIOR ART MANIFEST:
==================
All validated peptide sequences are cryptographically hashed (SHA-256)
and archived to establish prior art, preventing corporate capture.
"""

import json
import hashlib
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import subprocess
import sys

# =============================================================================
# PIPELINE CONFIGURATION
# =============================================================================

PIPELINE_NAME = "M4 Prolactinoma Therapeutic Pipeline"
PIPELINE_VERSION = "1.0.0"

STAGES = [
    {
        'name': 'Target Extraction',
        'script': 'm4_pituitary_target_extraction.py',
        'description': 'Fetch D2R and 5-HT2B receptor structures',
    },
    {
        'name': 'Agonist Design',
        'script': 'm4_d2r_selective_agonist_design.py',
        'description': 'Generate D2R-selective cyclic peptides',
    },
    {
        'name': 'Thermodynamics',
        'script': 'm4_prolactinoma_thermodynamics.py',
        'description': 'MM/PBSA binding energy validation',
    },
]


# =============================================================================
# EXECUTION
# =============================================================================

def run_stage(stage: Dict, working_dir: Path) -> Dict:
    """Run a pipeline stage."""
    script_path = working_dir / stage['script']

    result = {
        'stage': stage['name'],
        'script': stage['script'],
        'status': 'PENDING',
        'start_time': datetime.now().isoformat(),
        'end_time': None,
        'output': None,
        'error': None,
    }

    if not script_path.exists():
        result['status'] = 'SKIPPED'
        result['error'] = f"Script not found: {script_path}"
        return result

    print(f"\n{'='*70}")
    print(f"STAGE: {stage['name']}")
    print(f"{'='*70}")
    print(f"Script: {stage['script']}")
    print(f"Description: {stage['description']}")
    print()

    try:
        # Run the script
        proc = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(working_dir),
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
        )

        result['output'] = proc.stdout
        result['error'] = proc.stderr if proc.returncode != 0 else None
        result['status'] = 'SUCCESS' if proc.returncode == 0 else 'FAILED'

        # Print output
        if proc.stdout:
            print(proc.stdout)

        if proc.returncode != 0 and proc.stderr:
            print(f"\nERROR:\n{proc.stderr}")

    except subprocess.TimeoutExpired:
        result['status'] = 'TIMEOUT'
        result['error'] = 'Stage exceeded 10 minute timeout'
    except Exception as e:
        result['status'] = 'ERROR'
        result['error'] = str(e)

    result['end_time'] = datetime.now().isoformat()
    return result


# =============================================================================
# PRIOR ART MANIFEST
# =============================================================================

def collect_peptide_sequences(working_dir: Path) -> List[Dict]:
    """Collect all generated peptide sequences."""
    sequences = []

    # Check peptides directory
    peptide_dir = working_dir / "peptides"
    if peptide_dir.exists():
        for fasta_file in peptide_dir.glob("*.fasta"):
            with open(fasta_file) as f:
                current_header = None
                current_seq = ""

                for line in f:
                    line = line.strip()
                    if line.startswith('#'):
                        continue
                    elif line.startswith('>'):
                        if current_seq:
                            sequences.append({
                                'header': current_header,
                                'sequence': current_seq,
                                'source': fasta_file.name,
                            })
                        current_header = line[1:]
                        current_seq = ""
                    else:
                        current_seq += line

                if current_seq:
                    sequences.append({
                        'header': current_header,
                        'sequence': current_seq,
                        'source': fasta_file.name,
                    })

    return sequences


def generate_prior_art_manifest(
    sequences: List[Dict],
    pipeline_results: List[Dict],
    working_dir: Path,
) -> Dict:
    """Generate the prior art manifest with cryptographic hashes."""

    manifest = {
        'manifest_version': '1.0',
        'pipeline': PIPELINE_NAME,
        'pipeline_version': PIPELINE_VERSION,
        'generated': datetime.now().isoformat(),
        'license': {
            'code': 'AGPL-3.0-or-later',
            'materials': 'OpenMTA',
            'documentation': 'CC-BY-SA-4.0',
        },
        'prior_art_declaration': (
            "The peptide sequences and design methodologies contained herein "
            "are hereby released into the public domain as PRIOR ART as of "
            f"{datetime.now().strftime('%B %d, %Y')}. This establishes a public "
            "record preventing subsequent patent claims on these specific "
            "sequences and the described design approaches."
        ),
        'pipeline_execution': {
            'stages': [r['stage'] for r in pipeline_results],
            'all_success': all(r['status'] == 'SUCCESS' for r in pipeline_results),
        },
        'sequences': [],
    }

    for seq_data in sequences:
        seq = seq_data['sequence']
        seq_hash = hashlib.sha256(seq.encode()).hexdigest()

        manifest['sequences'].append({
            'header': seq_data.get('header', ''),
            'sequence': seq,
            'length': len(seq),
            'sha256': seq_hash,
            'source_file': seq_data.get('source', ''),
        })

    # Calculate manifest hash
    manifest_content = json.dumps(manifest['sequences'], sort_keys=True)
    manifest['manifest_sha256'] = hashlib.sha256(manifest_content.encode()).hexdigest()

    # Save manifest
    manifest_file = working_dir / "PRIOR_ART_MANIFEST.json"
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\nPrior Art Manifest saved: {manifest_file}")
    print(f"Manifest SHA-256: {manifest['manifest_sha256']}")

    return manifest


def create_archive(working_dir: Path, manifest: Dict) -> str:
    """Create ZIP archive of all results."""

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_name = f"prolactinoma_pipeline_{timestamp}.zip"
    archive_path = working_dir / "results" / archive_name

    archive_path.parent.mkdir(exist_ok=True)

    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add manifest
        manifest_file = working_dir / "PRIOR_ART_MANIFEST.json"
        if manifest_file.exists():
            zf.write(manifest_file, "PRIOR_ART_MANIFEST.json")

        # Add structures
        structures_dir = working_dir / "structures"
        if structures_dir.exists():
            for f in structures_dir.glob("*"):
                zf.write(f, f"structures/{f.name}")

        # Add peptides
        peptides_dir = working_dir / "peptides"
        if peptides_dir.exists():
            for f in peptides_dir.glob("*"):
                zf.write(f, f"peptides/{f.name}")

        # Add thermodynamics
        thermo_dir = working_dir / "thermodynamics"
        if thermo_dir.exists():
            for f in thermo_dir.glob("*"):
                zf.write(f, f"thermodynamics/{f.name}")

        # Add target extraction results
        target_file = working_dir / "target_extraction_results.json"
        if target_file.exists():
            zf.write(target_file, "target_extraction_results.json")

    print(f"\nArchive created: {archive_path}")
    return str(archive_path)


# =============================================================================
# MAIN CONTROLLER
# =============================================================================

def run_pipeline() -> Dict:
    """Run the complete prolactinoma pipeline."""

    print("="*70)
    print(f"{PIPELINE_NAME}")
    print(f"Version: {PIPELINE_VERSION}")
    print("="*70)
    print(f"\nStarted: {datetime.now().isoformat()}")
    print("\nApplication: Prolactinoma (Benign Pituitary Tumor)")
    print("Goal: Design hyper-selective D2R agonist peptides")
    print("Mechanism: D2R activation → lactotroph apoptosis → tumor shrinkage")

    # Get working directory
    working_dir = Path(__file__).parent

    # Create results directory
    (working_dir / "results").mkdir(exist_ok=True)

    # Run all stages
    pipeline_results = []

    for stage in STAGES:
        result = run_stage(stage, working_dir)
        pipeline_results.append(result)

        if result['status'] not in ['SUCCESS', 'SKIPPED']:
            print(f"\nWARNING: Stage '{stage['name']}' did not complete successfully")
            print(f"Status: {result['status']}")
            if result['error']:
                print(f"Error: {result['error']}")

    # Collect sequences and generate manifest
    print("\n" + "="*70)
    print("GENERATING PRIOR ART MANIFEST")
    print("="*70)

    sequences = collect_peptide_sequences(working_dir)
    print(f"\nCollected {len(sequences)} peptide sequences")

    manifest = generate_prior_art_manifest(sequences, pipeline_results, working_dir)

    # Create archive
    print("\n" + "="*70)
    print("CREATING ARCHIVE")
    print("="*70)

    archive_path = create_archive(working_dir, manifest)

    # Final summary
    print("\n" + "="*70)
    print("PIPELINE COMPLETE")
    print("="*70)

    success_count = sum(1 for r in pipeline_results if r['status'] == 'SUCCESS')
    total_count = len(pipeline_results)

    print(f"\nStages completed: {success_count}/{total_count}")
    print(f"Peptides generated: {len(sequences)}")
    print(f"Archive: {archive_path}")
    print(f"Manifest hash: {manifest['manifest_sha256'][:32]}...")

    print("\n" + "="*70)
    print("PRIOR ART DECLARATION")
    print("="*70)
    print(f"""
The D2R-selective agonist peptide sequences generated by this pipeline
are hereby released as PRIOR ART as of {datetime.now().strftime('%B %d, %Y')}.

This establishes a public record preventing subsequent patent claims on:
1. The specific peptide sequences
2. The design methodology (pharmacophore-based cyclic peptide design)
3. The selectivity strategy (5-HT2B steric clash)

LICENSE: AGPL-3.0-or-later (code) + OpenMTA (materials) + CC-BY-SA-4.0 (docs)
""")

    return {
        'pipeline_results': pipeline_results,
        'manifest': manifest,
        'archive': archive_path,
        'sequences_count': len(sequences),
        'success': success_count == total_count,
    }


if __name__ == "__main__":
    results = run_pipeline()
