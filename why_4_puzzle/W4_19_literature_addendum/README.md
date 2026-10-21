# W4-19: published a₀–Λ relations missing from the register

**Verdict: NOTHING NEW.** None of the six published relations without a register row gives κ = ½; each is π-odd,
Ω-dependent or carries a free factor. **κ = ½ stays FITTED.** Not theory closed.

A read-only literature sweep looked only at works outside the 32π chat's lane E table (about 35 papers). It found twelve:
- Six already have rows: Blanchet–Le Tiec K290, BIMOND K026/K076/K493, Berezhiani–Khoury K643, Kanatchikov K175/K216,
  Urueña Palomo K012/K105, Escala K012.
- The six below had none. Their formulas were re-checked against the arXiv PDF text, except Navarro–Van Acoleyen (from a
  summary).

| id | work | reading (frozen, 2f0d6413c) | κ | π in κ² | in window | class |
|---|---|---|---|---|---|---|
| L1 | Zhao 2008 | ρ_Λc² = a₀²/8πG as an equality (the paper says ∼) | √(8π) = 5.013 | odd | no | any |
| L2 | Maeder 2023 (scale-invariant vacuum) | a₀ = ((1−Ω_m)²/4) n cH₀, n = 1 | Ω_Λ^{3/2}√(π/6) = 0.410 | odd | yes | free (Ω-dependent; a₀ evolves) |
| L3 | van Putten 2017 | a₀ = √(1−q)H/2π: (a) Λ = ω₀²; (b) ΛCDM q₀ | 0.798; 0.688 | odd | no | menu |
| L4 | Luo 2026 | a₀ = 2β²c²√(Λ/12), β² ∼ ⅓ | √(8π/27) = 0.965 | odd | no | odd |
| L5 | Navarro & Van Acoleyen 2006 | a₀ = cμ, μ set by f(R,P,Q) | — | — | — | free |
| L6 | Funkhouser 2006 | a₀ ∼ cH_Λ (factor b free) | √(8π/3) = 2.894 | odd | no | free |

## What this says

- **Zhao's field-energy reading is the cleanest density form in the literature, and it misses by exactly 32π.**
  ρ_Λc² = a₀²/8πG, while the framework has ρ_Λc² = 4a₀²/G. The why-4 puzzle is precisely that factor.
- **Maeder's 0.410 is the only entry inside the window.** It is not a constant κ: it moves with Ω_Λ (MUTATE) and so
  predicts an a₀ that changes over time.
- **No 2023–2026 paper derives ½.** This agrees with lane E.

## Checks

- **K1** reproduces the sweep's numbers. **K2** confirms the 32π miss.
- **MUTATE** (Ω_Λ → 0.70) moves L2 and L3b and leaves the pure numbers fixed (exit 1 by design).

`FROZEN_CRITERIA.md`, `w4_19.py`, `w4_19.out`, `w4_19_MUTATE.out`, `w4_19_results*.json`. Run from the repo root:
`python3 why_4_puzzle/W4_19_literature_addendum/w4_19.py`.
