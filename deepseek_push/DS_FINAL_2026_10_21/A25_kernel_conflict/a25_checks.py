#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A25 -- THE KERNEL CONFLICT: WHICH INTERPOLATION FUNCTION IS THE THEORY'S, AND WHICH ONES CLOSE Lambda
=====================================================================================================

THE CONFLICT (A5 tension 1).  Zenodo 23251231 states the dark energy is the vacuum energy of the MOND field,
        Lambda c^4/a0^2 = (1/2) Int (nu-1) d(y^2) = Int y (nu-1) dy = 73.19   (observed),
and that "with the RAR kernel the integral converges to 12.99, 5.6 times below".  Zenodo 23171085 states the
quadrature kernel closes with y_t = 94-129.  But the framework's action (A12 sec. 5, verified residual 0) gives
the Langmuir/simple kernel nu = (1+sqrt(1+4/y))/2, and A4 computed that it closes at y_t = 100.40 with a linear
divergence pi/2 per unit y_t.  No repo file states which kernel is canonical.

WHAT THIS FILE COMPUTES
  K1  the four kernels and their exact identities (action -> Langmuir; parametric pair -> RAR; q_P2 -> quadrature)
  K2  the tail coefficient c = lim y(nu-1)  (1, 1/2, 0, divergent) -- this is what decides convergence
  K3  the bare integral I_bare(Y) = Int_0^Y y(nu-1)dy, exact and asymptotic, and the divergence exponent
  K4  the turn-off integral I_turn(y_t) = Int_0^inf y(nu-1)/(1+(y/y_t)^2) dy, exact rational forms + asymptotics
  K5  the y_t that makes each kernel equal 73.19 (and RAR: proof that none exists)
  K6  the record's 94-129 band = the quadrature kernel at its two a0 normalisations
  K7  12.99 = 2 pi^4/15 exactly; 5.6x = 73.19/(2 pi^4/15)
  K8  the target bookkeeping: 32 pi = 3 Z^2, 73.19 = 32 pi Omega_Lambda
  K9  SPARC (on disk) fixed-footing Delta chi^2 for all four kernels
  K10 SPARC with (amplitude, a0) profiled -- the fair kernel-shape test
  K11 whether the Lambda-required turn-off is visible in the RAR (it is not)
  K12 the Solar-System coefficient c*a0 against the Earth bound, and the planetary cap on y_t
  K13 the KiDS-1000 lensing RAR (on disk): a null result for kernel separation
  K14 the canonical kernel is the action's kernel (mutation hook)

Run:  python3 a25_checks.py            (exit 0 iff every check passes)
      python3 a25_checks.py --mutate   (canonical kernel := quadrature; K5, K9, K10, K14 must FAIL)
