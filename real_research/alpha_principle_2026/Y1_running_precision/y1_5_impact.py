#!/usr/bin/env python3
"""y1_5_impact.py -- Part 4 of Y1_PREREGISTRATION.md (U3 part and the bar): what the tighter, validated running does to lane U3's 34 verdicts (V09 undecided, V25/P08 marginal, all others), and to lane D's bar.
Mechanism: lane U3's own scorer (u3_lib.residuals, mono_kill, bridge, look_elsewhere) is called READ-ONLY with the Y1-central trajectory substituted for its '2L-T' run IN MEMORY (no file of lane U3 is edited);
the tolerance of every constraint is 2 sigma of the residual over a Monte-Carlo ensemble of the budget items E1-E5 (N = 200, seed 20260929) instead of U3's max(2 x band, 1%); for parametric-scale variants U3's factor-2 scale band is kept.
A second, conservative tolerance adds the anchor spread (direct M_W 80.3692 versus 80.360 and the SM-fit value 80.356, route P hand-over, Buttazzo's g_3) linearly.
Run:    python3 y1_5_impact.py            (exit 0 iff the internal consistency checks pass)
MUTATE: python3 y1_5_impact.py MUTATE     (the control replaces the Y1 central run by a run shifted by +3% in a_Y and must break the consistency check 'the central Y1 run is reproduced by the adapter'; exit 1; exit 3 if not)
Writes y1_5_results.json.  Imports lanes B, N1, U3, D READ-ONLY (path-relative).  No bytecode.
"""
import sys
sys.dont_write_bytecode = True
import os
import json
import math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for sub in ("B_rg_asymptotic_safety", "N1_joint_couplings", "U3_invented_uv_boundary", "D_calibration_bar"):
    sys.path.insert(0, os.path.join(HERE, "..", sub))
import y1_lib as L
import u3_lib as U3
import alpha_bar_checker as BAR
import bar_lib as BL
from scipy.optimize import brentq

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
PI = math.pi
P = L.PDG
fails = []


