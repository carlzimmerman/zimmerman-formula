# CFG45 — the rule-readings harness: four readings, all populations, one conjunction

Script: `CFG45_rule_readings.py`, about 5 s. Outputs: `.out`, `_results.json`, and the MUTATE pair (collapse masses divided by 100). Written by a delegated agent with the readings, statistics and thresholds declared in the docstring before the first run; re-run here. Both runs exit 1: the MUTATE run by design, the main run because the control C2a failed (kept).

## The four readings (declared, none added afterwards)

| | reading |
|---|---|
| (L) | the bare law (control) |
| (S) | the sum as committed (CFG35): law + f_ex (1 − f_b) M_NFW(<r) |
| (M) | the radial max: dark mass inside r is max(the law's phantom, the collapse halo), with no f_ex |
| (E) | the exterior leftover: the law inside the edge, the leftover placed only outside it |

Acceptance (A1–A7): the ultra-faints (|KM median| < 2σ), the classical satellites (not below −2σ), SPARC (unchanged), SLUGGS, the X-ray ellipticals, UGC 2487 (error 0.071 dex, declared by the harness because CFG36 gave none) and the four Di Teodoro S0/S0a.

## Result (sigma, canonical | alt)

| population | L | S | M | E |
|---|---|---|---|---|
| UFD, KM median | +3.77 \| +3.55 | −0.41 \| −0.41 | −0.35 \| −0.35 | = L |
| MW classical | +0.32 \| +0.09 | −1.78 \| −1.90 | −1.77 \| −1.77 | = L |
| M31 LVD | +0.60 \| +0.42 | **−2.67 \| −2.66** | −2.48 \| −2.72 | = L |
| SPARC log M_* ≥ 10, fraction < 0.03 dex | 100% | 98% | **64%** | 100% |
| SLUGGS | +3.28 \| +2.67 | +0.39 \| +0.10 | **−2.12 \| −2.13** | = L |
| X-ray ellipticals | +1.70 \| +1.58 | +1.04 \| +1.03 | +0.78 \| +0.78 | = L |
| gates passed | 5/7 | **6/7** | 4/7 | 5/7 |

**No reading passes all seven.** (S) fails only the classical satellites (M31 LVD). (M) does not fix the double count and additionally over-predicts SLUGGS and moves 36% of the massive SPARC spirals by more than 0.03 dex. (E) is identical to the bare law in every lane, because the exterior shell never reaches a data radius.

## Controls and caveats

- C1 passes: (L) and (S) reproduce 66 committed numbers from CFG32, CFG36, CFG38, CFG40, CFG41 and CFG42.
- **C2a fails, kept:** the largest r/r_e is 60 (SLUGGS's Jeans tail). A diagnostic added after seeing it (R1) shows E − L = 0 exactly; no gate, threshold or reading changed.
- Fragile assumptions: the clamped Moster relation (the UFD floor is the collapse-mass floor); the NFW cusp, which closes the ultra-faints and over-predicts the classical dwarfs at once, so a core would trade one for the other; the lane error models and the colour convention.

## Standing

**Among the natural zero-parameter readings, the sum is the best, and it fails one gate. None closes candidate B, and the radial max is not a fix.** This is a design constraint, not a result for the framework. Nothing here says the theory is closed.

**Kernel note (CFG64).** This lane's estimator uses the exponential RAR kernel (`hunt_lib.nu_s`, ν = 1/(1 − e^{−√y})), not ν_mono as the text above says; the two agree to 3 × 10⁻⁹ for y ≤ 0.1. Swapping the kernel to P2 leaves the headline verdict unchanged (see `CFG64_kernel_robustness/README.md`).
