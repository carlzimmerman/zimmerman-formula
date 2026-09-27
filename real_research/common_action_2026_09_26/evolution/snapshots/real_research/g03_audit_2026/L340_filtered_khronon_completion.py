#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L340 -- C-H/K, THE FILTERED-KHRONON COMPLETION: the first construction on the record that carries the phantom's
momentum and is healthy at the orders computed.  A candidate, not a theory: the gates run here pass; the open list
at the end is what stands between it and one.

THE CONSTRUCTION (one line on top of astra's C-H, ACTION.md, whose fields, filter and endpoint terms are unchanged)
    I_CHK = I_CH + c^3/(16 pi G) Int d^4x sqrt(-g) [ alpha_c a_mu a^mu - c_2 K^2 ]
            with the C-H kernel q built from a MONOTONE phantom law nu_mono (below).
  * a_mu = D_mu ln N and K = nabla_mu n^mu are C-H's own clock quantities: the two added terms are the Blas-Pujolas-
    Sibiryakov khronometric alpha- and lambda-terms (lambda_BPS = c_2, beta = 0 so c_T = c exactly).
  * alpha_c a^2 is NOT inside C-H's |DU - a|^2, so the auxiliary U cannot cancel it.
  * On static slices K = 0 and the c_2-term and its first variation vanish: every static result of C-H/T-B (the
    Cassini and ephemeris floors, the deep-MOND limit, lensing = dynamics at leading static order) is inherited;
    alpha_c renormalises G by 1 - alpha_c (1+C)/2 ~ 1e-9.

WHY EACH PIECE (each is forced by a committed failure)
  * L330: C-H's MOND sector carries no momentum, so its phantom is frozen initial data.  The khronon K^2 channel
    (lambda != 1) is the one momentum channel on the record (L330 M5); here it is shown to restore tracking.
  * The record's 08-31 theorem (fc_kh_terminal; memory "Cassini-vs-ghost pincer"): a khronometric MOND kernel is
    radially stable only if the phantom acceleration y q is non-decreasing, and a non-decreasing phantom leaves a
    constant ~a0 tail that the ephemerides exclude ~1e4 x.  In C-H the kernel acts on the heat-FILTERED field, so the
    Sun's own high-y field never reaches it: the tail is invisible at xi >= 0.03 pc and the pincer is broken by the
    filter (S1 below reproduces the ~1e4 x exclusion at xi -> 0 and shows it vanishes at the committed floor).
  * The clock's O(Phi/c^2) symbol (G03 audit, 09-22; derivation re-run here as D1-D4): its inertia carries
    lambda_0 = 16 pi G rho_ph / c^2, so in QUMOND's negative-phantom lobes (every external-field configuration) the
    inertia crosses zero at k ~ 6.5/xi -> a pole -> linearised Hadamard ill-posedness.  The alpha_c a^2 term adds
    inertia alpha_c k^2 that removes the crossing for alpha_c >= alpha_min ~ G|rho_ph| xi^2/c^2, far below the
    preferred-frame bounds.

WHAT THIS LANE CHECKS (pre-registered in the build log: tracking, no tachyon, no ghost, GR limit)
  A1 the monotone kernel: nu_mono = nu_RAR below the phantom peak (y_p = 2.540, h_p = 0.6476 a0), then a phantom
     acceleration that keeps rising slowly (h' = 0.05 h_p/(y + y_p)); both constitutive directions C_T = nu - 1 and
     C_L = h'(y) are > 0 at every y.  nu_RAR has C_L < 0 for y > 2.54 (min -0.032): the non-monotone kernel.
  H1 TRACKING (unitary ADM scalar block, astra's L_2 + the two khronon terms, symbolic): with c_2 != 0 the
     omega -> 0 response of every field is the static MOND solution and det M(0) != 0 (no frozen mode).  Control
     c_2 = 0: det M(0) = 0 and the omega -> 0 response is NEWTONIAN (L330's frozen phantom).
  H2 NO TACHYON, NO GHOST at O((Phi/c^2)^0): one extra mode, omega^2 > 0 and positive Krein energy, for C_T and C_L
     of nu_mono at every y in 1e-3..1e4; the ghost/tachyon appears for nu_RAR's C_L < 0 (control).
  H3 THE KERNEL CONDITION IS NECESSARY: across every momentum channel scanned (the c_2 channel; the polarisation
     current 4k^2 g beta Udot; Udot^2 and psidot Udot couplings) a direction with C < 0 is a ghost or a tachyon.
  D1-D4 the G03 audit's clock-symbol derivation, re-run (S1 ln N to 2nd order; S2 the tilted leaf Laplacian;
     S3 the local sector's O(lambda_0) operator; S4 the heat boundary layer).
  H4 NEGATIVE-LOBE HEALTH at O(Phi/c^2): with alpha_c >= alpha_min the clock inertia is positive at every k and
     omega^2 > 0 at every k that fits inside the lobe, for the Solar-neighbourhood, galaxy and cluster lobes; control
     alpha_c = 0 reproduces the audit's pole.
  K2 SPARC: nu_mono vs nu_RAR on f21's 18-bin statistic, both footings: |Delta chi^2| <= 2 (indistinguishable).
  S1 THE SOLAR SYSTEM: f29's phantom quadrature with nu_mono: quadrupole and Saturn-monopole floors equal nu_RAR's
     (0.031/0.045 pc canonical, 0.033/0.049 alt); at xi <= 1e-3 pc nu_mono is ephemeris-excluded by >= 1e4 x (the
     08-31 theorem's tail, reproduced) -- the filter is what saves it.
  P1 THE PARAMETER WINDOW: alpha_1 = -4 alpha_c, alpha_2 ~ -alpha_c/2 (khronometric, beta = 0, alpha_c << c_2),
     c_T = 1; BBN |G_cos/G_N - 1| ~ 1.5 c_2 < 0.1; tracking c_s >= 3 x 600 km/s where C <= 100; alpha_c >= alpha_min.
     Non-empty: alpha_c in (alpha_min, 3.2e-9), c_2 in (7.2e-3, 0.067).
  T1 THE NEW PREDICTION: the phantom follows a source moving at v relative to the preferred frame with a lag of
     order (v/c_s)^2, c_s^2 = c_2 c^2/(C(2 + 3 c_2)); for a source faster than c_s the phantom is left behind.

  MUTATE=1 swaps nu_mono for nu_RAR (the framework's current kernel): A1 and H2 must FAIL (rc = 1).

SCOPE.  Linear, frozen-coefficient, principal order (plus the audit's O(Phi/c^2) clock terms, metric mixing dropped
there as in the audit).  NOT computed: nonlinear well-posedness; the full 1PN metric of C-H/K (beta_PPN, zetas) --
the PPN numbers quoted are the khronometric formulas with the C-H sector filtered off at Solar-System wavenumbers;
cosmological perturbations (C is singular at zero gradient); the dark sector and clusters (unchanged: still missing).

Run from the repository root:  python3 real_research/g03_audit_2026/L340_filtered_khronon_completion.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from scipy.special import erf
from scipy.optimize import brentq
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "L340", "L340_filtered_khronon_completion"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 104); P(t); P("=" * 104)


P(__doc__.split("WHY EACH PIECE")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the kernel is nu_RAR (non-monotone); A1 and H2 must FAIL ***")

# ============================================================================================ A1 the kernel
banner("A1  THE KERNEL: a monotone phantom law, and why nu_RAR is not one")
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10**LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 / (-np.expm1(-np.sqrt(y)))
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y
def CL_of(nuf, y):                       # longitudinal constitutive coefficient d(y nu)/dy - 1 = d(phantom)/d(g_N)
    y = np.asarray(y, float); e = 1e-5
    return ((y * (1 + e)) * nuf(y * (1 + e)) - (y * (1 - e)) * nuf(y * (1 - e))) / (2 * y * e) - 1.0
KER = nu_rar if MUTATE else nu_mono
KNAME = "nu_RAR" if MUTATE else "nu_mono"
ys = np.logspace(-3, 4, 1401)
CT = KER(ys) - 1.0; CLv = CL_of(KER, ys)
dlog = np.log10(nu_mono(ys) / nu_rar(ys))
P(f"    nu_RAR phantom peak: y_p = {Y_P:.4f}, h_p = {H_P:.4f} a0; nu_mono follows nu_RAR below it, then h' = {DELTA} h_p/(y+y_p)")
P(f"    kernel used: {KNAME};  min C_T = {CT.min():.3e};  min C_L = {CLv.min():+.3e} (nu_RAR's min C_L = {CL_of(nu_rar, ys).min():+.4f})")
P(f"    nu_mono vs nu_RAR: max |d log g_obs| = {np.abs(dlog).max():.4f} dex at y = {ys[np.argmax(np.abs(dlog))]:.1f}")
OUT["numbers"]["A1"] = {"y_p": Y_P, "h_p": H_P, "delta": DELTA, "kernel": KNAME, "min_CT": float(CT.min()), "min_CL": float(CLv.min()),
                        "max_dlog_vs_rar": float(np.abs(dlog).max())}
check("A1 the kernel in use has positive constitutive coefficients in both directions at every y in 1e-3..1e4 "
      "(phantom acceleration non-decreasing in g_N)", f"{KNAME}: min C_T {CT.min():.2e}, min C_L {CLv.min():+.2e}",
      CT.min() > 0 and CLv.min() > 0,
      "nu_mono differs from nu_RAR by <= 0.01 dex; nu_RAR itself fails this at y > 2.54 (the phantom turns over)")

# ============================================================================================ H1 tracking
banner("H1  TRACKING: astra's scalar block + the khronon terms (unitary gauge, principal order, symbolic)")
k, C, c2, ac, w = sp.symbols('k C c_2 alpha_c omega', real=True)
a2s, a3s, gs_ = sp.symbols('a2 a3 g', real=True)
psi, phi, beta, U, R = sp.symbols('psi phi beta U R')
D = -sp.I * w
eps = -c2                                            # (1 - lambda) with lambda = 1 + c_2
def block(C_, eps_, ac_, a2_=0, a3_=0, g_=0):
    E = [4*k**2*psi - 4*k**2*phi - D*(-12*D*psi + 4*k**2*beta + 6*eps_*(3*D*psi - k**2*beta) + a3_*D*U),
         -4*k**2*psi - 4*k**2*(U - phi) + 2*ac_*k**2*phi - R,
         4*k**2*D*psi - 2*eps_*k**2*(3*D*psi - k**2*beta) + 4*k**2*g_*D*U + D*R,
         4*k**2*(U - phi) + 4*k**2*C_*U - D*(2*a2_*D*U + a3_*D*psi + 4*k**2*g_*beta)]
    X = [psi, phi, beta, U]
    M = sp.Matrix([[sp.diff(e_, x_) for x_ in X] for e_ in E]); S = sp.Matrix([-e_.subs({x_: 0 for x_ in X}) for e_ in E])
    return M, S
M, S = block(C, eps, ac)
herm = sp.simplify(M - M.H.subs({sp.conjugate(w): w, sp.conjugate(k): k, sp.conjugate(C): C, sp.conjugate(c2): c2,
                                 sp.conjugate(ac): ac})) == sp.zeros(4)
det0 = sp.factor(sp.simplify(M.det().subs(w, 0)))
sol = M.LUsolve(S); psiN = -R / (4 * k**2)
lims = {}
for nm, v in zip(("psi", "phi", "beta", "U"), sol):
    num, den = sp.fraction(sp.cancel(sp.together(v / psiN)))
    lims[nm] = sp.factor(sp.cancel(num.subs(w, 0) / den.subs(w, 0)))
static_psi = sp.factor((1 + C) / (1 - ac * (1 + C) / 2))
M0, S0 = block(C, 0, ac)
det0_ctrl = sp.simplify(M0.det().subs(w, 0))
sol0 = M0.LUsolve(S0)
num0, den0 = sp.fraction(sp.cancel(sp.together(sol0[0] / psiN)))
w_small = sp.Symbol('w_small', positive=True)
ctrl_lim = sp.limit(sp.cancel(num0 / den0).subs(w, w_small), w_small, 0, '+')
P(f"    M(omega) Hermitian: {herm};  det M(0) = {det0}")
P(f"    omega -> 0:  psi/psi_N = {lims['psi']},  phi/psi_N = {lims['phi']},  U/psi_N = {lims['U']},  beta = {lims['beta']}")
P(f"    static MOND solution of the same block: psi = phi = {static_psi} psi_N  (alpha_c renormalises G, BPS-like)")
P(f"    control c_2 = 0 (C-H alone): det M(0) = {det0_ctrl};  omega -> 0+ of psi/psi_N = {sp.simplify(ctrl_lim)}  (Newtonian: frozen phantom)")
trk = (sp.simplify(lims['psi'] - static_psi) == 0 and sp.simplify(lims['phi'] - static_psi) == 0 and sp.simplify(lims['beta']) == 0
       and det0 != 0)
ctrl_ok = det0_ctrl == 0 and sp.simplify(ctrl_lim - 1) == 0
OUT["numbers"]["H1"] = {"det0": str(det0), "limits": {kk: str(vv) for kk, vv in lims.items()}, "control_det0": str(det0_ctrl),
                        "control_limit": str(ctrl_lim)}
check("H1 with the khronon's c_2 channel the omega -> 0 response is the static MOND solution and there is no frozen mode; "
      "without it (control) the response is Newtonian and det M(0) = 0",
      f"psi -> {lims['psi']} psi_N; det M(0) = {det0}; control: {sp.simplify(ctrl_lim)} psi_N, det 0",
      herm and trk and ctrl_ok, "the phantom forms and follows sources that move slowly compared with c_s (T1); L330's gate is passed")

# ============================================================================================ H2 health, O(1)
banner("H2  NO TACHYON, NO GHOST at leading order (Krein signs of the block modes, both constitutive directions)")
Mf = sp.lambdify((w, k, C, c2, ac, a2s, a3s, gs_), block(C, -c2, ac, a2s, a3s, gs_)[0], "numpy")
detP = sp.Poly(sp.expand(block(C, -c2, ac, a2s, a3s, gs_)[0].det().subs(k, 1)), w)
cf = sp.lambdify((C, c2, ac, a2s, a3s, gs_), [detP.coeff_monomial(w**j) for j in (4, 2, 0)], "numpy")
def modes(Cv, c2v, acv, a2v=0.0, a3v=0.0, gv=0.0):
    A4, A2, A0_ = [complex(x) for x in cf(Cv, c2v, acv, a2v, a3v, gv)]
    Ws = ([-A0_ / A2] if abs(A2) > 1e-300 else []) if abs(A4) < 1e-14 else \
         [(-A2 + s * np.sqrt(A2 * A2 - 4 * A4 * A0_ + 0j)) / (2 * A4) for s in (1, -1)]
    out = []
    for W in Ws:
        if abs(W) < 1e-14: out.append("zero"); continue
        if abs(W.imag) > 1e-9 * max(1, abs(W)) or W.real < 0: out.append("TACHYON"); continue
        w0 = math.sqrt(W.real); Mn = lambda ww: np.array(Mf(ww, 1, Cv, c2v, acv, a2v, a3v, gv), dtype=complex)
        ev, vec = np.linalg.eigh(Mn(w0)); v = vec[:, np.argmin(abs(ev))]; hh = 1e-6 * max(1, w0)
        s_ = float(np.real(np.conj(v) @ ((Mn(w0 + hh) - Mn(w0 - hh)) / (2 * hh)) @ v))
        out.append("ok" if s_ > 0 else "GHOST")
    return out
C2V, ACV = 1.0e-2, 1.0e-9
ysH = np.logspace(-3, 4, 57)
bad = []
for yv in ysH:
    for lab, Cv in (("T", float(KER(yv) - 1)), ("L", float(CL_of(KER, yv)))):
        ms = modes(Cv, C2V, ACV)
        if any(m in ("TACHYON", "GHOST") for m in ms): bad.append((round(float(yv), 3), lab, Cv, ms))
ctrl = modes(float(CL_of(nu_rar, 10.0)), C2V, ACV)
cs2_T = [float(C2V / ((KER(yv) - 1) * (2 + 3 * C2V))) for yv in (0.01, 1.0, 100.0)]
P(f"    kernel {KNAME}, c_2 = {C2V}, alpha_c = {ACV}: unhealthy (y, direction) cells: {len(bad)}  {bad[:4]}")
P(f"    control nu_RAR C_L at y = 10 ({float(CL_of(nu_rar, 10.0)):+.4f}): {ctrl}")
P(f"    mode speed^2 c_s^2/c^2 = c_2/(C(2+3c_2)), transverse, at y = 0.01 / 1 / 100: {', '.join(f'{v:.2e}' for v in cs2_T)}")
OUT["numbers"]["H2"] = {"c2": C2V, "alpha_c": ACV, "n_bad": len(bad), "bad_sample": bad[:6], "control": ctrl, "cs2_T": cs2_T}
check("H2 every (y, direction) cell of the kernel gives exactly healthy modes (omega^2 > 0, positive energy); the "
      "control C < 0 (nu_RAR, longitudinal, y = 10) gives a ghost or tachyon", f"{len(bad)} unhealthy cells; control {ctrl}",
      len(bad) == 0 and any(m in ("TACHYON", "GHOST") for m in ctrl))

# ============================================================================================ H3 the kernel condition is necessary
banner("H3  THE KERNEL CONDITION IS NECESSARY: every momentum channel scanned is unhealthy where C < 0")
fam_bad, fam_n = 0, 0
for Cv in (-0.12, -0.05, -0.01):
    for c2v in (1e-3, 1e-2, 5e-2):
        for G_ in (-1.0, 0.0, 1.0):
            for A2_ in (-1.0, 0.0, 1.0):
                for A3_ in (-1.0, 0.0, 1.0):
                    ms = modes(Cv, c2v, 0.0, A2_ * abs(Cv), A3_ * abs(Cv), G_ * Cv)
                    fam_n += 1; fam_bad += any(m in ("TACHYON", "GHOST") for m in ms)
pol = [modes(Cv, 0.0, 0.0, 6 * Cv**2 + 2 * Cv / 1e-2, 0.0, -Cv) for Cv in (-0.1, 0.3)]
P(f"    C < 0 cells scanned (c_2 channel x polarisation current x Udot^2 x psidot Udot): {fam_n}; unhealthy: {fam_bad}")
P(f"    exact polarisation current (g = -C, c_2 = 0, speed^2 1e-2): C = -0.1 -> {pol[0]}, C = +0.3 -> {pol[1]}")
OUT["numbers"]["H3"] = {"cells": fam_n, "unhealthy": fam_bad, "polarisation_current": pol}
check("H3 no momentum channel in the scanned families makes a C < 0 direction healthy (C is the clock's inertia; momentum "
      "couplings change only its restoring term)", f"{fam_bad}/{fam_n} unhealthy", fam_bad == fam_n,
      "the record's non-monotone kernels (nu_RAR, mu_exp) cannot be completed this way; a monotone phantom law is required")

# ============================================================================================ D1-D4 the audit's clock symbol, re-run
banner("D1-D4  THE CLOCK'S O(Phi/c^2) SYMBOL (G03 audit derivation, re-run in full)")
t, x, y, z = sp.symbols('t x y z', real=True); X4 = [t, x, y, z]
e, epsA = sp.symbols('e epsilon', positive=True)
pi_ = sp.Function('pi')(t, x, y, z); phi0 = sp.Function('phi0')(x, y, z); U0 = sp.Function('U0')(x, y, z)
Ff = sp.Function('F')(t, x, y, z)
N0 = sp.exp(epsA * phi0); ginv = sp.diag(-1 / N0**2, 1, 1, 1)
tau = t + e * pi_; dtau = [sp.diff(tau, v) for v in X4]
Xc = -sum(ginv[m, n] * dtau[m] * dtau[n] for m in range(4) for n in range(4))
lnN = -sp.log(Xc) / 2
lnN2 = sum(sp.diff(lnN, e, j).subs(e, 0) * e**j / sp.factorial(j) for j in range(3))
tgt1 = epsA * phi0 - e * sp.diff(pi_, t) + e**2 * (sp.diff(pi_, t)**2 + N0**2 * sum(sp.diff(pi_, v)**2 for v in (x, y, z))) / 2
d1 = sp.simplify(sp.expand(sp.expand_log(sp.expand(lnN2 - tgt1), force=True)))
eta = sp.diag(-1, 1, 1, 1)
Xf = -sum(eta[m, n] * dtau[m] * dtau[n] for m in range(4) for n in range(4))
n_dn = [-dd / sp.sqrt(Xf) for dd in dtau]; n_up = [sum(eta[m, kk] * n_dn[kk] for kk in range(4)) for m in range(4)]
h_up = [[eta[m, n] + n_up[m] * n_up[n] for n in range(4)] for m in range(4)]
Kx = sum(sp.diff(n_up[m], X4[m]) for m in range(4))
DelF = sum(h_up[m][n] * sp.diff(Ff, X4[m], X4[n]) for m in range(4) for n in range(4)) + Kx * sum(n_up[m] * sp.diff(Ff, X4[m]) for m in range(4))
DelF1 = DelF.subs(e, 0) + e * sp.diff(DelF, e).subs(e, 0)
lap = lambda f: sum(sp.diff(f, v, 2) for v in (x, y, z))
gdot = lambda f, g_: sum(sp.diff(f, v) * sp.diff(g_, v) for v in (x, y, z))
d2 = sp.simplify(sp.expand(DelF1 - (lap(Ff) - e * (2 * gdot(pi_, sp.diff(Ff, t)) + lap(pi_) * sp.diff(Ff, t)))))
u_ = -sp.diff(pi_, t); Ux = epsA * U0 + e * u_; Th = Ux - lnN
nd = [-dd / sp.sqrt(Xc) for dd in dtau]; nu_v = [sum(ginv[m, kk] * nd[kk] for kk in range(4)) for m in range(4)]
hup = [[ginv[m, n] + nu_v[m] * nu_v[n] for n in range(4)] for m in range(4)]
dTh = [sp.diff(Th, v) for v in X4]
Lloc = N0 * 2 * sum(hup[m][n] * dTh[m] * dTh[n] for m in range(4) for n in range(4))
Th0 = epsA * (U0 - phi0); lam0x = -4 / N0 * sum(sp.diff(N0 * sp.diff(Th0, v), v) for v in (x, y, z))
Ltot = Lloc - N0 * lam0x * Ux
L2 = sp.diff(Ltot, e, 2).subs(e, 0) / 2
from sympy.calculus.euler import euler_equations
def EL(Lx):
    eqs = euler_equations(Lx, [pi_], X4) if Lx.has(pi_) else []
    return eqs[0].lhs if eqs else sp.S(0)
d3a = sp.simplify(EL(sp.expand(L2.subs(epsA, 0))))
Tgt = sp.expand(sp.diff(-(N0 * lam0x / 2) * (sp.diff(pi_, t)**2 + N0**2 * sum(sp.diff(pi_, v)**2 for v in (x, y, z))), epsA).subs(epsA, 0))
d3b = sp.simplify(sp.expand(EL(sp.expand(sp.diff(L2, epsA).subs(epsA, 0))) - EL(Tgt)))
kk_, bb_, ll_, ww_, PP_ = sp.symbols('k b lambda_0 omega P', positive=True)
pim = PP_ * sp.cos(kk_ * x - ww_ * t)
Xz = lambda zz: -sp.exp(-kk_**2 * zz) * sp.diff(pim, t, 2)
Bz = sp.diff(pim, x) * 2 * sp.diff(Xz(z), x) + sp.diff(pim, x, 2) * Xz(z)
avg = lambda f: sp.simplify(sp.integrate(sp.integrate(f, (x, 0, 2 * sp.pi / kk_)) * kk_ / (2 * sp.pi), (t, 0, 2 * sp.pi / ww_)) * ww_ / (2 * sp.pi))
heat = sp.simplify(sp.integrate(ll_ * avg(Bz), (z, 0, bb_)))
d4 = sp.simplify(heat - ll_ * (1 - sp.exp(-bb_ * kk_**2)) * avg(sp.diff(pim, t)**2))
P(f"    D1 ln N_clock 2nd order: residual {d1};  D2 tilted leaf Laplacian: residual {d2}")
P(f"    D3 local sector: O(eps^0) EL = {d3a} (clock pure gauge on a Newtonian background); O(eps^1) vs -(N0 lambda0/2)(pi_t^2+|grad pi|^2): {d3b}")
P(f"    D4 heat boundary layer - lambda0(1 - e^(-b k^2))<pi_t^2> = {d4}")
dok = d1 == 0 and d2 == 0 and d3a == 0 and d3b == 0 and d4 == 0
check("D1-D4 the clock's O(Phi/c^2) terms: inertia 2k^2 C/(1+C) + lambda0 (1/2 - e^{-b k^2}), restoring (lambda0/2) k^2, "
      "lambda0 = 16 pi G rho_ph/c^2 -- every ingredient verified symbolically", f"residuals {d1}, {d2}, {d3a}, {d3b}, {d4}", dok,
      "metric mixing dropped (it enters at O(lambda0^2/k^2)), frozen coefficients -- the audit's stated approximations")

# ============================================================================================ H4 negative lobes
banner("H4  NEGATIVE-PHANTOM LOBES at O(Phi/c^2): the alpha_c a^2 term removes the audit's pole")
Gn, cc, Msun, PCm = 6.6743e-11, 2.99792458e8, 1.98892e30, 3.0857e16
def symbol(kv, lam0, C0, xi, acv, c2v):
    bb = xi**2 / 2
    inertia = 2 * kv**2 * C0 * math.exp(-(xi * kv)**2) / (1 + C0) + acv * kv**2 + lam0 * (0.5 - math.exp(-bb * kv**2))
    restoring = lam0 / 2 * kv**2 + c2v * kv**4
    return inertia, restoring
cases = {"Solar nbhd lobe": (-0.01, 0.157, 0.045, 0.03), "galaxy-in-group lobe": (-0.05, 0.3, 4.0, 50.0),
         "cluster-outskirt lobe": (-1e-4, 1.0, 50.0, 3e5), "galaxy transition (rho > 0)": (0.05, 0.3, 4.0, 1000.0)}
H4 = {}
for nm, (rho_pc3, C0, xi_pc, Llobe_pc) in cases.items():
    rho = rho_pc3 * Msun / PCm**3; lam0 = 16 * math.pi * Gn * rho / cc**2; xi = xi_pc * PCm; L = Llobe_pc * PCm
    ks = np.logspace(math.log10(2 * math.pi / L), math.log10(1e3 / xi), 4000)
    a_min = abs(lam0) * xi**2 / 20 if lam0 < 0 else 0.0
    res = {}
    for acv in (0.0, ACV):
        inr = np.array([symbol(kv, lam0, C0, xi, acv, C2V) for kv in ks])
        res[acv] = (bool((inr[:, 0] > 0).all()), bool((inr[:, 1] / np.where(inr[:, 0] != 0, inr[:, 0], np.nan) > 0).all()))
    H4[nm] = {"lam0_m-2": lam0, "alpha_min": a_min, "alpha_c=0": res[0.0], "alpha_c=1e-9": res[ACV]}
    P(f"    {nm:28s} rho_ph {rho_pc3:+.0e} Msun/pc^3, xi {xi_pc} pc: lambda0 = {lam0:+.2e} m^-2, alpha_min ~ {a_min:.1e};  "
      f"(inertia>0, omega^2>0) alpha_c=0: {res[0.0]}, alpha_c=1e-9: {res[ACV]}")
OUT["numbers"]["H4"] = H4
neg = [v for kk2, v in H4.items() if v["lam0_m-2"] < 0]
check("H4 in every negative-phantom lobe the clock inertia stays positive and omega^2 > 0 at all k that fit inside the lobe "
      "once alpha_c = 1e-9 (>> alpha_min); with alpha_c = 0 the inertia crosses zero (the audit's pole, control)",
      "; ".join(f"{kk2}: {v['alpha_c=0']} -> {v['alpha_c=1e-9']}" for kk2, v in H4.items()),
      all(v["alpha_c=1e-9"] == (True, True) for v in H4.values()) and all(not v["alpha_c=0"][0] for v in neg),
      "alpha_min ~ G |rho_ph| xi^2 / c^2 is the phantom potential across xi -- 1e-19..1e-11, far below alpha_2's 3.2e-9")

# ============================================================================================ H5 static limit
banner("H5  THE STATIC LIMIT IS UNTOUCHED: K = 0 on a static slicing")
Ns = sp.Function('N', positive=True)(x, y, z); ws_ = sp.Function('w')(x, y, z)
gs = sp.diag(-Ns**2, *(3 * [sp.exp(2 * ws_)])); gsi = gs.inv()
ns_dn = [-Ns, 0, 0, 0]; ns_up = [sum(gsi[m, kk] * ns_dn[kk] for kk in range(4)) for m in range(4)]
sq = sp.sqrt(-gs.det())
Kst = sp.simplify(sum(sp.diff(sq * ns_up[m], X4[m]) for m in range(4)) / sq)
P(f"    K = nabla_mu n^mu for a static lapse N(x) and static leaves, zero shift: {Kst}")
check("H5 on static configurations K = 0, so -c_2 K^2 and its first variation (proportional to K) vanish: C-H's static "
      "solutions, Cassini/ephemeris floors and deep-MOND limit carry over; alpha_c only renormalises G by O(1e-9)",
      f"K_static = {Kst}", Kst == 0)

# ============================================================================================ K2 SPARC
banner("K2  SPARC: the monotone kernel against nu_RAR on f21's binned statistic")
sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
cwd = os.getcwd(); os.chdir(os.path.join(REPO, "hunt_2026"))
from hunt_lib import load_sparc, A0 as A0H
gals = load_sparc(); os.chdir(cwd)
gb = np.concatenate([g_["gbar"] for g_ in gals]); go = np.concatenate([g_["gobs"] for g_ in gals])
gid = np.concatenate([np.full(len(g_["r"]), i) for i, g_ in enumerate(gals)])
mm = (gb > 0) & (go > 0); gb, go, gid = gb[mm], go[mm], gid[mm]; lo = np.log10(go)
K2 = {}
for foot, a0 in A0H.items():
    lyy = np.log10(gb / a0); edges = np.linspace(-2.6, 1.6, 22); cen = 0.5 * (edges[1:] + edges[:-1])
    chi = {"RAR": 0.0, "mono": 0.0}; nb = 0
    for i in range(len(cen)):
        kb = (lyy >= edges[i]) & (lyy < edges[i + 1])
        if kb.sum() < 15: continue
        rng = np.random.default_rng(i); gl = np.unique(gid[kb]); bs = []
        for _ in range(200):
            pick = rng.choice(gl, len(gl), replace=True)
            idx = np.concatenate([np.where(kb & (gid == g_))[0] for g_ in pick]); bs.append(np.median(lo[idx]))
        se = float(np.std(bs)); ob = float(np.median(lo[kb])); mg = float(np.median(np.log10(gb[kb])))
        chi["RAR"] += ((ob - (math.log10(float(nu_rar(10**cen[i]))) + mg)) / se)**2
        chi["mono"] += ((ob - (math.log10(float(nu_mono(10**cen[i]))) + mg)) / se)**2; nb += 1
    K2[foot] = {"bins": nb, "chi2_RAR": chi["RAR"], "chi2_mono": chi["mono"], "delta": chi["mono"] - chi["RAR"]}
    P(f"    {foot:9s}: {nb} bins, chi^2 nu_RAR = {chi['RAR']:.1f}, nu_mono = {chi['mono']:.1f}, Delta = {chi['mono'] - chi['RAR']:+.1f}")
OUT["numbers"]["K2"] = K2
check("K2 on SPARC the monotone kernel is indistinguishable from nu_RAR (|Delta chi^2| <= 2 on 18 bins, both footings; "
      "nu_RAR's chi^2 reproduces f21's 38.8)", "; ".join(f"{f_}: {v['delta']:+.1f}" for f_, v in K2.items()),
      all(abs(v["delta"]) <= 2 for v in K2.values()) and abs(K2["canonical"]["chi2_RAR"] - 38.8) < 0.2)

# ============================================================================================ S1 Solar System
banner("S1  THE SOLAR SYSTEM with the monotone kernel (f29's phantom quadrature, both footings)")
MS_, AU = 1.98892e30, 1.495978707e11; R_SAT = 9.54 * AU; GEXT = 2.32e-10; Q2C = 5.2e-27
MBND = 1.1e-17 * 4 / 3 * math.pi * R_SAT**3
NR, NT = 1400, 241
def phantom(nuf, M, wd, gext, a0, rmin, rmax):
    r = np.geomspace(rmin, rmax, NR); th = np.linspace(0, math.pi, NT); Rg, TH = np.meshgrid(r, th, indexing="ij")
    xx = Rg / (math.sqrt(2) * wd); Menc = M * (erf(xx) - math.sqrt(2 / math.pi) * (Rg / wd) * np.exp(-Rg**2 / (2 * wd * wd)))
    Menc = np.where(Rg < 0.05 * wd, M * math.sqrt(2 / math.pi) * (Rg / wd)**3 / 3 * (1 - 0.3 * (Rg / wd)**2), Menc)
    gsr = -Gn * Menc / Rg**2; gr = gext * np.cos(TH) + gsr; gt = -gext * np.sin(TH)
    f = nuf(np.hypot(gr, gt) / a0) - 1.0; Fr = Rg**2 * f * gr; Ft = np.sin(TH) * f * gt
    dFr = np.gradient(Fr, r, axis=0) / Rg**2; dFt = np.gradient(Ft, th, axis=1) / (Rg * np.maximum(np.sin(TH), 1e-12))
    dFt[:, 0] = dFt[:, 1]; dFt[:, -1] = dFt[:, -2]
    return r, th, -(dFr + dFt) / (4 * math.pi * Gn)
def quad(r, th, rho):
    P2 = 0.5 * (3 * np.cos(th)**2 - 1)
    return 3 * Gn * 2 * math.pi * integrate.trapezoid(integrate.trapezoid(rho * P2[None, :] * np.sin(th)[None, :], th, axis=1) / r, r)
def encl(r, th, rho, s):
    inner = integrate.trapezoid(rho * np.sin(th)[None, :], th, axis=1) * 2 * math.pi * r**2; m_ = r <= s
    return integrate.trapezoid(inner[m_], r[m_])
XIS = np.array([1e-4, 1e-3, 0.01, 0.02, 0.03, 0.04, 0.05, 0.07, 0.1, 0.2]) * PCm
def run_ss(nuf, a0):
    eN = brentq(lambda e_: float(nuf(e_)) * e_ - GEXT / a0, 1e-9, GEXT / a0 * 1.5, xtol=1e-14) * a0; rM = math.sqrt(Gn * MS_ / a0)
    q, mo = [], []
    for xi in XIS:
        r, th, rho = phantom(nuf, MS_, xi, eN, a0, min(1e-4 * rM, 1e-3 * xi, 0.1 * R_SAT), max(1e4 * rM, 1e3 * xi))
        q.append(abs(quad(r, th, rho)) / Q2C); mo.append(encl(r, th, rho, R_SAT) / MBND)
    def cross(v):
        v = np.array(v)
        for i in range(3, len(XIS)):
            if v[i - 1] >= 1 > v[i]:
                return math.exp(np.interp(0, [math.log(v[i]), math.log(v[i - 1])], [math.log(XIS[i]), math.log(XIS[i - 1])])) / PCm
        return float("nan")
    return cross(q), cross(mo), q, mo
SS = {}
for foot, a0 in (("canonical", 9.36e-11), ("alt", 1.13e-10)):
    for nm, nf in (("nu_RAR", nu_rar), ("nu_mono", nu_mono)):
        xq, xm, q, mo = run_ss(nf, a0); SS[(foot, nm)] = (xq, xm, q, mo)
        P(f"    {foot:9s} {nm:8s}: quadrupole floor {xq:.3f} pc, Saturn-monopole floor {xm:.3f} pc;  at xi = 1e-4 pc: "
          f"Q2/ceil {q[0]:.2e}, M/bound {mo[0]:.2e}")
OUT["numbers"]["S1"] = {f"{kk2[0]}/{kk2[1]}": {"xi_Q2": v[0], "xi_M": v[1], "M_over_bound_at_1e-4pc": v[3][0]} for kk2, v in SS.items()}
same = all(abs(SS[(f_, "nu_mono")][j] - SS[(f_, "nu_RAR")][j]) < 2e-3 for f_ in ("canonical", "alt") for j in (0, 1))
tail = all(SS[(f_, "nu_mono")][3][0] > 1e4 for f_ in ("canonical", "alt"))
check("S1 with the filter the monotone kernel's Solar-System floors equal nu_RAR's; without it (xi = 1e-4 pc) its constant "
      "phantom tail is ephemeris-excluded by > 1e4 x -- the 08-31 Cassini-vs-ghost pincer, reproduced, and broken by the filter",
      "; ".join(f"{kk2[0]}/{kk2[1]}: {v[0]:.3f}/{v[1]:.3f} pc" for kk2, v in SS.items()) +
      f"; unfiltered monotone tail {SS[('canonical', 'nu_mono')][3][0]:.1e} x bound", same and tail,
      "the filtered field inside the Solar System stays at y < 2.54, where the two kernels coincide")

# ============================================================================================ P1 window, T1 prediction
banner("P1  THE PARAMETER WINDOW, and T1 the tracking speed")
A2_BOUND, A1_BOUND, BBN = 1.6e-9, 1.1e-5, 0.1
ac_max = min(2 * A2_BOUND, A1_BOUND / 4)
c2_max = BBN / 1.5
vtrk, Cmax = 3 * 600e3 / cc, 100.0
c2_min = 2 * Cmax * vtrk**2 / (1 - 3 * Cmax * vtrk**2)
amin_all = max(v["alpha_min"] for v in H4.values())
P(f"    alpha_c window: alpha_min {amin_all:.1e} < alpha_c < {ac_max:.1e}   (|alpha_2| < {A2_BOUND}, |alpha_1| < {A1_BOUND}; alpha_1 = -4 alpha_c, alpha_2 ~ -alpha_c/2)")
P(f"    c_2 window:     {c2_min:.2e} < c_2 < {c2_max:.3f}   (tracking c_s >= 3 x 600 km/s where C <= {Cmax:.0f}; BBN 1.5 c_2 < {BBN})")
P(f"    c_T = 1 exactly (beta = 0; the K^2 term is trace-only, invisible to transverse-traceless modes)")
OUT["numbers"]["P1"] = {"alpha_c_min": amin_all, "alpha_c_max": ac_max, "c2_min": c2_min, "c2_max": c2_max}
check("P1 a non-empty window satisfies the preferred-frame, GW170817, BBN, tracking and negative-lobe conditions at once",
      f"alpha_c in ({amin_all:.1e}, {ac_max:.1e}); c_2 in ({c2_min:.1e}, {c2_max:.3f})",
      amin_all < ac_max and c2_min < c2_max,
      "PPN from the khronometric formulas with the C-H sector filtered off at Solar-System wavenumbers (e^{-xi^2 k^2}, xi/AU ~ 1e4)")
rows = []
for c2v in (c2_min, 0.03, c2_max):
    for Cv in (1.0, 10.0, 100.0):
        rows.append((c2v, Cv, cc * math.sqrt(c2v / (Cv * (2 + 3 * c2v))) / 1e3))
P("    c_s [km/s] (C = 1 / 10 / 100):  " + " | ".join(f"c_2 = {c2v:.3g}: " + ", ".join(f"{r_[2]:.0f}" for r_ in rows if r_[0] == c2v)
                                                        for c2v in (c2_min, 0.03, c2_max)))
OUT["numbers"]["T1"] = rows
check("T1 (a prediction, not a test) the phantom follows sources slower than c_s ~ 1e3-1e4 km/s in halos and lags faster ones "
      "(fractional lag ~ (v/c_s)^2); merging clusters at 3000-4700 km/s sit near the edge for c_2 near its floor",
      "; ".join(f"c_2={r_[0]:.2g}, C={r_[1]:.0f}: {r_[2]:.0f} km/s" for r_ in rows[:3]), True, load_bearing=False)

banner("VERDICT")
P(f"""  C-H/K -- astra's C-H plus the khronon's alpha- and lambda-terms, with a monotone phantom law -- passes every gate run
  here: the phantom forms and follows matter (H1, the L330 gate), no tachyon and no ghost at leading order (H2), the
  negative-lobe pole removed at O(Phi/c^2) (H4), the static C-H results inherited exactly (H5), galaxies unchanged
  (K2), the Solar System unchanged at the committed floors (S1), and a non-empty window for the preferred-frame,
  GW170817, BBN and tracking conditions (P1).  Two record no-goes are evaded by named mechanisms: the frozen phantom
  (L330) by the lambda-channel, the 08-31 Cassini-vs-ghost pincer by the heat filter.  The price is a kernel change of
  <= 0.01 dex (the phantom acceleration must never decrease) and a new prediction (T1).  NOT computed and required
  before this is a theory: nonlinear well-posedness; the full 1PN metric; cosmological perturbations; the dark sector.
  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
