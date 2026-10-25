# Effective 3D extension and conservative local conversion

## Field choice

In physical units let each T packet source a normalized Gaussian of dispersion
sigma. Define u by curl u=0, div u=4pi G rho_T, and isolated decay at infinity.
The vector at position y is a sum over the actual 3D packet positions:

    d_i = y-x_i, r_i=|d_i|,
    F(s)=erf(s/sqrt(2))-sqrt(2/pi)*s exp(-s²/2),
    u(y)=G sum_i m_i F(r_i/sigma) d_i/r_i³.

Set

    U_T = a0²/(4pi G) integral w(|u|/a0) d³y,
    w(z)=-log(1-z)-z,  0 <= z < 1.

The spherical expression in the previous checkpoint is recovered for a spherical
source, because u=GM_T(<r)/r² and d³y=4pi r²dr. A nonspherical configuration is
not replaced by enclosed mass, and particles do not feel a baryonic center
reaction. Both species source ordinary gravity, but only T sources this field.

This is a *specified longitudinal effective extension*, not a unique consequence
of the spherical law. In particular, minimizing integral w(|u|) over every vector
field with fixed div u would yield curl[w'(|u|)u/|u|]=0, which is generally
incompatible with imposing curl u=0. That distinct nonlinear elliptic model is
NOT solved by this code. The present extension is quasistatic: no propagating
field modes or radiation transport are included.

## All-space quadratic energy and finite nonlinear remainder

With G=Mb=b=1 and kappa=a0 b²/(G Mb), expand w(z)=z²/2+sum_{j>=3}z^j/j.
The quadratic field energy is evaluated analytically, including the exterior:

    U_2 = (1/2) sum_ij m_i m_j erf(r_ij/(2sigma))/r_ij,
    U_2,self = sum_i m_i²/(2sqrt(pi)sigma).

The remaining energy is midpoint quadrature on a fixed Cartesian cube:

    U_>2 = kappa²/(4pi) sum_q dV [w(z_q)-z_q²/2].

The omitted nonlinear exterior scales as R^-3 in the distant monopole limit.
It is not identically zero, nor is a close source at the box edge represented
accurately. Live evolution stops if a T source comes within 3sigma of a face.
Mesh/box and translation/rotation controls measure finite errors rather than
assuming them away. The domain z<1 is checked at quadrature nodes; unsampled
maxima remain a limitation, particularly near saturation. No clipping is used.

For one packet, write f(r)=F(r/sigma)/r³. The vector kernel derivative is

    d[u_i]/d[x_i] = -m_i [f I + (f'/r) d_i d_i^T].

For the remainder,

    dU_>2/du = dV/(4pi) u z/(1-z).

Contract these expressions and add the analytic gradient of U_2. The actual
force is -grad_i(U_g+U_T). This exactly differentiates the *discrete* potential;
energy integration can therefore converge despite finite mesh symmetry errors.
There is no force projection or kinetic-energy correction. Gaussian self-energy
is retained in capture: subtracting it just to make capture easier would change
the physical model. Packet-mass and sigma refinement are necessary.

## Local reaction and receiver

The illustrative physical interaction uses the same parameters everywhere:

    h = 0.1 kpc,
    Sigma/m = 1 cm²/g = 2.0884e-10 kpc²/Msun,
    V_h=4pi h³/3,
    gamma_ij = (Sigma/m) m_b max[-(v_T/F-v_b) dot n,0]/V_h,
    gamma_ij=0 when |x_T/F-x_b| >= h.

This is a finite-range volume reaction kernel with incoming flux, not a derived
particle cross section or an exact hard-sphere contact model. Rotating and
unordered cases use identical parameters. Mass/size inputs only set initial
conditions and physical-to-internal unit conversions. No galaxy name is read
by the interaction. No expanding-neighbor circulation estimator is used.

At an accepted candidate event, compute Delta=U_T(after)-U_T(before) at the
actual fixed positions. Let K_n=mu v_n²/2 be incoming normal relative kinetic
energy. Require K_n>=max(Delta,0); saturation is a separate rejection.
For F->T, Q_rad=.91(K_n-Delta); for T->F, Q_rad=0. The outgoing normal speed is

    v_n,out = sqrt(v_n,in² - 2(Delta+Q_rad)/mu).

A central equal-and-opposite impulse effects this change. The pair's kinetic
energy changes by -Delta-Q_rad. Add Q_rad to Q, so

    H = kinetic + U_g + U_T + Q

is unchanged at the collision, with pair momentum and angular momentum also
unchanged. Radiation is an isotropic Newtonian receiver: it carries energy but
no resolved momentum, gravity or subsequent absorption. This is intentionally
an open radiative closure, not complete microscopic detailed balance.

Baryon-baryon pairs within the same h can dissipate with normal restitution .5;
the lost kinetic energy also enters Q. Their kernels are not expanded to force
cooling when a region is sparsely sampled.

## Transport, sampling and diagnostic limits

Adaptive kick-drift-kick integration controls the Hamiltonian error. Before
processing collisions, a swept-segment test detects possible near encounters;
steps subdivide if relative displacement exceeds .2h (.1h in the control).
The sum of incoming hazards at each particle is limited to .1 per trial
interval, before sequential collisions. Speeds and individual rates are
recomputed after impulses; later rates can in principle increase, so the maximum
actual hazard-step product is also reported. This finite stochastic splitting
is not an exact simultaneous multi-collision solver. Curved trajectories can
differ from the straight swept check; the gravity step and interval control
bound the tested approximation, not an all-trajectory theorem.

The new acceleration diagnostic uses actual 3D softened Newtonian radial forces
at 12 radii times 24 azimuths in the initial xy plane, centered on current baryonic
COM. Compare g_total with [g_b+sqrt(g_b²+4 a0 g_b)]/2. Negative radial samples are
excluded and their count is reported. This is a diagnostic, not a likelihood or
a requirement that arbitrary nonspherical nonequilibrium systems obey an exact
algebraic RAR. It does not rotate into a fitted final disk plane.

Free-bound fractions use instantaneous Newtonian specific energy; they are not
asymptotic retention or observed missing-mass estimates. All initial media share
the assumed reservoir mass 5.364 Mb. Initial T controls are explicitly separated
from formation runs.

Temporal resolution of a rare encounter is different from sufficient spatial
sampling of a local density. For independent samples of the smooth initial flattened Plummer target density,
the maximum density gives the expected-count upper bound

    E[N_b in h] <= N_b h_internal³/(27 flat trunc),
    trunc=1000/101^(3/2).

It holds at every position for the smooth target density before evolution.
The actual initializer uses stratified fixed radii; this continuum estimate is
not a rigorous probability bound for those discrete radial shells.
Thus requiring even 32 expected local baryon packets needs at least
32*27*flat*trunc/h_internal³ particles. This is a necessary lower bound, not a
sufficient resolution criterion, and not a claim that every collision requires
32 partners. It quantifies why empty neighborhoods in a small-N run cannot settle
the continuum formation question across a huge physical size range.

## What this interaction can and cannot select directly

At fixed local densities and an isotropic free-particle velocity distribution,
rotating the baryon velocity vector while keeping its speed fixed leaves the
relative-speed statistics of an isotropic binary kernel unchanged. Thus the
present reaction does not directly recognize global circulation coherence.
Rotation can affect formation indirectly by changing density, geometry and
velocity distributions under live dynamics. This conditional symmetry argument
is not a no-go theorem for local interactions with additional fields, spin,
gradient-dependent couplings or anisotropic distributions. It is a reason not
to expect a generic radiative scattering law alone to guarantee disk selection.
