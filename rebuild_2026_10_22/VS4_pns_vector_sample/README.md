# VS4_pns_vector_sample: NO VERDICT. Extraction check C1 failed, rms 0.112 against 0.05. With C1 waived the label would still be UNDECIDED

Criteria: `FROZEN_CRITERIA.md` (bda6cdff53), alone first, **not blind**. `vs4.py`, `vs4.out`, `vs4.json`, `vs4_MUTATE.out`, `vs4_diag.py`, `vs4_diag.out`. Source: arXiv e-print 1712.05833 (Pulsoni+2018), in `_external_data/vs3_pulsoni2018/`, sha256 d7d964a04d0d236a289ef099de5d07f38cf4faee47467fbacffffd8ceafc6c4f. Dispersions come from the paper's vector figures. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Reinstates nothing.

Not graded, because C1 failed. n = 24, canonical; alt is within 0.003.

| Row | Slow | Central | Mass slope |
|---|---|---|---|
| **1000 kpc, 1000 km/s, primary** | +0.057 +- 0.037 | +0.022 +- 0.031 | +0.094 +- 0.039 |
| 500 kpc, 500 km/s | +0.050 +- 0.035 | +0.042 +- 0.028 | +0.093 +- 0.036 |
| 300 kpc, 500 km/s | +0.051 +- 0.036 | +0.034 +- 0.033 | +0.091 +- 0.038 |
| Primary, no JAM quality 0 (n = 20) | +0.099 +- 0.029 | +0.011 +- 0.022 | +0.055 +- 0.028 |

Slow non-centrals at primary: NGC 3608, 4365, 4374, 4552, so the count of 4 is met only through the window chosen after seeing labels. MUTATE: slow falls to +0.013 +- 0.039 and -0.007 +- 0.038, as required.

## C1
Overlap with CFG492, figure minus CFG492: NGC 3608 -0.207, NGC 1023 -0.203, NGC 4564 -0.072, NGC 3377 -0.066, NGC 5846 -0.061, NGC 4374 -0.060, NGC 821 +0.007, NGC 4494 -0.007. Mean -0.084.
- **NGC 3608:** CFG492 bins 100, 163, 158 km/s, the figure 77, 102, 84. The raw catalogue has std 271 km/s at 2-4 arcmin against 83 inside 1 arcmin. The excess is in a small number of outlying velocities. NGC 3607 sits 5.9 arcmin away; contamination is plausible, not shown.
- **NGC 1023:** CFG492 126-179 km/s, the figure 83-131. The paper takes dispersion about its rotation fit and CFG492 does not, which fits a rotating S0.
- The remaining six still run about 0.05 dex low, so the two methods differ systematically.

I set C1 assuming the two reductions were near equal. The disagreement mainly points at CFG492's PN rows, but the rule was fixed before the run and I don't regrade.

## Consequences
- **VS3's lean does not stand.** It needed NGC 3608's +0.137 contrast; on the published reduction NGC 3608 is -0.057. NGC 1023's counterexample also goes away.
- Being central never reaches 2 sigma in any row, but the bar for SPLIT NOT REAL is not met either.
- Rotation is positive in every row and exceeds 2 sigma only without JAM quality 0, a row that drops two slow rotators. It trades against mass.

## Limits
Figure-read, smoothed values. Isotropic Jeans. Quality-0 JAM rows. Central is a magnitude rule. An offset is not a halo. No mechanism tested. The per-PN catalogues behind NGC 4552 and 4365 (Arnaboldi et al.) were "in prep." in this source; a re-reduction with one method would need them.
