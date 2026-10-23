# Coupled nonlinear field evolution: measured early stage, no relic yield yet

The requested **final surviving cold abundance has not been calculated**.
What is now calculated is a three-dimensional nonlinear early stage with both
complex fields and every original potential term retained. It develops
substantial spatial Phi structure, but remains radiation-like and partly
coherent. X is still overdamped. Its output does not justify a dilute kinetic
handoff, and no cold population has been inserted into the collapse solver.

## Result

Five periodic lattice evolutions were completed: three 32^3 controls, a 64^3
run and a 96^3 refinement. All evolve to conformal time z=200; the final scale
factor is 501.403. The fine run gives, averaged over z=150--200:

| Observable | Result |
|---|---:|
| Inhomogeneous Phi variance / total Phi mean square | 0.421916 |
| Coherent mean-field contribution / total mean square | 0.578084 |
| Phi pressure / energy, ratio of time-integrated quantities | 0.339848 |
| Phi potential / total Phi energy | 0.271034 |
| Final change in squared physical homogeneous X amplitude | about +1.03e-11 |
| Final H/M | 2.67347e7 |

These variance fractions are **not particle or mass fractions**. Their
20-unit rolling average first exceeds one half at z=76, then varies; there
is no permanent 50% fragmentation or remnant claim. The tiny X change is a
finite-run diagnostic, not a certified physical prediction at eleven-digit
precision. An otherwise identical g=0 control also leaves its homogeneous
physical X amplitude constant, as expected in this early massless limit.

The simulation demonstrates nonlinear growth and saturation of spatial
structure in the specified source realization. It does not demonstrate full
thermalization, irreversible breakup into independent particles, or a cold
bound object. All resolved nonzero momenta at the endpoint satisfy
p/m >= 2.10e9. The homogeneous mode cannot be counted as a cold population:
X has not started its massive oscillation regime, and Phi still has a large
quartic interaction energy and radiation-like pressure.

The inferred H=M epoch would be at a=2.59254e6, another factor 5170.6 in
expansion beyond this endpoint, or z approximately 1.03618e6. This is a
scale-separation problem, not something fixed by taking a few more early
lattice timesteps. A validated averaging or kinetic description is required
to cross it economically. No such closure is assumed in these results.

## Equations actually evolved

The potential is unchanged:

\[
 V=m^2|\Phi|^2+M^2|X|^2+g(X^*\Phi^2+X\Phi^{*2})+
 \lambda|\Phi|^4.
\]

All four fields are canonical real components,
Phi=(f1+i f2)/sqrt(2), X=(x1+i x2)/sqrt(2). Set
q=a(f1,f2,x1,x2)/Fmax, z=sqrt(lambda) Fmax eta, and use spatial coordinates
y=sqrt(lambda) Fmax x. The prescribed radiation background is a=1+bz,
b=Hinf/(sqrt(lambda) Fmax). With primes denoting z derivatives,

\[
 q_s''-\nabla_y^2 q_s+\partial U/\partial q_s=0,
\]

\[
 U={a^2\over2}(\hat m^2(q_1^2+q_2^2)+\hat M^2(q_3^2+q_4^2))
 +{(q_1^2+q_2^2)^2\over4}
 +ca[q_3(q_1^2-q_2^2)+2q_4q_1q_2],
\]

where hat m=m/(sqrt(lambda) Fmax), hat M=M/(sqrt(lambda) Fmax),
c=g/(sqrt(2) lambda Fmax). The retained numerical parameters are the existing
m=0.001 GeV, M=2m sqrt(1+0.02^2), g=2.168e-6 GeV and lambda=0.00881292.
No coupling or mass was enlarged to accelerate conversion. Fmax/H=4.257455
and c=3.03884e-15 for the selected source patch.

A nearest-neighbor periodic spatial Hamiltonian and velocity Verlet time
integration are used. The explicitly time-dependent Hamiltonian obeys
dEconf/dz=partial U/partial z; its integrated work is tracked. The discrete
U(1) charge is the volume average of
q1 q2' - q2 q1' + 2(q3 q4' - q4 q3').

Physical energy and pressure use q'-bq/a for the kinetic term. This removes
the spurious conformal kinetic energy of a frozen physical field. The common
positive factor lambda Fmax^4/a^4 cancels from the reported pressure and
energy fractions. No physical X abundance is inferred from conformal energy.

## Initial state: vacuum-motivated, conditional, not an assumed cold seed

This is a **classical-statistical approximation**, not an exact quantum-state
evolution. Hinf=1.3445177278709404e10 GeV and the inflation/reheating history
remain imposed inputs. To avoid simply reusing the previous field-only sample
and guessing its spatial noise, this run constructs a new explicitly
specified finite-band source:

1. Begin all four coarse fields at zero. Evolve the original potential drift
   with horizon-crossing noise dW/(2 pi) for 55 e-folds, using 4096 patches,
   dt=0.01 and PCG64 seed 2026102201.
2. Evolve five further drift-only e-folds. Select the patch closest to the
   median Phi and X squared amplitudes by a fixed log-distance rule. It is
   patch 1773, not a patch selected for a favorable fragmentation outcome.
   Rotate the global U(1) phase to make the coarse Phi real. The end values
   in units of H are (1.204493, 0, -1.340917, -0.377776).
