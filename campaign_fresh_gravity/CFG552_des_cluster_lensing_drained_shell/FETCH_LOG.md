# CFG552 FETCH LOG

Owner approval (chat, 2026-10-10, "swing both"): fetch the published DES-Y3 redMaPPer stacked ΔΣ tables with covariance (preferred), and DES-Y1 McClintock+19 ΔΣ as a cross-check. Public sources only, MB-scale; stop if > 200 MB or if a login or bot check stands in the way.

**Result: no ΔΣ table and no covariance was downloaded. Neither product is publicly released in any approved source (checked 2026-10-10).** Only index pages, READMEs and repository file listings were fetched. They are logged below. No ΔΣ value was read.

## Fetches (2026-10-10; index / metadata only; kept in the session scratchpad, not in `_external_data`)

| URL | HTTP | bytes | SHA-256 | what it showed |
|---|---|---|---|---|
| https://des.ncsa.illinois.edu/static/des_components/elements-built.html | 200 | 2589111 | 7819c66b39b5986e78eac48e8beeeb86883ce865a31eca4dc32b6bcde81cd43b | The DES release-site bundle (the release pages are a JS app). Y3 key-cluster page text: "The data vectors will be available for download here when the paper is accepted"; same for the chains. Catalog only: `y3_redmapper_v6.4.22+2_release.h5`. |
| https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/y3kp_clusters/ | 200 | 680 | 7425b90ffdc38d8b85a0f8a2da4e2abd8bb9090eef1c8619fadc94d7d737aa5f | holds only `data/` |
| https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/y3kp_clusters/data/ | 200 | 768 | 94fdcf6a50debcb96377bb49b4ab9f9d9e255c52f013fc401114803c57e7973c | holds only `y3_redmapper_v6.4.22+2_release.h5`, 343,740,336 bytes (HEAD; last-modified 2026-03-31). It is the cluster CATALOG, not ΔΣ, and it is over the 200 MB cap. NOT fetched. |
| https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/y3kp_clusters/chains/ | 404 | 146 | 55f7d9e99b8e2d4e0e193b2f0275501e6d9c1ebd29cadbea6a0da48a8587e3e0 | not published |
| https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/datavectors/ | 200 | 1021 | c969d83ea25a5c7e182dff111ce954959039da402c891dfd1ffdc8ebeec35990 | 3x2pt FITS only (redMaGiC / MagLim); no cluster file |
| https://desdr-server.ncsa.illinois.edu/despublic/y1a1_files/redmapper/ | 200 | 1310 | 4121e892d07d492c9e4184ec9c5df0b34639fe48ecff04e960fd487b36e44cff | Y1 redMaPPer catalog / members / randoms / zmask only; no lensing profiles |
| https://raw.githubusercontent.com/tmcclintock/DES_Y1_WL_Analysis/master/lensing_analysis/README.md | 200 | 709 | 267d925b45256d4c7c4e9f58f165acf9b6db3c90c7f55475970bbfc5093e0a77 | McClintock+19 analysis code |
| https://api.github.com/repos/tmcclintock/DES_Y1_WL_Analysis/git/trees/master?recursive=1 | 200 | 19178 | a4741a1c68c0e793a426cb52a8bec8b060bdbd826c143163942f2b76cb1505e8 | best-fit files, MCMC chains, boost chains, photo-z files. **No ΔΣ data vector and no covariance file.** |
| https://api.github.com/repos/tmcclintock/DES_Y3_redMaPPer_mass_calibration/git/trees/master?recursive=1 | 200 | 13970 | 610d2be3d1ae8ba812c10a4e507a5d6ee96c50407d41e44579844608ee7e55d4 | ΔΣ from the **Buzzard simulation** only (12 λ–z bins). These are mocks, not DES data, so they cannot be used. |
| https://api.github.com/repos/tmcclintock/Y1_SAC_Clusters/git/trees/master?recursive=1 | 200 | 6127 | 817a096be9eec17dbf7748574170a4f338447a9e090d57679ddb27e3ff25ea88 | `stackreals.tgz` (79.8 MB): realisations of the semi-analytic covariance MODEL, not the measured ΔΣ. NOT fetched. |

## Also checked, with nothing found (queries only; no files fetched)
- DES directories `y1a1_files/`, `y1a1_files/chains/`, `y3a2_files/`, `y3a2_files/chains/`, `y3a2_files/y3kp_cats/`, `other_files/paper-data/`: no cluster-lensing profiles.
- arXiv ancillary files: 1805.00039 (McClintock+19), 1710.06808 (Chang+18 splashback), 2105.05914 (Shin+21), 2503.13632 / 2503.13631 (DES-Y3 clusters): none.
- VizieR J/MNRAS/482/1352 (McClintock+19), J/ApJ/864/83 (Chang+18): "Table or Catalog not found".
- Zenodo search (redMaPPer ΔΣ, DES cluster lensing, splashback lensing DES): no DES cluster ΔΣ release.
- GitHub repository search and the `des-science` org: no cluster ΔΣ data release. `MariaElidaiana/desy1-mustar-analysis` is code only.
- No login wall or bot check was met. The products simply are not public.
