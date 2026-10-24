#!/usr/bin/env python3
"""X8 production run (FROZEN_CRITERIA §2, §3, §5, §6): one case (footing, orbit, t_i) at one resolution h.

Self-consistent by default; X8_MUTATE=1 drops the self-consistent update (frozen F, the review's s = 0 model).
Variants (N-checks): --dt-half, --box-half (B_out = 10 Mpc), --tol-tight (hold-law tol 1e-8).
Checkpoints to work/<tag>.ckpt.pkl every 10 min, on SIGTERM and at the --maxwall guard (exit 3); --resume continues.
Writes runs/<tag>.json.
"""
import argparse
import ctypes
import json
import math
import os
import pickle
import resource
import signal
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

if os.environ.get("MallocMediumZone") != "0":           # AMENDMENT A1: the macOS medium allocator keeps freed pages
    os.environ["MallocMediumZone"] = "0"                 # resident; disable it so RSS reflects live memory
    os.execv(sys.executable, [sys.executable] + sys.argv)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from x8_core import (A0, EPS, G, K, LSTAR, M1, M2, ORBITS, T0, T_END, A_K, TK, HoldSolver, MonoAQUAL, Sim,  # noqa: E402
                     initial_state, make_pair_grid, pair_positions, plummer_phi)

ap = argparse.ArgumentParser()
ap.add_argument("--foot", required=True, choices=["canonical", "alt"])
ap.add_argument("--orbit", required=True, choices=["O1", "O2"])
ap.add_argument("--ti", required=True, type=float)
ap.add_argument("--h", required=True, type=float)
ap.add_argument("--dt-half", action="store_true")
ap.add_argument("--box-half", action="store_true")
ap.add_argument("--tol-tight", action="store_true")
ap.add_argument("--maxwall", type=float, default=27.0, help="minutes before checkpoint-and-exit")
ap.add_argument("--resume", action="store_true")
args = ap.parse_args()
MUTATE = os.environ.get("X8_MUTATE", "0") == "1"
tag = f"{args.foot}_{args.orbit}_ti{int(args.ti)}_h{int(args.h)}"
tag += ("_dthalf" if args.dt_half else "") + ("_boxhalf" if args.box_half else "") + ("_toltight" if args.tol_tight else "")
tag += "_MUTATE" if MUTATE else ""
OUTBASE = Path(os.environ.get("X8_OUT", str(HERE)))     # development runs redirect their outputs (X8_OUT)
WORK, RUNS = OUTBASE / "work", OUTBASE / "runs"
WORK.mkdir(exist_ok=True)
RUNS.mkdir(exist_ok=True)
CKPT = WORK / f"{tag}.ckpt.pkl"
LOG = open(WORK / f"{tag}.log", "a")
T_WALL0 = time.time()
STOP = {"flag": False}


class _RU(ctypes.Structure):                              # rusage_info_v0, padded
    _fields_ = [("uuid", ctypes.c_uint8 * 16)] + [(n_, ctypes.c_uint64) for n_ in (
        "user_time", "system_time", "pkg_idle_wkups", "interrupt_wkups", "pageins", "wired_size", "resident_size",
        "phys_footprint", "proc_start_abstime", "proc_exit_abstime")] + [("pad", ctypes.c_uint64 * 32)]


def footprint_gb():
    """phys_footprint of this process (the macOS measure the heavy queue uses)."""
    try:
        ru = _RU()
        ctypes.CDLL("/usr/lib/libproc.dylib").proc_pid_rusage(os.getpid(), 0, ctypes.byref(ru))
        return ru.phys_footprint / 1e9
    except Exception:
        return float("nan")


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    LOG.write(line + "\n")
    LOG.flush()


def on_term(signum, frame):
    STOP["flag"] = True


signal.signal(signal.SIGTERM, on_term)

# ------------------------------------------------------------------ case geometry
a0 = A0[args.foot]
gamma_L = K * LSTAR[args.foot] ** 2 / 2.0
rfun, rdfun = ORBITS[args.orbit]
t_i, t_end = args.ti, T_END[args.orbit]
t_stop = t_end + 0.1
ts = np.linspace(t_i, t_end, 4001)
r_max = max(rfun(t) for t in ts)
if args.orbit == "O1" and t_i < math.pi * TK < t_end:
    r_max = max(r_max, 2 * A_K)
