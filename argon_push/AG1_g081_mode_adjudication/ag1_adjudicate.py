#!/usr/bin/env python3
"""AG1 — adjudication of the G081 mode-equation discrepancy flagged (unadjudicated) in
GF2_closure_half/README.md boundary 4.

THE FLAG (GF2 README): "while preparing this lane, a re-derivation of the G081
linearized momentum equation could not reproduce its [SELF-CONSISTENT] mode equation
(G081's form omits the standard -delta_rho*grad(Phi0) force term). ... The point is
flagged for the audit registry."

G081 AS COMMITTED (deepseek_push/G081_equilibrium_stability.py L31-36):
    Euler (linear)  : -w^2 rho0 xi = -rho0 phi1' + sigma^2 (rho0 xi')'
    Poisson (self)  : (r^2 phi1')'/r^2 = 4 pi G delta_rho_e  =>  phi1' = -4 pi G A xi/r^2
    => [SELF-CONSISTENT]  sigma^2 xi'' - (2 sigma^2/r) xi' + (2 sigma^2/r^2 - w^2) xi = 0
and its verdicts (G081_results.json): double homology zero mode {r, r^2}, "omega^2 = 0
exact (marginal), cap-invariant", "neutral continuum", "well-posed linear relaxation".

WHAT THIS LANE DOES: re-derives the linearization from the four primitive equations
(continuity, Euler with ALL force terms, Poisson, isothermal EOS) symbolically; pinpoints
the discrepancy (MUTATE M2 must reproduce G081's form under the omission); computes the
corrected spectral structure (exact closed forms + independent numerics); tables the
stability verdict at G081's own registered constants (read at runtime); demonstrates the
r->0 ill-posedness; and states consequences for G081 V2/V3, GF2's P1 boundary, and
G111 reading-(c). FROZEN_CRITERIA.md (committed before any run) governs PASS/FAIL.

Sign convention: xi ~ exp(-i w t), so w^2 > 0 = stable oscillation, w^2 < 0 = growth.
G081's printed ODE corresponds to xi ~ exp(w t) (w^2_G081 = -w^2_here); zero-mode and
drift statements are convention-independent. Documented in C1.

House rules: append-only; no file outside argon_push/ is modified; honest FAILs
preserved; exit 0 only on real passes.
"""
import json
import math
import os
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
G081_JSON = os.path.join(REPO, "deepseek_push", "G081_results.json")

MUTATE = os.environ.get("MUTATE", "0") == "1"

KPC = 3.0856775814913673e19  # m

checks = []


def record(name, ok, detail):
    checks.append(dict(name=name, pass_=bool(ok), detail=str(detail)))
    print(("PASS" if ok else "FAIL") + "  " + name)
    print("      " + str(detail))


def load_constants():
    with open(G081_JSON) as f:
        g = json.load(f)
    K = g["constants"]
    return g, K


