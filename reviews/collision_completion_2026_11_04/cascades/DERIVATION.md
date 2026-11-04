# CC10 actual neutral cascades and occupation forces

The complete vacuum, charged-relic and cold-photino target is still open. This
package supplies an executed physical 25-group collision network, charged-return
tests, coherent neutral cascade transfer, and a short coupled field/population
history. The coordinator is continuing the cooling history with these inputs.

Base contract: `../CONTRACT.md`, shared revision
`fd417eea045a0b6259b8efff5e20ca62a2e14f7e`. Each computation's v2 manifest pins
the exact source and data bytes; shared branch display order is not provenance.
Only this new `cascades/` directory was written.

## Physical states and actual vertices

All masses and rates below are divided by the appropriate power of
`mu=sqrt(f)`. The packet is `e=h=lambda=.003`, `g=sqrt(29/200)e`,
`mu=2e6 GeV`, `xi=.02`. The scalar kinetic coefficient is 62.

`network.state` first adapts each scalar and Takagi degeneracy block to residual
`Q²`, then to the unbroken gauge Casimir. An additional gauge-component
projector separates the massless U1 gaugino from the Goldstino. The twelve
charged zero scalar Goldstones are removed. All two neutral zero scalars remain.
The physical counts are 86 real scalars and 73 Weyls, including 36 charged real
scalars and 36 charged Weyls. The 25 species groups are:

| representation | scalar groups | fermion groups |
|---|---:|---:|
| charged `(3,2)+conjugate` | 3, each 12 real states | 3, each 12 Weyls |
| neutral SU3 octet | 4, each 8 real states | 3, each 8 Weyls |
| neutral SU2 triplet | 4, each 3 real states | 3, each 3 Weyls |
| neutral singlet | massless group of 2; massive group of 4 | Goldstino 1; U1 gaugino 1; massive group of 2 Weyls |

Group IDs use `S/F`, `c/8/3/1`, and increasing rigid-tree mass rank. The raw
unbroken gauginos are `F1_1,F3_0,F8_0`, with physical spin degeneracies `2,6,16`.
The Goldstino is `F1_0`. Lowest charged groups are `Fc_0` (24 spin states) and
`Sc_0` (12 real scalar states). A charged scalar real-state count equals the
particle-plus-antiparticle degeneracy. For signed populations `signed_lift`
halves charged degeneracies and assigns charges `+1,-1`; multiplying all charges
by `sqrt(5/12)` restores the generator normalization.

The actual component FFS and SSS vertices are transformed into these bases.
For a scalar parent group A and fermion daughter groups I,J, define

`A_AIJ = (2-delta_IJ)/d_A sum_{a in A,i in I,j in J}|y_ija|²`,

and define `B_AIJ` by replacing the squared norm with `Re(y_ija²)`. Here `d_A`
counts real scalar columns, not Weyl spins. With `z_i=m_i/M`,

`Gamma(A->I J)=M beta/(16 pi) [A_AIJ(1-z_i²-z_j²)-2 B_AIJ z_i z_j]`.

For SSS, the analogous ordered cubic norm gives

`Gamma(A->J K)=C_AJK beta/(32 pi M)`.

For a fermion parent I, average the FFS norm over its Weyl columns. Its
spin-averaged rate is

`Gamma(I->J A)=M beta/(16 pi) [A_IJA(1+z_j²-z_a²)+2 B_IJA z_j]`.

The physical spin degeneracy is twice the parent Weyl-column count. These
definitions reproduce the prior ordered-index width normalization. All
unpolarized two-body decays have an isotropic rest-frame direction after the
stated spin average.

`vertices.py` stores these invariant norms even for kinematically closed
channels. `VertexBackground.at(x)` interpolates the norms, then reconstructs the
mass-dependent amplitude and exact two-body phase space. It never interpolates
a closed zero-width endpoint directly into an open width. The data cover 209
points on `.1 <= x <= 200`: step .05 through4.1, .2 through10, .5 through30,
then coarser points. The exact first grid is serialized. Gaugino current rates
and finite one-loop kinematic masses are separately interpolated. `full_events`
replaces the lowest F/C-to-gaugino channels with these current-projected rates;
it does not add them to the tree channels a second time. Other heavy channels
use tree amplitudes with the small gaugino kinematic masses inserted.

Coverage is all physical tree FFS and SSS vertices. Massive-vector and loop
decay exits are omitted. This is complete tree coverage for the low B3 example
at x=3 and every state reached from the singlet parent at the exact pole, where
all broken-vector exits are kinematically closed. Broad higher-parent rates
retain this coverage qualification. Exact fourfold singlet interference is
handled by channel matrices, not by asserting that a diagonal group rate is
the coherent answer.

