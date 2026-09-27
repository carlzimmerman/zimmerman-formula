# CRISPY FRIED CHICKEN RECIPE 

**Construction and verification blueprint for one complete relativistic-MOND theory.**
Current objective, updated by the user on **2026-09-08**: construct a new theory
that passes the requirements, not another elimination-only campaign. Work starts
from [the thirteen-requirement specification](FRIED_CHICKEN_SPEC.md). Its physics
requirements take precedence over older recipe language and historical verdicts.

Build one explicit action and its connected derivation. Preserve the exponential
kernel, derive the physical metric response, and prove the constraint and matter
structure together. Checks remain honest: a failure identifies a construction
obligation; it is not permission to conceal the failure or relax a requirement.
Historical obstructions are reference material, not the main deliverable.

**User decision — 2026-09-26 (the author): the kernel is ν_mono, causality is criterion B, Z corrected.**
These three decisions supersede, where they conflict, the ingredients below and the "exact
exponential target" wording of any 2026-09-26 amendment written before them.

- **Requirements 1 and 12 — the kernel is ν_mono.** In QUMOND form, with y = |∇Su|/a₀ the
  filtered Newtonian acceleration: ν_mono(y) = 1 + h_mono(y)/y, with
  h_mono(y) = ∫₀^y max(h′_RAR(s), δ h_p/(s + y_p)) ds. Here h_RAR(y) = y/(e^{√y} − 1) is the
  phantom of the framework's RAR law ν_RAR(y) = 1/(1 − e^{−√y}) (Milgrom & Sanders 2008 eq. 13
  at α = ½), y_p = 2.5396 is its peak, h_p = 0.6476 a₀, and δ = 0.05 is a chosen constant.
  - ν_mono = ν_RAR for y ≤ y* = 2.3374, where the max switches branch, just below the peak.
    Everywhere the two differ by ≤ 0.0104 dex, most at y = 14.35
    ([L340](../../real_research/g03_audit_2026/L340_filtered_khronon_completion.py) A1, K2;
    [XC4](../../real_research/extra_crispy_2026/XC4_nu_mono_splice.py) S2–S4).
    *Corrected 2026-09-26: this line first said "below the peak" and "≤ 0.01 dex" (XR3 K1–K2).*
  - The join at y* is C^{1,1}. C_L is continuous (0.0066) and positive, and dC_L/dy jumps from
    −0.0361 to −0.0014 (XC4 S5). It is still open whether to use a C² variant (a smooth max) or
    to do the symbol and strong-coupling arguments nonsmoothly (XR3 step 0 (b)).
  - Field equations: ∇²u = 4πGρ_b, ∇²Φ = 4πGρ_b + S*∇·[(ν_mono − 1)∇Su], with
    S = e^{(ξ²/2)Δ}.
  - **Why.** A phantom that turns over (C_L < 0) is a ghost or tachyon in every khronon
    momentum channel scanned (L340 H2/H3). Both ν_RAR (y > 2.54) and μ_exp (x > 1, where
    C_L = (1 − x)/(eˣ + x − 1)) turn over. ν_mono does not.
  - **Consequences.**
    - The exact μ_exp target and its primitive G(y) become historical.
    - GR recovery comes from the heat filter, not the kernel's tail. The monotone phantom
      leaves a ~a₀ residual that the ephemerides exclude ~10⁴× unless ξ ≥ 0.031 pc
      (canonical) / 0.045 pc (alt) (L340 S1), so the filter is a required ingredient.
    - The QUMOND primitive is Q(Z) = Z + 2∫₀^{√Z} h_mono(s) ds.
    - The deep-MOND limit, the BTFR and a₀ are unchanged.
- **Requirement 7 — causality is criterion B.** The theory must admit a global time function,
  the khronon τ, compatible with every characteristic cone. That includes degenerate
  (infinite-speed) cones lying in its leaves.
  - No signal may propagate backward in τ, and there may be no closed causal curves.
  - Propagation outside the metric light cone is allowed (Bruneton 2007; Babichev, Mukhanov &
    Vikman 2008; the cuscuton of Afshordi, Chung & Geshnizjani 2007).
  - The metric-cone criterion (A) is dropped because no scalar MOND realisation can meet it
    ([L318](../../real_research/g03_audit_2026/L318_causality_criterion_decides_rung3.py) K3/K4).
  - Well-posedness of the mixed elliptic–hyperbolic Cauchy problem is still required
    ([XC2](../../real_research/extra_crispy_2026/XC2_wellposedness_scoping.py)).
  - C-H/K under B: the khronon's cone is finite (4.4×10²–7.9×10⁵ c; XC1 A9, XC2 B6), and its
    elliptic MOND constraint acts within the leaves. Both are allowed.
  - **Consequence, both ways.** Gate 7's signalling theorem
    ([elliptic_channel_signaling_theorem_2026.py](../theory_2026/york/elliptic_channel_signaling_theorem_2026.py))
    is a criterion-A result. It therefore no longer closes the strict two-DOF constraint branch.
    - That branch ([cde_l4c_2026](cde_l4c_2026/CDE_L4C_STATUS.md), status OPEN; its
      N_grav = 2 certificate was withdrawn 2026-09-03) would meet requirement 2 exactly.
    - But none of its gates were ever derived: the full-action Dirac chain, the moving-source
      (L330-type) gate, the boosted 1PN metric, lensing and the FLRW branch.
    - It was also built on μ_exp.
- **§1 Numbers — Z corrected.** Z = cH_Λ/a₀ = √(32π/3) = 5.7888 is κ = ½ restated
  (Z² = 8π/(3κ²)). It is not a second fitted number, and never ≈ 21.
  - κ is measured: 0.465 ± 0.076 (BTFR), 0.55 ± 0.17 (distance-free).
  - It is not derivable in this action class ([kappa_closure](../../kappa_closure/README.md)
    k01–k03).

**Reciprocal-vacuum amendment — 2026-09-26, CD26-5.**
The [new candidate and review](../../real_research/breakthrough_review_2026_09_26/README.md)
replace the PQ vacuum ingredients, for CA5-GNC-R only, by
`V0 F(t)` outside the excitation perspective, where
`F(t)=1+(t+1/t-2)^2`, `t=1+Z-<Z>_h>0`.
This keeps a positive convex boundary barrier while setting
`F'(1)=F''(1)=0`; the prior `zeta=4/ell-1` tuning is absent.
The new action has positive vacuum scalar kinetic/restoring coefficients
for all finite nonzero modes in its stated domain, a positive occupied-FRW
kinetic Schur complement, and a smooth positive fixed-data Z solve.
Keep the complete occupied spatial matrix and nonlinear inhomogeneous
evolution as separate open gates. The exact global filtered-MOND target,
full constraints/PPN and observed vacuum magnitude also remain open.
The new transport bounds concern linear transverse fields on an expanding
pump and do not certify halo clearing. V0 is an input vacuum tension.
All thirteen requirements and the author's decisions above remain intact.

**Common-action construction amendment — 2026-09-26, CD26-4.**
The [common-action checkpoint](../../real_research/common_action_2026_09_26/README.md)
adds explicit candidate ingredients and records their costs. It preserves
the author's decisions above and all thirteen requirements; it does not
declare the complete recipe satisfied.

