#!/usr/bin/env python3
"""AN1: spherical collapse of the one-field action's dust, slow branch (Q0 -> infinity).
Criteria: FROZEN_CRITERIA.md. Run: python3 an1.py checks|rows|conv [--mutate]
kappa = 1/2 FITTED. Gravitating field, no particle. No completion past a fold."""
import os, sys, json, time, signal, resource
import numpy as np
from scipy.linalg import solve_banded
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

G = 4.30091e-6          # kpc (km/s)^2 / Msun
TU = 0.97779            # Gyr per kpc/(km/s)
MS2 = 3.24078e-14       # m/s^2 per (km/s)^2/kpc
AF = {"canonical": 9.3603e-11 / MS2, "alt": 1.1312e-10 / MS2}
CK = 299792.458
H_ = 0.672
RX0, RB0 = 33.2, 33.2 / 5.35   # Msun/kpc^3 comoving (RF5/UX2 native)
MUTATE = "--mutate" in sys.argv
SIGN = -1.0 if MUTATE else 1.0
TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__))
_STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda *a: _STOP.__setitem__("flag", True))


class Bg:
    def __init__(s, rm0=RX0 + RB0, h=H_, eds=False):
        s.H0 = 0.1 * h
        rc = 3 * s.H0**2 / (8 * np.pi * G)
        s.rm0 = rm0
        s.Om = 1.0 if eds else rm0 / rc
        s.OL = 0.0 if eds else 1 - s.Om
        s.eds = eds

    def a(s, t):
        if s.OL == 0:
            return (1.5 * np.sqrt(s.Om) * s.H0 * t) ** (2 / 3)
        q = 1.5 * np.sqrt(s.OL) * s.H0 * t
        return (s.Om / s.OL) ** (1 / 3) * np.sinh(q) ** (2 / 3)

    def t(s, a):
        if s.OL == 0:
            return a**1.5 / (1.5 * np.sqrt(s.Om) * s.H0)
        return np.arcsinh(np.sqrt(s.OL / s.Om) * a**1.5) / (1.5 * np.sqrt(s.OL) * s.H0)

    def H(s, a):
        return s.H0 * np.sqrt(s.Om / a**3 + s.OL)


def gbar(x):
    """mean of exp(-q^2/2R^2) inside q, x=q/R"""
    x = np.asarray(x, float)
    out = np.ones_like(x)
    m = x > 1e-3
    from scipy.special import erf
    xx = x[m]
    out[m] = 3 / xx**3 * (np.sqrt(np.pi / 2) * erf(xx / np.sqrt(2)) - xx * np.exp(-xx**2 / 2))
    out[~m] = 1 - 3 * x[~m] ** 2 / 10
    return out


def shell_collapse_t(bg, M, r0, v0, t0, tmax):
    L = bg.OL * bg.H0**2
    f = lambda t, y: [y[1], -G * M / y[0] ** 2 + L * y[0]]
    ev = lambda t, y: y[0] - 1e-5 * r0
    ev.terminal = True
    s = solve_ivp(f, (t0, tmax), [r0, v0], events=ev, rtol=1e-10, atol=1e-12 * r0, method="DOP853")
    return s.t_events[0][0] if len(s.t_events[0]) else np.inf


def edge_amp(bg, Mtot, zi):
    """delta_bar at q(Mtot), z_i, so the shell in pure dust collapses at z=0"""
    ai = 1 / (1 + zi)
    q = (3 * Mtot / (4 * np.pi * bg.rm0)) ** (1 / 3)
    ti, Hi, t0 = bg.t(ai), bg.H(ai), bg.t(1.0)
    def F(d):
        r = ai * q * (1 - d / 3)
        v = Hi * ai * q * (1 - 2 * d / 3)
        return shell_collapse_t(bg, Mtot, r, v, ti, 3 * t0) - t0
    return brentq(F, 1e-3, 0.5, xtol=1e-8), q


