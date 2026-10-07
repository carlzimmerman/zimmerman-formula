#!/usr/bin/env python3
"""CFG412 diagnostics, REPORTED ONLY (written after the frozen run; no verdict depends on them).
D1: K3 failed at 3e-3; repeat the linear V-web comparison with the Nyquist planes zeroed (odd derivatives at Nyquist
    are not real-symmetric) to see whether the gap is numerical.
D2: why the turnaround cover keeps the filament ON mass: split the T1-ON, l3 < 0 mass by (i) local delta >= Delta_ta - 1
    (the cell alone passes the spherical test), (ii) covered by B1 balls of peaks with ON radius >= 2 cells
    (resolved hosts, >= 1.56 Mpc/h), (iii) covered only by 0-1-cell balls, (iv) not covered.
D3: the T1-ON, l3 < 0 mass binned by local density 1 + delta.
CFG412_MUTATE=1: D2 uses T1 in place of B1 (coverage must become 100% trivially -> sanity of the bookkeeping).
"""
import os, sys, json, math
import numpy as np
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg412_screen as S

MUT = os.environ.get("CFG412_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
try:
    os.nice(15)
except OSError:
    pass
L, OUT = [], {}
def P(s=""):
    print(s, flush=True); L.append(s)

def cover_by_radius(delta, rmin_cells):
    """B1 painted only from peaks whose ON ball reaches >= rmin_cells."""
    M = S.M; fB = np.zeros(M ** 3, np.float32)
    mx = ndimage.maximum_filter(delta, size=3, mode="wrap")
    pk = np.argwhere((delta == mx) & (delta >= 3 * (S.TAU - S.EPS)))
    for c in pk:
        hw = 3
        while True:
            g, order, r2s, last, grp = S.geom(hw)
            ix, iy, iz = (c[0] + g) % M, (c[1] + g) % M, (c[2] + g) % M
            idx = ((ix[:, None, None] * M + iy[None, :, None]) * M + iz[None, None, :]).ravel()
            ds = delta.ravel()[idx][order].astype(np.float64)
            cum = np.cumsum(ds)[last]; n = last + 1
            F = np.minimum.accumulate(S.smear(((1.0 + cum / n) - 1.0) / 3.0))
            inside = r2s[last] <= hw * hw
            if F[inside][-1] > 0 and hw < 40:
                hw *= 2; continue
            break
        on = inside & (F > 0.5)
        rmax = math.sqrt(r2s[last][on][-1]) if on.any() else 0.0
        if rmax < rmin_cells:
            continue
        Fc = F[grp]; ok = inside[grp] & (Fc > 0)
        sel = idx[order][ok]; fB[sel] = np.maximum(fB[sel], Fc[ok])
    return fB.reshape((M,) * 3)

for foot in ("canonical", "alt"):
    snap = np.load(os.path.join(S.WORK, f"cfg410_RES_Rc3_MIXA_FLAT_{foot}_N256_z0.npz"))
    delta = S.deposit(snap["pos"].astype(np.float64)); rho = 1 + delta
    dk = S.fwd(delta)
    tk = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    t = [S.inv(S.KV[i] * S.KV[j] * dk * S.IK2) for i, j in tk]
    l1, l2, l3 = S.eig3(t); del t
    fT1 = S.smear(l2); onT = fT1 > 0.5; fil = l3 < 0
    # D1
    M = S.M; nyq = np.ones(dk.shape, bool); nyq[M // 2] = False; nyq[:, M // 2] = False; nyq[..., -1] = False
    dkn = dk * nyq
    tn = [S.inv(S.KV[i] * S.KV[j] * dkn * S.IK2) for i, j in tk]; n1, n2, n3 = S.eig3(tn); del tn
    vel = [S.inv(-(1j * kv) * (-dkn * S.IK2)) for kv in S.KV]
    sig = [-S.inv(1j * S.KV[i] * S.fwd(vel[j]) * nyq) for i, j in tk]; del vel
    v1, v2, v3 = S.eig3(sig); del sig
    rel = max(float(np.abs(v1 - n1).max()), float(np.abs(v2 - n2).max()), float(np.abs(v3 - n3).max())) / float(np.abs(n1).max())
    P(f"{foot}: D1 Nyquist-zeroed linear V-web vs Hessian eigenvalues: max rel diff {rel:.2e}")
    OUT[f"{foot}_D1"] = rel
    del n1, n2, n3, v1, v2, v3
    # D2
    base = rho * (onT & fil); Mf = float(base.sum())
    fAll, _ = S.turnaround_cover(delta)
    fRes = fT1 if MUT else cover_by_radius(delta, 2.0)
    fAll = fT1 if MUT else fAll
    self_ = delta >= (S.DTA0 - 1)
    cR = fRes > 0.5; cA = fAll > 0.5
    parts = {"local_delta>=Delta_ta-1": float(base[self_].sum()) / Mf,
             "covered_by_resolved_host(>=2 cells)": float(base[cR].sum()) / Mf,
             "covered_only_by_0-1_cell_balls": float(base[cA & ~cR].sum()) / Mf,
             "not_covered": float(base[~cA].sum()) / Mf,
             "resolved_cover_and_not_self": float(base[cR & ~self_].sum()) / Mf}
    P(f"  D2 T1-ON l3<0 mass split: " + "; ".join(f"{k} {v:.3f}" for k, v in parts.items()))
    OUT[f"{foot}_D2"] = parts
    # D3
    edges = [0, 5, 8, 10.8056, 15, 25, 50, 1e9]
    hist = [float(base[(rho >= a) & (rho < b)].sum()) / Mf for a, b in zip(edges[:-1], edges[1:])]
    P("  D3 T1-ON l3<0 mass by 1+delta: " + "; ".join(f"[{a:g},{b:g}) {v:.3f}" for a, b, v in zip(edges[:-1], edges[1:], hist)))
    OUT[f"{foot}_D3"] = dict(edges=edges, frac=hist)
json.dump(OUT, open(os.path.join(HERE, f"cfg412_diag_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg412_diag{SUF}.out"), "w").write("\n".join(L) + "\n")
