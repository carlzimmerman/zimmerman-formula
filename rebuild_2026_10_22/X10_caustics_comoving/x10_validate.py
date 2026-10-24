#!/usr/bin/env python3
"""X10 validation (FROZEN_CRITERIA §4) and the D-ISO diagnostic (§6).

  python3 x10_validate.py --single vcm|iso --mass MW|M31 --foot canonical|alt --h 20|10|5
        -> work/single_<mode>_<mass>_<foot>_h<h>[_MUTATE].json   (one single-mass run)
  python3 x10_validate.py --collect
        -> x10_validate[_MUTATE].out, x10_validate_results[_MUTATE].json   (R-X8a, R-X8b, V-cm, D-ISO)

vcm: the mass's full v3s switched static equilibrium boosted to +V (X10_MUTATE=1: -V, the wrong sign), Dirichlet data
     following the mass (X8 V-a2's set-up), run 15.167 Gyr with the production integrator (adaptive dt, floor flag F4).
iso: the FROZEN §2 rule for one galaxy (held iff e < 0, boosted; the rest at rest), Dirichlet data fixed about the start.
The single-mass driver follows X8's x8_validate.single_mass_run (commit 72515e7e75); x8_core is imported read-only.
"""
import argparse
import json
import math
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

MUTATE = os.environ.get("X10_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
WORK = HERE / "work"
WORK.mkdir(exist_ok=True)
T_RUN = 18.067 + 0.1 - 3.0                               # the longest production window (O2 t_i 3) incl. the tail
JCRIT, SUSTAIN = 0.05, 0.1
MASS = {"MW": M1, "M31": M2}
V_VCM = {"MW": 74.8, "M31": 44.9}                        # km/s: the largest production boost per galaxy (O1 t_i 3)
V_ISO = {"MW": 68.75, "M31": 41.25}                      # km/s: the O2 speeds
BOX = (500.0, -600.0, 1600.0)                            # fine zone R <= 500, z in [-600, 1600] kpc


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
        if mode == "vcm":                                # the data follow the mass (X8 V-a2)
            Xb = np.zeros_like(RR)
            Xb[bm] = mono(np.hypot(RR, ZZ - zc(t))[bm])
        else:                                            # iso: the far khronon is at rest, data fixed about the start
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
    lab = (qR > 0) & (qR <= R_f - 2 * hh) & (qz >= z_lo + 2 * hh) & (qz <= z_hi - 2 * hh)   # axis excluded (A1)
    dq = np.hypot(qR, qz)
    sel_out = lab & (dq >= 2 * EPS) & (dq <= 300.0)
    sel_in = lab & (dq < 2 * EPS)
    mx_out = mx_in = mx_all = disp_out = disp_all = 0.0
    t_mx_out = 0.0
    wake = {s_: {"min": None, "event": None, "first_below": None} for s_ in ("down", "up")}
    wst = {s_: np.full(qR.size, np.nan) for s_ in ("down", "up")}
    edge = None
    stiff = None
    series = []
    next_series = 0.0

    def recd(J, k, t):
        return {"J": float(J[k]), "t": float(t), "label": [float(qR[k]), float(qz[k])],
                "pos": [float(sim.XR[k]), float(sim.XZ[k])], "dz_from_mass": float(sim.XZ[k] - zc(t)),
                "start_class": int(cls[k])}

    def sample(t):
        nonlocal mx_out, mx_in, mx_all, disp_out, disp_all, t_mx_out, edge, stiff, next_series
        J = sim.J()
        dJ = np.abs(J - 1)
        v = float(dJ[sel_out].max())
        if v > mx_out:
            mx_out, t_mx_out = v, t
        mx_in = max(mx_in, float(dJ[sel_in].max()))
        mx_all = max(mx_all, float(dJ[qR > 0].max()))
        d = np.hypot(sim.XR - qR, sim.XZ - qz - (V * t if mode == "vcm" else 0.0))      # in the mass's frame
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
            belowg = J < JCRIT
            stw = wst[s_]
            stw[~belowg] = np.nan
            if t <= T_RUN - 0.1 + 1e-9:
                stw[belowg & np.isnan(stw) & zf] = t
            conf = belowg & ~np.isnan(stw) & (t - stw >= SUSTAIN - 1e-9) & (stw <= T_RUN - 0.1 + 1e-9)
            if conf.any() and wake[s_]["event"] is None:
                k = int(np.flatnonzero(conf)[np.argmin(stw[conf])])
                wake[s_]["event"] = dict(recd(J, k, stw[k]), confirmed_at=float(t))
            if zf.any() and t <= T_RUN - 0.1 + 1e-9:
                k = int(np.flatnonzero(zf)[np.argmin(J[zf])])
                if wake[s_]["min"] is None or J[k] < wake[s_]["min"]["J"]:
                    wake[s_]["min"] = recd(J, k, t)
                if J[k] < JCRIT and wake[s_]["first_below"] is None:
                    wake[s_]["first_below"] = recd(J, k, t)
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
            "wake": wake, "D_EDGE": edge, "D_STIFF": stiff, "series": series,
            "hold_iters_per_call": sim.iters_total / max(sim.ncalls, 1), "xmax_seen": sim.xmax_seen,
            "wall_s": time.time() - t_wall, "rss_GB": rss()}