# ----------------------------------------------------------------------------
# C0 — first-principles symbolic linearization (corrected + omission)
# ----------------------------------------------------------------------------
def part_C0_C1_C2_C3():
    r, A, G, C, sigma2, w2, lam = sp.symbols("r A G C sigma2 w2 lam", positive=True)
    eps = sp.symbols("eps")
    xi = sp.Function("xi")
    xif = xi(r)
    Xi0, Xi1, Xi2 = sp.symbols("Xi0 Xi1 Xi2")
    d1 = sp.Derivative(xif, r)
    d2 = sp.Derivative(xif, (r, 2))

    rho0 = A / r**2
    Phi0p = C / r                      # equilibrium field of the log branch
    # continuity: delta_rho = -(1/r^2) d(r^2 rho0 xi)/dr
    delta_rho = -sp.diff(r**2 * rho0 * xif, r) / r**2
    delta_rho_s = sp.simplify(delta_rho)          # = -rho0 xi' for A/r^2
    delta_P = sigma2 * delta_rho                  # isothermal closure
    # Poisson, inner mass frozen (phi1' = -4 pi G A xi / r^2 = -C xi/r^2 with C = 4 pi G A)
    phi1p = -C * xif / r**2

    # full Euler, all terms on one side:  -w^2 rho0 xi + rho0 phi1' + delta_rho Phi0' + (delta_P)' = 0
    euler_full = -w2 * rho0 * xif + rho0 * phi1p + delta_rho * Phi0p + sp.diff(delta_P, r)
    # omission variant (G081 L31): drop delta_rho * Phi0'
    euler_omit = -w2 * rho0 * xif + rho0 * phi1p + sp.diff(delta_P, r)

    def coeffs(expr):
        e = expr.subs({xif: Xi0, d1: Xi1, d2: Xi2})
        e = sp.expand(sp.simplify(e / rho0))
        c2 = sp.simplify(e.coeff(Xi2, 1))
        c1 = sp.simplify(e.coeff(Xi1, 1))
        c0 = sp.simplify(e.coeff(Xi0, 1))
        const = sp.simplify(e.subs({Xi0: 0, Xi1: 0, Xi2: 0}))
        return c2, c1, c0, const

    # sanity: delta_rho = -rho0 xi'
    dr_check = sp.simplify(delta_rho_s + rho0 * d1) == 0

    f2, f1, f0, fc = coeffs(euler_full)
    # predicted: euler_full/rho0 = -[sigma2 xi'' + (C-2 sigma2) xi'/r + (C/r^2 + w2) xi]
    pred2 = -sigma2
    pred1 = -(C - 2 * sigma2) / r
    pred0 = -(C / r**2 + w2)
    okC0 = (
        dr_check
        and sp.simplify(f2 - pred2) == 0
        and sp.simplify(f1 - pred1) == 0
        and sp.simplify(f0 - pred0) == 0
        and fc == 0
    )
    record(
        "C0 first-principles linearization -> (E-corr)",
        okC0,
        f"delta_rho=-rho0*xi': {dr_check}; coeffs/rho0 of full Euler: xi''={sp.simplify(f2)}, "
        f"xi'={sp.simplify(f1)}, xi={sp.simplify(f0)}, const={fc}  "
        f"(predicted -sigma2, -(C-2sigma2)/r, -(C/r^2+w2), 0)",
    )

    # closure reduction sigma^2 = C/2  =>  xi'' + (w^2/sigma^2 + 2/r^2) xi = 0
    f2c = sp.simplify(f2.subs(sigma2, C / 2))
    f1c = sp.simplify(f1.subs(sigma2, C / 2))
    f0c = sp.simplify(f0.subs(sigma2, C / 2))
    record(
        "C0b drift cancels EXACTLY at sigma^2=C/2 (closure)",
        bool(f1c == 0 and f2c == -C / 2 and sp.simplify(f0c + (C / r**2 + w2)) == 0),
        f"xi' coefficient at closure: {f1c} (identically 0: the omitted +C/r pairs with the "
        f"pressure-curvature -2sigma^2/r); xi'' coefficient: {f2c}; xi coefficient: {f0c} = -(C/r^2+w2)",
    )

    # C0c — GF2 P1 base identities (the kappa chain's algebraic base, untouched by the mode error)
    lap = sp.simplify(sp.diff(r**2 * sp.diff(C * sp.log(r), r), r) / r**2)   # 3-D radial Laplacian
    rho_poisson = sp.simplify(C / (4 * sp.pi * G * r**2))
    hydro = sp.simplify((sp.diff((C / 2) * rho0, r) + rho0 * Phi0p).subs(C, 4 * sp.pi * G * A))
    okP1 = lap == C / r**2 and sp.simplify(rho_poisson.subs(C, 4 * sp.pi * G * A) - rho0) == 0 and hydro == 0
    record(
        "C0c GF2 P1 base re-verified (Laplacian(C ln r)=C/r^2; rho0=C/(4 pi G r^2); hydrostatic residual=0 at sigma^2=C/2)",
        okP1,
        f"lap={lap}; rho0={sp.simplify(rho_poisson.subs(C, 4*sp.pi*G*A))}; hydro residual={hydro}",
    )

    # C1/M2 — the SAME machinery with delta_rho*Phi0' deleted reproduces G081 L36
    o2, o1, o0, oc = coeffs(euler_omit)
    # euler_omit/rho0 = -[sigma2 xi'' - 2 sigma2 xi'/r + (C/r^2 + w2) xi]
    okC1_der = (
        sp.simplify(o2 + sigma2) == 0
        and sp.simplify(o1 - 2 * sigma2 / r) == 0
        and sp.simplify(o0 + (C / r**2 + w2)) == 0
        and oc == 0
    )
    # G081 L36 as printed:  sigma2 xi'' - (2 sigma2/r) xi' + (2 sigma2/r^2 - w2G) xi = 0,
    # in ITS convention xi ~ exp(wG t)  <=>  w2G = -w2 (mine is exp(-i w t)).
    # Multiply my omission polynomial by -1 and compare coefficient-by-coefficient at closure.
    w2G = sp.symbols("w2G")
    mine = sp.expand((-1) * (o2 * Xi2 + o1 * Xi1 + o0 * Xi0)).subs(sigma2, C / 2)
    theirs = sp.expand((sigma2 * Xi2 - (2 * sigma2 / r) * Xi1 + (2 * sigma2 / r**2 - w2G) * Xi0)
                       .subs({sigma2: C / 2, w2G: -w2}))
    g081_match = sp.simplify(sp.expand(mine - theirs)) == 0
    # zero modes of the omitted equation at w2=0
    om_ode = o2 * Xi2 + o1 * Xi1 + o0 * Xi0
    om0 = sp.simplify(om_ode.subs({w2: 0, sigma2: C / 2}))
    zm_r = sp.simplify(om0.subs({Xi0: r, Xi1: 1, Xi2: 0}))
    zm_r2 = sp.simplify(om0.subs({Xi0: r**2, Xi1: 2 * r, Xi2: 2}))
    okC1 = okC1_der and g081_match and zm_r == 0 and zm_r2 == 0
    record(
        "C1 omission pinpointed (MUTATE M2): term-deleted machinery reproduces G081 L36 + its {r, r^2} zero modes",
        okC1,
        f"deleted-term coefficients match sigma2*xi''-(2sigma2/r)xi'+(C/r^2+w2)xi exactly: {okC1_der}; "
        f"at closure, under the time-convention relabel w^2_G081 = -w^2_here (G081 prints the exp(w t) form), "
        f"coefficient-by-coefficient identical to G081 L36: {g081_match}; zero-mode residuals at w=0: "
        f"xi=r -> {zm_r}, xi=r^2 -> {zm_r2}",
    )

    # C2 — zero modes under the CORRECTED equation at closure
    corr_ode = (f2 * Xi2 + f1 * Xi1 + f0 * Xi0).subs(sigma2, C / 2)
    corr0 = sp.simplify(-corr_ode.subs(w2, 0) / (C / 2))  # = xi'' + 2 xi/r^2
    cr = sp.simplify(corr0.subs({Xi0: r, Xi1: 1, Xi2: 0}))
    cr2 = sp.simplify(corr0.subs({Xi0: r**2, Xi1: 2 * r, Xi2: 2}))
    okC2 = cr != 0 and cr2 != 0 and sp.simplify(cr - 2 / r) == 0 and cr2 == 4
    record(
        "C2 homology zero modes KILLED by the corrected equation",
        okC2,
        f"at w=0, sigma^2=C/2: residual(xi=r) = {cr} (!= 0), residual(xi=r^2) = {cr2} (!= 0). "
        f"G081's double homology zero mode does not survive the -delta_rho*grad(Phi0) term.",
    )

    # M1 — no real constant w^2 makes xi=r a solution of (E-corr*)
    # (solve on a free real symbol: the module-level w2 carries positive=True and would
    #  filter the formally negative, r-dependent solution)
    w2f = sp.symbols("w2f", real=True)
    resid_r = sp.simplify(corr_ode.subs({Xi0: r, Xi1: 1, Xi2: 0, w2: w2f}))
    sol_w2 = sp.solve(sp.Eq(resid_r, 0), w2f)
    okM1 = len(sol_w2) == 1 and sol_w2[0].has(r)  # w^2 = -C/r^2: r-dependent => no global mode
    record(
        "M1 (mutation, must fail as designed): 'xi=r solves (E-corr*) at some real constant w^2'",
        okM1,
        f"formal solution w^2 = {sol_w2} — r-dependent, so no constant-w^2 mode exists. Mutation fails as designed: {okM1}",
    )

    # C3 — homology premise false at fixed sigma^2
    eps = sp.symbols("eps")
    rho_lam = (A / (1 + eps) ** 2 / r**2)
    C_lam = 4 * sp.pi * G * A / (1 + eps) ** 2
    hydro_lam = sp.simplify(sp.diff((2 * sp.pi * G * A) * rho_lam, r) + rho_lam * C_lam / r)
    hydro_lam_series = hydro_lam.series(eps, 0, 2).removeO()
    per_rho = sp.simplify(hydro_lam / rho_lam)
    per_rho_series = per_rho.series(eps, 0, 2).removeO()
    okC3 = hydro_lam.subs(eps, 0) == 0 and hydro_lam_series != 0 and sp.simplify(
        per_rho_series - (-2 * eps * (4 * sp.pi * G * A) / r)) == 0
    record(
        "C3 'homology of the isothermal family at fixed sigma^2' (G081 L177) is not a family of equilibria",
        okC3,
        f"hydrostatic residual of A/(1+eps)^2 r^-2 at sigma^2=C/2 fixed (C=4 pi G A substituted): "
        f"first order = {sp.simplify(sp.expand(hydro_lam_series))}; per unit density = {per_rho_series} "
        f"(frozen prediction: -2 eps C/r). True homology scales (A, C, sigma^2) together; at fixed "
        f"sigma^2 the equilibrium is unique (A itself).",
    )

    return dict(okC0=okC0, okC1=okC1, okC2=okC2, okC3=okC3, okM1=okM1)


