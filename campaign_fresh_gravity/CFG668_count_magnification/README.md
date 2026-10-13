# CFG668 — background galaxies behind clusters vs blank sky (result)

Criteria frozen in 6207c1861. Data: 361 redMaPPer clusters (λ>60, z 0.1–0.3) and 445 clean random SDSS fields
(no λ>20 cluster within 15'); SDSS DR18 galaxies, r 17–21.5, photo-z > z_cl + 0.2. Angular annuli; no cosmology.

Faint bin (r 20.5–21.5), galaxies per pointing:
| annulus | behind clusters | blank sky | ratio |
|---|---|---|---|
| 0–2' | 7.00 | 4.34 | 1.61 ± 0.08 |
| 2–4' | 17.89 | 13.14 | 1.36 ± 0.05 |
| 4–6' | 26.42 | 21.63 | 1.22 ± 0.05 |

**Verdict as frozen: NOT DIAGNOSTIC.** The count slope is s > 0.4 in every bin (1.21, 1.08, 0.58), so the frozen
sign-flip test cannot be run: lensing and member leakage both predict an excess. The size of the excess (implied μ ≈ 2.8
averaged over 0–2') is not lensing.
POST-HOC (cfg668_posthoc_zcut.py, not frozen): the inner excess falls with the photo-z gap, 2.47 → 1.61 → 1.18 → 1.07 → 1.15
for gaps 0.1–0.5, so it is cluster members leaking through SDSS photo-z. With gap ≥ 0.4 the ratio is 1 within 1σ, but only
~0.7 galaxies per cluster remain inside 2', far too few to see a 5–10% lensing effect.
MUTATE (shuffled positions): ratios return to 1 (one bin at 0.72 ± 0.10, the only >2σ excursion of 9).
SDSS is too shallow for this test; it needs deeper imaging with good photo-z (e.g. HSC, DES, KiDS).
κ fitted; cold energy mass required; not theory closed.

## Addendum A1 result — KiDS DR5 + DES Y6 (criteria 461d16c55; cfg668_a1_analysis.py → cfg668_a1.out)
120 KiDS + 248 DES clusters (redMaPPer λ>30), 137 + 256 clean blank fields, 1.45 M galaxies (r 20–24).
Combined, 0–2', galaxies behind clusters / blank sky:
| photo-z gap | r 20–22 | r 22–23 | r 23–24 | frozen verdict |
|---|---|---|---|---|
| +0.3 (primary) | 1.43 ± 0.06 (s 0.70) | 1.23 ± 0.03 (s 0.48) | 1.03 ± 0.02 (s 0.37) | CONTAMINATED |
| +0.4 (confirm) | 1.33 ± 0.07 (s 0.84) | 1.09 ± 0.03 (s 0.57) | 0.95 ± 0.02 (s 0.40) | MIXED (no frozen pattern) |

**Verdict as frozen: LENSING NOT DETECTED.** The primary gap is still contaminated by members. At +0.4 the faint bin sits at
s ≈ 0.40, the null point where magnification changes nothing, so there is no bin with s clearly below 0.4 to show the deficit.
The faint-core deficit that does appear (DES 0.943 ± 0.018 at +0.4, s = 0.44; 0.899 ± 0.018 at +0.5, s = 0.50) is in a bin where
lensing predicts a small EXCESS, so it reads as faint galaxies hidden behind bright cluster members (obscuration/blending), not lensing.
Not frozen, hint only: the bright excess survives a +0.5 gap (DES 1.44 ± 0.12, KiDS 1.17 ± 0.13). A magnification μ ≈ 1.2 would
give about that, but bright members thrown to high photo-z do the same, and this data cannot split them.
MUTATE: DES null at every gap; KiDS shows a coherent ~5% low offset (up to −2.4σ), so KiDS field-to-field systematics are ~5%.
Next honest step: shear (already done: CFG663 says the extra sector lenses) or spectroscopic backgrounds; counts cannot do it.
κ fitted; cold energy mass required; not theory closed.

## Addendum A2 result — quasars (criteria a17b552d1; cfg668_a2_quasars.py → cfg668_a2.out)
25,663 redMaPPer λ≥20 clusters vs 48,987 blank fields; quasars at z_Q > z_cl + 0.5 (cannot be members).
| catalogue (primary aperture) | bright / steep | middle | faint |
|---|---|---|---|
| Quaia G<20 (0–4') | 1.068 ± 0.031 (s 0.90, +2.2σ) | 1.026 ± 0.024 (s 0.53) | 0.975 ± 0.021 (s 0.46) |
| DR16Q (1–4') | 1.000 ± 0.023 (s 0.68) | 0.963 ± 0.016 (s 0.31, −2.3σ) | 0.971 ± 0.013 (s −0.17, −2.3σ) |
Combined steepest bin: R = 1.025 ± 0.018 (+1.4σ). **Verdict as frozen: NOT DETECTED** (needs ≥ 3σ).
The DR16Q faint deficits go the lensing way, but the faint DR16Q slope is negative (the spectroscopic catalogue is incomplete there), and
inside 1' DR16Q drops to 0.75 ± 0.04: fibre collisions and blending near cluster galaxies, far bigger than lensing. Not usable as lensing.
POST-HOC (cfg668_a2_posthoc_lambda.py, not frozen): the Quaia bright excess does not grow with richness (λ 20–30: 1.11 ± 0.04;
30–50: 1.03 ± 0.04; ≥50: 1.06 ± 0.06). Lensing must grow with mass, so the +2.2σ is not read as lensing.
MUTATE: NULL for both catalogues. Expected size for typical weak lensing (μ ≈ 1.05 over 0–4') is R ≈ 1.06 in the steep bin, i.e. at
the edge of this sample's reach (±0.03); counts alone cannot make the call. Shear (CFG663) remains the measurement that settles lensing.
κ fitted; cold energy mass required; not theory closed.
