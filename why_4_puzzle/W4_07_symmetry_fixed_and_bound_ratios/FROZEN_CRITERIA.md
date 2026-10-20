# W4-07: ratios fixed by a symmetry or by a consistency bound: can any fix the 4? (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-07 script exists.** Append-only after this commit. Rules:
`campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CAMPAIGN_RULES.md`. **κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ±
0.095). Not theory closed.

## Question

L32 (N4, RIGIDITY) says a derivation needs a ratio fixed by discrete or structural data, not by a continuous coupling. W4-05
showed that theories which fix their own vacuum give κ² = 8π × algebraic. Two classes on record have **no CFG894 register
row** (checked 2026-10-20: swampland 0, WGC 0, TCC 0, dS conjecture 0, Higuchi 0, partially massless 0, S-matrix 0):
1. ratios fixed **by a gauge or conformal symmetry** in de Sitter;
2. ratios fixed **by saturating a consistency bound** (the swampland conjectures, the species scale, amplitude positivity).

Does any of them fix ξ in a₀² = ξ G ε_DE (κ² = ξ), ħ-free, with no free coupling?

## Items, starting relations (from memory, PROVISIONAL; nothing downloaded) and hand expectations

Units c = 1; ρ_DE = 3H²/(8πG) on the de Sitter background, generalised to H² = 16πGρ/((d−1)(d−2)) for the dimension test.

| id | principle | fixed relation | reading for a₀ | hand expectation |
|---|---|---|---|---|
| B1 | **Partially massless spin-2** (Higuchi bound saturated; Deser–Waldron gauge symmetry) | m² = (d−2)H², which is 2H² at d = 4 | a = m c² | κ² = 16π/(d−1), so 16π/3 at d = 4, κ = 4.09. MISS, π × algebraic. A symmetry fixes the ratio, but through H. |
| B2 | **Conformally coupled scalar** in de Sitter (ξ_c = (d−2)/(4(d−1))) | m_eff² = ξ_c R = ξ_c d(d−1)H² | a = m_eff c² | R = d(d−1)H², so m_eff² = d(d−2)H²/4 and κ² = 4πd/(d−1): 16π/3 at d = 4 (equal to B1 there), 5π at d = 5. MISS, π × algebraic. |
| B3 | **Weak-gravity conjecture saturated** (m = √2 g q M_P) with the seesaw a₀ = m²/M_P | a₀ = 2g²q² M_P | a₀ itself | ħ-bearing through M_P (∝ ħ^{1/2}), with g free: HBAR / TRADE |
| B4 | **dS swampland conjecture** \|V′\|/V ≥ c_S/M_P | an inequality on the quintessence slope | none | BOUND, not a selection (S2). ħ via M_P. |
| B5 | **Trans-Planckian censorship** | inequalities on Λ and on inflation | none | BOUND |
| B6 | **Species scale** Λ_sp = M_P/√N | N free | a₀ = Λ_sp²/M_P = M_P/N | TRADE (N), ħ-bearing |
| B7 | **Seesaw realised microscopically** (Berezhiani–Khoury superfluid: a₀ = α³Λ²/M_P; identify Λ⁴ = ε_DE in natural units) | ħ cancels | a₀ = α³√(ε)/M_P | κ² = α⁶ with non-reduced M_Pl, or 8πα⁶ with reduced M_P. TRADE in α; the π enters only through the Planck-mass convention. κ = ½ needs α = 2^{−1/3} or (32π)^{−1/6}. |
| B8 | **Flat-space amplitude positivity** | sign constraints on EFT coefficients | — | CLOSURE (structural): a constant vacuum energy does not enter any flat-space scattering amplitude, so no amplitude bound links a₀ to ε. In de Sitter it enters through H, which is H-type. |

## Inputs, footing, π / ħ

- Inputs: symbols only (H, G, m, g, q, M_P, ħ, α, N, d), plus each principle's own pure numbers. No a₀ value, κ, Z or Ω_Λ.
- Footing: ρ_DE.
- π:
  - B1 and B2 are declared `odd` (π × algebraic).
  - B7's π depends on the Planck-mass convention, and that dependence is the MUTATE.
- ħ: B3 and B6 carry ħ^{±1/2}. B7 cancels ħ only under the identification Λ⁴ = ε (shown symbolically).

## Checks

- **I1:** no forbidden constant in the compute block.
- **I2:** κ² is symbolic; free symbols are printed.
- **I3:** κ² is dimensionless, with ħ carried as M L² T⁻¹ in SI-style symbols for B3, B6 and B7.
- **I7:** ħ power of κ² is printed for every item.
- **I8:** κ²/π is algebraic for B1 and B2, and κ² ≠ ¼.
- **K1:** B1 and B2 are equal at d = 4 (2H² both) and differ at d = 5 (dimension test S3).
- **K2:** B7's ħ cancellation is shown by sympy with ħ, c and G explicit.
- **K3:** each hand value equals the script's symbolic value.

## Outcome classes and lane verdict (CFG894 §7)

- Per item: EXACT CANDIDATE / CONSISTENT / MISS / MENU / TRADE / HBAR / BOUND / CLOSURE / VOID.
- **Lane verdict (frozen):**
  - **RIGID BUT π-ODD:** every symmetry-fixed item is π × algebraic and misses, and every bound item is BOUND, TRADE or
    HBAR.
  - **CANDIDATE:** any EXACT CANDIDATE (then an audit lane plus §8).
- Hand expectation: **RIGID BUT π-ODD.** The partially massless point is the record's first true symmetry-fixed ratio, and it
  gives κ = 4.09, extending W4-05's dichotomy from "self-determined vacuum" to "symmetry-fixed ratio".

## Mutation control (`W4_07_MUTATE=1`, separate `_MUTATE` outputs, exit 1 when it bites)

- **M1:** d = 4 → 5 for B1 and B2. Expected: B1 κ² = 16π/4 = 4π, while B2 moves differently. K3 must FAIL.
- **M2:** reduced ↔ non-reduced Planck mass in B7. Expected: κ² changes by 8π. K3 must FAIL for B7.
- **M3:** Higuchi coefficient (d−2) → (d−1). Expected: B1 κ² changes. K3 must FAIL for B1.
- I1, I3 and K2 must still pass.

## Second predictions (stated, not scored)

- B1: a partially massless graviton in de Sitter has a specific helicity count, 4 instead of 5. Nonlinear completion is
  problematic (recalled, provisional).
- B7: superfluid dark matter has its own galaxy-cluster and phonon phenomenology.

## Files

`w4_07.py`, `.out`, `_results.json`, `_MUTATE.out`, `_results_MUTATE.json`, `README.md`. One register row per item (B1–B8),
then `kappa_campaign_lee.py` rerun.
