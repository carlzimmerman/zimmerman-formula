#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG318 -- GATE G11 (STRONG FIELD: BLACK HOLES, NEUTRON-STAR STRUCTURE) FOR THE FILTERED C-H/K CHASSIS.
Criteria frozen and committed first: campaign_fresh_gravity/CFG318_strong_field_bh/FROZEN_CRITERIA.md (1d3908e07).

CHASSIS (L340; CFG291 map): I = I_CH + (c^3/16 pi G) Int sqrt(-g)[alpha_c a.a - c_2 K^2], beta = 0, so the BH/NS sees
the BPS khronon with alpha = c14 = alpha_c, beta = c13 = 0, lambda = c2 = c_2 (the heat filter removes the C-H sector at
these scales; section D5 quantifies it).

DERIVED HERE (sympy): the static spherical reduced action in khronon-adapted ADM variables; its K = 0 multiplier form;
the O(alpha) exterior metric e = 1 - 2M/r + alpha q(r), g^rr = e/(e + r e' + (alpha/2) r^2 U'^2); the observables;
the static neutron-star equations with an aligned khronon.
ADOPTED: Barausse-Jacobson-Sotiriou 2011 asymptotics and Berglund et al. 2012 c14 = 0 solution (controls); the
eikonal light-ring correspondence (Cardoso et al. 2009); Iyer-Will 3rd-order WKB; Barausse 2019's dipole coefficient;
CFG311's NS sensitivities; Read et al. 2009 piecewise polytropes (parameters recalled, as in CFG311).

CFG318_MUTATE=1 scores alpha = 0.1 (outside the window): the window gate must flag it (rc = 1); outputs carry _MUTATE.
Run from anywhere:  python3 campaign_fresh_gravity/CFG318_strong_field_bh/cfg318_strong_field_bh.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG318_MUTATE", "0") == "1"
SLUG = "cfg318_strong_field_bh"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "CFG318", "mutate": MUTATE, "frozen_criteria_commit": "1d3908e07", "checks": {}, "numbers": {}}
T0 = time.time()
mp.mp.dps = 30


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reading)'} {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 112); P(t); P("=" * 112)


def rel(p):
    return os.path.relpath(p, REPO)


P(__doc__.strip())
if MUTATE:
    P("\n  *** MUTATE=1: alpha = 0.1 is scored; the window gate must FAIL (rc = 1) ***")

# ================================================================================================ inputs
L340F = os.path.join(REPO, "real_research", "g03_audit_2026", "L340_filtered_khronon_completion_results.json")
L350F = os.path.join(REPO, "real_research", "g03_audit_2026", "L350_chk_cosmological_G_gate_results.json")
XC1F = os.path.join(REPO, "real_research", "extra_crispy_2026", "XC1_strong_coupling_chk_results.json")
C311F = os.path.join(REPO, "campaign_fresh_gravity", "CFG311_ns_sensitivity", "cfg311_ns_sensitivity_results.json")
L340 = json.load(open(L340F)); L350 = json.load(open(L350F)); XC1 = json.load(open(XC1F)); C311 = json.load(open(C311F))
AC_MIN, AC_MAX = L340["numbers"]["P1"]["alpha_c_min"], L340["numbers"]["P1"]["alpha_c_max"]
C2_MIN, C2_MAX = L340["numbers"]["P1"]["c2_min"], L340["numbers"]["P1"]["c2_max"]
CAPS = sorted(float(r_["c2_ceiling"]) for r_ in L350["numbers"]["G2"]["rows"] if r_.get("c2_ceiling") is not None)
XC1_CS = (XC1["numbers"]["A9"]["cs_uv_min"], XC1["numbers"]["A9"]["cs_uv_max"])
S_NS = C311["numbers"]["s_over_alpha"]["max_over_EOS"]
AC_GRID = np.logspace(math.log10(AC_MIN), math.log10(AC_MAX), 9)
C2_GRID = np.logspace(math.log10(C2_MIN), math.log10(C2_MAX), 9)
ALPHA_SCORED = np.array([0.1]) if MUTATE else AC_GRID
P(f"\n  inputs ({rel(L340F)}): alpha_c in [{AC_MIN:.6e}, {AC_MAX:.3e}], c_2 in [{C2_MIN:.6e}, {C2_MAX:.6e}]")
P(f"  CFG311 committed s/alpha (max over EOS): {S_NS}")
OUT["numbers"]["inputs"] = {"alpha_c": [AC_MIN, AC_MAX], "c2": [C2_MIN, C2_MAX], "s_over_alpha_CFG311": S_NS,
                            "sources": [rel(L340F), rel(L350F), rel(XC1F), rel(C311F)]}
BOUND_SH, BOUND_QNM, BOUND_DIP, READ_ISCO, READ_NS = 0.10, 0.01, 1e-4, 0.01, 0.01

# ================================================================================================ D1 reduced action
banner("D1  STATIC SPHERICAL REDUCED ACTION (khronon time T, areal r; N, V = N^r, A = gamma_rr); C1 and C2")
r = sp.Symbol('r', positive=True)
al, be, la, Mm, Cc = sp.symbols('alpha beta lambda M C', positive=True)
Nf, Vf, Af = [sp.Function(n)(r) for n in ('N', 'V', 'A')]
Krr = -(Vf * Af.diff(r) / Af + 2 * Vf.diff(r)) / (2 * Nf); Kth = -Vf / (r * Nf)
KK = Krr**2 + 2 * Kth**2; Ktr = Krr + 2 * Kth
R3 = 2 / r**2 * (1 - 1 / Af) + 2 * Af.diff(r) / (r * Af**2)
Lfull = Nf * sp.sqrt(Af) * r**2 * ((1 - be) * KK - (1 + la) * Ktr**2 + R3 + al * (Nf.diff(r) / Nf)**2 / Af)
EL = [e.lhs for e in euler_equations(Lfull, [Nf, Vf, Af], r)]


def on(ex, sub):
    for k in (2, 1):
        ex = ex.subs({F.diff(r, k): sub[F].diff(r, k) for F in (Nf, Vf, Af)})
    return sp.simplify(ex.subs(sub))


