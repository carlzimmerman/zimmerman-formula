# Ciocan / MUSE-DARK III a₀(z) vs the framework — a REAL ~15σ tension (softens to ~3–5σ only via a shared systematic). Corrects a prior over-favorable read.

*Workflow `wz7kw0yam` (4 agents), banked 2026-06-20. Puts a real σ-number on the framework's STRONGEST
live challenge. Both-ways — and the honest result goes AGAINST the framework, reported at full weight.
Quarantine: a0(0)=9.36e-11 is an INPUT, so the amplitude-marginalized SHAPE test is the fair one.
Verified verbatim against A&A aa59230-26 (arXiv:2604.22613).*

## Verdict: REAL-TENSION-SLOPE-SURVIVES. This is the strongest live pressure on the framework's
## distinctive content — materially stronger than the prior "non-diagnostic ~2σ" headline.

Ciocan et al. (MUSE-DARK III, 79 SF galaxies, 0.33<z<1.44) measure a₀ **RISING**: a₀(0)=1.00±0.04,
slope a₁=1.59₋₀.₁₀⁺⁰·¹¹ (×10⁻¹⁰/z), a₀(z~1)=2.38±0.1, trend "at ~30σ." The framework's declining
√ρ_DE branch goes the **WRONG SIGN**.

## ⚠️ LOAD-BEARING CORRECTION — against the framework (the prior banked softening rested on a wrong premise)
The prior banked read called this "non-diagnostic ~2σ," leaning on *"Ciocan's absolute a₀ sits ~2×
above 1.2e-10 even at low-z = an M/L offset,"* so offset-marginalization would rescue the shape.
**That premise is FALSE.** The paper's intercept is **a₀(0)=1.00** — *below* canonical 1.2, with the
framework's 0.936 only ~1.6σ from it (fine at z=0). **There is NO 2× low-z offset.** The factor-2 at
z~1 is produced by the **SLOPE**, not a normalization. So offset-marginalization removes a non-existent
offset and does **not** rescue the framework. The "~2σ" was an artifact of binning 79 galaxies into 4
coarse points with per-bin errors ~3.5× too large (information loss, not principled marginalization).

## The honest σ, layered (framework flat/declining branch)
| treatment | declining | flat | rising-cH |
|---|---|---|---|
| (a) RAW, fixed a₀(0)=0.936 | 13.7σ | 14.0σ | 8.8σ |
| **(b) FAIR shape/slope (amplitude marginalized, paper's own stat err)** | **17.2σ (wrong sign)** | **15.1σ** | **2.2σ (not excluded)** |
| (b') prior's "norm-marg" on 4 coarse bins | 2.5σ | 1.9σ | 0.25σ |
| (c) + shared ΛCDM-assembly drift systematic (30–50% of a₁) | **~3–5σ** | ~3–4σ | ~0.4σ |
| (c') fully over-marginalized (2 free params on 4 pts) | ~0σ | ~0σ | ~0σ |

**For a flat line, amplitude-marginalization IS the slope test** — there is no offset escape. The fair
test (b) is ~15σ (flat) / ~17σ (declining, *worst of the three, wrong sign*). It does **NOT** collapse
under offset-marginalization.

## What legitimately softens it (genuinely shared, NOT special pleading) — the ~3–5σ floor
1. **Shared ΛCDM-assembly drift.** ΛCDM with NO fundamental a₀ *also* yields an apparent rising a₀
   (Magneticum, Mayer+2023, MNRAS 518:257 — ×3 to z=2.3 = +0.80/z ≈ **~50% of MUSE's +1.59/z**). Folded
   as a 30–50% systematic on a₁ → residual ~3–5σ. This is a real shared systematic, not framework-only.
2. **MUSE is STEEPER than EVERY forward-model.** Ciocan herself: "the measured a₀(z) is faster than
   H(z)." Even the rising-cH rival (a₁~1.36) **undershoots** the data by 2.2σ, and Magneticum supplies
   only ~50%. So +1.59/z is not cleanly a *fundamental* a₀(z) for **anyone** — a fitted a₀ ≠ a
   fundamental a₀.

The (c') ~0σ is **over-fitting** (the Magneticum coefficient floats unconstrained on 4 points) — not
physical, do NOT cite it.

## Impact on Front C — two legs, split
- **Cosmology leg (DESI evolving-DE → √ρ_DE bump): UNTOUCHED by MUSE, stays alive-favored at 3.1–4.2σ**
  (a consistency cross-check on ρ_DE as input).
- **Direct-datum leg (MUSE): a GENUINE ~15σ statistical tension** with the framework flat/declining
  shape, held off the kill-line **only** by the shared-ΛCDM-assembly systematic (residual ~3–5σ). NOT
  referee-proof, but **materially stronger pressure than the prior headline**, and the framework's
  declining branch is the **worst** of the three.
- **w→−1 does NOT help:** it flattens the branch to exactly FLAT = the full ~15σ case. DESI DR3 settles
  the cosmology leg but NOT the MUSE confrontation.

## What would settle it
1. **Near-term:** re-derive a₀(z) on ONE homogeneous IFS sample (KROSS+KMOS3D+KGES+MUSE) through a
   common pressure-support/decomposition pipeline that **forward-models out the Magneticum ΛCDM
   apparent-a₀ drift** (needs ≤2% velocity precision) — separates a fundamental a₀(z) from the
   assembly-driven apparent rise.
2. **z≥2 deep-MOND BTFR SIGN** (ELT/HARMONI + JWST, early-mid 2030s): framework discs ~6–10% BELOW the
   local BTFR; rising rival ABOVE (opposite sign) — the cleanest framework OUTPUT discriminator
   (conditional on large |wₐ|).

## Honest net (both ways)
A **real ~15σ statistical slope-tension** with the framework's distinctive a₀(z) shape — the declining
branch is the worst-fitting of the three (wrong sign). It is **NOT a referee-proof kill**: a genuinely-
shared ΛCDM-assembly systematic supplies ~50% of the slope and MUSE is too steep for any model, leaving
a ~3–5σ residual. But it is the **strongest live pressure on the framework**, and this banking
**corrects the prior over-favorable "non-diagnostic ~2σ" read** (which rested on a non-existent 2× M/L
offset). The cosmology leg stays alive-favored; the direct-datum leg is a real, sub-kill tension.

### Scripts (exit 0, under opus_48_extended_research/reviews/a0z_ciocan/)
ciocan_a0z_FINAL_RECONCILE.py · ciocan_a0z_chi2.py · ciocan_a0z_SKEPTIC_AUDIT.py
### Source: Ciocan et al. MUSE-DARK III, A&A 709 L16 (arXiv:2604.22613); Mayer+2023 (Magneticum, MNRAS 518:257)
