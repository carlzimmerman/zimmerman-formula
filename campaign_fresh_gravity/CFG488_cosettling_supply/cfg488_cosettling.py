#!/usr/bin/env python3
"""CFG488: co-settling per Lagrangian shell as the supply rule behind the 5.85 r_M edge.
Criteria: FROZEN_CRITERIA.md (committed alone first, 88f3bdcaa).

kappa = 1/2 is FITTED. Both footings scored separately, never pooled. No dark-matter particle is added: the cold fluid's
MASS is still required and its amount (Omega_c/Omega_b = 5.364) is an input. G9 stands. Offline theory + numerics on
committed record files only; no downloads. This is not "theory closed".

Run:  python3 cfg488_cosettling.py                    (writes cfg488.out, cfg488_results.json, cfg488_sims.json;
                                                       exit 0 iff K1-K5 pass)
      CFG488_MUTATE=1 python3 cfg488_cosettling.py    (Omega_c/Omega_b x 2 at fixed Omega_m; writes *_MUTATE.*;
                                                       exit 1 iff the teeth are detected, as frozen)
      CFG488_NPROC sets the process count (default 3).

Units: the scale-free readings use G = 1, M_b = 1, lengths in r_M = sqrt(G M_b/a0) (point host: y = 1/x^2). The infall runs
use kpc, km/s, Msun (CFG118's units) and are converted to r_M at each mass and footing.
"""
import os
import sys
import math
import json
import time
import hashlib
import tempfile
import subprocess

sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.dirname(HERE)
REPO = os.path.dirname(CFGDIR)
sys.path.insert(0, CFGDIR)
import CFG4_common as C4  # noqa: E402  (record constants; nu_mono = FP1's committed kernel, read-only)

