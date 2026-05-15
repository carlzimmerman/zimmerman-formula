#!/usr/bin/env python3
"""
M-σ Relation in the Z² Framework
=================================

Calculates the predicted M_BH/M_bulge ratio evolution with redshift
based on Z²-MOND framework where a₀ = cH(z)/Z.

Key prediction: "Overmassive" high-z black holes are EXPECTED,
not anomalous, because M_BH/M_bulge ∝ H(z)/H₀.

Carl Zimmerman | May 2026
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
import json

# =============================================================================
# CONSTANTS
# =============================================================================

# Physical constants
c = 2.998e8  # m/s
G = 6.674e-11  # m³ kg⁻¹ s⁻²
M_SUN = 1.989e30  # kg
H0_SI = 70e3 / 3.086e22  # s⁻¹ (70 km/s/Mpc)
H0_kms_Mpc = 70  # km/s/Mpc

# Z² framework constants
Z_SQUARED = 32 * np.pi / 3  # = 33.510321
Z = np.sqrt(Z_SQUARED)       # = 5.788810
OMEGA_M = 6/19               # = 0.315789
OMEGA_L = 13/19              # = 0.684211

# MOND acceleration scale from Z²
a0 = c * H0_SI / Z  # ≈ 1.18×10⁻¹⁰ m/s²

# M-σ relation parameters (McConnell & Ma 2013)
M_SIGMA_ALPHA = 8.32  # log(M_BH/M☉) at σ = 200 km/s
M_SIGMA_BETA = 5.64   # power law slope (often approximated as ~4-5)
SIGMA_REF = 200  # km/s reference velocity dispersion

# Local M_BH/M_bulge ratio
LOCAL_MBH_MBULGE = 0.001  # Observed at z ≈ 0


# =============================================================================
# COSMOLOGY
# =============================================================================

def H_over_H0(z: float) -> float:
    """
    Hubble parameter ratio H(z)/H₀ for Z² cosmology.

    H(z)/H₀ = √(Ω_m(1+z)³ + Ω_Λ)
    """
    return np.sqrt(OMEGA_M * (1 + z)**3 + OMEGA_L)


def a0_at_z(z: float) -> float:
    """
    MOND acceleration scale at redshift z.

    Assuming a₀(z) = c·H(z)/Z
    """
    return a0 * H_over_H0(z)


def lookback_time_Gyr(z: float) -> float:
    """Approximate lookback time in Gyr."""
    # Simplified for flat ΛCDM
    from scipy.integrate import quad

    def integrand(zp):
        return 1 / ((1 + zp) * H_over_H0(zp))

    t_H0 = 1 / H0_SI / (3.156e16)  # Hubble time in Gyr
    result, _ = quad(integrand, 0, z)
    return t_H0 * result


def age_of_universe_Gyr(z: float) -> float:
    """Age of universe at redshift z in Gyr."""
    t_now = 13.8  # Gyr (approximate)
    if z == 0:
        return t_now
    return t_now - lookback_time_Gyr(z)


# =============================================================================
# M-σ RELATION
# =============================================================================

def M_BH_from_sigma(sigma_kms: float) -> float:
    """
    Black hole mass from velocity dispersion using M-σ relation.

    log(M_BH/M☉) = 8.32 + 5.64 × log(σ/200 km/s)

    Args:
        sigma_kms: Velocity dispersion in km/s

    Returns:
        M_BH in solar masses
    """
    log_M = M_SIGMA_ALPHA + M_SIGMA_BETA * np.log10(sigma_kms / SIGMA_REF)
    return 10**log_M


def sigma_from_vflat(v_flat_kms: float) -> float:
    """
    Velocity dispersion from flat rotation velocity using Z²-MOND.

    σ = v_flat / Z

    Args:
        v_flat_kms: Flat rotation velocity in km/s

    Returns:
        Velocity dispersion in km/s
    """
    return v_flat_kms / Z


def vflat_from_M_baryonic(M_baryonic: float, z: float = 0) -> float:
    """
    Flat rotation velocity from baryonic mass using BTFR.

    v_flat⁴ = G × M_baryonic × a₀(z)

    Args:
        M_baryonic: Baryonic mass in solar masses
        z: Redshift (for a₀ evolution)

    Returns:
        v_flat in km/s
    """
    M_kg = M_baryonic * M_SUN
    a0_z = a0_at_z(z)
    v_flat_ms = (G * M_kg * a0_z)**0.25
    return v_flat_ms / 1000  # Convert to km/s


# =============================================================================
# M_BH / M_BULGE EVOLUTION
# =============================================================================

def MBH_Mbulge_ratio(z: float) -> float:
    """
    Predicted M_BH/M_bulge ratio at redshift z.

    M_BH/M_bulge ∝ a₀(z) ∝ H(z)

    Normalized to LOCAL_MBH_MBULGE at z = 0.
    """
    return LOCAL_MBH_MBULGE * H_over_H0(z)


def MBH_Mbulge_enhancement(z: float) -> float:
    """Enhancement factor relative to z = 0."""
    return H_over_H0(z)


# =============================================================================
# PREDICTIONS
# =============================================================================

@dataclass
class HighZPrediction:
    """Prediction for a high-z system."""
    z: float
    H_ratio: float
    MBH_Mbulge: float
    a0_z: float
    age_Gyr: float

    def __str__(self):
        return (f"z = {self.z:.1f}: "
                f"H(z)/H₀ = {self.H_ratio:.1f}, "
                f"M_BH/M_bulge = {self.MBH_Mbulge:.4f}, "
                f"a₀ = {self.a0_z:.2e} m/s², "
                f"Age = {self.age_Gyr:.2f} Gyr")


def predict_at_redshift(z: float) -> HighZPrediction:
    """Generate full prediction for a given redshift."""
    return HighZPrediction(
        z=z,
        H_ratio=H_over_H0(z),
        MBH_Mbulge=MBH_Mbulge_ratio(z),
        a0_z=a0_at_z(z),
        age_Gyr=age_of_universe_Gyr(z)
    )


def print_evolution_table():
    """Print table of M_BH/M_bulge evolution with redshift."""
    print("\n" + "="*70)
    print("M_BH/M_BULGE EVOLUTION IN Z² FRAMEWORK")
    print("="*70)

    print(f"\nFundamental constants:")
    print(f"  Z² = 32π/3 = {Z_SQUARED:.6f}")
    print(f"  Z = {Z:.6f}")
    print(f"  a₀ = cH₀/Z = {a0:.3e} m/s²")
    print(f"  Ω_m = 6/19 = {OMEGA_M:.6f}")
    print(f"  Ω_Λ = 13/19 = {OMEGA_L:.6f}")

    print(f"\n{'z':<6} {'H(z)/H₀':<10} {'M_BH/M_bulge':<14} {'Enhancement':<12} {'Age (Gyr)':<10}")
    print("-"*55)

    redshifts = [0, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12]

    for z in redshifts:
        pred = predict_at_redshift(z)
        print(f"{z:<6.1f} {pred.H_ratio:<10.2f} {pred.MBH_Mbulge:<14.5f} "
              f"{pred.H_ratio:<12.1f}× {pred.age_Gyr:<10.2f}")


def compare_with_observations():
    """Compare Z² predictions with JWST observations."""

    print("\n" + "="*70)
    print("COMPARISON WITH JWST OBSERVATIONS")
    print("="*70)

    # Observed high-z BH systems (approximate values from literature)
    observations = [
        {"name": "Local galaxies", "z": 0, "MBH_Mstar": 0.001, "ref": "Kormendy+13"},
        {"name": "GN-z11", "z": 10.6, "MBH_Mstar": 0.002, "ref": "Maiolino+23"},
        {"name": "CEERS-1019", "z": 8.7, "MBH_Mstar": 0.01, "ref": "Larson+23"},
        {"name": "UHZ1", "z": 10.1, "MBH_Mstar": 0.4, "ref": "Bogdan+23"},
        {"name": "JADES-GS-z7", "z": 7.1, "MBH_Mstar": 0.01, "ref": "Übler+23"},
        {"name": "J0313-1806 (quasar)", "z": 7.64, "MBH_Mstar": 0.1, "ref": "Wang+21"},
    ]

    print(f"\n{'Object':<25} {'z':<6} {'Observed':<12} {'Z² Predicted':<14} {'Ratio':<10}")
    print("-"*70)

    for obs in observations:
        z = obs["z"]
        observed = obs["MBH_Mstar"]
        predicted = MBH_Mbulge_ratio(z)
        ratio = observed / predicted if predicted > 0 else 0

        status = "✓" if 0.1 < ratio < 10 else "?"

        print(f"{obs['name']:<25} {z:<6.1f} {observed:<12.4f} {predicted:<14.4f} {ratio:<10.1f}× {status}")

    print("\nNote: M_BH/M_* can differ from M_BH/M_bulge due to bulge/disk decomposition")
    print("      Ratios within 0.1× to 10× are considered consistent given uncertainties")


def quasar_luminosity_evolution():
    """Predict how maximum quasar luminosity evolves with z."""

    print("\n" + "="*70)
    print("QUASAR LUMINOSITY EVOLUTION")
    print("="*70)

    # Reference: L_Edd ∝ M_BH, and M_BH ∝ M_bulge × H(z)/H₀
    # For a galaxy of fixed baryonic mass, max quasar luminosity ∝ H(z)

    print("\nFor a galaxy of fixed baryonic mass M_baryonic:")
    print("  M_BH(z) = M_BH(0) × H(z)/H₀")
    print("  L_Edd(z) = L_Edd(0) × H(z)/H₀")

    print(f"\n{'z':<6} {'L_Edd enhancement':<20} {'Typical L_Edd (erg/s)':<25}")
    print("-"*55)

    # Reference: Local quasar with M_BH = 10^8 M☉
    L_Edd_ref = 1.26e38 * 1e8  # erg/s for 10^8 M☉

    for z in [0, 2, 4, 6, 8, 10]:
        enhancement = H_over_H0(z)
        L_Edd = L_Edd_ref * enhancement
        print(f"{z:<6.0f} {enhancement:<20.1f}× {L_Edd:<25.2e}")


# =============================================================================
# FALSIFICATION CRITERIA
# =============================================================================

def print_falsification_criteria():
    """Print criteria for testing/falsifying Z² predictions."""

    print("\n" + "="*70)
    print("FALSIFICATION CRITERIA")
    print("="*70)

    print("""
