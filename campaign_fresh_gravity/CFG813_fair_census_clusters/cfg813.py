"""CFG813 -- fair census test of H-EX on 76 redMaPPer-matched eRASS1 clusters (M_cond = lambda x 10^10.7, brackets x0.5/x2).
Criteria: FROZEN_CRITERIA.md (553e544df).  Uses CFG809's machinery read-only (exec'd defs).  Run: python3 cfg813.py [workers]
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
BR = {"x1": 1.0, "x0.5": 0.5, "x2": 2.0}
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
    fs = 0.20 if br == "fs0.20" else lam[i] * 10 ** 10.7 * BR[br] / Mg[-1]
    o = G["cluster_runs"](Mg, fs, float(d["z"][i]), R5 * 1000.0)
    return i, br, fs, o
if __name__ == "__main__":
    T0 = time.time(); NW = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    jobs = [(int(i), b) for b in BR for i in SEL] + [(int(i), "fs0.20") for i in SEL[:5]]
    with Pool(NW) as p:
        res = p.map(job, jobs, chunksize=1)
    R = {(i, b): (fs, o) for i, b, fs, o in res}
    P(f"CFG813  fair census test: {len(SEL)} redMaPPer-matched eRASS1 clusters; {time.time() - T0:.0f} s")
    ER809 = list(np.load(os.path.join(EXT, "cfg809_work", "erass.npy"), allow_pickle=True))
    k = "s|canonical|EX"
    dev = max(float(np.max(np.abs(R[(int(i), "fs0.20")][1][k]["base"] + R[(int(i), "fs0.20")][1][k]["res"] - ER809[int(i)][k]["base"] - ER809[int(i)][k]["res"]) / np.maximum(np.abs(ER809[int(i)][k]["base"] + ER809[int(i)][k]["res"]), 1e-30))) for i in SEL[:5])
    k1 = dev < 1e-6
    P(f"  K1 fs=0.20 rerun vs CFG809 stored (5 clusters): max rel {dev:.1e} -> {'PASS' if k1 else 'FAIL'}")
    fr = np.array([R[(int(i), "x1")][1][k]["meta"]["fret"] for i in SEL]); fsv = np.array([R[(int(i), "x1")][0] for i in SEL])
    k2 = float(np.median(fr)) < 0.60
    P(f"  K2 median f_ret {np.median(fr):.3f} (range {fr.min():.2f}-{fr.max():.2f}); median fs {np.median(fsv):.3f} -> {'PASS' if k2 else 'FAIL'} (floor unbound)")
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
    RES = dict(lane="CFG813", n=n, K1=bool(k1), K2=bool(k2), median_fret=float(np.median(fr)))
    RES["plain_law"] = score(d["PL"][SEL], "plain law (CFG687 PL)")
    RES["cfg809_fs020"] = score(np.array([ER809[int(i)][k]["base"] + ER809[int(i)][k]["res"] for i in SEL]), "CFG809 H-EX fs=0.20")
    for b in BR:
        for kk in ("s|canonical|EX", "s|alt|EX"):
            Pm = np.array([R[(int(i), b)][1][kk]["base"] + R[(int(i), b)][1][kk]["res"] for i in SEL])
            RES[f"{b}|{kk}"] = score(Pm, f"fair {b} {kk}")
    pr, ref = RES["x1|s|canonical|EX"], RES["cfg809_fs020"]
    def cls_of(r):
        return "FAIR PASS" if (r["ok"] and r["S"] < ref["S"]) else ("IMPROVES" if r["S"] < ref["S"] else "NO GAIN")
    cls = cls_of(pr); brs = [cls_of(RES[f"{b}|s|canonical|EX"]) for b in ("x0.5", "x2")]
    P(f"\n  CLASS (primary, canonical): {cls}; brackets x0.5/x2: {brs[0]} / {brs[1]} -> {'ROBUST' if all(c == cls for c in brs) else 'BRACKET-DEPENDENT'}")
    RES.update(cls=cls, brackets=brs)
    json.dump(RES, open(os.path.join(HERE, "cfg813_results.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg813.out"), "w").write("\n".join(OUT) + "\n")
