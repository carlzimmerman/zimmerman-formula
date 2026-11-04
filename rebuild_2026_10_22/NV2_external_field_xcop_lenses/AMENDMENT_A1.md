# NV2 Amendment A1, 2026-11-04: after the download and the first run of control 3, before any E1 value for any system

**What happened.** The criteria say the record's SPARC E1 was built from 2M++ in catalogue mode `full`. That was my misreading: `run_pipeline.py` defaults to `full`, but the file `gext_vectors.csv` was written in mode `ks115` (Ks ≤ 11.5 everywhere, D ≤ 200 Mpc, Chae Sec. 3.1 as written). Control 3(e) caught it on its first run. Run as frozen (mode `full`), NV2's code misses the csv by up to 0.149 dex (noclu) and 0.129 dex (maxclu), and so does the record's own `GextEstimator` in mode `full` (the same numbers). The record's code in mode `ks115` reproduces the csv to 5e-6 dex on all 175 galaxies. Controls 3(a)-(d) passed on that run.

**Change.** "Catalogue mode `full`, as the record" becomes **catalogue mode `ks115`, as the record**, everywhere: control 3(e), NV2's SPARC E1 (2M++ sources, R_s = 30 Mpc) and control 4's SPARC test points. The depth scale is now reported as E1(`full`) − E1(`ks115`). Nothing else changes. No tolerance, label, gate or seed changes.

**State when written.** The 2MPZ cones are downloaded (70,879 rows, 7.09 MB; `nv2_download.json`). No E1 value has been computed for any SPARC galaxy, X-COP cluster or KiDS lens in NV2's convention. Step 0 has not run, and neither have the fidelity control, the NV1 base controls or any fit.

κ = ½ FITTED; not theory closed.
