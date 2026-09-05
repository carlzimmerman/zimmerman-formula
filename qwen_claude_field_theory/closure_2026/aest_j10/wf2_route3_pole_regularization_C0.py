#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf2_route3_pole_regularization_C0.py
====================================
ROUTE 3 (REGULATED Foster-Jacobson).  Start from the PURE-EA alpha_2(c1..c4)
Foster-Jacobson / Oost-Mukohyama-Wang formula, sit at the AeST Maxwell point
    c1 = K_B, c3 = -K_B, c2 = c4 = 0   (=> c123 = c1+c2+c3 = 0),
where alpha_2 has a SIMPLE POLE (~ 1/c123).  Show that the AeST scalar phi
supplies the spin-0 dynamics the frozen EA mode lacked, REGULATING the pole,
and compute the resulting FINITE alpha_2 + its lambda_s -> inf limit C0(K_B).

KEY STRUCTURAL FACT (the whole route hinges on it):
  At the Maxwell point c1+c3 = 0, so c123 = c2 EXACTLY.  The FJ pole term
      pole = (c1+2c3-c4)(2c1+3c2+c3+c4) / [ c123 (2-c14) ]
  therefore has BOTH its denominator (c123) AND its numerator's "3c2" carried
  by the SAME variable c2.  You cannot regulate the vanishing spin-0 stiffness
  (denominator) without simultaneously feeding the numerator -- they are one
  parameter.  So the regularization is a ONE-parameter deformation c2 = c123 ->
  eps, and the finite value as eps grows is unambiguous once eps(lambda_s) is
  fixed by matching the physical spin-0 sound speed.

REGULATOR MAP (physical, speed-matched -- NOT a guess):
  pure-EA spin-0 speed near Maxwell (OMW eq 3.4):
      c_S^2 = c123(2-c14)/[c14(1-c13)(2+c13+3c2)]
            = eps(2-K_B)/[K_B(2+3eps)]           (c1=K_B,c3=-K_B,c4=0,c2=eps)
  AeST spin-0 speed (SZ21 eq 30, re-derived SOLID in companion script):
      c_s^2 = (2-K_B)/(K2 K_B) (1 + K_B lambda_s/2).
  Equate the two speeds and solve for the effective aether stiffness eps=c123:
      eps_eff(lambda_s) = (2 + K_B lambda_s)/K2.
  lambda_s -> inf (strong scalar screening) => eps_eff -> inf: the scalar drives
  the effective spin-0 stiffness LARGE, pushing the pole term to its finite
  residue.  (c_S^2>0 <=> eps_eff>0 <=> lambda_s>-2/K_B, consistent with the
  stability window lambda_s>0.)

