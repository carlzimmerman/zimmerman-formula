# kappa_slot_2026 — the ε_tot = 1/(32π) slot, swarmed (2026-09-16)

**The question.** In the graviton-bath crossover form the framework's coefficient obeys
κ² = 8π ε_tot exactly (a₀² = 3 ε_tot c² H_Λ², H_Λ² = 8πGρ_Λ/3), so κ = ½ ⟺ ε_tot = 1/(32π).
ε_tot is the dimensionless fluctuation-energy fraction a worldline in the de Sitter static patch sees from the graviton bath through the forced nonlinear coupling −X²/8 of S = −m∫√(1+X), X = h_μν u^μ u^ν.

**The two committed lanes that disagree, and both must be read first:**
- `real_research/reviews/mi_graviton_bath_ctp_2026.py` (2026-08-09, 15/15): summing the per-mode variance ε₁ ~ G T_dS²/8 over N = S_dS = π/(GH²) horizon modes gives ε_tot = S_dS·ε₁, a PURE NUMBER; normalisation A (⟨h²⟩ = G T²) gives ε_tot = 1/(32π) ⇒ κ = ½ exactly; the standard normalisation B (h = √(32πG) φ, ⟨φ²⟩ = T²/12) gives ε_tot = 1/12 ⇒ κ = 1.447; B with two polarisations 1/6 ⇒ 2.047. The lane's own text: "I chose A loosely."
- `qwen_claude_field_theory/closure_2026/a0_promotion_2026/graviton_bath_ctp_drift_2026.py` (2026-09-01): the CTP rectified drift evaluated: every Λ-dependent term is O(ħ), the drift is a fraction n/(6 S_dS) of H²r (∝ 1/S_dS ≈ 1e-122), proportional to r (a Λ renormalisation, not a constant a₀), and shapeless (f(T) = T² ⇒ q = 0 in the crossover master formula). Its verdict: the mechanism cannot deliver κ; the only rescue is "holographic coherence: an enhancement of exactly S_dS — a new postulate, category III".

So the slot exists only if the horizon entropy MULTIPLIES (08-09) rather than DIVIDES (09-01). That adjudication is lane KS01; every other lane is conditional on it and must say so in its verdict.

**Standing rules (the same for every lane here):**
1. Test the construction on ITS OWN terms; verify a FAIL as hard as a PASS; never manufacture either.
2. Every check states the measurement and the threshold separately; no literal-True checks; a FAIL is a finding, not a bug to hide.
3. Both a₀ footings wherever a dimensional number appears: canonical 9.3619e-11 (κ = ½, ρ_Λ, H_Λ = H₀√Ω_Λ) and alternative 1.1279e-10 (ρ_crit, cH₀). Ω_Λ = 0.685, H₀ = 67.4.
4. Nothing fed in that contains the answer: no a₀, no Ω_Λ-built number, on the input side of a "derivation". Any candidate that lands on ½ must be checked a SECOND independent way before it is reported (the 08-09 lane's near-miss rule).
5. Convention audit: every π, 2, ħ, k_B, polarisation count and Planck-unit choice that enters ε_tot is listed with its justification; a number that changes under a legitimate convention change is CONVENTION, not a result.
6. Measured band to compare against: κ = 0.465 ± 0.076 (BTFR) and 0.551 ± 0.043 (distance-free); MLS16 g† = 1.20 ± 0.02 (rand) ± 0.24 (syst) ×1e-10 m s⁻². Four candidates already sit inside 2σ; a candidate is only "selected" if the band separates it from its nearest rival.
7. Output: `KS0n_<slug>.py` + `.out` (+ `.json` if useful) in this directory; sympy/mpmath for exact steps; a mutation control where a theorem is claimed (MUTATE=1 must break it). Read-only outside this directory. No commits. No personal names in files.
8. Prior kills you must not re-propose: the de Sitter–Unruh route forces a₀ = 2cH_Λ (excluded 15.6σ; `real_research/reviews/mi_deser_levin_interpolation_2026.py`); the candidate scalar action cannot fix κ (zero-mode theorem, `kappa_closure/k01`); the sequestering-type global constraint falls 1e-5 short (`kappa_closure/k02`); the "cubic noise drift" is evaluated and closed (09-01); Z = 2√(8π/3), a₀ = c²/(Z R_dS), a₀ = Λ²/(2M_Pl) are all κ = ½ restated, not derivations.

**Lanes.** KS01 adjudication (× vs ÷ S_dS) · KS02 normalisation table (conditional) · KS03 rival coefficients and discrimination · KS04 look-elsewhere control · KS05 the category-III enhancement priced · KS06 number field and form.

## 2026-09-18 — the clock hand-off

The covariant-action work moved to `../clock_swarm_2026/CLOCK_WORK_ORDER.md` (status of the four clock constructions, the two theorems every action must respect, how to run every existing lane, and CK02–CK23 in granular detail). Read it before touching any covariant action; the direction-blind programme of this directory is closed (SW07).
