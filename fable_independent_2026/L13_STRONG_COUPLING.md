# L13 — P7: the khronometric survivor's open wound, computed

2026-09-08. Lane L13 of [CHARTER.md](CHARTER.md).
Script: [L13_strong_coupling.py](L13_strong_coupling.py) → [L13_strong_coupling.out](L13_strong_coupling.out).
22 PASS, 4 FAIL. All **13 controls PASS**; every FAIL is a substantive finding, none a machinery failure.

Target: `THE_ACTION_2026-09-05.md` §1–3, against `CRISPY_FRIED_CHICKEN_RECIPE.md`'s **P7** ("if α→0
simultaneously sends the scalar kinetic normalization →0, treat as STRONGLY COUPLED unless an independent
finite normalization is shown") and **A3** ("MANDATORY DESIGN PRINCIPLE: PPN-visible coupling ≠ kinetic
normalization").

## Verdict in one line

**P7 does not fire. A3's mandatory design principle is violated anyway, and A3's healthy pattern
α_PF ∝ e^(−y) is refuted.** The theory is safe by a number (c₁₄ = 10⁻⁵ is 10⁸⁶ times larger than the value
that would hurt), not by the design separation A3 requires.

## The two objects, computed

**(a) PPN-visible preferred-frame couplings.** With `c₁ = −c₃ = K_B`, `c₄ = c₁₄ − K_B`, the Foster–Jacobson
Einstein-aether formulas give, symbolically and exactly:

    alpha_1 = -4 c_14                                        exact, for every K_B and c_2
    alpha_2 = c_14 (c_2 - c_14 - 2 c_14 c_2) / [c_2 (c_14 - 2)]
            = -c_14/2 + c_14^2/(2 c_2) + 3 c_14^2/4 + O(c_14^3)

reproducing g03v's closed form together with the O(c₁₄²) remainder it drops, and vanishing **exactly** on
`c_2* = c_14/(1 − 2 c_14)`. **Neither α contains the screening variable at all.**

**(b) Kinetic normalisation.** Three independent routes agree.

- *Flat decoupling limit.* At `c₁₃ = 0` the whole clock sector collapses to `M²[c₁₄ a·a − c₂ (∇·n)²]`
  (the identity `(∇n)² − (∇n)(∇n)ᵀ = −a²` for hypersurface-orthogonal `n`, verified exactly), giving
  `L₂ = M²[c₁₄ (∂ᵢχ̇)² − c₂(∇²χ)²]`.
- *Full unitary-gauge reduction* with lapse and shift integrated out reproduces Einstein-aether's published
  spin-0 speed `c_s² = c₂(2−c₁₄)/[c₁₄(2+3c₂)]`, and at `c₁₄ = 0` the lapse becomes a Lagrange multiplier:
  **the khronon exists only because c₁₄ ≠ 0.**
- *Coupled (χ, δφ) system* including the AeST mixing `2(2−K_B)J^μ∂_μφ`. The mixing carries one time
  derivative, so it is antisymmetric and drops out of the kinetic Hessian entirely:

      H_kin = diag( 2 M^2 c_14 k^2 ,  2 M^2 |K_2| )     at EVERY value of the screening variable.

## The answer

**Same coefficient?** Yes, exactly. `−α₁/4` divided by the khronon's kinetic coefficient is identically 1,
for every `K_B, c₂, c₁₄`. **A3 violated as an identity, not as an approximation.** For the MOND scalar A3 *is*
satisfied: its normalisation `|K₂|` appears in no PPN α and does not depend on `J_Y`.

**Screened?** No. `α₁, α₂` are constants. The screening reaches the frame sector only through the sub-leading
drag, and it falls as a **power law 1/y**, not `e^(−y)`. Integrating out the stiff scalar in the screened
regime gives the exact effective normalisation

    c_14_eff(Sigma) = c_14 + (2-K_B)/Sigma + c_2 |K_2| / [(2-K_B) Sigma],     Sigma = J_Y = s/Delta(s)

— a **positive** correction that screening *removes*: `c₁₄_eff/c₁₄` = 1.190 at Saturn, 1.0018 at 1 AU,
1.0000001 at Cassini conjunction. The normalisation is never multiplied by a vanishing factor.

**Λ_sc.** Every cubic monomial of the khronon carries the derivative multiset {1,2,2}, so `L₃` is a single
dimension-5 operator with `Λ_sc = 2 M_pl √c₁₄`. On the α₂ = 0 line PPN forces (`c₂ ≈ c₁₄`), the khronon is
exactly luminal, so no sound-speed factor enters:

| background | c₁₄_eff | Λ_sc [GeV] | 1/Λ_sc [m] | AU / (1/Λ_sc) |
|---|---|---|---|---|
| Saturn orbit | 1.190e−5 | 1.68e16 | 1.17e−32 | 1.27e43 |
| Earth orbit | 1.002e−5 | 1.54e16 | 1.28e−32 | 1.17e43 |
| Cassini conjunction (b = 1.6 R☉) | 1.000e−5 | 1.54e16 | 1.28e−32 | 1.17e43 |

