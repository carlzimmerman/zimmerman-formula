# A false positive in the Hermes dust objective

The unchanged `hermes_push/search/objective.py` accepts a synthetic input with total loss below `1e-12`, although its own density does not redshift as dust. The execution is a successful reproduction of a scientific-gate failure. No optimizer is run; no coefficient file, action, or physical history is constructed or modified.

At `objective.py:70-71`, the dust gate tests only the slope of a least-squares line through `log(rho)` versus `log(a)`. Slope `-3` does not imply that all points lie on that line. The claim that the residual vanishes exactly when dust redshifting holds (`objective.py:54`, `SEARCH.md:4-7`) is therefore false.

Set the synthetic input's constant `q=.5`, `d/U=.45*a^2`, and `s0=1.001`. The objective's density simplifies exactly to

    rho(a) = U0*a^p / (1 - .225*a^2).

Choose `p` to subtract the regression slope of `-log(1-.225*a^2)`, and choose `U0=.78*(1-.225)` to retain the objective's normalization. Every parameter remains within its declared bounds. The resulting gate loss is approximately `8.88e-16`; all other coded gate penalties vanish. Nevertheless `a^3 rho` spans approximately `0.68051005` to `0.78`: a 14.62% maximum-to-minimum variation. The recorded result contains the actual values and all ten samples.

The minimal repair to this implementation would test residuals of constant `a^3 rho` (or the corresponding local conservation equation), rather than only a fitted slope. That repair has not been applied here. Even a repaired algebraic density gate would not establish a solution of the same-action background equations, pressureless stress, gradient criticality, an attractor, or observational viability.

This is an implementation counterexample, not a replacement coefficient history. The name `constant_charge_check` refers solely to the necessary `a^3 rho` constancy claimed for independently conserved pressureless density; it is not a calculation of the clock's Noether charge.

`audit.py` imports the original objective directly and independently verifies the simplified density. `run_001/manifest.json` pins that source and this audit, records execution bounds and dirty Git HEAD, and hashes the resulting artifact and logs. Computation-audit and proof-audit skills were used to separate successful execution from the failed scientific interpretation. No universal mathematical or physical no-go claim follows.
