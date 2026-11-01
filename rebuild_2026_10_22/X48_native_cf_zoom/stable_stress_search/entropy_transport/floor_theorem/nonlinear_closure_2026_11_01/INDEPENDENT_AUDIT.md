# Independent audit of the nonlinear startup continuation

**Normalized target.** For the unchanged virgin-sphere semidiscrete ODE,
prove a number `T>0`, independent of every integer `N>=32`, such that
`x_i(t_a+s)>=4` for every `0<=s<=T` and
`1<=i<=ceil(N/4)`. Here `x=-theta`, `rho(t_a)=1`, `K(t_a)=0`,
`x(t_a)=C_a`, `M=pi/3`, and the exterior nodal mass is `dm/2`.

**Primary verdict: incomplete, with the smallest missing implication being
a mesh-uniform improvement of an actual-solution bootstrap.** None of the
audited notes establishes the density/compression hypotheses on a
common interval or the required nonlinear central pointwise estimate.
No counterexample to the specified trajectory is established either.

The conditional new results survive this audit. In particular, the actual
heat coefficient commutator left open in equation (27) of the preceding
entropy-energy note is now bounded by H6 under the expressly stated
prefix hypothesis. H28--H37 also account for the heat contribution to the
full first energy's weight derivative. This is a substantive resolution
of those named estimates; it is not an unconditional closure of that
energy or of the target.

Review provenance: fresh delegated audit, independently reconstructed from
the exact source and raw proof notes, using the proof-audit skill. The
auditor did not author the reviewed notes. This provenance is distinct
from mathematical proof; it does not exclude correlated conceptual errors.
Only this audit file was written. No source, author note, initial datum,
parameter, numerical artifact, or previous proof note was changed, and no
trajectory or new collapse grid was run.

## Claim cards and dependency graph

All statements concern finite ordered spherical geometry with positive
cell volumes and accepted `K>=0`, over the real numbers. All differences
are actual finite-edge differences; no continuum limit or frozen-graph
substitution is used.

1. `heat_absorption.md`: on a prefix `I={1,...,J}` of the actual solution,
   assume `2<x_i(v)<=8` for every `0<v<=s<=10^-3`, common activation,
   and spatially constant references in H3. Then H6 holds for every
   nonnegative weight supported on internal prefix edges. For
   `s<=10^-6`, H7 follows; a supported material cutoff gives H27.
   With differentiable references, H37 is a complete first-energy
   inequality with the local work H35 retained explicitly.
2. `viscous_energy.md`: on an active compressing prefix, the actual old
   stress `q=kappa(x-2)` has the identities (6), (11), (15), and (16).
   Under (17), the moving density-gradient energy obeys (19). The
   correction stress still creates a mechanical memory-gradient norm.
   Equations (28) and (30) refute an unconditional nonpositive heat sign
   for either proposed plain gradient square; (26) proves only
   unweighted total-variation contraction under heat alone.
3. `bootstrap.md`: under the actual inner-three-quarter density cap (D),
   conserved energy controls the global gravitational and kinetic
   energies and the prefix radii. The actual truncated scalar boundary
   problem then obeys (11). Adding the cut sign (B) and nonlinear input
   (17) bounded above by one yields the central-quarter conclusion.
   These sufficient inputs remain hypotheses.
4. `adverse_trace.md`: a one-sided actual cell compression cap `x<=U`,
   with `UT<=log(2)`, gives A1 for `0<=p<3`. The existing reference
   bound `nu_d>=24s^2` on `T<=.001` gives A5. The conclusion controls
   a time integral, not boundary amplitude or propagator transfer.
5. `coupled_gradient.md`: no smooth, state-only positive endpoint metric
   of the specified nearest-neighbor `(z,K)` gradient form has a
   state-box-uniform heat-work bound by locally bounded functions of
   the specified zeroth- and first-gradient norms. Optional geometry
   factors have a finite nonzero local limit. This is a scoped energy
   obstruction using instantaneous admissible states, not a trajectory
   claim or an obstruction to every possible energy.

The dependency graph is:

