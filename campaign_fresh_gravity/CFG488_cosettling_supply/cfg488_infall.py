#!/usr/bin/env python3
"""CFG488 infall worker: one spherical secondary-infall run (CFG118's machinery, copied; CFG118's shellcore.c compiled
read-only into a temporary directory) and its co-settling products. Imported by cfg488_cosettling.py for its constants
(no side effects on import); run as a script by it, one process per run:

    python3 cfg488_infall.py '<spec json>' <output json path>

H-N ("HN"): CFG118's point core in Planck18 LCDM, cold shells at Omega_c rho_crit(z_i), other baryons smooth.
H-B ("HB"): CFG118's C2 configuration, Einstein-de Sitter, one collisionless background, point seed, read at a = 1.
CFG488_MUTATE=1 doubles Omega_c/Omega_b at fixed Omega_m (shell composition and smooth baryons).
"""
import os
import sys
import math
import json
import time
import hashlib
import tempfile
import subprocess
import ctypes
from ctypes import c_int32, c_int64, c_double, POINTER

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.dirname(HERE)
SHELLCORE = os.path.join(CFGDIR, "CFG118_secondary_infall", "shellcore.c")
MUT = os.environ.get("CFG488_MUTATE", "0") == "1"

SHARE_TRUE = 5.364
SHARE = 2.0 * SHARE_TRUE if MUT else SHARE_TRUE
FB = 1.0 / (1.0 + SHARE)
G = 4.30091727e-6                                   # kpc (km/s)^2 / Msun (CFG118 / CFG44 Bcommon)
KPC_M = 3.0856775814913673e19
H0 = 67.4 / 1000.0                                  # km/s/kpc
OM, OL = 0.315, 0.685
OB = OM * FB
OC = OM - OB
RHOC0 = 3.0 * H0 ** 2 / (8.0 * math.pi * G)
ZI = 100.0
A0_SI = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}   # = CFG4_common.A0 (checked by the main script)
A0K = {f: A0_SI[f] * KPC_M / 1e6 for f in A0_SI}
M_SIM = 1e10
QS = (0.05, 0.1, 0.2)
NS, NS_RES = 20000, 5000
ETA, ETAH = 0.01, 3e-4
KMAX, KF = 40, 18
SOFT_FRAC = 1e-3
TAU_MIN, TAU_PER_DEC, TAU_FRAC = 1e-5, 60, 0.9
LE = np.round(np.arange(-4.0, math.log10(3.0) + 1e-9, 0.025), 10)
EDGES_TA = 10.0 ** LE                               # radial edges in units of the run's r_ta0 (0.025 dex)


class Params(ctypes.Structure):
    _fields_ = [("eds", c_int32), ("H0", c_double), ("Om", c_double), ("OL", c_double), ("fsm", c_double), ("G", c_double),
                ("core", c_int32), ("Mb", c_double), ("eps", c_double), ("h", c_double), ("N", c_int32), ("m", c_double),
                ("q", c_double), ("t0", c_double), ("t1", c_double), ("kmax", c_int32), ("kf", c_int32), ("eta", c_double),
                ("etaH", c_double), ("nsnap", c_int32)]


class Stats(ctypes.Structure):
    _fields_ = [("nticks", c_int64), ("nkicks", c_int64), ("nslowticks", c_int64), ("nfloor", c_int64), ("nrefl", c_int64),
                ("nlazy", c_int64), ("nfallback", c_int64), ("nturn", c_int64), ("njfb", c_int64), ("maxD", c_double)]


def build_lib():
    tmp = tempfile.mkdtemp(prefix="cfg488_")
    so = os.path.join(tmp, "libshellcore.so")
    subprocess.run(["cc", "-O3", "-shared", "-fPIC", "-o", so, SHELLCORE, "-lm"], check=True, capture_output=True)
    L = ctypes.CDLL(so)
    dp = POINTER(c_double)
    L.run_shells.restype = c_int32
    L.run_shells.argtypes = [POINTER(Params), dp, dp, dp, dp, dp, dp, dp, dp, dp, dp, POINTER(c_int32), POINTER(Stats)]
    return L


