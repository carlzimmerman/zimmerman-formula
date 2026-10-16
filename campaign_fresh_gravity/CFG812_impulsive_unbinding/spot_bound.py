"""CFG812 spot check: bound fraction of freed cold energy for 12 eRASS1 clusters spanning gas mass (canonical, nu_s, EX)."""
import os, sys, numpy as np
from multiprocessing import Pool
os.environ["CFG812_MODE"] = "defs"
src = os.path.abspath("cfg812.py")
txt = open(src).read().split("# ============================================================================================ eRASS1 (CFG687)")[0]
G = {"__file__": src, "__name__": "t"}; exec(compile(txt, src, "exec"), G)
d = np.load(os.path.join(G["LANES"], "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
idx = [int(x) for x in np.argsort(d["mg"])[np.linspace(0, len(d["mg"]) - 1, 12).astype(int)]]
def one(i):
    R5, mgas = float(d["R500"][i]), float(d["mg"][i]); r = G["RGRID"]; rc = 0.15 * R5; sh = (1 + (r / rc) ** 2) ** -1.0; sh[r > 3] = 0
    dm = 4 * np.pi * (r * G["MPC"]) ** 2 * sh; Mm = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r * G["MPC"]))]; Mg = Mm * (mgas / np.interp(R5, r, Mm))
    rk = r * 1000; mg = np.interp(G["R_OBS"], rk, Mg, left=0, right=Mg[-1]); mc = G["cond_profile"](G["R_OBS"], 0.2 * Mg[-1], R5 * 1000, "EX")
    *_, meta = G["run_system"](G["R_OBS"], mc, mg, float(d["z"][i]), "canonical", "s", "EX")
    return np.log10(mgas), meta["fret"], meta["res_frac"], meta["bound_frac"]
if __name__ == "__main__":
    with Pool(12) as p:
        out = p.map(one, idx)
    for lm, fr, rf, bf in out:
        print(f"log Mg {lm:.2f}: f_ret {fr:.3f}  free/supply {rf:.3f}  bound fraction {bf:.4f}")
    print("min bound fraction:", min(o[3] for o in out))
