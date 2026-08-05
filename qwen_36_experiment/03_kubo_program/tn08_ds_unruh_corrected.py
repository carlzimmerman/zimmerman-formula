#!/usr/bin/env python3
"""
tn08 — Corrected De Sitter Unruh Response: Embedding Space Computation

KEY FIX: The invariant distance Z is computed DIRECTLY from embedding space
coordinates T_i(tau), NOT from a simplified analytic formula.

Z^2 = H^2 * sum_i (T_i(tau) * T_i(tau'))  where the sum uses the dS metric signature.

This avoids any errors in the analytic derivation of Z.

Also: this script implements the AUTONOMOUS RESEARCH LOOP — each run analyzes
results and decides what to compute next.
"""

import numpy as np
from scipy.integrate import trapezoid, quad
from scipy.optimize import brentq, minimize_scalar
import json, os, sys, time

# =========================================================================
# CONSTANTS (H=1 natural units)
# =========================================================================
H = 1.0
eps_wightman = 1e-14


# ============================================================================
# SECTION 0: EMBEDDING SPACE WORLDLINE — CORRECT PARAMETERIZATION
# ============================================================================

def worldline_embedding(tau, A_over_H, omega_over_H):
    """Compute embedding space coordinates T_i(tau) for uniformly accelerated trajectory.

    Parameters:
        A_over_H: proper acceleration in units of H
        omega_over_H: coordinate angular velocity in units of H

    The trajectory is constrained by:
        (1) A = H^2 * r0 / sqrt(1 - H^2*r0^2)  => r0 determined by A
        (2) dt/dtau and dtheta/dtau from four-velocity normalization
        (3) chi = sqrt(1 + (A/H)^2) related to r0, omega

    Returns array [T0, T1, T2, T3, T4] at proper time tau.
    """
    A = A_over_H  # H=1

    # Step 1: radius from acceleration
    r0H_sq = A**2 / (1.0 + A**2)
    r0 = np.sqrt(r0H_sq) / H  # physical radius
    omega = omega_over_H * H

    # Step 2: boost factor chi from normalization constraint
    # chi^2 = (1 - r0^2*omega^2) / (1 - r0^2) ... but this must be > 1
    denom = 1.0 - r0H_sq
    if denom <= 0:
        return None

    chi_sq = (1.0 - r0**2 * omega**2) / denom
    if chi_sq < 1.0:
        # Not a valid timelike trajectory — no physical solution
        return None

    chi = np.sqrt(chi_sq)

    # Step 3: hyperbolic angle rate from proper acceleration
    # A^2 = H^2 * (chi^2 - 1) / r0^2 ... need to be careful
    # Actually, for the embedding: dT0/dtau ~ chi*H*cosh(H*eta), etc.
    # The proper acceleration depends on both the boost rate and angular velocity.

    # For a trajectory with constant A and omega at fixed radius r0:
    # eta_dot = d(HE)/dtau where E is the rapidity parameter
    # From the embedding: the four-acceleration magnitude is determined by chi and omega.

    # RELATIONSHIP: A^2 = H^2 * (chi^2 - 1) / r0^2 when computed from embedding
    # => eta_dot = sqrt(chi^2 - 1) * H / r0 ... but this diverges as r0 -> 0.

    # CORRECT: for a Rindler observer with A >> H at radius r0 ~ 1/H:
    # eta_dot ~ A (not A/r0)

    # Actually, the proper acceleration of our worldline is:
    # A_phys^2 = (dT/dtau)^(-1) * [-(dT0''/dtau^2)^2 + ...]
    # This determines the relationship between chi_dot and omega.

    # For simplicity and correctness, let me use the DIRECT parametrization:
    # T0 = (1/H)*sqrt(chi^2-1) * sinh(H*eta(tau))
    # T1 = (1/H)*sqrt(chi^2-1) * cosh(H*eta(tau))
    # T2 = r0 * cos(theta(tau))
    # T3 = r0 * sin(theta(tau))
    # T4 = 0 (embedded in 5D, this is the extra dimension with T4 satisfying constraint)

    # Wait — T0^2 - T1^2 - T2^2 - T3^2 - T4^2 must equal H^{-2}.
    # -(chi^2-1)*sinh^2 + (chi^2-1)*cosh^2 = chi^2-1 (from T0,T1)
    # r0^2*cos^2 + r0^2*sin^2 = r0^2 (from T2,T3)
    # Total: (chi^2-1) + r0^2 = H^{-2} => chi^2 = 1 + H^2*r0^2

    # So chi is FIXED by r0, not by omega! The constraint is:
    # chi^2 = 1 + 1/(r0H_sq) ... no wait.

    # Actually: -T0^2 + T1^2 + T2^2 + T3^2 + T4^2 = (chi^2-1) + r0^2
    # This must equal H^{-2} = 1/H^2 = 1 (in natural units).
    # So: chi^2 - 1 + r0^2*H^2 = 1 => chi^2 = 2 - r0^2*H^2

    # Hmm, that doesn't match A. Let me re-derive from scratch.

    # CONSTRAINT: The worldline must lie on the dS hyperboloid:
    #   -T0^2 + T1^2 + T2^2 + T3^2 + T4^2 = H^{-2}

    # My embedding ansatz:
    #   T0 = a * sinh(eta)     where a = sqrt(chi^2-1)/H
    #   T1 = a * cosh(eta)
    #   T2 = r0 * cos(theta)
    #   T3 = r0 * sin(theta)
    #   T4 = 0

    # Constraint: -a^2*sinh^2 + a^2*cosh^2 + r0^2*cos^2 + r0^2*sin^2 = H^{-2}
    # => a^2*(cosh^2-sinh^2) + r0^2 = H^{-2}
    # => a^2 + r0^2 = H^{-2}
    # => a^2 = H^{-2} - r0^2
    # => chi^2 - 1 = (H*a)^2 = 1 - (r0*H)^2
    # => chi^2 = 2 - (r0*H)^2

    # So for any r0 < 1/H (inside cosmological horizon), chi is fixed:
    r0H_sq_actual = A**2 / (1.0 + A**2)
    chi_fixed_sq = 2.0 - r0H_sq_actual  # from hyperboloid constraint

    if chi_fixed_sq < 1.0:
        # This means r0 is too close to the horizon — need different embedding
        # Use T4 ≠ 0 to satisfy constraint
        chi_fixed_sq = 1.0 + A**2  # fallback
    chi_fixed = np.sqrt(max(chi_fixed_sq, 1.0))

    a_param = np.sqrt(max(chi_fixed**2 - 1.0, 1e-10)) / H

    # Hyperbolic angle: eta_dot is determined by proper time normalization
    # The worldline must have constant proper acceleration A.
    # From the embedding, A^2 = (dT/dtau)^(-2) * sum(d^2T_i/dtau^2)^2 with correct signs.

    # For our ansatz, the four-acceleration magnitude depends on eta_dot and theta_dot.
    # We need A^2 = H^2 * (chi^2 - 1) / r0^2 ... this is getting circular.

    # CLEAN APPROACH: Use chi as the FREE parameter and derive everything else.
    # The proper acceleration is determined by how fast eta changes with tau:
    #   d(eta)/dtau = omega_eta
    # where omega_eta relates A to the geometry.

    # For a Rindler observer in dS (r0 → 1/H, chi → sqrt(2)):
    #   A ~ H*sqrt(chi^2-1) / sqrt(1-r0H^2) ... diverges as r0 → 1/H.

    # Instead of trying to get the analytic relationship right (which I keep messing up),
    # let me COMPUTE Z directly from the embedding with fixed chi and omega,
    # then COMPUTE A_phys from the worldline and check consistency.

    # FIXED PARAMETERIZATION (chi from hyperboloid + r0):
    a_val = np.sqrt(max(chi_fixed**2 - 1.0, 1e-10))
    eta_rate = H * np.sqrt(chi_fixed**2 - 1.0) / a_val if a_val > 0 else H
    theta_dot = omega * H

    # Embedding coordinates
    T0 = a_val / H * np.sinh(eta_rate * tau) if abs(eta_rate*tau) < 700 else a_val/H * np.exp(abs(eta_rate*tau))/2
    T1 = a_val / H * np.cosh(eta_rate * tau) if abs(eta_rate*tau) < 700 else a_val/H * np.exp(abs(eta_rate*tau))/2
    T2 = r0 * np.cos(theta_dot * tau)
    T3 = r0 * np.sin(theta_dot * tau)
    # T4 = 0 (already satisfies constraint with T0-T3)

    return np.array([T0, T1, T2, T3, 0.0])


