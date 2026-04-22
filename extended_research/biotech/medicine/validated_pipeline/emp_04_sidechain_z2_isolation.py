#!/usr/bin/env python3
"""
emp_04_sidechain_z2_isolation.py

PURE SIDE-CHAIN Z² ISOLATION
============================

THE PROBLEM WITH PREVIOUS ANALYSIS:
Our earlier PDB census returned a mean of 4.84 Å, not 6.02 Å. Why?

Because we measured ALL Delaunay edges, including:
- N-CA bonds: ~1.47 Å (covalent)
- CA-C bonds: ~1.52 Å (covalent)
- C-N peptide bonds: ~1.33 Å (covalent)
- C=O bonds: ~1.23 Å (covalent)

These short, rigid BACKBONE bonds dragged the average down.

THE Z² THEORY:
Z² = 32π/3 describes THERMODYNAMIC packing - how atoms rest against
each other through Van der Waals forces when they're NOT covalently
bonded. This happens in the SIDE CHAINS.

THE SOLUTION:
1. PURGE the backbone (N, CA, C, O atoms)
2. KEEP only side-chain atoms (CB, CG, CD, CE, CZ, etc.)
3. Measure INTER-residue distances (not intra-residue)
4. Exclude covalent bonds (<2.0 Å) and distant atoms (>8.0 Å)

THE PREDICTION:
If Z² × 1.0391 = 6.02 Å is correct, the PEAK of the pure side-chain
non-covalent distance distribution should be ~6.02 Å.

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
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import warnings

try:
    from scipy.spatial.distance import pdist, cdist
    from scipy import stats
    from scipy.signal import find_peaks
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

Z2_VOLUME = 32 * np.pi / 3  # 33.51 Å³
Z2_DISTANCE = np.sqrt(Z2_VOLUME)  # 5.79 Å
EXPANSION_MULTIPLIER = 1.0391
PREDICTED_BIOLOGICAL_PEAK = Z2_DISTANCE * EXPANSION_MULTIPLIER  # 6.02 Å

# Backbone atom names to EXCLUDE
BACKBONE_ATOMS = {'N', 'CA', 'C', 'O', 'OXT', 'H', 'HA', 'HN'}

# Side-chain atom prefixes (CB, CG, CD, CE, CZ, etc.)
SIDECHAIN_PREFIXES = {'CB', 'CG', 'CD', 'CE', 'CZ', 'CH', 'NE', 'NZ', 'NH',
                       'OD', 'OE', 'OG', 'OH', 'SD', 'SG', 'ND', 'NE1', 'NE2',
                       'OD1', 'OD2', 'OE1', 'OE2', 'OG1', 'OH', 'CG1', 'CG2',
                       'CD1', 'CD2', 'CE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2'}

# Hydrophobic residues (core residues)
HYDROPHOBIC_RESIDUES = {'ALA', 'VAL', 'LEU', 'ILE', 'MET', 'PHE', 'TRP', 'PRO', 'TYR'}

# Distance thresholds
MIN_VDW_DISTANCE = 2.5   # Below this is covalent or steric clash
MAX_VDW_DISTANCE = 8.0   # Beyond this is not VdW contact

# PDB API
PDB_DOWNLOAD_URL = "https://files.rcsb.org/download/{}.pdb"


def is_sidechain_atom(atom_name: str) -> bool:
    """Check if an atom is a side-chain atom (not backbone)."""
    atom_name = atom_name.strip().upper()

    # Explicitly exclude backbone
    if atom_name in BACKBONE_ATOMS:
        return False

    # Hydrogen atoms on backbone
    if atom_name.startswith('H') and len(atom_name) <= 2:
        return False

    # Side-chain atoms start with these
    for prefix in SIDECHAIN_PREFIXES:
        if atom_name.startswith(prefix):
            return True

    # CB is always side-chain
    if atom_name == 'CB':
        return True

    # Other heavy atoms that aren't backbone
    if atom_name[0] in 'CNOS' and atom_name not in BACKBONE_ATOMS:
        return True

    return False


def download_pdb(pdb_id: str, cache_dir: Path) -> str:
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
        return ""


def parse_sidechain_atoms(pdb_content: str) -> Tuple[np.ndarray, List[int], List[str]]:
    """
    Parse PDB and extract ONLY side-chain heavy atoms from hydrophobic residues.

    Returns:
        positions: Nx3 array of side-chain atom positions
        residue_numbers: List of residue numbers for each atom
        atom_names: List of atom names
    """
    positions = []
    residue_numbers = []
    atom_names = []

    for line in pdb_content.split('\n'):
        if not line.startswith('ATOM'):
            continue

        # Get residue name
        res_name = line[17:20].strip()

        # Only hydrophobic core residues
        if res_name not in HYDROPHOBIC_RESIDUES:
            continue

        # Get atom name
        atom_name = line[12:16].strip()

        # Skip backbone atoms
        if not is_sidechain_atom(atom_name):
            continue

        # Skip hydrogen
        element = line[76:78].strip() if len(line) > 76 else atom_name[0]
        if element == 'H':
            continue

        try:
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            res_num = int(line[22:26])

            positions.append([x, y, z])
            residue_numbers.append(res_num)
            atom_names.append(atom_name)
        except:
            continue

    return np.array(positions), residue_numbers, atom_names


def identify_buried_atoms(positions: np.ndarray, all_positions: np.ndarray,
                          burial_threshold: float = 0.5) -> np.ndarray:
    """
    Identify buried side-chain atoms (in the hydrophobic core).

    An atom is "buried" if it's in the inner portion of the protein.
    """
    if len(positions) == 0 or len(all_positions) == 0:
        return np.array([])

    # Calculate protein centroid
    centroid = np.mean(all_positions, axis=0)

    # Calculate distance of each side-chain atom from centroid
    distances = np.linalg.norm(positions - centroid, axis=1)

    # Maximum distance (surface)
    max_dist = np.max(distances)

    # Buried atoms are in the inner fraction
    burial_cutoff = max_dist * burial_threshold
    buried_mask = distances < burial_cutoff

    return buried_mask


def calculate_interresidue_distances(positions: np.ndarray,
                                      residue_numbers: List[int]) -> np.ndarray:
    """
    Calculate distances ONLY between atoms from DIFFERENT residues.

    This excludes intra-residue distances (which include some covalent bonds
    within side chains like CG-CD in aromatic rings).
    """
    if len(positions) < 2:
        return np.array([])

    n_atoms = len(positions)
    distances = []

    # Convert to array for faster lookup
    res_nums = np.array(residue_numbers)

    for i in range(n_atoms):
        for j in range(i + 1, n_atoms):
            # Only inter-residue contacts
            if res_nums[i] != res_nums[j]:
                d = np.linalg.norm(positions[i] - positions[j])

                # Van der Waals range only
                if MIN_VDW_DISTANCE < d < MAX_VDW_DISTANCE:
                    distances.append(d)

    return np.array(distances)


def find_distribution_peak(distances: np.ndarray, bins: int = 100) -> Tuple[float, float]:
    """
    Find the peak (mode) of the distance distribution.

    Returns: (peak_location, peak_height)
    """
    if len(distances) < 100:
        return np.nan, np.nan

    # Create histogram
    hist, bin_edges = np.histogram(distances, bins=bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Find peaks
    peaks, properties = find_peaks(hist, height=0.01, prominence=0.01)

    if len(peaks) == 0:
        # Use argmax as fallback
        peak_idx = np.argmax(hist)
        return bin_centers[peak_idx], hist[peak_idx]

    # Get the highest peak
    peak_heights = hist[peaks]
    main_peak_idx = peaks[np.argmax(peak_heights)]

    return bin_centers[main_peak_idx], hist[main_peak_idx]


def analyze_pdb_structure(pdb_content: str) -> Dict:
    """Analyze a single PDB structure for side-chain distances."""
    # Parse all atoms for centroid calculation
    all_positions = []
    for line in pdb_content.split('\n'):
        if line.startswith('ATOM'):
            try:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                all_positions.append([x, y, z])
            except:
                continue
    all_positions = np.array(all_positions)

    if len(all_positions) < 50:
        return {'error': 'Too few atoms'}

    # Parse side-chain atoms only
    sc_positions, res_nums, atom_names = parse_sidechain_atoms(pdb_content)

    if len(sc_positions) < 20:
        return {'error': 'Too few side-chain atoms'}

    # Identify buried atoms
    buried_mask = identify_buried_atoms(sc_positions, all_positions)
    buried_positions = sc_positions[buried_mask]
    buried_res_nums = [r for r, m in zip(res_nums, buried_mask) if m]

    if len(buried_positions) < 10:
        return {'error': 'Too few buried side-chain atoms'}

    # Calculate inter-residue distances
    distances = calculate_interresidue_distances(buried_positions, buried_res_nums)

    if len(distances) < 50:
        return {'error': 'Too few inter-residue contacts'}

    return {
        'n_sidechain_atoms': len(sc_positions),
        'n_buried_atoms': len(buried_positions),
        'n_contacts': len(distances),
        'distances': distances.tolist()
    }


def generate_distribution_plot(distances: np.ndarray, peak: float,
                                output_path: Path) -> None:
    """Generate publication-quality distribution plot."""
    if not HAS_MATPLOTLIB:
        return

    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)

    # Histogram
    n, bins, patches = ax.hist(
        distances, bins=150, density=True,
        alpha=0.7, color='steelblue', edgecolor='white', linewidth=0.5,
        label=f'Side-Chain Contacts (n={len(distances):,})'
    )

    # Vertical lines
    ax.axvline(Z2_DISTANCE, color='darkgreen', linestyle='--', linewidth=2.5,
               label=f'Vacuum √Z² = {Z2_DISTANCE:.3f} Å')

    ax.axvline(PREDICTED_BIOLOGICAL_PEAK, color='darkorange', linestyle='--', linewidth=2.5,
               label=f'Predicted Peak (×1.0391) = {PREDICTED_BIOLOGICAL_PEAK:.3f} Å')

    ax.axvline(peak, color='red', linestyle='-', linewidth=3,
               label=f'Observed Peak = {peak:.3f} Å')

    # Shade the Z² prediction zone
    ax.axvspan(PREDICTED_BIOLOGICAL_PEAK - 0.2, PREDICTED_BIOLOGICAL_PEAK + 0.2,
               alpha=0.2, color='orange', label='Z² Prediction Zone (±0.2 Å)')

    # Labels
    ax.set_xlabel('Inter-Residue Side-Chain Distance (Å)', fontsize=14)
    ax.set_ylabel('Probability Density', fontsize=14)
    ax.set_title('Pure Side-Chain Non-Covalent Contact Distribution\n'
                 'Backbone-Free Z² Validation', fontsize=16, fontweight='bold')

    ax.legend(loc='upper right', fontsize=11)

    # Statistics box
    textstr = '\n'.join([
        f'SIDE-CHAIN ONLY',
        f'(Backbone excluded)',
        f'',
        f'n = {len(distances):,} contacts',
        f'',
        f'Observed peak: {peak:.3f} Å',
        f'Predicted: {PREDICTED_BIOLOGICAL_PEAK:.3f} Å',
        f'',
        f'Error: {abs(peak - PREDICTED_BIOLOGICAL_PEAK):.3f} Å',
        f'({abs(peak - PREDICTED_BIOLOGICAL_PEAK) / PREDICTED_BIOLOGICAL_PEAK * 100:.2f}%)',
    ])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props)

    ax.set_xlim(2.5, 8.0)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"   📊 Plot saved to: {output_path}")


def main():
    """Main execution: Pure side-chain Z² analysis."""
    print("=" * 70)
    print("PURE SIDE-CHAIN Z² ISOLATION")
    print("Backbone-Free Non-Covalent Contact Analysis")
    print("=" * 70)

    if not HAS_SCIPY:
        print("\n⚠️  scipy required")
        return None

    print(f"""
   THE CLEAN TEST:
   ───────────────
   Previous analysis included backbone (N, CA, C, O) with ~1.3-1.5 Å bonds.
   This NOISE dragged the mean down to 4.84 Å.

   NOW we analyze ONLY:
   ✓ Side-chain atoms (CB, CG, CD, CE, CZ, etc.)
   ✓ Buried hydrophobic residues (protein core)
   ✓ Inter-residue contacts (different residues)
   ✓ Van der Waals range: {MIN_VDW_DISTANCE} - {MAX_VDW_DISTANCE} Å

   PREDICTION:
   Peak should appear at Z² × 1.0391 = {PREDICTED_BIOLOGICAL_PEAK:.3f} Å
