# QX11 frozen criteria: FG1's gate set for the law alone (C4), regraded on the action's exact field

Frozen before any QX11 script exists. Rules: closure_2026_11_06/SWARM_BRIEF.md. Kappa = 1/2 FITTED; not theory
closed. Footings never pooled. Adopts nothing.

## Why

QX8 (3ba7c78ce6) regraded SPARC on the action's exact AQUAL field and passed both footings. QX9 (cd94913d33)
reported, without grading, that FG1's own Upsilon-tilt statistic on QX8's exact-field fits is +0.170 canonical,
above FG1's 0.15 line, and +0.090 alt. FG1 (rebuild_2026_10_22/FG1_final_grade, criteria 3b2fae101a) graded the
law alone as candidate C4. This lane regrades C4's lines on the exact field.

## The statistic, exactly as FG1 used it

- **Tl:** FG1's law tail (fg1_law_tail_add.py, UR2's statistic). U is each galaxy's best-fit Upsilon on the 0.30-1.20
  grid (fit_one). The sample is SPARC rotmod galaxies with Q <= 2 and Inc >= 30 (SPARC_Lelli2016c.mrt).
  t = median U(0 < Vflat < 100) - median U(Vflat > 150).
  **Line: |t| <= 0.15, per footing, as FG1 used it.** FG1 put no error on t. A bootstrap error is reported but the
  line is not moved: 4000 draws, galaxies resampled within each speed group, seed 20261106.
- **S:** the harness line, rms <= 0.110 and 0.50 <= median U <= 0.80. Recomputed here from QX8's parts.
- The exact field is QX8's: law log g plus the interpolated exact-field correction T, from QX8's parts, read only,
  the same way QX9 did it. Both footings use FG1's a0 values (9.3603e-11 and 1.1312e-10).

## Rows the exact field cannot move on FG1's own statistics (carried, with the reason)

In spherical symmetry the AQUAL equation integrates exactly to mu(g/a0) g = g_N (Bekenstein-Milgrom), so the exact
field equals the algebraic law. FG1's C4 cells for these lines use spherical or point models, so they carry over
unchanged:
- LT: point mass Mb at the outer radius R;
- G, K: spherical group and cluster templates;
- Ln: isolated point lens;
- Dw: plain nu(g_N) on dwarfs.

MW is already X5's full AQUAL row. DM stays NOT GRADED. X stays NOT GRADED, as in FG1, with CS2's numbers shown.
IC is carried as FAIL. That is an argument, not a regrade: QX8's largest low-surface-brightness median correction
(about -0.20 dex) cannot close E = -0.59 (Z -7.9). A disc-modelled exact field for LT, Dw or IC would be a new
statistic and is not graded here.

## Known answers (any failure = NO VERDICT)

- KA1: law mode reproduces FG1's tilt, +0.020 / -0.020, and median U, 0.52 / 0.44, to |d| <= 1e-9.
- KA2: law-mode LT recomputed from SL1's cache with FG1's formula reproduces -0.02515 / -0.06403 to 1e-4.
- KA3: exact-mode S reproduces QX8's exact rms and median U to 1e-9.
- KA4: exact-mode t reproduces QX9's FG1_U_tilt_ex to 1e-9.

## MUTATE (separate outputs)

Before fitting, plant an Upsilon-Vflat trend: g_obs is multiplied by 1.5 for every galaxy with 0 < Vflat < 100,
on the exact field. The exact-field Tl must then exceed 0.15 on both footings, and the run exits 1. If it does not,
the statistic has no power and no verdict stands.

## Labels, per footing

- Tl: PASS if |t| <= 0.15, FAIL if over.
- C4 on the exact field: PASSES EVERY GRADED LINE, or FAILS with the failed lines listed (FG1's format, NOT GRADED
  never a pass).
- If the canonical Tl fails, the README says so plainly. The a0 law, as an algebraic law, passes FG1's tilt row.
  The action's exact AQUAL solution fails it on the canonical footing.
