# CFG534: does the settled cold energy depend on assembly history at fixed stellar mass? FOOTING-DEPENDENT as frozen: canonical NOT DIAGNOSTIC / alt H NOT SUPPORTED (KiDS matched early−late +0.53 / +0.49 at 1.6σ). SPARC alone shows the H pattern

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (aa8dc312e).
- **Scripts:**
  - `cfg534_kids.py`: Test 1, plus the KiDS part of Test 4. It execs CFG531's `cfg531_kids.py` read-only, which in turn execs CFG529. It runs in about 5 s, using the CFG531 law-table cache.
  - `cfg534_sparc_sluggs.py`: Tests 2 and 3, plus the SPARC/SLUGGS part of Test 4. It runs in about 3 min (permutations).
  - `cfg534_verdict.py`: applies the frozen ladder to the JSONs.
  - MUTATE runs use `CFG534_MUTATE=1` and write to `*_MUTATE.*`.
- **Settings:**
  - κ = ½ is FITTED. The footings 9.3603e-11 and 1.1312e-10 are never pooled. The kernel is ν_mono.
  - The cold energy's mass is still required. Nothing was downloaded. This is not "theory closed".
- **Numbers** come from `cfg534_*_results*.json`. Pairs are canonical / alt.

## Hypothesis H
Old, early-type, merger-built or central systems carry settled cold energy beyond the law's phantom. Young, gas-rich systems sit on the law. H was tested only as a sign prediction at fixed mass. No amplitude was fitted.

## Test 1: KiDS f30 lenses, matched inside (M_gal, z) group × radial-bin cells
In the f30 sample a group is a fixed (M\*, z) cell: the within-group spread is 0.003 dex, and M_gal − M\* does not depend on type. Late (or NUV-detected) lens weights are scaled to the early class's weight in each cell. The two classes then share identical model stacks (K2: 3e-15), and Δε is fitted on Δd with a jackknife covariance.

**Matched early − late** (constructions A and B agree to 0.003):

| | Δε(K9) | Z | ε early | ε late |
|---|---|---|---|---|
| canonical | **+0.529 ± 0.324** | **+1.63** | +0.848 | +0.221 |
| alt | +0.485 ± 0.296 | +1.64 | +0.691 | +0.116 |

- **Unmatched** (CFG531 (c), reproduced exactly, K1): early +0.832 / +0.676 against late −0.313 / −0.373.
  - Matching moves late from −0.31 to +0.22. So about half of CFG531's +1.15 split is the mass distribution.
  - The point estimate that remains is still positive, but at 1.6σ.
- **By band** (canonical): K-in +0.20 ± 0.64, K-mid +0.70 ± 0.57, K-out +1.15 ± 0.78.
- **By tertile** (1c): T1 +1.17 ± 0.78, T2 +0.79 ± 0.52, T3 +0.23 ± 0.46. All Z are 0.5–1.5.
- **Matched late ε** is +0.76σ / +0.44σ from 0, so the late types sit on the law (the qualifier holds).
- **Amplitude reading:** the matched split corresponds to a uniform M\* shift of **+0.39 dex** in the early class. That is above CFG531's allowed ≤ 0.15–0.20.

**1b, NUV-undetected − NUV-detected** (covered lenses, matched):
- All: +0.242 ± 0.269 (Z +0.90) / +0.222 ± 0.246 (Z +0.90). The sign is the same as H predicts, but it is not significant.
- Inside the late types: −0.05 ± 0.34. Inside the early types: +0.04 ± 0.57. Both are null.
- At fixed type, UV status carries nothing. Any UV signal comes through the type mix.

## Test 2: SLUGGS, 17 ETGs (small N; consistent/inconsistent only)
Partial Spearman ρ(offset, proxy | log M\*). The p values come from permuting the proxy within mass tertiles. Footings agree.

| proxy | ρ | permutation-null mean | reading |
|---|---|---|---|
| environment (F/G/C) | −0.28 | +0.21 | INCONSISTENT (p− 0.007): non-central Virgo members (4459, 4473, 4526) have low offsets |
| central | +0.70 | +0.70 | untestable: the 5 centrals are exactly the 5 most massive galaxies |
| E morphology | +0.26 | +0.12 | consistent (p+ 0.32) |
| log L_X/L_B | +0.54 | +0.51 | consistent (p+ 0.42) |
| composite H-score | +0.41 | +0.45 | consistent (p+ 0.59) |