B_out = 10000.0 if args.box_half else 20000.0
grid = make_pair_grid(r_max, args.h, B_out=B_out)
R_f, z_lo, z_hi, hh = grid.fine
RR, ZZ = np.meshgrid(grid.R, grid.z)
bmask = np.ones_like(RR, bool)
bmask[1:-1, :-1] = False
mono = MonoAQUAL(M1 + M2, a0)
XI_BDY = np.zeros_like(RR)
XI_BDY[bmask] = mono(np.hypot(RR, ZZ)[bmask])          # barycentre fixed at the origin, total mass fixed


def baryons(t):
    z1, z2 = pair_positions(rfun(t))
    return [(M1, z1), (M2, z2)]


def bc(t, phib):
    return XI_BDY, XI_BDY - phib


def null_z(t):
    z1, z2 = pair_positions(rfun(t))

    def gz(z):
        return sum(-G * M * (z - zc) / ((z - zc) ** 2 + EPS ** 2) ** 1.5 for M, zc in ((M1, z1), (M2, z2)))
    return brentq(gz, z1 + 3 * EPS, z2 - 3 * EPS)


tol = 1e-8 if args.tol_tight else 1e-7

# ------------------------------------------------------------------ initial state or resume
if args.resume and CKPT.exists():
    st = pickle.loads(CKPT.read_bytes())
    m_int = st["m_node"]
    sim = Sim(grid, a0, gamma_L, baryons, bc, grid.full(st["Xi_int"], XI_BDY), st["m"].reshape(grid.NZ - 2, grid.NR - 1),
              st["t"], frozen=False, tol=tol, node_masses=False)
    if MUTATE:
        sim.frozen = True
        sim.acc_frozen = st["chi0"]
    for k_ in ("XR", "XZ", "VR", "VZ", "t", "flags", "ncalls", "iters_total", "xmax_seen"):
        setattr(sim, k_, st[k_])
    sim.hold.Xi_int = st["Xi_int"]
    acc, step, dt, meta, trk = st["acc"], st["step"], st["dt"], st["meta"], st["trk"]
    log(f"RESUME {tag} at t = {sim.t:.4f} step {step}")
else:
    log(f"START {tag}: grid NR {grid.NR} NZ {grid.NZ} interior {grid.nint}; fine zone R <= {R_f}, z in [{z_lo}, {z_hi}], "
        f"h {hh}; B_out {B_out}; r_max {r_max:.1f}")
    z1, z2 = pair_positions(rfun(t_i))
    phib0 = plummer_phi(grid.R, grid.z, [(M1, z1), (M2, z2)])
    Xi_eq, m_int, rho0, x0, info = initial_state(grid, a0, phib0, XI_BDY, gamma_L=gamma_L)
    log(f"  v3s static: {info['iterations']} Newton it (last), rel residual {info['rel_residual']:.2e}, stiffness outer "
        f"{info['stiffness_outer']}; omega_max {info['omega_max']:.3f} /Gyr")
    dt = min(0.02, 0.15 / info["omega_max"]) / (2.0 if args.dt_half else 1.0)
    meta_cfl = 0.15 / (2.0 if args.dt_half else 1.0)
    sim = Sim(grid, a0, gamma_L, baryons, bc, Xi_eq, m_int, t_i, frozen=MUTATE, tol=tol)
    acc = sim.accel(t_i)
    # t_i diagnostics: residual net force, stiffness-to-self-force ratio
    gRb, gzb = grid.node_grad(phib0)
    gb = np.hypot(gRb, gzb)[1:-1, :-1].ravel()
    a_mag = np.hypot(*acc)
    fine_lab = (sim.q_R <= R_f) & (sim.q_z >= z_lo) & (sim.q_z <= z_hi)
    net_rel = float((a_mag[fine_lab] / gb[fine_lab]).max())
    stiff_rel = None
    if not MUTATE:
        chi = sim._chi_nodes(t_i)
        cR, cz = grid.node_grad(chi)
        pR, pz = grid.node_grad(np.maximum(sim._rho, 0.0))
        sr = (gamma_L * np.hypot(pR, pz) / np.maximum(np.hypot(cR, cz), 1e-300))[1:-1, :-1].ravel()
        pos = (m_int.ravel() > 0) & fine_lab
        stiff_rel = {"max": float(sr[pos].max()), "median": float(np.median(sr[pos]))}
    meta = {"tag": tag, "foot": args.foot, "orbit": args.orbit, "t_i": t_i, "t_end": t_end, "h": args.h, "mutate": MUTATE,
            "variants": {"dt_half": args.dt_half, "box_half": args.box_half, "tol_tight": args.tol_tight},
            "grid": {"NR": grid.NR, "NZ": grid.NZ, "n_interior": grid.nint, "R_f": R_f, "z_lo": z_lo, "z_hi": z_hi,
                     "B_out": B_out, "r_max": r_max},
            "static": {"iterations_last": info["iterations"], "rel_residual": info["rel_residual"],
                       "stiffness_outer": info["stiffness_outer"]},
            "omega_max": info["omega_max"], "dt": dt, "tol": tol, "gamma_L": gamma_L, "a0": a0,
            "n_soft": int((m_int < 0).sum()), "n_soft_fine": int(((m_int.ravel() < 0) & fine_lab).sum()),
            "soft_mass": float(m_int[m_int < 0].sum()), "net_force_rel_at_ti_max": net_rel, "stiffness_ratio_at_ti": stiff_rel}
    log(f"  dt {dt:.5f} Gyr; soft labels {meta['n_soft']} ({meta['n_soft_fine']} in the fine zone); net |a|/|g_b| at t_i "
        f"max {net_rel:.2e}; stiffness/self-force {stiff_rel}")
    step = 0
    trk = None

