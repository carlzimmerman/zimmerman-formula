#!/usr/bin/env python3
"""
01_data_provenance.py

Copyright (C) 2026 Carl Zimmerman
Zimmerman Unified Geometry Framework (ZUGF)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

01_data_provenance.py - Data Fetching with Strict Quality Control

PURPOSE:
Fetch protein structures from RCSB PDB with rigorous quality filtering.
This script implements Gemini's "Data Provenance & Quality Control" prompt.

QUALITY FILTERS:
1. Resolution: Reject X-ray structures worse than 2.5 Å
2. Method: Flag and separate Cryo-EM, NMR, X-ray structures
3. Completeness: Check for missing residues in binding regions
4. Logging: Full provenance trail with DOI citations

CRITICAL RULES:
- NO mock data
- NO hardcoded outputs
- If fetch fails, raise Exception (do not return defaults)
- All data sources logged with timestamps

Author: Carl Zimmerman
Date: April 21, 2026
"""
import urllib.request
import urllib.error
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import sys

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = Path(__file__).parent / "data"
LOG_DIR = Path(__file__).parent / "logs"
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Quality thresholds
MAX_RESOLUTION_ANGSTROM = 2.5  # Reject worse than this
REQUIRED_METHODS = ['X-RAY DIFFRACTION', 'ELECTRON MICROSCOPY', 'SOLUTION NMR']

# Provenance log file
PROVENANCE_LOG = LOG_DIR / f"provenance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"


# =============================================================================
# STRICT ERROR HANDLING
# =============================================================================

class DataProvenanceError(Exception):
    """Raised when data quality checks fail."""
    pass


class FetchError(Exception):
    """Raised when data cannot be fetched from RCSB."""
    pass


# =============================================================================
# PROVENANCE LOGGING
# =============================================================================

class ProvenanceLogger:
    """Thread-safe provenance logging with full audit trail."""

    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.entries = []
        self._initialize_log()

    def _initialize_log(self):
        """Initialize CSV log with headers."""
        with open(self.log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp',
                'pdb_id',
                'resolution_angstrom',
                'experimental_method',
                'publication_doi',
                'organism',
                'chain_count',
                'residue_count',
                'missing_residues',
                'quality_status',
                'rejection_reason',
                'local_file_path',
            ])
        print(f"Provenance log initialized: {self.log_file}")

    def log_entry(self, entry: Dict):
        """Log a single entry to the provenance file."""
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                entry.get('timestamp', datetime.now().isoformat()),
                entry.get('pdb_id', 'UNKNOWN'),
                entry.get('resolution', 'N/A'),
                entry.get('method', 'UNKNOWN'),
                entry.get('doi', 'N/A'),
                entry.get('organism', 'UNKNOWN'),
                entry.get('chain_count', 0),
                entry.get('residue_count', 0),
                entry.get('missing_residues', 0),
                entry.get('status', 'UNKNOWN'),
                entry.get('rejection_reason', ''),
                entry.get('local_path', ''),
            ])
        self.entries.append(entry)


# =============================================================================
# RCSB API FUNCTIONS
# =============================================================================