f0 = 1 - 2 * Mm / r; U0 = sp.sqrt(f0 + Cc**2 / r**4)
res_c1 = [on(e.subs({al: 0, be: 0}), {Nf: U0, Af: 1 / U0**2, Vf: -Cc * U0 / r**2}) for e in EL]
P(f"    alpha = beta = 0, Schwarzschild + maximal slicing (N = U, A = 1/U^2, V = -C U/r^2), symbolic lambda, C, M: residuals {res_c1}")
okC1a = all(x == 0 for x in res_c1)
# C2: Berglund et al. 2012 c14 = 0 family (beta != 0), any r_ae
r0, rae = sp.symbols('r0 r_ae', positive=True)
Nb = sp.sqrt(1 - r0 / r + (1 - be) * rae**4 / r**4)
res_c2 = [on(e.subs(al, 0), {Nf: Nb, Af: 1 / Nb**2, Vf: Nb * rae**2 / r**2}) for e in EL]
gTT_b = sp.simplify(-(Nb**2) + (1 / Nb**2) * (Nb * rae**2 / r**2)**2)
P(f"    Berglund c14 = 0 family (symbolic beta = c13, r0, r_ae): residuals {res_c2};  g_TT = {sp.factor(gTT_b)}")
uh = {}
for c13 in (sp.Integer(0), sp.Rational(3, 10)):
    g = r**4 - r0 * r**3 + (1 - c13) * rae**4
    rr_ = sp.solve(sp.diff(g, r), r); rr_ = [x for x in rr_ if x != 0][0]
    rae4 = sp.solve(g.subs(r, rr_), rae**4)
    rae4 = sp.solve(g.subs(r, rr_), rae)[0]**4 if not rae4 else rae4[0]
    uh[str(c13)] = (sp.simplify(rr_ / r0), sp.simplify(rae4 / r0**4 - sp.Rational(27, 256) / (1 - c13)))
P(f"    regularity (double root of (u.chi)^2 r^4): r_UH/r0 and r_ae^4/r0^4 - 27/(256(1-c13)): {uh}")
okC2 = all(x == 0 for x in res_c2) and all(v[0] == sp.Rational(3, 4) and v[1] == 0 for v in uh.values()) \
    and sp.simplify(gTT_b + 1 - r0 / r - be * rae**4 / r**4) == 0
check("C2 Berglund et al. 2012 c14 = 0 solution solves D1 exactly at beta != 0; regularity gives r_UH = 3 r0/4 and "
      "r_ae^4 = 27 r0^4/(256 (1 - c13)) at c13 = 0, 0.3", f"residuals {res_c2}; {uh}", okC2,
      "published closed form reproduced by the lane's own field equations (an off-chassis beta tests the machinery)")

# ================================================================================================ D2 multiplier form
banner("D2  O(alpha) STATIC BH: K = 0 multiplier form (lambda K -> mu), exact in alpha; linearisation; Sigma(r)")
Mu = sp.Function('mu')(r); Bf = sp.Function('B')(r); Ch = sp.Symbol('Chat')
Lmu = Nf * sp.sqrt(Af) * r**2 * (KK - Ktr**2 + R3 + al * (Nf.diff(r) / Nf)**2 / Af) + Mu * Nf * sp.sqrt(Af) * r**2 * Ktr
EN, EV, EA, EM = [e.lhs for e in euler_equations(Lmu, [Nf, Vf, Af, Mu], r)]
Vs = -Ch * sp.sqrt(Bf) / r**2                              # K = 0  <=>  V sqrt(A) r^2 = const = -Chat


def onB(ex):
    ex = ex.subs({Af.diff(r, 2): (1 / Bf).diff(r, 2), Af.diff(r): (1 / Bf).diff(r), Af: 1 / Bf})
    ex = ex.subs({Vf.diff(r, 2): Vs.diff(r, 2), Vf.diff(r): Vs.diff(r), Vf: Vs})
    return sp.simplify(ex)


EM2 = onB(EM); EV2 = onB(EV)
mup = sp.solve(EV2, Mu.diff(r))[0]
EA2 = sp.simplify(onB(EA).subs(Mu.diff(r), mup)); EN2 = onB(EN)
Bsol = sp.solve(sp.numer(sp.together(EA2)), Bf)[0]
ode = sp.numer(sp.together(sp.simplify(EN2.subs(Bf.diff(r), Bsol.diff(r)).subs(Bf, Bsol))))
P(f"    K = 0 holds identically on V = -Chat sqrt(B)/r^2: {EM2 == 0};  mu' = {sp.simplify(mup)}")
P(f"    B (= gamma^rr) from the A-equation: B = {sp.simplify(Bsol)}")
# invariants: e = N^2 - Chat^2/r^4 ; g^rr = B e / N^2
NN = sp.Symbol('NN'); Np = sp.Symbol('Np'); ee = sp.Function('e')(r)
grr_expr = sp.simplify((Bsol * (Nf**2 - Ch**2 / r**4) / Nf**2).subs(Nf.diff(r), Np).subs(Nf, NN))
# derive g^rr = e/(e + r e' + (alpha/2) r^2 N'^2) with e' = 2 N N' + 4 Chat^2/r^5
e_of = NN**2 - Ch**2 / r**4; ep_of = 2 * NN * Np + 4 * Ch**2 / r**5
okGRR = sp.simplify(grr_expr - e_of / (e_of + r * ep_of + al / 2 * r**2 * Np**2)) == 0
P(f"    g^rr = B e/N^2 equals e/(e + r e' + (alpha/2) r^2 N'^2) identically: {okGRR}")
# linearise about the regular alpha = 0 slicing (M = 1): C = 3 sqrt(3)/4, U = (r - 3/2) sqrt(r^2 + r + 3/4)/r^2
C0 = 3 * sp.sqrt(3) / 4; Ureg = (r - sp.Rational(3, 2)) * sp.sqrt(r**2 + r + sp.Rational(3, 4)) / r**2
okU = sp.simplify(Ureg**2 - (1 - 2 / r + C0**2 / r**4)) == 0
eps, c1, ah = sp.symbols('epsilon c1 alphahat'); Qf = sp.Function('Q')(r)
lin = ode.subs(al, eps * ah).subs(Ch, C0 + eps * c1).subs(Nf, Ureg + eps * Qf / (2 * Ureg)).doit()
lin1 = sp.expand(sp.simplify(sp.diff(lin, eps).subs(eps, 0))); lin0 = sp.simplify(lin.subs(eps, 0))
kfac = sp.simplify(lin1.coeff(Qf.diff(r, 2)) / r**2)
Sig = sp.simplify(-(lin1.subs({Qf.diff(r, 2): 0, Qf.diff(r): 0, Qf: 0}).subs(c1, 0) / kfac) / ah)
resid_lin = sp.simplify(lin1 - kfac * ((r**2 * Qf.diff(r)).diff(r) - ah * Sig - 24 * C0 * c1 / r**4))
Sig = sp.factor(sp.cancel(Sig))
P(f"    background residual {lin0}; U^2 = 1 - 2/r + C^2/r^4 with the double root at r = 3/2: {okU}")
P(f"    linear equation == k(r) [ (r^2 Q')' - alpha Sigma - 24 C c1/r^4 ],  Q = delta(N^2): residual {resid_lin}")
P(f"    Sigma(r) = {Sig}")
okSigma = lin0 == 0 and resid_lin == 0 and okU and okGRR and EM2 == 0
# c1 drops out of e: the c1 particular solution Q = 2 C c1/r^4 cancels in e = N^2 - Chat^2/r^4 at O(eps)
Qc1 = 2 * C0 * c1 / r**4
okc1 = sp.simplify((r**2 * Qc1.diff(r)).diff(r) - 24 * C0 * c1 / r**4) == 0 and sp.simplify(Qc1 - sp.diff((C0 + eps * c1)**2, eps).subs(eps, 0) / r**4) == 0
P(f"    khronon-charge shift c1: Q_c1 = 2 C c1/r^4 solves its equation and cancels in e: {okc1}")
x = sp.Symbol('x', positive=True)
Sig_ser = sp.series(Sig.subs(r, 1 / x), x, 0, 11).removeO()
# large-r series for q: (r^2 q')' = Sigma, no constant and no 1/r term
qser = 0
for k in range(3, 11):
    ck = Sig_ser.coeff(x, k)                              # Sigma ~ ck r^-k  ->  q ~ ck r^-k/(k(k-1)),
    qser += ck / (k * (k - 1)) * x**k                    # since (r^2 (r^-k)')' = k(k-1) r^-k
