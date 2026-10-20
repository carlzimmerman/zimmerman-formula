# CFG897: κ door D1, the stiffness term's own vacuum on an expanding background. CLOSURE

**Bottom line.** The stiffness term cannot be the dark energy, so this door gives no κ. κ = ½ stays FITTED. Two different
statements need separating:

- **Is the stiffness term the dark energy?** No, and it fails on three separate counts:
  - **Sign:** its energy on the cosmic background is negative.
  - **Equation of state:** it grows like H², so it only rescales G in the Friedmann equation and never acts as a separate Λ.
  - **Size:** it is 10⁻¹⁹–10⁻¹⁵ of the critical density.
- **What κ would the matching give?** As a derivation the route is a TRADE: κ ∝ 1/L*. Even ignoring the sign, the independent
  L* window gives κ ≥ 1×10⁷ (≥ 3×10⁶ with the most favourable O(1) curvature coupling). That is EXCLUDED.

The door expected "κ ~ 10⁶–10⁸ (excluded) or vanishing". Both happen, and the sign makes the result stronger than expected.
Footings are never pooled. No de Sitter–Unruh argument is used. GF2's ½ is the SIS ratio and plays no part. Not "theory closed".

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (4c7a17d27).
- **Script:** `cfg897.py` (sympy minisuperspace; one process, ~3 s, 71 MB).
  - Normal run: `OMP_NUM_THREADS=1 nice -n 10 python3 cfg897.py` → `cfg897.out`, `cfg897_results.json`. 35/35 checks pass,
    exit 0.
  - `CFG897_MUTATE=1` → `cfg897_MUTATE.out`, `cfg897_results_MUTATE.json`. 5/5 teeth bite, exit 1 by design.
