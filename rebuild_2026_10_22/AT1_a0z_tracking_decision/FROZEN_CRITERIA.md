# AT1_a0z_tracking_decision: FROZEN CRITERIA (2026-11-03)

Committed alone, before any script, Lean file or number of this lane exists. κ = ½ is FITTED. Not theory closed.

## 0. Question and what is reused

Does a₀ track ρ_DE (the law: a₀(z)/a₀(0) = √X(z)) or the expansion rate (rival: a₀ ∝ H(z), ratio E(z) = H/H₀)?

This lane writes a **sample-level decision rule** for a future high-z kinematic sample and **certifies its arithmetic in
Lean**. It does not grade any data and it does not search for a new sample.
- The thresholds are reused, not reinvented: CFG689 primary mode (curvature free, BAO + Pantheon+), frozen at 1c237145d /
  0db6da294 / bb21587be, results 6c064b83a3. Inputs are the posterior quantiles in
  `campaign_fresh_gravity/CFG689_native_ruler_bao/cfg689.json` → `BAO+SN.P1` (sqrtX_q, E_q at 2.5/16/50/84/97.5 %), z* ∈
  {1.0, 1.2, 1.5, 2.33}.
- The separation statistic is CFG689 §6 / CFG683: gap = log10 E₁₆ − log10 √X₈₄; σ_E = log10 E₅₀ − log10 E₁₆;
  σ_X = log10 √X₈₄ − log10 √X₅₀; S(e) = gap / √(e² + σ_E² + σ_X²); e_3σ = largest e with S ≥ 3.
- The sample search is CFG685 (`campaign_fresh_gravity/CFG685_deciding_sample_hunt/`): no public sample reaches e_3σ (best
  0.4–0.5 dex). Its proposal target (z 1.0–1.6 discs, CO kinematics v/σ ≥ 6, three gas tracers, resolved JWST M/L, N ≈
  25–50) is quoted, not re-derived.
- The single-disc rule stays CFG806 / CFG809 §4 (owner 10-20 governing plans). One disc excludes no model; AT1 does not apply
  to one disc.

## 1. The measured quantity (footing-free)

Per redshift bin z*: ȳ = log10(a₀(z*) / a₀,ref), where a₀,ref is measured **with the same estimator** (same kernel, same
gas and stellar recipes) on a comparison sample at z < 0.1. κ, the footing value and ρ_DE's absolute level cancel in the
ratio, so the rule is the same on both footings and needs no H₀. Using a footing value (9.36e-11, 1.13e-10) as a₀,ref voids a
grade.

Error: e = √(e_stat² + c²).
- e_stat: the sample's statistical error on ȳ (inverse-variance mean of per-galaxy log a₀, including the reference sample's).
- c: the sample's **declared common mode** that does not cancel between the z* and z < 0.1 samples (IMF evolution, gas
  conversion α_CO / [CII] / dust, pressure-support recipe). It is declared in the sample's own criteria before its ȳ is seen.
  CFG685 puts IMF + gas conversion alone at 0.05–0.10 dex.

## 2. Gates (all before ȳ is looked at)

- **G1 power:** e ≤ e_3σ(z*) from CFG689 primary. Otherwise NOT POWERED, no verdict.
- **G2 gas:** every galaxy has at least one direct cold-gas tracer (CO, [CI], [CII] or dust). Scaling-relation gas → not
  graded (CFG685).
- **G3 pressure support:** the asymmetric-drift / pressure correction is declared before data, and its sample-median size at
  the radius used is ≤ 0.05 dex, or the sample's median v/σ ≥ 6.
- **G4 regime:** the radius used reaches g_bar ≤ 0.5 a₀,ref for each galaxy.

## 3. Distances and outcomes (primary mode only; flat + θ* mode reported beside, no verdict weight)

Let T = log10 √X₅₀, R = log10 E₅₀, with the side-facing widths: tX = log10 √X₈₄ − T if ȳ > T, else T − log10 √X₁₆;
tE = R − log10 E₁₆ if ȳ < R, else log10 E₈₄ − R.
- d_T = (ȳ − T) / √(e² + tX²) (signed; positive means above tracking)
- d_R = (R − ȳ) / √(e² + tE²) (signed; positive means below the rival)

Outcomes, exclusive, checked in this order:
1. **TRACKING FAVOURED:** |d_T| ≤ 2 and d_R ≥ 3.
2. **RIVAL FAVOURED:** |d_R| ≤ 2 and d_T ≥ 3.
3. **NEITHER:** |d_T| > 3 and |d_R| > 3.
4. **INCONCLUSIVE:** anything else.

TRACKING FAVOURED at one z* is support for the law's a₀(z), not a derivation of κ, and not evidence for the framework over
ΛCDM (that is P6 / DM14, a different comparison). RIVAL FAVOURED or NEITHER at a powered z* falsifies the law's a₀(z) at that
redshift on the measured sample.

## 4. Lean certificate (core Lean 4, no Mathlib; integer arithmetic on quantities rounded to 1e-6 dex)

Rounding is conservative for each claim (gap rounded down and widths up where a claim says "at least"; the reverse for "less
than").
- **C1 e_3σ arithmetic:** at each z*, S(e_3σ) ≥ 3 (as gap² ≥ 9(e² + σ_E² + σ_X²)), and S(e_3σ + 0.001) < 3.
- **C2 power gate:** for every c ≥ e_3σ(z*) and every e_stat, G1 fails (general theorem over integers). And the minimum N for
  per-galaxy error s and common mode c, N_min = ⌈s² / (e_3σ² − c²)⌉, at s ∈ {0.14, 0.20, 0.30} dex and c ∈ {0.05, 0.075} dex,
  each certified as the least N that passes.
- **C3 no double consistency:** at every z*, at e = e_3σ, no ȳ has both |d_T| ≤ 2 and |d_R| ≤ 2 (shown as 2(√(e² + σ_X²) +
  √(e² + σ_E²)) ≤ gap, with rational upper bounds on the roots checked by squaring). Smaller e only shrinks both roots.
- **C4 outcome function:** the four outcomes are a total, exclusive function of (d_T, d_R) (decided on the boundary cases).
- Every theorem's `#print axioms` goes into the .out. A `sorry` or a non-core axiom voids the certificate.

## 5. Script checks (python, stdlib only)

- K1 reproduce CFG689's e_3σ from the json quantiles within one grid step (0.001 dex), on the same 1000-point grid.
- K2 the Lean integers are generated from the json by the script, never typed by hand; the script prints them and their
  rounding direction.
- K3 grep the script and the Lean file for footing a₀ values (9.36, 1.13e-10, 1.2e-10) and measured κ; fail on a hit.

## 6. Mutation control (separate `_MUTATE` outputs)

σ_X doubled (the law's own ρ_DE(z) band twice as wide). Expected: e_3σ falls at every z*; at z* 2.33, σ_X ≈ 0.25 > gap / 3 ≈
0.15, so no e passes and the bin becomes NOT DECIDABLE. The script exits non-zero if e_3σ does not fall at all four z*. The
Lean MUTATE file states C1 with the mutated widths and must fail to compile at z* 2.33.

## 7. Second prediction / what this does not do

The rule depends on κ nowhere (the ratio cancels it), so it cannot pin κ. Its value is that a future sample can be graded
against a rule fixed today. Reported outputs: e_3σ table, N_min table, the c ceiling (c < e_3σ) per z*, and the Lean axioms.