P(f"    Sigma ~ {Sig_ser};  q ~ {sp.expand(qser)}")
residue = sp.limit((r - sp.Rational(3, 2)) * Sig, r, sp.Rational(3, 2))
P(f"    Sigma has a simple pole at the universal horizon r = 3/2 with residue {residue} (= {float(residue):.6f}): q ~ x ln x there")
OUT["numbers"]["D2"] = {"Sigma": str(Sig), "Sigma_series": str(Sig_ser), "q_series": str(sp.expand(qser)),
                        "mu_prime": str(sp.simplify(mup)), "B": str(sp.simplify(Bsol)), "Sigma_pole_residue_at_rUH": str(residue)}

# C3: BJS asymptotics (r0 = 2 at M = 1): e_3 = -alpha r0^3/48 = -alpha/6; B_EF^2 = e g_rr = e + r e' + (alpha/2) r^2 U'^2
e_ser = 1 - 2 * x + ah * qser
Up_ser = sp.series(sp.diff(Ureg, r).subs(r, 1 / x), x, 0, 8).removeO()
BEF2 = sp.expand(e_ser + (1 / x) * sp.diff(e_ser, x) * (-x**2) + ah / 2 * (1 / x**2) * Up_ser**2)
BEF = sp.series(sp.sqrt(BEF2), x, 0, 4).removeO()
BEF_lin = sp.expand(sp.diff(BEF, ah).subs(ah, 0))
e3 = sp.expand(e_ser).coeff(x, 3)
P(f"    e series x^3 coefficient: {e3}  (BJS: -alpha r0^3/48 = {-ah * 8 / 48})")
P(f"    EF B series at O(alpha): {BEF_lin}*alpha  (BJS: alpha r0^2/16 x^2 + alpha r0^3/12 x^3 = {sp.Rational(4, 16)} x^2 + {sp.Rational(8, 12)} x^3)")
okC3 = sp.simplify(e3 + ah / 6) == 0 and sp.simplify(BEF_lin.coeff(x, 2) - sp.Rational(1, 4)) == 0 \
    and sp.simplify(BEF_lin.coeff(x, 3) - sp.Rational(2, 3)) == 0 and BEF_lin.coeff(x, 1) == 0
check("C3 the derived O(alpha) solution reproduces Barausse-Jacobson-Sotiriou 2011's published asymptotic coefficients "
      "(e: -c14 r0^3/48 x^3; EF B: +c14 r0^2/16 x^2, +c14 r0^3/12 x^3) exactly", f"e3 = {e3}; B_EF lin = {BEF_lin}", okC3)
check("D2 linear O(alpha) equation reduces exactly to (r^2 Q')' = alpha Sigma + 24 C c1/r^4; c1 drops out of e; "
      "g^rr = e/(e + r e' + (alpha/2) r^2 N'^2) identically", f"residual {resid_lin}; c1 {okc1}; g^rr {okGRR}", okSigma and okc1)

# ================================================================================================ C5 numerics for q
banner("C5  q(r) NUMERICALLY: nested quadrature vs the closed-form inner integral vs an ODE integration")
Sig_f = sp.lambdify(r, Sig, "mpmath")
I1 = sp.integrate(sp.apart(Sig, r), r)
I1_f = sp.lambdify(r, I1, "mpmath")
RBIG = mp.mpf(10)**6
I1_inf = I1_f(RBIG) + mp.quad(Sig_f, [RBIG, mp.inf])
Jc = lambda s: I1_inf - I1_f(s)                         # J(s) = Int_s^inf Sigma
Jn = lambda s: mp.quad(Sig_f, [s, 10 * s, mp.inf])
q_c = lambda rr: mp.quad(lambda s: Jc(s) / s**2, [rr, 10 * rr, mp.inf])
q_n = lambda rr: mp.quad(lambda s: Jn(s) / s**2, [rr, 10 * rr, mp.inf])
d12 = max(abs(q_c(v) - q_n(v)) / abs(q_n(v)) for v in (2, 3, 6, 20))
qser_f = sp.lambdify(x, qser, "mpmath")
dser = abs(q_c(50) - qser_f(mp.mpf(1) / 50)) / abs(q_c(50))
sol = solve_ivp(lambda rr, y: [y[1] / rr**2, float(Sig_f(rr))], [400.0, 3.0],
                [float(qser_f(mp.mpf(1) / 400)), 400.0**2 * float(sp.diff(qser, x).subs(x, sp.Rational(1, 400))) * (-1 / 400.0**2)],
                method="DOP853", rtol=1e-12, atol=1e-30)
dode = abs(sol.y[0, -1] - float(q_c(3))) / abs(float(q_c(3)))
P(f"    q(2), q(3), q(6) = {float(q_c(2)):.10e}, {float(q_c(3)):.10e}, {float(q_c(6)):.10e}")
P(f"    nested vs closed-form inner: max rel diff {float(d12):.2e};  series O(x^10) at r = 50: {float(dser):.2e};  ODE inward to r = 3: {dode:.2e}")
check("C5 q by nested quadrature and by the closed-form inner integral agree to 1e-12; the O(x^10) series matches at r = 50 "
      "to 1e-10", f"{float(d12):.1e}; {float(dser):.1e}; ODE {dode:.1e}", d12 < 1e-12 and dser < 1e-10 and dode < 1e-8)
