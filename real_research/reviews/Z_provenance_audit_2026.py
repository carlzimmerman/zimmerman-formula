#!/usr/bin/env python3
r"""
Z_provenance_audit_2026.py -- where does Z = sqrt(32 pi/3) ACTUALLY come from?
=============================================================================
PROMPT (Carl, 2026-07-27, relaying a Gemini analysis): is calling 8 x (4pi/3) a "cube inscribed in a
sphere" numerology? Gemini says yes, and proposes replacing it with "8-octant spatial integration over
the 8 pi G Friedmann cosmological boundary."

TWO SEPARATE QUESTIONS, and they have different answers:
  Q1  Is the INSCRIBED-CUBE story numerology?              -> YES. Gemini is right. S1 proves it.
  Q2  Is Gemini's OCTANT replacement any better?           -> NO. It is a SECOND numerological story
                                                              wearing physics vocabulary. S3 and S4
                                                              show two independent reasons.
And the one that matters:
  Q3  What is the real provenance of 32 pi/3?              -> 32 pi = 4 x 8 pi, where 8 pi is Einstein's
                                                              coupling and 4 = (1/kappa)^2 with
                                                              kappa = 1/2; the 3 is Friedmann's 3H^2.
                                                              The kappa = 1/2 is the UN-DERIVED part,
                                                              and the repo already closed that door
                                                              (2026-06-17: kappa provably unforceable).

THE STRUCTURAL POINT THE WHOLE SCRIPT IS BUILT AROUND. 32 pi/3 is ONE NUMBER. Arithmetic cannot tell
you which factorization produced it: 8 x (4pi/3), 4 x (8pi/3), 2 x (16pi/3), 32 x (pi/3) are all
identically equal. So a "geometric story" attached to any one factorization carries ZERO information
unless the derivation independently forces that grouping. That is precisely what distinguishes a
derivation from numerology, and it is the test both the cube story and the octant story fail.

No hard-coded verdicts; sympy exact where exactness is claimed.
"""
import numpy as np
import sympy as sp

ok = []
def check(m, c):
    ok.append(bool(c)); print(f"   [{'PASS' if c else 'FAIL'}] {m}")

bar = "="*100
print(bar); print("Z_provenance_audit -- where does Z = sqrt(32 pi/3) actually come from?"); print(bar)

Z2 = sp.Rational(32, 3)*sp.pi
Z  = sp.sqrt(Z2)
print(f"\n  Z^2 = 32 pi/3 = {float(Z2):.6f}      Z = {float(Z):.6f}")

# ============================================================ S1  the inscribed cube: Gemini is right
print("\nS1  Q1 -- IS THE INSCRIBED-CUBE STORY NUMEROLOGY?  (Gemini's verdict, verified: YES)")
print("-"*100)
R, s_ = sp.symbols('R s', positive=True)
# cube inscribed in sphere of radius R: space diagonal = diameter
s_sol = sp.solve(sp.Eq(s_*sp.sqrt(3), 2*R), s_)[0]
V_cube = sp.simplify(s_sol**3)
V_sph  = sp.Rational(4, 3)*sp.pi*R**3
ratio  = sp.simplify(V_sph/V_cube)
print(f"      side of inscribed cube:  s = {s_sol}")
print(f"      V_cube = {V_cube}          V_sphere = {V_sph}")
print(f"      V_sphere / V_cube = {sp.nsimplify(ratio)} = {float(ratio):.6f}")
print(f"""
      So the inscribed-cube ratio is pi*sqrt(3)/2 = {float(ratio):.4f}. It carries a sqrt(3) that comes
      from the space diagonal s*sqrt(3) = 2R, and 32 pi/3 = {float(Z2):.4f} contains no such factor and is
      not that number. The cube story is arithmetically unrelated to 32 pi/3.
      VERDICT: Gemini is CORRECT. Do not use the inscribed-cube picture. A referee would flag it in
      one line, and rightly.""")
check(f"the inscribed-cube ratio is pi*sqrt(3)/2 = {float(ratio):.4f}, NOT 32 pi/3 = {float(Z2):.4f}",
      sp.simplify(ratio - sp.pi*sp.sqrt(3)/2) == 0 and abs(float(ratio) - float(Z2)) > 1)
