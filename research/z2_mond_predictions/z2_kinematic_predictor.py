#!/usr/bin/env python3
"""
Z²-MOND KINEMATIC PREDICTOR
============================

Calculates velocity dispersion and rotation velocity predictions for high-z
galaxies based on the Z² framework.

Usage:
  python z2_kinematic_predictor.py

Carl Zimmerman | May 2026
"""

import numpy as np
import json
from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime

# =============================================================================
# Z² FRAMEWORK CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # = 33.510321
Z = np.sqrt(Z_SQUARED)       # = 5.788810

# Cosmological parameters
OMEGA_M = 6 / 19             # = 0.315789
OMEGA_LAMBDA = 13 / 19       # = 0.684211

# MOND acceleration scale
A0_LOCAL = 1.20e-10  # m/s²

# Physical constants
G = 6.67430e-11      # m³/(kg·s²)
M_SUN = 1.989e30     # kg
C = 299792458        # m/s

# Geometric factor for spheroidal systems
F_GEOM = 1.5

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def E_of_z(z: float) -> float:
    """Normalized Hubble parameter E(z) = H(z)/H₀."""
    return np.sqrt(OMEGA_M * (1 + z)**3 + OMEGA_LAMBDA)

def a0_of_z(z: float) -> float:
    """MOND acceleration scale at redshift z."""
    return A0_LOCAL * E_of_z(z)

def sigma_dispersion(M_stellar: float, z: float, f_geom: float = F_GEOM) -> float:
    """
    Calculate velocity dispersion for a dispersion-supported system.

    Parameters:
        M_stellar: Stellar mass in solar masses
        z: Redshift
        f_geom: Geometric factor (default 1.5)

    Returns:
        Velocity dispersion in km/s
    """
    M_kg = M_stellar * M_SUN
    a0_z = a0_of_z(z)
    sigma_mps = (G * M_kg * a0_z) ** 0.25 / f_geom
    return sigma_mps / 1000  # Convert to km/s

def sigma_standard_mond(M_stellar: float, f_geom: float = F_GEOM) -> float:
    """Standard MOND prediction (constant a₀)."""
    M_kg = M_stellar * M_SUN
    sigma_mps = (G * M_kg * A0_LOCAL) ** 0.25 / f_geom
    return sigma_mps / 1000

def v_rotation(M_baryonic: float, z: float) -> float:
    """
    Calculate rotation velocity for a rotation-supported system.

    Parameters:
        M_baryonic: Baryonic mass in solar masses
        z: Redshift

    Returns:
        Rotation velocity in km/s
    """
    M_kg = M_baryonic * M_SUN
    a0_z = a0_of_z(z)
    v_mps = (G * M_kg * a0_z) ** 0.25
    return v_mps / 1000

def v_standard_mond(M_baryonic: float) -> float:
    """Standard MOND rotation velocity prediction."""
    M_kg = M_baryonic * M_SUN
    v_mps = (G * M_kg * A0_LOCAL) ** 0.25
    return v_mps / 1000

# =============================================================================
# GALAXY DATABASE
# =============================================================================

@dataclass
class Galaxy:
    """A high-z galaxy with known properties."""
    name: str
    redshift: float
    stellar_mass: float  # Solar masses
    mass_error_factor: float  # Factor uncertainty (e.g., 2 means 0.5-2x)
    status: str  # "verified", "awaiting", "upper_limit"
    observed_sigma: Optional[float] = None  # km/s if measured
    observed_sigma_plus: Optional[float] = None
    observed_sigma_minus: Optional[float] = None
    reference: str = ""
    notes: str = ""

# Database of known high-z galaxies
GALAXY_DATABASE = [
    Galaxy(
        name="GN-z11",
        redshift=10.603,
        stellar_mass=1e9,
        mass_error_factor=2,
        status="verified",
        observed_sigma=91,
        observed_sigma_plus=18,
        observed_sigma_minus=32,
        reference="Xu et al. (2024), ApJ 976, 142",
        notes="First z>10 kinematic detection. EXACT MATCH."
    ),
    Galaxy(
        name="GLASS-z12 (GHZ2)",
        redshift=12.34,
        stellar_mass=1e9,
        mass_error_factor=3,
        status="awaiting",
        reference="Naidu et al. (2022); Castellano et al. (2022)",
        notes="Second confirmed z>12 galaxy."
    ),
    Galaxy(
        name="JADES-GS-z14-0",
        redshift=14.1793,
        stellar_mass=5e8,
        mass_error_factor=3,
        status="upper_limit",
        observed_sigma=40,  # Upper limit
        reference="Robertson et al. (2024); Schouws et al. (2025)",
        notes="Most distant spectroscopically confirmed. Upper limit only."
    ),
    Galaxy(
        name="CEERS-1749",
        redshift=10.9,
        stellar_mass=3e10,
        mass_error_factor=2,
        status="awaiting",
        reference="Finkelstein et al. (2022)",
        notes="Very massive for this redshift."
    ),
    Galaxy(
        name="Maisie's Galaxy",
        redshift=11.44,
        stellar_mass=1e9,
        mass_error_factor=2,
        status="awaiting",
        reference="Finkelstein et al. (2023)",
        notes="Named after discoverer's daughter."
    ),
    Galaxy(
        name="UNCOVER-z13",
        redshift=13.0,
        stellar_mass=5e8,
        mass_error_factor=3,
        status="awaiting",
        reference="UNCOVER program",
        notes="Photometric redshift, awaiting spectroscopy."
    ),
    Galaxy(
        name="JADES-GS-z13-0",
        redshift=13.2,
        stellar_mass=1e8,
        mass_error_factor=3,
        status="awaiting",
        reference="JADES program",
        notes="Very compact."
    ),
    Galaxy(
        name="RXCJ2248-ID",
        redshift=10.0,
        stellar_mass=5e8,
        mass_error_factor=3,
        status="awaiting",
        reference="Lensed galaxy",
        notes="Lensed with magnification ~10."
    ),
]