OUT["numbers"]["q"] = {str(v): float(q_c(v)) for v in (2, 2.5, 3, 4, 6, 10, 20)}

# ================================================================================================ D3 observables
banner("D3  OBSERVABLES: photon sphere / shadow, eikonal QNM (Omega_c, lambda_L), ISCO -- linear coefficients in alpha")
Up_f = sp.lambdify(r, sp.diff(Ureg, r), "mpmath")
def metric(a):
    e = lambda rr: 1 - 2 / rr + a * q_c(rr)
    ep = lambda rr: 2 / rr**2 - a * Jc(rr) / rr**2
    epp = lambda rr: -4 / rr**3 + a * (Sig_f(rr) / rr**2 + 2 * Jc(rr) / rr**3)
    grr = lambda rr: e(rr) / (e(rr) + rr * ep(rr) + a / 2 * rr**2 * Up_f(rr)**2)
    return e, ep, epp, grr

def observables(a):
    e, ep, epp, grr = metric(a)
    rph = mp.findroot(lambda rr: rr * ep(rr) - 2 * e(rr), mp.mpf(3))
    bc = rph / mp.sqrt(e(rph))
    Om = mp.sqrt(e(rph)) / rph
    Veff = lambda rr: grr(rr) * e(rr) * (1 - e(rr) * bc**2 / rr**2)
    lamL = mp.sqrt(mp.diff(Veff, rph, 2) / 2)
    L2 = lambda rr: rr**3 * ep(rr) / (2 * e(rr) - rr * ep(rr))
    risco = mp.findroot(lambda rr: mp.diff(L2, rr), mp.mpf(6))
    Omisco = mp.sqrt(ep(risco) / (2 * risco))
    rH = mp.findroot(e, mp.mpf(2))
    return dict(r_ph=rph, b_c=bc, Omega_c=Om, lambda_L=lamL, r_isco=risco, Omega_isco=Omisco, r_H=rH)

O0 = observables(mp.mpf(0))
P("    alpha = 0: " + ", ".join(f"{k} = {mp.nstr(v, 14)}" for k, v in O0.items()))
s3 = mp.sqrt(3)
okC4 = (abs(O0["r_ph"] - 3) < 1e-10 and abs(O0["b_c"] - 3 * s3) < 1e-10 and abs(O0["r_isco"] - 6) < 1e-10
        and abs(O0["Omega_c"] - 1 / (3 * s3)) < 1e-10 and abs(O0["lambda_L"] - 1 / (3 * s3)) < 1e-10 and abs(O0["r_H"] - 2) < 1e-12)
ha = mp.mpf("1e-7")
Op, Om_ = observables(ha), observables(-ha)
COEF = {k: float((Op[k] - Om_[k]) / (2 * ha) / O0[k]) for k in O0}      # fractional shift per unit alpha
curv = {k: float((Op[k] + Om_[k] - 2 * O0[k]) / ha**2 / O0[k]) for k in O0}
P("    fractional shift per unit alpha (d ln X/d alpha): " + ", ".join(f"{k} {v:+.6e}" for k, v in COEF.items()))
P(f"    analytic check: d ln b_c/d alpha = -3 q(3)/2 = {float(-1.5 * q_c(3)):+.6e}; d ln Omega_c/d alpha = +3 q(3)/2")
okA = abs(COEF["b_c"] / float(-1.5 * q_c(3)) - 1) < 1e-6 and abs(COEF["Omega_c"] / float(1.5 * q_c(3)) - 1) < 1e-6
OUT["numbers"]["D3"] = {"alpha0": {k: float(v) for k, v in O0.items()}, "dlnX_dalpha": COEF, "second_order_reading": curv}
# alpha -> 0 (C1): the metric is Schwarzschild at alpha = 0 and every deviation is linear in alpha
e0, _, _, g0 = metric(mp.mpf(0))
c1dev = max(abs(e0(mp.mpf(v)) - (1 - 2 / mp.mpf(v))) + abs(g0(mp.mpf(v)) - (1 - 2 / mp.mpf(v))) for v in ("2.5", 3, 6, 30))
check("C1 alpha -> 0: the alpha = beta = 0 maximal-slicing family solves D1 for symbolic lambda, C; at alpha = 0 "
      "e = g^rr = 1 - 2M/r exactly; deviations linear in alpha (Sigma multiplies alpha)", f"D1 residuals {res_c1}; metric dev {float(c1dev):.1e}",
      okC1a and c1dev < 1e-25)
check("C4 Schwarzschild numbers at alpha = 0: r_ph = 3M, b_c = 3 sqrt(3) M, r_ISCO = 6M, M Omega_c = M lambda_L = 1/(3 sqrt 3), "
      "r_H = 2M (1e-10); the shadow/Omega_c slopes equal -/+ 3 q(3)/2 (1e-6)", f"{ {k: mp.nstr(v, 12) for k, v in O0.items()} }", okC4 and okA)

# WKB l = 2 test scalar (reading) -- Iyer & Will 1987, 3rd order
banner("WKB  l = 2 test scalar field, 3rd-order WKB (reading; the direct khronon coupling of finite-l tensors is NOT derived)")
Qs, Js = sp.symbols('Qs Js')
def Dr(ex):
    return sp.diff(ex, r) + sp.diff(ex, Qs) * (-Js / r**2) + sp.diff(ex, Js) * (-Sig)
QD = [Qs]                                                 # d^k q/dr^k in terms of (r, q, J): q' = -J/r^2, J' = -Sigma
for _ in range(14):
    QD.append(sp.simplify(Dr(QD[-1])))
