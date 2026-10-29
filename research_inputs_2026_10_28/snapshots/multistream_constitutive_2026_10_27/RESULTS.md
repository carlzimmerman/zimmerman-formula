# Multistream constitutive law: what is derived and what is still missing

Research checkpoint MC27, 2026-10-27. Base `4aea352e6b`.

**The requested dynamical derivation is not complete.** We now have a positive,
finite-energy kinetic realization of an exact logarithmic **inner equilibrium**
pressure law. Two relaxation calculations also expose explicit expressions for
the candidate amplitude. Neither selects the required vacuum-normalized
coefficient or a stopping density. The classical multistream equations admit an
exact fixed-Lambda rescaling that prevents such coefficient selection from the
equations alone across unconstrained initial states.

This is stronger than the previous assumed-fluid construction, but weaker than
deriving the law from an initially cold field. No parameter match is counted as
a microscopic prediction. The adopted kappa=1/2 remains fitted/adopted.

## 1. Exact stress from streams does not close at the density

For cold streams indexed by a, total density and mean velocity are

    rho=sum_a rho_a,  u=sum_a rho_a v_a/rho,
    Pi_ij=sum_a rho_a (v_a-u)_i(v_a-u)_j.

Their velocities are independent state information. Shell crossing creates a
stress tensor but does not by itself give Pi_ij=P(rho) delta_ij. Even after
isotropization, the exact collisionless moment equations give

    Dp/Dt+(5/3)p div u+(2/3)div q=0,

where q is the third-moment energy flux. A material law p=A ln(rho/rho_ref)
with fixed A would require the specific transport relation

    div q=(3A-5p) div u/2.

For q=0, the adiabatic response is instead p proportional to rho^(5/3).
Consequently an equilibrium pressure curve cannot replace the transport
equation when testing damping, stability or the stopping mechanism. See
[kinetic derivation](kinetic_closure/DERIVATION.md).

## 2. A finite exact logarithmic inner equilibrium exists

We tested the naive marginal tail f(E)=C(E-E0)^(-5/2). It gives finite density
and a formal logarithmic pressure gradient, but its kinetic pressure diverges.
The positive lowered-escape completion has finite moments, yet changes the
logarithmic slope by a cutoff-dependent factor. That failure is specific to
that completion; it is not a no-go for an exact logarithmic inner interval.

An independent constructive route starts from the following C1 potential-density
curve, with x=(Phi-Phi_star)/Delta_m and rho_m=A/Delta_m:

    rho/rho_m = 1/x                for 0<x<=1,
                (3-x)^2/4         for 1<=x<=3,
                0                 for x>=3.

The right-Abel inverse is nonnegative and decreasing and has compact accessible
energy support. For every central x0>0 all local kinetic moments are finite.
The distribution has a derivative cusp at the matching energy; it is not
claimed to be a globally smooth analytic distribution.

Integrating its velocity moments gives

    P=A[-ln x+2/3]                for 0<x<=1,
    P=A(3-x)^3/12                 for 1<=x<=3.

Thus the inner equilibrium obeys exactly

    P=A ln(rho/rho_ref),  rho_ref=rho_m exp(-2/3).

This construction chooses a density-potential completion and inverts it. It
establishes realizability, not selection of that completion by violent
relaxation. A and Delta_m are free dimensional parameters.

We independently solved its full Poisson halo to its zero-pressure outer edge
for x0=.03,.1,.2,.249, neglecting Lambda locally. All four have finite radius,
mass and kinetic energy. The scalar virial error is below 5.1e-10. When x0<=1/4,
the whole quarter-density core lies in the exact logarithmic interval and

    Sigma_core=rho_c r_quarter
              =5.84477267596 sqrt[A/(4piG)].

The four independent core columns agree with this expression within 1.2e-11
relative. This recovers the earlier core relation from an actual finite kinetic
equilibrium. It does not transfer the earlier barotropic-fluid stability result
to the kinetic system. See [finite-halo evidence](finite_tail/run_compact/result.json)
and [construction details](kinetic_closure/DERIVATION.md).

