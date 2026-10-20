# W4-05: theories that fix their own vacuum: can any of them fix the 4? (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-05 script exists.** Append-only after this commit. Rules followed:
`campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CAMPAIGN_RULES.md`. **κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ±
0.095, κ_crit = 0.345 ± 0.078, never pooled). Not theory closed.

## Question and why this class

The zero-mode wall says a local action can shift its vacuum constant freely, so most routes end as a TRADE (W4-01, W4-02,
W4-03, CFG911). The only escape on record is a theory whose action **fixes its own vacuum** in terms of its own scale ℓ, with
no free cosmological constant. If such a theory also supplies a natural acceleration c²/ℓ for the a₀ sector, ε_DE and a₀ are
tied with no free coupling.

The structural hypothesis, frozen here and tested on each family, is the **self-determined-vacuum dichotomy**:
- if Λ_eff = A_Λ/ℓ² and a = A_a c²/ℓ with A_Λ and A_a algebraic numbers fixed by the action, then
  κ² = a²/(c²Gρ_DE) = 8π A_a²/A_Λ;
- that is π times an algebraic number, which is transcendental (Lindemann), so never ¼;
- its size is set by √(8π) ≈ 5 unless A_a²/A_Λ is small.

This applies W4-02's coefficient-domain theorem (rational functions of π with algebraic coefficients) to a concrete class. It
does not replace it. The census adds seven families with no CFG894 register row, checked 2026-10-20: Born–Infeld/EiBI 0,
Palatini 0, Brans–Dicke 0, Maggiore 0, Deser–Woodard 0, running vacuum 0, TeVeS 0. Overlap check: W4-04 (parallel session;
microscopic SUSY / D3-brane DBI / heat-kernel induction / amplitude ratio) is not repeated here. The EiBI row below concerns
the gravitational action √|g + κ_E R(Γ)|, not a brane DBI.

## Families, starting equations (from memory, PROVISIONAL; nothing downloaded) and declared readings

Units c = 1 in the script; ρ_DE ≡ Λ_eff/(8πG); κ² = a²/(Gρ_DE).

| family | own vacuum relation | reading for a | hand expectation (disclosed) |
|---|---|---|---|
| **V1 EiBI gravity** (Bañados–Ferreira): S = (1/8πG)(1/κ_E)∫[√|g + κ_E R(Γ)| − λ√|g|] | Λ_eff = (λ − 1)/κ_E. V1a: no separate cosmological term (λ = 0), so Λ_eff = −1/κ_E, which is de Sitter for κ_E < 0. V1b: λ free. | a = 1/√|κ_E| (the Born–Infeld curvature scale) | V1a κ² = 8π, κ 5.013, MISS, π-odd. V1b TRADE. |
| **V2 f(R) = R − μ⁴/R** (metric, Carroll et al.; Palatini, Vollick) | Vacuum trace equation R f′ − 2f = 0 gives R = √3 μ², and de Sitter R = 4Λ gives Λ_eff = √3μ²/4 (same static root in both formalisms) | a = μ | κ² = 32π/√3, κ 7.62, MISS, π-odd (π × algebraic) |
| **V3 Brans–Dicke / scalar–tensor** | G_eff = 1/φ; Λ or V(φ) is free | none intrinsic | TRADE |
| **V4 Maggiore RR nonlocal** (−(m²/12)M_P² R□⁻²R) | ρ_DE follows from m through the whole expansion history, with zero initial conditions for the auxiliary fields | a = m | The m ↔ ρ_DE relation needs the measured matter history (a forbidden upstream input), and ρ_DE,RR(z) drifts while m is constant, so it is not tracking. Classed CONDITION/TRADE; no κ number is computed. |
| **V5 Deser–Woodard nonlocal MOND** | f(□⁻¹R) built to reproduce MOND; a₀ is an explicit parameter; Λ free | a₀ (input) | TRADE |
| **V6 running vacuum** (Shapiro–Solà): ρ_Λ(H) = ρ₀ + 3νH²/(8πG) | ρ₀ and ν free | none intrinsic (cH would be H-type) | TRADE |
| **V7 TeVeS** (Bekenstein 2004) | a₀ = √(3k) c²/(4πℓ) from the scalar's k and ℓ; Λ free | a₀ from (k, ℓ) | TRADE: ℓ, k and Λ are independent. Context, recalled: the original TeVeS tensor speed is excluded by GW170817. |

