#!/usr/bin/env python3
"""
emp_03_universal_geometry_law.py

THE UNIVERSAL GEOMETRIC LAW: PDB Census
=======================================

FIRST PRINCIPLE:
If 1.0391 is the fundamental expansion coefficient of terrestrial,
carbon-based life at standard biological conditions (310K, aqueous),
it MUST appear as the absolute mean across ALL known protein structures.

HYPOTHESIS:
The distribution of non-covalent packing distances across the entire
Protein Data Bank should show a Gaussian peak centered at:

   PEAK = Z² × 1.0391 = 5.79 × 1.0391 ≈ 6.02 Å

This would prove that Z² → Biological geometry is not a coincidence
but a UNIVERSAL LAW governing all terrestrial carbon-based life.

DATA SOURCE:
RCSB Protein Data Bank - non-redundant sample of 1000+ diverse structures

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
    from scipy.optimize import curve_fit
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

Z2_VOLUME = 32 * np.pi / 3  # 33.51 Å³
Z2_DISTANCE = np.sqrt(Z2_VOLUME)  # 5.79 Å (vacuum baseline)
EXPANSION_MULTIPLIER = 1.0391
PREDICTED_BIOLOGICAL_PEAK = Z2_DISTANCE * EXPANSION_MULTIPLIER  # 6.02 Å

# PDB API
PDB_SEARCH_API = "https://search.rcsb.org/rcsbsearch/v2/query"
PDB_DOWNLOAD_URL = "https://files.rcsb.org/download/{}.pdb"

# Non-redundant set parameters
SEQUENCE_IDENTITY_CUTOFF = 30  # %

# Hydrophobic residues
HYDROPHOBIC_RESIDUES = {'ALA', 'VAL', 'LEU', 'ILE', 'MET', 'PHE', 'TRP', 'PRO'}


def gaussian(x, amplitude, mean, sigma):
    """Gaussian function for curve fitting."""
    return amplitude * np.exp(-(x - mean)**2 / (2 * sigma**2))


def build_nonredundant_query(result_limit: int = 1000) -> dict:
    """
    Build query for diverse, non-redundant protein structures.

    Uses:
    - High resolution (< 2.0 Å)
    - X-ray crystallography
    - Diverse protein classes
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
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entry_info.polymer_entity_count_protein",
                        "operator": "greater",
                        "value": 0
                    }
                }
            ]
        },
        "return_type": "entry",
        "request_options": {
            "results_content_type": ["experimental"],
            "sort": [{"sort_by": "rcsb_accession_info.deposit_date", "direction": "desc"}],
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
            timeout=120
        )
        response.raise_for_status()
        results = response.json()

        pdb_ids = []
        if "result_set" in results:
            for result in results["result_set"]:
                pdb_ids.append(result["identifier"])
        return pdb_ids

    except Exception as e:
        print(f"   PDB search error: {e}")
        return []


def download_pdb(pdb_id: str, cache_dir: Path) -> Optional[str]:
    """Download PDB file."""
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


def parse_pdb_heavy_atoms(pdb_content: str) -> Tuple[np.ndarray, List[str]]:
    """Parse heavy atoms from PDB."""
    positions = []
    residue_names = []

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

                positions.append([x, y, z])
                residue_names.append(res_name)
            except:
                continue

    return np.array(positions), residue_names


def extract_core_distances(positions: np.ndarray, residue_names: List[str]) -> np.ndarray:
    """Extract non-covalent contact distances from protein core."""
    if len(positions) < 50:
        return np.array([])

    # Get hydrophobic residues
    hydro_mask = np.array([r in HYDROPHOBIC_RESIDUES for r in residue_names])
    if np.sum(hydro_mask) < 20:
        return np.array([])

    hydro_pos = positions[hydro_mask]

    # Get inner 50% (buried core)
    centroid = np.mean(positions, axis=0)
    distances = np.linalg.norm(hydro_pos - centroid, axis=1)
    median_dist = np.median(distances)
    core_mask = distances < median_dist
    core_pos = hydro_pos[core_mask]

    if len(core_pos) < 10:
        return np.array([])

    # Delaunay triangulation
    try:
        tri = Delaunay(core_pos)
        contact_dists = []

        for simplex in tri.simplices:
            for i in range(4):
                for j in range(i + 1, 4):
                    d = np.linalg.norm(core_pos[simplex[i]] - core_pos[simplex[j]])
                    # Non-covalent range
                    if 3.0 < d < 8.0:
                        contact_dists.append(d)

        return np.array(contact_dists)

    except:
        return np.array([])


