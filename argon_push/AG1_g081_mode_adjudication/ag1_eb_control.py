#!/usr/bin/env python3
"""AG1 C6 — Ebert-Bonnor control: the SAME primitive-equation linearization machinery
that adjudicates G081 (ag1_adjudicate.py part C0), applied to the NON-SINGULAR truncated
isothermal sphere, must reproduce the classical instability threshold (literature control
targets, typed here per FROZEN_CRITERIA.md C6 allowance): xi_crit ~ 6.451, contrast
rho_c/rho_edge ~ 14.04 (Ebert 1955 / Bonnor 1956 / Antonov 1962).

General machinery (derived in AG1 C0, valid for any smooth barotropic background):
    q = r^2 rho0 xi
    sigma^2 q'' + (Phi0' - 2 sigma^2/r) q' + (4 pi G rho0 + w^2) q = 0
    (used: perturbed enclosed mass m1 = -4 pi q exactly, for regular center;
     phi1' = -4 pi G rho0 xi;  delta_rho = -q'/r^2)
    surface BC (delta P_L = 0):  q'(R) = q(R) * (d ln rho0/dr)|_R
    regular center: q ~ x^3.

Dimensionless isothermal form (r = r0 x, r0 = sigma/sqrt(4 pi G rho_c), rho0 = rho_c e^{-psi},
psi'' + (2/x) psi' = e^{-psi}, Phi0' = sigma^2 psi'/r0, omega~^2 = w^2 r0^2/sigma^2):

    q'' + (psi' - 2/x) q' + (e^{-psi} + omega~^2) q = 0        [FULL]
    q'' - (2/x) q' + (e^{-psi} + omega~^2) q = 0               [M3: -delta_rho*grad(Phi0) DELETED]

The term DELETED in M3 is exactly the term G081 omitted (psi' q').

C6 (pre-registered tolerance): xi_crit in [6.43, 6.47] AND contrast in [13.99, 14.09]
at the omega~^2 = 0 marginal point; plus stability-direction check: lowest eigenvalue
omega~_0^2 > 0 at xi_R = 5.5 and < 0 at xi_R = 8.0.
M3 (mutation, must fail as designed): with psi' q' deleted, the marginal point must NOT
land in the tolerance windows (else the control is insensitive to the adjudicated term
and the adjudication is demoted to SUSPECT).

House rules: honest FAILs preserved; exit 0 only on real passes; results JSON on disk.
"""
import json
import math
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))

X0 = 1e-6          # series start
XMAX = 14.0

# literature control targets (typed per freeze; NOT used anywhere else)
XI_CRIT_LIT = 6.451
CONTRAST_LIT = 14.04
XI_TOL = (6.43, 6.47)
CHI_TOL = (13.99, 14.09)


def integrate_background_and_mode(full_term=True, wt2=0.0):
    """Joint integration: y = [psi, psi', q, q'] from X0 to XMAX (dense output)."""

    def rhs(x, y):
        psi, dpsi, q, dq = y
        d2psi = math.exp(-psi) - 2.0 * dpsi / x
        coef = (dpsi - 2.0 / x) if full_term else (-2.0 / x)
        d2q = -coef * dq - (math.exp(-psi) + wt2) * q
        return [dpsi, d2psi, dq, d2q]

    # series ICs: psi ~ x^2/6 - ... ; q ~ x^3 (normalization free)
    y0 = [X0**2 / 6.0, X0 / 3.0, X0**3, 3.0 * X0**2]
    sol = solve_ivp(rhs, (X0, XMAX), y0, method="DOP853", rtol=1e-12, atol=1e-14,
                    dense_output=True)
    if not sol.success:
        raise RuntimeError("background/mode integration failed: " + sol.message)
    return sol


def surface_residual(sol, x_R):
    psi, dpsi, q, dq = sol.sol(x_R)
    return dq + dpsi * q        # delta P_L = 0  <=>  q' + psi' q = 0 at the truncation


