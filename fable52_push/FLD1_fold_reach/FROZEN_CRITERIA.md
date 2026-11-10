# FLD1 FROZEN CRITERIA: does the folded region reach as far as the law is seen? (2026-11-10)

Committed alone, before any script or number. TEST lane, quarantined: adopts nothing, relabels nothing, registers nothing.
Two footings, never pooled (canonical a0 = 9.3603e-11, alt 1.1312e-10 m/s^2; kappa = 1/2 FITTED).

## 0. Question and why

COL1 (origin 918545cf2b) found that the clock of action (A) folds and that the equations give no answer behind a fold;
CLOSURE.md (origin 9e4d9b3222) says any completion must make the clock static behind the fold. A necessary condition: if
the law lives only behind the fold, then at every epoch the folded region must reach at least as far as the law is
observed. From the action's own shell dynamics, how far does the folded region reach at each redshift, and does it cover
the radii where the record sees the law?

## 1. Machinery (COL1's A4, unchanged in its equation)

X14's exact shell equation in the law-dominated limit (mu_K r << 1), one independent ODE per Lagrangian shell X:

    r'' = -G M_b s(t) r/(r^2 + eps^2)^{3/2} - G M_X/r^2 - (4 pi/3) G rho_b(t) r + Omega_L H0^2 r + U(G [M_X - (4 pi/3) nbar(t) r^3]/r^2),

M_X = (4 pi/3) nbar0 X^3, U(y) = a0 y/(a0 - |y|); eps = 1 kpc; s(t) a smoothstep over 1 Gyr from the start; shells reaching
their flux-cap wall or r_s = 0.3 kpc are reflected (passage through the centre); vectorised leapfrog; KD1's cosmology per
footing. A shell's enclosed charge changes only when that shell is crossed, so every trajectory is exact up to its own
first crossing. Grid (production): N = 2400 shells, log-spaced in X from 0.03 X_M to 15 X_M with
X_M = (M_b / ((4 pi/3) nbar0))^{1/3} (the Lagrangian radius of the baryon mass); COL1's A4 grid (20 kpc to 8 Mpc) is used
for KA1 only.

## 2. Definitions (fixed before any number)

- **Crossed shell:** a shell that has had an order inversion with a Lagrangian neighbour (r_i >= r_{i+1}) at least once.
  First crossing, not turnaround.
- **R_fold(t):** the radius of the smallest sphere that contains every crossed shell at time t (the maximum current radius
  over crossed shells). Zero before the first crossing.
- **R_ta(t), the turnaround radius:** the largest current radius among shells with radial velocity <= 0. Reported beside
  R_fold.
- **Validity of the law-dominated limit:** (mu_K R)^2 <= 0.1. RESULT.md states the radius where this ends for mu_K 0.1, 1.78,
  3.71 and 198 per Mpc. R_fold is graded only from this limit; the mu_K 0.1 bracket below measures its error.
- **Mass interpolation:** R_fold(z; M_b) is computed at log M_b = 6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12 and
  interpolated linearly in (log M_b, log R_fold) at fixed z; a galaxy outside 6.5-12 is graded at the nearest end and
  flagged.

## 3. Comparisons and pass lines (per footing)

- **(a1) SPARC.** QX8's loader (the record's 175 rotmod files and SPARC_Lelli2016c.mrt). R_last = the largest measured radius;
  M_b = 0.5 L[3.6] + 1.33 M_HI (Upsilon 0.5; brackets 0.3 and 0.8 reported). **Line: R_fold(z = 0; M_b) >= R_last for every
  galaxy.** Report the count beyond the fold and the largest R_last / R_fold, with names.
