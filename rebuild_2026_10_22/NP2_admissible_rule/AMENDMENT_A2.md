# NP2 Amendment A2, 2026-11-03, written AFTER a first, aborted controls run, BEFORE any real-data fit

**Disclosure.** The first `controls` run was started under FROZEN_CRITERIA + A1 and stopped when its processes passed the 1 GB RSS cap (1.6 GB). By then these control numbers had been read; they are the reason for this amendment. No real-data fit, gate, Stage 3 card or label has been computed.

What the aborted run showed:
- Control 1 (known answer): X-COP +0.4675, LT −0.0252: OK. Control 8 (Υ loader reproduces BF1's ST and SH at 0.5): OK.
- Control 3 (checker): flags the planted bump (3287 violations) and NP1's frozen L3 canonical rule (4247; end to end 30 of 50 dwarf rows, 2 of 2 IC 1613, 173 SPARC points, matching NP1's post check); passes the zero rule. OK.
- Control 2 (zero-weight rule vs RQ3's law card): **failed as frozen**, for two reasons that are not differences between the rule and the law:
  - 21 rows read NOT COMPUTABLE for the zero rule: A15-A17 and B1 because the candidate receives NaN gas or r there (NP1's frozen design, FROZEN_CRITERIA C5: those rows stay NOT COMPUTABLE), and B4-B20 because the control runs with `--no-keys`.
  - C1's Z differs by 7.6e-5 at Z = 16491.96, a relative 5e-9 floating-point difference between the W3 wrapper's form of the law and RQ3's own form.
- Control 4 on L5 canonical, planted N0: gates 3-4 pass (SPARC 0.010 against 0.195).
- Control 7 on L5 canonical, planted N0: the fit converged on the constraint set but the checker found 47 050 violations (train rows: 877 stars-only, worst slope −0.55; wide box: 15 572, log y above the constraint box). The planted form (1 + f) log1p(1/y) is itself inadmissible on 80 % of train rows along stars-only (its own slope < ε) and 36 % at fixed share, far beyond the high-y corner the criteria anticipated. A noise-free fit to it is pulled against the constraint at the data and dips between constraint points.

## Changes
1. **Control 2 comparison.** Rows the zero rule reads NOT COMPUTABLE because the candidate is handed NaN inputs (RQ3 reports "candidate returned non-finite"), or because keys were not run, are listed and skipped; every other row must match RQ3's `results/law.json` in label, and in Z and value to a relative 1e-6 (|Δ| ≤ 1e-6 · max(1, |reference|)).
2. **Enforcement pool (C1).** The active set now runs over C (as frozen) plus a refinement set R, all train-only or synthetic: the fit's own train rows' leaves, a Sobol set of 2 × |C| points in the constraint box (seed 20261105), and a Sobol set of 2 × |C| points in the checker's wide box (seed 20261106). The checker keeps its own wide Sobol set (seed 20261104), every holdout row, every CX1 row and the end-to-end test; none of those enter the fit. Round cap 80 (was 40) for the larger pool.
3. **Working-set cap.** At most 4000 functionals in the working set (memory, 1 GB RSS cap); new violators are added 500 per round (A1 said 1500). Hitting the cap with violations left = not converged → UNDETERMINED (INADMISSIBLE).
4. **Control 7 replaced.** Its planted form was not admissible, so it couldn't test the solver. New control 7, run per arm and footing in mode F: planted **g = law(g_b, a0 (1 + 0.5 f))**, noise-free and at SPARC's errors (NP1's draw), on train and every point holdout line. It is admissible: along stars-only, d g/d g_b ∝ g_b/2 + a0(1 + 0.5 f) − 0.5 a0 f = g_b/2 + a0 > 0; along gas-only a rises too. The fit must converge, pass the full C4 checker, and pass gates 3 and 4. The old control 7 on (1 + f) log1p(1/y) N0 is still run and reported, and not gated.
5. A smoke run of the new control 7 form (L3 and L5, canonical, before this amendment, outside the committed outputs) converged with no active constraint and no checker violation in ~70 s, RSS 0.77-0.84 GB.

Everything else is unchanged: the constraint (S_v ≥ 0.05 along stars-only and gas-only), the λ grid, mode U, gates, labels and controls 1, 3, 4, 5, 6, 8.

κ = ½ FITTED; not theory closed.
