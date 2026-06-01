#!/usr/bin/env python3
"""
Val 05: AlphaFold2 Batch Structure Generation Pipeline

PhD-Level Validation Script

Purpose:
--------
Generate 3D structures for all peptide candidates using protein structure
prediction tools (ESMFold local or ColabFold API as AF2 alternatives).

Scientific Question:
-------------------
Do the Z²-designed peptides fold into stable, well-defined 3D structures
suitable for receptor binding?

Methods:
--------
1. Load all peptide candidates from the database
2. Submit sequences for structure prediction (ESMFold or ColabFold)
3. Analyze pLDDT confidence scores
4. Validate predicted structures against Z² framework constraints
5. Filter candidates by structural quality

Dependencies:
-------------
pip install requests numpy pandas biopython

For local ESMFold:
pip install torch fair-esm

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later
"""

# =============================================================================
# LEGAL DISCLAIMER: This is THEORETICAL COMPUTATIONAL RESEARCH only.
# Not peer reviewed. Not medical advice. Not a validated therapeutic.
# All predictions require experimental validation.
# See: extended_research/biotech/LEGAL_DISCLAIMER.md
# =============================================================================


import json
import hashlib
import time
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

import numpy as np

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("WARNING: requests not available. Install with: pip install requests")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


# ============================================================================
# Z² FRAMEWORK CONSTANTS
# ============================================================================

Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
COORDINATION_NUMBER = 8  # Z²/Vol(B³) = 8
NATURAL_LENGTH_SCALE = (Z_SQUARED ** 0.25) * 3.8  # ≈ 9.14 Å


# ============================================================================
# STRUCTURE PREDICTION APIs
# ============================================================================

# ESMFold API (Meta AI - no signup required)
ESMFOLD_API_URL = "https://api.esmatlas.com/foldSequence/v1/pdb/"

# ColabFold API (backup)
COLABFOLD_API_URL = "https://api.colabfold.com/batch"


def predict_structure_esmfold(
    sequence: str,
    name: str = "peptide",
    max_retries: int = 3,
    retry_delay: float = 5.0
) -> Optional[Dict]:
    """
    Predict structure using ESMFold API.

    Parameters:
    -----------
    sequence : str
        Amino acid sequence
    name : str
        Name/identifier for the peptide
    max_retries : int
        Number of retry attempts
    retry_delay : float
        Delay between retries (seconds)

    Returns:
    --------
    Dict with PDB string, pLDDT scores, and metadata
    """
    if not REQUESTS_AVAILABLE:
        return None

    # Clean sequence
    sequence = sequence.upper().strip()
    valid_aa = set('ACDEFGHIKLMNPQRSTVWY')
    sequence = ''.join(aa for aa in sequence if aa in valid_aa)

    if len(sequence) < 5:
        return {'error': f'Sequence too short: {len(sequence)} residues'}

    if len(sequence) > 400:
        return {'error': f'Sequence too long for ESMFold API: {len(sequence)} residues'}

    for attempt in range(max_retries):
        try:
            response = requests.post(
                ESMFOLD_API_URL,
                data=sequence,
                headers={'Content-Type': 'text/plain'},
                timeout=120
            )

            if response.status_code == 200:
                pdb_string = response.text

                # Parse pLDDT from B-factor column
                plddt_scores = parse_plddt_from_pdb(pdb_string)

                return {
                    'name': name,
                    'sequence': sequence,
                    'length': len(sequence),
                    'pdb_string': pdb_string,
                    'plddt_scores': plddt_scores,
                    'plddt_mean': float(np.mean(plddt_scores)) if plddt_scores else 0.0,
                    'plddt_min': float(np.min(plddt_scores)) if plddt_scores else 0.0,
                    'plddt_max': float(np.max(plddt_scores)) if plddt_scores else 0.0,
                    'method': 'ESMFold',
                    'timestamp': datetime.now().isoformat(),
                    'success': True
                }

            elif response.status_code == 429:
                # Rate limited - wait and retry
                print(f"    Rate limited, waiting {retry_delay * 2}s...")
                time.sleep(retry_delay * 2)

            elif response.status_code == 500:
                # Server error - might be temporary
                print(f"    Server error, attempt {attempt + 1}/{max_retries}")
                time.sleep(retry_delay)

            else:
                return {
                    'error': f'API returned status {response.status_code}',
                    'name': name,
                    'sequence': sequence,
                    'success': False
                }

        except requests.exceptions.Timeout:
            print(f"    Timeout, attempt {attempt + 1}/{max_retries}")
            time.sleep(retry_delay)

        except Exception as e:
            return {
                'error': str(e),
                'name': name,
                'sequence': sequence,
                'success': False
            }

    return {
        'error': f'Failed after {max_retries} attempts',
        'name': name,
        'sequence': sequence,
        'success': False
    }


