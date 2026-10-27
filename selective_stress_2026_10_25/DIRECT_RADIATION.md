# Reciprocal conversion radiation: mechanism and restrictions

This is a new dynamical coupling, not the earlier supplied radial oscillator.
The full galaxy theory remains open. The direct source can be tested while
preserving a previously computed static branch because it vanishes at rest.

## Action, forces, and energy

In a stated medium rest frame let chi be a shift-symmetric massless scalar,
with positive time coefficient and positive propagation speed c_s. Let
jT=(rhoT,jTspace) be the T current. Add

    Lint = g partial_mu(chi) jT^mu.

If this current is exactly conserved, this is a boundary term and supplies no
bulk radiation. Conversion makes div(jT)=Gamma nonzero, so variation gives a
source proportional to Gamma. Total matter mass can remain conserved since
div(jF)=-Gamma. Shift charge includes both scalar momentum and g*rhoT.
This is a proposed effective operator; its coefficient, medium state and
microscopic conversion law are not derived.

For a collective converted fraction N(q), compact normalized source h(r),
and kinetic inertia I>0, the explicit reduced action is

    L = I qdot^2/2 - V(q)
        + integral [chidot^2-c_s^2 |grad chi|^2]/2 dV
        + g N(q) integral h chidot dV.

The equations, including reciprocal material force, are

    I qddot + V'(q) = g N'(q) integral h chidot dV,
    chiddot - c_s^2 Delta chi = -g h N'(q) qdot.

The chemical-potential shift for T at fixed carrier is -g chidot; F has no
direct shift. A free F reservoir must therefore be checked for conversion
under this pulse; no direct F coupling alone is insufficient to prove safety.
For conserved T transport the simultaneous canonical spatial-momentum shift
g grad(chi) must also be included. Its pure-gauge contributions cancel in the
Euler force; -grad(-g chidot) alone is not an additional material body force.
The nontrivial interaction is with conversion, div(jT), rather than a new
static force throughout the converted core.
For a mobile-fluid completion this statement uses the physical velocity
current and the complete canonical momentum square. A wave-field version
must use the corresponding spatial covariant derivative, including its
quadratic gradient term. Keeping only a linear coupling to a *bare* wave
current would omit that term and would not establish the positive Hamiltonian
or pure-gauge force cancellation asserted here. The collective q prototypes
have no spatial material transport and do not encounter this omitted term.

Canonical scalar momentum is Pi=chidot+g N h. The Hamiltonian is

    H=P^2/(2I)+V(q)
      +integral [(Pi-g N h)^2+c_s^2 |grad chi|^2]/2 dV.

It is bounded below whenever V is bounded below. Its velocity form is the
sum of the material and positive wave energies. It introduces no static
potential when chidot=grad chi=0 and Pi=gNh. In an isolated evolution the
corresponding shift charge must move outward; it cannot be silently deleted.

Multiplying the equations by qdot and chidot gives

    Hdot = -outgoing energy flux,
    d/dt integral [chidot+gNh] dV = -outgoing shift-charge flux.

The numerical sponge is a passive approximation to those fluxes. Its two
ledgers are tracked explicitly, separately from the scalar energy remaining
inside the computational domain. All tests begin with chi=chidot=0, so the
initial energy is actually the conversion potential, not an inserted wave.

## Why a stronger relativistic coupling alone is insufficient

For slow variation of N, define the positive Poisson solution -Delta U=h,
U->0 at infinity, and A0=integral hU=integral |grad U|^2. The quasistatic
scalar is chi=-g Ndot U/c_s^2. Integrating it out produces

    Delta I_N = g^2 A0/c_s^2 > 0.

Thus increased coupling changes the material motion. Omitting this reciprocal
added inertia would overestimate radiation.

For a normalized spherical source supported inside R, outside U=1/(4pi r).
The exterior field alone contributes A0>=1/(4pi R). Far outgoing waves obey

    chi = -g Ndot(t-r/c_s)/(4pi c_s^2 r) + finite-size corrections,
    Prad = g^2 Nddot^2/(4pi c_s^3).

For a linear harmonic N=A cos(omega t), energy E=Ieff omega^2 A^2/2 and
average power give an energy decay rate

    gamma_E = g^2 omega^2/(4pi c_s^3 Ieff)
            <= omega^2/(4pi c_s A0)
            <= omega^2 R/c_s.

