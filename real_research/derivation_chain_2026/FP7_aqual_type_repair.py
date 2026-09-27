#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP7 -- THE AQUAL-TYPE REPAIR OF THE ROOT ACTION: the core's QUMOND sector replaced by an AQUAL-type MOND term on a scalar
with its own a0-free inertia, varied as one action and scored on every gate the chain runs.

WHY.  FP3 (committed 9b265b331) traced the ungated C-H/K core's two failures -- sigma_8 = 18-27 (L341) and FP5's
Hadamard-ill-posed zero-field linearisation -- to one root: the core's QUMOND energy q ~ (4/3) Z^(3/4) reads the
constraint-fixed U, is O(eps^(3/2)) around FRW and has an INFINITE zero-field tangent.  FP3 left one door (G1t): an
AQUAL-type J ~ (2/3) Y^(3/2), O(eps^3) with ZERO tangent, on a field with its own inertia.  This lane builds that repair
and runs it through statics, FRW, stability, c_T/PPN, the mode count and the constants.

THE REPAIRED ACTION (units c = 1, x0 = ct; alpha = a0/c^2; per 1/(16 pi G)):
  I = (1/16 pi G) Int d^4x sqrt(-g) {  R - 2 Lambda + alpha_c a_m a^m - c_2 (K - <K>_h)^2        kept: EH + BPS khronon, beta = 0, leaf average
        + (2 - alpha_c) h^{mn} (2 a_m - D_m chi) D_n chi                                        the AQUAL chassis (A1: forced by statics)
        - 2 alpha^2 J( h^{mn} D_m phi D_n phi / alpha^2 )                                       the MOND term, on phi (J = J_P2)
        + 2 lambda (n^m d_m phi)^2                                                             phi's a0-free inertia (khronon frame)
        + Int_0^b dz L (d_z W - Delta_h W) + lambda_0 (W_0 - phi) }  ,  chi = W_b = S_h phi      heat filter, adapted (A1b: forced)
      + GHY + S_m[g]                                                                           matter minimally coupled to g only
  J_P2(Y) = -(1/4) ln(1 - 2 sqrt Y) - sqrt(Y)/2 - Y/2,  J' = mu_s(sqrt Y),  mu_s(x) = x/(1 - 2x):  P2 in two-field AQUAL form.
  Removed from the core: C-H's U, its chassis 2 h (DU - a)(DU - a) and its kernel 2 alpha^2 q(|D W_b|^2/alpha^2).
  n_m = -d_m tau/sqrt(X) is the clock's unit normal, a_m = D_m ln N its acceleration, h = g + n n, K = nabla.n.

