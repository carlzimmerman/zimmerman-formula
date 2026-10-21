# p63 — a₀ as a field: can an identification or a quantization fix k04's ratio Z/β²? (frozen criteria, committed alone)

**Status: FROZEN 2026-10-19, before any p63 script exists.** Runs are sympy/arithmetic only, and they start only when no
1024³ job is live (CFG654 chain6 NCS0 → NC1x was running at freeze time). Append-only after this commit.

## Question

k04 (`kappa_closure/k04_four_form_promotion_consistency.py`, F2) promoted a₀ to a four-form flux q, with vacuum
P(q) = Zq²/2 + bβ²q² and a₀ = β√G|q|. The flux amplitude cancels and

    κ² = a₀²/(G ε_vac) = 2β²/(Z + 2bβ²),   κ = ½  ⟺  Z/β² = 8 − 2b = 7.964 (K_B = 0).

Z/β² is a free ratio of two couplings. This is the last shape that the general arguments of 2026-10-19 leave open (memory
note `project-puzzle-32pi-campaign`, 10-19 block): a₀ as a field, with the ratio fixed by an identification or by
quantization rather than chosen. **Does any construction below fix Z/β² (equivalently κ), with no continuous free
coupling, no ħ in κ, and a value inside the measured window?**

## Target window (frozen; from committed sources, not from p62's unrun output)

κ_Λ := a₀/(c√(Gρ_Λ)) and κ_crit := a₀/(c√(Gρ_crit)) = κ_Λ√Ω_Λ, with registers of GF1 (Ω_Λ = 0.685, ρ_crit = 8.533238720309458e-27).

- **PRIMARY:** distance-free κ_Λ = 0.551 ± 0.043 (`opus_48_extended_research/papers/THE_HORIZON_FORM_OF_THE_BTFR.md` §6.1),
  2σ ⇒ κ_Λ ∈ [0.465, 0.637] and κ_crit ∈ [0.385, 0.527]. A candidate is IN only if it lands inside on **both** footings.
- **SECONDARY (reported, not decisive):** method spread κ_Λ ∈ [0.444, 0.700]: p48 pool 8.318e-11
  (`sonnet55_push/puzzle_32pi/p48_meta_analysis.out`) to MIGHTEE CFG309 1.3111e-10
  (`campaign_fresh_gravity/CFG309_mightee_width_frame/cfg309_cfg301chain_FRAME_summary.json`).
- κ = ½ itself is not the target. GF1's "n = 2.000 ± 0.017" is circular (it uses the footing a₀) and is **not** used.

## Candidates (fixed list; nothing outside it may be promoted after the run)

**C1 — saturated dual polarization (identification).** Cold energy's polarization P^μ (CFG694/695 normalization, u = 4πG|P|)
is the Hodge dual of the three-form, so the four-form flux is its 4-divergence q = ∇_μP^μ. That divergence is a bound-charge
(mass) density, and dark energy is identified with it: ρ_Λ = q. In FRW, q = (Ṗ⁰ + 3HP⁰)/c, with the attractor P⁰ = cq/(3H).
The cosmic state sits at the saturation 4πG P⁰ = a₀. No coupling is left free: the saturation scale is a₀ itself (CFG695), and the
bound-charge coefficient is 1 (CFG694). Prediction form: κ_Λ(z) = (4π/3)√(Gρ_Λ)/H(z).
- **C1 gate (premise):** the cosmic state must have FINITE W. CFG695's W(u) = −(a₀/4πG)[u + a₀ ln(1 − u/a₀)] → +∞ as u → a₀,
  and u = a₀g/(a₀+g) reaches a₀ only as g → ∞. If the time component obeys the same W, C1 is INCONSISTENT. The script reports
  W at the C1 state for both covariant readings: (i) |P^μP_μ|, (ii) P⁰ separately.

**C1b — patch bootstrap (identification).** The same medium responds to the de Sitter field g = H²r with CFG695's u(g). The
bound charge it induces inside the dark-energy radius R_Λ = c/H_Λ is required to equal the patch's vacuum mass (4π/3)ρ_Λ R_Λ³.
R_Λ depends on ρ_DE alone, so the condition stays local in ρ_DE.

**C2 — flux lattice (quantization).** Brown–Teitelboim/Bousso–Polchinski: q = N e, so ρ_Λ = N² ρ₁ with ρ₁ the one-quantum density.
a₀ is tied to one quantum, a₀ = κ₁ c√(Gρ₁), which gives κ = κ₁/N. GF1's integer n is read as the flux number N. To count as
FORCED, κ₁ must be fixed by a stated principle. κ₁ = 1 by "naturalness" is a choice and makes C2 a MENU.

