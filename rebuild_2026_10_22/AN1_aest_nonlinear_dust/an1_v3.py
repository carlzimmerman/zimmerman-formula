#!/usr/bin/env python3
"""AN1 v3 rerun after the centre-cell bug: see AMENDMENT_A3.md, FROZEN_CRITERIA.md.
Imports an1.py and replaces only what A3 names. Writes an1_v3_* outputs; never touches first-published files.
Run: python3 an1_v3.py checks|rows|conv|held|verify [--mutate] [--mutate-linear] [--mutate-step]
kappa = 1/2 FITTED. Gravitating field, no particle. No completion past a fold. Reinstates nothing."""
import os, sys, json, time, resource
ARGV = list(sys.argv)
MUT_LINEAR = "--mutate-linear" in ARGV   # A3 MUTATE: restore linear-in-r enclosed mass
MUT_STEP = "--mutate-step" in ARGV       # A3 MUTATE: no step rejection at the wall
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import an1
from an1 import G, TU, CK, AF, Bg, SETUP, RX0, RB0, gbar, edge_amp, glaw

TAG = "_MUTATE" if an1.MUTATE else ("_MUTATE_LINEAR" if MUT_LINEAR else ("_MUTATE_STEP" if MUT_STEP else ""))
CF_STRICT = 1e-4      # A3: the strict line is primary
EPS_WORK = 1e-3       # A3: step rejection, work mismatch per shell over its energy scale
OPT = {"stop": "A1"}  # A3: baryon turning below r_f stops where it is; "snap" = code as first run


# ---------- enclosed mass: r^3, shell's mass inside its mid-q surface
def _setup_fr(s):
    cum = np.cumsum(s.mb)
    lo = cum - s.mb
    ql, qh = np.cbrt(lo), np.cbrt(cum)
    qc = 0.5 * (ql + qh)
    s.fr = (qc**3 - ql**3) / (qh**3 - ql**3)


_old_Mb = an1.Run.Mb


def Mb(s, x):
    if s.Mb_fn is not None:
        return s.Mb_fn(x)
    if s.rb is None:
        return s.Mseed
    if MUT_LINEAR:
        return _old_Mb(s, x)
    if not hasattr(s, "fr"):
        _setup_fr(s)
    o = np.argsort(s.rb)
    c = np.cumsum(s.mb[o]) - (1 - s.fr[o]) * s.mb[o]
    return np.interp(np.asarray(x) ** 3, np.concatenate([[0.0], s.rb[o] ** 3]), np.concatenate([[0.0], c]))


def _Mfield(s, x):
    if MUT_LINEAR:
        return np.interp(x, s.r, s.m)
    return np.interp(np.asarray(x) ** 3, s.r**3, s.m)


def forces(s, tol=1e-8):
    r = s.r
    dV3 = (r[1:] ** 3 - r[:-1] ** 3) / 3
    S = G * (s.dm - s.rbarf / s.aval() ** 3 * 4 * np.pi * dV3) if s.bg is not None else G * s.dm
    s.u, s.res = s.hold.solve(s.u, r, S, s.uo, tol=tol)
    rc, _, D, _ = s.hold.geom(r)
    E = np.zeros_like(r)
    E[1:-1] = -(s.u[1:] - s.u[:-1]) / D
    E[-1] = 0.0 if s.hold.neu else -(s.uo - s.u[-1]) / (r[-1] - rc[-1])
    s.E = E
    f = 1 - s.KB / 2
    g = np.zeros_like(r)
    g[1:] = f * G * (s.Mb(r[1:]) + s.m[1:]) / r[1:] ** 2
    s.g = g
    F = -g + an1.SIGN * E + s.Lam * r
    F[0] = 0.0
    F[s.pinf] = 0.0
    s.F = F
    if s.rb is not None:
        s.gb = f * G * (s.Mb(s.rb) + _Mfield(s, s.rb)) / s.rb**2 - s.Lam * s.rb
    return F