CHECKS
  A1  statics from the action's own variation (sympy): psi = Phi; the chassis is FORCED -- the only quadratic chassis
      A a^2 + B a.Dchi + C |Dchi|^2 whose static phi-equation has no Newtonian term and whose Newtonian limit is GR + BPS
      (G_N = G/(1 - alpha_c/2), Phi = Phi_N + chi) is A = alpha_c, B = 2(2 - alpha_c), C = -(2 - alpha_c), the perfect
      square above.  CONTROL: C-H's chassis pins chi to the Newtonian potential (QUMOND); the naive (4, -2) chassis leaves
      a Newtonian term 4 alpha_c/(2 - alpha_c) of the WRONG sign.
  A1b the filter's placement: the discrete action's gradient carries S^T on the chassis's source and J on phi unfiltered;
      in Fourier the physical MOND response is sigma^2 (chassis filtered: bounded), 1/sigma^2 (J filtered: backward heat)
      or 1 (both: no filtering) -- only the first is admissible.
  A2  P2 embeds exactly (J_P2 closed form, J(0) = 0, deep (2/3) Y^(3/2), saturation x -> 1/2 = the a0/2 tail); the
      spherical law is P2 EXACTLY; static health C_T = mu_s > 0, C_L = (x mu_s)' > 0; C^QUMOND = 1/C^phi in both channels.
  A3  thin exponential discs (h = 0.1 R_d), y = 0.01-100: AQUAL vs QUMOND vs the algebraic law, from a DUAL (flux)
      Kacanov solve (provably convergent: w = nu - 1 is non-increasing); CONTROL: a Plummer sphere (AQUAL = QUMOND =
      algebraic); SPARC-level: the difference after profiling Upsilon vs SPARC's per-point errors and the RAR scatter.
  A4  the Solar System under the double filter (dual AQUAL on a spherical staggered grid; g02's filter kernel and gates
      exec'd read-only): CONTROLS -- spherical AQUAL = QUMOND exactly; the analytic linear EFE far field; the same grid's
      QUMOND reproduces FP1's committed P2 numbers.  Floors per gate on both footings and three Galactic fields; the strict
      law (xi -> 0) fails by its exact a0/2 tail.
  B1  FRW background (minisuperspace sympy): Friedmann = GR, a0 absent, phibar-dot ~ a^-3 (declared zero).
  B2  the linear FRW equations derived from the action (FP2's machinery + the new terms): J is O(eps^3) (zero tangent)
      and drops out; the new sector enters only the lapse, khronon and phi equations.
  B3  the zero-field linearisation (Minkowski block, sympy): modes omega^2 = 0 (marginal) and omega^2 > 0 -- no Hadamard
      growth; E(C_phi) in (alpha_c, 2] (FP5's E > 2 band removed).  CONTROL: the naive chassis has a growing band.
  B4  sub-horizon reduction of the FRW equations: no slip, G_eff = G_N [1 + eps(k, a)], lambda_eff chi'' = -4 pi G rho delta:
      the zero-field MOND response is inertia-limited, eps = (2/5)(ck/aH)^2/lambda_eff in the matter era.
  B5  sigma_8 vs LCDM (same primordial spectrum, declared cold dark mass), NO gate: linear (derived system) and at the
      physical amplitude (FP3/L341's yardstick with the scalar's own speed), both footings; gates >= 0.922 and <= 1.02.
  B6  strong coupling around zero field (tree level): Lambda_sc -> 0 at exact zero field; its size in real backgrounds.
  C1-C3 stability: the modes' T and V on Minkowski and static MOND backgrounds (y = 1e-3..1e4, both channels); the FC-KH (yq)'
      theorem re-derived for the new term; tracking (the L330 gate) and its speed.
  D1-D2 c_T = 1; full preferred-frame PPN with FP2's moving-source pipeline (read-only reuse).
  E1-E2 the mode count and whether the extra scalar is physically harmful.
  F   the repaired action's constants.   T  the sigma_8-vs-tracking pincer on lambda_eff.   W the ledger.
MUTATE=1 replaces the perfect-square chassis by the naive one (B, C) = (4, -2) with the BPS alpha_c a^2 kept: A1's
no-Newtonian-term check and B3's zero-field well-posedness must FAIL (rc = 1).

Run from the repository root:  python3 real_research/derivation_chain_2026/FP7_aqual_type_repair.py
"""
import os, re, sys, io, json, math, time, contextlib, warnings
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.optimize import brentq
from scipy.integrate import solve_ivp, quad, cumulative_trapezoid
from scipy import integrate
from scipy.special import erf
from scipy.linalg import expm
import scipy.sparse as sps
import scipy.sparse.linalg as spl
from numpy.polynomial import legendre as npleg

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("FP7_REPO_ROOT", os.path.dirname(os.path.dirname(HERE)))   # the env override is for out-of-tree testing only
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")              # the chain's committed inputs (== HERE in-tree)
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP7_aqual_type_repair"
OUT = {"lane": "FP7", "mutate": MUTATE, "root": "AQUAL-type repair of the C-H/K core (perfect-square chassis, J_P2 on phi, "
       "lambda (n.dphi)^2 inertia, heat filter on the chassis)", "checks": {}, "numbers": {}, "ledger": []}
CH = []
T0 = time.time()


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 112 + "\n" + t + "\n" + "=" * 112)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


P(__doc__.split("CHECKS")[0].strip())
CHASSIS = "naive" if MUTATE else "square"
if MUTATE:
    P("\n  *** MUTATE=1: the chassis is the NAIVE 4 a.Dchi - 2 |Dchi|^2 (BPS alpha_c a^2 kept, not completed into the square): "
      "A1 and B3 must FAIL ***")

# ---------------------------------------------------------------------------------------------- inputs from the chain
cc, Gn, PC_M, AU_M = 299792458.0, 6.67430e-11, 3.0856775814913673e16, 1.495978707e11
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
fp0 = os.path.join(CHAIN, "FP0_core_postulates_results.json")
if os.path.exists(fp0):
    n0 = json.load(open(fp0))["numbers"]
    A0 = {"canonical": n0["a0_canonical"], "alt": n0["a0_rho_total"]}
FP1_FLOORS = {"canonical": 0.0294, "alt": 0.0316}              # FP1 D2 (P2 QUMOND, double filter, binding Saturn monopole)
fp1j = os.path.join(CHAIN, "FP1_static_sector_results.json")
if os.path.exists(fp1j):
    try:
        d2 = json.load(open(fp1j))["numbers"]["D2"]
        FP1_FLOORS = {f: d2[f"P2/{f}"]["floor_pc"] for f in ("canonical", "alt")}
    except Exception:
        pass
AC_MAX, C2_FLOOR_FP2, V_TRACK = 3.2e-9, 7.2888e-3, 3 * 600e3            # FP2 B4, FP2 C4, the L330/FP2 tracking target
P(f"\n  inputs: a0 = {A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2 (FP0); FP1's QUMOND-P2 Solar-System floors "
  f"{FP1_FLOORS['canonical']:.4f} / {FP1_FLOORS['alt']:.4f} pc; alpha_c <= {AC_MAX:.1e} (FP2); tracking 3 x 600 km/s (FP2 C4)")
BCH = {"square": lambda ac: (2 * (2 - ac), -(2 - ac)), "naive": lambda ac: (4, -2)}[CHASSIS]

# ================================================================================================ A1 statics
banner("A1  THE STATIC WEAK-FIELD LIMIT FROM THE ACTION: psi = Phi, and the chassis is FORCED")
X3 = sp.symbols("x y z", real=True)
grad = lambda F: [sp.diff(F, xx) for xx in X3]
dot = lambda A_, B_: sum(a_ * b_ for a_, b_ in zip(A_, B_))
lap = lambda F: sum(sp.diff(F, xx, 2) for xx in X3)
eps = sp.symbols("epsilon", positive=True)
alph, ac_, Gs = sp.symbols("alpha alpha_c G", positive=True)
Aa, Bb, Cb = sp.symbols("A B C", real=True)
rho_s = sp.symbols("rho", real=True)
PhiF, PsiF, chiF = [sp.Function(n_)(*X3) for n_ in ("Phi", "Psi", "chi")]
Jf = sp.Function("J")
# exact static density per (1/16 pi G) d^4x on the branch tau = x0, ds^2 = -e^{2 Phi} dx0^2 + e^{-2 Psi} dx^2 (FP1 A1: the EH part
# is e^{Phi - Psi}(2|grad Psi|^2 - 4 grad Phi.grad Psi) up to a divergence; a_i = d_i Phi, h^{ij} = e^{2 Psi} delta, sqrt(-g) = e^{Phi - 3 Psi};
# statics: n.d phi = 0 (the inertia term is silent), chi = S phi with S = 1 here (the filter is A1b)
hij = sp.exp(2 * eps * PsiF)
Yex = hij * dot(grad(eps * chiF), grad(eps * chiF)) / (eps * alph) ** 2
exact = (sp.exp(eps * (PhiF - PsiF)) * (2 * dot(grad(eps * PsiF), grad(eps * PsiF)) - 4 * dot(grad(eps * PhiF), grad(eps * PsiF)))
         + sp.exp(eps * (PhiF - 3 * PsiF)) * (Aa * hij * dot(grad(eps * PhiF), grad(eps * PhiF))
                                               + Bb * hij * dot(grad(eps * PhiF), grad(eps * chiF))
                                               + Cb * hij * dot(grad(eps * chiF), grad(eps * chiF))
                                               - 2 * (eps * alph) ** 2 * Jf(Yex)))
lead = sp.simplify(sp.expand(sp.series(exact, eps, 0, 3).removeO()).coeff(eps, 2))
braces = (2 * dot(grad(PsiF), grad(PsiF)) - 4 * dot(grad(PhiF), grad(PsiF)) + Aa * dot(grad(PhiF), grad(PhiF))
          + Bb * dot(grad(PhiF), grad(chiF)) + Cb * dot(grad(chiF), grad(chiF)) - 2 * alph ** 2 * Jf(dot(grad(chiF), grad(chiF)) / alph ** 2))
lead_ok = sp.simplify(sp.expand(lead - braces)) == 0
Lst = sp.expand(braces - 16 * sp.pi * Gs * rho_s * PhiF)
psi_ok = sp.simplify(euler_equations(Lst, [PsiF], X3)[0].lhs.subs(PsiF, PhiF).doit()) == 0
Lred = sp.expand(Lst.subs(PsiF, PhiF).doit())
k1, k2, Zs = sp.symbols("k1 k2 Z", positive=True)
Jpoly = k1 * Zs ** sp.Rational(3, 2) + k2 * Zs ** 2                       # a generic test primitive (the algebra is kernel-blind)
ELs = euler_equations(Lred.replace(Jf, sp.Lambda(Zs, Jpoly)), [PhiF, chiF], X3)
Jp = sp.diff(Jpoly, Zs).subs(Zs, dot(grad(chiF), grad(chiF)) / alph ** 2)
divJ = sum(sp.diff(Jp * sp.diff(chiF, xx), xx) for xx in X3)
res_Phi = sp.simplify(sp.expand(ELs[0].lhs - ((4 - 2 * Aa) * lap(PhiF) - Bb * lap(chiF) - 16 * sp.pi * Gs * rho_s)))
res_chi = sp.simplify(sp.expand(ELs[1].lhs - (-Bb * lap(PhiF) - 2 * Cb * lap(chiF) + 4 * divJ)))
# eliminate lap Phi:  4 div(J' grad chi) - [B^2/(4-2A) + 2C] lap chi = 16 pi G rho B/(4 - 2A);  Phi = [4/(4-2A)] Phi_N + [B/(4-2A)] chi
newt_coef = Bb ** 2 / (4 - 2 * Aa) + 2 * Cb
req = sp.solve([sp.Eq(newt_coef, 0), sp.Eq(4 / (4 - 2 * Aa), 1 / (1 - ac_ / 2)), sp.Eq(Bb / (4 - 2 * Aa), 1)], [Aa, Bb, Cb], dict=True)
uniq = len(req) == 1 and sp.simplify(req[0][Aa] - ac_) == 0 and sp.simplify(req[0][Bb] - 2 * (2 - ac_)) == 0 and sp.simplify(req[0][Cb] + (2 - ac_)) == 0
square_id = sp.simplify(sp.expand(2 * sp.Symbol("a2") - (2 - ac_) * (sp.Symbol("X2") - 2 * sp.Symbol("aX") + sp.Symbol("a2"))
                                  - (ac_ * sp.Symbol("a2") + 2 * (2 - ac_) * sp.Symbol("aX") - (2 - ac_) * sp.Symbol("X2"))))
# controls: C-H's chassis (A, B, C) = (2 + alpha_c, -4, 2); the naive chassis (alpha_c, 4, -2)
ch_phi = sp.factor((4 - 2 * Aa).subs(Aa, 2 + ac_))
ch_pin = sp.simplify(((16 * sp.pi * Gs * rho_s) / 4).subs(ac_, 0))           # at alpha_c -> 0 the Phi equation reads 4 lap chi = 16 pi G rho
naive_resid = sp.factor(newt_coef.subs({Aa: ac_, Bb: 4, Cb: -2}))
Bm, Cm = BCH(ac_)
used_resid = sp.factor(newt_coef.subs({Aa: ac_, Bb: Bm, Cb: Cm}))
P(f"    leading O(eps^2) static density = the stated braces: {lead_ok};  psi-equation solved by Psi = Phi: {psi_ok}")
P(f"    EL residuals vs [(4 - 2A) lap Phi - B lap chi = 16 pi G rho] and [-B lap Phi - 2C lap chi + 4 div(J' grad chi) = 0]: {res_Phi}, {res_chi}")
P(f"    requirements (no Newtonian term in phi's equation; Phi = Phi_N[G_N] + chi; G_N = G/(1 - alpha_c/2)) -> {req}")
P(f"    the solution is the perfect square: 2 a^2 - (2 - alpha_c)|Dchi - a|^2 = alpha_c a^2 + (2 - alpha_c)(2a - Dchi).Dchi: {square_id == 0}")
P(f"    CONTROL C-H chassis (2 + alpha_c, -4, 2): lapse coefficient 4 - 2A = {ch_phi} -> 0 as alpha_c -> 0, so the Phi-equation "
  f"becomes 4 lap chi = 16 pi G rho (chi pinned to Newton: QUMOND)")
P(f"    CONTROL naive chassis (alpha_c, 4, -2): residual Newtonian coefficient in phi's equation {naive_resid} (subtracted from "
  f"4 J': mu_eff = J' - alpha_c/(2 - alpha_c) < 0 below x ~ alpha_c/2)")
P(f"    chassis in use ({CHASSIS}): residual Newtonian coefficient {used_resid}")
OUT["numbers"]["A1"] = dict(requirements=str(req), naive_residual=str(naive_resid), used_residual=str(used_resid))
check("A1 STATICS FROM THE ACTION: at leading weak-field order psi = Phi (no slip), the lapse equation is (4 - 2A) lap Phi - "
      "B lap chi = 16 pi G rho and phi's is -B lap Phi - 2C lap chi + 4 div(J' grad phi) = 0; requiring no Newtonian term in "
      "phi's equation and a GR + BPS Newtonian limit (Phi = Phi_N[G_N] + chi) has the UNIQUE solution A = alpha_c, "
      "B = 2(2 - alpha_c), C = -(2 - alpha_c): the perfect square; the chassis in use carries no Newtonian term",
      f"series {lead_ok}; Psi = Phi {psi_ok}; EL residuals {res_Phi}, {res_chi}; unique {uniq}; square identity {square_id == 0}; "
      f"residual of the chassis in use {used_resid}",
      lead_ok and psi_ok and res_Phi == 0 and res_chi == 0 and uniq and square_id == 0 and used_resid == 0,
      "C-H's chassis (A = 2 + alpha_c) makes the lapse a multiplier that pins its field to Newton (QUMOND, an infinite "
      "zero-field tangent); the AQUAL chassis keeps GR's lapse and puts MOND on the non-Newtonian scalar")

# ================================================================================================ A1b the filter's placement
banner("A1b  THE HEAT FILTER'S PLACEMENT: on the chassis (chi = S phi), not inside J")
rng = np.random.default_rng(7)
NG, dxg = 10, 1.0 / 10
I1 = np.eye(NG)
D1 = (np.roll(I1, -1, axis=1) - I1) / dxg
Dx, Dy = np.kron(D1, I1), np.kron(I1, D1)
DTD = Dx.T @ Dx + Dy.T @ Dy
S_ = expm(-0.01 * DTD)
xs_ = np.arange(NG) * dxg
XG, YG = np.meshgrid(xs_, xs_, indexing="ij")
Ph0 = (np.sin(2 * np.pi * XG) + 0.3 * rng.standard_normal(XG.shape)).ravel() * 0.02
f0 = (0.4 * np.cos(2 * np.pi * (XG + YG)) + 0.2 * rng.standard_normal(XG.shape)).ravel() * 0.01
acn, Bn, Cn = 1e-3, *BCH(1e-3)
mu_s = lambda x: x / (1.0 - 2.0 * x)
J_P2 = lambda Y: -0.25 * np.log(1 - 2 * np.sqrt(Y)) - np.sqrt(Y) / 2 - Y / 2


def act_d(fv):
    ch_ = S_ @ fv
    Y = (Dx @ fv) ** 2 + (Dy @ fv) ** 2
    return float(np.sum(-2 * ((Dx @ Ph0) ** 2 + (Dy @ Ph0) ** 2) + acn * ((Dx @ Ph0) ** 2 + (Dy @ Ph0) ** 2)
                        + Bn * ((Dx @ Ph0) * (Dx @ ch_) + (Dy @ Ph0) * (Dy @ ch_)) + Cn * ((Dx @ ch_) ** 2 + (Dy @ ch_) ** 2) - 2 * J_P2(Y)))


def stated_d(fv):
    ch_ = S_ @ fv
    Y = (Dx @ fv) ** 2 + (Dy @ fv) ** 2
    Jp = mu_s(np.sqrt(Y))
    return S_.T @ (Bn * DTD @ Ph0 + 2 * Cn * DTD @ ch_) - 4 * (Dx.T @ (Jp * (Dx @ fv)) + Dy.T @ (Jp * (Dy @ fv)))


fdg = np.array([(act_d(f0 + 1e-6 * e_) - act_d(f0 - 1e-6 * e_)) / 2e-6 for e_ in np.eye(NG * NG)])
err_adj = float(np.max(np.abs(fdg - stated_d(f0))) / np.max(np.abs(fdg)))
# Fourier gains of the physical MOND response for the three placements (sympy, linear response about a uniform J' = J0)
kf, sg_, J0, sK = sp.symbols("k sigma J_0 s", positive=True)
PhiK, phK = sp.symbols("Phi_k phi_k")


def gain(sc, sj):
    Lk = (-(2 - ac_) * kf ** 2 * PhiK ** 2 + 2 * (2 - ac_) * kf ** 2 * PhiK * sc * phK - (2 - ac_) * kf ** 2 * sc ** 2 * phK ** 2
          - 2 * J0 * kf ** 2 * sj ** 2 * phK ** 2 - sK * PhiK)
    sol = sp.solve([sp.diff(Lk, PhiK), sp.diff(Lk, phK)], [PhiK, phK], dict=True)[0]
    mond = sp.simplify(sol[PhiK] - (-sK / (2 * (2 - ac_) * kf ** 2)))           # physical potential minus its Newtonian part
    unf = sp.simplify(mond.subs(sg_, 1))
    return sp.simplify(mond / unf)


g_i, g_ii, g_iii = gain(sg_, 1), gain(1, sg_), gain(sg_, sg_)
P(f"    discrete static action on a 10x10 periodic leaf, S = exp(-0.01 D^T D), chassis on S phi, J_P2 on phi: |FD gradient - "
  f"(S^T[B D^TD Phi + 2C D^TD S phi] - 4 D^T(J' D phi))| = {err_adj:.1e}")
P(f"    physical MOND response relative to the unfiltered law:  chassis on S phi: {g_i};  J on S phi: {g_ii};  both: {g_iii}")
check("A1b THE FILTER'S PLACEMENT IS FORCED: the discrete action's phi-gradient is S^T[chassis source] + div(J' grad phi) "
      "(the variation itself puts S^T on the source; J reads phi unfiltered); in Fourier the physical MOND response is "
      "sigma^2 = e^{-xi^2 k^2} (double filter, bounded) with the chassis on S phi, 1/sigma^2 (backward heat, unbounded) with J "
      "on S phi, and 1 (no filtering at all) with both -- only the chassis placement is admissible",
      f"adjoint residual {err_adj:.1e}; gains {g_i}, {g_ii}, {g_iii}",
      err_adj < 1e-6 and sp.simplify(g_i - sg_ ** 2) == 0 and sp.simplify(g_ii - sg_ ** -2) == 0 and sp.simplify(g_iii - 1) == 0,
      "the coordinator's 'filter on the new field's gradient' is realised as chi = S_h phi in the chassis; a filter inside J "
      "would need S^{-1} of the matter source, and filtering both cancels")

# ================================================================================================ A2 P2 in AQUAL form
banner("A2  P2 IN TWO-FIELD AQUAL FORM: J_P2 closed form, the spherical law, static health, the QUMOND duality")
Yq, xq_, yq_ = sp.symbols("Y x y", positive=True)
Jsym = -sp.Rational(1, 4) * sp.log(1 - 2 * sp.sqrt(Yq)) - sp.sqrt(Yq) / 2 - Yq / 2
mus_sym = xq_ / (1 - 2 * xq_)
Jp_ok = sp.simplify(sp.diff(Jsym, Yq) - mus_sym.subs(xq_, sp.sqrt(Yq))) == 0
J0_ok = sp.limit(Jsym, Yq, 0) == 0
deep = sp.limit(Jsym / Yq ** sp.Rational(3, 2), Yq, 0)
xsol = sp.sqrt(yq_ ** 2 + yq_) - yq_
sph_ok = sp.simplify(mus_sym.subs(xq_, xsol) * xsol - yq_) == 0 and sp.simplify((xsol + yq_) - sp.sqrt(yq_ ** 2 + yq_)) == 0
tail = sp.limit(xsol, yq_, sp.oo)
CT_phi = mus_sym
CL_phi = sp.simplify(sp.diff(xq_ * mus_sym, xq_))
CL_form = sp.simplify(CL_phi - 2 * xq_ * (1 - xq_) / (1 - 2 * xq_) ** 2) == 0
nuP2 = sp.sqrt(1 + 1 / yq_)
CTQ, CLQ = nuP2 - 1, sp.diff(yq_ * nuP2, yq_) - 1
dual_T = sp.simplify(CTQ * CT_phi.subs(xq_, xsol) - 1) == 0
dual_L = sp.simplify(CLQ * CL_phi.subs(xq_, xsol) - 1) == 0
pos_T = sp.solve_univariate_inequality(CT_phi > 0, xq_, relational=False).intersect(sp.Interval.open(0, sp.Rational(1, 2))) == sp.Interval.open(0, sp.Rational(1, 2))
pos_L = sp.solve_univariate_inequality(CL_phi > 0, xq_, relational=False).intersect(sp.Interval.open(0, sp.Rational(1, 2))) == sp.Interval.open(0, sp.Rational(1, 2))
P(f"    J_P2(Y) = {Jsym};  J' = mu_s(sqrt Y): {Jp_ok};  J(0) = 0: {J0_ok};  J/Y^(3/2) -> {deep} (deep MOND)")
P(f"    spherical first integral mu_s(x) x = y  ->  x = sqrt(y^2 + y) - y,  g/a0 = x + y = sqrt(y^2 + y) (P2): {sph_ok};  x -> {tail} as y -> oo (the a0/2 tail)")
P(f"    C_T = mu_s = {CT_phi}, C_L = (x mu_s)' = {CL_phi}: positive on (0, 1/2): {pos_T}, {pos_L};  C^QUMOND = 1/C^phi: T {dual_T}, L {dual_L}")
check("A2 P2 EMBEDS EXACTLY IN AQUAL FORM: J_P2 = -(1/4) ln(1 - 2 sqrt Y) - sqrt(Y)/2 - Y/2 has J' = mu_s(sqrt Y) = sqrt(Y)/(1 - 2 sqrt Y), "
      "J(0) = 0 and J -> (2/3) Y^(3/2) (ZERO tangent); the spherical law is g = sqrt(g_N^2 + g_N a0) EXACTLY, with the scalar "
      "saturating at a0/2 (P2's tail); the static operator is elliptic in both channels (C_T = mu_s, C_L = 2x(1-x)/(1-2x)^2 > 0 "
      "on 0 < x < 1/2), and each coefficient is the reciprocal of QUMOND's (nu - 1, nu - 1 + y nu')",
      f"J' {Jp_ok}; J(0) {J0_ok}; deep {deep}; spherical {sph_ok}; tail {tail}; C_L form {CL_form}; positivity {pos_T}/{pos_L}; duality {dual_T}/{dual_L}",
      Jp_ok and J0_ok and deep == sp.Rational(2, 3) and sph_ok and tail == sp.Rational(1, 2) and CL_form and pos_T and pos_L and dual_T and dual_L)
OUT["numbers"]["A2"] = dict(J=str(Jsym), C_T=str(CT_phi), C_L=str(CL_phi))
P(f"    ({time.time() - T0:.0f} s)")

# ================================================================================================ A3 thin exponential discs
banner("A3  THIN EXPONENTIAL DISCS: AQUAL vs QUMOND vs the algebraic P2 law (dual Kacanov), and what SPARC can tell")
wP2 = lambda s: np.sqrt(1.0 + 1.0 / np.maximum(s, 1e-300)) - 1.0      # w = nu_P2 - 1: grad phi = w(|F|) F, F the scalar's flux
nuP2n = lambda y: np.sqrt(1.0 + 1.0 / np.maximum(y, 1e-300))


def faces(d0, grow, xmax):
    f = [0.0]; d = d0
    while f[-1] < xmax:
        f.append(f[-1] + d); d *= grow
    return np.array(f)


class Cyl:
    """axisymmetric (R, z >= 0) finite-volume grid; cell-centred potentials, face fluxes, corner stream function for the dual
    (F = grad Phi_N + curl(A e_phi)); the reflection plane and the axis carry A = 0, the outer boundary A = 0 (isolated source)."""

    def __init__(s, Rf, zf):
        s.Rf, s.zf = Rf, zf
        s.Rc = 0.5 * (Rf[1:] + Rf[:-1]); s.zc = 0.5 * (zf[1:] + zf[:-1])
        nR, nz = len(s.Rc), len(s.zc); s.nR, s.nz, s.N = nR, nz, nR * nz
        s.vol = np.outer(0.5 * (Rf[1:] ** 2 - Rf[:-1] ** 2), np.diff(zf)).ravel()
        cid = lambda i, j: i * nz + j
        r_, c_, v_ = [], [], []; s.outR = []
        for i in range(nR):
            for j in range(nz):
                f_ = i * nz + j
                if i < nR - 1:
                    d = s.Rc[i + 1] - s.Rc[i]; r_ += [f_, f_]; c_ += [cid(i + 1, j), cid(i, j)]; v_ += [1 / d, -1 / d]
                else:
                    d = Rf[-1] - s.Rc[-1]; r_.append(f_); c_.append(cid(i, j)); v_.append(-1 / d); s.outR.append((f_, d))
        s.GR = sps.csr_matrix((v_, (r_, c_)), shape=(s.N, s.N))
        r_, c_, v_ = [], [], []; s.outz = []
        for i in range(nR):
            for j in range(nz):
                f_ = i * nz + j
                if j < nz - 1:
                    d = s.zc[j + 1] - s.zc[j]; r_ += [f_, f_]; c_ += [cid(i, j + 1), cid(i, j)]; v_ += [1 / d, -1 / d]
                else:
                    d = zf[-1] - s.zc[-1]; r_.append(f_); c_.append(cid(i, j)); v_.append(-1 / d); s.outz.append((f_, d))
        s.Gz = sps.csr_matrix((v_, (r_, c_)), shape=(s.N, s.N))
        s.aR = np.array([Rf[i + 1] * (zf[j + 1] - zf[j]) for i in range(nR) for j in range(nz)])
        s.az = np.array([0.5 * (Rf[i + 1] ** 2 - Rf[i] ** 2) for i in range(nR) for j in range(nz)])
        r_, c_, v_ = [], [], []
        for i in range(nR):
            for j in range(nz):
                f_ = i * nz + j; r_.append(cid(i, j)); c_.append(f_); v_.append(s.aR[f_])
                if i < nR - 1: r_.append(cid(i + 1, j)); c_.append(f_); v_.append(-s.aR[f_])
        s.DvR = sps.csr_matrix((v_, (r_, c_)), shape=(s.N, s.N))
        r_, c_, v_ = [], [], []
        for i in range(nR):
            for j in range(nz):
                f_ = i * nz + j; r_.append(cid(i, j)); c_.append(f_); v_.append(s.az[f_])
                if j < nz - 1: r_.append(cid(i, j + 1)); c_.append(f_); v_.append(-s.az[f_])
        s.Dvz = sps.csr_matrix((v_, (r_, c_)), shape=(s.N, s.N))
        dRc = np.concatenate([np.diff(s.Rc), [Rf[-1] - s.Rc[-1]]]); dzc = np.concatenate([np.diff(s.zc), [zf[-1] - s.zc[-1]]])
        s.VR = np.array([Rf[i + 1] * (zf[j + 1] - zf[j]) * dRc[i] for i in range(nR) for j in range(nz)])
        s.Vz = np.array([0.5 * (Rf[i + 1] ** 2 - Rf[i] ** 2) * dzc[j] for i in range(nR) for j in range(nz)])
        s.nA = (nR - 1) * (nz - 1); aid = lambda i, j: i * (nz - 1) + j
        r_, c_, v_ = [], [], []
        for i in range(nR - 1):
            for j in range(nz):
                f_ = i * nz + j; dz = zf[j + 1] - zf[j]
                if j < nz - 1: r_.append(f_); c_.append(aid(i, j)); v_.append(-1 / dz)
                if j > 0: r_.append(f_); c_.append(aid(i, j - 1)); v_.append(1 / dz)
        s.CR = sps.csr_matrix((v_, (r_, c_)), shape=(s.N, s.nA))
        r_, c_, v_ = [], [], []
        for i in range(nR):
            for j in range(nz - 1):
                f_ = i * nz + j; ar = 0.5 * (Rf[i + 1] ** 2 - Rf[i] ** 2)
                if i < nR - 1: r_.append(f_); c_.append(aid(i, j)); v_.append(Rf[i + 1] / ar)
                if i > 0: r_.append(f_); c_.append(aid(i - 1, j)); v_.append(-Rf[i] / ar)
        s.Cz = sps.csr_matrix((v_, (r_, c_)), shape=(s.N, s.nA))
        r_, c_, v_ = [], [], []
        for i in range(nR):
            for j in range(nz):
                r_.append(cid(i, j)); c_.append(i * nz + j); v_.append(0.5)
                if i > 0: r_.append(cid(i, j)); c_.append((i - 1) * nz + j); v_.append(0.5)
        s.MR = sps.csr_matrix((v_, (r_, c_)), shape=(s.N, s.N))
        r_, c_, v_ = [], [], []
        for i in range(nR):
            for j in range(nz):
                r_.append(cid(i, j)); c_.append(i * nz + j); v_.append(0.5)
                if j > 0: r_.append(cid(i, j)); c_.append(i * nz + j - 1); v_.append(0.5)
        s.Mz = sps.csr_matrix((v_, (r_, c_)), shape=(s.N, s.N))
        r_, c_, v_ = [], [], []
        for i in range(nR):
            for j in range(nz):
                f_ = i * nz + j
                if i < nR - 1: r_ += [f_, f_]; c_ += [cid(i, j), cid(i + 1, j)]; v_ += [0.5, 0.5]
                else: r_.append(f_); c_.append(cid(i, j)); v_.append(1.0)
        s.AR = sps.csr_matrix((v_, (r_, c_)), shape=(s.N, s.N))
        r_, c_, v_ = [], [], []
        for i in range(nR):
            for j in range(nz):
                f_ = i * nz + j
                if j < nz - 1: r_ += [f_, f_]; c_ += [cid(i, j), cid(i, j + 1)]; v_ += [0.5, 0.5]
                else: r_.append(f_); c_.append(cid(i, j)); v_.append(1.0)
        s.Az = sps.csr_matrix((v_, (r_, c_)), shape=(s.N, s.N))
        s.rbR = np.hypot(Rf[-1], s.zc); s.rbz = np.hypot(s.Rc, zf[-1])
        s.lu = spl.splu((s.DvR @ s.GR + s.Dvz @ s.Gz).tocsc())

    def grad(s, phi, bR, bz):
        gR = s.GR @ phi; gz = s.Gz @ phi
        for (f_, d), b in zip(s.outR, bR): gR[f_] += b / d
        for (f_, d), b in zip(s.outz, bz): gz[f_] += b / d
        return gR, gz

    def poisson(s, rhs, bR, bz):
        oR = np.zeros(s.N); oz = np.zeros(s.N)
        for (f_, d), b in zip(s.outR, bR): oR[f_] = b / d
        for (f_, d), b in zip(s.outz, bz): oz[f_] = b / d
        return s.lu.solve(rhs - s.DvR @ oR - s.Dvz @ oz)

    def dual(s, gNR, gNz, tol=1e-8, itmax=260):
        A = np.zeros(s.nA); ch = 1.0
        for it in range(itmax):
            FR = gNR + s.CR @ A; Fz = gNz + s.Cz @ A
            wc = wP2(np.hypot(s.MR @ FR, s.Mz @ Fz)); wR = s.AR @ wc; wz = s.Az @ wc
            K = (s.CR.T @ sps.diags(s.VR * wR) @ s.CR + s.Cz.T @ sps.diags(s.Vz * wz) @ s.Cz).tocsc()
            An = spl.spsolve(K, -(s.CR.T @ (s.VR * wR * gNR) + s.Cz.T @ (s.Vz * wz * gNz)))
            ch = np.max(np.abs(An - A)) / max(1e-30, np.max(np.abs(An))); A = An
            if ch < tol:
                break
        FR = gNR + s.CR @ A; Fz = gNz + s.Cz @ A
        wc = wP2(np.hypot(s.MR @ FR, s.Mz @ Fz)); wR = s.AR @ wc; wz = s.Az @ wc
        cres = s.CR.T @ (s.VR * wR * FR) + s.Cz.T @ (s.Vz * wz * Fz)
        cscl = np.abs(s.CR.T) @ np.abs(s.VR * wR * FR) + np.abs(s.Cz.T) @ np.abs(s.Vz * wz * Fz)
        return dict(A=A, FR=FR, Fz=Fz, wR=wR, wz=wz, it=it + 1, change=ch, curl=float(np.max(np.abs(cres) / np.maximum(cscl, 1e-300))))


def gphi_sph(r, M):
    gN = M / r ** 2; return np.sqrt(gN ** 2 + gN) - gN


def phi_sph(rs, M, rref=1e7):
    out = []
    for r_ in np.atleast_1d(rs):
        rt = 1e4 * max(r_, 1.0, math.sqrt(M))
        out.append(-(quad(lambda s_: gphi_sph(s_, M), r_, rt, limit=400)[0] + math.sqrt(M) * math.log(rref / rt)))
    return np.array(out)


def axisym_run(rho_fun, M, Rf, zf):
    c = Cyl(Rf, zf)
    R, Z = np.meshgrid(c.Rc, c.zc, indexing="ij")
    src = 4 * math.pi * rho_fun(R, Z).ravel() * c.vol
    bRN, bzN = -M / c.rbR, -M / c.rbz
    PhiN = c.poisson(src, bRN, bzN)
    gNR, gNz = c.grad(PhiN, bRN, bzN)
    wN = wP2(np.hypot(c.MR @ gNR, c.Mz @ gNz))                        # QUMOND: grad phi_Q = gradient part of w(|g_N|) g_N
    bRp, bzp = phi_sph(c.rbR, M), phi_sph(c.rbz, M)
    phiQ = c.poisson(c.DvR @ ((c.AR @ wN) * gNR) + c.Dvz @ ((c.Az @ wN) * gNz), bRp, bzp)
    gQR, _ = c.grad(phiQ, bRp, bzp)
    sol = c.dual(gNR, gNz)
    k0 = np.arange(c.nR - 1) * c.nz                                 # the first z row (midplane), interior R faces
    gN = -gNR[k0]; gQ = gN - gQR[k0]; gA = gN - (sol["wR"] * sol["FR"])[k0]
    return dict(R=c.Rf[1:c.nR], gN=gN, gQ=gQ, gA=gA, galg=nuP2n(np.abs(gN)) * gN, it=sol["it"], change=sol["change"],
                curl=sol["curl"], cells=(c.nR, c.nz))


HZ = 0.1
tA3 = time.time()
# CONTROL: a Plummer sphere (b = 1, M = 3: y ~ 1 at r ~ 1) -- AQUAL, QUMOND and the algebraic law must coincide
Mpl = 3.0
pl = axisym_run(lambda R, Z: 3 * Mpl / (4 * math.pi) * (1 + R ** 2 + Z ** 2) ** -2.5, Mpl, faces(0.02, 1.04, 300.0), faces(0.02, 1.04, 300.0))
selp = (pl["R"] > 0.1) & (pl["R"] < 30)
pl_AQ = float(np.max(np.abs(np.log10(pl["gA"][selp] / pl["gQ"][selp])))); pl_Aa = float(np.max(np.abs(np.log10(pl["gA"][selp] / pl["galg"][selp]))))
P(f"    CONTROL Plummer sphere (M = 3 a0 b^2/G): max |log gA/gQ| = {pl_AQ:.1e} dex, max |log gA/g_alg| = {pl_Aa:.1e} dex over 0.1 < r/b < 30 "
  f"({pl['it']} Kacanov it, curl residual {pl['curl']:.1e})")
DISCS = {}
for yd in (300.0, 30.0, 3.0, 0.3):
    DISCS[yd] = axisym_run(lambda R, Z, yd=yd: yd / (4 * math.pi * HZ) * np.exp(-R) * 4 * np.exp(-2 * np.abs(Z) / HZ) / (1 + np.exp(-2 * np.abs(Z) / HZ)) ** 2,
                           yd, faces(0.02, 1.035, 300.0), faces(HZ / 8, 1.04, 300.0))
    o = DISCS[yd]
    P(f"    disc y_d = GM/(R_d^2 a0) = {yd:g}: {o['cells'][0]}x{o['cells'][1]} cells, {o['it']} Kacanov it (change {o['change']:.1e}, "
      f"curl residual {o['curl']:.1e})")
# SPARC's own per-point errors (read-only) and FP1's RAR scatter
errs = []
for fn in sorted(os.listdir(os.path.join(REPO, "real_research", "data", "sparc_data"))):
    if fn.endswith("_rotmod.dat"):
        d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", fn), comments="#")
        if d.ndim == 2 and d.shape[1] >= 3:
            ok_ = (d[:, 1] > 0) & (d[:, 2] > 0)
            errs += list(2 * d[ok_, 2] / d[ok_, 1] / math.log(10))
SPARC_MED = float(np.median(errs)); N_SPARC = len(errs)
RAR_SCATTER = 0.108
try:
    RAR_SCATTER = float(json.load(open(fp1j))["checks"]["C0 CONTROL: the committed real_research/rar_framework_a0_mlfit.py statistic is reproduced -- "
                                                       "P2 at its a0 and Upsilon = 0.70 gives 0.108 dex"]["measured"].split(" dex")[0])
except Exception:
    pass
rows3 = []
worst_AQ, worst_prof, worst_Aa, worst_Qa = 0.0, 0.0, 0.0, 0.0
for yd, o in DISCS.items():
    y = np.abs(o["gN"]); sel = (y >= 0.01) & (y <= 100) & (o["R"] >= 0.3) & (o["R"] <= 8.0)
    dAQ = np.log10(o["gA"][sel] / o["gQ"][sel]); dAa = np.log10(o["gA"][sel] / o["galg"][sel]); dQa = np.log10(o["gQ"][sel] / o["galg"][sel])
    s_ = (2 * y[sel] + 1) / (2 * (y[sel] + 1))                       # P2's d ln g / d ln g_N: the Upsilon direction
    u_ = float(np.sum(s_ * dAQ) / np.sum(s_ ** 2)); prof = dAQ - s_ * u_
    rows3.append((yd, float(y[sel].min()), float(y[sel].max()), float(np.max(np.abs(dAQ))), float(np.sqrt(np.mean(dAQ ** 2))),
                  10 ** u_ - 1, float(np.sqrt(np.mean(prof ** 2))), float(np.max(np.abs(dAa))), float(np.max(np.abs(dQa)))))
    worst_AQ = max(worst_AQ, rows3[-1][3]); worst_prof = max(worst_prof, rows3[-1][6]); worst_Aa = max(worst_Aa, rows3[-1][7]); worst_Qa = max(worst_Qa, rows3[-1][8])
    P(f"    y_d {yd:5g}: y {rows3[-1][1]:.3g}-{rows3[-1][2]:.3g} over 0.3 <= R/R_d <= 8: AQUAL/QUMOND max {rows3[-1][3]:.4f} dex, rms "
      f"{rows3[-1][4]:.4f}; Upsilon-profiled (shift {rows3[-1][5]:+.2%}) rms {rows3[-1][6]:.4f}; vs algebraic: AQUAL {rows3[-1][7]:.3f}, "
      f"QUMOND {rows3[-1][8]:.3f} dex")
    for R_ in (0.3, 1.0, 2.2, 5.0):
        k_ = int(np.argmin(np.abs(o["R"] - R_)))
        P(f"        R = {o['R'][k_]:5.2f} R_d (y = {abs(o['gN'][k_]):.3g}): gA/gQ = {o['gA'][k_] / o['gQ'][k_]:.4f}, gA/g_alg = "
          f"{o['gA'][k_] / o['galg'][k_]:.4f}, gQ/g_alg = {o['gQ'][k_] / o['galg'][k_]:.4f}")
P(f"    SPARC (read-only, {N_SPARC} points): median per-point error in log g_obs = {SPARC_MED:.4f} dex; the RAR scatter at P1's a0 = {RAR_SCATTER:.3f} dex (FP1 C0)")
OUT["numbers"]["A3"] = dict(plummer=dict(AQ=pl_AQ, Aalg=pl_Aa), discs=rows3, sparc_median_err=SPARC_MED, rar_scatter=RAR_SCATTER,
                            hz=HZ, time_s=time.time() - tA3)
a3_ctrl = pl_AQ < 3e-3 and pl_Aa < 3e-3 and all(o["curl"] < 1e-4 for o in DISCS.values())
check("A3 CONTROL: the dual (flux) solver is exact where it must be -- for a Plummer sphere AQUAL, QUMOND and the algebraic "
      "law coincide to discretisation accuracy, and every disc solve satisfies the curl equation curl(w F) = 0 to < 1e-4",
      f"Plummer max |dlog| AQUAL/QUMOND {pl_AQ:.1e}, AQUAL/algebraic {pl_Aa:.1e}; disc curl residuals "
      + ", ".join(f"{o['curl']:.0e}" for o in DISCS.values()), a3_ctrl)
check("A3 (a) THIN DISCS, AQUAL vs QUMOND: over y = 0.01-100 and 0.3 <= R/R_d <= 8 of thin exponential discs (h = 0.1 R_d) the "
      "two-field AQUAL and QUMOND realisations of P2 differ by at most the printed dex, and after profiling Upsilon by less than "
      "SPARC's median per-point error: SPARC-level data cannot tell them apart (both differ from the algebraic law by more)",
      f"max |AQUAL/QUMOND| {worst_AQ:.4f} dex, Upsilon-profiled rms <= {worst_prof:.4f} dex vs SPARC median error {SPARC_MED:.3f} dex "
      f"and RAR scatter {RAR_SCATTER:.3f} dex; algebraic-law deviations AQUAL {worst_Aa:.3f}, QUMOND {worst_Qa:.3f} dex",
      worst_prof < 0.5 * SPARC_MED and worst_AQ < RAR_SCATTER,
      "the disc family is fixed by y_d = GM/(R_d^2 a0), so the comparison is footing-free; which galaxy sits at which y_d moves with "
      "a0.  The larger effect is common to both: the algebraic RAR is not exact for discs in either field theory (inner LSB discs)")
P(f"    ({time.time() - T0:.0f} s)")

# ================================================================================================ A4 the Solar System
banner("A4  THE SOLAR SYSTEM UNDER THE DOUBLE FILTER: dual AQUAL for the smoothed Sun in the Galaxy's field (g02 read-only)")
g02p = os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "g02_filtered_efe.py")
g02src = open(g02p).read()
G2 = {"__file__": g02p, "__name__": "g02head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(g02src[:g02src.index("# ---------------------------------------------------------------- 3. the scans")], "g02_head", "exec"), G2)
PCg, GMs, AUg = G2["PC"], G2["GM"], 1.495978707e11
Q2_CEIL, M_SAT_BOUND, A_SUNWARD, PLANETS, R_SAT, Gg = G2["Q2_CEIL"], G2["M_SAT_BOUND"], G2["A_SUNWARD"], G2["PLANETS"], G2["R_SAT"], G2["G"]
EARTH_BOUND, MARS_BOUND = 3.66e-14, 3.72e-14
G_EXT = {"2.00": 2.00e-10, "2.32": 2.32e-10, "2.64": 2.64e-10}


class SphDual:
    """two-field AQUAL in DUAL form on a spherical staggered grid (r log-spaced, theta uniform): F = F_N + curl(Psi e_phi/(r sin)),
    grad phi = w(|F|) F, Kacanov on the Stokes stream function Psi at the corners; Psi = 0 on the axis and the inner sphere, and the
    analytic linear-EFE stream function on the outer sphere.  F_N is the EXACT discrete gradient of the analytic potential (so a
    uniform external field is an exact discrete solution); |F_N| at cell centres is analytic.  Units GM = a0 = 1 (r_M = 1)."""

    def __init__(s, rmin, rmax, NR=380, NT=61):
        s.rf = np.geomspace(rmin, rmax, NR + 1); s.rc = np.sqrt(s.rf[1:] * s.rf[:-1])
        s.tf = np.linspace(0.0, math.pi, NT + 1); s.tc = 0.5 * (s.tf[1:] + s.tf[:-1]); s.NR, s.NT = NR, NT
        dcos = np.cos(s.tf)[:-1] - np.cos(s.tf)[1:]
        s.vol = np.outer((s.rf[1:] ** 3 - s.rf[:-1] ** 3) / 3.0, dcos)
        s.Ar = np.outer(s.rf ** 2, dcos); s.At = np.outer((s.rf[1:] ** 2 - s.rf[:-1] ** 2) / 2.0, np.sin(s.tf))
        s.Vr = np.zeros((NR + 1, NT)); s.Vr[1:NR] = s.Ar[1:NR] * np.diff(s.rc)[:, None]
        s.Vt = np.zeros((NR, NT + 1)); s.Vt[:, 1:NT] = s.At[:, 1:NT] * (s.rc[:, None] * np.diff(s.tc)[None, :])
        s.nA = (NR - 1) * (NT - 1); aid = lambda i, j: (i - 1) * (NT - 1) + (j - 1)
        r_, c_, v_ = [], [], []
        for i in range(1, NR):
            for j in range(NT):
                if j + 1 <= NT - 1: r_.append(i * NT + j); c_.append(aid(i, j + 1)); v_.append(1.0 / s.Ar[i, j])
                if j >= 1: r_.append(i * NT + j); c_.append(aid(i, j)); v_.append(-1.0 / s.Ar[i, j])
        s.Cr = sps.csr_matrix((v_, (r_, c_)), shape=((NR + 1) * NT, s.nA))
        r_, c_, v_ = [], [], []
        for i in range(NR):
            for j in range(1, NT):
                if i + 1 <= NR - 1: r_.append(i * (NT + 1) + j); c_.append(aid(i + 1, j)); v_.append(-1.0 / s.At[i, j])
                if i >= 1: r_.append(i * (NT + 1) + j); c_.append(aid(i, j)); v_.append(1.0 / s.At[i, j])
        s.Ct = sps.csr_matrix((v_, (r_, c_)), shape=(NR * (NT + 1), s.nA))

    def FN(s, xi, eta):
        gs = lambda r: ((erf(r / (math.sqrt(2) * xi)) - math.sqrt(2 / math.pi) * (r / xi) * np.exp(-r ** 2 / (2 * xi ** 2))) if xi > 0 else 1.0) / r ** 2
        pot = lambda r, t: (-erf(r / (math.sqrt(2) * xi)) / r if xi > 0 else -1.0 / r) + eta * r * np.cos(t)
        R, T = np.meshgrid(s.rc, s.tc, indexing="ij"); Pc = pot(R, T)
        Fr = np.zeros((s.NR + 1, s.NT)); Fr[1:s.NR] = (Pc[1:] - Pc[:-1]) / np.diff(s.rc)[:, None]
        Fr[0] = gs(s.rf[0]) + eta * np.cos(s.tc); Fr[s.NR] = gs(s.rf[-1]) + eta * np.cos(s.tc)
        Ft = np.zeros((s.NR, s.NT + 1)); Ft[:, 1:s.NT] = (Pc[:, 1:] - Pc[:, :-1]) / (s.rc[:, None] * np.diff(s.tc)[None, :])
        s._FNc = (gs(R) + eta * np.cos(T), -eta * np.sin(T))
        return Fr.ravel(), Ft.ravel()

    def cellmag(s, Fr, Ft, FNr, FNt):
        dr = Fr.reshape(s.NR + 1, s.NT) - FNr.reshape(s.NR + 1, s.NT); dt = Ft.reshape(s.NR, s.NT + 1) - FNt.reshape(s.NR, s.NT + 1)
        return np.hypot(s._FNc[0] + 0.5 * (dr[1:] + dr[:-1]), s._FNc[1] + 0.5 * (dt[:, 1:] + dt[:, :-1]))

    def facew(s, wc):
        wr = np.zeros((s.NR + 1, s.NT)); wr[1:s.NR] = 0.5 * (wc[1:] + wc[:-1]); wr[0] = wc[0]; wr[s.NR] = wc[-1]
        wt = np.zeros((s.NR, s.NT + 1)); wt[:, 1:s.NT] = 0.5 * (wc[:, 1:] + wc[:, :-1]); wt[:, 0] = wc[:, 0]; wt[:, s.NT] = wc[:, -1]
        return wr.ravel(), wt.ravel()

    def psi_far(s, eta):
        if eta <= 0:
            return np.zeros(s.NT + 1)
        xe = math.sqrt(eta ** 2 + eta) - eta; muT = xe / (1 - 2 * xe); muL = 2 * xe * (1 - xe) / (1 - 2 * xe) ** 2
        th = np.linspace(0, math.pi, 4001); gq = np.sqrt(np.sin(th) ** 2 + np.cos(th) ** 2 * muT / muL)
        return np.interp(s.tf, th, cumulative_trapezoid((math.sqrt(muT / muL) / gq ** 3 - 1.0) * np.sin(th), th, initial=0.0))

    def solve(s, xi, eta, tol=1e-7, itmax=1500, Psi0=None):
        FNr0, FNt0 = s.FN(xi, eta)
        pb = s.psi_far(eta); br = np.zeros((s.NR + 1, s.NT)); bt = np.zeros((s.NR, s.NT + 1))
        br[s.NR] = (pb[1:] - pb[:-1]) / s.Ar[s.NR]; bt[s.NR - 1, 1:s.NT] = -pb[1:s.NT] / s.At[s.NR - 1, 1:s.NT]
        FNr, FNt = FNr0 + br.ravel(), FNt0 + bt.ravel()
        Psi = np.zeros(s.nA) if Psi0 is None else Psi0.copy(); Vr, Vt = s.Vr.ravel(), s.Vt.ravel(); ch = 1.0
        for it in range(itmax):
            wr, wt = s.facew(wP2(s.cellmag(FNr + s.Cr @ Psi, FNt + s.Ct @ Psi, FNr0, FNt0)))
            K = (s.Cr.T @ sps.diags(Vr * wr) @ s.Cr + s.Ct.T @ sps.diags(Vt * wt) @ s.Ct).tocsc()
            Pn = spl.spsolve(K, -(s.Cr.T @ (Vr * wr * FNr) + s.Ct.T @ (Vt * wt * FNt)))
            ch = np.max(np.abs(Pn - Psi)) / max(1e-30, np.max(np.abs(Pn))); Psi = Pn
            if ch < tol:
                break
        Fr, Ft = FNr + s.Cr @ Psi, FNt + s.Ct @ Psi
        wr, wt = s.facew(wP2(s.cellmag(Fr, Ft, FNr0, FNt0)))
        wNr, wNt = s.facew(wP2(s.cellmag(FNr0, FNt0, FNr0, FNt0)))
        return dict(Psi=Psi, gr=wr * Fr, gt=wt * Ft, gQr=wNr * FNr0, gQt=wNt * FNt0, it=it + 1, change=ch)

    def phantom(s, gr, gt):
        gr = gr.reshape(s.NR + 1, s.NT) * s.Ar; gt = gt.reshape(s.NR, s.NT + 1) * s.At
        return ((gr[1:] - gr[:-1]) + (gt[:, 1:] - gt[:, :-1])) / (4 * math.pi * s.vol)


def leg_proj(g, rho, lmax=4):
    u = np.cos(g.tf); out = []
    for l in range(lmax + 1):
        Pint = npleg.legint([0] * l + [1])
        out.append((2 * l + 1) / 2.0 * (rho * (npleg.legval(u[:-1], Pint) - npleg.legval(u[1:], Pint))[None, :]).sum(axis=1))
    return out


def ss_obs(g, rho_u, xi_u, a0):
    """FP1/g02 gates from a phantom density in units (GM = a0 = 1): g02's exact Gaussian mode kernel (read-only) as the OUTPUT
    filter, the monopole mass inside Saturn (Pitjev-Pitjeva), Q2 in Park's sign convention, the sunward anomaly at the planets."""
    rM = math.sqrt(GMs / a0); r = g.rc * rM
    rho_si = [m_ * (a0 / (Gg * rM)) for m_ in leg_proj(g, rho_u)]
    filt = [G2["gauss_filter_mode"](r, rho_si[l], l, xi_u * rM) if xi_u > 0 else rho_si[l] for l in range(5)]
    Menc = cumulative_trapezoid(4 * math.pi * filt[0] * r ** 2, r, initial=0.0)
    Q2 = 3 * Gg * 2 * math.pi * integrate.trapezoid(filt[2] * 0.4 / r, r)
    gr_ = Gg * Menc / r ** 2
    pl_ = {k_: float(np.interp(v_, r, gr_)) for k_, v_ in PLANETS.items()}
    return dict(Q2=abs(Q2) / Q2_CEIL, M=float(np.interp(R_SAT, r, Menc)) / M_SAT_BOUND, gmax=max(abs(v_) for v_ in pl_.values()) / A_SUNWARD,
                Earth=pl_["Earth"], Mars=pl_["Mars"])


yN_of = lambda gobs, a0: (-a0 + math.sqrt(a0 ** 2 + 4 * gobs ** 2)) / 2 / a0        # P2: g_obs = sqrt(g_N^2 + g_N a0)
tA4 = time.time()
# CONTROL 1: spherical (no external field) -- AQUAL and QUMOND coincide identically (Psi = 0)
g_c = SphDual(1e-3 * 0.78, 3e3, NR=300, NT=49)
oc = g_c.solve(0.78, 0.0)
sph_diff = float(np.max(np.abs(g_c.phantom(oc["gr"], oc["gt"]) - g_c.phantom(oc["gQr"], oc["gQt"]))) / np.max(np.abs(g_c.phantom(oc["gQr"], oc["gQt"]))))
# CONTROL 2: the analytic linear EFE far field dphi = -1/(sqrt(muT muL) r'), r' = r sqrt(sin^2 + cos^2 muT/muL)
ye_c = yN_of(2.32e-10, A0["canonical"]); xe_c = math.sqrt(ye_c ** 2 + ye_c) - ye_c
muT_c, muL_c = xe_c / (1 - 2 * xe_c), 2 * xe_c * (1 - xe_c) / (1 - 2 * xe_c) ** 2
o2 = g_c.solve(0.78, ye_c)
grf = o2["gr"].reshape(g_c.NR + 1, g_c.NT)
far_err = []
for rt in (300.0, 1000.0):
    i_ = int(np.argmin(np.abs(g_c.rf - rt))); rr_ = g_c.rf[i_]
    fth = 1 / np.sqrt(np.sin(g_c.tc) ** 2 + np.cos(g_c.tc) ** 2 * muT_c / muL_c)
    ana = fth / (math.sqrt(muT_c * muL_c) * rr_ ** 2)
    far_err.append(float(np.max(np.abs((grf[i_] - xe_c * np.cos(g_c.tc)) - ana)) / np.max(np.abs(ana))))
# the scans (both footings, three Galactic fields); the same solve gives QUMOND (F = F_N) for the FP1 control
XIS = [0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.05, 0.1, 0.3, 1.0]


def cross(xis, vals):
    v = np.array(vals)
    if v[-1] >= 1:
        return float("nan")
    i = len(v) - 1
    while i > 0 and v[i - 1] < 1:
        i -= 1
    if i == 0:
        return xis[0]
    return math.exp(np.interp(0.0, [math.log(v[i]), math.log(v[i - 1])], [math.log(xis[i]), math.log(xis[i - 1])]))


SSA, SSQ, FLA, FLQ = {}, {}, {}, {}
for foot, a0 in A0.items():
    rM = math.sqrt(GMs / a0)
    for tag, ge in G_EXT.items():
        g_ = SphDual(0.1 * AUg / rM, 3e3, NR=380, NT=61); Psi = None; ra, rq = [], []
        for xp in XIS:
            xi_u = xp * PCg / rM
            o_ = g_.solve(xi_u, yN_of(ge, a0), Psi0=Psi); Psi = o_["Psi"]
            ra.append(ss_obs(g_, g_.phantom(o_["gr"], o_["gt"]), xi_u, a0)); rq.append(ss_obs(g_, g_.phantom(o_["gQr"], o_["gQt"]), xi_u, a0))
        SSA[(foot, tag)], SSQ[(foot, tag)] = ra, rq
    for lab, SS, FL in (("AQUAL", SSA, FLA), ("QUMOND", SSQ, FLQ)):
        per = {t_: {gate: cross(XIS, [r_[gate] for r_ in SS[(foot, t_)]]) for gate in ("Q2", "M", "gmax")} for t_ in G_EXT}
        allf = [x_ for v_ in per.values() for x_ in v_.values()]
        fl = float("nan") if any(math.isnan(x_) for x_ in allf) else max(allf)
        binding = max(((g__, t_) for t_, v_ in per.items() for g__ in v_), key=lambda gt: per[gt[1]][gt[0]])
        window = (not math.isnan(fl)) and all(all(r_[g__] < 1 for g__ in ("Q2", "M", "gmax")) for t_ in G_EXT
                                               for r_, x_ in zip(SS[(foot, t_)], XIS) if x_ >= fl)
        FL[foot] = dict(floor=fl, binding=binding, per=per, window=window)
P(f"    CONTROL spherical (no external field): max |rho_AQUAL - rho_QUMOND| / max rho = {sph_diff:.1e} (identical: two-field AQUAL = QUMOND in spherical symmetry)")
P(f"    CONTROL linear EFE far field (canonical, 2.32e-10: x_e = {xe_c:.4f}, mu_T = {muT_c:.3f}, mu_L = {muL_c:.2f}): max relative error "
  f"of the Sun's perturbation at r = 300 / 1000 r_M: {far_err[0]:.3f} / {far_err[1]:.3f} (the nonlinear core's own multipoles fall off as ~1/r)")
P(f"\n    the double filter, g_ext = 2.32e-10, AQUAL (QUMOND on the same grid in brackets):\n    {'footing':9s} " + " ".join(f"{x_:>13.3f}" for x_ in XIS) + "   <- xi [pc]")
for foot in A0:
    for gate, lab in (("Q2", "Q2/ceil"), ("M", "M(<Sat)/bnd"), ("gmax", "g_r/sunward")):
        P(f"    {foot:9s} " + " ".join(f"{a_[gate]:6.3f}({q_[gate]:5.2f})" if a_[gate] < 10 else f"{a_[gate]:6.1f}({q_[gate]:5.1f})"
                                     for a_, q_ in zip(SSA[(foot, '2.32')], SSQ[(foot, '2.32')])) + f"   {lab}")
    for lab, FL in (("AQUAL", FLA), ("QUMOND", FLQ)):
        v_ = FL[foot]
        P(f"    -> {lab:6s} {foot}: floors per gate (g_ext 2.00/2.32/2.64): " + "; ".join(
            f"{g__} " + "/".join(f"{v_['per'][t_][g__]:.4f}" for t_ in G_EXT) for g__ in ("Q2", "M", "gmax"))
          + f";  BINDING {v_['floor']:.4f} pc ({v_['binding'][0]} at {v_['binding'][1]}e-10); window to 1 pc: {v_['window']}")
# the strict law (xi -> 0): the a0/2 tail is exact for AQUAL too (spherical AQUAL = P2); the strict QUMOND Q2 on this grid as a control
strictQ = {}
for foot, a0 in A0.items():
    rM = math.sqrt(GMs / a0); gq_ = SphDual(1e-3 * AUg / rM, 3e3, NR=360, NT=61); vals = []
    for ge in G_EXT.values():
        FNr, FNt = gq_.FN(0.0, yN_of(ge, a0))
        wNr, wNt = gq_.facew(wP2(gq_.cellmag(FNr, FNt, FNr, FNt)))
        vals.append(ss_obs(gq_, gq_.phantom(wNr * FNr, wNt * FNt), 0.0, a0)["Q2"])
    strictQ[foot] = (min(vals), max(vals))
tails = {f: 0.5 * a0 / EARTH_BOUND for f, a0 in A0.items()}
fp1_strict = {}
try:
    d1 = json.load(open(fp1j))["numbers"]["D1"]
    fp1_strict = {f: (d1[f"P2/{f}"]["Q2_min"], d1[f"P2/{f}"]["Q2_max"]) for f in A0}
except Exception:
    pass
P(f"    strict (xi -> 0): the scalar saturates at a0/2 (A2), so the Earth anomaly is a0/2 = {tails['canonical']:.0f}x / {tails['alt']:.0f}x the bound "
  f"(canonical / alt), exactly as for QUMOND; strict QUMOND Q2/ceiling on this grid {strictQ['canonical'][0]:.2f}-{strictQ['canonical'][1]:.2f} / "
  f"{strictQ['alt'][0]:.2f}-{strictQ['alt'][1]:.2f} (FP1 committed " + " / ".join(f"{fp1_strict[f][0]:.2f}-{fp1_strict[f][1]:.2f}" for f in A0 if f in fp1_strict) + "); "
  f"the strict AQUAL Q2 is NOT computed here (the dual iteration does not converge for an unsmoothed point source)")
# FP1 control: QUMOND floors on this grid vs FP1's committed ones
fp1_ok = all(abs(FLQ[f]["floor"] / FP1_FLOORS[f] - 1) < 0.03 for f in A0)
ctrl_ok = sph_diff < 1e-10 and max(far_err) < 0.03 and fp1_ok and (not fp1_strict or all(abs(strictQ[f][1] / fp1_strict[f][1] - 1) < 0.05 for f in A0))
OUT["numbers"]["A4"] = dict(spherical_identity=sph_diff, far_field_err=far_err, AQUAL_floors={f: dict(floor=v_["floor"], binding=v_["binding"],
                            per=v_["per"], window=v_["window"]) for f, v_ in FLA.items()}, QUMOND_floors={f: v_["floor"] for f, v_ in FLQ.items()},
                            strict_tail_over_bound=tails, strict_QUMOND_Q2=strictQ, time_s=time.time() - tA4,
                            table_2p32={f"{f}": [dict(xi=x_, A=a_, Q=q_) for x_, a_, q_ in zip(XIS, SSA[(f, '2.32')], SSQ[(f, '2.32')])] for f in A0})
check("A4 CONTROLS: spherical two-field AQUAL equals QUMOND identically; the dual solver reproduces the analytic linear EFE far "
      "field of the Sun to < 3% (r >= 300 r_M); the SAME grid's QUMOND reproduces FP1's committed P2 floors (0.0294 / 0.0316 pc) to < 3% and "
      "its strict Q2 to < 5%",
      f"spherical {sph_diff:.1e}; far field {far_err[0]:.3f}/{far_err[1]:.3f}; QUMOND floors {FLQ['canonical']['floor']:.4f}/"
      f"{FLQ['alt']['floor']:.4f} vs FP1 {FP1_FLOORS['canonical']:.4f}/{FP1_FLOORS['alt']:.4f}; strict QUMOND max {strictQ['canonical'][1]:.2f}/"
      f"{strictQ['alt'][1]:.2f} vs FP1 " + "/".join(f"{fp1_strict[f][1]:.2f}" for f in A0 if f in fp1_strict), ctrl_ok)
a4_ok = all(FLA[f]["window"] and FLA[f]["floor"] < 0.1 for f in A0) and all(tails[f] > 1000 for f in A0)
check("A4 THE FILTER CARRIES OVER: with the action's double filter the AQUAL scalar passes Cassini Q2, the Saturn monopole and the "
      "sunward anomaly at every planet for every xi from its binding floor to 1 pc, on both footings and at all three Galactic "
      "fields; the strict law (xi -> 0) is excluded by its exact a0/2 tail, so the filter is load-bearing here too",
      "; ".join(f"{f}: AQUAL floor {FLA[f]['floor']:.4f} pc ({FLA[f]['binding'][0]} at {FLA[f]['binding'][1]}e-10; QUMOND on the same grid "
                f"{FLQ[f]['floor']:.4f}), tail {tails[f]:.0f}x" for f in A0), a4_ok,
      "the AQUAL scalar leaks LESS than QUMOND's phantom here (its external-field suppression is stronger: mu_T ~ 4.5, mu_L ~ 50 at "
      "the Sun), so the floor drops; xi stays a declared constant")
P(f"    ({time.time() - tA4:.0f} s for A4; {time.time() - T0:.0f} s total)")

# ================================================================================================ B1 FRW background
banner("B1  THE FRW BACKGROUND OF THE REPAIRED ACTION (minisuperspace, sympy)")
tt = sp.symbols("t", real=True)
Nf, af, phb = sp.Function("N", positive=True)(tt), sp.Function("a", positive=True)(tt), sp.Function("phibar")(tt)
Lam_, rho0_, lam_ = sp.symbols("Lambda rho_0 lambda", positive=True)
Hn = sp.diff(af, tt) / (af * Nf)
# on FRW: a_m = 0, h^{mn} D phi D phi = 0 (phi = phi(t)), chi = S phi = phi (the constant mode has gain one): chassis = J = 0;
# (K - <K>) = 0; only EH, Lambda, dust and the inertia 2 lambda (n.d phi)^2 = 2 lambda phidot^2/N^2 survive
Lmini = Nf * af ** 3 / (16 * sp.pi * Gs) * (3 * Hn ** 2 - (3 * Hn) ** 2 - 2 * Lam_ + 2 * lam_ * (sp.diff(phb, tt) / Nf) ** 2) - Nf * rho0_
Hs_ = sp.symbols("H", positive=True)
eN = sp.diff(Lmini, Nf).subs(Nf, 1).subs(sp.diff(af, tt), Hs_ * af)
H2sol = sp.solve(sp.Eq(eN, 0), Hs_)
H2 = sp.simplify(H2sol[0] ** 2)
H2_gr = 8 * sp.pi * Gs * rho0_ / (3 * af ** 3) + Lam_ / 3
phi_eq = sp.simplify(sp.diff(sp.diff(Lmini, sp.diff(phb, tt)), tt).subs(Nf, 1).doit())
kin_extra = sp.simplify(H2 - H2_gr)
fr_ok = sp.simplify(kin_extra.subs(sp.diff(phb, tt), 0)) == 0 and not any(s_ in H2.free_symbols for s_ in (alph, ac_))
P(f"    H^2 = {H2};  minus GR: {kin_extra}  (vanishes for phibar-dot = 0);  phi equation: {phi_eq} = 0  =>  phibar-dot ~ a^-3")
check("B1 THE FRW BACKGROUND IS GR: on FRW the chassis and J vanish identically (a_m = 0, no spatial gradient, J(0) = 0), the "
      "Friedmann equation is GR's plus the inertia's kination term (lambda/3) phibar-dot^2, which decays as a^-6 "
      "(d/dt(a^3 lambda phibar-dot) = 0); with the declared phibar-dot = 0 it is exactly GR, and a0 is absent: a0(z)/a0(0) = 1",
      f"H^2 - H^2_GR = {kin_extra}; phi-equation {phi_eq}; a0 / alpha_c in Friedmann: False", fr_ok,
      "phibar-dot = 0 is declared initial data (like the dark mass): a free constant of motion, set to zero")

# ================================================================================================ B2 the linear FRW equations
banner("B2  THE LINEAR FRW EQUATIONS, DERIVED FROM THE ACTION (FP2's D machinery, read-only reuse, + the new sector)")
tB2 = time.time()
tq, xq, yq, zq = sp.symbols('t x y z', real=True)
X4 = (tq, xq, yq, zq)
e = sp.Symbol('e')
alc, c2c, Gc, Lam, lamc, Bsym, Csym = sp.symbols('alpha_c c_2 G Lambda lambda B_ch C_ch', real=True)
a = sp.Function('a', positive=True)(tq)
rb = sp.Function('rhobar', positive=True)(tq)
Phi, Psi, Bq, Eq, piq, th, dq, chi = [sp.Function(s_)(tq, xq) for s_ in ('Phi', 'Psi', 'B', 'E', 'pi', 'theta', 'delta', 'chi')]
FIELDS = [Phi, Psi, Bq, Eq, piq, th, dq, chi]


def ser(expr, n=2):
    ex = sp.expand(expr)
    return sp.Add(*[ex.coeff(e, i) * e ** i for i in range(n + 1)])


def powser(Xe, p_):
    Xe = sp.expand(Xe); X0, X1, X2 = Xe.coeff(e, 0), Xe.coeff(e, 1), Xe.coeff(e, 2)
    uu = (e * X1 + e ** 2 * X2) / X0
    return ser(X0 ** p_ * (1 + p_ * uu + p_ * (p_ - 1) / 2 * uu ** 2))


g4 = sp.zeros(4, 4)
g4[0, 0] = -(1 + 2 * e * Phi)
g4[0, 1] = g4[1, 0] = e * a * sp.diff(Bq, xq)
g4[1, 1] = a ** 2 * (1 - 2 * e * Psi + 2 * e * sp.diff(Eq, xq, 2))
g4[2, 2] = a ** 2 * (1 - 2 * e * Psi)
g4[3, 3] = a ** 2 * (1 - 2 * e * Psi)
gb4 = g4.subs(e, 0); hm4 = (g4 - gb4) / e; gbi4 = gb4.inv()
gi4 = (gbi4 - e * gbi4 * hm4 * gbi4 + e ** 2 * gbi4 * hm4 * gbi4 * hm4 * gbi4).applyfunc(ser)
sqg4 = powser(-ser(g4.det()), sp.Rational(1, 2))
Gam4 = [[[sp.expand(ser(sum(gi4[l, s_] * (sp.diff(g4[s_, m], X4[n]) + sp.diff(g4[s_, n], X4[m]) - sp.diff(g4[m, n], X4[s_])) for s_ in range(4)) / 2))
          for n in range(4)] for m in range(4)] for l in range(4)]


def Ric4(m, n):
    return sum(sp.diff(Gam4[l][m][n], X4[l]) - sp.diff(Gam4[l][m][l], X4[n]) +
               sum(Gam4[l][l][s_] * Gam4[s_][m][n] - Gam4[l][n][s_] * Gam4[s_][m][l] for s_ in range(4)) for l in range(4))


R4 = sp.expand(ser(sum(gi4[m, n] * Ric4(m, n) for m in range(4) for n in range(4))))
tau4 = tq + e * piq
dtau4 = [sp.diff(tau4, v_) for v_ in X4]
Xk4 = sp.expand(ser(-sum(gi4[m, n] * dtau4[m] * dtau4[n] for m in range(4) for n in range(4))))
isX4 = powser(Xk4, -sp.Rational(1, 2))
n_dn4 = [sp.expand(ser(-dtau4[m] * isX4)) for m in range(4)]
n_up4 = [sp.expand(ser(sum(gi4[m, s_] * n_dn4[s_] for s_ in range(4)))) for m in range(4)]
K4 = sp.expand(ser(sum(sp.diff(sp.expand(ser(sqg4 * n_up4[m])), X4[m]) for m in range(4)) * powser(sqg4, -1)))
acc4 = [sp.expand(ser(sum(n_up4[s_] * (sp.diff(n_dn4[m], X4[s_]) - sum(Gam4[l][s_][m] * n_dn4[l] for l in range(4))) for s_ in range(4)))) for m in range(4)]
aa4 = sp.expand(ser(sum(gi4[m, s_] * acc4[m] * acc4[s_] for m in range(4) for s_ in range(4))))
Kbar = 3 * sp.diff(a, tq) / a
dK_leaf = ser(K4 - (Kbar + e * piq * sp.diff(Kbar, tq) + e ** 2 * piq ** 2 * sp.diff(Kbar, tq, 2) / 2))
dTd = [sp.diff(tq + e * th, v_) for v_ in X4]
Ldust = -rb * (1 + e * dq) / 2 * sqg4 * (sum(gi4[m, s_] * dTd[m] * dTd[s_] for m in range(4) for s_ in range(4)) + 1)
# the new sector around the zero-field background chi = e chi_1 (S = 1 at cosmological k: xi k ~ 1e-8):
#   h^{mn} a_m D_n chi = a^m d_m chi (n.a = 0),  h^{mn} D chi D chi = g^{mn} d chi d chi + (n.d chi)^2,  (n.d phi)^2
dchi = [sp.diff(e * chi, v_) for v_ in X4]
ndchi = sp.expand(ser(sum(n_up4[m] * dchi[m] for m in range(4))))
a_dchi = sp.expand(ser(sum(gi4[m, s_] * acc4[m] * dchi[s_] for m in range(4) for s_ in range(4))))
h_dchi2 = sp.expand(ser(sum(gi4[m, s_] * dchi[m] * dchi[s_] for m in range(4) for s_ in range(4)) + ndchi ** 2))
Lnew = Bsym * a_dchi + Csym * h_dchi2 + 2 * lamc * ndchi ** 2
Lt = sp.expand(ser(sqg4 * (R4 - 2 * Lam + alc * aa4 + Lnew) - c2c * sqg4 * dK_leaf ** 2 + 16 * sp.pi * Gc * Ldust))
L1, L2 = Lt.coeff(e, 1), Lt.coeff(e, 2)
bgE = [sp.simplify(ee.lhs - ee.rhs) for ee in euler_equations(L1, FIELDS, [tq, xq])]
rbs = sp.solve(bgE[0], rb)[0]
adds = sp.solve(bgE[1].subs(rb, rbs), sp.diff(a, tq, 2))[0]
ELq = euler_equations(L2, FIELDS, [tq, xq])
kF = sp.Symbol('k', positive=True)
amp = {F: sp.Function(F.func.__name__ + 'k')(tq) for F in FIELDS}


def fourier(ex):
    for F in FIELDS:
        ex = ex.subs(F, amp[F] * sp.exp(sp.I * kF * xq))
    return sp.expand(sp.simplify(ex.doit() * sp.exp(-sp.I * kF * xq)))


def bgsub(ex):
    ex = ex.subs({amp[Bq]: 0, amp[Eq]: 0}).doit()
    ex = ex.subs(sp.diff(a, tq, 3), sp.diff(adds, tq)).subs(sp.diff(a, tq, 2), adds).subs(rb, rbs)
    ex = ex.subs(sp.diff(a, tq, 2), adds)
    return sp.expand(sp.simplify(ex))


Eg = [bgsub(fourier(ee.lhs - ee.rhs)) for ee in ELq]
names8 = ['Phi', 'Psi', 'B', 'E', 'pi', 'theta', 'delta', 'chi']
newparts = {nm: sp.factor(sp.expand(ee - ee.subs({Bsym: 0, Csym: 0, lamc: 0}))) for nm, ee in zip(names8, Eg)}
for nm in names8:
    P(f"    [{nm:5s}] new-sector part: {newparts[nm]}")
# the MOND term at zero field: J(Y) with Y = O(e^2) is O(e^3) -- no quadratic part, zero tangent (FP3 B1's order count, re-derived)
Jser = sp.series(Jsym.subs(Yq, e ** 2 * sp.Symbol('Y1', positive=True)), e, 0, 4).removeO()
J_order = min(sp.Poly(sp.expand(Jser), e).monoms())[0]
J_tangent = sp.limit(sp.diff(Jsym, Yq), Yq, 0)
unchanged = all(newparts[nm] == 0 for nm in ('Psi', 'B', 'E', 'theta', 'delta'))
touched = all(newparts[nm] != 0 for nm in ('Phi', 'pi', 'chi'))
P(f"    J_P2 around zero field: leading order e^{J_order} (the quadratic action has no J part); zero-field tangent J'(0) = {J_tangent}")
P(f"    ({time.time() - tB2:.0f} s)")
OUT["numbers"]["B2"] = {nm: str(v_) for nm, v_ in newparts.items()}
check("B2 THE LINEAR FRW EQUATIONS, DERIVED: J_P2 is O(eps^3) around the zero-field background with J'(0) = 0 (no infinite "
      "tangent: FP3's G1t door, verified), so the quadratic action carries the chassis and the inertia only; the new sector "
      "enters exactly three equations -- the lapse (B_ch k^2 a chi), the khronon (B_ch k^2 d(a chi)/dt) and phi's own "
      "(4 lambda a^3 (chi'' + 3H chi') = k^2 a [B_ch (Phi - pi') + 2 C_ch chi]) -- and leaves the Psi, B, E and dust equations GR + khronon",
      f"J order e^{J_order}; tangent {J_tangent}; untouched equations {unchanged}; touched {touched}",
      J_order == 3 and J_tangent == 0 and unchanged and touched)

# ================================================================================================ B3 zero-field well-posedness
banner("B3  THE ZERO-FIELD LINEARISATION: the Minkowski block of the repaired action (unitary gauge, symbolic second variation)")
tB3 = time.time()
tt_, xx_, yy_, zz_ = sp.symbols('t x y z', real=True)
X3m = (xx_, yy_, zz_)
eb = sp.Symbol('e_b')
alm, c2m, Cph, lmm, sgm = sp.symbols('alpha_c c_2 C_phi lambda sigma', real=True)
nf, pf, Bf, Sf, Ff = [sp.Function(s_)(tt_, xx_, yy_, zz_) for s_ in ('n', 'psi', 'B', 'S', 'phi')]
Nl = sp.exp(eb * nf)
gam = sp.diag(*[sp.exp(-2 * eb * pf)] * 3)
gin = gam.inv()
Ni = [eb * (sp.diff(Bf, X3m[0]) + Sf), eb * sp.diff(Bf, X3m[1]), eb * sp.diff(Bf, X3m[2])]
Gm3 = [[[sum(gin[a_, d_] * (sp.diff(gam[d_, b_], X3m[c_]) + sp.diff(gam[d_, c_], X3m[b_]) - sp.diff(gam[b_, c_], X3m[d_])) for d_ in range(3)) / 2
         for c_ in range(3)] for b_ in range(3)] for a_ in range(3)]
DN = [[sp.diff(Ni[j], X3m[i]) - sum(Gm3[kq][i][j] * Ni[kq] for kq in range(3)) for j in range(3)] for i in range(3)]
Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(gam[i, j], tt_) - DN[i][j] - DN[j][i]) / (2 * Nl))
Kup = gin * Kij * gin
KK = sum(Kij[i, j] * Kup[i, j] for i in range(3) for j in range(3))
trK = sum(gin[i, j] * Kij[i, j] for i in range(3) for j in range(3))


def Ric3(b_, c_):
    return sum(sp.diff(Gm3[a_][b_][c_], X3m[a_]) - sp.diff(Gm3[a_][b_][a_], X3m[c_]) +
               sum(Gm3[a_][a_][d_] * Gm3[d_][b_][c_] - Gm3[a_][c_][d_] * Gm3[d_][b_][a_] for d_ in range(3)) for a_ in range(3))


R3 = sum(gin[b_, c_] * Ric3(b_, c_) for b_ in range(3) for c_ in range(3))
ai = [sp.diff(sp.log(Nl), xi_) for xi_ in X3m]
aa = sum(gin[i, j] * ai[i] * ai[j] for i in range(3) for j in range(3))
Fi = [sp.diff(eb * Ff, xi_) for xi_ in X3m]
Xi = [sgm * f_ for f_ in Fi]                                         # D_i chi, chi = S phi -> sigma(k) phi mode by mode
chassis = Bsym * sum(gin[i, j] * ai[i] * Xi[j] for i in range(3) for j in range(3)) + Csym * sum(gin[i, j] * Xi[i] * Xi[j] for i in range(3) for j in range(3))
Jquad = -2 * Cph * sum(gin[i, j] * Fi[i] * Fi[j] for i in range(3) for j in range(3))   # -2 alpha^2 J about a frozen background: C_phi = C_T or C_L
ndphi = (sp.diff(eb * Ff, tt_) - sum(sum(gin[i, j] * Ni[j] for j in range(3)) * Fi[i] for i in range(3))) / Nl
Lfull = Nl * sp.exp(-3 * eb * pf) * (KK - trK ** 2 + R3 + alm * aa - c2m * trK ** 2 + chassis + Jquad + 2 * lmm * ndphi ** 2)
L2f = sp.expand((sp.diff(Lfull, eb, 2) / 2).subs(eb, 0))
ELf = euler_equations(L2f, [nf, pf, Bf, Sf, Ff], [tt_, xx_, yy_, zz_])
kq_, wq_ = sp.symbols('k omega', real=True)
An, Ap, AB, AS, AF = sp.symbols('A_n A_psi A_B A_S A_phi')
phs = sp.exp(sp.I * (kq_ * zz_ - wq_ * tt_))
fsub = {nf: An * phs, pf: Ap * phs, Bf: AB * phs, Sf: AS * phs, Ff: AF * phs}
ELk_gen = [sp.expand(sp.simplify((e_.lhs - e_.rhs).subs(fsub).doit() / phs)) for e_ in ELf]
Bu, Cu = BCH(alm)
ELk = [sp.expand(e_.subs({Bsym: Bu, Csym: Cu})) for e_ in ELk_gen]
for nm, e_ in zip(["n", "psi", "B", "S", "phi"], ELk):
    P(f"    dL/d{nm:4s}: {sp.factor(e_)}")
Mblk = sp.Matrix([[sp.expand(sp.diff(ELk[r_], v_)) for v_ in (Ap, An, AB, AF)] for r_ in (1, 0, 2, 4)])
detM = sp.factor(sp.expand(Mblk.det(method='berkowitz')))
U2 = sp.Symbol('U2')
polyU = sp.Poly(sp.numer(sp.together(detM.subs(wq_, sp.sqrt(U2) * kq_))), U2)
roots0 = [sp.simplify(r_) for r_ in sp.solve(polyU.as_expr().subs(Cph, 0), U2)]
cfs = polyU.all_coeffs()
prod0 = sp.simplify((cfs[-1] / cfs[0]).subs(Cph, 0))
P(f"    det M = {detM}")
P(f"    zero field (C_phi = 0): omega^2/k^2 roots {roots0};  product of roots {prod0}")
# the naive chassis, as a control
ELk_nv = [sp.expand(e_.subs({Bsym: 4, Csym: -2})) for e_ in ELk_gen]
Mnv = sp.Matrix([[sp.expand(sp.diff(ELk_nv[r_], v_)) for v_ in (Ap, An, AB, AF)] for r_ in (1, 0, 2, 4)])
pnv = sp.Poly(sp.numer(sp.together(sp.factor(Mnv.det(method='berkowitz')).subs(wq_, sp.sqrt(U2) * kq_))), U2)
prod_nv = sp.factor((pnv.all_coeffs()[-1] / pnv.all_coeffs()[0]).subs(Cph, 0))
sum_nv = sp.factor((-pnv.all_coeffs()[1] / pnv.all_coeffs()[0]).subs(Cph, 0))
neg_nv = sp.factor(sp.limit(prod_nv / sum_nv / alm, alm, 0) * alm)                # the growing root ~ product/sum, O(alpha_c)
# E(C_phi): the lambda = 0 root is BPS's omega^2 = c_2 (2 - E) k^2/(E (2 + 3 c_2)) with E_AQUAL
EAQ = (2 * (2 - alm) * sgm ** 2 + 2 * alm * Cph) / ((2 - alm) * sgm ** 2 + 2 * Cph)
root_l0 = sp.solve(sp.numer(sp.together(detM.subs(lmm, 0).subs(wq_, sp.sqrt(U2) * kq_))), U2)
E_ok = len(root_l0) == 1 and sp.simplify(root_l0[0] - c2m * (2 - EAQ) / (EAQ * (2 + 3 * c2m))) == 0
E_lim = (sp.simplify(EAQ.subs(Cph, 0)), sp.limit(EAQ, Cph, sp.oo), sp.factor(sp.simplify(sp.diff(EAQ, Cph))))
# numbers: the naive chassis's growing band (bounded by the filter) at the window's alpha_c, lambda = 1, xi = 0.03 pc
LAMEFF_NV = 1.0 + (2 + 3 * C2_FLOOR_FP2) / C2_FLOOR_FP2         # lambda = 1 plus the khronon's inertia at FP2's c_2 floor
rate_nv = math.sqrt(AC_MAX / (2.0 * LAMEFF_NV)) / math.sqrt(math.e)   # max_k sqrt(alpha_c sigma^2/(2 lambda_eff)) k, sigma = e^{-xi^2 k^2/2}, per (c/xi)
efold_nv_yr = (0.03 * PC_M / cc) / rate_nv / 3.156e7
roots_pos = (len(roots0) == 2 and any(sp.simplify(r_) == 0 for r_ in roots0))
fast = [r_ for r_ in roots0 if sp.simplify(r_) != 0]
fast_pos = bool(fast) and all(float(fast[0].subs({alm: av, c2m: cv, lmm: lv, sgm: sv})) > 0
                              for av in (1e-13, 3.2e-9, 1.0) for cv in (1e-4, 7.29e-3, 1.0) for lv in (1e-3, 1.0, 1e8) for sv in (1.0, 1e-3))
P(f"    CONTROL naive chassis: product of the zero-field roots {prod_nv} < 0 -> one growing mode, omega^2/k^2 ~ {neg_nv}; with the filter "
  f"the band is bounded: max rate sqrt(alpha_c/2 lambda_eff)/(sqrt(e) xi) -> e-fold {efold_nv_yr:.0f} yr at alpha_c = {AC_MAX:.1e}, lambda = 1, c_2 = {C2_FLOOR_FP2:.2e}, xi = 0.03 pc")
P(f"    E_AQUAL(C_phi) = {EAQ}: lambda = 0 root = BPS(E_AQUAL) {E_ok}; E(0) = {E_lim[0]}, E(oo) = {E_lim[1]}, dE/dC_phi = {E_lim[2]} < 0")
P(f"    (the C-H core, FP5 C3: E(C) = alpha_c + 2C/(1 + C) -> alpha_c + 2 > 2 at zero field: Hadamard ill-posed)  ({time.time() - tB3:.0f} s)")
OUT["numbers"]["B3"] = dict(det=str(detM), zero_field_roots=[str(r_) for r_ in roots0], naive_product=str(prod_nv), E_AQUAL=str(EAQ))
check("B3 ZERO-FIELD WELL-POSEDNESS RESTORED: at zero field the repaired action's scalar block has omega^2 = 0 (the marginal "
      "MOND-khronon mode: at most linear growth, no Hadamard instability) and omega^2 = (2 - alpha_c)(c_2 lambda + (2 + 3c_2) "
      "sigma^2) k^2/(alpha_c lambda (2 + 3c_2)) > 0 at every alpha_c, c_2, lambda and filter factor; the khronon's effective BPS "
      "coefficient is E(C_phi) = [2(2 - alpha_c) sigma^2 + 2 alpha_c C_phi]/[(2 - alpha_c) sigma^2 + 2 C_phi], in (alpha_c, 2] "
      "(= 2 only at exactly zero field) -- FP5's E = 2 + alpha_c > 2 band is gone.  CONTROL: the naive chassis has a growing mode",
      f"roots {roots0}; fast root positive on the grid {fast_pos}; E = BPS {E_ok}; naive product {prod_nv}",
      roots_pos and fast_pos and E_ok and sp.simplify(E_lim[0] - 2) == 0 and sp.simplify(E_lim[1] - alm) == 0,
      "the perfect square is what makes the zero-field mode exactly marginal; any Newtonian residual of the wrong sign (the naive "
      "chassis) turns it into a growing band k xi <~ 1 with an e-fold of ~1e4-1e5 yr (bounded by the filter, but present)")

# ================================================================================================ B4 sub-horizon reduction
banner("B4  SUB-HORIZON REDUCTION OF THE DERIVED FRW EQUATIONS: slip, G_eff and phi's inertia-limited response")
ep = sp.Symbol('epsilon', positive=True); lh = sp.Symbol('lambdahat', positive=True)
scl = {amp[Phi]: ep ** 2 * amp[Phi], amp[Psi]: ep ** 2 * amp[Psi], amp[chi]: ep ** 2 * amp[chi], amp[piq]: ep ** 4 * amp[piq], amp[th]: ep ** 2 * amp[th]}


def lead_order(ex):
    ex = ex.subs(kF, kF / ep).subs(lamc, lh / ep ** 2)
    for F_, v_ in scl.items():
        ex = ex.subs(F_, v_)
    ex = sp.expand(ex.doit())
    lo = min(m_[0] for m_ in sp.Poly(ex, ep).monoms())
    return sp.expand(ex.coeff(ep, lo))


Bf_, Cf_ = BCH(alc)
LEAD = {nm: lead_order(ee.subs({Bsym: Bf_, Csym: Cf_})) for nm, ee in zip(names8, Eg)}
Ps_, Fs_, Xs_, ds_ = amp[Psi], amp[Phi], amp[chi], amp[dq]
slip_sol = sp.solve(LEAD['Psi'], Ps_)
slip0 = len(slip_sol) == 1 and sp.simplify(slip_sol[0] - Fs_) == 0
rho_bar = sp.simplify(rbs)                                           # 8 pi G rho_bar = (3 adot^2 - Lambda a^2)/a^2 (the derived Friedmann)
phiF = sp.solve(LEAD['Phi'].subs(Ps_, Fs_), Fs_)[0]
poisson_res = sp.simplify((kF ** 2 / a ** 2) * (phiF - Xs_) + 4 * sp.pi * Gc * rho_bar * ds_ / (1 - alc / 2))
chi_red = sp.expand(LEAD['chi'].subs(Ps_, Fs_).subs(Fs_, phiF))
chi_target = sp.expand(-4 * a ** 3 * (lh * (sp.diff(Xs_, tq, 2) + 3 * sp.diff(a, tq) / a * sp.diff(Xs_, tq)) + 4 * sp.pi * Gc * rho_bar * ds_))
chi_res = sp.simplify(sp.expand(chi_red - chi_target).subs(sp.diff(a, tq, 2), adds))
th_sol = sp.solve(LEAD['delta'], sp.diff(amp[th], tq))
cont = sp.solve(sp.simplify(LEAD['theta'].subs(sp.diff(a, tq, 2), adds)), sp.diff(ds_, tq))
dust_ok = (len(th_sol) == 1 and sp.simplify(th_sol[0] - Fs_) == 0 and len(cont) == 1
           and sp.simplify(cont[0] + kF ** 2 / a ** 2 * amp[th]) == 0)
# matter-era particular solution: chi = C delta with delta ~ a ~ t^(2/3), H = 2/(3t), 4 pi G rho = (2/3) t^-2
ts = sp.symbols('t_s', positive=True); Cp_ = sp.symbols('C_p', real=True)
dl_ = ts ** sp.Rational(2, 3)
Cpart = sp.solve(sp.Eq(lh * (sp.diff(Cp_ * dl_, ts, 2) + 3 * (2 / (3 * ts)) * sp.diff(Cp_ * dl_, ts)), -sp.Rational(2, 3) * ts ** -2 * dl_), Cp_)[0]
Ceps = sp.simplify(-Cpart * (kF ** 2) / (sp.Rational(3, 2) * (2 / (3 * ts)) ** 2) * (2 / (3 * ts)) ** 2)   # -(k/a)^2 chi / (4 pi G rho delta) at H -> 1 units
# the khronon's own inertia (next order): the slow Minkowski root at alpha_c -> 0 is C_phi c_2 k^2/(c_2 lambda + (2 + 3 c_2) sigma^2)
slowM = sp.factor(sp.limit((cfs[-1] / cfs[0]) / (-cfs[1] / cfs[0]), alm, 0))
lam_eff_form = sp.simplify(Cph / slowM)
P(f"    leading order (k -> k/eps, potentials ~ eps^2, pi ~ eps^4, lambda ~ lambdahat/eps^2):")
for nm in ('Phi', 'Psi', 'chi', 'delta', 'theta'):
    P(f"      [{nm:5s}] {sp.factor(LEAD[nm])}")
P(f"    slip: Psi = {slip_sol};  Poisson: (k/a)^2 (Phi - chi) + 4 pi G_N rho delta = {poisson_res};  phi: lambda (chi'' + 3H chi') + 4 pi G rho delta, ratio - 1 = {chi_res}")
P(f"    dust: theta' = Phi and delta' = -(k/a)^2 theta: {dust_ok}  =>  delta'' + 2H delta' = 4 pi G_N rho delta - (k/a)^2 chi")
P(f"    matter era: chi = {Cpart} delta, so G_eff/G_N - 1 = (2/5)(ck/aH)^2/lambda_eff (x G/G_N);  slow Minkowski root {slowM}  =>  "
  f"lambda_eff = {lam_eff_form}")
OUT["numbers"]["B4"] = dict(slow_root=str(slowM), lambda_eff=str(lam_eff_form), chi_particular=str(Cpart))
check("B4 LINEAR COSMOLOGY, DERIVED: sub-horizon the repaired action gives NO slip (Psi = Phi), the Poisson law "
      "(k/a)^2 (Phi - chi) = -4 pi G_N rho delta, phi's equation lambda (chi'' + 3H chi') = -4 pi G rho delta with NO restoring "
      "term at linear order, and the dust's delta'' + 2H delta' = 4 pi G_N rho delta - (k/a)^2 chi: the MOND scalar responds to the "
      "web by INERTIA alone, G_eff/G_N = 1 + (2/5)(ck/aH)^2/lambda_eff in the matter era, with lambda_eff = lambda + (2 + 3c_2)/c_2 "
      "(the khronon locked to phi adds its own inertia; next order, from the exact slow root)",
      f"slip {slip0}; Poisson residual {poisson_res}; phi residual {chi_res}; dust {dust_ok}; chi_part {Cpart}; lambda_eff {lam_eff_form}",
      slip0 and poisson_res == 0 and chi_res == 0 and dust_ok and sp.simplify(Cpart + sp.Rational(3, 5) / lh) == 0
      and sp.simplify(lam_eff_form - (lmm + (2 + 3 * c2m) * sgm ** 2 / c2m)) == 0,
      "FP3's order count is right for J (it drops out) but not for the scalar's linear coupling: the chassis is Newton-strength, "
      "and at zero field nothing but inertia resists the source -- a k^2-growing fifth force (ck/aH)^2/lambda_eff")

# ================================================================================================ B5 sigma_8
banner("B5  sigma_8 WITH NO GATE: the derived linear system, and the physical-amplitude yardstick (L341/FP3), both footings")
tB5 = time.time()
Mpc_ = 3.0856775814913673e22
h_ = 0.6736; om_b, om_c = 0.02237, 0.1200; T_CMB = 2.7255; N_eff = 3.046; ns_ = 0.965
H0 = 100 * h_ * 1e3 / Mpc_; rho_crit0 = 3 * H0 ** 2 / (8 * math.pi * Gn)
Og = (4 * 5.670374419e-8 * T_CMB ** 4 / cc ** 3) / rho_crit0; Or = Og * (1 + N_eff * (7 / 8) * (4 / 11) ** (4 / 3))
Ob, Oc = om_b / h_ ** 2, om_c / h_ ** 2; Om = Ob + Oc; OL = 1 - Om - Or; SIG8 = 0.811
Ez = lambda a_: math.sqrt(Or / a_ ** 4 + Om / a_ ** 3 + OL)
dlnH = lambda a_: 0.5 * (-4 * Or / a_ ** 4 - 3 * Om / a_ ** 3) / Ez(a_) ** 2


def T_EH98(k):
    th_ = T_CMB / 2.7; s_ = 44.5 * math.log(9.83 / (Om * h_ * h_)) / math.sqrt(1 + 10 * om_b ** 0.75)
    ag = 1 - 0.328 * math.log(431 * Om * h_ * h_) * (Ob / Om) + 0.38 * math.log(22.3 * Om * h_ * h_) * (Ob / Om) ** 2
    ge = Om * h_ * (ag + (1 - ag) / (1 + (0.43 * k * s_ / h_) ** 4)); qq = k * th_ * th_ / ge
    L_ = math.log(2 * math.e + 1.8 * qq); C_ = 14.2 + 731.0 / (1 + 62.5 * qq); return L_ / (L_ + C_ * qq * qq)


P_un = lambda kh: (kh * h_) ** ns_ * T_EH98(kh * h_) ** 2
Wth = lambda x_: 3 * (math.sin(x_) - x_ * math.cos(x_)) / x_ ** 3
PN = (SIG8 / math.sqrt(quad(lambda kh: kh ** 2 * P_un(kh) * Wth(8 * kh) ** 2 / (2 * math.pi ** 2), 1e-4, 60, limit=600)[0])) ** 2
KH = np.logspace(math.log10(0.02), math.log10(20.0), 48)
DREF = np.array([math.sqrt(k ** 3 * PN * P_un(k) / (2 * math.pi ** 2)) for k in KH])
W8 = np.array([Wth(8 * k) ** 2 for k in KH])
sigma8_of = lambda D0, kmax=99.0: math.sqrt(np.trapz((D0 ** 2 * W8)[KH <= kmax], np.log(KH[KH <= kmax])))
A_I = 1 / 1001.0
r0 = solve_ivp(lambda N_, Y: [Y[1], 1.5 * (Om / math.exp(3 * N_) / Ez(math.exp(N_)) ** 2) * Y[0] - (2 + dlnH(math.exp(N_))) * Y[1]],
               (math.log(A_I), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-10, atol=1e-14).y[0][-1]
DI = DREF / r0


def grow_lin(kh, lam_eff, fifth=True):
    """the derived sub-horizon system in N = ln a (B4), alpha_c -> 0 (its O(1e-9) renormalisations are invisible here)"""
    kph = kh * h_ / Mpc_

    def rhs(N_, Y):
        a_ = math.exp(N_); d_, dp_, x_, xp_ = Y; Oma = Om / a_ ** 3 / Ez(a_) ** 2
        q2 = (cc * kph / (a_ * H0 * Ez(a_))) ** 2
        return [dp_, 1.5 * Oma * d_ - (q2 * x_ if fifth else 0.0) - (2 + dlnH(a_)) * dp_, xp_, -1.5 * Oma * d_ / lam_eff - (3 + dlnH(a_)) * xp_]
    x0 = -0.6 / lam_eff
    return solve_ivp(rhs, (math.log(A_I), 0.0), [1.0, 1.0, x0, x0], method="LSODA", rtol=1e-9, atol=1e-14).y[0][-1]


S8_LCDM = sigma8_of(np.array([DI[i] * grow_lin(k, 1e30, fifth=False) for i, k in enumerate(KH)]))
S8_LCDM_1 = sigma8_of(np.array([DI[i] * grow_lin(k, 1e30, fifth=False) for i, k in enumerate(KH)]), kmax=1.0)
s8_lin = lambda le, kmax=99.0: sigma8_of(np.array([DI[i] * grow_lin(k, le) for i, k in enumerate(KH)]), kmax) / (S8_LCDM if kmax > 50 else S8_LCDM_1)


def s8_phys(le, a0v, mode):
    """L341/FP3's physical-amplitude yardstick with the AQUAL scalar's own speed: boost = 1 + C_Q/(1 + (H/(c_s k))^2),
    C_Q = nu_P2(y) - 1 at the linear field's amplitude y, c_s^2 = C_phi/lambda_eff with C_phi = 1/C_Q (A2's duality)."""
    def boost(y, a_, kh):
        CQ = math.sqrt(1 + 1 / max(y, 1e-300)) - 1.0
        cs = cc / math.sqrt(CQ * le); kph = kh * h_ / (a_ * Mpc_)
        return 1.0 + CQ / (1.0 + (H0 * Ez(a_) / (cs * kph)) ** 2)
    if mode == "rms":
        def rhs(N_, Y):
            a_ = math.exp(N_); D_, Dp = Y; rho_ = Om * rho_crit0 / a_ ** 3
            gk = 4 * math.pi * Gn * rho_ * np.abs(DI * D_) / (KH * h_ / (a_ * Mpc_))
            grms = math.sqrt(np.trapz(gk ** 2 / KH, KH) / np.trapz(1 / KH, KH))
            return [Dp, 1.5 * (Om / a_ ** 3 / Ez(a_) ** 2) * boost(grms / a0v, a_, 1.0) * D_ - (2 + dlnH(a_)) * Dp]
        D0 = DI * solve_ivp(rhs, (math.log(A_I), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-7, atol=1e-12).y[0][-1]
    else:
        D0 = []
        for i, kh in enumerate(KH):
            def rhs(N_, Y, kh=kh):
                a_ = math.exp(N_); d_, dp_ = Y
                gN = 4 * math.pi * Gn * Om * rho_crit0 / a_ ** 3 * abs(d_) / (kh * h_ / (a_ * Mpc_))
                return [dp_, 1.5 * (Om / a_ ** 3 / Ez(a_) ** 2) * boost(gN / a0v, a_, kh) * d_ - (2 + dlnH(a_)) * dp_]
            D0.append(solve_ivp(rhs, (math.log(A_I), 0.0), [DI[i], DI[i]], method="LSODA", rtol=1e-7, atol=1e-22).y[0][-1])
        D0 = np.array(D0)
    return sigma8_of(D0) / S8_LCDM


def thresh(fun, lo=1e2, hi=1e11, target=1.02):
    fl, fh = math.log(lo), math.log(hi)
    for _ in range(40):
        mid = 0.5 * (fl + fh)
        if fun(math.exp(mid)) > target: fl = mid
        else: fh = mid
    return math.exp(fh)


LAM_KH0 = (2 + 3 * C2_FLOOR_FP2) / C2_FLOOR_FP2                     # lambda_eff at lambda = 0, c_2 at FP2's tracking floor
LAM_TRACK = 0.01 * (cc / V_TRACK) ** 2                              # C_phi >= 0.01 (FP2's 'C <= 100') tracked at 3 x 600 km/s
grid_le = [LAM_KH0, 1e4, 1e6, 1e7, 3e7, 1e8, 1e9]
lin_tab = {le: s8_lin(le) for le in grid_le}
th_lin = thresh(s8_lin); th_lin1 = thresh(lambda le: s8_lin(le, kmax=1.0))
phys_tab = {(f, m): {le: s8_phys(le, A0[f], m) for le in (LAM_KH0, 1e5, 1e7, 1e8)} for f in A0 for m in ("rms", "permode")}
th_phys = {(f, m): thresh(lambda le, f=f, m=m: s8_phys(le, A0[f], m), lo=1e2, hi=1e11) for f in A0 for m in ("rms", "permode")}
lcdm_limit = s8_lin(1e14)
P(f"    LCDM control: sigma_8 = {S8_LCDM:.5f} (FP3/L341 yardstick: 0.81009); lambda_eff -> oo gives the ratio {lcdm_limit:.6f}")
P("    linear (derived system):  " + ";  ".join(f"lambda_eff {le:.3g}: {v_:.4g}" for le, v_ in lin_tab.items()))
P(f"    sigma_8 <= 1.02 x LCDM needs lambda_eff >= {th_lin:.2e} (k <= 20 h/Mpc, the yardstick's range) / {th_lin1:.2e} (k <= 1 h/Mpc only)")
for (f, m), tab in phys_tab.items():
    P(f"    physical amplitude {f:9s} {m:7s}: " + ";  ".join(f"lambda_eff {le:.3g}: {v_:.4g}" for le, v_ in tab.items())
      + f";  sigma_8 <= 1.02 needs lambda_eff >= {th_phys[(f, m)]:.2e}")
P(f"    lower gate sigma_8/sigma_8,LCDM >= 0.922: the scalar only adds attraction, so every row passes it; the upper gate decides")
P(f"    ({time.time() - tB5:.0f} s)")
OUT["numbers"]["B5"] = dict(S8_LCDM=S8_LCDM, linear={f"{le:.4g}": v_ for le, v_ in lin_tab.items()}, lin_threshold=th_lin, lin_threshold_k1=th_lin1,
                            phys={f"{k_[0]}/{k_[1]}": {f"{le:.4g}": v_ for le, v_ in tab.items()} for k_, tab in phys_tab.items()},
                            phys_threshold={f"{k_[0]}/{k_[1]}": v_ for k_, v_ in th_phys.items()}, lambda_eff_lambda0=LAM_KH0)
b5_ok = (abs(S8_LCDM / 0.81009 - 1) < 1e-3 and abs(lcdm_limit - 1) < 1e-3 and all(v_ > 10 for v_ in (phys_tab[(f, 'rms')][LAM_KH0] for f in A0))
         and th_lin > 1e6 and min(th_phys.values()) > 1e6 and all(v_ >= 0.922 for tab in phys_tab.values() for v_ in tab.values()))
check("B5 sigma_8 WITH NO GATE, verified both ways: the LCDM limit (lambda_eff -> oo) is recovered and L341's yardstick reproduced; "
      "at the smallest inertia the action allows (lambda = 0, the khronon's own (2 + 3c_2)/c_2 = 277 at FP2's floor) the web reaches "
      "MOND equilibrium and sigma_8 is L341's ~ 20x; sigma_8 <= 1.02 x LCDM needs lambda_eff >~ 1e7-1e8 (linear and physical-amplitude "
      "yardsticks, both footings); the lower gate (>= 0.922) never binds",
      f"LCDM {S8_LCDM:.5f}; at lambda_eff = {LAM_KH0:.0f}: rms {phys_tab[('canonical', 'rms')][LAM_KH0]:.1f}/{phys_tab[('alt', 'rms')][LAM_KH0]:.1f}, "
      f"per-mode {phys_tab[('canonical', 'permode')][LAM_KH0]:.1f}/{phys_tab[('alt', 'permode')][LAM_KH0]:.1f}; thresholds linear {th_lin:.1e} "
      f"(k<=1: {th_lin1:.1e}), physical " + ", ".join(f"{k_[0]}/{k_[1]} {v_:.1e}" for k_, v_ in th_phys.items()), b5_ok,
      "the linear sigma_8 at small lambda_eff is formally astronomical (the k^2 force runs away at high k); physically the web then "
      "sits in MOND equilibrium, which the physical-amplitude yardstick captures (the ungated core's L341 numbers)")

# ================================================================================================ B6 strong coupling
banner("B6  STRONG COUPLING AROUND ZERO FIELD (tree level) and the classical validity of the linearisation")
# canonical slow mode: L = (1/2) varphi'^2 - (1/2) c_s^2 |grad varphi|^2 - kappa3 |grad varphi|^3, varphi = sqrt(2 lambda_eff) M_P q,
# c_s^2 = C_phi/lambda_eff, kappa3 = (2/3)/(alpha M_P (2 lambda_eff)^(3/2)); in the frame x = c_s x' the cubic coefficient is
# kappa3 c_s^(-9/2), so Lambda_sc = c_s^(9/4) [alpha M_P (2 lambda_eff)^(3/2) (3/2)]^(1/2) and the length ell_sc = c_s hbar c/Lambda_sc
HBARC = 1.973269804e-7; MP_eV = 2.435e27
rows6 = []
for foot, a0 in A0.items():
    alpha_eV = a0 / cc ** 2 * HBARC
    for lab, ybg in (("web y ~ 1e-3", 1e-3), ("galaxy outskirts y ~ 0.1", 0.1), ("Solar neighbourhood x_e", None)):
        xbg = (math.sqrt(yN_of(2.32e-10, a0) ** 2 + yN_of(2.32e-10, a0)) - yN_of(2.32e-10, a0)) if ybg is None else math.sqrt(ybg ** 2 + ybg) - ybg
        Cphi = xbg / (1 - 2 * xbg)
        for le in (LAM_KH0, 1e8):
            cs = math.sqrt(Cphi / le)
            Lsc = cs ** 2.25 * math.sqrt(alpha_eV * MP_eV * (2 * le) ** 1.5 * 1.5)
            rows6.append((foot, lab, le, cs, Lsc, cs * HBARC / Lsc))
for r_ in rows6:
    P(f"    {r_[0]:9s} {r_[1]:28s} lambda_eff {r_[2]:9.3g}: c_s = {r_[3]:.2e} c, Lambda_sc = {r_[4]:.2e} eV, ell_sc = {r_[5]:.2e} m")
# classical validity of the zero-field linearisation: the J force over the inertia, R_NL ~ (3/5) k^3 delta/(alpha lambda_eff^2 H^2)
kk = 0.2 * h_ / Mpc_
RNL = {le: 0.6 * kk ** 3 * 0.3 / ((A0["canonical"] / cc ** 2) * le ** 2 * (H0 / cc) ** 2) for le in (LAM_KH0, 1e4, 1e8)}
P("    classical: J's force / inertia on the web (k = 0.2 h/Mpc, delta = 0.3, z = 0): " + ", ".join(f"lambda_eff {le:.3g}: {v_:.1e}" for le, v_ in RNL.items())
  + "  (>> 1: the web leaves the linear regime and sits in MOND equilibrium)")
OUT["numbers"]["B6"] = dict(rows=rows6, R_NL=RNL)
check("B6 (reported) STRONG COUPLING: phi's gradient energy vanishes at exactly zero field, so the tree-level strong-coupling scale "
      "Lambda_sc = c_s^(9/4) [ (3/2) alpha M_P (2 lambda_eff)^(3/2) ]^(1/2) -> 0 there (c_s -> 0): the exact FRW background is formally "
      "infinitely strongly coupled.  In any real background (web y ~ 1e-3, galaxies, the Solar neighbourhood) the cutoff length is "
      "<= ~1 mm, far below every scale the classical theory is used on; the classical linearisation itself holds only while J's force "
      "is below the inertia (R_NL << 1), which needs lambda_eff >~ 1e5 on the web",
      "; ".join(f"{r_[0][:3]}/{r_[1][:12]}/{r_[2]:.0e}: ell {r_[5]:.1e} m" for r_ in rows6[::2]) + "; R_NL " + ", ".join(f"{v_:.0e}" for v_ in RNL.values()),
      max(r_[5] for r_ in rows6) < 1e-2, load_bearing=False,
      reading="safe as a classical EFT away from exact zero field; the quantum strong-coupling question at exact zero field is OPEN")

# ================================================================================================ C1 health (Krein)
banner("C1  HEALTH: the two scalar modes' kinetic (T) and restoring (V) matrices, Minkowski and static MOND backgrounds (both channels)")
tC = time.time()
herm = all(sp.expand(Mblk[i, j] - sp.conjugate(Mblk[j, i]).subs({sp.conjugate(v_): v_ for v_ in (alm, c2m, Cph, lmm, sgm, kq_, wq_)})) == 0
           for i in range(4) for j in range(4))
# eliminate the lapse and the shift (their equations carry no omega^2: constraints) and read the reduced 2x2 system
# (psi, phi): M2(omega) = omega^2 T - V  (L = (1/2) x' T x' - (1/2) x V x): health <=> T > 0 (no ghost) and V >= 0 (no tachyon)
nB = sp.solve([ELk[0], ELk[2]], [An, AB], dict=True)[0]
rows2 = [sp.expand(sp.simplify(ELk[1].subs(nB))), sp.expand(sp.simplify(ELk[4].subs(nB)))]
M2 = sp.Matrix([[sp.expand(sp.diff(r_, v_)) for v_ in (Ap, AF)] for r_ in rows2])
T2 = M2.applyfunc(lambda e_: sp.simplify(sp.expand(e_).coeff(wq_, 2)))
V2 = M2.applyfunc(lambda e_: sp.simplify(-sp.expand(e_).subs(wq_, 0)))
lin_ok = all(sp.simplify(sp.expand(M2[i, j]) - (T2[i, j] * wq_ ** 2 - V2[i, j])) == 0 for i in range(2) for j in range(2))
detT, detV = sp.factor(T2.det()), sp.factor(V2.det())
P(f"    reduced (psi, phi) system after the lapse and shift constraints: T = {T2.tolist()}")
P(f"    V = {V2.tolist()};  det T = {detT};  det V = {detV};  exact quadratic in omega: {lin_ok}")
T11, T22, T12 = sp.simplify(T2[0, 0]), sp.simplify(T2[1, 1]), sp.simplify(T2[0, 1])
V11, dV = sp.simplify(V2[0, 0]), sp.factor(V2.det())
noghost = T12 == 0 and sp.simplify(T11 - 4 * (2 + 3 * c2m) / c2m) == 0 and sp.simplify(T22 - 4 * lmm) == 0
nograd = sp.simplify(V11 - 4 * kq_ ** 2 * (2 - alm) / alm) == 0 and sp.simplify(dV - 16 * Cph * kq_ ** 4 * (2 - alm) / alm) == 0
P(f"    Sylvester: T = diag({T11}, {T22}) > 0 iff c_2 > 0, lambda > 0 (no ghost);  V_11 = {V11} > 0 iff 0 < alpha_c < 2;  det V = {dV} >= 0 "
  f"iff C_phi >= 0 (= 0: the marginal zero-field mode)")
xofy = lambda y_: math.sqrt(y_ * y_ + y_) - y_
CTf = lambda x_: x_ / (1 - 2 * x_)
CLf = lambda x_: 2 * x_ * (1 - x_) / (1 - 2 * x_) ** 2
Vd = sp.lambdify((kq_, Cph, alm, sgm), (V11, dV), "numpy")
ysH = np.logspace(-3, 4, 57)
bad, ncell = [], 0
for yv in ysH:
    for lab, Cv in (("T", CTf(xofy(yv))), ("L", CLf(xofy(yv)))):
        for acv in (1e-13, 3.2e-9):
            for sv in (1.0, 0.1):
                ncell += 1
                v1, dv = Vd(1.0, Cv, acv, sv)
                if not (v1 > 0 and dv > 0):
                    bad.append((round(float(yv), 4), lab, acv, sv))
nurar = lambda y_: 1.0 / (-math.expm1(-math.sqrt(y_)))
CLQ_rar = lambda y_, e_=1e-5: ((y_ * (1 + e_)) * nurar(y_ * (1 + e_)) - (y_ * (1 - e_)) * nurar(y_ * (1 - e_))) / (2 * y_ * e_) - 1.0
ctrl_C = 1.0 / CLQ_rar(10.0)
ctrl = "TACHYON" if Vd(1.0, ctrl_C, 1e-9, 1.0)[1] < 0 else "ok"
P(f"    P2 on static MOND backgrounds (y = 1e-3..1e4, both channels, both alpha_c ends, sigma = 1 and 0.1): cells with V not positive definite {len(bad)} of {ncell};"
  f"  control nu_RAR partner (C_L^phi = 1/C_L^Q = {ctrl_C:+.2f} at y = 10): det V < 0 -> {ctrl}")
check("C1 NO GHOST, NO GRADIENT INSTABILITY, exactly: eliminating the lapse and shift (constraints) leaves two scalar modes with "
      "L = (1/2) x'.T.x' - (1/2) x.V.x, T = diag(4(2 + 3c_2)/c_2, 4 lambda) (the khronon's inertia and phi's) and det V = "
      "16 C_phi k^4 (2 - alpha_c)/alpha_c: healthy iff c_2, lambda > 0, 0 < alpha_c < 2 and C_phi > 0 in each channel, marginal at "
      "C_phi = 0 (zero field); P2 has C_T, C_L > 0 at every y (both channels, both alpha_c ends); the non-monotone control "
      "(C_L < 0) is a tachyon.  The same holds on FRW sub-horizon (B3-B4)",
      f"Hermitian {herm}; reduction exact {lin_ok}; T {noghost}; V {nograd}; P2 cells unhealthy {len(bad)} of {ncell}; control {ctrl}",
      herm and lin_ok and noghost and nograd and len(bad) == 0 and ctrl == "TACHYON",
      "health needs a monotone scalar flux (C_T, C_L > 0): L340 H2/H3's condition in AQUAL form; P2 meets it at every x in (0, 1/2)")

# ================================================================================================ C2 FC-KH
banner("C2  THE FC-KH (yq)' THEOREM, RE-DERIVED FOR THE NEW TERM")
yy = sp.symbols("y", positive=True)
muF = sp.Function("mu")
W_ = sp.integrate(yy * sp.Symbol("m"), yy)                        # placeholder not used: identity checked with a generic mu below
Wfun = sp.Function("W")
ident = sp.simplify((1 - sp.diff(yy * muF(yy), yy)) - sp.diff(yy * (1 - muF(yy)), yy)) == 0   # W' = y mu  =>  1 - W'' = (y(1 - mu))'
mu_exp = 1 - sp.exp(-yy)
kh_exp = sp.simplify(sp.diff(yy * (1 - mu_exp), yy))                                         # (1 - y) e^-y: negative for y > 1 (FC-KH's kill)
z_ = sp.symbols("z", positive=True)
mu_P2 = (-1 + sp.sqrt(1 + 4 * z_ ** 2)) / (2 * z_)                                           # P2 in single-field form: g_N = mu(g/a0) g
p2_single = sp.simplify(mu_P2 * z_ * z_ + mu_P2 * z_ - z_ ** 2) == 0 or sp.simplify(z_ ** 2 - ((mu_P2 * z_) ** 2 + mu_P2 * z_)) == 0
kh_P2 = sp.simplify(sp.diff(z_ * (1 - mu_P2), z_))
kh_P2_pos = sp.simplify(sp.expand((sp.sqrt(4 * z_ ** 2 + 1)) ** 2 - (2 * z_) ** 2)) == 1 and sp.simplify(kh_P2 - (1 - 2 * z_ / sp.sqrt(4 * z_ ** 2 + 1))) == 0
twoE = sp.factor(sp.simplify(2 - EAQ))
P(f"    identity (W' = y mu): 1 - W'' = (y(1 - mu))': {ident}")
P(f"    FC-KH's exponential mu on the lapse: (y(1 - mu))' = {kh_exp}  -> negative for y > 1 (the committed kill, reproduced)")
P(f"    P2 on the lapse (single-field mu_P2(z) = (sqrt(1 + 4z^2) - 1)/(2z)): (z(1 - mu))' = {kh_P2} > 0 for all z: {kh_P2_pos} "
  f"(P2's slow a0/2 tail is FC-KH's own escape clause)")
P(f"    the repaired action: the lapse's function is alpha_c a^2 (f'' = 2 alpha_c > 0, no MOND on the lapse); the khronon sees 2 - E = {twoE}, "
  f"positive iff C_phi > 0 -- the analogue of FC-KH's condition is the monotone scalar flux (A2, C1)")
check("C2 THE FC-KH (yq)' OBSTRUCTION DOES NOT ARISE: re-derived, FC-KH's khronon coefficient is 1 - W'' = (y(1 - mu))' for a MOND "
      "function on the LAPSE, negative for y > 1 with the exponential mu (reproduced); in the repaired action the lapse carries only "
      "alpha_c a^2, the MOND function sits on phi, and the khronon's 2 - E = 2(2 - alpha_c) C_phi/((2 - alpha_c) sigma^2 + 2 C_phi) is "
      "positive iff C_phi > 0 in each channel -- which P2 satisfies everywhere (and P2 would pass FC-KH's own test anyway: its a0/2 "
      "tail is the theorem's escape clause, removed from the Solar System by the filter, A4)",
      f"identity {ident}; exp {kh_exp}; P2 {kh_P2} > 0: {kh_P2_pos}; 2 - E = {twoE}",
      ident and kh_P2_pos and sp.simplify(twoE - 2 * (2 - alm) * Cph / ((2 - alm) * sgm ** 2 + 2 * Cph)) == 0)

# ================================================================================================ C3 tracking
banner("C3  TRACKING (the L330 gate) AND THE TRACKING SPEED")
wT_, kT_ = sp.symbols("omega_T k_T", positive=True)
MC = Mblk.subs({wq_: wT_, kq_: kT_})
Rs_ = sp.Symbol("R")
SC = sp.Matrix([0, Rs_, sp.I * wT_ * Rs_, 0])                   # rows (psi, n, B, phi): conserved source, lapse R, momentum -D R
detC = sp.factor(sp.expand(MC.det(method='berkowitz')))
det0 = sp.factor(detC.subs(wT_, 0))


def cramer(Mx, Sx, i):
    Mi = Mx.copy(); Mi[:, i] = Sx
    return sp.cancel(sp.expand(Mi.det(method='berkowitz')) / sp.expand(Mx.det(method='berkowitz')))


psiC = cramer(MC, SC, 0)
psiN = -Rs_ / (4 * kT_ ** 2)
num0, den0 = sp.fraction(sp.cancel(psiC / psiN))
lim0 = sp.factor(sp.cancel(num0.subs(wT_, 0) / den0.subs(wT_, 0)))
static_expect = sp.simplify(1 / (1 - alm / 2) + sgm ** 2 / Cph)              # Phi/Phi_N[G] = G_N/G + sigma^2/C_phi (A1's linearised statics)
det0_c2 = sp.factor(detC.subs(c2m, 0).subs(wT_, 0))
root_l0 = sp.factor(root_l0[0])
v_ = V_TRACK / cc
c2_floor = float(sp.nsolve(root_l0.subs({alm: 1e-9, sgm: 1, Cph: 0.01}) - v_ ** 2, c2m, 7e-3))
reach = LAM_TRACK
P(f"    det M(omega = 0) = {det0}  (nonzero iff c_2 C_phi != 0);  control c_2 = 0: {det0_c2}")
P(f"    omega -> 0 response psi/psi_N = {lim0};  static linear law G_N/G + sigma^2/C_phi = {static_expect}")
P(f"    slow mode speed c_s^2 = C_phi/lambda_eff (B4); lambda = 0: c_s^2 = {root_l0}  ->  3 x 600 km/s at C_phi = 0.01 (FP2's C <= 100) needs "
  f"c_2 >= {c2_floor:.4e} (FP2 C4: {C2_FLOOR_FP2:.4e}); with lambda > 0 it needs lambda_eff <= 0.01 (c/1800 km/s)^2 = {LAM_TRACK:.1f}")
OUT["numbers"]["C3"] = dict(det0=str(det0), c2_floor=c2_floor, lambda_track=LAM_TRACK)
check("C3 TRACKING: with the khronon's c_2 channel the omega -> 0 response of the repaired block is the static MOND law "
      "(psi/psi_N -> G_N/G + sigma^2/C_phi, det M(0) proportional to c_2 C_phi, zero without c_2: L330's frozen phantom); the "
      "tracking speed is c_s^2 = C_phi/lambda_eff, and at lambda = 0 the exact root reproduces FP2's floor c_2 >= 7.29e-3 "
      "(the AQUAL block is the C-H/K block under C^Q = 1/C^phi)",
      f"limit {lim0}; det0 {det0}; control {det0_c2}; c_2 floor {c2_floor:.4e} vs {C2_FLOOR_FP2:.4e}; lambda_eff <= {LAM_TRACK:.1f}",
      sp.simplify(lim0 - static_expect) == 0 and det0 != 0 and det0_c2 == 0 and abs(c2_floor / C2_FLOOR_FP2 - 1) < 2e-3)
P(f"    ({time.time() - tC:.0f} s)")

# ================================================================================================ D c_T and PPN
banner("D1  c_T = 1: the tensor sector of the repaired action")
hp_, hx_ = [sp.Function(s_)(tt_, zz_) for s_ in ('h_p', 'h_x')]
gamT = sp.Matrix([[1 + eb * hp_, eb * hx_, 0], [eb * hx_, 1 - eb * hp_, 0], [0, 0, 1]])
ginT = gamT.inv()
GmT = [[[sum(ginT[a_, d_] * (sp.diff(gamT[d_, b_], X3m[c_]) + sp.diff(gamT[d_, c_], X3m[b_]) - sp.diff(gamT[b_, c_], X3m[d_])) for d_ in range(3)) / 2
         for c_ in range(3)] for b_ in range(3)] for a_ in range(3)]
KijT = sp.Matrix(3, 3, lambda i, j: sp.diff(gamT[i, j], tt_) / 2)
KupT = ginT * KijT * ginT
KKT = sum(KijT[i, j] * KupT[i, j] for i in range(3) for j in range(3))
trKT = sum(ginT[i, j] * KijT[i, j] for i in range(3) for j in range(3))


def Ric3T(b_, c_):
    return sum(sp.diff(GmT[a_][b_][c_], X3m[a_]) - sp.diff(GmT[a_][b_][a_], X3m[c_]) +
               sum(GmT[a_][a_][d_] * GmT[d_][b_][c_] - GmT[a_][c_][d_] * GmT[d_][b_][a_] for d_ in range(3)) for a_ in range(3))


R3T = sum(ginT[b_, c_] * Ric3T(b_, c_) for b_ in range(3) for c_ in range(3))
# the new sector on a TT perturbation of flat space with phi = 0, N = 1: a_i = 0, D phi = 0, n.d phi = 0 -> every new term vanishes
new_TT = (Bsym * 0 + Csym * 0 - 2 * Cph * 0 + 2 * lmm * 0)
LT = sp.expand((sp.diff(sp.sqrt(gamT.det()) * (KKT - trKT ** 2 + R3T - c2m * trKT ** 2 + new_TT), eb, 2) / 2).subs(eb, 0))
ELT = euler_equations(LT, [hp_, hx_], [tt_, zz_])
AT_ = sp.Symbol('A_T')
ELTk = sp.factor(sp.simplify((ELT[0].lhs - ELT[0].rhs).subs({hp_: AT_ * sp.exp(sp.I * (kq_ * zz_ - wq_ * tt_)), hx_: 0}).doit()
                             / sp.exp(sp.I * (kq_ * zz_ - wq_ * tt_))))
wsolT = sp.solve(ELTk.subs(AT_, 1), wq_)
kinT = sp.expand(LT).coeff(sp.Derivative(hp_, tt_) ** 2)
# on a static MOND background the J-term gives h_TT an anisotropic 'mass' ~ J'(grad phi_0)^2 ~ x^2 mu_s alpha^2: |c_T - 1| ~ m^2/(2 k^2)
kGW = 2 * math.pi * 100.0 / cc
dcT = max(((xofy(yv) ** 2 * CTf(xofy(yv))) * (A0[f] / cc ** 2) ** 2) / (2 * kGW ** 2) for f in A0 for yv in (0.01, 1.0, 100.0))
P(f"    TT Euler-Lagrange: {ELTk};  omega roots {wsolT};  kinetic coefficient {kinT};  new sector on TT at zero field: identically 0")
P(f"    on a MOND background (x^2 mu_s alpha^2 mass-like term, 100 Hz): |c_T - 1| <~ {dcT:.1e} (GW170817: 1e-15)")
check("D1 c_T = 1: the chassis, J and the inertia are scalar functions of (a_m, D phi, n.d phi), all zero on a transverse-traceless "
      "perturbation of flat space, so the tensor sector is GR's (omega^2 = k^2, kinetic 1/2) exactly; on a MOND background the "
      "J-term's anisotropic 'mass' leaves |c_T - 1| ~ 1e-40 at LIGO frequencies",
      f"roots {wsolT}; kinetic {kinT}; background estimate {dcT:.1e}", set(wsolT) == {kq_, -kq_} and sp.simplify(kinT - sp.Rational(1, 2)) == 0 and dcT < 1e-20)

banner("D2  THE FULL PREFERRED-FRAME PPN (FP2's moving-source pipeline, read-only reuse, on the repaired block)")
tD = time.time()
kB, wB, vB, GA, muB = sp.symbols('k omega v G_ae mu', real=True)
ELB = [e_.subs({kq_: kB, wq_: wB}) for e_ in ELk]
Pf = 1 / (16 * sp.pi * GA)
gmB = 1 / sp.sqrt(1 - vB ** 2)
kpB = sp.symbols('kp', positive=True)
BOOST = {kB: kpB * sp.sqrt(1 + (gmB ** 2 - 1) * muB ** 2), wB: gmB * kpB * muB * vB}
MB = sp.symbols('M', positive=True)


def ms_solve(rho, sub):
    J_long, Pi = rho * wB, rho * vB ** 2
    eqs = [sp.Eq(Pf * ELB[0].subs(sub), rho), sp.Eq(Pf * ELB[1].subs(sub), Pi), sp.Eq(Pf * ELB[2].subs(sub), sp.I * J_long), sp.Eq(ELB[4].subs(sub), 0)]
    s_ = sp.solve(eqs, [An, Ap, AB, AF], dict=True)
    return s_[0] if s_ else None


S_PER_J = sp.solve(sp.Eq(Pf * ELB[3] + 1, 0), AS)[0]


def h00_rest(sol, rho):
    PhiB = sol[An] - sp.I * wB * sol[AB]
    h = gmB ** 2 * (-2 * PhiB - 2 * vB ** 2 * sol[Ap] + 2 * S_PER_J * rho * (vB ** 2 - wB ** 2 / kB ** 2))
    return gmB * h.subs(BOOST)


def v2_parts(expr):
    s_ = sp.expand(sp.series(expr, vB, 0, 3).removeO())
    return sp.simplify(s_.coeff(vB, 0)), sp.factor(sp.simplify(s_.coeff(vB, 2).subs(muB, 0))), sp.factor(sp.simplify(s_.coeff(vB, 2).coeff(muB, 2)))


solF = ms_solve(gmB * MB, {})
hF = h00_rest(solF, gmB * MB)
o0F, AisoF, CaniF = v2_parts(sp.simplify(hF / sp.simplify(hF.subs(vB, 0))))
alpha1 = sp.factor(-2 * AisoF); alpha2 = sp.factor(CaniF)
sol0 = ms_solve(MB, {vB: 0})
s0 = {kk_: sp.simplify(vv_.subs({vB: 0, wB: 0})) for kk_, vv_ in sol0.items()}
gamma_ppn = sp.simplify(s0[Ap] / s0[An])
U_obs = sp.simplify(-s0[An]); h0jT = sp.simplify(-2 * s0[An] - 2 * s0[Ap] + S_PER_J * MB)
alpha3 = sp.simplify(alpha1 - sp.factor(sp.simplify(-2 * h0jT / U_obs)))
yagi2 = alm * (alm - c2m + 2 * alm * c2m) / (c2m * (2 - alm))
filt1 = sp.simplify(alpha1.subs(sgm, 0) + 4 * alm); filt2 = sp.simplify(alpha2.subs(sgm, 0) - yagi2)
a1_0 = sp.factor(sp.limit(alpha1, alm, 0)); a2_0 = sp.factor(sp.limit(alpha2, alm, 0))
ser1 = sp.simplify(sp.series(alpha1, sgm, 0, 3).removeO().coeff(sgm, 2)); ser2 = sp.simplify(sp.series(alpha2, sgm, 0, 3).removeO().coeff(sgm, 2))
f1s, f2s = sp.lambdify((Cph, c2m, alm, lmm), ser1, "numpy"), sp.lambdify((Cph, c2m, alm, lmm), ser2, "numpy")
F1 = lambda r, xi: math.erf(r / (2 * xi)) - (r / (xi * math.sqrt(math.pi))) * math.exp(-r * r / (4 * xi * xi)) if r / xi > 1e-3 else (r / xi) ** 3 / (6 * math.sqrt(math.pi))
leak1, leak2 = 0.0, 0.0
for f in A0:
    xe = xofy(yN_of(2.32e-10, A0[f])); xi_m = (FLA[f]["floor"] if 'FLA' in globals() else 0.025) * PC_M
    for Cv in (CTf(xe), CLf(xe)):
        for c2v in (7.29e-3, 1.0):
            for lv in (1e-3, 1.0, 1e4, 1e8):
                leak1 = max(leak1, abs(float(f1s(Cv, c2v, 1e-9, lv))) * F1(AU_M, xi_m))                      # alpha_1: LLR, 1 AU
                leak2 = max(leak2, max(abs(float(f2s(Cv, c2v, 1e-9, lv))) * F1(r_, xi_m) for r_ in (6.957e8, 1.0e4)))   # alpha_2: solar spin, pulsars
leak = max(leak1, leak2)
ac_bound = min(1e-5 / 4, min(brentq(lambda a_: abs(float(yagi2.subs({alm: a_, c2m: c2v}))) - 1.6e-9, 1e-15, 1e-6) for c2v in (7.29e-3, 0.067, 1.0)))
P(f"    gamma = {gamma_ppn};  alpha_3 = {alpha3};  alpha_1 = {alpha1}")
P(f"    alpha_2 = {alpha2}")
P(f"    filtered (sigma -> 0: the Solar System): alpha_1 + 4 alpha_c = {filt1}, alpha_2 - Yagi+14 = {filt2};  MOND regime (alpha_c -> 0): alpha_1 = {a1_0}, alpha_2 = {a2_0}")
P(f"    leakage where the bounds live (xi at the AQUAL floor, C_phi of the Galactic field at the Sun, lambda up to 1e8): alpha_1 at 1 AU {leak1:.1e}, alpha_2 at R_sun / 10 km {leak2:.1e};  alpha_c <= {ac_bound:.2e}  ({time.time() - tD:.0f} s)")
OUT["numbers"]["D2"] = dict(alpha1=str(alpha1), alpha2=str(alpha2), alpha1_MOND=str(a1_0), alpha2_MOND=str(a2_0), leak=leak, alpha_c_bound=ac_bound)
check("D2 THE FULL PPN OF THE REPAIRED ACTION: gamma = 1 (no slip), alpha_3 = 0 (the g_0j and g_00 readings of alpha_1 agree), "
      "closed-form alpha_1 and alpha_2; with the filter (sigma -> 0) they are exactly the khronometric -4 alpha_c and Yagi+14's alpha_2, "
      "and the MOND sector's leakage where the bounds live (alpha_1 at 1 AU, alpha_2 at R_sun and 10 km) is negligible for any lambda <= 1e8, so the bounds CONSTRAIN alpha_c <= 3.2e-9 as "
      "before; in the MOND regime alpha_1 = -8 sigma^2/(C_phi + sigma^2) (FP2's -8C/(1+C) under C = 1/C_phi) and alpha_2 carries "
      "+lambda sigma^2/(C_phi (C_phi + sigma^2)): the inertia's moving-source lag",
      f"gamma {gamma_ppn}; alpha_3 {alpha3}; filtered {filt1}, {filt2}; leak alpha_1 {leak1:.1e}, alpha_2 {leak2:.1e}; alpha_c <= {ac_bound:.2e}",
      gamma_ppn == 1 and alpha3 == 0 and filt1 == 0 and filt2 == 0 and leak < 1e-11 and 3.0e-9 < ac_bound < 3.3e-9
      and sp.simplify(a1_0 + 8 * sgm ** 2 / (Cph + sgm ** 2)) == 0,
      "beta = 1 is inherited (KM3): at 1 AU the filtered chi is smooth, its uniform gradient drops out of a.Dchi, and the sector "
      "reduces to GR + BPS")

# ================================================================================================ E the mode count
banner("E1  THE MODE COUNT (deg_omega of the determinants), and E2 whether the extra scalar is physically harmful")
deg_T = sp.Poly(sp.expand(ELTk.subs(AT_, 1)), wq_).degree()
deg_V = sp.Poly(sp.expand(ELk[3]), wq_).degree() if ELk[3].has(wq_) else 0
deg_S = sp.Poly(sp.numer(sp.together(detM)), wq_).degree()
deg_S0 = sp.Poly(sp.numer(sp.together(detM.subs(lmm, 0))), wq_).degree()
N_modes = 2 * (deg_T // 2) + deg_V // 2 + deg_S // 2
N_modes0 = 2 * (deg_T // 2) + deg_V // 2 + deg_S0 // 2
phi_l0 = sp.solve(ELk[4].subs({lmm: 0, Cph: 0}), AF)
P(f"    tensor: deg_omega {deg_T} per polarisation (2 modes); vector (transverse shift): deg {deg_V} (a constraint); scalar: deg {deg_S} "
  f"(lambda > 0) / {deg_S0} (lambda = 0)  ->  N = {N_modes} / {N_modes0}")
P(f"    lambda = 0 at exactly zero field: phi = {phi_l0} (the auxiliary phi inherits 1/sigma(k) = e^(+xi^2 k^2/2); lambda > 0 removes it)")
check("E1 THE MODE COUNT: 2 tensor + 1 khronon + 1 MOND scalar = 4 propagating modes for lambda > 0 (3 at lambda = 0, where phi is "
      "auxiliary and the khronon carries the MOND mode, but its exact-zero-field value then needs the inverse filter 1/sigma(k)); "
      "the heat filter adds none (FP5's G-2b: its pair is second class, the Schur complement only multiplies the chassis by sigma)",
      f"deg tensor {deg_T}, vector {deg_V}, scalar {deg_S}/{deg_S0}; N = {N_modes}/{N_modes0}; phi(lambda = 0, zero field) = {phi_l0}",
      N_modes == 4 and N_modes0 == 3 and deg_V == 0)
# E2: is the fourth mode harmful?  (reported, with numbers)
E_uhecr = 1e20 * 1.602176634e-19                                     # J
m_eff = E_uhecr / cc ** 2
xi_fl = min(v_["floor"] for v_ in FLA.values()) * PC_M if 'FLA' in globals() else 0.025 * PC_M
dEdx = Gn * m_eff ** 2 / xi_fl ** 2                                  # coherent emission is cut at k ~ 1/xi (the coupling is sigma(k))
dE_100Mpc = dEdx * 100 * Mpc_
P(f"    Cherenkov: the slow mode is subluminal in MOND regions (c_s^2 = C_phi/lambda_eff), but matter couples to it only through chi = S phi: "
  f"the coupling is e^(-xi^2 k^2/2); coherent emission (k <~ 1/xi) by a 1e20 eV cosmic ray loses ~ G (E/c^2)^2/xi^2 x 100 Mpc = "
  f"{dE_100Mpc:.1e} J of its {E_uhecr:.0f} J")
P(f"    GW170817: c_T = 1 (D1) and on flat space the TT sector does not mix with the scalars at quadratic order; fifth force: it IS the "
  f"MOND force, screened in the Solar System by the filter (A4); PPN: gamma = 1, khronometric alphas (D2)")
check("E2 (reported) THE FOURTH MODE IS NOT PHYSICALLY HARMFUL in the channels named: no fifth force in the Solar System (A4), gamma = 1 "
      "and khronometric alphas (D2), c_T = 1 and no TT mixing (D1), and Cherenkov losses of cosmic rays negligible because the filter "
      "decouples it above k ~ 1/xi; the spec's 'at most one extra scalar' (FRIED_CHICKEN_VERDICT Case 4) is therefore a preference "
      "here, not a physical exclusion -- but this mode's INERTIA is exactly what the sigma_8-vs-tracking pincer (T) turns on",
      f"UHECR Cherenkov loss over 100 Mpc {dE_100Mpc:.1e} J vs {E_uhecr:.0f} J; c_T - 1 < {dcT:.0e}; gamma = 1",
      dE_100Mpc < 1e-20 * E_uhecr, load_bearing=False)

# ================================================================================================ F constants
banner("F   THE CONSTANTS OF THE REPAIRED ACTION, AND THEIR STATUS")
CONST = [
    ("G", "measured", "laboratory G_N = G/(1 - alpha_c/2) (the Newtonian limit, A1); the MOND scalar's source uses G (O(1e-9) apart)"),
    ("Lambda", "measured", "fixed constant; the background is GR + Lambda (B1)"),
    ("a0 = alpha c^2 (kappa)", "declared (P1), kappa = 1/2 FITTED", f"{A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2; enters only through J (statics), absent from linear cosmology (B2)"),
    ("chassis (2, 2 - alpha_c)", "DERIVED", "A1: the unique quadratic chassis with no Newtonian term in phi's equation and a GR + BPS Newtonian limit"),
    ("J = J_P2", "POSTULATED", "FP0's L1a (P2) in two-field AQUAL form (A2); any monotone J is admissible (C1)"),
    ("xi", "bounded (CONSTRAINT)", "Solar-System floor " + (" / ".join(f"{FLA[f]['floor']:.4f}" for f in A0) if 'FLA' in globals() else "?") + " pc (A4; QUMOND's 0.0294/0.0316); ceiling ~100 pc (disc scales, inherited)"),
    ("alpha_c", "bounded (CONSTRAINT)", "0 < alpha_c <= 3.2e-9 (D2, khronometric); the L340 H4 lower edge (O(Phi/c^2) lobes) is not re-derived here (OPEN)"),
    ("c_2", "bounded, in tension", f"tracking at lambda = 0 needs c_2 >= {C2_FLOOR_FP2:.2e} (C3); sigma_8 at lambda = 0 would need (2 + 3c_2)/c_2 >~ 1e7"),
    ("lambda (NEW)", "EMPTY WINDOW (FAILS)", "sigma_8 needs lambda_eff >~ 1e7-4e8 (B5); tracking needs lambda_eff <= 277 (<= 2.8e4 even at C_phi >= 1) (C3, T)"),
    ("beta", "fixed = 0", "GW170817 (D1)"),
    ("phibar-dot", "declared = 0", "a free constant of motion on FRW (B1); its kination decays as a^-6"),
    ("dark mass", "declared (cold, Omega_c)", "not a state of these fields (as in FP3/FP5); sigma_8 is computed with it declared"),
]
for c_, st_, why in CONST:
    P(f"    {c_:26s} {st_:30s} {why}")
check("F (reported) the repaired action's constants: 2 measured (G, Lambda), 1 fitted coupling (kappa), 1 derived structure (the chassis), "
      "1 postulated function (J_P2), 3 bounded knobs (xi, alpha_c, c_2), 1 NEW constant (lambda) whose window is empty, 1 fixed (beta), "
      "2 declared data (phibar-dot, the dark mass)", f"{len(CONST)} rows", True, load_bearing=False)
OUT["numbers"]["F"] = [dict(constant=c_, status=st_, note=w_) for c_, st_, w_ in CONST]

# ================================================================================================ T the pincer
banner("T   THE PINCER: sigma_8 needs a heavy MOND scalar, tracking a light one")
lam_sig = min([th_lin, th_lin1] + list(th_phys.values()))
LAM_TRACK_GEN = 1.0 * (cc / V_TRACK) ** 2                            # tracking only where C_phi >= 1 (inner galaxies)
LAM_ROT = 0.1 * (cc / 200e3) ** 2                                    # internal rotation 200 km/s, margin 1, C_phi = 0.1 (y ~ 0.01)
cs_at_sig = {Cv: cc * math.sqrt(Cv / lam_sig) / 1e3 for Cv in (0.01, 0.1, 1.0)}
s8_at_track = {f: (phys_tab[(f, "rms")][LAM_KH0], phys_tab[(f, "permode")][LAM_KH0]) for f in A0}
P(f"    sigma_8 <= 1.02: lambda_eff >= {lam_sig:.2e} (the most lenient yardstick: linear, k <= 1 h/Mpc; others {th_lin:.1e}, "
  + ", ".join(f"{v_:.1e}" for v_ in th_phys.values()) + ")")
P(f"    tracking 3 x 600 km/s: lambda_eff <= {LAM_TRACK:.0f} (C_phi >= 0.01, FP2's convention) / {LAM_TRACK_GEN:.2e} (only where C_phi >= 1); "
  f"internal rotation 200 km/s at y ~ 0.01: <= {LAM_ROT:.2e}")
P(f"    at lambda_eff = {lam_sig:.1e} the MOND scalar moves at " + ", ".join(f"{v_:.0f} km/s (C_phi = {k_:g})" for k_, v_ in cs_at_sig.items())
  + f";  at lambda_eff = {LAM_KH0:.0f} sigma_8/LCDM = " + ", ".join(f"{f} {v_[0]:.1f} (rms) / {v_[1]:.1f} (per-mode)" for f, v_ in s8_at_track.items()))
gap = lam_sig / max(LAM_TRACK_GEN, LAM_ROT)
OUT["numbers"]["T"] = dict(lambda_sigma8=lam_sig, lambda_track=LAM_TRACK, lambda_track_generous=LAM_TRACK_GEN, lambda_rotation=LAM_ROT,
                           gap_min=gap, cs_at_sigma8_kms=cs_at_sig, sigma8_at_track=s8_at_track)
check("T THE sigma_8-vs-TRACKING PINCER ON THE SCALAR'S INERTIA (verified both ways): sigma_8 within 2% needs lambda_eff >~ 1e7 on the most "
      "lenient yardstick, while a MOND field that follows a galaxy moving at 600 km/s (x3) needs lambda_eff <= 277 where C_phi >= 0.01 "
      "(<= 2.8e4 even if only C_phi >= 1 regions must track; <= 2e5 just to follow 200 km/s rotation): the window is EMPTY by >= "
      "1.5 decades on the most generous reading.  At the tracking edge sigma_8 is L341's ~ 20x; at the sigma_8 edge the field moves at ~10-100 km/s",
      f"lambda_sigma8 >= {lam_sig:.2e} vs tracking <= {LAM_TRACK:.0f} / {LAM_TRACK_GEN:.1e} / rotation {LAM_ROT:.1e}: gap x{gap:.0f}; "
      f"c_s at the sigma_8 edge " + ", ".join(f"{v_:.0f}" for v_ in cs_at_sig.values()) + " km/s",
      gap > 10 and all(v_[0] > 10 for v_ in s8_at_track.values()) and max(cs_at_sig.values()) < 1800,
      "the a0-free inertia cannot separate the web from galaxies: FP3 C6's tracking-class pincer, now for the AQUAL scalar (the "
      "khronon-locked inertia at lambda = 0 is FP3's c_2 channel exactly)")
check("G (reported) the AQUAL-type repair with an a0-free inertia passes sigma_8 AND keeps galaxies' MOND (tracking) with NO gate",
      f"no: lambda_eff must be >= {lam_sig:.1e} for sigma_8 and <= {LAM_TRACK_GEN:.1e} for tracking", lam_sig <= LAM_TRACK_GEN, load_bearing=False)

# ================================================================================================ W ledger
banner("W   THE LEDGER: FP7, the AQUAL-type repair of the root action")
fl_txt = " / ".join(f"{FLA[f]['floor']:.4f}" for f in A0) if 'FLA' in globals() else "?"
LEDGER = [
    ("R7a", "the repaired root: the core with C-H's U-sector replaced by (2 - alpha_c) h(2a - Dchi)Dchi - 2 alpha^2 J_P2(|Dphi|^2/alpha^2) "
            "+ 2 lambda (n.dphi)^2, chi = S_h phi (khronon terms, leaf average, filter kept)", "POSTULATED",
     "the coordinator's repair of FP3's G1t; the inertia's form is the suggested a0-free (n.dphi)^2"),
    ("R7b", "the chassis is forced: 2a^2 - (2 - alpha_c)|Dchi - a|^2 (no Newtonian term in phi's equation, GR + BPS Newtonian limit); "
            "C-H's sign pins its field to Newton (QUMOND)", "DERIVED", "A1 (sympy EL of the static density)"),
    ("R7c", "the filter must sit on the chassis (chi = S phi): J on S phi needs S^{-1}; filtering both cancels", "DERIVED", "A1b (discrete adjoint + Fourier gains)"),
    ("R7d", "static law: psi = Phi, Phi = Phi_N[G_N] + S phi, div(mu_s grad phi) = 4 pi G S rho (two-field AQUAL); P2 exact in spherical "
            "symmetry; C_T, C_L > 0; C^Q = 1/C^phi", "DERIVED", "A1, A2"),
    ("R7e", f"thin exponential discs: AQUAL vs QUMOND <= {worst_AQ:.3f} dex (y = 0.01-100, R >= 0.3 R_d), <= {worst_prof:.3f} dex after "
            f"profiling Upsilon (SPARC median error {SPARC_MED:.3f} dex): not resolvable by SPARC", "DERIVED", "A3 (dual Kacanov; Plummer control)"),
    ("R7f", f"Solar System under the double filter: AQUAL floors {fl_txt} pc (Saturn monopole binds; QUMOND 0.0294/0.0316); strict "
            f"law excluded by its a0/2 tail (1279x / 1545x)", "DERIVED", "A4 (dual AQUAL; g02 read-only; FP1 reproduced)"),
    ("R7g", "FRW background = GR (chassis, J vanish; phibar-dot ~ a^-3, declared 0); a0 absent", "DERIVED", "B1"),
    ("R7h", "zero tangent: J is O(eps^3) around FRW and drops out of linear order", "DERIVED", "B2"),
    ("R7i", "zero-field well-posedness restored: omega^2 = 0 (marginal) + omega^2 > 0; E(C_phi) in (alpha_c, 2] (FP5's E > 2 band gone)",
     "DERIVED", "B3 (the naive chassis re-opens a growing band: MUTATE)"),
    ("R7j", "linear cosmology: no slip; G_eff/G_N = 1 + (2/5)(ck/aH)^2/lambda_eff (matter era), inertia-limited; lambda_eff = lambda + (2+3c_2)/c_2",
     "DERIVED", "B4 (sub-horizon reduction of the action's FRW equations)"),
    ("R7k", f"sigma_8 with no gate: lambda_eff <= 277 gives L341's ~ 20x; sigma_8 <= 1.02 needs lambda_eff >= {lam_sig:.1e}", "FAILS",
     "B5 + T (linear and physical-amplitude yardsticks, both footings)"),
    ("R7l", "strong coupling: Lambda_sc -> 0 at exact zero field; ell_sc <= ~1 mm in real backgrounds (tree level)", "DERIVED",
     "B6 (reported); the quantum zero-field question is OPEN"),
    ("R7m", "stability: no ghost, no gradient instability for monotone J (T = diag(4(2+3c_2)/c_2, 4 lambda), det V ~ C_phi); FC-KH's (yq)' "
            "obstruction absent", "DERIVED", "C1, C2"),
    ("R7n", "tracking: omega -> 0 gives static MOND iff c_2 C_phi != 0; c_s^2 = C_phi/lambda_eff; lambda = 0 reproduces c_2 >= 7.29e-3", "DERIVED", "C3"),
    ("R7o", "c_T = 1 (exact on flat space; ~1e-41 on MOND backgrounds)", "DERIVED", "D1"),
    ("R7p", "PPN: gamma = 1, alpha_3 = 0, closed-form alpha_1, alpha_2; filtered = khronometric; alpha_c <= 3.2e-9 unchanged; beta = 1 inherited",
     "DERIVED", "D2 (FP2's pipeline)"),
    ("R7q", "mode count N = 4 (lambda > 0) / 3 (lambda = 0); the filter adds none", "DERIVED", "E1"),
    ("R7r", "the fourth mode is not harmful (fifth force, PPN, Cherenkov, GW170817): the spec's limit is a preference", "DERIVED", "E2 (reported)"),
    ("R7s", "lambda (the MOND scalar's inertia): sigma_8 needs >= 1e7, tracking <= 2.8e4: EMPTY", "FAILS", "T"),
    ("R7t", "a web-vs-galaxy separation of the scalar's response (a new scale ~ Mpc in its inertia, or a density-read gate)", "OPEN",
     "T; with the zero tangent a gate need not vanish on FRW, so FP3's convexity lemma no longer binds -- FP3's chord bound (L* outskirts, KiDS) does; untested"),
    ("R7u", "nonlinear well-posedness; the L340 H4 O(Phi/c^2) lobes for the new sector; KiDS-EFE with AQUAL's EFE; Boltzmann-level cosmology",
     "OPEN", "not computed here"),
]
for k_, what, status, basis in LEDGER:
    P(f"    {k_:5s} {status:11s} {what}  --  {basis}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger of this lane", f"{len(LEDGER)} links", True, load_bearing=False)

# ================================================================================================ verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P(f"""  The AQUAL-type repair, varied as one action: the chassis is forced to the perfect square 2a^2 - (2 - alpha_c)|Dchi - a|^2 and
  the filter to the chassis (A1, A1b); the static law is two-field AQUAL with P2 exact in spherical symmetry (A2); thin discs differ
  from QUMOND by <= {worst_AQ:.3f} dex, below SPARC's resolution (A3); the filter carries over and the Solar System passes above
  {fl_txt} pc (A4).  On FRW the background is GR, J drops out of linear order (zero tangent), and the zero-field linearisation
  is well-posed -- FP5's Hadamard failure is cured (B1-B3).  The repair is healthy for any monotone J (C1-C2), its omega -> 0
  response is static MOND for sources slower than c_s = (C_phi/lambda_eff)^(1/2) c (C3), keeps c_T = 1 and khronometric PPN (D1-D2), and adds one propagating scalar that harms nothing in the channels
  checked (E).  It does NOT fix sigma_8: at zero field the MOND scalar is still sourced at linear order through the chassis and
  resisted only by inertia, a k^2-growing fifth force (ck/aH)^2/lambda_eff (B4); sigma_8 within 2% needs lambda_eff >= {lam_sig:.1e},
  tracking needs <= 277 (<= 2.8e4 at most) -- an empty window (T).  At the smallest inertia the action allows the web sits in MOND
  equilibrium and sigma_8 is L341's ~ 20x.  FP3's root cause was half the story: the infinite tangent caused the ill-posedness
  (fixed here); sigma_8 is the MOND response of the web itself, which no local, a0-free inertia can separate from galaxies.
  Time {time.time() - T0:.0f} s.""")
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {len(CH) - sum(1 for _, ok, _ in CH if not ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
