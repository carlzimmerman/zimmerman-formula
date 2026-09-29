# CFG187 — AeST with a Henneaux–Teitelboim Λ-tie: the time-flow reading assembled as one candidate, and its scorecard. FROZEN QUESTION

Written 2026-09-29, before any CFG187 script ran. Requested by the orchestrator (door 11, the time-direction reading of the owner's flowing-vacuum picture, `closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md`, addenda 1–2). κ = ½ is FITTED. Nothing here says the theory is closed.

## 0. What I have already seen (disclosure)

Before writing this file I read, and so know the numbers of: `closure_map/GATES.md`, `GATES_STATUS_2026-09-29.md`, CFG176 and CFG177 (READMEs), CFG172's README (door 11C, which scored Einstein-aether/khronon variants and left AeST-type vector–scalar models out of scope), CFG43's README, XR20's README and `.out` controls, `real_research/reviews/mi_relativistic_completion_aest_2026.py`, `mi_aest_jeans_nonlinear_verdict_2026.py`, `real_research/bridge1_aest_equations.md` (the record's transcription of the AeST action, checked there against the arXiv LaTeX source), `qwen_claude_field_theory/closure_2026/V9_PPN_KILL_VERDICT.md`, the condensate pincer files (`CONDENSATE_NOGO_THEOREM.md`, `CONDENSATE_MU_PINCER_VERDICT.md`, `AEST_BOUNDARY_CONDITION_CLOSURE.md` and their `.out`), `ACTIONS_AND_NOGOS.md`, CFG4 (README, clusters/galaxy-law `.out`), CFG7_hierarchy_fg001.out (its "law with the external field" rival column), CFG8, CFG31, CFG61, CFG64, CFG185 (README), BS3 and FP23 `.out`, CFG1 A01, the DR4 pre-registration's Arm A/B/C text, and KM1's README. **So every carried number below is known to me before the script; the scorecard is an assembly, not a blind test.**

One exploratory evaluation was run before this file (in the scratchpad, not in the repo): importing `CFG4_common` and printing h(y) = y(ν − 1) at Earth, Mars and Saturn for P2, ν_mono and the RAR kernel, to check the import works without writing bytecode. It gave P2 0.5, ν_mono 1.177, RAR 0 at Earth (canonical). No other number of this lane was computed. CFG185 (now committed, 568107b4f) has these values.

## 1. The candidate (declared)

Units c = 1; 16πG̃ = 1 in the algebra. The AeST action is the record's transcription of Skordis & Złośnik 2021, eq. 5 (`real_research/bridge1_aest_equations.md`), with two changes: the MOND normalisation is tied to Λ, and Λ is the Henneaux–Teitelboim (HT) field with its multiplier, written as in CFG43 / XR20 T1:

    S = ∫d⁴x { √−g [ R − (K_B/2) F^{μν}F_{μν} + 2(2−K_B) J^μ∇_μφ − (2−K_B) 𝒴 − 𝓕(𝒴, 𝒬; Λ) − 2Λ − λ(A^μA_μ + 1) ] + 2Λ ∂_μT^μ } + S_m[g]

- A^μ unit timelike (the time-flow), F_{μν} = ∇_μA_ν − ∇_νA_μ, J^μ = A^ν∇_νA^μ, 𝒬 = A^μ∇_μφ, 𝒴 = (g^{μν} + A^μA^ν)∇_μφ∇_νφ.
- 𝓕(𝒴, 𝒬; Λ) = (2 − K_B) α(Λ)² j(𝒴/α(Λ)²) + 𝒦(𝒬). The deep-MOND limit j(s) → [2λ_s/(3(1+λ_s))] s^{3/2} reproduces the transcription's 𝒥 → [2λ_s/(3(1+λ_s)a₀)] 𝒴^{3/2} with a₀ → α(Λ).
- **The tie (POSTULATED):** α(Λ) = κ √(Λ/8π), i.e. a₀ = κ c √(G ρ_Λ). It is a coupling function written into the action, as in XR20 T1; it is not derived. **κ = ½ FITTED** (canonical footing; on ρ_Λ the alt footing needs κ = 0.6043, XR20 C3).
- 𝒦(𝒬) = 𝒦₂(𝒬 − 𝒬₀)² + … is AeST's dust sector. The constant term the transcription puts in 𝒦 (−2Λ) is moved out and replaced by the HT field Λ(x) with multiplier T^μ (a vector density), so there is one cosmological constant, not two.
- Kernel: the framework's ν_mono (the 09-26 decision), P2 reported, embedded in j's full shape through the record's AQUAL embedding (`mi_relativistic_completion_aest_2026.py` Part B). The exponential RAR kernel is reported only for the Solar-System tail.
- AeST's own parameters (K_B, λ_s, 𝒦₂, 𝒬₀) are declared, not fitted here; the dust amount is an integration constant (the record: "amount I₀ free").

## 2. Questions

