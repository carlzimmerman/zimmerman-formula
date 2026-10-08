#!/usr/bin/env python3
"""CFG452: T15/T16 settling budget with a0(z) = kappa c sqrt(G rho_DE(z)) as a moving target.  (criteria: FROZEN_CRITERIA.md, fa8a989af)

dM/dt = Gamma (S(t) M_b - M), M(z=2) = 0  ->  M/M_b = Gamma tau * int_0^1 S(u) exp(-Gamma tau (1-u)) du,  u = fractional time since z = 2.
a0(z) = a0_footing * r(z), r = p13c DESI DR2 chain median of sqrt(rho_DE(z)/rho_DE0).  Footings never pooled.
Run: python3 cfg452_moving_a0z.py  |  CFG452_MUTATE=1 plants r(z>0) = 0.5.  Local data only.
"""
import csv, json, math, os, sys
import numpy as np

MUT = os.environ.get("CFG452_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
lines = []
def say(s=""):
    lines.append(s); print(s)

G = 6.674e-11; GYR = 3.156e16; TAU = 10.3 * GYR; KPC = 3.086e19
LAM = 0.028; RHO_R500 = 1.55e-24
RATE_R500_TAU = math.sqrt(4 * math.pi * G * RHO_R500) * TAU
RATE_MW200_TAU = math.sqrt(4 * math.pi * G * (200e3 ** 2 / (4 * math.pi * G * (30 * KPC) ** 2))) * TAU

# ---- time map u(z) (flat LCDM Om 0.30, H0 70; shape only, tau held)
OM = 0.30
def t_of_z(z):
    return math.asinh(math.sqrt((1 - OM) / OM) * (1 + z) ** -1.5)       # proportional to cosmic time
U = np.linspace(0.0, 1.0, 4001)
t2, t0 = t_of_z(2.0), t_of_z(0.0)
zg = np.linspace(0, 2, 20001); tg = np.array([t_of_z(z) for z in zg])
Z_U = np.interp(t2 + U * (t0 - t2), tg[::-1], zg[::-1])

# ---- DE curves r(z)
P13 = list(csv.DictReader(open(os.path.join(REPO, "sonnet55_push", "puzzle_32pi", "p13c_desi_dr2_chains_a0z.csv"))))
def curve(fit, col="q50"):
    zz = np.array([float(r["z"]) for r in P13 if r["fit"] == fit]); rr = np.array([float(r[col]) for r in P13 if r["fit"] == fit])
    return lambda z: np.interp(z, zz, rr)
CURVES = {"flat (w = -1)": lambda z: np.ones_like(np.asarray(z, float)),
          "DESI+CMB+Pantheon+ (primary)": curve("DESI+CMB+Pantheon+"),
          "Pantheon+ q16": curve("DESI+CMB+Pantheon+", "q16"), "Pantheon+ q84": curve("DESI+CMB+Pantheon+", "q84"),
          "DESI+CMB+Union3": curve("DESI+CMB+Union3"), "DESI+CMB+DESY5": curve("DESI+CMB+DESY5"), "DESI+CMB (no SN)": curve("DESI+CMB")}
if MUT:
    CURVES = {"flat (w = -1)": CURVES["flat (w = -1)"], "MUTATE r(z>0) = 0.5": lambda z: np.where(np.asarray(z, float) > 0, 0.5, 1.0)}
checks = {}
c2 = [abs(float(CURVES.get("DESI+CMB+Pantheon+ (primary)", curve("DESI+CMB+Pantheon+"))(2.0)) - 0.8779) < 1e-3]
c2 += [abs(float(curve(f)(2.5)) - v) < 1e-3 for f, v in (("DESI+CMB+Pantheon+", 0.827), ("DESI+CMB+Union3", 0.782), ("DESI+CMB+DESY5", 0.798))]
checks["C2_p13c_inputs"] = bool(all(c2))

# ---- moving-target settling
def S_u(Mb, R, a0, r):
    a0u = a0 * r(Z_U)
    return 1.0 / (np.exp(np.sqrt(G * Mb * 1.989e30 / a0u) / KPC / R) - 1.0)
def settled(Su, k):                       # k = Gamma tau
    return float(np.trapz(k * Su * np.exp(-k * (1 - U)), U))
def lam_max(x, Su, rate_tau):
    if x > Su[-1]:                        # lambda -> inf limit is today's S
        return math.inf
    lo, hi = 0.0, 1.0
    while settled(Su, hi * rate_tau) < x:
        hi *= 2
        if hi > 1e4:
            return math.inf
    for _ in range(100):
        m = 0.5 * (lo + hi)
        if settled(Su, m * rate_tau) < x: lo = m
        else: hi = m
    return 0.5 * (lo + hi)

def mw_x(Mb, V):
    return ((V * 1e3) ** 2 * (30 * KPC) / G - Mb * 1.989e30) / (Mb * 1.989e30)
def v_infeasible(a0, r, Mb=7.0e10):
    Su = S_u(Mb, 30.0, a0, r); lim = Su[-1]                   # lambda -> inf limit: today's S
    lo, hi = 150.0, 300.0
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if mw_x(Mb, m) <= lim: lo = m
        else: hi = m
    return 0.5 * (lo + hi)

D450 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG450_xcop_gas_radius_audit", "cfg450_results.json")))["deficits"]
def xs(fk):
    d = D450[fk]
    return [d["0.0"]["groups"]["med"], d["0.3"]["groups"]["med"], d["0.0"]["clusters_R500"]["med"], d["0.3"]["clusters_R500"]["med"]]

def run(a0, x, r):
    xg0, xg3, xc0, xc3 = x
    Sm, Sg, Sc = S_u(7.0e10, 30.0, a0, r), S_u(6e12, 554.0, a0, r), S_u(2.8e13, 985.0, a0, r)
    kR, kM = LAM * RATE_R500_TAU, LAM * RATE_MW200_TAU
    rows = {f"MW30_V{V}": xv - settled(Sm, kM) for V, xv in ((188, 1.48), (200, 1.8), (230, 2.7))}
    rows.update(groups_b0=xg0 - settled(Sg, kR), groups_b03=xg3 - settled(Sg, kR), clusters_b0=xc0 - settled(Sc, kR), clusters_b03=xc3 - settled(Sc, kR))
    mw = {}
    for Mb in (7.0e10, 1.0e11):
        SmB = S_u(Mb, 30.0, a0, r)
        for V in (188, 200, 230):
            xv = mw_x(Mb, V); feas = xv <= SmB[-1]
            rt = math.sqrt(4 * math.pi * G * (V * 1e3) ** 2 / (4 * math.pi * G * (30 * KPC) ** 2)) * TAU
            mw[f"Mb{Mb:.0e}_V{V}"] = dict(x=xv, feasible=bool(feas), lam_max=lam_max(xv, SmB, rt) if feas else math.inf)
    oth = {"groups_b0": lam_max(xg0, Sg, RATE_R500_TAU), "groups_b03": lam_max(xg3, Sg, RATE_R500_TAU),
           "clusters_b0": lam_max(xc0, Sc, RATE_R500_TAU), "clusters_b03": lam_max(xc3, Sc, RATE_R500_TAU)}
    inter = {}
    for lab, keys in (("frozen_Mb7e10", [k for k in mw if k.startswith("Mb7e+10")]), ("verbatim_both_Mb", list(mw))):
        mwl = [mw[k]["lam_max"] for k in keys if mw[k]["feasible"]]
        w = [[min(mwl), max(mwl)] if mwl else [math.inf, math.inf], [oth["groups_b0"], oth["groups_b03"]], [oth["clusters_b0"], oth["clusters_b03"]]]
        lo, hi = max(v[0] for v in w), min(v[1] for v in w)
        inter[lab] = dict(mw=w[0], inter=[lo, hi], nonempty=bool(lo <= hi))
    gap = 0.028 / oth["clusters_b03"]
    g = rows["groups_b03"]
    return dict(rows=rows, mw=mw, others=oth, inter=inter, V1=bool(rows["clusters_b0"] < 0 and rows["clusters_b03"] < 0),
                V2=[g, "knife-edge" if abs(g) < 0.15 else ("negative" if g < 0 else "positive")], V3=v_infeasible(a0, r),
                V4=[gap, "STANDS" if gap >= 1.5 else ("WEAKENED" if gap >= 1.0 else "BREAKS")],
                S_today=[float(Sm[-1]), float(Sg[-1]), float(Sc[-1])], S_eff=[settled(Sm, kM) / (1 - math.exp(-kM)), settled(Sg, kR) / (1 - math.exp(-kR)), settled(Sc, kR) / (1 - math.exp(-kR))])

# ---- C1: flat reproduces CFG451
C451 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG451_t15_t16_own_footings", "cfg451_results.json")))["rows"]
err = []
for fk, a0 in A0.items():
    ref = next(v for k, v in C451.items() if k.startswith(fk))
    o = run(a0, xs(fk), CURVES["flat (w = -1)"])
    err += [abs(o["rows"][k] - ref["T15"]["rows"][k]) for k in ref["T15"]["rows"]]
    err += [abs(o["V3"] - ref["V3"]) / 100, abs(o["V4"][0] - ref["V4"][0])]
    err += [abs(o["others"][k] - ref["T16"]["others"][k]) for k in o["others"]]
    for k, v in ref["T16"]["mw"].items():
        if v["feasible"]:
            err.append(abs(o["mw"][k]["lam_max"] - v["lam_max"]))
checks["C1_flat_reproduces_cfg451"] = bool(max(err) < 1e-6)

say(f"CFG452 settling with a0(z) tracking rho_DE(z)  MUTATE={MUT}")
say(f"r(z) at z = 0.4 / 1 / 2: " + "; ".join(f"{k} {float(f(0.4)):.3f}/{float(f(1.0)):.3f}/{float(f(2.0)):.3f}" for k, f in CURVES.items()))
say("")
OUT = {}
for fk, a0 in A0.items():
    say(f"{fk} footing (a0(0) = {a0:.4e}; CFG450 deficits groups {xs(fk)[0]:.3f}/{xs(fk)[1]:.3f}, clusters {xs(fk)[2]:.4f}/{xs(fk)[3]:.4f})")
    OUT[fk] = {}
    for cn, r in CURVES.items():
        o = run(a0, xs(fk), r); OUT[fk][cn] = o
        fz, vb = o["inter"]["frozen_Mb7e10"], o["inter"]["verbatim_both_Mb"]
        say(f"  {cn:30s} clusters {o['rows']['clusters_b0']:+.3f}/{o['rows']['clusters_b03']:+.3f}  groups b0.3 {o['V2'][0]:+.3f} ({o['V2'][1]})"
            f"  MW30 V188/200/230 {o['rows']['MW30_V188']:+.3f}/{o['rows']['MW30_V200']:+.3f}/{o['rows']['MW30_V230']:+.3f}  V3 {o['V3']:.1f} km/s")
        say(f"  {'':30s} S_eff/S_today MW/gr/cl {o['S_eff'][0]/o['S_today'][0]:.4f}/{o['S_eff'][1]/o['S_today'][1]:.4f}/{o['S_eff'][2]/o['S_today'][2]:.4f}"
            f"  cluster window [{o['others']['clusters_b0']:.4f}, {o['others']['clusters_b03']:.4f}]  V4 {o['V4'][0]:.2f}x {o['V4'][1]}"
            f"  V5 frozen {'nonempty' if fz['nonempty'] else 'EMPTY'} [{fz['inter'][0]:.4f}, {fz['inter'][1]:.4f}], verbatim {'nonempty' if vb['nonempty'] else 'EMPTY'} [{vb['inter'][0]:.4f}, {vb['inter'][1]:.4f}]")
    say("")
prim = "MUTATE r(z>0) = 0.5" if MUT else "DESI+CMB+Pantheon+ (primary)"
changed = any(OUT[fk][prim]["V1"] != OUT[fk]["flat (w = -1)"]["V1"] or OUT[fk][prim]["V4"][1] != OUT[fk]["flat (w = -1)"]["V4"][1] for fk in A0)
head = "a0(z) MATTERS" if changed else "a0(z) DOES NOT CHANGE THE BUDGET'S VERDICT"
shift = {fk: OUT[fk][prim]["rows"]["clusters_b0"] - OUT[fk]["flat (w = -1)"]["rows"]["clusters_b0"] for fk in A0}
say(f"HEADLINE ({prim} vs flat): {head}; cluster b=0 shift " + ", ".join(f"{k} {v:+.4f}" for k, v in shift.items()))
if MUT:
    checks["MUTATE_history_seen"] = bool(all(v > 0.1 for v in shift.values()))
say("checks: " + json.dumps(checks))
json.dump(dict(mutate=MUT, headline=head, shift=shift, results=OUT, checks=checks), open(os.path.join(HERE, f"cfg452_results{TAG}.json"), "w"), indent=1, default=float)
ok = all(checks.values())
print("<LANE> COMPLETE: all checks PASS" if ok else "<LANE> COMPLETE: -- SOME CHECKS FAIL")
sys.exit(0 if ok else 1)