**C3 — Kaloper–Sorbo monodromy (quantization).** L ⊃ μθF₄/24, with the axion period θ ≅ θ + 2πf. Gauge invariance under membrane
nucleation quantizes μf against e. Write κ in (e, μ, f, ħ) and find whether the quantization removes Z/β² ħ-free. Pure 4D
has no magnetic dual of a membrane (the dual of a 3-form potential is a (−1)-form), so no Dirac pairing exists without the axion.

**Cited, not re-run (record already decides):** Blanchet–Seraille non-Abelian graviphoton (arXiv:2502.14686; the record's
reading in `opus_48_extended_research/reviews/BRIDGE_COMPUTATIONAL_DOORS_2026-06-19.md`: coefficient IC-dependent ⇒ FREE);
instanton/Gauss–Bonnet couplings (p19 and the README census ⇒ done).

## Tests per candidate

- **T1 κ:** symbolic κ_Λ and κ_crit (sympy), numeric at the GF1 registers, today and in the pure-dS limit.
- **T2 free couplings:** the number f of continuous couplings left in κ after the construction's own rules. FORCED needs f = 0.
- **T3 ħ power:** κ ∝ ħ^p. FORCED needs p = 0.
- **T4 general d:** the construction is written in d spacetime dimensions (top form in place of F₄; Friedmann
  H² = 16πGρ/((d−1)(d−2))) before d = 4 is set. The d = 4 value must not be imposed by hand (screen test 2).
- **T5 a₀(z):** the candidate's own a₀(z). It is classed TRACKING (a₀ ∝ √ρ_DE: the framework law, flat for w = −1), RIVAL
  (∝ H(z)) or OTHER (e.g. ∝ 1/H(z)). Only TRACKING can be IN. OTHER is reported with a₀(2.5)/a₀(0) on the GF1 registers
  (flat ΛCDM).
- **T6 local sector:** state whether the candidate needs unstiffened QUMOND/BIMOND (p58: Cassini rejects κ = ½ there at +6.3σ)
  or embeds in the stiffened action (CFG770–779). If it inherits k04's feedback, the k04 F6 correction applies: an unstable
  band at 2.39 < g_N/a₀ < 155. That must be shown removed, or the candidate is INCONSISTENT.
- **T7 extra prediction:** at least one observable besides a₀ (screen test 3), stated, not tested.

## Classification (per candidate) and lane verdict

- **FORCED-IN:** f = 0, p = 0, premise gate passes, T5 = TRACKING, T6 compatible, both footings inside PRIMARY.
- **FORCED-OUT:** f = 0, p = 0, gate passes, but outside PRIMARY on either footing (or T5 ≠ TRACKING).
- **MENU:** κ fixed only up to a discrete choice (an integer or a "natural" O(1) constant). Report how many elements land in
  PRIMARY and the null P(≥1 hit) for κ₁ log-uniform on [0.1, 10] with N = 1…10 (declared now).
- **FREE:** f ≥ 1. **ħ-DEPENDENT:** p ≠ 0. **INCONSISTENT:** the premise gate or T6 fails.

Lane verdict:
- **CANDIDATE DERIVATION (conditional on its identification premise):** at least one FORCED-IN. Wording is never "derived" or "closed".
- **NARROWED:** no FORCED-IN, but at least one FORCED-OUT or MENU that turns k04's free ratio into a fixed or discrete number.
- **CLOSED:** every candidate FREE, ħ-DEPENDENT or INCONSISTENT. The a₀-as-field door closes with the named failure.

## Controls and MUTATE

- **K1:** reproduce k04 F2 from its committed output: κ² = 2β²/(Z + 2bβ²), Z/β² = 7.964 at K_B = 0, and b from I = 0.4525.
- **K2:** reproduce CFG695's W(u) and its divergence at u → a₀ (sympy limit).
- **M1:** saturation at 2a₀ in C1. κ_C1 must double (the construction responds).
- **M2:** PRIMARY window scaled ×2. C1's class must change.
- **M3:** insert ħ into C3's κ. T3 must report p ≠ 0.

## Pre-freeze disclosure (hand algebra, in chat, before this file)

- **C1:** κ_Λ = (4π/3)√(Gρ_Λ)/H gives √(2π/3) = 1.447 in pure dS and ≈ 1.20 today (×√Ω_Λ), with a₀ ∝ 1/H(z) (OTHER).
  The premise gate is expected to fail (W diverges at saturation).
- **C1b:** the bound mass inside R_Λ is R_Λ² u(R_Λ)/G. Equality with the vacuum mass gives Z/(1+Z)·a₀ = cH_Λ/2 ⇒ Z = 1,
  κ_Λ = √(8π/3) = 2.89.
