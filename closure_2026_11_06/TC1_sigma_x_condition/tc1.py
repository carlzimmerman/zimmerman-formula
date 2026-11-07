#!/usr/bin/env python3
"""TC1: does TC03's clock-gradient catastrophe reach the QX19 one action, and does it fire on physical data?

Criteria: CRITERIA.md (4f3d3efa6b), committed alone before any script. Checks S1, S2/J3, KA1-KA3, N1, N2, P0/P1.
N1/KA3 read the per-run checkpoints written by tc1_runs.py (runs/). Outputs tc1.json / tc1.out.
MUTATE: TC1_MUTATE=1 plants the blend scale b = 4X (classifier layer 0 < Sigma < 4X); must exit 1. Outputs *_MUTATE.*.
  python3 closure_2026_11_06/TC1_sigma_x_condition/tc1.py
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, glob
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
MUT = os.environ.get("TC1_MUTATE") == "1"
BFAC = 4 if MUT else 1                      # blend scale b = BFAC * X (planted 4 under MUTATE)
TAG = "_MUTATE" if MUT else ""
AGE_S = 13.8e9 * 3.15576e7                  # 4.35e17 s
CL = 2.99792458e8; G_SI = 6.674e-11; KAPPA = 0.5
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
OUT, RES, CHK = [], {}, {}


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}")


P("TC1  Sigma > X condition for the QX19 one action" + ("  [MUTATE: b = 4X]" if MUT else ""))
P("kappa = 1/2 FITTED; not theory closed; adopts nothing")

# ============================================================ S1: densities equal on O = {Sigma >= b} u {Sigma <= 0}
q = sp.Symbol("q", real=True)
form = json.load(open(glob.glob(os.path.join(REPO, "action_search_2026_11_05/AC21_smooth_3d/iter_6*/form.json"))[0]))
pieces = [(sp.Rational(a), sp.Rational(b), sp.sympify(e, locals={"q": q})) for a, b, e in form["pieces"]]
pieces += [(sp.Integer(1), sp.oo, sp.Integer(1))]
f_pcs, c1, c0 = [], sp.Integer(0), sp.Integer(0)
for a, b, e in pieces:
    F1 = sp.integrate(e, (q, a, q)) + c1; F0 = sp.integrate(F1, (q, a, q)) + c0
    f_pcs.append((a, b, sp.expand(F0)))
    if b != sp.oo:
        c1, c0 = F1.subs(q, b), F0.subs(q, b)
f_last = f_pcs[-1][2]
S, Xs = sp.symbols("Sigma X", positive=True)
b_ = BFAC * Xs
F_on = sp.simplify(b_ ** 2 * f_last.subs(q, S / b_))          # valid for Sigma >= b
d_on = [sp.simplify(F_on - S ** 2 / 2), sp.simplify(sp.diff(F_on - S ** 2 / 2, S)), sp.simplify(sp.diff(F_on - S ** 2 / 2, Xs))]
f_mid = [e for a, b, e in f_pcs if a <= sp.Rational(1, 2) <= b][0]
diff_mid = sp.nsimplify(f_mid.subs(q, sp.Rational(1, 2)) - sp.Rational(1, 8))
ok_on = all(sp.simplify(d) == 0 for d in d_on) and sp.simplify(f_last - q ** 2 / 2) == 0
check("S1", ok_on and diff_mid != 0,
      f"f = q^2/2 exactly for q >= 1 (c1(1) = {c1}, c0(1) = {c0}); F - max(Sigma,0)^2/2 and d/dSigma, d/dX vanish for "
      f"Sigma >= b; f = 0 for q <= 0 (AC21 T4, F = 0 = AC2q there); in the layer f(1/2) - 1/8 = {float(diff_mid):.4g} != 0")
# row-level equality at the clock-only point Sigma/X = 2 (planted to fail under MUTATE)
q_row = sp.Rational(2, BFAC)
f_at = [e for a, b, e in f_pcs if a <= q_row <= b][0].subs(q, q_row)
eq_row = sp.simplify((BFAC ** 2) * f_at - sp.Rational(2) ** 2 / 2) == 0
check("S1_row", eq_row, f"F(Sigma = 2X; b = {BFAC}X) = max(Sigma,0)^2/2 at the clock-only point: {eq_row}")
RES["S1"] = dict(c1_at_1=str(c1), c0_at_1=str(c0), f_half_minus_eighth=float(diff_mid), eq_at_2X=bool(eq_row), b_over_X=BFAC)

# ============================================================ S2: TC03 on-branch background, margin, c^2, G
r, A, g, r0, u, a, z = sp.symbols("r A gamma r0 u a z", positive=True)
D = (A * r - 1 - g * r ** 2) / g
A0 = (1 + g * r0 ** 2) / r0
assert sp.simplify(D.subs({A: A0, r: r0})) == 0
SX = sp.simplify((D + r ** 2) / (r ** 2 / 2))
E = sp.simplify((SX - 2).subs({r: r0 * (1 + u), A: A0 * (1 + a)}).subs(g, z / r0 ** 2))
E_lin = sp.simplify(sp.diff(E, u).subs({u: 0, a: 0}) * u + sp.diff(E, a).subs({u: 0, a: 0}) * a)
P(f"S2: Sigma/X - 2 = 2D/r^2 = {sp.factor(E)}  (r0 cancels: {r0 not in E.free_symbols}); linear part {E_lin}")
import mpmath as mpm
mpm.mp.dps = 60                                                           # 1 + u with u ~ 1e-17 needs > 17 digits
Ef = sp.lambdify((u, a, z), E, "mpmath")


def eps1(z0):
    z0 = mpm.mpf(z0); lo, hi = mpm.mpf(0), mpm.mpf("0.5")
    for _ in range(70):
        m = (lo + hi) / 2; gr = [m * (2 * mpm.mpf(i) / 20 - 1) for i in range(21)]
        worst = max(abs(Ef(uu, aa, z0)) for uu in gr for aa in gr)
        (lo, hi) = (m, hi) if worst <= mpm.mpf("0.5") else (lo, m)
    return float(lo)


ZS = [1e-17, 1e-6, 1e-2, 0.1, 0.25, 0.45]
e1 = {str(z0): eps1(z0) for z0 in ZS}
for z0 in ZS:
    P(f"   z0 = {z0:<7g}: eps1 = {e1[str(z0)]:.4e}  (eps1/z0 = {e1[str(z0)] / z0:.4f})")
# analytic: E is a rational function, E(0,0) = 0, denominator (1+u)^2 > 0 near 0 -> eps1(z0) > 0 for every z0 > 0
den = sp.denom(sp.together(E)); num = sp.numer(sp.together(E))
ok_cont = sp.simplify(num.subs({u: 0, a: 0})) == 0 and sp.simplify(den.subs({u: 0, a: 0})) != 0
H = r ** 2 / 2 + g * D ** 2 / 2                                          # r-dependent part at fixed A, P
h, R, H3 = sp.diff(H, r), sp.diff(H, r, 2), sp.diff(H, r, 3)
sub0 = {A: (1 + g * r ** 2) / r}
c2 = sp.simplify((h / (r * R)).subs(sub0).subs(g, z / r ** 2))
Gx = sp.simplify((3 * (1 - h / (r * R)) - h * H3 / R ** 2).subs(sub0).subs(g, z / r ** 2))
ok_c2 = sp.simplify(c2 - z / (z + (1 - z) ** 2)) == 0
zg = np.concatenate([np.geomspace(1e-17, 1e-3, 50), np.linspace(1e-3, 0.5, 500)])
Gv = sp.lambdify(z, Gx, "numpy")(zg)
P(f"S2: c^2 = {c2} ; G = {sp.factor(Gx)} ; min G on (0, 1/2] = {Gv.min():.4f}")
check("S2", ok_cont and all(v > 0 for v in e1.values()) and ok_c2 and Gv.min() > 0,
      "Sigma/X = 2 at D(r0,A0) = 0; Sigma/X - 2 continuous with value 0 at the background, so eps1(z0) > 0 for every z0; "
      "c^2 = z/(z+(1-z)^2) = CHAIN E4; G > 0 on (0, 1/2]")
J3 = "HOLDS" if CHK["S2"] and CHK["S1"] else "NOT SHOWN"
P(f"J3: {J3}. For eps < eps1(z0) the bootstrap box B' = B n {{|Sigma/X - 2| <= 1/2}} is compact, admissible and holds the "
  "initial range in its interior; FORMATION s4 gives T0(B') > 0, s5 gives T_k <= C_eps/k < T0(B'); every prebreak state "
  "lies in Sigma > X where A2 = A1 (S1). Note eps1 ~ z0/4: at physical z0 ~ 1e-17 TC03's family needs dr/r < ~1e-17.")
RES["S2"] = dict(E=str(sp.factor(E)), E_lin=str(E_lin), eps1=e1, c2=str(c2), G=str(sp.factor(Gx)), G_min=float(Gv.min()), J3=J3)

# ============================================================ KA1: asymmetric pulse slope ratio
t = np.linspace(1e-6, 1 - 1e-6, 2_000_001)
eta_p = lambda s: np.exp(-1 / s) / (np.exp(-1 / s) + np.exp(-1 / (1 - s)))
Aa_, Dd_, Bb_ = 0.8, 0.1, 0.1
tt = np.linspace(0, 1, 4_000_001)
psi = np.where(tt <= Aa_, eta_p(np.clip(tt / Aa_, 1e-9, 1 - 1e-9)),
               np.where(tt <= Aa_ + Dd_, 1.0, 1 - eta_p(np.clip((tt - Aa_ - Dd_) / Bb_, 1e-9, 1 - 1e-9))))
dpsi = np.gradient(psi, tt)
ratio = float(-dpsi.min() / dpsi.max())
check("KA1", abs(ratio - 8) <= 1e-6 * 8 or abs(ratio - 8) < 1e-5, f"max(-psi')/max psi' = {ratio:.8f} (TC03 pulse: 8)")
RES["KA1"] = dict(ratio=ratio)

# ============================================================ KA2: Riccati comparison catastrophe time
rows_ka2, ok_ka2 = [], True
for kap in (0.1, 1.0, 3.0):
    for C in (0.1, 1.0, 10.0):
        for P0 in (0.0, 1.0, 10.0):
            Rc = 1.01 * max(1.0, 6 * C / kap)
            for mult in (1.0, 2.0, 10.0):
                Q0 = P0 + mult * Rc
                tb_bound = 2 / (kap * Q0)
                ev = lambda tt_, y: y[0] - 1e9; ev.terminal = True
                sol = solve_ivp(lambda tt_, y: [kap * y[0] ** 2 - C * (y[0] + y[1] + 1), -kap * y[1] ** 2 + C * (y[0] + y[1] + 1)],
                                (0, 2 * tb_bound), [Q0, P0], events=ev, rtol=1e-10, atol=1e-12, max_step=tb_bound / 2000)
                tb = float(sol.t_events[0][0]) if len(sol.t_events[0]) else math.inf
                mono = bool(np.all(np.diff(sol.y[0] - sol.y[1]) >= -1e-9 * np.abs(sol.y[0]).max()))
                ok = tb <= tb_bound and mono; ok_ka2 &= ok
                rows_ka2.append(dict(kappa=kap, C=C, P0=P0, Q0=Q0, t_b=tb, bound=tb_bound, ratio=tb / tb_bound, cone_monotone=mono, ok=ok))
mr = max(x["ratio"] for x in rows_ka2)
check("KA2", ok_ka2, f"{len(rows_ka2)} comparison rows: blow-up t_b <= 2/(kappa Q0) on all (max t_b/bound = {mr:.4f}); Q - P non-decreasing")
RES["KA2"] = dict(rows=rows_ka2, max_ratio=mr)

# ============================================================ P0/P1 planted controls (classifier on a synthetic state)


def classify(sx_min, sx_max, bf=BFAC):
    if sx_min > bf * (1 + 1e-6):
        return "IN"
    if sx_max < -1e-6:
        return "OFF-SIDE"
    return "LAYER"


def fires_hom(Q0, kap=1.0, C=1.0):
    """homogeneous Sigma/X = 2 background: no source; compressive weighted gradient obeys Q' = kap Q^2 - C Q"""
    ev = lambda tt_, y: y[0] - 1e9; ev.terminal = True
    sol = solve_ivp(lambda tt_, y: [kap * y[0] ** 2 - C * y[0]], (0, 50.0), [Q0], events=ev, rtol=1e-10, atol=1e-14)
    return (len(sol.t_events[0]) > 0), (float(sol.t_events[0][0]) if len(sol.t_events[0]) else None)


