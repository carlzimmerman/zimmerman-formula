#!/usr/bin/env python3
"""y1_6_x1_hybrid.py -- Part 4 (lane X1) of Y1_PREREGISTRATION.md.  A HYBRID: the Y1 SM running (loops declared below) plus lane X1's one- and two-loop exotic-state thresholds (E6 27: D, D^c at M_D; two doublets at M_H;
the neutral singlet omitted), NO three-loop exotic increments (declared approximation), NO exotic Yukawas, continuous couplings at thresholds (as in X1).
It re-asks two lane-X1 questions with the tighter running: (i) the single-27 free fit ('closest approach 0.0207, tolerance [0.01, 0.04]'); (ii) where the three-27 exact solutions of a_1 = a_2 = a_3 sit (X1: X = 4.6-5.1e13 GeV, M_H 100 GeV to 2e8, M_D 2e7 to 5e13).
Also the plain-SM (S1/S2 desert) zero-knob rules R-A, R-B, R-C: new miss factors read from y1_5_results.json.
Run:    python3 y1_6_x1_hybrid.py            (exit 0 iff the internal checks pass)
MUTATE: python3 y1_6_x1_hybrid.py MUTATE     (the control flips the sign of the exotic one-loop increments; the validation against lane X1's own runner must fail: exit 1; exit 3 if not)
Imports lane X1 READ-ONLY (path-relative).  No bytecode.  Writes y1_6_results.json.
"""
import sys
sys.dont_write_bytecode = True
import os
import json
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import differential_evolution, least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for sub in ("B_rg_asymptotic_safety", "N1_joint_couplings", "U3_invented_uv_boundary", "D_calibration_bar", "X1_spectrum_meets_boundary"):
    sys.path.insert(0, os.path.join(HERE, "..", sub))
import y1_lib as L
import x1_lib as X1

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
PI = math.pi
XP = X1.XP
fails = []


