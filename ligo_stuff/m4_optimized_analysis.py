#!/usr/bin/env python3
"""
M4-Optimized LIGO Chirality Analysis
=====================================

Production-grade analysis pipeline optimized for Apple M4 Max:
- 16 cores (12 performance + 4 efficiency)
- 64GB unified memory
- Accelerate framework for BLAS/FFT

This script performs the full R-ratio chirality test on LIGO data.

Author: Carl Zimmerman
Date: May 2026
"""

import numpy as np
import h5py
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from scipy import signal
from scipy.interpolate import interp1d
import json
import os
import time
import warnings
warnings.filterwarnings('ignore')

# Force numpy to use all available threads
os.environ['OMP_NUM_THREADS'] = '16'
os.environ['VECLIB_MAXIMUM_THREADS'] = '16'

# =============================================================================
# CONFIGURATION
# =============================================================================

CONFIG = {
    'sample_rate': 4096,  # Hz
    'f_low': 20,          # Hz
    'f_high': 500,        # Hz - extended range
    'segment_duration': 60,  # seconds per FFT segment
    'overlap_fraction': 0.5,
    'n_workers': 12,      # Use performance cores
    'batch_size': 3600,   # 1 hour batches for memory efficiency
}

# Physical constants
c = 299792458.0
H0 = 67.4 * 1000 / 3.086e22

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def print_header(text):
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)

def print_status(text):
    print(f"  [{time.strftime('%H:%M:%S')}] {text}")

# =============================================================================
# DATA LOADING
# =============================================================================

def load_strain_data(detector, data_dir=OUTPUT_DIR):
    """Load strain data for a detector."""
    filepath = os.path.join(data_dir, f'{detector.lower()}_strain.hdf5')
    if not os.path.exists(filepath):
        return None
    with h5py.File(filepath, 'r') as f:
        strain = f['strain'][:]
    return strain.astype(np.float64)

def load_orf_data(baseline='H1-L1', data_dir=OUTPUT_DIR):
    """Load pre-computed ORF decomposition."""
    filepath = os.path.join(data_dir, 'multi_baseline_orf_results.json')
    with open(filepath, 'r') as f:
        data = json.load(f)

    bl_data = data['baselines'][baseline]
    freqs = np.array(bl_data['frequencies_hz'])
    gamma_total = np.array(bl_data['gamma_total'])
    gamma_pp = np.array(bl_data['gamma_pp'])

    return freqs, gamma_total, gamma_pp

# =============================================================================
# CORE ANALYSIS FUNCTIONS (Optimized for M4)
# =============================================================================

def compute_csd_batch(args):
    """
    Compute cross-spectral density for a batch of data.
    Designed for parallel execution.
    """
    h1_batch, l1_batch, fs, nperseg, noverlap = args

    freqs, Pxy = signal.csd(h1_batch, l1_batch, fs=fs,
                            nperseg=nperseg, noverlap=noverlap,
                            window='hann', detrend='linear')

    return freqs, Pxy

def compute_omega_estimators(freqs, Pxy, gamma_total_interp, gamma_pp_interp,
                              f_low=20, f_high=500):
    """
    Compute Omega estimators for standard and polarized searches.

    Vectorized for optimal M4 performance.
    """
    # Frequency mask
    mask = (freqs >= f_low) & (freqs <= f_high)
    freqs_band = freqs[mask]
    Pxy_band = Pxy[mask]

    if len(freqs_band) == 0:
        return None

    # ORF interpolation (vectorized)
    gamma_total_f = gamma_total_interp(freqs_band)
    gamma_pp_f = gamma_pp_interp(freqs_band)

    # Avoid division by zero
    gamma_total_f = np.where(np.abs(gamma_total_f) < 1e-10,
                              np.sign(gamma_total_f) * 1e-10, gamma_total_f)
    gamma_pp_f = np.where(np.abs(gamma_pp_f) < 1e-10,
                           np.sign(gamma_pp_f) * 1e-10, gamma_pp_f)

    # Conversion factor: strain^2/Hz -> Omega_GW
    # Omega = (10 pi^2 / 3 H0^2) * f^3 * S_h(f) / gamma(f)
    conversion = (10 * np.pi**2 / (3 * H0**2)) * freqs_band**3
    Re_Pxy = np.real(Pxy_band)

    # Point estimators per frequency bin
    Y_standard = conversion * Re_Pxy / gamma_total_f
    Y_polarized = conversion * Re_Pxy / gamma_pp_f

    # Optimal weighting: inverse variance
    # For simplicity, use uniform weighting here
    Omega_std = np.mean(Y_standard)
    Omega_pol = np.mean(Y_polarized)

    # Standard errors
    sigma_std = np.std(Y_standard) / np.sqrt(len(Y_standard))
    sigma_pol = np.std(Y_polarized) / np.sqrt(len(Y_polarized))

    return {
        'Omega_std': Omega_std,
        'Omega_pol': Omega_pol,
        'sigma_std': sigma_std,
        'sigma_pol': sigma_pol,
        'freqs': freqs_band,
        'Y_standard': Y_standard,
        'Y_polarized': Y_polarized
    }