- **C2:** κ = κ₁/N. With κ₁ = 1 only N = 2 lands in PRIMARY, but the null hit rate is expected to be high.

These expectations are disclosed so that the scripted results cannot be presented as surprises. The scripts decide, and
a script result that disagrees with a hand value replaces it, with the disagreement recorded.

## Honesty rules

- No knob scans. The C1 covariant readings (i)/(ii) are the only variants, and the C2 null ranges are fixed above.
- Identity-class results (anything true by construction) are flagged as such and never scored as evidence.
- κ = ½ stays FITTED in all writing unless the verdict is CANDIDATE DERIVATION, and even then it is conditional.

## Files to be produced (after the 1024³ job)

`p63_a0_field_coupling.py` (+ `.out`, `_results.json`), `p63_a0_field_coupling_MUTATE.out`, `README.md` with the verdict.

## Erratum (appended 2026-10-19, while writing the script, before any run)

- **M1 direction.** With the saturation at 2a₀ and the cosmic state still at saturation, κ_C1 **halves**; it does not double.
  The test is the factor-2 response: check T4-C1 (κ_dS = √(2π/3)) must FAIL under MUTATE.
- **M2 target.** C1's class is set by its premise gate whatever the window, so M2 is applied to C1's **window verdict**
  (check W1) instead of its class.
- **M1 and M2 in one run.** W1 always uses the σ = 1 construction, so M1's halving cannot cancel M2's ×2 window.
- **MUTATE run, declared:** T4-C1 (M1), W1 (M2), C2's "only N = 2" (M2) and H1 (M3) must FAIL. K1, K2 and T4-C1b must PASS.

## Erratum 2 (appended 2026-10-19, after a read-only provenance audit, before any run): the window source was superseded

- **What was wrong.** The PRIMARY window used κ_Λ = 0.551 ± 0.043 from THE_HORIZON_FORM_OF_THE_BTFR.md §6.1. That value is
  superseded twice in the committed record. It mixed H₀ conventions: SPARC's Hubble-flow distances are at H₀ = 73 while ρ_Λ is
  at 67.4. And its ±0.043 held the bulge M/L fixed. MNRAS v3.1 (`qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/
  paper_numbers.out`, tracked) gives the same estimator as κ_B = 0.58 ± 0.18 on the consistent (R1) convention.
- **Replacement PRIMARY window.** CFG493's GLS combination of the M/L-insensitive routes, with shared systematics included
  (`campaign_fresh_gravity/CFG493_kappa_combined/cfg493_kappa_combined.out`, tracked): κ_Λ = 0.4172 ± 0.0946 and
  κ_crit = 0.3452 ± 0.0783. That is 2σ ⇒ κ_Λ ∈ [0.228, 0.606], κ_crit ∈ [0.189, 0.502]. It is the record's own designated
  combined value, and its verdict there is CONSISTENT BUT NOT DISCRIMINATING.
- **SECONDARY (reported).** MNRAS v3.1 R1 estimators: A 0.450 ± 0.073, B 0.58 ± 0.18, C 0.43 ± 0.08.
- **Consequences, declared before the run:**
  - C1 (1.20) and C1b (2.89) stay far outside.
  - C2 with κ₁ = 1 now lands at N = 2, 3 **and** 4. The pre-freeze line "only N = 2 lands" no longer holds. The C2 check is
    re-declared as `hits == [2, 3, 4]`; under M2 the hits become [1, 2] and the check must FAIL.
  - The C2 null rises to about 0.71.
  - Nothing else in the classification rules changes.

## Amendment 3 (appended 2026-10-20, before any run): run condition only

- **What changes.** The frozen text says the runs "start only when no 1024³ job is live". The owner instructed a parallel
  session to swing every remaining κ lane ("keep swinging all of them"). Since this criteria file was written, the record's
  own rule for lanes beside a live 1024³ job is CFG894 `KAPPA_CAMPAIGN_RULES.md` §11 (2026-10-20): light single-core scripts
  only (`nice -n 10`, `OMP_NUM_THREADS=1`, under ~1 GB, seconds). p63 is sympy and arithmetic of that size. It is run under
  §11 beside the live NC2x (CFG654, chain7b).
- **What does not change.** No candidate, check, window, classification rule, MUTATE or verdict rule is altered. The script
  (`p63_a0_field_coupling.py`, written 2026-10-19 by the session that froze this lane) is run unmodified.
- **Who ran it.** A parallel session (why_4_puzzle lanes), on the owner's instruction; recorded so the provenance is clear.
