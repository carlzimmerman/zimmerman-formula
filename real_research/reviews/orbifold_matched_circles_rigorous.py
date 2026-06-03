#!/usr/bin/env python3
"""
The 20.6 Gpc T^3/Z2 ORBIFOLD vs matched circles -- Carl's two loopholes, checked from first principles.
=======================================================================================================
Carl asked, sharply: (1) did the searches look for circles at the SCALE a 20.6 Gpc box predicts? and
(2) is the "20.6 Gpc" really the MIRROR half-cell, so the true periodicity is 41.2 Gpc and the circles
are pushed out of reach? He asked for direct proof it is WRONG. Honest finding after the calculation:
it is NOT wrong -- the exclusion holds -- and here is exactly why each loophole fails, computed. (I do
not manufacture a refutation to please; the loopholes are good physics and they are checked, not waved.)

Construction (from the repo): T^3 with a SYMMETRIC CUBE edge L_c = 20.6 Gpc (L_x=L_y=L_z; the docs lock
this), quotiented by Z2 = point inversion y -> -y (the 8 fixed points (0 or pi)^3 prove it). The Z2
HALVES the fundamental domain.
Planck 2015 XVIII (arXiv:1502.01593, VERIFIED): matched-circle search has alpha_min ~ 15 deg and excludes
at 99% CL any topology with back-to-back circles larger than that; cubic-T^3 limit R_i > 0.97 chi_rec.
Needs numpy.
"""
import numpy as np

CHI = 14.0                       # comoving distance to last scattering, Gpc (Planck)
ALPHA_MIN = 15.0                 # Planck matched-circle sensitivity floor, deg (arXiv:1502.01593)


def alpha_deg(d):
    """Angular radius of the matched-circle pair from a copy at distance d. cos a = (d/2)/chi."""
    x = (d/2)/CHI
    return np.degrees(np.arccos(x)) if x <= 1 else None


def main():
    print("="*90)
    print("20.6 Gpc T^3/Z2 orbifold vs matched circles -- the two loopholes, computed")
    print("="*90)
    print(f"  chi_rec = {CHI} Gpc; circles exist iff a copy is within 2*chi = {2*CHI} Gpc; cos(alpha)=(d/2)/chi.")
    print(f"  Planck search: alpha_min ~ {ALPHA_MIN} deg, both orientations, 99% CL; cubic-T^3 bound R_i>0.97 chi.\n")

    print("  LOOPHOLE 1 -- 'did they search at the right SCALE?'  (you, paraphrased)")
    print("    The 20.6 Gpc cube's nearest copies and the circles they make:")
    L = 20.6
    for nm, d in [("face translation  L", L), ("face diagonal  sqrt2 L", np.sqrt(2)*L),
                  ("body diagonal sqrt3 L", np.sqrt(3)*L)]:
        a = alpha_deg(d)
        s = f"alpha = {a:.1f} deg  ({'IN the 15-90 search range, peak sensitivity' if a and a>ALPHA_MIN else 'below floor'})" if a else "NO circle (copy beyond 2 chi)"
        print(f"      {nm:24} d={d:5.1f} Gpc  ->  {s}")
    print(f"    ANSWER: yes. The dominant circles sit at alpha={alpha_deg(L):.1f} deg -- squarely inside the searched")
    print("      15-90 deg band, where the search is MOST sensitive. The scale was covered. None were found.\n")

    print("  LOOPHOLE 2 -- 'is 20.6 the MIRROR half-cell, so the true torus is 41.2 Gpc?'  (your key idea)")
    print("    Suppose the translation lattice were 41.2 Gpc (20.6 = the half-cell). Then:")
    a41 = alpha_deg(41.2)
    print(f"      pure translation  d=41.2 Gpc -> {'NO circle (41.2 > 28)' if a41 is None else f'alpha={a41:.1f}'}  <-- your loophole WORKS, for the translations.")
    print("      BUT the Z2 inversion y->-y is still there, and it maps the observer to a copy at distance")
    print("      2|y0 - (nearest fixed point)| <= the cell size. A copy reappears within ~20.6 Gpc:")
    for nm, d in [("Z2 mirror, generic observer", 20.6), ("Z2 mirror, near a fixed point", 10.3)]:
        print(f"        {nm:30} d={d:5.1f} Gpc -> alpha = {alpha_deg(d):.1f} deg  (IN range)")
    print("    ANSWER: the mirror REINTRODUCES the circles the doubled translations removed. Doubling the")
    print("      cell to dodge the translation circles just hands them back through the inversion. No escape.\n")

    print("  THE INTERPRETATION-ROBUST REASON (why no relabelling can save it)")
    Ri_torus = L/2                  # the generous reading: inscribed radius of the CUBE
    Ri_orb = L/4                    # the orbifold domain is HALF the cube -> smaller R_i
    print(f"    The binding quantity is R_i, the inscribed-sphere radius of the FUNDAMENTAL DOMAIN.")
    print(f"      cube (torus) reading:    R_i = L/2 = {Ri_torus:.1f} Gpc")
    print(f"      orbifold-domain reading: R_i = L/4 = {Ri_orb:.1f} Gpc   (Z2 HALVES the domain -> even smaller)")
    print(f"    Planck requires R_i > 0.97 chi = {0.97*CHI:.1f} Gpc. Both readings fail:")
    print(f"      {Ri_torus:.1f} Gpc is short by {(0.97*CHI-Ri_torus)/(0.97*CHI)*100:.0f}%;  {Ri_orb:.1f} Gpc by {(0.97*CHI-Ri_orb)/(0.97*CHI)*100:.0f}%.")
    print("""    Key point: R_i < chi_rec means the last-scattering sphere does NOT fit inside one fundamental
      domain, so SOME identification -- translation OR mirror -- MUST bring a copy within 2 chi and make
      matched circles. The Z2 only ADDS identifications and SHRINKS the domain; it can only LOWER R_i,
      never raise it above chi_rec. So the mirror makes exclusion EASIER, not harder.\n""")

    print("="*90)
    print("HONEST VERDICT")
    print("="*90)
    print(f"""  You asked for proof it is WRONG. After the calculation, the honest result is that it is RIGHT, and
  your two loopholes both fail for concrete, computed reasons:
    1. the circles are at alpha = {alpha_deg(L):.1f} deg -- inside the 15-90 deg searched band, peak sensitivity;
    2. doubling the cell to 41.2 Gpc removes the translation circles but the Z2 MIRROR reinstates a copy
       at <= 20.6 Gpc, so the 42.6 deg circles return;
    3. robustly, R_i = 10.3 Gpc (or 5.1 for the true orbifold domain) < 0.97 chi = 13.6 Gpc, and the Z2
       can only shrink the domain. There is no relabelling that lifts R_i above chi_rec.
  I will not manufacture a refutation. The 20.6 Gpc T^3/Z2 orbifold is excluded by the Planck matched-
  circle search -- and the Z2 mirror, far from rescuing it, makes the case stronger. The questions were
  exactly the right ones to ask; this is what checking them rigorously returns.""")
    print("="*90)


if __name__ == "__main__":
    main()
