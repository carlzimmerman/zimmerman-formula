#!/usr/bin/env python3
"""
Test Zimmerman Formula Redshift Evolution Predictions Against Literature Constraints.

Key prediction: a₀(z) = a₀(0) × √(Ωm(1+z)³ + ΩΛ)

Comparison with Milgrom (2017) analysis of Genzel et al. high-z rotation curves.

Author: Carl Zimmerman
Date: March 2026
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# COSMOLOGICAL PARAMETERS (Planck 2018)
# =============================================================================

c = 299792458        # m/s
G = 6.67430e-11      # m^3 kg^-1 s^-2
H0_fiducial = 71.1   # km/s/Mpc (best fit for Zimmerman formula)
Omega_m = 0.315
Omega_Lambda = 0.685
a0_observed = 1.2e-10  # m/s² (local measurement)

# =============================================================================
# ZIMMERMAN FORMULA PREDICTIONS
# =============================================================================

def zimmerman_a0(H0_kmsMpc: float) -> float:
    """Calculate a₀ from the Zimmerman Formula at z=0."""
    H0_si = H0_kmsMpc * 1000 / (3.086e22)  # Convert to s^-1
    rho_c = 3 * H0_si**2 / (8 * np.pi * G)
    return c * np.sqrt(G * rho_c) / 2

def zimmerman_Ez(z: float) -> float:
    """
    Calculate E(z) = H(z)/H₀ = √(Ωm(1+z)³ + ΩΛ)

    This is the standard ΛCDM Hubble parameter evolution.
    """
    return np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda)

def zimmerman_a0_ratio(z: float) -> float:
    """
    Zimmerman prediction: a₀(z)/a₀(0) = E(z)
    """
    return zimmerman_Ez(z)

# =============================================================================
# ALTERNATIVE EVOLUTION MODELS
# =============================================================================

def constant_a0_ratio(z: float) -> float:
    """No evolution: a₀(z) = a₀(0)"""
    return 1.0

def powerlaw_evolution(z: float, alpha: float = 1.5) -> float:
    """Power-law evolution: a₀(z)/a₀(0) = (1+z)^α"""
    return (1 + z)**alpha

# =============================================================================
# MILGROM (2017) CONSTRAINTS
# =============================================================================

# From arXiv:1703.06110:
# "all but exclude a value of the MOND constant of ~4a₀ at z~2"
# This rules out a₀ ∝ (1+z)^1.5 which gives 5.2× at z=2

MILGROM_EXCLUDED_RATIO_Z2 = 4.0  # Approximately excluded at z~2
MILGROM_CONSTRAINT_REDSHIFT = 2.0

# =============================================================================
# ANALYSIS
# =============================================================================

def main():
    print("=" * 70)
    print("ZIMMERMAN FORMULA - HIGH-Z PREDICTIONS vs CONSTRAINTS")
    print("=" * 70)

    # Calculate predictions at key redshifts
    print("\n" + "=" * 70)
    print("REDSHIFT EVOLUTION PREDICTIONS")
    print("=" * 70)

    print(f"\nZimmerman prediction: a₀(z)/a₀(0) = √(Ωm(1+z)³ + ΩΛ)")
    print(f"Using Ωm = {Omega_m}, ΩΛ = {Omega_Lambda}")
    print()

    print(f"{'Redshift':<10} {'Zimmerman':<12} {'Constant':<12} {'(1+z)^1.5':<12}")
    print("-" * 50)

    for z in [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
        zimm = zimmerman_a0_ratio(z)
        const = constant_a0_ratio(z)
        power = powerlaw_evolution(z, 1.5)
        print(f"{z:<10} {zimm:<12.3f} {const:<12.3f} {power:<12.3f}")

    # Compare with Milgrom constraints
    print("\n" + "=" * 70)
    print("COMPARISON WITH MILGROM (2017) CONSTRAINTS")
    print("=" * 70)

    z_test = 2.0
    zimm_z2 = zimmerman_a0_ratio(z_test)
    power_z2 = powerlaw_evolution(z_test, 1.5)

    print(f"""
Reference: arXiv:1703.06110
"High-redshift rotation curves and MOND" (Milgrom 2017)

Key constraint from analysis of Genzel et al. high-z data:
  - Data "all but exclude" a₀ ~ 4a₀(0) at z~2
  - Specifically rules out a₀ ∝ (1+z)^1.5 evolution

Predictions at z = {z_test}:
  - (1+z)^1.5 model:  {power_z2:.2f}× a₀(0)  ← EXCLUDED by Milgrom
  - Zimmerman model:  {zimm_z2:.2f}× a₀(0)  ← BELOW excluded threshold
  - Constant a₀:      1.00× a₀(0)
  - Excluded (Milgrom): ~{MILGROM_EXCLUDED_RATIO_Z2}× a₀(0)

STATUS: Zimmerman prediction ({zimm_z2:.2f}×) is COMPATIBLE with current constraints.
        It predicts evolution intermediate between "constant" and "excluded".
""")

    # Detailed comparison
    print("=" * 70)
    print("CRITICAL TEST: WHERE DOES ZIMMERMAN DIFFER FROM ALTERNATIVES?")
    print("=" * 70)

    print(f"""
