# Causal parent, mass accounting, and remaining parameters

A consistent weak-gravity parent for transported microscopic carriers is

L = sum_a [m_a*v_a²/2 + q_a*A(x_a).v_a - q_a*phi(x_a) - m_a*Phi(x_a)]
    + integral [(E²-B²)/2 - |grad Phi|²/(8*pi*G)] d³x,

with E=-grad phi-dot A, B=curl A, c=1, and physical charge q in
Heaviside units. Neutral baryons have q=0; positive and negative constituents
appear separately. A quantum version replaces trajectories with charged matter
fields and includes their kinetic covariant derivatives. This action fixes the
Coulomb kernel q_a*q_b/(4*pi*r) in its static limit. Numerical code absorbs
1/sqrt(4*pi*G) into its dimensionless charges.

Variation gives Maxwell equations with rho_q=sum q_a delta(x-x_a),
J_q=sum q_a v_a delta(x-x_a), and Poisson gravity lap Phi=4*pi*G*rho_m.
The moving constituent sources obey dot rho_q+div J_q=0 exactly. Neutral-pair
centers carry the sum of the constituent masses: calling them a medium does
not remove their gravitational source. A polarization representation is a
coarse-graining of these sources, not an additional charge or mass reservoir.

The isolated-system conserved energy is
K + integral (E²+B²)/2 d³x + (1/2)*integral rho_m*Phi d³x,
with consistent finite-size charge self-energies or renormalized particle
masses. Energy carried away by radiation must remain in the domain accounting
or be measured as boundary flux. Eliminating the electrostatic and Newtonian
fields produces the pair potential used in the experiment. The softened
kernel is a numerical choice, not the exact point-charge Maxwell theory.

Maxwell propagation is causal. Newtonian gravity is not a causal gravitational
completion. A relativistic gravitational theory would require stress-energy
from rest masses, motion and the electromagnetic field; the present particle
experiment does not include that completion or binding energy as gravitating
mass. It also does not simulate radiation. Consequently the experiment cannot
verify the full causal parent's energy balance or capture rates.

For the microscopic two-body spectrum, adding Newtonian constituent gravity
replaces kappa in DERIVATION.md by kappa_eff=kappa+G*epsilon*m². Under the
vacuum matching kappa=G*m² this is kappa*(1+epsilon). It rescales B and a_B;
it does not remove the ground-state dipole gap 3B/4. The reported atomic
numbers use pure Coulomb atomic units and test dimensionless ratios, not a
calibrated physical dark-atom mass.

Parameter ledger:
- Charge conservation fixes equal and opposite constituent charges.
- Vacuum cancellation of positive-positive electric and gravitational forces
  fixes q²/(4*pi)=G*m² conditionally. This is a matching requirement, not a
  consequence of gauge symmetry. The electric contribution remains repulsive;
  net positive-positive force at this matching is zero, not a tether.
- The microscopic mass m and mass ratio epsilon remain undetermined.
- Given those constants, B, a_B and oscillator strengths are derived; they
  cannot independently be tuned to different objects.
- The collective chain's spring constant and arrangement are additional model
  assumptions. They do not close the parameter budget and were used only to
  test the gapless-mode argument.
- Density, temperature, spin, preparation and abundances are state variables.
  They require cosmological/assembly evolution, not separate galaxy labels.
- Softening, particle number, integration tolerance, duration and seeds are
  numerical controls, not microscopic predictions.
- The critical exponent/normalization, nonlinear saturation, and preparation
  of the previously fitted medium are still not derived. No fitted chi or
  independent reaction rate is inserted here to make the new tests succeed.

A next discriminating route is an interacting quantum medium with explicitly
specified masses, density and Hamiltonian. Compute its retarded polarization
spectral function (including oscillator strengths), identify whether a stable
critical phase actually exists, and use that same state's mass and equation of
state in transport. A one-particle DOS or a phonon DOS cannot substitute for
this calculation. This is unresolved work, not a claimed mechanism.
