# CFG39 — candidate B's harness re-run with the derived cold-mass rule

Script: `CFG39_harness_with_rule.py`, about a minute.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Collapse masses are multiplied by 30: the budget floods (Ω ≈ 1.9), SPARC's rms jumps by 0.24, and H1 fails (rc = 1).
- The main run exits 1. H1 failed on its KiDS clause, which was an artefact of my own threshold scan (below).

## What changes where

The rule adds dark mass only where a system's collapse cold mass exceeds its phantom (f_ex > 0).
- **Unchanged by construction:** CMB lensing, the forest, Cassini, and every population gate. They involve low-mass or Newtonian-owned systems, or don't read the cold mass.
- **Not re-scorable without circularity:** X-COP and the Bullet keep their rows. The rule only raises their dark mass above the as-written identity.
- **Recomputed here:** SPARC, the cold-mass budget, and KiDS.

## Results

**Controls.**
- C1: the harness's eight committed budget values are reproduced exactly from CFG11's integral.
- C2: SPARC's rms, 0.1003 at Υ 0.61 on CFG4's own weighted statistic, is reproduced.

| gate | without the rule | with the rule | verdict |
|---|---|---|---|
| SPARC (CFG4's statistic) | rms 0.1003 | **0.1012 (+0.0009)**; only UGC 2487 (S0, log M_* 11.48, f_ex 0.58) is touched | unchanged |
| budget, lenient | Ω_ph 0.188–0.219 | **+0.003 to +0.007** of leftover (0.195–0.224) vs Ω_c 0.265 | still passes |
| budget, strict (reported) | 0.229–0.266 vs 0.159 | +0.003 to +0.005 | still fails, as before |
| KiDS | — | f_ex(red) = **0** at all four lens-bin centres (log M_* 10.15, 10.45, 10.7, 10.9; post-hoc) | unchanged in fact; H1's declared clause failed on an artefact |

**H1 failed as declared.** Its KiDS clause scanned for the stellar mass where the red leftover switches on, starting at log M_* 10.00. That is below the red table's first point (10.28), where the clamped collapse mass is unphysical: the same trap CFG36 hit with dwarfs. The scan therefore reported 10.00. At the actual lens-bin centres the leftover is zero (R1, added after the main run and labelled post-hoc). The declared failure stands in the record, with this explanation.

## Standing

**The derived conservation rule costs B no gate in practice:**
- SPARC moves 0.0009 dex;
- the budget grows by at most 0.007 of Ω and stays within Ω_c;
- KiDS's lenses carry no leftover.

B's harness stays at 42/48 with the rule, but that score is inferred, not established. The declared test failed on the artefact, and X-COP and the Bullet cannot be re-scored without circularity.

**The one real cost** is UGC 2487, already known from CFG36.

Nothing here says the theory is closed.
