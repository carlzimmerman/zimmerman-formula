# B4 result: a sharper lattice test of the Multiple Point Principle (flat-histogram line positions, equal-weight criterion)

**Bottom line.** Flat-histogram Monte Carlo (Wang-Landau densities of states with centre-flip proposals, equal-weight coexistence points, L = 4 and 6) shrinks the lattice error on 1/alpha(M_P) from B2's 5.5% (SU(2)) and 17% (SU(3)) to 0.8% and 2.4%, but the pre-registered chain that certifies the cheap windowed estimator (gate G-W) failed marginally (SU(2): mean offset 0.0032 against a 0.003 limit, driven by the junction point), so the "3% sharper" claim is stated, not certified. SU(2): triple point (beta_F, beta_A) = (0.484 +- 0.026, 2.456 +- 0.014) gives 1/alpha_2(M_P) = 50.55 +- 0.42 (lattice) with the exponentiated continuum correction and 48.25 without, against Y1's 49.203: Y1 lies BETWEEN the two conventions (each alone is more than 2 lattice sigma away), and with the unresolved convention spread (+-2.30) carried as an inherited sigma the verdict is PASS-WEAK (z = +0.58). SU(3): 1/alpha_3(M_P) = 67.7 +- 1.6 (lattice, with a stated finite-size and hysteresis allowance) +- 3.8 inherited, 28% above Y1's 52.971 (z = +3.6 with the inherited spread, +9.0 lattice-only): FAIL (provisional), and robust, because every triple point must lie on the well-determined flat I-II line at beta_A = 6.1-6.25 for beta_F <= 1, so no outcome of the steep line gives less than 1/alpha_3 = 63.5; the papers' graphical reading beta_A = 5.4 is not reproduced (B4 and B2 both find about 6.1). U(1) was not touched.

## Table (scripts `b4_*`, outputs `*.out`; criteria of `B4_PREREGISTRATION.md` with Amendments 1-3; confrontation `b4_confrontation.out`)

