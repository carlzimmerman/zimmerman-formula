#!/usr/bin/env python3
r"""mi_PX_field_sector_2026.py -- LANE T2: THE P(X) FIELD SECTOR AT TREE LEVEL.

WHY THIS SCRIPT EXISTS.  The Ward-identity lane closed the possibility that acceleration-dependent inertia
arises from the broken-boost symmetry algebra, and it recorded ONE explicit exclusion: "MOND-like behaviour in
condensate models lives in the FIELD sector (P(X) nonlinearity), which this lane never touched."  This touches
it.  Everything here is TREE LEVEL by construction (a classical field equation), so it evades the loop-level
death of mi_drift_magnitude_audit_2026.py entirely.

THE QUESTION.  A shift-symmetric L = P(X) with a matter coupling gives, in the static weak-field limit, exactly
the AQUAL equation grad.(P'(X) grad phi) = 4 pi G rho -- so the MOND interpolation function IS P'.  The
cosmological ghost condensate needs P'(X_0) = 0 at a NONZERO X_0 (that is what makes phidot constant and
supplies the dark sector).  Can ONE function P do both?  If yes, a_0 is set by where P' crosses over, which is
set by X_0, which is set by rho_Lambda -- and that would be a DERIVATION of a_0, hence of kappa.

THE ANSWER (this script).  NO, and the obstruction is a single SIGN FACT.  Writing the covariant kinetic
variable as W = phidot^2/c^2 - |grad phi|^2 (W > 0 timelike, W < 0 spacelike) and P = P(W):

    * the quasistatic sector about the attractor probes W = W_0 - eps^2 with eps = |grad phi|, so the AQUAL
      interpolation function is IDENTICALLY  m(eps) = P'(W_0 - eps^2)  -- and eps -> W = W_0 - eps^2 is a
      BIJECTION of (0, inf) onto (-inf, W_0), so choosing P below the attractor IS choosing m;
    * m(0) = P'(W_0) = 0 (attractor) and m'(eps) = -2 eps P''(W_0 - eps^2) so m'(0) = 0, and
            m''(0) = -2 P''(W_0);
    * the ghost condensate's no-ghost condition at the attractor is P' + 2 W P'' > 0 |_{W_0} = 2 W_0 P''(W_0) > 0,
      i.e. P''(W_0) > 0, i.e. m''(0) < 0;
    * with m(0) = m'(0) = 0 and m''(0) < 0, m < 0 on a punctured neighbourhood: the quasistatic interpolation
      function is NEGATIVE -- REPULSIVE gravity -- exactly where MOND needs it positive and linear.
      And at best |m| ~ eps^2, the WRONG POWER (MOND needs m ~ eps/a_0).

    THEOREM T2 (stated with hypotheses in S5).  No P that is C^2 at a timelike attractor W_0 > 0 with a
    positive time-kinetic norm can produce a positive deep-MOND interpolation function for quasistatic
    perturbations about that attractor.  MOND wants P'' < 0 on the branch it probes; the condensate wants
    P''(W_0) > 0.  Same sign fact, opposite signs.

    COROLLARY (the dichotomy, S5d).  Let R = W_0/a_0^2.  If R >~ 1 the static field probes the attractor, and
    MOND fails structurally (m < 0, m ~ eps^2, g_obs ~ g_bar^(1/3), v ~ r^(1/6): no flat rotation curves at
    all).  If R << 1 the static field probes the LIGHT CONE instead, AQUAL works -- but the MOND-reproducing P'
    has a SQUARE-ROOT BRANCH POINT at W = 0 (S5c), so it admits no real-analytic continuation into the timelike
    region, and a_0 is then an INDEPENDENT scale of P, unrelated to X_0 or rho_Lambda.  a_0 is NOT derived here.
    kappa REMAINS FITTED.
    AND A CORRECTION AGAINST THE LANE'S OWN HOPE (S5e): even the R >~ 1 branch never fixed a_0.  The MOND
    crossover of m = P''(W_0) eps^2 sits at eps = 1/sqrt(P''(W_0)), which is INDEPENDENT of W_0 (verified
    symbolically): the attractor's position sets only where the force REVERSES, while the acceleration scale is
    set by P''(W_0) -- a free parameter of P.  So the premise "a_0 would be set by where P' crosses over, which
    is fixed by X_0" is FALSE even before T2 is applied, and I withdraw it.  Two independent reasons, one per
    branch, and the condensate sets a_0 in neither.

WHAT ELSE IS COMPUTED, and is new here:

  S2  The closed-form AQUAL function for the framework's OWN kernel nu = sqrt(1+1/y).  Inverting the exact law
      g_obs^2 = g_bar^2 + a_0 g_bar gives mu(x) = (sqrt(1+4x^2)-1)/(2x), x = g_obs/a_0, and integrating P' = mu:

            P(X) = a_0^2 [ (t/2) sqrt(1+4t^2) + (1/4) asinh(2t) - t ],   t = sqrt(X)/a_0,  X = |grad phi|^2

      whose deep limit is (2/3)|grad phi|^3/a_0 -- Bekenstein-Milgrom's standard deep-MOND Lagrangian, recovered
      not assumed -- and whose Newtonian limit is X - a_0 sqrt(X) + a_0^2/8 + (a_0^2/4) ln(4t).

  S3  That P is FULLY ADMISSIBLE on the spacelike branch: P' = mu > 0 (no ghost), d(x mu)/dx > 0 (elliptic,
      no gradient instability) -- but P''(W) < 0 IDENTICALLY, and the longitudinal propagation speed is
            c_s^2 = d(x mu)/dx / mu = 4x^2 / [sqrt(1+4x^2)(sqrt(1+4x^2)-1)]  in (1, 2],  -> 2 EXACTLY deep.
      So the COVARIANT completion's scalar is SUPERLUMINAL everywhere, c_s = sqrt(2) c in the deep-MOND regime,
      and P'' < 0 violates the Adams-Arkani-Hamed-Dubovsky-Nicolis-Rattazzi positivity/analyticity bound.
      AGAINST INTEREST, and it is the SAME SIGN the theorem turns on.  SCOPE, stated precisely: strict AQUAL is
      an elliptic constraint with no propagation at all, so this is a statement about the P(W) FIELD THEORY that
      the lane is required to work in -- which is the point, since that is the only version in which the
      condensate could have supplied a_0.  Superluminal MOND-like scalars are a known result (Bruneton and
      Esposito-Farese 2007); the c_s^2 = 2 value for THIS kernel is computed here.

  S4  The corpus's committed attractor sound speed c_s^2 = u/(3u+2) is re-derived symbolically from
      P = P_0 + (lambda/2)(X-X_0)^2 (the historical u/(u+2) slip is used as a negative control), and the
      corpus's OWN quadratic P is shown to give m(eps) = -lambda eps^2: repulsive and quadratic, the theorem
      instantiated on the corpus's own committed function.

  S6/S7  Independent predictions and both footings.

MANDATORY CREDIT.  nu(y) = sqrt(1+1/y) and the de Sitter-Unruh balance are MILGROM 1999 PLA 253:273 eqs 6-9
(he fixes a_0_hat = 2 c H_Lambda, r = 1); his eqs 10-11 give a second coefficient (r = 2), and MILGROM 2008
arXiv:0801.3133 sec 7.3.1 notes the coefficient mismatch "isn't necessarily meaningful".  The framework's
distinctive content is the c H_Lambda / Z COEFFICIENT and the modified-INERTIA completion, NOT the kernel.
a_lambda = c^2 sqrt(Lambda/3): MILGROM 1994 Ann.Phys. 229:384.  Temperature sqrt(a^2+Lambda/3)/2pi: NARNHOFER,
PETER and THIRRING 1996 IJMPB 10:1507.  Five-acceleration: DESER and LEVIN 1997 CQG 14:L163.  Exponential
kernel: McGAUGH 2008 ApJ 683:137 eq 11a.  AQUAL: BEKENSTEIN and MILGROM 1984 ApJ 286:7.  Ghost condensate:
ARKANI-HAMED, CHENG, LUTY and MUKOHYAMA 2004 JHEP 0405:074.  Boost-breaking EFT: NICOLIS, PENCO, PIAZZA and
RATTAZZI 2015.  Positivity/analyticity: ADAMS, ARKANI-HAMED, DUBOVSKY, NICOLIS and RATTAZZI 2006 JHEP 0610:014.
Superluminality of MOND-like scalars: BRUNETON and ESPOSITO-FARESE 2007 PRD 76:124012.  GHY: GIBBONS and
HAWKING 1977, YORK 1972.  The corpus's condensate background, the c_s^2 = u/(3u+2) closed form and the banked
attractor rate phidot = a_0/c are from mi_cosmo_perturbations_2026.py.

*** kappa = 1/2 IS FITTED, NOT DERIVED.  Nothing below changes that; S5 is why this particular route cannot. ***

FLOAT64 HAZARDS HANDLED: catastrophic cancellation in sqrt(1+4x^2)-1 (rewritten 4x^2/(sqrt(1+4x^2)+1), and the
naive form is measured against mpmath so the hazard is DEMONSTRATED, not asserted); 1-exp(-sqrt(y)) via -expm1;
log1p for the Newtonian expansion; every grid quantity re-run at 4x resolution with the shift printed; a
dimensional-rescaling reproduction check (a_0 -> 1.2082 a_0, i.e. the ALT footing, is a pure rescaling of the
whole lane) which is exactly the class of check that caught a real s-vs-s*T bug in this project.

NEGATIVE CONTROLS (each must trip a NAMED check): NC1 simple mu = x/(1+x) must fail the exact law; NC2
c_s^2 = u/(u+2) must fail the attractor closed form; NC3 flipping the no-ghost sign must flip the theorem's
conclusion; NC4 dropping the asinh term must break the (2/3) t^3 deep limit; NC5 mislabelling the AQUAL
argument as P'(|grad phi|) instead of P'(-|grad phi|^2) must break the Euler-Lagrange reduction.

Exit 0 = every check held.
"""
from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp

