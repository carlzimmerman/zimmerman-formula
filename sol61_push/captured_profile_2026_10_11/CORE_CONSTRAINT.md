# A finite phase-space ceiling cannot reproduce the exact central cusp

2026-10-11. Base: `a5e6e3696c2fe80dfcd1932c633f371f4b08d3c1`.
Conditional local theorem and positive local construction. This is not a
microscopic identification of cold energy or a derivation of the force law.

## Assumptions and target

Take a spherical smooth baryonic core with nonzero finite central density,
no central point mass, and

\[
 g_N(r)=Ar+O(r^3),\qquad A=\frac{4\pi G\rho_b(0)}3>0.
\]

For the Plummer source used in the experiments, `A=GM/b_f^3`. Both the raw
exponential and repaired kernels have the same low-acceleration asymptotic
`nu(y) ~ y^(-1/2)`. Thus, putting `B=sqrt(a0 A)`, the stipulated law gives

\[
 g(r)\sim Br^{1/2},\qquad
 M_c(<r)=\frac{r^2}{G}[g(r)-g_N(r)]
 \sim\frac BG r^{5/2}.
\tag{1}
\]

This uses only the force asymptotic, with no differentiation. For the smooth
repository kernels, or with explicit derivative remainder control, it also
gives

\[
 \rho_c(r)\sim D r^{-1/2},\qquad D=\frac{5B}{8\pi G}.
\tag{2}
\]

The limit is at the centre of extended baryons, where `g_N -> 0`. It differs
from the high-acceleration Kepler annulus outside a compact source. The
earlier exponential-hollow and repaired-log-tail calculations concern that
other limit; neither removes (1).

## Obstruction for bounded collisionless distributions

Let `f(x,v,t)` be a three-dimensional mass distribution function with
`0 <= f <= f_max < infinity`, transported by Hamiltonian Vlasov evolution.
Along each characteristic `df/dt=0`; retaining only selected trajectories
cannot increase this bound. Assume that after assembly the retained component
has finite local velocity support bounded by escape speed
`v_esc(r)=sqrt(2 Psi(r))`, with `Psi(0)=Psi_0 < infinity`.

Integrating over the whole permitted velocity ball, irrespective of
anisotropy, gives

\[
 \rho_{\rm ret}(r)\le\frac{4\pi}{3}f_{\max}[2\Psi(r)]^{3/2}.
\tag{3}
\]

Consequently `M_ret(<r)=O(r^3)` near the origin. This contradicts the positive
`r^(5/2)` leading term of (1) if exact equality is required down to arbitrarily
small radius. Positive normalized time averaging or phase averaging of the
actual evolved DF preserves (3). The result does not require isotropic orbits.

Self-gravity does not by itself evade this argument when the final escape
depth is finite. The target cusp has locally integrable force and finite
central potential. However, a globally untruncated logarithmic potential
has no finite escape depth; a physical outer boundary or bounded energy
support is essential. Bounded f alone with unbounded velocities does not
imply (3).

The finite orbit atoms of the previous planar capture experiment are singular
distributions and fall outside these hypotheses. The new profile experiment
instead starts with a bounded 3D DF. Finite quadrature approximations to it
still have individual orbital caustics, so the analytic ceiling must not be
tested by treating those atoms as the exact continuum DF.

## What a positive singular isotropic completion would require

Including the stipulated cold gravity, the local relative potential satisfies

\[
 \delta=\Psi_0-\Psi(r)\sim Qr^{3/2},\qquad Q=\frac{2B}{3}.
\]

The cold cusp dominates the finite baryonic core density in this exact limit.
Equation (2) becomes `rho_c ~ C delta^(-1/3)`, where `C=D Q^(1/3)`.
For an isotropic mass DF with specific binding energy `epsilon`, the velocity
integral is

\[
 \rho(\Psi)=4\pi\sqrt2\int_0^\Psi
 f(\epsilon)\sqrt{\Psi-\epsilon}\,d\epsilon.
\tag{4}
\]

The lower limit assumes a specified finite escape-energy convention; changing
the regular lower-energy part does not determine the leading singular term.
If `f(epsilon) ~ F (Psi_0-epsilon)^(-p)`, `p>3/2`, then setting
`t=(Psi-epsilon)/delta` yields

\[
 \rho\sim4\pi\sqrt2 F\,
 \mathrm B(3/2,p-3/2)\,\delta^{3/2-p}.
\]

A positive local construction matching the target is therefore

\[
 \boxed{f(\epsilon)\sim
 \frac{D Q^{1/3}}{4\pi\sqrt2\,\mathrm B(3/2,1/3)}
 (\Psi_0-\epsilon)^{-11/6}.}
\tag{5}
\]

This is sufficient locally. Pointwise necessity requires suitable inversion
regularity; a density asymptotic alone cannot justify differentiating arbitrary
remainders. Equation (5) does not establish global DF positivity, finite outer
mass, stability or formation from a specified initial state.

The singularity has finite mass. The local density of states for potential
gap proportional to `r^(3/2)` scales as `u^(5/2)`, with `u=Psi_0-epsilon`.
Multiplying by (5) gives mass per binding-energy interval proportional to
`u^(2/3)`, which is integrable. An infinite phase-space peak is not an infinite
enclosed mass.

In the *baryon-only tracer* potential, the gap instead behaves as
`delta=(A/2)r^2`. The analogous exponent is `7/4`, with coefficient
`D(A/2)^(1/4)/[4 pi sqrt(2) B(3/2,1/4)]`. That is a distinct control, not
the self-consistent potential of the target cusp. Confusing these potentials
would give the wrong exponent for the full theory.

## Physical interpretation and remaining choices

This excludes exact-to-origin realization from bounded collisionless f with
finite escape depth. It does not exclude finite-annulus fits: without a
physical value of f_max, the departure radius can be arbitrarily small.
Singular zero-dispersion sheets, a genuinely unbounded initial DF, or dynamics
that change the phase-space ceiling evade the stated class. None is thereby
shown to generate the required profile or to describe nature.

A finite phase-space ceiling would instead require a central regularization
of the exact law. Formally the asymptotic crossover scale compares
`D r^(-1/2)` with `rho_max=(4 pi/3) f_max (2 Psi_0)^(3/2)`, giving
`r_phase ~ (D/rho_max)^2` only when this radius lies in the asymptotic domain.
This is a conditional scale relation, not a measured radius or an additional
parameter-free prediction.

The exponent 11/6 is an inverse consequence of the supplied force law. It
does not predict that law, select a carrier, determine its cosmic abundance,
or explain kappa=1/2. Two independent analytic reviews checked the enclosed-
mass obstruction and Abel coefficient; numerical endpoint checks in
[experiment.py](experiment.py) test the velocity-integral normalization.