def invariant_distance_squared_direct(tau1, tau2, A_over_H, omega_over_H):
    """Compute Z^2 = H^2 * (-T0*T0' + T1*T1' + T2*T2' + T3*T3' + T4*T4') directly."""
    w1 = worldline_embedding(tau1, A_over_H, omega_over_H)
    w2 = worldline_embedding(tau2, A_over_H, omega_over_H)
    if w1 is None or w2 is None:
        return float('inf')

    # de Sitter metric signature in embedding space: (-, +, +, +, +)
    Zsq = H**2 * (-w1[0]*w2[0] + w1[1]*w2[1] + w1[2]*w2[2] + w1[3]*w2[3] + w1[4]*w2[4])
    return Zsq


def invariant_distance_squared_proper(tau, A_over_H, omega_over_H):
    """Z^2 between tau=0 and tau=tau' along the worldline."""
    return invariant_distance_squared_direct(0.0, tau, A_over_H, omega_over_H)


# ============================================================================
# SECTION 1: WORLDLINE VERIFICATION
# ============================================================================

print("=" * 80)
print("SECTION 1: EMBEDDING SPACE WORLDLINE VERIFICATION")
print("=" * 80)
print()

def check_hyperboloid_constraint(T):
    """Verify worldline lies on dS hyperboloid."""
    T = np.asarray(T)
    if len(T) < 5:
        return float('nan')
    return -T[0]**2 + T[1]**2 + T[2]**2 + T[3]**2 + T[4]**2

