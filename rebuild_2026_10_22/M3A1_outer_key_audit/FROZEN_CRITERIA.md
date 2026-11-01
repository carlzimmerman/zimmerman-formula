# M3A1_outer_key_audit: frozen criteria (data-side audit of G-OUT-M3, no new mechanism, no new data)

Written before any script of this lane. NOT BLIND: ZN4's, DR6's, X7's, LF1's, GS4's, BA1's numbers are known to me, including X7's stored M3 OUTER numbers for the C* template (rand_t -0.070, Z_rand_t -2.03; leakT_t +0.069; s_CAL = s_STAT; s_CONS 0.129), which I read while choosing candidates. kappa = 1/2 FITTED, unused here beyond the chain. Cold dark energy, no particle. Not theory closed.

## Question
Is the failure of ZN4 on measured gas (+0.005) at G-OUT-M3, Z +4.41 / +4.13 (f* 0.034 / 0.0615, h 0.672; +4.07 / +3.81 at h 0.686), G-OUT-Mall and G-MID-T3 real, or a data-side artefact? Either direction counts: report if the audit makes it worse.

## Already tested, not repeated (only cited)
Global gas offset (GS4 +0.005 +- 0.017; GS5); one common slope (OG1: s 2.04 to 3.07 moves M3 by 0.37 in Z); boundary (VB1); resolution (ZN4); two-halo (DR6, GC1, RF4); mass definition (MA1); HSE (RF3, HL1, HL2, LF1); X7's all-cluster PSF regression and core-band calibration; X11, X13 source-size in MID; IC1's inner-band miscentring (not OUTER).

## Candidates, sizes taken from data on disk, no fitted amplitude
Class I = measured independently of the tangential cluster shear. Class K = from the key's own shear (a stability read, can't make a pass).

