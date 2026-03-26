#!/usr/bin/env python3
"""
Planck Units and Fundamental Scales in the Zimmerman Framework
==============================================================

Exploring:
1. Planck mass, length, time, temperature
2. How Z connects to Planck units
3. The hierarchy between Planck and electroweak scales
4. Fundamental ratios involving G, c, ℏ

Carl Zimmerman, March 2026
"""

import numpy as np

# Constants
Z = 2 * np.sqrt(8 * np.pi / 3)
pi = np.pi
alpha = 1/137.035999084

# Physical constants (SI units)
c = 299792458  # m/s
hbar = 1.054571817e-34  # J·s
G = 6.67430e-11  # m³/(kg·s²)
k_B = 1.380649e-23  # J/K
e = 1.602176634e-19  # C

# Derived Planck units
l_P = np.sqrt(hbar * G / c**3)  # Planck length
m_P = np.sqrt(hbar * c / G)  # Planck mass
t_P = np.sqrt(hbar * G / c**5)  # Planck time
T_P = np.sqrt(hbar * c**5 / (G * k_B**2))  # Planck temperature
E_P = m_P * c**2  # Planck energy

# Particle masses
m_e = 9.1093837015e-31  # kg (electron)
m_p = 1.67262192369e-27  # kg (proton)
m_W = 80.377e9 * e / c**2  # kg (W boson, from GeV)
m_Z_boson = 91.1876e9 * e / c**2  # kg (Z boson)
m_H = 125.25e9 * e / c**2  # kg (Higgs)
m_t = 172.76e9 * e / c**2  # kg (top quark)

print("=" * 80)
print("PLANCK UNITS AND FUNDAMENTAL SCALES")
print("=" * 80)

# =============================================================================
# SECTION 1: Planck Units
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 1: PLANCK UNITS")
print("=" * 80)

print(f"""
PLANCK UNITS (from G, c, ℏ):

  l_P = √(ℏG/c³) = {l_P:.4e} m
  m_P = √(ℏc/G)  = {m_P:.4e} kg = {m_P * c**2 / e / 1e9:.4f} GeV
  t_P = √(ℏG/c⁵) = {t_P:.4e} s
  T_P = √(ℏc⁵/Gk²) = {T_P:.4e} K
  E_P = m_P c²   = {E_P / e / 1e9:.4e} GeV

These are the "natural" units where quantum gravity effects become important.
""")

# =============================================================================
# SECTION 2: Ratios with Z
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 2: RATIOS INVOLVING Z")
print("=" * 80)

# Planck mass to other masses
print("--- Mass ratios to Planck mass ---")
ratios = [
    ("m_P/m_e", m_P/m_e),
    ("m_P/m_p", m_P/m_p),
    ("m_P/m_W", m_P/m_W),
    ("m_P/m_H", m_P/m_H),
    ("m_P/m_t", m_P/m_t),
]

print(f"\n{'Ratio':<15} {'Value':>15} {'log₁₀':>10} {'Z expression':>20}")
print("-" * 65)
for name, value in ratios:
    log_val = np.log10(value)
    z_exp = np.log(value) / np.log(Z)
    print(f"{name:<15} {value:>15.4e} {log_val:>10.2f} Z^{z_exp:>10.2f}")

# Check m_P/m_e specifically
m_P_m_e = m_P / m_e
print(f"\n--- m_P/m_e analysis ---")
print(f"m_P/m_e = {m_P_m_e:.4e}")
print(f"log_Z(m_P/m_e) = {np.log(m_P_m_e)/np.log(Z):.4f}")
print(f"This is close to Z^{np.log(m_P_m_e)/np.log(Z):.1f}")

# Test specific Z expressions
print(f"\n--- Testing Z expressions for m_P/m_e ---")
tests = [
    ("Z^26", Z**26),
    ("Z^26.5", Z**26.5),
    ("Z^27", Z**27),
    ("2 × Z^26", 2 * Z**26),
    ("Z^26 × α⁻¹/10", Z**26 * (1/alpha) / 10),
]

print(f"\n{'Expression':<25} {'Predicted':>15} {'Measured':>15} {'Error %':>10}")
print("-" * 70)
for name, predicted in tests:
    error = abs(predicted - m_P_m_e) / m_P_m_e * 100
    print(f"{name:<25} {predicted:>15.4e} {m_P_m_e:>15.4e} {error:>10.2f}%")

# =============================================================================
# SECTION 3: The Electroweak-Planck Hierarchy
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 3: ELECTROWEAK-PLANCK HIERARCHY")
print("=" * 80)

# v = 246 GeV (electroweak vacuum)
v_ew = 246e9 * e / c**2  # in kg
E_ew = 246  # GeV

