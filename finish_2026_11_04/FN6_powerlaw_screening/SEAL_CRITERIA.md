# FN6 seal for Gaia DR4: frozen criteria

Committed alone, before the seal is generated. The owner said "Seal it" (2026-11-04): seal FN6's wide-binary prediction for the window points before Gaia DR4 (2 December 2026, provisional), as CW1 did. `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`, CW1's seal and the D2 note are not edited. This seal adds rows for FN6's window only; the bare law's own DR4 rule (D2 law-first) is unchanged. kappa = 1/2 FITTED. Not theory closed. A window is a description, not a derivation.

## What is sealed
From `fn6_wb.json` (FN6's run, 9fd0447628), per footing and window point (canonical 3, alt 9):
- the screening length at 1 Msun, L(1 Msun), and r_M;
- gamma_r at s = 1, 2, 3, 5, 7, 10, 15, 20, 30 kAU;
- the frozen DR4 pipeline's gamma_inf and its spread over four realisations. The pipeline is the one CW1 used, SHA-256 7c884e0e0a4cb9cb5d6280d558cf64c829974ed14143a90261bd6a6fbf3007c9, imported read-only;
- the same pipeline's Newtonian value: canonical 0.9919, alt 0.9794.

## Decision rule, frozen now
DR4's measured gamma_hat through that pipeline is compared with each window point. sigma_tot = sqrt(0.0276^2 + spread^2), where 0.0276 is the registered error (sigma_fit 0.019 plus sigma_sys 0.020, N = 30,000; FN2's `fn2_dr4.out` row (a)) and spread is the point's own.
- **EXCLUDED** if abs(gamma_hat - gamma_inf) > 3 sigma_tot.
- **CONSISTENT** if abs(gamma_hat - gamma_inf) <= 2 sigma_tot.
- **TENSION** otherwise.

The window as a whole is EXCLUDED on a footing only if every one of its points is.

## Declared now
Most canonical points sit within 2 sigma of Newton's pipeline value. So DR4 can exclude them only if it finds a boost, not by finding Newton. The alt points at p = 0.45 predict a boost, gamma about 1.21, so a Newtonian DR4 excludes those.

## Output
`fn6s_seal.py` writes `SEALED_PREDICTION_DR4.md` from `fn6_wb.json`, and its SHA-256 to `SEALED_PREDICTION_DR4.sha256`. Both are committed before DR4 and never edited after.
