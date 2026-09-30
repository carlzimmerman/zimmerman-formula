#!/usr/bin/env python3
"""CFG220 -- the CRISTAL outer-radius decomposition on the INDEPENDENT baryon route (SED M* + dust gas), class A only (the six dust detections), and the shared gas calibration that would reverse it.
Frozen criteria: FROZEN_CRITERIA.md here (2e025c40e), committed before the independent-route numbers.  kappa = 1/2 FITTED, NOT DERIVED.  Author decompositions, not a direct a0 measurement.
No sentence says the data favour a framework.  Reuses CFG213's data block and functions (cfg213_two_sided.py exec'd read-only up to its BINS definition).
Run:  python3 campaign_fresh_gravity/CFG220_cristal_outer_independent/cfg220_outer_independent.py        (MUTATE=1: D x 1.5)
"""
import os, sys, io, re, json, math, contextlib
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MUT = os.environ.get("MUTATE", "").strip() == "1"
SFX = "_MUTATE" if MUT else ""
path213 = os.path.join(CFG, "CFG213_dysmalpy_two_sided", "cfg213_two_sided.py")
src213 = open(path213).read()
ns = {"__file__": path213, "__name__": "cfg213"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src213[:src213.index("BINS = {")], "cfg213", "exec"), ns)
cr, vec, EXCL, verdict, KER, A0F, E, nu1, K, G2SI, fnum = (ns[k] for k in ("cr", "vec", "EXCL", "verdict", "KER", "A0F", "E", "nu1", "K", "G2SI", "fnum"))
out = []


def P(s=""):
    print(s, flush=True); out.append(s)


CHK = []


def check(name, val, ok):
    CHK.append(bool(ok))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


P(__doc__.split("Run:")[0].strip())
NB, SEED = 10000, 220
DET = ("02", "03", "07a", "11", "19", "20")
UL = ("08", "12", "23b")
RDEFS = ("table_Rout", "outermost_data_marker")
byid = {g["id"]: g for g in cr}
rng = np.random.default_rng(SEED)
BIDX = {}


def boot(n):
    if n not in BIDX:
        BIDX[n] = np.random.default_rng(SEED * 10 + n).integers(0, n, size=(NB, n))
    return BIDX[n]


def med_ci(d):
    bs = np.median(d[boot(len(d))], axis=1)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return float(np.median(d)), float(lo), float(hi)


def gas_ratio(g):
    f = g["f_molgas"]
    return f / (1 - f)


def vec_rows(rdef):
    """{id: (R kpc, V_bary, V_tot)} for a radius definition, as CFG213's outer block reads them."""
    o = {}
    for v in vec:
        if v["radius_definition"] != rdef:
            continue
        did = {"10a": "10a-E"}.get(v["id"], v["id"])
        vb, vt, Rk = fnum(v["Vbary_kms"]), fnum(v["Vtot_kms"]), fnum(v["R_kpc"])
        if vb > 0 and vt > 0 and Rk > 0:
            o[did] = (Rk, vb, vt)
    return o


def rows_for(rdef, ids, route, tau=0.0, mutate=MUT):
    """route: 'ind' (g_bar scaled by M_ind/M_fit, M_ind = M* + M_gas 10^tau) or 'fit' (as the authors' M_bary)."""
    vr = vec_rows(rdef)
    rows = []
    for i in ids:
        if i not in vr:
            continue
        Rk, vb, vt = vr[i]
        g = byid[i]
        rho = 1.0
        if route == "ind":
            Ms = 10 ** g["logMstar"]
            Mind = Ms + Ms * gas_ratio(g) * 10 ** tau
            rho = Mind / 10 ** g["logMfit"]
        gobs = vt ** 2 / Rk * G2SI
        gbar = rho * vb ** 2 / Rk * G2SI
        D = gobs / gbar * (1.5 if mutate else 1.0)
        rows.append(dict(id=i, z=g["z"], gbar=gbar, D=D, rho=rho, R=Rk))
    return rows


def deltas(rows, law, foot, nu):
    a0 = np.array([A0F[foot] * (E(r["z"]) if law == "rival" else 1.0) for r in rows])
    gb = np.array([r["gbar"] for r in rows]); D = np.array([r["D"] for r in rows])
    return np.log10(D / nu(gb / a0))