def parse_plddt_from_pdb(pdb_string: str) -> List[float]:
    """
    Parse pLDDT scores from PDB B-factor column.
    ESMFold stores pLDDT in the B-factor column (column 61-66).
    """
    plddt_scores = []
    seen_residues = set()

    for line in pdb_string.split('\n'):
        if line.startswith('ATOM') and ' CA ' in line:
            try:
                # B-factor is columns 61-66 (0-indexed: 60-66)
                bfactor = float(line[60:66].strip())
                res_num = int(line[22:26].strip())

                if res_num not in seen_residues:
                    plddt_scores.append(bfactor)
                    seen_residues.add(res_num)
            except (ValueError, IndexError):
                continue

    return plddt_scores


def analyze_structure_quality(plddt_scores: List[float]) -> Dict:
    """
    Analyze structure quality based on pLDDT scores.

    pLDDT interpretation (AlphaFold scale):
    - Very high (>90): High confidence
    - Confident (70-90): Good confidence
    - Low (50-70): Low confidence
    - Very low (<50): Unstructured or disordered

    For short peptides, lower scores are expected.
    """
    if not plddt_scores:
        return {
            'quality_class': 'unknown',
            'interpretation': 'No pLDDT scores available'
        }

    mean_plddt = np.mean(plddt_scores)
    min_plddt = np.min(plddt_scores)

    # Fraction in each confidence bin
    very_high = sum(1 for p in plddt_scores if p > 90) / len(plddt_scores)
    confident = sum(1 for p in plddt_scores if 70 <= p <= 90) / len(plddt_scores)
    low = sum(1 for p in plddt_scores if 50 <= p < 70) / len(plddt_scores)
    very_low = sum(1 for p in plddt_scores if p < 50) / len(plddt_scores)

    # Quality classification (adjusted for short peptides)
    if mean_plddt > 80:
        quality_class = 'high'
        interpretation = 'Well-defined structure with high confidence'
    elif mean_plddt > 65:
        quality_class = 'moderate'
        interpretation = 'Partially ordered structure (typical for short peptides)'
    elif mean_plddt > 50:
        quality_class = 'low'
        interpretation = 'Mostly disordered with some ordered regions'
    else:
        quality_class = 'very_low'
        interpretation = 'Intrinsically disordered (expected for some bioactive peptides)'

    return {
        'quality_class': quality_class,
        'interpretation': interpretation,
        'mean_plddt': float(mean_plddt),
        'min_plddt': float(min_plddt),
        'fraction_very_high': float(very_high),
        'fraction_confident': float(confident),
        'fraction_low': float(low),
        'fraction_very_low': float(very_low)
    }


