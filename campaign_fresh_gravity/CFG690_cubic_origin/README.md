# CFG690: does deep-regime scale invariance fix astra's cubic, and is that symmetry independent of the law?

**Label: CUBIC = R0-SHAPED, REDUCED (SI forces it uniquely, but SI is the deep law restated). γ = 0 INTERPOLATION ON SPARC:
FAIL by the frozen line (rms passes, Υ_disk below the band).**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (d87cde1d4), 2026-10-12. Block CFG690–699 (owner-approved for this
  chat).
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory
  closed"; nothing here says the data favour the framework. astra's sector is read only from `STABLE_SOURCED_RESPONSE.md`; no
  astra file is edited.
- **Script:** `cfg690.py`. Run `OMP_NUM_THREADS=1 nice -n 10 python3 cfg690.py`: one process, seconds, exit 0 →
  `cfg690.out`, `cfg690_results.json`. `CFG690_MUTATE=1` exits 1 as designed (M1, M2, M3 all bite) → `_MUTATE` outputs.
  Reads `CFG4_common` (A0, ν_mono, SPARC loader) and `CFG4_galaxy_law_results.json` read-only. Nothing downloaded.

## Results

| test | result |
|---|---|
| **T1** SI uniqueness (sympy) | ∫\|P\|ⁿ d³x scales as λ^(3−n): invariant iff **n = 3**. General W: λ³W(p/λ) = W(p) ⇒ W(p) = W(1)p³. Source term invariant. Quadratic term λ⁻¹ on-shell (Gauss fixes D), stiffness λ⁻¹: both irrelevant in the deep regime. On P = a∇φ the deep action is the AQUAL ∫\|∇φ\|³. **PASS** |
| **T2** SI vs the deep law (sympy) | (a) dlnV²/dlnr = (n−3)/(n−1), dlnV⁴/dlnM = 2/(n−1): flat and BTFR **iff n = 3**. (b) SI + {G, a₀} only as A₀ = Ga₀ ⇒ V = (A₀M)^{1/4}, unique, no r. (c) the deep law is SI-invariant; Newton is not. **PASS: SI ⇔ flat curves + BTFR** |
| **T3** raw SPARC, ν_SI(y) = 1 + y^{−1/2} (γ = 0) | canonical **0.1012 dex @ Υ 0.46**; alt **0.1007 @ Υ 0.42** (ν_mono 0.1003 @ 0.61 / 0.0991 @ 0.57; Newton 0.2755). rms ≤ 0.110 on both, but Υ_disk is below the frozen 0.50–0.80 band ⇒ **FAIL** |
| T3 control | CFG4's ν_mono and Newton reproduced to ≤ 1e-6 in rms, Υ exact, both footings: PASS |
| T3 post-hoc (no verdict weight) | ν_SI with Υ_disk held at 0.50: 0.1045 (canonical) / **0.1114 (alt, above 0.110)** |
| T4 (reported) | high-field residual Δg/g_N = y^{−1/2}: 1.3e-4 at 1 AU, 1.2–1.3e-3 at Saturn (both footings) |
| MUTATE | M1 W = \|P\|² not invariant; M2 wrong mass scaling breaks the source term; M3 ν = 1 gives 0.2755: all bite |

## Reading

1. **The cubic is not a free choice once deep-regime SI is assumed.** It is the unique potential compatible with it. The
   stiffness and quadratic terms are exactly the SI-breaking terms, which is why they set the onset length and the high-field
   side.
2. **But SI is not independent of the law.** SI together with "G and a₀ enter only as Ga₀" is equivalent to flat curves plus
   the BTFR. Nothing on the record derives SI from anything else. So R0 moves from "a form chosen to match" to **one postulate
   that is the deep law restated**. That is progress in bookkeeping (one symmetry instead of a tuned exponent), not an
   independent origin. R0 still does not pass.
3. **What would make R0 pass:** a derivation of deep-regime SI, or equivalently of G and a₀ appearing only as Ga₀, from the
   carrier's own degrees of freedom. A conformal sector that becomes scale-invariant at low acceleration, with a₀ as its single
   breaking scale, is the shape such a derivation would need. None is on the record.
4. **astra's γ = 0 interpolation fits the rms but asks for too little stellar mass.** ν = 1 + y^{−1/2} gives more boost at
   y ≈ 1 than ν_mono, so the fit lowers Υ_disk to 0.42–0.46. Held at the band edge, the alt footing exceeds 0.110. The quadratic
   coupling (astra's choice; SI does not fix it) sets this interpolation, so the C2 failure belongs to that coupling, not the
   cubic. Stiffness changes the interior below ℓ_γ and is not tested here.
5. **The γ = 0 form is also not Solar-System-silent.** Its residual √(a₀/g_N) is about 10⁻³ at Saturn, a power law and not
   exponential (S5). Stiffness would have to screen it. Whether ℓ_γ ∝ M^{−1/2} can screen the Sun while leaving galaxies
   unscreened is the open quantitative question for that sector.

## Disclosures (2026-10-12)

- **T1 scaling.** The criteria state that the quadratic term scales as λ⁻¹. That holds on-shell, where D = a∇φ − P is fixed by
  Gauss's law. Off-shell it scales as λ⁺¹ and acts as the constraint P = a∇φ in the deep regime. Both are printed. The uniqueness
  result uses the deep effective action on the constraint surface.
- **Post-hoc number.** The Υ = 0.50 post-hoc rms was added after the first run, to size the Υ-band failure. It has no verdict
  weight.
- **Warnings.** numpy prints RuntimeWarnings from the masked matmul. The controls reproduce CFG4 to ≤ 1e-6, so they do not
  affect the statistic.
