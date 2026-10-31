# SC2_clone_rule_on_spec_lenses: per-lens clones change 10 of SI1's and SI2's 20 frozen classes at the frozen counts, all toward route E. A1 traces that to catalogue noise, not the rule. At low noise both rules agree, and neither reads TENSION GONE

Criteria: `FROZEN_CRITERIA.md` (a664f7af34), committed alone before any number. Frozen runs: eda8433972, script `sc2_run.py`, table `sc2_classes.out`. Post-result: `AMENDMENT_A1.md` (29a43ed9a7), `sc2_a1.py`, `sc2_a1_table.py`, `sc2_a1.out`. P2's, SI1's and SI2's own files are not edited.

## Result
**Frozen classes that CHANGE, old rule to per-lens clones at the same counts: 10 of 20.** All go to ROUTE E PREFERRED.

| footing | sample, line | old | new | Δχ² old to new | 20 per lens, new rule | 20 per lens, old rule |
|---|---|---|---|---|---|---|
| canonical | S3 all, R2 | NOT POWERED | ROUTE E | −10.6 to −14.8 | ROUTE E, NOT POWERED | NEITHER, ROUTE E |
| canonical | **S1 all, R0 (SI1's LAW PREFERRED)** | LAW | ROUTE E | +8.7 to −9.8 | NEITHER, NEITHER | NEITHER, NEITHER |
| canonical | S1 red, R0 | LAW | ROUTE E | +16.1 to −8.0 | LAW, NEITHER | NEITHER, NEITHER |
| canonical | S1 red, R2 | NEITHER | ROUTE E | −2.0 to −22.9 | NEITHER, NEITHER | NEITHER, ROUTE E |
| canonical | **S1 all, R2 (SI2's NEITHER)** | NEITHER | ROUTE E | −0.3 to −22.9 | ROUTE E, ROUTE E | ROUTE E, ROUTE E |
| alt | S3 all, R0 | NOT POWERED | ROUTE E | −5.8 to −11.3 | ROUTE E, NOT POWERED | ROUTE E, ROUTE E |
| alt | S1 all, R0 | LAW | ROUTE E | +7.6 to −12.9 | NEITHER, NEITHER | NEITHER, NEITHER |
| alt | S1 red, R0 | LAW | ROUTE E | +17.3 to −11.0 | NEITHER, NEITHER | NEITHER, NEITHER |
| alt | S1 red, R2 | NEITHER | ROUTE E | −6.8 to −31.1 | NEITHER, NEITHER | ROUTE E, ROUTE E |
| alt | S1 all, R2 | NEITHER | ROUTE E | −6.6 to −29.7 | ROUTE E, ROUTE E | ROUTE E, ROUTE E |

**SI2's combined reading does not change at the frozen counts:** LENSING TENSION GONE ON CLEAN LENSES on both. **P2's verdict does not change:** UNDECIDABLE (N too small), on all 16 catalogues.

**The changes are not the rule (A1, post-result).**
- **The rule's effect on Δχ² is consistent with zero on all 20 lines.** The largest is 1.5 se. S1 all at R2: −1.0 ± 5.4 at the frozen counts, +2.2 at 20 per lens. S1 all at R0: −3.5 ± 6.3, and +0.4. S3 all at R2: −7.0 ± 6.4, and +0.1.
- **The old rule moves as much against itself.** Six old-rule catalogues of S1 all at R0 read LAW 2, ROUTE E 3, NEITHER 1, with Δχ² from −22.6 to +13.6. SI1's +8.7 was one of those draws. S1 all at R2 reads ROUTE E 5, NEITHER 1, and SI2's −0.3 is the highest of the six.
- **The rule does fix the weights,** as it should (table below). The skew on GAMA is small, and at this precision it doesn't reach Δχ².

**What the low-noise runs read, under either rule (20 per lens, 2 catalogues per rule, canonical):**
- **SI1's LAW PREFERRED on S1 does not hold.** S1 all at R0 is +1.6, +1.6 (old) and −0.3, +4.3 (new): NEITHER, four of four.
- **SI2's level S1 at R2 does not hold.** S1 all at R2 is −18.2, −18.5 (old) and −15.8, −16.4 (new): ROUTE E PREFERRED, four of four, route E p 0.53 to 0.75, law p 0.006 to 0.03. The raw L − R line, which doesn't use I, gives −17.4 and the same class.
- **S3 leans route E too,** with both fits poor: all at R2 is −16.8 to −30.0, law p below 1e-4, route E p 0.01 to 0.02.
- **SI2's combined reading is MIXED, not TENSION GONE, four of four.** No all-lens line prefers the law. It misses TENSION GONE only because route E's p on S3 is below 0.05 on the frozen χ²(15) reference. Against Hotelling's T², a closer reference for 15 bins from 36 patches, that p is 0.04 to 0.06 and the law's is 0.001 to 0.006, so it sits on the line.

**For gate G8.** The clone rule is not a threat to SI2's headline. Catalogue noise is. SI2's reading rested on one catalogue with 2 clones per lens on S1. TENSION GONE comes up 5 of 6 times on old-rule catalogues at those counts, 4 of 6 on new-rule ones, and 0 of 4 at 20 per lens. Relative to the frozen numbers, less noise moves Δχ² toward route E on every all-lens line, so nothing here brings back a law preference. It does not make route E a good fit either: its p on S3 falls from 0.89 to 0.01–0.02. Whether to restate G8 from these runs is the owner's call, and I have not edited SI1's or SI2's files.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. The theory stays open. Nothing here says the data favour the framework.

## Weight ratios, K_H3-style (source weight per centre, mean over the range's bins)
| sample | range | lens/I, old rule | lens/I, new rule | new rule, k20 | lens/R |
|---|---|---|---|---|---|
| S3 | in | 1.262 | 1.180 | 1.180 | 1.096 |
| S3 | O1 | 1.123 | 1.064 | 1.062 | 0.981 |
| S3 | **O2** | **1.058** | **1.009** | 1.007 | 0.936 |
| S1 | in | 1.203 | 1.183 | 1.177 | 1.188 |
| S1 | O1 | 1.091 | 1.073 | 1.068 | 1.075 |
| S1 | **O2** | **1.033** | **1.015** | 1.014 | 1.020 |

The old rule passes SI3's 0.10 limit in O2 on both samples, across all six catalogues (S3 1.051 to 1.058, S1 1.033 to 1.048). KiDS's was 1.12 to 1.39. The skew exists here but is small: mean z of lens against clones 0.2328 / 0.2405 on S3 and 0.2173 / 0.2206 on S1; mean lg M★ 10.706 / 10.760 and 10.591 / 10.619. Under the new rule they match exactly. The ratio left in the inner bins, 1.18, is no longer a z or mass effect. P2 disclosed two candidates for it, lens-associated sources and iso-randoms falling in masked areas, and neither is corrected.

## Frozen comparison: old against new at the frozen counts
Δχ² = χ²(route E) − χ²(law), 15 bins, 36-patch jackknife, Hartlap. Bold marks a changed class. LAW and ROUTE E are LAW PREFERRED and ROUTE E PREFERRED. Raw L − R lines are in `sc2_classes.out`, and they are identical on both runs by K3.

**Canonical, frozen comparison**

| sample, line | old: χ²(law), p | χ²(route E), p | Δχ² | D | class | new: χ²(law), p | χ²(route E), p | Δχ² | D | class |
|---|---|---|---|---|---|---|---|---|---|---|
| S3 all, R0 | 17.8, 0.28 | 12.6, 0.63 | −5.1 | 2.51 | NOT POWERED | 24.7, 0.05 | 14.5, 0.49 | −10.1 | 2.77 | NOT POWERED |
| S3 blue, R0 | 17.1, 0.31 | 13.7, 0.55 | −3.4 | 0.87 | NOT POWERED | 19.8, 0.18 | 16.5, 0.35 | −3.3 | 0.87 | NOT POWERED |
| S3 red, R0 | 17.8, 0.27 | 13.1, 0.60 | −4.8 | 2.48 | NOT POWERED | 22.8, 0.09 | 15.7, 0.40 | −7.1 | 2.61 | NOT POWERED |
| S3 red, R2 | 19.8, 0.18 | 9.8, 0.83 | −10.0 | 2.78 | NOT POWERED | 23.2, 0.08 | 11.6, 0.71 | −11.6 | 3.00 | NOT POWERED |
| S3 all, R2 | 19.3, 0.20 | 8.7, 0.89 | −10.6 | 2.77 | NOT POWERED | 26.5, 0.03 | 11.7, 0.70 | −14.8 | 3.13 | **ROUTE E** |
| S1 all, R0 | 15.8, 0.40 | 24.4, 0.06 | +8.7 | 4.26 | LAW | 31.9, 0.007 | 22.1, 0.11 | −9.8 | 4.53 | **ROUTE E** |
| S1 blue, R0 | 16.7, 0.34 | 20.8, 0.14 | +4.1 | 2.09 | NOT POWERED | 18.9, 0.22 | 17.5, 0.29 | −1.4 | 1.84 | NOT POWERED |
| S1 red, R0 | 32.5, 0.006 | 48.6, 2e-5 | +16.1 | 4.79 | LAW | 35.0, 0.002 | 27.0, 0.03 | −8.0 | 4.72 | **ROUTE E** |
| S1 red, R2 | 34.2, 0.003 | 32.2, 0.006 | −2.0 | 5.27 | NEITHER | 46.6, 4e-5 | 23.7, 0.07 | −22.9 | 5.35 | **ROUTE E** |
| S1 all, R2 | 22.7, 0.09 | 22.3, 0.10 | −0.3 | 4.63 | NEITHER | 40.6, 4e-4 | 17.8, 0.27 | −22.9 | 5.05 | **ROUTE E** |

**Alt, frozen comparison**

| sample, line | old: χ²(law), p | χ²(route E), p | Δχ² | D | class | new: χ²(law), p | χ²(route E), p | Δχ² | D | class |
|---|---|---|---|---|---|---|---|---|---|---|
| S3 all, R0 | 18.5, 0.24 | 12.6, 0.63 | −5.8 | 2.86 | NOT POWERED | 25.9, 0.04 | 14.5, 0.49 | −11.3 | 3.07 | **ROUTE E** |
| S3 blue, R0 | 17.6, 0.29 | 13.7, 0.55 | −3.9 | 0.99 | NOT POWERED | 20.2, 0.16 | 16.5, 0.35 | −3.7 | 0.98 | NOT POWERED |
| S3 red, R0 | 18.6, 0.23 | 13.1, 0.60 | −5.6 | 2.82 | NOT POWERED | 23.4, 0.08 | 15.7, 0.40 | −7.7 | 2.89 | NOT POWERED |
| S3 red, R2 | 21.9, 0.11 | 9.8, 0.83 | −12.0 | 3.16 | ROUTE E | 24.8, 0.05 | 11.6, 0.71 | −13.2 | 3.32 | ROUTE E |
| S3 all, R2 | 21.3, 0.13 | 8.7, 0.89 | −12.6 | 3.16 | ROUTE E | 28.7, 0.02 | 11.7, 0.70 | −17.0 | 3.47 | ROUTE E |
| S1 all, R0 | 16.9, 0.32 | 24.5, 0.06 | +7.6 | 4.88 | LAW | 35.0, 0.002 | 22.1, 0.10 | −12.9 | 5.11 | **ROUTE E** |
| S1 blue, R0 | 16.4, 0.35 | 20.8, 0.14 | +4.3 | 2.37 | NOT POWERED | 19.1, 0.21 | 17.4, 0.29 | −1.7 | 2.06 | NOT POWERED |
| S1 red, R0 | 31.4, 0.008 | 48.6, 2e-5 | +17.3 | 5.51 | LAW | 38.1, 9e-4 | 27.1, 0.03 | −11.0 | 5.33 | **ROUTE E** |
| S1 red, R2 | 39.0, 6e-4 | 32.2, 0.006 | −6.8 | 6.03 | NEITHER | 54.9, 2e-6 | 23.8, 0.07 | −31.1 | 6.03 | **ROUTE E** |
| S1 all, R2 | 29.0, 0.02 | 22.4, 0.10 | −6.6 | 5.26 | NEITHER | 47.6, 3e-5 | 17.8, 0.27 | −29.7 | 5.70 | **ROUTE E** |

**Reported, k20:** every line is in `sc2_classes.out`. It reads the combined reading as MIXED.

**P2, canonical, S3 at (a) y_e = 0:**

| run | A_in | A_O1 | A_O2 | classes (O1, O2) | S | verdict |
|---|---|---|---|---|---|---|
| old | 1.83 ± 0.30 | 0.57 ± 0.38 | −0.16 ± 0.42 | consistent, between | 0.87 | UNDECIDABLE |
| new | 1.86 ± 0.34 | 0.75 ± 0.40 | −0.26 ± 0.40 | consistent, over | 0.90 | UNDECIDABLE |
| k20 | 1.88 ± 0.30 | 0.68 ± 0.35 | −0.43 ± 0.37 | consistent, over | 0.99 | UNDECIDABLE |

## A1: the rule against catalogue noise (post-result, reported only)
Six catalogues per rule at the frozen counts, counting the frozen ones. Two per rule at 20 per lens. Mean and sd are of Δχ². se = √(sd²/6 + sd²/6). NP, LAW, RE, N are the four classes. The diagonal-only column has no matrix inverse in it. K3 and K4 pass on every catalogue.

**Canonical**

| sample, line | old rule, 6 catalogues: mean ± sd | classes | new rule, 6 catalogues: mean ± sd | classes | rule effect ± se | diagonal-only rule effect ± se | 20 per lens, old rule | 20 per lens, new rule |
|---|---|---|---|---|---|---|---|---|
| S3 all, R0 | −11.2 ± 3.4 | NP 6 | −17.5 ± 12.0 | N 2, NP 4 | −6.3 ± 5.1 | −0.7 ± 1.8 | −20.5, −9.6: RE, NP | −17.4, −12.8: RE, NP |
| S3 blue, R0 | −3.7 ± 1.0 | NP 6 | −3.7 ± 0.9 | NP 6 | −0.1 ± 0.5 | −0.1 ± 0.2 | −4.1, −4.1: NP, NP | −3.7, −4.0: NP, NP |
| S3 red, R0 | −9.4 ± 2.6 | NP 6 | −13.3 ± 10.9 | N 1, NP 5 | −3.9 ± 4.6 | +0.2 ± 1.6 | −19.6, −10.6: NP, NP | −10.1, −11.7: NP, NP |
| S3 red, R2 | −16.1 ± 3.4 | NP 1, RE 5 | −20.3 ± 13.8 | N 2, NP 3, RE 1 | −4.2 ± 5.8 | +0.8 ± 2.0 | −29.3, −17.6: N, RE | −18.1, −19.1: RE, NP |
| S3 all, R2 | −17.8 ± 3.9 | NP 2, RE 4 | −24.8 ± 15.2 | N 3, NP 2, RE 1 | −7.0 ± 6.4 | −0.3 ± 2.2 | −30.0, −16.8: N, RE | −26.3, −20.2: RE, NP |
| S1 all, R0 | −1.6 ± 13.2 | LAW 2, N 1, RE 3 | −5.1 ± 7.7 | LAW 1, N 1, RE 4 | −3.5 ± 6.3 | −0.6 ± 4.6 | +1.6, +1.6: N, N | −0.3, +4.3: N, N |
| S1 blue, R0 | +1.2 ± 2.0 | NP 6 | −0.7 ± 2.5 | NP 6 | −1.9 ± 1.3 | −0.2 ± 0.7 | +0.8, −0.5: NP, NP | +0.6, +1.3: NP, NP |
| S1 red, R0 | −1.7 ± 14.7 | LAW 2, N 2, RE 2 | +0.9 ± 7.6 | LAW 2, N 2, RE 2 | +2.6 ± 6.8 | −0.3 ± 4.4 | +0.1, +3.0: N, N | +9.6, +5.1: LAW, N |
| S1 red, R2 | −20.5 ± 15.2 | N 2, RE 4 | −14.5 ± 9.3 | N 2, RE 4 | +5.9 ± 7.3 | +0.7 ± 5.1 | −16.6, −12.6: N, RE | −6.9, −10.0: N, N |
| S1 all, R2 | −18.0 ± 12.2 | N 1, RE 5 | −19.0 ± 5.0 | RE 6 | −1.0 ± 5.4 | +0.1 ± 5.1 | −18.2, −18.5: RE, RE | −15.8, −16.4: RE, RE |

**Alt**

| sample, line | old rule, 6 catalogues: mean ± sd | classes | new rule, 6 catalogues: mean ± sd | classes | rule effect ± se | diagonal-only rule effect ± se | 20 per lens, old rule | 20 per lens, new rule |
|---|---|---|---|---|---|---|---|---|
| S3 all, R0 | −12.9 ± 3.8 | NP 2, RE 4 | −19.7 ± 13.7 | N 2, NP 2, RE 2 | −6.8 ± 5.8 | −1.0 ± 2.0 | −23.7, −11.1: RE, RE | −20.2, −14.5: RE, NP |
| S3 blue, R0 | −4.2 ± 1.1 | NP 6 | −4.3 ± 1.0 | NP 6 | −0.0 ± 0.6 | −0.1 ± 0.2 | −4.7, −4.7: NP, NP | −4.3, −4.7: NP, NP |
| S3 red, R0 | −10.7 ± 2.9 | NP 1, RE 5 | −15.0 ± 12.4 | N 2, NP 3, RE 1 | −4.3 ± 5.2 | +0.0 ± 1.9 | −22.4, −11.9: RE, NP | −11.8, −13.0: RE, NP |
| S3 red, R2 | −18.8 ± 3.7 | RE 6 | −23.4 ± 15.7 | N 2, NP 1, RE 3 | −4.6 ± 6.6 | +0.6 ± 2.3 | −34.2, −20.3: N, RE | −21.5, −21.8: RE, RE |
| S3 all, R2 | −20.9 ± 4.4 | RE 6 | −28.4 ± 17.3 | N 3, NP 1, RE 2 | −7.5 ± 7.3 | −0.8 ± 2.4 | −35.2, −19.8: N, RE | −30.9, −23.4: RE, RE |
| S1 all, R0 | −4.2 ± 13.9 | LAW 1, N 2, RE 3 | −8.0 ± 8.2 | N 2, RE 4 | −3.8 ± 6.6 | −1.1 ± 5.2 | +0.0, +0.2: N, N | −2.3, +2.3: N, N |
| S1 blue, R0 | +1.3 ± 2.1 | NP 6 | −0.9 ± 2.9 | NP 6 | −2.2 ± 1.5 | −0.3 ± 0.8 | +0.8, −0.7: NP, NP | +0.5, +1.3: NP, NP |
| S1 red, R0 | −4.4 ± 17.4 | LAW 1, N 3, RE 2 | −1.9 ± 7.8 | LAW 1, N 4, RE 1 | +2.5 ± 7.8 | −0.8 ± 4.9 | −2.5, +1.6: N, N | +7.8, +3.0: N, N |
| S1 red, R2 | −28.9 ± 18.1 | N 1, RE 5 | −23.7 ± 9.9 | N 1, RE 5 | +5.2 ± 8.4 | −0.2 ± 5.9 | −25.9, −20.7: RE, RE | −14.8, −18.5: N, N |
| S1 all, R2 | −25.4 ± 13.3 | N 1, RE 5 | −27.0 ± 5.1 | RE 6 | −1.6 ± 5.8 | −0.8 ± 5.8 | −25.9, −26.9: RE, RE | −22.8, −25.5: RE, RE |

**Combined reading tally:** old rule at frozen counts GONE 5, MIXED 1; new rule GONE 4, MIXED 2; 20 per lens MIXED 4 of 4. **P2:** UNDECIDABLE on every catalogue.

**20 per lens, canonical, in detail:**

| run | sample, line | χ²(law), p | χ²(route E), p | Δχ² | D | class | law A_in, A_O1, A_O2 | route E A_in, A_O1 |
|---|---|---|---|---|---|---|---|---|
| old rule, a | S3 all, R0 | 52.2, 5e-6 | 31.7, 0.007 | −20.5 | 3.04 | ROUTE E | 1.93±0.31, 0.46±0.35, −0.45±0.37 | 1.91±0.33, 1.80±1.13 |
| old rule, a | S3 all, R2 | 60.5, 2e-7 | 30.6, 0.01 | −30.0 | 3.49 | NEITHER | 1.47±0.24, 0.38±0.28, −0.38±0.30 | 1.36±0.23, 1.16±0.73 |
| old rule, a | S1 all, R0 | 23.1, 0.08 | 24.8, 0.05 | +1.6 | 5.08 | NEITHER | 1.39±0.14, 0.78±0.18, 0.27±0.17 | 1.47±0.16, 2.61±0.55 |
| old rule, a | S1 all, R2 | 29.5, 0.01 | 11.4, 0.72 | −18.2 | 5.54 | ROUTE E | 1.08±0.11, 0.64±0.14, 0.23±0.15 | 1.05±0.11, 1.70±0.36 |
| old rule, b | S3 all, R0 | 40.5, 4e-4 | 30.9, 0.009 | −9.6 | 2.71 | NOT POWERED | 1.70±0.30, 0.43±0.34, −0.30±0.37 | 1.66±0.32, 1.71±1.10 |
| old rule, b | S3 all, R2 | 45.1, 7e-5 | 28.3, 0.02 | −16.8 | 3.06 | ROUTE E | 1.29±0.23, 0.35±0.28, −0.25±0.31 | 1.19±0.22, 1.09±0.71 |
| old rule, b | S1 all, R0 | 25.2, 0.05 | 26.8, 0.03 | +1.6 | 4.68 | NEITHER | 1.41±0.14, 0.69±0.19, 0.25±0.19 | 1.51±0.17, 2.34±0.59 |
| old rule, b | S1 all, R2 | 32.4, 0.006 | 13.9, 0.53 | −18.5 | 5.02 | ROUTE E | 1.10±0.11, 0.57±0.15, 0.21±0.16 | 1.08±0.12, 1.52±0.38 |
| new rule, a | S3 all, R0 | 47.3, 3e-5 | 29.9, 0.01 | −17.4 | 3.12 | ROUTE E | 1.88±0.30, 0.68±0.35, −0.43±0.37 | 1.89±0.31, 2.50±1.10 |
| new rule, a | S3 all, R2 | 54.7, 2e-6 | 28.4, 0.02 | −26.3 | 3.58 | ROUTE E | 1.43±0.23, 0.55±0.28, −0.36±0.30 | 1.34±0.22, 1.61±0.71 |
| new rule, a | S1 all, R0 | 20.0, 0.17 | 19.7, 0.18 | −0.3 | 4.95 | NEITHER | 1.35±0.15, 0.76±0.17, 0.28±0.18 | 1.48±0.17, 2.50±0.53 |
| new rule, a | S1 all, R2 | 26.8, 0.03 | 11.0, 0.75 | −15.8 | 5.49 | ROUTE E | 1.06±0.11, 0.62±0.14, 0.24±0.15 | 1.05±0.12, 1.63±0.35 |
| new rule, b | S3 all, R0 | 44.9, 8e-5 | 32.1, 0.006 | −12.8 | 2.59 | NOT POWERED | 1.88±0.29, 0.60±0.35, −0.38±0.39 | 1.89±0.31, 2.15±1.11 |
| new rule, b | S3 all, R2 | 49.5, 1e-5 | 29.3, 0.01 | −20.2 | 2.96 | NOT POWERED | 1.43±0.22, 0.49±0.29, −0.31±0.32 | 1.34±0.21, 1.38±0.72 |
| new rule, b | S1 all, R0 | 20.5, 0.15 | 24.8, 0.05 | +4.3 | 4.98 | NEITHER | 1.37±0.14, 0.79±0.18, 0.28±0.19 | 1.48±0.17, 2.58±0.55 |
| new rule, b | S1 all, R2 | 29.3, 0.01 | 12.8, 0.62 | −16.4 | 5.31 | ROUTE E | 1.07±0.11, 0.65±0.15, 0.23±0.16 | 1.05±0.12, 1.69±0.36 |

## Why one catalogue isn't enough here
- **S1's I has 2 clones per lens,** so I is a third of the variance. I expected about 1.15 D of noise in Δχ² from that, about 5.
- **The real scatter is larger.** The half-split estimate with the covariance fixed gives 5 to 6 on S1, and the six old-rule catalogues show sd 12 to 15. Each catalogue also changes the jackknife covariance, and a 15 × 15 inverse from 36 patches is itself noisy, so χ² moves as well as the data vector. S3's route E χ² at R2 runs 8.7 to 28.6 across old-rule catalogues and 8.9 to 52.8 across new-rule ones.
- **New-rule S3 has the widest scatter at the frozen counts,** sd 11 to 15 against 3 to 4 for the old rule. My reading, not tested: the old rule rarely keeps low-acceptance lenses and the new rule must place them, and if those are few and heavy in the weights, 4 clones each is too few. At 20 per lens the two new-rule values differ by about 6.

## Checks
| check | result |
|---|---|
| K1: old rule reproduces SI2's lines and combined reading, SI1's all, inner, outer and classes, P2's verdicts, profile, amplitudes and weight lines | PASS, \|d\| 0 |
| K2: every lens has exactly its count, clone z and lg M★ equal its lens's, edge margin, brute veto on 200 per sample | PASS, new and k20. No lens short |
| K3: lens and R per-centre sums, raw L − R lines, unchanged | PASS, \|d\| 0 |
| K4: cross-shear of Δ and half A − half B of I, p ≥ 0.001 | PASS. Lowest 0.0030, S3 cross on the new run |
| K5: new rule's lens/I in O2 within 0.10 of 1 | PASS, 1.009 and 1.015 |
| MUTATE: clones from the top half of z, canonical | Bites. K2 and K5 fail (lens/I O2 1.41, 1.46), χ²(route E) changes on every all-lens line, prints NO READING, exits 1 |

## Disclosures
- **A wrong count in my own text.** Commit eda8433972's message and the first version of `AMENDMENT_A1.md` said 10 of 40 classes. There are 2 footings, 2 samples and 5 lines, so 20. The amendment file is corrected. The commit message stands as written.
- **A1 is post-result.** I added it after seeing the frozen flips, because one catalogue per rule can't separate the rule from noise. Its seeds were fixed before its numbers.
- **The T² line** is a reported reference, added after A1's table. The frozen classes and the combined reading use χ²(15), as SI1 froze them.

## What this cannot show
- Per-lens clones match z and mass only. They do not match the lens's footprint or colour. SI2's red and blue lines keep the sample's full I, as it disclosed.
- Faint neighbours are in neither model. UN1 works on that. R2 stays an open choice.
- SI1's reported variants, SI2's sensitivity tables and AS1, which runs SI2's text, are not regraded. Their I is still one old-rule catalogue, and their single-seed numbers should be read with the scatter above in mind.
- Six catalogues and two at low noise give rough spreads. Nothing is tuned, but a rule effect of a few units in Δχ² can't be excluded at this precision.
- Absolute p-values are limited by the 36-patch covariance at any catalogue size.
- A preference compares two members of this record only.

## Compute
One thread, `nice -n 15`, at most two processes at once. About 46 minutes of CPU in all (phase A 1,470 s; grades 1,305 s), against a limit of about 90. Peak RSS 1.45 GB at the frozen counts and 2.15 GB at 20 per lens. Run order: `sc2_run.py grade old`, `sc2_run.py measure` and `grade` for new, k20, mutate, `sc2_table.py`; then `sc2_a1.py measure` and `grade` for each A1 catalogue, `sc2_a1_table.py`. Scratch work files are rebuilt from fixed seeds.
