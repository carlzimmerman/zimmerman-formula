#!/usr/bin/env python3
"""MK1 library (criteria b1fbded1e2): the static dust of action (A) around a point baryon mass on the a0 law, capped at form B's
share (ONE1's construction) or uncapped (S4's zero point), its exact projection, and the neighbour kernel generalised to it.

Units: x = r / r_M with r_M = sqrt(G M_b / a0); potential phi = Phi / s with s = sqrt(G M_b a0) = a0 r_M; masses in M_b.
Static equation (QX17 limits table, gamma_L = 0): r^2 mu(g/a0) g = G (M_b + M_K), M_K' = -sig mu_K^2 r^2 Phi / G. In these units
    ell(x) = M_L / M_b = sgn(ms) (|ms|/2 + sqrt(ms^2/4 + |ms| x^2)),  ms = 1 + kappa,
    dphi/dx = ell / x^2,   dkappa/dx = -sig m^2 x^2 phi,   m = mu_K r_M,   sig = +1 (action), -1 (MUTATE M-SIGN).
Capped (form B): the charge ell - 1 reaches X at x_c; beyond, ell = 1 + X and phi = -(1 + X)/x. At x_c the law fixes
ms_c = (1 + X)^2 / (x_c^2 + 1 + X); shoot on x_c (inward integration) so that kappa(0) = 0.
Uncapped: phi = the mu_K = 0 law potential matched to S4's zero point at 3 Mpc, integrated outward to x_end with the dust.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; MPC = 3.0857e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOT = ("canonical", "alt")
XMIN = 1e-5


def ell_of(ms, x):
    a = np.abs(ms)
    return np.sign(ms) * (0.5 * a + np.sqrt(0.25 * a * a + a * x * x))


def phi_law(x, C=0.0):
    """mu_K = 0 law potential of a point mass (units s): -1/(2x) - sqrt(1/4 + x^2)/x + asinh(2x) + C (derivative ell/x^2)."""
    x = np.asarray(x, float)
    return -0.5 / x - np.sqrt(0.25 + x * x) / x + np.arcsinh(2 * x) + C


def _rhs(sig, m):
    m2 = m * m
    def f(u, y):
        x = math.exp(u); phi, kap = y
        ell = ell_of(1.0 + kap, x)
        return [ell / x, -sig * m2 * x ** 3 * phi]          # d/du with u = ln x
    return f


def _shoot_fn(m, X, sig):
    f = _rhs(sig, m)
    def shoot(xc, dense=False):
        msc = (1 + X) ** 2 / (xc * xc + 1 + X)
        y0 = [-(1 + X) / xc, msc - 1.0]
        with np.errstate(all="ignore"):
            sol = solve_ivp(f, (math.log(xc), math.log(XMIN)), y0, method="DOP853", rtol=1e-10, atol=1e-13, dense_output=dense)
        if not sol.success: return np.nan, sol
        return sol.y[1, -1], sol
    return shoot


def capped_profile(m, X, sig=1.0, n_out=4000, xc_prev=None, n_scan=41):
    """Self-consistent capped profile on the branch continuous from m = 0 (AMENDMENT A1): the root of kappa(XMIN) = 0 in x_c
    nearest the previous branch point xc_prev (default: the dust-free x_t), searched in [0.5, 1] xc_prev (sig +1) or
    [1, 2] xc_prev (sig -1). No root there = the branch has folded: ok False. Also counts every root on [1e-3, 1e3] x_t."""
    xt = math.sqrt(X * (X + 1))
    if m <= 0.0:
        x = np.geomspace(XMIN, xt, n_out); C = -(1 + X) / xt - phi_law(xt)
        ell = 0.5 + np.sqrt(0.25 + x * x)
        return dict(ok=True, x=x, phi=phi_law(x, C), kap=np.zeros_like(x), ell=ell, dell=x / np.sqrt(0.25 + x * x), xc=xt, C=C)
    shoot = _shoot_fn(m, X, sig)
    xp = xt if xc_prev is None else xc_prev
    lo, hi = (0.5 * xp, xp * (1 + 1e-9)) if sig > 0 else (xp * (1 - 1e-9), 2.0 * xp)
    grid = np.geomspace(lo, hi, n_scan); vals = np.array([shoot(z)[0] for z in grid])
    br = [(grid[i], grid[i + 1]) for i in range(len(grid) - 1) if np.isfinite(vals[i]) and np.isfinite(vals[i + 1]) and vals[i] * vals[i + 1] <= 0]
    if not br:
        return dict(ok=False, reason="branch folded: no capped state continuous from m = 0", xc=np.nan)
    a, b = (max(br) if sig > 0 else min(br))           # nearest the previous point (largest bracket below it / smallest above)
    xc = brentq(lambda z: shoot(z)[0], a, b, xtol=1e-12 * xt, rtol=1e-12, maxiter=200)
    v, sol = shoot(xc, dense=True)
    x = np.geomspace(XMIN, xc, n_out); y = sol.sol(np.log(x)); phi, kap = y[0], y[1]
    ms = 1.0 + kap; ell = ell_of(ms, x)
    am = np.abs(ms); S = np.sqrt(0.25 * am * am + am * x * x); kp = -sig * m * m * x * x * phi
    dell = kp * (0.5 + (0.5 * am + x * x) / (2 * S)) + np.sign(ms) * am * x / S
    return dict(ok=True, x=x, phi=phi, kap=kap, ell=ell, dell=dell, xc=xc, resid=float(v),
                phi_neg=bool(np.all(phi < 0)), kap_mono=bool(np.all(np.diff(kap) * sig >= -1e-12)))


def count_roots(m, X, sig=1.0, n_scan=241):
    """every root of kappa(XMIN) = 0 on [1e-3, 1e3] x_t (reported: the other branches)."""
    xt = math.sqrt(X * (X + 1)); shoot = _shoot_fn(m, X, sig)
    grid = np.geomspace(1e-3 * xt, 1e3 * xt, n_scan); vals = np.array([shoot(z)[0] for z in grid])
    return int(sum(1 for i in range(len(grid) - 1) if np.isfinite(vals[i]) and np.isfinite(vals[i + 1]) and vals[i] * vals[i + 1] <= 0))


def capped_branch(ms, X, sig=1.0, n_out=4000):
    """profiles along ascending m by continuation from m = 0 (A1). Returns list aligned with ms (ok False after the fold)."""
    out = []; xp = math.sqrt(X * (X + 1)); dead = False; mprev = 0.0
    for m in ms:
        if dead: out.append(dict(ok=False, reason="beyond the fold", xc=np.nan)); continue
        # sub-steps so the continuation never jumps more than 0.05 dex in m
        steps = [m] if mprev <= 0 else list(np.geomspace(mprev, m, max(2, int(math.ceil(math.log10(m / mprev) / 0.05)) + 1))[1:])
        if mprev <= 0 and m > 1e-4:
            steps = list(np.geomspace(1e-4, m, max(2, int(math.ceil(math.log10(m / 1e-4) / 0.05)) + 1)))
        p = None
        for mm in steps:
            p = capped_profile(mm, X, sig, n_out=n_out, xc_prev=xp)
            if not p["ok"]: break
            xp = p["xc"]
        if not p["ok"]:
            dead = True; out.append(p); continue
        out.append(p); mprev = m
    return out


def lam_max(m):
    """S4 / VSZ zero point lambda_max(mu_K, r_M) = (2/3)(1 - ln(3 sqrt2 / (mu_K r_M)))."""
    return (2.0 / 3.0) * (1.0 - math.log(3.0 * math.sqrt(2.0) / m))


def uncapped_profile(m, x3, xend, sig=1.0, n_out=None):
    """Law with no end + dust; S4's zero point at x3 = 3 Mpc / r_M; integrated outward to xend = 30 Mpc / r_M (M_L constant beyond)."""
    lam = lam_max(m) if m > 0 else 0.0
    C = (-1.0 / x3 + lam + math.log(x3)) - phi_law(x3)
    if n_out is None:
        n_out = int(min(400000, max(6000, 40 * m * xend + 4000)))
    if m <= 0.0:
        x = np.geomspace(XMIN, xend, n_out); ell = 0.5 + np.sqrt(0.25 + x * x)
        return dict(ok=True, x=x, phi=phi_law(x, C), kap=np.zeros_like(x), ell=ell, dell=x / np.sqrt(0.25 + x * x), xc=xend, C=C)
    f = _rhs(sig, m)
    x0 = XMIN; y0 = [float(phi_law(x0, C)), -sig * m * m * x0 * x0 * 0.5 * (-1.0)]   # kappa(x0) ~ sig m^2 x0^2 / 2 (phi ~ -1/x)
    y0[1] = sig * m * m * x0 * x0 / 2.0
    # log grid inside 1/m, linear-ish (fine) beyond so the oscillation is resolved
    xa = np.geomspace(x0, min(xend, 0.5 / m), n_out // 4)
    xb = np.linspace(xa[-1], xend, max(2, n_out - len(xa)))[1:] if xend > xa[-1] else np.array([])
    x = np.concatenate([xa, xb])
    sol = solve_ivp(f, (math.log(x0), math.log(xend)), y0, method="DOP853", rtol=1e-10, atol=1e-12, t_eval=np.log(x),
                    max_step=0.02 if m * xend < 1 else min(0.02, 0.3 / (m * xend)))
    if not sol.success:
        return dict(ok=False, reason=sol.message)
    phi, kap = sol.y[0], sol.y[1]; ms = 1.0 + kap; ell = ell_of(ms, x)
    am = np.abs(ms); S = np.sqrt(0.25 * am * am + am * x * x); kp = -sig * m * m * x * x * phi
    dell = kp * (0.5 + (0.5 * am + x * x) / (2 * np.maximum(S, 1e-300))) + np.sign(ms) * am * x / np.maximum(S, 1e-300)
    return dict(ok=True, x=x, phi=phi, kap=kap, ell=ell, dell=dell, xc=xend, C=C, lam=lam)


def dsig_profile(u, prof, nt=6001, chunk=120):
    """DeltaSigma (units M_b / r_M^2) at projected u of a spherical profile: baryon point + extended dM/dx = dell up to xc, then
    nothing (a point of mass ell(xc) beyond). Same cosh substitution as ONE1's dsig. Vectorised over u in chunks (memory)."""
    u = np.asarray(u, float); xc = prof["xc"]; lx = np.log(prof["x"]); out = np.empty(len(u))
    ellc = float(prof["ell"][-1]); far = u >= xc
    out[far] = ellc / (math.pi * u[far] ** 2)
    idx = np.where(~far)[0]; s = np.linspace(0.0, 1.0, nt)
    for c0 in range(0, len(idx), chunk):
        ii = idx[c0:c0 + chunk]; ui = u[ii]
        T = np.arccosh(xc / ui); t = T[:, None] * s[None, :]; xx = ui[:, None] * np.cosh(t)
        dm = np.interp(np.log(xx), lx, prof["dell"])
        Sig = np.trapz(dm / np.cosh(t), s, axis=1) * T / (2 * math.pi * ui)
        Mc = np.interp(np.log(ui), lx, prof["ell"]) + ui * np.trapz(dm * np.tanh(t) * np.exp(-t), s, axis=1) * T
        out[ii] = Mc / (math.pi * ui * ui) - Sig
    return out


def enclosed_dust_direct(prof, m, sig=1.0):
    """kappa(x) by direct trapezoid of -sig m^2 x^2 phi on the profile's own phi (KA5)."""
    x, phi = prof["x"], prof["phi"]; integ = -sig * m * m * x * x * phi
    return np.concatenate([[prof["kap"][0]], prof["kap"][0] + np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(x))])