# ----------------------------------------------------------------------------
# C4 — exact spectral structure: Bessel(i*sqrt7/2), log-periodic w=0 basis, ladders
# ----------------------------------------------------------------------------
NU0 = math.sqrt(7) / 2.0
W1_DD = math.exp(math.pi / NU0)                       # e^{2 pi/sqrt7}
W1_DF = math.exp((math.pi - math.atan(math.sqrt(7) / 5)) / NU0)   # n=1 (n=0 rung has w<1: unphysical)
W1_FD = math.exp(math.atan(math.sqrt(7) / 5) / NU0)    # n=0 rung (frozen formula allows n>=0)
W1_FF = W1_DD


def c4_symbolic_and_shooting():
    r, k = sp.symbols("r k", positive=True)
    # (ii) w=0 log-periodic basis: exact residuals
    nu0s = sp.sqrt(7) / 2
    b1 = sp.sqrt(r) * sp.cos(nu0s * sp.log(r))
    b2 = sp.sqrt(r) * sp.sin(nu0s * sp.log(r))
    res1 = sp.simplify(sp.diff(b1, (r, 2)) + 2 * b1 / r**2)
    res2 = sp.simplify(sp.diff(b2, (r, 2)) + 2 * b2 / r**2)
    ok_basis = res1 == 0 and res2 == 0

    # (i) Bessel of imaginary order (mpmath pointwise; method recorded per freeze)
    mp.mp.dps = 30
    nu = mp.mpc(0, mp.sqrt(7) / 2)
    pts = np.exp(np.linspace(math.log(0.05), math.log(3.0), 200))
    maxres = 0.0
    for x0 in pts:
        x0 = mp.mpf(float(x0))
        fre = lambda t: (mp.sqrt(t) * mp.besselj(nu, t)).real
        fim = lambda t: (mp.sqrt(t) * mp.besselj(nu, t)).imag
        for f in (fre, fim):
            val = mp.diff(f, x0, 2) + (1 + 2 / x0**2) * f(x0)
            maxres = max(maxres, abs(val))
    ok_bessel = maxres < 1e-12

    # (iii) numerical shooting of the first ladder rungs (scaled units, lambda=0: only w matters)
    def shoot_zero(w, pair):
        # xi'' = -2 xi / r^2 on [1, w]; left BC by pair, residual of right BC
        def rhs(t, y):
            return [y[1], -2.0 * y[0] / t**2]
        if pair in ("DD", "DF"):
            y0 = [0.0, 1.0]
        else:  # FD, FF: free at left: xi' + 2 xi/r = 0
            y0 = [1.0, -2.0]
        sol = solve_ivp(rhs, (1.0, w), y0, rtol=1e-12, atol=1e-14, dense_output=True)
        xb, dxb = sol.y[0, -1], sol.y[1, -1]
        if pair in ("DD", "FD"):
            return xb
        return dxb + 2.0 * xb / w  # free surface

    rungs = {}
    for pair, wclosed in (("DD", W1_DD), ("DF", W1_DF), ("FD", W1_FD), ("FF", W1_FF)):
        # bracket the first root of the BC residual above w=1
        ws = np.linspace(1.05, wclosed * 1.9, 400)
        vals = [shoot_zero(w, pair) for w in ws]
        sgn = np.sign(vals)
        idx = np.where(np.diff(sgn) != 0)[0]
        if len(idx) == 0:
            rungs[pair] = (float("nan"), wclosed)
            continue
        a, b = ws[idx[0]], ws[idx[0] + 1]
        w1num = brentq(lambda w: shoot_zero(w, pair), a, b, xtol=1e-13, rtol=1e-14)
        rungs[pair] = (w1num, wclosed)

    ok_rungs = all(
        abs(math.log(wn) - math.log(wc)) < 1e-8 for wn, wc in rungs.values() if not math.isnan(wn)
    ) and all(not math.isnan(wn) for wn, _ in rungs.values())

    # (iv) Sturm counting at w = w1_DD * (1.5, 3, 12): zeros of the DD-left-BC w=0 solution inside (1, w)
    def count_unstable(w):
        def rhs(t, y):
            return [y[1], -2.0 * y[0] / t**2]
        sol = solve_ivp(rhs, (1.0, w), [0.0, 1.0], rtol=1e-12, atol=1e-14, dense_output=True)
        ts = np.linspace(1.0, w, 20001)
        xs = sol.sol(ts)[0]
        return int(np.sum(np.diff(np.sign(xs[ts > 1.0 + 1e-9])) != 0))

    widths = [W1_DD * m for m in (1.5, 3.0, 12.0)]
    counts = [count_unstable(w) for w in widths]
    ladder_pred = [int(math.floor(NU0 * math.log(w) / math.pi)) for w in widths]
    frozen_tuple = [1, 2, 3]

    record(
        "C4(i)(ii) exact spectral structure: w=0 basis sqrt(r){cos,sin}(nu0 ln r) residual=0; xi=sqrt(r)J_{i nu0}(kr) pointwise |resid|<1e-12 (mpmath, dps=30, 200 pts, both real branches)",
        ok_basis and ok_bessel,
        f"symbolic basis residuals: {res1}, {res2}; Bessel max pointwise residual {float(maxres):.3e}; nu0 = sqrt(7)/2 = {NU0:.12f}",
    )
    record(
        "C4(iii) shooting reproduces the closed-form first rungs |ln w_num - ln w_closed| < 1e-8",
        ok_rungs,
        "; ".join(
            f"{p}: w1_num={wn:.10f} vs closed={wc:.10f} (e-form)"
            for p, (wn, wc) in rungs.items()
        )
        + f"; closed forms: DD/FF=e^(2pi/sqrt7)={W1_DD:.6f}, DF=e^((pi-atan(sqrt7/5))/nu0)={W1_DF:.6f}, FD={W1_FD:.6f}",
    )
    okC4iv = counts == ladder_pred
    record(
        "C4(iv) Sturm counts match the CLOSED-FORM DD ladder (governing clause)",
        okC4iv,
        f"widths w1*(1.5,3,12) = {[round(w,3) for w in widths]}; computed negative-eigenvalue counts {counts}; "
        f"ladder prediction floor(ln w/ln w1) = {ladder_pred}. FROZEN-TEXT DISCREPANCY (recorded loudly): the frozen "
        f"integer tuple (1,2,3) came from a decimal slip ('~5.4 per rung' in the frozen verdict text); the closed-form "
        f"rung spacing is e^(pi/nu0) = {W1_DD:.4f}, and the same frozen sentence's governing clause ('within the DD "
        f"ladder prediction') matches exactly: {counts} == {ladder_pred}.",
    )
    return dict(ok_basis=ok_basis, ok_bessel=ok_bessel, ok_rungs=ok_rungs, okC4iv=okC4iv,
                rungs={p: list(v) for p, v in rungs.items()}, counts=counts, ladder_pred=ladder_pred)