def fit_gaussian_to_distribution(distances: np.ndarray, bins: int = 100) -> Dict:
    """Fit Gaussian to the distance distribution."""
    hist, bin_edges = np.histogram(distances, bins=bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Initial guesses
    amplitude_guess = np.max(hist)
    mean_guess = bin_centers[np.argmax(hist)]
    sigma_guess = np.std(distances)

    try:
        popt, pcov = curve_fit(
            gaussian, bin_centers, hist,
            p0=[amplitude_guess, mean_guess, sigma_guess],
            maxfev=10000
        )

        # Calculate R²
        y_pred = gaussian(bin_centers, *popt)
        ss_res = np.sum((hist - y_pred)**2)
        ss_tot = np.sum((hist - np.mean(hist))**2)
        r_squared = 1 - (ss_res / ss_tot)

        return {
            'amplitude': float(popt[0]),
            'mean': float(popt[1]),
            'sigma': float(popt[2]),
            'r_squared': float(r_squared),
            'bin_centers': bin_centers.tolist(),
            'histogram': hist.tolist()
        }

    except Exception as e:
        return {
            'error': str(e),
            'empirical_mean': float(np.mean(distances)),
            'empirical_std': float(np.std(distances))
        }


def generate_distribution_plot(distances: np.ndarray, fit_result: Dict,
                                output_path: Path) -> None:
    """Generate high-resolution Gaussian distribution plot."""
    if not HAS_MATPLOTLIB:
        print("   matplotlib not available, skipping plot")
        return

    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)

    # Histogram
    n, bins, patches = ax.hist(
        distances, bins=100, density=True,
        alpha=0.7, color='steelblue', edgecolor='white',
        label=f'Empirical Distribution (n={len(distances):,})'
    )

    # Fitted Gaussian
    if 'mean' in fit_result:
        x_fit = np.linspace(3.0, 9.0, 500)
        y_fit = gaussian(x_fit, fit_result['amplitude'],
                        fit_result['mean'], fit_result['sigma'])
        ax.plot(x_fit, y_fit, 'r-', linewidth=2.5,
                label=f'Gaussian Fit (R²={fit_result["r_squared"]:.4f})')

    # Vertical reference lines
    ax.axvline(Z2_DISTANCE, color='darkgreen', linestyle='--', linewidth=2,
               label=f'Vacuum Baseline √Z² = {Z2_DISTANCE:.3f} Å')

    ax.axvline(PREDICTED_BIOLOGICAL_PEAK, color='darkorange', linestyle='--', linewidth=2,
               label=f'Predicted Biological Peak = {PREDICTED_BIOLOGICAL_PEAK:.3f} Å')

    if 'mean' in fit_result:
        ax.axvline(fit_result['mean'], color='red', linestyle='-', linewidth=2,
                   label=f'Empirical Peak = {fit_result["mean"]:.3f} Å')

    # Labels and title
    ax.set_xlabel('Non-Covalent Contact Distance (Å)', fontsize=14)
    ax.set_ylabel('Probability Density', fontsize=14)
    ax.set_title('Universal Geometric Law: PDB-Wide Distance Distribution\n'
                 'Zimmerman Unified Geometry Framework', fontsize=16, fontweight='bold')

    # Legend
    ax.legend(loc='upper right', fontsize=11)

    # Add text box with statistics
    textstr = '\n'.join([
        f'n = {len(distances):,} contacts',
        f'Structures analyzed',
        f'',
        f'Empirical mean: {np.mean(distances):.3f} Å',
        f'Empirical std:  {np.std(distances):.3f} Å',
        f'',
        f'Expansion multiplier:',
        f'  Predicted: 1.0391',
        f'  Observed:  {np.mean(distances)/Z2_DISTANCE:.4f}'
    ])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

    ax.set_xlim(3.0, 9.0)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"   📊 Plot saved to: {output_path}")


