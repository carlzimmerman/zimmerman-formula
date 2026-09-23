# Proof audit

Primary verdict: **proved as written**, for the scalar conservative Thomson
process and bounded continuous radial profiles specified in THEOREM.md.
Reviewer/author: Codex, same session. This is self-review, not independent
peer review. Qwen's earlier unsupported coefficients are not proof inputs.

The exact target is Var(D)>=2*(2d)^(3/2)/(9*sqrt(M)) for every continuous
0<=kappa<=M, M>0, d=integral r*kappa>0, central source, unit ball and speed.
Its variables are real; there is no asymptotic approximation, finite profile
scan, or observational fitting.

Dependency graph:

    bounded rate -> nonexplosion + exit tail -> E[T^2]<infinity
    kernel integrals + F'=-k/2 -> mean martingale
    mean martingale + square generator + exit tail -> variance bracket
    z^2 generator + integral2z=1 -> eliminate Qz -> variance >= 2Qs/3
    Lipschitz radius + nonnegative k*r^2 -> Qs >= integral k*r^2
    opacity cap + fixed mean + signed comparison -> radial moment bound
    combine -> claimed variance bound -> relative bound + physical units

| Obligation | Status | Evidence |
|---|---|---|
| Process and observable unchanged | Passed | Section1; D=T-Z, all photons |
| Escape and finite second moment | Passed | Section2, geometric tail with exp(-2M) |
| Correct kernel normalization/moments | Passed | Section3 and computed exact integrals |
| Mean normalization, including ds=2r dr | Passed | Section3; F(0)=integral r*kappa |
| Squared jump versus generator sign | Passed | Section4; independent generator-of-Y^2 check |
| Passage to unbounded exit time | Passed | L2 domination and monotone convergence, Section4 |
| Occupation identity and boundary sign | Passed | Section4; e in[0,1], no factorization |
| Nonmonotone radial trajectories | Passed | Section5; Lipschitz chain rule handles backtracking |
| Constrained radial inequality | Passed | Section6; pointwise signed comparison |
| Discontinuous comparison not assumed admissible | Passed | Section6; used only as integration comparator |
| d=0 and d=M/2 endpoints | Passed | Sections1,6 plus exact checks |
| Physical units and cap convention | Passed | Section7 plus exact substitution |
| Independent peer review | Not addressed | Same-author self-review only |
| Optimal constant | Out of scope | No equality/attainment claim |
| Literature priority | Not addressed conclusively | Bounded primary-source search only |
| JWST observations and model applicability | Out of scope | No measurements used |

Adversarial checks included: negative z in the physical interior; zero opacity;
saturated mean forcing the uniform cap profile; arbitrary radial backtracking;
large M with very loose but finite escape tail; rate zero on subintervals;
isotropic scattering substituted through the same integration/elimination
code; an erroneous generator-difference used as squared jump; and the previous
uncapped family, whose diverging M makes the present bound compatible with
vanishing relative variance.

The isotropic negative changes E[mu^2] from2/5 to1/3 and changes the boundary
coefficient in the variance identity from11/9 to1. Its residual against the
fixed Thomson identity is2*(e-1)/9. This properly rejects the Thomson
certificate; it does NOT assert that isotropic transport violates the final
lower bound. The coefficient2/3 survives that change.

All19 checks in certified/result.json pass. The v2 computation manifest
records input hashes, command, environment, resource caps and outputs and
validates against the repository. The proof is in THEOREM.md, not in a count
of passed checks. The code performs no random sampling. Algebra checks do
not substitute for the written stochastic and inequality arguments.

Proofreading covered all newly written theorem equations, quantifiers,
references and unit conversions. No unresolved mathematical gap was found
under the stated hypotheses. No unrelated research or saved Qwen artifact
was changed. Independent review remains the cheapest way to challenge a
possible shared reasoning error before using this result as a research claim.

Reproduction from repository root:

    /opt/homebrew/Caskroom/miniconda/base/bin/python3 real_research/reviews/jwst_opacity_cap_theorem_2026_09_22/verify.py

The preserved certified run was produced using the computation-audit bounded
runner with contract.json and both THEOREM.md and verify.py as hashed inputs.
Avoid editing those inputs in place after certification; use a new revision
and output directory for any later mathematical correction.
