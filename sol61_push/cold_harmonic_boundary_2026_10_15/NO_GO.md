# Harmonic shifts defeat every finite elasticity amplitude in the old boundary model

2026-10-15. This is an analytic counterexample to the finite **clock-mass** construction proposed in [CCC](../cold_constraint_cap_2026_10_15/THEORY.md). It is not a no-go theorem for every possible finite-phase gravitational action or propulsion system. The argument is self-reviewed, not independently refereed.

## Exact hypotheses and quadratic form

Work about the flat rest member of that family: γij=δij, N=1, β=0, ΦA=xA. Use signature −+++ and reduced Planck mass M. Let h≥0 be smooth, bounded, compactly supported and positive on the nonempty bounded open set Ω={h>0}. In the old model h supplies a positive lapse mass and shift mass as well as a spatial strain mass. Let θ≥0 be compactly supported. Let 0≤κ≤κmax be bounded on Ω. The acceleration-square coefficient A may be nonnegative; it has no velocity mixing on this background. No new shift-shear-gradient operator is included.

For metric velocity uij=δγdotij and shift perturbation v, put Dvij=∂ivj+∂jvi. The velocity/shift form at lapse perturbation α=0 is

\[
J(u,v)={M^2\over8}\int[|u-Dv|^2-(\operatorname{tr}u-2\operatorname{div}v)^2
+\theta(\operatorname{tr}u-2\operatorname{div}v)^2+\kappa|u|^2]
+2\int h|v|^2.
\]

The flat lapse form is independent of velocity and has nonnegative quadratic part ∫[hα²+M²A|∇α|²]/2. Outside its support it imposes the Einstein linear scalar constraint R1(Q)=0. We will take u smooth with compact support strictly inside Ω, so this exterior constraint, its time derivative, and all boundary compatibility conditions are respected. At initial Q=0 the lapse is α=0.

The reduced kinetic form is the minimum over the shift energy space, retaining any null directions as constraints. We justify this reduction below; the argument does not drop a null auxiliary mode.

## The uncontrolled harmonic direction

For any k>0 choose

\[
f_k(x,y,z)=e^{kz}\cos(kx),\quad \Delta f_k=0,\qquad
|\nabla f_k|^2=k^2e^{2kz},\quad
|\nabla^2 f_k|^2=2k^2|\nabla f_k|^2.
\]

These identities hold pointwise. Choose a smooth compact cutoff ζ=1 on a neighborhood of the supports of θ and h, and set F=ζfk and v=∇F. The vector v is smooth and compactly supported. Its curl is identically zero globally. Its divergence vanishes wherever θ is nonzero, and v=∇fk on Ω.

For every compact gradient shift,

\[
\int[|Dv|^2-4(\operatorname{div}v)^2]=0.
\]

To see the cancellation directly, the divergence of (∇²F)∇F−(ΔF)∇F is |∇²F|²−(ΔF)². The integral is zero. The region where F is cut off lies outside the material phase. The locally indefinite Einstein shift contribution there cancels the harmonic Hessian contribution inside. The θ term sees no divergence in the phase, so it does not prevent this cancellation.

Let C=1+κmax and choose 0≤χ≤1 smooth with compact support in Ω so that

\[
\int_\Omega\chi|\nabla^2f_k|^2\ge\tfrac12\int_\Omega|\nabla^2f_k|^2.
\]

Such χ exists for each finite k by inner regularity and smooth approximation of the finite positive weighted integral on Ω. There is no derivative-of-u penalty in the kinetic form, so no uniform bound on derivatives of χ is being assumed. Define

\[
u={2\chi\over C}\nabla^2 f_k.
\]

This is smooth, compactly supported in Ω, and tracefree. Thus the θ square is zero everywhere for this pair (u,v). Expanding the Einstein term and using its integrated pure-shift cancellation gives exactly

\[
J(u,v)={M^2\over8}\int_\Omega(1+\kappa)|u|^2
-{M^2\over2}\int_\Omega u:\nabla^2f_k
+2\int_\Omega h|\nabla f_k|^2.
\]

Since χ²≤χ and 1+κ≤C,

\[
\begin{aligned}
J(u,v)&\le-{M^2\over2C}\int_\Omega\chi|\nabla^2 f_k|^2
+2h_{\max}\int_\Omega|\nabla f_k|^2\\
&\le\left[2h_{\max}-{M^2k^2\over2C}\right]
\int_\Omega|\nabla f_k|^2.
\end{aligned}
\]