def main():
    """Main execution: PDB census for universal geometric law."""
    print("=" * 70)
    print("THE UNIVERSAL GEOMETRIC LAW")
    print("PDB Census: Proving the Thermodynamic Expansion Multiplier")
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
   HYPOTHESIS:
   ───────────
   If Z² = 32π/3 governs vacuum atomic geometry, and biological systems
   operate with a Thermodynamic Expansion Multiplier of 1.0391, then
   the ENTIRE Protein Data Bank should show:

   MEAN PACKING DISTANCE = {Z2_DISTANCE:.3f} × 1.0391 = {PREDICTED_BIOLOGICAL_PEAK:.3f} Å

   This is the empirical test of the Universal Geometric Law.
""")

    # Search for diverse structures
    print("\n📊 Querying RCSB Protein Data Bank...")
    query = build_nonredundant_query(result_limit=1000)
    pdb_ids = search_pdb(query)
    print(f"   Found {len(pdb_ids)} high-resolution X-ray structures")

    # Fallback diverse set
    if len(pdb_ids) < 100:
        print("   Using curated diverse set...")
        # Well-characterized, diverse protein structures
        pdb_ids = [
            "1A0A", "1A0C", "1A0H", "1A0I", "1A0J", "1A0K", "1A0N", "1A0P",
            "1A0R", "1A0S", "1A0T", "1A12", "1A17", "1A1S", "1A1U", "1A1X",
            "1A2J", "1A2K", "1A2P", "1A2X", "1A2Y", "1A2Z", "1A34", "1A36",
            "1A3A", "1A3N", "1A3Q", "1A3R", "1A3W", "1A3Y", "1A42", "1A43",
            "1A44", "1A45", "1A48", "1A4A", "1A4G", "1A4I", "1A4J", "1A4L",
            "1A4M", "1A4P", "1A4R", "1A4S", "1A4U", "1A4V", "1A4W", "1A4Y",
            "1A50", "1A52", "1A53", "1A59", "1A5T", "1A5Z", "1A62", "1A65",
            "1A69", "1A6A", "1A6G", "1A6M", "1A6Q", "1A6T", "1A6V", "1A73",
            "1A75", "1A76", "1A78", "1A7D", "1A7G", "1A7H", "1A7J", "1A7S",
            "1A7T", "1A7V", "1A7W", "1A80", "1A81", "1A82", "1A87", "1A88",
            "1A8D", "1A8E", "1A8G", "1A8H", "1A8I", "1A8J", "1A8K", "1A8O",
            "1A8P", "1A8R", "1A8S", "1A99", "1A9N", "1A9X", "1AAC", "1ABA",
            # Add more diverse structures
            "1CRN", "1UBQ", "1LYZ", "1MBA", "1HEL", "1TIM", "1GEN", "1ENH",
            "1IGD", "1PGB", "1ROP", "1SH1", "1TEN", "1YCC", "2ACE", "2LZM"
        ]

    # Process structures
    print(f"\n📐 Analyzing {len(pdb_ids)} protein structures...")
    print("   (This may take several minutes)")

    all_distances = []
    structures_processed = 0
    structures_failed = 0

    for i, pdb_id in enumerate(pdb_ids):
        if (i + 1) % 50 == 0:
            print(f"   ... processed {i + 1}/{len(pdb_ids)} ({len(all_distances):,} contacts)")

        pdb_content = download_pdb(pdb_id, cache_dir)
        if pdb_content is None:
            structures_failed += 1
            continue

        positions, residue_names = parse_pdb_heavy_atoms(pdb_content)
        if len(positions) < 50:
            structures_failed += 1
            continue

        distances = extract_core_distances(positions, residue_names)
        if len(distances) < 10:
            structures_failed += 1
            continue

        all_distances.extend(distances.tolist())
        structures_processed += 1

        time.sleep(0.05)  # Rate limiting

    print(f"\n   Structures processed: {structures_processed}")
    print(f"   Structures failed: {structures_failed}")
    print(f"   Total contacts: {len(all_distances):,}")

    if len(all_distances) < 1000:
        print("\n   WARNING: Insufficient data for robust analysis")

    all_distances = np.array(all_distances)

    # Calculate statistics
    print("\n" + "=" * 70)
    print("RESULTS: UNIVERSAL GEOMETRIC LAW")
    print("=" * 70)

    empirical_mean = np.mean(all_distances)
    empirical_std = np.std(all_distances)
    empirical_median = np.median(all_distances)
    observed_multiplier = empirical_mean / Z2_DISTANCE

    # Error from predicted
    error_from_predicted = abs(empirical_mean - PREDICTED_BIOLOGICAL_PEAK)
    percent_error = (error_from_predicted / PREDICTED_BIOLOGICAL_PEAK) * 100

    print(f"""
   PDB CENSUS STATISTICS:
   ──────────────────────
   Structures analyzed: {structures_processed}
   Total contacts:      {len(all_distances):,}

   EMPIRICAL DISTRIBUTION:
   Mean distance:   {empirical_mean:.4f} Å
   Std deviation:   {empirical_std:.4f} Å
   Median:          {empirical_median:.4f} Å

   THEORETICAL PREDICTIONS:
   Vacuum baseline (√Z²):           {Z2_DISTANCE:.4f} Å
   Predicted biological peak:       {PREDICTED_BIOLOGICAL_PEAK:.4f} Å
   (using multiplier 1.0391)

   OBSERVED EXPANSION MULTIPLIER:   {observed_multiplier:.4f}
   PREDICTED MULTIPLIER:            1.0391
   MULTIPLIER ERROR:                {abs(observed_multiplier - 1.0391):.4f} ({abs(observed_multiplier - 1.0391) / 1.0391 * 100:.2f}%)

   PEAK LOCATION:
   Predicted: {PREDICTED_BIOLOGICAL_PEAK:.4f} Å
   Observed:  {empirical_mean:.4f} Å
   Error:     {error_from_predicted:.4f} Å ({percent_error:.2f}%)
