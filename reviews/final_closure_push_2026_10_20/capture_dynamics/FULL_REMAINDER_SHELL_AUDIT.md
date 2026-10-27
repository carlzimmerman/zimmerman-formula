# Audit: full-remainder finite circular-shell continuation

20 October 2026. Assessment base `f659e6d8e1ee4cf2b756f091aff56b018da1fb1e`.
Reviewed source:
`../full_remainder_shell/FULL_REMAINDER_SHELL.md`, SHA256
`9d92fbdeb4dcf0d8c9d29335c174445d9f2396b19afc15dbc279f2680eb625b9`.
The initially audited snapshot was
`db374e2ab556de7016d8297e0d82c55908ae16a4091c28be52ea47e169ac56be`;
the final change corrected a prose separator and clarified the outer-taper
integral's lower-limit delimiters. The affected lines were re-read and the
mathematical conclusion is unchanged.

**Normalized claim.** The specified zero-stiffness reciprocal spherical energy
with full remainder `R(u)=u^2/(a0-u)` admits finite smooth nonnegative spatial
two-population profiles with both stocks positive, an exact total
ordinary-tracer law on a compact annulus,
singular stationary circular phase-space measures and a positive conserved
energy for their coherent linear radial shell perturbations. A stated
subfamily also has positive fixed-angular-momentum radial splitting second
variation, stable fixed-field circular test orbits and a uniform negative
circular specific-energy gap.

**Primary verdict: proved as written in that scope.** I found no failed
analytic implication in the displacement, energy, profile or specific-energy
arguments. These results do not provide a smooth warm equilibrium, a
time-dependent kinetic stability theorem, nonlinear shell-order preservation,
formation or full-theory closure.

## Exact hypotheses and dependency graph

The proof assumes separately conserved positive cold masses, fixed finite
nondecreasing baryonic enclosed mass `B`, smooth compact cold spatial densities
in a hollow interval `[r_0,R]`, positive lower baryonic stock on that support,
and a uniform gap `u<=u_*<a0`. The prescribed baryons may be a smooth core; a
point source is also allowed with its fixed self-energy subtracted. Cold
particles have ordinary inertia, and only their tethered self-gravity is
cancelled by the declared critical counterterm. Stiffness is zero.

The logical chain is:

`declared reciprocal energy -> actual material shell accelerations -> circular
balance -> independent two-species displacement equations -> positive weighted
second variation -> coherent radial linear energy bound`;

`monotone target C + inner/outer taper -> finite admissible profiles + positive
angular momenta + exact law annulus -> stationary singular circular measures`;

`additional saturation/fraction restriction -> positive background epicyclic
coefficient -> local fixed-field radial orbit stability and positive radial
splitting second variation`;

`global M<=C and finite baryonic/cold stock -> integrable species potentials
-> uniform negative circular specific-energy bounds`.

No empirical score or derivation of a population fraction is a leaf of this
argument. The total law amplitude on the annulus is selected in `C`.

## Independent displacement reconstruction

For `mu_i=M_i'`, a first-order material push-forward has
`delta M_i=-mu_i xi_i`. At the position of a displaced tethered shell its own
enclosed `T` is constant. The fixed baryon *profile*, however, changes along
the shell by `B'xi_t`; the free mass changes by `mu_f(xi_t-xi_f)`. Therefore

    Delta_t u=-2u xi_t/r,
    Delta_t a_t=-G B'xi_t/r^2-G mu_f(xi_t-xi_f)/r^2
                 +2G(B+F)xi_t/r^3-2uR'xi_t/r.

The angular momentum attached to the baseline shell stays fixed. Its
centrifugal acceleration changes by `3a_t xi_t/r`, using
`ell_t^2=-r^3a_t`. Adding that term gives exactly the source's tethered
equation, with

    kappa_t0^2=G(B+F)/r^3+GB'/r^2+(2uR'-3R)/r.

The analogous free-shell calculation keeps its own `F` fixed and changes
`T` by `mu_t(xi_f-xi_t)`. It yields the other displayed equation and

    kappa_f0^2=G(B+T+F)/r^3+GB'/r^2.

Both relative-displacement cross forces and both `B'` terms are correct.
Holding the baryonic enclosed number constant during a shell displacement
would have been incorrect; the source does not do that.

Direct differentiation of the full remainder gives

    R'=u(2a0-u)/(a0-u)^2,
    2uR'-3R=u^2(a0+u)/(a0-u)^2>=0.

