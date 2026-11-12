# SLK1 (SLOW-TAIL KERNEL ON THE RADIAL ACCELERATION RELATION): FROZEN CRITERIA

Committed alone, before any SLK1 script exists and before any SLK1 number is computed. 2026-11-12.
Owner, 2026-11-12: "keep swinging". A test lane: it adopts nothing.

κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt), never pooled. Not "theory closed". No outcome may be
described as the data favouring the framework.

## 0. What this lane is

EUC7 (f4d4b5ae46): the Codex phase-2 slow-tail kernel `μ★(x) = 1 − 1/√(1 + 2x)`, unscreened and unfitted, lands the
SLACS lenses at a Salpeter stellar mass where law S (`μ = x/(1+x)`) is 0.07 dex short. EUC7 named the next gate:
rotation curves, where the slow tail's transition is stronger (at g_N = a₀ it gives g = 1.85 a₀ against law S's 1.62).
This lane runs it on the published radial acceleration relation.

## 1. Data (frozen)

`sol61_push/cold_production_2026_10_11/empirical_2026_10_12/RAR.mrt`: Lelli, McGaugh, Schombert & Pawlowski (2017),
data behind their Figure 2: log g_bar, its error, log g_obs, its error, for the SPARC points that pass their quality
cuts, with their stellar mass-to-light ratios (0.5 disc, 0.7 bulge at 3.6 μm) already applied. Used as published. The
script prints the file's sha256 and the number of points.

**Seen before freezing (disclosed).** The file's header and its first 17 rows; EUC7's results; the transition values
above. No residual, scatter or fit of any kernel on this file has been computed in this lane.

## 2. Kernels and statistics (frozen)

Kernels, each as the spherical algebraic relation `g_N = μ(g/a₀) g`:
- **K** slow tail, `μ = 1 − 1/√(1 + 2x)`;
- **S** law S, `μ = x/(1 + x)`;
- **B** law B, `g² = g_N² + a₀ g_N`;
- **R** the published fitting function, `g = g_N / (1 − exp(−√(g_N/a₀)))` (reference only).

For each kernel and footing, with residual `r = log g_obs − log g_pred(g_bar)`:
1. `rms` of `r`;
2. `median` of `r`;
3. `trend` = the range (max − min) of the median `r` in six bins of log g_bar with edges −12, −11.5, −11, −10.5, −10,
   −9.5, −8.5;
4. reduced χ² with `σ² = e_gobs² + (d log g_pred / d log g_bar · e_gbar)²`.

**Words for K, per footing, against S on the same points:**
- **RAR COMPARABLE** if `rms_K ≤ rms_S + 0.010`, `trend_K ≤ trend_S + 0.03` and `|median_K| ≤ |median_S| + 0.03` (dex);
- **RAR WORSE** if `rms_K ≥ rms_S + 0.020` or `trend_K ≥ trend_S + 0.06`;
- **RAR MARGINAL** otherwise.

**Reported, no word:**
- the same statistics with one global shift of log g_bar free within ±0.15 dex (a common stellar-mass and distance
  scale), chosen to minimise the rms, and the shift each kernel asks for;
- the same with a₀ free, and the a₀ each kernel asks for;
- law B and the fitting function R.

## 3. Instrument checks (frozen; a failure makes the lane NOT EVALUABLE)

- **R1** the fitting function R with a₀ = 1.20e-10 gives an rms of 0.13 ± 0.01 dex (the published scatter).
- **R2** kernel inversion for K to 1e-10 (EUC7's S1) and for S against its closed form to 1e-12.
- **MUTATE** (`SLK1_MUTATE=newton`, a₀ → 10⁻³⁰): the rms of K must rise on both footings; exit 1; separate outputs.

## 4. Not claimed

- The algebraic relation is exact for spheres; discs differ at the 10–20 % level in the field. The same approximation is
  applied to every kernel, so the comparison between kernels is like for like; the absolute scatter is not a test.
- No per-galaxy fit, no mass-to-light freedom beyond the one global shift, no screening.
- A WORSE word is a fail of the unscreened kernel on this relation at the published mass-to-light ratios. A COMPARABLE
  word is not a pass of the kernel: the Solar System obligation in EUC7 stands.
