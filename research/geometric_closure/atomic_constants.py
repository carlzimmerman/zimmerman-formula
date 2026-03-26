#!/usr/bin/env python3
"""
Atomic Physics Constants in the Zimmerman Framework
====================================================

Exploring:
1. Rydberg constant
2. Bohr radius
3. Electron classical radius
4. Compton wavelengths
5. Atomic mass unit
6. Fine structure intervals

Carl Zimmerman, March 2026
"""

import numpy as np

Z = 2 * np.sqrt(8 * np.pi / 3)
pi = np.pi
alpha = 1/137.035999084
alpha_s = 0.1180
Omega_Lambda = 0.685
Omega_m = 0.315

# Fundamental constants (CODATA 2018)
c = 299792458  # m/s (exact)
hbar = 1.054571817e-34  # J·s
h = 6.62607015e-34  # J·s (exact)
e = 1.602176634e-19  # C (exact)
m_e = 9.1093837015e-31  # kg
m_p = 1.67262192369e-27  # kg
epsilon_0 = 8.8541878128e-12  # F/m
mu_0 = 1.25663706212e-6  # H/m

# Derived atomic constants
a_0 = 5.29177210903e-11  # m (Bohr radius)
r_e = 2.8179403262e-15  # m (classical electron radius)
lambda_C_e = 2.42631023867e-12  # m (electron Compton wavelength)
lambda_C_p = 1.32140985539e-15  # m (proton Compton wavelength)
R_inf = 10973731.568160  # m⁻¹ (Rydberg constant)
E_h = 4.3597447222071e-18  # J (Hartree energy)
m_u = 1.66053906660e-27  # kg (atomic mass unit)

print("=" * 80)
print("ATOMIC PHYSICS CONSTANTS IN THE ZIMMERMAN FRAMEWORK")
print("=" * 80)
print(f"\nZ = 2√(8π/3) = {Z:.10f}")
print(f"α = 1/(4Z² + 3) = {1/(4*Z**2 + 3):.10f}")

# =============================================================================
# SECTION 1: Length Scales
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 1: ATOMIC LENGTH SCALES")
print("=" * 80)

print(f"""
FUNDAMENTAL LENGTHS:
  a₀ (Bohr radius)           = {a_0:.6e} m
  r_e (classical e⁻ radius)  = {r_e:.6e} m
  λ_C,e (e⁻ Compton)         = {lambda_C_e:.6e} m
  λ_C,p (proton Compton)     = {lambda_C_p:.6e} m

KEY RATIOS:
  a₀/r_e = {a_0/r_e:.2f} = 1/α² = {1/alpha**2:.2f}
  a₀/λ_C,e = {a_0/lambda_C_e:.4f} = 1/(2πα) = {1/(2*pi*alpha):.4f}
  λ_C,e/r_e = {lambda_C_e/r_e:.4f} = 2π/α = {2*pi/alpha:.4f}
""")

# Test Z expressions for length ratios
print("--- Testing Z expressions for atomic length ratios ---")
tests_length = [
    ("a₀/r_e", a_0/r_e, "(4Z²+3)²", (4*Z**2+3)**2),
    ("a₀/λ_C,e", a_0/lambda_C_e, "(4Z²+3)/(2π)", (4*Z**2+3)/(2*pi)),
    ("λ_C,e/λ_C,p", lambda_C_e/lambda_C_p, "m_p/m_e", 1836.15),
    ("λ_C,p (fm)", lambda_C_p*1e15, "0.21/Z", 0.21/Z * 1e15),
]

print(f"\n{'Ratio':<15} {'Measured':>15} {'Formula':<15} {'Predicted':>15} {'Error %':>10}")
print("-" * 75)
for name, meas, formula, pred in tests_length:
    error = abs(pred - meas)/meas * 100
    print(f"{name:<15} {meas:>15.4f} {formula:<15} {pred:>15.4f} {error:>10.3f}%")

# =============================================================================
# SECTION 2: Energy Scales
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 2: ATOMIC ENERGY SCALES")
print("=" * 80)

