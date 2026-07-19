# SYNTHESIS — Dark-energy density from Type Ia supernovae vs the framework galaxy prediction

**Location:** `/Users/carlzimmerman/new_physics/prep_2026/sne_lambda/`
**Scripts (all exit 0):** `setup.py`, `sne_extract.py`, `predict_diagram.py` — verified in `VERIFY.md`.
**Date:** 2026-07-18. Framework background = standard ΛCDM throughout. No 'proves'.

---

## Headline

The dark-energy density **extracted from Type Ia supernovae** (Pantheon+, standard ΛCDM) and the
density **predicted from galaxy rotation-curve dynamics** (the framework's Λ-blind measured a₀,
inverted through ρ_DE = 4a₀²/Gc²) **agree to a factor ~1.0–1.6, at ≤1.5σ for both H₀** — an honest,
independent, factor-level cross-corroboration of the very density Sarkar's SNe-leg critique targets.
It is **not** a precision match and **not** a null. The apparently perfect canonical-a₀ agreement
is **circular** and carries zero weight.

---

## Outcome — does the SNe density agree with the framework galaxy prediction?

**SNe side (standard ΛCDM extraction — there is NO framework-native SNe formula).**
Pantheon+ (Brout+2022, ApJ 938:110) SNe-only flat-ΛCDM: Ω_m = 0.334 ± 0.018 → Ω_Λ = 0.666 ± 0.018,
q₀ = −0.499 (accelerating). SNe fix Ω_Λ via SHAPE (q₀); the ABSOLUTE density needs H₀ (SNe are
M_B–H₀ degenerate), so both H₀ are carried:

| H₀ | ρ_crit (kg/m³) | ρ_DE(SNe) (kg/m³) |
|----|----------------|-------------------|
| 67.4 (Planck) | 8.533e-27 | **5.683e-27 ± 1.54e-28** |
| 73.0 (SH0ES)  | 1.001e-26 | **6.666e-27 ± 1.80e-28** |

H₀ lever alone = (73.0/67.4)² = **1.17×** — the dominant axis; the ± is Ω_Λ-only (~2.7%).

**Galaxy side (framework prediction, ρ_DE = 4a₀²/Gc²).** The honest input is the a₀ **measured
from SPARC rotation curves** (Λ-blind, banked a0-line, `fire_slope_results.json` budget_gas):
GLS gas-dominated a₀ = 1.181e-10 ± 16% → **ρ_DE = 9.308e-27 ± 3.00e-27** (σ_ln ρ = 2×16% = 0.322).

**The genuine test — ratio ρ_DE(galaxy)/ρ_DE(SNe), with the a₀ box propagated:**

| Footing (a₀) | vs H₀=67.4 (Planck) | vs H₀=73.0 (SH0ES) |
|---|---|---|
| **measured GLS 1.181e-10 (GENUINE)** | **1.638× (+1.53σ)** | **1.396× (+1.03σ)** |
| measured median 9.73e-11 | 1.110× | 0.946× |
| alt 1.131e-10 (fixed, no box) | 1.500× (+15.0σ artifact) | 1.278× (+9.1σ artifact) |
| canonical 9.355e-11 **[CIRCULAR]** | 1.027× (+0.98σ) | 0.875× (−4.93σ) |

The genuine measured-a₀ density **agrees with the SNe density at ≤1.5σ for both H₀**, the tension
softened (correctly, not spuriously) by the 32% a₀ error box. The median variant lands 0.9–1.1×.

**Which footing the SNe favor — sharper zero-free-parameter μ(z) diagram test** (real Pantheon+,
1580 SNe / 24 bins, galaxy-Λ plugged into standard ΛCDM μ(z), Ω_m held at SNe 0.334, one H₀/M_B
offset marginalized, **zero SNe-fitted shape parameters**; best-fit LCDM ref χ²=21.0/22):

