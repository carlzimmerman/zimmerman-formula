#!/usr/bin/env python3
"""CFG413 growth leg: share of the RES excess source (T1-weighted) lying beyond x * r_ta of every resolved peak,
on CFG410's BASE z0 snapshots, with CFG412's turnaround-sphere machinery (cfg412_screen imported read-only).
Criteria: FROZEN_CRITERIA.md.  ESTIMATE only; no PM run.  One process, one FFT thread, nice 15.
Usage: nice -n 15 python3 cfg413_growth.py ;  CFG413_MUTATE=1 ... (adds x = 0.05; separate outputs)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time
import numpy as np
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG412_filament_blind_switch"))
import cfg412_screen as S                                                   # read-only import (no main run)

MUTATE = os.environ.get("CFG413_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
try:
    os.nice(15)
except OSError:
    pass
XS = [0.23, 0.3, 0.4, 0.5, 0.7, 1.0]
if MUTATE:
    XS = [0.05] + XS
RMINS = (2.0, 1.0, 3.0)                     # resolved threshold in cells: 2 = frozen (CFG412-D2), 1 and 3 reported only
D2_REF = {"canonical": 0.805, "alt": 0.811}  # CFG412-D2 covered_by_resolved_host(>=2 cells)
M = S.M
LOG, CHK = [], {}
def P(s=""):
    print(s, flush=True); LOG.append(s)
def check(name, ok, msg):
    CHK[name] = bool(ok); P("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, msg))
T0 = time.time()

def peaks_and_radii(delta):
    """CFG412 turnaround-cover peaks; returns centres and first-crossing ON radius (cells) of each."""
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

_BALL = {}
def ball(R):
    key = round(R, 6)
    if key not in _BALL:
        n = int(math.floor(R + 1e-9)); g = np.arange(-n, n + 1)
        r2 = g[:, None, None] ** 2 + g[None, :, None] ** 2 + g[None, None, :] ** 2
        sel = np.argwhere(r2 <= R * R + 1e-9) - n
        _BALL[key] = sel
    return _BALL[key]

def in_mask(pk, rad, x, rmin):
    m = np.zeros(M ** 3, bool)
    for c, r in zip(pk[rad >= rmin], rad[rad >= rmin]):
        off = ball(x * r); p = (c[None, :] + off) % M
        m[(p[:, 0] * M + p[:, 1]) * M + p[:, 2]] = True
    return m.reshape((M,) * 3)

OUT = dict(mutate=MUTATE, xs=XS, rmins=RMINS)
for foot in ("canonical", "alt"):
    t0 = time.time()
    snap = np.load(os.path.join(S.WORK, f"cfg410_RES_Rc3_MIXA_FLAT_{foot}_N256_z0.npz"))
    delta = S.deposit(snap["pos"].astype(np.float64)); f_st = snap["f"].astype(np.float32); rho = 1.0 + delta
    dk = S.fwd(delta)
    tk = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    t = [S.inv(S.KV[i] * S.KV[j] * dk * S.IK2) for i, j in tk]
    l1, l2, l3 = S.eig3(t); del t, l1
    fT1 = S.smear(l2); del l2
    agree = float(np.mean((fT1 > 0.5) == (f_st > 0.5)))
    check(f"K5 {foot}: re-computed T1 agrees with stored f", agree >= 0.995, f"{agree:.5f}")
    fil = l3 < 0; del l3
    onT = fT1 > 0.5
    # RES excess source, exactly CFG412 pm_leg (copied)
    phik = (-1.5 * S.Om) * dk * S.IK2
    kJ = lambda T: math.sqrt(1.5 * S.Om) * 100.0 / (math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3)
    Wk = (S.MIXA[0] / (1.0 + S.K2 / kJ(1e4) ** 2) + S.MIXA[1] / (1.0 + S.K2 / kJ(1e6) ** 2) + S.MIXA[2]).astype(np.float32)
    gb = [S.FB * (-S.inv(1j * kv * phik * Wk)) for kv in S.KV]; del Wk, phik
    y = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / (S.A0[foot] / S.ACC_UNIT)
    w = (S.nu_mono(y) - 1.0).astype(np.float32); del y
    divk = sum(1j * kv * S.fwd(w * g) for kv, g in zip(S.KV, gb)); del gb, w
    s_ph = -S.inv(divk); del divk
    s_c = (1.5 * S.Om * (1.0 - S.FB)) * rho
    exc = np.maximum(s_ph - s_c, 0.0).astype(np.float32); del s_ph, s_c, dk
    E = fT1 * exc; Etot = float(E.sum()); Efil = float((E * fil).sum())
    Mfil = rho * (onT & fil); Mf = float(Mfil.sum()); Mon = rho * onT; Mo = float(Mon.sum())
    pk, rad = peaks_and_radii(delta)
    P(f"\n[{foot}] peaks {len(pk)}; resolved (>=2 cells) {int((rad >= 2).sum())}, >=1 {int((rad >= 1).sum())}, >=3 {int((rad >= 3).sum())}; "
      f"ON radius of resolved peaks median {np.median(rad[rad >= 2]) * S.DX:.2f} Mpc/h, max {rad.max() * S.DX:.2f}; "
      f"l3<0 share of T1-weighted excess {Efil / Etot:.3f}  ({time.time() - t0:.0f} s)")
    res = {}
    for rmin in RMINS:
        rows = {}
        for x in XS:
            IN = in_mask(pk, rad, x, rmin); B = ~IN
            S_ = float((E * B).sum()) / Etot
            Sf = float((E * (fil & B)).sum()) / Efil
            rows[str(x)] = dict(S=S_, S_fil=Sf, Xhat=S.X_CFG410[foot] * Sf,
                                mass_on_beyond=float(Mon[B].sum()) / Mo, mass_fil_inside=float(Mfil[IN].sum()) / Mf,
                                vol_in=float(IN.mean()))
        res[str(rmin)] = rows
        P(f"  resolved >= {rmin:g} cells" + ("  (FROZEN)" if rmin == 2.0 else "  (reported only)"))
        P("     x    | S(x) excess beyond | S_fil  | Xhat (est.) | T1-ON mass beyond | volume IN")
        for x in XS:
            r = rows[str(x)]
            P(f"    {x:5.2f} | {r['S']:8.3f}           | {r['S_fil']:6.3f} | {r['Xhat']:7.3f}     | {r['mass_on_beyond']:8.3f}          | {r['vol_in']:.4f}")
    OUT[foot] = dict(n_peaks=int(len(pk)), n_resolved=int((rad >= 2).sum()), excess_fil_share=Efil / Etot, K5=agree, rows=res)
    fr = res["2.0"]
    k3 = abs(fr["1.0"]["mass_fil_inside"] - D2_REF[foot])
    check(f"K3 {foot}: x=1 T1-ON l3<0 mass inside resolved balls vs CFG412-D2 {D2_REF[foot]}", k3 <= 0.01,
          f"{fr['1.0']['mass_fil_inside']:.4f} (|diff| {k3:.4f})")
    mono = all(np.all(np.diff([res[str(rm)][str(x)][q] for x in XS]) <= 1e-12) for rm in RMINS for q in ("S", "S_fil"))
    check(f"K4 {foot}: S(x), S_fil(x) non-increasing in x", mono, "")
    del delta, rho, fT1, exc, E, fil, onT, Mfil, Mon
OUT["checks"] = CHK
P(f"\nchecks {CHK}; elapsed {time.time() - T0:.0f} s")
json.dump(OUT, open(os.path.join(HERE, f"cfg413_growth_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg413_growth{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