## Conservative statistical event measure

Let `q=p/Tc`, with a positive quadrature weight `W_i` for `q² dq`. Occupations
are per physical spin state. Evolve comoving number coordinates

`Y_si = g_s W_i f_si/(2 pi²)`,

so physical number is `Tc³ sum_i Y_si`. For each physical parent node and
rest-frame angular quadrature node, generate exact Lorentz-boosted two-body
energies. Project each daughter to two neighboring nodes with positive weights
that sum to one and reproduce that daughter's energy. Each event has
stoichiometry `nu=(-1,alpha,1-alpha,beta,1-beta)` and satisfies

`sum_i nu_i E_i(x)=0`.

The vacuum forward event coefficient is

`K = [g_parent W_parent/(2 pi²)] Gamma M/E_parent w_angle/2`.

The `statistics/quantum.py` entropy projection uses `eta=+1` for bosons and
`eta=-1` for fermions. Its forward and inverse products are

`F = f_parent product_children (1+eta_i f_i)^weight_i`,

`R = (1+eta_parent f_parent) product_children f_i^weight_i`.

The number equation is `dY/dtau = sum_events nu K(F-R)`.
Both inverse processes and final-state factors are therefore present, including
neutral inverse reactions. This is a finite entropy-variable projection; it is
not claimed to be the continuum collision integral evaluated exactly.

Writing `ell_i=log[f_i/(1+eta_i f_i)]`, the sign of `F-R` equals that of
`ell_parent-sum_children weight_i ell_i`. Consequently the finite event entropy
production is nonnegative. A common Bose/Fermi equilibrium with affine energy
and conserved-charge odds satisfies detailed balance exactly. Signed lifting
also gives `nu dot Q=0` event by event. All accepted implicit number-Newton
steps enforce nonnegative populations and the fermion occupation ceiling.

Out-of-support events are omitted, with the actual population-weighted forward
rate recorded. The tested early direct histories have zero such weighted
omission. This does not establish a bound on unrepresented inverse production
from an arbitrary hard bath. In particular, these early `q<=80` grids are not
late grids: at `Tc=1e-6`, pole daughters need `q` of order40000. The separate
neutral transfer code uses physical momentum nodes through `.3 mu`.

### Exact angular integration of the finite projection

The warm angular convergence failure has an executed resolution. Every daughter
energy is affine in the rest-frame cosine. Split its interval at every energy
grid boundary of either daughter. On each resulting interval, rescale to
`-1 <= u <= 1`; all interpolation weights have the form `w_i=a_i+b_i u`.
The forward and reverse statistical products are each `exp(A+B u)`.

Define `I_n(A,B)=integral_{-1}^1 u^n exp(A+B u) du`. The number RHS uses only
`I_0,I_1`; the analytic number Jacobian uses `I_0,I_1,I_2`. Away from B=0,

`I_0=2 exp(A) sinh(B)/B`,

`I_1=I_0 [coth(B)-1/B]`,

`I_2=I_0 [1-2(coth(B)-1/B)/B]`.

The implementation uses Taylor series near zero and endpoint logarithms at
large |B|. It does not subtract large A and |B| to recover a modest endpoint
exponent. The physical interval half-width multiplies the reaction measure.
With stoichiometric sign s_i, each RHS contribution is

`K s_i [a_i(I_0^F-I_0^R)+b_i(I_1^F-I_1^R)]`.

For a pair of node positions i,j the derivative combines

`a_i a_j I_0+(a_i b_j+b_i a_j)I_1+b_i b_j I_2`,

with the appropriate logarithmic derivative of f or availability and the
physical number measure. Repeated daughter nodes are summed by sparse COO/CSR
construction. Separate availability arrays preserve sub-ulp Pauli holes.
At exactly zero fractional child factors the projected vector field is not
classically differentiable; its numerical Jacobian regularization is declared.

`angular_exact.py` is the frozen reference. `run_angular001` verifies elementary
moments, duplicate daughters, synthetic and actual directional Jacobians,
energy, detailed balance, entropy, and an independent32-node quadrature on
every split interval. The actual warm and pole RHS agree with this independent
reference at about `1e-15`; Jacobian direction errors are `6e-11`–`2e-10`.
Global two-angle RHS errors are30–40% near the warm crossing; eight-angle
errors remain4–5%, and even64angles leave about .15% at those points. Those
errors explain why the coarse-angle histories cannot be promoted as physical
solutions of the discrete momentum model.