def step(s, tmax):
    """KDK, as an1.Run.step, with A3's rejection: at low mu E is singular at r_w = sqrt(G m/a0); a drift
    past r_w meets a huge E and the kick then injects energy. A step whose trapezoid work error on any shell
    exceeds EPS_WORK of that shell's energy scale is undone and retried at half dt."""
    if not hasattr(s, "F"):
        s.forces()
    fac = getattr(s, "dtfac", 1.0)
    saved = (s.r.copy(), s.v.copy(), s.u.copy(), s.F.copy(), s.E.copy(), s.g.copy(), s.t)
    if s.rb is not None:
        savedb = (s.rb.copy(), s.vb.copy(), s.pinb.copy(), s.gb.copy())
    while True:
        dt = s.dt(tmax) * fac
        s.v += 0.5 * dt * s.F
        s.r += dt * s.v
        s.r[0] = 0.0
        if s.rb is not None:
            fly = ~s.pinb
            s.vb[fly] -= 0.5 * dt * s.gb[fly]
            s.rb[fly] += dt * s.vb[fly]
            fin = np.isfinite(s.rf)
            hit = fly & (s.vb <= 0) & ((fin & (s.rb <= s.rf)) | ~fin)
            hf = hit & fin
            if OPT["stop"] == "snap":
                s.rb[hf] = s.rf[hf]
            else:
                # A1's text: at r_f when falling through it, at turnaround if that is below r_f.
                through = hf & (s.rb + dt * np.abs(s.vb) >= s.rf)
                s.rb[through] = s.rf[through]
                turned_below = hf & ~through
                if turned_below.any():
                    s.n_turnbelow = getattr(s, "n_turnbelow", 0) + int(turned_below.sum())
                    s.m_turnbelow = getattr(s, "m_turnbelow", 0.0) + float(s.mb[turned_below].sum())
            s.vb[hit] = 0.0
            s.pinb |= hit
        s.t += dt
        if not np.all(np.diff(s.r) > 0):
            s.crossed = True
            return dt
        Fold = saved[3]
        s.forces()
        if MUT_STEP or fac < 1e-6:
            break
        dr = s.r - saved[0]
        scale = 0.5 * saved[1] ** 2 + np.abs(s.g) * s.r + 1e-30
        W = 0.5 * np.abs(s.F - Fold) * np.abs(dr) / scale
        if W[1:].max() <= EPS_WORK:
            break
        # undo and halve
        s.r, s.v, s.u, s.F, s.E, s.g, s.t = saved[0].copy(), saved[1].copy(), saved[2].copy(), saved[3].copy(), saved[4].copy(), saved[5].copy(), saved[6]
        if s.rb is not None:
            s.rb, s.vb, s.pinb, s.gb = savedb[0].copy(), savedb[1].copy(), savedb[2].copy(), savedb[3].copy()
        fac *= 0.5
        s.nrej = getattr(s, "nrej", 0) + 1
    s.dtfac = min(1.0, fac * 1.5)
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


an1.Run.Mb = Mb
an1.Run.forces = forces
an1.Run.step = step


# ---------- stop radii: M(<r_f) = the shell's mass inside its mid-q surface, not its outer edge
def stop_radii(key, mb):
    if MUT_LINEAR:
        return an1.stop_radii(key, mb)
    cum = np.cumsum(mb)
    lo = cum - mb
    qc = 0.5 * (np.cbrt(lo) + np.cbrt(cum))
    mid = qc**3
    rf = np.full_like(mb, np.inf)
    if key == "1e12":
        Md, Rd = 6.72e10, 3.565
        x = np.logspace(-6, 2, 8000)
        M = Md * (1 - (1 + x) * np.exp(-x))
        s = cum <= Md * 0.9999
        rf[s] = Rd * np.interp(mid[s], M, x)
    else:
        R5, rcg, Mg = 1350.0, 0.15 * 1350.0, 1.19e14
        x = np.logspace(-4, np.log10(R5), 8000)
        P = lambda r: r - rcg * np.arctan(r / rcg)
        M = Mg * P(x) / P(R5)
        s = cum <= Mg
        rf[s] = np.interp(mid[s], M, x)
    return rf


def build(key, mu_Mpc, foot, N=1500, amp=1.0, MGdiv=1.0, KB=0.0, eta=0.005, zi=20.0, dom=2.0):
    """an1.build; dom moves the outer boundary (verification only), N counts cells to 2 q_t so dq is unchanged."""
    st = SETUP[key]
    bg = Bg()
    M = st["M"]
    de, qt = edge_amp(bg, M, zi)
    RG = (M / MGdiv / ((2 * np.pi) ** 1.5 * bg.rm0)) ** (1 / 3)
    d0 = de / gbar(np.array([qt / RG]))[0] * amp
    Nc = int(round(N * dom / 2.0))
    qe = np.linspace(0, dom * qt, Nc + 1)
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
    R = an1.Run(r, v, dm, AF[foot], mu_Mpc * 1e-3, KB=KB, bg=bg, rbarf=RX0, rb=rb0, vb=vb0, mb=mb, rf=rf, eta=eta)
    R.t = bg.t(ai)
    R.dq = qe[1] - qe[0]
    R.t0 = bg.t(1.0)
    R.meta = dict(d0=float(d0), de=float(de), qt=float(qt), RG=float(RG))
    return R


# ---------- fold reader: any closing cell under the line, not only the smallest cell
def fold(s, Cf, dq):
    dr = np.diff(s.r)
    dv = np.diff(s.v)
    C = dr / (s.aval() * dq)
    m = (C < Cf) & (dv < 0)
    if not m.any():
        return None
    idx = np.where(m)[0]
    i = int(idx[np.argmin(C[idx])])
    return i, s.t + dr[i] / abs(dv[i])


def save(s, path):
    d = {k: getattr(s, k) for k in ("r", "v", "u", "t", "nstep", "turned")}
    d["dtfac"] = getattr(s, "dtfac", 1.0)
    d["nrej"] = getattr(s, "nrej", 0)
    d["n_tb"] = getattr(s, "n_turnbelow", 0)
    d["m_tb"] = getattr(s, "m_turnbelow", 0.0)
    if s.rb is not None:
        d.update(rb=s.rb, vb=s.vb, pinb=s.pinb)
    np.savez(path, **d)


