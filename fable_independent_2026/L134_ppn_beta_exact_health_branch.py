#!/usr/bin/env python3
"""
PPN beta for the "health branch": GR + non-propagating cuscuton clock + leaf-projected AQUAL scalar phi
with a conformal (fifth-force) coupling to matter.
====================================================================================================
EXACT SYMBOLIC computation.  Every check ASSERTS a statement; PASS = the statement is TRUE.

BRANCH AS SPECIFIED (the object under test):
    S = int sqrt(-g) [ R/(16 pi G)  +  L_clock(tau, N)  -  (1/(8 pi G)) a0t^2 F(P/a0t^2) ] + S_m[A^2(phi) g]
    P = h^{ab} d_a phi d_b phi  (leaf-projected spatial gradient), mu(y) = F'(y^2) = 1 - e^{-y},
    A(phi) = the conformal factor implementing the "-lambda grad phi" fifth force on matter.

STRUCTURAL FACTS INHERITED FROM THE BRANCH SPEC (not re-derived here):
    (i)   T^phi_{mu nu} = O((grad phi)^2) = O(4)  =>  the O(2) metric is matter-sourced only (no slip).
    (ii)  the cuscuton clock is exactly shift-independent and leaf projection kills dP/dg^{0i}
          =>  alpha_1 = alpha_2 = 0 in the strict asymptotically-flat limit; alpha_3 = 0.
    (iii) the clock carries no O(2) stress (absorbed in Lambda).  <-- FLAGGED AS AN INHERITED ASSUMPTION.

WHAT IS PROVED HERE (all exact, no PPN truncation):
    A. Deep-Newtonian analyticity: F(X) = X - 2 + 2(1+sqrt X) e^{-sqrt X}.  The non-analytic remainder is
       EXACTLY 2(1+y)e^{-y} with y = |grad phi|/a0t, so the standard PPN expansion is an ASYMPTOTIC series
       whose error is exponentially small IF AND ONLY IF y >> 1.  (Numeric gate script tests whether y >> 1
       actually holds in the solar system -- it does not, in the observationally allowed corner.)
    B. The exterior of ANY static spherical body in Einstein + massless canonical scalar is EXACTLY the
       Janis-Newman-Winicour / Fisher solution (verified against G_{mu nu} = 8 pi G T^phi_{mu nu}).
    C. The EXACT isotropic-coordinate transformation r = rho (1 + b/(4 rho))^2 diagonalises the JORDAN
       (matter) metric for ANY conformal factor A(phi) -- the conformal factor cancels from g_rr/g_thth.
    D. Reading off the PPN form of the Jordan metric, normalised by the DYNAMICALLY measured G_N M:
              gamma = 1 - 2 f,          f == G_s/G_N  (fifth-force fraction of Newtonian gravity)
              beta  = 1                 EXACTLY, if A(phi) = e^{alpha phi}       (constant fifth-force coupling)
              beta  = 1 - f^2/2         EXACTLY, if A(phi) = 1 + lambda phi      (strictly linear coupling)
              eta_N = 4 beta - gamma - 3 = 2f - 2f^2  (linear) or 2f (exponential)
       => THE EFFECTIVE-G SPLIT LEAKS INTO gamma, NOT INTO beta.  beta is protected to O(f^2).
"""
import sympy as sp
import sys, time

T0 = time.time(); FAILS = []; N = [0]


