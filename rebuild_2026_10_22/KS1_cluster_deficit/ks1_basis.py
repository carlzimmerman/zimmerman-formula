#!/usr/bin/env python3
"""KS1 basis: for each cluster and h, the shear signal of hat(x) * M_gas and hat(x) * M_law g_gas/a0 through CU1's chain, linear projector. Read only of CU1. kappa = 1/2 FITTED; not theory closed."""
import os, sys, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, os.path.join(RB, "CU1_gas_term_replication"))
import numpy as np, cu1_core as C
NODES = np.array([.2, .35, .6, 1., 1.7, 3.5])
def hats(x):
    lx = np.log10(np.maximum(x, 1e-6)); ln = np.log10(NODES); o = []
    for j in range(len(ln)):
        e = np.zeros(len(ln)); e[j] = 1; o.append(np.interp(lx, ln, e))  # flat outside
    return np.array(o)
def proj_lin(M, off):
    rho = np.gradient(M, C.RM) / (4 * np.pi * C.RM ** 2); f = (rho[C._ii] * (1 - C._w) + rho[C._ii + 1] * C._w) * C._rrdu_m; du = C._u[:, 1] - C._u[:, 0]; Sig = 2 * du * (.5 * f[:, 0] + f[:, 1:-1].sum(1) + .5 * f[:, -1])
    if off > 1e-4:
        Rp = np.sqrt(C.RF[:, None] ** 2 + off ** 2 + 2 * C.RF[:, None] * off * np.cos(C.PHI)[None, :]); vals = np.interp(np.log(Rp), np.log(C.RF), Sig); Sig = (.5 * (vals[:, 0] + vals[:, -1]) + vals[:, 1:-1].sum(1)) * (C.PHI[1] - C.PHI[0]) / np.pi
    x = Sig * C.RF; cum = np.concatenate([[0.], np.cumsum(.5 * (x[1:] + x[:-1]) * np.diff(C.RF))]) + .5 * Sig[0] * C.RF[0] ** 2; dS = 2 * cum / C.RF ** 2 - Sig
    return np.interp(np.log(C.RC), np.log(C.RF), dS) / C.KG_PC2
if __name__ == "__main__":
    t0 = time.time(); S = C.Shear(.005, .034); N = S.N; os.makedirs(os.path.join(HERE, "cache_basis"), exist_ok=True); out = {}
    for hk, (h, hi, _) in C.HS.items():
        m = S.m; E = m["E"][:, hi]; W = np.where(E < 1e8, 1 / np.where(E > 0, E, np.inf) ** 2, 0.); den = m["den"][:, hi]; mm = m["m3to8"][:, hi]; G_ = np.zeros((N, 6, 8)); T_ = {f: np.zeros((N, 6, 8)) for f in C.A0}; Lg = np.zeros((N, 4)); R5s = np.zeros(N); Tn = {f: np.zeros((N, 8)) for f in C.A0}; Vl = {f: np.zeros((N, 8)) for f in C.A0}
        for i in range(N):
            c = S.chain[hk][i]; DM = float(S._dm(min(float(S.z[i]), 2.33))) * 101.54 / h; q = (DM / (1 + float(S.z[i]))) / S._DAcat(float(S.z[i])); R5 = float(S.R5[i]) * q; R5s[i] = R5; x = C.RG / R5; H = hats(x); Mg = c["Mb"] / 1.034
            # reduced-shear factor from the law plus a nominal term
            Ml = S.msrc("canonical", i, hk, 0); Mref = Ml + 4 * np.minimum(x ** -.6, 3) * Mg; _, Sb, _ = C.project(Mref, c["off"]); fr = np.ones(8); g = den[i] > 0; tot = sum(Sb ** (p + 1) * mm[i][p] for p in range(6)); fr[g] = 1 + tot[g] / den[i][g]
            for j in range(6):
                G_[i, j] = W[i] * proj_lin(H[j] * Mg, c["off"]) * fr
            for f, a0 in C.A0.items():
                Mlf = S.msrc(f, i, hk, 0); Vl[f][i] = W[i] * proj_lin(Mlf, c["off"]) * fr; tm = Mlf * C.G * Mg / C.RM ** 2 / a0
                Tn[f][i] = W[i] * proj_lin(tm, c["off"]) * fr
                for j in range(6): T_[f][i, j] = W[i] * proj_lin(H[j] * tm, c["off"]) * fr
            if i % 100 == 0: print(hk, i, round(time.time() - t0), flush=True)
        out[f"G_{hk}"] = G_; out[f"R5_{hk}"] = R5s; out[f"W_{hk}"] = W
        for f in C.A0: out[f"T_{f}_{hk}"] = T_[f]; out[f"Tall_{f}_{hk}"] = Tn[f]; out[f"Vl_{f}_{hk}"] = Vl[f]
    np.savez_compressed(os.path.join(HERE, "cache_basis", "basis.npz"), NODES=NODES, **out); print("done", round(time.time() - t0))
