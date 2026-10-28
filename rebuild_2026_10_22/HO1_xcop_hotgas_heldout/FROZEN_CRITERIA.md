# HO1_xcop_hotgas_heldout: FROZEN CRITERIA (committed alone, with the assumption ledger, before any script or number)

Written 2026-10-27. **Goal.** Test the frozen combined "CL2 picture" on data that its calibrating lanes did not grade:

- (a) the X-COP individual cluster mass profiles graded by `../CS2_core_law_out_of_sample/` (35 points);
- (b) the hot-gas groups test of `../HG2_kids_lowg_hot_gas/` (KT2017 groups, eRASS1 X-bright vs X-faint).

Passing is evidence. Failing is information. Both are reported as found.

Standing caveats:
- κ = ½ is FITTED.
- Footings: canonical a₀ = 9.3603e-11 m/s² (primary) and alt 1.1312e-10 m/s². They are scored separately and never pooled.
- Route E: Newtonian gravity on baryons plus cold dark energy halos. Cold dark energy is a gravitating w ≈ 0 field
  component, never a particle. ΛCDM appears only as the rival.
- Not "theory closed". Nothing here says the data favour the framework or ΛCDM.
- No downloads. Every input is already on disk.

## 0. The CL2 picture (frozen, implemented exactly; nothing is refit)

| element | frozen definition | source |
|---|---|---|
| switch | a system carries a route-E cold dark energy halo iff it is a satellite OR M200 > 10^12.3 M☉ | CL1 / CL2, T = 12.3 |
| M200, galaxies and groups | log M200 = a + b (log M_b − 10), EM1 row R1 of `A_c2b_refit` | `EM1_emergent_dust_law/em1_emergent_results.json` |
| M, clusters | M = M_b,t + M_fair (GS1 budget, below) | GS1 / CL1 |
| below the switch | the galaxy law on baryons only: g = g_N ν(g_N/a₀), ν(y) = ½ + √(¼ + 1/y), no halo | CL2's `LF_G` / `LF_M` |
| above the switch | route E: Newtonian baryons + halo, no law boost | CL2's `LF_G` / `LF_M` |
| core surface density | Σ = max(a₀/(2πG), η(M) Σ_coll(M)), η = (4/(3 B(1))) c_f(M)^{5/4}, B(1) = 3 ln 2 − π/2 | X43 |
| Σ_coll | X43's Lacey–Cole half-mass collapse surface density on the CLASS `A_c2b_refit` background | X43 `sigma_coll` |
| c_f(M) | 4 × c_nat(M)/c_nat(10^14), c_nat = 11.63 / 8.22 / 7.31 at log M 12 / 13 / 14 (X48 nine-seed, `x48_analyze_results_ng48_A2.json` `cf_by_mass`), linear in log M, clamped outside | CL2 shape S9, L = 4 |
| halo profile | Burkert at that Σ, compact-root convention; saturated at the peak if infeasible (counted) | X43 `solve_r0` |
| group halo normalisation | the whole M200 inside R200 (200 ρ_c, EM1 background h), as X43's `group_logsig` | X43 |
| cluster halo normalisation | GS1: M_fair = (Ω_c/Ω_b) M_b,t with Ω_c/Ω_b = 5.2715 (h 0.6856427, Ω_m 0.2976016, ω_b 0.0223081); M_b,t = 1.2 × the gas counted to the self-consistent turnaround radius r_ta, gas = X30's β-model (r_c = 0.15 R500, β = 2/3) normalised to M_gas,500, with density slope s = 2.777 beyond R500 (GS1's X-COP measurement); halo truncated at r_ta | GS1 `_gc2_ext` as carried by CL2's `budget_edit` |

**Implementation rule.** The picture is not re-coded. The harness executes CL2's own source
(`../CL2_native_cf_slope/cl2_native_slope.py`, up to its K0 block) read-only. It then runs CL2's X43 copy at exactly CL2's tag
`shpS9_L4_T12.3_B` in this lane's directory. The X-COP and HG2 graders call that namespace's functions: `sig_core`,
`solve_r0`, `B`, `sigma_coll`, `BGS`, `A0`, the X30 namespace's `_gc2_ext` and `r_ta_com` with CL2's native edits, and CL2's
`LF_G` for the switch.

Only two pieces are new code:
- the X-COP and group geometry (radii, masses, units);
- the grade statistics, which are CS2's and HG2's own.

## 1. Step 0: stop rule (before any graded number)

