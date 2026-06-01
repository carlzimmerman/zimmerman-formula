"""
constants.py - Central Source of Truth for Z² Abiogenesis Investigation

This module defines all fundamental constants, derived quantities, and
experimental values used across the computational abiogenesis framework.

IMPORTANT DISTINCTION:
- Z² (the constant) = 32π/3 ≈ 33.51 (sphere-cube coupling)
- Z₂ (the group) = parity symmetry group (used in topology)

These are UNRELATED mathematically, despite similar notation.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any


# =============================================================================
# FUNDAMENTAL CONSTANTS (CODATA 2018)
# =============================================================================

# Physical Constants
c = 299792458.0           # Speed of light [m/s]
hbar = 1.054571817e-34    # Reduced Planck constant [J·s]
k_B = 1.380649e-23        # Boltzmann constant [J/K]
N_A = 6.02214076e23       # Avogadro number [mol⁻¹]
e = 1.602176634e-19       # Elementary charge [C]
m_e = 9.1093837015e-31    # Electron mass [kg]
m_p = 1.67262192369e-27   # Proton mass [kg]
epsilon_0 = 8.8541878128e-12  # Vacuum permittivity [F/m]
alpha = 1/137.035999084   # Fine structure constant

# Particle Physics
m_muon = 105.6583755      # Muon mass [MeV/c²]
m_pion = 139.57039        # Charged pion mass [MeV/c²]
tau_muon = 2.1969811e-6   # Muon lifetime [s]


# =============================================================================
# Z² GEOMETRIC CONSTANTS (Zimmerman Formula)
# =============================================================================

# The fundamental sphere-cube coupling constant
Z_SQUARED = 32 * np.pi / 3  # ≈ 33.510...
Z = np.sqrt(Z_SQUARED)       # ≈ 5.7888 Å

# Derived Z² quantities
Z_OVER_12 = Z / 12           # ≈ 0.4824 (compare to protein factor 0.491)
EIGHT_PI_OVER_Z_SQ = 8 * np.pi / Z_SQUARED  # = 0.75 exactly

# Z in different units
Z_ANGSTROM = Z               # 5.7888 Å
Z_NANOMETER = Z / 10         # 0.57888 nm
Z_METER = Z * 1e-10          # 5.7888e-10 m


# =============================================================================
# PACKING GEOMETRY CONSTANTS
# =============================================================================

# Ideal sphere packing fractions
PHI_FCC = np.pi / (3 * np.sqrt(2))  # ≈ 0.7405 (Face-centered cubic)
PHI_BCC = np.pi * np.sqrt(3) / 8    # ≈ 0.6802 (Body-centered cubic)
PHI_SC = np.pi / 6                   # ≈ 0.5236 (Simple cubic)
PHI_RANDOM = 0.64                    # Random close packing (empirical)

# Kissing numbers (maximum contacts in various dimensions)
KISSING_2D = 6
KISSING_3D = 12
KISSING_4D = 24

# Protein packing factor (experimental)
PROTEIN_FACTOR_EXPERIMENTAL = 0.491  # V / (A × <r>)
PROTEIN_FACTOR_PREDICTED = Z / 12    # ≈ 0.4824
PROTEIN_FACTOR_DISCREPANCY = abs(PROTEIN_FACTOR_EXPERIMENTAL - PROTEIN_FACTOR_PREDICTED) / PROTEIN_FACTOR_EXPERIMENTAL  # ~1.8%


# =============================================================================
# MINERAL LATTICE CONSTANTS (for DFT tests)
# =============================================================================

@dataclass
class MineralLattice:
    """Crystal structure parameters for origin-of-life minerals."""
    name: str
    formula: str
    lattice_constant: float  # Å
    structure: str
    z_deviation: float  # |a - Z| / Z

# Key minerals for abiogenesis
GALENA = MineralLattice("Galena", "PbS", 5.936, "rocksalt", abs(5.936 - Z) / Z)
PYRITE = MineralLattice("Pyrite", "FeS₂", 5.417, "cubic", abs(5.417 - Z) / Z)
MACKINAWITE = MineralLattice("Mackinawite", "FeS", 5.032, "tetragonal", abs(5.032 - Z) / Z)
GREIGITE = MineralLattice("Greigite", "Fe₃S₄", 9.876, "spinel", abs(9.876/2 - Z) / Z)


# =============================================================================
# BIOLOGICAL CONSTANTS
# =============================================================================

# Ribosome PTC (Peptidyl Transferase Center)
PTC_A2451_TO_TS = 5.2  # Å - Distance from A2451 to transition state
PTC_Z_DEVIATION = abs(PTC_A2451_TO_TS - Z) / Z  # ~10.2%

# Amino acid properties
AMINO_ACID_MASS_AVG = 110  # Da (average mass)
AMINO_ACID_VOLUME_AVG = 140  # Å³ (average volume)

# Cell parameters
E_COLI_RADIUS = 0.5e-6  # m (typical)
E_COLI_GENOME_BP = 4.6e6  # base pairs
BITS_PER_BP = 2  # Information content


# =============================================================================
# CHIRALITY PARAMETERS
# =============================================================================

# Frank Model rate constants (dimensionless)
FRANK_K0 = 1.0    # Spontaneous production
FRANK_K1 = 10.0   # Autocatalytic rate
FRANK_K2 = 100.0  # Mutual inhibition

# CISS (Chiral-Induced Spin Selectivity)
CISS_POLARIZATION = 0.20  # Typical 20% spin selectivity

# Muon physics for Z₂ cosmic ray model
MUON_POLARIZATION_COSMIC = 0.33  # Effective at sea level
CMB_PARITY_ASYMMETRY = 0.07     # From Planck data


# =============================================================================
# THERMAL PARAMETERS
# =============================================================================

# Early Earth conditions
TEMP_EARLY_EARTH_K = 353  # ~80°C (hydrothermal)
TEMP_BIOLOGICAL_K = 310   # 37°C (human body)
TEMP_ABSOLUTE_ZERO_K = 0

# Thermal expansion coefficients [K⁻¹]
THERMAL_EXPANSION_PROTEIN = 4e-4  # Approximate for proteins


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def z_deviation(value: float, in_angstroms: bool = True) -> float:
    """Calculate fractional deviation from Z."""
    z_ref = Z_ANGSTROM if in_angstroms else Z_METER
    return abs(value - z_ref) / z_ref


def z12_deviation(value: float) -> float:
    """Calculate fractional deviation from Z/12."""
    return abs(value - Z_OVER_12) / Z_OVER_12


def thermal_expansion_factor(T: float, T_ref: float = 273.15, alpha_T: float = THERMAL_EXPANSION_PROTEIN) -> float:
    """
    Calculate linear thermal expansion factor.

    L(T) / L(T_ref) = 1 + α_T × (T - T_ref)

    Args:
        T: Temperature [K]
        T_ref: Reference temperature [K] (default 0°C)
        alpha_T: Linear thermal expansion coefficient [K⁻¹]

    Returns:
        Linear expansion ratio
    """
    return 1 + alpha_T * (T - T_ref)


def get_all_constants() -> Dict[str, Any]:
    """Return all constants as a dictionary for export."""
    return {
        'Z_SQUARED': Z_SQUARED,
        'Z': Z,
        'Z_OVER_12': Z_OVER_12,
        'EIGHT_PI_OVER_Z_SQ': EIGHT_PI_OVER_Z_SQ,
        'PHI_FCC': PHI_FCC,
        'PHI_BCC': PHI_BCC,
        'PHI_SC': PHI_SC,
        'KISSING_3D': KISSING_3D,
        'PROTEIN_FACTOR_EXPERIMENTAL': PROTEIN_FACTOR_EXPERIMENTAL,
        'PROTEIN_FACTOR_PREDICTED': PROTEIN_FACTOR_PREDICTED,
        'PROTEIN_FACTOR_DISCREPANCY': PROTEIN_FACTOR_DISCREPANCY,
        'GALENA_LATTICE': GALENA.lattice_constant,
        'PYRITE_LATTICE': PYRITE.lattice_constant,
        'PTC_A2451_TO_TS': PTC_A2451_TO_TS,
        'PTC_Z_DEVIATION': PTC_Z_DEVIATION,
    }


# =============================================================================
# VALIDATION ON IMPORT
# =============================================================================

def _validate_constants():
    """Verify mathematical identities on module load."""
    # Check 8π/Z² = 3/4
    assert abs(EIGHT_PI_OVER_Z_SQ - 0.75) < 1e-10, "8π/Z² ≠ 0.75"

    # Check Z² = 8 × (4π/3)
    vol_unit_sphere = 4 * np.pi / 3
    assert abs(Z_SQUARED - 8 * vol_unit_sphere) < 1e-10, "Z² ≠ 8V_sphere"

    # Check kissing number relation
    assert KISSING_3D == 12, "3D kissing number ≠ 12"


_validate_constants()


# =============================================================================
# MODULE INFO
# =============================================================================

__version__ = "1.0.0"
__author__ = "Project Protogonos"
__description__ = "Central constants for Z² abiogenesis investigation"


if __name__ == "__main__":
    print("Z² Abiogenesis Constants")
    print("=" * 50)
    print(f"Z² = 32π/3 = {Z_SQUARED:.10f}")
    print(f"Z = √(32π/3) = {Z:.10f} Å")
    print(f"Z/12 = {Z_OVER_12:.10f}")
    print(f"8π/Z² = {EIGHT_PI_OVER_Z_SQ:.10f} (should be 0.75)")
    print()
    print("Protein Factor Comparison:")
    print(f"  Experimental: {PROTEIN_FACTOR_EXPERIMENTAL}")
    print(f"  Z/12 predicted: {Z_OVER_12:.4f}")
    print(f"  Discrepancy: {PROTEIN_FACTOR_DISCREPANCY*100:.2f}%")
    print()
    print("Mineral Lattice Deviations from Z:")
    print(f"  Galena (PbS): {GALENA.lattice_constant} Å ({GALENA.z_deviation*100:.1f}% off)")
    print(f"  Pyrite (FeS₂): {PYRITE.lattice_constant} Å ({PYRITE.z_deviation*100:.1f}% off)")
