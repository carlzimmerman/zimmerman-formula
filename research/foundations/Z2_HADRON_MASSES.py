#!/usr/bin/env python3
"""
Deriving Hadron Masses, QCD Scale, and More from Z²
====================================================

We derive additional particle physics quantities from Z² = CUBE × SPHERE = 32π/3:

1. Proton-electron mass ratio:
   - m_p/m_e = α⁻¹ × 67/5 = 1836.35 (0.01% error!)

2. QCD scale:
   - Λ_QCD = m_p × sin(θ_c) = m_p/√20 ≈ 210 MeV

3. Pion mass:
   - m_π = m_p/(BEKENSTEIN + N_gen) = m_p/7 ≈ 134 MeV

4. Neutron-proton mass difference:
   - Δm = m_e × 8π/D_string ≈ 1.28 MeV

5. W boson mass (absolute):
   - m_W = m_e × 10^(2(GAUGE+1)/(BEKENSTEIN+1)) ≈ 81 GeV

6. CMB recombination redshift:
   - z_recomb = CUBE × α⁻¹ ≈ 1096

Author: Carl Zimmerman
Date: March 2026
"""

import numpy as np

# ============================================================================
# FUNDAMENTAL Z² CONSTANTS
# ============================================================================

CUBE = 8                           # Vertices of cube
SPHERE = 4 * np.pi / 3            # Volume of unit sphere
Z_SQUARED = CUBE * SPHERE          # = 32π/3 ≈ 33.51

# Derived dimensional constants
BEKENSTEIN = int(round(3 * Z_SQUARED / (8 * np.pi)))  # = 4
GAUGE = int(round(9 * Z_SQUARED / (8 * np.pi)))       # = 12
N_GEN = BEKENSTEIN - 1                                 # = 3
D_STRING = GAUGE - 2                                   # = 10

# Fine structure constant from Z²
alpha_inv = 4 * Z_SQUARED + 3  # = 137.04
alpha = 1 / alpha_inv

# Cabibbo angle from Z²
sin_theta_c = 1 / np.sqrt(2 * D_STRING)  # = 1/√20

print("=" * 70)
print("HADRON MASSES, QCD SCALE, AND COSMOLOGY FROM Z²")
print("=" * 70)
print(f"\nZ² = {Z_SQUARED:.6f}")
print(f"α⁻¹ = {alpha_inv:.4f}")
print(f"sin(θ_c) = 1/√{2*D_STRING} = {sin_theta_c:.6f}")

# ============================================================================
# 1. PROTON-ELECTRON MASS RATIO
# ============================================================================

print("\n" + "=" * 70)
print("1. PROTON-ELECTRON MASS RATIO")
print("=" * 70)

# Measured value (CODATA 2018)
m_p_m_e_measured = 1836.15267343

# Z² derivation
# m_p/m_e = α⁻¹ × (GAUGE + 1 + 2/(BEKENSTEIN + 1))
#         = α⁻¹ × (13 + 2/5)
#         = α⁻¹ × 67/5

factor = (GAUGE + 1) + 2 / (BEKENSTEIN + 1)  # = 13 + 0.4 = 13.4
m_p_m_e_predicted = alpha_inv * factor

# Alternative form: α⁻¹ × 67/5
m_p_m_e_alt = alpha_inv * 67 / 5

print(f"\nZ² Derivation:")
print(f"  m_p/m_e = α⁻¹ × (GAUGE + 1 + 2/(BEKENSTEIN + 1))")
print(f"         = {alpha_inv:.4f} × ({GAUGE + 1} + 2/{BEKENSTEIN + 1})")
print(f"         = {alpha_inv:.4f} × ({GAUGE + 1} + {2/(BEKENSTEIN+1):.1f})")
print(f"         = {alpha_inv:.4f} × {factor:.4f}")
print(f"         = {m_p_m_e_predicted:.4f}")

print(f"\nAlternative form:")
print(f"  m_p/m_e = α⁻¹ × 67/5 = {alpha_inv:.4f} × 13.4 = {m_p_m_e_alt:.4f}")

