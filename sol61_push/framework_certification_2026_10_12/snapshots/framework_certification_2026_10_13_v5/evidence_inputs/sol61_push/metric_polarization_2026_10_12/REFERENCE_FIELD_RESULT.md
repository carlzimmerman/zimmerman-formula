# An adaptive reference field cancels a uniform external field but changes the outer force

12 October 2026. Continuation from `REPORT.md`; initial repository checkpoint `1d07a4c57`. **Partial constructive result:** a second polarization field gives an exact static cancellation of a uniform external field while preserving the convex fixed-source energy of the reduced Newtonian model. An explicitly dissipative one-dimensional evolution reaches that cancellation after the external field changes, without manually shifting its initial reference. This is an adaptive reference, not a demonstrated permanent memory of halo formation.

The cost is now calculable: quadratic reference stiffness produces an unwanted large-radius force, while a nonlinear stiffness repair alters the mass–velocity relation and is singular at a uniform vacuum. The mechanism remains phenomenological, and no relativistic lensing or empirical success is claimed.

## Target and routes

The target is a dynamical escape from the external-field dependence derived in `REPORT.md`, keeping a positive constrained energy and a useful deep-MOND response. Complete success would also require a covariant action, common photon/tensor characteristics, evolving matter, cosmological matching and the project's remaining selector requirements. Those are not replaced by this narrower target.

Three initial routes were tested: a time delay with unchanged constitutive equilibrium; a dynamical reference with quadratic spatial stiffness; and a pinning term to repair the reference's asymptotic behavior. A fourth route replaces quadratic stiffness by a nonlinear gradient energy. No other chat's files or active simulations were changed.

## A delay by itself cannot change the static response

For a relaxation equation \(\tau\dot Q=F(Q,g)\), every time-independent solution still satisfies \(F(Q,g)=0\). Likewise, a normalized integrable causal convolution applied to a stationary constitutive force leaves that force unchanged. Thus these particular finite-memory implementations retain the old equilibrium external-field effect. This does not rule out nonintegrable memory, extra conserved variables or a different constitutive energy.

The next construction changes the constitutive energy itself; it is not just a delayed version of the old response.

## Two fields and one constrained potential

Keep the previous gravitational coupling \(\mathbf Q\cdot\nabla\Phi\) and introduce a reference vector \(\mathbf R\). Replace the internal potential and gradient terms by

\[
 U(\mathbf Q,\mathbf R)=2\pi G|\mathbf Q|^2
       +{b\over3}|\mathbf Q-\mathbf R|^3,
 \qquad E_\nabla={\gamma\over2}|\nabla\mathbf Q|^2
                +{K_R\over2}|\nabla\mathbf R|^2.
\]

Both fields have positive inertias \(I_Q,I_R\). The coefficients \(b,\gamma,K_R\) are positive and chosen, not derived. In particular \(K_R\) is unrelated to the fitted cosmological coefficient \(\kappa\). Solving the Newtonian constraint under the same Helmholtz boundary assumptions as the previous report gives

\[
 H=\int d^3x\left[
 {I_Q\over2}|\dot{\mathbf Q}|^2+{I_R\over2}|\dot{\mathbf R}|^2
 +2\pi G|\mathbf Q_T|^2+{b\over3}|\mathbf Q-\mathbf R|^3
 +{\gamma\over2}|\nabla\mathbf Q|^2+{K_R\over2}|\nabla\mathbf R|^2
 -\mathbf Q\cdot\mathbf g_N\right].
\]

This is convex in the two fields for fixed sources. With \(\mathbf d=\mathbf Q-\mathbf R\), its cubic Hessian is
\(A=b(|\mathbf d|\mathbf 1+\mathbf d\mathbf d^T/|\mathbf d|)\), defined as zero at \(\mathbf d=0\). The block Hessian contains the positive form
\((\delta\mathbf Q-\delta\mathbf R)^T A(\delta\mathbf Q-\delta\mathbf R)\), both gradient squares, and the transverse gravitational square. Positive inertia therefore leaves no negative-stiffness exponential mode in this fixed-source constrained system. Zero modes, PDE existence and live matter require separate analysis.

