#!/usr/bin/env python3
"""AR1 K2 diagnosis, written after K2 failed and before any graded row was read. Null of dr8_action.py (M_b 0, same seeds, F 0, 12 passes), and the new solver on finer grids. A failed K2 stays failed; this says which side the 1.5 % sits on. kappa = 1/2 FITTED, unused; not theory closed."""
import math, os, pickle, sys
sys.dont_write_bytecode = True
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path[:0] = [HERE, os.path.join(RB, "DR8_pressure_core_response")]; import ar1_solver as A, dr8_ic as IC, dr8_action as AC
CD = os.path.join(HERE, "cache_k2"); OUT = []
def P(s): print(s, flush=True); OUT.append(str(s))
S = IC.setup(); Rd, r0, R2, Md = S["Rd"], S["r0"], S["R2"], S["Md"]; x, v, m, Msim, Mod = IC.build("core", S, 100, 1, 0.1); RR = np.array([1, 2, 2.2, 3, 4, 6, 8, 10.0]) * Rd; frac = 1 - Md / Msim; FF = Md / (Msim - Md); Qof = lambda M, g, m0, rr: np.interp(np.log(rr), np.log(g), M) / np.interp(np.log(rr), np.log(g), m0)
Qd = np.array([pickle.load(open(os.path.join(CD, f"s{s}.pkl"), "rb"))[0] for s in range(1, 9)]); N = []
for sd in range(1, 9):
    f = os.path.join(CD, f"n{sd}.pkl")
    if not os.path.exists(f):
        xx, vv, mm, Ms, Mo = IC.build("core", S, 100000, 100 + sd, 0.1); rg = np.geomspace(max(Mo.r[0], 2e-5), Mo.r[-1] * 3, 2500); Mi = np.where(rg < Mo.r[0], Mo.M[0], np.interp(np.log(rg), np.log(Mo.r), Mo.M)); Mf, ch, _, _ = AC.respond(xx, vv, rg, Mi, 0 * rg, 1.0, mm, passes=12); pickle.dump(Qof(Mf, rg, Mi, RR), open(f, "wb")); print("null", sd, ch, flush=True)
    N.append(pickle.load(open(f, "rb")))
N = np.array(N); P("dr8_action null Q, M_b 0, should be 1: " + " ".join(f"{q:.4f}" for q in np.median(N, 0)) + "; standard error " + " ".join(f"{q:.4f}" for q in np.std(N, 0, ddof=1) / math.sqrt(8)))
Qc = np.median(Qd / N, 0); P("dr8_action Q / its own null, same seeds: " + " ".join(f"{q:.3f}" for q in Qc))
rg3 = np.geomspace(2e-5, R2, 1500); M3 = np.interp(np.log(rg3), np.log(Mod.r), Mod.M) * frac; Mb3 = Md * (1 - Rd / np.sqrt(rg3 ** 2 + Rd ** 2))
for kw in (dict(), dict(nE=256, nY=48, nT=96), dict(nE=512, nY=64, nT=128, dl=0.005)):
    Qn = Qof(A.act_contract(rg3, Mb3, M3, FF, **kw)[0], rg3, M3, RR); P(f"new {kw or 'graded grid'}: Q " + " ".join(f"{q:.3f}" for q in Qn) + " | / dr8 raw " + " ".join(f"{q:+.3f}" for q in (Qn / np.median(Qd, 0) - 1)) + " | / dr8 null-corrected " + " ".join(f"{q:+.3f}" for q in (Qn / Qc - 1)))
open(os.path.join(HERE, "ar1_k2b.out"), "w").write("\n".join(OUT) + "\n")
