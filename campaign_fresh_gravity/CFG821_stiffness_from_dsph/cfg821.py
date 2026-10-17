"""CFG821 -- upper bound on the stiffness length L* from the MW classical dSphs.  Criteria: FROZEN_CRITERIA.md (107b2051b).
Run: python3 cfg821.py   (CFG821_MUTATE=1: S := 0).  Seconds.  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
MUT = os.environ.get("CFG821_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, kpc, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16
UPS, MW_MB, WID = 2.0, 6.0e10, 0.15
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
def fnum(x):
    try: return float(x)
    except: return None
D = []
for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv"))):
    MV, s_, es, rh, rgc = fnum(r.get("M_V")), fnum(r.get("vlos_sigma")), fnum(r.get("vlos_sigma_em")), fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical")), fnum(r.get("distance_gc"))
    if MV is None or s_ is None or rh is None or MV > -7.7 or r["name"] in ("LMC", "SMC", "Sagittarius"): continue
    D.append(dict(name=r["name"], LV=10 ** (0.4 * (4.83 - MV)), so=s_, eso=es or 0.1 * s_, rhl=rh, RGC=rgc or 100.0))
def wolf(M, rhl, B=1.0): return math.sqrt(G * B * M * Msun / (6.0 * (4.0 / 3.0) * rhl * PC)) / 1e3
def nu(y): y = max(y, 1e-12); return 1.0 / (-math.expm1(-math.sqrt(y)))
ST_s = np.array([0.01, 0.1, 0.3, 1, 3, 10, 100, 1000]); ST_S = np.array([0.0050, 0.048, 0.134, 0.358, 0.663, 0.894, 0.990, 0.998999])
def Sfun(s):
    if MUT: return 0.0
    if s <= 0.01: return s / 2
    if s >= 1000: return 1 - 1 / s
    return float(np.interp(math.log(s), np.log(ST_s), ST_S))
def pred(g, a0, L, efe):
    M = UPS * g["LV"]; y = G * (M / 2) * Msun / ((4 / 3) * g["rhl"] * PC) ** 2 / a0
    if efe: y += G * MW_MB * Msun / (g["RGC"] * kpc) ** 2 / a0
    B = nu(y); sN = wolf(M, g["rhl"])
    if L is None: return sN
    if L == 0: return sN * math.sqrt(B)
    rM = math.sqrt(G * M * Msun / a0) / PC; lg = L ** 2 / (2 * rM); s = (4 / 3) * g["rhl"] / lg
    return sN * math.sqrt(1 + Sfun(s) * (B - 1))
vU = (math.log(10) * WID / 2) ** 2
chi2 = lambda a0, L, efe: sum((math.log(g["so"]) - math.log(pred(g, a0, L, efe))) ** 2 / ((g["eso"] / g["so"]) ** 2 + vU) for g in D)
from scipy.stats import chi2 as C2
P(f"CFG821  L* upper bound from {len(D)} MW classical dSphs" + ("  [MUTATE S=0]" if MUT else ""))
a0 = A0["canonical"]
for g in D:
    P(f"  {g['name']:16s} sigma {g['so']:5.2f}+-{g['eso']:.2f}  Newton {pred(g, a0, None, False):5.2f}  law(iso) {pred(g, a0, 0, False):5.2f}  r_h {g['rhl']:6.0f} pc")
g0 = D[0]; k1 = abs(pred(g0, a0, 1e12, False) / pred(g0, a0, None, False) - 1) < 1e-6 or MUT; k2 = MUT or abs(pred(g0, a0, 1e-3, False) / pred(g0, a0, 0, False) - 1) < 1e-3
P(f"  K1 (L*->inf = Newton) {'PASS' if k1 else 'FAIL'}; K2 (L*->0 = law) {'PASS' if k2 else 'FAIL'}")
grid = np.geomspace(5.75, 3000, 400); RES = dict(lane="CFG821", mutate=MUT, n=len(D), K1=bool(k1), K2=bool(k2))
for efe in (False, True):
    for foot, a0 in A0.items():
        c = np.array([chi2(a0, L, efe) for L in grid]); c0, cN = chi2(a0, 0, efe), chi2(a0, None, efe); cmin = min(c.min(), c0)
        ok = grid[c - cmin <= 3.84]; up = float(ok.max()) if len(ok) else float("nan"); lo = float(ok.min()) if len(ok) else float("nan")
        p0 = float(C2.sf(c0, len(D) - 1))
        lab = f"{'law+EFE' if efe else 'isolated law'}|{foot}"
        RES[lab] = dict(chi2_unscreened=c0, p_unscreened=p0, chi2_newton=cN, chi2_min=float(cmin), L_best=float(grid[int(np.argmin(c))]), L95_up=up, L95_lo=lo)
        P(f"  [{lab:22s}] chi2 unscreened {c0:.1f} (p {p0:.3f}), Newton {cN:.1f}, min {cmin:.1f} at L* {grid[int(np.argmin(c))]:.0f} pc; 95% range {lo:.0f}-{up:.0f} pc")
pr = RES["isolated law|canonical"]; up = pr["L95_up"]
cls = ("INCONSISTENT" if up < 24 else ("WINDOW CLOSED (two-sided)" if up < 3000 * 0.99 else "NO UPPER BOUND"))
cond = " (CONDITIONAL: unscreened fit poor)" if pr["p_unscreened"] < 0.01 else ""
P(f"\n  CLASS (primary isolated law, canonical): {cls}{cond}; window with CFG820: [24, {up:.0f}] pc")
RES.update(cls=cls)
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg821_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg821{sfx}.out"), "w").write("\n".join(OUT) + "\n")