def analyze_segment_parallel(args):
    """Worker function for parallel segment analysis."""
    (seg_idx, h1_seg, l1_seg, fs, nperseg, noverlap,
     gamma_total_interp, gamma_pp_interp, f_low, f_high) = args

    try:
        freqs, Pxy = signal.csd(h1_seg, l1_seg, fs=fs,
                                nperseg=nperseg, noverlap=noverlap,
                                window='hann', detrend='linear')

        result = compute_omega_estimators(freqs, Pxy, gamma_total_interp,
                                          gamma_pp_interp, f_low, f_high)
        if result is None:
            return None

        result['segment_idx'] = seg_idx
        return result
    except Exception as e:
        return {'error': str(e), 'segment_idx': seg_idx}

# =============================================================================
# MAIN ANALYSIS PIPELINE
# =============================================================================

class M4ChiralityAnalyzer:
    """
    M4-optimized chirality analyzer for LIGO data.
    """

    def __init__(self, config=CONFIG):
        self.config = config
        self.fs = config['sample_rate']
        self.f_low = config['f_low']
        self.f_high = config['f_high']
        self.segment_duration = config['segment_duration']
        self.n_workers = config['n_workers']

        # FFT parameters
        self.nperseg = int(self.segment_duration * self.fs)
        self.noverlap = int(self.nperseg * config['overlap_fraction'])

        # Load ORF data
        self.orf_freqs, self.gamma_total, self.gamma_pp = load_orf_data()
        self.gamma_total_interp = interp1d(self.orf_freqs, self.gamma_total,
                                            kind='linear', bounds_error=False,
                                            fill_value=0)
        self.gamma_pp_interp = interp1d(self.orf_freqs, self.gamma_pp,
                                         kind='linear', bounds_error=False,
                                         fill_value=0)

        self.R_expected = 3.11  # From ORF analysis

    def analyze_data(self, h1_strain, l1_strain, use_parallel=True):
        """
        Full analysis of strain data.

        Parameters
        ----------
        h1_strain : ndarray
            H1 detector strain data
        l1_strain : ndarray
            L1 detector strain data
        use_parallel : bool
            Use multiprocessing (recommended for large datasets)

        Returns
        -------
        dict : Analysis results
        """
        n_samples = min(len(h1_strain), len(l1_strain))
        duration = n_samples / self.fs

        print_status(f"Analyzing {duration:.1f} seconds ({duration/3600:.2f} hours)")
        print_status(f"Using {self.n_workers} worker processes")

        # Divide into segments
        segment_length = self.nperseg * 2  # Each segment = 2 FFT lengths
        n_segments = n_samples // segment_length

        print_status(f"Processing {n_segments} segments...")

        # Prepare segment data
        segments = []
        for i in range(n_segments):
            start = i * segment_length
            end = start + segment_length
            segments.append((
                i,
                h1_strain[start:end],
                l1_strain[start:end],
                self.fs,
                self.nperseg,
                self.noverlap,
                self.gamma_total_interp,
                self.gamma_pp_interp,
                self.f_low,
                self.f_high
            ))

        # Process segments
        start_time = time.time()

        if use_parallel and len(segments) > 4:
            # Parallel processing
            with ProcessPoolExecutor(max_workers=self.n_workers) as executor:
                results = list(executor.map(analyze_segment_parallel, segments))
        else:
            # Sequential processing
            results = [analyze_segment_parallel(seg) for seg in segments]

        elapsed = time.time() - start_time
        print_status(f"Processing complete in {elapsed:.2f}s ({n_segments/elapsed:.1f} seg/s)")

        # Filter valid results
        valid_results = [r for r in results if r is not None and 'error' not in r]

        if len(valid_results) == 0:
            return {'error': 'No valid segments'}

        # Aggregate results
        return self._aggregate_results(valid_results, duration)

    def _aggregate_results(self, results, duration):
        """Aggregate per-segment results into final estimates."""

        # Extract arrays
        Omega_std_arr = np.array([r['Omega_std'] for r in results])
        Omega_pol_arr = np.array([r['Omega_pol'] for r in results])
        sigma_std_arr = np.array([r['sigma_std'] for r in results])
        sigma_pol_arr = np.array([r['sigma_pol'] for r in results])

        # Weighted mean (inverse variance weighting)
        w_std = 1 / np.maximum(sigma_std_arr**2, 1e-30)
        w_pol = 1 / np.maximum(sigma_pol_arr**2, 1e-30)

        Omega_std = np.sum(w_std * Omega_std_arr) / np.sum(w_std)
        Omega_pol = np.sum(w_pol * Omega_pol_arr) / np.sum(w_pol)

        sigma_std = 1 / np.sqrt(np.sum(w_std))
        sigma_pol = 1 / np.sqrt(np.sum(w_pol))

        # R-ratio
        if Omega_std != 0:
            R = Omega_pol / Omega_std
            rel_err_std = sigma_std / abs(Omega_std) if Omega_std != 0 else np.inf
            rel_err_pol = sigma_pol / abs(Omega_pol) if Omega_pol != 0 else np.inf
            sigma_R = abs(R) * np.sqrt(rel_err_std**2 + rel_err_pol**2)
        else:
            R = np.nan
            sigma_R = np.nan

        # Statistical tests
        # Is R consistent with 1.0 (unpolarized)?
        n_sigma_from_1 = abs(R - 1.0) / sigma_R if sigma_R > 0 else 0
        # Is R consistent with 3.11 (h+ only)?
        n_sigma_from_chiral = abs(R - self.R_expected) / sigma_R if sigma_R > 0 else 0

        # Chi-squared test for segment consistency
        R_per_segment = Omega_pol_arr / np.where(Omega_std_arr != 0, Omega_std_arr, 1e-30)
        chi2 = np.sum(((R_per_segment - R) / sigma_R)**2) if sigma_R > 0 else 0
        ndof = len(results) - 1

        return {
            'duration_seconds': duration,
            'n_segments': len(results),

            'Omega_std': float(Omega_std),
            'Omega_pol': float(Omega_pol),
            'sigma_std': float(sigma_std),
            'sigma_pol': float(sigma_pol),

            'R': float(R),
            'sigma_R': float(sigma_R),

            'n_sigma_from_unpolarized': float(n_sigma_from_1),
            'n_sigma_from_chiral': float(n_sigma_from_chiral),

            'chi2': float(chi2),
            'ndof': int(ndof),
            'chi2_per_dof': float(chi2/ndof) if ndof > 0 else 0,

            'segment_Omega_std': Omega_std_arr.tolist(),
            'segment_Omega_pol': Omega_pol_arr.tolist(),
            'segment_R': R_per_segment.tolist(),
        }

