# IC47: auxiliary solve repaired; interface convergence unresolved

Status: OPEN. This is a numerical improvement to the same IC46 candidate,
not a completed field theory, stability certificate, or no-go theorem.

At starting commit a404faef4, IC46's centered auxiliary solve stalled at
1.96569e-11 against its unchanged 2e-12 scaled-residual tolerance. Supplying
a symmetric finite-difference Jacobian with absolute increment 1e-8 makes
all four IC47 runs complete. Neither the action nor the boundary equations,
root acceptance tolerance, canonical evolution, or interface diagnostics
was changed. No momentum or interface projection was added.

All runs cover dimensionless time 2e-7 at patch width 3e-5:

| nodes | time step | Jacobian increment | maximum lapse residual | maximum inactive-clock residual | final interface reaction |
|---|---|---|---|---|---|
| 7 | 1e-8 | 1e-8 | 2.38e-10 | 5.64e-10 | 4.46e-6 |
| 7 | 5e-9 | 1e-8 | 3.25e-10 | 9.26e-10 | 1.94e-5 |
| 9 | 5e-9 | 1e-8 | 1.61e-9 | 4.61e-9 | -7.02e-5 |
| 7 | 1e-8 | 5e-9 | 2.85e-10 | 6.28e-10 | 4.46e-6 |

The interface reaction changes sign under spatial refinement and its magnitude
increases under time refinement. The conditional gradient-jump residual also
fails to improve. Thus these runs do not establish a convergent interface
solution. The small bulk residuals show that auxiliary root failure can be
removed independently of this unresolved issue. Halving the Jacobian increment
barely changes the seven-node final reaction, so this specific derivative
increment is not sufficient to explain the interface error.

Next calculation: condition the canonical fields and the endpoint evaluation
of W, then compare against higher-precision differentiation on identical data.
If the reaction discrepancy survives precision control, solve the full moving
interface boundary problem instead of supplying finite Taylor endpoint data.
Neither outcome may be assumed in advance. Full Dirac closure, PPN,
cosmological viability and the original exact general-source MOND requirement
remain separate outstanding obligations for this same action.

## Reproduction and results

From the repository root:

```
python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic47_jacobian_evolution.py > /tmp/ic47_jacobian_results.json
```

Exit 0: all numerical runs completed. Full output is preserved in
`ic47_jacobian_results.json`, including per-time diagnostics and wrapper hashes.
It depends on IC46's existing symbolic modules and stored initial data; the
three recorded hashes alone are not a complete dependency manifest.

From this directory:

```
python3 -m unittest test_ic46_two_phase_evolution test_ic46_centered_evolution
```

Exit 1: four tests, three pass, one fails at the original centered auxiliary
solve. That regression is preserved. IC47 would additionally fail its initial
reaction threshold of 1e-7 (observed 6.12e-6); completion of the new numerical
run must not be presented as passing that regression.

The latest Fable commit a404faef4 acknowledges L52 normalization and ephemeris
overstatements. Its claimed later constraint analysis has not been imported
as evidence about this different action.

Mathbox computation-audit discipline is used here: report bounded runs,
unchanged acceptance criteria, failed convergence and explicit limitations.
