# Independent review of the atomic energy selector

**Normalized claim and verdict: proved as written**, for I2's finite affine variational problem, I3's fixed-coefficient model, and I4's explicitly conditional fixed-population/fixed-mass response. This verdict does not verify the physical premise that a particular framework action couples to the whole atomic rest mass, or extend the theorem to renormalized QED.

Reviewed artifact: `fine_structure_puzzle/atomic_bridge/coordinator/ATOMIC_SELECTION_CLAIM.md`, SHA-256 `0fe094a27378702b5c8d9f42d6dade2b520712348b496c5981603898c37e3e9a`. Parent FSP-001, work package FSP-002, base Git `3c01aa2861bf576f4c2d942251eb9d2f89cae108`, dirty. Review date 2026-10-18. The reviewer received the raw claim and request to rederive the critical inequality and sensitivities, not the coordinator's separate conclusion or implementation. No author code was read or run for this review.

## Claim card and dependency graph

The mathematical objects are real \(\alpha\) in an open interval, one common alpha-independent set \(\mathcal D\) of normalized trial states, finite real trial forms \(h_\psi+\alpha v_\psi\), and a finite ground-energy infimum on that interval. The conclusion is concavity, hence no strict interior local minimum. Additional objects are positive fixed composition weights and a differentiable scalar map, or fixed-temperature density matrices with well-defined entropy/energy and the stated finiteness regularization.

The dependency chain is:

1. Common trial set + affine energy for each trial state → pointwise lower bound at each endpoint → infimum inequality → concavity.
2. Concavity + two-sided interior neighborhood → absence of strict local minimum; second differentiability → nonpositive second derivative.
3. Fixed positive population + locally monotone alpha map → no isolated matter-energy minimum; at a smooth stationary point with nonzero alpha derivative, the scalar Hessian inherits the sign.
4. I3 uses only \(D>0\) and ordinary differentiation.
5. I4 uses a specified positive atomic mass and \(v^4=G a_M M\), held \(G,a_M,N,m_e,m_p\) fixed; logarithmic differentiation gives the response.

All arrows after the stated variational definition are internal proofs. The Coulomb hydrogen spectrum and the framework's macroscopic source matching are model inputs, not independently established by this review. NIST numerical constants are irrelevant to the symbolic checks and were not re-audited.

## Independent derivations

Let \(x=t\alpha_1+(1-t)\alpha_2\), \(0\le t\le1\). For every *same admissible* trial state,

\[
h_\psi+xv_\psi=t(h_\psi+\alpha_1v_\psi)
 +(1-t)(h_\psi+\alpha_2v_\psi)
\ge tE(\alpha_1)+(1-t)E(\alpha_2).
\]

The right side is independent of the trial state, so its lower bound survives the infimum over \(\mathcal D\). Thus \(E(x)\ge tE(\alpha_1)+(1-t)E(\alpha_2)\). The direction is correct; taking an infimum of affine functions produces concavity.

If an interior point \(\alpha_*\) were a strict local minimum, choose sufficiently small \(h>0\) with both \(\alpha_*\pm h\) inside its neighborhood. The two endpoint values would each exceed \(E(\alpha_*)\), contradicting the midpoint inequality. This proof does not require an attained ground state, differentiability, a nondegenerate level or analyticity. At a twice-differentiable point, the same midpoint inequality divided by \(h^2\) gives \(E''\le0\).

A fixed positive sum preserves this inequality, and adding a constant or a linear function does too. An alpha-independent variational entropy term can simply be included in \(h_\rho\), so the stated finite canonical Gibbs problem obeys the same proof. The source correctly excludes the unregularized divergent atomic partition function.

For a positive fixed population \(n\), differentiating the scalar composition gives

\[
{d^2[nE(\alpha(\phi))]\over d\phi^2}
=n\{E''(\alpha)(\alpha')^2+E'(\alpha)\alpha''\}.
\]

At a smooth stationary point with \(\alpha'\ne0\), stationarity implies \(E'=0\). The remaining term is nonpositive. A positive healthy scalar kinetic normalization does not reverse that sign. The stated exception \(\alpha'=0\) is necessary; for example, composing a monotone energy with an independently extremized coupling function can produce a minimum. It does not derive the value built into that coupling function.

For I3,

\[
E'=C-2D\alpha,\quad E''=-2D<0.
\]

The only positive stationary point when \(C>0\) is \(C/(2D)\), a strict maximum. For \(C\le0\), the derivative is negative at every positive alpha. A boundary value alpha=0 is outside an interior positive-coupling selector and does not alter the claim.

For I1 and I4, independently set \(S=m_p+m_e\), \(\mu=m_pm_e/S\), and \(f=S-\mu\alpha^2/2\). Then

\[
\partial_{\ln m_e}\ln\mu=m_p/S,\qquad
\partial_{\ln m_p}\ln\mu=m_e/S,
\]

so the stated hydrogen-length sensitivities follow from \(a_H\propto(\mu\alpha)^{-1}\). Also \(M=Nf\), \(v=(G a_M Nf)^{1/4}\), and at fixed masses

\[
{\partial\ln v\over\partial\ln\alpha}
={1\over4}{\alpha\over f}(-\mu\alpha)
=-{\mu\alpha^2\over4(S-\mu\alpha^2/2)}.
\]

This requires \(f>0\) and lies within the stated weak-coupling nonrelativistic regime. Binding energy lowers the rest mass, so the negative sign is consistent. It is a derivative of a family at fixed atom count, not an extremization equation for alpha. Allowing alpha-dependent proton/electron masses introduces extra derivative terms; the source explicitly assigns that question elsewhere.

## Obligation matrix

| Obligation | Result | Reason |
|---|---|---|
| Same alpha-independent domain | Passed | Explicit hypothesis; necessary for mixing endpoints in one trial state. |
| Finite infimum and well-defined forms | Passed | Stated, with each expectation interpreted as a finite trial form. |
| Infimum inequality and sign | Passed | Derived directly above. |
| Interior, cusps and absent minimizer | Passed | Midpoint proof covers all three; no eigenstate is needed. |
| Scalar stability | Passed | Chain rule with stationary \(E'\) and nonzero \(\alpha'\). |
| Thermal extension | Passed | Conditional on stated finite Gibbs variational problem. |
| Fixed-core stationary attempt | Passed | Exact quadratic derivative and positive-domain check. |
| Reduced-mass and BTFR sensitivities | Passed | Direct independent logarithmic differentiation. |
| Full QED and variable composition | Out of scope | Explicitly excluded in the source. |
| Physical framework source matching | Conditional | The source presents it as an antecedent, not a demonstrated result. |

No gap was found in the stated mathematical conclusions. The strongest safe physical statement is the one already restricted in the claim: ordinary matter energy in the finite affine Coulomb approximation cannot provide a strict interior stable alpha selector by itself. The cheapest further check is an explicit non-affine mass/coupling/vacuum action, not more numerical minimization of the same affine family.

Review provenance: independent subagent derivation within the current task, using the proof-audit skill; no numerical computation required. The raw reviewed file's SHA-256 was measured with `shasum -a 256`. Any later edit to that file needs a freshness check before reusing this review.
