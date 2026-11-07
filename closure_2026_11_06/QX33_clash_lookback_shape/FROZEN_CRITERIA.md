# QX33 frozen criteria: at lookback (CLASH, z 0.19-0.70), is the mass the law is missing more concentrated than the baryons, and does that change with z?

Frozen before any QX33 number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Both footings, never pooled.

## Why (the clue under test)

The 11-07 doors (QX7 iter_4/5/7, 3f31773c79) left one clue. Near z = 0, the extra mass hot systems need is more concentrated
than their hot gas, and is closer to stars + gas. The question here is whether that is already true at z ~ 0.5, and whether it
changes with redshift.

Record already holding:
- h56 found on the same table that eta falls outward, with no redshift split and no per-cluster slope.
- An opus_48 review (FPS 2025) reported dark mass that follows the gas with a ~430 kpc exponential cutoff; that reading is
  literature, not ours.
The redshift split and the per-cluster concentration slope are new.

## Data (frozen)

- **Profiles:** Tian+2020 (VizieR J/ApJ/896/70/fig2), on disk at real_research/data/clash_rar_tian2020_fig2.tsv. It holds 84
  points in 20 clusters at r = 14.3-600 kpc.
  - g_tot comes from the Umetsu+2016 joint strong + weak lensing, so it involves no hydrostatics.
  - g_bar is gas (Donahue+2014) plus BCG stars. Gas and stars are NOT separated in this table, which is a stated limit.
- **Redshifts:** MCXC (on disk, gext_vectors_2026/data/raw/mcxc.tsv), matched by position. MACS0416 is not in MCXC, so it takes
  z = 0.396 (Postman+2012), entered by hand and disclosed. RXJ2248 is AS1063 (MCXC J2248.7-4431).
- **Split (frozen):** HIGH is z >= 0.40, LOW is z < 0.40.

## Quantities (frozen)

- Exact law inverse per footing: g_N,need = g_tot^2 / (g_tot + a0). Then R(r) = g_N,need / g_bar = M_need(<r) / M_b(<r).
- a0 is held at each footing's z = 0 value. The law ties a0 to rho_DE, which is constant to within this sample's precision.
- **Concentration slope per cluster:** s = the slope of a weighted least-squares fit of log10 R against log10 r, using every
  point of that cluster. The weights come from e_log(gtot), propagated through the inverse; e_log(gbar) is added in quadrature.
  How to read s:
  - s < 0: R falls outward, so the missing mass is more concentrated than the baryons.
  - s = 0: it traces the baryons.
  - s > 0: it is less concentrated, as gas-like or outer mass would be.
- **Amplitude:** A200 = log10 R at r = 200 kpc, interpolated in log r. Every cluster reaches 200 kpc.

## Labels (graded, per footing)

**Q1, shape at lookback (HIGH subsample; ALL reported).** The interval is a 95% bootstrap over clusters (10000 draws, seed 3333)
on the median s.
- **MORE CONCENTRATED THAN BARYONS:** the median is <= -0.10 and the upper bound is < 0.
- **TRACES BARYONS:** the interval lies inside [-0.10, +0.10].
- **LESS CONCENTRATED:** the median is >= +0.10 and the lower bound is > 0.
- Otherwise **UNRESOLVED**.

**Q2, evolution.** Delta_s = median s(HIGH) - median s(LOW), and Delta_A = median A200(HIGH) - median A200(LOW). The p value is
two-sided, from a permutation of redshift labels (10000, seed 3334).
- **EVOLVES:** |Delta| >= 0.10 and p < 0.05, for either quantity.
- Otherwise **NO EVOLUTION DETECTED**, reported with the 95% permutation half-width as the sensitivity.

## Reported, ungraded

- The Spearman correlation of s and of A200 with z.
- Variants: dropping r < 50 kpc (the BCG-dominated points; only clusters with at least 2 points left), and r scaled by the MCXC
  R500.
- The near-z clue for comparison: QX7 iter_7 (X-COP, z < 0.1) favoured baryon tracing over gas tracing.

## Controls

- K1: the inverse is exact, |g_law(g_N,need) - g_tot| / g_tot < 1e-10 at every point.
- K2: the parse gives 84 points in 20 clusters, matching h56, and all 20 match a redshift.
- K3: in the a0 -> 0 limit, R = g_tot / g_bar (Newton) to within 1e-6 dex.
- MUTATE A (bite): add -0.3 log10(r / 100 kpc) to log g_tot in the HIGH clusters only. Q2 must read EVOLVES for Delta_s.
- MUTATE B (bite): add +0.5 log10(r / 100 kpc) to log g_tot in every cluster. The Q1 label must change.