The last integral is strictly positive. Hence

\[
\boxed{k^2>{4(1+\kappa_{\max})h_{\max}\over M^2}
\quad\Longrightarrow\quad J(u,v)<0.}
\]

Every finite κmax admits such a k. Increasing the old derivative-elastic amplitude cannot make the full continuum kinetic form nonnegative. This settles the previously open stronger-κ route negatively, within the stated action and continuum assumptions.

## Why this is a physical reduced kinetic direction

The shift-only quadratic form is

\[
B(v)={M^2\over4}\|\nabla\times v\|_2^2
+{M^2\over2}\int\theta(\operatorname{div}v)^2+2\int h|v|^2\ge0.
\]

The u–v linear functional is bounded in this energy norm: integrate its derivative of v onto u. Both u and its derivatives have compact support in a region where h has a strictly positive minimum. A Cauchy–Schwarz bound using ∫h|v|² therefore applies. Any B-null shift vanishes on Ω; its derivatives vanish there as well, and its coupling to u is zero. Thus all shift-null multiplier constraints are satisfied. The affine minimization has a finite minimum in the Hilbert completion modulo the nullspace, by the Riesz representation theorem for that explicitly bounded functional. Uniqueness as an unweighted H¹ vector field is not claimed.

The reduced kinetic form is consequently ≤J(u,v)<0. The lapse velocity block minimizes at α=0 and cannot repair it. At initial Q=0 the static energy vanishes, so this is a negative **physical quadratic kinetic energy**, not merely an arbitrary negative auxiliary density or a potential instability. It establishes a ghost in this continuum rest-state construction; it does not assert a particular nonlinear decay rate or a complex-frequency spectrum.

All fields in the witness are smooth and compactly supported for each finite k. The cutoff shift can have a large norm before rescaling. Multiplying u and v by a common arbitrarily small amplitude keeps the sign and puts the whole perturbation in the linear regime. A microscopic cutoff below the required k would invalidate this witness as an effective-theory prediction; such a cutoff and its stabilizing completion have not been supplied. No claim about arbitrarily short physical wavelengths beyond an established cutoff is made.

## An explicit κmax=64 example with rational bounds

Normalize M=hmax=1 and take Ω to be the unit ball. One smooth choice is h(r)=exp[1−1/(1−r²)] for r<1 and zero otherwise. Let θ=1 through r=2 and taper it smoothly to zero by r=3; set κ=64θ. Take k=17 and replace fk by exp[17(z−1)]cos(17x), which only changes its normalization. Choose χ=1 for r≤99/100, smoothly zero by r=199/200. Choose ζ=1 through r=4 and zero by r=5.

Writing I(r)=∫ball(r)|∇fk|², direct integration gives

\[
I(r)={\pi e^{-2k}\over4k}[(2kr-1)e^{2kr}+(2kr+1)e^{-2kr}].
\]

At k=17, I(1)≤π/2, using e68≥1+68>35. Also e^−(17/50)≥1−17/50=33/50 gives

\[
I(99/100)\ge{53889\over170000}\pi>{\pi\over4}\ge\tfrac12 I(1).
\]

Thus this explicit χ meets the capture condition without a numerical quadrature assumption. The energy bound is

\[
J_{\rm red}\le J(u,v)\le-{29\over130}I(1)<0.
\]

For orientation only, I(1)≈1.52459643483. The sign and capture proof use exact identities and rational/exponential inequalities, not that decimal value. The [symbolic run](run_v2/calculation/results.json) checks the load-bearing identities.

## What survives, and what is superseded

The previous infinite-medium theorem is not contradicted: θ there does not stop, so the harmonic shift cannot be cut off outside its support at no material penalty. The previous globally massless finite cap is not contradicted either: its global lapse constraint excludes the velocity constructed here. The decaying purely planar theorem lacks this transverse harmonic family; a one-dimensional harmonic f has zero Hessian.

The finite clock-mass candidate, including its stronger κ=64/400 versions, is ruled out as a healthy continuum rest-state model under these assumptions. Its fixed-speed source family includes this V=0 rest member. This is enough to reject the claimed healthy full family; no unproved extension of the counterexample to every moving curved background is needed. A model restricted to a different phase or a different action requires a new analysis.

In the previous weighted comparison formulation, the required universal elasticity threshold C* is therefore infinite for this old finite-clock-mass class. The successful finite grids did not bound that supremum.
