# The bath-coupling family vs the spec sheet: a see-saw no-go, and the one coupling that survives

*C. Zimmerman, 2026-06-10. Trilemma calc #1b (`mi_coupling_family_scan.py` + `.out`, sympy+numeric verified; follows
`MI_BATH_TAIL_CONSTRAINT.md`). Question: within the bath-response→inertia family (the only live mechanism class for the
trilemma's missing object), does ANY coupling pass the pre-registered spec sheet — (i) deep-MOND limit, (ii)
ephemeris-safe tail (|δa(Saturn)| < 10⁻¹⁴, Folkner), (iii) a defensible a₀? Answer: the difference-family has a
**mutual-exclusion no-go**; exactly one coupling inside the family escapes. Both ways throughout. C1/C2 only.*

## The family (one physics input: thermal UDW response at the Deser-Levin temperature T_eff = T_dS√(1+x²), x = a/cH)
| Coupling | μ(x) | deep slope μ/x | tail x·(1−μ) | Saturn δa | verdict |
|---|---|---|---|---|---|
| **F1** gapless difference *(= Milgrom 1999, verbatim — see priority note)* | [√(1+x²)−1]/x | 0.5 ✓ | 1 | 5.4×10⁻¹⁰ | **DEAD ×54,000** |
| **F2** gapped difference, gapped-flat normalizer (gap ε) | [n(ε/√(1+x²))−n(ε)]/n(ε/x) | **∞ (deep MOND destroyed)** at every ε | ε·n(ε) → safe for ε ≥ 13.5 | 7.8×10⁻¹⁵ at ε=13.5 | **NO-GO (see-saw)** |
| **F3** gapped difference, gapless-flat normalizer | ε[n(ε/√(1+x²))−n(ε)]/x | collapses with ε (0.46→10⁻⁴) | **grows** with ε (1.1→6.8) | up to 3.7×10⁻⁹ | **DEAD both ends** |
| **F4** susceptibility, m_eff ∝ dT_eff/da | **x/√(1+x²) = μ_standard** (parameter-free, self-normalizing) | 1 ✓ | 1/(2x) → 0 ✓ | **2.3×10⁻¹⁵ SAFE (4× margin)** | **PASSES** |

**The no-go (the derivation-grade piece):** in the difference-family, the deep-MOND limit and an ephemeris-safe tail are
**mutually exclusive**. The gap that exponentially suppresses the tail (ε ≳ 13.5) freezes the gapped flat-space normalizer
(∝ e^{−ε/x}) and sends μ → ∞ in deep MOND (anti-MOND); restoring the deep limit with a gapless normalizer (F3) re-fattens
the tail *worse than gapless*. Verified numerically across ε ∈ {1, 5, 13.5, 20}; the see-saw has no crossing point.

**The escape (the construction-grade piece):** differentiating instead of subtracting — inertia as the *susceptibility*
of the detector's thermal state to acceleration, m_eff ∝ dT_eff/da — yields **exactly the standard MOND interpolation
function**, with no free parameter (the flat-space limit self-normalizes), a quadratic tail that passes Saturn with 4×
margin, and the deep limit intact. The spec sheet *selected* it; it was not assumed.

## The a₀ row (the coefficient gap, restated honestly — it does not go away)
| | implied a₀ | vs SPARC-fitting framework value |
|---|---|---|
| F1 (Milgrom-99) | 2cH_Λ = 1.08×10⁻⁹ | **11.6× (= 2Z) high** |
| F4 (susceptibility) | cH_Λ = 5.42×10⁻¹⁰ | **5.79× (= Z) high** |
| framework / SPARC | 9.36×10⁻¹¹ | — |
F4 halves the log-gap but the coefficient is still off by exactly Z — fully consistent with the banked verdict (Z is
data-selected, not derived; the doors found no mechanism forcing it). **No coefficient claim is made.** What changed is
ONLY this: the solar-system tail kill, which was fatal to the family's natural member, does not extend to F4.

## Priority & attribution (checked before claiming anything)
- **F1 IS Milgrom 1999** (astro-ph/9805346, Phys. Lett. A 253, 273): his μ(x) = √(1+(2x)⁻²) − (2x)⁻¹ with
  a₀ = 2c√(Λ/3) is algebraically identical to F1 under x → a/a₀ (verified by substitution). **So the ×54,000 ephemeris
  exclusion applies to a published proposal** — with the historical note that in 1999 a ~cH constant anomaly was
  arguably *supported* (the Pioneer anomaly, ≈8.7×10⁻¹⁰ ≈ cH₀, was then thought possibly real); the Folkner/INPOP
  planetary bounds that kill it came later. To our knowledge the planetary-ephemeris exclusion has not been applied to
  this specific proposal in this repo before; broader-literature duplication not excluded. [flag]
- **F4 does not appear in Milgrom-99** (it proposes the difference form only). Whether "μ_standard = (2πck_B/ħ)·dT_DL/da,
  exactly" is noted elsewhere in the literature is **unverified** — treated as possibly-known until checked. [flag]

## Honest scope (locked)
- This is **construction within one mechanism family**, not a derivation of MOND: the family itself rests on the
  unproven Step-4 link (bath response → inertia), F4 is *selected* by kill-tests, the coefficient stays Z-off, and the
  covariance obstruction (trilemma calc #3) is untouched — F4 is a worldline statement, not a field theory.
- Next bounded steps, in order of bite: (a) SPARC/RAR re-fit with μ_standard at a₀ = 9.36×10⁻¹¹ vs the McGaugh RAR
  function (repo machinery exists; does F4's *shape* survive galaxy data as well as its tail survives Saturn?);
  (b) wide-binary/EFE phenomenology of F4 (modified-inertia EFE differs from modified-gravity EFE);
  (c) the covariance question for susceptibility couplings specifically.
- Liability ledger rides along unchanged (type-blind: the lensing split; clusters; a₀(z) at z≈3).