- **(a2) KiDS, host-free (ONE1's bins).** ONE1's g_bar bin edges (cfg110_perlens.npz) become radii R = sqrt(G M_b / g_bar).
  Inner window = bins 7-12, middle window = bins 4-6, outer window = bins 0-3. **Line: R_fold(0; M_b) >= the outer edge of the
  inner window, and (a separate line) of the middle window, at log M_b 9.4, 10.45, 10.7 and 10.9.** The outer window is
  reported. ONE1's machinery takes a share, not an end radius; a halo ending at R_fold(0) is the truncated halo with share
  X_fold = [-1 + sqrt(1 + 4 x^2)]/2, x = R_fold / r_M, r_M = sqrt(G M_b / a0); X_fold is reported against ONE1's accepted
  range (census cap 53.64 through 59.5 at 1.6 R_h) as a mapped reading, not graded.
- **(b) High redshift.** RC100 (data_assembly/rc100_provenance/rc100_table3_six_fields_paper_values.csv, the paper's values;
  z 0.61-2.52). The paper gives no per-galaxy outer radius, only the sample's curve extent (mean 2.2 R_e, range 1.3-4 R_e).
  **Line: R_fold(z_i; M_b,i) >= 2.2 R_e,i for every galaxy.** Bracket: 4 R_e,i (the largest extent), reported. No other
  high-z sample is graded (the record holds no per-galaxy outer radii); nothing is downloaded.
- **(c) Form B's cap.** R_cap = x_t r_M with x_t^2 = X (X + 1), X = 59.5 (PD1's share). **Line: R_fold(0; M_b) >= R_cap** at
  every log M_b of the mass grid from 7 to 11.5.

## 4. Labels (per footing)

- **FOLD COVERS THE LAW'S RANGE:** (a1), (a2) inner and middle, (b) and (c) all pass.
- **DOES NOT:** any of them fails. RESULT.md names the galaxies, masses or epochs where the law is seen beyond the fold
  and by what factor.
- **NO VERDICT:** a known answer fails, or the convergence check fails.

## 5. Brackets (reported, never label-setting)

- Start redshift 20 and 30 against the primary z 10.
- At rest (today's mean density, gravity of the mean subtracted, no expansion) against Hubble flow; times mapped to z by the
  primary's clock (time since the start).
- mu_K = 0.1 per Mpc with the dust's leading correction: n_d = nbar + (mu_K^2/K) dh, dh(r) = Int_r^inf A dr', so the
  enclosed polarization charge loses (mu_K^2/K) Int_0^r 4 pi r'^2 dh dr' (one fixed-point pass per step, on the sorted
  shell radii), against the limit.

## 6. Known answers (all must pass, or the label is NO VERDICT)

- **KA1** COL1's A4 table: the first-crossing times outside 3, 10, 30, 100 kpc for all 8 rows (four masses x two footings)
  reproduced to the printed digits (three decimals in Gyr) on A4's grid.
- **KA2** A test shell (no law, no clock charge, no expansion) falling from rest in a Kepler field reaches the reflection
  radius at the closed-form time (pi/2) sqrt(q^3 / (2 G M)) corrected for r_s, and r(t) at 0.9 t_ff matches the cycloid,
  both to 1e-3.
- **KA3** Convergence in shell number at log M_b 10.45, canonical: R_fold at z = 4, 2, 1, 0 at N = 1200, 2400, 4800;
  line: N 2400 within 5 % of N 4800 at every graded epoch where R_fold > 0.

## 7. MUTATE (separate outputs; each must move R_fold(0) at log M_b 10.45, canonical, in the stated direction, by >= 5 %)

- M1 law off (U -> 0; the clock gravitates on itself): R_fold(0) **up** (self-gravitating infall gathers more charge).
- M2 start redshift halved (z_i = 5): R_fold(0) **down**.
- M3 mass x 10: R_fold(0) **up**.

## 8. Lean

`FLD1.lean`: the share-radius map x^2 = X (X + 1) <-> X = [-1 + sqrt(1 + 4 x^2)]/2 (x > 0), the deep-law halo mass
M_ph/M_b = [-1 + sqrt(1 + 4 x^2)]/2 at x = r/r_M, the window radius R = sqrt(G M/g) monotone in g, and the Kepler fall time
identity used by KA2. `FLD1_MUTATE.lean` with flipped statements must fail.

## 9. Done

Criteria (alone), scripts, outputs, MUTATE outputs, Lean with compile outputs, RESULT.md leading with the label and one
table (mass, R_fold at z 0, 1, 2, 4, the observed reach beside it), sections on what it does not settle (a necessary
condition only; non-spherical infall; mergers; the fold's own physics) and on anything in COL1 or CLOSURE.md found wrong;
committed with explicit paths and pushed by a sparse worktree. Does not touch README.md, CLOSURE.md, PAPER72, the register,
the decision file or MEMORY.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