This is an exact full-domain identity. Its leading small-u term recovers
the cubic parent; no small-u expansion is needed for the sign.

## Independent energy and coercivity reconstruction

Differentiating the displayed energy gives the claimed accelerations. The
primitive `w` differentiates to `R`. Its radial mass Hessian has

    H_tt=G R'/r^2,  H_tf=H_ft=-G/r^2,  H_ff=-G/r^2.

The material push-forward also has
`delta^2M_i=(mu_i xi_i^2)'`. Its contribution to the second variation is
`-int a_i' mu_i xi_i^2`, with zero boundary terms at the smooth cold edges.
The fixed-angular-momentum orbital energy adds
`-3int(a_i/r)mu_i xi_i^2`. Substitution therefore gives the source's
intermediate second-variation expression directly.

In its tethered diagonal, the background term
`-G R' mu_t/r^2` cancels the own-source Hessian term. The free own-density
term also cancels. The two remaining diagonals and reciprocal mixed terms
combine to

    W''=int [mu_t kappa_t0^2 xi_t^2+mu_f kappa_f0^2 xi_f^2
             +G mu_t mu_f(xi_t-xi_f)^2/r^2]dr.

Thus the displacement derivation and variational derivation agree without
freezing either cold source. Every coefficient is bounded on the finite
hollow support because of smoothness and the uniform saturation gap. The
weighted operator is symmetric in `L^2(mu_t dr) direct_sum L^2(mu_f dr)` and
is bounded on the whole space, hence self-adjoint there. Its lower bound is
`G B_*/R^3`. The conserved quadratic linear energy consequently controls
both the weighted displacement and radial velocity for all times of the
bounded linear equation.

This is the stated coherent linear Lyapunov theorem. The norm does not
control derivatives of displacement and cannot prevent nonlinear shell
crossing. A singular circular measure does not inherit arbitrary warm
Vlasov stability merely from this quadratic form.

## Finite smooth construction and stationary measure

I independently differentiated `R(u_b)=s_b` and obtain

    C'=2r/G [u_b-s_b u_b']+B'u_b',
    u_b-s_b u_b'=a0 u_b/(2a0-u_b)>0.

Hence `C` increases strictly wherever `B>0`; the proposed positive target
is an actual enclosed positive species candidate on the annulus, rather
than an unchecked enclosed-mass excess.

The inner taper is a product of increasing nonnegative `C` and increasing
smooth step. It has nonnegative derivative, lies below `C` and joins it
smoothly. In the outer taper, `M'=C'(1-S)` lies between zero and `C'` and
vanishes flatly at the outer edge. Integrating that inequality from `r_2`
shows `M<=C`, including after `M` becomes constant. Both joins are smooth
because the step is flat at its endpoints. All cold mass is finite.

For `T=fM,F=(1-f)M`, `0<f<1`, the tethered acceleration source obeys
`u<=f u_b<f a0`. Monotonicity of `R` then gives
`R(u)<R(u_b)=s_b`. Consequently both circular angular momenta are strictly
positive wherever matter is present, and the uniform saturation gap follows.
These checks establish the actual domain needed for the bounded operator;
the positive second variation alone would not have established it.

Where `M=C`, ordinary tracers see `s_b+u_b`, exactly the requested full law.
This is an imposed finite-annulus total-mass profile. It is not an attractor,
an abundance prediction, a fixed observed population fraction, or a score
against galaxy/dwarf/cluster data.

The circular phase-space measure has the correct normalization: the velocity
element `dv_r v_perp dv_perp dtheta` supplies exactly `2pi v_ci`, cancelling
the displayed prefactor. Every orbit stays on its own circular radius in
the self-consistent stationary force; a uniform distribution of orbital
planes and phases is therefore stationary as a measure. It is singular in
radial velocity and tangential speed, with zero radial dispersion.

The subtracted energy is finite. Near zero the cold contributions vanish.
At infinity finite baryonic and cold masses give gravitational integrand
`O(r^-2)`; `w(u)~u^3/(3a0)` gives remainder integrand `O(r^-4)`. Circular
kinetic energy is finite on the compact hollow support. This is not the
infinite-mass formal isotropic comparison audited in `reciprocity/AUDIT.md`.
Its exterior force integrals do not themselves establish a physical medium/
vacuum interface in the original relativistic theory.

