#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG172D_solver -- V0's static spherical field equations (CV1, S = 1) with a varying gate f(r), the theta equation of 11C-d, and the
DE12 layer construction (re-implemented copy).  Units for the radial solves: kpc, km/s, Msun.  All physics is stated in the docstrings;
nothing is tuned.  Imported by A2..A5.
"""
import math
import numpy as np
from scipy.linalg import solve_banded
import CFG172D_common as C

G = C.G                      # kpc (km/s)^2 / Msun
CKMS = C.C_KMS
KPC3_OVER_MS = C.KPC**3 / C.MS      # SI kg/m^3 -> Msun/kpc^3 factor
RHO_L_KPC = C.RHO_L * KPC3_OVER_MS  # rho_Lambda in Msun/kpc^3
H0_KPC = C.H0 * C.KPC / 1e3        # H0 in km/s/kpc (SI s^-1 * m/kpc ... /1e3)
THETA_L_KPC = 3 * math.sqrt(C.OL) * H0_KPC / CKMS          # theta_Lambda in 1/kpc (= sqrt(3 Lambda))


def Hz_kpc(z):
    return H0_KPC * math.sqrt(C.Om * (1 + z)**3 + C.OL)     # km/s/kpc


def theta_bar_kpc(z):
    return 3 * Hz_kpc(z) / CKMS


def make_grid(rmin=0.02, rmax=3.0e4, n=3000):
    r = np.geomspace(rmin, rmax, n)
    return r


def exp_sphere_rho(r, Mb, h=2.0):
    return Mb * np.exp(-r / h) / (8 * math.pi * h**3)


def exp_sphere_Menc(r, Mb, h=2.0):
    s = r / h
    return Mb * (1 - (1 + s + s**2 / 2) * np.exp(-s))


def solve_v0(r, f, a0, Mb, profile="point", m=1 / 100.0, sigma=1.0, h=2.0):
    """V0 static spherical system, S = 1, no dark component, background contrast neglected:
         (r^2 w')'/r^2 - M^2 w = 4 pi G f rho_b ,  M^2 = m^2 (1 - f)
         (r^2 P')'/r^2 - M^2 P = (r^2 f (nu-1) w')'/r^2 + sigma M^2 w ,   nu = nu_mono(|w'|/a0)
         Phi' = u' + (f P)' ,  u' = G M_b(<r)/r^2 ,  psi = 2 P is the multiplier Psi.
       returns dict(w, wp, P, gbar, gN, Menc, nu, Psi, Ssrc)  (potentials in (km/s)^2, gradients in (km/s)^2/kpc)."""
    n = len(r); s = np.log(r); ds = s[1] - s[0]
    rh = np.sqrt(r[:-1] * r[1:])
    if profile == "point":
        rho = np.zeros(n); Menc = np.full(n, Mb)
    else:
        rho = exp_sphere_rho(r, Mb, h); Menc = exp_sphere_Menc(r, Mb, h)
    M2 = m**2 * (1 - f)
    # ---- w equation:  d/ds(r w_s) - M2 r^3 w = ds-weighted source
    src = 4 * math.pi * G * f * rho * r**3
    Fin = G * f[0] * Menc[0]                                          # r^2 w' at the inner boundary (gated enclosed mass)
    nn = n - 1                                                        # unknowns w_0 .. w_{n-2};  w_{n-1} = 0
    ab = np.zeros((3, nn))
    a = rh / ds                                                       # flux coefficients at i+1/2
    diag = -(a[:nn] + np.concatenate([[0.0], a[:nn - 1]])) - M2[:nn] * r[:nn]**3 * ds
    up = a[:nn - 1]; lo = a[:nn - 1]
    ab[1, :] = diag; ab[0, 1:] = up; ab[2, :-1] = lo
    rhs = ds * src[:nn]
    rhs[0] += Fin                                                      # F_{-1/2} = Fin moves to the RHS with sign: F_0 - Fin - ... = ds*src
    w = np.zeros(n)
    w[:nn] = solve_banded((1, 1), ab, rhs)
    wp = np.empty(n); wp[1:-1] = (w[2:] - w[:-2]) / (r[2:] - r[:-2]); wp[0] = Fin / r[0]**2; wp[-1] = wp[-2]
    # a cleaner w' at half nodes for nu
    wph = (w[1:] - w[:-1]) / (rh * ds)
    nu_h = C.nu_mono(np.maximum(np.abs(wph), 1e-30) / a0)
    fh = 0.5 * (f[1:] + f[:-1])
    # ---- P equation:  F_i - F_{i-1} = M2 r^3 ds (P + sigma w),  F_i = a_i (P_{i+1}-P_i) - a_i fh (nu-1)(w_{i+1}-w_i)
    Pd = np.zeros(n)
    dfl = a * fh * (nu_h - 1) * (w[1:] - w[:-1])                       # the flux part from the kernel at i+1/2
    ab2 = np.zeros((3, nn))
    ab2[1, :] = diag; ab2[0, 1:] = up; ab2[2, :-1] = lo
    rhs2 = M2[:nn] * r[:nn]**3 * ds * sigma * w[:nn] + (dfl[:nn] - np.concatenate([[0.0], dfl[:nn - 1]]))
    # F_i - F_{i-1} = a_i P_{i+1} - (a_i + a_{i-1}) P_i + a_{i-1} P_{i-1}  - (dfl_i - dfl_{i-1});  equation: that = M2 r^3 ds (P + sigma w)
    # ab2 diag already carries -(a_i + a_{i-1}) - M2 r^3 ds ; move the sigma w term and the kernel flux to the RHS
    P = np.zeros(n)
    P[:nn] = solve_banded((1, 1), ab2, rhs2)
    Ph = P[:]
    fP = f * P
    fPp = np.gradient(fP, r)
    uN = G * Menc / r**2
    gbar = uN + fPp
    Psi = 2 * P
    Ssrc = 4 * math.pi * G * rho
    return dict(r=r, w=w, wp=wp, wph=wph, P=P, fPp=fPp, gbar=gbar, gN=uN, Menc=Menc, nu_h=nu_h, Psi=Psi, Ssrc=Ssrc, M2=M2, rho=rho)


def Bcal_NR(sol, a0, m=1 / 100.0, sigma=1.0):
    """B = dL/df (velocity^4/length^2 units, the NR brace coefficient):  a0^2 q + Psi (m^2 w - lap(u-v)) + sigma m^2 w^2  (O3c derived it)."""
    y = np.maximum(np.abs(sol["wp"]), 1e-30) / a0
    q = np.interp(np.log10(y), C.LYG, C.QG)
    return a0**2 * q + sol["Psi"] * (m**2 * sol["w"] - sol["Ssrc"]) + sigma * m**2 * sol["w"]**2, a0**2 * q


def Bbrace(sol, a0, m=1 / 100.0, sigma=1.0):
    """B in the covariant brace's units (1/kpc^2): 2 B_NR / c^4."""
    B_nr, Bq = Bcal_NR(sol, a0, m, sigma)
    return 2 * B_nr / CKMS**4, 2 * Bq / CKMS**4


# ------------------------------------------------------------------------------------------------ the theta equation (local, algebraic)
def gate_from_y(y, z, w, xc0=2.5, p=1, variant="even", zscale=True):
    """f(y), df/dy, d2f/dy2 with y = theta/thetabar;  u = D(y) E^(-2p) (frozen definition, 'even') or the monotone sensitivity variant."""
    E2z = C.E2(z)
    y = np.asarray(y, float)
    if variant == "mono":
        pos = y > 1e-12
        yy = np.where(pos, y, 1.0)
        D = np.where(pos, 1 / yy**2 - 1, 1e30)
        dD = np.where(pos, -2 / yy**3, 0.0); d2D = np.where(pos, 6 / yy**4, 0.0)
    else:
        y2 = y**2 + 1e-300
        D = 1 / y2 - 1; dD = -2 * y / y2**2 if False else -2 / (np.where(np.abs(y) > 1e-150, y, 1e-150))**3
        d2D = 6 / (np.where(np.abs(y) > 1e-150, y, 1e-150))**4
    sc = E2z**(-p) if zscale else 1.0
    u = D * sc; u_y = dD * sc; u_yy = d2D * sc
    t = (np.minimum(u, 1e30) / xc0 - 1.0) / (2 * w) + 0.5
    tu = 1.0 / (2 * w * xc0)
    Wv, W1, W2 = C.Wd(t)
    f = Wv
    f_y = W1 * tu * u_y
    f_yy = W2 * tu**2 * u_y**2 + W1 * tu * u_yy
    return f, f_y, f_yy, t, u


def hfun(vth, kind):
    """coupling function h(vartheta) and h', h''"""
    if kind == "lin":
        return vth, np.ones_like(vth), np.zeros_like(vth)
    a = 1 + np.abs(vth)
    return vth / a, 1 / a**2, -2 * np.sign(vth) / a**3


def theta_root(z, w, c2, Bb, rho_contrast, zeta, kind="lin", variant="even", ND=6000, branch="first"):
    """Continuation root y* = theta/thetabar of  Pi = -2 c2 thetabar^2 (y-1) + Bb f_y(y) - S_hat h'(vth) = 0,
       S_hat = (16 pi G rho_c / c^2) zeta thetabar / theta_L,  vth = (thetabar/theta_L)(y - 1),  taking the FIRST root below y = 1
       (the branch continuous with the background).  Also returns the number of sign changes of Pi in y (S-curve detector)."""
    tb = theta_bar_kpc(z)
    S0 = 16 * math.pi * G * rho_contrast / CKMS**2 * zeta * tb / THETA_L_KPC
    n = len(rho_contrast)
    dl = np.concatenate([[0.0], np.geomspace(1e-12, 1e8, ND)])                          # delta = 1 - y
    y = 1 - dl
    f, fy, fyy, t, u = gate_from_y(y, z, w, variant=variant)
    vth = (tb / THETA_L_KPC) * (y - 1)
    hv, h1, h2 = hfun(vth, kind)
    ystar = np.ones(n); nroots = np.zeros(n, int)
    if branch == "upper":
        # d1 alternative (S-curve) branch: the LAST up-crossing of G (stable root) when the gate term makes G dip below zero; trivial root y = 1 otherwise
        G_ = 2 * c2 * tb**2 * dl[None, :] + Bb[:, None] * fy[None, :] - S0[:, None] * h1[None, :]
        G_ = G_[:, 1:]                                        # drop delta = 0
        sg = np.sign(G_)
        up = (sg[:, 1:] > 0) & (sg[:, :-1] < 0)
        nroots[:] = ((sg[:, 1:] * sg[:, :-1]) < 0).sum(axis=1)
        has = up.any(axis=1)
        jl = up.shape[1] - 1 - np.argmax(up[:, ::-1], axis=1)    # last up-crossing
        rows = np.arange(n)
        g0 = G_[rows, jl]; g1 = G_[rows, jl + 1]
        yy = y[1:][jl] + (y[1:][jl + 1] - y[1:][jl]) * (-g0 / (g1 - g0 + 1e-300))
        ystar = np.where(has, yy, 1.0)
        return ystar, nroots
    act = np.where(S0 > 0)[0]
    if len(act):
        G_ = 2 * c2 * tb**2 * dl[None, :] + Bb[act, None] * fy[None, :] - S0[act, None] * h1[None, :]
        sg = np.sign(G_)
        chg = (sg[:, 1:] * sg[:, :-1] < 0)
        nroots[act] = chg.sum(axis=1)
        has = chg.any(axis=1)
        j = np.argmax(chg, axis=1)
        rows = np.arange(len(act))
        g0 = G_[rows, j]; g1 = G_[rows, j + 1]
        yy = y[j] + (y[j + 1] - y[j]) * (-g0 / (g1 - g0 + 1e-300))
        ystar[act] = np.where(has, yy, y[-1])
    return ystar, nroots


# ------------------------------------------------------------------------------------------------ the DE12 layer (re-implemented copy)
def de12_transition(z, Mb, foot, w, amp=True):
    """Copy of DE12's transition() (real_research/dark_energy_2026/DE12_mond_sector_gate_stiffness.py), SI units, V0's ORIGINAL gate
    (MS2's door: reading A+, density and phantom).  Used for control C4 (reproduce DE12) and MUTATE M1 (restore the original gate)."""
    a0 = C.A0_L[foot]; H = C.Hz(z); xce = 2.5 * C.E2(z)
    rho_bar = C.Om * C.rho_crit0 * (1 + z)**3
    hs = C.host(Mb, z)
    r = np.geomspace(1.0, 2e4, 20000) * C.KPC
    y = C.G_SI * Mb * C.MS / (r**2 * a0)
    rho_ph = Mb * C.MS * (C.h_of(y) - y * C.dh_of(y)) / (2 * math.pi * r**3 * y)
    rho_nfw = hs["rho_s"] / ((r / hs["rs"]) * (1 + r / hs["rs"])**2)
    rho_b = C.FB * (rho_nfw + rho_bar)
    xms = 4 * math.pi * C.G_SI * (rho_b + rho_ph - C.FB * rho_bar) / H**2
    gN = C.G_SI * Mb * C.MS / r**2; g = C.nu_of(y) * gN
    U = xms / xce
    t = (U - 1) / (2 * w) + 0.5
    _, W1, W2 = C.Wd(t)
    tU = 1 / (2 * w)
    B = a0**2 * C.q_of(y) / (8 * math.pi * C.G_SI)
    A_perp = C.nu_of(y) if amp else np.ones_like(y)
    A_par = (C.nu_of(y) + C.ynup_of(y)) if amp else np.ones_like(y)
    Umax = 4 * math.pi * C.G_SI / (H**2 * xce)
    out = {"r": r, "t": t, "rho_b": rho_b, "B": B, "g": g, "y": y, "H": H, "xce": xce, "rho_ph": rho_ph, "rho_nfw": rho_nfw, "rho_bar": rho_bar, "hs": hs}
    S = {}
    for lab, A in (("perp", A_perp), ("par", A_par)):
        Urho = Umax * A
        S[lab] = B * (W2 * tU**2 * Urho**2)
    out["c_gate2"] = {lab: rho_b * np.maximum(S[lab], 0.0) for lab in S}
    out["W1"], out["W2"] = W1, W2
    return out


def de12_cell(z, Mb, foot, w, amp=True):
    tr = de12_transition(z, Mb, foot, w, amp)
    m = (tr["t"] > 0) & (tr["t"] < 1)
    if not m.any():
        return None
    cg = np.sqrt(np.maximum(tr["c_gate2"]["perp"], tr["c_gate2"]["par"]))
    cmax = float(np.max(cg[m]))
    k1 = 1 / C.KPC
    gam = k1 * math.sqrt(max(cmax**2 - C.CS["1e6K"]**2, 0.0))
    r_e = float(np.interp(0.5, tr["t"][::-1], tr["r"][::-1])) / C.KPC
    return dict(c_gate_max=cmax, Gamma_over_H=gam / tr["H"], r_edge_kpc=r_e)
