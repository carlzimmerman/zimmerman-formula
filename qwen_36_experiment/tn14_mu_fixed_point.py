#!/usr/bin/env python3
"""
tn14: Self-Consistency Fixed-Point Equation for mu(x)

Question: What constraints does Milgrom's interpolation function nu(y) = sqrt(1+1/y)
place on the spectral deformation delta_rho(s) that must exist in NESS?

Approach: The Caldeira-Leggett integral computes the inertia correction from a spectral density:
  delta_m/rho_0 = (2/pi)*PV int_0^inf domega' rho(omega')/omega'^2

We parametrize the NESS spectral density as:
  rho_NESS(omega) = rho_eq(omega) + delta_rho(omega)

where rho_eq(omega) is the equilibrium KMS spectrum (positive, passivity) and
delta_rho(omega) is the non-equilibrium correction that flips the sign.

Key relation between nu(y) and delta_m:
  nu(y)^2 = 1 + delta_m(mu)/m_0

For Milgrom's nu(y) = sqrt(1+1/y):
  nu(y)^2 - 1 = 1/y
  => delta_m/m_0 = a_0/g_bar = 1/y

So: delta_m[delta_rho]/m_0 = 1/y for ALL y = g_bar/a_0.

This is an OVERDETERMINED system: one unknown function delta_rho(omega) must satisfy
infinitely many constraints (one per value of y). This is the fixed-point problem.

The key insight: delta_m depends on the ENTIRE spectrum, not just the value at a single frequency.
So we decompose delta_rho into a basis and solve for the coefficients.

METHODOLOGY:
1. Define a parametric family of spectral deformations (basis functions)
2. Compute delta_m[basis] for each basis element
3. Solve the linear system that maps basis coefficients to Milgrom's nu(y)^2 - 1
4. Check if a solution exists and what properties it must have

PAPER: tn14 — mu fixed-point equation from spectral self-consistency.
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize, least_squares
import json, os, sys

print("=" * 80)
print("tn14: SELF-CONSISTENCY FIXED-POINT EQUATION FOR mu(x)")
print("=" * 80)
print()


# ============================================================================
# CONSTANTS AND BASE SPECTRAL DENSITY
# ============================================================================

# Physical constants (natural units where convenient)
a0 = 9.389e-11       # m/s^2 (from de Sitter)
c_val = 2.99792458e8  # m/s
omega_c = a0 / c_val  # cutoff frequency ~ 3.13e-19 rad/s

# Equilibrium spectral density (dimensionless, on [0,1] in units of omega_c)
def rho_eq(s):
    """Equilibrium alpha=2 spectral measure: (1/pi)*sqrt(s/(1-s)) on (0,1)."""
    return np.sqrt(s / (1.0 - s)) / np.pi if 0 < s < 1 else 0.0


# ============================================================================
# PART 1: THE FIXED-POINT CONSTRAINT FROM MILGROM'S NU(Y)
# ============================================================================

print("=" * 80)
print("PART 1: MILGROM NU(Y) IMPOSES AN OVERDETERMINED SYSTEM")
print("=" * 80)
print()

"""
Milgrom's interpolation: nu(y) = sqrt(1 + 1/y), where y = g_bar/a_0.

The inertia correction is defined by:
  nu(y)^2 = 1 + delta_m/m_0

So: delta_m/m_0 = nu(y)^2 - 1 = 1/y = a_0/g_bar

Via the Caldeira-Leggett formula (in frequency space):
  delta_m/m_0 = (2/pi) * PV int_0^inf d(omega') rho_NES(omega') / omega'^2

In dimensionless form, s = omega/omega_c:
  delta_m/m_0 = (2/pi) * PV int_0^1 ds rho_NE S(s) / (s*omega_c)^2 * omega_c
              = (2/(pi*omega_c)) * PV int_0^1 ds rho_NES(s) / s

So the constraint is:
  (2/(pi*omega_c)) * integral[rho_NES(s)/s, s in (0,1)] = 1/y

for EVERY y = g_bar/a_0 > 0.

This is OVERDETERMINED: one integral must equal every possible value of 1/y.
The only way this works is if delta_rho depends on the ACCELERATION SCALE g_bar,
meaning rho_NES itself depends on the dynamical state.

