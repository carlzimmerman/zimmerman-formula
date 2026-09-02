# CDE-L4C PPN gate — corrected verdict: `alpha_3` OPEN (2026-09-01)

## Retraction

The previous file identified a normalized difference between the instantaneous constraint response `1/k^2` and a luminal scalar response `1/(k^2-omega^2/c^2)` with the standard PPN parameter `alpha_3`, and reported `alpha_3=-1`. That identification was not derived.

The calculation did establish:

- the principal CDE-L4C constraint response is `omega`-independent;
- its toy scalar denominator differs from a luminal retarded denominator at order `w^2`;
- the chosen normalization of that difference is `-1`.

It did **not** calculate:

- the complete boosted `g00`, `g0i`, and `gij` solution through the required PN orders;
- backreaction of every constraint and multiplier;
- the moving matter solution and ordinary-matter equations;
- the transformation to standard PPN gauge;
- the coefficient matching which defines `alpha_3`.

An instantaneous constraint is not, by itself, a proof of a nonzero preferred-frame PPN coefficient; general-relativistic lapse and shift constraints illustrate why the full gauge-constrained metric solution matters.

## Current CDE-L4C status

The principal Dirac and exact-MOND results remain scoped results. The claimed PPN kill is withdrawn. CDE-L4C is **OPEN at PPN**, and the full boosted 1PN solve is the next unavoidable calculation for this branch.

Executable provenance audit: `cde_l4c_ppn_alpha3.py`.
