# L93 — Linear growth and σ₈: making the F(Q)Θ Noether dust's "clusters like CDM" claim quantitative

**Script:** `L93_linear_growth_sigma8.py` · **Output:** `L93_linear_growth_sigma8.out` · **Result:** 19/19 checks PASS
(each PASS = the stated claim is TRUE). Self-contained numpy/scipy/sympy; imports NOTHING from
`qwen_claude_field_theory/` (astra's c_s²=0, G_eff=G, and the cubic MOND operator are reproduced independently).
Controls first. Both a₀ footings noted — a₀ is **absent** from linear cosmology, so both give bit-identical numbers.

## Verdict — one line

**At linear SUB-HORIZON order the F(Q)Θ Noether dust clusters EXACTLY like CDM: D(z) is identical to ΛCDM to
machine precision, and σ₈ = σ₈(ΛCDM) = 0.811 scale-independently — so the g04h growth-suppression deficit
(σ₈ ≤ 0.65) is quantitatively ABSENT.** The model inherits ΛCDM's mild S₈ lensing tension exactly (S₈ = 0.831,
−0.07σ from Planck, +1.0σ from KiDS-Legacy), no better and no worse. The full CMB/pre-recombination transfer,
the near-horizon k→0 health (L83), and the fine-tuned dust abundance (L84/L86/L87) are separate, open,
separately-tracked costs — not a growth deficit.

## Why the claim is exact, not approximate

L82 established two facts I reproduce as controls (C0, C1):

1. **The MOND operator is CUBIC in the perturbation.** On the homogeneous FLRW background the spatial gradient
   V=0, so `y=|V|/a₀ = O(δφ)` and the primitive `G(y)=y²+2(1+y)e^{−y}−2 ~ (2/3)y³`. A cubic operator
   contributes **no** quadratic `(∇δφ)²` term (⇒ no spatial-gradient/pressure) **and** drops from the linear
   gravitational equations (⇒ the Poisson coupling is standard Einstein `G_eff = 1/(8πM²) = G`, not the
   nonlinear MOND response).
2. **The quadratic scalar action is pressureless.** Time-kinetic `K_QQ = 3f²/2M² > 0`, spatial-gradient
   coefficient `= 0` ⟹ `c_s² = 0` **exactly** at the cosmological background.

Together these mean the dust's linear growth equation IS, character-for-character, the CDM growth equation:

```
δ'' + 2H δ' − 4πG ρ_m δ = 0        (G_eff = G ; no k²c_s² Jeans term because c_s² = 0)
```

So "clusters like CDM at linear sub-horizon order" is not an approximation to be checked numerically — it is an
**identity of the growth operator**. The numerical content of this lane is (i) validating the solver on ΛCDM,
(ii) confirming the identity holds to machine precision, and (iii) proving the pipeline can still detect a
deficit when one is physically present (so the "match" is not an artefact).

## The Jeans scale — the quantitative statement (Part 1)

Jeans balance `c_s²(k/a)² = 4πGρ_m` gives comoving `k_J(a) = √(1.5 Ω_m0/a)·H₀/c_s`.

| sector | k_J(a=1) | consequence |
|---|---|---|
| **Noether dust, c_s²=0** | **∞** (λ_J → 0) | **no** comoving scale is Jeans-suppressed — all modes grow |
| representative c_s = 200 km/s | 0.34 h/Mpc | k_J lands **in the observable/σ₈ band** — modes k>k_J suppressed (the g04h locus) |

c_s²=0 pushes the Jeans scale to infinity, removing the g04h suppression mechanism entirely.

## Linear growth D(z) — matter+Λ, recombination → today (Part 2)

Solving the growth ODE (Ω_m=0.315, Ω_Λ=0.685) from z=1090 to z=0:

| z | D(z) (D(0)=1) | f = dlnD/dlna | Ω_m(z) |
|---|---|---|---|
| 0.0 | 1.00000 | 0.5271 | 0.3150 |
| 0.5 | 0.76892 | 0.7610 | 0.6082 |
| 1.0 | 0.60675 | 0.8767 | 0.7863 |
| 2.0 | 0.41714 | 0.9586 | 0.9255 |
| 5.0 | 0.21117 | 0.9946 | 0.9900 |

- **Solver validated (C2):** reproduces the analytic ΛCDM growing-mode integral
  `D(a) = (5Ω_m/2) E(a) ∫₀^a da'/(a'E(a'))³` to `max|D_ODE/D_analytic − 1| = 7.8×10⁻⁹`.
- **Growth index (C3):** γ(0) = 0.554, the ΛCDM GR value ~0.55.
- **The identity (P2):** `max|D_model − D_ΛCDM| = 0` (bit-identical — the same equation).

**Precision answer:** D(z) matches ΛCDM to **machine precision (exactly 0)** because it is the identical
growth equation; the solver itself is trustworthy to ~10⁻⁸ (validated against the closed-form ΛCDM growth).

## σ₈ and the confrontation (Part 4)

Because `c_s²=0` (no k-dependent Jeans suppression) and `G_eff=G` (same growth at every scale),

```
σ₈(model) / σ₈(ΛCDM) = D_model(0) / D_ΛCDM(0) = 1   EXACTLY and scale-independently.
```

This ratio is **1 for any transfer function and any primordial amplitude** — it does not depend on the σ₈
normalisation. With the Eisenstein–Hu transfer + top-hat machinery normalised so ΛCDM gives σ₈=0.811
(control C4, kernel peaks at k_eff = 0.157 h/Mpc — deep sub-horizon, C4b):

