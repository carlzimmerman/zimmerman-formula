#!/usr/bin/env python3
"""CFG527 halo concentration ratio (declared in FROZEN_CRITERIA.md 'Reported', CFG524 post-hoc definition, not gating):
median over the 100 highest CIC peaks (256^3, 3^3 periodic max filter) of M(<2 cells)/M(<8 cells), run / matched S0, z = 0.
The conc() routine is CFG524's (cfg524_posthoc.py), copied verbatim."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W, W521, W359 = (os.path.join(EXT, d) for d in ("cfg527_work", "cfg521_work", "cfg359_work"))
from scipy import fft as sfft, ndimage
NP, NPEAK = 256, 100
def conc(path, L):
    pos = np.load(path)["pos"].astype(np.float64); M = NP; dx = L / M
    u = pos / dx; i0 = np.floor(u).astype(np.int64); w = u - i0; i1 = (i0 + 1) % M; i0 %= M; rho = np.zeros(M ** 3)
    for cx in (0, 1):
        for cy in (0, 1):
            for cz in (0, 1):
                ix = (i1 if cx else i0)[:, 0]; iy = (i1 if cy else i0)[:, 1]; iz = (i1 if cz else i0)[:, 2]
                ww = (w[:, 0] if cx else 1 - w[:, 0]) * (w[:, 1] if cy else 1 - w[:, 1]) * (w[:, 2] if cz else 1 - w[:, 2])
                rho += np.bincount((ix * M + iy) * M + iz, weights=ww, minlength=M ** 3)
    del pos, u, i0, i1, w
    rho = (rho / rho.mean()).reshape((M,) * 3).astype(np.float32)
    mx = ndimage.maximum_filter(rho, size=3, mode="wrap"); pk = np.argwhere(rho == mx)
    top = pk[np.argsort(rho[pk[:, 0], pk[:, 1], pk[:, 2]])[::-1][:NPEAK]]
    g = np.arange(M); g = np.minimum(g, M - g).astype(np.float32)
    r2 = g[:, None, None] ** 2 + g[None, :, None] ** 2 + g[None, None, :] ** 2
    rk = sfft.rfftn(rho, workers=4); m = {}
    for Rc in (2, 8):
        ball = (r2 <= Rc * Rc).astype(np.float32)
        m[Rc] = sfft.irfftn(rk * sfft.rfftn(ball, workers=4), s=rho.shape, workers=4)[top[:, 0], top[:, 1], top[:, 2]]
    return float(np.median(m[2] / m[8])), float(rho.max())
L_ = []
def P(s=""): print(s); L_.append(s)
S0 = {50: os.path.join(W521, "cfg521_S0_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L50_z0.npz"),
      25: os.path.join(W521, "cfg521_S0_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L25_z0.npz"),
      100: os.path.join(W521, "cfg521_S0_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L100_z0.npz"),
      200: os.path.join(W359, "cfg359_S0_FLAT_canonical_N256_z0.npz")}
def t(mix, dr, L, ft="canonical", md="census", nc=False):
    return os.path.join(W, f"cfg527_RES_TA{'_NOCOMP' if nc else ''}_{mix}_MASSCONS_fret{md}_FLAT_{ft}_N256" + (f"_L{L}" if L != 200 else "") + f"_draw{dr}_z0.npz")
OUT = {}
P("Halo concentration ratio: median over the 100 highest peaks of M(<2 cells)/M(<8 cells), run / matched S0 (z = 0)")
for Lb in (200, 100, 50, 25):
    runs = {"LR-can": t("NOFILT", "SHELL", Lb), "LR-alt": t("NOFILT", "SHELL", Lb, "alt"), "K1": t("NOFILT", "SHELL", Lb, md="one"),
            "MUTATE A": t("MIXA", "SC", Lb), "SHF": t("MIXA", "SHELL", Lb), "MUTATE B": t("NOFILT", "SHELL", Lb, nc=True)}
    c0, pk0 = conc(S0[Lb], Lb); OUT[str(Lb)] = {"S0": c0}
    P(f"\nL = {Lb}: S0 median c = {c0:.4f} (peak 1+delta {pk0:.0f})")
    for n, p in runs.items():
        if not os.path.exists(p): continue
        c, pk = conc(p, Lb); OUT[str(Lb)][n] = c / c0
        P(f"  {n:10s} c/c_S0 = {c / c0:.4f}   (peak 1+delta {pk:.0f})")
open(os.path.join(HERE, "cfg527_posthoc.out"), "w").write("\n".join(L_) + "\n")
json.dump(OUT, open(os.path.join(HERE, "cfg527_posthoc.json"), "w"), indent=1)
