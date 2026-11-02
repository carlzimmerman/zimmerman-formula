# CU1_gas_term_replication: REPRODUCED. The fit is a fail either way: canonical 14 of 15 with G-OUT-all over 2, alt 10 of 15, and no k from any bootstrap clears all 15

Criteria: `FROZEN_CRITERIA.md` (c4f9b3476f), committed alone first. Own build `cu1_core.py`, `cu1_gate.py`, `cu1_grade.py`, written from CRG1's SPEC and raw inputs; numbers committed in e0ae0d167c and 5281469b18 **before UX3's README was opened**. UX3, UX6, UX7 scripts never opened; UX6 and UX7 not opened at all. **Not blind:** I had the claimed numbers from the start. Reproducing means the numbers follow from the definition. It says nothing on whether the term is physically right. No action, no field equation. kappa = 1/2 FITTED. Cold sector stays retired; nothing here reinstates it. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

## Verdict, as frozen
All brief claims MATCH or CLOSE and no key's label flips. Line by line over UX3's README, 78 items: **73 MATCH, 4 CLOSE, 1 DISAGREE**, all in `cu1_compare.out`. The DISAGREE and CLOSEs are all joint chi^2 or its p, see below. Chi^2's tolerances (0.5, 2.0) were set in the compare script, after the freeze: the criteria had none for it.

| Claim | Claimed | Mine | Label |
|---|---|---|---|
| Law: keys, M3, X-COP (the gate) | 10, +4.76, +0.467 | 10, +4.759, +0.4675 | gate PASS |
| k canonical, alt | 13.29, 14.25 (brief 13.3, 14.3) | 13.288, 14.252 | MATCH |
| Canonical keys, failing | 14, G-OUT-all | 14, G-OUT-all | MATCH |
| G-OUT-all h 0.672, 0.686 | -2.71, -2.77 | -2.715, -2.771 | MATCH |
| G-OUT-M3 | +0.58, +0.35 | +0.579, +0.351 | MATCH |
| X-COP all 7 | -0.016, 0.089 | -0.0163, 0.0887 | MATCH |
| X-COP unseen 3 | -0.044, 0.081 | -0.0441, 0.0807 | MATCH |
| Joint p, h 0.672 | 0.38 (chi^2 16.1) | 0.352 (16.46) | CLOSE |
| Alt keys, failing | 10, same five | 10, same five | MATCH |
| Alt M3, joint p h 0.672 | -0.06, 0.24 | -0.059, 0.207 | MATCH, CLOSE |

Also MATCH: both pi^2 rows, the k scan's counts, gas +0 and f* 0.0615 counts, HSE -0.12 dex at -0.136, the plain multiplier's 2 of 15 and M3 -12.4.

## Two things the claim's wording hides
1. **Joint p 0.38 is the better h cell.** BA1's headline is the worse h, and that's h 0.686: **p 0.18** canonical, **0.10** alt, chi^2 19.8 and 22.3. Still JOINT PASS on the bootstrap. UX3's column does say "h 0.672", so it isn't an error, but 0.38 shouldn't be quoted alone. UX3's README doesn't print h 0.686 at k fit.
2. **My chi^2 runs above the record's, with the same Z.** 16.46 against 16.1; alt 19.15 against 18.5; law 65.9 against 65.0; multiplier 451 against 428, the one DISAGREE. Five R seeds give 16.2 to 16.8 at k fit and 64.6 to 66.5 on the law, so seed noise covers part of this, not all. So it lies in R, not in the keys. One try: R built on leak-subtracted n instead of raw moves it by 0.04, so that isn't it. **Not diagnosed.** I didn't read the record's R code. No class changes.

## Stress: k
k comes from 4 hydrostatic clusters, so its error is the real question.

| Canonical (alt) | k | 16-84 % or range |
|---|---|---|
| Fit on the 4 | 13.29 (14.25) | |
| Bootstrap of the 4, all 35 multisets | | 11.2-16.1 (12.1-17.3), sd 2.10 (2.28) |
| Bootstrap of the 7, 2,000 draws | median 12.38 (13.28) | 11.3-13.7 (12.1-14.7), sd 1.23 (1.33) |
| Leave one out of the 4 | | 11.9-15.7 (12.7-16.9) |
| Leave one out of the 7 | | 11.6-13.3 (12.5-14.2) |
| One cluster alone | | 8.7 A2142 to 18.1 A644 (9.3-19.6) |
| Every 4-of-7 split | | 10.4-15.0 (11.2-16.1) |

**Clusters don't share one k within their scatter:** a factor 2 between single clusters, and at the fitted k per-cluster means run -0.125 (A2142) to +0.091 (A644). Rows within a cluster aren't independent; the bootstrap treats clusters as the unit.

