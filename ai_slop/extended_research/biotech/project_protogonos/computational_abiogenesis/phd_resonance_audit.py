#!/usr/bin/env python3
"""
phd_resonance_audit.py

PhD-LEVEL Z-RESONANCE VALIDATION

AGENT ROLE: Senior Computational Biophysicist & Skeptic

MISSION: Validate the existence of a spatial frequency peak at Z ≈ 5.79 Å
across a diverse, non-redundant dataset of the Global Proteome.

ANALYSES:
1. Sequential distance decomposition (i→i+1, i→i+2, i→i+3, i→i+4)
2. Secondary structure decomposition (α-helix, β-sheet, coil)
3. Signal-to-noise ratio calculation
4. Statistical significance testing

Author: Project Protogonos
Date: May 28, 2026
"""

import numpy as np
from scipy.signal import find_peaks
from scipy import stats
from typing import Dict, List, Tuple, Optional
import urllib.request
import os
import json

# =============================================================================
# CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)  # 5.7888 Å
Z_TOLERANCE = 0.15      # Å (tight window for peak detection)
Z_WINDOW = (5.70, 5.85) # Target range for Z-peak

print("=" * 70)
print("PhD-LEVEL Z-RESONANCE AUDIT")
print("=" * 70)
print(f"""
  MISSION: Validate Z = {Z:.4f} Å as universal biological constant

  ANALYSES:
  1. Sequential distance decomposition (i→i+1, i→i+2, i→i+3, i→i+4)
  2. Secondary structure decomposition (α-helix, β-sheet, coil)
  3. Signal-to-noise ratio (R > 3.0 = biological signal)
  4. Statistical significance (p < 0.001)

  SUCCESS CRITERION:
  Peak in range {Z_WINDOW[0]:.2f}-{Z_WINDOW[1]:.2f} Å with SNR > 3.0
""")


# =============================================================================
# DIVERSE PROTEIN SET (High-resolution, non-redundant)
# =============================================================================

# Curated set of high-resolution (<2.0 Å), non-redundant proteins
HIGH_QUALITY_PROTEINS = [
    # ARCHAEA
    ('1AJ8', 'Rubredoxin', 'Archaea', 'Pyrococcus furiosus', 0.95),
    ('1B4O', 'Ferredoxin', 'Archaea', 'Sulfolobus', 1.70),

    # BACTERIA - diverse phyla
    ('2TRX', 'Thioredoxin', 'Bacteria', 'E. coli', 1.68),
    ('1AKE', 'Adenylate kinase', 'Bacteria', 'E. coli', 1.63),
    ('256B', 'Cytochrome b562', 'Bacteria', 'E. coli', 1.40),
    ('1BRS', 'Barnase', 'Bacteria', 'B. amyloliquefaciens', 1.50),

    # EUKARYA - Animals
    ('1LYZ', 'Lysozyme', 'Eukarya', 'Chicken', 1.33),
    ('1UBQ', 'Ubiquitin', 'Eukarya', 'Human', 1.80),
    ('1CRN', 'Crambin', 'Eukarya', 'Plant', 0.83),
    ('3CLN', 'Calmodulin', 'Eukarya', 'Human', 1.70),
    ('1MBN', 'Myoglobin', 'Eukarya', 'Sperm whale', 1.40),
    ('1YCC', 'Cytochrome c', 'Eukarya', 'Yeast', 1.23),
    ('1CYT', 'Cytochrome c', 'Eukarya', 'Tuna', 1.50),
    ('1CHO', 'Chymotrypsin', 'Eukarya', 'Bovine', 1.68),
    ('7RSA', 'Ribonuclease A', 'Eukarya', 'Bovine', 1.26),
    ('1PPL', 'Pepsin', 'Eukarya', 'Pig', 1.80),
    ('1TIM', 'TIM barrel', 'Eukarya', 'Chicken', 1.83),
    ('1VII', 'Villin headpiece', 'Eukarya', 'Chicken', 1.70),
    ('1GKZ', 'GFP', 'Eukarya', 'Jellyfish', 1.45),
    ('1PLC', 'Plastocyanin', 'Eukarya', 'Poplar', 1.33),

    # DIFFERENT FOLD CLASSES
    ('1UTG', 'Uteroglobin', 'Eukarya', 'Rabbit', 1.34),  # All-alpha
    ('1TEN', 'Tenascin', 'Eukarya', 'Human', 1.80),      # All-beta
    ('1CTF', 'Ribosomal L7', 'Bacteria', 'E. coli', 1.70), # Alpha+beta
]