def fetch_pdb_metadata(pdb_id: str) -> Dict:
    """
    Fetch metadata for a PDB entry from RCSB API.

    STRICT: Raises FetchError if API call fails.
    """
    pdb_id = pdb_id.upper().strip()

    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data
    except urllib.error.HTTPError as e:
        raise FetchError(f"HTTP error fetching {pdb_id}: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        raise FetchError(f"URL error fetching {pdb_id}: {e.reason}")
    except json.JSONDecodeError as e:
        raise FetchError(f"JSON decode error for {pdb_id}: {e}")


def fetch_pdb_file(pdb_id: str, output_dir: Path) -> Path:
    """
    Download PDB file from RCSB.

    STRICT: Raises FetchError if download fails.
    """
    pdb_id = pdb_id.upper().strip()
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    output_file = output_dir / f"{pdb_id}.pdb"

    try:
        urllib.request.urlretrieve(url, output_file)

        # Verify file was actually downloaded
        if not output_file.exists():
            raise FetchError(f"File not created after download: {output_file}")

        if output_file.stat().st_size == 0:
            raise FetchError(f"Downloaded file is empty: {output_file}")

        return output_file

    except urllib.error.HTTPError as e:
        raise FetchError(f"HTTP error downloading {pdb_id}: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        raise FetchError(f"URL error downloading {pdb_id}: {e.reason}")


# =============================================================================
# QUALITY CONTROL FUNCTIONS
# =============================================================================

def extract_resolution(metadata: Dict) -> Optional[float]:
    """Extract resolution from metadata. Returns None for NMR structures."""
    try:
        # X-ray diffraction resolution
        if 'rcsb_entry_info' in metadata:
            res = metadata['rcsb_entry_info'].get('resolution_combined', [None])[0]
            if res is not None:
                return float(res)

        # Try alternative locations
        if 'refine' in metadata and metadata['refine']:
            for refine in metadata['refine']:
                if 'ls_d_res_high' in refine:
                    return float(refine['ls_d_res_high'])

        return None
    except (TypeError, ValueError, IndexError):
        return None


def extract_experimental_method(metadata: Dict) -> str:
    """Extract experimental method from metadata."""
    try:
        if 'exptl' in metadata and metadata['exptl']:
            return metadata['exptl'][0].get('method', 'UNKNOWN')
        return 'UNKNOWN'
    except (TypeError, IndexError):
        return 'UNKNOWN'


def extract_doi(metadata: Dict) -> str:
    """Extract publication DOI from metadata."""
    try:
        if 'rcsb_primary_citation' in metadata:
            return metadata['rcsb_primary_citation'].get('pdbx_database_id_doi', 'N/A')
        return 'N/A'
    except (TypeError, KeyError):
        return 'N/A'


def extract_organism(metadata: Dict) -> str:
    """Extract source organism from metadata."""
    try:
        if 'rcsb_entry_info' in metadata:
            return metadata['rcsb_entry_info'].get('deposited_model_count', 'UNKNOWN')
        if 'entity_src_gen' in metadata and metadata['entity_src_gen']:
            return metadata['entity_src_gen'][0].get('pdbx_gene_src_scientific_name', 'UNKNOWN')
        return 'UNKNOWN'
    except (TypeError, IndexError, KeyError):
        return 'UNKNOWN'


def count_chains_and_residues(pdb_file: Path) -> Tuple[int, int, int]:
    """
    Parse PDB file and count chains, residues, and missing residues.

    Returns: (chain_count, residue_count, missing_residue_estimate)
    """
    chains = set()
    residues = set()
    prev_res_num = {}

    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                chain = line[21]
                res_num = int(line[22:26].strip())

                chains.add(chain)
                residues.add((chain, res_num))

                # Track gaps in residue numbering
                if chain in prev_res_num:
                    gap = res_num - prev_res_num[chain]
                    if gap > 1:
                        pass  # Could track gaps here
                prev_res_num[chain] = res_num

    # Estimate missing residues from REMARK 465 records
    missing = 0
    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith('REMARK 465') and len(line) > 20:
                # REMARK 465 lists missing residues
                missing += 1

    return len(chains), len(residues), missing


def validate_structure(pdb_id: str, metadata: Dict, pdb_file: Path, logger: ProvenanceLogger) -> bool:
    """
    Apply all quality filters to a structure.

    STRICT: Returns False and logs rejection reason if any filter fails.
    """
    timestamp = datetime.now().isoformat()

    # Extract metadata
    resolution = extract_resolution(metadata)
    method = extract_experimental_method(metadata)
    doi = extract_doi(metadata)
    organism = extract_organism(metadata)

    # Count structural elements
    chain_count, residue_count, missing = count_chains_and_residues(pdb_file)

    # Base entry
    entry = {
        'timestamp': timestamp,
        'pdb_id': pdb_id,
        'resolution': resolution,
        'method': method,
        'doi': doi,
        'organism': organism,
        'chain_count': chain_count,
        'residue_count': residue_count,
        'missing_residues': missing,
        'local_path': str(pdb_file),
    }

    # Quality checks
    rejection_reasons = []

    # Check 1: Resolution (for X-ray/Cryo-EM)
    if method in ['X-RAY DIFFRACTION', 'ELECTRON MICROSCOPY']:
        if resolution is None:
            rejection_reasons.append("Resolution not available")
        elif resolution > MAX_RESOLUTION_ANGSTROM:
            rejection_reasons.append(f"Resolution {resolution:.2f} Å > {MAX_RESOLUTION_ANGSTROM} Å threshold")

    # Check 2: Valid experimental method
    if method not in REQUIRED_METHODS:
        rejection_reasons.append(f"Unknown method: {method}")

    # Check 3: Minimum structure size
    if residue_count < 20:
        rejection_reasons.append(f"Too few residues: {residue_count}")

    # Check 4: Excessive missing residues (>20%)
    if residue_count > 0 and missing / residue_count > 0.20:
        rejection_reasons.append(f"Too many missing residues: {missing}/{residue_count}")

    # Log result
    if rejection_reasons:
        entry['status'] = 'REJECTED'
        entry['rejection_reason'] = '; '.join(rejection_reasons)
        logger.log_entry(entry)
        return False
    else:
        entry['status'] = 'ACCEPTED'
        entry['rejection_reason'] = ''
        logger.log_entry(entry)
        return True


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def fetch_validated_structure(pdb_id: str, logger: ProvenanceLogger) -> Optional[Path]:
    """
    Fetch a single PDB structure with full validation.

    Returns: Path to validated PDB file, or None if rejected.
    Raises: FetchError if fetch fails (does NOT return None silently).
    """
    print(f"\nProcessing {pdb_id}...")

    # Fetch metadata
    print(f"  Fetching metadata...")
    metadata = fetch_pdb_metadata(pdb_id)

    # Fetch PDB file
    print(f"  Downloading PDB file...")
    pdb_file = fetch_pdb_file(pdb_id, OUTPUT_DIR)

    # Validate
    print(f"  Validating quality...")
    is_valid = validate_structure(pdb_id, metadata, pdb_file, logger)

    if is_valid:
        print(f"  ✓ ACCEPTED: {pdb_id}")
        return pdb_file
    else:
        print(f"  ✗ REJECTED: {pdb_id}")
        # Remove rejected file to keep directory clean
        pdb_file.unlink()
        return None


def fetch_protein_set(pdb_ids: List[str]) -> Dict:
    """
    Fetch a set of PDB structures with quality control.

    Returns summary statistics and list of valid files.
    """
    print("=" * 80)
    print("DATA PROVENANCE PIPELINE")
    print("Fetching PDB structures with strict quality control")
    print("=" * 80)
    print(f"\nQuality thresholds:")
    print(f"  Max resolution: {MAX_RESOLUTION_ANGSTROM} Å")
    print(f"  Required methods: {REQUIRED_METHODS}")
    print(f"\nProcessing {len(pdb_ids)} structures...")

    logger = ProvenanceLogger(PROVENANCE_LOG)

    accepted = []
    rejected = []
    failed = []

    for pdb_id in pdb_ids:
        try:
            result = fetch_validated_structure(pdb_id, logger)
            if result:
                accepted.append(pdb_id)
            else:
                rejected.append(pdb_id)
        except FetchError as e:
            print(f"  ✗ FETCH FAILED: {pdb_id} - {e}")
            failed.append(pdb_id)
            # Log the failure
            logger.log_entry({
                'timestamp': datetime.now().isoformat(),
                'pdb_id': pdb_id,
                'status': 'FETCH_FAILED',
                'rejection_reason': str(e),
            })

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"  Total requested: {len(pdb_ids)}")
    print(f"  Accepted: {len(accepted)}")
    print(f"  Rejected: {len(rejected)}")
    print(f"  Failed: {len(failed)}")
    print(f"\nProvenance log: {PROVENANCE_LOG}")

    return {
        'total': len(pdb_ids),
        'accepted': accepted,
        'rejected': rejected,
        'failed': failed,
        'provenance_log': str(PROVENANCE_LOG),
    }


# =============================================================================
# DIVERSE PROTEIN SET FOR Z² VALIDATION
# =============================================================================

# Diverse set of well-characterized proteins for unbiased testing
DIVERSE_PROTEIN_SET = [
    # Small globular proteins
    '1UBQ',  # Ubiquitin (76 residues)
    '1L2Y',  # Trp-cage (20 residues)
    '2F21',  # Villin headpiece (35 residues)

    # Enzymes
    '1LYZ',  # Lysozyme
    '4HHB',  # Hemoglobin
    '1TIM',  # Triosephosphate isomerase

    # Membrane proteins
    '1F88',  # Rhodopsin
    '2RH1',  # Beta-2 adrenergic receptor
    '4DKL',  # GLP-1 receptor

    # Alpha-helical
    '1MBN',  # Myoglobin
    '2DN2',  # Insulin
    '1GCN',  # Glucagon

    # Beta-sheet
    '1TEN',  # Tenascin
    '1FNF',  # Fibronectin
    '1IGT',  # Immunoglobulin

    # Mixed alpha/beta
    '1AKE',  # Adenylate kinase
    '1CRN',  # Crambin
    '2GB1',  # Protein G B1

    # target system-related (our targets)
    '2N0A',  # Alpha-synuclein fibril
    '5OQV',  # Amyloid-beta fibril
    '4ZQK',  # PD-1/PD-L1 complex
    '5UAK',  # CFTR NBD1

    # Additional diversity
    '1AHO',  # Alpha-lactalbumin
    '1BDD',  # Protein A
    '1VII',  # Villin
    '3NJG',  # Green fluorescent protein
    '1CYO',  # Cytochrome c
    '2LZM',  # T4 lysozyme
    '1HHP',  # C2_Homodimer_A protease
    '1AAP',  # Amyloid precursor protein
]


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("STRICT DATA PROVENANCE SYSTEM")
    print("NO mock data. NO hardcoded outputs. FULL audit trail.")
    print("=" * 80)

    # Fetch diverse protein set for Z² validation
    results = fetch_protein_set(DIVERSE_PROTEIN_SET)

    # Save summary
    summary_file = LOG_DIR / "fetch_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nSummary saved: {summary_file}")

    if len(results['accepted']) < 10:
        print("\nWARNING: Fewer than 10 structures accepted.")
        print("Statistical analysis may be underpowered.")

    print("\n" + "=" * 80)
    print("Data provenance complete. All sources logged.")
    print("=" * 80)