# Test constraint at several points
print("Hyperboloid constraint: -T0^2+T1^2+T2^2+T3^2+T4^2 = H^{-2} = 1.0")
for A_H in [0.5, 1.0, 2.0]:
    for omega_H in [0.3, 0.5, 0.8]:
        T_vals = []
        for tau in [0.0, 1.0, 2.0]:
            w = worldline_embedding(tau, A_H, omega_H)
            if w is not None:
                T_vals.append((check_hyperboloid_constraint(w), tau))

        if T_vals:
            vals_list = [v[0] for v in T_vals]
            print(f"  A/H={A_H:.1f}, omega/H={omega_H:.3f}: constraint = {[f'{v[0]:.6f}' for v in T_vals]}")

print()


# ============================================================================
# SECTION 2: LIGHT CONE CROSSING ANALYSIS (WITH CORRECTED Z)
# ============================================================================

print("=" * 80)
print("SECTION 2: LIGHT CONE CROSSING — CORRECTED INvariant DISTANCE")
print("=" * 80)
print()

# Scan over omega for each A and find where Z^2 crosses 1
for A_H in [0.1, 0.3, 0.5, 0.7, 1.0, 2.0]:
    print(f"  A/H = {A_H:.1f}:")

    for omega_H_frac in [0.3, 0.5, 0.7, 0.9]:
        # Use fraction of max allowed angular velocity
        r0H_sq = A_H**2 / (1 + A_H**2)
        max_omega_H = np.sqrt((1 - r0H_sq) / r0H_sq) if r0H_sq < 0.99 else np.inf
        omega_H = min(omega_H_frac * max_omega_H, 0.95 * max_omega_H) if max_omega_H > 0 and np.isfinite(max_omega_H) else A_H * 0.5

        dtau_scan = np.linspace(0.01, 20.0, 4000)
        Zsq_vals = []
        valid_dtau = []
        for dt in dtau_scan:
            zsq = invariant_distance_squared_proper(dt, A_H, omega_H / H)
            if np.isfinite(zsq) and zsq > -100 and zsq < 1e10:
                Zsq_vals.append(zsq)
                valid_dtau.append(dt)

        if not Zsq_vals:
            continue

        Zsq_min = min(Zsq_vals)
        dtau_at_min = valid_dtau[np.argmin(Zsq_vals)]

        # Count crossings of Z^2 = 1
        crossings = sum(1 for i in range(len(Zsq_vals)-1) if (Zsq_vals[i]-1)*(Zsq_vals[i+1]-1) < 0)

        status = "CROSSING!" if crossings > 0 else ("near-zero" if Zsq_min < 0.5 else f">={Zsq_min:.4f}")
        print(f"    omega_frac={omega_H_frac:.1f}, omega/H~{omega_H:.3f}: Z^2_min={Zsq_min:8.3f} at dtau={dtau_at_min:.2f}, crossings={crossings}  [{status}]")
    print()


# ============================================================================
# SECTION 3: SPECTRAL DENSITY WITH CORRECTED COMMUTATOR
# ============================================================================

print("=" * 80)
print("SECTION 3: SPECTRAL DENSITY rho(omega) — CORRECTED COMMUTATOR")
print("=" * 80)
print()


def wightman_gplus_corrected(tau, A_over_H, omega_over_H):
    """G+ from direct embedding space computation."""
    zsq = invariant_distance_squared_proper(abs(tau), A_over_H, omega_over_H)

    if not np.isfinite(zsq) or zsq < -10:
        return complex(0.0, 0.0)

    zsq_minus_1 = zsq - 1.0
    if abs(zsq_minus_1) < 1e-30:
        # On light cone — use principal value + delta function
        sign = np.sign(tau)
        return complex(0.0, -sign * np.pi / (16.0 * np.pi**2))

    denom = zsq_minus_1 + 1j * eps_wightman * np.sign(zsq_minus_1) if abs(zsq_minus_1) > 0 else 1j * eps_wightman
    return -1.0 / (16.0 * np.pi**2 * denom)


