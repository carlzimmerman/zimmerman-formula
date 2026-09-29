# CFG114 — does the SLUGGS deficit survive GC slopes and orbits varied together?

- **Criteria:** frozen in `CFG114_FROZEN_CRITERIA.md` (c5b32b499), before any number.
- **Script:** `CFG114_sluggs_slope_orbit_box.py`, about 15 s, both footings.
- **Runs:**
  - The main run passes 5 of 6 and exits 1. The one failure is the headline H1, and that failure is the answer.
  - The MUTATE run (the deficit removed at the law's weakest cell) also fails H1 and exits 1.
  - As the frozen file said in advance, the control is therefore uninformative for H1. C1 passes in both runs.

## Bottom line

**The law's SLUGGS deficit does not survive both degeneracies at once, at the edges of the declared ranges.**

- **The box:** every published GC slope shifted by −0.4 to +0.4 (CFG111's brackets) × a constant GC anisotropy from −0.5 to +0.5 (CFG113's bracket).
- **Most of the box keeps the deficit.** It exceeds 2σ in **23 of 25 cells** (alt 21).
- **It falls below 2σ only where the slopes are shallower and the orbits radial.** At the corner, every γ_i − 0.4 with β = +0.5, it is **+0.013 ± 0.022 dex, 0.6σ** (alt 0.1σ).
- **On the canonical footing, each range alone** keeps the deficit at 2.28σ or more. **On the alt footing,** the lowest slope shift alone already gives 1.86σ.

**How extreme the corner is:**
- **The slopes:** every galaxy's slope sits 0.4 below the published relation. The mean γ becomes 2.39 instead of 2.79.
- **The orbits:** every GC, red and blue, is on radial orbits with β = +0.5 at every radius. That is more radial than any GC system in the bracket's sources: NGC 5846's red GCs reach about 0.4 only outside 3 R_e, and M87's red GCs are tangential.
- **At that corner the law fits under either variant:** with SLUGGS's population masses it gives −0.24σ; with the four centrals excluded, −0.58σ.

**The law, σ (mean/error), canonical** (rows: shift in every γ_i; columns: β):

| | −0.50 | −0.25 | 0 | +0.25 | +0.50 |
|---|---|---|---|---|---|
| −0.4 | 2.95 | 2.68 | 2.28 | **1.66** | **0.59** |
| −0.2 | 3.31 | 3.17 | 2.97 | 2.65 | 2.09 |
| 0 (published) | 3.66 | 3.64 | 3.60 | 3.53 | 3.38 |
| +0.2 | 4.00 | 4.09 | 4.19 | 4.33 | 4.51 |
| +0.4 | 4.34 | 4.52 | 4.74 | 5.06 | 5.51 |

**Alt:** the cells below 2σ are (−0.4, 0) 1.86, (−0.4, +0.25) 1.20, (−0.4, +0.5) 0.08 and (−0.2, +0.5) 1.61. The full box is in the log.

**The rule is conditional in the opposite corner.** It fits (|z| < 2) in 13 of 25 cells on each footing:
- **Slopes steeper than published:** it fails in every cell with the slopes 0.2 or 0.4 steeper (2.06–3.47σ, alt 2.23–3.66σ).
- **Published slopes, tangential orbits:** it fails at β = −0.5 (2.06σ).
- **At the law's favourable corner** it over-predicts (−2.59σ).

## Controls

- **C1:** the box's edges reproduce the committed lanes exactly, in 40 comparisons:
  - its centre and slope column reproduce CFG111 (the centre and R2);
  - its β row reproduces CFG113's bracket.
- **MUTATE:** with the deficit removed at the weakest cell (D = 0.013 dex canonical, 0.002 alt), H1 fails at 0.00σ and the script exits 1. The main run fails H1 too, so the control does not discriminate on H1, as declared.

## Caveats

- **The anisotropy model is simple.** β is constant, and one β serves both red and blue GCs.
- **The slope shift is coherent:** the same δ for every galaxy.
- **The box's edges are declared brackets, not probability distributions.** The corner is a worst case, not a likelihood.
- **The masses are CFG55's JAM calibration.** SLUGGS's population masses weaken the deficit further (R4).

## Disclosure

- After the first run, C1's printed count of comparisons was corrected from 38 to 40 in the script. Both logs are otherwise unchanged apart from timing.

## Reading

- **The law's SLUGGS failure is conditional on the GC slopes and orbits.** It stays above 2σ at the published slopes for any measured-range anisotropy (CFG113), and at isotropy for any slope shift within ±0.4 on the canonical footing (CFG111). It disappears when shallower slopes and radial orbits combine.
- **So SLUGGS alone cannot make the law's deficit a clean failure,** and its rule-favouring reading is equally conditional.
- **What would decide it:** measured GC density slopes (photometric) and GC anisotropy for the massive centrals, M87, NGC 4365, NGC 4374 and NGC 5846.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## Addendum after the independent re-derivations CFG104–CFG106 (appended 2026-09-29; the text above is unchanged)

- **CFG106** (independent re-derivation of CFG114) reproduces it: 23/25 and 21/25 law cells above 2σ, 13/25 for the rule, the corner at 0.586σ. It checked against printed targets, not blind. h50's solver truncates the line-of-sight integral at u = 6, which biases σ_pred by up to 0.57% at the corner. The slopes are one relation shifted coherently, so the law's 2σ failure is only as firm as the unknown correlation of the relation's two coefficients. With 1000 draws, the fraction with the law below 2σ is 4.6% (β = 0) and 21% (β = +0.5) at ρ = −0.99, and about 43–47% at ρ = 0. The corner is a mean cancellation on the box boundary: six galaxies are still under-predicted by more than 0.05 dex, and M87 would need γ ≈ 1.6. A 20% error inflation takes 23/25 to about 21/25. **The slopes are 3-D.** Alabi+2017 define γ as the slope of the de-projected GC number-density profile, as checked in the paper's arXiv HTML on 2026-09-29. So the Jeans solution's ρ ∝ r^−γ uses it as intended; the case of projected slopes, which would put SLUGGS at +5.6σ at φ = 1, does not arise. The 'published slopes' are one mass relation, γ = clip(−0.63 log M* + 9.81, 2, 4) (2.49–3.43), not per-galaxy measurements.