**MU4 FAILS (kept):** with the proxies shuffled inside the mass blocks, the mean composite ρ is +0.45 / +0.45, against the required |mean| < 0.1.
- The observed partial correlations sit at what the mass structure alone produces. At N = 17 the history proxies are collinear with mass.
- So SLUGGS is not informative at fixed M\*. This also applies to the recorded L_X partial ρ +0.47 (cold_mass cm05b). Under a mass-blocked null it is at the null mean (+0.51 here).
- The frozen rule's "composite ρ > 0" is met formally, but it carries no information.

## Test 3: SPARC, 153 discs (Q ≤ 2, Inc ≥ 30)
Early (T ≤ 3) minus late, matched in log M_b bins. Υ is 0.5 / 0.7, and the residuals are log g_obs/g_law.

| | canonical | alt |
|---|---|---|
| **Δ_out (R ≥ 3 R_d)** | **+0.071 ± 0.026 dex (Z +2.75)** | +0.072 ± 0.026 (Z +2.76) |
| Δ_in (R ≤ 1.5 R_d) | −0.037 ± 0.041 (Z −0.91) | −0.027 (Z −0.66) |
| Δ_out − Δ_in | **+0.104 ± 0.033 (Z +3.13)** | +0.098 (Z +3.00) |
| partial ρ(Δ_out, T \| M_b) | −0.32 | −0.33 |
| partial ρ(Δ_out, f_gas \| M_b) | −0.17 | −0.19 |

- **Same sign as H.** At fixed baryonic mass, early-type, gas-poor discs lie above the law in their outer parts.
- **Mass range.** Only 3 bins (log M_b 10.2–11.4) hold both classes: 23 early and 26 late galaxies.
- **MU3 PASS:** with T shuffled within the mass bins, the mean Z is +0.13 / +0.00.

**Post-freeze robustness** (dated 2026-10-09, no verdict weight; `sparc_postfreeze` in the JSON):
- **Δ_out stays positive in every variant**, at Z +1.7 to +3.7. The variants were:
  - Υ 0.4/0.6 and 0.6/0.8;
  - T ≤ 2 and T ≤ 4;
  - outer edges at 2 or 4 R_d;
  - inc ≤ 80;
  - mass bins shifted by 0.2 dex.
- **Leave-one-galaxy-out:** Z ranges from +2.41 to +3.64. The lowest value comes from dropping NGC 7814.
- **Δ_out − Δ_in is less robust:** Z +0.8 to +3.7.
  - It drops to 1.0–1.7σ with an inner edge of R ≤ 1 R_d.
  - It is 1.5–2.3σ with T ≤ 2, and 0.8–1.0σ when T ≤ 2 is combined with R ≤ 1 R_d.
  - Several early types are edge-on (NGC 891, 4013, 4157, 4217), but the inc ≤ 80 cut keeps +0.10 (Z 3.7 / 3.6).
- **The edge-on worry, checked:** the negative Δ_in is not an edge-on artefact. With inc ≤ 80, Δ_in is +0.04 (Z +0.9).

## Test 4: H or a stellar M/L that rises with age and mass?
**The discriminant.** An M/L error is largest where stars dominate. Extra settled cold energy is near zero there and grows outward.

- **KiDS:** declared non-discriminating before the run. All bands are in deep MOND, where an M/L shift and an isothermal extra component both scale like the law. For reference, the M/L template for +0.1 dex is ε 0.14 / 0.15 / 0.11 in K-in / K-mid / K-out, which is flat.
- **SPARC:** early − late Δ_in is −0.04 (no inner excess). Δ_out − Δ_in is +0.10 at 3.1σ / 3.0σ.
  - The pattern is extra mass at large radius, not a heavier stellar population.
  - A uniformly heavier early-type M/L would put the signal inside, and it is not there.
- **SLUGGS** (16 galaxies, population masses):
  - ρ(D_in, H \| M\*) is +0.35 (p+ 0.051 / 0.037).
  - ρ(D_out − D_in, H \| M\*) is +0.31 (p+ 0.88).
  - The block null is not centred at 0 (MU4), so neither reading is informative.
- **Frozen radial reading: EXTRA MASS on both footings**, carried by SPARC.

## Verdict (frozen ladder, `cfg534_verdict.out`)
- **canonical: NOT DIAGNOSTIC.** The matched 1a σ is 0.324, above the frozen 0.30 power floor.
- **alt: H NOT SUPPORTED.** σ is 0.296, and 1a Z is +1.64 < 2.
- **Headline: FOOTING-DEPENDENT.** The two labels differ only by the power floor. The same fact underlies both: the frozen KiDS test lacks the power to see the predicted split once mass is matched.

