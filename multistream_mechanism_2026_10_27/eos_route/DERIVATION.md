# Conditional core response and an energy outlet

This route replaces a conductivity shutoff by a restoring constitutive response.
It is a conditional reduced model: neither its active phase nor its coefficient
is derived from the original cold field. It provides a concrete stable endpoint
and an explicit transfer ledger for small perturbations, not nonlinear formation.

## Fixed active phase

Let the cold component admit a barotropic continuum description in a locally
relaxed core. Take an internal energy per physical volume

    u(rho) = -A [ln(rho/rho_ref)+1],       A>0.

The fluid identity P=rho*u_rho-u gives P=A ln(rho/rho_ref), and dP/drho=A/rho>0.
A constant background pressure can be subtracted in a core equilibrium but its
boundary matching must be retained. This is the known logotropic equation of
state, not a new derivation from multistream kinetic theory. The energy density
rho c^2+u and the stress must be consistently retained in a relativistic parent;
this calculation uses the Newtonian regime and the perturbative cold mass rho.

Hydrostatic equilibrium and Poisson give

    A laplacian(1/rho) = 4 pi G rho.

Writing theta=rho0/rho and r=a xi, a=sqrt(A/(4piG))/rho0,

    theta''+2theta'/xi=1/theta,    theta(0)=1, theta'(0)=0.

At theta(xi4)=4, xi4=5.84477267596. Therefore

    Sigma=rho0*r_quarter=xi4 sqrt(A/(4piG)).

This is a constitutive equilibrium relation, not a scattering-rate threshold.
At fixed A it holds for every member of the family whatever rho0; mass or the
matched envelope selects rho0. It does not independently select one volume density.
The logotropic profile cannot be extended indefinitely as an isolated halo:
its rho~1/r tail has infinite mass and the wrong far-field behavior. Here the
active core is bounded and requires an envelope. Matching that envelope is open.

The regular solution and constant-column result are known (Chavanis,
arXiv:2201.05903, equations 145-156). We solved the ODE independently.

## Radial restoring force and its boundary assumptions

