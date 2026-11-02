# CG1_a0_certificate: a0's certificate does not survive repair. sqrt(8 pi/3) gets 0.11 bits at SPARC's real precision and does not stand out from cH/2pi or cH/6

Frozen labels: **SEPARATES KOIDE ONLY**, and for the coefficient **FITS ON ONE FOOTING, NOT SPECIAL** (its second clause: inside on both footings, without the rest). This grades the coefficient only. It doesn't say the law is wrong, and it doesn't touch the law's fit to data. kappa = 1/2 FITTED. Not theory closed. The cold sector stays retired. Nothing here says the data favour the framework.

Criteria `FROZEN_CRITERIA.md` (d9db83969f), alone first, **not blind**. My stated expectation (a0 not certified, few bits) came out, so read this with that in mind. Numbers: `cg1_gate.out`, `cg1_kernel.out`, `cg1_cite.out`.

## What evidence a0's formula really has
| Source of evidence | Amount |
|---|---|
| Gate A as recorded | infinite bits: **a unit error** |
| Gate A, error fixed, nothing else | 5.51 bits at 5 %, under its 10 bit line. FDR-DEAD |
| Same, requiring the relation to land in the window | **no hit on either footing**: 1.2e-10 +- 5 % misses 9.36e-11 and 1.131e-10 |
| The kernel step, real power test, SPARC window | **0.11 bits**. 92.7 % of scrambled scalars get a decomposition as simple, with two forced places |
| Same, kernel-systematic or published 20 % window | 0.07, 0.02 bits |
| Same, if Einstein and Friedmann aren't independent | **a0 isn't in the class** |
| Scale: a0 is order c H at all (BK1, SPAN) | up to about 6 bits, inflated by Planck-laden trees. **Every rival below shares it** |

So what's left is the old coincidence a0 ~ c H, and the law's performance on data, which this lane doesn't grade. The specific number has no measurable support. Nor is it refuted: at this precision the test can't tell.

## Part A. The gate
Repairs A1-A7 in `gate/`, listed in `PATCH_FOR_PROJECT_ATOMOS.patch`. project_atomos not edited.

| Run | a0 | Koide | Five negatives + sqrt 2 | Rows |
|---|---|---|---|---|
| R0 original | CERTIFIED, bits inf | RE-LABELED, 15.27 | all FDR-DEAD | 8/8, reproduced in both the real file and the copy |
| R1 A1 only | **FDR-DEAD, 5.51** | same | same | **7/8** |
| R2 all, canonical | **FDR-DEAD, NO-HIT** | same | same (Z + 11 now NO-HIT) | a0 rows **all fail** |
| R2 all, alt | **FDR-DEAD, NO-HIT** | | | |

**The repaired suite fails by its own terms**, and I didn't edit its required status to hide that. Its a0 row requires CERTIFIED, and its footer says that means "fix the gate". That is the trap: the acceptance test hard-codes the answer. Whether a0 belongs in a positive-control row is the owner's decision.

**Does it still separate? Koide yes, a0 no.**
- **Koide holds.** 15.27 bits, stable across mass ranges (15.11, 15.36). Caveat: its window was set at its own deviation (-6.15e-6), and there's no multiplier for the choice of form.
- **a0's null reads only window width.** Under it, every negative beats a0: 11.17 bits at tolerance 1e-3, up to 16.90 at actual closeness (6 pi^5), against a0's 5.52. **5 of 5 at or above a0.**
- **The negatives' route kills a0.** The kernel 2.894 at 5 % gets E_chance 666, BAKED, and x = 1/Z gets 57.5. Negatives at actual closeness stay under the line: best is 6 pi^5, 4.07 bits, so that rejection is sound.
- So the separation came from routing: a0 alone got a friendly null, and then that null was misread.

**Other defects found.**
- Gate B accepted any implied free number in 0.05-20. 7.3 x kernel passed with the same declarations. Repaired, it fails.
- Gate A never checked the relation lands in its window.
- Gate B's places and gate C's "3 observables" are typed-in integers, not checks. Can't be repaired here; verdicts now print DECLARED, NOT VERIFIED. **So B and C aren't independent evidence for a0.**
- The comparative route's docstring had its sign backwards. Arithmetic kept, wording fixed. It gives -0.64 bits for sqrt 2; the docs say -1.08. Not chased.