**Q1 — the tie, from the action (sympy, load-bearing).**
- **L1 TIE.** a₀ is a function of Λ alone in the action (∂α/∂Λ ≠ 0), and α(Λ_obs) reproduces a₀ = 9.3603 × 10⁻¹¹ m s⁻² from FP0's ρ_Λ to 10⁻⁶ (canonical). The alt footing's κ = 0.6043 is reported.
- **L2 GLOBAL.** Varying T^μ gives ∂_μΛ = 0 identically, whatever the AeST sector (its symbols absent from those equations). Varying Λ gives ∂_μT^μ = (terms without T): the Λ-dependence of 𝓕 lands only in the unimodular clock, and no other field equation contains T.
- **L3 SAME-AS-AeST ON SHELL.** With Λ = Λ₀, the φ, A^μ and λ equations of the tied action equal plain AeST's at a₀ = α(Λ₀), for a generic j and 𝒦 (difference simplifies to 0).
- **L4 NO LOCAL DOF.** Periodic-lattice Dirac count: the HT sector gives N constraints Λ_{n+1} − Λ_n of rank N − 1, all brackets zero, no secondary constraint for a Hamiltonian with arbitrary Λ-dependence; phase-space count 2N − 2(N − 1) = 2 (one global pair); the local sector's count unchanged.
- **L5 FLAT.** On shell a₀(z)/a₀(0) = 1 exactly at z = 0.5, 1, 2.5, 5, 1100.
- **L6 FRW AND LINEAR ORDER.** On FRW with φ̄(t) and A along cosmic time, 𝒴̄ = 0, and for a general linear perturbation (metric, aether with the unit constraint, scalar) δ𝒴 = 0; so the a₀-sector (∝ 𝒴^{3/2}) is absent from the background and the linear equations (the record's bridge1 order counting, re-derived).
- **L7 COUNT.** Constants beyond AeST's own: {κ}; a₀ is not independent.
- **L8 METRIC-FREE.** The HT term 2Λ∂_μT^μ has zero metric variation, so it changes neither c_T nor the PPN metric.

**Q2 — the scorecard (reported, not load-bearing).** Each row of `closure_map/GATES.md` (ids unchanged) is given a status for the candidate, with candidate B's status from `GATES_STATUS_2026-09-29.md` beside it.
- Status codes: PASS / FAIL / MARGINAL / CONDITIONAL (passes only on a reading the record leaves open or excludes elsewhere) / NS (no data yet) / UNSCORED (no committed computation of the same physics) / N/A (a construct of B's that this candidate does not have).
- Physics code: **SAME** (a committed computation evaluates the equations the candidate reduces to: e.g. CFG7's "law with the external field" column for AeST's quasi-static MOND limit with its EFE); **CARRIED** (same class, base model differs, named); **LIT** (a literature statement, as the record quotes it or from memory, marked UNVERIFIED); **HERE** (computed by this lane).
- The galaxy-scale reading has two horns, scored separately and never pooled: **N**, the dust does not sit in galaxies (the published AeST phenomenology, which the record says needs a per-galaxy boundary constant, MMH23); **D**, the dust clusters like CDM on galaxy scales (the record's linear verdict, `mi_aest_jeans_nonlinear_verdict_2026.py` B1–B2). Galaxy rows are scored on horn N (the reading most favourable to AeST's MOND phenomenology) unless stated; the record's N9 theorem, which says horn N costs the CMB/forest, is scored on rows 3.01/3.12.
- Every carried number is anchored: the script checks that the cited text is present in the cited committed file (control C6).

**Q3 — how it differs from candidate B** (EFE present vs ownership; one field vs a switch; additive dust vs the max rule), and where it is better or worse on the committed rows.

**Q4 — what stays unexplained** (κ = ½; the tie's origin; the dust's placement).

## 3. The pre-declared rows and their sources (known to me, see §0)

| row | what is carried | source |
|---|---|---|
| 1.01 | SPARC rms ν_mono 0.1003/0.0991, P2 0.1083/0.1035 (horn N); horn D overshoot re-run here with current kernels | CFG4_galaxy_law.out; jeans script Part E (re-run) |
| 1.07–1.14 | the "law with the external field" rival column of CFG7 H0/H2/H4/H5/H6 | CFG7_hierarchy_fg001.out |
| 1.15 | Chae: rival 0.76/0.00σ; CFG8 refit median e > 0 at 1.7–3.0σ, environmental slope 0.55–0.87 ± 0.25, rank p 0.57–0.87 | CFG7 .out; CFG8_README.md |
| 1.16 | Coma UDGs under the external field: +1.159/+1.112 dex, 4.9/4.7σ | CFG31 .out (R7, from L23) |
| 1.18–1.26 | the bare law's rows (no B rule), EFE omitted | GATES_STATUS rows |
| 2.01 | horn D: additive reading 1.27–1.37 (8.4–10.6σ), a lower bound; horn N: law alone short, η 1.68–2.03 | CFG4_README.md; CFG4_clusters.out |
| 2.02 | horn D: collisionless dust as B's cosmic share (4.6×/4.9× needed) | CFG4_clusters.out |
| 3.01, 3.12 | AeST's CMB fit (LIT); only SZ21's "Exp" set meets the galactic μ bound (as the record quotes SZ21); N9 theorem; F1 ≥ 20 km/s at z = 3 | AEST_BOUNDARY_CONDITION_CLOSURE.md; condensate_mu_pincer_2026.out; CONDENSATE_NOGO_THEOREM.md |
| 3.05 | charge-fixed boundary: Δχ² ≥ +106; free constant: −0.5 to −4.9 (H1a); web-field EFE: +404/+415, +47/+52 inside 0.3 Mpc | aest_boundary_condition_closure_2026.out; BS3_isolated_field_two_halo.out |
| 3.10, 3.11, 5.13 | flat a₀(z) and the tie (L1–L5 HERE); κ 0.46, 0.29σ | GATES.md 3.11 |
| 4.01 | EFE quadrupole 3.99–5.69× (strict P2 law); monopole tail ν_mono 3011/2894/3620/3479×, P2 1279/1258/1545/1520× (re-derived HERE as a control) | CFG1_evidence_audit.out A01; CFG185 README |
| 4.02, 4.03 | c_T = c (LIT, the record's transcription); γ = 1 (the record's completion script C1–C2) | bridge1_aest_equations.md; completion script |
| 4.04 | α₁ = −2(K_B+2) (v9 kill; named residual: solar-profile background) | V9_PPN_KILL_VERDICT.md; CFG172 README §3 |
| 4.06 | Arm A 1.1614–1.1814 / 1.1917–1.2267 applies (not B's Arm C 1.000) | PREREGISTRATION_DR4.md |
| 4.08 | KM1 not transferable; kinematic 𝒴 shift under a boost HERE; CFG186 pending | KM1 README; CFG186 FROZEN_QUESTION.md |
| KiDS split | UNSCORED (an EFE theory predicts an environment-correlated difference not computed) | CFG61/67/110 |

## 4. Hand expectations (disclosed; not repaired if wrong)

- L1–L8 pass (the construction is XR20 T1 / CFG43 applied to AeST's 𝒥).
- The scorecard comes out worse than B on the EFE-sensitive rows (satellites, Coma UDGs, DF2, the Solar System) and on the clusters (X-COP fails on both horns), better on Chae, on having an action, and on c_T/γ. The KiDS gate fails on the record's own AeST closure. Galaxies (1.01) are CONDITIONAL.
- The tie changes no data row: untying it (MUTATE=1) changes only the bookkeeping rows 3.11/5.13 and the constant count.

## 5. Controls

- **C1** a₀ from FP0's ρ_Λ with κ = ½ is 9.3603e-11 and Λ/α² = 32π (XR20 C3: 100.530965).
- **C2** without the multiplier (T^μ removed), Λ's own equation is local and algebraic: for the deep-MOND j it pins 𝒴/α² to a constant and makes Λ vary with 𝒴 (the FP5 D3 behaviour); so the multiplier is what makes the tie global.
- **C3** the record's jeans Part E overshoot (Route A kernel) is reproduced: 2.06–4.42×.
- **C4** tails: P2 h → ½ − 1/(8y) (sympy); the RAR kernel's h decays above Y_P; ν_mono's floor value H_P = 0.648; CFG185's Earth ratios (ν_mono 3011×, P2 1279×, canonical) reproduced to 0.5%.
- **C5** E(z) = 1.322, 1.791, 3.769, 8.294, 20513.65 at z = 0.5, 1, 2.5, 5, 1100 reproduces FP0's committed `a0z_rival_E` to 10⁻⁶ (used by MUTATE=2).
- **C6** every carried anchor is found verbatim in its file.

## 6. MUTATE (each writes its own outputs, named by mode; each must exit 1)

- **MUTATE=1 (untie):** α(Λ) → a constant a₀ independent of Λ (plain AeST with an HT Λ beside it). Must fail **L1** and **L7**. Reported: which scorecard rows change.
- **MUTATE=2 (tie to the flow's expansion):** a₀ ∝ θ = ∇_μA^μ (the owner's "compaction" read as the tie variable) instead of Λ. Must fail **L1** and **L5** (expect a₀(2.5)/a₀(0) = 3.769, the rival law).

## 7. Scope (what this is not)

- Not a derivation of κ or of the tie. Not a new AeST calculation beyond the sympy structure checks, the tails, the kinematic boost, the overshoot arithmetic and the α₁-formula evaluation; every other row is carried or UNSCORED.
- Literature facts (AeST's CMB and P(k) fits, c_T = c, its quasi-static MOND limit with an EFE, its ghost-freedom) are as the record quotes them or from memory, and are marked UNVERIFIED; no paper was re-read (no network).
- Nothing here says the theory is closed, that the data favour the framework, or that a dark-matter particle is needed: the dust is a state of the scalar field, and the mass is still required.
