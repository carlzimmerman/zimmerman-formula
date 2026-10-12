# A dynamical clock can prepare the circular source

Status: a finite homogeneous classical construction closes the external-switch
energy-accounting gap in SOURCE_PREPARATION.md. It introduces one extra real
field and a deliberately chosen interaction. Initial displacement, phase and
clock motion remain inputs. It does not establish the cold medium's abundance,
identity, halo law or vacuum coupling.

## Autonomous action and equations

Keep the late two-complex-field action, with chi=(X+iY)/sqrt(2), and add a
canonical real clock sigma with no separate potential. For a chosen amplitude
scale L and dimensionless J>0 define s=sigma/(sqrt(J) L), and add

    Vclock = (3/2) M^2 Y^2 W(s).

This interaction is nonnegative. It explicitly breaks the chi charge symmetry
where W is nonzero. There is no externally prescribed time dependence.
Use the compact C2 window

    h(z)=10z^3-15z^4+6z^5,
    W(s)=0                       for s<=0,
         h(s/delta)              for 0<s<delta,
         1                       for delta<=s<=D,
         1-h((s-D)/delta)         for D<s<D+delta,
         0                       for s>=D+delta.

We use delta=0.01 and D>delta. This is a classical effective potential;
no renormalizable UV completion or quantum naturalness argument is asserted.
With daughters zero and time tau=Mt, write x=X/L and y=Y/L. Primes denote
tau derivatives. The equations are

    x''=-x,
    y''=-(1+3W(s)) y,
    J s''=-(3/2) W'(s) y^2.

The conserved total energy in units M^2 L^2 is

    H = [x'^2+y'^2+x^2+y^2+J s'^2]/2 + (3/2) W(s)y^2.

The source's dimensionless charge q=Q/(M L^2)=2(y x'-x y') obeys
q'=6 W(s) x y. These identities follow directly from the equations. They
provide distinct checks on the coupled dynamics.

Initially s=0, s'=1, x=sqrt(2)cos(theta), y=sqrt(2)sin(theta), x'=y'=0.
The source energy is 1 and clock kinetic energy J/2. In particular, J=10
requires five times the initial source energy in clock motion. This energy
cannot be omitted in a cosmological embedding.

## Backreaction matters, but a tuned crossing works

The entering clock slows as it raises the source's anisotropic potential.
It recovers energy during exit. Simply reusing the old rectangular-pulse width
D=pi/2 gives a substantial noncircular endpoint for a moderate-energy clock.
We solve two endpoint conditions x'=y and y'=-x by adjusting theta and D,
and reintegrate the resulting fixed parameters at tighter tolerance.

All three roots have theta approximately pi/4. The root adjustment is a
choice of model parameters and initial conditions, not dynamical attraction.

| Clock inertia J | Tuned window width D | Exit time Mt | Untuned initial eta at D=pi/2 | Tuned initial eta |
|---|---:|---:|---:|---:|
| 10 | 1.31463740265 | 1.58116460522 | 0.2456611 | 4.99999625e-7 |
| 100 | 1.54708898715 | 1.58082914857 | 0.00259535 | 4.99999625e-7 |
| 10000 | 1.57056100867 | 1.58079663651 | 7.49245e-7 | 4.99999625e-7 |

Here eta=1-q/[2 Echi sqrt(1+u^2)], u=0.001, and Echi is the dimensionless
source energy after the interaction vanishes. In the tuned cases Echi agrees
with its initial value 1 to within 2e-8, and the clock recovers its initial
speed to numerical precision. The source begins uncharged and finishes
nearly maximally charged. A subsequent common U(1) phase rotation maps its
circular trajectory to the source convention used by the conversion model.

For J=10 a positive width error of 0.001 raises eta to 6.92784e-6. This
confirms that finite backreaction can be accommodated, but accurate
preparation is still a tuning requirement. It does not establish robustness
to spatial fluctuations, initial clock-speed errors or quantum noise.

## Switching off and cosmological scope

After exit the clock has positive velocity and W=W'=0. In this homogeneous
Minkowski solution it keeps moving into the zero-interaction region forever.
The late classical charge symmetry and energy bound therefore apply to the
source/daughter subsystem again. The full action has an explicitly broken
symmetry in other regions of field space; this is not a proof of an exact
quantum charge symmetry in a completed theory.

For a homogeneous free canonical clock in an expanding universe,
(a^3 sigma-dot)'=0 in physical-time notation, so its kinetic density scales
as a^-6 after exit. It remains monotone for positive initial velocity. This
is a possible way for its kinetic contribution to become subdominant to a
matter-like source, but no Friedmann evolution or observational test has been
performed here. The earlier radiation-background simulation cannot be reused
unchanged while silently adding this clock energy.

## Evidence and what this does not solve

`autonomous_clock.py` integrates the clock and source together, splitting at
window edges to resolve the smooth ramps. It runs root finding at relative
tolerance 1e-10, reintegrates fixed parameters at 1e-12, and checks total
energy, the independently quadrature-integrated charge torque, circularity,
positive clock speed, parameter sensitivity and late decoupling.
All 27 checks pass. The largest absolute total-energy drift is 3.91e-7
(at total energy 5001); for J=10 it is 3.75e-10 (at total energy 6).
The torque-integral discrepancy is below 3.60e-10. The finite run and its
inputs are pinned in `autonomous_clock_run/manifest.json`. Evidence is
self-reviewed and numerical; passing checks do not prove general stability.

This replaces external switching by explicit conservative dynamics, with a
finite clock-energy cost. It still needs a prior origin for the displaced
source and clock motion, a phase-selection mechanism, a consistent expansion
history and perturbation analysis. It does not create matter from an empty
classical vacuum. Daughter quantum seeding and conversion remain separately
approximated in the existing work; they were not integrated during this pulse.
The repo's abundance, carrier transport, halo profile and acceleration law
remain unresolved.