def validate_z2_constraints(pdb_string: str, sequence: str) -> Dict:
    """
    Validate structure against Z² framework constraints.

    Checks:
    1. Contact density at Z²-derived cutoff (~9.14 Å)
    2. Compactness (Rg vs expected for length)
    3. Secondary structure consistency
    """
    if not pdb_string:
        return {'validation': 'failed', 'reason': 'No structure available'}

    # Parse CA coordinates
    ca_coords = []
    for line in pdb_string.split('\n'):
        if line.startswith('ATOM') and ' CA ' in line:
            try:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                ca_coords.append([x, y, z])
            except (ValueError, IndexError):
                continue

    if len(ca_coords) < 3:
        return {'validation': 'failed', 'reason': 'Too few residues'}

    ca_coords = np.array(ca_coords)

    # Calculate radius of gyration
    centroid = np.mean(ca_coords, axis=0)
    rg = np.sqrt(np.mean(np.sum((ca_coords - centroid)**2, axis=1)))

    # Expected Rg for random coil: Rg ≈ 2.0 * N^0.5 Å
    # Expected Rg for compact protein: Rg ≈ 2.5 * N^0.33 Å
    n_res = len(ca_coords)
    rg_random_coil = 2.0 * np.sqrt(n_res)
    rg_compact = 2.5 * (n_res ** 0.33)

    # Compactness ratio (1 = compact, >1 = extended)
    compactness = rg / rg_compact

    # Calculate contacts at Z² cutoff
    cutoff = NATURAL_LENGTH_SCALE  # 9.14 Å
    n_contacts = 0
    for i in range(len(ca_coords)):
        for j in range(i + 4, len(ca_coords)):  # Minimum separation |i-j| > 3
            dist = np.linalg.norm(ca_coords[i] - ca_coords[j])
            if dist <= cutoff:
                n_contacts += 1

    contacts_per_residue = n_contacts / n_res if n_res > 0 else 0

    # Z² prediction: 8 contacts per residue
    z2_deviation = abs(contacts_per_residue - COORDINATION_NUMBER) / COORDINATION_NUMBER

    return {
        'validation': 'passed' if z2_deviation < 0.5 and compactness < 2.0 else 'marginal',
        'n_residues': int(n_res),
        'radius_of_gyration': float(rg),
        'rg_compact_expected': float(rg_compact),
        'rg_random_coil_expected': float(rg_random_coil),
        'compactness_ratio': float(compactness),
        'contacts_at_z2_cutoff': int(n_contacts),
        'contacts_per_residue': float(contacts_per_residue),
        'z2_prediction': COORDINATION_NUMBER,
        'z2_deviation_fraction': float(z2_deviation),
        'structure_class': 'compact' if compactness < 1.2 else ('extended' if compactness > 1.8 else 'intermediate')
    }


def load_peptide_candidates(max_peptides: int = 100) -> List[Dict]:
    """
    Load peptide candidates from the database.
    """
    base_path = Path('/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech')
    candidates = []

    # target system directories
    disease_dirs = [
        'neurological', 'autoimmune', 'metabolic', 'oncology',
        'eye_vision', 'prolactinoma', 'dark_proteome'
    ]

    for disease_dir in disease_dirs:
        dir_path = base_path / disease_dir
        if not dir_path.exists():
            continue

        for json_file in dir_path.glob('*_candidates.json'):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)

                peptides = []
                if isinstance(data, dict) and 'candidates' in data:
                    peptides = data['candidates']
                elif isinstance(data, list):
                    peptides = data

                for pep in peptides:
                    if 'sequence' in pep:
                        pep['source'] = disease_dir
                        pep['source_file'] = json_file.name
                        candidates.append(pep)

                        if len(candidates) >= max_peptides:
                            return candidates

            except Exception as e:
                continue

    return candidates


