# NOTE, 2026-11-15 (pre-data, text only): the sha256 of the frozen wide-binary pipeline as it stands before Gaia DR4

Written under item T1 of `OWNER_DECISION_2026-11-15b_DR4_OPEN_GAPS.md` (gap C13 of the registry map,
`closure_2026_11_12/DR4MAP_gaia_dr4_registry_map/DR4_MAP.md`). It records a hash and changes nothing: no frozen file is
edited, no amendment is filed, and no pin, scorer or cut changes. Gaia DR4 is due 2026-12-02; no DR4 byte exists.
kappa = 1/2 FITTED; not theory closed.

## What is recorded

- The pre-registration's own manifest (`PREREGISTRATION_DR4.md`, the table of frozen files) lists
  `prep_2026/gaia_dr4_prep/wide_binary_pipeline.py` with sha256
  `669fecc4b42b0f0a23c263715d45c3a56cca112af70fccdc4ed95696d53bb4ff`. That is the file as first committed on
  2026-07-16.
- The file as it stands today has sha256
  `7c884e0e0a4cb9cb5d6280d558cf64c829974ed14143a90261bd6a6fbf3007c9`. It last changed in commit 2a18b570e8 on
  2026-09-22.
- The current hash is the one pinned by `RELEASE_DAY_CHECKLIST.md` section 3 and by the release-day wrapper
  `dr4_push_2026_11_05/DP3_release_day/dr4_release_day.sh`, whose hash check logs a mismatch and fails if the file
  differs.
- The map found that "No filed amendment records the new hash." This note is that record. It is not an amendment.

## Every commit of the file, with the file's sha256 at that commit

Read on 2026-11-15 with `git log -- prep_2026/gaia_dr4_prep/wide_binary_pipeline.py` and `shasum -a 256` on
`git show <commit>:<path>`. The right-hand column is the start of each commit's own subject line.

| commit | date | sha256 (first 12) | subject begins |
|---|---|---|---|
| f617640aeb | 2026-07-16 | 669fecc4b42b | The 2026-07-16 arc: MI field theory assembled + verified |
| 3829a5747e | 2026-08-08 | 63897739c1de | DR4 pipeline: three BLOCKING fixes applied |
| 42d4864033 | 2026-08-08 | 363365163512 | DR4 items 5+6: anisotropy falsifier and gated branch WIRED IN |
| ba6bd17f5d | 2026-08-09 | ab54f07d6611 | AMENDMENT 9 FILED |
| ae030faa04 | 2026-08-11 | 09aec11a0ff0 | THE_COMPLETION v9 PUBLISHED ... + the DR4 pipeline retarget |
| 40ca6ad7ff | 2026-08-13 | 6933795edbb7 | AMENDMENT 10 FILED |
| 5a865128fc | 2026-09-06 | d87879748e4c | AMENDMENT 11 FILED |
| 371c61edd5 | 2026-09-06 | ac7dd4a2106f | DR4 readiness after Amendment 11 |
| 2a18b570e8 | 2026-09-22 | 7c884e0e0a4c | DR4 readiness re-check (2026-09-22): the pipeline caught up to Amendment 12 |

## What this note does not say

- It does not review what each commit changed, and it does not say the changes were only retargeting. The registry
  map describes the file as "retargeted after filing"; the release checklist's section 3 holds the rule for checking
  that changes are names only.
- It does not change which hash binds on the day. The wrapper's pin does, and it already carries the current hash.

kappa = 1/2 FITTED; not theory closed.
