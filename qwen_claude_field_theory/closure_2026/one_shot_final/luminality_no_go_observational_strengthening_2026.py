#!/usr/bin/env python3
r"""Finite-shell observational strengthening of the curvature-QUMOND no-go.

The exact theorem is analytic: on a regular spherical MOND branch,

    lambda_r = -(a0/c^2) y exp(-y),      y(1-exp(-y)) = g_N/a0,

whereas the tensor principal symbol gives ``c_T^2=1/(1-2 lambda)``.
Consequently exact luminality would require lambda=0 and lambda_r=0.

This script asks a narrower numerical question: how much does the action-forced
profile vary across one finite MOND shell? The variation is independent of the
additive integration constant. At least one endpoint must have
``|lambda| >= |Delta lambda|/2`` for every choice of that constant. The script
solves the implicit MOND relation rather than identifying ``y`` with
``g_N/a0``. No assumption about lambda at spatial infinity is made.
"""

import sys

import numpy as np

G = 6.674e-11
c = 2.998e8
a0 = 9.36e-11
Msun = 1.989e30
kpc = 3.086e19
GW_BOUND = 7e-16
DELAY_BOUND = 1.7


def solve_mond_y(x):
    """Solve y*(1-exp(-y))=x for nonnegative scalar/array x by Newton iteration."""
    x = np.asarray(x, dtype=float)
    if np.any(x < 0):
        raise ValueError("g_N/a0 must be nonnegative")
    y = np.where(x == 0.0, 0.0, np.maximum(np.sqrt(x), x))
    for _ in range(80):
        mu = -np.expm1(-y)
        derivative = mu + y * np.exp(-y)
        step = np.divide(y * mu - x, derivative, out=np.zeros_like(y), where=derivative > 0)
        updated = np.maximum(0.0, y - step)
        if np.max(np.abs(updated - y) / np.maximum(1.0, updated)) < 2e-15:
            y = updated
            break
        y = updated
    residual = y * (-np.expm1(-y)) - x
    if np.max(np.abs(residual) / np.maximum(1.0, x)) > 2e-12:
        raise RuntimeError("Newton iteration did not solve the implicit MOND law")
    return y


def lam_profile(x, rs, mond=True):
    """Return y and lambda with lambda(rs[-1])=0 on the supplied finite shell."""
    x = np.asarray(x, dtype=float)
    rs = np.asarray(rs, dtype=float)
    if x.shape != rs.shape or x.ndim != 1 or len(x) < 2:
        raise ValueError("x and rs must be equal-length one-dimensional arrays")
    if not np.all(np.diff(rs) > 0):
        raise ValueError("rs must be strictly increasing")
    y = solve_mond_y(x) if mond else x.copy()
    source = y * np.exp(-y) if mond else np.zeros_like(y)
    segment = 0.5 * (source[:-1] + source[1:]) * np.diff(rs)
    tail_integral = np.concatenate((np.cumsum(segment[::-1])[::-1], [0.0]))
    # lambda_r=-(a0/c^2) source, hence lambda is positive inward when the
    # finite outer matching value is zero.
    lam = (a0 / c**2) * tail_integral
    return y, lam


def dcT(lam):
    """Return |c_T/c-1| from c_T^2=1/(1-2 lambda)."""
    return np.abs(1.0 / np.sqrt(1.0 - 2.0 * lam) - 1.0)


def constant_independent_speed_bound(delta_lambda):
    """Lower-bound the larger endpoint speed shift for any additive constant."""
    delta = float(abs(delta_lambda))
    if not 0.0 <= delta < 1.0:
        raise ValueError("finite-shell |Delta lambda| must be below one")
    return float(min(dcT(delta / 2.0), dcT(-delta / 2.0)))


def run_audit():
    checks = []

    def check(name, ok, detail=""):
        checks.append(bool(ok))
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

    print("=== Finite-shell observational strengthening ===")
    worst_over = 0.0
    for name, mass in [
        ("MW-like 6e10 Msun", 6e10 * Msun),
        ("dwarf 1e9 Msun", 1e9 * Msun),
        ("giant 3e11 Msun", 3e11 * Msun),
    ]:
        r_mond = np.sqrt(G * mass / a0)
        rs = np.linspace(r_mond, 3.0 * r_mond, 20001)
        x = G * mass / (a0 * rs**2)
        y, lam = lam_profile(x, rs)
        equation_error = np.max(np.abs(y * (-np.expm1(-y)) - x))
        variation = float(lam[0] - lam[-1])
        speed_shift = constant_independent_speed_bound(variation)
        over = speed_shift / GW_BOUND
        worst_over = max(worst_over, over)
        scale = np.sqrt(G * mass * a0) / c**2
        print(
            f"{name}: r_M={r_mond/kpc:.2f} kpc, y(r_M)={y[0]:.6f}, "
            f"Delta lambda={variation:.3e}, minimax |c_T/c-1|>={speed_shift:.3e}, "
            f"{over:.2e}x the bound"
        )
        check(f"{name}: implicit MOND equation solved", equation_error < 2e-13, f"max residual {equation_error:.1e}")
        check(f"{name}: finite-shell lambda variation is order v_flat^2/c^2", 0.05 < lam[0] / scale < 3.0, f"ratio {lam[0]/scale:.3f}")
        check(f"{name}: every additive constant leaves an endpoint >1e6 over bound", over > 1e6, f"{over:.2e}x")

    mass = 6e10 * Msun
    r_mond = np.sqrt(G * mass / a0)
    rs = np.linspace(r_mond, 3.0 * r_mond, 20001)
    x = G * mass / (a0 * rs**2)
    _, lam = lam_profile(x, rs)
    delay = np.trapz(dcT(lam), rs) / c
    print(f"MW representative outer-luminal matching delay: {delay:.3e} s ({delay/DELAY_BOUND:.2e}x 1.7 s)")
    check("outer-luminal matching delay exceeds 1.7 s by >1e4", delay / DELAY_BOUND > 1e4)

    _, lam_gr = lam_profile(x, rs, mond=False)
    check("mutation control mu=1: lambda profile and speed shift vanish", np.max(np.abs(lam_gr)) == 0.0 and np.max(dcT(lam_gr)) == 0.0)

    print(f"Checks: {sum(checks)}/{len(checks)}")
    print(
        "VERDICT: every additive lambda constant leaves at least one endpoint above the bound; "
        f"the largest sampled lower bound is {worst_over:.1e}x the stated speed bound."
    )
    print("This strengthens, but is not needed for, the exact analytic contradiction.")
    return all(checks)


if __name__ == "__main__":
    sys.exit(0 if run_audit() else 1)
