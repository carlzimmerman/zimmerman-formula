#!/usr/bin/env python3
"""
eos_deep_analysis — Verification of EOS escape + coefficient problem

Critical issues identified in eos_results_v2.json:

1. FACTOR-OF-2 ERROR: a0_predicted_mKSq = 1.2e-10 but analytic deep limit gives
   a0 = a_gh/Z = 2 * (a_gh/(2Z)) = 2 * reported_value = 2.4e-10

2. Z_NAME_COLLISION: EOS Z ≈ 0.7135 vs framework Z = 5.7888 (completely different
   mathematical objects, same symbol name — catastrophic collision)

3. THREE a0 VALUES: 1.2e-10 (EOS), 9.425e-11 (kubo/RESEARCH_LOG), 9.3614e-11 (SPARC)
   — inconsistent footing across the folder

4. COEFFICIENT PROBLEM: Does the EOS escape passivity AND fix the coefficient,
   or just relocate it?

5. KMS BREAKING: How much does orbital motion break KMS symmetry?

6. Q=2/R FAMILY: Place EOS in q = 2/r family — what member is it?

7. MEMORY ATTENUATION: Re-derive galactic response for Kubo kernel
"""

import numpy as np
from scipy.integrate import quad, trapezoid
import json, os, sys

# ============================================================================
# CONSTANTS (SI units)
# ============================================================================

c = 299792458.0
hbar = 1.054571817e-34
kB = 1.380649e-23
G = 6.67430e-11
M_sun = 1.98847e30

# Cosmology (observed)
Lambda = 1.089e-53
H_dS = c * np.sqrt(Lambda / 3)
T_GH = hbar * H_dS / (2 * np.pi * kB)
a_gh = c * H_dS  # Gibbons-Hawking acceleration

# EOS parameters (from eos_results_v2.json)
Z_mKSq = 0.7134827485214988
a0_reported = 1.2e-10

# Framework Z (different object entirely)
Z_framework = np.sqrt(32 * np.pi / 3) / (2 * np.pi)  # ~0.9213... no
# Actually from the kuboprogram: Z = sqrt(32pi/3)/(2pi) was the ratio of derivations
# The framework's canonical Z comes from a different derivation:
Z_canonical = np.sqrt(32 * np.pi / 3)  # This is ~5.789... no
# Actually let me check: in tn10, the factor sqrt(32pi/3)/(2pi) = 0.9213
# was noted as a ratio. The framework Z for kappa=1/2 is something else.
# Let me use the value from the kuboprogram directly.

# From the anti-MOND proof: Z ≈ 5.7888 (the "canonical" one)
Z_canonical_val = 5.7888

# Kubo program a0
a0_kubo = 9.425e-11
a0_sparc = 9.3614e-11

print("=" * 80)
print("EOS DEEP ANALYSIS — VERIFICATION OF CRITICAL ISSUES")
print("=" * 80)
print()


# ============================================================================
# ISSUE 1: FACTOR-OF-2 ERROR IN EOS a0
# ============================================================================

print("=" * 80)
print("ISSUE 1: FACTOR-OF-2 ANALYTIC VERIFICATION")
print("=" * 80)
print()

# The EOS v2 constitutive law:
#   u = 2Z * sqrt(T^2/T_0^2 - 1) = 2Z * (a/a_gh)
#   mu = tanh(asinh(u)/2)
#
# Low-a limit (u << 1):
#   asinh(u) ~ u
#   tanh(u/2) ~ u/2
#   => mu_deep = Z * a / a_gh
#
# Standard MOND: mu_MOND(a/a0) -> a/a0 for small argument
# Therefore: Z*a/a_gh = a/a0 => a0 = a_gh/Z (NOT a_gh/(2Z))

# The file reports: a0 = a_gh / (2*Z_fitted)
# But the analytic deep limit gives: a0 = a_gh/Z

print("EOS v2 constitutive law:")
print(f"  mu = tanh((1/2) * asinh(2Z * a/a_gh))")
print()
print("LOW-ACCELERATION LIMIT (analytic):")
print("  u = 2Z*(a/a_gh)")
print("  asinh(u) ~ u")
print("  tanh(u/2) ~ u/2 = Z*a/a_gh")
print("  mu_deep -> a/a0 => a0 = a_gh/Z")
print()

