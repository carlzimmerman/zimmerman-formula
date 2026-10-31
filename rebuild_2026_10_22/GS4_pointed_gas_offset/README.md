# GS4_pointed_gas_offset: NO OFFSET. Pointed gas masses and eRASS1's agree at the same radius, +0.005 ± 0.017 dex. By the frozen rule ZN3 fails on the keys: X-COP ONLY, G-OUT-M3 +4.35

Criteria and ledger: `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md` (1bf15a0aff), committed before any catalogue met eRASS1. Fetches: `FETCH_LOG.md`. Scripts `gs4_parse.py`, `gs4_match.py`, `gs4_regrade.py`, and post-result `gs4_post.py`. Numbers: `gs4_match.out`, `gs4_results.json`, `gs4_matched.csv`, `gs4_regrade.out`, `gs4_post.out`. κ = ½ FITTED; not theory closed. Nothing here says the data favour the framework.

**Primary:** 45 unique eRASS1 clusters with M500 4.4e13–5.6e14, at eRASS1's R500, h 0.70, Ωm 0.30. **Median d +0.005 ± 0.017,** rms 0.177. The line is +0.093, which is over 5 SE away. Slope against lg M500 −0.100 ± 0.100, 1.0σ, so no [MASS-DEPENDENT]. XMM +0.005 ± 0.020 and Chandra +0.009 ± 0.043 take the same class, so no [INSTRUMENT-DEPENDENT].

**SM1's +0.111 and RF3's +0.092 came from five massive clusters, and they don't carry over.** Those five are reproduced exactly (K1), and other tables agree with X-COP on them. X-COP's two clusters in the range read +0.122. Everything else in the range reads close to zero.

## By catalogue and lensing M500 tercile
d at eRASS1's R500, median, with N. Tercile edges are the lensing sample's, 1.36e14 and 2.39e14.

| Catalogue | instrument, radius | matched, all mass | in range, N | d ± SE | at own R500 | M1 | M2 | M3 |
|---|---|---|---|---|---|---|---|---|
| X-COP, **profile read** | XMM, HSE | 5 | 2 | +0.122 ± 0.011 | +0.090 | – | – | +0.122 (2) |
| Lovisari+20 | XMM, HSE | 59 | 4 | +0.029 ± 0.021 | −0.070 | – | – | +0.029 (4) |
| Lovisari+15 | XMM, HSE | 7 | 6 | +0.049 ± 0.112 | −0.065 | +0.049 (6) | – | – |
| Croston+08 REXCESS | XMM, Y_X | 18 | 12 | −0.030 ± 0.018 | −0.165 | – | −0.119 (1) | −0.020 (11) |
| Eckert+16 XXL | XMM, WL-based M–T | 7 | 6 | +0.094 ± 0.088 | +0.085 | +0.401 (1) | +0.118 (3) | +0.013 (2) |
| Maughan+08 | Chandra, Y_X | 36 | 6 | +0.095 ± 0.174 | +0.073 | – | +0.711 (1) | +0.048 (5) |
| Landry+13 | Chandra, HSE | 10 | 0 | – | – | – | – | – |
| Sun+09 | Chandra, HSE | 10 | 9 | −0.021 ± 0.034 | −0.121 | −0.021 (3) | −0.025 (4) | +0.032 (2) |
| Mahdavi+13 | mixed, WL | 9 | 1 | −0.023 | −0.070 | – | – | −0.023 (1) |
| Vikhlinin+09, not primary, LITERATURE-INPUT | Chandra | 20 | 8 | +0.057 ± 0.036 | +0.018 | – | – | +0.057 (8) |
| **Primary, unique clusters** | | | **45** | **+0.005 ± 0.017** | −0.087 | **+0.032 ± 0.061 (10)** | **−0.002 ± 0.086 (9)** | **+0.005 ± 0.016 (26)** |

All rows but X-COP's are slope-converted, s = 1.19. Each tercile takes the class NO OFFSET. All 10 catalogues' rows are in `gs4_matched.csv`.

