# Independent audit: conditional weak compactness

**Verdict: the stated on-branch sequential closure is proved. Full-switch
closure also follows under the same strong clock/auxiliary compactness
and a bounded multiplier, by passing KKT rather than a weak nonlinear
maximum. Neither statement constructs solutions or proves uniqueness.**

Reviewed `pf14/NATIVE_COMPACTNESS.md`, SHA256
`cae66fce913533683ce6c7aafa2f32862d0bc7b8e1ca88e0000a9d5d65869835`.
Independent delegated audit, 2026-11-06.

Assume a common domain, uniform local W1,infinity bounds for phi,A,Pi,
compact positive-clock/cap bounds, strong local C1 metric convergence,
and strong local L1 convergence of dphi. Take locally uniform limits
of the fields and weak-* limits of their bounded derivatives. To retain
the PF13 requirement dphi in BV, also impose a uniform local spacetime
BV bound, or separately require the limiting gradient to be BV. Strong
L1 convergence alone would not preserve that property. The actual file
names uniform BV as a sufficient compactness input; that input is still
an estimate to prove in an existence construction.

## Null-Lagrangian source

The exact distributional identity for Lipschitz A,Pi is

    A_t Pi_x-A_x Pi_t=partial_t(A Pi_x)-partial_x(A Pi_t).

Uniform A convergence and weak-* bounded dPi convergence pass each
product on the right. Thus the Jacobians converge distributionally to
the Jacobian of the limiting fields. They are uniformly bounded in
L-infinity, so the convergence also identifies their weak-* bounded
limit and rules out any surface delta in this source. No strong dA or
dPi convergence is required. This is a direct product/divergence proof,
not a claim that arbitrary weak derivative products are continuous.

## On-branch equations

Compact clock margins make r,n continuous locally Lipschitz functions
of dphi and the metric. They converge strongly in every finite local Lp
under the uniform bounds. The same holds for H,h and the on-branch
stress. In each wedge equation, dphi is strong L1 and the other
derivative is bounded weak-*, so the products pass. The base current
passes strongly, the topological current passes weak-*, and the scalar
divergence equation passes. The explicit sources converge strongly.
The strict Q margin passes a.e. The equations use no inverse of a
differentiated BV constraint.

Strong C1 convergence makes connections and their quadratic terms
converge uniformly locally. Their derivatives pass distributionally;
the metric factors multiplying these derivatives can be handled by
integration by parts with the same C1 convergence. Consequently every
Einstein component passes to the constitutive limiting stress. It is
important that all Einstein equations were imposed on the sequence.

## Full-switch extension under these same strong hypotheses

Let mu_k be nonnegative and uniformly bounded. In this field class its
bound also follows from D_k=wedge(dphi_k,dPi_k)/(E_k r_k), the compact
bounds and mu_k=D_eff,k-D_k. Extract mu_k weak-* converging to mu. Since
Q_k=A_k r_k converges strongly in finite Lp, the conditions

    Q_k>=1, mu_k>=0, mu_k(Q_k-1)=0

pass to Q>=1, mu>=0, mu(Q-1)=0. The algebraic A equation passes by the
same strong-times-weak argument, giving D=D_eff-mu. These identities
imply the full-switch max relation a.e.; it need not be obtained by
applying max to an unidentified weak limit of D alone.

Every multiplier term in J and T is mu_k times a strongly convergent
bounded coefficient (A_k n_k or Q_k n_k tensor n_k). It therefore
converges weak-* to the correct constitutive term. The remaining terms
converge as before, and all equations pass. Stress convergence is now
weak-* rather than necessarily strong, which is sufficient for the
Einstein distributional limit.

Thus a separate obstacle obstruction is absent under these strong
clock/Q compactness hypotheses. Weak convergence alone, without strong
Q, would not supply this KKT passage. This extension does not claim
that the required compactness persists at or beyond breakdown.

## Relation to the earlier loop and to uniqueness

The collapsing-loop test remains a valid one-time derivative-forcing
test. Its forcing is not the original bounded spacetime Jacobian.
Conditional spacetime compactness fixes the latter's limit and disallows
treating a loop impulse as an independently selectable scalar source.
It does not prove that every one-time loop is dynamically impossible,
or that two different limiting histories cannot exist. A closed graph
under a specified convergence is neither a construction of a convergent
family nor a uniqueness estimate between solutions.

## Revised-file check and metric-class qualification

Read the final revised file, SHA256
`25a2e64daa039a1f292b8f69c76978a44707beb49b4e0f7167dc282883378d02`.
Its explicit uniform BV input and strong-Q full-switch passage agree
with the derivation above. The distributional equations are sequentially
closed under the stated convergence.

For closure **inside the exact PF13 C1 intersect W2,1 metric class**, one
must additionally retain that class for the limit; strong C1 convergence
alone does not preserve integrability of all individual second weak
derivatives. The file explicitly retains the limit curvature class in
its full-switch paragraph; the same qualification applies on branch.
This does not obstruct distributional Einstein convergence with a C1
limit, but it matters for invoking the separate W2,1 weak-Bianchi audit.
No unproved second-derivative compactness is included in this verdict.

Final follow-up: verified the amended file SHA256
`d0ab5c95409be6e953efbc75bf84b68535ffcff60515f2d9641b1549ae7e7a87`.
Its top-level hypotheses now explicitly retain the limiting metric's
C1 intersect W2,1 curvature class for both branches. With that
qualification and the uniform BV input, the final actual-file verdict
is **proved as written: conditional sequential closure**, including the
strong-Q/bounded-multiplier full-switch extension. No existence or
uniqueness conclusion has been added.
