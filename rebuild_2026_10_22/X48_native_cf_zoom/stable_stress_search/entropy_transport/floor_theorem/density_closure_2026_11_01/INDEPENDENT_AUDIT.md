# Independent audit of entropy-gradient and local-reaction estimates

Base: **X48-NLC-2026-11-01-B**. Reviewer: the boundary-transfer agent,
separate from both authors of the reviewed notes. Observed shared HEAD:
`0ae3d11e4d9cce18027222b27ac565fd47373ad9`. The final byte hashes below
identify the reviewed revisions independently of the moving checkout.
The reviewer read the raw proofs and unchanged physical source and
reconstructed the critical finite-cell identities; author self-verification
was not treated as proof. Write scope for this review is this audit file.

**Primary verdict: conditional on the stated actual prefix envelope.**
The entropy-gradient estimates in Sections 4--7 of `flux_potential.md`,
the claims in `local_work.md`, and the subsequent combined estimates in
`gradient_symmetrizer.md` and `relative_entropy.md` pass this independent
review in their stated scope. In particular the last two notes now give
a complete conditional first-energy inequality with a valid activation
trace and the stated nested-collar `O(s^2)` and `O(s^5)` conclusions.
The original common-time central-quarter claim remains **incomplete**.
No estimate below propagates the provisional envelope or proves the
missing pointwise implication. Section 11 separately records the root
coordinator's narrower independent boundary-note review.
Section 12 independently reviews the subsequent bounded pointwise
continuation: its exact reductions and all-p identity pass, while its
coupled smoothing obligation remains open.

## 1. Exact claim cards and review boundary

The quantified setting is the unchanged normalized virgin-sphere
semidiscrete problem, every finite `N>=32`, exact ordered geometry,
`K>=0`, common activation density one and memory zero. The principal
conditional hypothesis is

\[
 2<x_i(v)\le8\qquad(0<v\le s\le T\le10^{-3})
\]

on each required material prefix and its cutoff halo. Constants are
independent of N, the first-cell radius, the pattern of open heat faces,
and the particular solution history satisfying this hypothesis.

The reviewed conclusions are:

1. `flux_potential.md`, Sections 4--7, equations (17)--(27), including
   the final alternative (22a): exact localized quadratic-memory heat
   balance, finite-edge conversion of `s^4 D(K)` into nonlinear heat
   dissipation, a negative-memory-gradient energy, density-gradient
   remainder and explicit forcing; propagation inequality for the
   one-sided gradient; and the resulting conditional absorption of
   the named interior mechanical memory-gradient work.
2. `local_work.md`, Sections 1--8, equations (L1)--(L23): genuine
   reference subtraction in the local reaction, finite Hardy control
   of radial shear, local-work bound, zeroth-order density energy,
   nested and coarse collar estimates, and their scoped insertion
   into the previously proved heat inequality.
3. `local_work.md`, Sections 9--13, equations (L24)--(L37): uniformly
   controlled auxiliary reaction flow, exact pullback equation on the
   actual branch, obstruction to uniformly coercive local quadratic
   principal metrics, and the explicit time-degenerate pullback cross
   metric.
4. `gradient_symmetrizer.md`, all sections and (G1)--(G24), and
   `relative_entropy.md`, all sections and (1)--(23): midpoint-gap
   mechanical symmetrization, weighted relative entropy, one-sided
   memory-gradient energy, their complete first-energy combination,
   fixed-mesh activation trace, and two successive collar integrations.
   The additional tight hypothesis is `|x-x_d|<=1/32` throughout the
   relevant prefix and histories.
5. `pointwise_continuation.md`, all sections and (1)--(13): the
   conditional first-energy consequences, static energy-to-pointwise
   nonimplication in its instantaneous-state class, sufficient actual
   constitutive conversion, covered-extrema memory comparison, and
   exact all-p stress/heat/weight identity. No coupled smoothing
   theorem is asserted or audited as proved.

