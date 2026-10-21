# W4-19: published a₀–Λ relations missing from the register (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-19 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
Literature lane. **κ = ½ is FITTED.** Not theory closed.

## Source

A read-only literature sweep (this session's background agent) looked only for works that the 32π chat's lane E audit
table (`sonnet55_push/puzzle_32pi/agents/E_literature_a0_coefficient/README.md`) did not open.
- It found twelve. Six already have register rows: Blanchet–Le Tiec K290, BIMOND K026/K076/K493,
  Berezhiani–Khoury K643, Kanatchikov K175/K216, Urueña Palomo K012/K105, Escala K012.
- Six have none. They are registered here.
- I re-checked each formula below against the arXiv PDF text, except **N–VA**, which is from a summary only and is marked
  partial. The PDFs stay outside the repo.

| id | work | formula as written | H |
|---|---|---|---|
| L1 | Zhao 2008, arXiv:0802.1775 | DE/DM switch "when energy density falls below a₀²/8πG ∼ 10⁻¹⁰ erg/cm³" (order statement) | — |
| L2 | Maeder 2023, arXiv:2302.06206 (MNRAS 520, 1447), eq. 80 | a₀ = ((1−Ω_m)²/2)(4π/3)Gρ_c r_H0 = ((1−Ω_m)²/4) n cH₀, with n ≃ 1 for Ω_m 0.2–0.3 | H₀ |
| L3 | van Putten 2017, arXiv:1707.01619, eqs. 5, 6 and 9 | ω₀ = √(1−q) H, Λ = ω₀², a₀ = ω₀/2π | H, q |
| L4 | Luo 2026, arXiv:2602.14515, eq. 14 and §virial | a_bg ≡ √(Λ/12); a₀ ≈ 2β² a_bg, β² = cos²α ∼ ⅓ | H_Λ |
| L5 | Navarro & Van Acoleyen 2006, arXiv:gr-qc/0512109 (partial) | a₀ = cμ; 6H₀² = μ²⟨…⟩ depends on the f(R, P, Q) chosen | H₀ |
| L6 | Funkhouser 2006, arXiv:physics/0502049, eq. 16 | a₀ ∼ cΛ^{1/2}, ε_vac = 3Λc²/8πG (his Λ is H_Λ²); factor b left free | H_Λ |

## Method (fixed)

- **κ = a₀/(c√(Gρ_Λ))** with ρ_Λ = Ω_Λ·3H₀²/(8πG), Ω_Λ = 0.685, and Λ = 8πGρ_Λ/c² where the paper writes Λ. Computed
  exactly in sympy.
- **Readings, declared now:**
  - L1 is read as an equality (ρ_Λc² = a₀²/8πG).
  - L2 at n = 1 and Ω_m = 1 − Ω_Λ; its Ω dependence is reported.
  - L3 has two readings, both reported: (a) Λ = ω₀² with Λ = 8πGρ_Λ/c² (de Sitter), and (b) ΛCDM q₀ = Ω_m/2 − Ω_Λ with H = H₀.
  - L4 at β² = ⅓.
  - L5 is FREE.
  - L6 is read as a₀ = cH_Λ, an order statement.
- **Class per CFG894:** odd / any / menu / free.
  - A route through H or Λ alone is `odd`.
  - A density route is `any`.
  - Two declared readings form a `menu`.
  - A free factor, an Ω-dependent (non-constant) κ or an order-only statement is `free`.
- **Report:** the π content of κ² for each entry, and whether κ lies in W_data [0.227, 0.607].

## Checks

- **K1:** sympy reproduces the sweep's numbers to 1e-3: L1 5.013, L2 0.410, L3 0.798 and 0.688, L4 0.965, L6 2.894.
- **K2:** the framework identity, L1's field-energy reading, misses 4a₀²/G by exactly 32π.
- **MUTATE (`W4_19_MUTATE=1`):** Ω_Λ → 0.70. The Ω-dependent entries (L2, L3b) must move; the pure-number entries (L1, L3a,
  L4, L6) must not.

## Verdict (frozen)

- **A PUBLISHED ROUTE GIVES ½:** some entry gives κ = ½ exactly with a mechanism and no free factor.
- **Otherwise, NOTHING NEW:** register the rows.

**Hand expectation:** NOTHING NEW. Every entry is π-odd, Ω-dependent or free; L2 (0.410) is the closest inside the
window and is not a constant κ.
