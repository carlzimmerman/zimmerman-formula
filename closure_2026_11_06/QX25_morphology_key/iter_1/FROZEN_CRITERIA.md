# QX25 iter_1 frozen criteria: is the plain-law step keyed on morphology / type?

Frozen before any graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Both footings, never pooled.
Rules are in closure_2026_11_06/SWARM_BRIEF.md.

## Why

QX20 found the plain law's offset is a step: hot and early systems sit +0.2 to +0.45 dex above SPARC. No single measured
variable tried so far explains it (QX20-QX24). The one candidate left is type itself.

Already seen before freezing, and disclosed:
- the SPARC Hubble-type counts on QX8's 175 galaxies: 16 with T <= 2, 97 with T >= 7;
- QX21's KiDS colour-split number (D = +0.158, s_stat 0.040);
- CFG61's printed Sersic-split chi2 (69.1 / 15).

No SPARC residual has been split by type.

## T1 (graded): Hubble type inside SPARC, at fixed g_bar

Data. QX8's loader, imported read-only: the 175 SPARC rotmod files plus SPARC_Lelli2016c.mrt, with T taken from the
mrt (never SPARC_table.txt). Exact-field corrections come from QX8's parts/ (read-only).

- Classes: EARLY = T <= 2 (S0, Sa, Sab); LATE = T >= 7 (Sd and later).

- Point residual: r = log10 g_obs - log10 g_pred. Four modes:
  - L0: law, fixed U = 0.50 (bulge 0.70, QX8's convention). **PRIMARY.** A per-galaxy U refit can absorb a type offset.
  - L1: law, refit U per galaxy (QX8's fit_one).
  - E0: exact field, fixed U.
  - E1: exact field, refit U.

- Fixed g_bar. Bin log10 g_bar (at U = 0.5) in 0.25 dex bins from -12.5 to -8.5.
  - In each bin, average each galaxy's points (weights W as QX8).
  - Class value = the unweighted mean over the class's galaxies in that bin.
  - Use a bin only if each class has >= 3 galaxies in it.
  - d_b = EARLY - LATE.
  - D = sum(w_b d_b) / sum(w_b), with w_b = n_e n_l / (n_e + n_l).
  - sigma_D = standard deviation of 2000 galaxy-bootstrap resamples (seed 25).

- Prediction. A type key sized to QX20's step predicts D >= +0.20 for the early end.

- Lines, applied to L0 on each footing:
  - KILLED if D <= 0.20 - 3 sigma_D.
  - SUPPORTED if D >= 3 sigma_D and D >= 0.20 - 2 sigma_D.
  - NO VERDICT otherwise.
  - The T1 label needs both footings to agree; otherwise NO VERDICT.
  - L1, E0 and E1 are reported with the same statistic.
  - For L1 and E1, also report the median per-galaxy log10 U_refit for EARLY minus LATE: the absorbed channel.

- Robustness, reported only: the Q <= 2 subset, and a looser EARLY class T <= 3.

## T1b (graded): continuous type proxies inside SPARC

Proxies:
- bulge fraction f_b = sum(1.4 Vbul^2) / sum(Vdisk^2 + 1.4 Vbul^2) over the galaxy's points (U = 1 shapes);
- central disc surface brightness SBdisk (mrt), used as log10 SBdisk.

Statistic:
- bin-matched residual per galaxy = the mean over its L0 points of (r - the mean of all galaxies' r in that g_bar bin);
- Q = the difference in the mean of that residual between the top and bottom proxy quartiles;
- for f_b, the top quartile is the most bulge-dominated;
- for SBdisk, the top quartile is the highest-SB discs, which are the more early-type, compact end;
- sigma from the same bootstrap.

Lines: the same as T1 (prediction >= +0.20), per proxy, both footings.
- f_b uses only galaxies with f_b > 0 versus f_b = 0: for bulgeless galaxies, the quartile rule is replaced by
  "f_b >= the 75th percentile of the f_b > 0 galaxies" against "f_b = 0".

## T2 (reported, ranked): which KiDS proxy carries the early/late split

Data: Brouwer+2021 Fig-8 isolated-lens colour bins (u-r split at 2.5) and Sersic bins (split at n = 2), with their
bias-corrected covariances.

Statistic: QX21's GLS mean of log10(ESD_early / ESD_late) on K1 bins 8-14, with the same s_sys = 0.05.

Law prediction:
- colour: CFG61's lens-by-lens value, +0.0002;
- Sersic: 0 to the same size. The algebraic law gives g_obs as a function of g_bar alone, so only projection terms enter.

Reported for each proxy: D, s_tot, and D/s_tot.
- A proxy "carries" the split if D >= 3 s_tot.
- The proxies are ranked by D/s_tot.

At fixed stellar mass: B21 released no type split crossed with mass bins, so that test is not on disk. It is written into
NEEDS_OWNER.md (the KiDS-bright isolated lens catalogue with colour, Sersic n and M*). Nothing is downloaded.

## T3 (statement rule, fixed now)

If T1 is KILLED on both footings and KiDS colour or Sersic has D >= 2 s_tot, the lane states: "the step separates
spheroid-dominated systems from discs. It does not appear within discs" (scoped to SPARC's T range and the B21 splits).

Otherwise the lane states what T1 and T2 show, with no extrapolation.

## Known answers

- KA1: QX8's algebraic-mode pooled grade, run through the import: rms 0.054087 @ U 0.52 (canonical), 0.053718 @ 0.44 (alt),
  to 1e-4.
- KA2: QX21's colour D = +0.15817, s_stat 0.04010, to 1e-4.
- KA3: CFG61's Sersic split chi2 on all 15 bins = 69.1 +- 0.5.

## Controls (MUTATE run, separate outputs qx25_MUTATE.*)

- M1, shuffled T: 1000 shuffles of the EARLY / LATE labels within the union, on L0. The mean shuffled D must satisfy
  |mean| <= 0.5 sigma_D, so the statistic carries no built-in offset.
- M2, power: plant +0.20 dex on every EARLY galaxy's points. The recovered D must equal D_obs + 0.20 to within 0.02.
- M3, Newton: replace the law by g_pred = g_bar. The all-SPARC mean residual at fixed U must shift by >= +0.30, so the
  anchor bites.
- If M1 or M2 fails, T1 is NO VERDICT.

## Scope

Late-type SPARC discs only, plus B21's isolated KiDS lenses. No ellipticals inside SPARC. A KILLED T1 does not exclude a
key that switches on only for spheroid-dominated systems outside SPARC's T range.
