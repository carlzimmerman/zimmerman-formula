# CFG569 FETCH_LOG

All from the ALMA science archive data portal (base URL https://almascience.nrao.edu/dataPortal/<file>), public QA2 products, fetched 2026-10-09 (UTC times 14:03-14:11) with the owner's approval ("swing both"; the minimum set only). Stored in campaign_fresh_gravity/_external_data/cfg569/ (git-ignored). Pre-download gate: 60 GiB free (>= 30 required). Throughput test on two small files: ~2.4 MB/s on the 22.6 MB file; the bulk ran at ~12-17 MB/s (total ~8 min), well under the 6 h cap. All byte counts equal the archive DataLink sizes in kurvs15_product_file_list.csv. NOT fetched: the 28.8 GB full-resolution Molina cube, any raw/ASDM tar, the Molina cont pb image.

| file | bytes | sha256 |
|---|---|---|
| member.uid___A001_X133d_X7a8.cdfs_31127_sci.spw25_27_29_31.cont.I.pb.tt0.fits | 584640 | 5cbbf538129c18bc2032561f6b7a7217e2989c0723f6577ece53b4b9d2a0cd23 |
| member.uid___A001_X133d_X7a8.cdfs_31127_sci.spw25_27_29_31.cont.I.tt0.pbcor.fits | 581760 | 72a1dee8cd635c47d479ed83fded46750ad4fee3e3b6273e4669e1e7e30f4d64 |
| member.uid___A001_X133d_X7a8.cdfs_31127_sci.spw29.cube.I.pb.fits.gz | 90867844 | 5b4cdcd7715c66ccb4321f71288a27598b9b2fb0040b6c08e54ab515af97e279 |
| member.uid___A001_X133d_X7a8.cdfs_31127_sci.spw29.cube.I.pbcor.fits | 273205440 | 5654d4c424a3ad69dd2bd66d7f5e57238a1fee4310619ade6c25b2f338b2c6da |
| member.uid___A001_X133d_X7ac.cdfs_31127_sci.spw29.cube.I.pb.fits.gz | 22586369 | 81fcfe0450e7093e3fe974aa3dd252cd86a4a64da579648567f18c51dc3b9a80 |
| member.uid___A001_X133d_X7ac.cdfs_31127_sci.spw29.cube.I.pbcor.fits | 69410880 | f5b1159dc4aeda676ff7a9d36f6142492a403cc07a490368d632849c72d6f723 |
| member.uid___A001_X1465_X137f.CDFS_31127_sci.spw23.repBW.I.pb.fits.gz | 1367972800 | 07470cae26f97d4a86aa79e0f4242919ea40fae11f6ffe31557d3f36d8705b63 |
| member.uid___A001_X1465_X137f.CDFS_31127_sci.spw23.repBW.I.pbcor.fits | 4758678720 | b58cc76cf447240c679f37525143f193337dc66490141033f9fa5aa945f2e315 |
| member.uid___A001_X1465_X137f.CDFS_31127_sci.spw23_25_27_29.cont.I.tt0.pbcor.fits | 39352320 | 85bcbd9d6b1bf021203252ae6e14306268e703bfbe7f98396e1dd356c9407d83 |

Derived locally (not fetched): the three pb .fits.gz files (Ibar B3, Ibar B6, Molina) were gunzipped beside the originals by the script.
