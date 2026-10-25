# Focused self-review of the full-source symmetry test

Primary verdict: correct only within the stated static and symmetry restrictions; microscopic joint selection remains incomplete. This is self-review, not an independent check. Scope: RESULT.md of the lane frozen at 5b477f2ae9, parent f71cf5ac6f.

## Claim and dependency checks

The tested claim is that the specified covariant and constant-shift symmetries do not protect the rank-one static quadratic response, and that the specific local transformation inferred from that rank-one matrix fails to be a symmetry of the sourced cubic action. This is not a claim about every gauge symmetry or UV completion.

| Obligation | Verdict | Evidence |
|---|---|---|
| Static Einstein term before eliminating metric potential | Passed in three spatial dimensions | ADM expansion below |
| Vector norm, F^2 and acceleration terms | Passed at stated order | U_0=-(1+Psi), U^0=1-Psi, J_i=partial_i Psi |
| Scalar source after diagonalization | Passed | Original source is rho Phi; substitution adds g rho chi |
| Independent R deformation allowed by stated symmetries | Passed | R is invariant under diffeomorphisms and independent of scalar shift |
| All constrained modes and cosmological stability | Not addressed | Static source-regime calculation only |
| Null matrix implies full gauge invariance | Refuted for the displayed transformation | Cubic and source variations are nonzero off shell |
| Constant linear internal symmetry protects zero spatial kinetic term | Refuted for stated positive-metric representation | Same invariant quadratic form exists for spatial derivatives |
| Listed conditions select an absolute amplitude | Not established | They are necessary tangency/matching conditions, not solved Ward identities |

## Independent analytic rederivation of the Einstein sign

For a static ADM metric with zero shift, lapse 1+Psi and h_ij=exp(-2Phi)delta_ij in three spatial dimensions, the Einstein action differs by a boundary term from integral lapse sqrt(h) R^(3). The spatial curvature is

    R^(3) = exp(2Phi)[4 Delta Phi - 2|grad Phi|^2].

To quadratic order the bulk gradient contribution is

    4(Psi-Phi)Delta Phi - 2|grad Phi|^2
      = 2|grad Phi|^2 - 4 grad Psi.grad Phi

after integration by parts. This agrees with RESULT.md. Phi variation yields Delta(Phi-Psi)=0. It uses decaying boundary data and zeta nonzero; harmonic boundary modes are not silently counted as propagating solutions. The vector and scalar terms at this order depend on Psi and chi, not Phi. This is why the same elimination holds when only zeta changes.

On the aligned background, F_i0=-partial_i Psi and F^2=-2|grad Psi|^2, giving +k|grad Psi|^2 in the original Lagrangian. J.grad chi=grad Psi.grad chi. At zeta=1, h=d=2-k, the reduced quadratic expression is proportional to |grad(Psi-chi)|^2, reproducing the parent expression. This checks both the sign and relative factor of the allowed Einstein deformation.

## Matrix and source controls

Matrix M=[[A,-B],[-B,C]] has determinant AC-B^2. On its zero surface, the vector (B/A,1) is null. Direct multiplication and completing the square agree. Changing A only gives beta_new=C-B^2/(A+delta A)=B^2 delta A/[A(A+delta A)]. At delta A=0 it vanishes; for positive delta A and A>0 it is positive. B=0 gives g=0 and removes the sourced scalar force; this is not a solution to the MOND goal.

Coordinated scaling (A,B,C)->t(A,B,C), t>0, preserves the zero determinant and g. It imposes no condition on gamma or V: changing gamma to t gamma at the same time, at fixed operational G_N and V, changes a0 to a0/t. This is a static-coefficient diagnostic, not a claim that a specified high-gradient completion keeps G_N fixed automatically. The general physical-ratio variation in RESULT.md explicitly includes delta G_N for that reason.

For a source-free one-dimensional patch embedded in space with chi=x^2/2 and x>0, div(|grad chi|grad chi)=2x is nonzero. Choosing a compactly supported epsilon there makes the cubic variation nonzero even though the quadratic null transformation preserves its square. On-shell vanishing of this variation is the Euler equation, not a Noether identity. Source transformations, additional fields and nonlinear transformations are outside this counterexample's scope.

## Units and normalization

With dimensionless chi and Phi, [A]=[B]=[C]=mass^2, [gamma]=mass, [alpha]=mass^3, [rho]=[V]=mass^4, and g is dimensionless. Then a0=g^3/(4 pi G_N gamma) has dimension mass, as required in natural units. After temporal canonical normalization, g_c and gamma_c have dimensions mass^-1 and mass^-2; their ratio g_c^3/gamma_c is unchanged. Differentiating C-B^2/A gives exactly delta C-2g delta B+g^2 delta A. Differentiating kappa gives the -3/2 coefficient of delta G_N/G_N; this would be missed by treating the high-gradient Newton calibration as automatically fixed.

## Source and proofreading coverage

The official arXiv HTML version header 2007.00082v3 and equations (5)-(6) were inspected on 2026-10-24. The source provides the baseline theory, not the generalized Ward-identity proof. No complete paper was downloaded. All new equations were reviewed for symbol and dimensional consistency. No executable experiment or numerical evidence is claimed. The full positive-vacuum action, quantum corrections and an actual extra symmetry remain missing; ordinary general covariance has been tested, not all possible quantum-gravity symmetries.