Each part must hold on the normal run. If any fails, the run prints STOPPED AT STEP 0, writes no grade and exits 1.

| id | what must be reproduced | tolerance |
|---|---|---|
| S0-CL2 | CL2's committed-on-disk `x62_x43copy_on_shpS9_L4_T12.3_B_results.json`, re-run here: per footing, SPARC rms (both backgrounds), groups mean and Z, and all 15 cluster-key predictions for both h | 1e-9 absolute |
| S0-CS2 | CS2's X-COP grader, executed from CS2's source, reproduces CS2's committed `cs2_out_of_sample_results.json` X-COP mean Δ, rms Δ, n and saturated count. This holds (i) for the CS2 law (A, q from that JSON, pivot 70.50) and (ii) for the OS1 comparator per footing (log Σ_a₀, q_f 0.892 / 0.748, pivot = GR1's `sigma_ref`) | 1e-9 absolute |
| S0-HG2 | HG2's committed `hg2_kids_lowg_hot_gas.json` | 1e-9 absolute |

S0-HG2 is run from HG2's own functions in HG2's own call order (one RNG seeded 20261025, power first, then the 2000-draw
bootstrap). It must reproduce:
- K1 A and σ_A;
- 190 groups, 14 BRIGHT, 188 supported;
- D, the 95% interval and power 0.448;
- the per-arm median Δ.

The SHA-256 of every source file and target JSON read in Step 0 is recorded in the output. CL2's script and results are on
disk; at freezing time they are not yet committed by their lane.

## 2. Graded lines

### (a) X-COP: CS2's 35 points, CS2's pass rule

- **Data.** Exactly CS2's rows: the 7 X-COP clusters that have `_mstar.fits`, at x = 0.1, 0.2, 0.3, 0.5 and 0.7 R500
  (35 points). g_obs = G M_HSE(<r)/r² from `M_FORW`. The data baryons are M_b,data(<r) = M_gas(<r) + M★(<r), both read as
  CS2 reads them.
- **Prediction.** All 7 are clusters, so they sit above the switch (checked, K1).
  - The halo comes from the CL2 picture and the GS1 budget built from each cluster's measured M_gas,500 (from `MGAS` at
    R500), R500 and z (FITS header).
  - Predicted g = G (M_b,data(<r) + M_h(<r))/r².
  - **Unlike CS2, no HSE mass enters the prediction.** The halo is normalised by the native fair share, not by the
    measured M_HSE at R500.