def outcome(vf, vr):
    if vf == "CONSISTENT" and vr == "DISFAVOURED-under":
        return "FLAT-SUPPORTED"
    if vr == "CONSISTENT" and vf == "DISFAVOURED-over":
        return "RIVAL-SUPPORTED"
    if vf == "CONSISTENT" and vr == "CONSISTENT":
        return "BOTH-CONSISTENT"
    if vf != "CONSISTENT" and vr != "CONSISTENT":
        return "BOTH-DISFAVOURED"
    return "OTHER"


def cell(rows, kname, foot):
    r = {}
    for law in ("flat", "rival"):
        m, lo, hi = med_ci(deltas(rows, law, foot, KER[kname]))
        r[law] = (m, lo, hi, verdict(lo, hi))
    return r, outcome(r["flat"][3], r["rival"][3])


# ------------------------------------------------------------------------------------------------ controls
P("\nCONTROLS")
committed = {"table_Rout": (0.019, -0.283), "outermost_data_marker": (0.023, -0.258)}
allv = [g["id"] for g in cr if g["id"] not in EXCL]
c1 = 0.0
for rdef, (cf, cr_) in committed.items():
    rows12 = rows_for(rdef, allv, "fit", mutate=False)
    mf = float(np.median(deltas(rows12, "flat", "canonical", K.nu_mono))); mr = float(np.median(deltas(rows12, "rival", "canonical", K.nu_mono)))
    c1 = max(c1, abs(mf - cf), abs(mr - cr_))
    P(f"    {rdef}: n = {len(rows12)}, flat {mf:+.3f}, rival {mr:+.3f} (CFG213: {cf:+.3f}, {cr_:+.3f})")
check("C1 with rho = 1 and CFG213's twelve-disc sample the outer-radius medians equal CFG213's committed values", f"max |difference| {c1:.1e}", c1 < 1e-3 + 1e-9)
# C2: rho = 1 exactly when M_ind = M_fit (synthetic entries through the same arithmetic)
byid["__syn"] = dict(id="__syn", z=5.0, logMstar=10.0, f_molgas=0.5, logMfit=math.log10(2e10))         # M_ind = 1e10 / 0.5 = 2e10 = M_fit
vec.append(dict(id="__syn", radius_definition="__t", R_kpc="3.0", Vbary_kms="150", Vtot_kms="200", gbar_over_a0="", gtot_over_a0="", sigma0_table_kms="", Vrot_Re_table_kms="", VDM_kms=""))
rs = rows_for("__t", ["__syn"], "ind", mutate=False)[0]; rf = rows_for("__t", ["__syn"], "fit", mutate=False)[0]
vec.pop(); del byid["__syn"]
check("C2 rho = 1 when M_ind = M_fit: D_ind equals D_fit (synthetic row through the route arithmetic)", f"rho {rs['rho']:.15f}, |D_ind - D_fit| {abs(rs['D'] - rf['D']):.1e}", abs(rs["rho"] - 1) < 1e-12 and abs(rs["D"] - rf["D"]) < 1e-12)

# ------------------------------------------------------------------------------------------------ main results
P("\nSAMPLE: the six dust DETECTIONS " + ", ".join(DET) + f";  upper-limit discs (one-sided bounds only) {', '.join(UL)}")
P("  route factors rho = M_ind / M_fit (log10): " + ", ".join(f"{i} {math.log10(10 ** byid[i]['logMstar'] * (1 + gas_ratio(byid[i])) / 10 ** byid[i]['logMfit']):+.2f}" for i in DET))
RES = {}
CELLS = [(k, f, r) for r in RDEFS for k in ("nu_mono", "P2") for f in ("canonical", "alt")]
for route in ("ind", "fit"):
    P(f"\n{'INDEPENDENT route (SED M* + dust gas)' if route == 'ind' else 'FIT route (the authors M_bary), the same six discs, for reference'}: median delta [95% CI] -> verdict; outcome class")
    for (kname, foot, rdef) in CELLS:
        rows = rows_for(rdef, DET, route)
        r, cls = cell(rows, kname, foot)
        RES[(route, kname, foot, rdef)] = (r, cls)
        P(f"  {rdef:22s} {kname:7s} {foot:9s} n = {len(rows)}: flat {r['flat'][0]:+.3f} [{r['flat'][1]:+.3f}, {r['flat'][2]:+.3f}] {r['flat'][3]:18s} rival {r['rival'][0]:+.3f} [{r['rival'][1]:+.3f}, {r['rival'][2]:+.3f}] {r['rival'][3]:18s} -> {cls}")