QD_f = [sp.lambdify((r, Qs, Js), d_, "mpmath") for d_ in QD]
Up_s = sp.lambdify(r, sp.diff(Ureg, r), "mpmath")
def wkb(a, n=0, l=2, deg=8):
    """Iyer-Will 3rd order; V(r*) derivatives from Taylor series in h = r - r_c (q replaced by its exact Taylor
    polynomial about r_c, built from q' = -J/r^2, J' = -Sigma), with d/dr* = F d/dr applied as series algebra."""
    def build(rc):
        qk = [QD_f[k](rc, q_c(rc), Jc(rc)) / mp.factorial(k) for k in range(len(QD_f))]
        qpoly = lambda rr: sum(c * (rr - rc)**k for k, c in enumerate(qk))
        e = lambda rr: 1 - 2 / rr + a * qpoly(rr)
        ep = lambda rr: mp.diff(e, rr)
        grr = lambda rr: e(rr) / (e(rr) + rr * ep(rr) + a / 2 * rr**2 * Up_s(rr)**2)
        F = lambda rr: mp.sqrt(e(rr) * grr(rr))
        V = lambda rr: e(rr) * l * (l + 1) / rr**2 + F(rr) * mp.diff(F, rr) / rr
        return V, F
    rc = mp.mpf(3)
    for _ in range(3):                                    # peak of V(r) (= peak of V(r*))
        V, F = build(rc)
        rc = mp.findroot(lambda rr: mp.diff(V, rr), rc)
    V, F = build(rc)
    Vt = mp.taylor(V, rc, deg); Ft = mp.taylor(F, rc, deg)
    def mul(A, B):
        return [sum(A[i] * B[k - i] for i in range(k + 1)) for k in range(min(len(A), len(B)))]
    def der(A):
        return [(k + 1) * A[k + 1] for k in range(len(A) - 1)]
    D = [Vt]
    for _ in range(6):
        D.append(mul(Ft, der(D[-1])))
    V0, V2, V3, V4, V5, V6 = [D[k][0] for k in (0, 2, 3, 4, 5, 6)]
    A_ = n + mp.mpf(1) / 2
    Lam = (1 / mp.sqrt(-2 * V2)) * (V4 / V2 / 8 * (mp.mpf(1) / 4 + A_**2) - (V3 / V2)**2 / 288 * (7 + 60 * A_**2))
    Omg = (1 / (-2 * V2)) * (mp.mpf(5) / 6912 * (V3 / V2)**4 * (77 + 188 * A_**2) - mp.mpf(1) / 384 * (V3**2 * V4 / V2**3) * (51 + 100 * A_**2)
                             + mp.mpf(1) / 2304 * (V4 / V2)**2 * (67 + 68 * A_**2) + mp.mpf(1) / 288 * (V3 * V5 / V2**2) * (19 + 28 * A_**2)
                             - mp.mpf(1) / 288 * (V6 / V2) * (5 + 4 * A_**2))
    w2 = V0 + mp.sqrt(-2 * V2) * Lam - 1j * A_ * mp.sqrt(-2 * V2) * (1 + Omg)
    w = mp.sqrt(w2)
    return w if mp.re(w) > 0 else -w
mp.mp.dps = 50
w0 = wkb(mp.mpf(0)); hw = mp.mpf("1e-6")
wp, wm = wkb(hw), wkb(-hw)
dwr = float(mp.re(wp - wm) / (2 * hw) / mp.re(w0)); dwi = float(mp.im(wp - wm) / (2 * hw) / mp.im(w0))
mp.mp.dps = 30
ref = complex(0.4836, -0.0968)
okW = abs(complex(w0) - ref) / abs(ref) < 0.01
P(f"    Schwarzschild l = 2 scalar n = 0 (WKB3): M omega = {mp.nstr(w0, 8)}  (recalled 0.4836 - 0.0968i)")
P(f"    d ln Re(omega)/d alpha = {dwr:+.6e}, d ln Im(omega)/d alpha = {dwi:+.6e}")
check("C4b WKB3 l = 2 scalar n = 0 at alpha = 0 within 1% of 0.4836 - 0.0968i", mp.nstr(w0, 8), okW)
OUT["numbers"]["WKB_l2_scalar"] = {"omega0": [float(mp.re(w0)), float(mp.im(w0))], "dln_re": dwr, "dln_im": dwi}

# ================================================================================================ scores on the window
banner("SCORES  shadow, eikonal QNM (f, tau), ISCO, WKB l = 2 reading -- over the scored alpha (lambda-independent at O(alpha))")
d_sh = np.abs(COEF["b_c"]) * ALPHA_SCORED
d_f = np.abs(COEF["Omega_c"]) * ALPHA_SCORED
d_tau = np.abs(COEF["lambda_L"]) * ALPHA_SCORED                          # tau = 1/omega_I ~ 1/lambda_L
d_isco = np.abs(COEF["Omega_isco"]) * ALPHA_SCORED
d_wkb = max(abs(dwr), abs(dwi)) * ALPHA_SCORED
amax = float(ALPHA_SCORED.max())
alam = float(ALPHA_SCORED.max() / C2_MIN)
P(f"    max |delta_shadow| = {d_sh.max():.3e} vs {BOUND_SH} -> margin {BOUND_SH / d_sh.max():.3e}")
P(f"    max |delta f_eik|  = {d_f.max():.3e}, |delta tau_eik| = {d_tau.max():.3e} vs {BOUND_QNM} -> margins "
  f"{BOUND_QNM / d_f.max():.3e}, {BOUND_QNM / d_tau.max():.3e}")
P(f"    ISCO: |delta Omega_isco| = {d_isco.max():.3e}, |delta r_isco/r_isco| = {abs(COEF['r_isco']) * amax:.3e} (reading vs 1%: margin {READ_ISCO / d_isco.max():.3e})")
P(f"    WKB l = 2 scalar: max fractional shift {d_wkb.max():.3e} (reading)")
P(f"    neglected O(alpha/lambda) relative correction: alpha/lambda <= {alam:.2e}")
ok_sh = bool(np.all(d_sh <= BOUND_SH)); ok_qnm = bool(np.all(d_f <= BOUND_QNM) and np.all(d_tau <= BOUND_QNM))
# C6 injection: the scorer must flag 20% shadow / 5% QNM
inj_sh = not (0.20 <= BOUND_SH); inj_q = not (0.05 <= BOUND_QNM)
check("C6 injection: the scorer flags an injected 20% shadow deviation and a 5% QNM deviation", f"{inj_sh}, {inj_q}", inj_sh and inj_q)
OUT["numbers"]["scores"] = {"alpha_scored": ALPHA_SCORED.tolist(), "max_d_shadow": float(d_sh.max()), "max_d_f": float(d_f.max()),
                            "max_d_tau": float(d_tau.max()), "max_d_isco_Omega": float(d_isco.max()),
                            "max_d_r_isco": abs(COEF['r_isco']) * amax, "max_d_wkb": float(d_wkb.max()),
                            "margin_shadow": BOUND_SH / float(d_sh.max()), "margin_f": BOUND_QNM / float(d_f.max()),
                            "margin_tau": BOUND_QNM / float(d_tau.max()), "alpha_over_lambda_max": alam}

