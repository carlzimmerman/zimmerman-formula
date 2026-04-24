#!/usr/bin/env python3
"""
Gravitational Waveform Generator
=================================
Author: Carl Zimmerman
Date: 2026-04-24

Generates the actual gravitational wave strain h(t) for binary mergers.
Includes the characteristic "chirp" signal.
"""

import numpy as np
import json
from typing import Tuple

# =============================================================================
# CONSTANTS
# =============================================================================

G = 6.67430e-11       # m³/kg/s²
c = 2.99792458e8      # m/s
M_sun = 1.98847e30    # kg
Mpc = 3.08567758e22   # m

# =============================================================================
# WAVEFORM PHYSICS
# =============================================================================

def chirp_mass(m1: float, m2: float) -> float:
    """Chirp mass in kg"""
    return (m1 * m2)**(3/5) / (m1 + m2)**(1/5)


def symmetric_mass_ratio(m1: float, m2: float) -> float:
    """η = m1*m2/(m1+m2)²"""
    return (m1 * m2) / (m1 + m2)**2


def phase_evolution(tau: np.ndarray, M_c: float, eta: float) -> np.ndarray:
    """
    Orbital phase as function of time to merger τ

    Using 2PN (post-Newtonian) expansion for accuracy

    Φ(τ) = Φ_c - (1/η) * (τ/5M)^(5/8) * [1 + PN corrections...]

    where M = G*M_c/c³ (geometric chirp mass)
    """
    # Geometric chirp mass (in seconds)
    M_geo = G * M_c / c**3

    # Dimensionless time
    Theta = eta * tau / (5 * M_geo)

    # Leading order phase
    phase = -2 * Theta**(5/8)

    # 1PN correction
    pn1 = (3715/8064 + 55/96 * eta) * Theta**(-1/4)

    # 1.5PN correction
    pn15 = -3 * np.pi / 4 * Theta**(-3/8)

    # 2PN correction
    pn2 = (9275495/14450688 + 284875/258048 * eta + 1855/2048 * eta**2) * Theta**(-1/2)

    # Combined phase
    phase = phase * (1 + pn1 + pn15 + pn2)

    return phase


def frequency_from_tau(tau: np.ndarray, M_c: float) -> np.ndarray:
    """
    GW frequency as function of time to merger

    f(τ) = (1/π) * (5/(256*τ))^(3/8) * (G*M_c/c³)^(-5/8)
    """
    M_geo = G * M_c / c**3

    # Avoid division by zero
    tau_safe = np.maximum(tau, 1e-10)

    f = (1/np.pi) * (5 / (256 * tau_safe))**(3/8) * M_geo**(-5/8)

    return f


def amplitude_from_frequency(f: np.ndarray, M_c: float, distance: float) -> np.ndarray:
    """
    Strain amplitude as function of frequency

    h(f) = (4/d) * (G*M_c/c²)^(5/3) * (π*f/c)^(2/3)
    """
    term1 = 4.0 / distance
    term2 = (G * M_c / c**2)**(5/3)
    term3 = (np.pi * f / c)**(2/3)

    return term1 * term2 * term3