```text
exact material/transport law + ordered geometry
  |-- prefix 2<x<=8 [unproved common-time input]
  |     |-- integrated rho bounds and prefix K maximum
  |     |-- exact stress inverse + exact geometry ratio
  |     |      -> H6 -> H7 -> H27
  |     |-- shared heat flux for S and its weight
  |            -> H28--H37
  |                   -> density-gradient and local-work closure [missing]
  |-- old-stress coordinate + compressing prefix [conditional input]
  |     -> old-stress/density energies
  |            -> correction mechanical memory gradient [uncontrolled]
  |-- prefix density cap (D) [unproved common-time input]
  |     -> conserved-energy geometry -> scalar boundary barrier
  |     + cut sign (B) + nonlinear propagator input <=1 [unproved]
  |            -> central-quarter target
  |-- one-sided cut compression cap [unproved common-time input]
        -> A1/A5 -> time-integrated adverse boundary input
              -> separated boundary transfer [missing]

closed localized nonlinear energy [missing]
  -> actual nonlinear central pointwise estimate [missing]
  -> improvement of common-time bootstrap [missing]
```

Every displayed leaf is an internal identity/inequality or an explicit
unchecked actual-solution hypothesis. No external regularity theorem is
load-bearing. The earlier leading-model smoothing theorem is not a
nonlinear actual-solution estimate.

## Obligation matrix

| Obligation | Audit status | Consequence and limitation |
| --- | --- | --- |
| Source law, both heaters, signed memory stress, outward heat gates | passed | Exact source retained; no quiet-branch or gate derivative is discarded. |
| H8--H14 startup state box and prefix `K` maximum | passed under H1 | Derived from integrated actual compression; exterior cells cannot supply inward heat to a prefix maximum. |
| H18--H21 finite-edge constitutive inversion | passed under H1 | No assumed compression gradient or interpolated compression is used. |
| H6/H7 old spatial commutator (27) | passed under H1/H3 | Mesh-uniform nonlinear bound, including the remaining `s^6 D(z)` term. |
| H24--H27 cutoff and collar work | passed under support hypotheses | Actual finite graph boundaries and inactive exterior divisions are handled correctly. |
| H28--H37 weight derivatives | passed under H1 and differentiable references | Exact heat-weight flux included; H35 remains explicit unestimated local work. |
| Moving old-stress energy and density-gradient propagation | passed under stated prefix hypotheses | Dissipation is for old stress, whereas H37 dissipates full stress. |
| Heat sign failures (28), (30) | passed as admissible-state constructions | Reject two sign inferences; do not refute the virgin-sphere trajectory. |
| Heat-only unweighted `TV(K)` contraction | passed | Does not control the mechanical weighted quadratic memory gradient. |
| Density-cap energy geometry and truncated scalar barrier | passed under (D) | Outer-quarter amplitude assumptions are unnecessary for these two steps. |
| Algebraic cut ghost and sign-only boundary reduction | passed | Positive cut stress requires no upper amplitude cap; negative cut input is retained. |
| A1/A5 adverse trace integral | passed under the one-sided cap | No lower compression or upper `K` cap is needed for this conditional result. |
| Coupled-gradient exact heat derivative and thermodynamic pullback | passed | Metric-coefficient heat derivatives are included in (5)--(7). |
| State-only coupled-metric obstruction, final scoped version | passed | Rank-one incompatibility and the positive checkerboard defect exclude only the explicitly stated closure class. |
| Proof of a common-time density/compression cap | not addressed by a closing estimate | Fixed-mesh activation continuity does not supply a uniform interval. |
| Full nonlinear local work/density-gradient closure | incomplete | Neither old-stress nor full-stress route has a closed energy estimate. |
| Actual nonlinear local pointwise control and first-exit improvement | incomplete | No common `T`, (UC), or unconditional floor follows. |

## Decisive reconstructions

### The actual heat estimate is valid and resolves the named commutator