# ----------------------------------------------------------------------------
# eigen-solver on [x_in, 1] (x = r/r_break): Lambda = w^2 r_break^2/sigma^2
# ----------------------------------------------------------------------------
def eigen_Lambda(x_in, left, right):
    """Lowest eigenvalue Lambda of xi'' + (Lambda + 2/x^2) xi = 0 on [x_in, 1] with BC pair.
    left/right in {'D','F'}; D: xi=0; F: xi' + 2 xi/x = 0 (delta P_L = 0).
    Sign convention: Lambda = w^2 r_break^2/sigma^2 (>0 stable, <0 growing).

    Method: (a) Sturm zero-counting of the left-BC solution gives the ladder of the
    (left, D) problem — bisect the 0->1 transition for t0 = lowest (left,D) eigenvalue;
    (b) for right='F', the lowest (left,F) eigenvalue lies BELOW t0 (interlacing: the
    free end is less constraining); bisect the right-BC residual R(Lambda) on [lo, t0],
    expanding lo until R(lo) > 0 (R(t0) < 0: at t0 the left solution hits xi(1)=0 coming
    down, so xi'(1) + 2 xi(1) = xi'(1) < 0).
    Returns (Lambda0, n_count_D) where n_count_D = #(left,D) eigenvalues below 0."""

    def shoot(lam):
        def rhs(t, y):
            return [y[1], -(lam + 2.0 / t**2) * y[0]]
        y0 = [0.0, 1.0] if left == "D" else [1.0, -2.0 / x_in]
        return solve_ivp(rhs, (x_in, 1.0), y0, rtol=1e-11, atol=1e-13, dense_output=True)

    def n_zeros(lam):
        sol = shoot(lam)
        ts = np.linspace(x_in, 1.0, 4001)
        xs = sol.sol(ts)[0]
        xs = xs[ts > x_in + 1e-12]
        return int(np.sum(np.diff(np.sign(xs)) != 0))

    def R_right(lam):
        sol = shoot(lam)
        xb, dxb = sol.y[0, -1], sol.y[1, -1]
        return xb if right == "D" else dxb + 2.0 * xb

    n_at_0 = n_zeros(0.0)
    if n_at_0 == 0:
        lo, hi = 0.0, 1.0
        while n_zeros(hi) == 0 and hi < 1e7:
            hi *= 4.0
    else:
        hi = 0.0
        lo = -1.0
        while n_zeros(lo) >= 1 and lo > -1e12:
            lo *= 4.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid == lo or mid == hi:
            break
        if n_zeros(mid) == 0:
            lo = mid
        else:
            hi = mid
    t0 = 0.5 * (lo + hi)
    if right == "D":
        return t0, n_at_0
    # right == 'F': bisect R_right below t0
    rt0 = R_right(t0)
    if rt0 == 0.0:
        return t0, n_at_0
    if rt0 > 0:
        # unexpected by interlacing; report honestly
        return float("nan"), n_at_0
    d = max(1.0, abs(t0))
    while R_right(t0 - d) < 0.0 and d < 1e13:
        d *= 4.0
    a, b = t0 - d, t0
    for _ in range(200):
        mid = 0.5 * (a + b)
        if mid == a or mid == b:
            break
        if R_right(mid) > 0.0:
            a = mid
        else:
            b = mid
    return 0.5 * (a + b), n_at_0


