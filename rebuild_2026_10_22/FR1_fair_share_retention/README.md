# FR1_fair_share_retention: NOT RETENTION [MASS-METHOD-DEPENDENT] [ERROR-DEPENDENT] as frozen, by a hair. A measured gas-fraction line, without X-COP or shear, has the right sign and takes measured-gas clusters to 14 of 15 keys with X-COP passing, but G-OUT-M3 stays +3.48, +3.09. Reach 0.31 to 0.47, the line was 0.33 in all four cells

Criteria: `FROZEN_CRITERIA.md` (e58eb28ed2), committed alone first. `fr1_line.py`, `fr1_def.py`, `fr1.py`, `fr1_read.py`, `fr1_quick.py`; numbers in `fr1_line.out`, `fr1_line.json`, `fr1.out`, `fr1_results.json`, `fr1_MUTATE.out`. Other lanes read only. **Not blind.** kappa = 1/2 FITTED, unused. The line is FITTED to gas-fraction data, not to keys. Cold dark energy, never a particle. No a0 in the cold sector. Not theory closed. Nothing here says the data favour the framework. FG1's verdict and the owner's retirement of route E's cold sector stand. **Galaxies aren't touched, so this says nothing like route E passes.**

## Answer
**Does measured data show it? The sign and trend, yes. The required size, no, not on the frozen line.** Hydrostatic line H, 176 clusters, 44 below lg M500 14.3, X-COP removed: lg Y500 (gas only, h 0.7) = -0.121 +- 0.006 + 0.219 +- 0.016 (lg M500 - 14.5). Same line reads -0.051 at X-COP's mass with f* 0.034, against X-COP's own -0.042, so the out-of-sample test lands, with the hydrostatic method shared.

