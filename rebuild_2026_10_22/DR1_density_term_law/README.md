# DR1_density_term_law: SPARC BREAKS, CLUSTERS NOT REACHED. The term g_D² = a₀[g_b + (4πGr/3)ρ_b] worsens SPARC on every reading and closes about 16 % of the law's X-COP deficit in dex; no density can close the rest

Criteria: `FROZEN_CRITERIA.md` (b601d76632), committed alone first. `dr1_offline.py`, `dr1_clusters.py`, `dr1_tail.py`; numbers in `dr1_offline.out`, `dr1_offline.json`, `dr1_g*.json`. MUTATE: `dr1_offline_MUTATE_*`, and rows in `dr1_g005_f034.json`. Post-result: `dr1_stress.py`. κ = ½ FITTED, unchanged. No halo, no cold dark energy here. Not theory closed. Nothing here says the data favour the framework. **Not blind:** see the criteria.

## Rule
ρ_b is spherically averaged: ρ_b = (dM_b/dr)/(4πr²), M_b = r²g_b/G, floored at ρ_b = 0. So g_s = g_b(1 + cS/3), S = dln M_b/dln r. c = 1 is the claim, c = 0 the plain law, c = 3 Verlinde's coefficient. No new number. On a disc M_b is the spherical-equivalent mass, a definition, not the enclosed mass. R1 (primary): g(g − g_b) = a₀g_s. R2: g = g_b + √(a₀g_s). R3: g² = g_b² + a₀g_s.

## Results
Υ per galaxy; A and B identical with no halo. Keys: 15, gas +0.005 (GS4), f★ 0.034, h 0.672 Z shown; failing keys count either h.

| Row | rms can | Υ can | tilt can | rms alt | Υ alt | tilt alt | X-COP can mean, rms | keys | G-OUT-M3 | G-MID-T3 | G-OUT-all | Groups Z |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **R1 c0, plain law** | **0.0541** | **0.52** | **+0.02** | 0.0537 | 0.44 | −0.02 | **+0.467, 0.476** | **10** | **+4.76** | +4.67 | −0.97 | +0.31 |
| **R1 c1, claim** | **0.0594** | **0.41** | **−0.18** | 0.0613 | 0.35 | −0.13 | **+0.393, 0.403** | **11** | **+3.66** | +3.95 | −1.70 | −0.19 |
| R1 c3, Verlinde's coefficient | 0.0754 | 0.30 | −0.11 | 0.0816 | 0.30 | −0.07 | +0.297, 0.310 | 7 | +1.80 | | −2.97 | −0.97 |
| R2 c0 | 0.0556 | 0.39 | +0.02 | 0.0583 | 0.34 | −0.03 | +0.406, 0.415 | 10 | +4.04 | | −1.35 | +0.22 |
| R2 c1 | 0.0640 | 0.31 | −0.07 | 0.0695 | 0.30 | −0.03 | +0.340, 0.350 | 10 | +2.94 | | −2.09 | −0.27 |
| R3 c0 | 0.0627 | 0.65 | +0.09 | 0.0581 | 0.56 | 0.00 | +0.522, 0.531 | 10 | +5.40 | | −0.62 | +0.39 |
| R3 c1 | 0.0652 | 0.50 | −0.19 | 0.0631 | 0.44 | −0.23 | +0.443, 0.452 | 10 | +4.32 | | −1.35 | −0.11 |
| R3 c3 | 0.0769 | 0.36 | −0.23 | 0.0793 | 0.30 | −0.15 | +0.339, 0.351 | 8 | +2.47 | | −2.60 | −0.91 |

Υ by V_flat, R1: plain 0.42, 0.62, 0.65, 0.44, 0.54, 0.70; claim 0.30, 0.39, 0.54, 0.40, 0.51, 0.68. Dwarfs fall to the grid floor.

f★ 0.0615, R1 c1: 11 keys, G-OUT-M3 +3.52. Alt, R1 c1: 10 keys, +2.78. Gas +0.111, a scale the data don't support, R1 c1: 8 keys, because G-OUT-all and low-mass keys go OVER while G-OUT-M3 is still +2.28.

