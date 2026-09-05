"""
wf2_maxwell_alpha2_pole_pathdep.py
==================================
QUESTION (WF2 task): At the pure-Maxwell Einstein-aether point
    c1 = -c3 = K_B ,  c2 = c4 = 0
does the Foster-Jacobson PPN parameter alpha_2 GENUINELY diverge, or does it
approach a FINITE (possibly path-dependent) limit?  I.e. is the c123 -> 0
singularity REMOVABLE (numerator also vanishes => 0/0 => finite) or GENUINE
(numerator nonzero => simple pole)?  And is the FJ formula even VALID there?

Formulas (SOLID, literature-verbatim): Oost-Mukohyama-Wang arXiv:1802.04303
  eq (1.1):  alpha_1 = -8(c3^2 + c1 c4)/(2 c1 - c1^2 + c3^2)
             alpha_2 = alpha_1/2
                       - (c1+2c3-c4)(2c1+3c2+c3+c4)/[ c123 (2-c14) ]
  eq (3.4):  c_S^2   = c123 (2-c14) / [ c14 (1-c13)(2+c13+3c2) ]     (spin-0)
             c_V^2   = [2c1 - c13(2c1-c13)] / [2 c14 (1-c13)]        (spin-1)
             c_T^2   = 1/(1-c13)                                     (spin-2)
  with c13=c1+c3, c14=c1+c4, c123=c1+c2+c3.
  (Identical to Foster-Jacobson gr-qc/0509083; also the AeST aether kinetic
   term -(K_B/2)F^2 is the c1=-c3=K_B, c2=c4=0 "Maxwell point".)

We do REAL sympy: exact numerator at the point, a fully GENERIC 3-direction
approach path, the Laurent leading term, left/right one-sided limits, and the
shared c123 factor with c_S^2.  Nothing is hand-asserted.
"""
import sympy as sp

c1, c2, c3, c4, KB = sp.symbols('c1 c2 c3 c4 K_B', real=True)
t = sp.symbols('t', positive=True)                  # path parameter t -> 0+
a, b, d = sp.symbols('a b d', real=True)            # generic path directions

c13  = c1 + c3
c14  = c1 + c4
c123 = c1 + c2 + c3

alpha1 = -8*(c3**2 + c1*c4)/(2*c1 - c1**2 + c3**2)
pole_term = (c1 + 2*c3 - c4)*(2*c1 + 3*c2 + c3 + c4)/(c123*(2 - c14))
alpha2 = alpha1/2 - pole_term

cS2 = c123*(2 - c14)/(c14*(1 - c13)*(2 + c13 + 3*c2))
cV2 = (2*c1 - c13*(2*c1 - c13))/(2*c14*(1 - c13))
cT2 = 1/(1 - c13)

MAX = {c1: KB, c3: -KB, c2: 0, c4: 0}

print("="*74)
print("0.  LITERATURE CROSS-CHECK of the alpha_2 transcription")
print("="*74)
# The web-search AI-summary offered an ALTERNATE-looking alpha_2. Test whether
# it is algebraically identical to the OMW-verbatim form (guards a typo).
alpha2_altform = ((2*c13 - c14)**2/(c123*(2 - c14))
                  - (12*c3*c13 + 2*c1*c14*(1 - 2*c14)
                     + (c1**2 - c3**2)*(4 - 6*c13 + 7*c14))
                    /((2 - c14)*(2*c1 - c1**2 + c3**2)))
diff = sp.simplify(alpha2 - alpha2_altform)
print("alpha2(OMW-verbatim) - alpha2(alt algebraic rearrangement) =", diff,
      "\n   -> identical forms" if diff == 0 else
      "\n   -> NOT identical (alt summary was garbled; OMW form is authoritative)")

print("\n" + "="*74)
print("1.  VALUES AT / NEAR THE MAXWELL POINT  (c1=K_B, c3=-K_B, c2=c4=0)")
print("="*74)
print("  c13   =", c13.subs(MAX))
print("  c14   =", c14.subs(MAX))
print("  c123  =", c123.subs(MAX), "   <-- ZERO  (this is what the pole divides by)")
print("  alpha_1(Maxwell)        =", sp.simplify(alpha1.subs(MAX)), "   [finite]")
print("  alpha_1/2 (first term)  =", sp.simplify((alpha1/2).subs(MAX)), "   [finite]")

print("\n" + "="*74)
print("2.  IS IT 0/0 (removable) OR N/0 (genuine pole)?  -- exact numerator")
print("="*74)
num = (c1 + 2*c3 - c4)*(2*c1 + 3*c2 + c3 + c4)
den = c123*(2 - c14)
num_at = sp.simplify(num.subs(MAX))
den_at = sp.simplify(den.subs(MAX))
print("  pole-term NUMERATOR (c1+2c3-c4)(2c1+3c2+c3+c4) at Maxwell =", num_at)
print("  pole-term DENOMINATOR c123(2-c14)               at Maxwell =", den_at)
print("  => numerator =", num_at, "(NONZERO for K_B!=0); denominator = 0")
print("  => NOT 0/0. This is a GENUINE (non-removable) pole, not removable.")

