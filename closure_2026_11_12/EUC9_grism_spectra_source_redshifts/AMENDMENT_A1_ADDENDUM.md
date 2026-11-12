# EUC9 AMENDMENT A1, ADDENDUM (POST HOC; disclosed)

2026-11-12. Written after amendment A1 (25d7f82cc2) was run on the truth lens alone and on the 31 field spectra, and
before it has been run on any other lens or grade-X spectrum. Committed alone. A1 itself is not edited.

## What was seen

On the truth lens, A1 finds the pair as predicted: midpoint 15,531.4 Å, half-split 67.0 Å = 1.50″ (θ_E = 1.51″),
components at 40.6 σ and 34.8 σ, flux ratio 1.15, dither statistic D = −6.4 (passes). On the 31 field spectra it finds
nothing, in either sign.

**But the line-identity step then calls the pair [O III]** (z = 2.1012), on an "[O III] 4960 partner" at 16.8 σ. That
partner is not there. The pair's separation (134 Å) happens to be close to the [O III] 4960–5008 spacing at this
wavelength (149 Å), so the partner template's red component sits on the wing of the main pair's blue peak and is
credited with its flux. There is nothing at the partner's blue component. Euclid's pipeline makes the same reading
(first solution 2.1144). DESI's [O II] doublet puts the source at 1.3657, where Hα is the midpoint.

## The correction

**A1.6** Under A1, every partner pair of the line-identity step ([O III] 4960; [S II], [O III] 5008, Hβ) is fitted
**jointly with the main pair's two components** (three fluxes, weighted least squares), and its S/N is the
significance of its own flux in that joint fit. A partner whose template cannot be separated from the main pair
(singular fit) is not counted. Thresholds unchanged (S/N ≥ 3; the 4960 flux 0.15 to 0.6 of the pair's).

The frozen search keeps its frozen identity step. This is a second repair made on the one truth lens; with A1 it is
post hoc and can only feed a POST HOC READING (A1).

κ = ½ FITTED. No outcome favours the framework.
