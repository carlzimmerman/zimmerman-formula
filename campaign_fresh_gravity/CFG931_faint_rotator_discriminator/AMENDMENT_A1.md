# CFG931 AMENDMENT A1 (POST-FREEZE, 2026-10-20, BEFORE ANY RUN): recovery condition, two implementation details, one INFO line

Frozen criteria: cad92ca1c. This amendment was written while coding the script, before the script was run and before any
residual, d_K, d_E, lever or class of this lane was computed. Nothing seen since the freeze motivates it except the frozen
text itself.

## A1-1. "When N allows" for the I-30 recovery must include the lever gate

**The problem in the frozen text.** Section 6 grades the lever gate (z(Δ_ref) ≥ 2) BEFORE the E/K rules. The I-30 injection
moves only group (i), so it cannot change Δ_ref = E(iii) − E(ii). If the lever gate fails, I-30 gives NOT DIAGNOSTIC (NO
LEVER) whatever N is. The frozen definition of "when N allows" (data gate + 2.84 σ(d_K) ≤ 0.30) would then call that a
control FAILURE and withhold every class. That outcome would come from the class order, not from the pipeline or from N.

**The change.** Recovery of I-30 is required where: the data gate passes, **the lever gate passes (z(Δ_ref) ≥ 2)**, and
2.84 σ(d_K) ≤ 0.30. Elsewhere the I-30 outcome is reported as "not recoverable here", with the failing gate named. The same
condition governs S1 (the shuffle requirement). The pipeline requirement (d_K moves by exactly +0.30 wherever an eligible
cell exists) is unchanged.

## A1-2. Implementation details the frozen text left open

- S2 (permutation p on the real data) uses 1000 draws with rng 9312. S1 keeps rng 9311.
- Exit codes: 0 = K-stage passed and every required control in that mode was met; 1 = a required MUTATE control failed;
  2 = a K-test failed (lane stops, no class).
- V4 (CFG828 dwarfs): the per-dwarf error is σ_Δ = 2·eso/(so·ln 10), from CFG824's symmetric σ error.
- The bootstrap is vectorised (same 4000 draws, rng 931, one fresh generator per footing × split × variant, groups drawn in
  the order i, ii, iii).

## A1-3. One INFO line (no class weight)

UGCA 444 (M* 6.0e6) is the only SPARC rotator with M* < 1e7 whose rotation curve reaches g_bar < 10^−11.5, but none of its
points pass errV/V < 0.10. The script prints its cell means Δ in W **without the point cut**, next to the high-M* (≥ 1e7)
rotators' cell means (with the cut) and the matched-M* dwarfs' cell means, per footing. One galaxy, errors ≥ 10 % per point:
INFO only, never graded, never part of any group.

κ = ½ FITTED; footings never pooled; not theory closed.