def integrate(L, Pp, r0, v0, tsnap):
    N = Pp.N
    snap = np.zeros((len(tsnap), N))
    ro, vo, j2, tta, rta, rp1 = (np.zeros(N) for _ in range(6))
    npe = np.zeros(N, np.int32)
    S = Stats()
    f = lambda x: x.ctypes.data_as(POINTER(c_double))
    r0 = np.ascontiguousarray(r0, float); v0 = np.ascontiguousarray(v0, float); ts = np.ascontiguousarray(tsnap, float)
    rc = L.run_shells(ctypes.byref(Pp), f(r0), f(v0), f(ts), f(snap), f(ro), f(vo), f(j2), f(tta), f(rta), f(rp1),
                      npe.ctypes.data_as(POINTER(c_int32)), ctypes.byref(S))
    if rc != len(tsnap):
        raise RuntimeError(f"integrator returned {rc}")
    return dict(r=ro, v=vo, t_ta=tta, r_ta=rta, snap=snap), {k: getattr(S, k) for k, _ in Stats._fields_}


def t_of_a(a, eds=False):
    if eds:
        return 2.0 / (3.0 * H0) * a ** 1.5
    return 2.0 / (3.0 * H0 * math.sqrt(OL)) * math.asinh(math.sqrt(OL / OM) * a ** 1.5)


def a_of_t(t, eds=False):
    if eds:
        return (1.5 * H0 * t) ** (2.0 / 3.0)
    return (OM / OL) ** (1.0 / 3.0) * math.sinh(1.5 * math.sqrt(OL) * H0 * t) ** (2.0 / 3.0)


def cosmo(kind):
    """(eds, Om, OL, smooth density parameter, density parameter carried by the shells)."""
    if kind == "EdS":
        return 1, 1.0, 0.0, 0.0, 1.0
    return 0, OM, OL, OB, OC


def Mcore(M, r, soft):
    r = np.asarray(r, float)
    return M * r ** 3 / (r * r + soft * soft) ** 1.5


def r_M_kpc(M, foot):
    return math.sqrt(G * M / A0K[foot])


def one_shell(ML, M, kind, t0, t1, rhoci, Hi, soft):
    eds, Om_, OL_, fsm, _ = cosmo(kind)
    r0 = (3.0 * ML / (4.0 * math.pi * rhoci)) ** (1.0 / 3.0)
    v0 = Hi * r0

    def rhs(t, y):
        a = a_of_t(t, eds == 1)
        return [y[1], -G * (float(Mcore(M, y[0], soft)) + ML) / y[0] ** 2 - 0.5 * fsm * H0 ** 2 / a ** 3 * y[0] + OL_ * H0 ** 2 * y[0]]

    ev = lambda t, y: y[1]
    ev.terminal, ev.direction = True, -1
    sol = solve_ivp(rhs, (t0, t1), [r0, v0], method="DOP853", rtol=1e-11, atol=[1e-13 * r0, 1e-13 * v0], events=ev)
    if len(sol.t_events[0]):
        return True, float(sol.y_events[0][0][0])
    return False, float(sol.y[0][-1])


def setup(M, kind):
    eds, Om_, OL_, fsm, ocold = cosmo(kind)
    ai = 1.0 / (1.0 + ZI)
    t0, t1 = t_of_a(ai, eds == 1), t_of_a(1.0, eds == 1)
    rhoci = ocold * RHOC0 * (1.0 + ZI) ** 3
    Hi = H0 * math.sqrt(Om_ / ai ** 3 + OL_)
    soft = SOFT_FRAC * r_M_kpc(M, "canonical")
    lo, hi = math.log(1e-2 * M), math.log(1e5 * M)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if one_shell(math.exp(mid), M, kind, t0, t1, rhoci, Hi, soft)[0]:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-11:
            break
    M_ta = math.exp(hi)
    r_ta0 = one_shell(M_ta, M, kind, t0, t1, rhoci, Hi, soft)[1]
    lo, hi = math.log(M_ta), math.log(1e4 * M_ta)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if one_shell(math.exp(mid), M, kind, t0, t1, rhoci, Hi, soft)[1] < 3.0 * r_ta0:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-11:
            break
    return dict(t0=t0, t1=t1, ai=ai, rhoci=rhoci, Hi=Hi, soft=soft, M_ta=M_ta, r_ta0=r_ta0, M_out=math.exp(0.5 * (lo + hi)))