**What the record now holds** (written after the results; no verdict weight):
1. **KiDS.** Once mass is controlled exactly, the early − late excess is +0.5 ± 0.3: positive, but not significant.
   - The frozen matching up-weights the few late lenses in high-mass cells, which costs power.
   - A post-freeze overlap-weighted estimator (W_A W_B/(W_A + W_B) per cell, the minimum-variance choice for a constant within-cell difference) gives **+0.78 ± 0.24 / +0.71 ± 0.22 (Z +3.18)**. Its within-group shuffle gives Z +0.53 (it does kill the signal).
   - That is a hint written after the freeze. It is not a pass, and it needs its own frozen lane.
   - The same estimator gives NUV +0.26 ± 0.23 (1.1σ).
2. **SPARC.** Independently, it shows H's sign and H's radial pattern: early-type discs are above the law outside, not inside, at fixed M_b. This is 2.75σ in the outer residual and 3σ in outer − inner, and the outer residual survives every variant tried.
   - It is the first on-disk evidence in this programme that separates "extra mass at large radius" from "heavier stars".
   - It rests on 23 early-type discs in a 1.2 dex mass range.
3. **SLUGGS.** It cannot test history at fixed mass with 17 galaxies, because the proxies are collinear with mass (MU4). The cm05 L_X partial correlation should not be cited as history-beyond-mass evidence.
4. **Late types.** Once matched, they sit on the law (ε ≈ +0.1 to +0.2 ± 0.27). CFG531's negative late ε was the mass mix.

## Controls and MUTATE
- **Controls:**
  - K1: CFG531 (c) is reproduced exactly (0.0).
  - K2: the matched model stacks are identical (3e-15).
  - K3: SPARC rms 0.1117 / 0.1005 matches CFG533.
  - K4: SLUGGS N is 17, with 16 having L_X.
- **MU1 PASS:** with labels shuffled inside the groups, the matched Z is +0.46 (type) and +0.35 (NUV) in all cells.
- **MU2 PASS:** an injected Δε of 0.3 is recovered to 1e-16.
- **MU3 PASS:** the SPARC shuffled mean Z is +0.13 / +0.00.
- **MU4 FAIL** (kept): the SLUGGS block-permutation null mean is +0.45, not ≈ 0. The SLUGGS arm is uninformative at fixed M\*.

## Dated disclosures (2026-10-09)
1. **MU2 covariance.** The first MUTATE run used the mock's own LOO vectors, which made the covariance singular. MU2 now keeps the real jackknife scatter of Δd. The criterion is unchanged.
2. **Post-freeze overlap-weighted KiDS estimator** (and its shuffle). It was added after the first run, once the frozen σ was seen to be inflated by the up-weighted late lenses. It carries no weight.
3. **Post-freeze SPARC robustness block** (Υ, class cut, region edges, inclination, bin phase, leave-one-out, per-bin listing). It was added after the first run and carries no weight.
4. **Test 4 SLUGGS** used the audit's 16-galaxy population-mass set (CFG55_16; NGC 821 excluded as in the audit).
5. **The permutation design for SLUGGS** (mass tertile blocks) turned out to give a non-zero null mean. This is reported via MU4 and not repaired.
6. **No frozen text was edited.**

## What would decide it
- **KiDS:** a frozen re-run with the overlap-weighted estimator, or more lensing area (KiDS-Legacy / DR5, a large fetch), to push the matched type split beyond 3σ under a pre-registered estimator. Nothing small on disk does this.
- **SPARC:** a disc sample with more early-type spirals over a wider mass range, plus a test against stellar-population M/L gradients. Candidates on disk: Di Teodoro+23 massive spirals and the RC100 table (an untested next step).
- **Ages:** no per-galaxy age table is on disk. McDermid+15 ATLAS3D stellar-population ages (VizieR J/MNRAS/448/3484, about 0.1 MB) would add an age proxy for the SLUGGS/ATLAS3D overlap. It would not fix the collinearity at N ≈ 17, so it is not decisive. Nothing was fetched.

## Run
```
nice -n 10 python3 cfg534_kids.py ; CFG534_MUTATE=1 nice -n 10 python3 cfg534_kids.py
nice -n 10 python3 cfg534_sparc_sluggs.py ; CFG534_MUTATE=1 nice -n 10 python3 cfg534_sparc_sluggs.py
python3 cfg534_verdict.py
```

κ = ½ is fitted. The cold energy's mass is still required. This is not "theory closed".
