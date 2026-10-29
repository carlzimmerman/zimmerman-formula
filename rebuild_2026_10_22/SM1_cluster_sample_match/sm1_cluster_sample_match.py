#!/usr/bin/env python3
"""SM1_cluster_sample_match: data-only comparison of X-COP and the eRASS1 x KiDS lensing clusters (mass overlap, same-cluster
definitions, apertures in R500 units). Frozen criteria 6a0406f8a7 (committed alone). No model enters.

kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 python3 -I sm1_cluster_sample_match.py      (SM1_MUTATE=1 twin)
"""
import os, sys, json, math, hashlib
import numpy as np
from astropy.io import fits

MUT = os.environ.get("SM1_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
DATA = os.path.join(REPO, "real_research", "data")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
P(f"SM1_cluster_sample_match (criteria 6a0406f8a7){'  [MUTATE: match radius 0]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")
XT = json.load(open(os.path.join(DATA, "xcop", "xcop_r500_ettori2019.json")))
L = np.load(os.path.join(REB, "X7_cluster_core_significance", "x7_measure_percluster.npz"))
E = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"))[1].data
EN = {str(n).strip(): k for k, n in enumerate(E["NAME"])}
checks = {}
NL = len(L["name"]); M500L = np.asarray(L["M500"], float) * 1e13
def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m)))
XC = {}
for n, v in XT.items():
    p_ = os.path.join(DATA, "xcop", n)
    if not os.path.isdir(p_): continue
    with fits.open(os.path.join(p_, f"{n}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = float(h[1].header["R500"]); hd = h[1].header.copy()   # RA/DEC from the gas file (every cluster has one)
    mg = li(gas["RADIUS"] * rg500, gas["MGAS"], v["R500"] * 1e3) if "MGAS" in gas.columns.names else float("nan")
    XC[n] = dict(z=v["z"], R500=v["R500"], M500=v["M500"] * 1e14, Mgas500=mg, ra=float(hd["RA"]), dec=float(hd["DEC"]))
checks["K0"] = NL == 326 and all(np.isfinite(c["Mgas500"]) for c in XC.values())
P(f"  K0: lensing N {NL}; X-COP {len(XC)} clusters, Mgas500(R500) finite: {'PASS' if checks['K0'] else 'FAIL'}")

# (a) mass overlap
xm = np.array([c["M500"] for c in XC.values()]); pct = float(np.mean(M500L <= np.median(xm)) * 100)
frac = float(np.mean(M500L >= xm.min()))
p90 = float(np.percentile(M500L, 90))
P(f"\n(a) M500: lensing 5/50/90/95% = {np.percentile(M500L, 5):.2e} / {np.median(M500L):.2e} / {p90:.2e} / {np.percentile(M500L, 95):.2e}; "
  f"X-COP {xm.min():.2e}-{xm.max():.2e}, median {np.median(xm):.2e} = lensing percentile {pct:.1f}; lensing fraction >= X-COP min {frac:.3f}")

# (b) same clusters
rmax = 0.0 if MUT else 3.0 / 60
ER, ED, EZ = np.asarray(E["RA"], float), np.asarray(E["DEC"], float), np.asarray(E["BEST_Z"], float)
rows = []; used = set(); k1 = True
for n, c in XC.items():
    s = np.degrees(np.arccos(np.clip(np.sin(np.radians(c["dec"])) * np.sin(np.radians(ED)) + np.cos(np.radians(c["dec"])) * np.cos(np.radians(ED)) * np.cos(np.radians(ER - c["ra"])), -1, 1)))
    ok = (s <= rmax) & (np.abs(EZ - c["z"]) < 0.01)
    if not ok.any(): continue
    j = int(np.where(ok)[0][np.argmin(s[ok])]); k1 &= j not in used; used.add(j)
    r = dict(xcop=n, erass=str(E["NAME"][j]).strip(), sep_arcmin=float(s[j] * 60),
             dlogR500=math.log10(float(E["R500"][j]) / 1e3 / c["R500"]), dlogM500=math.log10(float(E["M500"][j]) * 1e13 / c["M500"]),
             dlogMgas500=math.log10(float(E["MGAS500"][j]) * 1e11 / c["Mgas500"]), in_lensing=str(E["NAME"][j]).strip() in set(str(x) for x in L["name"]))
    rows.append(r)
    P(f"   {n:7s} <-> {r['erass']} ({r['sep_arcmin']:.1f}'): dlog R500 {r['dlogR500']:+.3f}, M500 {r['dlogM500']:+.3f}, Mgas500 {r['dlogMgas500']:+.3f}{'  [in lensing sample]' if r['in_lensing'] else ''}")
checks["K1"] = bool(k1); checks["K2"] = len(rows) >= 1
medR = float(np.median(np.abs([r["dlogR500"] for r in rows]))) if rows else float("nan")
medG = float(np.median(np.abs([r["dlogMgas500"] for r in rows]))) if rows else float("nan")
P(f"(b) matched {len(rows)}: median |dlog R500| {medR:.3f}, median signed {np.median([r['dlogR500'] for r in rows]) if rows else float('nan'):+.3f}; "
  f"median |dlog Mgas500| {medG:.3f}, signed {np.median([r['dlogMgas500'] for r in rows]) if rows else float('nan'):+.3f}; "
  f"median dlog M500 {np.median([r['dlogM500'] for r in rows]) if rows else float('nan'):+.3f}")

# (c) apertures in R500 units
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:] * EDGES[:-1])
R5L = np.array([float(E["R500"][EN[str(n).strip()]]) / 1e3 for n in L["name"]])
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
ap = {b: [float(np.median(RC[i[0]] / R5L)), float(np.median(RC[i[-1]] / R5L))] for b, i in BANDS.items()}
P(f"(c) lensing bands in R500 units (median over clusters, bin-centre range): " + "; ".join(f"{b} {v[0]:.2f}-{v[1]:.2f}" for b, v in ap.items())
  + f"; lensing R500 median {np.median(R5L):.3f} Mpc vs X-COP {np.median([c['R500'] for c in XC.values()]):.3f}; X-COP graded x = 0.1-0.7 R500")
outer_med = float(np.median(RC[6] / R5L))
defm = len(rows) >= 3 and (medR > 0.04 or medG > 0.1)
samp = (np.median(xm) > p90) or (outer_med > 1.0)
v = " + ".join(([f"DEFINITION MISMATCH (|dlog R500| {medR:.3f}, |dlog Mgas500| {medG:.3f})"] if defm else []) +
               ([f"SAMPLE MISMATCH (X-COP median at lensing percentile {pct:.0f}; OUTER band starts at {outer_med:.2f} R500)"] if samp else [])) or "COMPARABLE"
P(f"\n=== VERDICT: {v}")
RES = dict(criteria="6a0406f8a7", mutate=MUT, mass=dict(lens_pct=[float(np.percentile(M500L, q)) for q in (5, 50, 90, 95)], xcop=[float(x) for x in xm],
           xcop_median_pct=pct, frac_lens_ge_xcopmin=frac), matched=rows, apertures=ap, outer_start_R500=outer_med, verdict=v, checks=checks)
fn = os.path.join(HERE, f"sm1_cluster_sample_match_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(checks.values())}/{len(checks)}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"sm1_cluster_sample_match{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(checks.values()) else 1)