Sections 1--3 of `flux_potential.md`, concerning its original flux
potential and mean-state defect, are **outside this review**. The
boundary-transfer note is outside the boundary agent's independent
review; the root coordinator's separate reviewed scope is recorded in
Section 11. No whole-note approval is implied by the hash inventory.

## 2. Dependency graph

The reviewed proofs have the following noncircular leaves:

- **Exact source:** continuity, momentum stress, both heaters,
  shared outward luminosity, volume centroids, and conductance
  definitions in the four unchanged physical files.
- **Explicit hypothesis:** actual prefix envelope, valid geometry,
  nonnegative memory, fixed nonnegative cutoff weights, and the stated
  monotonicity/support/halo requirements.
- **Previously established conditional input:** the state box and
  constitutive coefficient inventory in `heat_absorption.md`, the
  earlier heat-energy inequality (H37), and the old-stress identity
  and density-gradient bookkeeping in `viscous_energy.md`.
  The reviewer reconstructed the particular state derivatives,
  inverse bounds, and cutoff factors used by the new local-work
  proof; this is not a new whole-proof audit of all earlier notes.
- **Internal proofs:** finite shared-flux summation, exact product
  differences, Hardy-series estimate, Young's inequality, finite
  dimensional ODE flow/variational equations, and rank-one matrix
  algebra.

There is no external theorem, numerical trajectory, continuum limit,
or finite-grid extrapolation supporting an all-N claim. The provisional
envelope is a hypothesis, never a consequence of the desired compression
bound.

## 3. Obligation matrix

| Obligation | Verdict | Exact reviewed content |
| --- | --- | --- |
| Local quadratic-memory heat identity | Passed under envelope and cutoff scope | Flux (18)--(19) |
| Actual centroid/conductance bounds, including first face | Passed | Flux (20)--(21) |
| High/low-gradient conversion with both heat gates | Passed under envelope | Flux (22), (22a) |
| Negative-face heat sign and full source estimate | Passed under envelope | Flux (23)--(25) |
| Named interior mechanical-gradient absorption | Passed conditional reduction | Flux (26)--(27), with the explicit remaining terms |
| Heated reference and finite constitutive inverse | Passed under envelope | Local (L2)--(L13) |
| Exact shear and finite weighted Hardy bound | Passed | Local (L14)--(L16) |
| Local-work, density, nested and coarse collar bounds | Passed under envelope and cutoff scope | Local (L17)--(L23) |
| Uniform reaction chart and actual pullback identity | Passed under envelope on actual branch | Local (L24)--(L30) |
| Uniformly coercive local quadratic metric obstruction | Passed in stated restricted class | Local (L31)--(L34) |
| Degenerate pullback metric and its cross term | Passed | Local (L35)--(L37) |
| Midpoint gradient symmetrizer and small startup exponent | Passed under tight envelope | Gradient (G6)--(G22) |
| Relative entropy, heat collar, and one-sided memory-gradient closure | Passed under tight envelope and common cutoff scope | Relative (7)--(21) with the now-proved mechanical input |
| Integration of the new complete first energy from activation | Passed conditional result | Relative (22)--(23), gradient (G23)--(G24) |
| Sufficient constitutive pointwise conversion and exact all-p identity | Passed in stated conditional/internal-prefix scope | Pointwise (5)--(13) |
| Static first-cell nonimplication | Passed in instantaneous-state class only | Pointwise (4), not an actual-IVP counterexample |
| Actual common prefix interval and central pointwise bound | Not proved | Original (UC) remains open |

## 4. Decisive entropy-gradient checks

From `dm W_i H_i=L_(i-1)-L_i`, the heat part of the quadratic
memory derivative is exactly

\[
 \sum_i\phi_iK_i(L_{i-1}-L_i)
 =-\sum_e\bar\phi_eL_e(K_l-K_r)
       +\sum_e\Delta_e\phi\,L_e\bar K_e.
\]