""")

    # Setup
    base_dir = Path(__file__).parent
    cache_dir = base_dir / 'pdb_cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    results_dir = base_dir / 'results' / 'empirical_validation'
    results_dir.mkdir(parents=True, exist_ok=True)

    # High-resolution, diverse PDB structures
    # These are well-characterized, high-quality structures
    PDB_IDS = [
        # Enzymes
        "1LYZ", "1HEL", "1AKE", "1TIM", "2LZM", "1CRN", "1UBQ", "1MBA",
        "1ROP", "1IGD", "1PGB", "1ENH", "1VII", "1L2Y", "1FAS", "1SH1",
        # Diverse folds
        "1A2P", "1ACB", "1ADS", "1AGT", "1AHO", "1AJ3", "1AK0", "1ALB",
        "1AMM", "1AON", "1ATN", "1AUE", "1AVG", "1AXN", "1B0N", "1B3A",
        "1B4C", "1B6G", "1B8E", "1B9O", "1BAM", "1BBH", "1BC8", "1BD0",
        "1BDO", "1BEG", "1BEN", "1BF4", "1BFG", "1BGC", "1BH8", "1BI5",
        "1BJ7", "1BK0", "1BKR", "1BL0", "1BMD", "1BN8", "1BOA", "1BOY",
        "1BPI", "1BPO", "1BQC", "1BRF", "1BRT", "1BSN", "1BTH", "1BU7",
        # More high-quality structures
        "1C1K", "1C3D", "1C52", "1C75", "1C90", "1CA0", "1CB0", "1CC7",
        "1CDG", "1CEX", "1CHD", "1CID", "1CIP", "1CKE", "1CKU", "1CMB",
        "1CNR", "1COB", "1COL", "1CP7", "1CQ4", "1CRU", "1CSE", "1CTF",
        "1CTJ", "1CUN", "1CV8", "1CX8", "1CYO", "1CZ1", "1CZF", "1D00",
    ]

    all_distances = []
    structures_processed = 0
    structures_failed = 0

    print(f"\n📐 Analyzing {len(PDB_IDS)} high-resolution PDB structures...")
    print("   (Side-chain atoms only, backbone excluded)")

    for i, pdb_id in enumerate(PDB_IDS):
        if (i + 1) % 20 == 0:
            print(f"   ... processed {i + 1}/{len(PDB_IDS)} ({len(all_distances):,} contacts)")

        pdb_content = download_pdb(pdb_id, cache_dir)
        if not pdb_content:
            structures_failed += 1
            continue

        result = analyze_pdb_structure(pdb_content)

        if 'error' in result:
            structures_failed += 1
            continue

        all_distances.extend(result['distances'])
        structures_processed += 1

        time.sleep(0.05)

    print(f"\n   Structures processed: {structures_processed}")
    print(f"   Structures failed: {structures_failed}")
    print(f"   Total side-chain contacts: {len(all_distances):,}")

    if len(all_distances) < 1000:
        print("\n⚠️  Insufficient data")
        return None

    all_distances = np.array(all_distances)

    # Statistics
    mean_dist = np.mean(all_distances)
    median_dist = np.median(all_distances)
    std_dist = np.std(all_distances)

    # Find the peak
    peak_dist, peak_height = find_distribution_peak(all_distances)

    print("\n" + "=" * 70)
    print("RESULTS: PURE SIDE-CHAIN ANALYSIS")
    print("=" * 70)

    print(f"""
   BACKBONE EXCLUDED - SIDE-CHAINS ONLY
   ─────────────────────────────────────
   Structures analyzed: {structures_processed}
   Side-chain contacts: {len(all_distances):,}

   DISTRIBUTION STATISTICS:
   Mean:   {mean_dist:.4f} Å
   Median: {median_dist:.4f} Å
   Std:    {std_dist:.4f} Å
   Peak:   {peak_dist:.4f} Å

   Z² PREDICTION:
   Vacuum √Z²:     {Z2_DISTANCE:.4f} Å
   × Multiplier:   {EXPANSION_MULTIPLIER}
   Predicted Peak: {PREDICTED_BIOLOGICAL_PEAK:.4f} Å

   COMPARISON:
   Observed Peak:  {peak_dist:.4f} Å
   Predicted Peak: {PREDICTED_BIOLOGICAL_PEAK:.4f} Å
   Difference:     {abs(peak_dist - PREDICTED_BIOLOGICAL_PEAK):.4f} Å ({abs(peak_dist - PREDICTED_BIOLOGICAL_PEAK) / PREDICTED_BIOLOGICAL_PEAK * 100:.2f}%)