### Exact uniform-field cancellation

The full static field equations are

\[
 \nabla^2\Phi=4\pi G(\rho_b+\nabla\cdot\mathbf Q),
\]
\[
 0=\nabla\Phi-4\pi G\mathbf Q-b|\mathbf d|\mathbf d
                      +\gamma\nabla^2\mathbf Q,
 \qquad 0=b|\mathbf d|\mathbf d+K_R\nabla^2\mathbf R.
\]

For any constant vector \(\mathbf C\), these equations are invariant under

\[
 \mathbf Q\mapsto\mathbf Q+\mathbf C,\quad
 \mathbf R\mapsto\mathbf R+\mathbf C,\quad
 \Phi\mapsto\Phi+4\pi G\mathbf C\cdot\mathbf x.
\]

The baryonic source is unchanged. So is the effective internal density \(\nabla\cdot\mathbf Q\). The added potential supplies only a uniform acceleration. This is an exact comparison of static solutions with correspondingly shifted boundary data, not yet a theorem that evolving galaxies acquire those boundary data. It cancels uniform external fields only; finite host gradients and tides do not transform away.

This construction is a counterexample to an unrestricted claim that *every* nonlinear Newtonian field equation must have a static uniform-field effect. It is not a counterexample to the project's scoped no-go results for a different field content, nor a proof that observed satellites require zero external-field effect.

## Does the reference adjust without being initialized to the answer?

For this question only, choose a positive-mobility gradient flow of the reduced energy. This assumes a dissipative reservoir; it does not derive microscopic dissipation. On a periodic one-dimensional domain, set \(4\pi G=b=1\), \(\gamma=0.01\), \(K_R=10\), and \(g_N(x)=\sin x+0.2\sin2x\). The nonzero Fourier modes of Q are longitudinal; its spatial mean retains the quadratic gravitational term. The evolution is

\[
 \dot Q=g_N+g_e-\bar Q-|Q-R|(Q-R)+\gamma Q_{xx},
 \qquad \dot R=|Q-R|(Q-R)+K_R R_{xx}.
\]

At fixed \(g_e\), the continuum energy obeys
\(\dot H=-\int(\dot Q^2+\dot R^2)dx\le0\). The energy injected by changing \(g_e\) is external work, not a violation of this identity. Start with the evolved zero-background solution, then step \(g_e\) to 1 or 3, leaving both initial fields unchanged.

For the step to 3, on the 128-cell grid:

| dimensionless time | relative internal-profile change |
|---:|---:|
| 0.1 | 0.0082 |
| 1 | 0.2390 |
| 2 | 0.3035 |
| 10 | 0.0424 |
| 20 | 0.00138 |
| 40 | 0.00000108 |
| 80 | below 1e-11 |

The relative change is the L2 norm of \(Q-\bar Q\) minus its original profile, divided by the original profile norm. Both field means approach 3. Holding the reference fixed instead leaves a **0.596** relative profile change. Thus the disappearance of the disturbance is generated by the additional dynamics in this example, rather than imposed by resetting the reference.

The 64- and 128-cell endpoint profiles differ by \(9.82\times10^{-5}\), just below the declared \(10^{-4}\) refinement threshold. Recovery within each grid is much more accurate because it tests the exact shift symmetry of that discretization; it is not a claim of a 1e-11 continuum error. No physical time in years follows from the arbitrary mobilities.

## The spherical cost is exact

