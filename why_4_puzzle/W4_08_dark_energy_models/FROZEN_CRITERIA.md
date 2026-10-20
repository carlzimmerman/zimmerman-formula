# W4-08: do the dark-energy models themselves fix the 4? (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-08 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
**κ = ½ is FITTED.** Not theory closed.

## Question

The law ties a₀ to ρ_DE, but every κ lane so far worked from the a₀ side or from gravity. W4-08 works from the dark-energy
side: if a dark-energy model fixes ρ_DE in terms of its own scale with no free amplitude, that scale could be the a₀ scale.
Checked 2026-10-20, families with **no CFG894 register row**: holographic (Li) 0, agegraphic 0, Chaplygin 0, Cardassian 0,
LQC 0, Dirac large numbers 0, interacting dark energy 0. Already registered (cross-references only): CKN, which is the
saturated holographic bound (FL12, RR-24/25); causal sets (1); the k-essence and quintessence trackers (W11, sol61-105).

## Families, defining relations (from memory, PROVISIONAL; nothing downloaded) and hand expectations

Units c = 1; M_P² = 1/(8πG); κ² = a²/(Gρ_DE).

| id | model | ρ_DE relation | natural a | hand expectation |
|---|---|---|---|---|
| E1 | holographic dark energy (Li 2004) | ρ = 3c_H² M_P²/L², with L the future event horizon | a = c²/L | κ² = 8π/(3c_H²): TRADE in c_H. At c_H = 1 (saturated, CKN) it is 8π/3, H-type π-odd (already registered). |
| E2 | agegraphic (Cai 2007) | ρ = 3n² M_P²/T², with T the cosmic age | a = c/T | κ² = 8π/(3n²): TRADE in n |
| E3 | generalized Chaplygin, p = −A/ρ^α | ρ → A^{1/(1+α)} at late times | none intrinsic | TRADE (A, α) |
| E4 | Cardassian (Freese–Lewis) | H² = (8πG/3)(ρ_m + Bρ_mⁿ) | none intrinsic | TRADE (B, n) |
| E5 | exponential-potential scaling attractor | Ω_φ = 3(1 + w_b)/λ² | a = cH | ρ_φ = Ω_φ·3H²/(8πG), so κ² = 8π/(3Ω_φ) = 8πλ²/(9(1+w_b)): TRADE in λ |
| E6 | LQC bounce density | ρ_c = √3/(32π²γ³) ρ_Pl, with γ fixed by black-hole entropy | none at the a₀ scale | HBAR: ρ_Pl ∝ c⁵/(ħG²), off by ~10¹²²; a Planck-scale density, not dark energy |
| E7 | causal-set everpresent Λ (Sorkin) | Λ ~ α_s/√V₄ ~ α_s H², stochastic | a = cH | ħ cancels; H-type π-odd with α_s a random O(1) amplitude: TRADE |
| E8 | Dirac large numbers | G ∝ 1/t, a₀ ~ cH coincidence | a = cH | H-type; G ∝ 1/t is excluded by lunar-ranging bounds on Ġ/G (recalled). CLOSURE. |
| E9 | interacting dark energy, Q = ξHρ_DE | ξ free | none intrinsic | TRADE |

## Inputs, footing, π / ħ

- Inputs: symbols only (c_H, n, A, α, B, λ, γ, α_s, ξ, ħ, G, H, L, T). No a₀ value, κ, Z or Ω_Λ.
- Footing: ρ_DE.
- π: E1, E2 and E5 are π-odd via M_P² = 1/(8πG).
- ħ: E6 only. E7 cancels it, shown symbolically.

## Checks

- **I1:** no forbidden constant in the compute block.
- **I2:** κ² is symbolic; free symbols are printed.
- **I3:** κ² is dimensionless (E6 with SI symbols).
- **I7:** ħ power printed.
- **K1:** E1 at c_H = 1 equals E2 at n = 1 equals the DGP crossover value 8π/3 (W4-01): the saturated horizon routes agree.
- **K2:** E7's ħ cancellation, Λ ~ ℓ_P²·(V₄/ℓ_P⁴)^{−1/2} with ℓ_P² = ħG/c³.
- **K3:** each hand value equals the script's symbolic value.
- **K4:** E6's density in SI exceeds ρ_DE by more than 10¹⁰⁰. Evaluated with SI constants and a declared ρ_DE = 6e-27 kg/m³
  order-of-magnitude placeholder, labelled as such; not a measured input to any κ.

## Outcome classes and verdict (CFG894 §7)

- Per family: EXACT / CONSISTENT / MISS / MENU / TRADE / HBAR / CLOSURE.
- **Lane verdict (frozen):**
  - **NO MODEL FIXES THE 4:** every family is TRADE, HBAR, CLOSURE, or H-type π-odd at a saturated parameter.
  - **CANDIDATE:** any EXACT CANDIDATE.
- Hand expectation: **NO MODEL FIXES THE 4.** The saturated horizon versions reduce to 8π/3 (κ 2.89), the record's recurring
  H-type value.

## Mutation control (`W4_08_MUTATE=1`, separate outputs, exit 1 when it bites)

- **M1:** reduced → non-reduced Planck mass (M_P² = 1/G) in E1, E2 and E5. Expected: κ² loses its 8π. K3 must FAIL.
- **M2:** E7's fluctuation exponent N^{−1/2} → N^{−1/3}, with N = V₄/ℓ_P⁴. Expected: ħ no longer cancels, so K2 must
  FAIL. Note: the reduced-Planck-length swap ℓ_P² → 8πħG/c³ would NOT move E7, because Λ ~ ℓ_P⁻²N^{−1/2} = V₄^{−1/2}
  is exactly independent of ℓ_P's normalisation; it was rejected as a control for that reason.

## Files

`w4_08.py`, outputs, `README.md`. One register row per family (E1–E9), then `kappa_campaign_lee.py` rerun.
