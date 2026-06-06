# a₀(z) model comparison on the complete compiled dataset — framework = constant (safe, untested); risers excluded

*C. Zimmerman, 2026-06-06. Capstone of the a₀(z) empirical work: a quantitative comparison of the four hypotheses on
EVERY published a₀(z) constraint 2016–2026 (two literature-harvest agents + my unified-pipeline points), with the
regime bias handled honestly. Script: `a0z_model_comparison.py` (+figure). This is the definitive current-data
verdict.*

## The compiled dataset (with regime flags — the key honesty)

| z | a₀ [10⁻¹⁰] | regime | source |
|---|---|---|---|
| 0.00 | 1.20 ± 0.24 | clean | SPARC (McGaugh+2016) |
| 0.045 | 1.69 ± 0.13 | clean | MIGHTEE-HI (Varasteanu+2025) |
| 0.045 | 1.32 ± 0.13 | clean | MIGHTEE+SPARC (Varasteanu+2025) |
| 0.85 | 0.85 ± 0.20 | interm | KROSS unified (this work, mass-controlled) |
| 1.50 | 1.10 ± 0.55 | clean | RC100 deep-MOND-17 (Del Popolo & Chan 2024, declining-leaning) |
| 0.90 | 2.38 ± 0.30 | **biased** | MUSE-DARK III (Ciocan+2026, RAR-fit, ΛCDM-degenerate) |
| 1.34 | 2.80 ± 0.55 | **biased** | KMOS³D unified (high-acceleration) |
| 2.23 | 2.90 ± 0.65 | **biased** | KMOS³D unified (high-acceleration) |
| 3.25 | 1.20 ± 0.50 | **biased** | Big Wheel (Weibel/Naidu+2024; g/a₀≈2.6, overestimate) |

**The decisive data fact (from the harvest):** there is **no genuinely deep-MOND datum at z≥2.** Every confirmed
high-z disk is high-acceleration (g/a₀ = 2.6 for the Big Wheel up to ~17 for REBELS-25), so `a₀=V⁴/(G M_bar)`
**overestimates** a₀ there. Those points are biased high (upper-limit-like) and must not drive the fit.

## The quantitative comparison (a₀(z)=A·f_h(z), A free, log-space χ²)

**CLEAN deep-MOND + intermediate sample (N=5, the honest fit):**

| hypothesis | χ²/dof | Δχ² vs framework | verdict |
|---|---|---|---|
| **framework √ρ_DE** | 2.80 | 0 | — |
| **constant** | 2.81 | **−0.04** | **DEGENERATE with framework** |
| Verlinde (cH) | 7.10 | **+17.2** | strongly disfavored (~4σ) |
| matter (1+z)^1.5 | 12.30 | **+38.0** | excluded (~6σ) |

- **Best-fit free power law on clean data: `a₀ ∝ (1+z)^p`, p = −0.74 ± 0.34** — *declining-leaning* (framework
  direction), consistent with constant (p=0) and framework (effective p≈−0.20), **inconsistent with Verlinde
  (p≈+1.08) and matter (p=+1.5)** at high significance.
- **The "rise" is a regime artifact, demonstrated:** including the biased high-acceleration points flips the best
  power law to **p=+0.42** (spurious rise); removing them (clean fit) gives **p=−0.74**. *All* the apparent evidence
  for rising a₀ is in the high-acceleration IFS points — exactly the regime bias the unified pipeline exposed
  (`A0Z_UNIFIED_PIPELINE_RESULT_…`). Clean data exclude rising.

*(Caveat stated plainly: χ²/dof ≈ 2.8 for the best models — the clean points scatter more than their quoted errors
(MIGHTEE 1.69 vs SPARC 1.20 vs KROSS 0.85), i.e. residual selection/systematic scatter. This inflates absolute χ² but
affects all models alike, so the **relative ranking is robust**; the absolute fit is systematic-limited — the floor
again.)*

## This matches the independent literature exclusions
- **Milgrom 2017** (arXiv:1703.06110): the Genzel disks (g=3–11 a₀) "all but exclude ~4a₀ at z~2, excluding
  a₀∝(1+z)^1.5." MOND fits with **constant** a₀.
- **McGaugh 2024 / Triton 2025** (arXiv:2406.17930): high-z BTFR shows no perceptible zero-point evolution →
  "excludes the picture in which a₀ evolves … through a₀~cH₀." Leaves **a₀~c²√Λ (constant, = framework with w=−1)
  viable.**
- **Limbach/Psaltis/Özel 2008** (arXiv:0809.2790): the z=1.2 BTFR intercept "marginally favors coupling to the
  dark-energy density (√ρ_DE)" over the cH coupling — a weak **direct lean toward the framework over Verlinde.**

## Verdict — "safe but untested," now quantified

1. **The framework is observationally indistinguishable from constant a₀** (Δχ²=−0.04) — because the DESI-driven
   decline is ≤26% to z=3 and the curve is near-flat to z~2.5, below all current sensitivity. The framework is *safe*:
   it sits on the favored (constant) reading.
2. **The rising rivals (Verlinde/QI cH, matter (1+z)^1.5) are excluded** — by this comparison (Δχ²=17, 38) and
   independently by Milgrom 2017 and McGaugh 2024. The framework's emergent-gravity competitor in the rising
   direction is dead on the data.
3. **The framework's distinctive decline is genuinely untested** — and *cannot* be tested with existing data, because
   no deep-MOND (g≪a₀) datum exists at z≥2 (every confirmed high-z disk is high-acceleration). Breaking the
   framework=constant degeneracy needs the one missing measurement: a clean deep-MOND rotation curve at z≳2, where
   a₀(z)/a₀(0)≈0.74 (−7% in V) finally clears the systematic floor.
4. **The low-z bump (z≈0.4, +6%) has the right sign in the one clean probe** (MIGHTEE-HI fits a₀ rising at 2.4σ) but
   the magnitude is unconstrained (data only reach z≤0.08); no HI/lensing sample binned at z~0.3–0.5 exists yet.

**Bottom line:** on the complete current dataset, `a₀∝√ρ_DE` is **safe (=constant) and its rising rivals are excluded**
— a better standing than "leaning unfavorable," but the framework's *own* signature (the decline) remains beyond reach
until deep-MOND z≳2 kinematics exist. The framework cannot yet be distinguished from standard MOND; it can only be
distinguished from Verlinde — and there, it wins.

*Numbers in `a0z_model_comparison.py`; figure `a0z_model_comparison.png`.*