Thus the collar sign in (18) follows specifically from outward
nonnegative flux and an outward-decreasing cutoff. The additional
weight derivative is `W_i'=rho_i h_i x_i`, giving exactly the last
term in (18). The source coefficient in (19) is generous:
`1.51*1600*11200=27059200`, with the remaining `K^2` work of
higher order on `s<=10^-3`.

For the face at the outer radius of its left cell,
`A_f*width_l<=3V_l` and `A_f*width_r<=V_r`. The left centroid
lies at least a quarter left-cell width from that face, while
`A_f*width_l>=V_l`. These prove both sides of (20), including
the cell abutting the origin. Hence
`C/a>=.025*(11s^2)^2>3s^4` and `sum a*d^2<=16M`.

For the threshold conversion, the small-temperature-drop class has

\[
 {2\cdot373\cdot1600\over(3/2)^{3/2}}
       <6.64\,10^5,
 \qquad (6.64\,10^5)^2<4.5\,10^{11}.
\]

On the high-gradient class, `J>=Aq/2` and the physical threshold gives
the stated fixed positive `beta_0`. Consequently
`Lq>=2.7 beta_0 s^4 a q^2`. The alternative (22a) is also valid:
`LJ>=3*(3/2)^3/4*beta_0*s^4*a*q^2`, whose coefficient exceeds
`2.4 beta_0`. The negative-gradient part is exactly `2s^2 F_-`.
No lower heat-conductance bound is asserted on closed faces.

If `q=K_l-K_r<0`, that face has zero outgoing luminosity. Both
neighboring contributions to `q_t` are nonnegative, proving (23)
without a neighboring-gradient sign assumption. The one-sided square
has zero derivative at `q=0`, so it has no missing switching term.
The geometry factor is nonincreasing on the compressing prefix.

The first inverse in (24) follows from `x=2+p/kappa` and
`918*38/64<546`. In the heater bound the derivative
`Q_z<=2800s` uses the inherited rectangular range
`2s<=z<=8s`, hence `rho-1<=exp(8s)-1`; it is not justified
by the coarser statement `rho<=1.01` alone. That inherited range is
indeed a consequence of the stated actual envelope. Young's inequality
then gives precisely the three coefficients in (25):

\[
 {400^2\over2\delta}s^2F_-,\qquad
 1.28\,10^6s^2F_-,\qquad
 {1.7\,10^6\over\sqrt\lambda}s^{1/2}(F_-+E_z).
\]

The old-stress product split (26) retains the favorable
`bar g*(Delta f)^2`. Its remaining `K` gradient cost has exactly
the `s^4 D(K)` power covered by (22) or (22a). This establishes
the named conditional gradient absorption, not the complete startup
estimate.

## 5. Decisive local-work and collar checks

The reference ODE contains both heaters and has no shear or heat
flux. Direct differentiation gives `S_d'=A_d`, `psi_d'=B_d`;
therefore (L10) subtracts the full homogeneous reaction before any
absolute-value estimate. The physical actual shear is retained.

The finite inverse (L6) follows by subtracting
`S=nu*x-2kappa+P` on a line segment in the rectangular state box,
then inverting `psi=K W^(3/2)`. In particular its density and memory
coefficients stay finite with the displayed powers. The extra density
coefficient in the last line is below `5e-9` after the stated
factorization, so rounding 86 to 87 is valid.

The derivative table in (L11)--(L13) was reconstructed from the exact
polynomial ramp and rational `g`. In particular the local memory box
gives `g<=.00016`, hence `Q/h<25`, which is essential to the sharper
`Q_z<=1250s` used here. The displayed second-derivative formula
(L12) and all listed bounds are consistent. Substitution gives the
unrounded coefficients reported below (L13); their rounded versions
are upper bounds throughout `s<=10^-3`.

The exact radial flux identity gives
`T_i=(2/3)(r_(i-1)/r_i)^3(v_i-<v>_(i-1))^2`, with `T_1=0`.
The weighted finite Hardy proof uses
`sum_(n>=j)n^(-3/2)<=3j^(-1/2)` and cutoff monotonicity;
its constant is `6*1.01^3<7`. Thus the shear bound 11 is valid
without any compression-gradient or adjacent-width estimate.