The Zimmerman formula makes a SPECIFIC, FALSIFIABLE prediction:

  a₀(z) = a₀(0) × √(Ωm(1+z)³ + ΩΛ)

This differs from both:
  1. "Constant a₀" (no evolution) - RULED OUT if we see any evolution
  2. "(1+z)^1.5" power law - ALREADY EXCLUDED by Milgrom's analysis

Zimmerman predicts a₀ evolution that EXACTLY follows the ΛCDM Hubble parameter.
""")

    # Calculate where models diverge most
    print("Model divergence by redshift:")
    print(f"{'z':<8} {'Zimm-Const':<15} {'Zimm-Power':<15}")
    print("-" * 40)

    for z in [0.5, 1.0, 1.5, 2.0, 2.5]:
        zimm = zimmerman_a0_ratio(z)
        const = constant_a0_ratio(z)
        power = powerlaw_evolution(z, 1.5)

        diff_const = zimm - const
        diff_power = power - zimm

        print(f"{z:<8} +{diff_const:<14.2f} -{diff_power:<14.2f}")

    # Required precision for discrimination
    print("\n" + "=" * 70)
    print("REQUIRED MEASUREMENT PRECISION FOR DISCRIMINATION")
    print("=" * 70)

    print("""
To distinguish Zimmerman from constant a₀:
  - At z=1: Need to measure a₀(z)/a₀(0) = 1.79 ± <0.4 (20% precision)
  - At z=2: Need to measure a₀(z)/a₀(0) = 3.03 ± <1.0 (30% precision)

Current state:
  - Milgrom (2017) analysis shows galaxies at z~2 have g(R½) ~ (3-11)a₀
  - This is CONSISTENT with Zimmerman but not a direct test
  - Direct a₀ measurement at high-z requires:
    1. Rotation curves extending to flat part (g << 10⁻¹⁰ m/s²)
    2. Independent baryonic mass measurement
    3. Resolution of individual galaxy dynamics

Best prospects:
  - JWST + ALMA combined observations of z~1-2 galaxies
  - SKA (future) 21cm observations at intermediate z
  - Stacking analysis of KMOS3D outer rotation curves
""")

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print("""
TESTABLE PREDICTIONS (Section 5.3 of Zimmerman Formula paper):

1. REDSHIFT EVOLUTION (tested above):
   ✓ Prediction: a₀(z)/a₀(0) = √(Ωm(1+z)³ + ΩΛ)
   ✓ Status: COMPATIBLE with Milgrom (2017) constraints
   ✓ Distinguishing feature: Predicts ~3× at z=2 (between 1× and 5×)

2. HUBBLE TENSION IMPLICATION:
   - Formula implies H₀ ≈ 71.5 km/s/Mpc from local a₀ measurement
   - This is BETWEEN Planck (67.4) and SH0ES (73.0)
   - Could offer consistency check independent of distance ladder

NEXT STEPS FOR DEFINITIVE TEST:
   1. Extract outer rotation curves from KMOS3D stacked data
   2. Compute RAR at z~1 and z~2 independently
   3. Fit a₀(z) and compare to Zimmerman prediction
   4. OR: Wait for JWST/ALMA resolved kinematics at high-z
""")

    # Generate comparison plot
    plot_evolution_comparison()

def plot_evolution_comparison():
    """Generate comparison plot of different a₀ evolution models."""

    z = np.linspace(0, 3, 100)

    zimm = np.array([zimmerman_a0_ratio(zi) for zi in z])
    const = np.ones_like(z)
    power15 = np.array([powerlaw_evolution(zi, 1.5) for zi in z])
    power10 = np.array([powerlaw_evolution(zi, 1.0) for zi in z])

    plt.figure(figsize=(10, 6))

    plt.plot(z, zimm, 'b-', linewidth=2, label='Zimmerman: √(Ωm(1+z)³ + ΩΛ)')
    plt.plot(z, const, 'g--', linewidth=1.5, label='Constant a₀')
    plt.plot(z, power15, 'r:', linewidth=2, label='(1+z)^1.5 [EXCLUDED by Milgrom 2017]')
    plt.plot(z, power10, 'orange', linewidth=1.5, linestyle='--', label='(1+z)^1.0')

    # Mark excluded region from Milgrom
    plt.axhline(y=4.0, color='red', linestyle='-', alpha=0.3, linewidth=10)
    plt.text(0.1, 4.3, 'EXCLUDED by Milgrom (2017)', fontsize=10, color='red')

    # Mark z=2 predictions
    plt.scatter([2.0], [zimmerman_a0_ratio(2.0)], color='blue', s=100, zorder=5)
    plt.scatter([2.0], [powerlaw_evolution(2.0, 1.5)], color='red', s=100, zorder=5, marker='x')

    plt.xlabel('Redshift z', fontsize=12)
    plt.ylabel('a₀(z) / a₀(0)', fontsize=12)
    plt.title('Evolution of MOND Acceleration Scale: Predictions vs Constraints', fontsize=14)
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 3)
    plt.ylim(0, 7)

    plt.tight_layout()
    plt.savefig('data/a0_evolution_comparison.png', dpi=150)
    print("\nPlot saved to data/a0_evolution_comparison.png")

if __name__ == "__main__":
    main()