This is a leading low-frequency, weak-damping harmonic statement, not a global
nonlinear radiation bound. It assumes a single reciprocal channel and includes
its inertia. It does not exclude rapid bursts, a different source geometry,
other interactions, or a nonrelativistic medium mode.

For a uniform sphere A0=3/(10pi R), giving gamma_E<=5 omega^2 R/(6c_s).
At fixed bare frequency Omega with eta=Delta I/I, omega^2=Omega^2/(1+eta),
so gamma_E=[5 R Omega^2/(6c_s)] eta/(1+eta)^2. Its maximum is at eta=1,
not arbitrarily large coupling.

For R=56.36 kpc, c_s=c, and *inverse angular frequency* 1/omega=100 Myr
(not a 100 Myr period), the uniform-sphere energy e-folding time is at least
65.28 Gyr in this approximation. Removing97.7191% needs at least246.8 Gyr.
This is a stated-timescale discriminator, not a measured galaxy-age result.

The finite-frequency audit computes the exact spherical retarded kernel

    A(k)=integral_0^(2R) p(d) exp(ikd)/(4pi d) dd,
    p(d)=3d^2/R^3[1-3d/(4R)+d^3/(16R^3)],
    Im A(k)=k |F(kR)|^2/(4pi),
    F(z)=3(sin z-z cos z)/z^3.

It verifies normalization, A(0), and the imaginary part at stated finite
frequencies. Only kR<<1 is used for the slow-source bound.

## Changed hypothesis with a slow phase mode

A positive medium sound speed c_s with R/c_s comparable to the conversion
timescale avoids the slow-source hierarchy. For R=56 kpc and timescale100 Myr,
this is roughly550 km/s. It requires a medium kinetic constitutive law, rather
than assuming the previous Lorentz phase inertia. The existing static energy
does not derive this speed. No common speed across galaxies is established.

The spherical tests choose c_s=R=I=1, V(q)=cos^2(pi q/2)/4 and
N(q)=sin^2(pi q/2), with a smooth compact h proportional to (1-r^2)^2.
They establish a reciprocal, positive-energy conversion-to-wave mechanism in
that reduced model. They do not establish mobile density, boundary restoration,
actual galaxy-law preservation during formation, or safe F reservoir response.
Those are additional obligations and cannot be inferred by juxtaposing two
separate successful component tests.

## Static boundary restoration survives this kinetic extension

Let u denote all previous mobile material/carrier coordinates on their mass
constraint, and let H0 be the tested constrained static Hessian. In canonical
variables the extended energy has the form

    E0(u)+[Pi-G(u)]^T A^-1[Pi-G(u)]/2
         +nonnegative scalar-gradient and material-kinetic terms,

where A is positive. About a static equilibrium Pi=G(u0), completing the
square gives the quadratic form

    delta_u^T H0 delta_u
      +[delta_Pi-DG delta_u]^T A^-1[delta_Pi-DG delta_u].

Its Schur complement after relaxing momenta is exactly H0. Thus an existing
local radial energy minimum remains an energy minimum under this extension;
its relaxed static boundary stiffness is unchanged. A passive outgoing sink
cannot increase the perturbation energy. This conditional energy argument
does not prove formation from the unstable all-F state or positivity of modes
outside the previously tested radial active space. The global constant-chi
shift is a zero-energy symmetry, not a negative mode.

PC-16 supplies a positive active radial H0 and relaxed boundary stiffness
4.11305e-4 Eunit/kpc^2 for the independent-field benchmark. SS-11 checks the
square and Schur algebra exactly. The benchmark's approximately 0.71% law
error and its failures at other masses are inherited unchanged.

## Frozen outer-reservoir response

For x=y=0 in an outer F cell, write ctheta=pi^2/4. Dropping positive phase
gradient terms, the local phase quadratic divided by ctheta has matrix

    [ B+J rho+beta C F(u)/ctheta,       -J rho ]
    [       -J rho, rho(Psi-hF-epsilon+J-drive) ].

The Schur margin for a common positive pulse drive is

    drive_crit=Psi-hF-epsilon+J
               -J^2 rho/[B+Jrho+beta C F(u)/ctheta].

