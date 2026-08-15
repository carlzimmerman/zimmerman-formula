# TASKS — 100 pre-scoped experiments, ranked by breakthrough potential within honesty

Format per task: **Hypothesis** · Method · PASS · KILL. Every task = one script in
`runs/tNNN_<slug>.py` via `qwenlib`, graded per PROTOCOL.md. Searches pre-register in
REGISTRY_FDR.md first (R7). Tasks ending in 0 carry the consolidation duty.

The single most valuable outcomes this list could produce, in order: (1) a forced
derivation of κ = ½ (or a theorem that none exists in a named class), (2) a
self-consistent second field that carries pressure without violating the stages-5/6/9
obstruction, (3) an in-repo reproduction of SZ21's Boltzmann background/linear system
at the pinned Q₀, (4) a decisive DR4 companion computation, (5) honest NULLs that close
doors permanently. A REFUTED/NULL verdict on any of these is a real contribution.

---

## A · The κ = ½ derivation programme (the crown-jewel open problem)

**T001 — Route catalog with forced coefficients.** Hypothesis: every published
dS-thermodynamic route (Milgrom 1999 Eqs 6–9; Pikhitsa 2010; Klinkhamer–Kopp 2011;
Verlinde-entropic; graviton-bath CTP from `project_crossover_master_formula`) forces a
coefficient ≠ ½ or forces none. Method: implement each route's coefficient algebra in
sympy; tabulate forced κ. PASS: table complete with each route's κ and its exclusion
status (2cH is excluded 15.6σ — committed). KILL: any route that actually forces ½ →
CANDIDATE, escalate immediately.
**T002 — ε_tot = 1/(32π) enumeration with FDR.** Hypothesis: the required ε_tot is not
special among ≤3-factor products of natural horizon fractions. Method: pre-register the
space {1/nπ, m/nπ : n ∈ 2..64 powers of 2, m ∈ 1,3}; count products hitting 1/(32π)
within the κ measurement window (±7.8% → ±15.6% on ε). PASS: report N_match vs
N_expected. KILL: none (NULL is informative).
**T003 — Graviton-bath cancellation, assumption-minimal.** Hypothesis: exactly one
assumption in the S_dS·GH² = π cancellation is load-bearing for κ² = 8πε_tot. Method:
sympy re-derivation; toggle each assumption; record which toggles move κ. PASS: the
assumption dependency table. KILL: cancellation fails to reproduce → flag the committed
memory as needing correction (DEFICIT-risk task).
**T004 — Response-function scan.** Hypothesis: no linear-response function (Boltzmann,
Wigner, Gaussian smearing σ ∈ [0.1,10]) in the dS-Unruh balance yields κ = ½ untuned.
Method: numeric balance integral per response; solve for implied κ. PASS: the scan
table + NULL/verdict. KILL: an untuned ½ appears → CANDIDATE + escalate.
**T005 — q-deformed Deser–Levin mirror.** Hypothesis: the Bose–Einstein route (11.1σ
low) reaches ½ only at a Tsallis q that nothing forces. Method: recompute the mirror
with q-statistics, q ∈ [0.5, 2]; find q(κ=½); search for any independent principle
pinning that q (pre-register the principle list). PASS: q* reported + forcing verdict.
**T006 — First-law smearing catalog.** Hypothesis: δS = δE/T on the dS horizon with the
a₀-line as EOM fixes κ only per smearing choice. Method: 5 named smearings; coefficient
per choice. PASS: table; KILL: choice-independent ½.
**T007 — Boundary-term ratios.** Hypothesis: κ² is not a ratio of GHY-to-bulk action
terms on the static patch at ≤3 combinations. Pre-register the combination space; count
hits vs chance. PASS: N vs baseline.
**T008 — Two-temperature interpolation family.** Hypothesis: within T_eff =
(T_U^n + T_dS^n)^(1/n), no n gives both the a₀-line form AND κ = ½. Method: derive the
implied g_obs(g_N) per n; fit n to the a₀-line; check implied κ. PASS: (n*, κ(n*))
reported both footings.
**T009 — The π-free theorem, formalized.** Hypothesis: κ is π-free (committed) AND any
derivation producing κ as a ratio of horizon areas/entropies must carry π — so the
derivation class "pure horizon-geometry ratios" is EXCLUDED. Method: formalize as a
parity argument in sympy over the generator set {A_horizon, S, T, ħ, c, G, Λ}. PASS: the
obstruction proof script or its refutation. This would be a genuinely new theorem-lette.
**T010 — κ-ledger consolidation.** Assemble KAPPA_LEDGER.md: every attempt above + the
committed history (TT-gauge kill, 5-variant 161.6× span, BE mirror) with one-line status.
Duty: refutation-check any CONFIRMED/CANDIDATE from T001–T009.

