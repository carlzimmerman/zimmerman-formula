# AZ23: causal response at the critical clock endpoint

κ = ½ FITTED; not theory closed

Exploratory prerequisite, not an admitted KC1 normalization candidate. Base record checked with ls, git log and rg on 2026-11-04; latest observed commit 7b7d1a7811. K728's nominal opening was already followed by K748–749. We do not rerun their static calculation. Their time-dependent response remains uncomputed in the inspected packet.

Inputs, read only: why_4_puzzle/W4_08_positive_mond_amplitudes/formal/unified_invariant/SINGLE_FUNCTION.md and formal/critical_endpoint/RESULT.md under the same W4_08 directory. No external data or cosmological fitted values.

Question: can causal evolution at the critical endpoint select a MOND response that a static analysis misses? First decisive subproblem: solve the constrained linear scalar evolution exactly on de Sitter, retaining lapse coupling to a conserved, dilute comoving dust perturbation. This is not a stationary galaxy. No new species is introduced: dust here denotes an infinitesimal baryonic probe. No claim about nonlinear response or cutoff validity follows.

Conventions: c=1, H>0, B>0, X=k_com^2/a^2>0, alpha=2, C=6 (the inherited cusp limit). Source rho_dot=-3H rho. Start with the inherited quadratic lapse/shift action, add -a^3 rho n, eliminate lapse, and derive the forced equation. Do not divide by 2-alpha. Solve the homogeneous equation and construct its causal Green function; test source scaling before considering any normalization claim.

Gates, identical on canonical and alt footings because no footing-specific input enters:
- PASS exact-response subproblem only if symbolic residuals of two independent homogeneous modes vanish, Wronskian is nonzero for X>0,H>0, and Green initial value/derivative are 0/1.
- PASS sourced subproblem only if lapse elimination and Euler variation agree, the conserved-source particular solution has zero residual, and reconstructed lapse satisfies its original constraint.
- A finite-time linear response is not an exact square-root mass response. Grade causal selection within this linear problem FAIL if it remains linear in source amplitude. The nonlinear physical mechanism remains NO VERDICT; physical kappa NOT EVALUABLE.
- Known answer: large-X/H^2 homogeneous roots must reproduce the constant-coefficient equation with friction 3H and restoring frequency squared 2H^2.
- MUTATE: dropping X_dot in the kinetic coefficient must produce a nonzero mode residual. A false rational witness in Lean must be rejected; true finite witnesses must compile, without sorry, custom axioms or native_decide. Lean witnesses are not a certificate of the physical mechanism.

All comparisons use exact symbolic or rational zero tests, with no numerical tolerance and no observation grading. Free H,B,k_com, source amplitude and initial time are symbolic, unselected/FITTED if assigned; inherited F,c1,c2,m and cusp width remain unselected. This lane supplies no b=1 constraint. Output includes both-footing verdicts, checks, input hashes and tool versions. Single-process algebra only. No scan, download or push.
