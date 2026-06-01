#!/usr/bin/env python3
"""
TESTABLE COSMOLOGICAL PREDICTIONS

These are predictions that can be FALSIFIED by observations.
If wrong, the framework is wrong. If right, it's evidence for real physics.

Carl Zimmerman | March 2026
"""

import numpy as np

print("=" * 70)
print("TESTABLE PREDICTIONS OF THE ZIMMERMAN FRAMEWORK")
print("=" * 70)

# Constants
c = 299792458  # m/s
Z = 2 * np.sqrt(8 * np.pi / 3)
H0_Planck = 67.4  # km/s/Mpc
H0_SH0ES = 73.0   # km/s/Mpc
a0_local = 1.2e-10  # m/s²

# Convert H0 to SI
H0_SI = 70 * 1000 / (3.086e22)  # s^-1

print(f"\nZ = 2√(8π/3) = {Z:.6f}")

# ============================================================================
print("\n" + "=" * 70)
print("PREDICTION 1: THE HUBBLE CONSTANT")
print("=" * 70)

# From a₀ = c × H₀ / Z
H0_predicted = Z * a0_local / c  # in s^-1
H0_predicted_kms = H0_predicted * 3.086e22 / 1000  # in km/s/Mpc

print(f"""
THE FORMULA:
  a₀ = c × H₀ / Z

Therefore:
  H₀ = Z × a₀ / c

PREDICTION:
  H₀ = {Z:.4f} × {a0_local:.2e} / {c}
     = {H0_predicted:.4e} s⁻¹
     = {H0_predicted_kms:.1f} km/s/Mpc

COMPARISON:
  Planck (CMB):     H₀ = {H0_Planck} km/s/Mpc
  SH0ES (local):    H₀ = {H0_SH0ES} km/s/Mpc
  Zimmerman:        H₀ = {H0_predicted_kms:.1f} km/s/Mpc

SIGNIFICANCE:
  The predicted value {H0_predicted_kms:.1f} is BETWEEN Planck and SH0ES.
  If confirmed, this resolves the Hubble tension.

HOW TO TEST:
  • Independent H₀ measurement (e.g., gravitational waves)
  • Improved a₀ measurement from local dynamics
  • Cross-check: if a₀ measured more precisely, H₀ is predicted exactly
""")

# ============================================================================
print("=" * 70)
print("PREDICTION 2: MOND ACCELERATION EVOLVES WITH REDSHIFT")
print("=" * 70)

def a0_at_z(z, Omega_m=0.315, Omega_Lambda=0.685):
    """MOND acceleration at redshift z"""
    E_z = np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda)
    return a0_local * E_z

# Calculate for various redshifts
redshifts = [0, 0.5, 1, 2, 3, 5, 10, 20]

print(f"""
THE FORMULA:
  a₀(z) = a₀(0) × E(z)

where E(z) = √(Ωₘ(1+z)³ + Ω_Λ)

This comes from a₀ ∝ H(z), and H(z) = H₀ × E(z).

PREDICTIONS:

  Redshift    E(z)      a₀(z)/a₀(0)    a₀(z) [m/s²]
  --------    -----     -----------    ------------""")

for z in redshifts:
    E_z = np.sqrt(0.315 * (1 + z)**3 + 0.685)
    a0_z = a0_at_z(z)
    print(f"  z = {z:4}     {E_z:5.2f}     {E_z:7.2f}×        {a0_z:.2e}")

print(f"""
OBSERVATIONAL CONSEQUENCES:

1. BARYONIC TULLY-FISHER RELATION (BTFR):
   M_bar = v⁴/(G × a₀)

   At higher z, a₀ is larger, so for the same v⁴:
   • M_bar appears SMALLER (less baryonic mass needed)
   • Or equivalently: v⁴/M_bar appears LARGER

   Prediction: BTFR normalization shifts DOWN at high z

   At z=2: shift of {np.log10(1/a0_at_z(2) * a0_local):.2f} dex in log M_bar

2. RADIAL ACCELERATION RELATION (RAR):
   The transition scale g† = a₀ shifts with z

   At z=2: g† is {a0_at_z(2)/a0_local:.1f}× higher
   This changes where galaxies transition to MOND regime

3. ROTATION CURVES:
   The asymptotic velocity v_flat = (G M_bar a₀)^(1/4)

   At higher z with higher a₀:
   v_flat should be HIGHER for the same M_bar
   Or: M_bar/v⁴ should be LOWER

HOW TO TEST:
  • JWST spectroscopy of z>2 galaxies (rotation curves)
  • Compare BTFR at z=0, z=1, z=2
  • ALMA/VLA kinematics of high-z systems
""")

