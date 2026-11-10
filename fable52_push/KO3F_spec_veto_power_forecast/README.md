# KO3F: would spectroscopy sharpen KO1's host veto? A power forecast (2026-11-09)

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Not registered in the closure record.

**This is a forecast, not a graded lane.** It has no frozen criteria and no label, because it grades nothing and reads no
lensing signal: the staged shear sums (`WG`) are never opened, and from KO1's result file only the published errors are
read. It was written to decide whether the "clean isolation test" in the push README (section 5, item 2) is worth freezing.

## Answer first

**Not on the data that exist today.** Redoing KO1's host veto with DESI DR1 redshifts shrinks the error on the late-type
(disc) outer amplitude by about 15 %. At the veto radius where KO1's edge effect is gone (1.6 R_h) the error goes from
0.68 / 0.62 to 0.57 / 0.52 of the law (canonical / alt). A 3 sigma call needs about 0.47. A veto test would land as NO POWER
by construction, so none was frozen.

## The question it would have answered

KO1's host-free late types show an outer amplitude of -0.19 +- 0.39 at the frozen veto radius and 0.13 +- 0.68 at 1.6 R_h,
while the same lenses read 1.5 to 1.6 of the law in the middle and inner windows. If a disc carries the law's field out to
Mpc radii the outer bins should read about 1.5 too; if it does not, about 0 to 0.1. Separating those at 3 sigma needs an
error of about 0.47 or less, and at 5 sigma about 0.28, at a veto radius where the tapered edge no longer biases the bins.

## What was computed

- KO1's host rule (a pool galaxy at least 0.3 dex more massive inside F R_h), with two line-of-sight rules: KO1's
  photometric window (230 Mpc), and a hybrid: where lens and candidate both have a good DESI redshift, a velocity window V
  (1000 or 1500 km/s) decides; otherwise the photometric window does.
- Error forecast sigma = c / sqrt(I), with I built from the pair weights and the law's model cells only, and c calibrated
  on fourteen errors KO1 already published.

Checks (both pass): the photometric samples rebuilt here have exactly KO1's sizes at 1.0, 1.3 and 1.6 R_h (40,667, 25,708,
17,335; zero lenses differ from KO1's scan); one constant reproduces all fourteen published errors (max / min 1.24).

## Numbers

Error on the late-type outer amplitude, in units of the law, canonical / alt:

| Veto radius | KO1's photometric veto (published) | Hybrid veto, all KiDS | Only lenses with a DESI redshift | Upper bound: those lenses if every unresolved candidate lay elsewhere |
|---|---|---|---|---|
| 1.0 R_h | 0.39 / 0.36 | 0.34 / 0.31 | 0.60 / 0.55 | 0.42 / 0.38 |
| 1.3 R_h | 0.49 / 0.45 | 0.45 / 0.41 | 0.74 / 0.67 | 0.44 / 0.40 |
| 1.6 R_h | 0.68 / 0.62 | 0.57 / 0.52 | 0.89 / 0.81 | 0.47 / 0.43 |

(V = 1000 km/s; 1500 km/s differs by 0.01 to 0.02. The forecast for KO1's own samples reads 0.37, 0.51, 0.66 canonical.)

Late-type lens counts at 1.6 R_h: 2,649 (KO1), 3,557 (hybrid), 1,380 (DESI redshift only), 6,747 (upper bound).

## Why the gain is small

- DESI DR1 covers 49 % of the lenses' sky (89,344 of 181,477), all in KiDS-North.
- BGS Bright stops at r = 19.5 and the lenses run to r = 20: 29,934 lenses (16 %) have a good redshift, 12,219 of them late.
- Inside the coverage, 70 % of pool galaxies brighter than r = 19.5 have a good redshift. At 1.0 R_h, 13,383 of the DESI
  lenses still have a photometric host that spectroscopy cannot rule on.
- Spectroscopy rescues 5,518 lenses at the frozen radius (1,973 late) and removes 65 whose host the photometric window
  missed.

## What does have power

1. **Model the neighbours instead of vetoing them.** That keeps all 93,398 late-type lenses instead of 2,649. It is lane
   KO2 (`closure_2026_11_09/KO2_kids_own_field_by_type/`, criteria frozen at 59e3c9ee9a, run by another session); its own
   design toy expects an error near 0.19 on its primary ratio. Once it lands, the DESI redshifts on disk can place its
   neighbours in the covered half as a bracket (its stated limit L3, chance projections). Nothing new is needed on disk.
2. **More shear on the DESI area.** DES Y3 (`DESY3_metacal_v03-004.h5`, 312,037,859,376 bytes, per CFG316's criteria) and
   HSC Y3 (needs an account). A rough scaling, with the overlap areas CFG316's criteria quote as provisional (716.8 and
   440.6 deg2 against 448.2 for KiDS) and source densities quoted from memory and not checked, gives about five times the
   KiDS-on-DESI weight: 0.89 would become about 0.4, and the complete-spectroscopy bound 0.47 about 0.2. The disk has
   3.7 GiB free. Nothing was fetched and no download is requested.

## Limits

- Masses stay photometric (LePhare at the photo-z) even where a DESI redshift exists.
- The forecast assumes weight-limited errors; the calibration supports that to 25 %.
- It forecasts errors only. Central values are unknown by construction.

## Files

`ko3f_forecast.py` (about 10 s, single thread), `ko3f_forecast.out`, `ko3f_forecast.json`. Inputs were on disk before the
script was written: KO1's staged inputs and DESI DR1 `BGS_BRIGHT_full_HPmapcut.dat.fits` (fetched 2026-10-03 by CFG316).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