`angular_fast.py` has the same exact factories and number protocol. It
vectorizes all channel-by-parent-node grid crossings and brackets. In
`run_fast002`, its indices, affine weights, coefficients, RHS, Jacobian, gross
rate and omission vectors are bit-for-bit equal to the reference builder at
the four tested physical points. An eight-phase memory-lean composite of
797747segments builds in .300s, evaluates RHS in .172s and Jacobian in .404s
in this environment. Peak RSS including reference comparisons is558MB.
The composite keeps `local_events/localops`, `phase_weights` and
`energy_average` for the scalar covariance. It avoids duplicating all phase
segment arrays into a second concatenated operator.

## Neutral energy, force and action

Each neutral population remains an explicit species. Its energy density and
dimensionless-x force contribution are

`rho_s=Tc³ sum_i E_si Y_si`,

`d rho_s/dx=Tc³ sum_i [d(m_s²)/dx]/(2 E_si) Y_si`.

The numerical force is the derivative of `rho/mu^4` with respect to `x`;
the physical field force has units `mu^3`. A negative neutral mass slope pushes
toward larger x. Calling a massive neutral daughter radiation discards this
force and generally violates the scalar-plus-particle energy ledger.

For the action `J=integral p_x dx/(2 pi)`, `dJ/dE=1/omega`. At fixed total
energy an occupation variation gives

`delta J=-(Tc³/omega) sum_i <E_i> delta Y_i`.

Local events conserve the energy of all particle species, so their covariance
numerator simplifies to

`C_action=Tc³[<sum E C>-sum <E><C>] = -Tc³ sum <E> C_avg`.

Thus the usual averaged equation reads

`d ln J/dN=-3+C_action/(omega H J)`.

`averaged.py` exposes both the full local energy residual and this covariance.
The coordinator's warm integrator instead evolves total energy and populations
and reconstructs J, which preserves the same accounting without a radiation
reservoir. A timescale ratio alone is not an averaging theorem; direct short
histories and occupation changes are tested separately.

## Executed evidence

All listed successful runs have fresh v2 manifests, one numerical thread,
wall<=240s, CPU<=235s, exact inputs before/after, and measured process RSS.
The computation runner owns the complete command and software provenance.

* `run_network001`: all25groups and 178–194 open grouped channels at eight x
  points. Physical counts, Takagi reconstruction and charge checks pass.
* `run_basis002`: per-daughter four-singlet absorptive matrices transformed
  into the prior CT09 basis. Their sum reproduces the prior complete pole
  matrix with maximum error `4.9631e-24`. Every channel matrix is PSD to the
  stated floating tolerance.
* `run_local001`: full quantum fixed-background dynamics at x3,5 and the pole,
  Tc=.004. Event energy residual<=`1.11e-16`, thermal detailed-balance
  residual<=`2.55e-16`; signed event charge is conserved. Starting with only
  Fermi FD particles, after ten B3 lifetimes the charged fractions are
  `.8644756` at x3 and `.8595481` at x5. Neutral forces are
  `-1.65207e-11` and `-9.65939e-12` in the above dimensionless convention.
  These are finite static tests, not equilibrium relic predictions.
* `run_vertices001` and `run_audit_vertices002`: all closed/open invariant
  vertices and exact-threshold interpolation. Weighted quantum-RHS and force
  errors versus fresh direct component evaluations are serialized at eleven
  test points, including the F/C crossing and scalar pole. Their maxima are
  `.00137459` for the RHS L1 relative norm and `5.08823e-6` for the weighted
  total force. The covariance
  identity passes on an eight-phase projection of the recorded orbit.
* `run_coupled003`: actual direct scalar field plus25quantum populations to
  `N=1e-5`, with leading gravity profile, physical initial FD quadrature and
  returning channels. The initial distribution is sampled by five8-node GL
  panels, not the coarse uniform local-test grid. At the endpoint the charged
  fraction is `.9973010698`, explicit massive-neutral energy is
  `9.16845e-12 mu^4`, neutral force is `-4.95890e-13` and charged force is
  `1.78350e-10`. Removing neutral force changes the endpoint field phase
  substantially; it is not a capture verdict.
* `run_coupled004`: timestep halved to50000 in mu inverse units; full f,x,v,
  time snapshots are exported. Charged fraction `.9973012021` differs by
  `1.32e-7` absolute from the coarser step. The final x differs by .00350.
  Maximum full energy-ledger error is `2.00e-6`. Initial FD force differs from
  an independent adaptive analytic light-branch integral by `-5.66e-6`
  relative. The positive empty-cell seed is explicitly quantified.
