# KL1 PART B AMENDMENT PB1: how Part B's frozen criteria are read on the KiDS-Legacy files (committed alone, before any Part B number)

Part B criteria d26939ed4f. TEST lane; adopts nothing. **kappa = 1/2 FITTED; not theory closed.** Footings never pooled.

**Timing, disclosed.** Written after the tarball was fetched and unpacked (`FETCH_LOG_PARTB.md`), its README and xi+- `.ini`
files read as text, and the xi+- FITS file's structure listed (extension names and sizes, header keys, the first rows of xiP,
the n(z) normalisation, the covariance's positive-definiteness). No model has been compared with the Legacy data; no Part B
chi^2, p or sigma8 exists. Part A's rows were still running; none of their values had been seen.

**What the release holds, and how each frozen item is read on it** (all from the release's own files):

1. **Data.** `data/KiDS_Legacy_xipm.fits`: xiP and xiM, 6 tomographic bins (21 pairs) x 9 angular bins (189 + 189 points), the
   378 x 378 COVMAT (xiP then xiM), NZ_SOURCE (6 bins, Z_MID 0.025 to 5.925 in steps of 0.05) with SIG_E_i and NGAL_i in its
   header.
2. **Angular bins.** Edges `geomspace(2, 300, 10)` arcmin, from the pipeline's `xip_binned` / `xim_binned` (theta_min 2,
   theta_max 300, ntheta 9; the FITS ANG values are their geometric centres). The model is averaged over each bin by CFG592's
   theta-weighted sub-bin rule (as for KiDS-1000), not by the release's pair-count weighting; this is a disclosed limit.
3. **Published cuts.** `keep_ang_xip = 2 300`, `keep_ang_xim = 4 300` (the pipeline's `scale_cuts`).
4. **Redshift prior.** Six decorrelated shifts with unit Gaussian widths about the means in `KiDS_Legacy_priors.ini`
   (`nofz_shifts`: 2.5374, -2.44484, -1.37982, -0.494275, 1.40234, 6.26323); the shifts in z are L x, where L is the lower Cholesky
   factor of `Nz_covariance.txt`. This is KiDS-1000's convention in CFG592 (`dz = L @ x`, n(z) moved as n(z - dz)).
5. **Shear bias.** The pipeline has no shear-bias module (the modules list is read as text), so the uncertainty sits in the
   covariance, as KiDS-1000's "with_m_bias" file did: no shear-bias parameter.
6. **Alignment.** One NLA amplitude (CFG592's), as frozen. The release's fiducial mass-dependent alignment model is not used.
7. **KB1's "n(z) that integrate to 1 per bin".** The file stores histogram weights per Delta z = 0.05 bin, so the check is that
   the weights sum to 1 per bin within 0.01. Reported beside it: the fraction of each bin's n(z) beyond z 3.5, where CFG592's grid
   ends; the loader renormalises on that grid, as it does for KiDS-1000.
8. **MB2's mapping.** KiDS-1000's five prior-mean shifts in z (L_K1000 x mu_K1000) are given to the Legacy bin of nearest mean
   redshift. Legacy's decorrelated means are then replaced by L^-1 of those shifts, and the arm is read as frozen (>= 0.5 width
   move of the Legacy best sigma8 under B1's settings).
9. **B2's area** is fitted from the Legacy covariance by Part A's A2 rule. Reported beside it as context: the effective area
   967.4 deg^2 that Wright et al. 2025 quote (a web read, PROVISIONAL).

**Nothing else changes.** No row, line, label rule, known answer tolerance (other than item 7's reading) or MUTATE arm is altered.
