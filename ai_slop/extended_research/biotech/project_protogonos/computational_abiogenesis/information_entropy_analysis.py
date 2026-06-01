#!/usr/bin/env python3
"""
Information Entropy Analysis: Does Z-Resonance Carry 41 Bits?
=============================================================

Project Protogonos - Final Validation Script

This script tests whether the Z = 5.79 Å backbone resonance pattern
encodes significant structural information, potentially ~41 bits as
hypothesized for minimal protein fold specification.

Information Theory Framework:
- Shannon entropy H(X) = -Σ p(x) log₂ p(x)
- Mutual information I(X;Y) = H(X) - H(X|Y)
- Kullback-Leibler divergence D_KL(P||Q) = Σ p(x) log₂(p(x)/q(x))

Key Questions:
1. How much information is in the i→i+2 distance distribution?
2. Does the Z-peak carry more information than random noise?
3. Is there mutual information between Z-resonance and fold type?
4. Does this approach the theoretical 41 bits for fold specification?

The 41 bits hypothesis:
- Levinthal's paradox suggests ~10^300 conformations
- But only ~10,000 known folds → log₂(10000) ≈ 13 bits for fold class
- Full backbone specification: ~3 bits/residue × 100 residues ≈ 300 bits
- Minimal fold specification (φ,ψ discretized): ~41 bits proposed

Author: Project Protogonos
Date: 2024
"""

import numpy as np
from scipy import stats
from scipy.special import rel_entr
from collections import defaultdict
import json
import warnings
warnings.filterwarnings('ignore')

# Z² Framework Constants
Z_SQUARED = 32 * np.pi / 3  # EXACTLY 32π/3
Z = np.sqrt(Z_SQUARED)       # 5.788810036466141 Å
Z_WINDOW = 0.15              # ±0.15 Å window for Z-peak detection

# Protein database with fold classifications (SCOP/CATH inspired)
PROTEIN_DATABASE = [
    # (PDB_ID, Name, Fold_Class, SCOP_Class)
    # Fold classes: all-α, all-β, α/β, α+β, small, membrane
    ('1AKE', 'Adenylate kinase', 'α/β', 'c.1'),
    ('1LYZ', 'Lysozyme', 'α+β', 'd.2'),
    ('1MBN', 'Myoglobin', 'all-α', 'a.1'),
    ('1UBQ', 'Ubiquitin', 'α+β', 'd.15'),
    ('2CY3', 'Cytochrome c3', 'all-α', 'a.3'),
    ('1CRN', 'Crambin', 'small', 'g.3'),
    ('1AJ8', 'Rubredoxin', 'small', 'g.41'),
    ('1TIM', 'Triosephosphate isomerase', 'α/β', 'c.1'),
    ('1GCN', 'Glucagon', 'all-α', 'a.24'),
    ('1PLW', 'Plastocyanin', 'all-β', 'b.6'),
    ('1WLA', 'WW domain', 'all-β', 'b.72'),
    ('2GB1', 'Protein G B1', 'α+β', 'd.15'),
    ('1VII', 'Villin headpiece', 'all-α', 'a.39'),
    ('1L2Y', 'Trp-cage', 'small', 'g.67'),
    ('1IGD', 'Immunoglobulin', 'all-β', 'b.1'),
    ('1HRC', 'Cytochrome c', 'all-α', 'a.3'),
    # IDPs for contrast
    ('1XQ8', 'α-Synuclein', 'IDP', 'disordered'),
    ('2N0A', 'Tau', 'IDP', 'disordered'),
    ('1IYT', 'Amyloid-β', 'IDP', 'disordered'),
]


def fetch_pdb_structure(pdb_id: str):
    """Fetch PDB structure and extract CA coordinates."""
    import urllib.request
    import gzip
    import io

    url = f"https://files.rcsb.org/download/{pdb_id}.pdb.gz"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            compressed = response.read()

        with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as f:
            pdb_content = f.read().decode('utf-8')

        # Parse CA atoms
        ca_coords = []
        residue_info = []

        for line in pdb_content.split('\n'):
            if line.startswith('ATOM') and line[12:16].strip() == 'CA':
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    resname = line[17:20].strip()
                    resnum = int(line[22:26])
                    chain = line[21]
                    ca_coords.append([x, y, z])
                    residue_info.append({
                        'resname': resname,
                        'resnum': resnum,
                        'chain': chain
                    })
                except (ValueError, IndexError):
                    continue

        return np.array(ca_coords), residue_info

    except Exception as e:
        return None, str(e)


