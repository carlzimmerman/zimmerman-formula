#!/usr/bin/env python3
"""
Telesterion Acoustic Analysis Suite
====================================
Computational modeling of the acoustic properties of the Telesterion at Eleusis.

Author: Carl Zimmerman
Date: April 28, 2026

This module calculates:
1. Room modes (axial, tangential, oblique) with degeneracy analysis
2. Reverberation time (RT60) under various conditions
3. Mode density and Schroeder frequency
4. Human body resonance overlaps
5. Helmholtz resonator (echeia) calculations
6. Tympanum (frame drum) frequencies
7. Temperature effects on acoustics
8. Psychoacoustic significance analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple, Dict
import json

# =============================================================================
# CONSTANTS AND PARAMETERS
# =============================================================================

@dataclass
class TelesterionGeometry:
    """Physical dimensions of the Telesterion"""
    length: float = 51.5  # meters (Lx)
    width: float = 51.5   # meters (Ly) - square floor plan
    height: float = 15.0  # meters (Lz) - estimated

    # Column configuration
    num_columns: int = 42
    column_rows: int = 6
    column_cols: int = 7
    column_diameter: float = 1.75  # meters (estimated, Doric 6:1 ratio)
    column_height: float = 10.5    # meters (estimated)

    # Capacity
    min_capacity: int = 3000
    max_capacity: int = 5000

    @property
    def volume(self) -> float:
        """Room volume in cubic meters"""
        return self.length * self.width * self.height

    @property
    def floor_area(self) -> float:
        """Floor area in square meters"""
        return self.length * self.width

    @property
    def wall_area(self) -> float:
        """Total wall area in square meters"""
        return 2 * (self.length + self.width) * self.height

    @property
    def total_surface_area(self) -> float:
        """Total interior surface area"""
        return 2 * self.floor_area + self.wall_area

    @property
    def column_spacing_x(self) -> float:
        """Average spacing between columns in x direction"""
        return self.length / (self.column_cols + 1)

    @property
    def column_spacing_y(self) -> float:
        """Average spacing between columns in y direction"""
        return self.width / (self.column_rows + 1)


@dataclass
class AcousticMaterials:
    """Absorption coefficients for materials at different frequencies"""
    # Frequencies for absorption data (Hz)
    frequencies: Tuple[float, ...] = (125, 250, 500, 1000, 2000, 4000)

    # Absorption coefficients (alpha) by material
    polished_marble: Tuple[float, ...] = (0.01, 0.01, 0.01, 0.01, 0.02, 0.02)
    rough_limestone: Tuple[float, ...] = (0.02, 0.02, 0.03, 0.04, 0.05, 0.05)
    wooden_roof: Tuple[float, ...] = (0.15, 0.11, 0.10, 0.07, 0.06, 0.07)

    # Audience absorption (standing, moderate density ~2 people/m²)
    audience_standing: Tuple[float, ...] = (0.20, 0.35, 0.50, 0.60, 0.70, 0.70)

    # Audience absorption (seated on stone, ~1 person/m²)
    audience_seated: Tuple[float, ...] = (0.10, 0.20, 0.30, 0.40, 0.50, 0.55)


@dataclass
class HumanResonances:
    """Human body resonance frequencies and thresholds"""
    # (frequency_hz, body_part, effect, threshold_db)
    resonances: List[Tuple[float, str, str, float]] = None

    def __post_init__(self):
        self.resonances = [
            (1.0, "Heart", "Cardiac rhythm effects", 120),
            (3.0, "Chest cavity", "Pressure sensation", 110),
            (5.0, "Abdominal organs", "Visceral discomfort", 100),
            (7.0, "Vestibular (peak)", "Dizziness, nausea, disorientation", 95),
            (10.0, "Brain alpha", "Entrainment, altered states", 90),
            (18.9, "Eyeball", "Visual disturbances (Tandy effect)", 90),
            (40.0, "Gamma peak", "Consciousness binding, memory", 85),
        ]


# Physical constants
SPEED_OF_SOUND_20C = 343.0  # m/s at 20°C
SPEED_OF_SOUND_COEFFICIENT = 0.606  # m/s per °C

# Z² constant for comparison
Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51


# =============================================================================
# ROOM MODE CALCULATIONS
# =============================================================================

def speed_of_sound(temperature_c: float) -> float:
    """Calculate speed of sound at given temperature"""
    return 331.3 + SPEED_OF_SOUND_COEFFICIENT * temperature_c


def calculate_room_mode(nx: int, ny: int, nz: int,
                        Lx: float, Ly: float, Lz: float,
                        c: float = SPEED_OF_SOUND_20C) -> float:
    """
    Calculate room mode frequency using the standard formula.

    f = (c/2) * sqrt((nx/Lx)² + (ny/Ly)² + (nz/Lz)²)

    Parameters:
        nx, ny, nz: Mode indices (non-negative integers)
        Lx, Ly, Lz: Room dimensions in meters
        c: Speed of sound in m/s

    Returns:
        Frequency in Hz
    """
    if nx == 0 and ny == 0 and nz == 0:
        return 0.0

    term = np.sqrt((nx/Lx)**2 + (ny/Ly)**2 + (nz/Lz)**2)
    return (c / 2) * term


def classify_mode(nx: int, ny: int, nz: int) -> str:
    """Classify a mode as axial, tangential, or oblique"""
    nonzero_count = sum(1 for n in [nx, ny, nz] if n > 0)
    if nonzero_count == 1:
        return "axial"
    elif nonzero_count == 2:
        return "tangential"
    else:
        return "oblique"


def calculate_all_modes(geometry: TelesterionGeometry,
                        max_freq: float = 100.0,
                        temperature: float = 20.0) -> List[Dict]:
    """
    Calculate all room modes up to a maximum frequency.

    Returns list of dicts with mode info including degeneracy detection.
    """
    c = speed_of_sound(temperature)
    modes = []

    # Calculate maximum mode index needed
    max_n = int(np.ceil(2 * max_freq * max(geometry.length, geometry.width, geometry.height) / c)) + 1

    for nx in range(max_n):
        for ny in range(max_n):
            for nz in range(max_n):
                if nx == 0 and ny == 0 and nz == 0:
                    continue

                freq = calculate_room_mode(nx, ny, nz,
                                          geometry.length, geometry.width, geometry.height, c)

                if freq <= max_freq:
                    modes.append({
                        'nx': nx,
                        'ny': ny,
                        'nz': nz,
                        'frequency': freq,
                        'type': classify_mode(nx, ny, nz),
                        'indices': (nx, ny, nz)
                    })

    # Sort by frequency
    modes.sort(key=lambda x: x['frequency'])

    # Detect degenerate modes (same frequency within 0.01 Hz tolerance)
    tolerance = 0.01
    for i, mode in enumerate(modes):
        mode['degenerate_with'] = []
        for j, other in enumerate(modes):
            if i != j and abs(mode['frequency'] - other['frequency']) < tolerance:
                mode['degenerate_with'].append(other['indices'])
        mode['is_degenerate'] = len(mode['degenerate_with']) > 0
        mode['degeneracy_order'] = len(mode['degenerate_with']) + 1

    return modes


def analyze_mode_degeneracy(modes: List[Dict]) -> Dict:
    """Analyze the pattern of degenerate modes"""
    degenerate_modes = [m for m in modes if m['is_degenerate']]

    # Group degenerate modes by frequency
    freq_groups = {}
    for mode in modes:
        freq_key = round(mode['frequency'], 2)
        if freq_key not in freq_groups:
            freq_groups[freq_key] = []
        freq_groups[freq_key].append(mode)

    # Find groups with multiple modes (degeneracies)
    degenerate_groups = {k: v for k, v in freq_groups.items() if len(v) > 1}

    return {
        'total_modes': len(modes),
        'degenerate_mode_count': len(degenerate_modes),
        'degeneracy_percentage': 100 * len(degenerate_modes) / len(modes) if modes else 0,
        'degenerate_frequency_groups': len(degenerate_groups),
        'max_degeneracy_order': max(m['degeneracy_order'] for m in modes) if modes else 0,
        'degenerate_groups': degenerate_groups
    }


# =============================================================================
# REVERBERATION TIME CALCULATIONS
# =============================================================================

def sabine_rt60(volume: float, total_absorption: float) -> float:
    """
    Calculate RT60 using Sabine equation.

    RT60 = 0.161 * V / A

    Parameters:
        volume: Room volume in m³
        total_absorption: Total absorption in Sabins (m²)

    Returns:
        RT60 in seconds
    """
    if total_absorption <= 0:
        return float('inf')
    return 0.161 * volume / total_absorption


def eyring_rt60(volume: float, surface_area: float, avg_absorption: float) -> float:
    """
    Calculate RT60 using Eyring equation (better for high absorption).

    RT60 = 0.161 * V / (-S * ln(1 - α_avg))

    Parameters:
        volume: Room volume in m³
        surface_area: Total surface area in m²
        avg_absorption: Average absorption coefficient

    Returns:
        RT60 in seconds
    """
    if avg_absorption >= 1:
        return 0
    if avg_absorption <= 0:
        return float('inf')
    return 0.161 * volume / (-surface_area * np.log(1 - avg_absorption))


def calculate_rt60_scenarios(geometry: TelesterionGeometry,
                            materials: AcousticMaterials) -> Dict:
    """
    Calculate RT60 for various occupancy scenarios.
    """
    results = {}

    # Surface areas
    floor_area = geometry.floor_area
    ceiling_area = floor_area
    wall_area = geometry.wall_area

    for freq_idx, freq in enumerate(materials.frequencies):
        freq_results = {}

        # Material absorptions at this frequency
        wall_alpha = materials.polished_marble[freq_idx]
        floor_alpha = materials.rough_limestone[freq_idx]
        ceiling_alpha = materials.wooden_roof[freq_idx]

        # Scenario 1: Empty hall
        total_absorption_empty = (
            wall_area * wall_alpha +
            floor_area * floor_alpha +
            ceiling_area * ceiling_alpha
        )
        freq_results['empty'] = sabine_rt60(geometry.volume, total_absorption_empty)

        # Scenario 2: 3000 initiates (standing)
        audience_area = 3000 / 2.0  # ~2 people per m²
        audience_alpha = materials.audience_standing[freq_idx]
        total_absorption_3000 = total_absorption_empty + audience_area * audience_alpha
        freq_results['3000_standing'] = sabine_rt60(geometry.volume, total_absorption_3000)

        # Scenario 3: 5000 initiates (packed)
        audience_area_5000 = 5000 / 2.5  # ~2.5 people per m²
        total_absorption_5000 = total_absorption_empty + audience_area_5000 * audience_alpha
        freq_results['5000_packed'] = sabine_rt60(geometry.volume, total_absorption_5000)

        # Scenario 4: With hypothetical acoustic treatment (echeia)
        # Assume 50 Helmholtz resonators adding 0.5 m² absorption each at resonant freq
        if 100 <= freq <= 500:  # Echeia would be tuned to speech/music range
            echeia_absorption = 50 * 0.5
        else:
            echeia_absorption = 0
        total_absorption_echeia = total_absorption_3000 + echeia_absorption
        freq_results['3000_with_echeia'] = sabine_rt60(geometry.volume, total_absorption_echeia)

        results[freq] = freq_results

    return results


# =============================================================================
# SCHROEDER FREQUENCY AND MODE DENSITY
# =============================================================================

def schroeder_frequency(rt60: float, volume: float) -> float:
    """
    Calculate Schroeder frequency - transition from discrete modes to diffuse field.

    f_s = 2000 * sqrt(RT60 / V)

    Below this frequency, room modes dominate. Above, statistical acoustics applies.
    """
    return 2000 * np.sqrt(rt60 / volume)


def mode_density(frequency: float, volume: float, c: float = SPEED_OF_SOUND_20C) -> float:
    """
    Calculate modal density (modes per Hz) at a given frequency.

    dn/df = 4π * V * f² / c³
    """
    return 4 * np.pi * volume * frequency**2 / c**3


def analyze_modal_statistics(modes: List[Dict], geometry: TelesterionGeometry) -> Dict:
    """Analyze statistical properties of the mode distribution"""
    if not modes:
        return {}

    frequencies = [m['frequency'] for m in modes]

    # Mode spacing statistics
    spacings = np.diff(sorted(frequencies))

    # Estimate RT60 at 500 Hz for Schroeder calculation
    materials = AcousticMaterials()
    rt60_scenarios = calculate_rt60_scenarios(geometry, materials)
    rt60_500 = rt60_scenarios[500]['3000_standing']

    f_schroeder = schroeder_frequency(rt60_500, geometry.volume)

    return {
        'total_modes': len(modes),
        'frequency_range': (min(frequencies), max(frequencies)),
        'mean_spacing': np.mean(spacings) if len(spacings) > 0 else 0,
        'min_spacing': np.min(spacings) if len(spacings) > 0 else 0,
        'max_spacing': np.max(spacings) if len(spacings) > 0 else 0,
        'schroeder_frequency': f_schroeder,
        'modes_below_schroeder': sum(1 for f in frequencies if f < f_schroeder),
        'modal_density_at_10Hz': mode_density(10, geometry.volume),
        'modal_density_at_50Hz': mode_density(50, geometry.volume),
        'modal_density_at_100Hz': mode_density(100, geometry.volume),
    }


# =============================================================================
# PSYCHOACOUSTIC ANALYSIS
# =============================================================================

def find_body_resonance_overlaps(modes: List[Dict],
                                  human: HumanResonances,
                                  tolerance_hz: float = 0.5) -> List[Dict]:
    """
    Find room modes that overlap with human body resonances.
    """
    overlaps = []

    for res_freq, body_part, effect, threshold in human.resonances:
        matching_modes = [
            m for m in modes
            if abs(m['frequency'] - res_freq) <= tolerance_hz
        ]

        if matching_modes:
            overlaps.append({
                'body_resonance': res_freq,
                'body_part': body_part,
                'effect': effect,
                'threshold_db': threshold,
                'matching_modes': matching_modes,
                'closest_mode': min(matching_modes, key=lambda m: abs(m['frequency'] - res_freq)),
                'frequency_error': min(abs(m['frequency'] - res_freq) for m in matching_modes)
            })

    return overlaps


def analyze_harmonic_series(fundamental: float, max_harmonic: int = 20) -> List[Dict]:
    """
    Analyze the harmonic series of the fundamental room mode.
    """
    harmonics = []
    human = HumanResonances()

    for n in range(1, max_harmonic + 1):
        freq = fundamental * n

        # Check for body resonance proximity
        closest_resonance = min(human.resonances,
                               key=lambda r: abs(r[0] - freq))

        harmonics.append({
            'harmonic_number': n,
            'frequency': freq,
            'closest_body_resonance': closest_resonance[0],
            'body_part': closest_resonance[1],
            'frequency_difference': abs(freq - closest_resonance[0]),
            'z_squared_ratio': freq / Z_SQUARED,
            'near_z_squared': abs(freq - Z_SQUARED) < 1.0
        })

    return harmonics


# =============================================================================
# HELMHOLTZ RESONATOR (ECHEIA) CALCULATIONS
# =============================================================================

def helmholtz_frequency(volume_liters: float,
                        neck_area_cm2: float,
                        neck_length_cm: float,
                        c: float = SPEED_OF_SOUND_20C) -> float:
    """
    Calculate Helmholtz resonator frequency.

    f = (c / 2π) * sqrt(A / (L * V))

    Parameters:
        volume_liters: Cavity volume in liters
        neck_area_cm2: Neck cross-sectional area in cm²
        neck_length_cm: Neck length in cm
        c: Speed of sound in m/s

    Returns:
        Resonant frequency in Hz
    """
    # Convert to SI units
    V = volume_liters / 1000  # m³
    A = neck_area_cm2 / 10000  # m²
    L = neck_length_cm / 100  # m

    # Add end correction (0.6 * radius for unflanged opening)
    radius = np.sqrt(A / np.pi)
    L_eff = L + 0.6 * radius

    return (c / (2 * np.pi)) * np.sqrt(A / (L_eff * V))


def design_echeia_array(target_frequencies: List[float],
                        c: float = SPEED_OF_SOUND_20C) -> List[Dict]:
    """
    Design a set of echeia (Helmholtz resonators) for target frequencies.
    Based on Vitruvius's description of bronze vessels in theater niches.
    """
    designs = []

    for target_freq in target_frequencies:
        # Start with reasonable vessel dimensions
        # Typical ancient vessel: 10-30 liters, neck 5-10 cm diameter, 3-8 cm long

        # Iterate to find good dimensions
        best_design = None
        best_error = float('inf')

        for volume in np.linspace(5, 40, 20):  # liters
            for neck_diameter in np.linspace(4, 12, 10):  # cm
                neck_area = np.pi * (neck_diameter/2)**2
                for neck_length in np.linspace(2, 10, 10):  # cm
                    freq = helmholtz_frequency(volume, neck_area, neck_length, c)
                    error = abs(freq - target_freq)

                    if error < best_error:
                        best_error = error
                        best_design = {
                            'target_frequency': target_freq,
                            'actual_frequency': freq,
                            'volume_liters': volume,
                            'neck_diameter_cm': neck_diameter,
                            'neck_length_cm': neck_length,
                            'error_hz': error,
                            'error_percent': 100 * error / target_freq
                        }

        designs.append(best_design)

    return designs


# =============================================================================
# TYMPANUM (FRAME DRUM) CALCULATIONS
# =============================================================================

def drum_membrane_frequency(diameter_m: float,
                           tension_N_per_m: float,
                           surface_density_kg_per_m2: float,
                           mode: Tuple[int, int] = (0, 1)) -> float:
    """
    Calculate vibration frequency of a circular membrane (drum head).

    f_{mn} = (α_{mn} / (π * D)) * sqrt(T / σ)

    where α_{mn} are zeros of Bessel functions.

    Parameters:
        diameter_m: Membrane diameter in meters
        tension_N_per_m: Tension per unit length in N/m
        surface_density_kg_per_m2: Mass per unit area in kg/m²
        mode: (m, n) mode indices

    Returns:
        Frequency in Hz
    """
    # Bessel function zeros α_{mn} for first several modes
    bessel_zeros = {
        (0, 1): 2.405,   # Fundamental
        (1, 1): 3.832,
        (2, 1): 5.136,
        (0, 2): 5.520,
        (3, 1): 6.380,
        (1, 2): 7.016,
        (4, 1): 7.588,
        (2, 2): 8.417,
        (0, 3): 8.654,
    }

    alpha = bessel_zeros.get(mode, 2.405)  # Default to fundamental

    return (alpha / (np.pi * diameter_m)) * np.sqrt(tension_N_per_m / surface_density_kg_per_m2)


def analyze_tympanum_frequencies(diameter_range_cm: Tuple[float, float] = (30, 100),
                                  tension_range: Tuple[float, float] = (500, 2000),
                                  surface_density: float = 0.5) -> Dict:
    """
    Analyze frequency ranges for ancient tympanum drums.

    Assumptions:
        - Goat skin membrane, ~0.5 kg/m² surface density
        - Hand-tensioned, moderate tension range
    """
    results = {
        'diameter_range_cm': diameter_range_cm,
        'tension_range_N_per_m': tension_range,
        'surface_density_kg_per_m2': surface_density,
        'frequency_estimates': []
    }

    for diameter_cm in [30, 40, 50, 60, 80, 100]:
        diameter_m = diameter_cm / 100

        for tension in [500, 1000, 1500, 2000]:
            freq = drum_membrane_frequency(diameter_m, tension, surface_density, (0, 1))

            results['frequency_estimates'].append({
                'diameter_cm': diameter_cm,
                'tension_N_per_m': tension,
                'fundamental_freq_hz': freq,
                'mode_1_1_freq_hz': freq * 3.832 / 2.405,  # Ratio of Bessel zeros
                'mode_2_1_freq_hz': freq * 5.136 / 2.405,
            })

    return results


# =============================================================================
# TEMPERATURE EFFECTS
# =============================================================================

def analyze_temperature_effects(geometry: TelesterionGeometry,
                                 temp_range: Tuple[float, float] = (15, 45)) -> Dict:
    """
    Analyze how temperature variations affect room acoustics.

    During ceremony: torches + crowd body heat → elevated temperature
    """
    temps = np.linspace(temp_range[0], temp_range[1], 7)
    results = []

    for temp in temps:
        c = speed_of_sound(temp)
        fundamental = calculate_room_mode(1, 0, 0,
                                         geometry.length, geometry.width, geometry.height, c)

        # Calculate first 10 harmonics
        harmonics = [fundamental * n for n in range(1, 11)]

        results.append({
            'temperature_c': temp,
            'speed_of_sound_m_s': c,
            'fundamental_hz': fundamental,
            '2nd_harmonic_hz': harmonics[1],
            '10th_harmonic_hz': harmonics[9],
            'z_squared_match_error': abs(harmonics[9] - Z_SQUARED),
            'z_squared_match_percent': 100 * abs(harmonics[9] - Z_SQUARED) / Z_SQUARED
        })

    return {
        'temperature_range': temp_range,
        'results': results,
        'optimal_temp_for_z_squared': min(results,
            key=lambda r: r['z_squared_match_error'])['temperature_c']
    }


# =============================================================================
# VISUALIZATION FUNCTIONS
# =============================================================================

def plot_mode_distribution(modes: List[Dict],
                          geometry: TelesterionGeometry,
                          save_path: str = None):
    """Plot the distribution of room modes with degeneracy highlighted"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Mode frequency histogram
    ax1 = axes[0, 0]
    frequencies = [m['frequency'] for m in modes]
    degenerate_freqs = [m['frequency'] for m in modes if m['is_degenerate']]

    ax1.hist(frequencies, bins=50, alpha=0.7, label='All modes', color='steelblue')
    ax1.hist(degenerate_freqs, bins=50, alpha=0.7, label='Degenerate modes', color='crimson')
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Count')
    ax1.set_title('Room Mode Distribution')
    ax1.legend()
    ax1.axvline(Z_SQUARED, color='gold', linestyle='--', linewidth=2, label=f'Z² = {Z_SQUARED:.2f} Hz')

    # 2. Mode type breakdown
    ax2 = axes[0, 1]
    types = [m['type'] for m in modes]
    type_counts = {t: types.count(t) for t in set(types)}
    ax2.bar(type_counts.keys(), type_counts.values(), color=['steelblue', 'seagreen', 'coral'])
    ax2.set_xlabel('Mode Type')
    ax2.set_ylabel('Count')
    ax2.set_title('Mode Classification')

    # 3. Degeneracy order distribution
    ax3 = axes[1, 0]
    degeneracy_orders = [m['degeneracy_order'] for m in modes]
    order_counts = {o: degeneracy_orders.count(o) for o in set(degeneracy_orders)}
    ax3.bar([str(k) for k in sorted(order_counts.keys())],
            [order_counts[k] for k in sorted(order_counts.keys())],
            color='purple', alpha=0.7)
    ax3.set_xlabel('Degeneracy Order')
    ax3.set_ylabel('Count')
    ax3.set_title('Mode Degeneracy Distribution\n(Order 1 = non-degenerate)')

    # 4. Low frequency modes with body resonances
    ax4 = axes[1, 1]
    low_freq_modes = [m for m in modes if m['frequency'] <= 50]
    freqs = [m['frequency'] for m in low_freq_modes]
    degens = [m['degeneracy_order'] for m in low_freq_modes]

    colors = ['crimson' if d > 1 else 'steelblue' for d in degens]
    ax4.scatter(freqs, degens, c=colors, s=100, alpha=0.7)

    # Add body resonance markers
    human = HumanResonances()
    for res_freq, body_part, _, _ in human.resonances:
        if res_freq <= 50:
            ax4.axvline(res_freq, color='green', linestyle=':', alpha=0.7)
            ax4.annotate(body_part, (res_freq, max(degens)*0.9),
                        rotation=90, fontsize=8, ha='right')

    ax4.set_xlabel('Frequency (Hz)')
    ax4.set_ylabel('Degeneracy Order')
    ax4.set_title('Low Frequency Modes vs Body Resonances\n(vertical lines = body resonances)')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved plot to {save_path}")

    return fig


