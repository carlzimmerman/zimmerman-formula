# Loading the charged source from a rolling clock

Status: a homogeneous classical conservative model now starts with zero
source field and zero source velocity, loads a displacement from clock kinetic
energy, and prepares nearly circular charged motion. This removes the supplied
source displacement and initial phase from the initial data, by placing a
selected displacement direction and scale in the potential. It does not
explain the clock reservoir's origin or establish the repository's full
cold-energy medium.

## Positive autonomous potential

Write chi=(X+iY)/sqrt(2), clock sigma=sqrt(J)L s, and tau=Mt. With source
coordinates x=X/L and y=Y/L, the dimensionless homogeneous potential is

    V/(M^2 L^2) = [(x-f(s))^2+(y-f(s))^2]/2 + (3/2) W(s)y^2.

W is the compact anisotropy pulse from AUTONOMOUS_CLOCK.md. Before that pulse,
f(s) first increases slowly from zero to one and then falls rapidly to zero.
For h(z)=10z^3-15z^4+6z^5, rise width R and release width e=0.0001,

    f(s)=0                            for s<=-R-e,
         h((s+R+e)/R)                for -R-e<s<-e,
         1-h((s+e)/e)                for -e<=s<0,
         0                            for s>=0.

This is a prescribed function of a dynamical field, not prescribed time.
Both profiles have compact support and are C2. The clock motion and source
respond to one another. The equations are

    x'' = -x+f,
    y'' = -y+f-3Wy,
    J s'' = (x+y-2f) f' - (3/2) W' y^2.

The conserved dimensionless energy is

    Etotal = [x'^2+y'^2+(x-f)^2+(y-f)^2+J s'^2]/2 + (3/2) W y^2.

At s=-R-e choose x=y=x'=y'=0, J=10, s'=sqrt(12/J). Thus the source begins
at its zero-energy minimum and all energy Etotal=6 is in clock motion.
The clock has positive canonical kinetic energy; it is an explicit reservoir.
The construction does not extract energy from an empty vacuum.

## Embedding in the daughter-conversion action

To retain positivity when daughters are included, shift chi consistently
inside the earlier positive squares. Define
chi0(s)=L f(s)(1+i)/sqrt(2), Delta=M^2-4m^2>0, and use

    V = m^2 |phi|^2 + 4m^2 |chi-chi0|^2
        + |sqrt(Delta)(chi-chi0)+(g/sqrt(Delta)) phi^2|^2
        + lambda_rep |phi|^4 + (3/2) M^2 Y^2 W(s),

with lambda_rep>0 and canonical kinetic terms for all fields. At phi=0 this
reduces exactly to the source/clock potential above. Classical phi=0 is an
invariant subspace because the daughter force vanishes there. After both f
and W vanish, the potential is exactly the late charged repulsive model.
This is a proposed extension of that model, not a derivation from the repo.

The field-dependent shifted interaction during loading differs from the
previous preparation model. Its quantum fluctuation bounds and production
history cannot be copied from the previous pulse calculation without a new
audit. Positivity of the classical potential does not prove quantum stability.

## How phase and displacement arise

During loading W=0. The source difference d=x-y satisfies d''+d=0. Since
its initial displacement and velocity are zero, d remains exactly zero.
Thus equal real components follow from the symmetric force, without imposing
a nonzero initial source phase. Slowly moving the minimum lets the source
approximately follow it; rapid release leaves it displaced near x=y=1.
The clock loses the corresponding energy. The subsequent anisotropy pulse
converts this displacement into rotation.

The relative orientation of the loading force and the anisotropy is selected
by the interaction itself. This relocates phase selection into the potential;
it is not a symmetry-based prediction or a proof that arbitrary couplings
would prepare the correct phase. The scale L is likewise a model parameter.
The calculation tests exact symmetric initial data, not attraction of arbitrary
classical perturbations to that data.

## Numerical formation histories

For each R, minimize the final circular residual
(x'-y)^2+(y'+x)^2 over pulse width 1.25<D<1.38, with the pulse edge width
fixed at 0.01. Reintegrate the fixed optimum at tighter tolerance. No initial
source displacement or phase is varied in this optimization.

| Rise width R | Tuned pulse width D | Total duration Mt | Final source energy | Final clock energy |
|---|---:|---:|---:|---:|
| 50 | 1.31398359529 | 47.2274638 | 1.001399965 | 4.998600035 |
| 100 | 1.31465139583 | 92.8696619 | 0.999971437 | 5.000028563 |
| 200 | 1.31463367702 | 184.1560978 | 1.000008254 | 4.999991746 |

Energies are in units M^2 L^2; their initial total is 6. Approximately
one-sixth of the clock's initial energy is stored in the final charged source.
For u=0.001, M=2m sqrt(1+u^2), each final source has
eta=(Echi-mQ)/Echi approximately 4.99999625e-7. Tight-run circular residuals
are below 5.6e-10. These floating-point values do not prove exact circularity.

The tighter runs have maximum total-energy drift below 2.3e-11. All 42 checks
pass, including the energy transferred from the clock, symmetric loading,
positive clock crossing, circularity budget and agreement between relative
tolerances 1e-11 and 2e-13. `clock_loading_run/manifest.json` records the
script, contract and outputs and validates. This is self-reviewed numerical
evidence for three homogeneous histories, not a general existence/stability
proof for fluctuating fields.

## What is established and what remains

There is now a concrete classical route from a rolling energetic field and
an initially zero source to the cold charged reservoir used by the daughter
conversion model. It accounts for the energy source and selects a displacement
direction through its couplings. It is not a demonstration that classical
zero daughters become occupied: that requires the separate quantum mechanism.

The source amount is still set by L and the available clock energy. Selecting
L to reproduce a chosen density is fitting an input, not predicting the cosmic
abundance. The profiles, their orientation, and the pulse width are also chosen.
No inflaton identity, reheating history, primordial fluctuation spectrum or
observational viability has been established for this clock.

The sharp release adds a new fluctuation stage. Earlier vacuum-heating bounds
apply to the old isolated pulse and do not yet certify this complete loading
history. Spatial and quantum perturbations, consistent Friedmann evolution,
and the full chain through daughter production remain to be checked. The
carrier's halo transport, profile and acceleration/vacuum-density relation
remain independent unresolved requirements of the original goal.