# ============================================================================
print("=" * 70)
print("PREDICTION 3: EARLY UNIVERSE MASS DISCREPANCIES")
print("=" * 70)

print(f"""
THE PREDICTION:

In MOND, the mass discrepancy D = M_dynamic / M_baryonic depends on a₀.

For a system in the deep MOND regime (g << a₀):
  D ∝ 1/√a₀

At higher redshift, a₀ is LARGER, so D is SMALLER.

Wait - this seems backwards from "more dark matter at high z"...

Let me reconsider:

Actually, the MOND formula gives:
  M_dynamic = M_baryonic × μ(g/a₀)

In deep MOND: μ(x) → x, so
  M_dynamic = M_baryonic × (g/a₀)
            = M_baryonic × (v²/r)/a₀

For a fixed observed v and r:
  If a₀ increases, M_dynamic DECREASES relative to Newtonian expectation

But what we observe is: at high z, galaxies seem to have MORE mass
than expected for their baryons. This is the "JWST surprise."

RESOLUTION:

The JWST surprise is that galaxies FORMED too fast.
With higher a₀ at high z:
  • MOND effects are weaker (closer to Newtonian)
  • BUT the critical density is higher
  • AND structure formation is enhanced

Actually, let me think about this more carefully...

In standard MOND (constant a₀):
  • Low surface brightness → more MOND → more "dark matter"

In evolving a₀:
  • At high z, a₀ is higher
  • The MOND transition happens at higher g
  • Systems that would be in MOND regime locally are in Newtonian regime at high z

This means:
  • High-z galaxies should show LESS mass discrepancy (more Newtonian)
  • But they formed FASTER because a₀ acts like enhanced gravity

The "impossible early galaxies" puzzle:
  • ΛCDM: needs >100% efficiency or new physics
  • Zimmerman: higher a₀ → faster collapse → earlier formation

QUANTITATIVE PREDICTION:

The MOND "boost" to gravity in the transition regime goes as √(a₀/g).
At z=10, a₀ is ~20× higher.
The effective gravity boost is ~√20 ≈ 4.5× higher.
Collapse timescale ∝ 1/√(Gρ_eff), so ~2× faster.

This is testable with JWST galaxy formation timescales.
""")

# ============================================================================
print("=" * 70)
print("PREDICTION 4: COSMOLOGICAL PARAMETERS")
print("=" * 70)

Omega_Lambda_pred = 3 * Z / (8 + 3 * Z)
Omega_m_pred = 8 / (8 + 3 * Z)

print(f"""
THE FORMULAS:
  Ω_Λ = 3Z / (8 + 3Z) = {Omega_Lambda_pred:.4f}
  Ω_m = 8 / (8 + 3Z) = {Omega_m_pred:.4f}

  Note: Ω_Λ + Ω_m = (3Z + 8) / (8 + 3Z) = 1 ✓

MEASURED VALUES (Planck 2018):
  Ω_Λ = 0.6847 ± 0.0073
  Ω_m = 0.3153 ± 0.0073

COMPARISON:
  Ω_Λ: predicted {Omega_Lambda_pred:.4f}, measured 0.6847, error {abs(Omega_Lambda_pred - 0.6847)/0.6847*100:.2f}%
  Ω_m: predicted {Omega_m_pred:.4f}, measured 0.3153, error {abs(Omega_m_pred - 0.3153)/0.3153*100:.2f}%

SIGNIFICANCE:
  These predictions are within the measurement uncertainty!

  But this is NOT independent - the formulas were constructed to fit.
  The test is whether FUTURE measurements remain consistent.

HOW TO TEST:
  • Next-generation CMB (CMB-S4)
  • Improved BAO measurements
  • Check if Ω_m, Ω_Λ remain at these exact values
""")

# ============================================================================
print("=" * 70)
print("PREDICTION 5: WIDE BINARY STARS")
print("=" * 70)

