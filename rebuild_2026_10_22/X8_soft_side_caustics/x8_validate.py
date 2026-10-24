#!/usr/bin/env python3
"""X8 validation (FROZEN_CRITERIA §4): R0 (the review reproduced read-only), V-a1 (static equilibrium), V-a2 (Galilean
moving equilibrium), V-b (linear dispersion on both sides of D.P = 0).

  python3 x8_validate.py --part R0|Va1|Va2|Vb     -> work/val_<part>[_MUTATE].json
  python3 x8_validate.py --collect                -> x8_validate[_MUTATE].out, x8_validate_results[_MUTATE].json
X8_MUTATE=1: frozen F (no self-consistent update).
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
from scipy.optimize import minimize_scalar
from scipy.special import j1, jn_zeros

if os.environ.get("MallocMediumZone") != "0":           # AMENDMENT A1: see x8_run.py
    os.environ["MallocMediumZone"] = "0"
    os.execv(sys.executable, [sys.executable] + sys.argv)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from x8_core import (A0, EPS, K, KMS, LSTAR, M2, HoldSolver, MonoAQUAL, Sim, initial_state, make_box_grid,  # noqa: E402
                     plummer_phi)

MUTATE = os.environ.get("X8_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
OUTBASE = Path(os.environ.get("X8_OUT", str(HERE)))
WORK = OUTBASE / "work"
WORK.mkdir(exist_ok=True)
REVIEW = HERE.parent.parent / "reviews" / "v3s_soft_side_caustics_2026_10_23"


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9


def bmask_of(grid):
    RR, ZZ = np.meshgrid(grid.R, grid.z)
    b = np.ones_like(RR, bool)
    b[1:-1, :-1] = False
    return RR, ZZ, b


# ====================================================================== R0
def part_R0():
    src = (REVIEW / "caustics.py").read_text()
    ns = {"__file__": str(REVIEW / "caustics.py"), "__name__": "x8_review_import"}
    saved = sys.argv
    sys.argv = [saved[0]]                               # the review's MUTATE flag stays off
    head = src[:src.index("# ================================================================ C0 solver check")]
    block = src[src.index("# ================================================================ C2 + C3"):src.index("# reading")]
    # run only the cases R0 needs (memory): the review's own loop body, with its iteration lists narrowed
    loop_ti = "for ti in (3.0, 6.0, 9.0):"
    assert block.count(loop_ti) == 1
    block = block.replace(loop_ti, "for ti in _X8_TI[(foot, oname)]:")
    exec(head, ns)
    full_A0, full_orb = dict(ns["A0"]), dict(ns["ORBITS"])
    ns["results"] = {}
    for foot, onames, tis in (("canonical", ("O1 timing Kepler", "O2 constant velocity"), (3.0,)),
                              ("alt", ("O2 constant velocity",), (9.0,))):
        ns["A0"] = {foot: full_A0[foot]}
        ns["ORBITS"] = {o: full_orb[o] for o in onames}
        ns["_X8_TI"] = {(foot, o): tis for o in onames}
        prev = ns["results"]
        exec(block, ns)                                 # the review's integrate(); writes nothing
        prev.update(ns["results"])
        ns["results"] = prev
    sys.argv = saved
    ref = json.loads((REVIEW / "caustics_results.json").read_text())["C3"]
    keys = ["canonical|O2 constant velocity|t_i 3.0|s 0", "canonical|O2 constant velocity|t_i 3.0|s 1",
            "canonical|O1 timing Kepler|t_i 3.0|s 0", "alt|O2 constant velocity|t_i 9.0|s 0"]
    rows, ok = [], True
    for k in keys:
        mine, theirs = ns["results"][k], ref[k]
        dd = abs(mine["det_min_to_t_end"] - theirs["det_min_to_t_end"])
        ts_ok = (mine["t_sc"] is None and theirs["t_sc"] is None) or (
            mine["t_sc"] is not None and theirs["t_sc"] is not None and abs(mine["t_sc"] - theirs["t_sc"]) <= 1e-9)
        ok &= dd <= 1e-6 and ts_ok
        rows.append({"case": k, "det_min_mine": mine["det_min_to_t_end"], "det_min_review": theirs["det_min_to_t_end"],
                     "abs_diff": dd, "t_sc_mine": mine["t_sc"], "t_sc_review": theirs["t_sc"], "t_sc_match": ts_ok})
    return {"pass": bool(ok), "rows": rows}


# ====================================================================== V-a (single mass)
def single_mass_run(foot, h, moving, T_run, log):
    a0 = A0[foot]
    gL = K * LSTAR[foot] ** 2 / 2
    if moving:
        grid = make_box_grid(500.0, -400.0, 1100.0, h, 20000.0)
    else:
        grid = make_box_grid(500.0, -500.0, 500.0, h, 20000.0)
    V = 110.0 * KMS if moving else 0.0
    RR, ZZ, bm = bmask_of(grid)
    mono = MonoAQUAL(M2, a0)

    def zc(t):
        return V * t

    def baryons(t):
        return [(M2, zc(t))]

    def bc(t, phib):
        Xb = np.zeros_like(RR)
        Xb[bm] = mono(np.hypot(RR, ZZ - zc(t))[bm])
        return Xb, Xb - phib

    phib0 = plummer_phi(grid.R, grid.z, baryons(0.0))
    Xb0, _ = bc(0.0, phib0)
    Xi, m, rho, x, info = initial_state(grid, a0, phib0, Xb0, gamma_L=gL)
    dt = min(0.02, 0.15 / info["omega_max"])
    sim = Sim(grid, a0, gL, baryons, bc, Xi, m, 0.0, frozen=MUTATE, v0=(0.0, V))
    acc = sim.accel(0.0)
    R_f, z_lo, z_hi, hh = grid.fine
    qR, qz = sim.q_R, sim.q_z
    lab = (qR > 0) & (qR <= R_f - 2 * hh) & (qz >= z_lo + 2 * hh) & (qz <= z_hi - 2 * hh)   # axis excluded (A1)
    dq = np.hypot(qR, qz)
    sel_out = lab & (dq >= 2 * EPS) & (dq <= 300.0)
    sel_in = lab & (dq < 2 * EPS)
    n = int(math.ceil(T_run / dt))
    nd = max(1, int(round(0.02 / dt)))
    mx_out = mx_in = mx_all = disp_out = disp_all = 0.0
    for s in range(1, n + 1):
        acc = sim.step(dt, acc)
        if s % nd == 0 or s == n:
            J = sim.J()
            dJ = np.abs(J - 1)
            mx_out = max(mx_out, float(dJ[sel_out].max()))
            mx_in = max(mx_in, float(dJ[sel_in].max()))
            mx_all = max(mx_all, float(dJ[qR > 0].max()))
            d = np.hypot(sim.XR - qR, sim.XZ - qz - V * sim.t)
            disp_out = max(disp_out, float(d[sel_out].max()))
            disp_all = max(disp_all, float(d[qR > 0].max()))
    res = {"foot": foot, "h": h, "moving": moving, "dt": dt, "steps": n, "omega_max": info["omega_max"],
           "aqual_rel_residual": info["rel_residual"], "n_interior": grid.nint,
           "max_absJm1_outside_2eps_le300": mx_out, "max_absJm1_inside_2eps": mx_in, "max_absJm1_all": mx_all,
           "max_comoving_disp_outside": disp_out, "max_comoving_disp_all": disp_all, "flags": sim.flags,
           "hold_iters_per_call": sim.iters_total / max(sim.ncalls, 1), "rss_GB": rss()}
    log(f"   {'V-a2' if moving else 'V-a1'} {foot:9s} h {h:4.0f}: max|J-1| out {mx_out:.3e} in {mx_in:.3e} all {mx_all:.3e}; "
        f"disp out {disp_out:.3e} all {disp_all:.3e} kpc; dt {dt:.4f}; iters/call {res['hold_iters_per_call']:.2f}")
    return res


def part_Va1(log):
    rows = [single_mass_run(f, h, False, 10.0, log) for f in ("canonical", "alt") for h in (20.0, 10.0, 5.0)]
    ok = all(r["max_absJm1_all"] <= 1e-4 and r["max_comoving_disp_all"] <= 1e-2 for r in rows)
    return {"pass": bool(ok), "rows": rows}


def part_Va2(log):
    rows = [single_mass_run("canonical", h, True, 6.0, log) for h in (20.0, 10.0, 5.0)]
    ok = all(r["max_absJm1_outside_2eps_le300"] <= 0.1 for r in rows if r["h"] in (10.0, 5.0))
    return {"pass": bool(ok), "rows": rows}


# ====================================================================== V-b (dispersion)
KRHO0 = 0.5            # Gyr^-2
LAM = 50.0             # kpc
RC, ZC, TAPER = 200.0, 200.0, 40.0


def taper(u, edge):
    w = np.ones_like(u)
    mid = (u > edge) & (u < edge + TAPER)
    w[mid] = np.cos(0.5 * math.pi * (u[mid] - edge) / TAPER) ** 2
    w[u >= edge + TAPER] = 0.0
    return w


def dispersion_run(sign, mode, h, log):
    foot = "canonical"
    a0 = A0[foot]
    gL = K * LSTAR[foot] ** 2 / 2
    grid = make_box_grid(320.0, -320.0, 320.0, h, 3000.0)
    RR, ZZ, bm = bmask_of(grid)
    rho0 = sign * KRHO0 / K
    rho_bg = rho0 * taper(RR[1:-1, :-1], RC) * taper(np.abs(ZZ[1:-1, :-1]), ZC)
    m = rho_bg * grid.V
    g0 = a0
    Xb = np.where(bm, g0 * ZZ, 0.0)
    phit_b = np.zeros_like(RR)
    hs = HoldSolver(grid, a0, tol=1e-9)
    Xi_int = hs.solve(K * m, Xb)
    Xi = grid.full(Xi_int, Xb)
    phit = grid.full(grid.solve_int(-K * m), phit_b)
    chi = Xi - phit
    rho_full = np.zeros_like(RR)
    rho_full[1:-1, :-1] = rho_bg
    phi_ext = chi - gL * np.maximum(rho_full, 0.0)       # exact stationarity of the background, stiffness included

    def baryons(t):
        return []

    def bc(t, phib):
        return Xb, phit_b

    sim = Sim(grid, a0, gL, baryons, bc, Xi, m, 0.0, frozen=MUTATE, tol=1e-7, phi_ext=phi_ext)
    # background values at the centre node (R = 0, z = 0)
    jc = int(np.argmin(np.abs(grid.z)))
    dR, dz = grid.node_grad(Xi)
    x_c = float(np.hypot(dR[jc, 0], dz[jc, 0]) / a0)
    rho_c = float(rho_full[jc, 0])
    qR, qz = sim.q_R, sim.q_z
    region = (qR <= RC) & (np.abs(qz) <= ZC)
    A = 1e-4 * LAM
    if mode == "L":
        k = 2 * math.pi / LAM
        shape = np.where(region, np.sin(k * qz), 0.0)
        sim.XZ = sim.XZ + A * shape
        Mm1 = (1 + x_c) ** 2 - 1
    else:
        zeros = jn_zeros(1, 40)
        jz = zeros[np.argmax(zeros / RC >= 2 * math.pi / LAM)]
        k = jz / RC
        shape = np.where(region, j1(k * qR), 0.0)
        sim.XR = sim.XR + A * shape
        Mm1 = x_c
    stiff_term = (LSTAR[foot] ** 2 * k * k / 2.0) if rho_c > 0 else 0.0
    om2_pred = K * rho_c * (Mm1 + stiff_term)
    rate_pred = math.sqrt(abs(om2_pred))
    centre = (qR <= 100.0) & (np.abs(qz) <= 100.0)
    S = shape[centre]
    norm = float(np.sum(S * S))

    def amp():
        disp = (sim.XZ - qz) if mode == "L" else (sim.XR - qR)
        return float(np.sum(disp[centre] * S) / norm)

    T_run = (1.5 * 2 * math.pi / rate_pred) if sign > 0 else (2.5 / rate_pred)
    dt = min(0.02, 0.15 / rate_pred)
    n = int(math.ceil(T_run / dt))
    acc = sim.accel(0.0)
    tt, aa = [0.0], [amp()]
    for s in range(1, n + 1):
        acc = sim.step(dt, acc)
        tt.append(sim.t)
        aa.append(amp())
    tt, aa = np.array(tt), np.array(aa)
    basis = np.cos if sign > 0 else np.cosh

    def cost(w):
        b = basis(w * tt)
        c = np.dot(b, aa) / np.dot(b, b)
        return float(np.sum((aa - c * b) ** 2))

    ws = np.linspace(0.0, 3 * rate_pred, 3001)
    cs = [cost(w) for w in ws]
    w0 = ws[int(np.argmin(cs))]
    lo, hi = max(0.0, w0 - 3 * rate_pred / 3000), w0 + 3 * rate_pred / 3000
    fit = minimize_scalar(cost, bounds=(lo, hi), method="bounded", options={"xatol": 1e-10})
    w_meas = float(fit.x)
    ratio = w_meas / rate_pred
    res = {"sign": sign, "mode": mode, "h": h, "k": k, "x_centre": x_c, "rho_centre": rho_c, "rate_pred": rate_pred,
           "rate_meas": w_meas, "ratio": ratio, "T_run": T_run, "dt": dt, "steps": n, "amp_start": float(aa[0]),
           "amp_end": float(aa[-1]), "fit_rms_rel": math.sqrt(fit.fun / len(tt)) / abs(aa[0]),
           "hold_iters_per_call": sim.iters_total / max(sim.ncalls, 1), "flags": sim.flags, "rss_GB": rss()}
    log(f"   V-b {mode}{'+' if sign > 0 else '-'} h {h:3.0f}: x_c {x_c:.4f}, rate pred {rate_pred:.5f} meas {w_meas:.5f} "
        f"ratio {ratio:.4f} (fit rms {res['fit_rms_rel']:.2e}); iters/call {res['hold_iters_per_call']:.2f}")
    return res


def part_Vb(log):
    rows = [dispersion_run(sg, md, h, log) for md in ("L", "T") for sg in (+1, -1) for h in (8.0, 4.0, 2.0)]
    fin = [r for r in rows if r["h"] == 2.0]
    ok = len(fin) == 4 and all(abs(r["ratio"] - 1) <= 0.05 for r in fin)
    return {"pass": bool(ok), "rows": rows}


# ====================================================================== main
ap = argparse.ArgumentParser()
ap.add_argument("--part", choices=["R0", "Va1", "Va2", "Vb"])
ap.add_argument("--collect", action="store_true")
a = ap.parse_args()

if a.part:
    t0 = time.time()
    logf = open(WORK / f"val_{a.part}{SUF}.log", "w")

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    res = {"R0": lambda: part_R0(), "Va1": lambda: part_Va1(log), "Va2": lambda: part_Va2(log),
           "Vb": lambda: part_Vb(log)}[a.part]()
    res["wall_s"] = time.time() - t0
    res["peak_rss_GB"] = rss()
    (WORK / f"val_{a.part}{SUF}.json").write_text(json.dumps(res, indent=1, default=float))
    log(f"{a.part}{SUF}: {'PASS' if res['pass'] else 'FAIL'}  ({res['wall_s']:.0f} s, peak RSS {res['peak_rss_GB']:.2f} GB)")

if a.collect:
    lines, out, npass = [], {"mutate": MUTATE}, 0
    labels = {"R0": "review reproduced (4 runs: det_min within 1e-6, t_sc within 1e-9)",
              "Va1": "static single mass: max|J-1| <= 1e-4 and displacement <= 1e-2 kpc (both footings, h 20/10/5)",
              "Va2": "Galilean-moving single mass: max|J-1| <= 0.1 outside 2 eps, <= 300 kpc, at h 10 and 5",
              "Vb": "dispersion L+/L-/T+/T- at h = 2 kpc: |rate_meas/rate_pred - 1| <= 0.05"}
    for p in ("R0", "Va1", "Va2", "Vb"):
        f = WORK / f"val_{p}{SUF}.json"
        if not f.exists():
            lines.append(f"{p:4s} MISSING")
            continue
        r = json.loads(f.read_text())
        out[p] = r
        npass += bool(r["pass"])
        lines.append(f"{p:4s} {'PASS' if r['pass'] else 'FAIL'}  {labels[p]}")
        for row in r["rows"]:
            if p == "R0":
                lines.append(f"       {row['case']}: det_min {row['det_min_mine']:+.6f} vs {row['det_min_review']:+.6f}; "
                             f"t_sc {row['t_sc_mine']} vs {row['t_sc_review']}")
            elif p in ("Va1", "Va2"):
                lines.append(f"       {row['foot']:9s} h {row['h']:4.0f}: max|J-1| outside {row['max_absJm1_outside_2eps_le300']:.3e}"
                             f", inside 2eps {row['max_absJm1_inside_2eps']:.3e}, all {row['max_absJm1_all']:.3e}; comoving "
                             f"disp outside {row['max_comoving_disp_outside']:.3e}, all {row['max_comoving_disp_all']:.3e} kpc")
            else:
                lines.append(f"       {row['mode']}{'+' if row['sign'] > 0 else '-'} h {row['h']:3.0f}: x_c {row['x_centre']:.4f}"
                             f" pred {row['rate_pred']:.5f} meas {row['rate_meas']:.5f} ratio {row['ratio']:.4f}")
    out["summary"] = f"{npass}/4 PASS"
    lines.append(out["summary"] + (" (MUTATE: frozen F)" if MUTATE else ""))
    txt = "\n".join(lines)
    print(txt)
    (HERE / f"x8_validate{SUF}.out").write_text(txt + "\n")
    (HERE / f"x8_validate_results{SUF}.json").write_text(json.dumps(out, indent=1, default=float))