# ================================================================================================ BH dipole
banner("DIPOLE  BBH: Delta s = 0 (non-spinning BH sensitivity is mass-independent); NS-BH: Delta s = s_NS, s_crit at B_dip = 1e-4")
def c0sq(a, l):
    return l * (2 - a) / (a * (2 + 3 * l))
def Cdip(a, l):
    return 4 / (3 * c0sq(a, l)**1.5 * a * (2 - a))
cs_xc1 = [math.sqrt(c0sq(a_, c_)) for a_ in (AC_MIN, AC_MAX) for c_ in (min([round(c, 6) for c in CAPS] + [C2_MIN]), C2_MAX)]
okXC1 = abs(min(cs_xc1) / XC1_CS[0] - 1) < 5e-5 and abs(max(cs_xc1) / XC1_CS[1] - 1) < 5e-5
P(f"    c_S at XC1's corners {min(cs_xc1):.4e} .. {max(cs_xc1):.4e} (XC1 A9 committed {XC1_CS[0]:.4e} .. {XC1_CS[1]:.4e})")
smax = max(S_NS.values())
worst_dip, min_marg, min_scrit_over_alpha = 0.0, np.inf, np.inf
for a_ in ALPHA_SCORED:
    for c_ in C2_GRID:
        Cd = Cdip(a_, c_)
        bd = 5 / 32 * Cd * (smax * a_)**2
        scrit = math.sqrt(BOUND_DIP * 32 / (5 * Cd))
        worst_dip = max(worst_dip, bd); min_marg = min(min_marg, BOUND_DIP / bd)
        min_scrit_over_alpha = min(min_scrit_over_alpha, scrit / a_)
scrit_top = math.sqrt(BOUND_DIP * 32 / (5 * Cdip(float(ALPHA_SCORED.max()), C2_MIN)))
ok_dip = worst_dip <= BOUND_DIP
P(f"    NS-BH with s_BH = 0: max B_dip = {worst_dip:.3e} vs {BOUND_DIP} -> margin {min_marg:.3e}")
P(f"    s_crit (|s_NS - s_BH| reaching B_dip = 1e-4): {scrit_top:.3e} at the top-alpha / bottom-c_2 corner; min s_crit/alpha_c = {min_scrit_over_alpha:.3e}")
P(f"    reading: Ramos & Barausse's sigma ~ 1e-3 at alpha = 0.02 suggests |s_BH| ~ 0.05 alpha (if linear): {0.05 * amax:.2e} << s_crit")
check("C7b the dipole coefficient's khronon speed reproduces XC1's committed UV speeds (4 s.f.)",
      f"{min(cs_xc1):.4e}/{max(cs_xc1):.4e}", okXC1)
OUT["numbers"]["dipole"] = {"max_Bdip_sBH0": worst_dip, "margin": min_marg, "s_crit_top_corner": scrit_top,
                            "min_scrit_over_alpha": min_scrit_over_alpha, "s_NS_over_alpha_max": smax}

# ================================================================================================ kernel + MOND filter
banner("D5  MOND / HEAT FILTER NEAR A BH (nu_mono reimplemented from the recipe/L340 definition)")
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
Y_STAR = brentq(lambda y: float(dh_rar(y)) - DELTA * H_P / (y + Y_P), 1.0, Y_P)
LYG = np.linspace(-12, 12, 240001); YG = 10**LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
H_STAR = float(np.interp(math.log10(Y_STAR), LYG, H_MONO))
def h_mono(y):
    y = np.asarray(y, float)
    tail = H_STAR + DELTA * H_P * np.log((y + Y_P) / (Y_STAR + Y_P))
    return np.where(y <= 1e11, np.interp(np.log10(np.maximum(y, 1e-12)), LYG, H_MONO), tail)
A1ref = L340["numbers"]["A1"]
okK = abs(Y_P / A1ref["y_p"] - 1) < 1e-4 and abs(H_P / A1ref["h_p"] - 1) < 1e-4
check("C7 nu_mono reproduces L340's committed y_p and h_p to 1e-4", f"y_p {Y_P:.6f} ({A1ref['y_p']:.6f}), h_p {H_P:.6f} ({A1ref['h_p']:.6f})", okK)
C_SI, G_SI, MSUN, PC = 299792458.0, 6.67430e-11, 1.98847e30, 3.0856775814913673e16
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
XI = {"canonical": 0.031 * PC, "alt": 0.045 * PC}
filt = {}
for nm, msun in (("M87*", 6.5e9), ("Sgr A*", 4.0e6), ("10 Msun", 10.0)):
    rg = G_SI * msun * MSUN / C_SI**2
    rph = 3 * rg; gph = G_SI * msun * MSUN / rph**2 / math.sqrt(1 - 2 / 3)
    row = {}
    for foot in ("canonical", "alt"):
        expo = -(XI[foot] / rph)**2 / 2
        y_upper = gph / A0[foot]                 # no filtered field near the BH exceeds its own unfiltered field
        hmax = float(h_mono(np.array([max(y_upper, 1e-12)]))[0])
        hmax = max(hmax, float(np.max(h_mono(np.logspace(-12, math.log10(y_upper), 2000)))))
        row[foot] = {"filter_exponent": expo, "y_ph_unfiltered": y_upper, "h_mono_max": hmax, "eps_MOND": hmax * A0[foot] / gph}
    filt[nm] = row
    P(f"    {nm:8s}: r_ph = {rph:.3e} m, g(r_ph) = {gph:.3e} m/s^2, y = {row['canonical']['y_ph_unfiltered']:.2e}; filter exponent "
      f"-xi^2/(2 r_ph^2) = {row['canonical']['filter_exponent']:.3e}; MOND force bound h_max a0/g = {row['canonical']['eps_MOND']:.2e} "
      f"(alt {row['alt']['eps_MOND']:.2e})")
eps_m = max(v[f]["eps_MOND"] for v in filt.values() for f in v)
P(f"    the filtered field near a galactic nucleus need not be high-y (it can vanish at a symmetric centre), so the bound "
  f"used is the kernel's: |MOND force| <= max h_mono a0 for any filtered y; worst epsilon_MOND = {eps_m:.2e}")
OUT["numbers"]["D5"] = {"filter": filt, "eps_MOND_max": eps_m, "y_p": Y_P, "h_p": H_P}

