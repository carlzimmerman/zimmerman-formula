# CFG51 — the ultra-faint failure with multi-epoch, binary-cleaned dispersions (Walker+2023)

Script: `CFG51_walker_ufd.py` (about 3 s); the reduction is `CFG51_walker_multiepoch/reduce_walker.py` (declared rules in its docstring; re-run here and identical to the delegated agent's table). Data: `real_research/data/walker2023/` (the gzipped VizieR J/ApJS/268/19 catalogues, 11.7 MB; fetched with the owner's approval). Outputs: `.out`, `_results.json`, and the MUTATE pair (dispersions × 0.5). **The main run exits 1: control C1 failed as declared** (below). H1 and H2 pass.

## Question

CFG46's statistical binary correction lowered B's ultra-faint offset but could not settle it. The decisive test is per-star multi-epoch data: stars whose velocities vary between epochs are removed. Walker et al. 2023 give per-epoch velocities for 16,369 stars in 38 systems (up to 15 epochs). Only **two ultra-faints are informative** (at least 8 multi-epoch members, at least half the sample): Boötes I (33 of 55) and Tucana II (9 of 14). Nine others lack members or epochs. This is a two-object test, not a sample statistic.

## Results (canonical footing; alt within 0.02)

| system | σ_law | single-epoch σ | all-epoch mean | binary-cleaned σ | offset, single | **offset, cleaned** | rule, cleaned |
|---|---|---|---|---|---|---|---|
| Boötes I | 2.36 | 4.82 | 3.92 | 3.91 (+0.45 −0.38) | +0.310 | **+0.219 ± 0.089 (2.46σ)** | −0.205 |
| Tucana II | 1.39 | 7.48 | 5.30 | 4.06 (+1.16 −0.82) | +0.730 | **+0.465 ± 0.128 (3.63σ)** | −0.165 |

**H1 passed:** the cleaned offset is positive at more than 2σ for both, on both footings. **H2 passed:** cleaning lowers the offset (Tucana II by 0.27 dex, Boötes I by 0.09) but does not remove it. The paper's own variability flag gives +0.224 and +0.394.

## What to know before believing it

- **Control C1 failed as declared.** It expected the single-epoch dispersions to agree with the repo's literature values to 30%. Boötes I does (4.82 against 4.0); **Tucana II does not (7.48 against 3.8)**. That factor of two is the binary inflation the cleaning removes, so the "failure" reflects the effect being measured. The tolerance is unchanged.
- **Boötes I's result rests on including its hot kinematic component.** The literature finds two components (cold 2.4, hot 4.6 km/s; Koposov+2011), and the reduction's velocity window keeps both. **The cold component alone (2.4 km/s) would put Boötes I at +0.007 dex, with no failure at all.** (Arroyo-Polonio's cold-only f-free 2.18 gives −0.03; CFG46.) Whether the hot component belongs to the galaxy is exactly the open question.
- **Tucana II is tidally disturbed in the literature** (an extended halo and a velocity gradient), and a gradient inflates a dispersion.
- **Membership is re-derived** (the catalogue has none): a ±4σ velocity window about the systemic velocity, logg < 4, Gaia proper motion and parallax. The window can remove large-excursion binaries before the cleaning (20 for Boötes I), which biases σ low. The first membership rule ran away in the most contaminated fields (Segue 1 gave 112 km/s) and was replaced once, with no further tuning (disclosed in the script). Segue 1 then kept 6 members and is unusable. No zero-point offset between epochs is modelled.

## Standing

**In the two systems where multi-epoch cleaning is possible, the bare law under-predicts the dispersions by +0.22 (Boötes I, 2.5σ) and +0.47 dex (Tucana II, 3.6σ) after cleaning.** For Boötes I that depends on the hot component; for Tucana II on the absence of a tidal inflation. **The derived rule over-predicts both by 0.17–0.21 dex.** The data lie between the bare law and the sum rule in both systems, consistent with CFG42–CFG46: neither reading fits, and the truth needs a partial debris.

Two objects do not make a population result. The other multi-epoch UFDs need data that do not exist yet (Hydrus I, Reticulum II and Ursa Major II have no repeat epochs in this catalogue).

Nothing here says the theory is closed.

**Kernel note (CFG64).** This lane's estimator uses the exponential RAR kernel (`hunt_lib.nu_s`, ν = 1/(1 − e^{−√y})), not ν_mono as the text above says; the two agree to 3 × 10⁻⁹ for y ≤ 0.1. Swapping the kernel to P2 leaves the headline verdict unchanged (see `CFG64_kernel_robustness/README.md`).
