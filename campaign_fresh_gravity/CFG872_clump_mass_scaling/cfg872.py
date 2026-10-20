"""CFG872 -- scaling of the self-consistent cold clump mass with stellar mass.  Criteria: FROZEN_CRITERIA.md (4851408cd).
Run: python3 cfg872.py (CFG872_MUTATE=1: sigma_obs = 1.5 sigma_law).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG872_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
nu = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15))))
def fnum(x):
    try: return float(x)
    except: return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
R27 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
R24 = json.load(open(os.path.join(LANES, "CFG824_dwarf_age_fossil", "cfg824_results.json")))["rows"]
R28 = json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))
P("CFG872  scaling of the self-consistent cold clump mass" + ("  [MUTATE sigma_obs = 1.5 sigma_law]" if MUT else ""))
RES = dict(lane="CFG872", mutate=MUT)
for foot in ("canonical", "alt"):
    a0 = A0[foot]; rows, skip = [], []
    for r in R28[f"{foot}|nu_e"]["rows"]:
        if r["delta"] <= 0.05: continue
        nm = r["name"]; L = LVD[nm]; rh = (4 / 3) * (fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical"))) * PC
        Ms = R27[nm]["ups"] * 10 ** (0.4 * (4.83 - fnum(L["M_V"]))); gN = G * (Ms / 2) * Msun / rh ** 2
        sl = math.sqrt(gN * nu(gN / a0) * rh / 3); so = (1.5 * sl) if MUT else R24[nm]["so"] * 1e3
        if so <= sl: skip.append(nm); continue
        def h(sx):
            rc = 4.5 * sx * sx / a0; f = rh * rh / (rh * rh + rc * rc); return sl * sl + f * 2 * sx * sx / 3 - so * so
        lo, hi = 1.0, 3e5
        if h(lo) * h(hi) > 0:
            # f -> 0 at large sx (core swallows r1/2): the excess term has a maximum; no root if it cannot reach
            sxs = np.geomspace(lo, hi, 4000); hv = np.array([h(s) for s in sxs]); idx = np.where(np.diff(np.sign(hv)))[0]
            if not len(idx): skip.append(nm); continue
            lo, hi = sxs[idx[0]], sxs[idx[0] + 1]
        sx = brentq(h, lo, hi)                       # smallest root (compact-core branch excluded by choosing the first sign change)
        Mcl = 81 * sx ** 4 / (4 * G * a0) / Msun; rc = 4.5 * sx * sx / a0 / PC
        rows.append(dict(name=nm, lMs=math.log10(Ms), lM=math.log10(Mcl), sx=sx / 1e3, rc=rc))
    lMs = np.array([x["lMs"] for x in rows]); lM = np.array([x["lM"] for x in rows])
    A = np.c_[np.ones(len(lMs)), lMs]; cf = np.linalg.lstsq(A, lM, rcond=None)[0]; s = float(cf[1])
    rng = np.random.default_rng(872); bs = []
    for _ in range(2000):
        i = rng.integers(0, len(lMs), len(lMs)); bs.append(np.linalg.lstsq(A[i], lM[i], rcond=None)[0][1])
    ss = float(np.std(bs)); rms = float(np.std(lM - A @ cf, ddof=2))
    c0, c1 = abs(s) / ss, abs(s - 1) / ss
    cls = ("FLOOR-LIKE" if (c0 < 2 and c1 >= 3) else ("SUPPLY-LIKE" if (c1 < 2 and c0 >= 3) else ("INTERMEDIATE" if (c0 >= 2 and c1 >= 2) else "UNDECIDED")))
    RES[foot] = dict(N=len(rows), skipped=skip, slope=s, slope_err=ss, rms=rms, median_Mcl=float(10 ** np.median(lM)), median_sigma=float(np.median([x["sx"] for x in rows])),
                     median_rc=float(np.median([x["rc"] for x in rows])), rows=rows, cls=cls)
    P(f"\n  [{foot}] N {len(rows)} (skipped: {skip}); median sigma_x {RES[foot]['median_sigma']:.2f} km/s, r_c {RES[foot]['median_rc']:.0f} pc, M_cl {RES[foot]['median_Mcl']:.2e} Msun")
    P(f"     log M_cl = {cf[0]:.2f} + {s:+.3f} (+-{ss:.3f}) log M*   [from 0: {c0:.1f} sigma, from 1: {c1:.1f} sigma]; residual rms {rms:.2f} dex  -> {cls}")
    if foot == "canonical" and not MUT:
        for x in sorted(rows, key=lambda x: x["lMs"]): P(f"       {x['name']:18s} log M* {x['lMs']:.2f}  sigma_x {x['sx']:5.2f}  r_c {x['rc']:6.0f} pc  log M_cl {x['lM']:.2f}")
if not MUT: P(f"\n  K1 median sigma_x {RES['canonical']['median_sigma']:.2f} km/s vs pooled 7.9 (within 20%: {abs(RES['canonical']['median_sigma'] / 7.9 - 1) < 0.2})")
RES["cls"] = RES["canonical"]["cls"]; P(f"\n  CLASS (canonical): {RES['cls']}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg872_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg872{sfx}.out"), "w").write("\n".join(OUT) + "\n")
