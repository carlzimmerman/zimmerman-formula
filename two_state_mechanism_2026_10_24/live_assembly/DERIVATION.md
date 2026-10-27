# Reciprocal assembly work with live gravity

This is a constructed collective effective model. It is not a microscopic
derivation or a three-dimensional galaxy simulation. The live calculation
replaces frozen density, but restricts geometry and the internal phase.

## Live degrees of freedom and common energy

Each spherical shell has positive mass mi, centroid radius Ri, radial speed
vi and conserved specific angular-momentum magnitude li. Orbital orientations
determine a net angular-momentum coherence f. The radial monopole calculation
keeps the same li magnitudes when f changes, so random versus aligned angular
motion has the same kinetic energy. It does not evolve disk flattening.

The shell cumulative mass kernel is S(r/Ri), a quintic smoothstep increasing
from zero at r=.75 Ri to one at r=1.25 Ri. This is a softened shell Hamiltonian,
not an exact fluid model of the changing shell thickness. Both matter states
source the same Newtonian mass M(r). Only T sources MT(r)=q Mc(r), with
q=sin²(pi x/2). The single collective x suppresses spatial phase instabilities;
it must not be used to infer their absence in the unconstrained model.

In units G=Mb=b=1, kappa=a0 b²/(G Mb), define

    K = sum_i mi [vi² + li²/Ri²]/2,
    Ug = - integral_0^infinity M(r)²/(2r²) dr,
    z = q Mc(r)/(kappa r²),
    w(z) = -log(1-z)-z,
    F(z) = z²/(1-z),
    s(x) = sin²(pi x)/pi²,
    Ux = kappa² integral r² [w(z)+beta C s(x) F(z)] dr,
    E = K+Ug+Ux+Q.

C=f² is a conserved collective circulation statistic under central forces.
It is not the earlier local vorticity statistic. The barrier is now a
collective field term over all space, rather than a material-only local
interaction. This change and the uniform phase are substantive approximations.
The spatial-gradient term vanishes identically in this restricted sector.

The code differentiates these same energies for every shell radius and x.
There is no imposed MOND acceleration on the particles. The gravitational
acceleration used for the RAR diagnostic is the actual G M(r)/r². Beyond the
quadrature boundary gravity is integrated analytically, and field energy is
integrated using t=1/r. Saturation z>=1 is rejected, never clipped.

## Work-paying conversion

Let vbar=sum_b mi vi/Mb. The nonnegative Rayleigh function is

    R = Gamma (vbar + A C xdot)²/2 + eta xdot²/2,

where Gamma>0, eta>0 and A>=0. In code `A` already includes C. The internal
coordinate is overdamped, so

    xdot = -(Ux_x + Gamma A C vbar)/(eta + Gamma A² C²),
    mi vdot_i = -partial_Ri(Ug+Ux) + mi li²/Ri³
                 - Gamma (vbar+A C xdot) mi/Mb    [baryons only],
    Qdot = Gamma (vbar+A C xdot)² + eta xdot².

Contraction vbar<0 can drive x upward from exactly zero. It also experiences
the reciprocal force; the source of the energy is mechanical motion and
gravitational work, not an unaccounted conversion reward.

Writing slip=vbar+A C xdot and B=A C, direct substitution gives

    d(K+Ug+Ux)/dt = -Gamma slip*vbar + Ux_x*xdot
                   = -Gamma slip² - eta xdot² = -Qdot.

The signed pump work rate is -Gamma B slip*xdot. The internal-coordinate
identity is Ux_x*xdot = pump_rate - eta xdot². Ux can additionally change
through shell displacement, whose opposite work is in the radial force.
Thus cumulative pump work is not equal to the total field-energy change.
Q remains an energy receiver with unspecified microscopic carriers. Its
rest-mass contribution to gravity is neglected in this Newtonian treatment.

All dissipative forces are radial, so they conserve shell angular momentum.
Spherical shells have zero net vector linear momentum; this does not test
recoil in a nonspherical medium. A common velocity boost of the entire system
is removed by defining radii and radial velocities about its center.

## Controls and diagnostics

At x=0 the parent field/barrier derivative Ux_x vanishes. With A=0 or C=0,
xdot=0 exactly even when the density evolves. Passive collapse in the old
gradient closure therefore cannot initiate T from exactly F. This is a
structural obstruction to that closure, not to assembly interactions generally.

For the reciprocal interaction, receiver energy, total energy and signed
pump work are integrated as separate variables. Finite differences check
both radial and phase energy derivatives. Resolution and tolerance studies
are needed beyond the analytic conservation identity.

A free shell is labeled snapshot-bound when

    (vi²+li²/Ri²)/2 + Phi_i < 0,

where Phi_i is the shell-kernel average of the current Newtonian potential,
including all positive mass. Report its free mass (1-q)mi, not its total mass.
This is an instantaneous diagnostic in a changing potential. True long-term
retention, and enough mass for a measured dwarf or cluster, require additional
live tests and observational data.

The RAR comparison uses the same parent's law applied to current baryonic
mass alone. It is a comparison, not a force imposed by the integrator. A
global coherent x does not allow the local T redistribution needed to derive
the static RAR, so a RAR failure here cannot refute a spatially resolved model.