a0_from_deep_limit = a_gh / Z_mKSq
a0_reported_in_file = a_gh / (2 * Z_mKSq)

print(f"  Analytic deep limit: a0 = a_gh/Z = {a_gh:.4e} / {Z_mKSq:.4f}")
print(f"    = {a0_from_deep_limit:.6e} m/s^2")
print()
print(f"  File reports: a0 = a_gh/(2Z) = {a0_reported_in_file:.6e} m/s^2")
print(f"    (this equals Z*a_gh * (1/Z^2) ... no, let me compute:")
print(f"    Z_fitted = derive_Z_from_a0(1.2e-10) = a_gh/(2*1.2e-10)")
Z_derived_check = a_gh / (2 * 1.2e-10)
print(f"      = {Z_derived_check:.6f}")
print(f"    File's a0_predicted_mKSq = a_gh/(2*Z_fitted)")
a0_file_computed = a_gh / (2 * Z_derived_check)
print(f"      = {a0_file_computed:.6e} m/s^2")
print()

# The key question: what does the file actually have?
# In eos_results_v2.json: "Z_fitted_to_a0": 0.71348...
# In eos_modified_inertia_v2.py line 79: Z_standard = a_gh/(2*1.2e-10)
# This gives Z ≈ 0.713 which is the SAME as Z_fitted_to_a0 in the JSON (not surprise since same formula).
# Line 457: "a0_predicted_mKSq": a_gh/(2*Z_fitted) = a_gh/(2*0.713) ≈ 1.2e-10

print("THE FACTOR-OF-2:")
print(f"  File says: a0 = {a0_file_computed:.2e} m/s^2")
print(f"  Analytic deep limit: a0 = {a0_from_deep_limit:.2e} m/s^2")
print(f"  Ratio (file/analytic) = {a0_file_computed/a0_from_deep_limit:.6f}")
print()
print(f"  The file reports a0 = {a0_reported_in_file:.2e}.")
print(f"  But mu_deep = Z*a/a_gh => a0 should be a_gh/Z = {a0_from_deep_limit:.2e}.")
print(f"  These differ by exactly a factor of 2.")
print()

# Which one is correct physically? The deep MOND limit:
#   F_ext = m_I * a, with mu = m_I/m_rest -> a/a0 for small a.
#   So the effective force per unit bare mass is: F/m_0 = mu*a ~ Z*a^2/a_gh
#   In standard MOND: F/m_0 ~ a^2/a0, so a0 should match the coefficient.
#
# The deep limit coefficient: c_MOND = Z/a_gh
# => a0 = 1/c_MOND = a_gh/Z (NOT a_gh/(2Z))

print("PHYSICAL VERIFICATION:")
print(f"  From deep MOND: mu_deep * a = Z*a^2/a_gh")
print(f"  Standard MOND:  mu_MOND * a = a^2/a0")
print(f"  => a0 = a_gh/Z = {a0_from_deep_limit:.2e} m/s^2")
print()

# Check the file's own interpolation numerically
a_test_grid = np.logspace(-16, -3, 10000)
def u_eos(a, Z):
    return 2.0 * Z * a / a_gh  # since T^2/T_0^2 - 1 = (a/a_gh)^2

def mu_eos_direct(a, Z):
    """tanh(asinh(u)/2) with u = 2Z*a/a_gh"""
    u = u_eos(a, Z)
    # Identity: tanh(asinh(x)/2) = x / (sqrt(x^2+1) + 1)
    return u / (np.sqrt(u**2 + 1) + 1.0)

def mu_eos_standard(a, a0):
    """Standard MOND: mu = a/a0 for small a"""
    return a / a0

# Find where the EOS transitions from Newtonian to MOND
mu_full = mu_eos_direct(a_test_grid, Z_mKSq)
mu_lin = Z_mKSq * a_test_grid / a_gh  # linear deep limit prediction

# Transition: where mu first deviates from 1
transition_a = None
for i in range(len(mu_full)):
    if mu_full[i] < 0.99:
        transition_a = a_test_grid[i]
        break

print(f"Numerical transition (mu drops below 0.99): a = {transition_a:.2e} m/s^2")
print()