def chk(name, ok, info=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        fails.append(name)


def exo_list(MD, MH, n27):
    ex = X1.exotic_bB(X1.exotics_e6(MD, MH, n27))
    if MUT:
        ex = [(m, -db, dB) for (m, db, dB) in ex]          # MUTATE: wrong sign of the one-loop increments
    return ex


def rhs_exo(t, y, o, Db, DB):
    d = 2.0 * L.rhs_lnmu2(y, o)
    gvec = np.array([0.6 * y[0], y[1], y[2]])
    dA = -(Db + (DB @ gvec) / (16 * PI ** 2)) / (2 * PI)            # d a_i / d ln mu (Y basis)
    dg = -gvec ** 2 / (4 * PI) * dA
    d[0] += 5.0 / 3.0 * dg[0]
    d[1] += dg[1]
    d[2] += dg[2]
    return d


def run_hybrid(u0, mu0, exo, X, o, rtol=1e-10):
    """State at X (the array u); exo = list of (mass, db[3], dB[3][3])."""
    pts = sorted({m for (m, _, _) in exo if mu0 < m < X})
    edges = [math.log(mu0)] + [math.log(m) for m in pts] + [math.log(X)]
    y = np.array(u0, float)
    for a, b in zip(edges[:-1], edges[1:]):
        mid = math.exp(0.5 * (a + b))
        Db = np.zeros(3)
        DB = np.zeros((3, 3))
        for (m, db, dB) in exo:
            if mid > m:
                Db = Db + db
                DB = DB + dB
        s = solve_ivp(lambda t, yy: rhs_exo(t, yy, o, Db, DB), [a, b], list(y), method="DOP853", rtol=rtol, atol=1e-14)
        y = s.y[:, -1]
    return y


def A_of(y):
    return np.array([4 * PI / (0.6 * y[0]), 4 * PI / y[1], 4 * PI / y[2]])


def res_RA(A):
    a1 = 0.6 * A[0]
    return np.array([X1.ratio_res(a1 / A[1], 1.0), X1.ratio_res(A[2] / A[1], 1.0)])


print("=" * 130)
print("Y1-6 lane X1 hybrid -- mode:", "MUTATE" if MUT else "REAL RUN")
print("=" * 130)

O_FAST = L.Opts(gauge_loops=2, yuk_loops=2)
O_FULL = L.Opts(gauge_loops=4, yuk_loops=3)
u0_y1 = L.central_u0()
Mt = L.PDG["Mt"]

# ------------------------------------------------------------------------------------- checks of the hybrid
tr = L.run_central(mu_max=1.3e19)
yy = run_hybrid(u0_y1, Mt, [], XP, O_FULL)
chk("hybrid with no exotics reproduces the Y1 central run at X_P (1e-7)", np.max(np.abs(A_of(yy) / np.array(tr.A(XP)) - 1)) < 1e-7, f"{np.max(np.abs(A_of(yy) / np.array(tr.A(XP)) - 1)):.1e}")

rng = np.random.default_rng(20260929)
worst = 0
for _ in range(6):
    n27 = int(rng.choice([1, 3]))
    MD = 10 ** rng.uniform(3, 14)
    MH = 10 ** rng.uniform(2, 12)
    ex_x1 = X1.exotics_e6(MD, MH, n27)
    run_x1 = X1.Run("2L-T", ex_x1)
    A_mt = np.array(run_x1.A(Mt))
    u0c = L.u_from_gY_g2_g3(math.sqrt(4 * PI / A_mt[0]), math.sqrt(4 * PI / A_mt[1]), math.sqrt(4 * PI / A_mt[2]), 0.9334, L.YB_MT_SMDR, L.YTAU_MT_SMDR, 0.126)
    for X in (1e14, 1e16):
        if math.log(X) > run_x1.lnmax:
            continue
        a_x1 = np.array(run_x1.A(X))
        a_me = A_of(run_hybrid(u0c, Mt, exo_list(MD, MH, n27), X, L.Opts(gauge_loops=2, yuk_loops=2)))
        worst = max(worst, float(np.max(np.abs(a_me / a_x1 - 1))))
chk("hybrid (two loops, started from X1's own values at m_t) reproduces X1's runner for random exotic masses and n27 = 1, 3 within 5e-4", worst < 5e-4, f"worst {worst:.2e}")

# ------------------------------------------------------------------------------------- (i) single 27, free fit
LO_X, HI_X = math.log10(1e11), math.log10(1.001 * XP)


def cost_factory(u0, o, n27, tag):
    def cost(p):
        lx, ld, lh = p
        X = 10 ** lx
        MD, MH = 10 ** ld, 10 ** lh
        y = run_hybrid(u0, Mt, exo_list(MD, MH, n27), X, o)
        A = A_of(y)
        if not np.all(A > 1):
            return 10.0
        return float(np.max(np.abs(res_RA(A))))
    return cost


def optimise(u0, o, n27, seed=1, maxiter=60):
    bounds = [(LO_X, HI_X), (3.0, HI_X), (2.0, HI_X)]
    res = differential_evolution(cost_factory(u0, o, n27, ""), bounds, seed=seed, popsize=12, maxiter=maxiter, tol=1e-10, polish=False, updating="immediate")
    p = res.x
    # local polish by Nelder-Mead in log space
    from scipy.optimize import minimize
    r2 = minimize(cost_factory(u0, o, n27, ""), p, method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-10, maxiter=400))
    return (r2.x, r2.fun) if r2.fun < res.fun else (p, res.fun)


print("\n(i) ONE 27, rule R-A with X free (3-dim least squares over X, M_D, M_H, floors M_D >= 1 TeV, M_H >= 100 GeV): closest approach max|r|, r = (a_1/a_2 - 1, a_3/a_2 - 1) in X1's ratio_res form")
# X1's own machinery, for the optimiser validation
def cost_x1(p):
    lx, ld, lh = p
    X = 10 ** lx
    run = X1.Run("2L-T", X1.exotics_e6(10 ** ld, 10 ** lh, 1))
    if math.log(X) > run.lnmax:
        return 10.0
    return float(np.max(np.abs(res_RA(np.array(run.A(X))))))
