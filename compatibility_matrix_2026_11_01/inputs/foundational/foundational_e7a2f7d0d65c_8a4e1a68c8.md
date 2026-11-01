# MS27 result: a conditional restoring core with a conserving energy outlet

2026-10-27. The full requested mechanism remains **open**. We constructed and
checked a reduced model that actually transfers energy and relaxes about a
stable, constant-surface-density core. Its pressure response and active phase
are assumptions; the exact coefficient linking the endpoint to Lambda is not
derived. No production halo, observational refit or existing theory file was
changed.

The acceleration footings and kappa=1/2 are inherited adopted/fitted inputs.
No calculation here selects kappa or promotes it to a derived constant.

The useful change is to give core physics **two distinct jobs**: establish a
restoring equilibrium and carry away excitations. Turning off a scattering
rate cannot perform both jobs. The four bounded routes below establish which
ingredients work mathematically and where they still fail physically.

## 1. Why a multistream scattering switch alone does not stop a core

The [kinetic construction](kinetic_route/DERIVATION.md) uses a nonnegative,
state-dependent relaxation rate multiplying a Maxwellianizing collision
operator. It conserves cold mass, momentum and kinetic energy exactly and has
the usual entropy sign. It can isotropize local streams while spatial fluxes
exchange energy between the core and envelope. Calling this a kinetic
description does not assert a fundamental particle species; deriving it from
the cold field remains necessary.

However, a collision operator that vanishes still leaves free-streaming heat
flux. The executable gives an explicit full-rank beam distribution below the
proposed stress threshold with a nonzero energy flux. Moreover, ordinary heat
exchange with a large envelope destabilizes a negative-heat-capacity virial
core. A small enough envelope can stabilize temperature equality, but the
endpoint then depends on total energy and mass. These are exact obstructions
to the simplest stop-valve and passive-thermostat constructions, not to every
possible core mechanism.

The [gravothermal route](gravothermal_route/REPORT.md) checks these signs
independently and retains the scale-invariance obstruction: ordinary
Vlasov-Poisson gravity with fixed Lambda does not supply a universal core
surface density over arbitrary initial data.

## 2. A pressure response that supplies a restoring equilibrium

In a fixed relaxed phase, adopt the known logarithmic constitutive response

\[
u(\rho)=-A[\ln(\rho/\rho_{\rm ref})+1],\qquad
P=\rho u_\rho-u=A\ln(\rho/\rho_{\rm ref}),\quad A>0.
\]

This equation of state is an additional assumption, not an output of stream
mixing. Its hydrostatic equation has cored solutions. With
`theta=rho0/rho`, `r=xi sqrt(A/(4piG))/rho0`, it becomes

\[
\theta''+\frac2\xi\theta'=\frac1\theta.
\]

At the quarter-density radius, `theta=4`, we independently obtain
`xi4=5.84477267596`. Consequently

\[
\rho_0 r_{1/4}=\xi_4\sqrt{\frac{A}{4\pi G}}.
\]

The endpoint is a constant **surface density**, with different central volume
densities and core sizes allowed. The EOS/scaling is known from logotropic
models; the [source check](eos_route/SOURCES.md) identifies the exact literature.
Our new scoped work is its conditional combination with a reciprocal outlet
and explicit stability/activation audits, without adopting its global fluid
cosmology.

For a fixed-mass sphere with fixed external pressure, the contrast-four core's
fundamental radial mode has

\[
\omega_0^2=0.0903960232\,(4\pi G\rho_0)>0.
\]

The mode therefore has a restoring force. A separate finite-element
calculation agrees with the shooting calculation and finds the expected
instability above the first fixed-pressure mass maximum, at density contrast
`5.13395466`. This stability is **conditional on the barotropic response and
moving interface against fixed external pressure**. It is not a proof for an
accreting halo, live envelope or moving phase transition. Defining a core by a
quarter-density radius does not itself justify putting the phase boundary
there. The unbounded logarithmic profile also has the wrong infinite-mass
tail, so a finite envelope must be derived.

## 3. An actual reciprocal energy-transfer channel

Let q be the amplitude of that stable core mode and chi a propagating real
mediator. A density-weighted current coupling has the fixed-phase mode
projection

\[
L=\frac\mu2(\dot q^2-\omega_0^2q^2)
+\frac12\int[\dot\chi^2-c_\chi^2|\nabla\chi|^2]d^3x
+\dot q\int J(r)\chi\,d^3x,
\qquad J=g\,\zeta_0 n_0^2\nabla\!\cdot\boldsymbol\xi.
\]

Here zeta is a material active-phase label advected with the core, and xi is
the radial displacement shape. Retaining the label's perturbation cancels
the otherwise missing interface source. A smooth-interface limit is required
before using discontinuous field variables. No phase-activation law has been
derived by writing this label.

Variation gives both the wave source and its reaction:

\[
\ddot\chi-c_\chi^2\nabla^2\chi=J\dot q,\qquad
\mu\ddot q+\mu\omega_0^2q=-\int J\dot\chi\,d^3x.
\]

Their common Hamiltonian is positive in this reduced sector:

\[
H=\frac{(p_q-\int J\chi\,d^3x)^2}{2\mu}
+\frac{\mu\omega_0^2q^2}{2}+H_\chi.
\]

