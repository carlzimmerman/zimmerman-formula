# CFG826 — does CFG824's age trend, carried to 12.5 Gyr, predict the ultra-faint dwarfs?

Criteria: `FROZEN_CRITERIA.md` (13399acac, before the script). Run: `python3 cfg826.py` (MUTATE `CFG826_MUTATE=1`). Seconds.

## Result — CLASS (canonical, primary trend, binary-corrected UFDs): **CONSISTENT**
| sample | E_UFD (ln σ_obs/σ_law) | CFG824 trend at 12.5 Gyr | z vs trend | flat (no-age) alternative | z vs flat |
|---|---|---|---|---|---|
| **binary-corrected, N = 7 (primary)** | **+0.70 ± 0.21** (+0.31 dex) | +0.48 ± 0.18 | **+0.80** | +0.15 | **+2.13** |
| same, C-ML (Υ 2.35) | +0.66 ± 0.21 | +0.40 ± 0.17 | +0.97 | +0.18 | +1.87 |
| same, alt footing | +0.66 ± 0.21 | +0.48 ± 0.18 | +0.63 | +0.15 | +1.95 |
| literature σ, N = 28 (secondary) | +0.93 ± 0.09 | +0.48 ± 0.13 | +2.86 (ABOVE) | +0.15 | +5.81 |

- The age line fitted on 28 independent dwarfs (CFG824, ages 0.5–12.6 Gyr), extrapolated to the UFDs' age, lands on the
  binary-corrected UFD excess; a no-age (flat) excess misses it at z = 2.1 in the primary (1.9–2.0 under C-ML / alt).
  This is the discrimination the criteria asked for, met in the primary only and on the 2σ line.
- With uncorrected literature dispersions the UFDs sit above even the trend (z +2.9): binaries inflate UFD σ, so the
  binary-corrected set is the primary by design.
- Per UFD (primary): Boötes I −0.08, Leo V +0.36, Hydrus I +0.46, Carina II +0.49, Reticulum II +0.97, Segue 1 +1.33,
  Willman 1 +1.39 (Willman 1 and Segue 1 are the two most debated systems).
- **Reading:** a cross-check, not support: CFG824 itself was NO SIGNAL after the M/L control. But the theory's open UFD
  excess (+0.33 dex) is now quantitatively what the dSph age trend predicts for 12.5-Gyr-old systems. H-FOSSIL is the one
  candidate that ties the classical-dSph and UFD shortfalls together. Decisive next step: CFG824b (SFH-based M/L per dwarf).

## Controls
- K1 PASS: refit slope 0.039849 = CFG824's stored slope.
- MUTATE (b = 0): the prediction equals the flat alternative (+0.147); the primary then classes UFDs ABOVE TREND (z +2.14).

κ = ½ fitted; cold energy mass required; not theory closed.

**Superseded reading (2026-10-18, CFG827):** with each dwarf's own SFH-based stellar M/L (E-MILES × Weisz+14), the
out-of-sample age trend vanishes (ρ +0.09, p 0.33). The trend here came from stellar M/L; H-FOSSIL as an age effect is not
supported. The numbers above stand as computed; only their interpretation is superseded. See `../CFG827_dwarf_age_sfh_ml/`.