* `run_seed001`: at x3,Tc=.004,100 number-Newton steps to `tau=1e9`, positive
  seeds `1e-25,1e-35,1e-45` give identical reported charged density and neutral
  force. Exactempty Newton line search stalls immediately; the seeded solver
  is not advertised as an exact boundary solver. The independent BDF local
  run starts from exactempty daughters.
* `run_action002`: reconstructing J at17 full direct004 snapshots gives
  `ln(J_end/J_initial)=-.03206023`; integrating twelve-phase covariance along
  the actual f(t) gives `-.03025207`. The difference is `.00180816` in log J,
  or5.64% of the observed drift. Endpoint phase, sparse time sampling and
  phase quadrature remain possible contributions. This is a measured
  averaging discrepancy, not a validation of arbitrary long histories.
  `run_action003` uses all67 snapshots and24phase nodes. Its endpoint
  difference is `.00180043`; the residual has oscillatory RMS `.00132057`
  and a fitted linear change `-.000491985` across the window. More quadrature
  alone does not remove the observed phase modulation.
* `run_coverage001`: a conservative necessary kinematic test for omitted
  broken-vector exits marks at most `.000826913` of the total particle energy
  and `.000289089` of the particle number in direct004 snapshots. This is a
  parent-population diagnostic, not an omitted reaction-rate bound.
* `run_transfer001`: a unit coherent singlet pulse `rho0=G/TrG` at the exact
  pole, with every actual secondary neutral parent retained in momentum space.
  The generator conserves energy, populations stay nonnegative to tolerance,
  and the parent density matrix stays PSD. At `tau=3e12`, about92.3% of the
  parent energy remains in massive neutral particles, mostly A2 and A3, with
  force `-1.74706e-4` per initial parent. This is a dilute static response,
  not a finite-density cosmological solution. `transfer.build_transfer`
  supplies the sparse secondary operator and channel injection maps used by
  the memory package.
* `run_warm_direct002`: restart the coordinator's immutable warm checkpoint
  at `N=.0021690179773`, where the orbit straddles the F/C ordering change.
  Three direct periods preserve all25 species, with 768 conservative quantum
  steps, no rejected steps, and maximum total energy error `7.10e-8`.
  The charged fraction relative to that checkpoint is `.9998958104`; the
  U1-gaugino yield rises by `.146006%`. Maximum soft-gaugino occupation changes
  are .15 even though integrated changes are small. Halving the timestep
  changes the charged fraction by only `8.81e-8` absolute.
* `run_warm_averaged001` and `run_compare_bridge001`: compare six-phase
  averaging with the same three-period direct history and final N, using a
  common cubic mass-squared interpolation for both event energies and forces.
  The charged endpoint relative error is `1.32968e-5`; the all-species
  number-weighted L1 error is `1.76432e-5`. The U1 yield error is `2.13984e-6`
  and its number-weighted shape error is `9.50630e-6`. The .15192 maximum
  occupation discrepancy is confined to the lowest-q cell; cells with
  occupation differences above .1 contribute only `4.88e-8` of the U1 group
  number error. Action differs by `.00036371` relative at the endpoint,
  or10.48% of the small three-period action drift. These are finite closure
  errors; an unweighted maximum occupation-change rate is not a bulk-yield
  error bound.
* The independent rest-frame angular check is consequential. At the warm
  crossing, two versus four angle nodes change the three-period charged-loss
  increment by about44% (only `4.59e-5` absolute in total charged fraction)
  and the U1-yield increment by about18%. Eight-angle refinement still changes
  those increments materially. The exact angular integration above resolves
  this numerical issue; the coarse-angle histories remain diagnostic records.
* `run_hole_diagnostic001`: positive tiny fermion holes can be retained while
  their relative Newton residual remains below the accuracy of double
  arithmetic. In the actual warm lowest-q SU2 and U1 cells, the observed
  residual plateau is around `1e-4`–`3e-4`, while a first-order roundoff-scale
  estimate is `3e-4`–`1e-3` and `dt*Jacobian_diagonal` is `5e10`–`9e11`.
  These are numerical conditioning observations, not a physical obstruction.
