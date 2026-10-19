"""CFG822 -- canonical v2 H-EX applied to 11 MW classical dSphs.  Criteria: FROZEN_CRITERIA.md (020ebf66d).
Machinery: CFG809 defs exec'd read-only.  Run: python3 cfg822.py   (CFG822_MUTATE=1: free mass uniform to r_ta).
kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
from scipy.stats import chi2 as C2
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG822_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
os.environ["CFG809_MODE"] = "defs"
src = os.path.join(LANES, "CFG809_expelled_gas_split", "cfg809.py")
txt = open(src).read().split("# ============================================================================================ eRASS1 (CFG687)")[0]
G = {"__file__": src, "__name__": "d"}; exec(compile(txt, src, "exec"), G)
Gsi, Msun, PCm, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19
def fnum(x):
    try: return float(x)
    except: return None
D = []
for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv"))):
    MV, s_, es, rh = fnum(r.get("M_V")), fnum(r.get("vlos_sigma")), fnum(r.get("vlos_sigma_em")), fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
    if MV is None or s_ is None or rh is None or MV > -7.7 or r["name"] in ("LMC", "SMC", "Sagittarius"): continue
    D.append(dict(name=r["name"], Mb=2.0 * 10 ** (0.4 * (4.83 - MV)), so=s_, eso=es or 0.1 * s_, rh=rh / 1000.0))
rob = np.geomspace(1e-3, 6e3, 900)
def run(g, foot, nofree=False):
    a = g["rh"]; Ms = g["Mb"] * rob ** 3 / (rob ** 2 + a ** 2) ** 1.5
    rg, Mcore, Mset, Mres, meta = G["run_system"](rob, Ms, np.zeros_like(rob), 0.0, foot, "s", "EX")
    r12 = (4 / 3) * a
    Mfree_tot = float(Mres[-1]); rta = meta["rta"]
    if MUT:
        fr = min(1.0, (r12 / rta) ** 3) * Mfree_tot
    else:
        fr = float(np.interp(r12, rg, Mres))
    if nofree: fr = 0.0
    Mtot = float(np.interp(r12, rg, Mcore)) + float(np.interp(r12, rg, Mset)) + fr
    sig = math.sqrt(Gsi * Mtot * Msun / (3 * r12 * KPC)) / 1e3
    return sig, fr / g["Mb"], meta
vU = (math.log(10) * 0.15 / 2) ** 2
P(f"CFG822  canonical v2 H-EX on {len(D)} MW classical dSphs" + ("  [MUTATE uniform free]" if MUT else ""))
RES = dict(lane="CFG822", mutate=MUT, rows={})
for foot in ("canonical", "alt"):
    c2 = 0.0
    for g in D:
        s, ff, meta = run(g, foot)
        c2 += (math.log(g["so"]) - math.log(s)) ** 2 / ((g["eso"] / g["so"]) ** 2 + vU)
        RES["rows"][f"{foot}|{g['name']}"] = dict(sig=s, free_in_r12_over_Mb=ff, fret=meta["fret"], free_frac=meta["res_frac"], rta_kpc=meta["rta"])
        if foot == "canonical":
            P(f"  {g['name']:16s} obs {g['so']:5.2f}  pred {s:5.2f}  free(<r1/2)/M_b {ff:6.2f}  f_ret {meta['fret']:.2f}  free/supply {meta['res_frac']:.2f}  r_ta {meta['rta']:.0f} kpc")
    p = float(C2.sf(c2, len(D) - 1))
    RES[foot] = dict(chi2=c2, p=p)
    P(f"  [{foot}] chi2 {c2:.1f} / {len(D) - 1} dof, p {p:.2e}  (unscreened law CFG821: 58.4 can / 51.8 alt)")
g0 = D[4] if len(D) > 4 else D[0]
s0, _, _ = run(g0, "canonical", nofree=True)
y = Gsi * (g0["Mb"] / 2) * Msun / ((4 / 3) * g0["rh"] * KPC) ** 2 / 9.3603e-11; sL = math.sqrt(Gsi * (g0["Mb"] / 2) * Msun / (3 * (4 / 3) * g0["rh"] * KPC) / (1.0 / (-math.expm1(-math.sqrt(y))) ** -1)) / 1e3
P(f"  K1 {g0['name']}: free=0 sigma {s0:.2f} vs isolated-law (Wolf, M/2) {sL:.2f} -> {'PASS' if abs(s0 / sL - 1) < 0.02 else 'FAIL (estimator convention, see README)'}")
pr = RES["canonical"]
cls = "H-EX EXPLAINS dSphs" if (pr["p"] >= 0.01 and pr["chi2"] < 58.4) else ("IMPROVES" if pr["chi2"] < 58.4 else "NO HELP")
P(f"\n  CLASS (canonical): {cls}")
RES["cls"] = cls
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg822_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg822{sfx}.out"), "w").write("\n".join(OUT) + "\n")
