#!/usr/bin/env python3
"""
test_designs_esmfold.py - Test Z² Designs with ESMFold Structure Prediction

Validates designed peptides by:
1. Predicting 3D structure with ESMFold
2. Measuring pLDDT confidence scores
3. Analyzing aromatic sidechain geometry
4. Verifying Z² distance potential

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import math
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime


# =============================================================================
# CONSTANTS
# =============================================================================

Z2_DISTANCE = 6.015152508891966  # Å
ESMFOLD_API = "https://api.esmatlas.com/foldSequence/v1/pdb/"

# pLDDT quality thresholds (ESMFold uses 0-1 scale, not 0-100)
PLDDT_EXCELLENT = 0.90
PLDDT_GOOD = 0.70
PLDDT_PASS = 0.50


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ESMFoldResult:
    """Result from ESMFold prediction."""
    sequence: str
    design_id: str

    # Structure prediction
    pdb_content: str
    prediction_success: bool

    # Quality metrics
    plddt_mean: float
    plddt_min: float
    plddt_max: float
    plddt_per_residue: List[float]

    # Aromatic analysis
    n_aromatics: int
    aromatic_plddt: float  # Average pLDDT of aromatic residues
    aromatic_positions: List[int]

    # Z² geometry in predicted structure
    aromatic_sidechain_lengths: List[float]
    z2_geometry_score: float

    # Overall assessment
    quality: str  # EXCELLENT, GOOD, PASS, FAIL
    recommendation: str


@dataclass
class TestReport:
    """Complete test report for a set of designs."""
    target_uniprot: str
    timestamp: str
    n_designs_tested: int
    n_passed: int
    n_failed: int

    results: List[ESMFoldResult]
    best_result: Optional[ESMFoldResult]

    summary: str


# =============================================================================
# ESMFOLD API
# =============================================================================

def predict_structure_esmfold(sequence: str, design_id: str) -> ESMFoldResult:
    """Predict structure using ESMFold API.

    API: https://api.esmatlas.com/foldSequence/v1/pdb/
    """
    print(f"    Predicting {design_id}: {sequence}...")

    try:
        # ESMFold API request
        data = sequence.encode('utf-8')
        request = urllib.request.Request(
            ESMFOLD_API,
            data=data,
            headers={
                'Content-Type': 'text/plain',
                'Accept': 'application/json'
            }
        )

        with urllib.request.urlopen(request, timeout=60) as response:
            pdb_content = response.read().decode('utf-8')

        # Parse PDB for pLDDT scores (in B-factor column)
        plddt_scores = parse_plddt_from_pdb(pdb_content)

        if not plddt_scores:
            return create_failed_result(sequence, design_id, "No pLDDT scores parsed")

        # Calculate metrics
        plddt_mean = sum(plddt_scores) / len(plddt_scores)
        plddt_min = min(plddt_scores)
        plddt_max = max(plddt_scores)

        # Find aromatic positions and their pLDDT
        aromatics = ['W', 'Y', 'F', 'H']
        aromatic_positions = [i for i, aa in enumerate(sequence) if aa in aromatics]
        aromatic_plddt_values = [plddt_scores[i] for i in aromatic_positions if i < len(plddt_scores)]
        aromatic_plddt = sum(aromatic_plddt_values) / len(aromatic_plddt_values) if aromatic_plddt_values else 0

        # Analyze aromatic sidechain geometry
        sidechain_lengths = analyze_aromatic_geometry(pdb_content, sequence)
        z2_score = calculate_z2_geometry_score(sidechain_lengths)

        # Determine quality
        if plddt_mean >= PLDDT_EXCELLENT:
            quality = "EXCELLENT"
            recommendation = "High confidence structure - proceed to docking"
        elif plddt_mean >= PLDDT_GOOD:
            quality = "GOOD"
            recommendation = "Good structure - suitable for further analysis"
        elif plddt_mean >= PLDDT_PASS:
            quality = "PASS"
            recommendation = "Moderate confidence - may need optimization"
        else:
            quality = "FAIL"
            recommendation = "Low confidence - redesign recommended"

        return ESMFoldResult(
            sequence=sequence,
            design_id=design_id,
            pdb_content=pdb_content,
            prediction_success=True,
            plddt_mean=plddt_mean,
            plddt_min=plddt_min,
            plddt_max=plddt_max,
            plddt_per_residue=plddt_scores,
            n_aromatics=len(aromatic_positions),
            aromatic_plddt=aromatic_plddt,
            aromatic_positions=aromatic_positions,
            aromatic_sidechain_lengths=sidechain_lengths,
            z2_geometry_score=z2_score,
            quality=quality,
            recommendation=recommendation
        )

    except urllib.error.HTTPError as e:
        print(f"      HTTP error: {e.code}")
        return create_failed_result(sequence, design_id, f"HTTP {e.code}")
    except urllib.error.URLError as e:
        print(f"      Connection error: {e}")
        return create_failed_result(sequence, design_id, str(e))
    except Exception as e:
        print(f"      Error: {e}")
        return create_failed_result(sequence, design_id, str(e))


def create_failed_result(sequence: str, design_id: str, error: str) -> ESMFoldResult:
    """Create a failed result."""
    return ESMFoldResult(
        sequence=sequence,
        design_id=design_id,
        pdb_content="",
        prediction_success=False,
        plddt_mean=0.0,
        plddt_min=0.0,
        plddt_max=0.0,
        plddt_per_residue=[],
        n_aromatics=0,
        aromatic_plddt=0.0,
        aromatic_positions=[],
        aromatic_sidechain_lengths=[],
        z2_geometry_score=0.0,
        quality="FAIL",
        recommendation=f"Prediction failed: {error}"
    )


def parse_plddt_from_pdb(pdb_content: str) -> List[float]:
    """Parse pLDDT scores from PDB B-factor column."""
    plddt_scores = []
    seen_residues = set()

    for line in pdb_content.split('\n'):
        if line.startswith('ATOM') and line[12:16].strip() == 'CA':
            try:
                resseq = int(line[22:26].strip())
                if resseq not in seen_residues:
                    bfactor = float(line[60:66].strip())
                    plddt_scores.append(bfactor)
                    seen_residues.add(resseq)
            except (ValueError, IndexError):
                continue

    return plddt_scores


def analyze_aromatic_geometry(pdb_content: str, sequence: str) -> List[float]:
    """Analyze aromatic sidechain geometry in predicted structure."""
    atoms = {}

    for line in pdb_content.split('\n'):
        if line.startswith('ATOM'):
            try:
                atom_name = line[12:16].strip()
                resseq = int(line[22:26].strip())
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])

                key = (resseq, atom_name)
                atoms[key] = (x, y, z)
            except (ValueError, IndexError):
                continue

    # Calculate CA to sidechain terminal distances for aromatics
    sidechain_lengths = []
    aromatics = ['W', 'Y', 'F', 'H']

    # Aromatic terminal atoms
    terminal_atoms = {
        'W': ['CZ2', 'CZ3', 'CH2'],
        'Y': ['CZ', 'OH'],
        'F': ['CZ'],
        'H': ['CE1', 'NE2']
    }

    for i, aa in enumerate(sequence):
        if aa in aromatics:
            resseq = i + 1  # 1-indexed
            ca_key = (resseq, 'CA')

            if ca_key not in atoms:
                continue

            ca_pos = atoms[ca_key]

            # Find terminal atom
            for term_atom in terminal_atoms.get(aa, []):
                term_key = (resseq, term_atom)
                if term_key in atoms:
                    term_pos = atoms[term_key]
                    dist = math.sqrt(
                        (ca_pos[0] - term_pos[0])**2 +
                        (ca_pos[1] - term_pos[1])**2 +
                        (ca_pos[2] - term_pos[2])**2
                    )
                    sidechain_lengths.append(dist)
                    break

    return sidechain_lengths


def calculate_z2_geometry_score(sidechain_lengths: List[float]) -> float:
    """Calculate how well aromatic sidechains could reach Z² distance."""
    if not sidechain_lengths:
        return 0.0

    # Aromatic sidechains should be ~5-6 Å to potentially reach Z² distance
    # with proper positioning
    target_length = 5.5  # Å - ideal sidechain length for Z² contact

    scores = []
    for length in sidechain_lengths:
        # Score based on how close to ideal length
        deviation = abs(length - target_length)
        score = max(0, 100 - deviation * 20)
        scores.append(score)

    return sum(scores) / len(scores)


# =============================================================================
# TEST RUNNER
# =============================================================================

def load_designs(design_file: Path) -> List[Dict]:
    """Load designs from JSON file."""
    with open(design_file, 'r') as f:
        data = json.load(f)
    return data.get('designs', [])


def test_designs(
    designs: List[Dict],
    target_uniprot: str,
    output_dir: Path,
    max_designs: int = 10,
    delay_seconds: float = 1.0
) -> TestReport:
    """Test designs with ESMFold."""

    print("\n" + "="*70)
    print("ESMFOLD STRUCTURE PREDICTION TEST")
    print("="*70)
    print(f"    Target: {target_uniprot}")
    print(f"    Designs to test: {min(len(designs), max_designs)}")
    print(f"    ESMFold API: {ESMFOLD_API}")

    results = []

    for i, design in enumerate(designs[:max_designs]):
        sequence = design.get('sequence', '')
        design_id = design.get('id', f"Design-{i+1}")

        result = predict_structure_esmfold(sequence, design_id)
        results.append(result)

        # Print progress
        status = "✓" if result.quality in ["EXCELLENT", "GOOD", "PASS"] else "✗"
        print(f"      {status} pLDDT: {result.plddt_mean:.1f} ({result.quality})")

        # Save PDB if successful
        if result.prediction_success and result.pdb_content:
            pdb_dir = output_dir / "predicted_structures"
            pdb_dir.mkdir(parents=True, exist_ok=True)
            pdb_file = pdb_dir / f"{design_id}.pdb"
            with open(pdb_file, 'w') as f:
                f.write(result.pdb_content)

        # Rate limiting
        if i < len(designs) - 1:
            time.sleep(delay_seconds)

    # Summary
    n_passed = sum(1 for r in results if r.quality in ["EXCELLENT", "GOOD", "PASS"])
    n_failed = len(results) - n_passed

    # Find best result
    passed_results = [r for r in results if r.prediction_success]
    best_result = max(passed_results, key=lambda r: r.plddt_mean) if passed_results else None

    # Generate summary
    if best_result and best_result.plddt_mean >= PLDDT_GOOD:
        summary = f"SUCCESS: {n_passed}/{len(results)} designs passed. Best pLDDT: {best_result.plddt_mean:.1f}"
    elif n_passed > 0:
        summary = f"PARTIAL: {n_passed}/{len(results)} designs passed. Consider optimization."
    else:
        summary = f"NEEDS WORK: All designs need optimization."

    report = TestReport(
        target_uniprot=target_uniprot,
        timestamp=datetime.now().isoformat(),
        n_designs_tested=len(results),
        n_passed=n_passed,
        n_failed=n_failed,
        results=results,
        best_result=best_result,
        summary=summary
    )

    return report


def print_report(report: TestReport) -> None:
    """Print test report."""
    print(f"\n{'='*70}")
    print("TEST RESULTS")
    print(f"{'='*70}")

    print(f"\n    Designs tested: {report.n_designs_tested}")
    print(f"    Passed: {report.n_passed}")
    print(f"    Failed: {report.n_failed}")
    print(f"    Pass rate: {report.n_passed/report.n_designs_tested*100:.1f}%")

    print(f"\n    RESULTS BY DESIGN:")
    print(f"    {'─'*60}")
    print(f"    {'ID':<12} {'Sequence':<14} {'pLDDT':<8} {'Arom pLDDT':<10} {'Quality'}")
    print(f"    {'-'*60}")

    for r in sorted(report.results, key=lambda x: -x.plddt_mean):
        print(f"    {r.design_id:<12} {r.sequence:<14} {r.plddt_mean:>6.1f}   {r.aromatic_plddt:>8.1f}   {r.quality}")

    if report.best_result:
        print(f"\n    BEST DESIGN:")
        print(f"    {'─'*50}")
        print(f"    ID: {report.best_result.design_id}")
        print(f"    Sequence: {report.best_result.sequence}")
        print(f"    pLDDT: {report.best_result.plddt_mean:.1f} (range: {report.best_result.plddt_min:.1f}-{report.best_result.plddt_max:.1f})")
        print(f"    Aromatics: {report.best_result.n_aromatics} (avg pLDDT: {report.best_result.aromatic_plddt:.1f})")
        print(f"    Z² Geometry Score: {report.best_result.z2_geometry_score:.1f}")
        print(f"    Quality: {report.best_result.quality}")
        print(f"    Recommendation: {report.best_result.recommendation}")

    print(f"\n    SUMMARY: {report.summary}")
    print(f"{'='*70}\n")


def save_report(report: TestReport, output_dir: Path) -> None:
    """Save test report to JSON."""
    output_file = output_dir / f"esmfold_test_{report.target_uniprot}.json"

    data = {
        'target_uniprot': report.target_uniprot,
        'timestamp': report.timestamp,
        'n_tested': report.n_designs_tested,
        'n_passed': report.n_passed,
        'n_failed': report.n_failed,
        'summary': report.summary,
        'results': [
            {
                'design_id': r.design_id,
                'sequence': r.sequence,
                'plddt_mean': r.plddt_mean,
                'plddt_min': r.plddt_min,
                'plddt_max': r.plddt_max,
                'n_aromatics': r.n_aromatics,
                'aromatic_plddt': r.aromatic_plddt,
                'z2_geometry_score': r.z2_geometry_score,
                'quality': r.quality,
                'recommendation': r.recommendation
            }
            for r in report.results
        ]
    }

    if report.best_result:
        data['best_design'] = {
            'id': report.best_result.design_id,
            'sequence': report.best_result.sequence,
            'plddt_mean': report.best_result.plddt_mean
        }

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"    Saved: {output_file}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Test Z² designs with ESMFold."""
    import argparse

    parser = argparse.ArgumentParser(description="Test Z² Designs with ESMFold")
    parser.add_argument("--designs", type=Path, required=True, help="Path to designs JSON")
    parser.add_argument("--uniprot", required=True, help="Target UniProt ID")
    parser.add_argument("--output", type=Path, help="Output directory")
    parser.add_argument("--max-designs", type=int, default=10, help="Max designs to test")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between API calls")
    args = parser.parse_args()

    output_dir = args.output or Path(__file__).parent.parent / "esmfold_tests"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load designs
    designs = load_designs(args.designs)

    if not designs:
        print("No designs found in file")
        return

    # Run tests
    report = test_designs(
        designs=designs,
        target_uniprot=args.uniprot,
        output_dir=output_dir,
        max_designs=args.max_designs,
        delay_seconds=args.delay
    )

    # Print and save
    print_report(report)
    save_report(report, output_dir)

    return report


if __name__ == "__main__":
    main()
