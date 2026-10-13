# Reverse reactions populate an initially empty unbound tail

Status: initial-time kinetic result for the existing daughter-only Plummer
halo. It includes Bose-stimulated decay of newly produced sources. It does
not compute permanent escape, an outward boundary flux, or a finite-time
halo evolution. The previous virial-capacity endpoint remains conditional
on no escape; that condition now requires a dynamical check.

## From source births to the unbound population

Use the same NR incoherent Boltzmann closure, leading mass mQ and initial
Plummer distribution as BOUND_HALO_REACTIONS.md. Write

    esc(r)=-Phi(r)/v_*^2,
    f(e,r)=A(r)(1-e/esc)^(7/2),  0<=e<esc,
    f(e,r)=0,                  e>=esc.

Here e is daughter kinetic energy in units m v_*^2 and v_*=u c. A newborn
source with dimensionless center-of-mass speed q has ec=1+q^2; its decay
products have energies

    e_hi=ec/2+q |cos theta|,
    e_lo=ec/2-q |cos theta|.

Born from bound daughters, ec<2esc. Thus at most one outgoing daughter is
unbound. Define a=esc-ec/2>0. Escape-capable directions exist if q>a,
with |cos theta|>z=a/q. The high-energy final occupation initially vanishes,
so the decay enhancement is exactly 1+f(e_lo), not (1+f)^2. The inverse
reaction into this source from that same outgoing pair has a zero initial
factor because the unbound parent occupation is zero.

The rate coefficient per occupied source for producing one unbound daughter
is therefore

    L_out = Gamma_NR integral_z^1 [1+A((a+q mu)/esc)^(7/2)] dmu,
    Gamma_NR = g^2 u/(16 pi m),

with zero result for q<=a. Gamma_NR is converted from natural units to
inverse time. There is no extra factor of two: integration over both signs
of cos theta counts the decay directions, and each qualifying decay makes
one unbound daughter. An independent antiderivative check uses

    L_out/Gamma_NR = (1-z)
       + A [(a+q)^(9/2)-(2a)^(9/2)] / [(9/2) q esc^(7/2)].

An energy-weighted coefficient L_E inserts (q mu-a) into the angular
integral. This is the positive specific orbital energy in units v_*^2,
not the total kinetic energy of the escaping daughter.

Let dR_chi be the initial source number birth rate resolved by position and
source momentum. Initially there are no sources, so their distribution
starts linearly in time. Integrating their subsequent decay gives

    Q_unbound(t)/Q = [m/(2 M_h)] integral dR_chi L_out * t^2 + o(t^2),
    E_orb,positive(t)/(M_h v_*^2)
                  = [m/(2 M_h)] integral dR_chi L_E * t^2 + o(t^2).

Equivalently, using the previously normalized differential source charge
production rate dcR=(2m/M_h)dR_chi, each coefficient is (1/4) integral dcR L.
This fixes both the identical-particle normalization and time-integration
factor. Source streaming, daughter depletion and reverse reactions modify
higher orders. The initial self-consistent potential change starts at t^3;
it does not change these t^2 production coefficients.

These statements assume the same factorized kinetic closure as the earlier
collision model. They are not a derivation of kinetic closure from coherent
field dynamics or an exact many-body calculation.

## Numerical result

For the existing 200-km/s central-dispersion test halo and microscopic
parameters, the finest quadrature gives

    Q_unbound/Q = 1.010074742e-4 [t/(1 Gyr)]^2 + o(t^2),
    E_orb,positive/(M_h v_*^2)
                = 1.769636211e-5 [t/(1 Gyr)]^2 + o(t^2).

The birth-weighted L_out is 0.002282609807/Gyr. The initial production-weighted
mean positive specific orbital energy is 0.1751985410 v_*^2. These are
initial derivatives expressed in Gyr units; they are not predictions at
1 Gyr, and no remainder bound or validity interval has been computed.

Radial/energy quadrature orders 16, 24 and 40 agree on the number coefficient
at better than 5e-9 relative. The angular number integral is checked against
its antiderivative; positive orbital-energy bounds and the prior independent
birth normalization also pass. The 32-point angular rule is not separately
refined; its number integral agrees with the analytic result, and its
energy integrand is smooth on the sampled intervals. The script records
9,733 individual checks, mostly repeated angular consistency checks; that
count is not a measure of physical validation. All pass, and the manifest
validates provenance. The mathematical interpretation is self-reviewed.

## Consequences for a proposed endpoint

The initially bound-only phase-space support is not invariant under the
retained reactions: newly occupied sources populate unbound modes at second
order. Such particles are still part of the total conserved system at this
stage. Positive orbital energy at creation is neither flux at infinity nor
proof of permanent escape. Subsequent collisions and changes in Phi can
recapture or redistribute them. The finite halo therefore needs explicit
transport of this tail before treating its bound mass as constant.

There is also a simple obstruction to using an ordinary global thermal
Bose-Einstein bath as an isolated finite-mass endpoint. For T>0, the usual
stationary detailed-balance ansatz has

    f_phi = {exp[(p^2/(2m)+m Phi-mu)/T]-1}^-1,
    F_chi = {exp[(P^2/(4m)+DeltaE+2m Phi-2mu)/T]-1}^-1.

For any admissible finite chemical potential and Phi tending to zero at
infinity, the daughter density tends to a strictly positive thermal value.
It therefore has infinite total mass. Sending mu to minus infinity empties
the gas; a zero-temperature condensate is a different case outside this
thermal argument. A cutoff, confinement, a sustained non-equilibrium state,
or explicit escape physics is needed for a finite halo. This is an
obstruction to that ansatz, not a uniqueness theorem for all stationary
solutions of the reacting gravitational system.

The next required calculation is an open-boundary, coupled source/daughter
and gravity evolution. The result here identifies a boundary channel that
such a calculation must retain. It does not establish a stable core, the
repo's halo profile, its vacuum coupling, or the cold-energy construction.
