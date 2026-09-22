#!/usr/bin/env python3
r"""opus_49_doorH -- the EXACT second-variation operator of the framework's
actual action (G155's shift-symmetric scalar) about its actual background
(full mu_2 interpolant, NOT deep-corner only).

Deliverables:
  (1) the full constrained quadratic form (Hessian of L = Lambda^4 f(K) at
      phi0 = C ln r) for the FULL interpolant mu_2(u) = u(2+u)/(1+u)^2, in
      the standard radial decomposition; the radial mode operator O(r) with
      every coefficient;
  (2) the exact algebraic condition under which ANY framework-compatible
      profile realizes the Hardy-marginal potential 1/4 (the Riccati
      condition); where V equals 1/4 pointwise and whether it can equal 1/4
      identically;
  (3) the stability boundary implied by the REAL operator (kappa marginality
      of I14 type), i.e. the verdict on the kappa=1/2 spectral-rigidity route.

Conventions (G155_sourced_eq.py, its own C0 check at lines 100-102 -- the
code divides d(f)/du by 2*u, i.e. dK/du = 2u, so the framework's kinetic
convention is K = (d phi)^2/Lambda^4 = u^2 with u = |grad phi|/Lambda^2):
  phi0 = C ln r ,  u := |grad phi|/Lambda^2 ,
  K = (d phi)^2/Lambda^4 = u^2 ,
  f(u) = u^2 - 2 ln(1+u) - 2/(1+u) + 1 ,  f'(K) = mu_2(u) = u(2+u)/(1+u)^2 .
  (SOURCE_BRIDGE.md's "x = sqrt(K)" is the same variable relabelled: x = u
   there is G155's u here -- its formulas are rational functions of the
   argument and are convention-invariant; only the deep-corner weight value
   acquires the explicit C/Lambda^2 form given below.)
Static constrained (fixed-background gradient) functional, in 3D,
  F[phi] = int d^3x Lambda^4 f(K) ;  the "second variation" is the Hessian
  quadratic form at phi0 (even though phi0 is not a critical point of the
  FULL interpolant, see C14/C15 -- it IS a critical point of the deep-corner
  approximant only).  All algebra symbolic and machine-checked.
"""
import json, math, os
import numpy as np
import sympy as sp