f1, t1 = fires_hom(10.0); f0, _ = fires_hom(0.0)
c_p1 = classify(2.0, 2.0, 1); c_p0 = classify(2.0, 2.0, 1)
check("P1", c_p1 == "IN" and f1 and t1 <= 2 / (1.0 * 10.0), f"planted Sigma/X = 2 state with cone data Q0 = 10: {c_p1}, FIRES at {t1:.4f} <= 0.2")
check("P0", c_p0 == "IN" and not f0, f"homogeneous Sigma/X = 2 (FRW-like), Q0 = 0: {c_p0}, {'FIRES' if f0 else 'NO FIRE'}")

# ============================================================ KA3 + N1: AC10 subset with AC2q and QX19 stiffness
import tc1_runs  # noqa: E402
runs = [json.load(open(fn)) for fn in sorted(glob.glob(os.path.join(HERE, "runs", "*.json")))]
idx = {}
for x in runs:
    rr = x["job"]["row"]; idx[(rr["foot"], rr["r_kpc"], rr["kind"], x["model"], x["N"])] = x
stored = {}
for fn in glob.glob(os.path.join(REPO, "action_search_2026_11_05/AC10_nonlinear_clock/parts/*.json")):
    d = json.load(open(fn)); rr = d["row"]
    if rr.get("model") == "AC2q" and rr.get("kind") in ("phantom", "clock_only", "soft"):
        for ru in d["rungs"]:
            stored[(rr["foot"], rr["r_kpc"], rr["kind"], ru["N"])] = ru
