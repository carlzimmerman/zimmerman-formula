# CFG231 — Door 12: the covariant and elastic completions of emergent gravity against the CFG44 target. FROZEN CRITERIA (phase 1)

Written 2026-09-29, before any script of this lane. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure or an appended erratum, never as an edit. No physics script has been written or run in phase 1. Every number marked [H] is arithmetic done by hand from record formulas and is itself to be checked in phase 2. κ = ½ is FITTED. Nothing here says the theory is closed, and nothing says any data favour the framework. A scoped no-go is a valid and likely answer; a pass is not the goal.

**Evidence-class tags (a requirement or a claim is never stated more strongly than its tag).**
- **[T]** Lean theorem in `fable_independent_2026/lean_2026/ChainCert` (commit b8d8b1ba5; `verify_chain.sh` PASS, 219 theorems, only `propext`, `Classical.choice`, `Quot.sound`, no `sorry`, no `axiom` declaration; MUTATE=1 fails as required). Only with its stated premises (§0.3).
- **[S]** a committed script output in the record, cited by lane and commit. Not re-run by this lane in phase 1.
- **[R]** a documentary statement of the record (README or status file), cited by file.
- **[H]** hand arithmetic done in this file, unverified until phase 2.
- **[M]** from memory, unverified (literature facts).
- **[D]** a declared choice of this lane.

**Scoping notes received mid-task.** (1) A first message (build on the status documents, cite the ChainCert ownership and no-EFE theorems with their exact premises, mark the Action/Dimension/FluidLink batch pending, list CFG250/251/252 as in flight elsewhere) was labelled for another lane and sent here by mistake; the coordinator confirmed it is harmless where folded in (§0.3, §0.4, §0.5). This lane is CFG231 (door 12). (2) The scoping that belongs to this lane: grep the repo for earlier scored or retired covariant emergent-gravity work, so door 12 does not repeat it; add a "prior work inherited" section (§0A); state the literature claims (authors, year, field content, form of the elastic response) each marked from memory for the data chat (§0B); keep the record-tension items (§9). Revision 2 of this file (2026-09-29, before any script) folds that in; the changes are the new §0A and §0B, a new variant B4 with an admissibility line in G1, a class-V de Sitter stability item in G5, and additions to §3, §4, §5, §8 and §9.

## Forking paths and multiplicity (stated first)