Consider spherical barotropic Euler-Poisson perturbations of a fixed-mass
sphere with prescribed external pressure and no baryons. Let the Lagrangian
radial displacement be r*eta(r)*exp(i omega t). Continuity gives

    Delta rho/rho = -(3eta+r eta'),
    Delta P = -A(3eta+r eta').

The radial pulsation equation is

    [A r^4 eta']' - 4r^3 P' eta + rho r^4 omega^2 eta=0.

With lambda=omega^2/(4piG rho0), this becomes

    eta''+4eta'/xi+[4theta'/(xi theta)+lambda/theta]eta=0.

Regularity fixes eta(0)=1, eta'(0)=0. At a moving interface against fixed
external pressure, Delta P=0 implies 3eta+xi eta'=0. This is not a rigid box
boundary. Neither a live halo envelope nor kinetic/phase-front degrees of freedom
have been included in this radial stability calculation.

A nodeless shooting solution at the quarter-density boundary has
lambda=0.0903960232>0: this mode oscillates rather than grows. The finite
root scan is checked against the zero mode at the mass turning point. At
fixed boundary density, M is proportional to xi^2 theta'/theta^2; its first
extremum occurs at theta'=1/sqrt(2), at xi=7.46171857547 and density contrast
5.13395466. A nodeless negative eigenvalue appears beyond it, as expected.
Consequently one must not claim every logotropic configuration is stable.
The contrast-four boundary is an explicit model assumption; it cannot be
chosen merely because that is the convention for measuring a halo core.

## Explicit outgoing-wave transfer

Let q be the amplitude of a stable core normal mode. Couple it to a real
massless mediator on a half-line x>=0, with positive parameters mu,T,c_chi:

    L = mu/2 (q_dot^2-omega0^2 q^2)
        + integral_0^infty T/2 [psi_t^2/c_chi^2-psi_x^2] dx,
    psi(0,t)=g q(t).

The interface condition can be imposed by a Lagrange multiplier. The shared
boundary carries equal and opposite reaction forces. With no incoming waves,
psi(x,t)=g q(t-x/c_chi), and

    mu q_ddot + (T g^2/c_chi) q_dot + mu omega0^2 q=0.

The core energy lost is exactly the energy carried into the mediator:

    E_core=mu/2(q_dot^2+omega0^2 q^2),
    dE_core/dt=-Gamma q_dot^2,
    F_out(0)=Gamma q_dot^2,       Gamma=T g^2/c_chi>=0.

For a finite observation boundary L, the conserved ledger is core energy plus
mediator energy inside [0,L] plus time-integrated outgoing flux at L. Over the
entire half-line at a finite time with finite-energy initial data, the ledger
is core plus all mediator energy. Eliminating the mediator with outgoing
conditions makes the core subsystem damped; it does not destroy total energy.
Incoming waves reverse this interpretation and can re-excite the core.

The numerical diagnostic uses modal units mu=omega0=1, Gamma=.4 and a small
q(0)=.1. The energy-ledger relative error is 7.7e-12, and the final mode energy
is 5.2e-18 of its initial value. The analytic damped-oscillator solution supplies
an independent check. This is damping of a pre-existing stable mode. It does
not show that collapse excites this mode, that a real field produces this
boundary coupling, or that an order-one density perturbation finds the core.
The mediator and core are connected as a reduced mode model; no complete
three-dimensional cold-field/mediator parent is claimed.

## Reciprocal finite-body compression source: executed continuation

The simple half-line boundary model was followed by a spatially resolved radial
wave calculation using an actual compact compression source. In a fixed active
phase, the existing density-weighted current coupling `g zeta n J^mu partial_mu chi`
has the linear mode projection

    L_int = q_dot integral J_source(r) chi d^3x,
    J_source = g zeta0 n0^2 div(xi_mode).

Here zeta is a material active-phase label satisfying `D zeta=0` during the
calculation. Its support moves with the fixed-mass core boundary. Formation of
that phase is not derived. With `delta n=-div(n0 xi_mode) q` and
`delta zeta=-xi_mode.grad zeta0 q`, the quadratic terms include both density
variation and material-label variation multiplying chi_t, as well as the
advective current term. Integrating in time and space gives the coefficient

    g [2zeta0 n0 div(n0 xi_mode)+n0^2 xi_mode.grad zeta0
       -div(zeta0 n0^2 xi_mode)] = g zeta0 n0^2 div(xi_mode).

This cancellation retains the moving-interface terms. A coupling window fixed
in space would instead have an additional surface source and is not this model.
In the diagnostic, div(xi_mode)=0 at the boundary, so the resulting compact
source also vanishes there. The constant linear background term is a time
boundary term.
This is a projection of a possible active-phase interaction, not the derivation
of its coupling or a complete finite-frequency parent.

The reduced action and equations, with `A_chi=integral J_source chi d^3x`, are

    L=mu/2(q_dot^2-omega0^2 q^2)
      +1/2 integral[chi_t^2-c_chi^2 |grad chi|^2]d^3x + q_dot A_chi,
    chi_tt-c_chi^2 laplacian chi=J_source q_dot,
    mu q_ddot+mu omega0^2 q=-integral J_source chi_t d^3x.

The exact canonical Hamiltonian is

    H=(p_q-A_chi)^2/(2mu)+mu omega0^2 q^2/2+H_chi >= 0.

The source and reaction transfer equal and opposite power. This is not a
forced field whose reaction has been discarded. Static q=chi=0 remains an
equilibrium. The modal core energy is the constrained quadratic perturbation
energy, including the fixed-pressure boundary-work convention; it is not the
entire halo's negative binding energy. Radiating it therefore does not assert
that cooling an ordinary virial core makes it expand.

`wave_outlet.py` solves the coupled core and radial field, using u=r chi and
an implicit midpoint update of the linear Hamiltonian system. The first t=70
run transferred 55.69% of the initial mode energy into the field. It failed
the declared 95% transfer check, while passing conservation/refinement. This
physical finite-time failure is preserved in `run_wave_checked`; the earlier
`run_wave` failed only on JSON serialization, with its original source retained.
No rate, source or threshold was changed to upgrade those outcomes.

The continuation `run_wave_extended` uses the same coupling and source, t=350,
and an outgoing impedance at radius 90 with an explicit outgoing-energy ledger.
On the fine grid the energy fractions are

    core oscillation: .01547594,
    mediator still inside radius 90: .03101218,
    exported beyond radius 90: .95351188.

Thus 98.45% has left the core mode, with total relative ledger error below
6.7e-13. Coarse/fine remaining-core fractions differ by .00111 of initial
energy. At zero coupling the core retains its energy. This is finite-time
evidence for relaxation in the declared reduced model, not continuum nonlinear
convergence or an astrophysical timescale.

For the finite spherical boundary the canonical u energy differs from the
original chi volume energy by `2pi c_chi^2 u(R)^2/R`; the physical integrated
flux has the compensating boundary term. The code tracks canonical wave energy
and its `4pi c_chi u_t(R)^2` impedance flux consistently. At infinity, or after
the pulse has passed the boundary, the surface term vanishes. The finite-grid
impedance is not asserted perfectly transparent; refinement is reported.
The audited continuation also measures incoming versus outgoing radial
characteristic power at radius 70: the ratio is 1.50e-4 coarse and 3.79e-5
fine. The final spherical surface correction is 5.19e-6 of initial energy
on the fine grid. This checks the boundary convention and contamination
rather than inferring transparency merely from selecting an outlet option.

Current source hashes validate against `run_wave_audited/manifest.json`.
Earlier manifests retain their original hashes and source snapshots; they
are historical records, not freshness certificates for the subsequently
instrumented source.

## Normalization test

To obtain the requested core surface density exactly, this EOS would require

    A_req = a0^2/(pi G xi4^2).

Numerically A_req is 1.22318e-12 Pa (canonical) and 1.78644e-12 Pa (alternative).
For the canonical a0^2=G rho_Lambda c^2/4,

    A_req/(rho_Lambda c^2)=1/(4pi xi4^2)=0.002329458.

This value is a matching requirement, not a derived coefficient.
A published Planck-density logarithm suggests A/(rho_Lambda c^2) approximately
1/ln(rho_P/rho_Lambda)=.00353241. It produces a surface density 1.23143 times
the canonical target, about 132 instead of 107 solar masses per square parsec.
It corresponds to an effective kappa about .616, not .5. The comparison uses
one physical Lambda; one must not replace it by the alternative footing's
inferred density to manufacture agreement. The ~23% proximity does not derive
the target or establish agreement with a calibrated observational likelihood.
The Planck-density matching is an extra microscopic assumption in the cited
model, not a consequence of logotropic hydrostatics alone.

## Activation remains a separate obligation

A globally active logotropic dark fluid has a cosmological sound-speed problem
(Ferreira and Avelino, Phys Lett B770 (2017) 213-216,
DOI 10.1016/j.physletb.2017.03.075). This route does not adopt it globally.
A phase activated by multistream stress might avoid the single-stream linear
pressure, but that is an unproved extension. A gate is not free: differentiating
its energy produces reciprocal kinetic/chemical stresses. The separate field
route derives these terms. Dropping them would invalidate conservation and
could change both the core and the early-state limit.

A conditional local core with a restoring force and an energy outlet is now
explicit. The missing implications are the microscopic EOS, coefficient,
phase transition/retention, live envelope, and formation. A gate that switches
off when the core becomes coherent could remove its supporting EOS and cause
renewed collapse; active-phase retention must be derived, not stipulated.

## Finite-amplitude radius continuation and its restricted basin

To go beyond linear motion without pretending to solve a nonlinear fluid,
restrict the core to the exactly mass-conserving family
`rho_y(r)=y^-3 rho_eq(r/y)`, where y=R/R_eq. Its shape is frozen. Define

    D=(1/V_eq) integral ln(rho_eq/rho_boundary) dV = .3111185777.

The scalar virial equation gives W_eq=-3 A V_eq D. Under homology the gravity
energy is W_eq/y, while internal energy plus the fixed-pressure work is
`A V_eq y^3[-D-1+3ln y]`. Thus the complete constrained potential is

    V(y)/(A V_eq)=-3D/y+y^3[-D-1+3ln y].

It has a local minimum at y=1 with second derivative 9-12D=5.26658, and an
inner unstable barrier at y=.676927. The barrier energy is .0958687 A V_eq
above the minimum. Gravity drives the potential to minus infinity at y=0;
there is no global stability claim. The collective inertia is
`integral rho_eq r^2 dV>0`; scaling time sets its dimensionless value to one.
Off-equilibrium homology does not satisfy the exact fluid traction condition:
`P_surface-P_ext=-3 A ln y`. Thus it is a variational collective-coordinate
ansatz whose omitted boundary layer and shape adjustments matter. It cannot
be called an exact pressure-boundary fluid trajectory. The damping coefficient
remains a free dimensionless choice after the inertia/time normalization.

Coupling this radius coordinate to the ideal half-line outlet gives the
exact reduced equation `y_ddot=-V'(y)-Gamma y_dot`, with the corresponding
positive outgoing ledger `E_out_dot=Gamma y_dot^2`. It is the nonlinear
mechanical continuation of that outlet, not of the complete spatial current
coupling. At Gamma=1, both tested rest starts y=.8 and 1.2 return to y=1 and
therefore Sigma/Sigma_target=1; their energy ledgers close to 2.3e-11 in these
units. This is evidence for two-sided restoration within the specified radius
reduction, not a cold-collapse calculation.

The run in `run_homology/` intentionally remains **failed**: an additional check
that both initial states have energy below the collapse barrier was false for
y=1.2. That state nonetheless returned after sufficient energy export. Only
the y=.8 case is protected by the simple below-barrier energy argument;
the y=1.2 case is an observed dissipative trajectory. No threshold or input
was changed to upgrade this record. A failed extra assertion must not be
described as an all-checks-passing experiment.