# ---------- hold equation
class Hold:
    def __init__(s, a0, mu, KB=0.0, neumann=False):
        s.a0, s.mu2, s.kap, s.neu = a0, mu * mu, KB / (2 - KB), neumann
        s.warn = 0
        s.nit = 0

    def Vf(s, E):
        return E / (1 + np.abs(E) / s.a0) + s.kap * E

    def dV(s, E):
        return 1 / (1 + np.abs(E) / s.a0) ** 2 + s.kap

    def Wf(s, E):
        y = np.abs(E) / s.a0
        w = np.where(y < 1e-4, y**2 / 2 - y**3 / 3, y - np.log1p(np.where(y < 1e-4, 0, y)))
        return s.a0**2 * w + 0.5 * s.kap * E**2

    def geom(s, r):
        rc = 0.5 * (r[1:] + r[:-1])
        dV3 = (r[1:] ** 3 - r[:-1] ** 3) / 3
        # A1: node spacing from the cell second moment, exact for a quadratic density at the centre
        m2 = 0.6 * (r[1:] ** 5 - r[:-1] ** 5) / (r[1:] ** 3 - r[:-1] ** 3)
        D = (m2[1:] - m2[:-1]) / (2 * r[1:-1])
        Dout = r[-1] - rc[-1]
        return rc, dV3, D, Dout

    def obj(s, u, r, dV3, D, Dout, S, uo):
        Ei = -(u[1:] - u[:-1]) / D
        val = np.sum(r[1:-1] ** 2 * D * s.Wf(Ei)) + np.sum(0.5 * s.mu2 * dV3 * u**2 - S * u)
        if not s.neu:
            Eo = -(uo - u[-1]) / Dout
            val += r[-1] ** 2 * Dout * s.Wf(np.array([Eo]))[0]
        return val

    def solve(s, u, r, S, uo=0.0, tol=1e-8, maxit=60):
        rc, dV3, D, Dout = s.geom(r)
        rr = r[1:-1] ** 2
        N = len(u)
        J = np.zeros(N + 1)
        for it in range(maxit):
            Ei = -(u[1:] - u[:-1]) / D
            J[1:-1] = rr * s.Vf(Ei)
            Eo = 0.0
            if not s.neu:
                Eo = -(uo - u[-1]) / Dout
                J[-1] = r[-1] ** 2 * s.Vf(np.array([Eo]))[0]
            mt = s.mu2 * dV3 * u
            R = J[1:] - J[:-1] + mt - S
            sc = np.abs(S) + np.abs(J[1:]) + np.abs(J[:-1]) + np.abs(mt) + 1e-300
            res = np.max(np.abs(R) / sc)
            s.nit += 1
            if res < tol:
                return u, res
            c = rr * s.dV(Ei) / D
            diag = s.mu2 * dV3 + 1e-300
            diag = diag.copy()
            diag[:-1] += c
            diag[1:] += c
            if not s.neu:
                diag[-1] += r[-1] ** 2 * s.dV(np.array([Eo]))[0] / Dout
            ab = np.zeros((3, N))
            ab[0, 1:] = -c
            ab[1] = diag
            ab[2, :-1] = -c
            du = solve_banded((1, 1), ab, -R, check_finite=False)
            f0 = s.obj(u, r, dV3, D, Dout, S, uo)
            slope = np.dot(R, du)
            lam = 1.0
            for _ in range(40):
                un = u + lam * du
                if s.obj(un, r, dV3, D, Dout, S, uo) <= f0 + 1e-4 * lam * slope + 1e-13 * abs(f0):
                    break
                lam *= 0.5
            u = u + lam * du
        s.warn += 1
        return u, res


