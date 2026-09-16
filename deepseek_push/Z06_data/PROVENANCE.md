# PROVENANCE -- Z06 tSZ data pull (2026-09-16)

## Fetched products (Z06_data/)

### ACT DR6 + Planck Compton-y map (Coulton et al. 2024; 2307.01258)
- file      : ilc_actplanck_ymap.fits
- url       : https://lambda.gsfc.nasa.gov/data/suborbital/ACT/ACT_adv/Compton_y_maps/ilc_actplanck_ymap.fits
- size      : 1783298880 bytes (1.78 GB)
- sha256    : 0f47b211d98a09ad67b60cbfe5f76c08366393db96903722a8a3caf67171f423
- delivered : 2024-03-21 (LAMBDA)
- projection: Plate Caree (RA---CAR / DEC--CAR), 43200x10320 px,
              0.5 arcmin/px, ICRS; lowpass ell < 17000
- units     : y (dimensionless); slope measurements unit-invariant
- citation  : Coulton, Madhavacheril, Duivenvoorden, Hill et al. 2024, PRD (arXiv:2307.01258);
              Naess et al. 2025 (ACT DR6 maps)
- source    : NASA LAMBDA (HEASARC/GSFC), ACT (AdvACT) Compton-y Map repository

## Mirrors / alternate branches
- Planck MILCA/NILC all-sky y-maps (IRSA release-3 tarball, 12.25 GB):
  https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/component-maps/foregrounds/COM_CompMap_Compton-SZMap_R2.02.tgz
  (covers A2319, dec +43.9 deg, outside the ACT footprint)

## Verification note
- size checked against the server Content-Length (1783298880 bytes);
- sha256 computed on the downloaded file (above);
- a mismatch of either is a FAIL of the pull, not a rounding note.

## Fetch script
- Z06_data/fetch_tsz_maps.sh -- the exact curl commands (resumable, -C -).
