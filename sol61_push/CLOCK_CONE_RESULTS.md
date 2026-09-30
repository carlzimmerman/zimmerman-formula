# Temporal stability does not complete spatial causality

Base 0c4c5778d8056bd619ff6c1055102650126b1f79. The previous retarded-clock result was genuine progress: it included continuum damping and proved absence of growing poles at real spatial momentum. This audit tests its unresolved spatial-cone dependency and finds an obstruction to treating that reduction as an exact all-scale local response.

## Claim and necessary source theorem

The object is the exact extrapolation

G_R(omega,k)=1/[Akin(omega^2-gamma k^2 B_R(omega,k))],

B_R=integral_0^1 sqrt(v^2 k^2(1-mu^2)-(omega+i0)^2)dmu,

with gamma,v,Akin positive. This is the same full orientation-averaged continuum kernel as RETARDED_CLOCK_RESULTS.md, not an isolated three-halves pole. No extra spatial stabilizer is included here.

For a retarded tempered response of a local observable supported inside |x|<=c*t, the Fourier-Laplace transform must be analytic in Im omega>c|Im k|. Primary source checked: Creminelli, Longo, Salehian and Zahed, [Analyticity and positivity of Green's functions without Lorentz, arXiv:2512.10843v2](https://arxiv.org/html/2512.10843v2), 7 May 2026, Section 3 equation 3.10 and Appendix A.3 equations A.21-A.27. The necessary analyticity direction follows by exponential decay on the support cone; the source gives the tempered-distribution formulation and accompanying growth bounds. Rescaling space extends the unit-speed statement to any finite c. Only the necessary direction is used; we do not infer microcausality from frequency positivity.

The response being extrapolated is translation invariant in a local flat approximation. Applying this theorem to the actual de Sitter state without that approximation would require a different calculation. Treating a bounded EFT approximation as exact outside its domain is also excluded from the conclusion below.

## A pole inside every finite-speed analytic tube

Continue omega=i*s and the spatial momentum vector to i*kappa along one fixed direction. In the region s>v*kappa, every orientation has a positive square-root argument, so there is no branch ambiguity. Up to an irrelevant nonzero normalization/sign the Laplace denominator is

D(s,kappa)=s^2-gamma kappa^2 B(s,kappa),

B(s,kappa)=integral_0^1 sqrt(s^2-v^2 kappa^2(1-mu^2))dmu.

It obeys sqrt(s^2-v^2 kappa^2)<=B<s for positive v*kappa. Choose

s_lo=gamma kappa^2/2, s_hi=gamma kappa^2,

kappa>4v/(sqrt(3)*gamma).

Then s_lo>v*kappa and B(s_lo)>s_lo/2. Consequently D(s_lo)<0 and D(s_hi)>0. The integral is analytic and continuous throughout this interval, hence D has a zero s_star in (s_lo,s_hi). Its numerator in G_R is nonzero, so this is a genuine singularity.

For any proposed finite cone speed c, additionally choose kappa>2c/gamma. The zero then satisfies s_star>c*kappa. It lies in the domain where a finite-cone tempered local response is required to be analytic. This contradicts that necessary condition. Thus this exact extrapolated kernel is incompatible with every finite signal cone.

For large kappa the pole is s_star=gamma kappa^2-v^2/(3gamma)+O(kappa^-2). The quadratic growth rather than linear growth makes the all-speed contradiction possible. The proof uses the bounds and intermediate value argument above; a finite root grid alone would not establish it.

These are complex-momentum poles. They do not represent exponentially growing normal modes at real momentum and do not invalidate the earlier real-momentum temporal-stability proof. That distinction is essential.

## A direct diagnostic limit

Formally set v=0 at fixed gamma in the normalized kernel. This is a mathematical limit, not a healthy zero-speed fermion construction. For real spatial momentum, B_L=s and

G_L(s,k)=1/[s(s+gamma k^2)],

G_L(t,k)=(1-exp(-gamma k^2*t))/(gamma k^2).

The corresponding three-dimensional spatial response, away from r=0, is

G_L(t,r)=erfc[r/(2sqrt(gamma*t))]/(4pi gamma r), t>0.

It is the time integral of a heat kernel and is positive at every r>0 for every positive t. This explains how frequency-stable behavior can coexist with arbitrarily long spatial tails. The v>0 conclusion does not depend on taking this singular physical limit: it was proved directly through complex momentum.

## Local observable and EFT qualifications

One must not use an instantaneous gauge potential alone as a microcausality test of physical gravity. In this reduced preferred-foliation scalar sector, however, the linear intrinsic curvature is delta R3=-4Delta zeta on a background with R3=0. Its local-source two-point response multiplies the scalar propagator by 16k^4, apart from normalization. At the displayed nonzero imaginary momenta this factor does not cancel the poles. Therefore simply differentiating the scalar into this local curvature does not remove the obstruction inside the assumed reduction. A full theory could change the constraint reduction, include other contributions or modify the operator response; those changes have not been calculated.

The exact extrapolation is refuted as a finite-cone completion. Its role as a restricted EFT remains open. The pole proof requires access to both the complex spatial and temporal scales involved. If new operators, bulk modes or the cosmological background are important there, the present extrapolation is not authoritative at the pole and cannot exclude that completion.

The required repair scale can be made explicit. For a unit-speed cone and 0<v<=1, choose kappa=4/gamma. There is already a pole with 8/gamma<s_star<16/gamma, inside that tube. From the prior matching,

1/gamma=4y a0_bare(3lambda-1)/[pi(lambda-1)].

Thus a proposed finite-cone completion cannot leave this exact response unchanged through that complex-frequency/momentum window. Whether the window lies within the physical EFT depends on y,lambda, the actual cutoff and H. Because a0 is linked to cosmological scales in the target, a full de Sitter calculation may be necessary; it is not legitimate to invoke the flat high-frequency approximation automatically at these scales. This is a repair obligation, not a new numerical selection of 32pi.

## Verification and audit decision

Twenty-four checks pass: bracket signs and poles for gamma=1, v={0.2,1}, kappa={3,10,30}; independent closed-form/angular quadrature; explicit unit-speed-tube examples; and the formal heat-kernel benchmark. Maximum relative root residual is about 3.30e-15. Both the code and result are pinned in the validated manifest. Universal cone exclusion is established by the analytic argument and the authenticated necessary theorem, not by these finite cases.

Self-review verdict: the exact extrapolated kernel is refuted as a finite-cone local tempered response. Its low-momentum collective resonance and real-momentum temporal stability survive as scoped results. The original physical goal remains unresolved. No claim is made that every preferred-time theory, every continuum completion or every theory with a collective three-halves dispersion is excluded.

Next, do not reuse this unchanged kernel as the claimed causal completion. A constructive continuation must alter the clock/constraint dynamics at the specified scale, or calculate the actual curved-state response that invalidates the extrapolation, and then redo the signal-cone audit. The independent current observational test of G_cosm/G_N remains available. Critical matching, vacuum normalization, selected D/lambda and exact 32pi are still missing; this obstruction closes only the exact response interpretation tested here.