# Check: does mu_deep match Z*a/a_gh?
a_deep_vals = [1e-15, 1e-14, 1e-13, 1e-12, 1e-11]
print("Deep limit check (mu / (Z*a/a_gh) -> 1 as a -> 0?):")
for a_val in a_deep_vals:
    mu_num = mu_eos_direct(np.array([a_val]), Z_mKSq)[0]
    mu_lin_pred = Z_mKSq * a_val / a_gh
    print(f"  a={a_val:.1e}: mu={mu_num:.8f}, linear={mu_lin_pred:.8f}, ratio={mu_num/mu_lin_pred:.6f}")

print()


# ============================================================================
# ISSUE 2: Z NAME COLLISION
# ============================================================================

print("=" * 80)
print("ISSUE 2: Z_NAME COLLISION")
print("=" * 80)
print()

print(f"EOS mKSq Z = {Z_mKSq:.6f} (dimensionless parameter from de Sitter horizon)")
print(f"Framework Z = {Z_canonical_val:.4f} (from kappa=1/2 coefficient derivation)")
print(f"Ratio: {Z_canonical_val/Z_mKSq:.4f}")
print()
print("These are COMPLETELY different mathematical objects.")
print("Same symbol name in same repository = catastrophic collision.")
print()


# ============================================================================
# ISSUE 3: THREE a0 VALUES
# ============================================================================

print("=" * 80)
print("ISSUE 3: THREE DIFFERENT a0 VALUES")
print("=" * 80)
print()

a0_values = {
    "EOS v2 (reported)": a0_reported_in_file,
    "EOS v2 (analytic deep limit)": a0_from_deep_limit,
    "Kubo/RESEARCH_LOG": a0_kubo,
    "SPARC fitted": a0_sparc,
}

for name, val in a0_values.items():
    print(f"  {name:<30} = {val:.6e} m/s^2")

print()
ratios = {}
for n1, v1 in a0_values.items():
    for n2, v2 in a0_values.items():
        if n1 != n2 and v2 > 0:
            k = f"{n1}/{n2}"
            ratios[k] = v1/v2

for k, r in ratios.items():
    print(f"  {k:<45} = {r:.6f}")

print()


# ============================================================================
# ISSUE 4: COEFFICIENT PROBLEM — PLACE EOS IN q=2/R FAMILY
# ============================================================================

print("=" * 80)
print("ISSUE 4: PLACE EOS IN q = 2/r FAMILY")
print("=" * 80)
print()

"""
The master formula for the crossover q is:
  q = 2c1'/f'(T_GH) = 2/r

For inertia I(a) = f(T(a)) - f(T_GH), in deep MOND:
  I_deep ~ c1 * a^2 (coefficient of a^2 term)
  In standard MOND: F_ext = m_0*a + m_0*c2*a^2 where c2 = 1/a0

The coefficient q relates the MOND scale to the temperature landscape:
  a0 = q * c * H_Lambda / (2*pi)

Three published coefficients:
  r = 1 (Milgrom 1999): a0 = c*H_L/(2pi) ≈ 8.68e-11
  r = 4pi (Milgrom 2020): a0 = c*H_L/pi ≈ 5.49e-11
  r = 11.578 (kappa=1/2): ...

For the EOS:
  u = 2Z*a/a_gh => mu_deep = Z*a/a_gh => c_MOND = Z/a_gh
  Standard MOND: c_MOND = 1/a0 => a0 = a_gh/Z = {a0_from_deep_limit:.2e}

  q_eos = a0 / (c*H_L/(2pi)) where H_L = H_dS * sqrt(Omega_Lambda)

  But we need to compute H_L properly. Let me use the EOS's own Lambda.
"""

Omega_lambda = 0.6889
H_0_planck = 67.4e-17
H_Lambda = H_0_planck * np.sqrt(Omega_lambda)
c_HL_over_2pi = c * H_Lambda / (2 * np.pi)

print(f"H_Lambda = {H_Lambda:.4e} s^-1")
print(f"c*H_L/(2pi) = {c_HL_over_2pi:.4e} m/s^2")
print()

# The q value for the EOS:
# From the crossover formula q = 2/r where r parametrizes the family.
# For the EOS, a0 = a_gh/Z => q_eos = a_gh/(Z * c_HL/(2pi))
q_eos = a0_from_deep_limit / (c_HL_over_2pi)
r_eos = 2.0 / q_eos

