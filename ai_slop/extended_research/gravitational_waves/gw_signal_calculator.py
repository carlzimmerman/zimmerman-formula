#!/usr/bin/env python3
"""
Gravitational Wave Signal Calculator
=====================================
Author: Carl Zimmerman
Date: 2026-04-24

Calculates gravitational wave signals from compact binary mergers
(neutron stars, black holes) using general relativity.

Key equations from Einstein's quadrupole formula and post-Newtonian theory.
"""

import numpy as np
import json
from dataclasses import dataclass
from typing import Tuple, Optional

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

# Fundamental constants (SI units)
G = 6.67430e-11       # Gravitational constant [m³/kg/s²]
c = 2.99792458e8      # Speed of light [m/s]
M_sun = 1.98847e30    # Solar mass [kg]
pc = 3.08567758e16    # Parsec [m]
Mpc = pc * 1e6        # Megaparsec [m]

# Derived constants
G_over_c2 = G / c**2           # [m/kg] - appears in Schwarzschild radius
G_over_c3 = G / c**3           # [s/kg] - appears in GW frequency equations
GM_sun_over_c3 = G * M_sun / c**3  # ~4.926e-6 seconds (geometric time unit)


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class BinarySystem:
    """Represents a compact binary system"""
    m1_solar: float          # Mass 1 in solar masses
    m2_solar: float          # Mass 2 in solar masses
    distance_mpc: float      # Distance in megaparsecs
    name: str = "Binary"     # System name

    def __post_init__(self):
        # Convert to SI
        self.m1 = self.m1_solar * M_sun
        self.m2 = self.m2_solar * M_sun
        self.distance = self.distance_mpc * Mpc

        # Derived quantities
        self.M_total = self.m1 + self.m2
        self.M_total_solar = self.m1_solar + self.m2_solar
        self.mu = (self.m1 * self.m2) / self.M_total  # Reduced mass
        self.eta = self.mu / self.M_total              # Symmetric mass ratio
        self.q = self.m2 / self.m1 if self.m1 >= self.m2 else self.m1 / self.m2  # Mass ratio


@dataclass
class GWSignal:
    """Gravitational wave signal properties"""
    chirp_mass_solar: float
    strain_amplitude: float
    frequency_hz: float
    time_to_merger_s: float
    luminosity_watts: float
    energy_radiated_joules: float
    schwarzschild_radius_m: float
    isco_frequency_hz: float


# =============================================================================
# CORE CALCULATIONS
# =============================================================================

def chirp_mass(m1: float, m2: float) -> float:
    """
    Calculate the chirp mass - the key parameter for GW amplitude

    M_c = (m1 * m2)^(3/5) / (m1 + m2)^(1/5)

    This combination appears because GW emission depends on the
    quadrupole moment's time derivatives.
    """
    return (m1 * m2)**(3/5) / (m1 + m2)**(1/5)


def gw_strain_amplitude(M_c: float, f_gw: float, distance: float) -> float:
    """
    Calculate the dimensionless strain amplitude h

    h = (4/r) * (G*M_c/c²)^(5/3) * (π*f/c)^(2/3)

    This is what LIGO/Virgo measure - the fractional change in
    arm length: ΔL/L = h ~ 10^-21 for typical detections
    """
    term1 = 4.0 / distance
    term2 = (G * M_c / c**2)**(5/3)
    term3 = (np.pi * f_gw / c)**(2/3)
    return term1 * term2 * term3


def time_to_merger(M_c: float, f_gw: float) -> float:
    """
    Time remaining until merger from current GW frequency

    τ = (5/256) * (c⁵/(G*M_c)^(5/3)) * (π*f)^(-8/3)

    As f increases, τ decreases - the "chirp" accelerates
    """
    term1 = 5.0 / 256.0
    term2 = c**5 / (G * M_c)**(5/3)
    term3 = (np.pi * f_gw)**(-8/3)
    return term1 * term2 * term3


def frequency_evolution(M_c: float, f_gw: float) -> float:
    """
    Rate of frequency change df/dt

    df/dt = (96/5) * π^(8/3) * (G*M_c/c³)^(5/3) * f^(11/3)

    This drives the characteristic "chirp" sound
    """
    term1 = 96.0 / 5.0 * np.pi**(8/3)
    term2 = (G * M_c / c**3)**(5/3)
    term3 = f_gw**(11/3)
    return term1 * term2 * term3


def gw_luminosity(M_c: float, f_gw: float) -> float:
    """
    Gravitational wave luminosity (power radiated)

    L = (32/5) * (c⁵/G) * (G*M_c*π*f/c³)^(10/3)

    At merger, this can exceed the luminosity of all stars
    in the observable universe combined!
    """
    c5_over_G = c**5 / G  # ~ 3.6e52 W (Planck luminosity)
    term1 = 32.0 / 5.0 * c5_over_G
    term2 = (G * M_c * np.pi * f_gw / c**3)**(10/3)
    return term1 * term2


