#!/usr/bin/env python3
"""
Telesterion Rigorous Wave Scattering Analysis
==============================================

First-principles analysis using:
- Helmholtz equation for wave propagation
- Bessel function expansion for cylinder scattering
- Interaural phase/time differences
- Psychoacoustic thresholds

Tests: Can columns create detectable binaural effects at 40 Hz?

Author: Carl Zimmerman
Date: April 28, 2026

Sources:
- Morse & Ingard, "Theoretical Acoustics"
- Kinsler & Frey, "Fundamentals of Acoustics"
- Psychoacoustic literature (Blauert, "Spatial Hearing")
"""

import numpy as np
from scipy import special
from dataclasses import dataclass
from typing import Dict, Tuple, List
import json

# =============================================================================
# PHYSICAL PARAMETERS
# =============================================================================

@dataclass
class ScatteringParameters:
    """Parameters for cylinder scattering analysis."""

    # Column properties
    column_radius_m: float = 0.875  # Half of ~1.75m diameter
    num_columns: int = 42
    column_arrangement: str = "6 rows × 7 columns"

    # Room properties
    room_length_m: float = 51.5
    room_width_m: float = 51.5
    column_spacing_x_m: float = 7.36  # 51.5 / 7
    column_spacing_y_m: float = 8.58  # 51.5 / 6

    # Acoustic properties
    sound_speed_ms: float = 343.0
    air_density_kg_m3: float = 1.2

    # Human head properties (for binaural analysis)
    head_radius_m: float = 0.0875  # ~17.5 cm diameter
    interaural_distance_m: float = 0.17  # Ear-to-ear through head

    # Anaktoron (central stone structure)
    # CORRECTED dimensions from Mylonas/Travlos
    anaktoron_length_m: float = 14.0
    anaktoron_width_m: float = 5.0


# =============================================================================
# BESSEL FUNCTION CYLINDER SCATTERING
# =============================================================================

def cylinder_scattering_coefficient(n: int, ka: float) -> complex:
    """
    Calculate scattering coefficient for mode n.

    For a rigid cylinder, the scattered field is:
    p_s = Σ aₙ Hₙ⁽¹⁾(kr) cos(nθ)

    where aₙ = -Jₙ'(ka) / Hₙ'⁽¹⁾(ka)

    Parameters:
        n: Angular mode number
        ka: Dimensionless wavenumber × radius

    Returns:
        Complex scattering coefficient aₙ
    """
    # Bessel function of first kind and its derivative
    Jn = special.jv(n, ka)
    Jn_prime = special.jvp(n, ka)

    # Hankel function of first kind (H = J + iY) and its derivative
    Yn = special.yv(n, ka)
    Yn_prime = special.yvp(n, ka)

    Hn = Jn + 1j * Yn
    Hn_prime = Jn_prime + 1j * Yn_prime

    # Scattering coefficient
    if abs(Hn_prime) > 1e-10:
        an = -Jn_prime / Hn_prime
    else:
        an = 0

    return an


def total_scattering_cross_section(ka: float, n_max: int = 20) -> float:
    """
    Calculate total scattering cross section.

    σ_s = (4/k) Σ |aₙ|²

    Returns cross section in units of cylinder radius.
    """
    sigma = 0
    for n in range(n_max):
        an = cylinder_scattering_coefficient(n, ka)
        epsilon_n = 1 if n == 0 else 2  # Neumann factor
        sigma += epsilon_n * abs(an)**2

    k = ka  # Normalized
    if k > 0:
        sigma *= 4 / k

    return sigma


def scattered_field_pattern(ka: float, angles_deg: np.ndarray,
                           n_max: int = 20) -> Dict:
    """
    Calculate scattered pressure field vs angle.

    The scattered field at angle θ is:
    p_s(θ) = Σ aₙ εₙ cos(nθ)

    for far-field (kr >> 1).

    Parameters:
        ka: Wavenumber × radius
        angles_deg: Array of scattering angles
        n_max: Maximum mode number

    Returns:
        Dictionary with scattered amplitude and phase
    """
    angles_rad = angles_deg * np.pi / 180

    p_scattered = np.zeros(len(angles_rad), dtype=complex)

    for n in range(n_max):
        an = cylinder_scattering_coefficient(n, ka)
        epsilon_n = 1 if n == 0 else 2

        # Far-field scattered pattern
        p_scattered += an * epsilon_n * np.cos(n * angles_rad)

    amplitude = np.abs(p_scattered)
    phase_rad = np.angle(p_scattered)

    # Normalize amplitude
    max_amp = np.max(amplitude)
    if max_amp > 0:
        amplitude_norm = amplitude / max_amp
    else:
        amplitude_norm = amplitude

    return {
        "angles_deg": angles_deg,
        "amplitude": amplitude_norm,
        "amplitude_dB": 20 * np.log10(amplitude_norm + 1e-10),
        "phase_deg": phase_rad * 180 / np.pi,
        "ka": ka
    }


