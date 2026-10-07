#!/usr/bin/env python3
"""CFG415 -- door 1 (shared turnaround catchments; groups vs clusters) and door 2 (sqrt(M_b) tracking = BTFR slope 4 on SPARC).
Frozen: FROZEN_CRITERIA.md.  Light CPU (1 thread, nice 15).  CFG415_MUTATE=1 -> shuffled host masses / M_b x V^2 (separate outputs)."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math
import numpy as np
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG412_filament_blind_switch"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "sonnet55_push", "puzzle_32pi", "agents", "V_evidence_for_the_coefficient"))
import cfg412_screen as S
from v_common import load_sparc
try:
    os.nice(15)
except OSError:
    pass
MUT = os.environ.get("CFG415_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
rng = np.random.default_rng(415)
LOG, OUT = [], {"mutate": MUT}
def P(s=""): print(s, flush=True); LOG.append(s)
M = S.M; DX = S.DX; DTA = 3 * S.TAU + 1; RHOM = 0.315 * 2.775e11

def peaks_and_radii(delta):                       # copied from CFG413 (cfg413_growth.py), unchanged
    mx = ndimage.maximum_filter(delta, size=3, mode="wrap")
    pk = np.argwhere((delta == mx) & (delta >= 3 * (S.TAU - S.EPS)))
    rad = np.zeros(len(pk))
    for n, c in enumerate(pk):
        hw = 3
        while True:
            g, order, r2s, last, grp = S.geom(hw)
            ix, iy, iz = (c[0] + g) % M, (c[1] + g) % M, (c[2] + g) % M
            idx = ((ix[:, None, None] * M + iy[None, :, None]) * M + iz[None, None, :]).ravel()
            ds = delta.ravel()[idx][order].astype(np.float64)
            cum = np.cumsum(ds)[last]; nn = last + 1
            F = np.minimum.accumulate(S.smear(((1.0 + cum / nn) - 1.0) / 3.0))
            inside = r2s[last] <= hw * hw
            if F[inside][-1] > 0 and hw < 40:
                hw *= 2; continue
            break
        on = inside & (F > 0.5)
        rad[n] = math.sqrt(r2s[last][on][-1]) if on.any() else 0.0
    return pk, rad

_B = {}
def ball(R):
    k = round(R, 6)
    if k not in _B:
        n = int(math.floor(R + 1e-9)); g = np.arange(-n, n + 1)
        r2 = g[:, None, None] ** 2 + g[None, :, None] ** 2 + g[None, None, :] ** 2
        _B[k] = np.argwhere(r2 <= R * R + 1e-9) - n
    return _B[k]

P(f"CFG415{' MUTATE' if MUT else ''} -- door 1: shared turnaround catchments (Delta_ta {DTA:.3f}, mesh {DX:.3f} Mpc/h)")
for foot in ("canonical", "alt"):
    snap = np.load(os.path.join(S.WORK, f"cfg410_RES_Rc3_MIXA_FLAT_{foot}_N256_z0.npz"))
    delta = S.deposit(snap["pos"].astype(np.float64)); rho = (1.0 + delta).ravel()
    pk, rad = peaks_and_radii(delta)
    res = rad >= 2.0; pk, rad = pk[res], rad[res]
    cells = [((c[None, :] + ball(r)) % M) for c, r in zip(pk, rad)]
    flat = [(p[:, 0] * M + p[:, 1]) * M + p[:, 2] for p in cells]
    cnt = np.zeros(M ** 3, np.int16)
    for f in flat:
        cnt[np.unique(f)] += 1
    s = np.array([float((rho[np.unique(f)] * (cnt[np.unique(f)] >= 2)).sum() / rho[np.unique(f)].sum()) for f in flat])
    Mta = (4 * math.pi / 3) * (rad * DX) ** 3 * DTA * RHOM
    if MUT:
        Mta = rng.permutation(Mta)
    gsel = (Mta >= 10 ** 13.5) & (Mta < 10 ** 14.5); csel = Mta >= 10 ** 14.5
    sg, sc = float(np.median(s[gsel])) if gsel.any() else float("nan"), float(np.median(s[csel])) if csel.any() else float("nan")
    OUT[foot] = dict(n_hosts=int(len(s)), n_group=int(gsel.sum()), n_cluster=int(csel.sum()), s_group=sg, s_cluster=sc,
                     s_group_mean=float(s[gsel].mean()) if gsel.any() else None, s_cluster_mean=float(s[csel].mean()) if csel.any() else None)
    P(f"  {foot:9s}: resolved hosts {len(s)} (group-like {gsel.sum()}, cluster-like {csel.sum()}); median shared fraction: groups {sg:.3f}, clusters {sc:.3f}")
v1 = all(OUT[f]["s_group"] >= OUT[f]["s_cluster"] for f in ("canonical", "alt"))
OUT["door1"] = "CONSISTENT" if v1 else "INCONSISTENT"
P(f"  door 1 verdict: {OUT['door1']} (groups vs clusters ordering; the mechanism is a reading, not established by a pass)")

P("\ndoor 2: sqrt(M_b) tracking = BTFR slope (SPARC Q<=2; M_b(<R_last) = V_bar^2 R/G with Upsilon 0.5/0.7)")
G, MSUN = 6.674e-11, 1.989e30
lv, lm = [], []
for g in load_sparc():
    if g.get("Q") is None or g["Q"] > 2 or len(g["Vobs"]) < 5:
        continue
    v3 = g["Vobs"][-3:]
    if v3.max() / v3.min() > 1.05:
        continue
    vb2 = (g["Vgas"][-1] * abs(g["Vgas"][-1]) + 0.5 * g["Vdisk"][-1] ** 2 + 0.7 * g["Vbul"][-1] ** 2) * 1e6
    if vb2 <= 0:
        continue
    Mb = vb2 * g["Rm"][-1] / G / MSUN; V = float(np.median(v3))
    if MUT:
        Mb *= V ** 2
    lv.append(math.log10(V)); lm.append(math.log10(Mb))
lv, lm = np.array(lv), np.array(lm)
slope = float(np.polyfit(lv, lm, 1)[0])
bs = [np.polyfit(lv[i], lm[i], 1)[0] for i in (rng.integers(0, len(lv), len(lv)) for _ in range(2000))]
err = float(np.std(bs))
OUT["door2"] = dict(N=int(len(lv)), slope=slope, err=err, verdict="CONSISTENT" if abs(slope - 4) <= 2 * err else "INCONSISTENT")
P(f"  N {len(lv)} flat-curve galaxies: log M_b vs log V_flat slope = {slope:.2f} +- {err:.2f} -> {OUT['door2']['verdict']} (4 = sqrt(M_b) tracking)")
open(os.path.join(HERE, f"cfg415_doors{SUF}.out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, f"cfg415_doors{SUF}.json"), "w"), indent=1)