# ------------------------------------------------------------------ tracker
m_lab = sim.m                                            # particle (deconvolved) masses
m_node = m_int.ravel() if not args.resume else st["m_node"]
soft = m_node < 0                                        # AMENDMENT A1: soft = discrete phantom < 0 at the label node
qR, qz = sim.q_R, sim.q_z
lab_valid = (qR > 0) & (qR <= R_f - 2 * hh) & (qz >= z_lo + 2 * hh) & (qz <= z_hi - 2 * hh)   # axis excluded (A1)
JCRIT, SUSTAIN = 0.05, 0.1
z1i, z2i = pair_positions(rfun(t_i))
near1 = (m_node > 0) & (np.hypot(qR, qz - z1i) <= 50.0)
near2 = (m_node > 0) & (np.hypot(qR, qz - z2i) <= 50.0)


def rec(val, t, k, XR, XZ, extra=None):
    z1, z2 = pair_positions(rfun(t))
    d1, d2 = math.hypot(XR[k], XZ[k] - z1), math.hypot(XR[k], XZ[k] - z2)
    out = {"J": float(val), "t": float(t), "t_minus_t0": float(t - T0), "label": [float(qR[k]), float(qz[k])],
           "pos": [float(XR[k]), float(XZ[k])], "dist_MW": d1, "dist_M31": d2, "z_rel_null": float(XZ[k] - null_z(t)),
           "charge": "soft" if m_node[k] < 0 else "stiff"}
    if extra:
        out.update(extra)
    return out


if trk is None:
    trk = {"start": np.full(m_lab.size, np.nan), "S": None, "S_t0": None, "S_TH": None, "fold": None, "event": None,
           "n_event_elements": 0, "graded": None, "stiff": None,
           "wake": {k_: None for k_ in ("MW_outer", "MW_inner", "M31_outer", "M31_inner")},
           "series": [], "follow": {}, "next_series": t_i, "iters_mark": (0, 0), "nsample": 0}


def upd(key, val, t, k, XR, XZ, holder=None, extra=None):
    h_ = trk if holder is None else holder
    if h_[key] is None or val < h_[key]["J"]:
        h_[key] = rec(val, t, k, XR, XZ, extra)


