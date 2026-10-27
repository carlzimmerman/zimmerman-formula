# What cold energy means, and the most useful change to investigate

20 October2026. User-authorized theoretical exploration; NOT an adopted change
to the canonical equations, frozen tests or publications. No kinetic solver or
new force law is implemented here. Latest observed source snapshot ae6217442.

**Verdict:** there is a defensible physical direction to investigate, but no
completed mechanism. Use a genuinely dynamical, self-gravitating cold phase
with conservative collision/heat/angular-momentum transport and escape.
Do not keep a universal phenomenological drift acting on that bound phase.
This needs a derivation and consistent coupling, not a renamed density gate.

## What would actually be happening?

Cold energy in this record means positive-energy massive excitations moving
nonrelativistically: most energy is rest energy, and material pressure is
small compared with energy density. It is not a heat reservoir with an
unlimited supply. At galactic scales it acts as gravitating mass.

There are currently distinct ingredients, not one fully joined theory:
1. Particle/field production and, in ARGON's separate real-mediator action,
   self-bound fragments from a prepared coherent state.
2. A polarization/settling medium intended to reproduce the baryonic galaxy
   force law. Its source and dynamical closure still have open dependencies.
3. A proposed extra cold population in faint dwarfs. Its existence, inventory,
   concentration and coupling cannot be inferred just by assigning a core.

CFG888 shows why this distinction matters: in the canonical density-as-
polarization identification, a critical term cancels cold self-gravity; the
Class-A effective kinetic equations instead use Newtonian cold self-gravity.
H-LINK's self-boosted mass formula is not derived in either current reading.
A tinker must choose one ontology/action and count the mass once, rather than
combine favorable equations from incompatible readings.

## Three routes, with the first two already obstructed

A. Adjust one universal mobility coefficient or a local density/Mach gate.
CFG913's declared42 choices fail their simultaneous galaxy/merger/dwarf
constraints. CFG915/916 show that remembering a formation label or freezing
surplus is not enough: exact recapture can erase release, while capped capture
adds a rule and still has unresolved transport. No all-function no-go claimed.
Repeating a density threshold without addressing these failures is not progress.

B. Weaken the critical quadratic to give the SAME polarization field self-gravity.
This is a real action change, but it also changes the original force law.
The analytic obstruction is derived below. It cannot be claimed to repair
cold self-gravity while automatically preserving the galaxy successes.

C. Treat autonomous bound structures as a dynamical phase and derive their
transport from microscopic scattering, rather than imposing a drift thermostat
on them. This is the recommended RESEARCH CANDIDATE, not a demonstrated repair.
It must not be an arbitrary per-galaxy mobility switch or a history label.

## A concrete failed simple tinker: the critical quadratic coefficient

In the local static ID branch, write K=4piG, u=K|P| and

 L = -|gradPhi|^2/(2K) + gradPhi.P - zeta K|P|^2/2
     -rho_b Phi - W_rem(u),
 g = g_N,b + u,              g = zeta u + K W_rem'(u).

For the fixed rational restoring law K W_rem'=f(u)=u^2/(a0-u), zeta=1 gives
g_N,b=f(u). Set zeta=1-eta, holding W_rem fixed. Then

 g_N,b = f(u)-eta u.

For eta>0, zero source admits u=0 AND u0=eta a0/(1+eta). The response slope
at zero is -eta and at u0 is eta(1+eta). Thus the modification changes the
small-field restoring curvature and introduces a nonzero algebraic branch.
It does not establish a stable finite object or a universal vacuum acceleration:
boundaries, vector directions, gradient terms and stability remain necessary.
For eta=.1 the branch has u0/a0=1/11; for eta=1 it is1/2.

If we try to keep the old galaxy response by changing K W_rem' to f+eta u,
then W_rem gains eta u^2/(2K), exactly cancelling the altered quadratic in L.
That retuning is algebraically the old action, not a new self-gravity mechanism.
These exact coefficient identities were independently reviewed and checked
with rational arithmetic in run_001. This is one scoped tinker, not a theorem
excluding every phase-dependent coupling or action extension.

## The physical candidate: conservative gravothermal evolution plus escape

A self-gravitating collisional population can carry heat outward. A virialized
core has negative heat capacity: for the isolated Newtonian benchmark
2K+W=0 and E=-K. Losing total energy makes it contract and increases its random
kinetic energy; it can stay nonrelativistic throughout. 'Cold' does not mean
that internal temperature must fall while the core contracts. For a core
inside an interacting host, include surface and interaction terms instead
of using E=-K blindly.

