#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L374 -- THE CONDENSATE'S DUST THROUGH SHELL CROSSING (one dimension): when two cold streams of the framework's own field
meet, do they pass through each other like collisionless matter?

WHY.  The record's no-particle reading of the dark sector (the ghost-condensate thread; Blanchet-Skordis K(Q) = mu^2 (Q-1)^2)
  makes the cold dark mass a state of the framework's own scalar: its condensate sits slightly above its minimum and the
  excess dilutes as cold dust.  The CMB constrains only a fluid, so linear cosmology cannot tell this from a particle.  The
  nonlinear universe can: halos need streams to cross (multistreaming), and so do Bullet and Harvey (the dark mass passes
  through while the gas collides).  A single-valued flow forms caustics where streams cross; the record lists this as the
  open liability of the mode reading ("caustic-quenched dust: no theory").  The candidate fix is the condensate's own k^4
  term, which gives its ripples a Schroedinger-like k^2 dispersion -- the property that lets fuzzy dark matter (a linear
  complex field) pass through itself by interference.  This lane asks whether the condensate's k^4 term does the same.

THE FIELD.  phi = t + pi, X = -g^{mu nu} d_mu phi d_nu phi, P(X) quadratic about its minimum X_0, plus the ghost condensate's
  higher-derivative term -(alpha / 2 M^2)(box phi)^2 (Arkani-Hamed, Cheng, Luty, Mukohyama 2004).  Weak field, non-relativistic,
  one dimension, with the dust density rho = 2 P''(X_0) (X - X_0) and velocity v = -d_x pi:
      d_t rho + d_x (rho v) = beta d_x^3 v              (the shift charge; beta = alpha / M^2 is the k^4 term)
      d_t v + v d_x v      = -d_x Phi - eps d_x rho      (eps = 1 / 4 P'': the condensate's warmth, p = eps rho^2 / 2)
      d_x^2 Phi = 4 pi G (rho - rho_bar)
  derived here from L = P''(X_0) delta^2 / 2 - (beta / 2)(d_x^2 pi)^2 with delta = 2 d_t pi - (d_x pi)^2 - 2 Phi; the
  Hamiltonian E = int [rho v^2 / 2 + eps rho^2 / 2 + beta (d_x v)^2 / 2 + (rho - rho_bar) Phi / 2] is conserved.  Linear
  waves: omega^2 = eps rho k^2 + eps beta k^4 -- a k^2 dispersion with D = sqrt(eps beta) in the role of hbar / 2m (fuzzy
  dark matter: omega = D k^2).  rho < 0 is the condensate below its minimum, where c_s^2 < 0 (the ghost instability).

THE TEST.  A cold converging flow v = v0 sin(2 pi x / L) on a uniform density in a periodic box: (i) free streaming (G = 0;
  the collisionless answer is exact, three streams after t_sc = L / (2 pi v0)); (ii) self-gravitating (4 pi G rho_bar =
  (2 pi v0 / L)^2: a one-dimensional halo forms and phase-mixes; the collisionless answer is an exact-force sheet N-body).
  Compared, each coarse-grained with a Gaussian of width L/50:
    the collisionless N-body answer (the target);
    Schroedinger-Poisson with the same D (fuzzy dark matter; the positive control, a field known to pass through itself);
    the pressureless fluid (eps = beta = 0; the negative control, the caustic);
    the condensate at warmth W = eps rho_bar / v0^2 = 1e-1, 1e-2, 1e-3, 1e-4 and de Broglie length lambda = 4 pi D / v0 =
    L/100, L/200 (sixteen cells).  (The CMB's bound on the dust's warmth today is far colder than any scanned W; the scan
    follows the trend toward cold.  W = 0.1 was added after the code test showed W = 1e-2 breaking down, to see whether a warm
    condensate survives; it can only make H easier.)
  MEASURE: the misplaced mass M = (1/2) int |rho_s - rho_s,Nbody| dx / int rho dx at every checkpoint after shell crossing;
  the condensate's minimum density (positivity); energy conservation.

PRE-DECLARED (before any run).  H (the sketch's hope): the condensate's own k^4 term quenches the caustic and the field tracks
  the collisionless answer as Schroedinger-Poisson does -- some (W, lambda) cell keeps M <= max(0.05, 2 x Schroedinger-
  Poisson's M at the same lambda and time) at every post-crossing checkpoint in BOTH tests, stays positive (min rho >= -0.01
  rho_bar), conserves energy to 1% and does not break down.  The equations' structure (a dispersive gamma = 2 fluid, not a
  linear wave equation) suggests it may not: then the condensate's dust collides like a fluid.

CHECKS
  C1 CONTROL (single stream): before shell crossing every solver agrees with the N-body answer (M <= 0.01).
  C2 POSITIVE CONTROL: Schroedinger-Poisson tracks the N-body answer after shell crossing (M <= 0.05, both tests, both lambda).
  C3 NEGATIVE CONTROL: the pressureless fluid follows the exact single-stream solution (central density 20 rho_bar at 0.95
     t_sc, within 10%) and then diverges (max rho > 50 rho_bar, or breakdown, by 1.05 t_sc).
  C4 NUMERICAL TRUST: every condensate run conserves energy to 1% at its checkpoints and while its density stays above
     -rho_bar (before any runaway).
  C5 RESOLUTION AND TIME STEP: the (W = 1e-3, L/100) free-streaming cell at twice the resolution and at half the time step
     gives the same verdict, with breakdown and first-negative times (or misplaced mass) agreeing within 20%.
  R1 = H.
  W  (reported) the full table.
MUTATE=1 replaces the condensate by a LINEAR complex field with the same D and the same eps self-interaction (Gross-
  Pitaevskii-Poisson: the dispersion in Madelung form) -- the inverted control: if the condensate fails and this passes, the
  failure lies in the form of the condensate's dispersion, not in the test.  FAST=1 is a code test (coarse grid, one cell);
  it writes nothing here.

Run from the repository root:  python3 real_research/condensate_dust_2026/L374_condensate_dust_shell_crossing.py
"""
import os, sys, json, math, time, tempfile
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
FAST = os.environ.get("FAST", "0") == "1"
SLUG = "L374_condensate_dust_shell_crossing" + ("_MUTATE" if MUTATE else "") + ("_FAST" if FAST else "")
OUTDIR = tempfile.gettempdir() if FAST else HERE
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L374", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_TRACK = True                                                  # H, set before any run

L, V0, RHOB = 1.0, 1.0, 1.0
TSC = L / (2 * math.pi * V0)
NX0 = 1024 if FAST else 8192
SIG_S = L / 50
GRAV = {"free": 0.0, "gravity": (2 * math.pi * V0 / L) ** 2}        # 4 pi G rho_bar
TCHK = {"free": [0.5 * TSC, 1.5 * TSC, 2.0 * TSC, 3.0 * TSC], "gravity": [0.05, 0.3, 0.6, 1.0, 1.5]}
LAMS = (L / 40,) if FAST else (L / 100, L / 200)
WS = (1e-2,) if FAST else (1e-1, 1e-2, 1e-3, 1e-4)
RES_W = WS[0] if FAST else 1e-3                                      # the resolution / time-step cell (C5)
NP_FREE, NP_GRAV = (100000, 20000) if FAST else (2000000, 200000)
M_TOL, POS_TOL, E_TOL = 0.05, -0.01, 0.01


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


class Grid:
    def __init__(self, nx):
        self.nx, self.dx = nx, L / nx
        self.x = np.arange(nx) * self.dx
        self.k = 2 * np.pi * np.fft.rfftfreq(nx, self.dx)
        self.kf = 2 * np.pi * np.fft.fftfreq(nx, self.dx)
        self.deal = self.k <= (2.0 / 3.0) * self.k[-1]
        self.gsm = np.exp(-0.5 * (self.k * SIG_S) ** 2)

    def smooth(self, rho):
        return np.fft.irfft(np.fft.rfft(rho) * self.gsm, self.nx)

    def phi_k(self, rho_k, grav):
        out = np.zeros_like(rho_k)
        if grav > 0:
            out[1:] = -grav * rho_k[1:] / self.k[1:] ** 2
        return out

    def misplaced(self, rs, rs_ref):
        """rs, rs_ref already smoothed: half the L1 distance over the total mass."""
        return float(0.5 * np.sum(np.abs(rs - rs_ref)) / np.sum(rs_ref))

    def cic(self, xp, m):
        s = (xp % L) / self.dx; i0 = np.floor(s).astype(np.int64); f = s - i0
        rho = (np.bincount(i0 % self.nx, weights=1 - f, minlength=self.nx)
               + np.bincount((i0 + 1) % self.nx, weights=f, minlength=self.nx))
        return rho * m / self.dx


def v_init(x): return V0 * np.sin(2 * np.pi * x / L)                  # converges on x = L/2
def S_init(x): return -(V0 * L / (2 * np.pi)) * np.cos(2 * np.pi * x / L)


# ================================================================================================ the collisionless answer
def nbody(test, nx):
    g = Grid(nx); out = {}
    if test == "free":
        q = (np.arange(NP_FREE) + 0.5) * L / NP_FREE; m = RHOB * L / NP_FREE
        for t in TCHK[test]:
            out[t] = g.smooth(g.cic(q + v_init(q) * t, m))
        return dict(rs=out, tsc=TSC)
    q = (np.arange(NP_GRAV) + 0.5) * L / NP_GRAV; m = RHOB * L / NP_GRAV
    xp, vp = q.copy(), v_init(q); grav = GRAV[test]

    def acc(xp):                                                       # exact sheet force, Jeans swindle, zero net force
        order = np.argsort(xp)
        rank = np.empty(NP_GRAV); rank[order] = np.arange(NP_GRAV)
        a = -grav * (m * (rank + 0.5) - RHOB * xp)
        return a - a.mean()
    dt, t, tsc = 2.5e-4, 0.0, None
    a = acc(xp)
    for tc in TCHK[test]:
        n = int(round((tc - t) / dt))
        for _ in range(n):
            vp += 0.5 * dt * a; xp += dt * vp
            if tsc is None and np.any(np.diff(xp) < 0):                # the first stream crossing (Lagrangian order breaks;
                tsc = t + dt                                           # it precedes any sheet reaching the box edge)
            xp %= L                                                    # periodic: the sheet force holds on [0, L)
            a = acc(xp); vp += 0.5 * dt * a
            t += dt
        out[tc] = g.smooth(g.cic(xp, m))
    return dict(rs=out, tsc=tsc, xmin=float(xp.min()), xmax=float(xp.max()))


# ================================================================================================ a linear complex field
def schrodinger(test, lam, eps_self, nx):
    """Schroedinger-Poisson (eps_self = 0) or Gross-Pitaevskii-Poisson: i psi_t = -D psi_xx + (Phi + eps |psi|^2) psi / 2D."""
    g = Grid(nx); D = lam * V0 / (4 * np.pi); grav = GRAV[test]
    psi = np.sqrt(RHOB) * np.exp(1j * S_init(g.x) / (2 * D))
    dtm = 1e-5 * (8192 / nx)

    def V(psi):
        rho = np.abs(psi) ** 2
        out = eps_self * rho if eps_self > 0 else np.zeros(nx)
        if grav > 0:
            out = out + np.fft.irfft(g.phi_k(np.fft.rfft(rho), grav), nx)
        return out / (2 * D)
    t, out = 0.0, {}
    for tc in TCHK[test]:
        n = max(1, int(math.ceil((tc - t) / dtm))); dt = (tc - t) / n
        kin = np.exp(-1j * D * g.kf ** 2 * dt)
        for _ in range(n):                                             # Strang splitting
            psi *= np.exp(-0.5j * dt * V(psi))
            psi = np.fft.ifft(kin * np.fft.fft(psi))
            psi *= np.exp(-0.5j * dt * V(psi))
        t = tc
        out[tc] = g.smooth(np.abs(psi) ** 2)
    return dict(rs=out, min_rho=0.0, e_drift=0.0, t_break=None)


# ================================================================================================ the condensate
def condensate(test, lam, W, nx, pressureless=False, dtfac=1.0):
    """the dispersive gamma = 2 fluid above: integrating-factor RK4 (Lawson), the k^4 exchange exact, 2/3 dealiasing."""
    g = Grid(nx); grav = GRAV[test]
    if pressureless:
        eps = beta = 0.0
    else:
        D = lam * V0 / (4 * np.pi); eps = W * V0 ** 2 / RHOB; beta = D ** 2 / eps
    om = math.sqrt(eps * beta) * g.k ** 2
    k4 = g.k ** 4
    rk = np.fft.rfft(np.full(nx, RHOB)); sk = np.fft.rfft(S_init(g.x))
    dtm = 2e-5 * (8192 / nx) * dtfac
    kd = (2.0 / 3.0) * g.k[-1]

    def Eop(tau):
        c = np.cos(om * tau); s = np.sin(om * tau)
        safe = om > 1e-300
        B = np.where(safe, beta * k4 * s / np.where(safe, om, 1.0), beta * k4 * tau)
        C = np.where(safe, -eps * s / np.where(safe, om, 1.0), -eps * tau)
        return c, B, C

    def apply(E, r, s_):
        c, B, C = E
        return c * r + B * s_, C * r + c * s_

    def Nl(r, s_):
        r_d, s_d = r * g.deal, s_ * g.deal
        rho = np.fft.irfft(r_d, nx); v = np.fft.irfft(1j * g.k * s_d, nx)
        nr = -1j * g.k * np.fft.rfft(rho * v)
        ns = -0.5 * np.fft.rfft(v * v) - g.phi_k(r_d, grav)
        return nr * g.deal, ns * g.deal

    def energy(r, s_):
        rho = np.fft.irfft(r, nx); v = np.fft.irfft(1j * g.k * s_, nx); dv = np.fft.irfft(-(g.k ** 2) * s_, nx)
        ph = np.fft.irfft(g.phi_k(r, grav), nx)
        return float(np.sum(0.5 * rho * v ** 2 + 0.5 * eps * rho ** 2 + 0.5 * beta * dv ** 2 + 0.5 * (rho - RHOB) * ph) * g.dx)
    E0 = energy(rk, sk); EK0 = 0.25 * RHOB * V0 ** 2 * L
    t, out, min_rho, e_drift, t_break, rho_c95 = 0.0, {}, RHOB, 0.0, None, None
    t_neg, e_pre, nstep = None, 0.0, 0
    rho_max_hist = []
    targets = sorted(set(TCHK[test] + ([0.95 * TSC, 1.05 * TSC] if pressureless else [])))
    for tc in targets:
        while t < tc - 1e-14 and t_break is None:
            rho = np.fft.irfft(rk, nx); v = np.fft.irfft(1j * g.k * sk, nx)
            vmax = float(np.max(np.abs(v))) + 1e-12
            dt = min(dtm, 0.25 * dtfac * g.dx / vmax, tc - t)
            if eps > 0:
                dt = min(dt, 0.5 * dtfac / (kd * math.sqrt(eps * max(float(np.max(np.abs(rho))), RHOB))))
            if grav > 0:
                dt = min(dt, 0.05 * dtfac / math.sqrt(grav * max(float(np.max(rho)), RHOB)))
            Eh, Eh2 = Eop(dt), Eop(0.5 * dt)
            k1 = Nl(rk, sk)
            a_ = apply(Eh2, rk + 0.5 * dt * k1[0], sk + 0.5 * dt * k1[1]); k2 = Nl(*a_)
            u2 = apply(Eh2, rk, sk); b_ = (u2[0] + 0.5 * dt * k2[0], u2[1] + 0.5 * dt * k2[1]); k3 = Nl(*b_)
            uh = apply(Eh, rk, sk); e3 = apply(Eh2, *k3)
            c_ = (uh[0] + dt * e3[0], uh[1] + dt * e3[1]); k4_ = Nl(*c_)
            e1 = apply(Eh, *k1); e23 = apply(Eh2, k2[0] + k3[0], k2[1] + k3[1])
            rk = uh[0] + dt / 6 * (e1[0] + 2 * e23[0] + k4_[0])
            sk = uh[1] + dt / 6 * (e1[1] + 2 * e23[1] + k4_[1])
            t += dt
            rho = np.fft.irfft(rk, nx)
            if not np.all(np.isfinite(rho)) or np.max(np.abs(rho)) > 1e4 * RHOB:
                t_break = t
                break
            min_rho = min(min_rho, float(rho.min())); nstep += 1
            if not pressureless and (nstep % 50 == 0 or (t_neg is None and rho.min() < POS_TOL)) and rho.min() >= -1.0:
                e_pre = max(e_pre, abs(energy(rk, sk) - E0) / EK0)     # energy before the runaway (rho >= -rho_bar)
            if t_neg is None and rho.min() < POS_TOL:
                t_neg = t                                              # first entry below the condensate's minimum
            if pressureless:
                rho_max_hist.append((t, float(rho.max())))
        if t_break is not None:
            break
        if pressureless and abs(tc - 0.95 * TSC) < 1e-12:
            rho_c95 = float(np.fft.irfft(rk, nx)[nx // 2])
        if tc in TCHK[test]:
            out[tc] = g.smooth(np.fft.irfft(rk, nx))
            if not pressureless:
                e_drift = max(e_drift, abs(energy(rk, sk) - E0) / EK0)
    rmax105 = max([r for tt, r in rho_max_hist if tt <= 1.05 * TSC + 1e-12], default=RHOB)
    return dict(rs=out, min_rho=min_rho, e_drift=max(e_drift, e_pre), t_break=t_break, t_neg=t_neg, rho_c95=rho_c95,
                rho_max_105=rmax105)


def job(spec):
    kind, test, lam, W, nx = spec
    if kind == "nbody":
        return spec, nbody(test, nx)
    if kind == "sp":
        return spec, schrodinger(test, lam, 0.0, nx)
    if kind == "gp":
        return spec, schrodinger(test, lam, W * V0 ** 2 / RHOB, nx)
    if kind == "dust0":
        return spec, condensate(test, lam, W, nx, pressureless=True)
    if kind == "cond_dt2":
        return spec, condensate(test, lam, W, nx, dtfac=0.5)
    return spec, condensate(test, lam, W, nx)


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: the condensate is replaced by a linear complex field (Gross-Pitaevskii-Poisson, same D and eps) ***")
    if FAST: P("\n  *** FAST=1: code test on a coarse grid, one cell; nothing is written here ***")
    FIELD = "gp" if MUTATE else "cond"
    specs = [("nbody", te, None, None, NX0) for te in ("free", "gravity")]
    specs += [("sp", te, lam, None, NX0) for te in ("free", "gravity") for lam in LAMS]
    specs += [("dust0", "free", None, None, NX0)]
    specs += [(FIELD, te, lam, W, NX0) for te in ("free", "gravity") for lam in LAMS for W in WS]
    RES_SPEC = (FIELD, "free", LAMS[0], RES_W, 2 * NX0)
    DT2_SPEC = ("gp" if MUTATE else "cond_dt2", "free", LAMS[0], RES_W, NX0)
    specs += [RES_SPEC, ("nbody", "free", None, None, 2 * NX0), ("sp", "free", LAMS[0], None, 2 * NX0)]
    if not MUTATE:
        specs.append(DT2_SPEC)
    NPOOL = int(os.environ.get("L374_POOL", "2"))
    P(f"\n  {len(specs)} runs, pool {NPOOL}")
    with Pool(NPOOL) as pool:
        R = dict(pool.map(job, specs, chunksize=1))
    P(f"  runs done   [{time.time() - T0:.0f}s]")
    G0, G2 = Grid(NX0), Grid(2 * NX0)
    NB = {te: R[("nbody", te, None, None, NX0)] for te in ("free", "gravity")}
    tsc = {te: NB[te]["tsc"] for te in NB}
    post = {te: [t for t in TCHK[te] if tsc[te] is not None and t > tsc[te]] for te in NB}
    pre = {te: [t for t in TCHK[te] if tsc[te] is not None and t < tsc[te]] for te in NB}
    P(f"  shell crossing: free {tsc['free']:.4f} (exact {TSC:.4f}); self-gravitating {tsc['gravity']:.4f} (first stream crossing in "
      f"the N-body)")
    Mis = lambda spec, te, t, g=G0, nb=None: g.misplaced(R[spec]["rs"][t], (nb or NB[te])["rs"][t])

    # ------------------------------------------------------------------------------------------ table
    banner("MISPLACED MASS vs the collisionless answer (coarse-grained on L/50), per checkpoint")
    TAB = {}
    for te in ("free", "gravity"):
        for lam in LAMS:
            sp = ("sp", te, lam, None, NX0)
            TAB[f"SP|{te}|{lam:.4f}"] = {f"{t:.4f}": Mis(sp, te, t) for t in TCHK[te]}
            P(f"    {te:8s} Schroedinger-Poisson lambda = L/{round(L / lam)}: " + ", ".join(f"t={t:.3f}: {Mis(sp, te, t):.4f}" for t in TCHK[te]))
            for W in WS:
                sc = (FIELD, te, lam, W, NX0); r = R[sc]
                row = {f"{t:.4f}": Mis(sc, te, t) for t in TCHK[te] if t in r["rs"]}
                TAB[f"{FIELD}|{te}|{lam:.4f}|{W:g}"] = dict(M=row, min_rho=r["min_rho"], e_drift=r["e_drift"], t_break=r["t_break"],
                                                             t_neg=r.get("t_neg"))
                P(f"    {te:8s} {'GP' if MUTATE else 'condensate'} W = {W:g}, lambda = L/{round(L / lam)}: "
                  + ", ".join(f"t={float(t):.3f}: {m:.4f}" for t, m in row.items())
                  + f" | min rho {r['min_rho']:+.3g}" + (f" (below the minimum from t = {r['t_neg']:.4f}, {r['t_neg'] / tsc[te]:.2f} t_sc)" if r.get('t_neg') else "")
                  + f" | energy drift {r['e_drift']:.1e}"
                  + (f" | BROKE DOWN at t = {r['t_break']:.4f} ({r['t_break'] / tsc[te]:.2f} t_sc)" if r["t_break"] else ""))

    # ------------------------------------------------------------------------------------------ checks
    banner("CHECKS")
    c1 = []
    for te in ("free", "gravity"):
        for t in pre[te]:
            for spec in [s_ for s_ in R if s_[1] == te and s_[4] == NX0 and s_[0] in ("sp", FIELD, "dust0") and t in R[s_]["rs"]]:
                c1.append(Mis(spec, te, t))
    check("C1 CONTROL (single stream): before shell crossing every solver agrees with the N-body answer (M <= 0.01)",
          f"max M {max(c1):.2e} over {len(c1)} comparisons; pre-crossing checkpoints {pre}", len(c1) > 0 and max(c1) <= 0.01)
    c2 = {f"{te}|L/{round(L / lam)}": max(Mis(("sp", te, lam, None, NX0), te, t) for t in post[te]) for te in ("free", "gravity") for lam in LAMS}
    check("C2 POSITIVE CONTROL: Schroedinger-Poisson (a linear complex field with the same D) tracks the collisionless answer after "
          "shell crossing (M <= 0.05, both tests, both lambda)", f"max post-crossing M: {c2}", all(v <= M_TOL for v in c2.values()))
    d0 = R[("dust0", "free", None, None, NX0)]
    c3 = dict(rho_center_095=d0["rho_c95"], exact=20.0, rho_max_by_105=d0["rho_max_105"], t_break=d0["t_break"])
    check("C3 NEGATIVE CONTROL: the pressureless fluid follows the exact single-stream solution (central density 20 rho_bar at "
          "0.95 t_sc within 10%) and then diverges (max rho > 50 rho_bar, or breakdown, by 1.05 t_sc)", c3,
          d0["rho_c95"] is not None and abs(d0["rho_c95"] / 20.0 - 1) < 0.10
          and (d0["rho_max_105"] > 50 or (d0["t_break"] is not None and d0["t_break"] <= 1.05 * TSC)))
    if not MUTATE:
        c4 = {k_: v["e_drift"] for k_, v in TAB.items() if isinstance(v, dict) and "e_drift" in v}
        check("C4 NUMERICAL TRUST: every condensate run conserves energy to 1% at its checkpoints and while its density stays above -rho_bar",
              f"max drift {max(c4.values()):.1e}", max(c4.values()) <= E_TOL)
    # C5 resolution
    rr = R[RES_SPEC]; r1 = R[(FIELD, "free", RES_SPEC[2], RES_SPEC[3], NX0)]; rd = R[DT2_SPEC] if not MUTATE else r1
    NB2 = R[("nbody", "free", None, None, 2 * NX0)]
    m1 = {t: Mis((FIELD, "free", RES_SPEC[2], RES_SPEC[3], NX0), "free", t) for t in post["free"] if t in r1["rs"]}
    m2 = {t: G2.misplaced(rr["rs"][t], NB2["rs"][t]) for t in post["free"] if t in rr["rs"]}
    sp2 = {t: G2.misplaced(R[("sp", "free", RES_SPEC[2], None, 2 * NX0)]["rs"][t], NB2["rs"][t]) for t in post["free"]}

    def verdict(mm, rmin, tb, spm):
        return tb is None and rmin >= POS_TOL and len(mm) == len(post["free"]) and all(mm[t] <= max(M_TOL, 2 * spm[t]) for t in mm)
    sp1 = {t: Mis(("sp", "free", RES_SPEC[2], None, NX0), "free", t) for t in post["free"]}
    v1, v2 = verdict(m1, r1["min_rho"], r1["t_break"], sp1), verdict(m2, rr["min_rho"], rr["t_break"], sp2)
    md = {t: Mis(DT2_SPEC, "free", t) for t in post["free"] if t in rd["rs"]}
    vd = verdict(md, rd["min_rho"], rd["t_break"], sp1)

    def same(a, b):
        if a["t_break"] and b["t_break"]:
            ok_ = abs(b["t_break"] / a["t_break"] - 1) <= 0.20
            if a.get("t_neg") and b.get("t_neg"):
                ok_ = ok_ and abs(b["t_neg"] / a["t_neg"] - 1) <= 0.20
            return ok_
        return a["t_break"] is None and b["t_break"] is None
    agree = same(r1, rr) and same(r1, rd)
    if agree and r1["t_break"] is None:
        agree = (all(abs(m2[t] / m1[t] - 1) <= 0.20 for t in m1 if t in m2) and all(abs(md[t] / m1[t] - 1) <= 0.20 for t in m1 if t in md))
    check("C5 RESOLUTION AND TIME STEP: the (W = %g, L/%d) free-streaming cell at twice the resolution and at half the time step "
          "gives the same verdict, and its breakdown / first-negative times (or misplaced mass) agree within 20%%"
          % (RES_SPEC[3], round(L / RES_SPEC[2])),
          f"verdict {v1} / 2x grid {v2} / dt/2 {vd}; M {[round(v, 4) for v in m1.values()]} / {[round(v, 4) for v in m2.values()]} / "
          f"{[round(v, 4) for v in md.values()]}; first below the minimum {r1.get('t_neg')} / {rr.get('t_neg')} / {rd.get('t_neg')}; "
          f"breakdown {r1['t_break']} / {rr['t_break']} / {rd['t_break']}", v1 == v2 == vd and agree)

    # ------------------------------------------------------------------------------------------ R1
    banner("R1  THE HYPOTHESIS (set before any run)")
    PASS = {}
    for lam in LAMS:
        for W in WS:
            ok_te = {}
            for te in ("free", "gravity"):
                sc = (FIELD, te, lam, W, NX0); r = R[sc]
                ok_te[te] = (r["t_break"] is None and r["min_rho"] >= POS_TOL and (MUTATE or r["e_drift"] <= E_TOL)
                             and all(t in r["rs"] and Mis(sc, te, t) <= max(M_TOL, 2 * Mis(("sp", te, lam, None, NX0), te, t)) for t in post[te]))
            PASS[f"W={W:g}|L/{round(L / lam)}"] = ok_te
            P(f"    W = {W:g}, lambda = L/{round(L / lam)}: free {'tracks' if ok_te['free'] else 'does NOT track'}, "
              f"self-gravitating {'tracks' if ok_te['gravity'] else 'does NOT track'}")
    WIN = [k_ for k_, v in PASS.items() if v["free"] and v["gravity"]]
    check("R1 = H: the %s passes through itself like collisionless matter -- some (W, lambda) cell tracks the N-body answer in both "
          "tests, stays positive, conserves energy, does not break down" % ("linear complex field" if MUTATE else "condensate"),
          f"tracking cells: {WIN or 'none'}", bool(WIN) == EXPECT_TRACK)
    check("W (reported) the table above", "see above", True, load_bearing=False)
    OUT["numbers"].update(table=TAB, pass_cells=PASS, window=WIN, tsc=tsc, post=post, C2=c2, C3=c3,
                          C5=dict(M1={f"{t:.4f}": v for t, v in m1.items()}, M2={f"{t:.4f}": v for t, v in m2.items()},
                                  Mdt={f"{t:.4f}": v for t, v in md.items()}, min1=r1["min_rho"], min2=rr["min_rho"],
                                  tb1=r1["t_break"], tb2=rr["t_break"], tbdt=rd["t_break"], tn1=r1.get("t_neg"),
                                  tn2=rr.get("t_neg"), tndt=rd.get("t_neg")),
                          params=dict(L=L, v0=V0, rho_bar=RHOB, nx=NX0, sigma_s=SIG_S, lambdas=LAMS, W=WS, grav=GRAV,
                                      np_free=NP_FREE, np_grav=NP_GRAV))

    # ------------------------------------------------------------------------------------------ figure (never load-bearing)
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.4))
        t2 = TCHK["free"][2]; Ww = WS[0]
        ax[0].plot(G0.x, NB["free"]["rs"][t2], "k-", lw=2.2, label="collisionless (N-body)")
        ax[0].plot(G0.x, R[("sp", "free", LAMS[0], None, NX0)]["rs"][t2], "C0--", lw=1.6, label="Schroedinger-Poisson (same D)")
        rw = R[(FIELD, "free", LAMS[0], Ww, NX0)]
        if t2 in rw["rs"]:
            ax[0].plot(G0.x, rw["rs"][t2], "C3-", lw=1.4, label=f"{'GP' if MUTATE else 'condensate'} W = {Ww:g} (the warmest cell)")
        ax[0].set_title(f"free streaming, t = {t2 / TSC:.1f} t_sc, lambda = L/{round(L / LAMS[0])} (coarse-grained on L/50)", fontsize=9)
        ax[0].set_xlabel("x / L"); ax[0].set_ylabel("density / mean"); ax[0].legend(fontsize=8)
        for te, mk in (("free", "o"), ("gravity", "s")):
            for lam, ls in zip(LAMS, ("-", ":")):
                Wv = [W for W in WS]; rr_ = [R[(FIELD, te, lam, W, NX0)] for W in WS]
                tn = [r_.get("t_neg") / tsc[te] if r_.get("t_neg") else np.nan for r_ in rr_]
                tb = [r_["t_break"] / tsc[te] if r_["t_break"] else np.nan for r_ in rr_]
                ax[1].plot(Wv, tn, mk + ls, color="C1", ms=5, label=f"{te}, L/{round(L / lam)}: first below the minimum")
                ax[1].plot(Wv, tb, mk + ls, color="C3", ms=5, label=f"{te}, L/{round(L / lam)}: breakdown")
        ax[1].axhline(1.0, color="k", lw=0.8); ax[1].set_xscale("log")
        ax[1].set_xlabel("warmth W = eps rho_bar / v0^2"); ax[1].set_ylabel("time / shell-crossing time")
        ax[1].set_title("the condensate at every scanned cell" + (" (MUTATE: linear field)" if MUTATE else ""), fontsize=9)
        ax[1].legend(fontsize=6.5, ncol=2)
        fig.tight_layout(); fig.savefig(os.path.join(OUTDIR, SLUG + ".png"), dpi=110)
        P(f"  figure: {SLUG}.png")
    except Exception as e_:
        P(f"  figure skipped: {e_}")

    banner("VERDICT")
    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    json.dump(OUT, open(os.path.join(OUTDIR, SLUG + "_results.json"), "w"), indent=1,
              default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote "
      f"{os.path.join(OUTDIR, SLUG + '_results.json') if FAST else SLUG + '_results.json'}   [{time.time() - T0:.0f}s]")
    P(f"rc={0 if n_fail == 0 else 1}")
    sys.exit(0 if n_fail == 0 else 1)
