#!/usr/bin/env python3
"""AMENDMENT A3 diagnostic (POST-RESULT, reported only, no verdict weight): what drives the soft threshold events?

Reruns one case self-consistently (same code path as x8_run.py) and follows the event label of runs/<tag>.json:
J = (R/R_q) x det2 split into the hoop factor (radial collapse onto the axis) and the in-plane determinant, its distance
to the nearer galaxy, its velocity, and the number of folded (J < 0) positive labels within 30 kpc of it.
Also reports, at the event time, the soft labels with J < 0.5 by label radius (is the compression confined to the axis?).

  python3 x8_mechanism.py --foot canonical --orbit O2 --ti 3 --h 10
"""
import argparse
import json
import math
import os
import sys
from pathlib import Path

if os.environ.get("MallocMediumZone") != "0":
    os.environ["MallocMediumZone"] = "0"
    os.execv(sys.executable, [sys.executable] + sys.argv)
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from x8_core import (A0, K, LSTAR, M1, M2, ORBITS, T_END, A_K, TK, MonoAQUAL, Sim, initial_state,  # noqa: E402
                     make_pair_grid, pair_positions, plummer_phi)

ap = argparse.ArgumentParser()
ap.add_argument("--foot", default="canonical")
ap.add_argument("--orbit", default="O2")
ap.add_argument("--ti", type=float, default=3.0)
ap.add_argument("--h", type=float, default=10.0)
a = ap.parse_args()
tag = f"{a.foot}_{a.orbit}_ti{int(a.ti)}_h{int(a.h)}"
ref = json.loads((HERE / "runs" / f"{tag}.json").read_text())
a0, gL = A0[a.foot], K * LSTAR[a.foot] ** 2 / 2
rfun, rdfun = ORBITS[a.orbit]
t_i, t_end = a.ti, T_END[a.orbit]
ts = np.linspace(t_i, t_end, 4001)
r_max = max(rfun(t) for t in ts)
if a.orbit == "O1" and t_i < math.pi * TK < t_end:
    r_max = max(r_max, 2 * A_K)
g = make_pair_grid(r_max, a.h)
RR, ZZ = np.meshgrid(g.R, g.z)
bm = np.ones_like(RR, bool)
bm[1:-1, :-1] = False
mono = MonoAQUAL(M1 + M2, a0)
XB = np.zeros_like(RR)
XB[bm] = mono(np.hypot(RR, ZZ)[bm])


def baryons(t):
    z1, z2 = pair_positions(rfun(t))
    return [(M1, z1), (M2, z2)]


def bc(t, phib):
    return XB, XB - phib


phib0 = plummer_phi(g.R, g.z, baryons(t_i))
Xi, m_node, rho, x, info = initial_state(g, a0, phib0, XB, gamma_L=gL)
dt0 = min(0.02, 0.15 / info["omega_max"])
sim = Sim(g, a0, gL, baryons, bc, Xi, m_node, t_i)
acc = sim.accel(t_i)
qR, qz = sim.q_R, sim.q_z
soft = m_node.ravel() < 0
pos = ~soft
NZi, NRi = g.NZ - 2, g.NR - 1
ev = ref["event"]
target = ev["label"] if ev else ref["S"]["label"]
k = int(np.argmin(np.hypot(qR - target[0], qz - target[1])))
jk, ik = divmod(k, NRi)
track = []
next_s = t_i
radial = None
t_stop = (ev["t"] + 0.3) if ev else t_end
while sim.t < t_stop:
    om = sim.omega_max()
    dt = min(dt0, 0.15 / om) if om > 0 else dt0
    acc = sim.step(dt, acc)
    if sim.t >= next_s:
        next_s += 0.05
        J = sim.J()
        Xr = sim.XR.reshape(NZi, NRi)
        Xz = sim.XZ.reshape(NZi, NRi)
        hoop = Xr[jk, ik] / qR[k]
        det2 = J[k] / hoop
        z1, z2 = pair_positions(rfun(sim.t))
        d1, d2 = math.hypot(sim.XR[k], sim.XZ[k] - z1), math.hypot(sim.XR[k], sim.XZ[k] - z2)
        near = np.hypot(sim.XR - sim.XR[k], sim.XZ - sim.XZ[k]) <= 30.0
        nfold = int((near & pos & (qR > 0) & (J < 0)).sum())
        nsoft_near = int((near & soft).sum())
        track.append({"t": round(float(sim.t), 3), "J": float(J[k]), "hoop_R_over_Rq": float(hoop), "det2": float(det2),
                      "R": float(sim.XR[k]), "z": float(sim.XZ[k]), "vR": float(sim.VR[k]), "vz": float(sim.VZ[k]),
                      "dist_MW": d1, "dist_M31": d2, "folded_positive_within_30kpc": nfold,
                      "soft_within_30kpc": nsoft_near})
        if ev and radial is None and sim.t >= ev["t"]:
            sv = soft & (qR > 0)
            radial = {}
            for Rlab in sorted(set(qR[sv & (np.abs(qz - target[1]) <= 3 * a.h)]))[:8]:
                sel = sv & (qR == Rlab) & (np.abs(qz - target[1]) <= 3 * a.h)
                radial[f"{Rlab:.0f}"] = float(J[sel].min())
out = {"tag": tag, "label": [float(qR[k]), float(qz[k])], "event_ref": ev, "track": track,
       "J_min_by_label_R_near_event_z_at_t_c": radial}
fn = HERE / f"x8_mechanism_{tag}.json"
fn.write_text(json.dumps(out, indent=1))
print(f"{tag}: label {out['label']}; event {ev['t'] if ev else None}")
for r in track[::max(1, len(track) // 30)] + track[-6:]:
    print(f"  t {r['t']:7.3f}  J {r['J']:+.4f} = hoop {r['hoop_R_over_Rq']:.4f} x det2 {r['det2']:+.4f}  pos ({r['R']:.1f}, "
          f"{r['z']:.1f})  v ({r['vR']:+.1f}, {r['vz']:+.1f})  d_MW {r['dist_MW']:.0f}  folded+ within 30 kpc "
          f"{r['folded_positive_within_30kpc']}  soft within 30 {r['soft_within_30kpc']}")
print("  J min by label R (soft, |z_q - z_label| <= 3h) at t_c:", radial)