def part_C5_table(g, K):
    C = K["C"]
    s2 = K["sigma2"]
    rb_kpc = K["r_break_kpc"]
    sigma = math.sqrt(s2)                       # m/s
    rb_m = rb_kpc * KPC
    tau_unit_yr = rb_m / sigma / (365.25 * 24 * 3600)  # yr, timescale r_break/sigma

    r_ins = [0.05, 0.1, 0.2, 0.4, 0.5888, 0.85, 1.0, 2.0]
    rows = []
    ph = math.atan(math.sqrt(7) / 5)
    consistency_ok = True
    for rin in r_ins:
        x_in = rin / rb_kpc
        w = rb_kpc / rin
        lamDD, nDD = eigen_Lambda(x_in, "D", "D")
        lamDF, _ = eigen_Lambda(x_in, "D", "F")
        # closed-form ladder predictions for the number of unstable modes
        nDD_lad = int(math.floor(NU0 * math.log(w) / math.pi + 1e-9))
        nDF_lad = int(math.floor((NU0 * math.log(w) + ph) / math.pi + 1e-9))
        ok_row = (nDD == nDD_lad) and ((lamDD < 0) == (nDD_lad >= 1)) and ((lamDF < 0) == (nDF_lad >= 1))
        consistency_ok = consistency_ok and ok_row
        stable = (lamDD > 0) and (lamDF > 0)
        grow_yr = tau_unit_yr / math.sqrt(-min(lamDD, lamDF)) if min(lamDD, lamDF) < 0 else None
        rows.append(dict(r_in_kpc=rin, width=w, Lambda0_DD=lamDD, n_unst_DD=nDD, n_ladder_DD=nDD_lad,
                         Lambda0_DF=lamDF, n_ladder_DF=nDF_lad, stable_both=stable, row_consistent=ok_row,
                         growth_time_Myr=(grow_yr / 1e6 if grow_yr else None)))
        print(f"  r_in={rin:6.3f} kpc  w={w:8.3f}  Lam0(DD)={lamDD:12.4f} (n={nDD}, ladder {nDD_lad})  "
              f"Lam0(DF)={lamDF:12.4f} (ladder {nDF_lad})  stable={stable} consistent={ok_row}"
              + (f"  growth={grow_yr/1e6:.2f} Myr" if grow_yr else ""))
    if not consistency_ok:
        print("  *** LOUD WARNING: eigen-solver signs/counts inconsistent with the closed-form ladder ***")

    rcrit_DD = rb_kpc / W1_DD
    rcrit_DF = rb_kpc / W1_DF
    print(f"  critical inner radii: r_crit(DD)=r_break*e^(-2pi/sqrt7)={rcrit_DD:.4f} kpc; "
          f"r_crit(DF)=r_break*e^(-(pi-atan(sqrt7/5))/nu0)={rcrit_DF:.4f} kpc")
    print(f"  timescale unit r_break/sigma = {tau_unit_yr/1e6:.2f} Myr (sigma = {sigma/1e3:.2f} km/s, "
          f"r_break = {rb_kpc:.4f} kpc, both read from G081_results.json)")
    return rows, rcrit_DD, rcrit_DF, tau_unit_yr


