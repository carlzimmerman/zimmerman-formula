# WORK ORDER — derive, or close, the ε_tot = 1/(32π) slot (κ = ½)

**For:** any model or agent track picking this up. **Owner of the field-theory effort:** the lead track (astra); results land here and the lead integrates them. **Do not edit files outside `fable_independent_2026/kappa_slot_2026/`.** Read `README.md` in this directory first; its eight standing rules are binding for every lane below.

---

## 0. The state of the question, in one paragraph

The framework's acceleration scale is a₀ = κ c √(Gρ_Λ) with κ = ½ fitted. Every published "derivation" of κ in this repository is a rewrite of that definition (a₀ = c²/(Z R_dS), a₀ = Λ²/(2M_Pl), the Ω_Λ closure). The only place where κ became a well-posed calculation is the graviton-bath crossover: κ² = 8π ε_tot, where ε_tot is the fluctuation-energy fraction a worldline in the de Sitter static patch sees through the forced nonlinear coupling −X²/8 of S = −m∫√(1+X), X = h_μν u^μ u^ν. The 2026-08-09 lane summed the per-mode variance over N = S_dS horizon modes and obtained a pure number, 1/(32π) under one normalisation (κ = ½ exactly) and 1/12 under the standard one (κ = 1.447). The 2026-09-01 lane evaluated the same rectified drift in closed-time-path form and found it ∝ 1/S_dS (≈ 1e-122), r-proportional and shapeless. The slot is live only if the horizon entropy multiplies rather than divides. Nobody has adjudicated that. That is lane KS01, and everything else is conditional on it.

## 1. Read before writing a line

1. `real_research/reviews/mi_graviton_bath_ctp_2026.py` — the slot's origin; lines 129–133 (ε₁ ~ G T²/8), 158–176 (ε_tot = S_dS·ε₁ and κ² = 8π ε_tot), 197–221 (normalisations A and B), 237–260 (the author's own list of unpinned O(1)s and the near-miss warning).
2. `qwen_claude_field_theory/closure_2026/a0_promotion_2026/graviton_bath_ctp_drift_2026.py` — the closure; parts B (ħ-counting theorem), C (drift = n/(6 S_dS) H² r), D (f(T) = T² ⇒ q = 0), E (the priced rescues).
3. `real_research/reviews/mi_crossover_master_formula_2026.py` — q = 2/r, r ≡ f′(T_GH)/c1p; the map from a temperature-response function f(T) to the coefficient.
4. `real_research/reviews/mi_deser_levin_interpolation_2026.py` — the interpolation function derived from T(a) = √(a²+H²)/2π, and why that route fixes a₀ = 2cH_Λ (excluded 15.6σ).
5. `real_research/reviews/mi_cubic_noise_ctp_2026.py` — the universality screen (a₀ must be mass-independent ⇒ the bath must be gravitational) and the number-field discriminator (rate mechanisms carry √π, density mechanisms may be rational).
6. `kappa_closure/README.md`, `k01`–`k04` — the four closed routes; do not reopen them.
7. `real_research/reviews/mi_a0_profile_likelihood_sparc_2026.py` — how κ = ½ vs 1/2π was separated at 2.2σ (conditional on the α = 1 kernel), and the measured κ band.
8. `fable_independent_2026/L261_wave32_audit.py` — the check() format, the literal-True rule, both-footings rule.

## 2. Common deliverable format

- File: `KS0n_<slug>.py`, runnable with `python3` from the repository root, writing `KS0n_<slug>.out` (tee) and `KS0n_<slug>.json` (every number the verdict uses).
- Every check: `check(name, measured, ok, reading)` with `ok` a computed boolean; threshold stated in `name`. Print a final line `KSnn COMPLETE: p/n checks PASS`. rc = 1 if any check that the lane declares "load-bearing" fails, so the run itself carries the verdict.
- Where a theorem or identity is claimed: sympy exact, plus `MUTATE=1` environment switch that perturbs one hinge (a sign, an exponent, a normalisation) and must make the check fail; print both runs' tallies.
- Both footings (`A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}`, H_Λ = H₀√Ω_Λ vs H₀, ρ_Λ vs ρ_crit) wherever a dimensional number appears.
- A `VERDICT` block at the end, three lines: (1) what was computed, (2) the number(s) with the convention choices that produced them, (3) the honest sentence: DERIVED / CONVENTION / FREE / EXCLUDED / SLOT-NOT-LIVE, with what would change it.
- Append one line per lane to `KS00_INDEX.md` in this directory: `KSnn | verdict word | the one number | the file`.