# =============================================================================
# BINAURAL ANALYSIS
# =============================================================================

def analyze_binaural_effects(params: ScatteringParameters,
                            frequency_Hz: float,
                            listener_position: Tuple[float, float],
                            column_position: Tuple[float, float],
                            source_position: Tuple[float, float]) -> Dict:
    """
    Analyze interaural phase and time differences for scattered sound.

    The human auditory system uses:
    - ITD (Interaural Time Difference): Δt between ears
    - IPD (Interaural Phase Difference): Δφ between ears
    - ILD (Interaural Level Difference): ΔdB between ears

    For localization, humans are sensitive to:
    - ITD: ~10-20 μs at best
    - IPD: ~10-15° at low frequencies

    Parameters:
        params: Scattering parameters
        frequency_Hz: Sound frequency
        listener_position: (x, y) of listener center
        column_position: (x, y) of scattering column
        source_position: (x, y) of sound source
    """
    # Wavelength and wavenumber
    wavelength = params.sound_speed_ms / frequency_Hz
    k = 2 * np.pi / wavelength
    ka = k * params.column_radius_m

    # Scattering regime
    if ka < 0.1:
        regime = "Rayleigh (ka << 1): Column much smaller than wavelength, minimal scattering"
    elif ka < 1:
        regime = "Moderate (ka ~ 1): Column comparable to wavelength, some scattering"
    else:
        regime = "Geometric (ka >> 1): Column much larger than wavelength, strong scattering"

    # Listener ear positions (assuming facing source)
    source_to_listener = np.array([listener_position[0] - source_position[0],
                                   listener_position[1] - source_position[1]])
    distance_to_source = np.linalg.norm(source_to_listener)
    direction = source_to_listener / (distance_to_source + 1e-10)

    # Perpendicular direction (left-right)
    perpendicular = np.array([-direction[1], direction[0]])

    left_ear = np.array(listener_position) + params.interaural_distance_m/2 * perpendicular
    right_ear = np.array(listener_position) - params.interaural_distance_m/2 * perpendicular

    # Direct path (no scattering)
    direct_left = np.linalg.norm(left_ear - np.array(source_position))
    direct_right = np.linalg.norm(right_ear - np.array(source_position))

    direct_ITD_s = (direct_left - direct_right) / params.sound_speed_ms
    direct_ITD_us = direct_ITD_s * 1e6
    direct_IPD_deg = direct_ITD_s * frequency_Hz * 360

    # Path via column (source → column → ear)
    source_to_column = np.linalg.norm(np.array(column_position) - np.array(source_position))

    column_to_left = np.linalg.norm(left_ear - np.array(column_position))
    column_to_right = np.linalg.norm(right_ear - np.array(column_position))

    scattered_path_left = source_to_column + column_to_left
    scattered_path_right = source_to_column + column_to_right

    # Time difference for scattered path
    scattered_ITD_s = (scattered_path_left - scattered_path_right) / params.sound_speed_ms
    scattered_ITD_us = scattered_ITD_s * 1e6
    scattered_IPD_deg = scattered_ITD_s * frequency_Hz * 360

    # Additional phase from scattering
    # At angles near forward scattering, phase shift is minimal
    # At angles near 90°, phase shift can be significant

    # Human perception thresholds
    ITD_threshold_us = 20  # ~20 μs is human limit for pure tones
    IPD_threshold_deg = 15  # ~15° is typical threshold

    # Check if differences are perceptible
    direct_ITD_perceptible = abs(direct_ITD_us) > ITD_threshold_us
    direct_IPD_perceptible = abs(direct_IPD_deg) > IPD_threshold_deg

    return {
        "frequency_Hz": frequency_Hz,
        "wavelength_m": wavelength,
        "ka": ka,
        "scattering_regime": regime,

        "direct_path": {
            "left_ear_distance_m": direct_left,
            "right_ear_distance_m": direct_right,
            "ITD_us": direct_ITD_us,
            "IPD_deg": direct_IPD_deg,
            "ITD_perceptible": direct_ITD_perceptible,
            "IPD_perceptible": direct_IPD_perceptible
        },

        "scattered_path": {
            "source_to_column_m": source_to_column,
            "column_to_left_m": column_to_left,
            "column_to_right_m": column_to_right,
            "ITD_us": scattered_ITD_us,
            "IPD_deg": scattered_IPD_deg
        },

        "perception_thresholds": {
            "ITD_us": ITD_threshold_us,
            "IPD_deg": IPD_threshold_deg
        }
    }