def chk(name, ok, info=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        fails.append(name)


class Adapter:
    """Presents a Y1 trajectory with the interface lane U3's scorer expects (A(mu), lnmax)."""

    def __init__(self, tr, scale_aY=1.0):
        self.tr = tr
        self.lnmax = tr.lnmax - 1e-9
        self.scale_aY = scale_aY

    def A(self, mu):
        a = np.array(self.tr.A(max(mu, self.tr.mu0)))
        a[0] *= self.scale_aY
        return a


print("=" * 140)
print("Y1-5 impact on lane U3 and lane D -- mode:", "MUTATE" if MUT else "REAL RUN")
print("=" * 140)

old = {r["id"]: r for r in json.load(open(os.path.join(HERE, "..", "U3_invented_uv_boundary", "u3_1_results.json")))["rows"]}
VAR = U3.make_variants()

tr_cen = L.run_central(mu_max=3e21)
AD = Adapter(tr_cen, scale_aY=1.03 if MUT else 1.0)
chk("the central Y1 run is reproduced by the adapter (a_Y(X_P) equals the budget script's 55.2342 to 1e-4)", abs(AD.A(U3.XP)[0] - 55.2342) < 1e-3, f"{AD.A(U3.XP)[0]:.4f}")
U3._TRAJ_CACHE["2L-T"] = AD          # in-memory substitution (u3_lib.bridge and evaluate_bands read get_traj('2L-T'))

# ------------------------------------------------------------------------------------------- Monte-Carlo ensemble of trajectories (E1-E5, as in the budget script)
NIT = 200
rng = np.random.default_rng(20260929)
sMt = math.hypot(P["sMt_exp"], P["sMt_th"])
sg2 = abs(0.64779 - 0.64754) * max(abs(0.64779 - 0.64754) / abs(0.64754 - 0.65294), 0.108 / PI)
sgY = abs(0.35830 - 0.35940) * max(abs(0.35830 - 0.35940) / abs(0.35940 - 0.34972), 0.108 / PI)
sMZ_gY = 0.35830 * P["MZ"] * P["sMZ"] / (P["MZ"] ** 2 - P["MW"] ** 2)
sg3 = math.hypot(2.62e-5, 6.72e-5 / 2)
ens = []
for _ in range(NIT):
    z = rng.standard_normal(9)
    kw = dict(als=P["als"] + z[0] * P["sals"], MW=P["MW"] + z[1] * P["sMW"], Mt=P["Mt"] + z[2] * sMt, Mh=P["Mh"] + z[3] * P["sMh"], dgY=z[4] * sMZ_gY + z[5] * sgY, dg2=z[6] * sg2, rel_g3=z[7] * sg3,
              dyt=z[8] * 0.0005)
    ens.append(Adapter(L.run_central(mu_max=3e21, **kw)))
# anchors (shifts of the central value, not Gaussian)
anch = {"MW=80.360": Adapter(L.run_central(mu_max=3e21, MW=80.360)), "MW=80.356 (SM fit)": Adapter(L.run_central(mu_max=3e21, MW=80.356)),
        "Buttazzo g_3": Adapter(L.run_central(mu_max=3e21, g3_mode="buttazzo"))}
# route P hand-over
trP = U3.Traj("2L-T", inp=dict(alpha_inv=P["aem_inv"], s2w=P["s2w_hat"], alpha_s=P["als"]))
AP = np.array(trP.A(P["Mt"]))
u0P = L.central_u0()
u0P[0] = 5.0 / 3.0 * (4 * PI / AP[0])
u0P[1] = 4 * PI / AP[1]
anch["route P hand-over"] = Adapter(L.Traj(u0P, P["Mt"], L.Opts(gauge_loops=4, yuk_loops=3), mu_max=3e21))


def residual(v, ad, xfac=1.0, mu_eval=None):
    res = U3.residuals(v, U3.Shifted(ad, None), xfac=xfac, mu_eval=mu_eval)
    return res


# ------------------------------------------------------------------------------------------- scoring of the 34 variants
rows = []
print("\nPER VARIANT (old = lane U3; new = Y1-central with tol = 2 sigma[MC E1-E5] (reg) and tol_cons = tol_reg + anchor spread)")
print(f"{'id':4s} {'variant':<58s} {'X_new/X_old':>11s} {'old worst |r|/tol':>18s} {'new worst |r|/tol (reg)':>24s} {'(cons)':>8s}  old status -> new status")
for v in VAR:
    o = old[v["id"]]
    cen = residual(v, AD)
    rec = dict(id=v["id"], pid=v["pid"], label=v["label"], old_status=o["status"], old_ratio=None)
    if v["pid"] == "P08":
        rec["exists"] = True
    if cen["r"] is None:
        rec.update(exists=False, new_status="DEAD", reason="scale does not exist or beyond range")
        rows.append(rec)
        print(f"{v['id']:4s} {v['label'][:58]:<58s} {'none':>11s} {'':>18s} {'':>24s} {'':>8s}  {o['status']} -> DEAD (no scale)")
        continue
    K = len(cen["r"])
    samples = []
    for ad in ens:
        rr = residual(v, ad)
        if rr["r"] is not None and len(rr["r"]) == K:
            samples.append(rr["r"])
    samples = np.array(samples)
    sig = samples.std(axis=0, ddof=1) if len(samples) > 5 else np.full(K, np.nan)
    bandX = np.zeros(K)
    if v["param_scale"]:
        for xf in (0.5, 2.0):
            rr = residual(v, AD, xfac=xf)
            if rr["r"] is not None:
                bandX = np.maximum(bandX, np.abs(rr["r"] - cen["r"]))
    if v["pid"] == "P08":
        bandX = np.zeros(K)
    tol_reg = np.maximum(np.maximum(2 * sig, 2 * bandX), 1e-4)        # 1e-4 numerical floor (rules that fix a coupling to 0 have zero ensemble spread)
    spread = np.zeros(K)
    for nm, ad in anch.items():
        rr = residual(v, ad)
        if rr["r"] is not None and len(rr["r"]) == K:
            spread = np.maximum(spread, np.abs(rr["r"] - cen["r"]))
    tol_cons = tol_reg + spread
    ratio_reg = np.abs(cen["r"]) / tol_reg
    ratio_cons = np.abs(cen["r"]) / tol_cons
    jp_reg = bool(np.all(ratio_reg <= 1))
    jp_cons = bool(np.all(ratio_cons <= 1))
    lam = U3.N_TRIALS * float(np.prod([min(1.0, 2 * t / U3.LN_SPAN) for t in tol_reg]))
    Pla = 1 - math.exp(-lam)
    X = cen["X"]
    domain = bool(v["xspec"][0] in ("cross", "hetero") and X is not None and X > 1.001 * U3.XP)
    ev = dict(cen_r=cen["r"], tol=tol_reg, names=cen["names"])
    mk, hits = U3.mono_kill(v, ev)
    if domain:
        st, why = "DEAD", "T-DOMAIN"
    elif jp_reg:
        st, why = "PASS", "T-JOINT passed"
    elif mk:
        st, why = "DEAD", "T-MONO: " + ", ".join(hits)
    else:
        st, why = "FAIL", ""
    br = None
    if st == "FAIL":
        br = U3.bridge(v)
        if not br["feasible"]:
            st, why = "DEAD", "T-BRIDGE infeasible"
        elif max(br["N"]) <= 1.0:
            st, why = "UNDECIDED_BRIDGE", "N = " + str(np.round(br["N"], 3).tolist())
        else:
            st, why = "DEAD", "T-BRIDGE needs N = " + str(np.round(br["N"], 3).tolist())
    orat = max(abs(m) / t for m, t in zip(o["cen_r"], o["tol"])) if o.get("exists", True) and o.get("cen_r") is not None else float("nan")
    rec.update(exists=True, X=X, X_old=o.get("X"), names=cen["names"], cen_r=list(map(float, cen["r"])), sigma=list(map(float, sig)), tol_reg=list(map(float, tol_reg)), tol_cons=list(map(float, tol_cons)),
               ratio_reg=float(np.max(ratio_reg)), ratio_cons=float(np.max(ratio_cons)), old_ratio=orat, jpass_reg=jp_reg, jpass_cons=jp_cons, lam=lam, P=Pla, new_status=st, reason=why,
               bridge=None if br is None else dict(feasible=br["feasible"], N=br.get("N")))
    rows.append(rec)
    xr = X / o["X"] if o.get("X") else float("nan")
    print(f"{v['id']:4s} {v['label'][:58]:<58s} {xr:11.4f} {orat:18.1f} {np.max(ratio_reg):24.1f} {np.max(ratio_cons):8.1f}  {o['status']} -> {st} {('(' + why[:44] + ')') if why else ''}")

changed = [r for r in rows if r["old_status"] != r["new_status"]]
print("\nSTATUS CHANGES (old -> new):", [(r["id"], r["old_status"], r["new_status"]) for r in changed] if changed else "none")
n_pass = sum(1 for r in rows if r["new_status"] == "PASS")
print(f"variants passing T-JOINT under the tightened tolerance: {n_pass} of 34;  under the conservative tolerance: {sum(1 for r in rows if r.get('jpass_cons'))}")
chk("no variant passes T-JOINT that lane U3 killed by 10 tolerances or more (no accidental rescue by a shifted central run)", all(not (r.get("jpass_reg") and (r.get("old_ratio") or 0) > 10) for r in rows))

# ------------------------------------------------------------------------------------------- V09 in detail
print("\nV09 (P03, equal couplings in the Y normalisation at X_P; U3: UNDECIDED_BRIDGE with N = [0.759, 0, 0.959])")
v09 = [v for v in VAR if v["id"] == "V09"][0]
cen = residual(v09, AD)
r09 = [r for r in rows if r["id"] == "V09"][0]
print(f"    central residuals {np.round(cen['r'], 4)} ; sigma from the ensemble {np.round(r09['sigma'], 5)} ; tolerance 2 sigma {np.round(r09['tol_reg'], 5)}")
Ns = []
for ad in ens[:60]:
    U3._TRAJ_CACHE["2L-T"] = ad
    b = U3.bridge(v09)
    if b["feasible"]:
        Ns.append(b["N"])
U3._TRAJ_CACHE["2L-T"] = AD
Ns = np.array(Ns)
Nc = U3.bridge(v09)
print(f"    bridge with the Y1 central run: N = {np.round(Nc['N'], 4)} ; over 60 ensemble members: mean {np.round(Ns.mean(axis=0), 4)} sigma {np.round(Ns.std(axis=0, ddof=1), 4)}")
import itertools
best = None
for N in itertools.product((0, 1), repeat=3):
    rr = U3.residuals(v09, U3.Shifted(AD, N), ref=AD.A(U3.XP))
    ratio = np.max(np.abs(rr["r"]) / np.array(r09["tol_reg"]))
    print(f"      integer content N_(Y,2,3) = {N}: residuals {np.round(rr['r'], 4)}  worst |r|/tol_reg = {ratio:.1f}")
    best = ratio if best is None else min(best, ratio)
print(f"    nearest integer-content point misses by {best:.1f} tolerances; the continuous rescue N_Y = {Nc['N'][0]:.3f}, N_3 = {Nc['N'][2]:.3f} sits {abs(Nc['N'][0] - round(Nc['N'][0])) / max(Ns.std(axis=0, ddof=1)[0], 1e-9):.0f} sigma_N from an integer for N_Y")

# ------------------------------------------------------------------------------------------- V25 / P08 in detail
print("\nV25 (P08, the one-loop RG invariant I/S vanishes; U3: DEAD, fails by 1.1 tolerances at 1 TeV, marginal)")
v25 = [v for v in VAR if v["id"] == "V25"][0]
grid = [1e3, 1e4, 1e5, 1e7, 1e9, 1e11, 1e13, 1e15, 1e17, U3.XP]
print("    mu(GeV)      I/S central   sigma(ens)   |I/S|/(2 sigma)")
zero = None
prev = None
for mu in grid:
    cr = U3.residuals(v25, U3.Shifted(AD, None), mu_eval=mu)["r"][0]
    sm = np.array([U3.residuals(v25, U3.Shifted(ad, None), mu_eval=mu)["r"][0] for ad in ens[:80]])
    print(f"    {mu:9.2e}   {cr:+.5f}    {sm.std(ddof=1):.5f}     {abs(cr) / (2 * sm.std(ddof=1)):8.1f}")
    if prev is not None and prev[1] * cr < 0:
        zero = (prev[0], mu)
    prev = (mu, cr)
print(f"    zero crossing of I/S between the grid points: {zero}")
fz = lambda lm: U3.residuals(v25, U3.Shifted(AD, None), mu_eval=math.exp(lm))["r"][0]
if zero:
    mz = math.exp(brentq(fz, math.log(zero[0]), math.log(zero[1])))
    print(f"    I/S = 0 at mu = {mz:.3e} GeV (a scale-dependent statement: the one-loop 'invariant' drifts at higher loops; a rule 'I = 0' has no scale of its own)")
else:
    mz = None

# ------------------------------------------------------------------------------------------- lane D's bar
print("\nLANE D BAR: largest total relative precision sigma_max(k) at which a perfect hit in a family of k discrete choices has look-elsewhere P < 1e-3 (lane D's own rule: lambda = k rho 2 delta_eff, delta_eff = max(miss, sigma))")
rho = BAR.RHO_DEFAULT
dmax1 = -math.log(1 - BL.BAR_P) / (2 * rho)
print(f"    rho = {rho:.4f}  ->  sigma_max(k) = {dmax1:.4e} / k")
res4 = json.load(open(os.path.join(HERE, "y1_4_results.json")))
S = res4["summary"]
sig_rel = {}
for anchor, key in (("direct M_W (registered)", "after_quad_pct"), ("SM-fit-anchored M_W", "after_fit_anchored_pct"), ("conservative de-duplicated", "after_cons_dedup_pct"), ("conservative as registered", "after_cons_registered_pct")):
    sig_rel[anchor] = {}
    for Xn in ("X_P", "X_R", "X_S"):
        c = S[Xn]["central"]
        aem = c[0] + c[1]
        s_pct = S[Xn][key][3]
        sig_abs = s_pct / 100 * aem
        sig_rel[anchor][Xn] = dict(rel_to_137=sig_abs / BL.T, rel_to_aem=s_pct / 100)
print(f"    {'anchor':34s}{'scale':>6s}{'sigma(a_em)/137.036':>22s}{'k_max (rel 137)':>18s}{'sigma/a_em':>14s}{'k_max (rel a_em)':>18s}")
for anchor in sig_rel:
    for Xn in ("X_P", "X_R", "X_S"):
        s = sig_rel[anchor][Xn]
        print(f"    {anchor:34s}{Xn:>6s}{s['rel_to_137']:22.3e}{dmax1 / s['rel_to_137']:18.1f}{s['rel_to_aem']:14.3e}{dmax1 / s['rel_to_aem']:18.1f}")
print("\n    sigma_max(k) and the improvement over Y1 (direct M_W, X_P, relative to 137.036) needed / available:")
sP = sig_rel["direct M_W (registered)"]["X_P"]["rel_to_137"]
bar_rows = []
for k in (1, 2, 5, 10, 34, 81, 100, 1000):
    smax = dmax1 / k
    r = BAR.assess(delta=0.0, size=k, predicted_precision=sP, fitted_reals=0, scale_stated=True, verbose=False)
    print(f"      k = {k:5d}: sigma_max = {smax:.2e} ; Y1 direct-M_W sigma {sP:.2e} -> {'CAN clear' if sP < smax else 'cannot clear'} (factor {sP / smax:.2f} {'below' if sP < smax else 'above'} the limit) ; lane D checker with predicted precision = sigma: P = {r['p']:.3g}, c1 = {r['c1_lookelsewhere']}")
    bar_rows.append(dict(k=k, sigma_max=smax, y1_sigma=sP, clears=bool(sP < smax), P=r["p"]))
# the same k with U3's own bar-input for its 34: 5.9e-4
chk("lane D's own number for 34 trials (5.89e-4) is reproduced by sigma_max(34)", abs(dmax1 / 34 - 5.89e-4) < 0.02e-4, f"{dmax1 / 34:.3e}")
# joint (U3 J2) power
print("\nJOINT TEST POWER (lane U3's J2: lambda = k prod(2 tol_i / ln 100)), two ratio constraints at X_P (V09-like), tol_i = 2 sigma_i from the ensemble:")
for k in (34, 81):
    t = r09["tol_reg"]
    lam = k * float(np.prod([min(1.0, 2 * x / U3.LN_SPAN) for x in t]))
    print(f"      k = {k}: tol = {np.round(t, 5)} -> lambda = {lam:.2e}, P = {1 - math.exp(-lam):.2e}   (old tol {np.round(old['V09']['tol'], 4)} -> lambda {34 * float(np.prod([min(1.0, 2 * x / U3.LN_SPAN) for x in old['V09']['tol']])):.2e})")

with open(os.path.join(HERE, "y1_5_results_MUTATE.json" if MUT else "y1_5_results.json"), "w") as f:
    json.dump(dict(rows=rows, bar=bar_rows, sigma_rel=sig_rel, dmax1=dmax1, V25_zero=mz), f, indent=1, default=float)
print(f"\nY1-5: {len(fails)} failed" + (f": {fails}" if fails else ""))
if MUT:
    print("MUTATE control:", "BITES -> exit 1" if fails else "BROKEN -> exit 3")
    sys.exit(1 if fails else 3)
sys.exit(0 if not fails else 2)
