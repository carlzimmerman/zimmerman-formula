#!/usr/bin/env python3
"""MK2 library (criteria 3b4f515ff8): static dust of action (A) with a general dust term, around extended baryons on the a0 law,
with self-gravity and form B's share cap. One generic spherical solver serves clusters (SI units) and galaxies (units r_M, M_b,
s = sqrt(G M_b a0), so G = a0 = 1).
Static equation (criteria section 1): r^2 mu(g/a0) g = G [M_b(r) + M_d(r)], M_d' = 4 pi r^2 delta_rho_d(Phi);
    exponential: delta_rho_d = rho_bar (exp(|Phi|/c_s^2) - 1);   quadratic: delta_rho_d = mu^2 |Phi| / (4 pi G).
Cap: the charge C(r) = M_L(r) - M_b(r) ends at r_c where C = X M_b(r_c); beyond, M_L = M_b(r) + C(r_c) (Newtonian) and Phi -> 0 at
infinity. Outward shooting on the central potential Phi0 (dust zero at the centre), branch continuous from no dust.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "MK1_one_dust_constant"))
import mk1_lib as L1
G, MSUN, KPC, MPC = L1.G, L1.MSUN, L1.KPC, L1.MPC
C_SI = 2.99792458e8
A0 = L1.A0; FOOT = L1.FOOT
NOTE = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."


def law_g(gN, a0):
    gN = np.maximum(gN, 0.0)
    return 0.5 * gN + np.sqrt(0.25 * gN * gN + a0 * gN)


def src_from_ML(ML, r, Gc, a0):
    """the law inverted: the source mass M_src with M_src nu(G M_src/(r^2 a0)) = M_L (criteria section 3, row c)."""
    return ML * ML / (ML + r * r * a0 / Gc)


class Dust:
    """overdensity of the static dust as a function of the potential Phi (< 0 in wells).
    kind 'exp': rho_bar expm1(-Phi / cs2); 'quad': mu2 (-Phi) / (4 pi Gc); 'none': 0. sig -1 flips the sign (not used for exp)."""
    def __init__(self, kind, rho_bar=0.0, cs2=1.0, mu2=0.0, Gc=G):
        self.kind, self.rho_bar, self.cs2, self.mu2, self.Gc = kind, rho_bar, cs2, mu2, Gc
    def __call__(self, Phi):
        if self.kind == "exp":
            a = np.minimum(-Phi / self.cs2, 700.0)
            return self.rho_bar * np.expm1(a)
        if self.kind == "quad":
            return self.mu2 * (-Phi) / (4 * math.pi * self.Gc)
        return 0.0 * Phi


def integrate_out(Phi0, Mb_fn, dust, X, Gc, a0, r0, r1, self_grav=True, cap=True, dense=False):
    """outward from r0 with Phi(r0) = Phi0, M_d(r0) = 0 (the dust inside r0 is neglected; r0 << every scale). Stops at the cap.
    Returns (rc, Phi(rc), Md(rc), sol) or (None, ...) if the cap is not reached by r1."""
    def f(u, y):
        r = math.exp(u); Phi, Md = y; Mb = Mb_fn(r)
        Msrc = Mb + (Md if self_grav else 0.0)
        g = law_g(Gc * Msrc / (r * r), a0) if Msrc > 0 else -law_g(Gc * (-Msrc) / (r * r), a0)
        return [r * g, 4 * math.pi * r ** 3 * float(dust(Phi))]
    def cap_ev(u, y):
        r = math.exp(u); Phi, Md = y; Mb = Mb_fn(r); Msrc = Mb + Md
        ML = Msrc * (0.5 + math.sqrt(0.25 + r * r * a0 / (Gc * Msrc))) if Msrc > 0 else Msrc
        return (ML - Mb) - X * Mb_fn.Mtot                 # A2: global cap
    cap_ev.terminal = True; cap_ev.direction = 1
    with np.errstate(all="ignore"):
        sol = solve_ivp(f, (math.log(r0), math.log(r1)), [Phi0, 0.0], method="DOP853", rtol=1e-9, atol=1e-30 + 0.0,
                        events=cap_ev if cap else None, dense_output=dense, max_step=0.05)
    if cap and sol.t_events[0].size:
        u = sol.t_events[0][0]; y = sol.y_events[0][0]; return math.exp(u), y[0], y[1], sol
    if not cap:
        return math.exp(sol.t[-1]), sol.y[0, -1], sol.y[1, -1], sol
    return None, None, None, sol


class Baryons:
    """M_b(r) tabulated on a log grid (np.interp in log r); M_b constant beyond the grid's end. tail(r) = Int_r^inf G M_b / r'^2 dr'."""
    def __init__(self, r, M, Gc):
        self.r = np.asarray(r, float); self.M = np.asarray(M, float); self.lr = np.log(self.r); self.Gc = Gc
        f = Gc * self.M / self.r ** 2; seg = 0.5 * (f[1:] + f[:-1]) * np.diff(self.r)
        self.cum = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) + Gc * self.M[-1] / self.r[-1]
        self.lM = np.log(np.maximum(self.M, 1e-300)); self.Mtot = float(self.M[-1])     # A2: the system's baryons (constant beyond the grid)
    def __call__(self, x):
        if x <= self.r[0]: return self.M[0] * (x / self.r[0]) ** 3
        if x >= self.r[-1]: return self.M[-1]
        return math.exp(np.interp(math.log(x), self.lr, self.lM))
    def tail(self, x):
        if x >= self.r[-1]: return self.Gc * self.M[-1] / x
        if x <= self.r[0]: return float(self.cum[0])
        return float(np.interp(math.log(x), self.lr, self.cum))


