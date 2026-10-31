# SI3_nested_isolation: NO VERDICT as frozen, because my clone rule failed K_H3. With that rule fixed after the fact, the law's lead holds on S_strict and is gone on S_x300

Criteria: `FROZEN_CRITERIA.md` (60575303a2), committed alone before any script output or model number. Frozen run: b832059eca, scripts `si3_hole.py`, `si3_grade.py`, outputs `si3.out`, `si3_results.json`, `si3_MUTATE.*`. Post-result: `AMENDMENT_A1.md` (6e300b3366), `si3_a1*`; `AMENDMENT_A2.md` (1f91298bb9), `si3_a2*`. Scratch work files are rebuilt from fixed seeds by those scripts.

## Verdict
**Frozen: NO VERDICT.** K_H3 failed. Lens/I source weight per centre in O2 is 1.12, 1.19, 1.23, 1.28, 1.39 on S10, S20, S30, S_strict, S_x300, against a limit of 1.10. Every other check passes. The failure touches the hole term only, so the raw L lines stand as raw L, and the Δ = L − I numbers below carry no verdict.

**Why it failed.** My frozen clone rule drew a lens, then kept the point if it passed the veto. The veto accepts high-z and massive clones more easily, so I did not keep the lenses' z and mass. Mean z in mass bin 1 went from 0.235 to 0.269 on S10 and from 0.325 to 0.409 on S_x300. That skew alone predicts ratios of 1.10 to 1.33 from the catalogues. K_H3 caught a real flaw in I.

**A2 reading (post-result, not the lane verdict).** Per-lens clones give every lens exactly 4 accepted points, with no free parameter. K_H3 then passes at 1.02 to 1.05, and all 8 checks pass. The frozen rule on Δ_c = L − I_c reads: **LEAD SURVIVES STRICT ISOLATION; S_x300 differs: LEAD GONE.** I had seen the frozen Δ lines before writing that rule. Whether to adopt it is the owner's call.

