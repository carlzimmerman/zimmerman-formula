# C7_aest_class: provenance of the owner-approved CLASS download (2026-10-23 UTC)

**Approval.** The owner's words, relayed by the coordinator: "Yes: fetch class_public v3.3.4 source from its official
GitHub release into its own _external_data folder and start the native AeST CMB patch lane (derive the adiabatic initial
conditions first, validate against vanilla CLASS in the dust limit)."

**Storage.** Outside the repo, in a new empty directory: `../_external_data/class_public_v3.3.4_2026_10_22/`
(relative to the repo root). The CLASS source is not committed. Only this lane's `aest.patch` (a diff against the
pristine tree), scripts and outputs are committed.

| item | value |
|---|---|
| URL | https://github.com/lesgourg/class_public/archive/refs/tags/v3.3.4.tar.gz (served from codeload.github.com, HTTP 200) |
| retrieved | 2026-10-23T00:22:22Z – 00:22:23Z |
| file | `class_public-3.3.4.tar.gz` |
| bytes | 7995315 |
| sha256 | 35f2599f0eaa680d2f8198ddb7f70099df7c00a6c04f239c142cd8f3c420545c |
| tag check | `git ls-remote https://github.com/lesgourg/class_public.git refs/tags/v3.3.4` → e85808324f51fc694d12e3ed7439552a3c3f9540; `git get-tar-commit-id` on the tarball → the same commit |
| version string | `include/common.h`: `_VERSION_ "v3.3.4"` |

**Builds.** Two copies of the extracted tree were made under `../_external_data/class_aest_build_2026_10_22/`:
`class_vanilla/` (unmodified source, built with `make -j2 class`) and `class_aest/` (patched; built the same way).
The pristine extraction `class_public_v3.3.4_2026_10_22/class_public-3.3.4/` is never built or modified.
Only CLASS's documented C build (`make class`) and the resulting `class` executable are run; no Python wrapper, no
other script from the tarball. Runs: `OMP_NUM_THREADS=1 nice -n 15` (CLASS honours OMP_NUM_THREADS in
`include/parallel.h`).

**Other inputs (already on disk, see C2 PROVENANCE):** SZ21 TeX source and figure PDFs
(`../_external_data/aest_papers_2026_10_22/src_2007.00082/`); the Fig. 1 benchmark parameters were read from the text
layer of `Cl_TT_EE_with_residuals.pdf` with `pdftotext -layout`. Planck plik-lite and low-ℓ data from
`../_external_data/cobaya_2026_10_22/packages/` through C2's numpy likelihoods.
