# CFG924: CFG652 re-run with CFG922 A1's total-flux census. CFG652 VERDICT MOVES: BOTH EXCLUDED → NOT DIAGNOSTIC (FRAGILE: gas extent) (AM1 jitter: not noise-sensitive); ±0.2 dex bracket EXCEEDED (HIGH)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone in 4f4def674 before any script was written and before any A1 mass of any
  eFEDS group was computed. Block CFG920–929 (LEDGER row 663).
- **Amendment:** `AMENDMENT_AM1.md` (5e87b8c41), POST HOC. It was written after the frozen M-INJ end-to-end leg failed and before
  the main run. It adds the M-INJb wiring control and a model-noise ensemble (JITTER). Frozen rules and verdict logic are
  unchanged.
- **Label:** DATA RE-CHECK of CFG652 (criteria 11c7906ef, result ef182618d), following CFG922's side finding. CFG652's condensed
  masses came from GAaP aperture LePhare masses, with masked galaxies dropped. No new posit, no new model.
- **Settings:** κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 are kept apart. CFG652's own models (a) Theory v2
  (condensed-source phantom + CFG637 reservoir) and (b) candidate B (all-baryon phantom), unchanged. Raw KiDS-1000 lensing,
  framework-native models only. The extra mass is cold energy, not a particle. Not "theory closed".

## Answer
Under the frozen rule, **CFG652's verdict moves: BOTH EXCLUDED → NOT DIAGNOSTIC (FRAGILE: gas extent)**, on both footings.

**What moved.** 6 of 10 cells move: all three M_cond cells (x1, ±0.2 dex) on both footings. In each, model (a)'s χ²_a falls
just below the p = 0.01 line: 18.3–19.1 against 20.09, p 0.014–0.019. Model (a) is still a poor fit, but it is no longer
excluded. Model (b) stays excluded on canonical (p 0.001–0.004) and is borderline on alt (p 0.004–0.016). With Δχ² of only
+2 to +8 the rule cannot separate the two models. The gas-extent cells (1 R_X, 4 R_X) stay BOTH EXCLUDED, hence FRAGILE. The
uncapped A1u bracket also reads NOT DIAGNOSTIC on both footings.

**What drives the move: the sample, not the masses.**
- The 8 groups that newly get M_cond > 0 (131 → 139) have weaker lensing, so the measured band drops: 783 kpc 43.5 → 38.9,
  533 kpc 70.9 → 66.2, 248 kpc 133 → 125 M☉/pc². The covariance changes with it.
- On CFG652's own 131 groups with the A1c masses (SAME, no verdict weight) the label stays BOTH EXCLUDED on both footings:
  χ²_a 23.8 / 24.0, χ²_b 27.0 / 23.4.
- The ×1.68 condensed mass itself barely moves model (a)'s stacked prediction: outer A_out(a) +0.159 → +0.154. It does lift
  (b) a little: A_out(b) +0.426 → +0.386 canonical, +0.387 → +0.346 alt. (b) still falls short by ×2.2–2.4 in the band.

**Model noise does not explain the move (AM1).** CFG652's model (a) is chaotic in its inputs, so each χ²_a is one draw:
- the jitter sd of χ²_a is 0.28–0.55;
- across four jittered realizations each, F stays BOTH EXCLUDED and A1c stays NOT DIAGNOSTIC (0/16 label changes);
- every frozen cell move has |Δχ²_a| = 2.5–4.6, against 2 × sd = 0.71 / 1.09.

So the label is **not NOISE-SENSITIVE**, and no move is WITHIN MODEL NOISE. The canonical margin is thin, though: A1c χ²_a spans
18.6–19.8 against the 20.09 line.

The bracket question has a clear answer from the census alone. With CFG922 A1's correction, CFG652's condensed masses rise by a
**median +0.226 dex (×1.68; 16–84%: +0.15 / +0.44)** per group, and 60% of groups shift by more than 0.2 dex. So CFG652's
declared M_cond ± 0.2 dex bracket did not cover the aperture bias: **BRACKET EXCEEDED (HIGH)**, though only just at the median.
The uncapped upper end (A1u) is almost the same (+0.228 dex), so the 1 mag cap matters only in the tail.

