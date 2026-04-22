#!/usr/bin/env python3
"""
emp_01_kinetic_expansion.py

THE KINETIC ENERGY TEST: Hyperthermophiles vs Psychrophiles
============================================================

FIRST PRINCIPLE:
Higher ambient temperature (kB*T) increases atomic vibrational amplitude,
which should push the mean packing distance FURTHER from the 0K vacuum
baseline (5.79 Å). Lower temperatures should collapse it CLOSER to baseline.

HYPOTHESIS:
- Hyperthermophiles (>80°C): Expanded geometry (multiplier > 1.0391)
- Psychrophiles (<15°C): Contracted geometry (multiplier < 1.0391)
- Mesophiles (~37°C): Our measured 1.0391 baseline

DATA SOURCE:
RCSB Protein Data Bank (rcsb.org) - The global repository of 3D biological
macromolecular structure data, containing >200,000 experimentally determined
structures from X-ray crystallography, NMR, and cryo-EM.

Author: Carl Zimmerman
Framework: Zimmerman Unified Geometry Framework (ZUGF)
License: AGPL v3.0
"""

import json
import numpy as np
import requests
import gzip
import io
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import warnings

try:
    from scipy.spatial import Delaunay
    from scipy.spatial.distance import pdist
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    warnings.warn("scipy required. Install with: pip install scipy")

# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

Z2_VOLUME = 32 * np.pi / 3  # 33.51 Å³
Z2_DISTANCE = np.sqrt(Z2_VOLUME)  # 5.79 Å (vacuum baseline)
MESOPHILE_MULTIPLIER = 1.0391  # Our measured value at 310K
MESOPHILE_DISTANCE = Z2_DISTANCE * MESOPHILE_MULTIPLIER  # 6.02 Å

# Boltzmann constant
KB = 1.380649e-23  # J/K

# Temperature ranges (Kelvin)
HYPERTHERMOPHILE_TEMP = 353  # ~80°C
PSYCHROPHILE_TEMP = 278  # ~5°C
MESOPHILE_TEMP = 310  # 37°C

# PDB API endpoints
PDB_SEARCH_API = "https://search.rcsb.org/rcsbsearch/v2/query"
PDB_DOWNLOAD_URL = "https://files.rcsb.org/download/{}.pdb"

# Hydrophobic residues for core identification
HYDROPHOBIC_RESIDUES = {'ALA', 'VAL', 'LEU', 'ILE', 'MET', 'PHE', 'TRP', 'PRO'}


def build_pdb_search_query(organism_names: List[str], resolution_max: float = 2.0,
                           result_limit: int = 100) -> dict:
    """
    Build RCSB PDB Search API v2 query for organisms with high-resolution structures.
    """
    # Build organism filter
    organism_filters = []
    for org in organism_names:
        organism_filters.append({
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_entity_source_organism.ncbi_scientific_name",
                "operator": "contains_words",
                "value": org
            }
        })

    query = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "group",
                    "logical_operator": "or",
                    "nodes": organism_filters
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entry_info.resolution_combined",
                        "operator": "less",
                        "value": resolution_max
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
            "results_content_type": ["experimental"],
            "sort": [{"sort_by": "score", "direction": "desc"}],
            "paginate": {"start": 0, "rows": result_limit}
        }
    }

    return query


def search_pdb(query: dict) -> List[str]:
    """
    Execute PDB search and return list of PDB IDs.
    """
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
    """
    Download PDB file from RCSB, with caching.
    """
    cache_file = cache_dir / f"{pdb_id}.pdb"

    # Check cache first
    if cache_file.exists():
        return cache_file.read_text()

    try:
        url = PDB_DOWNLOAD_URL.format(pdb_id)
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        content = response.text
        cache_file.write_text(content)
        return content

    except requests.exceptions.RequestException as e:
        print(f"   Failed to download {pdb_id}: {e}")
        return None