HEAD = ("nu_mono", "canonical", "table_Rout")
hcls = RES[("ind",) + HEAD][1]
allcls = {RES[("ind", k, f, r)][1] for (k, f, r) in CELLS}
robust = len(allcls) == 1
P(f"\nHEADLINE (independent route, {HEAD[2]}, nu_mono, canonical): {hcls}; across the eight cells: {sorted(allcls)} -> {'ROBUST' if robust else 'KERNEL/FOOTING/RADIUS-DEPENDENT'}")
# leave-one-out
loo = {}
for drop in DET:
    ids = [i for i in DET if i != drop]
    r, cls = cell(rows_for(HEAD[2], ids, "ind"), HEAD[0], HEAD[1])
    loo[drop] = (r, cls)
loo_ok = all(v[1] == hcls for v in loo.values())
P("  leave-one-out (headline cell): " + "; ".join(f"drop {d}: flat {v[0]['flat'][0]:+.3f}, rival {v[0]['rival'][0]:+.3f} -> {v[1]}" for d, v in loo.items()))
P(f"  -> {'LOO-ROBUST' if loo_ok else 'NOT LOO-ROBUST'}")
# per-disc table at the headline cell
P("\nPER DISC (independent route, table_Rout, nu_mono, canonical): g_bar/A0, D_ind, D_fit, delta_flat, delta_rival")
rows_i, rows_f = rows_for(HEAD[2], DET, "ind"), rows_for(HEAD[2], DET, "fit")
for ri, rf_ in zip(rows_i, rows_f):
    di = [float(deltas([ri], law, "canonical", K.nu_mono)[0]) for law in ("flat", "rival")]
    P(f"  {ri['id']:5s} z {ri['z']:.3f}  R {ri['R']:.2f} kpc  g_bar/A0 {ri['gbar'] / A0F['canonical']:6.2f} (fit {rf_['gbar'] / A0F['canonical']:6.2f})  D_ind {ri['D']:.3f} (D_fit {rf_['D']:.3f})  delta_flat {di[0]:+.3f}  delta_rival {di[1]:+.3f}")

# ------------------------------------------------------------------------------------------------ calibration flip
P("\nCALIBRATION FLIP: a uniform gas-mass offset tau (dex) on all six detections, M_ind(tau) = M* + M_gas 10^tau; headline cell")


def med_tau(tau, law):
    return float(np.median(deltas(rows_for(HEAD[2], DET, "ind", tau=tau), law, HEAD[1], KER[HEAD[0]])))


tau_star = {}
for law in ("flat", "rival"):
    f_ = lambda t: med_tau(t, law)
    try:
        tau_star[law] = brentq(f_, -2.0, 2.0, xtol=1e-10)
    except ValueError:
        tau_star[law] = None
    P(f"  tau*_{law} (the gas-mass offset at which the median delta_{law} is 0): " + ("none in [-2, +2]" if tau_star[law] is None else f"{tau_star[law]:+.3f} dex"))
    if tau_star[law] is not None:
        c3 = abs(med_tau(tau_star[law], law))
        check(f"C3 at tau*_{law} the median delta is 0", f"{c3:.1e}", c3 < 1e-9)
grid = np.round(np.arange(-1.0, 1.0001, 0.01), 2)
cls_t = {}
for t in grid:
    r_, c_ = cell(rows_for(HEAD[2], DET, "ind", tau=float(t)), HEAD[0], HEAD[1])
    cls_t[float(t)] = c_
c0 = cls_t[0.0]
flips = [t for t in grid if cls_t[float(t)] != c0]
tflip = min((abs(t) for t in flips), default=None)
tflip_signed = [t for t in flips if abs(t) == tflip][0] if flips else None
robust_cal = all(cls_t[float(t)] == c0 for t in grid if abs(t) <= 0.25 + 1e-9)
P(f"  class at tau = 0: {c0}; class changes first at tau = " + ("none in [-1, +1]" if tflip is None else f"{tflip_signed:+.2f} dex (to {cls_t[float(tflip_signed)]}), i.e. {tflip / 0.25:.1f} x the 0.25 dex baseline"))
P(f"  -> {'CALIBRATION-ROBUST' if robust_cal else 'CALIBRATION-LIMITED'} (class unchanged for every |tau| <= 0.25 dex: {robust_cal})")
seq = []
prev = None
for t in grid:
    c_ = cls_t[float(t)]
    if c_ != prev:
        seq.append((float(t), c_)); prev = c_
P("  class along tau (from -1.0 to +1.0): " + "; ".join(f"{t:+.2f}: {c_}" for t, c_ in seq))

