"""CFG852 -- does the dwarf excess track gas loss (metallicity deficit at fixed M*)?  Criteria: FROZEN_CRITERIA.md (9f77f4463).
Run: python3 cfg852.py (CFG852_MUTATE=1).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG852_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC, a0 = 6.674e-11, 1.989e30, 3.0857e16, 9.3603e-11
nu = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15)))); law = lambda gN: gN * nu(gN / a0)
def fnum(x):
    try: return float(x)
    except: return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
EXCL = {"LMC", "SMC", "WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32"}
R28 = {r["name"]: r for r in json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))["canonical|nu_e"]["rows"]}
def delta_ups2(r):
    MV, s, rh = fnum(r.get("M_V")), fnum(r.get("vlos_sigma")), fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
    if None in (MV, s, rh): return None
    r12 = (4 / 3) * rh * PC; Ms = 2.0 * 10 ** (0.4 * (4.83 - MV)); gb = G * (Ms / 2) * Msun / r12 ** 2
    return math.log10(3 * (s * 1e3) ** 2 / r12 / law(gb)), math.log10(gb)
def sample(primary):
    S = []
    for nm, r in LVD.items():
        Z, MV = fnum(r.get("metallicity")), fnum(r.get("M_V"))
        if Z is None or MV is None or nm in EXCL: continue
        if primary:
            if nm not in R28: continue
            d, lg = R28[nm]["delta"], R28[nm]["lgbar"]
        else:
            x = delta_ups2(r)
            if x is None: continue
            d, lg = x
        S.append(dict(name=nm, d=d, lg=lg, Z=Z, lL=0.4 * (4.83 - MV)))
    return S
def analyse(S, rng=None, inj=False, shuf=False):
    lL = np.array([s["lL"] for s in S]); Z = np.array([s["Z"] for s in S]); d = np.array([s["d"] for s in S]); lg = np.array([s["lg"] for s in S])
    c1, c0 = np.polyfit(lL, Z, 1); dZ = Z - (c0 + c1 * lL)
    if inj: d = -0.5 * dZ + rng.normal(0, 0.1, len(d))
    if shuf: dZ = rng.permutation(dZ)
    A = np.vstack([np.ones_like(lg), lg]).T; rd = d - A @ np.linalg.lstsq(A, d, rcond=None)[0]; rz = dZ - A @ np.linalg.lstsq(A, dZ, rcond=None)[0]
    rho, pl = spearmanr(rz, rd, alternative="less"); _, pg = spearmanr(rz, rd, alternative="greater")
    return dict(N=len(S), c1=float(c1), rho=float(rho), p_less=float(pl), p_greater=float(pg))
P("CFG852  dwarf excess vs metallicity deficit at fixed M* (gas-loss proxy)" + ("  [MUTATE]" if MUT else ""))
RES = dict(lane="CFG852", mutate=MUT)
pri, sec = sample(True), sample(False)
if MUT:
    rng = np.random.default_rng(852)
    for lab, S in (("primary", pri), ("secondary", sec)):
        a, b = analyse(S, rng, inj=True), analyse(S, rng, shuf=True)
        P(f"  [{lab}] injection rho {a['rho']:+.2f} p(<0) {a['p_less']:.4f} -> {'SIGNAL' if a['p_less'] < 0.05 else 'none'} (must be SIGNAL); shuffle rho {b['rho']:+.2f} p(<0) {b['p_less']:.3f} -> {'SIGNAL' if b['p_less'] < 0.05 else 'none'} (must be none)")
        RES[lab] = dict(inj=a, shuf=b)
else:
    a, b = analyse(pri), analyse(sec)
    RES.update(primary=a, secondary=b)
    P(f"  [primary: CFG828 dwarfs, Ups_SFH]  N {a['N']}  MZR slope {a['c1']:.3f}  partial rho(Delta, dZ | g_bar) {a['rho']:+.3f}  p(<0) {a['p_less']:.3f}  p(>0) {a['p_greater']:.3f}")
    P(f"  [secondary: all LVD pressure-supported, Ups 2]  N {b['N']}  MZR slope {b['c1']:.3f}  partial rho {b['rho']:+.3f}  p(<0) {b['p_less']:.3f}  p(>0) {b['p_greater']:.3f}")
    cls = "NOT DIAGNOSTIC" if a["N"] < 12 else ("GAS-LOSS SIGNAL" if (a["rho"] < 0 and a["p_less"] < 0.05 and b["rho"] < 0 and b["p_less"] < 0.10) else ("OPPOSITE" if (a["rho"] > 0 and a["p_greater"] < 0.05) else "NO SIGNAL"))
    RES["cls"] = cls; P(f"\n  CLASS: {cls}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg852_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg852{sfx}.out"), "w").write("\n".join(OUT) + "\n")