def snapshot_taus(T):
    n = int(round(TAU_PER_DEC * math.log10(TAU_FRAC * T / TAU_MIN)))
    return np.concatenate([[0.0], np.geomspace(TAU_MIN, TAU_FRAC * T, n + 1)])


def tavg_weights(taus, W):
    """c[b, s] with sum_s c[b,s] h_s = (1/W_b) int_0^W_b h(tau) dtau, h piecewise linear between snapshots (CFG118, copied)."""
    ns = len(taus)
    c = np.zeros((len(W), ns))
    for b, w in enumerate(W):
        k = int(np.searchsorted(taus, w, side="right")) - 1
        if k >= 1:
            d = np.diff(taus[:k + 1])
            c[b, :k] += 0.5 * d
            c[b, 1:k + 1] += 0.5 * d
        if k < ns - 1 and w > taus[k]:
            L = w - taus[k]
            f = L / (taus[k + 1] - taus[k])
            c[b, k] += 0.5 * L * (2.0 - f)
            c[b, k + 1] += 0.5 * L * f
        c[b] /= w
    return c


def zero_velocity_radius(r, v):
    o = np.argsort(r); rs, vs = r[o], v[o]
    k = np.where(vs <= 0)[0]
    if not len(k) or k[-1] + 1 >= len(rs):
        return float("nan")
    k = k[-1]
    return float(rs[k] + (rs[k + 1] - rs[k]) * (0.0 - vs[k]) / (vs[k + 1] - vs[k]))