def load(s, path):
    d = np.load(path)
    s.r, s.v, s.u, s.t, s.nstep, s.turned = d["r"], d["v"], d["u"], float(d["t"]), int(d["nstep"]), bool(d["turned"])
    s.dtfac, s.nrej, s.n_turnbelow, s.m_turnbelow = float(d["dtfac"]), int(d["nrej"]), int(d["n_tb"]), float(d["m_tb"])
    if s.rb is not None:
        s.rb, s.vb, s.pinb = d["rb"], d["vb"], d["pinb"]
    if hasattr(s, "F"):
        del s.F


an1.Run.fold = fold
an1.Run.save = save
an1.Run.load = load


# ---------- reads: r^3 for every enclosed mass
def diag(R, key):
    st = SETUP[key]
    o = np.argsort(R.r)
    out = {}
    for nm, X in zip(st["names"], st["Rs"]):
        Md = float(np.interp(X**3, R.r[o] ** 3, R.m[o]))
        Mb_ = float(R.Mb(np.array([X]))[0])
        gN = G * Mb_ / X**2
        gl = glaw(gN, R.a0)
        Mph = (gl - gN) * X**2 / G
        out[nm] = dict(R=X, Md=Md, Mb=Mb_, Mph=Mph, ex_over_Mb=(Md - Mph) / Mb_ if Mb_ > 0 else None,
                       Md_over_Mb=Md / Mb_ if Mb_ > 0 else None, Md_over_Mph=Md / Mph if Mph > 0 else None,
                       n_field_nodes=int(np.sum(R.r[1:] <= X)))
    Rt = st["Rt"]
    idx = np.where(R.r[1:] <= Rt)[0] + 1
    d = dict(masses=out)
    if len(idx):
        gt = R.g[idx]
        Vc = np.sqrt(np.maximum(gt * R.r[idx], 1e-30))
        d["max_F_over_g"] = float(np.max(np.abs(R.F[idx]) / gt))
        d["max_v_over_Vc"] = float(np.max(np.abs(R.v[idx]) / Vc))
        d["E_over_g_Rt"] = float(R.E[idx[-1]] / gt[-1])
        q = gt / (CK * Vc) * 1e3
        d["Q0_need_perMpc"] = float(np.max(q))
        sel = R.r[idx] >= 1.0
        d["Q0_need_r_ge_1kpc_perMpc"] = float(np.max(q[sel])) if sel.any() else None
        d["F_over_g_outside_1kpc"] = float(np.max((np.abs(R.F[idx]) / gt)[sel])) if sel.any() else None
        d["v_over_Vc_outside_1kpc"] = float(np.max((np.abs(R.v[idx]) / Vc)[sel])) if sel.any() else None
    else:
        d["max_F_over_g"] = d["max_v_over_Vc"] = None
    d["baryon_stopped_on_profile"] = float(np.sum(R.mb[R.pinb & np.isfinite(R.rf)]) / np.sum(R.mb[np.isfinite(R.rf)]))
    d["inner_ratio_r1_over_half_r2"] = float(2 * R.r[1] / R.r[2])
    return d


def integrate(R, tmax, Cf=CF_STRICT, nmax=400000, wall=1200.0, ckpt=None, fold_on=True, kill_at=None):
    """Budget 4e5 steps or 20 min, as frozen; counted in CPU seconds (A3: the machine is shared and loaded)."""
    c0 = time.process_time()
    if ckpt and os.path.exists(ckpt):
        R.load(ckpt)
    R.forces()
    status = None
    while R.t < tmax - 1e-12:
        if kill_at is not None and R.nstep == kill_at:
            an1._STOP["flag"] = True
        if an1._STOP["flag"]:
            if ckpt:
                R.save(ckpt)
            return dict(status="PREEMPTED")
        R.step(tmax)
        if getattr(R, "crossed", False):
            status = dict(status="FOLD", i=int(np.argmin(np.diff(R.r))), t_fold=R.t, crossed_in_step=True)
            break
        if fold_on:
            if not hasattr(R, "frozen_line") and Cf < 1e-2:
                f2 = R.fold(1e-2, R.dq)
                if f2:
                    R.frozen_line = dict(t=float(f2[1]), cell=f2[0])
            f = R.fold(Cf, R.dq)
            if f:
                status = dict(status="FOLD", i=f[0], t_fold=f[1])
                break
        if R.nstep >= nmax or time.process_time() - c0 > wall:
            status = dict(status="UNRESOLVED", reason="budget")
            break
    if status is None:
        status = dict(status="END")
    status.update(t=R.t, nstep=R.nstep, turned=R.turned, cpu=time.process_time() - c0, newton_warn=R.hold.warn, nit=R.hold.nit,
                  nrej=getattr(R, "nrej", 0), n_turnbelow=getattr(R, "n_turnbelow", 0), m_turnbelow=getattr(R, "m_turnbelow", 0.0))
    if ckpt and os.path.exists(ckpt):
        os.remove(ckpt)
    return status