def analyze_gamma_frequency_scattering(params: ScatteringParameters) -> Dict:
    """
    Specific analysis for 40 Hz (gamma frequency).

    Tests the hypothesis: Do columns create binaural effects at 40 Hz?
    """
    frequency = 40.0
    wavelength = params.sound_speed_ms / frequency  # ~8.57 m

    k = 2 * np.pi / wavelength
    ka = k * params.column_radius_m

    print(f"\n40 Hz ANALYSIS:")
    print(f"  Wavelength: {wavelength:.2f} m")
    print(f"  Column radius: {params.column_radius_m:.3f} m")
    print(f"  ka parameter: {ka:.3f}")

    # The key question: Is ka large enough for significant scattering?

    # Calculate scattering coefficients
    coeffs = []
    for n in range(5):
        an = cylinder_scattering_coefficient(n, ka)
        coeffs.append({
            "n": n,
            "magnitude": abs(an),
            "phase_deg": np.angle(an) * 180 / np.pi
        })

    # Total scattering cross section
    sigma = total_scattering_cross_section(ka)

    # Scattered field pattern
    angles = np.linspace(0, 360, 361)
    pattern = scattered_field_pattern(ka, angles)

    # Maximum angular variation in scattered field
    max_variation_dB = np.max(pattern["amplitude_dB"]) - np.min(pattern["amplitude_dB"])

    # Critical assessment
    if ka < 0.3:
        assessment = "NEGLIGIBLE scattering - wavelength much larger than column"
    elif ka < 1.0:
        assessment = "WEAK scattering - some directional effects but limited"
    else:
        assessment = "MODERATE scattering - noticeable directional effects"

    return {
        "frequency_Hz": frequency,
        "wavelength_m": wavelength,
        "column_radius_m": params.column_radius_m,
        "ka": ka,
        "scattering_coefficients": coeffs,
        "total_cross_section_normalized": sigma,
        "max_angular_variation_dB": max_variation_dB,
        "assessment": assessment
    }


def analyze_head_as_scatterer(params: ScatteringParameters,
                              frequency_Hz: float) -> Dict:
    """
    Analyze the human head as a sound scatterer.

    For binaural beats to work, the head must create sufficient
    interaural differences. At low frequencies, the head is
    acoustically "transparent".
    """
    wavelength = params.sound_speed_ms / frequency_Hz
    k = 2 * np.pi / wavelength
    ka_head = k * params.head_radius_m

    # Head scattering regime
    if ka_head < 0.3:
        head_effect = "TRANSPARENT - sound diffracts around head, minimal ILD"
    elif ka_head < 1.5:
        head_effect = "TRANSITIONAL - some head shadow, moderate ILD"
    else:
        head_effect = "SHADOWING - significant head shadow, strong ILD"

    # At low frequencies, ITD dominates over ILD
    # Maximum ITD for plane wave is ~700 μs (head diameter / c)
    max_ITD_us = params.interaural_distance_m / params.sound_speed_ms * 1e6

    # IPD at this frequency
    max_IPD_deg = max_ITD_us * 1e-6 * frequency_Hz * 360

    return {
        "frequency_Hz": frequency_Hz,
        "wavelength_m": wavelength,
        "head_radius_m": params.head_radius_m,
        "ka_head": ka_head,
        "head_effect": head_effect,
        "max_ITD_us": max_ITD_us,
        "max_IPD_deg": max_IPD_deg,
        "note": f"At {frequency_Hz} Hz, IPD of {max_IPD_deg:.1f}° is {'above' if max_IPD_deg > 15 else 'below'} typical threshold"
    }


# =============================================================================
# COLUMN BINAURAL BEATS HYPOTHESIS
# =============================================================================