def jsafe(o):
    if isinstance(o, dict):
        return {str(k): jsafe(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsafe(v) for v in o]
    if isinstance(o, np.ndarray):
        return jsafe(o.tolist())
    if isinstance(o, (np.floating, float)):
        return float(o) if np.isfinite(o) else None
    if isinstance(o, (np.integer,)):
        return int(o)
    return o


def run_sim(spec):
    """one infall run + its co-settling products: time-averaged bin masses (each bin over its own last dynamical time; the first bin holds everything inside its upper edge) and
    enclosed masses at the edges, for the eligible (R1), ineligible, R2-eligible and all cold shells, on EDGES_TA x r_ta0."""
    t_start = time.time()
    kind, q, N = spec["kind"], spec["q"], spec["N"]
    cos = "EdS" if kind == "HB" else "LCDM"
    su = setup(M_SIM, cos)
    eds, Om_, OL_, fsm, ocold = cosmo(cos)
    m = su["M_out"] / N
    Mk = m * (np.arange(N) + 0.5)
    r0 = (3.0 * Mk / (4.0 * math.pi * su["rhoci"])) ** (1.0 / 3.0)
    v0 = su["Hi"] * r0
    Pp = Params(eds, H0, Om_, OL_, fsm, G, 1, M_SIM, su["soft"], 1.0, N, m, q, su["t0"], su["t1"], KMAX, KF, ETA, ETAH, 0)
    T = su["t1"] - su["t0"]
    taus = snapshot_taus(T)
    tsnap = (su["t1"] - taus)[::-1].copy()
    tsnap[-1] = su["t1"]
    Pp.nsnap = len(tsnap)
    out, stats = integrate(build_lib(), Pp, r0, v0, tsnap)
    snap = out["snap"][::-1]                                         # row 0 = z = 0, ascending lookback
    # eligibility (R1, inner-first) by cumulative BARYON content, fractional boundary shell
    if kind == "HN":
        bshell = m * OB / OC                                         # the baryons that came with each cold shell
        cold_frac = 1.0
    else:                                                            # H-B: the shells are total matter in the cosmic ratio
        bshell = m * FB
        cold_frac = 1.0 - FB
    w_el = np.clip((M_SIM - bshell * np.arange(N)) / bshell, 0.0, 1.0)
    turned = np.isfinite(out["t_ta"])
    f_r = M_SIM / (bshell * turned.sum())                            # R2: one fraction of every turned shell's baryons
    W_SETS = {"elig": w_el * cold_frac, "inelig": (1.0 - w_el) * cold_frac, "r2": np.where(turned, f_r, 0.0) * cold_frac,
              "all": np.full(N, cold_frac)}
    r_ta0 = su["r_ta0"]
    e = EDGES_TA * r_ta0
    rc = np.sqrt(e[1:] * e[:-1])
    z0 = np.sort(snap[0])

    def window(rr):
        Mt = Mcore(M_SIM, rr, su["soft"]) + m * np.searchsorted(z0, rr)
        rhob = Mt / (4.0 * math.pi / 3.0 * rr ** 3)
        return np.minimum(np.sqrt(3.0 * math.pi / (16.0 * G * rhob)), taus[-1])

    cB = tavg_weights(taus, window(rc))
    cE = tavg_weights(taus, window(e))
    live = np.where(cB.any(axis=0) | cE.any(axis=0))[0]
    prod = {k: {"dM": np.zeros(len(rc)), "Menc": np.zeros(len(e))} for k in W_SETS}
    for s in live:
        rs = snap[s]
        bi = np.maximum(np.searchsorted(e, rs, side="right") - 1, 0)   # the first bin also holds r < e[0]
        ok = bi < len(rc)
        o = np.argsort(rs)
        pos = np.searchsorted(rs[o], e)
        for k, w in W_SETS.items():
            if cB[:, s].any():
                prod[k]["dM"] += cB[:, s] * m * np.bincount(bi[ok], weights=w[ok], minlength=len(rc))
            if cE[:, s].any():
                cw = np.concatenate([[0.0], np.cumsum(w[o])])
                prod[k]["Menc"] += cE[:, s] * m * cw[pos]
    # G9 row: the eligible boundary shell (the last shell with w_el > 0) and its time-averaged radius at z = 0
    kb = int(np.max(np.where(w_el > 0)[0]))
    Wb = float(window(np.array([max(snap[0][kb], 1e-9)]))[0])
    cb = tavg_weights(taus, np.array([Wb]))[0]
    rbar = float(np.sum(cb * snap[:, kb]))
    Mtot_rbar = float(Mcore(M_SIM, rbar, su["soft"]) + m * np.searchsorted(z0, rbar))
    rta_meas = zero_velocity_radius(out["r"], out["v"])
    cold_in_rta = float(m * cold_frac * np.searchsorted(z0, rta_meas)) if np.isfinite(rta_meas) else float("nan")
    res = dict(spec=spec, setup=su, m=m, N=N, r_ta_meas=rta_meas, cold_in_rta=cold_in_rta, n_turned=int(turned.sum()),
               f_r2=f_r, elig_total=float(np.sum(W_SETS["elig"]) * m), bshell=bshell, kb=kb, rbar_b=rbar,
               Mtot_rbar=Mtot_rbar, stats=stats, seconds=time.time() - t_start,
               prod={k: {kk: vv.tolist() for kk, vv in d.items()} for k, d in prod.items()})
    return jsafe(res)


def config_hash():
    h = hashlib.sha256()
    h.update(open(SHELLCORE, "rb").read())
    h.update(open(os.path.abspath(__file__), "rb").read())
    return h.hexdigest()[:16]


if __name__ == "__main__":
    spec = json.loads(sys.argv[1])
    try:
        os.nice(10)
    except OSError:
        pass
    json.dump(run_sim(spec), open(sys.argv[2], "w"))