error_percent = abs(m_p_m_e_predicted - m_p_m_e_measured) / m_p_m_e_measured * 100

print(f"\nComparison:")
print(f"  Predicted: m_p/m_e = {m_p_m_e_predicted:.4f}")
print(f"  Measured:  m_p/m_e = {m_p_m_e_measured:.4f}")
print(f"  Error: {error_percent:.3f}%")

print(f"""
Physical Interpretation:
------------------------
The proton-electron mass ratio involves:
- α⁻¹ = 137.04: The fine structure constant inverse
- GAUGE + 1 = 13: Gauge bosons plus Higgs
- 2/(BEKENSTEIN + 1) = 0.4: Spacetime correction

The proton mass is:
- α⁻¹ times heavier than electron (electromagnetic factor)
- Multiplied by 13.4 (gauge + spacetime structure)

Where 67/5 = 13.4 comes from:
- 67 = 5 × 13 + 2 = (BEKENSTEIN + 1)(GAUGE + 1) + 2
- 5 = BEKENSTEIN + 1
""")

# ============================================================================
# 2. QCD SCALE Λ_QCD
# ============================================================================

print("\n" + "=" * 70)
print("2. QCD SCALE Λ_QCD")
print("=" * 70)

# Measured values (MS-bar, 5 flavors)
Lambda_QCD_measured = 210  # MeV (approximate)
m_proton = 938.272  # MeV

# Z² derivation
# Λ_QCD = m_p × sin(θ_c) = m_p / √20
Lambda_QCD_predicted = m_proton * sin_theta_c

print(f"\nZ² Derivation:")
print(f"  Λ_QCD = m_p × sin(θ_c)")
print(f"       = m_p / √(2(GAUGE - 2))")
print(f"       = m_p / √{2*D_STRING}")
print(f"       = {m_proton:.2f} MeV × {sin_theta_c:.4f}")
print(f"       = {Lambda_QCD_predicted:.1f} MeV")

error_percent = abs(Lambda_QCD_predicted - Lambda_QCD_measured) / Lambda_QCD_measured * 100

print(f"\nComparison:")
print(f"  Predicted: Λ_QCD = {Lambda_QCD_predicted:.1f} MeV")
print(f"  Measured:  Λ_QCD ≈ {Lambda_QCD_measured} MeV")
print(f"  Error: {error_percent:.1f}%")

print(f"""
Physical Interpretation:
------------------------
The QCD scale is set by:
- The proton mass (the fundamental QCD bound state)
- The Cabibbo angle (quark mixing)

Λ_QCD = m_p × sin(θ_c) connects:
- Strong force confinement scale
- Quark flavor mixing angle

The Cabibbo angle appears in QCD because:
- Both involve quark physics
- The mixing angle sets the transition scale
""")

# ============================================================================
# 3. PION MASS
# ============================================================================

print("\n" + "=" * 70)
print("3. PION MASS")
print("=" * 70)

# Measured values
m_pi0_measured = 134.977  # MeV (neutral pion)
m_pi_pm_measured = 139.570  # MeV (charged pion)
m_pi_avg = (m_pi0_measured + 2 * m_pi_pm_measured) / 3  # Average

# Z² derivation
# m_π = m_p / (BEKENSTEIN + N_gen) = m_p / 7
divisor = BEKENSTEIN + N_GEN  # = 7
m_pi_predicted = m_proton / divisor

print(f"\nZ² Derivation:")
print(f"  m_π = m_p / (BEKENSTEIN + N_gen)")
print(f"     = m_p / ({BEKENSTEIN} + {N_GEN})")
print(f"     = m_p / {divisor}")
print(f"     = {m_proton:.2f} / {divisor}")
print(f"     = {m_pi_predicted:.2f} MeV")

error_pi0 = abs(m_pi_predicted - m_pi0_measured) / m_pi0_measured * 100