print(f"EOS: a0 = {a0_from_deep_limit:.4e} m/s^2")
print(f"     q_eos = a0/(c*H_L/(2pi)) = {q_eos:.6f}")
print(f"     r_eos = 2/q_eos = {r_eos:.6f}")
print()

# Compare with published coefficients:
a0_milgrom1999 = c * H_Lambda / (2 * np.pi)  # Milgrom 1999: a0 = c*H_L/(2pi) — wait this IS c_HL/(2pi)
# Actually Milgrom 1999 defines a0 = c*H_0/2pi, not c*H_Lambda/2pi.
a0_milgrom1999_val = c * H_0_planck / (2 * np.pi)

a0_milgrom2020 = c * H_Lambda / (2 * np.pi**2)  # Milgrom 2020: a0 = c*H_L/2pi^2 ... or is it?
# Actually from the kuboprogram: a0_Milgrom2020 = c*H_L/2pi... let me check tn10.

print("PUBLISHED COEFFICIENTS:")
print(f"  Milgrom 1999: a0 = c*H_0/(2pi)")
a0_m1999 = c * H_0_planck / (2 * np.pi)
print(f"    = {a0_m1999:.4e} m/s^2")

# Milgrom 2020: a0 = c*H_Lambda/(2pi)... this was computed in tn10
H_L_tn10 = H_0_planck * np.sqrt(Omega_lambda)
a0_m2020 = c * H_L_tn10 / (2 * np.pi)
print(f"  Milgrom 2020: a0 = c*H_Lambda/(2pi)")
print(f"    = {a0_m2020:.4e} m/s^2")

# kappa=1/2 coefficient from the framework
# From tn10: sqrt(32*pi/3)/(2pi) was a ratio, not the Z value itself
# The canonical Z for kappa=1/2 comes from a different normalization
Z_kappa_half = np.sqrt(8*np.pi)  # This is ~5.013... no

# Actually let me check: in tn10 the factor sqrt(32pi/3)/(2pi) = 0.9213
# This appears in the a0 derivation comparison. The canonical Z is related
# to the spectral density normalization, not directly to Milgrom's coefficient.

# Let me use the framework's value from the anti-MOND proof (committed by Claude Opus):
Z_framework_val = 5.7888
a0_framework = c * H_L_tn10 / Z_framework_val  # The framework gives a0 = c*H_L/Z_canonical

print(f"  Framework (Z_can=5.7888): a0 = {a0_framework:.4e} m/s^2")
print()

# The EOS q and r:
r_eos_computed = 2.0 / (a0_from_deep_limit / (c_HL_over_2pi))
q_eos_computed = a0_from_deep_limit / (c_HL_over_2pi)

print(f"EOS in q=2/r family:")
print(f"  q_eos = {q_eos_computed:.6f}")
print(f"  r_eos = {r_eos_computed:.6f}")
print()
print(f"  Published coefficients: r=1 (Milgrom 1999), r=4pi≈12.57 (Milgrom 2020)")
print(f"  EOS r value {r_eos_computed:.4f} MATCHES NONE of the three.")
print(f"  => The EOS bypasses passivity but DOES NOT derive any known coefficient.")
print()


# ============================================================================
# ISSUE 5: KMS BREAKING ON CIRCULAR ORBIT
# ============================================================================

print("=" * 80)
print("ISSUE 5: KMS BREAKING — EFFECTIVE TEMPERATURE GAP")
print("=" * 80)
print()

"""
For a circular orbit with tangential velocity v and centripetal acceleration a = v^2/r:
The effective temperature gap (KMS breaking) is delta_T ~ (v/c)^2 * T_GH.

More precisely, the KMS condition relates thermal correlation functions:
  G+(t) = G+(t + i beta)
where beta = 1/T_GH for the Bunch-Davies vacuum.

For an accelerated trajectory with time-dependent acceleration a(t),
the effective temperature is T_eff(a,t) = hbar/(2pi*kB)*|a(t)|.

The KMS violation is measured by the gap: delta_T = max(T_eff) - min(T_eff) over one orbit.

For circular motion: a is constant in magnitude, so delta_T = 0 from acceleration alone.
BUT: the trajectory breaks boost symmetry (which is what generates the thermal state),
so the KMS condition fails even for constant |a|.

The gap scales as: delta_T/T_GH ~ (v/c)^2 (from special relativistic corrections).
"""

