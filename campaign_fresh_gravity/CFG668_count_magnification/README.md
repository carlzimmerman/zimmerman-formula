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
