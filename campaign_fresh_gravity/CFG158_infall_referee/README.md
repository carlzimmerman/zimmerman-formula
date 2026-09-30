# CFG158 — Referee of CFG118 (Door 6): independent re-derivation of the secondary-infall cumulative-mass headline

- **Criteria:** `CFG158_FROZEN_CRITERIA.md` (committed 240bcd976, sha256 6a0e1c05...), written before any script. The menu of ten doors was written knowing the target. The referee is NOT blind: CFG118's README numbers were read first, so they are targets, not predictions. CFG118's scripts, `.out` and `.json` were opened only after this lane's main and MUTATE runs were saved.
- **What is re-derived:** the CFG118 headline that the cumulative cold mass of spherical secondary infall onto a static baryon core, relative to the CFG44 target, is 1.0–4.2 at x = r/r_M ≈ 1 and 0.28–0.66 at x ≈ 28 (so C_infall/C_target falls with radius), that the radial scale follows the turnaround (M^0.33) rather than r_M (M^0.5), plus the EdS slope and the Hubble-flow control.
- **Standing rules:** κ = ½ and Ω_c h² stay fitted. A scoped no-go is a valid result. Nothing here says the data favour the framework or that the theory is closed. Failed controls and wrong expectations are kept below.

## Bottom line