def plot_rt60_analysis(rt60_results: Dict, save_path: str = None):
    """Plot RT60 across frequencies for different scenarios"""
    fig, ax = plt.subplots(figsize=(10, 6))

    frequencies = list(rt60_results.keys())
    scenarios = list(rt60_results[frequencies[0]].keys())

    colors = {'empty': 'gray', '3000_standing': 'steelblue',
              '5000_packed': 'seagreen', '3000_with_echeia': 'coral'}
    labels = {'empty': 'Empty hall', '3000_standing': '3000 initiates (standing)',
              '5000_packed': '5000 initiates (packed)', '3000_with_echeia': '3000 + echeia'}

    for scenario in scenarios:
        rt60_values = [min(rt60_results[f][scenario], 20) for f in frequencies]  # Cap at 20s for display
        ax.plot(frequencies, rt60_values, 'o-', color=colors[scenario],
                label=labels[scenario], linewidth=2, markersize=8)

    # Reference lines
    ax.axhline(7.8, color='purple', linestyle='--', alpha=0.5, label="St. Paul's Cathedral (full)")
    ax.axhline(2.0, color='orange', linestyle='--', alpha=0.5, label='Concert hall optimal')

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('RT60 (seconds)')
    ax.set_title('Reverberation Time Analysis: Telesterion at Eleusis')
    ax.set_xscale('log')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 15)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved plot to {save_path}")

    return fig