## 3. The lanes

### KS01 — ADJUDICATE: does S_dS multiply or divide? (the gate for everything else)

**Objective.** Decide whether the 08-09 structure ε_tot = N·ε₁ with N = S_dS is a legitimate mode sum or a double count, by computing the rectified drift ⟨g₂ h_uu²⟩ two independent ways and comparing.

**Procedure.**
1. Set up the static-patch worldline (static observer at the origin, then at proper acceleration a) coupled to a canonically normalised graviton, h_μν = √(32πG) φ_μν (state the polarisation basis explicitly; two TT polarisations).
2. Way 1 (thermal coincidence limit): in the Bunch–Davies state the static-patch observer sees each polarisation as a thermal field at T_GH = ħH/(2πk_B); compute ⟨h_uu²⟩ from the thermal two-point function at coincidence with the standard result ⟨φ²⟩_T = T²/12 per massless scalar degree of freedom (state the regularisation; subtract the Minkowski vacuum piece and say so). Express ε₁ ≡ (the −X²/8 term's energy per unit rest energy) and write it in Planck units. This is the 09-01 route: the thermal variance already sums over all modes.
3. Way 2 (explicit mode sum): write the static-patch mode expansion, sum the per-mode variance over modes with wavelength between the horizon and the Planck length, and count them; show whether the count is S_dS, S_dS^{1/2}, or O(1) after the UV subtraction, and whether the per-mode variance that multiplies it is ε₁ or ε₁/N. Do this symbolically in ħ, G, H so the ħ-counting of the 09-01 lane can be checked term by term.
4. The crux check: **C1** — do Ways 1 and 2 agree on the ħ- and S_dS-scaling of ⟨h_uu²⟩? If Way 2 reproduces Way 1 (the mode sum IS the thermal variance), then multiplying by S_dS is a double count and the slot is not live. If Way 2 differs by a factor S_dS, identify the physical assumption that produced it (phase coherence across horizon modes? a classical rather than quantum variance? counting area cells rather than field modes?) and state it as a postulate with a name.
5. **C2** — the r-proportionality: show whether the drift is ∝ r (a renormalisation of Λ) or a constant; a constant a₀ requires the drift to be r-independent at large r; test both ways.
6. **C3** — the shape: with T(a) = √(a²+H²)/2π (Deser–Levin), compute f(T) implied by the drift and its q = 2/r value from the master formula; q = 0 means no interpolation function.
7. Mutation: MUTATE=1 replaces T_GH by an ħ-free temperature; the ħ-counting conclusion must flip.

**Verdict template.** "The horizon entropy [multiplies | divides]; the 08-09 pure number is [a legitimate incoherent sum | a double count of the thermal variance]; the slot is [LIVE under the named postulate | NOT LIVE]." If NOT LIVE, KS02 and KS05 still run but must open with that sentence.

### KS02 — the normalisation table (conditional on KS01)

**Objective.** Assuming the multiplicative structure, pin every O(1) and report whether 1/(32π) occurs under any standard convention set.

**Procedure.**
1. Build ε_tot = N · c_pol · c_2pt · c_proj · c_norm · G T² / 8 with each factor a named symbol, then evaluate over the full grid: N ∈ {S_dS = A/4G, A/G, number of horizon modes counted explicitly in KS01}; c_pol ∈ {1, 2}; c_2pt ∈ {1 (loose A), 1/12 (thermal massless scalar), 1/6 (two components), the correct value for a TT graviton per polarisation that you derive}; c_proj = the h_μν u^μ u^ν projection for a static observer (derive it; state the frame) and separately for an accelerated observer at T(a); c_norm ∈ {32πG (canonical), 16πG, 8πG (list who uses which)}.
2. Print the table: convention set → ε_tot → κ = √(8π ε_tot) → distance from the measured band (both footings).
3. **C1** — is there a convention set in which every factor is the standard one (no "loose" entry) that gives ε_tot = 1/(32π) to better than 1%? **C2** — how many of the grid's cells land inside the measured 2σ band (this is KS04's prior, computed here for the physics grid)? **C3** — the 08-09 near-miss reproduced: A gives ½, B gives 1.447, B×2 gives 2.047.
4. Second independent way (rule 4 of the README): whichever set lands closest to ½, recompute it from the energy density of a thermal graviton gas at T_GH divided by ρ_Λ, times the mode-count enhancement, and confirm the same number.