def deep_dust_closed(r, rc, phic_abs, s, mu):
    """Deep-law test field Phi = -(|Phi_c| + s ln(rc/r)): M_K(<r) G / mu^2 = |Phi_c| r^3/3 + s (r^3/3 ln(rc/r) + r^3/9) (Lean MK1)."""
    return (phic_abs * r ** 3 / 3.0 + s * (r ** 3 / 3.0 * np.log(rc / r) + r ** 3 / 9.0))


# ------------------------------------------------------------------ neighbour kernel, generalised from ONE1's sigma_ph / build_H
NW = 641; NTH = 96
_TH, _WTH = np.polynomial.legendre.leggauss(NTH); _TH = (_TH + 1) * math.pi / 2; _WTH = _WTH * math.pi / 2


def sigma_ext(prof, X, n_log=2000, n_lin=6000, chunk=800):
    """extended-charge-only surface density in units of r_c (= xc r_M), normalised to unit mass; ONE1's sigma_ph with dell."""
    xc = prof["xc"]; lx = np.log(prof["x"])
    s_rm = np.unique(np.concatenate([np.geomspace(1e-6 * xc, 0.05 * xc, n_log), np.linspace(0.05 * xc, xc, n_lin)]))
    Sg = np.zeros(len(s_rm)); idx = np.where(s_rm < xc)[0]; ss = np.linspace(0.0, 1.0, 1501)
    for c0 in range(0, len(idx), chunk):
        ii = idx[c0:c0 + chunk]; si = s_rm[ii]; T = np.arccosh(xc / si)
        t = T[:, None] * ss[None, :]; xx = si[:, None] * np.cosh(t)
        dm = np.interp(np.log(xx), lx, prof["dell"])
        Sg[ii] = np.trapz(dm / np.cosh(t), ss, axis=1) * T / (2 * math.pi * si)
    s = np.concatenate([[0.0], s_rm / xc]); S = np.concatenate([[Sg[0]], Sg * xc * xc])
    dM = 2 * math.pi * s * S; Mc = np.concatenate([[0.0], np.cumsum(0.5 * (dM[1:] + dM[:-1]) * np.diff(s))]); tot = Mc[-1]
    return s, S / tot, Mc / tot, tot / X


