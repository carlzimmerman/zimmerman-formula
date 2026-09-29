#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D5common -- shared machinery for CFG130 (Door 5: does a non-negative f(E, L) exist for the CFG44 target?).

Self-contained (nothing imported from the repository).  Units a0 = 1, G = 1, baryon mass M = 1  =>  r_M = sqrt(G M/a0) = 1.
Target (CFG44 (T)): rho_c g_tot = a0 M_b(<r)/(4 pi r^3),  u = G M_tot(<r) = u_N + w,  w' = a0 r u_N/u,  g_tot = u/r^2 (the P2 law for a point mass).
The potential the fluid moves in is the target's own total potential; the fluid's density is the target's own, so self-consistency is automatic.
"""
import os, sys, math, json, time
import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.interpolate import PchipInterpolator
from scipy.special import gammainc

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
FOUR_PI = 4.0 * math.pi


# ------------------------------------------------------------------------------------------------------ targets / potentials
class Pot:
    """spherical target: attributes are callables of r (numpy arrays).
       Phi(r) with Phi' = g = u/r^2 ; rho(r) target cold-fluid density ; beta(r) = -(3/2) rho_b/rhobar_b ; sr2(r) = V_c^2/2 = u/(2 r)."""

    def __init__(self, name, u, Phi, rho, beta, uN, h=None):
        self.name, self.u, self.Phi, self.rho, self.beta, self.uN, self.h = name, u, Phi, rho, beta, uN, h

    def g(self, r):
        r = np.asarray(r, float)
        return self.u(r) / r ** 2

    def sr2(self, r):
        r = np.asarray(r, float)
        return self.u(r) / (2 * r)


def point_mass():
    """closed forms of CFG44 B1(a): u = sqrt(1 + r^2), rho = 1/(4 pi r sqrt(1+r^2)), Phi = asinh r - sqrt(1+r^2)/r, beta = 0 for r > 0 (M_b(<r) = M constant)."""
    return Pot("point mass",
               u=lambda r: np.sqrt(1.0 + np.asarray(r, float) ** 2),
               Phi=lambda r: np.arcsinh(np.asarray(r, float)) - np.sqrt(1.0 + np.asarray(r, float) ** 2) / np.asarray(r, float),
               rho=lambda r: 1.0 / (FOUR_PI * np.asarray(r, float) * np.sqrt(1.0 + np.asarray(r, float) ** 2)),
               beta=lambda r: np.zeros_like(np.asarray(r, float)),
               uN=lambda r: np.ones_like(np.asarray(r, float)))


def exp_sphere(h, rmin=1e-8, rmax=1e8, n=30001):
    """3-D exponential sphere rho_b = M/(8 pi h^3) exp(-r/h), M = 1: u_N = P(3, r/h).  w' = r u_N/u integrated in ln r from the P2 slow manifold."""
    uN = lambda r: gammainc(3.0, np.asarray(r, float) / h)
    lr = np.linspace(math.log(rmin), math.log(rmax), n)
    rg = np.exp(lr)

    def rhs(s, y):
        r = math.exp(s)
        un = float(uN(r))
        u = max(un + y[0], 1e-300)
        return [r * r * un / u]

    u0 = float(uN(rmin))
    w0 = u0 * (math.sqrt(1.0 + rmin * rmin / u0) - 1.0)
    sol = solve_ivp(rhs, (lr[0], lr[-1]), [w0], t_eval=lr, rtol=1e-11, atol=1e-30, method="Radau")
    w = sol.y[0]
    ug = uN(rg) + w
    gg = ug / rg ** 2
    Phi_g = cumulative_trapezoid(gg * rg, lr, initial=0.0)                       # Phi = Int g dr = Int g r dln r
    u_i = PchipInterpolator(lr, np.log(ug), extrapolate=True)
    Phi_i = PchipInterpolator(lr, Phi_g, extrapolate=True)

    def u(r):
        r = np.asarray(r, float)
        return np.exp(u_i(np.log(r)))

    def Phi(r):
        return Phi_i(np.log(np.asarray(r, float)))

    def rho(r):
        r = np.asarray(r, float)
        return uN(r) / (FOUR_PI * r * u(r))

    def beta(r):
        r = np.asarray(r, float)
        rhob = np.exp(-r / h) / (8 * math.pi * h ** 3)
        rhobar = 3 * uN(r) / (FOUR_PI * r ** 3)
        return -1.5 * rhob / rhobar

    return Pot(f"exp sphere h={h}", u, Phi, rho, beta, uN, h=h)