Angular momentum must be transported by non-spherical torques and stresses,
not thermal conduction alone. Energetic material can move outward or escape.
This supplies an identifiable E/J receiver, rather than an untracked sink.
A schematic coarse-grained autonomous sector would obey

 partial_t f + v.grad_x f - gradPhi.grad_v f = C[f],
 integral C dv =0,    integral m v C dv =0,
 integral (m v^2/2) C dv =0              [elastic local channel].

Together with self-gravity, such a channel redistributes energy; it does not
create it. A local collision preserves total momentum and hence local orbital
angular momentum. The distribution's stress/flux and gravity must actually
move J outward. Elastic two-point-particle scattering alone cannot turn an
isolated positive-orbital-energy pair into a bound binary. Many-body gravity,
a third receiver, internal excitation, or emitted field energy must be counted
for any capture claim. Inelastic/fragment-conversion channels need the full
binding, charge and energy balance, not the elastic identities above.

For the actual project, f could describe coarse-grained excitations or solitons
of a specified field: no new particle species is required by this notation.
But the record has NOT derived this C[f], its heat/stress coefficients, its
phase boundary or its coupling to the diffuse polarization medium. In particular,
adding a separate density source to an action which already counts it through
P would double count mass. Couplings need reciprocal forces and a common energy
ledger. Setting bound-phase alpha=0 by assertion merely restates the problem.
A phase-dependent action is possible to investigate, but is new physics until
its microstructure, stability and parameters are supplied.

## Why different dwarf cores might emerge without four fitted amplitudes

Gravothermal systems at different evolutionary stages need not have the same
central density. Early concentration, merger heating and tides can accelerate
or delay contraction; other systems can remain extended. This is a plausible
selector class, not a prediction that Draco/Sextans have particular histories.
The same interactions plus independently inferred histories must produce the
four outcomes. The later Sextans two-population constraint may favor extended
mass rather than a compact collapsed core; a theory must follow that evidence.

Primary literature establishes analogous behavior in DIFFERENT SIDM models:
- Sameie et al., arXiv1904.07872v2 (2020),
  https://arxiv.org/abs/1904.07872v2 : self-interactions plus MW tides can
  accommodate Draco/Fornax diversity in their model.
- Silverman et al., arXiv2606.02566v1 (2026),
  https://arxiv.org/abs/2606.02566v1 : in six simulated halos with an assumed
  cross section, merger heating delays collapse; three quiet systems collapse.
These do not validate cold energy, the original charged Phi/X or ARGON action,
source-produced abundance, our finite stock, or all four actual dwarfs. Do not
borrow their halo masses, cross sections or cosmology as framework predictions.

A useful rate scale is Gamma=rho (sigma_eff/m) v_rel. At rho=.1Msun/pc3,
v_rel10km/s, and ASSUMED sigma_eff/m1cm2/g, Gamma^-1=4.68Gyr. Density ten times
larger lowers that illustrative event time tenfold. Neither that time nor a
geometric cross section is the core-collapse time or the transport coefficient.
Angular/velocity-weighted microscopic scattering must determine the relevant
heat and viscosity rates. No cross section is derived here.

## Concrete next discriminator for this candidate

1. Choose the microscopic action and the counting of free versus polarization
   energy. ARGON's M100 fragments are an existing test object but a separate
   theory branch; original Phi/X needs its own derivation. Write any bridge
   coupling and all reciprocal source terms explicitly before a galaxy fit.
2. Extract a transport kernel from measured matched isolated/pair dynamics,
   including internal excitations, charge, binding and escaped E/J. Check
   whether ordinary conservative conduction/torques have a sufficient rate.
   A small exact elastic-conservation audit is not that measurement.
3. Forward-evolve one finite stock with the measured kernel and independent
   assembly histories; no universal imposed alpha/temperature or per-dwarf
   spin tuning. Preserve the finalized CFG918 capacity constraints.
4. Sextans' cored reference endpoint needs its entire1.15% non-core stock to
   reach~128km/s. Demonstrate that without extra core loss, not just an allowed
   endpoint. Reconcile the population-based stock problem before claiming a fit.
   Include the outer-star mass response in Fornax/LeoI and tides/return flow.
5. Re-test galaxy settling, merger response, cluster/lensing constraints and
   normalization in the SAME closed model. A successful dwarf mechanism is
   not permission to retain incompatible force-sector assumptions.

RUN/STATUS
run_001/manifest.json: completed and validated v2;18 bounded checks, no heavy
jobs. This evaluates exact identities and an illustrative event clock only.
No physical solver, force law, frozen criteria, publication or shared CURRENT
changed. Recommendation and failures retained; candidate mechanism OPEN.