From `z_t=x` and H1, `e^(2s)<=rho<=e^(8s)`. The source ramp gives
`11s^2<=h<=197s^2` and `0<=h'<=49s`. At a prefix maximum of `K`,
the inward entropy gate is closed and every outgoing luminosity is
nonnegative, so heat contributes no positive amount. The exact heaters
obey `Q<=197s^2(24+3200K)`, which yields `K<=1600s^3`.
Thus H12 is available on the whole mean-value box.

The exact endpoint subtraction

```text
nu_r Delta x = Delta f - x_l Delta nu + 2 Delta kappa - Delta P
```

is essential. It gives H19 and hence
`|Delta alpha|<=9s^-2|Delta f|+5800s^-1|Delta z|
+1.2e6|Delta K|`. Likewise, the exact potential difference gives
`|Delta K|<=.55|Delta q|+326000s^5|Delta z|`. These are finite-edge
identities and inequalities, not consequences of a bare amplitude bound.

The centroid inequality `4*pi*r_i^2*d_i>=V_i/4` gives
`ell/a<=16200s^4` on all internal prefix faces, including the first.
Squaring the previous bound produces exactly the H23 constants
`2.460375e13`, `1.021815e19`, and `2.7e19`. The extra density term
after converting `Delta K` is `9.31662e34*s^18 D(z)`, less than
`.1*s^6 D(z)` on `s<=.001`. H6 follows with the printed constants.
Young's inequality gives H7 at `s<=10^-6`; no `N` occurs.

For the cutoff, the work constants in H25 follow from
`(Delta phi)^2/bar phi<=4(Delta chi)^2`. The exact material geometry
gives H26. The chosen cutoff covers every `i<=ceil(N/4)` because
`theta_ceil(N/4)<=1/4+1/(2N)<=17/64<9/32` for `N>=32`.
If an edge has a positive endpoint cutoff, its left index satisfies
`i<3N/8+1/2`; hence `i+1<3N/8+3/2<=N/2`, for `N>=32`.
Both endpoints are therefore in `1,...,ceil(N/2)`. This is an all-N
argument; a finite residue check was only an arithmetic sanity check.

The older equation (24) is explicitly a spatial pairing. H28--H37 go
further: differentiation of `V f^2/(2nu)` contributes
`-V f^2 nu_K H/(2nu^2)`. Combining this with `V f S_K H/nu` gives
exactly the shared flux `F_h=alpha f-beta f^2/2`. No pointwise `H`,
`K_t`, or gate-Jacobian estimate is needed for this cancellation.
The H30 beta bounds and the H31 product identity are correct.
The printed pre-conversion H33 constants are reproduced; the converted
heat coefficient is `7.97148e21<8e21`, and the extra density coefficient
after factoring `s^6` is below 46 on `s<=.001`.

The remaining weight terms H36 are nonpositive on the assumed branch.
Thus H37 really is a full first-energy inequality with H35 retained.
It is not a closed estimate: the reaction work and density-gradient
propagation have not been bounded by the displayed energy/dissipation.
Division by activation-zero coefficients is used only for positive time;
integration from activation also needs the appropriate startup control.

### The old-stress energy has a valid but different obstruction

With `q=kappa(x-2)`, direct differentiation gives
`q_t=kappa L_r(q+e)+kappa R+beta*x*q` and
`(V/kappa)'=-x(1+beta)V/kappa`. Substitution yields precisely (11),
including its positive `x(beta-1)f^2/(2kappa)` term. It cannot be
dropped. The density error identity (15) and two-endpoint product
identity (16) are correct. Since `kappa` increases, the latter has
`B_e>=0`; since the whole earlier prefix compresses,
`a_e'/a_e=-4b_e/3<=0`.

Using `kappa>=k_-s^2`, Young's inequality gives the coefficient
`lambda/(2 epsilon k_-^2)` in (19), as printed. The residual
`s^6 D(z)` has lower-order size relative to this time-weighted energy.
However, (19) requires the gradient norm of **old** stress as input.
H37 dissipates the gradient of **full** stress. Replacing one by the other requires
control of the correction `e`, whose `K` derivative creates `s^4 D_a(K)`.
The bound `ell/a<=Cs^4` has the wrong direction to control that norm
by heat dissipation, and some gated faces have `ell=0`.

