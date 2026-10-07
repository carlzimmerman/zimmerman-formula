#!/usr/bin/env python3
"""Post-hoc pre-check (labelled; supports the 10-07 supply-edge hypothesis, NOT a frozen test): per resolved PM host on CFG410 BASE z0 snapshots,
x_h = r_edge / r_ON with r_edge = (5.364 / f_ret) r_M(M_b,now), M_b,now = f_ret * f_b * M_ta, M_ta = (4pi/3) r_ON^3 Delta_ta rho_m (h units),
declared f_ret(M_ta): 0.10 below 10^12.5, log-linear to 0.55 at 10^13.5 and 0.85 at 10^14.5, capped 0.90 (group/cluster gas+stars fractions)."""
import os, sys, math, json
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "CFG412_filament_blind_switch"))
import cfg412_screen as S
from cfg415_doors import peaks_and_radii  # copied CFG413 machinery
G = 4.30091e-9; FB = 0.157; RHOM = 0.315 * 2.775e11; H = 0.674; DTA = 3 * S.TAU + 1
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
def fret(lM):
    if lM < 12.5: return 0.10
    if lM < 13.5: return 0.10 + (0.55 - 0.10) * (lM - 12.5)
    return min(0.55 + (0.85 - 0.55) * (lM - 13.5), 0.90)
OUT = {}
for foot in ("canonical", "alt"):
    snap = np.load(os.path.join(S.WORK, f"cfg410_RES_Rc3_MIXA_FLAT_{foot}_N256_z0.npz"))
    delta = S.deposit(snap["pos"].astype(np.float64)); pk, rad = peaks_and_radii(delta); rad = rad[rad >= 2.0]
    rON = rad * S.DX / H                                   # Mpc
    Mta = (4 * math.pi / 3) * (rad * S.DX) ** 3 * DTA * RHOM / H   # Msun
    a0c = A0[foot] * 3.0857e22 / 1e6
    fr = np.array([fret(math.log10(m * H)) for m in Mta])
    Mbn = fr * FB * Mta; rM = np.sqrt(G * Mbn / a0c); x = (5.364 / fr) * rM / rON
    lM = np.log10(Mta * H)
    rows = {}
    for lab, sel in (("10^13-13.5", (lM >= 13) & (lM < 13.5)), ("10^13.5-14.5", (lM >= 13.5) & (lM < 14.5)), (">=10^14.5", lM >= 14.5)):
        if sel.any(): rows[lab] = dict(n=int(sel.sum()), x_median=float(np.median(x[sel])), x16=float(np.percentile(x[sel], 16)), x84=float(np.percentile(x[sel], 84)))
    OUT[foot] = rows
    print(foot, {k: (v["n"], round(v["x_median"], 2), round(v["x16"], 2), round(v["x84"], 2)) for k, v in rows.items()})
json.dump(OUT, open(os.path.join(HERE, "precheck_supply_edge_hosts.json"), "w"), indent=1)
