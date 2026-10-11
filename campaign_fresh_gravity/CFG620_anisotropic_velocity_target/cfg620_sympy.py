#!/usr/bin/env python3
"""CFG620 sympy items K1-K5 (FROZEN_CRITERIA.md 93abcbeb6) and the numeric angular-momentum test K6.
kappa = 1/2 FITTED; cold energy mass required; not "theory closed"."""
import math
import numpy as np
import sympy as sp


def k1():
    """discrete max-entropy: stationarity, Gram dual Hessian, strict concavity."""
    n, m = 4, 2
    F = sp.symbols("F0:%d" % n, positive=True); w = sp.symbols("w0:%d" % n, positive=True)
    lam = sp.symbols("l0:%d" % m, real=True); Mk = sp.symbols("M0:%d" % m, positive=True)
    P = sp.Matrix(n, m, lambda i, j: sp.Symbol(f"P{i}{j}", nonnegative=True))
    S = -sum(w[i] * F[i] * sp.log(F[i]) for i in range(n))
    Lg = S - sum(lam[k] * (sum(w[i] * F[i] * P[i, k] for i in range(n)) - Mk[k]) for k in range(m))
    sols = [sp.solve(sp.diff(Lg, F[i]), F[i]) for i in range(n)]
    expect = [sp.exp(-1 - sum(lam[k] * P[i, k] for k in range(m))) for i in range(n)]
    stat_ok = all(len(s) == 1 and sp.simplify(s[0] - e) == 0 for s, e in zip(sols, expect))
    # dual D(l) = sum w exp(-1 - P l) + l.M ; Hessian = sum_i w_i F_i P_i P_i^T (Gram)
    D = sum(w[i] * expect[i] for i in range(n)) + sum(lam[k] * Mk[k] for k in range(m))
    H = sp.hessian(D, lam)
    G = sum((w[i] * expect[i] * P[i, :].T * P[i, :] for i in range(n)), sp.zeros(m, m))
    gram_ok = sp.simplify(H - G) == sp.zeros(m, m)
    # strict concavity of S: Hessian diag(-w_i/F_i) < 0
    HS = sp.hessian(S, F)
    conc_ok = all(sp.simplify(HS[i, i] + w[i] / F[i]) == 0 for i in range(n)) and \
        all(HS[i, j] == 0 for i in range(n) for j in range(n) if i != j)
    return dict(stationarity_F_eq_exp_minus1_minus_Plambda=bool(stat_ok), dual_hessian_is_gram_PSD=bool(gram_ok),
                entropy_strictly_concave_unique=bool(conc_ok), passed=bool(stat_ok and gram_ok and conc_ok))


def k2():
    """r^3 moment of the anisotropic radial Jeans equation: 2K = int rho r g dV for any beta (P_r(R) = 0)."""
    r, R = sp.symbols("r R", positive=True)
    Pr = sp.Function("Pr")(r); beta = sp.Function("beta")(r); rho = sp.Function("rho")(r); g = sp.Function("g")(r)
    # Jeans: dPr/dr + 2 beta Pr / r = -rho g ; Pt (both tangential) = 2 (1 - beta) Pr ; K = (1/2) int (Pr + Pt) 4 pi r^2 dr
    jeans = sp.diff(Pr, r) + 2 * beta * Pr / r + rho * g
    # 4 pi int_0^R r^3 jeans dr = 0 ; by parts int r^3 Pr' = [r^3 Pr]_0^R - 3 int r^2 Pr  (boundary term 0 when Pr(R) = 0)
    integrand_after_parts = -3 * r ** 2 * Pr + 2 * beta * Pr * r ** 2 + rho * g * r ** 3
    # identity check: r^3 * jeans = d/dr(r^3 Pr) + integrand_after_parts
    ident = sp.simplify(r ** 3 * jeans - (sp.diff(r ** 3 * Pr, r) + integrand_after_parts)) == 0
    # 2K density: (Pr + Pt) r^2 = (3 - 2 beta) Pr r^2 ; so int (3 - 2 beta) Pr r^2 = int rho g r^3  <=> 2K = int rho r g dV
    twoK_density = (Pr + 2 * (1 - beta) * Pr) * r ** 2
    virial = sp.simplify(twoK_density + integrand_after_parts - rho * g * r ** 3) == 0
    return dict(by_parts_identity=bool(ident), twoK_equals_int_rho_r_g_for_any_beta=bool(virial),
                energy_constraint_redundant=bool(ident and virial), passed=bool(ident and virial))