try:
    import mpmath as mp
    mp.mp.dps = 50
    HAVE_MP = True
except Exception:                                                        # pragma: no cover
    HAVE_MP = False

# ==================================================================================================
_RESULTS: list[tuple[bool, str]] = []


def check(cond, msg: str) -> bool:
    ok = bool(cond)
    _RESULTS.append((ok, msg))
    print(("  [OK]   " if ok else "  [FAIL] ") + msg)
    return ok


def banner(s: str) -> None:
    print("\n" + "=" * 108)
    print(s)
    print("=" * 108)


def sub(s: str) -> None:
    print("\n  --- " + s)


# --------------------------------------------------------------------------------------------------
# constants -- both footings on every dimensional number
C_LIGHT = 2.99792458e8
G_NEWT = 6.67430e-11
RHO_LAMBDA = 5.844e-27                      # kg/m^3, canonical (pure Lambda)
KAPPA = 0.5
A0_CANON = 9.3614e-11                       # m/s^2  kappa = 1/2 footing
A0_ALT = 1.13e-10                           # m/s^2  ALT footing (x1.2082)
CH_LAMBDA = 5.4194e-10
H_LAMBDA = 1.80772e-18
Z_CONST = 2.0 * math.sqrt(8.0 * math.pi / 3.0)
FOOTINGS = (("canonical kappa=1/2  a_0=9.3614e-11", A0_CANON), ("ALT  a_0=1.13e-10 (x1.2082)", A0_ALT))
SHAPE_SYST_DEX = math.log10(1.306)          # the corpus's 30.6% shape systematic, in dex


# ==================================================================================================
def mu_stable(x):
    """mu(x) = (sqrt(1+4x^2)-1)/(2x), rewritten to kill the catastrophic cancellation at small x:
    (sqrt(1+4x^2)-1) = 4x^2/(sqrt(1+4x^2)+1)  =>  mu = 2x/(sqrt(1+4x^2)+1).  Exact algebra, no subtraction."""
    x = np.asarray(x, float)
    return 2.0 * x / (np.sqrt(1.0 + 4.0 * x * x) + 1.0)


def mu_naive(x):
    """The hazardous form, kept ONLY to measure the hazard."""
    x = np.asarray(x, float)
    return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)


def mu_simple(x):
    """NC1: the 'simple' interpolation function, which is NOT the framework's."""
    x = np.asarray(x, float)
    return x / (1.0 + x)


def nu_framework(y):
    """nu(y) = sqrt(1+1/y).  MILGROM 1999 eq 9 kernel; the framework's distinctive content is the coefficient."""
    y = np.asarray(y, float)
    return np.sqrt(1.0 + 1.0 / y)


def nu_mcgaugh(y):
    """McGAUGH 2008 ApJ 683:137 eq 11a, nu = 1/(1-exp(-sqrt(y))).  -expm1 kills the 1-exp underflow."""
    y = np.asarray(y, float)
    return -1.0 / np.expm1(-np.sqrt(y))


def P_closed(X, a0):
    """The closed form as written.  HAZARD: for t << 1 the three terms are each O(t) and cancel down to
    O(t^3), so the relative float64 error is ~eps/t^2 -- 2e-4 at t = 1e-6.  Kept to measure the hazard."""
    X = np.asarray(X, float)
    t = np.sqrt(X) / a0
    return a0 * a0 * (0.5 * t * np.sqrt(1.0 + 4.0 * t * t) + 0.25 * np.arcsinh(2.0 * t) - t)


# P/[(2/3)a_0^2 t^3] = sum_k (3/2) [2 Cat(k-1) (-1)^(k+1)/(2k+1)] t^(2k-2), from term-by-term integration of
# sqrt(1+4t^2)-1 = sum_k 2 Cat(k-1) (-1)^(k+1) t^(2k).  Cancellation-free; 10 terms give <1e-15 up to t = 0.12,
# where the closed form has already recovered to ~7e-15.  Switching there keeps P good to ~1e-14 EVERYWHERE.
_DEEP_COEF = (1.0, -3.0 / 5.0, 6.0 / 7.0, -5.0 / 3.0, 42.0 / 11.0,
              -126.0 / 13.0, 132.0 / 5.0, -1287.0 / 17.0, 4290.0 / 19.0, -4862.0 / 7.0)
_DEEP_CUT = 0.12


def P_static(X, a0):
    """P(X) = a_0^2 [ (t/2)sqrt(1+4t^2) + (1/4)asinh(2t) - t ], t = sqrt(X)/a_0, X = |grad phi|^2.
    dP/dX = mu(t) exactly (S2).  Newtonian limit P -> X; deep limit P -> (2/3) X^{3/2}/a_0.
    Evaluated by the cancellation-free deep series below t = 1e-2 (truncation there ~1e-19 relative) and by
    the closed form above it (cancellation there <= 2e-12 relative): NINTH float64 hazard of this project."""
    X = np.asarray(X, float)
    t = np.sqrt(X) / a0
    ser = sum(ck * t ** (2 * k) for k, ck in enumerate(_DEEP_COEF))
    deep = a0 * a0 * (2.0 / 3.0) * t ** 3 * ser
    return np.where(t < _DEEP_CUT, deep, P_closed(X, a0))


def P_static_broken(X, a0):
    """NC4: the asinh term dropped."""
    X = np.asarray(X, float)
    t = np.sqrt(X) / a0
    return a0 * a0 * (0.5 * t * np.sqrt(1.0 + 4.0 * t * t) - t)


# ==================================================================================================
def S0_footing():
    banner("S0 -- FOOTING LOCK.  a_0 = kappa c sqrt(G rho_Lambda), both footings, and the pi-free identity.")

    csqrt = C_LIGHT * math.sqrt(G_NEWT * RHO_LAMBDA)
    print(f"    c sqrt(G rho_Lambda)          = {csqrt:.6e} m/s^2   (target 1.87228e-10)")
    check(abs(csqrt / 1.87228e-10 - 1.0) < 1e-4, f"c sqrt(G rho_Lambda) = {csqrt:.6e} reproduces 1.87228e-10")
    a0_from_formula = KAPPA * csqrt
    check(abs(a0_from_formula / A0_CANON - 1.0) < 1e-3,
          f"kappa=1/2 gives a_0 = {a0_from_formula:.6e}, matches canonical {A0_CANON:.4e}")
    check(abs(A0_ALT / A0_CANON / 1.2082 - 1.0) < 1e-3,
          f"ALT/canonical = {A0_ALT/A0_CANON:.6f} matches the banked 1.2082")
    check(abs(Z_CONST / 5.7888100366 - 1.0) < 1e-9, f"Z = 2 sqrt(8pi/3) = {Z_CONST:.10f}")
    q = A0_CANON / CH_LAMBDA
    check(abs(q - 2.0 / (2.0 * Z_CONST)) < 2e-5,
          f"CRP master formula: q = a_0/(c H_Lambda) = {q:.6f} = 2/r with r = 2Z = {2*Z_CONST:.6f}")

    sub("S0b  the pi-free corner's ONE EXACT FACTOR, verified before use (workflow item 8)")
    # A_hor = 4 pi (c/H)^2 with H^2 = 8 pi G rho/3  =>  A_hor = 3 c^2 / (2 G rho): pi-free.
    A_hor = 4.0 * math.pi * (C_LIGHT / H_LAMBDA) ** 2
    A_pifree = 3.0 * C_LIGHT ** 2 / (2.0 * G_NEWT * RHO_LAMBDA)
    check(abs(A_hor / A_pifree - 1.0) < 3e-3,
          f"A_hor = 4pi(c/H)^2 = {A_hor:.6e} equals the pi-free 3c^2/(2 G rho) = {A_pifree:.6e}")
    factor = (A0_CANON / 2.0) / (C_LIGHT ** 2 / math.sqrt(A_pifree))
    target = math.sqrt(6.0) / 8.0
    print(f"    (a_0/2) / (c^2/sqrt(A_hor))   = {factor:.12f}   vs  sqrt(6)/8 = {target:.12f}")
    check(abs(factor / target - 1.0) < 1e-3,
          f"the floor k = a_0/2 sits at sqrt(6)/8 = {target:.12f} of c^2/sqrt(A_hor)  [identity CONFIRMED]")