def run_row(key, mu, foot, N=1500, amp=1.0, MGdiv=1.0, KB=0.0, eta=0.005, ckpt=None, kill_at=None, wall=1200.0, dom=2.0, Cf=CF_STRICT, eps=None):
    global EPS_WORK
    eps0 = EPS_WORK
    if eps is not None:
        EPS_WORK = eps
    R = build(key, mu, foot, N, amp, MGdiv, KB, eta, dom=dom)
    s = integrate(R, R.t0, Cf=Cf, ckpt=ckpt, kill_at=kill_at, wall=wall)
    EPS_WORK = eps0
    if s["status"] == "PREEMPTED":
        return s
    out = dict(key=key, mu=mu, foot=foot, N=N, amp=amp, MGdiv=MGdiv, KB=KB, eta=eta, dom=dom, Cf=Cf, **R.meta, **s)
    if eps is not None:
        out["eps"] = eps
    hbar = 4 * np.pi * G * RX0 * (1 + 20.0) ** 3 / (mu * 1e-3) ** 2 / CK**2
    out["hbar_zi_over_c2"] = float(hbar)
    out["quadratic_K_lapses"] = bool(hbar > 0.1)
    out["polytrope_R_kpc"] = float(np.pi / (mu * 1e-3))
    if hasattr(R, "frozen_line"):
        out["frozen_line_z"] = float(1 / R.bg.a(min(R.frozen_line["t"], R.t0)) - 1)
        out["frozen_line_cell"] = R.frozen_line["cell"]
    if not np.all(np.isfinite(R.r)):
        out["status"] = "UNRESOLVED"
        out["label"] = "UNRESOLVED"
        return out
    if np.all(np.diff(R.r) > 0):
        R.forces(tol=1e-6)
    out.update(diag(R, key))
    a_end = R.aval()
    out["z_end"] = float(1 / a_end - 1)
    C = np.diff(R.r) / (a_end * R.dq)
    out["Cmin_end"] = float(C.min())
    out["cell_Cmin_end"] = int(np.argmin(C))
    if s["status"] == "FOLD":
        i = s["i"]
        tf = min(s["t_fold"], R.t0 * 2)
        out["t_fold_Gyr"] = float(tf * TU)
        out["z_fold"] = float(1 / R.bg.a(min(tf, R.t0)) - 1)
        out["r_fold_kpc"] = float(0.5 * (R.r[i] + R.r[i + 1]))
        out["m_fold"] = float(R.m[i + 1])
        out["cell_fold"] = i
        out["grid_limited"] = bool(i < 3)
        out["edge_artefact"] = bool(i >= 0.95 * len(R.dm))
        out["label"] = "UNRESOLVED" if out["edge_artefact"] else "FOLD FIRST"
    elif s["status"] == "END":
        if not R.turned:
            out["label"] = "NO COLLAPSE"
        else:
            ok = out.get("max_F_over_g") is not None and out["max_F_over_g"] <= 0.1 and out["max_v_over_Vc"] <= 0.1
            out["label"] = "SETTLED" if ok else "OSCILLATING"
    else:
        out["label"] = "UNRESOLVED"
    return out


an1.integrate = integrate
an1.run_row = run_row
an1.stop_radii = stop_radii if not MUT_LINEAR else an1.stop_radii
an1.build = build


# ---------- new checks
def dust_sphere_exact(d, M, zi=20.0):
    """Independent of Run: energy integral by quadrature, cross-checked with an ODE. Returns t_collapse."""
    from scipy.integrate import quad, solve_ivp
    from scipy.optimize import brentq
    bg = Bg()
    ai = 1 / (1 + zi)
    q = (3 * M / (4 * np.pi * bg.rm0)) ** (1 / 3)
    L = bg.OL * bg.H0**2
    R0, V0 = ai * q * (1 - d / 3), bg.H(ai) * ai * q * (1 - 2 * d / 3)
    En = 0.5 * V0**2 - G * M / R0 - 0.5 * L * R0**2
    V2 = lambda x: 2 * (En + G * M / x + 0.5 * L * x**2)
    xs = np.logspace(np.log10(R0), np.log10(1000 * R0), 4000)
    j = np.where(V2(xs) < 0)[0][0]
    Rta = brentq(V2, xs[j - 1], xs[j], xtol=1e-12 * R0)
    # substitutions take out the end-point singularities
    f1 = lambda th: 2 * Rta * np.sin(th) * np.cos(th) * 0 + 0
    up = quad(lambda s: 2 * s / np.sqrt(V2(Rta - s * s)), 0, np.sqrt(Rta - R0), limit=400, epsabs=1e-10, epsrel=1e-11)[0]
    dn = quad(lambda s: 2 * s * s * s * 0 + 2 * s / np.sqrt(V2(s * s)) , 1e-9, np.sqrt(Rta) * 0.9, limit=400, epsabs=1e-10, epsrel=1e-11)[0]
    dn2 = quad(lambda s: 2 * s / np.sqrt(V2(Rta - s * s)), 0, np.sqrt(Rta - (np.sqrt(Rta) * 0.9) ** 2), limit=400, epsabs=1e-10, epsrel=1e-11)[0]
    tq = bg.t(ai) + up + dn + dn2
    ev = lambda t, y: y[0] - 1e-6 * R0
    ev.terminal = True
    so = solve_ivp(lambda t, y: [y[1], -G * M / y[0] ** 2 + L * y[0]], (bg.t(ai), 3 * bg.t(1.0)), [R0, V0], events=ev, rtol=1e-11, atol=1e-13 * R0, method="DOP853")
    return tq, float(so.t_events[0][0]), float(1 / bg.a(tq) - 1)