| quantity | model | observed | tension |
|---|---|---|---|
| σ₈ | **0.811** (= ΛCDM) | ~0.81 | — |
| S₈ = σ₈√(Ω_m/0.3) | **0.831** | 0.832 ± 0.013 (Planck) | **−0.07σ** |
| S₈ | 0.831 | 0.815 ± 0.016 (KiDS-Legacy) | **+1.0σ** |

The model **is** the ΛCDM value: it neither manufactures a deficit nor an improvement. It inherits ΛCDM's
mild S₈ lensing tension exactly.

## Adversarial control — the pipeline is NOT rigged to say "match" (Part 3 / P4b)

The same growth+σ₈ pipeline, fed a c_s²>0 sector (the g04h mechanism), **must** produce a real deficit.
Growth amplitude `|S(k)| = |D(k)/D_pressureless|` at z=0 (power ~ |S|²):

| k [h/Mpc] | c_s²=0 (MODEL) | c_s=150 km/s | c_s=300 km/s | c_s²∝ρ_d (a⁻³, capped) |
|---|---|---|---|---|
| 0.05 | 1.000000 | 0.996 | 0.983 | 0.003 |
| 0.10 | 1.000000 | 0.983 | 0.935 | 0.001 |
| 0.20 | 1.000000 | 0.935 | 0.760 | 0.0004 |
| 0.50 | 1.000000 | 0.645 | 0.107 | 0.0003 |
| 1.00 | 1.000000 | 0.107 | 0.009 | 0.0003 |

Resulting σ₈: **c_s=150 → 0.740, c_s=300 → 0.604, g04h-like c_s²∝ρ_d → 0.186** (the σ₈ ≤ 0.65 g04h ballpark),
against the model's **0.811**. So the pipeline detects a genuine deficit whenever c_s²>0; the "match" is
**specific to c_s²=0** and is not an artefact of the machinery. This is the "verify the match as hard as the
deficit" discipline: the deficit is reproduced (the mechanism is real), and the model avoids it.

## Honest caveats — clean sub-horizon vs. open elsewhere

1. **Full CMB / pre-recombination transfer T(k) is NOT derived here (P5b).** CDM-like clustering is established
   at linear **sub-horizon** scales (c_s²=0, G_eff=G, no Jeans cutoff, no free-streaming). Whether the dust
   yields the *same acoustic-scale transfer* as CDM through horizon crossing and the radiation era needs a
   Boltzmann integration — astra's open task. This lane does not claim it.
2. **Near-horizon k→0 strong coupling (L83) (P5c).** astra's symplectic-form collapse bears on the CMB's
   **lowest multipoles**, not on σ₈, whose kernel peaks at k_eff = 0.157 h/Mpc — deep sub-horizon, ~450×
   above the collapse scale. Separate concern.
3. **Abundance is fine-tuned (P5d).** Ω_c ≈ 0.264 is an input, set by the |C|/|A| ~ 10⁻²⁴ charge tuning
   (L84/L86/L87), not predicted. This lane addresses **growth and amplitude-shape given the amount**, not the
   abundance tuning.
4. **a₀ (P6).** a₀ (canonical 9.3619×10⁻¹¹ / alternate 1.1279×10⁻¹⁰ m/s²) appears in **no** linear-cosmology
   equation — background E(a), growth ODE, Jeans term, transfer, σ₈. It enters only the galaxy MOND term
   (cubic, dropped). Both footings give bit-identical D(0) and σ₈ (demonstrated, not assumed).

## Confidence

- **HIGH** that D(z) and σ₈ are identical to ΛCDM at linear sub-horizon order — it is the same growth
  equation (an exact identity from c_s²=0 + G_eff=G), and the solver is validated on the closed-form ΛCDM
  growth to 10⁻⁸.
- **HIGH** that the g04h deficit is absent at this order and that σ₈ ≈ 0.81 is consistent with observations to
  the same degree as ΛCDM (the pipeline reproduces the deficit for c_s²>0, so the null is meaningful).
- **MEDIUM/OPEN** on the *complete* structure verdict: the full CMB transfer and the near-horizon/low-ℓ health
  are separate, unresolved, and belong to astra's Boltzmann/ADM calculations — not addressed here.

## For the handoff ledger

> **A93.** The F(Q)Θ Noether dust's linear growth is quantitatively CDM's: because the MOND operator is cubic
> (c_s²=0, G_eff=G — L82, reproduced C0/C1), the growth equation is character-for-character ΛCDM's, so
> D(z) is bit-identical to ΛCDM (P2; solver validated to 7.8×10⁻⁹ against the analytic growing mode, C2;
> γ(0)=0.554, C3) and σ₈(model)=σ₈(ΛCDM)=0.811 scale-independently (P4a) ⟹ S₈=0.831, −0.07σ Planck / +1.0σ
> KiDS-Legacy (P4c). The g04h deficit (σ₈≤0.65) is ABSENT because c_s²=0 sends k_J→∞ (P1). Adversarial
> control: the SAME pipeline fed a c_s²>0 sector reproduces a real deficit (σ₈→0.74/0.60/0.19 for
> c_s=150/300/g04h-like, P3b/P4b), so the match is specific to c_s²=0, not rigged. Open (separate): full CMB
> transfer (P5b), near-horizon k→0 / low-ℓ (L83, P5c), fine-tuned abundance (L84/L87, P5d). a₀-independent
> (P6). `L93_linear_growth_sigma8.py`, 19/19 PASS, all controls PASS.
