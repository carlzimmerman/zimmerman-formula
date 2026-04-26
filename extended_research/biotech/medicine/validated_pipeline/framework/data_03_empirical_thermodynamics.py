#!/usr/bin/env python3
"""
data_03_empirical_thermodynamics.py - Empirical Binding Affinity Validation

Replaces heuristic binding scores with experimentally measured ΔG, Kd, Ki values
from BindingDB and PDBbind databases.

Key Scientists Referenced:
- Martin Karplus: CHARMM force field creator
- William Jorgensen: OPLS/AMBER force fields
- Rui Wang: PDBbind database creator
- Michael Gilson: BindingDB creator
- David Mobley: Absolute binding free energy calculations

Data Sources:
- BindingDB API: https://bindingdb.org/rest/getLigandsByUniprot
- PDBbind (via downloads): http://www.pdbbind.org.cn/
- ChEMBL: https://www.ebi.ac.uk/chembl/

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import math


# =============================================================================
# CONSTANTS
# =============================================================================

# API endpoints
BINDINGDB_API = "https://bindingdb.org/rest/getLigandsByUniprot"
CHEMBL_API = "https://www.ebi.ac.uk/chembl/api/data"

# Thermodynamic constants
R = 1.987  # cal/(mol·K) - gas constant
T = 310.15  # K - body temperature (37°C)
RT = R * T / 1000  # kcal/mol ≈ 0.616

# Unit conversions
# ΔG = RT * ln(Kd) where Kd is in M
# Kd in nM: ΔG = RT * ln(Kd * 1e-9) = RT * (ln(Kd) - 9*ln(10))
#                                    ≈ RT * (ln(Kd) - 20.723)


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class BindingMeasurement:
    """A single experimental binding measurement."""
    source_db: str  # BindingDB, ChEMBL, PDBbind
    ligand_id: str
    ligand_name: str
    ligand_smiles: str
    target_name: str
    target_uniprot: str

    # Binding constants (whichever is available)
    kd_nm: Optional[float] = None  # Dissociation constant (nM)
    ki_nm: Optional[float] = None  # geometrically stabilize constant (nM)
    ic50_nm: Optional[float] = None  # Half-maximal inhibitory (nM)

    # Thermodynamics
    delta_g_kcal: Optional[float] = None  # Free energy (kcal/mol)
    delta_h_kcal: Optional[float] = None  # Enthalpy (kcal/mol)
    tds_kcal: Optional[float] = None  # Entropy contribution (kcal/mol)

    # Metadata
    pdb_id: Optional[str] = None
    reference: Optional[str] = None


@dataclass
class TargetBindingProfile:
    """Complete binding profile for a target protein."""
    uniprot_id: str
    target_name: str

    # All measurements
    measurements: List[BindingMeasurement] = field(default_factory=list)

    # Statistics
    n_measurements: int = 0
    n_with_kd: int = 0
    n_with_structure: int = 0

    # Best binders
    best_kd_nm: Optional[float] = None
    best_delta_g: Optional[float] = None
    best_ligand: Optional[str] = None

    # Affinity distribution
    kd_median_nm: Optional[float] = None
    kd_range: Tuple[float, float] = (0.0, 0.0)


# =============================================================================
# THERMODYNAMIC CALCULATIONS
# =============================================================================

def kd_to_delta_g(kd_nm: float) -> float:
    """Convert dissociation constant (nM) to free energy (kcal/mol).

    ΔG = RT * ln(Kd)

    At 310K:
    - Kd = 1 nM  → ΔG ≈ -12.7 kcal/mol (excellent binder)
    - Kd = 10 nM → ΔG ≈ -11.3 kcal/mol (good binder)
    - Kd = 100 nM → ΔG ≈ -9.9 kcal/mol (moderate binder)
    - Kd = 1 μM  → ΔG ≈ -8.5 kcal/mol (weak binder)
    """
    if kd_nm <= 0:
        return 0.0
    kd_m = kd_nm * 1e-9  # Convert nM to M
    return RT * math.log(kd_m)  # kcal/mol


def delta_g_to_kd(delta_g_kcal: float) -> float:
    """Convert free energy (kcal/mol) to dissociation constant (nM).

    Kd = exp(ΔG / RT)
    """
    if delta_g_kcal == 0:
        return float('inf')
    kd_m = math.exp(delta_g_kcal / RT)
    return kd_m * 1e9  # Convert M to nM


# =============================================================================
# API FUNCTIONS
# =============================================================================

def query_bindingdb(uniprot_id: str, cutoff_nm: int = 100000) -> List[BindingMeasurement]:
    """Query BindingDB for binding measurements against a UniProt target.

    API: https://bindingdb.org/rest/getLigandsByUniprot?uniprot={ID};{cutoff}
    NOTE: Semicolon separates UniProt ID and cutoff value

    Args:
        uniprot_id: UniProt accession (e.g., "P30559")
        cutoff_nm: IC50 cutoff in nM (default 100 μM = 100000 nM)

    Returns:
        List of BindingMeasurement objects
    """
    # IMPORTANT: semicolon format, not query param format
    url = f"https://bindingdb.org/rest/getLigandsByUniprot?uniprot={uniprot_id};{cutoff_nm}&response=application/json"

    print(f"    [BindingDB] Querying {uniprot_id}...")

    try:
        request = urllib.request.Request(
            url,
            headers={'Accept': 'application/json', 'User-Agent': 'Z2-Framework/1.0'}
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read().decode('utf-8')

            # BindingDB returns text/plain even when asking for JSON
            if not content.strip():
                print(f"    [BindingDB] No data for {uniprot_id}")
                return []

            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                # Try parsing as TSV
                return parse_bindingdb_tsv(content, uniprot_id)

            return parse_bindingdb_json(data, uniprot_id)

    except urllib.error.HTTPError as e:
        print(f"    [BindingDB] HTTP error {e.code}: {e.reason}")
        return []
    except urllib.error.URLError as e:
        print(f"    [BindingDB] Connection error: {e}")
        return []


def parse_bindingdb_json(data: Dict, uniprot_id: str) -> List[BindingMeasurement]:
    """Parse BindingDB JSON response.

    BindingDB returns format:
    {
        "getLindsByUniprotResponse": {
            "bdb.affinities": [
                {"bdb.monomerid": 123, "bdb.smile": "...", "bdb.affinity_type": "Ki", "bdb.affinity": " 1.7"}
            ]
        }
    }
    """
    measurements = []

    # Handle the actual BindingDB response format
    response = data.get('getLindsByUniprotResponse', data)
    entries = response.get('bdb.affinities', [])

    if not entries:
        # Try alternate formats
        entries = data.get('affinities', [])
        if not entries and isinstance(data, list):
            entries = data

    for entry in entries:
        # Parse BindingDB specific format
        affinity_type = entry.get('bdb.affinity_type', entry.get('affinity_type', '')).upper()
        affinity_str = str(entry.get('bdb.affinity', entry.get('affinity', ''))).strip()

        # Parse the affinity value
        affinity_nm = parse_affinity_value(affinity_str)

        # Assign to appropriate constant based on type
        kd_nm = affinity_nm if affinity_type == 'KD' else None
        ki_nm = affinity_nm if affinity_type == 'KI' else None
        ic50_nm = affinity_nm if affinity_type in ('IC50', 'EC50') else None

        # Calculate ΔG from best available constant
        delta_g = None
        if kd_nm and kd_nm > 0:
            delta_g = kd_to_delta_g(kd_nm)
        elif ki_nm and ki_nm > 0:
            delta_g = kd_to_delta_g(ki_nm)
        elif ic50_nm and ic50_nm > 0:
            # IC50 ≈ 2 * Ki for competitive inhibitors
            delta_g = kd_to_delta_g(ic50_nm / 2)

        measurements.append(BindingMeasurement(
            source_db="BindingDB",
            ligand_id=str(entry.get('bdb.monomerid', entry.get('monomerid', ''))),
            ligand_name=entry.get('Name', 'Ligand'),
            ligand_smiles=entry.get('bdb.smile', entry.get('SMILES', '')),
            target_name=response.get('bdb.primary', uniprot_id),
            target_uniprot=uniprot_id,
            kd_nm=kd_nm,
            ki_nm=ki_nm,
            ic50_nm=ic50_nm,
            delta_g_kcal=delta_g,
            reference=entry.get('Article DOI', '')
        ))

    return measurements


def parse_bindingdb_tsv(content: str, uniprot_id: str) -> List[BindingMeasurement]:
    """Parse BindingDB TSV response (fallback)."""
    measurements = []
    lines = content.strip().split('\n')

    if len(lines) < 2:
        return measurements

    headers = lines[0].split('\t')

    for line in lines[1:]:
        if not line.strip():
            continue

        values = line.split('\t')
        row = dict(zip(headers, values))

        # Extract binding constants
        kd_nm = parse_affinity_value(row.get('Kd (nM)', ''))
        ki_nm = parse_affinity_value(row.get('Ki (nM)', ''))
        ic50_nm = parse_affinity_value(row.get('IC50 (nM)', ''))

        # Calculate ΔG
        delta_g = None
        if kd_nm:
            delta_g = kd_to_delta_g(kd_nm)
        elif ki_nm:
            delta_g = kd_to_delta_g(ki_nm)
        elif ic50_nm:
            delta_g = kd_to_delta_g(ic50_nm / 2)

        measurements.append(BindingMeasurement(
            source_db="BindingDB",
            ligand_id=row.get('Ligand InChI Key', ''),
            ligand_name=row.get('Ligand Name', 'Unknown'),
            ligand_smiles=row.get('Ligand SMILES', ''),
            target_name=row.get('Target Name', ''),
            target_uniprot=uniprot_id,
            kd_nm=kd_nm,
            ki_nm=ki_nm,
            ic50_nm=ic50_nm,
            delta_g_kcal=delta_g,
            pdb_id=row.get('PDB ID(s) of Target', ''),
            reference=row.get('PMID', '')
        ))

    return measurements


def parse_affinity_value(value: str) -> Optional[float]:
    """Parse affinity value, handling ranges and inequalities."""
    if not value or value in ('', 'N/A', 'None'):
        return None

    value = str(value).strip()

    # Handle inequalities
    for prefix in ['>', '<', '>=', '<=', '~', '≈']:
        value = value.replace(prefix, '')

    # Handle ranges (take geometric mean)
    if '-' in value and not value.startswith('-'):
        parts = value.split('-')
        try:
            vals = [float(p) for p in parts]
            return math.sqrt(vals[0] * vals[1])
        except ValueError:
            pass

    try:
        return float(value)
    except ValueError:
        return None


def query_chembl_target(uniprot_id: str) -> List[BindingMeasurement]:
    """Query ChEMBL for binding activities against a target.

    This is a simplified query - ChEMBL has a more complex API.
    """
    print(f"    [ChEMBL] Querying {uniprot_id}...")

    # First, get the ChEMBL target ID from UniProt
    target_url = f"{CHEMBL_API}/target.json?target_components__accession={uniprot_id}"

    try:
        request = urllib.request.Request(
            target_url,
            headers={'Accept': 'application/json', 'User-Agent': 'Z2-Framework/1.0'}
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))

        targets = data.get('targets', [])
        if not targets:
            print(f"    [ChEMBL] No target found for {uniprot_id}")
            return []

        chembl_id = targets[0].get('target_chembl_id')
        print(f"    [ChEMBL] Found target: {chembl_id}")

        # Now get activities for this target
        activity_url = f"{CHEMBL_API}/activity.json?target_chembl_id={chembl_id}&limit=100"

        request = urllib.request.Request(
            activity_url,
            headers={'Accept': 'application/json', 'User-Agent': 'Z2-Framework/1.0'}
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            activity_data = json.loads(response.read().decode('utf-8'))

        return parse_chembl_activities(activity_data, uniprot_id)

    except urllib.error.HTTPError as e:
        print(f"    [ChEMBL] HTTP error {e.code}")
        return []
    except urllib.error.URLError as e:
        print(f"    [ChEMBL] Connection error: {e}")
        return []


def parse_chembl_activities(data: Dict, uniprot_id: str) -> List[BindingMeasurement]:
    """Parse ChEMBL activity data."""
    measurements = []

    for activity in data.get('activities', []):
        # Extract value and units
        value = activity.get('standard_value')
        units = activity.get('standard_units', '')
        activity_type = activity.get('standard_type', '').upper()

        if not value:
            continue

        # Convert to nM
        try:
            value_nm = float(value)
            if units == 'uM':
                value_nm *= 1000
            elif units == 'pM':
                value_nm /= 1000
            elif units == 'mM':
                value_nm *= 1e6
        except ValueError:
            continue

        # Assign to appropriate constant
        kd_nm = value_nm if activity_type == 'KD' else None
        ki_nm = value_nm if activity_type == 'KI' else None
        ic50_nm = value_nm if activity_type == 'IC50' else None

        # Calculate ΔG
        delta_g = None
        if kd_nm:
            delta_g = kd_to_delta_g(kd_nm)
        elif ki_nm:
            delta_g = kd_to_delta_g(ki_nm)
        elif ic50_nm:
            delta_g = kd_to_delta_g(ic50_nm / 2)

        measurements.append(BindingMeasurement(
            source_db="ChEMBL",
            ligand_id=activity.get('molecule_chembl_id', ''),
            ligand_name=activity.get('molecule_pref_name', 'Unknown'),
            ligand_smiles=activity.get('canonical_smiles', ''),
            target_name=activity.get('target_pref_name', ''),
            target_uniprot=uniprot_id,
            kd_nm=kd_nm,
            ki_nm=ki_nm,
            ic50_nm=ic50_nm,
            delta_g_kcal=delta_g,
            reference=activity.get('document_journal', '')
        ))

    return measurements


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def build_binding_profile(
    uniprot_id: str,
    target_name: str = "Unknown"
) -> TargetBindingProfile:
    """Build complete binding profile from all data sources."""
    print(f"\n    Building binding profile for {uniprot_id}...")

    all_measurements = []

    # Query BindingDB
    bindingdb_data = query_bindingdb(uniprot_id)
    all_measurements.extend(bindingdb_data)
    print(f"    [BindingDB] Found {len(bindingdb_data)} measurements")

    # Query ChEMBL (optional - can be slow)
    # chembl_data = query_chembl_target(uniprot_id)
    # all_measurements.extend(chembl_data)
    # print(f"    [ChEMBL] Found {len(chembl_data)} measurements")

    # Calculate statistics
    kd_values = [
        m.kd_nm or m.ki_nm or (m.ic50_nm / 2 if m.ic50_nm else None)
        for m in all_measurements
    ]
    kd_values = [v for v in kd_values if v is not None and v > 0]

    best_kd = min(kd_values) if kd_values else None
    best_delta_g = kd_to_delta_g(best_kd) if best_kd else None

    # Find best ligand
    best_ligand = None
    if best_kd:
        for m in all_measurements:
            eff_kd = m.kd_nm or m.ki_nm or (m.ic50_nm / 2 if m.ic50_nm else float('inf'))
            if eff_kd and abs(eff_kd - best_kd) < 0.01:
                best_ligand = m.ligand_name
                break

    profile = TargetBindingProfile(
        uniprot_id=uniprot_id,
        target_name=target_name,
        measurements=all_measurements,
        n_measurements=len(all_measurements),
        n_with_kd=sum(1 for m in all_measurements if m.kd_nm),
        n_with_structure=sum(1 for m in all_measurements if m.pdb_id),
        best_kd_nm=best_kd,
        best_delta_g=best_delta_g,
        best_ligand=best_ligand,
        kd_median_nm=sorted(kd_values)[len(kd_values)//2] if kd_values else None,
        kd_range=(min(kd_values), max(kd_values)) if kd_values else (0.0, 0.0)
    )

    return profile


def print_binding_profile(profile: TargetBindingProfile) -> None:
    """Print formatted binding profile."""
    print(f"\n    {'='*60}")
    print(f"    BINDING PROFILE: {profile.uniprot_id}")
    print(f"    {'='*60}")
    print(f"    Target: {profile.target_name}")
    print(f"    Total measurements: {profile.n_measurements}")
    print(f"    With Kd: {profile.n_with_kd}")
    print(f"    With structure: {profile.n_with_structure}")

    if profile.best_kd_nm:
        print(f"\n    THERMODYNAMICS:")
        print(f"    {'─'*50}")
        print(f"    Best Kd: {profile.best_kd_nm:.2f} nM")
        print(f"    Best ΔG: {profile.best_delta_g:.2f} kcal/mol")
        print(f"    Best ligand: {profile.best_ligand}")
        print(f"    Kd range: {profile.kd_range[0]:.2f} - {profile.kd_range[1]:.2f} nM")
        print(f"    Kd median: {profile.kd_median_nm:.2f} nM")

        # Binding quality assessment
        if profile.best_kd_nm < 10:
            quality = "EXCELLENT (sub-nM to single-digit nM)"
        elif profile.best_kd_nm < 100:
            quality = "GOOD (10-100 nM)"
        elif profile.best_kd_nm < 1000:
            quality = "MODERATE (100 nM - 1 μM)"
        else:
            quality = "WEAK (> 1 μM)"

        print(f"\n    ASSESSMENT: Known binders exist - {quality}")

    else:
        print(f"\n    No binding affinity data found in BindingDB")

    print(f"    {'='*60}\n")


def validate_z2_against_empirical(
    uniprot_ids: List[str],
    output_dir: Optional[Path] = None
) -> Dict[str, TargetBindingProfile]:
    """Validate Z² framework against empirical binding data."""
    print("\n" + "="*70)
    print("EMPIRICAL THERMODYNAMICS VALIDATION")
    print("="*70)
    print(f"    Targets: {len(uniprot_ids)}")
    print(f"    Data sources: BindingDB")
    print(f"    Temperature: {T:.2f} K (body temperature)")
    print(f"    RT: {RT:.4f} kcal/mol")

    results = {}

    for uniprot_id in uniprot_ids:
        profile = build_binding_profile(uniprot_id)
        results[uniprot_id] = profile
        print_binding_profile(profile)

    # Summary
    print("\n" + "="*70)
    print("EMPIRICAL VALIDATION SUMMARY")
    print("="*70)

    print(f"\n    {'Target':<15} {'Best Kd (nM)':<15} {'ΔG (kcal/mol)':<15} {'Quality'}")
    print(f"    {'-'*60}")

    for uid, profile in results.items():
        if profile.best_kd_nm:
            if profile.best_kd_nm < 10:
                quality = "Excellent"
            elif profile.best_kd_nm < 100:
                quality = "Good"
            elif profile.best_kd_nm < 1000:
                quality = "Moderate"
            else:
                quality = "Weak"
            print(f"    {uid:<15} {profile.best_kd_nm:>12.2f}   {profile.best_delta_g:>12.2f}   {quality}")
        else:
            print(f"    {uid:<15} {'N/A':>12}   {'N/A':>12}   No data")

    print("="*70 + "\n")

    # Save results
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "empirical_thermodynamics.json"

        # Convert to serializable format
        output_data = {}
        for uid, profile in results.items():
            output_data[uid] = {
                'uniprot_id': profile.uniprot_id,
                'target_name': profile.target_name,
                'n_measurements': profile.n_measurements,
                'best_kd_nm': profile.best_kd_nm,
                'best_delta_g': profile.best_delta_g,
                'best_ligand': profile.best_ligand,
                'measurements': [asdict(m) for m in profile.measurements[:20]]  # Top 20
            }

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        print(f"    Saved: {output_file}")

    return results


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Validate Z² targets against empirical binding data."""
    import argparse

    parser = argparse.ArgumentParser(description="Empirical Thermodynamics Validator")
    parser.add_argument("--targets", nargs="+", help="UniProt IDs to analyze")
    parser.add_argument("--output", type=Path, help="Output directory")
    args = parser.parse_args()

    # Default targets - use structured targets from IDP filter
    if args.targets:
        targets = args.targets
    else:
        targets = [
            "P30559",  # Oxytocin receptor - SUITABLE
            "P04578",  # C2_Homodimer_A gp120 - CAUTION (but structured core)
        ]

    output_dir = args.output or Path(__file__).parent.parent / "empirical_validation"

    results = validate_z2_against_empirical(targets, output_dir)

    return results


if __name__ == "__main__":
    main()
