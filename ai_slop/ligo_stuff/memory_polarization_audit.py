#!/usr/bin/env python3
"""
Gravitational Memory Polarization Audit
========================================

The gravitational wave "memory effect" is a permanent displacement of spacetime
after a compact binary merger. Unlike the oscillatory GW signal, memory is a
DC offset that persists forever.

Standard GR Prediction:
- Memory has both h₊ and h× components
- h× memory is strongest for edge-on (high inclination) binaries
- Total memory amplitude: Δh ∝ (η M / D) × (v_final/c)²

Z² Framework Prediction:
- The T³/Z₂ orbifold projection should suppress h× modes
- Memory should be purely h₊, regardless of binary inclination
- Edge-on binaries should show "missing" h× memory

Analysis Strategy:
1. Stack post-merger strain from many BBH events
2. Extract the low-frequency "memory plateau"
3. Decompose into h₊ and h× using antenna patterns
4. Compare observed h×/h₊ ratio against GR prediction

Author: Carl Zimmerman
Date: May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, optimize
from scipy.interpolate import interp1d
import h5py
import json
import os
import time
import warnings
warnings.filterwarnings('ignore')

try:
    from gwpy.timeseries import TimeSeries
    HAS_GWPY = True
except ImportError:
    HAS_GWPY = False

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Physical constants
c = 299792458.0  # m/s
G = 6.674e-11    # m³/kg/s²
M_sun = 1.989e30  # kg
Mpc = 3.086e22   # m

# Analysis parameters
CONFIG = {
    'sample_rate': 4096,
    'memory_window': 0.5,     # seconds after merger to look for memory
    'highpass_freq': 10,      # Hz - memory is low frequency
    'lowpass_freq': 30,       # Hz - avoid ringdown oscillations
}

# GWTC events with good SNR for memory search
# Using actual events from GWTC-3 catalog
GWTC_EVENTS = [
    {'name': 'GW150914', 'gps': 1126259462.4, 'm1': 35.6, 'm2': 30.6, 'D': 410, 'iota': 2.74, 'snr': 24.4},
    {'name': 'GW170104', 'gps': 1167559936.6, 'm1': 31.0, 'm2': 20.1, 'D': 990, 'iota': 2.5, 'snr': 13.0},
    {'name': 'GW170814', 'gps': 1186741861.5, 'm1': 30.7, 'm2': 25.3, 'D': 580, 'iota': 1.4, 'snr': 15.9},
    {'name': 'GW170818', 'gps': 1187058327.1, 'm1': 35.5, 'm2': 26.8, 'D': 1060, 'iota': 2.3, 'snr': 11.3},
    {'name': 'GW190412', 'gps': 1239082262.2, 'm1': 30.1, 'm2': 8.3, 'D': 740, 'iota': 0.8, 'snr': 19.1},
    {'name': 'GW190521', 'gps': 1242442967.4, 'm1': 85.0, 'm2': 66.0, 'D': 5300, 'iota': 1.1, 'snr': 14.7},
    {'name': 'GW190814', 'gps': 1249852257.0, 'm1': 23.2, 'm2': 2.6, 'D': 241, 'iota': 0.9, 'snr': 25.0},
    {'name': 'GW191109', 'gps': 1257296855.2, 'm1': 65.0, 'm2': 47.0, 'D': 2900, 'iota': 1.8, 'snr': 12.1},
]

def print_header(text):
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)

def print_status(text):
    print(f"  [{time.strftime('%H:%M:%S')}] {text}")


# =============================================================================
# MEMORY THEORY
# =============================================================================

def compute_memory_amplitude(m1, m2, D_Mpc, inclination):
    """
    Compute theoretical memory amplitude for a BBH merger.

    The memory effect has both h₊ and h× components that depend on inclination.

    h₊_memory ∝ (1 + cos²ι) × η × (M/D) × (v_final/c)²
    h×_memory ∝ 2 cos(ι) × η × (M/D) × (v_final/c)²

    Returns (h_plus_memory, h_cross_memory) in strain units.
    """
    # Masses in kg
    M1 = m1 * M_sun
    M2 = m2 * M_sun
    M_total = M1 + M2

    # Symmetric mass ratio
    eta = (M1 * M2) / M_total**2

    # Distance in meters
    D = D_Mpc * Mpc

    # Final velocity (approximate - at ISCO)
    v_final = 0.4 * c  # ~0.4c at merger

    # Inclination factors
    cos_iota = np.cos(inclination)
    iota_plus = (1 + cos_iota**2) / 2  # h₊ factor
    iota_cross = cos_iota                # h× factor

    # Memory amplitude (order of magnitude)
    # Δh ~ (G M η / (c² D)) × (v/c)²
    h_char = (G * M_total * eta / (c**2 * D)) * (v_final / c)**2

    h_plus_memory = h_char * iota_plus * 0.5  # Factor of 0.5 from detailed calculation
    h_cross_memory = h_char * iota_cross * 0.3  # h× is typically smaller

    return h_plus_memory, h_cross_memory


def gr_memory_ratio(inclination):
    """
    Compute the GR prediction for h×/h₊ memory ratio.

    This ratio depends on inclination:
    - Face-on (ι = 0): h× = 0, ratio = 0
    - Edge-on (ι = π/2): h× maximal, ratio ~ 0.6
    """
    cos_iota = np.cos(inclination)
    iota_plus = (1 + cos_iota**2) / 2
    iota_cross = cos_iota

    if iota_plus == 0:
        return np.inf

    # GR prediction for memory ratio
    ratio = abs(iota_cross / iota_plus) * 0.6  # Factor from numerical relativity

    return ratio


# =============================================================================
# ANTENNA PATTERNS
# =============================================================================

def antenna_patterns(ra, dec, psi, gps_time, detector):
    """
    Compute antenna pattern functions F₊ and F× for a detector.

    Simplified calculation using detector orientation.
    """
    if detector == 'H1':
        arm_azimuth = np.radians(171.8)
        lat = np.radians(46.45)
        lon = np.radians(-119.41)
    elif detector == 'L1':
        arm_azimuth = np.radians(243.0)
        lat = np.radians(30.56)
        lon = np.radians(-90.77)
    else:
        return 0.5, 0.5  # Default

    # Source position in detector frame (simplified)
    theta = np.pi/2 - dec
    phi = ra

    # Antenna patterns (approximate)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    F_plus = 0.5 * (1 + cos_theta**2) * np.cos(2*phi) * np.cos(2*psi) - \
             cos_theta * np.sin(2*phi) * np.sin(2*psi)

    F_cross = 0.5 * (1 + cos_theta**2) * np.cos(2*phi) * np.sin(2*psi) + \
              cos_theta * np.sin(2*phi) * np.cos(2*psi)

    return F_plus, F_cross


# =============================================================================
# MEMORY EXTRACTION
# =============================================================================

def extract_memory_signal(strain, merger_time, sample_rate, config):
    """
    Extract the memory plateau from post-merger strain.

    Memory appears as a low-frequency step function after the merger.
    """
    # Time array
    n_samples = len(strain)
    t = np.arange(n_samples) / sample_rate

    # Find merger sample
    merger_sample = int(merger_time * sample_rate)
    if merger_sample < 0 or merger_sample >= n_samples:
        merger_sample = n_samples // 2

    # Post-merger window
    window_samples = int(config['memory_window'] * sample_rate)
    start = merger_sample
    end = min(merger_sample + window_samples, n_samples)

    # Pre-merger baseline
    baseline_start = max(0, merger_sample - window_samples)
    baseline_end = merger_sample

    # Extract segments
    pre_merger = strain[baseline_start:baseline_end]
    post_merger = strain[start:end]

    # Bandpass filter to isolate memory frequency band
    nyq = sample_rate / 2
    low = config['highpass_freq'] / nyq
    high = config['lowpass_freq'] / nyq

    if high < 1 and low > 0:
        b, a = signal.butter(4, [low, high], btype='band')
        pre_filtered = signal.filtfilt(b, a, pre_merger)
        post_filtered = signal.filtfilt(b, a, post_merger)
    else:
        pre_filtered = pre_merger
        post_filtered = post_merger

    # Memory is the DC offset (mean difference)
    pre_mean = np.mean(pre_filtered)
    post_mean = np.mean(post_filtered)

    memory_amplitude = post_mean - pre_mean
    memory_std = np.sqrt(np.var(pre_filtered) + np.var(post_filtered)) / np.sqrt(len(post_filtered))

    return {
        'memory': memory_amplitude,
        'uncertainty': memory_std,
        'pre_mean': pre_mean,
        'post_mean': post_mean,
        'snr': abs(memory_amplitude) / memory_std if memory_std > 0 else 0,
    }


def decompose_polarizations(h1_memory, l1_memory, F1p, F1c, F2p, F2c):
    """
    Decompose observed memory into h₊ and h× components.

    h_H1 = F₁₊ h₊ + F₁× h×
    h_L1 = F₂₊ h₊ + F₂× h×

    Solve the 2×2 system to get h₊ and h×.
    """
    # Matrix form: [h_H1, h_L1]ᵀ = [[F1p, F1c], [F2p, F2c]] × [h₊, h×]ᵀ
    A = np.array([[F1p, F1c], [F2p, F2c]])
    b = np.array([h1_memory, l1_memory])

    # Check if system is solvable
    det = np.linalg.det(A)
    if abs(det) < 1e-10:
        return None, None, "Singular matrix - degenerate antenna patterns"

    # Solve
    try:
        x = np.linalg.solve(A, b)
        h_plus = x[0]
        h_cross = x[1]
        return h_plus, h_cross, "OK"
    except np.linalg.LinAlgError:
        return None, None, "Linear algebra error"


# =============================================================================
# STACKING ANALYSIS
# =============================================================================

def simulate_event_memory(event, config):
    """
    Simulate memory measurement for an event.

    In a real analysis, we would download strain data. Here we simulate
    based on theoretical predictions with realistic noise.
    """
    # Theoretical memory
    h_plus_theory, h_cross_theory = compute_memory_amplitude(
        event['m1'], event['m2'], event['D'], event['iota']
    )

    # Add noise based on SNR
    # Memory SNR is much lower than signal SNR (factor ~0.01)
    memory_snr_factor = 0.01
    effective_snr = event['snr'] * memory_snr_factor

    noise_level = max(h_plus_theory, 1e-24) / effective_snr

    h_plus_observed = h_plus_theory + np.random.normal(0, noise_level)
    h_cross_observed = h_cross_theory + np.random.normal(0, noise_level)

    # For Z² test: what if h× is suppressed?
    # We'll compute both GR prediction and Z² prediction
    h_cross_z2 = 0.0  # Z² predicts no h× memory

    return {
        'h_plus_theory': h_plus_theory,
        'h_cross_theory': h_cross_theory,
        'h_plus_observed': h_plus_observed,
        'h_cross_observed': h_cross_observed,
        'h_cross_z2': h_cross_z2,
        'noise_level': noise_level,
        'iota': event['iota'],
        'gr_ratio': gr_memory_ratio(event['iota']),
    }


def coherent_stack_memory(events, config):
    """
    Coherently stack memory signals from multiple events.

    Weights by (theoretical amplitude)² × SNR² to optimize stacking.
    """
    print_status(f"Stacking memory from {len(events)} events...")

    # Collect measurements
    h_plus_stack = []
    h_cross_stack = []
    weights = []
    gr_ratios = []

    for event in events:
        result = simulate_event_memory(event, config)

        # Weight by inverse variance
        if result['noise_level'] > 0:
            weight = 1.0 / result['noise_level']**2
        else:
            weight = 1.0

        h_plus_stack.append(result['h_plus_observed'] * weight)
        h_cross_stack.append(result['h_cross_observed'] * weight)
        weights.append(weight)
        gr_ratios.append(result['gr_ratio'])

        print(f"    {event['name']}: h₊={result['h_plus_theory']:.2e}, "
              f"h×={result['h_cross_theory']:.2e}, ι={np.degrees(event['iota']):.0f}°")

    # Weighted average
    total_weight = sum(weights)
    h_plus_stacked = sum(h_plus_stack) / total_weight
    h_cross_stacked = sum(h_cross_stack) / total_weight

    # Uncertainty (inverse sqrt of total weight)
    sigma_plus = 1.0 / np.sqrt(total_weight)
    sigma_cross = 1.0 / np.sqrt(total_weight)

    # Observed ratio
    if abs(h_plus_stacked) > 1e-30:
        observed_ratio = abs(h_cross_stacked / h_plus_stacked)
        ratio_uncertainty = observed_ratio * np.sqrt(
            (sigma_plus/abs(h_plus_stacked))**2 + (sigma_cross/abs(h_cross_stacked + 1e-30))**2
        )
    else:
        observed_ratio = 0
        ratio_uncertainty = 0

    # Expected GR ratio (weighted average)
    expected_gr_ratio = np.average(gr_ratios, weights=weights)

    return {
        'h_plus_stacked': h_plus_stacked,
        'h_cross_stacked': h_cross_stacked,
        'sigma_plus': sigma_plus,
        'sigma_cross': sigma_cross,
        'observed_ratio': observed_ratio,
        'ratio_uncertainty': ratio_uncertainty,
        'expected_gr_ratio': expected_gr_ratio,
        'n_events': len(events),
        'total_weight': total_weight,
    }


# =============================================================================
# STATISTICAL TESTS
# =============================================================================

def test_z2_hypothesis(stacked_result):
    """
    Test the Z² hypothesis that h× memory is suppressed.

    H0 (GR): h×/h₊ = expected_gr_ratio
    H1 (Z²): h×/h₊ = 0

    Returns significance of deviation from each hypothesis.
    """
    observed = stacked_result['observed_ratio']
    sigma = stacked_result['ratio_uncertainty']
    gr_prediction = stacked_result['expected_gr_ratio']

    if sigma == 0:
        sigma = 0.1  # Avoid division by zero

    # Deviation from GR
    z_from_gr = (observed - gr_prediction) / sigma

    # Deviation from Z² (h× = 0)
    z_from_z2 = observed / sigma

    # Which model is favored?
    chi2_gr = z_from_gr**2
    chi2_z2 = z_from_z2**2

    # Delta chi²
    delta_chi2 = chi2_gr - chi2_z2  # Positive favors Z², negative favors GR

    return {
        'observed_ratio': observed,
        'gr_prediction': gr_prediction,
        'z2_prediction': 0.0,
        'sigma': sigma,
        'z_from_gr': z_from_gr,
        'z_from_z2': z_from_z2,
        'chi2_gr': chi2_gr,
        'chi2_z2': chi2_z2,
        'delta_chi2': delta_chi2,
        'favored_model': 'Z²' if delta_chi2 > 0 else 'GR',
    }


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_memory_analysis():
    print_header("GRAVITATIONAL MEMORY POLARIZATION AUDIT")
    print_status("Testing if h× memory is suppressed (Z² prediction)")

    # Theoretical overview
    print_header("THEORETICAL PREDICTIONS")

    print_status("Memory effect physics:")
    print("    • GR: Both h₊ and h× memory components exist")
    print("    • h× memory strongest for edge-on binaries (high ι)")
    print("    • Z² predicts: h× memory = 0 (topological suppression)")
    print()

    # Compute theoretical memory for each event
    print_header("EVENT ANALYSIS")

    for event in GWTC_EVENTS:
        h_plus, h_cross = compute_memory_amplitude(
            event['m1'], event['m2'], event['D'], event['iota']
        )
        ratio = gr_memory_ratio(event['iota'])
        print_status(f"{event['name']}: h₊={h_plus:.2e}, h×={h_cross:.2e}, "
                     f"h×/h₊={ratio:.2f}, ι={np.degrees(event['iota']):.0f}°")

    # Stack events
    print_header("COHERENT STACKING")

    stacked = coherent_stack_memory(GWTC_EVENTS, CONFIG)

    print_status(f"\nStacked results ({stacked['n_events']} events):")
    print_status(f"  h₊ (stacked) = {stacked['h_plus_stacked']:.3e} ± {stacked['sigma_plus']:.3e}")
    print_status(f"  h× (stacked) = {stacked['h_cross_stacked']:.3e} ± {stacked['sigma_cross']:.3e}")
    print_status(f"  Observed h×/h₊ = {stacked['observed_ratio']:.3f} ± {stacked['ratio_uncertainty']:.3f}")
    print_status(f"  Expected (GR) h×/h₊ = {stacked['expected_gr_ratio']:.3f}")

    # Hypothesis test
    print_header("HYPOTHESIS TEST")

    test = test_z2_hypothesis(stacked)

    print_status(f"Testing Z² vs GR:")
    print_status(f"  GR prediction:  h×/h₊ = {test['gr_prediction']:.3f}")
    print_status(f"  Z² prediction:  h×/h₊ = 0.000")
    print_status(f"  Observed:       h×/h₊ = {test['observed_ratio']:.3f} ± {test['sigma']:.3f}")
    print_status(f"")
    print_status(f"  Deviation from GR: {test['z_from_gr']:+.2f}σ")
    print_status(f"  Deviation from Z²: {test['z_from_z2']:+.2f}σ")
    print_status(f"  Δχ² (GR - Z²): {test['delta_chi2']:+.2f}")
    print_status(f"  Favored model: {test['favored_model']}")

    # Summary
    print_header("MEMORY POLARIZATION AUDIT SUMMARY")

    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    GRAVITATIONAL MEMORY POLARIZATION TEST                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PHYSICS:                                                                    ║
║    Memory = permanent spacetime displacement after merger                    ║
║    GR predicts both h₊ and h× memory components                              ║
║    Z² predicts h× memory is topologically forbidden                          ║
║                                                                              ║
║  STACKED RESULTS ({stacked['n_events']} BBH events):                                         ║
║    h₊ memory: {stacked['h_plus_stacked']:+.3e} ± {stacked['sigma_plus']:.3e}                            ║
║    h× memory: {stacked['h_cross_stacked']:+.3e} ± {stacked['sigma_cross']:.3e}                            ║
║                                                                              ║
║  POLARIZATION RATIO:                                                         ║
║    Observed:   h×/h₊ = {test['observed_ratio']:.3f} ± {test['sigma']:.3f}                                ║
║    GR expects: h×/h₊ = {test['gr_prediction']:.3f}                                           ║
║    Z² expects: h×/h₊ = 0.000                                                 ║
║                                                                              ║
║  STATISTICAL TEST:                                                           ║
║    Deviation from GR: {test['z_from_gr']:+5.2f}σ                                            ║
║    Deviation from Z²: {test['z_from_z2']:+5.2f}σ                                            ║
║    Δχ² (GR - Z²):     {test['delta_chi2']:+5.2f}                                             ║
║                                                                              ║
║  VERDICT: {test['favored_model']:^8} MODEL PREFERRED                                        ║
║                                                                              ║
║  INTERPRETATION:                                                             ║
║    • Δχ² > 0: Evidence for h× suppression (favors Z²)                        ║
║    • Δχ² < 0: h× memory present as expected (favors GR)                      ║
║    • |Δχ²| > 4: Strong preference (~2σ per parameter)                        ║
║                                                                              ║
║  NOTE: This analysis uses simulated measurements. Real analysis requires     ║
║        strain data download and careful systematic control.                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    # Save results
    output = {
        'analysis': 'memory_polarization_audit',
        'date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'events': [e['name'] for e in GWTC_EVENTS],
        'n_events': len(GWTC_EVENTS),
        'stacked_results': {
            'h_plus': float(stacked['h_plus_stacked']),
            'h_cross': float(stacked['h_cross_stacked']),
            'sigma_plus': float(stacked['sigma_plus']),
            'sigma_cross': float(stacked['sigma_cross']),
            'observed_ratio': float(stacked['observed_ratio']),
            'ratio_uncertainty': float(stacked['ratio_uncertainty']),
            'expected_gr_ratio': float(stacked['expected_gr_ratio']),
        },
        'hypothesis_test': {
            'z_from_gr': float(test['z_from_gr']),
            'z_from_z2': float(test['z_from_z2']),
            'delta_chi2': float(test['delta_chi2']),
            'favored_model': test['favored_model'],
        },
        'config': CONFIG,
    }

    with open(os.path.join(OUTPUT_DIR, 'memory_polarization_results.json'), 'w') as f:
        json.dump(output, f, indent=2)

    print_status("Saved: memory_polarization_results.json")

    # Create visualization
    create_memory_plot(GWTC_EVENTS, stacked, test)

    return output


def create_memory_plot(events, stacked, test):
    """Create visualization of memory analysis."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Memory amplitude vs inclination
    ax = axes[0, 0]
    iotas = [e['iota'] for e in events]
    h_plus = [compute_memory_amplitude(e['m1'], e['m2'], e['D'], e['iota'])[0] for e in events]
    h_cross = [compute_memory_amplitude(e['m1'], e['m2'], e['D'], e['iota'])[1] for e in events]

    ax.scatter(np.degrees(iotas), np.abs(h_plus), s=100, c='blue', label='h₊ memory', alpha=0.7)
    ax.scatter(np.degrees(iotas), np.abs(h_cross), s=100, c='red', label='h× memory', alpha=0.7)

    # Theoretical curve
    iota_theory = np.linspace(0, np.pi, 100)
    h_plus_theory = [(1 + np.cos(i)**2)/2 for i in iota_theory]
    h_cross_theory = [abs(np.cos(i)) for i in iota_theory]

    ax.plot(np.degrees(iota_theory), h_plus_theory, 'b--', label='h₊ (theory)', alpha=0.5)
    ax.plot(np.degrees(iota_theory), h_cross_theory, 'r--', label='h× (theory)', alpha=0.5)
    ax.axhline(y=0, color='green', linestyle=':', label='Z² prediction for h×')

    ax.set_xlabel('Inclination ι [degrees]')
    ax.set_ylabel('Memory amplitude (normalized)')
    ax.set_title('Memory vs Inclination')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 2: h×/h₊ ratio vs inclination
    ax = axes[0, 1]
    ratios = [gr_memory_ratio(e['iota']) for e in events]
    names = [e['name'] for e in events]

    ax.bar(range(len(events)), ratios, color='purple', alpha=0.7)
    ax.axhline(y=stacked['expected_gr_ratio'], color='red', linestyle='--',
               label=f'Weighted mean (GR) = {stacked["expected_gr_ratio"]:.2f}')
    ax.axhline(y=stacked['observed_ratio'], color='green', linestyle='-',
               label=f'Observed = {stacked["observed_ratio"]:.2f}')
    ax.axhline(y=0, color='blue', linestyle=':', label='Z² prediction = 0')

    ax.set_xlabel('Event')
    ax.set_ylabel('h×/h₊ ratio')
    ax.set_title('Memory Polarization Ratio by Event')
    ax.set_xticks(range(len(events)))
    ax.set_xticklabels([e['name'][-4:] for e in events], rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    # Plot 3: Stacked result comparison
    ax = axes[1, 0]
    models = ['GR\nPrediction', 'Observed', 'Z²\nPrediction']
    values = [stacked['expected_gr_ratio'], stacked['observed_ratio'], 0]
    errors = [0, stacked['ratio_uncertainty'], 0]
    colors = ['red', 'purple', 'green']

    bars = ax.bar(models, values, yerr=errors, color=colors, alpha=0.7, capsize=10)
    ax.set_ylabel('h×/h₊ ratio')
    ax.set_title('Model Comparison: Memory Polarization Ratio')
    ax.grid(True, alpha=0.3, axis='y')

    # Plot 4: Chi-squared comparison
    ax = axes[1, 1]
    chi2_values = [test['chi2_gr'], test['chi2_z2']]
    model_names = ['GR Model', 'Z² Model']
    colors = ['red' if test['favored_model'] == 'Z²' else 'green',
              'green' if test['favored_model'] == 'Z²' else 'red']

    ax.bar(model_names, chi2_values, color=colors, alpha=0.7)
    ax.axhline(y=min(chi2_values), color='blue', linestyle='--', label='Best fit')

    ax.set_ylabel('χ²')
    ax.set_title(f'Goodness of Fit (Favored: {test["favored_model"]})')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    for i, v in enumerate(chi2_values):
        ax.text(i, v + 0.1, f'{v:.2f}', ha='center', fontsize=12)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'memory_polarization_analysis.png'), dpi=150)
    print_status("Saved: memory_polarization_analysis.png")
    plt.close()


if __name__ == '__main__':
    run_memory_analysis()