This is the core insight: the NESS spectral density is NOT a fixed function.
It is a functional of the particle's acceleration profile through matter backreaction.
"""

# Show the overload: for different y values, what does delta_m/m_0 need to be?
y_values = [0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0]
dm_needed = []

print(f"  {'y (g_bar/a_0)':>14} {'nu(y)^2':>12} {'nu^2-1=1/y':>14} {'delta_m/m_0':>14}")
for y in y_values:
    nu_sq = 1.0 + 1.0 / y
    dm_needed.append(1.0 / y)
    print(f"  {y:14.2f} {nu_sq:12.6f} {1.0/y:14.6f} {1.0/y:14.6f}")

print()
print("CONCLUSION: delta_m/m_0 = 1/y must hold for ALL y simultaneously.")
print("The integral constraint is OVERDETERMINED — one number cannot equal many.")
print()
print("RESOLUTION: rho_NE S depends on the acceleration scale g_bar through backreaction.")
print("This means delta_rho(omega; [trajectory]) — a FUNCTIONAL of the path, not a fixed function.")


# ============================================================================
# PART 2: BASIS DECOMPOSITION OF DELTA_RHO
# ============================================================================

print()
print("=" * 80)
print("PART 2: BASIS DECOMPOSITION — PARAMETRIZING THE NESS SPECTRAL DEFORMATION")
print("=" * 80)
print()

"""
We decompose delta_rho into a basis of functions on [0,1]:
  delta_rho(s) = sum_i c_i * b_i(s)

The Caldeira-Leggett integral gives:
  delta_m/m_0 = (2/(pi*omega_c)) * int_0^1 ds * [rho_eq(s) + sum_i c_i*b_i(s)] / s
              = C_eq + sum_i c_i * C_i

where C_eq = (2/(pi*omega_c)) * int_0^1 rho_eq(s)/s ds  (equilibrium contribution)
and C_i = (2/(pi*omega_c)) * int_0^1 b_i(s)/s ds  (basis element contribution)

For MOND we need: delta_m/m_0 < 0 (negative, lowering inertia).
Since rho_eq is positive, C_eq > 0. We need sum c_i*C_i to be negative enough to overcome C_eq.

But there's a subtlety: for Milgrom's nu(y), the required delta_m depends on y.
So the basis must encode y-dependence too:
  delta_rho(s; y) = sum_i c_i(y) * b_i(s)
"""

# Define basis functions
def basis_1(s):
    """Delta function-like spike near a specific frequency s0."""
    s0 = 0.5
    sigma = 0.05
    return np.exp(-(s - s0)**2 / (2 * sigma**2)) / (sigma * np.sqrt(2*np.pi))

def basis_2(s):
    """Step function: constant negative spectral weight below s_threshold."""
    s_th = 0.3
    return -1.0 * (s < s_th)

def basis_3(s):
    """Power law deformation: delta_rho ~ s^p with tunable exponent."""
    p = -0.5  # integrable singularity at s=0
    return np.sign(s - 0.5) * np.abs(s - 0.5)**p if s > 0 else 0.0

def basis_4(s):
    """Localized negative dip at high frequency (near cutoff)."""
    s0 = 0.9
    sigma = 0.02
    return -np.exp(-(s - s0)**2 / (2 * sigma**2)) / (sigma * np.sqrt(2*np.pi))

def basis_5(s):
    """Broad negative deformation across entire spectrum."""
    return -0.1 * np.ones_like(s) if hasattr(s, '__len__') else -0.1


# Compute the Caldeira-Leggett coefficient C_i for each basis element
def calc_cl_coefficient(basis_func, s_min=1e-8, s_max=1.0):
    """Compute C = (2/(pi*omega_c)) * int_0^1 b(s)/s ds."""
    # The prefactor is common to all; we compute just the integral part
    try:
        result, _ = quad(lambda s: basis_func(s) / s, s_min, s_max, limit=500, epsabs=1e-12)
        return result
    except Exception as e:
        return np.nan

print("Computing Caldeira-Leggett coefficients for each basis element:")
print(f"  {'Basis':>20}  {'C_i (integral)':>18}")
print(f"  {'-'*50}")

basis_funcs = [basis_1, basis_2, basis_3, basis_4, basis_5]
basis_names = ["Gaussian(s0=0.5)", "Step(s<0.3)", "Power s^(-0.5)", "Neg.dip(s0=0.9)", "Broad neg."]

C_values = []
for i, bf in enumerate(basis_funcs):
    c_val_comp = calc_cl_coefficient(bf)
    C_values.append(c_val_comp)
    print(f"  {basis_names[i]:>20}  {c_val_comp:18.6f}")

# Also compute C_eq (equilibrium contribution)
C_eq, _ = quad(lambda s: rho_eq(s) / s, 1e-8, 1.0, limit=500, epsabs=1e-12)
print(f"  {'rho_eq':>20}  {C_eq:18.6f}")

# With prefactor (2/pi):
prefactor = 2.0 / np.pi
C_eq_p = prefactor * C_eq
C_vals_p = [prefactor * c for c in C_values]

print()
print(f"With prefactor 2/pi: C_eq = {C_eq_p:.6f}")
print("The equilibrium contribution is POSITIVE (anti-MOND).")
print()


# ============================================================================
# PART 3: SOLVING THE LINEAR SYSTEM — CAN WE GET NEGATIVE delta_m?
# ============================================================================

print("=" * 80)
print("PART 3: LINEAR SYSTEM — MINIMIZING DELTA_M WITH NEGATIVE DEFORMATIONS")
print("=" * 80)
print()

"""
We need: C_eq + sum_i c_i * C_i < 0 (MOND sign).