Thus the source's reaction is retained and energy is accounted for. With
outgoing waves and initially quiet chi, positive oscillation energy leaves
the core. The static endpoint remains at q=0 because this derivative
interaction adds no static restoring term. Radiating positive perturbation
energy around a stable pressure-supported core is different from cooling an
ordinary virial core's binding energy; the latter can drive contraction.
The core mode uses the constrained energy including the fixed-pressure
boundary-work convention.

The [spatial wave diagnostic](eos_route/wave_outlet.py) evolves the coupled mode
and radial mediator with the same compact source on two resolutions. In the
extended fine-grid calculation, after 350 synthetic modal time units:

| Initial perturbation energy now in | Fraction |
|---|---:|
| Core oscillation | 1.55% |
| Mediator inside the observation radius | 3.10% |
| Exported beyond the observation radius | 95.35% |

About **98.45% has left the core oscillation**. The total discrete ledger error
is below `7e-13`. Coarse/fine remaining-core fractions differ by `0.00111` of
the initial energy. The zero-coupling control retains its core energy.
These are finite linear-model results, with a specified outgoing boundary and
canonical spherical surface-energy convention; they are not a formation time
or halo-collapse result. The fine-grid incoming/outgoing characteristic-power
ratio at radius 70 is `3.79e-5`, four times smaller than the coarse-grid value.
This bounds numerical incoming-wave contamination in the measured channel;
it is not an exact transparent-boundary theorem. The half-line analytic outlet supplies a separate
conserving limiting example.

The first finite-source t=70 run transferred only 55.69% and failed the
declared 95% transfer check. It is preserved. The continuation extended time
and added an explicit outgoing flux boundary, retaining the original source
and coupling; no parameter was fitted to upgrade the short-time outcome.
An earlier serialization failure is retained separately. See
[the derivation and numerical record](eos_route/DERIVATION.md).

A further finite-amplitude, fixed-shape radius reduction was also executed.
Rest starts at 0.8 and 1.2 times the equilibrium radius both returned to the
same radius while exporting energy. This is a nonlinear mechanical example,
not a fluid-formation simulation. Its run retains a failed extra assertion:
the 1.2 start's energy was above the inner collapse barrier, so only its actual
trajectory, rather than the simple below-barrier proof, establishes return.
The potential remains unbounded toward zero radius, precluding a global
attractor claim. The complete derivation and failure are retained.
Away from equilibrium this frozen-shape ansatz also requires a boundary-layer
adjustment to satisfy the prescribed external traction; that adjustment is
not solved. The independent review checks the variational energy algebra,
not the claim that these are exact nonlinear fluid trajectories.

## 4. What stops this from being the requested full mechanism

To match the proposed surface density exactly, this constitutive law requires

\[
A_{\rm req}=\frac{a_0^2}{\pi G\xi_4^2}.
\]

It is `1.22318e-12 Pa` on canonical and `1.78644e-12 Pa` on the alternative
footing. Canonically,

\[
\frac{A_{\rm req}}{\rho_\Lambda c^2}=0.002329458.
\]

This is a **matching requirement**. Substituting it reproduces the target but
does not explain it. A published Planck-density-logarithm prescription gives a
nearby coefficient, but predicts a surface density about **23% higher** than
the canonical target. We did not adjust that prescription to force agreement.
One physical Lambda was used for this comparison; the alternative footing was
not assigned a different vacuum density to manufacture a normalization match.

The [field route](field_route/REPORT.md) makes the other gap precise. A healthy
local scalar can activate above kinetic stress and exchange energy, but its
threshold is a free ratio of couplings. An additive vacuum shift changes
gravitating Lambda without changing that threshold. Furthermore, multiplying
the logarithmic pressure by a stress gate is not a conserving shortcut: the
complete energy variation adds kinetic and pressure terms that can even reverse
the presumed force sign. The transition and its energy reference must be
derived as a whole. The active-phase calculation above avoids pretending that
those missing terms have been checked.

We then executed the next constitutive step, rather than leaving it as a
suggestion. Minimizing the simple healthy mediator's full canonical energy
gives `W_min proportional to K_p^(2/3)` at large canonical random-motion
energy. Along an adiabatic affine family `K_p proportional to rho^(5/3)`,
this produces `P proportional to rho^(10/9)`, not the logarithmic response.
Some coupling choices also yield negative reduced compressibility near
activation despite a locally stable scalar minimum. This particular mediator
therefore does not supply the assumed core EOS. Exact identities and a bounded
independent minimization/volume-variation check are retained in
[field_route/continuation](field_route/continuation/RESULT.md).

A globally active logarithmic EOS is already constrained by its cosmological
sound speed. Multistream activation might avoid that pressure before collapse,
but finite primordial dispersion, phase retention, the kinetic-to-field limit
and merger/infall perturbations remain untested. X54's specific homogeneous
exact-vacuum conversion bounds neither validate nor directly exclude this
momentum-carrying wave outlet.

## 5. Precise continuation

The useful next problem is a **complete cold-field phase energy** that yields
the logarithmic response (or another stable constant-column response), fixes A
relative to the total gravitating vacuum, and supplies the reciprocal current
coupling in one parent. It must specify the phase free-energy offset and its
stress-dependent variation, rather than attach a gate to the final force.
Then test a live finite envelope and nonlinear collapse. The current model
demonstrates that a restoring endpoint and a conserving outlet can coexist;
it does not derive those remaining microscopic and formation implications.

Detailed route outcomes, assumptions, source locators and execution manifests
are retained under the four route directories. No all-orders, causal,
cosmological or observational success is inferred from the bounded checks.
