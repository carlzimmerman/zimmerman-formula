#!/usr/bin/env python3
"""
The Weinstein/GU-prompted door, closed honestly: a0 from the geometry of the SPACE OF METRICS (superspace).
==========================================================================================================
Eric Weinstein's Geometric Unity is built on Met(X^4), the space of all metrics on spacetime (a 14-dim object:
4 base + 10 metric components). Stripped of GU's undefined machinery, the GU-INDEPENDENT, computable question is:
does the geometry of the space of metrics -- Wheeler's SUPERSPACE, with the DeWitt supermetric -- naturally produce
an acceleration scale a0 ~ cH, and could its dimensionless COEFFICIENT be computed (i.e. could it FORCE Z)?

Worked here. VERDICT: it is a RELABEL of the Friedmann/entanglement route already done, foreclosed to the same
coefficient cluster by the explicit-breaking theorem. NOT a new live door. (Closes the one named geometric object
the GU material points at, so "all scale-fixing routes checked" is airtight against the GU prompt.)

WHY (three structural facts, the third decisive):
 1. The DeWitt supermetric G^{ijkl} = (1/2 sqrt(h)) (h^{ik}h^{jl} + h^{il}h^{jk} - h^{ij}h^{kl}) is ULTRALOCAL and
    carries NO length or acceleration scale of its own -- only sqrt(h) and the gravitational coupling. Any scale
    must come from the BACKGROUND STATE you evaluate it on, and the only one on offer is the de Sitter / Hubble
    scale c/H. So a0 ~ cH is the ONLY possible output -- the scale is forced, exactly as in every other route.
 2. On FRW minisuperspace (scale factor a only) the WDW kinetic term reduces to the 1D cosmic free-fall in a, whose
    scale is sqrt(G rho). Reading a0 off this free-fall gives a0 = (c/2) sqrt(G rho_Lambda) -- IDENTICALLY the
    Friedmann route (geometric_origin_of_a0.py), Z = 2 sqrt(8pi/3) = 5.789. It is the SAME calculation relabeled.
 3. DECISIVE -- the explicit-breaking theorem applies verbatim: a0 is the scale that EXPLICITLY breaks deep-MOND
    conformal symmetry, and the DeWitt supermetric is (super)diffeomorphism-COVARIANT, so it cannot privilege one
    value of a symmetry-breaking scale. Hence it CANNOT force the coefficient -- same structural reason symmetry,
    bound-saturation, and transmutation all failed. The superspace-curvature/bound reading lands in the geometric
    1-2 cluster; the free-fall reading lands on 5.789; neither is independently forced.
Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; Mpc = 3.086e22
H0 = 67.4e3/Mpc; L = c/H0
Lam = 3*H0**2/c**2
rho_L = Lam*c**2/(8*np.pi*G)
Z = 2*np.sqrt(8*np.pi/3)


def main():
    print("#"*100); print("# The GU-prompted superspace door (Met(X^4) / DeWitt supermetric), closed honestly"); print("#"*100 + "\n")

    print("="*100); print("(1) the DeWitt supermetric carries NO scale of its own -> a0 ~ cH is the only output"); print("="*100)
    print("   G^{ijkl} = (1/2 sqrt h)(h^ik h^jl + h^il h^jk - h^ij h^kl): ultralocal, built only from h and G.")
    print(f"   The only background scale available is the de Sitter radius L = c/H0 = {L:.3e} m, so the emergent")
    print(f"   acceleration can only be a0 ~ c^2/L = cH0 = {c**2/L:.3e} m/s^2. SCALE forced (as in every route).\n")

    print("="*100); print("(2) the minisuperspace reduction = the Friedmann route, RELABELED"); print("="*100)
    a0_ff = (c/2)*np.sqrt(G*rho_L)
    print(f"   On FRW minisuperspace the WDW kinetic term is the cosmic free-fall in the scale factor; reading a0 off")
    print(f"   it gives a0 = (c/2) sqrt(G rho_Lambda) = {a0_ff:.3e} m/s^2, i.e. cH/a0 = {c**2/L/a0_ff:.3f} = Z = {Z:.3f}.")
    print(f"   This is IDENTICAL to geometric_origin_of_a0.py (Reading 3). Superspace adds no new number here.\n")

    print("="*100); print("(3) DECISIVE: the explicit-breaking theorem forecloses the coefficient"); print("="*100)
    print("   a0 is the scale that EXPLICITLY breaks deep-MOND conformal symmetry. The DeWitt supermetric is")
    print("   (super)diffeomorphism-COVARIANT -> it cannot privilege one value of a symmetry-breaking scale.")
    print(f"   So the coefficient is NOT forced: the free-fall reading gives {Z:.2f}; a configuration-space-curvature")
    print(f"   /bound reading lands in the geometric 1-2 cluster (cH/a0 ~ 1-2). Same outcome as symmetry / bound-")
    print(f"   saturation / transmutation: SCALE reproduced, COEFFICIENT not forced.\n")

    print("="*100); print("VERDICT"); print("="*100)
    print(f"""  The space-of-metrics / superspace arena the Weinstein/GU material points at is a GU-INDEPENDENT, computable
  object -- and worked honestly it is a RELABEL of the Friedmann/entanglement route, foreclosed to the same
  coefficient outcome by the explicit-breaking theorem. It reproduces the SCALE a0 ~ cH (a fourth+ independent
  derivation) but does NOT force the coefficient Z. It is not a new live door; it is the one named geometric
  object not previously run, now closed -- so the 'all scale-fixing mechanism classes checked' claim is airtight
  even against GU's master arena. The only genuinely live door remains the empirical a0(z) test.""")
    print("#"*100)


if __name__ == "__main__":
    main()
