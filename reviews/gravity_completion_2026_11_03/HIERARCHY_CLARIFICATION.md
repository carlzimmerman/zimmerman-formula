# Normalization clarification to the coupling-hierarchy reduction

The extremum in COUPLING_HIERARCHY.md is for m_chi/sqrt(F_eff), hence for mass
at fixed true F_eff or fixed raw F_eff²=rhoDE. Its sentence about the "largest
leading mass" is read with this constraint. It is not a statement that equal
couplings maximize the mass at fixed superpotential f.

At fixed f, the leading mass instead scales as
lambda³ sqrt(h/(30h²+lambda²)); its h derivative changes sign at
h=lambda/sqrt30. This does not alter the raw-DE bound, whose normalization
holds F_eff rather than f fixed. The independent exact review is
hierarchy_review/REVIEW.md and its bounded symbolic record. Numerical
run_hierarchy uses the correct fixed-F ratio throughout; its saved bytes and
original derivation input remain unchanged.