**Is KiDS's lead environmental?**
- **Part of it, yes.** At S10 the data run above the law itself: Q = Δχ²/D² is +1.73 ± 0.12, where +1 is what the law predicts. That excess is gone by S_strict, with Q +1.02 ± 0.27. The fall is 0.70 ± 0.19 (paired jackknife), and 1.18 ± 0.19 on the frozen I.
- **All of it depends on the host veto.** On S_strict the lead is what the law predicts: Δχ² +56.5 against D² 55.4, law p 0.63, route E p 5e-5. On S_x300, which removes about 99 % of hosts where S_strict removes about 62 % (F2's A1), the lead is +4.3 at D 5.73, Q +0.13 ± 0.35, and both models fit (p 0.54, 0.39). That Q is 2.5σ below the law and 3.2σ above route E. The label there is narrow: the line is +9.9, and I_c's two halves give +11.2 and −2.6.
- **Neither model has a neighbour term,** which leans toward the law (see limits).

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. The theory stays open. Nothing here says the data favour the framework.

## Δχ² = χ²(route E) − χ²(law) by sample, canonical
No fitted parameter. 59 cells. Block-diagonal 50-patch jackknife with Hartlap. N counts lenses in mass bins 1 to 4, so it is 2 to 46 below F2's sample counts (181,477 and 40,576). Q is +1 if the law is true and −1 if route E is true, σ = 2/D. Q is the column to compare between samples, because raw Δχ² falls with N regardless. NEITHER at S10 and S20 means above the law's band.

The two-halo columns are X53's statistic, the one that gives +434 on B21's bins. They are reported and not graded, because that template has ΛCDM-inherited initial conditions and 4 fitted amplitudes.

**R2**

| sample | N | Δ_c = L − I_c: Δχ² | D | Q | class | χ²(law), p | χ²(route E), p | frozen Δ = L − I: Δχ² | Q | raw L: Δχ² | Q | two-halo, Δ_c | two-halo, Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S10 | 181,431 | **+442.9** | 16.02 | +1.73 ± 0.12 | NEITHER | 121.0, 4e-6 | 563.8, 2e-83 | +427.2 | +1.69 | +473.3 | +1.60 | +207.8 | +201.1 |
| S20 | 93,012 | **+236.5** | 11.71 | +1.73 ± 0.17 | NEITHER | 87.8, 9e-3 | 324.3, 3e-38 | +200.0 | +1.58 | +249.6 | +1.49 | +114.3 | +98.9 |
| S30 | 57,261 | **+95.8** | 8.49 | +1.33 ± 0.24 | LAW PREFERRED | 67.7, 0.20 | 163.5, 9e-12 | +98.2 | +1.37 | +101.6 | +1.08 | +59.8 | +71.6 |
| S_strict | 40,574 | **+56.5** | 7.44 | +1.02 ± 0.27 | LAW PREFERRED | 54.8, 0.63 | 111.3, 5e-5 | +35.5 | +0.52 | +0.2 | +0.00 | +32.5 | +21.2 |
| S_x300 | 21,571 | **+4.3** | 5.73 | +0.13 ± 0.35 | NEITHER | 57.1, 0.54 | 61.5, 0.39 | +10.3 | +0.30 | −49.3 | −1.11 | −2.2 | +2.8 |

**R0**

| sample | N | Δ_c = L − I_c: Δχ² | D | Q | class | χ²(law), p | χ²(route E), p | frozen Δ = L − I: Δχ² | Q | raw L: Δχ² | Q | two-halo, Δ_c | two-halo, Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S10 | 181,431 | **+501.8** | 14.76 | +2.30 ± 0.14 | NEITHER | 203.1, 1e-17 | 704.9, 2e-111 | +466.0 | +2.18 | +551.7 | +2.15 | +277.1 | +253.8 |
| S20 | 93,012 | **+284.1** | 10.99 | +2.35 ± 0.18 | NEITHER | 136.8, 4e-8 | 420.9, 5e-56 | +229.0 | +2.17 | +300.8 | +2.08 | +154.0 | +131.5 |
| S30 | 57,261 | **+115.1** | 7.87 | +1.86 ± 0.25 | NEITHER | 84.1, 0.02 | 199.2, 4e-17 | +123.0 | +1.93 | +132.4 | +1.62 | +73.7 | +91.9 |
| S_strict | 40,574 | **+71.1** | 6.84 | +1.52 ± 0.29 | LAW PREFERRED | 65.8, 0.25 | 136.9, 4e-8 | +57.9 | +1.00 | +28.4 | +0.47 | +47.2 | +38.0 |
| S_x300 | 21,571 | **+14.7** | 5.33 | +0.52 ± 0.38 | LAW PREFERRED | 55.2, 0.62 | 70.0, 0.16 | +24.5 | +0.82 | −18.5 | −0.46 | +6.1 | +12.7 |

The labels on Δ_c at R0 are the same, except that S_x300 reads MIXED.

**For scale, on B21's bins at R0 (K1):** +667.4 with no two-halo term, +434.4 with it. Absolute Δχ² here is not directly comparable with those, because the sample, the bins and the covariance all differ. Taking B21's released matrix down to its block-diagonal part gives +764.4 and +465.3, so on those bins the block choice runs 15 % and 7 % high.

**Alt, R2**

| sample | Δ_c: Δχ² | D | Q | class | p(law) | p(route E) | frozen Δ: Δχ² | raw L: Δχ² |
|---|---|---|---|---|---|---|---|---|
| S10 | +460.3 | 18.19 | +1.39 ± 0.11 | NEITHER | 2e-4 | 9e-84 | +444.5 | +492.4 |
| S20 | +249.2 | 13.51 | +1.37 ± 0.15 | NEITHER | 0.07 | 2e-38 | +211.3 | +262.3 |
| S30 | +97.9 | 9.65 | +1.05 ± 0.21 | LAW PREFERRED | 0.25 | 9e-12 | +101.6 | +100.8 |
| S_strict | +57.6 | 8.42 | +0.81 ± 0.24 | LAW PREFERRED | 0.67 | 5e-5 | +32.4 | −7.5 |
| S_x300 | −0.1 | 6.49 | −0.00 ± 0.31 | NEITHER | 0.39 | 0.39 | +6.7 | −61.3 |

**Alt, R0**

| sample | Δ_c: Δχ² | D | Q | class | p(law) | p(route E) | frozen Δ: Δχ² | raw L: Δχ² |
|---|---|---|---|---|---|---|---|---|
| S10 | +547.9 | 16.82 | +1.94 ± 0.12 | NEITHER | 5e-11 | 1e-111 | +507.1 | +602.9 |
| S20 | +313.1 | 12.66 | +1.95 ± 0.16 | NEITHER | 9e-5 | 4e-56 | +251.6 | +330.7 |
| S30 | +124.3 | 8.94 | +1.56 ± 0.22 | NEITHER | 0.08 | 4e-17 | +133.9 | +141.3 |
| S_strict | +76.9 | 7.75 | +1.28 ± 0.26 | LAW PREFERRED | 0.44 | 4e-8 | +60.8 | +28.3 |
| S_x300 | +14.3 | 6.03 | +0.39 ± 0.33 | LAW PREFERRED | 0.60 | 0.16 | +25.9 | −21.5 |

## What the numbers say
- **The raw stacks can't be read at strict isolation.** Raw L's +0.2 and −49.3 are mostly the hole. I_c − R in O2 is −0.76 ± 0.13 on S_strict and −1.24 ± 0.20 on S_x300, and subtracting it takes the raw O2 signal from below zero to above it.
- **The environment acts mostly beyond 1.1 Mpc.** After the hole term, O2 falls throughout, by a factor of about 3. O1 holds at about 3.4 until S_x300.
- **Route E's shortfall at 0.4–1.1 Mpc mostly survives isolation.** Its A_O1 at R2 is 3.99, 3.88, 4.07, 3.38, 2.30. Continuing the halo to r_ta gives 3.24, 3.17, 3.27, 2.76, 1.89. The law's goes 1.34 to 0.81.
- **The lead on S_strict is outer.** Inner +7.8, outer +35.2. On S_x300 inner +2.7, outer +0.7.
- **R2 narrows the lead** at every sample, as on SI2's clean lenses, and it brings A_in to about 1 for both models.
- **Halo to r_ta,** Δ_c, R2 (reported): +387.7, +203.0, +81.1, +46.6, +2.0, with D 14.74, 10.69, 7.75, 6.82, 5.31. Same classes on S30, S_strict and S_x300.

**The hole's own size, and the signal around it** (inverse-variance mean, M☉/pc², native; L is unchanged by the amendments):

| sample | O1: I_c − R | O1: L | O1: L − I_c | O2: I_c − R | O2: L | O2: L − I_c |
|---|---|---|---|---|---|---|
| S10 | +0.18 ± 0.15 | +3.28 ± 0.16 | +3.31 ± 0.20 | −0.15 ± 0.08 | +1.35 ± 0.08 | +1.49 ± 0.08 |
| S20 | +0.07 ± 0.20 | +3.56 ± 0.23 | +3.57 ± 0.26 | −0.32 ± 0.12 | +1.02 ± 0.13 | +1.40 ± 0.14 |
| S30 | −0.20 ± 0.23 | +3.38 ± 0.31 | +3.50 ± 0.34 | −0.65 ± 0.13 | +0.60 ± 0.16 | +1.05 ± 0.17 |
| S_strict | −0.60 ± 0.34 | +3.13 ± 0.36 | +3.43 ± 0.42 | −0.76 ± 0.13 | −0.07 ± 0.16 | +0.76 ± 0.20 |
| S_x300 | −0.74 ± 0.37 | +1.92 ± 0.43 | +2.50 ± 0.48 | −1.24 ± 0.20 | −0.87 ± 0.24 | +0.45 ± 0.26 |

## Amplitudes, canonical (A = data/model, F2's estimator; A_in R ≤ 0.31, A_O1 0.4–1.1, A_O2 1.1–3 Mpc)
**Δ_c = L − I_c, R2**

| sample | law A_in | law A_O1 | law A_O2 | route E A_in | route E A_O1 | route E A_O2 |
|---|---|---|---|---|---|---|
| S10 | 1.08 ± 0.04 | 1.34 ± 0.07 | 1.26 ± 0.07 | 1.04 ± 0.04 | 3.99 ± 0.23 | 10.82 ± 0.67 |
| S20 | 1.06 ± 0.06 | 1.32 ± 0.09 | 1.20 ± 0.11 | 1.00 ± 0.06 | 3.88 ± 0.28 | 10.41 ± 1.01 |
| S30 | 1.05 ± 0.09 | 1.31 ± 0.11 | 0.86 ± 0.15 | 1.01 ± 0.08 | 4.07 ± 0.37 | 7.25 ± 1.29 |
| S_strict | 1.14 ± 0.11 | 1.17 ± 0.14 | 0.63 ± 0.17 | 1.09 ± 0.10 | 3.38 ± 0.46 | 5.33 ± 1.49 |
| S_x300 | 1.05 ± 0.13 | 0.81 ± 0.15 | 0.38 ± 0.21 | 1.00 ± 0.13 | 2.30 ± 0.49 | 3.20 ± 1.91 |

**Δ_c = L − I_c, R0**

| sample | law A_in | law A_O1 | law A_O2 | route E A_in | route E A_O1 | route E A_O2 |
|---|---|---|---|---|---|---|
| S10 | 1.31 ± 0.05 | 1.57 ± 0.09 | 1.50 ± 0.08 | 1.39 ± 0.06 | 6.22 ± 0.35 | 16.69 ± 1.02 |
| S20 | 1.28 ± 0.07 | 1.56 ± 0.10 | 1.41 ± 0.13 | 1.32 ± 0.08 | 5.96 ± 0.42 | 15.87 ± 1.50 |
| S30 | 1.25 ± 0.10 | 1.53 ± 0.13 | 1.02 ± 0.17 | 1.31 ± 0.11 | 6.12 ± 0.55 | 10.98 ± 1.90 |
| S_strict | 1.36 ± 0.13 | 1.38 ± 0.16 | 0.74 ± 0.20 | 1.42 ± 0.14 | 5.15 ± 0.68 | 7.99 ± 2.20 |
| S_x300 | 1.28 ± 0.16 | 0.95 ± 0.18 | 0.45 ± 0.25 | 1.33 ± 0.17 | 3.50 ± 0.73 | 4.81 ± 2.82 |

**Frozen Δ = L − I, R2 (no verdict)**

| sample | law A_in | law A_O1 | law A_O2 | route E A_in | route E A_O1 | route E A_O2 |
|---|---|---|---|---|---|---|
| S10 | 1.07 ± 0.04 | 1.31 ± 0.06 | 1.34 ± 0.07 | 1.02 ± 0.04 | 3.90 ± 0.20 | 11.34 ± 0.64 |
| S20 | 1.08 ± 0.07 | 1.34 ± 0.09 | 1.22 ± 0.11 | 1.04 ± 0.07 | 3.98 ± 0.30 | 10.51 ± 0.98 |
| S30 | 1.09 ± 0.09 | 1.40 ± 0.13 | 0.79 ± 0.15 | 1.03 ± 0.09 | 4.13 ± 0.41 | 6.61 ± 1.33 |
| S_strict | 1.17 ± 0.12 | 1.25 ± 0.12 | 0.53 ± 0.15 | 1.11 ± 0.12 | 3.75 ± 0.41 | 4.74 ± 1.25 |
| S_x300 | 1.08 ± 0.13 | 1.03 ± 0.18 | 0.35 ± 0.22 | 1.02 ± 0.12 | 3.09 ± 0.56 | 2.43 ± 1.87 |

**Frozen Δ = L − I, R0 (no verdict)**

| sample | law A_in | law A_O1 | law A_O2 | route E A_in | route E A_O1 | route E A_O2 |
|---|---|---|---|---|---|---|
| S10 | 1.30 ± 0.05 | 1.55 ± 0.07 | 1.59 ± 0.08 | 1.36 ± 0.06 | 6.09 ± 0.31 | 17.48 ± 0.98 |
| S20 | 1.30 ± 0.09 | 1.57 ± 0.11 | 1.44 ± 0.13 | 1.37 ± 0.09 | 6.06 ± 0.45 | 16.07 ± 1.48 |
| S30 | 1.30 ± 0.11 | 1.64 ± 0.15 | 0.92 ± 0.18 | 1.35 ± 0.12 | 6.28 ± 0.61 | 9.99 ± 1.97 |
| S_strict | 1.40 ± 0.15 | 1.47 ± 0.14 | 0.61 ± 0.18 | 1.47 ± 0.16 | 5.69 ± 0.61 | 7.10 ± 1.87 |
| S_x300 | 1.32 ± 0.16 | 1.21 ± 0.21 | 0.41 ± 0.26 | 1.36 ± 0.17 | 4.68 ± 0.85 | 3.71 ± 2.77 |

**Raw L, R2**

| sample | law A_in | law A_O1 | law A_O2 | route E A_in | route E A_O1 | route E A_O2 |
|---|---|---|---|---|---|---|
| S10 | 1.12 ± 0.04 | 1.35 ± 0.06 | 1.17 ± 0.07 | 1.07 ± 0.04 | 3.98 ± 0.19 | 10.33 ± 0.63 |
| S20 | 1.08 ± 0.06 | 1.34 ± 0.08 | 0.93 ± 0.10 | 1.03 ± 0.06 | 4.12 ± 0.27 | 8.62 ± 0.91 |
| S30 | 1.06 ± 0.08 | 1.25 ± 0.11 | 0.54 ± 0.13 | 1.02 ± 0.08 | 3.88 ± 0.35 | 5.02 ± 1.18 |
| S_strict | 1.10 ± 0.10 | 1.12 ± 0.12 | 0.05 ± 0.14 | 1.04 ± 0.10 | 3.43 ± 0.41 | 1.16 ± 1.24 |
| S_x300 | 1.09 ± 0.11 | 0.70 ± 0.14 | −0.63 ± 0.19 | 1.03 ± 0.11 | 2.21 ± 0.44 | −4.77 ± 1.66 |

**Raw L, R0** (the law's columns reproduce F2's README)

| sample | law A_in | law A_O1 | law A_O2 | route E A_in | route E A_O1 | route E A_O2 |
|---|---|---|---|---|---|---|
| S10 | 1.34 ± 0.05 | 1.59 ± 0.07 | 1.40 ± 0.08 | 1.42 ± 0.06 | 6.21 ± 0.29 | 15.95 ± 0.96 |
| S20 | 1.29 ± 0.07 | 1.58 ± 0.10 | 1.10 ± 0.12 | 1.35 ± 0.08 | 6.30 ± 0.41 | 13.19 ± 1.36 |
| S30 | 1.26 ± 0.10 | 1.46 ± 0.12 | 0.64 ± 0.15 | 1.31 ± 0.11 | 5.84 ± 0.51 | 7.64 ± 1.74 |
| S_strict | 1.31 ± 0.12 | 1.31 ± 0.14 | 0.06 ± 0.16 | 1.36 ± 0.13 | 5.17 ± 0.60 | 1.66 ± 1.83 |
| S_x300 | 1.32 ± 0.14 | 0.82 ± 0.16 | −0.74 ± 0.23 | 1.38 ± 0.15 | 3.33 ± 0.66 | −7.15 ± 2.46 |

## Argon's score (R2, canonical; the frozen line is the one with no verdict)
| Argon's line | Argon | frozen Δ | Δ_c | two-halo, frozen Δ | two-halo, Δ_c |
|---|---|---|---|---|---|
| S10 Δχ² | +280 to +350 | +427.2 MISS | +442.9 MISS | +201.1 MISS | +207.8 MISS |
| S30 Δχ² | +80 to +140 | **+98.2 HIT** | **+95.8 HIT** | +71.6 MISS | +59.8 MISS |
| S_strict Δχ² | −5 to +15 | +35.5 MISS | +56.5 MISS | +21.2 MISS | +32.5 MISS |
| S_strict A_O1 data/route E | 1.35 ± 0.25 | 3.75 ± 0.41 MISS | 3.38 ± 0.46 MISS | same | same |
| S_strict A_O2 data/law | at or below 0.35 | 0.53 ± 0.15 MISS | 0.63 ± 0.17 MISS | same | same |
| Pass line: at or below +15, A_O2 route E within 2σ of 1 | | not met (4.74 ± 1.25) | not met (5.33 ± 1.49) | not met | not met |
| Fail line: D ≥ 5 and Δχ² ≥ +25 | | **met** (D 8.27) | **met** (D 7.44) | not met (D 5.07) | not met (D 4.86) |
| Falsifier: above +30 on S_strict | | **fires** | **fires** | no | **fires** |

**One band of five on the graded statistic, none on the two-halo line.** Argon's text doesn't name the covariance or a two-halo term, so these scores are conditional on my frozen choices. Its A_O2 in the pass line doesn't name a model. I read it as route E's, and the law's misses as well.

Its S_strict band describes S_x300 instead, which it didn't predict: +4.3 or +10.3, with A_O2 data/law 0.38 ± 0.21 or 0.35 ± 0.22. Its A_O1 band misses there too, at 2.30 ± 0.49. No neighbour term is in these A_O1 values, and with the halo to r_ta S_strict gives 2.76 ± 0.36.

## Checks
| check | frozen I | I_c |
|---|---|---|
| K0: F2's law A_in, A_O1, A_O2 and errors, five samples, both footings | PASS, \|d\| 0 | PASS |
| K1: FC1's χ² and b on B21's bins, both footings | PASS, \|d\| 0 | PASS |
| K2: tables against direct projection; M_h(R200) | PASS, 3.4e-3; 2e-15 | PASS |
| K_H1: P2's record path on 3,000 real lenses against CFG110 and CFG116 | PASS, ΣWW 1e-9, ΔΣ 3e-8 σ | carries over |
| K_H2: veto on all 181,477 lenses reproduces S10, S20, S30, host, host300 | PASS, 0 mismatches | PASS |
| K_H3: patches; lens/I weight in O2 within 0.10 of 1 | **FAIL**, 1.12 to 1.39 | PASS, 1.02 to 1.05 |
| K_H4: cross-shear null of Δ, p ≥ 0.001 | PASS, lowest 0.0024 | PASS, lowest 0.0097 |
| K_H5: two halves of I, p ≥ 0.001 | PASS, lowest 0.10 | PASS, lowest 0.15 |

**MUTATE bites** (`si3_MUTATE.*`): route E's halo × 0.5, lens WG × 1.10, I from cross shear. K0 and K1 fail, m_H falls in every used cell, every sample's χ²(route E) and Δ change, the run prints NO VERDICT and exits 1.

**I_c's own noise** (`si3_a2_noise.out`, from its two halves): ± 17 on S10, 12.5 on S20, 7.3 on S30, 8.4 on S_strict, 4.8 on S_x300 in Δχ² at R2. The shift from frozen I to I_c is +15.6, +36.6, −2.4, +21.0, −6.0. Only S20 passes 2σ of two such catalogues. So the skew changes these Δχ² modestly, and most of the difference between the two Δχ² columns could be catalogue noise.

**Pre-freeze probe, disclosed in the criteria:** timing only, no shear number.

## Disclosures
- **The clone rule is my error in the frozen design.** The check I froze caught it.
- **A1's reading was wrong.** I blamed thinly covered sky. Matching on source coverage left the ratio at 1.09 to 1.35. The next line of evidence, the clones' z and mass, explained it. A1's run is kept (`si3_a1.out`), and it is the record of how the wrong reading failed.
- **A number was wrong in two commits.** A1's commit message and the first version of A2 said A1 moved every Δχ² by less than 8. The right figure is at most 9.4, corrected in 0aea921de5.
- **P2, SI1 and SI2 use the same draw-then-veto rule.** P2's acceptance is 0.45 on S3 and 0.71 on S1, and its stated "same z, M★" for I may not hold exactly. I have not tested that. Those lanes' results should not be taken as affected or unaffected until someone does.

## What this cannot show
- **Neighbours.** Neither graded model has a neighbour term, because a photo-z catalogue can't place neighbours along the line of sight. That leans toward the law, since route E's mass sits in halos. SI1 measured the term at +3.7 in Δχ² on N = 10,620. X53's two-halo line is the only proxy here: +32.5 on S_strict, −2.2 on S_x300. Its template has ΛCDM-inherited initial conditions, and it is not a grade.
- **Leakage.** F2's A1 estimates S_strict still leaks about 38 % of hosts. Δ removes the hole, not leaked hosts. S_x300's window catches about 99 %, but it was defined after F2's result and has half the lenses.
- **The mass mix changes with isolation.** Mass bin 1 is 28 % of S10 and 5 % of S_x300; bin 4 is 25 % and 52 %. So Q between samples is not a pure isolation effect. Per-mass-bin Δχ² on Δ_c at R2: S_strict +8.0, +5.0, +19.4, +24.1; S_x300 +3.6, −0.2, −6.6, +7.5.
- **R2 is an open choice,** taken from the record. Readings at R2 are conditional on it. At R0 S_x300 reads MIXED, not LEAD GONE.
- **Route E's rule is taken as given.** X53's sharp cut at R200 at FC1's rule. EM1's M200 relation was calibrated with NFW halos and Bullock c(M), which the record's own audit flags.
- **Covariance.** Dropping cross-mass terms runs 7 to 15 % high on B21's bins, and a noisy jackknife inverse adds scatter that Hartlap doesn't remove. p-values use χ²(n), as in SI1.
- **Sample.** S10 is the record's reconstruction of B21's sample (181k against 259k), and it runs 1.15 × B21 (F2 K4b).
- **A2 is post-result.** Its label cannot give the lane a verdict.
- A preference here compares two members of this record only.

## Next
- Decide whether to adopt per-lens clones and rerun under a new freeze.
- Test the same clone fix on P2, SI1 and SI2.
- A spectroscopic neighbour term at this N would settle the S_strict and S_x300 split, and GAMA can't supply that N.

## Compute
One thread, `nice -n 15`, at most two processes at once. Peak RSS 1.78 GB and 2.02 GB in the two catalogue stages, below 1.1 GB elsewhere. Wall time about 40 min for the frozen hole stacks and 5 min for each grade, with the zooms running. Run order: `si3_hole.py cat`, `si3_hole.py measure` north and south, `si3_grade.py`; then `si3_a1_measure.py`, `si3_a1_grade.py`; then `si3_a2.py cat`, `measure`, `grade`, `noise`.