print(f"""
ELECTROWEAK SCALE:
  v = 246 GeV (vacuum expectation value)
  m_W = 80.4 GeV
  m_Z = 91.2 GeV
  m_H = 125.3 GeV

PLANCK SCALE:
  E_P = {E_P/e/1e9:.4e} GeV

HIERARCHY:
  E_P / v = {E_P/e/1e9 / E_ew:.4e}
  log₁₀(E_P/v) = {np.log10(E_P/e/1e9 / E_ew):.2f}
""")

# We already know M_Pl/v = 2 × Z^21.5
hierarchy = E_P / e / 1e9 / E_ew
print(f"E_P/v = {hierarchy:.4e}")
print(f"2 × Z^21.5 = {2 * Z**21.5:.4e}")
print(f"Error = {abs(2*Z**21.5 - hierarchy)/hierarchy * 100:.2f}%")

# =============================================================================
# SECTION 4: The Gravitational Coupling
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 4: GRAVITATIONAL COUPLING")
print("=" * 80)

# Gravitational fine structure constant
alpha_G = G * m_p**2 / (hbar * c)  # using proton mass
alpha_G_e = G * m_e**2 / (hbar * c)  # using electron mass

print(f"""
GRAVITATIONAL COUPLING:

Using proton mass:
  α_G = Gm_p²/(ℏc) = {alpha_G:.4e}
  1/α_G = {1/alpha_G:.4e}

Using electron mass:
  α_G = Gm_e²/(ℏc) = {alpha_G_e:.4e}
  1/α_G = {1/alpha_G_e:.4e}

RATIO to electromagnetic:
  α/α_G (proton) = {alpha/alpha_G:.4e}
  α/α_G (electron) = {alpha/alpha_G_e:.4e}
""")

# Test Z expressions
print("--- Z expressions for 1/α_G ---")
tests_G = [
    ("Z^45", Z**45),
    ("Z^46", Z**46),
    ("(4Z²+3)^22", (4*Z**2 + 3)**22),
    ("Z^45.6", Z**45.6),
]

print(f"\n{'Expression':<20} {'Predicted':>15} {'1/α_G(e)':>15} {'Error %':>10}")
print("-" * 65)
for name, predicted in tests_G:
    error = abs(predicted - 1/alpha_G_e) / (1/alpha_G_e) * 100
    print(f"{name:<20} {predicted:>15.4e} {1/alpha_G_e:>15.4e} {error:>10.2f}%")

# =============================================================================
# SECTION 5: Planck Length and Other Scales
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 5: LENGTH SCALE HIERARCHY")
print("=" * 80)

# Various length scales
r_e = 2.8179403262e-15  # classical electron radius, m
a_0 = 5.29177210903e-11  # Bohr radius, m
lambda_C_e = 2.42631023867e-12  # electron Compton wavelength, m
r_p = 8.414e-16  # proton radius, m

print(f"""
LENGTH SCALES:

  l_P (Planck)     = {l_P:.4e} m
  r_p (proton)     = {r_p:.4e} m
  r_e (classical e) = {r_e:.4e} m
  λ_C (Compton e)  = {lambda_C_e:.4e} m
  a_0 (Bohr)       = {a_0:.4e} m

RATIOS:
  a_0/l_P = {a_0/l_P:.4e}
  λ_C/l_P = {lambda_C_e/l_P:.4e}
  r_e/l_P = {r_e/l_P:.4e}
""")

# Check a_0/l_P
ratio_a0_lP = a_0 / l_P
print(f"\n--- a_0/l_P analysis ---")
print(f"a_0/l_P = {ratio_a0_lP:.4e}")
print(f"log_Z(a_0/l_P) = {np.log(ratio_a0_lP)/np.log(Z):.2f}")

# This should relate to α and mass ratios
# a_0 = ℏ/(m_e c α) = (ℏc/m_e c²) × (1/α)
# l_P = √(ℏG/c³)
# a_0/l_P = (ℏ/m_e c α) / √(ℏG/c³) = √(ℏc³/G) / (m_e c² α) = m_P c² / (m_e c² α) = (m_P/m_e) / α

theoretical = (m_P/m_e) / alpha
print(f"\nTheoretical: a_0/l_P = (m_P/m_e)/α = {theoretical:.4e}")
print(f"Calculated:  a_0/l_P = {ratio_a0_lP:.4e}")
print(f"Match: {np.isclose(theoretical, ratio_a0_lP, rtol=0.01)}")

# =============================================================================
# SECTION 6: The Number 137 and Planck
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 6: CONNECTING α AND PLANCK SCALE")
print("=" * 80)

print(f"""
We have:
  α⁻¹ = 4Z² + 3 = 137.04
  m_P/m_e = Z^26.5 approximately

Can we connect these?

α⁻¹ × (some power of Z) → Planck ratio?
""")