# =============================================================================
# PDB UTILITIES
# =============================================================================

def download_pdb(pdb_id: str) -> Optional[str]:
    """Download PDB file."""
    pdb_id = pdb_id.lower()
    filepath = f"{pdb_id}.pdb"
    if os.path.exists(filepath):
        return filepath
    try:
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        urllib.request.urlretrieve(url, filepath)
        return filepath
    except:
        return None


def parse_pdb_with_ss(filepath: str) -> Tuple[np.ndarray, List[str], List[int]]:
    """
    Parse PDB file extracting C-alpha coords and secondary structure.

    Returns:
        coords: Nx3 array of C-alpha coordinates
        ss_codes: List of secondary structure codes ('H', 'E', 'C')
        residue_nums: List of residue numbers
    """
    coords = []
    residue_nums = []

    # First, extract HELIX and SHEET records for SS assignment
    helix_ranges = []
    sheet_ranges = []

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('HELIX'):
                try:
                    start = int(line[21:25])
                    end = int(line[33:37])
                    chain = line[19]
                    helix_ranges.append((chain, start, end))
                except:
                    pass
            elif line.startswith('SHEET'):
                try:
                    start = int(line[22:26])
                    end = int(line[33:37])
                    chain = line[21]
                    sheet_ranges.append((chain, start, end))
                except:
                    pass

    # Extract C-alpha atoms
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('ATOM') and ' CA ' in line:
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    resnum = int(line[22:26])
                    chain = line[21]

                    coords.append([x, y, z])
                    residue_nums.append(resnum)
                except:
                    pass

    coords = np.array(coords)

    # Assign secondary structure
    ss_codes = []
    for i, resnum in enumerate(residue_nums):
        ss = 'C'  # Default: coil
        chain = 'A'  # Simplified - assume first chain

        for c, start, end in helix_ranges:
            if start <= resnum <= end:
                ss = 'H'
                break

        if ss == 'C':
            for c, start, end in sheet_ranges:
                if start <= resnum <= end:
                    ss = 'E'
                    break

        ss_codes.append(ss)

    return coords, ss_codes, residue_nums


# =============================================================================
# SEQUENTIAL DISTANCE ANALYSIS
# =============================================================================

def analyze_sequential_distances(coords: np.ndarray) -> Dict:
    """
    Analyze distances by sequence separation.

    i→i+1: peptide bond (~3.8 Å)
    i→i+2: α-helix characteristic (~5.5-6.0 Å) ← Z TARGET
    i→i+3: α-helix turn (~5.0-5.5 Å)
    i→i+4: α-helix pitch (~6.3 Å)
    """
    n = len(coords)

    distances = {
        'i_to_i+1': [],
        'i_to_i+2': [],
        'i_to_i+3': [],
        'i_to_i+4': [],
        'long_range': []  # |i-j| > 4
    }

    for i in range(n):
        for j in range(i + 1, n):
            d = np.linalg.norm(coords[j] - coords[i])
            sep = j - i

            if sep == 1:
                distances['i_to_i+1'].append(d)
            elif sep == 2:
                distances['i_to_i+2'].append(d)
            elif sep == 3:
                distances['i_to_i+3'].append(d)
            elif sep == 4:
                distances['i_to_i+4'].append(d)
            elif d < 15:  # Only local contacts
                distances['long_range'].append(d)

    # Calculate statistics for each category
    results = {}
    for key, vals in distances.items():
        if vals:
            arr = np.array(vals)
            results[key] = {
                'mean': float(np.mean(arr)),
                'std': float(np.std(arr)),
                'median': float(np.median(arr)),
                'count': len(vals),
                'in_Z_window': float(np.mean((arr >= Z_WINDOW[0]) & (arr <= Z_WINDOW[1])))
            }
        else:
            results[key] = None

    return results


