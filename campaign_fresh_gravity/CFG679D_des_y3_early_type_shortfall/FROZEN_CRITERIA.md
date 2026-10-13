# CFG679D FROZEN CRITERIA: does the KiDS isolated early-type inner shortfall replicate in DES Y3?

Status: FROZEN 2026-10-13, committed alone, before any DES lensing number and before the KiDS twin (section 4) was run. Lane id:
CFG679D (block CFG670-679 used up; CFG679 = another chat's mechanism contract; suffix D avoids a collision without taking a new block). Nothing below may change after a lensing number is seen; departures go in the README, dated.

Standing settings: a0 = kappa c sqrt(G rho_DE), kappa = 1/2 FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) m/s^2, scored
separately, never pooled. Kernel nu_mono (cfg100_lib). The cold energy's mass is required (no particle). RAW DATA + framework-native:
no environment term, no stripping, no HOD, no LCDM mass function in any verdict. Not "theory closed"; nothing here says the data favour
the framework. Compute: nice 10, <= 2 processes, <= 4 GB RSS, memory guard (cfg679_lib.guard), no PM job.

## 1. The quantity
eps = Delta M(<r) / M_pred(<r) in a band of g_bar bins, as the GLS amplitude of the stacked own law profile o with E = 0:
eps = o^T W (d - o) / o^T W o, sigma = (o^T W o)^-1/2, W = (C_band / h)^-1, h = (50 - n - 2)/49 (Hartlap, 50 jackknife patches).
- o = LAW_RTA "full" (law + baryon point mass M_gal to r_ta,law; CFG503 kids_Md / kids_fin, cfg100_lib read-only), per lens group
  (0.01 dex in log M_gal x 0.03 in z), stacked with the data's per-lens bin weights.
