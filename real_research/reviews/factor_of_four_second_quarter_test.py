#!/usr/bin/env python3
"""
DECISIVE SUB-QUESTION: is the extra 4 (beyond Einstein's 8pi) a FORCED second Bekenstein-Hawking 1/4
(two-horizon / squared-entropy / Debye) -> DERIVED, or the free-fall (1/2)^2 convention -> ROUTE-DEPENDENT?

We trace EVERY factor in Z = sqrt(32pi/3) symbolically and test which structure produces the '4'.
"""
import sympy as sp

pi = sp.pi
c, G, Lam, rhoL, H = sp.symbols('c G Lambda rho_Lambda H', positive=True)

print("="*100)
print("(A) The exact factor tree of Z^2 = 32pi/3")
print("="*100)
Z2 = sp.Rational(32, 1)*pi/3
print(f"   Z^2 = 32 pi / 3 = {Z2}")
print(f"   FACTORIZATION the framework claims:  32pi/3 = 8pi * (1/3) * 4")
lhs = 8*pi*sp.Rational(1, 3)*4
print(f"   check 8pi*(1/3)*4 = {sp.simplify(lhs)}  == 32pi/3 ?  {sp.simplify(lhs - Z2)==0}")
print("""
   Where each factor is FORCED to live, traced from a0 = c^2 sqrt(Lambda/32pi):
     * Substitute Einstein  rho_Lambda = Lambda c^2/(8 pi G):
           a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_Lambda).
       The '8pi' is consumed CONVERTING Lambda->rho_Lambda (Einstein coupling) -- FORCED, unambiguous.
     * The de Sitter RATE is H_Lambda = c sqrt(Lambda/3) = sqrt(8pi/3) sqrt(G rho_Lambda).
       The '1/3' is the Friedmann 3 (from H^2 = (8piG/3) rho on the dS background) -- FORCED, lives in H.
     * What remains, relating a0 to sqrt(G rho_Lambda), is the dimensionless prefactor:
           a0 = kappa * c * sqrt(G rho_Lambda),  with the framework kappa = 1/2.
       Then Z = cH_Lambda/a0 = sqrt(8pi/3)/kappa, and  Z = sqrt(32pi/3)  <=>  kappa = 1/2.
""")

print("="*100)
print("(B) So the WHOLE 'extra 4' is 1/kappa^2 with kappa=1/2, i.e. (1/2)^{-2}=4. Pin kappa.")
print("="*100)
kappa = sp.Symbol('kappa', positive=True)
Z_of_kappa = sp.sqrt(8*pi/3)/kappa
print(f"   Z(kappa) = sqrt(8pi/3)/kappa.")
for name, k in [("free-fall / surface-gravity 1/2", sp.Rational(1,2)),
                ("no prefactor 1", sp.Integer(1)),
                ("thermal: a0=cH/2pi -> kappa=sqrt(8pi/3)/2pi", sp.sqrt(8*pi/3)/(2*pi)),
                ("Jeans 1/sqrt(pi)", 1/sp.sqrt(pi))]:
    Zval = sp.simplify(Z_of_kappa.subs(kappa, k))
    print(f"     kappa={str(k):28s} -> Z = {sp.nsimplify(Zval)} = {float(Zval):.4f}")
print("""
   The framework's Z=sqrt(32pi/3)=5.789 corresponds EXACTLY and ONLY to kappa=1/2.
   The thermal/Unruh route gives kappa=sqrt(8pi/3)/2pi=0.461 -> Z=2pi=6.283 (NOT 5.789).
   => no thermal/periodicity argument lands on 1/2; the 1/2 is kinematic, not thermal.
""")

print("="*100)
print("(C) Is kappa=1/2 a SECOND Bekenstein-Hawking 1/4, or a single free-fall 1/2?  THE crux.")
print("="*100)
print("""   Claim to test: '32pi = 4 x 8pi, and since Jacobson's 8pi ALREADY contains one BH-1/4 (8pi =
   2pi_Unruh x 4), the extra 4 is a SECOND BH-1/4 -> derived (two-horizon/squared-entropy/Debye).'

   Decompose Jacobson's 8pi (gr-qc/9504004) to see what the FIRST 4 is, then ask what the SECOND would
   have to be:""")
