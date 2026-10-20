"""CFG871 -- is the dwarf cold core's size set by its dispersion through the law, r_c = (9/2) sigma^2/a0?  Criteria: FROZEN_CRITERIA.md (9418bfeea).
Run: python3 cfg871.py (CFG871_MUTATE=1: coefficient 1).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG871_MUTATE") == "1"; COEF = 1.0 if MUT else 4.5; OUT = []
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
SIG = {}
for l in open(os.path.join(REPO, "real_research", "data", "arroyopolonio2026_ufd_binary_corrected.tsv")):
    if l.startswith("#") or l.startswith("name"): continue
    v = l.rstrip("\n").split("\t"); SIG[v[0]] = float(v[11])
AMAP = {"Boo I": "Bootes I", "Car II": "Carina II", "Hyd I": "Hydrus I", "Leo V": "Leo V", "Ret II": "Reticulum II", "Seg 1": "Segue 1", "Wil 1": "Willman 1"}
UFD = [(nm, SIG[k], 2.20) for k, nm in AMAP.items()]
def dwarf(nm, a0, ups):
    L = LVD[nm]; rh = (4 / 3) * (fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical"))) * PC
    M = ups * 10 ** (0.4 * (4.83 - fnum(L["M_V"]))); gN = G * (M / 2) * Msun / rh ** 2
    return math.sqrt(gN * nu(gN / a0) * rh / 3) / 1e3, rh / PC
P("CFG871  law-linked core: r_c = (9/2) sigma^2/a0?" + ("  [MUTATE coefficient 1]" if MUT else ""))
RES = dict(lane="CFG871", mutate=MUT, coef=COEF)
grid = np.geomspace(10, 3000, 400)
for foot in ("canonical", "alt"):
    a0 = A0[foot]; mw = [(r["name"], R24[r["name"]]["so"], R27[r["name"]]["ups"]) for r in R28[f"{foot}|nu_e"]["rows"] if (LVD[r["name"]].get("host") == "mw") and r["delta"] > 0.05]
    def vx_at(rc):
        lv = []
        for nm, so, ups in mw:
            sl, rpc = dwarf(nm, a0, ups); f = rpc ** 2 / (rpc ** 2 + rc ** 2)
            if so > sl: lv.append(0.5 * math.log10(3 * (so ** 2 - sl ** 2) / f))
        return 10 ** float(np.mean(lv))
    def E_at(rc):
        vx = vx_at(rc); E = []
        for nm, so, ups in UFD:
            sl, rpc = dwarf(nm, a0, ups); f = rpc ** 2 / (rpc ** 2 + rc ** 2); E.append(math.log(so / math.sqrt(sl ** 2 + f * vx ** 2 / 3)))
        E = np.array(E); return float(E.mean()), float(E.std(ddof=1) / math.sqrt(len(E))), vx
    ev = np.array([E_at(rc) for rc in grid]); Em, Es, Vx = ev[:, 0], ev[:, 1], ev[:, 2]
    in1 = grid[np.abs(Em) <= Es]; in2 = grid[np.abs(Em) <= 2 * Es]
    best = float(grid[np.argmin(np.abs(Em))]); vbest = float(Vx[np.argmin(np.abs(Em))]); sig = vbest / math.sqrt(2)
    rpred = COEF * (sig * 1e3) ** 2 / a0 / PC
    ok = len(in2) > 0 and in2.min() <= rpred <= in2.max()
    Mcl = 81 * (sig * 1e3) ** 4 / (4 * G * a0) / Msun; rho = Mcl / (4 * math.pi * best ** 3 / 3)
    RES[foot] = dict(rc_best=best, rc_1sig=[float(in1.min()), float(in1.max())] if len(in1) else None, rc_2sig=[float(in2.min()), float(in2.max())] if len(in2) else None,
                     Vx_best=vbest, sigma=sig, rc_pred=rpred, ratio=rpred / best, consistent=ok, M_clump=Mcl, rho_mean_in_rc=rho)
    P(f"\n  [{foot}] r_c best (UFD E = 0) = {best:.0f} pc;  1-sigma {in1.min():.0f}-{in1.max():.0f} pc;  2-sigma {in2.min():.0f}-{in2.max():.0f} pc" if len(in1) else f"\n  [{foot}] r_c best {best:.0f}; ranges empty")
    P(f"     V_x at best r_c {vbest:.2f} km/s -> sigma {sig:.2f} km/s;  r_c,pred = {COEF:g} sigma^2/a0 = {rpred:.0f} pc  (ratio {rpred / best:.2f})  -> {'inside' if ok else 'OUTSIDE'} the 2-sigma range")
    P(f"     implied clump mass M = 81 sigma^4/(4 G a0) = {Mcl:.2e} Msun; mean density inside r_c {rho:.2f} Msun/pc^3")
k1 = None
cls = "LAW-LINKED CORE CONSISTENT" if all(RES[f]["consistent"] for f in ("canonical", "alt")) else "INCONSISTENT"
RES["cls"] = cls; P(f"\n  CLASS: {cls}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg871_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg871{sfx}.out"), "w").write("\n".join(OUT) + "\n")