# ---------- engine
class Run:
    def __init__(s, r, v, dm, a0, mu, KB=0.0, bg=None, rbarf=0.0, neumann=False, Mb_fn=None,
                 rb=None, vb=None, mb=None, rf=None, ref=None, eta=0.005, uo=0.0, pin_turn=False, Mseed=0.0):
        s.r, s.v, s.dm = r.copy(), v.copy(), dm
        s.m = np.concatenate([[0], np.cumsum(dm)])
        s.a0, s.mu, s.KB, s.bg, s.rbarf = a0, mu, KB, bg, rbarf
        s.hold = Hold(a0, mu, KB, neumann)
        s.u = np.zeros(len(dm))
        s.Mb_fn = Mb_fn
        s.rb, s.vb, s.mb, s.rf = rb, vb, mb, rf
        s.pinb = None if rb is None else np.zeros(len(rb), bool)
        s.ref = ref
        s.eta = eta
        s.uo = uo
        s.Lam = 0.0 if bg is None else bg.OL * bg.H0**2
        s.nstep = 0
        s.t = 0.0
        s.turned = False
        s.pin_turn = pin_turn
        s.pinf = np.zeros(len(r), bool)
        s.pinf[0] = True
        s.ta = np.full(len(r), np.nan)
        s.Mseed = Mseed
        s.ta_r = np.full(len(r), np.nan)

    def aval(s):
        return 1.0 if s.bg is None else s.bg.a(s.t)

    def Mb(s, x):
        if s.Mb_fn is not None:
            return s.Mb_fn(x)
        if s.rb is None:
            return s.Mseed
        # A1: continuous enclosed mass; baryon shells sit at q cell centres, not on field nodes
        o = np.argsort(s.rb)
        c = np.cumsum(s.mb[o]) - 0.5 * s.mb[o]
        return np.interp(x, np.concatenate([[0.0], s.rb[o]]), np.concatenate([[0.0], c]))

    def forces(s, tol=1e-8):
        r = s.r
        dV3 = (r[1:] ** 3 - r[:-1] ** 3) / 3
        if s.bg is not None:
            S = G * (s.dm - s.rbarf / s.aval() ** 3 * 4 * np.pi * dV3)
        else:
            S = G * s.dm
        s.u, s.res = s.hold.solve(s.u, r, S, s.uo, tol=tol)
        rc, _, D, _ = s.hold.geom(r)
        E = np.zeros_like(r)
        E[1:-1] = -(s.u[1:] - s.u[:-1]) / D
        if s.hold.neu:
            E[-1] = 0.0
        else:
            E[-1] = -(s.uo - s.u[-1]) / (r[-1] - rc[-1])
        s.E = E
        f = 1 - s.KB / 2
        g = np.zeros_like(r)
        g[1:] = f * G * (s.Mb(r[1:]) + s.m[1:]) / r[1:] ** 2
        s.g = g
        F = -g + SIGN * E + s.Lam * r
        F[0] = 0.0
        F[s.pinf] = 0.0
        s.F = F
        if s.rb is not None:
            s.gb = f * G * (s.Mb(s.rb) + np.interp(s.rb, r, s.m)) / s.rb**2 - s.Lam * s.rb
        return F

    def dt(s, tmax):
        r, v, F = s.r, s.v, s.F
        dr = np.diff(r)
        dv = np.diff(v)
        dF = np.diff(F)
        rho = s.dm / (4 * np.pi * (r[1:] ** 3 - r[:-1] ** 3) / 3)
        k = np.pi / dr
        Em = 0.5 * np.abs(s.E[1:] + s.E[:-1])
        cL = 1 / (1 + Em / s.a0) ** 2 + s.hold.kap
        om2 = 4 * np.pi * G * rho * k**2 / (k**2 * cL + s.mu**2)
        om2 = np.maximum(om2, 4 * np.pi * G * rho * np.abs(k**2 / (k**2 * cL + s.mu**2) - 1))
        ts = [0.5 / np.sqrt(np.max(om2) + 1e-300)]
        ts.append(s.eta * np.min(dr / (np.abs(dv) + 1e-30)))
        ts.append(s.eta * np.sqrt(np.min(dr / (np.abs(dF) + 1e-30))))
        ts.append(s.eta * np.min(r[1:] / (np.abs(v[1:]) + 1e-30)))
        ts.append(s.eta * np.sqrt(np.min(r[1:] / (np.abs(F[1:]) + 1e-30))))
        if s.rb is not None:
            fly = ~s.pinb
            if fly.any():
                ts.append(s.eta * np.min(s.rb[fly] / (np.abs(s.vb[fly]) + 1e-30)))
                ts.append(s.eta * np.sqrt(np.min(s.rb[fly] / (np.abs(s.gb[fly]) + 1e-30))))
        return min(min(ts), tmax - s.t)

    def step(s, tmax):
        if not hasattr(s, "F"):
            s.forces()
        dt = s.dt(tmax)
        s.v += 0.5 * dt * s.F
        s.r += dt * s.v
        s.r[0] = 0.0
        if s.rb is not None:
            fly = ~s.pinb
            s.vb[fly] -= 0.5 * dt * s.gb[fly]
            s.rb[fly] += dt * s.vb[fly]
            fin = np.isfinite(s.rf)
            hit = fly & (s.vb <= 0) & ((fin & (s.rb <= s.rf)) | ~fin)
            # finite-rf shell that turns around below rf stops there (gas does not rise)
            s.rb[hit & np.isfinite(s.rf)] = s.rf[hit & np.isfinite(s.rf)]
            s.vb[hit] = 0.0
            s.pinb |= hit
        s.t += dt
        if not np.all(np.diff(s.r) > 0):
            s.crossed = True
            return dt
        s.forces()
        s.v += 0.5 * dt * s.F
        s.v[0] = 0.0
        if s.rb is not None:
            fly = ~s.pinb
            s.vb[fly] -= 0.5 * dt * s.gb[fly]
        s.nstep += 1
        if not s.turned and s.v[1] <= 0:
            s.turned = True
            s.t_turn = s.t
        if s.pin_turn:
            nw = (~s.pinf) & (s.v <= 0)
            s.ta[nw] = s.t
            s.ta_r[nw] = s.r[nw]
            s.pinf |= nw
            s.v[s.pinf] = 0.0
        return dt

    def fold(s, Cf, dq):
        dr = np.diff(s.r)
        dv = np.diff(s.v)
        C = dr / (s.aval() * dq)
        i = int(np.argmin(C))
        if C[i] < Cf and dv[i] < 0:
            return i, s.t + dr[i] / abs(dv[i])
        return None

    def save(s, path):
        d = {k: getattr(s, k) for k in ("r", "v", "u", "t", "nstep", "turned")}
        if s.rb is not None:
            d.update(rb=s.rb, vb=s.vb, pinb=s.pinb)
        np.savez(path, **d)

    def load(s, path):
        d = np.load(path)
        s.r, s.v, s.u, s.t, s.nstep, s.turned = d["r"], d["v"], d["u"], float(d["t"]), int(d["nstep"]), bool(d["turned"])
        if s.rb is not None:
            s.rb, s.vb, s.pinb = d["rb"], d["vb"], d["pinb"]
        if hasattr(s, "F"):
            del s.F


def glaw(gN, a0):
    return 0.5 * (gN + np.sqrt(gN**2 + 4 * gN * a0))


SETUP = {
    "1e12": dict(M=1e12, Rt=36.0, Rs=[7.84, 36.0], names=["2.2Rd", "Rlast"]),
    "1e15": dict(M=1e15, Rt=1350.0, Rs=[405.0, 945.0, 1350.0], names=["0.3R500", "0.7R500", "R500"]),
}


def stop_radii(key, mb):
    cum = np.cumsum(mb)
    rf = np.full_like(mb, np.inf)
    if key == "1e12":
        Md, Rd = 6.72e10, 3.565
        x = np.logspace(-4, 2, 4000)
        M = Md * (1 - (1 + x) * np.exp(-x))
        s = cum <= Md * 0.9999
        rf[s] = Rd * np.interp(cum[s], M, x)
    else:
        R5, rcg, Mg = 1350.0, 0.15 * 1350.0, 1.19e14
        x = np.logspace(-3, np.log10(R5), 4000)
        P = lambda r: r - rcg * np.arctan(r / rcg)
        M = Mg * P(x) / P(R5)
        s = cum <= Mg
        rf[s] = np.interp(cum[s], M, x)
    return rf


