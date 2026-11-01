# Static response: conditional diffuse endpoints, unresolved compact branch

`static_run_002` preserves the full frozen experiment. Its runner status is
**failed**, because the contract required all requested responses and all
four refinements to pass. It is nevertheless a valid evidence record with
all declared result artifacts present and unchanged input hashes. The
manifest validator passed on the current inputs. Do not describe this as
an entirely passing numerical experiment.

All six original PN28 baselines pass, as do all twelve zero-forcing controls.
The sixty response records contain 24 passing solutions (12 zero and 12
nonzero), 9 nonconverged attempts at fraction .25, and 27 explicitly unattempted
continuations after those failures. Three diffuse families reach their
prespecified final forcing `mb/M=.05, a/R=.5`:

| Baseline psi_c | epsilon | C_q/C_q0 | n_c/n_c0 | r_q/r_q0 | R/R0 |
|---:|---:|---:|---:|---:|---:|
| .95 | .0001 | .82433036 | .38050438 | 2.16641493 | .98925523 |
| .95 | .01 | .84043812 | .49274229 | 1.70563423 | .99076454 |
| .99 | .01 | .80379111 | .32368323 | 2.48326462 | .97960771 |

These mass-conserving equilibria have lower central dark density and lower
quarter-density column, larger quarter-density core radius, and slightly
smaller total matter radius. They therefore do not realize a simple increase
of the core column under the specified external potential. This is a static
branch result; it does not show that baryonic assembly dynamically takes
an initial halo to these equilibria.

The `.99,.01` diffuse endpoint's longer-domain/tighter-tolerance repetition
passes; its maximum relative change among density, matter radius and column
is `2.92e-7`, below the frozen `5e-5` line. The other three predetermined
refinements were unavailable because their endpoints did not converge.

The two weak-diffuse `.8` cases and weak-diffuse `.99,.0001` case failed to
converge on the first nonzero step. All six compact families also failed on
that step. Six failures hit the collocation node budget and three encountered
a singular Jacobian, with overflow warnings retained. These failures neither
prove absence of a branch nor establish instability. Resolving them would
require a separately declared numerical continuation study, for example
smaller intermediate steps with unchanged endpoints; this experiment did
not silently change its frozen steps or initial guesses.

Across the twelve successful nonzero states, the largest errors are:

- dark mass quadrature relative error: `2.55e-8`;
- independent total enclosed Poisson mass error: `3.35e-8`;
- integrated scalar balance: `9.31e-11`;
- finite-difference anisotropic stress balance: `8.10e-8`;
- full virial including external Plummer virial: `1.36e-11`;
- self-gravity potential/force energy equivalence: `1.29e-8`.

The analytic Plummer source controls and wrong-source-sign negative controls
pass. The latter rejects an incorrect mass balance, not a separately solved
wrong-sign model. Edge asymptote ratios are reported as diagnostics. They
are not interval or uniform error bounds.

`static_run_001` failed only at strict JSON serialization after processing
the same scientific cases, because a failed BVP had a NaN diagnostic. Its
logs and original source remain intact. `STATIC_AMENDMENT_A1.md` documents
the serialization-only wrapper for run 002; nonfinite diagnostics are null
with explicit original-value paths. No equations, forcing, thresholds or
branch choices were changed for that rerun.

Run 002 took about 2.33 seconds, used one configured numerical thread, and
reported macOS peak RSS 202,604,544 bytes. Its five artifacts total below
0.5 MB. No production simulation or empirical fit was run. This is the
author's self-audit; independent algebra/code review is separate.
