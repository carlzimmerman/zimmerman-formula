#!/usr/bin/env python3
"""CFG897: kappa door D1 -- the stiffness term's own vacuum on an expanding (FRW) background.

Criteria: FROZEN_CRITERIA.md (committed alone first, 4c7a17d27). Rules: CFG894 KAPPA_CAMPAIGN_RULES.md.

Question: if the covariant completion of CFG770's stiffness -(gamma/2)|grad P|^2 is evaluated on flat FRW with the only
isotropic background a vector can have (timelike, homogeneous P^mu), can its energy be the dark energy, and what kappa
would that imply?

Method: minisuperspace sympy (x0 = c t, lapse N, n space dimensions), full Euler-Lagrange derivatives,
eps = -a^-n dS/dN|_{N=1}, p = dS/da / (n a^(n-1))|_{N=1}. Numbers (H0, Omega_L) enter only at the very end.

Run:   OMP_NUM_THREADS=1 nice -n 10 python3 cfg897.py               -> cfg897.out, cfg897_results.json (exit 0 = checks pass)
       CFG897_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg897.py -> cfg897_MUTATE.out, cfg897_results_MUTATE.json
                                                                       (exit 1 = all teeth bite; 2 = a tooth failed: VOID)
kappa = 1/2 is FITTED. Not theory closed.
"""
import json
import math
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG897_MUTATE", "0") == "1"
OUT = os.path.join(HERE, "cfg897_MUTATE.out" if MUTATE else "cfg897.out")
JSN = os.path.join(HERE, "cfg897_results_MUTATE.json" if MUTATE else "cfg897_results.json")

LINES = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LINES.append(s)


CHECKS = {}


def check(name, ok, detail=""):
    CHECKS[name] = {"pass": bool(ok), "detail": str(detail)}
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")


tau = sp.Symbol("tau", real=True)          # x0 = c t
gam = sp.Symbol("gamma", real=True)        # stiffness constant (sign kept free; gamma > 0 is the record's sign)
h, hp, hpp, hppp = sp.symbols("h hp hpp hppp", real=True)   # h = a'/a = H/c and its tau-derivatives
f0, fp, fpp = sp.symbols("f fp fpp", real=True)              # proper norm |P| and its tau-derivatives
xi, zeta = sp.symbols("xi zeta", real=True)


# ----------------------------------------------------------------------------------------------------------------------
# geometry
# ----------------------------------------------------------------------------------------------------------------------
def frw(n):
    a = sp.Function("a")(tau)
    N = sp.Function("N")(tau)
    xs = sp.symbols(f"x1:{n + 1}", real=True)
    X = [tau] + list(xs)
    D = n + 1
    gdiag = [-N**2] + [a**2] * n
    gidiag = [1 / gg for gg in gdiag]
    Gam = [[[sp.S(0)] * D for _ in range(D)] for _ in range(D)]
    for l in range(D):
        for m in range(D):
            for nu in range(D):
                # diagonal metric: Gam^l_{m nu} = 1/2 g^{ll} (d_m g_{l nu} + d_nu g_{l m} - d_l g_{m nu})
                val = 0
                if l == nu:
                    val += sp.diff(gdiag[l], X[m])
                if l == m:
                    val += sp.diff(gdiag[l], X[nu])
                if m == nu:
                    val -= sp.diff(gdiag[m], X[l])
                Gam[l][m][nu] = sp.cancel(gidiag[l] * val / 2)
    Ric = sp.zeros(D)
    for m in range(D):
        for nn in range(D):
            e = 0
            for l in range(D):
                e += sp.diff(Gam[l][m][nn], X[l]) - sp.diff(Gam[l][m][l], X[nn])
                for s in range(D):
                    e += Gam[l][l][s] * Gam[s][m][nn] - Gam[l][nn][s] * Gam[s][m][l]
            Ric[m, nn] = sp.cancel(e)
    Rs = sp.cancel(sum(gidiag[m] * Ric[m, m] for m in range(D)))
    return dict(n=n, a=a, N=N, X=X, D=D, g=gdiag, gi=gidiag, Gam=Gam, Ric=Ric, R=Rs, sqrtg=N * a**n)


def vector_scalars(G, P0):
    """Scalars of a vector with contravariant components P^mu = (P0, 0, ..., 0)."""
    D, g, gi, Gam, X = G["D"], G["g"], G["gi"], G["Gam"], G["X"]
    Pu = [P0] + [sp.S(0)] * (D - 1)
    Pl = [g[m] * Pu[m] for m in range(D)]
    DP = [[sp.diff(Pl[nn], X[m]) - sum(Gam[l][m][nn] * Pl[l] for l in range(D)) for nn in range(D)] for m in range(D)]
    Sa = sum(gi[m] * gi[nn] * DP[m][nn] ** 2 for m in range(D) for nn in range(D))
    Se = sum(gi[m] * gi[nn] * DP[m][nn] * DP[nn][m] for m in range(D) for nn in range(D))
    Theta = sum(gi[m] * DP[m][m] for m in range(D))
    F = [[sp.diff(Pl[nn], X[m]) - sp.diff(Pl[m], X[nn]) for nn in range(D)] for m in range(D)]
    Sc = sum(gi[m] * gi[nn] * F[m][nn] ** 2 for m in range(D) for nn in range(D))
    SRic = sum(G["Ric"][m, nn] * Pu[m] * Pu[nn] for m in range(D) for nn in range(D))
    P2 = sum(Pl[m] * Pu[m] for m in range(D))
    SR = G["R"] * P2
    return dict(Sa=Sa, Sb=Theta**2, Sc=Sc, Se=Se, SRic=SRic, SR=SR, P2=P2, Theta=Theta)