def sample(t):
    J = sim.J()
    XR, XZ = sim.XR, sim.XZ
    trk["nsample"] += 1
    pos_valid = (XR <= R_f - 2 * hh) & (XZ >= z_lo + 2 * hh) & (XZ <= z_hi - 2 * hh)
    sv = soft & lab_valid & pos_valid
    in_win = t <= t_end + 1e-9
    if sv.any():
        k = int(np.flatnonzero(sv)[np.argmin(J[sv])])
        if in_win:
            upd("S", J[k], t, k, XR, XZ)
            if t <= T0 + 1e-9:
                upd("S_t0", J[k], t, k, XR, XZ)
            if t <= t_i + 13.8 + 1e-9:
                upd("S_TH", J[k], t, k, XR, XZ)
            if J[k] <= 0 and trk["fold"] is None:
                trk["fold"] = rec(J[k], t, k, XR, XZ)
    below = sv & (J < JCRIT)
    st = trk["start"]
    st[~below] = np.nan
    newb = below & np.isnan(st)
    st[newb] = t
    conf = below & (t - st >= SUSTAIN - 1e-9) & (st <= t_end + 1e-9)
    if conf.any():
        trk["n_event_elements"] = max(trk["n_event_elements"], int(conf.sum()))
        if trk["event"] is None:
            k = int(np.flatnonzero(conf)[np.argmin(st[conf])])
            trk["event"] = rec(J[k], st[k], k, XR, XZ, {"confirmed_at": float(t)})
    if in_win:
        gr = soft & ~lab_valid & (qR > 0)
        if gr.any():
            k = int(np.flatnonzero(gr)[np.argmin(J[gr])])
            upd("graded", J[k], t, k, XR, XZ)
        stf = (~soft) & lab_valid & pos_valid
        if stf.any():
            k = int(np.flatnonzero(stf)[np.argmin(J[stf])])
            upd("stiff", J[k], t, k, XR, XZ)
        r = rfun(t)
        rd = rdfun(t)
        z1, z2 = pair_positions(r)
        v1, v2 = -M2 / (M1 + M2) * rd, M1 / (M1 + M2) * rd
        ax = (XR <= 30.0) & pos_valid & (qR > 0)
        zones = {"MW_outer": ax & (XZ <= z1 - 2 * EPS) & (XZ >= z1 - 1000.0),
                 "MW_inner": ax & (XZ >= z1 + 2 * EPS) & (XZ <= z1 + 0.5 * r),
                 "M31_outer": ax & (XZ >= z2 + 2 * EPS) & (XZ <= z2 + 1000.0),
                 "M31_inner": ax & (XZ <= z2 - 2 * EPS) & (XZ >= z2 - 0.5 * r)}
        for zn, msk in zones.items():
            if msk.any():
                k = int(np.flatnonzero(msk)[np.argmin(J[msk])])
                vg = v1 if zn.startswith("MW") else v2
                upd(zn, J[k], t, k, XR, XZ, holder=trk["wake"],
                    extra={"galaxy_vz_kpc_per_Gyr": float(vg), "zone_outer_is_downstream": bool(
                        (zn == "MW_outer" and vg > 0) or (zn == "M31_outer" and vg < 0))})
        for nm, near, zg_i, zg in (("MW", near1, z1i, z1), ("M31", near2, z2i, z2)):
            for when, tw in (("t0", T0), ("t_end", t_end)):
                key = f"{nm}_{when}"
                if key not in trk["follow"] and t >= tw - 1e-9 and t_i <= tw:
                    dzg = zg - zg_i
                    mz = float(np.sum(m_node[near] * (XZ[near] - qz[near])) / np.sum(m_node[near]))
                    trk["follow"][key] = {"t": float(t), "galaxy_dz": float(dzg), "halo_mean_dz": mz,
                                          "ratio": (mz / dzg) if abs(dzg) > 1.0 else None,
                                          "max_dR": float(np.abs(XR[near] - qR[near]).max())}
    if t >= trk["next_series"] - 1e-9:
        c0, i0 = trk["iters_mark"]
        dc = sim.ncalls - c0
        trk["series"].append({"t": round(float(t), 4), "S_now": float(J[sv].min()) if sv.any() else None,
                              "n_soft_valid": int(sv.sum()),
                              "stiff_now": float(J[(~soft) & lab_valid & pos_valid].min()),
                              "xmax": float(sim.hold.last_xmax), "iters_per_call": (sim.iters_total - i0) / dc if dc else None,
                              "lost_mass": float(sim.lost_mass)})
        trk["iters_mark"] = (sim.ncalls, sim.iters_total)
        trk["next_series"] += 0.1