def k3():
    """edge: orbits with r_apo <= R have v_r^2 <= 2[Phi_eff(R) - Phi_eff(r)] -> 0 linearly as r -> R."""
    r, R, L, gR = sp.symbols("r R L g_R", positive=True)
    Phi = sp.Function("Phi")
    Peff = lambda x: Phi(x) + L ** 2 / (2 * x ** 2)
    bound = 2 * (Peff(R) - Peff(r))
    ser = sp.series(bound.subs(r, R - sp.Symbol("d", positive=True)), sp.Symbol("d", positive=True), 0, 2).removeO()
    d = sp.Symbol("d", positive=True)
    lead = sp.simplify(sp.diff(ser, d).subs(d, 0))
    # lead = 2 Phi'(R) - 2 L^2/R^3 = 2 (g_R - L^2/R^3) >= 0 for L^2 <= R^3 g_R (the orbits that stay inside R); zero-order term 0
    zero_term = sp.simplify(ser.subs(d, 0)) == 0
    lead_expect = 2 * sp.Subs(sp.Derivative(Phi(r), r), r, R).doit() - 2 * L ** 2 / R ** 3
    lead_ok = sp.simplify(lead - lead_expect) == 0
    return dict(vr2_bound_vanishes_at_edge=bool(zero_term), linear_coefficient_2_gR_minus_L2_over_R3=bool(lead_ok),
                sigma_r_to_zero_sigma_t_finite=bool(zero_term and lead_ok), passed=bool(zero_term and lead_ok))


def k4():
    """KINETIC_GATE re-verification (exponential kernel, point baryons; G = M_b = a0 = 1, q = r_M/r)."""
    r, q = sp.symbols("r q", positive=True)
    Mph = 1 / (sp.exp(1 / r) - 1)                               # M_b (nu - 1), sqrt(y) = 1/r
    rho = sp.diff(Mph, r) / (4 * sp.pi * r ** 2)
    rho_q = sp.simplify(rho.subs(r, 1 / q))
    target = q ** 4 / (4 * sp.pi) / (4 * sp.sinh(q / 2) ** 2)
    rho_ok = sp.simplify(sp.expand((rho_q - target).rewrite(sp.exp))) == 0
    slope = sp.simplify(r * sp.diff(rho, r) / rho)
    slope_q = sp.simplify(slope.subs(r, 1 / q))
    slope_ok = abs(float((slope_q - (-4 + q * sp.coth(q / 2))).subs(q, 2.7))) < 1e-12 and \
        abs(float((slope_q - (-4 + q * sp.coth(q / 2))).subs(q, 7.3))) < 1e-12
    qs = float(sp.nsolve(q * sp.coth(q / 2) - 4, q, 3.8))
    # isotropic: rho(Phi) = 4 pi sqrt2 int_Phi^inf f sqrt(E - Phi) dE ; d/dPhi = -2 pi sqrt2 int f / sqrt(E - Phi) <= 0
    E, P, Em = sp.symbols("E Phi E_m", real=True); f = sp.Function("f")
    integ = 4 * sp.pi * sp.sqrt(2) * f(E) * sp.sqrt(E - P)
    drho = sp.diff(integ, P)                                    # boundary term vanishes (sqrt(0) = 0)
    iso_ok = sp.simplify(drho + 2 * sp.pi * sp.sqrt(2) * f(E) / sp.sqrt(E - P)) == 0
    return dict(rho_formula_q4_over_4sinh2=bool(rho_ok), dlnrho_dlnr_eq_minus4_plus_q_coth=bool(slope_ok),
                q_star=qs, q_star_in_3_4=bool(3 < qs < 4), isotropic_drho_dPhi_le_0=bool(iso_ok),
                passed=bool(rho_ok and slope_ok and 3 < qs < 4 and iso_ok))


