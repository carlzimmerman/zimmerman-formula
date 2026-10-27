# Reversible assembly work and its limits

This is an effective Newtonian construction and self-review. It is not a
microscopic derivation. Source snapshots are under inputs/ and model.py.
The scale a0 is the canonical parent value; kappa is not derived here.

## Positive kinetic completion

Introduce positive internal inertia I and baryonic cyclic angles theta_i.
Let R=sum_b m_i r_i/Mb and a=alpha/Rhalf0. Take the ordered angular kinetic
terms to be

    L_ang = sum_b (m_i r_i^2/2) (theta_dot_i-a x Rdot)^2.

Together with ordinary radial and I xdot^2/2 kinetic terms, this is positive
definite for positive masses, radii and I. At fixed canonical momenta j_i,
theta_dot_i=j_i/r_i^2+a x Rdot. Subtracting sum m_i j_i theta_dot_i gives

    L_R = K_rad + I xdot^2/2 - U_eff - a J x Rdot,
    J=sum_b m_i j_i, lambda=a J.

Here U_eff contains the ordinary centrifugal energies, gravity, and the
same positive field/barrier potential as the two-state parent. Random
angular support is included as a separate fixed centrifugal contribution.
This completion explains the signs of the reciprocal velocity coupling;
it does not identify an actual microscopic rotor or local interaction.
The global mass-weighted R is a nonlocal collective approximation. The
phase inertia, alpha, drag normalization and barrier are postulates.

With Rayleigh dissipation (Gamma Rdot^2+eta xdot^2)/2,

    m_i rddot_i = -U_eff,ri + (lambda xdot-Gamma Rdot)m_b,i/Mb,
    I xddot = -Ux,x -lambda Rdot-eta xdot,
    Qdot=Gamma Rdot^2+eta xdot^2.

Multiplying by velocities cancels the two lambda terms exactly. Hence
E=K_rad+K_rot+I xdot^2/2+Ug+Ux+Q is constant. Initially x=xdot=0;
negative Rdot gives positive xddot for positive J. No prepared T seed or
external conversion work is inserted. J reversal and x reversal leave
q=sin^2(pi x/2) unchanged. At alpha=0 exact F remains F.

At fixed radii the total positive field energy still makes F preferred.
The finite-inertia coupling can cross a barrier only by paying with
mechanical energy. It cannot evade the bound in BARRIER_BOUND.md.

## Contraction-dependent protection

FT-I3 replaces fixed C=f^2 by C(R)=f^2 Rrot/(R+Rrot), with
Rrot=Jabs^2/(G Mb^3). This is an assumed baryonic virial estimate, not
measured velocity dispersion. The extra baryon force is

    - (dUx/dC) (dC/dR) m_b,i/Mb.

It is essential: an externally prescribed time-dependent gate would inject
unaccounted work. The code evaluates the potential's linear coefficient in
C and adds its exact radial derivative. The full energy directional
derivative tests this force with phase and radial motion together.
Both barrier and this new force vanish at uniform pure T/F. In a mixed,
moving state, neither the gravitational monopole nor a high q alone proves
the observed rotation-curve relation: there are additional mechanical forces.

## Angular transport

FT-I4 lets the ordered canonical j_i evolve. A symmetric nonnegative kernel
Kij and positive viscosity nu produce

    dot j_i=nu sum_j m_j Kij (Omega_j-Omega_i), Omega_i=j_i/r_i^2.

Antisymmetry gives sum m_i dot j_i=0. Multiplication by m_i Omega_i gives

    sum_i m_i Omega_i dot j_i
        = -(nu/2) sum_ij m_i m_j Kij (Omega_i-Omega_j)^2.

Adding the opposite positive heat to Qdot preserves the full energy identity.
The common rotor shift in physical angular velocity cancels from differences.
lambda remains constant because total J remains constant. Individual j_i
need not remain constant, so FT-B1's angular-momentum hypothesis no longer
holds; the route changes a proved obstruction rather than rerunning it.

The fixed random angular support and initial f used by C are model inputs.
This is not a self-consistent evolution of a 3D velocity distribution or of
local measured vorticity. A viscosity coefficient has not been matched to
gas or a specified microscopic carrier. Uniform conversion still suppresses
the spatial structure and nucleation that a realistic formation process needs.

## Diagnostics and interpretation

The initial halo is an independent truncated Plummer profile, not a scaled
solution of the acceleration law. Both species source actual Newtonian mass.
The RAR diagnostic compares G Mtotal/r^2 with the parent law applied to
current baryons; no target acceleration drives the shells. During pumping
there are additional baryonic forces, so passing this gravitational-only
diagnostic would be necessary for the intended settled state, not sufficient.
No run failing formation can be promoted using a coincidental RAR match.

Free-mass binding uses an instantaneous potential and unchanged cold angular
momenta. It is not eternal retention. The spherical softened shells, uniform
phase and fixed noise-free dissipative closures are severe restrictions.
Positive energy and good numerical conservation establish consistency of
these finite models, not the existence of the mechanism in nature.