Since C_eq > 0, we need negative combinations of basis functions.
The minimum possible delta_m is achieved by choosing the optimal coefficients.

But there's a constraint: the total spectral weight must remain physical.
We impose: |sum_i c_i| < some_bound to keep deformations moderate.

Let's find: what combination of basis functions gives the most negative delta_m?
"""

# Simple optimization: minimize C_eq + sum c_i * C_i subject to constraints
bounds = [(-5, 5) for _ in basis_funcs]  # each coefficient bounded

def objective(c_coeffs):
    """Negative of total CL integral — we want to maximize negative delta_m."""
    total = C_eq + sum(ci * ci_val for ci, ci_val in zip(c_coeffs, C_values))
    return total  # minimize this (want it negative)

# Try several starting points to find global minimum
results = []
for n_trial in range(10):
    np.random.seed(n_trial)
    c0 = np.random.randn(len(basis_funcs)) * 2
    res = minimize(objective, c0, bounds=bounds, method='L-BFGS-B',
                   options={'maxiter': 1000})
    results.append(res)

best = min(results, key=lambda r: r.fun)
print(f"Best objective value (min delta_m/m_0): {best.fun:.6f}")
print(f"Coefficients: {[f'{c:.4f}' for c in best.x]}")
print()

if best.fun < 0:
    print("SUCCESS: A linear combination of basis deformations can produce NEGATIVE delta_m.")
    print("This means the NESS deformation CAN flip the sign of the spectral density integral.")
else:
    print("PARTIAL SUCCESS: The minimum is near zero but not negative with these basis functions.")
    print("Need more flexible basis or different parametrization.")

print()
print(f"Dominant basis elements in optimal deformation:")
for i, (name, coeff) in enumerate(zip(basis_names, best.x)):
    if abs(coeff) > 0.1:
        sign = "NEGATIVE" if coeff < 0 else "POSITIVE"
        print(f"  {name:>20}: c_{i} = {coeff:+8.4f} ({sign} deformation)")

print()


# ============================================================================
# PART 4: THE FIXED-POINT EQUATION — SELF-CONSISTENT rho(y)
# ============================================================================

print("=" * 80)
print("PART 4: THE SELF-CONSISTENT FIXED-POINT EQUATION")
print("=" * 80)
print()

"""
The key equation: the spectral density must be self-consistent.

In NESS, rho(s) depends on the acceleration scale y through matter backreaction:
  rho(s; y) = rho_eq(s) + delta_rho(s; [a(tau)])

where delta_rho is a functional of the full acceleration history, not just g_bar.

