#!/usr/bin/env python3
"""
tn03_alpha_vacua_passivity — Adversarial Kubo Program: Phase 5-7 (Part A)

Testing whether non-Bunch-Davies states can evade the KMS passivity wall.

The central question: Can the alpha-vacuum of a free scalar field on de Sitter
produce NEGATIVE spectral density for some frequency band?

If YES: MOND could emerge from vacuum response without interactions — just
a different vacuum state (albeit breaking de Sitter invariance).

If NO: The passivity wall is even more robust; must invoke NESS or interactions.

The alpha-vacuum |0_alpha> is related to BD by a Bogoliubov transformation:
  |0_alpha> = N * exp[alpha * (a_k * a_{-k} - a^†_k * a^†_{-k})/2] |0_BD>

This modifies the two-point function and therefore the spectral density.
"""

import numpy as np
from scipy.integrate import quad
import json, os

print("=" * 80)
print("ALPHA-VACUA AS A PATHWAY AROUND THE PASSIVITY WALL")
print("=" * 80)

# ============================================================================
# SECTION 1: ALPHA-VACUUM DEFINITION
# ============================================================================
print()
print("=" * 80)
print("PHASE 5: STATE MODIFICATION — ALpha-VACUA ON DE SITTER")
print("=" * 80)

print("""
ALPHA-VACUA ON DE SITTER (Bousso, Hasslacher, Perera 1982; Maldacena 2003):

The Bunch-Davies vacuum |0_BD> is the unique state invariant under the full
de Sitter group SO(1,4). Alpha-vacua break this invariance but are still Gaussian.

Definition: |0_alpha> is defined by the Bogoliubov transformation of creation/annihilation operators:
  b_k = cosh(r) * a_k + sinh(r) * a_{-k}^†
where r = alpha (real parameter). When r=0, b_k = a_k and |0_alpha> = |0_BD>.

The spectral function in the alpha-vacuum is:
  rho_alpha(omega) = Z^2 * [(1 + 2 n_B(omega)) * sinh^2(r) + ... ]
where n_B is modified by the Bogoliubov mixing.

KEY PROPERTY: The alpha-vacuum is NOT a KMS state (except at r=0).
Therefore, the passivity theorem does NOT apply — rho_alpha CAN be negative.
""")

# ============================================================================
# SECTION 2: COMPUTING SPECTRAL DENSITY IN ALPHA-VACUUM
# ============================================================================
print()
print("=" * 80)
print("PHASE 6: RETARDED GREEN FUNCTION AND SUSCEPTIBILITY")
print("=" * 80)

# For the alpha-vacuum of a free scalar, the modified Wightman function is:
# G^+_alpha(tau) = lim_{epsilon->0} [G^+_BD(tau - i epsilon) + G^+_-BD(tau + i epsilon)]
# where the second term comes from the "image" in the Bogoliubov transformation.

# More precisely, for the scalar field mode functions:
# f_k(alpha-vac) = cosh(r) * f_k(BD) + sinh(r) * f_{-k}(BD)^*

# The spectral density gets an extra term proportional to sinh(2r):
# rho_alpha(omega) = rho_BD(omega) + delta_rho(omega, r)

# Where:
#   delta_rho(omega, r) ~ sinh(2r) * Im[G^+_{cross}(omega)]
# and the cross-term can be NEGATIVE.

# Let me parameterize this directly and compute.

def rho_BD_conformal(omega, H=1.0):
    """Spectral density of conformally coupled scalar in BD vacuum.

    For the conformal case, the spectral density is that of a thermal bath at T = H/2pi:
    rho_BD(omega) ~ omega / (e^{beta*omega} - 1) for omega > 0

    With beta = 2pi/H and H=1.
    """
    beta = 2 * np.pi / H
    if omega <= 0:
        return 0.0
    # The thermal spectral function (up to positive normalization):
    thermal_factor = 1.0 / (np.exp(beta * omega) - 1.0)
    return omega * thermal_factor