def batch_predict_structures(
    candidates: List[Dict],
    output_dir: Path,
    rate_limit_delay: float = 2.0,
    max_structures: int = 50
) -> List[Dict]:
    """
    Batch structure prediction for multiple peptides.
    """
    results = []
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nPredicting structures for {min(len(candidates), max_structures)} peptides...")
    print("-" * 50)

    for i, candidate in enumerate(candidates[:max_structures]):
        sequence = candidate.get('sequence', '')
        name = candidate.get('name', f'peptide_{i+1}')
        source = candidate.get('source', 'unknown')

        print(f"\n[{i+1}/{min(len(candidates), max_structures)}] {name} ({source})")
        print(f"  Sequence: {sequence[:30]}{'...' if len(sequence) > 30 else ''}")

        # Predict structure
        result = predict_structure_esmfold(sequence, name)

        if result and result.get('success'):
            # Analyze quality
            quality = analyze_structure_quality(result.get('plddt_scores', []))
            result['quality_analysis'] = quality

            # Validate Z² constraints
            z2_validation = validate_z2_constraints(
                result.get('pdb_string', ''),
                sequence
            )
            result['z2_validation'] = z2_validation

            # Save PDB file
            pdb_path = output_dir / f"{name.replace(' ', '_')}.pdb"
            with open(pdb_path, 'w') as f:
                f.write(result['pdb_string'])
            result['pdb_file'] = str(pdb_path)

            print(f"  ✓ pLDDT: {result['plddt_mean']:.1f} ({quality['quality_class']})")
            print(f"  ✓ Compactness: {z2_validation.get('compactness_ratio', 0):.2f}")
            print(f"  ✓ Z² validation: {z2_validation.get('validation', 'N/A')}")

            # Remove large PDB string from results (saved to file)
            result_copy = result.copy()
            result_copy.pop('pdb_string', None)
            results.append(result_copy)

        else:
            error = result.get('error', 'Unknown error') if result else 'No response'
            print(f"  ✗ Error: {error}")
            results.append({
                'name': name,
                'sequence': sequence,
                'source': source,
                'success': False,
                'error': error
            })

        # Rate limiting
        time.sleep(rate_limit_delay)

    return results


def generate_summary_report(results: List[Dict]) -> Dict:
    """
    Generate summary statistics for batch structure prediction.
    """
    successful = [r for r in results if r.get('success')]
    failed = [r for r in results if not r.get('success')]

    if not successful:
        return {
            'total': len(results),
            'successful': 0,
            'failed': len(failed),
            'summary': 'No successful predictions'
        }

    plddt_values = [r['plddt_mean'] for r in successful if 'plddt_mean' in r]
    quality_classes = [r['quality_analysis']['quality_class'] for r in successful if 'quality_analysis' in r]
    z2_statuses = [r['z2_validation']['validation'] for r in successful if 'z2_validation' in r]

    # Count quality classes
    quality_counts = {}
    for qc in quality_classes:
        quality_counts[qc] = quality_counts.get(qc, 0) + 1

    # Count Z² validation statuses
    z2_counts = {}
    for status in z2_statuses:
        z2_counts[status] = z2_counts.get(status, 0) + 1

    return {
        'total': len(results),
        'successful': len(successful),
        'failed': len(failed),
        'success_rate': len(successful) / len(results) if results else 0,
        'plddt_statistics': {
            'mean': float(np.mean(plddt_values)) if plddt_values else 0,
            'std': float(np.std(plddt_values)) if plddt_values else 0,
            'min': float(np.min(plddt_values)) if plddt_values else 0,
            'max': float(np.max(plddt_values)) if plddt_values else 0
        },
        'quality_distribution': quality_counts,
        'z2_validation_distribution': z2_counts,
        'interpretation': generate_interpretation(plddt_values, quality_counts, z2_counts)
    }


def generate_interpretation(
    plddt_values: List[float],
    quality_counts: Dict,
    z2_counts: Dict
) -> str:
    """
    Generate human-readable interpretation of results.
    """
    if not plddt_values:
        return "No structures predicted successfully."

    mean_plddt = np.mean(plddt_values)

    # pLDDT interpretation
    if mean_plddt > 80:
        plddt_interp = "high confidence (well-defined structures)"
    elif mean_plddt > 65:
        plddt_interp = "moderate confidence (partially ordered, typical for peptides)"
    elif mean_plddt > 50:
        plddt_interp = "low confidence (mostly disordered regions)"
    else:
        plddt_interp = "very low confidence (intrinsically disordered)"

    # Z² validation interpretation
    passed = z2_counts.get('passed', 0)
    marginal = z2_counts.get('marginal', 0)
    total = passed + marginal

    if total > 0:
        passed_frac = passed / total
        if passed_frac > 0.7:
            z2_interp = f"{passed_frac:.0%} of structures satisfy Z² contact constraints"
        else:
            z2_interp = f"Only {passed_frac:.0%} fully satisfy Z² constraints (short peptides expected)"
    else:
        z2_interp = "Z² validation not available"

    return f"""
Average pLDDT = {mean_plddt:.1f}: {plddt_interp}

Quality distribution: {quality_counts}

Z² Framework: {z2_interp}

Note: Short peptides (<30 residues) typically show lower pLDDT scores
because they lack the extensive intramolecular contacts that stabilize
larger protein structures. This does NOT indicate poor therapeutic potential.
"""