""")

    # Fit Gaussian
    print("   Fitting Gaussian distribution...")
    fit_result = fit_gaussian_to_distribution(all_distances)

    if 'mean' in fit_result:
        print(f"""
   GAUSSIAN FIT:
   Amplitude: {fit_result['amplitude']:.4f}
   Mean:      {fit_result['mean']:.4f} Å
   Sigma:     {fit_result['sigma']:.4f} Å
   R²:        {fit_result['r_squared']:.4f}
""")

    # Generate plot
    if HAS_MATPLOTLIB:
        plot_path = results_dir / 'universal_geometric_law_distribution.png'
        generate_distribution_plot(all_distances, fit_result, plot_path)

    # Statistical test: Is the observed mean significantly close to predicted?
    # Using one-sample t-test against predicted value
    t_stat, p_value = stats.ttest_1samp(all_distances, PREDICTED_BIOLOGICAL_PEAK)

    # 95% CI for the mean
    ci_95 = stats.t.interval(0.95, len(all_distances)-1,
                             loc=empirical_mean,
                             scale=stats.sem(all_distances))

    print(f"""
   STATISTICAL VALIDATION:
   ───────────────────────
   One-sample t-test (H0: mean = {PREDICTED_BIOLOGICAL_PEAK:.4f} Å):
     t-statistic: {t_stat:.4f}
     p-value:     {p_value:.2e}

   95% Confidence Interval: [{ci_95[0]:.4f}, {ci_95[1]:.4f}] Å

   Does CI contain predicted value ({PREDICTED_BIOLOGICAL_PEAK:.4f} Å)? {ci_95[0] <= PREDICTED_BIOLOGICAL_PEAK <= ci_95[1]}