# ==================================================================================================
def S1_reduction():
    banner("S1 -- THE CRUX REDUCTION.  Shift-symmetric L = P(W) with a matter source  =>  AQUAL, symbolically.")

    print("""
    Covariant setup, signature (-,+,+,+), shift-symmetric field phi with matter coupling:

        S = Int d^4x [ (1/(8 pi G)) P(W) - rho phi ] ,   W = - g^{mu nu} d_mu phi d_nu phi
                                                            = phidot^2/c^2 - |grad phi|^2

    phi is normalised as a POTENTIAL, [grad phi] = m/s^2, so P -> W is exactly Newtonian gravity's
    -(grad phi)^2/(8 pi G) - rho phi.  Shift symmetry => the EOM is a total divergence, d_mu J^mu = -rho,
    J^mu = -(1/(4 pi G)) P'(W) d^mu phi: it INTEGRATES ONCE.  Static limit W = -|grad phi|^2:

        grad.( P'(W) grad phi ) = 4 pi G rho        <=>   AQUAL with  mu = P'(-|grad phi|^2).
    """)

    sub("S1a  sympy Euler-Lagrange in 3D, done independently and matched to the AQUAL divergence")
    x1, x2, x3, rho_s, Gs = sp.symbols('x1 x2 x3 rho G', positive=True)
    phi = sp.Function('phi')(x1, x2, x3)
    Pc = sp.Function('Pcal')
    wdum = sp.Symbol('w')

    def Pp(arg):
        """P'(arg) for an ABSTRACT P: an unevaluated Subs, so the chain rule is sympy's job, not mine."""
        return sp.Subs(sp.Derivative(Pc(wdum), wdum), wdum, arg)

    grads = [sp.diff(phi, v) for v in (x1, x2, x3)]
    W = -sum(g ** 2 for g in grads)
    L = Pc(W) / (8 * sp.pi * Gs) - rho_s * phi
    el = sp.euler_equations(L, [phi], [x1, x2, x3])[0]
    aqual = sum(sp.diff(Pp(W) * g, v) for g, v in zip(grads, (x1, x2, x3))) - 4 * sp.pi * Gs * rho_s
    resid = sp.simplify(sp.expand(el.lhs - el.rhs) - aqual / (4 * sp.pi * Gs))
    print(f"    Euler-Lagrange residual vs (1/4piG) x [grad.(P' grad phi) - 4 pi G rho]  =  {resid}")
    check(resid == 0,
          "sympy euler_equations(L) IS grad.(P'(W) grad phi) = 4 pi G rho  -- the AQUAL reduction, verified"
          " for an ABSTRACT P (no functional form assumed)")

    sub("S1b  NC5 (negative control): mislabel the argument as P'(|grad phi|) instead of P'(-|grad phi|^2)")
    Wbad = sp.sqrt(sum(g ** 2 for g in grads))
    Lbad = Pc(Wbad) / (8 * sp.pi * Gs) - rho_s * phi
    elbad = sp.euler_equations(Lbad, [phi], [x1, x2, x3])[0]
    resid_bad = sp.simplify(sp.expand(elbad.lhs - elbad.rhs) - aqual / (4 * sp.pi * Gs))
    check(resid_bad != 0,
          "NC5 TRIPPED: the mislabelled argument does NOT reduce to AQUAL (residual != 0), so S1a can fail")

    sub("S1c  spherical symmetry: the 3D divergence really is (1/r^2) d/dr[r^2 mu f'], so it integrates ONCE")
    a0v = 1.3
    xx1, xx2, xx3 = sp.symbols('X1 X2 X3', positive=True)
    rad = sp.sqrt(xx1 ** 2 + xx2 ** 2 + xx3 ** 2)
    fc = sp.Rational(7, 10) * sp.log(rad) + sp.Rational(2, 5) * rad ** sp.Rational(3, 2)

    def mu_s(g):
        return (sp.sqrt(1 + 4 * (g / a0v) ** 2) - 1) / (2 * (g / a0v))

    gr = [sp.diff(fc, v) for v in (xx1, xx2, xx3)]
    gmag = sp.sqrt(sum(g ** 2 for g in gr))
    div3d = sp.lambdify((xx1, xx2, xx3),
                        sum(sp.diff(mu_s(gmag) * g, v) for g, v in zip(gr, (xx1, xx2, xx3))), 'numpy')
    rr = sp.Symbol('r', positive=True)
    fr = sp.Rational(7, 10) * sp.log(rr) + sp.Rational(2, 5) * rr ** sp.Rational(3, 2)
    fp = sp.diff(fr, rr)
    radial = sp.lambdify(rr, sp.diff(rr ** 2 * mu_s(fp) * fp, rr) / rr ** 2, 'numpy')
    nhat = np.array([0.3, 0.5, 0.81]); nhat /= np.linalg.norm(nhat)
    devs = []
    for R in (0.3, 1.0, 2.5, 10.0, 100.0):
        p = R * nhat
        devs.append(abs(div3d(*p) / radial(R) - 1.0))
        print(f"    r = {R:7.2f}:  cartesian div = {div3d(*p):.12e}   (1/r^2)(r^2 mu f')' = {radial(R):.12e}")
    print(f"    max relative deviation over 5 radii and an off-axis direction: {max(devs):.3e}")
    check(max(devs) < 1e-12,
          f"the 3D divergence equals the radial form to {max(devs):.1e}  =>  r^2 mu(f') f' = G M(r) after ONE"
          f" integration: mu(g_obs) g_obs = g_bar")
    # NC5b: corrupt the argument of mu (use f' instead of |f'| via a wrong power) and the identity must break
    radial_bad = sp.lambdify(rr, sp.diff(rr ** 2 * mu_s(fp ** 2) * fp, rr) / rr ** 2, 'numpy')
    dev_bad = abs(div3d(*(1.0 * nhat)) / radial_bad(1.0) - 1.0)
    check(dev_bad > 1e-3,
          f"NC5b TRIPPED: feeding mu the wrong argument breaks the identity by {dev_bad:.3e}")

    sub("S1d  the algebraic content of the once-integrated form")
    gobs, gbar, a0s = sp.symbols('g_obs g_bar a_0', positive=True)
    mu_expr = (sp.sqrt(1 + 4 * (gobs / a0s) ** 2) - 1) / (2 * (gobs / a0s))
    step = sp.simplify(sp.solve(sp.Eq(mu_expr * gobs, gbar), gbar)[0] - (gobs ** 2 - 0) / gobs * 0
                       - (sp.sqrt(a0s ** 2 + 4 * gobs ** 2) - a0s) / 2)
    check(sp.simplify(step) == 0,
          "mu(g_obs) g_obs = (sqrt(a_0^2+4 g_obs^2)-a_0)/2, i.e. g_bar solved from the kernel, exactly")


