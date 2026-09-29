#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg123_nl -- numerical machinery for the nonlinear ladder (N1-N3): integrate the exact static localised-RR system in the tilde variables of
cfg123_static.build_tilde (exponential sphere rho-tilde = e^{-r}, r in units of the scale height h, G = c = 1).
"""
import os, sys, math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, root

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg123_static as CS

R0 = 1e-4
_T = None


def T():
    global _T
    if _T is None:
        _T = CS.build_tilde()
    return _T


def y0_state(pc, Uc, rho0=1.0):
    """regular series initial data at r = R0 for the exponential sphere (rho-tilde(0) = 1)."""
    r0 = R0
    return np.array([0.0, rho0 * r0 ** 2 / 3.0, pc, Uc, -rho0 * r0 / 3.0, 0.0, -Uc * r0 / 3.0])


def rhs_y(r, y, lam, eps):
    t = T()
    return np.asarray(t["T"](r, *y, lam, eps, math.exp(-r))).ravel()


def integrate(eps, lam, pc, Uc, rmax, dense=False, rtol=1e-12, atol=1e-14):
    sol = solve_ivp(lambda r, y: rhs_y(r, y, lam, eps), (R0, rmax), y0_state(pc, Uc), method="DOP853", rtol=rtol, atol=atol, dense_output=dense)
    if not sol.success:
        raise RuntimeError("integration failed: " + sol.message)
    return sol


def U_exterior_c1_GR(sol_end, eps, rmax):
    """c1 = U(rmax) - (Q/(2M sqrt(k))) ln(1 - 2M/rmax) for the GR (lam = 0) Schwarzschild exterior; tilde variables."""
    at, bt, pt, Ut, Utp, St, Stp = sol_end
    a, b = 1 + eps * at, 1 + eps * bt
    z = 1.0 - 1.0 / b                                                   # 2M/r
    Q = rmax ** 2 * math.sqrt(a / b) * Utp                              # tilde flux (eps factored out)
    sqk = math.sqrt(a / (1.0 - z))
    if abs(z) < 1e-300:
        logterm = -1.0 / rmax
    else:
        logterm = math.log1p(-z) / (z * rmax)
    return Ut - (Q / sqk) * logterm


def solve_bg_pc(eps, rmax):
    """lam = 0 GR: shoot p~(0) so that p~(rmax) = 0; p~ = p-hat/eps^2 (monotone increasing in p~(0) where the integration exists; hydrostatic p~(0) ~ 0.06)."""
    if eps == 0.0:
        return 0.0

    def f(pc):
        try:
            return integrate(eps, 0.0, pc, 0.0, rmax).y[2, -1]
        except RuntimeError:
            return -1.0                                                # too little central pressure: the integration breaks down (negative p, singular)

    lo, hi = None, None
    for c in (0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.15, 0.2, 0.3, 0.5, 1.0, 2.0):
        v = f(c)
        if v < 0:
            lo = c
        elif lo is not None:
            hi = c
            break
    if lo is None or hi is None:
        raise RuntimeError("p~(0) bracket not found")
    return brentq(f, lo, hi, xtol=1e-15, rtol=1e-14)


def solve_Uc_GR(eps, pc, rmax):
    """lam = 0: U~ is affine in U~(0); fix U~(0) so that the constant c1 of the exterior U = c1 + ... vanishes (zero-data: U -> 0 at infinity)."""
    c0 = U_exterior_c1_GR(integrate(eps, 0.0, pc, 0.0, rmax).y[:, -1], eps, rmax)
    c1 = U_exterior_c1_GR(integrate(eps, 0.0, pc, 1.0, rmax).y[:, -1], eps, rmax)
    return -c0 / (c1 - c0)


def variational(eps, rmax, pc=None, Uc=None, rout=None):
    """O(lam) variational system about lam = 0 at exact eps: Z = [y~(7), Y(7)], Y = d y~/d lam; returns g~_lam(r) on rout (and the GR force g~(r)).
    p~_lam(0) fixed by p~_lam(rmax) = 0 (linear shooting); U~(0), S~(0) as in solve_Uc_GR / S(0) = 0."""
    t = T()
    if pc is None:
        pc = solve_bg_pc(eps, rmax)
    if Uc is None:
        Uc = solve_Uc_GR(eps, pc, rmax)

    def rhsZ(r, Z):
        y, Y = Z[:7], Z[7:]
        rt_ = math.exp(-r)
        f = np.asarray(t["T"](r, *y, 0.0, eps, rt_)).ravel()
        J = np.asarray(t["JT"](r, *y, 0.0, eps, rt_))
        Tl = np.asarray(t["TL"](r, *y, 0.0, eps, rt_)).ravel()
        return np.concatenate([f, J @ Y + Tl])

    def run(p1):
        Z0 = np.concatenate([y0_state(pc, Uc), np.zeros(7)])
        Z0[7 + 2] = p1
        return solve_ivp(rhsZ, (R0, rmax), Z0, method="DOP853", rtol=1e-12, atol=1e-14, dense_output=True)

    s0, s1 = run(0.0), run(1.0)
    p1 = -s0.y[7 + 2, -1] / (s1.y[7 + 2, -1] - s0.y[7 + 2, -1])
    sol = run(p1)
    out = {}
    if rout is not None:
        rr = np.asarray(rout, float)
        Zr = sol.sol(rr)
        gl, g = [], []
        for i, r in enumerate(rr):
            y, Y = Zr[:7, i], Zr[7:, i]
            rt_ = math.exp(-r)
            gy = np.asarray(t["gy"](r, *y, 0.0, eps, rt_)).ravel()
            gl.append(float(gy @ Y + t["gl"](r, *y, 0.0, eps, rt_)))
            g.append(float(t["g"](r, *y, 0.0, eps, rt_)))
        out = dict(r=rr, g_lam=np.array(gl), g=np.array(g))
    return out, dict(pc=pc, Uc=Uc, p1=p1, sol=sol)


# ------------------------------------------------------------------------------------------------ finite lam (N2)
def beta_flat(y_end, lam, rmax):
    """exterior flat-space form U r = alpha cos(m r) + beta sin(m r); returns beta (tilde)."""
    at, bt, pt, Ut, Utp, St, Stp = y_end
    m = math.sqrt(lam)
    f = Ut * rmax
    fp = Ut + rmax * Utp
    return f * math.sin(m * rmax) + fp / m * math.cos(m * rmax)


def solve_finite(eps, lam, rmax, guess=None):
    """finite lam, finite eps: shoot (p~(0), U~(0)) so that p~(rmax) = 0 and beta = 0 (standing-wave prescription, flat exterior form)."""
    if guess is None:
        pc0 = solve_bg_pc(eps, rmax)
        b0_ = beta_flat(integrate(eps, lam, pc0, 0.0, rmax).y[:, -1], lam, rmax)
        b1_ = beta_flat(integrate(eps, lam, pc0, 1.0, rmax).y[:, -1], lam, rmax)
        guess = (pc0, -b0_ / (b1_ - b0_))

    def res(v):
        s = integrate(eps, lam, v[0], v[1], rmax).y[:, -1]
        return [s[2] / max(eps ** 2, 1e-30) if eps != 0 else 0.0, beta_flat(s, lam, rmax)]

    if eps == 0.0:
        return guess[0], guess[1]
    r_ = root(res, guess, method="hybr", tol=1e-13)
    return r_.x[0], r_.x[1]


def g_at(eps, lam, pc, Uc, rmax, rout):
    sol = integrate(eps, lam, pc, Uc, rmax, dense=True)
    t = T()
    Zr = sol.sol(np.asarray(rout, float))
    return np.array([float(t["g"](r, *Zr[:, i], lam, eps, math.exp(-r))) for i, r in enumerate(rout)]), sol


def theta_theta_residual(sol, lam, eps, rr):
    """independent check: E_thth - p-hat r^2 with A'' from a finite difference of A' along the solution."""
    t = T()
    b0 = t["b0"]
    import sympy as sp
    if "Eth_f" not in t:
        S_ = b0["syms"]
        args = [S_["a"], S_["b"], S_["U"], S_["Up"], S_["S"], S_["Sp"], S_["ap"], S_["bp"], S_["Spp"], b0["app"], b0["ph"], b0["lam"], b0["r"], b0["rh"]]
        t["Eth_f"] = sp.lambdify(args, b0["Ethth"], "numpy", cse=True)
        # Spp from box S = -U
        t["ap_f"] = sp.lambdify([b0["r"], *b0["y"], b0["lam"], b0["rh"]], b0["ap"], "numpy", cse=True)
        t["bp_f"] = sp.lambdify([b0["r"], *b0["y"], b0["lam"], b0["rh"]], b0["bp"], "numpy", cse=True)
        t["Spp_f"] = sp.lambdify([b0["r"], *b0["y"], b0["lam"], b0["rh"]], b0["rhs"][6], "numpy", cse=True)
    worst = 0.0
    rows = []
    for r in rr:
        def full(rq):
            yt = sol.sol(rq)
            at, bt, pt, Ut, Utp, St, Stp = yt
            y = [1 + eps * at, 1 + eps * bt, eps ** 2 * pt, eps * Ut, eps * Utp, eps * St, eps * Stp]
            rh = eps * math.exp(-rq)
            return y, rh
        y, rh = full(r)
        d = 1e-4 * max(1.0, r)
        ym, rhm = full(r - d); yp_, rhp = full(r + d)
        apf = lambda yy, rq, rhh: float(t["ap_f"](rq, *yy, lam, rhh))
        app = (apf(yp_, r + d, rhp) - apf(ym, r - d, rhm)) / (2 * d)
        ap, bp = apf(y, r, rh), float(t["bp_f"](r, *y, lam, rh))
        Spp = float(t["Spp_f"](r, *y, lam, rh))
        Eth = float(t["Eth_f"](y[0], y[1], y[3], y[4], y[5], y[6], ap, bp, Spp, app, y[2], lam, r, rh))
        resid = Eth - y[2] * r * r
        scale = max(abs(Eth), abs(y[2] * r * r), abs(app) * r * r, 1e-300)
        rows.append((r, resid, scale))
        worst = max(worst, abs(resid) / scale)
    return worst, rows
