# Gaia DR4 dress rehearsal (2026-09-29): the frozen pipelines are intact and run

Read-only. No file in `prep_2026/gaia_dr4_prep/` was edited. The pipelines ran in a scratch copy made with `git archive HEAD`, because running in place would overwrite frozen outputs.

- **The pre-registration text is unchanged since Amendment 16.** sha256(PREREGISTRATION_DR4.md) = 97aa97c4…d3ad25, equal to Amendment 16's recorded "after" hash.
- **The freeze manifest's banked scripts match their 2026-07-16 hashes:** `stx_dipole_template.py`, `wb_dr4_prereg_framework_curve.py`, `stx_target.py` and `stx_inpop_recipe.py`.
- **`wide_binary_pipeline.py` does NOT match the manifest's 2026-07-16 hash (669fecc4…).** It was changed openly through filed amendments: the Amendment 9 retarget, Amendments 10 and 11, and the 2026-09-22 catch-up to Amendment 12.
  - Its current hash, 7c884e0e…3007c9, equals the reference that RELEASE_DAY_CHECKLIST §3 records (commit 2a18b570e8). The checklist's catalog_builder hashes also match.
  - **Documentation gap, for the owner:** no filed amendment records the pipeline's current hash; only the checklist, a procedure file, does. A skeptic checking the manifest on release day would see a mismatch. An appended amendment recording 7c884e0e… as the pipeline under which DR4 will be scored would close the chain. That is the owner's call; nothing was changed.
- **Both reproduction commands exit 0 in today's environment:** `python3 wide_binary_pipeline.py --dry-run` and `python3 stx_dipole_template.py`.
  - The dry run ends GATE VERDICT: PASS (linearity, injection recovery, null, sigma consistency).
  - Both outputs are identical to the committed `wide_binary_pipeline.out` and `stx_dipole_template.out`, apart from the committed file's trailing exit-code line.
- **Still open, unchanged by this rehearsal:** RELEASE_DAY_CHECKLIST §0 items C (variant (c) not implemented), D (no join code) and E (the NSS tables). A and B were resolved by Amendment 16.

κ = ½ stays fitted. DR4 can test B's survival but cannot confirm B over ΛCDM or Newton (CFG63).
