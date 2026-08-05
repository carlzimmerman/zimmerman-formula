#!/usr/bin/env python3
"""
tn07 — De Sitter-Corrected Unruh Response at a ~ H_dS

THE CRITICAL COMPUTATION: Can the FULL de Sitter Wightman function,
pulled back to an accelerated worldline at a ~ H (not the Rindler limit),
produce NEGATIVE spectral density in the Bunch-Davies vacuum?

Everything prior used the Rindler approximation a >> H. At a ~ H_dS,
the exact de Sitter geometry matters fundamentally.

PHYSICAL SETUP:
  Pure Rindler trajectory in dS_4:   Z^2 = 1 + (A/H)^2 sinh^2(A*Delta_tau/(2H))
  This is ALWAYS >= 1 (no light cone crossing).

  Acceleration + angular motion:      Z^2 involves sin^2 terms that can push
                                       Z toward 1 at specific Delta_tau values.

The question: does the dS-corrected Wightman function's commutator produce
rho(omega) < 0 even in BD vacuum?

LABELS: COMPUTED | ASSUMPTION | CONJECTURE
"""

import numpy as np
from scipy.integrate import quad, trapezoid
from scipy.optimize import minimize_scalar, brentq
import json, os, sys

# =========================================================================
# CONSTANTS (natural units H=1 everywhere; restore SI at end)
# =========================================================================
H = 1.0
eps_wightman = 1e-12  # i*eps prescription for Wightman function


# ============================================================================
# SECTION 0: THEORY — TWO TRAJECTORY TYPES IN DE SITTER SPACE
# ============================================================================

theory_section = """
TWO TYPES OF ACCELERATED TRAJECTORY IN dS_4:
==============================================

TYPE A — Pure Rindler (1+1d motion):
  Z^2(Δτ) = 1 + (A/H)^2 * sinh^2(A*Δτ/(2H))
  ALWAYS >= 1. No light cone crossing. Matches standard passivity theorem.

TYPE B — Acceleration + circular angular motion:
  From embedding space geometry for a trajectory at radius r_0 with
  proper acceleration A = H^2*r_0/sqrt(1-H^2*r_0^2):

  The invariant distance involves both hyperbolic (from radial boost)
  and trigonometric (from angular rotation in the static patch).

  Z^2 can approach or cross 1 for specific Δτ values, generating
  large imaginary parts in G+. This is the dS correction.

KEY RESULT: Type A confirms passivity (known). Type B is new territory
that requires computation at A ~ H where the MOND regime lives.
"""

print(theory_section)
print()


# ============================================================================
# SECTION 1: INVARIANT DISTANCE — CORRECT FORMULAS
# ============================================================================

def Zsq_rindler(dtau, A_over_H):
    """Type A: Pure Rindler trajectory in dS_4. ALWAYS >= 1."""
    if abs(dtau) < 1e-15:
        return 1.0
    arg = A_over_H * dtau / 2.0
    if abs(arg) < 500:
        return 1.0 + A_over_H**2 * np.sinh(arg)**2
    else:
        # Exponential regime — use exp form to avoid overflow
        sign = np.sign(arg)
        exp_val = np.exp(min(abs(arg), 700))
        return 1.0 + A_over_H**2 * exp_val**2 / 4.0


def Zsq_typeB(dtau, A_over_H, omega_frac=0.5):
    """Type B: Acceleration + circular angular motion in dS_4 static patch.

    For a trajectory with proper acceleration A at radius r_0, the invariant
    distance depends on both the radial boost (hyperbolic) and the angular
    rotation (trigonometric) in the embedding space.

    omega_frac: fraction of maximum allowed coordinate angular velocity.
    0 < omega_frac <= 1. At omega_frac = 1, trajectory approaches null.
    """
    if abs(dtau) < 1e-15:
        return 1.0

    # Radius from acceleration (A = H^2*r_0/sqrt(1-H^2*r_0^2))
    r0H_sq = A_over_H**2 / (1.0 + A_over_H**2)
    chi_sq = 1.0 + A_over_H**2

    # Max coordinate angular velocity for timelike trajectory:
    if r0H_sq <= 0 or r0H_sq >= 1 - 1e-15:
        return float('inf')

    max_omega_sq = (1.0 - r0H_sq) / r0H_sq
    omega = np.sqrt(max_omega_sq) * min(omega_frac, 0.99)

    # Hyperbolic term from radial boost
    arg_hyp = A_over_H * dtau / 2.0
    if abs(arg_hyp) < 500:
        cosh_val = np.cosh(arg_hyp)
    else:
        cosh_val = np.exp(min(abs(arg_hyp), 700)) / 2.0

    # Trigonometric term from angular motion
    sin_arg = omega * dtau / 2.0
    sin_val = np.sin(sin_arg)

    # Combined invariant distance (embedding space result):
    Zsq = chi_sq * cosh_val**2 - sin_val**2
    return Zsq