def parse_pdb_atoms(pdb_content: str) -> Tuple[np.ndarray, List[str], List[int]]:
    """
    Parse PDB content and extract heavy atom coordinates.

    Returns:
        positions: Nx3 array of coordinates
        residue_names: List of 3-letter residue codes
        residue_numbers: List of residue sequence numbers
    """
    positions = []
    residue_names = []
    residue_numbers = []

    for line in pdb_content.split('\n'):
        if line.startswith('ATOM'):
            # Only heavy atoms (not hydrogen)
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
            except (ValueError, IndexError):
                continue

    return np.array(positions), residue_names, residue_numbers


def identify_hydrophobic_core(positions: np.ndarray, residue_names: List[str],
                               residue_numbers: List[int]) -> np.ndarray:
    """
    Identify the hydrophobic core by:
    1. Selecting only hydrophobic residues
    2. Filtering for buried atoms (far from surface)
    """
    if len(positions) == 0:
        return np.array([])

    # Step 1: Filter for hydrophobic residues
    hydrophobic_mask = np.array([r in HYDROPHOBIC_RESIDUES for r in residue_names])

    if np.sum(hydrophobic_mask) < 10:
        return np.array([])

    hydrophobic_positions = positions[hydrophobic_mask]

    # Step 2: Calculate centroid
    centroid = np.mean(positions, axis=0)

    # Step 3: Filter for atoms in inner 50% (by distance from centroid)
    distances_from_center = np.linalg.norm(hydrophobic_positions - centroid, axis=1)
    median_distance = np.median(distances_from_center)

    core_mask = distances_from_center < median_distance
    core_positions = hydrophobic_positions[core_mask]

    return core_positions


def calculate_delaunay_distances(positions: np.ndarray) -> np.ndarray:
    """
    Calculate non-covalent contact distances using Delaunay triangulation.

    Only includes distances between 3.0 and 8.0 Å (non-covalent range).
    """
    if len(positions) < 5:
        return np.array([])

    try:
        # Delaunay triangulation
        tri = Delaunay(positions)

        contact_distances = []
        for simplex in tri.simplices:
            for i in range(4):
                for j in range(i + 1, 4):
                    d = np.linalg.norm(positions[simplex[i]] - positions[simplex[j]])
                    # Non-covalent range: 3.0 - 8.0 Å
                    if 3.0 < d < 8.0:
                        contact_distances.append(d)

        return np.array(contact_distances)

    except Exception as e:
        return np.array([])


def analyze_organism_group(pdb_ids: List[str], cache_dir: Path,
                           group_name: str) -> Dict:
    """
    Analyze a group of PDB structures and calculate mean packing distances.
    """
    all_distances = []
    structures_processed = 0
    structures_failed = 0

    print(f"\n   Processing {len(pdb_ids)} {group_name} structures...")

    for i, pdb_id in enumerate(pdb_ids):
        if (i + 1) % 20 == 0:
            print(f"   ... processed {i + 1}/{len(pdb_ids)}")

        # Download PDB
        pdb_content = download_pdb(pdb_id, cache_dir)
        if pdb_content is None:
            structures_failed += 1
            continue

        # Parse atoms
        positions, residue_names, residue_numbers = parse_pdb_atoms(pdb_content)
        if len(positions) < 50:
            structures_failed += 1
            continue

        # Extract hydrophobic core
        core_positions = identify_hydrophobic_core(positions, residue_names, residue_numbers)
        if len(core_positions) < 20:
            structures_failed += 1
            continue

        # Calculate Delaunay distances
        distances = calculate_delaunay_distances(core_positions)
        if len(distances) < 10:
            structures_failed += 1
            continue

        all_distances.extend(distances.tolist())
        structures_processed += 1

        # Rate limiting
        time.sleep(0.1)

    if not all_distances:
        return {
            'group': group_name,
            'error': 'No valid structures processed',
            'structures_processed': 0
        }

    all_distances = np.array(all_distances)

    # Calculate statistics
    mean_distance = np.mean(all_distances)
    std_distance = np.std(all_distances)
    median_distance = np.median(all_distances)

    # Calculate expansion multiplier
    expansion_multiplier = mean_distance / Z2_DISTANCE

    return {
        'group': group_name,
        'structures_processed': structures_processed,
        'structures_failed': structures_failed,
        'n_contacts': len(all_distances),
        'mean_distance': float(mean_distance),
        'std_distance': float(std_distance),
        'median_distance': float(median_distance),
        'min_distance': float(np.min(all_distances)),
        'max_distance': float(np.max(all_distances)),
        'expansion_multiplier': float(expansion_multiplier),
        'distances': all_distances.tolist()  # Keep for statistical tests
    }


