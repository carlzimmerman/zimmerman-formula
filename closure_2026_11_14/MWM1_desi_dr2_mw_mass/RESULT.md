# MWM1 RESULT: the framework's Milky Way line against DESI DR2's halo-free enclosed mass, 20-80 kpc

2026-11-14. TEST lane. Adopts nothing, relabels nothing (DR2REV, NMB1, RAW1, MWJ1, MWG1, MWT1, RRL2 keep their
labels), does not edit the scorecard, registers nothing. Criteria `FROZEN_CRITERIA.md` (d749c46dcf, alone, before
any script or number). Script and transcribed numbers d01ac83061 (committed before any run). One graded run
(`mwm1.out`, `mwm1_results.json`), twins and mutations in `mwm1_MUTATE.out`. A second run reproduced
`mwm1.out` and `mwm1_results.json` byte for byte. No amendment. Not pushed. Not blind: DR2REV and NMB1 had
already looked at the same release (disclosed in the criteria, section 1).

## Words (as frozen; FW census = primary case; standing a0 9.3603e-11 / 1.1312e-10)

| case | canonical | alt |
|---|---|---|
| **FW census** | **NO VERDICT, FRAGILE** | **NO VERDICT** |
| FW rc (reported beside it) | NO VERDICT, FRAGILE | NO VERDICT, FRAGILE |
| Newton, baryons only | STILL FAILS [all 13 radii LOW, z -7 to -16] | (same baryons) |

- **Against DESI's halo-free curves alone, the census line passes every radius on both footings.** It is low
  everywhere on canonical (z -1.0 to -1.8; worst at 45 kpc) and within 1.1 sigma on alt.
- **Canonical gets NO VERDICT from the tracer split.** The RR Lyrae-only data (NIMBLE-A RRL plus NIMBLE-B RRL)
  put 40 and 45 kpc LOW. The BHB-only data pass.
- **Alt gets NO VERDICT from the independent survey.** Li et al. (LAMOST + SDSS + DESI) report an uncorrected mass
  of 4.78e11 at 82 kpc. The line sits 2.19 sigma above it (HIGH). With Li et al.'s own mock correction
  (+13.7 per cent) the line passes (z +1.07).
- **FRAGILE on canonical.** Three brackets that raise DESI's mass turn the row into STILL FAILS: cold debris x1.10
  at r >= 40 kpc, beta -0.1, and flattening x1.05.
- **The gate has power.** The mutations bite: line x0.8 gives LOW at 13 of 13 radii (census, both footings), and
  data x1.5 beyond 50 kpc gives LOW there. The null twins pass in 198 of 200 draws.
- The frozen words are NO VERDICT on both footings. A pass by DESI's own curves is a HIT for the framework, not a
  pass of the theory. It awaits an independent re-grade.

## The table (FW census; masses in 1e11 Msun; D = mean of the four NIMBLE curves; sigma in dex)

| r [kpc] | DESI D (NIMBLE) | Table 4 joint (report only) | FW census can | FW census alt | Newton | sigma | z can / alt | word can / alt |
|---|---|---|---|---|---|---|---|---|
| 20 | 1.996 | 1.94 | 1.639 | 1.766 | 0.629 | 0.064 | -1.34 / -0.84 | PASS / PASS |
| 25 | 2.277 | 2.30 | 1.987 | 2.149 | 0.644 | 0.046-0.047 | -1.27 / -0.54 | PASS / PASS |
| 30 | 2.568 | 2.65 | 2.331 | 2.527 | 0.653 | 0.042 | -1.00 / -0.17 | PASS / PASS |
| 35 | 2.988 | 3.05 | 2.672 | 2.902 | 0.659 | 0.042 | -1.16 / -0.30 | PASS / PASS |
| 40 | 3.592 | 3.54 | 3.011 | 3.274 | 0.662 | 0.045 | -1.72 / -0.90 | PASS / PASS |
| 45 | 4.122 | 4.08 | 3.347 | 3.645 | 0.664 | 0.049 | -1.83 / -1.09 | PASS / PASS |
| 50 | 4.593 | 4.51 | 3.683 | 4.014 | 0.665 | 0.059 | -1.62 / -0.99 | PASS / PASS |
| 55 | 5.005 | 4.88 | 4.019 | 4.383 | 0.665 | 0.061-0.062 | -1.55 / -0.94 | PASS / PASS |
| 60 | 5.328 | 5.19 | 4.353 | 4.751 | 0.666 | 0.060 | -1.46 / -0.83 | PASS / PASS |
| 65 | 5.633 | 5.56 | 4.688 | 5.119 | 0.666 | 0.055 | -1.45 / -0.76 | PASS / PASS |
| 70 | 5.902 | 5.88 | 5.022 | 5.486 | 0.666 | 0.051 | -1.39 / -0.63 | PASS / PASS |
| 75 | 6.132 | 6.14 | 5.356 | 5.854 | 0.666 | 0.048 | -1.23 / -0.42 | PASS / PASS |
| 80 | 6.343 | 6.36 | 5.691 | 6.221 | 0.666 | 0.046 | -1.01 / -0.18 | PASS / PASS |

sigma = sqrt(s_D^2 + s_spread^2 + s_FW^2). s_D is Table 4's error (0.021-0.035 dex). s_spread is the scatter of
the four NIMBLE curves (0.022-0.051 dex, largest at 20 and 50-60 kpc). s_FW is the 10 per cent baryon range
(0.023-0.027 dex). FW rc: z from -0.78 to +0.30 (canonical) and -0.47 to +0.62 (alt), with every radius PASS in
the primary data. The per-radius points are strongly correlated. They are not independent tests.