The Young splittings in (L17)--(L20) and their constants were checked.
For example the unrounded shear density coefficient is `624442500`,
and the stress coefficient is `788906.25`, both below the displayed
roundings. The largest combined local-work coefficient after factoring
`1/s` is below `1.213e7`, so (L1)'s `2e7` is safe. The density
energy retains the exact moving-volume term and yields (L20).

For the nested cutoff, `9*146*612=804168`, and the heat term is
`1.898e8*s^4`, bounded by `190s^2` on this interval. This proves
(L21) with a common halo; no uncontrolled outside endpoint is included.
The coarse bootstrap energy in (L22) is below `4.3e5*s^2`, giving
the stated `O(s^4)` collar work. Adding (L1), (L20), and the inherited
(H37) gives exactly the coefficients and dissipation signs in (L23).
Neither nested nor coarse collar work launches the singular Gronwall
argument; the note explicitly preserves that limitation.

## 6. Reaction-flow and principal-metric checks

The prefix weights in (L24) are exactly the physical volumes up to the
common factor `dm`. Differentiating their normalized averages gives
(L26), including the sign in `delta beta`. The shifted Hardy average
has fixed-mass `l2` norm below 2.6. Consequently

\[
 13+{128\over3}\,4
    +{32\over3}{8\over.98}\,2.6<411,
 \qquad 6+{32\over3}(1+2.6)<45,
\]

as needed for (L27). The auxiliary box keeps the pole of `g` outside
the chart. Its bounds on `g`, `g'`, `h`, and `h'` give the three Q
derivative coefficients 7, .027, and 16. The majorant matrix has
Frobenius norm below 500; the maximum-norm majorant is below 300.
The flow displacements .00927, .083, and .000108 fit strictly inside
both forward and backward box margins. Thus the uniform chart and
inverse-Jacobian estimates (L29) follow from ordinary finite-dimensional
variational equations, with no N-dependent constant.

The auxiliary extension is used only for coordinates. At every actual
state in the assumed branch it agrees with the physical reaction,
including the entire radial shear. Differentiating the autonomous flow
identity therefore cancels the reaction exactly in (L30). This is an
actual transformed equation conditional on the envelope, not an altered
physical evolution.

At the homogeneous reference both factors of the gated heat flux vanish,
so its first variation is zero at each fixed finite mesh. The shear
derivative is also zero. The internal mechanical principal matrix is
therefore exactly the rank-one matrix (L31), and the homogeneous flow
Jacobian is identical and local at every cell. This justifies the
similarity formula (L32); it would not justify ignoring the nonlocal
commutator away from homogeneity.

For a positive metric M, semidefiniteness of the symmetric rank-one
product forces `M e_x=lambda grad S`, `lambda>0`; otherwise its
restriction to the span of those two vectors has negative determinant.
This gives (L33). The exact activation expansion has

\[
 \nu_d={9a^2\over4}s^2+O(s^3),\qquad
 S_{\rho,d}={9\over2}a(a-2)s+O(s^2),\quad a=C_a>2.
\]

Thus `S_rho/nu=b/s+O(1)`, with `b=2(a-2)/a>0`, contradicting
uniform upper and lower metric bounds. An N-independent zero-order
error cannot absorb a negative principal direction at arbitrary graph
frequency. Uniformly bounded reaction charts preserve this obstruction
by congruence. The conclusion is restricted to the stated local
quadratic principal-energy class; it is not a no-go result for weighted,
gradient, nonlocal, or frequency-dependent estimates.

Finally the three-square form (L35) has largest eigenvalue of order one
and smallest eigenvalue of order `s^2`. The leading two-variable
similarity in (L36) and pullback cross energy (L37) agree. With
`u=(-s,1)` and `v=(b/s,1+b)`, its matrix obeys
`M u=gamma*s^2*v`; its determinant is `gamma*s^2`. In the pure
compression direction its logarithmic derivative is `2/s`. Thus the
chart removes the reaction from the equation but does not remove the
time-degenerate metric derivative. The note's stated remaining work
is mathematically necessary for this proposed chart-only closure.