def find_critical(full_term=True):
    sol = integrate_background_and_mode(full_term=full_term, wt2=0.0)
    xs = np.linspace(2.0, 12.0, 2001)
    F = np.array([surface_residual(sol, x) for x in xs])
    # normalize the scan (q grows; sign structure is what matters)
    signs = np.sign(F)
    idx = np.where(np.diff(signs) != 0)[0]
    roots = []
    for i in idx:
        try:
            xr = None
            from scipy.optimize import brentq
            xr = brentq(lambda x: surface_residual(sol, x), xs[i], xs[i + 1], xtol=1e-12, rtol=1e-13)
            roots.append(xr)
        except Exception:
            pass
    if not roots:
        return None, None, sol, []
    # the classical critical point is the FIRST marginal truncation
    x_crit = roots[0]
    psi_R = sol.sol(x_crit)[0]
    return x_crit, math.exp(psi_R), sol, roots


def lowest_eigenvalue(sol_bg, x_R, lam_lo=-2.0, lam_hi=2.0, n_scan=401):
    """Lowest omega~^2 of the FULL machinery on [X0, x_R] by DIRECT residual scan:
    R(lam) = q'(x_R) + psi'(x_R) q(x_R) with q the regular solution at lam; lowest root.
    NOTE: Sturm zero-counting is INVALID here — the surface BC is Robin (delta P_L = 0),
    not Dirichlet, and the lam=0 solution's first zero can lie OUTSIDE the domain
    (measured: x_z ~ 8.99 for the critical-neighborhood solution). The residual scan is
    the eigenvalue definition itself."""

    psiR, dpsiR = sol_bg.sol(x_R)[:2]

    def R(lam):
        def rhs(x, y):
            psi, dpsi, q, dq = y
            d2psi = math.exp(-psi) - 2.0 * dpsi / x
            d2q = -(dpsi - 2.0 / x) * dq - (math.exp(-psi) + lam) * q
            return [dpsi, d2psi, dq, d2q]
        y0 = [X0**2 / 6.0, X0 / 3.0, X0**3, 3.0 * X0**2]
        s = solve_ivp(rhs, (X0, x_R), y0, method="DOP853", rtol=1e-12, atol=1e-14,
                      dense_output=True)
        q, dq = s.sol(x_R)[2:]
        return dq + dpsiR * q

    from scipy.optimize import brentq
    lams = np.linspace(lam_lo, lam_hi, n_scan)
    Rs = np.array([R(l) for l in lams])
    idx = np.where(np.diff(np.sign(Rs)) != 0)[0]
    if len(idx) == 0:
        return float("nan")
    return brentq(R, lams[idx[0]], lams[idx[0] + 1], xtol=1e-12)


def turning_point(sol_bg):
    """C6b corroboration: M~(xi) = xi^2 psi'(xi) e^{-psi/2} (fixed P_ext, c_s) peaks at the
    critical truncation (turning-point method, independent of the pulsation machinery)."""
    xs = np.arange(5.5, 7.5, 0.005)
    Ms = []
    for x in xs:
        psi, dpsi = sol_bg.sol(x)[:2]
        Ms.append(x**2 * dpsi * math.exp(-psi / 2))
    Ms = np.array(Ms)
    i = int(np.argmax(Ms))
    return float(xs[i]), float(Ms[i])


