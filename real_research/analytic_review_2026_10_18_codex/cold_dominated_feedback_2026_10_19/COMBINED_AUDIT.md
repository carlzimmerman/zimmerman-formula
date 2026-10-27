# Independent dependency and scope audit of the combined cold-halo theorem

19 October 2026. Reviewer `/root/audit_combined_scope`, a fresh isolated
subagent. Analytic reasoning and text/hash operations only. This report is
the only file written by this reviewer.

## Normalized claim and primary verdict

**Primary verdict: proved as written.** This is a dependency, quantifier and
scope verdict for the combined theorem at SHA-256
`f40bf9707243187989677e0c19a92c8878ba648365ce5b737c5a37598927ad6a`.
No additional missing implication was found when the exact proved source
lemmas are composed. The earlier exact-equilibrium and coercive-energy
theorems are inherited named mathematical inputs; this review does not
claim a new independent proof of their entire antecedent theory. That
inheritance does not leave (CF), a reduced inverse, or the desired work
estimate as an unresolved hypothesis of the combined result.

The normalized quantifiers are: fix the original spherical two-species
deep-cubic model and smooth hollow profile; fix `f=1/64`; choose any
sufficiently large positive scale `D` outside the described locally finite
exceptional set; then choose one sufficiently small **fixed positive**
warmth `delta` for the exact inverse and geometry. The exact law-annulus
cold mass satisfies `M/M_b=D x>=2D`. Starting from one exact smooth DF
provided by that inverse, form the product of the two weighted smooth
low-tube exact-density nullspaces in `GENERIC_FORCE_CANCELLATION.md`,
Section 2. In a sufficiently small open parameter neighborhood `U`, there
is an open dense subset `U_good` such that every fixed equilibrium in it
has the four conclusions: finitely many actual neutral-mode exceptions;
an ordinary boundary inverse elsewhere and a bounded Hölder remainder
after their finite-rank simple poles; bounded modal work on the complete
closed occupied action sets; and time-uniform full linear work and label
bounds for every smooth compact radial fixed-`L` canonical generator.

The density, mass, support, potentials, orbital maps, and frequency
geometry are fixed exactly in this genericity statement. The DF itself
varies. The topology is the specified topology on this constructed
exact-density DF family, not a topology on all possible profiles. Neither
the independently specified starting DF nor a particular numerical
parameter choice is certified. Constants can depend on `D`, `delta`, and
the selected DF. No nonlinear confinement or nonlinear actual-path work
bound is included.

## Dependency graph

1. The exact finite profile and exact smooth DF inverse give an actual
   positive-warmth two-species equilibrium with the original individual
   densities and potentials. The existing accessible-energy theorem gives
   coercive `Q`, its selfadjoint energy generator, and the compact
   energy-to-field map. These are inherited internal source inputs.
2. `GEOMETRY_AND_CAP.md` gives the arbitrarily cold-mass-dominated parameter
   family, no full action-frequency critical point on its narrow closed
   warm tube, finitely many simple circular extrema, the occupied-side cap
   resonance graphs, and physical endpoint estimates.
3. `BOUNDARY_PAIRING.md` gives the complete boundary source map, actual
   reciprocity and optical form, and compact field pencil.
4. `REGULAR_INVERSE.md` reconstructs every boundary kernel as an actual
   energy mode, uniformly locally in frequency; orthogonality and compact
   field extraction give locally finite real exceptions and the ordinary
   inverse off them. `HIGH_FREQUENCY_INVERSE.md` gives global decay and a
   high-frequency Neumann inverse, making the exceptional set finite.
5. `THRESHOLD_MODES.md`, with the concrete cap and endpoint inputs from
   step 2, gives the `C^(1,1)` actual-mode bootstrap. It reduces the only
   remaining fundamental circular obstruction to the mode force trace (CF).
6. `GENERIC_FORCE_CANCELLATION.md` gives the continuous exact-density
   nullspace projection and admissible open DF family, scalar
   transversality, and generic (CF) on a finite intersection of locally
   constant-nullity loci. The fresh scalar and variation audits verify
   the exact raw revision used here.
7. The hypotheses of `REDUCED_INVERSE.md` are now satisfied for every
   member of `U_good`. Its two divisible off-diagonal blocks and
   `delta Q_Gram/nu+delta^2 C` kernel block give the bounded Hölder
   pole-subtracted inverse. Steps 2 and 5--6 supply every closed-set
   modal-work quotient.
8. `CONDITIONAL_WORK.md` then applies with its extra condition (CF)
   discharged. It proves the smooth source transform, the scalar modal
   left-coupling difference quotient, the residue/spectral-projection
   identity, and the summable receiving Dini estimate. The finite modal
   sum and endpoint label identity give the full linear conclusions.