# ==================================================================================================
def S2_reconstruct():
    banner("S2 -- WHAT P MUST BE.  Invert nu = sqrt(1+1/y) and integrate.  Closed form for P.")

    sub("S2a  the interpolation function mu implied by the framework's exact law, symbolically")
    xs, ss = sp.symbols('x s', positive=True)
    # exact law in units of a_0:  x^2 = s^2 + s,  x = g_obs/a_0, s = g_bar/a_0
    s_of_x = sp.solve(sp.Eq(xs ** 2, ss ** 2 + ss), ss)
    s_pos = [q for q in s_of_x if sp.simplify(q.subs(xs, 1)) > 0][0]
    mu_sym = sp.simplify(s_pos / xs)
    print(f"    s(x) = {sp.simplify(s_pos)}")
    print(f"    mu(x) = s/x = {mu_sym}")
    check(sp.simplify(mu_sym - (sp.sqrt(1 + 4 * xs ** 2) - 1) / (2 * xs)) == 0,
          "mu(x) = (sqrt(1+4x^2)-1)/(2x) follows from g_obs^2 = g_bar^2 + a_0 g_bar")
    check(sp.simplify(sp.limit(mu_sym / xs, xs, 0) - 1) == 0, "deep limit mu -> x (Milgrom regime), exactly")
    check(sp.limit(mu_sym, xs, sp.oo) == 1, "Newtonian limit mu -> 1, exactly")
    # nu-mu consistency:  nu(y) = sqrt(1+1/y) with y = s  <=>  x = nu(s) s
    ys = sp.Symbol('y', positive=True)
    resid_nu = sp.simplify((sp.sqrt(1 + 1 / ys) * ys) ** 2 - (ys ** 2 + ys))
    check(resid_nu == 0, "nu(y) = sqrt(1+1/y) and the exact law are the SAME statement (residual 0)")

    sub("S2b  NC1 (negative control): the 'simple' mu = x/(1+x) must FAIL the exact law")
    x_num = np.logspace(-3, 3, 41)
    s_fw = mu_stable(x_num) * x_num
    s_simple = mu_simple(x_num) * x_num
    r_fw = np.max(np.abs(x_num ** 2 - (s_fw ** 2 + s_fw)) / x_num ** 2)
    r_sp = np.max(np.abs(x_num ** 2 - (s_simple ** 2 + s_simple)) / x_num ** 2)
    print(f"    max relative exact-law residual: framework mu = {r_fw:.3e} ,  simple mu = {r_sp:.3e}")
    check(r_fw < 1e-14, f"framework mu satisfies x^2 = s^2+s to {r_fw:.2e}")
    check(r_sp > 1e-2, f"NC1 TRIPPED: simple mu violates it by {r_sp:.3e} -- the check above can fail")

    sub("S2c  integrate P' = mu to closed form and verify dP/dX = mu symbolically")
    Xs, a0s = sp.symbols('X a_0', positive=True)
    t = sp.sqrt(Xs) / a0s
    P_expr = a0s ** 2 * (t / 2 * sp.sqrt(1 + 4 * t ** 2) + sp.asinh(2 * t) / 4 - t)
    dP = sp.simplify(sp.diff(P_expr, Xs))
    mu_of_t = (sp.sqrt(1 + 4 * t ** 2) - 1) / (2 * t)
    print(f"    P(X)   = a_0^2 [ (t/2)sqrt(1+4t^2) + (1/4)asinh(2t) - t ],  t = sqrt(X)/a_0")
    print(f"    dP/dX  = {dP}")
    check(sp.simplify(dP - mu_of_t) == 0, "dP/dX = mu(sqrt(X)/a_0) IDENTICALLY -- P is the AQUAL function")

    sub("S2d  limits of P: Bekenstein-Milgrom deep-MOND recovered, Newtonian recovered")
    ser = sp.series(P_expr.subs(Xs, (a0s * sp.Symbol('tt', positive=True)) ** 2),
                    sp.Symbol('tt', positive=True), 0, 6).removeO()
    lead = sp.simplify(sp.limit(P_expr / (sp.Rational(2, 3) * Xs ** sp.Rational(3, 2) / a0s), Xs, 0))
    print(f"    small-t series of P/a_0^2 : {sp.simplify(ser / a0s**2)}")
    print(f"    P / [(2/3) X^{{3/2}}/a_0]  ->  {lead}  as X -> 0")
    check(sp.simplify(lead - 1) == 0,
          "deep limit P -> (2/3)|grad phi|^3/a_0 = BEKENSTEIN-MILGROM's deep-MOND Lagrangian, RECOVERED")
    newt = sp.simplify(sp.limit(P_expr / Xs, Xs, sp.oo))
    check(sp.simplify(newt - 1) == 0, "Newtonian limit P -> X = |grad phi|^2, RECOVERED")
    # explicit subleading Newtonian structure (a_0 = 1 for legibility; restore by t -> sqrt(X)/a_0)
    big = sp.Symbol('T', positive=True)
    Pbig = sp.series(P_expr.subs({Xs: big ** 2, a0s: 1}).rewrite(sp.log), big, sp.oo, 2)
    print(f"    large-t form of P/a_0^2 (a_0 = 1) : {sp.simplify(Pbig)}")
    print(f"    i.e. P -> X - a_0 sqrt(X) + (a_0^2/4) ln(4 sqrt(X)/a_0) + a_0^2/8 : the -a_0 sqrt(X) piece is"
          f" the MOND tail on top of Newton")

    sub("S2e  NC4 (negative control): drop the asinh term, the deep limit must break")
    tt = np.logspace(-6, -3, 7)
    Xn = (tt * A0_CANON) ** 2
    good = P_static(Xn, A0_CANON) / (2.0 / 3.0 * Xn ** 1.5 / A0_CANON)
    bad = P_static_broken(Xn, A0_CANON) / (2.0 / 3.0 * Xn ** 1.5 / A0_CANON)
    print(f"    P/[(2/3)X^3/2/a0]  correct: {good[-1]:.12f}      asinh-dropped: {bad[-1]:.10f}")
    # the approach to the deep limit is not free: it is 1 - (3/5)t^2 + (6/7)t^4 + O(t^6).  Measure the
    # coefficient where the subtraction is well conditioned (t = 1e-3, 1e-2: 1-ratio is 6e-7 and 6e-5, so the
    # float64 noise floor is 1e-16/6e-7 ~ 2e-10, not the 1e-4 it would be at t = 1e-6).
    for tprobe in (1e-3, 1e-2):
        Xp = (tprobe * A0_CANON) ** 2
        ratio = float(P_static(Xp, A0_CANON) / (2.0 / 3.0 * Xp ** 1.5 / A0_CANON))
        meas = (1.0 - ratio) / tprobe ** 2
        pred = 0.6 - (6.0 / 7.0) * tprobe ** 2 + (5.0 / 3.0) * tprobe ** 4
        print(f"    t = {tprobe:.0e}: (1 - P/deep)/t^2 measured {meas:.12f} , predicted"
              f" 3/5 - (6/7)t^2 + (5/3)t^4 = {pred:.12f} , diff {meas-pred:+.2e}")
        check(abs(meas - pred) < 1e-10,
              f"at t = {tprobe:.0e} the approach to the deep limit follows the exact series"
              f" 1 - (3/5)t^2 + (6/7)t^4 - (5/3)t^6 to {abs(meas-pred):.1e}: BEKENSTEIN-MILGROM's deep-MOND"
              f" Lagrangian AND its first two corrections")
    check(np.abs(bad[-1] - 1.0) > 0.4, f"NC4 TRIPPED: asinh-dropped P misses the deep limit by "
                                       f"{abs(bad[-1]-1)*100:.1f}% -- the check above can fail")

    sub("S2f  float64 hazards DEMONSTRATED against mpmath: two distinct cancellations")
    if HAVE_MP:
        xh = 1e-9
        exact = mp.mpf(2) * mp.mpf(xh) / (mp.sqrt(1 + 4 * mp.mpf(xh) ** 2) + 1)
        e_stable = abs(float(mu_stable(xh)) / float(exact) - 1.0)
        e_naive = abs(float(mu_naive(xh)) / float(exact) - 1.0)
        print(f"    (i) mu at x = {xh:.0e}:  stable rel err = {e_stable:.3e} ,  naive rel err = {e_naive:.3e}")
        check(e_stable < 1e-15, f"stable mu is exact to {e_stable:.2e} vs mpmath at 50 dps")
        check(e_naive > 1e4 * max(e_stable, 1e-17),
              f"and the naive form really does lose it ({e_naive:.2e}): hazard demonstrated, not asserted")
        # HAZARD NINE: the closed form for P itself cancels to O(t^3) out of three O(t) pieces
        th = 1e-6
        Xh = (th * A0_CANON) ** 2
        tm = mp.mpf(th)
        P_exact = mp.mpf(A0_CANON) ** 2 * (tm / 2 * mp.sqrt(1 + 4 * tm ** 2) + mp.asinh(2 * tm) / 4 - tm)
        e_P_closed = abs(float(P_closed(Xh, A0_CANON)) / float(P_exact) - 1.0)
        e_P_series = abs(float(P_static(Xh, A0_CANON)) / float(P_exact) - 1.0)
        print(f"    (ii) P at t = {th:.0e}: closed-form rel err = {e_P_closed:.3e} ,"
              f" deep-series rel err = {e_P_series:.3e}")
        check(e_P_closed > 1e-6,
              f"HAZARD NINE CONFIRMED: the closed form for P loses {e_P_closed:.2e} at t = 1e-6 (three O(t)"
              f" terms cancelling to O(t^3)) -- a real trap, not a hypothetical one")
        check(e_P_series < 1e-14,
              f"the cancellation-free deep series fixes it ({e_P_series:.2e}), and every P evaluation below"
              f" uses it")
    else:                                                                # pragma: no cover
        check(False, "mpmath unavailable -- the float64 hazard checks could not be run")

    sub("S2g  REFINEMENT: numerical dP/dX vs mu, in float64 and at 50 dps, at h and h/4 and on a 4x grid")
    errs = {}
    for N, hf in ((200, 1e-5), (800, 1e-5), (800, 2.5e-6)):
        tg = np.logspace(-3, 3, N)
        Xg = (tg * A0_CANON) ** 2
        h = hf * Xg
        dnum = (P_static(Xg + h, A0_CANON) - P_static(Xg - h, A0_CANON)) / (2 * h)
        errs[(N, hf)] = float(np.max(np.abs(dnum / mu_stable(tg) - 1.0)))
        print(f"    float64  N = {N:4d}, h = {hf:.1e} X : max |dP/dX / mu - 1| = {errs[(N, hf)]:.3e}")
    print(f"    refinement shifts: 4x grid {errs[(800,1e-5)] - errs[(200,1e-5)]:+.2e} ,"
          f" h/4 {errs[(800,2.5e-6)] - errs[(800,1e-5)]:+.2e}")
    check(max(errs.values()) < 1e-8,
          f"float64 dP/dX reproduces mu to {max(errs.values()):.1e} at every resolution and step")
    if HAVE_MP:
        def P_mp(t):
            t = mp.mpf(t)
            return t / 2 * mp.sqrt(1 + 4 * t ** 2) + mp.asinh(2 * t) / 4 - t          # in units of a_0^2

        mp_errs = {}
        for hf in (mp.mpf('1e-12'), mp.mpf('2.5e-13')):
            worst = mp.mpf(0)
            for t in ('1e-6', '1e-3', '0.12', '1', '1e3'):
                tm = mp.mpf(t)
                Xm = tm ** 2
                d = (P_mp(mp.sqrt(Xm + hf * Xm)) - P_mp(mp.sqrt(Xm - hf * Xm))) / (2 * hf * Xm)
                ex = 2 * tm / (mp.sqrt(1 + 4 * tm ** 2) + 1)
                worst = max(worst, abs(d / ex - 1))
            mp_errs[hf] = worst
            print(f"    50 dps  h = {mp.nstr(hf, 2)} X : max |dP/dX / mu - 1| = {mp.nstr(worst, 3)}")
        shift = mp_errs[mp.mpf('2.5e-13')] - mp_errs[mp.mpf('1e-12')]
        print(f"    refinement shift (h/4, 50 dps): {mp.nstr(shift, 3)}  (2nd-order central difference:"
              f" expect ~1/16)")
        check(max(mp_errs.values()) < mp.mpf('1e-20'),
              f"at 50 dps, cancellation-free, dP/dX = mu to {mp.nstr(max(mp_errs.values()), 2)}: the identity is"
              f" exact and the float64 residual above is purely the step, not the algebra")

    sub("S2h  DIMENSIONAL-RESCALING reproduction check (the class that caught a real bug in this project)")
    lam = A0_ALT / A0_CANON                                              # the ALT footing IS a rescaling
    tg = np.logspace(-4, 4, 33)
    Pc_ = P_static((tg * A0_CANON) ** 2, A0_CANON)
    Pa_ = P_static((tg * A0_ALT) ** 2, A0_ALT)
    dev = float(np.max(np.abs(Pa_ / (lam ** 2 * Pc_) - 1.0)))
    print(f"    a_0 -> {lam:.4f} a_0 with X -> {lam**2:.4f} X :  max |P_alt/(lam^2 P_can) - 1| = {dev:.3e}")
    check(dev < 1e-12,
          f"P(lam^2 X; lam a_0) = lam^2 P(X; a_0) to {dev:.1e}: the ALT footing is a PURE RESCALING of the lane")
    return P_expr, Xs, a0s


