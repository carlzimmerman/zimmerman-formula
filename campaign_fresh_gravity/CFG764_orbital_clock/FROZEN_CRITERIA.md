# CFG764 FROZEN CRITERIA: is the cold-energy formation clock a local orbital clock, τ = k·t_orb?

Date: 2026-10-13. Block CFG760–769. Committed ALONE before any CFG764 script or number. κ = ½ FITTED; both footings, never pooled;
the cold energy's mass is required; no particle species; not "theory closed".

## Why
CFG763: a universal formation time τ ∈ [0.72–0.83, 3.47] Gyr fits young TDGs and old SPARC discs. The natural framework-native
alternative is a local clock set by the dynamics: τ = k·t_orb with t_orb = 2πR/V at the measured radius (the medium settles in a few
local orbits, as in CFG747/748). Then the outer, slow-orbit radii of large discs form last. This lane tests whether one k fits both.

## Lower bound (young TDGs; CFG763 model and code)
f_i = 1 − exp(−t_i/(k·t_orb,i)), with t_orb,i as in CFG441/763 and ages at −1σ (floored at 0.05 Gyr). χ²(k) on a log grid
k ∈ [0.01, 100] (0.01 dex). k_min,95 = the smallest k with χ² ≤ χ²_min + 3.84.

## Upper bound (raw SPARC, last measured point; CFG762's loader)
Each SPARC disc follows the law at its last point, so f ≥ 0.9 there after its baryon age t_b ≥ 8 Gyr:
k ≤ 8 Gyr/(ln 10 · t_orb,last), t_orb,last = 2πR_last/V_obs(R_last). k_max = the minimum over the 175 galaxies.
(Same favourable age as CFG763; V_obs, not V_bar.)

## Test
- **O1. OPEN iff k_min,95 ≤ k_max on both footings**; CLOSED otherwise. The k_max side has no footing dependence; k_min does.
- Reported: k_max at the 5th / 50th percentile galaxy (how many galaxies the longest orbits exclude), and the predicted f at the
  last point for the median SPARC galaxy at k = k_min,95.

## Controls
- **K1.** k → 0 and k → ∞ reproduce CFG441's Tier-B χ²_law and χ²_N (as CFG763 K1) within 0.01.

**MUTATE** (`CFG764_MUTATE=1`): V_obs := V_law for the TDGs. k_min,95 must then be ≤ 0.01 (the grid floor) and O1 OPEN. Exit 1 iff
it bites.

## Not tested
Radius dependence inside one galaxy beyond the last point; non-first-order formation; TDG non-equilibrium.