- **Inputs:** G, c, ρ_DE, L*, κ, all symbolic. γ = K L*²/2 = 2πG L*² (CFG770: Λ² = γ/K, L*² = 2Λ²). The cosmic norm is
  4πG|P| ≤ a₀ (CFG695 saturation; p63's convention 4πG P⁰ = a₀).
  - Measured values enter only at the end, to turn κ(L*) into numbers: H₀ = 67.4 km/s/Mpc and Ω_Λ = 0.685.
  - The L* window [24 pc, ≳ 1 kpc] (CFG820, CFG691) is used only to test the predicted range.
  - Nothing was downloaded, and no other lane was edited.

## Setup

- **Background.** On flat FRW the only isotropic background a vector can have is timelike: P^μ = (P⁰(t), 0, 0, 0).
- **Metric.** Minisuperspace with x⁰ = ct, ds² = −N²c²dt² + a²dx² in n = d − 1 space dimensions.
- **Energy and pressure.** ε = −a⁻ⁿ δS/δN|_{N=1} and p = (δS/δa)/(n aⁿ⁻¹)|_{N=1}, from full Euler–Lagrange derivatives.
- **What is held fixed.** The proper norm φ = |P| (V1). With a norm constraint (a Lagrange multiplier, as in Einstein-aether)
  this is the on-shell stress tensor, which K5 checks against the other two parametrisations.

## Results: the exact equations (n = 3, d = 4, γ > 0, fixed norm unless stated)

| structure (Lagrangian) | ε | p | class |
|---|---|---|---|
| (a) −(γ/2)∇_μP_ν∇^μP^ν | **−(γ/2c²)(φ̇² + 3H²φ²)** (any history); −(3/2)γH²φ²/c² at fixed norm | (γ/2c²)φ²(2Ḣ + 3H²) | NO SOLUTION (sign) |
| (b) −(γ/2)(∇_μP^μ)² | **−(γ/2c²)(φ̇ + 3Hφ)²** (any history); −(9/2)γH²φ²/c² at fixed norm | (3γ/2c²)φ²(2Ḣ + 3H²) | NO SOLUTION (sign) |
| (c) −(γ/4)F_μνF^μν | **0** (F ≡ 0 on the ansatz) | 0 | IDENTITY (vanishing) |
| (e) −(γ/2)∇_μP_ν∇^νP^μ | −(3/2)γH²φ²/c² | (γ/2c²)φ²(2Ḣ + 3H²) | (reported) |
| −(γ/2)R_μνP^μP^ν | −3γH²φ²/c² | (γ/c²)φ²(2Ḣ + 3H²) | (non-minimal piece) |
| −(γ/2)R P_μP^μ | −3γH²φ²/c² | (γ/c²)φ²(2Ḣ + 3H²) | (non-minimal piece) |

**Family (G).** L = −(γ/2)[½F² + (∇·P)² + ξR_μνP^μP^ν + ζRP²] reproduces the record's static −(γ/2)|∇P|² exactly for every
(ξ, ζ). At fixed norm it gives ε = −A γH²φ²/c², with **A(ξ, ζ) = 9/2 + 3ξ + 3ζ**.
- Structure (a) is ξ = −1, ζ = 0 (A = 3/2, checked).
- The energy is positive only if ξ + ζ < −3/2. Non-minimal couplings can therefore choose the sign, but they cannot change the
  size: the energy stays ∝ γH²φ².

**Any dimension (K6).**
- A_a = n/2 and A_b = n²/2: negative in every d.
- ε_c = 0.
- A_Ric = A_R = n(n−1)/2.
- So no choice of dimension rescues the route (S3).

**Equation of state.** At fixed norm, w_s = −1 − 2Ḣ/(3H²) = w_total for every structure.
- The term is an Einstein-aether-type H² piece. It enters the Friedmann equation as a renormalisation of G:
  G_cosmo/G_N = 1/(1 + δ), with **δ = (A/3)(a₀L*/c²)²** at 4πG|P| = a₀.
- At the fitted κ = ½ (report only), δ = 3.0e-19 to 1.6e-15 for L* from 24 pc to 1 kpc. That is far below BBN/CMB
  sensitivity (of order 1e-1 to 1e-2), so it cannot be tested.
- **Side result:** at the background level, the covariant stiffness is cosmologically harmless.

**Free branches (N4, no constraint and no potential).**
- **(b):** the EOM is ∂_μ(∇·P) = 0, so ∇·P = C. This gives ε = −γC²/2 and p = +γC²/2: exactly w = −1, but negative
  (the AdS sign), and C is a free integration constant. Class **CONDITION**. This is the only w = −1 piece the stiffness can
  make, and it has the wrong sign.
- **(a):** φ̈ + 3Hφ̇ − 3H²φ = 0. In de Sitter, φ ∝ e^{λHt} with λ = (−3 ± √21)/2 = 0.791 and −3.791. The growing mode drives
  ε_a negative without bound, so there is no constant energy. Class **NO SOLUTION**.

**Normalisations N2 and N3.**
- N2: the tether 4πG P = −g_c gives P = 0 on FRW, because g_c = 0 by isotropy.
- N3: the law's own vacuum, g_N = 0, gives u = 0.
- Both vanish identically (IDENTITY).

## The matching, and the κ it would need

Ignore the sign and match the size, |ε_s| = ρ_DE c², at 4πG|P| = a₀, with H² = 8πGρ_DE/(3Ω_H):

  **a₀,needed = √(3Ω_H/|A|) · c²/L*,  κ_needed = √(3Ω_H/|A|) · c/(L*√(Gρ_DE)).**

- κ depends on L* (d ln κ/d ln L* = −1, I2), so the route is a TRADE.
- An exact ½ would need L* = 2√(3Ω_H/|A|)·c/√(Gρ_DE), which is horizon scale.
- At Ω_H = 1 the condition loses ρ_DE altogether. It is then the degenerate point of the renormalised Friedmann equation
  (G_cosmo → ∞), not a determination of a₀ by ρ_DE (I5 note).

| variant (fixed norm, N1) | sign | min \|κ_Λ\| for L* ∈ [24 pc, 1 kpc] | min \|κ_crit\| | L* needed for κ_Λ = 0.607 |
|---|---|---|---|---|
| (a) minimal, A = 3/2 | negative: no solution | 1.82e7 | 1.51e7 | 30.0–36.2 Gpc |
| (b) minimal, A = 9/2 | negative: no solution | 1.05e7 | 8.70e6 | 17.3–20.9 Gpc |
| (G) ξ = ζ = −10, A = −111/2 (positive, most favourable O(1)) | positive | 2.99e6 | 2.48e6 | 4.9–6.0 Gpc |

- **The window.** W_data is [0.227, 0.607] on ρ_DE and [0.189, 0.501] on ρ_crit. Every variant misses it by more than 6.5
  orders of magnitude.
- **The L* it would take.** Reaching the window needs L* ≥ 4.9 Gpc ≥ 1.1 c/H₀. An L* that large would screen every galaxy
  (CFG820 K1: L* → ∞ gives Newton).
- **The curvature coupling it would take.** At L* = 1 kpc (or 24 pc) the window needs |A| = 2.0e15–1.4e16 (or 3.4e18–2.4e19),
  i.e. |ξ + ζ| ~ 1e15–1e19. That is a new hand-set horizon-scale constant, not a derivation.
- **The old floor.** At L* = 5.75 pc, κ_needed is 1.8–3.8e9 for the minimal variants.
- **The tuned positive branch also fails.** Tune it so that ε_s(today) = ρ_DE c². Because ε_s ∝ H², this forces
  G_cosmo/G_N = 1/(1 − Ω_Λ) = 3.17 and produces no acceleration, since an H² term only rescales G. BBN excludes it.

## Outcome (frozen rule)

| variant | class |
|---|---|
| (c) Maxwell, any normalisation | IDENTITY (vanishing) |
| N2 tether, N3 law vacuum | IDENTITY (vanishing) |
| N4 (b) free | CONDITION (free C; negative) |
| N4 (a) free | NO SOLUTION (sign; runaway) |
| (a), (b) fixed norm (N1 and every \|KP\| < a₀) | NO SOLUTION (sign); magnitude-only κ ≥ 1.05e7 |
| (G) O(1) non-minimal, positive branch | MISS (TRADE, magnitude), EXCLUDED (L*_needed ≥ 4.9 Gpc) |

- **Overall: CLOSURE.** No variant is CONSISTENT, and every check passes.
- **Option space.** p_exact = 0 (TRADE form) and p_data = 0.
- **S4 (second prediction).** δ_G ~ 1e-19 to 1e-15 gives p_second ≈ 1, so it carries no information.
- **The LEE statistic does not move.** The row is not determinate (cls `free`), so P_LEE(exact) = 0.20 and P_LEE(data) are
  unchanged when it is added.

## Checks: 35/35 PASS (`cfg897.out`)

- **I1** No forbidden constant is used. The only occurrence of the measured κ is the quoted standing-fact line.
- **K1** Scalar-field sanity of the ε/p extraction.
- **K2** Static flat limit. (a) = (b) + ½F² + a total derivative (variational check). The Maxwell form vanishes on curl-free P,
  so alone it cannot carry CFG770's longitudinal screening.
- **FRW results.**
  - ε_a and ε_b are negative semi-definite for every history (the hand estimate reproduced).
  - ε_c ≡ 0.
  - w_s = w_total.
- **K3** ∇_μP_ν∇^μP^ν − ½F² − (∇·P)² + R_μνP^μP^ν and ∇_μP_ν∇^νP^μ − (∇·P)² + R_μνP^μP^ν have identically vanishing
  Euler–Lagrange derivatives in N, a and φ (total derivatives).
- **K4** ε̇ + 3H(ε + p) = 0 at fixed norm (all five structures) and on the free stiffness EOM, for (a) and (b).
- **K5** V2 (P⁰ fixed) and V3 (P₀ fixed) with the norm constraint reproduce V1 exactly.
  - The naive off-shell values without the constraint differ, e.g. +(3/2)γH²φ² for (a) in V2: an off-shell evaluation would
    flip the sign. Only the constrained (on-shell) value is used.
- **K6** General d, n = 2…5.
- **K7** Agreement with the Einstein-aether form ε = −3αm²H², p = αm²(2Ḣ + 3H²), α = β₁ + 3β₂ + β₃ (Carroll & Lim 2004,
  "Lorentz-violating vector fields slow the universe down"). This is a consistency check, not an input.
- **K8a** δ from the Friedmann bookkeeping.
- **K8** Dimensions.
- **I2** κ_needed ∝ c G^{−1/2} ρ^{−1/2} L*^{−1}, with ħ⁰: a TRADE.
- **I3** At fixed L*, κ → ν/√(λμ) κ: a pure number only if L* ∝ c/√(Gρ).
- **I4** Set the law's κ to 0.4. a₀,needed and κ_needed do not move. The fraction ε_s/ρ_DE c² = A Gρ_DE L*² κ²/(3Ω_H c²) does
  move (it is a consistency relation).
- **I5** Not a Friedmann tautology.
- **I6** Footing as declared.
- **I7** ħ-power 0.
- **I8** The prefactor 3Ω_H/A has π-weight 0 (TRADE class).

## MUTATE (`cfg897_MUTATE.out`, exit 1): 5/5 bite

- **M1** γ → 0: ε_a = ε_b = 0, so there is no κ.
- **M2** d = 4 → 5: A_a 3/2 → 2 and A_b 9/2 → 8; κ moves × 0.8660 and × 0.7500, as stated.
- **M3** 4πG|P| = 2a₀: |ε| × 4 and κ × ½.
- **M4** γ → −γ, the sign the static limit forbids: ε_a and ε_b turn positive, and NO SOLUTION becomes a real κ of the same
  size (9.17e8 at 24 pc). The sign verdict is computed, not hard-coded.
- **M5** K = 4πG → 8πG: |ε| × ½ and κ × √2.

## Scope and assumptions (flagged)

- **Not re-evaluated here.**
  - The coupling term −|∇Φ − KP|²/2K and W_rem at the cosmic state are not re-evaluated.
  - They belong to the excluded slot class (X2, energy ~ a₀²/G) and the kernel-vacuum class (X10/CFG807: ill-defined, free
    additive constant).
  - At 4πG|P| = a₀, W_rem is singular (CFG807 V1; the p63-C1 gate).
- **This is a bound, not one value.** N1 is the largest norm CFG695 allows, so the size bound holds for every norm below it.
- **Covariant completion.** It is not unique. The declared structures and the family (G) cover every two-derivative quadratic
  form with the right static limit. Couplings of higher order or with a coefficient built from c²/a₀ are outside the option
  space: with that coefficient the energy becomes independent of a₀, which fails S2.
- **Not addressed.**
  - Stability of the timelike mode. Without a constraint, (a) has the wrong-sign temporal kinetic term (the N4 runaway).
  - Preferred-frame PPN effects of a timelike background. They are of order δ, so negligible.
- **No overlap with p63-C1.** That lane identifies ρ_Λ with the linear bound charge ∇_μP^μ; it is registered and unrun.

## Disclosures

- **Hand estimates before the freeze** (in the criteria): ε_a, ε_b, ε_c, w_s = w_total, the size of δ, and κ_|.| ~ 1e7–1e9.
  The script reproduced them. The door's own guess of a positive κ ~ 1e6–1e8 matches the size only; on shell the sign is
  negative.
- **Run history (K8 only).** Runs 1 and 2 failed K8 because of a bug in the check code, not in the physics: the units test
  compared the whole expression, including the pure numbers √3 and 1/3, to 1.
  - Run 2's first fix (`as_coeff_Mul`) does not strip √3.
  - Run 3 uses `as_independent`.
  - Both failed outputs are kept: `cfg897_firstrun_K8fail.out` and `cfg897_secondrun_K8fail.out`.
  - The diff between run 1 and run 3 is confined to the K8 line, the label (VOID → CLOSURE) and the check count. No criterion,
    number or class changed.
- **Numbers.** δ is evaluated at the fitted κ = ½ for reporting only. It scales as κ², so anywhere in W_data it lies within a
  factor of about 5 of that value.

κ = ½ FITTED (κ_Λ 0.417 ± 0.095, CFG493). Not theory closed.