The two three-cell examples are valid within the stated instantaneous
active state box. In (28), equal `W_1=W_2` makes face 1 active, while
the higher `W_3` closes face 2's temperature gate. The resulting work is
`L_1/(dm W_1)*[-2a_1 epsilon+a_2 p]>0`. In (30), face 2 instead
closes by the entropy gate, and the printed potential-gradient work is
positive. Positive cell volumes determine an ordered actual geometry;
the choices of epsilon use its actual conductances. Constant adjacent
states remove the neighboring face terms. Neither construction asserts
reachability from homogeneous activation.

For unweighted total variation, write the heat derivative using
`sigma_i=sign(p_i)` on nonzero drops. A nonzero `L_i` has `p_i>0`,
so `sigma_i=1` and its coefficient is
`(sigma_(i-1)-1)/(dm W_i)+(sigma_(i+1)-1)/(dm W_(i+1))<=0`.
At `p_i=0`, `L_i=0` and `p_i'|heat>=0`, so choosing `sigma_i=1`
equals the upper directional derivative of `|p_i|`. Missing endpoint
signs are zero. This proves (26), without upgrading it to a weighted
quadratic gradient estimate.

### The density-cap geometry and ghost reduction are valid

Summing positive volumes under (D), then using ordering outside the
prefix, gives (6). The lower bound `J/N>=23/32` and the actual half
outer mass give the gravitational bound (7). Exact conserved energy
and nonnegative internal energy give the kinetic bound. Integrating
the weighted radius norm yields (8); the outer tail nodal mass is at
least `15M/64`, so the prefix radius bound follows. No outer-quarter
compression or expansion cap enters this argument.

The jump-rate bounds (12) follow directly from the actual radii and
volumes. Taylor's inequality gives (13), with coefficient below
`3e8*s^2`; the exponential supersolution and
`(J-ceil(N/4))/N>=1/2-2/N>=7/16` give (14). The exterior half mass
does not enter these interior rows and has not been replaced incorrectly.

The algebraic ghost is `w_J=B_d-S_J/nu_d`, with `B_d=S_d/nu_d`.
It gives `S_d-nu_d*w_J=S_J` exactly, while `delta S_J=0`.
Consequently the restricted identity (16) includes the actual cut stress.
When `S_J>=0`, the ghost is at most 12, irrespective of positive stress
amplitude. If `S_J<0`, the adverse input is `S_-/nu_d`; it cannot be
discarded. The conditional implication (LC) to (19) is valid, including
the ceiling and the final numerical margin. Its premises have not been
improved along the actual solution on a common interval.

### The adverse trace bound controls an integral only

The source law gives `S_-<=(-Fdot)_+`. Under `x<=U`, continuity gives
`rho<=e^(Us)<=2`; the ramp then implies
`(Fdot)_+<=6U^3 e^(2UT)s^2=:As^2` and `0<=F<=As^3/3`.
For `w=s^-p`, integration by parts has a vanishing lower endpoint
when `p<3`, and
`integral w Fdot = w(T)F(T)-integral w'F>=0` for `p>=0`.
The truncated identity also bounds the negative part before passage
to zero. Hence its weighted negative variation is at most its weighted
positive variation, giving A1 with the printed constant.

On the existing reference interval, `x_d>=4`, `rho_d<=2`, and
`h_d>=16s^2(3-8s)>=32s^2`; thus `nu_d>=24s^2` and A5 follows
by choosing `p=2`. Quiet-phase crossings preserve these identities.
This lemma needs neither a lower compression bound nor an upper `K`
bound. It still assumes a one-sided compression cap, and no bound for
the actual separated boundary-transfer operator acting on this L1 input
has been supplied.

### Focused addendum: the coupled-gradient obstruction is valid within its scope

The exact gradient of `E_M` with respect to `K_i`, with instantaneous
geometry fixed, is (5): differentiating the two adjacent drops gives
`w_(i-1)-w_i`, and differentiating their metrics gives the displayed
quadratic coefficient terms. Substitution of the full shared heat flux
gives (6), including all `M_K H` contributions. Removing heat from the
remaining coefficient derivatives gives exactly (7).