# ==================================================================================================
def S3_admissibility():
    banner("S3 -- IS THE REQUIRED P ADMISSIBLE?  Spacelike (MOND) branch: ghost, gradient, sound speed.")

    print("""
    Perturbations delta about a SPACELIKE background (grad phibar != 0, phidot = 0), W = -X:
        L_2 = P'(W) [ deltadot^2/c^2 - |grad delta|^2 ] + 2 P''(W) (grad phibar . grad delta)^2
            = P' deltadot^2/c^2 - [ P' d_ij - 2 P'' d_i phibar d_j phibar ] d_i delta d_j delta
    time-kinetic norm      = P'  = mu                                  (no ghost <=> mu > 0)
    transverse stiffness   = P'  = mu                                  (>0)
    longitudinal stiffness = P' - 2 P'' X = mu + x mu' = d(x mu)/dx     (>0 <=> elliptic AQUAL)
    longitudinal speed     c_s^2 = d(x mu)/dx / mu.
    NOTE the inversion relative to the familiar timelike-background formula c_s^2 = P'/(P'+2WP''): with a
    SPACELIKE background gradient the P'' enhancement lands in the SPATIAL longitudinal direction, so the
    ratio flips.  Getting this backwards would have reported c_s^2 = 1/2 instead of 2.
    """)

    xs = sp.Symbol('x', positive=True)
    mu = (sp.sqrt(1 + 4 * xs ** 2) - 1) / (2 * xs)
    xmu = sp.simplify(xs * mu)
    dxmu = sp.simplify(sp.diff(xmu, xs))
    cs2 = sp.simplify(dxmu / mu)
    print(f"    x mu(x)      = {xmu}")
    print(f"    d(x mu)/dx   = {dxmu}")
    print(f"    c_s^2(x)     = {cs2}")

    xn = np.logspace(-6, 6, 241)
    mu_n = mu_stable(xn)
    dxmu_n = 2.0 * xn / np.sqrt(1.0 + 4.0 * xn * xn)
    cs2_n = dxmu_n / mu_n
    check(np.all(mu_n > 0), "P' = mu > 0 on 12 decades: NO GHOST on the spacelike branch")
    check(np.all(dxmu_n > 0), "d(x mu)/dx > 0 on 12 decades: elliptic, NO gradient instability (AQUAL well-posed)")
    check(sp.simplify(sp.limit(cs2, xs, 0) - 2) == 0,
          "c_s^2 -> 2 EXACTLY in the deep-MOND limit: the scalar propagates at sqrt(2) c")
    check(sp.limit(cs2, xs, sp.oo) == 1, "c_s^2 -> 1 in the Newtonian limit (from ABOVE)")
    check(np.all(cs2_n > 1.0 - 1e-12) and np.all(cs2_n <= 2.0 + 1e-12),
          f"c_s^2 in (1, 2] everywhere: min {cs2_n.min():.6f}, max {cs2_n.max():.6f} -- SUPERLUMINAL throughout")
    check(np.max(cs2_n) > 1.0 + 1e-6,
          "so subluminality FAILS for this AQUAL branch (a check stated so the failing outcome is the finding)")

    sub("S3b  P''(W) < 0 identically on the spacelike branch => the positivity/analyticity bound is violated")
    Ws = sp.Symbol('W', negative=True)
    a0s = sp.Symbol('a_0', positive=True)
    Pprime_W = ((sp.sqrt(1 + 4 * (-Ws) / a0s ** 2) - 1) / (2 * sp.sqrt(-Ws) / a0s))
    Ppp = sp.simplify(sp.diff(Pprime_W, Ws))
    print(f"    P''(W) = {Ppp}")
    vals = [float(Ppp.subs({Ws: -(w * A0_CANON ** 2), a0s: A0_CANON})) for w in (1e-4, 1e-2, 1.0, 1e2, 1e4)]
    print("    P''(W) sampled at -W/a_0^2 = 1e-4 .. 1e4 : " + ", ".join(f"{v:+.4e}" for v in vals))
    check(all(v < 0 for v in vals),
          "P'' < 0 IDENTICALLY: violates the ADAMS et al. 2006 positivity bound (no Lorentz-invariant UV"
          " completion), and it is the SAME SIGN the S5 theorem turns on -- AGAINST INTEREST")
    # |P''| divergence at the cone, exponent MEASURED not asserted.  In d = -W/a_0^2,
    #     P''(W) = (1 - sqrt(1+4d)) / (4 a_0^2 d^{3/2} sqrt(1+4d))
    # whose numerator cancels to -2d: evaluated at 50 dps, because float64 loses it entirely below d ~ 1e-8.
    if HAVE_MP:
        def Ppp_mp(d, a0):
            d, a0 = mp.mpf(d), mp.mpf(a0)
            return (1 - mp.sqrt(1 + 4 * d)) / (4 * a0 ** 2 * d ** mp.mpf(1.5) * mp.sqrt(1 + 4 * d))
        dgrid = np.logspace(-20, -12, 9)
        Ppp_num = np.array([abs(float(Ppp_mp(d, A0_CANON))) for d in dgrid])
        slope = float(np.polyfit(np.log(dgrid), np.log(Ppp_num), 1)[0])
        f64 = abs(float(Ppp.subs({Ws: -(1e-16 * A0_CANON ** 2), a0s: A0_CANON}))
                  / float(Ppp_mp(1e-16, A0_CANON)) - 1.0)
        print(f"    |P''| at -W/a_0^2 = 1e-20..1e-12 (50 dps): log-log slope = {slope:.10f}"
              f"   (theory -1/2 from P' ~ sqrt(-W))")
        print(f"    float64 relative error in P'' at d = 1e-16: {f64:.3e}  (the same cancellation, tenth"
              f" occurrence)")
        check(abs(slope + 0.5) < 1e-9 and Ppp_num[0] > Ppp_num[-1],
              f"|P''| -> infinity at the light cone as (-W)^(-1/2), measured Puiseux slope {slope:.10f}: P is"
              f" C^1 but NOT C^2 there -- the cusp IS the deep-MOND regime")
        check(f64 > 1e-3,
              f"and float64 alone would have got P'' wrong by {f64:.1e} there: the high-precision evaluation is"
              f" load-bearing, not decoration")
    else:                                                                # pragma: no cover
        check(False, "mpmath unavailable -- the Puiseux-exponent measurement could not be run")


# ==================================================================================================
def S4_attractor():
    banner("S4 -- THE COSMOLOGICAL ATTRACTOR SECTOR.  P'(X_0) = 0, and the corpus's c_s^2 = u/(3u+2).")

    lam, X0, P0 = sp.symbols('lambda X_0 P_0', positive=True)
    Xs = sp.Symbol('X', positive=True)
    us = sp.Symbol('u', nonnegative=True)
    P = P0 + sp.Rational(1, 2) * lam * (Xs - X0) ** 2
    PX, PXX = sp.diff(P, Xs), sp.diff(P, Xs, 2)
    check(sp.simplify(PX.subs(Xs, X0)) == 0, "quadratic P has P'(X_0) = 0: the attractor exists")
    check(sp.simplify(PXX - lam) == 0, "P''(X) = lambda > 0: the no-ghost condition 2 X_0 P'' > 0 holds")
    cs2 = sp.simplify((PX / (PX + 2 * Xs * PXX)).subs(Xs, X0 * (1 + us)))
    print(f"    c_s^2 = P'/(P' + 2 X P'') = {cs2}")
    check(sp.simplify(cs2 - us / (3 * us + 2)) == 0,
          "c_s^2 = u/(3u+2) -- the corpus's committed closed form, RE-DERIVED (0 at the attractor, 1/3 ceiling)")
    check(sp.simplify(cs2 - us / (us + 2)) != 0,
          "NC2 TRIPPED: the historical u/(u+2) slip is NOT equal to it, so the check above can fail")
    check(sp.limit(cs2, us, 0) == 0 and sp.limit(cs2, us, sp.oo) == sp.Rational(1, 3),
          "c_s^2 -> 0 at the attractor and -> 1/3 early: the condensate's exact range [0, 1/3)")

    sub("S4b  the no-ghost condition at a general attractor, on an explicit non-quadratic P")
    # L_2 for a timelike background: (P' + 2 W P'') deltadot^2/c^2 - P' |grad delta|^2.  Verify the coefficient
    # by expanding P(W) to second order in deltadot directly -- not by quoting the formula.
    Wt, dd, pd = sp.symbols('W_0 deltadot phidot', positive=True)
    Pgen = sp.Function('Pcal')
    Wpert = (pd + dd) ** 2                                             # phidot^2/c^2 with c = 1, |grad|=0
    ser = sp.series(Pgen(Wpert), dd, 0, 3).removeO()
    coef = sp.simplify(sp.expand(ser).coeff(dd, 2))
    target = sp.Subs(sp.Derivative(Pgen(wd := sp.Symbol('wd')), wd), wd, pd ** 2).doit() \
        + 2 * pd ** 2 * sp.Subs(sp.Derivative(Pgen(wd), wd, 2), wd, pd ** 2).doit()
    print(f"    coefficient of deltadot^2 in P((phidot+deltadot)^2) : {coef}")
    check(sp.simplify(coef - target) == 0,
          "the time-kinetic norm is P'(W_0) + 2 W_0 P''(W_0), derived by expansion; with P'(W_0) = 0 no-ghost"
          " is exactly P''(W_0) > 0")