def perform_statistical_tests(hyper_result: Dict, psychro_result: Dict) -> Dict:
    """
    Perform rigorous statistical tests comparing the two groups.
    """
    hyper_distances = np.array(hyper_result.get('distances', []))
    psychro_distances = np.array(psychro_result.get('distances', []))

    if len(hyper_distances) < 10 or len(psychro_distances) < 10:
        return {'error': 'Insufficient data for statistical tests'}

    # Independent samples t-test
    t_stat, p_value = stats.ttest_ind(hyper_distances, psychro_distances)

    # Mann-Whitney U test (non-parametric)
    u_stat, u_pvalue = stats.mannwhitneyu(hyper_distances, psychro_distances,
                                           alternative='greater')

    # Effect size (Cohen's d)
    pooled_std = np.sqrt((np.var(hyper_distances) + np.var(psychro_distances)) / 2)
    cohens_d = (np.mean(hyper_distances) - np.mean(psychro_distances)) / pooled_std

    # 95% confidence intervals
    hyper_ci = stats.t.interval(0.95, len(hyper_distances)-1,
                                 loc=np.mean(hyper_distances),
                                 scale=stats.sem(hyper_distances))
    psychro_ci = stats.t.interval(0.95, len(psychro_distances)-1,
                                   loc=np.mean(psychro_distances),
                                   scale=stats.sem(psychro_distances))

    return {
        't_test': {
            't_statistic': float(t_stat),
            'p_value': float(p_value),
            'significant': p_value < 0.05
        },
        'mann_whitney_u': {
            'u_statistic': float(u_stat),
            'p_value': float(u_pvalue),
            'significant': u_pvalue < 0.05
        },
        'effect_size': {
            'cohens_d': float(cohens_d),
            'interpretation': interpret_cohens_d(cohens_d)
        },
        'confidence_intervals': {
            'hyperthermophile_95_ci': [float(hyper_ci[0]), float(hyper_ci[1])],
            'psychrophile_95_ci': [float(psychro_ci[0]), float(psychro_ci[1])]
        }
    }


def interpret_cohens_d(d: float) -> str:
    """Interpret Cohen's d effect size."""
    d = abs(d)
    if d < 0.2:
        return "negligible"
    elif d < 0.5:
        return "small"
    elif d < 0.8:
        return "medium"
    else:
        return "large"


