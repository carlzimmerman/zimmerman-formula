#!/usr/bin/env python3
"""AMENDMENT A2 validity diagnostic (reported only): is each crossing in a region where the frozen-F model holds?

ADIABATIC-REGION (model invalid): current equilibrium phantom rho_eq > 0 and omega_loc * T_f >= 1, with
omega_loc^2 = 4 pi G rho_eq (M_L - 1), M_L = (1+x)^2 and T_f = r/|rdot|.  SLOW-REGION otherwise.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.argv = [sys.argv[0]]
src = (HERE / "caustics.py").read_text()
ns = {"__file__": str(HERE / "caustics.py")}
exec(src[:src.index("# ================================================================ C0 solver check")], ns)
g_and_T, phantom, nu, null_x, mass_pos, integrate = (ns[k] for k in ("g_and_T", "phantom", "nu", "null_x", "mass_pos", "integrate"))
A0, ORBITS, t_end, G, EPS, T0, V0, rdot_O1 = (ns[k] for k in ("A0", "ORBITS", "t_end", "G", "EPS", "T0", "V0", "rdot_O1"))


def classify(X, t, a0, rfun, oname):
    r = rfun(t)
    rho = phantom(X, r, a0)
    gN, _ = g_and_T(X, r)
    y = np.linalg.norm(gN, axis=1) / a0
    x = nu(y) * y
    Tf = r / (abs(rdot_O1(t)) if oname.startswith("O1") else abs(V0))
    om = np.sqrt(np.maximum(4 * math.pi * G * rho * ((1 + x) ** 2 - 1), 0.0))
    adiab = (rho > 0) & (om * Tf >= 1)
    p1, p2 = mass_pos(r)
    d = np.minimum(np.linalg.norm(X - p1, axis=1), np.linalg.norm(X - p2, axis=1))
    return adiab, om * Tf, rho, d


rows = {}
xs_rel = np.arange(-400.0, 400.0 + 1e-9, 10.0)
zs = np.arange(0.0, 400.0 + 1e-9, 10.0)
for foot, a0 in A0.items():
    for oname, rfun in ORBITS.items():
        for ti in (3.0, 6.0, 9.0):
            ri = rfun(ti)
            xn = null_x(ri)
            Xg = np.array([[xn + dx, 0.0, z] for dx in xs_rel for z in zs])
            p1, p2 = mass_pos(ri)
            Xg = Xg[np.minimum(np.linalg.norm(Xg - p1, axis=1), np.linalg.norm(Xg - p2, axis=1)) > 2 * EPS]
            rho0 = phantom(Xg, ri, a0)
            soft = rho0 < 0
            Q = Xg[soft]
            gN, _ = g_and_T(Q, ri)
            yq = np.linalg.norm(gN, axis=1) / a0
            xq = nu(yq) * yq
            Gam2 = 4 * math.pi * G * np.abs(rho0[soft]) * ((1 + xq) ** 2 - 1)
            for s in (0, 1):
                tt, dets, XX, _ = integrate(Q, Gam2, rfun, ti, t_end[oname], s)
                N = Q.shape[0]
                # track classification every 25 grid steps
                slow_track = np.ones(N, bool)
                for it in range(0, len(tt), 25):
                    adiab, _, _, _ = classify(XX[it], tt[it], a0, rfun, oname)
                    slow_track &= ~adiab
                cross_idx = [int(np.argmax(dets[:, j] <= 0)) if (dets[:, j] <= 0).any() else None for j in range(N)]
                n_cross, n_cross_adiab, n_cross_slow, details = 0, 0, 0, []
                for j, ic in enumerate(cross_idx):
                    if ic is None:
                        continue
                    n_cross += 1
                    adiab, omT, rho_eq, dgal = classify(XX[ic][j:j + 1], tt[ic], a0, rfun, oname)
                    cls = "ADIABATIC" if adiab[0] else "SLOW"
                    n_cross_adiab += cls == "ADIABATIC"
                    n_cross_slow += cls == "SLOW"
                    details.append({"t_c": float(tt[ic]), "class": cls, "omega_Tf": float(omT[0]), "rho_eq": float(rho_eq[0]),
                                    "dist_gal_kpc": float(dgal[0])})
                st = slow_track
                det_slow = float(dets[:, st].min()) if st.any() else None
                t_slow = float(tt[np.unravel_index(np.argmin(dets[:, st]), dets[:, st].shape)[0]]) if st.any() else None
                key = f"{foot}|{oname}|t_i {ti}|s {s}"
                rows[key] = {"n_soft": N, "n_cross": n_cross, "n_cross_adiabatic": n_cross_adiab, "n_cross_slow": n_cross_slow,
                             "n_slow_track": int(st.sum()), "det_min_slow_track": det_slow, "t_det_min_slow_track": t_slow,
                             "first_crossings": sorted(details, key=lambda d_: d_["t_c"])[:5]}
                fc = rows[key]["first_crossings"]
                print(f"{key:48s} cross {n_cross:3d} (adiabatic {n_cross_adiab:3d}, slow {n_cross_slow:3d}); slow-track "
                      f"elements {int(st.sum()):3d}/{N}, their det_min {det_slow if det_slow is None else round(det_slow, 4)} at "
                      f"{t_slow if t_slow is None else round(t_slow, 3)} Gyr"
                      + (f"; first crossing {fc[0]['class']} at t {fc[0]['t_c']:.3f}, omega T_f {fc[0]['omega_Tf']:.2e}, "
                         f"{fc[0]['dist_gal_kpc']:.0f} kpc" if fc else ""))
(HERE / "caustics_validity.json").write_text(json.dumps(rows, indent=1))
slow_cross = {k: v for k, v in rows.items() if v["n_cross_slow"] > 0}
both = {}
for k, v in rows.items():
    base = k.rsplit("|s ", 1)[0]
    both.setdefault(base, []).append(v["n_cross_slow"] > 0)
both_slow = [b for b, l in both.items() if all(l)]
print(f"SUMMARY: runs with a SLOW-REGION crossing: {len(slow_cross)}/{len(rows)}; cases with SLOW crossings in both brackets: "
      f"{both_slow}; min det over slow-track elements: {min(v['det_min_slow_track'] for v in rows.values() if v['det_min_slow_track'] is not None):.4f}")