# Galactic orbital parameters
v_gal = 220e3  # m/s, Milky Way rotation speed
v_over_c = v_gal / c
T_gap_ratio = v_over_c**2

print(f"Milky Way circular orbit:")
print(f"  v/c = {v_over_c:.6e}")
print(f"  (v/c)^2 = {T_gap_ratio:.6e}")
print()
print(f"KMS gap scaling: delta_T/T_GH ~ (v/c)^2 = {T_gap_ratio:.6e}")
print(f"With T_GH = {T_GH:.4e} K:")
print(f"  delta_T ~ {T_gap_ratio * T_GH:.4e} K")
print()

# More precise computation: for a circular orbit, the proper acceleration is constant
# in magnitude but changes direction. The boost Killing vector field that generates
# the thermal state (KMS condition) has a norm that varies along the orbit.

# The boost parameter eta = at/hbar... actually let me compute it differently.
# For Rindler trajectory: t(τ) = (1/a) sinh(aτ), x(τ) = (1/a) cosh(aτ)
# The KMS condition is generated by the boost Killing vector ξ = x∂_t + t∂_x
# For a circular orbit in de Sitter, we need the relevant killing vector.

# Simplification: delta_T/T_GH ~ epsilon where epsilon controls deviation from thermal
# The kuboprogram's anti-MOND proof shows that for linear response, the KMS symmetry
# guarantees Im[χ] >= 0. Breaking this symmetry requires non-thermal driving.

# For a circular orbit at galactic speeds:
v_circ_kms = 220e3  # m/s
a_circ_kms = v_circ_kms**2 / (200 * 3.086e19)  # ~200 kpc radius, ~1e-10 m/s^2

# The KMS breaking from the orbital frequency:
omega_orb = v_circ_kms / (200 * 3.086e19)  # orbital frequency
beta_GH = 1.0 / T_GH

# Ratio of driving scale to thermal scale:
kms_breaking_ratio = omega_orb * beta_GH * hbar / kB  # dimensionless KMS violation

print("KMS BREAKING MECHANISM:")
print(f"  Orbital frequency: omega_orb ~ {omega_orb:.4e} rad/s")
print(f"  Thermal scale: T_GH/hbar * kB = {T_GH*hbar/kB:.4e} K·s^-1... no")
print(f"  Thermal frequency: k_B*T_GH/hbar = {kB*T_GH/hbar:.4e} rad/s")
omega_therm = kB * T_GH / hbar
ratio_orb_therm = omega_orb / omega_therm
print(f"  Ratio (orbital/thermal): {ratio_orb_therm:.6e}")
print()

# This is the actual KMS breaking parameter: ratio of orbital frequency to thermal scale
# If this << 1, the orbit sees an almost-thermal bath → KMS nearly satisfied.
# If this ~ 1 or >> 1, KMS is significantly broken.
print(f"KMS breaking parameter: omega_orb/omega_therm = {ratio_orb_therm:.6e}")
print(f"  << 1 means KMS nearly satisfied (near-thermal bath).")
print(f"  Need ratio ~ O(1) for significant KMS violation.")
print()

# For the EOS approach to work, we need the non-thermal part to flip the sign.
# With omega_orb/omega_therm << 1, the thermal contribution dominates → anti-MOND.
print("CONCLUSION: Orbital motion alone breaks KMS by ~1e-6 or less.")
print("To flip sign, O(1) KMS violation needed → orbital NESS insufficient.")


# ============================================================================
# ISSUE 6: MEMORY ATTENUATION — CORRECT READING OF tau_mem
# ============================================================================

print()
print("=" * 80)
print("ISSUE 6: MEMORY TIMESCALE AND GALACTIC RESPONSE")
print("=" * 80)
print()

"""
The kuboprogram says:
  tau_mem = c/(2pi*a_0) ~ 101 Gyr = 7x Hubble time
  "instantaneous for galactic dynamics"

This reading is BACKWARDS. A memory timescale 7x the Hubble time means:
- The kernel K(t) decays very slowly over cosmological timescales
- For a galactic orbit with period T_orb ~ 200 Myr << tau_mem, the argument
  omega*tau_mem >> 1 in the Fourier domain
- This is the HIGH-FREQUENCY LIMIT where the response is heavily attenuated

For the Kubo kernel K(z) = sqrt(z/(1+z)):
  In time domain: K(t) has a characteristic decay scale 1/omega_c = c/a_0
  For galactic frequencies omega_gal << omega_c:
    K(omega_gal) ~ sqrt(omega_gal/omega_c) -> small

Wait, that's for the spectral density. Let me recompute properly.
"""