# ------------------------------------------------------------------------------------------------------ orbit machinery
def _roots(Phi, E, L2, rc, iters=80):
    """pericentre and apocentre of orbits (E, L^2) with a circular radius rc (h(rc) >= 0), vectorised bisection in ln r.
       h(r) = 2(E - Phi(r)) - L^2/r^2."""
    lo, hi = np.log(rc) - 40.0, np.log(rc)                                    # h(lo) < 0 (L^2/r^2 huge) , h(hi) >= 0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        r = np.exp(mid)
        hm = 2 * (E - Phi(r)) - L2 / r ** 2
        pos = hm >= 0
        hi = np.where(pos, mid, hi)
        lo = np.where(pos, lo, mid)
    rp = np.exp(0.5 * (lo + hi))
    lo, hi = np.log(rc), np.log(rc) + 40.0                                    # h(lo) >= 0 , h(hi) < 0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        r = np.exp(mid)
        hm = 2 * (E - Phi(r)) - L2 / r ** 2
        pos = hm >= 0
        lo = np.where(pos, mid, lo)
        hi = np.where(pos, hi, mid)
    ra = np.exp(0.5 * (lo + hi))
    return rp, ra


def orbit_grid(pot, rc_lo, rc_hi, per_decade, etas):
    """orbits labelled by circular radius rc and circularity eta = L/L_c(rc); returns rc, eta, E, L2, rp, ra flattened."""
    nrc = max(int(round(per_decade * (math.log10(rc_hi) - math.log10(rc_lo)))) + 1, 3)
    rcs = np.geomspace(rc_lo, rc_hi, nrc)
    RC, ETA = np.meshgrid(rcs, np.asarray(etas, float), indexing="ij")
    RC, ETA = RC.ravel(), ETA.ravel()
    g = pot.g(RC)
    Ec = pot.Phi(RC) + 0.5 * RC * g
    L2 = ETA ** 2 * RC ** 3 * g
    rp, ra = _roots(pot.Phi, Ec, L2, RC)
    return dict(rc=RC, eta=ETA, E=Ec, L2=L2, rp=rp, ra=ra)


def default_etas(n_tan=10, n_lin=14):
    return np.concatenate([np.geomspace(0.003, 0.3, n_tan), np.linspace(0.36, 0.9995, n_lin)])


