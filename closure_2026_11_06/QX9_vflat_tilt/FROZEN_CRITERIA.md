# QX9 frozen criteria: the Vflat slope QX8 reported, against PAPER67's "no tilt with speed"

Frozen before any QX9 number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Read-only reuse of QX8's
parts (closure_2026_11_06/QX8_sparc_exact_field/parts, 3ba7c78ce6) and of qx8.py's loader and fitter.

## What the record measured (established by reading, before any QX9 number)

- PAPER67's "tilt with speed" (+0.02 canonical / -0.02 alt; FG1 row Tl, line |tilt| <= 0.15, [NR2]) is
  median(refit Upsilon | Vflat < 100) - median(refit Upsilon | Vflat > 150), on Q <= 2, Inc >= 30
  (FG1 fg1law_RUN_tail.py). It is a tilt of the FITTED MASS-TO-LIGHT RATIO with speed, not of residuals.
- QX8's "+0.21 to +0.26 per dex" is the coefficient b_V of log10 Vflat in a joint least-squares fit
  mres = a + b_SB log10 SBeff + b_V log10 Vflat, where mres is the per-galaxy weighted mean residual
  log g_obs - log g_pred at that galaxy's refit Upsilon (grid 0.30-1.20). It is a partial coefficient at fixed
  SBeff, on all galaxies with Vflat > 0 and SBeff > 0, with no quality cut.

## Questions and lines

Q1 (same quantity?). By definition Q1 is answered NO unless the computation below shows that QX8's mres slope
and FG1's Upsilon tilt are the same number up to sign and scale. This is reported, not graded.

Q2 (what drives b_V?). Compute on both footings, for the law and the exact field:
- S0: QX8's b_V reproduced (known answer KA1, |diff| <= 1e-6).
- S1: the simple slope of mres on log Vflat, without SBeff.
- S2: b_V with the FG1 quality cut (Q <= 2, Inc >= 30).
- S3: b_V at fixed Upsilon = 0.50 (no refit; mres at the fixed value).
- S4: b_V on the bulge-free subset (Vbul = 0 at every point).
- S5: b_V on the gas-dominated subset (median Vgas^2 > Upsilon 0.5 Vdisk^2 over the galaxy's points).
- S6: b_V on galaxies whose refit Upsilon is off the grid edges (0.30 < U < 1.20).
- S7 (the null): mocks. For each real galaxy, draw g_obs from the law (algebraic, same footing) at its fitted
  Upsilon, with Gaussian noise from SPARC's eV in velocity, run the SAME refit and SAME regression, and take
  200 mock realisations. The null distribution of b_V is the mock distribution.

Lines (both footings must agree for a label; law and exact field reported separately):
- ARTEFACT (b): the real b_V lies inside the central 95 % of the S7 mock distribution, OR the slope loses
  significance (|b_V| < 2 sigma, bootstrap 2000) under S3, or under S2 together with S6.
- REAL (c): the real b_V lies outside the central 95 % of the mocks AND it keeps |b_V| >= 2 sigma under S2, S3
  and S6.
- MIXED: anything else (reported with the per-check table).
- If (c), or if Q1 turns out YES, PAPER67's "no tilt with speed" needs an erratum draft
  (ERRATUM_DRAFT.md in this lane dir, for the owner; PAPER67 files are not edited).

## Controls (separate outputs)

- MUTATE: plant mres -> mres + 0.20 log10(Vflat/100) in the mocks (as a velocity-dependent multiplicative factor
  on g_obs before refit). The pipeline must recover b_V within 0.20 +- 0.07 (median over mocks), or no verdict
  stands.
- KA1 above.

Compute: at most 2 threads, nice -n 15.