## 7. Remaining implication and strongest safe statement

The reviewed new lemmas hold on any actual interval satisfying their
prefix and halo assumptions, with constants uniform in N. They supply
new nonlinear gradient control, explicit reference-subtracted local
work, actual coarse collar control, and a uniformly regular reaction
coordinate map. They also identify the restricted metric obstruction.

The subsequent notes audited in Sections 9--10 resolve the singular-startup
integration for a different combined first energy, under the tighter
actual prefix envelope. They do not propagate that envelope or provide
actual pointwise control reaching the central quarter. The scalar
adverse-boundary transfer is reviewed separately. Zero activation energy
together with the earlier large-coefficient `E'<=C E/s+...` remained
insufficient; the new proof instead checks a smaller exponent and its
activation trace explicitly. This audit gives no unconditional
entropy-floor or (UC) status upgrade.

## 8. Pinned revisions and verification

The final proof hashes were rechecked after the authors finalized their
notes. Paths below are relative to `stable_stress_search/`:

| Reviewed input | SHA-256 |
| --- | --- |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/local_work.md` | `513035e97cabeebda25db702bad64969ba9e0fac3ddc87fd1b0e367edb925a5f` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/flux_potential.md` | `858dae640349b4efdf88cf4d9d98e524115fe9ed5505e56b88cf5961db559e78` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/gradient_symmetrizer.md` | `1cd907f4d47552d794282cce7a42a3382fc81c73c9c6ff314cb962ffca39abb6` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/relative_entropy.md` | `92fb61a920ef28e4e08324dbbcf3495cbf708dcc5f750de866fb1b407a8f56b6` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/boundary_transfer.md` (root review scope only) | `167d6c6fb6362e163c6473e99cbef986c948e124feac10c98ad7131036dfa6f3` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/pointwise_continuation.md` | `a2bc945dc7742faa803b0d7b858096a3424f5945ccef1dc02253c9a850701ea9` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/heat_absorption.md` | `b98843cec40271ef4a16bdb6c15baf50a43c203d6367fbf3ae72a4d299b74379` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/viscous_energy.md` | `874881bdaeb046fc607d500fc01d2402e8d4db1264c302e647ac137a39a920a1` |
| `entropy_transport/floor_theorem/startup_energy_route.md` | `06630aecae84c9b618e84c1ddded3f2025f7a89f7dca634bbbb05f50d0e2380b` |

Verification consists of raw-source reconstruction, exact algebra and
coefficient arithmetic, final SHA-256 checks, and audit-file delimiter
and whitespace checks. Focused mathematical proofreading covered this
audit only. No new physical integration, grid, source modification, or
external citation was used. Proof correctness rests on the displayed
analytic arguments and their explicit hypotheses, not agreement
between author and reviewer or a finite set of arithmetic checks.

## 9. Independent review of the midpoint gradient symmetrizer

Reviewer: boundary-transfer agent, separate from the author. Reviewed
final revision: the hash of `gradient_symmetrizer.md` in Section 8.
Primary verdict: **conditional on the tight actual prefix envelope**.
No correctness error was found in (G1)--(G24).

The exact old-viscosity primitive satisfies `F_z=kappa`. For
`m=(z_l+z_r)/2`, `d=z_r-z_l`, the midpoint gap
`U=2(F_l+F_r-2F(m))` has `U_d=Delta kappa` and
`U_m=2(kappa_l+kappa_r-2kappa(m))`. This yields the exact time
derivative (G8), so the mechanical cancellation uses the nonlinear
finite difference rather than a frozen coefficient.