def phi_out(rc, C, Mb_fn, Gc, r_far=None, n=None):
    """Phi(rc) for M_L(r) = M_b(r) + C beyond rc (Newtonian: the charge has ended); Phi -> 0 at infinity."""
    return -(Gc * C / rc + Mb_fn.tail(rc))


def solve_capped(Mb_fn, dust, X, Gc, a0, r0, r1, r_far, Phi0_prev, self_grav=True, n_scan=41, span=(0.97, 4.0)):
    """the capped static state on the branch continuous from Phi0_prev: root of F(Phi0) = Phi(rc) - Phi_out(rc), searched on
    Phi0 in [span[1], span[0]] x Phi0_prev (deeper allowed). Returns dict(ok, Phi0, rc, ...)."""
    def F(P0):
        rc, Pc, Md, _ = integrate_out(P0, Mb_fn, dust, X, Gc, a0, r0, r1, self_grav)
        if rc is None: return np.nan
        C = X * Mb_fn.Mtot
        return Pc - phi_out(rc, C, Mb_fn, Gc, r_far)
    grid = Phi0_prev * np.geomspace(span[0], span[1], n_scan)          # Phi0 < 0: from slightly shallower to much deeper
    vals = np.array([F(p) for p in grid])
    br = [(grid[i], grid[i + 1]) for i in range(len(grid) - 1) if np.isfinite(vals[i]) and np.isfinite(vals[i + 1]) and vals[i] * vals[i + 1] <= 0]
    if not br:
        return dict(ok=False, reason="no capped state on the branch (fold or cap not reached)", Phi0=np.nan)
    a, b = br[0]                                                        # nearest the previous point (the grid starts there)
    P0 = brentq(F, a, b, xtol=abs(Phi0_prev) * 1e-12, rtol=1e-12, maxiter=200)
    rc, Pc, Md, sol = integrate_out(P0, Mb_fn, dust, X, Gc, a0, r0, r1, self_grav, dense=True)
    return dict(ok=True, Phi0=P0, rc=rc, Phi_c=Pc, Md_c=Md, C=X * Mb_fn.Mtot, sol=sol, n_roots=len(br))


def profile_eval(st, r, Mb_fn, Gc, a0):
    """M_L(r), M_d(r), Phi(r) of a solved capped state (beyond rc: Newtonian with the ended charge). The measured mass counts the dust
    whether or not it self-gravitates (M-NOSELF changes only the potential that sets it)."""
    r = np.atleast_1d(np.asarray(r, float)); ML = np.empty(len(r)); Md = np.empty(len(r)); Ph = np.empty(len(r)); rc = st["rc"]
    for i, x in enumerate(r):
        if x <= rc:
            y = st["sol"].sol(math.log(x)); Ph[i], Md[i] = y[0], y[1]; Ms = Mb_fn(x) + Md[i]
            ML[i] = Ms * (0.5 + math.sqrt(0.25 + x * x * a0 / (Gc * Ms)))
        else:
            Md[i] = st["Md_c"]; ML[i] = Mb_fn(x) + st["C"]; Ph[i] = -(Gc * st["C"] / x + Mb_fn.tail(x))
    return ML, Md, Ph