def isco_frequency(M_total: float) -> float:
    """
    Innermost Stable Circular Orbit frequency

    f_ISCO = c³ / (6^(3/2) * π * G * M)

    This is approximately where the inspiral ends and merger begins
    (for Schwarzschild, non-spinning case)
    """
    return c**3 / (6**(3/2) * np.pi * G * M_total)


def schwarzschild_radius(M: float) -> float:
    """
    Schwarzschild radius: r_s = 2GM/c²

    For a solar mass: ~3 km
    For GW150914 final BH (~62 M_sun): ~183 km
    """
    return 2 * G * M / c**2


def orbital_separation(M_total: float, f_gw: float) -> float:
    """
    Orbital separation from GW frequency

    f_gw = 2 * f_orbital (quadrupole radiation)
    f_orbital = (1/2π) * sqrt(GM/r³)

    Solving for r: r = (GM / (π*f_gw)²)^(1/3)
    """
    f_orb = f_gw / 2.0
    return (G * M_total / (2 * np.pi * f_orb)**2)**(1/3)


# =============================================================================
# MAIN CALCULATOR
# =============================================================================

def calculate_gw_signal(binary: BinarySystem, f_gw: float) -> GWSignal:
    """
    Calculate all GW signal properties for a binary at given frequency
    """
    M_c = chirp_mass(binary.m1, binary.m2)
    M_c_solar = M_c / M_sun

    h = gw_strain_amplitude(M_c, f_gw, binary.distance)
    tau = time_to_merger(M_c, f_gw)
    L = gw_luminosity(M_c, f_gw)
    f_isco = isco_frequency(binary.M_total)
    r_s = schwarzschild_radius(binary.M_total)

    # Energy radiated (approximate - integrated luminosity)
    # E ~ L * τ (very rough estimate)
    E = L * tau * 0.1  # Factor accounts for non-constant L

    return GWSignal(
        chirp_mass_solar=M_c_solar,
        strain_amplitude=h,
        frequency_hz=f_gw,
        time_to_merger_s=tau,
        luminosity_watts=L,
        energy_radiated_joules=E,
        schwarzschild_radius_m=r_s,
        isco_frequency_hz=f_isco
    )