It includes coordinated carrier and matter conversion; the alignment-only
gap J is not used as a substitute. SS-09 computes a minimum drive_crit of
14.7024 in halo specific-energy units for r>1.2R. Scaling the finest smooth
source pulse to the actual benchmark energy release and converted mass gives
a global exterior drive envelope1.11326, leaving a positive margin13.5892.
The actual tiny nonzero outer T fraction is below 1.82e-13. This is a frozen
background local stability test, not a nonlinear no-nucleation theorem or a
simulation of mobile F matter. The halo-profile source test is a separate run.

## A stated canonical material dynamics and its extra phase

Static real spin amplitudes alone do not fix time evolution. One explicit
completion uses complex amplitudes psiT,psiF with a common canonical
Schroedinger coefficient sigma and the same positive gradient coefficient.
The static alignment extends to

    J |cos(alpha) psiT-sin(alpha) psiF|^2,

and introduces a relative material phase. At fixed positive real amplitudes
its additional energy is

    2J sqrt(rhoT rhoF) sin(alpha)cos(alpha)[1-cos(relative_phase)]>=0.

The total common matter phase is a symmetry; gradients of the phases carry
positive kinetic energy. In the continuum sigma=sqrt(kappa) in the previous
dynamical units. This is a canonical dynamical hypothesis consistent with the
previous wave coefficient, not something selected uniquely by static data.
The pressure functional remains a barotropic phenomenological input; no
microscopic quantum statistics or entropy production is derived by this step.

For mobile T use D_mu=partial_mu-i(g/sigma)partial_mu(chi); F is uncoupled.
The spatial term is kappa |D_i psiT|^2/2, not a linear-current truncation.
Varying this positive canonical action gives material currents with opposite
conversion sources and the reciprocal scalar source -g div(jT). For the
stated real alignment convention the material source is

    Gamma=(2J/sigma)sin(alpha)cos(alpha) Im(psiF* psiT).

No phenomenological energy injection or prescribed Gamma is needed for that
formal field model. It still needs actual solution with mobile density,
carrier dynamics and radiation, and it does not fix its common physical
couplings or repair the previously observed static failures.

## Dynamical outer-response test, beyond instantaneous curvature

A positive instantaneous quadratic energy does not preclude parametric
amplification. SS-21 records the halo-profile-source pulse at four exterior
radii. SS-22 tests its two material perturbation quadratures under a stated
canonical material time and a fast, adiabatically relaxed carrier.

At a local outer F background let t=u+iv be the infinitesimal T amplitude
relative to the stationary F phase. Set

    a0=Psi-hF-epsilon+J,
    b0=a0-J^2 rho/[B+Jrho+beta C F(u_background)/ctheta],
    a(t)=a0-drive(t), b(t)=b0-drive(t).

Here u_background denotes the response acceleration, not the perturbation
quadrature u. Adiabatic carrier elimination gives

    udot=a(t)v/sigma, vdot=-b(t)u/sigma.

Each frozen-coefficient step is integrated by its exact 2x2 exponential;
the energy-normalized singular value of the fundamental matrix tests every
initial perturbation phase. It does not mistake positivity of a,b for a
dynamical conclusion. The wave and density backgrounds remain prescribed.

The previous wave coefficient implies canonical material time 1.47944 Myr.
For a100 Myr pulse unit the largest perturbation-energy gain is 1.023375
over four probes and 200 pulse units. Alternative 1 Myr and 0.2 Myr pulse
units give largest gains1.023504 and 1.040038. Step subdivision1,2,4
converges; the finest symplectic determinant errors stay below 4.2e-12.
This is bounded local linear response for the stated canonical completion,
not a nonlinear F-conversion, entropy-heating or full-halo stability proof.

## Rapid internal conversion with derived inertia

The slow-source bound must not be applied to a fast internal transition by
assuming its timescale equals the infall time. In the alignment-dominated
canonical completion let the local real ground spinor be

    |g(q)>=(sin(pi q/2),cos(pi q/2)),

with orthogonal internal state at energy gap J. In its rotating basis the
Hamiltonian, with the common static energy removed, is

    [0, -i sigma pi qdot/2; i sigma pi qdot/2, J].

Its lower dressed eigenvalue is

    lambda_-=[J-sqrt(J^2+sigma^2 pi^2 qdot^2)]/2.

For M participating matter mass the adiabatic action contributes
Lkin=-M lambda_-. Its leading inertia is

    Iq=M sigma^2 pi^2/(2J).

This derivation is nonsingular at a pure T or F endpoint; eliminating a
relative-phase chart by dividing by sqrt(N(1-N)) would introduce an artificial
coordinate singularity. For a finite constant rotation the kinetic Hamiltonian
is

    T(P)=MJ/2 [1-sqrt(1-(P/Pmax)^2)], Pmax=M sigma pi/2.