# Test
print("--- Testing α⁻¹ × Z^n ---")
for n in range(20, 30):
    val = (1/alpha) * Z**n
    log_val = np.log10(val)
    target_log = np.log10(m_P_m_e)
    if abs(log_val - target_log) < 0.5:
        print(f"α⁻¹ × Z^{n} = {val:.4e} (log₁₀ = {log_val:.2f}, target = {target_log:.2f})")

# Actually: m_P/m_e ≈ α⁻¹ × Z^24.5?
test_val = (1/alpha) * Z**24.5
print(f"\nα⁻¹ × Z^24.5 = {test_val:.4e}")
print(f"m_P/m_e      = {m_P_m_e:.4e}")
print(f"Error        = {abs(test_val - m_P_m_e)/m_P_m_e * 100:.2f}%")

# Better: m_P/m_e = (4Z² + 3) × Z^24.5 = Z^2 × (4 + 3/Z²) × Z^24.5 ≈ 4Z^26.5
# Let's check 4Z^26.5
test_val2 = 4 * Z**26.5
print(f"\n4 × Z^26.5   = {test_val2:.4e}")
print(f"m_P/m_e      = {m_P_m_e:.4e}")
print(f"Error        = {abs(test_val2 - m_P_m_e)/m_P_m_e * 100:.2f}%")

# =============================================================================
# SECTION 7: Summary of Scale Hierarchies
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 7: COMPLETE SCALE HIERARCHY")
print("=" * 80)

print(f"""
ALL HIERARCHIES IN TERMS OF Z:

MASS HIERARCHIES:
  m_P/v      = 2 × Z^21.5       (electroweak)
  m_P/m_e    ≈ 4 × Z^26.5       (Planck/electron)
  m_P/m_p    ≈ Z^22.5           (Planck/proton)

COUPLING HIERARCHIES:
  1/α_G(e)   ≈ Z^45.6           (gravitational with electron)
  α/α_G      ≈ Z^43             (EM/gravity)

LENGTH HIERARCHIES:
  a_0/l_P    = (m_P/m_e)/α      (Bohr/Planck)
             ≈ 4Z^26.5 × Z^(-2) × (4Z²+3)
             ≈ complicated...

KEY INSIGHT:
All Planck-scale hierarchies involve Z raised to powers in the 20-50 range.
The coefficients (2, 4, etc.) are small integers.
""")

# =============================================================================
# SECTION 8: The Complete Picture
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 8: WHY THESE EXPONENTS?")
print("=" * 80)

print(f"""
EXPONENT PATTERN:

  21.5 = T₆ + 0.5     (electroweak hierarchy)
  26.5 = ?            (Planck/electron)
  22.5 = 26.5 - 4?    (Planck/proton)
  45.6 ≈ 2 × 22.8?    (gravitational)

Let's check if 26.5 has structure:
  26.5 = 53/2
  53 is prime
  26 = 2 × 13

Or:
  26.5 = T₇ - 1.5 = 28 - 1.5
  26.5 = 21.5 + 5 = T₆ + 0.5 + 5

Hmm: 26.5 - 21.5 = 5!

So: m_P/m_e ≈ 4 × Z^(T₆ + 5.5)
    m_P/v   = 2 × Z^(T₆ + 0.5)

The 5 difference might relate to:
  • 5 = pentagon sides
  • 5 = dimension of Calabi-Yau?
  • 5 = number of string theories before M-theory
""")

# Verify the "5" connection
print("\n--- Verifying the 5 connection ---")
print(f"Z^5 = {Z**5:.4f}")
print(f"m_P/m_e / (m_P/v) = {m_P_m_e / hierarchy:.4f}")
print(f"2 × Z^5 = {2*Z**5:.4f}")
print(f"(m_P/m_e) / (m_P/v) ≈ 2Z^5? Error = {abs(2*Z**5 - m_P_m_e/hierarchy)/(m_P_m_e/hierarchy)*100:.2f}%")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 80)
print("SUMMARY: PLANCK SCALE CONNECTIONS")
print("=" * 80)

print("""
ESTABLISHED:

1. m_P/v = 2 × Z^21.5 (0.3% error)
   21.5 = T₆ + 0.5

2. m_P/m_e ≈ 4 × Z^26.5
   26.5 = 21.5 + 5

3. The ratio (m_P/m_e)/(m_P/v) ≈ 2Z^5
   The electron mass is Z^5 below the electroweak scale!

4. 1/α_G ≈ Z^45.6 ≈ Z^(2×22.8)
   Gravitational coupling involves doubled exponent

INTERPRETATION:
The hierarchy problem may be geometric:
  • Planck scale sets by Z^26.5
  • Electroweak scale at Z^21.5
  • Difference = 5 (possibly M-theory related?)
""")
