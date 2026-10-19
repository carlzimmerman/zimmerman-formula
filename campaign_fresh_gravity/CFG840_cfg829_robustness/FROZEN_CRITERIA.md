# CFG840 FROZEN CRITERIA: robustness of CFG829 ("isolated late types obey the law at the dwarfs' g_bar") (before any script)

**ID note:** first ID of a new owner-chat block 840–849, taken 2026-10-18 after the ledger and lane dirs showed no CFG840–849.

**Why.** CFG829 is the night's headline positive (blue lenses A = 1.016 ± 0.086 over the law, excluding the dwarfs' ×2.75 at
20σ). The standing rule is to verify a win as hard as a fail. CFG829's script and statistic are reused unchanged
(`../CFG829_lensing_low_g_vs_dwarf_excess/cfg829.py` functions); only the variants below change.

## Variants (each reports A ± σ_A for blue lenses, canonical a0, ν_e)
- **V1 window shifts:** the window [10^−13.3, 10^−11.9) shifted by −0.3 and +0.3 dex, and widened to [10^−14, 10^−11.9).
- **V2 stellar-mass systematic:** g_bar × 10^−0.2 and × 10^+0.2 (B21's lens stellar masses carry a ~0.2 dex systematic);
  the window is applied to the shifted g_bar, the law re-evaluated at the shifted g_bar; g_obs unchanged.
- **V3 alternative late-type definition:** Sérsic bin 1 (n < 2, disc-like) instead of colour.
- **V4 independent lens sample:** GAMA isolated lenses (B21 Fig 4/C1, all types; reported against the KiDS all-isolated value,
  since GAMA is not colour-split).
- **V5 alt footing** (already in CFG829; repeated for completeness).

## Classes
- **ROBUST** if, in every V1–V3 and V5 variant, blue/disc A is within 2σ_A of 1 AND at least 3σ_A below 2.75.
- **FRAGILE** if any variant has A − 1 ≥ 2σ_A, or 2.75 − A < 3σ_A. Name the variant.
- V4 is reported (consistency of GAMA all-isolated with KiDS all-isolated within 2σ), not classed.

## Controls
- K1: the unshifted primary reproduces CFG829's A = 1.016 ± 0.086 exactly.
- MUTATE: g_obs × 2.75 in V1 → FRAGILE (every variant fails the 3σ-below-2.75 condition).

κ = ½ fitted; cold energy mass required; not theory closed.
