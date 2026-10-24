#!/usr/bin/env python3
"""X12 R-X10 (FROZEN_CRITERIA §4): X10's 2D isolated-mass D-ISO runs reproduced with X10's code.

PROVENANCE: `single_run` is copied from rebuild_2026_10_22/X10_caustics_comoving/x10_validate.py (commit c13d9a15a6)
unchanged in every statistic X10 reports; X8's x8_core.py is imported read-only from X8's directory. Changes, and only these:
  * output goes to this lane's work/ (X10's directory is never written);
  * added (output only) the FROZEN §5a wake statistics over the X12 window [0, W_a], W_a = 9.067 Gyr (key `wake_Wa`), the
    2D reference of X-ISO.

  python3 x12_2d.py --mass MW --foot canonical|alt --h 20|10|5     -> work/x2d_iso_MW_<foot>_h<h>.json
"""
import argparse
import json
import os
import resource
import sys
import time
from pathlib import Path

import numpy as np

if os.environ.get("MallocMediumZone") != "0":           # X8 AMENDMENT A1
    os.environ["MallocMediumZone"] = "0"
    os.execv(sys.executable, [sys.executable] + sys.argv)
HERE = Path(__file__).resolve().parent
X8DIR = HERE.parent / "X8_soft_side_caustics"
sys.path.insert(0, str(X8DIR))
from x8_core import (A0, EPS, G, K, KMS, LSTAR, M1, M2, MonoAQUAL, Sim, initial_state, make_box_grid,  # noqa: E402
                     plummer_phi)

