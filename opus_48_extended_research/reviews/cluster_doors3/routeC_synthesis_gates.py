#!/usr/bin/env python3
r"""
ROUTE C -- MULTI-FIELD no-particle dark sector: FOUR-GATE synthesis.
====================================================================
Pulls the three sub-route results into the G1-G4 ledger. Both ways. Quarantine held.
"""
print("="*100)
print("ROUTE C -- multi-field no-particle dark sector vs the ~30-49% gas-tracking core residual")
print("FOUR-GATE LEDGER (G1 sufficiency, G2 galaxy-veto, G3 no-new-particle, G4 data)")
print("="*100)
rows = [
 ("C(a) AeST aether VECTOR A_mu",
  "G1 FAIL", "G2 squeeze", "G3 PASS (own field)", "G4 FAIL (shape)",
  "Eling-Jacobson: spherical aether is timelike, curl vanishes -> ONLY the mu^2 mass term. That term "
  "~(mu r)^2 -> ~0.1-0.5% of the CORE residual (only O(1) at R500); rho_aether is centrally HOLLOW "
  "(rises outward, then NEGATIVE) = anti-gas-tracking. Same falsified-as-closure mass term, now dead in the core."),
 ("C(b1) 2nd scalar, FIXED-length Yukawa",
  "G1 PASS (alpha~1)", "G2 FAIL (a0 +0.30dex)", "G3 PARTIAL (relocates)", "G4 FAIL (shape OR Cassini)",
  "alpha~0.98 fills the core BUT a UNIVERSAL coupling shifts the SPARC RAR/BTFR a0 by +log10(1+alpha)=+0.30 dex "
  "(1.85x the welded 9.36e-11) -> shatters the a0=Lambda weld (scatter-invisible, normalization-fatal). And a "
  "universal coupling tracks TOTAL baryons = stars -> NOT gas-tracking. Gas-tracking needs composition-dependence "
  "-> Cassini |gamma-1| exceeded ~5 orders, no screening window (Sun denser/heavier than cluster core)."),
 ("C(b2) 2nd scalar, DENSITY-triggered (chameleon)",
  "G1 maybe", "G2 FAIL (env order)", "G3 PARTIAL (new V)", "G4 FAIL",
  "Galaxy/solar cores are ~275-1e5x DENSER than cluster cores -> any density-triggered clustering fires in "
  "GALAXIES FIRST (the density-a0 graveyard). No threshold is cluster-core-ON/galaxy-OFF. Adding V(chi) breaks "
  "shift symmetry = new structure."),
 ("C(c) bimetric / massive-graviton partner",
  "G1 maybe", "G2 FAIL", "G3 FAIL (new spin-2)", "G4 FAIL",
  "Same universal-vs-composition/Cassini dilemma as the scalar; PLUS Higuchi-ghost instability in the nonlinear "
  "cluster regime; a new spin-2 species with 5 dof = relocates fully. c_GW=c forces a tuned Mpc scale."),
 ("[ref] framework's OWN K(Q) dust (already in stack)",
  "G1 partial", "G2 PASS", "G3 PASS", "G4 FAIL (shape)",
  "The framework's second field IS the K(Q) Q-sector dust (CMB-fitting, cold w=0). It is CDM-like by "
  "construction -> tracks total matter, NOT the gas. Its amplitude I0 is a FREE integration constant "
  "(orthogonal to a0). Already credited in the ~17-20% Y-Q boost; cannot be made gas-tracking."),
]
for name,g1,g2,g3,g4,note in rows:
    print(f"\n  {name}")
    print(f"    {g1:18}{g2:22}{g3:24}{g4}")
    print(f"    {note}")

print("\n"+"="*100)
print("THE STRUCTURAL THEOREM (why NO multi-field no-particle closure works -- both ways)")
print("="*100)
print(r"""
  The core residual demands a field that simultaneously:
   (1) supplies ~41% extra mass IN THE CORE (50-420 kpc),
   (2) TRACKS THE GAS (centrally smooth ~10x-gas, M_res/M_star rising 15-30x outward), and
   (3) does NOT do (1) in galaxies (galaxy-veto) or the solar system (Cassini).

  A second gravitational field can discriminate cluster-core from galaxy/solar ONLY by:
   (A) a LENGTH scale (Yukawa range)  -> but a fixed length is universal across baryons
       => tracks STARS not gas (fails 2) AND, if range>=galaxy, re-bends the galaxy a0 (fails 3); 
   (B) a DENSITY scale (chameleon)    -> but cluster cores are LESS dense than galaxy/solar cores
       => fires in the wrong place (fails 3, the density-a0 graveyard); 
   (C) a COMPOSITION scale (gas vs stars) -> the ONLY way to satisfy (2), but it is a 
       composition-dependent fifth force => Cassini-excluded by ~5 orders, no screening window 
       (any screen that saves the Sun also screens the less-dense/lighter-enclosed cluster core).
  There is NO fourth discriminator. The three available scales each fail one of (2) or (3).
  => the gas-tracking core residual is structurally inaccessible to ANY no-particle multi-field
     extension that stays galaxy- and Cassini-safe. The closure RELOCATES (a 2nd field is undrived
     structure) AND breaks a gate. Confirms the residual is the irreducible shared-MOND core gap.
""")
print("  ROUTE C NET VERDICT: NO multi-field no-particle closure passes all four gates.")
print("  G1 reachable (alpha~1) but only by a universal coupling that FAILS G2 (a0 +0.30 dex) or a")
print("  composition coupling that FAILS G4-Cassini. The gas-tracking shape (G4) is the structural")
print("  wall: a clustering field tracks stars or density, never the gas, without a new SM coupling.")
print("  Both ways: hunted alpha/l_chi/density/composition/bimetric HARD; each breaks a named gate.")
print("  Quarantine held: a0/Z/kappa/I0 never asserted derived. CLOSES_RESIDUAL = NO.")