The fixed-point condition is:
  delta_m[y] = (2/pi)*int_0^1 ds rho(s; y)/s
  with constraint: nu(y)^2 = 1 + delta_m[y]/m_0 = 1 + 1/y

Substituting:
  (2/pi)*int_0^1 ds [rho_eq(s) + delta_rho(s; y)] / s = 1/y   for ALL y

This gives the FIXED-POINT EQUATION for delta_rho:
  (2/pi)*int_0^1 ds delta_rho(s; y)/s = 1/y - C_eq   for ALL y

The left side is a LINEAR functional of delta_rho. The right side is known (1/y).
So: we need to find delta_rho(s; y) such that its weighted integral equals 1/y - C_eq.

This has infinitely many solutions (underdetermined inverse problem).
The additional constraint is PHYSICS: delta_rho comes from matter backreaction,
which determines a unique solution.
"""

# For the purpose of THIS computation, we find ANY solution (minimal norm)
# Then in tn15 we will use the physical NESS equation to select the correct one.

# The minimal-norm solution to: int_0^1 delta_rho(s)/s ds = RHS for all y
# is a delta function at some frequency s* with amplitude A:
#   A/s* = RHS => A = s* * RHS

# For simplicity, we choose the representation as:
#   delta_rho(s; y) = f(y) * delta(s - s*)  (single-frequency deformation)

s_star = 0.5  # representative frequency in the spectrum
RHS_values = {}
for y in y_values:
    RHS = 1.0 / y - C_eq_p
    RHS_values[y] = RHS

print("Fixed-point equation: int delta_rho(s; y)/s ds = 1/y - C_eq")
print()
print(f"  {'y':>8}  {'RHS = 1/y - C_eq':>20}  {'Required A = s* * RHS':>22}")
print(f"  {'-'*55}")

for y in [0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0]:
    rhs = RHS_values[y]
    A_needed = s_star * rhs
    print(f"  {y:8.2f}  {rhs:20.6f}  {A_needed:22.6f}")

print()
print("Physical interpretation:")
print(f"  For y << C_eq (deep MOND, g_bar << a_0): RHS > 0 => delta_rho > 0")
print(f"  For y >> C_eq (Newtonian, g_bar >> a_0): RHS < 0 => delta_rho < 0")
print(f"  At crossover: y ~ 1/C_eq, delta_rho changes sign.")
print()

# Find the crossover point
y_cross = 1.0 / C_eq_p if C_eq_p > 0 else np.inf
print(f"Cross-over: y_cross = 1/C_eq = {y_cross:.4f}")
print(f"  For y < {y_cross:.2f} (deep MOND): need POSITIVE delta_rho (inverted population)")
print(f"  For y > {y_cross:.2f} (Newtonian): need NEGATIVE delta_rho (standard dissipation)")


# ============================================================================
# PART 5: CONSTRAINTS ON DELTA_RHO — WHAT PHYSICS CAN PRODUCE IT?
# ============================================================================

print()
print("=" * 80)
print("PART 5: CONSTRAINTS ON PHYSICAL MECHANISMS — REQUIREMENTS FOR delta_rho")
print("=" * 80)
print()

"""
From the fixed-point equation, delta_rho(s; y) must satisfy:

1. SIGN FLIP: Must be POSITIVE for low y (deep MOND) and NEGATIVE for high y (Newtonian).
   This means the NESS backreaction must INVERT spectral weight at some band.

2. FREQUENCY DEPENDENCE: Must be scale-dependent — different accelerations couple to
   different spectral bands differently. The coupling strength delta_rho(s; y) depends on
   how the matter trajectory frequency omega_gal ~ v/R compares to omega_c.

3. AMPLITUDE: |delta_rho| must be large enough to overcome C_eq (anti-MOND).
   At crossover, |RHS| = 0. So the deformation must match the equilibrium spectrum
   exactly at some scale and reverse sign beyond that.

4. LOCALIZATION: The deformation should be localized near galactic frequencies
   omega_gal ~ a_0/c to produce the MOND effect only at galactic scales, not
   at planetary or stellar scales.