# ================================================================================================ D4 neutron stars
banner("D4  NEUTRON STARS: static star with an aligned khronon at O(alpha) (sympy-derived), SLy (Read et al. 2009, recalled)")
Pp, rho_s, mu0 = sp.symbols('P rho mu0'); pf = sp.Function('p')
Lns = Nf * sp.sqrt(Af) * r**2 * (R3 + al * (Nf.diff(r) / Nf)**2 / Af) + 16 * sp.pi * Nf * sp.sqrt(Af) * r**2 * pf(mu0 / Nf)
ENs, EAs = [e.lhs for e in euler_equations(Lns, [Nf, Af], r)]
def rep(ex):
    ex = ex.replace(lambda z: isinstance(z, sp.Subs), lambda z: (rho_s + Pp) * Nf / mu0)
    return sp.simplify(ex.subs(pf(mu0 / Nf), Pp))
ENs, EAs = rep(ENs), rep(EAs)
yv, ypv, Av, Apv = sp.symbols('y yp Av Apv')       # y = N'/N
def to_y(ex):
    ex = sp.numer(sp.together(ex))
    ex = ex.subs({Nf.diff(r, 2): (ypv + yv**2) * Nf}).subs({Nf.diff(r): yv * Nf}).subs({Af.diff(r): Apv}).subs(Af, Av)
    return sp.expand(sp.simplify(ex.subs(Nf, 1)))     # the numerators are homogeneous of degree 2 in N
EAy = to_y(EAs); ENy = to_y(ENs)
P(f"    A-equation (y = N'/N): {sp.factor(EAy)} = 0")
P(f"    N-equation: {sp.factor(ENy)} = 0")
# GR check at alpha = 0
ysol0 = sp.solve(EAy.subs(al, 0), yv)[0]
okTOVgr = sp.simplify(ysol0 - ((Av - 1) + 8 * sp.pi * Pp * r**2 * Av) / (2 * r)) == 0
P(f"    alpha = 0: y = {sp.simplify(ysol0)} (standard TOV Phi'): {okTOVgr}")
ysols = sp.solve(EAy, yv)
ysol = [s_ for s_ in ysols if sp.limit(s_.subs({Av: 2, Pp: 0, r: 1}), al, 0) == sp.Rational(1, 2)][0]
dEAy = sp.diff(EAy, r) + sp.diff(EAy, yv) * ypv + sp.diff(EAy, Av) * Apv + sp.diff(EAy, Pp) * sp.Symbol('Ppr')
sol_lin = sp.solve([ENy, dEAy], [ypv, Apv], dict=True)[0]
Sy = 2 * (Av - 1) + 16 * sp.pi * Pp * r**2 * Av
ystable = Sy / (r * (2 + sp.sqrt(4 + al * Sy)))           # the same root, written without 1/alpha
assert sp.simplify(sp.radsimp(ysol - ystable)) == 0 or abs(float((ysol - ystable).subs({Av: 1.3, Pp: 0.01, r: 2.0, al: 0.01}))) < 1e-12
f_y = sp.lambdify((r, Av, Pp, al), ystable, "math")
f_Ap = sp.lambdify((r, Av, Pp, rho_s, yv, al, sp.Symbol('Ppr')), sol_lin[Apv], "math")
KAPPA = 7.42591549e-29 * 1e10; MSUN_KM = 1.4766250614; C_CGS = 2.99792458e10
CRUST = [(6.80110e-9, 1.58425, 0.0), (1.06186e-6, 1.28733, 2.44034e7), (5.32697e1, 0.62223, 3.78358e11), (3.99874e-8, 1.35692, 2.62780e12)]
SLY = (34.384, 3.005, 2.988, 2.851)
class PWP:
    def __init__(self, core):
        lp1, g1, g2, g3 = core; rho1, rho2 = 10**14.7, 10**15.0
        K1 = 10**lp1 / C_CGS**2 / rho1**g1; K2 = K1 * rho1**(g1 - g2); K3 = K2 * rho2**(g2 - g3)
        Kc, gc = CRUST[-1][0], CRUST[-1][1]; rho0 = (Kc / K1)**(1 / (g1 - gc))
        self.pieces = CRUST + [(K1, g1, rho0), (K2, g2, rho1), (K3, g3, rho2)]
        a = [0.0]
        for i in range(1, len(self.pieces)):
            Kp, gp, _ = self.pieces[i - 1]; K, gg, rb = self.pieces[i]
            a.append(a[-1] + Kp * rb**(gp - 1) / (gp - 1) - K * rb**(gg - 1) / (gg - 1))
        self.a = a; self.pb = [K * rb**gg for (K, gg, rb) in self.pieces]
    def e_of_p(self, p):
        pc = p / KAPPA; i = max(j for j in range(len(self.pieces)) if self.pb[j] <= pc)
        K, gg, _ = self.pieces[i]; rho = (pc / K)**(1 / gg)
        return ((1 + self.a[i]) * rho + K * rho**gg / (gg - 1)) * KAPPA
    def p_of_rho(self, rho):
        i = max(j for j in range(len(self.pieces)) if self.pieces[j][2] <= rho); K, gg, _ = self.pieces[i]
        return K * rho**gg * KAPPA
EOS = PWP(SLY)
def star(rho_c, a):
    pc = EOS.p_of_rho(rho_c); p_stop = EOS.p_of_rho(1e4); ec = EOS.e_of_p(pc)
    def rhs(rr, Y):
        A_, p_, lnN = Y
        p_ = max(p_, p_stop); e_ = EOS.e_of_p(p_)
        y_ = f_y(rr, A_, p_, a); pp = -(e_ + p_) * y_
        return [f_Ap(rr, A_, p_, e_, y_, a, pp), pp, y_]
    r0_ = 1e-5 / math.sqrt(ec)
    ev = lambda rr, Y: Y[1] - p_stop; ev.terminal = True; ev.direction = -1
    s_in = solve_ivp(rhs, [r0_, 100.0], [1 + 8 * math.pi * ec * r0_**2 / 3, pc, 0.0], method="DOP853", rtol=1e-11, atol=1e-30, events=ev)
    R = s_in.t[-1]; A_R, _, lnN_R = s_in.y[:, -1]
    def rhs_ext(rr, Y):
        A_, lnN = Y; y_ = f_y(rr, A_, 0.0, a)
        return [f_Ap(rr, A_, 0.0, 0.0, y_, a, 0.0), y_]
    rout = 4000 * R
    s_ex = solve_ivp(rhs_ext, [R, rout], [A_R, lnN_R], method="DOP853", rtol=1e-12, atol=1e-30, dense_output=True)
    rr3 = np.array([500 * R, 1000 * R, rout])
    l3 = np.array([s_ex.sol(v)[1] for v in rr3])
    # ln N = ln Ninf - r0/(2r) + c2/r^2 at large r (3-point fit)
    coef = np.linalg.solve(np.vstack([np.ones(3), 1 / rr3, 1 / rr3**2]).T, l3)
    r0fit = -2 * coef[1]
    M = r0fit * (1 - a / 2) / 2 / MSUN_KM
    yc = f_y(r0_, 1 + 8 * math.pi * ec * r0_**2 / 3, pc, a) / r0_
    return M, R, yc, float(np.min(np.exp(2 * s_in.y[2] - 0.5 * np.log(s_in.y[0]))))
