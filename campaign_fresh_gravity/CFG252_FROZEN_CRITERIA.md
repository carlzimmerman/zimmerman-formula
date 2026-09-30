# CFG252 — dark energy as the void–wall expansion difference ("between the bands"): FROZEN CRITERIA

Written 2026-09-29, before `CFG252_timescape_between_the_bands/CFG252_handcheck.py` existed and before any number in this lane was computed by a script. Nothing below may change after a script number is seen. Any later deviation goes in the lane README as a disclosed departure. Status: phase 1 (criteria plus a hand-check on literature parameters from memory). The orchestrator reviews and commits this file. **κ = ½ is FITTED, not derived.** Label for the whole lane: **NON-DIAGNOSTIC** for the framework-vs-ΛCDM question. This is a consistency hand-check of a premise swap, on unverified literature numbers. Nothing here says the theory is closed or that any data favour it.

## 0. What the author knew before writing (blindness disclosure)

- The a₀/(cH₀) coincidence: a₀ ≈ 0.14 cH₀ on the canonical footing (CFG174, CFG181). So any reading of the form κ′cH with κ′ ~ 0.1–0.2 and H ~ 50–75 km/s/Mpc was known in advance to land within a factor of about 2 of a₀. The rate readings (a) are therefore **not blind to their order of magnitude**.
- While reading the record, the author estimated mentally that reading (b1) is of order 10² a₀ and that reading (b2) is of order 0.5 a₀. (b2) was added to the menu after that estimate, so it is **post-hoc-flagged** and capped at p* (§5).
- These committed numbers were read before this file was written. They are record inputs, not new data:
  - the SPARC profile table in `real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.out`. Its clustered 2σ interval was estimated mentally at about [0.93, 1.27] × 10⁻¹⁰;
  - the environment slopes in `prep_2026/a0_line/cosmic_web_environment_results.json` (1c12985d2);
  - CFG182's A₉₅.
- No timescape number was looked up. Every literature value below is **from memory, unverified**, and names the citation the data chat should check in phase 2.

## 1. The idea (neutral wording)

The owner's idea, a mutation of door 11: between the bands of galaxies, read as the walls and filaments of the cosmic web, one feels the dark energy "slip by". The mutation under test is that **dark energy is not a constant vacuum but the difference in expansion between voids and walls**. The published family closest to this is the "timescape" model and related backreaction work (intended citations: Wiltshire 2007, New J. Phys. 9, 377; Wiltshire 2007, PRL 99, 251101; Wiltshire 2009, PRD 80, 123512; Buchert 2000/2008 for the averaging formalism; all from memory, unverified).

**Record check.** `grep -ril timescape` over the repository (excluding .git) finds 6 files. They are 3 scripts and their 3 outputs in `real_research/reviews/`: `mi_phantom_artifact_2026`, `mi_phantom_reframings_audit_2026` and `mi_lowz_anchor_sign_2026`. Each names timescape only as prior art ("the local-void/timescape literature owns the mundane version"). **No timescape calculation exists in the record.** The brief's claim that grep finds nothing is therefore not literally right, but its substance holds.

## 2. Why it matters to the framework

- The tie is a₀ = κ c √(Gρ_Λ) with κ = ½ FITTED. With ρ_Λ = 3H₀²Ω_Λ/(8πG), it is a₀ = κ c H₀ √(3Ω_Λ/(8π)) (ChainCert `A0Numeric.a0_of_rhoLambda`).
- The footings are canonical 9.3603e-11 (ρ_Λ, Ω_Λ = 0.6847, H₀ = 67.4) and alt 1.1312e-10 (ρ_total, i.e. Ω → 1) m/s².
- The certified `a0_numeric` is conditional on the ρ_Λ input and on `chain.hflat` (ρ_Λ constant in z).
- **Under the mutation there is no ρ_Λ**, so both premises lose their object. The tie must be re-expressed in the mutation's own quantities, or it fails. Those quantities are:
  - the dressed (wall-observer) and bare (volume-average) Hubble rates;
  - the void fraction f_v;
  - the lapse (clock-rate ratio) γ̄.

## 3. The model used: the timescape tracker solution (from memory, unverified)

Volume-average time is t. Intended citations: Wiltshire 2009 PRD 80, 123512 and Duley, Nazer & Wiltshire 2013 CQG 30, 175006. The script checks only that these relations are **internally consistent** (sympy). Whether they are the literature's equations is a phase-2 check.