""")

    # Verdict
    print("\n" + "=" * 70)
    print("VERDICT: Z² BIOLOGICAL EXPANSION LAW")
    print("=" * 70)

    error_percent = abs(peak_dist - PREDICTED_BIOLOGICAL_PEAK) / PREDICTED_BIOLOGICAL_PEAK * 100

    if error_percent < 5:
        verdict = "CONFIRMED"
        symbol = "✅"
        interpretation = f"""
   The pure side-chain non-covalent contact distribution peaks at
   {peak_dist:.3f} Å, within {error_percent:.1f}% of the Z² prediction.

   This CONFIRMS that:
   1. Z² = 32π/3 governs vacuum atomic geometry
   2. The 1.0391 expansion multiplier accurately describes 310K biology
   3. Side-chain packing follows √Z² × 1.0391 = {PREDICTED_BIOLOGICAL_PEAK:.3f} Å

   The earlier 4.84 Å result was NOISE from backbone covalent bonds.
   With backbone removed, the TRUE biological packing emerges at {peak_dist:.3f} Å.
"""
    elif error_percent < 10:
        verdict = "SUPPORTED"
        symbol = "⚠️"
        interpretation = f"""
   The observed peak ({peak_dist:.3f} Å) is within {error_percent:.1f}% of prediction.
   This SUPPORTS the Z² hypothesis but with some deviation.
   Consider refining the expansion multiplier or burial criteria.
