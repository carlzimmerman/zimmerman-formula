"""
Project Aitheria: Core Constants and Parameters
================================================

AGPL-3.0 License
Author: Carl Zimmerman
Date: May 2026

"If you try something and you fail, you gotta be honest about it."
    — Carl Zimmerman

STATUS: PROJECT ARCHIVED - See HONEST_ASSESSMENT.md

Z²-derived constants for gas-phase topological diversion from industrial flue gas.

CRITICAL NOTE: These are THEORETICAL parameters requiring experimental validation.
The physical mechanisms proposed here are speculative and need rigorous testing.
"""

import numpy as np
from typing import Dict, Any

# =============================================================================
# FUNDAMENTAL Z-CONSTANTS
# =============================================================================

Z_CONSTANT_ANGSTROM = np.sqrt(32 * np.pi / 3)  # 5.7888 Å
Z_CONSTANT_M = Z_CONSTANT_ANGSTROM * 1e-10     # 5.7888e-10 m

# Speed of light
C_LIGHT = 2.998e8  # m/s

# Fundamental Z-frequency
F_Z_HZ = C_LIGHT / Z_CONSTANT_M  # ~5.18e17 Hz (518 PHz)

# =============================================================================
# Z-DERIVED FREQUENCIES FOR GAS-PHASE APPLICATIONS
# =============================================================================

# 10^9 bridge (GHz range - surface acoustic waves)
F_SAW_GHZ = F_Z_HZ / 1e9 / 1e9  # ~518 GHz
F_SAW_HZ = F_SAW_GHZ * 1e9       # Hz

# 10^6 bridge (MHz range - alternative coupling)
F_ALT_MHZ = F_Z_HZ / 1e6 / 1e9  # ~518 MHz
F_ALT_HZ = F_ALT_MHZ * 1e6       # Hz

# User-specified frequency (from initial discussion)
F_TARGET_MHZ = 592.5  # MHz (user's proposed SAW frequency)
F_TARGET_HZ = F_TARGET_MHZ * 1e6

# =============================================================================
# STANENE LATTICE PROPERTIES
# =============================================================================

# Native stanene lattice constant
STANENE_NATIVE_A = 4.67e-10  # m (4.67 Å)

# Z-strained stanene (24% biaxial strain)
STANENE_Z_STRAIN = (Z_CONSTANT_M - STANENE_NATIVE_A) / STANENE_NATIVE_A  # ~24%
STANENE_Z_A = Z_CONSTANT_M  # 5.79 Å

# Thermal expansion coefficient for tin (β-Sn, white tin)
# Literature: α ≈ 22 × 10^-6 /K (bulk tin)
# For 2D stanene, this may differ significantly
ALPHA_TIN_BULK = 22e-6  # /K (bulk β-tin)
ALPHA_STANENE_ESTIMATED = 15e-6  # /K (estimated for 2D, needs validation)

# Melting point of tin
TIN_MELTING_K = 505  # K (231.9°C)

# Phase transition (α-Sn to β-Sn)
TIN_PHASE_TRANSITION_K = 286.4  # K (13.2°C)

# =============================================================================
# FLUE GAS CONDITIONS
# =============================================================================

# Typical coal-fired power plant flue gas composition (vol%)
FLUE_GAS_COMPOSITION = {
    'N2': 0.72,      # 72%
    'CO2': 0.13,     # 13%
    'H2O': 0.10,     # 10%
    'O2': 0.04,      # 4%
    'SO2': 0.002,    # 0.2% (2000 ppm)
    'NOx': 0.0005,   # 500 ppm
    'Hg': 5e-9,      # ~5 ppb
    'Xe': 8.6e-8,    # 0.086 ppm (from air)
    'Kr': 1.14e-6,   # 1.14 ppm (from air)
}

# Temperature range (K)
FLUE_GAS_T_MIN_K = 423  # 150°C
FLUE_GAS_T_MAX_K = 573  # 300°C
FLUE_GAS_T_TYPICAL_K = 473  # 200°C (typical)

# Velocity (m/s)
FLUE_GAS_VELOCITY_MIN = 10  # m/s
FLUE_GAS_VELOCITY_MAX = 30  # m/s
FLUE_GAS_VELOCITY_TYPICAL = 15  # m/s