def EL(Lag, q, kmax=4):
    """Euler-Lagrange derivative of a tau-density Lag w.r.t. the function q(tau) (derivatives up to kmax)."""
    res = sp.diff(Lag, q)
    for k in range(1, kmax + 1):
        dq = q.diff(tau, k)
        term = sp.diff(Lag, dq)
        if term != 0:
            res += (-1) ** k * sp.diff(term, tau, k)
    return res


def at_N1(expr, G):
    N = G["N"]
    for k in (4, 3, 2, 1):
        expr = expr.subs(N.diff(tau, k), 0)
    return expr.subs(N, 1)


def to_h(expr, G, ffun=None, fixed_norm=True):
    a = G["a"]
    rep = [(a.diff(tau, 4), (hppp + 4 * h * hpp + 3 * hp**2 + 6 * h**2 * hp + h**4) * a),
           (a.diff(tau, 3), (hpp + 3 * h * hp + h**3) * a),
           (a.diff(tau, 2), (hp + h**2) * a),
           (a.diff(tau, 1), h * a)]
    for old, new in rep:
        expr = expr.subs(old, new)
    if ffun is not None:
        if fixed_norm:
            for k in (4, 3, 2, 1):
                expr = expr.subs(ffun.diff(tau, k), 0)
            expr = expr.subs(ffun, f0)
        else:
            for k, s in ((2, fpp), (1, fp)):
                expr = expr.subs(ffun.diff(tau, k), s)
            expr = expr.subs(ffun, f0)
    return sp.simplify(sp.expand(expr))


def eps_p(Lag_density, G):
    """Lag_density = sqrt(-g) * L (tau density). Returns (eps, p) at N = 1 as functions of a(tau)."""
    n, a = G["n"], G["a"]
    EN = EL(Lag_density, G["N"])
    Ea = EL(Lag_density, a)
    eps = sp.simplify(at_N1(-EN / a**n, G))
    p = sp.simplify(at_N1(Ea / (n * a ** (n - 1)), G))
    return eps, p


def conservation_residual(eps, p, G):
    a = G["a"]
    return sp.simplify(sp.diff(eps, tau) + G["n"] * (a.diff(tau) / a) * (eps + p))


# ----------------------------------------------------------------------------------------------------------------------
# the FRW computation for one n (and one gamma)
# ----------------------------------------------------------------------------------------------------------------------
def frw_block(n, gval, verbose=True):
    G = frw(n)
    a, N = G["a"], G["N"]
    f = sp.Function("f")(tau)
    S1 = vector_scalars(G, f / N)            # V1: proper norm held fixed
    sq = G["sqrtg"]
    struct = {
        "a": -(gval / 2) * S1["Sa"],
        "b": -(gval / 2) * S1["Sb"],
        "c": -(gval / 4) * S1["Sc"],
        "e": -(gval / 2) * S1["Se"],
        "Ric": -(gval / 2) * S1["SRic"],
        "R": -(gval / 2) * S1["SR"],
    }
    res = {"n": n, "G": G, "f": f, "S1": S1, "struct": struct, "fixed": {}, "free": {}}
    for k, L in struct.items():
        eps, p = eps_p(sq * L, G)
        res["free"][k] = (eps, p)
        eF = to_h(eps, G, f, fixed_norm=True)
        pF = to_h(p, G, f, fixed_norm=True)
        # A defined by eps = -A * gamma * h^2 * f^2  (fixed norm); gamma here is the symbol, so a mutated gval moves A
        A = sp.simplify(-eF / (gam * h**2 * f0**2))
        res["fixed"][k] = {"eps": eF, "p": pF, "A": A}
    return res


# ----------------------------------------------------------------------------------------------------------------------
# matching and numbers
# ----------------------------------------------------------------------------------------------------------------------
Gs, cs, rhos, Ls, kap, OmH, Asym, hbar = sp.symbols("G c rho_DE Lstar kappa Omega_H A hbar", positive=True)
a0s = sp.Symbol("a0", positive=True)


def matching(A_abs, sat=1, Kfac=1):
    """|eps_s| = A gamma phi^2 H^2 / c^2 = rho_DE c^2 with gamma = K L*^2/2, K phi = sat*a0, H^2 = 8 pi G rho/(3 Omega_H).
    Returns (a0_needed, kappa_needed) symbolic."""
    K = Kfac * 4 * sp.pi * Gs
    gamma_ = K * Ls**2 / 2
    phi = sat * a0s / K
    H2 = 8 * sp.pi * Gs * rhos / (3 * OmH)
    eps_s = A_abs * gamma_ * phi**2 * H2 / cs**2
    sol = sp.solve(sp.Eq(eps_s, rhos * cs**2), a0s)
    sol = [s for s in sol if s.is_positive is not False]
    a0n = sp.simplify(sol[0])
    kn = sp.simplify(a0n / (cs * sp.sqrt(Gs * rhos)))
    return a0n, kn, sp.simplify(eps_s)


# SI constants (end conversion only)
G_SI = 6.67430e-11
C_SI = 299792458.0
PC = 3.0856775814913673e16
MPC = 1e6 * PC
H0_SI = 67.4e3 / MPC
OML = 0.685
RHO_CRIT = 3 * H0_SI**2 / (8 * math.pi * G_SI)
RHO_DE = OML * RHO_CRIT
L_DE = C_SI / math.sqrt(G_SI * RHO_DE)
R_H0 = C_SI / H0_SI
WDATA_DE = (0.227, 0.607)
WDATA_CRIT = (0.189, 0.501)
LSTARS_PC = [5.75, 24.0, 100.0, 1000.0]


def num(expr, subsd):
    return float(sp.N(expr.subs(subsd)))