**The unseen-3 pass is one of the luckier splits.** Over all 35 splits, the held-out 3 pass X-COP's line in **14 of 35** canonical, 17 of 35 alt; worst mean +0.121, rms 0.141. All 7 pass in 32 of 35, 34 of 35, but those rows include the fit's. The claimed split isn't an outlier in k. It's just not the only draw.

## Stress: k's error on the keys
| Canonical | P(15 of 15) | P(14) | 13 | 12 or fewer | G-OUT-all 16-84 % | G-OUT-M3 | worse-h joint p |
|---|---|---|---|---|---|---|---|
| Bootstrap of 4 | **0** | 0.44 | 0.30 | 0.26 | -3.08 to -2.45 | -0.31 to +1.23 | 0.09-0.26 |
| Bootstrap of 7 (600 draws) | **0** | 0.33 | 0.63 | 0.04 | -2.76 to -2.46 | +0.47 to +1.18 | 0.09-0.20 |
| 35 splits | **0** | 0.34 | 0.60 | 0.06 | -2.76 to -2.45 | +0.46 to +1.21 | 0.09-0.20 |

Alt: **P(14 or more) is 0 everywhere,** 9 to 12 keys, mostly 10; G-OUT-all -3.59 to -2.97, worse-h p 0.06-0.11. Joint p stays above 0.05 in 93-100 % of draws on both footings, so the joint pass holds up and the per-key fail does too.

**14 of 15 is fragile, the fail is not.**
- Canonical's 14 holds only for k 12.87 to 15.09. The fit, 13.29, sits 0.42 above the bottom, a third of a sigma of the 7-cluster bootstrap.
- **Fit k on all 7 and it reads 13 of 15:** k 12.40, G-MID-T3 +2.11 at h 0.686, G-OUT-all -2.60, X-COP +0.003, 0.087; alt k 13.31, 10 of 15. Post-result, direct cells.
- Pass windows, canonical (alt): G-OUT-all needs k <= 7.2 (3.1). G-OUT-M3 needs k >= 8.8 (7.0). G-MID-T3 needs k >= 12.9 (12.7). G-MID-b >= 10.7 (12.0). **G-OUT-all's window excludes every k in every bootstrap (lowest 8.7), and doesn't overlap M3's or MID-T3's, so no k passes all 15.** That is a shape miss, as UX3 said; its "below about pi^2 at best" is looser than my 7.2.
- Largest key moves from k's sigma (7-cluster): M3 0.39, MID-T3 0.29, OUT-Mall 0.23. Added here only as a size, not in any Z.
- **HSE 0.12 dex high (LF1), refit:** k 8.38, X-COP fits by construction, keys 11 of 15, M3 +2.12, worse p 0.013. UX3's sentence holds: the k drops to where M3 fails again. The result is conditional on the hydrostatic scale.
- **Fit readings.** Mean d = 0: k 13.51 (14.49), same counts. Linear in M_HSE/M_law - 1: k 12.85 (13.86), **canonical 13**, adds G-MID-T3. Alt unchanged. Gas uncapped at r_ta: same counts. So my primary reading, which matched UX3, is one where the count holds; the linear fit isn't.
- No negative density in any graded cell at k fit. 5 P bins over all clusters hit the SPEC's floor at canonical h 0.672, from miscentring.

## Checks, every failure listed
- K1 inputs: 28 files against MANIFEST, 326, 106, 35. PASS.
- **K2 FAILS its frozen 1 %:** 1.107 % at the innermost bin, 0.08 % at the outer. Cause, post-freeze: SPEC's inner disc rule 1/2 Sigma_0 R_0^2 undercounts a singular isothermal by R_0/R. A truncated-sphere analytic reads the same, so the 30 Mpc edge isn't it. Stays failed; effect on cored clusters is smaller, not separately measured.
- **K3 FAILS as written:** 0.5, since my test used an arbitrary offset 0.3 Mpc on a cluster whose inner ΔΣ goes negative and hits the floor in both runs. At offset 0 and the cluster's own offset, 1.6e-15. A bad test, kept as failed.
- K4 R = I gives sum Z^2, PASS. K5 reruns byte-identical: gate, grade, stress, compare.
- MUTATE, nu = 1: gate fails on all three, exit 1, separate outputs.

## Limits, unfinished
- EFE table C(s) taken as given, not solved (CRG1's A10 solved it). Constants, M_gas's cap and inputs are the SPEC's, so a wrong definition carries through. **This is mainly a test of code.** UX3 and SPEC share the record's chain.
- Not checked: UX3's Parts A, B, C (discs, switches, HSC against KiDS), its M/Mg table, its alt f* cells' Z. The enclosed-mass form and the Bullet aren't touched here.
- Boot7 propagation uses 600 of 2,000 k draws, interpolated on a 23-point k grid; midgrid check 8e-9, k fit 0.
- Machine ran at load about 20; one thread, nice 15.