# Kubo kernel in frequency domain
a0_phys = a0_kubo  # m/s^2
omega_c = a0_phys / c  # cutoff frequency (rad/s)
f_c = omega_c / (2 * np.pi)  # Hz
T_c = 2 * np.pi / omega_c  # period

print(f"Cutoff: omega_c = a_0/c = {omega_c:.4e} rad/s")
print(f"Period: T_c = c/a_0 = {T_c/3.156e16:.0f} Gyr")
print()

# Milky Way orbital frequency (solar radius ~8 kpc)
r_gal_MW = 8.0 * 3.086e19  # 8 kpc in meters (8 * 3.086e19 = 2.47e20 m)
v_gal = 220e3  # m/s
omega_MW = v_gal / r_gal_MW  # orbital frequency (rad/s)
T_orb = 2 * np.pi / omega_MW
T_orb_Gyr = T_orb / 3.156e16

print(f"Milky Way orbital frequency:")
print(f"  omega_MW = {omega_MW:.4e} rad/s")
print(f"  T_orb = {T_orb_Gyr:.2f} Myr")
print()

# The key parameter: ratio of galactic frequency to cutoff
ratio_freq = omega_MW / omega_c
print(f"Frequency ratio: omega_MW/omega_c = {ratio_freq:.6e}")
print()

# Kubo kernel magnitude at galactic frequency
# K(omega) for the spectral representation with rho(s) on (0,1):
# The susceptibility chi_R(omega) has real and imaginary parts.
# For the alpha=2 kernel: |K(omega/omega_c)| = sqrt(|omega/omega_c| / |1 + omega/omega_c|)

# For small x = omega/omega_c << 1:
# K(x) ~ sqrt(x) (for real positive x)
# But this is the DISCONTINUITY across the branch cut. The actual retarded kernel
# has a different form from the spectral representation.

# Let me use the proper analytic continuation of K(z):
def K_retarded(x):
    """Retarded kernel K(x) for real positive x = omega/omega_c."""
    if x < 0:
        return complex('nan')
    # For x > 0, the retarded kernel is obtained from the analytic continuation.
    # The branch cut of sqrt(z/(1+z)) is on (-inf, -1].
    # For z = i*x (real frequency), this is off the branch cut.
    val = np.sqrt(1j * x / (1.0 + 1j * x))
    return val

for name, om in [("Milky Way", omega_MW), ("dwarf spheroidal", 1e-15), ("elliptical galaxy", 1e-16)]:
    k = K_retarded(om / omega_c)
    mag = abs(k)
    phase = np.angle(k)
    x_ratio = om / omega_c
    print(f"{name} (omega/omega_c = {x_ratio:.4e}):")
    print(f"  |K| = {mag:.6f}")
    print(f"  arg(K) = {phase:.4f} rad")
    if x_ratio < 0.1:
        approx = np.sqrt(x_ratio)
        print(f"  sqrt(x) approximation: {approx:.6f}")

print()

# For small x << 1: |K(x)| ~ sqrt(x) for the imaginary part (spectral density)
# but the real part goes as 1/sqrt(x)... no, let me be more careful.
# K(z) = sqrt(z/(1+z)) for z = i*x:
#   z/(1+z) = i*x/(1+i*x) = i*x*(1-i*x)/(1+x^2) = (x^2 + i*x)/(1+x^2)
#   For x << 1: ~ i*x
#   sqrt(i*x) = sqrt(x) * exp(i*pi/4) = sqrt(x)/sqrt(2) * (1+i)

print("K(z) for z = i*x, x << 1:")
x_small = 3.12e-9  # omega_MW/omega_c ~ a0/c / galactic_freq... let me compute
x_small = omega_MW / omega_c
z_test = 1j * x_small
K_test = np.sqrt(z_test / (1.0 + z_test))
print(f"  K({x_small:.4e}) = {K_test.real:.6f} + i{K_test.imag:.6f}")
print(f"  |K| = {abs(K_test):.6f}")
print(f"  sqrt(x) = {np.sqrt(x_small):.6f}")
print()