# ==================================================================================================
def S5_theorem():
    banner("S5 -- THE DECISIVE TENSION.  Can ONE P do both?  THEOREM T2 and the dichotomy.")

    sub("S5a  the bijection: choosing P below the attractor IS choosing the quasistatic mu")
    print("""
    A quasistatic configuration in the presence of the attractor's phidot_0 is phi = phi_0(t) + psi(x), so
        W = W_0 - eps^2 ,  W_0 = phidot_0^2/c^2 > 0 ,  eps = |grad psi|
    and the AQUAL interpolation function is IDENTICALLY
        m(eps) := P'(W_0 - eps^2) .
    eps -> W_0 - eps^2 maps (0, inf) bijectively onto (-inf, W_0), so P on the whole sub-attractor branch is
    the SAME datum as m on (0, inf).  There is no freedom left to hide in.
    """)
    eps, W0 = sp.symbols('epsilon W_0', positive=True)
    Pf = sp.Function('Pcal')
    wq = sp.Symbol('wq')

    def Pp_of(arg, n=1):
        return sp.Subs(sp.Derivative(Pf(wq), (wq, n)), wq, arg)

    m = Pp_of(W0 - eps ** 2)
    m1 = sp.simplify(sp.diff(m, eps))
    m2 = sp.simplify(sp.diff(m, eps, 2))
    print(f"    m(eps)   = {m}")
    print(f"    m'(eps)  = {m1}")
    print(f"    m''(eps) = {m2}")
    m1_0 = sp.simplify(m1.subs(eps, 0).doit())
    m2_0 = sp.simplify(m2.subs(eps, 0).doit())
    print(f"    m'(0)    = {m1_0}      m''(0) = {m2_0}")
    check(m1_0 == 0, "m'(0) = 0 for any C^2 P (the eps^2 argument kills the linear term)")
    check(sp.simplify(m2_0 - (-2) * Pp_of(W0, 2).doit()) == 0,
          "m''(0) = -2 P''(W_0)  EXACTLY: the curvature of the interpolation function at zero acceleration IS"
          " minus twice the attractor's second derivative -- one equation, two incompatible sign demands")

    sub("S5b  THEOREM T2 -- the sign obstruction, with hypotheses, and instantiated numerically")
    print("""
    THEOREM T2.  Let P be C^2 in a neighbourhood of W_0 > 0 with
        (H1) P'(W_0) = 0                            [cosmological ghost-condensate attractor]
        (H2) P'(W_0) + 2 W_0 P''(W_0) > 0           [positive time-kinetic norm: no ghost]
    Then for the quasistatic interpolation function m(eps) = P'(W_0 - eps^2):
        (C1) m(0) = 0, m'(0) = 0, m''(0) = -2 P''(W_0) < 0, hence m(eps) < 0 for all sufficiently small eps > 0
             -- the scalar force is REPULSIVE in the deep regime;
        (C2) |m(eps)| = P''(W_0) eps^2 + O(eps^4), i.e. the leading power is 2, whereas deep MOND requires
             m = eps/a_0, power 1;
        (C3) since MOND requires m > 0 at observed accelerations, by the intermediate value theorem there is a
             FORCE-REVERSAL scale eps_rev > 0 with m(eps_rev) = 0, and eps_rev = O(sqrt(W_0)).
    Conversely m > 0 and increasing near eps = 0 requires P''< 0 there, which violates (H2).
    ESCAPES, all closed or priced:
        (E1) P not C^2 at W_0 (a |W-W_0|^{1/2} cusp AT the attractor).  Then m ~ +/- c eps, power 1 as MOND
             wants, but P''(W_0^-) = -/+ infinity: the MOND-correct sign gives a time-kinetic norm
             2 W_0 P'' = -infinity, a violent GHOST for every configuration with a spatial gradient.  Priced
             below (S5b-iii).
        (E2) two fields (condensate != MOND scalar).  Then a_0 is not fixed by X_0: no derivation.  This is
             what TeVeS/AeST do, and it is why they carry a_0 as an input.
        (E3) W_0 -> 0 (R << 1).  S5c: the MOND-reproducing P' has a square-root BRANCH POINT at W = 0, so it
             has no real-analytic continuation to W > 0; a_0 becomes an independent scale of P.  No derivation.
    """)
    lam_n, W0_n = 3.7, 1.0
    for name, Ppp_sign in (("no-ghost P''(W_0) = +lambda", +1.0), ("NC3: ghost P''(W_0) = -lambda", -1.0)):
        # concrete quadratic:  P'(W) = Ppp_sign*lam_n*(W - W0_n)  =>  m(eps) = -Ppp_sign*lam_n*eps^2
        ee = np.array([1e-3, 1e-2, 1e-1, 0.3])
        m_vals = Ppp_sign * lam_n * ((W0_n - ee ** 2) - W0_n)
        print(f"    {name:32s} m(eps) at eps = {ee} : " + ", ".join(f"{v:+.3e}" for v in m_vals))
        if Ppp_sign > 0:
            check(np.all(m_vals < 0),
                  "T2(C1) instantiated: the corpus's OWN quadratic P gives m(eps) = -lambda eps^2 < 0 --"
                  " REPULSIVE gravity in galaxies")
            p_fit = np.polyfit(np.log(ee), np.log(-m_vals), 1)[0]
            check(abs(p_fit - 2.0) < 1e-9,
                  f"T2(C2) instantiated: log-log slope of |m| is {p_fit:.9f} = 2, not the MOND power 1")
        else:
            check(np.all(m_vals > 0),
                  "NC3 TRIPPED: flipping the no-ghost hypothesis (H2) flips m > 0, so T2's conclusion is"
                  " hypothesis-dependent and the checks above can fail")

    print("\n    (iii) pricing escape E1, the cusp AT the attractor: P'(W) = +c sqrt(W_0-W) gives m = +c eps")
    # P'' is DIFFERENTIATED here, not asserted: P'(W) = sqrt(W_0 - W) for W < W_0, c = 1.  ELEVENTH float64
    # hazard, met while writing this block: differencing in ABSOLUTE W fails outright, because W_0 - W ~ 1e-12
    # and a step of 1e-16 is below the ulp of W_0 = 1.  The derivative must be taken in the OFFSET variable
    # d = W_0 - W (where dP'/dW = -dP'/dd), which is cancellation-free.
    Pp_d_cusp = lambda d: np.sqrt(d)
    ee = np.array([1e-6, 1e-4, 1e-2])
    dv = ee ** 2
    Wv = W0_n - dv
    hh = 1e-6 * dv
    Ppp_cusp = -(Pp_d_cusp(dv + hh) - Pp_d_cusp(dv - hh)) / (2 * hh)     # numerical dP'/dW = -dP'/dd
    Ppp_absW = (np.sqrt(np.maximum(W0_n - (Wv + 1e-16), 0.0))
                - np.sqrt(np.maximum(W0_n - (Wv - 1e-16), 0.0))) / (2e-16)
    print(f"        absolute-W differencing (the trap) : " + ", ".join(f"{v:+.3e}" for v in Ppp_absW))
    Ppp_exact = -0.5 / ee
    norm = Pp_d_cusp(dv) + 2.0 * Wv * Ppp_cusp                           # time-kinetic norm P' + 2 W P''
    print(f"        numerical P''      at eps = {ee}: " + ", ".join(f"{v:+.6e}" for v in Ppp_cusp))
    print(f"        analytic -1/(2eps) at eps = {ee}: " + ", ".join(f"{v:+.6e}" for v in Ppp_exact))
    print(f"        time-kinetic norm P' + 2 W P'':          " + ", ".join(f"{v:+.3e}" for v in norm))
    check(np.max(np.abs(Ppp_cusp / Ppp_exact - 1.0)) < 1e-9,
          f"the cusp's P'' = -1/(2 eps) is reproduced by offset-variable differentiation to"
          f" {np.max(np.abs(Ppp_cusp/Ppp_exact-1.0)):.1e} (sign and magnitude both derived, not asserted)")
    check(np.max(np.abs(Ppp_absW / Ppp_exact - 1.0)) > 1e-3,
          f"HAZARD ELEVEN CONFIRMED: absolute-W differencing gets the same P'' wrong by"
          f" {np.max(np.abs(Ppp_absW/Ppp_exact-1.0)):.1e} -- the offset variable is load-bearing")
    check(np.all(norm < 0) and abs(norm[0] / norm[-1]) > 1e3,
          "E1 PRICED: the MOND-correct cusp makes the time-kinetic norm NEGATIVE and diverging as eps -> 0"
          f" (ratio {abs(norm[0]/norm[-1]):.1e} over 4 decades of eps) -- the ghost is worst exactly in the"
          " deepest MOND regime")

    sub("S5c  the branch-point obstruction (escape E3): no real-analytic P joins the two regimes")
    dsym = sp.Symbol('d', positive=True)                                 # d = -W/a_0^2 > 0 spacelike
    a0v = sp.Symbol('a_0', positive=True)
    Pp_d = (sp.sqrt(1 + 4 * dsym) - 1) / (2 * sp.sqrt(dsym))             # P'(W) as a function of d
    ser = sp.series(Pp_d, dsym, 0, 2)
    print(f"    P'(W) near the cone, d = -W/a_0^2 :  {sp.simplify(ser)}   (half-integer powers of d)")
    check(sp.simplify(sp.limit(Pp_d / sp.sqrt(dsym), dsym, 0) - 1) == 0,
          "P'(W) ~ sqrt(-W)/a_0 at the light cone: a SQUARE-ROOT branch point, half-integer Puiseux exponent,"
          " so P is not real-analytic at W = 0")
    dPd = sp.simplify(sp.diff(Pp_d, dsym))
    lim = sp.limit(dPd, dsym, 0, '+')
    print(f"    dP'/dd as d -> 0^+  =  {lim}")
    check(lim == sp.oo,
          "|P''| -> infinity at W = 0: P is C^1 but NOT C^2 across the cone, so no real-analytic continuation"
          " into the timelike (cosmological) region exists")
    # the naive continuation is literally imaginary
    val = complex(sp.N(Pp_d.subs(dsym, sp.Symbol('dd')).subs(sp.Symbol('dd'), -1e-3)))
    print(f"    naive continuation to W = +1e-3 a_0^2 (d = -1e-3): P' = {val:.6g}")
    check(abs(val.imag) > 100.0 * abs(val.real),
          "continuing the MOND-reproducing P' across the cone gives a NON-REAL value (|Im| > 100|Re|): the"
          " cosmological branch of P is logically independent of the MOND branch, so a_0 is independent of X_0")

    sub("S5d  THE DICHOTOMY, with R = W_0/a_0^2, and where the corpus's own condensate sits")
    print("""
    R = W_0/a_0^2 = (phidot_0/(c a_0))^2 is the ONE dimensionless number that decides the lane.
        R >~ 1 : the static field probes the attractor over the observed range.  a_0 IS then fixed by X_0,
                 which is fixed by rho_Lambda -- the derivation the lane was sent to find -- but T2 applies and
                 MOND fails structurally (repulsive, power 2, no flat rotation curves).
        R << 1 : the static field probes the light cone, AQUAL works with the S2 closed form, but by S5c a_0 is
                 a NEW independent scale of P and the attractor tells you nothing about it.  No derivation.
    The corpus's own banked attractor rate (mi_cosmo_perturbations_2026.py S1e/R2) is phidot_0 = a_0/c for a
    DIMENSIONLESS field; in the AQUAL potential normalisation phi_pot = c^2 phi_dimless (gravitational-strength
    conformal coupling, which is what MOND REQUIRES since the scalar must supply the whole anomalous force)
    that is phidot_0/c = a_0 EXACTLY, so R = 1.  The corpus's own condensate sits at the WORST point of the
    dichotomy: the force reversal of T2(C3) lands at g_obs ~ a_0, in the middle of the measured range.
    """)
    phidot_dimless = A0_CANON / C_LIGHT
    for name, a0 in FOOTINGS:
        eps_c = C_LIGHT * (a0 / C_LIGHT)                                 # phi_pot normalisation: c * phidot_dim
        print(f"    {name:36s} phidot_0 = {a0/C_LIGHT:.6e} s^-1 -> eps_c = {eps_c:.6e} m/s^2, "
              f"R = {(eps_c/a0)**2:.6f}")
    check(abs(phidot_dimless / 3.1228e-19 - 1.0) < 2e-3,
          f"the corpus's banked attractor rate a_0/c = {phidot_dimless:.6e} s^-1 is reproduced (3.1228e-19)")
    # derive phidot from the framework's OWN chain (kappa M^2/M_Pl = kappa sqrt(G rho_Lambda)), not from a_0/c,
    # so this check fails if the footing chain is inconsistent rather than passing by construction
    phidot_chain = KAPPA * math.sqrt(G_NEWT * RHO_LAMBDA)
    R_corpus = (C_LIGHT * phidot_chain / A0_CANON) ** 2
    print(f"    phidot from kappa sqrt(G rho_Lambda) = {phidot_chain:.6e} s^-1  =>  R = {R_corpus:.6f}")
    check(abs(R_corpus - 1.0) < 1e-3,
          f"R = {R_corpus:.6f} = 1 on the corpus's own normalisation, derived through kappa sqrt(G rho_Lambda):"
          f" the pathology sits AT the observed a_0 scale")

    sub("S5e  AGAINST MY OWN FRAMING: even the R >~ 1 branch does NOT fix a_0 -- it is P''(W_0), not W_0")
    lamq, W0q, epsq = sp.symbols('lambda W_0 epsilon', positive=True)
    m_quad = lamq * ((W0q - epsq ** 2) - W0q)                            # P'(W) = lambda (W - W_0)
    cross = sp.solve(sp.Eq(-m_quad, 1), epsq)
    cross = [c for c in cross if sp.simplify(c.subs(lamq, 1)) > 0][0]
    print(f"    |m(eps)| = 1 (the Newtonian crossover) at eps = {cross}")
    check(sp.simplify(sp.diff(cross, W0q)) == 0,
          "the crossover acceleration of the power-2 branch is 1/sqrt(P''(W_0)) and is INDEPENDENT of W_0:"
          " d(eps_cross)/dW_0 = 0 identically")
    print("""
    So the sentence 'a_0 would then be fixed by X_0, which is fixed by rho_Lambda' is TOO GENEROUS and I
    withdraw it: in the attractor-probing branch the acceleration scale is set by the SECOND DERIVATIVE
    P''(W_0) = lambda -- an independent parameter of P, which in the corpus's own background solution is tied
    to the dark-matter AMOUNT, itself banked as FREE (mi_cosmo_perturbations_2026.py: "amount I_0 ~ Omega_dm
    robustly FREE").  W_0 sets only WHERE the T2(C3) force reversal sits, not where the MOND crossover sits.
    NET EFFECT: a_0 is not fixed by rho_Lambda in EITHER branch, for two DIFFERENT reasons -- P''(W_0) free in
    the R >~ 1 branch, a separate light-cone scale in the R << 1 branch.  The no-go is stronger than the
    dichotomy as I first stated it, and this correction cuts against the lane's hoped-for result.
    """)
    print("""
    HONEST CAVEAT, stated because it is load-bearing: R is set by the matter coupling, which the framework does
    not derive, so R = 1 is the corpus's own natural choice and not a theorem.  But the dichotomy covers EVERY
    R > 0, so the conclusion does not depend on it -- and after S5e the R >~ 1 branch does not even buy a_0, so
    the two branches fail for two independent reasons rather than trading off against each other.
    """)


