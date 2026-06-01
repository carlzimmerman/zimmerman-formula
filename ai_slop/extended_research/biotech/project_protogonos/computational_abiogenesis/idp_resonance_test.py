#!/usr/bin/env python3
"""
idp_resonance_test.py

INTRINSICALLY DISORDERED PROTEIN (IDP) Z-RESONANCE TEST

THE CRITICAL QUESTION:
Does the Z = 5.79 Å peak persist in proteins that LACK fixed 3D structure?

If YES: Z is a FUNDAMENTAL CONSTRAINT on the polypeptide chain itself,
        predating the evolution of folds.

If NO:  Z is an EVOLVED PROPERTY optimized for structural stability.

IDPs to test:
- α-synuclein (Parkinson's disease)
- Tau protein (Alzheimer's disease)
- p53 transactivation domain
- Amyloid-β precursor regions
- SUMO interaction motifs

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
Z_WINDOW = (5.65, 5.95)  # Target range

print("=" * 70)
print("IDP Z-RESONANCE TEST: THE FUNDAMENTAL CONSTRAINT HYPOTHESIS")
print("=" * 70)
print(f"""
  HYPOTHESIS:
  If Z = {Z:.4f} Å is a pre-folding constraint on the polypeptide chain,
  it should appear in Intrinsically Disordered Proteins (IDPs) that
  lack fixed secondary or tertiary structure.

  IDPs are "natively unfolded" - they sample many conformations.
  NMR ensembles capture this conformational diversity.

  PREDICTION:
  The i→i+2 distance distribution in IDPs should peak at Z ≈ 5.79 Å,
  matching the COIL regions of folded proteins (5.85 Å observed).
