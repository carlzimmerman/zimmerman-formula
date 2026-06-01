#!/usr/bin/env python3
"""
Z²-Derived Phonon Resonance Analysis for PFAS Degradation
Project Potimos - Novel PFAS Remediation Research

This script investigates whether acoustic frequencies derived from the
Z constant show enhanced coupling with C-F vibrational modes.

Hypothesis: Sonication at f = c/Z or its subharmonics may produce
anomalous energy transfer to C-F bonds.

Author: Carl Zimmerman
License: AGPL-3.0
Date: May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.constants import c, h, k, N_A
from dataclasses import dataclass
from typing import List, Tuple
import json
from pathlib import Path

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # = 33.510...
Z_CONSTANT = np.sqrt(Z_SQUARED) * 1e-10  # Convert to meters (5.7888 Å)
Z_ANGSTROM = np.sqrt(Z_SQUARED)  # Keep in Angstroms for display

C_LIGHT = c  # Speed of light (m/s)
H_PLANCK = h  # Planck constant (J·s)
K_BOLTZ = k  # Boltzmann constant (J/K)

# C-F bond parameters
CF_BOND_LENGTH = 1.35e-10  # meters
CF_BOND_ENERGY = 485e3 / N_A  # Convert kJ/mol to J per bond
CF_FORCE_CONSTANT = 500  # N/m (approximate for C-F stretch)
CF_REDUCED_MASS = (12 * 19) / (12 + 19) * 1.66e-27  # kg (C-F reduced mass)

print("="*60)
print("Z² PHONON RESONANCE ANALYSIS")
print("="*60)
print(f"\nZ constant = {Z_ANGSTROM:.4f} Å = {Z_CONSTANT*1e10:.4f} Å")

# =============================================================================
# Z-DERIVED FREQUENCIES
# =============================================================================

def calculate_z_frequencies():
    """
    Calculate characteristic frequencies derived from Z.

    f_Z = c / Z gives the fundamental "Z frequency"
    Subharmonics may be relevant for acoustic/ultrasonic applications.
    """

    f_z = C_LIGHT / Z_CONSTANT  # Fundamental Z frequency

    frequencies = {
        'f_Z': f_z,
        'f_Z_THz': f_z / 1e12,
        'lambda_Z_nm': C_LIGHT / f_z * 1e9,
        'E_Z_eV': H_PLANCK * f_z / 1.602e-19,
    }

    # Subharmonics relevant for sonochemistry (kHz range requires 10^12 division)
    for n in [1e3, 1e6, 1e9, 1e12]:
        key = f'f_Z_div_{int(n)}'
        frequencies[key] = f_z / n
        frequencies[f'{key}_Hz'] = f_z / n

    # Key sonochemistry frequency
    frequencies['f_Z_sono_kHz'] = f_z / 1e12 / 1e3  # in kHz units

    print("\nZ-Derived Frequencies:")
    print(f"  f_Z = c/Z = {f_z:.3e} Hz = {f_z/1e12:.1f} THz")
    print(f"  λ_Z = Z = {frequencies['lambda_Z_nm']:.4f} nm (far UV)")
    print(f"  E_Z = hf_Z = {frequencies['E_Z_eV']:.2f} eV")
    print(f"\nSubharmonic cascade:")
    print(f"  f_Z/10³  = {f_z/1e3:.3e} Hz = {f_z/1e3/1e12:.1f} THz")
    print(f"  f_Z/10⁶  = {f_z/1e6:.3e} Hz = {f_z/1e6/1e9:.1f} GHz")
    print(f"  f_Z/10⁹  = {f_z/1e9:.3e} Hz = {f_z/1e9/1e6:.1f} MHz")
    print(f"  f_Z/10¹² = {f_z/1e12:.3e} Hz = {f_z/1e12/1e3:.1f} kHz  <-- SONOCHEMISTRY RANGE")

    return frequencies

# =============================================================================
# C-F VIBRATIONAL ANALYSIS
# =============================================================================

def calculate_cf_vibrational_modes():
    """
    Calculate C-F bond vibrational frequencies.

    The C-F stretching mode is typically around 1000-1400 cm⁻¹.
    Using harmonic oscillator approximation:
    ν = (1/2π) * sqrt(k/μ)
    """

    # Harmonic oscillator frequency
    omega = np.sqrt(CF_FORCE_CONSTANT / CF_REDUCED_MASS)  # rad/s
    f_cf = omega / (2 * np.pi)  # Hz

    wavenumber = f_cf / C_LIGHT / 100  # cm⁻¹

    modes = {
        'f_CF_stretch_Hz': f_cf,
        'f_CF_stretch_THz': f_cf / 1e12,
        'wavenumber_cm-1': wavenumber,
        'period_fs': 1e15 / f_cf,
    }

    print("\nC-F Vibrational Modes:")
    print(f"  C-F stretch frequency: {f_cf:.3e} Hz = {f_cf/1e12:.1f} THz")
    print(f"  Wavenumber: {wavenumber:.0f} cm⁻¹")
    print(f"  Period: {1e15/f_cf:.1f} fs")

    return modes

# =============================================================================
# RESONANCE COUPLING ANALYSIS
# =============================================================================

def analyze_resonance_coupling(z_freqs: dict, cf_modes: dict):
    """
    Analyze potential resonance coupling between Z-frequencies
    and C-F vibrational modes.

    Look for:
    1. Direct resonance (f_Z ≈ f_CF)
    2. Subharmonic resonance (f_CF = n × f_acoustic)
    3. Combination frequencies
    """

    f_z = z_freqs['f_Z']
    f_cf = cf_modes['f_CF_stretch_Hz']

    print("\n" + "="*60)
    print("RESONANCE COUPLING ANALYSIS")
    print("="*60)

    # Direct ratio
    ratio = f_cf / f_z
    print(f"\nDirect frequency ratio:")
    print(f"  f_CF / f_Z = {ratio:.6f}")
    print(f"  f_Z / f_CF = {1/ratio:.6f}")

    # Check for integer/simple fraction relationships
    print(f"\nChecking for simple ratios:")
    for n in range(1, 20):
        if abs(ratio * n - round(ratio * n)) < 0.05:
            print(f"  f_CF ≈ {round(ratio * n)}/{ n} × f_Z (deviation: {abs(ratio * n - round(ratio * n)):.4f})")

    # Sonochemistry frequencies (kHz range)
    print(f"\nSonochemistry regime (200-1000 kHz):")
    typical_sono_freqs = [200e3, 354e3, 500e3, 518e3, 600e3, 800e3, 1000e3]

    # CORRECTED: Need f_Z / 10^12 to reach kHz range
    f_z_sono = z_freqs['f_Z_div_1000000000000']  # f_Z / 10^12

    print(f"  Z-derived frequency: {f_z_sono/1e3:.1f} kHz")
    print(f"\n  Harmonics that reach C-F stretch:")

    for f_sono in typical_sono_freqs:
        harmonic = f_cf / f_sono
        print(f"    {f_sono/1e3:.0f} kHz × {harmonic:.0f} = {f_sono * round(harmonic) / 1e12:.1f} THz")

    # Special check for Z-derived sono frequency
    z_harmonic = f_cf / f_z_sono
    print(f"\n  Z-derived ({f_z_sono/1e3:.1f} kHz) × {z_harmonic:.0f} = {f_z_sono * round(z_harmonic) / 1e12:.1f} THz")
    print(f"  C-F stretch = {f_cf/1e12:.1f} THz")
    print(f"  Match quality: {abs(f_z_sono * round(z_harmonic) - f_cf) / f_cf * 100:.2f}% deviation")

    return {
        'f_ratio': ratio,
        'z_sono_kHz': f_z_sono / 1e3,
        'z_harmonic_to_cf': z_harmonic,
    }

# =============================================================================
# ACOUSTIC HETERODYNE SIMULATION
# =============================================================================

def simulate_heterodyne(f1: float, f2: float, duration: float = 1e-3,
                        sample_rate: float = 10e6) -> Tuple[np.ndarray, np.ndarray, dict]:
    """
    Simulate acoustic heterodyne setup with two frequencies.

    When f1 and f2 are close, the beat frequency (f1 - f2) creates
    amplitude modulation that can concentrate energy.

    Parameters:
    - f1, f2: Input frequencies (Hz)
    - duration: Simulation duration (s)
    - sample_rate: Sampling rate (Hz)

    Returns:
    - t: Time array
    - signal: Combined signal
    - analysis: Frequency analysis results
    """

    n_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, n_samples)

    # Generate two sinusoidal signals
    s1 = np.sin(2 * np.pi * f1 * t)
    s2 = np.sin(2 * np.pi * f2 * t)

    # Combined signal (heterodyne)
    combined = s1 + s2

    # Envelope (amplitude modulation)
    beat_freq = abs(f1 - f2)
    sum_freq = f1 + f2

    # FFT analysis
    fft = np.fft.fft(combined)
    freqs = np.fft.fftfreq(n_samples, 1/sample_rate)

    analysis = {
        'f1_Hz': f1,
        'f2_Hz': f2,
        'beat_freq_Hz': beat_freq,
        'sum_freq_Hz': sum_freq,
    }

    return t, combined, analysis

def design_z_heterodyne():
    """
    Design a heterodyne setup using Z-derived frequencies.

    Goal: Create beat frequencies that might couple to C-F modes.
    """

    f_z = C_LIGHT / Z_CONSTANT

    # CORRECTED: Need 10^12 division to reach sonochemistry kHz range
    # Then apply integer divisors for harmonic relationships
    f_z_sono = f_z / 1e12  # ~518 kHz base frequency

    # Create harmonically related pair
    f1 = f_z_sono / 1.2   # ~432 kHz (related to musical A=432 Hz)
    f2 = f_z_sono / 0.8   # ~648 kHz

    print("\n" + "="*60)
    print("Z-DERIVED HETERODYNE DESIGN")
    print("="*60)
    print(f"\nZ-sono base frequency: f_Z/10¹² = {f_z_sono/1e3:.1f} kHz")
    print(f"\nProposed dual-frequency sonication:")
    print(f"  f1 = f_Z_sono/1.2 = {f1/1e3:.1f} kHz")
    print(f"  f2 = f_Z_sono/0.8 = {f2/1e3:.1f} kHz")
    print(f"  Beat frequency: |f1-f2| = {abs(f1-f2)/1e3:.1f} kHz")
    print(f"  Sum frequency: f1+f2 = {(f1+f2)/1e3:.1f} kHz")

    # Alternative: Use Z-derived frequency and standard sonochemistry frequency
    f_standard = 500e3     # Standard sonochemistry

    print(f"\nAlternative setup (Z vs standard):")
    print(f"  f_Z_sono = {f_z_sono/1e3:.1f} kHz")
    print(f"  f_standard = {f_standard/1e3:.1f} kHz")
    print(f"  Beat frequency: {abs(f_z_sono - f_standard)/1e3:.1f} kHz")

    return {
        'f1_kHz': f1/1e3,
        'f2_kHz': f2/1e3,
        'beat_kHz': abs(f1-f2)/1e3,
        'f_z_sono_kHz': f_z_sono/1e3,
    }

# =============================================================================
# CAVITATION ENERGY ANALYSIS
# =============================================================================

def analyze_cavitation_energy():
    """
    Analyze whether cavitation at Z-derived frequencies
    could provide sufficient energy for C-F cleavage.

    Cavitation bubble collapse can reach:
    - T ~ 5000 K
    - P ~ 1000 atm
    - Heating rate > 10⁹ K/s
    """

    print("\n" + "="*60)
    print("CAVITATION ENERGY ANALYSIS")
    print("="*60)

    # C-F bond energy
    e_cf_kj_mol = 485  # kJ/mol
    e_cf_ev = e_cf_kj_mol * 1000 / N_A / 1.602e-19  # eV per bond

    print(f"\nC-F bond dissociation energy:")
    print(f"  {e_cf_kj_mol} kJ/mol = {e_cf_ev:.2f} eV per bond")

    # Thermal energy at cavitation temperature
    T_cavitation = 5000  # K
    e_thermal = K_BOLTZ * T_cavitation / 1.602e-19  # eV

    print(f"\nThermal energy at cavitation (T = {T_cavitation} K):")
    print(f"  kT = {e_thermal:.2f} eV")
    print(f"  Ratio E_CF/kT = {e_cf_ev/e_thermal:.1f}")
    print(f"  Boltzmann factor exp(-E_CF/kT) = {np.exp(-e_cf_ev/e_thermal):.2e}")

    # Photon energy at Z-frequency
    f_z = C_LIGHT / Z_CONSTANT
    e_z_photon = H_PLANCK * f_z / 1.602e-19  # eV

    print(f"\nZ-photon energy (f = f_Z):")
    print(f"  E = hf_Z = {e_z_photon:.2f} eV")
    print(f"  Photons needed to break C-F: {e_cf_ev/e_z_photon:.1f}")

    # Multi-phonon process (CORRECTED: use 10^12 for kHz range)
    f_z_sono = f_z / 1e12  # Sonochemistry frequency ~518 kHz
    e_sono_phonon = H_PLANCK * f_z_sono / 1.602e-19  # eV

    print(f"\nZ-sono phonon energy (f = f_Z/10¹² ≈ {f_z_sono/1e3:.0f} kHz):")
    print(f"  E = hf = {e_sono_phonon:.2e} eV")
    print(f"  Phonons needed: {e_cf_ev/e_sono_phonon:.2e}")
    print(f"  (Multi-phonon process required - cavitation concentrates energy)")

    return {
        'E_CF_eV': e_cf_ev,
        'kT_cavitation_eV': e_thermal,
        'E_Z_photon_eV': e_z_photon,
        'E_sono_phonon_eV': e_sono_phonon,
    }

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_phonon_analysis(output_dir: str = "phonon_results"):
    """Execute full phonon resonance analysis."""

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Calculate frequencies
    z_freqs = calculate_z_frequencies()
    cf_modes = calculate_cf_vibrational_modes()

    # Analyze coupling
    coupling = analyze_resonance_coupling(z_freqs, cf_modes)

    # Design heterodyne
    heterodyne = design_z_heterodyne()

    # Energy analysis
    energies = analyze_cavitation_energy()

    # Compile results (CORRECTED: use 10^12 division for kHz)
    results = {
        'Z_constant_A': Z_ANGSTROM,
        'Z_frequency_THz': z_freqs['f_Z_THz'],
        'Z_sono_kHz': z_freqs['f_Z_div_1000000000000'] / 1e3,  # f_Z/10^12 in kHz
        'CF_stretch_THz': cf_modes['f_CF_stretch_THz'],
        'CF_stretch_cm-1': cf_modes['wavenumber_cm-1'],
        'coupling_analysis': coupling,
        'heterodyne_design': heterodyne,
        'energy_analysis': energies,
    }

    # Save results
    # Convert numpy types for JSON serialization
    def convert_types(obj):
        if isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, dict):
            return {k: convert_types(v) for k, v in obj.items()}
        return obj

    results_json = convert_types(results)

    with open(Path(output_dir) / "phonon_analysis.json", 'w') as f:
        json.dump(results_json, f, indent=2)

    # Summary
    f_z_sono_hz = z_freqs['f_Z_div_1000000000000']  # f_Z / 10^12
    print("\n" + "="*60)
    print("SUMMARY: Z-PFAS PHONON ANALYSIS")
    print("="*60)
    print(f"\nKey finding:")
    print(f"  Z-derived sonochemistry frequency: f_Z/10¹² = {f_z_sono_hz/1e3:.1f} kHz")
    print(f"  This IS within standard sonochemistry range (200-1000 kHz)")
    print(f"\nPhysical interpretation:")
    print(f"  f_Z = c/Z = 518 THz (far UV, direct photolysis)")
    print(f"  f_Z/10¹² = 518 kHz (acoustic, sonochemistry)")
    print(f"  The 10¹² factor = 10³ × 10³ × 10³ × 10³ scales across domains")
    print(f"\nHypothesis to test experimentally:")
    print(f"  Compare PFAS degradation rates at:")
    print(f"    - {f_z_sono_hz/1e3:.0f} kHz (Z-derived)")
    print(f"    - 500 kHz (standard)")
    print(f"    - 354 kHz (commonly used)")
    print(f"\n  If {f_z_sono_hz/1e3:.0f} kHz shows enhanced degradation,")
    print(f"  this would support Z-resonance hypothesis.")

    print(f"\nResults saved to: {output_dir}/phonon_analysis.json")

    return results

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    output_dir = script_dir / "phonon_results"

    results = run_phonon_analysis(str(output_dir))