def build(key, mu_Mpc, foot, N=1500, amp=1.0, MGdiv=1.0, KB=0.0, eta=0.005, zi=20.0):
    st = SETUP[key]
    bg = Bg()
    M = st["M"]
    de, qt = edge_amp(bg, M, zi)
    RG = (M / MGdiv / ((2 * np.pi) ** 1.5 * bg.rm0)) ** (1 / 3)
    d0 = de / gbar(np.array([qt / RG]))[0] * amp
    qe = np.linspace(0, 2 * qt, N + 1)
    ai = 1 / (1 + zi)
    Hi = bg.H(ai)
    db = d0 * gbar(qe / RG)
    r = ai * qe * (1 - db / 3)
    v = Hi * ai * qe * (1 - 2 * db / 3)
    dm = 4 * np.pi / 3 * RX0 * (qe[1:] ** 3 - qe[:-1] ** 3)
    mb = 4 * np.pi / 3 * RB0 * (qe[1:] ** 3 - qe[:-1] ** 3)
    rf = stop_radii(key, mb)
    qb = 0.5 * (qe[1:] + qe[:-1])
    dbb = d0 * gbar(qb / RG)
    rb0 = ai * qb * (1 - dbb / 3)
    vb0 = Hi * ai * qb * (1 - 2 * dbb / 3)
    a0 = AF[foot]
    mu = mu_Mpc * 1e-3
    R = Run(r, v, dm, a0, mu, KB=KB, bg=bg, rbarf=RX0, rb=rb0, vb=vb0, mb=mb, rf=rf, eta=eta)
    R.t = bg.t(ai)
    R.dq = qe[1] - qe[0]
    R.t0 = bg.t(1.0)
    R.meta = dict(d0=float(d0), de=float(de), qt=float(qt), RG=float(RG))
    return R


def diag(R, key):
    st = SETUP[key]
    bg = R.bg
    o = np.argsort(R.r)
    out = {}
    for nm, X in zip(st["names"], st["Rs"]):
        Md = float(np.interp(X, R.r[o], R.m[o]))
        Mb = float(R.Mb(np.array([X]))[0])
        gN = G * Mb / X**2
        gl = glaw(gN, R.a0)
        Mph = (gl - gN) * X**2 / G
        out[nm] = dict(R=X, Md=Md, Mb=Mb, Mph=Mph, ex_over_Mb=(Md - Mph) / Mb if Mb > 0 else None,
                       Md_over_Mb=Md / Mb if Mb > 0 else None)
    Rt = st["Rt"]
    idx = np.where(R.r[1:] <= Rt)[0] + 1
    d = dict(masses=out)
    if len(idx):
        gt = R.g[idx]
        Vc = np.sqrt(np.maximum(gt * R.r[idx], 1e-30))
        d["max_F_over_g"] = float(np.max(np.abs(R.F[idx]) / gt))
        d["max_v_over_Vc"] = float(np.max(np.abs(R.v[idx]) / Vc))
        d["E_over_g_Rt"] = float(R.E[idx[-1]] / gt[-1])
        d["Q0_need_perMpc"] = float(np.max(gt / (CK * Vc)) * 1e3)
    else:
        d["max_F_over_g"] = d["max_v_over_Vc"] = None
    d["baryon_stopped_on_profile"] = float(np.sum(R.mb[R.pinb & np.isfinite(R.rf)]) / np.sum(R.mb[np.isfinite(R.rf)]))
    return d


def integrate(R, tmax, Cf=1e-2, nmax=400000, wall=1200.0, ckpt=None, fold_on=True, kill_at=None):
    t0w = time.time()
    if ckpt and os.path.exists(ckpt):
        R.load(ckpt)
    R.forces()
    status = None
    while R.t < tmax - 1e-12:
        if kill_at is not None and R.nstep == kill_at:
            _STOP["flag"] = True
        if _STOP["flag"]:
            if ckpt:
                R.save(ckpt)
            return dict(status="PREEMPTED")
        R.step(tmax)
        if getattr(R, "crossed", False):
            status = dict(status="FOLD", i=int(np.argmin(np.diff(R.r))), t_fold=R.t, crossed_in_step=True)
            break
        if fold_on:
            f = R.fold(Cf, R.dq)
            if f:
                status = dict(status="FOLD", i=f[0], t_fold=f[1])
                break
        if R.nstep >= nmax or time.time() - t0w > wall:
            status = dict(status="UNRESOLVED", reason="budget")
            break
    if status is None:
        status = dict(status="END")
    status.update(t=R.t, nstep=R.nstep, turned=R.turned, wall=time.time() - t0w, newton_warn=R.hold.warn, nit=R.hold.nit)
    if ckpt and os.path.exists(ckpt):
        os.remove(ckpt)
    return status