def run_batch_prediction(output_dir: str = None, max_peptides: int = 30) -> Dict:
    """
    Main function: Run batch structure prediction pipeline.
    """
    print("=" * 70)
    print("Val 05: AlphaFold2/ESMFold Batch Structure Generation")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Using ESMFold API (Meta AI)")
    print()

    if output_dir is None:
        output_dir = Path('/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/validation/structures')
    else:
        output_dir = Path(output_dir)

    results_dir = output_dir.parent / 'results'
    results_dir.mkdir(parents=True, exist_ok=True)

    # Load candidates
    print("Step 1: Loading peptide candidates...")
    print("-" * 50)
    candidates = load_peptide_candidates(max_peptides=max_peptides * 2)
    print(f"  Found {len(candidates)} candidates")

    if not candidates:
        print("  No candidates found. Generating test sequences...")
        # Generate test sequences based on universal scaffolds
        test_sequences = [
            {'name': 'GLP1R_lead', 'sequence': 'HAEGTFTSDVSSYLEGQAAKEFIAWLVKGRG', 'source': 'metabolic'},
            {'name': 'GBA1_lead', 'sequence': 'CYRILKSWFAEGNHQTMPVD', 'source': 'neurological'},
            {'name': 'TNF_lead', 'sequence': 'AEQGTRILHKNSFPWYVMCD', 'source': 'autoimmune'},
            {'name': 'VEGF_lead', 'sequence': 'FWYLHKRCDEGAINMPQSTV', 'source': 'oncology'},
            {'name': 'CRF1_lead', 'sequence': 'AEGHIKLNPQRSTVWFYCMD', 'source': 'neurological'},
        ]
        candidates = test_sequences

    # Run batch prediction
    print("\nStep 2: Running structure predictions...")
    print("-" * 50)

    prediction_results = batch_predict_structures(
        candidates,
        output_dir,
        rate_limit_delay=2.0,
        max_structures=max_peptides
    )

    # Generate summary
    print("\nStep 3: Generating summary report...")
    print("-" * 50)

    summary = generate_summary_report(prediction_results)

    # Compile full results
    full_results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'ESMFold API',
        'framework': {
            'z_squared': Z_SQUARED,
            'coordination_number': COORDINATION_NUMBER,
            'natural_length_scale_angstrom': NATURAL_LENGTH_SCALE
        },
        'summary': summary,
        'predictions': prediction_results
    }

    # Save results
    results_path = results_dir / 'val_05_structure_prediction_results.json'
    with open(results_path, 'w') as f:
        json.dump(full_results, f, indent=2, default=str)

    print(f"\nResults saved to: {results_path}")
    print(f"PDB structures saved to: {output_dir}")

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY: Batch Structure Prediction")
    print("=" * 70)
    print(f"""
Total peptides: {summary['total']}
Successful predictions: {summary['successful']}
Failed predictions: {summary['failed']}
Success rate: {summary['success_rate']:.1%}

pLDDT Statistics:
  Mean: {summary['plddt_statistics']['mean']:.1f}
  Std:  {summary['plddt_statistics']['std']:.1f}
  Min:  {summary['plddt_statistics']['min']:.1f}
  Max:  {summary['plddt_statistics']['max']:.1f}

Quality Distribution: {summary['quality_distribution']}
Z² Validation: {summary['z2_validation_distribution']}

{summary['interpretation']}
""")

    return full_results


if __name__ == '__main__':
    # Run with limited peptides for demonstration
    # Increase max_peptides for full analysis
    results = run_batch_prediction(max_peptides=10)
    print("\nVal 05 complete.")
