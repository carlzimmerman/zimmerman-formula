# KT29_tidal_rule_mw_full_tensor: with the full tidal tensor, the tidal rule FAILS the Milky Way on both footings (ξ 37-53 kpc, v_c ≤ 204, 0 cells). KT28's alt survival depended on dropping the vertical term

Criteria: `FROZEN_CRITERIA.md` (3026c358d5), alone first, confirmed landed. `kt29.py` (KT28's MW arm; ξ per cell from the full tensor at (R0, 0)), `kt29.out`, `kt29.json`, `kt29.time`. No download. κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Register K842. 9 minutes, 0.88 GB.

| | canonical | alt |
|---|---|---|
| full-tensor ξ_tid(R0, 0), min/median/max | 41.7 / 48.1 / 53.0 kpc | 37.0 / 42.9 / 47.0 kpc |
| in-plane only, cell's own V (KT28's form) | 6.7 / 7.7 / 8.9 | 6.0 / 6.8 / 7.9 |
| cells passing all four | **0** (L1 0, L3 0; v_c max 203.0) | **0** (L1 0, L3 0; v_c max 203.9) |
| **Label** | **FULL-TENSOR TIDAL RULE FAILS MW** | **FAILS MW** |

**So KT28's alt survival is recorded as dependent on dropping the vertical term**, as frozen.

## Reading
- In the disc midplane the vertical tidal component T_zz ≈ ν 4πG ρ_b dominates τ, and it falls slowly with R (the gas columns are flat out to ~7 kpc), so ∂_R τ is small and ξ_tid is large: about 6x the in-plane value. My hand estimate was 15-25 kpc; the gas makes it worse. Smoothing over ~40 kpc removes most of the Milky Way's phantom: v_c drops to about 203 km/s, against 229 needed.
- **Beside, and this matters as much as the fail:** at z = 1.1 kpc, where K_z is measured, the same rule gives ξ of only 0.004-0.04 kpc, because there ∂_z τ is large (approximate, T_zz only). Within one disc the rule's length varies by a factor of about 1000-10,000 between the midplane and 1 kpc up. So a single-value treatment can't represent the rule in a disc at all. This kills the midplane-evaluated version, which is what was frozen, not every tidal rule. A real test needs a solve with ξ varying in (R, z). That's a different field equation, not this approximation.
- Either way, the tidal rule in its simplest form (Frobenius norm, |∇τ|) is dominated by local density inside a disc, not by the gravitational structure it was meant to track. That's a physical problem with the rule, not just a numerical one.

## As hard as a fail
- C2 (mass conservation of the smoothing) fails at these lengths: -6 % to -23 %, because ξ approaches the grid's reach. Some of the v_c loss is lost mass, not phantom. But KT17's ε = 1 (about 10-11 kpc) already failed v_c with mass conserved, and ξ here is 4x that, so the label doesn't hinge on C2.
- ∇²Φ = ν 4πG ρ_b drops the g_N·∇ν term; T2 (the solver's discrete Laplacian) wasn't computed, disclosed.

## Checks
C1 pass both. T1: the observed-curve in-plane value reproduces KT28 (8.778 / 7.264 kpc). C2 fails (above). KT17's C3 half-space factor fails again (known; the script exits 1 on it). MUTATE: KT17's path, not rerun.