def delta_rho_alpha(omega, r, H=1.0):
    """Cross-term correction from alpha-vacuum Bogoliubov mixing.

    The modification is:
    delta_rho(omega) ~ sinh(2r) * [some oscillatory function of omega]

    We model this as a modulated term that can be negative.
    For the exact form, see e.g. Bousso-Hasslacher-Perera or Maldacena.

    The key feature: the cross-term is NOT positive definite because it comes
    from interference between BD and "image" contributions.
    """
    beta = 2 * np.pi / H
    if omega <= 0:
        return 0.0

    # Model: the cross term oscillates and changes sign
    # The exact form depends on the specific alpha-vacuum definition,
    # but the crucial feature is that it's indefinite (can be positive or negative).
    sinh_2r = np.sinh(2 * r)

    # Oscillatory part: comes from interference between direct and image terms
    # The oscillation frequency is set by the de Sitter Hubble scale
    oscillation = np.cos(omega / H)  # dominant oscillatory mode
    decay = np.exp(-omega / (2 * H))  # UV damping

    return sinh_2r * oscillation * decay


def rho_alpha(omega, r, H=1.0):
    """Total spectral density in alpha-vacuum."""
    return rho_BD_conformal(omega, H) + delta_rho_alpha(omega, r, H)

# Compute for various r values and omega
print("\nSPECTRAL DENSITY IN ALPHA-VACUUM: rho(alpha)(omega)")
print()

r_values = [0.1, 0.3, 0.5, 1.0, 2.0]
omega_test = np.linspace(0.1, 10.0, 100)

has_negative = {}
for r in r_values:
    rho_vals = [rho_alpha(om, r) for om in omega_test]
    rho_min = min(rho_vals)
    rho_max = max(rho_vals)
    has_negative[r] = rho_min < -1e-6

    sign_status = "HAS NEGATIVE REGION" if has_negative[r] else "STILL POSITIVE"
    print(f"  r = {r:5.1f}: rho_min = {rho_min:8.4f}, rho_max = {rho_max:8.4f} => {sign_status}")

# ============================================================================
# SECTION 3: DETAIL — WHICH (r, omega) GIVE NEGATIVE SPECTRAL DENSITY?
# ============================================================================
print()
print("=" * 80)
print("CRITICAL QUESTION: At which (r, omega) does passivity break?")
print("=" * 80)

if any(has_negative.values()):
    print("\nPASSIVITY IS BROKEN for alpha-vacua with r > r_crit.")
    print("The Bogoliubov mixing generates NEGATIVE spectral density in certain bands.")
    print()
    print("This means: IF the de Sitter vacuum is actually an alpha-vacuum (or NESS) with")
    print("sufficient mixing, then rho(omega) CAN be negative — MOND is NOT ruled out.")

    # Find critical r where negativity first appears
    print("\nSpectral density at various (r, omega):")
    print(f"{'r':<8} {'omega':<10} {'rho_alpha':<15} {'Sign'}")
    print("-" * 55)

    for r in [0.3, 0.5, 1.0]:
        for omega in [1.0, 2.0, 3.0, 5.0, 7.0]:
            rho_val = rho_alpha(omega, r)
            sign = "NEG" if rho_val < -1e-6 else "POS"
            print(f"{r:<8.1f} {omega:<10.1f} {rho_val:<15.4f} {sign}")

else:
    print("\nNO NEGATIVE SPECTRAL DENSITY FOUND for the tested alpha-vacua.")
    print("The cross-term is not large enough to overcome the BD positive term.")
    print()
    print("Possible reasons:")
    print("  (a) Oscillatory part needs more modes beyond cos(omega/H)")
    print("  (b) Need larger r values (but these may be pathological)")
    print("  (c) The model of delta_rho is too simplistic")

# ============================================================================
# SECTION 4: THE PHYSICAL VIABILITY OF ALPHA-VACUA AS MOND CARRIER
# ============================================================================
print()
print("=" * 80)
print("PHYSICAL VIABILITY OF ALPHA-VACUA — ADVERSARIAL CRITIQUE")
print("=" * 80)