print(f"\nComparison:")
print(f"  Predicted: m_π = {m_pi_predicted:.2f} MeV")
print(f"  Measured:  m_π⁰ = {m_pi0_measured:.2f} MeV")
print(f"  Measured:  m_π± = {m_pi_pm_measured:.2f} MeV")
print(f"  Error (vs π⁰): {error_pi0:.2f}%")

print(f"""
Physical Interpretation:
------------------------
The pion-proton mass ratio is:
- 1/7 = 1/(BEKENSTEIN + N_gen)
- 7 = spacetime dimensions (4) + generations (3)

The pion is the lightest hadron because:
- It's a pseudo-Goldstone boson of chiral symmetry
- Its mass is suppressed by factor 7
""")

# ============================================================================
# 4. NEUTRON-PROTON MASS DIFFERENCE
# ============================================================================

print("\n" + "=" * 70)
print("4. NEUTRON-PROTON MASS DIFFERENCE")
print("=" * 70)

# Measured value
delta_m_np_measured = 1.29333  # MeV
m_electron = 0.51099895  # MeV

# Z² derivation
# Δm = m_e × 8π / D_string = m_e × 8π/10
delta_m_predicted = m_electron * 8 * np.pi / D_STRING

print(f"\nZ² Derivation:")
print(f"  Δm(n-p) = m_e × CUBE × π / D_string")
print(f"         = m_e × {CUBE}π / {D_STRING}")
print(f"         = {m_electron:.4f} MeV × {8*np.pi/D_STRING:.4f}")
print(f"         = {delta_m_predicted:.4f} MeV")

error_percent = abs(delta_m_predicted - delta_m_np_measured) / delta_m_np_measured * 100

print(f"\nComparison:")
print(f"  Predicted: Δm(n-p) = {delta_m_predicted:.4f} MeV")
print(f"  Measured:  Δm(n-p) = {delta_m_np_measured:.4f} MeV")
print(f"  Error: {error_percent:.2f}%")

print(f"""
Physical Interpretation:
------------------------
The neutron-proton mass difference involves:
- m_e: The electron mass scale
- 8π/10 = CUBE × π / D_string

The mass difference is:
- Electromagnetic in origin (d quark heavier than u)
- Scaled by electron mass
- Modified by cube-string geometric factor
""")

# ============================================================================
# 5. W BOSON MASS (ABSOLUTE SCALE)
# ============================================================================

print("\n" + "=" * 70)
print("5. W BOSON MASS (ABSOLUTE SCALE)")
print("=" * 70)

# Measured value
m_W_measured = 80.377  # GeV
m_e_GeV = 0.51099895e-3  # GeV

# Z² derivation
# m_W = m_e × 10^(2(GAUGE + 1)/(BEKENSTEIN + 1))
#     = m_e × 10^(26/5)
#     = m_e × 10^5.2
exponent = 2 * (GAUGE + 1) / (BEKENSTEIN + 1)  # = 26/5 = 5.2
m_W_predicted = m_e_GeV * 10**exponent

print(f"\nZ² Derivation:")
print(f"  m_W = m_e × 10^(2(GAUGE + 1)/(BEKENSTEIN + 1))")
print(f"     = m_e × 10^(2 × {GAUGE + 1} / {BEKENSTEIN + 1})")
print(f"     = m_e × 10^({2*(GAUGE+1)}/{BEKENSTEIN + 1})")
print(f"     = m_e × 10^{exponent:.1f}")
print(f"     = {m_e_GeV:.4e} GeV × {10**exponent:.0f}")
print(f"     = {m_W_predicted:.2f} GeV")

error_percent = abs(m_W_predicted - m_W_measured) / m_W_measured * 100

print(f"\nComparison:")
print(f"  Predicted: m_W = {m_W_predicted:.2f} GeV")
print(f"  Measured:  m_W = {m_W_measured:.2f} GeV")
print(f"  Error: {error_percent:.2f}%")