For radial fields \(\mathbf Q=q(r)\hat r\), \(\mathbf R=s(r)\hat r\), write
\(\mathcal L_r u=u''+2u'/r-2u/r^2\). Then

\[
 -\gamma\mathcal L_rq+b|q-s|(q-s)=g_N,
 \qquad -K_R\mathcal L_rs-b|q-s|(q-s)=0.
\]

Adding the equations eliminates the nonlinear term:

\[
 -\mathcal L_r w=g_N,\qquad w=\gamma q+K_Rs.
\]

Outside a compact mass \(M\), \(g_N=GM/r^2\), hence every exterior solution has

\[
 w={GM\over2}+{C_1\over r^2}+C_2r.
\]

Therefore both fields cannot decay to zero at infinity. On the bounded, asymptotically regular branch where they approach constants and their derivatives decay, the separate equations require \(q-s\to0\), giving

\[
 q_\infty=s_\infty={GM\over2(\gamma+K_R)},\qquad
 g_{\rm extra,\infty}={2\pi G^2M\over\gamma+K_R}.
\]

That is a constant radial force, not a flat-rotation-curve tail. The nonzero radial vector texture also has linearly divergent gradient energy at large radius. This obstruction closes the isolated decaying-boundary version of this quadratic-gradient construction. It does not exclude finite cosmological matching, whose boundary must be supplied by an actual model.

### A finite radial window survives

With a Plummer source, scale radius \(r_b\), and \(B=\sqrt{GM/b}\), use \(x=r/r_b\), \(q=(B/r_b)u\), \(s=(B/r_b)v\), \(\epsilon=\gamma/(bBr_b)\), \(K=K_R/(bBr_b)\). The source is \(f=x/(1+x^2)^{3/2}\). The sum and difference equations reduce to

\[
 -\mathcal L_x w=f,\qquad
 -{\epsilon K\over K+\epsilon}\mathcal L_x d+|d|d={K\over K+\epsilon}f,
\]
\[
 u={w+Kd\over K+\epsilon},\qquad v={w-\epsilon d\over K+\epsilon}.
\]

Eight boundary-value solves use regular inner conditions and \(u=v=0\) at an imposed outer radius, with \(\epsilon=0.01\). For outer radius 600, the polarization relative to the zero-stiffness MOND value \(\sqrt f\) is:

| K | x=3 | x=10 | x=30 | x=100 |
|---:|---:|---:|---:|---:|
| 1 | 2.342 | 5.764 | 15.046 | 42.219 |
| 10 | 1.132 | 1.480 | 2.417 | 5.159 |
| 100 | 1.009 | 1.047 | 1.142 | 1.416 |
| 1000 | 0.997 | 1.004 | 1.014 | 1.041 |

These are polarization ratios, not full-force ratios. Large K retains an approximate galaxy window, at the price of a free stiffness. Doubling the physical outer boundary from 300 to 600 changes the result: for K=1000 and x=100, 1.033 becomes 1.041. That dependence is a prediction of the assumed boundary problem, not a numerical convergence error or a derived halo edge. K itself depends on mass and source size for fixed physical coefficients; it cannot be held fixed across galaxies without explanation.

The local quadratic version of the same tradeoff is a Schur complement. For longitudinal relative curvature \(A>0\), eliminating the reference gives

\[
 H_{\rm eff}(k)=\gamma k^2+{A K_Rk^2\over A+K_Rk^2}.
\]

Short wavelengths retain the original restoring force; long wavelengths have only gradient stiffness. This soft long-wavelength response is why removing a uniform-field effect also changes the outer solution in this model.

## Two repairs and their costs

**Pin the reference.** Adding \(\mu^2|\mathbf R|^2/2\) supplies nonzero long-wavelength stiffness,
\(A\mu^2/(A+\mu^2)\), and can restore a decaying branch. But it explicitly breaks the common shift symmetry. In a uniform external field the reference equation becomes \(b|\mathbf d|\mathbf d=\mu^2\mathbf R\); generally \(\mathbf d\ne0\). Internal stiffness then depends on the external field again. This repair is not an exact uniform-field cancellation.

**Use nonlinear gradient energy.** Replace the reference gradient term by \(\lambda|\nabla\mathbf R|^p/p\), with the Frobenius norm and \(\lambda>0\). It is convex for \(p>1\) and preserves constant shifts. For a radial tail \(s=C/r\), its force scales as \(r^{1-2p}\). Matching \(GM/r^2\) selects \(p=3/2\), and an exact radial calculation gives

\[
 -\lambda\nabla\cdot(|\nabla\mathbf R|^{-1/2}\nabla\mathbf R)
 ={3^{3/4}\lambda\sqrt C\over r^2}\hat r,
 \qquad C={(GM)^2\over3^{3/2}\lambda^2}.
\]

The leading Q equation still gives \(q-s=B/r\), so

\[
 V_\infty^2=4\pi G(B+C)
 =\sqrt{GMa_0}+{4\pi G(GM)^2\over3^{3/2}\lambda^2},
\]

when b is calibrated as before. The inverse-radius force is restored, but its extra amplitude grows as \(M^2\), and its fractional deviation from BTFR as \(M^{3/2}\). A sufficiently large free \(\lambda\) can suppress this over a finite mass range; the calculation is not an exclusion of all parameter values.

There is a second cost: the Hessian of \(|\nabla R|^{3/2}\) diverges as \(|\nabla R|^{-1/2}\) near a uniform vacuum. With constant finite inertia there is no bounded linear wave-speed limit there. Smooth regularization recovers quadratic gradients at sufficiently small field gradients, returning the original far-tail issue. A nonlinear inertia or covariant resolution has not been constructed.

More generally, a nonvanishing first-gradient monomial \(R^m(\nabla R)^n\) has force scaling \(M^{(m+n-1)/2}r^{-(m+2n-1)}\) on a family \(R\propto\sqrt M/r\). Matching both \(Mr^{-2}\) powers requires \(m+n=3\) and \(m+2n=3\), hence \(n=0\). This is a homogeneity obstruction for that monomial class, not for ratios of invariants, nonlocal actions, additional scales or cancellation between terms.

## Verification and novelty boundaries

Three contracts preceded their runs. `reference_run` passes 34 grouped checks, including eight nonlinear boundary problems, integrated identities, exact radial identities and 48 six-by-six Hessian samples. `adaptation_run` passes 25 checks, including both resolutions, zero-step controls, dissipative energy descent and the frozen-reference control. `gradient_run` passes five exact symbolic gates. All three provenance manifests validate. The checks do not establish a full relativistic theory.

Self-audit verdict: **correct only after a stated restriction** — fixed sources and the displayed Newtonian actions, specified boundaries, and the particular phenomenological dissipative evolution. The endpoint symmetry is exact for static uniform shifts; tides, changing source positions and microscopic reference formation remain outside that proof. The nonlinear-gradient tail is an asymptotic branch calculation, not a global solution. No independent agent review was used.

The broader idea of history-sensitive MOND and modified external-field effects is already in [Milgrom, arXiv:2208.07073v3, section IV D](https://arxiv.org/pdf/2208.07073v3). That paper changes inertia and can depend on orbit-averaged external acceleration; it neither supplies this two-field gravitational action nor establishes its lensing. The source was checked on 12 October 2026 through the primary PDF, not cached.

Searches used “MOND external field effect memory”, “polarization shift symmetry reference field”, and “two vector fields gravitational polarization”, plus local searches in the prior polarization work and recent Claude lanes. This is not an exhaustive novelty search. The precise reference-field construction and the accompanying tradeoff are exploratory results of this continuation, not certified globally novel physics.

## Current research decision

The constructive advance is an explicit **adaptive background subtraction in the field equations**, with positive fixed-source energy and a demonstrated dissipative adjustment. It requires no externally assigned galaxy label in the periodic test. It does not yet identify a bound object, select a cosmological boundary, or provide real cold-mass abundance.

Do not promote the quadratic-gradient version to a complete galaxy theory: its isolated tail fails analytically. Keep finite cosmological matching open, with the derived radial sum equation as a mandatory constraint. The nonlinear-gradient version is also open only conditionally: its mass-dependent correction and singular vacuum need resolution before a data fit is meaningful. Further repetitions of the uniform-field toy test would not resolve either issue.

The next substantive question is whether a **covariant cosmological boundary or a regular reference-sector action** can cut off the soft common mode while retaining the successful internal shift cancellation. Neither is supplied by the current reduced model. The original physics goal remains open; this continuation adds a concrete mechanism and two explicit constraints on how it could be completed.
