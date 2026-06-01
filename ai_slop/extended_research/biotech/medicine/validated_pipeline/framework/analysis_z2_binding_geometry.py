#!/usr/bin/env python3
"""
analysis_z2_binding_geometry.py - Analyze if Known Binders Match Z² Geometry

Searches PDB for co-crystal structures of targets with their best ligands,
then measures key interaction distances to see if they match the Z² constant
of 6.015152508891966 Å.

Key hypothesis: If Z² framework is correct, the best binders should show
interaction distances clustered around 6.015 Å from aromatic anchor atoms
(Trp, Tyr, Phe) to target binding site atoms.

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import math
import re


# =============================================================================
# CONSTANTS
# =============================================================================

Z2_DISTANCE = 6.015152508891966  # Å - target interaction distance
Z2_TOLERANCE = 0.5  # Å - tolerance for matching

# RCSB PDB REST API
PDB_SEARCH_API = "https://search.rcsb.org/rcsbsearch/v2/query"
PDB_DATA_API = "https://data.rcsb.org/rest/v1/core/entry"

# Aromatic anchor atoms (atoms that should be ~6.015 Å from target)
AROMATIC_ANCHORS = {
    'TRP': ['CZ2', 'CZ3', 'CH2', 'CE3', 'NE1'],  # Indole ring atoms
    'TYR': ['CZ', 'CE1', 'CE2', 'OH'],  # Phenol ring atoms
    'PHE': ['CZ', 'CE1', 'CE2'],  # Benzene ring atoms
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class PDBStructure:
    """PDB structure information."""
    pdb_id: str
    title: str
    resolution: Optional[float]
    ligand_ids: List[str]
    uniprot_ids: List[str]
    method: str


@dataclass
class DistanceMeasurement:
    """A measured distance from ligand to receptor."""
    pdb_id: str
    ligand_residue: str
    ligand_atom: str
    receptor_residue: str
    receptor_atom: str
    distance: float
    matches_z2: bool  # True if within tolerance of 6.015 Å


@dataclass
class Z2ValidationResult:
    """Result of Z² geometry validation for a target."""
    uniprot_id: str
    target_name: str
    n_structures: int
    n_distances_measured: int
    n_z2_matches: int
    z2_match_rate: float
    distances: List[DistanceMeasurement]
    distance_histogram: Dict[str, int]  # Binned distances
    mean_distance: float
    std_distance: float


# =============================================================================
# API FUNCTIONS
# =============================================================================

def search_pdb_by_uniprot(uniprot_id: str, max_results: int = 50) -> List[str]:
    """Search PDB for structures containing a UniProt accession.

    Uses RCSB Search API v2.
    """
    query = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession",
                "operator": "exact_match",
                "value": uniprot_id
            }
        },
        "request_options": {
            "return_all_hits": False,
            "results_content_type": ["experimental"],
            "sort": [{"sort_by": "rcsb_entry_info.resolution_combined", "direction": "asc"}]
        },
        "return_type": "entry"
    }

    print(f"    [PDB] Searching for {uniprot_id} structures...")

    try:
        data = json.dumps(query).encode('utf-8')
        request = urllib.request.Request(
            PDB_SEARCH_API,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))

        pdb_ids = [hit['identifier'] for hit in result.get('result_set', [])][:max_results]
        print(f"    [PDB] Found {len(pdb_ids)} structures")
        return pdb_ids

    except urllib.error.HTTPError as e:
        print(f"    [PDB] HTTP error: {e.code}")
        return []
    except Exception as e:
        print(f"    [PDB] Error: {e}")
        return []


def get_pdb_info(pdb_id: str) -> Optional[PDBStructure]:
    """Get metadata for a PDB entry."""
    url = f"{PDB_DATA_API}/{pdb_id}"

    try:
        request = urllib.request.Request(
            url,
            headers={'Accept': 'application/json'}
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))

        # Extract info
        entry = data.get('rcsb_entry_info', {})
        container = data.get('rcsb_entry_container_identifiers', {})

        return PDBStructure(
            pdb_id=pdb_id,
            title=data.get('struct', {}).get('title', ''),
            resolution=entry.get('resolution_combined', [None])[0] if entry.get('resolution_combined') else None,
            ligand_ids=container.get('non_polymer_entity_ids', []),
            uniprot_ids=[],  # Would need separate query
            method=entry.get('experimental_method', 'Unknown')
        )

    except Exception as e:
        print(f"    [PDB] Error getting {pdb_id}: {e}")
        return None


def download_pdb_structure(pdb_id: str, output_dir: Path) -> Optional[Path]:
    """Download PDB structure file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{pdb_id}.pdb"

    if output_file.exists():
        return output_file

    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"

    try:
        request = urllib.request.Request(url)
        with urllib.request.urlopen(request, timeout=30) as response:
            content = response.read()

        with open(output_file, 'wb') as f:
            f.write(content)

        return output_file

    except Exception as e:
        print(f"    [PDB] Error downloading {pdb_id}: {e}")
        return None