print("\n" + "="*74)
print("3.  GENERIC APPROACH PATH  c2=a t, c4=b t, c3=-K_B+d t,  t->0+")
print("     (a,b,d arbitrary directions; the most general straight-line ray)")
print("="*74)
path = {c1: KB, c2: a*t, c4: b*t, c3: -KB + d*t}
c123_path = sp.simplify(c123.subs(path))
print("  c123 along path =", c123_path, "   (=> = (a+d) t : pole is hit unless a+d=0)")
a2_path = sp.simplify(alpha2.subs(path))
# Leading Laurent term in t (expect order -1 => simple pole)
lead = sp.series(a2_path, t, 0, 0).removeO()
lead = sp.simplify(lead)
print("  alpha_2(t) Laurent leading term =", lead)
coeff_m1 = sp.simplify(sp.limit(a2_path*t, t, 0))       # residue-like coefficient of 1/t
print("  coefficient of 1/t (path 'residue') =", sp.simplify(coeff_m1))
print("     -> = K_B^2 / [ (a+d)(2-K_B) ] : nonzero & PATH-DEPENDENT in sign/size")
print("     -> magnitude ALWAYS blows up (order 1/t); only its SIGN/scale depend")
print("        on direction (a+d). No finite limit exists. GENUINE DIVERGENCE.")

print("\n" + "="*74)
print("4.  ONE-SIDED (left/right) limits along the simplest ray c2=eps->0")
print("     (c1=K_B, c3=-K_B, c4=0)")
print("="*74)
eps = sp.symbols('epsilon', real=True)
a2_eps = sp.simplify(alpha2.subs({c1: KB, c3: -KB, c4: 0, c2: eps}))
print("  alpha_2(eps) =", a2_eps)
lim_plus  = sp.limit(a2_eps, eps, 0, dir='+')
lim_minus = sp.limit(a2_eps, eps, 0, dir='-')
print("  lim eps->0+ :", lim_plus)
print("  lim eps->0- :", lim_minus)
print("  => +/- infinity depending on side  ==> simple pole, NOT a finite limit.")

print("\n" + "="*74)
print("5.  WHY THE FORMULA IS SINGULAR HERE: it shares c123(2-c14) with c_S^2")
print("="*74)
cS2_num = sp.simplify((c123*(2 - c14)).subs(MAX))
cS2_den = sp.simplify((c14*(1 - c13)*(2 + c13 + 3*c2)).subs(MAX))
print("  spin-0 c_S^2 numerator at Maxwell =", cS2_num, " ; denominator =", cS2_den)
print("  => c_S^2(Maxwell) =", sp.simplify(cS2_num/cS2_den), "  (spin-0 mode FROZEN)")
print("  c_V^2(Maxwell) =", sp.simplify(cV2.subs(MAX)),
      " ; c_T^2(Maxwell) =", sp.simplify(cT2.subs(MAX)))
# Demonstrate the tie: alpha_2 pole term * c_S^2 is FINITE & nonzero at the point
tie = sp.simplify((pole_term*cS2))
tie_at = sp.limit(tie.subs({c1: KB, c3: -KB, c4: 0, c2: eps}), eps, 0)
print("\n  (alpha_2 pole term) x c_S^2  ->", sp.simplify(tie_at), "as eps->0")
print("  => alpha_2's blow-up is EXACTLY 1/(spin-0 phase space): the divergence")
print("     is the reciprocal of the vanishing scalar-mode speed.")

print("\n" + "="*74)
print("6.  DOMAIN OF VALIDITY of the FJ/OMW alpha_2 formula")
print("="*74)
print("""  Foster-Jacobson derive alpha_1,alpha_2 by solving the linearized field
  eqs and integrating out the aether's spin-0 mode; that reduction PRESUMES a
  propagating spin-0 sector (c_S^2 != 0) -- indeed FJ impose c_S^2>0 (no ghost/
  gradient instability, no vacuum Cherenkov). At the Maxwell point c123=0 the
  spin-0 mode is NON-dynamical (c_S^2=0), so the formula is applied OUTSIDE its
  domain. The 1/c123 pole is the algebraic FINGERPRINT of that breakdown, not a
  physical prediction alpha_2 -> infinity.
  Physically: the pure-aether Maxwell point has a strongly-coupled/degenerate
  spin-0 sector. In AeST the scalar field phi SUPPLIES the spin-0 dynamics and
  must regulate the pole; VSZ ASSERT alpha_1=alpha_2=0 for AeST (a claim; no
  published derivation). The correct alpha_2 is a FULL-AeST computation, which
  the pure-aether EA formula literally cannot see.""")

print("="*74)
print("VERDICT: GENUINE simple pole (numerator = -c1^2 != 0), NOT removable,")
print("NOT 0/0; limit is +/-inf by side, path-'residue' K_B^2/[(a+d)(2-K_B)].")
print("But it is an ARTIFACT of using the propagating-spin-0 EA formula at the")
print("c_S^2=0 Maxwell point (out of domain), NOT a physical alpha_2 divergence.")
print("="*74)
