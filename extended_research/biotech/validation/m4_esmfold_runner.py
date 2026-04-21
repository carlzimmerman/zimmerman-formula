#!/usr/bin/env python3
"""
M4 ESMFold Structure Prediction Runner
======================================

Runs ESMFold on all peptide sequences to get REAL 3D structure predictions.
This converts our heuristic-generated sequences into actual structural data.

Uses Apple M4 Max GPU acceleration via MPS backend.

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026
"""

import torch
import esm
import json
import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional
import hashlib
import time

# Check for MPS (Apple Silicon) or CUDA
if torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
    print(f"Using Apple Silicon MPS acceleration")
elif torch.cuda.is_available():
    DEVICE = torch.device("cuda")
    print(f"Using CUDA GPU")
else:
    DEVICE = torch.device("cpu")
    print(f"Using CPU (slower)")


@dataclass
class StructurePrediction:
    """ESMFold structure prediction result."""
    peptide_id: str
    sequence: str
    length: int
    plddt_mean: float  # Confidence score (0-100)
    plddt_per_residue: List[float]
    pdb_string: str
    prediction_time_s: float
    sha256: str


def load_sequences_from_fasta(fasta_path: str) -> List[tuple]:
    """Load sequences from FASTA file."""
    sequences = []
    current_id = None
    current_seq = []

    with open(fasta_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_id is not None:
                    sequences.append((current_id, "".join(current_seq)))
                current_id = line[1:].split("|")[0]  # Get ID before first pipe
                current_seq = []
            else:
                current_seq.append(line)

        if current_id is not None:
            sequences.append((current_id, "".join(current_seq)))

    return sequences


def predict_structure(model, sequence: str, peptide_id: str) -> Optional[StructurePrediction]:
    """Predict 3D structure using ESMFold."""
    start_time = time.time()

    try:
        # ESMFold prediction
        with torch.no_grad():
            output = model.infer_pdb(sequence)

        # Parse pLDDT from output (it's in the B-factor column of PDB)
        plddt_values = []
        for line in output.split("\n"):
            if line.startswith("ATOM"):
                try:
                    # B-factor is columns 61-66 in PDB format
                    bfactor = float(line[60:66].strip())
                    plddt_values.append(bfactor)
                except (ValueError, IndexError):
                    continue

        # Get per-residue pLDDT (average over atoms per residue)
        # For simplicity, take unique values (one per CA atom)
        ca_plddt = []
        for line in output.split("\n"):
            if line.startswith("ATOM") and " CA " in line:
                try:
                    bfactor = float(line[60:66].strip())
                    ca_plddt.append(bfactor)
                except (ValueError, IndexError):
                    continue

        plddt_mean = sum(ca_plddt) / len(ca_plddt) if ca_plddt else 0.0

        elapsed = time.time() - start_time
        sha = hashlib.sha256(sequence.encode()).hexdigest()[:16]

        return StructurePrediction(
            peptide_id=peptide_id,
            sequence=sequence,
            length=len(sequence),
            plddt_mean=round(plddt_mean, 2),
            plddt_per_residue=[round(x, 2) for x in ca_plddt],
            pdb_string=output,
            prediction_time_s=round(elapsed, 3),
            sha256=sha,
        )

    except Exception as e:
        print(f"  ERROR predicting {peptide_id}: {e}")
        return None


def run_esmfold_on_fasta(fasta_path: str, output_dir: str, max_peptides: int = None):
    """Run ESMFold on all sequences in a FASTA file."""
    print(f"\n{'='*70}")
    print(f"ESMFold Structure Prediction")
    print(f"{'='*70}")
    print(f"Input: {fasta_path}")
    print(f"Device: {DEVICE}")
    print()

    # Load model
    print("Loading ESMFold model...")
    model = esm.pretrained.esmfold_v1()
    model = model.eval()

    # Move to device - ESMFold is large, may need CPU for some operations
    # For M4 Max with 64GB, should be fine
    try:
        model = model.to(DEVICE)
        print(f"Model loaded on {DEVICE}")
    except Exception as e:
        print(f"Could not load on {DEVICE}, falling back to CPU: {e}")
        model = model.to("cpu")

    # Set chunk size for long sequences
    model.set_chunk_size(128)

    # Load sequences
    sequences = load_sequences_from_fasta(fasta_path)
    print(f"Loaded {len(sequences)} sequences")

    if max_peptides:
        sequences = sequences[:max_peptides]
        print(f"Processing first {max_peptides} peptides")

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    pdb_dir = output_path / "pdb_structures"
    pdb_dir.mkdir(exist_ok=True)

    # Process sequences
    results = []
    total_time = 0

    for i, (pep_id, sequence) in enumerate(sequences):
        print(f"\n[{i+1}/{len(sequences)}] {pep_id} ({len(sequence)} aa)")

        # Skip very long sequences (ESMFold limit ~400 aa)
        if len(sequence) > 400:
            print(f"  Skipping - sequence too long ({len(sequence)} > 400)")
            continue

        result = predict_structure(model, sequence, pep_id)

        if result:
            results.append(result)
            total_time += result.prediction_time_s

            # Save individual PDB
            pdb_path = pdb_dir / f"{pep_id}.pdb"
            with open(pdb_path, "w") as f:
                f.write(result.pdb_string)

            # Quality assessment
            if result.plddt_mean > 90:
                quality = "EXCELLENT"
            elif result.plddt_mean > 70:
                quality = "GOOD"
            elif result.plddt_mean > 50:
                quality = "LOW"
            else:
                quality = "VERY LOW"

            print(f"  pLDDT: {result.plddt_mean:.1f} ({quality}) | Time: {result.prediction_time_s:.2f}s")

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Processed: {len(results)} peptides")
    print(f"Total time: {total_time:.1f}s")
    print(f"Avg time per peptide: {total_time/len(results):.2f}s" if results else "N/A")

    if results:
        avg_plddt = sum(r.plddt_mean for r in results) / len(results)
        high_conf = sum(1 for r in results if r.plddt_mean > 70)
        print(f"Average pLDDT: {avg_plddt:.1f}")
        print(f"High confidence (pLDDT > 70): {high_conf} ({100*high_conf/len(results):.1f}%)")

    # Save results JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fasta_name = Path(fasta_path).stem

    output_json = {
        "source_fasta": str(fasta_path),
        "timestamp": datetime.now().isoformat(),
        "device": str(DEVICE),
        "total_peptides": len(results),
        "total_time_s": round(total_time, 2),
        "average_plddt": round(avg_plddt, 2) if results else None,
        "predictions": [
            {
                "peptide_id": r.peptide_id,
                "sequence": r.sequence,
                "length": r.length,
                "plddt_mean": r.plddt_mean,
                "plddt_per_residue": r.plddt_per_residue,
                "prediction_time_s": r.prediction_time_s,
                "sha256": r.sha256,
                "pdb_file": f"pdb_structures/{r.peptide_id}.pdb",
            }
            for r in results
        ],
    }

    json_path = output_path / f"esmfold_results_{fasta_name}_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(output_json, f, indent=2)
    print(f"\nResults saved: {json_path}")

    print(f"\nPDB structures saved to: {pdb_dir}")

    return results


def run_all_fastas():
    """Run ESMFold on all FASTA files in the biotech directory."""
    base_dir = Path(__file__).parent.parent
    output_base = Path(__file__).parent / "esmfold_predictions"

    # Find all FASTA files
    fasta_files = list(base_dir.glob("**/*.fasta"))
    print(f"Found {len(fasta_files)} FASTA files")

    # Filter to main peptide files (not antibody VH/VL)
    peptide_fastas = [
        f for f in fasta_files
        if "peptide" in f.name.lower() or "binder" in f.name.lower() or "agonist" in f.name.lower()
    ]
    print(f"Peptide FASTA files: {len(peptide_fastas)}")

    all_results = []

    for fasta_path in peptide_fastas:
        # Create output subdirectory matching source structure
        rel_path = fasta_path.relative_to(base_dir)
        output_dir = output_base / rel_path.parent

        results = run_esmfold_on_fasta(str(fasta_path), str(output_dir), max_peptides=20)
        all_results.extend(results)

    print(f"\n{'='*70}")
    print(f"ALL PREDICTIONS COMPLETE")
    print(f"{'='*70}")
    print(f"Total peptides processed: {len(all_results)}")

    return all_results


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Run on specific FASTA file
        fasta_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "./esmfold_output"
        max_pep = int(sys.argv[3]) if len(sys.argv) > 3 else None
        run_esmfold_on_fasta(fasta_path, output_dir, max_pep)
    else:
        # Run on all FASTA files
        run_all_fastas()