def hernquist(xa, n=3000):
    x = np.geomspace(1e-7, 1e7, n); return Baryons(x, x * x / (x + xa) ** 2, 1.0)


def emden_check():
    """KA2: Emden's isothermal equation psi'' + 2 psi'/xi = exp(-psi) integrated by the same DOP853 settings."""
    def f(xi, y): return [y[1], math.exp(-y[0]) - 2 * y[1] / xi]
    xi0 = 1e-6; xs = np.geomspace(xi0, 1e4, 200001)
    s = solve_ivp(f, (xi0, 1e4), [xi0 ** 2 / 6, xi0 / 3], t_eval=xs, rtol=1e-11, atol=1e-14, method="DOP853")
    psi = s.y[0]; i = int(np.argmin(np.abs(xs - 6.451))); contrast = math.exp(psi[i])
    r = np.exp(-psi) * xs ** 2 / 2; m = (xs >= 3e3) & (xs <= 1e4)
    return dict(contrast_6451=contrast, sis_ratio_min=float(r[m].min()), sis_ratio_max=float(r[m].max()))


# ------------------------------------------------------------------ fast fixed-step RK4 in u = ln r on a precomputed grid (same equations)
class Grid:
    """u grid from ln r0 to ln r1, step h; baryon masses at the nodes and half-nodes."""
    def __init__(self, Mb, r0, r1, h=0.01):
        n = int(math.ceil((math.log(r1) - math.log(r0)) / h)); self.u = math.log(r0) + h * np.arange(n + 1); self.h = h
        self.r = np.exp(self.u); self.rh = np.exp(self.u + 0.5 * h)
        self.M = np.array([Mb(x) for x in self.r]); self.Mh = np.array([Mb(x) for x in self.rh]); self.Mb = Mb


def rk4_out(Phi0, grid, dust_kind, rho4pi, cs2, mu2_4piG, X, Gc, a0, self_grav=True, cap=True, phi_zero_at=None):
    """returns (rc, Phi_c, Md_c, k_stop, Phi_arr, Md_arr). dust_kind: 0 none, 1 exp (rho4pi = 4 pi rho_bar), 2 quad (mu2_4piG = mu^2/G)."""
    h = grid.h; r = grid.r; rh = grid.rh; M = grid.M; Mh = grid.Mh; n = len(r)
    Phi = Phi0; Md = 0.0; P = [Phi]; D = [0.0]; sqrt = math.sqrt; expm1 = math.expm1
    def F(Ph, Md_, Mb, x):
        Ms = Mb + Md_ if self_grav else Mb
        if Ms > 0:
            gN = Gc * Ms / (x * x); g = 0.5 * gN + sqrt(0.25 * gN * gN + a0 * gN)
        else:
            gN = Gc * (-Ms) / (x * x); g = -(0.5 * gN + sqrt(0.25 * gN * gN + a0 * gN))
        if dust_kind == 1:
            a = -Ph / cs2; a = 700.0 if a > 700.0 else a; dd = rho4pi * x ** 3 * expm1(a)
        elif dust_kind == 2:
            dd = mu2_4piG * x ** 3 * (-Ph)
        else:
            dd = 0.0
        return x * g, dd
    Mtot = grid.Mb.Mtot
    def capf(Ph, Md_, Mb, x):
        Ms = Mb + Md_
        ML = Ms * (0.5 + sqrt(0.25 + x * x * a0 / (Gc * Ms))) if Ms > 0 else Ms
        return (ML - Mb) - X * Mtot                        # A2: global cap
    c_prev = capf(Phi, Md, M[0], r[0])
    for k in range(n - 1):
        x0, xm, x1 = r[k], rh[k], r[k + 1]
        k1 = F(Phi, Md, M[k], x0)
        k2 = F(Phi + 0.5 * h * k1[0], Md + 0.5 * h * k1[1], Mh[k], xm)
        k3 = F(Phi + 0.5 * h * k2[0], Md + 0.5 * h * k2[1], Mh[k], xm)
        k4 = F(Phi + h * k3[0], Md + h * k3[1], M[k + 1], x1)
        Pn = Phi + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); Dn = Md + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        if not (Pn == Pn and Dn == Dn) or abs(Dn) > 1e300:
            return None, None, None, k, np.array(P), np.array(D)
        if cap:
            c_new = capf(Pn, Dn, M[k + 1], x1)
            if c_prev < 0 <= c_new:
                t = c_prev / (c_prev - c_new); u = grid.u[k] + t * h
                Pc = Phi + t * (Pn - Phi); Dc = Md + t * (Dn - Md); P.append(Pn); D.append(Dn)
                return math.exp(u), Pc, Dc, k + 1, np.array(P), np.array(D)
            c_prev = c_new
        Phi, Md = Pn, Dn; P.append(Phi); D.append(Md)
    if phi_zero_at is not None:
        return r[-1], Phi, Md, n - 1, np.array(P), np.array(D)
    return None, None, None, n - 1, np.array(P), np.array(D)


