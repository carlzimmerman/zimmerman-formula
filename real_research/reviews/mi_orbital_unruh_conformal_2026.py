#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mi_orbital_unruh_conformal_2026.py -- INDEPENDENT CONFORMAL-COORDINATE DERIVATION LANE
=======================================================================================
Task (2026-08-03): derive the Wightman function W(s) of the conformally coupled
massless scalar (Bunch-Davies vacuum) along the static-patch circular orbit in dS4
by the CONFORMAL route -- Poincare (conformally flat) chart + conformal weighting of
the flat-space Wightman function -- and verify it EQUALS the GEMS embedding form

    W(s) = 1/(4 pi^2 (DX)^2(s - i eps)),
    (DX)^2(s) = 4 R^2 sin^2(w s/2) - 4 A^2 sinh^2(h s/2),
    A^2 = 1/H^2 - R^2,  h = H/N,  w = Omega/N,  N = sqrt(1 - H^2 R^2 - R^2 Omega^2),

so the compute lane rests on two independent derivations of the same W(s).
Also: explicit KMS check in the conformal chart (static limit is periodic in
imaginary proper time with period 2 pi N0 / H, i.e. thermal at the Deser-Levin
temperature T = H/(2 pi sqrt(1 - H^2 R^2))), and the required identities.

