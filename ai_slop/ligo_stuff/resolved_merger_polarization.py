#!/usr/bin/env python3
"""
Resolved Merger Polarization Analysis: GW150914
================================================

Tests whether the Z² framework's h₊ chirality prediction manifests in
individual resolved mergers.

Approach:
1. Download GW150914 strain data from GWOSC
2. Construct h₊-only and standard (h₊ + h×) filter banks
3. Compare matched filter SNR between models
4. Calculate likelihood ratio (proto-Bayes factor)

Physics:
- Standard GR: Both h₊ and h× emitted, ratio depends on inclination
- Z² prediction: h× suppressed by orbifold topology

Author: Carl Zimmerman
Date: May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.interpolate import interp1d
import h5py
import json
import os
import time
import warnings
warnings.filterwarnings('ignore')

try:
    from gwpy.timeseries import TimeSeries
    from pycbc.waveform import get_td_waveform
    from pycbc.filter import matched_filter, sigmasq
    from pycbc.psd import interpolate, inverse_spectrum_truncation
    from pycbc.types import TimeSeries as PyCBCTimeSeries
    HAS_PYCBC = True
except ImportError:
    HAS_PYCBC = False
    print("Note: PyCBC not available. Will use simplified analysis.")

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# GW150914 parameters (from GWTC-1)
GW150914 = {
    'name': 'GW150914',
    'gps_time': 1126259462.4,
    'm1': 35.6,  # Solar masses
    'm2': 30.6,
    'distance': 410,  # Mpc
    'inclination': 2.74,  # radians (nearly edge-on from PE)
    'ra': 1.95,
    'dec': -1.27,
}

# Analysis parameters
CONFIG = {
    'sample_rate': 4096,
    'segment_duration': 8,  # seconds around merger
    'f_low': 20,
    'f_high': 300,
}

def print_header(text):
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)

def print_status(text):
    print(f"  [{time.strftime('%H:%M:%S')}] {text}")


# =============================================================================
# DATA DOWNLOAD
# =============================================================================

def download_gw150914():
    """Download GW150914 strain data from GWOSC."""
    print_status("Downloading GW150914 data...")

    gps = GW150914['gps_time']
    duration = CONFIG['segment_duration']

    data = {}

    for det in ['H1', 'L1']:
        try:
            ts = TimeSeries.fetch_open_data(
                det,
                gps - duration/2,
                gps + duration/2,
                sample_rate=CONFIG['sample_rate'],
                cache=True
            )
            data[det] = ts.value.astype(np.float64)
            print_status(f"  {det}: {len(data[det])} samples")
        except Exception as e:
            print_status(f"  {det}: Failed - {e}")

    return data


# =============================================================================
# WAVEFORM GENERATION
# =============================================================================

def generate_gw_waveform(m1, m2, distance, inclination, polarization='both'):
    """
    Generate gravitational waveform.

    polarization: 'both' (h+ and h×), 'plus_only' (h+ only), 'cross_only' (h× only)
    """
    if not HAS_PYCBC:
        # Simplified waveform for testing
        return generate_simple_waveform(m1, m2, inclination, polarization)

    hp, hc = get_td_waveform(
        approximant='IMRPhenomD',
        mass1=m1,
        mass2=m2,
        delta_t=1.0/CONFIG['sample_rate'],
        f_lower=CONFIG['f_low'],
        distance=distance,
        inclination=inclination
    )

    if polarization == 'both':
        return hp, hc
    elif polarization == 'plus_only':
        return hp, None
    elif polarization == 'cross_only':
        return None, hc
    else:
        raise ValueError(f"Unknown polarization: {polarization}")


def generate_simple_waveform(m1, m2, inclination, polarization='both'):
    """
    Generate simplified inspiral-merger-ringdown waveform.
    For demonstration when PyCBC not available.
    """
    # Total mass and chirp mass
    M = m1 + m2
    eta = m1 * m2 / M**2
    Mc = M * eta**(3/5)

    # Time array
    fs = CONFIG['sample_rate']
    duration = 1.0  # seconds of waveform
    t = np.linspace(-duration, 0, int(duration * fs))

    # Simplified chirping frequency (Newtonian approximation)
    # f(t) = (5/256)^(3/8) * (c^3/(G*Mc))^(5/8) * |t|^(-3/8)
    # Using geometric units where G*M_sun/c^2 = 1.477 km

    # Frequency evolution
    tau = -t + 0.001  # time to merger
    tau = np.maximum(tau, 1e-6)  # avoid division by zero

    # Rough frequency scaling
    f_isco = 4400 / M  # ISCO frequency in Hz (approximate)
    f = f_isco * (tau / 0.01)**(-3/8)
    f = np.minimum(f, f_isco)  # cap at ISCO

    # Phase
    phase = 2 * np.pi * np.cumsum(f) / fs

    # Amplitude (grows as f^(2/3) during inspiral)
    amp = (f / f_isco)**(2/3)
    amp *= np.exp(-((t + 0.01) / 0.02)**2)  # Gaussian ringdown

    # Polarizations (inclination dependence)
    cos_iota = np.cos(inclination)

    # h+ has (1 + cos²ι)/2 dependence
    # h× has cos(ι) dependence
    h_plus_factor = (1 + cos_iota**2) / 2
    h_cross_factor = cos_iota

    hp = amp * h_plus_factor * np.cos(phase) * 1e-21
    hc = amp * h_cross_factor * np.sin(phase) * 1e-21

    if polarization == 'both':
        return hp, hc
    elif polarization == 'plus_only':
        return hp, np.zeros_like(hp)
    elif polarization == 'cross_only':
        return np.zeros_like(hc), hc
    else:
        return hp, hc


# =============================================================================
# ANTENNA PATTERNS
# =============================================================================

def antenna_pattern(ra, dec, psi, gps_time, detector):
    """
    Calculate antenna pattern functions F+ and F× for a detector.

    Simplified version - uses fixed detector orientations.
    """
    # Detector arm orientations (approximate, in radians from North)
    if detector == 'H1':
        arm_angle = np.radians(171.8)  # Hanford
        lat = np.radians(46.45)
    elif detector == 'L1':
        arm_angle = np.radians(243.0)  # Livingston
        lat = np.radians(30.56)
    else:
        raise ValueError(f"Unknown detector: {detector}")

    # Simplified antenna patterns (ignoring Earth rotation for short signals)
    # These are approximations valid near the detector's zenith

    theta = np.pi/2 - dec  # polar angle from detector
    phi = ra

    # Antenna pattern for + and × polarizations
    F_plus = 0.5 * (1 + np.cos(theta)**2) * np.cos(2*phi) * np.cos(2*psi) - \
             np.cos(theta) * np.sin(2*phi) * np.sin(2*psi)

    F_cross = 0.5 * (1 + np.cos(theta)**2) * np.cos(2*phi) * np.sin(2*psi) + \
              np.cos(theta) * np.sin(2*phi) * np.cos(2*psi)

    return F_plus, F_cross


# =============================================================================
# POLARIZATION ANALYSIS
# =============================================================================

def compute_detector_response(hp, hc, detector, ra, dec, psi, gps_time):
    """Compute the strain seen by a detector for given h+ and h×."""
    Fp, Fc = antenna_pattern(ra, dec, psi, gps_time, detector)

    if hp is not None and hc is not None:
        h = Fp * hp + Fc * hc
    elif hp is not None:
        h = Fp * hp
    elif hc is not None:
        h = Fc * hc
    else:
        raise ValueError("At least one of hp, hc must be provided")

    return h, Fp, Fc


def matched_filter_snr(data, template, psd=None, fs=4096):
    """
    Compute matched filter SNR.

    SNR = (d|h) / sqrt(h|h)

    where (a|b) = 4 Re ∫ ã*(f) b̃(f) / Sn(f) df
    """
    n = len(data)

    # FFT
    d_fft = np.fft.rfft(data)
    h_fft = np.fft.rfft(template)
    freqs = np.fft.rfftfreq(n, 1/fs)

    # Default PSD (white noise if not provided)
    if psd is None:
        psd = np.ones(len(freqs))

    # Frequency mask
    f_low = CONFIG['f_low']
    f_high = CONFIG['f_high']
    mask = (freqs >= f_low) & (freqs <= f_high)

    # Avoid division by zero
    psd_safe = np.where(psd > 0, psd, 1e-46)

    # Inner product
    df = freqs[1] - freqs[0]
    integrand_dh = np.conj(d_fft) * h_fft / psd_safe
    integrand_hh = np.conj(h_fft) * h_fft / psd_safe

    inner_dh = 4 * np.real(np.sum(integrand_dh[mask])) * df
    inner_hh = 4 * np.real(np.sum(integrand_hh[mask])) * df

    sigma = np.sqrt(inner_hh) if inner_hh > 0 else 1
    snr = inner_dh / sigma

    return snr, sigma


def estimate_psd(data, fs=4096, nperseg=4096):
    """Estimate power spectral density using Welch's method."""
    freqs, psd = signal.welch(data, fs=fs, nperseg=nperseg)
    return freqs, psd


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_polarization_analysis():
    print_header("RESOLVED MERGER POLARIZATION ANALYSIS: GW150914")
    print_status(f"Testing Z² h₊ chirality on individual BBH merger")

    # Download data
    print_header("DOWNLOADING DATA")
    strain_data = download_gw150914()

    if len(strain_data) < 2:
        print_status("ERROR: Need both H1 and L1 data")
        return None

    # Generate waveforms
    print_header("GENERATING WAVEFORMS")

    m1 = GW150914['m1']
    m2 = GW150914['m2']
    dist = GW150914['distance']
    inc = GW150914['inclination']

    print_status(f"Source: m1={m1} M☉, m2={m2} M☉, D={dist} Mpc")
    print_status(f"Best-fit inclination: ι = {np.degrees(inc):.1f}°")

    # Standard GR waveform (both polarizations)
    print_status("Generating standard GR waveform (h₊ + h×)...")
    hp_std, hc_std = generate_simple_waveform(m1, m2, inc, 'both')

    # h₊-only waveform (Z² prediction)
    print_status("Generating h₊-only waveform (Z² model)...")
    hp_z2, _ = generate_simple_waveform(m1, m2, inc, 'plus_only')

    # h×-only for comparison
    print_status("Generating h×-only waveform (null test)...")
    _, hc_null = generate_simple_waveform(m1, m2, inc, 'cross_only')

    # Analyze each detector
    print_header("COMPUTING MATCHED FILTER SNR")

    results = {}
    ra = GW150914['ra']
    dec = GW150914['dec']
    psi = 0.0  # Polarization angle (marginalize later)
    gps = GW150914['gps_time']

    for det in ['H1', 'L1']:
        print_status(f"\nAnalyzing {det}...")

        data = strain_data[det]
        fs = CONFIG['sample_rate']

        # Estimate PSD
        freqs_psd, psd = estimate_psd(data, fs)
        psd_interp = interp1d(freqs_psd, psd, bounds_error=False, fill_value=np.max(psd))

        # Get detector responses for each model
        h_std, Fp, Fc = compute_detector_response(hp_std, hc_std, det, ra, dec, psi, gps)
        h_z2, _, _ = compute_detector_response(hp_z2, np.zeros_like(hp_z2), det, ra, dec, psi, gps)
        h_null, _, _ = compute_detector_response(np.zeros_like(hc_null), hc_null, det, ra, dec, psi, gps)

        # Pad templates to match data length
        n_data = len(data)
        h_std_padded = np.zeros(n_data)
        h_z2_padded = np.zeros(n_data)
        h_null_padded = np.zeros(n_data)

        # Place template near end of segment (where merger occurs)
        start_idx = n_data - len(h_std) - 100
        h_std_padded[start_idx:start_idx+len(h_std)] = h_std
        h_z2_padded[start_idx:start_idx+len(h_z2)] = h_z2
        h_null_padded[start_idx:start_idx+len(h_null)] = h_null

        # PSD at analysis frequencies
        freqs_analysis = np.fft.rfftfreq(n_data, 1/fs)
        psd_analysis = psd_interp(freqs_analysis)

        # Compute SNRs
        snr_std, sigma_std = matched_filter_snr(data, h_std_padded, psd_analysis, fs)
        snr_z2, sigma_z2 = matched_filter_snr(data, h_z2_padded, psd_analysis, fs)
        snr_null, sigma_null = matched_filter_snr(data, h_null_padded, psd_analysis, fs)

        results[det] = {
            'snr_standard': snr_std,
            'snr_z2_hplus': snr_z2,
            'snr_null_hcross': snr_null,
            'Fp': Fp,
            'Fc': Fc,
        }

        print_status(f"  Standard (h₊+h×):  SNR = {snr_std:.2f}")
        print_status(f"  Z² model (h₊ only): SNR = {snr_z2:.2f}")
        print_status(f"  Null (h× only):     SNR = {snr_null:.2f}")

    # Combined analysis
    print_header("COMBINED NETWORK ANALYSIS")

    # Network SNR (quadrature sum)
    snr_net_std = np.sqrt(sum(r['snr_standard']**2 for r in results.values()))
    snr_net_z2 = np.sqrt(sum(r['snr_z2_hplus']**2 for r in results.values()))
    snr_net_null = np.sqrt(sum(r['snr_null_hcross']**2 for r in results.values()))

    print_status(f"Network SNR (Standard):  {snr_net_std:.2f}")
    print_status(f"Network SNR (Z² h₊):     {snr_net_z2:.2f}")
    print_status(f"Network SNR (h× null):   {snr_net_null:.2f}")

    # Log-likelihood ratio (Bayes factor proxy)
    # ln(B) ≈ (SNR_1² - SNR_2²) / 2
    ln_B_z2_vs_std = (snr_net_z2**2 - snr_net_std**2) / 2
    ln_B_std_vs_null = (snr_net_std**2 - snr_net_null**2) / 2

    print_status(f"\nLog-likelihood ratios:")
    print_status(f"  ln(B_z2/B_std) = {ln_B_z2_vs_std:.2f}")
    print_status(f"  ln(B_std/B_null) = {ln_B_std_vs_null:.2f}")

    # Interpret
    print_header("INTERPRETATION")

    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RESOLVED MERGER POLARIZATION TEST                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  EVENT: GW150914 (First Direct GW Detection)                                 ║