def run_row(key, mu, foot, N=1500, amp=1.0, MGdiv=1.0, KB=0.0, eta=0.005, ckpt=None, kill_at=None, wall=1200.0):
    R = build(key, mu, foot, N, amp, MGdiv, KB, eta)
    s = integrate(R, R.t0, ckpt=ckpt, kill_at=kill_at, wall=wall)
    if s["status"] == "PREEMPTED":
        return s
    bg = R.bg
    out = dict(key=key, mu=mu, foot=foot, N=N, amp=amp, MGdiv=MGdiv, KB=KB, eta=eta, **R.meta, **s)
    hbar = 4 * np.pi * G * RX0 * (1 + 20.0) ** 3 / (mu * 1e-3) ** 2 / CK**2
    out["hbar_zi_over_c2"] = float(hbar)
    out["polytrope_R_kpc"] = float(np.pi / (mu * 1e-3))
    if not (np.all(np.isfinite(R.r))):
        out["status"] = "UNRESOLVED"
        return out
    R.forces(tol=1e-6) if np.all(np.diff(R.r) > 0) else None
    out.update(diag(R, key))
    if s["status"] == "FOLD":
        i = s["i"]
        tf = min(s["t_fold"], R.t0 * 2)
        out["t_fold_Gyr"] = float(tf * TU)
        af = bg.a(min(tf, R.t0))
        out["z_fold"] = float(1 / af - 1)
        out["r_fold_kpc"] = float(0.5 * (R.r[i] + R.r[i + 1]))
        out["m_fold"] = float(R.m[i + 1])
        out["cell_fold"] = i
        out["grid_limited"] = bool(i < 3)
        out["edge_artefact"] = bool(i >= 0.95 * N)
        out["label"] = "FOLD FIRST"
    elif s["status"] == "END":
        if not R.turned:
            out["label"] = "NO COLLAPSE"
        else:
            ok = out.get("max_F_over_g") is not None and out["max_F_over_g"] <= 0.1 and out["max_v_over_Vc"] <= 0.1
            out["label"] = "SETTLED" if ok else "OSCILLATING"
    else:
        out["label"] = "UNRESOLVED"
    return out


# ---------- held start
def static_branch(key, mu_Mpc, foot, N=1200):
    """H2's static system with Psi(R_out)=0 by shooting; returns radii, M_b fn, M_d, E"""
    a0 = AF[foot]
    mu = mu_Mpc * 1e-3
    if key == "1e12":
        Rout = 300.0
        Md, Rd = 6.72e10, 3.565
        MB = lambda r: Md * (1 - (1 + r / Rd) * np.exp(-r / Rd))
    else:
        Rout = 3000.0
        R5, rcg, Mg = 1350.0, 202.5, 1.19e14
        P = lambda r: r - rcg * np.arctan(r / rcg)
        MB = lambda r: Mg * P(r) / P(R5)
    def rhs(r, y, ):
        h, Mh = y
        gN = G * (MB(r) + Mh) / r**2
        gt = glaw(max(gN, 0.0), a0) if gN >= 0 else -glaw(-gN, a0)
        return [-gt, mu**2 * h * r**2 / G]
    r0 = 1e-3 * Rout / 300
    def shoot(h0):
        s = solve_ivp(rhs, (r0, Rout), [h0, 0.0], rtol=1e-9, atol=[1e-6, 1.0], method="LSODA", dense_output=True)
        return s
    # Psi(R_out)=0 means h(R_out)=0, mu term included
    hi = 1.0
    f = lambda h0: shoot(h0).y[0, -1]
    lo = 0.0
    while f(hi) < 0:
        hi *= 2
    h0 = brentq(f, lo, hi, xtol=1e-6)
    s = shoot(h0)
    # field cells uniform in log r near the centre then linear: uniform in sqrt r
    x = np.linspace(np.sqrt(0.02 * Rout / 300), np.sqrt(Rout), N + 1) ** 2
    r = np.concatenate([[0.0], x])
    y = s.sol(x)
    h, Mh = y
    gN = G * (MB(x) + Mh) / x**2
    E = np.where(gN >= 0, glaw(np.abs(gN), a0), -glaw(np.abs(gN), a0))
    Mtot = E * x**2 / G
    Md = Mtot - MB(x)
    return dict(r=r, x=x, h=h, E=E, Md=Md, MB=MB, Rout=Rout, h0=h0, a0=a0, mu=mu)


def held_row(key, mu_Mpc, foot, kick=0.01, wall=1200.0):
    S = static_branch(key, mu_Mpc, foot)
    dm = np.diff(np.concatenate([[0.0], S["Md"]]))
    neg = np.where(dm <= 0)[0]
    r = S["r"]
    if len(neg):
        n = neg[0]
        trunc = float(r[n + 1]) if n > 0 else None
        if n < 50:
            return dict(key=key, mu=mu_Mpc, foot=foot, label="NOT RUN", reason=f"negative rho_d from r={trunc}")
        r = r[: n + 1]
        dm = dm[:n]
    hout = float(np.interp(r[-1], S["x"], S["h"]))
    Vc = np.sqrt(np.maximum(np.interp(r, S["x"], S["E"]) * r, 0.0))
    v = kick * Vc * np.sin(np.pi * r / r[-1])
    R = Run(r, v, dm, S["a0"], S["mu"], Mb_fn=S["MB"], uo=hout)
    R.u = np.interp(0.5 * (r[1:] + r[:-1]), S["x"], S["h"])
    R.dq = np.diff(r)
    R.forces()
    # outer shell frozen by construction of Dirichlet
    R.pinf[-1] = True
    F0 = R.F[1:-1].copy()
    R.dq = np.diff(r)
    Ef = float(np.max(np.abs(R.F[5:-5]) / R.g[5:-5]))
    tmax = 14.0 / TU
    s = integrate(R, tmax, wall=wall)
    out = dict(key=key, mu=mu_Mpc, foot=foot, max_F0_over_g=Ef, Rout=float(r[-1]), **s)
    if s["status"] == "FOLD":
        out["t_fold_Gyr"] = float(s["t_fold"] * TU)
        i = s["i"]
        out["r_fold_kpc"] = float(0.5 * (R.r[i] + R.r[i + 1]))
        out["label"] = "FOLD FIRST"
    elif s["status"] == "END":
        out["label"] = "HOLDS 14 Gyr"
    else:
        out["label"] = "UNRESOLVED"
    return out