An independent analytical review also proves finite outer radius, mass and
kinetic energy for every central 0<x0<3 in this constructed Newtonian family,
beyond the four numerical cases. In its outer region y=3-x obeys
y'=-m/r^2 and m'=r^2 y^2/4. A hypothetical infinite positive tail must have
y->0 and then y(r)>=m(r)/r, implying m'>=m^2/4 and a finite-radius blow-up,
contrary to a regular positive tail. Thus it reaches the vacuum edge at finite
radius. Matching to the exterior vacuum potential fixes its absolute energy
offset and gives a bound escape energy. See the
[independent review and full proof](normalization/REVIEW_COMPACT.md).

## 3. Two conditional amplitude formulas replace an unexplained constant

For homogeneous, dilute Lynden-Bell mixing in three velocity dimensions, take
a conserved phase-level content gamma(eta)=C/eta over a finite interval. Direct
integration gives a v^-5 intermediate tail and

    A=C/beta=2 K/[3 ln(eta_max/eta_min)],

where K is kinetic energy density in that homogeneous ensemble. The finite
mixture identity for K includes both end crossovers; identifying its
intermediate tail with a full logotropic halo is an additional step. For an
inhomogeneous halo, the global version involves mean energy and volume and
requires a spatial/escape-energy dictionary. Gaussian level data introduce
slowly varying corrections, and a single occupied level gives a different
distribution. Thus this is a mechanism under stated phase-level assumptions,
not universal forgetting of initial data. See [relaxation derivation](relaxation/DERIVATION.md).

A separately specified velocity-space diffusion model gives another exact
normalization identity. If D(v)=D0 v^4 and the stationary outward mass flux is
F=-4pi v^2 D partial_v f, integration over a finite driven band gives

    f(v)=F/(20pi D0) [v^-5-vout^-5],
    A_tail=F/(30D0).

This derives the exponent and amplitude from the diffusion and flux premises.
It does not derive those premises for cold self-gravity. A nonzero flux needs
a source, sink and energy reservoir; its drive power over the band is
F(vout^2-vin^2)/2 per spatial volume. The energy-only halo continuation of
this velocity tail must also be supplied. The cold homogeneous gravitational
response has a growing Jeans mode, so importing a stationary driven-plasma
diffusion calculation does not establish those premises.

The adopted canonical target uses Sigma=a0/(2piG) and
a0^2=G rho_Lambda c^2/4. Combining these with the exact inner core gives
the missing dimensionless relation

    A/(rho_Lambda c^2)=1/(4pi xi_quarter^2)=.0023294580123,

and, in the conditional diffusion route,

    F/(D0 rho_Lambda c^2)=.0698837404.

The second target additionally assumes that the dynamically obtained tail
continues into a core with this exact logarithmic coefficient and identifies
A_tail with that core's A. The mixing target has the same qualification. For
a different selected finite completion, the physical test is the jointly
predicted Sigma(A_tail, cutoff/state)=a0/(2piG); its required tail amplitude can
differ. No calculation here selects either the exact-log flux ratio or an
alternative physical completion. In the mixing route, the missing information
is K/(rho_Lambda c^2) together with the occupied phase-level span and the
tail-to-core map. These are now explicit physical quantities to calculate,
rather than a fitted A disguised as a pressure law.

## 4. Why Lambda alone does not select A in this classical parent

The following is an exact equation-level statement for Vlasov-Poisson-Lambda,
not a numerical fit. At fixed G,Lambda,c, set

    f_lambda(r,v,t)=lambda^-3 f(r/lambda,v/lambda,t),
    Phi_lambda(r,t)=lambda^2 Phi(r/lambda,t).

The Vlasov equation and

    Laplacian Phi=4piG rho-Lambda c^2