E_h_eV = E_h / e  # Hartree in eV
Ry_eV = E_h_eV / 2  # Rydberg in eV
m_e_eV = m_e * c**2 / e  # electron mass in eV

print(f"""
ENERGY SCALES:
  E_H (Hartree)  = {E_h_eV:.6f} eV = {E_h_eV*1000:.3f} meV
  Ry (Rydberg)   = {Ry_eV:.6f} eV
  m_e c²         = {m_e_eV:.0f} eV = {m_e_eV/1e6:.6f} MeV

KEY RELATIONS:
  E_H = α² × m_e c² = {alpha**2 * m_e_eV:.6f} eV
  Ry = α² × m_e c² / 2 = {alpha**2 * m_e_eV / 2:.6f} eV

  E_H / m_e c² = α² = {alpha**2:.10f}
""")

# Test Z expressions
print("--- Testing Z expressions for energy scales ---")
tests_energy = [
    ("E_H/m_e c² ×10⁵", E_h_eV/m_e_eV * 1e5, "1/(4Z²+3)² ×10⁵", 1/(4*Z**2+3)**2 * 1e5),
    ("Ry (eV)", Ry_eV, "m_e c² α²/2", m_e_eV * alpha**2 / 2),
    ("Ry × (4Z²+3)²", Ry_eV * (4*Z**2+3)**2, "m_e c²/2 (eV)", m_e_eV/2),
]

print(f"\n{'Quantity':<20} {'Measured':>15} {'Formula':<20} {'Predicted':>15} {'Error %':>10}")
print("-" * 85)
for name, meas, formula, pred in tests_energy:
    error = abs(pred - meas)/meas * 100
    print(f"{name:<20} {meas:>15.6f} {formula:<20} {pred:>15.6f} {error:>10.3f}%")

# =============================================================================
# SECTION 3: Rydberg Constant
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 3: RYDBERG CONSTANT")
print("=" * 80)

print(f"""
RYDBERG CONSTANT:
  R_∞ = {R_inf:.6f} m⁻¹
      = {R_inf/1e7:.10f} × 10⁷ m⁻¹

THEORETICAL FORMULA:
  R_∞ = α² m_e c / (2h)
      = m_e c α² / (2h)

With α = 1/(4Z² + 3):
  R_∞ = m_e c / [2h(4Z² + 3)²]
""")

# Calculate R_∞ from Z
R_calc = m_e * c * alpha**2 / (2 * h)
R_from_Z = m_e * c / (2 * h * (4*Z**2 + 3)**2)

print(f"Calculated R_∞ = {R_calc:.6f} m⁻¹")
print(f"From Z formula = {R_from_Z:.6f} m⁻¹")
print(f"Measured R_∞   = {R_inf:.6f} m⁻¹")
print(f"Error (calc)   = {abs(R_calc - R_inf)/R_inf * 100:.6f}%")
print(f"Error (from Z) = {abs(R_from_Z - R_inf)/R_inf * 100:.6f}%")

# =============================================================================
# SECTION 4: Mass Ratios
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 4: ATOMIC MASS RATIOS")
print("=" * 80)

m_p_m_e = m_p / m_e
m_u_m_e = m_u / m_e

print(f"""
MASS RATIOS:
  m_p/m_e = {m_p_m_e:.4f}
  m_u/m_e = {m_u_m_e:.4f}

  m_u/m_p = {m_u/m_p:.10f}  (≈ 1 - binding/mass)

ZIMMERMAN FORMULA FOR m_p/m_e:
  m_p/m_e = 9(6Z² + Z) - (8 + 3Z)
          = 54Z² + 9Z - 8 - 3Z
          = 54Z² + 6Z - 8
""")

# Test
mp_me_pred = 9*(6*Z**2 + Z) - (8 + 3*Z)
print(f"Predicted m_p/m_e = {mp_me_pred:.4f}")
print(f"Measured m_p/m_e  = {m_p_m_e:.4f}")
print(f"Error = {abs(mp_me_pred - m_p_m_e)/m_p_m_e * 100:.4f}%")

# =============================================================================
# SECTION 5: Fine Structure
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 5: FINE STRUCTURE INTERVALS")
print("=" * 80)