def Qfun(rho, dl, s, S, Mc):
    """ONE1's Qfun (unit extended mass inside a disc of radius rho centred dl from the halo's centre), verbatim logic."""
    base = np.where(rho > dl, np.interp(np.minimum(rho - dl, 1.0), s, Mc), 0.0)
    slo = np.abs(rho - dl); shi = np.minimum(rho + dl, 1.0); act = slo < shi
    out = base.copy()
    if act.any():
        a, b = slo[act][:, None], shi[act][:, None]; ss = a + (b - a) * (1 - np.cos(_TH[None, :])) / 2; jac = (b - a) * np.sin(_TH[None, :]) / 2
        r_, d_ = rho[act][:, None], dl[act][:, None] if np.ndim(dl) else dl
        with np.errstate(divide="ignore", invalid="ignore"):
            cosa = (ss * ss + d_ * d_ - r_ * r_) / (2 * ss * d_)
        al = np.arccos(np.clip(cosa, -1.0, 1.0)); Si = np.interp(ss, s, S)
        out[act] += (al * 2 * ss * Si * jac * _WTH[None, :]).sum(1)
    return out


def build_H_prof(prof, X, nd=480):
    """ONE1's build_H with the extended profile of prof (units of its own end radius r_c)."""
    s, S, Mc, norm = sigma_ext(prof, X); w = np.linspace(0.0, 1.0, NW); DG = np.geomspace(1e-4, 300.0, nd)
    HL = np.zeros((nd, NW)); HU = np.zeros((nd, NW)); CC = np.zeros(nd)
    for i, dl in enumerate(DG):
        lo = max(0.0, dl - 1.0); rl = lo + w * (dl - lo); ru = dl + w
        rho = np.concatenate([rl, ru[1:]]); q = Qfun(rho, np.full(rho.size, dl), s, S, Mc)
        with np.errstate(divide="ignore", invalid="ignore"):
            integ = np.where(rho > 0, q / rho, 0.0)
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(rho))])
        H = 2 * cum - q; HL[i] = H[:NW]; HU[i] = H[NW - 1:] - 2 * np.log1p(ru); CC[i] = H[-1] - 2 * math.log(dl + 1) + 1
    return dict(X=X, DG=DG, LD=np.log(DG), HL=HL, HU=HU, CC=CC, fb=1.0 / (1 + X), norm=norm, xc=prof["xc"])


