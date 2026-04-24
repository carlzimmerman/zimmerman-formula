#!/usr/bin/env python3
"""
data_02_idp_filter.py - Filter Intrinsically Disordered Proteins

Prevents Z² pharmacophore design from targeting proteins that are intrinsically
disordered (IDP) or have significant disordered regions (IDR).

Key Scientists Referenced:
- A. Keith Dunker: Pioneer of IDP discovery, DisProt database
- Vladimir Uversky: Charge-hydropathy plots for disorder prediction
- Rohit Pappu: Phase behavior of disordered proteins
- Peter Tompa: Coupled folding-binding mechanisms

Data Sources:
- DisProt API: https://disprot.org/api/{UniProt_ID}
- UniProt feature annotations

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from pathlib import Path


# =============================================================================
# CONSTANTS
# =============================================================================

DISPROT_API_BASE = "https://disprot.org/api"
UNIPROT_API_BASE = "https://rest.uniprot.org/uniprotkb"

# Disorder thresholds
MAX_DISORDER_FRACTION = 0.30  # Reject if >30% disordered
MAX_DISORDER_REGION_LENGTH = 50  # Flag continuous disorder >50 residues

# Charge-hydropathy boundaries (Uversky plot)
# Proteins below this line are likely disordered
CH_BOUNDARY_SLOPE = 2.785
CH_BOUNDARY_INTERCEPT = -1.151


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class DisorderRegion:
    """A single disordered region annotation."""
    start: int
    end: int
    length: int
    evidence_type: str
    confidence: float


@dataclass
class IDPAnalysis:
    """Complete IDP analysis for a protein."""
    uniprot_id: str
    protein_name: str
    sequence_length: int

    # DisProt data
    disprot_id: Optional[str]
    disorder_regions: List[DisorderRegion]
    total_disorder_residues: int
    disorder_fraction: float
    max_disorder_region: int

    # Charge-hydropathy analysis
    mean_hydropathy: float
    mean_net_charge: float
    ch_score: float  # Distance from Uversky boundary

    # Verdict
    is_idp: bool
    is_partial_idp: bool
    recommendation: str

    # Data quality
    has_disprot_data: bool
    evidence_count: int


# =============================================================================
# AMINO ACID PROPERTIES
# =============================================================================

# Kyte-Doolittle hydropathy scale
HYDROPATHY = {
    'A':  1.8, 'C':  2.5, 'D': -3.5, 'E': -3.5, 'F':  2.8,
    'G': -0.4, 'H': -3.2, 'I':  4.5, 'K': -3.9, 'L':  3.8,
    'M':  1.9, 'N': -3.5, 'P': -1.6, 'Q': -3.5, 'R': -4.5,
    'S': -0.8, 'T': -0.7, 'V':  4.2, 'W': -0.9, 'Y': -1.3
}

# Charge at pH 7
CHARGE = {
    'D': -1, 'E': -1,  # Negative
    'K': +1, 'R': +1, 'H': +0.1,  # Positive (H is partially charged)
    'A': 0, 'C': 0, 'F': 0, 'G': 0, 'I': 0, 'L': 0,
    'M': 0, 'N': 0, 'P': 0, 'Q': 0, 'S': 0, 'T': 0,
    'V': 0, 'W': 0, 'Y': 0
}


# =============================================================================
# API FUNCTIONS
# =============================================================================

def query_disprot(uniprot_id: str) -> Optional[Dict]:
    """Query DisProt API for disorder annotations.

    API Reference: https://disprot.org/api/{UniProt_ID}
    Returns JSON with disorder regions and evidence.
    """
    url = f"{DISPROT_API_BASE}/{uniprot_id}"

    try:
        request = urllib.request.Request(
            url,
            headers={'Accept': 'application/json', 'User-Agent': 'Z2-Framework/1.0'}
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"    [DisProt] No entry for {uniprot_id}")
            return None
        raise
    except urllib.error.URLError as e:
        print(f"    [DisProt] Connection error: {e}")
        return None


def query_uniprot_features(uniprot_id: str) -> Optional[Dict]:
    """Query UniProt for protein features including disorder.

    API Reference: https://rest.uniprot.org/uniprotkb/{id}
    """
    url = f"{UNIPROT_API_BASE}/{uniprot_id}.json"

    try:
        request = urllib.request.Request(
            url,
            headers={'Accept': 'application/json', 'User-Agent': 'Z2-Framework/1.0'}
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"    [UniProt] No entry for {uniprot_id}")
            return None
        raise
    except urllib.error.URLError as e:
        print(f"    [UniProt] Connection error: {e}")
        return None


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def calculate_charge_hydropathy(sequence: str) -> Tuple[float, float, float]:
    """Calculate mean hydropathy, mean net charge, and Uversky CH score.

    Based on: Uversky VN et al. (2000) "Why are 'natively unfolded' proteins
    unstructured under physiologic conditions?"

    The charge-hydropathy (CH) plot separates folded from disordered proteins.
    Boundary line: |<charge>| = CH_BOUNDARY_SLOPE * <hydropathy> + CH_BOUNDARY_INTERCEPT

    Returns:
        (mean_hydropathy, mean_net_charge, ch_score)
        ch_score > 0 means likely disordered
    """
    if not sequence:
        return 0.0, 0.0, 0.0

    # Normalize hydropathy to [0, 1] range (Uversky method)
    # Original scale: -4.5 to +4.5, normalized: (h + 4.5) / 9.0
    hydropathy_values = []
    charges = []

    for aa in sequence.upper():
        if aa in HYDROPATHY:
            hydropathy_values.append((HYDROPATHY[aa] + 4.5) / 9.0)
        if aa in CHARGE:
            charges.append(CHARGE[aa])

    if not hydropathy_values:
        return 0.0, 0.0, 0.0

    mean_hydropathy = sum(hydropathy_values) / len(hydropathy_values)
    mean_net_charge = abs(sum(charges) / len(sequence))

    # Calculate distance from boundary
    # Boundary: |charge| = 2.785 * hydropathy - 1.151
    boundary_charge = CH_BOUNDARY_SLOPE * mean_hydropathy + CH_BOUNDARY_INTERCEPT
    ch_score = mean_net_charge - boundary_charge  # Positive = disordered side

    return mean_hydropathy, mean_net_charge, ch_score


def parse_disprot_regions(disprot_data: Dict) -> List[DisorderRegion]:
    """Parse DisProt response into disorder regions."""
    regions = []

    if not disprot_data:
        return regions

    # DisProt returns regions in 'disprot_consensus' or 'regions' field
    region_data = disprot_data.get('regions', [])
    if not region_data:
        region_data = disprot_data.get('disprot_consensus', {}).get('regions', [])

    for r in region_data:
        # Check if this is a disorder annotation
        term = r.get('term_name', '').lower()
        if 'disorder' in term or 'unstructured' in term or 'flexible' in term:
            start = r.get('start', 0)
            end = r.get('end', 0)
            evidence = r.get('evidence_type', 'experimental')
            confidence = r.get('confidence', 1.0)

            regions.append(DisorderRegion(
                start=start,
                end=end,
                length=end - start + 1,
                evidence_type=evidence,
                confidence=confidence if isinstance(confidence, float) else 1.0
            ))

    return regions


def analyze_idp(
    uniprot_id: str,
    sequence: Optional[str] = None
) -> IDPAnalysis:
    """Complete IDP analysis for a protein target.

    Combines:
    1. DisProt experimental disorder annotations
    2. Charge-hydropathy analysis (Uversky plot)
    3. UniProt feature annotations
    """
    print(f"\n    Analyzing {uniprot_id} for intrinsic disorder...")

    # Query DisProt
    disprot_data = query_disprot(uniprot_id)
    has_disprot = disprot_data is not None

    # Get sequence and name from UniProt if not provided
    protein_name = "Unknown"
    if sequence is None:
        uniprot_data = query_uniprot_features(uniprot_id)
        if uniprot_data:
            sequence = uniprot_data.get('sequence', {}).get('value', '')
            protein_name = uniprot_data.get('proteinDescription', {}).get(
                'recommendedName', {}
            ).get('fullName', {}).get('value', 'Unknown')

    if not sequence:
        print(f"    [ERROR] Could not retrieve sequence for {uniprot_id}")
        return IDPAnalysis(
            uniprot_id=uniprot_id,
            protein_name=protein_name,
            sequence_length=0,
            disprot_id=None,
            disorder_regions=[],
            total_disorder_residues=0,
            disorder_fraction=0.0,
            max_disorder_region=0,
            mean_hydropathy=0.0,
            mean_net_charge=0.0,
            ch_score=0.0,
            is_idp=False,
            is_partial_idp=False,
            recommendation="ERROR: No sequence",
            has_disprot_data=False,
            evidence_count=0
        )

    seq_length = len(sequence)

    # Parse disorder regions from DisProt
    disorder_regions = parse_disprot_regions(disprot_data) if disprot_data else []
    disprot_id = disprot_data.get('disprot_id') if disprot_data else None

    # Calculate disorder statistics
    total_disorder = sum(r.length for r in disorder_regions)
    disorder_fraction = total_disorder / seq_length if seq_length > 0 else 0.0
    max_region = max((r.length for r in disorder_regions), default=0)

    # Charge-hydropathy analysis
    mean_hydropathy, mean_charge, ch_score = calculate_charge_hydropathy(sequence)

    # Determine IDP status
    is_idp = False
    is_partial_idp = False

    # Full IDP criteria (Uversky):
    # 1. CH score > 0 (above boundary)
    # 2. OR >50% disordered in DisProt
    if ch_score > 0 or disorder_fraction > 0.50:
        is_idp = True

    # Partial IDP criteria:
    # 1. 30-50% disordered
    # 2. OR any region > 50 residues disordered
    # 3. OR CH score > -0.1 (near boundary)
    elif (disorder_fraction > 0.30 or
          max_region > MAX_DISORDER_REGION_LENGTH or
          ch_score > -0.1):
        is_partial_idp = True

    # Generate recommendation
    if is_idp:
        recommendation = (
            "REJECT: Full IDP - not suitable for rigid pharmacophore design. "
            "Consider coupled folding-binding approach (Tompa) or phase separation "
            "targeting (Pappu) instead."
        )
    elif is_partial_idp:
        recommendation = (
            "CAUTION: Partial IDP - has significant disordered regions. "
            "Target only structured domains. Verify binding site rigidity with MD."
        )
    else:
        recommendation = (
            "SUITABLE: Protein is predominantly structured. "
            "Appropriate for Z² pharmacophore design."
        )

    analysis = IDPAnalysis(
        uniprot_id=uniprot_id,
        protein_name=protein_name,
        sequence_length=seq_length,
        disprot_id=disprot_id,
        disorder_regions=disorder_regions,
        total_disorder_residues=total_disorder,
        disorder_fraction=disorder_fraction,
        max_disorder_region=max_region,
        mean_hydropathy=mean_hydropathy,
        mean_net_charge=mean_charge,
        ch_score=ch_score,
        is_idp=is_idp,
        is_partial_idp=is_partial_idp,
        recommendation=recommendation,
        has_disprot_data=has_disprot,
        evidence_count=len(disorder_regions)
    )

    return analysis


def print_analysis(analysis: IDPAnalysis) -> None:
    """Print formatted IDP analysis."""
    print(f"\n    {'='*60}")
    print(f"    IDP ANALYSIS: {analysis.uniprot_id}")
    print(f"    {'='*60}")
    print(f"    Protein: {analysis.protein_name}")
    print(f"    Length: {analysis.sequence_length} residues")
    print(f"    DisProt ID: {analysis.disprot_id or 'Not in DisProt'}")

    print(f"\n    DISORDER STATISTICS:")
    print(f"    {'─'*50}")
    print(f"    Total disordered: {analysis.total_disorder_residues} residues ({analysis.disorder_fraction:.1%})")
    print(f"    Max disorder region: {analysis.max_disorder_region} residues")
    print(f"    Evidence count: {analysis.evidence_count}")

    print(f"\n    CHARGE-HYDROPATHY (UVERSKY PLOT):")
    print(f"    {'─'*50}")
    print(f"    Mean hydropathy: {analysis.mean_hydropathy:.3f}")
    print(f"    Mean net charge: {analysis.mean_net_charge:.3f}")
    print(f"    CH score: {analysis.ch_score:+.3f} ({'DISORDERED' if analysis.ch_score > 0 else 'FOLDED'} side)")

    print(f"\n    VERDICT:")
    print(f"    {'─'*50}")
    if analysis.is_idp:
        print(f"    ✗ FULL IDP - REJECT TARGET")
    elif analysis.is_partial_idp:
        print(f"    ⚠ PARTIAL IDP - USE CAUTION")
    else:
        print(f"    ✓ STRUCTURED - SUITABLE")
    print(f"\n    {analysis.recommendation}")
    print(f"    {'='*60}\n")


def filter_targets(
    uniprot_ids: List[str],
    output_dir: Optional[Path] = None
) -> Dict[str, IDPAnalysis]:
    """Filter a list of targets, identifying IDPs.

    Returns dict of analyses keyed by UniProt ID.
    """
    print("\n" + "="*70)
    print("IDP FILTER - Screening targets for intrinsic disorder")
    print("="*70)
    print(f"    Targets: {len(uniprot_ids)}")
    print(f"    Max disorder threshold: {MAX_DISORDER_FRACTION:.0%}")
    print(f"    Method: DisProt + Charge-Hydropathy (Uversky)")

    results = {}
    suitable = []
    rejected = []
    caution = []

    for uid in uniprot_ids:
        analysis = analyze_idp(uid)
        results[uid] = analysis
        print_analysis(analysis)

        if analysis.is_idp:
            rejected.append(uid)
        elif analysis.is_partial_idp:
            caution.append(uid)
        else:
            suitable.append(uid)

    # Summary
    print("\n" + "="*70)
    print("IDP FILTER SUMMARY")
    print("="*70)
    print(f"    SUITABLE (structured):   {len(suitable)}")
    for uid in suitable:
        print(f"        ✓ {uid}: {results[uid].protein_name}")

    print(f"\n    CAUTION (partial IDP):   {len(caution)}")
    for uid in caution:
        print(f"        ⚠ {uid}: {results[uid].protein_name}")

    print(f"\n    REJECTED (full IDP):     {len(rejected)}")
    for uid in rejected:
        print(f"        ✗ {uid}: {results[uid].protein_name}")

    print("="*70 + "\n")

    # Save results
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "idp_filter_results.json"
        with open(output_file, 'w') as f:
            json.dump(
                {uid: asdict(a) for uid, a in results.items()},
                f, indent=2, default=str
            )
        print(f"    Saved: {output_file}")

    return results


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Test IDP filter on Z² pipeline targets."""
    import argparse

    parser = argparse.ArgumentParser(description="IDP Filter for Z² Framework")
    parser.add_argument("--targets", nargs="+", help="UniProt IDs to analyze")
    parser.add_argument("--output", type=Path, help="Output directory")
    args = parser.parse_args()

    # Default targets from Z² pipeline
    if args.targets:
        targets = args.targets
    else:
        targets = [
            "P37840",  # Alpha-synuclein (Parkinson's) - KNOWN IDP
            "P10636",  # Tau (Alzheimer's) - KNOWN IDP
            "P04578",  # HIV gp120 - Structured
            "P30559",  # Oxytocin receptor - Structured GPCR
        ]

    output_dir = args.output or Path(__file__).parent.parent / "idp_analysis"

    results = filter_targets(targets, output_dir)

    return results


if __name__ == "__main__":
    main()