At a strict warm open-gate state, the principal heat row is
`D=(C b psi_z, C[b psi_K+b_q J])` in `(z,K)` variables. The sign in
`K_t=gamma D dot (z_rr,K_rr)+lower-order work` is positive, since
luminosity is outward and its gradients use `p=-z_r`, `q=-K_r`.
The highest-order gradient-energy heat work is the negative product
of this row with `m=(M_zK,M_KK)`. This quadratic expression has the
required sign for every second-derivative direction only when the two
rows are positive multiples. The direction in (13) gives exactly
`-(M_KK D_K/4)*(r_M-r_h)^2` for their product when the ratios differ.
The coefficient heat derivatives in (5) have fewer spatial differences
and do not change this principal test.

The exact derivative
`partial_p eta_h=-b b_q psi_z^2/(b psi_K+b_q J)^2<0` makes the
necessary row ratio incompatible with a state-only metric at two
different density gradients through the same warm state. The pulled-back
thermodynamic Hessian in (15) also checks: `v_z=-1/rho` and
`sigma_K=K^(-2/3)/3` give the printed matrix and ratio
`3K rho h/(2W)=psi_z/psi_K`. This ratio is strictly larger than
`eta_h` on an open gated face. Its positivity does not remove the
fourth-order defect.

The finite-edge checkerboard test correctly realizes that defect without
approaching either gate switch. At a fixed positive-radius warm profile,
`a~N`, `dm~N^-1`, and centroid separation is `~N^-1`. With
`epsilon=N^-3/2`, the gradient perturbation is `O(N epsilon)=O(N^-1/2)`.
Thus open gates and the strict instantaneous state box persist for all
sufficiently large `N`, even though this threshold can be very large
when the fixed startup time is small. The leading terms are
`delta G=4a epsilon*(-1)^i chi*(m dot v)` and
`delta H=-4A epsilon*(-1)^i chi*(D dot v)/(dm W d_centroid)`.
Their summed product has the positive size `cN^4 epsilon^2=cN`.

The claimed remainder order can be checked directly. The quadratic flux
remainder is at most `O((N epsilon)^2)=O(N^-1)` on this strict branch,
so its discrete heat divergence is at most `O(1)` cellwise. Pairing it
with the leading `delta G=O(N^-1/2)` gives `O(N^1/2)=o(N)` after
summing. Smooth state/metric coefficient variations in `G` have
cellwise size `O(epsilon)+O(N epsilon^2)` beyond the leading term;
their pairing with `delta H=O(N^1/2)` is also `o(N)`.
The smooth-base `G^0=O(N^-1)` and bounded base heat derivative give
only lower-order cross work. Reconstructing the radii from the perturbed
positive volumes preserves ordering; centroid and cumulative-radius
variations have fewer differences than the principal flux response.
Cutoff variation likewise contributes lower-order work on its fixed
smooth support.

The perturbation first-gradient quadratic norms have size
`O(N^2 epsilon^2)=O(N^-1)`, while the base norms stay bounded.
The other exact terms in (7), and the companion first stress/temperature
energy, have bounded work at the fixed positive startup time. A positive
time power multiplying the metric cannot remove the divergence in `N`.
Consequently the final stated class cannot give the proposed uniform
bound on the whole amplitude state box. The test imposes no actual
activation history and proves no reachable-trajectory counterexample.
Gradient-dependent or nonquadratic energies, higher mechanical
derivative dissipation, and estimates using additional proved trajectory
constraints remain outside its scope.

Before the final pinned version, this audit requested two scope
clarifications: the proposed right-hand-side functions must be locally
bounded on bounded norm sets, and extra positive geometry factors must
have a finite nonzero local limit uniformly in `N`. The author applied
both. A factor vanishing like `d_centroid^4`, for example, would suppress
the positive defect while also losing the gradient coercivity needed for
this continuation; it is not included in the final claim. No remaining
core mathematical error was found in the final scoped argument.

## Exact remaining gap and strongest safe statement