# ---------- checks
def K0():
    import sympy as sp
    k, mu, K_B, rhob, rhod, Psi, x = sp.symbols("k mu K_B rho_b rho_d Psi x", positive=True)
    G_ = sp.symbols("G", positive=True)
    # linear, Fourier, E = grad Psi branch: hold + Poisson -> static eq with law's mu symbol M
    M = sp.symbols("M")   # law mu(x); V = (1-M) E
    kap = K_B / (2 - K_B)
    # hold: -k^2 (1-M+kap) (-Psi)... with Xi=Psi: -(k^2)(1-M+kap)Psi - mu^2 Psi = 4 pi G rho_d
    rd = (-(k**2) * (1 - M + kap) * Psi - mu**2 * Psi) / (4 * sp.pi * G_)
    # Poisson: -k^2 Psi = 4 pi G (1-K_B/2)(rho_b+rho_d)
    eq = -(k**2) * Psi - 4 * sp.pi * G_ * (1 - K_B / 2) * (rhob + rd)
    target = (1 - K_B / 2) * (-(k**2) * M * Psi + mu**2 * Psi - 4 * sp.pi * G_ * rhob)
    r1 = sp.simplify(eq - target)
    # hmm sign of the mu term: static equation div[M grad Psi] + mu^2 Psi = 4 pi G rho_b
    s_ = 1 - k**2 / (k**2 + mu**2)
    r2 = sp.simplify(s_ - mu**2 / (k**2 + mu**2))
    return dict(res_static=str(r1), res_kernel=str(r2), ok=bool(r1 == 0 and r2 == 0))


def K1():
    bg = Bg(rm0=RX0 + RB0)
    zi = 20.0
    ai = 1 / (1 + zi)
    Mt = 1e12
    qt = (3 * Mt / (4 * np.pi * bg.rm0)) ** (1 / 3)
    d = 0.15
    N = 600
    qe = np.linspace(0, 3 * qt, N + 1)
    db = np.where(qe < qt, d, d * (qt / np.maximum(qe, 1e-9)) ** 3)
    r = ai * qe * (1 - db / 3)
    v = bg.H(ai) * ai * qe * (1 - 2 * db / 3)
    dm = 4 * np.pi / 3 * bg.rm0 * np.diff(qe**3)
    R = Run(r, v, dm, AF["canonical"], 1.24e8 * 1e-3, bg=bg, rbarf=bg.rm0)
    R.t = bg.t(ai)
    R.dq = qe[1] - qe[0]
    s = integrate(R, 3 * bg.t(1.0))
    i = 30
    Mi = 4 * np.pi / 3 * bg.rm0 * qe[i] ** 3
    tex = shell_collapse_t(bg, Mi, r[i], v[i], bg.t(ai), 3 * bg.t(1.0))
    err = (s.get("t_fold", np.inf) - tex) / tex
    return dict(t_fold=s.get("t_fold"), t_exact=tex, err=float(err), ok=bool(abs(err) <= 3e-3), status=s["status"])


def K2():
    bg = Bg(rm0=RX0 + RB0, eds=True)
    bg.rm0 = 3 * bg.H0**2 / (8 * np.pi * G)
    zi = 1000.0
    ai = 1 / (1 + zi)
    Mc = 1e8
    N = 500
    mlo, mhi = 30 * Mc, 3e4 * Mc
    q0 = (3 * mlo / (4 * np.pi * bg.rm0)) ** (1 / 3)
    q1 = (3 * mhi / (4 * np.pi * bg.rm0)) ** (1 / 3)
    qe = np.concatenate([[0.0], np.linspace(q0, q1, N)])
    m = 4 * np.pi / 3 * bg.rm0 * qe**3
    db = np.zeros_like(qe)
    db[1:] = Mc / m[1:]
    r = ai * qe * (1 - db / 3)
    v = bg.H(ai) * ai * qe * (1 - 2 * db / 3)
    dm = np.diff(m)
    R = Run(r, v, dm, AF["canonical"], 1.24e8 * 1e-3, bg=bg, rbarf=bg.rm0, pin_turn=True, Mseed=Mc)
    R.t = bg.t(ai)
    R.dq = np.diff(qe)
    s = integrate(R, bg.t(1.0), fold_on=False, nmax=400000)
    g = np.isfinite(R.ta)
    ta, rt = R.ta[g], R.ta_r[g]
    if g.sum() < 20:
        return dict(ok=False, n=int(g.sum()), status=s["status"])
    lt, lr = np.log10(ta), np.log10(rt)
    sel = lt > lt.max() - 1.0
    sl = np.polyfit(lt[sel], lr[sel], 1)[0]
    return dict(slope=float(sl), span_dex=float(lt.max() - lt.min()), ok=bool(abs(sl - 8 / 9) <= 0.01 and lt.max() - lt.min() >= 1.0), status=s["status"], n=int(g.sum()))