print(f"""
THE PREDICTION:

Wide binary stars with separations > 1000 AU probe gravity
at accelerations g < a₀.

If MOND is correct (with a₀ from Zimmerman):
  • Binaries should show enhanced orbital velocities
  • The enhancement follows the MOND interpolating function

SPECIFIC PREDICTION:

For a binary with separation s and g_N = GM/s²:

If g_N < a₀:
  v_observed / v_Newtonian = (a₀/g_N)^(1/4)

At s = 10,000 AU around a solar-mass star:
  g_N ≈ GM/s² = 6.67e-11 × 2e30 / (10000 × 1.5e11)² = 6e-14 m/s²

  This is much less than a₀ = 1.2e-10 m/s²

  Predicted boost: (1.2e-10 / 6e-14)^0.25 = {(1.2e-10 / 6e-14)**0.25:.1f}×

CURRENT STATUS:

Gaia DR3 data shows:
  • Some evidence for MOND-like behavior (Chae 2023)
  • Disputed by other analyses (Banik et al.)

The Zimmerman framework predicts:
  • a₀ = 1.2×10⁻¹⁰ m/s² (same as standard MOND)
  • Wide binaries SHOULD show the MOND effect
  • If they don't, both MOND and Zimmerman are falsified for local physics

HOW TO TEST:
  • Gaia DR4 with improved proper motions
  • Careful treatment of systematics
  • Focus on cleanest systems (no companions, known distances)
""")

# ============================================================================
print("=" * 70)
print("PREDICTION 6: THE STRONG COUPLING AT HIGH ENERGY")
print("=" * 70)

alpha_s_pred = 3 / (8 + 3 * Z)

print(f"""
THE FORMULA:
  α_s = 3 / (8 + 3Z) = {alpha_s_pred:.4f}

MEASURED VALUE:
  α_s(M_Z) = 0.1180 ± 0.0010

COMPARISON:
  Predicted: {alpha_s_pred:.4f}
  Measured:  0.1180
  Error: {abs(alpha_s_pred - 0.1180)/0.1180*100:.2f}%

THE CONNECTION:

The shared denominator (8 + 3Z) with Ω_m suggests:
  α_s = (3/8) × Ω_m

This would mean α_s and Ω_m are fundamentally related!

TESTABLE ASPECT:

α_s runs with energy (asymptotic freedom).
At different energy scales:
  α_s(μ) = α_s(M_Z) × f(μ/M_Z)

If the Zimmerman formula is fundamental:
  • α_s should approach 3/(8+3Z) at some natural scale
  • The running should be consistent with this value at M_Z

This is already well-tested and matches.
Not a new prediction, but a consistency check.
""")

# ============================================================================
print("=" * 70)
print("SUMMARY: FALSIFIABLE PREDICTIONS")
print("=" * 70)

print(f"""
┌─────────────────────────────────────────────────────────────────────┐
│                 FALSIFIABLE PREDICTIONS                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. HUBBLE CONSTANT                                                │
│     Prediction: H₀ = 71.5 km/s/Mpc                                 │
│     Test: Independent measurement (GW, other methods)              │
│     Falsified if: H₀ definitively ≠ 71.5                           │
│                                                                     │
│  2. a₀ EVOLUTION WITH REDSHIFT                                     │
│     Prediction: a₀(z) = a₀(0) × E(z)                               │
│     Test: BTFR, RAR, rotation curves at z > 1                      │
│     Falsified if: a₀ is constant with z                            │
│                                                                     │
│  3. EARLY GALAXY FORMATION                                         │
│     Prediction: Enhanced at high z due to higher a₀                │
│     Test: JWST galaxy formation efficiency                         │
│     Falsified if: Formation efficiency same at all z               │
│                                                                     │
│  4. WIDE BINARY ANOMALY                                            │
│     Prediction: MOND effect with a₀ = 1.2×10⁻¹⁰ m/s²              │
│     Test: Gaia DR4 proper motions                                  │
│     Falsified if: No anomaly in clean systems                      │
│                                                                     │
│  5. FUTURE Ω MEASUREMENTS                                          │
│     Prediction: Ω_Λ = 0.6846, Ω_m = 0.3154 (exactly)              │
│     Test: CMB-S4, future surveys                                   │
│     Falsified if: Values shift outside this                        │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  MOST CRITICAL TEST:                                               │
│                                                                     │
│  The a₀(z) evolution is the unique prediction.                     │
│  Standard MOND has constant a₀.                                    │
│  ΛCDM has no a₀ at all.                                            │
│                                                                     │
│  If a₀(z) = a₀(0) × E(z) is confirmed:                            │
│    → Strong evidence for Zimmerman framework                       │
│    → MOND is cosmologically connected                              │
│    → "Dark matter" is emergent from horizon physics                │
│                                                                     │
│  If a₀ is constant or absent:                                      │
│    → Zimmerman framework falsified                                 │
│    → Back to ΛCDM or constant-a₀ MOND                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
""")

print("=" * 70)
print("DOI: 10.5281/zenodo.19212718")
print("=" * 70)
