# OUT-3 (SCALE-FREE BOUNDARY) — κ = ½ ⟺ the formation normalisation equals the vacuum value

Lane family OUT, arm 3. TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing.
Footings graded separately and **never pooled** (canonical a₀ = 9.3603e-11, alt a₀ = 1.1312e-10 m/s²).
Cold dark energy is a **gravitating field component**, never a particle; the dark mass IS the sector's own
stress-energy — stated as the claim, with no ΛCDM hedge.
**κ = ½ FITTED; not theory closed.** This lane edits nothing outside its own folder.

**Committed alone, before any OUT3 script exists and before any OUT3 number is computed.**

---

## Honesty flag

This file is written **after** reading, and it reuses numbers from: `hy4_preview_push/FRAMEWORK.md`
(the G_λ symmetry statement), `closure_2026_11_11/FINAL6_kappa_formation` (Q1 form / Q2 coefficient),
`FINAL16_kappa_real` (flat direction), `FINAL18_kappa_fold` (fold matching: real constraint, 1.24–2.23 dex
mismatch, 1.86 dex mass drift, κ_M = 1.19e-3), `FINAL19_kappa_C` (deep-field column: R = 6.0 ± 1.4,
κ = √(2π) forced), `FINAL15_formation` (the ledger, X_f = X_L(g_b,f)), and
`fable52_push/FLD1_fold_reach` (the R_fold table). **This is therefore not a blind pre-registration.**
What is clean and frozen here: the three admissible matched-units pairs (§2), the six gates and their
thresholds (§4), and the mutation arms (§5). What is *not* clean: I already know FINAL-18 and FINAL-19
failed in the share and column slots, so the energy-density slot (arm A) is the only one with a real
chance, and I have chosen it as primary for that reason.

---

## 0. The take under test

> **κ = ½  ⟺  N_f = N_v**

with `N_f` the **formation normalisation** — the cold sector's dimensionless normalisation as pinned on the
fold Σ_f — and `N_v` the **vacuum value** of the same dimensionless normalisation, i.e. the value the
sector has where there is no halo: the cold dark energy, w = −1, uniform.

The equation is **scale-free** by construction: both sides are dimensionless and both are referred to the
sector's own unit, so no choice of a₀ enters the *statement* of the condition. Whether it *solves* for a₀
is gate G2.

---

## 1. The mechanism (the physical claim, in words)

The clock sector is one field with one conserved cold charge. In vacuum it is the cold dark energy:
uniform, w = −1, energy density ρ_Λ c². Around baryons it is the dark mass: the same stress-energy,
rearranged and pinned. The fold Σ_f — the first hypersurface going into collapse on which the clock's
expansion along its own normal θ_K vanishes — is the **boundary** between the two regimes: interior to it
the sector is static and carries the law; exterior to it the sector is still dust/background. The
framework's own symmetry statement is that the formation equations depend only on the ratio a₀/g, so the
map G_λ : (a₀, g) → (λa₀, λg) is an exact symmetry of them and κ is the only quantity charged under it
(FRAMEWORK.md §2). The **scale-free boundary** condition is the one statement that can break that
degeneracy without naming a number: it demands that the sector's normalisation be **continuous through
Σ_f** — the value the collapse pins inside equals the value the vacuum already has outside. If the two
sides are referred to the same dimensionless unit, that demand is an equation, and if it is an equation
in κ it *derives* κ. The three things that can go wrong, and which this lane grades, are: (i) the two
sides may carry the *same* G_λ weight, in which case the equation is either an identity or impossible and
κ stays a flat direction; (ii) they may carry different weights but return a number far from ½; (iii) they
may return ½ at one mass only, which is not a derivation because a₀ is universal to 0.041 dex.

---

## 2. Definitions (frozen): three admissible matched-units pairs

