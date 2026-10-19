"""CFG845 -- does H-PRIM (CFG844), calibrated on the dSphs, over-predict SPARC's small rotating dwarfs?
Criteria: FROZEN_CRITERIA.md (2d2ca7a9a).  Run: python3 cfg845.py (CFG845_MUTATE=1: P = 0).  kappa = 1/2 FITTED; not theory closed."""
import os, glob, json, math, numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG845_MUTATE") == "1"; OUT = []
def P_(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, KPC, a0 = 6.674e-11, 1.989e30, 3.0857e19, 9.3603e-11
nu = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
T = np.load(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_ics_tables_cmb.npz"))
h, wb, wc = float(T["h"]), float(T["omega_b"]), float(T["omega_c"]); Om = (wb + wc) / h ** 2
k = np.array(T["kh"]) * h; Pk = np.array(T["Plin0"]) / h ** 3; lna, lnD = np.array(T["lna"]), np.array(T["lnD"]); D0 = math.exp(np.interp(0.0, lna, lnD))
Dz = lambda z: math.exp(np.interp(-math.log1p(z), lna, lnD)) / D0; rho_m0 = Om * 2.775e11 * h ** 2
def sigma(R):
    x = k * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3; return math.sqrt(np.trapz(k ** 2 * Pk * W ** 2, k) / (2 * math.pi ** 2))
def collapse(Mb):                                                    # CFG844 recipe, unchanged
    Mcat = 6.364 * Mb / 0.10; RL = (3 * Mcat / (4 * math.pi * rho_m0)) ** (1 / 3); s = sigma(RL)
    zc = 0.0 if s <= 1.686 else brentq(lambda z: s * Dz(z) - 1.686, 0.0, 200.0)
    rho_vir = 178.0 * rho_m0 * (1 + zc) ** 3 / 1e9; rho_free = 0.90 * (wc / (wb + wc)) * rho_vir
    return zc, rho_free, (3 * Mcat / (4 * math.pi * rho_vir)) ** (1 / 3)
R44 = json.load(open(os.path.join(LANES, "CFG844_primordial_free_core", "cfg844_results.json")))["rows"]
lx = np.log10([d["r12"] / d["rvir"] for d in R44]); lP = np.log10([d["P"] for d in R44]); gam, a = np.polyfit(lx, lP, 1)
Pfit = lambda x: 10 ** (a + gam * math.log10(x))
P_("CFG845  H-PRIM (CFG844) vs SPARC small rotating dwarfs" + ("  [MUTATE P = 0]" if MUT else ""))
xm = 10 ** np.median(lx); P_(f"  calibration: log P = {a:.3f} + {gam:.3f} log x  (25 dwarfs); P(median x {xm:.3f}) = {Pfit(xm):.1f} vs CFG844 median P {np.median([d['P'] for d in R44]):.1f}")
Q = {}
for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: Q[v[0]] = dict(inc=float(v[5]), q=int(v[17]), Mb=(0.5 * float(v[7]) + 1.33 * float(v[13])) * 1e9)
        except ValueError: pass
gal = []
for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
    nm = os.path.basename(fn).replace("_rotmod.dat", ""); g = Q.get(nm)
    if not g or g["q"] > 2 or g["inc"] < 30 or g["Mb"] > 3e9: continue
    zc, rho_free, rvir = collapse(g["Mb"]); dif, dp, do = [], [], []
    for l in open(fn):
        if l.startswith("#") or not l.strip(): continue
        R, V, eV, Vg, Vd, Vb = [float(t) for t in l.split()[:6]]
        if V <= 0 or R <= 0 or eV / V >= 0.10: continue
        gb = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPC)
        if gb <= 0: continue
        x = R / rvir
        if not (0.01 <= x <= 0.5): continue
        go = V * V * 1e6 / (R * KPC); gl = float(gb * nu(gb / a0))
        Mfree = 0.0 if MUT else Pfit(x) * rho_free * (4 * math.pi / 3) * R ** 3      # Msun (R in kpc, rho in Msun/kpc^3)
        gh = gl + G * Mfree * Msun / (R * KPC) ** 2
        o, p = math.log10(go / gl), math.log10(gh / gl); dif.append(o - p); dp.append(p); do.append(o)
    if dif: gal.append(dict(name=nm, Mb=g["Mb"], zc=zc, rvir=rvir, n=len(dif), d=float(np.median(dif)), pred=float(np.median(dp)), obs=float(np.median(do))))
D = np.array([g["d"] for g in gal]); rng = np.random.default_rng(845)
bs = [rng.choice(D, len(D)).mean() for _ in range(2000)] if len(D) else [0]
mD, sD = (float(D.mean()), float(np.std(bs))) if len(D) else (float("nan"), float("nan"))
cls = "NOT DIAGNOSTIC" if len(gal) < 8 else ("H-PRIM EXCLUDED" if (mD <= -0.15 and mD / sD <= -3) else ("H-PRIM CONSISTENT" if abs(mD) < 0.10 else "TENSION"))
P_(f"\n  SPARC dwarfs (M_b <= 3e9) with points in 0.01 <= R/r_vir <= 0.5: {len(gal)}")
for g in sorted(gal, key=lambda g: g["Mb"]):
    P_(f"    {g['name']:10s} M_b {g['Mb']:8.2e} z_c {g['zc']:4.1f} r_vir {g['rvir']:6.1f} kpc  n {g['n']:2d}  Delta_obs {g['obs']:+.2f}  Delta_pred {g['pred']:+.2f}  obs-pred {g['d']:+.2f}")
P_(f"\n  mean Delta_obs {np.mean([g['obs'] for g in gal]):+.3f}  mean Delta_pred (H-PRIM) {np.mean([g['pred'] for g in gal]):+.3f}")
P_(f"  D = mean(obs - pred) = {mD:+.3f} +- {sD:.3f} dex  (z {mD / sD:+.1f})\n\n  CLASS: {cls}")
RES = dict(lane="CFG845", mutate=MUT, calib=dict(a=float(a), gamma=float(gam)), galaxies=gal, D=mD, sD=sD, cls=cls)
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg845_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg845{sfx}.out"), "w").write("\n".join(OUT) + "\n")