def generate_waveform(binary: BinarySystem,
                      f_start: float = 20.0,
                      f_end: Optional[float] = None,
                      n_points: int = 1000) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate a simplified inspiral waveform

    Returns: (time, frequency, strain) arrays
    """
    M_c = chirp_mass(binary.m1, binary.m2)

    if f_end is None:
        f_end = isco_frequency(binary.M_total)

    # Time array (backwards from merger)
    tau_start = time_to_merger(M_c, f_start)
    tau_end = time_to_merger(M_c, f_end)

    times = np.linspace(tau_start, max(tau_end, 0.001), n_points)

    # Frequency evolution: f(τ) from inverting τ(f)
    # τ = (5/256) * (c⁵/(G*M_c)^(5/3)) * (π*f)^(-8/3)
    # f = (1/π) * [(256/5) * (G*M_c)^(5/3) / (c⁵ * τ)]^(3/8)

    coeff = (256.0/5.0) * (G * M_c)**(5/3) / c**5
    frequencies = (1.0/np.pi) * (coeff / times)**(3/8)

    # Strain amplitude at each frequency
    strains = np.array([gw_strain_amplitude(M_c, f, binary.distance) for f in frequencies])

    # Convert to time before merger (t = 0 at merger)
    t_before_merger = -times

    return t_before_merger, frequencies, strains


# =============================================================================
# FAMOUS EVENTS
# =============================================================================

FAMOUS_EVENTS = {
    "GW150914": BinarySystem(
        m1_solar=35.6,
        m2_solar=30.6,
        distance_mpc=440,
        name="GW150914 (First Detection)"
    ),
    "GW170817": BinarySystem(
        m1_solar=1.46,
        m2_solar=1.27,
        distance_mpc=40,
        name="GW170817 (Neutron Star Merger)"
    ),
    "GW190521": BinarySystem(
        m1_solar=85,
        m2_solar=66,
        distance_mpc=5300,
        name="GW190521 (Most Massive)"
    ),
    "GW170104": BinarySystem(
        m1_solar=31.2,
        m2_solar=19.4,
        distance_mpc=880,
        name="GW170104"
    ),
}


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================

def format_scientific(value: float, unit: str = "") -> str:
    """Format large/small numbers in scientific notation"""
    if abs(value) < 1e-3 or abs(value) > 1e6:
        return f"{value:.3e} {unit}"
    else:
        return f"{value:.4f} {unit}"


def print_binary_analysis(binary: BinarySystem, frequencies: list = [20, 50, 100, 200]):
    """Print comprehensive analysis of a binary system"""

    print("=" * 70)
    print(f"  GRAVITATIONAL WAVE ANALYSIS: {binary.name}")
    print("=" * 70)

    print(f"\n{'SYSTEM PARAMETERS':=^70}")
    print(f"  Mass 1:              {binary.m1_solar:.2f} M_sun")
    print(f"  Mass 2:              {binary.m2_solar:.2f} M_sun")
    print(f"  Total Mass:          {binary.M_total_solar:.2f} M_sun")
    print(f"  Mass Ratio (q):      {binary.q:.3f}")
    print(f"  Symmetric η:         {binary.eta:.4f}")
    print(f"  Distance:            {binary.distance_mpc:.1f} Mpc ({binary.distance_mpc * 3.26:.1f} Mly)")

    M_c = chirp_mass(binary.m1, binary.m2)
    M_c_solar = M_c / M_sun
    print(f"\n  Chirp Mass:          {M_c_solar:.3f} M_sun")
    print(f"  Schwarzschild R:     {schwarzschild_radius(binary.M_total)/1000:.2f} km")
    print(f"  ISCO Frequency:      {isco_frequency(binary.M_total):.2f} Hz")

    print(f"\n{'SIGNAL AT VARIOUS FREQUENCIES':=^70}")
    print(f"  {'Freq (Hz)':<12} {'Strain h':<14} {'Time to Merge':<18} {'Luminosity':<16}")
    print("-" * 70)

    for f in frequencies:
        signal = calculate_gw_signal(binary, f)

        # Format time
        if signal.time_to_merger_s > 86400:
            time_str = f"{signal.time_to_merger_s/86400:.2f} days"
        elif signal.time_to_merger_s > 3600:
            time_str = f"{signal.time_to_merger_s/3600:.2f} hours"
        elif signal.time_to_merger_s > 60:
            time_str = f"{signal.time_to_merger_s/60:.2f} min"
        else:
            time_str = f"{signal.time_to_merger_s:.3f} s"

        # Format luminosity
        L_sun = 3.828e26  # Solar luminosity in watts
        L_ratio = signal.luminosity_watts / L_sun
        if L_ratio > 1e10:
            lum_str = f"{L_ratio:.2e} L_sun"
        else:
            lum_str = f"{L_ratio:.2e} L_sun"

        print(f"  {f:<12} {signal.strain_amplitude:<14.3e} {time_str:<18} {lum_str:<16}")

    # Peak values at ISCO
    f_isco = isco_frequency(binary.M_total)
    peak_signal = calculate_gw_signal(binary, f_isco)

    print(f"\n{'PEAK VALUES (at ISCO)':=^70}")
    print(f"  Peak Frequency:      {f_isco:.2f} Hz")
    print(f"  Peak Strain:         {peak_signal.strain_amplitude:.3e}")
    print(f"  Peak Luminosity:     {peak_signal.luminosity_watts:.3e} W")
    print(f"                       ({peak_signal.luminosity_watts/3.828e26:.2e} L_sun)")

    # Compare to total stellar output
    # Observable universe: ~10^24 stars, ~10^24 * L_sun total
    universe_luminosity = 1e24 * 3.828e26
    ratio = peak_signal.luminosity_watts / universe_luminosity
    print(f"  vs Universe stars:   {ratio:.1f}x all stars combined!")

    print("=" * 70)


def save_waveform_data(binary: BinarySystem, filename: str):
    """Save waveform data to JSON"""
    t, f, h = generate_waveform(binary)

    data = {
        "system": {
            "name": binary.name,
            "m1_solar": binary.m1_solar,
            "m2_solar": binary.m2_solar,
            "distance_mpc": binary.distance_mpc,
            "chirp_mass_solar": chirp_mass(binary.m1, binary.m2) / M_sun
        },
        "waveform": {
            "time_before_merger_s": t.tolist(),
            "frequency_hz": f.tolist(),
            "strain_amplitude": h.tolist()
        }
    }

    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=2)

    print(f"Saved waveform to {filename}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  GRAVITATIONAL WAVE SIGNAL CALCULATOR")
    print("  Based on Einstein's General Relativity")
    print("=" * 70)

    # Analyze famous events
    for name, binary in FAMOUS_EVENTS.items():
        print_binary_analysis(binary)
        print("\n")

    # Custom binary example
    print("\n" + "=" * 70)
    print("  CUSTOM BINARY EXAMPLE")
    print("=" * 70)

    custom = BinarySystem(
        m1_solar=10.0,
        m2_solar=10.0,
        distance_mpc=100,
        name="Equal Mass 10+10 M_sun"
    )
    print_binary_analysis(custom)

    # Save GW150914 waveform
    save_waveform_data(
        FAMOUS_EVENTS["GW150914"],
        "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/gravitational_waves/gw150914_waveform.json"
    )

    print("\n✓ Calculator complete!")
