"""CFG844 -- H-PRIM: early-collapse free cold energy as the faint-dwarf excess.  Criteria: FROZEN_CRITERIA.md (970c67ce3).
Native cosmology from CFG654 cmb tables.  Run: python3 cfg844.py (CFG844_MUTATE=1: z_c = 0).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
from scipy.stats import spearmanr
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG844_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC, KPC, a0 = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19, 9.3603e-11
nu = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15)))); law = lambda gN: gN * nu(gN / a0)
def fnum(x):
    try: return float(x)
    except: return None
T = np.load(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_ics_tables_cmb.npz"))
h, wb, wc = float(T["h"]), float(T["omega_b"]), float(T["omega_c"]); Om = (wb + wc) / h ** 2
k = np.array(T["kh"]) * h; Pk = np.array(T["Plin0"]) / h ** 3                       # 1/Mpc, Mpc^3
lna, lnD = np.array(T["lna"]), np.array(T["lnD"]); D0 = math.exp(np.interp(0.0, lna, lnD))
Dz = lambda z: math.exp(np.interp(-math.log1p(z), lna, lnD)) / D0
rho_m0 = Om * 2.775e11 * h ** 2                                                       # Msun / Mpc^3
def sigma(R):
    x = k * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3; return math.sqrt(np.trapz(k ** 2 * Pk * W ** 2, k) / (2 * math.pi ** 2))
FRET, FFREE, DC, DELTA = 0.10, 0.90, 1.686, 178.0
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
R28 = json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))["canonical|nu_e"]["rows"]
U27 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
P("CFG844  H-PRIM: collapse-epoch free cold energy vs the faint-dwarf excess" + ("  [MUTATE z_c = 0]" if MUT else ""))
P(f"  native: h {h:.4f}  Om {Om:.4f}  sigma8 {sigma(8 / h):.4f}  D(0) {Dz(0):.6f}")
rows, noex = [], []
for r in R28:
    L = LVD[r["name"]]; host = L.get("host", "") or "field"
    rh = (4 / 3) * (fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical"))) * PC
    Mb = U27[r["name"]]["ups"] * 10 ** (0.4 * (4.83 - fnum(L["M_V"]))); gl = law(G * (Mb / 2) * Msun / rh ** 2)
    Mex = gl * (10 ** r["delta"] - 1) * rh * rh / G / Msun; rho_need = 3 * Mex / (4 * math.pi * (rh / KPC) ** 3)     # Msun/kpc^3
    Mcat = 6.364 * Mb / FRET; RL = (3 * Mcat / (4 * math.pi * rho_m0)) ** (1 / 3); s = sigma(RL)
    zc = 0.0 if (MUT or s <= DC) else brentq(lambda z: s * Dz(z) - DC, 0.0, 200.0)
    rho_vir = DELTA * rho_m0 * (1 + zc) ** 3 / 1e9                                    # Msun/kpc^3 (total)
    rho_free = FFREE * (wc / (wb + wc)) * rho_vir
    rvir = (3 * Mcat / (4 * math.pi * rho_vir)) ** (1 / 3)                            # kpc
    d = dict(name=r["name"], host=host, delta=r["delta"], Mb=Mb, Mcat=Mcat, sigmaR=s, zc=zc, rho_need=rho_need, rho_free=rho_free, rvir=rvir, r12=rh / KPC,
             P=rho_need / rho_free if rho_need > 0 else 0.0)
    (rows if r["delta"] > 0.05 else noex).append(d)
P(f"\n  {'dwarf':18s} {'host':6s} {'Delta':>6s} {'M_cat':>9s} {'sig(R_L)':>8s} {'z_c':>5s} {'rho_need':>9s} {'rho_vir,free':>12s} {'P':>7s} {'r12/rvir':>8s}")
for d in sorted(rows, key=lambda d: d["zc"]):
    P(f"  {d['name']:18s} {d['host']:6s} {d['delta']:+6.2f} {d['Mcat']:9.2e} {d['sigmaR']:8.2f} {d['zc']:5.1f} {d['rho_need']:9.2e} {d['rho_free']:12.2e} {d['P']:7.1f} {d['r12'] / d['rvir']:8.3f}")
P(f"  no excess (Delta <= 0.05, excluded): {', '.join(d['name'] for d in noex)}")
x = np.log10([d["rho_free"] for d in rows]); y = np.log10([d["rho_need"] for d in rows])
rho, p = spearmanr(x, y, alternative="greater"); sl = float(np.polyfit(x, y, 1)[0]) if np.ptp(x) > 0 else float("nan")
Pm = float(np.median([d["P"] for d in rows])); inside = all(d["r12"] < d["rvir"] for d in rows)
t1 = rho > 0 and p < 0.05 and 0.5 <= sl <= 1.5; t2 = 1 <= Pm <= 300
cls = "SUPPORTS" if (t1 and t2) else ("AMPLITUDE ONLY" if t2 else "FAILS")
P(f"\n  T1 trend: Spearman rho {rho:+.2f} (p {p:.3f}), log-log slope {sl:.2f}  (range of log rho_vir,free {np.ptp(x):.2f} dex vs log rho_need {np.ptp(y):.2f} dex)")
P(f"  T2 amplitude: median P = rho_need / rho_vir,free = {Pm:.1f}  (r12 < r_vir for all: {inside})")
P(f"  field dwarfs with excess: " + ", ".join(f"{d['name']} P {d['P']:.1f}" for d in rows if d["host"] == "field"))
P(f"\n  CLASS: {cls}")
RES = dict(lane="CFG844", mutate=MUT, sigma8=sigma(8 / h), rows=rows, no_excess=[d["name"] for d in noex], rho=float(rho), p=float(p), slope=sl, P_median=Pm, inside=inside, cls=cls)
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg844_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg844{sfx}.out"), "w").write("\n".join(OUT) + "\n")