# ==================================================================================================
def S6_consequences():
    banner("S6 -- CONSEQUENCES OF THE R >~ 1 BRANCH: what a power-2 interpolation function predicts.")

    gobs, gbar, Cc, rr, GM = sp.symbols('g_obs g_bar C r GM', positive=True)
    sol = sp.solve(sp.Eq(Cc * gobs ** 2 * gobs, gbar), gobs)[0]
    print(f"    m = C g_obs^2 (power 2)  =>  g_obs = {sol}   i.e. g_obs ~ g_bar^(1/3)")
    check(sp.simplify(sp.log(sol.subs({gbar: sp.Symbol('B', positive=True) ** 3, Cc: 1}))
                      - sp.log(sp.Symbol('B', positive=True))) == 0,
          "the power-2 branch gives g_obs proportional to g_bar^(1/3) exactly")
    v2 = sp.simplify(rr * sol.subs(gbar, GM / rr ** 2))
    print(f"    v^2 = r g_obs = {v2}  =>  v ~ r^(1/6): rotation curves RISE forever, no flat part, no BTFR")
    slope = sp.simplify(sp.limit(sp.log(v2.subs({GM: 1, Cc: 1})) / sp.log(rr), rr, sp.oo))
    check(sp.simplify(slope - sp.Rational(1, 3)) == 0,
          f"d ln v^2/d ln r = 1/3 (v ~ r^(1/6)): FLAT ROTATION CURVES ARE LOST, so this branch is excluded by"
          f" the data the framework is built on")

    sub("S6b  quantify: the shape distance of the power-2 branch from the framework's own kernel, in dex")
    # power-2 branch:  m = C x^2, s = m x = C x^3 -> nu = x/s = C^{-1/3} s^{-2/3}; normalise at y = 1
    for lo, hi in ((1e-2, 1e2), (1e-1, 1e1)):
        yg = np.logspace(math.log10(lo), math.log10(hi), 4001)
        nu_p2 = math.sqrt(2.0) * yg ** (-2.0 / 3.0)
        d = np.abs(np.log10(nu_p2 / nu_framework(yg)))
        print(f"    y in [{lo:g}, {hi:g}]: max |dex| distance of the power-2 kernel from nu = {d.max():.4f} dex"
              f"  ({d.max()/SHAPE_SYST_DEX:.1f}x the corpus's 30.6% = {SHAPE_SYST_DEX:.4f} dex systematic)")
    yg = np.logspace(-2, 2, 4001)
    dmax = float(np.max(np.abs(np.log10(math.sqrt(2.0) * yg ** (-2.0 / 3.0) / nu_framework(yg)))))
    check(dmax > 10.0 * SHAPE_SYST_DEX,
          f"the power-2 branch is {dmax:.3f} dex away = {dmax/SHAPE_SYST_DEX:.1f}x the shape systematic:"
          f" observationally DEAD, not merely disfavoured")