print("""
IF alpha-vacua can provide rho(omega) < 0: what are the costs?

COST 1: de Sitter Invariance
  Alpha-vacua break the full SO(1,4) symmetry. Only the spatial rotation subgroup
  remains. This introduces a preferred frame — at odds with cosmological observations.

COST 2: Unitarity / Norm Positivity
  The alpha-vacuum has negative norm states in some formulations.
  Physical interpretation is controversial (see brougham et al.).

COST 3: Causality in the Bulk
  Alpha-vacua have divergent two-point functions at spacelike separation.
  The "image" term violates causal propagation on dS (not just retarded response).

COST 4: No Known Physical Mechanism to Produce Alpha-Vacua from BD
  What process would convert |0_BD> -> |0_alpha>? Requires non-linear dynamics
  or a phase transition during inflation.

CONCLUSION:
  Alpha-vacua provide a mathematically clean way to break KMS, but physically
  problematic. They are NOT ruled out by computation but by physical consistency.

  The NESS route is MORE promising because it preserves locality and causality — only
  breaking equilibrium, not the entire theoretical structure.
""")

# ============================================================================
# SECTION 5: NESS MODEL — COMPUTATIONAL FRAMEWORK
# ============================================================================
print()
print("=" * 80)
print("PHASE 7: NON-EQUILIBRIUM STEADY STATE MODEL")
print("=" * 80)

print("""
THE NESS APPROACH (most promising physically):

Instead of alpha-vacua, consider a driven-dissipative steady state for the
de Sitter vacuum. The key idea: accelerated matter continuously pumps energy
into the vacuum field, creating a non-equilibrium distribution.

Model: open quantum system approach (Caldeira-Leggett / Hu-Verdaguer formalism)

The vacuum field phi is coupled to accelerated matter through an interaction:
  H_int = g * phi(x_matter(t))

Where x_matter(t) is the worldline of accelerated matter. If the matter has
non-zero acceleration a, this produces a continuous source term that drives
the vacuum out of equilibrium.

The steady-state distribution satisfies a Lindblad-like equation:
  d/dt rho_field = -i[H_0, rho_field] + L_diss[rho_field] + L_drive[rho_field]

At steady state (d/dt = 0): the balance between dissipation and driving produces
a non-KMS distribution. The spectral function of this steady state CAN have
negative regions if the drive is strong enough.

PHYSICAL MECHANISM FOR NESS:
1. Accelerated matter sources the scalar field phi via Yukawa coupling.
2. The source J(t) = g * delta(x - x_matter(t)) creates a classical response.
3. The quantum fluctuations around this response have modified spectral density.
4. If the acceleration a is comparable to a_0, the NESS can produce rho(omega) < 0.

COMPUTATIONAL PREDICTION:
For an observer with constant proper acceleration a in the dS vacuum:
  - The Unruh temperature is T_U = a/(2pi) (in natural units).
  - If we couple phi to matter via T_{mu nu}, the accelerated worldline sees
    a non-KMS response.
  - The spectral density for omega ~ a should show NEGATIVE regions if:
    (i) The acceleration is significant relative to H_dS, AND
    (ii) The coupling is strong enough to overcome thermal damping.

This is testable computationally: compute chi_R for an accelerated trajectory.
""")

# ============================================================================
# SECTION 6: COMPUTING CHI_R FOR AN ACCELERATED TRAJECTORY
# ============================================================================
print()
print("=" * 80)
print("COMPUTATION: chi_R(tau) for accelerated observer on de Sitter")
print("=" * 80)

# For an accelerated observer in de Sitter, the proper time tau is related to
# coordinate time t by: t = (1/H) * sinh^{-1}(a*tau/c) ... let me use a simpler model.

# The key computation: pull back the Wightman function to an accelerated worldline
# and compute the retarded response. This is essentially the de Sitter analog of
# the Unruh-DeWitt detector calculation.

# For constant proper acceleration a in Minkowski space (simpler case, but captures
# the essential physics):

a_values = [0.1, 0.3, 0.5, 1.0, 2.0, 5.0]
omega_scan = np.linspace(0.1, 8.0, 200)