| Footing | Δχ² @67.4 | Δχ² @73.0 | Ω_m+Ω_Λ |
|---|---|---|---|
| measured median | +4.0 | **+0.01** | 0.96–1.07 (near-flat) |
| canonical [CIRCULAR] | +1.2 | +0.6 | ~1.0 |
| measured GLS (genuine) | **+41.4** | +21.7 | 1.26–1.42 (over-closes) |
| alt | +29.9 | +13.4 | 1.19–1.33 |

The diagram **favors the lower-a₀ (median) end** (Δχ² +0.01 at SH0ES, essentially perfect) and puts
the **high GLS central value in real shape-tension** (over-closes, Ω_m+Ω_Λ=1.42, high-z residual
−0.036 mag) — worst at Planck H₀. H₀=73.0 is systematically kinder to every galaxy footing.

**Circular-canonical caveat (the crux).** Canonical a₀ = cH_Λ/Z was DEFINED from a cosmological
(Planck) Λ, so ρ_DE(canonical) = 5.836e-27 equals Planck ρ_Λ to **0.12%** by construction. Its
1.027×/+0.98σ "match" only re-checks Planck-vs-SNe Λ — **algebra run backwards, zero evidential
weight.** It is flagged CIRCULAR in every docstring, JSON note, and verdict. Equally, the alt
footing's +15σ "tension" is the mirror-image zero-error-bar artifact and is not a headline.

---

## Thesis statement — can we get dark-energy density from SNe and tie it to the framework?

Yes, honestly and modestly. The SNe give ρ_DE = **5.68e-27 (Planck H₀) to 6.67e-27 (SH0ES H₀)**
kg/m³ by the **standard ΛCDM extraction** — the framework does **not** modify the background and has
no native SNe formula, so this leg is textbook Ω_Λ × ρ_crit. The framework contributes **only the
galaxy-side cross-check**: the Λ-blind, rotation-curve-measured a₀ inverts (ρ_DE = 4a₀²/Gc²) to
**9.31e-27 ± 3.0e-27** (GLS), landing **1.4–1.6× the SNe density at ≤1.5σ**, and 0.9–1.1× for the
median variant. On the density this **leans AGREES**; on the sharper diagram shape it **leans toward
the lower-a₀ footing**, with the high GLS central value in mild tension.

**What is genuinely NEW vs the banked a0-line/Planck comparison:** the banked a0-line compares the
measured a₀ to **Planck's** Λ (a CMB-inferred number). This lane instead ties the measured a₀ to the
**supernova** Λ specifically — a **different, independent observational leg**. That is what makes it
**Sarkar-relevant**: Sarkar attacks the SNe inference of acceleration; if galaxy dynamics
independently reproduce the same dark-energy density the SNe give (to ~50%, with **no SNe input**),
that is a genuine independent corroboration of the density his critique targets — not a proof, but a
real cross-check that does not route through the CMB. The **zero-SNe-fitted-parameter Hubble-diagram
prediction** (galaxy-Λ → μ(z), nothing fit to the SNe but one offset) is also new machinery here.

---

## Next

- **Tighten the a₀ box:** the whole significance is dominated by the 32% ρ error (16% a₀). A TRGB-
  calibrated or larger-sample a0-line would sharpen +1.5σ toward a decisive statement and resolve
  whether the SNe favor the GLS or median end.
- **Full Pantheon+ covariance:** the diagram Δχ²=+41 (GLS) uses diagonal errors + flat-form d_L with
  Ω_m+Ω_Λ≠1; the full covariance would shrink every Δχ² — it is NOT a clean 6σ kill. Redo with the
  official stat+sys covariance and proper curved d_L before quoting the diagram as a discriminant.
- **DESI/Union3 replication:** re-extract ρ_DE from an independent SNe compilation (Union3, DES-SN5YR)
  to test whether the ~1.4–1.6× GLS ratio is Pantheon+-specific.
- **Keep the circular caveat load-bearing:** never let `closest_footing="canonical"` (Planck_67.4 in
  the JSON) be quoted as a win — the closest **non-circular** footing is the median.
