# W1_EXTRACTION -- bulk per-side extraction, ALL per-side-capable WALLABY galaxies

Generated 2026-07-16 11:25 by `write_w1_report.py` from `perside_237.csv`
(driver `run_extraction_237.py`, QC frozen BEFORE extraction in `QC_FROZEN.md`).

## FIREWALL (read first)

At N~237 the achieved sensitivity at AQUAL amplitude is **~1-1.5 sigma**
(n=16 gave 0.3 sigma; sqrt(237/16) = 3.85x). **NEITHER pre-registered kill
condition (3-sigma AQUAL-vs-BranchB; N~1,157 canonical a0 = 9.36e-11,
N~1,424 alt a0 = 1.13e-10, both max-clustering e_N, w = 0.304) CAN TRIGGER
on this sample.** Kill-condition language in this lane appears ONLY as
"cannot trigger". a0 does not enter the extractor; both footings enter at
the confrontation stage only. This file contains NO directional statistic,
NO g_ext correlation, and NO AQUAL/Branch-B/pure-MI verdict.

## Sign convention (THE SIGN TRAP -- handled, hand-verified)

- **Pre-registered**: A_i = 2(v_rec - v_appr)/(v_rec + v_appr), tied to the
  RECEDING side (p_i > 0 predicts attractor-side-faster for x >~ 2e).
- **Extractor raw** (pilot printout): A_ext = 2(v_app - v_rec)/(v_app + v_rec)
  -- OPPOSITE ordering. Both recorded per galaxy in the CSV.
- Receding side determined EMPIRICALLY per galaxy (frozen rule, QC_FROZEN.md);
  `pa_flipped` galaxies (WKAPP PA anti-aligned with the true receding side): **0**.
- Hand verification from the raw mom1 map (independent code path,
  `hand_verify_sign.py`, J165901-601241): see its output below the funnel.
- PA source verified from Deg+2022 arXiv:2211.07333 Table 4 (fetched + grepped
  2026-07-16, not assumed): PA_model_g = "Position angle in equatorial
  coordinates (East of North)"; the paper does NOT restate receding-side
  anchoring, hence the empirical rule.

## QC funnel (cuts frozen 2026-07-16 BEFORE any real A value)

| stage | N |
|---|---|
| per-side-capable (CADC census: mom1 + WKAPP AvgMod geometry) | 237 |
| all 3 files downloaded (mom1 + mom0 + AvgMod) | 237 |
| extractor returned a valid A + bootstrap | 237 |
| **passed ALL frozen QC cuts** | **50** |

Exclusion reasons (a galaxy failing ANY frozen cut is excluded):

| reason | N |
|---|---|
| inclination >= 70 deg | 74 |
| n_outer < 4 rings | 67 |
| sanity ratio outside [0.8, 1.2] (all failures were LOW: beam-smeared / poorly-resolved per-side curve under-reads the WKAPP model) | 44 |
| sigma_boot >= 0.05 | 2 |

QC-pass galaxies running unweighted (mom0 unavailable): 0.

## sigma(A) distribution (QC pass, bootstrap) vs WHISP intrinsic rms 0.092

- median sigma_boot = **0.0110**; p10 = 0.0066, p90 = 0.0243
  (all extracted, pre-QC: median 0.0268, p90 0.0531)
- histogram (QC pass): [0.000,0.005): 2, [0.005,0.010): 17, [0.010,0.020): 23, [0.020,0.030): 7, [0.030,0.050): 1
- median sigma_boot / 0.092 = **0.12** -> the PIXEL-bootstrap error is
  subdominant to the intrinsic lopsidedness scatter; naive per-galaxy noise
  sqrt(0.092^2 + median sigma_boot^2) = 0.0927. HOWEVER the OBSERVED QC-pass
  rms(A) = 0.155 exceeds this: the bootstrap does NOT capture the dominant
  vsys-mismatch term (diagnosed below) -- the effective per-galaxy noise for any
  ensemble use is the observed 0.155, not 0.092.

## A_preregistered distribution (QC pass; DESCRIPTIVE ONLY -- no direction attached)

- N = 50; mean = +0.1040 +/- 0.0219 (sem); median = +0.0921;
  rms = 0.1551 (WHISP intrinsic 0.092); inverse-variance-weighted mean = +0.1050