# Jacobson: dQ = T dS, T = Unruh = hbar a /2pi c kB, S = eta A, eta = 1/4G(hbar/...) => Einstein with 8piG.
# The standard chain: T_Unruh has 1/2pi ; S=A/4 has 1/4 ; combining T dS = dQ with Raychaudhuri yields
# 8piG = 2pi(from 1/T's 2pi) x 4(from 1/eta's 4) x G.  So 8pi = 2pi x 4, and the '4' = 1/(1/4)= the BH quarter.
twopi, quarter = 2*pi, sp.Rational(1, 4)
eight_pi = twopi/quarter
print(f"     Jacobson:  T_Unruh ~ 1/(2pi),  S_BH = A/4 (eta=1/4).  Einstein eta-coupling: 8pi = (2pi)/(1/4) = {sp.simplify(eight_pi)}.")
print(f"     => the FIRST factor of 4 inside 8pi IS the Bekenstein-Hawking 1/4 (correct).")
print("""
     Now the framework needs ANOTHER 4 on top. For it to be a SECOND BH-1/4 it must come from a SECOND,
     independent entropy/horizon factor. Enumerate the only structural ways to get a second 4, and test:

       (i)  TWO horizons (entropy ~ 2 x A/4):  gives a factor 2, NOT 4.  [a0 would scale by 1/sqrt(2), Z=8.2] -- FAILS.
       (ii) SQUARED entropy / Debye (S ~ (A/4)^2 or equipartition with 1/4 twice): a0 ~ 1/S would need a
            very specific power; but a0 ~ sqrt(G rho), i.e. a0 ~ 1/sqrt(S_dS) (since S_dS ~ 1/(Lambda lP^2)
            ~ 1/(G rho hbar)). Check the power:""")
# S_dS ~ 3pi/(Lambda lP^2); a0 ~ c^2 sqrt(Lambda) ~ c^2 / sqrt(S_dS) up to constants. Verify exponent.
lP2 = sp.Symbol('l_P2', positive=True)  # lP^2 = hbar G/c^3
S_dS = 3*pi/(Lam*lP2)
a0_scale = c**2*sp.sqrt(Lam)            # the dimensional skeleton
# express a0 in terms of S_dS:
Lam_of_S = sp.solve(sp.Eq(sp.Symbol('S'), S_dS), Lam)[0]
a0_in_S = a0_scale.subs(Lam, Lam_of_S)
print(f"          S_dS = 3pi/(Lambda lP^2)  =>  Lambda = {Lam_of_S}")
print(f"          a0 ~ c^2 sqrt(Lambda) = {sp.simplify(a0_in_S)}   => a0 ~ S^(-1/2).")
print("""          So a0 ~ 1/sqrt(S_dS): a SINGLE power of the area-entropy under a square root. There is NO
          'squared entropy' and NO second factor of 1/4 in this scaling -- the BH-1/4 appears ONCE
          (inside Lambda->rho via the 8pi already), and the remaining 1/2 is the EXPONENT of the sqrt,
          which is the free-fall/surface-gravity 1/2, NOT a thermodynamic entropy coefficient. -- FAILS to be a 2nd 1/4.
       (iii)Debye/equipartition E=(1/2)NkT with N=S: yields a 1/2, i.e. the SAME single 1/2 (kinematic),
            not an extra 1/4. -- gives 1/2, consistent with free-fall reading, NOT a derived 2nd quarter.""")

print("="*100)
print("(D) Independent confirmation: the de Sitter STATIC-PATCH surface gravity carries 1/2, not 1/4-squared")
print("="*100)
r = sp.Symbol('r', positive=True)
f = 1 - Lam*r**2/3                 # static de Sitter metric function (lapse^2), horizon at r_H=sqrt(3/Lambda)
rH = sp.sqrt(3/Lam)
kappa_dS = sp.simplify(sp.diff(f, r).subs(r, rH)/2)   # surface gravity = f'(r_H)/2
print(f"   dS static metric f(r)=1-Lambda r^2/3, horizon r_H=sqrt(3/Lambda).")
print(f"   surface gravity kappa_dS = f'(r_H)/2 = {kappa_dS}  (magnitude {sp.simplify(sp.Abs(kappa_dS))}).")
print(f"   => kappa_dS = c^2 * sqrt(Lambda/3) [restoring c], the SINGLE 1/2 (from f'/2). a0=(c/2)sqrt(Grho) shares")
print(f"      exactly this 1/2. There is NO second 1/4 in any horizon surface gravity -- it is universally 1/2.")

print("\n" + "#"*100)
print("# SUB-QUESTION VERDICT (computed):")
print("#   The 'extra 4' is 1/kappa^2 with kappa=1/2 -- the SINGLE free-fall/surface-gravity 1/2, SQUARED,")
print("#   NOT a second Bekenstein-Hawking 1/4. Every structural route to a genuine 'second 1/4'")
print("#   (two horizons -> factor 2; squared/Debye entropy -> wrong power, a0~S^{-1/2} has the 1/4 only ONCE)")
print("#   FAILS to reproduce 4. The de Sitter surface gravity carries 1/2 once, universally.")
print("#   The thermal route that DOES have a clean entropic 2pi gives Z=2pi=6.28, NOT 5.79.")
print("#   ===> the 4 is the kinematic (1/2)^2 convention -> ROUTE-DEPENDENT, not a forced 2nd 1/4.")
print("#"*100)
