# CFG948 AMENDMENT A1: K2's "= BELOW in every cell" clause mis-stated CFG939's own record at v_rel = 50 km/s (control wording, not physics)

**Dated** 2026-10-21. **Post hoc.** Written after the first K-only run (`CFG948_MODE=K`, exit 2). Committed alone, before the
script is changed.

**Seen when this was written.** The K-only run computes and prints only control numbers:
- K1 printed CFG933's already-published numbers (reproduced exactly);
- K2 printed the V_esc,b of the 6 TDGs and DF2/DF4 (CFG939's published N5 values);
- K3/K4 printed engine identities, the A range of the Coma UDGs (5.15–9.13), and g_host at 1 Mpc.

No engine grid run, no ceiling, no comparison of any Coma UDG with the framework's range, no class and no MUTATE had been run
or printed.

## What failed

K2 (criteria section 7) has two parts:
- (i) **Reproduction.** CFG939's N5 rows equal its JSON. Passed: max relative difference 0.
- (ii) **Classification.** "The derived-reading sides ('tidal dwarfs', 'DF2/DF4' = BELOW) equal the JSON in every cell
  (2 footings × 4 L* × v_rel 100/50)". Failed: 8 of 16 cells.

## Why

The clause asserted BELOW for the tidal dwarfs at both v_rel values. CFG939's own `cfg939_results.json` gives the tidal
dwarfs **MIXED** in all 8 cells at v_rel = 50 km/s, because NGC 5291N has V_esc,b = 52.9 km/s > 50. DF2/DF4 are BELOW in
all 16 cells. In those 8 cells CFG939's record and the frozen sentence disagree, so no code could satisfy both. The sentence
was written without checking CFG939's v_rel = 50 cells. v_rel = 100 km/s is CFG939's declared lower bound (`VREL`) for debris
moving through a host's settled medium; v_rel = 50 km/s is its half-value sensitivity cell.

## Change (and nothing else)

K2(ii) becomes:
- **(ii-a)** The lane's derived-reading sides equal CFG939's JSON in **all 16 cells**, whatever they are. This is the
  reproduction.
- **(ii-b)** 'tidal dwarfs' = BELOW and 'DF2/DF4' = BELOW at **v_rel = 100 km/s** (8 cells), CFG939's declared bound.
- **(ii-c)** At v_rel = 50 km/s, DF2/DF4 = BELOW (8 cells). The tidal dwarfs' MIXED there is reported, not asserted.

K2(i), and everything else, is unchanged: the estimator, the engine, the grids, the ceiling rule, the classes, the
systematics, the reported rows, K0, K1, K3, K4 and MUTATE.

κ = ½ FITTED; footings never pooled; not theory closed.
