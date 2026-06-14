# The a₀ coefficient convention — H₀ vs H_Λ, and the apt comparison to Milgrom/Verlinde

**C. Zimmerman, 2026-06-13.** *Definitive clarification of which Hubble rate the framework's O(1) coefficient
is referenced to. Resolves a recurring conflation in the a₀/Z corpus (the cH₀-vs-cH_Λ / ρ_total-vs-ρ_DE bug):
the "clean" coefficient 1/Z = 0.173 is against **cH_Λ**, not cH₀. All numbers below are machine-verified
(Planck 2018, Ω_Λ = 0.6889). This is the single statement every writeup should use.*

## The canonical relations (machine-verified)

The framework's **formula** is `a₀ = c²√(Λ/32π) = 9.36×10⁻¹¹ m/s²` (the pure-Λ, ρ_DE value).

Writing the dimensionless coefficient against the two Hubble rates:

| relation | value | what it's against |
|---|---|---|
| **a₀ / cH₀** = √(3Ω_Λ/32π) | **0.143** ( = cH₀/6.97 ) | the **present** Hubble rate H₀ |
| **a₀ / cH_Λ** = 1/Z, Z = 2√(8π/3) | **0.173** ( = 1/5.789 ) | the **de Sitter / dark-energy** rate cH_Λ |

where **cH_Λ = c²√(Λ/3) = √(Ω_Λ)·cH₀ = 0.83·cH₀** (H_Λ is the asymptotic de Sitter Hubble rate set by Λ).

**The reconciliation (both are correct):** a₀/cH₀ = (1/Z)·√(Ω_Λ) = 0.173 × 0.83 = **0.143**. ✓ The two
coefficients differ by exactly **√(Ω_Λ) = 0.83** — and that factor **is the "why-now" / coincidence-problem
re-dressing**: it is unity only because we live near the Λ-domination epoch. It carries no extra physics; it
is the statement that ρ_DE ≈ ρ_total today.

## The rule (avoid the conflation)

1. **The clean geometric coefficient 1/Z = 0.173 is against cH_Λ, never cH₀.** Writing "a₀ = cH₀/Z" with
   1/Z=0.173 gives **1.13×10⁻¹⁰** (the ρ_total/H₀ reading), which is **+20% above** the
   canonical 9.36×10⁻¹¹ — a *different object*. The canonical value is a₀ = c·H_Λ/Z = 0.143·cH₀.
   *(Several early scripts — `reviews/a0_cH0_Z_check.py`, `reviews/Z_is_one_pure_number.py` — use the
   ρ_total form a₀ = (c/2)√(Gρ_c) = cH₀/Z and "rescue" it to 1.2×10⁻¹⁰ by setting H₀ = 71.5; that is the
   cH₀-vs-cH_Λ conflation, superseded by the canonical c²√(Λ/32π).)*

2. **Milgrom (a₀ ~ cH₀/2π, coeff 0.159) and Verlinde EG (a₀ = cH₀/6, coeff 0.167) reference cH₀.** So the
   apt comparison to them is the framework's **vs-cH₀ value, 0.143** — **not** 1/Z = 0.173.
   - **0.143 is the LOW outlier**, below both Milgrom 0.159 and Verlinde 0.167 — it is **not "bracketed"
     between them.** Any writeup claiming 1/Z=0.173 is "bracketed by 1/6 and 1/2π" is comparing across
     different Hubble rates and **overstates the agreement** (the 0.83 factor is doing the work).
   - The honest statement: against cH₀, the three coefficients are framework 0.143, Milgrom 0.159, Verlinde
     0.167 — an O(1) family spanning ~16%, which the SPARC a₀ (≥20% systematic, footing-bracketed
     7.8–11.3×10⁻¹¹; see `SPARC_RAR_FOOTING_BOTHWAYS_2026-06-13.md`) **cannot resolve.** Convention-compatible,
     non-diagnostic — the same verdict the H₀-hostage analysis reaches.

## The one-sentence version (use everywhere)

> a₀ = c²√(Λ/32π) gives **a₀/cH₀ = 0.143** (= cH₀/6.97) and equivalently **a₀/cH_Λ = 1/Z = 0.173** (= 1/5.789,
> against the de Sitter rate cH_Λ = √Ω_Λ·cH₀ = 0.83·cH₀); the clean 1/Z is referenced to cH_Λ, so any
> comparison to Milgrom (0.159) or Verlinde (0.167) — which use cH₀ — must use **0.143**, where the framework
> is the low outlier, not the bracketed middle. The √Ω_Λ = 0.83 gap is the why-now re-dressing, not new physics.

*Both-ways honesty held: this neither inflates the framework's agreement with Milgrom/Verlinde (it does not
bracket — it is the outlier) nor manufactures a deficit (the data cannot resolve the O(1) family either way).
Quarantine held: Z is stated as the framework's coefficient, never asserted as derived.*
