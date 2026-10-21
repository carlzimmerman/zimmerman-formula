# W4-11: the last gravity classes with no register row (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-11 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
**κ = ½ is FITTED.** Not theory closed.

## Question

After W4-01, W4-05, W4-07 and W4-09, four gravity classes still have **no CFG894 register row** (checked 2026-10-20): f(Q)
nonmetricity 0, f(R,T) 0, bumblebee 0, Weyl conformal geometry 0. Does any of them fix κ? The criterion is unchanged: a
fixed ρ_DE / a₀ ratio with no free coupling, ħ-free, and through c.

## Classes (structure only; detailed field equations are quoted from memory, PROVISIONAL; nothing downloaded)

| id | class | own vacuum | reading | hand expectation |
|---|---|---|---|---|
| Q1 | f(Q) = Q + αQⁿ, symmetric teleparallel, coincident gauge, Q = 6H² on flat FRW | On flat FRW its background equations map onto f(T)'s with T ↔ −Q (recalled, provisional), so the power-law correction self-accelerates exactly as f(T) does (W4-01 F6) | a² = \|Q_*\| with α\|Q_*\|^{n−1} = 1 | κ² = 16π(2n−1)^{1/(n−1)}: TRADE in n, π¹ at rational n (= W4-01's f(T)) |
| Q2 | f(R,T) = R + 2λT (Harko et al.) | in vacuum T = 0, so the theory is GR; Λ free | none intrinsic | TRADE (Λ, λ) |
| Q3 | bumblebee (vector B_μ, potential V(B² ∓ b²)) | vacuum B² = ±b²; V at its minimum is free | a = c²/b-scale (if b is a length) | TRADE (b and the vacuum constant are independent) |
| Q4 | Weyl conformal geometry (Ghilencea: R̃²/(4!ξ²) − F²/(4q²), broken to Einstein–Proca) | Λ ∝ ξ² M_P² from the broken phase, with ξ and q free and M_P carrying ħ | a = mass of the Weyl vector, m² ∝ q² M_P² | HBAR (via M_P) / TRADE (ξ, q) |

## Checks

- **I1:** no forbidden constant in the compute block.
- **I2:** κ² is symbolic with free symbols printed.
- **K1:** Q1 reduces to W4-01's f(T) value under the T ↔ −Q map (sympy identity).
- **K2:** Q2's vacuum trace equation with T = 0 gives R = 4Λ for any Λ (free).
- **K3:** the hand values are reproduced.

Classes: as in CFG894 §7. **Lane verdict:** NO CLASS FIXES THE 4 if all are TRADE or HBAR; CANDIDATE on any EXACT.
Hand expectation: **NO CLASS FIXES THE 4.**

## MUTATE (`W4_11_MUTATE=1`, exit 1 when it bites)

- **M1:** Q1 with the f(T) Friedmann normalisation 2·8πG → 2·4πG. Expected: κ² halves, so K3 must FAIL.
- **M2:** Q2 with a nonzero vacuum trace T = −4ρ_v (a cosmological-constant source). Expected: R gains a λ term, so K2's
  "any Λ" form must FAIL.

## Files

`w4_11.py`, outputs, `README.md`. One register row per class (Q1–Q4), then `kappa_campaign_lee.py` rerun.
