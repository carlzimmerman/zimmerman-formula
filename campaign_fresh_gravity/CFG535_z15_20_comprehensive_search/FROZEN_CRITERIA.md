# CFG535 FROZEN CRITERIA: comprehensive z ~ 1.5-2 search for crisp flat-a0 tests

Frozen 2026-10-09, committed alone before any forecast or test script exists and before any number below is computed.

**Framework terms.** a0 = kappa c sqrt(G rho_DE), kappa = 1/2 FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt), never pooled. FLAT: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) = 1 for w = -1. Rival: a0 proportional to H(z), taken as the CFG223 curve `H(z)` in `HZQ_common/hzq_core.py` (LAWS["H(z)"]; x2.37 at z 1.5, x3.03 at z 2.0). LCDM-with-feedback enters only through the record's effective-a0 PROXY curve (LAWS["PROXY"]), reported, never a pass line. Kernel: nu_mono (`hzq_core.NU`, the standing owner choice) primary; the plain kernel nu(y) = 1/(1 - exp(-sqrt y)) as a variant. Baryon discs: `hzq_core.disc_v2` (thin Freeman disc, R_d = R_e / 1.678). Cold energy mass is required by the framework; its amount is free. Not theory closed.

**Disclosures before freezing.** I have read (in this session, before writing this file) the READMEs or ledger rows of CFG52, CFG90, CFG164/166/170, CFG190, CFG216/233, CFG270, CFG385, CFG386, CFG400/401, CFG567, the KURVS memory note, `prep_2026/highz_tfr_fork/FORK_RESULTS.md` (Ubler+17 bTFR scored as two published bins: WASH), `data_assembly/HIGHZ_SOURCE_TABLE_2026-09-29.md` and the `high_z_tf_tables` README. I have looked at the column headers and row counts of `ubler2017.csv` (135 rows, z 0.60-2.6) and counted the KMOS3D catalogue rows at 1.4 <= z <= 2.1 with log M* >= 9.8 (141). I have NOT computed any velocity residual, slope or forecast. Abstract-level literature facts seen: Lang+17 stacked slope -0.26 (+0.10/-0.09) in V/V_max per R/R_turn (0.6 < z < 2.6, 101 galaxies); Tiley+19 stacks flat or rising to ~6 R_d (normalised by R_d); KGES (Tiley+21) CDS table A1 has z, M*, R50, v2.2c, sigma0c for 288 galaxies at 1.2-1.8 (ReadMe read, table not fetched).

## 1. Inventory inclusion rules
A source enters INVENTORY.md if it reports galaxy kinematics (rotation curve, a velocity at a stated radius, a stacked curve, or an integrated Tully-Fisher velocity) for galaxies with z in [1.4, 2.1], or a stack/sample whose range contains that band, published 2009-2026, found on disk, in the record, or on public abstract/listing/ReadMe pages. For each: N in band, observable, gas route, table access (on disk / public small table / figure only / proprietary), and TRIED status.

## 2. "Untried by the record"
A (source, statistic) pair is TRIED if any committed lane (CFG*, prep_2026, real_research) computed an a0 or law comparison on it (found by grep of the source name, arXiv id or data file). Census-only appearances (inventoried, not scored) are UNTRIED. A new statistic on a tried source is UNTRIED-STATISTIC and is flagged as such.

## 3. Ranking metric
Z_eff = (separation between FLAT and H(z) predictions of the statistic) / sqrt(sigma_stat^2 + sigma_shared^2), forecast with mocks in which **every mock draws its own shared nuisance values** (gas amount and its z-tilt, stellar-mass offset, gas extent, pressure prescription and sigma_0), so a shared offset is never averaged away. Reported per footing. Classes: CRISP Z_eff >= 3 in both footings; USEFUL 2-3; WEAK < 2. Ties broken by access: on disk > public small table > figure only > proprietary / new observations.