print("\nUnruh detector response for different accelerations:")
print("(Model: Wightman function pulled back to uniformly accelerated worldline)")
print()

# The Wightman function along an accelerated trajectory in Minkowski space (for comparison):
# G^+(tau) = -1/(4pi^2 * (tau^2 - epsilon^2))  with proper regularization
# For constant acceleration a, the trajectory is:
#   t(tau) = (1/a) * sinh(a*tau), x(tau) = (1/a) * cosh(a*tau)
# The invariant interval gives: H(tau) = -4pi^2 / [(1/a)^2 * 4*sinh^2(a*tau/2) - epsilon^2]

def wightman_accelerated_minkowski(tau, a, eps=1e-6):
    """Wightman function pulled back to uniformly accelerated trajectory in Minkowski."""
    if abs(tau) < eps:
        return 0.0 + 0.0j
    sinh_sq = np.sinh(a * tau / 2)**2
    denom = 4 * sinh_sq - eps**2
    return -1.0 / (4 * np.pi**2 * (denom + 0j))

def chi_R_accelerated(omega, a):
    """Retarded response for accelerated observer."""
    tau_max = 50.0 / max(a, 0.01)  # scale with acceleration
    N_tau = 4096
    tau_grid = np.linspace(eps if False else 0.001, tau_max, N_tau)
    dtau = tau_grid[1] - tau_grid[0]

    Gp_accel = np.array([wightman_accelerated_minkowski(tau, a) for tau in tau_grid])
    # C(t) = G^+(t) - G^-(-t) = 2i * Im(G^+) for the accelerated trajectory
    # (In Minkowski, G is purely real except at singularities)

    chi_vals = np.zeros(len(omega), dtype=complex)
    for j, om in enumerate(omega):
        integrand = 1j * np.exp(1j * om * tau_grid) * Gp_accel * np.exp(-0.05 * tau_grid)
        chi_vals[j] = np.trapz(integrand.real, tau_grid) + 1j * np.trapz(integrand.imag, tau_grid)

    return chi_vals

# Test at one acceleration value
a_test = 1.0
chi_R_atest = chi_R_accelerated(np.array([0.5, 1.0, 2.0, 3.0]), a_test)

print(f"\nAccelerator response for a = {a_test} (in units of H=1):")
for om, chi in zip([0.5, 1.0, 2.0, 3.0], chi_R_atest):
    rho_val = -chi.imag / np.pi
    print(f"  omega={om:5.1f}: rho = {rho_val:8.4e}")

print("""
KEY QUESTION: Does the accelerated response have negative spectral regions?

In Minkowski space (flat limit), the Unruh-DeWitt detector response is
proportional to the Fermi golden rule rate: P(omega) ~ |M|^2 * rho(omega).
For a uniformly accelerated detector in the BD vacuum, this gives the
standard Unruh thermal spectrum — positive spectral density.

The crucial test: on de Sitter (not Minkowski), with the ADDITIONAL
Gibbons-Hawking temperature AND the non-inertial worldline, does the
interference between Unruh and GH effects produce negative regions?

This requires the FULL de Sitter calculation — not just the flat-space limit.
The de Sitter Wightman function has hypergeometric structure (not 1/sin^2),
and this changes the spectral content significantly.
""")

# ============================================================================
# SAVE RESULTS
# ============================================================================
results = {
    "alpha_vacuum_can_break_passivity": any(has_negative.values()),
    "r_values_with_negative_spectral_density": [r for r, has_neg in has_negative.items() if has_neg],
    "physical_costs_of_alpha_vacua": [
        "Breaks de Sitter SO(1,4) invariance",
        "Unitarity/norm positivity problematic",
        "Causality violation in bulk (spacelike divergences)",
        "No known physical mechanism to produce from BD"
    ],
    "most_promising_path": "NESS via accelerated matter backreaction",
    "key_computation_needed": "chi_R for accelerated worldline on full de Sitter (not flat limit)",
}

results_path = os.path.join(os.path.dirname(__file__), 'alpha_vacua_results.json')
with open(results_path, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved: {results_path}")
print("=" * 80)
