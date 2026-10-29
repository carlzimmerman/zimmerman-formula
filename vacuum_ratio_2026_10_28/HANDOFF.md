# VR28 continuation handoff

User target remains open: derive B relative to full gravitating vacuum
energy, without fitting the acceleration target. Parent PN28 is unchanged.
Base revision and actual inputs are in INPUTS.json; reviewed artifact and
completed-run hashes are in VERIFICATION.json. No subagents were used,
no commit/push or manuscript integration was performed.

Start with README.md, DERIVATION.md and OFFSET_AND_LOOPS.md. Do not repeat
the same equilibrium, positivity, internal-symmetry or dimensional-analysis
arguments as though they supplied a missing equality.

## Route dispositions

| Route | Current result | Resumption condition |
|---|---|---|
| PN28 equilibrium/stability | Counterfamily with arbitrary B/V survives | A new constraint must exclude an allowed amplitude or vacuum-offset change. |
| Internal symmetry | Cannot forbid a metric-volume constant by itself | Specify a symmetry involving physical metric scaling or a different global/microscopic prescription; derive its action on every term. |
| Multiplicative dilation response | Conditional U_delta and B_curv/V_sector=delta derived | Calculate delta from a specified microscopic action and establish that the equation constrains total vacuum energy, not only a sector. |
| New halo branch | Finite-radius proof, exact EOS and dense-core running derived; 15 core tests pass | A finite-gradient or observational calculation is justified after choosing this physical parent. Do not import a universal a0 or old fits. |
| Gravity | Minimal de Sitter vacuum allows every positive ratio; nonminimal example adds an inequality | Supply a motivated F_g and an independent equation rather than imposing marginality or m=H. |
| Vacuum medium | B becomes inverse compressibility; full energy is an independent datum | Derive epsilon(q), the q-to-s dictionary and the boundary/chemical-potential state, including full gravitating energy. |
| Dilaton anomaly | PCDC sector relation has negative vacuum sign and a subtraction | Supply actual spectrum, saturation, decay-constant matching and the physical uplift mechanism. |
| Quantum protection | Canonical scalar one-loop term generates new exponents | Specify additional fields/symmetry and calculate cancellation/matching. No unspecified supersymmetric cancellation is assumed. |

## Exact remaining microscopic obligations

1. Explain why the relative kinetic metric and phase-space state are the
   physical ones; PN28 has not derived them from the owner's cold-field parent.
2. Compute the vacuum response, e.g. B=q0^2 epsilon_qq(q0), together with
   V=epsilon(q0)-q0 epsilon_q(q0). Both are required; fixing a subtraction
   constant by the desired answer is circular.
3. If using the scaling branch, derive its exponent and control the generated
   potential operators. B_curv/V_sector=delta alone only renames a free input.
4. Re-derive the observable acceleration map for the actual finite-gradient
   model. The new branch has Sigma_core proportional to rho_c^(-delta/2)
   in its formal dense limit, and is not exactly the old logarithmic model.

These are open physical tasks, not a claim that every possible completion
is impossible. No concrete UV spectrum or symmetry currently supplied by
this parent fixes the needed response or offset. Inventing one to hit the
old 0.002329458 target would not resolve the user's request.

## Reproducibility

Accepted main record: run/manifest.json, status completed, 32 named checks.
Accepted protection record: run_protection/manifest.json, status completed,
8 exact checks. Contracts preserve parameter sets, software, thresholds and
resource limits. Validate using the computation-audit validator with the
repository root. Exact executed argv is in each manifest; use fresh output
directories for any justified rerun. No rerun is needed for unchanged passing
cases. SELF_REVIEW.md is explicitly an author self-review.