- The rms DIFFERS from the WHISP 0.092 intrinsic-lopsidedness scatter.
- NOTE: an ensemble mean of A without the per-galaxy attractor direction is
  NOT the directional-EFE statistic (a nonzero mean here would indicate a
  convention/systematic, not physics; the directional test is cos(psi)-weighted
  and happens in the firing lane).

## Per-field breakdown

| field | capable | QC pass | mean A_pre | median | rms | median sigma |
|---|---|---|---|---|---|---|
| Hydra | 35 | 3 | +0.0825 | +0.2348 | 0.3038 | 0.0107 |
| NGC4636 | 43 | 7 | +0.1957 | +0.2022 | 0.1531 | 0.0079 |
| NGC4808 | 19 | 4 | +0.3383 | +0.3479 | 0.2315 | 0.0158 |
| NGC5044 | 92 | 18 | +0.0464 | +0.0605 | 0.1065 | 0.0117 |
| Norma | 31 | 12 | +0.0986 | +0.1010 | 0.0961 | 0.0113 |
| Vela | 17 | 6 | +0.0357 | +0.0264 | 0.0779 | 0.0098 |

## Diagnosed extraction systematic: vsys sensitivity (direction-blind)

The direction-blind QC-pass ensemble mean is **+0.1040 ± 0.0219**
— nonzero at ~4.7 sigma. A direction-blind mean of A should be ~0;
this was diagnosed (`diag_mean_offset.py`, computed not asserted):

- Per-galaxy empirical offset delta = (mom1 minor-axis weighted median − WKAPP
  VSys_model): **median +1.7 km/s, mean +2.5 km/s, rms 6.8 km/s, 70% positive**.
- NOT an optical-vs-radio cz convention mismatch: corr(delta, cz²/c) = -0.03
  and the mismatch would be 13–125 km/s at these cz — delta is ~2 km/s, flat in cz
  (half-a-WALLABY-channel scale, ~4 km/s channels).
- A_pre is amplified vsys error: dA/d(delta) ≈ 2/(v_rot · sin i · ⟨cosθ⟩) ≈ 0.026 per km/s
  (median). The coherent +2.5 km/s predicts a **+0.065 mean bias** (observed +0.104);
  the empirical 6.8 km/s scatter predicts σ_A ≈ 0.18 — the observed rms 0.155 is
  therefore **vsys-mismatch-dominated**, not pixel-noise-dominated (median
  bootstrap σ = 0.011) and not pure intrinsic lopsidedness (WHISP 0.092).
- DIAGNOSTIC-ONLY re-extraction with vsys := VSys_model + delta (frozen CSV
  untouched): mean A_pre → **+0.0280 ± 0.027** (consistent with zero),
  median +0.092 → +0.032.
- WKAPP quoted e_VSys (median 0.8 km/s, p90 3.8) explains only part of the
  6.8 km/s empirical scatter; the rest is map-vs-flat-disk-model mismatch
  (warps, lopsided outskirts, beam smearing into the minor axis).

**Implication for the firing lane (flag, not a verdict):** a direction-blind
additive offset in A cannot fake an attractor-aligned signal to first order
(cos ψ averages it out over isotropic attractor directions), but it (a) inflates
the per-galaxy noise from the banked 0.092 to ~0.155, further REDUCING achieved
sensitivity below the firewall's ~1–1.5σ estimate, and (b) any anisotropy of the
WALLABY fields on the sky couples the coherent +2.5 km/s term to the direction
statistic at second order — the firing lane must include a vsys-offset nuisance
test (e.g. re-fire with the delta-corrected A as a robustness branch). Neither
pre-registered kill condition can trigger regardless (see FIREWALL).

## Files

- `perside_237.csv` -- per-galaxy table (BOTH A_raw_extractor and
  A_preregistered, sigma_boot, QC pass/fail + reason, full provenance).
- `perside_237_curves.json` -- per-ring per-side curves (provenance).
- `run_extraction_237.py` (exit 0), `extraction_progress.log`, `data/`.
- `hand_verify_sign.py` (exit 0) -- raw-map hand check of the sign conversion
  (J165901-601241: PA side receding PASS; A_pre = -A_ext identically PASS;
  independent sign matches pipeline PASS).
- `diag_mean_offset.py` + `diag_mean_offset.json` -- vsys-systematic diagnosis.
- `QC_FROZEN.md` -- the frozen cuts; frozen BEFORE any real A value.
