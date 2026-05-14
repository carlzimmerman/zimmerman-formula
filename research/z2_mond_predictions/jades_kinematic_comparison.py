#!/usr/bin/env python3
"""
Z²-MOND PREDICTIONS vs JADES MEASURED KINEMATICS
=================================================

Compares Z²-MOND predictions to actually MEASURED velocity dispersions
from de Graaff et al. (2024) A&A, arXiv:2308.09742

These are z ~ 5.5-7.4 galaxies with NIRSpec high-resolution spectroscopy.

Carl Zimmerman | May 2026
"""

import numpy as np
import json
from dataclasses import dataclass, asdict
from typing import Optional
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

# Geometric factor for dispersion-dominated systems
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

def sigma_z2_mond(M_stellar: float, z: float, f_geom: float = F_GEOM) -> float:
    """Z²-MOND velocity dispersion prediction."""
    M_kg = M_stellar * M_SUN
    a0_z = a0_of_z(z)
    sigma_mps = (G * M_kg * a0_z) ** 0.25 / f_geom
    return sigma_mps / 1000  # Convert to km/s

def sigma_standard_mond(M_stellar: float, f_geom: float = F_GEOM) -> float:
    """Standard MOND prediction (constant a₀)."""
    M_kg = M_stellar * M_SUN
    sigma_mps = (G * M_kg * A0_LOCAL) ** 0.25 / f_geom
    return sigma_mps / 1000

# =============================================================================
# JADES KINEMATIC SAMPLE (de Graaff et al. 2024)
# =============================================================================

@dataclass
class JADESGalaxy:
    """Galaxy from JADES kinematic sample."""
    galaxy_id: str
    redshift: float
    log_stellar_mass: float  # log10(M*/M_sun)
    observed_sigma: float    # km/s
    observed_sigma_err: float
    observed_v_rot: float    # km/s
    observed_v_rot_err: float
    dynamics: str  # "rotation" or "dispersion"
    reference: str = "de Graaff et al. (2024), A&A 684, A87"

# The actual measured sample from arXiv:2308.09742
JADES_SAMPLE = [
    JADESGalaxy(
        galaxy_id="JADES-NS-00016745",
        redshift=5.566,
        log_stellar_mass=8.80,
        observed_sigma=55,
        observed_sigma_err=2,
        observed_v_rot=105,
        observed_v_rot_err=13,
        dynamics="rotation"
    ),
    JADESGalaxy(
        galaxy_id="JADES-NS-00019606",
        redshift=5.890,
        log_stellar_mass=7.54,
        observed_sigma=39.1,
        observed_sigma_err=1.8,
        observed_v_rot=5,
        observed_v_rot_err=5,
        dynamics="dispersion"
    ),
    JADESGalaxy(
        galaxy_id="JADES-NS-00022251",
        redshift=5.799,
        log_stellar_mass=8.21,
        observed_sigma=39.0,
        observed_sigma_err=1.0,
        observed_v_rot=23,
        observed_v_rot_err=4,
        dynamics="dispersion"
    ),
    JADESGalaxy(
        galaxy_id="JADES-NS-00047100",
        redshift=7.432,
        log_stellar_mass=8.53,
        observed_sigma=71,
        observed_sigma_err=4,
        observed_v_rot=91,
        observed_v_rot_err=19,
        dynamics="rotation"
    ),
    JADESGalaxy(
        galaxy_id="JADES-NS-10016374",
        redshift=5.504,
        log_stellar_mass=7.86,
        observed_sigma=62,
        observed_sigma_err=2,
        observed_v_rot=16,
        observed_v_rot_err=10,
        dynamics="dispersion"
    ),
    JADESGalaxy(
        galaxy_id="JADES-NS-20086025",
        redshift=7.263,
        log_stellar_mass=8.85,
        observed_sigma=25,
        observed_sigma_err=7,
        observed_v_rot=155,
        observed_v_rot_err=18,
        dynamics="rotation"
    ),
]

# =============================================================================
# PREDICTION CALCULATOR
# =============================================================================