- **Statistic (CS2's).** Δ = log₁₀ g_obs − log₁₀ g_pred over the 35 points.
- **Rule (CS2's, verbatim).** **PASS** iff |mean Δ| ≤ 0.05 dex **and** rms Δ ≤ 0.10 dex. Otherwise **FAIL**, labelled OVER
  (mean Δ < 0, the picture predicts too much pull) or UNDER.

### (b) HG2: the picture's prediction of HG2's measured D

- **Sample.** HG2's primary sample exactly: HG1's `build()` at HG1's primary settings, and the 188 groups inside the
  blue-lens reference range.
- **Prediction.** Per group, at HG1's radius r = (4/3) R_h:
  - baryons inside r are HG1's own: M_b(<r) = 0.5 M★ + M_gas(<r), so g_bar is HG1's;
  - for the switch and halo mass, the total baryons are M_b,tot = M★ + M_gas,500, with M_gas,500 the matched eRASS1
    catalogue value (BRIGHT) or 0 (FAINT, HG1's X-FAINT gas = 0);
  - M200 comes from EM1 R1 (A_c2b_refit). Above 10^12.3: g_pred = g_bar + G M_h(<r)/r², with the halo as X43's groups.
    Below: g_pred = g_bar ν(g_bar/a₀).
- **Statistic.** Δ_pred,i = log₁₀ g_pred,i − log₁₀ g_ref(g_bar,i), with HG2's own blue-lens `Ref` interpolation.
  D_pred = HG1's `D_stat` (0.1 dex σ bins, min-weighted median differences, BRIGHT − FAINT) on Δ_pred.
- **Rule.** **PASS** iff D_pred lies inside HG2's measured 95% interval for D, [−0.511, −0.076] (reproduced in S0-HG2).
  Otherwise **FAIL**, labelled ABOVE (the picture predicts too much bright-arm excess) or BELOW.

**Reported only, never graded:**
- **HG2's statistic on the model residual.** Δ_res,i = log g_obs,i − log g_pred,i. D_res comes from `D_stat`, with a
  2000-draw group bootstrap (seed 20261025, groups resampled within arms; no reference draws, since the model has none).
  HG2's classes are applied, including its power rule. Disclosed now: the power rule depends only on the sample, arms and
  bins, so it is expected to be HG2's 0.448 < 0.50, giving UNDERPOWERED. That is why this is not the graded line.
- Per-arm unstratified median Δ_res (the level against the picture).
- The fraction of groups above the switch, per arm.
- The variant M_b,tot = M★ only.
- Per-cluster X-COP mean Δ, and the per-radius mean Δ.
- The CS2 and OS1 X-COP numbers, for comparison.

### Verdicts

| level | rule |
|---|---|
| sub-test, per footing | PASS or FAIL as above |
| lane, per footing | **CL2 PICTURE PASSES BOTH HELD-OUT TESTS** / **CL2 PICTURE FAILS: <sub-tests>** |
| headline | canonical is the primary; alt is reported beside it |

If the footings disagree, the headline says so. There is no pooled verdict.

## 3. Checks (normal run)

- **K1, switch.** Every X-COP cluster is above T. CL2's `LF_G` branch counters show zero violations. Each HG2 group's
  branch equals [M200 > 10^12.3]: the halo branch reproduces g_bar + g_h, and the law branch reproduces g_bar ν(g_bar/a₀),
  to 1e-12 relative.
- **K2, budget.** For each X-COP cluster, the GS1 turnaround fixed point converges (relative step < 1e-6). The resulting
  M_b,t is independent of the starting guess (× 0.3 and × 3) to 1e-5 relative.
- **K3, halo identity.** The Burkert halo mass at r_ta equals M_fair to 1e-8 relative, or the cluster is counted as
  saturated. For each HG2 halo group, the mass at R200 equals M200 to 1e-8, or the group is counted as saturated.
- **K4, c_f table.** c_f at 10^12 / 10^13 / 10^14 equals CL2's printed [6.37, 4.5, 4.0] to 0.01.
- **K5, data identity.** The X-COP rows equal the matched-clumping lane's `targets.csv` g_obs to 1e-6 relative (CS2's K2,
  executed from CS2's source).
- **K6, resources.** Peak RSS < 1 GB per process, one thread.
- **Rerun.** A second normal run gives a byte-identical results JSON. Runtime and RSS are kept out of the JSON.

## 4. MUTATE twin (`HO1_MUTATE=1`, separate `_MUTATE` outputs)

- **m1.** CL2's own MUTATE inside the namespace: the switch flag inverted, and the S9 shape inverted to rising with mass.
- **m2.** The S0-HG2 target D is multiplied by 1.01.

The twin skips the stop rule and reports its (mutated) grades, labelled. It **must fail S0-CL2, K1 and S0-HG2**. It exits 1
when all three fail (the teeth bite) and 0 otherwise. An exit 0 from the twin means the harness cannot see the change, and
that is reported.

## 5. Disclosed before freezing

**Already seen, not computed here:**
- CS2's committed X-COP numbers. The OS1 comparator gives mean Δ −0.075, rms 0.124 (canonical) and −0.035, 0.092 (alt).
  The CS2 law gives −0.151, 0.205.
- Both used the measured M_HSE at R500 to normalise the halo. This lane does not.
- HG2's D = −0.294 [−0.511, −0.076] and its UNDERPOWERED class (power 0.448).

**Not computed or seen before freezing:** no number from this lane, and no X-COP or HG2-group prediction under the CL2
picture.

**Independence is partial:**
- GS1's slope s = 2.777 was measured on X-COP **gas** profiles (11 clusters, including these 7), so the cluster gas budget
  is not independent of X-COP gas. The graded quantity, the HSE total mass, entered no calibration.
- The HG2 groups were not graded by CL1, CL2 or GS1. CL2's group line is the 63 Tian groups (P4 estimator), which is a
  different sample.

**Known risks:**
- The halo budget inside R500 uses X30's β-model, not the measured X-COP gas profile. The graded baryons use the measured
  profile.
- The X-COP radii and masses are used in X-COP's own published cosmology, with no h conversion. This is as CS2 did.
- HG1's 3σ²/r estimator and the eRASS1 group gas masses carry HG2's disclosed limits.
- A BRIGHT group's switch depends on adding M_gas,500 to M_b,tot. That choice is in the ledger, with the M★-only variant
  reported.

Run: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ho1_heldout.py` and the twin, with `HO1_MUTATE=1`.
Amendments, if any, only in `AMENDMENTS.md`, each committed alone before the run it affects.