- **Vary the source and its zero mode together.** On compact leaves use the
  proper-volume projection in the carrier coupling and retain the resulting
  mean stress and clock terms. A purely spatial unprojected auxiliary cannot
  absorb an everywhere positive homogeneous source. Distinguish the lapse
  density from the auxiliary source whenever the coupling changes.
- **Use the Newton-normalized host and test the switching terms.** The
  normalized alpha sector removes the old finite-alpha frozen sign crossing.
  A convex activation energy controls the fixed-leaf auxiliary solve, but a
  weighted-Laplacian trigger has an additional lapse instability. The new
  intrinsic-Laplacian trigger plus fixed compensator repairs the calculated
  scalar principal block, with an explicitly changed inactive force law.
  Its global filtered static law is also changed: the heat kernel samples
  off/interface regions. Exact requirement 1 remains unresolved, and no old
  lensing, shear or moving-source pass transfers to this new gate.
- **Check canonical reduction, not positivity before elimination alone.**
  An exponential carrier has positive local kinetic coefficients and a unique
  canonical auxiliary solve, yet a two-cell control has negative reduced
  momentum curvature. The explicit perspective replacement
  `Ld=t Kd-Wd/t`, `t=1+Z-<Z>_h>0`, repairs that joint canonical convexity
  defect. It changes the source to `sigma=rho/t`; its nonlinear and vacuum
  response must be derived from this replacement.
- **Retain the positive floor and its physical price.** Adding `V0>0` to the
  carrier potential supplies a proved positive-domain barrier for the fixed
  smooth canonical constraint. Homogeneous `t=1` gives pressure `-V0` and
  energy density `V0`: a precise role for vacuum tension, with an uncomputed
  magnitude. Homogeneous subtraction does not remove its perturbations.
  The newest variant sets bare Lambda to zero, keeps `G_cosm/G_N=cN`, and
  treats any acceleration–tension relation as an explicit input.
- **Retain the derived vacuum-stiffness repair in that same action.** The
  actual expanding-vacuum calculation exposes an infrared scalar problem in
  the perspective-floor trial. The further term `-V0 zeta(t-1)^2`, outside
  `Wd/t`, with `zeta=4/ell-1`, repairs its scalar kinetic/restoring test for
  all finite nonzero wavelengths in the stated parameter window. It also
  preserves the fixed-data positive-lapse theorem. This latest CA4-GNC-PQ
  variant still needs the occupied-carrier, nonlinear and PPN calculations;
  positive linear vacuum modes are not a global theory certificate.
- **Use derived transport with all five real fields counted.** The positive
  square potential for two complex fields and one real field derives
  reversible charge conversion and an outgoing flux. The neutral-trigger
  trial did not improve clearing; the new packet clears only about `9.75e-5`
  of its initial region charge. Neither is a calibrated cosmological
  evacuation law. A slow-wave example is a separate parameter realization.
- **State global results at their proved scope.** Global carrier evolution
  is proved analytically on fixed flat/static geometry; the positive-floor
  auxiliary theorem holds for fixed smooth canonical data. The same PQ
  action also has a nonlinear future-global homogeneous expanding branch,
  approaching de Sitter under positive-mass/floor assumptions, with no
  ordinary matter in that theorem. Full spatially inhomogeneous evolution,
  including the lapse, foliation and all constraints, remains open.
  Lean certifies the listed algebraic bridges, not those continuum proofs
  or the full theory. The host scalar and five carrier scalars remain
  separately counted; the full Dirac classification is still required.

**Inverse-relationship amendment — 2026-09-26, CD26-3.**
The [inverse audit](../../real_research/dark_energy_inverse_2026_09_26/README.md)
keeps the author's filtered ν_mono and criterion-B decision. Its ingredients
clarify which quantities the theory can identify; they do not add a new
dark-matter particle or change the thirteen requirements.

- **Separate pressure from energy density.** Write Pi=-p, with Pi and energy
  density epsilon in J/m³. The proposed pressure link is a0²=κ²G_N Pi;
  the density link is a0²=κ²G_N epsilon. They coincide only for p=-epsilon.
  Specify and derive the chosen link from the common action, or label it as
  an allowed constitutive input. For a separately conserved component,
  constant Pi permits epsilon=Pi+D/a³. Constant a0 therefore does not fix
  the whole sector's equation of state or remove its independent charge/
  density boundary condition.
- **Add the inverse pressure test.** On a flat Einstein-form background
  with constant κ and G_cosm/G_N and negligible ordinary pressure, define
  Q=2 Hdot+3H². The pressure link predicts
  [a0(z)/a0(0)]² Q(0)/Q(z)=1, for a0(0)≠0 and Q(z)>0.
  A conserved pressureless contribution cancels
  exactly. Derive the background/action bridge and include curvature,
  ordinary pressure and data covariance before calling this an empirical pass.
- **Calibrate independent quantities once.** Keep g=G_cosm/G_N explicit:
  Z_H²=8πg/(3κ²), Lambda_geom=8πg a0²/(κ²c⁴), and
  H_vac=H_total sqrt(Omega_vac). The displayed g=1 vacuum dictionary above
  cannot be exported to an action with unequal Newton and cosmological
  couplings. Distinguish geometric, Newton-normalized and bare Lambda.
  A κ estimate already calibrated with an assumed vacuum density returns
  that same density when inverted; it is not a second measurement.
- **Keep gate inverses on their actual branch.** The phantom-inclusive
  DE1 edge and the matter-only lower switch identified in DE4 require
  different source profiles. Preserve background subtraction. Several
  gate epochs identify an exponent only with independent fraction history;
  otherwise they determine its product with the logarithm of that history.
- **Retain vacuum offset and clock excitation separately.** The canonical
  polar clock's rho+p removes its constant vacuum offset. Sound/dispersion
  identifies local potential derivatives on the stated circular branch,
  not that offset. Recovering the offset additionally needs separated
  stress and a specified potential; the clock's source and scalar pairs
  still belong in the full action and field count.
- **Make the lapse inverse a consistency test.** Positive N gives
  A/b=-4 Delta sqrt(N)/sqrt(N). With source, geometry, proper expansion
  and action coefficients calibrated, the reconstructed vacuum coefficient
  must be spatially constant. Without that calibration, exact families
  admit the same lapse, matter and expansion with different vacuum constants.
- **Use names at the established scope.** “Cosmic tension” denotes Pi=-p;
  use “effective cosmic tension” if it is reconstructed geometric stress.
  “Vacuum tension” requires an identified vacuum contribution. These are
  provisional descriptions, not a microscopic explanation or a renaming
  of every dark-sector contribution.

The checkpoint records exact calculations, inverse counterexamples and
scoped Lean certificates. It does not certify the full field theory or a
new observational fit. Common-action closure and the physical origin of
the vacuum magnitude remain open; the specification's permission to retain
an explicitly stated acceleration-scale input remains intact.

**Constructive continuation — 2026-09-26, CD26-2.**
The [continued construction](../../real_research/closure_push_2026_09_26/README.md)
records the user-decision revision above, which entered the shared repository
during its calculations. The operative target is now filtered ν_mono with
criterion B. Earlier exponential/metric-cone statements below remain historical
branch records; they do not override that decision.

- **Advance the cosmological construction:** a new constant active potential
  and gradient coefficient B=b exp(S) give a local linear physical metric/fluid
  system, with positive nonzero-mode kinetic matrix under stated conditions.
  These are explicit changes to the action. They must be connected to the
  operative static sector by a varied transition before claiming one theory.