- M_gal = M* (1 + f_cold), f_cold = 10^(-0.69 log M* + 6.63) (the record's convention, CFG96).
- Bins: CFG96's 15 g_bar bins (1e-15 to 5e-12 m/s^2, g_bar = G M_gal / R^2). Bands as CFG531: K-in = bins 12-14, K-mid 9-11,
  K-out 6-8, K9 = 6-14. **Primary band: K-in.** K9 and the others are reported.
- This differs from CFG531, whose model added an LCDM-built environment term E and stripping. That E is excluded by the 10-10 raw-data
  rule, so CFG531's number cannot be reproduced on DES. Hence the KiDS twin (section 4).

## 2. DES lens sample (defined before measuring)
- Catalogue: `DESY3_stellar_mass_catalog.hdf5` (ra, dec, z, mstar = log M*). Magnitudes g, r, i from DES Y3 GOLD 2.2 (SOF
  corrected magnitudes; if those names are absent, the GOLD 2.2 default model magnitudes, chosen from the column list before any lens
  is selected), matched by row or by coadd id / position (< 0.5").
- Cuts mirroring KiDS (CFG96): r < 20, 0.20 < z < 0.50 (KiDS used 0.10; the DES catalogue starts at 0.20), log M* < 11.0.
- Isolation f30 (CFG96 rule, verbatim adaptation): a lens is isolated if no pool galaxy (same catalogue, r < 20, 0.2 < z < 0.5) with
  log M* > log M*_lens - 1 lies within 3 Mpc comoving transverse (angle 3/chi_lens) with |Delta chi| < 30 Mpc; chi with H0 = 70,
  Om = 0.3 (CFG96's DC). The pool is truncated at z = 0.2 (DES) instead of 0.1 (KiDS); DES photo-z scatter differs from KiDS ANNz2;
  both are stated, not corrected.
- Early / late: KiDS typ = rest u - r > 2.0 (LePhare). DES has no u: within each (z 0.05) x (log M* 0.1 dex) cell, the reddest
  fraction f_E(cell) in observed g - i is early, with f_E(cell) = the KiDS f30 early fraction in the same cell (cells with < 20 KiDS
  lenses: the KiDS f30 early fraction of that z slice).
- **Primary DES sample: mass/z-matched.** Each DES lens of class c in cell k gets weight w = N_KiDS,c(k) / N_DES,c(k) (KiDS f30
  counts; DES cells empty in KiDS get 0). Reported: unweighted.
- Lenses must lie inside the downloaded source footprint (all metacal row slices used; section 3).

## 3. DES sources and estimator
- Sources: metacal unsheared ra, dec, e_1, e_2, weight; fiducial selection and tomographic bin from `index/select_bin1..4`.
- Only bins whose n(z) mean exceeds z_l + 0.2 are used for a lens at z_l (mirror of KiDS's z_B > z_l + 0.2; bin means 0.336, 0.521,
  0.741, 0.936 from the Y3 fiducial nz_source).
- <Sigma_crit^-1>_b(z_l) = integral of n_b(z_s) Sigma_crit^-1(z_l, z_s) (physical, H0 = 70, Om = 0.3 as CFG96).
- Response: R_b = mean (R11 + R22)/2 of selected sources of bin b on 20 random metacal chunks; selection response from the
  select_1p/1m/2p/2m lists on the same chunks if present, else neglected (disclosed).
- Per lens, per bin k: WG += w_s Sinv e_t, WW += w_s Sinv^2 R_b; e_t = -(e_1 cos 2phi - e_2 s sin 2phi), phi from (Delta RA cos dec,
  Delta dec), s = +1 or -1 fixed by the SIGN CONTROL below (not by the analysis sample).
- **Primary DES estimator:** random-subtracted and boost-corrected: DeltaSigma = B (lens) - (random), B_k = (sum_lens WW / sum_lens w_l)
  / (sum_rand WW / sum_rand w_r). Randoms: 5 per lens, uniform in the footprint (HEALPix nside 512 cells holding selected sources),
  each assigned a lens's (z, M_gal, weight) at random. Reported: no boost; no random subtraction (the KiDS-twin-like estimator).
- Covariance: 50 jackknife patches (5 dec bands x 10 RA quantiles of the lenses), Hartlap.
- **SIGN CONTROL (independent of the analysis sample):** lenses with log M* >= 11.2 (excluded from the analysis by log M* < 11),
  R = 0.3-2 Mpc: s is the sign that makes their stacked tangential ESD positive. Its amplitude is reported (bright-sample sanity).

## 4. The KiDS twin (comparator)
The section-1 estimator on KiDS f30 (cfg110_perlens WG / WW, lr_lenses, cfg96_isoflags, the June 50 patches), early (typ 1) and late.
- **Primary comparator for the ladder: the KiDS twin, f30 early, K-in, same footing.** Reported: the twin at z > 0.2, and CFG531's
  committed early K-in eps (+0.538 +- 0.193 canonical, construction A; alt from its JSON), labelled "with LCDM-built E".
- Control K-T1: the twin's own tables equal CFG503's committed LAW_RTA full_moster table (1e-6 relative) where on disk.

## 5. Verdict ladder (per footing; DES primary sample and estimator; early types, K-in)
Let eD +- sD (DES), eK +- sK (KiDS twin), sC = sqrt(sD^2 + sK^2).
- **(R) REPLICATES** if eD > 0 at >= 2 sD AND |eD - eK| <= 2 sC.
- **(S) KiDS-SPECIFIC** if |eD| <= sD AND |eD - eK| >= 2 sC.
- **(L) LOW POWER / NOT DIAGNOSTIC** otherwise.
If the footings differ: FOOTING-DEPENDENT with both. Reported with the same rules: K9; the early - late difference (DES vs KiDS twin;
jackknife of the per-patch difference, max with quadrature); the ladder against CFG531's committed value; the unmatched DES sample;
the no-boost and no-random estimators.

## 6. Controls
- C1 cross shear: GLS amplitude of DeltaSigma_x against o in K-in and K9 has |Z| < 3 (early and all).
- C2 random-point signal: chi2 of DeltaSigma_rand against 0 over the 15 bins, p > 0.001 (reported if it fails, with its size vs the
  lens signal).
- C3 SIGN CONTROL positive at >= 3 sigma (otherwise the lane stops: no detection, no verdict).
- C4 K-T1 (section 4).

## 7. MUTATE (CFG679_MUTATE=1, separate outputs)
- M1 (must not return R): every source shear rotated by a seeded random angle; eps must be consistent with -1 (|eps + 1| <= 2 sigma)
  in K-in and K9, and the ladder must not read R.
- M2 (must bite): own profile = baryons only (Newtonian point mass): eps_N(K9, all DES isolated lenses) > 0 at >= 3 sigma (the
  survey detects mass beyond the baryons). If M2 fails the lane reads LOW POWER whatever section 5 gives.

## 8. Outputs
`cfg679_download.py` (resumable, per-piece SHA-256 log), `cfg679_kids_twin.py`, `cfg679_des.py`; `.out`, `_results.json`, `_MUTATE.*`;
README with the verdict copied from JSON; LEDGER row before `| CFG680 |`. Data only under `_external_data/cfg679_des/` (gitignored).
