# Q6_v3_class: provenance of the Khronon CLASS builds (2026-10-23)

No download. The pristine CLASS v3.3.4 tree is C7's owner-approved one
(`covariant_push_2026_10_22/C7_aest_class/PROVENANCE.md`): `../_external_data/class_public_v3.3.4_2026_10_22/class_public-3.3.4/`
(repo-relative), tarball sha256 35f2599f0eaa680d2f8198ddb7f70099df7c00a6c04f239c142cd8f3c420545c. It is never built or modified.

| item | value |
|---|---|
| C7's AeST patch applied first | `covariant_push_2026_10_22/C7_aest_class/aest.patch`, sha256 acb780fe6d76f7765912638634ec594f03ea175e7cdb9edfbc4587d03887e34e (`patch -p1`, clean, no offsets) |
| this lane's patch (pristine → Khronon tree) | `khronon.patch`, sha256 cee6498a9aac8a259515066b0e6898aa0bc3cea99151e1289e4706ebec855155 (321 added, 7 removed lines) |
| mutate patch | `khronon_MUTATE.patch`, sha256 94064613069d3f0321b5a0d2623df670d9f91c8194fad3c054f20d34b721a97b (sign of θ + metric_continuity in the khronon δ′) |
| what differs from C7's built tree | only `background_aest_K()` (C7 lines 683–752), `perturbations_aest_rhs()` (C7 lines 31–74) and the sector's IC block (C7 lines 5525–5543, AMENDMENT A2.2); checked by `q6_validate.py` V_prov |
| builds | `../_external_data/class_khronon_build_2026_10_23/class_khronon/` and `class_khronon_mutate/`, each a fresh copy of the pristine tree made by `q6_make_patch.py`, built with `OMP_NUM_THREADS=1 nice -n 19 make -j1 class` (logs `build_class_khronon*.log` there) |
| `class_khronon/class` sha256 | 3ccb50b235cb4fe7b530d1f194827d4d20a8dec70347a500f6cf203c15024dc7 |
| `class_khronon_mutate/class` sha256 | 36014556bec36d252fc90ca6e6c490dc55c132ab614bf6038b749d2358b1cac4 |
| pristine reference binary | C7's `../_external_data/class_aest_build_2026_10_22/class_vanilla/class`, sha256 0d77bfa291546e4bce66724454899322e5f4026eb61ae546558da4528237853e (its source tree re-checked equal to pristine by V_prov) |
| in-process `classy` (K0b only: F3's background-A P(k)) | classy v3.3.4 (the same one F3 used) |

Run files go to `../_external_data/class_khronon_build_2026_10_23/runs_validate[_MUTATE]/` and `runs_native[_MUTATE]/`
(not committed). Only CLASS's documented C build and the `class` executable are run; no script from the tarball.
Likelihood data: Planck plik-lite and low-ℓ through C2's numpy re-implementation (C2 PROVENANCE), read-only.