def cell_class(r10, r5, t_i=0.0):
    """FROZEN §5b per-cell rule on two runs' wake dicts (h 10, h 5)."""
    e10, e5 = r10["down"]["event"], r5["down"]["event"]
    u10 = r10["up"]["min"]["J"] if r10["up"]["min"] else None
    u5 = r5["up"]["min"]["J"] if r5["up"]["min"] else None
    d10 = r10["down"]["min"]["J"] if r10["down"]["min"] else None
    d5 = r5["down"]["min"]["J"] if r5["down"]["min"] else None
    if e10 is not None and e5 is not None:
        tol = max(0.5, 0.1 * (e5["t"] - t_i))
        conv = abs(e5["t"] - e10["t"]) <= tol
        up_ok = (u10 is None or u10 > 0.5) and (u5 is None or u5 > 0.5)
        if conv and up_ok:
            return "PRESENT", f"t_c {e10['t']:.3f} / {e5['t']:.3f}; J_up {u10} / {u5}"
        if not up_ok:
            return "UNDECIDED", f"NOT SINGLED OUT: t_c {e10['t']:.3f} / {e5['t']:.3f}; J_up {u10} / {u5}"
        return "UNDECIDED", f"NOT CONVERGED: t_c {e10['t']:.3f} / {e5['t']:.3f}"
    if e10 is None and e5 is None and d10 is not None and d5 is not None and d5 >= JCRIT and d10 >= JCRIT \
            and abs(d5 - d10) <= 0.05:
        return "ABSENT", f"J_down {d10:.4f} / {d5:.4f}"
    return "UNDECIDED", f"NOT CONVERGED: events {e10 is not None} / {e5 is not None}; J_down {d10} / {d5}"


ap = argparse.ArgumentParser()
ap.add_argument("--single", choices=["vcm", "iso"])
ap.add_argument("--mass", choices=["MW", "M31"])
ap.add_argument("--foot", choices=["canonical", "alt"])
ap.add_argument("--h", type=float)
ap.add_argument("--collect", action="store_true")
a = ap.parse_args()

if a.single:
    res = single_run(a.single, a.mass, a.foot, a.h)
    f = WORK / f"single_{a.single}_{a.mass}_{a.foot}_h{int(a.h)}{SUF}.json"
    f.write_text(json.dumps(res, indent=1, default=float))
    print(f"{f.name}: max|J-1| outside {res['max_absJm1_outside_2eps_le300']:.4e} (t {res['t_of_max_outside']:.2f}), "
          f"inside {res['max_absJm1_inside_2eps']:.3e}; disp {res['max_comoving_disp_outside']:.3e} kpc; wake down "
          f"{res['wake']['down']['min']['J'] if res['wake']['down']['min'] else None} up "
          f"{res['wake']['up']['min']['J'] if res['wake']['up']['min'] else None}; {res['wall_s']:.0f} s, "
          f"{res['rss_GB']:.2f} GB", flush=True)

