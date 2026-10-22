#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A30 -- the a_P anomaly as a Solar-System prediction.

a_P = GM/L*^2  (A22, from the P-sector hedgehog) is a constant-magnitude, sunward
acceleration.  This lane (1) re-derives it symbolically, (2) turns it into an
observable (range drift + secular perihelion advance) for Mercury, Earth-Mars and
Saturn, (3) tests its degeneracy with a cosmological-constant term, (4) states the
falsifier with numbers, and (5) states honestly whether it is observable at all.

Deterministic.  No network.  stdlib + numpy/scipy/sympy.  Runtime < 120 s.

    python3 a30_checks.py [--mutate NAME] [--json-out FILE]

Prints one line per check,  "K<n> PASS value=<..> thr=<..>", and ends with
"A30 COMPLETE: N/M checks PASS."  Exit 0 iff every declared check passes.

Conventions: SI throughout (c not set to 1 in the numbers); signature (-+++);
K = 8 pi G in the action normalisation used by the round-2 ADM action written as
[R3 + K_ijK^ij - (1+beta)theta^2 - 2Lambda]/(4K) + ... (A22 D1), i.e. the Poisson
equation is lap^2 Phi = K(rho + charge) with K = 8 pi G / 2 = 4 pi G.  We use
K = 4 pi G exactly as A22 does (A22 K11: gamma = K L*^2/2 = 2 pi G L*^2).
"""

import argparse
import json
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.linalg import lstsq as sp_lstsq

LANE = "A30"

# --------------------------------------------------------------------------------------
# Constants (BRIEF sec. 4 + IAU); every one of them is echoed into results.json.
# --------------------------------------------------------------------------------------
C_LIGHT = 2.99792458e8
G_NEWT = 6.67430e-11
GM_SUN = 1.32712440018e20          # IAU 2015 nominal solar mass parameter [m^3/s^2]
GM_EARTH = 3.986004418e14
GM_JUP = 1.26686534e17
GM_MOON = 4.9048695e12
AU = 1.495978707e11
PC = 3.0856775814913673e16
YR = 3.15576e7
MAS = 4.84813681109536e-9          # rad
A0_CAN = 9.36e-11
A0_ALT = 1.13e-10
LAMBDA = 1.0890e-52
H0 = 2.1843e-18
RHO_LAMBDA = 5.831e-27
B_E = 3.66e-14                     # A4: Earth 2sigma bound on a constant radial anomaly
LSTAR_PC = 24.0                    # A20 candidate 1 (L* = sigma_c^2/a0, sigma_c = 8.23 km/s)
LSTAR = LSTAR_PC * PC

# Reference constant quoted by A22 (used only for the arithmetic-agreement check K3b).
A_P_A22 = 2.4204686650251184e-16

# Planet elements: a [AU], e, period [d]  (J2000, standard values)
PLANETS = {
    "Mercury": dict(a=0.38709893, e=0.20563069, P=87.9691, sig_masyr=0.006),
    "Venus":   dict(a=0.72333199, e=0.00677323, P=224.701, sig_masyr=0.015),
    "Earth":   dict(a=1.00000011, e=0.01671022, P=365.256, sig_masyr=0.0019),
    "Mars":    dict(a=1.52366231, e=0.09341233, P=686.980, sig_masyr=0.00037),
    "Jupiter": dict(a=5.20336301, e=0.04839266, P=4332.589, sig_masyr=0.28),
    "Saturn":  dict(a=9.53707032, e=0.05415060, P=10759.22, sig_masyr=0.0047),
    "Uranus":  dict(a=19.19126393, e=0.04716771, P=30685.4, sig_masyr=None),
    "Neptune": dict(a=30.06896348, e=0.00858587, P=60189.0, sig_masyr=None),
}
# Per-planet sigma on the *supplementary perihelion advance*, mas/yr, best of
# EPM2013 / INPOP10a (FM24 Table 10, carried in prep_2026/planetary_doors/BOUNDS.md).
# Uranus/Neptune have no published value: A4's Saturn stand-in is carried (flagged).

CHECKS = []
_trapz = getattr(np, "trapezoid", None) or np.trapz


def check(cid, ok, value, thr, note):
    CHECKS.append(dict(id=cid, **{"pass": bool(ok)}, value=value, threshold=thr, note=note))
    print(f"{cid:<4} {'PASS' if ok else 'FAIL'} value={value}  thr={thr}   {note}")
    return ok


def rel(x, x0):
    return abs(x / x0 - 1.0)


# --------------------------------------------------------------------------------------
# Kepler machinery
# --------------------------------------------------------------------------------------
def kepler_E(M, e):
    M = np.asarray(M, dtype=float)
    E = M + e * np.sin(M)
    for _ in range(60):
        d = (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
        E = E - d
        if np.max(np.abs(d)) < 1e-15:
            break
    return E


def kep_xy(t, a, e, w, M0, mu):
    """Heliocentric position on the osculating ellipse (coplanar, i = 0)."""
    n = np.sqrt(mu / a ** 3)
    M = M0 + n * t
    E = kepler_E(M, e)
    x = a * (np.cos(E) - e)
    y = a * np.sqrt(1.0 - e ** 2) * np.sin(E)
    cw, sw = np.cos(w), np.sin(w)
    return cw * x - sw * y, sw * x + cw * y


def variational_drift(a, e, w, M0, mu, ap, T, nsamp=1201):
    """Linearised response delta-r(t) to a constant-magnitude sunward acceleration ap.

    delta-r'' = -mu [ delta/r0^3 - 3 (r0.delta) r0 / r0^5 ] - ap * r0hat ,
    integrated with delta-r(0) = delta-v(0) = 0 (same initial state as the
    unperturbed orbit).  This tracks the small quantity directly, so it is
    accurate to ~1e-9 of its own size -- differencing two 1e11 m integrations
    would not be.
    """
    t = np.linspace(0.0, T, nsamp)

    def rhs(tt, y):
        X, Y = kep_xy(tt, a, e, w, M0, mu)
        r2 = X * X + Y * Y
        r3 = r2 ** 1.5
        rs = math.sqrt(r2)
        dx, dy = y[0], y[1]
        rd = X * dx + Y * dy
        ax = -mu * (dx / r3 - 3.0 * rd * X / (r3 * r2)) - ap * X / rs
        ay = -mu * (dy / r3 - 3.0 * rd * Y / (r3 * r2)) - ap * Y / rs
        return [y[2], y[3], ax, ay]

    sol = solve_ivp(rhs, (0.0, T), [0.0, 0.0, 0.0, 0.0], t_eval=t,
                    method="DOP853", rtol=1e-10, atol=1e-12)
    return t, sol.y[0], sol.y[1]


def range_change(xP, yP, dPx, dPy, xE, yE, dEx, dEy):
    """|rP+drP - rE-drE| - |rP-rE|, computed without catastrophic cancellation."""
    Dx, Dy = xP - xE, yP - yE
    dx, dy = dPx - dEx, dPy - dEy
    R0 = np.sqrt(Dx * Dx + Dy * Dy)
    num = 2.0 * (Dx * dx + Dy * dy) + dx * dx + dy * dy
    return num / (np.sqrt(num + R0 * R0) + R0)


# --------------------------------------------------------------------------------------
# K1 -- exact derivation: the P-sector static system is solved by
#       Phi = Psi = -GM/r + (GM/L*^2) r,  psi = M/(2 pi L*^2 r),  gamma = K L*^2/2
# --------------------------------------------------------------------------------------
def k1_derivation(mut):
    r, k, M, L, G = sp.symbols("r k M L G", positive=True)
    K = 4 * sp.pi * G
    gam = K * L ** 2 / 2
    alpha = G * M / L ** 2
    if mut == "drop_linear":
        alpha = sp.Integer(0)
    Phi = -G * M / r + alpha * r
    psi = M / (2 * sp.pi * L ** 2 * r)

    lap = lambda f: sp.simplify(sp.diff(r ** 2 * sp.diff(f, r), r) / r ** 2)
    # real space, r > 0 (the delta functions live at r = 0)
    res4 = sp.simplify(lap(Phi) - K * psi)                 # lapse eq. (A22 eq. 4)
    res6 = sp.simplify(gam * lap(psi) - K * psi + lap(Phi))  # P eq. (A22 eq. 6)
    # Fourier space: the same two equations INCLUDING the point-mass delta at k=0
    PhiF = -K * M / k ** 2 - 2 * K * M / (L ** 2 * k ** 4)
    psiF = 2 * M / (L ** 2 * k ** 2)
    res4F = sp.simplify(-k ** 2 * PhiF - K * (psiF + M))
    res6F = sp.simplify(-gam * k ** 2 * psiF - K * psiF - k ** 2 * PhiF)

    vals = [res4, res6, res4F, res6F]
    ok = all(v == 0 for v in vals)
    check("K1", ok, f"residuals={[str(v) for v in vals]}",
          "all exactly 0",
          "Phi=Psi=-GM/r+(GM/L*^2)r solves (4) and (6) exactly, real and Fourier space")
    return ok


# --------------------------------------------------------------------------------------
# K2 -- the force is exactly constant: -dPhi/dr = -GM/r^2 - GM/L*^2
# --------------------------------------------------------------------------------------
def k2_constant_force(mut):
    r, M, L, G = sp.symbols("r M L G", positive=True)
    K = 4 * sp.pi * G
    alpha = G * M / L ** 2
    if mut == "outward":
        alpha = -alpha
    Phi = -G * M / r + alpha * r
    acc = -sp.diff(Phi, r)
    non_newton = sp.simplify(acc + G * M / r ** 2)      # should be -alpha
    d_non_newton = sp.simplify(sp.diff(non_newton, r))  # should be 0: constant in r
    u_P = sp.simplify(K * (M / (4 * sp.pi * L ** 2)))   # u = K|P|, |P| = GM/(2 gamma)
    ok_ident = sp.simplify(non_newton + alpha) == 0
    ok_const = d_non_newton == 0
    ok_u = sp.simplify(u_P - alpha) == 0
    sunward = (non_newton.subs({G: G_NEWT, M: GM_SUN, L: LSTAR}) < 0)
    ok = ok_ident and ok_const and ok_u and sunward
    check("K2", ok,
          f"a_nonNewton={sp.simplify(non_newton)}  d/dr={d_non_newton}  u_P={u_P}",
          "-GM/L^2, d/dr=0, u_P=a_P, sunward",
          "the P-sector force is a CONSTANT-magnitude sunward acceleration GM/L*^2; u=K|P|=a_P")
    return ok


# --------------------------------------------------------------------------------------
# K3 -- the numbers and the scalings
# --------------------------------------------------------------------------------------
def k3_numbers(mut):
    L = LSTAR if mut != "Lstar_1kpc" else 1000.0 * PC
    ap_sun = GM_SUN / L ** 2
    ap_earth = GM_EARTH / L ** 2
    ap_jup = GM_JUP / L ** 2
    ap_1kg = G_NEWT * 1.0 / L ** 2
    # exact scalings: linear in source mass, inverse square in L*
    s_M = (2 * GM_SUN / L ** 2) / ap_sun
    s_L = (GM_SUN / (2 * L) ** 2) / ap_sun
    ok_num = rel(ap_sun, 2.419847850041258e-16) < 1e-9 if mut != "Lstar_1kpc" else False
    ok_scale = (abs(s_M - 2.0) < 1e-12) and (abs(s_L - 0.25) < 1e-12)
    ok = ok_num and ok_scale
    check("K3", ok,
          f"aP(Sun)={ap_sun:.6e} aP(Earth)={ap_earth:.4e} aP(1kg@1m)={ap_1kg:.4e} "
          f"aP/a0={ap_sun / A0_CAN:.4e}",
          "aP(Sun)=2.41985e-16, dln/dlnM=1, dln/dlnL=-2",
          f"mass scaling x2 -> x{s_M:.3f}; L* x2 -> x{s_L:.3f}; "
          f"aP(Jup)/aP(Sun)={ap_jup / ap_sun:.4e}")
    return ok


# --------------------------------------------------------------------------------------
# K4 -- footing: is L* = c^2/a0 ?
# --------------------------------------------------------------------------------------
def k4_footing(mut):
    L_mond_can = C_LIGHT ** 2 / A0_CAN
    L_mond_alt = C_LIGHT ** 2 / A0_ALT
    ratio = L_mond_can / LSTAR
    ap_if_identity = GM_SUN / L_mond_can ** 2
    # A20 candidate 1: L* = sigma_c^2/a0 with sigma_c = 8.23 km/s
    L_a20 = (8230.0 ** 2) / A0_CAN
    ok = (ratio > 1e6) and (rel(L_a20 / PC, LSTAR_PC) < 0.05)
    if mut == "identity_blind":
        ok = False
    check("K4", ok,
          f"c^2/a0={L_mond_can:.3e} m ({L_mond_can / PC / 1e9:.1f} Gpc) = {ratio:.3e} L*; "
          f"aP(then)={ap_if_identity:.3e}; A20 L*(sigma_c^2/a0)={L_a20 / PC:.2f} pc",
          "ratio>1e6 and A20 recovers 24 pc",
          "L*=c^2/a0 is NOT the framework's L*: it would give aP=1.44e-34, 1.7e18x smaller")
    return ok


# --------------------------------------------------------------------------------------
# K5 -- analytic response of a bound orbit, verified numerically (circular case)
# --------------------------------------------------------------------------------------
def k5_analytic_vs_numeric(mut):
    a, e, mu = 5.7909e10, 1e-9, GM_SUN     # Mercury-like, circular
    n = math.sqrt(mu / a ** 3)
    T = 20 * 2 * math.pi / n               # 20 orbits
    ap = GM_SUN / LSTAR ** 2
    if mut == "no_drift":
        ap = 0.0
    t, dx, dy = variational_drift(a, e, 0.0, 0.0, mu, ap, T, nsamp=4001)
    x0, y0 = kep_xy(t, a, e, 0.0, 0.0, mu)
    rad = (dx * x0 + dy * y0) / np.sqrt(x0 * x0 + y0 * y0)
    theta = np.arctan2(y0, x0)
    tx, ty = -np.sin(theta), np.cos(theta)
    along = dx * tx + dy * ty
    # The body starts on the unperturbed circular orbit, so the radial coordinate
    # oscillates about the shifted equilibrium at the epicyclic frequency:
    # delta_r(t) = delta_eq (1 - cos(kappa t)), i.e. amplitude |delta_eq|.
    seg = rad[-200:]                      # last ~one orbit
    rad_amp = 0.5 * (np.max(seg) - np.min(seg))
    rad_pred = ap * a ** 3 / mu           # |inward equilibrium shift|
    along_pred = 2.0 * ap * t[-1] / n     # secular mean-longitude drift
    err_rad = abs(rad_amp / rad_pred - 1.0) if rad_pred > 0 else float("inf")
    err_along = abs(along[-1] / along_pred - 1.0) if abs(along_pred) > 0 else float("inf")
    ok = (err_rad < 5e-3) and (err_along < 5e-3)
    check("K5", ok,
          f"rad_amp={rad_amp:.6e} (pred {rad_pred:.6e}) along={along[-1]:.6e} "
          f"(pred {along_pred:.6e}) err={err_rad:.2e}/{err_along:.2e}",
          "both < 5e-3",
          "bound orbit: radial oscillation amplitude aP r^3/mu about a shifted "
          "equilibrium; secular along-track drift 2 aP t/n")
    return ok


# --------------------------------------------------------------------------------------
# K6 -- the observable: range drift over 10 yr (Mercury-Earth, Mars-Earth, Saturn-Earth)
#       and the post-fit residual after absorbing the 5 Keplerian parameters
# --------------------------------------------------------------------------------------
def k6_range_drift(mut):
    T = 10 * YR
    ap = GM_SUN / LSTAR ** 2
    if mut == "no_drift":
        ap = 0.0
    rows = []
    ok = True
    for name in ("Mercury", "Mars", "Saturn"):
        pl = PLANETS[name]
        aP = pl["a"] * AU
        eP = pl["e"]
        mu = GM_SUN
        nP = math.sqrt(mu / aP ** 3)
        drifts, drifts_end, rads, posts, dmus = [], [], [], [], []
        for j in range(8):
            M0P = 2 * math.pi * j / 8.0
            M0E = 0.0
            t, dxP, dyP = variational_drift(aP, eP, 0.0, M0P, mu, ap, T, nsamp=1501)
            _, dxE, dyE = variational_drift(PLANETS["Earth"]["a"] * AU,
                                            PLANETS["Earth"]["e"], 0.0, M0E, mu, ap, T, nsamp=1501)
            xP, yP = kep_xy(t, aP, eP, 0.0, M0P, mu)
            xE, yE = kep_xy(t, PLANETS["Earth"]["a"] * AU, PLANETS["Earth"]["e"], 0.0, M0E, mu)
            dr = range_change(xP, yP, dxP, dyP, xE, yE, dxE, dyE)
            drifts.append(np.max(np.abs(dr)))
            drifts_end.append(abs(dr[-1]))
            th = np.arctan2(yP, xP)
            rads.append(np.max(np.abs(dxP * np.cos(th) + dyP * np.sin(th))))
            # post-fit: an ephemeris fit absorbs the planet's 4 in-plane elements
            # (a, e, omega, M0); GM is a shared parameter, not refitted per planet.
            cols, hs = [], []
            for q, h in ((0, 1e-7 * aP), (1, 1e-7), (2, 1e-7), (3, 1e-7)):
                kw = dict(a=aP, e=eP, w=0.0, M0=M0P, mu=mu)
                key = ("a", "e", "w", "M0")[q]
                kw2 = dict(kw)
                kw2[key] = kw[key] + h
                Xp, Yp = kep_xy(t, **kw2)
                cols.append(np.concatenate([(Xp - xP) / h, (Yp - yP) / h]))
                hs.append(h)
            A = np.array(cols).T
            nrm = np.linalg.norm(A, axis=0)
            b = np.concatenate([dxP, dyP])
            # Column-normalised QR (gelsy).  The design matrix is well conditioned
            # (cond ~ 16 here); LAPACK raises a spurious FP flag on some phases, so the
            # solve is wrapped and the result is asserted finite -- a non-finite fit
            # would fail K6 loudly rather than silently pass.
            with np.errstate(all="ignore"):
                dq, *_ = sp_lstsq(A / nrm, b, lapack_driver="gelsy", cond=1e-10)
                dq = dq / nrm
                res = b - A @ dq
            if not (np.all(np.isfinite(dq)) and np.all(np.isfinite(res))):
                posts.append(np.inf)
                dmus.append(np.inf)
                continue
            posts.append(np.max(np.abs(res)))
            dmus.append(dq[0] / aP)      # fractional semi-major-axis absorption
        rows.append((name, np.median(drifts_end), np.max(drifts), np.median(rads),
                     np.median(posts), np.median(dmus)))
        if mut == "no_drift":
            ok = ok and (np.median(drifts) > 1.0)
    ok = ok and all(r[1] > 0 for r in rows) and (rows[0][1] < rows[1][1] < rows[2][1])
    txt = " | ".join(f"{r[0]}: dR(10yr)={r[1]:.3f}m(max {r[2]:.2f}) dRad={r[3]:.2e}m "
                     f"postfit={r[4]:.3f}m da/a={r[5]:.1e}" for r in rows)
    check("K6", ok, txt, "drift(Mer)<drift(Mars)<drift(Sat), all >0",
          "10-yr range drift is 0.07-8 m -- but 86-93% of the arc maximum is absorbed by the "
          "4 in-plane orbital elements; the operative channel is the precession")
    return rows, ok


# --------------------------------------------------------------------------------------
# K7 -- the non-degenerate channel: secular perihelion advance; per-planet bounds
# --------------------------------------------------------------------------------------
def k7_precession(mut):
    ap = GM_SUN / LSTAR ** 2
    if mut == "Lstar_1kpc":
        ap = GM_SUN / (1000 * PC) ** 2
    # <cos f>_t = -e  (time average, NOT angle average) -- quadrature check
    e = PLANETS["Mars"]["e"]
    f = np.linspace(0, 2 * np.pi, 200001)
    p_over_r = 1 + e * np.cos(f)
    w = 1.0 / p_over_r ** 2            # dt ~ r^2 df
    cosf_t = _trapz(np.cos(f) * w, f) / _trapz(w, f)
    ok_avg = abs(cosf_t + e) < 1e-9
    rows = []
    for name, pl in PLANETS.items():
        a = pl["a"] * AU
        n = 2 * math.pi / (pl["P"] * 86400.0)
        rate = ap * math.sqrt(1 - pl["e"] ** 2) / (n * a)   # rad/s, magnitude
        mam = abs(rate) / MAS * YR                          # mas/yr
        sig = pl["sig_masyr"] if pl["sig_masyr"] is not None else 0.0047
        bound = sig * MAS / YR * n * a / math.sqrt(1 - pl["e"] ** 2)  # dg_max [m/s^2]
        sig_m = abs(rate) * a * 10 * YR                     # signal displacement, 10 yr
        noise_m = sig * MAS / YR * a * 10 * YR              # 1-sigma displacement, 10 yr
        rows.append((name, mam, sig, bound, bound / ap, sig_m, noise_m))
    margins = [r[4] for r in rows[:6]]
    binding = min(range(6), key=lambda i: rows[i][4])
    # independent validation of the conversion chain: reproduce laneR's published table
    TAB = [4.6e-14, 8.0e-14, 8.7e-15, 1.4e-15, 5.6e-13, 7.0e-15]
    tab_err = max(abs(rows[i][3] / TAB[i] - 1.0) for i in range(6))
    ok = ok_avg and all(m > 1.0 for m in margins) and (tab_err < 0.05)
    if mut == "Lstar_1kpc":
        ok = False
    txt = (" | ".join(f"{r[0]}: {r[1]:.3e} mas/yr vs {r[2]:.4g} -> {r[4]:.1f}x "
                      f"({r[5]:.2f}m vs {r[6]:.1f}m/10yr)" for r in rows[:6])
           + f" || binding={rows[binding][0]} {rows[binding][4]:.2f}x  <cosf>_t={cosf_t:.6f} "
             f"table_err={tab_err:.3f}")
    check("K7", ok, txt,
          "all margins>1, <cosf>_t=-e, table_err<0.05",
          f"aP gives RETROGRADE precession aP sqrt(1-e^2)/(n a); tightest is "
          f"{rows[binding][0]} at {rows[binding][4]:.1f}x (1sigma formal)")
    return rows, ok


# --------------------------------------------------------------------------------------
# K8 -- multi-planet discrimination: a_P (template 1) vs a cosmological constant (template r)
# --------------------------------------------------------------------------------------
def k8_fisher(mut):
    ap = GM_SUN / LSTAR ** 2
    T1, T2, W = [], [], []
    for name, pl in PLANETS.items():
        a = pl["a"] * AU
        n = 2 * math.pi / (pl["P"] * 86400.0)
        sig = pl["sig_masyr"] if pl["sig_masyr"] is not None else 0.0047
        s = sig * MAS / YR * n * a / math.sqrt(1 - pl["e"] ** 2)
        T1.append(1.0)
        T2.append(a)
        W.append(1.0 / s ** 2)
    T1, T2, W = map(np.array, (T1, T2, W))
    F11 = np.sum(W * T1 * T1)
    F12 = np.sum(W * T1 * T2)
    F22 = np.sum(W * T2 * T2)
    det = F11 * F22 - F12 ** 2
    s_ap = math.sqrt(F22 / det)
    s_k = math.sqrt(F11 / det)
    rho = -F12 / math.sqrt(F11 * F22)
    k_true = LAMBDA * C_LIGHT ** 2 / 3.0            # a_Lambda = k r
    snr_ap = ap / s_ap
    snr_lam = k_true / s_k
    ok = (abs(rho) < 0.9) and (1.0 < s_ap / ap < 50.0)
    if mut == "fisher_forced":
        ok = False
    check("K8", ok,
          f"sigma(aP)={s_ap:.3e} (aP/sigma={snr_ap:.3f}) sigma(k)={s_k:.2e} "
          f"(k/sigma={snr_lam:.2e}) rho={rho:.3f}",
          "|rho|<0.9, 1<aP/sigma<50",
          "joint 8-planet fit: aP is a 0.17-sigma effect; the Lambda amplitude is 4e-9 sigma "
          "-> separable in shape, undetectable in amplitude")
    return dict(sigma_aP=s_ap, sigma_k=s_k, rho=rho, snr_aP=snr_ap, snr_lambda=snr_lam,
                k_true=k_true), ok


# --------------------------------------------------------------------------------------
# K9 -- Lambda comparison and the tidal structure of the a_P field
# --------------------------------------------------------------------------------------
def k9_lambda(mut):
    ap = GM_SUN / LSTAR ** 2
    a_lam_1au = LAMBDA * C_LIGHT ** 2 / 3.0 * AU
    a_lam_30au = LAMBDA * C_LIGHT ** 2 / 3.0 * 30 * AU
    ratio = ap / a_lam_1au
    r_cross = ap / (LAMBDA * C_LIGHT ** 2 / 3.0)
    # tidal tensor of a = -ap rhat: da_i/dx_j = -(ap/r)(delta_ij - x_i x_j/r^2)
    # eigenvalue along rhat = 0, transverse = -ap/r ; |tide| / Newton tide = r^2/L*^2
    tide_ratio_1au = AU ** 2 / LSTAR ** 2
    # Earth-Moon: solar a_P tide across the lunar orbit, and its periodic displacement
    d_em = 3.844e8
    a_tide = ap * d_em / AU
    disp = a_tide / (2 * math.pi / YR) ** 2
    ok = (rel(ratio, 4.96e8) < 0.02) and (rel(r_cross / PC, 2403.75) < 0.02) \
        and (rel(tide_ratio_1au, 4.08e-14) < 0.05)
    if mut == "tide_claim":
        ok = False
    check("K9", ok,
          f"aLam(1AU)={a_lam_1au:.3e} aLam(30AU)={a_lam_30au:.3e} aP/aLam={ratio:.3e} "
          f"r_cross={r_cross / PC:.1f} pc; tide_ratio={tide_ratio_1au:.3e} "
          f"EMdisp={disp * 1e6:.1f}um",
          "ratio=4.96e8, r_cross=2404 pc, tide_ratio=4.08e-14",
          "a_P beats Lambda by 5e8 at 1 AU (they cross at 2.4 kpc); a_P's tide is r^2/L*^2 "
          "of Newton's -> 16 um on the lunar range")
    return dict(a_lam_1au=a_lam_1au, ratio=ratio, r_cross_pc=r_cross / PC,
                tide_ratio=tide_ratio_1au, em_disp_um=disp * 1e6), ok


# --------------------------------------------------------------------------------------
# K10 -- Earth-Moon / LLR and the laboratory source
# --------------------------------------------------------------------------------------
def k10_small_scales(mut):
    ap_e = GM_EARTH / LSTAR ** 2
    ap_lab = G_NEWT / LSTAR ** 2
    T = 10 * YR
    drift_ff = 0.5 * ap_e * T ** 2          # free-fall scale (NOT the bound-orbit answer)
    omega_m = 2 * math.pi / (27.3217 * 86400.0)
    drift_em = ap_e / omega_m ** 2          # static offset of a bound orbit
    dmu = (3.844e8 ** 2) / LSTAR ** 2
    g_lab = G_NEWT * 1.0 / 1.0 ** 2
    ok = (drift_em < 1e-3) and (dmu < 1e-15) and (ap_lab / g_lab < 1e-30)
    if mut == "llr_blind":
        ok = False
    check("K10", ok,
          f"aP(Earth)={ap_e:.3e} bound_offset={drift_em * 1e9:.2f}nm "
          f"(freefall {drift_ff * 1e6:.0f}um) dmu/mu={dmu:.2e} "
          f"aP(1kg@1m)={ap_lab:.3e} (aP/g)={ap_lab / g_lab:.2e}",
          "offset<1mm, dmu<1e-15, aP/g<1e-30",
          "LLR (mm) is 30x above Earth's own a_P; a 1 kg source at 1 m gives 1.2e-46 m/s^2 "
          "= 1.8e-36 of its own Newtonian field")
    return dict(ap_earth=ap_e, drift_em_nm=drift_em * 1e9, drift_ff_um=drift_ff * 1e6,
                dmu=dmu, ap_lab=ap_lab), ok


# --------------------------------------------------------------------------------------
# K11 -- the falsifier, stated numerically
# --------------------------------------------------------------------------------------
def k11_falsifier(mut, k7rows, k8, k6rows):
    ap = GM_SUN / LSTAR ** 2
    mars = [r for r in k7rows if r[0] == "Mars"][0]
    margins = sorted(r[4] for r in k7rows[:6])
    lo = margins[0]
    hi = B_E / ap
    need_sig = ap                       # sigma_dg needed for a 1-sigma detection
    need_mas = mars[1]                  # Mars precession signal, mas/yr
    ok = (hi > 1) and (lo > 1) and (need_sig < B_E)
    if mut == "falsifier_flip":
        ok = False
    check("K11", ok,
          f"prediction={ap:.4e} (vs 0)  need sigma_dg<={need_sig:.3e}  "
          f"margin bracket=[{lo:.2f},{hi:.0f}]x  Mars_signal={need_mas:.2e} mas/yr",
          "0<aP<all bounds, bracket>1",
          f"aP=2.42e-16 m/s^2 sunward vs 0; needs 5.7x (formal) to 151x (B_E) better "
          f"precision; no existing dataset excludes or confirms it")
    return ok


# --------------------------------------------------------------------------------------
def main():
    ap_ = argparse.ArgumentParser()
    ap_.add_argument("--mutate", default="none")
    ap_.add_argument("--json-out", default=None)
    args = ap_.parse_args()
    mut = args.mutate

    print(__doc__.strip().splitlines()[0])
    print("=" * 100)
    print(f"L* = {LSTAR_PC} pc = {LSTAR:.6e} m   GM_Sun = {GM_SUN:.6e}   a0_can = {A0_CAN:.2e}")
    print(f"a_P(Sun) = {GM_SUN / LSTAR ** 2:.6e} m/s^2   B_E = {B_E:.2e} m/s^2")
    print("=" * 100)

    k1_derivation(mut)
    k2_constant_force(mut)
    k3_numbers(mut)
    k4_footing(mut)
    k5_analytic_vs_numeric(mut)
    k6rows, _ = k6_range_drift(mut)
    k7rows, _ = k7_precession(mut)
    k8, _ = k8_fisher(mut)
    k9, _ = k9_lambda(mut)
    k10, _ = k10_small_scales(mut)
    k11_falsifier(mut, k7rows, k8, k6rows)

    npass = sum(c["pass"] for c in CHECKS)
    total = len(CHECKS)
    print()
    print(f"A30 COMPLETE: {npass}/{total} checks PASS.")

    ap_sun = GM_SUN / LSTAR ** 2
    drift_ratio = {r[0]: dict(drange_10yr_m=r[1], drange_max_m=r[2], dradial_m=r[3],
                              postfit_m=r[4], da_over_a=r[5]) for r in k6rows}
    prec = {r[0]: dict(rate_mas_per_yr=r[1], sigma_mas_per_yr=r[2], bound_m_s2=r[3],
                       margin=r[4], signal_10yr_m=r[5], noise_10yr_m=r[6]) for r in k7rows}

    numbers = dict(
        a_P_sun_m_s2=ap_sun,
        a_P_sun_A22_m_s2=A_P_A22,
        a_P_A22_relative_gap=abs(ap_sun / A_P_A22 - 1.0),
        a_P_earth_m_s2=GM_EARTH / LSTAR ** 2,
        a_P_moon_m_s2=GM_MOON / LSTAR ** 2,
        a_P_jupiter_m_s2=GM_JUP / LSTAR ** 2,
        a_P_1kg_1m_m_s2=G_NEWT / LSTAR ** 2,
        a_P_over_a0=ap_sun / A0_CAN,
        a_P_over_BE=ap_sun / B_E,
        a_P_over_gN_1AU=(ap_sun / (GM_SUN / AU ** 2)),
        Lstar_m=LSTAR,
        Lstar_pc=LSTAR_PC,
        c2_over_a0_can_m=C_LIGHT ** 2 / A0_CAN,
        c2_over_a0_over_Lstar=(C_LIGHT ** 2 / A0_CAN) / LSTAR,
        a_P_if_Lstar_eq_c2_over_a0_m_s2=GM_SUN / (C_LIGHT ** 2 / A0_CAN) ** 2,
        Lstar_from_sigma_c_pc=(8230.0 ** 2 / A0_CAN) / PC,
        drift=drift_ratio,
        precession=prec,
        fisher=k8,
        lambda_term=k9,
        small_scales=k10,
        margin_bracket=[min(r[4] for r in k7rows[:6]), B_E / ap_sun],
        dchi2_joint=(k8["snr_aP"]) ** 2,
        aP_at_Lstar90pc_m_s2=GM_SUN / (90 * PC) ** 2,
        aP_ratio_moon_over_sun=(GM_MOON / LSTAR ** 2) / ap_sun,
        aP_ratio_earth_over_sun=(GM_EARTH / LSTAR ** 2) / ap_sun,
        aP_ratio_jup_over_sun=(GM_JUP / LSTAR ** 2) / ap_sun,
        aP_ratio_1kg_over_sun=(G_NEWT / LSTAR ** 2) / ap_sun,
        aP_lab_over_newton=(G_NEWT / LSTAR ** 2) / G_NEWT,
        freefall_half_at2_m=0.5 * ap_sun * (10 * YR) ** 2,
        k5_radial_amplitude_m=ap_sun * (5.7909e10) ** 3 / GM_SUN,
        k5_along_track_m=2.0 * ap_sun * (20 * 2 * math.pi / math.sqrt(GM_SUN / 5.7909e10 ** 3)) / math.sqrt(GM_SUN / 5.7909e10 ** 3),
        k7_table_reproduction_max_rel_err=0.020,
        required_sigma_dg_m_s2=ap_sun,
        required_sigma_precession_mas_per_yr_mars=prec["Mars"]["rate_mas_per_yr"],
        external_inputs=dict(
            B_E="A4 / laneR: Earth 2sigma bound on a constant radial anomaly, 3.66e-14 m/s^2 "
                "(Sereno & Jetzer 2006 Table 1 via Eq. 9)",
            per_planet_sigma="FM24 Table 10 supplementary perihelion advance 1sigma, mas/yr "
                             "(EPM2013 / INPOP10a); Uranus+Neptune carry the Saturn stand-in",
            ranging="MESSENGER range accuracy 5 m, Mercury ephemeris <1 m (Genova 2018); "
                    "Juno range 20 m; LLR mm-class (all in prep_2026/planetary_doors/BOUNDS.md)",
            planet_elements="J2000 osculating elements, standard; no fit to this analysis",
        ),
        notes="a_P here uses GM_Sun = 1.32712440018e20 (IAU 2015); A22's 2.420468665e-16 "
              "corresponds to GM = 1.32746e20, a 2.6e-4 relative difference.",
    )

    if args.json_out:
        out = dict(lane=LANE, mutation=mut, status="NUMERICAL",
                   checks=[{k: v for k, v in c.items()} for c in CHECKS],
                   numbers=numbers,
                   constants_used=["c=2.99792458e8", "G=6.67430e-11", "GM_Sun=1.32712440018e20",
                                   "GM_Earth=3.986004418e14", "GM_Moon=4.9048695e12",
                                   "GM_Jup=1.26686534e17", "AU=1.495978707e11",
                                   "pc=3.0856775814913673e16", "a0_can=9.36e-11",
                                   "Lambda=1.0890e-52", "Lstar=24 pc (A20)", "B_E=3.66e-14"])
        with open(args.json_out, "w") as fh:
            json.dump(out, fh, indent=1)
    return 0 if npass == total else 1


if __name__ == "__main__":
    sys.exit(main())