# =============================================================================
# GEOMETRY ANALYSIS
# =============================================================================

def parse_pdb_atoms(pdb_path: Path) -> List[Dict]:
    """Parse atom coordinates from PDB file."""
    atoms = []

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                try:
                    atom = {
                        'record': line[0:6].strip(),
                        'serial': int(line[6:11].strip()),
                        'name': line[12:16].strip(),
                        'resname': line[17:20].strip(),
                        'chain': line[21].strip(),
                        'resseq': int(line[22:26].strip()),
                        'x': float(line[30:38].strip()),
                        'y': float(line[38:46].strip()),
                        'z': float(line[46:54].strip()),
                    }
                    atoms.append(atom)
                except (ValueError, IndexError):
                    continue

    return atoms


def calculate_distance(atom1: Dict, atom2: Dict) -> float:
    """Calculate Euclidean distance between two atoms."""
    dx = atom1['x'] - atom2['x']
    dy = atom1['y'] - atom2['y']
    dz = atom1['z'] - atom2['z']
    return math.sqrt(dx*dx + dy*dy + dz*dz)


def find_aromatic_receptor_distances(
    atoms: List[Dict],
    ligand_chains: List[str] = None
) -> List[DistanceMeasurement]:
    """Find distances from aromatic ligand atoms to receptor atoms.

    Looks for Trp, Tyr, Phe in ligand and measures to nearest receptor atoms.
    """
    measurements = []

    # Separate ligand and receptor atoms
    # Heuristic: HETATM records are often ligands, or chains with few residues
    chain_residue_counts = {}
    for atom in atoms:
        chain = atom['chain']
        if chain not in chain_residue_counts:
            chain_residue_counts[chain] = set()
        chain_residue_counts[chain].add(atom['resseq'])

    # Small chains (<20 residues) or HETATM are likely ligands
    ligand_atoms = []
    receptor_atoms = []

    for atom in atoms:
        chain = atom['chain']
        is_small_chain = len(chain_residue_counts.get(chain, [])) < 20
        is_hetatm = atom['record'] == 'HETATM'

        # Check if aromatic anchor residue
        is_aromatic_anchor = atom['resname'] in AROMATIC_ANCHORS

        if is_hetatm or (is_small_chain and is_aromatic_anchor):
            ligand_atoms.append(atom)
        else:
            receptor_atoms.append(atom)

    # Find aromatic anchor atoms in ligand
    aromatic_ligand_atoms = []
    for atom in ligand_atoms:
        resname = atom['resname']
        if resname in AROMATIC_ANCHORS:
            if atom['name'] in AROMATIC_ANCHORS[resname]:
                aromatic_ligand_atoms.append(atom)

    if not aromatic_ligand_atoms:
        # If no standard aromatics, look for any aromatic carbons in HETATM
        for atom in ligand_atoms:
            if atom['record'] == 'HETATM' and atom['name'].startswith('C'):
                aromatic_ligand_atoms.append(atom)

    # Measure distances to receptor
    for lig_atom in aromatic_ligand_atoms[:50]:  # Limit for performance
        for rec_atom in receptor_atoms:
            # Only consider non-hydrogen receptor atoms
            if rec_atom['name'].startswith('H'):
                continue

            dist = calculate_distance(lig_atom, rec_atom)

            # Only record distances in relevant range (3-12 Å)
            if 3.0 <= dist <= 12.0:
                matches_z2 = abs(dist - Z2_DISTANCE) <= Z2_TOLERANCE

                measurements.append(DistanceMeasurement(
                    pdb_id="",  # Will be filled in
                    ligand_residue=f"{lig_atom['resname']}{lig_atom['resseq']}",
                    ligand_atom=lig_atom['name'],
                    receptor_residue=f"{rec_atom['resname']}{rec_atom['resseq']}",
                    receptor_atom=rec_atom['name'],
                    distance=dist,
                    matches_z2=matches_z2
                ))

    return measurements