**Verdict template.** "Under standard conventions ε_tot = [value]; 1/(32π) is reached [only with the loose choice X | with the standard set Y]; the number is [CONVENTION | CANDIDATE]."

### KS03 — every rival coefficient as (κ, ε_tot), and what discriminates them

**Objective.** Put the framework's ½ on the same footing as every published a₀–Λ coefficient and state what measurement separates them.

**Procedure.**
1. Tabulate, each with its source and its footing (cH₀, cH_Λ, c√(Gρ_Λ), c√(Gρ_crit)): Milgrom 1983/1999 a₀ ≈ cH₀/(2π); Milgrom 2020 (r = 4π ⇒ q = 1/2π); the Deser–Levin/Unruh construction a₀ = 2cH_Λ; Verlinde 2016 a₀ = cH₀/6; the framework's κ = ½; the graviton normalisations B (1/12) and B×2 (1/6); the CKN seesaw form; any other in `kappa_closure/README.md`. Convert every one to κ ≡ a₀/(c√(Gρ_Λ)) and to ε_tot = κ²/(8π), on both footings.
2. Compare to the band: κ = 0.465 ± 0.076 (BTFR), 0.551 ± 0.043 (distance-free), and MLS16's g† converted (1.20 ± 0.02 ± 0.24). **C1** — list which candidates are inside 2σ of each measurement. **C2** — the minimum precision on κ needed to separate ½ from its nearest surviving rival at 3σ. **C3** — the H₀-tension degeneracy (repeat `kappa_closure/k03`'s logic): which candidate pairs move together under Planck-vs-SH0ES ρ_Λ, so that the "derivation" is degenerate with a cosmological systematic.
3. State the one observation that would decide: the deep-MOND Tully–Fisher zero point at z ≈ 2.5 to ±0.13 dex (already registered; do not re-register), or a κ measurement to ±5% in one homogeneous channel — and say which candidates it kills.

**Verdict template.** "N candidates inside 2σ; ½ separated from [rival] at [x]σ today; needs ±[y]% on κ; degenerate with the H₀ tension: [yes/no]."

### KS04 — the look-elsewhere control

**Objective.** Price any future landing on ½ before it is reported.

**Procedure.**
1. Enumerate dimensionless expressions from the alphabet {1, 2, 3, 4, 6, 8, π, √π, √2, √3, e, ln 2} with at most k operations (k = 2, 3, 4) — reuse `project_atomos` enumeration machinery if it imports cleanly, otherwise write a small enumerator; deduplicate numerically at 1e-9.
2. For each k, count expressions inside the measured κ band (each footing, 1σ and 2σ) and inside the ε_tot band (κ²/8π). Report the fraction: this is the probability that a random "natural" number explains κ at the current precision. **C1** — the fraction at k = 3 for the 2σ band; **C2** — the same at the ±5% precision KS03 says is needed; **C3** — the rank of ½ and of 1/(32π) among the in-band expressions by complexity.
3. Do not interpret; just report the numbers with the enumeration size. This lane is a control, not a search.

**Verdict template.** "At today's precision a fraction [p] of ≤k-operation natural numbers land in the band; at ±5% the fraction is [p′]."

### KS05 — the category-III enhancement, priced