The positive triangular-kernel formula was reconstructed. The exact
ramp bound `|kappa_zzz|<=40` yields
`|U-(9/4)m d^2|<=(35/3)m^2d^2` and
`|U_m-(9/4)d^2|<=20m d^2`, hence (G9). On the tight prefix
`m>=17s/4`. The resulting lower coercivity is exactly
`G>=221 D_eta(z)/8`; the constants 53 and `361/17` in (G10)
also follow from the stated finite-difference bounds.

The reference identity `s*x_d-z_d<=35s^2/2` and
`|e|<=delta*s` give
`bar x/m-1/s<=8delta/(17s)+70/17`. Combining this with (G9)
and the reference coefficient derivative proves (G12), including its
`delta/(2s)` growth coefficient. This is the leading signed scaling
cancellation absent from the earlier absolute stress-source bound.

In (G13)--(G15), the `c*Delta kappa*Delta v/s` pairing cancels
exactly between velocity and midpoint energy. Each of the remaining
four products spends precisely `mathscr D_v/8`. The first remainder
coefficient is at most `722/(17c)<14`; the other three rounded
coefficients `2.3e13`, `6.1e7`, and `3.8e9` are upper bounds.
The pressure derivative `|P_z|<=82000s^4` uses the inherited exact
range `z<=8s`. For example
`rho-1<=8s/(1-8s)` gives `h_z<49s`, which proves it together
with the other state bounds. Using only the separate looser
`h_z<=50s` table would not by itself prove this particular rounding.
This is a source-bound precision, not a missing hypothesis.

The full local reaction estimate (G16) keeps radial shear and uses
the already reviewed finite Hardy estimate. The strongly weighted
zeroth-order density energy satisfies exactly (G17). Its positive
velocity loss is `lambda E_v/s`, absorbed by `-E_v/s` with
`lambda=1/16`; it is not treated as a regular remainder.

The three collar estimates (G20) were reconstructed from (G19).
The respective unrounded outer constants are `1429632`, `31694848`,
and `4417668000000`, within the stated bounds. The density collar
spends `G/(32s)`; no favorable sign is asserted for that term.
Their combination with all interior estimates gives (G22): seven
sixteenths of velocity dissipation remain, and

\[
 \delta/2+14\delta^2+1/32<1/16
       \quad\text{for }\delta\le1/32.
\]

The regular coefficients fit below 250, and the complete memory cost
fits below `4e9*s*D_eta(K)`. Thus (G22) supplies the explicit
mechanical input (20) in the relative-entropy note, with a startup
exponent at most `1/16`. The stronger fixed-N trace (G23) is consistent
with the exact law; the weaker trace used below already suffices.

## 10. Independent review of the combined relative first energy

Reviewer: boundary-transfer agent, separate from the author. Reviewed
final revision: the hash of `relative_entropy.md` in Section 8.
Primary verdict: **conditional on the tight actual prefix envelope,
with the mechanical input supplied by (G22)**. No correctness error
was found in (1)--(23).

The relative memory square has exactly the heat identity (7), including
the reference derivative, `W_t` term, and the sign-indefinite collar
`Delta phi*L*bar k`. The note correctly estimates that collar instead
of using the favorable absolute-memory sign. With
`G_K=s^-6 E_K` and `N=lambda*sum(V phi e^2)/(2s^3)`, both
`Q_x*k*v` and `Q_z*k*e` scale as
`s^-1/2*sqrt(G_K E_v)` and
`s^-1/2*sqrt(G_K N)`, respectively. The `Q_K` and weight work are
`O(s^2)G_K`. Thus their positive growth coefficients are integrable;
no positive `C/s` was hidden there.

The flux comparison `LJ<=4Lq+2.4e16*s^14*a*(Delta z)^2` follows
by the two exact finite-edge cases in (11). Together with
`L^2/a<=16200s^4 LJ`, the cutoff estimate spends half the
relative heat dissipation and leaves only
`(C_B/8)s^8 D_eta(z)+C_chi s^4` after the weight `s^-6`.
This verifies all collar powers in (15), including closed faces.