Repairs only remove passes, so PAPER_ATOMOS_NULL's zero-certified count can't rise. Its calibration claim is what's affected.

## Part B. The kernel test
x = a0/(c R), scalars scrambled log-uniform over +- 1 dex about 1/Z, same window. Class T is a0's own: 2 distinct places of six, |e| = 1/2, kappa in {1, 2, 1/2}. 180 formal, 115 distinct.

| Window, a0 in | Half width | P, class T | P, +- 0.5 dex | Canonical | Alt | Bits, T | Scrambled registry, can / alt |
|---|---|---|---|---|---|---|---|
| W1 SPARC 2 sigma_boot, [0.915, 1.274]e-10 | 16.6 % | 0.927 | 1.000 | in | in | **0.11** | 0.996 / 0.997 |
| W2 three kernels, [0.727, 1.274] | 28.1 % | 0.955 | 1.000 | in | in | 0.07 | 0.999 / 1.000 |
| W3 published +- 40 %, PROVISIONAL | 42.4 % | 0.986 | 1.000 | in | in | 0.02 | 1.000 / 1.000 |
| W4 suite's 1.2e-10 +- 5 % | 5.0 % | 0.768 | 0.886 | **no hit** | **no hit** | 0 | 0.910 / 0.903 |

Random numbers as the "forced" registry do as well as the real one.

**Power.** Class T reaches 10 bits at half width **0.0032 %**, about 5000 times sharper than W1. Class S 0.0070 %, class W 0.0006 %. A true formula can't earn evidence on this test today; this is a limit of the test as much as a finding about a0. Even points-independent errors (+- 4 % at 2 sigma) wouldn't help: alt sits 4.65 % off, canonical further.

**Strict reading.** Friedmann is the 00 component of Einstein on FRW, and its 8 pi is Einstein's own. So "two independent places" is the same 8 pi plus a metric 3. Removing that pair, 1/Z is unreachable in the class. That's an argument about independence, not a measurement, so I give it as a second row.

## Part C. Rivals on SPARC
Record reproduced (K1). Bootstrap over galaxies gives sigma 8.28 %, close to the record's sqrt(N/n) 8.73 %; points-independent is 1.99 %. Net = fit bits minus log2 class size. Rank is among 703 distinct members. N = 4 pi is off the grid, 5.7 to 11 sigma away on every row; dropped.

| Kernel, footing | Best a0 | N = Z, sigma_boot, Net, rank | N = 2 pi | N = 6 | N = 8/sqrt 3 | Best Net |
|---|---|---|---|---|---|---|
| Framework, canonical | 1.080 | -1.73, -4.67, 26 | -2.71, -6.98, 36 | -2.16, -4.91, 33 | +1.00, -5.68, 13 | **Z, by 0.24** |
| Framework, alt | | +0.56, -2.55, 7 | -0.43, -1.41, 6 | **+0.13, -1.23, 1** | +3.29, -13.43, 43 | 6 |
| McGaugh, canonical | 0.871 | +0.79, -2.90, 11 | -0.11, -1.46, 2 | +0.40, -1.53, 4 | +3.29, -13.33, 47 | 2 pi |
| McGaugh, alt | | +2.88, -8.77, 41 | +1.98, -4.31, 27 | +2.49, -6.06, 33 | +5.37, -27.88, 72 | 2 pi |
| Simple, canonical | 0.882 | +0.64, -2.84, 10 | -0.25, -1.46, 3 | +0.25, -1.48, 3 | +3.09, -12.67, 46 | 2 pi |
| Simple, alt | | +2.70, -8.20, 38 | +1.81, -3.92, 26 | +2.31, -5.55, 31 | +5.15, -26.70, 72 | 2 pi |