# VERIFICATION
print("=" * 80)
print("SECTION 1: INVARIANT DISTANCE VERIFICATION")
print("=" * 80)
print()

print("Type A (Pure Rindler) — must be >= 1 always:")
for A_H in [0.1, 0.5, 1.0, 2.0, 5.0]:
    dtau_test = [0.0, 1.0, 2.0, 5.0]
    for dt in dtau_test:
        zsq = Zsq_rindler(dt, A_H)
        print(f"  A/H={A_H:.1f}, dtau={dt:.1f}: Z^2={zsq:.4f}")
print()

print("Type B (Acceleration + circular) — CAN approach Z=1:")
for A_H in [0.1, 0.5, 1.0, 2.0]:
    for omega_frac in [0.3, 0.5, 0.7, 0.9]:
        dtau_scan = np.linspace(0.01, 10.0, 2000)
        Zsq_vals = [Zsq_typeB(d, A_H, omega_frac) for d in dtau_scan]
        Zsq_min = min(Zsq_vals) if all(np.isfinite(z) for z in Zsq_vals) else float('inf')
        dtau_at_min = dtau_scan[np.argmin([abs(z) for z in Zsq_vals if np.isfinite(z)])] if any(np.isfinite(z) for z in Zsq_vals) else None
        crossing = "NEAR-ZERO!" if Zsq_min < 0 else "approaches 1" if Zsq_min < 1.5 else "safe"
        print(f"  A/H={A_H:.1f}, omega_frac={omega_frac:.1f}: Z^2_min={Zsq_min:8.4f} at dtau={dtau_at_min:.2f}  [{crossing}]")
    print()


# ============================================================================
# SECTION 2: WIGHTMAN FUNCTION AND COMMUTATOR
# ============================================================================

print("=" * 80)
print("SECTION 2: WIGHTMAN FUNCTION G+(Z^2) AND COMMUTATOR Im[C]")
print("=" * 80)
print()


def wightman_gplus(dtau, A_over_H, traj_type='A', omega_frac=0.5):
    """G+(Δτ) = -1/(16π²(Z²-1+iε)) for conformal scalar on dS_4."""
    if traj_type == 'A':
        zsq = Zsq_rindler(dtau, A_over_H)
    else:
        zsq = Zsq_typeB(dtau, A_over_H, omega_frac)

    if not np.isfinite(zsq):
        return complex(0.0, 0.0)

    zsq_minus_1 = zsq - 1.0
    if abs(zsq_minus_1) < 1e-20:
        return complex(0.0, -np.pi * np.sign(dtau)) / (16.0 * np.pi**2 + 1e-30)

    denom = zsq_minus_1 + 1j * eps_wightman * np.sign(zsq_minus_1) if abs(zsq_minus_1) > 0 else 1j * eps_wightman
    return -1.0 / (16.0 * np.pi**2 * denom)


def wightman_gplus_neg(dtau, A_over_H, traj_type='A', omega_frac=0.5):
    """G+(-Δτ) = conjugate of G+(Δτ) for the trajectory."""
    return np.conj(wightman_gplus(dtau, A_over_H, traj_type, omega_frac)) if dtau > 0 else wightman_gplus(-dtau, A_over_H, traj_type, omega_frac)


def commutator_im(dtau, A_over_H, traj_type='A', omega_frac=0.5):
    """Im[C(Δτ)] = Im[G+(Δτ) - G+(-Δτ)] for Δτ > 0."""
    if abs(dtau) < 1e-15:
        return 0.0
    Gp = wightman_gplus(abs(dtau), A_over_H, traj_type, omega_frac)
    Gn = wightman_gplus_neg(abs(dtau), A_over_H, traj_type, omega_frac)
    return Gp.imag - Gn.imag