def generate_inspiral_waveform(
    m1_solar: float,
    m2_solar: float,
    distance_mpc: float,
    f_low: float = 20.0,
    f_high: float = None,
    sample_rate: float = 4096.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate the full inspiral gravitational waveform

    Returns:
        t: time array (seconds before merger, t=0 at merger)
        h_plus: plus polarization strain
        h_cross: cross polarization strain
        f: instantaneous frequency
    """
    # Convert to SI
    m1 = m1_solar * M_sun
    m2 = m2_solar * M_sun
    distance = distance_mpc * Mpc

    # Derived quantities
    M_c = chirp_mass(m1, m2)
    M_total = m1 + m2
    eta = symmetric_mass_ratio(m1, m2)

    # ISCO frequency (end of inspiral)
    if f_high is None:
        f_isco = c**3 / (6**(3/2) * np.pi * G * M_total)
        f_high = min(f_isco, sample_rate / 2 - 100)  # Stay below Nyquist

    # Time at f_low
    M_geo = G * M_c / c**3
    tau_start = (5/256) * M_geo**(-5/3) * (np.pi * f_low)**(-8/3)
    tau_end = (5/256) * M_geo**(-5/3) * (np.pi * f_high)**(-8/3)

    # Time array (from tau_start to tau_end)
    # Need enough points for the waveform
    n_points = int((tau_start - tau_end) * sample_rate) + 1
    n_points = min(n_points, 10000000)  # Cap at 10M points

    tau = np.linspace(tau_start, max(tau_end, 1e-6), n_points)

    # Time before merger (t = -tau, so t=0 at merger)
    t = -tau

    # Frequency evolution
    f = frequency_from_tau(tau, M_c)

    # Clip frequency to valid range
    f = np.clip(f, f_low, f_high)

    # Amplitude evolution
    amplitude = amplitude_from_frequency(f, M_c, distance)

    # Phase evolution
    phase = phase_evolution(tau, M_c, eta)

    # GW frequency is twice orbital frequency
    # The waveform oscillates at the GW frequency
    gw_phase = 2 * phase  # Factor of 2 for quadrupole

    # Two polarizations (assuming optimal orientation)
    # h_+ and h_× are 90° out of phase
    h_plus = amplitude * np.cos(gw_phase)
    h_cross = amplitude * np.sin(gw_phase)

    return t, h_plus, h_cross, f


def generate_full_waveform_with_merger(
    m1_solar: float,
    m2_solar: float,
    distance_mpc: float,
    f_low: float = 20.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate waveform including a simple merger/ringdown model
    """
    # Get inspiral
    t_insp, h_plus_insp, h_cross_insp, f_insp = generate_inspiral_waveform(
        m1_solar, m2_solar, distance_mpc, f_low
    )

    # Merger parameters
    M_total = (m1_solar + m2_solar) * M_sun
    M_c = chirp_mass(m1_solar * M_sun, m2_solar * M_sun)
    distance = distance_mpc * Mpc

    # Ringdown frequency (Schwarzschild QNM approximation)
    # f_ring ≈ c³/(2π * G * M_final) * 0.32  (for l=m=2 mode)
    M_final = 0.95 * M_total  # ~5% radiated in GW
    f_ring = c**3 / (2 * np.pi * G * M_final) * 0.32

    # Ringdown damping time
    tau_ring = 2 * G * M_final / c**3 / 0.089  # Q ~ 12 for Schwarzschild

    # Generate ringdown
    t_ring_start = 0
    t_ring = np.linspace(0, 10 * tau_ring, 1000)

    # Peak amplitude at merger
    h_peak = h_plus_insp[-1] * 1.5  # Roughly 1.5x inspiral peak

    # Ringdown waveform (damped sinusoid)
    h_ring = h_peak * np.exp(-t_ring / tau_ring) * np.cos(2 * np.pi * f_ring * t_ring)

    # Combine
    t_full = np.concatenate([t_insp, t_ring])
    h_full = np.concatenate([h_plus_insp, h_ring])
    f_full = np.concatenate([f_insp, np.ones_like(t_ring) * f_ring])

    return t_full, h_full, f_full


# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

def save_waveform_data(t, h, f, filename, metadata=None):
    """Save waveform to JSON"""
    data = {
        "metadata": metadata or {},
        "time_seconds": t.tolist(),
        "strain": h.tolist(),
        "frequency_hz": f.tolist(),
        "n_points": len(t),
        "duration_seconds": float(t[-1] - t[0]),
    }

    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=2)

    print(f"Saved {len(t)} points to {filename}")


def print_waveform_stats(t, h, f, name=""):
    """Print waveform statistics"""
    print(f"\n{'=' * 70}")
    print(f"  WAVEFORM: {name}")
    print(f"{'=' * 70}")

    print(f"\n  Time range:        {t[0]:.4f} s to {t[-1]:.6f} s")
    print(f"  Duration:          {t[-1] - t[0]:.4f} s")
    print(f"  Number of points:  {len(t):,}")

    print(f"\n  Frequency range:   {f[0]:.1f} Hz to {f[-1]:.1f} Hz")

    print(f"\n  Strain amplitude:")
    print(f"    Initial:         {np.abs(h[0]):.3e}")
    print(f"    Peak:            {np.max(np.abs(h)):.3e}")
    print(f"    Final:           {np.abs(h[-1]):.3e}")

    # Number of cycles
    # Estimate from phase or frequency
    dt = np.diff(t)
    n_cycles = np.sum(f[:-1] * np.abs(dt)) / 2  # Divide by 2 for GW vs orbital
    print(f"\n  Estimated cycles:  {n_cycles:.0f}")