res_x1 = differential_evolution(cost_x1, [(LO_X, HI_X), (3.0, HI_X), (2.0, HI_X)], seed=1, popsize=10, maxiter=40, tol=1e-10, polish=False, updating="immediate")
print(f"    X1's own runner, my optimiser: closest approach {res_x1.fun:.4f} at log10(X, M_D, M_H) = {np.round(res_x1.x, 2)}   (lane X1 reported 0.0207)")
chk("my optimiser on X1's own runner finds a closest approach not larger than X1's 0.0207 (x 1.2)", res_x1.fun <= 0.0207 * 1.2, f"{res_x1.fun:.4f}")
p1, f1 = optimise(u0_y1, O_FAST, 1)
A_best = A_of(run_hybrid(u0_y1, Mt, exo_list(10 ** p1[1], 10 ** p1[2], 1), 10 ** p1[0], O_FULL))
r_full = res_RA(A_best)
print(f"    Y1 hybrid (SM two loops, Y1 boundary): closest approach {f1:.4f} at log10(X, M_D, M_H) = {np.round(p1, 2)} ; with the SM at four loops: r = {np.round(r_full, 4)}")
# tolerance from the ensemble at the best point
draws = L.mc_draws(120)
rs = []
for kw in draws:
    u0 = L.central_u0(**kw)
    y = run_hybrid(u0, kw["Mt"], exo_list(10 ** p1[1], 10 ** p1[2], 1), 10 ** p1[0], O_FAST)
    rs.append(res_RA(A_of(y)))
rs = np.array(rs)
sig = rs.std(axis=0, ddof=1)
print(f"    ensemble (N = 120, budget items E1-E5) at that point: sigma(r) = {np.round(sig, 5)} -> tolerance 2 sigma = {np.round(2 * sig, 5)} (lane X1 had [0.01, 0.04])")
miss_new = float(np.max(np.abs(res_RA(A_of(run_hybrid(u0_y1, Mt, exo_list(10 ** p1[1], 10 ** p1[2], 1), 10 ** p1[0], O_FAST)))) / (2 * sig)))
print(f"    closest approach in units of the new tolerance: {miss_new:.1f}   (lane X1: 2.1 x its smallest tolerance)")

# ------------------------------------------------------------------------------------- (ii) three 27s, exact family
print("\n(ii) THREE 27s: exact solutions of a_1 = a_2 = a_3 at some X with M_D >= 1 TeV, M_H >= 100 GeV (rule R-A, X free): scan in X, solve the two equations for (M_D, M_H)")


def family(u0, o, n27, nstart, label, seed=7):
    """Random-start 3-unknown (log10 X, log10 M_D, log10 M_H) solves of the two equations r(R-A) = 0 (the solution set is a curve)."""
    rng = np.random.default_rng(seed)
    lo = np.array([12.5, 3.0, 2.0])
    hi = np.array([14.8, 15.0, 12.0])

    def f(p):
        y = run_hybrid(u0, Mt, exo_list(10 ** p[1], 10 ** p[2], n27), 10 ** p[0], o)
        A = A_of(y)
        if not np.all(A > 1):
            return np.array([10.0, 10.0])
        return res_RA(A)
    sols = []
    for _ in range(nstart):
        x0 = lo + rng.random(3) * (hi - lo)
        try:
            s = least_squares(f, x0, bounds=(lo, hi), xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=60)
        except Exception:
            continue
        if s.cost < 1e-14:
            sols.append(s.x)
    sols = np.array(sols)
    print(f"    {label}: {len(sols)} exact solutions from {nstart} random starts")
    if len(sols):
        print(f"       log10 X in [{sols[:, 0].min():.3f}, {sols[:, 0].max():.3f}]  = X in [{10 ** sols[:, 0].min():.2e}, {10 ** sols[:, 0].max():.2e}] GeV ;  M_D in [{10 ** sols[:, 1].min():.1e}, {10 ** sols[:, 1].max():.1e}] ; M_H in [{10 ** sols[:, 2].min():.1e}, {10 ** sols[:, 2].max():.1e}] ; {int(np.sum(sols[:, 1] < sols[:, 0]))} of them have M_D < X")
    return sols