The strongest safe statement is the conjunction of the conditional
estimates above. They reduce several previously open terms and improve
the geometry/boundary hypotheses. They do not establish a common `T`,
the startup premise (UC), or an unconditional entropy floor.

A future closing proof must produce, on the actual solution and uniformly
over all `N>=32`, either the improvements of (D), (B), and the nonlinear
propagator input in (LC), or an explicitly proved replacement for them.
Within the energy route, it must control local work and propagate the
appropriate density gradient without an uncontrolled mechanical memory
gradient, then obtain a local pointwise estimate compatible with the
radial central embedding obstruction in the preceding entropy note.
The singular `E/s` inequality alone is not an initialization or a
common-time argument. A finite-mesh activation expansion, agreement on
finite grids, or a leading-model estimate cannot fill these implications.

The cheapest next discriminating check is a precise proposed bound for
the local work/density-gradient closure or for the separated actual
boundary-transfer operator applied to A5. It should state its startup
time weights, norm, support collar, and every still-assumed cap. This
audit supplies no new proof route to close those gaps.

## Source checks, arithmetic checks, and exact revisions

The auditor read `MaterialParameters`, `activation`, `density_weight`,
and `bulk_viscosity_source` in `material.py`; geometry, momentum, and
energy in `collapse.py`; memory damping and centroid geometry in
`transport.py`; and both outward heat gates in `convective_transport.py`.
Independent differentiation and finite summation by parts were used for
the identities above. An in-memory Python `fractions.Fraction` check
recomputed the printed H13/H19/H20/H23/H26/H30/H32/H33 constants,
both absorption times, and the bootstrap gravity, moment, radius,
exponential-rate, and final-margin inequalities; every check passed.
These are algebraic checks, not sampled-solution evidence. No external
theorem was needed and no `.mathbox` ledger was present at the workspace
root. Applicable ancestor `AGENTS.md` files were checked; none was found.

Commands used were read-only `cat`, `sed`, `rg`, source/ancestor inspection,
SHA-256 hashing with Python `hashlib`, and the in-memory exact-arithmetic
checks. The sole mutation was creation of this file. Paths in the table
are relative to `stable_stress_search/`; `D/` abbreviates
`entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/`.

| Audited input | SHA-256 |
| --- | --- |
| `D/heat_absorption.md` | `b98843cec40271ef4a16bdb6c15baf50a43c203d6367fbf3ae72a4d299b74379` |
| `D/viscous_energy.md` | `874881bdaeb046fc607d500fc01d2402e8d4db1264c302e647ac137a39a920a1` |
| `D/bootstrap.md` | `0b201a5eb41353945a1e6a374a69a3e3c290a961d6651ef9d0ff83737d5e6107` |
| `D/adverse_trace.md` | `9f2ac425673523ec6b64ca4bb2073a4b9d9c3c9291b0b40ef5b7dae640a9f291` |
| `D/coupled_gradient.md` | `f0c69a7b65cc8c3581e42d22d5ebbfa2b6cbf21b84a21f9a34e85e412e556492` |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/floor_theorem/TARGET.md` | `93792a4df2982bb70bbb68be3878405dbd3f8e2ea735c5f586ce0b28b2394b14` |
| `entropy_transport/floor_theorem/startup_energy_route.md` | `06630aecae84c9b618e84c1ddded3f2025f7a89f7dca634bbbb05f50d0e2380b` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/TARGET.md` | `845098298ef29ab6212a0c58edf46287806bb9d5944b794fc7b90e84f1f9b846` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/all_mesh_certificate.md` | `15582ff1b45a715fccc5c84cd4883fa533ce714fb77b7ef091aa53205ba69a18` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/entropy_energy.md` | `bb4429ad5f3c9345d2c6d44a7864c407e273caad13ed3643fac5aa822c9990e3` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/effective_flux.md` | `ba03913a2d497fcefc346b8f04cc0da2d128a3f7dee34ee535c36155459f3ba3` |

No mathematical error requiring an author-note repair was found in these
exact versions. This is a pass for their stated conditional and
obstruction claims, and an incomplete verdict for the unconditional target.