There is no directed cycle. Generic (CF) uses the actual kernel/mode
correspondence and mode bootstrap, but neither the reduced inverse nor
the future work estimate. The reduced inverse uses (CF), but no future
work bound. The work proof obtains its extra residue-coupled source
regularity directly, rather than assuming whole-field differentiability
or the desired receiving-work bound.

## Obligation matrix

| Obligation | Status | Decisive check |
| --- | --- | --- |
| Actual cold-dominated member and exact model | passed | Fixed `f=1/64`, original profile and kernels, `M/M_b=D x`; large `D` satisfies the exact deep/core restrictions. |
| Generic scale and strictly positive fixed warmth | passed | The exceptional scales are locally finite; warmth is chosen after the fixed scale and stays positive. |
| Exact individual-density nullspace | passed | `A_den B_den=I` and `Pi_null=I-B_den A_den`; the density change is exactly zero for the whole parameter, not only to first order. |
| Open actual DF family | passed | The strict relative low-tube height and energy-derivative margins survive a small weighted seminorm neighborhood. |
| Same support, potential, orbit and frequency geometry | passed | The upper tube is unchanged, positivity retains the lower tube, and both species' exact density profiles are fixed. |
| Energy and generator hypotheses throughout `U` | passed using inherited energy theorem | Relative `w` control preserves the coercive norm and the same accessible completion; the invariant distribution and fixed shell map retain the energy formulation. |
| Flat cap/end and square-root-weight bounds after DF perturbation | passed | The cap collar is unchanged; the low-tube relative lower bound and quantitative exponential endpoint weight control every finite physical derivative, including those of `sqrt(w)`. |
| Boundary-pencil common space and continuity | passed | Fixed `Y=C^gamma(I)^2`, fixed orbit charts and shell map; finite weighted source seminorms control the affine susceptibility variation. |
| Actual finite exceptional set and inverse off it | passed | Uniform kernel reconstruction plus compactness gives local finiteness; high-frequency decay excludes all large-frequency exceptions. |
| Generic (CF) for every kernel vector | passed | Scalar transversality contradicts the zero first Schur pairing on each locally constant-nullity locus; finite fundamental threshold list. |
| Negative frequencies and coincident thresholds | passed | Corrected reduced inverse uses `|nu|=kappa`; conjugation and the finite frequency set cover both signs and coincidences. |
| Bounded Hölder remainder after actual poles | passed | Every reduced-inverse hypothesis is supplied on `U_good`; no ordinary inverse at the poles is asserted. |
| Full closed receiver set | passed | Interior division, occupied-side eccentric cap graphs, endpoint flatness, higher-harmonic quadratic jets and fundamental (CF) cover every receiving boundary type. |
| Smooth-source work, not energy-only work | passed | Actual source transform and left-coupling quotient provide Hölder regularity plus amplitude decay; the Dini/harmonic sum is summable uniformly in the receiver. |
| One finite smooth norm of the generator | passed | Only finitely many orbital smooth-source seminorms and the initial energy norm occur, each controlled on the fixed compact physical neighborhood. |
| Certification of the original fixed DF | out of scope, explicitly excluded | Density of `U_good` permits arbitrarily close good choices; it does not assert membership of the original point. |
| Small cold mass or small susceptibility | out of scope, not assumed | Frequency smallness at large `|z|` is proved for each fixed actual halo. |
| Nonlinear confinement, actual perturbed paths or label gradients | out of scope, explicitly excluded | All receiving paths and fields belong to the linear equilibrium-orbit problem. |

## Decisive persistence checks

### Exact self-consistency and geometry

At fixed potentials the map from `H` to shell density per `dr` is linear.
For `V in N_den`, `A_den(H_*+V)=A_den H_*` exactly. Applying this separately
to both populations fixes their cumulative masses. This fixes the original
coupled potentials, including the tethered nonlinear background force, and
also fixes the actual linear shell kernel `P_tt`, which depends on the same
background `M_t`. It fixes `L_c`, the action/angle maps, `Omega`, the energy
cap, and all circular and cap threshold locations. Thus no geometric
hypothesis must be reproved as a moving-frequency assertion in DF parameter
space.

The species DFs remain functions of their actual fixed invariants `(E,L)`
and so remain stationary. On `0<=t<=delta^2/4`, the baseline exact DF has
strict positive margins relative to `u(y)`. Smallness of the first weighted
source seminorm controls both height and `t` derivative. Above that region
the original DF is unchanged. Hence the complete occupied warm tube and
positive physical susceptibility persist, including the physical circular
edge `t=0`; no incorrect lower-edge cutoff is introduced.

