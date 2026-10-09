# CFG509: is the KiDS early/late lensing split caused by satellites leaking unevenly into the two classes? Leakage really does differ by class, but it does NOT explain the split (4.40σ becomes 3.88σ)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone (dfc467df4). It was written after the photometric companion counts and before any lensing re-score.
- **Data:** on disk only; no downloads. All runs used nice 15 and at most 4 threads.
- **Standing rules:**
  - κ = ½ is fitted. The footings 9.3603e-11 and 1.1312e-10 are scored separately and never pooled. a₀ is flat.
  - The cold energy's mass is still required, and no particle species is added.
  - Nothing here says the data favour the framework, and nothing says "theory closed".

## Bottom line
1. **The model-independent counts show differential leakage** (`cfg509_counts.*`; no shear values are read). We use CFG502's method verbatim: count more-massive neighbours within 0.5 Mpc, with 10 < |Δχ| < 600 Mpc, and subtract the area-scaled 4–6 Mpc annulus.
   - **Raw excess per lens:** about the same in both classes. Late 0.248 ± 0.006, early 0.257 ± 0.005 (stack-weighted).
   - **At matched log M\* and z:** early lenses have **1.53×** as many excess companions as late lenses (0.321 vs 0.210). The early value is higher in **16 of 16** cells.
   - **Leaked fraction:** CFG502's halo-model conversion gives λ = 0.589 ± 0.017 (late) and 1.057 ± 0.022 (early). That is f_leak = **0.113 (late) vs 0.168 (early)**, a difference Δf = +0.055 ± 0.004.
   - **The record had the sign backwards:** its colour-blind E, based on mass alone, had more leakage in the late class (0.192 vs 0.159).
2. **That leakage moves the split only a little** (M0 masses, CFG503 environment term with class-dependent λ, the law at s = 1):

| setting | K1 (7 bins) χ² / σ, canonical = alt | inner 9 (R ≤ 0.3/h) χ² / σ, canonical (alt) |
|---|---|---|
| L-none: no environment (= CFG95 / CFG505) | 35.03 / **4.40** | 47.26 / **5.09** (5.10) |
| L-cb: colour-blind E (= CFG505 R3) | 35.58 / 4.45 | 50.31 / 5.34 |
| **L-meas: class leakage from the counts (headline)** | 29.79 / **3.88** | 36.31 / **4.14** (4.14) |
| L-meas with stripping | 3.95σ | 4.29σ |
| L-match / L-unw / L-2sd (favourable bracket) | 3.89 / 3.80 / 3.80σ | 4.16 / 3.97 / 3.98σ |
| L-lit, colour satellite fractions from the literature (LCDM-calibrated, transcribed from memory, flagged) | 4.05σ | 4.51σ |

3. **Verdict (frozen rule): NOT EXPLAINED.**
   - On K1 the split drops by 0.51σ on both footings. PARTLY needs a drop of at least 1σ; EXPLAINED needs below 2σ.
   - Every reported setting also reads NOT EXPLAINED, including the +2 SD bracket and the literature cross-check.
4. **Why it cannot work: the shape is wrong.**
   - A leaked satellite adds its host's off-centre ΔΣ, which is nearly flat inside about 0.5 Mpc. The class-dependent part E_early − E_late is +0.4 to +1.0 Msun/pc² across K1.
   - The measured split D = ESD_early − ESD_late rises steeply inward: 3.3, 7.1, 5.6, 5.3, 11.9, 21.5, 33.3 Msun/pc² over bins 8–14.
   - The diagnostic scan raised λ_early from 0 to 20 with λ_late held at its measured value. **No value brings K1 below 2σ.** The best is λ_early = 2.5 (3.07σ); larger values make the fit worse again.
   - So host lensing cannot produce the centrally concentrated excess of early types. That excess sits at R ≲ 0.1 Mpc, where the lens's own mass dominates.
5. **The split stays B's one specific failure.** Including the measured leakage, it is 3.9σ (K1) and 4.1σ (inner 9) on both footings.
   - Per-class absolute fits with L-meas: late K1 7.4/7, inner 9 10.1/9 (canonical). Early K1 95.7/7, inner 9 99.0/9 (canonical); 68.9 / 69.9 (alt).
   - So the early class's own inner profile is what fails. Leakage repairs the late class's outer bins (outer-6 χ² 32.5 → 9.5, reported only).

## M2 masses (CFG505 UV / colour-M/L), reported
- L-none: K1 4.52σ, inner 9 6.72σ.
- L-meas: K1 4.01σ, inner 9 5.55σ.
- Same reading: the leakage takes about 0.5σ off K1 and the split stands.

## Controls and MUTATE (all pass)
- **C0:** the staged ISO lenses are the same, in the same order, as `lr_lenses.npz`.
- **C1 (counts):** the all-lens measured/predicted ratio is 0.8454, reproducing CFG502's 0.845.
- **C1 (score) = MU0:** with zero leakage (E ≡ 0) the split reproduces CFG505/CFG95: 35.0254 (canonical), 35.0263 (alt).
- **C2:** the colour-blind E reproduces CFG505 R3: K1 35.579, inner 9 50.308.
- **C3:** E = A + f_W B reproduces CFG503's table to 3e-14.
- **C4:** the CFG261 base law table, rebuilt here, matches exactly.
- **MU1 (swap λ_early ↔ λ_late):** the split gets *worse* (K1 5.09σ, inner 9 6.66σ, against 3.88 / 4.14). So the swapped leakage does not explain it, as required. The machinery is sign-sensitive.
- **Disclosed fix:** the first main run printed "inf" for the stripping variant of L-f0 (λ = 0), from a 0/0 in a cell average. It was fixed to zero stripping when λ = 0 and re-run. No other number changed.
- numpy's Accelerate matmul RuntimeWarnings appear on stderr (the known quirk); every table is finite.

## Limits
- **The counts measure fraction × companions per satellite.** The λ conversion assigns all of the class difference to the leaked fraction. If early lenses instead sit in more massive hosts, B would grow per satellite, but by host-mass scaling, not by the factor of more than 30 that the inner bins need.
- **The host term is CFG503's** (NFW hosts, satellites distributed like the host, ζ ξ_NL), and CFG503's LCDM gate fails at 1–1.4 Mpc. Outer bins are never in a verdict.
- **No framework-native environment.** CFG506 has frozen criteria only and no results.
- **The literature cross-check is approximate.** Its colour satellite-fraction ratios (2.0 → 1.4) were transcribed from memory and not checked against the papers.
- **Owner go needed** for a direct spectroscopic satellite fraction (KiDS-bright × GAMA) or the MICE mock. Neither was used.

## Run
```
nice -n 15 python3 cfg509_counts.py                          # step 1-2, seconds; needs ../../../_external_data/cfg502_work/
nice -n 15 python3 -u cfg509_score.py                        # ~3 min; needs cfg503_work, cfg505_work; writes cache to cfg509_work
CFG509_MUTATE=1 nice -n 15 python3 -u cfg509_score.py
```
