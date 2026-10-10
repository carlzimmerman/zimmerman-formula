# CFG552: DES cluster stacked lensing vs the drained shell. Status: BLOCKED, the data are not public (2026-10-10). No test run, no criteria frozen, no ΔΣ read

- **Goal:** run CFG546's splashback-marginalised drained-shell fit (shell amplitude A, DK14 nuisances, both footings, 256³/512³ and CFG544-softened templates) on the published DES-Y3 redMaPPer stacked ΔΣ, with DES-Y1 McClintock+19 as a cross-check.
- **Finding:** neither data vector with its covariance is publicly released in any approved source. See `FETCH_LOG.md` for every URL, size and hash.
  - **DES-Y3 clusters (DES Collaboration 2025, arXiv 2503.13632).** The DES release page says the data vectors and chains "will be available for download here when the paper is accepted". The server's `y3kp_clusters/` holds only the redMaPPer catalog (`y3_redmapper_v6.4.22+2_release.h5`, 344 MB). That file is over the 200 MB cap, and it is a catalog, not ΔΣ.
  - **DES-Y1 (McClintock+19).** No ΔΣ table or covariance was found on the DES pages, arXiv ancillary files, VizieR, Zenodo or the authors' GitHub. The author's repositories hold code, chains, best fits, Buzzard-mock ΔΣ and semi-analytic covariance realisations only.
- **Why FROZEN_CRITERIA is not committed:** the frozen fit must use the published binning, units (physical or comoving), the corrections the authors applied (boost, miscentring, photo-z) and the covariance as released. None of these can be pinned before the product exists. The freeze is deferred to the day the data arrive, and it will still be committed alone before any ΔΣ value is read.
- **What would unblock it (owner's choice):**
  1. Wait for the DES-Y3 cluster data-vector release on the DES page (link below).
  2. Ask the authors for the Y1 ΔΣ tables and covariance by email (outreach stays in chat, not in the repo).
  3. Re-measure ΔΣ from the public DES-Y3 metacal shear catalogue plus the redMaPPer catalog. This is a new, much larger lane: the shear catalogue is ~100 GB class, the catalog is 344 MB, and it needs its own covariance (jackknife) and its own approval.
- **Forecast reminder (CFG546):** even with the data, DES-Y3 gives a Z of only ≈ 2.06 / 2.19 (canonical / alt) once splashback is marginalised. It falls below 1 with the 256³ template. A run could at best give a hint or a 2σ exclusion of A = 1 at the 512³ amplitude.
- κ = ½ is FITTED; the cold energy's mass is still required. Not "theory closed".

## Links for the owner
- DES-Y3 key-cluster release page (data vectors pending): https://des.ncsa.illinois.edu/releases/y3a2/Y3key-cluster
- DES-Y3 cluster file directory: https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/y3kp_clusters/data/
- DES-Y3 cluster cosmology paper: https://arxiv.org/abs/2503.13632
- DES-Y1 McClintock+19: https://arxiv.org/abs/1805.00039 ; analysis repository (no data vector): https://github.com/tmcclintock/DES_Y1_WL_Analysis