Table 4's joint, graded with the same rule but without s_spread (it carries emPDF's NFW and GME's power law, so it is
reported only): census canonical STILL FAILS [40-60 LOW] (z down to -2.56 at 45); census alt passes (worst -1.46).
This reproduces DR2REV's post hoc reading in frozen form.

## Alternatives (NO VERDICT triggers) and brackets (FRAGILE triggers), FW census

| run | canonical | alt |
|---|---|---|
| primary (four NIMBLE curves) | PASSES | PASSES |
| T1 RRL only | **STILL FAILS [40 LOW, 45 LOW]** | PASSES |
| T2 BHB only | PASSES | PASSES |
| T3 Li et al. at 82.25 kpc, uncorrected (D 4.78) | PASSES (z +1.51) | **STILL FAILS [80 HIGH]** (z +2.19) |
| T3c Li et al. with their mock correction (D 5.54) | PASSES | PASSES |
| B1 AuriDESI bias correction undone | PASSES | PASSES |
| B2 LMC disequilibrium, D x0.90 | PASSES | PASSES |
| B3 LMC at its maximum, D x0.80 at r >= 50 | PASSES | PASSES |
| B4 cold debris, D x1.10 at r >= 40 | **STILL FAILS [40-75 LOW]** | PASSES |
| B5+ beta +0.1 (D x0.953) | PASSES | PASSES |
| B5- beta -0.1 (D x1.047) | **STILL FAILS [40, 45 LOW]** | PASSES |
| B6- flattening, D x0.95 | PASSES | PASSES |
| B6+ flattening, D x1.05 | **STILL FAILS [40, 45 LOW]** | PASSES |
| B7 GME added at 50-80 | PASSES | PASSES |
| B8 hot gas (Miller and Bregman 2015) on the line | PASSES | PASSES |

FW rc's FRAGILE comes from B3: D x0.80 beyond 50 kpc puts the line HIGH at 80 kpc (canonical) and at 75 and 80 kpc
(alt). FW rc also fails T3 HIGH on both footings.

## Red-team of the data team's assumptions (each was written as a bracket before the run)

- **Equilibrium and the LMC (B2, B3).** The paper says neither its methods nor its mocks capture the LMC, and it
  cites biases "up to 20 per cent" (Section VII.3). Lowering DESI's mass helps the census line on both footings.
  It hurts FW rc only at the extreme.
- **The AuriDESI correction (B1).** It is calibrated on LCDM haloes. The NIMBLE corrections are only 2-4 per cent,
  and undoing them changes no word.
- **Cold or unrelaxed debris and beta (B4, B5).** These are the assumptions that matter for canonical. If DESI's
  outer mass is underestimated by about 5-10 per cent, canonical fails at 40-45 kpc.
- **BHB vs RR Lyrae (T1, T2).** The split is driven by NIMBLE-A RRL. It is 4.64 at 45 kpc, against 3.84-4.11 for
  the other three curves. The paper attributes NIMBLE-A RRL's fast rise to its tracer-density reconstruction (VI.1).
  That is the paper's reading, not tested here.
- **DESI vs LAMOST (T3).** Li et al.'s halo-free masses at 82 kpc (4.5-5.2e11, statistical errors only) sit 25 per
  cent below DESI at 80. That puts the alt line HIGH there unless Li's own 12-16 per cent mock correction is applied.
  The two surveys bracket the line from both sides.
- **Spherical symmetry (B6).** It moves canonical at 40-45 kpc at the 5 per cent level.

## Reported diagnostics

- External field (owner's actual-field reading): nu(sqrt(y^2 + e_N^2)) / nu(y) is between 0.999975 and 0.9999999
  at all 13 radii on both footings (y = 0.234 at 20 kpc to 0.0155 at 80 kpc, canonical). The no-field line is exact
  to 3e-5 here.
- At RAW1-rounded a0 every word is unchanged.
- 100 kpc (report only; DESI has no halo-free number there): FW census 7.03 (canonical) / 7.69 (alt), FW rc 7.86 /
  8.24, Newton 0.67. GME's extrapolated power law gives 7.4 (BHB) and 6.2 (RRL).
- Not graded (NFW-based): M200c = 1.19e12, emPDF, Li et al.'s M200. The framework has no virial mass to compare.

## Known answers, twins, mutations

KA1-KA5 all pass. RAW1's line is reproduced to 1e-4 at 30, 50 and 80 kpc. M = g r^2 / G in SI matches M_of_g. DESI
6.36e11 at 80 kpc is v_c = 184.9 km/s. The zip's sha256 matches DR2REV's and NMB1's record. fig11 reproduces
Table 4. NMB1's NIMBLE values at 30 and 80 kpc are reproduced exactly. TW0 passes. TW1 passes in 198 of 200 draws.
MU1 bites on all four cases. MU2 bites on both footings.

## Limits

- The 13 radii are one correlated curve, so no single significance is formed.
- s_D is the joint's calibrated error. A NIMBLE-only combination is less precise: NMB1 found 0.057 dex at 80 kpc.
  So the PASSes are, if anything, conservative and the LOWs generous.
- The DESI curves are spherical-Jeans fits, bias-corrected on LCDM mocks. The NIMBLE paper is "in preparation", so
  the curves are taken from the authors' figure data (Zenodo 10.5281/zenodo.23712180), not from a table.
- The McMillan 2017 census is the baryon model; its uncertainty enters only as 10 per cent.
- The hand estimate (canonical borderline, alt passes) was close. Canonical's primary row passes, with its worst
  point at -1.8 sigma.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