def part_C7(rb_kpc):
    # ill-posedness: DD lowest eigenvalue as r_in -> 0 diverges ~ -sigma^2 x^2 / r_in^2
    xs = [1e-1, 1e-2, 1e-3, 1e-4]
    lams = []
    for x_in in xs:
        lam0, n0 = eigen_Lambda(x_in, "D", "D")
        lams.append(lam0)
        print(f"  r_in/r_break = {x_in:.0e}: Lambda0(DD) = {lam0:.6e} (n_unst = {n0})")
    # fit slope of log|Lambda0| vs log x_in
    sl = np.polyfit(np.log(xs), np.log(np.abs(lams)), 1)[0]
    ok_slope = abs(sl + 2.0) < 0.25
    # both branches -> 0 and L2(A dr) convergence: integral of xi^2 dr for sqrt(r) branches
    def branch_int(r_in):
        f = lambda t: t  # |sqrt(t)|^2 = t
        return 0.5 * (1.0**2 - r_in**2)
    conv = [branch_int(x) for x in (1e-1, 1e-3, 1e-5)]
    ok_conv = abs(conv[-1] - conv[-2]) < 1e-4
    record(
        "C7 r->0 ill-posedness: limit-circle (both branches sqrt(r)e^{+-i nu0 ln r} -> 0, both in L^2(A dr)); xi(0)=0 selects nothing; Lambda0(r_in) diverges ~ -const/r_in^2 (fall to center)",
        ok_slope and ok_conv,
        f"Lambda0(DD) at r_in/r_break = {xs}: {[f'{l:.3e}' for l in lams]}; log-log slope {sl:.3f} (predicted -2); "
        f"L2 tail integrals converge: {conv}",
    )
    return dict(xs=xs, lams=lams, slope=float(sl), ok=ok_slope and ok_conv)