Self-determined-vacuum members: V1a and V2 (and V4, by history). The W4-01 self-accelerating members are re-tabulated for
the dichotomy count, not recomputed as new attempts: DGP crossover κ² = 8π/3, f(T) κ² = 16π(2n−1)^{1/(n−1)}, dRGT κ² = 8π/X.

## Inputs, footing, π / ħ

- Inputs: symbols only, plus the pure numbers of each action (√3, 4, 8π). No a₀ value, κ, Z or Ω_Λ upstream.
- Footing: ρ_DE (declared); ρ_crit only as report.
- π: every self-determined value is 8π × algebraic. Declared class `odd` (as "π × algebraic"; W4-02's grammar).
- ħ: none enters.

## Checks (printed in the .out)

- **I1:** the compute block contains no forbidden constant.
- **I2:** κ² is symbolic; free symbols are printed, and a free continuous symbol makes the reading a TRADE.
- **I3:** κ² is dimensionless.
- **I4:** no reading uses the law's κ.
- **I8:** κ²/π is algebraic (sympy `is_algebraic`) for each self-determined reading, and κ² ≠ ¼.
- **K1:** EiBI vacuum: the field equations of the √|g + κ_E R| action in vacuum give Λ_eff = (λ − 1)/κ_E. Checked here as the
  standard result's consistency: λ = 1 gives Λ = 0, and small-κ_E expansion recovers Einstein + Λ.
- **K2:** f(R): solve R f′ − 2f = 0 for f = R − μ⁴/R (R = √3μ²), and confirm f = R − 2Λ₀ gives R = 4Λ₀ (control).
- **K3:** each hand value equals the script's symbolic value.
- **K4 (the dichotomy count):** across the self-determined readings of W4-01 and W4-05, count κ² = 8π × algebraic. The frozen
  prediction is all of them, and none equal to ¼.

## Outcome classes and lane verdict (CFG894 §7)

Per reading: EXACT CANDIDATE / CONSISTENT / MISS / MENU / TRADE / CONDITION / VOID.

Lane verdict (frozen):
- **DICHOTOMY HOLDS:** every self-determined reading gives κ² = 8π × algebraic (none ¼), and every other family is a TRADE or
  CONDITION.
- **DICHOTOMY BROKEN:** a self-determined reading is not π × algebraic, or a family fixes κ without its own vacuum. Report it;
  an EXACT CANDIDATE then needs an audit lane and §8.

Hand expectation: **DICHOTOMY HOLDS**, with self-determined values κ = 5.01 (EiBI) and 7.62 (f(R)), both far above the window.
Adding W4-01's DGP gives κ ~ 3–8. The natural size of a self-determined κ is O(√8π), about ten times the measured 0.42.

## Mutation control (`W4_05_MUTATE=1`, separate `_MUTATE` outputs, exit 1 when it bites)

- **M1:** Einstein coupling 8πG → 4πG in ρ_DE = Λ/(8πG). Self-determined κ² halve (EiBI 8π → 4π; f(R) 32π/√3 → 16π/√3).
  K3 must FAIL.
- **M2:** f(R) exponent μ⁴/R → μ⁶/R². The vacuum root moves (R f′ − 2f = 0 gives R³ = 4μ⁶), so κ² changes. K3 must FAIL for V2.
- **M3:** EiBI with λ = ½ instead of 0. Λ_eff = −1/(2κ_E), so κ² doubles. K3 must FAIL for V1a.
- I1, I3 and K1/K2's controls must still pass.

## Second predictions (stated, not scored)

- V1a: EiBI's Born–Infeld scale also sets its compact-star structure (the EiBI parameter is bounded by neutron stars).
- V2: 1/R gravity's own instabilities (metric: Dolgov–Kawasaki; Palatini: atomic-scale issues), recalled, provisional.
- The dichotomy itself predicts that any future self-determined route lands at κ ~ √(8π A) with A = O(1).

## Files

`w4_05.py`, `w4_05.out`, `w4_05_results.json`, `w4_05_MUTATE.out`, `w4_05_results_MUTATE.json`, `README.md`. One register row
per family (V1–V7), then `kappa_campaign_lee.py` rerun.
