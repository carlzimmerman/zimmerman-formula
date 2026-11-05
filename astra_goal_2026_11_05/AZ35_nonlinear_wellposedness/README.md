# NO VERDICT — full nonlinear well-posedness remains unproved

Lane5(a), criteria db530f4da0. Kappa = 1/2 FITTED; not theory closed.
Neither a full theorem nor a full-action counterexample was obtained.
The audit identifies a missing norm estimate behind the earlier inference
from nonnegative sound-speed squared and bounded modal growth.

On the frozen soft branch, the density/velocity propagator norm grows
linearly with wavenumber even though its exponential growth rate is bounded.
At k256,t1 the norm is138.94797; the last doubling ratio is1.9995064 and
the asymptotic coefficient agrees within8.232e-5, below the frozen1e-3 line.
But the polarization/velocity transformation removes the k dependence
exactly. This is a regularity obligation, not a verdict of full ill-posedness.

The exact pressureless characteristic test loses invertibility at t1 for
v0=-sin(a). Uniform velocity does not. This is only a principal-subsystem
caustic; local existence before the caustic and full v3s evolution are
different claims. `DERIVATION.md` gives the equations, scope and self-review.

## Executed evidence

Main passes18/18 diagnostic checks, exit0. MUTATE passes15/18, exit1:
its positive stiff branch defeats the two footing-specific linear-k
witnesses, and its uniform velocity defeats the compression witness.
All invariant, known-answer and convergence checks still pass.

| Check | Main | MUTATE |
|---|---:|---:|
| Maximum50-digit relative discrepancy | 2.05e-16 | 5.37e-15 |
| RK4 4096/8192 relative pair change | 1.30e-13 | 4.97e-6 |
| Maximum4096-step error to exact | 1.50e-13 | 5.30e-6 |
| Frozen numerical tolerance | 1e-4 | 1e-4 |
| k256 propagator norm | 138.948 | 1.38101 |

Both footings are computed separately; the dimensionless results coincide
because the unit transformation is exact. Their time units are8.89480e13s
canonical and8.09117e13s alt at L_ref24pc. These are illustrative units,
not predictions of a physical caustic time. The positive-stiff control's
gamma1 is also illustrative; it is not a new screening-length fit.

The initial characteristic-polynomial check had a SymPy symbol-identity
bug. Its original script and failed result remain saved. The corrected
determinant test changes no physical or numerical criterion; see
`IMPLEMENTATION_NOTES.md`. Final runs took under0.2s each and peaked below
77MB RSS, with one numerical thread. JSON records input hashes and versions.

## Routes and remaining obligations

1. **Frozen evolution:** the bounded-eigenvalue inference is insufficient;
   the polarization-variable repair survives. Next: a variable-coefficient
   constrained energy estimate with the actual nonlinear leaf map.
2. **Nonlinear characteristics:** exact finite-time caustic in the principal
   truncation only. Next: retain the W/Poisson forces and constraints before
   attempting an on-shell counterexample.
3. **Static/interface proof:** AZ34's coercivity obstruction stands. Next:
   establish existence, traces and source dependence in a justified relaxed
   domain, then control the moving switch interface and timelike/cap margins.

These routes remain mathematically open. This lane has executed its declared
diagnostics and reached NO VERDICT; the overall program proceeds to the
separately frozen PN-sign lane, rather than promoting these tests to a proof.

## Reproduce

From the repository root:

```sh
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ35_nonlinear_wellposedness/run.py
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ35_nonlinear_wellposedness/run.py --mutate
```

Expected exits0 and1, with separate atomic output trees. The mathematical
lane label is NO VERDICT in both; exit0 certifies the finite diagnostic
checks, not the unresolved nonlinear theorem.