""")


# =============================================================================
# IDP DATABASE
# =============================================================================

# Known IDPs with PDB structures (mostly NMR ensembles)
IDP_DATABASE = [
    # Classic IDPs
    ('1XQ8', 'α-Synuclein', 'Human', 'Parkinson disease', 'NMR ensemble'),
    ('2N0A', 'Tau (repeat region)', 'Human', 'Alzheimer disease', 'NMR'),
    ('1YCR', 'p53 TAD (MDM2 bound)', 'Human', 'Tumor suppressor', 'NMR'),
    ('2L14', 'SUMO interaction motif', 'Human', 'Signaling', 'NMR'),

    # Partially disordered / flexible regions
    ('1D3Z', 'Ubiquitin (flexible)', 'Human', 'Reference', 'NMR ensemble'),
    ('2KKW', 'Amyloid-β (1-40)', 'Human', 'Alzheimer disease', 'NMR'),
    ('1IYT', 'Amyloid-β (1-42)', 'Human', 'Alzheimer disease', 'NMR'),
    ('2MXU', 'α-Synuclein micelle', 'Human', 'Membrane-bound', 'NMR'),

    # Disordered linkers and loops
    ('1SSX', 'Stathmin', 'Human', 'Microtubule regulation', 'X-ray'),
    ('2K39', 'HMGB1 (disordered tail)', 'Human', 'Chromatin', 'NMR'),

    # Control: highly ordered proteins for comparison
    ('1UBQ', 'Ubiquitin (ordered)', 'Human', 'Control - ordered', 'X-ray'),
    ('1MBN', 'Myoglobin (ordered)', 'Whale', 'Control - ordered', 'X-ray'),
]


# =============================================================================
# ANALYSIS FUNCTIONS
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
    except Exception as e:
        print(f"    Download failed: {e}")
        return None


def parse_nmr_ensemble(filepath: str) -> List[np.ndarray]:
    """
    Parse NMR ensemble PDB file - extract C-alpha coords for each model.

    NMR structures contain multiple MODELs representing conformational diversity.
    This is ideal for IDP analysis.
    """
    models = []
    current_model = []
    in_model = False

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('MODEL'):
                in_model = True
                current_model = []
            elif line.startswith('ENDMDL'):
                if current_model:
                    models.append(np.array(current_model))
                current_model = []
                in_model = False
            elif line.startswith('ATOM') and ' CA ' in line:
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    current_model.append([x, y, z])
                except:
                    pass

    # If no MODEL records, treat as single structure
    if not models and current_model:
        models.append(np.array(current_model))

    # If still no models, parse without MODEL records
    if not models:
        coords = []
        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith('ATOM') and ' CA ' in line:
                    try:
                        x = float(line[30:38])
                        y = float(line[38:46])
                        z = float(line[46:54])
                        coords.append([x, y, z])
                    except:
                        pass
        if coords:
            models.append(np.array(coords))

    return models


def calculate_i_to_i2_distances(coords: np.ndarray) -> np.ndarray:
    """Calculate all i→i+2 distances for a single structure."""
    n = len(coords)
    distances = []
    for i in range(n - 2):
        d = np.linalg.norm(coords[i + 2] - coords[i])
        distances.append(d)
    return np.array(distances)


def analyze_idp_ensemble(models: List[np.ndarray]) -> Dict:
    """
    Analyze i→i+2 distances across all models in an NMR ensemble.

    For IDPs, we expect:
    - Higher variance (more conformational diversity)
    - Peak near Z = 5.79 Å (if hypothesis is correct)
    """
    all_distances = []
    per_model_means = []

    for model in models:
        if len(model) < 5:
            continue
        distances = calculate_i_to_i2_distances(model)
        all_distances.extend(distances)
        per_model_means.append(np.mean(distances))

    if not all_distances:
        return {'status': 'NO_DATA'}

    arr = np.array(all_distances)

    # High-resolution histogram
    bins = np.linspace(4.0, 8.0, 81)  # 0.05 Å resolution
    hist, edges = np.histogram(arr, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2

    # Find peaks
    peaks, _ = find_peaks(hist, height=len(arr) * 0.005)
    peak_distances = [centers[p] for p in peaks]
    peak_heights = [hist[p] for p in peaks]

    # Find peak closest to Z
    z_peak = None
    z_peak_height = 0
    for d, h in zip(peak_distances, peak_heights):
        if Z_WINDOW[0] <= d <= Z_WINDOW[1]:
            if h > z_peak_height:
                z_peak = d
                z_peak_height = h

    # Signal-to-noise
    if len(hist) > 0:
        background = np.mean(hist[hist > 0])
        snr = z_peak_height / background if background > 0 and z_peak_height > 0 else 0
    else:
        snr = 0

    # Variance analysis (IDPs should show higher variance)
    variance = np.var(arr)

    # Per-model variance (conformational diversity)
    if len(per_model_means) > 1:
        inter_model_variance = np.var(per_model_means)
    else:
        inter_model_variance = 0

    return {
        'status': 'OK',
        'n_models': len(models),
        'n_distances': len(arr),
        'mean': float(np.mean(arr)),
        'std': float(np.std(arr)),
        'variance': float(variance),
        'inter_model_variance': float(inter_model_variance),
        'z_peak': z_peak,
        'z_peak_height': int(z_peak_height) if z_peak_height else 0,
        'snr': float(snr),
        'all_peaks': list(zip(peak_distances[:5], peak_heights[:5])),
        'in_z_window_fraction': float(np.mean((arr >= Z_WINDOW[0]) & (arr <= Z_WINDOW[1]))),
        'histogram': {'centers': centers.tolist(), 'counts': hist.tolist()}
    }


# =============================================================================
# MAIN TEST
# =============================================================================

def run_idp_test():
    """Run the IDP Z-resonance test."""

    results = {
        'idp': [],
        'ordered_control': []
    }

    print(f"\n  Testing {len(IDP_DATABASE)} proteins...")
    print("  " + "=" * 65)

    for pdb_id, name, organism, category, method in IDP_DATABASE:
        print(f"\n  {pdb_id}: {name}")
        print(f"  Category: {category} | Method: {method}")

        filepath = download_pdb(pdb_id)
        if filepath is None:
            print("    ✗ Download failed")
            continue

        models = parse_nmr_ensemble(filepath)

        if not models:
            print("    ✗ No models found")
            continue

        print(f"    Models: {len(models)} | Residues: {len(models[0]) if models else 0}")

        analysis = analyze_idp_ensemble(models)

        if analysis['status'] != 'OK':
            print(f"    ✗ Analysis failed: {analysis['status']}")
            continue

        # Classify result
        is_ordered = 'Control' in category

        analysis['pdb_id'] = pdb_id
        analysis['name'] = name
        analysis['category'] = category
        analysis['method'] = method

        if is_ordered:
            results['ordered_control'].append(analysis)
        else:
            results['idp'].append(analysis)

        # Report
        z_status = f"Z-peak: {analysis['z_peak']:.3f} Å" if analysis['z_peak'] else "No Z-peak"
        print(f"    i→i+2: {analysis['mean']:.3f} ± {analysis['std']:.3f} Å")
        print(f"    Variance: {analysis['variance']:.3f} Å²")
        print(f"    {z_status} | SNR: {analysis['snr']:.2f}")

        if analysis['z_peak'] and Z_WINDOW[0] <= analysis['z_peak'] <= Z_WINDOW[1]:
            if analysis['snr'] > 2.0:
                print("    ✓ Z-RESONANCE DETECTED")
            else:
                print("    ~ Weak Z-signal")
        else:
            print("    ✗ No Z-resonance in target window")

    # ==========================================================================
    # COMPARATIVE ANALYSIS
    # ==========================================================================

    print("\n" + "=" * 70)
    print("  IDP vs ORDERED PROTEIN COMPARISON")
    print("=" * 70)

    # IDP statistics
    idp_data = results['idp']
    if idp_data:
        idp_means = [r['mean'] for r in idp_data]
        idp_variances = [r['variance'] for r in idp_data]
        idp_z_peaks = [r['z_peak'] for r in idp_data if r['z_peak']]
        idp_z_fraction = [r['in_z_window_fraction'] for r in idp_data]

        print(f"\n  INTRINSICALLY DISORDERED PROTEINS (n={len(idp_data)}):")
        print(f"    Mean i→i+2:  {np.mean(idp_means):.3f} ± {np.std(idp_means):.3f} Å")
        print(f"    Avg variance: {np.mean(idp_variances):.3f} Å²")
        print(f"    Z-peak found: {len(idp_z_peaks)}/{len(idp_data)}")
        if idp_z_peaks:
            print(f"    Avg Z-peak:   {np.mean(idp_z_peaks):.3f} Å")
        print(f"    In Z-window:  {np.mean(idp_z_fraction)*100:.1f}% of distances")

    # Ordered control statistics
    ord_data = results['ordered_control']
    if ord_data:
        ord_means = [r['mean'] for r in ord_data]
        ord_variances = [r['variance'] for r in ord_data]
        ord_z_peaks = [r['z_peak'] for r in ord_data if r['z_peak']]
        ord_z_fraction = [r['in_z_window_fraction'] for r in ord_data]

        print(f"\n  ORDERED CONTROLS (n={len(ord_data)}):")
        print(f"    Mean i→i+2:  {np.mean(ord_means):.3f} ± {np.std(ord_means):.3f} Å")
        print(f"    Avg variance: {np.mean(ord_variances):.3f} Å²")
        print(f"    Z-peak found: {len(ord_z_peaks)}/{len(ord_data)}")
        if ord_z_peaks:
            print(f"    Avg Z-peak:   {np.mean(ord_z_peaks):.3f} Å")
        print(f"    In Z-window:  {np.mean(ord_z_fraction)*100:.1f}% of distances")

    # Statistical comparison
    if idp_data and ord_data:
        print("\n  STATISTICAL COMPARISON:")

        # T-test on means
        t_stat, p_mean = stats.ttest_ind(idp_means, ord_means)
        print(f"    Mean difference p-value: {p_mean:.4f}")

        # Variance ratio (F-test)
        f_stat = np.mean(idp_variances) / np.mean(ord_variances) if np.mean(ord_variances) > 0 else 0
        print(f"    Variance ratio (IDP/Ordered): {f_stat:.2f}")

        if f_stat > 1.5:
            print("    → IDPs show HIGHER conformational diversity (as expected)")

    # ==========================================================================
    # VERDICT
    # ==========================================================================

    print("\n" + "=" * 70)
    print("  VERDICT: THE FUNDAMENTAL CONSTRAINT HYPOTHESIS")
    print("=" * 70)

    # Calculate Z-resonance rates
    idp_z_rate = len([r for r in idp_data if r['z_peak'] and Z_WINDOW[0] <= r['z_peak'] <= Z_WINDOW[1]]) / len(idp_data) if idp_data else 0
    ord_z_rate = len([r for r in ord_data if r['z_peak'] and Z_WINDOW[0] <= r['z_peak'] <= Z_WINDOW[1]]) / len(ord_data) if ord_data else 0

    # Overall IDP mean
    overall_idp_mean = np.mean(idp_means) if idp_data else 0
    deviation_from_z = abs(overall_idp_mean - Z)

    print(f"""
  ╔══════════════════════════════════════════════════════════════════════╗
  ║                    IDP Z-RESONANCE RESULTS                           ║
  ╠══════════════════════════════════════════════════════════════════════╣
  ║                                                                      ║
  ║  TARGET Z:          {Z:.4f} Å                                        ║
  ║  IDP i→i+2 MEAN:    {overall_idp_mean:.4f} Å                                        ║
  ║  DEVIATION:         {deviation_from_z:.4f} Å ({deviation_from_z/Z*100:.1f}%)                                 ║
  ║                                                                      ║
  ║  Z-RESONANCE IN IDPs:     {idp_z_rate*100:.0f}% ({len([r for r in idp_data if r.get('z_peak')])} of {len(idp_data)})                          ║
  ║  Z-RESONANCE IN ORDERED:  {ord_z_rate*100:.0f}% ({len([r for r in ord_data if r.get('z_peak')])} of {len(ord_data)})                          ║
  ║                                                                      ║
  ╠══════════════════════════════════════════════════════════════════════╣
    """)

    if deviation_from_z < 0.3 and idp_z_rate > 0.3:
        verdict = "Z IS A FUNDAMENTAL CONSTRAINT"
        explanation = """
  ║  The Z = 5.79 Å wavelength appears in DISORDERED proteins.           ║
  ║  This cannot be explained by folded structure optimization.          ║
  ║                                                                      ║
  ║  CONCLUSION:                                                         ║
  ║  Z is a PRE-FOLDING geometric constraint on the polypeptide chain.   ║
  ║  It defines the "default" backbone geometry before secondary         ║
  ║  structure imposes its own wavelength.                               ║
        """
    elif deviation_from_z < 0.5:
        verdict = "Z IS PARTIALLY FUNDAMENTAL"
        explanation = """
  ║  The Z wavelength is present but not dominant in IDPs.               ║
  ║  IDPs show broader distance distributions (higher variance).         ║
  ║                                                                      ║
  ║  CONCLUSION:                                                         ║
  ║  Z may represent the AVERAGE backbone state, with IDPs sampling      ║
  ║  around this geometric center due to thermal fluctuations.           ║
        """
    else:
        verdict = "Z IS AN EVOLVED PROPERTY"
        explanation = """
  ║  The Z wavelength is NOT strongly present in IDPs.                   ║
  ║  It appears primarily in FOLDED proteins with fixed structure.       ║
  ║                                                                      ║
  ║  CONCLUSION:                                                         ║
  ║  Z-resonance is an EVOLVED property optimized for structural         ║
  ║  stability in folded proteins, not a fundamental constraint.         ║
        """

    print(f"  ║  VERDICT: {verdict:<52s}   ║")
    print(explanation)
    print("  ╚══════════════════════════════════════════════════════════════════════╝")

    # Save results
    output = {
        'summary': {
            'idp_mean': float(np.mean(idp_means)) if idp_data else None,
            'idp_std': float(np.std(idp_means)) if idp_data else None,
            'idp_z_rate': idp_z_rate,
            'ordered_mean': float(np.mean(ord_means)) if ord_data else None,
            'ordered_z_rate': ord_z_rate,
            'target_Z': Z,
            'verdict': verdict
        },
        'idp_results': [{k: v for k, v in r.items() if k != 'histogram'} for r in idp_data],
        'ordered_results': [{k: v for k, v in r.items() if k != 'histogram'} for r in ord_data]
    }

    with open('idp_resonance_results.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print("\n  Results saved to: idp_resonance_results.json")

    return output


if __name__ == "__main__":
    results = run_idp_test()
