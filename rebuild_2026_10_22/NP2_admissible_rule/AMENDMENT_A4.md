# NP2 Amendment A4, 2026-11-03, POST-CONTROL, before any real-data fit

**Written after reading the L3 controls** (`np2_controls_L3.out`); the L5 controls were still running. No real-data fit, gate, card or label has been computed.

## What the L3 controls showed
Base controls ALL OK. In both L3 cells, every control passes except one:
- Planted (1 + f) log1p(1/y), **noise-free (N0)**: no λ is eligible (every CV fold fit hits the 2000-functional cap), so λ = 32 is forced and the final fit hits the 4000 cap without converging (19-27 active, 88-92 thousand checker violations: the rule is not admissible). Gates 3-4 pass at alt and **fail at canonical** (gate 3 X-COP +0.095). By the frozen rule, L3 canonical reads UNDETERMINED (controls) in both modes.
- The same form at SPARC's errors (N1) is recovered in both cells (λ 4, converged, gate 3 SPARC 0.141 / 0.144, X-COP +0.001, LT +0.07-0.08). The class boost fails gate 3 as it must (0.290). The admissible plant law(g_b, a0(1 + 0.5 f)) is recovered noise-free and noisy with no checker violation. MUTATE bites in modes F and U through X-COP (+0.45 to +0.50).

## Reading
The N0 control asks an admissible fit to reproduce, exactly, a form that is inadmissible on 80 % of train rows (A2). The constrained fit can't, and the fit that comes back isn't even admissible, so this cell tests the projection against data it is built to refuse, not the machinery's ability to recover a leaf function. The criteria's own premise for it ("not admissible only at the high-y end") was wrong.

## Change
Control 4 for the label is **planted N1 only** (plus the admissible plant N0 and N1 of control 7, unchanged). Planted N0 is still run and reported in every cell. Every verdict is printed twice: the A4 label, and the label under the frozen control 4, which is UNDETERMINED (controls) in any cell where planted N0 fails. Both are carried to the README.

Nothing else changes.

κ = ½ FITTED; not theory closed.