- **Retain and solve the homogeneous lapse condition:** y=exp(S/2) turns the
  new nonlinear lapse equation into (-4bΔ-A)y=0. Explicit positive-density,
  expanding, inhomogeneous initial data solve the constraint. The positive
  ground-state factorization controls the normalized lapse shape; the global
  constraint and full field count cannot be discarded. A conditional canonical
  reduction to H_red=-c lambda0 preserves that global condition; its full-action
  and continuum hypotheses still need to be verified.
- **Use the actual outer heat filter at zero field:** it makes the fixed-leaf
  force spatially Lipschitz even where the inner acceleration vanishes.
  This does not establish Lipschitz dependence on source data or full coupled
  well-posedness. Keep that distinction in the requirement-9 calculation.
- **Improve the exponential branch without borrowing its passes:** the
  symmetric auxiliary penalty is globally C² and preserves its demonstrated
  static branch. Deriving G_N rather than setting it equal to G_bare opens a
  positive principal window, but the tested family fails its derived
  preferred-frame check. Neither conclusion automatically applies to ν_mono.
- **Keep clock stress in the common-action source:** a charged amplitude/phase
  clock has a proved homogeneous timelike branch, but also adds a nonzero
  static density and pressure response. Vacuum subtraction cannot remove that
  response. Its two scalar pairs must remain explicitly counted.

The checkpoint contains scoped Lean certificates and reproducible calculations.
The new potential's magnitude and the a0–Λ coefficient remain declared inputs.
Full nonlinear evolution, the common static/cosmological action, PPN and
empirical closure remain **OPEN**.

**Constructive amendment — 2026-09-26, CD26-1: all-door calculations.**
The [new calculation campaign](../../real_research/closure_doors_2026_09_26/README.md)
extends the source audit below with direct action constructions and controlled
continuations. Keep the thirteen requirements unchanged and use these updated
ingredients at their demonstrated scope:

- A directly integrated acceleration primitive gives exact **general-source
  exponential AQUAL**, with both static metric potentials varied. Its displayed
  two-scalar realization is healthy on a bounded low-acceleration principal
  branch; global health, field classification and PPN remain open.
- The original geometric heat filter does **not** contract the lapse-weighted
  norm for arbitrary positive lapse. Retain its proved sufficient contrast bound,
  or explicitly change to the weighted operator ΔN=N⁻¹Di(NDi). The latter repairs
  fixed-geometry auxiliary existence/uniqueness, and must be varied with N.
- A vacuum-regulated C∞ gate supplies a global domain and exact plateaus. Its
  actual scalar variation creates a curvature-gradient obligation. A concave
  repair and a local positive-energy causal completion are explicit separate
  constructions; their field counts and static effects must be reconciled.
- A healthy wave pole alone is insufficient: the regular rank-one trace-mixing
  family fails the independently derived conserved-source tidal response at
  high acceleration. New work must change that structure, not retune its weights.
- Fisher capillarity has a **local same-canonical-pair** wave representation.
  Its nodes and phase gradients need a global clock treatment; wave notation
  neither proves a new particle species nor supplies causal gravity by itself.
- Vacuum origin, its magnitude, the gate and κ remain separate questions.
  Requirement 13 permits a declared a0–Λ relation; no free coupling ratio or
  allowed vacuum counterterm is to be called a first-principles prediction.

The campaign retains exact calculations, numerical refinement, independent
reviews and scoped Lean certificates. These ingredients have not yet passed
as one common action. The target remains **OPEN**.

**Dated amendment — 2026-09-26: ingredient and evidence reconciliation.**
The thirteen-requirement spec remains the success contract. The recent C-H/K,
vacuum-gate and carrier calculations are useful branch research; they do not
replace the exact exponential target or certify one completed action. The
[source audit](../../real_research/closure_resume_2026_09_26/recipe_audit.md)
records the equations, input revisions and precise limits. Earlier checkpoints
below remain historical records, including their original dates and labels.

- **Keep the exact kernel distinct from approximate alternatives.** The original
  [C-H action](g03_covariant_action_2026/ACTION.md) already identifies itself as
  screened T-B, not strict exponential AQUAL T-A. [L340](../../real_research/g03_audit_2026/L340_filtered_khronon_completion.py)
  further replaces its kernel by `nu_mono`, numerically built from `nu_RAR`.
  Similar galaxy fits do not establish the exact equation in requirement 1.
  On its spherical branch, write `x=g/a0`, `t=g_N/a0` and `h=g-g_N`; then
  `t=x(1-exp(-x))`, `h/a0=x exp(-x)` and
  `d(h/a0)/dt=(1-x)/(exp(x)+x-1)<0` for `x>1`.
  Thus L340's positive-longitudinal-response construction cannot simply inherit
  that kernel. Its 243 failed alternative parameter cells are a bounded scan,
  not a theorem excluding every possible momentum channel or action.
- **Count the clock before assigning its category.** L340 adds
  `alpha_c a_mu a^mu - c_2 K^2` and explicitly obtains an extra scalar mode in
  its reduced block. Calling it a clock does not establish the spec's exception
  for a genuine matter/clock scalar. The full canonical classification,
  independent initial data and health must still be derived for the final action.
  Particle-free does not mean free of independent field initial data or charges.
- **Retain the no-dark-matter-particle constraint.** A Newtonian-inferred phantom
  density is a description of a derived metric response. It does not supply an
  independent cosmological density or prove equality to a field's Hilbert stress.
  L353/L361 explicitly introduce `rho_d`; a wave/condensate interpretation must
  state its action, initial data and observable force law before use. Numerical
  particles used to sample a continuum are not, by themselves, a particle ontology.
- **Do not promote partial PPN or strong-coupling checks.**
  [KM3](../../real_research/khronon_momentum_2026/KM3_chk_one_pn.py)
  derives static `beta=gamma=1` in the reduced khronometric sector; its remaining
  zero-parameter and filtered-remainder checks include documentary inputs.
  [XC1](../../real_research/extra_crispy_2026/XC1_strong_coupling_chk.py)
  supplies useful cubic/quartic decoupling power counting, while explicitly
  omitting filter metric/foliation vertices and a full curved-background analysis.
  G7/G8 remain conditional at full-action scope. XC1 also reports a scalar speed
  above the physical metric light cone; preferred-foliation causality alone is
  not a pass of requirement 7 without resolving that requirement explicitly.
- **Keep vacuum origin, scale normalization and environmental gate separate.**
  In C-H, `Lambda` and `a0` are independent inputs. A constant vacuum term has
  `w=-1`; the action must additionally explain its magnitude and any relation
  to `a0` before those are called derived. Four-form promotion is a distinct
  action proposal, and a relation structural within that proposal does not select
  its free dimensionless ratio. The L359 power and threshold are chosen inputs;
  L361 varies its nonrelativistic fields with the gate prescribed. A gate window
  or edge-law identity does not complete their covariant, conserved, stable
  combination. Never pool passes from different gate cells or action revisions.

**Next constructive obligation:** use one explicit particle-free action and one
kernel definition; derive its scalar constraint/initial-data structure, both
physical metric responses, and the gate's variation together. Preserve the
exponential branch as the target and label any alternative as a separate branch.
The canonical target is **OPEN**, with the bounded results above retained.