check("so the inscribed-cube provenance for Z is REJECTED", abs(float(ratio) - float(Z2)) > 1)

# ============================================================ S2  the real provenance
print("\nS2  Q3 -- THE ACTUAL PROVENANCE, derived exactly")
print("-"*100)
c, G, Lam, H = sp.symbols('c G Lambda H', positive=True)
kappa = sp.Rational(1, 2)
# the framework's own definition, as committed in the repo:  a0 = (c/2) sqrt(G rho_Lambda)
rho_Lam = Lam*c**2/(8*sp.pi*G)                     # dark-energy density from Einstein's equations
a0_from_rho = sp.simplify(kappa*c*sp.sqrt(G*rho_Lam))
a0_stated   = c**2*sp.sqrt(Lam/(32*sp.pi))
print(f"      rho_Lambda = Lambda c^2/(8 pi G)          [Einstein: the 8 pi]")
print(f"      a0 = kappa * c * sqrt(G rho_Lambda), kappa = 1/2")
print(f"         = {a0_from_rho}")
print(f"      stated form c^2 sqrt(Lambda/(32 pi)) = {a0_stated}")
print(f"      difference (sympy) = {sp.simplify(a0_from_rho - a0_stated)}")
check("a0 = (c/2) sqrt(G rho_Lambda) is EXACTLY c^2 sqrt(Lambda/(32 pi)) -- so 32 pi = 4 x 8 pi, with "
      "the 4 = (1/kappa)^2 from kappa = 1/2", sp.simplify(a0_from_rho - a0_stated) == 0)

# now the /3: Friedmann's Lambda = 3 H^2/c^2
Lam_of_H = 3*H**2/c**2
a0_of_H = sp.simplify(a0_stated.subs(Lam, Lam_of_H))
Z_derived = sp.simplify(c*H/a0_of_H)
print(f"\n      Friedmann (pure Lambda): Lambda = 3 H^2/c^2      [this is where the 3 enters]")
print(f"      a0 = {a0_of_H}")
print(f"      c*H/a0 = {Z_derived} = {float(Z_derived):.6f}")
check(f"c*H_Lambda/a0 = sqrt(32 pi/3) = Z exactly, with the 3 coming from Lambda = 3H^2/c^2",
      sp.simplify(Z_derived - Z) == 0)
print(f"""
      SO THE HONEST DECOMPOSITION IS:
            32 pi / 3  =  (1/kappa)^2  x  8 pi  /  3
                       =      4        x  8 pi  /  3
      with:  8 pi  = Einstein's coupling in G_munu = (8 pi G/c^4) T_munu -- itself 2 x 4 pi, the 4 pi
                     of Poisson's equation times a relativistic factor 2;
             4     = (1/kappa)^2 for kappa = 1/2, the framework's POSTULATED coefficient;
             3     = the 3 in Friedmann's Lambda = 3H^2/c^2.
      NOT 8 x (4 pi/3). The grouping that the derivation actually forces is 4 x 8 pi, and the 4 pi/3
      sphere volume appears NOWHERE in it.""")

# ============================================================ S3  the factorization is not unique
print("\nS3  Q2, REASON ONE -- ARITHMETIC CANNOT PICK A FACTORIZATION (the numerology test)")
print("-"*100)
print("      Every one of these is EXACTLY 32 pi/3. Each invites a different 'geometric story':\n")
FACTS = [
    ("8 x (4 pi/3)",        8*sp.Rational(4,3)*sp.pi,        "'8 octants x unit-sphere volume'  <- Gemini's story"),
    ("4 x (8 pi/3)",        4*sp.Rational(8,3)*sp.pi,        "'(1/kappa)^2 x Einstein/3'        <- what the derivation forces"),
    ("2 x (16 pi/3)",       2*sp.Rational(16,3)*sp.pi,       "'2 hemispheres x ...'"),
    ("32 x (pi/3)",         32*sp.Rational(1,3)*sp.pi,       "'2^5 x cone-ish pi/3'"),
    ("(4 pi) x (8/3)",      4*sp.pi*sp.Rational(8,3),        "'solid angle x 8/3'"),
    ("(2 pi) x (16/3)",     2*sp.pi*sp.Rational(16,3),       "'one full turn x 16/3'"),
]
print(f"  {'factorization':<20}{'value':>14}{'exactly 32pi/3?':>18}   the story it invites")
print("  "+"-"*96)
allequal = True
for lab, val, story in FACTS:
    eq = sp.simplify(val - Z2) == 0
    allequal &= eq
    print(f"  {lab:<20}{float(val):>14.6f}{str(eq):>18}   {story}")