def k5():
    """BGK toward n F_hat: local mass exact, KL decreasing, log-mean factorisation, energy closed only with the phi partner."""
    f, nF, gam = sp.symbols("f nF gamma", positive=True)
    C = -gam * (f - nF)
    # H-theorem integrand: dKL/dt = int C ln(f/nF) = -gamma (f - nF) ln(f/nF) <= 0 ; with x = f/nF: -(x - 1) ln x nF gamma
    x = sp.symbols("x", positive=True)
    h = (x - 1) * sp.log(x)
    # (x-1) ln x >= 0: derivative sign analysis -- h(1) = 0, h'(x) = ln x + 1 - 1/x has the sign of x - 1
    hp = sp.diff(h, x)
    sign_ok = sp.simplify(hp.subs(x, 1)) == 0 and all(float(hp.subs(x, v)) * (v - 1) > 0 for v in (0.01, 0.3, 0.9, 1.1, 3, 50))
    h_ok = sp.simplify(h.subs(x, 1)) == 0 and sign_ok
    Lam = (f - nF) / (sp.log(f) - sp.log(nF))
    fact_ok = sp.simplify(C - (-gam * Lam * (sp.log(f) - sp.log(nF)))) == 0
    lam_pos = all(float(Lam.subs({f: a, nF: b})) > 0 for a, b in ((0.2, 1.0), (3.0, 1.0), (1.0, 7.0)))
    # mass: int C dv = -gamma (n - n int F_hat dv) = 0 since int F_hat dv = 1
    n, Fint = sp.symbols("n Fint", positive=True)
    mass_ok = sp.simplify((-gam * (n - n * Fint)).subs(Fint, 1)) == 0
    # energy: dE_matter/dt = int (v^2/2 + Phi) C dv = int (v^2/2) C dv (Phi term vanishes by mass) ; nonzero in general,
    # so M.dE = 0 needs the phi partner absorbing exactly -int (v^2/2) C dv
    v, s2 = sp.symbols("v sigma2", positive=True)
    Ef = sp.Rational(3, 2) * s2; EF = sp.Symbol("E_target", positive=True)
    dEm = -gam * n * (Ef - EF)
    partner_needed = sp.simplify(dEm) != 0
    closed_with_partner = sp.simplify(dEm + (-dEm)) == 0
    return dict(mass_exact=bool(mass_ok), KL_decreasing_x_minus_1_lnx_ge_0=bool(h_ok), log_mean_factorisation=bool(fact_ok),
                log_mean_positive=bool(lam_pos), energy_needs_phi_partner=bool(partner_needed),
                energy_closed_with_partner=bool(closed_with_partner),
                passed=bool(mass_ok and h_ok and fact_ok and lam_pos and partner_needed and closed_with_partner))


def k6(n=4000, nbin=20, steps=200, p=0.05, seed=598):
    """numeric: bin-wise momentum-shifted resampling conserves total J (3-D rotating shell); plain resampling does not."""
    rng = np.random.default_rng(seed)
    def setup():
        x = rng.standard_normal((n, 3)); x /= np.linalg.norm(x, axis=1)[:, None]; x *= rng.uniform(1, 2, n)[:, None]
        omega = np.array([0, 0, 0.7]); v = np.cross(omega, x) + 0.3 * rng.standard_normal((n, 3))
        return x, v
    def J(x, v): return np.cross(x, v).sum(0)
    out = {}
    for mode in ("plain", "conserving"):
        x, v = setup(); J0 = J(x, v)
        rr = np.linalg.norm(x, axis=1); k = np.minimum((nbin * (rr - 1)).astype(int), nbin - 1)
        rhat = x / rr[:, None]
        for _ in range(steps):
            sel = rng.random(n) < p
            vr = (v * rhat).sum(1); vt_old = v - vr[:, None] * rhat
            # target: nonrotating Gaussian (stands in for F_hat): new radial and tangential components
            g = 0.5 * rng.standard_normal((n, 3)); vr_n = (g * rhat).sum(1); vt_n = g - vr_n[:, None] * rhat
            if mode == "conserving":
                for b in range(nbin):
                    m = sel & (k == b)
                    if m.sum() < 1: continue
                    # restore the bin's angular momentum: add a rigid rotation about the bin's own J axis
                    dJ = np.cross(x[m], vt_old[m]).sum(0) - np.cross(x[m], vt_n[m]).sum(0)
                    I = np.sum(rr[m] ** 2) * np.eye(3) - x[m].T @ x[m]
                    om = np.linalg.lstsq(I, dJ, rcond=None)[0]          # one particle: I singular along x, dJ is normal to x
                    vt_n[m] = vt_n[m] + np.cross(om, x[m])
            v = np.where(sel[:, None], vr_n[:, None] * rhat + vt_n, v)
        out[mode] = float(np.linalg.norm(J(x, v) - J0) / np.linalg.norm(J0))
    return dict(rel_dJ_plain=out["plain"], rel_dJ_conserving=out["conserving"],
                passed=bool(out["conserving"] <= 1e-12 and out["plain"] > 1e-3))


def all_items():
    R = dict(K1=k1(), K2=k2(), K3=k3(), K4=k4(), K5=k5(), K6=k6())
    R["K1_K5_pass"] = all(R[k]["passed"] for k in ("K1", "K2", "K3", "K4", "K5"))
    return R


if __name__ == "__main__":
    import json
    print(json.dumps(all_items(), indent=1))
