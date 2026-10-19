# CFG823 FROZEN CRITERIA: can the dSphs' total cold-energy supply pay for their inner mass at all? (committed before any script)

**Why.** CFG822: canonical v2's free share lands too far out; dSph σ stays ~2× short. Before any new placement rule is
considered, ask the placement-independent question: is the catchment's TOTAL cold-energy supply large enough to supply the
mass the dSphs need inside r_1/2? If not, no placement rule can work and the census supply itself fails for dwarfs.

## Inputs (exactly CFG821/822)
- The same 11 MW classical dSphs (`real_research/data/dsph/lvd_dwarf_mw.csv`, same cuts), M_b = 2 L_V, r_1/2 = (4/3) r_h.
- Required dynamical mass (Wolf): M_req = 3 σ_obs² r_1/2 / G; 1σ band from σ_obs ± e_σ and Υ ∈ {1, 2, 4} (M_b ×0.5/×1/×2).
- Census supply (CFG809 machinery, read from `cfg822_results.json`): f_ret per dSph (0.10 at the floor), catchment
  baryons bc = M_b / f_ret, total cold supply S_tot = 5.364 bc (retained + free shares together).

## Statistic
- Per dSph: need ratio N_in = (M_req − M_b/2) / M_b (cold mass needed inside r_1/2, in units of M_b), against the ceiling
  S_tot / M_b = 5.364 / f_ret, and the fraction of the total supply that must sit inside r_1/2: q = (M_req − M_b/2) / S_tot.
- Placement-independent bound: q ≤ 1 is NECESSARY.

## Classes (Υ = 2 primary; Υ = 1, 4 brackets reported)
- **BUDGET FAILS** if any dSph has q > 1 at > 2σ (σ_obs error only).
- **BUDGET TIGHT** if no dSph fails but the median q > 0.3 (more than 30% of the whole catchment's cold energy must sit
  inside r_1/2 ≈ 1% of r_ta, far denser than any settled or infall profile the framework has produced).
- **BUDGET OK** otherwise (placement is the only problem; a concentrating rule could in principle fix it).
- Report also q for the settled law (CFG821 profile) for scale, and the median r_1/2 / r_ta.

## Controls
- K1: M_req for Draco reproduces the Wolf value from CFG822's σ_obs and r_1/2 to 1e-6.
- MUTATE (separate output): f_ret forced to 1 (no expelled gas): S_tot drops 10× and q must rise 10×.

κ = ½ fitted; cold energy mass required; not theory closed.