## Census (`cfg924_census.json`)

| quantity | F (CFG652 frozen) | A1c (central, primary) | A1u (uncapped bracket) |
|---|---|---|---|
| groups with M_cond > 0 (of 148) | 131 | 139 (8 enter, 0 leave) | 138 |
| median M_cond over those groups | 2.09e11 M☉ | 4.46e11 M☉ | 4.50e11 M☉ |
| groups with a bright central (M_bcg > 0) | 82 | 98 | 98 |
| Δlog10 M_cond vs F (same groups): median (16–84%) | — | +0.226 (+0.150 / +0.438) | +0.228 (+0.151 / +0.483) |
| fraction with Δ > 0.2 / Δ < 0 | — | 0.60 / 0.05 | 0.61 / 0.05 |
| footprint: not measured / partial | — | 3 / 7 | 3 / 7 |

- Before the footprint step, the A1c shift is already +0.224 dex. The footprint step barely matters; the shift comes from the
  flux rescaling.
- **Masked galaxies:** 5% of groups fall (Δ < 0), because kept masked galaxies raise the 3–6 R_X background.
- **The 8 entering groups:**
  - 7 are measured (coverage 1.1–2.7). Under F each had net ≤ 0 and no galaxy inside 0.2 R_X. Under A1c, kept masked galaxies,
    or a net that turns positive under per-galaxy rescaling, give them mass (5 of the 7 now have a central).
  - 1 has coverage 0.0, a footprint hole. It is assigned the median M_cond/M_hot ratio, 0.068.
- One group is positive under A1c but zero under A1u (index 145). The uncapped rescaling also raises bright background-annulus
  galaxies, so its net drops to ≤ 0, and it has no central.
- **A1 identity:** CFG922's `load_bright(A1)` MASS_MED equals the A1 correction line applied to the unamended column (max abs
  0.0 dex). The sample fluxscale is median −0.457 mag (16–84%: −0.669 / −0.298), identical to CFG922.

## Verdict cells (A1c vs CFG652 stored; `cfg924.out`)

| footing | variant | χ²_a (8 dof) | p_a (A1c) | χ²_b | p_b (A1c) | Δχ²(b−a) | A_out (a) | A_out (b) | label | cell |
|---|---|---|---|---|---|---|---|---|---|---|
| can | x1 | 22.9 → 18.8 | 0.016 | 28.7 → 24.5 | 0.0019 | +5.8 → +5.8 | +0.159 → +0.154 ± 0.077 | +0.426 → +0.386 ± 0.063 | BOTH EXCLUDED → NOT DIAGNOSTIC | MOVES |
| can | +0.2 dex | 23.7 → 19.1 | 0.014 | 27.4 → 22.3 | 0.0043 | +3.8 → +3.3 | +0.174 → +0.178 | +0.415 → +0.368 | BOTH EXCLUDED → NOT DIAGNOSTIC | MOVES |
| can | −0.2 dex | 21.6 → 18.3 | 0.019 | 29.7 → 26.2 | 0.0010 | +8.1 → +7.9 | +0.151 → +0.137 | +0.432 → +0.398 | BOTH EXCLUDED → NOT DIAGNOSTIC | MOVES |
| can | gas 1 R_X | 36.2 → 33.6 | 5e-5 | 27.8 → 23.1 | 0.0033 | −8.4 → −10.6 | +0.463 → +0.480 | +0.410 → +0.368 | BOTH EXCLUDED | HOLDS |
| can | gas 4 R_X | 49.2 → 60.3 | 4e-10 | 30.1 → 25.8 | 0.0012 | −19.1 → −34.5 | −0.083 → −0.109 | +0.438 → +0.397 | BOTH EXCLUDED | HOLDS |
| alt | x1 | 22.3 → 18.9 | 0.015 | 25.2 → 20.9 | 0.0073 | +2.8 → +2.0 | +0.167 → +0.167 ± 0.079 | +0.387 → +0.346 ± 0.063 | BOTH EXCLUDED → NOT DIAGNOSTIC | MOVES |
| alt | +0.2 dex | 23.4 → 19.0 | 0.015 | 23.8 → 18.8 | 0.016 | +0.4 → −0.2 | +0.186 → +0.197 | +0.375 → +0.329 | BOTH EXCLUDED → NOT DIAGNOSTIC | MOVES |
| alt | −0.2 dex | 21.5 → 19.0 | 0.015 | 26.1 → 22.6 | 0.0039 | +4.6 → +3.6 | +0.154 → +0.146 | +0.393 → +0.359 | BOTH EXCLUDED → NOT DIAGNOSTIC | MOVES |
| alt | gas 1 R_X | 37.1 → 34.6 | 3e-5 | 25.0 → 20.1 | 0.0099 | −12.1 → −14.5 | +0.482 → +0.496 | +0.375 → +0.333 | BOTH EXCLUDED | HOLDS |
| alt | gas 4 R_X | 49.2 → 56.6 | 2e-9 | 26.7 → 22.3 | 0.0043 | −22.5 → −34.2 | −0.083 → −0.106 | +0.399 → +0.359 | BOTH EXCLUDED | HOLDS |