print(f"""
Physical Interpretation:
------------------------
The W boson mass is:
- 10^5.2 times the electron mass
- Exponent = 26/5 = 2(GAUGE + 1)/(BEKENSTEIN + 1)

The electroweak scale is set by:
- 26 = 2 × 13 = 2(GAUGE + 1): Twice the gauge + Higgs content
- 5 = BEKENSTEIN + 1: Spacetime + 1
""")

# ============================================================================
# 6. Z BOSON MASS (FROM W AND WEINBERG ANGLE)
# ============================================================================

print("\n" + "=" * 70)
print("6. Z BOSON MASS")
print("=" * 70)

# Z² values
sin2_theta_W = 3 / (GAUGE + 1)  # = 3/13
cos_theta_W = np.sqrt(1 - sin2_theta_W)  # = √(10/13)

m_Z_measured = 91.1876  # GeV
m_Z_predicted = m_W_predicted / cos_theta_W

print(f"\nFrom W mass and Weinberg angle:")
print(f"  m_Z = m_W / cos(θ_W)")
print(f"     = m_W / √(1 - 3/(GAUGE + 1))")
print(f"     = m_W / √(10/13)")
print(f"     = {m_W_predicted:.2f} / {cos_theta_W:.4f}")
print(f"     = {m_Z_predicted:.2f} GeV")

error_percent = abs(m_Z_predicted - m_Z_measured) / m_Z_measured * 100

print(f"\nComparison:")
print(f"  Predicted: m_Z = {m_Z_predicted:.2f} GeV")
print(f"  Measured:  m_Z = {m_Z_measured:.2f} GeV")
print(f"  Error: {error_percent:.2f}%")

# ============================================================================
# 7. CMB RECOMBINATION REDSHIFT
# ============================================================================

print("\n" + "=" * 70)
print("7. CMB RECOMBINATION REDSHIFT")
print("=" * 70)

# Measured value
z_recomb_measured = 1100  # approximately

# Z² derivation
# z_recomb = CUBE × α⁻¹ = 8 × 137
z_recomb_predicted = CUBE * alpha_inv

print(f"\nZ² Derivation:")
print(f"  z_recomb = CUBE × α⁻¹")
print(f"          = {CUBE} × {alpha_inv:.2f}")
print(f"          = {z_recomb_predicted:.0f}")

error_percent = abs(z_recomb_predicted - z_recomb_measured) / z_recomb_measured * 100

print(f"\nComparison:")
print(f"  Predicted: z_recomb = {z_recomb_predicted:.0f}")
print(f"  Measured:  z_recomb ≈ {z_recomb_measured}")
print(f"  Error: {error_percent:.1f}%")

print(f"""
Physical Interpretation:
------------------------
The recombination redshift is:
- CUBE × α⁻¹ = 8 × 137 = 1096
- Cube vertices times fine structure constant inverse

This connects:
- CMB physics (recombination)
- Electromagnetic coupling (α)
- Fundamental geometry (CUBE)
""")

# ============================================================================
# 8. QUARK MASS RATIOS
# ============================================================================

print("\n" + "=" * 70)
print("8. QUARK MASS RATIOS")
print("=" * 70)

# Measured quark masses (MS-bar at 2 GeV)
m_u = 2.16  # MeV
m_d = 4.67  # MeV
m_s = 93.4  # MeV

# Ratios
ratio_d_u_measured = m_d / m_u  # ≈ 2.16
ratio_s_d_measured = m_s / m_d  # ≈ 20

print(f"Measured quark mass ratios:")
print(f"  m_d/m_u = {ratio_d_u_measured:.2f}")
print(f"  m_s/m_d = {ratio_s_d_measured:.1f}")

# Z² predictions
ratio_d_u_predicted = (BEKENSTEIN + 1) / 2  # = 5/2 = 2.5
ratio_s_d_predicted = 2 * D_STRING  # = 20

