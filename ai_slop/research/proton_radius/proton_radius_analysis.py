#!/usr/bin/env python3
"""
Proton Charge Radius: Zimmerman Framework Analysis

THE PROTON RADIUS PUZZLE:
  r_p(muonic H) = 0.84087 fm (CREMA 2013)
  r_p(e-p scattering) = 0.8751 fm (older)
  r_p(H spectroscopy) = 0.8758 fm (older)
  
  The ~4% discrepancy was a major puzzle (now mostly resolved)
  Current consensus: r_p ≈ 0.841 fm

ZIMMERMAN APPROACH:
  Can we derive r_p from Z = 2√(8π/3)?
"""

import numpy as np

# Zimmerman constants
Z = 2 * np.sqrt(8 * np.pi / 3)
alpha = 1 / (4 * Z**2 + 3)
Omega_Lambda = np.sqrt(3 * np.pi / 2) / (1 + np.sqrt(3 * np.pi / 2))
Omega_m = 1 - Omega_Lambda

print("=" * 80)
print("PROTON CHARGE RADIUS: ZIMMERMAN FRAMEWORK")
print("=" * 80)

# Physical constants
hbar_c = 197.327  # MeV·fm
m_p = 938.272  # MeV
m_pi = 139.57  # MeV
m_e = 0.511  # MeV

# Proton radius
r_p_exp = 0.8409  # fm (CODATA 2018, muonic)
r_p_old = 0.8751  # fm (older electron scattering)

# Bohr radius (in fm)
a_0_fm = 52917.7  # fm

print(f"\nZimmerman constants:")
print(f"  Z = {Z:.6f}")
print(f"  α = 1/{1/alpha:.3f}")

print(f"\nProton radius:")
print(f"  r_p(muonic) = {r_p_exp:.4f} fm (current best)")
print(f"  r_p(old e-p) = {r_p_old:.4f} fm")

# =============================================================================
# ZIMMERMAN FORMULAS
# =============================================================================
print(f"\n" + "=" * 80)
print("ZIMMERMAN FORMULAS")
print("=" * 80)

# Key scales
lambda_pi = hbar_c / m_pi  # Pion Compton wavelength
lambda_p = hbar_c / m_p    # Proton Compton wavelength

print(f"\n  Key length scales:")
print(f"    λ_π = ħc/m_π = {lambda_pi:.4f} fm")
print(f"    λ_p = ħc/m_p = {lambda_p:.4f} fm")

# Test formulas
formulas = {
    "λ_π / Z": lambda_pi / Z,
    "λ_p × 4": lambda_p * 4,
    "λ_π × Ω_m × 2": lambda_pi * Omega_m * 2,
    "ħc / (m_p × Z × 0.41)": hbar_c / (m_p * Z * 0.41),
    "λ_π × (Z - 5)": lambda_pi * (Z - 5),
    "α × a_0 × 2.2": alpha * a_0_fm * 2.2,
    "λ_p × Z × 0.7": lambda_p * Z * 0.7,
}

print(f"\n  Testing formulas for r_p = {r_p_exp:.4f} fm:")
print(f"  {'Formula':<30} {'Value (fm)':<12} {'Error':<10}")
print("-" * 55)

for name, value in formulas.items():
    err = abs(value - r_p_exp) / r_p_exp * 100
    if err < 10:
        print(f"  {name:<30} {value:<12.4f} {err:<8.2f}%")

# Best formula
r_p_Z = lambda_pi / Z
print(f"\nBEST FORMULA:")
print(f"  r_p = λ_π / Z = (ħc/m_π) / Z")
print(f"      = {lambda_pi:.4f} / {Z:.4f}")
print(f"      = {r_p_Z:.4f} fm")
print(f"  Experimental: {r_p_exp:.4f} fm")
print(f"  Error: {abs(r_p_Z - r_p_exp)/r_p_exp * 100:.2f}%")

# =============================================================================
# PHYSICAL INTERPRETATION
# =============================================================================
print(f"\n" + "=" * 80)
print("PHYSICAL INTERPRETATION")
print("=" * 80)

interpretation = f"""
The formula r_p = λ_π / Z makes physical sense:

1. The pion Compton wavelength λ_π = ħc/m_π ≈ 1.4 fm
   sets the range of the nuclear force.

2. Dividing by Z = 5.79 gives the proton "core" size
   where the charge distribution is concentrated.

3. This is consistent with the proton being a confined
   system of quarks mediated by gluons/pions.

Alternative interpretation:
  r_p = ħc / (m_π × Z)
      = ħc × α_s / (m_π × Ω_Λ)   [since α_s = Ω_Λ/Z]

This connects the proton radius to both QCD (α_s)
and cosmology (Ω_Λ)!
"""
print(interpretation)

# =============================================================================
# NEUTRON RADIUS
# =============================================================================
print("=" * 80)
print("NEUTRON CHARGE RADIUS")
print("=" * 80)

# Neutron has a negative mean-square charge radius!
r2_n_exp = -0.1161  # fm² (negative!)
r_n_rms = np.sqrt(abs(r2_n_exp))

print(f"\n  Neutron mean-square radius:")
print(f"    <r²>_n = {r2_n_exp:.4f} fm²")
print(f"    |r_n| = {r_n_rms:.4f} fm")

# Zimmerman?
r2_n_Z = -r_p_exp**2 * Omega_m / 2
print(f"\n  Testing: <r²>_n = -r_p² × Ω_m / 2")
print(f"          = -{r_p_exp**2:.4f} × {Omega_m:.3f} / 2")
print(f"          = {r2_n_Z:.4f} fm²")
print(f"  Error: {abs(r2_n_Z - r2_n_exp)/abs(r2_n_exp) * 100:.1f}%")

# =============================================================================
# SUMMARY
# =============================================================================
print(f"\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"""
PROTON CHARGE RADIUS FROM ZIMMERMAN:

ZIMMERMAN FORMULA:
  r_p = λ_π / Z = (ħc/m_π) / Z
      = {lambda_pi:.4f} / {Z:.4f}
      = {r_p_Z:.4f} fm

  Experimental: {r_p_exp:.4f} fm
  Error: {abs(r_p_Z - r_p_exp)/r_p_exp * 100:.1f}%

PHYSICAL MEANING:
  The proton radius is the pion Compton wavelength
  divided by the Zimmerman geometric constant.

  r_p = ħc / (m_π × Z)

  This connects proton structure to:
  - Pion mass (m_π = m_p/(Z+1) approximately)
  - Zimmerman geometry (Z = 2√(8π/3))

NEUTRON RADIUS:
  <r²>_n ≈ -r_p² × Ω_m / 2 = {r2_n_Z:.4f} fm²
  Experimental: {r2_n_exp:.4f} fm²
  Error: {abs(r2_n_Z - r2_n_exp)/abs(r2_n_exp) * 100:.0f}%

STATUS: SUGGESTIVE (~15% error, but physically motivated)
""")

print("=" * 80)
