#!/usr/bin/env python3
"""
emp_02_dielectric_shielding.py

THE DIELECTRIC SOLVENT TEST: Membrane vs Globular Proteins
===========================================================

FIRST PRINCIPLE:
Water is highly polar (ε≈80) and physically permeates protein crevices,
acting as a geometric wedge that pushes atoms apart. Lipid bilayers are
non-polar (ε≈2) and exclude water entirely.

HYPOTHESIS:
Proteins buried inside lipid membranes should pack CLOSER to the pristine
vacuum geometry (5.79 Å) than water-soluble globular proteins because:
1. No water molecules inserting between atoms
2. Lower dielectric screening of electrostatic interactions
3. Stronger direct atom-atom contacts

Expected Results:
- Transmembrane helices: multiplier ≈ 1.01-1.02 (near vacuum)
- Globular protein cores: multiplier ≈ 1.04 (water-expanded)

DATA SOURCE:
RCSB Protein Data Bank + OPM (Orientations of Proteins in Membranes)

Author: Carl Zimmerman
Framework: Zimmerman Unified Geometry Framework (ZUGF)
License: AGPL v3.0
"""

import json
import numpy as np
import requests
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings

try:
    from scipy.spatial import Delaunay
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

Z2_VOLUME = 32 * np.pi / 3  # 33.51 Å³
Z2_DISTANCE = np.sqrt(Z2_VOLUME)  # 5.79 Å (vacuum baseline)

# Dielectric constants
WATER_DIELECTRIC = 80.0  # High polarity
LIPID_DIELECTRIC = 2.0   # Low polarity (hydrocarbon)
PROTEIN_INTERIOR = 4.0   # Intermediate

# PDB API
PDB_SEARCH_API = "https://search.rcsb.org/rcsbsearch/v2/query"
PDB_DOWNLOAD_URL = "https://files.rcsb.org/download/{}.pdb"

# Hydrophobic residues
HYDROPHOBIC_RESIDUES = {'ALA', 'VAL', 'LEU', 'ILE', 'MET', 'PHE', 'TRP', 'PRO'}

# Transmembrane-favoring residues (highly hydrophobic)
TM_RESIDUES = {'LEU', 'ILE', 'VAL', 'PHE', 'ALA', 'GLY', 'TRP'}


def build_membrane_protein_query(result_limit: int = 100) -> dict:
    """
    Build query for transmembrane proteins.
    Uses PDBTM/membrane annotation and high resolution.
    """
    query = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "struct_keywords.pdbx_keywords",
                        "operator": "contains_words",
                        "value": "MEMBRANE PROTEIN"
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entry_info.resolution_combined",
                        "operator": "less",
                        "value": 2.5
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entry_info.experimental_method",
                        "operator": "exact_match",
                        "value": "X-RAY DIFFRACTION"
                    }
                }
            ]
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": 0, "rows": result_limit}
        }
    }
    return query


def build_globular_protein_query(result_limit: int = 100) -> dict:
    """
    Build query for soluble globular proteins.
    Explicitly excludes membrane proteins.
    """
    query = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "struct_keywords.pdbx_keywords",
                        "operator": "contains_words",
                        "value": "HYDROLASE"  # Common soluble enzyme class
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entry_info.resolution_combined",
                        "operator": "less",
                        "value": 2.0
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entry_info.experimental_method",
                        "operator": "exact_match",
                        "value": "X-RAY DIFFRACTION"
                    }
                }
            ]
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": 0, "rows": result_limit}
        }
    }
    return query