def calculate_jades_predictions(galaxy: JADESGalaxy) -> dict:
    """Calculate Z²-MOND and standard MOND predictions for a JADES galaxy."""

    z = galaxy.redshift
    M_stellar = 10 ** galaxy.log_stellar_mass  # Convert from log

    # E(z) and a₀(z)
    E = E_of_z(z)
    a0_z = a0_of_z(z)

    # Z²-MOND prediction
    sigma_z2 = sigma_z2_mond(M_stellar, z)

    # Standard MOND prediction
    sigma_std = sigma_standard_mond(M_stellar)

    # Ratio and discrimination
    ratio = sigma_z2 / sigma_std
    discrimination_pct = (ratio - 1) * 100

    # Compare to observation
    obs_sigma = galaxy.observed_sigma
    obs_err = galaxy.observed_sigma_err

    # Deviations in sigma
    dev_z2 = (sigma_z2 - obs_sigma) / obs_err
    dev_std = (sigma_std - obs_sigma) / obs_err

    return {
        "galaxy_id": galaxy.galaxy_id,
        "redshift": z,
        "stellar_mass_Msun": M_stellar,
        "log_stellar_mass": galaxy.log_stellar_mass,
        "dynamics": galaxy.dynamics,
        "E_z": E,
        "a0_z_m_s2": a0_z,
        "z2_mond": {
            "sigma_v_km_s": sigma_z2,
            "deviation_from_obs_sigma": dev_z2,
        },
        "standard_mond": {
            "sigma_v_km_s": sigma_std,
            "deviation_from_obs_sigma": dev_std,
        },
        "observed": {
            "sigma_v_km_s": obs_sigma,
            "sigma_v_err": obs_err,
            "v_rot_km_s": galaxy.observed_v_rot,
            "v_rot_err": galaxy.observed_v_rot_err,
        },
        "discrimination": {
            "z2_over_std_ratio": ratio,
            "difference_percent": discrimination_pct,
        },
    }

# =============================================================================
# MAIN OUTPUT
# =============================================================================