**User decision — 2026-09-26, later the same day (the author, answering the cross-thread review): both branches, every switch variable, PAPER34 v2 after the re-score.**
These add to the decisions above and change none of them.

- **Architecture: both, as separate branches.** Asked which cosmology the one combined action
  should be built on, the author answered "Both, as separate branches".
  - **B-νmono (C-H/K).** The C-H/K khronon with the leaf average, the vacuum gate and the region
    kernel (L340, L350, L353, L359/L361, DE1–DE3). Its one covariant action is still to be
    written, with the gate as a varied term and a slot for the dark state. The
    [cross-thread review](../../real_research/cross_thread_review_2026_09_26/README.md) calls it
    "V0" (unrelated to any vacuum-tension V0), and its XR3 obligation table is the checklist.
  - **IC28.** The lead track's cosmological sector continues as its own branch.
  - Passes are never pooled across the two branches.
- **The switch variable: "all doors".** Asked which density the MOND switch should read, the
  author answered "all doors". Every candidate is explored as its own labelled cell and never
  pooled with another. The candidates are the curvature-based, phantom-inclusive variable
  (DE1/DE2, L352), the matter-only variable of the PM runs, and the absolute- and
  contrast-density definitions.
- **PAPER34: a v2 scope note after the re-score.** Asked whether PAPER34 needs a v2 note on the
  scope of L372's result, the author answered "Yes, after the re-score". The note waits until
  L372 has been re-scored at the p = 1, x_c0 = 2.5 cell.

**Current constructive checkpoint (2026-09-09, IC26):**
[The finite-band construction](integrable_clock_construction_2026/IC26_FINITE_BAND_REPAIR.md)
reconstructs A,D,E4 together and independently controls the negative lapse
Schur coefficient and high-frequency response. The IC25 amplification near
2.26e5 is reduced to order-unity values in preliminary same-action propagators;
refined and independent precision checks are recorded in ic26_run_001.
Residual long-wave modes, nonlinear interaction scales, same-function
off-trajectory tests, global/static/nonlinear closure and empirical gates
remain OPEN. A background or sampled-wave success is not full stability.

**Previous constructive checkpoint (2026-09-09, IC25):**
[The joint coefficient construction](integrable_clock_construction_2026/IC25_COUPLED_RECONSTRUCTION.md)
reconstructs A(S) and D(S) together, then varies their actual S-only jets.
Scaling the construction clock drift with exp(-3Q) removes the automatic
dilution factor from the homogeneous lapse Schur equation. The exploratory
mixed branch reaches seven barred-scale e-folds with sampled causal margins;
this is not a recombination fit or an infinite-time theorem. Full Hamiltonian
perturbation transport now supplements instantaneous roots. Same-function
off-trajectory tests, limiting jets, global/static matching, nonlinear closure,
PPN, interaction scales and empirical gates remain OPEN.

**Previous constructive checkpoint (2026-09-09, IC24):**
[The integrated potential construction](integrable_clock_construction_2026/IC24_INTEGRATED_POTENTIAL.md)
turns the pointwise repair into one local D(S) via a constrained initial-value
problem, with independent checks of both coefficient-integrability identities.
The sampled causal mixture extends past the old crossing to Q~.04860087,
where a new light-cone event occurs; no long healthy cosmology is claimed.
The negative lapse Schur design removes spatial auxiliary zeros on the regular
pinned branch. The next construction must integrate a second coefficient A(S)
alongside D(S), derive its characteristic response, and retain the same action
in all tests. Global/static extension, nonlinear closure and empirical gates
remain OPEN.

**Previous constructive checkpoint (2026-09-09, IC23):**
[The simultaneous matter calculation](integrable_clock_construction_2026/IC23_MIXTURE.md)
derives the three-scalar clock/radiation/positive-pressure system from one
summed action. Exact combined cone inequalities and full frequency checks
give a local positive subluminal mixed branch. Continuing that SAME branch
crosses the light cone near .00372333 e-folds while auxiliaries remain regular.
The next construction is an integrated potential coefficient D(S), using
the derived lapse-curvature control equation, not another isolated tuning or
an imported cosmology. Pointwise replacement jets are not yet a new global
action. Full closure remains OPEN.

**Previous constructive checkpoint (2026-09-09, IC22):**
[The dust and pressure derivation](integrable_clock_construction_2026/IC22_DUST_AND_PRESSURE.md)
varies the dust multiplier, computes the full local auxiliary matrix and
retains leading frequency-dependent mixing. Its real fast wave coexists with
an exactly derived defective zero-speed principal sector; no strong-hyperbolicity
pass is claimed for ideal dust. An explicit positive-pressure matter action,
with gravitational coefficients unchanged, gives two positive subluminal
characteristics on tested points, including w=10^-8. Next combine radiation
and this matter action in ONE three-scalar calculation, then test relative
flow and extended evolution. Separate two-field results are not a mixed-fluid
cosmology or a complete theory.

**Previous constructive checkpoint (2026-09-09, IC21):**
[The explicit radiation calculation](integrable_clock_construction_2026/IC21_RADIATION.md)
varies a minimally coupled radiation action with the unchanged IC20 gravity
action. Its coupled scalar principal matrix yields explicit density-dependent
positivity/light-cone inequalities, checked against the full time-dependent
quadratic reduction and short sourced evolution. The five dilute aligned
backgrounds have two positive subluminal scalar characteristics; this is not
recombination, relative-flow stability or full cosmology. Next derive the
degenerate dust sector and relative-flow constraints, while extending the
healthy background. No new global theory or empirical pass is announced.

**Previous constructive checkpoint (2026-09-09, IC20):**
[The joint-action handoff](integrable_clock_construction_2026/IC20_HANDOFF.md)
solves the kinetic/curvature and tensor-cone compatibility equations together.
The varied analytic auxiliary has a computed regular local constraint matrix;
the selected expanding vacuum point has positive scalar kinetic energy and an
all-wavelength positive oscillator coefficient, including time-dependent
curvature mixing. Short vacuum and small-matter background continuations are
tested, not a viable cosmology. A longer-lived parameter control has negative
finite-k scalar coefficients and cannot donate its longevity to the selected
action. Next derive coupled matter perturbations and construct a healthy
extended evolution from this same action. No full closure or PPN/galaxy pass.

**Previous constructive checkpoint (2026-09-08, IC19):**
[The normalized spatial handoff](integrable_clock_construction_2026/IC19_HANDOFF.md)
imposes Carl's scale relation in the action and establishes an invariant
expanding pole-clock plateau. Its cleaned spatial action has an explicitly
varied lapse operator and a regular expanding curved constraint witness.
The next scalar-energy calculation fails despite that regularity. The derived
trace/curvature compatibility now specifies what the next construction must
satisfy; a local Hessian solution is not a completed theory. Do not repeat
the same switch-shape scan or import PPN and galaxy passes from another model.

**Previous constructive checkpoint (2026-09-08, IC18):**
[The pinned-clock handoff](integrable_clock_construction_2026/IC18_HANDOFF.md)
removes the mixed clock–matter principal coupling by a varied auxiliary
constraint, preserving a positive causal clock and radiation/dust expansion
on its exact Einstein plateau. It adds no propagating auxiliary. The same
global action's homogeneous transition has now been varied: a located
primary/secondary rank-loss point fails the next preservation condition.
Retain the working pin mechanism; repair or rigorously exclude that transition
branch before claiming a global theory. No PPN, matched MOND galaxy, empirical
fit or full closure is certified. Exact checks and strict refusals are linked
in the new computation record.
The next discriminating input is Carl's original a0–Lambda normalization,
which the obsolete tuned witness did not implement. A separate finite probe
removes the sampled homogeneous transition roots, not the obligation to
construct a regular spatial connection. It is not counted as closure.

