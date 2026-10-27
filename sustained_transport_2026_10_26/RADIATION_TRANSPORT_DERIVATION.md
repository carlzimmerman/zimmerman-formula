# One coupled source, two distinct requirements

Use the unchanged CC Hamiltonian and dimensionless time tau=t/t_dyn. All
energies are in the inherited Eunit and the radial measure is r^2 dr (the
common solid-angle normalization is already absorbed). The scalar obeys

    chi_tautau - c^2 r^-2 (r^2 chi_r)_r = -S.

The cell source S_i below is integrated over its cell volume. The full material
Hamiltonian includes the covariant edge square, alignment, finite carrier and
every density-inertia derivative. dynamics.field implements those continuous
equations independently of the implicit evolution residual.

## Exact discrete conservation laws

Let mTi=|aTi|^2, mFi=|aFi|^2 and rhoTi=mTi/Vi. The exact covariant edge currents
and local conversion rate are

    jTe = kappa/sigma w_e Im(psiTi* U_e psiTj),
    jFe = kappa/sigma w_e Im(psiFi* psiFj),
    Gamma_i = 2J/sigma Im(aTi* alignmentTi).

Then mT_dot=-div(jT)+Gamma, mF_dot=-div(jF)-Gamma. For an arbitrary fixed
enclosed-mass interpolation M_R=sum wRi(mTi+mFi),

    M_R_dot = sum_edges (wR,j-wR,i)(jTe+jFe).

Conversion cancels exactly. Changing which component a cell belongs to cannot
replace inward total-mass current. A moving q=mT/(mT+mF)=1/2 crossing obeys

    q_dot=[Gamma-div(jT)+q div(jT+jF)]/(mT+mF).

Its speed and acceleration are observables of the full vector field, not an
independent radius equation or a fitted restoring force.

The global material shift charge is

    Qm=sum_i [g1 mTi + g2 mTi^2/Vi].

Using the complete edge and conversion companions gives the telescoping identity

    Qm_dot=sum_i S_i,
    Q_total=Qm+sum_wave Vw pi = constant

before exterior absorption, with the recorded absorber charge added afterward.
The first identity is checked directly with the independent continuous vector
field and again against the stored density/source histories. Endpoint density
secants in the evolution preserve the corresponding discrete charge identity.

Hamiltonian work is equally reciprocal:

    H_wave_dot=-sum_i S_i pi_material,i,
    H_material_dot=+sum_i S_i pi_material,i

apart from exterior transport/absorption. Splitting source into bulk and
conversion does not split radiated energy additively: waveform interference is
part of the actual coupled solution.

## Deriving the outgoing waveform without a seed

Write u=r chi. For a source contained inside r_s and regularity at the origin,
the zero-initial-field radial retarded solution at r>r_s is

    u(r,tau)=-1/(2c) integral dr' r'
             integral_[tau-(r+r')/c]^[tau-(r-r')/c] S(r',s) ds.

Differentiating and setting theta=tau-r/c gives

    u_tau=-1/(2c) integral dr' r'
                [S(r',theta+r'/c)-S(r',theta-r'/c)].

This is an additive driven solution: initial wave occupation can be exactly
zero. source_waveform_checked evaluates the time delays for every material
cell with NO fitted amplitude. It predicts the actual outgoing packet with
relative waveform L2 error 0.002261 over retarded physical times 0.1--4 Myr.
Predicted energy is 5.260639e-6 versus measured 5.260938e-6 Eunit. Source
truncation at 80 kpc, temporal interpolation and discretization are finite
approximations, not a continuum certificate.

In the compact/slow-source regime, expand the delayed source:

    I(tau)=integral r'^2 S(r',tau)dr'=Qm_dot,
    u=-I(theta)/c^2 + higher finite-size terms,
    u_tau=-I_dot(theta)/c^2,
    P_out=c u_tau^2=I_dot^2/c^3=Qm_ddot^2/c^3.

The compact prediction's waveform error is 0.003184 in the same tested packet.
Physical energy per Myr is P_out Eunit/t_dyn. When differentiating a history
sampled in Myr, d/dtau=t_dyn d/dt_Myr; the checked audit fixes this unit factor
in the charge-history comparison and obtains relative error 3.95e-5.

This explains why continued compression work is not automatically continued
radiation. Constant I builds a stationary near field after its turn-on pulse;
changing I radiates. Constant total-mass inflow alone does not fix I, since
I also depends on density-weighted compression and conversion. Sustained export
must be measured from the actual source and outgoing characteristics.

At leading quasistatic order, chi=-(-laplacian)^-1 S/c^2. Its positive near-field
energy is <S,(-laplacian)^-1 S>/(2c^2), and the reversible power required to
change it is its time derivative. Increasing a coupling increases both this
backreaction and the radiating source. No independent drag coefficient or
unpaid cooling term follows. This retains the earlier compact-source
limitation; it does not provide an exemption through a renamed mechanism.

## Moving-boundary response with no added wave population

For the actual 5.7-Myr state, perturb the material composition angle and carrier
locally around the live boundary. Keep total density in EVERY cell unchanged,
keep all material phases and both scalar fields unchanged, and solve one
interior-transition compensation amplitude to keep Q_total exactly fixed.
The reservoir remains free after release. These are response probes, not
initial populations used to claim autonomous formation.

Compute Rddot=D(Rdot)[full Hamiltonian vector field]. Opposite displacements
give the instantaneous odd response

    delta Rddot=-omega_probe^2 delta R,

with omega_probe^2=3.75342 Myr^-2 at ±0.01 kpc and 3.75628 at ±0.005 kpc.
Directional differences at 1e-7, 3e-8 and 1e-8 dimensionless time agree.
Both signs initially accelerate toward the unperturbed moving trajectory.
This is a real live-state local restoring response for the specified family.
It is not the density-relaxed equilibrium stiffness, an asymptotic stability
proof, or a result for all perturbations. Actual paired evolution is required
to see how long this response survives while density and radiation adjust.

The original joint objective additionally requires enough total mass to move
inward to form the law. None of these conservation identities, waveform
checks or local restoring responses implies that final requirement.
