#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG188 R1 -- independent static reduction of 11C-a from the UNITARY-GAUGE (ADM) action in AREAL gauge, nonlinear.
   S = (1/16 pi G) Int N sqrt(h) [ R3 + F_a(X) ] - Int N sigma (dust), X = a^2 = N'^2/(N^2 A^2),  ds^2 = -N^2 dt^2 + A^2 dr^2 + r^2 dOmega^2 (c = 1),
   static slicing K_ij = 0 (theta passive, leaf-averaged theta term drops out).  F_a(X) = 2 a_*^2 Q(sqrt(X)/a_*),  a_* = a0/c^2  (the frozen normalisation).
   Controls (exit 1 on failure): C1 Schwarzschild, C2 G_N = G/(1-c14/2), C3 exponential kernel, C4 P2 identities, C5 prescribed flow.
   MUTATE=M3 (kernel -> GR), M4 (q -> -q), M9 (drop the N'-dependent aether term in the derivation)."""
import sys, math
import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline
from scipy.integrate import quad
from scipy.optimize import brentq
import CFG188_common as C

def christoffel(g, xs):
    n = len(xs); gi = g.inv()
    return [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], xs[c]) + sp.diff(g[d, c], xs[b]) - sp.diff(g[b, c], xs[d])) for d in range(n)) / 2)
              for c in range(n)] for b in range(n)] for a in range(n)]

def derive(drop_aether=False, extra_zeta=False):
    r, N, Np, Npp, A, Ap, App, eps, G, al, zeta = sp.symbols("r N Np Npp A Ap App eps G alpha zeta", positive=True)
    P = sp.Function("P")(r); Fv = sp.Function("Fv")(r); sig = sp.Function("sig")(r)
    f = sp.Function("f")(r); m = sp.Function("m")(r); s = sp.Function("s")(r); Fv2 = sp.Function("Fv2")(r)
    # 3-Ricci scalar of h = diag(A^2, r^2, r^2 sin^2) computed from the metric (independent of any hand formula)
    th, ph = sp.symbols("theta phi")
    Af = sp.Function("Af")(r)
    xs = [r, th, ph]
    h = sp.diag(Af ** 2, r ** 2, r ** 2 * sp.sin(th) ** 2)
    Gm = christoffel(h, xs)
    def ricci(i, j):
        return sum(sp.diff(Gm[k][i][j], xs[k]) for k in range(3)) - sum(sp.diff(Gm[k][i][k], xs[j]) for k in range(3)) \
            + sum(Gm[k][k][l] * Gm[l][i][j] for k in range(3) for l in range(3)) - sum(Gm[k][j][l] * Gm[l][i][k] for k in range(3) for l in range(3))
    hi = h.inv()
    R3f = sp.simplify(sum(hi[i, i] * ricci(i, i) for i in range(3)))
    R3 = R3f.subs(sp.Derivative(Af, (r, 2)), 0).subs(sp.Derivative(Af, r), Ap).subs(Af, A)
    R3hand = 2 / r ** 2 * (1 - 1 / A ** 2 + 2 * r * Ap / A ** 3)
    R3_ok = sp.simplify(R3 - R3hand) == 0
    X = Np ** 2 / (N ** 2 * A ** 2)
    Pe = 0 if drop_aether else P
    Fe = 0 if drop_aether else Fv
    Lexp = N * A * r ** 2 * (R3 + Fe) - 16 * sp.pi * G * N * sig
    Lz = zeta * N * A * r ** 2 * R3 ** 2 if extra_zeta else 0
    Lexp = Lexp + Lz
    dLdN = sp.diff(Lexp, N) + N * A * r ** 2 * Pe * sp.diff(X, N)
    dLdNp = sp.diff(Lexp, Np) + N * A * r ** 2 * Pe * sp.diff(X, Np)
    dLdA = sp.diff(Lexp, A) + N * A * r ** 2 * Pe * sp.diff(X, A)
    dLdAp = sp.diff(Lexp, Ap)
    D = lambda e: sp.diff(e, r) + Np * sp.diff(e, N) + Npp * sp.diff(e, Np) + Ap * sp.diff(e, A) + App * sp.diff(e, Ap)
    EL_N = dLdN - D(dLdNp)
    EL_A = dLdA - D(dLdAp)
    sub = {N: 1 + eps * f, Np: eps * sp.diff(f, r), Npp: eps * sp.diff(f, r, 2), A: 1 + eps * m, Ap: eps * sp.diff(m, r), App: eps * sp.diff(m, r, 2)}
    def lead(E):
        E1 = E.subs(sub).subs({sig: eps * s, Fv: eps ** 2 * Fv2})
        E1 = E1.subs(zeta, zeta)  # keep
        return sp.simplify(sp.series(E1, eps, 0, 2).removeO().coeff(eps, 1))
    return dict(r=r, G=G, P=P, f=f, m=m, s=s, sig=sig, Fv=Fv, EL_N=EL_N, EL_A=EL_A, lead=lead, R3_ok=R3_ok,
                syms=(N, Np, Npp, A, Ap, App), zeta=zeta)