* `run_warm_direct_exact128` and `run_warm_direct_exact256`: restart the same
  old coarse-angle warm checkpoint with the corrected analytic operator and
  explicit mixed number/hole state. After one actual field period, the charged
  ratios are `.999976235063` and `.999976239099`. The U1 yield changes by
  `.000534392431` and `.000534398184` relative. Maximum total energy-ledger
  errors are `2.84e-7` and `7.10e-8`; both runs pass positivity, fermion bounds
  and collision-energy checks. Maximum fermion occupation relaxes to .930405
  in the finer run. The old coarse-angle soft saturation is not retained by
  the corrected operator.
* `run_warm_averaged_exact001` and `run_compare_bridge_exact001`: the same
  one-period corrected restart versus an eight-phase averaged history with
  steps<=`2e-8` in N. Charged endpoint relative error is `1.17579e-6`; all-species
  number-weighted L1 error is `1.53986e-6`. The U1 yield error is `5.09129e-8`
  and its weighted shape L1 error is `2.12864e-7`; the cycle-mean shape error is
  `1.54304e-7`. The action endpoint error is `-2.00164e-5` relative, or1.98% of
  the small action drift. This is an actual finite averaging control with the
  corrected angular operator. Its initial checkpoint came from the old
  operator, so it is a conditional restart, not a fresh corrected cosmology.

For the displaced low B3 parent at x3, the principal actual rates are

| exit | Gamma/mu |
|---|---:|
| `Sc_0+Sc_1` | `3.86594355e-10` |
| `Fc_0+Fc_0` | `1.52972513e-10` |
| `A3+R` | `1.10008482e-11` |
| `F8_0+F8_1` | `1.11248035e-10` |

The full one-way terminal carrier expectation is `1.857315664`. A dilute
momentum pulse evolved with the actual inverse-capable quantum network gives
`1.857386007` charged carriers per initial parent after40B3lifetimes. This
checks the return mechanism. It does not turn all neutral conversions into an
irreversible sink. At x25.399 the diagonal singlet expectation still returns
about .17974 carriers per parent; at the exact pole it returns zero in the
complete tree packet. Neutral inverse reactions can reopen pair production
when their populated momenta permit it.

Even a fixed-background tree-stable neutral is not a terminal reservoir along
a moving field orbit. A3 (`S8_0`) has zero decay width at x3, but its mass grows
to `.021895` and its width to about `6.40e-10` near the initial inner point
x=.18444, reopening charged daughter channels. The cooling calculation must
therefore follow the occupied A3 population through these changing thresholds.
The direct early charged deficit cannot be interpreted as irreversible loss.

## Failed and superseded attempts

Original sources were retained, not overwritten. `run_basis001` (`basis.py`)
failed on NumPy-bool JSON serialization; `basis_v2.py` produced the successful
run. `run_coupled001` (`coupled.py`) used a coarse local grid that biased the
initial FD force upward and drove x outside the pinned .1 lower boundary.
This is a discretization failure, not a physical exclusion. `run_coupled002`
uses the old recorded FD shell grid and is a sensitivity comparison; the
controlled physical-FD runs003/004 supersede it for the corrected initial
packet. `run_audit_vertices001` retained an object-copy force-audit bug and
then failed serialization; its exact source is `audit_vertices.py`, with the
corrected audit in `audit_vertices_v2.py`. Initial action-control serialization
similarly retains its original source. Failed pre-serialization runs do not
have result-level RSS measurements; none is invented retrospectively.
The first fast-builder candidate was archived verbatim as
`angular_fast_build001.py` before adding the requested public factory aliases.
`run_fast001` therefore has an archived historical input; `run_fast002` pins
the final canonical source and supersedes it. The archive hash binding is in
`SOURCE_ARCHIVES.json`. Future failed runs use `capture.py` to retain RSS even
if result serialization raises.

## Continuing obligations

The coordinator is advancing a common warm orbit-averaged history using the
actual all-species energy ledger, followed by late coherent memory where
needed. The decisive remaining checks are direct-versus-averaged action and
population control, finite momentum support through cooling, quantum-bath
phase dependence, and charged/neutral abundance evolution through the entire
window. Broad vector-open states require their actual vector widths if their
occupations become material. Loop adjoint decays, non-Abelian bound-state
formation and complete pole retuning remain separate physical leaves.
Scalar loop/thermal self energies and physical gravity matching beyond the
stated leading background and inserted gaugino masses are also not supplied
by this rigid-tree particle network.

No experiment here proves a final charged relic, cold photino abundance,
thermalization of neutral daughters, or a model-wide exclusion. The stated
finite implementations demonstrate that neutral return channels and
neutral momentum forces can be computed and cannot consistently be replaced
by immediate radiation.