**Objective.** The 09-01 lane says the mechanism needs "an enhancement of exactly S_dS". Examine the three known structures that could supply it and say whether any does so without a new free parameter.

**Procedure.**
1. Verlinde 2016 (emergent gravity): write his a₀ = cH₀/6 as an ε_tot and identify in his derivation the step that plays the role of the S_dS multiplication (the entropy displacement ∝ horizon entropy). State whether the enhancement is derived or postulated there, and whether it lands on 1/(32π) (it does not; compute the ratio).
2. de Sitter IR secular growth (stochastic inflation): ⟨φ²⟩ grows as H³t/(4π²); compute the number of e-folds for the massless-graviton variance to reach the value the slot needs; compare with the 09-01 estimate "~S_dS e-folds"; state whether the static patch's finite age forbids it.
3. A primordial tensor background: with the tensor-to-scalar ratio ceiling (state the value and source) compute the maximal ε_tot such a background supplies today; compare with 1/(32π).
4. Any fourth structure the executor can name, with the same three questions: is the S_dS factor derived, what number does it give, what does it cost.
5. **C1–C4** — for each: reaches 1/(32π) within a factor 2 [yes/no]; introduces a free parameter [yes/no]; is excluded by an existing bound [yes/no, which].

**Verdict template.** "Of the enhancement structures examined, [n] reach the needed factor; [m] do so without a new parameter; the slot is [closed with the mechanism | open under postulate X, priced at Y]."

### KS06 — number field and form

**Objective.** Make the discriminator exact: which mechanism classes can produce a rational κ, and is 1/(32π) itself a convention-free number?

**Procedure.**
1. Prove (sympy) κ² = 8π ε_tot from a₀² = 3 ε_tot c² H_Λ² and H_Λ² = 8πGρ_Λ/3; hence κ ∈ ℚ ⟺ ε_tot ∈ ℚ/π. Show where each π in 1/(32π) = π · (1/8) · (1/4π²) comes from: S_dS = π/(GH²), the 1/8 of the coupling, T = H/2π. Then list which of these are conventions (ħ = k_B = 1; T_GH's 2π; A/4G) and which are physics.
2. The universality screen for this mechanism: with the −X²/8 coupling, show whether the drift per unit rest mass is m-independent (it must be for an a₀); sympy.
3. The rate-vs-density classification: a mechanism whose natural output is cH carries the √(8π/3) conversion (Z = 2√(8π/3)) and cannot give a rational κ without a compensating √π; a mechanism whose output is c√(Gρ) can. Classify the graviton-bath route: its output is a₀ = cH × (pure number) per the 08-09 lane; state what that implies for the number field of κ under that route and whether it is consistent with the rational ½.
4. **C1** — the identity chain holds exactly; **C2** — m-independence; **C3** — the classification is stated with the compensating factor identified or shown absent.

**Verdict template.** "1/(32π) decomposes as [chain]; [k] of its factors are conventions; the graviton route is a [rate | density] mechanism and a rational κ [is | is not] available in it."

## 4. What counts as success for the whole slot

κ = ½ is DERIVED only if all of the following hold, each as a committed PASS with its script: KS01 finds the multiplicative structure legitimate under a named, independently motivated postulate (or with no postulate); KS02 finds 1/(32π) under a fully standard convention set and confirms it a second independent way; KS06 finds the number field consistent; KS04's control shows the landing is not what a random natural number does at the current precision; KS03 shows the band can separate ½ from its rivals, or names the measurement that will. Anything less is reported as exactly what it is: CONVENTION, FREE, or SLOT-NOT-LIVE. If KS01 returns NOT LIVE, the correct closing sentence for the programme is: "κ is a measured constant of the framework, not a derived one; the graviton-bath slot is closed with its mechanism", and the remaining lanes are context, not rescue.

## 5. Reporting

- Do not announce a derivation in a commit message before the second independent computation of rule 4 exists in the same commit.
- Every FAIL line stays in the `.out`; do not re-run with changed thresholds.
- The audit that will read this work is `L261`-style: it counts literal-True checks, it re-runs every script, and it reads the FAIL lines before the verdict.