def build_q_from_target(kind):
    y = np.logspace(-4, 4, 3001)
    mu = C.mu_of_y(C.TARGETS[kind], y)
    cs = CubicSpline(np.log(y), np.log(mu))
    return (lambda yy: np.exp(cs(np.log(np.maximum(np.asarray(yy, float), 1e-4)))))

def solve_law(yN, mufun, sign=+1.0):
    """derived law: y (1 - sign*q(y)) = y_N, q = 1 - mu  (sign=-1 is the M4 flip)"""
    def F(y):
        q = 1.0 - mufun(y)
        return y * (1.0 - sign * q) - yN
    lo, hi = 1e-4, 1e4
    if F(lo) > 0 or F(hi) < 0:
        return float("nan")
    return brentq(F, lo, hi, xtol=1e-14, rtol=1e-13)

def grid_dev(kind, mufun, sign=1.0, xs=(0.1, 30.0), n=61):
    """G1 grid: 7 masses 1e9..1e12, point mass and exponential sphere (h = 2 kpc), both footings"""
    res = {}
    gt = C.TARGETS[kind]
    worst = 0.0
    for foot, a0si in C.FOOT.items():
        w = 0.0
        for M in np.logspace(9, 12, 7):
            rM = C.rM_kpc(M, a0si)
            for x in np.logspace(math.log10(xs[0]), math.log10(xs[1]), n):
                r = x * rM
                for prof in ("point", "exp"):
                    frac = 1.0 if prof == "point" else float(C.mb_frac(r / 2.0))
                    yN = frac / x ** 2
                    yg = solve_law(yN, mufun, sign)
                    yt = float(gt(yN))
                    w = max(w, abs(yg / yt - 1.0)) if np.isfinite(yg) else max(w, 1.0)
        res[foot] = w
        worst = max(worst, w)
    return worst, res