subset = tc1_runs.subset_rows()
n_exp = len(subset) * 2 * len(tc1_runs.LADDER)
P(f"N1: {len(runs)} of {n_exp} runs on disk")
ka3_dev, n1 = [], []
for rr in subset:
    k = (rr["foot"], rr["r_kpc"], rr["kind"])
    for N in tc1_runs.LADDER:
        x = idx.get(k + ("AC2q", N)); s = stored.get(k + (N,))
        if x and s and x["t_fold_all"] is not None and s["t_fold_all"] is not None:
            ka3_dev.append(abs(x["t_fold_all"] / s["t_fold_all"] - 1))
        elif x and s:
            ka3_dev.append(0.0 if (x["t_fold_all"] is None and s["t_fold_all"] is None) else math.inf)
    a2, a4 = idx.get(k + ("AC2q", 4000)), idx.get(k + ("AC2q", 2000))
    q2, q4 = idx.get(k + ("QX19", 2000)), idx.get(k + ("QX19", 4000))
    if not (a2 and q2 and q4 and a4):
        n1.append(dict(foot=k[0], r_kpc=k[1], kind=k[2], status="MISSING")); continue
    sxmin = min(q2["sx_in_min"], q4["sx_in_min"], a2["sx_in_min"]); sxmax = max(q2["sx_in_max"], q4["sx_in_max"], a2["sx_in_max"])
    reg = classify(sxmin, sxmax)
    lay = q4["layer_in_b4"] if MUT else q4["layer_in"]
    tq, ta = q4["t_fold_all"], a2["t_fold_all"]
    fold = tq is not None and q2["t_fold_all"] is not None
    conv = fold and abs(tq / q2["t_fold_all"] - 1) <= 1e-3
    same = fold and ta is not None and abs(tq / ta - 1) <= 1e-3
    tsec = tq * rr["tau_f_s"] if fold else None
    within = fold and tsec < AGE_S
    dX = (max(q4["v_max"], a2["v_max"]) * rr["w_kms"] * 1e3 / CL) ** 2
    row = dict(foot=k[0], r_kpc=k[1], kind=k[2], Pi0_over_s2=rr["Pi0"] / rr["s2"], region=reg, sx_in_min=sxmin, sx_in_max=sxmax,
               sx_all_min=min(q4["sx_all_min"], a2["sx_all_min"]), layer_frac_interior=lay,
               layer_frac_all=q4["layer_all_b4"] if MUT else q4["layer_all"],
               t_fold_QX19=tq, t_fold_AC2q=ta, rel_QX19_AC2q=(abs(tq / ta - 1) if same or (fold and ta) else None),
               rel_ladder=(abs(tq / q2["t_fold_all"] - 1) if fold else None), converged=conv, same_as_AC2q=same,
               t_fold_s=tsec, t_fold_yr=(tsec / 3.15576e7 if tsec else None), within_age=within, X_shift_bound=dX,
               J_max_prefold=max(q4["J_max_in_prefold"] or 0, a2["J_max_in_prefold"] or 0))
    row["FIRES_IN"] = reg == "IN" and conv and same and within
    n1.append(row)
    P(f"  {k[0]:9s} {k[1]:5.0f} kpc {k[2]:10s} Pi0/s2 {row['Pi0_over_s2']:10.4g}: region {reg:8s} Sigma/X in "
      f"[{sxmin:.4g}, {sxmax:.4g}] layer {lay:.3g}; fold QX19 {tq} AC2q {ta} rel {row['rel_QX19_AC2q']} ladder {row['rel_ladder']}; "
      f"t = {('%.3g' % row['t_fold_yr']) if row['t_fold_yr'] else None} yr; "
      f"dX/X <= {dX:.1e}; FIRES_IN {row['FIRES_IN']}")