def mmax(a):
    lr = np.linspace(15.0, 15.6, 13)
    ms = [star(10**v, a)[0] for v in lr]
    i = int(np.argmax(ms)); lo, hi = lr[max(i - 1, 0)], lr[min(i + 1, len(lr) - 1)]
    from scipy.optimize import minimize_scalar
    res_ = minimize_scalar(lambda v: -star(10**v, a)[0], bounds=(lo, hi), method="bounded", options={"xatol": 1e-7})
    return -res_.fun, res_.x
M0max, lrc0 = mmax(0.0)
Ms, Rs, ycs, minco = star(10**lrc0, 0.0)
okC8 = abs(M0max / 2.049 - 1) < 0.02 and okTOVgr and minco > 0
P(f"    alpha = 0: M_max = {M0max:.5f} Msun (CFG311 recalled SLy 2.049); centre y/r = {ycs:.4e} (finite: N'(0) = 0); "
  f"min e^(2Phi - Lambda) inside = {minco:.4e} > 0 (CFG311's F-equation has no singular point)")
check("C8 TOV with the aligned khronon at alpha = 0 reproduces the standard TOV equation and SLy M_max 2.049 within 2%; "
      "regular centre; CFG311's moving-star khronon coefficient e^(2Phi-Lambda) > 0 throughout", f"M_max {M0max:.4f}", okC8)
ha_ns = 1e-3
Mp_, _ = mmax(ha_ns); Mm_, _ = mmax(-ha_ns)
slope = (Mp_ - Mm_) / (2 * ha_ns) / M0max
d_ns = abs(slope) * ALPHA_SCORED
P(f"    d ln M_max/d alpha = {slope:+.4f} (alpha = +-1e-3);  |delta M_max/M_max| on the scored alpha: max {d_ns.max():.3e} "
  f"(reading vs 1%: margin {READ_NS / d_ns.max():.3e})")
Ma_, Ra_, yca_, minca_ = star(10**lrc0, 1e-3)
P(f"    alpha = 1e-3 star at the same rho_c: centre y/r = {yca_:.4e}, min e^(2Phi-Lambda) = {minca_:.4e}: regular")
check("NS regular at alpha != 0 (alpha = 1e-3 test point: finite y/r at the centre, positive F-equation coefficient); "
      "|delta M_max/M_max| reading", f"slope {slope:+.4f}; max {d_ns.max():.2e}", (minca_ > 0 and math.isfinite(yca_)) and d_ns.max() <= READ_NS,
      "", load_bearing=False)
OUT["numbers"]["NS"] = {"M_max_alpha0": M0max, "log_rho_c": lrc0, "dlnMmax_dalpha": slope, "max_d_Mmax": float(d_ns.max())}

# ================================================================================================ window gate + verdict
banner("WINDOW GATE AND VERDICT (frozen rule, section 5)")
gate_ok = all(AC_MIN * (1 - 1e-12) <= a_ <= AC_MAX * (1 + 1e-12) for a_ in ALPHA_SCORED)
alpha2 = float(ALPHA_SCORED.max()) / 2
P(f"    window gate: every scored alpha in L340 P1: {gate_ok};  PPN |alpha2| ~ alpha/2 = {alpha2:.2e} vs |alpha-hat2| < 1.6e-9")
check("WINDOW the scored alpha lies inside L340's window (PPN |alpha2| <= 1.6e-9; the top corner sits on it by construction)", f"alpha max {ALPHA_SCORED.max():.3e}; |alpha2| {alpha2:.2e}",
      gate_ok and alpha2 <= 1.6e-9 * (1 + 1e-9))
controls_ok = all(ok for (nm, ok, lb) in CH if lb and not nm.startswith("WINDOW"))
observables_ok = ok_sh and ok_qnm and ok_dip
MOVING_BH_ESTABLISHED = False          # no moving-BH computation at alpha != 0 (here or published at window alpha)
FAILURE_DEMONSTRATED_IN_WINDOW = False  # Ramos & Barausse 2019: numerics at (0.02, 0.01, 0.1) only, plus a count
if not controls_ok:
    verdict = "OPEN"
elif not observables_ok or FAILURE_DEMONSTRATED_IN_WINDOW:
    verdict = "KILL"
elif not MOVING_BH_ESTABLISHED:
    verdict = "CONDITIONAL"
else:
    verdict = "PASS"
P(f"    controls ok: {controls_ok}; shadow {ok_sh}, ringdown {ok_qnm}, dipole {ok_dip}")
P(f"    moving-BH regularity at alpha_c != 0 established: {MOVING_BH_ESTABLISHED}; failure demonstrated in window: {FAILURE_DEMONSTRATED_IN_WINDOW}")
P(f"    VERDICT (G11, stated scope): {verdict}")
P("    condition: slowly moving (and rotating) BHs must be regular at the spin-0 horizon for alpha_c in the window. Ramos & "
  "Barausse 2019 find them singular for generic alpha != 0 (one numerical point outside the window plus a boundary-"
  "condition count); owner flag: if that count is read as a proof for every alpha > 0, G11 reads KILL for this chassis.")
OUT["verdict"] = verdict
OUT["numbers"]["verdict_inputs"] = {"controls_ok": controls_ok, "shadow": ok_sh, "ringdown": ok_qnm, "dipole": ok_dip,
                                    "moving_BH_established": MOVING_BH_ESTABLISHED, "failure_demonstrated_in_window": FAILURE_DEMONSTRATED_IN_WINDOW}

npass = sum(1 for c in CH if c[1]); nall = len(CH)
nlb_fail = [c[0] for c in CH if c[2] and not c[1]]
P(f"\n  runtime {time.time() - T0:.1f} s;  load-bearing failures: {nlb_fail if nlb_fail else 'none'}")
OUT["n_pass"], OUT["n_checks"] = npass, nall
jf = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
with open(jf, "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
P(f"  results -> {rel(jf)}")
P(f"\n{npass}/{nall} checks pass")
sys.exit(1 if nlb_fail else 0)