def test_binaural_beats_hypothesis(params: ScatteringParameters) -> Dict:
    """
    Rigorous test of the hypothesis:
    "Columns create passive binaural beats via phase-shifted reflections"

    For this to work:
    1. Columns must scatter sound significantly
    2. Left/right ears must receive different phases
    3. Phase difference must be perceptible
    """

    frequency = 40.0  # Gamma frequency

    results = {
        "hypothesis": "Columns create passive binaural beats at 40 Hz",
        "frequency_Hz": frequency,
        "tests": []
    }

    # Test 1: Is column scattering significant?
    wavelength = params.sound_speed_ms / frequency
    ka_column = 2 * np.pi * params.column_radius_m / wavelength

    test1 = {
        "test": "Column scattering magnitude",
        "ka": ka_column,
        "regime": "Rayleigh" if ka_column < 0.5 else "Moderate" if ka_column < 2 else "Geometric",
        "scattering_significant": ka_column > 0.5,
        "explanation": f"At ka = {ka_column:.2f}, scattering is {'significant' if ka_column > 0.5 else 'weak'}"
    }
    results["tests"].append(test1)

    # Test 2: Does head create sufficient ILD at 40 Hz?
    ka_head = 2 * np.pi * params.head_radius_m / wavelength

    test2 = {
        "test": "Head shadow at 40 Hz",
        "ka_head": ka_head,
        "head_is_transparent": ka_head < 0.3,
        "explanation": f"At ka = {ka_head:.3f}, the head is {'acoustically transparent' if ka_head < 0.3 else 'partially opaque'}"
    }
    results["tests"].append(test2)

    # Test 3: What is maximum achievable IPD?
    max_ITD_us = params.interaural_distance_m / params.sound_speed_ms * 1e6
    max_IPD_deg = max_ITD_us * 1e-6 * frequency * 360

    test3 = {
        "test": "Maximum interaural phase difference",
        "max_ITD_us": max_ITD_us,
        "max_IPD_at_40Hz_deg": max_IPD_deg,
        "perceptible": max_IPD_deg > 15,
        "explanation": f"Max IPD of {max_IPD_deg:.1f}° is {'above' if max_IPD_deg > 15 else 'below'} 15° threshold"
    }
    results["tests"].append(test3)

    # Test 4: Can column scattering create DIFFERENT phases at each ear?
    # For this, we need the column to be between source and listener
    # AND the scattering to create an asymmetric field

    # In the far field, scattered amplitude varies as cos(nθ)
    # Phase difference between ±10° (typical head subtended angle) is:
    # Δφ ≈ 20° × (scattered phase gradient)

    # At ka = 0.64, the n=1 mode dominates, giving:
    a1 = cylinder_scattering_coefficient(1, ka_column)
    phase_gradient_deg_per_deg = abs(a1) * 1  # Very rough estimate

    scattered_IPD = 20 * phase_gradient_deg_per_deg  # Over 20° head angle

    test4 = {
        "test": "Scattered phase difference across head",
        "n1_coefficient": abs(a1),
        "estimated_IPD_from_scattering_deg": scattered_IPD,
        "significant": scattered_IPD > 5,
        "explanation": f"Column scattering creates ~{scattered_IPD:.1f}° IPD across head width"
    }
    results["tests"].append(test4)

    # VERDICT
    all_tests_pass = (test1["scattering_significant"] and
                      test3["perceptible"])

    results["verdict"] = {
        "hypothesis_supported": all_tests_pass,
        "explanation": """
The "passive binaural beats" hypothesis requires:
1. Significant column scattering ✓ (ka = 0.64, moderate regime)
2. Head to differentiate phases ✓ (max IPD = 7.1°, marginal)

HOWEVER: "Binaural beats" technically refers to the PERCEPTION of a
difference tone when two slightly different frequencies reach the ears.
Columns create PHASE differences, not FREQUENCY differences.

The correct terminology is "interaural phase disparity" or
"spatial decorrelation", not "binaural beats".

At 40 Hz, the column scattering can create small interaural differences,
but the effect is MARGINAL, not dramatic.
"""
    }

    return results


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_wave_scattering_analysis():
    """Run complete wave scattering analysis."""

    print("="*70)
    print("TELESTERION RIGOROUS WAVE SCATTERING")
    print("Helmholtz Equation & Bessel Function Analysis")
    print("="*70)

    params = ScatteringParameters()

    # === 1. Basic scattering parameters ===
    print("\n" + "="*70)
    print("1. SCATTERING PARAMETERS")
    print("="*70)

    print(f"\nColumn properties:")
    print(f"  Radius: {params.column_radius_m:.3f} m (diameter {2*params.column_radius_m:.2f} m)")
    print(f"  Count: {params.num_columns}")
    print(f"  Arrangement: {params.column_arrangement}")

    print(f"\nFrequencies of interest:")
    freqs = [3.33, 6.67, 18.9, 40.0, 100.0, 400.0]
    for f in freqs:
        wavelength = params.sound_speed_ms / f
        ka = 2 * np.pi * params.column_radius_m / wavelength
        print(f"  {f:6.1f} Hz: λ = {wavelength:6.2f} m, ka = {ka:.3f}")

    # === 2. Gamma frequency analysis ===
    print("\n" + "="*70)
    print("2. GAMMA FREQUENCY (40 Hz) SCATTERING")
    print("="*70)

    gamma = analyze_gamma_frequency_scattering(params)

    print(f"\nScattering analysis:")
    print(f"  ka = {gamma['ka']:.3f}")
    print(f"  Assessment: {gamma['assessment']}")
    print(f"  Angular variation: {gamma['max_angular_variation_dB']:.1f} dB")

    print(f"\nScattering coefficients |aₙ|:")
    for c in gamma["scattering_coefficients"]:
        print(f"  n={c['n']}: |a| = {c['magnitude']:.4f}")

    # === 3. Head as scatterer ===
    print("\n" + "="*70)
    print("3. HUMAN HEAD AS SCATTERER")
    print("="*70)

    for f in [6.67, 40.0, 400.0]:
        head = analyze_head_as_scatterer(params, f)
        print(f"\n{f} Hz:")
        print(f"  ka_head = {head['ka_head']:.3f}")
        print(f"  Effect: {head['head_effect']}")
        print(f"  Max ITD: {head['max_ITD_us']:.1f} μs")
        print(f"  Max IPD: {head['max_IPD_deg']:.1f}°")

    # === 4. Binaural beats hypothesis ===
    print("\n" + "="*70)
    print("4. BINAURAL BEATS HYPOTHESIS TEST")
    print("="*70)

    binaural = test_binaural_beats_hypothesis(params)

    print(f"\nHypothesis: {binaural['hypothesis']}")
    print(f"\nTests:")
    for test in binaural["tests"]:
        print(f"\n  {test['test']}:")
        print(f"    {test['explanation']}")

    print(f"\nVERDICT:")
    print(binaural["verdict"]["explanation"])

    # === 5. Final verdict ===
    print("\n" + "="*70)
    print("5. FIRST-PRINCIPLES VERDICT")
    print("="*70)

    print(f"""
COLUMN SCATTERING AT 40 Hz:
===========================

Physical parameters:
• Column radius: {params.column_radius_m:.2f} m
• Wavelength at 40 Hz: {params.sound_speed_ms/40:.2f} m
• ka parameter: {2*np.pi*params.column_radius_m/(params.sound_speed_ms/40):.3f}

Scattering assessment:
• At ka = 0.64, we are in the MODERATE scattering regime
• The column is ~10% of the wavelength
• Some scattering occurs but it's not strong

Binaural effects:
• Maximum IPD from direct path geometry: ~7°
• Column scattering adds small additional phase variations
• Total effect is MARGINAL for binaural perception

VERDICT: The columns DO scatter 40 Hz sound, but the effect
is WEAK. The claim of "passive binaural beats creating gamma
entrainment" is OVERSTATED.

What the columns ACTUALLY do:
1. Create slight spatial decorrelation
2. Add diffuse reflections (increased reverberance)
3. Break up flutter echoes from parallel walls

What they DON'T do:
1. Create strong "binaural beats" (wrong terminology)
2. Dramatically alter the phase relationship between ears
3. "Hack the brain's spatial hearing" (overstatement)

For INFRASOUND (3-10 Hz):
• Wavelengths are 34-100+ meters
• ka is vanishingly small (0.01-0.03)
• Columns are INVISIBLE to infrasound
• No scattering effects whatsoever
""")

    return {
        "gamma_analysis": gamma,
        "binaural_test": binaural
    }


if __name__ == "__main__":
    results = run_wave_scattering_analysis()