if a.collect:
    lines, out = [], {"mutate_wrong_sign": MUTATE}
    TOL = 1e-9

    def say(s=""):
        print(s)
        lines.append(s)

    def fields(r):
        g = lambda d, k: (d[k] if d else None)                                   # noqa: E731
        return {"S.J": g(r["S"], "J"), "S_by_t0.J": g(r["S_by_t0"], "J"), "event.t": g(r["event"], "t"),
                "first_fold.t": g(r["first_fold"], "t"), "D_STIFF.J": g(r["D_STIFF"], "J"),
                "D_STIFF.t": g(r["D_STIFF"], "t"), "n_event_elements_max": r["n_event_elements_max"]}

    def compare(mine, ref):
        rows, ok = {}, True
        for k, v in fields(ref).items():
            w = fields(mine)[k]
            if v is None or w is None:
                good = v is None and w is None
                diff = None
            else:
                diff = abs(w - v)
                good = diff <= TOL * max(1.0, abs(v))
            ok &= good
            rows[k] = {"x8": v, "here": w, "abs_diff": diff, "ok": good}
        return ok, rows

    checks = []
    if not MUTATE:
        for cid, base in (("R-X8a", HERE / "work" / "x8repro" / "runs"), ("R-X8b", HERE / "runs")):
            allok, detail = True, {}
            for tg in ("canonical_O2_ti3_h10", "canonical_O1_ti9_h10"):
                ref = json.loads((X8DIR / "runs" / f"{tg}.json").read_text())
                fn = base / (f"{tg}.json" if cid == "R-X8a" else f"{tg}_rest.json")
                if not fn.exists():
                    allok, detail[tg] = False, "missing"
                    continue
                ok, rows = compare(json.loads(fn.read_text()), ref)
                allok &= ok
                detail[tg] = rows
            checks.append({"check": cid, "pass": bool(allok), "detail": detail})
            say(f"{cid:6s} {'PASS' if allok else 'FAIL'}  X8's committed runs json reproduced "
                f"({'X8 x8_run.py, X8_OUT redirected' if cid == 'R-X8a' else 'x10_run.py --start rest'}), tol 1e-9 rel")
            for tg, rows in detail.items():
                if rows == "missing":
                    say(f"       {tg}: missing")
                    continue
                say(f"       {tg}: " + "; ".join(f"{k} {r['here']} (diff {r['abs_diff']})" for k, r in rows.items()))
    # V-cm
    vrows, vok = [], True
    for mass in ("MW", "M31"):
        for foot in ("canonical", "alt"):
            rr = {}
            for h in (20, 10, 5):
                f = WORK / f"single_vcm_{mass}_{foot}_h{h}{SUF}.json"
                rr[h] = json.loads(f.read_text()) if f.exists() else None
            if rr[10] is None or rr[5] is None:
                vok = False
                vrows.append({"mass": mass, "foot": foot, "missing": True})
                continue
            v10, v5 = rr[10]["max_absJm1_outside_2eps_le300"], rr[5]["max_absJm1_outside_2eps_le300"]
            ok = v10 <= 0.1 and v5 <= 0.1 and v5 <= v10
            vok &= ok
            row = {"mass": mass, "foot": foot, "V_kms": rr[10]["V_kms"], "pass": ok,
                   "max_absJm1_outside": {h: (rr[h]["max_absJm1_outside_2eps_le300"] if rr[h] else None) for h in rr},
                   "max_absJm1_inside_2eps": {h: (rr[h]["max_absJm1_inside_2eps"] if rr[h] else None) for h in rr},
                   "max_comoving_disp_outside": {h: (rr[h]["max_comoving_disp_outside"] if rr[h] else None) for h in rr},
                   "flags": {h: (dict(rr[h]["flags"], F4=rr[h]["F4"]) if rr[h] else None) for h in rr}}
            vrows.append(row)
    checks.append({"check": "V-cm", "pass": bool(vok), "rows": vrows})
    say(f"V-cm   {'PASS' if vok else 'FAIL'}  boosted single mass over {T_RUN:.3f} Gyr: max|J-1| (2eps..300 kpc) <= 0.1 at h 10"
        f" and 5, h 5 <= h 10{' (WRONG-SIGN BOOST)' if MUTATE else ''}")
    for r in vrows:
        if r.get("missing"):
            say(f"       {r['mass']} {r['foot']}: missing")
            continue
        o = r["max_absJm1_outside"]
        say(f"       {r['mass']:3s} {r['foot']:9s} V {r['V_kms']} km/s: outside h20 {o[20]} h10 {o[10]:.4e} h5 {o[5]:.4e}  "
            f"inside 2eps {r['max_absJm1_inside_2eps']}  disp {r['max_comoving_disp_outside']}  {'ok' if r['pass'] else 'X'}")
    # D-ISO (no pass weight)
    iso = []
    for mass in ("MW", "M31"):
        for foot in ("canonical", "alt"):
            rr = {}
            for h in (20, 10, 5):
                f = WORK / f"single_iso_{mass}_{foot}_h{h}{SUF}.json"
                rr[h] = json.loads(f.read_text()) if f.exists() else None
            if rr[10] is None or rr[5] is None:
                iso.append({"mass": mass, "foot": foot, "missing": True})
                continue
            cl, why = cell_class(rr[10]["wake"], rr[5]["wake"])
            row = {"mass": mass, "foot": foot, "V_kms": rr[10]["V_kms"], "class": cl, "why": why,
                   "held_radius_max": rr[10]["held_radius_max"], "rcap": rr[10]["rcap"],
                   "per_h": {h: ({"down_min": rr[h]["wake"]["down"]["min"], "down_event": rr[h]["wake"]["down"]["event"],
                                  "up_min": rr[h]["wake"]["up"]["min"], "up_event": rr[h]["wake"]["up"]["event"],
                                  "D_EDGE": rr[h]["D_EDGE"], "D_STIFF": rr[h]["D_STIFF"],
                                  "core_absJm1_outside": rr[h]["max_absJm1_outside_2eps_le300"],
                                  "flags": dict(rr[h]["flags"], F4=rr[h]["F4"])} if rr[h] else None) for h in rr}}
            iso.append(row)
            say(f"D-ISO  {mass:3s} {foot:9s} V {row['V_kms']} km/s, held r <= {row['held_radius_max']:.0f} kpc: {cl}  {why}")
            for h in (20, 10, 5):
                p = row["per_h"][h]
                if p is None:
                    continue
                dm, um, de, ue = p["down_min"], p["up_min"], p["down_event"], p["up_event"]
                say(f"         h {h:2d}: down min {dm['J'] if dm else None:} at t {dm['t'] if dm else None} dz "
                    f"{dm['dz_from_mass'] if dm else None}; down event {de['t'] if de else None}; up min "
                    f"{um['J'] if um else None} at t {um['t'] if um else None}; up event {ue['t'] if ue else None}; edge "
                    f"{p['D_EDGE']['J'] if p['D_EDGE'] else None} at {p['D_EDGE']['t'] if p['D_EDGE'] else None}")
    out["checks"] = checks
    out["D_ISO"] = iso
    npass = sum(c["pass"] for c in checks)
    say(f"{npass}/{len(checks)} PASS" + (" (MUTATE: wrong-sign boost; V-cm must FAIL)" if MUTATE else ""))
    (HERE / f"x10_validate{SUF}.out").write_text("\n".join(lines) + "\n")
    (HERE / f"x10_validate_results{SUF}.json").write_text(json.dumps(out, indent=1, default=float))
    sys.exit(0 if (MUTATE or npass == len(checks)) else 1)
