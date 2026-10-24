#!/usr/bin/env python3
"""X12 3D run (FROZEN_CRITERIA §2-§6): one configuration at one resolution.

  --kind static  V-a1: M31 at rest, box S [-240, 240], 10 Gyr
  --kind vcm     V-cm: --mass MW|M31 boosted with its full equilibrium (data follow the mass), 15.167 Gyr (canonical)
  --kind wake    case W: isolated MW-mass at 68.75 km/s, X10 D-ISO start, window W_a = 9.067 Gyr (+0.1)
  --kind enc     case E: O2-like encounter, t_i 3, impact parameter --b, X10 co-moving start, to t_end + 0.1
Variants (N-checks): --dt-half, --box-half (B_out 2500 kpc), --tol-tight (hold tol 1e-8). X12_MUTATE=1: wrong-sign boost.
Checkpoints to work/<tag>.ckpt.pkl every 10 min, on SIGTERM and at the --maxwall guard (exit 3); --resume continues.
Writes runs/<tag>.json (and work/<tag>.final.npz).
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

for _k in ("OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_k, "1")
if os.environ.get("MallocMediumZone") != "0":
    os.environ["MallocMediumZone"] = "0"
    os.execv(sys.executable, [sys.executable] + sys.argv)

import numpy as np  # noqa: E402
from scipy.optimize import brentq  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import x12_core as C  # noqa: E402
from x12_core import A0, EPS, G, K, KMS, LSTAR, M1, M2, T0, MonoAQUAL  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--kind", required=True, choices=["static", "vcm", "wake", "enc"])
ap.add_argument("--foot", default="canonical", choices=["canonical", "alt"])
ap.add_argument("--mass", default="MW", choices=["MW", "M31"])
ap.add_argument("--h", required=True, type=float)
ap.add_argument("--b", type=float, default=0.0)
ap.add_argument("--dt-half", action="store_true")
ap.add_argument("--box-half", action="store_true")
ap.add_argument("--tol-tight", action="store_true")
ap.add_argument("--maxwall", type=float, default=27.0)
ap.add_argument("--resume", action="store_true")
ap.add_argument("--a1", choices=["loc", "box"], default=None, help="AMENDMENT A1 diagnostics (V-cm only)")
ap.add_argument("--a2", choices=["mir", "dt"], default=None, help="AMENDMENT A2 diagnostics (V-cm only)")
args = ap.parse_args()
MUTATE = os.environ.get("X12_MUTATE", "0") == "1"

# ------------------------------------------------------------------ configuration (FROZEN §2, §3)
W_A = 18.067 - 9.0                                          # the wake window
from x8_core import T_END as _TE  # noqa: E402
T_END_E = _TE["O2"]                                         # 18.067 Gyr (d = 300 kpc)
JCRIT, SUSTAIN = 0.05, 0.1
F1_, F2_ = M1 / (M1 + M2), M2 / (M1 + M2)                   # 0.375, 0.625
VMW, VM31 = 68.75 * KMS, 41.25 * KMS
B_OUT = 2500.0 if args.box_half else 5000.0
QG = 1.25
h = args.h
a0 = A0[args.foot]
gamma_L = K * LSTAR[args.foot] ** 2 / 2.0
kind = args.kind
if kind == "static":
    tag = f"static_M31_{args.foot}_h{int(h)}"
elif kind == "vcm":
    tag = f"vcm_{args.mass}_{args.foot}_h{int(h)}"
elif kind == "wake":
    tag = f"wake_{args.foot}_h{int(h)}"
else:
    tag = f"enc_b{int(args.b)}_{args.foot}_h{int(h)}"
tag += ("_dthalf" if args.dt_half else "") + ("_boxhalf" if args.box_half else "") + ("_toltight" if args.tol_tight else "")
tag += f"_A1{args.a1}" if args.a1 else ""
tag += f"_A2{args.a2}" if args.a2 else ""
tag += "_MUTATE" if MUTATE else ""
WORK, RUNS = HERE / "work", HERE / "runs"
WORK.mkdir(exist_ok=True)
RUNS.mkdir(exist_ok=True)
CKPT = WORK / f"{tag}.ckpt.pkl"
LOG = open(WORK / f"{tag}.log", "a")
T_WALL0 = time.time()
STOP = {"flag": False}


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    LOG.write(line + "\n")
    LOG.flush()


signal.signal(signal.SIGTERM, lambda s, f: STOP.__setitem__("flag", True))


class _RU(ctypes.Structure):
    _fields_ = [("uuid", ctypes.c_uint8 * 16)] + [(n_, ctypes.c_uint64) for n_ in (
        "user_time", "system_time", "pkg_idle_wkups", "interrupt_wkups", "pageins", "wired_size", "resident_size",
        "phys_footprint", "proc_start_abstime", "proc_exit_abstime")] + [("pad", ctypes.c_uint64 * 32)]


def footprint_gb():
    try:
        ru = _RU()
        ctypes.CDLL("/usr/lib/libproc.dylib").proc_pid_rusage(os.getpid(), 0, ctypes.byref(ru))
        return ru.phys_footprint / 1e9
    except Exception:
        return float("nan")


# boxes
if kind == "enc":
    mir = (0, 1, 0)
    fine = {"x": (-300.0, 300.0), "y": (0.0, 240.0), "z": (-1440.0, 1260.0), "h": h}
    t_i, t_stop = 3.0, T_END_E + 0.1
    t_win = T_END_E                                          # soft window end
else:
    mir = (1, 1, 0)
    if args.a2 == "mir":                                     # AMENDMENT A2-mir: full domain, no mirror planes
        assert kind == "vcm"
        mir = (0, 0, 0)
    zr = {"static": (-240.0, 240.0), "wake": (-480.0, 1200.0),
          "vcm": (-360.0, 1440.0) if args.mass == "MW" else (-360.0, 1020.0)}[kind]
    if args.a1 == "box":                                     # AMENDMENT A1-box: >= 300 kpc margin from graded labels
        assert kind == "vcm"
        zr = (-660.0, 1680.0) if args.mass == "MW" else (-600.0, 1260.0)
    fine = {"x": (0.0, 240.0), "y": (0.0, 240.0), "z": zr, "h": h}
    if args.a2 == "mir":
        fine["x"], fine["y"] = (-240.0, 240.0), (-240.0, 240.0)
    t_i = 0.0
    t_stop = {"static": 10.0, "vcm": 18.067 + 0.1 - 3.0, "wake": W_A + 0.1}[kind]
    t_win = t_stop - 0.1 if kind == "wake" else t_stop
t_wake_end = t_i + W_A                                       # the wake window end (E and W)
axes = [C.build_axis(fine[a][0], fine[a][1], h, B_OUT, QG, bool(mir[i])) for i, a in enumerate("xyz")]
grid = C.Grid3(*axes, mir, fine)
tol = 1e-8 if args.tol_tight else 1e-7
LSH = grid.ishape


# ------------------------------------------------------------------ baryons and boundary data
def gal_state(t):
    """[(name, M, position, velocity_z)] at time t."""
    if kind == "enc":
        d = C.r_O2(t)
        return [("MW", M1, (-F2_ * args.b, 0.0, -F2_ * d), F2_ * (-C.V0_ORB)),
                ("M31", M2, (F1_ * args.b, 0.0, F1_ * d), -F1_ * (-C.V0_ORB))]
    M = M1 if (kind != "static" and args.mass == "MW") or kind == "wake" else M2
    if kind == "static":
        return [("M31", M2, (0.0, 0.0, 0.0), 0.0)]
    V = VMW if M == M1 else VM31
    return [("MW" if M == M1 else "M31", M, (0.0, 0.0, V * t), V)]


def baryons(t):
    return [(M, p) for _, M, p, _ in gal_state(t)]


M_TOT = sum(M for _, M, _, _ in gal_state(t_i))
MONO = MonoAQUAL(M_TOT, a0)
XB_FIXED = C.mono_bdy(grid, M_TOT, a0, (0.0, 0.0, 0.0), MONO)


def bc(t, phib):
    if kind == "vcm":                                        # the data follow the mass (X8 V-a2, X10 V-cm)
        Xb = C.mono_bdy(grid, M_TOT, a0, gal_state(t)[0][2], MONO)
    else:
        Xb = XB_FIXED
    return Xb, Xb - phib


def null_point(t):
    gs = gal_state(t)
    if len(gs) < 2:
        return None, None
    p1, p2 = np.array(gs[0][2]), np.array(gs[1][2])
    sep = p2 - p1
    r = float(np.linalg.norm(sep))

    def gs_(s):
        a, b_ = s * r, (1 - s) * r
        return -G * M1 * a / (a * a + EPS ** 2) ** 1.5 + G * M2 * b_ / (b_ * b_ + EPS ** 2) ** 1.5
    s = brentq(gs_, 3 * EPS / r, 1 - 3 * EPS / r)
    return p1 + s * sep, sep / r


# ------------------------------------------------------------------ initial state or resume
if args.resume and CKPT.exists():
    st = pickle.loads(CKPT.read_bytes())
    sim = C.Sim3(grid, a0, gamma_L, baryons, bc, st["Xi_full"], None, st["t"], tol=tol, masses=st["m"])
    for k_ in ("t", "flags", "ncalls", "iters_total", "xmax_seen"):
        setattr(sim, k_, st[k_])
    sim.X, sim.V, sim.A = st["X"], st["V"], st["A"]
    sim.hold.Xi_int, sim.hold.Xi_prev = st["Xi_int"], st["Xi_prev"]
    sim.Xi_full = st["Xi_full"]
    sim._rho_abs = st["rho_abs"]
    meta, trk, step, dt0, cls, m_node = st["meta"], st["trk"], st["step"], st["dt0"], st["cls"], st["m_node"]
    log(f"RESUME {tag} at t = {sim.t:.4f} step {step}")
else:
    log(f"START {tag}: nodes {grid.shape} = {np.prod(grid.shape)}, unknowns {grid.nint}; fine {fine}; B_out {B_OUT}; "
        f"mirrors {mir}{' (WRONG-SIGN BOOST)' if MUTATE else ''}")
    phib0 = C.plummer_phi3(grid, baryons(t_i))
    Xi_eq, m_node, info = C.initial_state(grid, a0, phib0, XB_FIXED if kind != "vcm" else bc(t_i, phib0)[0], gamma_L,
                                          log=None)
    log(f"  v3s static: Newton it {info['iterations']}, rel residual {info['rel_residual']:.2e}, stiffness outer "
        f"{['%.1e' % v for v in info['stiffness_outer']]}; omega_max {info['omega_max']:.3f} /Gyr; "
        f"{(time.time() - T_WALL0):.0f} s")
    dt0 = min(0.02, 0.15 / info["omega_max"]) / (2.0 if (args.dt_half or args.a2 == "dt") else 1.0)
    sim = C.Sim3(grid, a0, gamma_L, baryons, bc, Xi_eq, m_node, t_i, tol=tol)
    m_node = m_node.ravel()
    qx, qy, qz = sim.q
    # ---- the start: velocity classes (FROZEN §2; X10 §2)
    sgn = -1.0 if MUTATE else 1.0
    gs = gal_state(t_i)
    if kind == "static":
        cls = np.zeros(qx.size, np.int8)
    elif kind == "vcm":
        cls = np.ones(qx.size, np.int8)
    elif kind == "wake":
        _, M, p, V = gs[0]
        e = 0.5 * V ** 2 - G * M / np.sqrt(qx ** 2 + qy ** 2 + (qz - p[2]) ** 2 + EPS ** 2)
        cls = (e < 0).astype(np.int8)
    else:
        es = []
        for _, M, p, V in gs:
            es.append(0.5 * V ** 2 - G * M / np.sqrt((qx - p[0]) ** 2 + (qy - p[1]) ** 2 + (qz - p[2]) ** 2 + EPS ** 2))
        cls = np.zeros(qx.size, np.int8)
        cls[(es[0] < 0) & (es[1] >= 0)] = 1
        cls[(es[1] < 0) & (es[0] >= 0)] = 2
        common = (es[0] < 0) & (es[1] < 0)
    Vg = [gs[0][3], gs[1][3] if len(gs) > 1 else 0.0]
    vz0 = np.zeros(qx.size)
    vz0[cls == 1] = sgn * Vg[0]
    vz0[cls == 2] = sgn * Vg[1]
    sim.V[2][:] = vz0
    del vz0
    # straddle labels (FROZEN §3 / X10 §3): a +-1 neighbour (mirror ghosts have the same class) of another class
    Cc = cls.reshape(LSH)
    stc = np.zeros(LSH, bool)
    for ax in range(3):
        sl1 = [slice(None)] * 3
        sl2 = [slice(None)] * 3
        sl1[ax], sl2[ax] = slice(1, None), slice(None, -1)
        d_ = Cc[tuple(sl1)] != Cc[tuple(sl2)]
        stc[tuple(sl1)] |= d_
        stc[tuple(sl2)] |= d_
    straddle0 = stc.ravel()
    del Cc, stc
    sim.accel(t_i)
    net = float(np.sqrt(sim.A[0] ** 2 + sim.A[1] ** 2 + sim.A[2] ** 2).max())
    dep0 = grid.deposit(sim.X[0], sim.X[1], sim.X[2], sim.m)
    dep_err = float(np.abs(dep0[grid.sl].ravel() - m_node).max() / np.abs(m_node).max())
    del dep0
    soft0 = m_node < 0
    held = {"n_class": [int((cls == c_).sum()) for c_ in (0, 1, 2)], "n_soft_held": int((soft0 & (cls > 0)).sum()),
            "n_straddle": int(straddle0.sum()), "n_soft_straddle": int((soft0 & straddle0).sum()),
            "V_kpc_per_Gyr": Vg, "boost_sign": sgn}
    if kind == "enc":
        held["n_common"] = int(common.sum())
    for c_, (nm, M, p, V) in zip((1, 2), gs):
        sel = cls == c_
        held[f"held_radius_max_{nm}"] = float(np.sqrt((qx[sel] - p[0]) ** 2 + (qy[sel] - p[1]) ** 2 +
                                                      (qz[sel] - p[2]) ** 2).max()) if sel.any() else None
        held[f"rcap_{nm}"] = 2 * G * M / V ** 2 if V else None
    meta = {"tag": tag, "kind": kind, "foot": args.foot, "mass": args.mass, "b": args.b, "h": h, "t_i": t_i,
            "t_stop": t_stop, "t_win": t_win, "t_wake_end": t_wake_end, "mutate_wrong_sign": MUTATE,
            "variants": {"dt_half": args.dt_half, "box_half": args.box_half, "tol_tight": args.tol_tight},
            "grid": {"shape": list(grid.shape), "n_unknown": grid.nint, "fine": fine, "B_out": B_OUT, "q": QG,
                     "mirrors": list(mir)},
            "static": {"iterations": info["iterations"], "rel_residual": info["rel_residual"],
                       "stiffness_outer": info["stiffness_outer"], "cg_iterations": info["cg_iterations"]},
            "omega_max_ti": info["omega_max"], "dt0": dt0, "tol": tol, "gamma_L": gamma_L, "a0": a0,
            "n_soft": int(soft0.sum()), "net_accel_at_ti_max": net, "deposit_identity_rel": dep_err,
            "D_HELD": held}
    log(f"  dt0 {dt0:.5f}; soft labels {meta['n_soft']}; max |a| at t_i {net:.2e} kpc/Gyr^2; deposit identity "
        f"{dep_err:.1e}; D-HELD {held}")
    step = 0
    trk = None

# ------------------------------------------------------------------ label sets
qx, qy, qz = sim.q
if trk is None:
    straddle = straddle0
else:
    straddle = trk["straddle"]
nstr = ~straddle
soft = m_node < 0
stiff = m_node > 0
fx, fy, fz = fine["x"], fine["y"], fine["z"]


def in_fine_valid(x, y, z, margin):
    """Inside the fine zone at least `margin` from its outer faces (mirror planes are not faces; |coordinate|)."""
    ok = np.ones(x.shape, bool)
    for c, (lo, hi), m in ((x, fx, mir[0]), (y, fy, mir[1]), (z, fz, mir[2])):
        cc = np.abs(c) if m else c
        ok &= cc <= hi - margin
        if not m:
            ok &= cc >= lo + margin
    return ok


axis_line = (qx == 0.0) & (qy == 0.0)                         # FROZEN §3: excluded from every J statistic
lab_valid = in_fine_valid(qx, qy, qz, 2 * h) & ~axis_line
VI = np.flatnonzero(lab_valid)                               # validated labels
SV = VI[soft[VI] & nstr[VI]]                                 # soft statistic candidates
STV = VI[stiff[VI] & nstr[VI]]
EDGE = np.flatnonzero(straddle & ~axis_line & in_fine_valid(qx, qy, qz, 0.0))
GRADED = np.flatnonzero(soft & ~lab_valid & ~axis_line & nstr)
AXL = np.flatnonzero(axis_line & in_fine_valid(qx, qy, qz, 2 * h))
if kind in ("static", "vcm", "wake"):
    p0 = gal_state(t_i)[0][2]
    dq = np.sqrt((qx - p0[0]) ** 2 + (qy - p0[1]) ** 2 + (qz - p0[2]) ** 2)
    SEL_OUT = VI[(dq[VI] >= 2 * EPS) & (dq[VI] <= 300.0)]
    SEL_IN = VI[dq[VI] < 2 * EPS]
    del dq
GALS = [g_[0] for g_ in gal_state(t_i)] if kind in ("wake", "enc") else []
LIDX = np.arange(qx.size).reshape(LSH)


def lattice_index(k):
    return np.unravel_index(int(k), LSH)


def svd_at(k):
    F = sim.defgrad(*lattice_index(k))
    return [float(v) for v in np.linalg.svd(F, compute_uv=False)]


def rec(J, t, k, extra=None):
    X, Y, Z = sim.X[0][k], sim.X[1][k], sim.X[2][k]
    out = {"J": float(J[k]), "t": float(t), "label": [float(qx[k]), float(qy[k]), float(qz[k])],
           "pos": [float(X), float(Y), float(Z)], "charge": "soft" if m_node[k] < 0 else "stiff",
           "start_class": int(cls[k]), "straddle": bool(straddle[k])}
    for nm, M, p, V in gal_state(t):
        out[f"dist_{nm}"] = float(math.sqrt((X - p[0]) ** 2 + (Y - p[1]) ** 2 + (Z - p[2]) ** 2))
        out[f"Rperp_{nm}"] = float(math.hypot(X - p[0], Y - p[1]))
        out[f"dz_{nm}"] = float(Z - p[2])
    npnt, nhat = null_point(t)
    if npnt is not None:
        out["along_sep_rel_null"] = float(np.dot(np.array([X, Y, Z]) - npnt, nhat))
    if extra:
        out.update(extra)
    return out


def upd(holder, key, J, t, k, extra=None):
    if holder.get(key) is None or J[k] < holder[key]["J"]:
        holder[key] = rec(J, t, k, extra)


if trk is None:
    trk = {"straddle": straddle, "nsample": 0, "next_series": t_i, "iters_mark": (0, 0), "series": [],
           "soft": {"start": np.full(SV.size, np.nan), "S": None, "S_t0": None, "fold": None, "event": None,
                    "n_event_max": 0, "sv_start": {}, "follow": None},
           "wake": {f"{g_}_{s_}": {"start": np.full(qx.size, np.nan), "min_W": None, "min_full": None,
                                   "first_below": None, "event": None, "sv_start": {}, "follow": None}
                    for g_ in GALS for s_ in ("down", "up")},
           "stiff": None, "stiff_first_below": None, "edge": None, "edge_first_fold": None, "graded": None,
           "axis": {"soft": None, "stiff": None, "first_below": None},
           "vstat": {"mx_out": 0.0, "t_mx_out": None, "mx_in": 0.0, "mx_all": 0.0, "disp_out": 0.0, "disp_all": 0.0},
           "dfollow": {}}
SVCAP = 20000


def sample(t, J):
    trk["nsample"] += 1
    X, Y, Z = sim.X
    in_soft_win = t <= t_win + 1e-9
    # ---- V-a1 / V-cm statistics
    if kind in ("static", "vcm", "wake"):
        vs = trk["vstat"]
        dJ = np.abs(J[SEL_OUT] - 1)
        v = float(dJ.max())
        if v > vs["mx_out"]:
            vs["mx_out"], vs["t_mx_out"] = v, float(t)
        vs["mx_in"] = max(vs["mx_in"], float(np.abs(J[SEL_IN] - 1).max()))
        vs["mx_all"] = max(vs["mx_all"], float(np.abs(J[VI] - 1).max()))
        p = gal_state(t)[0][2] if kind == "vcm" else (0.0, 0.0, 0.0)
        p0_ = gal_state(t_i)[0][2]
        dsp = np.sqrt((X[VI] - qx[VI] - (p[0] - p0_[0])) ** 2 + (Y[VI] - qy[VI] - (p[1] - p0_[1])) ** 2 +
                      (Z[VI] - qz[VI] - (p[2] - p0_[2])) ** 2)
        vs["disp_all"] = max(vs["disp_all"], float(dsp.max()))
        if kind != "wake":
            vs["disp_out"] = max(vs["disp_out"], float(np.sqrt(
                (X[SEL_OUT] - qx[SEL_OUT] - (p[0] - p0_[0])) ** 2 + (Y[SEL_OUT] - qy[SEL_OUT] - (p[1] - p0_[1])) ** 2 +
                (Z[SEL_OUT] - qz[SEL_OUT] - (p[2] - p0_[2])) ** 2).max()))
    # ---- soft statistic (X8 §5 / X10 §5a)
    if kind == "enc":
        so = trk["soft"]
        xs, ys, zs = X[SV], Y[SV], Z[SV]
        pv = in_fine_valid(xs, ys, zs, 2 * h)
        Js = J[SV]
        if pv.any() and in_soft_win:
            i = int(np.flatnonzero(pv)[np.argmin(Js[pv])])
            k = int(SV[i])
            upd(so, "S", J, t, k)
            if t <= T0 + 1e-9:
                upd(so, "S_t0", J, t, k)
            if J[k] <= 0 and so["fold"] is None:
                so["fold"] = rec(J, t, k)
        below = pv & (Js < JCRIT)
        st_ = so["start"]
        st_[~below] = np.nan
        newb = below & np.isnan(st_)
        st_[newb] = t
        for i in np.flatnonzero(newb)[:max(0, SVCAP - len(so["sv_start"]))]:
            so["sv_start"][int(SV[i])] = (float(t), svd_at(int(SV[i])))
        conf = below & (t - st_ >= SUSTAIN - 1e-9) & (st_ <= t_win + 1e-9)
        if conf.any():
            so["n_event_max"] = max(so["n_event_max"], int(conf.sum()))
            if so["event"] is None:
                i = int(np.flatnonzero(conf)[np.argmin(st_[conf])])
                k = int(SV[i])
                ev = rec(J, st_[i], k, {"confirmed_at": float(t), "sv_at_confirm": svd_at(k)})
                ev["sv_at_start"] = so["sv_start"].get(k)
                so["event"] = ev
                so["follow"] = {"k": k, "Jmin": float(J[k]), "t": float(t), "sv": ev["sv_at_confirm"]}
        if so["follow"] is not None:
            k = so["follow"]["k"]
            if J[k] < so["follow"]["Jmin"] and in_soft_win:
                so["follow"].update({"Jmin": float(J[k]), "t": float(t), "sv": svd_at(k)})
    # ---- wake cells (X10 §5b in 3D; FROZEN §5a)
    if GALS:
        gs = gal_state(t)
        d_sep = C.r_O2(t) if kind == "enc" else None
        for idx_g, (nm, M, p, V) in enumerate(gs):
            u = float(np.sign(V))
            Rp2 = (X - p[0]) ** 2 + (Y - p[1]) ** 2
            dz = Z - p[2]
            base = (Rp2 <= 900.0) & in_fine_valid(X, Y, Z, 2 * h) & ~axis_line
            if kind == "enc":
                outer_sign = -1.0 if nm == "MW" else 1.0     # MW's outer side is -z, M31's is +z
                outer = (dz * outer_sign >= 2 * EPS) & (dz * outer_sign <= 1000.0)
                inner = (-dz * outer_sign >= 2 * EPS) & (-dz * outer_sign <= 0.5 * d_sep)
                zone = base & (outer | inner)
            else:
                zone = base & (np.abs(dz) >= 2 * EPS) & (np.abs(dz) <= 1000.0)
            for s_ in ("down", "up"):
                key = f"{nm}_{s_}"
                w = trk["wake"][key]
                side = (dz * u < 0) if s_ == "down" else (dz * u > 0)
                zf = zone & side & stiff & nstr
                belowg = J < JCRIT
                stw = w["start"]
                stw[~belowg] = np.nan
                if t <= t_win + 1e-9:
                    newg = belowg & np.isnan(stw) & zf
                    stw[newg] = t
                    for k in np.flatnonzero(newg)[:max(0, SVCAP - len(w["sv_start"]))]:
                        w["sv_start"][int(k)] = (float(t), svd_at(int(k)))
                confg = belowg & ~np.isnan(stw) & (t - stw >= SUSTAIN - 1e-9) & (stw <= t_win + 1e-9)
                if confg.any() and w["event"] is None:
                    cand = np.flatnonzero(confg)
                    k = int(cand[np.argmin(stw[cand])])
                    ev = rec(J, float(stw[k]), k, {"confirmed_at": float(t), "galaxy_vz": V,
                                                   "sv_at_confirm": svd_at(k)})
                    ev["sv_at_start"] = w["sv_start"].get(k)
                    w["event"] = ev
                    w["follow"] = {"k": k, "Jmin": float(J[k]), "t": float(t), "sv": ev["sv_at_confirm"]}
                if w["follow"] is not None:
                    k = w["follow"]["k"]
                    if J[k] < w["follow"]["Jmin"] and t <= t_win + 1e-9:
                        w["follow"].update({"Jmin": float(J[k]), "t": float(t), "sv": svd_at(k)})
                if zf.any():
                    cand = np.flatnonzero(zf)
                    k = int(cand[np.argmin(J[cand])])
                    if t <= t_wake_end + 1e-9:
                        upd(w, "min_W", J, t, k, {"galaxy_vz": V})
                    if t <= t_win + 1e-9:
                        upd(w, "min_full", J, t, k, {"galaxy_vz": V})
                    if J[k] < JCRIT and w["first_below"] is None and t <= t_win + 1e-9:
                        w["first_below"] = rec(J, t, k, {"galaxy_vz": V})
            # D-FOLLOW (positive labels within 50 kpc of the galaxy's start position)
            for when, tw in (("t0", T0), ("t_end", t_win)):
                key = f"{nm}_{when}"
                if key not in trk["dfollow"] and t >= tw - 1e-9 and t_i <= tw:
                    p0g = gal_state(t_i)[idx_g][2]
                    near = stiff & (np.sqrt((qx - p0g[0]) ** 2 + (qy - p0g[1]) ** 2 + (qz - p0g[2]) ** 2) <= 50.0)
                    mz = float(np.sum(m_node[near] * (Z[near] - qz[near])) / np.sum(m_node[near]))
                    dzg = p[2] - p0g[2]
                    trk["dfollow"][key] = {"t": float(t), "galaxy_dz": dzg, "halo_mean_dz": mz,
                                           "ratio": mz / dzg if abs(dzg) > 1.0 else None}
    # ---- D-STIFF, D-EDGE, D-GRADED, D-AXIS
    if t <= t_win + 1e-9:
        pv = in_fine_valid(X[STV], Y[STV], Z[STV], 2 * h)
        if pv.any():
            i = int(np.flatnonzero(pv)[np.argmin(J[STV][pv])])
            k = int(STV[i])
            upd(trk, "stiff", J, t, k)
            if J[k] < JCRIT and trk["stiff_first_below"] is None:
                trk["stiff_first_below"] = rec(J, t, k)
        if EDGE.size:
            k = int(EDGE[np.argmin(J[EDGE])])
            upd(trk, "edge", J, t, k)
            if J[k] <= 0 and trk["edge_first_fold"] is None:
                trk["edge_first_fold"] = rec(J, t, k)
        if GRADED.size:
            k = int(GRADED[np.argmin(J[GRADED])])
            upd(trk, "graded", J, t, k)
        if AXL.size:
            for ch, msk in (("soft", soft[AXL]), ("stiff", stiff[AXL])):
                if msk.any():
                    k = int(AXL[msk][np.argmin(J[AXL[msk]])])
                    upd(trk["axis"], ch, J, t, k)
            k = int(AXL[np.argmin(J[AXL])])
            if J[k] < JCRIT and trk["axis"]["first_below"] is None:
                trk["axis"]["first_below"] = rec(J, t, k)
    if t >= trk["next_series"] - 1e-9:
        c0, i0 = trk["iters_mark"]
        dc = sim.ncalls - c0
        row = {"t": round(float(t), 4), "xmax": float(sim.hold.last_xmax),
               "iters_per_call": (sim.iters_total - i0) / dc if dc else None, "lost_mass": float(sim.lost_mass),
               "omega_max": float(sim.omega_max())}
        if kind == "enc":
            pv = in_fine_valid(X[SV], Y[SV], Z[SV], 2 * h)
            row["S_now"] = float(J[SV][pv].min()) if pv.any() else None
        if kind in ("static", "vcm", "wake"):
            row["absJm1_out_now"] = float(np.abs(J[SEL_OUT] - 1).max())
            if args.a1 or args.a2:                           # AMENDMENTS A1 / A2: where the maximum sits
                k = int(SEL_OUT[np.argmax(np.abs(J[SEL_OUT] - 1))])
                pg = gal_state(t)[0][2]
                row["max_at"] = {"label": [float(qx[k]), float(qy[k]), float(qz[k])],
                                 "pos": [float(X[k]), float(Y[k]), float(Z[k])],
                                 "rel_mass": [float(X[k] - pg[0]), float(Y[k] - pg[1]), float(Z[k] - pg[2])],
                                 "J": float(J[k])}
        for key, w in trk["wake"].items():
            row[f"{key}_min_so_far"] = w["min_full"]["J"] if w["min_full"] else None
        trk["series"].append(row)
        trk["iters_mark"] = (sim.ncalls, sim.iters_total)
        trk["next_series"] += 0.1 if kind == "enc" else 0.25


def checkpoint():
    st = {"m": sim.m, "m_node": m_node, "Xi_int": sim.hold.Xi_int, "Xi_prev": sim.hold.Xi_prev, "Xi_full": sim.Xi_full,
          "rho_abs": sim._rho_abs, "X": sim.X, "V": sim.V, "A": sim.A, "t": sim.t, "flags": sim.flags,
          "ncalls": sim.ncalls, "iters_total": sim.iters_total, "xmax_seen": sim.xmax_seen, "step": step, "dt0": dt0,
          "meta": meta, "trk": trk, "cls": cls, "dt_state": (dt_now, dt_min_seen, F4, next_sample, fp_peak)}
    tmp = CKPT.with_suffix(".tmp")
    tmp.write_bytes(pickle.dumps(st, protocol=4))
    os.replace(tmp, CKPT)


CFL = 0.15 / (2.0 if (args.dt_half or args.a2 == "dt") else 1.0)
if step == 0:
    sample(t_i, sim.jacobian(((0, LSH[0]), (0, LSH[1]), (0, LSH[2]))))
    dt_now, dt_min_seen, F4, fp_peak = dt0, dt0, None, 0.0
    next_sample = t_i + 0.02
else:
    dt_now, dt_min_seen, F4, next_sample, fp_peak = st["dt_state"]
last_ck = time.time()
FULLBLOCK = ((0, LSH[0]), (0, LSH[1]), (0, LSH[2]))
while sim.t < t_stop - 1e-12:
    om = sim.omega_max()
    dt_now = min(dt0, CFL / om) if om > 0 else dt0
    if dt_now < dt0 / 50.0:
        dt_now = dt0 / 50.0
        if F4 is None:
            F4 = sim.t
            log(f"  F4 time-step floor reached at t {sim.t:.4f} (omega_max {om:.2f})")
    dt_now = min(dt_now, t_stop - sim.t + 1e-12)
    dt_min_seen = min(dt_min_seen, dt_now)
    sim.step(dt_now)
    step += 1
    if sim.t >= next_sample - 1e-9 or sim.t >= t_stop - 1e-12:
        sample(sim.t, sim.jacobian(FULLBLOCK))
        next_sample += 0.02
    if step % 200 == 0:
        fp_peak = max(fp_peak, footprint_gb())
        so = trk["soft"]["S"]["J"] if kind == "enc" and trk["soft"]["S"] else None
        log(f"  step {step} t {sim.t:.3f} dt {dt_now:.5f} S {so} iters/call {sim.iters_total / max(sim.ncalls, 1):.2f} "
            f"xmax {sim.xmax_seen:.3f} rss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB footprint "
            f"{fp_peak:.2f} GB; {(time.time() - T_WALL0) / 60:.1f} min")
    now = time.time()
    if now - last_ck > 600:
        checkpoint()
        last_ck = now
    if STOP["flag"] or now - T_WALL0 > args.maxwall * 60:
        checkpoint()
        log(f"  CHECKPOINT at t {sim.t:.4f} step {step} ({'SIGTERM' if STOP['flag'] else 'wall guard'})")
        sys.exit(3)


def clean(d):
    if isinstance(d, dict):
        return {k: clean(v) for k, v in d.items() if k not in ("start", "sv_start")}
    return d


out = dict(meta)
out.update({"soft": clean(trk["soft"]) if kind == "enc" else None, "wake": clean(trk["wake"]),
            "D_STIFF": trk["stiff"], "D_STIFF_first_below": trk["stiff_first_below"],
            "D_EDGE": {"min": trk["edge"], "first_fold": trk["edge_first_fold"]}, "D_GRADED": trk["graded"],
            "D_AXIS": trk["axis"], "D_FOLLOW": trk["dfollow"], "vstat": trk["vstat"],
            "flags": dict(sim.flags, F4=F4), "dt_min_seen": dt_min_seen, "xmax_seen": sim.xmax_seen,
            "hold_calls": sim.ncalls, "hold_iters_per_call": sim.iters_total / max(sim.ncalls, 1), "steps": step,
            "series": trk["series"], "peak_footprint_GB_sampled": max(fp_peak, footprint_gb()),
            "peak_rss_GB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9})
(RUNS / f"{tag}.json").write_text(json.dumps(out, indent=1, default=float))
if CKPT.exists():
    CKPT.unlink()
ev = trk["soft"]["event"] if kind == "enc" else None
log(f"DONE {tag}: soft event {ev['t'] if ev else None}; wake events "
    f"{ {k: (w['event']['t'] if w['event'] else None) for k, w in trk['wake'].items()} }; vstat {trk['vstat']}; "
    f"flags {sim.flags} F4 {F4}; wall {(time.time() - T_WALL0) / 60:.1f} min (this segment)")