# Pressure (Pa)
FLUE_GAS_PRESSURE_PA = 101325  # ~1 atm (slight negative draft)

# =============================================================================
# TARGET MOLECULE PROPERTIES
# =============================================================================

MOLECULES = {
    'CO2': {
        'molar_mass': 44.01e-3,  # kg/mol
        'kinetic_diameter': 3.3e-10,  # m (3.3 Å)
        'quadrupole_moment': -4.3e-40,  # C·m² (significant!)
        'polarizability': 2.91e-40,  # C²·m²/J
        'bond_energy_kJ_mol': 799,  # C=O bond
        'carbon_credit_USD_ton': 100,  # $/ton CO2
    },
    'Hg': {
        'molar_mass': 200.59e-3,  # kg/mol
        'atomic_radius': 1.51e-10,  # m
        'spin_orbit_coupling': 1.5,  # eV (strong!)
        'ionization_energy': 10.44,  # eV
        'disposal_cost_USD_kg': 50,  # HAZMAT disposal
        'penalty_USD_lb_exceeded': 1000,  # EPA penalty estimate
    },
    'Xe': {
        'molar_mass': 131.29e-3,  # kg/mol
        'atomic_radius': 2.16e-10,  # m (2.16 Å)
        'polarizability': 4.04e-40,  # C²·m²/J (high!)
        'price_USD_kg': 2000,  # Market price
        'concentration_ppm': 0.086,  # In air
    },
    'Kr': {
        'molar_mass': 83.80e-3,  # kg/mol
        'atomic_radius': 1.78e-10,  # m
        'polarizability': 2.46e-40,  # C²·m²/J
        'price_USD_kg': 400,  # Market price
        'concentration_ppm': 1.14,  # In air
    },
    'SO2': {
        'molar_mass': 64.07e-3,  # kg/mol
        'kinetic_diameter': 4.1e-10,  # m
        'dipole_moment': 1.63,  # Debye
        'bond_energy_kJ_mol': 548,  # S=O bond
    },
    'N2': {
        'molar_mass': 28.01e-3,  # kg/mol
        'kinetic_diameter': 3.64e-10,  # m
        'quadrupole_moment': -1.52e-40,  # C·m² (small)
        'polarizability': 1.74e-40,  # C²·m²/J
    },
}

# =============================================================================
# Z-HARMONIC RELATIONSHIPS
# =============================================================================

# Z/2 pore size (for steric sieving)
Z_HALF_ANGSTROM = Z_CONSTANT_ANGSTROM / 2  # 2.89 Å

# Xe atomic diameter vs Z/2
XE_DIAMETER = 2 * MOLECULES['Xe']['atomic_radius'] * 1e10  # Å
XE_TO_Z_HALF_RATIO = XE_DIAMETER / Z_HALF_ANGSTROM  # ~1.49 (close to 3/2?)

# =============================================================================
# CURRENT TECHNOLOGY BENCHMARKS (FOR HONEST COMPARISON)
# =============================================================================

CURRENT_TECH = {
    'amine_scrubbing': {
        'capture_efficiency': 0.95,  # 95%
        'energy_penalty_fraction': 0.25,  # 25% of plant output
        'energy_GJ_per_ton_CO2': 4.0,  # GJ/ton
        'cost_USD_per_ton_CO2': 60,  # $/ton
    },
    'activated_carbon_injection': {
        'hg_removal_efficiency': 0.90,  # 90%
        'injection_rate_mg_m3': 160,  # mg/m³ (standard AC)
        'brominated_rate_mg_m3': 30,  # mg/m³ (brominated AC)
        'market_size_2024_USD': 1.31e9,  # $1.31B
    },
    'cryogenic_xe_separation': {
        'energy_intensive': True,
        'xe_purity': 0.9999,  # 99.99%
        'energy_relative': 1.0,  # baseline
        'hydrate_method_advantage': 0.20,  # 20% energy savings
    },
}

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