def K3():
    mu = 1e-3
    a0 = AF["canonical"] * 1e-6
    rc = 1e11
    N = 400
    R0 = 0.995 * np.pi / mu
    r = np.linspace(0, R0, N + 1)
    Mf = lambda x: 4 * np.pi * rc / mu**3 * (np.sin(mu * x) - mu * x * np.cos(mu * x))
    M = Mf(r)
    dm = np.diff(M)
    R = Run(r, np.zeros(N + 1), dm, a0, mu, neumann=True)
    R.dq = np.diff(r)
    R.forces(tol=1e-10)
    sel = (r > 0) & (r < 0.9 * np.pi / mu)
    fr = float(np.max(np.abs(R.F[sel]) / R.g[sel]))
    tdyn = 1 / np.sqrt(4 * np.pi * G * rc)
    i50 = int(np.searchsorted(R.m, 0.5 * R.m[-1]))
    r50 = R.r[i50]
    R.pinf[-1] = True
    s = integrate(R, tdyn, fold_on=False, nmax=100000)
    dr = abs(R.r[i50] - r50) / r50 if np.isfinite(R.r[i50]) else np.inf
    return dict(max_F_over_g=fr, r50_drift=float(dr), ok=bool(fr <= 5e-3 and dr <= 0.02), status=s["status"])


def K4():
    out = {}
    ok = True
    for foot in AF:
        S = static_branch("1e12", 0.1, foot)
        dm = np.diff(np.concatenate([[0.0], S["Md"]]))
        r = S["r"]
        R = Run(r, np.zeros_like(r), dm, S["a0"], S["mu"], Mb_fn=S["MB"], uo=float(S["h"][-1]))
        R.u = np.interp(0.5 * (r[1:] + r[:-1]), S["x"], S["h"])
        R.forces(tol=1e-10)
        sel = (r >= 1) & (r <= 100)
        err = np.abs(R.E[sel] / np.interp(r[sel], S["x"], S["E"]) - 1)
        out[foot] = float(err.max())
        ok &= bool(err.max() <= 2e-3)
    return dict(err=out, ok=ok)


def K5():
    mu = 1e-2
    a0 = AF["canonical"]
    N = 1500
    Rm = 1500.0   # A1: wall far out, low-density filler; no vacuum cell opens at the wall
    x = np.linspace(0, np.sqrt(Rm), N + 1) ** 2
    rhos = np.exp(-(x / 60.0) ** 2 / 2) + 1e-4
    Mraw = np.concatenate([[0], np.cumsum(np.diff(x**3) * 0.5 * (rhos[1:] + rhos[:-1]))])
    M = 1e12 * Mraw / Mraw[-1]
    dm = np.diff(M)
    v = -1.0 * np.minimum(x / 200.0, 1.0) * (1 - x / Rm)
    R = Run(x, v, dm, a0, mu, neumann=True)
    R.dq = np.diff(x)
    R.pinf[-1] = True  # A1: fixed outer wall, no boundary work
    def en(R):
        T = 0.5 * np.sum(dm * (0.5 * (R.v[1:] + R.v[:-1])) ** 2) + np.sum(dm * np.diff(R.v) ** 2) / 24
        mm = 0.5 * (R.m[1:] + R.m[:-1])
        rc_ = 0.5 * (R.r[1:] + R.r[:-1])
        UN = -G * np.sum(mm * dm / rc_)
        h = R.hold
        rc, dV3, D, Dout = h.geom(R.r)
        Obj = h.obj(R.u, R.r, dV3, D, Dout, G * dm, 0.0)
        return T + UN - Obj / G, T, UN, -Obj / G
    R.forces(tol=1e-10)
    E0 = en(R)
    tf = 0.0
    maxd = 0.0
    hold_err = 0.0
    while True:
        R.step(40.0)
        if getattr(R, "crossed", False) or R.t >= 40.0:
            break
        f = R.fold(0.2, R.dq)
        if f:
            break
        En = en(R)
        maxd = max(maxd, abs(En[0] - E0[0]) / max(abs(E0[1]) + abs(E0[2]) + abs(E0[3]), 1e-300))
        dV3 = (R.r[1:] ** 3 - R.r[:-1] ** 3) / 3
        hold_err = max(hold_err, abs(np.sum(mu**2 * dV3 * R.u) - G * R.m[-1]) / (G * R.m[-1]))
        tf = R.t
    mass_err = abs(np.sum(dm) - 1e12) / 1e12
    return dict(energy=float(maxd), hold=float(hold_err), mass=float(mass_err), t_stop=float(tf), steps=R.nstep,
                ok=bool(maxd <= 3e-3 and hold_err <= 1e-8 and mass_err <= 1e-13))


def K6():
    bg = Bg(rm0=RX0 + RB0)
    mu = 1e-3
    zi = 20.0
    ai = 1 / (1 + zi)
    kc = 0.09e-3  # comoving /kpc; k_phys = mu at z ~ 10
    eps = 1e-2
    N = 400
    qmax = 6 * np.pi / kc
    qe = np.linspace(0, qmax, N + 1)
    x = kc * np.maximum(qe, 1e-6)
    db = eps * 3 * (np.sin(x) - x * np.cos(x)) / x**3
    r = ai * qe * (1 - db / 3)
    v = bg.H(ai) * ai * qe * (1 - 2 * db / 3)
    dm = 4 * np.pi / 3 * bg.rm0 * np.diff(qe**3)
    R = Run(r, v, dm, AF["canonical"], mu, bg=bg, rbarf=bg.rm0)
    R.t = bg.t(ai)
    R.dq = qe[1] - qe[0]
    te = bg.t(1 / 6.0)
    s = integrate(R, te, fold_on=False)
    i = 8
    d_end = (qe[i] * bg.a(R.t) / R.r[i]) ** 3 - 1
    d_0 = (qe[i] * ai / r[i]) ** 3 - 1
    measured = d_end / d_0
    def rhs(t, y):
        a = bg.a(t)
        kph = kc / a
        s_ = mu**2 / (kph**2 + mu**2)
        return [y[1], -2 * bg.H(a) * y[1] + 4 * np.pi * G * bg.rm0 / a**3 * s_ * y[0]]
    # same start: d_dot = H d (Zel'dovich f = 1)
    so = solve_ivp(rhs, (bg.t(ai), te), [1.0, bg.H(ai)], rtol=1e-9, atol=1e-12)
    ode = so.y[0, -1]
    err = measured / ode - 1
    mx = float(np.max(np.abs(R.E)) / R.a0)
    return dict(measured=float(measured), ode=float(ode), err=float(err), max_x=mx, ok=bool(abs(err) <= 0.05), status=s["status"])


