# EUC9 AMENDMENT A1 (POST HOC; disclosed)

2026-11-12. Written after a dry run of the frozen search on the first 52 spectra to arrive (the truth lens, 34 of S,
17 of X; a fixed random order) and after the truth lens's spectrum was inspected pixel by pixel. Committed alone,
before the amended search exists and before any other lens or grade-X spectrum has been inspected. The frozen criteria
(bea4eacfa8) and amendment A0 (82cf65da28) are not edited; the frozen search is still run to completion on all spectra
and its word reported as it falls.

## What was seen

- **The truth lens is not found by the frozen rule, on any rung.** So H4 fails and the frozen word will be
  NOT EVALUABLE whatever the nulls do.
- Its dither spectra show the predicted signature plainly. Two peaks at about 15,461 Å and 15,598 Å, each above 15 σ
  per pixel. Midpoint 15,530 Å = Hα at z = 1.3657 (DESI: 1.3657). Half-split 68.5 Å = 1.53″ (θ_E = 1.51″). In the
  RGS000 dithers the blue peak is the stronger (34 σ against 14 σ); in the RGS180 dithers the red one (26 σ against
  14 σ): an arc and a fainter counter-image, mirrored between the two grism positions.
- **Why the frozen rule misses it.** The rule searches Euclid's own co-added spectrum and asks for NDITH ≥ 3 at both
  line centres. The pipeline's co-addition drops dithers where they disagree: at the blue peak NDITH = 2, and the red
  peak's central pixel is flagged "do not use" with NDITH = 0. A mirrored line is, by construction, a place where the
  two grism positions disagree. The frozen rule was pointed at the one product from which the signature is removed.
- Also seen, as counts only: in the 51 other spectra the frozen rule gave one pair in S and none in X; the injection
  checks passed except I2 (2 of 34 on that subset). No other spectrum was looked at.

## The amendment

**A1.1 Input.** The search runs on a re-co-addition of each object's dither spectra without rejection: each dither is
prepared exactly as §3 of the criteria prepares a spectrum (same good-pixel rule, running-median continuum, error
rescaling); the residuals are averaged with inverse-variance weights; the co-added errors are rescaled once more by
max(1, 1.4826 × MAD of residual/error). A pixel is good if at least one dither is. A system needs at least one usable
dither in each grism position.

**A1.2 Rule.** The frozen pair fit, single-line alternative, tiers, half-split range, flux-ratio band, line identity,
windows and guards, unchanged, with one substitution: "NDITH ≥ 3 at both centres" becomes "both grism positions have a
good dither at both centres". **The dither test of A0.2 is required**: class SECURE-A1 = passes the rule on the
re-co-addition and passes D. Rungs: **A1-TA**, then **A1-TB**.

**A1.3 Gates,** in the same form: H2 (grade-X null, limit max(1, 20 % of the lens rate)), H2b (sign-flipped null,
dithers flipped), coverage, K1, K2, K5. Injections are made into the dither spectra and re-co-added: I1 mirrored
pairs (combined S/N 12) returned within 13.4 Å in ≥ 70 %; I3 the same passing D in ≥ 60 %; I2 a single centred line in
every dither returned as SECURE-A1 in ≤ 5 %; I4 a true doublet in every dither returned as SECURE-A1 in ≤ 5 %.
**H4 is kept as a check but is no longer evidence**: A1 was designed on the truth lens. Twins as frozen, run on A1.

**A1.4 Words.** The frozen search keeps its own word. A1 can only give **POST HOC READING (A1)**. If an A1 rung passes
its gates, EUC1-F and EUC5-F are computed with their thresholds and bands untouched and every word is labelled
"under A1 (post hoc)"; they are not the frozen gates' verdicts and close nothing.

**A1.5 What A1 cannot fix, stated.** A galaxy projected within the extraction and off the deflector's centre is
mirrored too. Only the grade-X null bounds it. Objects observed at more than one roll angle have their split smeared.

κ = ½ FITTED. No outcome favours the framework.