# Sample the commutator for different trajectory types
print("Im[C(Δτ)] across acceleration regimes:")
print()

for A_H in [0.1, 0.5, 1.0, 2.0]:
    print(f"  A/H = {A_H:.1f}:")
    for traj_type in ['A', 'B']:
        omega_f = 0.5 if traj_type == 'B' else None
        dtau_test = [0.5, 1.0, 2.0, 3.0, 5.0]
        for dt in dtau_test:
            imC = commutator_im(dt, A_H, traj_type, omega_frac=omega_f)
            print(f"    {traj_type}: dtau={dt:.1f} => Im[C]={imC:.6e}")
        print()


# ============================================================================
# SECTION 3: SPECTRAL DENSITY — FOURIER TRANSFORM OF COMMUTATOR
# ============================================================================

print("=" * 80)
print("SECTION 3: SPECTRAL DENSITY rho(omega)")
print("=" * 80)
print()


def spectral_density_trapz(omega, A_over_H, traj_type='A', omega_frac=0.5,
                            dtau_max=100.0, N=8000, eta=0.02):
    """rho(ω) = -∫₀^∞ dτ e^{-ητ} sin(ωτ) Im[C(τ)] / π"""
    if omega <= 0:
        return 0.0

    dtau_grid = np.linspace(0.001, dtau_max, N)
    ImC_vals = np.array([commutator_im(d, A_over_H, traj_type, omega_frac) for d in dtau_grid])

    integrand = -np.exp(-eta * dtau_grid) * np.sin(omega * dtau_grid) * ImC_vals
    return trapezoid(integrand, dtau_grid) / np.pi


# Broad scan: trajectory type × acceleration × frequency
print("SPECTRAL DENSITY SCAN:")
print()
print(f"{'Trj':<5} {'A/H':<8} {'omega':<8} {'rho(omega)':<18}")
print("-" * 45)

results = {}
most_negative_rho = 0.0
most_negative_key = None

for traj_type in ['A', 'B']:
    for A_H in [0.1, 0.3, 0.5, 0.7, 1.0, 2.0, 5.0]:
        omega_fracs = [0.5] if traj_type == 'A' else [0.3, 0.5, 0.7, 0.9]

        for omega_f in omega_fracs:
            for omega in [0.1, 0.5, 1.0, 2.0, 3.0, 5.0]:
                rho = spectral_density_trapz(omega, A_H, traj_type, omega_f)
                key = (traj_type, A_H, omega_f, omega)
                results[key] = float(rho)

                if rho < most_negative_rho:
                    most_negative_rho = rho
                    most_negative_key = key

                marker = " NEGATIVE <<<<" if rho < -1e-8 else ""
                print(f"  {traj_type:<3} {A_H:<8.1f} {omega:<8.1f} {rho:<18.6e}{marker}")
            if traj_type == 'B' and omega_f < 0.9:
                print()

print()


# ============================================================================
# SECTION 4: CRITICAL FINDING
# ============================================================================

if most_negative_key:
    t, a, w, om = most_negative_key
    print("=" * 80)
    print("CRITICAL RESULT:")
    print(f"  Most negative rho = {most_negative_rho:.6e}")
    print(f"  Trajectory type = '{t}', A/H = {a:.1f}, omega_frac = {w:.1f}, omega = {om:.1f}")
    print()
    if t == 'B':
        print("NEGATIVE spectral density found for Type B (acceleration + circular motion).")
        print("This is the dS correction: angular motion in the static patch allows")
        print("Z to approach 1, generating large Im[C] that produces negative rho.")
    else:
        print("Negative spectral density found even for pure Rindler (Type A).")
        print("Need to investigate — this should not happen for pure Rindler!")
else:
    print("=" * 80)
    print("No significant negative spectral density found in the scan.")
    print("The passivity wall may hold even with exact dS geometry.")


# ============================================================================
# SAVE RESULTS
# ============================================================================

results_path = os.path.join(os.path.dirname(__file__), 'phase_ds_unruh_results.json')
output = {
    "most_negative_rho": float(most_negative_rho),
    "most_negative_params": str(most_negative_key),
    "all_results": {str(k): v for k, v in results.items()},
}

with open(results_path, 'w') as f:
    json.dump(output, f, indent=2)
print(f"\nResults saved: {results_path}")