# ------------------------------------------------------------------------------------------------ comparison with the forecast
P("\nCOMPARISON WITH THE FORECAST (CFG219, R_out, six discs, tau = 0.25; a description, not a test: a thin-disc model baryon curve there, the fit's here)")
f19 = json.load(open(os.path.join(CFG, "CFG219_z35_preflight", "cfg219_preflight_results.json")))["results"]["S6|nu_mono|canonical|Rout"]
fh, hf = f19["FLAT|H(z)|6|0.25"], f19["H(z)|FLAT|6|0.25"]
rr = RES[("ind",) + HEAD][0]
P(f"  forecast, flat TRUE: (delta_flat, delta_rival) = (0, {fh['mu']:+.3f}) with total scatter {fh['sd_mock']:.3f} on the rival's delta;  rival TRUE: ({hf['mu']:+.3f}, 0) with scatter {hf['sd_mock']:.3f} on the flat delta")
P(f"  realised (independent route): (delta_flat, delta_rival) = ({rr['flat'][0]:+.3f}, {rr['rival'][0]:+.3f})")
P(f"  distance to flat-true: flat {(rr['flat'][0] - 0.0) / hf['sd_mock']:+.2f} and rival {(rr['rival'][0] - fh['mu']) / fh['sd_mock']:+.2f} scatters;  to rival-true: flat {(rr['flat'][0] - hf['mu']) / hf['sd_mock']:+.2f} and rival {(rr['rival'][0] - 0.0) / fh['sd_mock']:+.2f} scatters")

# ------------------------------------------------------------------------------------------------ one-sided bounds
P("\nONE-SIDED BOUNDS (upper-limit discs, table f_molgas used as if a value: a LOWER bound on delta), headline cell; the six-disc medians are above")
mono = []
for i in UL:
    for d_tau in (-0.5, 0.0, 0.5):
        pass
b_rows = rows_for(HEAD[2], UL, "ind")
mf, mrv = RES[("ind",) + HEAD][0]["flat"][0], RES[("ind",) + HEAD][0]["rival"][0]
nab = {"flat": 0, "rival": 0}
for r in b_rows:
    bf = float(deltas([r], "flat", HEAD[1], KER[HEAD[0]])[0]); br = float(deltas([r], "rival", HEAD[1], KER[HEAD[0]])[0])
    nab["flat"] += bf > mf; nab["rival"] += br > mrv
    P(f"  CRISTAL-{r['id']:4s} z {r['z']:.3f}: delta_flat >= {bf:+.3f}, delta_rival >= {br:+.3f}")
P(f"  bounds above the six-disc median: flat {nab['flat']} of {len(b_rows)}, rival {nab['rival']} of {len(b_rows)} (a bound is never entered in a median)")
mono_ok = True
for i in UL:
    v = [float(deltas(rows_for(HEAD[2], [i], "ind", tau=t), "flat", HEAD[1], KER[HEAD[0]])[0]) for t in (-0.5, 0.0, 0.5)]
    mono_ok &= v[0] > v[1] > v[2]
check("C4 for each upper-limit disc delta falls monotonically as the gas mass rises (the bound direction)", f"{mono_ok}", mono_ok)

# ------------------------------------------------------------------------------------------------ MUTATE
if MUT:
    ok = True
    for rdef in RDEFS:
        r0 = rows_for(rdef, DET, "ind", mutate=False); r1 = rows_for(rdef, DET, "ind", mutate=True)
        for law in ("flat", "rival"):
            ok &= abs(float(np.median(deltas(r1, law, "canonical", K.nu_mono)) - np.median(deltas(r0, law, "canonical", K.nu_mono))) - math.log10(1.5)) < 1e-9
    check("MUTATE D x 1.5 raises every median by log10(1.5) to 1e-9", f"{ok}", ok)
P(f"\n{sum(CHK)}/{len(CHK)} controls pass")
js = {"headline": dict(cell=list(HEAD), cls=hcls, robust=robust, loo_robust=loo_ok, calibration_robust=robust_cal, tau_flip=tflip, tau_star=tau_star),
      "cells": {"|".join(k): dict(flat=v[0]["flat"], rival=v[0]["rival"], cls=v[1]) for k, v in RES.items()}}
json.dump(js, open(os.path.join(LANE, "cfg220_outer_independent" + SFX + "_results.json"), "w"), indent=1)
open(os.path.join(LANE, "cfg220_outer_independent" + SFX + ".out"), "w").write("\n".join(out) + "\n")
sys.exit(0 if all(CHK) else 1)