3. Add resolved Gaussian mode coordinates and momenta from de Sitter Hankel
   covariances in a constant local-background approximation. The effective
   squared masses are 3 lambda f^2, lambda f^2, M^2, M^2. For k/H at the
   radiation match, u=sqrt(pi)/2 H_nu^(1)(k/H), with its conformal derivative
   retained. Correlated coordinate/momentum sampling uses the Wronskian;
   physical velocities are not arbitrarily set to zero. The mean velocity
   is the potential slow-roll drift.
4. Retain the same 364 nonzero Fourier modes in all refinements, spanning
   k/H=0.07848--0.34207, with Fourier seed 2026102202. A common set of Fourier
   coefficients guarantees identical band-limited initial realizations on
   32^3, 64^3 and 96^3 meshes.

This procedure does **not** supply a complete inflationary quantum state.
There is an unresolved IR interval between the coarse cutoff exp(-5)H and
the box fundamental, and UV vacuum modes are omitted. The local-background
Hankel approximation ignores the time variation and nonlinear correlations
of the full stochastic background. One representative patch and one Fourier
seed are not an ensemble prediction. The classical realization's conserved
charge is not a measurement of quantum vacuum charge or evidence of an
asymmetric relic. These limitations must accompany every cosmological use.

No cold particle density, velocity distribution, or late source abundance is
specified anywhere in the initial conditions. However, “not assuming a cold
seed” must not be confused with “deriving every initial-state approximation.”

## Number-changing reactions: what is and is not included

The cubic and quartic terms are active in the full classical field equations.
There is no imposed conservation of quasiparticle number and no restriction
to elastic scattering. This retains nonlinear field processes associated
with the action's number-changing vertices in the classical-statistical
regime. **It is not a complete quantum collision calculation.**

In particular, this simulation does not by itself reproduce all spontaneous
and inverse quantum gain/loss terms when modes become dilute. Finite-band
classical fluctuations cannot replace that missing physics. Classical
statistical approximations have known ultraviolet and late-time limitations;
see [Epelbaum, Gelis and Wu](https://arxiv.org/abs/1402.0115) and
[Berges et al.](https://arxiv.org/abs/1312.5216). Those references establish
general limitations, not the correctness of this particular matching scheme.

The previously derived vacuum threshold coefficient C=1.0181e14 GeV^-8 in
dot n+3Hn=-C n^4 is **not applied** to this field state. Its assumptions are
not met: the state has an order-one coherent component, substantial quartic
energy, and no established dilute nonrelativistic distribution. Applying a
separate sink would omit heating and inverse reactions and overlap with
nonlinear processes already represented by the fields. A numerical answer
obtained that way would not be a surviving abundance from the action.

The handoff assessment therefore records `cold_relic_yield: null` and
`cold_mass_for_collapse: null`, not zero and not an assumed target density.
This is the concrete remaining obstacle to the requested survival result.
It is not evidence that later cold material is impossible.

## Numerical checks and provenance

The original four-case run failed its all-case UV-resolution assertion:
32^3 puts about 29% of final gradient energy above 0.6 of the one-axis
Nyquist wavenumber. That failure is retained. The corresponding fraction is
0.6205% at 64^3 and 0.002473% at 96^3. The original coarse run is not presented
as a fully resolved spectrum.

The completed 96^3 run has maximum relative conformal-energy/work residual
2.85e-6 and absolute charge drift 3.06e-13. Between 64^3 and 96^3, the late
inhomogeneous-variance fraction changes by 0.000422, gradient-energy fraction
by 0.000233 and pressure/energy by 0.000203. These bounded observables pass
the stated absolute 0.02 assessment threshold. This is not an ensemble,
volume, initial-band or full quantum convergence claim.

Independent code controls reproduce the exact homogeneous quartic elliptic
solution and a free massless X solution, with a factor-four error reduction
when the timestep halves. Selected force components agree with independent
finite differences of the Hamiltonian to about 2.3e-9. The massless Hankel
variance agrees with its analytic expression to 1.6e-15 relative error.

Evidence records:

- `coupled_fragmentation_run/manifest.json`: valid, **failed** coarse UV test.
- `coupled_fragmentation_96_run/manifest.json`: completed.
- `audit_coupled_lattice_run/manifest.json`: completed exact/gradient controls.
- `assess_coupled_fragmentation_run/manifest.json`: completed numerical and
  handoff assessment; the latter deliberately does not assert a cold yield.

The scripts and exact input/binary hashes are recorded in those manifests.
The initial/final binary states and CSV histories remain beside the results
for continuation. These are internal numerical checks, not external review.

## Status

The early nonlinear field stage is now a reproducible calculation. It has
not supplied the requested final surviving cold mass. Carrying the state to
X oscillation and conversion requires a validated treatment of the large
time-scale separation, followed by quantum number-changing kinetics or an
appropriate nonequilibrium quantum-field calculation. A thermal distribution,
conserved number, or sudden conversion cannot be assumed to close that gap.
The scalar-carrier/identified-medium bridge required by the existing collapse
solver also remains unspecified. No collapse or Nobel-level novelty claim
follows from this result.
