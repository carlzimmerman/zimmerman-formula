# L017819 / SDSS J1524+4409 — public DESI spectrum

An independent DESI DR1 observation has been recovered for the Euclid lens position, despite its absence from the local small strong-lens VAC.

| Item | Value |
| --- | --- |
| TARGETID | 39633153882587315 |
| Survey / program / HEALPIX | main / dark / 9907 |
| Target RA, Dec (deg) | 231.19026708953797, 44.16377927184152 |
| Separation from supplied Euclid coordinate | 0.307311 arcsec |
| Foreground Redrock z / zerr | 0.32022095721117494 / 0.00004154111050009619 |
| SPECTYPE / ZWARN / DELTACHI2 | GALAXY / 0 / 1961.729258287698 |
| NIGHT / EXPID / TILEID / fiber | 20220529 / 137243 / 11158 / 1350 |
| Coadd exposures / integration | 1 / 1118.4003 seconds |

The public [Legacy viewer spectrum](https://www.legacysurvey.org/viewer/desi-spectrum/dr1/targetid39633153882587315), its full DR1 target overlay, the independent NOIRLab DR1 database cone query, and the raw coadd FIBERMAP all identify the same target. Successful Data Lab response is retained in the sibling L002777 `desi_coverage/l017819_anonymous.csv`. The [public HEALPix directory](https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/healpix/main/dark/99/9907/) supplies the original products.

`target_coadd.npz` and `target_coadd_derived.fits` contain the target-only B/R/Z wavelength, flux, IVAR, MASK and RESOLUTION arrays; FITS additionally contains its FIBERMAP row. Flux units are 10^-17 erg s^-1 cm^-2 Angstrom^-1. Wavelength is in Angstrom; original grids are retained without resampling. Arrays are:

- WAVELENGTH: `(nwave,)`, with nwave 2751 / 2326 / 2881 for B / R / Z.
- FLUX, IVAR, MASK: `(1,nwave)`.
- RESOLUTION: `(1,11,nwave)`, original DESI diagonal-resolution storage, not a dense matrix or a Gaussian LSF. Use the DESI resolution convention when forward-convolving templates. Negative matrix entries are present in the original arrays and were retained.

The original 124,251,840-byte uncompressed coadd was not downloaded in full. `extract_coadd_ranges.py` read 44 HTTP206 ranges, totaling 678,078 bytes: all HDU headers, the small full FIBERMAP to establish the actual target row (141), and the target's exact array rows plus shared wavelength grids. Raw binary ranges and per-request URL/offset/Content-Range/hash provenance remain in `ranges/`; `coadd_range_manifest.json` maps the parent HDUs. Requests have 30-second timeouts and at most 2 MB per range; a response ignoring Range is rejected before reading its body. The derived FITS is explicitly a reconstructed subset, not an original archive product.

`redrock-main-dark-9907.fits` was fetched whole (262,080 bytes); its SHA256 equals the value in the archive's `healpix_checksums.txt`. The parent whole-coadd SHA256 cannot be verified from selected ranges. HTTPS identity, exact ranges, independent viewer equality, and derived internal FITS checksums provide bounded provenance, not whole-file certification.

Offline `validate.py` passed on Python 3.9.6, NumPy 1.26.4 and Astropy 6.0.1. `validation.json` records hashes, units/ranges, target separation, mask counts and checks. Finite flux values and all wavelengths agree exactly with the separately obtained official viewer arrays. Viewer NaNs exactly coincide with IVAR=0/MASK!=0; 5,19,14 masked pixels in B,R,Z. Noise differences are <5e-7 in native flux units. No fitting, masking beyond original products, flux correction, smoothing or template convolution has been applied to the saved scientific arrays.

`spectrum_check.png` is a qualitative display with two-pixel Gaussian smoothing only; `inspection_plot.py` recreates it. Broad excesses near the known-source CIII] position (4218 Angstrom) and MgII position (6185 Angstrom) are visible and qualitatively corroborate the previously established quasar source at z=1.210. Their broad profiles and foreground stellar absorption require joint modeling for numerical line measurements. This is not a blind new redshift measurement. At that z, H-beta and [OIII] are beyond the DESI wavelength range, so their absence is uninformative. No new stellar velocity dispersion is inferred here.

[Guo et al. 2026](https://arxiv.org/html/2602.13578v1), section 2.2, describes new pPXF dispersions using E-MILES templates and iterative quasar-line masks, with seven DESI DR1 systems shown in Figure 3. Root is independently auditing the reported L017819 dispersion. This extraction establishes the public data needed for that audit; it does not validate the published uncertainty, stellar-population mass, source deblending, AQUAL field solver or any full theory fit.

DESI data are CC BY 4.0. Downstream scientific publication must include the [DESI release citation and acknowledgement](https://data.desi.lbl.gov/doc/access/).