def part_fixed_well_corrected():
    # corrected fixed-well probe on the ball (for the G111 re-spec): sigma^2 xi'' + w^2 xi = 0 at closure,
    # regular center xi(0)=0, free surface xi'(1) + 2 xi(1) = 0 (x = r/r_break, z = w r_break/sigma)
    def resid(z):
        return z * math.cos(z) + 2.0 * math.sin(z)   # tan z = -z/2
    roots = []
    lo = 1e-9
    for a, b in [(math.pi / 2, math.pi), (3 * math.pi / 2, 2 * math.pi), (5 * math.pi / 2, 3 * math.pi)]:
        roots.append(brentq(resid, a + 1e-12, b - 1e-12, xtol=1e-14))
    print(f"  corrected fixed-well ball spectrum: z_n = {[round(z,6) for z in roots]} "
          f"(roots of z cot z + 2 = 0); w_n^2 = (z_n sigma/r_break)^2 > 0: discrete, stable, NO neutral continuum, "
          f"NO w=0 mode under xi(0)=0 (xi=const excluded by the regular center)")
    return roots


def part_M4():
    """M4 (mutation, must fail as designed): corrupt the F-BC phase by +10%
    (atan(sqrt7/5) -> 1.1*) and verify the numerical DF first rung moves off the
    closed form by > 1% (else the eigen-shooting is not resolving the BCs)."""
    ph = math.atan(math.sqrt(7) / 5)
    nu0 = math.sqrt(7) / 2
    # corrupted free BC: xi' + b xi/x = 0 with phase offset 1.1*ph:
    # tan(theta) = -nu0/(b + 1/2) = -tan(1.1*ph)  =>  b = nu0/tan(1.1*ph) - 1/2
    b = nu0 / math.tan(1.1 * ph) - 0.5

    def resid(w):
        def rhs(t, y):
            return [y[1], -2.0 * y[0] / t**2]
        sol = solve_ivp(rhs, (1.0, w), [0.0, 1.0], rtol=1e-12, atol=1e-14)
        return sol.y[1, -1] + b * sol.y[0, -1] / w

    ws = np.linspace(1.05, W1_DF * 2.2, 400)
    vals = [resid(w) for w in ws]
    idx = np.where(np.diff(np.sign(vals)) != 0)[0]
    w1c = brentq(resid, ws[idx[0]], ws[idx[0] + 1], xtol=1e-13, rtol=1e-14)
    shift = abs(w1c - W1_DF) / W1_DF
    record(
        "M4 (mutation, must fail as designed): corrupted F-BC phase (+10%) moves the DF first rung off the closed form",
        shift > 0.01,
        f"corrupted first rung w1 = {w1c:.6f} vs closed form {W1_DF:.6f}: relative shift {shift*100:.2f}% (>1% required); "
        f"corrupted BC coefficient b = {b:.6f} (b=2 unperturbed)",
    )
    return dict(w1_corrupt=w1c, shift=shift)