# ----------------------------------------------------------------------------------------------------------------------
def main_normal():
    say("CFG897: kappa door D1 -- the stiffness term's own vacuum on flat FRW (timelike homogeneous P)")
    say("kappa = 1/2 is FITTED (kappa_L 0.417 +- 0.095, CFG493 -- quoted, not used). Footings never pooled. Not theory closed.")
    say("")

    # ---------------- I1 self-grep
    say("== I1: self-grep for forbidden constants")
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    forb = ["9.36" + "e-11", "9.3603" + "e-11", "1.13" + "e-10", "1.1312" + "e-10", "1.2" + "e-10", "0.4" + "17",
            "0.4" + "5", "0.4" + "65", "0.5" + "3", "0.5" + "5", "0.5" + "51", "5.78" + "88", "0.17" + "27"]
    hits = []
    for v in forb:
        pat = r"(?<![\d.])" + re.escape(v) + r"(?![\d])"
        for ln, line in enumerate(src.splitlines(), 1):
            if re.search(pat, line):
                hits.append((v, ln))
    # the docstring quotes the measured kappa as a standing fact (not used); allow exactly that one quoted occurrence
    allowed = [(v, ln) for (v, ln) in hits if "quoted, not used" in src.splitlines()[ln - 1]]
    bad = [x for x in hits if x not in allowed]
    check("I1 no forbidden constants used", len(bad) == 0, f"hits outside the quoted standing-fact line: {bad}")

    # ---------------- K1 scalar sanity
    say("")
    say("== K1: scalar-field sanity of the eps/p extraction (n = 3)")
    G3 = frw(3)
    chi = sp.Function("chi")(tau)
    V = sp.Function("V")
    Ls_ = G3["sqrtg"] * (sp.Rational(1, 2) * chi.diff(tau) ** 2 / G3["N"] ** 2 - V(chi))
    e_, p_ = eps_p(Ls_, G3)
    ok = sp.simplify(e_ - (chi.diff(tau) ** 2 / 2 + V(chi))) == 0 and sp.simplify(p_ - (chi.diff(tau) ** 2 / 2 - V(chi))) == 0
    check("K1 scalar eps = chi'^2/2 + V, p = chi'^2/2 - V", ok, f"eps = {e_}, p = {p_}")

    # ---------------- K2 static flat limit
    say("")
    say("== K2: static flat limit (Minkowski, spatial P(x,y,z))")
    xx = sp.symbols("x y z", real=True)
    Pf = [sp.Function(f"P{i}")(*xx) for i in range(3)]
    dP = [[sp.diff(Pf[j], xx[i]) for j in range(3)] for i in range(3)]
    Sa_f = sum(dP[i][j] ** 2 for i in range(3) for j in range(3))
    Sb_f = sum(dP[i][i] for i in range(3)) ** 2
    Sc_half = sp.Rational(1, 2) * sum((dP[i][j] - dP[j][i]) ** 2 for i in range(3) for j in range(3))
    diff_ = sp.expand(Sa_f - Sc_half - Sb_f)
    ELs = []
    for j in range(3):
        e = sp.diff(diff_, Pf[j])
        for i in range(3):
            e -= sp.diff(sp.diff(diff_, sp.Derivative(Pf[j], xx[i])), xx[i])
        ELs.append(sp.simplify(e))
    check("K2 (a)_static = (c)_static + (b)_static + total derivative", all(e == 0 for e in ELs), f"EL of difference = {ELs}")
    chi3 = sp.Function("chi")(*xx)
    Pgrad = [sp.diff(chi3, v) for v in xx]
    Fgrad = sum((sp.diff(Pgrad[j], xx[i]) - sp.diff(Pgrad[i], xx[j])) ** 2 for i in range(3) for j in range(3))
    check("K2b Maxwell form vanishes on curl-free P (cannot stiffen longitudinal modes)", sp.simplify(Fgrad) == 0,
          "F_ij(grad chi) = 0; static energy of (a) = +(gamma/2) sum (d_i P_j)^2 >= 0 for gamma > 0")

    # ---------------- FRW block n = 3
    say("")
    say("== FRW, n = 3 (d = 4), V1: proper norm f = |P| held fixed; units x0 = c t, h = H/c")
    B = frw_block(3, gam)
    G, f = B["G"], B["f"]
    labels = {"a": "(a) -(g/2) D_mu P_nu D^mu P^nu", "b": "(b) -(g/2)(D.P)^2", "c": "(c) -(g/4) F^2",
              "e": "(e) -(g/2) D_mu P_nu D^nu P^mu", "Ric": "-(g/2) R_mn P^m P^n", "R": "-(g/2) R P_m P^m"}
    for k in ["a", "b", "c", "e", "Ric", "R"]:
        d = B["fixed"][k]
        say(f"  {labels[k]:36s}: eps = {d['eps']},   p = {d['p']},   A = {d['A']}")
    # general (time-dependent norm) energies for (a), (b)
    epsa_free = to_h(B["free"]["a"][0], G, f, fixed_norm=False)
    epsb_free = to_h(B["free"]["b"][0], G, f, fixed_norm=False)
    say(f"  any history f(tau):  eps_a = {sp.factor(epsa_free)}   eps_b = {sp.factor(epsb_free)}")
    ok_a = sp.simplify(epsa_free + gam / 2 * (fp**2 + 3 * h**2 * f0**2)) == 0
    ok_b = sp.simplify(epsb_free + gam / 2 * (fp + 3 * h * f0) ** 2) == 0
    check("FRW eps_a = -(g/2)(f'^2 + 3h^2 f^2), eps_b = -(g/2)(f' + 3hf)^2 (negative semi-definite for g > 0)", ok_a and ok_b,
          "hand estimate reproduced")
    check("FRW eps_c = p_c = 0 identically (F = 0 on the homogeneous ansatz)",
          B["fixed"]["c"]["eps"] == 0 and B["fixed"]["c"]["p"] == 0 and sp.simplify(B["free"]["c"][0]) == 0, "IDENTITY")

    # w at fixed norm
    wa = sp.simplify(B["fixed"]["a"]["p"] / B["fixed"]["a"]["eps"])
    wb = sp.simplify(B["fixed"]["b"]["p"] / B["fixed"]["b"]["eps"])
    wtot = -1 - sp.Rational(2, 3) * hp / h**2
    check("fixed norm: w_a = w_b = -1 - 2h'/(3h^2) = w_total (an H^2 term: renormalises G, never a separate Lambda)",
          sp.simplify(wa - wtot) == 0 and sp.simplify(wb - wtot) == 0, f"w_a = {wa}, w_b = {wb}")

    # ---------------- K3 covariant identity
    say("")
    say("== K3: (a) - (1/2)F^2 - (b) + Ric(P,P) and (e) - (b) + Ric(P,P) are total derivatives (general N, a, f)")
    S1 = B["S1"]
    sq = G["sqrtg"]
    for nm, comb in [("(a)-F^2/2-(b)+Ric", S1["Sa"] - S1["Sc"] / 2 - S1["Sb"] + S1["SRic"]),
                     ("(e)-(b)+Ric", S1["Se"] - S1["Sb"] + S1["SRic"])]:
        Ld = sq * comb
        r = [sp.simplify(EL(Ld, q)) for q in (G["N"], G["a"], f)]
        check(f"K3 {nm} total derivative", all(x == 0 for x in r), f"EL_N, EL_a, EL_f = {r}")

    # ---------------- K4 conservation
    say("")
    say("== K4: conservation eps' + n h (eps + p) = 0")
    for k in ["a", "b", "e", "Ric", "R"]:
        eps, p = B["free"][k]
        epsF = eps
        pF = p
        for kk in (4, 3, 2, 1):
            epsF = epsF.subs(f.diff(tau, kk), 0)
            pF = pF.subs(f.diff(tau, kk), 0)
        epsF = epsF.subs(f, f0)
        pF = pF.subs(f, f0)
        r = conservation_residual(epsF, pF, G)
        check(f"K4 fixed norm, {k}", r == 0, f"residual = {r}")
    # on-shell (no constraint): solve the f EOM of the stiffness term alone
    onshell = {}
    for k in ["a", "b"]:
        Lk = sq * B["struct"][k]
        Ef = sp.simplify(at_N1(EL(Lk, f), G))
        sol = sp.solve(Ef, f.diff(tau, 2))
        eps, p = B["free"][k]
        r = conservation_residual(eps, p, G)
        r = sp.simplify(r.subs(f.diff(tau, 2), sol[0]))
        check(f"K4 on the stiffness EOM, {k}", r == 0, f"f'' = {to_h(sol[0], G, f, fixed_norm=False)}, residual = {r}")
        onshell[k] = sol[0]

    # ---------------- N4: free branches
    say("")
    say("== N4: no constraint, no potential")
    Cc = sp.Symbol("C", real=True)
    # (b): first integral Theta = f' + 3 h f = C (N = 1)
    epsb, pb = B["free"]["b"]
    epsb_h = to_h(epsb, G, f, fixed_norm=False)
    pb_h = to_h(pb, G, f, fixed_norm=False)
    sub_fp = C_minus = Cc - 3 * h * f0
    sub_fpp = -3 * hp * f0 - 3 * h * C_minus
    epsC = sp.simplify(epsb_h.subs(fpp, sub_fpp).subs(fp, sub_fp))
    pC = sp.simplify(pb_h.subs(fpp, sub_fpp).subs(fp, sub_fp))
    # EOM of (b) at N=1 in h-form: check Theta' = 0 is the EOM
    Efb = to_h(at_N1(EL(sq * B["struct"]["b"], f), G), G, f, fixed_norm=False)
    Theta_p = fpp + 3 * hp * f0 + 3 * h * fp
    eom_is_thetap = sp.simplify(Efb / G["a"] ** 3 - gam * Theta_p) == 0 or sp.simplify(Efb - gam * Theta_p * G["a"] ** 3) == 0
    check("N4 (b): EOM is d/dtau(div P) = 0, so div P = C; eps = -(g/2)C^2, p = +(g/2)C^2, w = -1",
          eom_is_thetap and sp.simplify(epsC + gam * Cc**2 / 2) == 0 and sp.simplify(pC - gam * Cc**2 / 2) == 0,
          f"eps = {epsC}, p = {pC}: negative (AdS sign) for g > 0 and C is a free integration constant -> CONDITION")
    # (a): de Sitter exponent of f'' + 3 h f' - 3 h^2 f = 0
    lam = sp.Symbol("lam")
    fa_sol = to_h(onshell["a"], G, f, fixed_norm=False)
    say(f"  (a) free EOM: f'' = {fa_sol}")
    roots = sp.solve(sp.Eq(lam**2 * h**2, fa_sol.subs({fp: lam * h * f0, hp: 0}) / f0), lam)
    roots = [sp.nsimplify(r) for r in roots]
    say(f"  (a) de Sitter modes f ~ exp(lam h tau), lam = {roots} = {[float(r) for r in roots]}")
    say("      the growing mode makes eps_a = -(g/2)(lam^2 + 3) h^2 f^2 grow without bound and negative: no constant w = -1 energy")

    # ---------------- K5 held-fixed convention
    say("")
    say("== K5: V2 (P^0 fixed) and V3 (P_0 fixed) with the norm constraint reproduce V1")
    phi0 = sp.Symbol("phi0", positive=True)
    lamf = sp.Symbol("lambda_mult", real=True)
    for nm, (P0expr_fn, Cexpr_fn) in {
        "V2": (lambda q: q, lambda q: -G["N"] ** 2 * q**2 + phi0**2),
        "V3": (lambda q: q / G["N"] ** 2, lambda q: -q**2 / G["N"] ** 2 + phi0**2),
    }.items():
        q = sp.Function("q")(tau)
        Sv = vector_scalars(G, P0expr_fn(q))
        for k, coeff, key in [("a", -gam / 2, "Sa"), ("b", -gam / 2, "Sb")]:
            Lstiff = sq * coeff * Sv[key]
            Lcon = sq * lamf * Cexpr_fn(q)
            Eq_ = at_N1(EL(Lstiff + Lcon, q), G)
            pt = [(q.diff(tau, 2), 0), (q.diff(tau, 1), 0)]
            Eq_ = Eq_.subs(pt).subs(q, phi0)
            lam_sol = sp.solve(Eq_, lamf)[0]
            EN = at_N1(EL(Lstiff + Lcon, G["N"]), G).subs(pt).subs(q, phi0)
            eps_tot = to_h(-EN.subs(lamf, lam_sol) / G["a"] ** 3, G)
            EN0 = at_N1(EL(Lstiff, G["N"]), G).subs(pt).subs(q, phi0)
            eps_naive = to_h(-EN0 / G["a"] ** 3, G)
            target = B["fixed"][k]["eps"].subs(f0, phi0)
            check(f"K5 {nm} {k} with constraint = V1", sp.simplify(eps_tot - target) == 0,
                  f"eps_tot = {eps_tot}; naive (off-shell, not used) = {eps_naive}")

    # ---------------- K6 general d
    say("")
    say("== K6: general dimension (fixed norm): A_a = n/2, A_b = n^2/2, A_c = 0, A_Ric, A_R")
    Atab = {}
    allok = True
    for n in (2, 3, 4, 5):
        Bn = B if n == 3 else frw_block(n, gam, verbose=False)
        Aa, Ab, Ac = Bn["fixed"]["a"]["A"], Bn["fixed"]["b"]["A"], Bn["fixed"]["c"]["A"]
        ARic, AR = Bn["fixed"]["Ric"]["A"], Bn["fixed"]["R"]["A"]
        Atab[n] = {"A_a": str(Aa), "A_b": str(Ab), "A_c": str(Ac), "A_Ric": str(ARic), "A_R": str(AR)}
        ok = (sp.simplify(Aa - sp.Rational(n, 2)) == 0 and sp.simplify(Ab - sp.Rational(n * n, 2)) == 0
              and Bn["fixed"]["c"]["eps"] == 0)
        allok = allok and ok
        say(f"  n = {n} (d = {n + 1}): A_a = {Aa}, A_b = {Ab}, eps_c = {Bn['fixed']['c']['eps']}, A_Ric = {ARic}, A_R = {AR}")
    check("K6 A_a = n/2, A_b = n^2/2, eps_c = 0 for n = 2..5 (sign negative in every d)", allok, "")

    # ---------------- K7 Einstein-aether cross-check
    say("")
    say("== K7: Einstein-aether form eps = -3 alpha m^2 h^2, p = alpha m^2 (2h' + 3h^2), alpha = b1 + 3 b2 + b3")
    for k, alpha in [("a", gam / 2), ("b", 3 * gam / 2), ("e", gam / 2)]:
        d = B["fixed"][k]
        ok = (sp.simplify(d["eps"] + 3 * alpha * f0**2 * h**2) == 0
              and sp.simplify(d["p"] - alpha * f0**2 * (2 * hp + 3 * h**2)) == 0)
        check(f"K7 {k} (alpha = {alpha})", ok, "consistency with the published fixed-norm form (not an input)")

    # ---------------- general family (G)
    say("")
    say("== Family (G): -(g/2)[F^2/2 + (D.P)^2 + xi Ric(P,P) + zeta R P^2] (exact static limit for every xi, zeta)")
    # struct 'c' is -(g/4)F^2 = -(g/2)(F^2/2), so its A enters with weight 1 (it is zero on the ansatz anyway)
    A_G = sp.simplify(B["fixed"]["c"]["A"] + B["fixed"]["b"]["A"] + xi * B["fixed"]["Ric"]["A"] + zeta * B["fixed"]["R"]["A"])
    say(f"  fixed norm: eps = -A gamma h^2 f^2 with A(xi, zeta) = {A_G}")
    check("(G) at xi = -1, zeta = 0 reproduces (a)", sp.simplify(A_G.subs({xi: -1, zeta: 0}) - B["fixed"]["a"]["A"]) == 0,
          f"A(-1, 0) = {A_G.subs({xi: -1, zeta: 0})}")
    say("  positive energy needs A < 0, i.e. xi + zeta < -3/2: possible with O(1) non-minimal couplings (sign is then a choice)")
    A_nat_max = max(abs(A_G.subs({xi: s1 * 10, zeta: s2 * 10})) for s1 in (-1, 1) for s2 in (-1, 1))
    A_pos_max = abs(A_G.subs({xi: -10, zeta: -10}))
    say(f"  largest |A| with |xi|, |zeta| <= 10: {A_nat_max} (positive-energy branch: |A| = {A_pos_max} at xi = zeta = -10)")

    # ---------------- matching, symbolic (I2, I3, I4, I5, I7, I8)
    say("")
    say("== Matching |eps_s| = rho_DE c^2 at N1 (K phi = a0), symbolic")
    a0n, kn, eps_sym = matching(Asym)
    say(f"  eps_s(a0) = {eps_sym}")
    say(f"  a0_needed = {a0n}      kappa_needed = {kn}")
    deps = {str(X): sp.simplify(sp.diff(sp.log(kn), X) * X) for X in (Gs, cs, rhos, Ls, hbar)}
    check("I2 kappa_needed depends on L* (TRADE), hbar-free",
          deps["Lstar"] != 0 and deps["hbar"] == 0, f"d ln kappa / d ln X = {deps}")
    lam_, mu_, nu_ = sp.symbols("lambda_s mu_s nu_s", positive=True)
    ratio = sp.simplify(kn.subs({Gs: lam_ * Gs, rhos: mu_ * rhos, cs: nu_ * cs}, simultaneous=True) / kn)
    check("I3 scaling at fixed L*: kappa_needed is NOT invariant (pure number only if L* ~ c/sqrt(G rho))",
          sp.simplify(ratio - 1) != 0, f"kappa(lambda G, mu rho, nu c)/kappa = {ratio}")
    # I4 rename test
    frac = sp.simplify(eps_sym.subs(a0s, kap * cs * sp.sqrt(Gs * rhos)) / (rhos * cs**2))
    frac04 = frac.subs(kap, sp.Rational(2, 5))
    check("I4 law kappa -> 0.4: a0_needed and kappa_needed do not move; the fraction eps_s/rho c^2 does",
          (not a0n.has(kap)) and (not kn.has(kap)) and frac.has(kap),
          f"fraction = {frac} (at kappa = 0.4: {sp.simplify(frac04)})")
    check("I5 no Friedmann tautology: kappa_needed depends on L*, not Z^2 = 32 pi/3", kn.has(Ls), "")
    say(f"  I5 note: at Omega_H = 1 the condition fixes a0 = {sp.simplify(a0n.subs(OmH, 1))} with rho_DE cancelled: it is the")
    say("     degenerate point of the renormalised Friedmann equation (G_cosmo -> infinity), not a determination of a0 by rho_DE")
    check("I7 hbar-power 0", not kn.has(hbar), "classical route")
    pref = sp.simplify(kn**2 * Ls**2 * Gs * rhos / cs**2)
    pw = sp.Poly(sp.simplify(pref * Asym / OmH), sp.pi).degree() if pref.has(sp.pi) else 0
    check("I8 pi-weight of kappa_needed^2 prefactor", pw == 0, f"prefactor = {pref} (pi-weight {pw}; TRADE class)")
    check("I6 declared footing rho_DE; rho_crit reported as kappa_crit = kappa_L sqrt(Omega_L), never pooled", True, "")

    # second prediction
    deltaG = sp.simplify(Asym / 3 * (a0s * Ls / cs**2) ** 2)
    say(f"  S4: fixed-norm stiffness renormalises Friedmann: G_cosmo/G_N = 1/(1 + delta), delta = {deltaG}")
    # check delta from the Friedmann bookkeeping: H^2 (1 + 8 pi G A gamma phi^2/(3 c^4)) = (8 pi G/3c^2) eps_rest
    K_ = 4 * sp.pi * Gs
    dchk = sp.simplify(8 * sp.pi * Gs * Asym * (K_ * Ls**2 / 2) * (a0s / K_) ** 2 / (3 * cs**4) - deltaG)
    check("K8a delta = 8 pi G A gamma phi^2/(3 c^4) at K phi = a0", dchk == 0, "")

    # ---------------- K8 dimensions
    say("")
    say("== K8: dimensions (SI base units)")
    m_, kg_, s_ = sp.symbols("m kg s", positive=True)
    dims = {Gs: m_**3 / (kg_ * s_**2), cs: m_ / s_, rhos: kg_ / m_**3, Ls: m_, OmH: 1, Asym: 1}
    # units only: strip the pure-number coefficient (runs 1-2 compared sqrt(3) and 1/3 to 1 -- a check-code bug, disclosed)
    da0 = sp.simplify(a0n.subs(dims)).as_independent(m_, kg_, s_, as_Add=False)[1]
    dk = sp.simplify(kn.subs(dims)).as_independent(m_, kg_, s_, as_Add=False)[1]
    dd = sp.simplify(deltaG.subs({**dims, a0s: m_ / s_**2})).as_independent(m_, kg_, s_, as_Add=False)[1]
    check("K8 a0_needed [m s^-2], kappa_needed and delta dimensionless", sp.simplify(da0 / (m_ / s_**2)) == 1 and dk == 1 and dd == 1,
          f"[a0] = {da0}, [kappa] = {dk}, [delta] = {dd}")

    # ---------------- numbers (end conversion only)
    say("")
    say("== Numbers (end conversion only: H0 = 67.4 km/s/Mpc, Omega_L = 0.685)")
    say(f"  rho_DE = {RHO_DE:.4e} kg/m^3, l_DE = c/sqrt(G rho_DE) = {L_DE:.4e} m = {L_DE / MPC / 1e3:.2f} Gpc, c/H0 = {R_H0 / MPC / 1e3:.2f} Gpc")
    variants = [("(a) minimal", float(B["fixed"]["a"]["A"]), "NO SOLUTION (sign)"),
                ("(b) minimal", float(B["fixed"]["b"]["A"]), "NO SOLUTION (sign)"),
                ("(G) xi=zeta=-10 (positive energy, most favourable O(1))", float(A_G.subs({xi: -10, zeta: -10})), "")]
    table = []
    for name, Aval, _ in variants:
        for Om in (1.0, OML):
            for Lpc in LSTARS_PC:
                L = Lpc * PC
                sd = {Asym: abs(Aval), OmH: Om, Gs: G_SI, cs: C_SI, rhos: RHO_DE, Ls: L}
                kL = num(kn, sd)
                a0v = num(a0n, sd)
                row = {"variant": name, "A": Aval, "Omega_H": Om, "Lstar_pc": Lpc, "kappa_L_abs": kL,
                       "kappa_crit_abs": kL * math.sqrt(OML), "a0_needed": a0v, "sign_ok": Aval < 0}
                table.append(row)
    say(f"  {'variant':58s} {'Om_H':>5s} {'L*/pc':>7s} {'|kappa_L|':>10s} {'|kappa_crit|':>12s} {'a0_need m/s2':>12s}")
    for r in table:
        say(f"  {r['variant']:58s} {r['Omega_H']:5.3f} {r['Lstar_pc']:7.2f} {r['kappa_L_abs']:10.3e} {r['kappa_crit_abs']:12.3e} {r['a0_needed']:12.3e}")
    kmin = min(r["kappa_L_abs"] for r in table if r["Lstar_pc"] >= 24.0)
    kmin_crit = min(r["kappa_crit_abs"] for r in table if r["Lstar_pc"] >= 24.0)
    say(f"  smallest |kappa| over all variants with L* in [24 pc, 1 kpc]: {kmin:.3e} (rho_DE), {kmin_crit:.3e} (rho_crit)")
    say(f"  W_data = {WDATA_DE} (rho_DE), {WDATA_CRIT} (rho_crit)")

    # L* needed for kappa at the W_data edges
    say("  L*_needed for kappa at the W_data edges (rho_DE footing):")
    Lneed = []
    for name, Aval, _ in variants:
        for Om in (1.0, OML):
            for kv in WDATA_DE:
                Lval = math.sqrt(3 * Om / abs(Aval)) * L_DE / kv
                Lneed.append({"variant": name, "Omega_H": Om, "kappa": kv, "Lstar_needed_Gpc": Lval / MPC / 1e3})
                say(f"    {name:58s} Om_H {Om:5.3f} kappa {kv:5.3f}: L* = {Lval / MPC / 1e3:8.3f} Gpc ({Lval / R_H0:.2f} c/H0)")
    Lmin_Mpc = min(x["Lstar_needed_Gpc"] for x in Lneed) * 1e3
    say(f"  smallest L*_needed = {Lmin_Mpc:.1f} Mpc  (> 1 Mpc: every galaxy would be screened, CFG820 K1)")

    # required non-minimal coefficient
    say("  |A| required to put kappa in W_data (Omega_H = 1):")
    Areq = []
    for Lpc in (24.0, 1000.0):
        for kv in WDATA_DE:
            Ar = 3 * 1.0 * (L_DE / (Lpc * PC)) ** 2 / kv**2
            Areq.append({"Lstar_pc": Lpc, "kappa": kv, "A_required": Ar})
            say(f"    L* = {Lpc:6.1f} pc, kappa = {kv:5.3f}: |A| = {Ar:.3e}  (|xi + zeta| ~ {Ar / 3:.2e}; natural bound 20)")

    # delta (report only, at fitted kappa = 1/2 -- report only, not an input)
    say("  S4 delta = (A/3) kappa^2 (L*/l_DE)^2 at the fitted kappa = 1/2 (report only):")
    dtab = []
    for name, Aval, _ in variants[:2]:
        for Lpc in (24.0, 1000.0):
            dv = abs(Aval) / 3 * 0.25 * (Lpc * PC / L_DE) ** 2
            dtab.append({"variant": name, "Lstar_pc": Lpc, "delta": dv})
            say(f"    {name:12s} L* = {Lpc:6.1f} pc: |delta| = {dv:.2e}  (BBN/CMB sensitivity ~1e-1..1e-2): untestable, p_second ~ 1")
    say("  tuned positive branch (eps_s(today) = rho_DE c^2): eps_s ~ H^2 means G_cosmo/G_N = 1/(1 - Omega_L) = "
        f"{1 / (1 - OML):.2f} and no acceleration (an H^2 term only rescales G): EXCLUDED on equation of state as well")

    # ---------------- per-variant classes and overall label
    say("")
    say("== Per-variant classes (frozen rules, first that applies)")
    classes = {
        "(c) Maxwell, any normalisation": "IDENTITY (vanishing): F = 0 on the homogeneous ansatz",
        "N2 tether (P = 0 on FRW)": "IDENTITY (vanishing)",
        "N3 law vacuum (g_N = 0 => u = 0)": "IDENTITY (vanishing)",
        "N4 (b) free, div P = C": "CONDITION (free zero mode C); also negative energy",
        "N4 (a) free": "NO SOLUTION (sign; runaway, no constant energy)",
        "(a) fixed norm N1/N1b": "NO SOLUTION (sign); magnitude-only |kappa| >= %.2e" % min(
            r["kappa_L_abs"] for r in table if r["variant"].startswith("(a)") and r["Lstar_pc"] >= 24),
        "(b) fixed norm N1/N1b": "NO SOLUTION (sign); magnitude-only |kappa| >= %.2e" % min(
            r["kappa_L_abs"] for r in table if r["variant"].startswith("(b)") and r["Lstar_pc"] >= 24),
        "(G) O(1) non-minimal, positive branch": "MISS (TRADE, magnitude): kappa >= %.2e; L*_needed >= %.0f Mpc -> EXCLUDED" % (
            min(r["kappa_L_abs"] for r in table if r["variant"].startswith("(G)") and r["Lstar_pc"] >= 24), Lmin_Mpc),
    }
    for k, v in classes.items():
        say(f"  {k:42s}: {v}")
    any_consistent = any(WDATA_DE[0] <= r["kappa_L_abs"] <= WDATA_DE[1] for r in table
                         if r["Lstar_pc"] >= 24.0 and r["sign_ok"])
    void = not all(c["pass"] for c in CHECKS.values())
    label = "VOID" if void else ("CONSISTENT (not significant, TRADE)" if any_consistent else "CLOSURE")
    say("")
    say(f"OVERALL LABEL (frozen rule): {label}")
    say("  p_exact = 0 (TRADE form: kappa ~ c/(L* sqrt(G rho_DE)), exact 1/2 needs a horizon-scale L*); p_data = 0.")
    say("  kappa = 1/2 stays FITTED. Not theory closed.")
    npass = sum(c["pass"] for c in CHECKS.values())
    say(f"  checks: {npass}/{len(CHECKS)} PASS")

    out = {
        "lane": "CFG897", "door": "D1", "label": label, "checks": CHECKS,
        "fixed_norm_n3": {k: {"eps": str(v["eps"]), "p": str(v["p"]), "A": str(v["A"])} for k, v in B["fixed"].items()},
        "A_family_G": str(A_G), "A_by_dimension": Atab,
        "a0_needed": str(a0n), "kappa_needed": str(kn), "delta_G": str(deltaG),
        "numbers": table, "Lstar_needed": Lneed, "A_required": Areq, "delta_report": dtab,
        "classes": classes, "p_exact": 0.0, "p_data": 0.0,
        "end_constants": {"H0_km_s_Mpc": 67.4, "Omega_L": OML, "rho_DE": RHO_DE, "l_DE_m": L_DE},
    }
    return out, (0 if not void else 3)