def analyze_pdb_structure(pdb_path: Path, pdb_id: str) -> List[DistanceMeasurement]:
    """Analyze a single PDB structure for Z² geometry matches."""
    atoms = parse_pdb_atoms(pdb_path)

    if not atoms:
        return []

    measurements = find_aromatic_receptor_distances(atoms)

    # Fill in PDB ID
    for m in measurements:
        m.pdb_id = pdb_id

    return measurements


def create_distance_histogram(distances: List[float], bin_size: float = 0.5) -> Dict[str, int]:
    """Create histogram of distances."""
    histogram = {}

    for d in distances:
        bin_start = math.floor(d / bin_size) * bin_size
        bin_label = f"{bin_start:.1f}-{bin_start + bin_size:.1f}"
        histogram[bin_label] = histogram.get(bin_label, 0) + 1

    return dict(sorted(histogram.items()))


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def analyze_z2_geometry(
    uniprot_id: str,
    target_name: str,
    output_dir: Path,
    max_structures: int = 10
) -> Z2ValidationResult:
    """Analyze PDB structures for Z² geometry validation."""
    print(f"\n    {'='*60}")
    print(f"    Z² GEOMETRY ANALYSIS: {uniprot_id}")
    print(f"    {'='*60}")
    print(f"    Target: {target_name}")
    print(f"    Expected distance: {Z2_DISTANCE:.4f} Å ± {Z2_TOLERANCE} Å")

    # Search PDB
    pdb_ids = search_pdb_by_uniprot(uniprot_id, max_results=max_structures)

    if not pdb_ids:
        print(f"    No PDB structures found for {uniprot_id}")
        return Z2ValidationResult(
            uniprot_id=uniprot_id,
            target_name=target_name,
            n_structures=0,
            n_distances_measured=0,
            n_z2_matches=0,
            z2_match_rate=0.0,
            distances=[],
            distance_histogram={},
            mean_distance=0.0,
            std_distance=0.0
        )

    # Download and analyze structures
    pdb_dir = output_dir / "pdb_structures"
    all_measurements = []

    for pdb_id in pdb_ids[:max_structures]:
        print(f"    Analyzing {pdb_id}...")

        pdb_path = download_pdb_structure(pdb_id, pdb_dir)
        if pdb_path:
            measurements = analyze_pdb_structure(pdb_path, pdb_id)
            all_measurements.extend(measurements)
            print(f"        Found {len(measurements)} distance measurements")

    # Calculate statistics
    all_distances = [m.distance for m in all_measurements]
    z2_matches = [m for m in all_measurements if m.matches_z2]

    mean_dist = sum(all_distances) / len(all_distances) if all_distances else 0.0
    std_dist = 0.0
    if len(all_distances) > 1:
        variance = sum((d - mean_dist)**2 for d in all_distances) / len(all_distances)
        std_dist = math.sqrt(variance)

    histogram = create_distance_histogram(all_distances)

    result = Z2ValidationResult(
        uniprot_id=uniprot_id,
        target_name=target_name,
        n_structures=len(pdb_ids),
        n_distances_measured=len(all_measurements),
        n_z2_matches=len(z2_matches),
        z2_match_rate=len(z2_matches) / len(all_measurements) if all_measurements else 0.0,
        distances=all_measurements[:100],  # Keep top 100
        distance_histogram=histogram,
        mean_distance=mean_dist,
        std_distance=std_dist
    )

    # Print results
    print(f"\n    RESULTS:")
    print(f"    {'─'*50}")
    print(f"    Structures analyzed: {result.n_structures}")
    print(f"    Total distances measured: {result.n_distances_measured}")
    print(f"    Z² matches (±{Z2_TOLERANCE} Å): {result.n_z2_matches}")
    print(f"    Z² match rate: {result.z2_match_rate:.1%}")
    print(f"    Mean distance: {result.mean_distance:.3f} Å")
    print(f"    Std deviation: {result.std_distance:.3f} Å")

    print(f"\n    DISTANCE HISTOGRAM:")
    print(f"    {'─'*50}")
    for bin_label, count in histogram.items():
        bar = '█' * min(count // 5, 40)
        z2_marker = " ← Z²" if "5.5-6.0" in bin_label or "6.0-6.5" in bin_label else ""
        print(f"    {bin_label} Å: {bar} ({count}){z2_marker}")

    # Show best Z² matches
    if z2_matches:
        print(f"\n    TOP Z² GEOMETRY MATCHES:")
        print(f"    {'─'*50}")
        best_matches = sorted(z2_matches, key=lambda x: abs(x.distance - Z2_DISTANCE))[:5]
        for m in best_matches:
            deviation = m.distance - Z2_DISTANCE
            print(f"    {m.pdb_id}: {m.ligand_residue}.{m.ligand_atom} → {m.receptor_residue}.{m.receptor_atom}")
            print(f"        Distance: {m.distance:.3f} Å (deviation: {deviation:+.3f} Å)")

    print(f"    {'='*60}\n")

    return result


def run_full_analysis(
    targets: List[Tuple[str, str]],
    output_dir: Path
) -> Dict[str, Z2ValidationResult]:
    """Run Z² geometry analysis on multiple targets."""
    print("\n" + "="*70)
    print("Z² BINDING GEOMETRY VALIDATION")
    print("="*70)
    print(f"    Z² distance: {Z2_DISTANCE:.6f} Å")
    print(f"    Tolerance: ±{Z2_TOLERANCE} Å")
    print(f"    Targets: {len(targets)}")

    results = {}

    for uniprot_id, name in targets:
        result = analyze_z2_geometry(uniprot_id, name, output_dir)
        results[uniprot_id] = result

    # Summary
    print("\n" + "="*70)
    print("SUMMARY: Z² GEOMETRY VALIDATION")
    print("="*70)

    print(f"\n    {'Target':<20} {'Structures':<12} {'Distances':<12} {'Z² Match Rate'}")
    print(f"    {'-'*60}")

    total_matches = 0
    total_distances = 0

    for uid, result in results.items():
        print(f"    {uid:<20} {result.n_structures:<12} {result.n_distances_measured:<12} {result.z2_match_rate:.1%}")
        total_matches += result.n_z2_matches
        total_distances += result.n_distances_measured

    overall_rate = total_matches / total_distances if total_distances > 0 else 0.0
    print(f"    {'-'*60}")
    print(f"    {'OVERALL':<20} {'':<12} {total_distances:<12} {overall_rate:.1%}")

    # Interpret results
    print(f"\n    INTERPRETATION:")
    print(f"    {'─'*50}")
    if overall_rate > 0.15:
        print(f"    ✓ STRONG SIGNAL: {overall_rate:.1%} of binding distances match Z² constant")
        print(f"      This suggests Z² geometry is relevant to actual drug binding.")
    elif overall_rate > 0.08:
        print(f"    ~ MODERATE SIGNAL: {overall_rate:.1%} of distances match Z² constant")
        print(f"      Z² geometry appears in binding, but not dominant.")
    else:
        print(f"    ? WEAK SIGNAL: {overall_rate:.1%} of distances match Z² constant")
        print(f"      Further investigation needed.")

    print("="*70 + "\n")

    # Save results
    output_file = output_dir / "z2_geometry_analysis.json"
    output_data = {
        'z2_distance': Z2_DISTANCE,
        'tolerance': Z2_TOLERANCE,
        'results': {uid: asdict(r) for uid, r in results.items()}
    }

    # Convert DistanceMeasurement objects
    for uid, r in output_data['results'].items():
        r['distances'] = [asdict(d) for d in results[uid].distances]

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2, default=str)

    print(f"    Saved: {output_file}")

    return results


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run Z² geometry analysis on validated targets."""
    import argparse

    parser = argparse.ArgumentParser(description="Z² Binding Geometry Analysis")
    parser.add_argument("--targets", nargs="+", help="UniProt IDs to analyze")
    parser.add_argument("--output", type=Path, help="Output directory")
    parser.add_argument("--max-structures", type=int, default=10, help="Max PDB structures per target")
    args = parser.parse_args()

    # Default targets - structured targets from IDP filter
    if args.targets:
        targets = [(t, t) for t in args.targets]
    else:
        targets = [
            ("P30559", "Oxytocin receptor"),
            ("P04578", "C2_Homodimer_A gp120"),
        ]

    output_dir = args.output or Path(__file__).parent.parent / "z2_geometry_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    results = run_full_analysis(targets, output_dir)

    return results


if __name__ == "__main__":
    main()
