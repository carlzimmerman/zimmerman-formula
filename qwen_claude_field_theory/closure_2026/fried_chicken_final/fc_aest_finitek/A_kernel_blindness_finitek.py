#!/usr/bin/env python3
r"""
A_kernel_blindness_finitek.py
==============================================================================
STEP 1 of FC-FK route-A: VERIFY (do not assume) that the frozen MOND kernel
    F(Y,Q) = F_Q^star(Q) + a0^2 J_10( sqrt(Y)/a0 ) ,   a0 = const
is BLIND at quadratic order on the FLRW background (Ybar=0, Q0=phidot != 0),
so the finite-k scalar spectrum is PURE AeST HOST -- the same object whether the
free function carries J_10, tanh, or any admissible mu_n.

This is Carl's explicit caution: F_YY(0,Q) = (1/(4 a0)) Y^{-1/2} -> infinity in the
Y-CHART.  If that divergence, or an F_YQ / F_QQ cross term, injected a
kernel-DEPENDENT quadratic term, the whole finite-k analysis would be
kernel-specific and the k*-band question would change.  We prove it does NOT, by
four independent certificates, each a printed sympy residual == 0 (or an explicit
non-analytic order count).  If ANY injects a delta^2 term, this script FAILS loudly.

  C1  SEPARABILITY  =>  F_YQ == 0 identically (at EVERY (Y,Q), incl. (0,Q0)).
      The MOND sector and the K(Q) sector cannot mix at any order in perturbations.
  C2  F_M is CUBIC in the physical perturbation:  on Ybar=0, Y = |grad d-phi|^2/a^2
      = O(eps^2), so F_M = a0^2 J_10 = (1/3a0) Y^{3/2} = (1/3a0)|grad d-phi|^3/a^3
      = O(eps^3).  Its SECOND functional derivative at d-phi=0 is 0  => delta^2 F_M = 0.
  C3  The F_YY -> infinity divergence is a COORDINATE (Y-chart) artifact, TAMED by
      the vanishing measure:  F_YY (dY)^2 ~ Y^{-1/2}(Y^2) = Y^{3/2} = O(eps^3).
      Numerically demonstrated: the "quadratic" piece scales as eps^3, not eps^2.
  C4  F_QQ(0,Q0) = -4 K2  is the AeST HOST scalar-mass curvature; it is J_10-FREE
      (d/d[kernel] F_QQ = 0), i.e. the only quadratic curvature is the pure-AeST one.

VERDICT: the quadratic scalar action on FLRW is F_Q^star(Q) + [-(2-K_B)Y analytic
seed], i.e. PURE AeST HOST.  J_10 enters first at O(eps^3) (nonlinear/quasi-static),
exactly where galaxies test it.  The k*-band ghost question is therefore a HOST
question, valid for the whole mu_n family.

Self-contained.  python3 A_kernel_blindness_finitek.py
"""
import sympy as sp

P = print
FAILS = []
def check(label, cond, extra=""):
    ok = bool(cond)
    P(("  [ok]   " if ok else "  [FAIL] ") + label + (("\n         " + extra) if extra else ""))
    if not ok:
        FAILS.append(label)
    return ok
def hdr(s): P("\n" + "=" * 92 + "\n" + s + "\n" + "=" * 92)
def note(t, s): P(f"  [{t}] {s}")

# frozen symbols
Y, Q, Q0, a0, K2, KB = sp.symbols('Y Q Q0 a0 K2 K_B', positive=True)
Lam = sp.symbols('Lambda', positive=True)
eps = sp.symbols('epsilon', positive=True)

hdr("FC-FK route-A  STEP 1  --  kernel-blindness of F = F_Q^star(Q) + a0^2 J_10(sqrt(Y)/a0)")
note("frozen", "mu_10(y)=y/(1+y^10)^(1/10) => J_10(x)=x^3/3+O(x^13) => F_M=a0^2 J_10=(1/3a0)Y^{3/2}")
note("frozen", "F_Q^star(Q)=F(0,Q)=-2K(Q), K(Q)=-2Lambda+K2(Q-Q0)^2  (AeST convention, +4K2 healthy)")

# ---- Build F explicitly as the SUM (separable) --------------------------------
FQstar = -2 * (-2 * Lam + K2 * (Q - Q0) ** 2)             # F(0,Q) = -2 K(Q)
F_M    = Y ** sp.Rational(3, 2) / (3 * a0)                # a0^2 J_10 leading branch (exact small-Y)
F_full = FQstar + F_M                                     # the frozen free function