## 4. Forecasts (run on on-disk inputs; no data are scored)
Forecast sample: KMOS3D catalogue rows (`data_assembly/kmos3d_phibss/kmos3d_catalog.csv`) with 1.4 <= Z <= 2.1, LMSTAR >= 9.8, RHALF > 0; R_e = RHALF x `hzq_core.kpc_per_arcsec(Z)`. Baryons per galaxy: stellar disc (M*, R_e) + molecular gas disc, mu = Tacconi+18 scaling 10^(0.06 - 3.3 (log(1+z) - 0.65)^2 - 0.41 (log M* - 10.7)) (CFG90's form), gas scale R_gas = f_R R_e. HI not added (disclosed). V_c^2 = R g_N nu(g_N / a0(z)); V_rot^2 = V_c^2 - alpha(R) sigma_0^2, floored at (10 km/s)^2 (the floored fraction is reported).
Shared nuisances per mock: dlog M* ~ N(0, 0.15); dlog mu ~ N(0, 0.25); f_R ~ U(1, 2); sigma_0 = 45 + N(0, 8) km/s; pressure P_B alpha = 2R/R_d (Burkert+10, = 3.36 R/R_e) or P_K Kretschmer+21 alpha(x) = -0.146x^2 + 1.204x + 1.475, x = R/R_e - 1, each with probability 1/2. P0 (no pressure) is reported as a scenario only.
- **F1 stacked outer shape.** S = median over galaxies of dlog V_rot / dlog R between 2.2 R_d and 6 R_d (the Tiley-type stack range; Lang's ~4 R_e is close to 6.7 R_d). sigma_stat(S) = 0.05 for a stack of ~100 (variants 0.03, 0.10).
- **F2 population self-calibration.** A = median log10 V_rot(2.2 R_d) given the masses (the BTFR-like amplitude). sigma_stat(A) = 0.01 dex. Joint (A, S): each law's nuisance-marginalised (A, S) cloud (400 draws) approximated as a 2-D Gaussian plus stat covariance; 400 mocks per truth (FLAT and H(z)), each with its own nuisance draw and stat noise; Delta chi^2 = chi^2(wrong) - chi^2(true). Report the median Delta chi^2, the fractions above 4 and 9, and Z_eff = sqrt(median Delta chi^2) for A only, S only and joint. Rationale: S constrains M_b / a0, A constrains M_b a0 in the deep regime, so a shared gas offset partly cancels in the joint statistic.
- Both footings; kernel variant nu plain; seed 535.
- Hand estimates (forecast): HE-F1 Z_eff(S only) < 2 in both footings (pressure and gas extent dominate); HE-F2 the joint Z_eff exceeds A-only by >= 30% but stays < 3.

## 5. On-disk test T1: within-sample delta(z) slope of the Ubler+17 KMOS3D bTFR sample (UNTRIED-STATISTIC)
The record scored Ubler+17 only as two published bin offsets (prep_2026 fork lane) and as part of CFG52/CFG90's pooled feasibility count; no within-sample redshift-slope test exists (the analogue of CFG216 for RC100).
- **Data:** `data_assembly/high_z_tf_tables/ubler2017.csv` (135 rows; identical to `real_research/data/kmos3d_ubler2017.csv`). R_e from the KMOS3D catalogue by CFG90's rule (nearest in (dz/0.002, dlogM*/0.02), distance <= 1), RHALF x `hzq_core.kpc_per_arcsec`.
- **Prediction:** stars M* and gas M_bar - M* as two discs with the same R_e (variant: gas at 1.5 R_e); V_pred,law = max over R in [0.5, 5] R_d of V_c (matching the table's "maximum modelled circular velocity"). delta_law = log10(V_obs / V_pred,law). Laws FLAT, H(z); PROXY reported.
- **Statistic:** OLS slope b_law of delta_law on z over all matched rows; galaxy bootstrap 10,000, seed 535 -> sigma_boot.
- **Shared systematic:** a gas z-tilt M_gas -> M_gas 10^(t (z - z_med)), t one-sigma 0.19 dex per unit z (the size of CFG233's RC41-vs-PHIBSS gas tilt); sigma_sys(b) = |b(t=+0.19) - b(t=-0.19)| / 2. sigma_tot = sqrt(sigma_boot^2 + sigma_sys^2).
- **Power gate (decides before any lean):** Pi = |b_flat - b_rival| / sigma_tot(b_flat). DIAGNOSTIC only if Pi >= 3 in all four cells (2 footings x 2 kernels). Otherwise NON-DIAGNOSTIC: leans are printed descriptively and no law statement is made.
- **If DIAGNOSTIC:** a law is DISFAVOURED if |b_law| / sigma_tot > 3 in all four cells; CONSISTENT if < 2.
- Subset z in [1.3, 2.1]: same statistic, descriptive only.
- **Controls:** C1 135 rows, z split 65 / 24 / 46 at 1.3 and 1.8. C2 the matched KMOS3D IDs equal CFG90's KMOS3D set in `cfg90_per_object.csv` and R_e agree within 3% (cosmology conventions differ). C3 noiseless: V_obs := V_pred,FLAT gives b_flat = 0 to 1e-10; V_obs := V_pred,H(z) gives b_rival = 0 to 1e-10.
- **MUTATE M1 (written to separate outputs):** V_obs -> V_obs x V_pred,H(z) / V_pred,FLAT. DETECTED if b_flat(M1) - b_flat(main) equals (b_flat - b_rival)(main) within 5%. A non-detection is reported, not repaired.
- Hand estimates (T1): HE-T1a Pi < 3 in every cell; HE-T1b |b_flat - b_rival| in 0.02-0.05 dex per unit z; HE-T1c sigma_sys >= sigma_boot.

## 6. README verdict rule
CRISPY TEST AVAILABLE ON DISK (+ result) if T1 is DIAGNOSTIC or any on-disk statistic is CRISP; CRISPY TEST NEEDS DOWNLOAD if a forecast for a downloadable candidate is CRISP in both footings (list what, URL, size, test); otherwise NONE, with the best USEFUL candidates listed. A lean is not a detection; no sentence says the data favour the framework.

Compute: nice -n 10, <= 2 threads. No downloads. Lane folder only.