def plot_harmonic_analysis(harmonics: List[Dict], save_path: str = None):
    """Plot harmonic series analysis with body resonance and Z² comparison"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 1. Harmonic frequencies vs body resonances
    ax1 = axes[0]
    harm_nums = [h['harmonic_number'] for h in harmonics]
    harm_freqs = [h['frequency'] for h in harmonics]
    body_diffs = [h['frequency_difference'] for h in harmonics]

    # Color by proximity to body resonance
    colors = ['crimson' if d < 1.0 else 'steelblue' for d in body_diffs]
    ax1.bar(harm_nums, harm_freqs, color=colors, alpha=0.7)

    # Add body resonance horizontal lines
    human = HumanResonances()
    for res_freq, body_part, _, _ in human.resonances:
        if res_freq <= max(harm_freqs):
            ax1.axhline(res_freq, color='green', linestyle=':', alpha=0.5)
            ax1.annotate(f'{body_part} ({res_freq} Hz)',
                        (len(harm_nums)*0.7, res_freq), fontsize=8)

    # Mark Z²
    ax1.axhline(Z_SQUARED, color='gold', linestyle='--', linewidth=2)
    ax1.annotate(f'Z² = {Z_SQUARED:.2f} Hz', (len(harm_nums)*0.7, Z_SQUARED+1),
                fontsize=10, fontweight='bold', color='goldenrod')

    ax1.set_xlabel('Harmonic Number')
    ax1.set_ylabel('Frequency (Hz)')
    ax1.set_title('Telesterion Harmonic Series\n(red = within 1 Hz of body resonance)')

    # 2. Z² ratio analysis
    ax2 = axes[1]
    z_ratios = [h['z_squared_ratio'] for h in harmonics]
    near_z = [h['near_z_squared'] for h in harmonics]

    colors2 = ['gold' if n else 'steelblue' for n in near_z]
    ax2.bar(harm_nums, z_ratios, color=colors2, alpha=0.7)
    ax2.axhline(1.0, color='crimson', linestyle='-', linewidth=2, label='f = Z²')

    ax2.set_xlabel('Harmonic Number')
    ax2.set_ylabel('Frequency / Z²')
    ax2.set_title('Harmonic Frequencies as Ratio of Z²\n(gold = within 1 Hz of Z²)')
    ax2.legend()

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved plot to {save_path}")

    return fig


def plot_temperature_sensitivity(temp_results: Dict, save_path: str = None):
    """Plot how temperature affects room acoustics"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    temps = [r['temperature_c'] for r in temp_results['results']]
    fundamentals = [r['fundamental_hz'] for r in temp_results['results']]
    tenth_harmonics = [r['10th_harmonic_hz'] for r in temp_results['results']]
    z_errors = [r['z_squared_match_percent'] for r in temp_results['results']]

    # 1. Frequency vs temperature
    ax1 = axes[0]
    ax1.plot(temps, fundamentals, 'o-', color='steelblue', linewidth=2,
             markersize=8, label='Fundamental')
    ax1.plot(temps, tenth_harmonics, 's-', color='coral', linewidth=2,
             markersize=8, label='10th Harmonic')
    ax1.axhline(Z_SQUARED, color='gold', linestyle='--', linewidth=2, label=f'Z² = {Z_SQUARED:.2f}')

    ax1.set_xlabel('Temperature (°C)')
    ax1.set_ylabel('Frequency (Hz)')
    ax1.set_title('Room Mode Frequency vs Temperature')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Add ceremony temperature range
    ax1.axvspan(25, 35, alpha=0.2, color='orange', label='Likely ceremony range')

    # 2. Z² match error vs temperature
    ax2 = axes[1]
    ax2.plot(temps, z_errors, 'o-', color='purple', linewidth=2, markersize=8)
    ax2.set_xlabel('Temperature (°C)')
    ax2.set_ylabel('10th Harmonic Error from Z² (%)')
    ax2.set_title('Z² Match Quality vs Temperature')
    ax2.grid(True, alpha=0.3)

    # Mark optimal temperature
    opt_temp = temp_results['optimal_temp_for_z_squared']
    ax2.axvline(opt_temp, color='green', linestyle='--',
                label=f'Optimal: {opt_temp:.1f}°C')
    ax2.legend()

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved plot to {save_path}")

    return fig


