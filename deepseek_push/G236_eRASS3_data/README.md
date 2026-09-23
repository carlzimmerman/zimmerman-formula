# G236 — eRASS:3 (eROSITA DR2): the a0(z) virial-temperature sharp null + cluster-sector z-invariance

**Home of the next free G-number's lane.** The cluster sector's account book: `CLUSTER_CLOSEOUT.md` (G192);
the a0(z) kernel standing: `real_research/A0Z_KERNEL_STANDING_2026-06-06.md`; waveboard rows G161 (plateau
seal), G162 (12-decade sliver), G187 (phase-boundary discriminator) name eROSITA as the instrument.

## The release (audited, files in this folder)

eROSITA DR2 = the eRASS:3 cumulative source catalogues (eRASS1+2+3, 556 days, Dec 2019–Jun 2021),
western Galactic hemisphere, catalogue-only, public since 2026-07-31 (Ramos-Ceja+2026, A&A aa60385-26,
arXiv:2607.27772; reported by phys.org 2026-09-11). Headline numbers, **all reproduced on the shipped
files by this lane**:

| paper claim | measured here | check |
|---|---|---|
| main 0.2–2.3 keV: 1,911,744 point-like + 63,796 extended | 1,911,744 / 63,796 | C04 PASS |
| hard 2.3–5.0 keV: 15,980 (15,026 PS + 954 EXT) | 15,980 / 15,026 / 954 | C01–C03 PASS |
| ~88% of LS10 counterparts extragalactic | 87.8% (1,397,905/1,591,243, `class_gal_exgal` ≥ 1) | C05 PASS |
| EXT vs PS sky populations differ | KS D = 0.046 = 8.4× the 95% critical value | C13 PASS |

Shared with SDSS DR20: ~200,000 eRASS:3 sources with high-quality spectra and robust redshifts
(Merloni et al. / Roster et al., in prep.). "Tens of thousands of clusters out to z > 1".

## The two new predictions (registered in G236_eRASS3_a0z.py, verdicts PENDING data)

**E1 — the virial-temperature sharp null (shared with flat-MOND; kills the rising rivals).**
The framework's derived law is flat below z ~ 3 (S3-05: a0(z)/a0(0) = 1 − ~3e-5·z). Through the Q001
identity σ² = √(G·M_b·a0)/2, the X-ray temperature of a cluster at fixed baryonic mass traces a0:

  **Δ log10 T_X(z) / T_X(0)|_{M_b} = 0.000** (z ≤ 1), vs **+0.134 dex @ z=0.5 / +0.216 @ z=1**
  for the Ciocan M-RISE slope (1.59e-10 m/s² per unit z, MUSE-DARK III) — separated at ~21σ / ~35σ
  with 150-cluster z-bins against the framework's own 0.076-dex floor.

Falsifier (registered): any z-bin in [0.2, 1.0] with |Δlog10 T| > 0.010 dex at ≥ 2σ AND a second
consistent bin → the derived law dies. The (1+z)^{3/2} rival is already out at 17× (Tian+2024
constant cluster offset, no z-trend — the eRASS1 leg of exactly this test; eRASS:3 gives 2.4× the
extended sample and reaches z > 1).

**E2 — cluster-sector z-invariance (framework-DISTINCTIVE).** The 2/3 temperature law (G135,
rms 0.076 dex on 31 local systems) and the dust amplitude law c_dust(M500) are constitutional —
dark mass is the scalar's stress-energy, so no z-evolution is allowed. Falsifier: α drifts > 2σ
pooled, rms > 0.100 dex at z > 0.2, or the dust law's mass slope q moves > 2σ from −0.414 ± 0.157.
LCDM's NFW concentration evolution at fixed M500 predicts a T-normalization drift of order
+0.03–0.06 dex per unit z (CITED/UNVERIFIED, calibration only).

## Re-pointed at this release (existing registrations, now with an instrument)

- **G187 phase-boundary discriminator**: any eRASS:3 system in M500 ∈ [2,3]e14 with f_dust < 0.85
  voids the sharp-saturation reading (sharp s_ph = 8–12% vs smooth ramp 13–40%).
- **G162 sliver fill**: eRASS:3 groups in log M ∈ [13.07, 13.70] must sit on the 12-decade line's
  slope 1.004 ± 0.011.
- **G161 plateau seal**: eRASS:3 supplies the 2.4× deeper extended sample for the T-profile flat
  tail at r ~ 1.5–2 R500 (eROSITA FoV 5/12 full-window).

## Honest status

- DR2 is **catalogue-only**: no T_X, no M500 in the release files. E1–E4 verdicts wait on the eRASS:3
  cluster working-group products and the SDSS DR20 redshift cross-match (the sources are already in
  hand here: main + hard + LS10 counterpart catalogues downloaded, 2.3 GB).
- The high-z "more needles than expected" SMBH-abundance result (Roster et al.) is a registered
  **NON-CLAIM** for the framework: accretion is Newtonian-scale (no a0), and the framework makes no
  abundance prediction (S3-28/S3-34). It neither supports nor kills anything of ours.
- E1's flat prediction is shared with all constant-a0 MOND (the S3-17 relabel); E2's z-invariance is
  the framework-distinctive leg.

## Files

- `G236_eRASS3_a0z.py` — the lane: 13 checks, PASS/FAIL per check, results.json. Rerunnable.
- `G236_eRASS3_a0z.out`, `G236_results.json` — this run's output and machine verdict.
- `eRASS3_Hard_v1.2.fits.gz`, `SRG_eROSITA_SDSS_CV_CATALOGUE.fits.gz` — shipped DR2 files
  (downloaded; untracked with the main/LS10 catalogues — the repo tracks work+math only).
- `eRASS3_Main_v1.3.fits.gz`, `eRASSc3_Main_LS10_Public_27Jul2026.fits.gz` — shipped DR2 main + LS10
  counterpart catalogues, present in this folder but **untracked by design** (GitHub caps packs at
  2 GiB and blobs at 100 MB; the repo's house style keeps multi-GB raw data out of history — cf.
  G114_data). Re-download from eRODat if the folder is missing them; the lane reads them by path.