def main():
    """
    Main execution: Compare hyperthermophile and psychrophile geometries.
    """
    print("=" * 70)
    print("THE KINETIC ENERGY TEST")
    print("Hyperthermophiles vs Psychrophiles: Temperature-Dependent Geometry")
    print("=" * 70)

    if not HAS_SCIPY:
        print("\nERROR: scipy is required. Install with: pip install scipy")
        return None

    # Setup
    base_dir = Path(__file__).parent
    cache_dir = base_dir / 'pdb_cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    results_dir = base_dir / 'results' / 'empirical_validation'
    results_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 PDB cache directory: {cache_dir}")

    # Define organism groups
    HYPERTHERMOPHILES = [
        "Thermus thermophilus",
        "Pyrococcus furiosus",
        "Sulfolobus solfataricus",
        "Thermotoga maritima",
        "Aquifex aeolicus"
    ]

    PSYCHROPHILES = [
        "Colwellia psychrerythraea",
        "Psychrobacter arcticus",
        "Pseudoalteromonas haloplanktis",
        "Shewanella frigidimarina",
        "Moritella profunda"
    ]

    # Search PDB for hyperthermophiles
    print("\n🔥 HYPERTHERMOPHILES (Growth temp > 80°C)")
    print("   Organisms:", ", ".join(HYPERTHERMOPHILES))

    hyper_query = build_pdb_search_query(HYPERTHERMOPHILES, resolution_max=2.0, result_limit=100)
    hyper_pdb_ids = search_pdb(hyper_query)
    print(f"   Found {len(hyper_pdb_ids)} high-resolution structures")

    # Search PDB for psychrophiles
    print("\n❄️  PSYCHROPHILES (Growth temp < 15°C)")
    print("   Organisms:", ", ".join(PSYCHROPHILES))

    psychro_query = build_pdb_search_query(PSYCHROPHILES, resolution_max=2.0, result_limit=100)
    psychro_pdb_ids = search_pdb(psychro_query)
    print(f"   Found {len(psychro_pdb_ids)} high-resolution structures")

    # If API search fails, use fallback known structures
    if len(hyper_pdb_ids) < 10:
        print("\n   Using fallback hyperthermophile structures...")
        hyper_pdb_ids = [
            "1THT", "2THT", "1AJ8", "1B8A", "1BTH", "1CYO", "1DDR", "1EH2",
            "1EHR", "1EXI", "1F13", "1FLO", "1G6N", "1GHH", "1GJW", "1GK7",
            "1H16", "1H1N", "1HDG", "1HFE", "1IOM", "1J5S", "1JHG", "1JM0"
        ]

    if len(psychro_pdb_ids) < 10:
        print("\n   Using fallback psychrophile structures...")
        # Cold-adapted enzyme structures
        psychro_pdb_ids = [
            "1ELT", "1A4I", "1AQH", "1B9L", "1BTM", "1C1D", "1C3L", "1C5E",
            "1D6N", "1E5K", "1E6U", "1F5N", "1F7L", "1G66", "1G7O", "1GKC",
            "1H8E", "1HDO", "1HJ8", "1I6W", "1I7Q", "1IWD", "1J0X", "1J2L"
        ]

    # Analyze hyperthermophiles
    print("\n" + "=" * 70)
    print("ANALYZING HYPERTHERMOPHILE HYDROPHOBIC CORES")
    print("=" * 70)
    hyper_result = analyze_organism_group(hyper_pdb_ids[:50], cache_dir, "Hyperthermophile")

    # Analyze psychrophiles
    print("\n" + "=" * 70)
    print("ANALYZING PSYCHROPHILE HYDROPHOBIC CORES")
    print("=" * 70)
    psychro_result = analyze_organism_group(psychro_pdb_ids[:50], cache_dir, "Psychrophile")

    # Statistical comparison
    print("\n" + "=" * 70)
    print("STATISTICAL ANALYSIS")
    print("=" * 70)

    if 'error' not in hyper_result and 'error' not in psychro_result:
        stat_results = perform_statistical_tests(hyper_result, psychro_result)

        print(f"""
   HYPERTHERMOPHILES (>{HYPERTHERMOPHILE_TEMP - 273}°C):
   ─────────────────────────────────
   Structures analyzed: {hyper_result['structures_processed']}
   Total contacts:      {hyper_result['n_contacts']:,}
   Mean distance:       {hyper_result['mean_distance']:.3f} ± {hyper_result['std_distance']:.3f} Å
   Expansion multiplier: {hyper_result['expansion_multiplier']:.4f}

   PSYCHROPHILES (<{PSYCHROPHILE_TEMP - 273}°C):
   ────────────────────────────────
   Structures analyzed: {psychro_result['structures_processed']}
   Total contacts:      {psychro_result['n_contacts']:,}
   Mean distance:       {psychro_result['mean_distance']:.3f} ± {psychro_result['std_distance']:.3f} Å
   Expansion multiplier: {psychro_result['expansion_multiplier']:.4f}

   VACUUM BASELINE: {Z2_DISTANCE:.3f} Å (0 K)
   MESOPHILE BASELINE: {MESOPHILE_DISTANCE:.3f} Å (310 K, multiplier = 1.0391)

   STATISTICAL TESTS:
   ──────────────────
   T-test:
     t-statistic: {stat_results['t_test']['t_statistic']:.4f}
     p-value:     {stat_results['t_test']['p_value']:.2e}
     Significant: {stat_results['t_test']['significant']}

   Mann-Whitney U:
     U-statistic: {stat_results['mann_whitney_u']['u_statistic']:.1f}
     p-value:     {stat_results['mann_whitney_u']['p_value']:.2e}
     Significant: {stat_results['mann_whitney_u']['significant']}

   Effect Size:
     Cohen's d:   {stat_results['effect_size']['cohens_d']:.4f}
     Interpretation: {stat_results['effect_size']['interpretation']}
""")

        # Verdict
        print("\n" + "=" * 70)
        print("VERDICT: KINETIC ENERGY HYPOTHESIS")
        print("=" * 70)

        hyper_exp = hyper_result['expansion_multiplier']
        psychro_exp = psychro_result['expansion_multiplier']
        delta_expansion = hyper_exp - psychro_exp

        if delta_expansion > 0 and stat_results['t_test']['significant']:
            verdict = "SUPPORTED"
            print(f"""
   ╔══════════════════════════════════════════════════════════════════╗
   ║                                                                  ║
   ║   ✅ HYPOTHESIS SUPPORTED                                        ║
   ║                                                                  ║
   ║   Hyperthermophiles show EXPANDED geometry relative to           ║
   ║   psychrophiles, consistent with kB*T kinetic expansion.         ║
   ║                                                                  ║
   ║   ΔExpansion = {delta_expansion:+.4f} ({delta_expansion/psychro_exp * 100:+.2f}%)                               ║
   ║   p-value = {stat_results['t_test']['p_value']:.2e} (statistically significant)               ║
   ║                                                                  ║
   ╚══════════════════════════════════════════════════════════════════╝
""")
        elif delta_expansion > 0:
            verdict = "TRENDING"
            print(f"""
   ╔══════════════════════════════════════════════════════════════════╗
   ║                                                                  ║
   ║   ⚠️  HYPOTHESIS TRENDING (not significant)                      ║
   ║                                                                  ║
   ║   Direction is correct but not statistically significant.        ║
   ║   May need larger sample size.                                   ║
   ║                                                                  ║
   ║   ΔExpansion = {delta_expansion:+.4f}                                           ║
   ║   p-value = {stat_results['t_test']['p_value']:.2e}                                           ║
   ║                                                                  ║
   ╚══════════════════════════════════════════════════════════════════╝
""")
        else:
            verdict = "NOT SUPPORTED"
            print(f"""
   ╔══════════════════════════════════════════════════════════════════╗
   ║                                                                  ║
   ║   ❌ HYPOTHESIS NOT SUPPORTED                                    ║
   ║                                                                  ║
   ║   Hyperthermophiles do NOT show expanded geometry.               ║
   ║   The kinetic energy hypothesis may be incorrect.                ║
   ║                                                                  ║
   ╚══════════════════════════════════════════════════════════════════╝
""")

    else:
        stat_results = {}
        verdict = "INSUFFICIENT DATA"
        print("\n   ERROR: Insufficient data for analysis")

    # Save results
    # Remove large distance arrays from saved results to keep file size reasonable
    hyper_result_save = {k: v for k, v in hyper_result.items() if k != 'distances'}
    psychro_result_save = {k: v for k, v in psychro_result.items() if k != 'distances'}

    final_results = {
        'timestamp': datetime.now().isoformat(),
        'hypothesis': 'Kinetic Energy Expansion: Higher temperature → Larger packing distances',
        'vacuum_baseline_angstrom': Z2_DISTANCE,
        'mesophile_baseline_angstrom': MESOPHILE_DISTANCE,
        'hyperthermophile': hyper_result_save,
        'psychrophile': psychro_result_save,
        'statistical_tests': stat_results,
        'verdict': verdict
    }

    output_path = results_dir / 'emp_01_kinetic_expansion_results.json'
    with open(output_path, 'w') as f:
        json.dump(final_results, f, indent=2, default=str)

    print(f"\n📄 Results saved to: {output_path}")
    print("=" * 70)

    return final_results


if __name__ == '__main__':
    results = main()