def H_eval_multi(rho, dl, TS, ti):
    """ONE1's H_eval with a per-element table index ti into the stacked tables TS (HL, HU, CC: (nT, nd, NW)); shared DG grid."""
    fb = TS["fb"]; dl = np.maximum(dl, 1e-12); LD = TS["LD"]
    Hpm = np.where(rho > dl, 2 * np.log(np.maximum(rho, 1e-300) / dl) - 1.0, 0.0)
    ld = np.clip(np.log(dl), LD[0], LD[-1]); fi = (ld - LD[0]) / (LD[1] - LD[0])
    i = np.clip(np.floor(fi).astype(np.int64), 0, len(LD) - 2); a = fi - i
    lo = np.maximum(0.0, dl - 1.0); above = rho >= dl + 1.0; below = rho <= lo; upper = (rho >= dl) & ~above
    with np.errstate(divide="ignore", invalid="ignore"):
        wl = np.clip(np.where(dl > lo, (rho - lo) / (dl - lo), 0.0), 0.0, 1.0)
    wu = np.clip(rho - dl, 0.0, 1.0)
    ww = np.where(upper, wu, wl) * (NW - 1); j = np.clip(np.floor(ww).astype(np.int64), 0, NW - 2); b = ww - j
    HL, HU, CC = TS["HL"], TS["HU"], TS["CC"]
    def row(ii):
        hl = (1 - b) * HL[ti, ii, j] + b * HL[ti, ii, j + 1]; hu = (1 - b) * HU[ti, ii, j] + b * HU[ti, ii, j + 1]
        return np.where(upper, hu, hl)
    hmid = (1 - a) * row(i) + a * row(i + 1) + np.where(upper, 2 * np.log1p(np.maximum(rho, 0.0)), 0.0)
    cc = (1 - a) * CC[ti, i] + a * CC[ti, i + 1]
    Hph = np.where(above, cc + 2 * np.log(np.maximum(rho, 1e-300)) - 1.0, np.where(below & (dl >= 1.0), 0.0, hmid))
    return fb * Hpm + (1 - fb) * Hph


NOTE = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