def tophat_run(key, N, stop_on, mu=1.24e8, d=0.2030, zi=20.0):
    bg = Bg()
    M = SETUP[key]["M"]
    qt = (3 * M / (4 * np.pi * bg.rm0)) ** (1 / 3)
    qe = np.linspace(0, 3 * qt, N + 1)
    ai = 1 / (1 + zi)
    Hi = bg.H(ai)
    prof = lambda q: np.where(q < qt, d, d * (qt / np.maximum(q, 1e-9)) ** 3)
    db = prof(qe)
    r = ai * qe * (1 - db / 3)
    v = Hi * ai * qe * (1 - 2 * db / 3)
    dm = 4 * np.pi / 3 * RX0 * np.diff(qe**3)
    mb = 4 * np.pi / 3 * RB0 * np.diff(qe**3)
    qb = 0.5 * (qe[1:] + qe[:-1])
    dbb = prof(qb)
    rb0 = ai * qb * (1 - dbb / 3)
    vb0 = Hi * ai * qb * (1 - 2 * dbb / 3)
    rf = stop_radii(key, mb) if stop_on else np.zeros_like(mb)
    R = an1.Run(r, v, dm, AF["canonical"], mu * 1e-3, bg=bg, rbarf=RX0, rb=rb0, vb=vb0, mb=mb, rf=rf)
    R.t = bg.t(ai)
    R.dq = qe[1] - qe[0]
    R.t0 = bg.t(1.0)
    return R


def _track(R, Cstop=1e-3):
    """Largest |r_1 / (r_k / k) - 1|, k = 2, 3, 5, until the central cell reaches Cstop of its comoving size."""
    mx = 0.0
    R.forces()
    while R.t < 3 * R.t0:
        R.step(3 * R.t0)
        if getattr(R, "crossed", False):
            return mx, R.t, True
        for k in (2, 3, 5):
            mx = max(mx, abs(R.r[1] * k / R.r[k] - 1))
        if R.r[1] / (R.aval() * R.dq) < Cstop:
            return mx, R.t, False
    return mx, R.t, False


def K10():
    TOL = 2e-3
    out = dict(tol_rel_t=TOL, rows=[])
    ok = True
    for key in SETUP:
        tq, tode, zx = dust_sphere_exact(0.2030, SETUP[key]["M"])
        out[f"exact_{key}"] = dict(t_quad=tq, t_ode=tode, z=zx, rel=abs(tq - tode) / tq)
        ok &= abs(tq - tode) / tq < 1e-6
        for N in (300, 1200):
            for stop_on in (True, False):
                R = tophat_run(key, N, stop_on)
                s = integrate(R, 3 * R.t0)
                t = s.get("t_fold", np.inf)
                rel = (t - tq) / tq
                z = float(1 / R.bg.a(min(t, 3 * R.t0)) - 1)
                out["rows"].append(dict(key=key, N=N, stop=stop_on, status=s["status"], z=z, rel=float(rel), cell=s.get("i")))
                ok &= bool(abs(rel) <= TOL)
    out["ok"] = bool(ok)
    return out


def K11():
    TOL = 0.02
    out = dict(tol=TOL, rows=[])
    ok = True
    for key in SETUP:
        for N in (300, 1200):
            R = tophat_run(key, N, True)
            m, t, cr = _track(R)
            out["rows"].append(dict(kind="tophat", key=key, N=N, max_dev=float(m), crossed=cr, t=float(t)))
            ok &= bool(m <= TOL and not cr)
            R = build(key, 1.24e8, "canonical", N=N)
            m, t, cr = _track(R)
            out["rows"].append(dict(kind="P1", key=key, N=N, max_dev=float(m), crossed=cr, t=float(t)))
            ok &= bool(m <= TOL and not cr)
    out["ok"] = bool(ok)
    return out