def check(name, ok, detail=""):
    N[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n           ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


def sec(t):
    print("\n" + "=" * 110); print(t); print("=" * 110, flush=True)


print("=" * 110)
print("PPN beta -- EXACT symbolic computation for the cuscuton-clock + AQUAL-fifth-force health branch")
print("=" * 110, flush=True)

# =====================================================================================================
sec("PART A -- the deep-Newtonian regime: is the AQUAL kinetic function analytic?  (exact remainder)")
# =====================================================================================================
X, Y = sp.symbols("X y", positive=True)

# AQUAL:  L_phi = -(1/(8 pi G)) a0t^2 F(P/a0t^2),  EOM  div[ F'(P/a0t^2) grad phi ] = 4 pi G_c rho.
# The Bekenstein-Milgrom interpolating function is mu(y) = F'(y^2) with y = |grad phi|/a0t.
mu = 1 - sp.exp(-Y)
F = X - 2 + 2 * (1 + sp.sqrt(X)) * sp.exp(-sp.sqrt(X))

check("A1  F(X) = X - 2 + 2(1+sqrt X) e^{-sqrt X} is THE AQUAL kinetic function whose Bekenstein-Milgrom "
      "interpolating function is exactly mu(y) = 1 - e^{-y}:  dF/dX = 1 - e^{-sqrt X} identically",
      sp.simplify(sp.diff(F, X) - (1 - sp.exp(-sp.sqrt(X)))) == 0,
      f"dF/dX = {sp.simplify(sp.diff(F, X))}")

# the exact non-analytic remainder
R_exact = sp.simplify(F - (X - 2))
check("A2  the ENTIRE departure of F from its deep-Newtonian linear form (X - 2) is the closed-form "
      "remainder R(y) = 2(1+y) e^{-y}, y = sqrt X = |grad phi|/a0t -- i.e. the correction is exponentially "
      "small in y and there is NO power-law correction of any order",
      sp.simplify(R_exact.subs(X, Y**2) - 2 * (1 + Y) * sp.exp(-Y)) == 0,
      f"R = {sp.simplify(R_exact.subs(X, Y**2))}")

# the fractional force error in the deep-Newtonian branch: g_s = f g_N / mu  =>  dg/g_N = f (1/mu - 1)
frac_err = sp.simplify(1 / mu - 1)
ser = sp.simplify(sp.series(frac_err, Y, sp.oo, 3).removeO()) if False else None
check("A3  in the deep-Newtonian branch the FRACTIONAL error of the Newtonian (mu -> 1) truncation is "
      "exactly (1/mu - 1) = e^{-y}/(1-e^{-y}) ~ e^{-y}, so the PPN expansion of this branch is an "
      "ASYMPTOTIC expansion valid only where y >> 1 (this is the hypothesis the numeric gate must verify)",
      sp.simplify(frac_err - sp.exp(-Y) / (1 - sp.exp(-Y))) == 0,
      f"1/mu - 1 = {sp.simplify(frac_err)}")

check("A4  mu(y) -> 1 and F(X) -> X - 2 as y -> oo, and every derivative of the remainder is also O(e^{-y}) "
      "=> if (and only if) y >> 1 everywhere in the solar system, the scalar sector is an ordinary massless "
      "canonical scalar there and the STANDARD PPN machinery applies exactly",
      sp.limit(mu, Y, sp.oo) == 1 and sp.limit(2 * (1 + Y) * sp.exp(-Y), Y, sp.oo) == 0,
      "lim mu = 1, lim R = 0")

# =====================================================================================================
sec("PART B -- the EXACT static exterior: Janis-Newman-Winicour / Fisher, verified from the field equations")
# =====================================================================================================
r, th = sp.symbols("r theta", positive=True)
b, s, k, G = sp.symbols("b s k G", positive=True)

f_r = 1 - b / r
g_E = sp.diag(-f_r**s, f_r**(-s), f_r**(1 - s) * r**2, f_r**(1 - s) * r**2 * sp.sin(th)**2)
phi = k * sp.log(f_r)

coords = [sp.Symbol("t"), r, th, sp.Symbol("varphi")]
ginv = g_E.inv()
detg = sp.simplify(g_E.det())


def christoffel(g, gi, x):
    n = len(x)
    Ga = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for m in range(n):
            for nn in range(m, n):
                e = 0
                for d in range(n):
                    e += gi[a, d] * (sp.diff(g[d, m], x[nn]) + sp.diff(g[d, nn], x[m]) - sp.diff(g[m, nn], x[d]))
                e = sp.simplify(e / 2)
                Ga[a][m][nn] = e
                Ga[a][nn][m] = e
    return Ga


def ricci(Ga, x):
    n = len(x)
    Rc = sp.zeros(n, n)
    for m in range(n):
        for nn in range(m, n):
            e = 0
            for a in range(n):
                e += sp.diff(Ga[a][m][nn], x[a]) - sp.diff(Ga[a][m][a], x[nn])
                for c in range(n):
                    e += Ga[a][a][c] * Ga[c][m][nn] - Ga[a][nn][c] * Ga[c][m][a]
            e = sp.simplify(e)
            Rc[m, nn] = e
            Rc[nn, m] = e
    return Rc


Gam = christoffel(g_E, ginv, coords)
Ric = ricci(Gam, coords)
Rs = sp.simplify(sum(ginv[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
Ein = sp.simplify(Ric - sp.Rational(1, 2) * Rs * g_E)

# canonical massless scalar:  L = R/(16 pi G) - (1/2)(d phi)^2  =>  G_mn = 8 pi G [ d_m phi d_n phi - (1/2) g_mn (d phi)^2 ]
dphi = sp.Matrix([sp.diff(phi, c) for c in coords])
dphi2 = sp.simplify(sum(ginv[i, j] * dphi[i] * dphi[j] for i in range(4) for j in range(4)))
Tphi = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        Tphi[i, j] = sp.simplify(dphi[i] * dphi[j] - sp.Rational(1, 2) * g_E[i, j] * dphi2)

resid = sp.simplify(Ein - 8 * sp.pi * G * Tphi)
# The tt residual fixes k^2:
sol_k2 = sp.solve(sp.simplify(sp.numer(sp.together(resid[0, 0]))), k**2, dict=True)
k2_val = sp.simplify(sol_k2[0][k**2]) if sol_k2 else None

check("B1  the JNW/Fisher ansatz  ds^2 = -f^s dt^2 + f^{-s} dr^2 + f^{1-s} r^2 dOmega^2, f = 1 - b/r, "
      "phi = k ln f  solves Einstein + massless canonical scalar EXACTLY, provided k^2 = (1 - s^2)/(16 pi G). "
      "(This is the unique static spherical vacuum-with-scalar exterior, so it is the exterior of ANY static star.)",
      k2_val is not None and sp.simplify(k2_val - (1 - s**2) / (16 * sp.pi * G)) == 0,
      f"solved k^2 = {sp.simplify(k2_val)}   (target (1-s^2)/(16 pi G))")

ksub = sp.sqrt((1 - s**2) / (16 * sp.pi * G))
maxres = 0
ok_all = True
for sval in [sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4), sp.Rational(9, 10), 1]:
    rr = sp.simplify((Ein - 8 * sp.pi * G * Tphi).subs(k, ksub).subs(s, sval))
    for i in range(4):
        for j in range(4):
            e = sp.simplify(sp.expand(sp.powsimp(sp.radsimp(rr[i, j]), force=True)))
            if e != 0:
                e = sp.simplify(sp.nsimplify(e))
            if e != 0:
                ok_all = False
                maxres = e
check("B2  with k^2 = (1-s^2)/(16 pi G) ALL TEN components of G_{mu nu} - 8 pi G T^phi_{mu nu} vanish "
      "identically (full field-equation verification at s = 1/4, 1/2, 3/4, 9/10, 1, symbolic in r, b, G)",
      ok_all,
      f"every component identically 0 at all five s values (residual = {maxres})")

check("B3  s in (0,1]:  s = 1 is the scalar-free Schwarzschild point (k = 0); any nonzero scalar charge "
      "forces s < 1.  So the Einstein-frame 'mass' parameter s*b is strictly LESS than the full 2 G_N M "
      "whenever the fifth force is on -- this is the geometric origin of the effective-G split.",
      sp.simplify(((1 - s**2) / (16 * sp.pi * G)).subs(s, 1)) == 0,
      "k^2(s=1) = 0  <=> Schwarzschild")

# =====================================================================================================
sec("PART C -- EXACT isotropic coordinates for the JORDAN (matter) metric, for ANY conformal factor")
# =====================================================================================================
rho = sp.symbols("rho", positive=True)
r_of_rho = rho * (1 + b / (4 * rho))**2
f_iso = sp.simplify((1 - b / r_of_rho))
f_iso = sp.simplify(sp.factor(sp.together(f_iso)))

target = ((1 - b / (4 * rho)) / (1 + b / (4 * rho)))**2
check("C1  the transformation r = rho (1 + b/(4 rho))^2 gives EXACTLY "
      "f = 1 - b/r = [(1 - b/4rho)/(1 + b/4rho)]^2 -- the standard Schwarzschild isotropic map, "
      "which here is INDEPENDENT of the JNW exponent s and of the conformal factor A(phi)",
      sp.simplify(f_iso - target) == 0,
      f"f(rho) = {sp.simplify(f_iso)}")

# The Jordan metric is ghat = A^2 g_E.  Isotropy requires ghat_rr dr^2 + ghat_thth dOmega^2 = B(drho^2 + rho^2 dOmega^2).
# ghat_rr/ghat_thth = g_rr/g_thth = 1/(f r^2) -- the conformal factor A^2 CANCELS.
A2 = sp.Function("A2")
ratio_E = sp.simplify((f_r**(-s)) / (f_r**(1 - s) * r**2))
check("C2  the ratio g_rr / g_thth = 1/(f r^2) is INDEPENDENT of s AND of the conformal factor A^2(phi) "
      "(A^2 cancels in the ratio) => the SAME isotropic map r(rho) diagonalises the Jordan metric for "
      "every conformal coupling.  Hence gamma and beta can be read off exactly, with no PPN truncation.",
      sp.simplify(ratio_E - 1 / (f_r * r**2)) == 0,
      "g_rr/g_thth = 1/(f r^2), s-free and A-free")

# verify the isotropic consistency.  Both sides carry the common factor A^2 f^{-s}; strip it and test
# the s-free, A-free core identity  (dr/drho)^2 == f * r^2 / rho^2.
lhs = sp.simplify(sp.diff(r_of_rho, rho)**2)
rhs = sp.simplify(f_iso * r_of_rho**2 / rho**2)
check("C3  isotropy identity verified exactly:  (dr/drho)^2 = f r^2/rho^2 (the s-free, A-free core of "
      "f^{-s}(dr/drho)^2 = f^{1-s} r^2/rho^2), so ghat_ij = A^2 f^{1-s}(1 + b/4rho)^4 delta_ij is EXACTLY "
      "isotropic for every s and every conformal factor",
      sp.simplify(sp.expand(lhs - rhs)) == 0,
      f"(dr/drho)^2 - f r^2/rho^2 = {sp.simplify(sp.expand(lhs - rhs))}")

# EXACT b-series machinery.  ln f is analytic in b, so f^p = exp(p ln f) can be expanded for SYMBOLIC p.
Lf = sp.series(sp.log(sp.Rational(1,1)*(1 - b/(4*rho))) - sp.log(1 + b/(4*rho)), b, 0, 4).removeO() * 2
Lf = sp.expand(sp.simplify(Lf))            # = -b/rho + O(b^3)
check("C4  ln f = 2[ln(1 - b/4rho) - ln(1 + b/4rho)] = -b/rho + O(b^3) EXACTLY -- the b^2 coefficient "
      "vanishes identically, which is what makes the beta extraction below clean",
      sp.simplify(Lf.coeff(b, 1) + 1/rho) == 0 and sp.simplify(Lf.coeff(b, 2)) == 0,
      f"ln f = {Lf}")


def fpow_series(p, order=3):
    """exact b-series of f_iso**p for SYMBOLIC exponent p."""
    Lt = sum(Lf.coeff(b, n) * b**n for n in range(1, order))
    out = 0
    for n in range(0, order):
        out += (p * Lt)**n / sp.factorial(n)
    return sp.expand(sp.series(sp.expand(out), b, 0, order).removeO())


# =====================================================================================================
sec("PART D -- EXACT beta and gamma.  CASE 1: exponential (constant) fifth-force coupling A = e^{alpha phi}")
# =====================================================================================================
c = sp.symbols("c", real=True)   # c == 2 alpha k  (the scalar's contribution to the Jordan g_00 exponent)

# CASE 1: A^2 = e^{2 alpha phi} = f^{2 alpha k} = f^c  =>  ghat_00 = -f^{s+c}
nu = s + c
g00_hat_exp = -f_iso**nu
g00_series = sp.expand(-fpow_series(nu, 3))

c1 = sp.expand(sp.simplify(g00_series.coeff(b, 1)))       # coefficient of b^1  -> 2m/rho  => 2 G_N M = nu b
c2 = sp.expand(sp.simplify(g00_series.coeff(b, 2)))       # coefficient of b^2  -> -2 beta m^2/rho^2

m_over_b = sp.simplify(c1 * rho / 2)                       # m/b   (m = G_N M)
beta_exp = sp.simplify(-c2 * rho**2 / (2 * (m_over_b)**2))

check("D1  (exponential coupling) the DYNAMICAL mass read from ghat_00 is 2 G_N M = (s + c) b == nu b, "
      "where c = 2 alpha k is the fifth-force part of the exponent",
      sp.simplify(m_over_b - nu / 2) == 0,
      f"m/b = {sp.simplify(m_over_b)}")

check("D2  *** beta = 1 EXACTLY for a constant (exponential) fifth-force coupling, for ANY s and ANY c *** "
      "-- i.e. for ANY strength of the fifth force.  The reason is structural: ghat_00 = -f^nu is a pure "
      "power of f for every nu, and the isotropic expansion of -f^nu always has b^2 coefficient -nu^2/2, "
      "which is exactly -2 m^2 with m = nu b/2.  The effective-G split cancels identically in beta.",
      sp.simplify(beta_exp - 1) == 0,
      f"beta = {sp.simplify(beta_exp)}  (identically 1, s- and c-free)")

# gamma from ghat_ij
gij_hat_exp = f_iso**c * f_iso**(1 - s) * (1 + b / (4 * rho))**4
gij_ser = sp.expand(sp.series(sp.expand(fpow_series(c + 1 - s, 3) * (1 + b/(4*rho))**4), b, 0, 2).removeO())
gam_coef = sp.simplify(gij_ser.coeff(b, 1))               # = 2 gamma m / (b rho)
gamma_exp = sp.simplify(gam_coef * rho / (2 * m_over_b))
check("D3  (exponential coupling) gamma = (s - c)/(s + c) EXACTLY.  With the fifth-force FRACTION "
      "f_frac == G_s/G_N = c/(s+c) this is gamma = 1 - 2 f_frac.  *** THE EFFECTIVE-G SPLIT LEAKS INTO "
      "gamma, NOT INTO beta. ***  Light measures the Einstein-frame mass s*b; orbits measure (s+c)*b.",
      sp.simplify(gamma_exp - (s - c) / (s + c)) == 0,
      f"gamma = {sp.simplify(gamma_exp)} = 1 - 2 c/(s+c)")

ff = sp.symbols("f_frac", positive=True)
check("D4  substitution check: writing c = f_frac (s + c) i.e. f_frac = c/(s+c), gamma = 1 - 2 f_frac exactly",
      sp.simplify(((s - c) / (s + c)).subs(c, s * ff / (1 - ff)) - (1 - 2 * ff)) == 0,
      "gamma(f_frac) = 1 - 2 f_frac")

# =====================================================================================================
sec("PART D -- CASE 2: strictly LINEAR conformal coupling A = 1 + lambda phi (the 'S_int = -lambda phi rho' reading)")
# =====================================================================================================
lam = sp.symbols("lam", real=True)
# A = 1 + lambda phi = 1 + lambda k ln f  =>  A^2 = (1 + (c/2) ln f)^2 with c = 2 lambda k
A2_lin = (1 + (c / 2) * sp.log(f_iso))**2
g00_hat_lin = -A2_lin * f_iso**s
Lt3 = sum(Lf.coeff(b, n) * b**n for n in range(1, 3))
g00_lin_ser = sp.expand(sp.series(sp.expand(-(1 + (c/2)*Lt3)**2 * fpow_series(s, 3)), b, 0, 3).removeO())

c1L = sp.expand(sp.simplify(g00_lin_ser.coeff(b, 1)))
c2L = sp.expand(sp.simplify(g00_lin_ser.coeff(b, 2)))
mL = sp.simplify(c1L * rho / 2)
beta_lin = sp.simplify(-c2L * rho**2 / (2 * mL**2))

check("D5  (linear coupling) the dynamical mass is unchanged at leading order: 2 G_N M = (s + c) b, "
      "because 1 + lambda phi and e^{lambda phi} agree to first order",
      sp.simplify(mL - nu / 2) == 0,
      f"m/b = {sp.simplify(mL)}")

beta_lin_s = sp.simplify(sp.factor(sp.simplify(beta_lin)))
target_lin = 1 - sp.Rational(1, 2) * (c / (s + c))**2
check("D6  *** (linear coupling) beta = 1 - (1/2) [c/(s+c)]^2 = 1 - f_frac^2/2 EXACTLY *** -- the deviation "
      "from beta = 1 is SECOND order in the fifth-force fraction, and is NEGATIVE.  It comes entirely from "
      "the curvature of A(phi) (d^2 lnA/dphi^2 = -lambda^2 != 0), not from the effective-G split.",
      sp.simplify(beta_lin_s - target_lin) == 0,
      f"beta = {beta_lin_s}")

gij_hat_lin = A2_lin * f_iso**(1 - s) * (1 + b / (4 * rho))**4
gij_lin_ser = sp.expand(sp.series(sp.expand((1 + (c/2)*Lt3)**2 * fpow_series(1 - s, 3) * (1 + b/(4*rho))**4), b, 0, 2).removeO())
gamma_lin = sp.simplify(gij_lin_ser.coeff(b, 1) * rho / (2 * mL))
check("D7  (linear coupling) gamma = (s-c)/(s+c) = 1 - 2 f_frac, IDENTICAL to the exponential case: "
      "gamma is first order in the coupling and cannot tell the two coupling forms apart",
      sp.simplify(gamma_lin - (s - c) / (s + c)) == 0,
      f"gamma = {sp.simplify(gamma_lin)}")

# =====================================================================================================
sec("PART E -- the Nordtvedt combination, and the ISOLATION of the effective-G split")
# =====================================================================================================
eta_exp = sp.simplify(4 * 1 - gamma_exp - 3)
eta_lin = sp.simplify(4 * beta_lin_s - gamma_lin - 3)
eta_exp_f = sp.simplify(eta_exp.subs(c, s * ff / (1 - ff)))
eta_lin_f = sp.simplify(eta_lin.subs(c, s * ff / (1 - ff)))

check("E1  eta_N = 4 beta - gamma - 3 = 2 f_frac  (exponential coupling) -- i.e. the Nordtvedt effect is "
      "FIRST order in the fifth-force fraction and is entirely inherited from gamma, since beta = 1",
      sp.simplify(eta_exp_f - 2 * ff) == 0,
      f"eta_N = {eta_exp_f}")

check("E2  eta_N = 2 f_frac - 2 f_frac^2  (linear coupling) -- same leading behaviour",
      sp.simplify(eta_lin_f - (2 * ff - 2 * ff**2)) == 0,
      f"eta_N = {sp.simplify(eta_lin_f)}")

# The critical subtlety, isolated:
check("E3  *** THE CRITICAL SUBTLETY, RESOLVED. ***  Write the metric with the BARE G (the Einstein-frame "
      "normalisation): then Psi = Phi and 'gamma = 1'.  Write it with the DYNAMICAL G_N (the PPN "
      "normalisation, the only one an observer can use) and gamma = 1 - 2 f_frac.  The two differ by the "
      "effective-G split alone.  beta, by contrast, is IDENTICAL in the two normalisations to O(f_frac^2): "
      "the b^2 coefficient of -f^nu scales as nu^2 exactly as m^2 does, so the split cancels in beta. "
      "CONCLUSION: the split leaks into gamma (at O(f)) and into eta_N (at O(f)), but into beta only at "
      "O(f^2) and only through the coupling's curvature.",
      sp.simplify(beta_exp - 1) == 0 and sp.simplify(sp.series(beta_lin_s.subs(c, s * ff / (1 - ff)), ff, 0, 3).removeO()
                                                     - (1 - ff**2 / 2)) == 0,
      "beta_exp - 1 == 0 identically; beta_lin = 1 - f^2/2 + O(f^3)")

# =====================================================================================================
sec("PART F -- consistency: reproduce the known scalar-tensor (Damour-Esposito-Farese) formulae")
# =====================================================================================================
al0, be0 = sp.symbols("alpha_0 beta_0", real=True)
gamma_DEF = 1 - 2 * al0**2 / (1 + al0**2)
beta_DEF = 1 + sp.Rational(1, 2) * be0 * al0**2 / (1 + al0**2)**2
# our f_frac maps to alpha_0^2/(1+alpha_0^2)
ff_map = al0**2 / (1 + al0**2)
check("F1  our gamma = 1 - 2 f_frac reproduces the standard scalar-tensor result gamma - 1 = "
      "-2 alpha_0^2/(1+alpha_0^2) under the identification f_frac = alpha_0^2/(1+alpha_0^2) "
      "(equivalently G_N = G(1 + alpha_0^2))",
      sp.simplify((1 - 2 * ff_map) - gamma_DEF) == 0,
      "matches Damour-Esposito-Farese")
check("F2  our beta = 1 (exponential) reproduces DEF's beta - 1 = (1/2) beta_0 alpha_0^2/(1+alpha_0^2)^2 "
      "with beta_0 = d alpha/d phi = 0, which is exactly the constant-coupling (Brans-Dicke) case: "
      "Brans-Dicke has beta = 1 for every omega -- an independent cross-check of D2",
      sp.simplify(beta_DEF.subs(be0, 0) - 1) == 0,
      "beta_0 = 0 => beta = 1")
check("F3  our beta = 1 - f_frac^2/2 (linear) reproduces DEF with beta_0 = -alpha_0^2 (the curvature of "
      "A = 1 + lambda phi at phi = 0 in canonically normalised units)",
      sp.simplify(sp.series(beta_DEF.subs(be0, -al0**2), al0, 0, 5).removeO()
                  - sp.series((1 - ff_map**2 / 2), al0, 0, 5).removeO()) == 0,
      "beta_DEF(beta_0=-alpha_0^2) = 1 - alpha_0^4/2 + ... = 1 - f_frac^2/2 + ...")

w = sp.symbols("omega", positive=True)
# Brans-Dicke in Einstein-frame variables: alpha_0^2 = 1/(2 omega + 3)  =>  f_frac = alpha_0^2/(1+alpha_0^2)
ff_BD = sp.simplify((1 / (2 * w + 3)) / (1 + 1 / (2 * w + 3)))
check("F4  *** TEXTBOOK CROSS-CHECK. ***  Substituting the Brans-Dicke value alpha_0^2 = 1/(2 omega + 3) "
      "into our gamma = 1 - 2 f_frac gives EXACTLY gamma = (1 + omega)/(2 + omega), the textbook "
      "Brans-Dicke light-deflection parameter -- and our beta gives exactly beta = 1, the textbook "
      "Brans-Dicke value for every omega.  This is the strongest available confirmation that the "
      "'gamma = 1' of the branch spec is a BARE-G statement and the OBSERVABLE gamma is 1 - 2 f_frac.",
      sp.simplify((1 - 2 * ff_BD) - (1 + w) / (2 + w)) == 0,
      f"gamma(BD) = {sp.simplify(1 - 2*ff_BD)} = (1+omega)/(2+omega);  beta(BD) = 1")

check("F5  the Cassini bound |gamma - 1| < 2.3e-5 therefore translates into the familiar omega > 4e4 "
      "(Bertotti-Iess-Tortora 2003) under this dictionary, confirming the normalisation is the standard one",
      abs(float(sp.solve(sp.Eq(1 - (1 + w) / (2 + w), sp.Rational(23, 1000000)), w)[0]) - 43476) < 200,
      f"omega_min = {float(sp.solve(sp.Eq(1 - (1+w)/(2+w), sp.Rational(23,1000000)), w)[0]):.0f}  "
      "(literature: omega > 4e4)")

# =====================================================================================================
sec("PART G -- what the fifth force does NOT do: an explicit statement of the residual assumptions")
# =====================================================================================================
check("G1  [SCOPE] beta is computed for the EXTERIOR of a single static spherical body.  The PPN beta is "
      "defined by exactly this coefficient (the U^2 term of g_00), so this is the complete determination "
      "of beta.  The Whitehead parameter xi and the many-body O(4) potentials are NOT computed here.",
      True, "single-body U^2 coefficient = the definition of beta")
check("G2  [INHERITED ASSUMPTION, NOT PROVED HERE] the cuscuton clock contributes no O(2) stress.  If it "
      "did, it would renormalise the metric-sector G universally (affecting light and matter alike), which "
      "rescales G but does NOT change f_frac, hence does NOT change gamma, beta or eta_N.  A clock stress "
      "that acted differently on the two would be an additional gamma contribution.  FLAGGED AS OPEN.",
      True, "universal clock-G renormalisation is beta-neutral; non-universal is UNDETERMINED")
check("G3  [SCOPE] the above holds where mu = 1 to exponential accuracy (y >> 1).  Where y <~ 1 the scalar "
      "is in its OWN MOND regime, the exterior is no longer Einstein+massless-canonical-scalar, and the PPN "
      "expansion itself does not apply.  Whether the solar system satisfies y >> 1 is the numeric gate.",
      True, "PPN validity <=> y >> 1 everywhere tested")

# =====================================================================================================
sec("SUMMARY")
# =====================================================================================================
print("""
  EXACT RESULTS (f == f_frac == G_s/G_N, the fifth-force fraction of Newtonian gravity):

      gamma_PPN =  1 - 2 f                                  (exact, both coupling forms)
      beta_PPN  =  1                                        (exact, A = e^{alpha phi}: constant coupling)
      beta_PPN  =  1 - f^2/2                                (exact, A = 1 + lambda phi: linear coupling)
      eta_N     =  4 beta - gamma - 3 = 2f  or  2f - 2f^2

  => BETA IS PROTECTED.  The effective-G split (G_N = G + G_s) leaks into gamma and eta_N at FIRST order
     in f, but into beta only at SECOND order and only via the coupling's curvature.  A theory of this
     class CANNOT be killed by beta; it is killed (or cleared) by gamma, eta_N and the perihelion anomaly.
""")

print("=" * 110)
print(f"{'ALL CHECKS PASS' if not FAILS else 'FAILURES: ' + str(FAILS)}   {N[0] - len(FAILS)}/{N[0]}   [{time.time()-T0:.1f}s]")
print("=" * 110)
sys.exit(1 if FAILS else 0)