## B · β = 1 and the offset-DBI structure

**T011 — β from brane quantization.** Hypothesis: μ²Λ_D² = M⁴ is equivalent to an
integer/half-integer brane-tension condition in some normalization. Method: sympy; the
offset-DBI as tension×volume (committed: β=1 ⟺ pure brane action); scan normalizations.
PASS: equivalence table; KILL: none.
**T012 — β stability interior/edge.** Hypothesis: β = 1 is an interior point of the
ghost/gradient-stable range, i.e. stability does NOT select it. Method: K″>0 and c_s²>0
over β ∈ [0.25, 4] numerically. PASS: the stable interval; honest statement either way.
**T013 — a₀(z) under β ≠ 1.** Hypothesis: the CMB off-switch + forest constancy narrow β
to a computable interval containing 1. Method: generalize a0z_ratio_sq to β≠1 (numeric
background integration); apply the committed constraints (off at z=1090 to ≤0.006;
constant to <1% at z≤5). PASS: the allowed β interval, both ν₀ edges.
**T014 — Bounded-K uniqueness scan.** Hypothesis: among {offset-DBI, arctan, tanh,
Born-Infeld-log, cosh-cap}, only offset-DBI does all three jobs (w=−1 exact at minimum,
linear-ρ dust, bounded pressure) with ≤3 parameters. Method: symbolic checks per
candidate. PASS: the elimination table (this hardens "DBI selected" into "DBI unique in
class" or refutes it).
**T015 — Q₀-offset symmetry.** Hypothesis: a discrete symmetry Q → 2Q₀−Q protects the
offset minimum. Method: check K invariance; derive the domain-wall consequence; bound
wall abundance by the committed Ω ≤ 4.4e-7 excitation ceiling. PASS: symmetry verdict +
wall bound.
**T016 — z_t observables.** Hypothesis: z_t = ν₀^(−1/3)−1 ∈ [17,35] imprints a
computable signature on the dark-ages 21cm global signal timing. Method: a₀(z) enters
structure formation via the committed collapse-speedup factors (1.34–1.96×, declining
with z); estimate the shift of first-collapse redshift vs ΛCDM at both ν₀ edges. PASS:
signature size table (this creates a NEW falsifiable front if ≳ timing precision).

## C · The second field / the dust problem (open problem 2d — highest stakes)

**T017 — Obstruction theorem, machine-checked.** Hypothesis: stages 5+6+9's trio
(ρ = Q₀n charge lock; ρ+3p dynamics vs ρ+p lensing double-visibility; c_s² ∝ a⁻³ for
every ghost-free K) is airtight as stated. Method: re-derive each leg in sympy from the
action. PASS: 3/3 legs verified (or the crack, which would be huge — DEFICIT-risk on
the committed record, WIN-risk on the door).
**T018 — Second-field catalog: k-essence χ.** Hypothesis: a second shift-symmetric field
χ with p_χ = K_χ(X_χ) can carry cluster-scale pressure while evading all three legs.
Method: write the two-field action; check which leg kills it (the charge lock does not
apply to χ; double-visibility and c_s² still do). PASS: the named killing leg or a
surviving parameter region (CANDIDATE + escalate).
**T019 — Second-field catalog: vector condensate.** Same as T018 for a Proca-type χ_μ
(mind stage51's gated-Proca kill: y ∝ 1/a₀² explodes at recombination — check whether an
UNgated vector evades it).
**T020 — Second-field catalog: χ coupled through 𝒜(Q).** Hypothesis: a field entering
only via a₀²(Q,χ) shifts galaxy phenomenology without touching the CMB (bridge1's
order-counting protects the linear sector). Method: order-counting for the two-field
case; identify the first order at which χ appears. PASS: the order table. Consolidation
duty (T020): refresh OPEN_THREADS.
**T021 — Cell 1 (2,0) flow pricing, sharpened.** Hypothesis: the marginal-LIVE ~1.3
violation at pinned X survives the stage61 continuity density. Method: recompute the
stage54 B4 flow pricing with continuity ρ(r). PASS: the updated violation factor with
verdict LIVE/DEAD (this is a standing door — treat with both-ways care).
**T022 — Interior-reservoir transient.** Hypothesis: stage63's named escape (a
pre-existing interior charge reservoir draining without gating the inflow) cannot
supply >0.3× binding for >1 t_dyn. Method: extend the stage63 donor-cell solve with a
pre-loaded interior profile (three initial profiles); measure transient drain. PASS:
the transient table; KILL of the escape or its promotion.
**T023 — Anti-aligned RAR damage, quantified.** Hypothesis: the anti-aligned branch's
pile-up (98% retained) is RAR-fatal through local-a₀ suppression. Method: pile-up
density → S(r) → the stage59 B2 refit tolerance. PASS: fatal/plausible verdict (kills
the branch permanently or keeps it).
**T024 — The dust endpoint under weak-net drain.** Hypothesis: with Cell-3 transport
demoted, the central accumulation problem (stage 3's BH endpoint, falsified 5.8e5× vs
Sgr A*) stands unresolved. Method: recompute the endpoint mass under the continuity
inflow with the weak-net closure; state the standing tension honestly. PASS: the number
+ the honest sentence (DEFICIT-risk task — do it anyway; R2).