K_BOLTZMANN = 1.381e-23  # J/K
N_AVOGADRO = 6.022e23  # /mol
R_GAS = 8.314  # J/(mol·K)
H_PLANCK = 6.626e-34  # J·s
EPSILON_0 = 8.854e-12  # F/m

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_lattice_at_temperature(T_K: float, alpha: float = ALPHA_STANENE_ESTIMATED) -> float:
    """
    Calculate Z-strained stanene lattice constant at temperature T.

    Args:
        T_K: Temperature in Kelvin
        alpha: Linear thermal expansion coefficient (/K)

    Returns:
        Lattice constant in meters
    """
    T_ref = 300  # Reference temperature (room temp)
    delta_T = T_K - T_ref
    a_T = STANENE_Z_A * (1 + alpha * delta_T)
    return a_T


def get_lattice_drift_percent(T_K: float) -> float:
    """
    Calculate percentage drift from ideal Z-constant at temperature T.

    Args:
        T_K: Temperature in Kelvin

    Returns:
        Percentage drift from Z-constant
    """
    a_T = get_lattice_at_temperature(T_K)
    drift = (a_T - Z_CONSTANT_M) / Z_CONSTANT_M * 100
    return drift


def get_molecule_thermal_velocity(molecule: str, T_K: float) -> float:
    """
    Calculate mean thermal velocity of a gas molecule.

    Args:
        molecule: Molecule name (key in MOLECULES dict)
        T_K: Temperature in Kelvin

    Returns:
        Mean thermal velocity in m/s
    """
    M = MOLECULES[molecule]['molar_mass']
    m = M / N_AVOGADRO  # Mass per molecule
    v_mean = np.sqrt(8 * K_BOLTZMANN * T_K / (np.pi * m))
    return v_mean


def get_residence_time(channel_length_m: float, gas_velocity: float) -> float:
    """
    Calculate gas residence time in the Aitheria channel.

    Args:
        channel_length_m: Length of Z-lined channel in meters
        gas_velocity: Gas flow velocity in m/s

    Returns:
        Residence time in seconds
    """
    return channel_length_m / gas_velocity


def get_saw_wavelength(frequency_hz: float, sound_speed: float = 3000) -> float:
    """
    Calculate SAW wavelength for given frequency.

    Args:
        frequency_hz: SAW frequency in Hz
        sound_speed: Speed of sound in substrate (m/s)
                     LiNbO3: ~3000-4000 m/s

    Returns:
        Wavelength in meters
    """
    return sound_speed / frequency_hz


# =============================================================================
# SUMMARY OUTPUT
# =============================================================================

def print_summary():
    """Print summary of Aitheria constants."""
    print("=" * 60)
    print("PROJECT AITHERIA: Core Constants Summary")
    print("=" * 60)
    print(f"\nZ-Constant: {Z_CONSTANT_ANGSTROM:.4f} Å")
    print(f"Z/2 (steric target): {Z_HALF_ANGSTROM:.4f} Å")
    print(f"\nZ-derived frequencies:")
    print(f"  f_Z (fundamental): {F_Z_HZ:.3e} Hz ({F_Z_HZ/1e15:.1f} PHz)")
    print(f"  f_SAW (10⁹ bridge): {F_SAW_GHZ:.1f} GHz")
    print(f"  f_alt (10⁶ bridge): {F_ALT_MHZ:.1f} MHz")
    print(f"  f_target (user): {F_TARGET_MHZ} MHz")
    print(f"\nStanene properties:")
    print(f"  Native lattice: {STANENE_NATIVE_A*1e10:.2f} Å")
    print(f"  Z-strained: {STANENE_Z_A*1e10:.4f} Å (strain: {STANENE_Z_STRAIN*100:.1f}%)")
    print(f"  α (thermal expansion): {ALPHA_STANENE_ESTIMATED*1e6:.1f} × 10⁻⁶ /K")
    print(f"\nLattice drift at flue gas temperatures:")
    for T in [FLUE_GAS_T_MIN_K, FLUE_GAS_T_TYPICAL_K, FLUE_GAS_T_MAX_K]:
        drift = get_lattice_drift_percent(T)
        print(f"  {T-273:.0f}°C: {drift:+.3f}%")
    print(f"\nTarget molecules:")
    for mol, props in MOLECULES.items():
        if 'price_USD_kg' in props:
            print(f"  {mol}: ${props['price_USD_kg']}/kg")
        elif 'carbon_credit_USD_ton' in props:
            print(f"  {mol}: ${props['carbon_credit_USD_ton']}/ton (carbon credit)")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print_summary()
