"""CFG814 -- H-EX with per-cluster catchment retention from the measured eROSITA outskirt slope (-3 at r200m = 2.2 R500),
primary P (r^-3 to r_ta) and bracket F (r^-3 to 2 r200m, then r^-2).  Criteria: FROZEN_CRITERIA.md (aba237371).  Uses CFG809's machinery read-only (exec'd defs).  Run: python3 cfg813.py [workers]
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, json, time
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
EXT = os.path.abspath(os.path.join(LANES, "..", "..", "_external_data"))
os.environ["CFG809_MODE"] = "defs"
SRC = os.path.join(LANES, "CFG809_expelled_gas_split", "cfg809.py")
txt = open(SRC).read().split("# ============================================================================================ eRASS1 (CFG687)")[0]
G = {"__file__": SRC, "__name__": "cfg809_defs"}; exec(compile(txt, SRC, "exec"), G)
d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
lam = np.array(json.load(open(os.path.join(EXT, "cfg726_work", "lambda.json")))["lam"], float)
SEL = np.where(lam > 0)[0]
BR = {"P": None, "F": None}

import math
DT = json.load(open(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_delta_ta.json")))
_h = 0.6736; _FB = 0.02237 / (0.02237 + 0.1200); _OM = (0.02237 + 0.1200) / _h ** 2; _RHOM0 = _OM * 2.775e11 * _h ** 2
def f_eff_of(i, prof):
    R5, mgas, z = float(d["R500"][i]), float(d["mg"][i]), float(d["z"][i])
    r = np.logspace(-3, np.log10(60), 6000); rc = 0.15 * R5; Rm = 2.2 * R5
    sh = (1 + (r / rc) ** 2) ** -1.0; sm = (1 + (Rm / rc) ** 2) ** -1.0
    sh = np.where(r > Rm, sm * (r / Rm) ** -3.0, sh)
    if prof == "F":
        s2 = sm * 2.0 ** -3.0; sh = np.where(r > 2 * Rm, s2 * (r / (2 * Rm)) ** -2.0, sh)
    dm = 4 * np.pi * r ** 2 * sh; Mm = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r))]; Mm *= mgas / np.interp(R5, r, Mm)
    M3 = float(np.interp(3.0, r, Mm)); Mc = lam[i] * 10 ** 10.7; rta = 5.0
    for _ in range(200):
        bc = float(np.interp(rta, r, Mm)) + Mc
        rn = (3 * bc / _FB / (4 * math.pi * float(np.interp(z, DT["z"], DT["D"])) * _RHOM0 * (1 + z) ** 3)) ** (1 / 3)
        if abs(rn - rta) < 1e-7: break
        rta = 0.5 * (rta + rn)
    return min((M3 + Mc) / bc, 1.0)
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def gas(i):
    R5, mgas = float(d["R500"][i]), float(d["mg"][i]); r = G["RGRID"]; rc = 0.15 * R5; sh = (1 + (r / rc) ** 2) ** -1.0; sh[r > 3] = 0
    dm = 4 * np.pi * (r * G["MPC"]) ** 2 * sh; Mm = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r * G["MPC"]))]
    return Mm * (mgas / np.interp(R5, r, Mm)), R5
def job(arg):
    i, br = arg
    Mg, R5 = gas(i)
    fs = lam[i] * 10 ** 10.7 / Mg[-1]
    fe = f_eff_of(i, br)
    def catch_fixed(Mc_tot, Mhot_tot, fe=fe):
        ret = Mc_tot + Mhot_tot; bc = ret / fe
        return bc, 5.364 * bc, ret / bc
    G["catch_ex"] = catch_fixed
    o = G["cluster_runs"](Mg, fs, float(d["z"][i]), R5 * 1000.0)
    return i, br, fs, o
if __name__ == "__main__":
    T0 = time.time(); NW = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    jobs = [(int(i), b) for b in BR for i in SEL]
    with Pool(NW) as p:
        res = p.map(job, jobs, chunksize=1)
    R = {(i, b): (fs, o) for i, b, fs, o in res}
    P(f"CFG814  eROSITA-outskirt catchment H-EX: {len(SEL)} redMaPPer-matched eRASS1 clusters; {time.time() - T0:.0f} s")
    ER809 = list(np.load(os.path.join(EXT, "cfg809_work", "erass.npy"), allow_pickle=True)); k = "s|canonical|EX"
    feP = np.array([f_eff_of(int(i), "P") for i in SEL]); feF = np.array([f_eff_of(int(i), "F") for i in SEL])
    k1 = abs(np.median(feP) - 0.761) < 0.01
    P(f"  K1 median f_eff (P) {np.median(feP):.3f} vs frozen expectation 0.761 -> {'PASS' if k1 else 'FAIL'} (bracket F median {np.median(feF):.3f})")
    k2 = None
    P("  K2 not evaluable: CFG813 stored scores only, no per-cluster profiles (disclosed)")
    fr = np.array([R[(int(i), "P")][1][k]["meta"]["fret"] for i in SEL])
    P(f"  realised f_ret (P) median {np.median(fr):.3f}")
    D, E = d["D"][SEL], d["E"][SEL]; W = np.where(E > 0, 1 / E ** 2, 0); n = len(SEL)
    order = np.argsort(d["ra"][SEL]); patch = np.empty(n, int); patch[order] = np.arange(n) * 15 // n
    BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
    A_of = lambda sel, Pm: {b: (W[sel][:, j] * D[sel][:, j]).sum() / (W[sel][:, j] * Pm[sel][:, j]).sum() for b, j in BANDS.items()}
    def jk(sel0, Pm):
        full = A_of(sel0, Pm); reps = [A_of(sel0 & (patch != q), Pm) for q in range(15)]
        return {b: (float(full[b]), float(np.sqrt(14 / 15 * np.sum((np.array([r[b] for r in reps]) - np.mean([r[b] for r in reps])) ** 2)))) for b in full}
    mg = d["mg"][SEL]; half = [mg <= np.median(mg), mg > np.median(mg)]; allm = np.ones(n, bool)
    def score(Pm, lab):
        A = jk(allm, Pm); h = [jk(t, Pm)["MID"] for t in half]
        zm, zo = (A["MID"][0] - 1) / A["MID"][1], (A["OUTER"][0] - 1) / A["OUTER"][1]; zh = [(x[0] - 1) / x[1] for x in h]
        ok = abs(zm) < 2 and abs(zo) < 2 and all(abs(z) < 3 for z in zh); S = zm ** 2 + zo ** 2 + sum(z ** 2 for z in zh)
        P(f"  {lab:34s}: MID {A['MID'][0]:.2f}+-{A['MID'][1]:.2f} (Z {zm:+.1f}) OUTER {A['OUTER'][0]:.2f}+-{A['OUTER'][1]:.2f} (Z {zo:+.1f}) halves MID "
          + " ".join(f"{x[0]:.2f}(Z{z:+.1f})" for x, z in zip(h, zh)) + f"  sumZ2 {S:.1f} -> {'pass' if ok else 'fail'}")
        return dict(A=A, halves=h, ok=bool(ok), S=float(S))
    RES = dict(lane="CFG814", n=n, K1=bool(k1), median_feff_P=float(np.median(feP)), median_feff_F=float(np.median(feF)))
    RES["plain_law"] = score(d["PL"][SEL], "plain law (CFG687 PL)")
    RES["cfg809_fs020"] = score(np.array([ER809[int(i)][k]["base"] + ER809[int(i)][k]["res"] for i in SEL]), "CFG809 H-EX fs=0.20")
    for b in BR:
        for kk in ("s|canonical|EX", "s|alt|EX"):
            Pm = np.array([R[(int(i), b)][1][kk]["base"] + R[(int(i), b)][1][kk]["res"] for i in SEL])
            RES[f"{b}|{kk}"] = score(Pm, f"fair {b} {kk}")
    cls = "CONFIRMED" if RES["P|s|canonical|EX"]["ok"] else "NOT CONFIRMED"
    rob = RES["F|s|canonical|EX"]["ok"]
    P(f"\n  CLASS (primary P, canonical): {cls}" + ("; ROBUST (bracket F also passes)" if (cls == "CONFIRMED" and rob) else ("; bracket F fails" if cls == "CONFIRMED" else "")))
    RES.update(cls=cls, robust=bool(rob))
    json.dump(RES, open(os.path.join(HERE, "cfg814_results.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg814.out"), "w").write("\n".join(OUT) + "\n")
