# D5_kappa_four: FROZEN CRITERIA (written and committed before any script or number)

Door: register door 1 (`deepseek_push/CANDIDATE_LAWS_REGISTER.md`, "NEW OPEN doors registered from DSF-21 §8"):
"scale-setting functional returning exactly 4 in ρ_DE c²/(a₀²/G)".

Standing rules: κ = ½ is FITTED. κ = Z/4π = 0.460659 (a₀ = cH_Λ/2π) is a POSTULATE (DSF-21 A75; Milgrom's relation).
Z = 2√(8π/3) = 5.78881. Two footings (canonical a₀ = 9.36e-11, alt 1.13e-10 m/s²), never pooled. No dark-matter
particle. Not theory closed. Nothing in this lane may be called "κ derived".

## 0. The exact statement of the door (convention fixed here)

a₀ = κ c √(G ρ_Λ)  ⇔  a₀² = κ² c² G ρ_Λ  ⇔  **ρ_Λ c² / (a₀²/G) = 1/κ² ≡ R**.
κ = ½ ⇔ R = 4 ⇔ G ρ_Λ = 4 a₀²/c² ⇔ Λ = 32π a₀²/c⁴ ⇔ a₀ = cH_Λ/Z (H_Λ² = Λc²/3 = 8πGρ_Λ/3).
The script verifies this chain symbolically (check K0).

## 1. What would count as a derivation (applies to anything this lane touches)

A construction counts as a derivation of R = 4 only if all three hold:
- **D1 (no insertion):** a named principle forces the number; neither ½, 4, 32π nor Z is written in, and no free
  O(1) choice is made after seeing the target.
- **D2 (look-elsewhere):** the class the principle belongs to does not land in the current data band by chance with
  probability ≥ 0.5 (P_cover below), OR the hit is exact and the class's exact-hit probability is < 0.0027.
- **D3 (second prediction):** the same principle fixes a second, independent observable not already fixed by the
  framework's own a₀ ∝ √ρ_DE law.

## 2. Angle T: a no-go theorem for the horizon-thermodynamic class (new as a stated, enumerated class result)

**Class H_D.** a₀ is a monomial Π_i X_i^{e_i} × c^a G^b ħ^d k_B^f, with the X_i drawn from the de Sitter horizon
quantities of H = H_Λ, each with its exact textbook coefficient:
r_H = c/H; A = 4πr_H²; V = (4π/3)r_H³; T_GH = ħH/(2πk_B); S_BH = k_B c³A/(4Għ); E_MS = c⁴r_H/(2G) (Misner–Sharp);
u_Λ = ρ_Λc² = 3c²H²/(8πG) (Friedmann); E_Λ = u_Λ V; E_Komar = 2E_Λ (|ρ+3p|c²V); g_s = cH (surface gravity).
Exponents e_i are rationals with denominator dividing D; the result must be an acceleration, ħ-free and k_B-free.
D = 1 (products and quotients only) and D = 2 (square roots allowed).

**Claims to be computed (not assumed):**
- T1 (reduction): every admissible monomial equals q·π^m·cH_Λ with q a positive real algebraic number (rational for
  D = 1) and m ∈ (1/D)ℤ; hence κ² = (8/3) q² π^(2m+1). Proof by dimensional analysis (ħ- and k_B-freedom force
  G's exponent to 0) plus π-weight bookkeeping; the script checks it on every enumerated monomial.
- T2: ½ ∉ S₁ (D = 1), by transcendence of π (κ² = rational × odd power of π ≠ ¼). Z/4π ∈ S₁ (κ² = 2/(3π)).
- T3: in S₂, ½ is reachable only with m = −½ and q² = 3/32; report the minimal enumerated constructions that hit it
  and whether any of them is free of an explicit square root of a π-odd block.

**Enumeration (declared grammar, no tuning):** at most three distinct blocks per monomial, each exponent in
{±1/D, ±2/D, …, ±2} (|e| ≤ 2), plus free powers of c, G, ħ, k_B solved for by dimensional analysis. Duplicate κ values
are merged (exact symbolic comparison of q² and m).

**LEE (frozen definitions):**
- Data bands (external, quoted, not refitted): CFG493 κ_Λ = 0.417 ± 0.095; DSF-21 A81 joint κ_P3 = 0.378 ± 0.121
  converted to the ρ_Λ convention by A81's own factor (κ_P3 = 0.41345 ⇔ κ = ½), i.e. κ_DE ≈ 0.457 ± 0.146.
  Band = ±2σ.
- p_elem: fraction of distinct S_D values in [0.1, 10] that lie in the band.
- P_cover: probability, for κ* log-uniform in [0.1, 10], that the band of the same fractional half-width centred on
  κ* contains ≥ 1 element of S_D (computed exactly on a fine grid, 10⁵ points).
- P_exact(½, 1%): number of distinct S_D values within ±1% of ½ (excluding ½ itself).
**Pass/fail and meaning (Angle T):**
- If T2 holds and P_cover(S₁) ≥ 0.5: **SCOPED NO-GO** for H₁: the class cannot give ½ exactly, yet it lands in the
  band with no evidential weight; any H₁ member fails D2 by construction.
- If ½ ∈ S₂ only through m = −½: the class H₂ "reaches" ½ only by the square-root insertion; that fails D1 unless a
  principle for the square root is named. Report as NO SELECTION.
- Second prediction (D3): every member of H_D predicts a₀ ∝ H_Λ (constant for w = −1) or, if H(z) is read, a₀ ∝ H(z).
  The script reports H(2.5)/H₀ for Planck ΛCDM (the record's Z1 number is 3.77); nothing in the class fixes a second
  number that depends on the coefficient. Expected: no D3 pass.

## 3. Angle A: audit of the record's "data select 4 among the natural caps" (FINAL_THEORY.md §1, l.144–156)

The claim: "the saturation cap admits only R ∈ {1, 2, 4} … 4 is the only natural value the data admit".
**Test:** take A19's OWN natural grid (β ∈ {1, 2}, χ ∈ {1, 2, 3, 4}, R = β²χ → {1, 2, 3, 4, 8, 12, 16}), plus A19's own
"repair" value R = 4π, plus the cap fractions R = n for n = 1…8. For each, z = (1/√R − κ_meas)/σ under both data bands.
- A1 (reproduction): R ∈ {1, 2, 4} under CFG493 reproduce A19 K10's 6.14 / 3.05 / 0.87σ to ±0.01.
- **Verdict V_A (frozen):** the claim is SUPPORTED if R = 4 is the only value of A19's own grid with |z| < 2 under
  CFG493; CONTRADICTED if ≥ 2 values have |z| < 2. Also report whether any grid value has |z| smaller than R = 4's.
- If CONTRADICTED, the README lists the file:line locations repeating the claim as a record error (read-only; we do
  not edit other lanes' files).

## 4. Footings
Report κ for both footing a₀ values (canonical 9.3603e-11, alt 1.1312e-10 m/s²) with the canonical Planck ρ_Λ
(H₀ = 67.4 km/s/Mpc, Ω_Λ = 0.6847), and the nearest element of S₁ and S₂ to each. Not pooled.

## 5. Script contract
`d5_kappa_four.py`: stdlib + sympy, single thread, seconds. One line per check `Kn PASS|FAIL value threshold`.
Checks: K0 convention chain; K1 T1 reduction on every enumerated monomial; K2 ½ ∉ S₁; K3 Z/4π ∈ S₁; K4 ½-hits in S₂
all have m = −½ and q² = 3/32; K5 LEE numbers computed and finite; K6 A19 reproduction (A1); K7 Angle-A verdict
computed for both bands. Exit 0 iff all checks pass. Writes `d5_kappa_four.out`, `d5_kappa_four_results.json`.
**MUTATE** (`D5_MUTATE=1`): replace Friedmann's 8π/3 by 1 (H² = Gρ_Λ, in u_Λ and in the κ conversion; drops the
Einstein 8π/3 bookkeeping). This must break K2 (½ becomes reachable in S₁, q = ½) and K3 (Z/4π leaves S₁); outputs `d5_kappa_four_MUTATE.out`, `d5_kappa_four_results_MUTATE.json`.

## 6. What this lane will not claim
No κ derived; no "data select ½"; no new data; no edits outside `doors_push_2026_10_22/D5_kappa_four/`.
