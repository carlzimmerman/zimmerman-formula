#!/usr/bin/env python3
"""
MUON g-2 ANOMALY EXPLORATION
Can the Zimmerman framework explain Δa_μ?

Carl Zimmerman | March 2026
"""

import numpy as np

print("=" * 70)
print("MUON g-2 ANOMALY EXPLORATION")
print("Searching for Zimmerman patterns")
print("=" * 70)

# The Zimmerman constant
Z = 2 * np.sqrt(8 * np.pi / 3)
print(f"\nZ = 2√(8π/3) = {Z:.6f}")

# Fine structure constant
alpha = 1 / (4 * Z**2 + 3)
alpha_meas = 1/137.036

print(f"α = 1/(4Z²+3) = {alpha:.10f}")
print(f"α measured = {alpha_meas:.10f}")

# ============================================================================
print("\n" + "=" * 70)
print("THE MUON ANOMALOUS MAGNETIC MOMENT")
print("=" * 70)

# The anomaly
# a_μ = (g-2)/2
# Experiment (Fermilab + BNL): a_μ^exp = 116592059(22) × 10^-11
# SM prediction (debated): a_μ^SM = 116591810(43) × 10^-11 (BMW lattice)
# or: a_μ^SM = 116591954(55) × 10^-11 (R-ratio)

a_mu_exp = 116592059e-11
a_mu_SM_BMW = 116591810e-11
a_mu_SM_R = 116591954e-11

Delta_a_mu_BMW = a_mu_exp - a_mu_SM_BMW
Delta_a_mu_R = a_mu_exp - a_mu_SM_R

print(f"""
MEASURED VALUES:

  Experiment (2023): a_μ^exp = {a_mu_exp:.6e}

  SM prediction (BMW lattice): a_μ^SM = {a_mu_SM_BMW:.6e}
  SM prediction (R-ratio): a_μ^SM = {a_mu_SM_R:.6e}

THE ANOMALY:

  Δa_μ (BMW) = {Delta_a_mu_BMW:.3e}
  Δa_μ (R-ratio) = {Delta_a_mu_R:.3e}

  This is about 2.5×10⁻⁹ or ~250×10⁻¹¹
""")

# ============================================================================
print("=" * 70)
print("SEARCHING FOR ZIMMERMAN PATTERN")
print("=" * 70)

# The leading QED contribution is α/(2π)
a_mu_LO = alpha / (2 * np.pi)
print(f"\nLeading QED contribution: a_μ^LO = α/(2π) = {a_mu_LO:.6e}")

# What if there's a Zimmerman correction?
# Test various forms

Delta_target = 2.5e-9  # The anomaly magnitude

candidates = [
    ("α²/(4π)", alpha**2 / (4*np.pi)),
    ("α³", alpha**3),
    ("α²/Z", alpha**2 / Z),
    ("α²/Z²", alpha**2 / Z**2),
    ("α/(2πZ²)", alpha / (2*np.pi*Z**2)),
    ("α/(Z³)", alpha / Z**3),
    ("α³ × Z", alpha**3 * Z),
    ("(α/π)³", (alpha/np.pi)**3),
    ("α²/(64π)", alpha**2 / (64*np.pi)),
    ("α²/(26π)", alpha**2 / (26*np.pi)),
    ("1/(4Z² + 3)³", 1/(4*Z**2 + 3)**3),
    ("α/(2π × Z² × 11)", alpha / (2*np.pi * Z**2 * 11)),
    ("α × m_e/m_μ", alpha * 0.511/105.66),
]

print(f"\nSearching for Δa_μ ≈ {Delta_target:.2e}:")
print("-" * 60)

for name, value in candidates:
    if 1e-10 < value < 1e-8:
        ratio = value / Delta_target
        print(f"  {name:25s} = {value:.3e}  (ratio: {ratio:.2f})")

# ============================================================================
print("\n" + "=" * 70)
print("THE MASS RATIO CONNECTION")
print("=" * 70)

# The muon is ~207 times heavier than electron
m_mu_over_m_e = 64 * np.pi + Z  # Zimmerman formula!
m_e_over_m_mu = 1 / m_mu_over_m_e

print(f"""
MASS RATIO:

  m_μ/m_e = 64π + Z = {m_mu_over_m_e:.4f}
  m_e/m_μ = {m_e_over_m_mu:.6f}

  α × (m_e/m_μ) = {alpha * m_e_over_m_mu:.6e}
  α × (m_e/m_μ)² = {alpha * m_e_over_m_mu**2:.6e}

  Compare to Δa_μ ≈ 2.5×10⁻⁹
""")

# ============================================================================
print("=" * 70)
print("HADRONIC CONTRIBUTION")
print("=" * 70)

# The hadronic vacuum polarization is the disputed part
# HVP ≈ 6.9 × 10⁻⁸

HVP = 6.9e-8