The threshold `q/d=s^3` is an instantaneous algebraic split; it
requires no threshold derivative. Dividing the prior threshold bound
by `s^3` gives exactly (16): `2s F_0`, the heat term
`10*s^-6 D_H/(27 beta_*)`, `16M s^7`, and
`4.5e11*s^11 D_eta(z)`. The negative-face heat sign makes
`F_0'|heat<=0`. The three positive source coefficients in (17)
were rederived, including `4.5e6*s^3/epsilon` and
`1.28e6*s^2`. No negative-gradient collar term is missing.

The complete velocity collar uses the exact stress split (18).
Young weights `bar nu/s`, `1/s` for the density energy, and `s`
for the memory gradient give (19) with outer forcing
`C*s^2 E_v,out`. All three gradient shares are explicit.

Now use the independently reviewed (G22) in (20), choose a fixed
multiplier for (15), and a small velocity share in (17). This gives
the complete inequality (21) for
`E=E_v+G_midpoint+N+A_0 G_K+F_0`, with startup exponent no
larger than `1/16<1` and only integrable additional growth. No heat
mean-state defect from the earlier flux-potential attempt is used.

The activation launch is valid without a uniform fixed-mesh Taylor
constant. On each fixed mesh, bounded local right-hand side gives
`v=O_N(s)`, `e=O_N(s^2)`. The heater bound and exact two gated
flux factors give `L=H=O_N(s^10)`, and the relative source gives
`k=O_N(s^4)`. Hence the full energy is `O_N(s)`, so
`s^-p E(s)->0` separately for every fixed N for `p<=1/16`.
The integrating-factor inequality then has uniform coefficients and
zero initial trace for each mesh; taking its scalar bound does not
retain an N-dependent initial constant.

With three fixed nested cutoffs and all required endpoint halos, the
coarse amplitude input bounds the outer velocity energy by `C/s`.
Its first forcing is `O(s)`, giving `E_outer<=C s^2`. The next
collar is bounded by this energy, giving forcing `O(s^4)` and
`E_inner<=C s^5`. This proves (23) and
`sum V phi_inner v^2<=C s^6` conditionally, with constants
independent of N. The tight envelope itself and coupled pointwise
recovery are still open. These conditional energy estimates must not
be reported as a common bootstrap interval or as (UC).

## 11. Root coordinator's independent boundary-note review

Reviewer: root coordinator, separate from the boundary-note author.
Reviewed revision: `boundary_transfer.md` hash in Section 8. The
reviewer's stated independently reconstructed scope is (BT1)--(BT6)
for the exact transfer/capacity sign and (BT10)--(BT22) for the actual
positive estimates, conditional on the earlier density/energy geometry
lemma and their explicit one-sided prefix cap.

The root review reconstructed the lower flux bound from the prefix
compression cap, the upper flux bound from the reserved tail mass
`>=3M/32` and global kinetic bound `<4`, and the estimate of total
negative cell-volume derivative by `UQ_*`. Their combination gives
the stated `Lambda`, summed time variation, and fixed-cut pigeonhole
factor 64. The floor/ceiling and adjacent-capacity bounds, including
`N=32`, passed that review. The exact Duhamel transfer (BT3) and
capacity-energy sign (BT6) also passed.

The coordinator did **not** independently certify the finite-block
probability step (BT9) in the coarse coefficient-class counterexample.
That subsection remains author self-review only; this audit does not
give it an independent pass. The actual positive flux, variation, and
fixed-cut estimates do not depend on that counterexample. Neither the
positive reviewed estimates nor the scoped counterexample establishes
the actual energy-constrained pointwise boundary kernel or (UC).

## 12. Independent audit of the bounded pointwise continuation

Reviewer: boundary-transfer agent, separate from the author. Reviewed
final revision: `pointwise_continuation.md` hash in Section 8. Primary
verdict: **conditional on the stated actual prefix envelope** for the
energy consequences and sufficient dynamic conversion; **proved in
its stated instantaneous-state class** for the static nonimplication.
No actual coupled smoothing or common-time bootstrap is proved.