def calculate_i_plus_2_distances(coords: np.ndarray) -> np.ndarray:
    """Calculate all i→i+2 backbone distances."""
    if len(coords) < 3:
        return np.array([])

    distances = []
    for i in range(len(coords) - 2):
        d = np.linalg.norm(coords[i+2] - coords[i])
        distances.append(d)

    return np.array(distances)


def shannon_entropy(data: np.ndarray, n_bins: int = 50,
                    range_min: float = 4.0, range_max: float = 9.0) -> dict:
    """
    Calculate Shannon entropy of a distribution.

    Returns entropy in bits and the probability distribution.
    """
    if len(data) == 0:
        return {'entropy': 0, 'p': np.array([]), 'bins': np.array([])}

    # Create histogram (probability distribution)
    counts, bin_edges = np.histogram(data, bins=n_bins, range=(range_min, range_max))

    # Normalize to probabilities
    p = counts / counts.sum() if counts.sum() > 0 else counts

    # Remove zeros (log(0) undefined)
    p_nonzero = p[p > 0]

    # Shannon entropy: H = -Σ p log₂(p)
    entropy = -np.sum(p_nonzero * np.log2(p_nonzero))

    # Maximum possible entropy (uniform distribution)
    max_entropy = np.log2(n_bins)

    # Normalized entropy (0 = deterministic, 1 = uniform)
    normalized = entropy / max_entropy if max_entropy > 0 else 0

    return {
        'entropy': entropy,
        'max_entropy': max_entropy,
        'normalized_entropy': normalized,
        'p': p,
        'bins': bin_edges,
        'n_bins': n_bins
    }


def kl_divergence(p: np.ndarray, q: np.ndarray) -> float:
    """
    Calculate Kullback-Leibler divergence D_KL(P||Q).

    Measures how much P diverges from reference Q.
    Returns bits of information.
    """
    # Add small epsilon to avoid log(0)
    eps = 1e-10
    p = p + eps
    q = q + eps

    # Normalize
    p = p / p.sum()
    q = q / q.sum()

    # D_KL = Σ p log(p/q)
    return np.sum(rel_entr(p, q)) / np.log(2)  # Convert to bits


def create_z_reference_distribution(n_bins: int = 50,
                                    range_min: float = 4.0,
                                    range_max: float = 9.0) -> np.ndarray:
    """
    Create a reference distribution centered on Z = 5.79 Å.

    This represents the "ideal" Z-resonant distribution.
    """
    bin_centers = np.linspace(range_min, range_max, n_bins)

    # Gaussian centered on Z
    sigma = 0.3  # Å - expected thermal width
    z_dist = np.exp(-0.5 * ((bin_centers - Z) / sigma)**2)

    return z_dist / z_dist.sum()


def create_random_walk_distribution(n_bins: int = 50,
                                    range_min: float = 4.0,
                                    range_max: float = 9.0) -> np.ndarray:
    """
    Create null hypothesis: random coil distribution.

    For a freely-jointed chain, i→i+2 distance follows
    a Maxwell-Boltzmann-like distribution.
    """
    bin_centers = np.linspace(range_min, range_max, n_bins)

    # Random coil: broad distribution centered ~6.5 Å
    # Based on Flory random coil statistics
    mu = 6.5  # Expected mean for random coil
    sigma = 1.5  # Broad distribution

    random_dist = np.exp(-0.5 * ((bin_centers - mu) / sigma)**2)

    return random_dist / random_dist.sum()


def calculate_z_information_content(p_observed: np.ndarray, n_bins: int = 50,
                                    range_min: float = 4.0,
                                    range_max: float = 9.0) -> dict:
    """
    Calculate how much information the Z-peak carries above random coil.

    Information content = D_KL(observed || random)
    """
    # Reference distributions
    q_random = create_random_walk_distribution(n_bins, range_min, range_max)
    q_z_ideal = create_z_reference_distribution(n_bins, range_min, range_max)

    # Information relative to random (how ordered is it?)
    info_vs_random = kl_divergence(p_observed, q_random)

    # Information relative to Z-ideal (how close to Z?)
    info_vs_z = kl_divergence(p_observed, q_z_ideal)

    # Z-resonance information: random→observed - random→Z_ideal
    # This measures how much the observed distribution "knows" about Z
    z_information = info_vs_random - info_vs_z

    return {
        'info_vs_random': info_vs_random,
        'info_vs_z_ideal': info_vs_z,
        'z_resonance_info': z_information,
        'total_ordering_bits': info_vs_random
    }