# =============================================================================
# FREQUENCY-RESOLVED ANALYSIS
# =============================================================================

def compute_R_vs_frequency(h1_strain, l1_strain, fs, gamma_total_interp,
                           gamma_pp_interp, f_low=20, f_high=500,
                           n_freq_bins=50):
    """
    Compute R(f) as a function of frequency.
    """
    nperseg = int(60 * fs)
    noverlap = nperseg // 2

    freqs, Pxy = signal.csd(h1_strain, l1_strain, fs=fs,
                            nperseg=nperseg, noverlap=noverlap,
                            window='hann', detrend='linear')

    # Bin frequencies
    freq_mask = (freqs >= f_low) & (freqs <= f_high)
    freqs_band = freqs[freq_mask]
    Pxy_band = Pxy[freq_mask]

    # Create frequency bins
    freq_edges = np.linspace(f_low, f_high, n_freq_bins + 1)
    freq_centers = (freq_edges[:-1] + freq_edges[1:]) / 2

    R_f = []
    sigma_R_f = []

    for i in range(n_freq_bins):
        bin_mask = (freqs_band >= freq_edges[i]) & (freqs_band < freq_edges[i+1])
        if np.sum(bin_mask) < 3:
            R_f.append(np.nan)
            sigma_R_f.append(np.nan)
            continue

        f_bin = freqs_band[bin_mask]
        Pxy_bin = Pxy_band[bin_mask]

        gamma_total_f = gamma_total_interp(f_bin)
        gamma_pp_f = gamma_pp_interp(f_bin)

        gamma_total_f = np.where(np.abs(gamma_total_f) < 1e-10, 1e-10, gamma_total_f)
        gamma_pp_f = np.where(np.abs(gamma_pp_f) < 1e-10, 1e-10, gamma_pp_f)

        conversion = (10 * np.pi**2 / (3 * H0**2)) * f_bin**3
        Re_Pxy = np.real(Pxy_bin)

        Y_std = conversion * Re_Pxy / gamma_total_f
        Y_pol = conversion * Re_Pxy / gamma_pp_f

        Omega_std = np.mean(Y_std)
        Omega_pol = np.mean(Y_pol)

        if Omega_std != 0:
            R = Omega_pol / Omega_std
            sigma = abs(R) * np.sqrt(2) / np.sqrt(len(Y_std))  # Simplified error
        else:
            R = np.nan
            sigma = np.nan

        R_f.append(R)
        sigma_R_f.append(sigma)

    return freq_centers, np.array(R_f), np.array(sigma_R_f)

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    print_header("M4-OPTIMIZED LIGO CHIRALITY ANALYSIS")

    # System info
    print_status(f"CPU cores available: {mp.cpu_count()}")
    print_status(f"Using {CONFIG['n_workers']} workers")

    # Load data
    print_header("LOADING DATA")

    h1_strain = load_strain_data('h1')
    l1_strain = load_strain_data('l1')

    if h1_strain is None or l1_strain is None:
        print("Error: Could not load strain data")
        exit(1)

    n_samples = min(len(h1_strain), len(l1_strain))
    h1_strain = h1_strain[:n_samples]
    l1_strain = l1_strain[:n_samples]
    duration = n_samples / CONFIG['sample_rate']

    print_status(f"H1: {len(h1_strain):,} samples")
    print_status(f"L1: {len(l1_strain):,} samples")
    print_status(f"Duration: {duration:.1f}s ({duration/3600:.2f} hours)")
    print_status(f"Memory: {(h1_strain.nbytes + l1_strain.nbytes) / 1e9:.2f} GB")

    # Initialize analyzer
    print_header("ANALYSIS")
    analyzer = M4ChiralityAnalyzer(CONFIG)

    # Run analysis
    results = analyzer.analyze_data(h1_strain, l1_strain, use_parallel=True)

    # Print results
    print_header("RESULTS")

    print(f"""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                         R-RATIO CHIRALITY TEST                               ║
    ╠══════════════════════════════════════════════════════════════════════════════╣
    ║                                                                              ║
    ║  DATA:                                                                       ║
    ║    Duration: {results['duration_seconds']/3600:.2f} hours                                               ║
    ║    Segments: {results['n_segments']}                                                         ║
    ║                                                                              ║
    ║  OMEGA ESTIMATES:                                                            ║
    ║    Ω_standard  = {results['Omega_std']:+.3e} ± {results['sigma_std']:.3e}                       ║
    ║    Ω_polarized = {results['Omega_pol']:+.3e} ± {results['sigma_pol']:.3e}                       ║
    ║                                                                              ║
    ║  R-RATIO:                                                                    ║
    ║    R = {results['R']:+.3f} ± {results['sigma_R']:.3f}                                                ║
    ║                                                                              ║
    ║  HYPOTHESIS TESTS:                                                           ║
    ║    Distance from R=1.0 (unpolarized):  {results['n_sigma_from_unpolarized']:.2f}σ                              ║
    ║    Distance from R=3.11 (h+ only):     {results['n_sigma_from_chiral']:.2f}σ                              ║
    ║                                                                              ║
    ║  CONSISTENCY:                                                                ║
    ║    χ²/ndof = {results['chi2_per_dof']:.2f}                                                      ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """)

    # Interpretation
    if results['sigma_R'] > 0:
        if results['n_sigma_from_unpolarized'] < 2:
            interpretation = "CONSISTENT WITH UNPOLARIZED (R ≈ 1)"
        elif results['n_sigma_from_chiral'] < 2:
            interpretation = "CONSISTENT WITH CHIRAL (R ≈ 3.11)"
        else:
            interpretation = "NOISE-DOMINATED / INCONCLUSIVE"
    else:
        interpretation = "INSUFFICIENT DATA"

    print(f"  INTERPRETATION: {interpretation}")

    # Frequency-resolved analysis
    print_header("FREQUENCY-RESOLVED R(f)")

    orf_freqs, gamma_total, gamma_pp = load_orf_data()
    gamma_total_interp = interp1d(orf_freqs, gamma_total, kind='linear',
                                   bounds_error=False, fill_value=0)
    gamma_pp_interp = interp1d(orf_freqs, gamma_pp, kind='linear',
                                bounds_error=False, fill_value=0)

    freq_centers, R_f, sigma_R_f = compute_R_vs_frequency(
        h1_strain, l1_strain, CONFIG['sample_rate'],
        gamma_total_interp, gamma_pp_interp,
        f_low=20, f_high=200, n_freq_bins=30
    )

    # Generate figure
    print_header("GENERATING FIGURES")

    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.25)

    # Panel A: R(f) vs frequency
    ax1 = fig.add_subplot(gs[0, 0])
    valid = ~np.isnan(R_f)
    ax1.errorbar(freq_centers[valid], R_f[valid], yerr=sigma_R_f[valid],
                 fmt='o-', color='blue', markersize=5, capsize=3, linewidth=1.5)
    ax1.axhline(1.0, color='green', linestyle='--', linewidth=2, label='R=1 (unpolarized)')
    ax1.axhline(3.11, color='red', linestyle='--', linewidth=2, label='R=3.11 (h+ only)')
    ax1.set_xlabel('Frequency (Hz)', fontsize=12)
    ax1.set_ylabel('R(f)', fontsize=12)
    ax1.set_title('A: R-ratio vs Frequency', fontsize=13, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(20, 200)

    # Panel B: Per-segment R distribution
    ax2 = fig.add_subplot(gs[0, 1])
    segment_R = np.array(results['segment_R'])
    valid_seg = np.isfinite(segment_R) & (np.abs(segment_R) < 100)
    ax2.hist(segment_R[valid_seg], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
    ax2.axvline(results['R'], color='red', linestyle='-', linewidth=2, label=f"Mean R = {results['R']:.2f}")
    ax2.axvline(1.0, color='green', linestyle='--', linewidth=2, label='R=1')
    ax2.axvline(3.11, color='orange', linestyle='--', linewidth=2, label='R=3.11')
    ax2.set_xlabel('R per segment', fontsize=12)
    ax2.set_ylabel('Count', fontsize=12)
    ax2.set_title('B: Distribution of Segment R-values', fontsize=13, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Panel C: Omega estimates per segment
    ax3 = fig.add_subplot(gs[1, 0])
    seg_idx = np.arange(len(results['segment_Omega_std']))
    ax3.plot(seg_idx, results['segment_Omega_std'], 'b-', alpha=0.7, label='Ω_standard')
    ax3.plot(seg_idx, results['segment_Omega_pol'], 'r-', alpha=0.7, label='Ω_polarized')
    ax3.axhline(0, color='black', linestyle='-', linewidth=0.5)
    ax3.set_xlabel('Segment index', fontsize=12)
    ax3.set_ylabel('Ω estimate', fontsize=12)
    ax3.set_title('C: Ω Estimates per Segment', fontsize=13, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Panel D: Summary
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')

    summary_text = f"""
╔═══════════════════════════════════════════════════════════════════╗
║           M4-OPTIMIZED CHIRALITY ANALYSIS SUMMARY                 ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  CONFIGURATION:                                                   ║
║    Workers: {CONFIG['n_workers']} cores                                           ║
║    Frequency band: {CONFIG['f_low']}-{CONFIG['f_high']} Hz                                   ║
║    Segment duration: {CONFIG['segment_duration']}s                                      ║
║                                                                   ║
║  RESULT:                                                          ║
║    R = {results['R']:+.3f} ± {results['sigma_R']:.3f}                                         ║
║                                                                   ║
║  STATISTICAL SIGNIFICANCE:                                        ║
║    {results['n_sigma_from_unpolarized']:.1f}σ from unpolarized (R=1)                               ║
║    {results['n_sigma_from_chiral']:.1f}σ from chiral (R=3.11)                                 ║
║                                                                   ║
║  INTERPRETATION:                                                  ║
║    {interpretation:55s}     ║
║                                                                   ║
║  NOTE: Current data is noise-dominated (no SGWB signal).          ║
║  This analysis validates the pipeline for future detections.      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
    ax4.text(0.02, 0.98, summary_text, transform=ax4.transAxes, fontsize=10,
             fontfamily='monospace', verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    fig.suptitle('M4-Optimized LIGO Chirality Analysis', fontsize=15, fontweight='bold', y=0.98)

    plt.savefig(os.path.join(OUTPUT_DIR, 'm4_analysis_results.png'),
                dpi=200, bbox_inches='tight', facecolor='white')
    print_status("Saved: m4_analysis_results.png")

    # Save results
    output = {
        'analysis': 'm4_optimized_chirality_analysis',
        'config': CONFIG,
        'results': {k: v for k, v in results.items()
                   if not isinstance(v, list) or len(v) < 100},
        'interpretation': interpretation
    }

    with open(os.path.join(OUTPUT_DIR, 'm4_analysis_results.json'), 'w') as f:
        json.dump(output, f, indent=2)
    print_status("Saved: m4_analysis_results.json")

    print_header("ANALYSIS COMPLETE")