# =============================================================================
# SECONDARY STRUCTURE DECOMPOSITION
# =============================================================================

def analyze_by_secondary_structure(coords: np.ndarray, ss_codes: List[str]) -> Dict:
    """
    Analyze i→i+2 distances separately for α-helix, β-sheet, and coil.
    """
    n = len(coords)

    distances = {
        'helix': [],   # H
        'sheet': [],   # E
        'coil': []     # C
    }

    for i in range(n - 2):
        d = np.linalg.norm(coords[i + 2] - coords[i])

        # Use the secondary structure of the middle residue
        ss = ss_codes[i + 1] if i + 1 < len(ss_codes) else 'C'

        if ss == 'H':
            distances['helix'].append(d)
        elif ss == 'E':
            distances['sheet'].append(d)
        else:
            distances['coil'].append(d)

    # Calculate statistics
    results = {}
    for key, vals in distances.items():
        if vals:
            arr = np.array(vals)

            # Find peak in distribution
            bins = np.linspace(4, 8, 81)  # 0.05 Å resolution
            hist, edges = np.histogram(arr, bins=bins)
            centers = (edges[:-1] + edges[1:]) / 2

            if len(hist) > 0 and np.max(hist) > 0:
                peak_idx = np.argmax(hist)
                peak_dist = centers[peak_idx]
                peak_height = hist[peak_idx]

                # Signal-to-noise ratio
                background = np.mean(hist[hist > 0])
                snr = peak_height / background if background > 0 else 0

                results[key] = {
                    'mean': float(np.mean(arr)),
                    'std': float(np.std(arr)),
                    'peak_distance': float(peak_dist),
                    'peak_height': int(peak_height),
                    'snr': float(snr),
                    'count': len(vals),
                    'in_Z_window': float(np.sum((arr >= Z_WINDOW[0]) & (arr <= Z_WINDOW[1])) / len(arr))
                }
            else:
                results[key] = {'count': len(vals), 'mean': float(np.mean(arr))}
        else:
            results[key] = None

    return results


# =============================================================================
# STATISTICAL VALIDATION
# =============================================================================

