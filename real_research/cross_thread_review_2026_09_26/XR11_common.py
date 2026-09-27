#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR11_common -- the machinery XR11's two lanes share (imported, never run on its own).

  * L352's constants and its monotone-repaired RAR kernel, and DE12's constants, hosts, C-infinity gate and transition(),
    REIMPLEMENTED here (not exec'd from their scripts); XR11_dark_channel_gate.py's C1 checks this copy against DE12's
    committed numbers (24 layers + the A = 1 control, 0e+00).
  * transition12(z, M_b, footing, w, amp, g): DE12's uncapped transition with an optional weight g on the MOND-sector
    reading (g = 1 is DE12's).
  * dark_layer(...): the gate reading the dark fluid (XR11 reading A): its first variation dV = -B V'(rho) and its
    anti-stiffness c_gate,d^2 = rho B V''(rho), with V(rho) = W(t(U(rho))).
  * jeans_sigma, v_esc, menc_nfw: the host carrier's isotropic Jeans dispersion (untruncated NFW), Newtonian escape speed.
"""
import math
import numpy as np
from scipy.optimize import brentq

# ---------------------------------------------------------------------------------- L352's constants and kernel (reimplemented)
c_l = 2.99792458e8; Mpc = 3.0856775814913673e22; G = 6.67430e-11
h = 0.6736; om_b, om_c = 0.02237, 0.1200; T_CMB = 2.7255; N_eff = 3.046
H0 = 100 * h * 1e3 / Mpc; rho_crit0 = 3 * H0 ** 2 / (8 * math.pi * G)
Og = (4 * 5.670374419e-8 * T_CMB ** 4 / c_l ** 3) / rho_crit0; Or = Og * (1 + N_eff * (7 / 8) * (4 / 11) ** (4 / 3))
Ob, Oc = om_b / h ** 2, om_c / h ** 2; Om = Ob + Oc; OL = 1 - Om - Or
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}


def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"): return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def dh_rar(y, e=1e-6): return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)


YP = brentq(lambda y: float(dh_rar(y)), 1, 5); HP = float(h_rar(YP))
LYG = np.linspace(-14, 14, 280001); YG = 10 ** LYG; DH = np.maximum(dh_rar(YG), 0.05 * HP / (YG + YP))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])
# ---------------------------------------------------------------------------------- DE12's constants (reimplemented)
MS = 1.98892e30; KPC = Mpc / 1e3; KB, MP = 1.380649e-23, 1.67262e-27
FB = 0.02237 / (0.02237 + 0.1200)
E2 = lambda z: 0.3138 * (1 + z) ** 3 + 0.6862                      # L359's gate background
Hz = lambda z: H0 * math.sqrt(Om * (1 + z) ** 3 + OL)
h_of = lambda y: np.interp(np.log10(y), LYG, HM)
dh_of = lambda y: np.interp(np.log10(y), LYG, DH)
QG = 2.0 * ((2.0 / 3.0) * YG[0] ** 1.5 + np.concatenate([[0.0], np.cumsum(0.5 * (HM[1:] + HM[:-1]) * np.diff(YG))]))
q_of = lambda y: np.interp(np.log10(y), LYG, QG)
nu_of = lambda y: 1.0 + h_of(y) / y
ynup_of = lambda y: dh_of(y) - h_of(y) / y
V_CAP = 325e3
CS = {"1e5K": math.sqrt(KB * 1e5 / (0.6 * MP)), "1e6K": math.sqrt(KB * 1e6 / (0.6 * MP))}
HBAR, EV = 1.054571817e-34, 1.602176634e-19
W_M = 0.25; TU = 1 / (2 * W_M)
FOOT = ("canonical", "alt")


def Wd(t):
    t = np.asarray(t, float)
    inside = (t > 0) & (t < 1)
    tt = np.where(inside, t, 0.5)
    ell = np.clip(1 / tt - 1 / (1 - tt), -700, 700)
    W = 1 / (1 + np.exp(ell))
    gq = 1 / tt ** 2 + 1 / (1 - tt) ** 2
    gp = -2 / tt ** 3 + 2 / (1 - tt) ** 3
    W1 = W * (1 - W) * gq
    W2 = W * (1 - W) * ((1 - 2 * W) * gq ** 2 + gp)
    W = np.where(t >= 1, 1.0, np.where(t <= 0, 0.0, W))
    return W, np.where(inside, W1, 0.0), np.where(inside, W2, 0.0)


def host(Mb, z):
    """DE12's host: the NFW of M_b (30% of the cosmic baryons bound for galaxies; all above 1e13), continued past r200."""
    M200 = Mb / (0.3 * FB) if Mb < 1e13 else Mb / FB
    rhoc = rho_crit0 * E2(z) * (Hz(z) / (H0 * math.sqrt(E2(z)))) ** 2
    cc = 10 ** (0.905 - 0.101 * math.log10(M200 / (1e12 / h))) * (1 + z) ** -0.5
    r200 = (3 * M200 * MS / (4 * math.pi * 200 * rhoc)) ** (1 / 3); rs = r200 / cc
    rho_s = M200 * MS / (4 * math.pi * rs ** 3 * (math.log(1 + cc) - cc / (1 + cc)))
    return dict(M200=M200, r200=r200, rs=rs, rho_s=rho_s, c=cc)


def transition12(z, Mb, foot, w, amp=True, g=1.0, r=None):
    """DE12's transition(), uncapped branch (g = 1 is DE12's; g scales the MOND-sector reading: U = g U_MS)."""
    a0 = A0[foot]; H = Hz(z); xce = 2.5 * E2(z)
    rho_bar = Om * rho_crit0 * (1 + z) ** 3
    hs = host(Mb, z)
    r = np.geomspace(1.0, 2e4, 20000) * KPC if r is None else r
    y = G * Mb * MS / (r ** 2 * a0)
    rho_ph = Mb * MS * (h_of(y) - y * dh_of(y)) / (2 * math.pi * r ** 3 * y)
    rho_nfw = hs["rho_s"] / ((r / hs["rs"]) * (1 + r / hs["rs"]) ** 2)
    rho_b = FB * (rho_nfw + rho_bar)
    xms = 4 * math.pi * G * (rho_b + rho_ph - FB * rho_bar) / H ** 2
    U = g * xms / xce
    t = (U - 1) / (2 * w) + 0.5
    _, W1, W2 = Wd(t)
    tU = 1 / (2 * w)
    B = a0 ** 2 * q_of(y) / (8 * math.pi * G)
    Umax = g * 4 * math.pi * G / (H ** 2 * xce)
    c2 = {}
    for lab, A in (("perp", nu_of(y) if amp else np.ones_like(y)), ("par", (nu_of(y) + ynup_of(y)) if amp else np.ones_like(y))):
        S_ = B * (W2 * tU ** 2 * (Umax * A) ** 2)
        c2[lab] = rho_b * np.maximum(S_, 0.0)
    return dict(r=r, t=t, rho_b=rho_b, B=B, y=y, H=H, c_gate2=c2)


def cgate_max12(tr):
    m = (tr["t"] > 0) & (tr["t"] < 1)
    if not m.any(): return None, None
    cg = np.sqrt(np.maximum(tr["c_gate2"]["perp"], tr["c_gate2"]["par"]))
    return float(np.max(cg[m])), float(np.interp(0.5, tr["t"][::-1], tr["r"][::-1]))



# ============================================================================================ the dark channel on real layers
def dark_layer(z, Mb, foot, n=1.0, S=1.0, w=W_M, r=None, ampA=False, absolute=None, rho_c_override=None):
    """the gate reading the dark fluid.  Density door (n > 0, contrast reading): U = (x_d/x_c,eff)^n, x_d = 4 pi G drho/H^2,
    drho = (1 - f_b) S rho_NFW (the carrier's mean is the leaf mean).  Depletion mirror (n < 0, absolute reading, defined
    in voids too): U = (rho_d/rho_ref)^n, rho_ref = rho_c + <rho_d>, so its layer sits where the density door's does.
    The fluid that responds: rho_d = drho + (1 - f_b) rho_bar."""
    absolute = (n < 0) if absolute is None else absolute
    a0 = A0[foot]; H = Hz(z); xce = 2.5 * E2(z)
    rho_bar = Om * rho_crit0 * (1 + z) ** 3
    hs = host(Mb, z)
    r = np.geomspace(1.0, 3e4, 30000) * KPC if r is None else r
    y = G * Mb * MS / (r ** 2 * a0)
    rho_nfw = hs["rho_s"] / ((r / hs["rs"]) * (1 + r / hs["rs"]) ** 2)
    drho = (1 - FB) * S * rho_nfw
    rho_d = drho + (1 - FB) * rho_bar
    rho_c = xce * H ** 2 / (4 * math.pi * G)                          # the vacuum threshold, as a density contrast
    rho_c = rho_c if rho_c_override is None else rho_c_override
    read, ref = (rho_d, rho_c + (1 - FB) * rho_bar) if absolute else (drho, rho_c)
    U = (read / ref) ** n
    t = (U - 1) / (2 * w) + 0.5
    W0, W1, W2 = Wd(t)
    tU = 1 / (2 * w)
    Ur, Urr = n * U / read, n * (n - 1) * U / read ** 2
    A = nu_of(y) if ampA else 1.0
    Ur, Urr = Ur * A, Urr * A ** 2
    B = a0 ** 2 * q_of(y) / (8 * math.pi * G)
    V1 = W1 * tU * Ur
    V2 = W2 * tU ** 2 * Ur ** 2 + W1 * tU * Urr
    return dict(r=r, t=t, W=W0, U=U, y=y, B=B, rho_d=rho_d, drho=drho, rho_c=rho_c, rho_bar_d=(1 - FB) * rho_bar, read=read, ref=ref,
                c2=rho_d * B * V2, dV=-B * V1, V1=V1, V2=V2, H=H, xce=xce, hs=hs, a0=a0, rho_nfw=rho_nfw)


def layer_stats(L_):
    m = (L_["t"] > 0) & (L_["t"] < 1)
    if not m.any(): return None
    i_e = np.where(m)[0]
    tm, rm_ = L_["t"][m], L_["r"][m]
    r_e = float(np.interp(0.5, tm, rm_)) if tm[0] < tm[-1] else float(np.interp(0.5, tm[::-1], rm_[::-1]))
    c2 = L_["c2"][m]
    return dict(r_e=r_e, r_in=float(L_["r"][i_e[0]]), r_out=float(L_["r"][i_e[-1]]), c_max=float(np.sqrt(max(c2.max(), 0.0))),
                dV_max=float(np.max(np.abs(L_["dV"][m]))), dV_sign=float(np.sign(L_["dV"][m][np.argmax(np.abs(L_["dV"][m]))])),
                i_cmax=int(i_e[np.argmax(c2)]))


def menc_nfw(hs, r):
    xx = r / hs["rs"]
    return 4 * math.pi * hs["rho_s"] * hs["rs"] ** 3 * (np.log(1 + xx) - xx / (1 + xx))


def jeans_sigma(z, Mb, r_eval, S=1.0):
    """isotropic Jeans dispersion of the host's carrier (untruncated NFW tracer) in the Newtonian potential of the
    point-mass baryons + the NFW (gas f_b always, carrier (1 - f_b) S): the generous, phase-mixed estimate."""
    hs = host(Mb, z)
    rr = np.geomspace(1e-3 * hs["rs"], 3000 * hs["r200"], 40000)
    rho_t = 1.0 / ((rr / hs["rs"]) * (1 + rr / hs["rs"]) ** 2)
    M = Mb * MS + (FB + (1 - FB) * S) * menc_nfw(hs, rr)
    integ = rho_t * G * M / rr ** 2
    tail = np.concatenate([np.cumsum((0.5 * (integ[1:] + integ[:-1]) * np.diff(rr))[::-1])[::-1], [0.0]])
    return float(np.sqrt(np.interp(r_eval, rr, tail / rho_t)))


def v_esc(z, Mb, r, S_carrier=1.0):
    """Newtonian escape speed to infinity from r: point-mass baryons + the host NFW's gas share f_b and carrier share."""
    hs = host(Mb, z)
    phi = -G * Mb * MS / r - (FB + (1 - FB) * S_carrier) * 4 * math.pi * G * hs["rho_s"] * hs["rs"] ** 3 * math.log(1 + r / hs["rs"]) / r
    return math.sqrt(-2 * phi)