def checkpoint():
    st = {"m": sim.m, "m_node": m_node, "Xi_int": sim.hold.Xi_int, "dt_now": dt_now, "dt_min_seen": dt_min_seen,
          "F4": F4, "XR": sim.XR, "XZ": sim.XZ, "VR": sim.VR, "VZ": sim.VZ, "t": sim.t,
          "flags": sim.flags, "ncalls": sim.ncalls, "iters_total": sim.iters_total, "xmax_seen": sim.xmax_seen,
          "acc": acc, "step": step, "dt": dt, "meta": meta, "trk": trk, "chi0": sim.acc_frozen}
    tmp = CKPT.with_suffix(".tmp")
    tmp.write_bytes(pickle.dumps(st, protocol=4))
    os.replace(tmp, CKPT)


CFL = 0.15 / (2.0 if args.dt_half else 1.0)
if step == 0:
    sample(t_i)
    dt_now, dt_min_seen, F4 = dt, dt, None
else:
    dt_now, dt_min_seen, F4 = st["dt_now"], st["dt_min_seen"], st["F4"]
next_sample = t_i + 0.02 * (trk["nsample"])
last_ck = time.time()
fp_peak = 0.0
while sim.t < t_stop - 1e-12:
    # AMENDMENT A1: adaptive step, dt = min(dt0, 0.15 / omega_max(t)), floor dt0/50 (flag F4 when reached)
    om = sim.omega_max() if not MUTATE else 0.0
    dt_now = min(dt, CFL / om) if om > 0 else dt
    if dt_now < dt / 50.0:
        dt_now = dt / 50.0
        if F4 is None:
            F4 = sim.t
            log(f"  F4 time-step floor reached at t {sim.t:.4f} (omega_max {om:.2f})")
    dt_now = min(dt_now, t_stop - sim.t + 1e-12)
    dt_min_seen = min(dt_min_seen, dt_now)
    acc = sim.step(dt_now, acc)
    step += 1
    if sim.t >= next_sample - 1e-9 or sim.t >= t_stop - 1e-12:
        sample(sim.t)
        next_sample += 0.02
    if step % 500 == 0:
        fp_peak = max(fp_peak, footprint_gb())
        log(f"  step {step} t {sim.t:.3f} dt {dt_now:.5f}  S {trk['S']['J'] if trk['S'] else None}  iters/call "
            f"{sim.iters_total / max(sim.ncalls, 1):.2f}  xmax {sim.xmax_seen:.3f}  "
            f"rss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB  footprint {fp_peak:.2f} GB")
    now = time.time()
    if now - last_ck > 600:
        checkpoint()
        last_ck = now
    if STOP["flag"] or now - T_WALL0 > args.maxwall * 60:
        checkpoint()
        log(f"  CHECKPOINT at t {sim.t:.4f} step {step} ({'SIGTERM' if STOP['flag'] else 'wall guard'}); resume with --resume")
        sys.exit(3)

out = dict(meta)
out.update({"S": trk["S"], "S_by_t0": trk["S_t0"], "S_by_ti_plus_TH": trk["S_TH"], "first_fold": trk["fold"],
            "event": trk["event"], "n_event_elements_max": trk["n_event_elements"], "D_GRADED": trk["graded"],
            "D_STIFF": trk["stiff"], "D_WAKE": trk["wake"], "D_FOLLOW": trk["follow"],
            "flags": dict(sim.flags, F4=F4), "dt_min_seen": dt_min_seen, "xmax_seen": sim.xmax_seen,
            "hold_calls": sim.ncalls, "peak_footprint_GB_sampled": max(fp_peak, footprint_gb()),
            "hold_iters_per_call": sim.iters_total / max(sim.ncalls, 1), "series": trk["series"], "steps": step,
            "peak_rss_GB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9})
(RUNS / f"{tag}.json").write_text(json.dumps(out, indent=1, default=float))
np.savez_compressed(WORK / f"{tag}.final.npz", XR=sim.XR, XZ=sim.XZ, qR=qR, qz=qz, m=m_lab, J=sim.J())
if CKPT.exists():
    CKPT.unlink()
log(f"DONE {tag}: S {trk['S']['J'] if trk['S'] else None}  event {trk['event']}  fold {trk['fold'] is not None}  "
    f"flags {sim.flags}  wall {(time.time() - T_WALL0) / 60:.1f} min")