The exact-inverse proof uses the specific exponential flatness of `u`,
not arbitrary flatness. Every physical derivative of an admissible smooth
variation costs only finite inverse powers of `h` and endpoint distance,
and that exponential weight absorbs them. The source topology supplies
the same bounds for every derivative order. The smooth zero extensions
required by boundary pairing and high-frequency inversion therefore
persist throughout `U`.

### Coercive energy, accessibility and the square-root susceptibility

On the low tube `|delta w|<=epsilon w_*`, with arbitrarily small fixed
`epsilon`; outside it the susceptibility is unchanged. Thus the old and
new weighted kinetic norms are equivalent on the same function space.
The orbit-average-zero accessible subspace is fixed because the orbits
and support are fixed, so its completion does not change under these
equivalent norms. The field part of `Q` is fixed. If
`Q_*=A_*+V_field>=c_* A_*`, then
`Q_new>=Q_*-C epsilon A_*>=c A_new` after shrinking `U`.
This explicitly supplies the coercivity needed by kernel reconstruction,
orthogonality, off-axis injectivity and the initial field estimate at each
parameter. It does not infer positivity of the indefinite shell matrix.

The stronger square-root regularity used by the reduced inverse also
persists. Near the top cap the DF and its exponential-flat baseline are
unchanged. In the low tube the relative positive lower bound allows
derivatives of `sqrt(w)` to be bounded using the weighted derivative
estimates; at angular-momentum ends its exponential square-root weight
still dominates every finite inverse-power coordinate factor. Thus the
bounded first two derivatives and flat extension required there do not
hold only for the original Fourier reconstruction. Every admissible DF
in the stated neighborhood has them.

The inherited energy theorem is the actual smooth-halo result in
`CLASSICAL_RADIAL_STABILITY.md` and the full-feedback spectral formulation.
The fixed-density and invariant-DF hypotheses match it. This focused audit
checked the persistence just described and read those source statements;
it did not rerun their whole historical proof chain.

### Why the genericity result discharges the downstream condition

The genericity parameter is precisely the product of the two real
`N_den` spaces. The positive fundamental circular threshold list is finite
and fixed. At each threshold, compact Fredholmness and norm-continuity give
finite upper-semicontinuous integer nullity. Every nonempty open parameter
set contains a smaller open set of constant minimal nullity. The finite
intersection of the locally constant loci is therefore open dense; no
infinite Baire intersection is hidden.

At such a parameter the finite square Schur matrix has its full dimension
as nullity along every small admissible parameter line, so it vanishes
identically and every first kernel/cokernel quadratic entry is zero. The
proved scalar transversality supplies a nonzero entry if any actual mode
has a bad fundamental force trace. This contradiction applies to every
kernel vector, including multidimensional kernels, simultaneous circles
and species-specific choices. Its conclusion is exactly the all-fields
(CF) hypothesis in the corrected reduced-inverse theorem, not merely one
chosen basis-vector condition or absence of modes. No full-rank
perturbation matrix is required.

The raw scalar argument has been separately independently audited at its
current exact revision. The density-variation audit deliberately leaves
that scalar leaf as an input; the scalar audit proves that same leaf.
Those reports therefore compose, rather than leaving a further
transversality assumption in the combined theorem.

### Closed-set work and smooth-norm scope

The geometry selected here has no eccentric full-frequency critical
point, so it does not inherit unproved eccentric Morse logarithmic
subtractions from a broader model. At eccentric cap contacts the level
enters the positive-weight interior, which gives actual trace division;
flatness alone is not used to force the trace. At physical endpoints,
accessible zero mass and integrated susceptibility bounds give
arbitrary-order flat force decay, absorbing the nonzero endpoint
frequency derivative. The concrete cap and endpoint arguments also give
the quantitative bounds needed by the mode bootstrap, avoiding the
abstract unspecified-boundary qualification in `GEOMETRY_MODES_AUDIT.md`.
The circular bootstrap and generic (CF) control the remaining circular
fundamental thresholds; higher harmonics are already quadratic.

In the work proof, the reduced inverse is applied only after the modal
left-coupling difference quotient is proved. The residue is identified
with the actual `Q`-orthogonal spectral projection. The pole-subtracted
derivative transform is consequently Hölder with `O(1/|z|)` amplitude.
The receiving Dini minimum gains the summable sequence
`|k|^(-1-gamma) log(2+|k|)`. This does not require an energy-space
boundary resolvent or an energy-norm-only work estimate. The work bound
is uniform on the closed receiver set, while its constant uses finitely
many smooth seminorms of the source datum. For a fixed halo, smooth
physical-to-orbit pullback and field extraction bound those seminorms by
one finite smooth norm of `g_0` on the occupied physical neighborhood;
the initial energy norm is bounded there as well since `W_*<infinity`.
The boundary label is defined by its transport equation and endpoint
identity, without division by a zero susceptibility.