"""
import os, sys, json, math, argparse
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "hunt_2026"))

MUTATE = "--mutate" in sys.argv
CHECKS = []
NUM = {}


def check(cid, ok, measured, threshold, note=""):
    ok = bool(ok)
    CHECKS.append({"id": cid, "pass": ok, "value": measured, "threshold": threshold})
    print("  %-4s %s %s" % (cid, "PASS" if ok else "FAIL", measured))
    print("        threshold: %s" % threshold)
    if note:
        print("        %s" % note)
    return ok


def banner(t):
    print("\n" + "=" * 104)
    print(t)
    print("=" * 104)


# ------------------------------------------------------------------ constants (BRIEF sec. 4, all labelled external)
C_LIGHT = 2.99792458e8
G_N = 6.67430e-11
LAMBDA = 1.0890e-52
A0_CAN = 9.36e-11
A0_ALT = 1.13e-10
Z_SCALE = 2.0 * math.sqrt(8.0 * math.pi / 3.0)            # 5.78881 = 2 sqrt(8 pi/3)
TARGET = mp.mpf("73.19")                                   # Zenodo 23251231, external
TARGET_32PI = 32 * mp.pi                                   # = Lambda c^4/a0^2 under a0 = c^2 sqrt(Lambda/32 pi)
TARGET_A4 = mp.mpf("100.405845")                           # A4 a4_results.json, from BRIEF constants
B_EARTH = 3.66e-14                                         # A4: Earth 2 sigma bound on a constant radial anomaly
Y_T_NEPTUNE = 605.96                                       # A4: tightest planetary cap (over-tight stand-in)

print("=" * 104)
print("A25 -- THE KERNEL CONFLICT" + ("   [MUTATE: canonical kernel := quadrature]" if MUTATE else ""))
print("=" * 104)
print("  external inputs: Lambda = %.4e m^-2, a0_can = %.3e, a0_alt = %.3e, c = %.8e" % (LAMBDA, A0_CAN, A0_ALT, C_LIGHT))
print("  target (Zenodo 23251231): Lambda c^4/a0^2 = 73.19   [external, not recomputed]")

# ==================================================================================== K1  the four kernels
banner("K1  THE FOUR KERNELS AND THEIR EXACT IDENTITIES")

y = sp.symbols("y", positive=True)
u = sp.symbols("u", positive=True)
Z = sp.symbols("Z", positive=True)

nu_L = (1 + sp.sqrt(1 + 4 / y)) / 2                        # Langmuir / simple  (the action's)
nu_Q = sp.sqrt(1 + 1 / y)                                  # quadrature (P2)
nu_R = 1 / (1 - sp.exp(-sp.sqrt(y)))                       # RAR / exponential (McGaugh et al.)

# (a) Langmuir is the exact inverse of mu(x) = x/(1+x), i.e. of g_N = g^2/(g+a0)
x = sp.symbols("x", positive=True)
g = sp.symbols("g", positive=True)
a0 = sp.symbols("a0", positive=True)
res_a = sp.simplify(g * (g / a0) / (1 + g / a0) - g**2 / (g + a0))
# (b) Langmuir is the gradient branch of W_full(u) = (a0^2/K)[-u/a0 - ln(1-u/a0)]: K W' = a0 u/(a0-u), g_N = g-u
Wp = a0 * u / (a0 - u)
g_sol = sp.solve(sp.Eq(Wp - u, sp.Symbol("gN")), u)         # invert g_N = u^2/(a0-u)
res_b = sp.simplify((nu_L - (1 + sp.sqrt(1 + 4 * a0 / sp.Symbol("gN"))) / 2))
# verify g = (gN/2)(1+sqrt(1+4a0/gN)) is the root of g^2 - gN g - a0 gN = 0
res_b2 = sp.simplify((sp.Symbol("gN") / 2 * (1 + sp.sqrt(1 + 4 * a0 / sp.Symbol("gN"))))**2
                     - sp.Symbol("gN") * (sp.Symbol("gN") / 2 * (1 + sp.sqrt(1 + 4 * a0 / sp.Symbol("gN"))))
                     - a0 * sp.Symbol("gN"))
# (c) RAR is exactly the parametric pair mu(u) = 1-e^-u, x(u) = u^2/mu(u), u = sqrt(y)
mu_u = 1 - sp.exp(-u)
x_u = u**2 / mu_u
res_c = sp.simplify((x_u / (u**2)) - 1 / (1 - sp.exp(-u)))
res_c2 = sp.simplify(sp.expand(res_c))
# (d) quadrature is exactly q_P2'(Z) = nu_Q(sqrt Z) - 1 with FP1's q_P2 (written with Z = s^2)
s = sp.symbols("s", positive=True)
qP2 = ((2 * s + 1) / 2) * sp.sqrt(s**2 + s) - sp.Rational(1, 4) * sp.log(
    2 * s + 1 + 2 * sp.sqrt(s**2 + s)) - s**2
res_d = sp.simplify(sp.together(sp.diff(qP2, s) / (2 * s) - (sp.sqrt(1 + 1 / s) - 1)))
kc = max(abs(float(res_a)), abs(float(res_b2)), abs(float(res_c2)), abs(float(res_d)))
print("    symbolic residuals: Langmuir<->mu (%.1e), Langmuir action branch (%.1e), RAR parametric pair (%.1e),"
      % (float(abs(res_a)), float(abs(res_b2)), float(abs(res_c2))))
print("                         quadrature<-q_P2 (%.1e)" % float(abs(res_d)))
check("K1", kc < 1e-25, "max symbolic residual = %.2e over 4 kernel identities" % kc,
      "max residual < 1e-25 (sympy exact)")
NUM["K1_max_symbolic_residual"] = kc

# numerical definitions (float, used everywhere below)
def nuL(yv):
    yv = np.maximum(np.asarray(yv, float), 1e-300)
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / yv))

def nuQ(yv):
    yv = np.maximum(np.asarray(yv, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / yv)

def nuR(yv):
    yv = np.maximum(np.asarray(yv, float), 1e-300)
    return 1.0 / (-np.expm1(-np.sqrt(yv)))

# nu_mono: L340's filtered splice, exactly as FP1_static_sector.py:132-143 builds it
Y_P = 2.5396382826332706   # L340 A1
H_P = 0.647610237891915    # L340 A1
DELTA = 0.05               # L340 A1
Y_STAR = 2.3374124053      # XC4 S2 (closed form)
H_STAR = Y_STAR / math.expm1(math.sqrt(Y_STAR))

def hR(yv):
    yv = np.maximum(np.asarray(yv, float), 1e-300)
    return yv / np.expm1(np.sqrt(np.minimum(yv, 1e4)))   # clipped where it underflows to 0 anyway

def hM(yv):
    yv = np.maximum(np.asarray(yv, float), 1e-14)
    return np.where(yv <= Y_STAR, hR(yv), H_STAR + DELTA * H_P * np.log((yv + Y_P) / (Y_STAR + Y_P)))

def nuM(yv):
    yv = np.maximum(np.asarray(yv, float), 1e-14)
    return 1.0 + hM(yv) / yv

KER = {"L": (nuL, "Langmuir/simple (the action's)"), "Q": (nuQ, "quadrature (P2)"),
       "R": (nuR, "RAR/exponential"), "M": (nuM, "nu_mono (L340 splice)")}
CANON = "Q" if MUTATE else "L"     # <- the one mutation: pretend the record's kernel is the canonical one

print("\n    nu(y) on the range that matters (y = g_N/a0):")
print("    %8s %12s %12s %12s %12s" % ("y", "nu_L", "nu_Q", "nu_R", "nu_M"))
for yv in (0.01, 0.1, 1.0, 10.0, 100.0, 1e4):
    print("    %8.2f %12.6f %12.6f %12.6f %12.6f" % (yv, nuL(yv), nuQ(yv), nuR(yv), nuM(yv)))
NUM["kernel_table"] = {str(yv): {"L": float(nuL(yv)), "Q": float(nuQ(yv)), "R": float(nuR(yv)), "M": float(nuM(yv))}
                       for yv in (0.01, 0.1, 1.0, 10.0, 100.0, 1e4)}

# pairwise maximum separation in dex -- the size of the target the RAR has to resolve (scatter 0.06 dex)
yy = np.logspace(-3, 3, 200001)
print("\n    pairwise |dlog10 nu| over y in [1e-3, 1e3]:")
SEP = {}
for na, nb in (("L", "Q"), ("L", "R"), ("Q", "R"), ("M", "R"), ("M", "L")):
    dd = np.abs(np.log10(KER[na][0](yy) / KER[nb][0](yy)))
    i = int(np.argmax(dd))
    SEP["%s_%s" % (na, nb)] = {"max_dex": float(dd[i]), "at_y": float(yy[i])}
    print("      %s vs %s: %.5f dex at y = %.3f   (nu ratio %.4f)" % (na, nb, dd[i], yy[i], KER[na][0](yy[i]) / KER[nb][0](yy[i])))
print("    validation of nu_mono: max |log10(nu_M/nu_R)| = %.8f at y = %.4f   (L340 A1 stores 0.0103700578 at 14.35)"
      % (SEP["M_R"]["max_dex"], SEP["M_R"]["at_y"]))
NUM["kernel_separation"] = SEP

# ==================================================================================== K2  tail coefficient
banner("K2  THE TAIL COEFFICIENT c = lim_{y->inf} y(nu-1)  --  THIS DECIDES CONVERGENCE")
cL = mp.mpf(1)
cQ = mp.mpf(1) / 2
cR = mp.mpf(0)
hL8 = float(mp.mpf(1e8) * (mp.sqrt(1 + 4 / mp.mpf(1e8)) / 2 + mp.mpf(1) / 2 - 1))
hQ8 = float(mp.mpf(1e8) * (mp.sqrt(1 + 1 / mp.mpf(1e8)) - 1))
hR4 = float(hR(1e4))
cM_inc = float((hM(1e12) - hM(1e6)) / math.log(1e6))   # h_M = h0 + delta*h_p*ln y  ->  increment isolates delta*h_p
print("    c_L = %.12f (exact 1)      c_Q = %.12f (exact 1/2)" % (hL8, hQ8))
print("    c_R = h(1e4) = %.3e  (exponential decay: e^{-sqrt y})" % hR4)
print("    c_M: [h(1e12)-h(1e6)]/ln(1e6) = %.8f   (delta*h_p = %.8f)  -> h_M diverges as ln y" % (cM_inc, DELTA * H_P))
# the other coefficient: the deep-MOND additive term  beta = lim_{y->0} (nu - y^-1/2),  g = sqrt(a0 g_N) + beta*a0*sqrt(y)
ye = 1e-8
beta = {}
for k, (f, _) in KER.items():
    beta[k] = float(f(ye) - 1.0 / math.sqrt(ye))
print("    deep coefficient beta = lim (nu - y^-1/2) at y = 1e-8:  L %.6f | Q %.2e | R %.6f | M %.6f  (exact 1/2, 0, 1/2, 1/2)"
      % (beta["L"], beta["Q"], beta["R"], beta["M"]))
ok2 = (abs(hL8 - 1) < 1e-6 and abs(hQ8 - 0.5) < 1e-6 and hR4 < 1e-3
       and abs(cM_inc - DELTA * H_P) < 1e-4 and abs(beta["L"] - 0.5) < 1e-3 and abs(beta["Q"]) < 1e-3
       and abs(beta["R"] - 0.5) < 1e-3)
check("K2", ok2, "c = (1, 0.5, 0.0, ln-div): %.9f, %.9f, %.2e, %.8f ; beta = (0.5, 0, 0.5, 0.5): %.5f, %.1e, %.5f, %.5f"
      % (hL8, hQ8, hR4, cM_inc, beta["L"], beta["Q"], beta["R"], beta["M"]),
      "c to 1e-6 / 1e-4; beta(L,Q,R) to 1e-3")
NUM["tail_c"] = {"L": hL8, "Q": hQ8, "R": hR4, "M_log_increment": cM_inc, "delta_hp": DELTA * H_P}
NUM["deep_beta"] = beta

# ==================================================================================== K3  bare integral
banner("K3  THE BARE INTEGRAL  I_bare(Y) = Int_0^Y y(nu-1) dy  (the integral the record writes as (1/2)Int(nu-1)d(y^2))")
Ysym = sp.symbols("Y", positive=True)
hL_s = sp.simplify(y * (nu_L - 1))
hQ_s = sp.simplify(y * (nu_Q - 1))
IL_s = sp.integrate(hL_s, (y, 0, Ysym))
IQ_s = sp.integrate(hQ_s, (y, 0, Ysym))
print("    exact antiderivative, Langmuir :  I_L(Y) =", sp.simplify(IL_s))
print("    exact antiderivative, quadrature:  I_Q(Y) =", sp.simplify(IQ_s))
IL_f = sp.lambdify(Ysym, IL_s, "mpmath")
IQ_f = sp.lambdify(Ysym, IQ_s, "mpmath")
compact_L = ((Ysym + 2) * sp.sqrt(Ysym**2 + 4 * Ysym) - Ysym**2) / 4 - sp.log((Ysym + 2 + sp.sqrt(Ysym**2 + 4 * Ysym)) / 2)
compact_Q = ((2 * Ysym + 1) * sp.sqrt(Ysym**2 + Ysym) - 2 * Ysym**2) / 4 - sp.log(sp.sqrt(Ysym + 1) + sp.sqrt(Ysym)) / 4
cLf = sp.lambdify(Ysym, compact_L, "mpmath")
cQf = sp.lambdify(Ysym, compact_Q, "mpmath")
print("    compact form,  Langmuir :  I_L(Y) = [(Y+2)sqrt(Y^2+4Y) - Y^2]/4 - ln[(Y+2+sqrt(Y^2+4Y))/2]")
print("    compact form, quadrature:  I_Q(Y) = [(2Y+1)sqrt(Y^2+Y) - 2Y^2]/4 - ln[sqrt(Y+1)+sqrt(Y)]/4")
rel_compact = max(abs(float(cLf(mp.mpf(1e5)) / IL_f(mp.mpf(1e5)) - 1)), abs(float(cQf(mp.mpf(1e5)) / IQ_f(mp.mpf(1e5)) - 1)))
print("    compact vs sympy antiderivative at Y = 1e5: max rel %.1e  (double-precision evaluation; the identity is"
      " acosh z = ln(z+sqrt(z^2-1)))" % rel_compact)
IR_inf = 2 * sp.gamma(4) * sp.zeta(4)
print("    exact, RAR    :  I_R(inf) = 2*Gamma(4)*zeta(4) =", sp.simplify(IR_inf), "= 2*pi^4/15 =", float(2 * sp.pi**4 / 15))
print("                     (substituting y = u^2 turns Int y/(e^sqrt y - 1) dy into 2 Int u^3/(e^u - 1) du)")
print("    exact, nu_mono:  diverges (h_M -> delta*h_p*ln y, so Int h_M dy ~ delta*h_p*Y ln Y)")
# numeric certification of the closed forms against adaptive quadrature
mp.mp.dps = 30
def Ibare_num(hfun, Yv):
    Yv = mp.mpf(Yv)                       # Int_0^Y h(y) dy, finite by construction
    pts = [0, mp.mpf("0.5"), mp.mpf("1"), mp.mpf("10"), Yv / 4, Yv / 2, Yv]
    return mp.quad(lambda yy: hfun(yy), pts)

hLm = lambda yy: mp.mpf(yy) * (mp.sqrt(1 + 4 / mp.mpf(yy)) / 2 + mp.mpf(1) / 2 - 1)
hQm = lambda yy: mp.mpf(yy) * (mp.sqrt(1 + 1 / mp.mpf(yy)) - 1)
rel_err = []
for Yv in (1e3, 1e6):
    rel_err.append(abs(float(IL_f(mp.mpf(Yv)) - Ibare_num(hLm, Yv)) / float(IL_f(mp.mpf(Yv)))))
    rel_err.append(abs(float(IQ_f(mp.mpf(Yv)) - Ibare_num(hQm, Yv)) / float(IQ_f(mp.mpf(Yv)))))
print("    closed form vs adaptive quadrature at Y = 1e3, 1e6: max rel %.2e" % max(rel_err))
# divergence exponent from the exact closed forms
gL = float((IL_f(mp.mpf(1e8)) - IL_f(mp.mpf(1e6))) / (1e8 - 1e6))
gQ = float((IQ_f(mp.mpf(1e8)) - IQ_f(mp.mpf(1e6))) / (1e8 - 1e6))
print("    incremental slope dI/dY: L %.9f (->1), Q %.9f (->1/2)" % (gL, gQ))
print("    I_L(1e8) - 1e8 + ln(1e8) = %.9f   (constant 1/2)" % float(IL_f(mp.mpf(1e8)) - mp.mpf(1e8) + mp.log(mp.mpf(1e8))))
print("    I_Q(1e8) - 5e7 + ln(1e8)/8 = %.9f (constant -0.1107868)" % float(IQ_f(mp.mpf(1e8)) - mp.mpf(5e7) + mp.log(mp.mpf(1e8)) / 8))
ok3 = (max(rel_err) < 1e-9 and abs(gL - 1) < 1e-6 and abs(gQ - 0.5) < 1e-6
       and sp.simplify(IR_inf - 2 * sp.pi**4 / 15) == 0 and rel_compact < 1e-10)
check("K3", ok3, "closed forms certified: max rel %.1e (quad), %.1e (compact); dI/dY = %.9f (L), %.9f (Q); I_R(inf) = %.12f" % (max(rel_err), rel_compact, gL, gQ, float(IR_inf)),
      "rel<1e-9 vs quadrature, <1e-10 compact; slopes 1 and 1/2 to 1e-6; I_R = 2pi^4/15 exactly")
NUM["I_bare"] = {"I_L_exact_at_1e8": float(IL_f(mp.mpf(1e8))), "I_Q_exact_at_1e8": float(IQ_f(mp.mpf(1e8))),
                 "dIdY_L": gL, "dIdY_Q": gQ, "I_R_inf": float(IR_inf), "two_pi4_over_15": float(2 * sp.pi**4 / 15),
                 "rel_err_closed_form": max(rel_err), "rel_err_compact": rel_compact,
                 "C_L_asymptotic": 0.5, "C_Q_asymptotic": -0.1107867951}

# ==================================================================================== K4  turn-off integral
banner("K4  THE TURN-OFF INTEGRAL  I_turn(y_t) = Int_0^inf y(nu-1)/(1+(y/y_t)^2) dy")

def FL_rat(Yv):     # A4 eq (11): v = sqrt(y^2+4y)-y  (y:0..inf <-> v:0..2)
    Yv = mp.mpf(Yv)
    return mp.quad(lambda v: Yv**2 * v**2 * (4 - v) / (4 * Yv**2 * (2 - v)**2 + v**4), [0, 2])

def FQ_rat(Yv):     # v = sqrt(y^2+y)-y  (y:0..inf <-> v:0..1/2)
    Yv = mp.mpf(Yv)
    return mp.quad(lambda v: 2 * Yv**2 * v**2 * (1 - v) / (Yv**2 * (1 - 2 * v)**2 + v**4), [0, mp.mpf(1) / 2])

def Fturn(hfun, Yv):
    """Int_0^inf h(y)/(1+(y/Y)^2) dy with y = Y tan t; the t -> pi/2 tail is O(1e-12)."""
    Yv = mp.mpf(Yv)
    return mp.quad(lambda t: hfun(Yv * mp.tan(t)) * Yv,
                   [0, mp.pi / 4, mp.pi / 2 - mp.mpf("1e-6"), mp.pi / 2 - mp.mpf("1e-12")])

def FR_turn(Yv):
    """RAR with turn-off, exactly: 2 Int_0^inf u^3 du /((e^u-1)(1+u^4/Y^2)), u = sqrt(y). No overflow."""
    Yv = mp.mpf(Yv)
    return 2 * mp.quad(lambda uu: uu**3 / (mp.expm1(uu) * (1 + uu**4 / Yv**2)), [0, 1, 5, 15, 40, 80])

hRm = lambda yy: mp.mpf(yy) / mp.expm1(mp.sqrt(mp.mpf(yy)))
def hMm(yy):
    yy = mp.mpf(yy)
    if yy <= 0:
        return mp.mpf(0)
    if yy <= Y_STAR:
        return yy / mp.expm1(mp.sqrt(yy))
    return H_STAR + DELTA * H_P * mp.log((yy + Y_P) / (Y_STAR + Y_P))

rel4 = []
for Yv in (20, 50, 100):
    rel4.append(abs(float(FL_rat(Yv) - Fturn(hLm, Yv)) / float(FL_rat(Yv))))
    rel4.append(abs(float(FQ_rat(Yv) - Fturn(hQm, Yv)) / float(FQ_rat(Yv))))
print("    exact rational form vs direct quadrature (y_t = 20, 50, 100): max rel %.2e" % max(rel4))
# asymptotic closed forms
Y100 = mp.mpf(100)
asL = mp.pi / 2 * Y100 - mp.log(Y100) + mp.mpf(1) / 2
asQ = mp.pi / 4 * Y100 - mp.log(Y100) / 8 - mp.mpf("0.1107867951")
fL100, fQ100 = FL_rat(100), FQ_rat(100)
print("    asymptotic L: (pi/2)Y - lnY + 1/2 = %.6f  vs exact %.6f  (rel %.1e)" % (float(asL), float(fL100), abs(float(asL / fL100 - 1))))
print("    asymptotic Q: (pi/4)Y - lnY/8 + C_Q = %.6f  vs exact %.6f  (rel %.1e)" % (float(asQ), float(fQ100), abs(float(asQ / fQ100 - 1))))
print("    RAR: F_R(1e6) = %.9f   -> 2pi^4/15 - F_R = %.2e  (= 2*Gamma(8)zeta(8)/y_t^2 = %.1f/y_t^2)"
      % (float(FR_turn(1e6)), float(2 * mp.pi**4 / 15 - FR_turn(1e6)), float(2 * mp.factorial(7) * mp.zeta(8))))
ok4 = max(rel4) < 1e-9 and abs(float(asL / fL100 - 1)) < 2e-3 and abs(float(asQ / fQ100 - 1)) < 2e-3
check("K4", ok4, "rational forms exact (max rel %.1e); asymptotics at y_t=100: L %.1e, Q %.1e" % (max(rel4), abs(float(asL / fL100 - 1)), abs(float(asQ / fQ100 - 1))),
      "rel < 1e-9 exact; < 2e-3 asymptotic")
NUM["I_turn_values"] = {"F_L(50)": float(FL_rat(50)), "F_L(100)": float(fL100), "F_Q(50)": float(FQ_rat(50)),
                        "F_Q(100)": float(fQ100), "F_R(100)": float(FR_turn(100)), "F_R(1e6)": float(FR_turn(1e6)),
                        "F_M(50)": float(Fturn(hMm, 50)), "F_M(100)": float(Fturn(hMm, 100)),
                        "asymptotic_rel_L": abs(float(asL / fL100 - 1)), "asymptotic_rel_Q": abs(float(asQ / fQ100 - 1)),
                        "rational_vs_quad_max_rel": max(rel4),
                        "RAR_correction_coefficient": float(2 * mp.factorial(7) * mp.zeta(8))}

# ==================================================================================== K5  the roots
banner("K5  THE TURN-OFF THAT MAKES EACH KERNEL EQUAL 73.19")

def bisect(f, lo, hi, tol=1e-14):
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        fm = f(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
        if hi - lo < tol * max(1, abs(mid)):
            break
    return (lo + hi) / 2

FUN = {"L": lambda Y: FL_rat(Y), "Q": lambda Y: FQ_rat(Y), "R": lambda Y: FR_turn(Y), "M": lambda Y: Fturn(hMm, Y)}
roots = {}
for k in ("L", "Q", "R", "M"):
    r = bisect(lambda Y: FUN[k](Y) - TARGET, mp.mpf("0.05"), mp.mpf("1e5"))
    roots[k] = r
    if r is None:
        print("    %s: NO ROOT.  sup I_turn = %.9f < 73.19" % (k, float(FUN[k](mp.mpf(1e6)))))
    else:
        print("    %s: y_t = %.6f   (F = %.9f, target 73.19)" % (k, float(r), float(FUN[k](r))))
r32_L = bisect(lambda Y: FL_rat(Y) - TARGET_32PI, mp.mpf(1), mp.mpf(1e4))
r32_Q = bisect(lambda Y: FQ_rat(Y) - TARGET_32PI, mp.mpf(1), mp.mpf(1e4))
r32_M = bisect(lambda Y: Fturn(hMm, Y) - TARGET_32PI, mp.mpf(1), mp.mpf(1e4))
r100_L = bisect(lambda Y: FL_rat(Y) - TARGET_A4, mp.mpf(1), mp.mpf(1e4))
r100_Q = bisect(lambda Y: FQ_rat(Y) - TARGET_A4, mp.mpf(1), mp.mpf(1e4))
r100_M = bisect(lambda Y: Fturn(hMm, Y) - TARGET_A4, mp.mpf(1), mp.mpf(1e4))
print("    reference targets: 32pi = %.6f -> y_t: L %.4f, Q %.4f, M %.4f" % (float(TARGET_32PI), float(r32_L), float(r32_Q), float(r32_M)))
print("    100.405845 (A4, BRIEF constants) -> y_t: L %.4f, Q %.4f, M %.4f" % (float(r100_L), float(r100_Q), float(r100_M)))
ok5 = (roots["R"] is None and roots["L"] is not None and abs(float(roots["L"]) - 48.7877) < 5e-3
       and abs(float(roots["Q"]) - 94.0539) < 5e-2 and abs(float(roots["M"]) - 63.6856) < 5e-2
       and float(FUN["R"](mp.mpf(1e6))) < float(TARGET)
       and abs(float(roots[CANON]) - 48.7877) < 5e-3)   # the canonical kernel must be the one that closes at 48.79
check("K5", ok5, "y_t(73.19): L %.4f, Q %.4f, M %.4f, R none (sup %.6f); canonical(%s) %.4f" % (float(roots["L"]), float(roots["Q"]), float(roots["M"]), float(FUN["R"](mp.mpf(1e6))), CANON, float(roots[CANON])),
      "L 48.7877+-0.005, Q 94.054+-0.05, M 63.686+-0.05, R no root, canonical == 48.7877")
NUM["y_t_at_73_19"] = {k: (None if v is None else float(v)) for k, v in roots.items()}
NUM["y_t_at_32pi"] = {"L": float(r32_L), "Q": float(r32_Q), "M": float(r32_M)}
NUM["y_t_at_100_405845"] = {"L": float(r100_L), "Q": float(r100_Q), "M": float(r100_M)}

# ==================================================================================== K6  the record's band
banner("K6  THE RECORD'S 94-129 BAND IS THE QUADRATURE KERNEL AT ITS TWO a0 NORMALISATIONS")
q73 = float(roots["Q"])
q32 = float(bisect(lambda Y: FQ_rat(Y) - TARGET_32PI, mp.mpf(1), mp.mpf(1e4)))
q100 = float(bisect(lambda Y: FQ_rat(Y) - TARGET_A4, mp.mpf(1), mp.mpf(1e4)))
print("    quadrature at 73.19      -> y_t = %.4f   (record 23171085: 94)" % q73)
print("    quadrature at 32pi       -> y_t = %.4f   (record: 128.9 on the kappa=1/2 footing)" % q32)
print("    quadrature at 100.405845 -> y_t = %.4f   (A4: 128.7559)" % q100)
print("    the theory's kernel (L)  -> y_t = %.4f at 73.19, %.4f at 32pi   [factor %.3f below the band]"
      % (float(roots["L"]), float(NUM["y_t_at_32pi"]["L"]), q73 / float(roots["L"])))
# sharing the record's y_t over-predicts Lambda for the action kernel
over = float(FL_rat(mp.mpf(q73)) / TARGET)
print("    feeding the record's y_t = 94.05 to the action kernel over-predicts Lambda by %.4f x" % over)
ok6 = (abs(q73 / 94.0 - 1) < 5e-3 and abs(q32 / 128.9 - 1) < 5e-3 and abs(q100 / 128.7559 - 1) < 1e-3
       and abs(over - 1.93) < 0.1)
check("K6", ok6, "band reproduced: Q(73.19)=%.4f vs 94 (%.2f%%); Q(32pi)=%.4f vs 128.9 (%.2f%%); L over-predicts by %.3fx" % (q73, 100 * abs(q73 / 94 - 1), q32, 100 * abs(q32 / 128.9 - 1), over),
      "<0.5% on both ends of 94-129; over-prediction 1.9-2.0x")
NUM["band"] = {"F_over_73.19_at_record_y_t": {k: float(FUN[k](mp.mpf(q73)) / TARGET) for k in ("L", "Q", "R", "M")},
               "Q_at_73.19": q73, "Q_at_32pi": q32, "Q_at_100.405845": q100, "record_94": 94.0,
               "record_128.9": 128.9, "L_over_prediction_at_Q_y_t": over}

# ==================================================================================== K7  12.99 and 5.6
banner("K7  12.99 = 2 pi^4/15 EXACTLY, AND 5.6x = 73.19/(2 pi^4/15)")
ratio = float(TARGET / IR_inf)
print("    I_R(inf) = 2 pi^4/15 = %.10f ; record says 12.99  (%.3f%%)" % (float(IR_inf), 100 * abs(float(IR_inf) / 12.99 - 1)))
print("    73.19 / 12.9878788 = %.6f ; record says 5.6  (%.2f%%)" % (ratio, 100 * abs(ratio / 5.6 - 1)))
ok7 = abs(float(IR_inf) / 12.99 - 1) < 1e-3 and abs(ratio / 5.6 - 1) < 1e-2
check("K7", ok7, "I_R = %.8f (2pi^4/15), 12.99 to %.3f%%; 5.6x = %.4f" % (float(IR_inf), 100 * abs(float(IR_inf) / 12.99 - 1), ratio),
      "<0.1% and <1% (5.6 is 5.635 rounded to two figures)")
NUM["record_reproduction"] = {"I_R_inf": float(IR_inf), "record_12.99": 12.99,
                              "rel_err_12.99": abs(float(IR_inf) / 12.99 - 1), "ratio_73.19_over_I_R": ratio,
                              "rel_err_5.6": abs(ratio / 5.6 - 1)}

# ==================================================================================== K8  target bookkeeping
banner("K8  WHAT 73.19 IS: 32 pi = 3 Z^2 AND 73.19/32 pi = Omega_Lambda")
res_Z = sp.simplify(3 * (2 * sp.sqrt(8 * sp.pi / 3))**2 - 32 * sp.pi)
omega_from_target = float(TARGET / TARGET_32PI)
H0 = 67.4e3 / 3.0856775814913673e22
omega_brief = LAMBDA * C_LIGHT**2 / (3 * H0**2)
N_alt = float(LAMBDA * C_LIGHT**4 / A0_ALT**2)
N_can = float(LAMBDA * C_LIGHT**4 / A0_CAN**2)
a0_of_target = math.sqrt(LAMBDA * C_LIGHT**4 / float(TARGET))
print("    3Z^2 - 32pi = %s   (Z = 2 sqrt(8pi/3) = %.6f)" % (res_Z, Z_SCALE))
print("    73.19/32pi = %.6f  -> Omega_Lambda implied by the record's target" % omega_from_target)
print("    BRIEF (Lambda, H0=67.4): Omega_Lambda = %.6f -> 32 pi Omega_L = %.4f  (= A4's alt-footing N_Lambda %.4f)"
      % (omega_brief, 32 * math.pi * omega_brief, N_alt))
print("    BRIEF canonical a0: Lambda c^4/a0^2 = %.6f  (A4 stored 100.405845)" % N_can)
print("    a0 that makes Lambda c^4/a0^2 = 73.19: %.5e m/s^2  (record: 1.097e-10, %.2f%%)"
      % (a0_of_target, 100 * abs(a0_of_target / 1.097e-10 - 1)))
ok8 = (res_Z == 0 and abs(omega_from_target - 0.72803) < 1e-4 and abs(32 * math.pi * omega_brief / N_alt - 1) < 5e-3
       and abs(N_can / 100.405845 - 1) < 2e-3 and abs(a0_of_target / 1.097e-10 - 1) < 5e-3)
check("K8", ok8, "32pi=3Z^2 exact; 73.19/32pi=%.5f; BRIEF Omega_L=%.4f -> %.2f (=%.2f); a0(73.19)=%.4e" % (omega_from_target, omega_brief, 32 * math.pi * omega_brief, N_alt, a0_of_target),
      "identity exact; Omega to 1e-4; N_Lambda to 0.5% (a0_alt is cH0/Z to 0.12%); a0 to 0.5%")
NUM["targets"] = {"32pi": float(TARGET_32PI), "73.19_over_32pi": omega_from_target, "Z": Z_SCALE,
                  "Omega_Lambda_BRIEF": omega_brief, "N_Lambda_BRIEF_alt": N_alt, "N_Lambda_BRIEF_canonical": N_can,
                  "a0_that_gives_73.19": a0_of_target}

# ==================================================================================== K9/K10  SPARC
banner("K9-K10  SPARC ON DISK: WHICH KERNEL DOES THE TRANSITION FOLLOW?")
from hunt_lib import load_sparc, A0 as A0H, load_rar, B as BRAW

gals = load_sparc()
gb = np.concatenate([q["gbar"] for q in gals])
go = np.concatenate([q["gobs"] for q in gals])
gid = np.concatenate([np.full(len(q["r"]), i) for i, q in enumerate(gals)])
msk = (gb > 0) & (go > 0)
gb, go, gid = gb[msk], go[msk], gid[msk]
lg = np.log10(go)
print("    SPARC: %d galaxies, %d points (hunt_lib.load_sparc, Q<=2, inc>=30, >=6 pts)" % (len(gals), len(gb)))

def binned(a0_ref):
    ly = np.log10(gb / a0_ref)
    edges = np.linspace(-2.6, 1.6, 22)
    cen = 0.5 * (edges[1:] + edges[:-1])
    rows = []
    for i in range(len(cen)):
        k = (ly >= edges[i]) & (ly < edges[i + 1])
        if k.sum() < 15:
            continue
        rng = np.random.default_rng(i)
        gl = np.unique(gid[k])
        bb = []
        for _ in range(200):
            pick = rng.choice(gl, len(gl), replace=True)
            idx = np.concatenate([np.where(k & (gid == g_))[0] for g_ in pick])
            bb.append(np.median(lg[idx]))
        rows.append((cen[i], float(np.median(lg[k])), float(np.std(bb)), int(k.sum()), float(np.median(np.log10(gb[k])))))
    return np.array(rows)

SPARC = {}
for foot, a0v in A0H.items():
    rows = binned(a0v)
    yb = 10 ** rows[:, 0]
    chi = {}
    worst = {}
    for k, (f, _) in KER.items():
        pr = np.log10(f(yb)) + rows[:, 4]
        chi[k] = float(np.sum(((rows[:, 1] - pr) / rows[:, 2])**2))
        tr = (rows[:, 0] > -1.0) & (rows[:, 0] < 0.8)
        worst[k] = float(np.max(np.abs((rows[tr, 1] - pr[tr]) / rows[tr, 2])))
    SPARC[foot] = {"chi": chi, "worst": worst, "dof": len(rows), "rows": rows}
    print("    %-9s (%d bins) chi2: L %.1f | Q %.1f | R %.1f | M %.1f    worst transition pull: L %.2f | Q %.2f | R %.2f"
          % (foot, len(rows), chi["L"], chi["Q"], chi["R"], chi["M"], worst["L"], worst["Q"], worst["R"]))
    print("               dchi2(Q-L) = %+8.2f    dchi2(R-L) = %+6.2f    dchi2(M-L) = %+6.2f"
          % (chi["Q"] - chi["L"], chi["R"] - chi["L"], chi["M"] - chi["L"]))
dQL = [SPARC[f]["chi"]["Q"] - SPARC[f]["chi"][CANON] for f in SPARC]
dRL = [SPARC[f]["chi"]["R"] - SPARC[f]["chi"][CANON] for f in SPARC]
print("    canonical kernel = %s ;  dchi2(Q - canon) = %.1f / %.1f ; dchi2(R - canon) = %.1f / %.1f"
      % (CANON, dQL[0], dQL[1], dRL[0], dRL[1]))
ok9 = all(SPARC[f]["chi"]["Q"] - SPARC[f]["chi"][CANON] > 50 for f in SPARC) and \
      all(abs(SPARC[f]["chi"]["R"] - SPARC[f]["chi"][CANON]) < 15 for f in SPARC)
check("K9", ok9, "fixed footing: dchi2(Q-canon) = %.1f, %.1f ; dchi2(R-canon) = %.1f, %.1f" % (dQL[0], dQL[1], dRL[0], dRL[1]),
      "Q excluded at >50 on both footings; |R-canon| < 15")
NUM["SPARC_fixed"] = {f: {"chi2": SPARC[f]["chi"], "worst_transition_pull": SPARC[f]["worst"], "dof": SPARC[f]["dof"],
                          "dchi2_Q_minus_L": SPARC[f]["chi"]["Q"] - SPARC[f]["chi"]["L"],
                          "dchi2_R_minus_L": SPARC[f]["chi"]["R"] - SPARC[f]["chi"]["L"],
                          "dchi2_M_minus_L": SPARC[f]["chi"]["M"] - SPARC[f]["chi"]["L"]} for f in SPARC}

# K10: (amplitude, a0) profiled -- the fair shape test, no footing preference
rowsC = SPARC["canonical"]["rows"]
def profiled(f):
    def chi(p):
        A = 10 ** p[0]
        a0v = 10 ** p[1]
        pr = np.log10(A * f(10 ** rowsC[:, 0] * A0_CAN / a0v)) + rowsC[:, 4]
        return float(np.sum(((rowsC[:, 1] - pr) / rowsC[:, 2])**2))
    best = None
    for la0 in np.arange(-10.2, -9.5, 0.02):
        for la in np.arange(-0.4, 0.4, 0.02):
            v = chi((la, la0))
            if best is None or v < best[0]:
                best = (v, la, la0)
    r = minimize(chi, [best[1], best[2]], method="Nelder-Mead",
                 options=dict(xatol=1e-7, fatol=1e-9, maxiter=6000))
    return float(r.fun), float(10 ** r.x[0]), float(10 ** r.x[1])

PROF = {}
for k, (f, _) in KER.items():
    PROF[k] = profiled(f)
    print("    profiled (A, a0): %s  chi2 = %7.2f on %d dof   A = %.4f   a0 = %.4e" % (k, PROF[k][0], len(rowsC) - 2, PROF[k][1], PROF[k][2]))
d10 = PROF["Q"][0] - PROF[CANON][0]
ok10 = d10 > 10 and abs(PROF["R"][0] - PROF[CANON][0]) < 5
check("K10", ok10, "profiled: dchi2(Q-canon) = %+.2f ; dchi2(R-canon) = %+.2f ; a0(Q) = %.3e vs a0(canon) = %.3e" % (d10, PROF["R"][0] - PROF[CANON][0], PROF["Q"][2], PROF[CANON][2]),
      "Q worse by >10 with equal parameters; |R-canon| < 5")
NUM["SPARC_profiled"] = {k: {"chi2": PROF[k][0], "A": PROF[k][1], "a0": PROF[k][2]} for k in PROF}
NUM["SPARC_profiled"]["dof"] = len(rowsC) - 2

# ==================================================================================== K11  turn-off visibility
banner("K11  IS THE Lambda-REQUIRED TURN-OFF VISIBLE IN THE RAR?")
vis = {}
for k in ("L", "Q", "M"):
    if roots[k] is None:
        continue
    yt = float(roots[k])
    yy = np.logspace(-3, 3, 4001)
    f = KER[k][0](yy)
    ft = 1 + (KER[k][0](yy) - 1) / (1 + (yy / yt)**2)
    frac = np.abs(f - ft) / f
    i = int(np.argmax(frac))
    vis[k] = {"max_dg_over_g": float(frac[i]), "max_dex": float(frac[i] / math.log(10)), "at_y": float(yy[i]), "y_t": yt}
    print("    %s (y_t = %.2f): max |dg/g| = %.5f = %.5f dex at y = %.1f" % (k, yt, vis[k]["max_dg_over_g"], vis[k]["max_dex"], vis[k]["at_y"]))
# and the chi2 cost on SPARC
cost = {}
for k in ("L", "Q", "M"):
    if roots[k] is None:
        continue
    yt = float(roots[k])
    f = KER[k][0]
    ft = lambda yy, f=f, yt=yt: 1 + (f(yy) - 1) / (1 + (yy / yt)**2)
    rows = SPARC["canonical"]["rows"]
    pr = np.log10(ft(10 ** rows[:, 0])) + rows[:, 4]
    cost[k] = float(np.sum(((rows[:, 1] - pr) / rows[:, 2])**2)) - SPARC["canonical"]["chi"][k]
    print("    %s: SPARC dchi2 from imposing the Lambda-required turn-off = %+.3f" % (k, cost[k]))
ok11 = all(v["max_dex"] < 0.01 for v in vis.values()) and all(abs(v) < 1.0 for v in cost.values())
check("K11", ok11, "turn-off signature: max %.5f dex (L), %.5f dex (Q); SPARC dchi2 <= %.2f" % (vis["L"]["max_dex"], vis["Q"]["max_dex"], max(abs(v) for v in cost.values())),
      "max < 0.01 dex (RAR scatter 0.06 dex) and |dchi2| < 1")
NUM["turnoff_visibility"] = {"signature": vis, "SPARC_dchi2": cost}

# ==================================================================================== K12  Solar System
banner("K12  THE STRONG-FIELD COEFFICIENT: A NUMBER THAT DOES DISTINGUISH THE KERNELS")
sf = {"L": 1.0 * A0_CAN, "Q": 0.5 * A0_CAN, "R": 0.0, "M": float("inf")}
for k in ("L", "Q", "R"):
    print("    %s: c*a0 = %.3e m/s^2 = %.1f x the Earth bound (B_E = %.2e)" % (k, sf[k], sf[k] / B_EARTH, B_EARTH))
yt_cap = Y_T_NEPTUNE
print("    planetary cap (A4, Neptune, over-tight stand-in): y_t <= %.2f" % yt_cap)
print("    required: L %.2f (margin %.2fx), Q %.2f (margin %.2fx), M %.2f (margin %.2fx)"
      % (float(roots["L"]), yt_cap / float(roots["L"]), float(roots["Q"]), yt_cap / float(roots["Q"]),
         float(roots["M"]), yt_cap / float(roots["M"])))
ok12 = abs(sf["L"] / B_EARTH / 2557.38 - 1) < 1e-3 and abs(sf["Q"] / B_EARTH / 1278.69 - 1) < 1e-3 and \
       all(yt_cap / float(roots[k]) > 1 for k in ("L", "Q", "M"))
check("K12", ok12, "c*a0/B_E = %.1f (L), %.1f (Q), 0 (R); one y_t inside the planetary cap for L (margin %.1fx)" % (sf["L"] / B_EARTH, sf["Q"] / B_EARTH, yt_cap / float(roots["L"])),
      "2557.38 and 1278.69 to 0.1%; margin > 1")
NUM["solar_system"] = {"c_a0_over_BE": {k: sf[k] / B_EARTH for k in ("L", "Q")}, "B_E": B_EARTH,
                       "y_t_cap": yt_cap, "margin": {k: yt_cap / float(roots[k]) for k in ("L", "Q", "M")}}

# ==================================================================================== K13  KiDS lensing RAR
banner("K13  THE KiDS-1000 LENSING RAR (ON DISK): A NULL FOR KERNEL SEPARATION")
gbr, gor, errr = load_rar("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
nb = len(gbr)
d = np.genfromtxt(os.path.join(BRAW, "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt"), comments="#")
corr = np.zeros((nb, nb))
idx = 0
for a in range(nb):
    for b in range(nb):
        corr[a, b] = d[idx, 5]
        idx += 1
Cm = corr * np.outer(errr, errr)
Cinv = np.linalg.inv(Cm)
print("    %d bins, g_bar = %.2e .. %.2e m/s^2 (y = %.1e .. %.1e), median error %.1f%%"
      % (nb, gbr.min(), gbr.max(), gbr.min() / A0_CAN, gbr.max() / A0_CAN, 100 * np.median(errr / gor)))
print("    smallest covariance eigenvalue / largest = %.2e (a near-singular common mode)" % (np.linalg.eigvalsh(Cm).min() / np.linalg.eigvalsh(Cm).max()))
kchi = {}
print("    correlation common mode: min/max covariance eigenvalue = %.2e" % (np.linalg.eigvalsh(Cm).min() / np.linalg.eigvalsh(Cm).max()))
for k, (f, _) in KER.items():
    m = f(gbr / A0_CAN) * gbr
    A = float((m @ Cinv @ gor) / (m @ Cinv @ m))
    r = gor - A * m
    kchi[k] = float(r @ Cinv @ r)
    print("    %s: profiled amplitude A = %.4f, chi2 = %.2f (15 bins, 1 param)" % (k, A, kchi[k]))
dk = kchi["Q"] - kchi["L"]
print("    dchi2(Q-L) = %+.2f -> the deep lensing RAR does NOT separate the kernels" % dk)
ok13 = abs(dk) < 20
check("K13", ok13, "KiDS RAR: dchi2(Q-L) = %+.2f (no separation); chi2/dof(L) = %.2f" % (dk, kchi["L"] / (nb - 1)),
      "|dchi2| < 20 -> a null, reported as such")
NUM["KiDS_lensing"] = {"N": nb, "chi2": kchi, "dchi2_Q_minus_L": dk,
                       "eigen_ratio": float(np.linalg.eigvalsh(Cm).min() / np.linalg.eigvalsh(Cm).max()),
                       "gbar_range": [float(gbr.min()), float(gbr.max())],
                       "y_range": [float(gbr.min() / A0_CAN), float(gbr.max() / A0_CAN)]}

# ==================================================================================== K14  canonical kernel
banner("K14  THE CANONICAL KERNEL IS THE ACTION'S KERNEL")
print("    canonical kernel in this run: %s (%s)" % (CANON, KER[CANON][1]))
print("    action -> W_full -> nu: A12 sec.5 (K10, residual 0); lattice: A2 sec.1-2")
ok14 = (CANON == "L")
check("K14", ok14, "canonical = %s, expected L (the action's kernel)" % CANON, "canonical == 'L'")
NUM["canonical"] = CANON

# ==================================================================================== secondary numbers
NUM["secondary"] = {
    "y_t_ratio_Q_over_L_at_73.19": float(roots["Q"] / roots["L"]),
    "a0_if_RAR_and_Lambda": float((LAMBDA * C_LIGHT**4 / (2 * sp.pi**4 / 15))**0.5),
    "a0_if_RAR_and_Lambda_over_a0_can": float((LAMBDA * C_LIGHT**4 / (2 * sp.pi**4 / 15))**0.5 / A0_CAN),
    "F_R_deficit_at_1e6": float(2 * mp.pi**4 / 15 - FR_turn(1e6)),
    "32pi_Omega_L_BRIEF": 32 * math.pi * omega_brief,
    "chi2_per_dof_L_profiled": PROF["L"][0] / (len(rowsC) - 2),
    "nominal_sigma_dchi2_17p05": float(mp.sqrt(d10)),      # 1 dof: Delta chi^2 = z^2
    "nominal_sigma_dchi2_Q_fixed": {f: float(np.sqrt(max(0.0, SPARC[f]["chi"]["Q"] - SPARC[f]["chi"]["L"]))) for f in SPARC},
    "nu_at_y_half": {k: float(KER[k][0](0.5)) for k in KER},
}
NUM["external_inputs"] = {
    "12.99": "Zenodo 23251231 (RAR-kernel vacuum value)",
    "5.6": "Zenodo 23251231 (ratio to 73.19)",
    "73.19": "Zenodo 23251231 (observed Lambda c^4/a0^2)",
    "94": "Zenodo 23171085 (y_t at measured a0 = 1.097e-10)",
    "128.9": "Zenodo 23171085 (y_t on the kappa = 1/2 footing)",
    "100.405845": "A4 a4_results.json (Lambda c^4/a0_can^2 from BRIEF constants)",
    "128.7559": "A4 a4_results.json (quadrature y_t at 100.405845)",
    "0.0103700578": "L340 A1 stored max |dlog10(nu_mono/nu_RAR)| at y = 14.35",
    "2.5396382826": "L340 A1 y_p",
    "0.6476102379": "L340 A1 h_p",
    "0.05": "L340 A1 delta",
    "3.66e-14": "A4 B_E, Earth 2 sigma bound (m/s^2)",
    "605.96": "A4 tightest planetary y_t cap (Neptune, over-tight stand-in)",
    "6.11e5": "A4 Earth y_t cap",
    "0.06": "RAR intrinsic scatter in dex (repo convention, f21/f23)",
}

# ==================================================================================== summary
npass = sum(1 for c in CHECKS if c["pass"])
print("\n" + "=" * 104)
print("SUMMARY")
print("=" * 104)
for k in ("L", "Q", "R", "M"):
    r = roots[k]
    print("  %-2s %-32s c = %-12s y_t(73.19) = %s" %
          (k, KER[k][1], ("1" if k == "L" else "1/2" if k == "Q" else "0" if k == "R" else "inf (ln y)"),
           ("none" if r is None else "%.4f" % float(r))))
print("  the 5.6x 'tension' is 73.19/12.9878788 = %.4f and belongs to the RAR kernel only." % ratio)
print("  the record's 94-129 band is the quadrature kernel at two a0 normalisations; the action's kernel gives "
      "%.2f-%.2f." % (float(roots["L"]), float(NUM["y_t_at_32pi"]["L"])))
print("  SPARC: dchi2(Q - L) = %.1f (canonical footing), %.1f (alt); dchi2(R - L) = %.1f, %.1f."
      % (SPARC["canonical"]["chi"]["Q"] - SPARC["canonical"]["chi"]["L"], SPARC["alt"]["chi"]["Q"] - SPARC["alt"]["chi"]["L"],
         SPARC["canonical"]["chi"]["R"] - SPARC["canonical"]["chi"]["L"], SPARC["alt"]["chi"]["R"] - SPARC["alt"]["chi"]["L"]))

out = {"lane": "A25_kernel_conflict",
       "status": "CLOSED-DERIVED (kernel) + NUMERICAL (closure roots) + DECIDABLE (falsifier)",
       "mutate": MUTATE,
       "checks": CHECKS,
       "numbers": NUM,
       "constants_used": [
           "c = 2.99792458e8 m/s [BRIEF]",
           "Lambda = 1.0890e-52 m^-2 [BRIEF]",
           "a0_can = 9.36e-11 m/s^2 [BRIEF]",
           "a0_alt = 1.13e-10 m/s^2 [BRIEF]",
           "G = 6.67430e-11 [BRIEF]",
           "H0 = 67.4 km/s/Mpc [BRIEF]",
           "Z = 2 sqrt(8 pi/3) = 5.78881 [BRIEF]",
           "target 73.19 [Zenodo 23251231, external]",
           "94 and 128.9 [Zenodo 23171085, external]",
           "100.405845 and 128.7559 [A4 a4_results.json]",
           "B_E = 3.66e-14 m/s^2 and y_t cap 605.96 [A4]",
           "y_p = 2.5396382826, h_p = 0.6476102379, delta = 0.05, y* = 2.3374124053 [L340 A1 / XC4 S2]",
           "SPARC rotmods, 147 galaxies / 3140 points, Upsilon_d = 0.5, Upsilon_b = 0.7 [hunt_2026/hunt_lib.py]",
           "KiDS-1000 Brouwer+2021 Fig.4-5 C1 isolated RAR, 15 bins + covariance [real_research/data]"],
       }
with open(os.path.join(HERE, "a25_results.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("\n  wrote a25_results.json")
print("\nA25 COMPLETE: %d/%d checks PASS." % (npass, len(CHECKS)))
sys.exit(0 if npass == len(CHECKS) else 1)