║                                                                              ║
║  NETWORK SNR COMPARISON:                                                     ║
║    Standard GR (h₊ + h×):  {snr_net_std:6.2f}                                        ║
║    Z² Model (h₊ only):     {snr_net_z2:6.2f}                                        ║
║    Null Test (h× only):    {snr_net_null:6.2f}                                        ║
║                                                                              ║
║  LOG-LIKELIHOOD RATIO:                                                       ║
║    Z² vs Standard: {ln_B_z2_vs_std:+7.2f}  {'(Z² preferred)' if ln_B_z2_vs_std > 0 else '(Standard preferred)':20}           ║
║                                                                              ║
║  INTERPRETATION:                                                             ║
║    • Positive ln(B) favors Z² model (h₊ enhancement)                         ║
║    • Negative ln(B) favors standard GR (h₊ + h× equal)                       ║
║    • |ln(B)| > 5 is "strong" evidence                                        ║
║    • |ln(B)| > 8 is "decisive" evidence                                      ║
║                                                                              ║
║  NOTE: This is a simplified analysis. Full Bayesian PE with Bilby            ║
║        would provide rigorous Bayes factors and parameter posteriors.        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    # Save results
    output = {
        'event': GW150914,
        'analysis': {
            'H1': {k: float(v) if isinstance(v, (int, float, np.floating)) else v
                   for k, v in results['H1'].items()},
            'L1': {k: float(v) if isinstance(v, (int, float, np.floating)) else v
                   for k, v in results['L1'].items()},
        },
        'network': {
            'snr_standard': float(snr_net_std),
            'snr_z2': float(snr_net_z2),
            'snr_null': float(snr_net_null),
            'ln_bayes_z2_vs_std': float(ln_B_z2_vs_std),
        },
        'conclusion': 'Z² preferred' if ln_B_z2_vs_std > 0 else 'Standard GR preferred',
    }

    with open(os.path.join(OUTPUT_DIR, 'gw150914_polarization_results.json'), 'w') as f:
        json.dump(output, f, indent=2)

    print_status("Saved: gw150914_polarization_results.json")

    # Create visualization
    create_polarization_plot(strain_data, hp_std, hc_std, hp_z2, results)

    return output


