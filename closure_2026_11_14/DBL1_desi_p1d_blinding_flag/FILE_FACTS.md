# DBL1 file facts (item 1 of SCOPE.md; from the files only)

Script `dbl1_file.py` (reads the archive at `_external_data/desi_dr1_p1d_qmle/raw/data_points.tar` and the folder
`_external_data/desi_dr1_p1d_qmle/ext/`, both relative to the repository root; writes nothing). Output `dbl1_file.out`.
Run: `python3 -I -B dbl1_file.py > dbl1_file.out`. One process, seconds, light.

## The archive

- 30 members: 25 figure text files (`fig_*.txt`) and 5 FITS files (the brief said three; there are five):
  `best_fit_arinyo.fits`, `cov_diag_inflation.fits`, and three P1D tables, `desi_y1_baseline_...`,
  `desi_y1_snr3_...` and `desi_y1_xe_..._qmle_power_estimate_contcorr_v3.fits`.
- The archive's MD5 checksum on disk (`33d7fc21bfd3d745ed71a0bbe80ca433`, computed with `md5 -q`) equals the one the
  Zenodo record 10.5281/zenodo.16943723 lists for its only file `data_points.tar` (see SOURCES.md). So the archive is,
  byte for byte, the paper's published data-point release.
- The two files under `ext/` (`cov_diag_inflation.fits` and the baseline table) are byte-identical to the archive members
  of the same name.
- Packaging oddity: the member named `fig_10a_bF.txt` (65.8 MB) is not text. Its first bytes are a tar header
  (`./PaxHeaders/fig_10b_ratio.txt`), so it looks like a nested tar archive packed under that name. It plays no part here.

## The three P1D tables (baseline, snr3, xe)

Each has the same six HDUs: an empty primary; `P1D_BLIND` (binary table); `SYSTEMATICS` (binary table); `COVARIANCE`,
`COVARIANCE_STAT`, `COVARIANCE_SYST` (images, 1020 x 1020; 765 x 765 for xe; header `IS_BD = False`).

- `P1D_BLIND` header keywords beyond the FITS structure keys: `NZ = 12`, `NK = 85`, `BLINDING = 'desi_y1'`,
  `VELUNITS = True`, `EXTNAME = 'P1D_BLIND'`. No keyword carries a date, a code version, a blinding seed, an amplitude,
  or an "unblinded" flag. No comment text on any keyword.
- Rows: 12 redshift bins z = 2.2 ... 4.4 (xe: 9 bins, 2.2 ... 3.8) times 85 wavenumbers, k = 0.00025 ... 0.0527 s/km.
- Columns (units from the header; meaning from the values, labelled "appears"):
  - `Z`, `K1`, `K2`, `K`: bin redshift, k bin edges and centre (s/km).
  - `PINPUT` (km/s): appears to be the input fiducial power given to the estimator.
  - `PFID` (km/s): appears to be the fiducial power as used in the estimate; median PFID/PINPUT = 1.010; 8 rows with
    PFID = 0 at the highest k for z 2.2 and 2.4.
  - `ThetaP` (no unit given; values in km/s): appears to be the estimator's deviation from the fiducial. In 681 of 1020
    baseline rows, PFID + ThetaP equals PRAW - PNOISE to 1e-6.
  - `PRAW`, `PNOISE` (km/s): appear to be the raw estimate and the noise term subtracted from it.
  - `PLYA` (km/s): the measurement the record reads. It is not PRAW - PNOISE and not PFID + ThetaP: median
    PLYA/(PFID + ThetaP) = 0.965 (1st to 99th percentile 0.43 to 1.00), as the file name's "sb1subt" (side-band
    subtracted) and "contcorr" (continuum correction) would lead one to expect. Sample: z 3.0, k 0.00975 s/km,
    PLYA = 20.66 km/s.
  - `E_PK` (km/s): total error; E_PK^2 = E_STAT^2 + E_SYST^2 to 5e-16.
  - `E_STAT`, `E_SYST` (km/s): statistical and systematic errors; `E_SYST` equals the `SYSTEMATICS` table's total.
  - `PSMOOTH` (no unit given): appears to be a smooth curve of the same size as PLYA (median PLYA/PSMOOTH 0.958).
- `SYSTEMATICS` columns: `Z`, `K`, `E_DLA_COMPLETENESS`, `E_BAL_COMPLETENESS`, `E_RESOLUTION`, `E_CONTINUUM`,
  `E_CONTINUUM_ADD`, `E_NOISE_SCALE`, `E_NOISE_ADD`, `E_SYST`. No blinding column.
- No column, extension or keyword holds a second ("unblinded" or "blinded") version of the power. Every power column
  shares one scale, so a blinding applied as a factor to the data would leave no trace inside the file.

## The other FITS members

- `best_fit_arinyo.fits`: 12 binary tables `Z2.2` ... `Z4.4` with columns `k`, `p1d`, `model`, `cov_init`, `cov_inf`
  (no units, no blinding keyword). Looks like the paper's model-fit inputs and outputs.
- `cov_diag_inflation.fits`: a primary image of 1020 numbers, no keyword beyond the FITS structure keys.

## What the figure files can and cannot tell

- `fig_8a_qmle.txt` (z 2.4, 2.6, 2.8; 195 rows, all on the table's (z, k) grid): columns `z k ratio err`. For every
  row, err/(1 + ratio) equals the table's E_PK/PLYA to 2.8e-17. So the figure was built from exactly this table's
  PLYA and E_PK, divided by some reference curve that the file does not name. **Tells:** the table is the very
  measurement the published Figure 8 plots. **Cannot tell:** whether a factor was applied to the data, because a
  common factor cancels in this test and the reference curve is unknown.
- `fig_8a_fft.txt` (204 rows): the companion FFT measurement on a different k grid (0 rows on the table's grid). Same
  form, different estimator; it cannot be compared row by row with the table without the reference curve.
- `fig_8b_edr.txt` (80 rows, 54 on the grid): the early-data measurement in the same ratio form. Its fractional errors
  differ from the table's by up to 0.031, as expected for a different data set. It could test the amplitude against
  an earlier, independently published measurement only if the reference curve were known; it is not, so it cannot.
- `fig_9_eboss_dr1_dla.txt` (34 rows, z 2.2 and 2.4, eBOSS k grid): `smooth_ratio` runs from about 0.13 at the
  lowest k down to about 0.0 to 0.01 at k near 0.01 s/km, with "Small DLA" and "Sub-DLA" template columns. It reads as
  the DESI-to-eBOSS excess and its explanation. The eBOSS table is not on disk, so this lane cannot recompute the
  ratio from `PLYA`; with eBOSS it would be an amplitude check against an external survey.
- `fig_6b_e_jackknife.txt`: `e_qmle` matches the table's E_STAT at z 2.4 to within 0.92 to 0.99 (median 0.972); it
  concerns errors, not amplitude.
- Bottom line from the files: the table is the measurement shown in the published figures. Nothing in the files says
  whether that measurement carries a blinding; that question goes to the paper and the code (SOURCES.md).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