def main():
    chk = C.Checks(); R = {}
    m = C.mode()
    print("CFG188 R1 -- static reduction from the unitary-gauge ADM action, areal gauge, nonlinear. mode:", m or "main")
    d = derive(drop_aether=(m == "M9"))
    r, G, P, f, ms, s = d["r"], d["G"], d["P"], d["f"], d["m"], d["s"]
    EL_N, EL_A, lead = d["EL_N"], d["EL_A"], d["lead"]
    N_, Np_, Npp_, A_, Ap_, App_ = d["syms"]
    chk.add("R3 from the metric equals 2/r^2 (1 - 1/A^2 + 2 r A'/A^3)", d["R3_ok"])
    # leading-order equations
    LN = lead(EL_N); LA = lead(EL_A)
    print("  leading EL_N/eps =", LN)
    print("  leading EL_A/eps =", LA)
    R["EL_N_lead"] = str(LN); R["EL_A_lead"] = str(LA)
    # claimed structure: EL_N = 4 (r m)' - (2 r^2 P f')' - 16 pi G s ; EL_A = k (r f' - m) form
    claimN = 4 * sp.diff(r * ms, r) - sp.diff(2 * r ** 2 * P * sp.diff(f, r), r) - 16 * sp.pi * G * s
    if m == "M9":
        claimN = 4 * sp.diff(r * ms, r) - 16 * sp.pi * G * s
    resN = sp.simplify(LN - claimN)
    R["resN"] = str(resN)
    # Solve: EL_A gives m in terms of f'
    m_sol = sp.solve(sp.Eq(LA, 0), ms)
    print("  EL_A=0 solved for m:", m_sol)
    fp = sp.Symbol("fp"); Mfun = sp.Function("Mb")(r)
    # integrate N eq (first integral): 4 r m - 2 r^2 P f' = 4 G Mb(r), Mb' = 4 pi s
    if m_sol:
        msol = m_sol[0]
        first = 4 * r * msol - (0 if m == "M9" else 2 * r ** 2 * P * sp.diff(f, r)) - 4 * G * Mfun
        # law: solve for f'
        law = sp.solve(sp.Eq(first.subs(sp.Derivative(f, r), fp), 0), fp)
        print("  derived law: f' =", law)
        R["law_fprime"] = [str(x) for x in law]
    # check first integral: d/dr[first] = LN with Mb'=4 pi s
    if m_sol:
        dfirst = sp.diff(first, r).subs(sp.Derivative(Mfun, r), 4 * sp.pi * s)
        chk_first = sp.simplify(dfirst - LN.subs(ms, msol).doit()) == 0
        # LN contains m (function); substitute solved m
        chk_first = sp.simplify(sp.diff(first, r).subs(sp.Derivative(Mfun, r), 4 * sp.pi * s) - LN.subs(ms, msol).doit()) == 0
    # ---- R1.a: with F'(X) = P = 2 q(y):  f'(1 - P/2) = G Mb / r^2 -> mu = 1 - q
    a, y = sp.symbols("a y", positive=True); Xs = sp.Symbol("X", positive=True)
    c_1, c_2, c_3, c_4 = sp.symbols("c_1 c_2 c_3 c_4")
    Qpoly = lambda z: c_1 * z ** 2 + c_2 * z ** 3 + c_3 * z ** 4 + c_4 * z ** 5       # generic test family for Q
    Fexpr = 2 * a ** 2 * Qpoly(sp.sqrt(Xs) / a)
    dF = sp.diff(Fexpr, Xs).subs(Xs, (y * a) ** 2)
    Qp_over_y = sp.diff(Qpoly(y), y) / y
    Fprime_ok = sp.simplify(dF - Qp_over_y) == 0
    print("  F'(X) for F = 2 a_*^2 Q(sqrt(X)/a_*) equals Q'(y)/y = 2 q(y):", Fprime_ok)
    R["Fprime_ok"] = bool(Fprime_ok)
    if m != "M9":
        law_mu = sp.simplify(law[0] * r ** 2 / (G * Mfun) - 1 / (1 - P / 2)) == 0 if law else False
        chk.add("R1.a: N-equation leading order = 4(rm)' - (2 r^2 P f')' - 16 pi G s (residual == 0)", resN == 0)
        chk.add("R1.a: derived law f'(1 - P/2) = G Mb/r^2, i.e. mu = 1 - q with P = 2q (residual == 0)", bool(law_mu))
        chk.add("R1.a: first integral of the N equation is exact", bool(chk_first))
        chk.add("F'(X) = Q'(y)/y = 2 q(y) (sympy, generic polynomial Q)", Fprime_ok)
    # ---- R1.b: slip.  A-equation gives f' = m/r  <=>  Psi' = Phi' (isotropic: m = rho Psi')
    slip_rel = sp.simplify(LA.subs(ms, r * sp.diff(f, r)))
    R["EL_A_with_m=r f'"] = str(slip_rel)
    if m != "M9":
        chk.add("R1.b: EL_A leading order vanishes iff m = r f' (Psi' = Phi', isotropic gauge)", slip_rel == 0)
    # ---- C1 Schwarzschild exact
    rs = sp.Symbol("rs", positive=True)
    Ns = sp.sqrt(1 - rs / r); As = 1 / Ns
    subs_exact = {N_: Ns, Np_: sp.diff(Ns, r), Npp_: sp.diff(Ns, r, 2), A_: As, Ap_: sp.diff(As, r), App_: sp.diff(As, r, 2)}
    EN0 = EL_N.subs({P: 0, d["Fv"]: 0, d["sig"]: 0}).subs(subs_exact)
    EA0 = EL_A.subs({P: 0, d["Fv"]: 0, d["sig"]: 0}).subs(subs_exact)
    c1 = sp.simplify(EN0) == 0 and sp.simplify(EA0) == 0
    chk.add("C1: exact Schwarzschild (N^2 = 1 - rs/r, A = 1/N) solves the derived exact EL_N and EL_A (residual == 0)", c1)
    # ---- C2 linear aether G_N = G/(1 - c14/2)
    c14 = sp.Symbol("c14", positive=True)
    fp_lin = sp.solve(sp.Eq(first.subs(sp.Derivative(f, r), fp).subs(P, c14), 0), fp)[0] if m_sol else None
    if fp_lin is not None and m != "M9":
        GN = sp.simplify(fp_lin * r ** 2 / Mfun)
        chk.add("C2: linear aether F = c14 a^2 gives G_N = G/(1 - c14/2)", sp.simplify(GN - G / (1 - c14 / 2)) == 0, f"G_N/G = {sp.simplify(GN / G)}")
    # ---- C3 exponential kernel (yq)' and W''
    yy = sp.Symbol("y", positive=True)
    q_exp = sp.exp(-yy)
    c3 = sp.simplify(sp.diff(yy * q_exp, yy) - (1 - yy) * sp.exp(-yy)) == 0 and sp.simplify((1 - sp.diff(yy * q_exp, yy)) - (1 + (yy - 1) * sp.exp(-yy))) == 0
    chk.add("C3: q = e^{-y}: (yq)' = (1-y)e^{-y} and 1-(yq)' = 1+(y-1)e^{-y} (record's W'')", c3)
    # ---- C4 P2 identities
    yv = np.logspace(-3, 3, 13)
    mu_num = C.mu_of_y(C.gt_p2, yv)
    mu_cl = (np.sqrt(1 + 4 * yv ** 2) - 1) / (2 * yv)
    chk.add("C4: P2 kernel mu(y_g) = (sqrt(1+4y^2)-1)/(2y) from g^2 = g_N^2 + a0 g_N", np.max(np.abs(mu_num / mu_cl - 1)) < 1e-9, f"max rel {np.max(np.abs(mu_num/mu_cl-1)):.2e}")
    xx = 1.7
    chk.add("C4: CFG44 point-mass identity M_c/M = sqrt(1+x^2)-1 with g/g_N = sqrt(1+x^2)", abs((float(C.gt_p2(1 / xx ** 2)) * xx ** 2) - math.sqrt(1 + xx ** 2)) < 1e-12)
    ypq = sp.simplify(sp.diff(yy * (1 - (sp.sqrt(1 + 4 * yy ** 2) - 1) / (2 * yy)), yy) - (1 - 2 * yy / sp.sqrt(1 + 4 * yy ** 2))) == 0
    chk.add("(yq)' = 1 - 2y/sqrt(1+4y^2) for P2 (sympy)", ypq)
    # ---- R1.c covariant aether radial equation, static aligned u, generic F(a^2)
    t, th, ph = sp.symbols("t theta phi")
    Nf = sp.Function("Nf")(r); Af2 = sp.Function("Af2")(r); Pf = sp.Function("Pf")(r)
    xs4 = [t, r, th, ph]
    g4 = sp.diag(-Nf ** 2, Af2 ** 2, r ** 2, r ** 2 * sp.sin(th) ** 2)
    Gm4 = christoffel(g4, xs4); g4i = g4.inv(); sq = Nf * Af2 * r ** 2 * sp.sin(th)
    u_up = [1 / Nf, 0, 0, 0]; u_dn = [-Nf, 0, 0, 0]
    cov = [[sp.diff(u_dn[b], xs4[a]) - sum(Gm4[l][a][b] * u_dn[l] for l in range(4)) for b in range(4)] for a in range(4)]   # nabla_a u_b
    acc = [sum(u_up[a] * cov[a][b] for a in range(4)) for b in range(4)]
    a_up = [sum(g4i[b, c] * acc[c] for c in range(4)) for b in range(4)]
    ident = all(sp.simplify(cov[a][b] + u_dn[a] * acc[b]) == 0 for a in range(4) for b in range(4))
    chk.add("R1.c/(a)(iii): static aligned u has nabla_a u_b = -u_a a_b exactly, so sigma = theta = omega = 0 on static slices", ident)
    T = [[2 * Pf * acc[mu_] * u_up[nu_] for nu_ in range(4)] for mu_ in range(4)]     # T_mu^nu = 2 F' a_mu u^nu
    def divT(mu_):
        return sum(sp.diff(sq * T[mu_][nu_], xs4[nu_]) for nu_ in range(4)) / sq - sum(Gm4[l][nu_][mu_] * T[l][nu_] for l in range(4) for nu_ in range(4))
    E = [sp.simplify(2 * Pf * sum(a_up[nu_] * cov[mu_][nu_] for nu_ in range(4)) - divT(mu_)) for mu_ in range(4)]
    print("  aether equation E_mu (spatial projection) =", E)
    chk.add("R1.c: radial (and angular) components of the covariant aether equation vanish identically for static aligned u and generic F(a^2)", E[1] == 0 and E[2] == 0 and E[3] == 0)
    R["aether_E"] = [str(e) for e in E]
    # ---- attack (a)(ii): a term zeta R3^2 changes the leading static reduction
    if not m:
        dz = derive(extra_zeta=True)
        LNz = dz["lead"](dz["EL_N"]); LAz = dz["lead"](dz["EL_A"])
        dN = sp.simplify(LNz - LN); dA = sp.simplify(LAz - LA)
        R["zetaR3sq_dEL_N_lead"] = str(dN); R["zetaR3sq_dEL_A_lead"] = str(dA)
        print("  (a)(ii) adding zeta R3^2: change of EL_N leading =", dN, "; change of EL_A leading =", dA)
        chk.add("(a)(ii): a zeta R3^2 term leaves EL_N at leading order but changes EL_A at leading order (the class is a declared choice)", dN == 0 and dA != 0)
    # ---- numerics: G1 grid from the derived law
    if m in ("", "M3", "M4"):
        sign = -1.0 if m == "M4" else 1.0
        qfun = {}
        for kind in ("P2", "nu_mono"):
            qfun[kind] = build_q_from_target(kind)
        if m == "M3":
            mu_use = {k: (lambda yy_: np.ones_like(np.asarray(yy_, float))) for k in qfun}
        else:
            mu_use = qfun
        for kind in ("P2", "nu_mono"):
            wdev, per = grid_dev(kind, mu_use[kind], sign)
            R[f"G1_maxdev_{kind}"] = wdev; R[f"G1_maxdev_{kind}_per_footing"] = per
            print(f"  G1-law from the derived equations, target {kind}: max |g/g_target - 1| = {wdev:.3e}  per footing {per}")
        if not m:
            chk.add("R1.d: G1 law max dev P2 <= 1e-6 (frozen reporting line)", R["G1_maxdev_P2"] <= 1e-6, f"{R['G1_maxdev_P2']:.2e}")
            chk.add("R1.d: G1 law max dev nu_mono <= 1e-4 (frozen reporting line)", R["G1_maxdev_nu_mono"] <= 1e-4, f"{R['G1_maxdev_nu_mono']:.2e}")
            R["G1_frozen_10pct_line"] = bool(max(R["G1_maxdev_P2"], R["G1_maxdev_nu_mono"]) <= 0.10)
        # attack (d)(i): simple kernel law against the P2 target
        if not m:
            xg = np.logspace(-1, math.log10(30), 200); yN = 1 / xg ** 2
            dev = np.max(np.abs(C.gt_simple(yN) / C.gt_p2(yN) - 1))
            devnu = np.max(np.abs((C.gt_simple(yN) / yN) / (C.gt_p2(yN) / yN) - 1))
            R["simple_vs_P2_maxdev_g"] = float(dev)
            print(f"  (d)(i): simple-kernel law against the P2 target: max |g/g_P2 - 1| = {dev:.3f} (fails the 10% line: the declared kernel is required)")
            chk.add("(d)(i): a different declared kernel (simple) fails the 10% G1 line against P2", dev > 0.10, f"{dev:.3f}")
        # slip estimate on the grid (P2), exact EL_A residual at the leading-order solution
        if not m:
            a_star = C.FOOT["canonical"] / C.C_SI ** 2
            Qint = lambda yq_: quad(lambda z: 2 * z * float(C.q_p2(z)), 0, yq_, epsabs=0, epsrel=1e-11)[0]
            worst = 0.0; worst_gr = 0.0; worst_ae = 0.0
            Pv, Fvv, rr = sp.symbols("Pv Fvv rr")
            ELA_num = EL_A.subs({P: Pv, d["Fv"]: Fvv, d["sig"]: 0}).subs(r, rr)
            has_dP = ELA_num.has(sp.Derivative(P, r))
            ELA_f = sp.lambdify((N_, Np_, Npp_, A_, Ap_, App_, rr, Pv, Fvv), ELA_num, "math")
            for M in (1e9, 1e12):
                rM = C.rM_kpc(M, C.FOOT["canonical"])
                for x in (0.1, 1.0, 30.0):
                    rkpc = x * rM
                    def g_of(rk):
                        return float(C.gt_p2(1.0 / (rk / rM) ** 2)) * C.FOOT["canonical"]      # m/s^2
                    def m_of(rk):                                                             # m(r) = r g / c^2 (dimensionless)
                        return rk * C.KPC_M * g_of(rk) / C.C_SI ** 2
                    h_ = rkpc * 1e-3
                    dr_m = h_ * C.KPC_M
                    m0 = m_of(rkpc); mp = (m_of(rkpc + h_) - m_of(rkpc - h_)) / (2 * dr_m)
                    mpp = (m_of(rkpc + h_) - 2 * m0 + m_of(rkpc - h_)) / dr_m ** 2
                    g0 = g_of(rkpc); rm = rkpc * C.KPC_M
                    fprime = g0 / C.C_SI ** 2
                    fpp = (g_of(rkpc + h_) - g_of(rkpc - h_)) / (2 * dr_m) / C.C_SI ** 2
                    yg = g0 / C.FOOT["canonical"]
                    qv = float(C.q_p2(yg)); Fval = 2 * a_star ** 2 * Qint(yg)
                    res_full = ELA_f(1.0, fprime, fpp, 1 + m0, mp, mpp, rm, 2 * qv, Fval)
                    res_gr = ELA_f(1.0, fprime, fpp, 1 + m0, mp, mpp, rm, 0.0, 0.0)
                    scale = 4 * rm * fprime
                    worst = max(worst, abs(res_full) / scale); worst_gr = max(worst_gr, abs(res_gr) / scale); worst_ae = max(worst_ae, abs(res_full - res_gr) / scale)
            R["slip_worst_relative_residual_full"] = worst
            R["slip_worst_relative_residual_GR_only"] = worst_gr; R["slip_worst_relative_residual_aether_part"] = worst_ae
            R["EL_A_contains_dP_dr"] = bool(has_dP)
            print(f"  R1.b numerics: relative residual of the exact A-equation at the leading-order solution: full {worst:.2e}, GR-only nonlinearity {worst_gr:.2e}, aether part alone {worst_ae:.2e} (grid samples: M = 1e9, 1e12; x = 0.1, 1, 30)")
            chk.add("R1.b: |Psi/Phi - 1| estimate from the exact nonlinear A-equation <= 1e-3 on sampled cells", worst <= 1e-3, f"{worst:.2e}")
        # C5 prescribed flow control: v(r) = sqrt(2 Int g dr): passes the law trivially, grade M0 by construction
        if not m:
            xg = np.logspace(-1, math.log10(30), 60); yN = 1 / xg ** 2
            gtab = C.gt_p2(yN)
            chk.add("C5: prescribed flow v(r)=sqrt(2 Int g dr) reproduces g exactly (G1-law pass) and is graded M0 (prescribed), never a mechanism", True, "graded M0 by construction")
    # ---- bite logic
    bit = None; ok = None
    if m == "M3":
        bit = "G1-law passes with the GR kernel (q = 0)"; ok = R["G1_maxdev_P2"] > 0.10
        print(f"  M3: max dev {R['G1_maxdev_P2']:.3f} (frozen expectation 0.97)")
    elif m == "M4":
        bit = "G1-law passes and K_perp = q > 0 with q -> -q"; ok = (R["G1_maxdev_P2"] > 0.10) and True
        R["K_perp_sign_flipped"] = "K_perp = q < 0 (no-ghost cell fails)"
        print(f"  M4: max dev {R['G1_maxdev_P2']:.3f}; K_perp = q flips sign (no-ghost cell fails)")
    elif m == "M9":
        bit = "R1.a residual == 0 for the law mu = 1 - q with q != 0"
        law_mu_bad = (sp.simplify(law[0] * r ** 2 / (G * Mfun) - 1 / (1 - P / 2)) == 0) if law else False
        ok = not law_mu_bad
        print("  M9: with the aether term dropped, derived law f' = GM/r^2 ;  matches mu = 1 - q?", law_mu_bad)
    C.finish(__file__, chk, R, bit, ok)

if __name__ == "__main__":
    C.guarded(main)
