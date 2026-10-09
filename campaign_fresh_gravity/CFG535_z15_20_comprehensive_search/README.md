# CFG535: comprehensive z ~ 1.5-2 search for crisp flat-a0 tests. VERDICT: NONE (no crisp test on disk or one download away)

**Ledger line:** CFG535 (owner chat 10-09): search + scoping of z 1.4-2.1 kinematics for FLAT vs a0 ~ H(z). 19 on-disk and 7 public sources inventoried; untried: Lang+17 / Tiley+19 stacks, KGES table A1 (43 KB), the on-disk KMOS3D H-band z 1.3-1.8 cubes (170 rows, never fitted), Ubler+17 within-sample delta(z). Forecasts with shared nuisances drawn per mock: stacked outer shape Z_eff 0.45-0.51, stack x amplitude self-calibration 0.15-0.53, amplitude alone 0.33-0.55, all WEAK in both footings; on-disk T1 (Ubler delta(z)) NON-DIAGNOSTIC (power gate Pi 0.54-0.64 < 3). The binding wall at z ~ 1.5-2 is the outer pressure-support prescription for shapes and the gas calibration for amplitudes. kappa fitted; not theory closed.

Criteria `FROZEN_CRITERIA.md`, committed alone first (**bd4eef97a**). Scripts: `cfg535_t1_ubler_dz.py` (T1 + MUTATE), `cfg535_forecast.py` (F1, F2), `cfg535_posthoc_calibration_needed.py` (POST HOC, labelled). Outputs `*.out`, `*_results*.json`. Inventory and ranked shortlist: `INVENTORY.md`. Nothing downloaded; seconds of CPU at nice 10, 2 threads.

