# CLOCK WORK ORDER — how to run the clock constructions, what is dead, what is live, and every next step (2026-09-18)

Orchestrator hand-off for autonomous agents. Read §0 before touching anything. Every claim below points at a committed
script; every next step has an objective, inputs, a method, a decision rule written before the run, and named deliverables.
Rules are in §3. Nothing here derives κ = ½ (fitted; provably underivable in this action class, L226/k01–k03).

## 0. Read first — the four clock constructions on the record and their status

| id | construction | where | status (2026-09-18) |
|---|---|---|---|
| C1 | cuscuton-clock sector (clock τ, projected-gradient scalar, cubic operator γ, closure P(X) = −(U/2)ln(U − 2dX)) + λφρ_m force coupling + **disformal matter coupling along the clock direction** | PAPER24 (DOI 10.5281/zenodo.22729429), PAPER25 (22729935); `fable_independent_2026/L186–L225`; parameter point L223 PART A | **DEAD AS WRITTEN on GW170817 (CK01)**: photons ride g̃ = g + disformal(φ)nn, gravitons ride g; photon–graviton delay along the NGC 4993 sightline 1.8–2.3 yr vs 1.7 s, both footings, both kernels, even with no Newtonian-regime share (the deep-MOND part of φ alone suffices). The record's own `prep_2026/gw170817_check` (3.5e7 s) predates the papers and is cited nowhere in L186–L225. The alignment s₀ ≥ 1.5e7 (PAPER25) is irrelevant: the cone split is a scalar. **The cosmological sector results (L186–L201 cold clustering component, L224/L225 forest) stand on their own; the force-law/lensing coupling (L208/L214/L215) is what dies.** |
| C2 | **single-metric** clock host (2026-09-18: lensing = dynamics DERIVED from the action, L279; α₂ settled, L280 — see `real_research/clock_2026/`) (khronon τ, c₁₃ = 0, c₁₄ ≲ 2.5e-5) + one MOND scalar φ with the k⁴ healing-length operator ξ²(∇V)² screening it inside ξ; matter and photons minimally on g | `qwen_claude_field_theory/closure_2026/FINAL_THEORY_CANDIDATE_2026-09-05.md`; action `closure_2026/g03_covariant_action_2026/ACTION.md` (+ FULL_VARIATION.md); lanes `hunt_2026/f29–f35, g03b–g03h`; roadmap `closure_2026/FRIED_CHICKEN_ROADMAP_2026-09-04.md` (G00–G14, astra's) | **LIVE, open gates**: G04–G14 not run; the C-H action's "conditional conserved-source causal failure" (FULL_VARIATION.md) unresolved; α₂(clock) = −5.9e-6 against the 4e-7 bound not reconciled (CK10); galactic phenomenology asserted not solved (CK13); strong coupling of the clock corner not computed (CK09). Passes by computation: quadrupole (g03d, floors 0.03/0.05 pc; L47 ephemeris floor ξ ≥ 4.00 pc), PPN corner α₁ ≈ −4c₁₄ (f33), γ = 1 (f32/f33), health at the corner (f34), FLRW minisuperspace (g03e), measured G (f35/g03f), c_T = c (c₁₃ = 0). Not touched by SW04 (screened, no 1/r share) nor SW06/CK01 (one metric). |
| C3 | IC-1 integrable auxiliary-clock construction (varied clock T, auxiliary u, U(c) = (1−c)[ln(1−c)² − 2ln(1−c) + 2] − 2) | `closure_2026/integrable_clock_construction_2026/ACTION.md` (astra, 2026-09-08); `fable_independent_2026/L74–L76` | OPEN construction: galactic health is one inequality v(S)R < 2.58 (L74, favourable sign, astra's IVP to finish); clusters a real open cost (L75/L76: no gentle winding gate separates galaxies from clusters on SPARC). Its work order 1–4 is in its ACTION.md; not repeated here. |
| C4 | CAM minimal repair S_min = ∫√−g[(M²/2)(R − 2Λ) + M²a² − M²a₀²Q(a/a₀)] + S_m | `closure_2026/cuscuton_acceleration_mond_2026/ACTION.md` (2026-09-10) | historical CAM refuted; the minimal repair is not a closed theory; no lane assigned below. |

**Two theorems every construction must respect (both computed this week):**
- **T1 — one physical metric for every species.** Any second matter/photon metric carrying the phantom potential fails GW170817's differential Shapiro test by ≥ 7 orders (`kappa_slot_2026/SW06`, `CK01`, `prep_2026/gw170817_check`). Conformal couplings evade T1 but lose lensing (light bends by the baryons only, DC-013/L241).
- **T2 — the MOND scalar's Newtonian-regime 1/r share must vanish or be screened.** A share s of the local 1/r potential with no gravitomagnetic partner gives α₁ = −8s/(1 + s) (`SW04`); C2 evades it by the k⁴ screening (no 1/r piece inside ξ, f30–f33); C1 traded it for the alignment s₀ ≥ 1.5e7, which does not evade T1.

**Do not cite as standing:** "the loop is closed", "closed on its own gates" for C1 (L223 is superseded by CK01 for the force-law coupling), the registered Arm-B ceilings 1.0450/1.0300 as C2's prediction (L47: at ξ ≥ 4 pc the pair is screened, γ_v = 1.000 + 8e-5), any SW01/SW02/SW03 rule as a live theory, THE_EQUILIBRIUM_THEORY.md, 5.09 keV, PAPER30 §5's table (the do-not-cite list).

## 1. How to run what exists

Environment: `python3` with numpy, scipy, sympy, mpmath (all lanes are self-contained; each prints `[PASS]/[FAIL]` lines with the
measurement and threshold stated separately and writes a `.json`). Lean: `cd fable_independent_2026/lean_2026 && lake env lean <file>.lean`
(Lean 4 + Mathlib; exit 0 and `#print axioms` = propext/Classical.choice/Quot.sound only).

**C1, the clock chain (run in order; every lane ~seconds to minutes):**
```
python3 fable_independent_2026/L186_clock_stability_theorem.py      # c_s² = (1−s₀)m_rel/(2−m_rel): sign(c_s²) = sign(1−s₀)
python3 fable_independent_2026/L200_coefficient_history.py          # s₀ − 1 = w/m_rel; the one-parameter family
python3 fable_independent_2026/L212_decoupling_branch.py            # W₀ = U − 2γq̄²q̄' = 0 removes the clock–scalar mixing
python3 fable_independent_2026/L213_branch_solved_and_the_board.py  # ρ₃/ρ = 1/(s₀−1); s₀ ≥ 2; π₃/π_grav ≤ 0.044
python3 fable_independent_2026/L214_force_law_on_the_branch.py      # a₀ = λ³/(12πGβs₀); C = 2kq̄²/U ≳ 1e3
python3 fable_independent_2026/L215_solar_system_on_the_branch.py   # γ = 1 exactly; boosted α₁ = 8f_s
python3 fable_independent_2026/L216_clock_alignment.py              # s₀ ≥ 1.5e7 from the 4.6 m/s alignment
python3 fable_independent_2026/L217_where_the_clock_rate_comes_from.py  # s₀ − 1 = wQ/(q̄d), a conserved charge; flat-a₀ drift ⇒ w ≤ 5.7e-7
python3 fable_independent_2026/L223_end_to_end.py                   # the 12-gate board at one point (11/11) — now superseded for the force-law coupling by CK01
python3 fable_independent_2026/L224_sector_perturbations.py         # linear growth integrator (validated to 6e-9 vs ΛCDM)
python3 fable_independent_2026/L225_flux_power.py                   # 256³ FGPA forest flux power (8/8)
python3 fable_independent_2026/clock_swarm_2026/CK01_clock_gw170817_gate.py   # the missing gate (5/5, findings)
```
The parameter point (L223 PART A): w = 5.66e-7, s₀ = 1.5e7, m_rel = w/(s₀−1) = 3.77e-14, U = m_rel ρ_dm = 3.68e-25 eV⁴, μ = 2dq̄²/U = 1 − m_rel, C = k/d = 1/μ_floor = 1e3, reach κ = 3.2e4 (stand-in; L222 withdrew the computed cutoff). astra's background bridge is imported read-only from `closure_2026/clock_response_repair_2026/cosmological_bridge_2026/radiation_probe.py` (class `ProbeBackground`) — never edit it.

**C2, the single-metric candidate:** `hunt_2026/f29_coherence_length_law.py` (ξ ladder: Cassini sub-pc; outer-halo globulars tens of pc), `f30_ppn_screening_door.py` (Green's function (1 − e^{−r/ξ})/r; force ratio r²/2ξ² inside ξ), `f31_ppn_k4_alpha1.py`, `f31c_ppn_k4_operators.py` (α₁'s scalar drag → −4(2−K_B)/(J_Y(1+ξ²k²)+1)), `f32`/`f33*` (æther/clock host PPN ladders), `f34` (time-dependent quadratic action, health), `f35` (measured G), `g03b–g03h` (floors, zero-field limit, FLRW minisuperspace, measured G, wide-binary orientation); `closure_2026/RUN_ALL_GATES.py`; G00–G02 scripts named in the roadmap (`g00_provenance.py`, `g01_strict_aqual.py`, `g02_filtered_efe.py`). Expected as committed: f33 ladder 0 FAIL; g03d floors 0.03/0.05 pc; L47 ξ ≥ 4.00 pc (F1 FAIL = the finding that the registered ceilings are vacuous).

**This week's constraints (kappa_slot_2026):** SW04 8/11 (α₁ theorem), SW05 12/12 (quadrature window), SW06 7/7 + `lean_2026/SW06_local_nogo.lean` (lensing trilemma), SW07 5/5 (the DR4 three-way table), L263/L264 (real-mass phantom dead; SEP ⇒ EFE).

## 2. Next steps — granular, in the order they should run

Naming: `CKnn_<slug>.py/.out/.json` in this directory; one line per lane in `CK00_INDEX.md`; MUTATE controls write `CKnn_results_MUTATE.json`, never the main file; the main run is the last before `git add`.

### Group A — the GW170817 repair of C1 (blocks everything else on C1)

**CK02 — the single-metric rewrite: move the disformal structure into the gravitational sector.**
Objective: is there a version of C1 in which matter, photons AND gravitons ride one metric while the scalar still supplies the force law?
Inputs: PAPER24 eq. (action) and §5; L215's matter-metric expansion; the clock's n_μ = −∂_μτ/√X.
Method: define g̃_μν = g_μν + B(φ, X) n_μ n_ν; rewrite S_EH[g] + S_clock in terms of g̃ (a disformal transformation of the Einstein–Hilbert term with a clock-built vector produces a DHOST-type action with φ-dependent coefficients; do the transformation in sympy on (i) a general static weak-field metric, (ii) FRW, (iii) a TT tensor perturbation on FRW); couple matter and photons minimally to g̃; derive the tensor-mode speed c_T and the static potentials Φ̃, Ψ̃.
Decision rule (written before the run): PASS only if c_T = 1 EXACTLY by structure (|c_T − 1| < 1e-15 without tuning B) and the static force law still reproduces g = √(a₀GM)/r beyond r_M with lensing = dynamics (Φ̃ = Ψ̃). If c_T − 1 ∝ B, the construction is dead unless B ≤ 1e-15 everywhere, which removes the force law: record the kill.
Deliverables: `CK02_gravitational_disformal.py/.out/.json`; a Lean file for any exact identity used (the disformal transformation of the tensor kinetic term). Cost: 1–2 days.

**CK03 — the alternative: drop the disformal coupling; can the sector's own clustering supply the lensing?**
Objective: with λφρ_m only (conformal), light bends by Φ + Ψ of g; the sector's clustered density around galaxies would have to reproduce the lensing RAR.
Inputs: L187/L188 (density-gated depletion, the sector's clustering), L248 (the mass-budget truncation test on the real Brouwer+2021 KiDS data, `real_research/data/lensing_rar/brouwer2021_rar/`, full covariance).
Method: compute the sector's clustered profile around an L* galaxy from the L186–L201 background + L224 growth (Jeans scale 4.9 /Mpc at z = 0), then run the L248 machinery on it (slope below 1e-13 m/s², the turn at g_bar = a₀/(1+B)²).
Decision rule: Δχ² vs Brouwer ≥ +25 ⇒ dead (L248's kill inherited: measured slope 0.537 ± 0.026 has NO turn); otherwise report the profile and the Δχ².
Deliverables: `CK03_sector_lensing_profile.py/.out/.json`. Cost: 1 day.

**CK04 — the erratum.** PAPER24 and PAPER25 need versioned errata carrying CK01 (a "GW170817 gate" section: the construction's disformal coupling fails the differential Shapiro test by 3e7–4e7×; what survives is the cosmological sector). **Zenodo deposits only on the user's explicit go** (`zenodo_publish_paper24_2026.py --newversion`, `..._paper25_...`); prepare the tex diff and stop.

### Group B — C2, the single-metric candidate: astra's roadmap gates G04–G14 with concrete contracts (astra leads; support lanes may pre-compute)

**CK05 = G04 — full variation and the Ward identity.** Vary g, τ, φ and the C-H auxiliaries (U, W(z,x), L(z,x), λ₀) of `g03_covariant_action_2026/ACTION.md`; derive ∇_μT^{μν}_matter = 0 from the matter equations alone and show the Bianchi identity closes with the clock and scalar equations (sympy on a general static metric and on FRW). Decision: the identity holds exactly; any residual ∝ a field equation is acceptable, a residual that is not is a FAIL. Deliverables: `CK05_variation_ward.py`, Lean for the algebraic identity. Also resolve FULL_VARIATION.md's "conditional conserved-source causal failure": state the condition, test it on the compact domain, and record PASS/FAIL. Cost: 2 days.

**CK06 = G05/G06 — ADM, Legendre map, Dirac–Bergmann count.** Kinetic matrix on the generic branch (y > 0, k ≠ 0) and on the strata y = 0, k = 0 (distinct strata; never extend a count across a rank change, IC-1's rule). Target: 2 tensor + clock + φ; the clock cuscuton-like with a second-class pair; report det of the constraint matrix symbolically; MUTATE control: flip the sign of the ξ² term and show the count/health changes. Deliverables: `CK06_dirac_count.py`. Cost: 3 days.

**CK07 = G07 — FLRW with the clock.** Minisuperspace with the lapse restored (reuse L213's ρ,p machinery: ρ = −a⁻³∂_N(Na³L)|_{N=1}, p = (3a²)⁻¹[∂_a − d_t∂_ȧ](Na³L)|_{N=1}); the ξ term's background contribution (V = 0 on FRW ⇒ zero; verify); the Λ renormalisation G_cos/G = 1/(1 + (c₁₃ + 3c₂)/2)-type (g03e). Decision: an expanding regular branch exists with H² = (8πG/3)ρ(1 + O(c₁₄)) and the scalar's FRW kinetic coefficient finite (no TeVeS strong coupling at Y = 0: the k⁴ term or a Θ-term must keep it finite — state which). Deliverables: `CK07_flrw_clock.py`. Cost: 1 day.

**CK08 = G08 — the independent weak-field metric and the measured G; ONE number for ξ_min.** Reproduce f30 G1/G2 ((1 − e^{−r/ξ})/r; force ratio r²/2ξ² inside ξ) and G_N = G/(1 − c₁₄/2) (f35/g03f) from the full metric equations, then reconcile the two floors on the record: g03d's 0.03/0.05 pc (the static Cassini solve) and L47's 4.00 pc (Pitjev–Pitjeva on the fourth-order carrier, M_ph(<r)/M = r²/2ξ²). Decision: state which carrier C2 actually has and derive ξ_min once; if it is 4 pc, the wide-binary and Oort predictions are fully screened (γ_v = 1.000). Deliverables: `CK08_weakfield_xi_min.py`, Lean for the floor algebra. Cost: 1 day.

**CK09 = G09 — modes, GW and strong coupling.** Quadratic action on (i) the PPN corner (f34 exists) and (ii) a galactic background g ~ a₀ (new): the scalar's dispersion ω² = c_s²k²(1 + ξ²k²) with c_s² ≈ 0.04, the khronon's fast mode, c_T = 1; the strong-coupling scale of the clock corner Λ_sc ∼ M_P√c₁₄ (c₁₄ ≤ 2.5e-5 ⇒ Λ_sc ∼ 5e-3 M_P — compute it properly with the scalar mixing) against every scale the theory is used at. Decision: all kinetic eigenvalues positive on both backgrounds; Λ_sc above the highest energy scale probed. Deliverables: `CK09_modes_strong_coupling.py`. Cost: 2 days.

**CK10 = G10 — the FULL PPN, and the α₂ reconciliation first. [DONE 2026-09-18: `real_research/clock_2026/L280`: α₂ passes at c₁₄ ≤ 8×10⁻⁷ or on the equal-speed locus c₂ = c₁₄/(1−2c₁₄), c₁₄ ∈ [1, 2.5]×10⁻⁵; the record's corner c₁₄ = 10⁻⁵, c₂ = 1 failed by 12×. Remaining for G10: the other PPN parameters (β, γ, ξ, α₃, ζ_i) re-derived with the screened scalar at the passing corners.]** The scorecard lists α₂(clock) = −5.9e-6 at c₁₄ = 1e-5; the bound is |α₂| < 4e-7 (solar spin axis). On the khronometric (α, β, λ) family α₁ = α₂ = 0 is a 1-parameter locus (Blas–Sibiryakov; L270 P3): find the point with c₁₃ = 0, evaluate the health conditions there (no ghost, no gradient instability, c_T = 1), THEN compute all ten PPN parameters (β, γ, ξ, α₁, α₂, α₃, ζ₁–ζ₄) with the screened scalar present, using SW04's bookkeeping (g₀₀'s w²U and wⁱwʲU_ij coefficients, g₀ᵢ's w_iU and wʲU_ij, the rest-frame V+W invariant) as the cross-check. Decision: every parameter inside its bound at a point that is healthy; a point that needs c₁₄ < 0 or c₁₃ ≠ 0 is a FAIL. Deliverables: `CK10_full_ppn.py`. Cost: 3 days.

**CK11 = G11 — causality and the Lifshitz dispersion.** The k⁴ operator gives group velocity > c for k > 1/ξ; on a preferred foliation this is not a closed-causal-curve problem, but the initial-value problem must be well posed: prove ellipticity of the fourth-order spatial operator on the leaves (extend g03c's symbol J_Y k² + ξ²k⁴ to the full quadratic action including the clock) and hyperbolicity in τ; state the causal structure (leaf-instantaneous constraints, as IC-1 and L268 C2 accept). Decision: a theorem-level statement with the domain of ellipticity; a failure of ellipticity anywhere in y ∈ [0, ∞) is a FAIL. Deliverables: `CK11_causality.py` + Lean where algebraic. Cost: 2 days.

**CK12 = G12 — cosmological perturbations and observables.** Extend the L224 integrator (validated to 6.4e-9 against ΛCDM growth) with the clock and the screened scalar; compute CMB acoustic-scale deviation, growth, lensing amplitude, S₈, the forest flux power (reuse L225's FGPA chain, same seed). Decision (L224/L225 tolerances): acoustic ≤ 1e-4, forest flux within the eBOSS/high-res bands (0.03/0.08), lensing at z = 0 ≤ 3%. If feasible, a CLASS/hi_class fork for C_ℓ; state it is not a likelihood. Deliverables: `CK12_perturbations.py`. Cost: 1–2 weeks.

**CK13 — the galactic solve (the scorecard's kill item 4, asserted not solved).** Extend `theory_2026/aqual_solver_2026.py` (the validated axisymmetric AQUAL solver) with the k⁴ term; solve 3 SPARC discs spanning the RAR plus the Milky Way at ξ ∈ {4, 10, 30} pc. Decision: rotation curves within 2% of the ξ = 0 AQUAL curve beyond 0.5 kpc; the MW vertical force at the Sun (the vertical-force front, f_M = 1.30) unchanged to 1%; a larger change means the healing length is not invisible at galaxy scale and the RAR must be refit. Deliverables: `CK13_galactic_k4_solve.py`. Cost: 3 days.

**CK14 = G13 — the discriminating predictions (C2's fingerprints).** (i) Gaia DR4 wide binaries: γ_v = 1.000 + O((s/ξ)²/2) (fully screened for ξ ≥ 4 pc) against the cap law 1.086–1.155 (SW01) and AQUAL 1.1614–1.2267 (Arm A) — SW07's three-way table is the scoring sheet; (ii) the Oort-cloud/comet anisotropy front (DOI 10.5281/zenodo.21966646 predicts an AQUAL field-aligned signature): C2 predicts NULL, the cap law an isotropic boost; write the three-way decision rule before any comet data; (iii) size-dependent screening: systems smaller than ξ are Newtonian regardless of acceleration — the outer-halo globulars (f29 G1: Pal 4, Pal 14, NGC 2419 vs Pal 3) with the full k⁴ profile and Gaia DR3 dispersions (CK23); (iv) the Cassini quadrupole exactly zero at r_M ≪ ξ. Registering anything in `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md` is append-only on the user's explicit go. Deliverables: `CK14_predictions_ledger.md` + the scripts behind each number. Cost: 2 days.

**CK15 = G14 — closure package or restricted no-go.** Extend `closure_2026/RUN_ALL_GATES.py` with CK05–CK14; Lean certificates for every algebraic identity (screening Green's function, ξ floor, PPN corner formulas, the local no-go); an honest restricted no-go if any gate fails. Never say "theory closed".

### Group C — the clock sector's own open numbers (worth running only if CK02 or CK03 rescues a lensing route for C1)

**CK16 — the origin of s₀ ≥ 1.5e7.** L217: s₀ − 1 = wQ/(q̄d) with Q the conserved charge of the shift symmetry. Compute what fixes Q's value: the tracking attractor (L194) and the criticality onset (z ≈ 1.7e4 at the corrected reach, L224); test whether initial data at z ≥ 1e4 predict s₀(z = 0) within a decade of 1.5e7. Decision: predicted ⇒ "explained"; otherwise s₀ stays a measured number and PAPER25's title stands as an inequality. Deliverables: `CK16_clock_rate_origin.py`.

**CK17 — the reach with the correct sound speed.** L222 F2: L219 used P(X) alone; L186's full c_s² = (1 − s₀)m_rel/(2 − m_rel) carries (1 − s₀) = −1.5e7 and is imaginary at Y = 0 before criticality. Recompute the UV cutoff and the criticality floor; decision: the window 1.5e-8 ≲ w ≲ 5.7e-7 (L218, ceiling from the flat-a₀ drift) survives or collapses. Deliverables: `CK17_reach_recomputed.py`.

**CK18 — pin ℓ; evaluate U > 4dℓ; the C·w trade-off.** L205/L208's window 1 < 4dℓ/U < 8 and L223 V6b (the flat law constrains the product C·w ≤ 5.7e-4): map the allowed (C, w, ℓ) region with drift ≤ 1% at z ≤ 5 and μ_floor = d/k ≤ 1e-3. Deliverables: `CK18_window_map.py`.

**CK19 — the disformal cosmology** (only after CK02 passes): background + perturbations with the rewritten coupling. **CK20 — one-loop radiative stability** with the actual cutoff from CK17 (L220–L222 left δU/U = O(1), "marginally stable").

### Group D — data lanes independent of the construction

**CK21 — DR4 readiness.** Re-run the Amendment-10/11 pipeline dry run (`prep_2026/gaia_dr4_prep/`, `predictions_2026/`); attach SW07's three-way table as the scoring sheet; the cap-law band (1.086–1.155) becomes a third arm ONLY on the user's go.

**CK22 — the comet-anisotropy three-way rule.** Recompute the Oort-cloud prediction under C2 (null), the cap law (isotropic boost, SW01) and AQUAL (field-aligned, the published front); freeze the decision rule.

**CK23 — the ξ ladder with Gaia DR3.** Pal 4, Pal 14, NGC 2419, Pal 3 and the 16–28 pc population of `hunt_2026/u03`: fit ξ with the full k⁴ screening profile (not the leading (r/ξ)²/2); decision: one ξ consistent with all within 2σ, or the Pal 3 contradiction f29 flagged.

## 3. Rules (binding)

1. Test the framework on its own terms; verify a FAIL as hard as a PASS; never manufacture a win or a deficit. A FAIL is a finding.
2. Both a₀ footings always (9.3619e-11 canonical, 1.1279e-10 alt); both kernels (ν_RAR, μ₂) where a kernel enters.
3. Every load-bearing claim is a committed runnable script; checks compute booleans with measurement and threshold stated; no literal-True checks; MUTATE controls where the structure does the work.
4. Lean certifies algebra of definitions only; say so.
5. astra leads the field-theory effort: never edit `hunt_2026/*ASTRA*`, `closure_2026/*/ACTION.md`, or the cosmological bridge; reproduce before contradicting; write support lanes.
6. `PREREGISTRATION_DR4.md` and every `*_HASH.txt` are append-only on the user's explicit go. Zenodo deposits only on the user's explicit go.
7. No personal names or personal framing in committed files or commit messages; grep before commit.
8. Never write "theory closed", "no open doors", "derived κ".