are unchanged. Density amplitude is unchanged, while P_lambda=lambda^2 P at
the corresponding point. Therefore an equilibrium with logarithmic coefficient
A has another allowed equilibrium with A_lambda=lambda^2 A at exactly the same
Lambda. Mass, radius and core column scale as lambda^3, lambda and lambda.
Restricting lambda to an open interval preserves nonrelativistic velocities.

This rescaling changes initial phase-level/Casimir data and boundary sizes. It
therefore rules out a universal coefficient from these equations alone for
unrestricted states. It does not rule out an explicitly specified primordial
distribution, a fixed physical boundary, quantum gradients, a new interaction
or a covariant parent that breaks the scaling and demonstrably selects a state.
Such an ingredient has to be calculated, not silently assumed.

Even at a given A, the compact logarithmic family has a range of central
densities. A universal core column is not a unique central density or an
automatic stopping rule.

## 5. Checks that did not supply the missing selection

- The lowered-tail family can be fitted to the earlier Planck-log amplitude at
  z0=.0332661. Its independently specified first fluid mass maximum is instead
  z0=.6710981, far outside the log regime. Neither is a kinetic attractor
  selection rule. See [cutoff calculation](finite_tail/DERIVATION.md).
- The conditional identification K=rho_Lambda c^2 and
  eta_max/eta_min=rho_Planck/rho_Lambda gives A/(rho_Lambda c^2)=.00235494,
  near the target. Both identifications are unproved: positive kinetic stress
  differs from vacuum stress, and a phase-space density ratio contains velocity
  factors. In this specific mixture the proposed huge phase-level range also
  puts most kinetic energy outside the nonrelativistic regime at the tested
  illustrative density contrasts. A relativistic completion must redo the
  normalization. Numerical proximity is not counted as a prediction.
- Eliminating positive affine internal modes constrains the resulting energy
  to be increasing and concave in canonical K. A density-linear energy term
  allows an inverse-designed logarithmic pressure on a restricted branch, but
  its coefficient is still inserted into the parent. Finite-temperature or
  finite-dimensional quantum logarithms do not fix the vacuum ratio. See
  [normalization proof and its exact exception](normalization/RESULT.md).
- The latest local two-measure symmetry test retains a fixed-vacuum response
  deformation after canonical normalization. Its shared-origin algebraic
  identity does not supply the missing action-to-multistream-pressure map.

## 6. Source calibration

The marginal-tail/log-pressure bridge is discussed in
[Chavanis, arXiv:2603.21302v1](https://arxiv.org/abs/2603.21302v1),
Sections III.3, IV.7 and V. That source explicitly leaves full distribution
selection open and does not calculate a vacuum-noise amplitude. Its plasma
white-noise example is conditional. One gravitational reference,
[arXiv:2411.18827](https://arxiv.org/abs/2411.18827), is withdrawn; the
[replacement v4](https://arxiv.org/abs/2506.02104v4) treats an inhomogeneous
accreting halo with red-noise and cusp assumptions. It is not a theorem of a
universal finite core pressure or its amplitude. Version-specific checks and
additional primary sources are recorded in relaxation/ and normalization/.

## 7. Evidence and open continuation

All new calculations use disjoint files under this directory. They include
independent velocity quadratures, stationary-flux normalization, full finite
halo integration, global virial balance, exact symbolic reconstruction and
finite-dimensional internal-mode checks. All seven bounded runs completed and
their manifests passed current-input hash validation. Run manifests state the
actual finite assertions and bounds. The compact construction and root halo
calculation received independent mathematical review; the analytic proofs are
human-readable arguments, not formal proof-assistant certificates. See the
[final verification record](VERIFICATION.json). There is no time-dependent core-formation simulation,
primordial-state selection, cosmological perturbation calculation or new halo fit.

The remaining objective is to derive one state-selection/transport mechanism
from an explicit microscopic parent: its occupied phase levels, reciprocal
energy exchange, diffusion/response spectrum and escape boundary must determine
A and the terminal central density together. Repeating an assumed log pressure
or tuning a cutoff does not advance that step. See [continuation handoff](NEXT.md).