1. **The headline reproduces with independent code.** All headline lines H-A to H-F pass. Set-up numbers agree with CFG118 to 5e-4 (M_ta/M_b = 23.63, r_ta = 236, 508, 1094, 2358 kpc, x_ta = 193, 132, 90, 61). The cumulative-mass envelopes are R(1.12) = [1.07, 4.65] (README 1.0–4.2) and R(28.2) = [0.280, 0.678] (README 0.28–0.66). The ratio falls with radius in all 24 runs. The radius where M_c = M_b scales as M^0.33–0.34 for point cores (0.22–0.24 for exponential spheres), with the turnaround at M^0.3333 and never near M^0.5.
2. **Three of my own controls fail, and the run exits 1.** C2 (EdS slope −2.410 against the frozen line |slope + 9/4| ≤ 0.15 and against CFG118's −2.238), C3 (5,000 vs 20,000 shells) and C4 (time-step doubling). The first full run also failed C1 (9.7e-2); that was my integrator's early-time interpolation, fixed and re-run (both kept). The noise floor of the cumulative mass at 5,000 shells is about 10% in this integrator, comparable to CFG118's own C3 failure. So the agreement is agreement to about that level, not a 5% statement: 13 of 24 cases agree with CFG118 within 5% at x = 1.12, and 22 of 24 at x = 28.2.
3. **G1 fails in every run** in this set-up, as in CFG118. That is a scoped no-go for door 6 (spherical, static core from z = 100, smooth baryon background, three angular-momentum brackets). Nothing here reaches beyond that set-up.

## Files and the exact re-run command

Run from the lane directory; `julia` must be on PATH (Julia 1.12.6 here); numpy, scipy needed.

```
CFG158_NPROC=12 python3 cfg158_referee.py                                  # main; exit 1 here (C2, C3, C4 fail); writes cfg158_referee.out / _results.json; 53.7 min wall on 12 workers (shared machine, load 15-80)
MUTATE=1 CFG158_NPROC=4 python3 cfg158_referee.py                          # controls M1-M5; exit 1 (bites); writes cfg158_referee_MUTATE.out / _results.json
python3 cfg158_posthoc_extra.py                                            # post-hoc rows (EdS estimators, C4 attribution, 5k vs 20k spread) -> cfg158_posthoc_extra.out
python3 cfg158_posthoc_compare.py <CFG118 results json>                    # R5, only after the two runs above -> cfg158_posthoc_compare.out
```

| file | what |
|---|---|
| `cfg158_shells.jl` | Julia kernel (final version) |
| `cfg158_referee.py` | driver: set-up, targets, runs, all checks; `MUTATE=1` runs M1–M5 |
| `cfg158_referee.out`, `_results.json` | main run (final) |
| `cfg158_referee_MUTATE.out`, `_MUTATE_results.json` | MUTATE run |
| `cfg158_posthoc_extra.py/.out`, `cfg158_posthoc_compare.py/.out` | post-hoc rows and R5 |
| `cfg158_sims/` | per-run products (binaries, meta, logs; 72 MB); a run is reused only if its spec text matches |
| `firstrun/` | the first full run kept: its `.out`, results, driver v1, kernel v2/v3 copies, logs, products (68 MB) |
| `cfg158_shells_v1_firstrun.jl` | the very first kernel |

Runtime: the frozen budget was about 20 min per run; the main run took 53.7 min wall because the machine was shared and loaded and the corrected scheme needs 22,423 intervals (against 13,780 at a flat 1 Myr). The scope was not reduced.

## The headline against CFG118's numbers

Canonical footing, N_s = 20,000, window-averaged M_c(<r)/M_c,target(<r). CFG118 numbers are its own "post-hoc (iii)" table (read after my runs). Full 24-row comparison in `cfg158_posthoc_compare.out`.

| quantity | CFG118 | CFG158 | line |
|---|---|---|---|
| M_ta/M_b, point (all masses) | 23.64 | 23.63 | H-E PASS |
| M_ta/M_b, exponential (1e9…1e12) | 19.72, 22.25, 23.48, 23.64 | 19.71, 22.24, 23.47, 23.63 | H-E PASS |
| r_ta(z=0) kpc (point) | 236, 508, 1094, 2358 | 236, 508, 1094, 2358 | H-E PASS |
| R(1.12) envelope, all 24 runs | [1.04, 4.24] | [1.07, 4.65] | H-A PASS |
| R(1.12) envelope, point cores only | (in its table) | [1.07, 4.29] | reported |
| R(28.2) envelope, all 24 runs | [0.275, 0.655] | [0.280, 0.678] | H-B PASS |
| R(28.2) envelope, point cores only | (in its table) | [0.381, 0.678] | reported |
| falls with radius (24 runs) | yes | 24 of 24 | H-C PASS |
| radius M_c = M_b exponent, point q = 0.05/0.1/0.2 | 0.348, 0.332, 0.321 | 0.342, 0.331, 0.338 | H-D PASS |
| same, exponential | 0.241, 0.242, 0.237 | 0.220, 0.242, 0.239 | H-D PASS |
| turnaround exponent | 0.333 (point), 0.342 (exp) | 0.3333, 0.3416 | H-D PASS |
| x_1 (M_c = M_b), point q = 0.1, 1e9 to 1e12 | 1.75, 1.12, 0.80, 0.54 | 1.68, 1.12, 0.81, 0.51 | reported |
| Hubble flow dr, dv | 4.3e-7, 2.0e-7 | 1.7e-7, 2.5e-7 | C1 PASS |
| EdS slope (least squares, 7 bins) | −2.238 | **−2.410** | **C2 FAIL** |

Case-by-case agreement with CFG118 (24 cases, ratio CFG158/CFG118):
- x = 1.12: median 1.033, largest deviation 27% (exp 1e9, q = 0.05: 4.65 against 3.66), 13 of 24 within 5%.
- x = 28.2: median 1.007, largest deviation 12%, 22 of 24 within 5%.
- 5,000-shell runs: x = 1.12 median 7.5% (largest 89%), x = 28.2 median 1.8% (largest 19%).
- Local C_infall/C_target: x = 1.12 median ratio 1.04, 16–84% [0.89, 1.14]; x = 28.2 median 0.95, [0.82, 1.18]; x = 0.11 noisy in both (median 1.24, [0.54, 3.8]; exponential bins differ by up to ~20×).

## Verdict per pass line

| line | verdict | numbers |
|---|---|---|
| H-A | PASS | R(1.12) envelope [1.071, 4.646] (min in [0.85, 1.15], max in [3.57, 4.83]); point-only [1.071, 4.288] |
| H-B | PASS | R(28.2) envelope [0.280, 0.678] (min in [0.238, 0.322], max in [0.561, 0.759]); point-only [0.381, 0.678] |
| H-C | PASS | R(28.2) < R(1.12) in 24 of 24; non-increasing over x = 1.12, 3, 10, 28.2 in 24 of 24 |
| H-D | PASS | point exponents 0.342, 0.331, 0.338 (line [0.29, 0.38], all < 0.45); turnaround 0.3333 (line [0.323, 0.343]); exponential 0.220, 0.242, 0.239 (line [0.17, 0.29]) |
| H-E | PASS | M_ta/M_b point 23.63 (line 20.1–27.1), exp 19.71–23.63 (line 16.7–27.1); r_ta and x_ta within lines |
| H-F | PASS | G1 fails in all 24 canonical runs; the longest stretch inside ±10% is 0.0–0.4 dex; largest deviation 0.9–26 for point cores and 3.9–7000 for exponential spheres (inner bins) |
| C1 | PASS (second run) | 1.7e-7, 2.5e-7 |
| C2 | **FAIL** | slope −2.410 (line |slope + 9/4| ≤ 0.15 and |slope + 2.238| ≤ 0.05); local slopes −2.84 to −1.91; counts per bin 75–180; M_ta/M_seed = 56.38 (hand 57) |
| C3 | **FAIL** | largest |R5k/R20k − 1|: R(1.12) 0.623 (line 0.25; median 0.096), R(28.2) 0.132 (line 0.10; median 0.028); 5,000-shell runs: still 24 of 24 falling, R(1.12) [1.07, 6.54], R(28.2) [0.28, 0.67] |
| C4 | **FAIL** | R(1.12) 1.856 to 1.842 (−0.8%); R(28.2) 0.441 to 0.483 (+9.5%); line 3% |
| C5 | PASS | zero-velocity radius at z = 0 vs single-shell r_ta: largest 3.7e-5 (line 1e-2) |
| C6 | PASS | pericentre 0.05000, 0.10000, 0.20000; energy drift 1.4e-6, 5.4e-7, 1.4e-7 over 2000 orbits |
| C7 | PASS | target identities to 4e-16 (point), 6.4e-9 (closure ODE), 1.7e-9 (exponential Poisson) |
| C8 | PASS | on R = 1 the evaluator fails H-A and H-C |
| exit | 1 | C2, C3, C4 |

## Every disagreement, classified

- **Numerical, CFG158 vs CFG118 (valid):**
  - C2: my slope is −2.410 where CFG118 has −2.238 (both fits over r/r_ta in [0.03, 0.15], 7 bins). Post-hoc (`cfg158_posthoc_extra.out`) the slope moves by ±0.1 with the radius window and with time-averaging (−2.22 to −2.43), so −9/4 is not excluded by my code; but the frozen line is missed and stays missed. Cause not identified.
  - R(1.12): individual cases differ from CFG118 by up to 27% (exponential 1e9, q = 0.05). Median 3%. This is inside the ~10–20% run-to-run noise at 5,000 shells, but at 20,000 shells I have no second realisation to say the noise is that large there.
  - R(28.2): agrees to a median 0.7%.
  - The local x ≈ 0.11 bins (few shells) disagree by factors up to ~20 for exponential spheres; both codes call those bins noisy.
- **Qualitative:** none. The sign of every deviation (too much cold mass inside r_M, too little outside), the falling ratio and the M^(1/3) radial scale all agree.
- **Control (mine; the frozen text says this limits how the run can be read):**
  - C3 and C4 fail. Post-hoc attribution (`cfg158_posthoc_extra.out`, 1e10 point q = 0.1, N = 5,000): halving Δt_s and η_H alone gives R(1.12) 2.04 and R(28.2) 0.435; changing rtol alone gives 2.05 and 0.436; both together gives 1.84 and 0.483; the base is 1.86 and 0.441; the 20,000-shell run gives 1.99 and 0.493. So single parameter changes move R(1.12) by ~10% and the combined change moves R(28.2) by ~10%: chaotic sensitivity at the noise floor, not a systematic trend. That noise is a limit on what "agreement" can mean here.
  - C2 as above.
  - C1 failed in the first full run (see below) and passes now.

## The first full run (kept) and why the scheme changed

The first full run used a flat Δt_s = 1 Myr with the frozen predictor–corrector (node profile interpolated at fixed r). Its own controls failed:
- **C1 = 9.7e-2** (bulk shells −0.4%, end shells up to 10%). Cause: at z = 100 a 1 Myr interval is 4% of a Hubble time, the shells move several node gaps per interval, and the fixed-r interpolation only cancels for equal gaps.
- Its C2 (−2.409), C3 (R(1.12) 0.387, R(28.2) 0.134) and C4 (R(1.12) −12.3%, R(28.2) +12.6%) also failed.
- Its headlines nevertheless passed: H-A [1.087, 4.535], H-B [0.287, 0.677], H-C to H-F PASS. So the headline agreement did not depend on the C1 repair.
- Also in the first run, 10 runs crashed with a "step underflow" (shells on circular orbits in the exponential core have v_r ≈ 0 and no radial acceleration, so a relative tolerance on v_r is unattainable). A last-resort branch (tolerance scaled by j/r, reached only below h = 1e-10) was added. It never triggers in the runs that had completed (a completed run was re-run and its outputs are byte-identical; counter `vscale_fallbacks = 0`).

The kept scheme differs from the frozen text in two ways, both disclosed:
1. **Adaptive early Δt_s** = min(1 Myr, η_H/H) with η_H = 3e-4 (22,423 intervals). A pre-run test at N = 2,000 gave C1 deviations 1.8e-6 at η_H = 1e-3 and 1.7e-7 at 3e-4.
2. **Rank-node interpolation:** in the corrector the k-th node radius is interpolated linearly in time between the sorted profiles, rather than interpolating M_c at a fixed r. This is exact for a uniform expansion.

The first-run folder holds the driver v1, the kernel v2 and v3 copies, the `.out` and the products.

## MUTATE outcomes

| cell | result | verdict |
|---|---|---|
| M1 drop the core | R(1.12) = 8.7e-4 (no turnaround at all: 0 of 5,000 shells) | **bites** (H-A and H-E fail) |
| M2 near-radial q = 0.002 | R(1.12) = 2.605, R(28.2) = 0.290 against the q = 0.05, N = 20,000 run's 2.106: ratio 1.237 (line 1.3) | does **not** bite (informative; expectation P = 60% missed) |
| M3 no smooth baryon background (shells carry Ω_m) | M_ta/M_b = 36.81 (line > 27.1); the simulation's zero-velocity radius 577.9 kpc against the single-shell 578.0; R(28.2) = 0.665 | **bites** (H-E fails) |
| M4 sub-Hubble IC v = 0.9 H r, no core | max deviation from the Hubble flow 0.23 at a = 0.060 (z = 15.7), line 1e-2 | **bites**, but on a truncated run (see departures) |
| M5 evaluator on the target's M_c | C8: R = 1 fails H-A and H-C | as required |

MUTATE exits 1 (M1, M3 and M4 each bite). Two things to note:
- The near-radial M2 lowers R(28.2) from 0.49 to 0.29 while raising R(1.12) by 24%; the cold mass moves inward, which is the wrong direction for the target.
- The M1 value 8.7e-4 is far above my hand estimate (1e-6). The cause is the linear-through-the-origin profile inside the innermost node, a discreteness artefact of the 5,000-shell profile.

## What is shared and what is independent

- **Shared inputs, read from the frozen file or README:**
  - Planck18 (H₀ = 67.4, Ω_m = 0.315, Ω_c = 0.2655), z_i = 100 on the Hubble flow, matter + Λ only.
  - The CFG44 target and its exponential sphere.
  - The smooth uniform baryon background and the static core from z_i.
  - Plummer softening at 1e-3 r_M.
  - The j formula at first turnaround for q = 0.05, 0.1, 0.2.
  - The 3 r_ta extent rule and the exponential h = 2, 3, 4, 5 kpc against M_b = 1e9 to 1e12. Both were my guesses, flagged in the frozen file. **CFG118's docstring confirms the h mapping** (opened after the runs); my extent reading reproduces its M_out to 5e-4.
  - The local-dynamical-time averaging window.
- **Independent:**
  - The language, the code and the integrator. This lane uses adaptive Dormand–Prince 5(4) test bodies in a rebuilt enclosed-mass profile; CFG118 uses a block-step KDK leapfrog with per-kick sorting.
  - The single-shell set-up by scipy root-finding.
  - The cumulative-mass extraction, binning and averaging code.
  - The EdS set-up.
- **Independence stops at:** the frozen cosmology and set-up, the readings above, the j formula, and Newtonian gravity. A shared wrong reading (the smooth-background convention, the j formula) cannot be seen; M3 and the point-mass-form j row are the only probes. Row R3: the point-mass-form j gives R(1.12) = 1.77, R(28.2) = 0.49 against the base 1.86, 0.44 (1e10, q = 0.1, N = 5,000). An outer extent of 6 r_ta gives 2.91 and 0.43.

## Wrong expectations kept

- E1: hand M_ta ≈ 28 M_b (range 20–35); the code gives 23.63. The estimate was 18% high but inside its stated range.
- E8: EdS slope within 0.15 of −9/4 (P = 80%) and within 0.05 of −2.238 (P = 50%): both missed (−2.410).
- E9: Hubble flow ≤ 1e-6 (P = 90%). It failed on the first run and needed two fixes.
- C3 (P = 65%) and C4 failed.
- M1: hand estimate 1e-6, found 8.7e-4 (discreteness).
- M2: P(bite) = 60%, did not bite.
- M3: hand M_ta = 40–55 M_b, found 36.8; the direction and the bite hold.
- Hand estimates that held: r_ta (P 70%), x_ta, R(28.2) envelope ends (P 40%), R(1.12) envelope ends (P 30%), the exponents (P 70% and 35%), the falling ratio, the sign.

## Departures from the frozen criteria

1. Adaptive early Δt_s and rank-node interpolation (above). The pre-fix run is kept.
2. The last-resort v_r tolerance branch (above).
3. **M4** is run to interval 6,000 (z = 15.7, 0.25 Gyr), not to z = 0. The full sub-Hubble run collapses every shell and is impractical (a 500-shell version stalled for minutes at the collapse). The deviation of 0.23 already exceeds the line at that epoch.
4. **C4** halves η_H with Δt_s (0.5 Myr, η_H = 1.5e-4) and takes rtol 1e-11.
5. Sample cadence (2 Myr over the last 400 Myr, 20 Myr out to 8 Gyr) and the local window are my own; snapshot values are in `.out`.
6. The runs were spread over 4–12 Julia workers; the wall time is 2.7 times the frozen budget.
7. The kernel's `maxint`/`tfinal` option (for M4) was added after the main run; it does not touch the default path but that was not re-verified bitwise.
8. The frozen H-D exponential line ([0.17, 0.29]) is included in the H-D pass.

## What was NOT tested

- Non-spherical collapse, mergers, tidal torques, a growing baryon core, feedback, warm or self-interacting dark matter, any j distribution other than the three brackets (the frozen file's declared list).
- Whether 20,000 shells are enough for the ~10% noise: no second 20,000-shell realisation exists. C3/C4 show 5,000 shells are at the ~10% level.
- The alt-footing tables are computed (`.out`) but carry no pass line.
- The bootstrap errors of CFG118 were not re-derived.
- The local inner bins (x ≲ 0.3) are noisy and not compared beyond the table above.
- No CFG118 script was re-run; its numbers are read from its JSON.

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## In-place re-run (orchestrator)

Re-run in this directory (`run_all.out`): the main run `CFG158_NPROC=12 python3 cfg158_referee.py` (53 min wall on a loaded machine) exits 1 exactly as the referee's did: H-A to H-F, C1 and C5-C8 pass, C2, C3 and C4 fail (kept). `MUTATE=1` (`CFG158_NPROC=4`, fresh runs; the referee's MUTATE used cached runs) exits 1 (the controls bite); the two post-hoc scripts exit 0. `cfg158_referee_results.json` and `cfg158_referee_MUTATE_results.json` are identical to the referee's apart from the recorded wall time; the `.out` files differ only in timing and, for MUTATE, in the cache line ("cached: 0, to run: 4" here against "cached: 4" there). The run is deterministic. The 72 MB of per-run products (`cfg158_sims/`, regenerated by the run) and the referee's 68 MB of first-run products are not committed; `firstrun/` holds the first run's scripts, kernel versions and outputs (the first full run failed C1 at 9.7e-2 and had ten step-underflow crashes; kept as produced). The frozen criteria are `../CFG158_FROZEN_CRITERIA.md` (240bcd976).


## Fresh re-run by the orchestrating session (2026-09-29)
The scripts and kernels were copied to a scratch directory without `cfg158_sims/`, so every simulation was regenerated. The runs were: `CFG158_NPROC=12 python3 cfg158_referee.py` (43 min, exit 1 as documented), `MUTATE=1 CFG158_NPROC=4` (exit 1), and both post-hoc scripts (exit 0; the compare script against CFG118's committed results JSON). `cfg158_referee_results.json` and `cfg158_referee_MUTATE_results.json` are identical to the committed ones apart from the recorded wall time, and both post-hoc `.out` files are identical. C2, C3 and C4 fail exactly as committed, and M2 does not bite, as committed.
