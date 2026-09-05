#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf2_scalar_spin0_regularization.py
==================================
THE LOAD-BEARING DERIVATION.  In AeST the aether spin-0 (longitudinal) mode is
FROZEN at the Einstein-aether Maxwell point (c123 = c1+c2+c3 = 0 => c_S^2 = 0),
and the pure-aether Foster-Jacobson alpha_2 has a SIMPLE POLE ~ 1/c123.  The
scalar phi is supposed to "supply the spin-0 dynamics" and regulate the pole.
QUESTION (the task's dichotomy):
   (1) does the scalar feedback shift the effective spin-0 stiffness to NONZERO,
       so the spin-0 sector is healthy and alpha_2 is FINITE?
   (2) or does it EXACTLY cancel the preferred-frame source (=> alpha_1=alpha_2=0)?

We set up the coupled (aether-longitudinal chi + scalar dphi) QUADRATIC action
from the AeST action, expand, Fourier, and read off the effective spin-0 sector.

CONTEXT (this dir, SOLID):
  * AeST aether kinetic = EA MAXWELL POINT c1=K_B,c3=-K_B,c2=c4=0 => c123=0.
  * pure-aether: c_S^2=0 (frozen spin-0), alpha_2 ~ 1/c123 POLE, alpha_1=-4K_B.
    (wf_ppn_alpha12_maxwellpoint.py, wf_verify_alpha2_maxwell_independent.py)

ACTION (Skordis-Zlosnik, arXiv:2109.13287 = PRD106.104041, Eq.1; defs verbatim
from the paper):
  S = (1/16 pi Gt) \int sqrt(-g)[ R - 2Lam - (K_B/2)F_{mn}F^{mn}
        + 2(2-K_B) J^mu \nabla_mu phi - (2-K_B) Y - F(Y,Q) - lam(A^2+1)] + S_m
  J^mu = A^nu \nabla_nu A^mu (aether accel);  F_{mn}=2\nabla_[m A_n];
  Q = A^mu \nabla_mu phi ;  Y=(g^{mn}+A^mu A^nu)\nabla_mu phi \nabla_nu phi ;
  K(Qb) = -1/2 F(0,Qb) = K2 (Qb-Q0)^2+... ;  dF/dY|bg = (2-K_B) lam_s.
  Minkowski bg: A^mu=(1,0,0,0), phi=Q0 t => Qbar=Q0, Ybar=0.

METHOD: flat space, metric perturbation frozen (this is exactly the SZ21
linear-stability arena; the metric is restored only in the DISCUSSION). The
2-field (chi,dphi) block is validated below by EXACTLY reproducing SZ21's
propagating scalar-mode dispersion c_s^2 [Eq.30] and M^2 [Eq.22].

Every printed line labelled SOLID / SUGGESTIVE / NOT-COMPUTED.  Real sympy.
Run only; do NOT git commit.
"""
import sympy as sp

print("="*84)
print(" wf2  AeST scalar regularization of the frozen aether spin-0 mode (alpha_2)")
print(" action+defs: Skordis-Zlosnik 2109.13287 (PRD106.104041) Eq.(1),(21),(22),(30)")
print("="*84)

KB, lam_s, K2, Q0, k, w, wbar = sp.symbols('K_B lambda_s K2 Q0 k omega wbar', positive=True)
twoKB = 2 - KB

# ===========================================================================
print("\n" + "#"*84)
print("# PART A.  Spin-0 quadratic action, term by term (flat space, metric frozen)")
print("#"*84)
print(r"""
Background A^mu=(1,0,0,0), phi=Q0 t.  Unit constraint (A^0)^2 = 1+V^2 => dA^0 is
2nd order; linear aether d.o.f. = spatial V^i, longitudinal V^i = d^i chi.

Term 1  -(K_B/2)F^2 :  F_{0i}=Vdot_i, F_{ij}=d_iV_j-d_jV_i=0 for V=grad chi.
        F^2 = 2 F_{0i}F^{0i} = -2(grad chi_dot)^2  =>  -(K_B/2)F^2 = +K_B(grad chi_dot)^2.
        => Fourier |chi|^2 coeff:  K_B k^2 w^2.  TIME-kinetic only, NO spatial
        stiffness -> this IS the c_S^2=0 freeze (static self-term vanishes).

Term 2  -(2-K_B)Y.  On this bg, with h^{00}=-1+(A^0)^2=V^2 , h^{0i}=V^i:
        Y = Q0^2 V^2 + 2 Q0 V^i d_i dphi + (grad dphi)^2.
        (2a) -(2-K_B)Q0^2 V^2       : aether MASS   (from h^{00}=V^2)
        (2b) -2(2-K_B)Q0 V.grad dphi: chi--dphi mixing
        (2c) -(2-K_B)(grad dphi)^2  : scalar gradient

Term 3  2(2-K_B)J.grad phi, J^i=Vdot^i :  +2(2-K_B) Vdot^i d_i dphi
        (chi_dot--dphi mixing; the J^0 Q0 piece = (1/2)Q0 d_t V^2 is a total
         time derivative -> dropped)

Term 4  -F(Y,Q):  F(0,Q0)=0, F_Q(0,Q0)=0, F_QQ(0,Q0)=-4K2, F_Y(0,Q0)=(2-K_B)lam_s.
        -F_Y Y  promotes the (2-K_B) in (2a,2b,2c) to (2-K_B)(1+lam_s).
        -(1/2)F_QQ (dQ)^2 = +2 K2 (dphi_dot)^2 : scalar TIME-kinetic (dQ=dphi_dot).
""")

# coefficients (all (2-K_B)(1+lam_s) pieces = 2a,2b,2c after Term-4 F_Y):
m2 = twoKB*(1+lam_s)*Q0**2      # coeff of (V^i)^2   (mass)          [2a]
b  = twoKB*(1+lam_s)*Q0         # coeff of grad chi.grad dphi (-2*?) [2b]
a  = twoKB                      # coeff of grad chi_dot.grad dphi    [T3]
d  = twoKB*(1+lam_s)            # coeff of (grad dphi)^2             [2c]
c  = 2*K2                       # coeff of (dphi_dot)^2              [T4]

print("-"*84)
print("Cross-check MASS coeff vs SZ21 vector mass M^2 [Eq.22]  (independent anchor):")
print("-"*84)
M2_SZ = twoKB*(1+lam_s)*Q0**2/KB
print("   my (V^i)^2 mass coeff  m2 =", m2)
print("   SZ21  K_B*M^2 (Eq.22)     =", sp.simplify(KB*M2_SZ),
      "  MATCH:", sp.simplify(m2-KB*M2_SZ) == 0, " [SOLID]")

# ===========================================================================
print("\n" + "#"*84)
print("# PART B.  The KEY ALGEBRAIC FACT: terms 2a+2b+2c form a PERFECT SQUARE")
print("#"*84)
print(r"""
   -(2-K_B)(1+lam_s)[ Q0^2 V^2 + 2 Q0 V.grad dphi + (grad dphi)^2 ]
 = -(2-K_B)(1+lam_s) ( Q0 V^i + d_i dphi )^2 .
The scalar and the longitudinal aether enter the Y-sector ONLY through the
gauge-invariant combination  ( Q0 V^i + d_i dphi ) = d_i( Q0 chi + dphi ),
i.e. the perturbed SPATIAL GRADIENT OF phi in the aether frame.
""")
print("   algebraic signature of the perfect square:  m2*d - b^2 =",
      sp.simplify(m2*d - b**2), "  (== 0)  [SOLID]")

# Fourier 2x2 inverse propagator.  grad->i k, d_t->-i w.
# off-diagonal real part is NEGATIVE (term 2b enters as -2(2-K_B)(1+lam_s)Q0 grad chi.grad dphi);
# only |M_chidphi|^2=b^2 enters det/c_s^2/M^2, so the sign is physically inert -- fixed here
# just so the static null vector prints as the true flat direction dphi = -Q0 chi.
Mxx = KB*k**2*w**2 - m2*k**2
Mpp = c*w**2      - d*k**2
Mxp = -b*k**2 + sp.I*a*w*k**2
Mpx = sp.conjugate(Mxp)
det = sp.expand(Mxx*Mpp - Mxp*Mpx)
print("\nM_chichi   =", Mxx)
print("M_dphidphi =", Mpp)
print("M_chidphi  =", Mxp)
print("\ndet M(w,k) =", sp.expand(det))
print("   -> every term carries w^2 (the k^4 pieces cancel by m2*d=b^2):")
print("   det/w^2 =", sp.expand(sp.simplify(det/w**2)))

# propagating branch: det/w^2 = 0  -> omega^2 = c_s^2 k^2 + M^2
w2 = sp.symbols('w2', positive=True)
sol = sp.solve(sp.Eq((det/w**2).subs(w**2, w2), 0), w2)[0]
P = sp.Poly(sp.expand(sp.simplify(sol)), k)
cs2 = sp.simplify(P.coeff_monomial(k**2))
M2  = sp.simplify(P.coeff_monomial(1))
cs2_SZ = twoKB/(K2*KB)*(1 + sp.Rational(1,2)*KB*lam_s)   # SZ21 Eq.30
print("\nPROPAGATING spin-0 mode  omega^2 = c_s^2 k^2 + M^2 :")
print("   c_s^2 (derived) =", cs2)
print("   M^2   (derived) =", M2)
print("   c_s^2 - SZ21 Eq.30 =", sp.simplify(cs2 - cs2_SZ),
      " ;  M^2 - SZ21 Eq.22 =", sp.simplify(M2 - M2_SZ))
print("   => EXACT match to SZ21.  The 2-field (chi,dphi) block correctly")
print("      captures the physical spin-0 mode.  [SOLID -- strong validation]")

# ===========================================================================
print("\n" + "#"*84)
print("# PART C.  The naive 'scalar mass stiffens the aether' is FALSE")
print("#"*84)
Mxx0, Mpp0, Mxp0 = Mxx.subs(w,0), Mpp.subs(w,0), Mxp.subs(w,0)
Gchi_inv_static = sp.simplify(Mxx0 - Mxp0*sp.conjugate(Mxp0)/Mpp0)
print("\nStatic (w->0) effective chi inverse propagator (integrate out dphi):")
print("   G_chi^{-1}(w=0) = M_chichi(0) - |M_chidphi(0)|^2/M_dphidphi(0) =",
      Gchi_inv_static, "  [SOLID]")
print("""
   The Q0^2 mass (2a) that the scalar clock injects into the longitudinal aether
   is EXACTLY UNDONE by the chi--dphi mixing (2b,2c): perfect square => the
   STATIC longitudinal-aether stiffness is EXACTLY ZERO, and det(w=0)=0
   (the 2x2 is singular -- a frozen/constraint direction survives).
   => The regularization is NOT "the scalar adds a static stiffness to the
      aether-longitudinal mode."  That naive picture is refuted. [SOLID]
""")
print("   null direction of M(w=0):  M(0).v=0  with v = (chi,dphi) =",
      sp.Matrix([[Mxx0, Mxp0],[Mxp0, Mpp0]]).nullspace()[0].T,
      "  (i.e. dphi = -Q0 chi : the flat direction Q0 chi+dphi->const of Y). [SOLID]")

# ===========================================================================
print("\n" + "#"*84)
print("# PART D.  WHERE the regularization actually lives: massive scalar carrier")
print("#"*84)
print(r"""
The physical spin-0 response is the PROPAGATING mode omega^2 = c_s^2 k^2 + M^2
(matched to SZ21 above).  Its STATIC Green's function is
      G_phys(w=0,k) ~ 1 / ( c_s^2 k^2 + M^2 )      -- FINITE (Yukawa, range 1/M),
whereas pure Einstein-aether had the frozen longitudinal mode giving
      G_EA(w=0,k)  ~ 1 / ( c123 * k^2 )  -> 1/0   -- the alpha_2 POLE.
""")
# show the two Green's functions and the Q0->0 / K2->0 limits
Gphys = 1/(cs2*k**2 + M2)
print("   G_phys(w=0,k) = 1/(c_s^2 k^2 + M^2) =", sp.simplify(Gphys))
print("   finite for K2>0, Q0>0, 0<K_B<2, lam_s>-1.  [SOLID]")
print("   switch the scalar OFF:")
print("     K2 -> oo (no scalar Q-kinetic): c_s^2 -> 0  => G_phys -> 1/M^2 (still finite, pure mass)")
print("     Q0 -> 0 (no clock, M^2->0) AND K2->oo : G_phys -> pole returns.  [SOLID]")
print(r"""
WHY the surviving frozen (null) direction does NOT re-introduce a pole:
on the null direction ( Q0 V + grad dphi ) = 0 AND dphi_dot = dQ = 0, so BOTH
the Y-stress ( ~ (Q0 V+grad dphi)^2 ) and the Q-stress ( ~ Q0 dQ ) VANISH.
=> the frozen direction is STRESS-FREE => it does not couple to the metric and
is not sourced by matter (matter couples only to g_{mn}).  Matter drives only
the healthy massive mode, whose response is finite.
LABEL: SUGGESTIVE-strong (stress-free argument is analytic; the fully rigorous
statement needs the metric+matter PPN carried through -- NOT-COMPUTED here).
""")

# ===========================================================================
print("\n" + "#"*84)
print("# PART E.  alpha_1 (spin-1): the scalar CANNOT do the same job")
print("#"*84)
print(r"""
Scalar phi is SPIN-0.  Its couplings to the TRANSVERSE aether V^i_T (div V_T=0):
   Y-mixing 2 Q0 V^i_T d_i dphi  and  J-mixing 2(2-K_B) Vdot^i_T d_i dphi
both integrate to (div V_T)(...) = 0.  The ONLY scalar effect on the vector
sector is the mass -(2-K_B)(1+lam_s)Q0^2 (V^i_T)^2 [transverse part of h^{00}].
=> No chi-like integrate-out can cancel the spin-1 alpha_1. Different sector. [SOLID]

SZ21 Eq.(21):  S(V) = -1/2 (Vdot+W).grad^2.(Vdot+W)
                     + K_B[ |beta_dot|^2 - grad beta.grad beta - M^2 |beta|^2 ]
states the massive aether transverse beta DECOUPLES from the metric
gravitomagnetic (V,W).  If complete, matter (coupling only to g) never sources
beta => the vector sector gives NO long-range aether preferred-frame potential
=> alpha_1 -> 0 by a SPIN-1 METRIC-DECOUPLING route, INDEPENDENT of the scalar.
LABEL: SUGGESTIVE (transcribed decoupling); exact alpha_1 NOT-COMPUTED here.
Pure-EA Foster-Jacobson gives alpha_1 = -4 K_B, so the AeST vector-metric
decoupling is the load-bearing difference and deserves its own explicit check.
""")

print("="*84)
print("VERDICT")
print("="*84)
print(r"""
DICHOTOMY RESOLUTION (both halves as posed are too crude; the true answer is
between them and now pinned):

 alpha_2 (spin-0):  REGULARIZED TO FINITE  -- but NOT by stiffening the aether.
   * The scalar's Q0-mass on the aether-longitudinal mode is EXACTLY cancelled
     by the chi--dphi mixing (perfect square (Q0 V + grad dphi)^2, m2*d=b^2):
     the static aether-longitudinal stiffness stays ZERO, det(w=0)=0.
   * The spin-0 DYNAMICS is instead carried by a HEALTHY MASSIVE SCALAR mode
     omega^2 = c_s^2 k^2 + M^2 with c_s^2=(2-K_B)/(K2 K_B)(1+K_B lam_s/2),
     M^2=(2-K_B)(1+lam_s)Q0^2/K_B (BOTH matched to SZ21).  Its static Green's
     function 1/(c_s^2 k^2 + M^2) is FINITE, replacing the pure-EA 1/(c123 k^2)
     pole.  The surviving frozen direction is STRESS-FREE, so it decouples from
     gravity and cannot re-open the pole.
   * "effective spin-0 kinetic coefficient": the aether's own c123 stays 0, but
     the spin-0 SECTOR acquires a nonzero effective kinetic operator supplied by
     the scalar (2 K2 dphi_dot^2 + gradient), => alpha_2 FINITE.  This is the
     spirit of dichotomy branch (1) [regularize to finite], with the mechanism
     corrected: scalar CARRIER, not aether stiffening.  [SOLID for finiteness of
     the spin-0 response; exact alpha_2 number NOT-COMPUTED -- needs metric+matter]

 alpha_1 (spin-1):  the scalar does NOT cancel it (wrong sector).  alpha_1=0
   would rest on the SZ21 massive-vector/metric decoupling, a separate spin-1
   statement.  So VSZ's unqualified "alpha_1=alpha_2=0" is only PARTLY grounded
   here: alpha_2 is manifestly regularized-to-finite by the scalar; alpha_1=0
   is a distinct, still-uncomputed spin-1 claim.  [honest status]
""")
print("done.")
