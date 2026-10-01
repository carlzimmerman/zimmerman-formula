# CFG272 stage 1 — the blind pre-flight: the four ALPAKA discs with a stellar mass are near-Newtonian at R_ext, so none can be an a₀ point; ID 24 has no point

> **κ = ½ FITTED. No velocity column was loaded; no g_obs, D, δ or s\* of any disc was formed. A forecast, not a measurement. No sentence says the data favour a law.**
> Criteria `FROZEN_CRITERIA.md` (**e06a91b8a**). Script `cfg272_alpaka_five.py` (shared `../HZQ_common/hzq_core.py`); outputs `cfg272_stageA.out`, `cfg272_stageA_results.json`.

## Bottom line
1. **All four discs with an M\* are ILL-CONDITIONED: y = g_bar/a₀ at R_ext with stars only (B0) = 13.7, 15.3, 8.2, 12.1 for IDs 13, 23, 25, 28** (ν_mono(y) = 1.050, 1.045, 1.082, 1.057). A 0.03 dex change of the baryon mass destroys the root for 13, 23 and 28 (lever not computable); ID 25 has a lever of −20. **None is drawable as an a₀ point**, and with the baryons a lower limit every row is in any case a limit. This is the conditioning theorem of **CFG240 (7b73ef6a0; Lean `T3_newton_limit` / `T3_newton_limit_a0`: for ν → 1 at large y, g_obs/g → f and the a₀ dependence disappears; the break-even table: a sample with no point below y_min = 0.1 never reaches σ(log a₀) = 0.1 dex)** in the sample: each disc is a single radius with y ≳ 8 and no deep point.
2. **The gas floor does not change the regime.** M_gas,B1/M\* = 0.075 (13: the [CI] floor α_[CI],min = 1.0), 0.074 (23), 0.204 (25), 0.502 (28), so g_bar rises by 7–50 % and y to 14.7, 16.4, 9.9, 18.1; the conventional route B2 (α_CO 4.36 for 23, 24; α_[CI] 9.7 for 13; 0.8 for 25, 28) reaches M_gas/M\* = 0.73 (13) and 0.40 (23). **ID 24 has no M\*; its gas-only floor has y = 2.2 (B1) and 12.0 (B2): a baryon lower limit made of the gas alone is uninformative: no point.**
3. **The Monte Carlo cannot recover a planted law at these y:** noiseless-world coverage (declared 10 % V error, the published inclination and M\* errors) is 0.05, 0.02, 0.28, 0.10 at 68 % and 0.79, 0.78, 0.94, 0.79 at 95 %; the rooted-draw intervals are biased high (conditioning on a root). The failure is the finding (CFG274's lesson).
4. **The inclination is the largest single geometric uncertainty of ID 13:** the adopted i_HST = 37° against i_ALMA = 24° gives a g_obs factor 2.19 (0.340 dex); ID 28's two values agree (0.012 dex); IDs 23, 24, 25 have only i_ALMA (70°, 75°, 74° ± 3–6°).
5. **Baryon knobs move g_bar** (stars at 2 R_e −0.44 for the CO-sized discs with R_e = R_ext/1.2, −0.20 for ID 28 with its dashed R_e; R_e × 1.5 −0.23 / −0.08; spherical −0.11…−0.12; ID 13 with the JWST R_e 3.34 kpc −0.12 dex), larger than the 5–8 % headroom of ν_mono(y): as in lane E, whether a root exists is decided by the baryon model.

## Decisions (the frozen map)
- **PF-D1 ESTIMATOR VALIDATED: True** (C1–C5 pass). **PF-D2 ILL-CONDITIONED: 4 of 4 with an M\*** (13, 23, 25, 28). **PF-D3 DRAWABLE: none.** ID 24: no M\*, no point.

## Controls
- **C1–C5 pass:** the C3 restated in CFG274's Addendum 1 form was frozen here from the start and **passes — all four stars-only g_bar equal CFG227's printed S3 strings exactly** (relative deviation 4.3e-5 = the file's five-digit rounding); C2 (Freeman, `gdisc` equal to CFG229's), C4 (estimator bit-equal to CFG223's), C5 (noiseless identity 2e-15). C6 is reported (fails for the ill-conditioned rows by construction).

## Hand estimates (frozen before any number; kept as they fall)
- **HE1 hit** (y ≥ 5 for all four, all ILL-CONDITIONED, none drawable). **HE2 hit** (gas floor / M\* 0.075, 0.074, 0.204 for 13, 23, 25 and 0.502 for 28). HE3–HE7 are scored at stage B.

## Disclosures
- Only baryon and geometry columns were loaded (the kinematics file and the digitised ring values are read at stage B only; the ring radii for the R_mean knob are geometry); CFG227's committed S3 `g_bar` column was read for C3 and nothing else of that file.
- The α_CO / α_[CI] routes are frozen in the criteria before any velocity: B1 (the lower limit: α_CO,min = 0.8, r_J1 = 1; α_[CI],min = 1.0) and B2 (conventional).