| | lg Y |
|---|---|
| M3, Y500, on the line (model's lg M500 14.35) | -0.120 |
| **carry, R500 to R200, GS1's gas slope + ZN4's shape** | **+0.062** |
| **M3, Y200** | **-0.055**, cold/baryon 6.11 |
| HM1's need for Z 2, Z 0 | -0.127, -0.203 (7.4 to 9) |

So the data reach the need at R500 and the carry takes half of it back. X-COP's own measured carry is +0.031.

## Grades, gas +0.005 (GS4), ZN4's native profile. f* and h cells: G-OUT-M3 doesn't depend on f*, since (1 + f*) cancels
| Row | keys | G-OUT-M3, h 0.672, 0.686 | Z_tot | joint chi^2 for 15, p | X-COP | reach |
|---|---|---|---|---|---|---|
| fair share (= ZN4) | 12, 12 | +4.41, +4.07; +4.13, +3.81 | +3.51 to +3.03 | 31.9-38.2, 9e-4 to 7e-3 FAIL | +0.013, 0.075 PASS | |
| **H, PRIMARY** | **14, 14** | **+3.48, +3.09** | **+2.77, +2.46** | **20.1-20.3, 0.16-0.17 PASS** | **+0.024, 0.072 PASS** | **0.31 to 0.47** |
| H - 1 sigma | 14 | +3.27, +2.89 | +2.61, +2.30 | 18.3-18.5 | +0.018 PASS | 0.40 to 0.57 |
| H + 1 sigma | 13 | +3.69, +3.29 | +2.94, +2.62 | 22.1-22.3 | +0.031 PASS | 0.21 to 0.38 |
| HG, Y on gas | 14 | +3.43, +3.03 | +2.73, +2.42 | 19.5 | +0.030 PASS | 0.33 to 0.50 |
| H + g, HL2's +0.031 | 14 | +2.57, +2.22 | +2.05, +1.77 | 13.6 | -0.003 PASS | 0.73 to 0.89 |
| **W, lensing or WL-calibrated T** | **6** | **-2.00, -2.19** | -1.59, -1.74 | 32.6-37.3 FAIL | **-0.097, 0.117 FAIL** | over 2.6, overshoots |
| H without L20 | 12 | +4.08, +3.66 | +3.26, +2.92 | 26 | +0.056 FAIL | 0.02 to 0.20 |
| H without L15, S09 | 12 | +4.71, +4.32 | +3.76, +3.43 | 39 | +0.024 PASS | negative |
| H at +0.111, reported only, scale unsupported | 15 | +0.74 | | | +0.024 PASS | |

The p values use M3A1's R from the fair-share row, disclosed. **Only G-OUT-M3 stays over 2 on H,** and the other two keys ZN4 fails come in. **Verdict reads on the one cell f* 0.0615, h 0.672: reach 0.306 against 0.333.** The others are 0.39, 0.47, 0.40. The label is frozen; that it's a hair is the fair reading, hence [ERROR-DEPENDENT]. This isn't a pass in any row on measured gas.

Post-result, no label, f* 0.034:
- H with X-COP's measured carry +0.031, not GS1 + ZN4: 14, M3 +2.85, +2.50, Z_tot +2.27, X-COP +0.027.
- H + g with that carry: 14, M3 **+2.03, +1.72**, Z_tot +1.62, X-COP +0.003. Two choices made after seeing the result; still 14 at h 0.672 by 0.03. Not a claim.
- GS1's tail s 2.676, 3.071: M3 +3.48, +3.49. The carry isn't from s: most of it lies inside eRASS1's own R500, on the measured profile.

## What's weak
1. **The line's real error at M3's mass is about 0.04 dex, not its bootstrap 0.008.** M3 sits at lg M500 14.34 (h 0.7), between two sets: L20 above, L15 + S09 below. In 14-14.5 there are 18 clusters: median -0.137 +- 0.043, line -0.157. Z moves 27 per dex, so ±0.04 is ±1.1 in Z. **Slope 0.219 is steeper than inside either set** (L20 0.17 +- 0.04, L15 + S09 0.10 +- 0.06), so part of it is a step between samples, instruments and selection. The two leave-out rows show it.
2. **Mass method, the main open thing.** XXL (WL-calibrated M-T, Eckert+16) reads lg Y -0.50 +- 0.06 at lg M500 14.5 with hardly a slope. H reads -0.12. Those differ far more than HL2's +0.03, on different clusters. W's slope is negative because WL noise in M drives it (pairs alone -0.22 +- 0.07), as frozen. So W doesn't support retention at this size; it says lensing-tied masses at low mass aren't settled.
3. **Carry.** GS1's slope is measured on X-COP only, and lighter clusters have no measurement here. A carry of 0.062 against X-COP's 0.031 moves M3 by 0.6.
4. Selection: X-ray bright low-mass samples are likely gas-rich, so Y is high there. Group stars above f* would go the other way. Neither applied, sizes unknown. No z trend in the line.

## Same statement as EM1? (report only)
EM1 as Y200 against line H with M3's carry, line minus EM1, lg: lg M_b 14 +0.08; 13.5 +0.03; 13 -0.02; 12.5 -0.07 (measured down to here); 12 -0.12; 11 -0.21; 10 -0.31 (no data). **Inside 0.07 dex across lg M200 13.5-14.4, on data EM1 never saw,** and that is real news for G13. Below 1e13 the straight line falls under EM1, which is an extrapolation of a straight line, not a measured break. EM1 is fitted on SPARC, slope in Y 0.11 per dex against 0.22 here, and this carry at 1e13 is unmeasured. So it's a suggestive overlap, not a join. It's why OP2 (+2.39, +2.10) does better than H: EM1's Y200 at M3 is near 0.78, H's 0.88.

## Outside R200
M3: missing (1 - Y200) f_b M200 is 6e12, at HM1's Z 2 line 1.3e13. The grader already holds 1.0e14 of baryons from R200 to r_ta. So the budget has room, and M_c(r_ta)/Mfair is 0.84 with no change to it. **Nothing on disk tests this at M3's mass:** X-COP's gas stops near 2 R500 and is massive; PSZ2's Y5R500 reaches only M500 6-9e14 (GS5) and is unreliable in Y5/Y500; no ACT y map is in `_external_data` now, and GH3/GH4 were galaxy lenses. Not ruled out, not supported.

## Not double counted
GS4 compares two surveys' gas at a radius: +0.005 stays on eRASS1's gas. The line is gas over mass at fixed mass. LF1 and any KiDS mass aren't used. Circularity stated: X-COP tests hydrostatic masses against a hydrostatic line; clusters are separate, method isn't, so its pass doesn't vouch for hydrostatic masses.

## Probability judgments, mine
Y500 falls toward low mass on hydrostatic masses: 95 %. It's real gas lack, not all mass bias: 70 %. Y200 at M3 is low enough to bring G-OUT-M3 under 2 on measured gas: 25 %. Retention supplies at least a third of the need: 60 %, higher than the label reads.

## Checks
K1 f_ret 1 per key and X-COP against ZN4, both f*: |d| 0, joint 0, PASS. K2 parser and injected line, PASS. K3 every cluster's solved M500 back through the line, 6e-17, PASS. K4 closure on M3 0.004 dex, all clusters -0.008 to +0.015, PASS. MUTATE slope flip: X-COP -0.158, 256 cells with no solution, M3 +4.48, BITES. By hand: pred 1.040 to 1.150, +0.109; HM1's rate gives +0.151, with M3 picked by Mb200 and shell mix differing, so same size, not exact.

## Errors, disclosed
**GS4's `gs4_inputs.csv` holds Y_X (T x Mgas) in E16's M500 column, not a mass.** GS4 reads only R500, so its results aren't affected. Caught here from an absurd f_gas 0.38, before any grade; E16's mass now comes from its r500; a check across catalogues shows all others agree. **First K1 was off by 1.3e-5 in pred,** from one ulp in f_c through the ill-conditioned thin tail; the exact fair-share expression passes, |d| 0. So predictions carry about that noise. First grade run: labels "Hg"/"HG" and "H+1s"/"H-1s" collided in cache names on a case-blind disk; caught from a jump between f* cells; renamed and rerun. The hand K3 first used wrong h; the grader's canonical background is h 0.6758 for Y, with the 0.672, 0.686 cells applying to the data. Criteria said "per background"; only one is on the canonical path. Y-on-M keeps one ratio of x500 from ZN4 at z 0.25. Thresholds use the grader's bg A rule as before.

## Expectation on record
PARTLY 55 %, NOT 25 %; label NOT by one cell, in spirit between them. Slope 0.1: wrong, 0.22. Carry eating part: right, and I underrated it. X-COP stays passing 70 %: yes. W far off: I didn't foresee it.

Unfinished: nothing frozen. Natural next step, not done: a cluster-mass measurement across lg M500 14-14.5 on one instrument and method, and gas beyond R500 at that mass. Both need data not on disk.

kappa = 1/2 FITTED. Not theory closed.