run3 = X1.Run("2L-T", X1.exotics_e6(1e8, 1e5, 3))
A3 = np.array(run3.A(Mt))
u0_x1 = L.u_from_gY_g2_g3(math.sqrt(4 * PI / A3[0]), math.sqrt(4 * PI / A3[1]), math.sqrt(4 * PI / A3[2]), 0.9334, L.YB_MT_SMDR, L.YTAU_MT_SMDR, 0.126)
fam_x1 = family(u0_x1, O_FAST, 3, 50, "hybrid started from X1's own boundary (SM two loops)")
fam_y1 = family(u0_y1, O_FAST, 3, 50, "hybrid started from Y1-central (SM two loops)")
if len(fam_y1):
    k = int(np.argsort(fam_y1[:, 0])[len(fam_y1) // 2])
    X0, MD0, MH0 = 10 ** fam_y1[k, 0], 10 ** fam_y1[k, 1], 10 ** fam_y1[k, 2]
    y = run_hybrid(u0_y1, Mt, exo_list(MD0, MH0, 3), X0, O_FULL)
    a2X = A_of(y)[1]
    verdict, tau = X1.proton_check(X0, a2X)
    print(f"    proton-lifetime check (lane X1's RECALLED scaling, uncertain by 10x) at a middle solution X = {X0:.2e}: tau ~ {tau:.1e} yr vs 2.4e34 -> {verdict}")
chk("the three-27 exact-solution family exists both from X1's boundary and from Y1-central (a re-fit that costs two mass knobs, as in lane X1)", len(fam_x1) > 0 and len(fam_y1) > 0)
chk("X1's family lies at X = 4.6e13-5.1e13 in X1's report: my hybrid from X1's boundary lands within a factor 1.3 of that range", len(fam_x1) > 0 and 4.6e13 / 1.3 <= 10 ** np.median(fam_x1[:, 0]) <= 5.1e13 * 1.3, f"median {10 ** np.median(fam_x1[:, 0]):.2e}" if len(fam_x1) else "")

# ------------------------------------------------------------------------------------- plain-SM zero-knob rules
print("\nPLAIN SM (S1 = SM desert; S2 = Spin(10) 16 x 3 has the same running): zero-knob rules R-A / R-B / R-C, the same numbers as lane U3's P03 / V03 (read from y1_5_results.json)")
R5 = json.load(open(os.path.join(HERE, "y1_5_results.json")))["rows"]
byid = {r["id"]: r for r in R5}
OLD = {r["id"]: r for r in json.load(open(os.path.join(HERE, "..", "U3_invented_uv_boundary", "u3_1_results.json")))["rows"]}
for vid, txt in (("V03", "R-B: a_3/a_2 residual at the a_1 = a_2 crossing (component 1)"), ("V06", "R-A GUT norm, X_P"), ("V07", "R-A GUT norm, X_R"), ("V08", "R-A GUT norm, X_S"), ("V09", "R-C Y norm, X_P"), ("V10", "R-C Y norm, X_R"), ("V11", "R-C Y norm, X_S")):
    r = byid[vid]
    comp = [abs(c) / t for c, t in zip(r["cen_r"], r["tol_reg"])]
    oldrow = OLD[vid]
    oldcomp = [abs(c) / t for c, t in zip(oldrow["cen_r"], oldrow["tol"])]
    if vid == "V03":
        comp, oldcomp = comp[:1], oldcomp[:1]
    print(f"    {vid} {txt:60s}: residuals {np.round(r['cen_r'], 4)} tol_new {np.round(r['tol_reg'], 4)} -> worst miss factor {max(comp):.1f}   (lane U3/X1: {max(oldcomp):.1f})")

json.dump(dict(single27=dict(closest=f1, x=list(map(float, p1)), sigma_r=list(map(float, sig)), miss_new=miss_new, x1_optimiser=float(res_x1.fun)),
               family_x1_boundary=fam_x1.tolist(), family_y1=fam_y1.tolist()), open(os.path.join(HERE, "y1_6_results_MUTATE.json" if MUT else "y1_6_results.json"), "w"), indent=1, default=float)
print(f"\nY1-6: {len(fails)} failed" + (f": {fails}" if fails else ""))
if MUT:
    print("MUTATE control:", "BITES -> exit 1" if fails else "BROKEN -> exit 3")
    sys.exit(1 if fails else 3)
sys.exit(0 if not fails else 2)
