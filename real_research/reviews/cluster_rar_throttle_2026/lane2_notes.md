# Lane 2 -- Tian+2020 CLASH cluster RAR vs Branch B throttle break (y_c=2.894)

## Data (Tian, Umetsu, Ko et al. 2020, ApJ 896, 70 = arXiv:2001.08340)
- 20 CLASH clusters; g_obs from weak+strong LENSING, g_bar from X-ray gas + BCG stars.
- Fit: `ln g_tot = 0.51(+0.04/-0.05) ln g_bar - 9.80(+1.07/-1.08)`.
  Slope 0.51 = clean single power law, paper explicitly reports NO breaks/multiple slopes.
- Consistent with deep-limit `g_tot = sqrt(g_dagger g_bar)`.
- **g_dagger = (2.02+/-0.11)e-9 m/s^2** (~21.6x canonical a0; ~17x galaxy 1.2e-10).
- Intrinsic scatter 14.7(+2.9/-2.8)% = 0.059 dex. Radii 14-600 kpc.
- **g_bar range (verbatim): max 2.1e-10 (BCG core), min 1.3e-11 (intracluster).**

## The decisive geometry
- Break at g_bar = y_c*a0 = 2.71e-10 (canonical) / 3.27e-10 (alt).
- Tian max g_bar = 2.1e-10 => y_max = 2.24 (canonical) / 1.86 (alt).
- **y_max < y_c=2.894 on BOTH footings.** The break sits ABOVE the top data point
  (factor 1.29 short canonical, 1.56 short alt). Throttle T(y)=1 everywhere Tian
  measures => Branch B is identically plain framework MOND across the whole cluster RAR.

## Sensitivity (even if range were reached)
- Peak throttle break ~0.017 dex (n=1, y~4-6). vs 0.059 dex intrinsic scatter,
  0.1-0.3 dex systematic floor. Signal/scatter=0.27, signal/floor=0.06-0.17.
  Need ~0.01 dex at y~5-10 -- no cluster-RAR set reaches it.

## Deficit
- g_dagger=21.6x a0 => framework MOND under-predicts cluster g_obs by sqrt(21.6)=4.6x
  deep (0.4-0.62 dex across Tian's range). Known shared-MOND cluster deficit.
- Throttle inactive below y_c => adds ZERO in-hand cost; the predicted worsening at
  y>y_c is beyond Tian's reach. Deficit is shared-MOND, not Branch-B-specific.

## Verdict: UNDERPOWERED / OUT-OF-RANGE
Not BREAK-DETECTED (throttle inactive in-range), not FLAT-DISFAVORS (no-break fit is
consistent with Branch B, which also predicts no break below y_c). Branch B cluster-viable
in the same deficient way as plain MOND.
