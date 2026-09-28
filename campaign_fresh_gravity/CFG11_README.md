# CFG11 — the cold budget under FG001's own hierarchy

Script: `CFG11_budget_hierarchy.py`, about 10 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Every group is split back into its galaxies, which gives R = 1, so H0 fails (rc = 1). The MUTATE edges then reproduce CFG4's every-galaxy edges exactly.
- The main run exits 1, because H1 failed.

κ = ½ is fitted. Both footings are used.

## The question

CFG4's minimal conflict is KiDS's reach against the cold matter that has turned around. At the strict reading (z = 0, the turned-around share 0.602 of Ω_c), the window is closed:
- the budget edge is 0.280 (canonical P2) or 0.243 (alt);
- the KiDS floor with the 2-halo term is 0.303–0.310.

That budget let **every galaxy** carry its own phantom out to x r_ta; CFG4 called it an upper bound. Under FG001, only the outermost bound system owns a phantom:
- a group's cold component is one phantom, sourced by the group's total baryons;
- members' cold components are lumps inside it, never added on top (T5).

The per-system phantom grows sublinearly with baryonic mass (≈ M_b^¾), so grouping can only lower the sum.

## The measurement

Grouping comes from the Kourkchi & Tully 2017 catalogue (ApJ 843, 16; `real_research/data/kt2017_*.tsv`). Groups are defined inside their second-turnaround radius.

**Samples.** Volume-limited: D ≤ D_max and K_s ≤ 11.75 at D_max.

**Distances.** The catalogue's own convention, the group's mean V_hel / 75.

**Per-system phantom.** CFG4's own function: the law's isolated profile, Δ_ta(0) = 11.81, with the phantom out to x r_ta.

**Baryons.** CFG4's own: M_* = 0.6 L_K (declared), plus SPARC's gas fraction fit.

**The ratio.** R(x) = Σ_groups M_ph(Σ members' M_b) / Σ_galaxies M_ph(M_b).

**The FG001 budget.**
- The reduction 1 − R is applied only above each sample's mass limit. Dwarfs below the limit keep their own phantoms (conservative).
- The strict edge solves Ω_ph,FG001(x_b) = Ω_c × 0.602.

## Results

| check | result |
|---|---|
| C1: CFG4_target's committed Ω_ph(x), budget edges, Ω_c and f_ta | 192 values, reproduced exactly |
| C2: the join, with summed member L_K against the catalogue's group logK | no missing groups; median \|d\| 0.058 dex in the catalogue's convention (659 groups). The "Dist" column gives 0.151 |
| H0: grouping lowers the sum, R(0.31) < 1 | pass: 0.891 (D ≤ 15), 0.766 (D ≤ 25), 0.806 (D ≤ 35) |
| **H1: the strict edge reaches the KiDS floor on both footings, both kernels, all three samples** | **FAILED** |

The strict edge under FG001 (floor with the 2-halo term in parentheses):

| sample | canonical P2 | canonical ν_mono | alt P2 | alt ν_mono |
|---|---|---|---|---|
| D ≤ 15 Mpc (satellite fraction 0.33) | 0.306 (0.309) | 0.303 (0.303) | 0.265 (0.310) | 0.263 (0.306) |
| D ≤ 25 Mpc (0.46, Virgo inside) | **0.336** | **0.333** | 0.292 | 0.289 |
| D ≤ 35 Mpc (0.39) | **0.322** | **0.319** | 0.279 | 0.277 |
| D ≤ 35, largest group removed (0.35) | **0.313** | **0.310** | 0.271 | 0.269 |
| every galaxy its own system (CFG4) | 0.280 | 0.278 | 0.243 | 0.241 |

The robustness rows (reported, P2), as edges canonical / alt:

| variant | D ≤ 25 | D ≤ 35 |
|---|---|---|
| Υ_K 0.4 | 0.339 / 0.294 | 0.324 / 0.281 |
| Υ_K 0.8 | 0.334 / 0.290 | 0.320 / 0.278 |
| K_s ≤ 13 | 0.348 / 0.302 | 0.332 / 0.288 |
| the "Dist" distances | 0.350 / 0.304 | 0.337 / 0.293 |

The alt footing stays 0.006–0.04 short in every variant.

## Disclosure

The first run was the MUTATE run. Its C2 used the catalogue's "Dist" column and failed, at a median |d| of 0.151 dex.

The diagnosis: the catalogue's group luminosities use velocity distances. Mean V_hel / 75 reproduces them to 0.058.

The lane was switched to that convention before the main run, with "Dist" kept as a robustness row. The hypotheses were not changed.

## Standing

**The minimal conflict narrows but does not close.**
- FG001's own bookkeeping removes 11–23% of the phantom budget.
- On the canonical footing that opens the strict window in the deeper samples: x_e ∈ [0.31, 0.32–0.34].
- The alt footing stays closed. It would need R ≈ 0.72–0.78.
- The canonical Local Volume sample misses by 0.003.

**Caveat.** The catalogue's groups are virialized structures, inside the second turnaround. FG001's top-level system is the outermost bound system, which can be the larger turned-around region.
- Counting infall regions as part of their group would lower R further. That is untested.
- It needs its own declared association criterion. The framework's own r_ta is the natural one.

Nothing here says the theory is closed.