def search_pdb(query: dict) -> List[str]:
    """Execute PDB search."""
    try:
        response = requests.post(
            PDB_SEARCH_API,
            json=query,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        response.raise_for_status()
        results = response.json()

        pdb_ids = []
        if "result_set" in results:
            for result in results["result_set"]:
                pdb_ids.append(result["identifier"])
        return pdb_ids

    except requests.exceptions.RequestException as e:
        print(f"   PDB search error: {e}")
        return []


def download_pdb(pdb_id: str, cache_dir: Path) -> Optional[str]:
    """Download PDB file with caching."""
    cache_file = cache_dir / f"{pdb_id}.pdb"

    if cache_file.exists():
        return cache_file.read_text()

    try:
        url = PDB_DOWNLOAD_URL.format(pdb_id)
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        content = response.text
        cache_file.write_text(content)
        return content
    except:
        return None


def parse_pdb_atoms(pdb_content: str) -> Tuple[np.ndarray, List[str], List[int]]:
    """Parse PDB content for heavy atoms."""
    positions = []
    residue_names = []
    residue_numbers = []

    for line in pdb_content.split('\n'):
        if line.startswith('ATOM'):
            element = line[76:78].strip() if len(line) > 76 else line[12:14].strip()
            if element == 'H':
                continue

            try:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                res_name = line[17:20].strip()
                res_num = int(line[22:26])

                positions.append([x, y, z])
                residue_names.append(res_name)
                residue_numbers.append(res_num)
            except:
                continue

    return np.array(positions), residue_names, residue_numbers


def identify_tm_helical_core(positions: np.ndarray, residue_names: List[str]) -> np.ndarray:
    """
    Identify transmembrane helical regions.

    TM helices are characterized by:
    1. High hydrophobicity
    2. Helical secondary structure (approximated by local geometry)
    3. Extended along a single axis (membrane normal)
    """
    if len(positions) < 20:
        return np.array([])

    # Filter for TM-favoring residues
    tm_mask = np.array([r in TM_RESIDUES for r in residue_names])

    if np.sum(tm_mask) < 15:
        return np.array([])

    tm_positions = positions[tm_mask]

    # For TM proteins, the hydrophobic core IS the membrane-spanning region
    # We'll use all TM-favorable residues
    return tm_positions


def identify_globular_core(positions: np.ndarray, residue_names: List[str]) -> np.ndarray:
    """
    Identify the hydrophobic core of a globular protein.

    This core is WATER-BATHED on all sides (unlike TM proteins).
    """
    if len(positions) < 50:
        return np.array([])

    # Filter for hydrophobic residues
    hydrophobic_mask = np.array([r in HYDROPHOBIC_RESIDUES for r in residue_names])

    if np.sum(hydrophobic_mask) < 20:
        return np.array([])

    hydrophobic_positions = positions[hydrophobic_mask]

    # Get the BURIED hydrophobic residues (inner 40%)
    centroid = np.mean(positions, axis=0)
    distances = np.linalg.norm(hydrophobic_positions - centroid, axis=1)

    # Keep inner 40% (most buried)
    threshold = np.percentile(distances, 40)
    core_mask = distances < threshold

    return hydrophobic_positions[core_mask]


def calculate_delaunay_distances(positions: np.ndarray) -> np.ndarray:
    """Calculate non-covalent contact distances."""
    if len(positions) < 5:
        return np.array([])

    try:
        tri = Delaunay(positions)
        distances = []

        for simplex in tri.simplices:
            for i in range(4):
                for j in range(i + 1, 4):
                    d = np.linalg.norm(positions[simplex[i]] - positions[simplex[j]])
                    if 3.0 < d < 8.0:
                        distances.append(d)

        return np.array(distances)
    except:
        return np.array([])


def analyze_protein_group(pdb_ids: List[str], cache_dir: Path,
                          group_name: str, core_extractor) -> Dict:
    """Analyze a group of proteins."""
    all_distances = []
    processed = 0
    failed = 0

    print(f"\n   Processing {len(pdb_ids)} {group_name} structures...")

    for i, pdb_id in enumerate(pdb_ids):
        if (i + 1) % 20 == 0:
            print(f"   ... processed {i + 1}/{len(pdb_ids)}")

        pdb_content = download_pdb(pdb_id, cache_dir)
        if pdb_content is None:
            failed += 1
            continue

        positions, residue_names, _ = parse_pdb_atoms(pdb_content)
        if len(positions) < 50:
            failed += 1
            continue

        core = core_extractor(positions, residue_names)
        if len(core) < 15:
            failed += 1
            continue

        distances = calculate_delaunay_distances(core)
        if len(distances) < 10:
            failed += 1
            continue

        all_distances.extend(distances.tolist())
        processed += 1
        time.sleep(0.1)

    if not all_distances:
        return {'group': group_name, 'error': 'No valid data'}

    all_distances = np.array(all_distances)

    return {
        'group': group_name,
        'structures_processed': processed,
        'structures_failed': failed,
        'n_contacts': len(all_distances),
        'mean_distance': float(np.mean(all_distances)),
        'std_distance': float(np.std(all_distances)),
        'median_distance': float(np.median(all_distances)),
        'expansion_multiplier': float(np.mean(all_distances) / Z2_DISTANCE),
        'distances': all_distances.tolist()
    }


def main():
    """Main execution: Compare membrane vs globular protein geometry."""
    print("=" * 70)
    print("THE DIELECTRIC SOLVENT TEST")
    print("Membrane Proteins vs Globular Proteins: Water Exclusion Effect")
    print("=" * 70)

    if not HAS_SCIPY:
        print("\nERROR: scipy required")
        return None

    # Setup
    base_dir = Path(__file__).parent
    cache_dir = base_dir / 'pdb_cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    results_dir = base_dir / 'results' / 'empirical_validation'
    results_dir.mkdir(parents=True, exist_ok=True)

    print(f"""
   PHYSICAL PRINCIPLE:
   ────────────────────
   Water (ε = {WATER_DIELECTRIC}): High polarity, inserts between atoms, expands geometry
   Lipid (ε = {LIPID_DIELECTRIC}): Low polarity, excludes water, tight packing

   PREDICTION:
   Transmembrane helices → Close to vacuum baseline (5.79 Å)
   Globular protein cores → Expanded (~6.02 Å)
""")

    # Search for membrane proteins
    print("\n🔬 TRANSMEMBRANE PROTEINS (Lipid Environment, ε ≈ 2)")
    tm_query = build_membrane_protein_query(result_limit=100)
    tm_pdb_ids = search_pdb(tm_query)
    print(f"   Found {len(tm_pdb_ids)} membrane protein structures")

    # Fallback TM structures
    if len(tm_pdb_ids) < 10:
        print("   Using known transmembrane structures...")
        tm_pdb_ids = [
            "1BRD", "1C3W", "1E12", "1FX8", "1H2S", "1J4N", "1JB0", "1KF6",
            "1KPK", "1L9H", "1M0L", "1MHS", "1MSL", "1OCC", "1OKC", "1PV6",
            "1R3J", "1RH5", "1SOR", "1U19", "1XIO", "1YEW", "1ZLL", "2A65",
            "2AHY", "2B6O", "2BG9", "2BRD", "2F93", "2HYD", "2IC8", "2JLN"
        ]

    # Search for globular proteins
    print("\n💧 GLOBULAR PROTEINS (Aqueous Environment, ε ≈ 80)")
    glob_query = build_globular_protein_query(result_limit=100)
    glob_pdb_ids = search_pdb(glob_query)
    print(f"   Found {len(glob_pdb_ids)} globular protein structures")

    # Fallback globular structures
    if len(glob_pdb_ids) < 10:
        print("   Using known globular structures...")
        glob_pdb_ids = [
            "1AKE", "1BPI", "1C5E", "1CRN", "1ECA", "1ENH", "1FAS", "1GEN",
            "1HEL", "1HMK", "1IGD", "1L2Y", "1LYZ", "1MBA", "1NXB", "1OVA",
            "1PGB", "1ROP", "1SH1", "1TEN", "1TIM", "1UBQ", "1YCC", "2ACE",
            "2AIT", "2CHS", "2CPL", "2LZM", "2PKA", "2SNS", "3BLM", "3CHY"
        ]

    # Analyze transmembrane proteins
    print("\n" + "=" * 70)
    print("ANALYZING TRANSMEMBRANE PROTEIN CORES")
    print("=" * 70)
    tm_result = analyze_protein_group(
        tm_pdb_ids[:50], cache_dir,
        "Transmembrane",
        identify_tm_helical_core
    )

    # Analyze globular proteins
    print("\n" + "=" * 70)
    print("ANALYZING GLOBULAR PROTEIN CORES")
    print("=" * 70)
    glob_result = analyze_protein_group(
        glob_pdb_ids[:50], cache_dir,
        "Globular",
        identify_globular_core
    )

    # Statistical comparison
    print("\n" + "=" * 70)
    print("RESULTS: DIELECTRIC ENVIRONMENT EFFECT")
    print("=" * 70)

    if 'error' not in tm_result and 'error' not in glob_result:
        tm_distances = np.array(tm_result['distances'])
        glob_distances = np.array(glob_result['distances'])

        # T-test
        t_stat, p_value = stats.ttest_ind(tm_distances, glob_distances)

        # Effect size
        pooled_std = np.sqrt((np.var(tm_distances) + np.var(glob_distances)) / 2)
        cohens_d = (np.mean(glob_distances) - np.mean(tm_distances)) / pooled_std

        print(f"""
   TRANSMEMBRANE CORES (Lipid, ε = {LIPID_DIELECTRIC}):
   ────────────────────────────────────────
   Structures analyzed:  {tm_result['structures_processed']}
   Total contacts:       {tm_result['n_contacts']:,}
   Mean distance:        {tm_result['mean_distance']:.3f} ± {tm_result['std_distance']:.3f} Å
   Expansion multiplier: {tm_result['expansion_multiplier']:.4f}

   GLOBULAR CORES (Water, ε = {WATER_DIELECTRIC}):
   ─────────────────────────────────────────
   Structures analyzed:  {glob_result['structures_processed']}
   Total contacts:       {glob_result['n_contacts']:,}
   Mean distance:        {glob_result['mean_distance']:.3f} ± {glob_result['std_distance']:.3f} Å
   Expansion multiplier: {glob_result['expansion_multiplier']:.4f}

   VACUUM BASELINE: {Z2_DISTANCE:.3f} Å

   STATISTICAL COMPARISON:
   ───────────────────────
   T-test:
     t-statistic: {t_stat:.4f}
     p-value:     {p_value:.2e}
     Significant: {p_value < 0.05}

   Effect Size:
     Cohen's d:   {cohens_d:.4f}
     Globular {cohens_d:.2f}σ more expanded than TM

   DISTANCE FROM VACUUM:
     TM proteins:      {tm_result['mean_distance'] - Z2_DISTANCE:.3f} Å above vacuum
     Globular proteins: {glob_result['mean_distance'] - Z2_DISTANCE:.3f} Å above vacuum
""")

        # Verdict
        print("\n" + "=" * 70)
        print("VERDICT: DIELECTRIC SHIELDING HYPOTHESIS")
        print("=" * 70)

        tm_expansion = tm_result['expansion_multiplier']
        glob_expansion = glob_result['expansion_multiplier']
        delta = glob_expansion - tm_expansion

        # Check if TM is closer to vacuum than globular
        tm_vacuum_distance = abs(tm_expansion - 1.0)
        glob_vacuum_distance = abs(glob_expansion - 1.0)

        if tm_vacuum_distance < glob_vacuum_distance and p_value < 0.05:
            verdict = "SUPPORTED"
            print(f"""
   ╔══════════════════════════════════════════════════════════════════╗
   ║                                                                  ║
   ║   ✅ HYPOTHESIS SUPPORTED                                        ║
   ║                                                                  ║
   ║   Transmembrane proteins pack TIGHTER than globular proteins.    ║
   ║   Water exclusion brings TM geometry CLOSER to vacuum baseline.  ║
   ║                                                                  ║
   ║   TM expansion:  {tm_expansion:.4f} (distance from 1.0: {tm_vacuum_distance:.4f})           ║
   ║   Glob expansion: {glob_expansion:.4f} (distance from 1.0: {glob_vacuum_distance:.4f})           ║
   ║   Δ: {delta:.4f} (p = {p_value:.2e})                                       ║
   ║                                                                  ║
   ║   PHYSICAL INTERPRETATION:                                       ║
   ║   Water acts as a GEOMETRIC WEDGE, physically pushing atoms      ║
   ║   apart. Without water, atoms collapse toward vacuum packing.    ║
   ║                                                                  ║
   ╚══════════════════════════════════════════════════════════════════╝
""")
        else:
            verdict = "NOT SUPPORTED" if not p_value < 0.05 else "INCONCLUSIVE"
            print(f"""
   ╔══════════════════════════════════════════════════════════════════╗
   ║                                                                  ║
   ║   ⚠️  HYPOTHESIS {verdict:^20}                      ║
   ║                                                                  ║
   ║   TM expansion:  {tm_expansion:.4f}                                        ║
   ║   Glob expansion: {glob_expansion:.4f}                                        ║
   ║   p-value: {p_value:.2e}                                           ║
   ║                                                                  ║
   ╚══════════════════════════════════════════════════════════════════╝
""")

        stat_results = {
            't_test': {'t_statistic': float(t_stat), 'p_value': float(p_value)},
            'cohens_d': float(cohens_d)
        }

    else:
        stat_results = {}
        verdict = "INSUFFICIENT DATA"
        print("\n   ERROR: Insufficient data")

    # Save results
    tm_save = {k: v for k, v in tm_result.items() if k != 'distances'}
    glob_save = {k: v for k, v in glob_result.items() if k != 'distances'}

    final_results = {
        'timestamp': datetime.now().isoformat(),
        'hypothesis': 'Dielectric Shielding: Water expands geometry, lipid preserves vacuum packing',
        'vacuum_baseline': Z2_DISTANCE,
        'water_dielectric': WATER_DIELECTRIC,
        'lipid_dielectric': LIPID_DIELECTRIC,
        'transmembrane': tm_save,
        'globular': glob_save,
        'statistical_tests': stat_results,
        'verdict': verdict
    }

    output_path = results_dir / 'emp_02_dielectric_shielding_results.json'
    with open(output_path, 'w') as f:
        json.dump(final_results, f, indent=2)

    print(f"\n📄 Results saved to: {output_path}")
    print("=" * 70)

    return final_results


if __name__ == '__main__':
    results = main()
