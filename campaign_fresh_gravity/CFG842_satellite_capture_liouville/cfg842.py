"""CFG842 -- Liouville ceiling on satellites capturing host cold energy.  Criteria: FROZEN_CRITERIA.md (127c29c26).
Run: python3 cfg842.py (CFG842_MUTATE=1: no phase-space dilution).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
from scipy.integrate import quad
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG842_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC, KPC, a0 = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19, 9.3603e-11
nu = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15)))); law = lambda gN: gN * nu(gN / a0)
def fnum(x):
    try: return float(x)
    except: return None
LVD = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv")))}
R28 = {r["name"]: r for r in json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))["canonical|nu_e"]["rows"]}
R39 = json.load(open(os.path.join(LANES, "CFG839_pericentre_tides", "cfg839_results.json")))["rows"]
U27 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
R24 = json.load(open(os.path.join(LANES, "CFG824_dwarf_age_fossil", "cfg824_results.json")))["rows"]
def host(Mb):
    rM = math.sqrt(G * Mb * Msun / a0)
    Mc = lambda r: 0.5 * Mb * (math.sqrt(1 + 4 * r * r / rM ** 2) - 1)                       # Msun, r in m
    rho = lambda r: (0.5 * Mb * (4 * r / rM ** 2) / math.sqrt(1 + 4 * r * r / rM ** 2)) / (4 * math.pi * r * r)   # Msun / m^3
    sig = lambda r: math.sqrt(r * law(G * Mb * Msun / r ** 2) / 2)                             # m/s
    return Mc, rho, sig
P("CFG842  Liouville ceiling on host cold-energy capture by MW satellites" + ("  [MUTATE no dilution]" if MUT else ""))
RES = dict(lane="CFG842", mutate=MUT, rows={}); worst = 0.0
for Mb in (6.0e10, 8.0e10):
    Mc, rho, sig = host(Mb)
    if Mb == 6.0e10 and not MUT:
        r100 = 100 * KPC; k1 = quad(lambda r: 4 * math.pi * r * r * rho(r), 0, r100, limit=200)[0] / Mc(r100)
        P(f"  K1 int rho dV / M_c at 100 kpc = {k1:.6f} -> {'PASS' if abs(k1 - 1) < 1e-3 else 'FAIL'}")
    P(f"\n  [M_MW {Mb:.0e}]  {'satellite':18s} {'rho_need':>10s} {'rho_c(D)':>10s} {'rho_c(peri)':>11s} {'sig_s/sig_h':>11s} {'ceiling/need':>12s}  (Msun/kpc^3)")
    for nm, o in R39.items():
        L = LVD[nm]; rh = (4 / 3) * (fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical"))) * PC
        Ms = U27[nm]["ups"] * 10 ** (0.4 * (4.83 - fnum(L["M_V"]))); gl = law(G * (Ms / 2) * Msun / rh ** 2)
        Mextra = max(gl * (10 ** R28[nm]["delta"] - 1), 0) * rh * rh / G / Msun
        rho_need = 3 * Mextra / (4 * math.pi * rh ** 3)
        ss = R24[nm]["so"] * 1e3; best = 0.0; cells = []
        for D in (o["rnow"] * KPC, o["rp"] * KPC):
            sh = ss if MUT else sig(D); ceil_ = rho(D) * (ss / sh) ** 3; best = max(best, ceil_ / rho_need if rho_need > 0 else float("inf")); cells.append((rho(D), sh))
        worst = max(worst, best) if rho_need > 0 else worst
        k3 = (KPC ** 3)
        RES["rows"].setdefault(nm, {})[f"{Mb:.0e}"] = dict(rho_need=rho_need * k3, rho_now=cells[0][0] * k3, rho_peri=cells[1][0] * k3, sig_ratio=ss / cells[1][1], ratio=best)
        P(f"           {nm:18s} {rho_need * k3:10.2e} {cells[0][0] * k3:10.2e} {cells[1][0] * k3:11.2e} {ss / cells[1][1]:11.3f} {best:12.2e}")
cls = "CAPTURE EXCLUDED" if worst < 0.1 else ("CAPTURE POSSIBLE" if worst >= 1 else "MARGINAL")
RES["max_ratio"] = worst; RES["cls"] = cls; P(f"\n  largest ceiling/need over satellites, distances, MW masses: {worst:.2e}\n  CLASS: {cls}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg842_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg842{sfx}.out"), "w").write("\n".join(OUT) + "\n")