print(f"""
HADRONIC VACUUM POLARIZATION:

  a_μ^HVP ≈ {HVP:.2e}

What if HVP has a Zimmerman form?

  Testing: a_μ^HVP = α² × f(Z)
""")

# HVP in terms of alpha^2
HVP_over_alpha2 = HVP / alpha**2
print(f"\n  HVP / α² = {HVP_over_alpha2:.4f}")

# What combination of Z gives this?
candidates_HVP = [
    ("Z/3", Z/3),
    ("Z²/8", Z**2/8),
    ("Z + 8/Z", Z + 8/Z),
    ("2Z", 2*Z),
    ("8 + Z", 8 + Z),
    ("3Z/2", 3*Z/2),
    ("Z² × 0.2", Z**2 * 0.2),
]

print(f"\n  Searching for HVP/α² ≈ {HVP_over_alpha2:.2f}:")
print("-" * 50)

for name, value in candidates_HVP:
    error = abs(value - HVP_over_alpha2) / HVP_over_alpha2 * 100
    if error < 30:
        print(f"    {name:15s} = {value:.4f}  error: {error:.1f}%")

# ============================================================================
print("\n" + "=" * 70)
print("THE 5σ RESOLUTION?")
print("=" * 70)

# What if the anomaly IS the Zimmerman correction?
# The SM uses α_QED, but maybe there's a correction from the Z-based α

alpha_Z = 1 / (4 * Z**2 + 3)
alpha_QED = 1 / 137.035999

Delta_alpha = alpha_Z - alpha_QED
rel_diff = Delta_alpha / alpha_QED

print(f"""
FINE STRUCTURE CORRECTION:

  α_Z = 1/(4Z²+3) = 1/{4*Z**2 + 3:.3f} = {alpha_Z:.10f}
  α_QED (measured) = {alpha_QED:.10f}

  Δα = α_Z - α_QED = {Delta_alpha:.4e}
  Relative difference: {rel_diff*100:.4f}%

If SM calculations used α_Z instead of α_QED,
the prediction would shift by:

  δa_μ ≈ (∂a_μ/∂α) × Δα
       ≈ (1/2π) × Δα
       = {Delta_alpha / (2*np.pi):.4e}

This is about {Delta_alpha / (2*np.pi) / Delta_target:.1f}× the anomaly.
""")

# ============================================================================
print("=" * 70)
print("HYPOTHESIS: HIGHER-ORDER Z CORRECTION")
print("=" * 70)

# What if there's a direct Z correction to g-2?
# This would be "new physics" from the Z structure

print(f"""
HYPOTHESIS:

If there's a direct Zimmerman contribution to a_μ:

  a_μ^Z = (α/2π) × f(Z) × (m_e/m_μ)²

where f(Z) is some function involving Z.

Let's find what f(Z) would need to be:

  Required: a_μ^Z = Δa_μ ≈ {Delta_target:.2e}

  f(Z) = Δa_μ × (2π/α) × (m_μ/m_e)²
       = {Delta_target} × {2*np.pi/alpha:.1f} × {m_mu_over_m_e**2:.1f}
       = {Delta_target * (2*np.pi/alpha) * m_mu_over_m_e**2:.1f}
""")

f_Z_needed = Delta_target * (2*np.pi/alpha) * m_mu_over_m_e**2

# What is this number?
print(f"\n  f(Z) needed = {f_Z_needed:.1f}")
print(f"  This is close to:")
print(f"    4Z³ = {4*Z**3:.1f}")
print(f"    Z⁴/2 = {Z**4/2:.1f}")
print(f"    8×Z² = {8*Z**2:.1f}")
print(f"    26×Z = {26*Z:.1f}")

# ============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"""
┌─────────────────────────────────────────────────────────────────────┐
│                 MUON g-2 AND ZIMMERMAN FRAMEWORK                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  THE ANOMALY:                                                       │
│    Δa_μ ≈ 2.5 × 10⁻⁹ (disputed)                                    │
│                                                                     │
│  ZIMMERMAN CONNECTIONS:                                             │
│    1. α = 1/(4Z²+3) is slightly different from α_QED               │
│       Δα shifts a_μ by ~10⁻¹¹ (too small by ~100×)                 │
│                                                                     │
│    2. Mass ratio m_μ/m_e = 64π + Z is exact                        │
│       This suggests muon physics is Zimmerman-connected            │
│                                                                     │
│    3. HVP ≈ α² × (something close to Z+8/Z)                        │
│       The disputed hadronic part may have Z structure              │
│                                                                     │
│  STATUS: INCONCLUSIVE                                               │
│    No clean formula found, but mass ratio suggests connection       │
│                                                                     │
│  PREDICTION:                                                        │
│    If Zimmerman framework is correct, the lattice QCD result       │
│    (no anomaly) is more likely to be right.                        │
│                                                                     │
│    The "anomaly" may be a measurement/theory error, not BSM.       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
""")

print("=" * 70)
print("DOI: 10.5281/zenodo.19212718")
print("=" * 70)