## D · Wide binaries / DR4 companions

**T025 — Perpendicular nonlinear two-body (coarse 3D).** Hypothesis: the perpendicular
finite-mass correction is also ≤1 (stage64's stated approximation). Method: 3D
finite-difference AQUAL solve at ONE separation (10 kAU), coarse (96³), both gates
(μ≡1, small-mass→B_perp=1.2598). PASS: B_perp,nl/B_perp reported with gate errors.
**T026 — Unequal masses.** Colinear exact pair at q = m₂/m₁ ∈ {0.3, 0.5, 0.7}, s = 10,
20 kAU; does B depend on q beyond the total-mass scaling the amendment assumed? PASS:
the q-table.
**T027 — Composed band from exact-pair tables.** Hypothesis: composing B(s,θ,q) over the
registered population statistics moves the band top by a computable amount. Method: use
stage64's table + T025/T026; the pipeline's population synthesis for weights. PASS: the
composed γ_v vs the frozen band (NOTHING FROZEN TOUCHED — escalate the comparison).
**T028 — Solar-circle overdensity, independent brackets.** Hypothesis: the dense corner
(1.47e4) is bounded by at least one independent local observable (ISM accretion rates,
Oort-comet flux stability, LISA-band stochastic limits — pre-register the list). Method:
one bound per observable, OOM. PASS: the bracket table (this is the ν₀-meter
prerequisite — the highest-leverage small task in this section).
**T029 — Chae-vs-Banik fork on shared mocks.** Hypothesis: the 19σ-Newtonian vs
γ=1.43±0.06 disagreement reproduces on a single mock catalog under the two published
selection/statistics choices. Method: build one mock (Amendment-10 truth), run both
analysis chains (simplified per their papers' stated cuts). PASS: the fork located
(selection? projection? statistic?). This defuses or sharpens the 13× systematic worry.
**T030 — 2(f) sign-falsifier power.** Hypothesis: the perpendicular-dominant anisotropy
sign (+0.0013–0.0046) is detectable at DR4 N~1157 at ≥2σ. Method: Monte Carlo with the
registered noise model. PASS: the power curve. Consolidation duty.

## E · CMB / Boltzmann staging (killing LITERATURE-INHERITED, piece by piece)

**T031 — DBI background integrator.** Hypothesis: the closed-form background (n ∝ a⁻³
exact, w = w₀/a³, c_ad² = 2w₀/a³) reproduces from direct ODE integration of the corpus
DBI K at pinned Q₀. Method: integrate; compare closed form to 1e-8. PASS: match both ν₀
edges.
**T032 — SZ21 fit reproduction, background level.** Hypothesis: the Cosh and Exp
published parameter sets reproduce their own μ = √(2K₂/(2−K_B))·Q₀ and background
w₀ against SZ21's stated values. Method: bridge1's verbatim equations. PASS: table
(first in-repo reproduction — partial de-tag at background grade only; say so).
**T033 — Linear system at one k.** Hypothesis: integrating the exact Eqs (7)–(12) from
bridge1 at k = 0.05 Mpc⁻¹, pinned Q₀, gives dust-like δ growth (Π → 0). Method: stiff
ODE integration, adiabatic ICs. PASS: δ(a) tracks CDM within 5% through recombination.
**T034 — E-equation stability.** Hypothesis: the anti-damping worry (stage 55's one
surviving item: Eq 12 second-order in α) does NOT produce a growing mode at pinned
parameters. Method: eigenvalues of the linear system from T033 across a ∈ [1e-4, 1].
PASS: max Re(λ) reported; growing mode → escalate immediately (existential if real).
**T035 — 3-fluid third-peak proxy.** Hypothesis: a photon-baryon-scalar toy reproduces
the fitted theory's third-peak-height sensitivity to Q₀ at the ≤0.5% level stage62
priced. Method: tight-coupling toy with the T033 field; peak-height vs Q₀ across the
pinned band. PASS: sensitivity curve vs the stage62 proxy (validates or corrects it).
**T036 — Share-proxy k-dependence.** Extend stage62 with the k²/(a²8πG̃ρ) factor
(stage57 D3: ~75 at the third peak): does any k make the mixing share exceed 1%?
PASS: share(k, Q₀) table.
**T037 — P(k) shape at pinned Q₀.** Hypothesis: the pinned band's μ⁻¹ = 0.07–0.4 Mpc
oscillation radius does not distort P(k) in the SDSS window beyond the published
residuals. Method: the r_C ~ (r_M μ⁻²)^(1/3) suppression estimate per k. PASS: the
distortion bound.
**T038 — Joint (ν₀, Q₀) consistency.** Hypothesis: the off-switch floor, the RAR
ceiling (continuity, Υ-refit), and the pinned Q₀ band have nonempty joint volume.
Method: 2D scan with the committed constraints as inequalities. PASS: the joint region
plot data + both-footing table.
**T039 — Recombination flow-y map.** Hypothesis: the stage54 velocity table's v_rec
values reproduce from linear theory (T033's θ at recombination). Method: compare.
PASS: v_rec from first principles vs the committed 12.6/23.1 km/s.
**T040 — Boltzmann-staging consolidation.** Which LITERATURE-INHERITED tags can honestly
step down a grade given T031–T039, which cannot. Write the tag ledger. Consolidation
duty.

## F · Galaxies / RAR grunt

**T041 — Radius-dependent suppression refit.** Hypothesis: the continuity S(r) profile
(not uniform suppression) degrades the SPARC RAR by less than the uniform-S estimate.
Method: apply S(r) from the stage61 continuity density per galaxy radius; Υ refit;
compare 0.108 baseline. PASS: dex table at both ν₀ edges (stage61 PART C's caveat done
properly — could tighten or relax the ceiling; both directions live).
**T042 — External-field environment estimator.** Assign each SPARC galaxy an external x
from group catalogs (pre-register the catalog choice); output the per-galaxy x_ext
table for T041/T043. PASS: table + method note.
**T043 — Per-galaxy ν₀ ceiling map.** Which single galaxy binds the ν₀ ceiling hardest
under T041's profile? PASS: the ranked list (targets future data).
**T044 — Gas-scale κ systematics.** Re-measure κ (a₀-line slope, gas-dominated subset)
under ±10% absolute gas-scale shifts; PASS: dκ/dscale (the committed unlock lever,
quantified).
**T045 — Dwarf spheroidals under local a₀ + EFE.** Hypothesis: the framework's local-a₀
+ EFE predictions for MW dSphs (pre-register 5: Fornax, Sculptor, Draco, Sextans,
Carina) match observed σ_v within modeling spread. Method: committed kernel + MW field.
PASS: the 5-row table both footings.
**T046 — M33 strong bench.** Full rotation-curve fit of M33 (the cleanest disc) at
anchored a₀, Υ free: residual profile vs the a₀-line. PASS: dex + structure verdict.
**T047 — RAR intrinsic-scatter decomposition.** Hypothesis: the 0.108 dex is consistent
with zero intrinsic scatter after observational errors. Method: hierarchical error
budget on SPARC. PASS: the intrinsic-scatter posterior interval.
**T048 — Tidal-dwarf predictions.** The framework predicts TDGs on the same RAR
(no-DM objects); tabulate the 6 published TDG velocity claims vs the kernel. PASS: the
table with per-object verdicts (shared-with-MOND; say so).
**T049 — z≤1 HI bTFR target list.** Assemble the concrete sample list (surveys, N,
expected errors) that reaches the 0.15 dex falsification bar from stage60. PASS: the
observing-case table (makes the bar actionable).
**T050 — Galaxy-section consolidation.** Consolidation duty + promote/demote.

## G · Clusters / lensing

**T051 — η spread under local a₀.** Recompute the cluster η window (kernel-labelled,
1.72–2.08 committed) with S(r) from the framework's own cluster-scale charge flow.
PASS: the updated spread, both kernels, both footings.
**T052 — a₀-bump matrix regression.** Re-run the committed bump health matrix
(c_T = 1, no-ghost, A_max ∈ [2.72, 4.46]×fiducial) from its scripts; verify current.
PASS: green table (regression insurance).
**T053 — KiDS in-transit pricing.** Stage63 C3's residual: the drained-charge transit
surface density in the 0.04–2.2 Mpc window vs the stage12 rejection band. Method:
Ṁ_drain ceilings × transit-time profile. PASS: Σ(r) vs the band (closes or charges
the weak-net closure).
**T054 — Bullet-class OOM.** Hypothesis: the framework's collisionless charge +
gas-offset lensing passes the Bullet at OOM (shared with all RMOND; say so). PASS:
the offset/mass-ratio table.
**T055 — Hydrostatic bias prediction.** The kernel implies a computable X-ray
hydrostatic-mass bias b(r) profile per cluster mass; tabulate vs the observed b ~ 0.2.
PASS: b(M, r) table both footings.
**T056 — R500 acceleration catalog.** For 20 named clusters (pre-register the sample),
g(R500)/a₀ — the committed 0.33–0.58 range verified on real data. PASS: the catalog.

## H · Symbol/beauty searches — FDR-armored (R7 mandatory; NULL expected and valuable)

**T057 — κ expression search, complexity ≤4.** Pre-register the generator set
{1,2,3,π,e,√·,/,·,+,−} and complexity measure; count expressions in the κ window
(0.551±0.086 at 2σ). PASS: N_match vs density baseline; the honest sentence. NOTE: ½
and 1/2π-family are already known members — the question is ONLY the surplus.
**T058 — ν₀-window expression search.** Same machinery for [2.14e-5, 1.77e-4] (a
4-decade target — expect enormous chance rates; the task exists to PROVE that).
**T059 — X-band search.** Same for X ∈ [106, 453]. Expected outcome: NULL with a big
baseline — which retires "X looks like <pretty number>" claims permanently.
**T060 — Ω_Λ numerology autopsy.** The retracted 3Z/(8+3Z): compute the chance
probability properly (density of complexity-≤4 forms within 0.04% of 0.685). PASS: the
autopsy number; closes the retracted claim with arithmetic. Consolidation duty.
**T061 — Tautology classifier.** Catalog every "beautiful identity" in the corpus
(2Z ratio, Z = √(8π/3)/κ, the 31112 conversion, etc.); classify TAUTOLOGY /
CONVENTION / CONTENT with a proof line each. PASS: the classified table (kills future
re-discoveries of tautologies).
**T062 — Two-scale uniqueness extension.** Extend the det = 2 uniqueness theorem to
two-scale laws a₀ = ξc√(Gρ_Λ)·f(ρ_m/ρ_Λ): what f survive the RAR + solar system +
clusters jointly? PASS: the constraint table (a genuine structural search with physics
gates, not numerology).
**T063 — κ-precision unlock map.** At what (M/L zero-point, gas-scale) precision does
the measured κ separate ½ from 1/2π-family at 3σ? PASS: the precision-requirement
contour (turns the κ question into an observing proposal).

## I · Structural / TOE-adjacent (bounded, honest)

**T064 — SME coefficient refresh under MG arm.** Recompute the induced s_μν under the
operative arm; verify against current gravity-sector bounds table. PASS: the bound
table (CPT-even-only theorem restated).
**T065 — GW subleading effects.** c_T = 1 exact; compute the next-order dispersion/
damping from the aether sector at K_B ≤ 0.25 vs LVK bounds. PASS: the margin table.
**T066 — Strong-field environments.** Hypothesis: a₀-local effects vanish near compact
objects (g ≫ a₀ everywhere). Verify the suppression exponent; bound any NS-timing
signature. PASS: the bound (a safety check that should pass; if it doesn't, escalate).
**T067 — Energy-conditions audit.** NEC/WEC/DEC for the full action on FRW + halo +
tilted backgrounds (symbolic). PASS: the condition table (feeds the health matrix).
**T068 — Characteristics/hyperbolicity at tilt.** Hypothesis: the QS F(Y,Q) system
stays elliptic/causal at finite tilt w ≤ the collapse values. Method: principal-symbol
eigenvalues over (y, w) grid. PASS: the domain map — THIS IS A HEALTH-MATRIX CELL
(stage51 owed; the single most-requested structural item).
**T069 — Health-matrix assembly.** Collect T067/T068 + committed results into the
perturbation health matrix skeleton with named EMPTY cells. PASS: the matrix file with
every cell sourced or marked owed.
**T070 — Cosmological tensor modes through DBI background.** Integrate h_× through the
a₀(z) transition; verify no feature at z_t beyond 1e-6. PASS: the bound. Consolidation.

## J · Data-facing new fronts

**T071 — MUSE Υ-degeneracy protocol.** Write the analysis protocol that would separate
a₀ evolution from M*/L at z ≤ 0.5 (pre-register estimator); compute required N. PASS:
the protocol + power table (the McGaugh-flagged degeneracy, made quantitative).
**T072 — JWST high-z rotation curves leverage table.** Which published z > 3 curves
reach y ≲ 1? Tabulate their a₀(z)-law leverage (expected: none decisive; prove it).
**T073 — SN-Ia host-step power refresh.** Recompute the decisive-test power with
current public sample sizes; PASS: power vs the committed 18%.
**T074 — Forest constancy at pinned parameters.** Re-run the b-cutoff comparison at
pinned Q₀/ν₀ (the corrected 0.4–0.9σ machinery); PASS: updated σ both footings.
**T075 — Redshift-drift discriminator.** w = −1 exact vs DESI-CPL best fit: ELT
redshift-drift signal difference over 20 yr. PASS: the ns-precision requirement table.
**T076 — Local-group timing.** The timing argument under the kernel: M_LG implied;
compare abundance expectations. PASS: the number + tension statement either way.
**T077 — Beyond-2.2-Mpc lensing forecast.** Predicted stacked ΔΣ(r) to 10 Mpc at
pinned parameters; which survey (Euclid/LSST year-N) reaches 3σ on the 1/r tail?
PASS: the forecast table.
**T078 — Dark-ages 21cm timing.** T016's signature vs planned lunar-farside
sensitivities; PASS: detectable/undetectable verdict per mission class.
**T079 — Cluster-scale ν₀ meter.** Does any cluster observable (BCG wobble, splashback
radius) carry the local-a₀ suppression signature at the ν₀ ceiling? OOM per observable
(pre-register 4). PASS: the leverage table.
**T080 — Fronts consolidation.** Rank all J-section fronts by (leverage × data
availability); write the top-3 into OPEN_THREADS. Consolidation duty.

## K · Verification infrastructure (do these early; everything else leans on them)

**T081 — Full-corpus CI runner.** Script that runs every `nbody_2026/stage*.py` +
`real_research/reviews/*.py` and reports green/red with runtimes. PASS: the report
(catches bit-rot; run weekly).
**T082 — Frozen-file guard.** Script that hashes PREREGISTRATION_DR4.md + all
*_HASH.txt and fails if any differ from the committed digests. PASS: green run.
**T083 — DO-NOT-CITE linter.** Grep-based linter over qwen_38_experiment/ for the R8
retracted phrases; PASS: clean run on the current folder; wire into the loop (run
before every ledger append).
**T084 — Units checker.** Add dimensional-analysis helpers to qwenlib (quantity tuples
(value, [m,kg,s] powers)); unit-test on 10 committed formulas. PASS: 10/10.
**T085 — Kernel-library regression tests.** Pin qwenlib against 12 committed numbers
(tensor 1.4732/0.3674/1.2598; γ asymptotes 1.2138/1.2586; S(1.47e4, ceilings); a₀(z)
at z=1090 = 0.002–0.006; …). PASS: 12/12 (this file becomes the canary).
**T086 — Ledger integrity checker.** Parse LEDGER.md; flag rows with missing risk
fields, unfilled verdicts, or search rows without REGISTRY_FDR entries. PASS: clean.
**T087 — Refutation-duty tracker.** Script listing every CONFIRMED ledger row without a
linked refutation attempt. PASS: the list (the adversarial loop's memory).
**T088 — Negative-results museum.** Collect all REFUTED/NULL rows into
NEGATIVE_RESULTS.md grouped by door-closed. PASS: the file (this is publishable
material — the corpus's best tradition).
**T089 — Escalation digest.** Script that formats ESCALATE.md into a one-page digest
for Carl with dates and blocking tasks. PASS: the digest.
**T090 — Infra consolidation.** Run T081–T089 end-to-end; fix breaks; consolidation
duty.

## L · Exploratory — the "beautiful math with teeth" section

**T091 — Sector-duality search.** Hypothesis: a field redefinition exchanges the Q
(dust/CMB) and Y (MOND/galaxy) sectors, formalizing "the dark-energy triumph and the
galaxy problem are the same property." Method: sympy transformation ansatz space
(pre-register: 6 families); check action invariance. PASS: the family table; any exact
duality → CANDIDATE + escalate (this would be a genuinely deep structural result).
**T092 — Emergent-κ from averaging.** Hypothesis: volume-averaging a₀²(Q) over a
realistic density field renormalizes the effective coefficient by an O(1) factor —
could ½ be an averaging artifact of a derived 2? Method: average the committed a₀²(Q)
over lognormal density fields calibrated to σ₈; compute κ_eff/κ_bare. PASS: the factor
distribution (if ¼ appears naturally, that is the single most exciting number this
list can produce; if not, an important door closes).
**T093 — Holographic budget cross-constraint.** Impose dS entropy + the a₀ relation +
Ω_Λ as one constraint system; solve for what additional relation WOULD close it; state
it as a falsifiable target (NOT as a claim). PASS: the target relation + its current
observational status.
**T094 — Offset-DBI soliton spectrum.** Kinks between Q₀ vacua: mass per area, cosmic
abundance bound from Ω ≤ 4.4e-7, lensing signature bound. PASS: the bound table.
**T095 — Swampland catalog.** μ²Λ_D² = M⁴ and the field range vs distance/de-Sitter
conjecture bounds — catalog only, no verdicts (the conjectures are not data). PASS:
the catalog with every entry labelled CONJECTURE-REFERENCED.
**T096 — BH thermodynamics with local a₀.** Hypothesis: horizon thermodynamics is
unmodified to O((a₀ r_s/c²)¹) — compute the leading correction exponent and bound it
with EHT/LVK. PASS: the exponent + bound.
**T097 — Superfluid-MOND crosswalk.** Map the corpus condensate onto Berezhiani–Khoury
phase-diagram axes; identify ONE observable where the two frameworks differ at >2σ
reachable precision. PASS: the discriminating observable + required data.
**T098 — Kernel-space joint scan.** Over a 2-parameter kernel family containing Route A
(pre-register the family), which region survives RAR + solar-system + wide-binary
Amendment-10 band jointly? Is Route A interior or edge? PASS: the region map (edge =
fine-tuning worry, interior = robustness — both informative).
**T099 — The ν₀ measurement assembly.** Combine every ν₀-sensitive computed front
(RAR ceiling T041, DR4 meter, forest T074, 21cm T078, cluster T079) into one
likelihood-style table: what jointly measures ν₀ first? PASS: the ranked table.
**T100 — Grand consolidation.** Re-read the whole ledger. Write FINDINGS.md: every
CONFIRMED result that survived refutation, every door closed, every escalation
pending; regenerate OPEN_THREADS ranked by (evidence surplus × decisiveness); propose
the next 100 tasks as one-liners. PASS: the file. This is the handoff artifact for
Carl and the frontier model.

---

## M · The million-monkeys programme (T101–T120) — engine-driven, FDR-armored

The engine is `mm_search.py` (bounded RAM, deterministic, chance baseline built in —
the session just launches it and records the 3-line summary). Targets: `targets_sm.py`
(24 high-precision SM/cosmology numbers) + `targets_zimmerman.py` (the framework's own,
tautology-graded). STANDING PRIOR, stated before any search: the corpus's number-field
obstruction (Z carries √π, flavor data are algebraic) and the walled SM bridge — searches
are PERMITTED, but a surplus is a CANDIDATE-ESCALATE, never a claim. Symmetric honesty:
no candidate is discarded by authority either — the surplus number decides.

**T101 — Verify the targets table.** Cross-check every `targets_sm.py` entry marked
(VERIFY) for internal consistency (ratios vs masses, sin² vs angles); note any entry
needing a PDG re-check in the ledger. PASS: the consistency table.
**T102–T108 — Base-pack sweeps.** One task per group, `--pack base --cmax 5`:
couplings (alpha_inv, alpha_s_MZ, sin2thW_msbar); mass ratios (mmu/me, mtau/mmu, mp/me,
mn/mp); CKM (lambda, A, rhobar, etabar, delta); PMNS (three sin² + delta); EW shape
(mW/mZ, mH/v, yt); cosmology (ns, omega_b_h2, omega_c_h2); koide_Q + one rerun of each
surplus>3 target at cmax 6. Record every surplus, NULL expected almost everywhere.
**T109 — Controls audit.** Positive control: koide_Q must find 2/3 with surplus >> 1
(it does — prebuilt smoke test). Negative control: run 5 CONVENTION-grade targets and
confirm the engine REFUSES them. PASS: both controls green.
**T110 — MM consolidation.** The full surplus table across T102–T108 with a Bonferroni
line (24 targets × packs); anything jointly significant → ESCALATE. Consolidation duty.
**T111–T115 — Zimmerman-pack sweeps.** The same target groups with `--pack zimm`
(generators include κ=½, Z, √π, R_dm): does ANY SM number prefer the framework's
constants beyond chance? This is the honest version of the retracted Z²-numerology —
same question, with the trial counting the original never had.
**T116 — Geometric angles.** `--pack angle` (adds φ golden ratio) on the CKM/PMNS
angle targets, plus a scripted catalog of exact polyhedral/platonic solid angles and
arctan(p/q√n) forms vs the measured angles, FDR-counted. PASS: the surplus table.
**T117 — Relations among SM constants only.** Targets = SM numbers, generators = other
SM numbers (no framework input): the machinery must rediscover known structure (Koide;
sin²θ_W vs mW/mZ: on-shell sin²θ_W = 1−(mW/mZ)² is a DEFINITION — the engine must flag
it as such, the classifier's negative control). PASS: known structure found AND labelled.
**T118 — Framework numbers at depth.** κ_meas, ν₀ edges, Q0 edges as targets, base pack,
cmax 6 (extends T057–T059 one complexity deeper with the engine). NULL expected; record.
**T119 — The obstruction test on winners.** For every hit with surplus ≥ 3 anywhere:
classify its expression algebraic vs transcendental-π-carrying; test compatibility with
the number-field obstruction; write the verdict per winner.
**T120 — FINDINGS_MM.md.** The programme's honest summary: every surplus, every NULL,
the controls, the Bonferroni verdict, and what (if anything) earns escalation to the
frontier-model harvest. Consolidation duty.

## N · The seeded-idea stream (dispatcher-driven, no fixed numbers)

`idea_seed.py` throws framework objects × SM constants × mathematical motifs into short
random paragraphs (deterministic per id). The dispatcher (`next_duty.py`) routes three
session types automatically: INTERPRET (fresh context deciphers ONE seed into one
falsifiable hypothesis), BLIND REFEREE (a later fresh session grades the interpretation
reading ONLY that file — PURSUE/DISCARD), PROMOTE (a passed idea becomes a task spec in
TASKS_SEEDED.md with full PASS/KILL + FDR discipline). Ideas enter the ledger like
everything else; DISCARD is a success. Seeds auto-replenish every ~6 duties.

## S · The symbolic-regression stream (T121–T130) — forms from data, verified

The engine is `sr_engine.py` (GP over expression trees, numpy-only, deterministic;
train/holdout split + shuffled-target nulls built in — the FDR analog for regression).
Data lives in `data/` (exported from committed pipelines only; never fabricate a table).
A discovery needs BOTH: holdout performance competitive with the named baseline AND real
R² far outside the shuffled-null band. Engine smoke test (committed): from the real
3,389-point SPARC set it recovered √(x(x+√(3.24−x))) — a₀-line-class structure, holdout
RMSE 3.0434 vs the a₀-line's 3.0435, null R² ≈ 0. The machinery finds real laws.

**T121 — Positive control at full budget.** `--gens 80 --pop 500 --nulls 3 --baseline
a0line`, seeds 0,1,2. PASS: best expression's holdout RMSE within 1% of the a₀-line and
equivalent structure (sqrt of quadratic-plus-linear); record all three seeds' winners.
**T122 — Beat-the-law hunt.** Same data, complexity cap raised (edit parsimony 0.0005),
5 seeds: does ANY form beat the a₀-line holdout by >2%? NULL expected (anchoring is
cost-free — a committed result); a robust winner → CANDIDATE-ESCALATE (likely Υ
systematics, say so). Run BOTH footings (re-export data at a0_alt for the second).
**T123 — Residual structure.** New dataset: residual r = y − √(x²+x) vs x. SR it. PASS:
the null verdict (r is noise) or the found form with its null band; either is banked.
**T124 — BTFR blind recovery.** Export (M_b, V_flat) per galaxy from the committed
pipeline into data/btfr.json; SR V(M) with baseline btfr (V ∝ M^0.25). PASS: the quarter
power found blind; KILL of the export if the pipeline columns are ambiguous — BLOCKED.
**T125 — Weak-lensing extension.** If the stage12 KiDS profile data exists in-repo,
export (R, ΔΣ or g) to data/ and SR the 40 kpc–2.2 Mpc relation; does a₀-line structure
hold at extended range? If the data is not in-repo: BLOCKED, name the file needed.
**T126 — The required dust-pressure law.** Build the constraint table for open problem
2d from committed numbers (what p(ρ) a second field would need at cluster cores vs what
the obstruction trio forbids); SR the required form; verdict: does ANY closed form
satisfy both? This is a derived-data regression — label it so.
**T127 — a₀(z) minimality.** Generate the derived-law curve from qwenlib.a0z_ratio_sq
at both ν₀ edges; SR it (features z). PASS: the engine finds a form of complexity ≤ the
closed form's (√ of rational in (1+z)⁶) — the β = 1 law is the minimal description; a
simpler equivalent found → CANDIDATE (genuinely interesting).
**T128 — SM relations from data (walled-bridge prior in force).** data/leptons.json =
the three charged-lepton masses; SR the Koide combination blind (POSITIVE CONTROL: the
engine must find m-structure equivalent to Q = 2/3). Then the quark sector and mixing
angles as generation-indexed tables. Any surplus → ESCALATE only; the atomos null and
the number-field obstruction are the standing priors, stated in the ledger row.
**T129 — Cross-front form transfer.** Mechanical comparison of all winner expressions
from T121–T128: does any structural motif repeat across unrelated fronts? PASS: the
comparison table (this is the bridge hunt, done as tree-matching, not vibes).
**T130 — FINDINGS_SR.md.** Controls audit + every verdict + escalations; consolidation
duty.