ka3_max = max(ka3_dev) if ka3_dev else math.inf
check("KA3", len(ka3_dev) == len(subset) * len(tc1_runs.LADDER) and ka3_max <= 1e-6,
      f"AC2q rerun = AC10 stored t_fold_all on {len(ka3_dev)} rung pairs, max rel dev {ka3_max:.2e} (line 1e-6)")
complete = all(x.get("status") != "MISSING" for x in n1)
check("N1_complete", complete, f"{sum(x.get('status') != 'MISSING' for x in n1)} of {len(n1)} rows graded")
fires_by_foot = {f: any(x.get("FIRES_IN") for x in n1 if x["foot"] == f) for f in FOOT}
in_rows = [x for x in n1 if x.get("region") == "IN"]
layer_rows = [x for x in n1 if x.get("region") == "LAYER"]
if MUT:
    co = [x for x in n1 if x.get("kind") == "clock_only"]
    check("MUT_detect", all(x.get("region") == "IN" for x in co),
          f"clock-only rows classified {[x.get('region') for x in co]} with planted layer 0 < Sigma < 4X (must read LAYER -> FAIL)")
RES["N1"] = dict(rows=n1, KA3_max_rel=ka3_max, fires_by_foot=fires_by_foot)

# ============================================================ N2: static region census (reported)
DATA = os.path.join(REPO, "real_research", "data")


