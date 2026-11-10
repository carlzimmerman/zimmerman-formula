# KL1 Part B fetch log: KiDS-Legacy cosmic-shear data release

kappa = 1/2 FITTED; not theory closed. TEST lane; adopts nothing.

- **Go:** the owner, 2026-11-10, in the closure chat, answering "Download the KiDS-Legacy cosmic-shear release (125 MB, from the
  KiDS site)?": "Yes, download". Scope: this one file only. Relayed to KL1 by the closure chat.
- **Criteria first:** Part B's criteria were committed alone (d26939ed4f) before the download.
- **Page:** https://kids.strw.leidenuniv.nl/sciencedata.php links `sci_data/KiDS_Legacy_cosmic_shear_data_release.tar.gz`
  ("gzipped tarball", 125 MB: Nautilus chains, data vectors, covariance matrices, redshift distributions and CosmoSIS
  configuration files for Wright et al. and Stölzner et al.).
- **URL:** https://kids.strw.leidenuniv.nl/sci_data/KiDS_Legacy_cosmic_shear_data_release.tar.gz
- **Fetched:** 2026-11-10T19:29:23Z (UTC), one HTTPS GET with a generic client name; server Last-Modified 2025-12-15 09:42:10 GMT.
- **Size:** 131,095,396 bytes (the HEAD request's Content-Length, matched by the file).
- **sha256:** `7fdf214cbb54e51d5ca385d79a4590750d3c5dc9fe6803460bab8ed841c57f77`
- **Where:** a new, empty folder `_external_data/kl1_kids_legacy_2026_11_10/` beside the repository (untracked; nothing from it is
  committed).
- **Members (listed before extracting):** 50 entries, 42 regular files and 8 folders under one top folder
  `KiDS_Legacy_cosmic_shear_data_release/`. There are no links, absolute paths or `..` components, and no executables or scripts:
  - README.txt;
  - `data/`: KiDS_Legacy_xipm.fits, KiDS_Legacy_cosebis.fits, KiDS_Legacy_bandpowers.fits, Nz_covariance.txt, and 21 TreeCorr
    xi+- ascii files in `cosmosis_xipm/`;
  - `chains_and_config_files/` with four subfolders (xipm, cosebis, bandpowers, cosebis_plus_external), each holding a Nautilus
    chain and three CosmoSIS `.ini` files.

  Extracted in place: 269 MB.
- **Handling:** untrusted data. Nothing shipped in the tarball is run. The `.ini` files are read as text only. KL1's scripts live in
  this lane and read the data with `python3 -I`, with the paths passed as arguments.
- **Note from the release README:** the fiducial Legacy constraints use COSEBIs and band powers; the xi+- are provided "for
  completeness and for comparison with previous studies". The fiducial alignment model is mass-dependent. Part B uses the xi+- with
  CFG592's one-amplitude alignment, as its criteria freeze.