## ZN3's regrade, frozen rule, one template, both h
| gas | f★ 0.034 | f★ 0.0615 | class |
|---|---|---|---|
| **+0.005, measured** | **12 of 15, G-OUT-M3 +4.35** | **12 of 15, G-OUT-M3 +4.06** | **X-COP ONLY** |
| +0.022, median + SE | 12, +3.92 | 13, +3.63 | X-COP ONLY |
| −0.012, median − SE | 10, +4.75 | 11, +4.48 | X-COP ONLY |
| +0.111 (K3, ZN3's own) | 15, +1.46 | 15, −1.33 | passes both |

The worst values are at h 0.672; h 0.686 is 3.61–4.02 for the measured row, and G-MID-T3 and G-OUT-Mall also go over 2. X-COP's own line isn't moved by this offset, since it reads the rule's halo, not the keys' gas. d(M) wasn't run because the tag didn't fire.

## How hard I pushed on the low number
ZN3 needed this high, so a low answer is the disappointing one, and it gets the same audit.

| Test, not graded | N | median d |
|---|---|---|
| Gas slope 1.0, 1.4 | 45 | −0.010, +0.021 |
| 6 arcmin | 46 | +0.007 |
| eRASS1 CTS500 above, below median | 23, 22 | −0.002, +0.007 |
| z below, above 0.2 | 36, 9 | −0.003, +0.070 ± 0.101 |
| M13 + E16, no hydrostatic radius | 7 | +0.070 ± 0.085 |
| In the lensing sample | 5 | −0.002 ± 0.056 |
| At each catalogue's own R500 | 45 | −0.087 ± 0.021 |
| All masses, post-result | 130 | +0.024 ± 0.008 |
| lg M500 14.75–15, above 15, post-result | 60, 23 | +0.023 ± 0.008, +0.040 ± 0.015 |

- Row by row in `gs4_post.out`, matches are good: mostly under 2′, sensible redshifts. The wild rows (+0.71, +0.52) have 11–14 eRASS1 counts, and a median holds up against them.
- Reaching +0.093 by the slope alone would take s of about 2.3. L15's value over a wider range is about 1.58.
- The largest single move is the radius: eRASS1's R500 is larger than the pointed papers' by a median of 0.05–0.10 dex. Own-radius d is lower still, so that step isn't what's keeping it down.
- Same clusters, different tables agree: 53 pairs, median |difference| 0.027 (K2). X-COP is high against Vikhlinin on the same clusters by 0.039, and level with Lovisari+20.

## Limits
1. **M1 and M2 are weak.** +0.032 ± 0.061 and −0.002 ± 0.086 don't exclude +0.093 on their own. M3, where G-OUT-M3 fails, is the well-measured one (26 clusters), though G-OUT-M3's tercile is by Mgas and this one's by M500.
2. **Only 5 of the 45 are in the lensing sample.** Pointed samples are X-ray bright, so the matched objects aren't typical of it.
3. **eRASS1's M500 and R500 are its own scaling (ΛCDM count fit, WL-calibrated).** The radius everything is read at depends on them. A noise-correlated tilt in d against that M500 is expected and did not appear above 2σ.
4. **Slope-converted rows use X-COP's massive-cluster slope at every mass.** Only X-COP is a profile read.
5. **Published Mgas differ in centring, clumping, background and calibration.** Hydrostatic, Y_X and WL-based radii are mixed. Cross-catalogue offsets are small, but a shared bias in all pointed work wouldn't show here.
6. **Deviations, none tuned, all before matching except the post-result rows marked.** V09 uses only its low-z table (the high-z names give no usable position). S09 uses only rows with a measured r500. Five Abell-style Zwicky aliases and a few others for NED came from my memory; a wrong alias just fails to match on position and z. Z5247 was unresolved.

## Checks
K1 X-COP against SM1 and RF3, max |d| 7e-17, PASS. Other tables on those five: median |difference| 0.039, under 0.05, PASS. K2 0.027, PASS. K3 at +0.111 against ZN3: preds, Z, rms |d| 0, PASS. MUTATE RA + 1°: 0 matches of 181, BITES. MUTATE shuffle: rms 0.177 to 0.627, K1 FAILS, BITES. Its median moves to +0.73, with a fake slope, because a shuffle puts massive clusters' gas on light ones in the mass window: that's the shuffle's artefact, not a surviving offset.

## Couldn't get
VizieR's CDS hosts timed out, so tables came from the IDIA mirror. No per-cluster Mgas500 in Schellenberger & Reiprich 17, Andrade-Santos+17/+21, Pratt+09, Mantz+16, Martino+14, Zhang+08. Vikhlinin+09 tabulates M_G, not gas mass. Mahdavi+13's and Landry+13's clusters nearly all sit above the range on eRASS1's M500.

    python3 -I gs4_parse.py; python3 -I gs4_match.py; python3 -I gs4_post.py; python3 gs4_regrade.py --k3; python3 gs4_regrade.py --dex 0.0053 0.0223 -0.0116; GS4_MUTATE=ra python3 -I gs4_match.py; GS4_MUTATE=shuffle python3 -I gs4_match.py

κ = ½ FITTED; cold dark energy is a gravitating field component, never a particle; not theory closed.
