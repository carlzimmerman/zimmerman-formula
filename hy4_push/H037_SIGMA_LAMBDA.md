# H037 — σ from Λ: a Kepler-grade dispersion law (form only)

Lane: `H037_sigma_lambda_relation.py` → `H037_results.out` / `H037_results.json`
Reading: **12 PASS / 1 FAIL**. Both a₀ footings. Measurement and threshold separate.

## The derivation

    G046 (temperature)   σ² = ½ √(G M_b a₀)
    H016 (seesaw)        a₀ = Λ²/(n M_Pl),  n = 2

Eliminate a₀ (natural units, G = 1/M_Pl²):

    σ⁴ = ¼ G M_b a₀ = M_b Λ² / (4 n M_Pl³)

    σ = (1/√2) (n M_Pl³)^(−1/4) · Λ^(1/2) · M_b^(1/4)

SI form (Λ an energy in J, M_Pl = √(ħc/G) a mass in kg; M_Pl eliminated):

    σ⁴ = G M_b Λ² / (4 n M_Pl c ħ)  =  (M_b Λ² / 4n) · (G/ħc)^{3/2}

    n = 2:   σ⁴ = (M_b Λ²/8)·(G/ħc)^{3/2}        σ⁴/M_b = G Λ²/(8 M_Pl c ħ)

Equivalently, since Λ⁴ = ρ_Λ: **σ⁸ ∝ ρ_Λ** at fixed M_b — the eighth power of
the halo dispersion tracks the dark-energy density.

## Numbers (zero free parameters)

| quantity | canonical (a₀ = 9.3619e-11) | alternative (a₀ = 1.1279e-10) |
|---|---|---|
| implied Λ | 2.2403 meV | 2.4590 meV |
| K = σ⁴/M_b | 1.5621e-21 (m/s)⁴/kg | 1.8820e-21 (m/s)⁴/kg |
| M_b/σ⁴ | 321.9 M⊙(km/s)^−4 | 267.2 M⊙(km/s)^−4 |
| σ(1e10 M⊙) | 74.65 km/s | 78.21 km/s |
| σ(6e10 M⊙) | 116.84 km/s | 122.41 km/s |
| σ(1e11 M⊙) | 132.76 km/s | 139.09 km/s |

M_b/σ⁴ = 4/(G a₀) = 4A with A = 80.46 the registered BTFR zero point
(measured 321.94 vs 321.84, ratio 1.000302). σ/v_c = 0.707107 at every mass.

## Exponents

* **d ln σ / d ln Λ = 1/2** (exact, sympy and numeric). σ ∝ √Λ at fixed M_b.
* **d ln σ / d ln M_b = 1/4** — matches the canonical Faber–Jackson slope
  ⟨log σ | log L⟩ ≈ 1/4 (observed range 0.176 Cannarozzo+2020 SDSS → ~0.30
  for massive quiescents).
* d ln σ / d ln n = −1/4, d ln σ / d ln M_Pl = −3/4.

## Sensitivity to Λ (σ₀ = 132.76 km/s at M_b = 1e11 M⊙)

| ΔΛ/Λ | Δσ/σ | Δσ |
|---|---|---|
| +1% | +0.50% | +0.66 km/s |
| +10% | +4.88% | +6.48 km/s |
| +25% | +11.8% | +15.7 km/s |
| +100% | +41.4% | +55.0 km/s |

Real, measured Λ spread: Planck H₀ = 67.4 vs SH0ES H₀ = 73.04 → Λ differs by
4.10% → σ differs by **2.03%** (2.0 km/s at 100 km/s). The whole 22% a₀
tension (P11) damps to **4.77%** in σ. Both are below the 0.075 dex (18.9%)
intrinsic scatter of the observed M–σ relation. **Not discriminating.**

## Faber–Jackson

* Exponent: consistent (0.25 predicted vs ≈0.25 observed).
* Zero point: **FAILS**. Predicted σ(1e11 M⊙) = 132.8 km/s vs observed
  σ_e ≈ 170 km/s (Cannarozzo+2020, SDSS ETGs) — κ = σ_e/σ_halo = 1.281. That
  deficit is 28% in σ, i.e. it would need a₀ 2.7× larger, far outside P11's
  22%. So G046's σ is the *halo* dispersion, not the aperture stellar σ_e; κ
  is not derived and is not a constant of the framework. The FJ comparison
  tests the exponent only — never the zero point.

## Verdict: new in form, circular in content, not independently testable

1. **Circular.** a₀ = Λ²/(2 M_Pl) *is* the postulate: H029 showed
   [Λ²/(2 M_Pl)]/a₀ = 1 identically, and here ρ_Λ = 4Λ⁴/n² = Λ⁴ for n = 2
   (numerically 0.999898). Substituting it into G046 renames a₀; every number
   this relation predicts, P5 + P6 already predicted. Per H029 it is a
   unification (one fewer symbol), not a finding.
2. **Not testable as stated.** Λ is measured, not a knob — "σ ∝ √Λ" cannot be
   dialled. The only live content is the zero point, which is P6/4.
3. **Quarter-power damping cuts both ways.** σ ∝ a₀^{1/4} makes the relation
   look precise but also makes a 22% a₀ error only a 4.8% σ error — under the
   19% scatter. The sensitivity that would falsify it is diluted below the
   noise of the observable.

### What would make it worth something
1. Derive κ = σ_e/σ_halo ≈ 1.28 from the action.
2. Measure σ⁴/M_b with systematics below ~5% (currently ~19%).
3. Find a sector where Λ enters without a₀ being independently measurable —
   i.e. where the elimination is not invertible. Halo dispersion is not such a
   sector: a₀ is measured far better than σ is.