The Z² prediction for M_BH/M_bulge evolution is:

    M_BH/M_bulge(z) = 0.001 × H(z)/H₀

This prediction is FALSIFIED if:

1. STATISTICAL: Mean M_BH/M_* at z ~ 6-7 is NOT 10-15× local value
   - Need sample of >20 galaxies with BH and stellar mass measurements
   - Systematic uncertainties must be understood

2. INDIVIDUAL: Well-measured systems strongly deviate
   - Example: If a z = 6 galaxy has M_BH/M_* = 0.001 (local value)
   - Or if a z = 6 galaxy has M_BH/M_* = 0.5 (50× prediction)

3. DYNAMICS: σ ≠ v_flat/Z at any redshift
   - Direct test of Z²-MOND relation
   - Requires resolved kinematics at high z

The prediction is SUPPORTED if:

1. M_BH/M_* increases with z following H(z)/H₀
2. σ = v_flat/Z holds at all z where both are measured
3. M-σ relation normalization evolves as predicted

CRITICAL TEST:
  At z = 7: Predicted M_BH/M_bulge = {:.4f}
  At z = 10: Predicted M_BH/M_bulge = {:.4f}

  These are SPECIFIC, FALSIFIABLE predictions.
""".format(MBH_Mbulge_ratio(7), MBH_Mbulge_ratio(10)))


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run all analyses."""

    print("\n" + "="*70)
    print("M-σ RELATION IN Z² FRAMEWORK")
    print("="*70)
    print(f"\nKey insight: a₀ = cH/Z implies M_BH/M_bulge ∝ H(z)")
    print(f"This EXPLAINS why high-z BHs appear 'overmassive'")

    print_evolution_table()
    compare_with_observations()
    quasar_luminosity_evolution()
    print_falsification_criteria()

    print("\n" + "="*70)
    print("END OF ANALYSIS")
    print("="*70)


if __name__ == "__main__":
    main()