N = 131 (CFG652) → 139 (A1c). K1 cross-shear on the A1c sample: χ² 1.3/8, p 0.995 (PASS).

- **A1u x1 (bracket; FRAGILE not evaluated):** χ²_a 18.3 / 18.2, χ²_b 24.0 / 20.5 → NOT DIAGNOSTIC on both footings (N 138).
- **Final:** CFG652 stored 'BOTH EXCLUDED' → A1c 'NOT DIAGNOSTIC (FRAGILE: gas extent)'.
- **CFG924 VERDICT (frozen rule): CFG652 VERDICT MOVES.**
- **Reported, no verdict weight:**
  - **SAME** (131 groups, A1c masses): BOTH EXCLUDED on both footings (χ²_a 23.8 / 24.0, χ²_b 27.0 / 23.4).
  - **POSTHOC** cut under A1c (M_bcg > 0 and M_cond ≥ 1e11, N 96): '(a) FAVOURED (FRAGILE: gas extent)', χ²_a 9.4 / 10.0,
    χ²_b 28.8 / 24.9. That is the same reading as CFG652's own POSTHOC, and still post hoc.
  - **Split:** D_obs −0.013 ± 0.138 against (a) +0.22 / +0.25 and (b) +0.04. M2 still does not kill the trend (shuffle median
    −0.25), so the split still does not isolate hot gas.

## Model noise (AM1 JITTER; `cfg924_JITTER.out`)
Model (a) re-run with M_cond × (1 + k·1e-12), k = 1..4; model (b) unjittered; x1 cell; verbatim score.

| sample | footing | χ²_a unjittered | jitter χ²_a (k = 1..4) | mean ± sd | labels |
|---|---|---|---|---|---|
| F (CFG652, N 131) | can | 22.896 | 22.802, 23.225, 22.156, 22.328 | 22.63 ± 0.48 | BOTH EXCLUDED ×4 |
| F | alt | 22.338 | 22.917, 22.282, 22.612, 22.820 | 22.66 ± 0.28 | BOTH EXCLUDED ×4 |
| A1c (N 139) | can | 18.751 | 19.785, 18.621, 19.168, 19.731 | 19.33 ± 0.55 | NOT DIAGNOSTIC ×4 |
| A1c | alt | 18.908 | 18.881, 19.036, 18.478, 19.330 | 18.93 ± 0.36 | NOT DIAGNOSTIC ×4 |

- **NOISE-SENSITIVE: no.**
- **WITHIN MODEL NOISE: none.** Every cell's |Δχ²_a| (2.5–11.0) exceeds 2 × the larger sd: 1.09 canonical, 0.71 alt.
- **Margins:**
  - F sits 2.1–3.1 above the p = 0.01 line in every realization.
  - A1c sits 0.3–1.5 below it on canonical and 0.8–1.6 below on alt.