def main():
    print("=" * 96)
    print("AG1 C6 — Ebert-Bonnor control (machinery anchor) + M3 mutation")
    print(f"literature control targets (typed per freeze): xi_crit={XI_CRIT_LIT}, contrast={CONTRAST_LIT}")
    print(f"pre-registered windows: xi in {XI_TOL}, contrast in {CHI_TOL}")
    print("=" * 96)

    x_crit, chi, sol, roots = find_critical(full_term=True)
    print(f"\nFULL machinery (with -delta_rho*grad(Phi0) = +psi' q'):")
    print(f"  marginal (omega~^2=0) truncations found on [2,12]: {[round(r,6) for r in roots]}")
    ok_xi = x_crit is not None and XI_TOL[0] <= x_crit <= XI_TOL[1]
    ok_chi = chi is not None and CHI_TOL[0] <= chi <= CHI_TOL[1]
    print(f"  xi_crit  = {x_crit}   (window {XI_TOL})   -> {'PASS' if ok_xi else 'FAIL'}")
    print(f"  contrast = {chi}   (window {CHI_TOL}) -> {'PASS' if ok_chi else 'FAIL'}")
    if x_crit is not None and chi is not None:
        print(f"  deviations from literature values: d xi = {x_crit-XI_CRIT_LIT:+.4f}, d contrast = {chi-CONTRAST_LIT:+.4f}")

    # stability direction checks (direct residual scan; n_unst no longer applicable)
    w55 = lowest_eigenvalue(sol, 5.5)
    w80 = lowest_eigenvalue(sol, 8.0)
    ok_dir = (w55 > 0) and (w80 < 0)
    print(f"  direction: omega~_0^2(xi_R=5.5) = {w55:+.6f} (expect > 0);  "
          f"omega~_0^2(xi_R=8.0) = {w80:+.6f} (expect < 0) -> {'PASS' if ok_dir else 'FAIL'}")

    # C6b corroboration: turning-point method (independent of pulsation machinery)
    x_turn, M_turn = turning_point(sol)
    ok_turn = XI_TOL[0] <= x_turn <= XI_TOL[1]
    print(f"  turning point (C6b): M~(xi) = xi^2 psi' e^(-psi/2) peaks at xi = {x_turn:.4f} "
          f"(window {XI_TOL}) -> {'PASS' if ok_turn else 'FAIL'}")

    # M3 mutation: delete the psi' q' term (exactly G081's omission)
    x_crit_m, chi_m, sol_m, roots_m = find_critical(full_term=False)
    print(f"\nM3 mutation (term DELETED, i.e., G081's linearization):")
    print(f"  marginal truncations found on [2,12]: {[round(r,6) for r in roots_m]}")
    if x_crit_m is None:
        m3_ok = True
        print("  NO marginal point on [2,12] -> the deleted-term machinery does not reproduce the")
        print("  classical instability threshold at all. Mutation fails as designed: PASS")
    else:
        in_window = (XI_TOL[0] <= x_crit_m <= XI_TOL[1]) and (CHI_TOL[0] <= chi_m <= CHI_TOL[1])
        m3_ok = not in_window
        print(f"  xi_crit(M3) = {x_crit_m:.6f}, contrast(M3) = {chi_m:.6f}; inside C6 windows: {in_window}")
        print(f"  -> mutation {'fails as designed: PASS' if m3_ok else 'LANDS IN WINDOW: FAIL — control insensitive to the adjudicated term; adjudication DEMOTED TO SUSPECT'}")

    c6_pass = ok_xi and ok_chi and ok_dir and ok_turn
    print("\n" + "=" * 96)
    if c6_pass:
        print(f"C6 PASS: the primitive-equation machinery reproduces the Ebert-Bonnor/Antonov critical point "
              f"(xi={x_crit:.4f}, contrast={chi:.4f}) and the stability direction — the AG1 spectral thresholds "
              f"inherit this anchor.")
    else:
        print("C6 CONTROL-NOT-CONVERGED / FAIL (loud, per freeze): the adjudication's derivation discrepancy "
              "(C0-C3, exact algebra) stands regardless, but AG1's spectral THRESHOLDS are demoted to CONDITIONAL.")
    print(f"AG1_EB COMPLETE: C6={'PASS' if c6_pass else 'FAIL'}, M3={'as-designed' if m3_ok else 'SENSITIVITY-FAIL'}")

    out = dict(
        lane="AG1_g081_mode_adjudication/C6_EB_control",
        literature_targets=dict(xi_crit=XI_CRIT_LIT, contrast=CONTRAST_LIT),
        windows=dict(xi=XI_TOL, chi=CHI_TOL),
        full=dict(xi_crit=x_crit, contrast=chi, marginal_roots=roots,
                  omega0_2_at_5_5=w55, omega0_2_at_8=w80,
                  turning_point_xi=x_turn, turning_point_M=M_turn),
        m3=dict(xi_crit=x_crit_m, contrast=chi_m, marginal_roots=roots_m, as_designed=m3_ok),
        C6_pass=bool(c6_pass),
        M3_ok=bool(m3_ok),
    )
    with open(os.path.join(HERE, "ag1_eb_control_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("results -> ag1_eb_control_results.json")
    return 0 if (c6_pass and m3_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