# ===========================================================================
hdr("C1  SEPARABILITY  =>  F_YQ = 0 identically  (no MOND<->K(Q) mixing at ANY order)")
F_YQ = sp.simplify(sp.diff(F_full, Y, Q))
check("F_YQ = d^2 F/dY dQ = 0 for all (Y,Q)  (F is a SUM F_Q^star(Q) + F_M(Y))",
      sp.simplify(F_YQ) == 0, f"F_YQ = {F_YQ}   -- so the cross term F_YQ dY dQ is ABSENT identically")
# even the mixed third derivatives vanish -> no mixing at cubic order either
F_YYQ = sp.simplify(sp.diff(F_full, Y, Y, Q))
F_YQQ = sp.simplify(sp.diff(F_full, Y, Q, Q))
check("all mixed derivatives F_YYQ = F_YQQ = 0  (separability holds to all orders)",
      F_YYQ == 0 and F_YQQ == 0, f"F_YYQ={F_YYQ}, F_YQQ={F_YQQ}")
note("=>", "the Y (MOND) sector and the Q (K(Q)/dust) sector are DECOUPLED in F.  Any quadratic")
note("=>", "cross-injection is impossible: it would need F_YQ != 0.  [THEOREM by separability]")

# ===========================================================================
hdr("C2  F_M is CUBIC in the physical perturbation  =>  delta^2 F_M = 0")
# On FLRW: Ybar = 0 and delta(Y)_linear = 0 (aether-orthogonal projector kills phidot).
# The FULL perturbation of Y is Y = |grad(d-phi)|^2/a^2 = eps^2 * g2 (g2 = |grad f|^2/a^2).
g2 = sp.symbols('g2', positive=True)                     # = |grad f|^2 / a^2  (O(1))
Y_of_eps = eps ** 2 * g2                                 # physical scaling of Y on Ybar=0
F_M_eps = F_M.subs(Y, Y_of_eps)
F_M_eps = sp.simplify(F_M_eps)
order = sp.simplify(sp.limit(F_M_eps / eps ** 3, eps, 0))
check("F_M(d-phi) = (1/3a0)(eps^2 g2)^{3/2} = (g2^{3/2}/3a0) eps^3  => leading order is eps^3",
      sp.simplify(F_M_eps - g2 ** sp.Rational(3, 2) / (3 * a0) * eps ** 3) == 0,
      f"F_M = {F_M_eps}  ;  lim F_M/eps^3 = {order} (finite, nonzero) => F_M = O(eps^3)")
# second variation = coefficient of eps^2 in F_M(eps) = 0
coeff_eps2 = F_M_eps.coeff(eps, 2)
check("coefficient of eps^2 in F_M = 0  => delta^2 F_M = 0  (kernel invisible at quadratic order)",
      sp.simplify(coeff_eps2) == 0, f"[eps^2] F_M = {coeff_eps2}")
note("=>", "F_M = (1/3a0)|grad(d-phi)|^3/a^3 is a HOMOGENEOUS CUBIC in grad(d-phi): its second")
note("=>", "functional derivative at d-phi=0 vanishes.  The sharp MOND kernel contributes 0 to")
note("=>", "the quadratic (linear-perturbation) action.  [COMPUTATION, exact]")

# ===========================================================================
hdr("C3  the F_YY -> oo divergence is a Y-CHART ARTIFACT, tamed by the vanishing measure")
F_Y  = sp.diff(F_M, Y)
F_YY = sp.simplify(sp.diff(F_M, Y, 2))
sing = sp.limit(F_YY, Y, 0, '+')
check("F_YY = (1/(4 a0)) Y^{-1/2} -> +oo as Y->0  (the chart divergence Carl flagged)",
      F_YY == 1 / (4 * a0) * Y ** sp.Rational(-1, 2) and sing == sp.oo,
      f"F_YY = {F_YY} -> {sing}")
# the would-be quadratic term is (1/2) F_YY (dY)^2 ; but dY is the FULL O(eps^2) perturbation
dY_eps = Y_of_eps                                        # dY = Y - Ybar = eps^2 g2
naive_quadratic = sp.simplify(sp.Rational(1, 2) * F_YY.subs(Y, Y_of_eps) * dY_eps ** 2)
order3 = sp.simplify(sp.limit(naive_quadratic / eps ** 3, eps, 0))
check("(1/2)F_YY (dY)^2 = (1/2)(Y^{-1/2}/4a0)(eps^2 g2)^2 evaluated on Y=eps^2 g2  ~  eps^3  (NOT eps^2)",
      sp.simplify(naive_quadratic - g2 ** sp.Rational(3, 2) / (8 * a0) * eps ** 3) == 0,
      f"(1/2)F_YY(dY)^2 = {naive_quadratic}  ;  /eps^3 -> {order3} => the divergence x measure = O(eps^3)")
