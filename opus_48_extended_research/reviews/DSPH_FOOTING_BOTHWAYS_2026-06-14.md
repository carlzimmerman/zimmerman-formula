# Dwarf-Spheroidal Front -- a0 Footing Audit (both ways)

Date: 2026-06-14. Auditor: independent (Opus). Scope: the dSph velocity-dispersion + EFE scripts under
`real_research/` (the Fable corpus). Framework a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2 (pure rho_DE).

## What a0 the Fable scripts actually used

| script | a0 literal | operative? | M/L_V | verdict on footing |
|---|---|---|---|---|
| `real_research/predictions/door2_dwarf_spheroidals.py` (L27) | `A0 = 1.2e-10` | YES (drives every sigma) | 2.0 | CANONICAL McGaugh, NOT framework. The framework value `A0_LAMBDA` is computed at L28 and printed as "within ~20%" but NEVER used in `predict()`. |
| `real_research/predictions/door2_dsph_ultraprecision.py` | geomean band `sqrt(9.1e-11 * 1.2e-10)=1.045e-10` for the scorecard; reports framework `A0_LAM_CEN=9.36e-11` AND `A0_RAR=1.2e-10` side by side | scorecard at 1.045e-10 | 2.0 | MIXED. Framework a0 is shown but the headline median/pulls anchor on the geomean (1.045e-10), still ~12% above framework. |
| `real_research/reviews/project15_dsph_efe_thermometers.py` (L13) | `a0 = 1.2e-10` | YES (Crater II EFE) | 2.0 | CANONICAL, NOT framework. |
| `real_research/reviews/widening_lensing_bao_LG_dsph.py` (L19) | `A0 = 1.2e-10` | YES | -- | CANONICAL, NOT framework. |

So the operative a0 across the dSph front is **1.2e-10 (canonical McGaugh)**, ~28% ABOVE the framework's
9.36e-11 (framework is 22% below canonical). `door2_dsph_ultraprecision.py` is the only one that even displays
the framework value, and even it anchors its scorecard on a geomean band, not 9.36e-11.

## Direction of the footing error -- this is a (mild) FALSE WIN, not a false deficit

sigma scales as a0^(1/4) (isolated) and a0^(1/2) (EFE). Framework a0 is LOWER, so ALL predicted dispersions
DROP: isolated dwarfs 6.0% colder, EFE dwarfs 11.7% colder. Lower predicted sigma makes the **over-dispersed**
cases (where the framework already under-predicts: Sextans/Draco/UMi) WORSE, and the **under-dispersed** cases
(Leo II, Carina) slightly better. The dSph scorecard is dominated by over-dispersed outliers, so the net effect
of using the canonical (higher) a0 was to make the framework look BETTER on its worst cases. That is a
FALSE WIN to flag -- the opposite polarity from the SPARC-RAR "20% too low" false-deficit.

## The "3/8 over-dispersed at -3 to -4 sigma" verdict, re-checked at framework a0 (M/L held at 2.0)

| dwarf | canon a0=1.2e-10 pull | framework a0=9.36e-11 pull | delta |
|---|---|---|---|
| Sextans | -3.42 | **-3.73** | -0.31 |
| Draco | -3.69 | **-4.15** | -0.45 |
| Ursa Minor | -3.62 | **-4.12** | -0.50 |
| (Sculptor) | +2.87 | +1.56 | -1.31 |
| (Fornax) | +1.80 | +0.91 | -0.89 |

- The COUNT is unchanged: **3/8 over-dispersed** beyond 40% at BOTH a0 (Sextans, Draco, Ursa Minor).
  Median |log(pred/obs)| barely moves: 0.092 dex (canon) -> 0.091 dex (framework). within-40% = 5/8 both.
- The PULLS get WORSE on the framework footing: the over-dispersed tension deepens from ~-3.4/-3.7/-3.6 sigma
  to ~-3.7/-4.2/-4.1 sigma. **The verdict is robust; the framework footing makes it slightly more severe.**
- So the "-3 to -4 sigma, 3/8 over-dispersed" headline was computed at the CANONICAL a0. On the framework's
  OWN a0 it is "-3.7 to -4.2 sigma, 3/8 over-dispersed" -- the framework inherits MOND's classic Draco/UMi/
  Sextans failures and the lower a0 makes them marginally deeper. No mis-verdict; if anything the Fable text
  understated the tension by using the higher canonical a0.

## Crater II (the headline EFE "clean success", project15) re-checked

McGaugh pre-registered ~2.1 km/s; Caldwell+2017 measured 2.7+-0.3.
- canon a0=1.2e-10: sig_efe(pred) = 1.93 km/s (~2.6 sigma below measured)
- framework a0=9.36e-11: sig_efe(pred) = **1.71 km/s** (~3.3 sigma below measured)

Crater II is EFE-dominated so sig_efe ~ sqrt(a0/g_ext); the lower framework a0 makes it COLDER and slightly
FURTHER from the 2.7+-0.3 measurement. Still the right qualitative MOND/EFE signature (much colder than a
LambdaCDM 4-7 km/s NFW halo), but the framework a0 sits a touch worse than McGaugh's canonical-a0 2.1, not
better. Another mild FALSE WIN from the canonical footing.

## The M/L convention (a second, separate footing knob -- flagged both ways)

The Fable scripts use M/L_V = 2.0. The MEMORY flags Upsilon ~ 0.70 as the framework convention. Lowering M/L
to 0.70 (with framework a0) lowers M, hence sigma, hence DEEPENS every tension dramatically: 5/8 over-dispersed,
median 0.242 dex, Draco/UMi pulls -5.5/-5.7 sigma. This is NOT a fair single-knob test -- Upsilon~0.70 is the
SPARC-RAR disk M/L (3.6um), whereas dSphs are old metal-poor stellar systems for which M/L_V ~ 1.5-2 is the
standard (Fable's choice is defensible and conservative here). I report it only to be complete: the dSph
over-dispersion is a real MOND failure that gets WORSE, not better, under any framework-leaning convention
(lower a0 OR lower M/L). There is no convention in the framework's favor that rescues Draco/UMi/Sextans.

## Net

- FALSE WIN (anti-framework correction): the canonical a0=1.2e-10 (used operatively in door2_dwarf_spheroidals,
  project15, widening_lensing) made the framework's over-dispersed outliers ~0.3-0.5 sigma SHALLOWER and
  Crater II ~0.4 km/s closer to data than the framework's own 9.36e-11 delivers. On the framework footing the
  3/8 over-dispersion is -3.7 to -4.2 sigma, not -3.4 to -3.7. Retract the implicit "looks this good" framing
  tied to 1.2e-10.
- NO false deficit found on this front: the "3/8 over-dispersed" verdict is NOT a high-priest artifact; it is
  robust and in fact mildly understated by the canonical a0.
- The one honest credit to the framework: `door2_dsph_ultraprecision.py` does display the framework a0 and
  reports both anchors, and explicitly states the z=0 scorecard (successes AND failures) is SHARED with
  constant-a0 MOND and tests the VALUE of a0, not its evolution -- which is correct and fair.