def K8():
    ck = os.path.join(HERE, "ckpt_k8.npz")
    a = run_row("1e12", 56.6, "canonical", N=300, wall=600)
    r = run_row("1e12", 56.6, "canonical", N=300, ckpt=ck, kill_at=max(10, a.get("nstep", 100) // 2), wall=600)
    _STOP["flag"] = False
    b = run_row("1e12", 56.6, "canonical", N=300, ckpt=ck, wall=600)
    if os.path.exists(ck):
        os.remove(ck)
    ta, tb = a.get("t_fold", np.nan), b.get("t_fold", np.nan)
    return dict(ta=ta, tb=tb, first=r.get("status"), rel=float(abs(ta - tb) / ta), ok=bool(r.get("status") == "PREEMPTED" and abs(ta - tb) / ta <= 1e-10))


def run_checks():
    res = {}
    for nm, f in [("K0", K0), ("K1", K1), ("K2", K2), ("K3", K3), ("K4", K4), ("K5", K5), ("K6", K6), ("K8", K8)]:
        if MUTATE and nm in ("K8", "K0"):
            continue
        t = time.time()
        try:
            res[nm] = f()
        except Exception as e:
            res[nm] = dict(ok=False, error=repr(e))
        res[nm]["wall"] = time.time() - t
        print(nm, json.dumps(res[nm]), flush=True)
    res["maxrss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**30
    json.dump(res, open(os.path.join(HERE, f"an1_checks{TAG}.json"), "w"), indent=1)
    print("ALL", all(v["ok"] for k, v in res.items() if k.startswith("K")))


MUS = [0.0156, 0.1, 1.0, 10.0, 56.6, 2.04e4, 1.24e8]
def grid():
    rows = []
    for key in SETUP:
        for mu in MUS:
            for foot in AF:
                rows.append(dict(key=key, mu=mu, foot=foot))
    for key in SETUP:
        for mu in MUS[:3]:
            for foot in AF:
                rows.append(dict(key=key, mu=mu, foot=foot, amp=3.0))
    for key in SETUP:
        for mu in MUS:
            rows.append(dict(key=key, mu=mu, foot="canonical", KB=0.078))
    for key in SETUP:
        for mu in MUS:
            rows.append(dict(key=key, mu=mu, foot="canonical", MGdiv=8.0))
    return rows


def rid(c):
    return f"{c['key']}_{c['mu']}_{c['foot']}_A{c.get('amp', 1.0)}_G{c.get('MGdiv', 1.0)}_K{c.get('KB', 0.0)}_N{c.get('N', 1500)}_e{c.get('eta', 0.005)}"


def run_list(rows, fn):
    done = {}
    if os.path.exists(fn):
        for l in open(fn):
            d = json.loads(l)
            done[d["id"]] = d
    T0 = time.time()
    for c in rows:
        i = rid(c)
        if i in done:
            continue
        ck = os.path.join(HERE, f"ckpt_row{TAG}.npz")
        out = run_row(ckpt=ck, **c)
        if out.get("status") == "PREEMPTED":
            print("preempted", i, flush=True)
            return
        out["id"] = i
        with open(fn, "a") as f:
            f.write(json.dumps(out) + "\n")
        print(i, out.get("label"), "z_f", out.get("z_fold"), "r_f", out.get("r_fold_kpc"), "steps", out.get("nstep"), "wall %.0f" % out.get("wall", 0), flush=True)
        if time.time() - T0 > 6 * 3600:
            print("6h cap reached", flush=True)
            return


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "checks":
        run_checks()
    elif cmd == "rows":
        run_list(grid(), os.path.join(HERE, f"an1_rows{TAG}.jsonl"))
    elif cmd == "conv":
        rows = []
        for key in SETUP:
            for mu, amp in [(1.0, 3.0), (56.6, 1.0), (1.24e8, 1.0)]:
                for N, eta in [(750, 0.005), (1500, 0.005), (3000, 0.005), (1500, 0.0025)]:
                    rows.append(dict(key=key, mu=mu, foot="canonical", amp=amp, N=N, eta=eta))
        run_list(rows, os.path.join(HERE, f"an1_conv{TAG}.jsonl"))
    elif cmd == "held":
        fn = os.path.join(HERE, f"an1_held{TAG}.jsonl")
        with open(fn, "w") as f:
            for key in SETUP:
                for mu in (0.1, 1.0):
                    for foot in AF:
                        o = held_row(key, mu, foot)
                        f.write(json.dumps(o) + "\n")
                        f.flush()
                        print(o, flush=True)
