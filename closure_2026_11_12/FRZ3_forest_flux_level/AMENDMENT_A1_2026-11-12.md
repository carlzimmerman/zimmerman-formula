# FRZ3 AMENDMENT A1 (2026-11-12): a density floor in the flux step

Committed alone, after the criteria (e56c67ae91) and before any graded number. Cause: the scratch smoke run of the anchor
code at the frozen grid stopped with NaN optical depths in the mutation field B = R + 2 (L - R). Doubling the difference
makes the density negative where rule 5 takes more than half of a halo centre's mass out (L < R / 2), and the FGPA power
law (1 + delta)^beta and the temperature (1 + delta)^(gamma - 1) are undefined there. The same can happen in the reading-V
bracket field R + (V - RV). No ratio from the smoke run was opened.

Change: in the flux step every gas density is floored at 1 + delta = 1e-3 before tau and T are computed; the number and
fraction of floored pixels is recorded for every field. The primary reference and rule 5 fields are still asserted
strictly positive before the flux step (unchanged), so the floor cannot act on them and the graded label is unaffected by
this amendment. "Both readings": without the floor the affected mutation / bracket fields have no defined flux (NaN), so
the only reading that exists is the floored one; RESULT reports the floored fraction beside each affected number.

Nothing else changes.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