| id | what | how | class |
|---|---|---|---|
| C1a | Eddington / upscatter: M3 is cut on catalogue MGAS500 and the prediction takes the same noisy number per cluster | per-cluster error from MGAS500_L, _H; Tweedie shift E[x_true given x_obs] = x_obs + sigma^2 d ln p/dx on lg MGAS500, density from the 326; regrade with bin membership unchanged | I |
| C1b | the same, measured: pointed gas against eRASS1 in a window cut on eRASS1 MGAS500 at M3's edges, z in M3's range | gs4_matched.csv, GS4's unique-cluster rule; median, SE, slope against lg MGAS500 | I |
| C2a | gas at M3 alone | C1b's median and its +- SE regraded on M3's clusters only | I |
| C2b | is +4.41 stat-only? | list what s holds; Z_tot adding gas SE, OG1's slope range, seed spread from ZN4's bootstrap, m, n(z), leakage in quadrature | reported |
| C3a | covariance | joint chi^2 for ZN4 at +0.005 by BA1's method (bootstrap R; jackknife R reported) | K |
| C3b | which clusters | own bootstrap and 30-patch jackknife of M3's Z; leave-one-out range; drop top 1, 3, 5, 10 by contribution to (n - v), compared with the same drops on a null where the mean excess is removed; 10 % trimmed ratio; N against S; z halves; mass halves; each of the two OUTER bins | K |
| C4a | boost | B = 1 in OUTER; M3's own B in place of the 326's | I |
| C4b | m | not on disk per the ledger unless found; 0.02 is a provisional ceiling, marked LITERATURE-INPUT, never counted in the combination | ceiling |
| C4c | photo-z | F1's C5d route (SOM n(z) per tomographic bin, source weights) on M3's z; also n(z) shifted by the SOM_cov_multiplied.asc sigma if the file reads cleanly | I |
| C4d | random subtraction | new extended randoms, X11's placement and count (20 per cluster, seed 20261025), tangential as well as cross, replacing the 5-6 of F1 in D; also A without subtraction and A_RR, A_x per bin in M3 | I |
| C4e | PSF leakage per tile | X7's stored leakT on ZN4's template (X7's bracket, carried across, not refit) | I |
| C5 | miscentring | catalogue offsets x 0, x 2 in the model, OUTER only; x 2 is a bracket, not a measurement | bracket |

## Rule
Worst-cell baseline: ZN4's chain, gas +0.005, four cells (f* 0.034, 0.0615; h 0.672, 0.686), one template.
Reach of an effect, per cell: (Z_base - Z_variant) / (Z_base - 2). Positive lowers the miss. 1 = lands on the line. Report the range over cells.

## Labels
- REAL: no class I effect reaches 1/3 in any cell.
- PARTLY: one class I effect reaches 1/3 or more in at least one cell, and the net below doesn't land.
- ARTEFACT: the net sum of ALL class I shifts at measured central values, including those that raise Z, brings Z <= 2 in all 4 cells. Lowering-only sums are reported, never graded. Brackets and ceilings are never counted.
- Tag [WORSE THAN STATED]: net class I shift raises Z.
- Tag [NOT SIGNIFICANT WITH FULL ERRORS]: Z_tot <= 2 by widening alone. This is not a pass.
- Tag [FEW-CLUSTER]: dropping at most 5 clusters gets Z <= 2 and the null's same drop moves Z less than half as much.
No rule passes here: a result that lands is not a pass unless the effect is measured independently of the keys, and a pass would need its own regrade of all 15 keys, X-COP, groups.
G-OUT-Mall and G-MID-T3 are reported beside M3 under each variant where it costs nothing; the label is on M3, as the single worst key.

## Runs
ZN4's grader text, unedited, through my own driver and my own cache dir: base, C1a, C2a, C5 x0, x2, at both f*. Own randoms, one thread, nice 15, checkpoint per cluster, SIGTERM safe, reading the session's KiDS column cache read-only. Nothing is written to any other lane.

## Checks (failed check: no verdict)
K1 baseline reproduces ZN4's G-OUT-M3 at +0.005: |d Z| <= 0.01 (expected about 0), all keys' preds <= 1e-6.
K2 own per-cluster dump reproduces meas, pred for M1-M3, Mall from sums, <= 1e-6.
K3 my estimator re-measures Draw, Rmean on the first 3 clusters with F1's seed (F1's randoms), <= 1e-6 x max; and Draw on all M3, same line.
K4 extended randoms reproduce X11's cross level in MID, +0.000 +- 0.022 at h 0.672 canonical on C*: |d| <= 0.005.
K5 Tweedie on synthetic: noise added to a known Gaussian, shift within 10 % of analytic.
K6 bootstrap identity draw returns the full-sample Z.
MUTATE: (a) C1a's sign flipped must move Z the opposite way, by at least half as much; (b) randoms with e2 flipped, 5 clusters, K3 must FAIL; (c) M3's membership shuffled: Z's excess must drop by at least 1; (d) excess removed in C3b's null: Z within 0.05 of 0. Separate outputs.

## Expectation on record
PARTLY. C4d lands 25-40 % of the need, because the -0.07 random level looks like X11's cross fluctuation. C1a raises Z by a few tenths, since the bin is cut on the number the prediction uses. Nothing else reaches a third. Net well short of the line, so the wall stands. A few clusters don't drive it.

## Amendment A1, before any verdict and before the extended randoms were read
C1a's prediction for all 326 sends M1's low-count clusters up by large factors, because Tweedie's shift grows with sigma squared at the density's edge (M1's median error is 0.33 dex). G-OUT-Mall reads nonsense under it and the flipped sign divides by zero. M3's Z depends only on M3's clusters, so its C1a value is untouched. Changes: MUTATE (a) flips the sign on M3 only; added job C1a_M3 (M3 only), so Mall is read correctly; added report-only C1a_cap, shift only where the catalogue error is <= 0.2 dex. The label still uses C1a as frozen. K4's line stays |d| <= 0.005, on X11's template scale. C4a and C4c, being multiplicative, keep the grader's fractional s; additive shifts keep its absolute s. C1a and C2a overlap: the frozen net counts both; the net without C2a is reported too.