note("=>", "Y^{-1/2}(divergent) times (dY)^2 = (eps^2)^2 (vanishing) = eps^3.  The chart singularity")
note("=>", "is EXACTLY cancelled by the physical smallness of dY.  No eps^2 term survives.  This is")
note("=>", "the AQUAL/Legendre non-analyticity, not a dynamical injection.  [COMPUTATION, exact]")

# numeric belt-and-suspenders: measure the exponent
import numpy as np
def quad_piece(e):
    Yv = e ** 2 * 1.0                                    # g2=1
    return 0.5 * (1.0 / (4 * 1.0)) * Yv ** (-0.5) * (Yv) ** 2   # (1/2)F_YY (dY)^2, a0=1
es = np.array([1e-2, 1e-3, 1e-4, 1e-5])
vals = np.array([quad_piece(e) for e in es])
slopes = np.diff(np.log(vals)) / np.diff(np.log(es))    # d ln(piece)/d ln eps
check("numeric exponent of the 'F_YY(dY)^2' piece = 3.000 (a cubic, not a quadratic)",
      np.allclose(slopes, 3.0, atol=1e-9), f"d ln/d ln eps = {slopes} (all = 3)")

# ===========================================================================
hdr("C4  the ONLY quadratic curvature is the HOST F_QQ(0,Q0) = -4 K2  (J_10-free)")
F_QQ = sp.simplify(sp.diff(F_full, Q, 2))
F_QQ_at = sp.simplify(F_QQ.subs(Q, Q0))
check("F_QQ(0,Q) = -4 K2 (constant in Q)  and at the condensate F_QQ(0,Q0) = -4 K2",
      sp.simplify(F_QQ + 4 * K2) == 0 and sp.simplify(F_QQ_at + 4 * K2) == 0,
      f"F_QQ = {F_QQ}  (the physical time-kinetic in -F is +4K2 > 0, HEALTHY)")
# it is manifestly independent of a0/kernel: differentiate wrt a term that only J_10 carries
# encode a generic kernel amplitude 'A' multiplying the MOND branch and show F_QQ is A-free
A = sp.symbols('A', positive=True)
F_withkernel = FQstar + A * Y ** sp.Rational(3, 2) / (3 * a0)
check("d/dA [ F_QQ ] = 0  (the quadratic Q-curvature does not see the MOND kernel amplitude)",
      sp.simplify(sp.diff(sp.diff(F_withkernel, Q, 2), A)) == 0,
      "so F_QQ = -4K2 is a pure-HOST number for the WHOLE mu_n family (J_10, tanh, mu_5, ...)")

# ===========================================================================
hdr("VERDICT  --  STEP 1")
P("""  PROVEN (each a printed residual == 0 or an explicit order count):
   C1  F_YQ == 0 identically (separability) -- NO MOND<->K(Q) mixing at any order.
   C2  F_M = (1/3a0)|grad d-phi|^3/a^3 = O(eps^3) -- delta^2 F_M = 0 (kernel invisible at quad order).
   C3  F_YY ~ Y^{-1/2} -> oo is a Y-CHART artifact: F_YY (dY)^2 = O(eps^3), no eps^2 injection.
   C4  the only quadratic curvature is the HOST F_QQ(0,Q0) = -4 K2, provably J_10-free.

  => the quadratic scalar action on FLRW (Ybar=0, Q0!=0) is
        S^(2) = S^(2)[ -(2-K_B)Y analytic seed ]  +  S^(2)[ F_Q^star(Q) = -2K(Q) ]   (PURE AeST HOST)
     with the sharp kernel J_10 entering first at O(eps^3).  The finite-k / k*-band ghost question
     below is a HOST question -- identical for J_10, mu_5, tanh, any admissible mu_n.  KERNEL-BLIND.""")
P("=" * 92)
nf = len(FAILS)
P(f"CERTIFICATE (STEP 1): {nf} FAIL(s)." + ("  All checks passed." if not nf else ""))
for f in FAILS: P("   FAILED:", f)
import sys
sys.exit(0 if nf == 0 else 1)