def shoot_fast(grid, dust_kind, rho4pi, cs2, mu2_4piG, X, Gc, a0, Phi0_prev, self_grav=True, cap=True, steps=(0.0, -0.002, 0.002, -0.006, 0.006, -0.012, 0.015, -0.02, 0.035, 0.08, 0.17, 0.3, 0.6), first=False):
    """root of the cap mismatch along the branch from Phi0_prev (Phi0 < 0; deeper = more negative). first=True: wide scan (no-dust start).
    With cap=False (M-NOCAP): Phi = 0 at the grid's end (3 R200) instead."""
    Mb = grid.Mb
    def Fm(P0):
        rc, Pc, Dc, k, _, _ = rk4_out(P0, grid, dust_kind, rho4pi, cs2, mu2_4piG, X, Gc, a0, self_grav, cap, phi_zero_at=(None if cap else True))
        if rc is None: return np.nan
        if not cap: return Pc                                   # Phi(3 R200) = 0
        return Pc - (-(Gc * X * Mb.Mtot / rc + Mb.tail(rc)))
    if first:
        cand = Phi0_prev * np.geomspace(0.02, 50, 121)
    else:
        cand = np.array([Phi0_prev * (1 + s) for s in steps])
        order = np.argsort(np.abs(np.array(steps)))
        cand = cand[order]
    vals = [(p, Fm(p)) for p in cand]
    vals = [v for v in vals if np.isfinite(v[1])]
    vals.sort(key=lambda t: t[0])
    br = [(vals[i][0], vals[i + 1][0]) for i in range(len(vals) - 1) if vals[i][1] * vals[i + 1][1] <= 0]
    if not br:
        return dict(ok=False, reason="no static capped state on the branch (fold)" if cap else "no state with Phi(3 R200) = 0", Phi0=np.nan)
    a, b = min(br, key=lambda ab: abs(0.5 * (ab[0] + ab[1]) - Phi0_prev))
    P0 = brentq(Fm, a, b, xtol=abs(Phi0_prev) * 1e-10, rtol=1e-12, maxiter=100)
    rc, Pc, Dc, k, Parr, Darr = rk4_out(P0, grid, dust_kind, rho4pi, cs2, mu2_4piG, X, Gc, a0, self_grav, cap, phi_zero_at=(None if cap else True))
    return dict(ok=True, Phi0=P0, rc=rc, Phi_c=Pc, Md_c=Dc, C=(X * Mb.Mtot if cap else None), u=grid.u[:len(Parr)], Phi=Parr, Md=Darr, k=k, n_br=len(br))


def eval_fast(st, r, grid, Gc, a0):
    """M_L(r), M_d(r), Phi(r) of a shoot_fast state (beyond rc: Newtonian with the ended charge)."""
    r = np.atleast_1d(np.asarray(r, float)); lu = np.log(r); Mb = grid.Mb
    Md = np.interp(lu, st["u"], st["Md"]); Ph = np.interp(lu, st["u"], st["Phi"])
    ML = np.empty(len(r))
    for i, x in enumerate(r):
        if st["C"] is not None and x > st["rc"]:
            Md[i] = st["Md_c"]; ML[i] = Mb(x) + st["C"]; Ph[i] = -(Gc * st["C"] / x + Mb.tail(x))
        else:
            Ms = Mb(x) + Md[i]; ML[i] = Ms * (0.5 + math.sqrt(0.25 + x * x * a0 / (Gc * Ms))) if Ms > 0 else Ms
    return ML, Md, Ph
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
