#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG118 -- Door 6: spherical secondary infall of a cold fluid onto a baryon core (shell crossing), against CFG44's target
C(r) = rho_c r^3 g_tot = (a0/4 pi) M_b(<r).

Frozen criteria: ../CFG118_FROZEN_CRITERIA.md (committed in b09ca1480 before this script); shared gates G1-G5 in
../closure_map/TEN_DOORS_GATES_2026-09-29.md.  The menu of doors was written knowing the target.

THE SIMULATION (as frozen; the numerical choices marked [declared] were fixed before any H1 number was seen)
  * 1-D spherical Lagrangian shell code (shellcore.c, compiled at run time into a temporary directory): N_s = 20,000 cold
    shells (5,000 for C3), Newtonian gravity in physical coordinates, each shell feels
        -G [M_b(<r) + M_c(<r)] / r^2 + (Lambda c^2/3) r + j^2/r^3   (+ the smooth background, below);
    enclosed masses exact at every kick (every shell drifted and re-sorted at every multiple of the level-17 step, the fast
    tier at every tick, slow shells counted at their exact positions; see shellcore.c); shells cross freely; a shell feels
    half its own mass.
  * Planck18 background: H0 = 67.4, Omega_m = 0.315, Omega_L = 0.685, Omega_b/Omega_m = 0.157 (Omega_c = 0.2655).
    [declared reading] The cold shells carry Omega_c only; the rest of the cosmic baryons (Omega_b, outside the core) are a
    smooth, non-clustering background on the Hubble flow.  Without it C1 cannot hold: cold shells at Omega_c moving with
    Planck18's H(z) would be a 16% under-density at z = 100 and leave the Hubble flow by far more than 1e-6.
  * Initial conditions (Bertschinger): at z_i = 100 the shells are uniformly spaced in enclosed cold mass at Omega_c
    rho_crit(z_i), on the Hubble flow, out to the Lagrangian mass whose shell sits at 3 r_ta(z = 0) at z = 0 (r_ta(z=0) and
    that mass from the exact single-shell orbit before crossing, with the core and background included).
  * The baryon core, static in physical coordinates from z_i: a point mass (Plummer-softened at 1e-3 r_M, canonical r_M)
    or CFG44's exponential sphere, h = 2, 3, 4, 5 kpc for M_b = 1e9, 1e10, 1e11, 1e12 Msun.
  * Angular momentum: radial until a shell first reaches maximum radius; there
        j^2 = 2 [Phi(r_ta) - Phi(q r_ta)] / ((q r_ta)^-2 - r_ta^-2),
    the energy/pericentre relation for apocentre r_ta and pericentre q r_ta in the potential of the mass enclosed at that
    moment (shells inside r_ta at their current radii, the core, the smooth background, Lambda), q = 0.05, 0.1, 0.2, the same
    at every mass; all three reported, with the realised first-pericentre ratios.  (A first version used the point-mass form
    j^2 = 2 G M(<r_ta) r_ta q/(1+q); in a timing run its realised first pericentres were ~2q, so it was replaced before any
    H1 number was computed.)
  * Integrator [declared]: kick-drift-kick leapfrog with individual power-of-two steps, step = min(eta t_loc, eta_H/H(t)),
    t_loc = min(sqrt(r/g_pull), r/|v|, r^2/j), eta = 0.01, eta_H = 3e-4; 2^40 ticks over z = 100..0.
  * Density at z = 0 [declared]: shells binned in log r (0.1 dex); each bin time-averaged over the last local dynamical
    time t_dyn(r) = sqrt(3 pi/(16 G rho_bar(<r))) (Binney & Tremaine's; rho_bar from M_b + M_c at z = 0), capped at 0.9 of the
    run; snapshots at lookback 0 and 60 per decade from 1e-5 to 0.9 of the run (piecewise-linear time quadrature).

EVALUATION
  C_X,b = (Delta M_X,b / V_b) r_b^3 G [M_b(<r_b) + M_c,X(<r_b)] / r_b^2 for X = simulation and target (the same binned estimator
  for both; r_b the geometric bin centre); ratio = C_sim/C_target on 25 bins of 0.1 dex, x = r/r_M from 0.1 to 31.6
  (r_M = sqrt(G M_b/a0)), on both footings: a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt).
  C1 CONTROL: no core: every shell on the Planck18 Hubble flow to 1e-6 relative at z = 0 (position and velocity).
  C2 CONTROL: Einstein-de Sitter, Lambda = 0, a single collisionless background (all matter in the shells, Bertschinger's set-up),
    q = 0.05, a point seed of 1e10 Msun: the least-squares log-slope of the inner profile over the self-similar range
    [declared: r/r_ta(z=0) in [0.03, 0.15], r_ta the measured zero-velocity radius] is -9/4 +- 0.15.
  C3 CONTROL: 5,000 vs 20,000 shells, every mass/geometry/bracket, both footings: |ratio_5k/ratio_20k - 1| <= 0.10 on bins with
    centres in x in [0.3, 30].
  H1 [HEADLINE]: on each footing, for at least one bracket q: |ratio - 1| <= 0.10 on every bin with centre in [0.1, 30] for every
    mass and both geometries.  H1 passes only if it passes on both footings.
  R1 ratio curves, largest deviation, the x range within 10% (plus a shell-bootstrap discreteness indicator, reported only).
  R2 the radius where the log-slope of rho_c is -2 (5-bin sliding least squares on the 0.1-dex profile, first downward crossing
     outward from x = 0.1) against M_b: fitted exponent, against r_M ~ M^(1/2) and the turnaround ~ M^(1/3).
  R3 G2-G5 as statements.
POST-HOC (added after the first full run showed C3 failing; reported only, no frozen verdict depends on them): where C3 fails
  (local bins against the cumulative cold mass), H1 on the 5,000-shell runs, the cumulative cold mass against the target's, and an
  R2 cross-check with the radius where M_c(<r) = M_b.
MUTATE=1: G1 (H1 and R1) is evaluated on the target's own binned rho_c and M_c in place of the simulated ones; H1 must then pass.
The simulations are unchanged by MUTATE (a MUTATE run reuses the main run's cached simulation products when their hash matches).
Run: python3 CFG118_secondary_infall.py ; MUTATE=1 python3 CFG118_secondary_infall.py   (CFG118_NPROC sets the process count)
"""
import os
import sys
import math
import json
import time
import hashlib
import inspect
import shutil
import tempfile
import subprocess
import ctypes
from ctypes import c_int32, c_int64, c_double, POINTER

sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import gammainc

HERE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.dirname(HERE)
sys.path.insert(0, CFGDIR)
sys.path.insert(0, os.path.join(CFGDIR, "CFG44_fluid_target"))
import CFG7_common as C                                                                  # Report (read-only import)
from Bcommon import G, KPC_M, exp_sphere, point_mass, target_fields                     # the CFG44 target (read-only import)

SLUG = "CFG118_secondary_infall"
MUTATE = os.environ.get("MUTATE", "0") == "1"

# ------------------------------------------------------------------------------------------------ constants (declared)
H0 = 67.4 / 1000.0                          # km/s/kpc
OM, OL, FB = 0.315, 0.685, 0.157
OC, OB = OM * (1.0 - FB), OM * FB
RHOC0 = 3.0 * H0 ** 2 / (8.0 * math.pi * G)  # Msun/kpc^3
ZI = 100.0
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
assert A0_SI == C.A0_SI
FOOTS = ("canonical", "alt")
A0K = {f: A0_SI[f] * KPC_M / 1e6 for f in FOOTS}            # (km/s)^2/kpc
MASSES = (1e9, 1e10, 1e11, 1e12)
HEXP = {1e9: 2.0, 1e10: 3.0, 1e11: 4.0, 1e12: 5.0}
GEOMS = ("point", "exp")
QS = (0.05, 0.1, 0.2)
NS, NS_C3 = 20000, 5000
ETA, ETAH = 0.01, 3e-4
KMAX, KF = 40, 18
SOFT_FRAC = 1e-3
XB_EDGES = 10.0 ** np.round(np.arange(-1.0, 1.5001, 0.1), 10)    # 25 G1 bins, x = 0.1 .. 31.6
GEN_EDGES = 10.0 ** np.round(np.arange(-2.0, 3.5001, 0.1), 10)   # generic profile grid in units of the canonical r_M
G1_LO, G1_HI, C3_LO = 0.1, 30.0, 0.3
C2_RANGE = (0.03, 0.15)
TAU_MIN, TAU_PER_DEC, TAU_FRAC = 1e-5, 60, 0.9
NBOOT = 200
GYR = 3.0856775814913673e16 / 3.15576e16                          # 1 kpc/(km/s) in Gyr (0.9778)

SIM_CONFIG = dict(H0=H0, OM=OM, OL=OL, FB=FB, ZI=ZI, MASSES=MASSES, HEXP=[HEXP[m] for m in MASSES], QS=QS, NS=NS, NS_C3=NS_C3,
                  ETA=ETA, ETAH=ETAH, KMAX=KMAX, KF=KF, SOFT_FRAC=SOFT_FRAC, XB=XB_EDGES.tolist(), GEN=GEN_EDGES.tolist(),
                  C2_RANGE=C2_RANGE, TAU=(TAU_MIN, TAU_PER_DEC, TAU_FRAC), NBOOT=NBOOT, A0=A0_SI)


def r_M(M, foot="canonical"):
    return math.sqrt(G * M / A0K[foot])


# ------------------------------------------------------------------------------------------------ the C integrator
class Params(ctypes.Structure):
    _fields_ = [("eds", c_int32), ("H0", c_double), ("Om", c_double), ("OL", c_double), ("fsm", c_double), ("G", c_double),
                ("core", c_int32), ("Mb", c_double), ("eps", c_double), ("h", c_double), ("N", c_int32), ("m", c_double),
                ("q", c_double), ("t0", c_double), ("t1", c_double), ("kmax", c_int32), ("kf", c_int32), ("eta", c_double),
                ("etaH", c_double), ("nsnap", c_int32)]


class Stats(ctypes.Structure):
    _fields_ = [("nticks", c_int64), ("nkicks", c_int64), ("nslowticks", c_int64), ("nfloor", c_int64), ("nrefl", c_int64),
                ("nlazy", c_int64), ("nfallback", c_int64), ("nturn", c_int64), ("njfb", c_int64), ("maxD", c_double)]


def build_lib():
    """compile shellcore.c into a fresh temporary directory (nothing is written into the repository)."""
    tmp = tempfile.mkdtemp(prefix="cfg118_")
    so = os.path.join(tmp, "libshellcore.so")
    cmd = ["cc", "-O3", "-shared", "-fPIC", "-o", so, os.path.join(HERE, "shellcore.c"), "-lm"]
    subprocess.run(cmd, check=True, capture_output=True)
    return tmp, so


_LIB = {}


def lib(so):
    if so not in _LIB:
        L = ctypes.CDLL(so)
        dp = POINTER(c_double)
        L.run_shells.restype = c_int32
        L.run_shells.argtypes = [POINTER(Params), dp, dp, dp, dp, dp, dp, dp, dp, dp, dp, POINTER(c_int32), POINTER(Stats)]
        _LIB[so] = L
    return _LIB[so]


def integrate(so, P, r0, v0, tsnap):
    N = P.N
    snap = np.zeros((len(tsnap), N))
    ro, vo, j2, tta, rta, rp1 = (np.zeros(N) for _ in range(6))
    npe = np.zeros(N, np.int32)
    S = Stats()
    f = lambda x: x.ctypes.data_as(POINTER(c_double))
    r0 = np.ascontiguousarray(r0, float); v0 = np.ascontiguousarray(v0, float); ts = np.ascontiguousarray(tsnap, float)
    rc = lib(so).run_shells(ctypes.byref(P), f(r0), f(v0), f(ts), f(snap), f(ro), f(vo), f(j2), f(tta), f(rta), f(rp1),
                            npe.ctypes.data_as(POINTER(c_int32)), ctypes.byref(S))
    if rc != len(tsnap):
        raise RuntimeError(f"integrator returned {rc} (expected {len(tsnap)} snapshots)")
    stats = {k: getattr(S, k) for k, _ in Stats._fields_}
    return dict(r=ro, v=vo, j2=j2, t_ta=tta, r_ta=rta, r_p1=rp1, nperi=npe, snap=snap), stats


# ------------------------------------------------------------------------------------------------ background and cores
def t_of_a(a, eds=False):
    if eds:
        return 2.0 / (3.0 * H0) * a ** 1.5
    return 2.0 / (3.0 * H0 * math.sqrt(OL)) * math.asinh(math.sqrt(OL / OM) * a ** 1.5)


def a_of_t(t, eds=False):
    if eds:
        return (1.5 * H0 * t) ** (2.0 / 3.0)
    return (OM / OL) ** (1.0 / 3.0) * math.sinh(1.5 * math.sqrt(OL) * H0 * t) ** (2.0 / 3.0)


def cosmo(kind):
    """(eds flag, Om, OL, f_smooth, cold density parameter carried by the shells)."""
    if kind == "EdS":
        return 1, 1.0, 0.0, 0.0, 1.0            # Bertschinger's single collisionless background
    return 0, OM, OL, OB, OC                    # Planck18: shells carry Omega_c, the other baryons a smooth background


def Mb_enc(M, geom, r, soft=None):
    """baryon mass inside r (Msun); soft != None gives the Plummer-softened point mass the integrator uses."""
    r = np.asarray(r, float)
    if geom == "point":
        if soft is None:
            return M * np.ones_like(r)
        return M * r ** 3 / (r * r + soft * soft) ** 1.5
    if geom == "exp":
        return M * gammainc(3.0, r / HEXP[M])
    return np.zeros_like(r)


def one_shell(ML, M, geom, kind, t0, t1, rhoci, Hi, soft):
    """exact orbit of one shell of Lagrangian cold mass ML before any crossing; returns (turned before t1?, r(t1 or t_ta), v)."""
    eds, Om_, OL_, fsm, _ = cosmo(kind)
    r0 = (3.0 * ML / (4.0 * math.pi * rhoci)) ** (1.0 / 3.0)
    v0 = Hi * r0

    def rhs(t, y):
        a = a_of_t(t, eds == 1)
        Mb = float(Mb_enc(M, geom, y[0], soft)) if geom else 0.0
        return [y[1], -G * (Mb + ML) / y[0] ** 2 - 0.5 * fsm * H0 ** 2 / a ** 3 * y[0] + OL_ * H0 ** 2 * y[0]]

    ev = lambda t, y: y[1]
    ev.terminal, ev.direction = True, -1
    sol = solve_ivp(rhs, (t0, t1), [r0, v0], method="DOP853", rtol=1e-11, atol=[1e-13 * r0, 1e-13 * v0], events=ev)
    if len(sol.t_events[0]):
        return True, float(sol.y_events[0][0][0]), 0.0
    return False, float(sol.y[0][-1]), float(sol.y[1][-1])


def setup(M, geom, kind):
    """the z = 0 turnaround shell (its Lagrangian mass and radius) and the Lagrangian mass whose shell is at 3 r_ta(z=0)."""
    eds, Om_, OL_, fsm, ocold = cosmo(kind)
    ai = 1.0 / (1.0 + ZI)
    t0, t1 = t_of_a(ai, eds == 1), t_of_a(1.0, eds == 1)
    rhoci = ocold * RHOC0 * (1.0 + ZI) ** 3
    Hi = H0 * math.sqrt(Om_ / ai ** 3 + OL_)
    soft = SOFT_FRAC * r_M(M) if geom == "point" else None
    lo, hi = math.log(1e-2 * M), math.log(1e5 * M)
    assert one_shell(math.exp(lo), M, geom, kind, t0, t1, rhoci, Hi, soft)[0]
    assert not one_shell(math.exp(hi), M, geom, kind, t0, t1, rhoci, Hi, soft)[0]
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if one_shell(math.exp(mid), M, geom, kind, t0, t1, rhoci, Hi, soft)[0]:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-11:
            break
    M_ta = math.exp(hi)
    r_ta0 = one_shell(M_ta, M, geom, kind, t0, t1, rhoci, Hi, soft)[1]
    lo, hi = math.log(M_ta), math.log(1e4 * M_ta)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if one_shell(math.exp(mid), M, geom, kind, t0, t1, rhoci, Hi, soft)[1] < 3.0 * r_ta0:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-11:
            break
    M_out = math.exp(0.5 * (lo + hi))
    return dict(t0=t0, t1=t1, ai=ai, rhoci=rhoci, Hi=Hi, soft=soft, M_ta=M_ta, r_ta0=r_ta0, M_out=M_out)


# ------------------------------------------------------------------------------------------------ analysis of one run
def snapshot_taus(T):
    n = int(round(TAU_PER_DEC * math.log10(TAU_FRAC * T / TAU_MIN)))
    return np.concatenate([[0.0], np.geomspace(TAU_MIN, TAU_FRAC * T, n + 1)])


def tavg_weights(taus, W):
    """c[b, s] with sum_s c[b,s] h_s = (1/W_b) int_0^W_b h(tau) dtau, h piecewise linear between the snapshots (taus ascending)."""
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


def binned(snap_s, m, edges, Mb_c, taus, want_shells=False):
    """time-averaged shell mass per bin and enclosed shell mass at the bin centres, each bin over its own last dynamical time.
    snap_s: snapshot radii ordered by ascending lookback (row 0 = z = 0)."""
    rc = np.sqrt(edges[1:] * edges[:-1])
    s0 = np.sort(snap_s[0])
    Mc0 = m * np.searchsorted(s0, rc)
    rhobar = (Mb_c + Mc0) / (4.0 * math.pi / 3.0 * rc ** 3)
    W = np.sqrt(3.0 * math.pi / (16.0 * G * rhobar))
    capped = W > taus[-1]
    W = np.minimum(W, taus[-1])
    c = tavg_weights(taus, W)
    live = np.where(c.any(axis=0))[0]
    dM = np.zeros(len(rc)); Mc = np.zeros(len(rc))
    N = snap_s.shape[1]
    O = np.zeros((len(rc), N)) if want_shells else None
    E = np.zeros((len(rc), N)) if want_shells else None
    idx = np.arange(N)
    for s in live:
        rs = snap_s[s]
        so = np.sort(rs)
        cnt = np.searchsorted(so, edges)
        dM += c[:, s] * m * np.diff(cnt)
        Mc += c[:, s] * m * np.searchsorted(so, rc)
        if want_shells:
            bi = np.searchsorted(edges, rs, side="right") - 1
            ok = (bi >= 0) & (bi < len(rc))
            O[bi[ok], idx[ok]] += c[bi[ok], s]
            E += c[:, s][:, None] * (rs[None, :] < rc[:, None])
    return dict(rc=rc, dM=dM, Mc=Mc, W=W, n_capped=int(capped.sum()), O=O, E=E)


def ratio_of(dM, Mc, dMT, McT, Mb_c):
    with np.errstate(divide="ignore", invalid="ignore"):
        return dM * (Mb_c + Mc) / (dMT * (Mb_c + McT))


def zero_velocity_radius(r, v):
    o = np.argsort(r); rs, vs = r[o], v[o]
    k = np.where(vs <= 0)[0]
    if not len(k) or k[-1] + 1 >= len(rs):
        return float("nan")
    k = k[-1]
    return float(rs[k] + (rs[k + 1] - rs[k]) * (0.0 - vs[k]) / (vs[k + 1] - vs[k]))


def run_one(job):
    """one simulation + its analysis (picklable dict in, dict of small arrays out)."""
    so, spec = job
    t_start = time.time()
    kind, M, geom, q, N = spec["kind"], spec["M"], spec["geom"], spec["q"], spec["N"]
    cos = "EdS" if kind == "C2" else "LCDM"
    if kind == "C1":                                                 # the 1e10 point configuration's shells, with no core
        su = setup(1e10, "point", "LCDM")
        su["soft"] = None
    else:
        su = setup(M, geom, cos)
    eds, Om_, OL_, fsm, ocold = cosmo(cos)
    m = su["M_out"] / N
    Mk = m * (np.arange(N) + 0.5)
    r0 = (3.0 * Mk / (4.0 * math.pi * su["rhoci"])) ** (1.0 / 3.0)
    v0 = su["Hi"] * r0
    core = 0 if kind == "C1" else (1 if geom == "point" else 2)
    P = Params(eds, H0, Om_, OL_, fsm, G, core, 0.0 if kind == "C1" else M, su["soft"] or 0.0, HEXP.get(M, 1.0), N, m, q,
               su["t0"], su["t1"], KMAX, KF, ETA, ETAH, 0)
    T = su["t1"] - su["t0"]
    taus = snapshot_taus(T)
    tsnap = (su["t1"] - taus)[::-1].copy()
    tsnap[-1] = su["t1"]
    P.nsnap = len(tsnap)
    out, stats = integrate(so, P, r0, v0, tsnap)
    snap_s = out["snap"][::-1]                                       # ascending lookback: row 0 = z = 0
    res = dict(spec=spec, setup={k: v for k, v in su.items()}, m=m, stats=stats, N=N)
    if kind == "C1":
        a1 = a_of_t(su["t1"])
        dr = out["r"] / (r0 * a1 / su["ai"]) - 1.0
        dv = out["v"] / (H0 * out["r"]) - 1.0
        res.update(c1_dr=float(np.abs(dr).max()), c1_dv=float(np.abs(dv).max()), n_turned=int(np.isfinite(out["r_ta"]).sum()))
        res["seconds"] = time.time() - t_start
        return res
    Mb_core = (lambda r: Mb_enc(M, geom, r))                         # unsoftened, as in the target
    rta_meas = zero_velocity_radius(out["r"], out["v"])
    turned = np.isfinite(out["r_ta"])
    peri = out["nperi"] >= 1
    pr = out["r_p1"][peri] / out["r_ta"][peri]
    res.update(r_ta_meas=rta_meas, n_turned=int(turned.sum()), n_peri=int(peri.sum()),
               peri_ratio=[float(np.percentile(pr, p)) for p in (16, 50, 84)] if peri.sum() > 10 else [float("nan")] * 3)
    # generic profile (units of the canonical r_M)
    rMc = r_M(M)
    ge = GEN_EDGES * rMc
    gb = binned(snap_s, m, ge, Mb_core(np.sqrt(ge[1:] * ge[:-1])), taus)
    res["gen"] = dict(rc=gb["rc"].tolist(), dM=gb["dM"].tolist(), Mc=gb["Mc"].tolist(), W=gb["W"].tolist(), n_capped=gb["n_capped"])
    if kind == "C2":
        res["seconds"] = time.time() - t_start
        return res
    # the G1 bins on both footings, with a shell-bootstrap discreteness indicator
    rng = np.random.default_rng(118)
    Wts = rng.multinomial(N, np.full(N, 1.0 / N), size=NBOOT).astype(float)
    res["foot"] = {}
    for f in FOOTS:
        e = XB_EDGES * r_M(M, f)
        rc = np.sqrt(e[1:] * e[:-1])
        Mbc = Mb_core(rc)
        b = binned(snap_s, m, e, Mbc, taus, want_shells=True)
        T_ = spec["target"][f]
        dMT, McT = np.array(T_["dM"]), np.array(T_["Mc"])
        rat = ratio_of(b["dM"], b["Mc"], dMT, McT, Mbc)
        bdM = m * np.einsum("bn,kn->bk", b["O"], Wts); bMc = m * np.einsum("bn,kn->bk", b["E"], Wts)
        brat = ratio_of(bdM, bMc, dMT[:, None], McT[:, None], Mbc[:, None])
        res["foot"][f] = dict(dM=b["dM"].tolist(), Mc=b["Mc"].tolist(), W=b["W"].tolist(), n_capped=b["n_capped"],
                              ratio=rat.tolist(), boot_sd=np.std(brat, axis=1).tolist(),
                              n_distinct=(b["O"] > 0).sum(axis=1).tolist(), mean_shells=(b["dM"] / m).tolist())
    res["seconds"] = time.time() - t_start
    return res


def kepler_test(job):
    """numerical diagnostic (reported): a test shell (m = 0) in the static softened 1e10 point mass, turnaround at 0.7 kpc (the
    innermost main-run shell's radius), for the whole run length; energy drift and the realised pericentre ratio per bracket."""
    so, q = job
    M, rta = 1e10, 0.7
    eps = SOFT_FRAC * r_M(M)
    t0, t1 = t_of_a(1.0 / (1.0 + ZI)), t_of_a(1.0)
    P = Params(1, H0, 1.0, 0.0, 0.0, G, 1, M, eps, 1.0, 1, 0.0, q, t0, t1, KMAX, KF, ETA, 1e300, 1)
    out, st = integrate(so, P, np.array([rta]), np.array([1e-9]), np.array([t1]))
    r, v, j2, ra = out["r"][0], out["v"][0], out["j2"][0], out["r_ta"][0]
    E0 = j2 / (2 * ra * ra) - G * M / math.sqrt(ra * ra + eps * eps)
    E1 = 0.5 * v * v + j2 / (2 * r * r) - G * M / math.sqrt(r * r + eps * eps)
    return dict(q=q, dE=(E1 - E0) / abs(E0), peri_ratio=out["r_p1"][0] / ra, nperi=int(out["nperi"][0]), kicks=st["nkicks"])


# ------------------------------------------------------------------------------------------------ the target on the G1 bins
_TB = {}


def target_binned(M, geom, foot):
    if (M, geom, foot) in _TB:
        return _TB[(M, geom, foot)]
    prof = point_mass(M) if geom == "point" else exp_sphere(M, HEXP[M])
    tf = target_fields(prof, a0=A0K[foot])
    lr, lw = np.log(tf["r"]), np.log(tf["w"])
    McT = lambda r: np.exp(np.interp(np.log(r), lr, lw)) / G
    e = XB_EDGES * r_M(M, foot)
    rc = np.sqrt(e[1:] * e[:-1])
    _TB[(M, geom, foot)] = dict(dM=np.diff(McT(e)).tolist(), Mc=McT(rc).tolist())
    return _TB[(M, geom, foot)]


def sim_hash():
    src = open(os.path.join(HERE, "shellcore.c")).read()
    fns = "".join(inspect.getsource(f) for f in (setup, one_shell, run_one, binned, tavg_weights, snapshot_taus, Mb_enc, cosmo,
                                                  ratio_of, zero_velocity_radius, kepler_test, target_binned))
    return hashlib.sha256((src + fns + json.dumps(SIM_CONFIG, sort_keys=True)).encode()).hexdigest()[:16]


def jsafe(o):
    if isinstance(o, dict):
        return {str(k): jsafe(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsafe(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return jsafe(o.tolist())
    return o


def fnum(x, fmt="{:.3g}"):
    return "nan" if x is None or not np.isfinite(x) else fmt.format(x)


# ------------------------------------------------------------------------------------------------ main
def simulate_all(R):
    tmp, so = build_lib()
    try:
        targets = {(M, g, f): target_binned(M, g, f) for M in MASSES for g in GEOMS for f in FOOTS}
        specs = []
        for N, kind in ((NS, "main"), (NS_C3, "C3")):
            for q in QS:
                for M in MASSES:
                    for g in GEOMS:
                        specs.append(dict(kind=kind, M=M, geom=g, q=q, N=N, target={f: targets[(M, g, f)] for f in FOOTS}))
        specs.append(dict(kind="C1", M=1e10, geom=None, q=0.05, N=NS))
        specs.append(dict(kind="C2", M=1e10, geom="point", q=0.05, N=NS))
        # longest first: point-mass cores at the smallest bracket and 20,000 shells
        specs.sort(key=lambda s: (s["N"] != NS, s["geom"] != "point", s["q"]))
        nproc = int(os.environ.get("CFG118_NPROC", "8"))
        import multiprocessing as mp
        R.P(f"  running {len(specs)} simulations + 3 test orbits on {nproc} processes ...")
        t0 = time.time()
        with mp.get_context("spawn").Pool(nproc) as pool:
            kep = pool.map(kepler_test, [(so, q) for q in QS])
            runs = []
            for i, res in enumerate(pool.imap_unordered(run_one, [(so, s) for s in specs])):
                s = res["spec"]
                R.P(f"    [{i + 1:2d}/{len(specs)}] {s['kind']:4s} M={s['M']:.0e} {str(s['geom']):5s} q={s['q']:.2f} N={s['N']:5d}: "
                    f"{res['seconds']:6.0f} s, {res['stats']['nkicks']:.3g} kicks, {res['stats']['nticks']:.3g} ticks   "
                    f"(elapsed {time.time() - t0:.0f} s)")
                runs.append(res)
        for r_ in runs:
            r_["spec"].pop("target", None)
        return dict(hash=sim_hash(), runs=runs, kepler=kep, wall=time.time() - t0, nproc=nproc)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    R = C.Report(SLUG, MUTATE)
    P = R.P
    P(__doc__.split("Run: python3")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: G1 is evaluated on the target's own rho_c and M_c in place of the simulated ones -- H1 must PASS ***")
    cache = os.path.join(HERE, SLUG + "_sims.json")
    h = sim_hash()
    sims = None
    if MUTATE and os.path.exists(cache):
        d = json.load(open(cache))
        if d.get("hash") == h:
            sims = d
            P(f"\n  simulation products reused from {os.path.basename(cache)} (hash {h}; the main run wrote them)")
    if sims is None:
        R.banner("SIMULATIONS")
        sims = jsafe(simulate_all(R))
        if not MUTATE:
            json.dump(sims, open(cache, "w"))
            P(f"  simulation products written to {os.path.basename(cache)} (hash {h})")
    runs = sims["runs"]
    get = lambda kind, M=None, g=None, q=None: [r for r in runs if r["spec"]["kind"] == kind and (M is None or r["spec"]["M"] == M)
                                                and (g is None or r["spec"]["geom"] == g) and (q is None or r["spec"]["q"] == q)]
    P(f"\n  simulation wall time {sims['wall'] / 60:.1f} min on {sims['nproc']} processes (machine shared and loaded)")

    # ------------------------------------------------------------------------------------------ set-up table
    R.banner("SET-UP: the z = 0 turnaround and the shell extent (exact single-shell orbits before crossing)")
    P(f"  {'M_b':>7s} {'core':5s} {'r_M can':>8s} {'r_M alt':>8s} {'M_ta/M_b':>9s} {'r_ta0 kpc':>10s} {'x_ta':>6s} {'M_out/M_b':>10s} "
      f"{'m/M_b':>8s} {'r_ta meas/pred (q=.05,.1,.2)':>30s}")
    for M in MASSES:
        for g in GEOMS:
            rr = get("main", M, g)
            su = rr[0]["setup"]
            meas = [get("main", M, g, q)[0]["r_ta_meas"] / su["r_ta0"] for q in QS]
            P(f"  {M:7.0e} {g:5s} {r_M(M):8.2f} {r_M(M, 'alt'):8.2f} {su['M_ta'] / M:9.2f} {su['r_ta0']:10.1f} {su['r_ta0'] / r_M(M):6.1f} "
              f"{su['M_out'] / M:10.1f} {rr[0]['m'] / M:8.4f} {', '.join(f'{x:.3f}' for x in meas):>30s}")
            R.num(f"setup_{M:.0e}_{g}", dict(M_ta=su["M_ta"], r_ta0=su["r_ta0"], M_out=su["M_out"], r_M_can=r_M(M), r_M_alt=r_M(M, "alt")))
    P("  (r_ta meas = the zero-velocity radius of the shells at z = 0; pred = the single-shell orbit.)")
    P("\n  realised first pericentre / turnaround radius (16/50/84 percentiles over the shells that reached a pericentre):")
    for q in QS:
        P(f"    q = {q:.2f}: " + "  ".join(f"{M:.0e}/{g} " + "/".join(fnum(x, '{:.3f}') for x in get('main', M, g, q)[0]['peri_ratio'])
                                     for M in MASSES for g in GEOMS))
    R.num("peri_ratio", {f"q={q}|{M:.0e}|{g}": get("main", M, g, q)[0]["peri_ratio"] for q in QS for M in MASSES for g in GEOMS})
    P("\n  per-run integrator counters (20,000 shells): kicks, ticks, slow ticks, step-floor hits, reflections, lazy checks, fallbacks")
    for q in QS:
        for M in MASSES:
            for g in GEOMS:
                s_ = get("main", M, g, q)[0]
                st = s_["stats"]
                P(f"    q={q:.2f} {M:6.0e} {g:5s}: {st['nkicks']:.3g} / {st['nticks']:.3g} / {st['nslowticks']:.3g} / {st['nfloor']} / "
                  f"{st['nrefl']} / {st['nlazy']:.3g} / {st['nfallback']}; turned {s_['n_turned']}, {s_['seconds']:.0f} s")

    # ------------------------------------------------------------------------------------------ C1
    R.banner("C1 CONTROL: no baryon core -- the shells follow the Planck18 Hubble flow to 1e-6 at z = 0")
    c1 = get("C1")[0]
    P(f"  N = {c1['N']}, extent M_out = {c1['setup']['M_out']:.4g} Msun; max |r/r_Hubble - 1| = {c1['c1_dr']:.3e}; "
      f"max |v/(H0 r) - 1| = {c1['c1_dv']:.3e}; shells that turned around: {c1['n_turned']}; {c1['stats']['nkicks']:.3g} kicks")
    R.num("C1", dict(dr=c1["c1_dr"], dv=c1["c1_dv"]))
    R.check("C1 CONTROL: no core, every shell on the Hubble flow to 1e-6 relative at z = 0 (position and velocity)",
            f"max |dr/r| = {c1['c1_dr']:.2e}, max |dv/v| = {c1['c1_dv']:.2e}", c1["c1_dr"] <= 1e-6 and c1["c1_dv"] <= 1e-6)

    # ------------------------------------------------------------------------------------------ numerical diagnostic
    R.banner("NUMERICAL DIAGNOSTIC (reported): the adaptive leapfrog on the most eccentric, most-orbited shell")
    for k_ in sims["kepler"]:
        P(f"  test shell in the static softened 1e10 point mass, turnaround 0.7 kpc, q = {k_['q']}: realised r_peri/r_ta = "
          f"{k_['peri_ratio']:.4f}, {k_['nperi']} pericentres, energy drift over the run {100 * k_['dE']:+.2f}%")
    R.num("kepler_test", sims["kepler"])
    worst = max(abs(k_["dE"]) for k_ in sims["kepler"])
    R.check("numerical: energy drift of the innermost-type orbit over ~2,000 orbits below 1% at eta = 0.01",
            f"worst |dE/E| = {100 * worst:.2f}% (q = 0.05 orbits are the worst)", worst < 0.01, load_bearing=False)

    # ------------------------------------------------------------------------------------------ C2
    R.banner("C2 CONTROL: Einstein-de Sitter, Lambda = 0, point seed, q = 0.05 -- Bertschinger's r^(-9/4)")
    c2 = get("C2")[0]
    gen = c2["gen"]
    rc = np.array(gen["rc"]); dM = np.array(gen["dM"])
    vol = 4 * math.pi / 3 * (np.array(GEN_EDGES[1:]) ** 3 - np.array(GEN_EDGES[:-1]) ** 3) * r_M(1e10) ** 3
    rho = dM / vol
    lam = rc / c2["r_ta_meas"]
    sel = (lam >= C2_RANGE[0]) & (lam <= C2_RANGE[1]) & (rho > 0)
    slope = float(np.polyfit(np.log(rc[sel]), np.log(rho[sel]), 1)[0]) if sel.sum() >= 3 else float("nan")
    loc = np.gradient(np.log(np.maximum(rho, 1e-300)), np.log(rc))
    P(f"  seed 1e10 Msun; measured r_ta(a=1) = {c2['r_ta_meas']:.1f} kpc (predicted {c2['setup']['r_ta0']:.1f}); "
      f"M_ta = {c2['setup']['M_ta'] / 1e10:.1f} seed masses")
    P(f"  realised first-pericentre ratio r_p1/r_ta (16/50/84%): {', '.join(fnum(x) for x in c2['peri_ratio'])}")
    P("  lambda = r/r_ta  " + "  ".join(f"{x:.3f}" for x in lam[sel]))
    P("  rho (Msun/kpc^3) " + "  ".join(f"{x:.3g}" for x in rho[sel]))
    P("  local slope      " + "  ".join(f"{x:+.2f}" for x in loc[sel]))
    P(f"  least-squares log-slope over lambda in [{C2_RANGE[0]}, {C2_RANGE[1]}] ({int(sel.sum())} bins): {slope:+.3f} (Bertschinger -2.250)")
    R.num("C2", dict(slope=slope, r_ta=c2["r_ta_meas"], lam=lam[sel].tolist(), rho=rho[sel].tolist(), local=loc[sel].tolist()))
    R.check("C2 CONTROL: EdS point-seed infall at q = 0.05 approaches rho ~ r^(-9/4) within +-0.15 over the self-similar range",
            f"fitted slope {slope:+.3f} over lambda = r/r_ta in [{C2_RANGE[0]}, {C2_RANGE[1]}]", abs(slope + 2.25) <= 0.15)
    R.check("C2 (reported): local slopes over the same range", f"min {loc[sel].min():+.2f}, max {loc[sel].max():+.2f}",
            bool(np.all(np.abs(loc[sel] + 2.25) <= 0.15)), load_bearing=False)

    # ------------------------------------------------------------------------------------------ R1 and H1
    xe = XB_EDGES; xc = np.sqrt(xe[1:] * xe[:-1])
    g1 = (xc >= G1_LO) & (xc <= G1_HI)
    c3m = (xc >= C3_LO) & (xc <= G1_HI)
    table = {}
    for f in FOOTS:
        R.banner(f"R1 ({f} footing, a0 = {A0_SI[f]:.4e}): C_infall / C_target on x = r/r_M bins (0.1 dex), z = 0" +
                 ("   [MUTATE: target rho_c in place of the simulation]" if MUTATE else ""))
        P("  x centres: " + " ".join(f"{x:5.2f}" for x in xc))
        for q in QS:
            P(f"\n  q = r_peri/r_ta = {q}:")
            for M in MASSES:
                for g in GEOMS:
                    r_ = get("main", M, g, q)[0]
                    F_ = r_["foot"][f]
                    if MUTATE:
                        T_ = target_binned(M, g, f)
                        e = XB_EDGES * r_M(M, f); rcb = np.sqrt(e[1:] * e[:-1])
                        rat = ratio_of(np.array(T_["dM"]), np.array(T_["Mc"]), np.array(T_["dM"]), np.array(T_["Mc"]), Mb_enc(M, g, rcb))
                    else:
                        rat = np.array(F_["ratio"], float)
                    dev = np.abs(rat - 1.0)
                    dg = np.where(g1, dev, -1.0)
                    kmx = int(np.argmax(dg))
                    ok = g1 & (dev <= 0.1)
                    best, run_, start = (None, None), 0, None
                    for i_ in range(len(xc)):
                        if ok[i_]:
                            start = i_ if run_ == 0 else start
                            run_ += 1
                            if best[0] is None or run_ > best[1] - best[0] + 1:
                                best = (start, i_)
                        else:
                            run_ = 0
                    xr = f"[{xe[best[0]]:.2f}, {xe[best[1] + 1]:.2f}]" if best[0] is not None else "none"
                    table[(f, q, M, g)] = dict(maxdev=float(dg[kmx]), x_at=float(xc[kmx]), x_within=xr, ratio=rat.tolist(),
                                               boot_sd=F_["boot_sd"], n_distinct=F_["n_distinct"], mean_shells=F_["mean_shells"],
                                               passes=bool(dg[kmx] <= 0.1))
                    P(f"  {M:6.0e} {g:5s} " + " ".join(f"{x:5.2f}" if np.isfinite(x) else "  nan" for x in rat) +
                      f" | max|dev| {dg[kmx]:.2f} at x={xc[kmx]:.2f}; within 10%: {xr}")
        P("\n  discreteness indicators (simulation, x = 0.1 / 0.3 / 1 / 3 / 10 / 30 bins): time-averaged shells in the bin; "
          "distinct shells visiting it in the window; shell-bootstrap sd of the ratio")
        ii = [int(np.argmin(np.abs(np.log(xc / x)))) for x in (0.1, 0.3, 1, 3, 10, 30)]
        for q in QS:
            for M in MASSES:
                for g in GEOMS:
                    t_ = table[(f, q, M, g)]
                    P(f"    q={q:.2f} {M:6.0e} {g:5s} shells " + "/".join(fnum(t_['mean_shells'][i], '{:.2g}') for i in ii) +
                      "; distinct " + "/".join(str(t_['n_distinct'][i]) for i in ii) +
                      "; boot sd " + "/".join(fnum(t_['boot_sd'][i], '{:.2f}') for i in ii))
    R.num("R1", {f"{f}|q={q}|{M:.0e}|{g}": v for (f, q, M, g), v in table.items()})

    R.banner("H1 [HEADLINE]: G1 -- for at least one bracket, |C_infall/C_target - 1| <= 0.10 over x in [0.1, 30] at every mass, "
             "both geometries" + ("   [MUTATE]" if MUTATE else ""))
    h1 = {}
    for f in FOOTS:
        per_q = {}
        for q in QS:
            fails = [(M, g, table[(f, q, M, g)]["maxdev"]) for M in MASSES for g in GEOMS if not table[(f, q, M, g)]["passes"]]
            per_q[q] = not fails
            md = max(table[(f, q, M, g)]["maxdev"] for M in MASSES for g in GEOMS)
            P(f"  {f:9s} q = {q:.2f}: {8 - len(fails)}/8 mass-geometry cases pass; largest deviation {md:.2f}; "
              + ("PASS" if not fails else "fails: " + ", ".join(f"{M:.0e}/{g} ({d:.2f})" for M, g, d in fails)))
        h1[f] = any(per_q.values())
        R.check(f"H1 on the {f} footing (reported per footing)", "brackets passing: " +
                (", ".join(str(q) for q in QS if per_q[q]) or "none"), h1[f], load_bearing=False)
    R.num("H1", dict(per_footing=h1))
    worst = {f: min(max(table[(f, q, M, g)]["maxdev"] for M in MASSES for g in GEOMS) for q in QS) for f in FOOTS}
    R.check("H1 [HEADLINE]: G1 holds (every mass, both geometries, one bracket, both footings)",
            f"best bracket's largest deviation: canonical {worst['canonical']:.2f}, alt {worst['alt']:.2f} (pass line 0.10)",
            h1["canonical"] and h1["alt"])

    # ------------------------------------------------------------------------------------------ C3
    R.banner("C3 CONTROL: 5,000 vs 20,000 shells -- ratio curves agree to 10% over x in [0.3, 30]")
    c3rows, c3ok = [], True
    for f in FOOTS:
        for q in QS:
            for M in MASSES:
                for g in GEOMS:
                    a20 = np.array(get("main", M, g, q)[0]["foot"][f]["ratio"], float)
                    a5 = np.array(get("C3", M, g, q)[0]["foot"][f]["ratio"], float)
                    with np.errstate(divide="ignore", invalid="ignore"):
                        d = np.abs(a5 / a20 - 1.0)
                    dm = float(np.nanmax(np.where(c3m, d, np.nan))) if np.isfinite(d[c3m]).all() else float("inf")
                    c3rows.append((f, q, M, g, dm))
                    c3ok &= dm <= 0.1
    for f in FOOTS:
        for q in QS:
            P(f"  {f:9s} q={q:.2f}: " + "  ".join(f"{M:.0e}/{g} {dm:.3f}" for f_, q_, M, g, dm in c3rows if f_ == f and q_ == q))
    worst3 = max(r[4] for r in c3rows)
    R.num("C3", [dict(foot=r[0], q=r[1], M=r[2], geom=r[3], maxdev=r[4]) for r in c3rows])
    R.check("C3 CONTROL: the 5,000-shell ratio curves reproduce the 20,000-shell ones to 10% over x in [0.3, 30]",
            f"largest |ratio_5k/ratio_20k - 1| = {worst3:.3f} over {len(c3rows)} curves", c3ok)

    # ------------------------------------------------------------------------------------------ R2
    R.banner("R2: the infall profile's radial scale against M_b (radius where the log-slope of rho_c is -2)")
    r2 = {}
    for g in GEOMS:
        for q in QS:
            rows = []
            for M in MASSES:
                r_ = get("main", M, g, q)[0]
                gen = r_["gen"]
                rc = np.array(gen["rc"]); dM = np.array(gen["dM"])
                vol = 4 * math.pi / 3 * (GEN_EDGES[1:] ** 3 - GEN_EDGES[:-1] ** 3) * r_M(M) ** 3
                rho = dM / vol
                lr, lrho = np.log(rc), np.log(np.maximum(rho, 1e-300))
                sl = np.full(len(rc), np.nan)
                for i_ in range(2, len(rc) - 2):
                    w_ = slice(i_ - 2, i_ + 3)
                    if np.all(rho[w_] > 0):
                        sl[i_] = np.polyfit(lr[w_], lrho[w_], 1)[0]
                r_m2 = float("nan")
                start = int(np.searchsorted(rc / r_M(M), 0.1))
                for i_ in range(max(start, 3), len(rc)):
                    if np.isfinite(sl[i_ - 1]) and np.isfinite(sl[i_]) and sl[i_ - 1] > -2.0 >= sl[i_]:
                        fr = (sl[i_ - 1] + 2.0) / (sl[i_ - 1] - sl[i_])
                        r_m2 = float(math.exp(lr[i_ - 1] + fr * (lr[i_] - lr[i_ - 1])))
                        break
                rows.append((M, r_m2, r_["r_ta_meas"]))
            Ms = np.array([x[0] for x in rows]); rm2 = np.array([x[1] for x in rows]); rta = np.array([x[2] for x in rows])
            okk = np.isfinite(rm2)
            e2 = float(np.polyfit(np.log(Ms[okk]), np.log(rm2[okk]), 1)[0]) if okk.sum() >= 3 else float("nan")
            eta_ = float(np.polyfit(np.log(Ms), np.log(rta), 1)[0])
            r2[(g, q)] = dict(r_m2=rm2.tolist(), x_m2=(rm2 / np.array([r_M(M) for M in Ms])).tolist(), exp_m2=e2, r_ta=rta.tolist(), exp_ta=eta_)
            P(f"  {g:5s} q={q:.2f}: r(-2) = " + ", ".join(f"{fnum(x, '{:.3g}')}" for x in rm2) + " kpc (x = " +
              ", ".join(fnum(x, '{:.2f}') for x in rm2 / np.array([r_M(M) for M in Ms])) + f"); exponent {fnum(e2, '{:.3f}')}; "
              f"r_ta(z=0) exponent {eta_:.3f}")
    R.num("R2", {f"{g}|q={q}": v for (g, q), v in r2.items()})
    e_all = [v["exp_m2"] for v in r2.values() if np.isfinite(v["exp_m2"])]
    R.check("R2 (reported): the infall radial scale scales like the target's r_M ~ M^(1/2) (exponent within 0.05 of 0.5)",
            f"exponents of r(-2): {', '.join(f'{x:.3f}' for x in e_all)} (turnaround expectation 1/3)",
            bool(e_all) and all(abs(x - 0.5) <= 0.05 for x in e_all), load_bearing=False)

    # ------------------------------------------------------------------------------------------ post-hoc diagnostics
    R.banner("POST-HOC DIAGNOSTICS (added after the first full run showed C3 failing; reported only -- no frozen verdict changes)")
    P("  (i) where C3 fails: the local binned ratio against the cumulative cold mass M_c(<r), 5,000 vs 20,000 shells")
    diag = []
    for f in FOOTS:
        for q in QS:
            for M in MASSES:
                for g in GEOMS:
                    A_ = get("main", M, g, q)[0]["foot"][f]; B_ = get("C3", M, g, q)[0]["foot"][f]
                    with np.errstate(divide="ignore", invalid="ignore"):
                        dr = np.abs(np.array(B_["ratio"], float) / np.array(A_["ratio"], float) - 1.0)
                        dm = np.abs(np.array(B_["Mc"], float) / np.array(A_["Mc"], float) - 1.0)
                    s1 = (xc >= 1.0) & (xc <= G1_HI); s3 = (xc >= 3.0) & (xc <= G1_HI)
                    diag.append(dict(foot=f, q=q, M=M, geom=g, ratio_03=float(np.nanmax(np.where(c3m, dr, np.nan))),
                                     ratio_3=float(np.nanmax(np.where(s3, dr, np.nan))), Mc_1=float(np.nanmax(np.where(s1, dm, np.nan))),
                                     Mc_3=float(np.nanmax(np.where(s3, dm, np.nan))), Mc_28=float(dm[-1])))
    for k_, lab in (("ratio_03", "local ratio, x in [0.3, 30] (the frozen C3 measure)"), ("ratio_3", "local ratio, x in [3, 30]"),
                    ("Mc_1", "cumulative M_c(<r), x in [1, 30]"), ("Mc_3", "cumulative M_c(<r), x in [3, 30]"),
                    ("Mc_28", "cumulative M_c(<r) at x = 28")):
        v = np.array([d_[k_] for d_ in diag])
        P(f"    |5k/20k - 1| of the {lab}: median over the 48 curves {np.median(v):.3f}, largest {v.max():.3f}")
    R.num("posthoc_C3_breakdown", diag)
    P("\n  (ii) H1 evaluated on the 5,000-shell runs (same evaluator)")
    h1_5k = {}
    for f in FOOTS:
        worst_per_q = []
        for q in QS:
            devs = [float(np.max(np.where(g1, np.abs(np.array(get("C3", M, g, q)[0]["foot"][f]["ratio"], float) - 1.0), -1.0)))
                    for M in MASSES for g in GEOMS]
            worst_per_q.append(max(devs))
        best = min(worst_per_q)
        h1_5k[f] = best
        P(f"    {f:9s}: best bracket's largest deviation {best:.2f} (pass line 0.10) -> " + ("PASS" if best <= 0.1 else "FAIL"))
    R.num("posthoc_H1_5k_best_maxdev", h1_5k)
    P("\n  (iii) the cumulative cold mass against the target's (canonical footing): M_c,sim(<r)/M_c,target(<r) at x = 1.12 and 28.2")
    cm = []
    for q in QS:
        line = []
        for M in MASSES:
            for g in GEOMS:
                T_ = target_binned(M, g, "canonical")
                v20 = [get("main", M, g, q)[0]["foot"]["canonical"]["Mc"][i] / T_["Mc"][i] for i in (10, 24)]
                v5 = [get("C3", M, g, q)[0]["foot"]["canonical"]["Mc"][i] / T_["Mc"][i] for i in (10, 24)]
                cm.append(dict(q=q, M=M, geom=g, x1=v20[0], x28=v20[1], x1_5k=v5[0], x28_5k=v5[1]))
                line.append(f"{M:.0e}/{g} {v20[0]:.2f}|{v20[1]:.2f}")
        P(f"    q={q:.2f}: " + "  ".join(line))
    a28 = np.array([c_["x28"] for c_ in cm]); a28_5 = np.array([c_["x28_5k"] for c_ in cm])
    P(f"    at x = 28.2 the simulated cold mass is {a28.min():.2f}-{a28.max():.2f} of the target's (5,000 shells: {a28_5.min():.2f}-{a28_5.max():.2f})")
    R.num("posthoc_Mc_vs_target", cm)
    P("\n  (iv) R2 cross-check with a cumulative scale: the radius where M_c(<r) = M_b (the target puts it at x = sqrt(3) for a point mass,")
    P("      i.e. r ~ M_b^(1/2)); generic profile, both resolutions")
    r2b = {}
    for kind in ("main", "C3"):
        for g in GEOMS:
            for q in QS:
                rs_ = []
                for M in MASSES:
                    gen = get(kind, M, g, q)[0]["gen"]
                    rc_, Mc_ = np.array(gen["rc"]), np.array(gen["Mc"])
                    i_ = int(np.argmax(Mc_ >= M))
                    rs_.append(math.exp(np.interp(math.log(M), [math.log(Mc_[i_ - 1]), math.log(Mc_[i_])], [math.log(rc_[i_ - 1]), math.log(rc_[i_])])))
                ex = float(np.polyfit(np.log(MASSES), np.log(rs_), 1)[0])
                r2b[f"{kind}|{g}|q={q}"] = dict(r=rs_, x=[r / r_M(M) for r, M in zip(rs_, MASSES)], exponent=ex)
                P(f"    {'20k' if kind == 'main' else ' 5k'} {g:5s} q={q:.2f}: r = {', '.join(f'{r:.3g}' for r in rs_)} kpc (x = "
                  f"{', '.join(f'{r / r_M(M):.2f}' for r, M in zip(rs_, MASSES))}); exponent {ex:.3f}")
    R.num("posthoc_R2_Mc_equals_Mb", r2b)

    # ------------------------------------------------------------------------------------------ R3: gates
    R.banner("R3: the shared gates as statements (G1 is H1; the door lives or dies on G1)")
    P("  G1 target        : " + ("PASS" if (h1['canonical'] and h1['alt']) else "FAIL") + " (H1 above).")
    P("  G2 CMB/growth    : the cold fluid is CDM (collisionless, cold shells under Newtonian gravity only), so its linear growth and")
    P("                     CMB behaviour are LCDM's by construction (not re-tested here).  The simulation's idealised background")
    P("                     (baryons outside the core held smooth) slows the cold perturbation's growth a little; that is a set-up")
    P("                     simplification, not a property of the mechanism.")
    P("  G3 reciprocity   : ordinary Newtonian gravity between the cold fluid and the baryons: the reaction on the baryons is the")
    P("                     Newtonian pull of the cold mass (third law) and the dynamics conserve energy.  The core is held static,")
    P("                     which is an untested hypothesis, not a result.")
    P("  G4 constants     : no constant in the dynamics beyond LCDM's.  The result depends on declared initial-condition choices")
    P("                     (z_i = 100, the full core present from z_i, the bracket q, the smooth-background reading); a pass that")
    P("                     needed one of them would count it against G4.  kappa enters only through the target's a0.")
    P("  G5 well-posedness: collisionless CDM (Vlasov-Poisson) is well posed; Newtonian gravity is Solar-System (Cassini) safe.")
    R.num("R3", dict(G1="PASS" if (h1["canonical"] and h1["alt"]) else "FAIL", G2="CDM by construction", G3="Newtonian",
                     G4="no new dynamical constant; IC choices declared", G5="CDM well posed"))

    P("\n  kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.")
    nf = R.write(here=HERE)
    sys.exit(1 if nf else 0)


if __name__ == "__main__":
    main()