def nu(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-300))


def census(R_m, gN, a0):
    ok = (gN > 0) & np.isfinite(gN)
    R_m, gN = R_m[ok], gN[ok]
    if len(R_m) < 3:
        return None
    Fm = R_m ** 2 * (nu(gN / a0) - 1) * gN
    rho_ph = np.gradient(Fm, R_m) / (4 * math.pi * G_SI * R_m ** 2)
    rho_de = a0 ** 2 / (KAPPA ** 2 * CL ** 2 * G_SI)
    return 2 + rho_ph / rho_de


N2 = {}
for foot, a0 in FOOT.items():
    allsx = []
    for fn in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
        try:
            d = np.genfromtxt(fn, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        Rm = d[:, 0] * 3.0857e19
        VB2 = np.sign(d[:, 3]) * d[:, 3] ** 2 + 0.5 * d[:, 4] ** 2 + 0.7 * d[:, 5] ** 2
        sx = census(Rm, VB2 * 1e6 / Rm, a0)
        if sx is not None:
            allsx.append(sx)
    s = np.concatenate(allsx)
    N2[f"SPARC_{foot}"] = dict(n_gal=len(allsx), n_pts=int(s.size), frac_in=float(np.mean(s > BFAC)),
                               frac_layer=float(np.mean((s > 0) & (s < BFAC))), frac_off=float(np.mean(s < 0)),
                               min_sx=float(s.min()), median_sx=float(np.median(s)))
    try:
        from astropy.io import fits
        xs, ncl, gas_only = [], 0, []
        for cdir in sorted(glob.glob(os.path.join(DATA, "xcop", "*"))):
            nm = os.path.basename(cdir)
            if not os.path.isdir(cdir):
                continue
            with fits.open(os.path.join(cdir, f"{nm}_fgas_profile.fits")) as h:
                gas = h[1].data.copy(); r5 = h[1].header["R500"]
            gr = np.asarray(gas["RADIUS"], float) * r5; gM = np.asarray(gas["MGAS"], float)
            okg = np.isfinite(gM) & (gM > 0); gr, gM = gr[okg], gM[okg]
            sf = os.path.join(cdir, f"{nm}_mstar.fits")
            if os.path.exists(sf):
                with fits.open(sf) as h:
                    st = h[2].data.copy()
                sr = np.asarray(st["RADIUS"], float); sM = np.asarray(st["MSTAR"], float); oks = np.isfinite(sM) & (sM > 0)
                Ms = np.interp(gr, sr[oks], sM[oks])
            else:                                            # no stellar file on disk: gas only (listed)
                Ms = 0.0 * gr; gas_only.append(nm)
            Mb = (gM + Ms) * 1.989e30; Rm = gr * 3.0857e19
            sx = census(Rm, G_SI * Mb / Rm ** 2, a0)
            if sx is not None:
                xs.append(sx); ncl += 1
        s = np.concatenate(xs)
        N2[f"XCOP_{foot}"] = dict(n_cl=ncl, gas_only=gas_only, n_pts=int(s.size), frac_in=float(np.mean(s > BFAC)),
                                  frac_layer=float(np.mean((s > 0) & (s < BFAC))), frac_off=float(np.mean(s < 0)),
                                  min_sx=float(s.min()), median_sx=float(np.median(s)))
    except Exception as ex:                                  # frozen: X-COP census NO VERDICT if files do not load
        N2[f"XCOP_{foot}"] = dict(status="NO VERDICT", error=repr(ex))
for k_, v_ in N2.items():
    P(f"N2 {k_}: {v_}")
P("N2 reading: static configurations are time-independent regular solutions; no finite-time catastrophe can fire on them.")
RES["N2"] = N2

# ============================================================ other configurations, verdict
RES["other"] = dict(FRW="IN (Sigma/X = 2), Q = 0: NO FIRE", linear_growth="IN for dips d >= -X (frw_pert); linear: NO FIRE",
                    moving_sun="NO VERDICT (AC15 NO VERDICT; nonlinear run in another lane)")
gates_ok = all(CHK[k_] for k_ in ("S1", "S2", "KA1", "KA2", "KA3", "P0", "P1", "N1_complete"))
if not gates_ok:
    label = "NO VERDICT"
elif J3 == "HOLDS" and all(fires_by_foot.values()):
    label = "FIRES"
elif not any(x.get("region") in ("IN", "OFF-SIDE") and x.get("within_age") and x.get("converged") for x in n1):
    label = "UNCONDITIONAL"
else:
    label = "NO VERDICT"
fire_rows = [f"{x['foot']} {x['r_kpc']:.0f} kpc {x['kind']}" for x in n1 if x.get("FIRES_IN")]
P(f"LABEL: {label}. J3 {J3}. Rows firing inside Sigma > X: {fire_rows}")
P("QX19 rows lost (frozen rule): none of the 10 PASS rows asserts global regularity; well-posedness re-scoped to local-in-time; "
  "'Nonlinear fold' row takes the N1 result." if label == "FIRES" else "QX19 rows: see criteria for this label.")
RES.update(label=label, J3=J3, checks=CHK, fire_rows=fire_rows, mutate=MUT)
open(os.path.join(HERE, f"tc1{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"tc1{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if all(CHK.values()) else 1)