## Controls
- **K 5/5 PASS, all exact** (`cfg924_K.out`; max rel 0.0 everywhere; peak RSS 0.36 GB):
  - **K1:** CFG922's `census_652` (exec'd) on the unamended bright sample reproduces CFG652's 148 stored M_cond and M_bcg.
  - **K2:** CFG652's verbatim score block on its own stored work files reproduces `cfg652_test_results.json`, `_POSTHOC` and
    `_MUTATE`: every number and label, 0 mismatches.
  - **K3:** `cfg652_model` (sha256 04352d4e…, unchanged) reproduces all 22 stored model arrays for 6 groups spanning the
    M_cond range.
  - **K4a:** CFG922's A1 fluxscale median and 16/84 percentiles are reproduced exactly.
  - **K4b:** CFG922's `Census` under A1 reproduces `cfg922_census_A1.json` net_med, net_sup, sig_sup and coverage for all 318
    eRASS1 clusters.
- **MUTATE:**
  - **M-INJ, as frozen: FAILED** on its end-to-end leg (`cfg924_MUTATE.out`).
    - The census leg is exact: a planted −0.5 mag gives M_cond = 10^0.2 × F to 3.9e-15.
    - The scored χ²_a came out 23.052 / 23.529 against CFG652's stored p02 23.650 / 23.392. χ²_b agreed to 4e-5 / 3e-4. Labels
      agreed.
    - **Mechanism:** CFG652's model (a) is CFG637's Method A, a time-stepped 1D shell infall with shell crossings, and its
      reservoir is placed from each shell's state at t_obs. It is chaotic in its inputs. A 1e-15 relative change in M_cond moves
      per-group ΔΣ_a by up to 62%, mostly in the inner bins; (b) moves in 1–2 groups by ≤ 5%. Identical inputs reproduce bit
      for bit (K3). This is not a CFG924 pipeline fault, but it is a frozen failure and stays recorded as one.
  - **M-INJb (post hoc, AM1): PASS.** The exact CFG652 float plant (stored M_cond × 10**0.2) reproduces the stored p02 per-group
    arrays (max rel 0.0) and the p02 χ² on both footings (23.650177 / 27.416938; 23.391596 / 23.761410) and labels. The
    wiring is exact.
  - **M1 (CFG652's own, on A1c): PASS.** (a) with the hot gas relabelled condensed gives 24.524 / 20.935, identical to (b).

## Post-hoc items and disclosures (dated 2026-10-20)
1. **AM1** was written after the frozen M-INJ failure and before the main run. Its commit (5e87b8c41) landed about one minute
   after the M-INJb run had started (the first `git commit` lacked a `git add`). M-INJb is a pure control, and MAIN started
   after the commit.
2. **CFG652's own χ² carries model noise.** Its stored χ²_a (22.9 / 22.3) is 2.8 / 2.2 above the p = 0.01 line (20.09). The
   p02 cell re-run with 1e-15 input jitter moved χ²_a by −0.60 / +0.14 (from M-INJ). The x1 jitter sd is 0.48 / 0.28 (F) and
   0.55 / 0.36 (A1c). Any lane that re-scores CFG652's or CFG637's model (a) should carry a jitter ensemble.
3. **Footprint coverage** is measured on the bright sample itself (all rows, any z / mask / mass), mirroring CFG922 A1, on
   CFG652's R_X apertures with its 3–6 R_X annulus. Members inflate the aperture count (median coverage 2.1), so only real holes
   fall below 0.5.
4. **A1u's p02 / m02 / g1 / g4 cells** are copies of x1 (declared). A1u is a bracket on the x1 label only.
5. **Implementation:** CFG922 and CFG652 code was exec'd from text slices with hard guards. No stage of theirs can run, and no
   file of theirs is written. The sha256 of 16 CFG652/CFG922 committed outputs and 4 `cfg652_work` npz files is unchanged
   before vs after all runs (20/20 OK). Work files are in
   `_external_data/cfg924_work`. Data and `_external_data` paths resolve through the main checkout when run from a worktree.

## What is and is not established
- **Established, on the record's own data and code:**
  - CFG652's condensed masses were biased low by the aperture photometry: a median ×1.68 per group, beyond its declared
    ±0.2 dex bracket.
  - With CFG922 A1's census, CFG652's frozen rule no longer excludes Theory v2's model (a) (p 0.014–0.019) and cannot separate
    (a) from (b). The verdict moves BOTH EXCLUDED → NOT DIAGNOSTIC (FRAGILE: gas extent), on both footings, at the A1u upper end
    too, and not within model noise.
  - The move comes from the 8 groups A1 adds to the sample, not from the larger masses. On CFG652's own 131 groups the label
    stays BOTH EXCLUDED.
  - Candidate B's all-baryon phantom stays short by ×2.2–2.4 in the 0.25–0.8 Mpc band, and excluded on canonical.
  - CFG652's model (a) (CFG637 Method A) is chaotic in its inputs. Its χ²_a carries model noise with sd 0.3–0.55.
- **Not established:**
  - This is not a pass for (a). χ²_a 18–20 for 8 dof is still a poor fit (p < 0.02). The (a) shortfall of about 40% in the outer
    band (A_out +0.15 to +0.20) and its over-concentrated inner reservoir remain.
  - The label hangs on the sample definition (SAME stays BOTH EXCLUDED), on the gas extent (1 and 4 R_X stay BOTH EXCLUDED),
    and on a thin canonical margin.
  - The A1 rebuild is approximate (CFG922's caveat: −1.6 to −2.9 mag for bright galaxies at z > 0.25). The 1 mag cap matters
    little here (A1u gives the same label).
  - The missing 2-halo term is unchanged.
  - Spectroscopic member masses (GAMA G09 StellarMasses + G3C, CFG652 §5) would replace the photometric census altogether.
- κ is not derived; this is not "theory closed"; nothing here says the data favour the framework.

## Files and re-run (from this directory, one at a time, OMP_NUM_THREADS=1, nice 10)
| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (4f4def674) |
| `AMENDMENT_AM1.md` | post-hoc amendment (5e87b8c41) |
| `cfg924.py` | everything |
| `cfg924_K.out`, `cfg924_K.json` | `CFG924_MODE=K python3 cfg924.py` (about 7 min) |
| `cfg924_MUTATE.out`, `cfg924_results_MUTATE.json` | `CFG924_MODE=MUTATE python3 cfg924.py` (frozen M-INJ, about 35 min) |
| `cfg924_MUTATE_B.out`, `cfg924_results_MUTATE_B.json` | `CFG924_MODE=MUTATE_B python3 cfg924.py` (AM1 M-INJb, about 35 min) |
| `cfg924.out`, `cfg924_results.json`, `cfg924_census.json` | `python3 cfg924.py` (main, about 4 h) |
| `cfg924_JITTER.out`, `cfg924_results_JITTER.json` | `CFG924_MODE=JITTER python3 cfg924.py` (AM1, after main, about 2.4 h) |

- **Read-only inputs:**
  - lane files: CFG652 (`cfg652_test.py` preamble / models / score blocks, `cfg652_model.py`, stored results JSONs), CFG922
    (`cfg922.py` census slices, `cfg922_results_A1.json`, `cfg922_census_A1.json`), CFG686 (distance slice, K4b only), CFG687
    (`cfg687_percluster.npz` positions, K4b only);
  - external: `_external_data/cfg652_work` (inputs, ESD, models), the KiDS DR4 bright sample + LePhare.
- Nothing was downloaded. No other lane was edited. Every run used one core at nice 10. Peak RSS was ≤ 0.39 GB (K 0.36, MUTATE 0.24, MUTATE_B 0.10, MAIN 0.39, JITTER
  0.10), beside the live 1024³ NC2x job.
- **The NC2x job aborted twice while this lane was running** (chain log; abort rule = swap growth):
  - **12:44:** the K run (12:38–12:45, ≤ 0.36 GB) was live. Swap jumped +5.3 GB in one minute while disk_free fell to 8.2 GB.
    The chain7 notes say "low disk + a parallel job". A contribution from this lane cannot be excluded.
  - **15:42:** MAIN (≤ 0.39 GB) was live. The chain7b notes attribute it to a 31 GB Ollama model.
  - NC2x was relaunched at 13:20 and at 16:24.

κ = ½ fitted; footings never pooled; cold energy mass still required; not theory closed.