## Remaining gap, strongest safe statement and cheapest next check

**Exact remaining gap in this synthesis: none found.** The strongest safe
statement is the combined theorem's generic exact-DF, fixed-density,
fixed-positive-warmth full linear closed-set work result, with its stated
halo-dependent smooth-data norm. It is not necessary to retain (CF) or
the reduced inverse as an unresolved condition after composing these
proved lemmas at the authenticated revisions.

Certifying a separately chosen original DF would be a different problem:
the theorem expressly provides no such membership test or parameter
certificate. Nonlinear confinement and actual-path work likewise remain
separate problems. Neither omission restricts the result actually stated.
The cheapest publication/provenance check is to preserve these exact
source pins and accurately carry the generic DF quantifier into any
later manuscript statement; no numerical check can replace or strengthen
the analytic genericity implication audited here.

## Exact revisions, source checks and review provenance

Repository source prefix:
`/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/analytic_review_2026_10_18_codex/`.

Raw artifacts under `cold_dominated_feedback_2026_10_19/` actually read:

| Artifact | SHA-256 |
| --- | --- |
| `COMBINED_THEOREM.md` | `f40bf9707243187989677e0c19a92c8878ba648365ce5b737c5a37598927ad6a` |
| `GENERIC_FORCE_CANCELLATION.md` | `fbe1782f5e165001e0979eca662da2d0ba7f4171bec74959e09e25c27e539112` |
| `GEOMETRY_AND_CAP.md` | `c40c5f63e533fe19e41b996e292d21892160bf2b4aa31ffb499313b64f54fc0d` |
| `BOUNDARY_PAIRING.md` | `5b5f2f73d54b034fa014b6efbeeb9acb5cadd9a30f2f40340745569610bba23d` |
| `REGULAR_INVERSE.md` | `4830712683b98b46a53b796b4bde109c618a4fd26fa910cd47176ebe9f3ddf80` |
| `HIGH_FREQUENCY_INVERSE.md` | `6111b7f0f2e2ea0ef1ea80b81c1a1227374bedc270614c50698db830ade8d49c` |
| `THRESHOLD_MODES.md` | `40304ae8d1c0495cdd7482202aa9dcdfa494f12287754b7e648dd2adf26a77b5` |
| `REDUCED_INVERSE.md` | `ebc588cbd3fef36295dc355542f5b5344327c6ed1d76af12e777ee36786e93d1` |
| `CONDITIONAL_WORK.md` | `b20cefd311eee9e356e1437f5ab6cbe0bb00db19027ebcede0ff374e2bdfab9f` |

The exact smooth inverse `smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md`
was read directly, at the source pin
`490b137269ea5c918dae517085974752a3e1bc3d9df4f3e88b99eeccde41a55b`.
The actual classical energy source and the full-feedback spectral source
were read for their hypotheses and their use under DF changes, and their
hashes were authenticated as
`ff33f52fb33a7166a10ae5ba0c99b873ae581916286c6eefca2f70f86b880cb4`
and `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`,
respectively.

Separate independent reports read: `INVERSE_AUDIT.md`,
`HIGH_FREQUENCY_AUDIT.md`, `GEOMETRY_MODES_AUDIT.md`,
`REDUCED_INVERSE_AUDIT.md`, `WORK_AUDIT.md`,
`FORCE_CANCELLATION_AUDIT.md`, and `DENSITY_VARIATIONS_AUDIT.md`.
The latter two report hashes were authenticated as
`dc83d1a7246eefc4e2eddba19a7036baf6ec9bf058533299f930373cf5cf7032`
and `f55976e4b06da43944474f635eedf7a3f5c6759da85c49e4c038e5a510ace62d`.
The reduced-inverse report verifies the final `|nu|` correction, and the
work report authenticates raw work hash `b20cefd...`. The generic raw
proof's historical reduced-inverse pin is not its transversality input;
the corrected final reduced inverse is the dependency used here, as
recorded in `SOURCE_NOTES.md`.

This is an independent fresh-session composition audit with direct reads
of the raw proofs, not an inference from agreement among author verdicts.
The proof-audit skill and its general-logic and duality obligations were
read. No applicable `AGENTS.md` was found in the inspected ancestor and
target locations. No external source, scientific script, numerical
integration, scientific array analysis, or process inspection/control was
used. Operations were `pwd`, `rg`, `cat`, `sed`, existence checks,
`shasum -a 256`, and writing this temporary report with `apply_patch`.
No repository artifact or ledger was changed.