PRIOR ART used here (exact references -- none of the constructions below is new):
 * GEMS / embedding thermality, incl. static and circular dS worldlines:
   S. Deser & O. Levin, Class. Quantum Grav. 14 (1997) L163;
   S. Deser & O. Levin, Phys. Rev. D 59 (1999) 064004 ("Mapping Hawking into Unruh").
 * Conformal vacuum; conformally coupled scalar carries weight Omega^{-1} per point
   in d=4 (so W_dS = (a a')^{-1} W_flat):
   N. D. Birrell & P. C. W. Davies, "Quantum Fields in Curved Space" (1982),
   secs. 3.7 and 5.4; T. S. Bunch & P. C. W. Davies, Proc. R. Soc. A 360 (1978) 117.
 * Chordal (1-Z) closed form of the dS conformal two-point function:
   M. Spradlin, A. Strominger, A. Volovich, hep-th/0110007, sec. 4.
 * Flat-space circular-motion detector response (the H->0 anchor):
   J. R. Letaw, Phys. Rev. D 23 (1981) 1709;
   J. S. Bell & J. M. Leinaas, Nucl. Phys. B 212 (1983) 131.
 * Framework context: Milgrom, Phys. Lett. A 253 (1999) 273 (hyperbolic balance);
   Milgrom, Phys. Rev. D 102 (2020) 084015 (kappa = 1/2pi).

Conventions: c = 1, mostly-plus 5D Minkowski (-++++), dS4 hyperboloid X.X = 1/H^2.
Flat massless Wightman normalization: W_flat = 1/(4 pi^2 [ |Dx|^2 - (Dt - i eps)^2 ]),
so on an inertial line W = -1/(4 pi^2 (Dt - i eps)^2).

All numerics use mpmath at dps 50-80 (float64 saturation / underflow traps avoided
by design; the corpus has been burned by 1 - exp(-47) == 1.0 before).
Every check prints [OK]/[FAIL] and any failure exits 1.
"""

import sys
import time
import sympy as sp
import mpmath as mp

T0 = time.time()
NPASS = [0]
NTOT = [0]


def check(name, ok, detail=""):
    NTOT[0] += 1
    tag = "[OK]  " if ok else "[FAIL]"
    if ok:
        NPASS[0] += 1
    print(f"{tag} {name}" + (f"   ({detail})" if detail else ""), flush=True)
    return ok


def zero_sym(expr):
    """Robust symbolic is-this-identically-zero (exp/trig rational identities)."""
    e = sp.sympify(expr)
    e = sp.expand_trig(e)
    e = e.rewrite(sp.exp)
    e = sp.expand(e)
    e = sp.cancel(sp.together(e))
    e = sp.expand(e)
    if e == 0:
        return True
    return sp.simplify(e) == 0


def rel(x, y):
    d = mp.fabs(x - y)
    m = max(mp.fabs(x), mp.fabs(y))
    return d / m if m > 0 else d


print("=" * 78)
print("S1  SYMBOLIC SETUP: charts, embeddings, induced metrics")
print("=" * 78)

H = sp.Symbol('H', positive=True)
R = sp.Symbol('R', positive=True)
Om = sp.Symbol('Omega', positive=True)
tau, tau1, tau2 = sp.symbols('tau tau_1 tau_2', real=True)
sS = sp.Symbol('s')  # complex-capable proper-time separation for KMS algebra
sR = sp.Symbol('s_r', real=True)

# ---- Poincare / conformally flat chart (expanding patch, eta < 0) --------------
eta, etap = sp.symbols('eta eta_p', negative=True)
x1, x2, x3, y1, y2, y3 = sp.symbols('x_1 x_2 x_3 y_1 y_2 y_3', real=True)


def X_conf(et, xv):
    """Embedding of the Poincare chart point (eta, x) into 5D Minkowski.
    Derived from X^+ = X4+X0 = -1/(H^2 eta), Xi = -x_i/(H eta),
    X^- = X4-X0 = -eta + x^2/eta  (standard, cf. Spradlin-Strominger-Volovich)."""
    xsq = xv[0] ** 2 + xv[1] ** 2 + xv[2] ** 2
    X0 = sp.Rational(1, 2) * (-1 / (H ** 2 * et) + et - xsq / et)
    X4 = sp.Rational(1, 2) * (-1 / (H ** 2 * et) - et + xsq / et)
    return [X0, -xv[0] / (H * et), -xv[1] / (H * et), -xv[2] / (H * et), X4]


def dot5(U, V):
    return -U[0] * V[0] + U[1] * V[1] + U[2] * V[2] + U[3] * V[3] + U[4] * V[4]


Xa = X_conf(eta, (x1, x2, x3))

# C1: hyperboloid constraint
c1 = zero_sym(dot5(Xa, Xa) - 1 / H ** 2)
check("C1  Poincare-chart embedding lies on the dS hyperboloid X.X = 1/H^2", c1)

# C2: induced metric is conformally flat with factor 1/(H eta)^2
qc = (eta, x1, x2, x3)
J = sp.Matrix([[sp.diff(Xa[M], q) for q in qc] for M in range(5)])
G5 = sp.diag(-1, 1, 1, 1, 1)
g_ind = sp.expand(J.T * G5 * J)
g_target = sp.diag(-1, 1, 1, 1) / (H * eta) ** 2
c2 = all(zero_sym(g_ind[i, j] - g_target[i, j]) for i in range(4) for j in range(4))
check("C2  induced metric = (1/(H eta))^2 diag(-1,1,1,1)  (conformally flat, "
      "correct factor)", c2)

# C3: chordal identity (DX)^2 = [ (Dx)^2 - (Deta)^2 ] / (H^2 eta eta')
Xb = X_conf(etap, (y1, y2, y3))
dX = [Xa[M] - Xb[M] for M in range(5)]
chord = dot5(dX, dX)
target3 = ((x1 - y1) ** 2 + (x2 - y2) ** 2 + (x3 - y3) ** 2
           - (eta - etap) ** 2) / (H ** 2 * eta * etap)
c3 = zero_sym(chord - target3)
check("C3  chordal identity (DX)^2 = [(Dx)^2 - (Deta)^2]/(H^2 eta eta')", c3)

# ---- static chart --------------------------------------------------------------
tS, rho, thS, phS = sp.symbols('t rho theta varphi', real=True)


def X_stat(t_, rho_, th_, ph_):
    r0 = sp.sqrt(1 / H ** 2 - rho_ ** 2)
    return [r0 * sp.sinh(H * t_),
            rho_ * sp.sin(th_) * sp.cos(ph_),
            rho_ * sp.sin(th_) * sp.sin(ph_),
            rho_ * sp.cos(th_),
            r0 * sp.cosh(H * t_)]


Xs = X_stat(tS, rho, thS, phS)
c4a = zero_sym(dot5(Xs, Xs) - 1 / H ** 2)
check("C4a static-chart embedding lies on the hyperboloid", c4a)

qs = (tS, rho, thS, phS)
Js = sp.Matrix([[sp.diff(Xs[M], q) for q in qs] for M in range(5)])
gs = sp.expand(Js.T * G5 * Js)
f = 1 - H ** 2 * rho ** 2
gs_target = sp.diag(-f, 1 / f, rho ** 2, rho ** 2 * sp.sin(thS) ** 2)
c4b = all(zero_sym(gs[i, j] - gs_target[i, j]) for i in range(4) for j in range(4))
check("C4b static induced metric = diag(-(1-H^2 rho^2), 1/(1-H^2 rho^2), rho^2, "
      "rho^2 sin^2 th)", c4b)

# ---- the circular worldline, layer-1 definitions -------------------------------
N1 = sp.sqrt(1 - H ** 2 * R ** 2 - R ** 2 * Om ** 2)
h1 = H / N1
w1 = Om / N1
A1 = sp.sqrt(1 - H ** 2 * R ** 2) / H          # = sqrt(1/H^2 - R^2)
N0 = sp.sqrt(1 - H ** 2 * R ** 2)

# worldline in the static chart, in PROPER time: t = tau/N, rho=R, th=pi/2, ph=Om tau/N
Xwl = [e.subs({tS: tau / N1, rho: R, thS: sp.pi / 2, phS: Om * tau / N1})
       for e in Xs]

print()
print("=" * 78)
print("S2  (b) EXACT COORDINATE TRANSFORMATION: the orbit in the conformal chart")
print("=" * 78)

Xp_wl = sp.simplify(Xwl[4] + Xwl[0])            # X^+ = X4 + X0
eta_wl = -1 / (H ** 2 * Xp_wl)                  # inverse map, eta(tau)
x1_wl = Xwl[1] / (H * Xp_wl)                    # inverse map, x_i(tau)
x2_wl = Xwl[2] / (H * Xp_wl)
x3_wl = Xwl[3] / (H * Xp_wl)

eta_closed = -sp.exp(-h1 * tau) / (H ** 2 * A1)
x1_closed = R * sp.exp(-h1 * tau) * sp.cos(w1 * tau) / (H * A1)
x2_closed = R * sp.exp(-h1 * tau) * sp.sin(w1 * tau) / (H * A1)

c5a = zero_sym(eta_wl - eta_closed)
check("C5a worldline in conformal chart: eta(tau) = -e^{-h tau}/(H^2 A)  (exact)", c5a)
c5b = (zero_sym(x1_wl - x1_closed) and zero_sym(x2_wl - x2_closed)
       and zero_sym(x3_wl))
check("C5b worldline in conformal chart: x(tau) = (R/(H A)) e^{-h tau} "
      "(cos w tau, sin w tau, 0)  (exact log-spiral)", c5b)
c5c = zero_sym(Xp_wl - A1 * sp.exp(h1 * tau))
check("C5c X^+ = A e^{h tau} > 0 for all tau: the WHOLE orbit sits inside the "
      "expanding Poincare patch", c5c)
deta = sp.diff(eta_closed, tau)
c5d = zero_sym(deta - h1 * sp.exp(-h1 * tau) / (H ** 2 * A1))
check("C5d d eta/d tau = +h e^{-h tau}/(H^2 A) > 0: eta increases with tau, so the "
      "flat-chart (Deta - i eps) prescription maps to s - i eps", c5d)

print()
print("=" * 78)
print("S3  (c) TWO-ROUTE WIGHTMAN COMPARISON along the orbit")
print("=" * 78)

# Layer-2 abstract symbols (A,h,w free positive; H^2 tied by A^2 = 1/H^2 - R^2,
# i.e. H^2 = 1/(A^2+R^2) -- assumption-free polynomial substitution).
Aq, Rq, hq, wq = sp.symbols('A_q R_q h_q w_q', positive=True)
Hq2 = 1 / (Aq ** 2 + Rq ** 2)                   # H^2
Hq = sp.sqrt(Hq2)


def eta_q(T):
    return -sp.exp(-hq * T) / (Hq2 * Aq)


def xq(T):
    return (Rq * sp.exp(-hq * T) * sp.cos(wq * T) / (Hq * Aq),
            Rq * sp.exp(-hq * T) * sp.sin(wq * T) / (Hq * Aq))


def a_conf(T):
    return -1 / (Hq * eta_q(T))                 # scale factor a(eta) = -1/(H eta)


x1a, x2a = xq(tau1)
x1b, x2b = xq(tau2)
Dconf = a_conf(tau1) * a_conf(tau2) * ((x1a - x1b) ** 2 + (x2a - x2b) ** 2
                                       - (eta_q(tau1) - eta_q(tau2)) ** 2)
Dgems_closed_q = (4 * Rq ** 2 * sp.sin(wq * (tau1 - tau2) / 2) ** 2
                  - 4 * Aq ** 2 * sp.sinh(hq * (tau1 - tau2) / 2) ** 2)
c6a = zero_sym(Dconf - Dgems_closed_q)
check("C6a CONFORMAL ROUTE == GEMS: a(eta)a(eta') [|Dx|^2 - Deta^2] = "
      "4R^2 sin^2(w s/2) - 4A^2 sinh^2(h s/2)  (exact, and depends on tau1,tau2 "
      "only through s = tau1-tau2: stationarity is manifest)", c6a)

# C6b: the GEMS chord computed directly from the static embedding, full layer-1
Xw1 = [e.subs(tau, tau1) for e in Xwl]
Xw2 = [e.subs(tau, tau2) for e in Xwl]
dXw = [Xw1[M] - Xw2[M] for M in range(5)]
Dgems_l1 = dot5(dXw, dXw)
Dclosed_l1_s12 = (4 * R ** 2 * sp.sin(w1 * (tau1 - tau2) / 2) ** 2
                  - 4 * A1 ** 2 * sp.sinh(h1 * (tau1 - tau2) / 2) ** 2)
c6b = zero_sym(Dgems_l1 - Dclosed_l1_s12)
check("C6b (DX)^2(s) = 4R^2 sin^2(w s/2) - 4A^2 sinh^2(h s/2) with A^2=1/H^2-R^2, "
      "h=H/N, w=Omega/N  -- the brief's interval formula, EXACT", c6b)

INTERVAL_CONFIRMED = bool(c6a and c6b)

print("     => W(s) = (a a')^{-1} W_flat = 1/(4 pi^2 (DX)^2(s - i eps)).")
print("        OVERALL CONSTANT from the conformal route: 1/(4 pi^2), sign such")
print("        that W -> -1/(4 pi^2 s^2) at s -> 0. No extra H- or N-dependent")
print("        factor. (Chordal form: W = H^2/(8 pi^2 (1-Z)), Z = H^2 X.X'.)")

print()
print("=" * 78)
print("S4  REQUIRED IDENTITIES (unit norm, 5-acceleration, GEMS split, series)")
print("=" * 78)

c7 = zero_sym(A1 ** 2 * h1 ** 2 - R ** 2 * w1 ** 2 - 1)
check("C7  A^2 h^2 - R^2 w^2 = 1  (4-velocity unit normalization)", c7)

u5 = [sp.diff(e, tau) for e in Xwl]
c8a = zero_sym(dot5(u5, u5) + 1)
check("C8a u.u = -1 along the worldline (proper-time parametrization exact)", c8a)

a5 = [sp.diff(e, tau, 2) for e in Xwl]
a5sq_target = A1 ** 2 * h1 ** 4 + R ** 2 * w1 ** 4
c8b = zero_sym(dot5(a5, a5) - a5sq_target)
check("C8b a5^2 = A^2 h^4 + R^2 w^4  (5-acceleration closed form)", c8b)

c9a = zero_sym(dot5(a5, Xwl) - 1)
check("C9a a5 . X = 1, i.e. the component of a5 along the unit normal n = H X is "
      "exactly H for this worldline (the GEMS normal split)", c9a)

# C9b: intrinsic dS proper acceleration from the 4D static metric (Christoffels)
g4 = sp.diag(-f, 1 / f, rho ** 2, rho ** 2 * sp.sin(thS) ** 2)
g4inv = g4.inv()
crd = [tS, rho, thS, phS]
Gam = [[[sp.Rational(1, 2) * sum(
    g4inv[m, k] * (sp.diff(g4[k, a], crd[b]) + sp.diff(g4[k, b], crd[a])
                   - sp.diff(g4[a, b], crd[k])) for k in range(4))
    for b in range(4)] for a in range(4)] for m in range(4)]
u4 = [1 / N1, 0, 0, Om / N1]
unorm = sum(g4[a, a] * u4[a] ** 2 for a in range(4)).subs({rho: R, thS: sp.pi / 2})
c9b_pre = zero_sym(unorm + 1)
acc4 = [sum(Gam[m][a][b] * u4[a] * u4[b] for a in range(4) for b in range(4))
        for m in range(4)]
a2_int = sum(g4[m, m] * acc4[m] ** 2 for m in range(4)).subs(
    {rho: R, thS: sp.pi / 2})
c9b = c9b_pre and zero_sym(a2_int - (a5sq_target - H ** 2))
check("C9b intrinsic a^2 (4D Christoffel computation) = a5^2 - H^2  "
      "(GEMS relation verified, not assumed; u4 normalized)", c9b)

a2_closed = (1 - H ** 2 * R ** 2) * R ** 2 * (H ** 2 + Om ** 2) ** 2 / N1 ** 4
c9c = zero_sym(a2_int - a2_closed)
check("C9c bonus closed form a^2 = (1-H^2R^2) R^2 (H^2+Omega^2)^2 / N^4, i.e. "
      "a = gamma_v^2 R (H^2+Omega^2)/N0", c9c)

# ---- short-proper-time expansion (I2 / Luo functional input) -------------------
Dclosed_l1 = (4 * R ** 2 * sp.sin(w1 * sR / 2) ** 2
              - 4 * A1 ** 2 * sp.sinh(h1 * sR / 2) ** 2)
ser = sp.series(Dclosed_l1, sR, 0, 8).removeO()
c2c = ser.coeff(sR, 2)
c4c = ser.coeff(sR, 4)
c6c = ser.coeff(sR, 6)
c10a = zero_sym(c2c + 1)
check("C10a series: s^2 coefficient = -1  (uses A^2h^2 - R^2w^2 = 1)", c10a)
c10b = zero_sym(c4c + a5sq_target / 12)
check("C10b series: s^4 coefficient = -a5^2/12, so (DX)^2 = -s^2[1 + a5^2 s^2/12 "
      "+ ...] with a5^2 = a^2 + H^2: the I2 functional is TORSION-BLIND at this "
      "order (h,w enter only via a5^2)", c10b)
c10c = zero_sym(c6c - (R ** 2 * w1 ** 6 - A1 ** 2 * h1 ** 6) / 360)
check("C10c series: s^6 coefficient = (R^2 w^6 - A^2 h^6)/360 -- the FIRST place "
      "torsion (h vs w separately) enters the short-time expansion", c10c)

print()
print("=" * 78)
print("S5  (d) KMS / DESER-LEVIN CHECK, symbolic part")
print("=" * 78)

h0 = H / N0
Dstat = -4 * (N0 ** 2 / H ** 2) * sp.sinh(h0 * sS / 2) ** 2
c11a = zero_sym(Dstat.subs(sS, sS + 2 * sp.pi * sp.I / h0) - Dstat)
check("C11a static (Omega=0) interval is periodic in imaginary proper time with "
      "period 2 pi/h0 = 2 pi N0/H  =>  KMS at T = H/(2 pi sqrt(1-H^2R^2)) "
      "(Deser-Levin 1997)", c11a)

print()
print("=" * 78)
print("S6  FLAT LIMIT H -> 0 (interval-level Letaw anchor, independently coded)")
print("=" * 78)

# independently coded flat-space circular interval: t = gamma_f s, |Dx|^2 =
# 4 R^2 sin^2(Omega Dt/2), gamma_f = 1/sqrt(1 - R^2 Omega^2)
gam_f = 1 / sp.sqrt(1 - R ** 2 * Om ** 2)
Dflat = 4 * R ** 2 * sp.sin(Om * gam_f * sR / 2) ** 2 - gam_f ** 2 * sR ** 2
try:
    Dlim = sp.limit(Dclosed_l1, H, 0, '+')
except Exception:
    Dlim = None
if Dlim is None:
    c15 = False
else:
    c15 = zero_sym(Dlim - Dflat)
check("C15 lim_{H->0} (DX)^2 = 4R^2 sin^2(Omega gamma s/2) - gamma^2 s^2, the "
      "flat circular interval of Letaw 1981 (coded independently from flat "
      "kinematics)", c15)

print()
print("=" * 78)
print("S7  EXACT PHYSICAL PARAMETRIZATION (v, a) <-> (R, Omega)")
print("=" * 78)

v_loc = R * Om / N0                      # local orbital speed wrt static observer
g2_loc = 1 / (1 - v_loc ** 2)
c16a = zero_sym(g2_loc ** 2 * v_loc ** 2 * (H ** 2 + Om ** 2) ** 2 / Om ** 2
                - a2_int)
check("C16a exact relation a = gamma_v^2 v (H^2 + Omega^2)/Omega  =>  Omega solves "
      "the QUADRATIC gamma_v^2 v Omega^2 - a Omega + gamma_v^2 v H^2 = 0", c16a)

c16c = zero_sym((((v_loc ** 2 / R) ** 2 / a2_int) - (1 - v_loc ** 2) ** 2
                 ).subs(H, 0))
check("C16c at H = 0: R = gamma_v^2 v^2/a and Omega = a/(gamma_v^2 v) EXACTLY -- "
      "so the brief's leading-order map R = v^2/a, Omega = a/v is correct with "
      "relative corrections O(v^2) (and O(H^2 v^2/a^2) at H > 0)", c16c)

print()
print("=" * 78)
print("S8  NUMERICS (mpmath): two-route cross-validation, KMS, normalization")
print("=" * 78)

mp.mp.dps = 60


def params_from_va(v, a, Hn=None):
    """EXACT inversion (v, a) -> (R, Omega): centripetal (+) branch of the
    quadratic gamma^2 v Om^2 - a Om + gamma^2 v H^2 = 0; R = v/sqrt(Om^2+v^2H^2).
    Exists iff a >= 2 gamma_v^2 v H (minimum proper acceleration at fixed v)."""
    Hn = mp.mpf(1) if Hn is None else Hn
    v, a = mp.mpf(v), mp.mpf(a)
    g2 = 1 / (1 - v ** 2)
    disc = a ** 2 - 4 * g2 ** 2 * v ** 2 * Hn ** 2
    if disc < 0:
        raise ValueError("a below the minimum 2 gamma^2 v H")
    Omn = (a + mp.sqrt(disc)) / (2 * g2 * v)
    Rn = v / mp.sqrt(Omn ** 2 + (v * Hn) ** 2)
    return params_from_ROm(Rn, Omn, Hn)


def params_from_ROm(Rn, Omn, Hn):
    N0n = mp.sqrt(1 - (Hn * Rn) ** 2)
    Nn = mp.sqrt(1 - (Hn * Rn) ** 2 - (Rn * Omn) ** 2)
    return dict(H=Hn, R=Rn, Om=Omn, N0=N0n, N=Nn, A=N0n / Hn,
                h=Hn / Nn, w=Omn / Nn)


def W_conf_num(P, t1, t2):
    """Conformal-route W: chart worldline + conformal factors + flat Wightman."""
    Hn, An, Rn, hn, wn = P['H'], P['A'], P['R'], P['h'], P['w']

    def et(T):
        return -mp.exp(-hn * T) / (Hn ** 2 * An)

    def xx(T):
        return (Rn * mp.exp(-hn * T) * mp.cos(wn * T) / (Hn * An),
                Rn * mp.exp(-hn * T) * mp.sin(wn * T) / (Hn * An))

    e1, e2 = et(t1), et(t2)
    af1, af2 = -1 / (Hn * e1), -1 / (Hn * e2)
    xa, xb = xx(t1), xx(t2)
    dx2 = (xa[0] - xb[0]) ** 2 + (xa[1] - xb[1]) ** 2
    D = af1 * af2 * (dx2 - (e1 - e2) ** 2)
    return 1 / (4 * mp.pi ** 2 * D)


def W_gems_num(P, t1, t2):
    """GEMS-route W: raw 5D chord of the static-chart embedding."""
    An, Rn, hn, wn = P['A'], P['R'], P['h'], P['w']
    d0 = An * (mp.sinh(hn * t1) - mp.sinh(hn * t2))
    d1 = Rn * (mp.cos(wn * t1) - mp.cos(wn * t2))
    d2 = Rn * (mp.sin(wn * t1) - mp.sin(wn * t2))
    d4 = An * (mp.cosh(hn * t1) - mp.cosh(hn * t2))
    D = -d0 ** 2 + d1 ** 2 + d2 ** 2 + d4 ** 2
    return 1 / (4 * mp.pi ** 2 * D)


def W_closed_num(P, s):
    """The closed form handed to the compute lane, verbatim."""
    An, Rn, hn, wn = P['A'], P['R'], P['h'], P['w']
    D = (4 * Rn ** 2 * mp.sin(wn * s / 2) ** 2
         - 4 * An ** 2 * mp.sinh(hn * s / 2) ** 2)
    return 1 / (4 * mp.pi ** 2 * D)


# C16b: exact-inversion round trip
ok16b = True
det16b = []
for (vv, aa) in [('1e-4', '1e-2'), ('1e-4', '1e3'), ('1e-3', '1'),
                 ('1e-3', '1e3'), ('0.3', '2.5')]:
    P = params_from_va(vv, aa)
    v_back = P['R'] * P['Om'] / P['N0']
    a_gems = mp.sqrt(P['A'] ** 2 * P['h'] ** 4 + P['R'] ** 2 * P['w'] ** 4
                     - P['H'] ** 2)
    a_clsd = P['N0'] * P['R'] * (P['H'] ** 2 + P['Om'] ** 2) / P['N'] ** 2
    e1 = rel(v_back, mp.mpf(vv))
    e2 = rel(a_gems, mp.mpf(aa))
    e3 = rel(a_clsd, mp.mpf(aa))
    ok16b &= (e1 < mp.mpf('1e-50') and e2 < mp.mpf('1e-50')
              and e3 < mp.mpf('1e-50'))
    det16b.append(float(max(e1, e2, e3)))
check("C16b numeric round trip (v,a)->(R,Omega)->(v,a) at 5 grid points incl. "
      "v=1e-4..0.3, a/H=1e-2..1e3, both a-formulas", ok16b,
      f"max rel err {max(det16b):.1e}")

# C13: two-route cross-validation of W at grid corners, complex s, plus
# numeric stationarity (tau0-independence)
ok13 = True
worst13 = mp.mpf(0)
for (vv, aa) in [('1e-4', '1e-2'), ('1e-4', '1e3'), ('1e-3', '1'),
                 ('1e-3', '1e3'), ('0.3', '2.5')]:
    P = params_from_va(vv, aa)
    wv = P['w']
    s_list = [mp.mpc(mp.mpf('0.6'), -mp.mpf('0.2') / wv),
              mp.mpc(mp.mpf('2.3'), -mp.mpf('0.7')) / wv,
              mp.mpc(mp.mpf('0.85'), 0)]
    for s in s_list:
        for t0 in [mp.mpf(0), mp.mpf('1.3')]:
            Wc = W_conf_num(P, t0 + s, t0)
            Wg = W_gems_num(P, t0 + s, t0)
            Wl = W_closed_num(P, s)
            worst13 = max(worst13, rel(Wc, Wg), rel(Wc, Wl))
            ok13 &= (rel(Wc, Wg) < mp.mpf('1e-40')
                     and rel(Wc, Wl) < mp.mpf('1e-40'))
check("C13 numeric: conformal-route W == GEMS-route W == closed form, 5 params x "
      "3 complex s x 2 worldline offsets (stationarity), dps 60", ok13,
      f"worst rel diff {mp.nstr(worst13, 3)}")

# C11b/C11c/C12: KMS in the conformal chart
mp.mp.dps = 50
Pstat = params_from_ROm(mp.mpf('0.6'), mp.mpf(0), mp.mpf(1))
beta_DL = 2 * mp.pi * Pstat['N0'] / Pstat['H']          # Deser-Levin period
beta_naive = 2 * mp.pi / Pstat['H']                      # WRONG: Tolman factor absent
okb = True
worstb = mp.mpf(0)
gapw = mp.inf
for s in [mp.mpc('0.7', '-0.3'), mp.mpc('1.9', '-1.1'), mp.mpc('0.25', '-2.0')]:
    t0 = mp.mpf('0.4')
    W1 = W_conf_num(Pstat, t0 + s, t0)
    W2 = W_conf_num(Pstat, t0 + s - 1j * beta_DL, t0)
    W3 = W_conf_num(Pstat, t0 + s - 1j * beta_naive, t0)
    worstb = max(worstb, rel(W1, W2))
    gapw = min(gapw, rel(W1, W3))
    okb &= rel(W1, W2) < mp.mpf('1e-40')
check("C11b numeric KMS in the conformal chart: W(s - i 2piN0/H) = W(s) at R=0.6 "
      "(Omega=0), several complex s", okb, f"worst rel diff {mp.nstr(worstb, 3)}")
check("C11b' control (test has teeth): the naive period 2pi/H WITHOUT the Tolman "
      "factor FAILS", gapw > mp.mpf('1e-2'),
      f"min rel diff {mp.nstr(gapw, 3)} >> 0")

# C11c: R=0 pipeline reproduces the known Gibbons-Hawking thermal form
P0 = params_from_ROm(mp.mpf(0), mp.mpf(0), mp.mpf(1))
okc = True
worstc = mp.mpf(0)
for s in [mp.mpc('0.8', '-0.4'), mp.mpc('2.1', '-1.7')]:
    Wp = W_conf_num(P0, s, mp.mpf(0))
    Wth = -(P0['H'] ** 2 / (16 * mp.pi ** 2)) / mp.sinh(P0['H'] * s / 2) ** 2
    worstc = max(worstc, rel(Wp, Wth))
    okc &= rel(Wp, Wth) < mp.mpf('1e-40')
check("C11c R=0 limit of the conformal pipeline = -(H^2/16pi^2)/sinh^2(Hs/2), the "
      "Gibbons-Hawking thermal Wightman at T=H/2pi (normalization pinned)", okc,
      f"worst rel diff {mp.nstr(worstc, 3)}")

# C12: the ROTATING worldline is NOT iota-beta periodic for any of the candidate
# periods => strict KMS/thermality is broken by rotation (as in Letaw's flat case)
Prot = params_from_ROm(mp.mpf('0.3'), mp.mpf('1.1'), mp.mpf(1))
cands = [2 * mp.pi * Prot['N0'] / Prot['H'], 2 * mp.pi / Prot['h'],
         2 * mp.pi / Prot['H']]
s = mp.mpc('0.7', '-0.3')
gaps = []
for b in cands:
    W1 = W_conf_num(Prot, s, mp.mpf(0))
    W2 = W_conf_num(Prot, s - 1j * b, mp.mpf(0))
    gaps.append(rel(W1, W2))
ok12 = all(g > mp.mpf('1e-2') for g in gaps)
check("C12 control: with Omega != 0 NO candidate imaginary period (2piN0/H, "
      "2pi/h, 2pi/H) restores periodicity -- the orbital W is non-thermal in the "
      "strict KMS sense; T_eff(E) can only be an E-dependent effective quantity",
      ok12, "rel diffs " + ", ".join(mp.nstr(g, 2) for g in gaps))

# C14: overall constant -- s^2 W(s) -> -1/(4 pi^2) as s -> 0 (conformal pipeline)
mp.mp.dps = 80
P = params_from_va('1e-3', '1')
s = mp.mpf('1e-12')
val_c = 4 * mp.pi ** 2 * s ** 2 * W_conf_num(P, s, mp.mpf(0))
val_g = 4 * mp.pi ** 2 * s ** 2 * W_gems_num(P, s, mp.mpf(0))
ok14 = (mp.fabs(val_c + 1) < mp.mpf('1e-20')
        and mp.fabs(val_g + 1) < mp.mpf('1e-20'))
check("C14 normalization: 4 pi^2 s^2 W(s) -> -1 as s -> 0 on BOTH routes (the "
      "constant is exactly 1/(4 pi^2), Hadamard-normalized)", ok14,
      f"|4pi^2 s^2 W + 1| = {mp.nstr(mp.fabs(val_c + 1), 3)}")

print()
print("=" * 78)
print("REPORT -- verified closed forms for the compute lane")
print("=" * 78)
print("""
  worldline (static chart, proper time tau):  t = tau/N, rho = R, theta = pi/2,
      phi = Omega tau / N,   N = sqrt(1 - H^2 R^2 - R^2 Omega^2)
  worldline (conformal chart, EXACT):
      eta(tau) = -e^{-h tau}/(H^2 A),   x(tau) = (R/(H A)) e^{-h tau}
                 (cos w tau, sin w tau, 0),   a(eta) = -1/(H eta) = H A e^{h tau}
      (entire orbit inside the expanding Poincare patch; d eta/d tau > 0)

  interval:   (DX)^2(s) = 4 R^2 sin^2(w s/2) - 4 A^2 sinh^2(h s/2)
              A = sqrt(1/H^2 - R^2),  h = H/N,  w = Omega/N          [CONFIRMED]
  Wightman:   W(s) = 1/(4 pi^2 (DX)^2(s - i eps))     <- overall constant 1/4pi^2,
              W -> -1/(4 pi^2 s^2) as s -> 0; no extra H- or N-dependent factor.
  identities: A^2 h^2 - R^2 w^2 = 1;   a5^2 = A^2 h^4 + R^2 w^4;
              a^2 = a5^2 - H^2  (GEMS normal component = H, verified by 4D
              Christoffel computation);  a = gamma_v^2 R (H^2+Omega^2)/N0.
  short time: (DX)^2 = -s^2 [1 + (a5^2/12) s^2 + ((A^2h^6 - R^2w^6)/360) s^4]
              + O(s^8)   -- s^4-in-bracket term is where torsion first enters;
              the s^2-in-bracket term depends ONLY on a5^2 = a^2 + H^2
              (I2/second-moment functional is torsion-blind at leading order).
  KMS:        Omega = 0  =>  W periodic in imaginary s, period 2 pi N0/H
              =>  T = H/(2 pi sqrt(1 - H^2 R^2))  (Deser-Levin / Tolman-GH).
              Omega != 0  =>  NOT periodic for any candidate period.
  EXACT physical parametrization (replaces leading-order R = v^2/a, Omega = a/v):
      gamma_v^2 = 1/(1 - v^2),  v = R Omega/sqrt(1 - H^2 R^2)
      Omega = [ a + sqrt(a^2 - 4 gamma_v^4 v^2 H^2) ] / (2 gamma_v^2 v)
      R     = v / sqrt(Omega^2 + v^2 H^2)
      valid iff a >= 2 gamma_v^2 v H (minimum proper acceleration at fixed v);
      the '+' root is the centripetal branch (R ~ v^2/a); the '-' root is a
      second, dS-dominated branch (R ~ a/H^2) -- the compute lane must use '+'.
""")

dt = time.time() - T0
print(f"SUMMARY: {NPASS[0]}/{NTOT[0]} checks passed in {dt:.1f} s")
if NPASS[0] != NTOT[0]:
    print("RESULT: FAIL")
    sys.exit(1)
print("RESULT: PASS -- conformal route and GEMS route agree exactly; interval "
      "formula, identities, KMS/Deser-Levin all confirmed")
sys.exit(0)