def main():
    print("=" * 90)
    print("Z²-MOND vs MEASURED KINEMATICS: JADES SAMPLE (de Graaff et al. 2024)")
    print("=" * 90)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    print("Z² FRAMEWORK CONSTANTS")
    print("-" * 90)
    print(f"Z² = 32π/3 = {Z_SQUARED:.6f}")
    print(f"a₀(z) = a₀(0) × E(z), where E(z) = √[Ω_m(1+z)³ + Ω_Λ]")
    print(f"a₀(0) = {A0_LOCAL:.2e} m/s²")
    print(f"Ω_m = 6/19 = {OMEGA_M:.6f}")
    print(f"Ω_Λ = 13/19 = {OMEGA_LAMBDA:.6f}")
    print()

    # Calculate predictions
    all_results = []

    print("=" * 90)
    print("COMPARISON TABLE")
    print("=" * 90)
    print()

    header = f"{'Galaxy ID':<22} | {'z':>5} | {'log M★':>7} | {'E(z)':>5} | {'σ obs':>8} | {'σ Z²':>8} | {'σ std':>8} | {'Δ Z²':>6} | {'Δ std':>6}"
    print(header)
    print("-" * 90)

    # Statistics accumulators
    z2_deviations = []
    std_deviations = []

    for galaxy in sorted(JADES_SAMPLE, key=lambda g: g.redshift):
        result = calculate_jades_predictions(galaxy)
        all_results.append(result)

        sigma_z2 = result["z2_mond"]["sigma_v_km_s"]
        sigma_std = result["standard_mond"]["sigma_v_km_s"]
        sigma_obs = result["observed"]["sigma_v_km_s"]
        sigma_err = result["observed"]["sigma_v_err"]

        dev_z2 = result["z2_mond"]["deviation_from_obs_sigma"]
        dev_std = result["standard_mond"]["deviation_from_obs_sigma"]

        z2_deviations.append(abs(dev_z2))
        std_deviations.append(abs(dev_std))

        print(f"{galaxy.galaxy_id:<22} | {galaxy.redshift:>5.3f} | {galaxy.log_stellar_mass:>7.2f} | {result['E_z']:>5.1f} | {sigma_obs:>5.0f}±{sigma_err:<2.0f} | {sigma_z2:>8.1f} | {sigma_std:>8.1f} | {dev_z2:>+5.1f}σ | {dev_std:>+5.1f}σ")

    print()

    # Statistics
    mean_z2_dev = np.mean(z2_deviations)
    mean_std_dev = np.mean(std_deviations)

    print("=" * 90)
    print("STATISTICAL SUMMARY")
    print("=" * 90)
    print()
    print(f"Mean |deviation| from observed:")
    print(f"  Z²-MOND:       {mean_z2_dev:.2f}σ")
    print(f"  Standard MOND: {mean_std_dev:.2f}σ")
    print()

    # Detailed analysis
    print("=" * 90)
    print("DETAILED ANALYSIS")
    print("=" * 90)
    print()

    for result in sorted(all_results, key=lambda r: r["redshift"]):
        sigma_z2 = result["z2_mond"]["sigma_v_km_s"]
        sigma_std = result["standard_mond"]["sigma_v_km_s"]
        sigma_obs = result["observed"]["sigma_v_km_s"]
        sigma_err = result["observed"]["sigma_v_err"]

        print(f"{result['galaxy_id']} (z = {result['redshift']:.3f}, {result['dynamics']}-dominated):")
        print(f"  Stellar mass: {result['stellar_mass_Msun']:.2e} M☉")
        print(f"  E(z) = {result['E_z']:.2f} → a₀(z) = {result['a0_z_m_s2']:.2e} m/s²")
        print(f"  Z²-MOND σ:     {sigma_z2:>6.1f} km/s ({result['z2_mond']['deviation_from_obs_sigma']:>+5.1f}σ from obs)")
        print(f"  Standard σ:    {sigma_std:>6.1f} km/s ({result['standard_mond']['deviation_from_obs_sigma']:>+5.1f}σ from obs)")
        print(f"  Observed σ:    {sigma_obs:>6.0f} ± {sigma_err:.0f} km/s")
        print(f"  Z² enhancement: {result['discrimination']['difference_percent']:.0f}%")

        # Assessment
        dev_z2 = abs(result["z2_mond"]["deviation_from_obs_sigma"])
        dev_std = abs(result["standard_mond"]["deviation_from_obs_sigma"])

        if dev_z2 < 1.5 and dev_std > 3:
            print(f"  ★ STRONGLY FAVORS Z²-MOND")
        elif dev_z2 < dev_std:
            print(f"  → Favors Z²-MOND")
        elif dev_std < dev_z2:
            print(f"  → Favors standard MOND")
        else:
            print(f"  → Inconclusive")
        print()

    # Key insight
    print("=" * 90)
    print("KEY INSIGHT: MASS UNCERTAINTY")
    print("=" * 90)
    print("""
The JADES sample has typical stellar mass uncertainties of ~0.3-0.5 dex.
Since σ ∝ M^0.25, a 0.5 dex mass uncertainty translates to:
  σ uncertainty = 10^(0.5 × 0.25) - 1 = 33%

This is comparable to the Z²-MOND enhancement at z ~ 6 (70-80%).

IMPORTANT: The observed σ values may be affected by:
1. Stellar mass uncertainties (systematic)
2. Gas fraction (these are likely gas-rich)
3. Geometric factors (inclination, morphology)
4. Outflows/inflows affecting line widths

The de Graaff et al. finding that M_dyn >> M_stellar by factors of 10-40
suggests either:
- Significant dark matter in these systems
- Stellar mass underestimation
- OR: Enhanced gravity (like Z²-MOND predicts!)
""")

    # Save to JSON
    output = {
        "generated": datetime.now().isoformat(),
        "source": "de Graaff et al. (2024), A&A 684, A87; arXiv:2308.09742",
        "z2_constants": {
            "Z_squared": Z_SQUARED,
            "a0_local": A0_LOCAL,
            "Omega_m": OMEGA_M,
            "Omega_Lambda": OMEGA_LAMBDA,
        },
        "statistics": {
            "mean_abs_deviation_z2_mond": mean_z2_dev,
            "mean_abs_deviation_std_mond": mean_std_dev,
            "n_galaxies": len(all_results),
        },
        "predictions": all_results,
    }

    output_file = "/Users/carlzimmerman/new_physics/zimmerman-formula/research/z2_mond_predictions/jades_comparison.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print()
    print("=" * 90)
    print(f"Full results saved to: {output_file}")
    print("=" * 90)

if __name__ == "__main__":
    main()
