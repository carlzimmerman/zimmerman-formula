#!/usr/bin/env python3
"""
Black Hole Physics Calculator with Z² Framework Connections
============================================================

Comprehensive calculations for black hole thermodynamics, showing
how the Z² = 32π/3 framework connects to Hawking radiation,
Bekenstein-Hawking entropy, and black hole mechanics.

Carl Zimmerman | May 2026
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple

# =============================================================================
# PHYSICAL CONSTANTS (SI Units)
# =============================================================================

# Fundamental constants
c = 2.998e8        # Speed of light (m/s)
G = 6.674e-11      # Gravitational constant (m³ kg⁻¹ s⁻²)
hbar = 1.055e-34   # Reduced Planck constant (J·s)
k_B = 1.381e-23    # Boltzmann constant (J/K)
sigma_SB = 5.670e-8  # Stefan-Boltzmann constant (W m⁻² K⁻⁴)

# Derived constants
M_sun = 1.989e30   # Solar mass (kg)
l_P = np.sqrt(G * hbar / c**3)  # Planck length (m)
M_P = np.sqrt(hbar * c / G)     # Planck mass (kg)
t_P = np.sqrt(G * hbar / c**5)  # Planck time (s)
T_P = np.sqrt(hbar * c**5 / (G * k_B**2))  # Planck temperature (K)

# Time units
year_s = 3.156e7   # Seconds per year
Gyr_s = 3.156e16   # Seconds per Gyr

# =============================================================================
# Z² FRAMEWORK CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3      # = 33.510321
Z = np.sqrt(Z_SQUARED)          # = 5.788943
BEKENSTEIN = 3 * Z_SQUARED / (8 * np.pi)  # = 4.0 exactly
OMEGA_LAMBDA = 13 / 19          # = 0.6842
OMEGA_M = 6 / 19                # = 0.3158


@dataclass
class BlackHole:
    """Black hole properties"""
    mass_kg: float
    spin_a: float = 0.0  # Spin parameter (0 to 1)
    charge: float = 0.0  # Charge (usually 0)

    @property
    def mass_solar(self) -> float:
        return self.mass_kg / M_sun

    @property
    def schwarzschild_radius(self) -> float:
        """Schwarzschild radius r_s = 2GM/c² (m)"""
        return 2 * G * self.mass_kg / c**2

    @property
    def horizon_area(self) -> float:
        """Event horizon area A = 4πr_s² (m²)"""
        r_s = self.schwarzschild_radius
        return 4 * np.pi * r_s**2

    @property
    def surface_gravity(self) -> float:
        """Surface gravity κ = c⁴/(4GM) (m/s²)"""
        return c**4 / (4 * G * self.mass_kg)


# =============================================================================
# HAWKING TEMPERATURE
# =============================================================================

def hawking_temperature(mass_kg: float) -> float:
    """
    Calculate Hawking temperature for a Schwarzschild black hole.

    T_H = ℏc³ / (8πGMk_B)

    Args:
        mass_kg: Black hole mass in kg

    Returns:
        Temperature in Kelvin
    """
    return hbar * c**3 / (8 * np.pi * G * mass_kg * k_B)


def hawking_temperature_z2(mass_kg: float) -> float:
    """
    Calculate Hawking temperature using Z² formula.

    T_H = 4ℏc³ / (3Z²GMk_B)

    Since 8π = (3/4)Z², this is equivalent to the standard formula.

    Args:
        mass_kg: Black hole mass in kg

    Returns:
        Temperature in Kelvin
    """
    return 4 * hbar * c**3 / (3 * Z_SQUARED * G * mass_kg * k_B)


def verify_8pi_z2_relation():
    """Verify that 8π = (3/4)Z²"""
    eight_pi = 8 * np.pi
    three_quarter_z2 = 0.75 * Z_SQUARED
    match = 100 * (1 - abs(eight_pi - three_quarter_z2) / eight_pi)

    print(f"8π = {eight_pi:.6f}")
    print(f"(3/4)Z² = {three_quarter_z2:.6f}")
    print(f"Match: {match:.4f}%")
    return match > 99.99


# =============================================================================
# BEKENSTEIN-HAWKING ENTROPY
# =============================================================================

def bekenstein_hawking_entropy(mass_kg: float) -> float:
    """
    Calculate Bekenstein-Hawking entropy.

    S = A / (4 ℓ_P²) = k_B × A / (4 ℓ_P²)

    Args:
        mass_kg: Black hole mass in kg

    Returns:
        Entropy in units of k_B
    """
    # Horizon area
    r_s = 2 * G * mass_kg / c**2
    A = 4 * np.pi * r_s**2

    # Entropy
    S = A / (4 * l_P**2)
    return S


def bekenstein_hawking_entropy_z2(mass_kg: float) -> float:
    """
    Calculate Bekenstein-Hawking entropy using Z² formula.

    S = A / (BEKENSTEIN × ℓ_P²)

    where BEKENSTEIN = 3Z²/(8π) = 4

    Args:
        mass_kg: Black hole mass in kg

    Returns:
        Entropy in units of k_B
    """
    r_s = 2 * G * mass_kg / c**2
    A = 4 * np.pi * r_s**2

    S = A / (BEKENSTEIN * l_P**2)
    return S


def verify_bekenstein_equals_4():
    """Verify that BEKENSTEIN = 3Z²/(8π) = 4"""
    calculated = 3 * Z_SQUARED / (8 * np.pi)

    print(f"BEKENSTEIN = 3Z²/(8π) = 3 × {Z_SQUARED:.6f} / {8*np.pi:.6f}")
    print(f"           = {3 * Z_SQUARED:.6f} / {8*np.pi:.6f}")
    print(f"           = {calculated:.6f}")
    print(f"Expected:  4.0")
    print(f"Match: {100 * (1 - abs(calculated - 4) / 4):.4f}%")
    return abs(calculated - 4) < 1e-10


# =============================================================================
# EVAPORATION AND LIFETIME
# =============================================================================

def evaporation_time(mass_kg: float) -> float:
    """
    Calculate black hole evaporation time.

    t_evap = 5120 π G² M³ / (ℏc⁴)

    Args:
        mass_kg: Black hole mass in kg

    Returns:
        Evaporation time in seconds
    """
    return 5120 * np.pi * G**2 * mass_kg**3 / (hbar * c**4)


def hawking_luminosity(mass_kg: float) -> float:
    """
    Calculate Hawking radiation luminosity.

    P = ℏc⁶ / (15360 π G² M²)

    Args:
        mass_kg: Black hole mass in kg

    Returns:
        Power in Watts
    """
    return hbar * c**6 / (15360 * np.pi * G**2 * mass_kg**2)


def peak_wavelength(mass_kg: float) -> float:
    """
    Calculate peak wavelength of Hawking radiation.

    λ_peak = hc / (2.82 k_B T_H)

    Args:
        mass_kg: Black hole mass in kg

    Returns:
        Wavelength in meters
    """
    T_H = hawking_temperature(mass_kg)
    h = 2 * np.pi * hbar
    return h * c / (2.82 * k_B * T_H)


def peak_wavelength_to_rs_ratio(mass_kg: float) -> float:
    """
    Calculate ratio of peak wavelength to Schwarzschild radius.

    This should be approximately Z²/3 ≈ 11.17

    Args:
        mass_kg: Black hole mass in kg

    Returns:
        λ_peak / r_s ratio
    """
    lambda_peak = peak_wavelength(mass_kg)
    r_s = 2 * G * mass_kg / c**2
    return lambda_peak / r_s


# =============================================================================
# SAGITTARIUS A* ANALYSIS
# =============================================================================

def analyze_sgr_a_star():
    """Analyze Sagittarius A* black hole"""

    # Observed properties
    mass = 4.0e6 * M_sun  # 4 million solar masses
    distance = 8.178e3 * 3.086e16  # 8.178 kpc in meters
    spin = 0.94  # Estimated spin parameter

    print("=" * 70)
    print("SAGITTARIUS A* ANALYSIS")
    print("=" * 70)

    print(f"\nObserved Properties:")
    print(f"  Mass: {4.0e6:.2e} M☉ = {mass:.3e} kg")
    print(f"  Distance: 8.178 kpc = {distance:.3e} m")
    print(f"  Spin parameter: a = {spin}")

    # Schwarzschild radius
    r_s = 2 * G * mass / c**2
    print(f"\nDerived Properties:")
    print(f"  Schwarzschild radius: r_s = {r_s:.3e} m = {r_s/1e9:.2f} million km")

    # Shadow radius (Schwarzschild approximation)
    r_shadow = np.sqrt(27) * G * mass / c**2  # = 3√3 × r_s/2
    print(f"  Shadow radius: r_shadow = {r_shadow:.3e} m")

    # Angular size
    theta_rad = r_shadow / distance
    theta_uas = theta_rad * 1e6 * 180 * 3600 / np.pi  # microarcseconds
    print(f"  Angular radius: {theta_uas:.1f} μas")
    print(f"  Angular diameter: {2*theta_uas:.1f} μas")
    print(f"  Observed (EHT): 51.8 ± 2.3 μas")

    # Hawking temperature
    T_H = hawking_temperature(mass)
    print(f"\nHawking Temperature:")
    print(f"  T_H = {T_H:.3e} K")
    print(f"  (CMB temperature: 2.725 K, ratio: {T_H/2.725:.3e})")

    # Entropy
    S = bekenstein_hawking_entropy(mass)
    print(f"\nEntropy:")
    print(f"  S = {S:.3e} k_B")
    print(f"  S = 10^{np.log10(S):.1f} k_B")

    # Evaporation time
    t_evap = evaporation_time(mass)
    t_evap_years = t_evap / year_s
    print(f"\nEvaporation Time:")
    print(f"  t_evap = {t_evap:.3e} s = 10^{np.log10(t_evap_years):.0f} years")
    print(f"  (Universe age: ~1.4 × 10¹⁰ years)")

    # Luminosity
    P = hawking_luminosity(mass)
    print(f"\nHawking Luminosity:")
    print(f"  P = {P:.3e} W")
    print(f"  (Solar luminosity: 3.83 × 10²⁶ W)")

    return {
        "mass": mass,
        "r_s": r_s,
        "T_H": T_H,
        "S": S,
        "t_evap": t_evap_years,
        "P": P
    }


# =============================================================================
# BLACK HOLE MERGER ANALYSIS
# =============================================================================

@dataclass
class MergerEvent:
    """Gravitational wave merger event"""
    name: str
    date: str
    m1_solar: float
    m2_solar: float
    m_final_solar: float
    spin_final: Optional[float] = None
    snr: Optional[float] = None


# Key LIGO/Virgo events
MERGER_EVENTS = [
    MergerEvent("GW150914", "2015-09-14", 36, 29, 62, 0.67, 24),
    MergerEvent("GW170817", "2017-08-17", 1.4, 1.4, 2.7, None, 33),  # NS merger
    MergerEvent("GW190521", "2019-05-21", 85, 66, 142, 0.72, 14),
    MergerEvent("GW231123", "2023-11-23", 100, 140, 225, None, None),
    MergerEvent("GW250114", "2025-01-14", None, None, None, None, 80),
]


def analyze_merger(event: MergerEvent):
    """Analyze a black hole merger event"""

    print(f"\n--- {event.name} ({event.date}) ---")

    if event.m1_solar is None:
        print("  Mass data not available")
        return

    m1 = event.m1_solar * M_sun
    m2 = event.m2_solar * M_sun
    m_final = event.m_final_solar * M_sun

    # Energy radiated
    m_radiated = (event.m1_solar + event.m2_solar - event.m_final_solar)
    E_radiated = m_radiated * M_sun * c**2
    efficiency = m_radiated / (event.m1_solar + event.m2_solar)

    print(f"  Initial masses: {event.m1_solar} + {event.m2_solar} = {event.m1_solar + event.m2_solar} M☉")
    print(f"  Final mass: {event.m_final_solar} M☉")
    print(f"  Mass radiated: {m_radiated:.1f} M☉ = {E_radiated:.3e} J")
    print(f"  Efficiency: {100*efficiency:.1f}%")

    if event.spin_final:
        print(f"  Final spin: a = {event.spin_final}")
        print(f"  Compare to Ω_Λ = {OMEGA_LAMBDA:.3f}")

    if event.snr:
        print(f"  Signal-to-noise ratio: {event.snr}")

    # Hawking properties of final black hole
    T_H = hawking_temperature(m_final)
    S = bekenstein_hawking_entropy(m_final)

    print(f"  Final black hole:")
    print(f"    Hawking temperature: {T_H:.3e} K")
    print(f"    Entropy: 10^{np.log10(S):.1f} k_B")


def analyze_all_mergers():
    """Analyze all recorded merger events"""

    print("=" * 70)
    print("BLACK HOLE MERGER ANALYSIS")
    print("=" * 70)

    for event in MERGER_EVENTS:
        analyze_merger(event)


# =============================================================================
# Z² CONNECTION VERIFICATION
# =============================================================================

def verify_all_z2_connections():
    """Verify all Z² connections to black hole physics"""

    print("=" * 70)
    print("Z² CONNECTIONS TO BLACK HOLE PHYSICS")
    print("=" * 70)

    print(f"\nFundamental Z² Constants:")
    print(f"  Z² = 32π/3 = {Z_SQUARED:.6f}")
    print(f"  Z = √(Z²) = {Z:.6f}")

    print("\n" + "-" * 70)
    print("1. BEKENSTEIN = 4 Verification")
    print("-" * 70)
    verify_bekenstein_equals_4()

    print("\n" + "-" * 70)
    print("2. 8π = (3/4)Z² Verification")
    print("-" * 70)
    verify_8pi_z2_relation()

    print("\n" + "-" * 70)
    print("3. Hawking Temperature Formulas")
    print("-" * 70)

    test_mass = 10 * M_sun
    T_standard = hawking_temperature(test_mass)
    T_z2 = hawking_temperature_z2(test_mass)

    print(f"\nFor a 10 M☉ black hole:")
    print(f"  Standard formula: T_H = ℏc³/(8πGMk_B) = {T_standard:.6e} K")
    print(f"  Z² formula:       T_H = 4ℏc³/(3Z²GMk_B) = {T_z2:.6e} K")
    print(f"  Match: {100 * T_z2 / T_standard:.4f}%")

    print("\n" + "-" * 70)
    print("4. Entropy Formulas")
    print("-" * 70)

    S_standard = bekenstein_hawking_entropy(test_mass)
    S_z2 = bekenstein_hawking_entropy_z2(test_mass)

    print(f"\nFor a 10 M☉ black hole:")
    print(f"  Standard formula: S = A/(4ℓ_P²) = {S_standard:.6e} k_B")
    print(f"  Z² formula:       S = A/(BEKENSTEIN×ℓ_P²) = {S_z2:.6e} k_B")
    print(f"  Match: {100 * S_z2 / S_standard:.4f}%")

    print("\n" + "-" * 70)
    print("5. Peak Wavelength / r_s Ratio")
    print("-" * 70)

    ratio = peak_wavelength_to_rs_ratio(test_mass)
    z2_prediction = Z_SQUARED / 3

    print(f"\nFor a 10 M☉ black hole:")
    print(f"  λ_peak / r_s = {ratio:.4f}")
    print(f"  Z²/3 = {z2_prediction:.4f}")
    print(f"  Match: {100 * (1 - abs(ratio - z2_prediction) / z2_prediction):.2f}%")


# =============================================================================
# PRIMORDIAL BLACK HOLE ANALYSIS
# =============================================================================

def primordial_black_hole_analysis():
    """Analyze primordial black holes and their evaporation"""

    print("=" * 70)
    print("PRIMORDIAL BLACK HOLE ANALYSIS")
    print("=" * 70)

    universe_age = 13.8e9 * year_s  # Age of universe in seconds

    print(f"\nUniverse age: {13.8e9:.2e} years = {universe_age:.3e} s")

    # Find mass that evaporates in universe lifetime
    # t_evap = 5120 π G² M³ / (ℏc⁴)
    # M = (t_evap × ℏc⁴ / (5120 π G²))^(1/3)

    M_critical = (universe_age * hbar * c**4 / (5120 * np.pi * G**2))**(1/3)

    print(f"\nCritical mass (evaporates in universe age):")
    print(f"  M_critical = {M_critical:.3e} kg = {M_critical/M_sun:.3e} M☉")

    # Table of different masses
    masses_kg = [1e5, 1e10, 1e12, 1e15, M_critical, 1e20, M_sun]
    mass_names = ["10⁵ kg", "10¹⁰ kg", "10¹² kg", "10¹⁵ kg", "Critical", "10²⁰ kg", "1 M☉"]

    print("\n" + "-" * 90)
    print(f"{'Mass':<15} {'T_H (K)':<15} {'t_evap (years)':<20} {'Status':<20}")
    print("-" * 90)

    for mass, name in zip(masses_kg, mass_names):
        T = hawking_temperature(mass)
        t = evaporation_time(mass) / year_s

        if t < 13.8e9:
            status = "Evaporated"
        elif t < 1e20:
            status = "Evaporating"
        else:
            status = "Stable"

        print(f"{name:<15} {T:<15.3e} {t:<20.3e} {status:<20}")


# =============================================================================
# INFORMATION CAPACITY
# =============================================================================

def information_analysis(mass_kg: float):
    """Analyze information storage capacity of a black hole"""

    print(f"\nInformation Analysis for M = {mass_kg/M_sun:.2e} M☉:")

    S = bekenstein_hawking_entropy(mass_kg)
    I_bits = S / np.log(2)  # Convert from nats to bits

    r_s = 2 * G * mass_kg / c**2
    A = 4 * np.pi * r_s**2

    bits_per_planck_area = I_bits / (A / l_P**2)
    bits_per_dof = I_bits / 19  # Per cosmological degree of freedom

    print(f"  Entropy: {S:.3e} k_B (nats)")
    print(f"  Information: {I_bits:.3e} bits")
    print(f"  Horizon area: {A:.3e} m² = {A/l_P**2:.3e} ℓ_P²")
    print(f"  Bits per Planck area: {bits_per_planck_area:.4f}")
    print(f"  Expected (1/4 per Planck area): {0.25:.4f}")
    print(f"  Bits per cosmological DoF: {bits_per_dof:.3e}")


# =============================================================================
# MAIN
# =============================================================================

def print_summary():
    """Print summary of all black hole Z² connections"""

    print("\n" + "=" * 70)
    print("BLACK HOLE PHYSICS IN THE Z² FRAMEWORK - SUMMARY")
    print("=" * 70)

    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                     KEY Z² CONNECTIONS                                ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  1. BEKENSTEIN = 3Z²/(8π) = 4                                        ║
║     • The "4" in S = A/(4ℓ_P²) comes from Z² geometry                ║
║     • Not arbitrary - emerges from T³/Z₂ orbifold                    ║
║                                                                       ║
║  2. 8π = (3/4)Z²                                                     ║
║     • The "8π" in Hawking temperature is Z²-related                  ║
║     • T_H = ℏc³/(8πGMk_B) = 4ℏc³/(3Z²GMk_B)                         ║
║                                                                       ║
║  3. λ_peak/r_s = Z²/3 ≈ 11.17                                        ║
║     • Peak Hawking wavelength scales with Z²                         ║
║                                                                       ║
║  4. 19 Degrees of Freedom                                            ║
║     • Ω_Λ = 13/19, Ω_m = 6/19 → 19 total                            ║
║     • Black holes: maximum entropy = all DoF saturated               ║
║     • Information stored at 1 bit per 4 Planck areas                 ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════╗
║                   WHAT IS BEING RADIATED?                             ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  Hawking radiation is THERMAL blackbody radiation containing:        ║
║                                                                       ║
║  • Photons (all masses)                                              ║
║  • Gravitons (all masses)                                            ║
║  • Massive particles (if m < k_B T_H / c²)                           ║
║                                                                       ║
║  Mechanism: Vacuum fluctuations near horizon create pairs            ║
║  • One particle falls in (negative energy)                           ║
║  • One escapes (positive energy = radiation)                         ║
║  • Black hole loses mass                                             ║
║                                                                       ║
║  The spectrum carries NO information about what fell in              ║
║  (classically) → Information Paradox                                 ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════╗
║                  IS INFORMATION LOST?                                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  Z² Framework Perspective:                                           ║
║                                                                       ║
║  • Information stored on horizon at density 1/(4ℓ_P²)               ║
║  • The "4" = BEKENSTEIN connects to orbifold geometry                ║
║  • 19 degrees of freedom encode the information                      ║
║  • Hawking radiation may carry subtle correlations                   ║
║  • Unitarity could be preserved through entanglement                 ║
║                                                                       ║
║  The Page curve suggests information DOES come out:                  ║
║  • Early: Entropy increases (radiation entangled with BH)            ║
║  • Page time: Entropy peaks at S/2                                   ║
║  • Late: Entropy decreases (radiation self-entangled)                ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    print_summary()
    verify_all_z2_connections()
    analyze_sgr_a_star()
    analyze_all_mergers()
    primordial_black_hole_analysis()
    information_analysis(4e6 * M_sun)  # Sgr A*