def _k12(N, vin=100.0, nmax=200000):
    """Wall bounce, A3. Field only, mu 0.1 /Mpc, no background. With m_1 fixed and the mu term negligible, r^2 V(E) = G m_1 gives a closed
    potential for the first shell: e = v^2/2 - a0 rw^2/r - (a0 rw/2) ln((r-rw)/(r+rw)), rw = sqrt(G m_1/a0).
    The shell comes in at vin, reflects off rw (the small mu term lets r go a little under rw, so e is read after, at r > 5 rw);
    |e_out - e_in| / (vin^2/2) must be under K5's line 3e-3."""
    mu, a0 = 1e-4, AF["canonical"]
    Rm = 1500.0
    x = np.linspace(0, np.sqrt(Rm), N + 1) ** 2
    rhos = np.exp(-(x / 60.0) ** 2 / 2) + 1e-4
    Mraw = np.concatenate([[0], np.cumsum(np.diff(x**3) * 0.5 * (rhos[1:] + rhos[:-1]))])
    M = 1e12 * Mraw / Mraw[-1]
    dm = np.diff(M)
    v = -vin * np.ones_like(x) * (1 - x / Rm)
    v[0] = 0.0
    R = an1.Run(x, v, dm, a0, mu, neumann=True)
    R.dq = np.diff(x)
    R.pinf[-1] = True
    rw = np.sqrt(G * dm[0] / a0)
    def e1():
        r1, v1 = R.r[1], R.v[1]
        if r1 <= rw:
            return np.nan
        return 0.5 * v1**2 - a0 * rw**2 / r1 - 0.5 * a0 * rw * np.log((r1 - rw) / (r1 + rw))
    R.forces(tol=1e-10)
    e0 = e1()
    rmin, emx = R.r[1], np.inf
    read = None
    while R.nstep < nmax:
        R.step(1e3)
        if getattr(R, "crossed", False):
            break
        rmin = min(rmin, R.r[1])
        e = e1()
        if R.v[1] > 0 and R.r[1] > 5 * rw and np.isfinite(e):
            read = dict(v_out=float(R.v[1]), r=float(R.r[1]))
            emx = abs(e - e0) / (0.5 * vin**2)
            break
    return dict(rw=float(rw), rmin=float(rmin), rmin_over_rw=float(rmin / rw), v_in=float(vin), read=read, max_rel_e=float(emx), steps=R.nstep, nrej=getattr(R, "nrej", 0),
                newton_warn=R.hold.warn, ok=bool(read is not None and emx <= 3e-3))


def K12():
    a, b = _k12(300), _k12(1200)
    return dict(N300=a, N1200=b, ok=bool(a["ok"] and b["ok"]))