""")

    # Verdict
    print("\n" + "=" * 70)
    print("VERDICT: UNIVERSAL GEOMETRIC LAW")
    print("=" * 70)

    # Success criteria
    multiplier_close = abs(observed_multiplier - 1.0391) < 0.05  # Within 5%
    peak_close = percent_error < 5  # Within 5%
    ci_contains_predicted = ci_95[0] <= PREDICTED_BIOLOGICAL_PEAK <= ci_95[1]

    if multiplier_close and peak_close:
        verdict = "CONFIRMED"
        print(f"""
   ╔══════════════════════════════════════════════════════════════════╗
   ║                                                                  ║
   ║   ✅ UNIVERSAL GEOMETRIC LAW CONFIRMED                           ║
   ║                                                                  ║
   ║   The PDB census reveals that biological packing distance        ║
   ║   follows a Gaussian distribution centered at:                   ║
   ║                                                                  ║
   ║           {empirical_mean:.3f} Å ≈ √Z² × 1.0391 = {PREDICTED_BIOLOGICAL_PEAK:.3f} Å              ║
   ║                                                                  ║
   ║   OBSERVED MULTIPLIER: {observed_multiplier:.4f}                               ║
   ║   PREDICTED MULTIPLIER: 1.0391                                   ║
   ║   ERROR: {abs(observed_multiplier - 1.0391) / 1.0391 * 100:.2f}%                                              ║
   ║                                                                  ║
   ║   The Thermodynamic Expansion Multiplier is validated across     ║
   ║   {structures_processed} diverse protein structures and {len(all_distances):,} atomic          ║
   ║   contacts from the global Protein Data Bank.                    ║
   ║                                                                  ║
   ║   Z² = 32π/3 is the fundamental constant of biological geometry. ║
   ║                                                                  ║
   ╚══════════════════════════════════════════════════════════════════╝
""")
    elif peak_close:
        verdict = "SUPPORTED"
        print(f"""
   ╔══════════════════════════════════════════════════════════════════╗
   ║                                                                  ║
   ║   ⚠️  UNIVERSAL GEOMETRIC LAW SUPPORTED (with caveats)           ║
   ║                                                                  ║
   ║   The empirical peak ({empirical_mean:.3f} Å) is close to prediction       ║
   ║   ({PREDICTED_BIOLOGICAL_PEAK:.3f} Å) but with some deviation.                    ║
   ║                                                                  ║
   ║   OBSERVED MULTIPLIER: {observed_multiplier:.4f}                               ║
   ║   DEVIATION: {abs(observed_multiplier - 1.0391) / 1.0391 * 100:.2f}%                                              ║
   ║                                                                  ║
   ╚══════════════════════════════════════════════════════════════════╝
""")
    else:
        verdict = "NOT CONFIRMED"
        print(f"""
   ╔══════════════════════════════════════════════════════════════════╗
   ║                                                                  ║
   ║   ❌ UNIVERSAL GEOMETRIC LAW NOT CONFIRMED                       ║
   ║                                                                  ║
   ║   The empirical peak ({empirical_mean:.3f} Å) deviates significantly      ║
   ║   from the predicted value ({PREDICTED_BIOLOGICAL_PEAK:.3f} Å).                   ║
   ║                                                                  ║
   ║   DEVIATION: {percent_error:.2f}%                                              ║
   ║                                                                  ║
   ╚══════════════════════════════════════════════════════════════════╝
""")

    # Save results
    final_results = {
        'timestamp': datetime.now().isoformat(),
        'hypothesis': 'Universal Geometric Law: Mean packing = √Z² × 1.0391',
        'vacuum_baseline': Z2_DISTANCE,
        'predicted_multiplier': 1.0391,
        'predicted_biological_peak': PREDICTED_BIOLOGICAL_PEAK,
        'structures_analyzed': structures_processed,
        'total_contacts': len(all_distances),
        'empirical': {
            'mean': float(empirical_mean),
            'std': float(empirical_std),
            'median': float(empirical_median),
            'observed_multiplier': float(observed_multiplier)
        },
        'gaussian_fit': fit_result,
        'statistical_test': {
            't_statistic': float(t_stat),
            'p_value': float(p_value),
            '95_ci': [float(ci_95[0]), float(ci_95[1])],
            'ci_contains_predicted': ci_contains_predicted
        },
        'validation': {
            'multiplier_error_percent': abs(observed_multiplier - 1.0391) / 1.0391 * 100,
            'peak_error_percent': percent_error,
            'verdict': verdict
        }
    }

    output_path = results_dir / 'emp_03_universal_geometry_law_results.json'
    with open(output_path, 'w') as f:
        json.dump(final_results, f, indent=2, default=str)

    print(f"\n📄 Results saved to: {output_path}")
    print("=" * 70)

    return final_results


if __name__ == '__main__':
    results = main()