It is positive on |P|<Pmax and reduces to P^2/(2Iq). The full time-varying
spinor is not exactly eliminated by this constant-rotation formula; adiabatic
tracking remains a stated hypothesis. Scalar drive and response detuning also
correct the pure alignment gap. This is not a microscopic derivation of the
canonical action itself.

SS-23 checks the eigenvalue and Legendre algebra exactly. With the previous
wave coefficient, J=30 and participating mass5.20496 Mb, Iq=0.000598928
in the old dynamical units. The binding-only conversion-potential scale
epsilon M gives inverse frequency 0.49315 Myr. A separately labeled potential
equal to the entire previously computed collapse release gives 0.33642 Myr.
R/c is 0.18377 Myr, so the relevant omega R/c values are0.373 and 0.546,
not the assumed0.00184 of a smooth100 Myr change. The low-frequency
65 Gyr estimate does not apply to these rapid internal-mode hypotheses.

SS-25 audits their scale near the actual static benchmark. The smallest local
internal gap in the core is 28.548 versus J=30. Freezing the onsite mean-field
detuning increases the estimated collective inertia by 9.68%; the bare Lorentz
carrier inertia is only 1.31e-4 of the leading material inertia. This audits
the existing branch, not the entire formation path or the transport inertia.

SS-24 puts the derived inertia into the same reciprocal, spherical, measured-
profile-source calculation with scalar propagation at c. It compares quadratic
kinetics with the finite-rotation Hamiltonian. The binding-only fine run exports
99.8077% of its binding-potential energy and reaches97.7191% at 22.63 Myr.
The whole-release-potential hypothesis exports 99.9141% of that stipulated
potential and reaches the threshold at 13.69 Myr. All field energy starts at 0.
These are reduced-model outcomes. The binding-only reservoir is 1.56149 Eunit,
whereas actual collapse release is 3.35523 Eunit; exporting the former cannot
be described as exporting the latter. The whole-release cosine potential has
not been derived along an actual mobile-matter trajectory.

SS-26 applies the measured whole-release-hypothesis pulse to the local canonical
outer perturbations. The worst energy gain over four probes is 1.044071,
with timestep subdivision converging. The smallest sampled instantaneous gap
is 14.1505. This improves on a static threshold test but retains frozen density,
adiabatic carrier and omitted spatial-gradient restrictions.

## Actual transport cannot be hidden inside the rapid internal coordinate

SS-27 uses the independently equilibrated free all-F halo and formed endpoint,
not a toy potential. On the explicitly defined curve

    m(N)=(1-N)m_initial+N*m_final, mT(N)=N*mT_final,

continuity fixes total radial flux. At any radius Cauchy-Schwarz gives
sum_i rho_i v_i^2 >= (total mass flux)^2/(r^4 rho_total). Consequently

    Ttransport >= Ndot^2/2 integral [Delta M(<r)]^2/(r^2 rho(N,r)) dr.

At N=1/2 the associated q-coordinate transport inertia is 3.89e8 times
the internal-state inertia. The actual existing energy functional also places
a 0.01269 Eunit barrier above the initial state on this curve. It cannot be
followed from rest without another route through configuration space. Even
ignoring that barrier and allocating the entire potential drop to kinetic
motion gives a conditional minimum transit time 9.025 Gyr for this curve.
This is not a general formation-time bound or a no-go for local inside-out
conversion. It rejects using a single rapidly varying global population as
the actual mass-redistribution coordinate. SS-28 therefore separates front
position from infall in the next potential-landscape discriminator.

## Numerical conservation identity

The q equation uses discrete derivatives DV=(V1-V0)/(q1-q0) and
DN=(N1-N0)/(q1-q0); waves use implicit midpoint. The reciprocal source is
-g h (N1-N0)/dt, and the material force uses g DN times the same weighted
midpoint chidot. The cross work cancels exactly. With sponge gamma(r)>=0,

    H1-H0 = -dt integral gamma chidot_mid^2 dV.

The shift-charge sink is dt integral gamma chidot_mid dV. Positive passive
energy escape does not imply a positive charge sink; both signs are retained.
Outer Neumann closure lies behind the sponge. Domain/refinement comparisons
are necessary to interpret sponge loss as outgoing radiation.
