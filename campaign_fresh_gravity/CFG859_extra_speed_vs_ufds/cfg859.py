"""CFG859 -- does CFG856's extra isothermal speed survive the ultra-faint dwarfs?  Criteria: FROZEN_CRITERIA.md (a40dd5cd9).
Run: python3 cfg859.py (CFG859_MUTATE=1: V_x x 0.3).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG859_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; UPS = 2.20
VX = {"canonical": 9.42, "alt": 9.24}
nu = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15)))); 
def fnum(x):
    try: return float(x)
    except: return None
LVD = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv")))}
U26 = json.load(open(os.path.join(LANES, "CFG826_ufd_age_crosscheck", "cfg826_results.json")))
prim_names = list(U26["canonical|E|primary"]["rows"].keys())
AMAP_SIG = {}
for l in open(os.path.join(REPO, "real_research", "data", "arroyopolonio2026_ufd_binary_corrected.tsv")):
    if l.startswith("#") or l.startswith("name"): continue
    v = l.rstrip("\n").split("\t"); AMAP_SIG[v[0]] = (float(v[11]), 0.5 * (float(v[12]) + float(v[14])))
AMAP = {"Boo I": "Bootes I", "Car II": "Carina II", "Hyd I": "Hydrus I", "Leo V": "Leo V", "Ret II": "Reticulum II", "Seg 1": "Segue 1", "Wil 1": "Willman 1"}
prim = []
for k, nm in AMAP.items():
    if nm in prim_names: s, e = AMAP_SIG[k]; prim.append((nm, s, e))
USED = set(json.load(open(os.path.join(LANES, "CFG824_dwarf_age_fossil", "cfg824_results.json")))["rows"]) | {"Antlia II", "Crater II", "Sextans"} | set(prim_names)
sec = [(nm, fnum(r["vlos_sigma"]), fnum(r.get("vlos_sigma_em")) or 0.1 * fnum(r["vlos_sigma"])) for nm, r in LVD.items()
       if fnum(r.get("M_V")) is not None and fnum(r["M_V"]) > -7.7 and fnum(r.get("vlos_sigma")) and (fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))) and nm not in USED and nm not in ("LMC", "SMC")]
def sig_law(nm, a0):
    r = LVD[nm]; rh = (4 / 3) * (fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))) * PC; M = UPS * 10 ** (0.4 * (4.83 - fnum(r["M_V"])))
    gN = G * (M / 2) * Msun / rh ** 2; return math.sqrt(gN * nu(gN / a0) * rh / 3) / 1e3, rh
def E_of(S, a0, vx, rc=0.0):
    E = []
    for nm, s, e in S:
        sl, rh = sig_law(nm, a0); rk = rh / PC
        fx = rk ** 2 / (rk ** 2 + rc ** 2) if rc > 0 else 1.0                  # cored isothermal: M_x(<r) = Vx^2 r^3/(G(r^2+rc^2))
        E.append(math.log(s / math.sqrt(sl ** 2 + fx * vx ** 2 / 3)))
    E = np.array(E); return float(E.mean()), float(E.std(ddof=1) / math.sqrt(len(E))), E
P("CFG859  CFG856's extra speed vs the ultra-faint dwarfs" + ("  [MUTATE V_x x0.3]" if MUT else ""))
RES = dict(lane="CFG859", mutate=MUT)
for foot in ("canonical", "alt"):
    a0 = A0[foot]; vx = VX[foot] * (0.3 if MUT else 1.0)
    for lab, S in (("primary (binary-corrected)", prim), ("secondary (literature sigma)", sec)):
        m, se, E = E_of(S, a0, vx); m0, se0, _ = E_of(S, a0, 0.0)
        cls = "SURVIVES UFDs" if abs(m) < 2 * se else ("OVER-PREDICTS UFDs (needs a core)" if m <= -2 * se else "UNDER-PREDICTS")
        rc = None
        if lab.startswith("primary") and cls.startswith("OVER") and not MUT:
            f = lambda rc: E_of(S, a0, vx, rc)[0]
            rc = brentq(f, 1e-3, 1e5) if f(1e5) > 0 else None
        RES[f"{foot}|{lab}"] = dict(N=len(S), E=m, se=se, E_law_only=m0, cls=cls, rc_pc=rc, names=[x[0] for x in S])
        P(f"  [{foot} | {lab}] N {len(S)}: E = ln(sigma_obs/sigma_pred) {m:+.3f} +- {se:.3f}  (law alone {m0:+.3f})  -> {cls}" + (f"   post-hoc core radius r_c = {rc:.0f} pc" if rc else ""))
RES["cls"] = RES["canonical|primary (binary-corrected)"]["cls"]
P(f"\n  K1 law-only primary E (Ups 2.20) = {RES['canonical|primary (binary-corrected)']['E_law_only']:+.3f}  (CFG826 +0.70 at Ups 2, +0.68 at 2.20)")
P(f"\n  CLASS (canonical, primary): {RES['cls']}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg859_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg859{sfx}.out"), "w").write("\n".join(OUT) + "\n")