| Coupling | B2 (L = 4, 6 hysteresis brackets) | B4 value (exponentiated) +- lattice +- inherited | not exponentiated | lattice precision vs 3% | z vs Y1 (with inherited / lattice-only exp. / lattice-only not exp.) | Verdict |
|---|---|---|---|---|---|---|
| 1/alpha_Y | UNDECIDED | not touched (authors' model; lane B3) | - | - | - | UNDECIDED |
| 1/alpha_2 | 49.89 +- 2.76 (5.5%) +- 2.34 | **50.55 +- 0.42 +- 2.30**; triple point (0.484 +- 0.026, 2.456 +- 0.014) | 48.25 | 0.8% (< 3%) but G-W formally failed: NOT certified | +0.58 / +3.24 / -2.27 | **PASS-WEAK** (Y1 = 49.203 sits between the two conventions) |
| 1/alpha_3 | 66.7 +- 11.1 (17%) +- 3.8 | **67.70 +- 1.63 +- 3.80**; triple point (0.715 +- 0.451, 6.147 +- 0.158) | 63.90 | 2.4% under the stated allowances: NOT certified | +3.56 / +9.04 / +6.71 | **FAIL** (provisional; robust to the steep line, see below) |

Papers' own numbers for comparison (B1): 1/alpha_2 = 49.5 +- 6.95, 1/alpha_3 = 56.7 +- 8.5, from graphical readings (0.54, 2.4) and (0.8, 5.4). Y1 targets 55.234 / 49.203 / 52.971.

## What was measured

Algorithms: link updates = near-identity Metropolis hits + centre flip (Z2/Z3) + (SU(2)) Metropolis-corrected reflection "overrelaxation"; Wang-Landau densities of states (applied per sweep) in the sampled variable A = sum of the adjoint plaquette observable. Line points = the beta_A at which the integrated weights of the low-A and high-A phases are equal (equal-weight criterion; equal-height also computed for the production values and agrees within 0.001-0.002). Two estimators: the pre-registered full-range flat-histogram production (frozen Wang-Landau table, up to 12 refinement rounds, block jackknife, 24 traversals target) and, because the full-range walk is too slow at L >= 6 and at SU(3), the windowed Wang-Landau estimator WW of Amendment 2 (16-bin windows, hot/cold-start replicas, stitched). Lattices: SU(2) L = 4 (all ten beta_F; production and WW) and L = 6 (WW at beta_F = 0, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8); SU(3) L = 4 only (WW at eight beta_F; production at 0.8, and an attempt at 1.2 that did not tunnel).

SU(2), beta_A*(L, beta_F) (production L = 4; WW L = 6; value after the 1/L^4 extrapolation, "mix" variant; points marked * have L = 4 only and carry the mean measured shift +0.014 with its spread):

| beta_F | L = 4 (production) | L = 6 (WW) | L -> infinity |
|---|---|---|---|
| 0.0 | 2.5171 +- 0.0012 | 2.5317 +- 0.0024 | 2.5353 +- 0.0086 |
| 0.1 | 2.5147 +- 0.0007 | - | 2.5290 +- 0.0133 * |
| 0.2 | 2.5043 +- 0.0012 | 2.5160 +- 0.0024 | 2.5189 +- 0.0072 |
| 0.3 | 2.4846 +- 0.0012 | 2.4975 +- 0.0025 | 2.5006 +- 0.0078 |
| 0.4 | 2.4571 +- 0.0012 | 2.4703 +- 0.0025 | 2.4736 +- 0.0080 |
| 0.55 | 2.3475 +- 0.0005 | - | 2.3619 +- 0.0132 * (junction; not in the primary segments) |
| 0.6 | 2.2455 +- 0.0004 | 2.2357 +- 0.0239 | 2.2333 +- 0.0302 (hysteresis-affected, 25 of 84 windows run hit the sweep cap) |
| 0.7 | 2.0493 +- 0.0007 | 2.0753 +- 0.0126 | 2.0818 +- 0.0213 (hysteresis-affected, 23 of 57 windows run hit the sweep cap) |
| 0.8 | 1.8722 +- 0.0008 | 1.8840 +- 0.0025 | 1.8870 +- 0.0073 |
| 0.9 | 1.7060 +- 0.0009 | - | 1.7203 +- 0.0133 * |

Primary segments S1 = {0.2, 0.3, 0.4}: beta_A = 2.5651 - 0.2250 beta_F; S2 = {0.6, 0.7, 0.8}: beta_A = 3.3268 - 1.7987 beta_F; intersection (0.484 +- 0.026, 2.4563 +- 0.0139), correlation -0.64. Fit-range systematic (the five declared alternative segment sets; no quadratic fit was made) 0.32 in 1/alpha_2, statistical+finite-size 0.27, lattice total 0.42. The three input variants agree: "win" (WW at every L) 50.54, "mix" (production at L = 4, WW at L = 6; the pre-registered fallback and the primary because G-W failed) 50.55, "prod" (production values only: L = 4 everywhere and L = 6 at beta_F = 0.35 [calibration], 0.4, 0.8; shift transferred to the other points; triple point (0.496 +- 0.010, 2.4508 +- 0.0127)) 50.55; non-exponentiated 48.24-48.25 in all. The finite-size shift from L = 4 to 6 is +0.012 to +0.015 at the well-converged points (+0.026 and -0.010 at the two hysteresis-affected ones); the 1/L^4 extrapolation adds about +0.003. Pure-adjoint point (gate G-K): beta_c(beta_F = 0) = 2.535 +- 0.009, inside the declared [2.40, 2.60]. Consistency with B2 (G-B2): all six L = 4 values lie inside B2's hysteresis brackets, and at beta_F = 0, 0.4 they equal B2's midpoints to 0.003.

SU(3), beta_A*(L = 4, beta_F) (hot-start / cold-start replica means in brackets):

| beta_F | WW value | hot / cold | note |
|---|---|---|---|
| 0.0 | 6.249 +- 0.054 | 6.278 / 6.219 | 2 replicas |
| 0.4 | 6.244 +- 0.002 | 6.244 / 6.243 | 6 replicas |
| 0.6 | 6.192 +- 0.005 | 6.194 / 6.189 | 2 replicas |
| 0.8 | 6.1205 +- 0.0027 | 6.125 / 6.116 | production (22 traversals) 6.1174 +- 0.0004 |
| 1.0 | 5.82 +- 0.27 | 5.97 / 5.67 | hysteresis band |
| 1.2 | 5.47 +- 0.15 | 5.62 / 5.31 | 74 of 117 windows capped; full-range production did not tunnel (dropped) |
| 1.6 | 4.91 +- 0.25 | 5.04 / 4.77 | hysteresis band |
| 2.0 | 4.317 +- 0.005 | 4.319 / 4.315 | |

S1 = {0, 0.4, 0.8}: beta_A = 6.363 - 0.302 beta_F; S2 = {1.2, 1.6}: beta_A = 7.150 - 1.403 beta_F; intersection (0.715 +- 0.451, 6.147 +- 0.158). The error on 1/alpha_3 (1.63) is dominated by the assumed common finite-size shift of +-0.06 in beta_A (no SU(3) L = 6 comparison could be completed; see below), by the hysteresis bands of the S2 points, and the very large error on beta_F (the two segments are nearly parallel in the region) matters little because 1/alpha_3 depends mostly on beta_A. Alternatives S1', S2', S1'+S2' move 1/alpha_3 by <= 0.05.

Why the SU(3) FAIL is robust: the I-II line (S1) is well determined (hot and cold replicas agree to 0.01 at beta_F = 0.4 and 0.8; the production run at 0.8 agrees with WW to 0.003; B2's brackets contain the values). A triple point must lie on S1; for any junction at beta_F between 0.6 and 1.0 the conversion gives 1/alpha_3 >= 67.4 (exponentiated) / 63.5 (not exponentiated), against Y1's 52.97. To reach Y1 (exponentiated) the junction would need beta_A about 5.0, which is 1.1 below the measured S1 line and more than three times the widest hot-cold hysteresis band (0.3); even the papers' own beta_A = 5.4 would not suffice. The papers' (0.8, 5.4) is therefore not reproduced; the ratio of my beta_A to theirs, 6.12/5.4 = 1.13, is close to 9/8, which would be the factor between two common normalisations of the SU(3) adjoint term; I did NOT verify this (the lattice papers behind the graphical reading were not read), it is an observation that points to checking the source figure's normalisation, not a finding.

## Gates and controls (all outputs kept)

* G-P (algorithm + analysis on the exact 2D q = 20 Potts transition, `b4_0_potts.out`): beta_c = 1.69967 +- 0.00136 vs exact 1.69967, round trips >= 25 at L = 10-16 (exit 0). MUTATE (`b4_0_potts_MUTATE.out`, acceptance without the weight difference): fires through the precision condition and the round-trip condition (deviation 2.98 sigma, borderline; exit 1). The earlier output with the previous Wang-Landau scaling is `b4_0_potts_prefix_prescaling.out`.
* G-C (flat-histogram gauge code reweighted vs B2's independent canonical code; SU(2) L = 4, `b4_1_su2_gates.out`: four observables within 1.2 sigma, exit 0; SU(3) L = 4, `b4_2_su3_gates.out`: within 1.7 sigma, exit 0). MUTATE (`b4_1_su2_MUTATE.out`, `b4_2_su3_MUTATE.out`): reweighted means off by up to 132 sigma (SU(2): +42.8, +17.6, -132.5, -21.3) and up to 40 sigma (SU(3): +39.7, +12.2, -2.1, -6.4), exit 1.
* Extra checks at L = 6 (non-gating): beta_F = 0.4: full-range production (seeded from the windowed density, 32 traversals) 2.46931 +- 0.00014 versus WW 2.47031 +- 0.00080 (+0.0010, 1.2 sigma); beta_F = 0.8: production (25 traversals) 1.88395 +- 0.00018 versus WW 1.88404 +- 0.00087 (+0.0001); calibration point beta_F = 0.35 (outside the grid, seen before the grid was run): production 2.48462 +- 0.00017 versus WW 2.48608 +- 0.00043 (+0.0015). WW is higher than production by 0 to 0.0015, the same sign and size as at L = 4. Production at beta_F = 0.6 and 0.7 (L = 6) was started and aborted by me (`logs/su2_ppoint_L6_bF0.6_0.7_ABORTED.out`).
* G-K: passed (2.535 +- 0.009). G-B2: all consistent (SU(2) six, SU(3) five points).
* G-W (windowed vs production at L = 4, `b4_analysis.out`): SU(2) FAILED by the declared mean-difference limit (+0.0032 vs 0.003; largest single deviation 1.8 sigma; the junction point beta_F = 0.55 differs by 0.017); SU(3) one matched point (beta_F = 0.8): difference +0.0031 (0.7 sigma), also above the absolute 0.003 limit. MUTATE (`b4_analysis_MUTATE.out`, +0.02 bias): G-W fails, exit 1. Consequence applied (Amendment 2): the primary SU(2) variant is "mix"; the SU(3) fallback cannot be formed (one production point) so "win" is used and flagged.
* G-CONV and its MUTATE (`b4_confrontation_MUTATE.out`): pass / fire as required.
* Exponentiated versus not (decision (e)): the primary text (hep-ph/9311321 section 5) introduces the exponentiated corrections as a crude estimate of the omitted second-order error (about one unit of 20) and gives no preference; hep-ph/9607278 averages several procedures. The question stays UNDECIDED; I carry the difference as an inherited sigma and report both conversions. The effect is decisive for SU(2): exponentiated 50.55 and non-exponentiated 48.25 straddle Y1's 49.203.

## Deviations from the pre-registration (all in Amendments 1-3 of `B4_PREREGISTRATION.md`)

1. Procedure changes after calibration (Amendment 1): Wang-Landau flatness over visited bins with both ends touched; up to 12 refinement rounds (not 2); adaptive bin count; pilot separation rule; thinning of the jackknife sample; Potts gate on L = 10-16 with a clipped range; G-C at beta_A = 2.3/2.65 (SU(2)), 5.6/6.5 (SU(3)). An implementation error (Wang-Landau increments applied per link instead of per sweep) was found and fixed during calibration; its effect was noisy tables, not a wrong sampling distribution.
2. Estimator change (Amendment 2): the full-range walk was too slow at L = 6 (one traversal about 1e5 sweeps), so a windowed Wang-Landau estimator was introduced before any grid point was run, with a new gate G-W; G-W then failed marginally (Amendment 3) and the pre-registered fallback was applied.
3. Post hoc items (Amendment 3, marked): the estimator systematic (rms WW minus production over the primary-segment points, 0.0024), the hot/cold error floor, the "transfer" of finite-size shifts to L = 4-only points, replica counts reduced for the steep-line points (4, 3 replicas at L = 6; 2 replicas for most SU(3) points, 1e5 sweep cap), the assumed +-0.06 common finite-size shift for SU(3).
4. Not done: L = 8 (any group), SU(2) full-range production at L = 6 at beta_F = 0.2, 0.3, 0.6, 0.7 (done at 0.4, 0.8), the V-method (attempted at L = 4: the two high phases II and III are not resolved as separate peaks in A + F at the base point, no root found, no result), the Z2-line scan, SU(3) overrelaxation, an SU(3) L = 6 finite-size measurement (aborted, see Honest limits). The 3% precision for SU(2) and SU(3) is therefore reported but not certified.
5. Process count: the plan said at most 10 concurrent processes; during parts of the run I had up to 12-15 (several jobs of 3-4 workers overlapped), on a machine whose load average rose to 183 for about 15 minutes because of other jobs; all were run with nice 10.
6. First runs: the first Potts attempts (unclipped range, L = 24) and the first SU(2) L = 6 calibration were not saved as FIRSTRUN files (see Amendment 3 item 6).

## Honest limits

* The finite-size extrapolation rests on two lattices (L = 4, 6) for SU(2) and, for SU(3), on an assumption (+-0.06 common shift, from the SU(2) analogue). The one SU(3) L = 6 point attempted (beta_F = 0.4, windowed, 2 replicas, 1e5-sweep cap) was aborted by me after 32 windows: 24 of the 32 windows of the hot-start replica did not meet the flatness criterion within the cap (`logs/su3_wpoint_L6_bF0.4_ABORTED.out`), so no SU(3) L = 6 value exists and the SU(3) finite-size allowance is an assumption, not a measurement.
* Windows in the mixed-phase region of the steep I-III lines do not converge reliably (hidden barriers); hot and cold replicas then disagree, which sets the larger errors there. The junction region (beta_F about 0.5 for SU(2)) is where the high-A phase is a mixture of two phases, and the definition of an equal-weight point is ambiguous there; the primary segments avoid it (0.55 not used) and the result does not depend on it (alternatives within 0.35 in 1/alpha_2).
* The conversion's inherited conventions (exponentiated or not; Bianchi factor; N_gen = 3; identification of the single-group triple point with the multiple point; M_Planck) are untouched: moving M_Planck by a factor 3 shifts Y1's targets by at most 1.2, 0.5, 1.2 in 1/alpha_(Y,2,3); that is the ~1-unit floor.
* The SU(2) agreement with Y1 depends on the exponentiation convention: the lattice error alone (0.4) is smaller than the 2.3 between the conventions. SU(2) is therefore consistent with Y1 only because Y1 sits between them.

## Compute

About 4.6 hours wall clock (20:12 to about 00:50), roughly 20 core-hours (an estimate from sweep counts and process times, not a measurement), 12-15 processes at peak (over the planned 10, see above). Raw series and tables (several GB at most) are in the gitignored `cache/`, binaries in `bin/`.

## Files

`B4_PREREGISTRATION.md` (Amendments 1-3), `src/{b4_common.h,muca.h,su2m.c,su3m.c,potts.c}`, `b4_lib.py`, `b4_tp.py`, `b4_0_potts.py` (+`.out`, `_MUTATE.out`, `_prefix_prescaling.out`), `b4_1_su2.py`, `b4_2_su3.py` (modes gates / point / wpoint / ppoint; +`b4_1_su2_gates.out`, `b4_1_su2_MUTATE.out`, `b4_2_su3_gates.out`, `b4_2_su3_MUTATE.out`, `*_prebinfix.out` for the gate outputs before the final binaries), `b4_3_vertex.py` (V-method, failed at L = 4, `logs/su2V_L4.log`), `b4_analysis.py` (+`b4_analysis.out`, `b4_analysis_MUTATE.out`), `b4_confrontation.py` (+`.out`, `_MUTATE.out`, `b4_rows.json`), `b4_tp_su{2,3}_weight*.json`, `results/*.json` (every line point), `logs/` (job logs), `run_queue.sh`, `jobs_*.txt`.

alpha stays an INPUT; kappa = 1/2 FITTED; SM-mass wall unchanged; a sharper MPP is a mechanism-level result with a ~1-unit systematic floor in 1/alpha from the Planck-scale identification, not a derivation of the measured digits.