## Frozen label
**SPARC BREAKS, CLUSTERS NOT REACHED**, on R1, c = 1, canonical: Υ 0.41 off the line, tilt −0.18 beyond 0.15, X-COP and keys fail. No [READING-DEPENDENT] tag: R2 breaks Υ; R3 sits on Υ 0.50 at canonical but its tilt fails on both footings. **IMPROVES: no,** rms rises on all three readings and both footings. Passes in the table: rms line, groups. My expectation held; the rms rise is slightly bigger than I guessed.

## The main test: does the term reach the cluster deficit?
**No, and it can't.** Median X-COP S is 1.52 at x ≤ 0.75, moving log(M_HSE/M) from +0.467 to +0.393, 16 % of the way. The S that would give M_HSE has median 34 (alt 28), and every one of the 35 rows needs S > 3, while S ≤ 3 is the ceiling for a density falling outward. MUTATE at S ≡ 3 in every row still leaves +0.343. So at c = 1 the term has no route to clusters, whatever the density profile. X-COP is hydrostatic; the keys aren't, and agree in direction: G-OUT-M3 stays +3.66.

The term helps the heaviest clusters and hurts the lighter ones in the same run: at c = 3 G-OUT-M3 clears (+1.80) but G-OUT-all goes −2.97, and SPARC is gone. S at 1.4 Mpc is about 0.83 in the median, so it isn't selective by mass. The law's trouble here is the trend with mass (G-MID-b, G-OUT-b, G-MID-T3 stay out), which S doesn't address.

## Other parts of the claim
- **"Vanishes outside discs":** exact where ρ_b = 0, so 1/R lensing is unchanged there. SPARC's last point still has median S 0.46, so it's beyond the gas, and any CGM keeps the term on. Not graded with KiDS.
- **"Improves on the law":** no. Surface-brightness slope, HS1's: −0.016 ± 0.060 → −0.072 ± 0.065, still flat, moving the wrong way (reported).
- **LITTLE THINGS: can't be graded.** The rows hold one point, with no baryon profile. Bracket only: median E −0.025 (S = 0), −0.084 (1), −0.168 (3); the line breaks somewhere between S = 1 and 3.
- **Citation:** Yoon, Han, Hwang, arXiv:2601.01715 exists, with the 5.2σ (Stouffer; Fisher 4.5, binomial 4.0) over MOND in 23 dSphs. Look-up, PROVISIONAL, preprint. **Its form is coefficient 1, g² = g_b² + (a/6)(g_b + 4πGρr), a = 5.41e-10, in quadrature: not the claim's 1/3.** That's R3 c3's family, up to amplitude, which p34 and this lane both find much worse on SPARC. It compares against MOND, not this law; not regraded here, no dSph data used.

## Record
Coefficient 1 was already out: p34 Δχ² +1389 / +2216. CFG117 and CFG231 fail G1 on the mass-additive form. Coefficient 1/3 was not on record; it's now closed at this definition of ρ_b.

## Limits
M_b is spherical-equivalent on discs; a true enclosed mass would change S there but not X-COP's ceiling, which is what stops the cluster side. X-COP's S comes from each cluster's measured rows, a coarse radial grid. Post-result stress, not graded: a 5-point mean on dM/dr gives Υ 0.40, rms 0.0590, tilt −0.18, so derivative noise doesn't carry SPARC's result.

## Checks
K1 c = 0 reproduces the law rms 6.9e-18, Υ 0.52, 0.44. K2 unmodified grader on NR1's preds 0, template 0. K3 LITTLE THINGS 0.0002. K4 0, 2.1e-25. K5 HS1's law slope 1.2e-17. K6 R3 c3 worse than c0 (χ² 37060 → 55825), as p34 reports. MUTATE S × 0: returns plain exactly on SPARC, X-COP, keys. S ≡ 3: Υ 0.52 → 0.30, X-COP +0.343, 6 keys: bites. KiDS, Local Group, MW not run.

κ = ½ FITTED. Not theory closed.