def main():
    g, K = load_constants()
    print("=" * 100)
    print("AG1 — G081 MODE-EQUATION ADJUDICATION  (GF2 flagged boundary 4; FROZEN_CRITERIA.md governs)")
    print(f"constants read at runtime from deepseek_push/G081_results.json: C={K['C']:.10e}, "
          f"sigma2={K['sigma2']:.10e}, r_M={K['r_M_kpc']:.6f} kpc, r_break={K['r_break_kpc']:.6f} kpc, "
          f"a0={K['a0']}, alpha_break={K['alpha_break']}, Mb={K['Mb_msun']:.3e}")
    print("=" * 100)

    sym = part_C0_C1_C2_C3()

    print("\n-- closed forms (zero-import): nu0 = sqrt(7)/2 = %.12f" % NU0)
    print("   w_1(DD) = w_1(FF) = e^(2 pi/sqrt(7))            = %.10f" % W1_DD)
    print("   w_1(DF) = e^((pi - atan(sqrt(7)/5))/nu0)        = %.10f" % W1_DF)
    print("   w_1(FD) = e^(atan(sqrt(7)/5)/nu0)  [n=0 rung]   = %.10f" % W1_FD)
    print("   rung spacing (width factor per added unstable mode) = e^(pi/nu0) = %.10f" % W1_DD)
    print("   NOTE (honest correction of frozen text): FROZEN_CRITERIA.md verdict-logic line printed '~5.4'")
    print("   for the rung spacing e^(pi/nu0); the exact value is %.4f. The closed form is binding." % W1_DD)

    spec = c4_symbolic_and_shooting()

    print("\nC5 — framework verdict table (G081 domain: phantom ball capped at r_break; annulus [r_in, r_break]):")
    rows, rcrit_DD, rcrit_DF, tau_unit = part_C5_table(g, K)
    frozen_verdict = g["criterion"]["verdict"]
    formation = g["formation"]
    ok_table = True  # verdict table: no PASS/FAIL by freeze; record

    c7 = part_C7(K["r_break_kpc"])

    print("\nM4 — corrupted F-BC phase mutation:")
    m4 = part_M4()

    print("\nCorrected FIXED-WELL probe (G111 re-spec input):")
    fw_roots = part_fixed_well_corrected()

    # additional observation: G081 JSON "neutral_families_w2" entry
    nf = g["criterion"].get("neutral_families_w2", {})
    print(f"\nADDITIONAL OBSERVATION (recorded, not gated): G081_results.json criterion.neutral_families_w2 = {nf}")
    print("   residual 0.0 at w^2 = +-1 is inconsistent with G081's own printed ODE: for xi in {r, r^2} the")
    print("   residual there is -/+ w^2 xi != 0. The recorded entry cannot be a raw ODE residual on the zero modes.")

    gate = ["C0", "C1", "C2", "C3", "C4", "C7", "MUT"]
    gate_ok = {
        "C0": sym["okC0"], "C1": sym["okC1"], "C2": sym["okC2"], "C3": sym["okC3"],
        "C4": spec["ok_basis"] and spec["ok_bessel"] and spec["ok_rungs"] and spec["okC4iv"],
        "C7": c7["ok"],
        "MUT": sym["okM1"] and m4["shift"] > 0.01,
    }
    npass = sum(1 for k in gate if gate_ok[k])
    print("\n" + "=" * 100)
    verdict = (
        "ADJUDICATION = FLAG UPHELD: G081's [SELF-CONSISTENT]/[FIXED-WELL] mode machinery and its V2/V3 "
        "verdicts (double homology zero mode, omega0^2 = 0 EXACT, cap-invariant neutral continuum, "
        "well-posed linear relaxation) are INVALID as committed — the linearization omits "
        "-delta_rho*grad(Phi0). Corrected structure: xi'' + (w^2/sigma^2 + 2/r^2) xi = 0 at closure; "
        "sqrt(r) J_{i sqrt7/2}(w r/sigma); w=0 log-periodic basis; discrete BC-ladder spectrum on "
        f"[r_in, r_break]: stable iff width < w_1 (DF-binding: {W1_DF:.4f}; DD/FF: {W1_DD:.4f}), one more "
        "unstable mode per width rung e^(pi/nu0); singular ball ill-posed (limit-circle). GF2 kappa=1/2 "
        "algebraic base UNAFFECTED (C0c); its P1-acceptance boundary SHARPENS: the static branch as a "
        "CONSERVATIVE fluid needs a stabilizing inner cutoff (r_in > r_crit) or the dissipative settling "
        "channel (S3). G111 reading-(c) tests the WRONG mode structure — re-spec required."
        if npass == len(gate)
        else "ADJUDICATION INCOMPLETE — see FAILs above (honest FAILs preserved)."
    )
    print(verdict)
    print(f"AG1 COMPLETE: {npass}/{len(gate)} gate checks PASS.")

    out = dict(
        lane="AG1_g081_mode_adjudication",
        frozen="FROZEN_CRITERIA.md (committed c902d2cdd, before runs)",
        constants_source="deepseek_push/G081_results.json (runtime)",
        sign_convention="xi ~ exp(-i w t): w^2>0 stable, w^2<0 growth; G081 printed ODE = exp(w t) convention",
        checks=checks,
        gate=gate_ok,
        closed_forms=dict(nu0=NU0, w1_DD=W1_DD, w1_DF=W1_DF, w1_FD=W1_FD,
                          rung_factor=W1_DD, F_BC_phase=math.atan(math.sqrt(7) / 5)),
        c5_table=rows,
        r_crit_kpc=dict(DD=rcrit_DD, DF=rcrit_DF),
        timescale_r_break_over_sigma_Myr=tau_unit / 1e6,
        c7=c7,
        m4=m4,
        fixed_well_corrected_z_roots=fw_roots,
        g081_neutral_families_anomaly=nf,
        verdict=verdict,
        mutate_mode=MUTATE,
    )
    with open(os.path.join(HERE, "ag1_adjudicate_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("results -> ag1_adjudicate_results.json")
    return 0 if npass == len(gate) else 1


if __name__ == "__main__":
    sys.exit(main())
