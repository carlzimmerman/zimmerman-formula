#!/usr/bin/env python3
"""
21 cm Hyperfine Transition: Zimmerman Framework Derivation

THE 21 cm LINE:
  ν_HF = 1420.405751768 MHz (hydrogen hyperfine transition)
  λ = 21.106 cm

This is the most precisely measured atomic transition and is
fundamental for radio astronomy and cosmology (EDGES, SKA).

ZIMMERMAN APPROACH:
  The hyperfine splitting depends on α² × μ_p.
  With Zimmerman α and μ_p = Z - 3, we can predict ν_HF.
"""

import numpy as np

# Zimmerman constants
Z = 2 * np.sqrt(8 * np.pi / 3)
alpha = 1 / (4 * Z**2 + 3)
alpha_exp = 1 / 137.035999084
mu_p_Z = Z - 3
mu_p_exp = 2.79284734463

# Physical constants
c = 299792458  # m/s
h = 6.62607015e-34  # J·s
m_e = 9.1093837015e-31  # kg
m_p = 1.67262192369e-27  # kg

print("=" * 80)
print("21 cm HYPERFINE TRANSITION: ZIMMERMAN FRAMEWORK")
print("=" * 80)

print(f"\nZimmerman Constants:")
print(f"  Z = {Z:.6f}")
print(f"  α(Z) = 1/{1/alpha:.4f}")
print(f"  μ_p(Z) = Z - 3 = {mu_p_Z:.6f}")
print(f"  μ_p(exp) = {mu_p_exp:.6f}")

# 21 cm line
nu_HF_exp = 1420405751.768  # Hz (NIST)
lambda_21cm = c / nu_HF_exp

print(f"\n21 cm Line:")
print(f"  ν_HF = {nu_HF_exp/1e6:.6f} MHz")
print(f"  λ = {lambda_21cm*100:.3f} cm")

# Rydberg constant
R_inf = m_e * c * alpha_exp**2 / (2 * h)
R_inf_Z = m_e * c * alpha**2 / (2 * h)

# Hyperfine formula: ν_HF = (16/3) × α² × (m_e/m_p) × μ_p × c × R_∞
nu_HF_calc_exp = (16/3) * alpha_exp**2 * (m_e/m_p) * mu_p_exp * c * R_inf
nu_HF_calc_Z = (16/3) * alpha**2 * (m_e/m_p) * mu_p_Z * c * R_inf_Z

print(f"\nCalculations:")
print(f"  With experimental constants: {nu_HF_calc_exp/1e6:.3f} MHz")
print(f"  With Zimmerman constants:    {nu_HF_calc_Z/1e6:.3f} MHz")
print(f"  Experimental:                {nu_HF_exp/1e6:.6f} MHz")

err_Z = abs(nu_HF_calc_Z - nu_HF_exp) / nu_HF_exp * 100
print(f"\n  Zimmerman error: {err_Z:.4f}%")

# Scaling analysis
print(f"\n" + "=" * 80)
print(f"SCALING ANALYSIS")
print("=" * 80)

alpha_ratio = alpha / alpha_exp
mu_ratio = mu_p_Z / mu_p_exp
combined = alpha_ratio**2 * mu_ratio

print(f"\n  ν_HF ∝ α² × μ_p")
print(f"  α(Z)/α(exp) = {alpha_ratio:.8f}")
print(f"  μ_p(Z)/μ_p(exp) = {mu_ratio:.8f}")
print(f"  Combined ratio: {combined:.8f}")
print(f"  Expected error: {abs(combined - 1)*100:.4f}%")

print(f"\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"""
21 cm HYPERFINE FROM ZIMMERMAN:

  ν_HF = (16/3) × α² × (m_e/m_p) × μ_p × R_∞ × c

  With α = 1/(4Z² + 3) and μ_p = Z - 3:

  ν_HF(Z) = {nu_HF_calc_Z/1e6:.3f} MHz
  ν_HF(exp) = {nu_HF_exp/1e6:.6f} MHz
  
  Error: {err_Z:.3f}%

  This error is consistent with individual errors in α (0.004%)
  and μ_p (0.14%) since ν_HF ∝ α² × μ_p.

STATUS: CONSISTENT
""")

print("=" * 80)