43 orders of magnitude shorter than 1 AU. The classical criterion is normalisation-free and even cleaner:
`L₃/L₂ = −2χ̇` for the dominant monomial, and `|χ̇| ≲ 10⁻⁶` in the Solar System.

For P7 to be fatal the theory would need `c₁₄ < 7.3e−92`, i.e. 10⁸⁶ below its working value.

## Why the wound was real, and how it was healed

The control that matters: the **same machinery kills the historical candidate P7 was written about.** With
`η = c₁₄ = 2e^(−y)` (`KHRONOMETRIC_MOND_GAUNTLET`, recipe §9), `α₁ = −4η = −8e^(−y)` — the recipe's own
quoted value — and at Earth's orbit `y = 6.3e7`, so `log₁₀(1/Λ_sc / m) = 1.4e7`. P7 fired by ten million
decades. The test is not blind.

**The current action escapes P7 by abandoning A3's mechanism.** It does not screen α_PF; it makes the
coefficient a constant and tunes it: `c₁₄ ≈ 10⁻⁵` (α₁ = −4e−5 against the 10⁻⁴ bound) and `c₂` within 8% of
`c₂*` for α₂. The P7 direction still exists in parameter space — `c₁₄ → 0` sends α₁ and the kinetic
normalisation to zero together, ratio fixed at −4 — it is simply enormously far from where the theory sits.

## Two costs the screening does impose (reported, not promoted to kills)

1. **The MOND scalar's cone.** Its normalisation `|K₂|` is constant but its gradient stiffness `J_Y = s/Δ(s)`
   is fixed by the static law and Δ is bounded by the bounded-boost theorem, so
   `c_s,⊥² = (2−K_B) J_Y c²/|K₂| ≥ (2−K_B) s c²/(C |K₂|)` is **forced**: at |K₂| = 5e5, `c_s/c` = 19 at 1 AU
   (17 on the alt footing) and 2522 at Cassini conjunction (2298 alt). Subluminality at 1 AU would need
   |K₂| ≥ 1.76e8 — 352× above the dark sector's window edge and 65× above the growth pincer's 2.7e6.
   In a khronometric theory with a preferred foliation this is **not by itself acausal**; it is a quantified
   cost of the screening, and it would be a third arm of the |K₂| pincer only if subluminality were required.
2. **What the action as published does not determine.** On the carried kernel's saturated branch
   (`s > 2.540`) `Δ' = 0` identically, so the longitudinal stiffness `Σ_∥ = 1/Δ'` is infinite and `J(Y)` has
   an infinite slope at `Y = (C a₀)²`. The published kernel is therefore not C² at the Solar-System
   background, and **the MOND scalar's own cubic action there cannot be written down from the action as
   written.** Missing input: a C² continuation of Δ(s) past its maximum with Δ' > 0.

## Controls (all PASS)

| control | reproduces |
|---|---|
| K0 | the carried kernel's `s_sat = 2.540`, `C = 0.6476` (THE_ACTION §3) |
| C1 | the hypersurface-orthogonal identity `A − C = −a²`, exact at rational points |
| C2a/b/c | the exact quadratic and cubic expansions of `a·a` and `(∇·n)²`; the {1,2,2} derivative pattern |
| C3 | Einstein-aether's **published** spin-0 speed, from an independent unitary-gauge reduction |
| C3b | GR control: at `c₁₄ = 0` the lapse is a Lagrange multiplier, no propagating scalar |
| C4a/b | THE_ACTION §5.7's fast-clock speed `(2−K_B)²/(c₁₄|K₂|)` and its threshold `c₂ = 1.3e−5` |
| C4c | **f34's two full-metric mode speeds** (4.1899e−2, 4.1096e+4) to 1.3% and 3.2% |
| C4d | `c₁₄_eff` as an exact rational identity, not a truncated series |
| C5a/b/b2/c | α₁ = −4c₁₄ exactly; g03v's α₂ closed form and its `c₂*` root; f33's PPN corner |
| C5d | the recipe's own `α₁ = −8e^(−y)` for the historical candidate |
| C5e | the khronon is exactly luminal on the PPN-forced `c₂ = c₂*` line |
| C6 | the same Λ_sc machinery detects P7 firing catastrophically for `η = 2e^(−y)` |

## Scope — not done here

The ξ² coherence operator is omitted from the frame-sector drag (it screens further, so the reported drag is
an upper bound); the metric-mediated khronon interactions are not computed (they are `1/M_pl`-suppressed
without the `1/c₁₄` enhancement, so the decoupling limit gives the *lowest* Λ_sc); the O(1) coefficient of
Λ_sc is a power-counting estimate, and only its parametric dependence `2 M_pl √c₁₄` is load-bearing. The
classical figure `|χ̇| ≲ 10⁻⁶` is an order-of-magnitude estimate from the w/c = 1.2e−3 CMB-frame tilt, not a
solved Solar-System khronon profile; no PASS/FAIL rests on it. The `Σ = J_Y` used in the drag is the
transverse (conservative) stiffness — with the longitudinal `Σ_∥ = 1/Δ'` the drag is exactly zero on the
saturated branch, which only strengthens the conclusion that the screening leaves `c₁₄` alone.