The powers in (2)--(3) follow from the independently reviewed inner
first energy: the velocity square is `O(s^6)`, the density square
`O(s^8)`, and relative memory square `O(s^11)`. Dividing the
constitutive difference by `s^2` consequently gives its weighted
`l2` norm `O(s^3)`. The stated scalar smoothing exponent is explicitly
a scaling heuristic; no such theorem is applied to the actual system.

The static example (4) was reconstructed from the exact volume divergence.
Given its cell compressions, the nodal velocity
`u_i=-r_i*<x>_i/3` realizes them on its ordered homogeneous geometry.
All density and memory error energies vanish, while its first-cell
velocity energy is `M*epsilon^2/(2 rho_d N s)` and its velocity
supremum is `epsilon`. Arbitrarily large N at each fixed positive s
therefore defeats a static embedding from the displayed energy bound
to pointwise amplitude improvement. The example does not have the
specified activation history, and the note correctly draws no
counterexample to the actual IVP or to dynamic smoothing from it.

For (5), split the state path first in x at fixed actual `(z_i,K_i)`,
then in density at fixed `(x_d,K_i)`, then in memory at fixed
`(x_d,z_d)`. This gives exactly
`f=nu_i*v+A_i*e+B_i*k`. On every such path,
`S_z=kappa_z*((1+g)x_d-2)+P_z` is positive and bounded above and
below by positive constants times s; `nu_i` is comparable to `s^2`,
and `S_K=O(s^2)`. Thus all divided-difference bounds in (5) hold
uniformly in N, including zero state differences interpreted by their
derivatives.

Writing `a_i=A_i/nu_i`, the resulting scalar density equation has
`a_*/s<=a_i<=a^*/s` and forcing bounded by
`C(s^theta+s^3)` under (7). Its integrating factor from time tau
to s is at most `(tau/s)^(a_*)`. The zero-error activation trace
therefore gives
`|e(s)|<=C(s^(theta+1)+s^4)`. Substitution in the same exact
constitutive identity gives
`|v(s)|<=C(s^theta+s^3)`. This proves (6)--(7) as a sufficient
actual conversion with uniform constants, rather than assuming
pointwise density or compression regularity.

The memory-extremum discussion (8) is also correct in its stated scope.
At a largest K its incoming face is closed and its outgoing luminosity
is nonnegative; at a smallest K its outgoing face is closed and its
incoming luminosity is nonnegative. The reference memory is spatially
constant, so these are the extrema of `K-K_d`. The lower prefix
extremum does require the exterior collar or controlled incoming
comparison value, exactly as the note says. No such comparison is
available for the heat divergence at a stress extremum.

For the all-p identity, direct stress differentiation gives (9), on
the interior prefix and cutoff support where a spatially constant
reference stress has zero graph Laplacian. The temperature derivative
(10) includes its exact density-weight contribution. Differentiating
`V|f|^p/(p nu)` gives the mechanical graph pairing in (12). Its
full heat coefficient after inserting
`H=(L_prev-L)/(dm W)` is exactly

\[
 {S_K\over\rho\nu W}J_p(f)
       -{\nu_K\over p\rho\nu^2W}|f|^p
 =M_p.
\]

Shared-flux summation therefore gives
`+sum L*Delta(phi M_p)` with the sign displayed in (12).
The remaining time-weight terms are exactly the last line of (12)
and are nonpositive on the active compressing branch. All-p
differentiation is valid also at `f=0` for `p>=2`. The exact finite
product identity for `Delta M_p` is precisely (13); neither a
coefficient difference nor a heat-dependent weight term was omitted.

These checks establish a correctly formulated remaining coupled
level-set/all-p obligation. They do not estimate its level-dependent
density terms or mixed stress/temperature power weights. The note's
verdict that no mesh-uniform coupled smoothing estimate has yet been
proved is consistent with the audited derivation. Actual prefix
coverage, pointwise recovery at the origin, and (UC) remain open.