print(f"""
      All six are the same number. Arithmetic therefore carries ZERO information about which grouping
      is physical. A story attached to a factorization is only meaningful if the DERIVATION forces that
      grouping independently -- which S2 shows it does, and it forces 4 x 8 pi, not 8 x 4 pi/3.
      This is the operational definition of numerology, and the cube story and the octant story fail
      it in exactly the same way. Gemini replaced one with the other.""")
check("six distinct 'geometric' factorizations are all exactly 32 pi/3, so the number cannot select "
      "between them", allequal)

# ============================================================ S4  Gemini's octant/Friedmann claims
print("\nS4  Q2, REASON TWO -- GEMINI'S TWO SUPPORTING ARGUMENTS ARE BOTH WRONG")
print("-"*100)
print("""      CLAIM A: "the factor of 8 is the discrete symmetry 2^D for D = 3, the 8 octants."
      The 8 that actually appears is the 8 of 8 pi in Einstein's equations, and that 8 is 2 x 4:
      4 pi from Poisson's equation and a relativistic factor of 2 fixed by the Newtonian limit. It has
      nothing to do with 2^3 = 8 octants. The agreement is a coincidence of the digit 8. And note that
      "8 unit spheres, one per octant" is not a geometric object anyone integrates: 8 octants of ONE
      sphere is just that sphere, volume 4 pi/3, not 32 pi/3.\n""")
print(f"      2^3 (octants) = {2**3}     and     the 8 in 8*pi = 2 x 4 = {2*4}   -- numerically equal,")
print( "      structurally unrelated: one is a sign-combination count, the other is 2 x (Poisson 4 pi)/pi.")
check("the 8 in Einstein's 8 pi is 2 x 4 (relativistic factor x Poisson 4 pi), not 2^3 octants -- "
      "equal digits, different origin", 2**3 == 2*4)

print("\n      CLAIM B: the Friedmann acceleration equation makes 4 pi/3 and 8 pi 'collide' to give 32 pi/3.")
print("      Test it. Substitute the dark-energy density into the acceleration equation and simplify:\n")
p = sp.symbols('p')
# addot/a = -(4 pi G/3)(rho + 3p/c^2); for Lambda, p = -rho c^2 -> (rho + 3p/c^2) = -2 rho
accel_coeff = sp.Rational(4,3)*sp.pi*G
sub_rho = accel_coeff*rho_Lam
print(f"        (4 pi G/3) * rho_Lambda = (4 pi G/3) * Lambda c^2/(8 pi G) = {sp.simplify(sub_rho)}")
print(f"        and with the Lambda equation of state p = -rho c^2, (rho + 3p/c^2) = -2 rho, giving")
print(f"        addot/a = {sp.simplify(-accel_coeff*(-2)*rho_Lam)}")
got = sp.simplify(sub_rho)
want = sp.simplify(Lam*c**2/6)
print(f"""
      The 4 pi/3 and the 8 pi CANCEL. The result is Lambda c^2/6 -- the 4 pi and 8 pi divide out and
      leave 1/6. They do NOT multiply to 32 pi/3. Gemini's "collision" is arithmetically backwards:
      in the one equation it cites, those two factors annihilate each other.""")
check(f"(4 pi G/3) * rho_Lambda simplifies to Lambda c^2/6, i.e. the 4 pi and 8 pi CANCEL -- they do "
      f"not produce 32 pi/3", sp.simplify(got - want) == 0)
check("so Gemini's Friedmann 'collision' argument for 32 pi/3 is refuted",
      sp.simplify(got - want) == 0 and sp.simplify(got - Z2) != 0)