def create_polarization_plot(strain_data, hp_std, hc_std, hp_z2, results):
    """Create visualization of polarization analysis."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    fs = CONFIG['sample_rate']

    # Plot 1: Waveforms
    ax = axes[0, 0]
    t = np.arange(len(hp_std)) / fs
    ax.plot(t, hp_std * 1e21, 'b-', label='h₊ (standard)', alpha=0.7)
    ax.plot(t, hc_std * 1e21, 'r-', label='h× (standard)', alpha=0.7)
    ax.plot(t, hp_z2 * 1e21, 'g--', label='h₊ (Z² model)', linewidth=2)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Strain [×10⁻²¹]')
    ax.set_title('GW150914 Waveform Templates')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 2: H1 strain
    ax = axes[0, 1]
    t_h1 = np.arange(len(strain_data['H1'])) / fs
    ax.plot(t_h1, strain_data['H1'] * 1e21, 'k-', alpha=0.5, linewidth=0.5)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Strain [×10⁻²¹]')
    ax.set_title('H1 Strain Data (GW150914)')
    ax.grid(True, alpha=0.3)

    # Plot 3: L1 strain
    ax = axes[1, 0]
    t_l1 = np.arange(len(strain_data['L1'])) / fs
    ax.plot(t_l1, strain_data['L1'] * 1e21, 'k-', alpha=0.5, linewidth=0.5)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Strain [×10⁻²¹]')
    ax.set_title('L1 Strain Data (GW150914)')
    ax.grid(True, alpha=0.3)

    # Plot 4: SNR comparison
    ax = axes[1, 1]
    detectors = ['H1', 'L1', 'Network']
    snrs_std = [results['H1']['snr_standard'], results['L1']['snr_standard'],
                np.sqrt(results['H1']['snr_standard']**2 + results['L1']['snr_standard']**2)]
    snrs_z2 = [results['H1']['snr_z2_hplus'], results['L1']['snr_z2_hplus'],
               np.sqrt(results['H1']['snr_z2_hplus']**2 + results['L1']['snr_z2_hplus']**2)]

    x = np.arange(len(detectors))
    width = 0.35

    bars1 = ax.bar(x - width/2, snrs_std, width, label='Standard (h₊+h×)', color='blue', alpha=0.7)
    bars2 = ax.bar(x + width/2, snrs_z2, width, label='Z² (h₊ only)', color='green', alpha=0.7)

    ax.set_xlabel('Detector')
    ax.set_ylabel('Matched Filter SNR')
    ax.set_title('SNR Comparison: Standard GR vs Z² Model')
    ax.set_xticks(x)
    ax.set_xticklabels(detectors)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'gw150914_polarization_analysis.png'), dpi=150)
    print_status("Saved: gw150914_polarization_analysis.png")
    plt.close()


if __name__ == '__main__':
    run_polarization_analysis()
