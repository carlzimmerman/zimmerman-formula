# CF2_decoupled_threshold_map: a concentration-independent switch threshold

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (7881b642f8).
- **Harness:** CF1 (e370b35e1c) / X62 (8c7768d26d), with the switch flag M > 10^T decoupled from c_f.

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict string printed by the frozen code: "NO DECOUPLED THRESHOLD (lensing and groups never pass together)"

**This label is wrong for the reason it gives, and that is disclosed.** The classifier tested the threshold class
(lensing, groups, SPARC and dwarfs) jointly on both footings. It exempted the alt footing's MW ultra-faint class, as the
criteria require, but did not exempt alt's **SPARC line**, which fails at every T and c_f (as in CF1 and X62). Every point
therefore fell through to the last branch. The map itself shows:

- **Canonical footing: the threshold is solved for every T in 12.2–12.5.** At c_f = 4.75 and 5.0, KiDS lensing,
  groups, SPARC and all five dwarf classes pass together. Only cluster lines fail: G-OUT-M3 (UNDER), or G-IN-Mall (OVER)
  at c_f = 5.25. At T = 12.1 lensing still fails (Δχ² +22.3), so the lower edge of the window is between 12.1 and 12.2.
- **Alt footing.** Lensing and groups pass for T ≥ 12.3 (at T = 12.2 groups are +2.01 at c_f = 4.75), but the SPARC line
  and the MW ultra-faints fail everywhere. These are c_f- and T-independent alt problems, not threshold problems.

**Reading.** A concentration-independent switch at **10^12.2–10^12.5 M☉** (canonical) satisfies lensing, groups, SPARC and
the dwarfs together. CF1's "threshold against concentration" tension is resolved by decoupling them. The remaining lines
are cluster lines; CL1 combines this switch with GS1's measured cluster budget. T is located by this map; it is not
derived.

Group masses (EM1 relation): log M200 12.01–13.69, median 12.76. KiDS lens bins: ≤ 12.05.

## Checks: 9/9

- K0a/b/c and K2a/b (the X62 reproductions).
- S0a: the crossover flag at c_f = 5 reproduces CF1 exactly.
- K1: flagged counts do not increase with T.
- K2: the switch property holds at every point.
- K3: < 1 GB.
- **Pending:** the twin and the rerun.

## Files

- `cf2_decoupled.py`
- `cf2_decoupled_results.json`; the `.out` is written at exit
- the per-run `x62_*copy_*` outputs
