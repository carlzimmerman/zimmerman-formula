# =====================================================================
# TEST G — THE MOST HOSTILE CHECK: does hyperfiniteness ITSELF auto-supply
# state-matching? (steelman the REDUCTION, then test it to destruction)
#
# Steelman: In R (hyperfinite II_1), is the action of Aut(R) on faithful
# normal states transitive enough that ANY two states with the same modular
# spectrum are conjugate by an automorphism? If YES, then 'both R + same
# modular data' => phi automatic, and hyperfiniteness REDUCES phi to spectrum.
# =====================================================================
print("=== TEST G: does Aut(R) transitivity reduce phi to spectrum-matching? ===\n")

print("THE RELEVANT THEOREM (Connes-Stormer; Connes uniqueness of R):")
print(" - On the HYPERFINITE II_1 factor R, TWO faithful normal states with the")
print("   SAME modular spectrum (same S-invariant / same eigenvalue list of the")
print("   density, INCLUDING MULTIPLICITIES) ARE conjugate by an automorphism of R.")
print(" - PROOF INGREDIENT: R is AFD, Aut(R) acts with dense orbits; the modular")
print("   invariant is complete for the PAIR (R, state) up to conjugacy.")
print()
print("=> So IF (and only if) the two boost spectra match WITH MULTIPLICITIES,")
print("   the state-matching automorphism EXISTS. Hyperfiniteness DOES reduce phi")
print("   from 'construct an iso' to 'CHECK the modular spectra (w/ multiplicity)")
print("   coincide' -- a genuine, real reduction. THIS IS THE POSITIVE HALF.")
print()
print("=== BUT THE RESIDUAL CONDITION IS NOT FREE -- it is exactly the hard data ===")
print("The check that must hold for the automorphism to exist:")
print("  (R1) chord algebra is hyperfinite R  [TEST F: PLAUSIBLE-NOT-PROVEN]")
print("  (R2) chord boost spectrum = dS boost spectrum INCLUDING MULTIPLICITIES")
print("       [TEST D: dS side has INFINITE tower-degeneracy; the chord side must")
print("        reproduce the SAME (Delta+n) ladder with the SAME multiplicity per")
print("        level -- this is the FULL n-point spectral match agentUU's GAP B")
print("        already showed imports the WHOLE dictionary (R slides 11-147 over")
print("        KMS-consistent line shapes unless EVERY moment matches).]")
print("  (R3) the conjugating automorphism must be INNER-compatible with the")
print("       observer dressing / center placement [agentTT: edge sector survives;")
print("       TEST C/E: centralizer gauge moves the placement observable].")
print()
print("=== NET ===")
print("Hyperfiniteness REDUCES phi: 'does an iso exist' -> 'do the modular spectra")
print("match with multiplicity (+ chord is R)'. That is a REAL reduction in KIND")
print("(from constructing an iso to checking an invariant).")
print("BUT the resulting CHECK is NOT lighter than agentUU's GAP B: matching the")
print("boost spectrum WITH MULTIPLICITIES = matching every n-point function =")
print("the full state-level dictionary. The reduction changes the PROBLEM TYPE")
print("(existence -> invariant-match) but NOT the DIFFICULTY (still the whole")
print("dictionary). And it adds a NEW unproven premise (chord = R, not L(F_n)).")
