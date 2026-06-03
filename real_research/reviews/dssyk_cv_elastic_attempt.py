#!/usr/bin/env python3
"""
ATTEMPTING the calculation: does straining the de Sitter maximal-volume slice around a baryon give MOND?
=======================================================================================================
Carl: "actually attempt the DSSYK static-patch elastic-response calculation (does straining the
maximal-volume slice around a baryon give M_D prop r, attractive?)."

Honest scope up front: the full chord-algebra DSSYK computation is beyond what I can do rigorously, and
I will NOT fake it. But DSSYK's GEOMETRIC face -- complexity = VOLUME of the maximal slice (CV) -- is
computable in GR perturbation theory, and that IS the elastic-response question. So I compute the
maximal-slice volume response to a baryon and read off what law it gives. Result below is largely
NEGATIVE and it CORRECTS my own earlier sign guess -- which is the honest outcome of an attempt that
doesn't pan out, reported straight. Needs numpy + scipy.
"""
import numpy as np
from scipy import integrate

# ------------------------------------------------------------------------------------------------
def part1_requirement():
    print("="*94); print("PART 1 [DERIVED last pass] -- what MOND demands of ANY response"); print("="*94)
    print("""  deep-MOND phantom halo: M_D(r) = r * sqrt(a0 M_b / G)  ->  rho_D ~ sqrt(M_b)/r^2.
  TWO requirements: (a) volume-extensive (rho~1/r^2), and (b) NON-LINEAR in the source (~sqrt(M_b)).
  The sqrt(M_b) is the AQUAL non-linearity: a response LINEAR in M_b can never give it (it gives a
  Newtonian-type law). So any candidate 'medium' must respond NON-LINEARLY. Keep this as the test.\n""")


def part2_the_calculation():
    print("="*94); print("PART 2 [COMPUTED] -- the maximal-slice (complexity=volume) response to a baryon"); print("="*94)
    print("""  Setup: complexity C = V_max/(G L), L=c/H. Baryon = Schwarzschild-de Sitter perturbation; weak
  field, isotropic gauge: spatial metric h_ij=(1-2Phi)delta_ij, Phi=-GM_b/r, sqrt(h)~1-3Phi.
  Volume response within R:  dV(R) = INT_0^R (-3Phi) 4 pi r^2 dr = INT_0^R (3 G M_b/r) 4 pi r^2 dr.""")
    G = M = 1.0
    integ = lambda r: 3*G*M/r * 4*np.pi*r**2
    print(f"\n  {'R':>6}{'dV(R) numeric':>16}{'6 pi G M R^2':>16}{'dV/R^2':>10}")
    for R in (1.0, 2.0, 4.0, 8.0):
        val, _ = integrate.quad(integ, 1e-6, R)
        print(f"  {R:>6.1f}{val:>16.3f}{6*np.pi*G*M*R**2:>16.3f}{val/R**2:>10.3f}")
    print("  => dV(R) = 6 pi G M_b R^2 :  LINEAR in M_b, proportional to R^2. (numeric = analytic.)\n")


def part3_findings():
    print("="*94); print("PART 3 [FINDINGS] -- three reasons the straightforward attempt does NOT give MOND"); print("="*94)
    print("""  FINDING 1 [wrong law]. dV is LINEAR in M_b; MOND is sqrt(M_b). A linear response CANNOT produce
    the deep-MOND sqrt-law (Part 1). The leading complexity=volume response therefore does not give MOND.

  FINDING 2 [naive sourcing is unphysical]. If one treats dC=dV/(G L) as a dark mass M_D ~ dC, then
    g_D = G M_D/R^2 ~ G M_b R^2/(L R^2) = G M_b/L = CONSTANT in R -- a distance-independent extra
    acceleration, neither Newton (1/R^2) nor MOND (1/R). It is unphysical. This PROVES that
    'complexity = volume' does not directly source gravity: the elastic BACK-REACTION (how the
    complexity perturbation feeds back on the metric) is required, and that is the uncomputed step.

  FINDING 3 [my earlier SIGN guess was BACKWARDS -- correction]. In the potential well Phi<0, so
    sqrt(h)=1-3Phi>1: the baryon INCREASES the local maximal-slice volume, i.e. dC>0. A baryon is a
    complexity EXCESS, not a deficit. My earlier heuristic ('baryon = low-complexity defect -> 2nd law
    restores -> attractive') is thus likely WRONG; if the second law removes the excess, the response
    could be REPULSIVE (anti-MOND). The sign is undetermined and my prior guess is retracted.\n""")


def part4_what_would_rescue():
    print("="*94); print("PART 4 [OPEN] -- what could still rescue it, and what I will NOT fake"); print("="*94)
    print("""  The attempt fails only at LEADING (linear) order in the naive CV reading. Two things could still
  give MOND, and neither is derivable here:
    (i) Verlinde's SPECIFIC non-linear elastic relation (an entropy/strain 'yield' condition) has no
        automatic analog in CV; if the complexity medium had that exact non-linear constitutive law, the
        sqrt-law could re-appear. Not supplied by complexity=volume; would have to be imported.
    (ii) SECOND-LAW SATURATION: if the de Sitter vacuum sits at maximal complexity C~C_max~e^S, the
        response to a perturbation is bounded/non-linear near saturation -- a genuine source of
        non-linearity. But mapping 'complexity near C_max' to an AQUAL sqrt-law is not established, and I
        cannot derive it without the DSSYK chord dynamics. Stating it is honest; computing it is the
        research program; faking it is what this whole repo's June audit exists to prevent.\n""")


def verdict():
    print("="*94); print("HONEST VERDICT -- the attempt, reported straight"); print("="*94)
    print("""  I attempted the elastic-response calculation in the tractable (complexity=volume) face of DSSYK
  static-patch holography. RESULT: it does NOT give MOND.
    * the maximal-slice response is LINEAR in M_b (computed: dV=6 pi G M_b R^2) -> cannot be the sqrt-law;
    * treating complexity as a direct gravitational source is unphysical (constant acceleration);
    * the sign heuristic I gave last pass is probably BACKWARDS (a baryon raises, not lowers, local
      complexity) -- retracted.
  The hypothesis 'de Sitter complexity supplies the MOND medium' is therefore NOT confirmed, and the
  easy version is falsified. It is not fully dead: a non-linear constitutive law (Verlinde-type) or a
  complexity-saturation mechanism near C_max could in principle restore the sqrt-law, but neither is
  supplied by complexity=volume and I will not manufacture one.

  WHAT WE LEARNED (the value of a negative result):
    - 'MOND needs a volume source' is necessary but the harder, decisive requirement is the AQUAL
      NON-LINEARITY (sqrt(M_b)); the leading CV response is linear, so it is the WRONG kind of medium
      at leading order.
    - the second-law-of-complexity SIGN is not obviously favorable -- and on this calculation it points
      the wrong way. Any future claim must reckon with dC>0 around a baryon.
    - the honest frontier is now narrower and sharper: not 'does complexity source MOND' (the leading
      answer is no) but 'does complexity SATURATION near C_max produce an AQUAL non-linearity' -- a
      much more specific question, and the only remaining opening.""")
    print("="*94)


def main():
    print("#"*94); print("# DSSYK / complexity=volume elastic response to a baryon -- an honest attempt"); print("#"*94 + "\n")
    part1_requirement(); part2_the_calculation(); part3_findings(); part4_what_would_rescue(); verdict()


if __name__ == "__main__":
    main()
