# Session 6 calcs: results (2026-10-06)

Criteria: `FROZEN_CRITERIA.md` (P and F frozen before their scripts). κ = ½ fitted; both footings. Promoted into committed lane CFG390 (scripts and outputs byte-identical to the exploratory run).

| test | script | frozen verdict | key numbers |
|---|---|---|---|
| P: VPOS members vs non-members (43 MW satellites with full phase space; poles from LVD proper motions, 300 MC draws each) | `plane_members.py` | **DISFAVOURED** (TDG origin within the settling model) | in-plane (either sense) 14 vs 29: Δ = **+0.034 ± 0.098** dex; co-orbiting 11 vs 32: Δ = +0.148 ± 0.094. Both footings identical (the offset differences are footing-free here). MUTATE (members made Newtonian) gives Δ = −0.52 → SUPPORTED, detected (exit 1) |
| F: fossil a₀ by Hubble type (gas-dominated deep points, Υ-free) | `fossil_a0_type.py` | **NOT POSSIBLE** | 0 early types (T ≤ 5) have ≥ 3 qualifying points; 27 late types do. MUTATE could not run (no early types) |

## What this settles
- **The settling model and a tidal-debris origin of the Milky Way's satellite plane are incompatible.** Plane members carry the same mass excess over the law as non-members. If they were tidal dwarfs, the settling model would make them Newtonian, which would put them roughly 0.3–1 dex lower. One of the two must give: either the VPOS is not made of tidal dwarfs, or old tidal dwarfs are not Newtonian (contradicting the model's young-TDG reading in CFG7). VPOS normal as recalled (169.3°, −2.8°); membership by a 30° pole cut.
- **SPARC cannot test fossil a₀ cleanly:** its early types have no gas-dominated deep points. That needs early-type galaxies with extended HI discs.
