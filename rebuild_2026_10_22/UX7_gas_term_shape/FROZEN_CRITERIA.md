# UX7_gas_term_shape: FROZEN CRITERIA (committed alone, before any script or new number)

Owner's go, 2026-11-02. **Not blind, and the list is steered.** Read before this: UX3 README, criteria, scripts, its key table and scan; LW1, LM1, GM1 READMEs. So I already know the base term's miss: k about 13.3, canonical 14 of 15, only G-OUT-all over 2 at -2.71, -2.77; alt 10 of 15; MID-T3 and OUT-all pull apart at one k; LM1's dM/Mg falls outward, 8 to 5 to nothing by 1.7 Mpc. **F1, F6, F7 and F8 below were chosen knowing that direction.** Also looked at, for inputs only: eRASS1 columns and coverage on the 326 (KT on 106, median fractional error 0.75; L500 on all 326), overlap of GS4's pointed tables with eRASS1, which X-COP clusters are in eRASS1. No number for any form here exists yet.

kappa = 1/2 FITTED. Every form is FITTED, a description: no action, no field equation, nothing derived. The cold sector stays retired; no result here reinstates it. No particle. Footings canonical 9.3603e-11, alt 1.1312e-10, never pooled. Not theory closed. Nothing here says the data favour the framework. **No disc grade and no disc claim: discs stay an open problem for every form here; UX3's unswitched term breaks them and nothing here addresses that.** No downloads. UX3's files are read, not edited. One thread, nice 15, under 4 GB.

## Forms. Exactly one fitted number k each, per footing
x = g_gas/a0, y = g_b/a0, S = dlnM_gas/dlnr, u = r/R500. M = M_law H unless stated. F0 is UX3's, the reference, not one of the 8.
- **F0** H = 1 + k x. Enclosed gas.
- **F1 local gas:** H = 1 + k x S. x S = 4 pi G rho_gas r / a0: gas at r, not gas inside r.
- **F2 saturating:** H = 1 + k x/(1 + x). The term stops growing above g_gas ~ a0, with a0 as the only scale.
- **F3 all baryons:** H = 1 + k y. Stars count too. On the keys f is constant, so this differs from F0 only through k's fit on X-COP.
- **F4 in a0:** g = law(g_b, a0 (1 + k x)). The law's scale moves; no boost on the law's result.
- **F5 additive enclosed:** M = M_law + k M_gas(<r). LM1's statement as a rule; no a0 in the term.
- **F6 two-body:** H = 1 + k x^2. Quadratic in gas, as emissivity is.
- **F7 additive local:** M = M_law + k S M_gas(<r).
- **F8 atmosphere:** H = 1 + k x exp(-u). The term belongs to the virialised atmosphere. R500 here is the catalogue's, so **this form takes a mass-tied scale, and is not a pure gas form.**

## Rival: tied to M500, not gas
Same radial shape, amplitude by mass. s(r) = M_gas(<r)/M_gas(R500).
- **R1:** H = 1 + k G M500 s(r) / (r^2 a0). Against F0.
- **R2:** M = M_law + k M500 s(r). Against F5.
- **M500 source, primary, M_L:** eRASS1 L500 through lg M500 = a + b lg L500 + c lg(1+z), OLS, fitted on hydrostatic tables only: S09, L15, L20 rows of GS4's `gs4_inputs.csv`, M scaled to h 0.7 by the table's h, matched to the whole eRASS1 catalogue at sep < 5 arcmin and |dz| < 0.03. No shear enters. c replaces E(z), so no assumed background is added by me; the tables and catalogue themselves were reduced with h 0.7, Om 0.3, stated. **Limits stated now:** L500 and Mgas500 come from the same X-ray image, so this mass is independent of the keys' shear, not of the gas data; the catalogue's R500 aperture came from its M500, a weak dependence; HSE bias is carried; Malmquist bias not corrected.
- **Report rows, no label: R1c, R2c** with catalogue M500. Count-rate mass calibrated on shear including KiDS, so **not independent**. Shown to see whether the source matters.
- **Temperature mass not run:** KT exists on 106 of 326 with median error 0.75, and M keys need all 326.
- **X-COP rows for R1, R2** use X-COP's HSE M500: most of the 7 have no eRASS1 entry. So the rival's X-COP numbers use the very mass method they are compared to, partly circular; said in the README. k is fitted there and carried to M_L, which is calibrated to the same mass kind.
- In the grader, M500 x qd, as UX3 scaled Okabe. Stated difference: gas scales qd^2.5.