# =============================================================================
# PREDICTION CALCULATOR
# =============================================================================

def calculate_predictions(galaxy: Galaxy) -> dict:
    """Calculate Z²-MOND and standard MOND predictions for a galaxy."""

    z = galaxy.redshift
    M = galaxy.stellar_mass

    # Z²-MOND predictions
    E = E_of_z(z)
    a0_z = a0_of_z(z)
    sigma_z2 = sigma_dispersion(M, z)
    v_rot_z2 = v_rotation(M, z)

    # Standard MOND predictions
    sigma_std = sigma_standard_mond(M)
    v_rot_std = v_standard_mond(M)

    # Uncertainties from mass uncertainty
    sigma_z2_low = sigma_dispersion(M / galaxy.mass_error_factor, z)
    sigma_z2_high = sigma_dispersion(M * galaxy.mass_error_factor, z)

    sigma_std_low = sigma_standard_mond(M / galaxy.mass_error_factor)
    sigma_std_high = sigma_standard_mond(M * galaxy.mass_error_factor)

    # Discrimination
    ratio = sigma_z2 / sigma_std
    discrimination_pct = (ratio - 1) * 100

    result = {
        "galaxy": galaxy.name,
        "redshift": z,
        "stellar_mass_Msun": M,
        "E_z": E,
        "a0_z_m_s2": a0_z,
        "z2_mond": {
            "sigma_v_km_s": sigma_z2,
            "sigma_v_range": [sigma_z2_low, sigma_z2_high],
            "v_rot_km_s": v_rot_z2,
        },
        "standard_mond": {
            "sigma_v_km_s": sigma_std,
            "sigma_v_range": [sigma_std_low, sigma_std_high],
            "v_rot_km_s": v_rot_std,
        },
        "discrimination": {
            "ratio": ratio,
            "difference_percent": discrimination_pct,
        },
        "status": galaxy.status,
    }

    if galaxy.observed_sigma is not None:
        result["observed"] = {
            "sigma_v_km_s": galaxy.observed_sigma,
            "error_plus": galaxy.observed_sigma_plus,
            "error_minus": galaxy.observed_sigma_minus,
        }

        # Calculate deviations
        err = (galaxy.observed_sigma_plus + galaxy.observed_sigma_minus) / 2 if galaxy.observed_sigma_minus else galaxy.observed_sigma_plus
        if err and err > 0:
            result["z2_mond"]["deviation_sigma"] = (sigma_z2 - galaxy.observed_sigma) / err
            result["standard_mond"]["deviation_sigma"] = (sigma_std - galaxy.observed_sigma) / err

    return result

# =============================================================================
# MAIN OUTPUT
# =============================================================================

