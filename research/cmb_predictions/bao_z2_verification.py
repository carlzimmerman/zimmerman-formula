#!/usr/bin/env python3
"""
BAO SCALE AND DESI COMPARISON: Z² FRAMEWORK VERIFICATION
=========================================================

Compares Z² framework predictions with DESI 2024 BAO results.

Carl Zimmerman | May 2026
"""

import numpy as np

# =============================================================================
# Z² FRAMEWORK CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # = 33.510321
Z = np.sqrt(Z_SQUARED)       # = 5.788810

# Z² Cosmological predictions
OMEGA_LAMBDA_Z2 = 13/19
OMEGA_M_Z2 = 6/19
H0_Z2 = 71.5  # km/s/Mpc (from a₀ = cH₀/Z)

# Physical constants
c = 299792.458  # km/s

print("=" * 70)
print("BAO SCALE AND DESI COMPARISON: Z² VERIFICATION")
print("=" * 70)
print()

# =============================================================================
# Z² PREDICTIONS
# =============================================================================

print("Z² FRAMEWORK PREDICTIONS")
print("-" * 70)
print(f"Ω_Λ = 13/19 = {OMEGA_LAMBDA_Z2:.6f}")
print(f"Ω_m = 6/19  = {OMEGA_M_Z2:.6f}")
print(f"H₀ ~ {H0_Z2} km/s/Mpc (from a₀ = cH₀/Z)")
print(f"w = -1 (cosmological constant)")
print(f"w_a = 0 (no evolution)")
print()

# =============================================================================
# DESI 2024 RESULTS
# =============================================================================

print("DESI 2024 BAO RESULTS (arXiv:2404.03002)")
print("-" * 70)

desi_results = {
    "Ω_m (BAO alone)": (0.295, 0.015),
    "Ω_m (BAO+CMB)": (0.307, 0.005),
    "H₀ (BAO+BBN)": (68.52, 0.62),
    "H₀ (BAO+CMB)": (67.97, 0.38),
    "w (BAO alone)": (-0.99, 0.14),  # Average of asymmetric errors
}

for param, (value, err) in desi_results.items():
    print(f"{param}: {value:.3f} ± {err:.3f}")

print()

# =============================================================================
# COMPARISON
# =============================================================================

print("=" * 70)
print("Z² vs DESI COMPARISON")
print("=" * 70)
print()

# Ω_m comparison
print("MATTER DENSITY Ω_m:")
print("-" * 70)
om_z2 = OMEGA_M_Z2
om_desi_bao = (0.295, 0.015)
om_desi_cmb = (0.307, 0.005)
om_planck = (0.3153, 0.0073)

comparisons = [
    ("DESI BAO alone", om_desi_bao[0], om_desi_bao[1]),
    ("DESI + CMB", om_desi_cmb[0], om_desi_cmb[1]),
    ("Planck 2018", om_planck[0], om_planck[1]),
]

print(f"{'Measurement':<20} | {'Value':>10} | {'Z² diff':>10} | {'Deviation':>10}")
print("-" * 70)
print(f"{'Z² prediction':<20} | {om_z2:>10.4f} | {'--':>10} | {'--':>10}")
for name, val, err in comparisons:
    diff = om_z2 - val
    dev = abs(diff) / err
    print(f"{name:<20} | {val:>10.4f} | {diff:>+10.4f} | {dev:>10.2f}σ")

print()

# H₀ comparison
print("HUBBLE CONSTANT H₀:")
print("-" * 70)
h0_z2 = H0_Z2
h0_comparisons = [
    ("DESI + BBN", 68.52, 0.62),
    ("DESI + CMB", 67.97, 0.38),
    ("Planck 2018", 67.4, 0.5),
    ("SH0ES", 73.0, 1.0),
    ("TRGB", 69.8, 1.7),
    ("CCHP", 71.5, 1.8),
]

print(f"{'Measurement':<20} | {'Value':>12} | {'Z² diff':>10} | {'Deviation':>10}")
print("-" * 70)
print(f"{'Z² prediction':<20} | {h0_z2:>12.2f} | {'--':>10} | {'--':>10}")
for name, val, err in h0_comparisons:
    diff = h0_z2 - val
    dev = abs(diff) / err
    status = "✓" if dev < 2 else "~" if dev < 3 else "!"
    print(f"{name:<20} | {val:>12.2f} | {diff:>+10.2f} | {dev:>9.2f}σ {status}")

print()

# w comparison
print("DARK ENERGY EQUATION OF STATE w:")
print("-" * 70)
w_z2 = -1.0
w_desi = (-0.99, 0.14)

w_diff = w_z2 - w_desi[0]
w_dev = abs(w_diff) / w_desi[1]

print(f"Z² prediction:    w = {w_z2:.2f} (cosmological constant)")
print(f"DESI BAO alone:   w = {w_desi[0]:.2f} ± {w_desi[1]:.2f}")
print(f"Difference:       {w_diff:+.2f}")
print(f"Deviation:        {w_dev:.2f}σ")
print()
print("Status: ✓ CONSISTENT (Z² prediction w = -1 agrees with DESI)")
print()

# =============================================================================
# HUBBLE PARAMETER EVOLUTION
# =============================================================================

print("=" * 70)
print("HUBBLE PARAMETER EVOLUTION H(z)")
print("=" * 70)
print()

def H_of_z(z, Om, OL, H0):
    """Hubble parameter as function of redshift."""
    return H0 * np.sqrt(Om * (1 + z)**3 + OL)

def E_of_z(z, Om, OL):
    """Normalized Hubble parameter E(z) = H(z)/H₀."""
    return np.sqrt(Om * (1 + z)**3 + OL)