## What is new against the record
1. **Inventory gaps found:** the KMOS3D **H-band z 1.3-1.8 cubes are already on disk** (`../_external_data/kmos3d/cubes relative to the repo root`, 739 cubes in all; CFG270 fitted only the 195 K-band z >= 1.9 ones). Lang+17 and Tiley+19 stacked curves were cited but never scored. KGES table A1 (288 galaxies at 1.2-1.8: M*, R50, v2.2c, sigma0c) is a 43 KB CDS table, same pipeline as the on-disk KROSS/SAMI table. Nestor Shachar+25 (zC406690, z 2.2) gives a ring + bulge mass model for a galaxy whose exponential-disc fit broke CFG400/401.
2. **Why stacks do not escape the wall (F1).** At the forecast sample (141 KMOS3D galaxies, z median 1.61, log M* median 10.37, R_e median 3.4 kpc, Tacconi mu median 1.0), the stacked log-slope of V_rot between 2.2 and 6 R_d is, at central nuisances, FLAT -0.104 / H(z) -0.024 with Kretschmer pressure and FLAT -0.397 / H(z) -0.216 with Burkert pressure (canonical, nu_mono). **The pressure prescription moves the stack slope by 0.19-0.29, more than the law separation (0.17-0.20 in the nuisance-averaged means).** Shared-nuisance spread of S is 0.35-0.42 against a separation of 0.17-0.20: Z_eff 0.45-0.51 in every cell. Both laws comfortably make a falling stack (Lang's fall) with Burkert pressure, so a falling stack does not discriminate. Outer y at 6 R_d: 0.6-0.7 (FLAT) vs 0.23-0.28 (H(z)), i.e. both near the deep regime, where shapes converge.
3. **Population self-calibration (F2)** (shape constrains M_b / a0, amplitude M_b a0): with the frozen priors the joint statistic does not beat the amplitude alone (Z_eff joint 0.15-0.53 vs A-only 0.33-0.55; HE-F2 missed). POST HOC (not frozen): with the pressure law known and gas and M* known to 0.10 dex, joint Z_eff 1.55-1.78; with every calibration at 0.05 dex and the gas extent known, 2.25-2.39, still below 3 at sigma_stat(S) = 0.05. A CRISP stack test would need a known pressure correction, ~0.05 dex baryon calibration and several hundred in-band discs traced to 6 R_d.
4. **T1, Ubler+17 within-sample delta(z) (129 of 135 matched to catalogue R_e; C1-C3 pass):** b_FLAT -0.075 / -0.072, b_H(z) -0.096 / -0.095 dex per unit z (canonical / alt, nu_mono, gas at R_e); separation 0.020-0.023 against sigma_tot 0.037 (bootstrap 0.014, gas z-tilt 0.034-0.035). **Power gate Pi 0.54-0.64: NON-DIAGNOSTIC; no law statement.** Descriptive only: both laws over-predict V increasingly with z (T_FLAT -1.95 to -1.99, T_H(z) -2.89 to -2.94 sigma_tot); a linear read of the committed tilt sensitivity (post hoc) puts the gas z-tilt that zeroes b at about -0.40 dex per unit z for FLAT and -0.60 for H(z), against CFG233's measured-gas tilt of -0.19 +- 0.14. The z 1.3-2.1 subset (n 29) has the opposite sign (b_FLAT +0.10), descriptive. Gas at 1.5 R_e: Pi 0.85-0.96, same class.

## Ranked shortlist (forecast power, both footings; details in INVENTORY.md)
| rank | test | data | Z_eff canonical / alt | class |
|---|---|---|---|---|
| 1 | stack shape x amplitude self-calibration | own in-band stack from the on-disk H-band cubes + KGES | 0.34 / 0.53 (post hoc, calibrations known: 1.6-2.4) | WEAK |
| 2 | stacked outer shape | Lang+17 / Tiley+19 stacks or own stack | 0.47 / 0.51 | WEAK |
| 3 | Ubler+17 within-sample delta(z) | on disk | Pi 0.54 / 0.62 (run) | NON-DIAGNOSTIC |
| 4 | KGES same-pipeline amplitude | KGES table (43 KB) | 0.41 / 0.55 | WEAK |
| 5 | zC406690 ring re-model | arXiv 2503.00839 | not forecast; one object at z 2.2 | n/a |

## Downloads (none approved; for the owner's go only, none is CRISP)
| what | source | size | enables |
|---|---|---|---|
| KGES table A1 | CDS J/MNRAS/506/323 (`tablea1.dat`) | 43 KB | z ~ 1.5 same-pipeline amplitude vs KROSS/SAMI; sigma0 for a pressure term; members for an own stack. Forecast WEAK |
| Lang+17 stacking table + stack points | arXiv 1703.05491 (HTML ~0.3-1 MB; PDF ~5 MB for figure digitisation) | ~1-6 MB | F1 / F2 on the published stack. Forecast WEAK |
| Tiley+19 stacked curves | arXiv 1811.05982 PDF | ~5-10 MB | F1 with R_d normalisation. Forecast WEAK |
| zC406690 ring paper | arXiv 2503.00839 PDF | ~10 MB | re-model of CFG401's falling curve with a ring geometry (single object) |
| KGES cubes | hosting not confirmed | ~1.5 GB if hosted | own stack at 1.2-1.8; overlaps KURVS |
No download is needed to fit the on-disk H-band cubes; that would be a new frozen lane (CFG270 machinery), class D (stars only), and by F1/F2 it cannot be crisp either.

## Controls, hand estimates, disclosures
- T1: **C1 PASS** (135 rows, 65/24/46). **C2 PASS** (matched IDs identical to CFG90's 129, R_e within 3%). **C3 PASS** (noiseless slopes 0 to 1e-10). **MUTATE M1 DETECTED** in all 8 cells (the injected rival boost moves b_FLAT by exactly the main-run separation); this is an injection-propagation check and close to tautological, it does not show power.
- Hand estimates: HE-T1a hit (Pi < 3 everywhere), HE-T1b hit (separation 0.020-0.030), HE-T1c hit (gas-tilt systematic exceeds the bootstrap). HE-F1 hit. **HE-F2 MISSED** (the joint statistic does not reach 1.3 x the amplitude-only power in every cell).
- F2 uses a 2-D Gaussian approximation to each law's nuisance cloud; the pressure mixture is bimodal, so some S-only Z_eff come out slightly negative (the narrower rival cloud is penalised). The approximation is disclosed, not repaired; it cannot turn a 0.5 into a 3.
- HI is not added in the forecasts; Ubler's tabulated M_bar is used as given in T1 (its gas route is the paper's, not verified). The PROXY (LCDM effective-a0) curve sits between the two laws in every statistic: no statistic here separates LCDM-with-feedback either.
- The posthoc script imports and re-runs the frozen forecast (its JSON is rewritten byte-identically; md5 checked before and after).
- Literature facts come from abstracts, arXiv listing pages and one CDS ReadMe (all PROVISIONAL); ADS and VizieR HTML pages refused the fetcher. A full ADS listing sweep was not possible.

## Reading
The z ~ 1.5-2 window has no crisp test on disk or one small download away. Shape statistics (stacks) are limited by the outer pressure-support prescription, amplitude statistics by the gas calibration, and their combination by both; no published sample measures pressure and gas well enough. This agrees with CFG386, CFG567 and the KURVS front. The crisp route stays the sealed predictions (CFG571: U4_27928 public 2026-11-06, GS4_24110 public 2026-11-28) and the CFG567 observing specification (low-V discs with an inner JWST/AO anchor and resolved CO). A lean is not a detection; nothing here favours or excludes FLAT, H(z) or the PROXY.

kappa = 1/2 FITTED. Footings 9.3603e-11 / 1.1312e-10, never pooled. Cold energy mass required, amount free. Not theory closed.