def calculate_mutual_information(distances_by_fold: dict, n_bins: int = 50) -> dict:
    """
    Calculate mutual information I(Distance; Fold_Class).

    I(D;F) = H(D) - H(D|F)

    This measures how much knowing the distance distribution
    tells us about the fold class.
    """
    # Combine all distances for marginal H(D)
    all_distances = []
    fold_classes = list(distances_by_fold.keys())

    for fold, distances in distances_by_fold.items():
        all_distances.extend(distances)

    all_distances = np.array(all_distances)

    # Marginal entropy H(D)
    h_d = shannon_entropy(all_distances, n_bins)['entropy']

    # Conditional entropy H(D|F) = Σ P(F) H(D|F=f)
    h_d_given_f = 0
    total_n = len(all_distances)

    for fold, distances in distances_by_fold.items():
        if len(distances) == 0:
            continue
        p_f = len(distances) / total_n  # P(F=f)
        h_d_f = shannon_entropy(np.array(distances), n_bins)['entropy']  # H(D|F=f)
        h_d_given_f += p_f * h_d_f

    # Mutual information
    mutual_info = h_d - h_d_given_f

    # Normalized mutual information
    h_f = np.log2(len(fold_classes))  # H(F) assuming uniform
    normalized_mi = mutual_info / h_f if h_f > 0 else 0

    return {
        'H_D': h_d,
        'H_D_given_F': h_d_given_f,
        'I_D_F': mutual_info,
        'normalized_MI': normalized_mi,
        'n_fold_classes': len(fold_classes)
    }


def calculate_z_peak_information(distances: np.ndarray) -> dict:
    """
    Calculate specific information content of the Z-peak region.

    Focuses on the ±0.15 Å window around Z = 5.79 Å.
    """
    if len(distances) == 0:
        return {'z_peak_bits': 0, 'z_peak_fraction': 0}

    # Distances in Z window
    z_mask = np.abs(distances - Z) < Z_WINDOW
    z_fraction = z_mask.sum() / len(distances)

    # Self-information of Z-peak: -log₂(p_z)
    # If Z-peak is rare (low p), it carries MORE information
    if z_fraction > 0:
        z_self_info = -np.log2(z_fraction)
    else:
        z_self_info = np.inf

    # Expected Z-peak fraction under null (random coil)
    # For a broad distribution σ~1.5 Å, ±0.15 Å window captures ~8%
    null_fraction = 0.08

    # Surprise relative to null
    if z_fraction > 0:
        surprise = np.log2(z_fraction / null_fraction)
    else:
        surprise = -np.inf

    return {
        'z_peak_fraction': z_fraction,
        'z_self_info_bits': z_self_info,
        'z_surprise_bits': surprise,  # + means more than expected, - means less
        'is_z_enriched': z_fraction > null_fraction
    }


def analyze_protein_information(pdb_id: str, name: str,
                                fold_class: str, scop_class: str) -> dict:
    """Comprehensive information analysis for a single protein."""

    # Fetch structure
    coords, residue_info = fetch_pdb_structure(pdb_id)

    if coords is None or len(coords) < 10:
        return {'status': 'FAILED', 'pdb_id': pdb_id, 'error': str(residue_info)}

    # Calculate distances
    distances = calculate_i_plus_2_distances(coords)

    if len(distances) < 5:
        return {'status': 'FAILED', 'pdb_id': pdb_id, 'error': 'Too few distances'}

    # Shannon entropy
    entropy_result = shannon_entropy(distances)

    # Z-specific information
    z_info = calculate_z_information_content(
        entropy_result['p'],
        entropy_result['n_bins']
    )

    # Z-peak information
    z_peak_info = calculate_z_peak_information(distances)

    return {
        'status': 'OK',
        'pdb_id': pdb_id,
        'name': name,
        'fold_class': fold_class,
        'scop_class': scop_class,
        'n_residues': len(coords),
        'n_distances': len(distances),
        'mean_distance': float(np.mean(distances)),
        'std_distance': float(np.std(distances)),
        'shannon_entropy': float(entropy_result['entropy']),
        'max_entropy': float(entropy_result['max_entropy']),
        'normalized_entropy': float(entropy_result['normalized_entropy']),
        'info_vs_random': float(z_info['info_vs_random']),
        'info_vs_z_ideal': float(z_info['info_vs_z_ideal']),
        'z_resonance_info': float(z_info['z_resonance_info']),
        'z_peak_fraction': float(z_peak_info['z_peak_fraction']),
        'z_self_info_bits': float(z_peak_info['z_self_info_bits']),
        'z_surprise_bits': float(z_peak_info['z_surprise_bits']),
        'is_z_enriched': bool(z_peak_info['is_z_enriched']),
        'distances': distances.tolist()
    }