def K8():
    ck = os.path.join(HERE, f"an1_v3_ckpt_k8{TAG}.npz")
    a = run_row("1e12", 56.6, "canonical", N=300, wall=600)
    r = run_row("1e12", 56.6, "canonical", N=300, ckpt=ck, kill_at=max(10, a.get("nstep", 100) // 2), wall=600)
    an1._STOP["flag"] = False
    b = run_row("1e12", 56.6, "canonical", N=300, ckpt=ck, wall=600)
    if os.path.exists(ck):
        os.remove(ck)
    ta, tb = a.get("t_fold", np.nan), b.get("t_fold", np.nan)
    return dict(ta=ta, tb=tb, first=r.get("status"), rel=float(abs(ta - tb) / ta), ok=bool(r.get("status") == "PREEMPTED" and abs(ta - tb) / ta <= 1e-10))


def run_checks():
    res = {}
    lst = [("K10", K10), ("K11", K11), ("K12", K12), ("K0", an1.K0), ("K1", an1.K1), ("K2", an1.K2), ("K3", an1.K3), ("K4", an1.K4), ("K5", an1.K5), ("K6", an1.K6), ("K8", K8)]
    for nm, f in lst:
        if TAG and nm in ("K0", "K8"):
            continue
        c = time.process_time()
        try:
            res[nm] = f()
        except Exception as e:
            res[nm] = dict(ok=False, error=repr(e))
        res[nm]["cpu"] = time.process_time() - c
        print(nm, json.dumps(res[nm]), flush=True)
        json.dump(res, open(os.path.join(HERE, f"an1_v3_checks{TAG}.json"), "w"), indent=1)
    res["maxrss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**30
    json.dump(res, open(os.path.join(HERE, f"an1_v3_checks{TAG}.json"), "w"), indent=1)
    print("ALL", all(v["ok"] for k, v in res.items() if k.startswith("K")))


def rid(c):
    return f"{c['key']}_{c['mu']}_{c['foot']}_A{c.get('amp', 1.0)}_G{c.get('MGdiv', 1.0)}_K{c.get('KB', 0.0)}_N{c.get('N', 1500)}_e{c.get('eta', 0.005)}_D{c.get('dom', 2.0)}_W{c.get('eps', EPS_WORK)}"


def run_list(rows, fn, name):
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
        ck = os.path.join(HERE, f"an1_v3_ckpt_{name}{TAG}.npz")
        out = run_row(ckpt=ck, **c)
        if out.get("status") == "PREEMPTED":
            print("preempted", i, flush=True)
            return False
        out["id"] = i
        out["maxrss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**30
        with open(fn, "a") as f:
            f.write(json.dumps(out) + "\n")
        print(i, out.get("label"), "z_f", out.get("z_fold"), "r_f", out.get("r_fold_kpc"), "steps", out.get("nstep"), "rej", out.get("nrej"), "warn", out.get("newton_warn"), "cpu %.0f" % out.get("cpu", 0), flush=True)
        if time.time() - T0 > 6 * 3600:
            print("6h cap reached", flush=True)
            return False
    return True


def conv_rows():
    rows = []
    for key in SETUP:
        for mu, amp in [(1.0, 3.0), (56.6, 1.0), (1.24e8, 1.0)]:
            for N, eta in [(750, 0.005), (1500, 0.005), (3000, 0.005), (1500, 0.0025)]:
                rows.append(dict(key=key, mu=mu, foot="canonical", amp=amp, N=N, eta=eta))
    return rows


def k7_grade(fn):
    rows = [json.loads(l) for l in open(fn)]
    t = lambda d: d.get("t_fold", d["t"])
    out, ok = [], True
    for key in SETUP:
        for mu, amp in [(1.0, 3.0), (56.6, 1.0), (1.24e8, 1.0)]:
            g = lambda N, e: [d for d in rows if d["key"] == key and d["mu"] == mu and d["N"] == N and d["eta"] == e][0]
            a, b, c = g(1500, 0.005), g(3000, 0.005), g(1500, 0.0025)
            dN, de = abs(t(a) - t(b)) / t(b), abs(t(a) - t(c)) / t(c)
            rf = None
            lim = a.get("grid_limited", True) or b.get("grid_limited", True)
            if not lim:
                rf = a["r_fold_kpc"] / b["r_fold_kpc"]
            good = dN <= 0.03 and de <= 0.03 and (rf is None or 1 / 1.5 <= rf <= 1.5)
            ok &= bool(good)
            out.append(dict(key=key, mu=mu, amp=amp, z750=g(750, 0.005).get("z_fold"), z1500=a.get("z_fold"), z3000=b.get("z_fold"), dt_N=dN, dt_eta=de, rf_ratio=rf, r1500=a.get("r_fold_kpc"), r3000=b.get("r_fold_kpc"), ok=bool(good)))
    return dict(rows=out, ok=bool(ok))


# ---------- held start: an1's static branch with R_out as a parameter; outer 5 % of cells kept apart from the fold reader
def static_branch(key, mu_Mpc, foot, N=1200, Rfac=1.0):
    from scipy.integrate import solve_ivp
    from scipy.optimize import brentq
    a0, mu = AF[foot], mu_Mpc * 1e-3
    if key == "1e12":
        Rout = 300.0 * Rfac
        Mdisc, Rd = 6.72e10, 3.565
        MB = lambda r: Mdisc * (1 - (1 + r / Rd) * np.exp(-r / Rd))
    else:
        Rout = 3000.0 * Rfac
        R5, rcg, Mg = 1350.0, 202.5, 1.19e14
        P = lambda r: r - rcg * np.arctan(r / rcg)
        MB = lambda r: Mg * P(r) / P(R5)

    def rhs(r, y):
        h, Mh = y
        gN = G * (MB(r) + Mh) / r**2
        gt = glaw(max(gN, 0.0), a0) if gN >= 0 else -glaw(-gN, a0)
        return [-gt, mu**2 * h * r**2 / G]
    r0 = 1e-3 * (300.0 if key == "1e12" else 3000.0) / 300
    shoot = lambda h0: solve_ivp(rhs, (r0, Rout), [h0, 0.0], rtol=1e-9, atol=[1e-6, 1.0], method="LSODA", dense_output=True)
    grid_h = np.logspace(2, 9, 57)
    fv = [shoot(x_).y[0] for x_ in grid_h]
    h0 = None
    for i_ in range(len(grid_h) - 1):
        if fv[i_][-1] * fv[i_ + 1][-1] < 0:
            c_ = brentq(lambda z: shoot(z).y[0, -1], grid_h[i_], grid_h[i_ + 1], xtol=1e-6)
            if np.all(shoot(c_).y[0][:-1] > 0):
                h0 = c_
                break
    if h0 is None:
        return None
    s = shoot(h0)
    x = np.linspace(np.sqrt(0.02 * (300.0 if key == "1e12" else 3000.0) / 300), np.sqrt(Rout), N + 1) ** 2
    y = s.sol(x)
    h, Mh = y
    gN = G * (MB(x) + Mh) / x**2
    E = np.where(gN >= 0, glaw(np.abs(gN), a0), -glaw(np.abs(gN), a0))
    Md = E * x**2 / G - MB(x)
    return dict(r=np.concatenate([[0.0], x]), x=x, h=h, E=E, Md=Md, MB=MB, Rout=Rout, h0=h0, a0=a0, mu=mu)


def held_row(key, mu_Mpc, foot, kick=0.01, N=1200, Rfac=1.0, wall=1200.0, tGyr=14.0):
    base = dict(key=key, mu=mu_Mpc, foot=foot, kick=kick, N=N, Rfac=Rfac)
    S = static_branch(key, mu_Mpc, foot, N=N, Rfac=Rfac)
    if S is None:
        return dict(base, label="NOT RUN", reason="no positive static branch to R_out")
    dm = np.diff(np.concatenate([[0.0], S["Md"]]))
    r = S["r"]
    neg = np.where(dm <= 0)[0]
    if len(neg):
        if neg[0] < 50:
            return dict(base, label="NOT RUN", reason=f"negative rho_d from r={float(r[neg[0]+1])}")
        r, dm = r[: neg[0] + 1], dm[: neg[0]]
    Vc = np.sqrt(np.maximum(np.interp(r, S["x"], S["E"]) * r, 0.0))
    R = an1.Run(r, kick * Vc * np.sin(np.pi * r / r[-1]), dm, S["a0"], S["mu"], Mb_fn=S["MB"], uo=float(np.interp(r[-1], S["x"], S["h"])))
    R.u = np.interp(0.5 * (r[1:] + r[:-1]), S["x"], S["h"])
    R.pinf[-1] = True
    q0 = np.diff(r)
    R.dq = q0
    R.forces()
    F0 = float(np.max(np.abs(R.F[5:-5]) / R.g[5:-5]))
    n95 = int(0.95 * len(dm))
    tmax, cmin = tGyr / TU, 1.0
    res, tev, cell = "HOLDS", None, None
    c0 = time.process_time()
    while R.t < tmax - 1e-12:
        R.step(tmax)
        if an1._STOP["flag"]:
            res = "PREEMPTED"
            break
        if getattr(R, "crossed", False):
            d = np.diff(R.r)
            cell = int(np.argmin(d))
            res, tev = ("INNER FOLD" if cell < n95 else "OUTER WALL CELL"), R.t * TU
            break
        C, dv = np.diff(R.r) / q0, np.diff(R.v)
        cmin = min(cmin, float(C[:n95].min()))
        mi = (C[:n95] < CF_STRICT) & (dv[:n95] < 0)
        if mi.any():
            cell = int(np.where(mi)[0][0])
            res, tev = "INNER FOLD", R.t * TU
            break
        mo = (C[n95:] < CF_STRICT) & (dv[n95:] < 0)
        if mo.any():
            cell = n95 + int(np.where(mo)[0][0])
            res, tev = "OUTER WALL CELL", R.t * TU
            break
        if R.nstep >= 400000 or time.process_time() - c0 > wall:
            res = "BUDGET"
            break
    return dict(base, label=res, t_Gyr=R.t * TU, t_event_Gyr=tev, cell=cell, r_event=None if cell is None else float(R.r[cell]), n_cells=len(dm), Cmin_inner=cmin, F0_over_g=F0,
                Rout=float(r[-1]), steps=R.nstep, nrej=getattr(R, "nrej", 0), newton_warn=R.hold.warn, cpu=time.process_time() - c0)


def run_held():
    fn = os.path.join(HERE, f"an1_v3_held{TAG}.jsonl")
    seen = set()
    if os.path.exists(fn):
        seen = {(d["key"], d["mu"], d["foot"], d["kick"], d["N"], d["Rfac"]) for d in map(json.loads, open(fn))}
    plan = []
    for key in SETUP:
        for mu in (0.1, 1.0):
            for foot in AF:
                plan.append((key, mu, foot, 0.01, 1200, 1.0))
            plan += [(key, mu, "canonical", 0.01, 2400, 1.0), (key, mu, "canonical", 0.1, 1200, 1.0), (key, mu, "canonical", 0.01, 1200, 2.0), (key, mu, "canonical", 0.1, 1200, 2.0)]
    for p in plan:
        if p in seen:
            continue
        o = held_row(p[0], p[1], p[2], kick=p[3], N=p[4], Rfac=p[5])
        if o.get("label") == "PREEMPTED":
            return
        with open(fn, "a") as f:
            f.write(json.dumps(o) + "\n")
        print(o, flush=True)


def verify_rows(fn):
    """A3: every non-fold row, and fold rows at z_fold < 0.05, at N 3000, eta 0.0025, outer boundary at 3 q_t, step-rejection tolerance / 4."""
    rows = []
    for l in open(fn):
        d = json.loads(l)
        if d["label"] != "FOLD FIRST" or d.get("z_fold", 9) < 0.05:
            b = dict(key=d["key"], mu=d["mu"], foot=d["foot"], amp=d["amp"], MGdiv=d["MGdiv"], KB=d["KB"])
            rows += [dict(b, N=3000), dict(b, eta=0.0025), dict(b, dom=3.0), dict(b, eps=EPS_WORK / 4)]
    return rows


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "checks":
        run_checks()
    elif cmd == "rows":
        run_list(an1.grid(), os.path.join(HERE, f"an1_v3_rows{TAG}.jsonl"), "rows")
    elif cmd == "conv":
        fn = os.path.join(HERE, f"an1_v3_conv{TAG}.jsonl")
        if run_list(conv_rows(), fn, "conv"):
            g = k7_grade(fn)
            json.dump(g, open(os.path.join(HERE, f"an1_v3_k7{TAG}.json"), "w"), indent=1)
            print(json.dumps(g, indent=0))
    elif cmd == "held":
        run_held()
    elif cmd == "verify":
        run_list(verify_rows(os.path.join(HERE, f"an1_v3_rows{TAG}.jsonl")), os.path.join(HERE, f"an1_v3_verify{TAG}.jsonl"), "verify")