- The menu of variants below was written **knowing the target** (CFG44), **knowing door 2's result** (CFG117: point-mass ratio (1 + x)/x) and knowing the CFG44 B1 N5 output (the P2 law's own phantom departs from the exponential-sphere target by a charge-function ratio R up to 2.28 to 2.48) [R, S]. The hand estimates in §3 were made after reading those numbers. They are not blind.
- Earlier scored or retired treatments of Verlinde / Hossenfelder in the repo were read before freezing (§0A). Several of them are pre-campaign, use other gates (Route 3's five gates, not G1–G5) and other recipes (Q₂ from an assumed external field); none of their numbers is imported as a result here.
- Cells scored: 8 scored variants × 2 geometries × 7 masses × 2 choices of H × 2 footings, each on a 3001-node grid. No pass line is pooled across variants. A variant that passes one normalisation and fails another is reported as a split, never as a pass.
- Nothing is scanned to make a gate pass. The variant menu is finite and fixed here; the only numerical inputs are the declared ones in §5.

---

## 0. What is tested, and what the record already says

### 0.1 The question

Door 12 is the part of door 2 that CFG117 listed as untested: Hossenfelder's covariant version, later formulations, and non-spherical systems (CFG117 README, "Untested hypotheses") [R]. CFG117 scored Verlinde's formula as a SHAPE test only, at a₀ = a_V, and found the ratio C_V/C_target = (1 + x)/x for a point mass [S: bb504274c]. Door 12 asks:

- **12a** — does a covariant vector-field completion (a vector in de Sitter that drags on baryons and carries a Λ-tied scale) supply the missing object C(r) = ρ_c r³ g_tot = (a₀/4π) M_b(<r) (CFG44; `closure_map/GAPS_1_2_JOINT_STATUS.md`) as a DERIVED mechanism?
- **12b** — the elastic dark-energy phenomenology (volume-law entropy, a_V = cH/6): does any reading of it, with or without the derivative term and the onset gate, reproduce the target's shape, and is its normalisation compatible with the Λ tie?
- **12c** — if a covariant action admits a free constitutive (interpolating) function, does a function exist that restores the target's r⁻¹ inner regime, and can that function be DERIVED rather than declared?

Gates: G1–G5 of `closure_map/TEN_DOORS_GATES_2026-09-29.md` (5ef77ea09), weakened nowhere; this file adds lines only. The dark density plays the role of ρ_c exactly as in CFG117: ρ_D = M_D′/(4πr²), g_tot = G(M_b + M_D)/r². Per CFG44 the whole content of G1 is one function of radius with no dynamical origin in the record [R: GAPS_1_2_JOINT_STATUS lines 1, 6, 12].

### 0.2 Record cited, not re-derived (each read for this file; classes as the files state them)

| item | what it says that bears on door 12 | class |
|---|---|---|
| `closure_map/TEN_DOORS_RESULT_2026-09-29.md` incl. the appended referee note | door 2 row: G1 F, G2 U, G3 U, G4 P (count only), G5 F; no referee lane for door 2; "Hossenfelder's covariant Lagrangian" listed as not tested; the cross-door reading (the missing object must itself carry an acceleration scale) is a READING, not a theorem; the menu was written knowing the target | [R] |
| CFG117 README + `CFG117_FROZEN_CRITERIA.md` (b09ca1480; lane bb504274c) | C_V/C_target = (1 + x)/x exactly; spheres 10–16 at x = 0.1; κ_V = √(8π/3)/6 = 0.4824 (H_Λ), 0.5829 (H₀); a_V/a₀ = 0.9650 canonical / 0.7985 alt (H_Λ), 1.1660 / 0.9648 (H₀); Hees et al.: perihelia off by seven orders; no action, so G2/G3 UNDEFINED | [S], literature facts inside it [M] |
| `closure_map/GAPS_1_2_JOINT_STATUS.md` | the target is exact; no local or EOS closure produces it; what is left is a nonlocal, non-adiabatic exchange keyed to the enclosed baryon mass; Gap 2 reduces, as an IDENTIFICATION not a theorem, to Gap 1 (ownership); a construction giving C(r) with no bound-only switch would falsify that identification | [R] |
| `closure_map/GATES_STATUS_2026-09-29.md` rows 5.01, 5.02, 5.11, 5.12, 5.13 | no action produces B; 5.12 says the target gives the inner profile "exactly for P2" (see §9 for a wording tension with B1 N5); the Unruh route retired (CFG47) | [R] |
| `closure_map/SHARED_VS_SPECIFIC_2026-09-29.md`, `CLAIMS_AUDIT_2026-09-29.md` | door 2 addenda copy the CFG117 verdict; nothing further on Hossenfelder | [R] |
| `closure_map/DOOR11_RESULT_2026-09-29.md` and addenda 1–2 | timelike-flow, aether-type vector classes (11C-a/b/c: CFG172, referee CFG188; 11C-d: CFG172D) are scoped no-gos; for 11C-a any kernel within the G1 band with (yq)′ ≥ 0 keeps a Solar-System tail ≥ 0.282 a₀ (a theorem GIVEN that premise, CFG188); the P2 tail gives Q₂ 6.3e3× the bound; a cosmological constant cannot flow; the no-EFE theorem is Lean-certified (addendum 2, item 4) | [R] |
| `data_assembly/DOOR11_LITERATURE_2026-09-29.md` (the only emergent-gravity literature file; a source to check, not an authority) | Verlinde 2017 [ABS]; Lelli–McGaugh–Schombert 2017 [ABS]: matches the RAR only with low M/L and predicts unobserved radius-correlated residuals; Hees–Famaey–Bertone 2017 [ABS]: perihelia off by 1e7; **Hossenfelder 2017, PRD 95, 124018, arXiv:1703.01415 [ABS]: "a vector field in de Sitter that drags on baryons and also gives dark energy"** (abstract level only; nothing else about her Lagrangian is in the record); Tuveri & Cadoni 2019 [ABS] | [ABS] via the data chat |
| B1 N5 (`CFG44_fluid_target/B1_target_and_hydrostatics.out`) | the P2 law's OWN phantom has charge function R = 4πr³ρ_ph g/(a₀M_b) = 1 exactly for a point mass but R in [1.000, 2.279] (compact exponential sphere) and [1.000, 2.484] (diffuse) on extended profiles | [S] |

### 0.3 The two new Lean items, with their exact premises (ChainCert `Ownership`, b8d8b1ba5; not upgraded)

1. **No-EFE theorem [T].** Definition: a pointwise map F is EFE-free when F(z + z_e) − F(z_e) = F(z) for all internal z and external z_e (on the physical ray: z, z_e > 0). Statements: a continuous EFE-free map between real topological vector spaces is continuous linear (`noEFE_continuousLinear`; ℝ³ in `noEFE_linear_R3`); on the ray continuity is needed only on (0, ∞) (`noEFE_linear_ray`). For a kernel with ν(y)√y → 1 as y → 0⁺, the law g_N ↦ ν(g_N/a₀) g_N with a₀ > 0 is NOT EFE-free, even on the ray and without continuity (`deep_not_efeFreeRay`, `law_not_efeFreeRay`; instances ν_mono, ν_β at β = 1, and √(1 + a₀/g_N)); the vector law ν(‖g_N‖/a₀) g_N is not EFE-free on any nontrivial real normed space (`vecLaw_not_efeFree`). **Scope stated by Lean:** pointwise (algebraic, QUMOND-type) laws only; AQUAL/QUMOND field equations are not formalised, and the theorem says nothing about them beyond this pointwise reading. It is mathematics, not an empirical statement.
2. **Ownership is non-local [T].** Premises: a hierarchy H with a top-level system i (parent none) and an owned system j (parent some p); g_N ≠ 0; ν(g_N/a₀) ≠ 1. Conclusion: the two get different internal accelerations with the same internal and external fields (`ownership_distinguishes`), so no function of (internal field, external field) reproduces the ownership rule (`ownership_not_field_local`). A kernel with the deep limit is ≠ 1 somewhere (`deep_kernel_ne_one`). NOT certified: that nature realises ownership; that any action produces it; which systems are owned (the hierarchy is an input).

**How door 12 uses them (no more than this).**
- The bridge from [T] to a field theory is a step of mine, class [H]: a LOCAL covariant action's static spherical law is a function of the local Newtonian field, so it is not the ownership rule. The scored classes K1–K3 (§1.3) are pointwise laws with ν(y)√y → 1 (hand check [H]: K2 gives √y + 1, K1 gives √(1 + y), K3 gives √y/2 + √(y/4 + 1); all → 1), so the Lean premise holds for them and each has an EFE as a pointwise law.
- Door 12 can therefore bear only on Gap 2's density profile of an ISOLATED top-level system; it cannot bear on Gap 1's ownership. That is stated as a diagnostic (D-EFE), not a gate.

### 0.4 In flight elsewhere (NOT duplicated here; no result of theirs is cited)

| lane | subject | status here |
|---|---|---|
| CFG250 | mass-free outer-slope a₀ at KURVS | in flight elsewhere |
| CFG251 | door 11D, including "set at turnaround" as a possible ownership mechanism | in flight elsewhere |
| CFG252 | a timescape / void-wall reading of dark energy against the a₀ tie | in flight elsewhere |
| ChainCert Action / Dimension / FluidLink batch (peer's side) | an AQUAL action to the kernel in spherical symmetry; dimensional analysis on monomials; the fluid cap's a₀ linked to the chain's a₀ | **pending, not a result.** The files exist in the peer's working tree but are not in commit b8d8b1ba5's README, so they are not cited. `Action` is close to 12c; if it lands before phase 2 the orchestrator may append an addendum, and this lane changes no line of this file because of it. |

### 0.5 Screening list (what this lane does NOT repeat, so a reader can see the boundary)

Timelike unit-vector / aether / khronon flows (11C-a/b/c/d: CFG172, CFG172D, CFG188), nonlocal metric gravity (door 9), mimetic (door 10), dipolar (door 3), superfluid (door 4), interacting vacuum (door 8), CFG250, CFG251, CFG252, and anything in the pending ChainCert batch.

---

## 0A. Prior work inherited (repo grep for Hossenfelder, about 51 files, plus a name search for the covariant-MI paper; each file read for its Hossenfelder / Verlinde content only)

Rule for this section: a file's own verdict is recorded with its own evidence class; door 12 inherits a statement as a CLAIM TO CHECK or as context, never as a result of this lane. No number below is imported into a pass line.

| # | file (repo-relative) | what it is, its verdict | inherited | NOT inherited |
|---|---|---|---|---|
| 1 | `campaign_fresh_gravity/CFG117_verlinde/README.md`, `CFG117_FROZEN_CRITERIA.md` (b09ca1480; lane bb504274c) | door 2, Verlinde's formula as a SHAPE test at a₀ = a_V: scoped no-go on G1 (0 of 16 cases; point mass (1 + x)/x); G2/G3 UNDEFINED; G4 P (count only); G5 F (Hees et al.). No referee lane. Lists "Hossenfelder's covariant Lagrangian, later formulations, non-spherical systems" as untested [S, R] | the formula and its analytic point-mass ratio as control C3 (re-derived, not imported); the a_V/a₀ table (cited as [S] in §1.5, recomputed in A7); the fact that door 12 is the item CFG117 left untested | the script outputs; the H₀/H_Λ verdicts as verdicts of this lane; CFG117 scored only Verlinde's algebraic formula, never an action |
| 2 | `real_research/VERLINDE_DEEP_DIVE_2026-06.md` (2026-06; "papers fetched 2026-06-28") | comparison of the framework with Verlinde. Says Hossenfelder 2017 wrote a covariant Lagrangian (a vector field on de Sitter dragging baryons) that reproduces Verlinde's equations in the weak-field / static / spherical / negligible-imposter-mass limit, and that in that form **the MOND interpolation function is unnecessary and its one free parameter is fixed**; partial (limit-only, a de Sitter-recovery error later corrected, an extra integration constant appears), disputed (Pardo, arXiv:1706.07854). Verdict: both it and the framework are at "scale + deep-MOND limit, not a controlled transition"; Verlinde slightly ahead on the covariant front [R; literature facts inside are the file's own, [M] for this lane] | the literature claims as items L2–L7 of §0B, to be checked by the data chat; the statement that her covariant form has NO free interpolating function (this changes how 12c is scoped, §1.2 note) | any credit statement ("ahead", "only serious covariant completion"); the framework-side comparison |
| 3 | `real_research/reviews/verlinde_foundation_stress_test.md` (v12, 2026-05-31) | stress test of Verlinde as a TOE foundation: no covariant Lagrangian for Verlinde's own text; Hossenfelder's covariant version "initially failed to recover the de Sitter solution (an error, corrected), and small perturbations around de Sitter grow, so the state is not stable"; Dai–Stojkovic contested; no CMB framework; clusters short by ~2. Verdict: emergent-gravity foundation is the weakest link [R; file says "verified rather than from memory", not re-checked here] | the de Sitter-instability claim as item L5, converted into an explicit G5 sub-item of this lane that I DERIVE for class V (§2, G5 (v)), not import | the conclusion about the TOE narrative; the cluster and CMB remarks (not gates of this lane) |
| 4 | `real_research/reviews/toe_law/agentP_verlinde_coefficient.md`, `agentH1_candidate_matrix.md` (§2.8) | coefficient audit and candidate matrix. CEG: "dead at the solar system" (Hees et al. ×10⁷), metric-level so lensing is affected, the transition keys to g_N AND dg_N/dr; covariant CEG "exists but its dS background is perturbatively unstable (banked)"; no CMB framework; cluster residual ~2× survives; scored 1/8 [R] | context for G5 and for D2; the observation that the transition depends on dg_N/dr (which is the derivative term of B1) | the matrix scores; the "banked" instability is not treated as established |
| 5 | `qwen_claude_field_theory/closure_2026/route3_entropic_gravity_2026.py`, `route3B_entropic_independent_2026.py` ("Route 3", pre-campaign gates) | Verlinde standalone against five Route-3 gates (amplitude law, force screening, Q₂ and 1-AU monopole, theoretical health, no double count): DEAD as a survivor, 1 of 5 gates. Contains: **Theorem V1** (sympy: with the differentiated form M_D = r√(a M_b/G), Verlinde's M_D equals the TOTAL deep-MOND effective mass, M_D = M_ph + M_b); the "covariantisation dilemma" (an action puts Verlinde back inside the hypotheses of the arm-level Q₂ proof and of a k-essence static-stress theorem: "no action → gate 4 undefined; action → Q₂ at 17× the ceiling"); Q₂ computed with an ASSUMED external field g_ext = 1.9–2.6 a₀; Hossenfelder 2017 named as "prior art not verified against the paper" [S/R] | (i) the reading behind V1 becomes variant **B4** (Verlinde's M_D read as the TOTAL mass, not an added mass), scored here with an added admissibility line (§2 G1); (ii) the dilemma is a hypothesis to be tested: does class V, once an action exists, leave G3/G5 as the Route-3 lane predicted (§3) | its verdict as a verdict of door 12; the gates (different from G1–G5); the Q₂ recipe (an assumed-EFE recipe; this lane uses CFG7 H1 and reports the other only if cheap, never pooled); the "a₀(z) collision" with a framework a₀(z) law of "0.0060 at recombination" (a pre-campaign number; the campaign's own a₀(z) statement is the flat law with the ∝ H(z) rival, and a_V ∝ H(z) is only REPORTED here as D1); "Theorem 1 (k-essence static stress)" is a theorem for a single SCALAR with a static radial profile (`t1_kessence_pt_theorem_2026.py`); it is not applied to a vector, and A3 computes the vector's own static stress components instead |
| 6 | `opus_48_extended_research/papers/COVARIANT_MI_FIELD_THEORY.md` (v7) | the framework's OWN covariant field theory of modified inertia (khronometric + memory-field sectors), not a covariant version of Verlinde. Hossenfelder appears only as third author of Mistele–McGaugh–Hossenfelder 2023 (A&A 676, A100), whose lensing-versus-clusters objection to AeST the paper says its primordial shift charge resolves. Its own headlines: the pure-MI arm predicts baryonic lensing and is excluded at ~21σ; four of the author's own claims are withdrawn [R, from the paper's own summary lines; not re-checked] | nothing as a result. It is a different sector (modified inertia) and a different question | any claim about emergent gravity; its verdicts are not re-scored |
| 7 | `opus_48_extended_research/reviews/ROUTE2_LENSING_DM_FOOTING_AUDIT_2026-06-15.md`, `AEST_NONLINEAR_PHI_CLUSTER_2026-06-20.md`, `EVADE_DENSITY_NOGO_2026-06-20.md`, `dm_illusion/DARK_SECTOR_IS_FIELD_ENERGY_2026-06-19.md`, `qwen_claude_field_theory/closure_2026/condensate_pincer_2026/AEST_BOUNDARY_CONDITION_CLOSURE.md`, `real_research/bs_khronon_2026/README.md` and several further AeST / khronon files that match on Mistele–McGaugh–Hossenfelder 2023 or 2022 | AeST lensing confrontation (Mistele–McGaugh–Hossenfelder, A&A 676 A100, arXiv:2301.03499): a scalar-tensor / aether class, not Hossenfelder's covariant emergent gravity. `DARK_SECTOR_IS_FIELD_ENERGY` repeats "Hossenfelder's covariant Verlinde is unstable around de Sitter" and "static dS vacuum lacks the fuel an elastic active response would need" as banked one-liners [R] | the one-liner about de Sitter is the same claim as L5, not an independent source | all AeST results (a different class; AeST + the a₀ tie is CFG187 [R: DOOR11_RESULT supporting lanes]) |
| 8 | `sonnet55_push/puzzle_32pi/agents/E_literature_a0_coefficient/README.md` (row 45) | literature agent's table on a₀–Λ coefficients: a row groups "Hossenfelder 1703.01415; Cadoni et al. 1801.10374, 1707.09945; Peach 1806.10195; …" with "a₀² = Λ by order of magnitude, prefactor depends on the field mass; factors of order one neglected; … the 1/6 imported from Verlinde in eq 1.2; arbitrary critical length; inverse approach" — verdict "O(1) unfixed" [R, one grouped row; which clause belongs to which paper is not resolved there] | a G4 caution (item L8 of §0B): in her theory the tie's prefactor may be undetermined or imported from Verlinde | any attribution of a specific clause to a specific paper |
| 9 | `opus_48_extended_research/reviews/cluster_doors3/route_d_fresh_mechanism_sweep.py` (rows 183, 227, 229) | a cluster-door sweep table: Verlinde EG "FAIL … NULL (>5σ ruled out)"; a mixed "Hossenfelder–Mistele covariant emergent / superfluid lensing" row (galaxy-scale fits, clusters deviate, G1 + G4 FAIL) [R] | nothing (clusters are not a gate here) | the mixed row; it conflates a superfluid class (door 4) with emergent gravity |
| 10 | `real_research/TOE_LITERATURE_DOSSIER.md`, `real_research/papers/WHITEPAPER_TOE_MAP_2026.md`, `prep_2026/mi_fingerprint/PRIOR_ART.md`, `citations/**` (index and bibliography pages), `sol61_push/review_scope.json`, `fable_independent_2026/L153c_oscillatory_radius_lensing.py`, `opus_48_extended_research/papers/THE_COMPLETION*.md` and the other papers and json files that match | bibliography entries and the Mistele–McGaugh–Hossenfelder / Khelashvili–Rudakovskyi–Hossenfelder citations; the dossier ticks Hossenfelder as "✅ covariant completion" [R] | nothing (the tick is contradicted by rows 2–4 as "partial and unstable"; kept in §9) | all of it |
| 11 | `data_assembly/DOOR11_LITERATURE_2026-09-29.md`, `DOORS_LITERATURE_STATUS_2026-09-29.md` (the data chat) | [ABS] of Hossenfelder 2017 (§0.2); Verlinde, Lelli et al., Hees et al., Brouwer et al., Tuveri–Cadoni, Hossenfelder & Mistele 2020 (MW rotation curve with ~20% less baryons; a superfluid-type paper, outside door 12) | as §0.2 | Hossenfelder & Mistele 2020 (outside class) |
| 12 | `closure_map/*` and `campaign_fresh_gravity/LEDGER.md`, `STANDING_2026-09-29.md` | copy the CFG117 row; nothing further on Hossenfelder | as §0.2 | — |

**What is inherited, in one sentence.** No earlier lane scored a covariant emergent-gravity ACTION against the CFG44 target: CFG117 scored Verlinde's algebraic formula, Route 3 scored it against pre-campaign gates and predicted (without an action) that a covariantisation would face the Q₂ and stability problems, and the rest is literature commentary. The one earlier statement that changes this lane's design is that Hossenfelder's covariant form reportedly has no free interpolating function (row 2), so 12c is scoped as an EXTENSION whose function is declared, not as part of her theory.

## 0B. Literature claims used by this lane, each **from memory, unverified**, for the data chat to check against the papers

Each line says what I believe, where the repo already repeats it (with the file's own class), and what check would settle it. Nothing in the scoring depends on a claim being true except where noted.

- **L1 — Verlinde.** E. P. Verlinde, "Emergent Gravity and the Dark Universe", arXiv:1611.02269 (Nov 2016); SciPost Phys. 2, 016 (2017). Field content: none; not an action (a holographic / elasticity argument on a de Sitter background). Claim: dark energy carries a volume-law entropy in addition to the area-law entropy of the horizon; matter displaces it; the elastic response gives an apparent dark force. Form of the response: for a spherical baryon distribution, M_D²(r) = (a_M r²/G) d(M_B(r) r)/dr in the general (derivative) form, reducing to g_D = √(a_M g_B) for a point mass, with a_M = cH₀/6 (the 6 = 2(d − 1) at d = 4, CFG117 read eq. 4.49). An onset criterion M_B(<r)/(4πr²) < cH₀/(8πG) (his eq. 1.3 as CFG117 records it). Check: the equations quoted, the meaning of M_D (added to M_B or total; see L9), and whether the derivative form or the M_B-only form is his final statement. [M; repeated in CFG117, Route 3 (which uses the M_B-only form and calls it "universally quoted"), agentP]
- **L2 — Hossenfelder, authorship and venue.** S. Hossenfelder, "Covariant Version of Verlinde's Emergent Gravity", Phys. Rev. D 95, 124018 (2017), arXiv:1703.01415, sole author (exact title wording unverified). [M; the journal and number are repeated in the repo, the data chat has the [ABS] sentence]
- **L3 — Hossenfelder, field content.** The action contains the metric and a vector field A_μ on a de Sitter background; the repo's [ABS] wording is "a vector field in de Sitter that drags on baryons and also gives dark energy". Whether there is also a scalar, a Lagrange multiplier fixing the vector's norm, or a non-canonical kinetic function, I do NOT recall. Check: the Lagrangian as printed (every term, the coupling to baryons, the source of the de Sitter background). Nothing in class V's scoring rests on the unrecalled terms; the classification of a no-go does (§1.2, §8). [M]
- **L4 — Hossenfelder, elastic response.** In the weak-field, static, spherical limit with a negligible "imposter" (test) mass the theory reproduces Verlinde's dark-force relation, without a free interpolating function, with one free parameter fixed and an integration constant appearing. Check: whether the reproduced relation is the derivative form or the M_B-only form; whether the Newtonian (inner) regime is present in her equations or is imposed by hand (this decides whether the inner r⁻¹ regime of the target exists at all in her theory). [M; the repo's statement is in `VERLINDE_DEEP_DIVE_2026-06.md`, itself unverified]
- **L5 — Hossenfelder, stability.** A de Sitter-recovery error in the first version was corrected; small perturbations around de Sitter grow in the covariant version. Check: whether the growth is a gradient or a ghost instability, on which background, and whether it is in the corrected version. [M; repeated in `verlinde_foundation_stress_test.md` and `agentP_verlinde_coefficient.md` as "banked"]
- **L6 — Comment on Hossenfelder.** Pardo, arXiv:1706.07854 (a comment in PRD, per the repo). Content unknown to me. [M, repo-only]
- **L7 — Critique of Verlinde's derivation.** Dai & Stojkovic, JHEP 11 (2017) 007, arXiv:1710.00946: the elastic-strain argument done carefully recovers Newtonian gravity; contested by Yoon, arXiv:2003.03198. Hees, Famaey & Bertone, PRD 95, 064019, arXiv:1702.04358: the weak-field formula misses planetary perihelion advances by seven orders of magnitude. Lelli, McGaugh & Schombert, MNRAS 468, L68, arXiv:1702.04355: matches the RAR only with low M/L and predicts unobserved radius-correlated residuals. Brouwer et al., arXiv:1612.03034: parameter-free lensing agreement, non-diagnostic. Diez-Tejedor, Gonzalez-Morales & Profumo, MNRAS 477, 1285, arXiv:1612.06282: agrees with MOND at both ends of the transition, departs by up to ~50% in the middle. Milgrom & Sanders, arXiv:1612.09582: criticism of the non-generality of the relation. [M / [ABS] via the data chat for Hees, Lelli, Brouwer; the rest repo-only]
- **L8 — the a₀–Λ tie in the covariant paper.** The grouped literature row (`sonnet55_push/.../E_literature_a0_coefficient/README.md`) says the tie holds "by order of magnitude", the prefactor depends on the field mass, and the 1/6 is imported from Verlinde. I cannot say which paper each clause belongs to. Check: is the a_V = cH/6 in Hossenfelder's action derived or imported. [M, repo-only, grouped]
- **L9 — is Verlinde's M_D added to or included in the baryon mass?** My belief: added (g_obs = g_B + g_D in the tests by Brouwer et al. and Lelli et al.). Route 3's Theorem V1 identifies M_D with the TOTAL deep-MOND effective mass instead. The two readings differ by exactly one M_b, i.e. the linear sum versus the quadrature structure that CFG117 found. Check: the paper's definition of M_D. This lane scores both readings (B1–B3 added; B4 total). [M]

## 1. The exact model classes to be scored

### 1.1 Common setting (S0)

Static, weak-field, spherical, isolated, Newtonian limit. Inputs: M_b(<r) from CFG44's `Bcommon` (read-only import: `point_mass`, `exp_sphere`), g_N = GM_b(<r)/r², and the acceleration scale a of the class. **Unknown solved for:** the dark mass function M_D(r) (equivalently the dark field E(r) = GM_D/r²). Outputs:

- g_tot = G(M_b + M_D)/r², ρ_D = M_D′/(4πr²), and the G1 charge function **R(r) = 4πr³ρ_D g_tot / (a₀ M_b(<r))**, which equals C_model/C_target because the target is defined as C_T = (a₀/4π) M_b(<r) (CFG117 control C2 [S]).
- A **prescribed** M_D(r) (a table, a fit, or the target's own ODE) fails G1 AS A MECHANISM by rule (grade M0, §2). A **declared function shape** with the profile solved from it is grade M1. A shape that follows from a stated symmetry or action with only Λ-tied scales is grade M2.

### 1.2 12a — the covariant vector class V (action stated; its static reduction is what is solved)

**What is and is not known of Hossenfelder's paper.** From the record: an [ABS]-level statement only (§0.2). From memory [M]: an action with a vector field (and possibly a scalar) whose response to baryons reproduces Verlinde's dark-force relation in a limit, and which also yields dark energy in de Sitter. **I cannot reconstruct her Lagrangian term by term offline. Class V is therefore a reconstruction that shares her declared structure (a vector in de Sitter, a drag-type coupling to baryons, a Λ-tied scale); a no-go in V is a no-go of her paper only if her action lies inside V, which phase 2 cannot check.** This limitation is stated in the verdict line and in §8.

Action (units c = 1 where convenient; E = the electric-type invariant of A_μ):

S = ∫ d⁴x √−g [ (R − 2Λ)/(16πG) − (1/8πG) 𝓕(X) − V(A²) ] + S_m[g, ψ] + ε ∫ d⁴x √−g A_μ J_b^μ,  X = −½ F_{μν}F^{μν}/… (electric sector X = E² in the static frame).

Static spherical reduction (the equations to be solved): the Gauss law **𝒟(E) ≡ 𝓕′-weighted flux: 𝒟(E(r)) = ε² g_N(r)** (radial component of E; magnetic sector zero), baryons feel g_tot = g_N + E (drag coupling: the vector force is a gradient of A₀, so it is a potential force), the metric is unmodified at this order.

Sub-variants (each a separate scored variant, none pooled):

- **V0 — canonical vector (the null control class).** 𝓕 = X (Maxwell), V = ½m²A² with m tied to Λ (m = H_Λ/c, so the range c/H_Λ ≈ 5 Gpc [H]). Solves (∇² − m²)A₀ = −εq ρ_b. Expected: E ∝ g_N at every galactic r (a rescaling of G by 1 ± ε²) with no acceleration scale, so no a₀ can appear [H]. Scored so that "a vector by itself supplies no scale" is a computed statement, not an assumption.
- **V1 — elastic vector, drag coupling.** 𝒟 is a declared constitutive function of E with one scale a = a_V (the Λ-tied scale, §1.5); ε ≡ 1 [D]. The three declared laws are K1–K3 (§1.3). Solves 𝒟(E) = g_N for E (a quadratic in each case), then M_D = r²E/G.
- **V2 — gravitating vector (the "field energy is the dark mass" reading).** Same Gauss law, but the baryons feel only the metric and M_D(r) = ∫4πr′²u_A dr′/c², u_A = the canonical energy density of the field. Solves the Gauss law then a quadrature. Expected: u_A/c² is ~10⁻⁶ of the required density because E ~ a₀ is acceleration-scale [H: (a₀²/8πGc²) ≈ 7e-29 kg/m³ against a₀/(4πGr) ≈ 4e-22 kg/m³ at 10 kpc; the record's door 11B′ found the same ≤ 1.2e-6 for a massless flow, CFG173 [R]].
- **Scope note from the prior-work read (§0A row 2, L4).** The repo records that her covariant form reproduces Verlinde's relation in the weak-field static spherical limit WITHOUT a free interpolating function. If so, the nearest member of V1 to her reported limit is K2 (deep-only law) and the Newtonian-regime functions K1, K3 of §1.3 are EXTENSIONS, not parts of her theory: they are scored as "what a covariant action would need", and their verdicts are never attributed to her paper. Whether her equations contain the inner Newtonian regime at all is L4's open check.
- **Not V (already covered):** a UNIT-NORM timelike vector with F(a²), F(K) or a matter–θ coupling is the 11C class (CFG172, CFG188); not repeated.

### 1.3 12c — the constitutive function (what an "interpolating function" is in this class)

In S0 any single-valued Gauss law 𝒟(E) = g_N gives E = ψ(g_N) with ψ the inverse of 𝒟, i.e. g_tot = ν(g_N/a) g_N: the AQUAL-type map. The class is therefore exactly "which 𝒟". Declared members:

- **K1 (the P2-inverse):** 𝒟(E) = E²/(a − 2E), giving E = √(g_N² + a g_N) − g_N, g_tot = g_N√(1 + a/g_N) (P2). It has a pole at E = a/2 (an elastic limit). Its Lagrangian is a polynomial plus a log barrier, 𝓛 ∝ −E²/4 − aE/4 − (a²/8) ln(a − 2E) [H, to be checked by sympy]. **It restates the target's own kernel: grade M1 at best (G1 by construction on a point mass).**
- **K2 (deep-only, "Verlinde-point-mass"):** 𝒟(E) = E²/a, E = √(a g_N), g_tot = g_N + √(a g_N), M_D² = a r² M_b(<r)/G. It coincides with 12b's B2.
- **K3 (the simple wall):** 𝒟(E) = E²/(a − E), E = (√(g_N² + 4a g_N) − g_N)/2, g_tot = (g_N + √(g_N² + 4a g_N))/2 (the "simple" interpolating form with scale a). Its Lagrangian is likewise a log barrier with the wall at E = a.
- **KODE (positive control only, not a candidate):** the target's own ODE, (u_N + w)w′ = a₀ r u_N with u = GM, w = GM_D. It is the prescribed profile: grade M0. It exists so the harness can pass.

**Point-mass uniqueness (exact, [H], to be verified by sympy).** For a point mass, with g_tot = g_N(1 + f(x)), x = r/r_M, r_M = √(GM/a), the charge function is R = f′(x)(1 + f(x))/x = d[(1 + f)²]/d(x²). So R ≡ 1 iff (1 + f)² = 1 + x² (the Newtonian limit fixes the constant), i.e. the P2 law exactly. Consequences: K1 gives R = 1; K2 gives R = (1 + x)/x (matches CFG117 [S]); K3 gives R = 1 + 1/√(1 + 4x²) (1.98 at x = 0.1, 1.447 at x = 1, 1.050 at x = 10, 1.017 at x = 30; within 10% only for x ≳ 4.98) [H]. **G1 on the point mass within a band therefore pins the total-field law to P2 within that band; a variant cannot "derive" anything but P2 or fail.** The point-mass identities are Lean-certified in ChainCert.PointMass [R: GAPS_1_2_JOINT_STATUS line 1; CFG44 README].

**Sphere core limit ([H], checked against B1 N5 in phase 2).** For any cored baryon density and any 𝒟 with the deep limit 𝒟 ≈ E²/a as E → 0, the inner limit gives R → 5/2: g ∝ √(a g_N) ∝ r^{1/2}, u = r²g ∝ r^{5/2}, ρ_D ∝ r^{−1/2}, C_D = (5/2) C_target. This agrees with B1 N5's R up to 2.48 for the P2 phantom on extended profiles [S]. The CFG44 target itself has g_T² = (2/5) a g_N in the core, a different deep amplitude, because the target is a function of the ENCLOSED mass. So **any local single-field law with the deep limit misses the exponential-sphere target at small x on cored spheres, by a factor up to 2.5, for every constitutive function**; only a law that reads the enclosed mass (nonlocal in the sense of CFG44) can match it. That statement is [H] until phase 2 and is the reason §2 scores G1 on the spheres and not only the point mass.

### 1.4 12b — the elastic dark-energy phenomenology (Verlinde's formula and its discrete readings)

The formula (from CFG117's frozen text [R]; the paper itself [M]): M_D² = (a_V r²/G) d(M_b r)/dr, a_V = cH/6, where the 1/6 = 1/(2(d − 1)) at d = 4 comes from the volume-law part of the de Sitter entropy (CFG117 read this at eq. 4.49 [R]). Discrete readings, each a separate scored variant:

- **B1** — the formula as written (with the derivative term, so a local-density term 4πr³ρ_b enters M_D). Solves algebraically for M_D from M_b(<r) and ρ_b(r). Re-implemented from the formula, not from CFG117's script.
- **B2** — the derivative term dropped: M_D² = a r² M_b(<r)/G ≡ K2. For a point mass B1 and B2 agree.
- **B3** — B1 with Verlinde's onset gate: dark mass only where M_b(<r)/(4πr²) < cH/(8πG) (his eq. 1.3 as CFG117 records it [R]), i.e. with a₀ = cH = 6a_V, only where g_N < a₀/2 = 3a_V. For a point mass with the target a₀ = a_V that is x > 1/√3 = 0.577 [S: CFG117 R1 note]. A sharp gate (an unvaried mask); its stability as a varied term is the DE12/DE13 question (§2, G5).

- **B4** — the TOTAL-mass reading (Route 3's Theorem V1, §0A row 5, L9): Verlinde's M_D is the whole effective mass, g_tot = G M_D/r² with M_D² = a r² M_b(<r)/G (M_B-only form; the derivative-form total is reported alongside), and the dark density is what is left after the baryons, ρ_D = ρ_tot − ρ_b, M_D^{dark} = M_D − M_b. For a point mass this is the deep-MOND law g_tot = √(a g_N) at every radius: R = 1 exactly for x > 0 [H] but M_D^{dark} = M(x − 1) < 0 for x < 1 and g_tot < g_N there, so it is exercised by the admissibility line of §2 (G1). Solves algebraically.

The dependence on the entropy law enters ONLY through the normalisation a_V = c H/(2(d − 1)) with d = 4 (volume law) and through the MUTATE MU2 (area-law only: no volume term, no elastic dark force). Other d, other exponents and any free entropy exponent are NOT scored (a free exponent is a new constant, G4).

### 1.5 The constants ledger (only κ and Ω_c h² beyond declared function shapes)

| item | value / tie | status |
|---|---|---|
| κ | ½ FITTED (target's a₀ = κ c √(Gρ_Λ): canonical 9.3603e-11, alt 1.1312e-10 m/s²) | fitted |
| Ω_c h² | 0.1200, FITTED, only in the G2 "with-cold" run | fitted |
| a (the model's scale) | a_V = cH_Λ/6 with H_Λ = H₀√Ω_Λ (primary, tied to Λ); a_V(H₀) = cH₀/6 reported. H₀ = 67.4, Ω_Λ = 0.685 (CFG117's declared values). In κ terms κ_V = √(8π/3)/6 = 0.4824 [S: CFG117 R2], which REPLACES κ (it is a derived-in-the-source number [M]); it is not ½ | tied |
| the 1/6 | derived in the source argument, not in an action [R: CFG117 G4 note]; in Hossenfelder's covariant paper it may be imported from Verlinde, with the tie "by order of magnitude" (L8, a grouped literature row, unresolved) | not checkable "in the same action"; if imported, the tie is not derived in her action either |
| ε (vector-to-baryon coupling) | ≡ 1 [D]: the statement that the deep-regime scale and the wall scale are the same single scale a. Freed, ε² a and the wall a/2 decouple: a new constant | declared, flagged |
| the constitutive function 𝒟 | K1, K2, K3 are declared shapes; their scale is a only | declared shape (M1) |
| m (V0 mass) | m = H_Λ/c [D]; its effect at galactic r is ≲ 1e-12 [H] | tied, inert |

Any additional constant is a G4 FAIL unless tied to Λ or κ in the same action.

---

## 2. Scoring of G1–G5 and tools

Common numerics: numpy/scipy for profiles, root-finds and quadratures; sympy for every analytic step (Euler–Lagrange, the static reduction, R(x), principal symbols). Each script reproduces its controls (§4) before it scores. Grids: 3001 log-uniform nodes in x = r/r_M, x ∈ [0.1, 30], both ends exact nodes; r_M = √(GM_b/a₀) with the a₀ of the scored normalisation; masses M_b = 1e9, 3e9, 1e10, 3e10, 1e11, 3e11, 1e12 M☉; geometries point mass and exponential sphere h = 2 kpc at every mass [D: the task's spec; CFG117's h(M) = 2, 3, 4, 5 kpc reported as a sensitivity]; G, kpc and km/s units as `Bcommon`.

| gate | pass line | how it is scored | tools |
|---|---|---|---|
| **G1 strict (headline)** | R(x) ∈ [0.9, 1.1] over x ∈ [0.1, 30], all 7 masses, both geometries, SAME constants at every mass, in **N-shape** (target a₀ := the model's a; isolates shape, CFG117's convention), **N-tie canonical** (a from the Λ tie, target a₀ = 9.3603e-11) AND **N-tie alt** (target a₀ = 1.1312e-10). Reported per H ∈ {H_Λ (primary), H₀}. **Admissibility (added line, weakens nothing):** on every node also ρ_D ≥ 0, the cumulative dark mass M_D^{dark}(<r) ≥ 0 (counting any point-like piece at the origin), and g_tot ≥ g_N; a cell with R in band but an inadmissible profile is F ("R-only pass" is reported separately, never as a pass) | evaluate R from §1.1 for every variant and cell; report max |R − 1|, the x range within 10%, R at x = 0.1, 1, 3, 10, 30 | numpy/scipy; sympy for closed forms |
| **G1-P2 (reported, not the headline)** | max |g_tot/g_P2 − 1| ≤ 0.10 against the P2 law's OWN field, same grid | the reading CFG172 used for 11C-a/b/c ("compare with P2"); reported so a variant that "restates P2" is visibly different from one that hits CFG44's exponential-sphere target | numpy |
| **G1 mechanism** | grade M2 required for a pass as mechanism; M1 = declared shape; M0 = prescribed profile (FAIL as mechanism) | inspect which functions are declared and whether the shape follows from a stated symmetry with only Λ-tied scales (sympy: attempt to derive 𝒟(E) = E²/(a − 2E) from the log-barrier action of §1.3 and from Born–Infeld-type and AQUAL-type families; each attempt is recorded, each failure kept) | sympy |
| **G2 CMB and growth** | linear growth within 5% of ΛCDM to k = 30 /Mpc; CMB unchanged; perturbation equations stated or UNDEFINED. Two readings, never pooled: **with-cold** (Ω_c h² = 0.1200 present, the emergent force acts additionally) and **no-cold** (the emergent sector must itself supply cold growth) | (i) around FRW the background is E = 0 and 𝒟(E) ~ E² gives a vanishing linear stiffness, so linear theory is strongly coupled; G2 is scored by the nonlinear quasi-static estimate G_eff/G − 1 = E/g_N = ψ(g_lin)/g_lin with g_lin the linear-perturbation Newtonian field at (k, z, δ), as CFG172 did for its a-channel; (ii) Verlinde's formula applied to the cosmic mean density: M_D/M_b = 2√(R_H/(3Ω_m r)), R_H = c/H₀ [H]; (iii) the quasi-static equations and a growth ODE for the baryon and cold components; table over k ∈ {0.1, 0.3, 1, 3, 10, 30}/Mpc, z ∈ {0, 0.5, 1, 2, 3, 10, 30, 1000}; pass iff |G_eff/G − 1| ≤ 5% everywhere. CMB TT/TE/EE: UNDEFINED unless a Boltzmann treatment is defined (none is) | sympy, numpy/scipy |
| **G3 reaction and energy** | reaction ≤ 0.10 g_law over x ∈ [0.3, 30] and the canonical energy of the vector sector inside r_e ≤ ½ M_b V_f², V_f² = √(GM_b a₀), in BOTH r_ta conventions (this lane's and CFG4's; they differ by 1.7–3.6×), conventions imported read-only from `CFG48_gap1_switch/G4_exchange_action.py` and `Gcommon.py`; if a definition is unclear it is stated and disclosed, not guessed | reaction = the force on baryons beyond the gradient of a potential, from the vector's own field equations (zero by construction for a potential force: recorded p*, not a pass of substance); for V2 the gravitating reading. Energy = canonical (Noether) energy of the sector integrated to r_e from the solved E(r), with the action's normalisation (1/8πG)𝓕 | sympy (T⁰⁰), numpy (quadrature) |
| **G4 constants** | no constant beyond κ and Ω_c h²; scale tied to Λ (CFG43's tie P_cap = (κ²/8π)ρ_Λ c², or a stated equivalent) | the ledger of §1.5; strict count (declared numbers such as ε ≡ 1 count as declared, not tied); the normalisation table a_V/a₀ for H_Λ and H₀ on both footings; a re-tie check (vary each ledger entry across its window and record which verdicts move) | numpy |
| **G5 well-posedness, Solar System** | no ghost, no gradient instability, hyperbolic and causal (DE12/DE13/XC criteria); Q₂ ≤ 5.2e-27 s⁻² (2σ, gate 4.01); γ − 1 within (2.1 ± 2.3)e-5 (2σ); GW170817 c_T = c | (i) second variation of the reduced action about the static solution: 𝒟′ = dD/dE > 0 and 𝒟/E > 0 (radial and transverse stiffness), the characteristic speeds; control: reproduce FC-KH's exponential result (yq)′ = (1 − y)e^{−y} < 0 for y > 1 before scoring K1–K3 [R: CFG172 §4 C2]; (ii) **Q₂ as CFG7 H1 does it** (tide = max(|dg/dR|, g/R)), for the isolated Sun's E at Saturn (9.54 AU) and for the Milky Way's E at the Sun; (iii) B3's gate: the DE12/DE13 structural statement (a smooth on/off gate flat at both ends has W″ of both signs) applied to the onset gate, the sharp gate scored as an unvaried mask (the V0 obstruction [R]); (iv′) hypotheses of the Route-3 dilemma tested, not imported (§0A row 5): with the class-V action in hand, compute the static stress components (ρ, p_r, p_t) of the vector sector and state whether the G3 energy and G5 Q₂ outcomes agree with the Route-3 prediction; (v) **de Sitter stability of class V** (the claim L5 is not imported): expand the class-V action to second order about its de Sitter background (background vector value tied to Λ, §1.5), state the kinetic, gradient and mass terms of the vector perturbation and whether any mode grows (sympy); UNDEFINED if the background is not fixed by the declared class; (iv) c_T = c and γ as statements: a minimally coupled vector with no A^μA^νR_μν-type term leaves c_T = 1, and the drag force leaves the metric unmodified (γ = 1 at this order); lensing versus dynamics is diagnostic D2, not a gate | sympy, numpy |

Diagnostics, reported and not gates: **D-EFE** (does the pointwise law satisfy the Lean premise ν(y)√y → 1? then, by [T], scoped to pointwise laws, it has an EFE; the field-equation version is not formalised); **D-own** (a local action's static law is a function of the local total field; by [T] plus the [H] bridge it is not the ownership rule); **D1** (flat versus ∝ H(z) a₀: evaluate a_V(z) = cH(z)/6, which is ∝ H(z), for z = 0, 1, 2.5, 5; the distinctive law of the framework is flat, the rival ∝ H(z); a_V ∝ H(z) is a property to be REPORTED, not scored); **D2** (Φ versus Ψ, lensing versus dynamics for the drag reading); **D3** (the enclosed-mass structure: whether any variant's M_D depends on M_b(<r) only).

---

## 3. Hand ESTIMATES of the outcome (written before any script; kept whatever the scripts show)

Subjective probabilities for the verdict each script will record. F = fail, P = pass, U = undefined, "p*" = passes only trivially or by construction, "P-decl" = pass with a declared shape.

| gate | V0 | V2 | B1 | B2 = K2 | B3 | B4 | K3 | K1 |
|---|---|---|---|---|---|---|---|---|
| G1 strict | F 0.999 | F 0.999 | F 0.995 | F 0.995 | F 0.99 | F 0.97 (R = 1 on the point mass but inadmissible for x < 1 [H]; spheres R → 5/2 in cores) | F 0.99 (R = 1 + 1/√(1 + 4x²) on a point mass [H]) | F 0.95 (two independent counts, below); point mass P 0.97 in N-shape |
| G1-P2 reading | F | F | F | F | F | F | F ~0.9 (simple vs P2: ~14% at y ≈ 1 [H]) | P-decl 1.0 |
| G1 mechanism | F (no scale) | F | M0/M1 | M1 | M1 | M1 | M1 | M1 at best; M2 0.01 |
| G2 (with-cold) | F 0.6, U 0.35 | F 0.5, U 0.45 | F 0.75 | F 0.75 | F 0.5 (gate) | F 0.75 | F 0.7 | F 0.7, U 0.25 |
| G2 (no-cold) | U 0.9 | U 0.9 | U 0.7, F 0.3 | same | same | same | same | same |
| G3 reaction | p* | p* | p* | p* | p* | p* | p* | p* |
| G3 energy | F 0.3 | F 0.9 | F 0.85 | F 0.85 | F 0.8 | F 0.85 | F 0.85 | F 0.85 (E_field/E_orb ~ O(1)·r_e/r_M ≈ 10–300 in the deep regime [H]; the record's exchange ratios are 23–318 [R]) |
| G4 strict | F 0.7 (ε free) | F 0.7 | P count 0.55 | P count 0.55 | P count 0.5 | P count 0.55 | P count 0.5 (ε ≡ 1 declared) | F 0.5 (wall a/2 knows the target) |
| G5 | Solar System p* (no scale) | F | F 0.99 (Q₂ ~ 1e7×) | F 0.99 | stability F 0.85 as a varied gate | F 0.99 (Q₂ ~ 1e7×) | F 0.95 (Q₂ ~ 1.3e4×) | F 0.95 (Q₂ ~ 6.3e3×, [H]) |

Hand arithmetic behind the G5 row [H]: E at Saturn is a₀/2 = 4.68e-11 m/s² (K1, canonical), E/R = 3.3e-23 s⁻², against 5.2e-27: 6.3e3×; K3 (wall at a): 1.3e4×; K2 at Saturn: E = √(a_V g_N) = 7.7e-8 m/s², E/R = 5.4e-20: 1e7× (the record's Hees figure of seven orders [R]); B3's gate sets E = 0 at the Sun because g_N ≫ 3a_V, so Q₂ passes for B3 only by the gate, which is the V0 obstruction (an unvaried mask; varied as a smooth term it meets the DE12/DE13 statement that a gate flat at both ends has a wrong-sign second variation, [R]).

**Two independent reasons K1 should fail G1 strict** [H, with the record numbers]: (a) the spheres: R up to ~2.5 in cores for any local deep-limit law (B1 N5 [S]); (b) the normalisation: with H_Λ the model's deep amplitude is a_V/a₀ = 0.965 (canonical) but 0.7985 (alt), so on the alt footing R → 0.80 at large x, outside 10% [S: CFG117 R2 numbers]; with H₀ it is 1.166 (canonical) and 0.965 (alt). No choice of H passes both footings.

**Expected binding gate.** G1 for V0, V2, B1, B2, B3, B4, K3 (shape, plus admissibility for B4; structurally: point mass R = (1 + x)/x or 1 + 1/√(1 + 4x²)). For K1, the only variant that reproduces the point-mass target, the binding gate is G1 strict on the spheres and the alt footing, and independently **G5 (the Solar-System tail, Q₂ ≈ 6e3×)**: the same pincer as door 11C-a [R: G1 forces a tail of about a₀/2, Q₂ forbids it].

**Overall.** P(scoped no-go on every variant) ≈ 0.95. P(any candidate variant passes G1 strict) ≈ 0.04. P(any variant passes G1 as a derived mechanism, M2) ≈ 0.005. P(any variant passes G1 strict and G5 together) ≈ 0.01. If a variant surprises, the surprise is kept and independently re-derived (§7). **A pass is not manufactured and a fail is not softened.**

**Two further hand statements from the prior-work read [H].** (i) Route 3's covariantisation dilemma (§0A row 5) predicts that an action-based version faces the Q₂ and stability problems; the hand Q₂ above (1e3–1e7×) agrees in direction, with the recipe of this lane, and de Sitter stability of class V is UNDEFINED until its background is fixed (P(U) 0.5, P(unstable mode) 0.3, P(stable) 0.2). (ii) If L4 holds (her theory has no interpolating function and reproduces the deep relation), her theory is at best K2/B1, which fails G1 by (1 + x)/x [S: CFG117]; K1 and K3 then say what an extension would need, not what her paper does.

**Assumptions these estimates rest on (each unverified until phase 2):** the core limit R → 5/2 for a local deep-limit law [H]; class V is close enough to Hossenfelder's action that a no-go transfers [M, unverifiable offline]; K1's log-barrier Lagrangian is the correct integral of its 𝒟 [H]; CFG117's a_V/a₀ table [S].

---

## 4. Controls

**Reproduction controls (must pass in the main run; a failure is kept, disclosed, exit 1):**
- **C1** CFG44 point-mass identities: M_c = M(√(1 + x²) − 1), g = √(g_N² + a g_N), R ≡ 1 for K1 (sympy, then numerics to 1e-6).
- **C2** point-mass uniqueness: R = f′(1 + f)/x = 1 ⇔ (1 + f)² = 1 + x², from sympy, not imported.
- **C3** Verlinde point mass: M_D = M x and R = (1 + x)/x (derived independently here, then compared with CFG117's analytic statement, not with its script output).
- **C4** K3: R = 1 + 1/√(1 + 4x²) at x = 0.1, 1, 10, 30 to 1e-9.
- **C5** the P2 law's own phantom on the exponential sphere: R ∈ [1, ~2.5], compared with B1 N5's ranges ([1.000, 2.279] compact, [1.000, 2.484] diffuse) to 2% on the same profiles as N5; a mismatch is kept, not repaired.
- **C6** the core limit R → 5/2 (sympy on a cored profile) and its numerical approach on the 1e9 sphere at x = 0.1.
- **C7** Q₂ recipe: E = a₀/2 at 9.54 AU gives 6.3e3× (canonical), reproducing CFG172's tail figure [R].
- **C8** (positive control of the pass logic) KODE: the target's own ODE passes G1 strict on every cell and MUST be graded M0.
- **C9** the canonical-vector null: V0 gives E ∝ g_N with no scale (ratio constant to 1e-9 over the grid).

**MUTATE controls (each flips a load-bearing cell; `MUTATE=<name>`; outputs named by mode; the control "bites" when the named headline differs from the main run's in the predicted direction; a bite exits 1; a non-biting MUTATE exits 0 and is recorded as a declared control failure, kept):**
- **MU1 prescribe the profile** (M_D := the target's own cold mass, KODE, in place of each variant's M_D): G1 strict must flip F → P on every cell (the evaluator can pass); the mechanism grade stays M0.
- **MU2 area-law only (drop the volume term):** a_V → 0, so M_D ≡ 0. G1 must stay F (R = 0), and the Q₂ cell must flip F → P: the Solar-System failure is carried by the dark force, and the normalisation cell is load-bearing.
- **MU3 flip the sign of the elastic response** (𝒟 → −𝒟): ρ_D < 0 and 𝒟′ < 0. G1 must flip (sign) and the G5 stability cell must flip P → F (radial ghost/gradient instability), so the stability evaluator discriminates.
- **MU4 swap the footing:** K1 with H_Λ scored against the alt a₀ instead of the canonical one: the point-mass N-tie cell must flip P → F (R → 0.7985), showing the tie cell is load-bearing; a second sub-mode uses H₀ against the canonical footing (1.166).
- **MU5 restrict to the point mass:** K1's G1 strict must flip F → P on the point-mass-only grid, showing the sphere test is what fails K1.
- **MU6 remove the onset gate:** B3 → B1: the Q₂ cell must flip P → F and the G1 cell inside x < 0.577 must flip (R = 0 → nonzero).
- **MU8 admissibility off:** B4 scored with the admissibility line removed: G1 must flip F → P on the point mass (R = 1 for x > 0), showing that the admissibility line is what fails B4 and that an R-only test would have passed a profile with negative dark mass.
- **MU7 gravitating reading** (V1's drag coupling replaced by V2's field-energy source): G1 must flip P → F for K1 in N-shape (R → ~1e-6 [H]).

---

## 5. Declared choices

1. **Class V is a reconstruction** (§1.2): what is known of Hossenfelder's action is the [ABS] sentence; the rest is [M]. The verdict wording must say "in the frozen class V".
2. **G1 strict is the C-reading on CFG44's target (spheres included);** G1-P2 (against the P2 law's own field) is reported next to it and never merged. The reading CFG172 used for 11C-a/b/c ("P-declared kernel") is the P2 reading; door 12's headline is the strict one [D].
3. **Three normalisations** (N-shape, N-tie canonical, N-tie alt); a split is reported as a split. H_Λ is primary (the tie to Λ); H₀ (Verlinde's text) is carried and reported.
4. **ε ≡ 1** and one scale a for both the deep regime and the wall [D].
5. **Sphere:** exponential, h = 2 kpc at every mass (task spec); CFG117's h(M) set as a reported sensitivity.
6. **G3 reaction** is scored by construction for a potential force and marked p*, not a pass of substance; **G3 energy** is the canonical energy of the vector sector to r_e, with the action's own normalisation (1/8πG)𝓕; both r_ta conventions.
7. **G2** has two readings (with-cold, no-cold) and a nonlinear quasi-static estimate because linear theory around E = 0 is strongly coupled (𝒟 ~ E² gives vanishing stiffness); the CMB part is UNDEFINED.
8. **Q₂ as CFG7 H1** (tide = max(|dg/dR|, g/R)), isolated Sun and Milky-Way tide, no EFE; Cassini γ and c_T as statements.
9. **Ownership and EFE** are diagnostics (D-own, D-EFE), not gates; the [T] items are used only as §0.3 states, and the bridge from a pointwise law to a field theory is [H].
10. **Literature:** every statement about Verlinde's or Hossenfelder's papers beyond what the record files quote is [M]. No network was used.
11. **Hand estimates (§3) and hand arithmetic (§1, §3) are unverified until phase 2.**
12. **Admissibility** (ρ_D ≥ 0, cumulative dark mass ≥ 0, g_tot ≥ g_N) is an added G1 line [D]; without it a total-mass reading (B4) passes an R-only test on a point mass with negative dark mass. It weakens no gate.
13. **Inheritance (§0A):** earlier lanes' numbers are context or claims to check, never pass lines; Route 3's Q₂ recipe (assumed external field) is not used; the pre-campaign a₀(z) claim is not used; the campaign's a₀(z) statement (flat law versus the ∝ H(z) rival) is only what D1 reports.
14. **Literature (§0B):** L1–L9 are from memory and unverified; only L3 and L4 affect how a verdict is worded.

---

## 6. Script plan

Names (lane directory `campaign_fresh_gravity/CFG231_door12/`, to be created by the orchestrator at commit; in phase 2 scripts are written in the scratch dir first). Repo root from `ZF_REPO` or by walking up from `__file__`; every printed path is `<repo>/…`; no absolute home path is ever printed or stored. Each script < 15 min; numpy/scipy/sympy only. **Exit convention:** the main run exits 0 if all reproduction controls and internal identities pass (gate verdicts F or P are results, not exit codes); a control failure exits 1 and is kept; `MUTATE=<name>` exits 1 when the control bites and 0 when it does not (recorded as a declared control failure); MUTATE outputs are written as `*_MUTATE_<name>.out/.json`.

| script | content | gates |
|---|---|---|
| `CFG231_common.py` | constants (both footings, H_Λ and H₀), kernels K1–K3, CFG44 `Bcommon` read-only import, grids, repo-root helper | — |
| `CFG231_A1_point_mass_algebra.py` | sympy: R for V0, K1, K2, K3, B1; the uniqueness statement; log-barrier Lagrangians; attempts to derive 𝒟 (M2) from stated families; C1–C4, C9 | G1 (point mass), G1 mechanism |
| `CFG231_A2_sphere_charge_function.py` | numpy: exponential sphere, all variants (incl. B4 and the admissibility line) × masses × footings; G1 strict and G1-P2 tables; C5, C6, C8; MU1, MU4, MU5, MU8 | G1 |
| `CFG231_A3_vector_class.py` | sympy: Euler–Lagrange for V0/V1/V2, the static reduction, Green's function for V0, field energy and V2's dark mass, the vector's static stress components (ρ, p_r, p_t); hyperbolicity conditions; second variation about the de Sitter background (G5 (v)); D-EFE premise check | G1 (12a), G5 (i), (iv′), (v), diagnostics |
| `CFG231_A4_cosmology.py` | G2: quasi-static estimate, growth ODE, mean-density application of Verlinde's formula, with-cold and no-cold runs; D1 | G2 |
| `CFG231_A5_reaction_energy.py` | G3: reaction statement, canonical energy to r_e in both conventions (CFG48 read-only) | G3 |
| `CFG231_A6_solar_stability.py` | G5: Q₂ (isolated Sun, MW tide), FC-KH control, gate second variation (DE12/13 statement), γ and c_T statements; C7; MU2, MU3, MU6, MU7 | G5 |
| `CFG231_A7_normalisation_ledger.py` | G4: a_V/a₀ table, κ_V, ledger and re-tie check; MU2 normalisation cell | G4 |
| `CFG231_verdict.py` | reads the JSONs and prints the G1–G5 table per variant and the diagnostics; no physics | — |

MUTATE assignment: A2 (MU1, MU4, MU5, MU8), A6 (MU2, MU3, MU6, MU7), A7 (MU2, MU4).

---

## 7. What counts as a pass of G1 as a mechanism; what a scoped no-go looks like

- **Pass of G1 as a mechanism (M2):** the field equations of an action containing only Λ-tied scales, κ and Ω_c h², with no declared constitutive shape beyond what a stated symmetry fixes, produce R ∈ [0.9, 1.1] on the whole G1 grid (point mass AND exponential spheres, N-tie on both footings), and the derivation of the function is written out (which term gives 𝒟 = E²/(a − 2E), or whichever function it is). It must not be a prescribed profile (C8 and MU1 show the harness recognises that). Because the point-mass condition pins the law to P2 (§1.3), such a pass would be a derivation of P2 itself. **In that case an independent re-derivation is required before anything is reported**, the pass is stated with the gates that still fail, and it would count against the identification "Gap 2 reduces to Gap 1" (GAPS_1_2_JOINT_STATUS line 12) only if it needs no bound-only switch; it would say nothing about ownership (§0.3). A P-declared result (M1) gets an independent re-derivation of the field equations and no mechanism claim.
- **A scoped no-go looks like:** "within the frozen class (V0, V1 with K1–K3, V2, and the readings B1–B4; static spherical weak field; drag or gravitating coupling; one Λ-tied scale; ε ≡ 1), no variant satisfies G1 strict; the point-mass ratio is (1 + x)/x (K2, B1, B2), 1 + 1/√(1 + 4x²) (K3), or exactly 1 only for K1, which restates the target's kernel (M1) and still misses the spheres by up to ~2.5 and the alt footing by 0.80, and carries a Solar-System tail with Q₂ ≈ 6e3×", with the exact hypotheses listed and the binding gate named. Nothing here would say the theory is closed, that emergent gravity is refuted outside the class, or that any data favour the framework.

## 8. What is NOT covered

- Hossenfelder's action term by term (no offline access; class V is a reconstruction, and L3/L4 are open checks); the content of the Pardo comment (L6); Hossenfelder & Mistele 2020 and Khelashvili et al. 2024 (superfluid and per-galaxy DM-versus-MOND papers, outside the class); Mistele–McGaugh–Hossenfelder 2022/2023 (AeST, a different class); later covariant formulations; a scalar-tensor sector beyond the Λ-tied mass term; non-minimal couplings (A^μA^νR_μν, ξRA²), which move c_T and would need their own gate scoring.
- Verlinde's cosmological section, his cluster and lensing evidence, and the time-dependent and non-spherical regimes; non-spherical baryons (all variants); the external-field and merger regimes beyond the diagnostics D-EFE and D-own.
- Other emergent or thermodynamic routes: Milgrom's de Sitter Unruh argument (κ = ½ is not derived from it; the Unruh route is retired, CFG47), minimal-temperature entropic gravity, Tuveri–Cadoni scale-symmetry breaking (all named in the data chat's file at [ABS] level only).
- Boltzmann-code CMB (G2's CMB part is UNDEFINED), nonlinear cosmology, clusters, lensing (diagnostic D2 only), stellar M/L and the RAR fits (Lelli et al. 2017 is context, not a gate).
- The unit-norm timelike vector class (11C, CFG172/CFG188/CFG172D), CFG250/251/252 and the pending ChainCert batch (§0.4, §0.5).
- Anything about ownership (Gap 1): door 12 addresses only an isolated top-level system's dark density.

## 9. Record tensions noticed while writing (kept, not edited; for the orchestrator)

1. `GATES_STATUS` row 5.12 says the target gives the inner profile "exactly for P2 (ν_mono departs by up to 2%)". B1 N5 shows the P2 phantom's charge function equals 1 exactly for a POINT mass but reaches 2.28 to 2.48 on extended profiles, and the CFG44 README's referee correction says "up to 2.5 on extended profiles". The row's wording appears to hold for the point mass only.
2. CFG172's G1 for 11C-a/b/c compares with the P2 law ("P-declared kernel"); under this file's G1 strict (CFG44's exponential-sphere target) the same P2 law would, on B1 N5's numbers, miss the spheres at small x. That is a difference of reading, not an error in CFG172; it is why §2 reports G1-P2 beside G1 strict. Not re-scored here.
3. (Withdrawn: the first scoping message's lane label CFG230 was a mistake, confirmed by the coordinator; this lane is CFG231.)
4. The TOE dossier (`real_research/TOE_LITERATURE_DOSSIER.md`) ticks Hossenfelder as "✅ covariant completion"; `VERLINDE_DEEP_DIVE`, `verlinde_foundation_stress_test` and `agentP` call it partial, limit-only, disputed and unstable around de Sitter. Kept as a tension between repo files (§0A rows 2–4, 10), all of them unverified against the paper.
5. Two earlier lanes used different forms of Verlinde's M_D: CFG117's frozen text has the derivative form d(M_B r)/dr, Route 3 uses the M_B-only form and calls it "universally quoted". This lane scores both (B1, B2) and does not decide which is Verlinde's final statement (L1).
6. Route 3's Theorem V1 identifies M_D with the total deep-MOND effective mass, whereas CFG117 and the observational tests add M_D to M_B (L9). This lane scores both (B4 versus B1–B3).
7. Route 3 and its companion compare Verlinde's a_M ∝ H(z) with a framework a₀(z) value of 0.0060 at recombination; the campaign's own a₀(z) statement is the flat law with the ∝ H(z) rival. The pre-campaign number is not used (§5 item 13).
8. Route 3's Q₂ (17× the ceiling if an external field is granted) and this lane's Q₂ (isolated Sun at Saturn, and the Milky-Way tide, CFG7 H1) are different recipes and are not to be compared without saying so.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
