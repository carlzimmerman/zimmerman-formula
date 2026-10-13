# Conditional coldness of the combined source and daughter population

2026-10-11. Checkpoint inspected at f68ed250521153df9386afc39b549b79f7aa9773.
This addresses the moving-source omission in [INVERSE_CHANNEL.md](INVERSE_CHANNEL.md).
It proves a statement about an on-shell reaction description, not about the
complete coherent field action.

## Hypotheses

Consider a homogeneous expanding volume V=a^3 V_0 containing particles of
mass m and source particles of mass M>2m. Allow arbitrary momentum spectra,
source decay, inverse production with moving sources, and elastic scattering.
Assume:

1. All reactions conserve Q=N_y+2N_h and total on-shell particle energy.
2. The energy and stress are sums of free on-shell particle contributions;
   coherent interaction energy, mean-field stress and vacuum energy are absent
   or separately controlled. Occupations need not be dilute for the algebra.
3. There is no external heating, gravitational clustering work or exchange
   with radiation. Expansion obeys dE=-P dV with P>=0.
4. Initially N_h=N_0 at rest, N_y=0, hence Q=2N_0 and E_0=M N_0.

These are substantive hypotheses. The already computed Gaussian envelope
has coherent interaction energy and does not automatically satisfy item 2.

## All-momentum inequality

Let T be the total kinetic energy. At any time,

\[
 E=mN_y+MN_h+T=mQ+(M-2m)N_h+T.
\]

Therefore 0<=T<=E-mQ. For every particle with mass mu and energy e,

\[
 {p^2\over e}={(e-\mu)(e+\mu)\over e}\le 2(e-\mu).
\]

Summing gives 3PV<=2T. Here P is one-third of the spatial stress trace;
for isotropic distributions it is the usual pressure. Since expansion makes
E nonincreasing while Q is constant,

\[
 0\le {P\over\rho}={PV\over E}
 \le {2\over3}\left(1-{mQ\over E}\right)
 \le {2\over3}\left(1-{2m\over M}\right),\qquad \rho=E/V.
\]

This includes arbitrary conversions to moving sources and arbitrary elastic
redistribution. It does not require a fixed daughter fraction or impose a
momentum cutoff. The finite rest-energy excess is the entire available
kinetic-energy budget under these hypotheses.

For M=2m sqrt(1+u_*^2), u_*=0.001, define eta=1-2m/M. Rationalization gives

\[
 \eta={u_*^2\over\sqrt{1+u_*^2}(1+\sqrt{1+u_*^2})}
 =4.99999625\times10^{-7},\qquad
 P/\rho\le3.33333083\times10^{-7}.
\]

The result concerns the combined material density, excluding rho_Lambda.
It does not establish a small sound speed or determine perturbation dynamics.
The initial source was already cold; this theorem preserves coldness during
carrier conversion and does not explain the initial energy supply.

## A hot-tail bound, not a ban on every fast particle

For particles with Lorentz factor at least gamma_0>1, kinetic energy is
at least (1-1/gamma_0) times their energy. Consequently

\[
 {E_{\rm tail}\over E}\le {\eta\over1-1/\gamma_0}.
\]

For p/mass>=1, gamma_0=sqrt(2), the bound is 1.70710551e-6. Rare energetic
particles are allowed; substantial conversion of the sector's rest energy
to heat is forbidden by the weighted number invariant in this model.

## Where the original action remains unproved

The resonant three-wave Hamiltonian b_K a_p^dagger a_q^dagger plus its
Hermitian conjugate conserves N_y+2N_h for every momentum combination K=p+q.
That exact algebraic invariant does not become an exact symmetry of the
original two-real-component potential. Counter-rotating terms and processes
such as four daughters turning into two daughters can violate it. Their
rates have not been bounded here. Losing this invariant releases rest
energy and invalidates the small kinetic budget.

Even a number-conserving coherent Hamiltonian has interaction energy. The
kinetic-pressure theorem cannot be applied through its coherent production
stage without bounding that energy and stress. It can apply after a justified
transition to an on-shell description, but that transition is still missing.
No dilute Boltzmann approximation is asserted for the highly occupied run.

## Evidence and decision

The proof above is analytic and covers arbitrary spectra under its stated
hypotheses. [pressure_bound.py](pressure_bound.py) provides 52 finite checks
of constructed mixtures and single-particle inequalities, plus benchmark
values. [Results](pressure_bound_run/results.json) and
[manifest](pressure_bound_run/manifest.json) record those checks. The finite
checks do not prove the all-momentum theorem; the inequalities do. Review
was a direct self-audit of the energy decomposition, pressure trace and
monotonicity under expansion, not independent review.

This changes the next research decision: calculating a stable daughter
fraction is not necessary to prove coldness if the combined sector's energy
budget and weighted number can be controlled. The outstanding work is to
bound coherent stress and number violation for this action, or to construct
an explicitly different action with an exact protecting symmetry and show
that its production and cold-medium properties meet the repository target.
Such a symmetry-protected alternative would change the carrier model and
must not inherit the present simulation's yield without a new derivation.