**Previous constructive checkpoint (2026-09-08, IC17):**
[The pole-clock handoff](integrable_clock_construction_2026/IC17_HANDOFF.md)
specifies the action-derived early radiation/cold-clock construction, actual
baryon-source variation, and a corrected scope audit of the transition
obstruction. It retains the static exponential primitive and supplies a
tested eight-physical-e-fold background without the prior small-S ghost
or late-condensate tuning. These are finite, sourced-background results,
not an empirical recombination fit or complete gravitational closure.
The subsequent full irrotational clock–dust principal test passes on aligned
samples but FAILS with relative flow, including a local ADM constraint-data
construction for the failing point. IC17 is not a uniformly healthy theory.
Next repair that same-action mixed principal structure and rerun the explicit
counterexample before attempting transition or embedded-galaxy certification.
Do not import IC15's separate matter-potential repair into IC17 by name.

**Previous constructive checkpoint (IC13/IC14):**
[The new handoff](integrable_clock_construction_2026/IC13_IC14_HANDOFF.md)
records an explicit fold-free local matter response, a derived transition
kinetic/curvature repair and its remaining superluminal scalar, a quantified
early-history limitation, and the full-covariance supernova reanalysis.
IC14 is the best local matter component, not a global MOND action. Its results
cannot be pooled with IC13 as if a combined healthy theory had been derived.
Full closure remains OPEN; the next construction and its early-universe and
sourced-galaxy obligations are explicit in that handoff.

**Previous constructive checkpoint (IC11/IC12):**
[The shared handoff](integrable_clock_construction_2026/IC11_HANDOFF.md)
records the new convex clock-pressure construction, matter-coupled response,
full transition, combined action, and exact-law empirical source targets.
IC11 improves the healthy vacuum plateau; its balanced auxiliary response also
passes weak-matter cone tests. The separately completed tensor/auxiliary
transition and the IC12 combined action still fail a scalar kinetic condition.
Clusters and galaxy pairs supply required source targets, not successful
predictions of the clock. Carl's paddle/wake history-dependence suggestion is
[credited explicitly](integrable_clock_construction_2026/CARL_CLOCK_MEMORY_INSIGHT.md).
The next construction must repair the full transition and matter-domain
limitations, then predict the same physical-metric galaxy/cluster forces.
No complete theory, empirical confirmation, or novelty certification is claimed.

**Previous constructive checkpoint (IC10):**
[IC10 local Einstein–clock construction](integrable_clock_construction_2026/IC10_LOCAL_CLOCK.md)
continues the explicit phase action while retaining its static exponential
primitive. [IC8–IC9 optical alignment](integrable_clock_construction_2026/OPTICAL_ALIGNMENT.md)
removes the tested shear/curvature mixing and aligns the tensor cone, but
IC9's exact scalar response retains a rational spatial factor. IC10 aligns
the trace kinetic term as well: its vacuum expanding plateau is exactly
Einstein gravity plus a local clock pressure built from the same primitive.
Fresh auxiliary solves and finite FLRW evolution have positive sampled clock
kinetic energy, subluminal sampled clock propagation and expansion. The
auxiliary carries no independent mode on this regular plateau; the genuine
clock is explicitly counted separately from the two tensors.

This is **not a complete gravity theory**. The next unavoidable calculation
was full-action evolution through the located eta boundary near S=0.230724,
including its momentum derivatives, constraint preservation and physical
characteristics. Matter-coupled causality, strong coupling, galactic matching,
zero-field control, measured G, PPN and realistic cosmology remain OPEN.
Exact derivations, unsuccessful full-goal gates and bounded tests are linked
in the [reproduction record](integrable_clock_construction_2026/REPRODUCE.md).
No full-theory PASS, novelty certification or empirical prediction is claimed.
Continue from this explicit action, not historical candidate labels below.

**Methodological inspiration:** OpenAI's *NavierStokesAndEuler* repository,
particularly its independently specified Comparator challenges and separately
checked proof submissions. We adapt that verification architecture to a
constructive gravity target; we do not import a fluid theorem as gravity evidence.
See [the pinned project checking instructions][NS-checks] and the complete
attribution and limits in section 12.

**Every future Claude/Qwen/Codex handoff begins from this file and the current
spec. Last updated 2026-09-08.** Record a proved gate change with its exact action
revision and supporting derivation; never rewrite immutable old evidence.

---

## 1. FROZEN INGREDIENTS
- **I1 — MOND kernel [amended 2026-09-26, user decision]:** ν_mono, the RAR exponential law
  ν_RAR(y)=1/(1−e^{−√y}) with a monotone phantom (definition in the user-decision block above), QUMOND form,
  y=|∇Su|/a₀. Limits ν→y^{−1/2} (y≪1), ν→1 (y≫1). Historical, retired as the target: the AQUAL μ(y)=1−e^{−y},
  y=g/a₀. Changing the kernel again = a DIFFERENT recipe, branched explicitly, never silently substituted.
- **I2 — Single physical metric:** S_m=S_m[g,ψ]. No hidden second metric / disformal matter metric /
  sector-dependent G without explicit reclassification.
- **I3 — GR tensor sector:** c_T=1, Q_T>0. No hiding a tensor-speed correction behind a low-frequency
  approximation.
- **I3a — Gravitational mode target:** exactly N_grav=2, the tensor polarizations.
  A genuine matter/primordial-clock scalar is allowed only with its own explicit,
  healthy, separately derived count. Relabeling a scalar graviton is not a solution.
- **I4 — Local screening anchor:** the Solar System is high-acceleration INSIDE the galactic MOND
  environment ⇒ screening must be controlled by a LOCAL dynamical quantity (acceleration/derivative), not
  environment labels, halo phases, potential-only or velocity-dispersion screening.
- **I5 — Newtonian recovery [amended 2026-09-26]:** through the heat filter S=e^{(ξ²/2)Δ}, ξ ≥ 0.031 pc
  (canonical) / 0.045 pc (alt) (L340 S1). The kernel acts on the filtered field, so the Sun's own high-y field
  never reaches it. A monotone phantom keeps rising slowly, so the kernel's tail is not exponentially small;
  the filter does the screening. No singular 1/y factors to repair perturbative order unless the full
  nonlinear theory proves them removable.
- **Numbers (locked) [Z corrected 2026-09-26]:** a₀=κc√(Gρ_Λ)=9.3619e-11 (κ=½ FITTED;
  Z=cH_Λ/a₀=√(32π/3)=5.7888 is κ=½ restated, not a second number — the earlier "Z~21" was an error; the a₀
  reframing is the claim, not a derivation). a₀(z): the framework's law is FLAT (a w=−1 vacuum; <1% to z=5;
  L37, L273–L275). That is a prediction, NOT action-derived; a₀∝H(z) is the rival.
