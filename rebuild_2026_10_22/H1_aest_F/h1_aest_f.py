#!/usr/bin/env python3
"""H1_aest_F: is there an F(Y, Q) in AeST's class that is healthy at Y = 0, keeps normal linear growth, gives the galactic
law on SPARC, keeps the stiffness-screened Solar System and respects BBN?  Criteria: FROZEN_CRITERIA.md (committed first).

External input (on disk, outside the repo, sha256 in covariant_push_2026_10_22/C2_aest_cosmology/PROVENANCE.md):
  SZ21 = arXiv:2007.00082 newRMONDLett.tex (eqs. NT_A_action, Jcal limits, Minkowski_action, lambda_s > 0 condition);
  VSZ  = arXiv:2304.05134 main.tex (eqs. Phi-Orig, Chi-Orig, def_f_general, mu_Simple, mu_Exp, mu_Hyp).
Read-only reuse: C5's linearisation (source slices exec'd, nothing written), AG4b's SPARC pipeline (copied verbatim),
C6's Route-F solver (imported).  kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed.

Run: OMP_NUM_THREADS=1 nice -n 15 python3 h1_aest_f.py          (H1_MUTATE=1 for the mutation run)
"""
import json
import math
import os
import resource
import sys
import time

import numpy as np
import sympy as sp