def calculate_total_fold_information(results: list) -> dict:
    """
    Calculate total information content for fold specification.

    Tests the 41 bits hypothesis.
    """
    # Group by fold class
    distances_by_fold = defaultdict(list)

    for r in results:
        if r['status'] != 'OK':
            continue
        distances_by_fold[r['fold_class']].extend(r['distances'])

    # Mutual information between distance and fold
    mi_result = calculate_mutual_information(distances_by_fold)

    # Average per-residue information
    total_residues = sum(r['n_residues'] for r in results if r['status'] == 'OK')
    total_distances = sum(r['n_distances'] for r in results if r['status'] == 'OK')

    avg_entropy = np.mean([r['shannon_entropy'] for r in results if r['status'] == 'OK'])
    avg_info_vs_random = np.mean([r['info_vs_random'] for r in results if r['status'] == 'OK'])

    # Per-residue information content
    if total_distances > 0:
        bits_per_residue = avg_info_vs_random * total_distances / total_residues
    else:
        bits_per_residue = 0

    # Estimate total fold information
    # Based on backbone distance constraints
    avg_residues = total_residues / len([r for r in results if r['status'] == 'OK'])
    estimated_fold_bits = bits_per_residue * avg_residues

    return {
        'mutual_info_distance_fold': mi_result['I_D_F'],
        'H_distance': mi_result['H_D'],
        'H_distance_given_fold': mi_result['H_D_given_F'],
        'normalized_MI': mi_result['normalized_MI'],
        'n_fold_classes': mi_result['n_fold_classes'],
        'avg_shannon_entropy': avg_entropy,
        'avg_info_vs_random': avg_info_vs_random,
        'bits_per_residue': bits_per_residue,
        'estimated_fold_bits': estimated_fold_bits,
        'target_41_bits': 41.0,
        'fraction_of_target': estimated_fold_bits / 41.0
    }


def calculate_information_spectrum(distances: np.ndarray,
                                   n_positions: int = 100) -> dict:
    """
    Calculate position-specific information content.

    Sliding window analysis to find where Z-information concentrates.
    """
    window_centers = np.linspace(4.5, 8.0, n_positions)
    window_width = 0.3  # Å

    info_spectrum = []

    for center in window_centers:
        # Distances in window
        mask = np.abs(distances - center) < window_width
        fraction = mask.sum() / len(distances) if len(distances) > 0 else 0

        # Self-information
        if fraction > 0:
            self_info = -np.log2(fraction)
        else:
            self_info = np.nan

        info_spectrum.append({
            'center': center,
            'fraction': fraction,
            'self_info': self_info
        })

    # Find minimum self-info (maximum probability peak)
    valid_info = [(s['center'], s['self_info']) for s in info_spectrum
                  if not np.isnan(s['self_info'])]

    if valid_info:
        peak_center, peak_info = min(valid_info, key=lambda x: x[1])
    else:
        peak_center, peak_info = Z, np.nan

    # Z-specific information
    z_idx = np.argmin(np.abs(window_centers - Z))
    z_info = info_spectrum[z_idx]['self_info'] if z_idx < len(info_spectrum) else np.nan

    return {
        'spectrum': info_spectrum,
        'peak_center': float(peak_center),
        'peak_self_info': float(peak_info) if not np.isnan(peak_info) else None,
        'z_position_info': float(z_info) if not np.isnan(z_info) else None,
        'z_offset': float(peak_center - Z)
    }


