"""CFG858 -- can the stiffened action produce the dwarfs' extra speed?  Criteria: FROZEN_CRITERIA.md (bb25c4ddd).
Solves u^2/(a0-u) - (L*^2/2)(u'' + 2u'/r - 2u/r^2) = g_N for Plummer dSphs.  Run: python3 cfg858.py (CFG858_MUTATE=1: sign flip).
Units: r in kpc, accelerations in units of a0.  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
from scipy.integrate import solve_bvp
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG858_MUTATE") == "1"; SGN = -1.0 if MUT else 1.0; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
GK = 4.30091e-6; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; TOKPC = 3.0857e19 / 1e6
def fnum(x):
    try: return float(x)
    except: return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
R27 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
# Sextans has no Weisz SFH (not in CFG827): Upsilon_V = 2 as in CFG821 (deviation disclosed in README)
DW = ["Draco", "Ursa Minor", "Sextans", "Canes Venatici I", "Leo II", "Fornax"]
LST = [1, 3, 10, 24, 31, 100, 300, 1000]
ulaw = lambda gN: 0.5 * (-gN + np.sqrt(gN * gN + 4 * gN))
def solve(M, a, L, a0u):
    gN = lambda r: GK * M * r / (r * r + a * a) ** 1.5 / a0u
    r = np.geomspace(1e-3 * a, 300 * a, 600); uL = ulaw(gN(r))
    c = (L / 1000.0) ** 2 / 2 * SGN
    def f(r, y):
        u = np.minimum(y[0], 0.999999); return np.vstack([y[1], (u * u / (1 - u) - gN(r)) / c - 2 * y[1] / r + 2 * y[0] / r ** 2])
    def bc(ya, yb): return np.array([ya[0] - r[0] * ya[1], yb[0] - ulaw(gN(r[-1]))])
    y0 = np.vstack([uL, np.gradient(uL, r)])
    s = solve_bvp(f, bc, r, y0, tol=1e-6, max_nodes=200000)
    return s, gN, uL, r
P("CFG858  stiffened action vs the dwarfs' extra speed" + ("  [MUTATE anti-stiffness]" if MUT else ""))
RES = dict(lane="CFG858", mutate=MUT, rows={}); allmax = 0.0; atr = []
for foot in ("canonical", "alt"):
    a0u = A0[foot] * TOKPC
    P(f"\n  [{foot}]  G_ratio = g(r1/2)/g_law(r1/2) for L* (pc) = {LST}")
    for nm in DW:
        Lr = LVD[nm]; a = (fnum(Lr.get("rhalf_sph_physical")) or fnum(Lr.get("rhalf_physical"))) / 1000; M = R27.get(nm, {"ups": 2.0})["ups"] * 10 ** (0.4 * (4.83 - fnum(Lr["M_V"])))
        r12 = 4 / 3 * a; row = []
        for L in LST:
            s, gN, uL, r = solve(M, a, L, a0u)
            if not s.success: row.append(float("nan")); continue
            u12 = float(s.sol(r12)[0]); gl12 = float(gN(r12) + ulaw(gN(r12))); gr = (gN(r12) + u12) / gl12
            rr = np.geomspace(1e-2 * a, 100 * a, 400); ratio = (gN(rr) + s.sol(rr)[0]) / (gN(rr) + ulaw(gN(rr)))
            row.append(float(gr)); allmax = max(allmax, float(ratio.max())) if foot == "canonical" else allmax
            if foot == "canonical" and 24 <= L <= 1000: atr.append(gr)
        RES["rows"][f"{foot}|{nm}"] = row
        P(f"     {nm:18s} " + "  ".join(f"{x:.4f}" for x in row))
mx_window = max(atr) if atr else float("nan")
supply = sum(1 for nm in DW if max(RES["rows"][f"canonical|{nm}"][3:]) >= 10 ** 0.3) > len(DW) / 2
cls = "STIFFNESS CAN SUPPLY V_x" if supply else ("STIFFNESS ONLY SCREENS" if (mx_window <= 1 + 1e-3 and allmax <= 1.01) else "SMALL OVERSHOOT")
k1 = [RES["rows"][f"canonical|{nm}"][0] for nm in DW]
P(f"\n  K1 (L* = 1 pc): G_ratio {['%.4f' % x for x in k1]} (law = 1)")
P(f"  max G_ratio over dwarfs for L* in [24 pc, 1 kpc]: {mx_window:.4f};  max g/g_law anywhere (canonical, all L*): {allmax:.4f}")
pb = math.log(1.3) / math.log(1000 / 24); P(f"  coincidence base rate: P(random log-uniform L in [24 pc, 1 kpc] within x1.3 of 24 pc) = {pb:.2f}")
P(f"\n  CLASS: {cls}"); RES.update(max_window=mx_window, max_anywhere=allmax, base_rate=pb, cls=cls)
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg858_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg858{sfx}.out"), "w").write("\n".join(OUT) + "\n")