- **T1.** f_v(t) = 3 f_v0 H̄₀ t / [3 f_v0 H̄₀ t + (1 − f_v0)(2 + f_v0)].
- **T2.** Wall and void rates in volume time are H_w = 2/(3t) and H_v = 1/t. The bare rate is H̄ = (1 − f_v)H_w + f_v H_v = (2 + f_v)/(3t).
- **T3.** The wall lapse is γ̄ = dt/dτ_w = 1 + f_v/2 = H̄/H_w. The tracker's uniform-quasilocal-expansion postulate is that each region measures H̄ in its own proper time. This gives the void lapse dt/dτ_v = (2 + f_v)/3.
- **T4.** The dressed (wall-observer) rate is H = γ̄H̄ − dγ̄/dt = (4f_v² + f_v + 4)/(6t).
- **T5.** Dressed redshift: 1 + z = (2 + f_v) f_v^{1/3} / (3 f_v0^{1/3} H̄₀ t).
- **T6.** The bare densities are Ω̄_M = 4(1 − f_v)/(2 + f_v)², Ω̄_k = 9f_v/(2 + f_v)² and Ω̄_Q = −f_v(1 − f_v)/(2 + f_v)², which sum to 1. The dressed matter density is Ω_M = γ̄³Ω̄_M = (1 − f_v)(2 + f_v)/2.
- **T7.** t₀ = (2 + f_v0)/(3H̄₀). The tracker is fixed by (f_v0, H₀ dressed), with H̄₀ = 2(2 + f_v0)H₀/(4f_v0² + f_v0 + 4).

**Parameter sets (from memory, unverified; verdicts at P-A only):**

| set | f_v0 | H₀ dressed (km/s/Mpc) | intended citation | recalled derived values (checked for memory consistency only) |
|---|---|---|---|---|
| **P-A (primary)** | 0.695 | 61.7 | Wiltshire 2009; Duley, Nazer & Wiltshire 2013 | H̄₀ ≈ 50.1, γ̄₀ ≈ 1.35, Ω_M0 ≈ 0.41 |
| P-B | 0.76 | 61.7 | Leith, Ng & Wiltshire 2008, ApJ 672, L91 | Ω_M0 ≈ 0.33, γ̄₀ ≈ 1.38 |
| sweep | 0.55–0.85, step 0.05 | 60.0, 61.7, 64.0 | covers recent Pantheon+ fits (Lane et al. 2025, MNRAS; Seifert et al. 2025, MNRAS Lett.), whose values are not recalled reliably | robustness only |

**The sweep rule.** The sweep is a robustness band over the premise's own literature uncertainty. It is not a knob and it adds no constant. A verdict that flips inside the sweep is labelled **parameter-dependent**, and no sweep point can turn a P-A FAIL into a PASS.

**Candidate rates at z = 0:**
- H1: the dressed H₀ (wall observer, global);
- H2: the bare H̄₀ (volume average; also the rate every region measures in its own time, T3);
- H3: the void rate in volume time, 1/t₀;
- H4: the void rate as timed by wall clocks, γ̄₀/t₀;
- H5: the wall rate in volume time, 2/(3t₀).

## 4. Readings (scored separately, never pooled)

### (a) Tie by rate: a₀ = κ′ c H

κ′ is fixed a priori by the framework's own conversion, κ′ = κ √(3Ω_Λ^eq/(8π)) with κ = ½. The only freedom is which Ω_Λ-equivalent the mutation supplies. Declared options, and no others:

- **a-0, literal.** The mutation has no Λ: Ω_Λ^eq = 0, so κ′ = 0 and a₀ = 0.
- **a-1, total density** (the record's alt footing: ρ = 3H²/(8πG) of the chosen H). Ω_Λ^eq = 1 and κ′ = ½√(3/(8π)) = 0.17275, applied to H1–H5.
- **a-2, non-matter fraction on the matching average.** Ω_Λ^eq = 1 − Ω_M, with the pairs:
  - (H1, 1 − Ω_M0 dressed);
  - (H2, 1 − Ω̄_M0 bare) = Ω̄_k + Ω̄_Q, the backreaction-plus-curvature share;
  - (H3/H4, void: Ω_M = 0, giving 1);
  - (H5, wall: Ω_M = 1 locally, giving 0).
- **a-3, borrowed apparent Ω_Λ.** Ω_Λ^eq = 0.6847, the Planck ΛCDM value the chain uses, with each H. **This reinstates the number the mutation removes, so it cannot PASS.** It is reported for completeness only, as a restatement row.

Any κ′ chosen to match the band counts as a fit, not a pass.

### (b) Tie by lapse

- **b1, spatial gradient (as briefed).** a = c² Δ/L, with:
  - Δ ∈ {γ̄₀ − 1 (wall against volume average), H_v/H_w − 1 (wall against void, both in volume time)};
  - L ∈ {10, 30, 50} Mpc.
  - Reported only: the velocity such an acceleration would impart in 1 Gyr, against observed void outflows of a few hundred km/s (from memory, unverified).
- **b2, temporal lapse rate (POST-HOC-FLAGGED, §0).** a = c dγ̄/dt (volume time) and c γ̄ dγ̄/dt (wall time), with dγ̄/dt = f_v(1 − f_v)/(2t) in the tracker.
  - Possible prior art: in the timescape literature the relative deceleration of regional frames under the "cosmological equivalence principle" has been compared with the MOND scale. That is from memory and unverified; phase 2 must check it (intended citation: Wiltshire 2008, PRD 78, 084032).
  - b2's class is capped at p*.

### (c) Environment

- **c-own.** Each region reads its own-clock H. By the tracker's postulate that is H̄ everywhere, so the contrast is 0. G-T2 then passes trivially, because the premise enforces it; the label is p*. Its a₀ is the H2 row of (a).
- **c-common.** Regions read H in a common (volume) clock. The void/wall a₀ ratio is H_v/H_w (3/2 in the tracker), so voids are higher by log₁₀(H_v/H_w) dex. The mapping to the record's slope d log₁₀ a₀ / d log₁₀(1 + δ) is two-phase:
  - δ_w = f_v0/(1 − f_v0), with all the matter in the walls;
  - δ_v = −0.8 (primary; the record's DELTA_VOID) or −0.9 (variant);
  - s = −log₁₀(H_v/H_w) / [log₁₀(1 + δ_w) − log₁₀(1 + δ_v)].
- **c-local.** The a-2 tie applied region by region. A wall is locally Ω_M = 1, so Ω_Λ^eq,wall = 0 and a₀ = 0 in walls, where the idealised model puts every galaxy.

## 5. Gates

**G-T1 (value).** Is a₀ inside the SPARC 2σ band without tuning?

- **Primary band S1.** The clustered 2σ interval of the SPARC per-galaxy-Υ profile likelihood: {a₀ : Δχ²(a₀)/19.314 ≤ 4}, where 19.314 = 3380/175 is the note's clustering inflation squared.
  - It is linearly interpolated from the committed table in `mi_a0_profile_likelihood_milgrom_footing_2026.out`.
  - The script re-derives the note's minimum (1.0766e-10) and Δχ²(0.9361e-10) = 63.90 as controls.
- **Reported, not verdict-changing:**
  - S2: best × (1 ± 2 × 0.0544), the note's linear clustered error. On S2 the canonical footing itself sits at −2.40σ; this is disclosed, and it is why S2 is not primary.
  - The fitted κ windows (CFG0 F3; CFG117), 0.465 ± 0.076 (BTFR) and 0.55 ± 0.17 (distance-free), converted to a₀ = (κ/½) × 9.3603e-11.
- **Also reported for every row:** a₀/a₀_can, a₀/a₀_alt, and the equivalent κ on the ρ_Λ footing.
- **Premise:** the SPARC band is taken as measured. Timescape is not used to re-calibrate SPARC distances; that is a phase-2 question.

**G-T2 (environment).** No environment dependence beyond the committed limits.

- **Primary limit:** the 2M++ real-space slope with clean (redshift-independent) distances, N = 52: −0.0832 ± 0.1352 (`cosmic_web_environment_results.json`).
  - It is primary because a local-H a₀ corrupts Hubble-flow distances with a sign-flipping confound, as that script's own header derives.
  - The record's clean sample has **0 deep-void galaxies**.
- **Secondary limit:** 2MRS counts, clean, N = 38: +0.0286 ± 0.0751. This is galaxy counts. Bias b = 1 is primary and b = 1.3 is a variant; the predicted slope is divided by b.
- **Reported only:**
  - the ALL and Hubble-flow rows (confounded);
  - the ρ_local exclusion (13σ SBeff, ~34σ kNN, ~7.5σ Ursa Major; `a0_environmental_fork_test.py`, EMPIRICAL_TESTS A14; memory note says 7–34σ). That exclusion tests slope **+0.5, the opposite sign** to c-common, so it is recorded **N/A** for any void-enhanced reading;
  - the SPARC-self kNN slope −0.010 ± 0.015. It is not mapped, because a kNN density among SPARC galaxies is not 1 + δ of the matter and the record has no calibration.
- **Rule per row:** z = (pred − meas)/σ.
  - FAIL if |z| ≥ 3; TENSION if 2 ≤ |z| < 3; CONSISTENT otherwise.
  - Also **UNDERPOWERED** if |pred|/σ < 2, meaning the limit cannot separate the prediction from zero.
- **Sky dipole.** CFG182 gives A₉₅ = 0.43 (CFG192: 0.40).
  - A rate-tied a₀ inherits the local Hubble-flow anisotropy. The declared input (from memory, unverified: Wiltshire, Smale, Mattsson & Watkins 2013, PRD 88, 083529) is a fractional variation of 0.01–0.05 within ~100 Mpc.
  - CONSISTENT and NON-DIAGNOSTIC if 0.05 < A₉₅/2.
  - CFG182's post-hoc Hubble-flow subsample result is not scored.

**G-T3 (a₀(z)).** For each surviving reading, compute a₀(z)/a₀(0) at z ∈ {0.85, 1.5, 2.2, 2.5, 5.0}. Compare it with flat (1) and with the rival E(z) (Ω_m = 0.3153, `CFG7_common.OM_PL`).

- **Classes at z = 1.5:**
  - flat-like: |Δlog| ≤ 0.05 dex;
  - rising: above +0.05 dex. Rising is also "rival-like" if within 0.1 dex of log E;
  - falling: below −0.05 dex.
- **Committed results that bear on it:**
  - KURVS z ≈ 1.5 (CFG140–CFG194): a lean to the rival that is fragile and calibration-bound; not a detection.
  - CFG213 z ≈ 5: the rival is DISFAVOURED-under on the fit route, ROUTE-DEPENDENT; z ≈ 1.4 gives no separation.
  - CFG197 z > 3.5: both laws consistent, one-sided.
  - CFG196 z ≈ 2.2: cannot discriminate.
  - CFG190/198 MUSE-DARK: nothing established.
- **Grade:** NOT DECIDED, unless a committed result robustly excludes the reading's law; none does.
  - A reading whose rise at z = 5 reaches at least E(5) × 10^−0.1 **inherits** CFG213's route-dependent disfavour.
  - A smaller positive rise "partially bears", and is not scored.
  - If no reading is flat-like, record that **the mutation forfeits the framework's distinctive flat a₀(z)**.

**G-T4 (premise).** Does timescape itself survive current data? This is a gate on the premise, recorded from memory and **not tested here**. Grade: PREMISE CONTESTED (from memory, unverified). The README lists:
- the SN analyses claiming support;
- the CMB, H₀ and BAO/DESI tensions;
- the theoretical objections;
- the numerical-relativity bounds on backreaction.

## 6. Classes per reading, and the restatement rule

- **DIES:** a₀ = 0 or undefined for the galaxies SPARC measures, or more than 1 dex from a₀_can.
- **FAIL:** outside S1 at P-A, or G-T2 FAIL on the primary limit.
- **p* (restatement):** inside S1 but one of the following:
  - MUTATE-invariant: the same a₀ within 1% when f_v0 → 0 at fixed dressed H₀, which is the a₀/(cH₀) coincidence of CFG174/CFG181 in any cosmology;
  - borrowed (a-3);
  - post-hoc (b2);
  - enforced by the premise (c-own).
- **PASS (G-T1 only):** inside S1, κ′ fixed a priori, and the value changes when the void–wall structure is removed.

**Restatement is not a pass.** A reading that lands in the band because a₀ ≈ 0.14–0.17 cH for any H of 55–75 km/s/Mpc has shown the coincidence, not a mechanism. No reading can be graded as supported in this lane.

## 7. MUTATE and outputs

- **`MUTATE=1`** sets f_v0 → 0 at fixed dressed H₀. This is the exact Einstein–de Sitter limit, handled analytically: γ̄ = 1, H̄ = H_w = H, dγ̄/dt = 0, Ω_M = 1.
  - **Required behaviour:**
    - the load-bearing premise check L1 (f_v0 > 0, so a non-matter fraction > 0 and a lapse > 0) fails, and rc = 1;
    - a-2, b1, b2, c-common and c-local go to zero;
    - a-1 is unchanged, which shows it is blind to the void–wall structure.
  - The headline line must differ between the modes.
  - Outputs: `CFG252_handcheck.out` / `CFG252_handcheck_results.json`, and `CFG252_handcheck_MUTATE.out` / `CFG252_handcheck_results_MUTATE.json`.
- **Controls, holding in both modes:**
  - C0: the conversion reproduces FP0's a₀ values from its committed H_Λ.
  - C1: the SPARC table re-derives the note's minimum and Δχ².
  - C2: the tracker identities T1–T7 hold in sympy.
  - C3 (reported, not load-bearing): the P-A and P-B trackers reproduce the recalled derived values. This checks memory consistency, not the literature.

## 8. What phase 2 would need (not done here)

1. The data chat verifies every "from memory" value and equation against the papers, and corrects this file only by an appended addendum. That covers T1–T7, P-A, P-B, the recent Pantheon+ fits, the Hubble-flow variance, the CMB and BAO status, and the prior-art question on b2.
2. If any reading earns PASS at G-T1, the next step is its G-T3 a₀(z) confrontation through the committed high-z pipelines (CFG213's DysmalPy route, CFG197's floor, the KURVS P4 map), frozen before any number.
3. c-common needs deep-void galaxies with redshift-independent distances. The record has none; the committed power estimate is about 266 clean galaxies against 52 (N_needed_3sig_alt).
