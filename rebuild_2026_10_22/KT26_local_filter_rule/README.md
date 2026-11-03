# KT26_local_filter_rule: the local, mass-free form of ε = κ FAILS the Milky Way on canonical (0 cells, outer curve) and PASSES on alt (30 cells); the footings swap relative to KT25

Criteria: `FROZEN_CRITERIA.md`, alone first, confirmed landed. `kt26.py` (KT17's code; MW filter length set to ξ_loc(R0) per footing; KT25's ε 0.5 Cassini and dwarf parts rerun as a reproduction), `kt26.log`, `kt26.out`, `kt26.json`, `kt26.time`. No download. κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Register K838. 8 minutes, 0.45 GB.

## Part A, identity: exact
ε = κ is the same as **ξ = V∞² / g*, g* = c sqrt(G ρ) = a0 / κ**: the smoothing length is where the deep-MOND field equals g*. In this form ξ has no 1/2; the 1/2 is only in a0 = κ g*. A1 0 and 2e-16.

## Part B, the local rule
**ξ_loc = |g|² / (|∇|g|| g*)** needs no system mass and equals κ r_M for a point mass in the deep limit (B1: 1.00001 at 100 r_M, 1.00000 at 1e4 r_M).

## Part C, Milky Way (graded): ξ_loc(R0) = V² / ((1 - 2 dlnV/dlnR) g*)

| | canonical | alt |
|---|---|---|
| ξ_loc(R0) | 8.10 kpc (vs KT25's 5.0-5.5) | 6.71 kpc (vs 4.6-5.4) |
| pass all four | **0** | **30** (23 at share 0.35, 7 at 0.26) |
| L1 v_c / L3 Ou | 14 / 0 | 114 / 55 |
| best D | 1.75 (v_c 222.5, K 70.7, Ou 105) | 0.65 (v_c 227.0, K 69.2, Ou 33) |
| **Label** | **LOCAL RULE FAILS MW** | **LOCAL RULE PASSES MW** |

The `LABEL` lines in `kt26.log` are KT17's combined labels from the copied code (they use the ε 0.5 Cassini row) and aren't KT26's labels; the table above is.

## Part D, direction only (not graded)
- Sun, MW field 2.32e-10 included: ξ_loc = 208 r_M (canonical), 189 (alt) at Saturn; **4.8 r_M and 3.0 r_M at r_M**. That's far above KT16's Cassini threshold (0.45, 0.50), so the local rule would very likely **pass Cassini on both footings**, alt included, where KT25's global form failed.
- Fornax-like dwarf in the MW field: ξ_loc 0.40 kpc (canonical), 0.33 (alt), about 3x KT25's. More smoothing removes phantom, so the direction is **worse for the dwarfs**; KT15 showed too much smoothing hurts them (9/24). Not graded.

## Reading
- **The local rule smooths more than the global one wherever the field isn't deep-MOND**, because there V² > V∞². At R0 that's 1.5x more. Canonical's MW loses its outer curve at 8.1 kpc; alt's lower g* gives 6.7 kpc, which still passes.
- **The footings swap:** the global form (KT25) survives on canonical and fails Cassini on alt; the local form fails the MW on canonical, passes it on alt, and would very likely pass Cassini on both. So no single footing passes both forms.
- As hard as a fail: alt's passing cells are KT17-type corners (thick share 0.26-0.35, Sigma_b and M_bb at the high edges); strict h fails everywhere; the dwarfs and SPARC under the local rule aren't run; and ξ_loc(R0) is a one-point approximation to a position-dependent filter, not a solve of the local field equation.

## Checks
A1, B1 pass. Reproduction: KT25's Cassini (0.481, 1.06) and dwarf (15/24) rows reproduced exactly. KT17's C3 half-space check fails again (known). Q5 doubled grid on alt's best: dK +0.06, dv +0.08. MUTATE: KT17's path, not rerun.