def main():
    print("=" * 80)
    print("Z²-MOND KINEMATIC PREDICTIONS FOR HIGH-z GALAXIES")
    print("=" * 80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    print("Z² FRAMEWORK CONSTANTS")
    print("-" * 80)
    print(f"Z² = 32π/3 = {Z_SQUARED:.6f}")
    print(f"Z = √(Z²) = {Z:.6f}")
    print(f"a₀(0) = {A0_LOCAL:.2e} m/s²")
    print(f"Ω_m = 6/19 = {OMEGA_M:.6f}")
    print(f"Ω_Λ = 13/19 = {OMEGA_LAMBDA:.6f}")
    print()

    # Calculate all predictions
    all_predictions = []

    print("=" * 80)
    print("PREDICTIONS TABLE")
    print("=" * 80)
    print()

    print(f"{'Galaxy':<20} | {'z':>6} | {'M_★':>10} | {'E(z)':>6} | {'σ (Z²)':>10} | {'σ (std)':>10} | {'Diff':>8} | {'Status':>10}")
    print("-" * 110)

    for galaxy in sorted(GALAXY_DATABASE, key=lambda g: g.redshift):
        pred = calculate_predictions(galaxy)
        all_predictions.append(pred)

        sigma_z2 = pred["z2_mond"]["sigma_v_km_s"]
        sigma_std = pred["standard_mond"]["sigma_v_km_s"]
        diff_pct = pred["discrimination"]["difference_percent"]

        status_icon = "✓✓✓" if galaxy.status == "verified" else "..." if galaxy.status == "awaiting" else "↑lim"

        print(f"{galaxy.name:<20} | {galaxy.redshift:>6.2f} | {galaxy.stellar_mass:>10.1e} | {pred['E_z']:>6.1f} | {sigma_z2:>10.1f} | {sigma_std:>10.1f} | {diff_pct:>+7.0f}% | {status_icon:>10}")

    print()

    # Verified galaxy details
    print("=" * 80)
    print("VERIFIED PREDICTIONS")
    print("=" * 80)
    print()

    for galaxy in GALAXY_DATABASE:
        if galaxy.status == "verified":
            pred = calculate_predictions(galaxy)
            sigma_z2 = pred["z2_mond"]["sigma_v_km_s"]
            sigma_std = pred["standard_mond"]["sigma_v_km_s"]

            print(f"  {galaxy.name} (z = {galaxy.redshift}):")
            print(f"    Z²-MOND prediction:  σ = {sigma_z2:.1f} km/s")
            print(f"    Standard MOND:       σ = {sigma_std:.1f} km/s")
            print(f"    Observed:            σ = {galaxy.observed_sigma} (+{galaxy.observed_sigma_plus}/-{galaxy.observed_sigma_minus}) km/s")
            print()

            dev_z2 = pred["z2_mond"].get("deviation_sigma", 0)
            dev_std = pred["standard_mond"].get("deviation_sigma", 0)

            print(f"    Z²-MOND deviation:   {dev_z2:.2f}σ")
            print(f"    Std MOND deviation:  {dev_std:.2f}σ")
            print()

            if abs(dev_z2) < 0.5:
                print("    STATUS: ██████████ EXACT MATCH ██████████")
            elif abs(dev_z2) < 1:
                print("    STATUS: ████ EXCELLENT MATCH ████")
            print()

    # Awaiting measurements
    print("=" * 80)
    print("AWAITING MEASUREMENT")
    print("=" * 80)
    print()

    for galaxy in sorted(GALAXY_DATABASE, key=lambda g: g.redshift):
        if galaxy.status == "awaiting":
            pred = calculate_predictions(galaxy)
            sigma_z2 = pred["z2_mond"]["sigma_v_km_s"]
            sigma_std = pred["standard_mond"]["sigma_v_km_s"]

            print(f"  {galaxy.name} (z = {galaxy.redshift}):")
            print(f"    Z²-MOND prediction:  σ = {sigma_z2:.0f} ± {(pred['z2_mond']['sigma_v_range'][1] - sigma_z2):.0f} km/s")
            print(f"    Standard MOND:       σ = {sigma_std:.0f} ± {(pred['standard_mond']['sigma_v_range'][1] - sigma_std):.0f} km/s")
            print(f"    Discrimination:      {pred['discrimination']['difference_percent']:.0f}% difference")
            print()

    # Save to JSON
    output = {
        "generated": datetime.now().isoformat(),
        "z2_constants": {
            "Z_squared": Z_SQUARED,
            "Z": Z,
            "a0_local": A0_LOCAL,
            "Omega_m": OMEGA_M,
            "Omega_Lambda": OMEGA_LAMBDA,
        },
        "predictions": all_predictions,
    }

    output_file = "/Users/carlzimmerman/new_physics/zimmerman-formula/research/z2_mond_predictions/predictions_database.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print("=" * 80)
    print(f"Full predictions saved to: {output_file}")
    print("=" * 80)

# =============================================================================
# QUICK CALCULATOR
# =============================================================================

def predict_galaxy(name: str, z: float, M_stellar: float):
    """Quick prediction for a new galaxy."""
    galaxy = Galaxy(
        name=name,
        redshift=z,
        stellar_mass=M_stellar,
        mass_error_factor=2,
        status="new"
    )

    pred = calculate_predictions(galaxy)

    print(f"\n{name} (z = {z}, M_★ = {M_stellar:.1e} M_☉)")
    print(f"  E(z) = {pred['E_z']:.2f}")
    print(f"  a₀(z) = {pred['a0_z_m_s2']:.2e} m/s²")
    print(f"  Z²-MOND σ_v = {pred['z2_mond']['sigma_v_km_s']:.1f} km/s")
    print(f"  Std MOND σ_v = {pred['standard_mond']['sigma_v_km_s']:.1f} km/s")
    print(f"  Difference: {pred['discrimination']['difference_percent']:.0f}%")

    return pred

# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    main()

    # Example: predict for a hypothetical new galaxy
    print("\n" + "=" * 80)
    print("EXAMPLE: Predict for a new galaxy")
    print("=" * 80)
    predict_galaxy("Hypothetical-z15", z=15.0, M_stellar=1e9)