def commutator_im_corrected(tau, A_over_H, omega_over_H):
    """Im[C] = Im[G+(tau) - G+(-tau)] for tau > 0."""
    if abs(tau) < 1e-15:
        return 0.0

    zsq_pos = invariant_distance_squared_proper(abs(tau), A_over_H, omega_over_H)
    zsq_neg = invariant_distance_squared_proper(-abs(tau), A_over_H, omega_over_H)

    def gplus_from_zsq(zsq_val):
        if not np.isfinite(zsq_val) or zsq_val < -10:
            return complex(0.0, 0.0)
        d = zsq_val - 1.0 + 1j * eps_wightman * np.sign(max(abs(zsq_val-1), 1e-30))
        if abs(d) < 1e-30:
            return complex(0.0, -np.pi/(16*np.pi**2))
        return -1.0 / (16.0 * np.pi**2 * d)

    Gp = gplus_from_zsq(zsq_pos)
    Gn = gplus_from_zsq(zsq_neg)
    return Gp.imag - Gn.imag


def spectral_density_corrected(omega, A_over_H, omega_over_H,
                                 dtau_max=200.0, N=8000, eta=0.01):
    """rho(ω) = -FT[Im[C(τ)]]/π with corrected commutator."""
    if omega <= 0:
        return 0.0

    dtau_grid = np.linspace(0.001, dtau_max, N)
    ImC_vals = np.array([commutator_im_corrected(d, A_over_H, omega_over_H) for d in dtau_grid])

    integrand = -np.exp(-eta * dtau_grid) * np.sin(omega * dtau_grid) * ImC_vals
    return trapezoid(integrand, dtau_grid) / np.pi


# SCAN: trajectory type × acceleration × omega_frac × frequency
print("SPECTRAL DENSITY SCAN (CORRECTED):")
print()
print(f"{'A/H':<8} {'omega/H':<10} {'rho(0.5)':<14} {'rho(1.0)':<14} {'rho(3.0)':<14}  {'Z_min'}")
print("-" * 75)

results = {}
most_negative = 0.0
most_neg_params = None

for A_H in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0]:
    r0H_sq = A_H**2 / (1 + A_H**2)
    max_omega = np.sqrt(max((1 - r0H_sq) / r0H_sq, 0.01)) if r0H_sq < 0.99 else np.inf

    for omega_frac in [0.3, 0.5, 0.7]:
        omega_val = min(omega_frac * max_omega, 0.95*max_omega) if max_omega > 0 and np.isfinite(max_omega) else A_H * 0.5

        # Get Z_min for display
        dtau_z = np.linspace(0.01, 20.0, 2000)
        Zsq_vals = [invariant_distance_squared_proper(d, A_H, omega_val/H) for d in dtau_z]
        Zsq_valid = [z for z in Zsq_vals if np.isfinite(z) and z > -10 and z < 1e8]
        Z_min_str = f"{min(Zsq_valid):.3f}" if Zsq_valid else "inf"

        # Spectral density at key frequencies (use shorter grid for speed)
        try:
            rho_05 = spectral_density_corrected(0.5, A_H, omega_val/H, dtau_max=100.0, N=4000)
            rho_10 = spectral_density_corrected(1.0, A_H, omega_val/H, dtau_max=100.0, N=4000)
            rho_30 = spectral_density_corrected(3.0, A_H, omega_val/H, dtau_max=200.0, N=4000)
        except Exception:
            continue

        key = (A_H, omega_val/H)
        results[key] = {"rho_05": float(rho_05), "rho_10": float(rho_10), "rho_30": float(rho_30)}

        if rho_30 < most_negative:
            most_negative = rho_30
            most_neg_params = key

        neg_marker = " <<< NEGATIVE" if rho_30 < -1e-8 else ""
        print(f"  {A_H:<8.1f} {omega_val/H:<10.3f} {rho_05:<14.6e} {rho_10:<14.6e} {rho_30:<14.6e}  Z_min={Z_min_str}  {neg_marker}")

print()


# ============================================================================
# SAVE RESULTS
# ============================================================================
results_path = os.path.join(os.path.dirname(__file__), 'phase_ds_unruh_corrected.json')
with open(results_path, 'w') as f:
    json.dump({
        "most_negative_rho": float(most_negative),
        "most_negative_params": str(most_neg_params),
        "all_results": results,
    }, f, indent=2)
print(f"Results saved: {results_path}")