- **Z is best in 1 of 6 cells, by 0.24 bits.** Every Net is negative: no formula's fit pays for its class.
- **Inside class T**, 5 of 22 members fit better than Z on canonical, 3 of 21 on alt.
- **On the framework's own kernel, alt:** Verlinde's cH/6 ranks 1, Milgrom's cH0/2pi ranks 6, Z ranks 7, all under 0.6 sigma_boot.
- **On the framework's own kernel, canonical:** 8/sqrt 3 is closer than Z, and the record's "kappa = 1/2 beats 1/2pi" is 1.73 against 2.71 sigma_boot, not a resolved separation.
- **Kernel moves a0 by 20 %**, more than the gap between rivals, and flips which footing fits: canonical on McGaugh's and simple, alt on the framework's. Raw chi2 min 3140.1, 2971.6, 3014.5, framework highest. Shape isn't graded here; it's a reason the a0 value is conditional.

## Part D. Citations, nothing edited
`CITATIONS.tsv`: 281 files at d9db83969f, by pattern, BK1 and this lane excluded. A (132) names the gate or calibration; B (15) a0 + CERTIFIED; C (134) forced-kernel wording. Many in A are auto-built `citations/works` pages and atomos code.

**To correct first:**
- `project_atomos/STATUS.md:25` and `HOWTO_RUN.md:12`: a0 CERTIFIED; `project_atomos/calibration/calibrate.py`; `notes/ENGINE_REVERSE_ENGINEERING.md`, `notes/GATE_SPEC.md`.
- `deepseek_push/THE_COMPLETE_THEORY.md` and deepseek E03, E05, D07, C06, F01, G201, AS015: a0 + CERTIFIED.
- `project_atomos/PAPER_ATOMOS_NULL.md`, v2, zenodo json (deposited, 10.5281/zenodo.21654272): cites the gate. Its null stands; its a0 calibration language, if any, needs reading by its owner. I saw no line certifying a0 in it.
- `book/22_what_is_forced_the_form_and_the_8_3_kern.md`: **kernel as forced, Einstein / Friedmann; the pattern misses it**, since it doesn't use the phrase. So this list is a floor.
- `real_research/papers/DSUNRUH_MI_THEORY_2026.md`, `opus_48_extended_research/papers/WB_CUBIC_GATE_LAW.md`: forced-kernel wording.

PAPER67's tex has no match on certificate or kernel wording. Not edited, per rules.

**Patch for project_atomos, for its owner:** `gate/candidate.py`, `fdr.py`, `forced_kernel.py`, `interlock.py` per the patch; `calibrate.py` candidate_a0 gets `structural_target` (see `a0_cand` in `cg1_gate.py`) and a decision on the row's required status.

## Checks and twins
K1 pass (sig_int 0.0808; 63.94 vs 63.90; 5.38 vs 5.34). K2 pass. K3 pass. K4 PLANT at alt recovered, +0.02 sigma_boot, though the plant has no correlated within-galaxy errors, so its 3 % is not a real error. K5 pass. K6 0.28 GB. Rerun byte-identical, both scripts. **MUTATE exits 1 on both:** the mismatch trips NULL-SCALE-MISMATCH; E = 7 pi loses a0 from T; a0 x 1.25 fails K1.

## Limits
- Registry and classes are my choice, frozen but not unique. A smaller registry lowers P, though at W1 half width about 15 evenly spaced values would cover the band. Class S, with 55 values, still gives P 0.843.
- Windows ignore distance and inclination errors except as bootstrap picks them up, so they're if anything too narrow, which favours the test.
- The rate comes from the footings; a different H0 moves every row together. Rival attributions partly recalled, PROVISIONAL.
- First run of K1 used +- 0.6 in code against +- 0.3 frozen. Corrected before the published run; it passes at 0.3.
- Citation patterns are a floor, and tiers are mechanical. I read only the lines quoted above.
- Fit bits use Dchi2/(N/n), not the bootstrap; the two agree to about 5 % on sigma on the reference kernel, less well on McGaugh's (12.0 vs 9.06 %).

kappa = 1/2 FITTED. Not theory closed.
