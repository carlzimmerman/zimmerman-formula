# PLT1 RESULT: the framework's enclosed mass at 100 kpc and beyond against the literature compilation of DESI DR2 Results III

2026-11-12. Criteria: `FROZEN_CRITERIA.md`, committed alone (e51543aa5e) before the script existed
and before any value in the `fig13/` literature files was read. TEST lane. Adopts nothing. Relabels
no other lane; row 32's status is not changed here. kappa = 1/2 FITTED; not theory closed.

## Labels

Median pull of each class, all rows with r >= 100 kpc, 20 per cent floor. H = field halo stars
(8 rows); S = satellites, globular clusters, streams (10 rows). Negative: line below the published
masses.

| case | H | S | headline |
|---|---|---|---|
| E1 canonical (Local Group field) | -0.68, PASSES | -1.56, PASSES, FRAGILE | **PASSES, FRAGILE** |
| E1 alt | -0.66, PASSES | -1.54, PASSES, FRAGILE | **PASSES, FRAGILE** |
| E0 canonical (no field) | +1.01, PASSES | +0.28, PASSES | **PASSES** |
| E0 alt | +1.34, PASSES | +0.61, PASSES | **PASSES** |

**The FRAGILE flag is the finding.** The graded set mixes six class-S rows at 100 kpc, where the
field reading has not yet saturated, with four at 200 to 273 kpc, where it has. On the pre-named
variant "rows with r >= 150 kpc only", class S under E1 **FAILS LOW** on both footings: pulls
-2.56, -2.88, -1.04, -3.20, median -2.72. On the canonical footing E1 also fails class S with the
10 per cent floor. With published errors and no floor the class-S median is -2.40 / -2.37.

The hand expectation written into the criteria (a split between the classes) was wrong for the
graded set: no case splits.

## The rows beyond 150 kpc, where the two readings differ

| class | r [kpc] | published mass [10^11 Msun] | source label, method | pull E1 (can) | pull E0 (can / alt) |
|---|---|---|---|---|---|
| H | 150 | 7.50 +/- 2.50 | Deason12b, Jeans | -0.80 | +0.95 / +1.22 |
| H | 200 | 6.80 +/- 4.10 | Bhattacharjee14, Jeans | -0.27 | +1.39 / +1.57 |
| H | 200 | 8.11 (+0.41, -0.50) | Hattori21, DF | -2.24 | +2.78 / +3.27 |
| S | 200 | 11.00 (+2.70, -2.20) | CorreaMagnus22, DF | -2.56 | +0.77 / +1.10 |
| S | 200 | 14.90 +/- 4.00 | Li25, DF | -2.88 | -0.23 / +0.03 |
| S | 240 | 7.90 +/- 2.30 | Makarov25, tracer mass estimator | -1.04 | +2.33 / +2.62 |
| S | 273 | 14.30 (+3.50, -3.20) | Fritz20, tracer mass estimator | -3.20 | +0.92 / +1.25 |

The line there: E1 5.25 to 5.27 x 10^11 on both footings; E0 10.4 / 11.4 at 150 kpc, 13.7 / 15.0 at
200 kpc, 20.4 / 22.4 at 300 kpc (canonical / alt).

- The field reading is below every one of the seven rows, and below four of them by more than two
  sigma.
- The no-field reading is above six of the seven on the canonical footing (all seven on alt) and
  beyond two sigma for two: Hattori21, by far the tightest row, and Makarov25.
- The published masses themselves span 6.8 to 14.9 x 10^11 at 200 to 273 kpc. The two tracer mass
  estimators from satellites differ by a factor 1.8 (7.9 at 240 kpc against 14.3 at 273 kpc).

## Reported, not graded

- **The paper's own NFW extrapolation** (7.53 / 9.65 / 11.27 x 10^11 at 100 / 150 / 200 kpc) passes
  both classes: medians +0.88 (H) and +0.09 (S). The two classes are therefore not in conflict with
  each other at this gate.
- **Field window, all rows:** both classes pass for e_N in [0, 0.0165] on both footings (H alone to
  0.0405). The record's 0.01273 and the rotation curve's [0, 0.008] are inside it.
- **Baryon amplitude that would centre a class under E1:** 1.34 / 1.32 for H and 1.65 / 1.59 for S
  (canonical / alt).
- **Matched-field value of today's correction lane** (4.94 / 4.95 x 10^11) against the rows at
  r >= 150 kpc: class-S pulls -2.78, -3.05, -1.21, -3.41 (median -2.91); class-H median -0.94.
- **Row 32's kill as first registered** (a measured M(<200 kpc) >= 1.0 x 10^12): three of the seven
  rows at r >= 150 kpc have central values at or above 1.0 x 10^12 (11.0, 14.9, 14.3, all class S);
  none is above it at two published sigma. The row gave no significance rule, so this is recorded
  and its status is left to its own record.

## Post hoc (after the graded run; not in the criteria)

`plt1_posthoc.out`: using only the rows at r >= 150 kpc, the class-S median pull reaches -2 at
e_N = 0.0078 on both footings (a plateau of 6.64 x 10^11); at e_N = 0.008 it is -2.04 and at the
record's 0.01273 it is -2.71. Class H allows fields up to 0.041. So the satellite and
globular-cluster masses beyond 150 kpc ask for a field no stronger than the rotation curve's own
upper bound (0.008), and are against the Local Group value the record uses. Three or four rows, a
20 per cent floor, and a statistic chosen after seeing the graded output: a pointer, not a result.

## Checks

KA1 to KA5 pass on the first run (file hash; the fig13 joint file matches Table 4 to 0.005; the
ported baryon model gives 6.6814 x 10^10 and M_sph/M_b = 0.9777, 0.9972; the line reproduces the
record at 80, 150, 200 and 300 kpc to 0.011 per cent and the closed-form plateau 5.276 x 10^11 to
0.05 per cent; synthetic rows). M1 and M2 bite in both classes (`plt1_mut.out`): a field of 0.05
fails low (medians -2.23 in H, -3.93 in S) and a flat speed doubled fails high (+5.1 to +5.6).
Hand checks in SI: E0 canonical at 200 kpc 1.373 x 10^12 (script 13.72); pulls of the 200 kpc and
273 kpc class-S rows -2.56 and -3.20 (script the same).

## Limits

- The rows are published Newtonian enclosed masses. The distribution-function rows assume a halo
  form and are partly extrapolations; the compilation does not say how far each is constrained by
  its tracers.
- The rows are not independent (shared tracers and Gaia data); the median pull is a summary, not a
  significance.
- The field reading's angle average is exact only for tracers spread isotropically about the field
  direction. The satellites are not, and along the field G239 finds the apparent mass much higher
  than the average. Whether that raises or lowers what a satellite analysis reports depends on
  where the satellites sit relative to the field, which this lane does not compute.
- The 20 per cent floor is a choice. The 10 and 30 per cent variants are in the output.
- "FRAGILE" compares PASSES, FAILS LOW and FAILS HIGH; the "(beyond 3)" tag is not treated as a
  label change.
- Baryons are the McMillan 2017 census at A = 1; hot halo gas is not in it.

## Files

`FROZEN_CRITERIA.md`; `plt1.py` (takes the path of the Zenodo zip; the zip is not stored here; md5
5b0cc3aa9947286eb9348e947d01182d); `plt1.out`; `plt1_results.json`; `plt1_mut.out`;
`plt1_posthoc.py`, `plt1_posthoc.out` (post hoc, labelled).