`u_f ≡ a₀/g_b,f = (R_f/r_M)²`, `r_M ≡ √(G M_b/a₀)`, `X(u) ≡ (√(1+4u) − 1)/2` (FLD1's exact share),
`R_f` = FLD1's R_fold, `M_b` the baryons inside R_f at the fold, `Z ≡ √(8π/3)`.

**Formation normalisation — three admissible dimensionless readings:**

| id | slot | definition | depends on |
|---|---|---|---|
| **F1** | energy density | `N_f = G ρ_c(Σ_f) c²/a₀²`, `ρ_c = 3 X(u_f) M_b /(4π R_f³)` | a₀, R_f, M_b |
| **F2** | column | `N_f = Σ_c(Σ_f)/(a₀/G)`, `Σ_c = M_C/(4πR_f²)` → `= X(u_f)/(4π u_f)` | u_f |
| **F3** | share | `N_f = X(u_f)` | u_f |

**Vacuum value — three admissible dimensionless readings, in the same units:**

| id | slot | definition |
|---|---|---|
| **V1** | energy density | `N_v = G ρ_Λ c²/a₀² = 1/κ²` |
| **V2** | column | `N_v = ρ_Λ R_Λ/(a₀/G) = 1/(Z κ)`, `R_Λ = c/H_Λ`, `H_Λ = c√(8πGρ_Λ/3)` |
| **V3** | share | `N_v = ρ_Λ/ρ_b,0 = Ω_Λ/Ω_b` |

**Admissible arms are the unit-matched pairs only: A = (F1,V1), B = (F2,V2), C = (F3,V3).**
Mixing slots (e.g. F1 with V2) compares an energy density to a column and is **inadmissible**; such pairs
are recorded in `out3_menu.out` under "mismatched" and are not graded and not counted.

**Arm A is the primary arm.** Rationale, stated now and not revisited: arms B and C are the column and
share slots, and those slots were already graded by FINAL-19 (column, R = 6.0 ± 1.4, κ = √(2π) forced) and
FINAL-18 (share/charge continuity at the fold, κ_M = 1.19e-3). Arm A — the **energy density** at the fold
matched to the vacuum energy density — is the literal reading of "the formation normalisation equals the
vacuum value" in the slot where the a₀-sector's vacuum constant lives (p09/K010's `U_v = 32π ⟺ W_v = 4`,
K014's `ρ_L = W a₀²/G`), and it has not been run at the fold. Arms B and C are run here as **sibling
arms**, on the same fold table, so that the three slots are graded together on one footing.

---

## 3. The algebra to be certified (Lean, `OUT3.lean`)

1. `kappa_def` — `N_v(V1) = 1/κ²` exactly, from `a₀ = κ c √(Gρ_Λ)`.
2. `iff_half` — `N_v(V1) = 4 ⟺ κ = ½` for κ > 0. **(This is the IFF of the take. It is an identity.)**
3. `armA_iff` — `N_f(F1) = N_v(V1) ⟺ ρ_c(Σ_f) = ρ_Λ` (the a₀² cancels; the condition is on the density).
4. `armA_invert` — `ρ_c(Σ_f) = ρ_Λ` with `X(1+X) = x²` inverted exactly gives
   `a₀ = G M_b q(1+q)/R_f²` with `q ≡ 4πρ_Λ R_f³/(3M_b)`; hence
   `κ_A = G M_b q(1+q)/(c√(Gρ_Λ) R_f²)`. No deep-field approximation.
5. `armB_invert` — `N_f(F2) = N_v(V2)` ⟺ `κ_B = [(1 + 8πũ/Z)² − 1]/(4ũ)`, `ũ ≡ c√(Gρ_Λ)R_f²/(GM_b)`.
6. `armC_invert` — `N_f(F3) = N_v(V3)` ⟺ `κ_C = s(1+s)/(Z² ũ)·…` → exactly `κ_C = Ω_Λ/Ω_b`-root:
   `κ_C = q_C(1+q_C)/ũ` with `q_C = Ω_Λ/Ω_b`.
7. `lambda_weight` — the G_λ weight `w ≡ d ln N/d ln λ` of each side, at fixed (M_b, R_f, ρ_Λ, G, c):
   `w(N_f,F1) = ½·(d ln X/d ln u) − 2`, `w(N_v,V1) = −2`; `w(N_f,F2) = ½·(d ln X/d ln u) − 1`,
   `w(N_v,V2) = −1`; `w(N_f,F3) = ½·(d ln X/d ln u)`, `w(N_v,V3) = 0`.
   In the deep-field limit `X ∝ √u` these are `−3/2, −2`, `−1/2, −1`, `+1/2, 0`.
   **All three arms therefore carry different weights on the two sides: if R_f is a₀-independent, no arm
   is a flat direction.** (This is the structural claim the lane exists to state and certify; it
   generalises FINAL-18's "real constraint, not a flat direction" from the share slot to all three.)
8. `fold_lambda_blind` — if instead the fold *rescaled* so that u_f were λ-invariant, all three arms would
   collapse to a flat direction (weights equal). This is the counter-theorem, and it is why the measured
   `d ln R_f/d ln a₀ = 2.9e-3 dex/dex` (FINAL-18) is load-bearing: it is the number that decides between
   "real constraint" and "flat direction".

---

## 4. Gates (frozen thresholds; graded in this order, first failure is not masked)

Constants: Planck h = 0.674, Ω_Λ = 0.685, Ω_b = 0.0493, G = 6.67430e-11, c = 2.99792458e8,
M_sun = 1.989e30. Footings a₀ = 9.3603e-11 (canonical) and 1.1312e-10 (alt), never pooled.
Fold table: FLD1's `RESULT.md` (R_fold at z = 0/1/2/4 and R_ta at z = 0, log M_b = 7 → 11.5, canonical;
alt differs by < 0.5 % in R_fold).

| gate | statement | pass threshold |
|---|---|---|
| **G1** | the IFF of the take is exact (κ = ½ ⟺ N_v = 4 in slot V1) | Lean `iff_half` compiles; identity, expected PASS |
| **G2** | is `N_f = N_v` a real constraint or a flat direction? | the two sides' G_λ weights differ by ≥ 0.1, **and** the equation has at most one root in a₀ (Lean `fold_match_unique`-style). PASS = real constraint |
| **G3** | **the number** — does the root land on ½? | \|log₁₀(κ_arm/0.5)\| ≤ 0.0212 (5 %) for the *measured* a₀'s own footing, at some mass in the grid |
| **G4** | **universality in mass** — is the root mass-independent? | drift of log₁₀ κ_arm over log M_b ∈ [7, 11.5] ≤ 0.041 dex (the canonical/alt footing spread 0.5log₁₀(1.1312/0.93603); the RAR requires a₀ universal to about this) |
| **G5** | **universality in epoch** — is the root redshift-independent? | drift over z ∈ [0,4] ≤ 0.041 dex |
| **G6** | **mutation** — do the controls bite? | ≥ 3 of the 4 pre-registered mutation arms move the primary number by ≥ 5 % in the stated direction |

**Label vocabulary (frozen):** PASS / FAIL / NO VERDICT. The lane's headline label is
**DERIVED** iff G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5 all PASS; **NOT DERIVED (FITTED)** otherwise, with the
failing gates named.

---

## 5. Mutation arms (frozen, run against arm A at log M_b = 10.45, z = 0, canonical)

| arm | change | expected direction of κ_A if the mechanism is real |
|---|---|---|
| **M1** | ρ_Λ → ρ_crit (the alt footing's density; Ω_Λ → 1) | κ_A moves ∝ ρ_Λ^{3/2}, so **up** by (1/0.685)^{3/2} = 1.77 |
| **M2** | R_f → 0.52 R_ta (FLD1's own ratio) instead of FLD1's tabulated R_fold | changes κ_A only through R_f⁴ |
| **M3** | mass × 10 (log M_b 11.45) | κ_A ∝ R_f⁴/M_b ∝ M_b^{1/3}, so **up** by 10^{1/3} = 2.15 |
| **M4** | the vacuum value read at z = 4 (ρ_Λ fixed, R_f from FLD1's z = 4 column) | R_f falls by ×8, so κ_A **down** by 8⁴/1 = 4096 |

---

## 6. Outputs

`out3.py` → `out3.out`, `out3.json`, `out3_menu.out`; `out3_MUTATE=1` → `out3_MUTATE.out/.json`;
Lean `OUT3.lean` → `compile.txt`, `OUT3_MUTATE.lean` → `compile_MUTATE.txt`; `RESULT.md`.
