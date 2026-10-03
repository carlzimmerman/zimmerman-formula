# CFG315 data manifest

All data are outside git, at `../_external_data/desi_dr1_lensing/` (relative to the repository root). The full fetch record is in `FETCH_LOG.md` there.

| file | source URL | bytes | sha256 | fetched (UTC) |
|---|---|---|---|---|
| `lwb_DESI_dr1.tar.gz` (Heydenreich+25 "Lensing Without Borders" DESI DR1 release; CC-BY-4.0) | https://zenodo.org/api/records/22914838/files/lwb_DESI_dr1.tar.gz/content (DOI 10.5281/zenodo.22914838) | 46,198,472 | 641526ac9c0a6724ac8ddf0a446f3cbf852ad1adfcadd20fd4e5f8bebd34f557 | 2026-10-03T12:18:32Z |
| `zenodo_record_22914838.json` (record metadata; md5 of the tarball 0030ca0f05353b38aa61aaa7c26960f8 matches) | https://zenodo.org/api/records/22914838 | small | c36c5cbad959972bddf67ab10cf1f6dbec33806735a0a949f549c3d08f23c4b7 | 2026-10-03 |
| `arxiv_2506.21677v1.html` (+ text extract) | https://arxiv.org/html/2506.21677v1 | 713,039 | 6589b7b5149b80565f0cf484de9a921419c242f5ff98228a9116b6df2e4eb301 | 2026-10-03 |
| `extracted/` (the tarball unpacked: `ggl/`, `wp/`, `covariances/`; 4,654 entries) | n/a | about 151 MB | n/a | 2026-10-03 |

- **The GitHub repo named in the approval** (`sheydenreich/DESI_Y1_measurements`) holds no data: 3 kB and one 2024 initial commit. The paper names Zenodo and GitHub as its release hosts, so the Zenodo tarball is the approved data product.
- **Read-only use of data already on disk:** `../_external_data/kids_lensing_zsplit/KiDS_DR4_brightsample_LePhare.fits`, for the stellar-mass calibration.