- **μ realizations (verified; historical since 2026-09-26 — they realise the retired μ_exp; ν_mono's QUMOND
  primitive is Q(Z)=Z+2∫₀^{√Z}h_mono(s)ds, which for ν_RAR is Z+4I₃(Z^{1/4})):** (A) auxiliary-Legendre χ: V′(χ)=−[ln(1−χ)]², χ=μ(y); primitive
  G(y)=y²+2(1+y)e^{−y}−2 with G′/(2y)=1−e^{−y}. (B) nonlocal F₊(Z)=4[1−(1+√Z/2)e^{−√Z/2}], Z=4y²,
  2F₊′=e^{−y} (`mond_compiler_2026/FROZEN_PRIMITIVE.md`). Constitutive ingredients, not new fields.

## 2. HISTORICAL CONSTRUCTION WARNINGS (apply only with their proved hypotheses)
The entries below retain earlier research claims for traceability. A historical
class label or finite search is not an automatic theorem about a new action.
- **P1 — Quadratic MOND carrier stress:** a carrier lensing only through (DΦDΦ)^TF-type quadratic flux
  vs a linear obstruction. [T3 + order-counting kill a9261161: Σ_P is unique O(ε²,Φ²).]
- **P2 — Unscreened constant preferred-frame coupling:** killed by α₁,α₂. The viable pattern is
  **α_PF ∝ 1−μ = e^{−y}** (or a proven equivalent). [AeST α₂∝1/K_B; disformal α₂∝φ̇_c².]
- **P3 — Lapse-weighted MOND destroying the constraint algebra** (H_perp demoted → unwanted scalar).
  [φ=lnN and sf42 both leaked → 3 DOF + strong coupling.]
- **P4 — Hidden propagating scalar:** "auxiliary"/"nonlocal" by NAME doesn't count — must demonstrate no
  independent canonical initial data. A localization trick does not remove a physical scalar.
- **P5 — Ghost by negative spectral residue:** negative kinetic eigenvalue/residue = kill unless a full
  constrained analysis proves the variable nonphysical.
- **P6 — Temporal nonlocality as a free escape:** spatial elliptic nonlocality is admissible research;
  □⁻¹_ret needs an explicit causal construction + phase-space analysis. [Banked: ω²=½c²k² warning.]