MUT = os.environ.get("CFG488_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
NPROC = int(os.environ.get("CFG488_NPROC", "3"))
SHELLCORE = os.path.join(CFGDIR, "CFG118_secondary_infall", "shellcore.c")   # read-only; compiled into a temp dir
_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ======================================================================================================== constants
SHARE_TRUE = 5.364                                  # Omega_c/Omega_b (input; the shells' composition)
SHARE = 2.0 * SHARE_TRUE if MUT else SHARE_TRUE     # MUTATE: cosmic ratio x 2 at fixed Omega_m
FB = 1.0 / (1.0 + SHARE)
X_EDGE = 1.0 / math.log(1.0 + 1.0 / SHARE_TRUE)     # 5.8498 r_M: the TRUE edge, always the scoring reference
LOGMB = [9.0, 10.5, 11.5]
FOOTS = C4.FOOTS
A0_SI = {f: float(C4.A0[f]) for f in FOOTS}         # 9.3603e-11 / 1.1312e-10 (kappa = 1/2 FITTED)
TOL_P1, TOL_P1B, TOL_MUT = 0.05, 0.05, 0.02
P1B_LO, P1B_HI = 0.1, 0.8

# the infall worker (CFG118's machinery, copied into cfg488_infall.py; no side effects on import)
sys.path.insert(0, HERE)
import cfg488_infall as IF  # noqa: E402
assert IF.A0_SI == A0_SI and IF.SHARE == SHARE and IF.MUT == MUT
M_SIM, QS, NS, NS_RES, EDGES_TA = IF.M_SIM, IF.QS, IF.NS, IF.NS_RES, IF.EDGES_TA
r_M_kpc = IF.r_M_kpc
CFG118_MTA, CFG118_RTA0 = 23.641598526545486, 507.9993489845386   # CFG118 point core, 1e10 (committed sims.json)

R = {"lane": "CFG488", "mutate": MUT, "kappa": "1/2 FITTED", "share": SHARE, "share_true": SHARE_TRUE, "f_b": FB,
     "x_edge_true": X_EDGE, "controls": {}, "formulations": {}, "clusters": {}, "g9": {}, "depletion": {}, "reported": {}}

P("=" * 116)
P(f"CFG488 co-settling per Lagrangian shell   MUTATE={MUT}")
P(f"shell composition Omega_c/Omega_b = {SHARE:.3f} (f_b = {FB:.6f}); TRUE edge r_edge = r_M/ln(1+1/5.364) = {X_EDGE:.4f} r_M")
P(f"footings: canonical a0 = {A0_SI['canonical']:.4e}, alt a0 = {A0_SI['alt']:.4e} m/s^2 (kappa = 1/2 FITTED; never pooled)")
P("=" * 116)


# ======================================================================================================== kernel and target (scale-free units)
def nu(y):
    return C4.nu_mono(np.maximum(np.asarray(y, float), 1e-300))


def Mph_point(x, m=1.0):
    """phantom inside x (units of r_M of the PRESENT M_b = 1) for a point host of mass m: m (nu(m/x^2) - 1)."""
    x = np.asarray(x, float)
    return m * (nu(m / x ** 2) - 1.0)


def Mb_hern(x, m, a):
    x = np.asarray(x, float)
    return m * x ** 2 / (x + a) ** 2


def Mph_hern(x, m, aa=0.3):
    """Hernquist host of mass m with a = aa * r_M(m) = aa sqrt(m) (self-similar growth)."""
    a = aa * math.sqrt(m) if np.isscalar(m) else aa * np.sqrt(m)
    Mb = Mb_hern(x, m, a)
    return Mb * (nu(Mb / np.asarray(x, float) ** 2) - 1.0)


def x_exhaust(S):
    return 1.0 / math.log(1.0 + 1.0 / S)


def marg_point(y):
    """d M_ph/d M at fixed r for a point host, in M_b units: nu(y) + y nu'(y) - 1 (central difference, rel step 1e-3: the
    committed nu_mono is a table, and smaller steps amplify its interpolation noise; error <= 6e-6 absolute, checked in K1)."""
    y = np.asarray(y, float)
    h = 1e-3
    return ((y * (1 + h)) * (nu(y * (1 + h)) - 1) - (y * (1 - h)) * (nu(y * (1 - h)) - 1)) / (2 * h * y)


def x_marginal(S):
    """the marginal exhaustion radius x_k (units of r_M of the CURRENT mass): nu + y nu' - 1 = S at y = 1/x^2."""
    return 10 ** brentq(lambda lx: float(marg_point(np.array([10 ** (-2 * lx)]))[0]) - S, -2, 4, xtol=1e-14)


def r_frac(xg, M, total, frac=0.999):
    """radius enclosing frac of 'total' for a cumulative profile M on grid xg (log-interp)."""
    tgt = frac * total
    i = int(np.searchsorted(M, tgt))
    if i <= 0:
        return float(xg[0])
    if i >= len(M):
        return float(xg[-1])
    f = (tgt - M[i - 1]) / (M[i] - M[i - 1])
    return float(10 ** (math.log10(xg[i - 1]) + f * (math.log10(xg[i]) - math.log10(xg[i - 1]))))


def p1b_metric(xg, Melig, Mtgt, x_edge=X_EDGE):
    sel = (xg >= P1B_LO * x_edge) & (xg <= P1B_HI * x_edge)
    d = Melig[sel] / Mtgt[sel] - 1.0
    k = int(np.argmax(np.abs(d)))
    return float(d[k]), float(xg[sel][k])


# ======================================================================================================== K1 (sympy)
P("\n[K1] sympy: composition identity, point-mass exhaustion radius, marginal-edge equation, CS-M telescoping")
Sx, Mb_, dq = sp.symbols("S M_b dq", positive=True)
qq = sp.symbols("q", positive=True)
rho_b = sp.Function("rho_b")
ident = sp.simplify(sp.Integral(Sx * rho_b(qq), (qq, 0, dq)) - Sx * sp.Integral(rho_b(qq), (qq, 0, dq)))
xs, ss = sp.symbols("x s", positive=True)
nu_s = 1 / (1 - sp.exp(-ss))                              # nu_mono closed form below y = 2.54, s = sqrt(y)
nu_pm = nu_s.subs(ss, 1 / xs)                              # point mass: sqrt(y) = 1/x
exh = sp.simplify(nu_pm - 1 - 1 / (sp.exp(1 / xs) - 1))
xe_sym = 1 / sp.log(1 + 1 / Sx)
exh2 = sp.simplify((nu_pm - 1).subs(xs, xe_sym) - Sx)
yy_ = sp.symbols("y", positive=True)
nu_y = 1 / (1 - sp.exp(-sp.sqrt(yy_)))
marg_expr = sp.simplify(sp.diff(yy_ * (nu_y - 1), yy_) - (nu_y + yy_ * sp.diff(nu_y, yy_) - 1))
mm, xk = sp.symbols("m x_k", positive=True)
Mph_m = mm * (nu_y.subs(yy_, mm / xs ** 2) - 1)            # phantom of a point host m inside x (x in r_M(final) units)
dMph = sp.diff(Mph_m, mm)
# self-similarity of the marginal phantom: d_m M_ph(<x; m) depends on y = m/x^2 only, so each increment's marginal edge is
# x_k sqrt(m) (the basis of the CS-M closed form checked numerically in K3). (The telescoping itself is the fundamental
# theorem of calculus; sympy cannot integrate nu_mono's derivative in closed form, so the closed form is checked in K3.)
yv = sp.symbols("Y", positive=True)
tele = sp.simplify(sp.diff(dMph.subs(mm, yv * xs ** 2), xs))
xk_true = x_marginal(SHARE_TRUE)
xk_mut = x_marginal(2 * SHARE_TRUE)
k1_xe_num = abs(x_exhaust(SHARE_TRUE) - float(1 / (sp.log(1 + 1 / sp.Rational(5364, 1000)))))
# numeric check of the marginal equation with the closed form (y = 1/x_k^2 < 2.54)
mk_check = float((nu_y + yy_ * sp.diff(nu_y, yy_) - 1).subs(yy_, 1 / xk_true ** 2)) - SHARE_TRUE
K1 = bool(ident == 0 and exh == 0 and exh2 == 0 and marg_expr == 0 and tele == 0 and abs(mk_check) < 1e-4 and k1_xe_num < 1e-12)
P(f"  composition identity residual = {ident}; nu-1 = 1/(e^(1/x)-1) residual = {exh}; x_e = 1/ln(1+1/S) residual = {exh2}")
P(f"  marginal phantom d(y(nu-1))/dy = nu + y nu' - 1 residual = {marg_expr}; d/dx of d_m M_ph at fixed y = m/x^2: {tele}")
P(f"  x_e(5.364) = {x_exhaust(SHARE_TRUE):.6f} r_M; x_k(5.364) = {xk_true:.6f} r_M (closed-form check {mk_check:.1e}); "
  f"x_k(10.728) = {xk_mut:.6f}  -> K1 {'PASS' if K1 else 'FAIL'}")
R["controls"]["K1"] = {"pass": K1, "x_e": x_exhaust(SHARE_TRUE), "x_k": xk_true, "x_k_mut": xk_mut, "mk_check": mk_check}


# ======================================================================================================== scale-free readings: CS-P, CS-M, CS-F
P("\n" + "=" * 116)
P("SCALE-FREE READINGS (history enters only through the Lagrangian order of the galaxy's baryons; any monotone history")
P("from ~0 gives the same result). Units: r_M of the present M_b. Point host scored; Hernquist a = 0.3 r_M(t) reported.")
P("=" * 116)
XG = np.logspace(-3, 3, 12001)
TGT = Mph_point(XG)
MP_LOG = np.linspace(-12, 0, 6001)                  # increments m' = M'/M_b (log grid)
MPV = 10 ** MP_LOG


def superpose(fun, S, xg=XG):
    """M_s(<x) = int_0^1 min(fun(x, m'), S) dm' (trapezoid in m' on the log grid + the analytic piece below 1e-12)."""
    out = np.zeros_like(xg)
    w = np.zeros_like(MPV)
    dm = np.diff(MPV)
    w[:-1] += 0.5 * dm
    w[1:] += 0.5 * dm
    for i0 in range(0, len(xg), 1000):
        xx = xg[i0:i0 + 1000][:, None]
        f = np.minimum(fun(xx, MPV[None, :]), S)
        out[i0:i0 + 1000] = (f * w[None, :]).sum(1) + S * MPV[0]
    return out


f_marg_point = lambda xx, m: marg_point(m / xx ** 2)
f_prop_point = lambda xx, m: nu(m / xx ** 2) - 1.0


def f_marg_hern(xx, m, aa=0.3):
    h = 1e-3
    return (Mph_hern(xx, m * (1 + h), aa) - Mph_hern(xx, m * (1 - h), aa)) / (2 * h * m)


def f_prop_hern(xx, m, aa=0.3):
    return Mph_hern(xx, m, aa) / m


def score_profile(name, Ms, Melig, tgt, S, host, support=None):
    """edge r_999 and P1b from a settled cumulative profile (scale-free: identical in all 6 cells)."""
    re = r_frac(XG, Ms, S)
    r99 = r_frac(XG, Ms, S, 0.99)
    d1 = math.log10(re / X_EDGE)
    db, xb = p1b_metric(XG, Melig, tgt)
    return {"host": host, "r_e": re, "r_99": r99, "support": support, "dex": d1, "p1": abs(d1) <= TOL_P1,
            "p1b_dev": db, "p1b_at": xb, "p1b": abs(db) <= TOL_P1B, "S_total": float(Ms[-1])}


SF = {}
# CS-P: the pooled LIVE fill of the present target, supply = composition x M_b (exact)
Ms_P = np.minimum(TGT, SHARE)
SF["CS-P"] = score_profile("CS-P", Ms_P, Ms_P, TGT, SHARE, "point", support=x_exhaust(SHARE))
# K2
k2 = abs(x_exhaust(SHARE_TRUE) / 5.8498 - 1) if not MUT else 0.0
xsup = brentq(lambda lx: float(Mph_point(np.array([10 ** lx]))[0]) - SHARE_TRUE, -1, 3, xtol=1e-14)
K2 = abs(10 ** xsup / 5.8498 - 1) <= 1e-4
P(f"[K2] CS-P point host, exhaustion radius of the composition supply: {10 ** xsup:.6f} r_M (5.8498 to {abs(10 ** xsup / 5.8498 - 1):.1e})"
  f" -> K2 {'PASS' if K2 else 'FAIL'}")
R["controls"]["K2"] = {"pass": bool(K2), "x": 10 ** xsup}

# CS-M: marginal phantom per increment, frozen at accretion
Ms_M = superpose(f_marg_point, SHARE)
xk = x_marginal(SHARE)
SF["CS-M"] = score_profile("CS-M", Ms_M, Ms_M, TGT, SHARE, "point", support=xk)
# K3: telescoped closed form
mstar = np.minimum(1.0, (XG / xk) ** 2)
# increments with m' > m* still hold part of their cold outside x; those with m' <= m* have placed ALL of it inside x
Ms_M_closed = Mph_point(XG) - Mph_point(XG, mstar) + SHARE * mstar
sel3 = (XG >= 0.05 * xk) & (XG <= 0.95 * xk)
k3err = float(np.max(np.abs(Ms_M[sel3] / Ms_M_closed[sel3] - 1)))
K3 = k3err <= 1e-4
P(f"[K3] CS-M numerical superposition vs telescoped closed form on [0.05, 0.95] x_k: max rel err {k3err:.1e} -> K3 {'PASS' if K3 else 'FAIL'}")
R["controls"]["K3"] = {"pass": bool(K3), "max_rel_err": k3err}

# CS-F: proportional share per increment, frozen at accretion
Ms_F = superpose(f_prop_point, SHARE)
SF["CS-F"] = score_profile("CS-F", Ms_F, Ms_F, TGT, SHARE, "point", support=x_exhaust(SHARE))

# Hernquist a = 0.3 r_M(t) (reported)
TGT_H = Mph_hern(XG, 1.0)
SFH = {}
SFH["CS-P"] = score_profile("CS-P", np.minimum(TGT_H, SHARE), np.minimum(TGT_H, SHARE), TGT_H, SHARE, "hernquist0.3")
Ms_MH = superpose(f_marg_hern, SHARE)
SFH["CS-M"] = score_profile("CS-M", Ms_MH, Ms_MH, TGT_H, SHARE, "hernquist0.3")
Ms_FH = superpose(f_prop_hern, SHARE)
SFH["CS-F"] = score_profile("CS-F", Ms_FH, Ms_FH, TGT_H, SHARE, "hernquist0.3")

P(f"\n  {'reading':7s} {'host':13s} {'r_e(99.9%)':>11s} {'support':>9s} {'dex vs r_edge':>14s} {'P1':>5s} "
  f"{'P1b max dev':>12s} {'at x':>6s} {'P1b':>5s}  settled total / M_b")
for nm in ("CS-P", "CS-M", "CS-F"):
    for d in (SF[nm], SFH[nm]):
        sup = f"{d['support']:.3f}" if d["support"] else "   --"
        P(f"  {nm:7s} {d['host']:13s} {d['r_e']:11.4f} {sup:>9s} {d['dex']:+14.4f} {'yes' if d['p1'] else 'no':>5s} "
          f"{d['p1b_dev']:+12.4f} {d['p1b_at']:6.2f} {'yes' if d['p1b'] else 'no':>5s}  {d['S_total']:.4f}")
for xr in (0.5, 1.0, 2.0, X_EDGE * 0.5, X_EDGE):
    i = int(np.searchsorted(XG, xr))
    P(f"    x = {XG[i]:6.3f} r_M: M_s/M_ph  CS-P {Ms_P[i] / TGT[i]:.4f}  CS-M {Ms_M[i] / TGT[i]:.4f}  CS-F {Ms_F[i] / TGT[i]:.4f}"
      f"   | inside r_edge: CS-M {np.interp(X_EDGE, XG, Ms_M) / SHARE:.3f}, CS-F {np.interp(X_EDGE, XG, Ms_F) / SHARE:.3f} of the supply"
      if abs(xr - X_EDGE) < 1e-9 else
      f"    x = {XG[i]:6.3f} r_M: M_s/M_ph  CS-P {Ms_P[i] / TGT[i]:.4f}  CS-M {Ms_M[i] / TGT[i]:.4f}  CS-F {Ms_F[i] / TGT[i]:.4f}")
R["formulations"]["scale_free_point"] = SF
R["formulations"]["scale_free_hernquist"] = SFH
R["formulations"]["profiles_at"] = {f"{xr:.3f}": {"CS-P": float(np.interp(xr, XG, Ms_P) / np.interp(xr, XG, TGT)),
                                                    "CS-M": float(np.interp(xr, XG, Ms_M) / np.interp(xr, XG, TGT)),
                                                    "CS-F": float(np.interp(xr, XG, Ms_F) / np.interp(xr, XG, TGT))}
                                    for xr in (0.585, 1.0, 2.0, 2.925, 4.68)}

# R-EQ test (continuum): equal to the SHARE control min(M_ph, 5.364) to 1e-6 relative
share_ctrl = np.minimum(TGT, SHARE_TRUE)
REQ = {nm: bool(np.max(np.abs(prof / share_ctrl - 1)) <= 1e-6) for nm, prof in (("CS-P", Ms_P), ("CS-M", Ms_M), ("CS-F", Ms_F))}
P(f"\n  R-EQ (profile = CFG462's SHARE control to 1e-6): CS-P {REQ['CS-P']}, CS-M {REQ['CS-M']}, CS-F {REQ['CS-F']}"
  + ("   [MUTATE: the share control is the TRUE 5.364; the mutated readings cannot equal it]" if MUT else ""))


# ======================================================================================================== infall histories (worker: cfg488_infall.py)
def jsafe(o):
    return IF.jsafe(o)


P("\n" + "=" * 116)
P("INFALL HISTORIES: H-N (CFG118 point core, LCDM; scored) and H-B (Bertschinger EdS; reported); one run per q at 1e10,")
P("rescaled r ~ M^(1/3) (exact self-similarity of the point-core problem)")
P("=" * 116)
sha_sc = hashlib.sha256(open(IF.SHELLCORE, "rb").read()).hexdigest()
P(f"  integrator: CFG118_secondary_infall/shellcore.c (read-only), sha256 {sha_sc[:16]}...; compiled into a temp dir per run")
CACHE = os.path.join(HERE, f"cfg488_sims{TAG}.json")
H = IF.config_hash()
sims = None
if os.path.exists(CACHE):
    d = json.load(open(CACHE))
    if d.get("hash") == H:
        sims = d
        P(f"  simulation products reused from {os.path.basename(CACHE)} (hash {H})")
if sims is None:
    specs = [dict(kind="HN", q=q, N=NS) for q in QS]
    if not MUT:
        specs += [dict(kind="HB", q=q, N=NS) for q in QS] + [dict(kind="HN", q=q, N=NS_RES) for q in QS]
    tmpd = tempfile.mkdtemp(prefix="cfg488_runs_")
    t0w = time.time()
    P(f"  running {len(specs)} infall simulations, {NPROC} at a time (separate processes) ...")
    pending, active, runs = list(enumerate(specs)), [], []
    while pending or active:
        while pending and len(active) < NPROC:
            i, s = pending.pop(0)
            outp = os.path.join(tmpd, f"run{i}.json")
            pr = subprocess.Popen([sys.executable, os.path.join(HERE, "cfg488_infall.py"), json.dumps(s), outp],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            active.append((i, s, outp, pr))
        time.sleep(2.0)
        still = []
        for i, s, outp, pr in active:
            if pr.poll() is None:
                still.append((i, s, outp, pr))
                continue
            if pr.returncode != 0:
                raise RuntimeError(f"infall run {s} failed: {pr.stderr.read().decode()[-2000:]}")
            res = json.load(open(outp))
            P(f"    [{len(runs) + 1}/{len(specs)}] {s['kind']} q={s['q']:.2f} N={s['N']}: {res['seconds']:.0f} s, turned {res['n_turned']}")
            runs.append(res)
        active = still
    sims = dict(hash=H, runs=runs, wall=time.time() - t0w, nproc=NPROC, shellcore_sha256=sha_sc)
    json.dump(sims, open(CACHE, "w"))
    P(f"  products written to {os.path.basename(CACHE)} (hash {H}); wall {sims['wall'] / 60:.1f} min")
RUNS = sims["runs"]


def getrun(kind, q, N=NS):
    for r in RUNS:
        if r["spec"]["kind"] == kind and abs(r["spec"]["q"] - q) < 1e-12 and r["spec"]["N"] == N:
            return r
    return None


# ---------------------------------------------------------------- K4: CFG118's set-up reproduced
P("\n[K4] H-N set-up vs CFG118's committed point-core 1e10 runs")
k4 = []
for q in QS:
    r = getrun("HN", q)
    su = r["setup"]
    mta, rta0 = su["M_ta"] / M_SIM, su["r_ta0"]
    meas = r["r_ta_meas"] / rta0
    ok = abs(mta / CFG118_MTA - 1) <= 0.01 and abs(rta0 / CFG118_RTA0 - 1) <= 0.01 and abs(meas - 1) <= 0.01
    k4.append(ok)
    P(f"  q = {q:.2f}: M_ta/M_b = {mta:.3f} (CFG118 {CFG118_MTA:.3f}), r_ta0 = {rta0:.2f} kpc (CFG118 {CFG118_RTA0:.2f}), "
      f"measured zero-velocity / single-shell = {meas:.4f}; cold mass inside the measured r_ta at z = 0 = "
      f"{r['cold_in_rta'] / M_SIM:.2f} M_b; shells to {su['M_out'] / M_SIM:.1f} M_b; {'ok' if ok else 'MISS'}")
K4 = all(k4) if not MUT else True
if MUT:
    P("  (MUTATE: the shell split is changed, so CFG118's numbers are not expected; K4 is checked in the main run)")
P(f"  -> K4 {'PASS' if K4 else 'FAIL'}  (note: M_ta in CFG118's set-up is the COLD Lagrangian mass of the turnaround shell;"
  f" the core is extra)")
R["controls"]["K4"] = {"pass": bool(K4), "M_ta_over_Mb": [getrun("HN", q)["setup"]["M_ta"] / M_SIM for q in QS],
                       "cold_in_rta_over_Mb": [getrun("HN", q)["cold_in_rta"] / M_SIM for q in QS]}


# ---------------------------------------------------------------- pool-based readings CS-I, CS-0 (and CS-P on the same grid)
def x_ta(run, M, foot):
    return run["setup"]["r_ta0"] * (M / M_SIM) ** (1.0 / 3.0) / r_M_kpc(M, foot)


def tgt_point(x):
    return Mph_point(x)


def cs_inward(xe, dP):
    """inward-only fill: greedy innermost-first (a parcel in bin b can settle anywhere inside the bin's upper edge)."""
    Tup = tgt_point(xe[1:])
    F = 0.0
    strand = np.zeros_like(dP)
    for b in range(len(dP)):
        s = min(dP[b], max(0.0, Tup[b] - F))
        F += s
        strand[b] = dP[b] - s
    Pc = np.concatenate([[0.0], np.cumsum(dP)])
    cut = float(min(Pc[-1], np.min(tgt_point(xe[1:]) + Pc[-1] - Pc[1:])))
    return F, strand, cut


def edge_from_total(S):
    """radius enclosing 99.9% of a settled profile min(M_ph(<x), S) (point host)."""
    return 10 ** brentq(lambda lx: float(Mph_point(np.array([10 ** lx]))[0]) - 0.999 * S, -3, 4, xtol=1e-13)


def cs0(xe, dP, group):
    """in place: settled per bin = min(pool, target) on bins of 'group' x 0.025 dex."""
    n = (len(dP) // group) * group
    dPg = dP[:n].reshape(-1, group).sum(1)
    xeg = xe[:n + 1:group]
    dT = np.diff(tgt_point(xeg))
    ds = np.minimum(dPg, dT)
    Ms = np.concatenate([[0.0], np.cumsum(ds)])
    re = r_frac(xeg, Ms, Ms[-1])
    return float(Ms[-1]), re, xeg, Ms


def eval_pool(run, wkey, M, foot):
    x_scale = x_ta(run, M, foot)
    xe = EDGES_TA * x_scale
    dP = np.array(run["prod"][wkey]["dM"]) / M_SIM
    Penc = np.array(run["prod"][wkey]["Menc"]) / M_SIM
    Tenc = tgt_point(xe)
    out = {"x_ta": x_scale}
    # CS-I
    F, strand, cut = cs_inward(xe, dP)
    re_I = edge_from_total(F)
    Selig_in = np.minimum(Tenc, F) + np.concatenate([[0.0], np.cumsum(strand)])
    dI, xI = p1b_metric(xe, Selig_in, Tenc)
    out["CS-I"] = {"settled": F, "cut": cut, "stranded": float(strand.sum()), "r_e": re_I, "dex": math.log10(re_I / X_EDGE),
                   "p1b_dev": dI, "p1b_at": xI, "stranded_inside_rM": float(np.interp(1.0, xe, np.concatenate([[0.0], np.cumsum(strand)])))}
    # CS-0 (0.05 dex scored; 0.1 dex reported)
    S0, re0, xeg, Ms0 = cs0(xe, dP, 2)
    d0, x0 = p1b_metric(xe, np.concatenate([[0.0], np.cumsum(dP)]), Tenc)
    S0b, re0b, _, _ = cs0(xe, dP, 4)
    out["CS-0"] = {"settled": S0, "r_e": re0, "dex": math.log10(re0 / X_EDGE), "p1b_dev": d0, "p1b_at": x0,
                   "settled_01dex": S0b, "r_e_01dex": re0b}
    # pool diagnostics
    Ptot = float(dP.sum())
    out["pool"] = {"total_binned": Ptot, "r50": r_frac(xe, np.concatenate([[0.0], np.cumsum(dP)]), Ptot, 0.5),
                   "r99": r_frac(xe, np.concatenate([[0.0], np.cumsum(dP)]), Ptot, 0.99),
                   "P_over_T_at_rM": float(np.interp(1.0, xe, Penc) / Mph_point(1.0)),
                   "P_over_T_at_redge": float(np.interp(X_EDGE, xe, Penc) / Mph_point(X_EDGE))}
    return out, xe, dP, Penc, strand


POOL = {}
P("\n" + "=" * 116)
P("POOL-BASED READINGS (H-N, R1 inner-first; 6 cells x 3 q). Edges in r_M; dex = log10(r_e / 5.8498 r_M).")
P("=" * 116)
K5_err = 0.0
for q in QS:
    run = getrun("HN", q)
    P(f"\n  H-N q = {q:.2f}: eligible cold (composition) = {run['elig_total'] / M_SIM:.6f} M_b; binned time-averaged pool "
      f"closure {np.sum(run['prod']['elig']['dM']) / run['elig_total']:.4f}; boundary shell index {run['kb']}")
    P(f"    {'cell':22s} {'x_ta':>6s} | {'CS-I settled':>12s} {'stranded':>9s} {'r_e':>7s} {'dex':>7s} {'P1b dev':>8s} | "
      f"{'CS-0 settled':>12s} {'r_e':>7s} {'dex':>7s} {'P1b dev':>8s} | {'pool r50':>8s} {'r99':>7s} {'P/T(rM)':>8s}")
    for l in LOGMB:
        M = 10 ** l
        for foot in FOOTS:
            o, xe, dP, Penc, strand = eval_pool(run, "elig", M, foot)
            K5_err = max(K5_err, abs(o["CS-I"]["settled"] - o["CS-I"]["cut"]) / max(o["CS-I"]["cut"], 1e-30))
            POOL[(q, l, foot)] = o
            P(f"    {f'{l:.1f} {foot}':22s} {o['x_ta']:6.1f} | {o['CS-I']['settled']:12.3f} {o['CS-I']['stranded']:9.3f} "
              f"{o['CS-I']['r_e']:7.3f} {o['CS-I']['dex']:+7.3f} {o['CS-I']['p1b_dev']:+8.3f} | {o['CS-0']['settled']:12.3f} "
              f"{o['CS-0']['r_e']:7.2f} {o['CS-0']['dex']:+7.3f} {o['CS-0']['p1b_dev']:+8.3f} | {o['pool']['r50']:8.2f} "
              f"{o['pool']['r99']:7.2f} {o['pool']['P_over_T_at_rM']:8.2f}")
K5 = K5_err <= 1e-9
P(f"\n[K5] CS-I min-cut total vs innermost-first greedy fill: max rel diff {K5_err:.1e} -> K5 {'PASS' if K5 else 'FAIL'}")
R["controls"]["K5"] = {"pass": bool(K5), "max_rel": K5_err}
R["formulations"]["pool_HN"] = {f"q{k[0]}_{k[1]:.1f}_{k[2]}": v for k, v in POOL.items()}


def pool_verdict(name):
    """P1 / P1b with the same-q rule: pass if some q passes in all 6 cells."""
    per_q = {}
    for q in QS:
        cells = [POOL[(q, l, f)][name] for l in LOGMB for f in FOOTS]
        p1 = all(abs(c["dex"]) <= TOL_P1 for c in cells)
        p1b = all(abs(c["p1b_dev"]) <= TOL_P1B for c in cells)
        per_q[q] = {"p1": p1, "p1b": p1b, "dex_range": [min(c["dex"] for c in cells), max(c["dex"] for c in cells)],
                    "p1b_worst": max((c["p1b_dev"] for c in cells), key=abs)}
    return per_q


PV = {nm: pool_verdict(nm) for nm in ("CS-I", "CS-0")}
for nm in ("CS-I", "CS-0"):
    for q in QS:
        v = PV[nm][q]
        P(f"  {nm} q = {q:.2f}: edge dex range {v['dex_range'][0]:+.3f} .. {v['dex_range'][1]:+.3f}  P1 {'yes' if v['p1'] else 'no'};"
          f"  worst P1b dev {v['p1b_worst']:+.3f}  P1b {'yes' if v['p1b'] else 'no'}")

# ---------------------------------------------------------------- K6 resolution (reported), R2 and H-B (reported)
K6 = None
if not MUT:
    P("\n[K6] resolution (reported): N = 5000 vs 20000 H-N, CS-I and CS-0 edges")
    k6max = 0.0
    k6by = {"CS-I": 0.0, "CS-0": 0.0}
    flips = []
    POOL5 = {}
    for q in QS:
        rlo = getrun("HN", q, NS_RES)
        for l in LOGMB:
            for f in FOOTS:
                o5, *_ = eval_pool(rlo, "elig", 10 ** l, f)
                POOL5[(q, l, f)] = o5
                o20 = POOL[(q, l, f)]
                for nm in ("CS-I", "CS-0"):
                    dd = abs(o5[nm]["dex"] - o20[nm]["dex"])
                    k6max = max(k6max, dd)
                    k6by[nm] = max(k6by[nm], dd)
    for nm in ("CS-I", "CS-0"):
        for q in QS:
            c5 = [POOL5[(q, l, f)][nm] for l in LOGMB for f in FOOTS]
            p1_5 = all(abs(c["dex"]) <= TOL_P1 for c in c5)
            p1b_5 = all(abs(c["p1b_dev"]) <= TOL_P1B for c in c5)
            if (p1_5 and p1b_5) != (PV[nm][q]["p1"] and PV[nm][q]["p1b"]):
                flips.append(f"{nm} q={q}")
            P(f"    {nm} q = {q:.2f} at N = 5000: edge dex {min(c['dex'] for c in c5):+.3f} .. {max(c['dex'] for c in c5):+.3f}, "
              f"worst P1b {max((c['p1b_dev'] for c in c5), key=abs):+.3f} -> (1) {'pass' if (p1_5 and p1b_5) else 'fail'}")
    K6 = k6max <= 0.05
    P(f"  max |edge(5000) - edge(20000)|: CS-I {k6by['CS-I']:.3f} dex, CS-0 {k6by['CS-0']:.3f} dex (the CS-0 edge is the pool's outer"
      f" tail) -> K6 {'PASS' if K6 else 'FAIL (kept, disclosed)'}; (1) verdict flips at N = 5000: {flips if flips else 'none'}")
    R["controls"]["K6"] = {"pass": bool(K6), "max_dex": k6max, "by_reading": k6by, "verdict_flips": flips}

    P("\n  R2 (uniform retention; reported) and H-B (Bertschinger EdS; reported): CS-I edge dex / CS-I P1b dev / CS-0 edge dex")
    rep = {}
    for lab, kind, wkey in (("R2 H-N", "HN", "r2"), ("R1 H-B", "HB", "elig")):
        for q in QS:
            run = getrun(kind, q)
            for f in FOOTS:
                row = []
                for l in LOGMB:
                    o, *_ = eval_pool(run, wkey, 10 ** l, f)
                    row.append((o["CS-I"]["dex"], o["CS-I"]["p1b_dev"], o["CS-0"]["dex"], o["CS-I"]["stranded"]))
                    rep[f"{lab}_q{q}_{l}_{f}"] = o
                ok1 = all(abs(a) <= TOL_P1 and abs(b) <= TOL_P1B for a, b, c, d in row)
                P(f"    {lab} q = {q:.2f} {f:9s}: " + "  ".join(f"[{l:.1f}] {a:+.3f} / {b:+.3f} / {c:+.3f} (strand {d:.2f})"
                                                       for l, (a, b, c, d) in zip(LOGMB, row))
                  + f"  CS-I (1) {'pass' if ok1 else 'fail'}")
    R["reported"]["R2_HB"] = rep
    # CS-P is history-blind: its supply from every history and q
    tots = [r["elig_total"] / M_SIM for r in RUNS]
    P(f"\n  CS-P supply from every run (composition, fractional boundary shell): min {min(tots):.12f}, max {max(tots):.12f} M_b"
      f" (spread {max(tots) - min(tots):.1e}) -> the CS-P profile is identical across histories (R-EQ history test)")
    R["reported"]["CSP_supply_spread"] = max(tots) - min(tots)
    REQ_hist = (max(tots) - min(tots)) <= 1e-9 * SHARE
else:
    REQ_hist = True

# ---------------------------------------------------------------- contamination (reported)
P("\n  CONTAMINATION (reported): INELIGIBLE (unsettled, CDM-like) cold fluid of H-N inside r, / M_ph(<r) [and in share units]")
cont = {}
for q in QS:
    run = getrun("HN", q)
    parts = []
    for l in LOGMB:
        for f in FOOTS:
            xs_ = x_ta(run, 10 ** l, f)
            xe = EDGES_TA * xs_
            Mi = np.array(run["prod"]["inelig"]["Menc"]) / M_SIM
            vals = {}
            for lab, xr in (("rM", 1.0), ("half_edge", 0.5 * X_EDGE), ("edge", X_EDGE)):
                mi = float(np.interp(math.log10(xr), np.log10(xe), Mi))
                vals[lab] = {"over_Mph": mi / Mph_point(xr), "share_units": mi / SHARE_TRUE}
            cont[f"q{q}_{l}_{f}"] = vals
            if f == "canonical":
                parts.append(f"[{l:.1f}] rM {vals['rM']['over_Mph']:.2f}  r_e/2 {vals['half_edge']['over_Mph']:.2f}  "
                             f"r_e {vals['edge']['over_Mph']:.2f} ({vals['edge']['share_units']:.2f} sh)")
    P(f"    q = {q:.2f} (canonical): " + " | ".join(parts))
flag_cont = {}
for l in LOGMB:
    for f in FOOTS:
        flag_cont[f"{l}_{f}"] = all(cont[f"q{q}_{l}_{f}"]["edge"]["over_Mph"] > 0.10 for q in QS)
# R2 (reported): under uniform retention the ineligible cold is (1 - f_r) of every turned shell plus the unturned ones
cont_r2 = {}
for q in QS:
    run = getrun("HN", q)
    parts = []
    for l in LOGMB:
        for f in FOOTS:
            xe = EDGES_TA * x_ta(run, 10 ** l, f)
            Mi = (np.array(run["prod"]["all"]["Menc"]) - np.array(run["prod"]["r2"]["Menc"])) / M_SIM
            mi = float(np.interp(math.log10(X_EDGE), np.log10(xe), Mi))
            mh = float(np.interp(math.log10(0.5 * X_EDGE), np.log10(xe), Mi))
            cont_r2[f"q{q}_{l}_{f}"] = {"edge_over_Mph": mi / Mph_point(X_EDGE), "half_edge_over_Mph": mh / Mph_point(0.5 * X_EDGE)}
            if f == "canonical":
                parts.append(f"[{l:.1f}] r_e/2 {mh / Mph_point(0.5 * X_EDGE):.2f}  r_e {mi / Mph_point(X_EDGE):.2f}")
    P(f"    R2, q = {q:.2f} (canonical; f_r = {run['f_r2']:.3f}): " + " | ".join(parts))
R["reported"]["contamination_R2"] = cont_r2
P(f"  'law contaminated' flag (ineligible > 10% of M_ph(<r_edge) at every q): " +
  ", ".join(f"{k} {'YES' if v else 'no'}" for k, v in flag_cont.items()))
R["reported"]["contamination"] = cont
R["reported"]["contamination_flag"] = flag_cont


# ======================================================================================================== (2) clusters
P("\n" + "=" * 116)
P("(2) CLUSTERS: unsettled fraction of the dark mass inside R500 (record: CFG453 committed medians, X-COP)")
P("=" * 116)
J453 = json.load(open(os.path.join(CFGDIR, "CFG453_t15_deficit_units", "cfg453_results.json")))
CL = {}
for f in FOOTS:
    D = J453["D1"][f]
    xA, xT, nucl = D["xA"]["cl"], D["xT"]["cl"], D["nu"]["cl"]
    urec = [SHARE_TRUE * a / t for a, t in zip(xA, xT)]
    lo, hi = min(urec), max(urec)
    u_free = 0.0
    u_place = 1.0 - min(nucl - 1.0, SHARE) / SHARE
    sens_free = max(0.0, xT[1] - SHARE) / xT[1]
    CL[f] = {"nu_minus_1": nucl - 1, "xT": xT, "xA": xA, "u_rec_range": [lo, hi], "u_free": u_free, "u_inplace": u_place,
             "u_free_sens_b03": sens_free, "Mdark_pred_free_over_Mb": nucl - 1, "Mdark_pred_inplace_over_Mb": SHARE,
             "Mdark_meas_over_Mb": xT}
    P(f"  {f:9s}: nu-1 = {nucl - 1:.3f}; x_T15 (b=0/0.3) = {xT[0]:.3f}/{xT[1]:.3f}; record u in [{lo:.4f}, {hi:.4f}] "
      f"(CFG383 bracket 0.3-0.7)")
    P(f"             free placement (CS-P, CS-M, CS-F): u = {u_free:.3f}  -> dark inside R500 = M_ph = {nucl - 1:.2f} M_b "
      f"(measured {xT[0]:.2f}-{xT[1]:.2f}); sensitivity with ineligible = max(0, x_T - S) at b = 0.3: u = {sens_free:.3f}")
    P(f"             in place (CS-I, CS-0): u = 1 - (nu-1)/{SHARE:.3f} = {u_place:.4f}  "
      f"(margins to the range: {u_place - lo:+.4f} / {hi - u_place:+.4f})")
CRIT2 = {}
for nm in ("CS-P", "CS-M", "CS-F", "CS-I", "CS-0"):
    key = "u_free" if nm in ("CS-P", "CS-M", "CS-F") else "u_inplace"
    CRIT2[nm] = all(CL[f]["u_rec_range"][0] <= CL[f][key] <= CL[f]["u_rec_range"][1] for f in FOOTS)
P("  (2) per reading: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in CRIT2.items()))
R["clusters"] = {"per_footing": CL, "crit2": CRIT2}


# ======================================================================================================== (3) G9
P("\n" + "=" * 116)
P("(3) G9: does keying settling to the baryons' accretion history need a direct baryon-cold coupling?")
P("=" * 116)
g9rows = {}
for N_ in ((NS, NS_RES) if not MUT else (NS,)):
    run = getrun("HN", 0.1, N_)
    sig = run["bshell"] / run["Mtot_rbar"]
    g9rows[N_] = {"per_parcel_signal": sig, "rbar_over_rta0": run["rbar_b"] / run["setup"]["r_ta0"]}
    P(f"  per-parcel signal, N = {N_}: the eligible boundary shell's own partner baryons ({run['bshell'] / M_SIM:.2e} M_b) vs the mass "
      f"enclosed at its time-averaged radius ({run['rbar_b'] / run['setup']['r_ta0']:.4f} r_ta0): dg/g = {sig:.2e}")
if not MUT:
    ratio = g9rows[NS_RES]["per_parcel_signal"] / g9rows[NS]["per_parcel_signal"]
    P(f"  ratio (N=5000)/(N=20000) = {ratio:.3f} (1/N scaling predicts 4.000)")
    # POST-HOC (labelled; added after the first output): the ratio above mixes the shell mass (exactly 1/N) with the enclosed
    # mass at each run's own single-shell time-averaged radius, which differs (0.106 vs 0.061 r_ta0). At one common radius:
    rr = g9rows[NS]["rbar_over_rta0"]
    sig_c = {}
    for N_ in (NS, NS_RES):
        run_ = getrun("HN", 0.1, N_)
        Menc = M_SIM + float(np.interp(math.log10(rr), np.log10(EDGES_TA), np.array(run_["prod"]["all"]["Menc"])))
        sig_c[N_] = run_["bshell"] / Menc
    P(f"  POST-HOC, same radius {rr:.4f} r_ta0 (time-averaged enclosed mass): dg/g = {sig_c[NS]:.2e} (N=20000), "
      f"{sig_c[NS_RES]:.2e} (N=5000), ratio {sig_c[NS_RES] / sig_c[NS]:.3f}: the per-parcel signal is the shell's own baryon"
      f" mass over an O(1) enclosed mass, so it vanishes as 1/N in the continuum")
    g9rows["ratio"] = ratio
    g9rows["posthoc_common_radius"] = {str(k): v for k, v in sig_c.items()}
# collective signal at r_edge (1e10 canonical, q = 0.1): galaxy baryons in the core vs left on the eligible orbits
run = getrun("HN", 0.1)
xs_ = x_ta(run, 1e10, "canonical")
xe = EDGES_TA * xs_
Pel = np.array(run["prod"]["elig"]["Menc"]) / M_SIM
Pall = np.array(run["prod"]["all"]["Menc"]) / M_SIM
pin = float(np.interp(math.log10(X_EDGE), np.log10(xe), Pel))
call = float(np.interp(math.log10(X_EDGE), np.log10(xe), Pall))
dMb = 1.0 - pin / SHARE
coll = dMb / (1.0 + call)
P(f"  collective signal at r_edge (1e10, canonical, q = 0.1): if the galaxy's baryons stayed on the eligible orbits, the baryons"
  f" inside r_edge drop by {dMb:.3f} M_b against {1 + call:.2f} M_b enclosed: dg/g = {coll:.3f} (O(f_b); halo-level, not per parcel)")
g9rows["collective"] = coll
G9CLASS = {
    "CS-P": ("G9-FAIL", "needs q in Gal(t) for every cold parcel (partner identity across species)",
             "cap = (rho_c/rho_b)_cosmic x M_b,gal: species-split M_b,gal and the settled cold's own enclosed mass "
             "(G9-TENSION); with the ratio read from (own density, K) it is the share cap written as a law = the edge definition"),
    "CS-I": ("G9-FAIL", "partner identity (as CS-P) plus inward-only motion",
             "Lagrangian cut M_L(q) <= M_b,gal/f_b: M_L latched from its own turnaround field is clean, M_b,gal is species-split "
             "(G9-TENSION), f_b a coefficient; and the cut IS the R1 assumption, not retention physics"),
    "CS-0": ("G9-FAIL", "partner identity", "as CS-I"),
    "CS-M": ("G9-FAIL", "partner identity and the galaxy's baryon mass at each accretion",
             "needs M_b,gal(t) along the history: species-split (G9-TENSION) and per-shell identity (FAIL)"),
    "CS-F": ("G9-FAIL", "as CS-M", "as CS-M"),
}
P("\n  classification (literal rule | best gravitational surrogate):")
for k, (c, why, sur) in G9CLASS.items():
    P(f"    {k}: {c} ({why}) | surrogate: {sur}")
CRIT3 = {k: v[0] == "G9-CLEAN" for k, v in G9CLASS.items()}
R["g9"] = {"rows": {str(k): v for k, v in g9rows.items()}, "class": {k: {"literal": v[0], "why": v[1], "surrogate": v[2]}
                                                                      for k, v in G9CLASS.items()}, "crit3": CRIT3}


# ======================================================================================================== (4) depletion vs KiDS
P("\n" + "=" * 116)
P("(4) DEPLETION: LIVE (edge = x_e(S) r_M(present)) and SET (edge = r_M/ln(1 + f_ret/S)) on CFG413's KiDS lens groups")
P("=" * 116)
sys.path.insert(0, os.path.join(CFGDIR, "CFG100_kids_mass_rederivation"))
import cfg100_lib as L100  # noqa: E402  (read-only import, as CFG413)
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
zl = lens["z"].astype(float); Mgal = lens["Mgal"].astype(float)
WW = np.load(os.path.join(DATA, "cfg110_perlens.npz"))["WW"]
lmg = np.log10(Mgal)
key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(zl / 0.03).astype(np.int64)
_, gi, cnt = np.unique(key, return_inverse=True, return_counts=True)
gi = gi.ravel()
GM = 10 ** (np.bincount(gi, weights=lmg) / cnt); GZ = np.bincount(gi, weights=zl) / cnt
GW = np.bincount(gi, weights=WW.sum(1))
NG = len(cnt)


def wpct(v, w, p):
    o = np.argsort(v)
    cw = np.cumsum(w[o]) / w.sum()
    return float(np.interp(p / 100.0, cw, v[o]))


DEP = {"n_groups": int(NG), "n_lenses": int(len(zl))}
t_ = time.time()
for f in FOOTS:
    a0 = L100.A0[f]
    rta = np.array([L100.r_ta_law(GM[g], a0, GZ[g]) for g in range(NG)])
    rM = np.sqrt(L100.G_MPC * GM / a0)
    xr = rM / rta                                                     # r_M / r_ta per group
    x_live = x_exhaust(SHARE) * xr
    med_live = wpct(x_live, GW, 50)

    def med_set(fr):
        return wpct(xr / np.log(1.0 + fr / SHARE), GW, 50)

    f05 = math.exp(brentq(lambda lf: med_set(math.exp(lf)) - 0.5, math.log(1e-4), 0.0))
    f03 = math.exp(brentq(lambda lf: med_set(math.exp(lf)) - 0.3, math.log(1e-4), 0.0))
    census = {fr: med_set(fr) for fr in (0.07, 0.10, 0.18, 0.3, 0.5)}
    DEP[f] = {"median_rta_Mpc": wpct(rta, GW, 50), "median_rM_over_rta": wpct(xr, GW, 50),
              "live_median": med_live, "live_p16": wpct(x_live, GW, 16), "live_p84": wpct(x_live, GW, 84),
              "live_frac_in_window": float(GW[(x_live >= 0.3) & (x_live <= 0.5)].sum() / GW.sum()),
              "set_f_for_0.5": f05, "set_f_for_0.3": f03, "set_median_at_f": census,
              "set_edge_rM_at_f": {fr: 1.0 / math.log(1 + fr / SHARE) for fr in (1.0, 0.5, 0.3, 0.18, 0.10, 0.07)}}
    P(f"  {f:9s}: {NG} groups; weighted median r_ta = {DEP[f]['median_rta_Mpc']:.3f} Mpc, r_M/r_ta = {DEP[f]['median_rM_over_rta']:.4f}")
    P(f"             LIVE: x_edge = {x_exhaust(SHARE):.3f} r_M -> median {med_live:.4f} r_ta (16-84%: {DEP[f]['live_p16']:.4f}-"
      f"{DEP[f]['live_p84']:.4f}); weight in [0.3, 0.5]: {DEP[f]['live_frac_in_window']:.3f}")
    P(f"             SET: median x_edge = 0.5 at f_ret = {f05:.4f}, = 0.3 at f_ret = {f03:.4f}; at f_ret 0.07 / 0.10 / 0.18 / 0.3 / 0.5: "
      + " / ".join(f"{census[k]:.3f}" for k in (0.07, 0.10, 0.18, 0.3, 0.5)))
P(f"  (r_ta per group from cfg100 r_ta_law, {time.time() - t_:.0f} s)")
LIVE_LABEL = "MATCH" if all(0.3 <= DEP[f]["live_median"] <= 0.5 for f in FOOTS) else "MISS"
SET_LABEL = "CONDITIONAL"
P(f"  SET edge in r_M: " + ", ".join(f"f_ret {k}: {v:.1f}" for k, v in DEP['canonical']['set_edge_rM_at_f'].items()))
P(f"  (4) labels: LIVE {LIVE_LABEL}; SET {SET_LABEL} (needs f_ret,gal {DEP['canonical']['set_f_for_0.5']:.3f}-"
  f"{DEP['canonical']['set_f_for_0.3']:.3f} canonical / {DEP['alt']['set_f_for_0.5']:.3f}-{DEP['alt']['set_f_for_0.3']:.3f} alt;"
  f" PAPER45 v1 census 0.07-0.10 is halo-level, and co-settling has f_ret,gal >= census)")
DEP["labels"] = {"LIVE": LIVE_LABEL, "SET": SET_LABEL}
R["depletion"] = DEP


# ======================================================================================================== verdicts
P("\n" + "=" * 116)
P("VERDICT TABLE")
P("=" * 116)
CRIT1, REQF = {}, {}
for nm in ("CS-P", "CS-M", "CS-F"):
    d = SF[nm]
    CRIT1[nm] = bool(d["p1"] and d["p1b"])
    REQF[nm] = bool(REQ[nm] and REQ_hist) if nm == "CS-P" else bool(REQ[nm])
for nm in ("CS-I", "CS-0"):
    CRIT1[nm] = any(PV[nm][q]["p1"] and PV[nm][q]["p1b"] for q in QS)
    REQF[nm] = False
P(f"  {'reading':7s} {'(1) edge+law':>13s} {'R-EQ':>5s} {'(2) clusters':>13s} {'(3) G9':>9s}")
for nm in ("CS-P", "CS-I", "CS-0", "CS-M", "CS-F"):
    P(f"  {nm:7s} {('PASS' if CRIT1[nm] else 'FAIL'):>13s} {('yes' if REQF[nm] else 'no'):>5s} "
      f"{('PASS' if CRIT2[nm] else 'FAIL'):>13s} {G9CLASS[nm][0]:>9s}")
all3 = [nm for nm in CRIT1 if CRIT1[nm] and CRIT2[nm] and CRIT3[nm]]
c1 = [nm for nm in CRIT1 if CRIT1[nm]]
if all3:
    VERDICT = "PASS"
elif c1 and all(REQF[nm] for nm in c1):
    VERDICT = "FAIL (RESTATEMENT ONLY)"
else:
    VERDICT = "FAIL"
P(f"\n  LANE VERDICT: {VERDICT}" + ("" if not MUT else "   [MUTATE run: scored against the TRUE r_edge; see the teeth below]"))
P(f"  (4): LIVE {LIVE_LABEL}, SET {SET_LABEL}")
R["verdict"] = VERDICT
R["criteria"] = {"crit1": CRIT1, "req": REQF, "crit2": CRIT2, "crit3": CRIT3}

# ======================================================================================================== MUTATE teeth / f_b-test
rc = 0 if (K1 and K2 and K3 and K4 and K5) else 1
if MUT:
    P("\n" + "=" * 116)
    P("MUTATE TEETH: Omega_c/Omega_b x 2; predicted shifts vs the main run")
    P("=" * 116)
    main_path = os.path.join(HERE, "cfg488_results.json")
    teeth = False
    if os.path.exists(main_path):
        Rm = json.load(open(main_path))
        dS = math.log10(x_exhaust(SHARE) / x_exhaust(SHARE_TRUE))
        dK = math.log10(x_marginal(SHARE) / x_marginal(SHARE_TRUE))
        pred = {"CS-P": dS, "CS-F": dS, "CS-M": dK, "CS-I": dS, "CS-0": dS}
        moved, failp1 = {}, {}
        for nm in ("CS-P", "CS-M", "CS-F"):
            sh = SF[nm]["dex"] - Rm["formulations"]["scale_free_point"][nm]["dex"]
            moved[nm] = abs(sh - pred[nm]) <= TOL_MUT
            failp1[nm] = not SF[nm]["p1"]
            P(f"  {nm}: shift {sh:+.4f} dex (predicted {pred[nm]:+.4f}) -> {'as predicted' if moved[nm] else 'NOT as predicted'};"
              f" mutated edge {SF[nm]['dex']:+.4f} vs true r_edge -> P1 {'fails' if failp1[nm] else 'passes'}")
        for nm in ("CS-I", "CS-0"):
            shs = []
            for q in QS:
                for l in LOGMB:
                    for f in FOOTS:
                        shs.append(POOL[(q, l, f)][nm]["dex"] - Rm["formulations"]["pool_HN"][f"q{q}_{l:.1f}_{f}"][nm]["dex"])
            moved[nm] = all(abs(s - pred[nm]) <= TOL_MUT for s in shs)
            failp1[nm] = not CRIT1[nm]
            P(f"  {nm}: shifts {min(shs):+.3f} .. {max(shs):+.3f} dex over q x cells (supply-keyed prediction {pred[nm]:+.4f})"
              f" -> {'as predicted' if moved[nm] else 'NOT as predicted'}")
        main_p1 = [nm for nm, v in Rm["criteria"]["crit1"].items() if v]
        teeth = moved["CS-P"] and failp1["CS-P"] and all(moved[nm] and failp1[nm] for nm in main_p1)
        fb_main, fb_mut = 1 / (1 + SHARE_TRUE), FB
        fbt = {nm: -2 * (SF[nm]["dex"] - Rm["formulations"]["scale_free_point"][nm]["dex"]) * math.log(10) /
               math.log(fb_mut / fb_main) for nm in ("CS-P", "CS-M", "CS-F")}
        P(f"  f_b-test d ln y_e/d ln f_b (finite difference over the MUTATE pair; 2.18 = local value for a genuine nu = Om/Ob edge): "
          + ", ".join(f"{k} {v:.3f}" for k, v in fbt.items()))
        P(f"  (2) under MUTATE: in-place u = " + ", ".join(f"{f} {CL[f]['u_inplace']:.4f} (range {CL[f]['u_rec_range'][0]:.4f}-"
                                                        f"{CL[f]['u_rec_range'][1]:.4f})" for f in FOOTS))
        R["mutate_teeth"] = {"pred": pred, "moved": moved, "fail_p1": failp1, "main_p1_passers": main_p1, "detected": teeth,
                             "fb_test": fbt}
    else:
        P("  main-run results not found; run the main mode first")
    P(f"\n  TEETH {'DETECTED' if teeth else 'NOT DETECTED'}")
    rc = 1 if teeth else 0
P(f"\nControls: K1 {K1}  K2 {K2}  K3 {K3}  K4 {K4}  K5 {K5}  K6 {K6} (reported)")
P(f"exit code {rc}")
R["exit_code"] = rc
json.dump(jsafe(R), open(os.path.join(HERE, f"cfg488_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg488{TAG}.out"), "w").write("\n".join(_LOG) + "\n")
sys.exit(rc)