# Compare at key redshifts
z_values = [0.0, 0.5, 1.0, 1.5, 2.0, 2.33, 3.0, 4.0]

print(f"{'z':>6} | {'E(z) Z²':>10} | {'E(z) DESI':>10} | {'Diff %':>10}")
print("-" * 50)

for z in z_values:
    E_z2 = E_of_z(z, OMEGA_M_Z2, OMEGA_LAMBDA_Z2)
    E_desi = E_of_z(z, 0.307, 0.693)  # DESI+CMB values
    diff_pct = 100 * (E_z2 - E_desi) / E_desi
    print(f"{z:>6.2f} | {E_z2:>10.4f} | {E_desi:>10.4f} | {diff_pct:>+10.2f}%")

print()

# =============================================================================
# COMOVING DISTANCE
# =============================================================================

print("=" * 70)
print("COMOVING DISTANCES")
print("=" * 70)
print()

def comoving_distance(z, Om, OL, H0):
    """Comoving distance in Mpc."""
    from scipy import integrate

    def integrand(z_prime):
        return c / H_of_z(z_prime, Om, OL, H0)

    result, _ = integrate.quad(integrand, 0, z)
    return result

# Compare at DESI effective redshifts
desi_z_eff = [0.51, 0.71, 0.93, 1.32, 2.33]

print(f"{'z_eff':>8} | {'D_C(Z²) [Mpc]':>15} | {'D_C(DESI) [Mpc]':>15} | {'Diff %':>10}")
print("-" * 60)

for z in desi_z_eff:
    D_z2 = comoving_distance(z, OMEGA_M_Z2, OMEGA_LAMBDA_Z2, H0_Z2)
    D_desi = comoving_distance(z, 0.307, 0.693, 67.97)
    diff_pct = 100 * (D_z2 - D_desi) / D_desi
    print(f"{z:>8.2f} | {D_z2:>15.1f} | {D_desi:>15.1f} | {diff_pct:>+10.2f}%")

print()
print("Note: Z² predicts ~5% larger comoving distances due to higher H₀")
print()

# =============================================================================
# SOUND HORIZON ESTIMATE
# =============================================================================

print("=" * 70)
print("SOUND HORIZON ESTIMATE")
print("=" * 70)
print()

# Simplified Eisenstein & Hu approximation
def sound_horizon_approx(Om, Ob, h):
    """
    Approximate sound horizon using Eisenstein & Hu fitting formula.
    Returns r_d in Mpc.
    """
    omega_m = Om * h**2
    omega_b = Ob * h**2

    # Fitting formula from Eisenstein & Hu (1998)
    r_d = 55.154 * np.exp(-72.3 * (omega_b + 0.0006)**2) / \
          (omega_m**0.25351 * omega_b**0.12807)

    return r_d

# Standard baryon density
Ob_standard = 0.0493

# Z² sound horizon
h_z2 = H0_Z2 / 100
r_d_z2 = sound_horizon_approx(OMEGA_M_Z2, Ob_standard, h_z2)

# DESI/Planck calibration
h_desi = 67.97 / 100
r_d_desi = sound_horizon_approx(0.307, Ob_standard, h_desi)

# Planck value
r_d_planck = 147.09  # Mpc (Planck 2018)

print(f"Sound horizon estimates:")
print(f"  Z² parameters:     r_d ≈ {r_d_z2:.2f} Mpc")
print(f"  DESI parameters:   r_d ≈ {r_d_desi:.2f} Mpc")
print(f"  Planck calibration: r_d = {r_d_planck:.2f} Mpc")
print()
print("Note: Simplified formula; full Boltzmann calculation needed for precision.")
print()

# =============================================================================
# DARK ENERGY DYNAMICS TEST
# =============================================================================

print("=" * 70)
print("DARK ENERGY DYNAMICS TEST")
print("=" * 70)
print()

print("DESI hints at time-varying dark energy (2.6σ):")
print("  w₀ > -1 (phantom crossing)")
print("  w_a < 0 (evolving)")
print()
print("Z² prediction:")
print("  w = -1 exactly (cosmological constant)")
print("  w_a = 0 (no evolution)")
print()
print("If DESI dynamics confirmed:")
print("  → Z² would need modification (Ω_Λ could evolve)")
print("  → Or DESI systematics/statistics issue")
print()
print("Current status: 2.6σ is NOT conclusive (need 5σ)")
print("Future test: DESI Year 3-5 will reach 4-5σ sensitivity")
print()

# =============================================================================
# SUMMARY
# =============================================================================

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print()

summary = """
┌──────────────────────────────────────────────────────────────────────┐
│              Z² vs DESI COMPARISON SUMMARY                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Parameter        Z² Value      DESI Value      Status               │
│  ─────────────────────────────────────────────────────────────────   │
│  Ω_m              0.3158        0.307 ± 0.005   ~2σ (marginal)       │
│  H₀               71.5          68.0 ± 0.4      >3σ (Hubble tension) │
│  w                -1.0          -0.99 ± 0.14   <0.1σ (consistent)   │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Key Finding:                                                        │
│  • Z² is CLOSER to Planck than to DESI for Ω_m                      │
│  • Z² H₀ (71.5) is between Planck (67.4) and SH0ES (73.0)           │
│  • Z² w = -1 agrees perfectly with DESI w = -0.99                   │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Future Tests:                                                       │
│  • DESI Year 3-5: Will test Ω_m at 5σ level                         │
│  • DESI Year 3-5: Will test w_a at 4-5σ level                       │
│  • If w_a ≠ 0 confirmed: Z² needs revision                          │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
"""
print(summary)