THESE ARE THE PHYSICAL REQUIREMENTS on any NESS mechanism:
  (R1) Produces inverted spectral density (rho < 0) near omega_gal ~ omega_c
  (R2) Localization to galactic frequency band
  (R3) Amplitude matching the equilibrium spectrum at crossover scale
  (R4) Scale-dependent coupling: delta_rho depends on omega/omega_c
"""

print("Physical requirements for any viable NESS mechanism:")
for r in ["R1: Inverted spectral density (rho < 0) near galactic frequencies",
          "R2: Localization to omega ~ a_0/c band",
          "R3: Amplitude matching equilibrium at crossover y ~ 1/C_eq",
          "R4: Scale-dependent coupling delta_rho(omega; g_bar)"]:
    print(f"  {r}")

print()


# ============================================================================
# PART 6: CONNECTION TO EXISTING KNOWLEDGE — WHAT WE ALREADY KNOW HELPS
# ============================================================================

print("=" * 80)
print("PART 6: BRIDGING TO KNOWN RESULTS — WHAT FOLLOWS FROM FIXED-POINT")
print("=" * 80)
print()

"""
From the fixed-point equation, we learn:

1. Milgrom's nu(y) uniquely determines the INTEGRAL of delta_rho(s; y)/s,
   NOT the function delta_rho(s; y) itself. The functional form is underdetermined.

2. This means: MANY different NESS mechanisms can produce the same Milgrom nu(y).
   The fixed-point equation constrains only one moment (weighted integral) of delta_rho.

3. To fix delta_rho uniquely, we need the PHYSICS — the specific backreaction equation
   that connects matter acceleration to vacuum state change. This is the content of tn15.

4. Key result: The fixed-point equation tells us WHAT delta_rho must do (constraints R1-R4).
   The NESS equation in tn15 tells us HOW it does it (specific functional form).

5. Both Stieltjes and KK failed to connect rho_eq to nu(y) because THEY ARE EQUILIBRIUM
   transforms. In NESS, the mapping is: delta_rho(s; y) -> delta_m(y) -> nu(y)^2 = 1 + delta_m/m_0.
   This is NOT an equilibrium transform — it depends on the dynamical state y through backreaction.
"""

print("Key insight from fixed-point analysis:")
print("  The fixed-point equation determines only ONE moment of delta_rho(s).")
print("  Milgrom's nu(y) at all y values constrains infinitely many moments,")
print("  but they are NOT independent — they are linked through the backreaction.")
print()
print("  Both Stieltjes and KK fail because they are EQUILIBRIUM transforms.")
print("  The NESS mapping is: trajectory -> backreaction -> rho_NE S(y) -> delta_m(y) -> nu(y)")
print("  This is a dynamical chain, not a linear transform on a fixed spectral density.")
print()


# ============================================================================
# SAVE RESULTS
# ============================================================================

results = {
    "title": "tn14: Self-Consistency Fixed-Point Equation for mu(x)",
    "key_result": {
        "C_eq": float(C_eq_p),
        "y_cross": float(y_cross),
        "min_delta_m": float(best.fun),
        "solution_exists": bool(best.fun < 0),
    },
    "constraints_on_delta_rho": {
        "R1_sign_flip": "Must be positive for deep MOND (low y), negative for Newtonian (high y)",
        "R2_localization": "Must be localized near omega ~ omega_c",
        "R3_amplitude": "Must match C_eq at crossover scale y ~ 1/C_eq",
        "R4_scale_dep": "delta_rho must depend on the dynamical state y = g_bar/a_0"
    },
    "interpretation": {
        "fixed_point_nature": "Underdetermined inverse problem — infinitely many delta_rho satisfy the constraint",
        "stieltjes_KK_failure": "Both fail because they are equilibrium transforms; NESS requires dynamical chain",
        "next_step": "tn15: physical NESS equation selects unique delta_rho from backreaction"
    },
}

results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tn14_fixed_point_results.json')
os.makedirs(os.path.dirname(results_path), exist_ok=True)
with open(results_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"Results saved: {results_path}")
print("=" * 80)
print("tn14 COMPLETE — fixed-point equation constrains delta_rho but does not fix it.")
print("Need physical NESS equation (tn15) to determine unique solution.")
print("=" * 80)

sys.exit(0)