- **P7 — Screening that kills the kinetic term:** if α→0 simultaneously sends the scalar kinetic
  normalization →0, treat as STRONGLY COUPLED unless an independent finite normalization is shown.
  [The khronometric survivor's exact open wound.]

## 3. ACCEPTABLE PROTEINS
- **A1 — Constraint-first dynamics:** MOND as a gravitational constraint (q=−⅙ ln det γ,
  C_M = D_i[μ(y)D^i q]−source ≈ 0); generic branch gives a second-class pair + 2 tensor DOF. Branch-
  restricted; never promote to a global theorem without the open checks (foliation, matter, cosmology).
- **A2 — Auxiliary-Legendre χ** (see I5/μ-realizations).
- **A3 — Preferred frame, IF screened:** allowed when observables are screened (α_PF ~ e^{−y}); **MANDATORY
  DESIGN PRINCIPLE: PPN-visible coupling ≠ kinetic normalization** — the same coefficient must not control
  both (else P7).
- **A4 — Spatial trace-free tensors:** allowed to solve a genuine constraint problem, NOT to manufacture
  lensing; check G0 weak-field order BEFORE building the action. [Q_ij second-class removal is proven.]
- **A5 — Spatially nonlocal elliptic operators:** (−D²)⁻¹, f(−D²/a₀²) — elliptic, no temporal mode,
  controlled GR limit. NOTE: changes momentum scaling, NEVER perturbative amplitude order.

## 4. THE CORE COOKING RULE
**MOND strength ≠ lensing carrier ≠ propagating-scalar normalization** — unless a derivation proves
identifying them creates no instability. (The central lesson of the whole program: AeST identified the
first two and died at α₂; khronometric identifies the last two and risks strong coupling.)

## 5. REQUIRED PROOF OBLIGATIONS (all from the same action)
Build these as connected work packages under section 12. Prioritize constructing
the action and its central constraint/matter/static identities; independent workers
may derive other sectors once the same action revision is frozen. A failed check
must be reported and addressed in the construction, not promoted to a pass.
- **G0 Structural order:** Φ→εΦ; order every proposed source. Different-order terms cannot cancel for
  arbitrary weak fields without an independently justified singular mechanism.
- **G1 Exact MOND reduction:** ∇·[μ∇Φ]=4πGρ over the full MOND domain (no isolated-point fits).
- **G2 Newtonian/GR limit:** derive the measured G_N and its relation to bare
  couplings, then establish regular recovery using that same measured constant
  in dynamics, lensing and cosmology. Never hide a discrepancy by inconsistent
  normalizations or assume measured G_N equals the bare coupling.
- **G3 Tensor sector:** explicit quadratic action; Q_T>0, c_T²=1.
- **G4 DOF:** actual Hamiltonian/characteristic analysis. Never infer DOF from appearance.
- **G5 Ghost/gradient:** K_i>0, c_i²>0 for every propagating mode (or an explicitly justified limit).
- **G6 Lensing:** derive Φ,Ψ; MOND-enhanced dynamics AND lensing; clean target Φ=Ψ.
- **G7 PPN:** compute γ,β,α₁,α₂,α₃ explicitly. Never infer α₂=0 from "no explicit vector."
- **G8 Strong coupling:** canonically normalize; compute Λ_sc on the ACTUAL Solar-System background;
  require Λ_sc ≫ E_relevant. A vanishing kinetic coefficient is not rescued by a large sound speed.
- **G9 Matter consistency:** full relativistic conservation, not just the Newtonian-limit check.
- **G10 Cosmology:** FLRW, a₀ behavior, cosmological G, perturbations, growth, CMB/ISW, k=0 branch.
- **G11 Strong field:** compact objects, BHs, caustics, nonlinear continuation where demanded.
- **G12 Radiative/naturalness:** is the screening relation technically stable or fine-tuned?

## 6. VERDICT VOCABULARY (exactly one per result)
**PASS** (explicitly established) · **OPEN** (survives prior gates, not yet computed) · **CONDITIONAL**
(works on a stated branch/domain) · **KILL** (demonstrated failure) · **DEAD CLASS** (structural proof
eliminates a family). Never call a candidate "viable" while OPEN or CONDITIONAL.

## 7. DISCOVERY ALGORITHM
Trusted target → explicit construction → action variation → coupled proof
obligations → independently reproduced checks → assembled same-action result.
The next deliverable must supply an action term, a derivation, a solved compatibility
condition, or a verified construction lemma needed by the candidate. Do not replace
it with a fresh catalogue of excluded models. If a calculation exposes a defect,
retain the evidence and derive a correction from the required identity; do not
silently change models between gates. Stop claiming progress from a new label alone.

## 8. GLOBAL DESIGN TARGET
One metric; ν_mono through the heat filter [amended 2026-09-26]; correct MOND dynamics + lensing; c_T=1; no
ghost; no gradient instability; acceptable PPN; Λ_sc≫E; causality by criterion B (a global preferred time, no
signal backward in it); healthy matter + cosmology. **The required gravitational
count is N_grav=2; the calculation must derive that count, never hard-code it.**
Additional genuine matter/clock modes must be separately counted and healthy as
specified in FRIED_CHICKEN_SPEC.md. A computed third gravitational mode does not
pass simply because a previous recipe allowed it. Constant a₀ is acceptable;
the fitted a₀–Λ relation is not promoted to a first-principles derivation.

## 9. HISTORICAL PROGRAM SNAPSHOT (2026-08-29; not current certification)
This archived snapshot and section 10 were not re-audited by the blueprint edit.
Their broad class verdicts and PASS labels must be checked against their actual
assumptions, code and current spec before reuse. In particular, a three-gravitational-
mode candidate cannot close the current two-mode target. Do not treat a candidate
scan as a universal proof or the phrase "only live class" as an exhaustive theorem.
**Master no-go (DEAD CLASS, exhaustive):** {local, ≤2-deriv, single-metric, correct MOND lensing} ⇒
{unremovable preferred-frame carrier}. 108k-candidate search, zero survivors; unique lensing fix =
Bekenstein's disformal (M5/M1=4.000000, rediscovered by root-finding); cancellation ∝A_0², frame not
removable. `mond_compiler_2026/CAPSTONE_PINCER.md`. ⇒ the 2-DOF/no-frame dream is dead; escapes = screen
the frame (A3/P2 pattern) or leave locality (A5).

**⭐ Current best candidate — khronometric/Hořava + MOND (self-screened), CONDITIONAL:**
`L = N√γ[K_ijK^ij − λ_K K² + R³ + η a²] − N√γ V(χ) + S_m[g,ψ]`, η=2(1−χ)=2e^{−y}, β=0, λ_K≠1.
(`theory_discovery/KHRONOMETRIC_MOND_GAUNTLET.md`, 35/35, BPS-anchored.)
| Gate | Verdict |
|---|---|
| G3 c_T=1 | PASS (proven; β=0 forced) |
| G6 lensing Ψ=Φ boosted | PASS (γ_PPN=1; NOT the ×2 under-lens) |
| G7 α₁=−8e^{−y}, α₂≈−e^{−y} | PASS structural (MOND-off ⇒ α≡0; const λ_K adds nothing unscreened) |
| G5 khronon health | PASS on 1<λ_K≤1.10 (BBN-narrowed) |
| G4 DOF | =3 (2 tensor + 1 khronon; H_perp 2nd class, Hořava-class) |
| 🔴 G8 Λ_sc as η→0 | **OPEN — THE make-or-break** (c_s²→∞; P7 risk; same wall as AeST c_s²~1/K_B) |
| 🔴 kernel-dependence | screening NEEDS the exponential kernel (μ_n gives α₂~7e-6 @Neptune, 60× over) |
| 🔴 Cassini Q₂ / G9–G12 | UNTESTED |
**Next architecture must separate: screened PPN response ⟂ finite kinetic normalization (A3 principle).**

**Live alternative — nonlocal DEFW/F₊ (aether-free):** evades the master no-go via A5; PASS: MOND, BTFR,
spherical lensing, c_T=1 (TT quadratic); OPEN: localization→G4→G7→G10 (P4/P6 apply; ω²=½c²k² warning).
`mond_compiler_2026/FROZEN_PRIMITIVE.md`.

## 10. HISTORICAL FAILURE RECORDS (preserved, not the active work queue)
| Architecture | Killed by | Ref |
|---|---|---|
| FC-AeST + c₂★ (6-DOF aether) | α₂=1+2/K_B~8e4 (λ_s=1); α₁~−2.7 | 66cf94e5, FC_AEST_STATUS.md |
| 2-DOF MMG constraint-first (lapse) | γ_PPN=0, α₁=+4, α₃=−1, matter non-conservation | REFEREE_REPORT_FINAL.md |
| Disformal scalar (TeVeS-no-vector) | under-lenses; α₂∝φ̇_c² unprotected | 4ccc9f27 |
| ZMBC auxiliary-σ Legendre | μ+2sμ′=0 ⇒ μ∝s^{−1/2} only | (sympy) |
| Local aux-carrier Q+(∇Φ∇Φ)^TF+R^TF | G0: Σ_AR O(ε³) vs Σ_P O(ε²); Σ_RR spin-0 only | a9261161 |
| TTA-1 as-written (B from χΦ′) | under-lenses ×2 (Ψ tied to un-boosted g_N) | TTA1_AND_SELFSCREEN.md |
| UV-deformed AeST (λ_∞~10⁸) | needs β₀~1e-8 vs fold β₀_min=0.533; placement pincer | (documented) |
| CCG curvature-ratio | Ostrogradsky; ratio singularity; tidal≠acceleration | (documented) |
| Minimal AC-MOND (aux connection) | regular branch A_μ=0 ⇒ carrier off | (sympy) |
| Whole local no-frame class | the 108k master no-go | 9c52966f |

## 11. THE "EXTRA CRISPY" RULE
Never "we found the new theory" → **"we found the next architecture."** Never "no ghost" → **"no ghost in
the tested sector."** Never "viable" until every mandatory gate is PASS.
The objective is to construct and demonstrate one complete theory. Neither a
collection of failures nor a collection of unrelated passes satisfies it.

## 12. CRISPY FRIED CHICKEN VERIFICATION BLUEPRINT

### 12.1 What is borrowed, and what is our adaptation

The OpenAI project supplies Lean formalizations and distinct challenge/solution
modules, with explicitly listed theorem names and allowed axioms; its checking
configuration also requests a second kernel. That is the methodological
inspiration, not evidence for this gravity program. [OpenAI repository README][NS-main];
[Navier–Stokes checking configuration][NS-config].

Comparator's documented guarantee is conditional on trusted challenge definitions,
imports, build configuration, isolation and kernel correctness. It checks statement
identity, permitted axioms and proof acceptance, with optional additional kernels.
Its documentation also warns that unrestricted definition holes can satisfy a
formal challenge without meeting its intended meaning. [Comparator documentation][Comparator].

**Our constructive adaptation:** specify the desired gravity theory independently
of the candidate, build the candidate and proofs separately, and then verify that
the proved statements are exactly the required ones. This is an original project
workflow proposal, not a claim that the fluid authors devised this gravity method.

In short: **fixed gravity challenge → one explicit action and connected proofs →
independent statement, dependency and proof checks → same-action assembly**.
This verification strategy is explicitly **inspired by OpenAI's
NavierStokesAndEuler project** and its [Comparator checking workflow][NS-checks].
Adopting that workflow is not an assertion that our gravity proofs have already
been formalized or checked by Lean.

### 12.2 Three separate responsibilities

| Responsibility | Required artifact | Cannot be changed by the proof author to obtain a pass |
| --- | --- | --- |
| Trusted challenge | Precise thirteen-requirement contract, physical definitions, allowed fields, boundary/initial data, empirical tolerances and branch hypotheses | Meaning of N_grav, physical metric, conservation, exact μ, admissibility, or the success predicate |
| Construction and proof | One fully written action/Hamiltonian, Euler–Lagrange equations, canonical structure and connected proofs | No borrowing a missing result from another action, coefficient choice, matter sector or inverse prescription |
| Independent verification | Statement comparison, proof/dependency review, executed calculations and, for implemented Lean portions, kernel checks | Cannot replace missing mathematics by hashes, green tests, unchecked axioms or sampled ranks |

The intended final statement is **existence of one explicit admissible theory
satisfying the fixed spec**, not merely “if a successful theory exists, it works.”
The challenge owns the definition of success. A candidate record must not contain
assumed fields such as `has_two_dof = true`, `gamma = 1`, or `satisfies_spec = true`
in place of derived propositions. No assumed MOND equation may stand in for varying
the action. Supply nonempty admissible-data/parameter witnesses, including a
nontrivial galactic branch and H≠0 FLRW from the same theory, so an inconsistent
hypothesis set cannot make the result vacuously true.

### 12.3 Construct from joint compatibility conditions

The first construction package is one physical metric plus the permitted field
content, including a genuine primordial clock only if its healthy independent
initial data and canonical classification can be demonstrated. Write every action
term, coefficient, physical metric coupling and boundary prescription explicitly;
`S_aux` is a placeholder, not a finished construction. Preserve the exact primitive
G(y) while deriving its placement in the action rather than assigning a phantom
stress by hand. Keep a₀ constant and the a₀–Λ relation labeled input unless derived.

Solve the degeneracy/constraint conditions, matter Ward identity and two static
metric variations as a **joint compatibility problem** for that action. Do not
derive MOND first and bolt unrelated lensing, conservation or DOF results onto it.
Any proposed auxiliary elimination must preserve the action domain, boundary
conditions and solution/initial-data correspondence. A singular reduction is its
own branch, not a limit to substitute without proof.

Each successful lemma becomes a dependency for the next calculation. When an
identity does not close, the construction worker must identify and derive the
missing coupling or constraint—not launch a stand-alone family-elimination scan.
Verification still reports genuine failures; the new priority does not authorize
false passes or suppression of adverse data.

### 12.4 One action ID, with parallel proof packages

Freeze a candidate ID containing the commit/hash of the full action, physical
matter sector, parameter values/functions, clock prescription, inverse domains
and boundary conditions. The following packages all consume that ID:

| Package | Required derived output |
| --- | --- |
| V0 — Definition and variation | Explicit action, independent variations of every field, boundary terms, and agreement of equivalent Hamiltonian/Lagrangian descriptions |
| V1 — Constitutive law and static geometry | Exact μ=1−exp(−y), general-source quasistatic equation, independent Φ and Ψ, spherical/BTFR limits, measured G_N and regular high-acceleration recovery |
| V2 — Canonical closure | All primary/secondary/higher constraints, actual functional Poisson brackets, preservation to closure, first-/second-class separation and separate gravitational/matter counts |
| V3 — Matter and causal evolution | Full ordinary-matter Ward identity; physical, gauge-invariant initial/retarded response; auxiliary initial-data correspondence; no unacceptable instantaneous channel |
| V4 — Cosmology and stability | Expanding backgrounds and coupled scalar/vector/tensor perturbations; positive tensor kinetic term and c_T=c; ghost/gradient/strong-coupling analysis |
| V5 — PPN and empirical recovery | Derived β,γ,α₁,α₂,α₃, source/environment matching, dated primary observational bounds and one consistent measured Newton constant |
| V6 — Exceptional sectors and assembly | Separate k=0/k≠0, y=0/y>0, vanishing matter/clock charge, domains and boundaries; demonstrate overlap of all required parameter/solution regimes |

V1, V2 and V4 can run in parallel once V0 fixes their input. V3 and V5 must
use the reconstructed physical metric, not a convenience potential. Workers have
disjoint files; the coordinator compares action IDs and shared intermediate
equations before merging. Changing the action invalidates dependent proofs until
they are rederived; a same-directory name or successful rerun alone is insufficient.

### 12.5 Evidence levels must remain separate

- **Analytic derivation:** full statement, hypotheses and argument; independent
  mathematical review is required for load-bearing claims.
- **Exact computation:** a reproducible symbolic/exact identity or matrix result
  at the stated level. Derive ranks and constraints; a finite-mode matrix does not
  establish a functional operator's rank or boundary-domain closure.
- **Numerical/empirical evidence:** declared range, precision, refinements, data
  provenance, uncertainties, selection cuts and out-of-sample checks. It tests
  physical predictions; it is not a universal theorem or a derivation of a₀.
- **Lean-verified portion:** actual checked declarations with fixed definitions,
  proof dependencies and allowed axioms. An unfinished `.lean` file, unchecked
  `sorry`, or a proof of only a constitutive identity is not full-theory verification.

Start formalization with small, stable construction lemmas (for example the
exponential primitive and a correctly scoped canonical identity), then formalize
the essential bridges: action → equations, equations → constraints/observables,
and those results → the thirteen requirements. Inspect definition holes and
non-vacuity independently. Do not axiomatize an unproved physical bridge merely
to complete a Lean theorem. Formal proof checks mathematics, not whether a model
fits nature or is novel; those remain separate empirical and literature tasks.

### 12.6 Reproducible verification and the present implementation boundary

Pin the action, source dependencies, data and toolchain; record exact commands,
software versions, outputs, exit statuses and hashes. Execute every new scientific
script. Run independent Python jobs in parallel with bounded resources; avoid
multiple workers rewriting the same artifacts. Compare symbolic and numerical
routes when they check genuinely independent aspects of a claim.

For future Lean verification, separate trusted challenges from submissions,
check statement identity and allowed axioms, and use an additional kernel where
supported. The documented isolation path is Linux-specific; ordinary macOS builds
or development substitutes do not establish that guarantee. [Comparator][Comparator].

**This edit updates the blueprint; it does not install or execute Lean/Comparator.**
Neither `lean` nor `lake` was found on this task's PATH on 2026-09-08. No gravity
proof or external fluid proof is certified by this documentation change. The
reference repository's instructions are not silently advertised as commands for
a gravity Lean project that has not been created.

The final review must inspect each requirement and its actual proof/evidence,
including common action identity and nonempty admissible branches. No overall
PASS until all mandatory requirements are established. Optional a₀–Λ derivation
and any remaining phenomenological inputs must be labeled exactly as the spec
allows. Report files, commands, exits, the strongest result, OPEN/CLOSED status,
and the next concrete construction calculation; do not redefine a partial result
as the user's completed theory.

### 12.7 Attribution and source-check record

1. **OpenAI. *Finite time blowup for Navier–Stokes and Euler equations*.**
   *NavierStokesAndEuler* software repository (title as given in its README), revision
   `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`; README, ComparatorChallenges/README.md,
   and ComparatorChallenges/NavierStokes.json. Accessed 2026-09-08.
   [Repository at the cited revision][NS-repo]; [checking instructions][NS-checks].
2. **The leanprover/comparator project. *Comparator*.** Primary repository
   documentation, master version read 2026-09-08; sections on checking, additional
   kernels, definition holes and development. The documentation credits original
   development to Lean FRO. Its revision must be pinned before any future executed
   gravity proof audit. [Documentation][Comparator].

Source question: attribution of a verification workflow, not verification of a
fluid theorem or a novelty claim. The primary README and checking configuration
were inspected; no external proof build was run and no full source cache was
created. Fetching the reference `.lean` statement failed during this update, so
no theorem-content claim relies on that unsuccessful fetch. Classification:
**adjacent verification method, adapted constructively here**. This attribution
does not imply OpenAI endorsement, an equivalence between fluid and gravity
equations, or proof of the existence of the requested MOND theory.

[NS-repo]: https://github.com/openai/NavierStokesAndEuler/tree/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538
[NS-main]: https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/README.md
[NS-checks]: https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/ComparatorChallenges/README.md
[NS-config]: https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/ComparatorChallenges/NavierStokes.json
[Comparator]: https://github.com/leanprover/comparator/blob/master/README.md