MUTATE = os.environ.get("X12_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
WORK = HERE / "work"
WORK.mkdir(exist_ok=True)
T_RUN = 18.067 + 0.1 - 3.0                               # X10: the longest production window (O2 t_i 3) incl. the tail
W_A = 18.067 - 9.0                                       # X12 FROZEN §2: the wake window
JCRIT, SUSTAIN = 0.05, 0.1
MASS = {"MW": M1, "M31": M2}
V_VCM = {"MW": 74.8, "M31": 44.9}
V_ISO = {"MW": 68.75, "M31": 41.25}
BOX = (500.0, -600.0, 1600.0)


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9


def single_run(mode, mass, foot, h):
    t_wall = time.time()
    a0 = A0[foot]
    gL = K * LSTAR[foot] ** 2 / 2
    M = MASS[mass]
    Vkms = (V_VCM if mode == "vcm" else V_ISO)[mass]
    V = Vkms * KMS
    grid = make_box_grid(BOX[0], BOX[1], BOX[2], h, 20000.0)
    R_f, z_lo, z_hi, hh = grid.fine
    RR, ZZ = np.meshgrid(grid.R, grid.z)
    bm = np.ones_like(RR, bool)
    bm[1:-1, :-1] = False
    mono = MonoAQUAL(M, a0)

    def zc(t):
        return V * t

    def baryons(t):
        return [(M, zc(t))]

    XB0 = np.zeros_like(RR)
    XB0[bm] = mono(np.hypot(RR, ZZ)[bm])

    def bc(t, phib):
        if mode == "vcm":
            Xb = np.zeros_like(RR)
            Xb[bm] = mono(np.hypot(RR, ZZ - zc(t))[bm])
        else:
            Xb = XB0
        return Xb, Xb - phib

    phib0 = plummer_phi(grid.R, grid.z, baryons(0.0))
    Xb0, _ = bc(0.0, phib0)
    Xi, m, rho, x, info = initial_state(grid, a0, phib0, Xb0, gamma_L=gL)
    dt0 = min(0.02, 0.15 / info["omega_max"])
    sim = Sim(grid, a0, gL, baryons, bc, Xi, m, 0.0, frozen=False)
    qR, qz = sim.q_R, sim.q_z
    sgn = -1.0 if MUTATE else 1.0
    if mode == "vcm":
        cls = np.ones(qR.size, dtype=np.int8)
    else:
        e = 0.5 * V ** 2 - G * M / np.sqrt(qR ** 2 + qz ** 2 + EPS ** 2)
        cls = (e < 0).astype(np.int8)
    sim.VZ = np.where(cls == 1, sgn * V, 0.0)
    sh = (grid.NZ - 2, grid.NR - 1)
    C = cls.reshape(sh)
    stc = np.zeros(sh, bool)
    d_ = C[:, 1:] != C[:, :-1]
    stc[:, 1:] |= d_
    stc[:, :-1] |= d_
    d_ = C[1:, :] != C[:-1, :]
    stc[1:, :] |= d_
    stc[:-1, :] |= d_
    straddle = stc.ravel()
    nstr = ~straddle
    soft = m.ravel() < 0
    acc = sim.accel(0.0)
    lab = (qR > 0) & (qR <= R_f - 2 * hh) & (qz >= z_lo + 2 * hh) & (qz <= z_hi - 2 * hh)
    dq = np.hypot(qR, qz)
    sel_out = lab & (dq >= 2 * EPS) & (dq <= 300.0)
    sel_in = lab & (dq < 2 * EPS)
    mx_out = mx_in = mx_all = disp_out = disp_all = 0.0
    t_mx_out = 0.0
    wake = {s_: {"min": None, "event": None, "first_below": None} for s_ in ("down", "up")}
    wst = {s_: np.full(qR.size, np.nan) for s_ in ("down", "up")}
    # X12 addition (output only): the same statistics over [0, W_A]
    wakeW = {s_: {"min": None, "event": None, "first_below": None} for s_ in ("down", "up")}
    wstW = {s_: np.full(qR.size, np.nan) for s_ in ("down", "up")}
    edge = None
    stiff = None
    series = []
    next_series = 0.0

    def recd(J, k, t):
        return {"J": float(J[k]), "t": float(t), "label": [float(qR[k]), float(qz[k])],
                "pos": [float(sim.XR[k]), float(sim.XZ[k])], "dz_from_mass": float(sim.XZ[k] - zc(t)),
                "start_class": int(cls[k])}

    def track(J, t, zf, s_, store, stw, t_last):
        belowg = J < JCRIT
        stw[~belowg] = np.nan
        if t <= t_last + 1e-9:
            stw[belowg & np.isnan(stw) & zf] = t
        conf = belowg & ~np.isnan(stw) & (t - stw >= SUSTAIN - 1e-9) & (stw <= t_last + 1e-9)
        if conf.any() and store[s_]["event"] is None:
            k = int(np.flatnonzero(conf)[np.argmin(stw[conf])])
            store[s_]["event"] = dict(recd(J, k, stw[k]), confirmed_at=float(t))
        if zf.any() and t <= t_last + 1e-9:
            k = int(np.flatnonzero(zf)[np.argmin(J[zf])])
            if store[s_]["min"] is None or J[k] < store[s_]["min"]["J"]:
                store[s_]["min"] = recd(J, k, t)
            if J[k] < JCRIT and store[s_]["first_below"] is None:
                store[s_]["first_below"] = recd(J, k, t)

    def sample(t):
        nonlocal mx_out, mx_in, mx_all, disp_out, disp_all, t_mx_out, edge, stiff, next_series
        J = sim.J()
        dJ = np.abs(J - 1)
        v = float(dJ[sel_out].max())
        if v > mx_out:
            mx_out, t_mx_out = v, t
        mx_in = max(mx_in, float(dJ[sel_in].max()))
        mx_all = max(mx_all, float(dJ[qR > 0].max()))
        d = np.hypot(sim.XR - qR, sim.XZ - qz - (V * t if mode == "vcm" else 0.0))
        disp_out = max(disp_out, float(d[sel_out].max()))
        disp_all = max(disp_all, float(d[qR > 0].max()))
        XR, XZ = sim.XR, sim.XZ
        pos_valid = (XR <= R_f - 2 * hh) & (XZ >= z_lo + 2 * hh) & (XZ <= z_hi - 2 * hh)
        zg = zc(t)
        ax = (XR <= 30.0) & pos_valid & (qR > 0) & (~soft) & nstr
        for s_ in ("down", "up"):
            side = ((XZ <= zg - 2 * EPS) & (XZ >= zg - 1000.0)) if s_ == "down" else (
                (XZ >= zg + 2 * EPS) & (XZ <= zg + 1000.0))
            zf = ax & side
            track(J, t, zf, s_, wake, wst[s_], T_RUN - 0.1)       # X10's statistic, unchanged
            track(J, t, zf, s_, wakeW, wstW[s_], W_A)             # X12 addition
        ed = straddle & (qR > 0) & pos_valid
        if ed.any():
            k = int(np.flatnonzero(ed)[np.argmin(J[ed])])
            if edge is None or J[k] < edge["J"]:
                edge = recd(J, k, t)
        sf = lab & pos_valid & nstr & (~soft)
        if sf.any():
            k = int(np.flatnonzero(sf)[np.argmin(J[sf])])
            if stiff is None or J[k] < stiff["J"]:
                stiff = recd(J, k, t)
        if t >= next_series - 1e-9:
            series.append({"t": round(float(t), 3), "absJm1_out_now": v,
                           "wake_down_now": float(J[ax & (XZ <= zg - 2 * EPS) & (XZ >= zg - 1000.0)].min())
                           if (ax & (XZ <= zg - 2 * EPS) & (XZ >= zg - 1000.0)).any() else None,
                           "wake_up_now": float(J[ax & (XZ >= zg + 2 * EPS) & (XZ <= zg + 1000.0)].min())
                           if (ax & (XZ >= zg + 2 * EPS) & (XZ <= zg + 1000.0)).any() else None,
                           "iters_per_call": sim.iters_total / max(sim.ncalls, 1)})
            next_series += 0.5

    sample(0.0)
    next_sample, F4, dt_min = 0.02, None, dt0
    steps = 0
    while sim.t < T_RUN - 1e-12:
        om = sim.omega_max()
        dt = min(dt0, 0.15 / om) if om > 0 else dt0
        if dt < dt0 / 50.0:
            dt = dt0 / 50.0
            if F4 is None:
                F4 = sim.t
        dt = min(dt, T_RUN - sim.t + 1e-12)
        dt_min = min(dt_min, dt)
        acc = sim.step(dt, acc)
        steps += 1
        if sim.t >= next_sample - 1e-9 or sim.t >= T_RUN - 1e-12:
            sample(sim.t)
            next_sample += 0.02
        if time.time() - t_wall > 27 * 60:
            print("wall guard reached; this single-mass run is not checkpointed", flush=True)
            sys.exit(3)
    return {"mode": mode, "mass": mass, "M": M, "foot": foot, "h": h, "V_kms": Vkms, "boost_sign": sgn, "T_run": T_RUN,
            "dt0": dt0, "dt_min": dt_min, "steps": steps, "F4": F4, "flags": sim.flags, "omega_max": info["omega_max"],
            "aqual_rel_residual": info["rel_residual"], "n_interior": grid.nint, "n_held": int((cls == 1).sum()),
            "held_radius_max": float(dq[cls == 1].max()) if (cls == 1).any() else None,
            "rcap": 2 * G * M / V ** 2, "n_straddle": int(straddle.sum()),
            "max_absJm1_outside_2eps_le300": mx_out, "t_of_max_outside": t_mx_out, "max_absJm1_inside_2eps": mx_in,
            "max_absJm1_all": mx_all, "max_comoving_disp_outside": disp_out, "max_comoving_disp_all": disp_all,
            "wake": wake, "wake_Wa": wakeW, "W_a": W_A, "D_EDGE": edge, "D_STIFF": stiff, "series": series,
            "hold_iters_per_call": sim.iters_total / max(sim.ncalls, 1), "xmax_seen": sim.xmax_seen,
            "wall_s": time.time() - t_wall, "rss_GB": rss()}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mass", default="MW", choices=["MW", "M31"])
    ap.add_argument("--foot", required=True, choices=["canonical", "alt"])
    ap.add_argument("--h", type=float, required=True)
    a = ap.parse_args()
    res = single_run("iso", a.mass, a.foot, a.h)
    f = WORK / f"x2d_iso_{a.mass}_{a.foot}_h{int(a.h)}{SUF}.json"
    f.write_text(json.dumps(res, indent=1, default=float))
    w = res["wake"]
    print(f"{f.name}: down event {w['down']['event']['t'] if w['down']['event'] else None}; up min "
          f"{w['up']['min']['J'] if w['up']['min'] else None}; W_a: down event "
          f"{res['wake_Wa']['down']['event']['t'] if res['wake_Wa']['down']['event'] else None} up min "
          f"{res['wake_Wa']['up']['min']['J'] if res['wake_Wa']['up']['min'] else None}; {res['wall_s']:.0f} s, "
          f"{res['rss_GB']:.2f} GB", flush=True)