# ----------------------------------------------------------------------------------------------------------------------
def main_mutate():
    say("CFG897 MUTATE run: five teeth; exit 1 iff all bite, 2 (VOID) if any does not")
    teeth = {}
    base = frw_block(3, gam)
    Aa0, Ab0 = base["fixed"]["a"]["A"], base["fixed"]["b"]["A"]
    a0n, kn, _ = matching(Asym)
    sd0 = {OmH: 1, Gs: G_SI, cs: C_SI, rhos: RHO_DE, Ls: 24 * PC}
    ka0 = num(kn, {**sd0, Asym: abs(float(Aa0))})
    kb0 = num(kn, {**sd0, Asym: abs(float(Ab0))})
    say(f"  baseline n=3: A_a = {Aa0}, A_b = {Ab0}; |kappa| at L* = 24 pc: (a) {ka0:.4e}, (b) {kb0:.4e}")

    # M1 gamma -> 0
    m1 = frw_block(3, sp.S(0))
    e1 = [m1["fixed"][k]["eps"] for k in ("a", "b")]
    bite = all(e == 0 for e in e1) and Aa0 != 0
    teeth["M1 gamma->0: every eps_s -> 0, no kappa"] = bite
    say(f"  M1 gamma -> 0: eps_a, eps_b = {e1} -> {'BITES' if bite else 'DOES NOT BITE'}")

    # M2 d 4 -> 5
    m2 = frw_block(4, gam)
    Aa2, Ab2 = m2["fixed"]["a"]["A"], m2["fixed"]["b"]["A"]
    ka2 = num(kn, {**sd0, Asym: abs(float(Aa2))})
    kb2 = num(kn, {**sd0, Asym: abs(float(Ab2))})
    bite = (sp.simplify(Aa2 - 2) == 0 and sp.simplify(Ab2 - 8) == 0 and abs(ka2 / ka0 - math.sqrt(3 / 4)) < 1e-12
            and abs(kb2 / kb0 - 0.75) < 1e-12)
    teeth["M2 d 4->5: A_a 3/2->2, A_b 9/2->8, kappa x sqrt(3/4), x 3/4"] = bite
    say(f"  M2 n = 4: A_a = {Aa2}, A_b = {Ab2}; kappa ratios {ka2 / ka0:.6f}, {kb2 / kb0:.6f} -> {'BITES' if bite else 'DOES NOT BITE'}")

    # M3 saturation at 2 a0
    _, kn3, eps3 = matching(Asym, sat=2)
    _, _, eps1 = matching(Asym, sat=1)
    r_eps = sp.simplify(eps3 / eps1)
    r_k = num(kn3, {**sd0, Asym: abs(float(Aa0))}) / ka0
    bite = r_eps == 4 and abs(r_k - 0.5) < 1e-12
    teeth["M3 saturation 2 a0: |eps| x4, kappa x1/2"] = bite
    say(f"  M3 K phi = 2 a0: eps ratio {r_eps}, kappa ratio {r_k:.6f} -> {'BITES' if bite else 'DOES NOT BITE'}")

    # M4 gamma -> -gamma
    m4 = frw_block(3, -gam)
    e4a = m4["fixed"]["a"]["eps"]
    e4b = m4["fixed"]["b"]["eps"]
    c4 = [sp.simplify(e / (gam * h**2 * f0**2)) for e in (e4a, e4b)]
    c0 = [sp.simplify(base["fixed"][k]["eps"] / (gam * h**2 * f0**2)) for k in ("a", "b")]
    pos = all(x.is_number and x > 0 for x in c4)
    base_neg = all(x.is_number and x < 0 for x in c0)
    # with positive energy the matching has a real solution of the same magnitude
    A4 = sp.simplify(-e4a / (gam * h**2 * f0**2))
    k4 = num(kn, {**sd0, Asym: abs(float(A4))})
    bite = bool(pos and base_neg and abs(k4 / ka0 - 1) < 1e-12)
    teeth["M4 gamma->-gamma: eps_a, eps_b > 0 (NO SOLUTION -> real kappa, same magnitude)"] = bite
    say(f"  M4 gamma -> -gamma: eps_a = {e4a}, eps_b = {e4b} (h, f real => positive): kappa {k4:.4e} -> {'BITES' if bite else 'DOES NOT BITE'}")

    # M5 K = 4 pi G -> 8 pi G
    _, kn5, eps5 = matching(Asym, Kfac=2)
    r_eps5 = sp.simplify(eps5 / eps1)
    r_k5 = num(kn5, {**sd0, Asym: abs(float(Aa0))}) / ka0
    bite = r_eps5 == sp.Rational(1, 2) and abs(r_k5 - math.sqrt(2)) < 1e-12
    teeth["M5 K 4piG->8piG: |eps| x1/2, kappa x sqrt2"] = bite
    say(f"  M5 K = 8 pi G: eps ratio {r_eps5}, kappa ratio {r_k5:.6f} -> {'BITES' if bite else 'DOES NOT BITE'}")

    allbite = all(teeth.values())
    say("")
    say(f"MUTATE: {sum(teeth.values())}/{len(teeth)} teeth bite -> {'exit 1 (by design)' if allbite else 'VOID (exit 2)'}")
    say("The overall label of the normal run is not changed by a MUTATE run.")
    return {"lane": "CFG897", "mode": "MUTATE", "teeth": teeth, "all_bite": allbite}, (1 if allbite else 2)


if __name__ == "__main__":
    if MUTATE:
        res, code = main_mutate()
    else:
        res, code = main_normal()
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(LINES) + "\n")
    with open(JSN, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=str)
    sys.exit(code)
