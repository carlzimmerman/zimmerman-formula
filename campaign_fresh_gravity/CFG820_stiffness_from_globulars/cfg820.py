"""CFG820 -- lower bound on the stiffness length L* from the outer-halo globulars.  Criteria: FROZEN_CRITERIA.md (4058a83d7).
Data: CFG332's cluster table (cfg332_globulars_results.json); estimators copied verbatim from cfg332_globulars.py; screening S(s)
from CFG691's table.  Run: python3 cfg820.py   (CFG820_MUTATE=1: S := 1).  Seconds.  kappa = 1/2 FITTED; not theory closed."""
import os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG820_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, kpc, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16
UPS_V, MW_MB, WID = 1.6, 6.0e10, 0.15                         # CFG332 constants
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
GC = json.load(open(os.path.join(LANES, "CFG332_globulars_three_routes", "cfg332_globulars_results.json")))["clusters"]
def wolf_sigma(M, rhl, boost=1.0): return np.sqrt(G * boost * M * Msun / (6.0 * (4.0 / 3.0) * rhl * PC)) / 1e3
def g_ext(RGC): return G * MW_MB * Msun / (RGC * kpc) ** 2
def y_int(g, a0): return G * (UPS_V * g["LV"] * Msun / 2) / ((4.0 / 3.0) * g["rhl"] * PC) ** 2 / a0
def nu_arr(y): y = max(float(y), 1e-12); return 1.0 / (-math.expm1(-math.sqrt(y)))
ST_s = np.array([0.01, 0.1, 0.3, 1, 3, 10, 100, 1000]); ST_S = np.array([0.0050, 0.048, 0.134, 0.358, 0.663, 0.894, 0.990, 0.998999])
def Sfun(s):
    if MUT: return 1.0
    if s <= 0.01: return s / 2
    if s >= 1000: return 1 - 1 / s
    return float(np.interp(math.log(s), np.log(ST_s), ST_S))
def pred(g, a0, Lstar):
    M = UPS_V * g["LV"]; sN = wolf_sigma(M, g["rhl"]); Blaw = nu_arr(y_int(g, a0) + g_ext(g["RGC"]) / a0)
    if Lstar is None: return sN, 0.0
    rM = math.sqrt(G * M * Msun / a0) / PC; lg = Lstar ** 2 / (2 * rM); s = (4.0 / 3.0) * g["rhl"] / lg
    Sv = Sfun(s); return sN * math.sqrt(1 + Sv * (Blaw - 1)), Sv
vU = (math.log(10) * WID / 2) ** 2
def chi2(gcs, a0, L):
    return sum((math.log(g["so"]) - math.log(pred(g, a0, L)[0])) ** 2 / ((g["eso"] / g["so"]) ** 2 + vU) for g in gcs)
P("CFG820  L* lower bound from outer-halo globulars" + ("  [MUTATE S=1]" if MUT else ""))
for g in GC:
    a0 = A0["canonical"]; M = UPS_V * g["LV"]; sN = wolf_sigma(M, g["rhl"]); B = nu_arr(y_int(g, a0) + g_ext(g["RGC"]) / a0)
    P(f"  {g['name']:9s}: sigma_obs {g['so']:.2f}+-{g['eso']:.2f}; Newton {sN:.2f}; law+EFE {sN * math.sqrt(B):.2f} (B {B:.2f}); r_h {g['rhl']:.1f} pc, M {M:.2e}")
# K1/K2 identities
g0 = GC[0]; a0 = A0["canonical"]
k1 = abs(pred(g0, a0, 1e9)[0] / wolf_sigma(UPS_V * g0["LV"], g0["rhl"]) - 1) < 1e-6 or MUT
Bl = nu_arr(y_int(g0, a0) + g_ext(g0["RGC"]) / a0)
k2 = abs(pred(g0, a0, 1e-6)[0] / (wolf_sigma(UPS_V * g0["LV"], g0["rhl"]) * math.sqrt(Bl)) - 1) < 1e-3
P(f"  K1 (L* -> inf gives Newton): {'PASS' if k1 else 'FAIL'};  K2 (L* -> 0 gives law+EFE): {'PASS' if k2 else 'FAIL'};  (CFG332 combined-p T not recomputed: different statistic, disclosed)")
grid = np.geomspace(5.75, 3000, 400)
RES = dict(lane="CFG820", mutate=MUT, K1=bool(k1), K2=bool(k2))
for lab, gcs in (("primary (no Pal 3)", [g for g in GC if g["name"] != "Pal 3"]), ("all four", GC)):
    for foot, a0 in A0.items():
        c = np.array([chi2(gcs, a0, L) for L in grid]); cN = chi2(gcs, a0, None); cmin = min(c.min(), cN)
        ok = grid[c - cmin <= 3.84]; L95 = float(ok.min()) if len(ok) else float("nan")
        RES[f"{lab}|{foot}"] = dict(chi2_newton=cN, chi2_at_Lmin=float(c[0]), chi2_min=float(cmin), L95=L95)
        P(f"  [{lab:18s} {foot:9s}] chi2: Newton {cN:.2f}, at L*=5.75 pc {c[0]:.2f}, min {cmin:.2f} -> L*_95 >= {L95:.1f} pc")
pr = RES["primary (no Pal 3)|canonical"]; L95 = pr["L95"]
# consequence for UFDs
P("\n  consequence: screening S for UFD-like systems at L*_95 (canonical)")
for Mb in (1e3, 1e4):
    for rh in (20, 40):
        rM = math.sqrt(G * Mb * Msun / A0["canonical"]) / PC; lg = L95 ** 2 / (2 * rM); s = (4 / 3) * rh / lg
        P(f"    M_b {Mb:.0e}, r_h {rh} pc: l_gamma {lg:.0f} pc, s {s:.3f}, S {Sfun(s):.3f}")
cls = "BOUND TIGHTENED" if L95 > 5.75 * 1.01 else "NO TIGHTENING"
P(f"\n  CLASS (primary, canonical): {cls}; L*_95 = {L95:.1f} pc")
RES.update(cls=cls)
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg820_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg820{sfx}.out"), "w").write("\n".join(OUT) + "\n")