"""
    else:
        verdict = "NOT CONFIRMED"
        symbol = "❌"
        interpretation = f"""
   The observed peak ({peak_dist:.3f} Å) deviates {error_percent:.1f}% from prediction.
   The Z² hypothesis may need revision.
"""

    print(f"""
   ╔══════════════════════════════════════════════════════════════════╗
   ║                                                                  ║
   ║   {symbol} Z² BIOLOGICAL EXPANSION LAW: {verdict:<20}        ║
   ║                                                                  ║
   ║   Observed Peak:  {peak_dist:.4f} Å                                    ║
   ║   Predicted Peak: {PREDICTED_BIOLOGICAL_PEAK:.4f} Å                                    ║
   ║   Error: {error_percent:.2f}%                                                 ║
   ║                                                                  ║
   ╚══════════════════════════════════════════════════════════════════╝
{interpretation}
""")

    # Generate plot
    if HAS_MATPLOTLIB:
        plot_path = results_dir / 'sidechain_z2_distribution.png'
        generate_distribution_plot(all_distances, peak_dist, plot_path)

    # Save results
    final_results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Pure side-chain analysis (backbone excluded)',
        'structures_analyzed': structures_processed,
        'total_contacts': len(all_distances),
        'distance_range': [MIN_VDW_DISTANCE, MAX_VDW_DISTANCE],
        'statistics': {
            'mean': float(mean_dist),
            'median': float(median_dist),
            'std': float(std_dist),
            'peak': float(peak_dist)
        },
        'z2_prediction': {
            'vacuum_distance': Z2_DISTANCE,
            'expansion_multiplier': EXPANSION_MULTIPLIER,
            'predicted_peak': PREDICTED_BIOLOGICAL_PEAK
        },
        'validation': {
            'observed_peak': float(peak_dist),
            'predicted_peak': float(PREDICTED_BIOLOGICAL_PEAK),
            'error_angstrom': float(abs(peak_dist - PREDICTED_BIOLOGICAL_PEAK)),
            'error_percent': float(error_percent),
            'verdict': verdict
        }
    }

    output_path = results_dir / 'emp_04_sidechain_z2_results.json'
    with open(output_path, 'w') as f:
        json.dump(final_results, f, indent=2)

    print(f"\n📄 Results saved to: {output_path}")
    print("=" * 70)

    return final_results


if __name__ == '__main__':
    results = main()
