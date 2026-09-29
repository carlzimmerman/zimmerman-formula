# CFG66 — do the Boötes I and Tucana II offsets survive their two flagged systematics?

Script: `CFG66_bootes_tucana_systematics.py` (about 40 s; it imports CFG51's reduction read-only). Outputs: `.out`, `_results.json`, and the MUTATE pair (velocities × 0.5). Written by a delegated agent with the question and criteria declared before the first run, and re-run here (main exits 0; the MUTATE run fails S1 and S2 as required).

## The frozen questions

CFG51 found, after per-star binary cleaning, that the bare law under-predicts Boötes I (+0.219 dex, 2.46σ) and Tucana II (+0.465 dex, 3.63σ), and flagged two systematics. **Q1:** Boötes I has a cold (≈ 2.4 km/s) and a hot (≈ 4.6 km/s) component in the literature, and CFG51's velocity window keeps both. **Q2:** Tucana II is tidally disturbed (an extended halo and a velocity gradient), and a gradient inflates a dispersion. Do the offsets survive (a) a two-Gaussian mixture fit for Boötes I and (b) a linear-velocity-gradient fit for Tucana II? Survival = the offset stays positive at more than 2σ on both footings.

## Results

**Q1, Boötes I (53 cleaned stars, common mean).** Fitted: s_cold = 2.00 km/s (1σ 1.19–2.82), s_hot = 5.09 (4.09–6.64), f_hot = 0.525 (0.29–0.84), total σ = 3.94 (3.46–4.56). **The split is not detected:** the likelihood-ratio improvement over one Gaussian is 2.31 and a parametric bootstrap gives P(LR ≥ 2.31) = 0.155 under the single-Gaussian null.
- Total-mixture offset: **+0.222 ± 0.097 dex (2.29σ)** canonical, +0.202 (2.09σ) alt. **S1 passes, marginally.**
- **Cold-only offset: −0.072 ± 0.203 (−0.35σ)** canonical, −0.092 (−0.45σ) alt. It does not survive; it is consistent with zero and with the total-mixture offset, because the s_cold interval is wide and dominates the ±0.20 dex error. **This replaces CFG51's "+0.007" (which used the literature's 2.4 km/s).**

**Q2, Tucana II (12 cleaned stars, tangent plane about the LVD centre).** The gradient is 2.0 ± 15.9 km/s/deg (0.43 km/s per half-light radius, position angle poorly defined); the likelihood ratio against zero gradient is 0.020 (p = 0.99, and 0.99 by a position-permutation null). The gradient-removed dispersion is 4.060 (+1.164 −0.821) km/s, unchanged from 4.064. Offset **+0.464 ± 0.128 dex (3.62σ)**, alt +0.444 (3.46σ). **S2 passes.** With 12 stars the gradient is essentially unconstrained (an error of about 3.4 km/s across one half-light radius), so this cannot exclude a moderate gradient.

## Controls and caveats

C1 passes (the single-Gaussian, gradient-free fits reproduce CFG51: 3.9108 and 4.0641 km/s; 55/14 members, 53/12 cleaned). A normalisation bug in the agent's first run (the single-Gaussian likelihood omitted an N ln 2π term the mixture included, giving LR = −95) was fixed before any result was used; no other change. The Boötes I margins (2.29σ, 2.09σ) are thin: the error is dominated by the 0.076-dex systematic floor plus the statistical error, and the alt footing barely clears 2σ. S1 rests on reading the total mixture dispersion as the galaxy's, and the mixture is not statistically preferred, so this is close to CFG51's own single-Gaussian result. Fitting a gradient to 12 stars lowers σ by chance (permutation null median 3.65 km/s), and here it lowered it not at all. Inherited from CFG51: the re-derived membership, no zero-point offset between epochs, and the 20 stars removed by the Boötes I velocity window before cleaning.

## Standing

**Both CFG51 offsets survive the declared systematics; Boötes I marginally, and its cold component alone is consistent with no failure.** The data cannot say whether Boötes I's hot component belongs to the galaxy. Two objects are not a population result. Nothing here says the theory is closed.