# ==================================================================================================
def S7_predictions():
    banner("S7 -- INDEPENDENT PREDICTIONS (mandatory) and both footings.")

    sub("S7a  the surviving branch's signature: an explicit admissible m with BOTH scales, and its reversal")
    print("""
    An explicit interpolation function satisfying every hypothesis of T2 AND reproducing MOND above eps_c:
        m(eps) = mu_fw(eps/a_0) * eps (eps - eps_c)/(eps^2 + eps_c^2)
    has m(0) = m'(0) = 0, m''(0) = -2/(a_0 eps_c) < 0 (so P''(W_0) = +1/(a_0 eps_c) > 0, no ghost), m < 0 for
    eps < eps_c, m(eps_c) = 0 (the T2(C3) reversal), and m/mu_fw = 1 - eps_c/eps + O((eps_c/eps)^2).
    PREDICTION: a MOND-force SUPPRESSION of exactly eps_c/eps at low acceleration and a FORCE REVERSAL below
    g_obs = eps_c.  Demanding <10% suppression at the lowest measured acceleration bounds eps_c, and that bound
    is quoted BOTH WAYS in S7a2 (conservative eps_c <= 1e-2 a_0, aggressive 1e-3 a_0), i.e. R <= 1e-4 to 1e-6 --
    four to six orders BELOW the corpus's own R = 1.
    """)
    a0 = A0_CANON
    eps_c = 1e-3 * a0
    e = np.logspace(-5, 3, 4001) * a0
    m = mu_stable(e / a0) * e * (e - eps_c) / (e ** 2 + eps_c ** 2)
    m_of = lambda ep: mu_stable(ep / a0) * ep * (ep - eps_c) / (ep ** 2 + eps_c ** 2)
    hh = 1e-6 * eps_c
    m2_num = (m_of(hh) - 2.0 * 0.0 + m_of(-hh) if False else (m_of(hh) + m_of(hh)) / hh ** 2 * 0.0)
    m2_num = 2.0 * m_of(hh) / hh ** 2                                    # m(0)=m'(0)=0 => m ~ m''(0) eps^2/2
    m2_0 = -2.0 / (a0 * eps_c)
    print(f"    m''(0): numerical 2 m(h)/h^2 = {m2_num:.6e} , analytic -2/(a_0 eps_c) = {m2_0:.6e}")
    check(abs(m2_num / m2_0 - 1.0) < 1e-5 and m2_num < 0,
          f"m''(0) = -2/(a_0 eps_c) reproduced numerically to {abs(m2_num/m2_0-1.0):.1e} and NEGATIVE, so"
          f" P''(W_0) = +1/(a_0 eps_c) > 0: no-ghost SATISFIED by this explicit m")
    check(np.all(m[e < 0.9 * eps_c] < 0), "m < 0 below eps_c: the T2(C3) reversal is explicit, not hypothetical")
    check(np.all(m[e > 1.2 * eps_c] > 0), "m > 0 above eps_c: MOND is recovered there")
    mu_fw = mu_stable(e / a0)
    ratio = np.where(np.abs(m) > 0, m, 0.0) / mu_fw
    exact_fac = e * (e - eps_c) / (e ** 2 + eps_c ** 2)
    i10 = int(np.argmin(np.abs(e / a0 - 1e-2)))
    z = eps_c / e[i10]
    print(f"    suppression at g_obs = 1e-2 a_0 with eps_c = 1e-3 a_0 : m/mu_fw = {ratio[i10]:.6f} ,"
          f" 1 - eps_c/g = {1.0-z:.6f} , (eps_c/g)^2 = {z*z:.2e}")
    # absolute comparison (m vanishes at eps_c, so no ratio there)
    dev_abs = float(np.max(np.abs(m - mu_fw * exact_fac)) / np.max(np.abs(m)))
    check(dev_abs < 1e-14,
          f"the suppression factor is EXACTLY eps(eps-eps_c)/(eps^2+eps_c^2): max |m - mu_fw x factor| /"
          f" max|m| = {dev_abs:.1e} over 8 decades")
    check(abs(ratio[i10] - (1.0 - z)) < 2.0 * z * z,
          f"and its expansion is 1 - eps_c/g_obs + O((eps_c/g_obs)^2): residual"
          f" {abs(ratio[i10]-(1-z)):.2e} <= 2 (eps_c/g)^2 = {2*z*z:.2e}")
    sub("S7a2  the bound BOTH WAYS -- do not truncate the systematic at its tight end")
    print("""
    The bound on eps_c depends on how deep the rotation-curve data really reach in g_obs (not g_bar).  Both
    ends of that range are reported, and the CONSERVATIVE end is the headline:
        g_obs,min = 1e-1 a_0  (the bulk of SPARC's outermost points)   -> eps_c <= 1e-2 a_0   [CONSERVATIVE]
        g_obs,min = 1e-2 a_0  (the deepest dwarf/outer points believed) -> eps_c <= 1e-3 a_0   [aggressive]
    """)
    for name, a0f in FOOTINGS:
        print(f"    {name:36s} reversal predicted below g_obs = {1e-2*a0f:.4e} (conservative) to"
              f" {1e-3*a0f:.4e} m/s^2 (aggressive); = {a0f:.4e} at the corpus's own R = 1")
    sup = []
    for gmin_rel, ec_rel in ((1e-1, 1e-2), (1e-2, 1e-3)):
        gm, ec = gmin_rel * a0, ec_rel * a0
        fac = gm * (gm - ec) / (gm ** 2 + ec ** 2)
        sup.append(1.0 - fac)
        print(f"    g_obs,min = {gmin_rel:.0e} a_0 with eps_c = {ec_rel:.0e} a_0 : force suppression"
              f" {100*(1-fac):.2f}%")
    check(all(0.10 <= s <= 0.12 for s in sup),
          f"both ends of the range really do deliver the stated ~10% suppression at their g_min"
          f" ({100*sup[0]:.2f}% and {100*sup[1]:.2f}%): the bound is the 10% criterion, not a fitted number")

    sub("S7b  the SHAPE prediction: distance of the reconstructed P's kernel from nu and from McGaugh 2008 11a")
    res = {}
    for N in (2001, 8001):
        yg = np.logspace(-4, 4, N)
        d = np.abs(np.log10(nu_mcgaugh(yg) / nu_framework(yg)))
        res[N] = (float(d.max()), float(yg[int(np.argmax(d))]))
        print(f"    N = {N:5d}: max |dex| between nu = sqrt(1+1/y) and McGaugh 11a = {res[N][0]:.5f} dex"
              f" at y = {res[N][1]:.4f}")
    shift = res[8001][0] - res[2001][0]
    print(f"    REFINEMENT shift (4x grid): {shift:+.2e} dex")
    check(abs(shift) < 1e-4, f"the max-dex scan is grid-converged (shift {shift:+.1e} dex under 4x refinement)")
    check(res[8001][0] < SHAPE_SYST_DEX,
          f"framework nu vs McGaugh 11a = {res[8001][0]:.4f} dex < the 30.6% = {SHAPE_SYST_DEX:.4f} dex shape"
          f" systematic: the R << 1 branch's shape prediction is NOT currently distinguishable")
    print(f"    By construction the surviving branch's kernel IS nu = sqrt(1+1/y) above eps_c (distance 0 dex);"
          f"\n    its ONLY shape signature is the 1 - eps_c/g_obs low-acceleration suppression of S7a.")

    sub("S7c  the AQUAL Lagrangian scale in dark-energy units: an exact relabelling identity, both footings")
    kap, rho, cc, Gg = sp.symbols('kappa rho c G', positive=True)
    a0_sym = kap * cc * sp.sqrt(Gg * rho)
    ident = sp.simplify(a0_sym ** 2 / (8 * sp.pi * Gg) / (rho * cc ** 2))
    print(f"    [a_0^2/(8 pi G)] / (rho_Lambda c^2) = {ident}")
    check(sp.simplify(ident - kap ** 2 / (8 * sp.pi)) == 0,
          "the AQUAL Lagrangian scale a_0^2/(8 pi G) is EXACTLY kappa^2/(8 pi) of the dark-energy density")
    for name, a0f in FOOTINGS:
        K = a0f ** 2 / (8.0 * math.pi * G_NEWT)
        kap_f = a0f / (C_LIGHT * math.sqrt(G_NEWT * RHO_LAMBDA))
        print(f"    {name:36s} K = {K:.5e} J/m^3 , K/(rho_L c^2) = {K/(RHO_LAMBDA*C_LIGHT**2):.5e}"
              f" , kappa^2/8pi = {kap_f**2/(8*math.pi):.5e}")
    check(abs((A0_CANON ** 2 / (8 * math.pi * G_NEWT)) / (RHO_LAMBDA * C_LIGHT ** 2)
              / (KAPPA ** 2 / (8 * math.pi)) - 1.0) < 1e-3,
          "numerically: K/(rho_Lambda c^2) = kappa^2/8pi = 9.947e-3 canonical (1.449e-2 ALT) -- a RELABELLING"
          " (kappa <-> Lagrangian scale), which by the corpus's kappa-linear theorem can never FORCE kappa")


# ==================================================================================================
def main() -> int:
    print(__doc__)
    S0_footing()
    S1_reduction()
    S2_reconstruct()
    S3_admissibility()
    S4_attractor()
    S5_theorem()
    S6_consequences()
    S7_predictions()

    banner("VERDICT -- LANE T2")
    print("""
    1. The reduction is real: shift-symmetric L = P(W) with a matter source IS AQUAL at tree level, with the
       interpolation function mu = P'(W).  Verified symbolically (S1a), with a negative control (S1b).
    2. The P that reproduces the framework's OWN kernel nu = sqrt(1+1/y) is closed-form,
       P(X) = a_0^2[(t/2)sqrt(1+4t^2) + (1/4)asinh(2t) - t], t = sqrt(X)/a_0.  Its deep limit is
       Bekenstein-Milgrom's (2/3)|grad phi|^3/a_0, RECOVERED not assumed (S2d).
    3. It is admissible on the spacelike branch -- no ghost, elliptic -- but P'' < 0 identically and the
       longitudinal speed of the COVARIANT completion is c_s^2 in (1,2], EXACTLY 2 in the deep-MOND limit:
       superluminal everywhere, and the ADAMS et al. positivity bound violated.  AGAINST INTEREST (S3).
    4. THE ANSWER TO THE LANE'S QUESTION IS NO.  Theorem T2: no C^2 P with a ghost-free timelike attractor can
       give a positive, linear deep-MOND interpolation function for quasistatic perturbations about that
       attractor.  m''(0) = -2 P''(W_0), and the two requirements fix that sign oppositely.  All three escapes
       are closed or priced (cusp => diverging ghost; two fields => a_0 an input; W_0 -> 0 => a square-root
       branch point at the cone, so a_0 is an independent scale).
    5. a_0 is NOT derived, in EITHER branch and for two different reasons: P''(W_0) -- not W_0 -- sets the
       crossover in the attractor-probing branch (S5e, a correction AGAINST the lane's own hoped-for result),
       and a separate light-cone scale sets it in the other.  kappa REMAINS FITTED.  On the corpus's own banked
       normalisation R = 1 and the force reversal lands at g_obs ~ a_0.
    6. INDEPENDENT PREDICTIONS: (i) the attractor-probing branch predicts g_obs ~ g_bar^(1/3), v ~ r^(1/6), no
       flat rotation curves, a shape 1.185 dex from nu = 10.2x the 30.6% shape systematic -- dead; (ii) ANY
       condensate-generated MOND predicts a low-acceleration force suppression 1 - eps_c/g_obs and a FORCE
       REVERSAL below g_obs = eps_c, with eps_c <= 1e-2 a_0 = 9.4e-13 (canonical) / 1.1e-12 (ALT) m/s^2 on the
       conservative reading of how deep rotation curves reach, 1e-3 a_0 on the aggressive one; (iii) c_s^2 = 2
       deep => the MOND branch has no Lorentz-invariant, unitary UV completion.
    7. Framework nu vs McGaugh 2008 11a is 0.0571 dex max (at y = 0.387), INSIDE the 0.1159 dex (30.6%) shape
       systematic: a measured shape cannot currently separate them, so prediction (ii) -- an outer-galaxy force
       DEFICIT growing as 1/g_obs -- is the only live handle this lane produces.
    """)
    n_ok = sum(1 for ok, _ in _RESULTS if ok)
    n = len(_RESULTS)
    for ok, msg in _RESULTS:
        if not ok:
            print("  FAILED: " + msg)
    print(f"\n{n_ok}/{n} checks held.")
    return 0 if n_ok == n else 1


if __name__ == "__main__":
    sys.exit(main())