def orbit_moments(pot, og, redges, beta_fn, npsi=300, chunk=400):
    """time-fraction moments of every orbit in the radial bins [redges[j], redges[j+1]]:
         M   = fraction of the orbit's time inside the bin      (mass of a unit-mass orbit)
         Kr  = Int v_r^2 dt / T ,   Kt = Int (L^2/r^2) dt / T ,   Kb = Int [L^2/r^2 - 2 (1 - beta(r)) v_r^2] dt / T .
       r is parametrised by ln r = lm - la cos(psi) so dt/dpsi is smooth through the turning points and wide peri/apo ratios."""
    n = len(og["rc"])
    nb = len(redges) - 1
    M = np.zeros((n, nb)); Kr = np.zeros((n, nb)); Kt = np.zeros((n, nb)); Kb = np.zeros((n, nb))
    lre = np.log(redges)
    psi_e = np.linspace(0.0, math.pi, npsi + 1)
    psi_m = 0.5 * (psi_e[1:] + psi_e[:-1])
    dpsi = psi_e[1] - psi_e[0]
    for s in range(0, n, chunk):
        sl = slice(s, min(s + chunk, n))
        lp, la_ = np.log(og["rp"][sl]), np.log(og["ra"][sl])
        lm = 0.5 * (lp + la_)[:, None]
        la = 0.5 * (la_ - lp)[:, None]
        E = og["E"][sl][:, None]
        L2 = og["L2"][sl][:, None]
        lr_m = lm - la * np.cos(psi_m)[None, :]
        r_m = np.exp(lr_m)
        vr2 = np.maximum(2 * (E - pot.Phi(r_m)) - L2 / r_m ** 2, 1e-30)
        dt = r_m * la * np.sin(psi_m)[None, :] * dpsi / np.sqrt(vr2)
        vt2 = L2 / r_m ** 2
        bet = pot.beta(r_m) if beta_fn is None else beta_fn(r_m)
        cols = [dt, dt * vr2, dt * vt2, dt * (vt2 - 2 * (1 - bet) * vr2)]
        cums = [np.concatenate([np.zeros((dt.shape[0], 1)), np.cumsum(c, axis=1)], axis=1) for c in cols]
        T = cums[0][:, -1:]
        lr_e = lm - la * np.cos(psi_e)[None, :]
        for k in range(dt.shape[0]):
            for c_i, out in enumerate((M, Kr, Kt, Kb)):
                cv = np.interp(lre, lr_e[k], cums[c_i][k] / T[k, 0])
                out[s + k] = np.diff(cv)
    return dict(M=M, Kr=Kr, Kt=Kt, Kb=Kb)


def bin_targets(pot, redges, sr2_fn=None, nsub=64):
    """target bin integrals: b_m = Int 4 pi r^2 rho dr ; b_r = Int 4 pi r^2 rho sigma_r^2 dr (sigma_r^2 = V_c^2/2 unless sr2_fn given);
       returned with the Simpson rule on nsub sub-intervals in ln r."""
    nb = len(redges) - 1
    bm = np.zeros(nb); br = np.zeros(nb)
    sr2_fn = pot.sr2 if sr2_fn is None else sr2_fn
    for j in range(nb):
        lr = np.linspace(math.log(redges[j]), math.log(redges[j + 1]), 2 * nsub + 1)
        r = np.exp(lr)
        f1 = FOUR_PI * r ** 3 * pot.rho(r)
        f2 = f1 * sr2_fn(r)
        w = np.ones_like(lr); w[1:-1:2] = 4; w[2:-1:2] = 2
        d = (lr[-1] - lr[0]) / (2 * nsub) / 3
        bm[j] = d * np.sum(w * f1); br[j] = d * np.sum(w * f2)
    return bm, br


# ------------------------------------------------------------------------------------------------------ the linear programme
def solve_lp(mom, bm, br, variant, rows=None, bscale_floor=0.0):
    """min t  s.t.  |(A w - b)_j| <= t s_j ,  w >= 0.   variant: 'V1' (mass rows), 'V2' (+ beta rows), 'V3' (+ radial-energy rows).
       rows: optional slice of bins to use.  returns eps* (the min-max relative residual) and the weights."""
    from scipy.optimize import linprog
    nb = len(bm)
    sel = np.arange(nb) if rows is None else np.arange(nb)[rows]
    A, b, s = [mom["M"][:, sel].T], [bm[sel]], [bm[sel]]
    if variant in ("V2", "V3"):
        A.append(mom["Kb"][:, sel].T); b.append(np.zeros(len(sel))); s.append(2 * br[sel])
    if variant == "V2iso":                                            # beta = 0 imposed: <v_t^2> = 2 <v_r^2>
        A.append((mom["Kt"] - 2 * mom["Kr"])[:, sel].T); b.append(np.zeros(len(sel))); s.append(2 * br[sel])
    if variant == "V3":
        A.append(mom["Kr"][:, sel].T); b.append(br[sel]); s.append(br[sel])
    A = np.vstack(A); b = np.concatenate(b); s = np.concatenate(s)
    A = A / s[:, None]; b = b / s
    R, n = A.shape
    c = np.zeros(n + 1); c[-1] = 1.0
    Aub = np.vstack([np.hstack([A, -np.ones((R, 1))]), np.hstack([-A, -np.ones((R, 1))])])
    bub = np.concatenate([b, -b])
    res = linprog(c, A_ub=Aub, b_ub=bub, bounds=[(0, None)] * n + [(0, None)], method="highs")
    if res.status != 0:
        return float("nan"), None
    return float(res.x[-1]), res.x[:-1]