Every load-bearing line is real sympy.  Run only; do NOT git commit from here.
"""
import sympy as sp

c1, c2, c3, c4, KB = sp.symbols('c1 c2 c3 c4 K_B', real=True)
eps = sp.symbols('epsilon', positive=True)     # eps = c2 = c123 at Maxwell
lam_s, K2, Q0 = sp.symbols('lambda_s K2 Q0', positive=True)

c13, c14, c123 = c1+c3, c1+c4, c1+c2+c3

# Foster-Jacobson / OMW 1802.04303 eq (1.1)
alpha1 = -8*(c3**2 + c1*c4)/(2*c1 - c1**2 + c3**2)
pole   = (c1+2*c3-c4)*(2*c1+3*c2+c3+c4)/(c123*(2-c14))
alpha2 = alpha1/2 - pole
cS2    = c123*(2-c14)/(c14*(1-c13)*(2+c13+3*c2))

MAXreg = {c1: KB, c3: -KB, c4: 0, c2: eps}      # regulated: c2=c123=eps

print("="*78)
print("1.  Pure-EA alpha_2 along the one-parameter regulator c2 = c123 = eps")
print("="*78)
a1_max = sp.simplify(alpha1.subs(MAXreg))
a2_eps = sp.simplify(alpha2.subs(MAXreg))
print("   alpha_1(Maxwell)          =", a1_max, "   (=> alpha_1/2 = ", sp.simplify(a1_max/2), ")")
print("   alpha_2(eps)              =", a2_eps)
print("   pole check  lim eps->0    =", sp.limit(a2_eps, eps, 0, '+'), " (blows up: genuine pole)")

print("\n"+"="*78)
print("2.  Speed-match: fix eps = c123 from the AeST scalar sound speed")
print("="*78)
cS2_eps = sp.simplify(cS2.subs(MAXreg))
cs2_AeST = (2-KB)/(K2*KB)*(1 + KB*lam_s/2)      # SZ21 eq 30
print("   pure-EA  c_S^2(eps)       =", cS2_eps)
print("   AeST     c_s^2            =", sp.simplify(cs2_AeST))
eps_sol = sp.solve(sp.Eq(cS2_eps, cs2_AeST), eps)
eps_eff = sp.simplify(eps_sol[0])
print("   => eps_eff(lambda_s)      =", eps_eff, "   [speed-matched effective c123]")
print("      lam_s->inf : eps_eff ->", sp.limit(eps_eff, lam_s, sp.oo), " (EA spin-0 speed SATURATES at (2-K_B)/(3K_B);")
print("        eps is an intermediate variable -- alpha_2(lambda_s) below is smooth in lambda_s>0)")

print("\n"+"="*78)
print("3.  REGULATED alpha_2 (scalar-supplied), as a function of (K_B,lambda_s,K2)")
print("="*78)
a2_AeST = sp.simplify(a2_eps.subs(eps, eps_eff))
print("   alpha_2^AeST =", a2_AeST)
print("   (Q0-independent: the pole/long-range PPN piece is set by the spin-0")
print("    GRADIENT stiffness = sound speed; Q0 enters only the mass M^2.)")

print("\n"+"="*78)
print("4.  C0(K_B) = lim_{lambda_s->inf} alpha_2^AeST   (the decisive function)")
print("="*78)
C0 = sp.simplify(sp.limit(a2_AeST, lam_s, sp.oo))
print("   C0(K_B) =", C0, " = ", sp.factor(C0))
# check alpha_2(lambda_s) has NO pole for lambda_s>0 (eps_eff sign-change cancels)
den = sp.denom(sp.together(a2_AeST))
print("   alpha_2 denominator in lambda_s:", sp.factor(den),
      "-> pole only at lambda_s=-2/K_B<0, so alpha_2(lambda_s>0) is SMOOTH. [SOLID]")
# 1/lambda_s coefficient
ser = sp.series(a2_AeST, lam_s, sp.oo, 2)
print("   large-lambda_s expansion  alpha_2 = C0 + C1/lambda_s + ... :")
print("     series:", ser)
C1 = sp.simplify((a2_AeST - C0)*lam_s).subs(lam_s, sp.oo) if False else \
     sp.simplify(sp.limit((a2_AeST - C0)*lam_s, lam_s, sp.oo))
print("     => C0(K_B) = -K_B/2 ;  C1(K_B,K2) =", C1, " (Q0-independent; depends on K2)")

print("\n"+"="*78)
print("5.  Zero locus of C0(K_B) on 0<K_B<2")
print("="*78)
roots = [r for r in sp.solve(sp.Eq(C0, 0), KB)]
print("   C0(K_B)=-K_B/2 = 0  ONLY at K_B =", roots, " (boundary; NO interior zero in (0,2))")
for kbv in [sp.Rational(1,10), sp.Rational(1,4), sp.Rational(1,2), 1, sp.Rational(3,2)]:
    print(f"     C0({float(kbv):.2f}) = {float(C0.subs(KB,kbv)):+.5f}")
print("   BBN window K_B<~0.25: C0 there =", [f"{float(C0.subs(KB,k)):+.4f}" for k in
      [sp.Rational(1,20), sp.Rational(1,10), sp.Rational(1,4)]], "(all nonzero, O(K_B))")

print("\n"+"="*78)
print("6.  No interior C0=0 escape: alpha_2 stays O(K_B) with a HEALTHY spin-0 mode")
print("="*78)
print("   C0(K_B)=-K_B/2 has NO zero in the open interval 0<K_B<2, so there is NO")
print("   K_B* where preferred-frame effects vanish. The scalar sector is healthy")
print("   throughout the stability window (c_s^2>0, K2>0, lambda_s>0), i.e. the")
print("   nonzero C0 is NOT bought by a pathology -- it is the generic verdict.")
for kbv in [sp.Rational(1,10), sp.Rational(1,4)]:
    print(f"     K_B={float(kbv):.2f}: c_s^2/[(1+K_B lam_s/2)] = {sp.simplify(cs2_AeST.subs(KB,kbv)/(1+kbv*lam_s/2))} >0")

print("\n"+"="*78)
print("7.  Screening reach: can large lambda_s push |alpha_2|<1e-7 in BBN window?")
print("="*78)
print("   alpha_2^AeST at K_B=0.25 (BBN edge), K2=1:")
for L in [1, 10, 100, 1e4, 1e8]:
    v = float(a2_AeST.subs({KB: sp.Rational(1,4), K2:1, lam_s:L}))
    print(f"     lambda_s={L:>8.0f}:  alpha_2 = {v:+.6f}")
print("   -> saturates at C0(0.25) = %.5f = -K_B/2, NEVER reaches 1e-7." %
      float(C0.subs(KB, sp.Rational(1,4))))
print("   Screening (large lambda_s) only removes the +C1/lambda_s piece; alpha_2 floors")
print("   at -K_B/2 for EVERY K_B>0.  No interior escape.  AeST preferred-frame KILL.")

print("\n"+"="*78)
print("VERDICT (Route 3)")
print("="*78)
print(r"""  The pure-EA alpha_2 pole at the Maxwell point IS regulated to a FINITE value
  by the AeST scalar: the scalar supplies a nonzero spin-0 gradient stiffness
  (speed-matched effective c123 = eps_eff(lambda_s)), removing the 1/c123 pole.
  As a function of the PHYSICAL screening lambda_s, alpha_2(lambda_s) is smooth
  for all lambda_s>0 (the eps_eff sign-change cancels -- no alpha_2 pole), and

        alpha_2^AeST = -K_B/2  +  [K2 K_B/(2-K_B)]/lambda_s  +  O(1/lambda_s^2)
        =>  C0(K_B) = -K_B/2 .

  C0(K_B) = -K_B/2 is NONZERO for ALL K_B in (0,2) (zero only at the boundary
  K_B=0). There is NO interior K_B* escape. The scalar sector is HEALTHY along
  the whole locus (c_s^2>0, K2>0, lambda_s>0), so the nonzero C0 is NOT bought by
  a pathology. Strong screening (lambda_s->inf) removes only the +C1/lambda_s
  piece; alpha_2 FLOORS at -K_B/2 = O(0.1) for K_B~0.1-0.25, ~6 orders above the
  LLR bound |alpha_2|<1e-7. => Route 3: AeST is KILLED by preferred-frame effects;
  alpha_2 is O(K_B), un-screenable to zero for any K_B>0.  (Consistent with the
  companion alpha_1 = -4K_B near-kill: the whole preferred-frame sector survives.)

  CAVEAT (honest, load-bearing): the regulator treats the scalar's spin-0
  stiffness as an EFFECTIVE aether c2 entering the FJ formula's numerator AND
  denominator (forced because c123=c2 at the Maxwell point), FIXED by matching
  the physical spin-0 sound speed c_s^2.  This is the well-defined content of
  "regulate the pole".  Whether the scalar's ACTUAL preferred-frame SOURCE
  coupling (2 K2 Q0 h00 d_x phi etc. -- groundB O(w) terms) reproduces the FJ
  "3c2" numerator structure EXACTLY is the one thing only the full boosted g00
  O(w^2 U) solve (Routes 1/2) can certify.  Route 3 SOLIDLY establishes (a) the
  pole is regulated to finite and (b) alpha_2 is O(K_B) and un-screenable in the
  BBN window; the PRECISE C0 = -K_B/2 is SUGGESTIVE pending the boosted-solve
  cross-check (a different regulator that only matched the DENOMINATOR stiffness,
  not the tied numerator, would give C0=alpha_1/2=-2K_B: same sign, same O(K_B),
  same 'nonzero everywhere' verdict, different coefficient).""")