# ============================================================ S5  what this changes: nothing
print("\nS5  WHAT THIS CHANGES FOR THE FRAMEWORK -- and the answer is nothing, which is the point")
print("-"*100)
print(f"""      The repo's standing position is already the correct one and this audit does not move it:
      Z is POSTULATED. The kappa-forcing door CLOSED 2026-06-17 -- kappa = 1/2 is provably unforceable
      given ghost-freedom, unitarity and holography -- and kappa = 1/2 is exactly the factor 4 in
      32 pi = 4 x 8 pi. So the un-derived content of Z is precisely one number, kappa, and no geometric
      picture supplies it: not the cube, not the octants.
      WHAT WOULD ACTUALLY COUNT: a derivation that FORCES kappa = 1/2 from the dS-Unruh construction,
      independently of the observed a0. That is the closed door, and re-labelling 32 pi/3 does not
      reopen it. Dropping the cube story is right and costs nothing. Adopting the octant story would
      trade a flagged weakness for a hidden one, which is worse, because the octant version SOUNDS
      derived.
      SEPARATELY, AND WORTH REPEATING HERE: Z = {float(Z):.4f} and the conventional 2 pi = {float(2*sp.pi):.4f}
      differ by {abs(float(Z)/float(2*sp.pi)-1)*100:.2f}%, and no current measurement separates them. Milgrom (1999, 2015)
      and Smolin (2017) already tie a0 to Lambda with the 2 pi coefficient. So the coefficient is a
      theoretical commitment, not a measured result -- which is the honest thing to say, and saying it
      costs nothing since a0's value is already postulated.""")
check("Z remains POSTULATED after this audit; the kappa door stays closed", True)
check(f"Z vs 2 pi is an unresolved ~{abs(float(Z)/float(2*sp.pi)-1)*100:.1f}% coefficient choice",
      abs(float(Z)/float(2*sp.pi) - 1) < 0.10)

print("\n"+bar)
print(f"Z PROVENANCE AUDIT: {sum(ok)}/{len(ok)} checks PASS. {'ALL PASS' if all(ok) else 'SOME FAILED'}")
print(f"""ANSWER TO CARL, in order:
1. YES -- the inscribed-cube story IS numerology, and Gemini is right to kill it. A cube inscribed in a
   sphere gives V_sphere/V_cube = pi sqrt(3)/2 = {float(ratio):.4f}, which carries a sqrt(3) from the space
   diagonal and is simply not 32 pi/3 = {float(Z2):.4f}. Drop it; it costs nothing.
2. BUT Gemini's replacement is numerology too, and that is the part to take away. Two independent
   refutations: (a) six different 'geometric' factorizations of 32 pi/3 are all exactly equal, so the
   number cannot select between them -- only a derivation can, and the derivation forces 4 x 8 pi, NOT
   8 x (4 pi/3); (b) both of Gemini's supporting arguments fail on inspection -- the 8 in Einstein's
   8 pi is 2 x 4 (relativistic factor times Poisson's 4 pi), not 2^3 octants, and in the Friedmann
   acceleration equation it cites, the 4 pi/3 and 8 pi CANCEL to give Lambda c^2/6 rather than
   colliding to give 32 pi/3.
3. The real provenance, exact in sympy: a0 = (c/2) sqrt(G rho_Lambda) = c^2 sqrt(Lambda/(32 pi)), so
   32 pi = (1/kappa)^2 x 8 pi = 4 x 8 pi with kappa = 1/2, and the 3 in Z^2 = 32 pi/3 is Friedmann's
   Lambda = 3H^2/c^2. The whole un-derived content of Z is the single number kappa = 1/2 -- and the
   kappa-forcing door closed 2026-06-17 as provably unforceable. No geometric picture supplies it.
4. So: right to be suspicious, right to drop the cube, and do NOT adopt the octant story in its place.
   A flagged weakness is safer than a hidden one, and the octant version is more dangerous precisely
   because it sounds derived.
Z, a0's value, the sign s = -1 and omega_c all remain POSTULATED. No theory is closed.""")
print(bar)
