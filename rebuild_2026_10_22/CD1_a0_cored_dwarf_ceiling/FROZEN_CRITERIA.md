# CD1_a0_cored_dwarf_ceiling — FROZEN CRITERIA (committed alone, before any script or graded number)

Written 2026-10-25. The owner asked for a swing "for the actual answer" while away. κ = ½ FITTED. Footings canonical /
alt, scored separately and never pooled. Cold dark energy (w ≈ 0, a gravitating field component; not matter, never a
particle). Nothing here says the data favour the framework or ΛCDM. Not "theory closed".

## 0. Why

The record's strongest lead is X38 (f72216ad98): route-E cold dark energy halos, Burkert-cored at ρ₀r₀ = Σ_a0 = a₀/(2πG)
(107 / 129 M☉ pc⁻²), no new constant. It passes SPARC and the cluster OUTER bands. It fails the heaviest cluster cores,
which need about 2× that surface density (X39). X38 did **not** grade dwarfs ("the relation would be extrapolated").

This lane grades dwarfs **without any halo-mass relation**, using one property of a fixed-Σ Burkert halo. Its
acceleration at radius r is g_h(r) = π G Σ r₀² B(r/r₀) / r², with B(x) = ln(1+x²) + 2 ln(1+x) − 2 arctan x. For fixed
Σ, the maximum over **every** core radius r₀ is

  g_h,max = π G Σ · max_x B(x)/x² = (a₀/2) · 0.508967… = 0.254484 a₀,

independent of r. So no fixed-Σ_a0 halo, whatever its size or mass, can supply more than 0.2545 a₀ at any radius.

**Disclosed before freezing (not blind):** I computed this ceiling and compared it, at a few radii, with X24's floor
(c₀ = 4.5 km/s gives 3c₀²/r = 1.05 / 0.70 / 0.42 / 0.21 a₀ at r = 20 / 30 / 50 / 100 pc, canonical). No per-dwarf
number from the table below has been computed or looked at.

## 1. Data (on disk; nothing downloaded)

`rebuild_2026_10_22/X1_hosted_recount/x1_per_system.csv` (X1's committed per-system table, both footings, 89 dwarfs
each). Used columns: `footing, name, host, cls, logMstar, rh_pc, sigma, Delta[Newton], sdMC[Newton]`. X1 conventions
are inherited unchanged: Wolf estimator with r₁₂ = (4/3) r_h, g_obs = 3σ²/r₁₂, g_N = G (M★/2) / r₁₂², Υ_V = 2, binaries
handled as in X1 (Arroyo), and sdMC = X1's Monte Carlo spread of log(g_obs/g_N).

## 2. Quantities

- g_N from `logMstar` and `rh_pc` as above; g_obs = g_N · 10^Δ, Δ = `Delta[Newton]`.
- **Route-E requirement:** g_h,req = g_obs − g_N (the halo supplies everything above Newtonian baryons; no law force).
  Rows with Δ ≤ 0 need no halo and pass trivially.
- Its log uncertainty is sd_h = sdMC · 10^Δ / (10^Δ − 1), first-order propagation; rows with 10^Δ − 1 < 0.1 are reported
  but not graded.
- z_i = (log g_h,req − log g_h,max) / sd_h, with g_h,max = 0.254484 a₀ of the row's footing.
- **Required surface density** S_i = g_h,req / g_h,max, in units of Σ_a0: the smallest Σ/Σ_a0 that could reach the
  requirement at r₁₂ for the best possible r₀.

## 3. Classes (per footing; the lane verdict is the class if both footings agree, else UNDECIDED)

| class | rule |
|---|---|
| DWARFS EXCLUDE FIXED-Σ_a0 | ≥ 25% of graded dwarfs have z ≥ 2 |
| CONSISTENT | < 5% of graded dwarfs have z ≥ 2 and median S ≤ 1 |
| PARTIAL | anything else |

Reported only, not graded:
- the fraction with z ≥ 2 and median S by X1 class (`cls` / `host`);
- the S quantiles (50 / 84 / 97.5%);
- Spearman ρ of S with logM★ and with r_h;
- S at the dwarf scale compared with X39's cluster-core requirement (~2).

## 4. Checks

- **K1** max_x B(x)/x² from a dense grid equals the root of d/dx[B/x²] = 0 (brentq) to 1e-6, and B's closed form matches
  quadrature of the Burkert profile to 1e-8 at x = 0.5, 1, 3.
- **K2** g_N recomputed from `logMstar` and `rh_pc` reproduces X1's ratio: log(3σ²/r₁₂ / g_N) equals `Delta[Newton]` to
  0.02 dex in ≥ 95% of rows. If it fails, stop and report the definition mismatch; never re-fit.
- **K3** Row count is 89 per footing; no NaN in the used columns among graded rows.
- **MUTATE=1** (separate outputs): (a) set every g_obs = g_N · 10^(Δ/4), a weak discrepancy: the class must not be
  DWARFS EXCLUDE; (b) set every g_h,req = 3 g_h,max with the real sd: the class must be DWARFS EXCLUDE. The MUTATE run
  exits 1 if both behave as required.

## 5. Disclosed limits

- Equilibrium, sphericity and the Wolf estimator are assumed, as in X1. Tides and stripping would only lower a real
  halo's g_h, so they make the ceiling stricter, not looser.
- The ceiling assumes the X38 Burkert shape. Another cored shape at the same ρ₀r₀ has a different constant. That is
  reported as a limit, not explored (no shape scan).
- Υ_V = 2 is X1's. A larger Υ lowers g_h,req.
- This tests the X38 hypothesis on dwarfs only. It says nothing about SPARC or clusters, which X38 already graded.

Run: `python3 cd1_dwarf_ceiling.py`; `MUTATE=1 python3 cd1_dwarf_ceiling.py`. Light: < 0.5 GB, one thread, seconds.
