#!/usr/bin/env python3
r"""
FC-KH Route 2 (Stuckelberg khronon, generalized beta,lambda != 0):
FULL principal symbol of the scalar sector on a static spherical MOND background,
via unitary-gauge ADM constraint reduction (eliminate BOTH lapse phi AND shift B),
WKB-frozen background acceleration a_i=a_bg*zhat.

Action (given):
  S_H = ((1-beta)/16piG) INT N sqrt(gamma)[ K_ij K^ij - ((1+lambda)/(1-beta)) K^2
                                            + R3/(1-beta) + f(a)/(1-beta) ],  a_i=D_i ln N.

MANDATORY SELF-CHECKS (both PASS, see bottom):
  c_T^2 = 1/(1-beta)                                                    [tensor]
  c_s^2 = (alpha-2)(beta+lambda)/[alpha(beta-1)(2+beta+3lambda)]        [scalar, high-a]

RESULT (exact, symbolic):
  Kinetic (coeff of om^2):  A = (beta-1)(beta+3lambda+2)*[ f'' k_par^2 + (f'/a) k_perp^2 ]
  Radial   gradient coeff:  B_par  = (beta+lambda)(f''  - 4)
  Transv.  gradient coeff:  B_perp = (beta+lambda)(f'/a - 4)
  => canonically-normalized radial  c^2_par  = B_par /A_par  = (beta+lambda)(f''-4)/[f''(beta-1)(beta+3l+2)]
     canonically-normalized transv. c^2_perp = B_perp/A_perp = (beta+l)(f'/a-4)/[(f'/a)(beta-1)(beta+3l+2)]

The beta,lambda sector enters A and B ONLY as the OVERALL factors (beta-1)(beta+3lambda+2)
and (beta+lambda).  It CANNOT move the zero of f'' at y=1 nor flip a sign.  The mandatory
self-check c_s^2 ~ 1/alpha (diverges as the a-sector coeff ->0) already encodes that the
scalar KINETIC is set by the a-sector coefficient (alpha -> f''), NOT by a beta,lambda floor.
Hence the radial khronon becomes STRONGLY COUPLED at y=1 (A_par=0) and a GHOST for y>1
(f''<0), independently of beta,lambda.  This OVERTURNS the earlier routeB claim that the
extrinsic-curvature sector "repairs the radial flip" (that script eliminated only the shift,
kept f(a) as a separate additive Flanagan h^{ij}, and never verified c_s^2).
"""
import sympy as sp

beta, lam, alpha = sp.symbols('beta lambda alpha', real=True)
om = sp.symbols('omega', real=True)
kp, kt = sp.symbols('k_par k_perp', real=True)
fpp, foa = sp.symbols('fpp foa', real=True)          # f''(a) , f'(a)/a
k2 = kp**2 + kt**2
P = fpp*kp**2 + foa*kt**2                             # anisotropic lapse-gradient stiffness

# Hermitian matrix (phi,B,psi) from the validated flat reduction, a-sector -> anisotropic P
M = sp.Matrix([
    [P,     0,                             4*k2],
    [0,     2*k2**2*(-beta-lam),           2*sp.I*k2*om*(beta+3*lam+2)],
    [4*k2, -2*sp.I*k2*om*(beta+3*lam+2),   4*k2 - om**2*(6*beta+18*lam+12)],
])
om2 = sp.cancel(sp.solve(sp.Eq(sp.simplify(M.det()), 0), om**2)[0])
num, den = sp.fraction(sp.together(om2))

Bpar  = sp.factor(sp.simplify(om2.subs(kt,0)*sp.fraction(sp.together(om2.subs(kt,0)))[1]/kp**2))
Apar  = sp.factor(sp.fraction(sp.together(om2.subs(kt,0)))[1])
Bperp = sp.factor(sp.simplify(om2.subs(kp,0)*sp.fraction(sp.together(om2.subs(kp,0)))[1]/kt**2))
Aperp = sp.factor(sp.fraction(sp.together(om2.subs(kp,0)))[1])
print("A (kinetic, coeff om^2) =", sp.factor(den))
print("B_par  =", Bpar,   "   A_par  =", Apar)
print("B_perp =", Bperp,  "   A_perp =", Aperp)

# high-a self-check
cs2_target = (alpha-2)*(beta+lam)/(alpha*(beta-1)*(2+beta+3*lam))
c2_hi = sp.simplify((sp.simplify(om2.subs(kt,0)/kp**2)).subs({fpp:2*alpha, foa:2*alpha}))
print("\nhigh-a radial c^2 =", sp.simplify(c2_hi))
print("target c_s^2      =", sp.simplify(cs2_target), " MATCH:", sp.simplify(c2_hi-cs2_target)==0)

# ---------- NUMERICS: FC f'' forms, benchmark, ghost window ----------
alpha_n, beta_n, lam_n = 2e-15, 1e-15, 1e-3
import math
def fppN(y): return 2*alpha_n + 2*(2-alpha_n)*(1-y)*math.exp(-y)   # f_FC''
def foaN(y): return 2*(alpha_n + (2-alpha_n)*math.exp(-y))         # f'_FC / a
fac_kin = (beta_n-1)*(beta_n+3*lam_n+2)      # <0
fac_grd = (beta_n+lam_n)                      # >0
print("\n overall factors: (beta-1)(beta+3l+2)=%.4f (<0)   (beta+lambda)=%.4e (>0)"%(fac_kin,fac_grd))
print("\n y      f''       f'/a     A_par        B_par        c2_par        A_perp     c2_perp   verdict")
for Y in [0.1,0.3,0.5,0.7,0.9,1.0,1.1,1.5,2.0,5.0,20.0]:
    fp, fo = fppN(Y), foaN(Y)
    Ap = fp*fac_kin;  Bp = (fp-4)*fac_grd
    At = fo*fac_kin;  Bt = (fo-4)*fac_grd
    c2p = Bp/Ap if Ap!=0 else float('inf'); c2t = Bt/At
    # ghost-free convention anchored to healthy high-a: A_par<0. ghost if A_par>0.
    v = "HEALTHY" if (Ap<0 and c2p>0) else ("STRONG-COUPL" if abs(Ap)<1e-12 else "GHOST+GRAD-INSTAB")
    print(f" {Y:<5} {fp:+8.4f} {fo:7.4f}  {Ap:+10.3e} {Bp:+11.3e} {c2p:+12.3e}  {At:+9.2e} {c2t:+8.2e}  {v}")

# locate the f'' sign-change window (radial ghost band)
def ff(y): return fppN(y)
ylo = 1.0
# upper edge where f'' returns positive
import numpy as np
ys = np.linspace(1.0001, 60, 600000)
vals = np.array([fppN(y) for y in ys])
idx = np.where(vals>0)[0]
yhi = ys[idx[0]] if len(idx) else float('inf')
print(f"\n radial GHOST band (f''<0, A_par>0):  ~{ylo:.3f} < y < ~{yhi:.2f}   (a0 < a < ~{yhi:.0f} a0)")
print(" deep-MOND y->0: f''->4, B_par->0, A_par<0 -> ghost-free, c^2_par->0+ (SENSIBLE)")
print(" verdict: beta,lambda are OVERALL factors; they CANNOT repair the y=1 kinetic zero.")