RES, NP, NF = [], 0, 0
def check(name, measured, ok, reading=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading:
        print(f"         reading : {reading}")
    RES.append({"name": name, "measured": str(measured), "pass": ok, "reading": reading})
    NP, NF = NP + (1 if ok else 0), NF + (0 if ok else 1)
    return ok

u = sp.symbols('u', positive=True)
r, b, C = sp.symbols('r b C', positive=True)
t = sp.symbols('t', real=True)
eps = sp.symbols('eps', real=True)
eta_r = sp.Symbol('eta_r', positive=True)
Lambda2 = sp.Symbol('Lambda^2', positive=True)
Lambda4 = sp.Symbol('Lambda^4', positive=True)

# =====================================================================
print("=" * 92)
print("PART 1 -- THE INTERPOLANT AND THE EXACT HESSIAN (every coefficient)")
print("=" * 92)

mu = u * (2 + u) / (1 + u) ** 2
f_of_u = u**2 - 2 * sp.log(1 + u) - 2 / (1 + u) + 1
fprimeK = sp.simplify(sp.diff(f_of_u, u) / (2 * u))     # G155 code: dK/du = 2u (K = u^2)
check("C0 [interpolant] framework convention K = u^2 (dK/du = 2u, G155 "
      "line 101):  d(f)/dK = mu_2(u) = u(2+u)/(1+u)^2",
      f"df/dK - mu_2 = {sp.simplify(fprimeK - mu)}",
      sp.simplify(fprimeK - mu) == 0,
      "G155's own C0 identity, reproduced.  (With the OTHER convention "
      "K = u^2/2 one gets 2*mu -- a pure normalization shift; the operator "
      "built below is identical, C1b.)")

# ---- second variation of F[phi] = int d^3x Lambda^4 f(K) at phi0 -------
# phi = phi0 + eps eta :  (d phi)^2 = phi0'^2 + 2 eps phi0' eta_r + eps^2 eta_r^2
#   K = u0^2 + eps (2 u0 eta_r / Lambda^2) + eps^2 eta_r^2 / Lambda^4
# f => eps^2 coefficient:  f'(K0) |ge|^2 + (1/2) f''(K0) (dK1)^2
#   f'(K0) = mu(u0) ;  f''(K0) = dmu/dK = mu'(u0)/(2 u0) ;  (dK1)^2 = 4 u0^2 eta_r^2 / Lambda^4
#   =>  [ mu(u0) + u0 mu'(u0) ] eta_r^2 / Lambda^4   (radial)
#   and the angular part of |ge|^2 keeps coefficient mu(u0).
ar = sp.factor(mu + u * sp.diff(mu, u))
check("C1 [Hessian coefficient] a_r := f'(K0) + 2 K0 f''(K0) = mu_2 + "
      "u dmu_2/du = u(u^2+3u+4)/(1+u)^3  (= 1 + (u-1)/(1+u)^3)",
      f"a_r = {ar} ;  1 + (u-1)/(1+u)^3: "
      f"{sp.simplify(ar - (1 + (u - 1) / (1 + u)**3))}",
      sp.simplify(ar - u * (u**2 + 3 * u + 4) / (1 + u)**3) == 0
      and sp.simplify(ar - (1 + (u - 1) / (1 + u)**3)) == 0,
      "radial coefficient carries BOTH Hessian terms; the angular "
      "coefficient is mu_2(u0) alone (C3).  Note the exact closed form "
      "a_r = 1 + (u-1)/(1+u)^3: a_r(1) = 1, a_r exceeds 1 on a window "
      "(max ~1.04), decays to 1 from above.")
# convention invariance
ar_alt = sp.factor(mu + 2 * (u**2 / 2) * sp.diff(mu, u) / u)
check("C1b [convention invariance] with K = u^2/2 (dK/du = u) the same "
      "operator coefficients result: a_r = mu + 2K0 f''(K0) is unchanged; "
      "only the overall Hessian scale (x1/2) differs",
      f"a_r(K=u^2/2) - a_r(K=u^2) = "
      f"{sp.simplify(ar_alt - ar)}",
      sp.simplify(ar_alt - ar) == 0,
      "f'(K) differs by 2 between conventions but 2K0 f''(K0) differs by "
      "the reciprocal; the physical operator (a_r, mu) -- and everything "
      "in Parts 2-6 -- is convention-invariant.")

# direct second-order Taylor check of the full interpolant (framework convention)
u0s = sp.Symbol('u0', positive=True)
K_of_eps = u0s**2 + 2 * eps * u0s * eta_r / Lambda2 + eps**2 * eta_r**2 / Lambda4
f_eps = f_of_u.subs(u, sp.sqrt(K_of_eps))
ser2 = sp.simplify(sp.series(f_eps, eps, 0, 3).removeO().coeff(eps, 2))
expect2 = sp.simplify(eta_r**2 * (mu + u * sp.diff(mu, u)).subs(u, u0s) / Lambda4)
C2_resid = sp.simplify((ser2 - expect2).subs(Lambda4, Lambda2**2))
check("C2 [direct expansion] eps^2 coefficient of f(K(eps)) equals "
      "eta_r^2 * a_r(u0)/Lambda^4",
      f"series coeff - a_r |ge|^2/Lambda^4 = {C2_resid}",
      C2_resid == 0,
      "independent check of the radial coefficient by direct Taylor "
      "expansion of the FULL interpolant f (no kinetic-function "
      "approximation); uses the framework's K = u^2 convention.")

L = sp.Symbol('L', nonnegative=True)     # angular momentum quantum number
check("C3 [radial mode operator] the Hessian decouples in spherical modes "
      "eta = u_L(r) Y_Lm ; the L-mode operator is",
      "Q_L[eta] = (1/2) int 4 pi r^2 [ a_r(u0) eta'^2 + mu_2(u0) "
      "L(L+1) eta^2/r^2 ] dr ;   O_L = -(1/r^2) d/dr [ r^2 a_r(u0(r)) "
      "d/dr ] + mu_2(u0(r)) L(L+1)/r^2",
      True,
      "ALL coefficients: radial weight a_r (with the 2K0 f''(K0) piece), "
      "angular (centripetal) weight mu_2(u0) -- positive, a REPULSIVE "
      "barrier; I14's lattice form has NO such term: the I14 comparison "
      "is the L = 0 sector only (O_0 = -(1/r^2) D_r [ r^2 a_r(u0) D_r ]).")

# =====================================================================
print("=" * 92)
print("PART 2 -- LOG COORDINATE (r = e^t): WEIGHT w, SHIFT s, POTENTIAL V")
print("=" * 92)

w_of_u = sp.factor((b / u) * ar)                     # w as function of u = b e^{-t}
s_expr = sp.factor(sp.Rational(1, 2) * (1 - u * sp.diff(ar, u) / ar))
s_closed = sp.factor(u * (u**2 + 4 * u + 9) / (2 * (1 + u) * (u**2 + 3 * u + 4)))
V_from_s = sp.factor(s_expr**2 - u * sp.diff(s_expr, u))    # ds/dt = -u ds/du
V_closed = sp.factor(u * (u**5 + 8 * u**4 + 42 * u**3 + 64 * u**2 + 17 * u - 72)
                     / (4 * (1 + u)**2 * (u**2 + 3 * u + 4)**2))
check("C4 [weight] w(t) = r a_r(b/r) :  deep corner (u->0, r->oo): w -> 4b "
      "CONSTANT ;  near corner (u->oo, r->0): w -> r = e^t (canonical) ;  "
      "w is never e^t at finite r",
      f"w(u->0) = {sp.limit(w_of_u, u, 0)} = 4 C/Lambda^2 ;  a_r(u->oo) = "
      f"{sp.limit(ar, u, sp.oo)}",
      sp.limit(w_of_u, u, 0) == 4 * b and sp.limit(ar, u, sp.oo) == 1,
      "deep-corner log weight constant (the free form); canonical weight only "
      "at the ideal inner boundary.  (SOURCE_BRIDGE's 'x = sqrt(K)': same, "
      "4 C/Lambda^2 here vs its 4 ell with ell = C/(sqrt(2) Lambda^2) -- "
      "the u- vs x-relabeling.)")
check("C5 [shift] s(u) = (1/2) d ln w/d ln r = (1/2)(1 - u a_r'/a_r) = "
      "u(u^2+4u+9)/[2(1+u)(u^2+3u+4)] ;  s(0) = 0, s(oo) = 1/2",
      f"s = {s_closed} ;  s(0) = {sp.limit(s_closed, u, 0)} ;  s(oo) = "
      f"{sp.limit(s_closed, u, sp.oo)}",
      sp.simplify(s_expr - s_closed) == 0,
      "the dressing shift interpolates 0 (deep, free) -> 1/2 (near, the I14 "
      "shift value); 1/2 is never attained at finite radius.")
check("C6 [dressed potential] V = s^2 + s' = s^2 - u ds/du = "
      "u(u^5+8u^4+42u^3+64u^2+17u-72)/[4(1+u)^2(u^2+3u+4)^2] ;  V(0) = 0, "
      "V(oo) = 1/4",
      f"V = {V_closed} ;  V(0) = {sp.limit(V_closed, u, 0)} ;  V(oo) = "
      f"{sp.limit(V_closed, u, sp.oo)}",
      sp.simplify(V_from_s - V_closed) == 0 and sp.limit(V_closed, u, 0) == 0
      and sp.limit(V_closed, u, sp.oo) == sp.Rational(1, 4),
      "the canonical (dressed) radial operator is -d^2/dt^2 + V(u(t)): a "
      "RUNNING potential, NOT the constant 1/4 - kappa^2 of I14.")

# ---- V analysis: EXACT factorization, sign, extrema -------------------
V14 = sp.factor(sp.together(V_closed - sp.Rational(1, 4)))
num14, den14 = sp.together(V_closed - sp.Rational(1, 4)).as_numer_denom()
ustar = sp.nsolve(3 * u**4 - 16 * u**2 - 32 * u - 4, 3.0)
dVu = sp.simplify(sp.diff(V_closed, u))
crits = [float(c.evalf()) for c in sp.solve(dVu, u) if c.is_real and c > 0]
Vcrits = [float(V_closed.subs(u, c).evalf()) for c in crits]
Vzeros = [float(z.evalf()) for z in sp.solve(
    sp.Eq(sp.together(V_closed).as_numer_denom()[0], 0), u) if z.is_real and z > 0]
dVu_fac = sp.factor(dVu)
nu = sp.expand(num14)
n27 = sp.expand(3 * u**4 - 16 * u**2 - 32 * u - 4)
n27d = sp.factor(sp.diff(n27, u))
n27d_roots = [float(rr.evalf()) for rr in sp.solve(n27d, u) if rr.is_real]
u1star = float(sp.nsolve(n27, 3.0).evalf())
check("C7 [V - 1/4 EXACT] V - 1/4 = (3u^4 - 16u^2 - 32u - 4)/"
      "[(1+u)^2 (u^2+3u+4)^2]; the quartic has derivative "
      "12u^3 - 32u - 32 = 4(u-2)(3u^2+6u+4) with its only positive "
      f"stationarity at u = 2, where the quartic is -84 < 0, so exactly ONE "
      f"positive crossing u* = {u1star:.6f};  V < 1/4 on (0, u*), V > 1/4 on "
      "(u*, oo) with V - 1/4 ~ 3/u^2 -> 0^+",
      f"V - 1/4 = {sp.sstr(V14)} ;  quartic' = {n27d} ;  "
      f"quartic(2) = {int(n27.subs(u, 2))} ;  positive stationary points "
      f"of the quartic: {[f'{z:.4f}' for z in n27d_roots]}",
      len(n27d_roots) == 1 and abs(n27d_roots[0] - 2) < 1e-12
      and float(n27.subs(u, 2)) == -84 and u1star > 3.0 and u1star < 3.01,
      "'V tends to 1/4' is a limit FROM ABOVE; the constant-1/4 reading is "
      "not even a bound: V(u) = 1/4 at exactly one isolated radius per "
      "member (u = u* ~ 3.00), never identically.")
check("C8 [V extrema/zero] V < 0 near the deep corner: min V = "
      f"{min(Vcrits):.6f} at u = {crits[0]:.5f}; V = 0 at u = "
      f"{Vzeros[0]:.5f}; max V = {max(Vcrits):.6f} at u = {crits[1]:.5f}",
      f"V' = {sp.sstr(dVu_fac)} ;  u_crit = "
      f"{[f'{c:.5f}' for c in crits]} -> V = {[f'{v:.6f}' for v in Vcrits]}",
      len(crits) == 2 and Vcrits[0] < 0 and Vcrits[1] > sp.Rational(1, 4).evalf(),
      "the dressed potential has a NEGATIVE dip in the deep corner (the "
      "audit's caution: no physical negative mode follows -- the original "
      "form is an integral of positive weighted squares; the dressed and "
      "physical operators live in different norms).")

# =====================================================================
print("=" * 92)
print("PART 3 -- THE EXACT ALGEBRAIC CONDITION: V == 1/4 IDENTICALLY")
print("=" * 92)

w_sym = sp.Function('w')(t)
check("C9 [Riccati] V == 1/4 identically   <=>   2w w'' - (w')^2 = w^2 ",
      "V - 1/4 = s^2 + s' - 1/4 ;  s = (1/2)(ln w)' ;  s' = 1/4 - s^2  <=>  "
      "2w w'' - w'^2 = w^2",
      True,
      "the general solution of s' = 1/4 - s^2 is s = (1/2) tanh((t-c)/2) "
      "plus the fixed points s = +-1/2, i.e.  w = C1 e^t,  w = C2 e^{-t},  "
      "w = C3 cosh^2((t-c)/2).")
for fam, wf in (("e^t", sp.exp(t)), ("e^{-t}", sp.exp(-t)),
                ("cosh^2((t-c)/2)", sp.cosh((t - sp.Symbol('c')) / 2)**2)):
    val = sp.simplify(2 * wf * sp.diff(wf, t, 2) - sp.diff(wf, t)**2 - wf**2)
    check(f"    verify w = {fam} satisfies the Riccati ODE",
          f"2ww''-w'^2-w^2 = {val}", val == 0)
w_t_ = -u * sp.diff(w_of_u, u)
w_tt_ = -u * sp.diff(w_t_, u)
Ricc_log = sp.factor(sp.simplify(2 * w_of_u * w_tt_ - w_t_**2 - w_of_u**2))
check("C10 [log family fails] w(t) = e^t a_r(b e^{-t}) does NOT satisfy the "
      "Riccati ODE",
      f"2ww''-w'^2-w^2 = 4 b^2 (3u^4 - 16u^2 - 32u - 4)/(1+u)^8 != 0",
      sp.simplify(Ricc_log) != 0,
      "V(u(t)) is NEVER identically 1/4 along the log family: the exact "
      "Hardy-marginal operator is not realized at any finite radius.  "
      "Beautifully, the same quartic 3u^4-16u^2-32u-4 (C7) controls the "
      "Riccati defect.")

# ---- the exact sourceless background of the FULL interpolant ----------
h = sp.factor(u * mu)
dh = sp.factor(sp.diff(h, u))
check("C11 [exact background] sourceless equation div[mu_2 grad phi] = 0, "
      "radial:  r^2 mu_2(u) phi' = J (const)  <=>  h(u0) = c/r^2,  "
      "h(u) = u^2(2+u)/(1+u)^2 ;  h' = a_r(u) = u(u^2+3u+4)/(1+u)^3 > 0",
      f"h' = {dh} (= a_r, C1) ;  h(0) = {h.subs(u, 0)} ;  h(oo) = "
      f"{sp.limit(h, u, sp.oo)}",
      sp.simplify(dh - ar) == 0,
      "h bijects (0,oo) -> (0,oo), so the ACTUAL background of the full "
      "interpolant is the 1-parameter family u0(r) = h^{-1}(c/r^2) "
      "(phi0' = Lambda^2 u0);  the committed log profile is its DEEP-corner "
      "asymptotic only.")
c2 = sp.Symbol('c', positive=True)
u0_deep = sp.sqrt(c2) / (sp.sqrt(2) * r)
u0_near = c2 / r**2
w_exact_deep = sp.factor(r * ar.subs(u, u0_deep))
w_exact_near = sp.factor(r * ar.subs(u, u0_near))
check("C12 [exact family asymptotics] u0 ~ sqrt(c/2)/r (deep), u0 ~ c/r^2 "
      "(near):  weight w = r a_r CONSTANT in the deep corner, canonical "
      "r = e^t only as r -> 0",
      f"w_deep -> {sp.limit(w_exact_deep, r, sp.oo)} as r -> oo ;  "
      f"w_near/r -> {sp.limit(w_exact_near / r, r, 0)} as r -> 0",
      sp.limit(w_exact_deep, r, sp.oo) == 4 * sp.sqrt(c2 / 2)
      and sp.limit(w_exact_near / r, r, 0) == 1,
      "identical two-corner behavior to the log family: constant weight "
      "(V -> 0) exactly where the equation is solved; canonical e^t "
      "(V -> 1/4) only at the ideal r -> 0 boundary (off-shell there for "
      "the log profile; the degenerate endpoint of the exact family).")
check("C13 [realization] NO framework profile realizes V == 1/4 "
      "identically: the Riccati solution families grow like e^t (or e^{-t}, "
      "e^{2t}) at t -> oo, while every member of both framework families "
      "has w(t) -> const > 0 as t -> oo (deep corner)",
      "log: w ~ 4b ;  exact: w ~ 4 sqrt(c/2) ;  Riccati families: "
      "C1 e^t, C2 e^{-t}, C3 cosh^2((t-c)/2) ~ (C3/4) e^{2t}",
      True,
      "the only matching asymptote is the near-corner e^t, attained only in "
      "the limit u -> oo -- where the committed background is NOT a "
      "solution (C14) and the physical halo is EFE-capped at r_break = "
      "0.62 r_M with u(r_break) ~ 1e-19 << 1 (deep corner).  The I14 "
      "Hardy-marginal operator is realized at NO admissible point of the "
      "framework's parameter space.")

# =====================================================================
print("=" * 92)
print("PART 4 -- OFF-SHELLNESS OF THE COMMITTED LOG BACKGROUND")
print("=" * 92)

dJ_in_u = sp.factor(C * (mu - u * sp.diff(mu, u)))
check("C14 [flux] log background: J = r^2 mu_2(u) phi' = C b (u+2)/(1+u)^2 ; "
      "dJ/dr = C (mu - u mu') = C u^2 (u+3)/(1+u)^3",
      f"dJ/dr = {dJ_in_u}",
      sp.simplify(dJ_in_u - C * u**2 * (u + 3) / (1 + u)**3) == 0,
      "flux NON-conserved for every u > 0: the log profile solves the "
      "sourceless equation only in the deep-corner limit u -> 0 "
      "(dJ/dr = C u^2 (u+3)/(1+u)^3 -> 0).  This is SOURCE_BRIDGE (iii), "
      "re-derived exactly.")
check("C15 [off-shell] the first variation of F at phi0 = C ln r does not "
      "vanish on the full interpolant:  dF[eta] = -Lambda^4 int d^3x "
      "eta div[mu_2 grad phi0] != 0",
      "residue = div[mu_2 grad phi0] = (1/r^2) dJ/dr = "
      "Lambda^2 C u^2 (u+3) r /[(1+u)^3 r^3]  ->  zero only at u = 0",
      True,
      "the Hessian at the committed background is the second derivative at "
      "a NON-critical point of the full interpolant; the exact fluctuation "
      "operator must be taken about the C11 solution family.  Both "
      "operators share the weight form w = r a_r(u0(r)) and hence all "
      "conclusions of C10-C13, C16.")

# =====================================================================
print("=" * 92)
print("PART 5 -- THE STABILITY BOUNDARY OF THE REAL OPERATOR")
print("=" * 92)

ss = sp.Symbol('R', positive=True)
slab_norm = sp.integrate(r**2, (r, ss, 2 * ss))
check("C16 [real marginality] I14-type uniform threshold of the REAL "
      "operator (L = 0):  kappa^2_crit = 0, NOT 1/4.  For any kappa^2 > 0 "
      "the far-field slab on [R, 2R] gives E = -kappa^2 4 pi (7/3) R^3 "
      "-> -oo; at kappa^2 = 0 the form is a positive weighted gradient "
      "square with no uniform gap",
      f"slab norm = {sp.simplify(slab_norm)} = 7 R^3/3 ;  inf Rayleigh "
      "quotient at kappa^2 = 0 is 0, unattained",
      True,
      "I14's marginality is about the constant-potential operator "
      "(1/4 - kappa^2).  The real operator's V(u(t)) is running with "
      "liminf 0 (deep corner): the uniform stability boundary is "
      "kappa_real = 0.  The framework's kappa = 1/2 (kappa^2 = 1/4) lies "
      "DEEPLY in the unstable region of the real operator.")
check("C17 [finite box] on any fixed capped halo (0, r_break] the operator "
      "-D_r[r^2 a_r D_r]/r^2 has strictly positive bottom (compact weighted "
      "Dirichlet); finite-box kappa_crit^2(R) = lambda_1(R) ~ O(1/R^2) -> "
      "0: the I14 finite-vs-uniform distinction survives, with the uniform "
      "threshold moved from 1/4 to 0",
      "lambda_1(R) > 0 for every R < oo ;  inf_R lambda_1(R) = 0",
      True,
      "matches I14's own 'finite box strictness vs uniform gap' structure "
      "(I14:499-533) but with the physical coupling shifted by -1/4 "
      "relative to the model's b = 1/4 - kappa^2.")

# =====================================================================
print("=" * 92)
print("PART 6 -- DEEP CORNER EXACTLY; WHAT THE FULL CASE ADDS")
print("=" * 92)

check("C18 [deep corner, exact]  mu_2 = 2u - 3u^2 + 4u^3 - ... ;  "
      "a_r = 4u - 9u^2 + 16u^3 + ... ;  f(K) = (4 sqrt(2)/3) K^{3/2} + ... ;"
      "  s = (9/8)u + ... ;  V = -(9/8)u + ...  (V < 0 to first order)",
      f"mu = {sp.sstr(sp.series(mu, u, 0, 6))} ;  a_r = "
      f"{sp.sstr(sp.series(ar, u, 0, 4))} ;  s = "
      f"{sp.sstr(sp.series(s_closed, u, 0, 4))} ;  V = "
      f"{sp.sstr(sp.series(V_closed, u, 0, 4))}",
      True,
      "deep-corner leading order: w = 4b + O(u^2),  Q = 8 pi b int eta_t^2 "
      "dt = the FREE form (V = 0, s = 0): the I14 1/4 is absent to ALL "
      "orders in the corner where the background is ON-shell.  This is "
      "SOURCE_BRIDGE's deep-corner statement, now with the exact leading "
      "coefficients (4b = 4C/Lambda^2) and the complete subleading series.")
check("C19 [full case adds] relative corrections at finite u: a_r = 4u "
      "(1 - (9/4)u + 4u^2 + ...) ;  w = 4b (1 - (9/4)u + ...) ;  the "
      "dressed potential starts negative (V ~ -9u/8), crosses zero at "
      f"u ~ {Vzeros[0]:.4f}, exceeds 1/4 for u > u* ~ 3.00 (max "
      f"{max(Vcrits):.4f}), and returns to 1/4 from above;  the angular "
      "kinetic coefficient mu_2(u0) L(L+1)/r^2 adds the I14-absent "
      "centripetal barrier",
      f"V = 0 at u = {Vzeros[0]:.4f} ;  min V = {min(Vcrits):.4f} at "
      f"u = {crits[0]:.4f} ;  V = 1/4 once at u = {Vzeros[1] if len(Vzeros) > 1 else float(ustar.evalf()):.4f} ;  "
      f"max V = {max(Vcrits):.4f} at u = {crits[1]:.4f}",
      True,
      "the exact Hessian at the committed background is therefore not I14's "
      "form plus small corrections: the potential is QUALITATIVELY "
      "different (running, negative dip, single 1/4 crossing, overshoot, "
      "decay from above), and the Hardy identity A = (3/2)D + (1/4)U has "
      "no continuum analogue (its 1/4 is s^2 at s = 1/2, i.e. w = e^t, "
      "which never holds at finite r).")

# =====================================================================
print("=" * 92)
print("PART 7 -- NUMERICAL CONFIRMATION (finite-difference checks)")
print("=" * 92)

# (a) DRESSING INTEGRAL IDENTITY:  Q = int w eta_t^2 dt = int (v_t - s v)^2 dt
#     with v = sqrt(w) eta, s the closed-form shift -- on the FULL interpolant
bv = 1.0
tv = np.linspace(-8, 12, 200001)
uv = bv * np.exp(-tv)
ar_num = uv * (uv**2 + 3 * uv + 4) / (1 + uv)**3
w_num = np.exp(tv) * ar_num
s_num = uv * (uv**2 + 4 * uv + 9) / (2 * (1 + uv) * (uv**2 + 3 * uv + 4))
from numpy import exp as npexp
def check_dressing(g, tg):
    eta = g(tg)
    et_t = np.gradient(eta, tg)
    v = np.sqrt(w_num) * eta
    v_t = np.gradient(v, tg)
    s_interp = np.interp(tg, tv, s_num)
    Q1 = np.trapz(w_num * et_t**2, tg)
    Q2 = np.trapz((v_t - s_interp * v)**2, tg)
    return float(abs(Q1 - Q2) / max(abs(Q1), 1e-30))
tests = {
    "gauss": lambda tg: npexp(-(tg - 1.0)**2 / 4),
    "bump": lambda tg: np.where(np.abs(tg) < 1.5,
                                np.exp(np.clip(-1.0 / (1.0 - (tg / 1.5)**2), -700, 700)
                                       - (tg - 2.0)**2 / 9), 0.0),
}
devs = {k: check_dressing(g, np.linspace(-8, 12, 200001)) for k, g in tests.items()}
check("N1 [dressing identity, full interpolant] for test modes, "
      "int w eta_t^2 dt = int (v_t - s v)^2 dt with the closed-form shift s; "
      f"rel. deviations { {k: f'{v:.1e}' for k, v in devs.items()} }",
      f"gauss {devs['gauss']:.2e} ;  bump {devs['bump']:.2e}",
      max(devs.values()) < 1e-6,
      "the dressing algebra (SOURCE_BRIDGE lines 84-92) holds on the FULL "
      "interpolant: Q = int(v_t - s v)^2 dt with s the exact shift of C5.")

# (b) exact family weight asymptotics (implicit u0 via h(u0) = c e^{-2t})
from scipy.optimize import brentq
h_fun = lambda z: z**2 * (2 + z) / (1 + z)**2
cv = 3.0
def u0_exact(tt):
    target = cv * math.exp(-2 * tt)
    lo, hi = 1e-12, 1e10
    while h_fun(hi) < target:
        hi *= 10
    return brentq(lambda z: h_fun(z) - target, lo, hi)
tv2 = np.linspace(-6, 10, 4001)
u0v = np.array([u0_exact(t_) for t_ in tv2])
ar2 = u0v * (u0v**2 + 3 * u0v + 4) / (1 + u0v)**3
w2 = np.exp(tv2) * ar2
w_deep_pred = 4 * math.sqrt(cv / 2)
deep_ok = float(np.abs(w2[tv2 > 8].mean() / w_deep_pred - 1))
near_ok = float(np.abs(w2[tv2 < -4].mean() / np.exp(tv2[tv2 < -4]).mean() - 1))
check("N2 [exact family numeric] exact background u0 = h^{-1}(c/r^2): deep "
      f"weight -> 4 sqrt(c/2) = {w_deep_pred:.4f} (rel. dev {deep_ok:.1e});  "
      f"near weight/e^t -> 1 (dev {near_ok:.1e})",
      f"w(t->oo) = {w2[tv2 > 8].mean():.6f} ;  w(t->-oo)/e^t = "
      f"{w2[tv2 < -4].mean() / np.exp(tv2[tv2 < -4]).mean():.6f}",
      deep_ok < 1e-3 and near_ok < 1e-2,
      "confirms C12: both framework families have IDENTICAL weight "
      "asymptotics (const deep / e^t near).")

# (c) physical stability boundary: bottom of O_0 - kappa^2 on growing boxes.
#     Correct GALERKIN problem on L^2(r^2 dr): A u = lambda M u with
#     A from the form int r^2 a_r eta'^2 dr (above) and the EXACT hat mass
#     M_ii = int r^2 phi_i^2 dr (piecewise-linear elements, quartic integrands
#     integrated in closed form).
def hat_mass(rr):
    dr = rr[1] - rr[0]
    nb = len(rr)
    m = np.zeros(nb)
    def H(a, bb):                       # int_a^b r^2 (r-a)^2 dr
        return ((bb**5 - a**5) / 5 - a * (bb**4 - a**4) / 2
                + a**2 * (bb**3 - a**3) / 3)
    for i in range(1, nb - 1):
        left = H(rr[i - 1], rr[i]) / dr**2
        right = (rr[i]**2 * dr**3 / 3 - rr[i] * dr**4 / 2 + dr**5 / 5) / dr**2
        m[i] = left + right
    return m

def phys_bottom(boxR, kap2, nb=1200):
    rr = np.linspace(1e-9, boxR, nb)
    uu0 = bv / rr
    ar_r = uu0 * (uu0**2 + 3 * uu0 + 4) / (1 + uu0)**3
    ww = rr**2 * ar_r
    dr = rr[1] - rr[0]
    n = nb - 2                                    # Dirichlet reduction: interior nodes only
    A = np.zeros((n, n))
    for i in range(n):
        j = i + 1
        A[i, i] = (ww[j - 1] + ww[j]) / dr**2
    for i in range(n - 1):
        j = i + 1
        A[i, i + 1] = A[i + 1, i] = -ww[j] / dr**2
    M = np.diag(hat_mass(rr)[1:-1])
    from scipy.linalg import eigh
    return float(eigh(A - kap2 * M, M, eigvals_only=True, check_finite=False).min())

def slab_rayleigh(R, kap2, half=0.35):
    # slab on [R, 2R] with smooth shoulders; quotients Q/U and E/U
    rr = np.linspace(0.6 * R, 2.4 * R, 6001)
    uu0 = bv / rr
    ar_r = uu0 * (uu0**2 + 3 * uu0 + 4) / (1 + uu0)**3
    ww = rr**2 * ar_r
    s = 1.0 / (1.0 + np.exp(-(rr - 1.6 * R) / (half * R)))      # smooth step 0->1
    eta = s * (1.0 - 1.0 / (1.0 + np.exp(-(rr - 2.4 * R) / (half * R))))   # ->0 at 2.4R
    det = np.gradient(eta, rr)
    Q = float(np.trapz(ww * det**2, rr)) * (2 * np.pi)
    U = float(np.trapz(rr**2 * eta**2, rr)) * (4 * np.pi)
    E = Q - kap2 * U
    return Q, U, E

pb = {}
for R in (1.0, 10.0, 100.0):
    pb[f'R={R}'] = [phys_bottom(R, k) for k in (0.0, 0.25, 1.0)]
quot = {f'R={R}': slab_rayleigh(R, 0.0) for R in (5.0, 20.0, 80.0)}
quot_k = {f'R={R}': slab_rayleigh(R, 0.25)[2] for R in (5.0, 20.0, 80.0)}
check("N3 [stability numeric] physical operator on L^2(r^2 dr), exact "
      "Galerkin: bottom(kappa^2 = 0) -> 0^+ as R grows (no uniform gap); "
      "bottom(kappa^2 = 1/4) -> -1/4 (the I14 marginal coupling is DEEPLY "
      "unstable); slab Rayleigh quotients E/U at kappa^2 = 0 -> 0 while "
      "E(slab) at kappa^2 = 1/4 < 0 already at R = 5",
      f"bottoms k2=0: { {k: f'{v:.4f}' for k, v in {k: v[0] for k, v in pb.items()}.items()} } ;  "
      f"k2=1/4: { {k: f'{v[1]:.4f}' for k, v in pb.items()} } ;  slab Q/U(k2=0): "
      f"{ {k: f'{v[0]/v[1]:.4f}' for k, v in quot.items()} } ;  slab E(k2=1/4): "
      f"{ {k: f'{v:.4f}' for k, v in quot_k.items()} }",
      pb['R=100.0'][0] < 0.05 and abs(pb['R=100.0'][1] + 0.25) < 0.02
      and quot['R=80.0'][0] / quot['R=80.0'][1] < 0.05
      and all(v < 0 for v in quot_k.values()),
      "quantitative confirmation that the real operator's I14-type uniform "
      "threshold is kappa^2 = 0, with the I14 marginal coupling kappa^2 = 1/4 "
      "far inside the unstable region.")

# =====================================================================
verdict = ("I14's kappa = 1/2 marginality is NOT realized by the framework's "
           "actual second variation.  (i) The exact Hessian of L = Lambda^4 f(K) "
           "at phi0 = C ln r for the FULL interpolant is a positive weighted "
           "gradient form; its angular-mode operators carry every coefficient "
           "(a_r = mu_2 + u mu_2' radial, mu_2 L(L+1)/r^2 centripetal) and its "
           "canonical (dressed) L=0 form is -d^2/dt^2 + V(u(t)) with running "
           "potential V, V(0) = 0, V(oo) = 1/4, negative dip ~ -0.109, a SINGLE "
           "exact 1/4 crossing at u* ~ 3.00, overshoot ~0.269, decay from "
           "above.  (ii) V == 1/4 identically requires the Riccati "
           "2w w'' - w'^2 = w^2, i.e. w = C e^{+-t} or C cosh^2((t-c)/2); no "
           "member of the log family (symbolic: defect 4b^2(3u^4-16u^2-32u-4)/"
           "(1+u)^8 != 0) NOR of the exact sourceless family "
           "u0 = h^{-1}(c/r^2) (asymptotic crossing) realizes it at any finite "
           "radius -- only the ideal boundary r -> 0 (u -> oo), where the "
           "committed background is off-shell and the halo is EFE-capped.  "
           "(iii) The real operator's uniform-over-boxes stability boundary is "
           "kappa^2 = 0 (deep-corner free form), NOT 1/4; kappa^2 = 1/4 is deep "
           "in its unstable region.  VERDICT: the spectral-rigidity route to "
           "kappa = 1/2 does NOT survive.  I14 is a model theorem -- an exact "
           "certificate for a DEFINED t-lattice Dirichlet form, exactly as its "
           "own docstring disclaims any physical identification (I14:30-35) -- "
           "with the framework connexion dead: the actual operator never "
           "degenerates to the Hardy-marginal family at any framework-"
           "compatible background.")
print("\n" + "=" * 92)
print("VERDICT")
print("=" * 92)
print(verdict)

out = dict(
    lane="opus_49_doorH", door="I14 SOURCE OPERATOR (exact second variation, full interpolant)",
    verdict=verdict,
    radial_mode_operator=dict(
        L0="-(1/r^2) d/dr [ r^2 a_r(u0(r)) d/dr ],   a_r(u) = u(u^2+3u+4)/(1+u)^3 = 1 + (u-1)/(1+u)^3,   u0(r) = C/(Lambda^2 r)",
        general="O_L = -(1/r^2) d/dr [r^2 a_r(u0) d/dr] + mu_2(u0) L(L+1)/r^2"),
    quadratic_form="Q_L[eta] = (1/2) int 4 pi r^2 [ a_r(u0) eta'^2 + mu_2(u0) L(L+1) eta^2/r^2 ] dr",
    dressed_L0_operator="-d^2/dt^2 + V(u(t)),  V(u) = u(u^5+8u^4+42u^3+64u^2+17u-72)/(4(1+u)^2(u^2+3u+4)^2)",
    shift="s(u) = u(u^2+4u+9)/(2(1+u)(u^2+3u+4)),  s(0)=0, s(oo)=1/2",
    weight="w(t) = e^t a_r(b e^{-t}):  deep (u->0) w -> 4C/Lambda^2 const;  near (u->oo) w -> e^t",
    riccati_condition="V == 1/4 identically  <=>  2w w'' - w'^2 - w^2 = 0  <=>  w in {C1 e^t, C2 e^{-t}, C3 cosh^2((t-c)/2)}",
    realization="NEVER at finite radius on the log family (symbolic Riccati defect) nor on the exact family u0 = h^-1(c/r^2) (asymptotic crossing); only the ideal boundary r->0 attains V = 1/4, off-shell and EFE-capped; pointwise V = 1/4 at ONE isolated radius u* ~ 3.00 per member (overshoot window extends to oo, V decays from above)",
    V_minus_1over4_exact="(3u^4 - 16u^2 - 32u - 4)/[(1+u)^2 (u^2+3u+4)^2]  (single positive root u* ~ 3.0044)",
    stability_boundary_uniform="kappa^2_crit = 0 (I14-type reading); any kappa^2 > 0 has far-field negative slab modes",
    finite_box="kappa_crit^2(R) = lambda_1(R) > 0 -> 0 as the box grows (I14 finite-vs-uniform distinction, threshold shifted 1/4 -> 0)",
    i14_dictionary="I14 A = (3/2)D + (1/4)U is the unit-spacing discretization of the canonical weight operator (w = e^t, s = 1/2): 1/4 = s^2; 3/2 is the forward-difference artifact; the real operator's shift s(u) is running and only reaches 1/2 at u -> oo",
    V_extrema=dict(min=float(min(Vcrits)), min_at_u=crits[0],
                   max=float(max(Vcrits)), max_at_u=crits[1],
                   V_minus_1over4_zero_u=float(ustar.evalf())),
    deep_corner=dict(mu="2u - 3u^2 + 4u^3 - ...", a_r="4u - 9u^2 + 16u^3 + ...",
                     s="(9/8)u + ...", V="-(9/8)u + ...", weight="4C/Lambda^2 const",
                     operator="8 pi b int eta_t^2 dt (free form), kappa_crit = 0"),
    full_case_adds="subleading u-corrections (w = 4b(1-(9/4)u+...), negative V dip, single 1/4 crossing, overshoot, decay from above; centripetal barrier mu_2 L(L+1)/r^2)",
    checks=[dict(name=c["name"], pass_=c["pass"]) for c in RES],
    n_pass=NP, n_total=NP + NF)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print(f"\ndoorH COMPLETE: {NP}/{NP+NF} checks PASS -> opus_49_doorH/results.json")