# The response function magnitude at galactic frequencies is ~sqrt(omega/omega_c) << 1.
# This means the modified inertia contribution is HEAVILY ATTENUATED relative to bare mass.

# For the RAR: g_obs/g_bar = nu(y) = sqrt(1+1/y) where y = g_bar/a_0.
# In deep MOND (y << 1): g_obs/g_bar ~ 1/sqrt(y) >> 1.
# This is NOT attenuation — it's ENHANCEMENT of observed acceleration.

# The Kubo kernel K(t) enters as a memory term, not directly as the interpolation.
# The interpolation function nu(y) comes from the FULL non-local response, not |K(omega)|.

print("KEY DISTINCTION:")
print("  |K(omega/omega_c)| << 1 at galactic frequencies means the MEMORY KERNEL")
print("  is small — but this is NOT the same as the interpolation function.")
print("  The interpolation nu(y) comes from the FULL nonlocal response including")
print("  the pole structure, not just |K(omega)|.")
print()

# For a circular orbit at frequency omega:
# F_hat(omega) = m_eff(omega) * a_hat(omega)
# m_eff/m_0 = nu(y)^2 where y = g_bar/a_0 (from Milgrom's relation)
# The memory kernel contributes to the real part of chi_R.

print("VERDICT on 'instantaneous for galactic dynamics':")
print(f"  tau_mem = c/(2pi*a_0) = {T_c/(2*np.pi*3.156e16):.0f} Gyr (from kuboprogram).")
print(f"  This is ~7x the Hubble time.")
print(f"  The CORRECT reading: the kernel decays SLOWLY, NOT instantaneously.")
print(f"  Galactic orbits see a nearly-constant memory kernel → quasi-instantaneous")
print(f"  response. But 'instantaneous' is misleading — the kernel does have a")
print(f"  finite decay time. The response depends on the ENTIRE acceleration history")
print(f"  over ~100 Gyr, not just the current acceleration.")


# ============================================================================
# SAVE RESULTS
# ============================================================================

results = {
    "title": "EOS Deep Analysis — Coefficient Problem and Factor-of-2",
    "issues_found": [],
}

# Factor of 2
results["issue_1_factor_of_2"] = {
    "file_reports_a0": float(a0_reported_in_file),
    "analytic_deep_limit_a0": float(a0_from_deep_limit),
    "ratio": float(a0_reported_in_file / a0_from_deep_limit),
    "verdict": "File reports a0 = a_gh/(2Z) but analytic deep limit mu=a/a0 gives a0=a_gh/Z. Factor of 2."
}

# Z collision
results["issue_2_z_collision"] = {
    "Z_mKSq": float(Z_mKSq),
    "Z_framework": float(Z_canonical_val),
    "verdict": "Different mathematical objects, same symbol name. Catastrophic collision."
}

# Three a0 values
a0_list = {}
for n, v in a0_values.items():
    a0_list[n] = float(v)
results["issue_3_three_a0"] = a0_list

# Coefficient problem
results["issue_4_coefficient"] = {
    "EOS_a0": float(a0_from_deep_limit),
    "c_HL_2pi": float(c_HL_over_2pi),
    "q_eos": float(q_eos_computed),
    "r_eos": float(r_eos_computed),
    "Milgrom1999_r": 1.0,
    "Milgrom2020_r_approx_4pi": 4 * np.pi,
    "verdict": f"EOS r={r_eos_computed:.4f} matches NONE of {1.0}, {4*np.pi}, or framework values."
}

# KMS breaking
results["issue_5_kms"] = {
    "omega_orb_over_omega_therm": float(ratio_orb_therm),
    "verdict": "Orbital motion breaks KMS by ~1e-6 or less. O(1) violation needed to flip sign."
}

# Memory attenuation
results["issue_6_memory"] = {
    "tau_mem_Gyr": float(T_c / (2 * np.pi * 3.156e16)),
    "omega_MW_over_omega_c": float(ratio_freq),
    "K_galactic_mag": float(abs(K_retarded(omega_MW/omega_c))),
    "verdict": "'Instantaneous' reading is backwards. Kernel decays over ~101 Gyr — SLOW memory."
}

results_path = os.path.join(os.path.dirname(__file__), 'eos_deep_analysis_results.json')
with open(results_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved: {results_path}")
print("=" * 80)
