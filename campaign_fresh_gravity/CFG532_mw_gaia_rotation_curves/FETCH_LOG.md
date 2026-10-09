# CFG532 fetch log

Only ONE download was made in this lane: the review's arXiv source. On 2026-10-09 the coordinator corrected the scope: only the review was approved, not the tables of the curves it cites. Raw files go to `../_external_data/cfg532_work/`, which is outside the repository.

| date (UTC) | URL | saved as | size (bytes) | SHA-256 |
|---|---|---|---|---|
| 2026-10-09 20:22 | https://arxiv.org/e-print/2608.10189 | `cfg532_work/2608.10189_src` (gzip tar) | 443,793 | 489db16ce41832290a1746e2886c0906983101e4100bac6f5a0e70b5653c9736 |
| (extracted) | — | `cfg532_work/src/MW_RC_review_corrected_6_11.tex` | 152,100 | 51cae3afd1cb2d0d9139221c093ca442301aa9145951f621dc03f1979d730379 |

- The tarball also contains the review's figure PDFs. They were not used.
- The 35-entry compilation table (`tab:rc_data`) is parsed straight from the `.tex` by `cfg532_mw_curves.py`. Control K2 checks the parse: 35 rows, 6.3–49.0 kpc.
- Nothing else was fetched. The cited curves that are not on disk are listed in README.md, so the owner can decide whether to approve them.