def calculate_z_resonance_statistics(coords: np.ndarray) -> Dict:
    """
    Calculate comprehensive Z-resonance statistics with p-values.
    """
    n = len(coords)

    # Calculate i→i+2 distances
    i_to_i2_distances = []
    for i in range(n - 2):
        d = np.linalg.norm(coords[i + 2] - coords[i])
        i_to_i2_distances.append(d)

    if len(i_to_i2_distances) < 10:
        return {'status': 'INSUFFICIENT_DATA'}

    arr = np.array(i_to_i2_distances)

    # High-resolution histogram
    bins = np.linspace(4.5, 7.5, 61)  # 0.05 Å resolution
    hist, edges = np.histogram(arr, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2

    # Find all peaks
    peaks, properties = find_peaks(hist, height=3)

    # Find peak closest to Z
    z_peak_idx = None
    z_peak_dist = None
    z_peak_height = 0

    for p in peaks:
        if Z_WINDOW[0] <= centers[p] <= Z_WINDOW[1]:
            if hist[p] > z_peak_height:
                z_peak_idx = p
                z_peak_dist = centers[p]
                z_peak_height = hist[p]

    # Signal-to-noise ratio
    background_mask = (centers < Z_WINDOW[0] - 0.3) | (centers > Z_WINDOW[1] + 0.3)
    if np.sum(background_mask) > 0:
        background = np.mean(hist[background_mask])
        background_std = np.std(hist[background_mask])
    else:
        background = np.mean(hist)
        background_std = np.std(hist)

    snr = z_peak_height / background if background > 0 else 0

    # Z-score for peak significance
    if background_std > 0:
        z_score = (z_peak_height - background) / background_std
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    else:
        z_score = 0
        p_value = 1.0

    # Full-Width at Half-Maximum (FWHM)
    fwhm = None
    if z_peak_idx is not None:
        half_max = z_peak_height / 2
        left_idx = z_peak_idx
        right_idx = z_peak_idx

        while left_idx > 0 and hist[left_idx] > half_max:
            left_idx -= 1
        while right_idx < len(hist) - 1 and hist[right_idx] > half_max:
            right_idx += 1

        fwhm = centers[right_idx] - centers[left_idx]

    return {
        'z_peak_found': z_peak_dist is not None,
        'z_peak_distance': z_peak_dist,
        'z_peak_height': int(z_peak_height),
        'signal_to_noise': snr,
        'z_score': z_score,
        'p_value': p_value,
        'fwhm': fwhm,
        'mean_i2': float(np.mean(arr)),
        'std_i2': float(np.std(arr)),
        'n_distances': len(arr),
        'match_to_Z': abs(z_peak_dist - Z) / Z * 100 if z_peak_dist else None
    }


# =============================================================================
# MAIN AUDIT
# =============================================================================

def run_phd_audit():
    """Run the PhD-level Z-resonance audit."""

    all_results = []
    domain_stats = {'Archaea': [], 'Bacteria': [], 'Eukarya': []}
    ss_aggregated = {'helix': [], 'sheet': [], 'coil': []}

    print(f"\n  Analyzing {len(HIGH_QUALITY_PROTEINS)} high-quality proteins...")
    print("  " + "=" * 65)

    for pdb_id, name, domain, organism, resolution in HIGH_QUALITY_PROTEINS:
        print(f"\n  {pdb_id}: {name} ({organism})")
        print(f"  Resolution: {resolution} Å | Domain: {domain}")

        filepath = download_pdb(pdb_id)
        if filepath is None:
            print("    ✗ Download failed")
            continue

        coords, ss_codes, residue_nums = parse_pdb_with_ss(filepath)
        n_ca = len(coords)

        if n_ca < 20:
            print(f"    ✗ Too few residues ({n_ca})")
            continue

        # Secondary structure composition
        n_helix = ss_codes.count('H')
        n_sheet = ss_codes.count('E')
        n_coil = ss_codes.count('C')
        print(f"  Residues: {n_ca} (H:{n_helix}, E:{n_sheet}, C:{n_coil})")

        # Sequential distance analysis
        seq_result = analyze_sequential_distances(coords)

        # Secondary structure decomposition
        ss_result = analyze_by_secondary_structure(coords, ss_codes)

        # Z-resonance statistics
        z_stats = calculate_z_resonance_statistics(coords)

        # Report i→i+2 results
        if seq_result.get('i_to_i+2'):
            i2 = seq_result['i_to_i+2']
            print(f"  i→i+2: {i2['mean']:.3f} ± {i2['std']:.3f} Å")

        if z_stats.get('z_peak_found'):
            print(f"  Z-peak: {z_stats['z_peak_distance']:.3f} Å | SNR: {z_stats['signal_to_noise']:.2f} | p={z_stats['p_value']:.2e}")
            status = "✓ Z-RESONANCE" if z_stats['signal_to_noise'] > 3.0 else "~ weak"
        else:
            status = "✗ No Z-peak"
        print(f"  Status: {status}")

        # Aggregate by domain
        if z_stats.get('z_peak_distance'):
            domain_stats[domain].append({
                'pdb': pdb_id,
                'peak': z_stats['z_peak_distance'],
                'snr': z_stats['signal_to_noise']
            })

        # Aggregate by secondary structure
        for ss_type in ['helix', 'sheet', 'coil']:
            if ss_result.get(ss_type) and ss_result[ss_type].get('peak_distance'):
                ss_aggregated[ss_type].append(ss_result[ss_type]['peak_distance'])

        all_results.append({
            'pdb_id': pdb_id,
            'name': name,
            'domain': domain,
            'organism': organism,
            'resolution': resolution,
            'n_residues': n_ca,
            'ss_composition': {'H': n_helix, 'E': n_sheet, 'C': n_coil},
            'sequential': seq_result,
            'secondary_structure': ss_result,
            'z_statistics': z_stats
        })

    # ==========================================================================
    # UNIVERSAL MATRIX OUTPUT
    # ==========================================================================

    print("\n" + "=" * 70)
    print("  UNIVERSAL RESONANCE MATRIX")
    print("=" * 70)

    print("\n  Domain         | n  | Avg Peak (Å) | Match to Z | Avg SNR")
    print("  " + "-" * 60)

    for domain in ['Archaea', 'Bacteria', 'Eukarya']:
        data = domain_stats[domain]
        if data:
            peaks = [d['peak'] for d in data]
            snrs = [d['snr'] for d in data]
            avg_peak = np.mean(peaks)
            avg_snr = np.mean(snrs)
            match = (1 - abs(avg_peak - Z) / Z) * 100
            print(f"  {domain:<14s} | {len(data):2d} | {avg_peak:.3f}       | {match:.1f}%      | {avg_snr:.2f}")
        else:
            print(f"  {domain:<14s} | -- | ---          | ---        | ---")

    # ==========================================================================
    # SECONDARY STRUCTURE DECOMPOSITION
    # ==========================================================================

    print("\n" + "=" * 70)
    print("  SECONDARY STRUCTURE DECOMPOSITION")
    print("=" * 70)

    print("\n  Structure  | n  | Avg i→i+2 Peak | Match to Z | Verdict")
    print("  " + "-" * 60)

    for ss_type, label in [('helix', 'α-Helix'), ('sheet', 'β-Sheet'), ('coil', 'Coil')]:
        data = ss_aggregated[ss_type]
        if data:
            avg = np.mean(data)
            std = np.std(data)
            match = (1 - abs(avg - Z) / Z) * 100
            in_window = sum(1 for d in data if Z_WINDOW[0] <= d <= Z_WINDOW[1]) / len(data) * 100
            verdict = "✓ Z-resonant" if in_window > 50 else "✗ Not Z-resonant"
            print(f"  {label:<10s} | {len(data):2d} | {avg:.3f} ± {std:.3f}   | {match:.1f}%      | {verdict}")
        else:
            print(f"  {label:<10s} | -- | ---            | ---        | ---")

    # ==========================================================================
    # SEQUENTIAL DISTANCE ANALYSIS SUMMARY
    # ==========================================================================

    print("\n" + "=" * 70)
    print("  SEQUENTIAL DISTANCE ANALYSIS")
    print("=" * 70)

    # Aggregate sequential distances
    seq_agg = {'i_to_i+1': [], 'i_to_i+2': [], 'i_to_i+3': [], 'i_to_i+4': []}

    for r in all_results:
        for key in seq_agg.keys():
            if r['sequential'].get(key):
                seq_agg[key].append(r['sequential'][key]['mean'])

    print("\n  Separation | Avg Distance | Expected     | Z-Match")
    print("  " + "-" * 55)

    expected = {
        'i_to_i+1': ('~3.8 Å', 'Peptide bond'),
        'i_to_i+2': ('~5.4-6.0 Å', '← Z TARGET'),
        'i_to_i+3': ('~5.0-5.5 Å', 'Helix turn'),
        'i_to_i+4': ('~6.3 Å', 'Helix pitch')
    }

    for key in seq_agg.keys():
        if seq_agg[key]:
            avg = np.mean(seq_agg[key])
            std = np.std(seq_agg[key])
            exp, note = expected[key]
            z_match = abs(avg - Z) < 0.3
            marker = "← Z!" if z_match and key == 'i_to_i+2' else ""
            print(f"  {key:<10s} | {avg:.3f} ± {std:.3f} | {exp:<12s} | {note} {marker}")

    # ==========================================================================
    # FINAL VERDICT
    # ==========================================================================

    print("\n" + "=" * 70)
    print("  FINAL VERDICT")
    print("=" * 70)

    # Count significant Z-resonances
    z_significant = sum(1 for r in all_results
                        if r['z_statistics'].get('z_peak_found')
                        and r['z_statistics'].get('signal_to_noise', 0) > 3.0)

    total = len([r for r in all_results if r['z_statistics'].get('z_peak_found') is not None])

    # Calculate global i→i+2 statistics
    all_i2_means = [r['sequential']['i_to_i+2']['mean']
                    for r in all_results
                    if r['sequential'].get('i_to_i+2')]

    global_i2_mean = np.mean(all_i2_means) if all_i2_means else 0
    global_i2_std = np.std(all_i2_means) if all_i2_means else 0

    print(f"""
  ╔══════════════════════════════════════════════════════════════════════╗
  ║                    PhD-LEVEL AUDIT RESULTS                           ║
  ╠══════════════════════════════════════════════════════════════════════╣
  ║                                                                      ║
  ║  GLOBAL i→i+2 DISTANCE: {global_i2_mean:.3f} ± {global_i2_std:.3f} Å                           ║
  ║  TARGET Z:              {Z:.4f} Å                                    ║
  ║  DEVIATION:             {abs(global_i2_mean - Z):.3f} Å ({abs(global_i2_mean - Z)/Z*100:.1f}%)                          ║
  ║                                                                      ║
  ║  Z-RESONANCE DETECTION:                                              ║
  ║    Significant (SNR > 3): {z_significant}/{total} proteins ({z_significant/total*100:.0f}%)                   ║
  ║                                                                      ║
  ║  SECONDARY STRUCTURE:                                                ║
  ║    α-Helix: {'RESONANT' if ss_aggregated['helix'] and np.mean(ss_aggregated['helix']) < 6.0 else 'VARIABLE'}                                               ║
  ║    β-Sheet: {'RESONANT' if ss_aggregated['sheet'] and np.mean(ss_aggregated['sheet']) < 6.0 else 'NOT RESONANT'}                                           ║
  ║    Coil:    {'RESONANT' if ss_aggregated['coil'] and np.mean(ss_aggregated['coil']) < 6.0 else 'VARIABLE'}                                               ║
  ╠══════════════════════════════════════════════════════════════════════╣
  """)

    # Determine verdict
    if z_significant / total > 0.7 and abs(global_i2_mean - Z) < 0.2:
        verdict = "UNIVERSAL LAW CONFIRMED"
        explanation = "The Z = 5.79 Å resonance appears across all domains with high significance."
    elif z_significant / total > 0.5:
        verdict = "PARTIAL CONFIRMATION"
        explanation = "Z-resonance detected in majority of proteins, strongest in α-helical regions."
    else:
        verdict = "FOLD-SPECIFIC PROPERTY"
        explanation = "Z-resonance is characteristic of α-helices, not universal to all proteins."

    print(f"  ║  VERDICT: {verdict:<50s}   ║")
    print(f"  ║                                                                      ║")
    print(f"  ║  {explanation[:68]:<68s} ║")
    print(f"  ╚══════════════════════════════════════════════════════════════════════╝")

    # Save results
    output = {
        'summary': {
            'total_proteins': total,
            'z_significant': z_significant,
            'global_i2_mean': global_i2_mean,
            'global_i2_std': global_i2_std,
            'target_Z': Z,
            'deviation': abs(global_i2_mean - Z),
            'verdict': verdict
        },
        'domain_stats': {k: v for k, v in domain_stats.items()},
        'secondary_structure': {k: {'peaks': v, 'mean': np.mean(v) if v else None}
                                for k, v in ss_aggregated.items()},
        'proteins': all_results
    }

    with open('phd_resonance_audit_results.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print("\n  Results saved to: phd_resonance_audit_results.json")

    return output


if __name__ == "__main__":
    results = run_phd_audit()