print(f"""
FINE STRUCTURE:
  The fine structure splitting scales as α⁴.

  For hydrogen 2P level:
    ΔE_fs / E_1s ∼ α⁴/16 = {alpha**4/16:.2e}

HYPERFINE STRUCTURE:
  The 21 cm line (1420 MHz) from hyperfine splitting:
    ν_HFS = 1420.405751768 MHz

  This scales as α⁴ × m_e/m_p × Ry
""")

nu_HFS = 1420.405751768e6  # Hz
E_HFS_eV = h * nu_HFS / e

print(f"HFS energy = {E_HFS_eV*1e6:.6f} μeV")
print(f"HFS / Ry = {E_HFS_eV / Ry_eV:.2e}")
print(f"Expected ∼ α⁴ × m_e/m_p = {alpha**4 * m_e/m_p:.2e}")

# =============================================================================
# SECTION 6: Electron g-factor
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 6: ELECTRON g-FACTOR")
print("=" * 80)

g_e = 2.00231930436256  # electron g-factor
a_e = (g_e - 2) / 2  # anomalous magnetic moment

print(f"""
ELECTRON g-FACTOR:
  g_e = {g_e:.14f}
  a_e = (g-2)/2 = {a_e:.14f}

SCHWINGER TERM:
  a_e ≈ α/(2π) = {alpha/(2*pi):.14f}

WITH α FROM Z:
  a_e ≈ 1/[(4Z²+3) × 2π] = {1/((4*Z**2+3) * 2*pi):.14f}

Error vs measured: {abs(alpha/(2*pi) - a_e)/a_e * 100:.4f}%
""")

# =============================================================================
# SECTION 7: The α-Z Connection in Atomic Physics
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 7: THE α-Z CONNECTION")
print("=" * 80)

print(f"""
CENTRAL RESULT:
  α = 1/(4Z² + 3)

This means ALL atomic physics is determined by Z!

EXAMPLES:
  1. Bohr radius: a₀ = ℏ/(m_e c α) = ℏ(4Z²+3)/(m_e c)

  2. Rydberg: R_∞ = m_e c α²/(2h) = m_e c/[2h(4Z²+3)²]

  3. Hartree: E_H = m_e c² α² = m_e c²/(4Z²+3)²

  4. Fine structure: ΔE/E ∝ α² = 1/(4Z²+3)²

THE FACTOR (4Z² + 3):
  4Z² = 4 × 8 × (4π/3) = 128π/3 = 134.04

  Adding 3 (spatial dimensions):
  4Z² + 3 = 137.04 = α⁻¹

GEOMETRIC MEANING:
  α⁻¹ = (spacetime dims × cube vertices × sphere volume) + (spatial dims)
      = 4 × 8 × (4π/3) + 3
      = 137.04
""")

# =============================================================================
# SECTION 8: Summary
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 8: SUMMARY")
print("=" * 80)

print(f"""
ATOMIC PHYSICS FROM Z:

1. LENGTH SCALES (all determined by α = 1/(4Z²+3)):
   a₀/r_e = α⁻² = (4Z²+3)²
   a₀/λ_C = 1/(2πα) = (4Z²+3)/(2π)

2. ENERGY SCALES:
   E_H = m_e c² α² = m_e c²/(4Z²+3)²
   Ry = E_H/2

3. RYDBERG CONSTANT:
   R_∞ = m_e c/[2h(4Z²+3)²]
   Completely determined by Z and fundamental constants!

4. ELECTRON g-2:
   a_e ≈ 1/[(4Z²+3) × 2π] = α/(2π)
   The Schwinger term follows from Z!

5. PROTON-ELECTRON MASS RATIO:
   m_p/m_e = 9(6Z²+Z) - (8+3Z) = 1836.3
   Error: 0.008%

KEY INSIGHT:
All of atomic physics - from the Bohr radius to fine structure -
derives from the single geometric constant Z = 2√(8π/3).

The factor 137 = 4Z² + 3 combines:
  • 4 (spacetime dimensions)
  • Z² = 32π/3 (sphere-cube geometry)
  • 3 (spatial dimensions)
""")