def solve_lp_margin(mom, bm, br, variant, tol=0.02, rows=None):
    """SUPPLEMENT (added after the first LP result, not a frozen criterion): interior feasibility.  max lam  s.t.  |(A w - b)_j| <= tol s_j , w_i >= lam
       for every orbit that touches the window.  lam > 0  <=>  a strictly positive weight function (a positive margin) exists at that tolerance.
       returns lam/mean(w over the contributing orbits) (<= 1)."""
    from scipy.optimize import linprog
    nb = len(bm)
    sel = np.arange(nb) if rows is None else np.arange(nb)[rows]
    A, b, s = [mom["M"][:, sel].T], [bm[sel]], [bm[sel]]
    if variant in ("V2", "V3"):
        A.append(mom["Kb"][:, sel].T); b.append(np.zeros(len(sel))); s.append(2 * br[sel])
    if variant == "V3":
        A.append(mom["Kr"][:, sel].T); b.append(br[sel]); s.append(br[sel])
    A = np.vstack(A); b = np.concatenate(b); s = np.concatenate(s)
    A = A / s[:, None]; b = b / s
    touch = np.abs(A).sum(axis=0) > 0
    A = A[:, touch]
    R_, n = A.shape
    c = np.zeros(n + 1); c[-1] = -1.0
    Aub = np.vstack([np.hstack([A, np.zeros((R_, 1))]), np.hstack([-A, np.zeros((R_, 1))]),
                     np.hstack([-np.eye(n), np.ones((n, 1))])])
    bub = np.concatenate([b + tol, -b + tol, np.zeros(n)])
    res = linprog(c, A_ub=Aub, b_ub=bub, bounds=[(0, None)] * n + [(0, None)], method="highs")
    if res.status != 0:
        return float("nan")
    w = res.x[:-1]
    return float(res.x[-1] / np.mean(w)) if np.mean(w) > 0 else 0.0


# ------------------------------------------------------------------------------------------------------ report
class Report:
    def __init__(self, slug, mutate):
        self.slug = slug + ("_MUTATE" if mutate else "")
        self.lines, self.checks, self.numbers, self.t0 = [], [], {}, time.time()

    def P(self, s=""):
        print(s, flush=True)
        self.lines.append(s)

    def banner(self, s):
        self.P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)

    def check(self, name, detail, ok, load_bearing=True):
        self.checks.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=load_bearing))
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")

    def num(self, k, v):
        self.numbers[k] = v

    def write(self):
        lb = [c for c in self.checks if c["load_bearing"]]
        nf = sum(not c["ok"] for c in lb)
        self.P(f"\n  {sum(c['ok'] for c in self.checks)}/{len(self.checks)} checks pass; load-bearing failures: {nf}   ({time.time() - self.t0:.0f} s)")

        def clean(o):
            if isinstance(o, dict):
                return {str(k): clean(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [clean(v) for v in o]
            if isinstance(o, (np.floating, float)):
                return float(o) if np.isfinite(o) else str(o)
            if isinstance(o, np.integer):
                return int(o)
            if isinstance(o, (np.bool_, bool)):
                return bool(o)
            if isinstance(o, np.ndarray):
                return clean(o.tolist())
            return o if isinstance(o, (int, str)) or o is None else str(o)

        json.dump(clean(dict(slug=self.slug, load_bearing_failures=nf, checks=self.checks, numbers=self.numbers)),
                  open(os.path.join(HERE, self.slug + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")
        return nf