T0 = time.time()
MUT = os.environ.get("H1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUTF = open(os.path.join(HERE, f"h1_aest_f{TAG}.out"), "w")
RES = {"lane": "H1_aest_F", "mutate": MUT, "criteria": "FROZEN_CRITERIA.md"}
CHECKS = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUTF.write(s + "\n")
    OUTF.flush()


def check(kid, ok, value, thr):
    CHECKS.append({"id": kid, "pass": bool(ok), "value": str(value), "threshold": thr})
    P(f"{kid} {'PASS' if ok else 'FAIL'} {value} {thr}")


P(f"H1_aest_F  mutate={MUT}")
P("kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed.")

# ============================================================================ Part A: C5's linearisation (read-only exec)
C5 = os.path.join(REPO, "covariant_push_2026_10_22", "C5_health")
src = open(os.path.join(C5, "c5_health.py")).read()


def sl(a, b):
    i = src.index(a)
    return src[i:src.index(b, i)]


ns = {}
exec(compile("import sympy as sp\nimport math\nimport mpmath as mp\nSZSGN = 1\n"
             + sl("t, x, y, z = sp.symbols", "NAMES = [")
             + sl("def quad_matrix(", "log(f\"C5_health  mutate")
             + sl("KB, KK2, lam, Q0, Ls = sp.symbols", "Msz = sz_scalar()")
             + sl("def jordan_energy(", "EJ_aest = jordan_energy"), "c5_slices", "exec"), ns)
t, x, y, z, w, k = (ns[s] for s in ("t", "x", "y", "z", "w", "k"))
KB, KK2, lam, Q0, Ls = (ns[s] for s in ("KB", "KK2", "lam", "Q0", "Ls"))
quad_matrix, sz_lagrangian, jordan_energy = ns["quad_matrix"], ns["sz_lagrangian"], ns["jordan_energy"]
c5json = json.load(open(os.path.join(C5, "c5_health_results.json")))
loc = {"k": k, "K_B": KB, "K_2": KK2, "lambda_s": lam, "Q_0": Q0, "L_s": Ls}

I, eps = sp.symbols("I epsilon", real=True)
Psi, Phi, al, vp = [sp.Function(nm)(t, z) for nm in ("Psi", "Phi", "alpha", "varphi")]
hup = sp.diag(-2 * Psi, -2 * Phi, -2 * Phi, -2 * Phi)
A = [sp.diff(al, v) for v in (x, y, z)]
FIELDS = [Psi, Phi, al, vp]

# exact metric / unit aether to second order (g^00 = -1 + 2 Psi, g^ij = (1 + 2 Phi) delta, A_i = d_i alpha)
gu00 = -1 + 2 * eps * Psi
guij = 1 + 2 * eps * Phi
sqg = (1 - 2 * eps * Psi) ** sp.Rational(-1, 2) * (1 + 2 * eps * Phi) ** sp.Rational(-3, 2)
Ai = [eps * a for a in A]
A0low = -sp.sqrt((1 + guij * sum(a ** 2 for a in Ai)) / (-gu00))
dphi = [Q0 + eps * sp.diff(vp, t)] + [eps * sp.diff(vp, v) for v in (x, y, z)]
Aup = [gu00 * A0low] + [guij * a for a in Ai]
Qex = sum(Aup[m] * dphi[m] for m in range(4))
ISGN = -1 if MUT else 1
dL = sp.expand(2 * ISGN * I * sp.series(sqg * (Qex - Q0), eps, 0, 3).removeO().coeff(eps, 2))
P(f"  dust-background term 2I[sqrt(-g)(Q-Qbar)]^(2) = {sp.simplify(dL)}")

res_lin = {}
for stiff in (False, True):
    tagS = "with gamma_L" if stiff else "no gamma_L"
    L0 = sz_lagrangian(hup, A, vp, stiff)
    M0 = quad_matrix(L0, FIELDS, (t, z), {})
    EJ = jordan_energy(M0, w)[0]
    M = quad_matrix(L0 + dL, FIELDS, (t, z), {})
    W2, s_ = sp.symbols("W2 s")
    dp = sp.expand(M.det().subs(w, sp.sqrt(W2)))
    dps = sp.Poly(sp.expand(dp.subs({W2: s_ * W2, I: s_ * I})), s_)
    cs = dps.all_coeffs()[::-1]
    lead = next(c for c in cs if sp.simplify(c) != 0)
    G2 = sp.factor(-sp.solve(lead, W2)[0])            # Gamma^2 = -omega^2 at O(I)
    res_lin[stiff] = dict(EJ=EJ, G2=G2)
    P(f"  [{tagS}] Jordan energy E_J = {EJ}")
    P(f"  [{tagS}] dust growth rate Gamma^2 = {G2}")

# K1: reproduce C5's Jordan energies
ref = c5json["H10"]
d1 = sp.simplify(res_lin[False]["EJ"] - sp.sympify(ref["jordan_energy_AeST"][0], locals=loc))
d2 = sp.simplify(res_lin[True]["EJ"] - sp.sympify(ref["jordan_energy_AeST_plus_stiffness"][0], locals=loc))
check("K1", d1 == 0 and d2 == 0, f"E_J - C5 json: {d1}, {d2}", "both 0 (C5 H10 reproduced from C5's own source)")

# K2: E_J / Gamma^2 = -8 k^2 D^2 / (I Q0^3 N^2) (minus a square), Gamma^2(k->0) = I Q0 / 2, closed form at lambda=0, L*=0
k2ok, k2val = True, []
for stiff in (False, True):
    G2, EJ = res_lin[stiff]["G2"], res_lin[stiff]["EJ"]
    Nn, Dd = sp.fraction(sp.factor(G2 / (I * Q0 / 2)))
    ratio = sp.factor(sp.simplify(EJ / G2 * I * Q0 ** 3 * Nn ** 2 / (k ** 2 * Dd ** 2)))
    ir = sp.simplify(sp.limit(G2, k, 0) - I * Q0 / 2)
    ok = ratio.is_number and float(ratio) < 0 and ir == 0
    k2ok &= ok
    k2val.append(f"[{'gL' if stiff else 'no gL'}] E_J*I*Q0^3*N^2/(Gamma^2 k^2 D^2) = {ratio}; Gamma^2(0) - I Q0/2 = {ir}")
mu = sp.Symbol("mu", positive=True)
u = sp.Symbol("u", positive=True)
cf = sp.simplify((res_lin[False]["G2"] / (I * Q0 / 2)).subs(lam, 0).subs(KK2, mu ** 2 * (2 - KB) / (2 * Q0 ** 2)).subs(k, sp.sqrt(u) * mu)
                 - 1 / (1 + 2 * u / (2 - KB)))
k2ok &= cf == 0
check("K2", k2ok, "; ".join(k2val) + f"; closed form residual {cf}",
      "negative constant (E_J = -(pos) * Gamma^2 / I) both cases; Gamma^2(0) = I Q0/2 = 4 pi G rho; closed form 0")

# K3: Y = q^{mu nu} d phi d phi on the Y = 0 background has no O(1), O(eps) part; O(eps^2) = |grad phi + Q0 A|^2
gu = sp.diag(gu00, guij, guij, guij)
qup = sp.Matrix(4, 4, lambda m, n: gu[m, n] + Aup[m] * Aup[n])
Yex = sum(qup[m, n] * dphi[m] * dphi[n] for m in range(4) for n in range(4))
Ys = sp.series(Yex, eps, 0, 3).removeO()
y0, y1, y2 = (sp.simplify(Ys.coeff(eps, i)) for i in range(3))
V2 = sum((sp.diff(vp, v) + Q0 * a) ** 2 for v, a in zip((x, y, z), A))
y2r = sp.simplify(y2 - V2)
check("K3", y0 == 0 and y1 == 0 and y2r == 0, f"Y^(0) = {y0}, Y^(1) = {y1}, Y^(2) - |grad phi + Q0 A|^2 = {y2r}",
      "0, 0, 0 (F beyond linear in Y is >= cubic: health at Y = 0 sees F only via lambda_0 = F_Y(0)/(2-K_B))")

# numeric growth / band functions
mu_s = sp.Symbol("mu_s", positive=True)
subsK = {KK2: mu_s ** 2 * (2 - KB) / (2 * Q0 ** 2)}
G2n = {s_: sp.lambdify((k, lam, Ls, KB, mu_s, Q0), sp.simplify((res_lin[s_]["G2"] / (I * Q0 / 2)).subs(subsK)), "numpy")
       for s_ in (False, True)}
EJn = {s_: sp.lambdify((k, lam, Ls, KB, mu_s, Q0), res_lin[s_]["EJ"].subs(subsK), "numpy") for s_ in (False, True)}
RES["linear"] = {("with_gamma_L" if s_ else "no_gamma_L"): {"E_J": str(res_lin[s_]["EJ"]), "Gamma2": str(res_lin[s_]["G2"])}
                 for s_ in (False, True)}

# ============================================================================ Part B: the F family and its static maps
LAM_BBN = 24.7


def f_family():
    """id -> (f(x), f'(x), lambda_s, lambda_0, x_max, in_family)"""
    fam = {}
    b = 1 / LAM_BBN
    fam["SZ-simple"] = (lambda X: X / (1 + b + b * X), lambda X: (1 + b) / (1 + b + b * X) ** 2, LAM_BBN, 0.0, np.inf, True)
    fam["SZ-exp"] = (lambda X: LAM_BBN * (1 - np.exp(-X / (1 + LAM_BBN))), lambda X: LAM_BBN / (1 + LAM_BBN) * np.exp(-X / (1 + LAM_BBN)),
                     LAM_BBN, 0.0, np.inf, True)
    fam["SZ-sharp"] = (lambda X: np.minimum(X, LAM_BBN + 1) / (1 + b), lambda X: np.where(X < LAM_BBN + 1, 1 / (1 + b), 0.0),
                       LAM_BBN, 0.0, np.inf, True)
    fam["SZ-inf"] = (lambda X: X, lambda X: np.ones_like(X), np.inf, 0.0, np.inf, True)
    if MUT:
        fam["cap-n1"] = (lambda X: X / (1 + X), lambda X: 1 / (1 + X) ** 2, np.inf, 0.0, np.inf, True)
    else:
        fam["cap-n1"] = (lambda X: X / (1 - X), lambda X: 1 / (1 - X) ** 2, np.inf, 0.0, 1.0, True)
    fam["cap-n2"] = (lambda X: X / (1 - 2 * X), lambda X: 1 / (1 - 2 * X) ** 2, np.inf, 0.0, 0.5, True)
    for l0 in (1e-3, 1e-2, 1e-1):
        fam[f"door-l0={l0:g}"] = (lambda X, l0=l0: l0 + X / (1 - X), lambda X: 1 / (1 - X) ** 2, np.inf, l0, 1.0, False)
    return fam


FAM = f_family()


def solve_x(f, Yn, xmax):
    """f(x) x = Yn, vectorised bisection in log x (f x is monotone increasing for every member)."""
    Yn = np.asarray(Yn, float)
    lo = np.full(Yn.shape, -40.0)
    hi = np.full(Yn.shape, math.log(xmax * (1 - 1e-15)) if np.isfinite(xmax) else 40.0)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        X = np.exp(mid)
        big = f(X) * X > Yn
        hi = np.where(big, mid, hi)
        lo = np.where(big, lo, mid)
    return np.exp(0.5 * (lo + hi))


def g_of_y(fid, yv):
    f, fp, lam_s, l0, xmax, _ = FAM[fid]
    b = 0.0 if not np.isfinite(lam_s) else 1 / lam_s
    Yn = np.asarray(yv, float) / (1 + b)
    X = solve_x(f, Yn, xmax)
    return Yn + X, X


LY = np.linspace(-10, 8, 180001)
TAB = {}
for fid in FAM:
    gg, _ = g_of_y(fid, 10 ** LY)
    TAB[fid] = np.log10(gg)


EXACT = {}                                                    # filled after K4: members proven identical to a closed form


def nu_of(fid):
    if fid in EXACT:
        return EXACT[fid]
    tab = TAB[fid]
    return lambda yv: 10 ** np.interp(np.log10(np.maximum(yv, 1e-10)), LY, tab) / np.maximum(yv, 1e-300)


NU1 = lambda yv: 0.5 * (1 + np.sqrt(1 + 4 / yv))
NU2 = lambda yv: np.sqrt(1 + 1 / yv)
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
import CFG4_common as C  # noqa: E402  (the record's SPARC loader, footings, nu_rar)

NU_RAR = C.nu_rar

# K4: static maps
yy = np.logspace(-6, 4, 401)
e1 = float(np.max(np.abs(g_of_y("cap-n1", yy)[0] / (NU1(yy) * yy) - 1)))
e2 = float(np.max(np.abs(g_of_y("cap-n2", yy)[0] / (NU2(yy) * yy) - 1)))
rng = np.random.default_rng(7)
yt = 10 ** rng.uniform(-6, 5, 200)
et = max(float(np.max(np.abs(nu_of(fid)(yt) * yt / g_of_y(fid, yt)[0] - 1))) for fid in FAM)
gd = g_of_y("SZ-simple", np.array([1e-8, 1e8]))[0]
ed, en = abs(gd[0] / math.sqrt(1e-8) - 1), abs(gd[1] / 1e8 - 1)
check("K4", e1 <= 1e-12 and e2 <= 1e-12 and et <= 1e-8 and ed <= 1e-3 and en <= 1e-3,
      f"cap-n1 vs nu1 {e1:.1e}; cap-n2 vs nu2 {e2:.1e}; table vs direct {et:.1e}; SZ-simple deep {ed:.1e}, Newton {en:.1e}",
      "<=1e-12, <=1e-12, <=1e-8, <=1e-3, <=1e-3")
RES["static_map_checks"] = dict(cap_n1=e1, cap_n2=e2, table=et, deep=ed, newton=en)
# AMENDMENT A1 (post-result): a member whose map equals a closed-form law to <= 1e-12 (K4) is scored with that closed form,
# so that round-off in the table is not scored as a difference between identical laws.
if e1 <= 1e-12:
    EXACT["cap-n1"] = NU1
if e2 <= 1e-12:
    EXACT["cap-n2"] = NU2
RES["scored_with_closed_form"] = sorted(EXACT)

# ============================================================================ Part C: SPARC (AG4b pipeline, verbatim)
LN10 = math.log(10.0)
KPC_S = 3.0857e19
LU0, SIG_U, S0 = math.log10(0.5), 0.10, 0.05
LU = LU0 + np.linspace(-0.5, 0.5, 201)
UG = 10 ** LU
A0 = {f: C.A0[f] for f in C.FOOTS}
GAL = C.load_sparc()
D_ = []
for gx in GAL:
    R, Vo, eV, Vg, Vd, Vb = (np.asarray(gx[kk], float) for kk in ("R", "Vobs", "eV", "Vgas", "Vdisk", "Vbul"))
    Rm = R * KPC_S
    gb_lo = (np.sign(Vg) * Vg ** 2 + UG[0] * Vd ** 2 + 1.4 * UG[0] * Vb ** 2) * 1e6 / Rm
    gb_hi = (np.sign(Vg) * Vg ** 2 + UG[-1] * Vd ** 2 + 1.4 * UG[-1] * Vb ** 2) * 1e6 / Rm
    go = (Vo * 1e3) ** 2 / Rm
    m = (Vo > 0) & (go > 0) & (gb_lo > 0) & (gb_hi > 0) & np.isfinite(go) & (R > 0)
    if m.sum() < 5:
        continue
    gas = np.sign(Vg[m]) * Vg[m] ** 2 * 1e6 / Rm[m]
    star = (Vd[m] ** 2 + 1.4 * Vb[m] ** 2) * 1e6 / Rm[m]
    sv = 2.0 / LN10 * np.clip(eV[m], 1, None) / np.clip(Vo[m], 1, None)
    D_.append(dict(name=gx["name"], go=go[m], gas=gas, star=star, sv=sv))
P(f"SPARC: {len(GAL)} rotmod files, {len(D_)} galaxies, {sum(len(d['go']) for d in D_)} points")


def gbar(d, U):
    return d["gas"][:, None] + d["star"][:, None] * np.atleast_1d(U)[None, :]


def fit_all(data, nu, a0):
    rms, chi = [], []
    for d in data:
        gb = gbar(d, UG)
        r = np.log10(d["go"])[:, None] - np.log10(nu(gb / a0) * gb)
        s2 = d["sv"][:, None] ** 2 + S0 ** 2
        c2 = (r ** 2 / s2).sum(0) + ((LU - LU0) / SIG_U) ** 2
        i = int(np.argmin(c2))
        rms.append(math.sqrt(np.mean((r[:, i] / 2) ** 2)))
        chi.append(float(c2[i]))
    return np.array(rms), np.array(chi)


def paired_z(d1, d2):
    d = d2 - d1
    d = d[np.isfinite(d)]
    n = len(d)
    rg = np.random.default_rng(20261020)
    idx = rg.integers(0, n, (10000, n))
    med = float(np.median(d))
    sd = float(np.std(np.median(d[idx], axis=1)))
    return med, sd, (-med / sd if sd > 0 else 0.0), n


ag4b = json.load(open(os.path.join(REPO, "argon_push", "AG4b_sparc_population_upsilon", "ag4b_results.json")))
k5, k5v = True, []
FITS = {}
for f in C.FOOTS:
    a0 = A0[f]
    FITS[f] = {"n1": fit_all(D_, NU1, a0), "n2": fit_all(D_, NU2, a0), "RAR": fit_all(D_, NU_RAR, a0)}
    Dm, sD, zz, n = paired_z(FITS[f]["n1"][0], FITS[f]["n2"][0])
    pr = ag4b["footings"][f]["primary"]
    ok = abs(Dm - pr["D"]) <= 1e-9 and abs(zz - pr["z"]) <= 1e-9 and n == pr["n"]
    k5 &= ok
    k5v.append(f"{f}: D {Dm:+.6f} (AG4b {pr['D']:+.6f}), z {zz:+.4f} (AG4b {pr['z']:+.4f}), n {n}")
check("K5", k5, "; ".join(k5v), "AG4b primary reproduced to 1e-9")

SP = {}
for f in C.FOOTS:
    a0 = A0[f]
    r1, c1 = FITS[f]["n1"]
    rR, cR = FITS[f]["RAR"]
    SP[f] = {"canonical_vs_RAR": dict(z=paired_z(rR, r1)[2], D=paired_z(rR, r1)[0], S1=float((c1 - cR).sum()))}
    P(f"\n=== SPARC, footing {f} (a0 = {a0:.4e}) ===")
    P(f"  yardstick: canonical vs nu_RAR  z = {SP[f]['canonical_vs_RAR']['z']:+.2f}, S1 = {SP[f]['canonical_vs_RAR']['S1']:+.1f}")
    for fid in FAM:
        rc, cc = fit_all(D_, nu_of(fid), a0)
        Dc, sDc, zc, _ = paired_z(r1, rc)
        Dr, sDr, zr, _ = paired_z(rR, rc)
        SP[f][fid] = dict(z_vs_canonical=zc, D_vs_canonical=Dc, S1_vs_canonical=float((cc - c1).sum()),
                          z_vs_RAR=zr, D_vs_RAR=Dr, S1_vs_RAR=float((cc - cR).sum()), pass_iii_footing=bool(zc > -2))
        P(f"  {fid:14s} vs canonical: d {Dc:+.4f} dex, z {zc:+7.2f}, S1 {SP[f][fid]['S1_vs_canonical']:+9.1f} | "
          f"vs nu_RAR: d {Dr:+.4f}, z {zr:+7.2f}, S1 {SP[f][fid]['S1_vs_RAR']:+9.1f}")
RES["SPARC"] = SP

# ============================================================================ Part D: screened Solar System (C6 Route F)
sys.path.insert(0, os.path.join(REPO, "covariant_push_2026_10_22", "C6_literal_cassini"))
import c6_solver as C6S  # noqa: E402  (read-only)

c6 = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C6_literal_cassini", "c6_literal_cassini_results.json")))
GM, PC6 = 1.32712440018e20, 3.0857e16
A06 = {"canonical": 9.36e-11, "alt": 1.13e-10}
PARK, HEES = 5.2e-27, 9.0e-27
EV = c6["inputs"]["E"]


def I2_gen(MT, ML, nk=4000, nc=64, kmin=1e-4, kmax=1e4):
    cg, cw = np.polynomial.legendre.leggauss(nc)
    P2 = 0.5 * (3 * cg ** 2 - 1)
    lk = np.linspace(np.log(kmin), np.log(kmax), nk)
    kk = np.exp(lk)
    m = (1 - cg ** 2) / MT + cg ** 2 / ML
    chi = m[None, :] / (1 - m[None, :] + kk[:, None] ** 2 * m[None, :] / 2)
    c2 = 2.5 * (chi * P2 * cw).sum(1)
    cgt, cwt = np.polynomial.legendre.leggauss(256)
    at = 1 / ((1 - cgt ** 2) / MT + cgt ** 2 / ML) - 1
    tail = 2.5 * (at * 0.5 * (3 * cgt ** 2 - 1) * cwt).sum()
    trap = getattr(np, "trapezoid", None) or np.trapz
    return trap(kk ** 3 * c2, lk) - 4.0 * tail / kmax


def Q2_of(MT, ML, Lpc):
    return -2 * GM / (5 * math.pi * (Lpc * PC6) ** 3) * I2_gen(MT, ML)


k6, k6v = 0.0, 0.0
for f in ("canonical", "alt"):
    for E in ("E0", "E1", "E2", "E3"):
        xe = EV[f][E]["ge"] / A06[f]
        k6 = max(k6, abs(I2_gen(1 + xe, (1 + xe) ** 2) - C6S.routeF_I2(xe, 0.0)))
        q = Q2_of(1 + xe, (1 + xe) ** 2, 24)
        k6v = max(k6v, abs(q / c6["R1_physical"][f"{f}|24|{E}"]["Q2"] - 1))
check("K6", k6 <= 1e-10 and k6v <= 1e-6, f"I2 vs c6_solver {k6:.1e}; Q2 vs C6 json {k6v:.1e}", "<=1e-10, <=1e-6 rel")

SS = {}
P("\n=== screened Solar System (L* = 24 pc; Route F with the candidate's own response at C6's g_Ne) ===")
for fid, (f_, fp, lam_s, l0, xmax, _) in FAM.items():
    b = 0.0 if not np.isfinite(lam_s) else 1 / lam_s
    rows, ok = {}, True
    for fo in ("canonical", "alt"):
        for E in ("E0", "E1", "E2", "E3"):
            ye = EV[fo][E]["gNe"] / A06[fo]
            xv = float(solve_x(f_, np.array([ye / (1 + b)]), xmax)[0])
            MT, ML = 1 + float(f_(np.array(xv))), 1 + float(f_(np.array(xv))) + xv * float(fp(np.array(xv)))
            q = Q2_of(MT, ML, 24)
            rows[f"{fo}|{E}"] = dict(x_V=xv, M_T=MT, M_L=ML, Q2=q, over_Park=abs(q) / PARK)
            ok &= abs(q) <= PARK and MT >= 1 and ML >= 1
    SS[fid] = dict(rows=rows, pass_iv=bool(ok), max_over_Park=max(r["over_Park"] for r in rows.values()),
                   min_M=min(min(r["M_T"], r["M_L"]) for r in rows.values()))
    P(f"  {fid:14s} max |Q2|/Park = {SS[fid]['max_over_Park']:.2e}; min(M_T, M_L) = {SS[fid]['min_M']:.3f} -> {'PASS' if ok else 'FAIL'}")
RES["solar_system"] = SS
RES["planets_carried_from_C6"] = {kk: v["ratio"] for kk, v in c6["R2_planets"].items()}

# ============================================================================ Part E: health and growth per candidate
KBV, H, LST_PC = 0.05, 0.68, 24.0
MPC = 1e6
P("\n=== health at Y = 0 and linear growth (K_B = 0.05, L* = 24 pc, h = 0.68) ===")
kgrid = np.logspace(-3, math.log10(0.3), 400) * H          # 1/Mpc
GR = {}


def kc_band(l0, stiff, mu_inv):
    """largest k (1/Mpc) with E_J < 0 (the Jeans band), or inf if E_J < 0 at every k."""
    kk = np.logspace(-4, 8, 6001)
    e = EJn[stiff](kk, l0, (LST_PC / MPC) if stiff else 0.0, KBV, 1 / mu_inv, 1.0)
    if np.all(e < 0):
        return float("inf")
    neg = np.where(e < 0)[0]
    return float(kk[neg.max()]) if len(neg) else 0.0


for fid, (f_, fp, lam_s, l0, xmax, fam_in) in FAM.items():
    out = {"lambda_0": l0, "in_family": fam_in, "i_lit": bool(l0 > 0)}
    for mu_inv in (1.0, 10.0):
        for stiff in (False, True):
            Lsv = (LST_PC / MPC) if stiff else 0.0
            gF = G2n[stiff](kgrid, l0, Lsv, KBV, 1 / mu_inv, 1.0)
            gR = G2n[stiff](kgrid, 0.0, Lsv, KBV, 1 / mu_inv, 1.0)
            tg = f"mu^-1={mu_inv:g}Mpc|{'gL' if stiff else 'noGL'}"
            out[tg] = dict(max_dev_vs_ref=float(np.max(np.abs(gF / gR - 1))), ref_over_GR_at_kmax=float(gR[-1]),
                           k_c_per_Mpc=kc_band(l0, stiff, mu_inv))
    out["ii_IR"] = True                                        # K2: Gamma^2(0) = 4 pi G rho for every lambda_0 (symbolic)
    out["ii_q"] = bool(out["mu^-1=1Mpc|gL"]["max_dev_vs_ref"] <= 0.01 and out["mu^-1=1Mpc|noGL"]["max_dev_vs_ref"] <= 0.01)
    out["ii_lit"] = bool(l0 == 0)
    out["i_band_noGL"] = bool(np.isfinite(out["mu^-1=1Mpc|noGL"]["k_c_per_Mpc"]))
    out["i_band_gL"] = bool(np.isfinite(out["mu^-1=1Mpc|gL"]["k_c_per_Mpc"]))
    out["i_strict"] = False                                    # K2: E_J < 0 wherever Gamma^2 > 0, and Gamma^2(0) > 0
    out["v"] = bool(lam_s >= LAM_BBN)
    GR[fid] = out
    a, b_ = out["mu^-1=1Mpc|noGL"], out["mu^-1=1Mpc|gL"]
    P(f"  {fid:14s} lambda_0 = {l0:g}: (i-lit) {'PASS' if out['i_lit'] else 'FAIL'}; Jeans band k_c (mu^-1 = 1 Mpc) "
      f"{a['k_c_per_Mpc']:.3g} / {b_['k_c_per_Mpc']:.3g} per Mpc (no gL / gL); (ii-q) max|dGamma^2| {a['max_dev_vs_ref']:.2e} / "
      f"{b_['max_dev_vs_ref']:.2e}; AeST ref/GR at 0.3 h/Mpc {a['ref_over_GR_at_kmax']:.3f}")
RES["health_growth"] = GR
# reported only: where the floor door changes the far field (g_N = lambda_0^2 a0, i.e. r = r_M / lambda_0) for 1e11 Msun
GMg = 6.674e-11 * 1e11 * 1.989e30
RES["door_far_field_onset_kpc_1e11Msun"] = {f: {f"{l0:g}": math.sqrt(GMg / A0[f]) / l0 / KPC_S for l0 in (1e-3, 1e-2, 1e-1)}
                                             for f in C.FOOTS}
P(f"  [reported] floor door: far-field change sets in at r = r_M/lambda_0 (1e11 Msun): {RES['door_far_field_onset_kpc_1e11Msun']} kpc")

# ============================================================================ verdict
P("\n=== scorecard (verdict conditions: i = i-lit, ii = IR and q, iii both footings, iv, v) ===")
SC = {}
for fid in FAM:
    g_ = GR[fid]
    iii = all(SP[f][fid]["pass_iii_footing"] for f in C.FOOTS)
    row = dict(i=g_["i_lit"], ii=g_["ii_IR"] and g_["ii_q"], iii=iii, iv=SS[fid]["pass_iv"], v=g_["v"], in_family=g_["in_family"])
    row["all"] = all(row[c] for c in ("i", "ii", "iii", "iv", "v"))
    SC[fid] = row
    P(f"  {fid:14s} {'family' if row['in_family'] else 'OUTSIDE'}: " + " ".join(f"({c}) {'P' if row[c] else 'F'}"
                                                                          for c in ("i", "ii", "iii", "iv", "v"))
      + f"  -> {'ALL PASS' if row['all'] else 'fails'}")
RES["scorecard"] = SC
npass = sum(ch["pass"] for ch in CHECKS)
if npass < len(CHECKS):
    verdict = "UNDECIDED"
elif any(r["all"] and r["in_family"] for r in SC.values()):
    verdict = "FOUND"
else:
    verdict = "NONE IN THE FAMILY"
door = [fid for fid, r in SC.items() if (not r["in_family"]) and r["all"]]
P(f"\nVERDICT: {verdict}" + (f"; outside the family (+1 POSTULATED constant lambda_0) all five pass for: {door}" if door else
                            "; no outside-family door passes all five"))
RES["verdict"] = verdict
RES["door_all_pass"] = door

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
RES.update(checks=CHECKS, n_pass=npass, n_checks=len(CHECKS), runtime_s=round(time.time() - T0, 1), max_rss_GB=round(rss, 3))
P(f"  runtime {time.time() - T0:.1f} s, max RSS {rss:.3f} GB")
P(f"H1_AEST_F COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
json.dump(RES, open(os.path.join(HERE, f"h1_aest_f_results{TAG}.json"), "w"), indent=1, default=float)
OUTF.close()
sys.exit(0 if npass == len(CHECKS) else 1)