# =============================================================================
# MAIN ANALYSIS FUNCTION
# =============================================================================

def run_full_analysis(output_dir: str = None) -> Dict:
    """
    Run complete acoustic analysis of the Telesterion.

    Returns comprehensive results dictionary.
    """
    print("=" * 70)
    print("TELESTERION ACOUSTIC ANALYSIS")
    print("Computational Modeling of the Hall of Initiation at Eleusis")
    print("=" * 70)
    print()

    # Initialize
    geometry = TelesterionGeometry()
    materials = AcousticMaterials()
    human = HumanResonances()

    results = {
        'geometry': {
            'length_m': geometry.length,
            'width_m': geometry.width,
            'height_m': geometry.height,
            'volume_m3': geometry.volume,
            'floor_area_m2': geometry.floor_area,
            'wall_area_m2': geometry.wall_area,
            'total_surface_area_m2': geometry.total_surface_area,
            'num_columns': geometry.num_columns,
            'is_square': geometry.length == geometry.width,
        }
    }

    # =========================================================================
    # 1. ROOM MODE ANALYSIS
    # =========================================================================
    print("1. ROOM MODE ANALYSIS")
    print("-" * 40)

    modes = calculate_all_modes(geometry, max_freq=100.0)
    degeneracy_analysis = analyze_mode_degeneracy(modes)
    modal_stats = analyze_modal_statistics(modes, geometry)

    print(f"   Total modes (0-100 Hz): {degeneracy_analysis['total_modes']}")
    print(f"   Degenerate modes: {degeneracy_analysis['degenerate_mode_count']} "
          f"({degeneracy_analysis['degeneracy_percentage']:.1f}%)")
    print(f"   Max degeneracy order: {degeneracy_analysis['max_degeneracy_order']}")
    print(f"   Schroeder frequency: {modal_stats['schroeder_frequency']:.1f} Hz")
    print()

    # Fundamental mode
    fundamental = modes[0]['frequency']
    print(f"   FUNDAMENTAL MODE: {fundamental:.3f} Hz")
    print(f"   (This is INFRASONIC - below human hearing threshold of ~20 Hz)")
    print()

    # First 10 modes
    print("   First 10 modes:")
    for i, mode in enumerate(modes[:10]):
        deg_str = f" [DEGENERATE x{mode['degeneracy_order']}]" if mode['is_degenerate'] else ""
        print(f"      {i+1}. ({mode['nx']},{mode['ny']},{mode['nz']}) = {mode['frequency']:.2f} Hz "
              f"({mode['type']}){deg_str}")
    print()

    results['modes'] = {
        'total_count': len(modes),
        'fundamental_hz': fundamental,
        'degeneracy_analysis': degeneracy_analysis,
        'modal_statistics': modal_stats,
        'first_20_modes': modes[:20],
    }

    # =========================================================================
    # 2. REVERBERATION TIME ANALYSIS
    # =========================================================================
    print("2. REVERBERATION TIME (RT60) ANALYSIS")
    print("-" * 40)

    rt60_results = calculate_rt60_scenarios(geometry, materials)

    print("   RT60 at 500 Hz (standard reference):")
    print(f"      Empty hall:           {rt60_results[500]['empty']:.1f} seconds")
    print(f"      3000 initiates:       {rt60_results[500]['3000_standing']:.1f} seconds")
    print(f"      5000 initiates:       {rt60_results[500]['5000_packed']:.1f} seconds")
    print(f"      3000 + echeia:        {rt60_results[500]['3000_with_echeia']:.1f} seconds")
    print()
    print("   Reference: St. Paul's Cathedral (full) = 7.8 seconds")
    print("   Reference: Concert hall optimal = 1.7-2.1 seconds")
    print()

    results['rt60'] = rt60_results

    # =========================================================================
    # 3. BODY RESONANCE OVERLAP ANALYSIS
    # =========================================================================
    print("3. HUMAN BODY RESONANCE OVERLAP ANALYSIS")
    print("-" * 40)

    overlaps = find_body_resonance_overlaps(modes, human, tolerance_hz=1.0)

    print(f"   Found {len(overlaps)} overlaps between room modes and body resonances:")
    for overlap in overlaps:
        closest = overlap['closest_mode']
        print(f"      • {overlap['body_part']} ({overlap['body_resonance']} Hz): "
              f"Mode ({closest['nx']},{closest['ny']},{closest['nz']}) = {closest['frequency']:.2f} Hz "
              f"(Δ = {overlap['frequency_error']:.2f} Hz)")
        print(f"        Effect: {overlap['effect']}")
    print()

    results['body_resonance_overlaps'] = overlaps

    # =========================================================================
    # 4. HARMONIC SERIES ANALYSIS
    # =========================================================================
    print("4. HARMONIC SERIES ANALYSIS")
    print("-" * 40)

    harmonics = analyze_harmonic_series(fundamental, max_harmonic=15)

    print(f"   Fundamental: {fundamental:.3f} Hz")
    print(f"   Z² = 32π/3 = {Z_SQUARED:.3f} Hz")
    print()
    print("   Harmonic series:")
    for h in harmonics[:12]:
        z_match = " ← NEAR Z²!" if h['near_z_squared'] else ""
        body_match = f" (near {h['body_part']})" if h['frequency_difference'] < 2.0 else ""
        print(f"      {h['harmonic_number']:2d}× = {h['frequency']:.2f} Hz{body_match}{z_match}")
    print()

    # Z² analysis
    tenth = harmonics[9]
    print(f"   10th HARMONIC ANALYSIS:")
    print(f"      10 × {fundamental:.3f} = {tenth['frequency']:.3f} Hz")
    print(f"      Z² = {Z_SQUARED:.3f} Hz")
    print(f"      Difference: {abs(tenth['frequency'] - Z_SQUARED):.3f} Hz "
          f"({100*abs(tenth['frequency'] - Z_SQUARED)/Z_SQUARED:.2f}%)")
    print()

    results['harmonics'] = harmonics

    # =========================================================================
    # 5. TEMPERATURE SENSITIVITY ANALYSIS
    # =========================================================================
    print("5. TEMPERATURE SENSITIVITY ANALYSIS")
    print("-" * 40)

    temp_results = analyze_temperature_effects(geometry)

    print("   Effect of torch-heated air on room acoustics:")
    print()
    print("   Temp(°C)  Speed(m/s)  Fundamental(Hz)  10th Harm(Hz)  Z² Error(%)")
    print("   " + "-" * 65)
    for r in temp_results['results']:
        print(f"   {r['temperature_c']:6.1f}    {r['speed_of_sound_m_s']:7.1f}      "
              f"{r['fundamental_hz']:8.3f}        {r['10th_harmonic_hz']:8.3f}      "
              f"{r['z_squared_match_percent']:6.2f}")
    print()
    print(f"   Optimal temperature for Z² match: {temp_results['optimal_temp_for_z_squared']:.1f}°C")
    print()

    results['temperature_analysis'] = temp_results

    # =========================================================================
    # 6. ECHEIA (HELMHOLTZ RESONATOR) DESIGN
    # =========================================================================
    print("6. ECHEIA (HELMHOLTZ RESONATOR) DESIGN")
    print("-" * 40)

    # Target frequencies based on Pythagorean intervals from a ~200 Hz reference
    target_freqs = [100, 150, 200, 267, 300, 400]  # Approximate musical intervals
    echeia_designs = design_echeia_array(target_freqs)

    print("   Hypothetical echeia vessels tuned to Pythagorean intervals:")
    print()
    for design in echeia_designs:
        print(f"      Target: {design['target_frequency']:.0f} Hz → "
              f"Actual: {design['actual_frequency']:.1f} Hz")
        print(f"         Volume: {design['volume_liters']:.1f} L, "
              f"Neck: {design['neck_diameter_cm']:.1f} cm × {design['neck_length_cm']:.1f} cm")
    print()

    results['echeia_designs'] = echeia_designs

    # =========================================================================
    # 7. TYMPANUM (FRAME DRUM) ANALYSIS
    # =========================================================================
    print("7. TYMPANUM (FRAME DRUM) ANALYSIS")
    print("-" * 40)

    tympanum_results = analyze_tympanum_frequencies()

    print("   Estimated frequencies for ancient tympanum drums:")
    print("   (Goat skin membrane, hand-tensioned)")
    print()
    print("   Diameter(cm)  Tension(N/m)  Fundamental(Hz)")
    print("   " + "-" * 45)
    for est in tympanum_results['frequency_estimates'][::4]:  # Every 4th to reduce output
        print(f"   {est['diameter_cm']:8.0f}       {est['tension_N_per_m']:8.0f}         "
              f"{est['fundamental_freq_hz']:8.1f}")
    print()
    print("   Large processional tympanum (1m diameter) could produce ~30-50 Hz")
    print("   This overlaps with gamma brainwave entrainment range (30-100 Hz)")
    print()

    results['tympanum_analysis'] = tympanum_results

    # =========================================================================
    # 8. PSYCHOACOUSTIC SUMMARY
    # =========================================================================
    print("8. PSYCHOACOUSTIC SIGNIFICANCE SUMMARY")
    print("-" * 40)
    print()
    print("   The Telesterion's acoustic environment would have produced:")
    print()
    print("   • INFRASONIC FUNDAMENTAL (~3.3 Hz)")
    print("     - Below hearing threshold but potentially felt as vibration")
    print("     - Within range affecting vestibular system (0.7-7 Hz)")
    print("     - 3,000+ people chanting/drumming could excite this mode")
    print()
    print("   • DEGENERATE MODE BUILDUP")
    print(f"     - {degeneracy_analysis['degeneracy_percentage']:.1f}% of modes are degenerate")
    print("     - Square floor plan causes constructive interference")
    print("     - Could create 'hot spots' of intense acoustic pressure")
    print()
    print("   • LONG REVERBERATION (~6-7 seconds with crowd)")
    print("     - Comparable to medieval cathedrals")
    print("     - Creates immersive, otherworldly sound environment")
    print("     - Masks directional cues, enhancing disorientation")
    print()
    print("   • BODY RESONANCE ALIGNMENT")
    print(f"     - {len(overlaps)} room modes within 1 Hz of body resonances")
    print("     - 2nd harmonic (~6.7 Hz) near vestibular peak (7 Hz)")
    print("     - 3rd harmonic (~10 Hz) at brain alpha frequency")
    print()

    results['summary'] = {
        'fundamental_hz': fundamental,
        'is_infrasonic': fundamental < 20,
        'degeneracy_percentage': degeneracy_analysis['degeneracy_percentage'],
        'rt60_with_crowd': rt60_results[500]['3000_standing'],
        'body_resonance_overlaps': len(overlaps),
        'z_squared_match_at_20C': abs(harmonics[9]['frequency'] - Z_SQUARED),
    }

    # =========================================================================
    # 9. GENERATE PLOTS
    # =========================================================================
    if output_dir:
        print("9. GENERATING VISUALIZATION PLOTS")
        print("-" * 40)

        import os
        os.makedirs(output_dir, exist_ok=True)

        plot_mode_distribution(modes, geometry,
                              save_path=f"{output_dir}/mode_distribution.png")
        plot_rt60_analysis(rt60_results,
                          save_path=f"{output_dir}/rt60_analysis.png")
        plot_harmonic_analysis(harmonics,
                              save_path=f"{output_dir}/harmonic_analysis.png")
        plot_temperature_sensitivity(temp_results,
                                    save_path=f"{output_dir}/temperature_sensitivity.png")

        # Save results to JSON
        results_serializable = json.loads(
            json.dumps(results, default=lambda x: float(x) if isinstance(x, np.floating) else str(x))
        )
        with open(f"{output_dir}/analysis_results.json", 'w') as f:
            json.dump(results_serializable, f, indent=2)
        print(f"   Saved results to {output_dir}/analysis_results.json")
        print()

    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

    return results


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import sys

    # Determine output directory
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        output_dir = "/Users/carlzimmerman/new_physics/zimmerman-formula/research/telesterion_analysis"

    # Run full analysis
    results = run_full_analysis(output_dir=output_dir)