## Fit and grade
k: least squares on X-COP train (positions 0, 2, 4, 6) of log10(M_HSE/M_model), UX3's `xcop()` rows, per footing, bounded search. Never on keys.
1. **X-COP** unseen (1, 3, 5): |mean| <= 0.05, rms <= 0.10; all 7, same lines. LF1's HSE - 0.12 dex as a bracket, at the same k.
2. **15 keys** through UX3's path (LW1 tail, SL1 driver, NF1 grader), cells gas +0.005 f* 0.034 (**primary**), gas +0.005 f* 0.0615, gas 0 f* 0.034; h 0.672, 0.686; both footings. g_gas = g_b/(1 + f*).
3. Per row: keys over 2 in either h, every Z, worst |Z| and **margin (worst |Z| - 2)**, G-OUT-M3, joint chi^2 by UX3's `joint`, boot and jack p.
4. **Report only, primary cell:** k x 0.7, 0.85, 1.15, 1.3, to see whether any nearby k clears all 15. This is a look at the keys, never a fit, and not in any label or rank.

## Rank, per footing, never pooled
Primary cell, F0-F8 and R1, R2. Rank A by smallest of the two h boot p, descending. Rank B by largest of the two h |Z|, ascending. Sum of ranks; ties by rank B.

## Labels, per form and footing
- **PASS:** 15 of 15 in all three cells and both h; boot and jack p >= 0.05 in all; X-COP unseen and all 7 pass. A form passes only if both footings do, and the title says if they differ. Still fitted, still no action, still silent on discs.
- **NEAR MISS:** X-COP passes, primary cell at most 1 key over 2, worst |Z| <= 2.30, boot p >= 0.05 in both h.
- **IMPROVED:** X-COP passes, worst |Z| at least 0.25 below F0's on that footing in the primary cell, not NEAR MISS.
- **NO GAIN:** X-COP passes, none of the above.
- **X-COP FAIL:** X-COP unseen or all 7 fails, whatever the keys read.
The 2.30 and 0.25 are my numbers now, chosen knowing F0 reads 2.77 (alt 3.29).

## Gas against M500
R1 vs F0, R2 vs F5, per footing and h, primary cell. d = Z_a - Z_b; Dchi2 = chi2_a - chi2_b; sd = 2 sqrt(d' R^-1 d), BA1's R, same eigenvalue cut, predictions held fixed (a stated approximation). Forecast separation F = sqrt(d' R^-1 d)/2, what either truth would give.
- **NOT SEPARABLE:** F < 3 in any footing or h: the keys can't tell these apart with this lever, whatever Dchi2 reads.
- **M500 BETTER / GAS BETTER:** F >= 3 and |Dchi2|/sd >= 3, same sign in both footings and h.
- **NOT SEPARATED:** otherwise.

## Look-elsewhere, measured as well as stated
Stated: 8 forms and 2 rivals, on a family (the x tie) BF1 picked from about 2e9 tries, itself found after LM1 and GM1 showed the ratio; keys already read for F0. No p in this lane is a discovery p. A high joint p is a failure to reject, conditional on all that.
**Measured, random-shape control:** 40 shapes H = 1 + k x^p u^q S^t, (p, q, t) drawn uniformly in [0.5, 2.5], [-2, 1], [0, 2], seed 20261102, none examined before drawing, each with k fitted on X-COP train the same way, graded on the primary cell, both footings. Report the fraction of draws that pass X-COP and match or beat the best listed form's worst |Z|, and its p. **If that fraction is at or above 0.10, the best form's shape is not earned over an arbitrary shape,** and the README leads with it. It samples only this power-law family, so it is a lower bound on the freedom used. Plain Bonferroni on the best form's count: 10 trials.

## Checks, before reading
K1 F0 at UX3's k reproduces `ux3_keys_g005_f034.json` per key, both footings, |dZ| <= 1e-9. K2 F0's fit reproduces `ux3_kfit.json`, 1e-5. K3 every form at k = 0 equals the law row on canonical, |dZ| <= 1e-9. K4 F3 at k equals F0 at k (1 + f*), |dZ| <= 1e-9. K5 R1 with M500 set to Mgas500 x c equals F0 at k c, |dZ| <= 0.02, the tolerance for the qd difference, h 0.672. K6 M_L against X-COP HSE on the X-COP clusters that are in eRASS1, median offset reported; over 0.15 dex is stated as a failed check. K7 M_L calibration N >= 30.
A failed K1 or K3 stops any verdict.

**MUTATE twin, must fail or move:** all forms at k x 3 (X-COP must fail); R1, R2 with M_L shuffled among the 326, seed fixed (keys must move, else the rival has no lever, which is itself reported). Separate outputs. Rerun must be byte-identical for the read's output.

## Expectation, mine, on record
Any form PASS on both footings: 7 %. NEAR MISS on canonical somewhere: 35 %. F1, F6 or F8 best: 60 %, since I built them for this miss. F5, F7 hurt M3 or X-COP: 60 %. Alt still worse than canonical on all: 65 %. Rival: NOT SEPARABLE 65 %, NOT SEPARATED 25 %, either BETTER 10 %. Random control fraction at or above 0.10: 50 %: the honest likeliest reading is that a falling radial shape helps, and no particular form is earned.

## Limits known now
No field equation. Bullet offset untested and the same threat to all gas forms. X-COP hydrostatic. Keys are KiDS; HSC's disagreement (UX3 Part C) isn't resolved here. Catalogue gas. Stars in the grader are a constant share, so forms can't differ by stars there.