## Splitting second variation and local test-orbit condition

For particles initially at one shell radius, the first enclosed-mass
variation depends on the mean displacement, and the second on its second
moment. Splitting that moment into mean-square plus variance yields the
source's additional variance term with coefficient
`kappa_bg,i^2=-a_i'-3a_i/r`. This is a positive second-variation statement
under its extra sign condition, not a solved splitting evolution theorem.

With constant partition,

    kappa_bg,t^2=kappa_t0^2+GM'/r^2[(1-f)-fR'(u)].

Since `1+R'=a0^2/(a0-u)^2`, its displayed condition
`u<=a0(1-sqrt(f))` makes the bracket nonnegative. The uniform bound
`u<=f a0` gives the independent algebraic estimate

    (1-f)-fR'(u)>=(1-3f+f^2)/(1-f)^2.

It is sufficient for `0<f<=(3-sqrt(5))/2`; equality at the fraction bound
still leaves the strict positive baryon term in `kappa_t0^2`. The free
background coefficient is positive without this fraction restriction.
Finite-total-mass baryons also allow the optional support-far-out subfamily
for any fixed `f<1`, as the source states.

For a fixed background and fixed test-particle angular momentum, the second
derivative of the effective radial potential is exactly `kappa_bg,i^2` at
the circular radius. Therefore positivity establishes a strict local radial
minimum and `(ell_ci^2)'=r^3 kappa_bg,i^2>0`. This is a valid fixed-field
local orbit result. It does not prove self-consistent kinetic stability,
nonlinear splitting stability or a finite-temperature continuation.

## Uniform negative circular specific-energy reserve

Let `v=GM/r^2`. The source explicitly defines this as an acceleration.
For `0<f<1`,

    R(fv)=f^2R(v)(a0-v)/(a0-fv)<=f^2R(v)<=f^2s_b.

The stated upper and lower bounds on the actual inward tethered force follow.
The finite-total-mass baryonic hypothesis is needed here as well as finite
cold mass: it makes the exterior force integrable and allows
`Phi_i(infinity)=0`. Monotone enclosed masses then give the source's lower
bound on `-Phi_i(r)`.

Combining that lower bound with the upper bound on circular kinetic energy
`rh_i/2` gives, with the correct signs,

    E_ct<=-G[(1/2-f^2)B+F/2]/r,
    E_cf<=-G(B+M)/(2r).

For `f<1/sqrt(2)`, the positive baryonic lower stock and finite outer radius
give both uniform negative caps as written. The fraction `f=1/64` yields
`1/2-f^2=2047/4096` exactly. These are individual circular specific energies
in their actual stationary species potentials. Their sum is not the
counted total system energy; pair energies would be counted differently.
The source now makes that distinction explicit.

The resulting gap is a useful ingredient for a later smoothing argument.
It does not prove that smoothing preserves the self-consistent forces,
exact annulus, positivity, energy slope or stability. No all-time smooth
warm target is discharged by it.

## Verdict matrix, provenance and next check

| Obligation | Audit result |
|---|---|
| direct independent shell displacement equations | passed |
| full-R mass Hessian and cross-square second variation | passed |
| bounded weighted linear operator and coercive gap | passed under stated hollow/gap/regularity hypotheses |
| finite positive smooth spatial profiles and exact law annulus | passed; annulus and partition are selected inputs |
| stationary circular measure normalization | passed; singular phase-space scope |
| optional radial splitting second variation | passed under the extra saturation bound |
| fixed-field local radial test-orbit stability | passed under the same bound |
| circular negative specific-energy reserve | passed under finite exterior stock and fraction restriction |
| smooth warm phase-space continuation and kinetic stability | not established |
| nonlinear all-time behavior or shell-order preservation | not established |
| physical source/partition/formation, finite stiffness and metric | not addressed |

This is a same-team separate-agent audit. The reviewer reconstructed the
general displacement/energy formula before reading this draft and shared
the reconstructed formulas and scope cautions with the author/coordinator.
The review is therefore not blind or fresh-context. The arguments here are
analytic; no finite scientific computation or experiment was used to infer
a universal statement. Hashing and source reads are provenance only.

The next distinct proof obligation is the one stated in the source:
construct a smooth finite phase-space family near these circular measures,
control the change in its self-consistent full-remainder potentials and law
annulus, and prove an appropriate stability theorem. The orbit gap and
positive second variation do not choose that missing continuation.
