#!/usr/bin/env python3
"""significance_vs_z.py — traceability addendum (NOT part of the 2026-07-21 freeze).

Reproduces the z-dependence of the a0-decline significance quoted in
RUBIN_PREREG_2026.md Sec. 6.1 limitation 1 (and in the JCAP submission memo,
Attack 5): propagating the SAME DESI DR2 (+CMB+Pantheon+) w0-wa posterior
through the framework relation

    R(z) = a0(z)/a0(0) = sqrt( rho_DE(z)/rho_DE0 )
         = [ (1+z)^{3(1+w0+wa)} * exp(-3 wa z/(1+z)) ]^{1/2}

at reference redshifts z = 1, 2, 3, 10, and reporting the posterior
credibility of a decline (fraction of samples with R < 1, mapped to a
Gaussian sigma) — the same Bayesian-tail convention as the frozen
a0z_gate_estimator.py. Also runs the tight SN+CMB/BAO forecast covariance
(the Rubin FoM~500 scenario) for the "1.1 sigma at z=1 but 4.7 sigma at
z>=2" statement.

Expected output (frozen-doc values): 0.34σ (z=1), 1.7σ (z=2), 2.0σ (z=3),
2.4σ (z=10) for DESI-now; ~1.1σ (z=1), ~4.7σ (z>=2) for SN+CMB/BAO.

This script is a post-freeze traceability addendum: it changes no threshold,
band, or estimator, and it is deliberately NOT listed in FREEZE_HASHES.txt.
numpy/scipy only; exits 0.
"""
import sys
import numpy as np
from scipy.special import erfcinv

np.seterr(all="ignore")

SEED = 20260721
N = 400_000  # same draw count as the frozen estimator

# DESI DR2 + CMB + Pantheon+ (arXiv:2503.14738), the frozen baseline input
W0, SW0 = -0.838, 0.055
WA, SWA = -0.62, 0.22
RHO = -0.86

# Rubin SN + CMB/BAO forecast covariance (FoM ~500), same means; the frozen
# scripts use rho = -0.90 for the projected Rubin rows
SW0_F, SWA_F, RHO_F = 0.020, 0.08, -0.90


def draw(sw0, swa, rho, rng):
    cov = np.array([[sw0**2, rho * sw0 * swa], [rho * sw0 * swa, swa**2]])
    L = np.linalg.cholesky(cov)
    u = rng.standard_normal((2, N))
    w0, wa = (np.array([[W0], [WA]]) + L @ u)
    return w0, wa


def R_of_z(z, w0, wa):
    lnrho = 3.0 * (1.0 + w0 + wa) * np.log1p(z) - 3.0 * wa * z / (1.0 + z)
    return np.exp(0.5 * lnrho)


def decline_sigma(R):
    # IDENTICAL convention to the frozen a0z_gate_estimator.py: posterior
    # tail mapped to a Gaussian sigma, with the not-decline fraction floored
    # at 0.5/N (which caps the reportable significance at ~4.7 sigma for
    # N = 4e5 — the origin of the prereg's "4.6-4.7 sigma" MC range).
    frac_notdecline = max(np.mean(R >= 1.0), 0.5 / N)
    return np.sqrt(2) * erfcinv(2 * frac_notdecline)


def main():
    rng = np.random.default_rng(SEED)
    zs = [1.0, 2.0, 3.0, 10.0]
    expected = {1.0: 0.34, 2.0: 1.7, 3.0: 2.0, 10.0: 2.4}

    print("DESI DR2 (+CMB+Pantheon+) posterior propagated to R(z):")
    w0, wa = draw(SW0, SWA, RHO, rng)
    ok = True
    for z in zs:
        R = R_of_z(z, w0, wa)
        med = np.median(R)
        lo, hi = np.percentile(R, [16, 84])
        sig = decline_sigma(R)
        tol = 0.1 if z < 10 else 0.15
        match = abs(sig - expected[z]) < tol
        ok &= match
        print(f"  z={z:>4.1f}: R = {med:.3f} [{lo:.3f}, {hi:.3f}]  "
              f"decline {sig:.2f} sigma  (doc: {expected[z]} sigma) "
              f"{'OK' if match else 'MISMATCH'}")

    print("\nRubin SN + CMB/BAO forecast covariance (FoM ~500), same means:")
    w0f, waf = draw(SW0_F, SWA_F, RHO_F, rng)
    exp_f = {1.0: 1.1, 2.0: 4.7, 3.0: 4.7}
    for z in [1.0, 2.0, 3.0]:
        R = R_of_z(z, w0f, waf)
        sig = decline_sigma(R)
        match = abs(sig - exp_f[z]) < 0.2
        ok &= match
        print(f"  z={z:>4.1f}: R = {np.median(R):.3f}  decline {sig:.2f} sigma  "
              f"(doc: {exp_f[z]} sigma) {'OK' if match else 'MISMATCH'}")

    if not ok:
        print("\nFAIL: at least one significance does not match the frozen doc.")
        return 1
    print("\nPASS: all z-dependent significances reproduce the frozen-doc values.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