def create_ascii_waveform(t, h, width=70, height=20):
    """Create ASCII art representation of waveform"""
    # Sample down for display
    n_display = width
    indices = np.linspace(0, len(t)-1, n_display).astype(int)

    t_disp = t[indices]
    h_disp = h[indices]

    # Normalize to height
    h_norm = h_disp / np.max(np.abs(h_disp))
    h_scaled = ((h_norm + 1) / 2 * (height - 1)).astype(int)

    # Create grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    # Plot points
    for i, y in enumerate(h_scaled):
        y_inv = height - 1 - y  # Invert for display
        if 0 <= y_inv < height:
            grid[y_inv][i] = '*'

    # Add center line
    center = height // 2
    for i in range(width):
        if grid[center][i] == ' ':
            grid[center][i] = '-'

    # Print
    print("\n  Waveform (ASCII visualization):")
    print("  " + "+" + "-" * width + "+")
    for row in grid:
        print("  |" + "".join(row) + "|")
    print("  " + "+" + "-" * width + "+")
    print(f"  {'t = ' + f'{t[0]:.2f}s':<20}{'MERGER':^30}{'t = 0':>20}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  GRAVITATIONAL WAVEFORM GENERATOR")
    print("=" * 70)

    # =========================================================================
    # GW170817 - Binary Neutron Star Merger
    # =========================================================================
    print("\n" + "=" * 70)
    print("  GW170817: Binary Neutron Star Merger")
    print("=" * 70)

    t_ns, h_ns, f_ns = generate_full_waveform_with_merger(
        m1_solar=1.46,
        m2_solar=1.27,
        distance_mpc=40,
        f_low=24
    )

    print_waveform_stats(t_ns, h_ns, f_ns, "GW170817 (NS-NS)")
    create_ascii_waveform(t_ns, h_ns)

    # Show the last second in detail
    print("\n  Last 1 second of inspiral (the 'chirp'):")
    mask = t_ns > -1.0
    t_last = t_ns[mask]
    h_last = h_ns[mask]

    # Sample at specific times
    print(f"\n  {'Time (s)':<15} {'Strain h':<15} {'Frequency (Hz)':<15}")
    print("-" * 50)

    for t_sample in [-1.0, -0.5, -0.2, -0.1, -0.05, -0.02, -0.01, -0.001]:
        idx = np.argmin(np.abs(t_ns - t_sample))
        if idx < len(t_ns):
            print(f"  {t_ns[idx]:<15.4f} {h_ns[idx]:<15.3e} {f_ns[idx]:<15.1f}")

    # =========================================================================
    # GW150914 - Binary Black Hole Merger
    # =========================================================================
    print("\n" + "=" * 70)
    print("  GW150914: Binary Black Hole Merger")
    print("=" * 70)

    t_bh, h_bh, f_bh = generate_full_waveform_with_merger(
        m1_solar=35.6,
        m2_solar=30.6,
        distance_mpc=440,
        f_low=20
    )

    print_waveform_stats(t_bh, h_bh, f_bh, "GW150914 (BH-BH)")
    create_ascii_waveform(t_bh, h_bh)

    # =========================================================================
    # Comparison
    # =========================================================================
    print("\n" + "=" * 70)
    print("  COMPARISON: NS-NS vs BH-BH")
    print("=" * 70)

    print(f"""
  Property              GW170817 (NS-NS)     GW150914 (BH-BH)
  ----------------------------------------------------------------
  Total Mass            2.73 M_sun           66.2 M_sun
  Chirp Mass            1.19 M_sun           28.7 M_sun
  Distance              40 Mpc               440 Mpc
  Duration (>20 Hz)     ~100 s               ~0.2 s
  Peak Frequency        ~1600 Hz             ~150 Hz
  Peak Strain           ~{np.max(np.abs(h_ns)):.1e}           ~{np.max(np.abs(h_bh)):.1e}

  Key Differences:
  - NS-NS: Long inspiral (100s), high frequency, kilonova afterglow
  - BH-BH: Short inspiral (<1s), lower frequency, no EM counterpart
    """)

    # =========================================================================
    # Save waveforms
    # =========================================================================

    save_waveform_data(
        t_ns, h_ns, f_ns,
        "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/gravitational_waves/gw170817_waveform.json",
        metadata={
            "event": "GW170817",
            "type": "Binary Neutron Star",
            "m1_solar": 1.46,
            "m2_solar": 1.27,
            "distance_mpc": 40
        }
    )

    save_waveform_data(
        t_bh, h_bh, f_bh,
        "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/gravitational_waves/gw150914_waveform_full.json",
        metadata={
            "event": "GW150914",
            "type": "Binary Black Hole",
            "m1_solar": 35.6,
            "m2_solar": 30.6,
            "distance_mpc": 440
        }
    )

    # =========================================================================
    # The actual chirp sound (frequency content)
    # =========================================================================
    print("\n" + "=" * 70)
    print("  THE 'CHIRP' - Frequency Evolution")
    print("=" * 70)

    print("""
  The characteristic 'chirp' sound comes from the frequency increasing:

  GW170817 (NS-NS):                    GW150914 (BH-BH):

  t = -60s:   f = 30 Hz  (low hum)    t = -0.5s:  f = 35 Hz
  t = -10s:   f = 50 Hz               t = -0.2s:  f = 50 Hz
  t = -1s:    f = 150 Hz              t = -0.1s:  f = 70 Hz
  t = -0.1s:  f = 500 Hz              t = -0.05s: f = 100 Hz
  t = -0.01s: f = 1200 Hz             t = -0.02s: f = 150 Hz (MERGER)
  t = 0:      f = 1600 Hz (MERGER)

  To hear the chirp: shift frequency UP by ~200x to audio range
  (LIGO does this for public outreach)
    """)

    print("\n" + "=" * 70)
    print("  Waveform generation complete!")
    print("=" * 70)