def run_information_entropy_analysis():
    """Main analysis: Test the 41 bits hypothesis."""

    print("=" * 70)
    print("INFORMATION ENTROPY ANALYSIS: Does Z-Resonance Carry 41 Bits?")
    print("=" * 70)
    print(f"\nZ² = 32π/3 = {Z_SQUARED:.6f}")
    print(f"Z = √(32π/3) = {Z:.6f} Å")
    print(f"Z-window: ±{Z_WINDOW} Å")
    print("\n" + "-" * 70)

    # Analyze all proteins
    results = []

    print("\nAnalyzing proteins...")
    print("-" * 70)
    print(f"{'PDB':<6} {'Name':<25} {'Fold':<8} {'H(D)':<8} {'I_Z':<8} {'Z-frac':<8}")
    print("-" * 70)

    for pdb_id, name, fold_class, scop_class in PROTEIN_DATABASE:
        result = analyze_protein_information(pdb_id, name, fold_class, scop_class)
        results.append(result)

        if result['status'] == 'OK':
            print(f"{pdb_id:<6} {name[:24]:<25} {fold_class:<8} "
                  f"{result['shannon_entropy']:.3f}    "
                  f"{result['z_resonance_info']:.3f}    "
                  f"{result['z_peak_fraction']:.3f}")
        else:
            print(f"{pdb_id:<6} {name[:24]:<25} FAILED")

    # Calculate fold-level information
    print("\n" + "=" * 70)
    print("FOLD-LEVEL INFORMATION ANALYSIS")
    print("=" * 70)

    fold_info = calculate_total_fold_information(results)

    print(f"\nMutual Information I(Distance; Fold):")
    print(f"  I(D;F) = {fold_info['mutual_info_distance_fold']:.4f} bits")
    print(f"  H(D) = {fold_info['H_distance']:.4f} bits")
    print(f"  H(D|F) = {fold_info['H_distance_given_fold']:.4f} bits")
    print(f"  Normalized MI = {fold_info['normalized_MI']:.4f}")

    print(f"\nPer-Residue Information Content:")
    print(f"  Average Shannon entropy: {fold_info['avg_shannon_entropy']:.4f} bits")
    print(f"  Average info vs random: {fold_info['avg_info_vs_random']:.4f} bits")
    print(f"  Bits per residue: {fold_info['bits_per_residue']:.4f} bits")

    print(f"\nEstimated Total Fold Information:")
    print(f"  Estimated: {fold_info['estimated_fold_bits']:.2f} bits")
    print(f"  Target (41 bits hypothesis): {fold_info['target_41_bits']:.0f} bits")
    print(f"  Fraction of target: {fold_info['fraction_of_target']:.2%}")

    # Z-resonance specific analysis
    print("\n" + "=" * 70)
    print("Z-RESONANCE INFORMATION CONTENT")
    print("=" * 70)

    ok_results = [r for r in results if r['status'] == 'OK']

    # Separate ordered vs IDP
    ordered = [r for r in ok_results if r['fold_class'] != 'IDP']
    idp = [r for r in ok_results if r['fold_class'] == 'IDP']

    print(f"\nOrdered Proteins (n={len(ordered)}):")
    if ordered:
        avg_z_info = np.mean([r['z_resonance_info'] for r in ordered])
        avg_z_frac = np.mean([r['z_peak_fraction'] for r in ordered])
        z_enriched = sum(1 for r in ordered if r['is_z_enriched'])
        print(f"  Average Z-resonance info: {avg_z_info:.4f} bits")
        print(f"  Average Z-peak fraction: {avg_z_frac:.3f}")
        print(f"  Z-enriched: {z_enriched}/{len(ordered)} ({100*z_enriched/len(ordered):.0f}%)")

    print(f"\nIntrinsically Disordered Proteins (n={len(idp)}):")
    if idp:
        avg_z_info_idp = np.mean([r['z_resonance_info'] for r in idp])
        avg_z_frac_idp = np.mean([r['z_peak_fraction'] for r in idp])
        z_enriched_idp = sum(1 for r in idp if r['is_z_enriched'])
        print(f"  Average Z-resonance info: {avg_z_info_idp:.4f} bits")
        print(f"  Average Z-peak fraction: {avg_z_frac_idp:.3f}")
        print(f"  Z-enriched: {z_enriched_idp}/{len(idp)} ({100*z_enriched_idp/len(idp) if idp else 0:.0f}%)")

    # Information comparison: ordered vs IDP
    if ordered and idp:
        info_ratio = avg_z_info / avg_z_info_idp if avg_z_info_idp != 0 else float('inf')
        print(f"\n  Information ratio (ordered/IDP): {info_ratio:.2f}x")

    # Calculate Z-specific bits
    print("\n" + "=" * 70)
    print("Z-POSITION SPECIFIC INFORMATION")
    print("=" * 70)

    # Combine all ordered distances
    all_ordered_distances = []
    for r in ordered:
        all_ordered_distances.extend(r['distances'])
    all_ordered_distances = np.array(all_ordered_distances)

    if len(all_ordered_distances) > 0:
        spectrum = calculate_information_spectrum(all_ordered_distances)

        print(f"\nInformation Spectrum Analysis (ordered proteins):")
        print(f"  Peak position: {spectrum['peak_center']:.3f} Å")
        print(f"  Peak self-info: {spectrum['peak_self_info']:.3f} bits")
        print(f"  Z-position info: {spectrum['z_position_info']:.3f} bits")
        print(f"  Offset from Z: {spectrum['z_offset']:.3f} Å")

        # Is the peak at Z?
        if abs(spectrum['z_offset']) < 0.2:
            print(f"\n  ✓ Peak IS at Z (offset < 0.2 Å)")
        else:
            print(f"\n  ✗ Peak NOT at Z (offset = {spectrum['z_offset']:.3f} Å)")

    # Final verdict
    print("\n" + "=" * 70)
    print("FINAL VERDICT: 41 BITS HYPOTHESIS")
    print("=" * 70)

    # Calculate actual Z-encoded bits
    z_specific_bits = fold_info['mutual_info_distance_fold']

    # Estimate information in Z-peak specifically
    if ordered:
        avg_z_surprise = np.mean([r['z_surprise_bits'] for r in ordered
                                  if not np.isinf(r['z_surprise_bits'])])
    else:
        avg_z_surprise = 0

    total_z_bits = z_specific_bits + avg_z_surprise

    print(f"\nZ-Resonance Information Content:")
    print(f"  Mutual info (distance↔fold): {z_specific_bits:.3f} bits")
    print(f"  Z-peak surprise (vs random): {avg_z_surprise:.3f} bits")
    print(f"  Total Z-encoded information: {total_z_bits:.3f} bits")
    print(f"  Target (41 bits): 41.0 bits")
    print(f"  Fraction achieved: {total_z_bits/41*100:.1f}%")

    # Per-distance-constraint contribution
    avg_constraint_bits = total_z_bits / (len(all_ordered_distances) / len(ordered)) if ordered else 0
    bits_needed = 41 / avg_constraint_bits if avg_constraint_bits > 0 else float('inf')

    print(f"\nScaling Analysis:")
    print(f"  Average residues per protein: {np.mean([r['n_residues'] for r in ordered]):.0f}")
    print(f"  Bits per i→i+2 constraint: {avg_constraint_bits:.4f}")
    print(f"  Constraints needed for 41 bits: {bits_needed:.0f}")

    # Verdict
    if total_z_bits > 10:
        verdict = "SIGNIFICANT Z-INFORMATION"
        explanation = "Z-resonance carries meaningful structural information"
    elif total_z_bits > 5:
        verdict = "MODERATE Z-INFORMATION"
        explanation = "Z-resonance carries detectable but limited information"
    else:
        verdict = "WEAK Z-INFORMATION"
        explanation = "Z-resonance alone insufficient for fold specification"

    print(f"\n{'='*70}")
    print(f"VERDICT: {verdict}")
    print(f"{'='*70}")
    print(f"\n{explanation}")
    print(f"\nThe Z-resonance at 5.79 Å encodes ~{total_z_bits:.1f} bits of structural")
    print(f"information, which is {total_z_bits/41*100:.0f}% of the hypothesized 41 bits")
    print(f"needed for minimal fold specification.")

    if total_z_bits < 41:
        deficit = 41 - total_z_bits
        print(f"\nThe remaining ~{deficit:.0f} bits must come from:")
        print(f"  - Side chain interactions")
        print(f"  - Hydrogen bonding patterns")
        print(f"  - Hydrophobic core packing")
        print(f"  - Solvent interactions")

    # Save results
    output = {
        'summary': {
            'total_z_bits': total_z_bits,
            'target_bits': 41.0,
            'fraction_achieved': total_z_bits / 41,
            'mutual_info_distance_fold': z_specific_bits,
            'z_peak_surprise': avg_z_surprise,
            'verdict': verdict,
            'Z': Z,
            'n_proteins_analyzed': len(ok_results)
        },
        'fold_info': {k: float(v) if isinstance(v, (np.floating, np.integer)) else v
                      for k, v in fold_info.items()},
        'protein_results': [{k: v for k, v in r.items() if k != 'distances'}
                           for r in results]
    }

    with open('information_entropy_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: information_entropy_results.json")

    return output


if __name__ == '__main__':
    run_information_entropy_analysis()