print(f"\nZ² Predictions:")
print(f"  m_d/m_u = (BEKENSTEIN + 1)/2 = {BEKENSTEIN + 1}/2 = {ratio_d_u_predicted:.2f}")
print(f"  m_s/m_d = 2 × D_string = 2 × {D_STRING} = {ratio_s_d_predicted}")

print(f"\nComparison:")
print(f"  m_d/m_u: Predicted = {ratio_d_u_predicted:.2f}, Measured = {ratio_d_u_measured:.2f}, Error = {abs(ratio_d_u_predicted - ratio_d_u_measured)/ratio_d_u_measured*100:.0f}%")
print(f"  m_s/m_d: Predicted = {ratio_s_d_predicted}, Measured = {ratio_s_d_measured:.1f}, Error = {abs(ratio_s_d_predicted - ratio_s_d_measured)/ratio_s_d_measured*100:.0f}%")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("SUMMARY: HADRON AND QCD RESULTS FROM Z²")
print("=" * 70)

print(f"""
NEW DERIVATIONS FROM Z²:

Z² = CUBE × SPHERE = {Z_SQUARED:.4f}
α⁻¹ = 4Z² + 3 = {alpha_inv:.2f}

HADRON MASSES:
| Quantity    | Formula                          | Predicted    | Measured     | Error  |
|-------------|----------------------------------|--------------|--------------|--------|
| m_p/m_e     | α⁻¹ × 67/5                       | {m_p_m_e_predicted:.2f}      | {m_p_m_e_measured:.2f}      | {abs(m_p_m_e_predicted - m_p_m_e_measured)/m_p_m_e_measured*100:.3f}% |
| Λ_QCD       | m_p × sin(θ_c)                   | {Lambda_QCD_predicted:.0f} MeV     | ~{Lambda_QCD_measured} MeV      | ~{abs(Lambda_QCD_predicted - Lambda_QCD_measured)/Lambda_QCD_measured*100:.0f}%   |
| m_π         | m_p / 7                          | {m_pi_predicted:.1f} MeV     | {m_pi0_measured:.1f} MeV     | {error_pi0:.1f}%  |
| Δm(n-p)     | m_e × 8π/10                      | {delta_m_predicted:.3f} MeV   | {delta_m_np_measured:.3f} MeV   | {abs(delta_m_predicted - delta_m_np_measured)/delta_m_np_measured*100:.1f}%  |

ELECTROWEAK SCALE:
| Quantity    | Formula                          | Predicted    | Measured     | Error  |
|-------------|----------------------------------|--------------|--------------|--------|
| m_W         | m_e × 10^(26/5)                  | {m_W_predicted:.1f} GeV     | {m_W_measured:.1f} GeV     | {abs(m_W_predicted - m_W_measured)/m_W_measured*100:.1f}%  |
| m_Z         | m_W / √(10/13)                   | {m_Z_predicted:.1f} GeV     | {m_Z_measured:.1f} GeV     | {abs(m_Z_predicted - m_Z_measured)/m_Z_measured*100:.1f}%  |

COSMOLOGY:
| Quantity    | Formula                          | Predicted    | Measured     | Error  |
|-------------|----------------------------------|--------------|--------------|--------|
| z_recomb    | CUBE × α⁻¹                       | {z_recomb_predicted:.0f}         | ~{z_recomb_measured}         | {abs(z_recomb_predicted - z_recomb_measured)/z_recomb_measured*100:.1f}%  |

KEY FORMULAS:
  m_p/m_e = α⁻¹ × (GAUGE + 1 + 2/(BEKENSTEIN+1)) = 137 × 13.4 = {m_p_m_e_predicted:.1f}
  Λ_QCD = m_p / √20 = {Lambda_QCD_predicted:.0f} MeV
  m_π = m_p / (BEKENSTEIN + N_gen) = m_p/7 = {m_pi_predicted:.0f} MeV
  m_W = m_e × 10^(26/5) = {m_W_predicted:.1f} GeV
  z_recomb = 8 × 137 = {z_recomb_predicted:.0f}

"The proton mass is 137 × 13.4 electron masses — pure geometry."
""")
