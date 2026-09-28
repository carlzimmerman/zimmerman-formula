# Hub reproduction re-runs still owed

Every review lane is re-run by the hub in a scratch mirror (read-only links to the repository; outputs never touch
it) before or soon after commit, and the result is recorded in its commit or in README.md. The lanes below were
committed with the re-run PENDING because the machine was overloaded (2026-09-27). Each will be re-run when the
load allows, and this file updated.

| Lane | Commit | Why it matters | Specific risk |
|---|---|---|---|
| XR22 | 661ea3cff | the Gaia DR4 amendment will rest on its numbers | `XR22_common.py` was edited at 10:00, after lane 1's MUTATE output and during its main run |
| XR23 | 6b7ab8243 | JWST ceiling; δ_c; the T_EH98 flag | none known |
| XR26 | 68135cb7a | the CMB-lensing wall | none known (its patched CLASS is rebuilt from source by the script) |
| XR28 | a45bd96ab | the cluster cap on L | `XR28_common.py` was edited at 12:18, after the `outskirts_L` (12:07) and `hot_phase` (12:16) main runs; only the controls were re-run after it |
| XR29 | 633c161b5 | the Milky Way outer curve | none known |
| XR32 | fa341733d | the S8 result | none known |

Re-run and matched (recorded in their commits or README.md): XR11–XR15, XR14's score, XR17, XR18, XR18b, XR19,
XR20, XR21 stage 1 (controls and web channel), XR25, XR27, XR30, XR31, XR33.

## Re-run 2026-09-28: all six matched

All six were re-run in scratch mirrors with `run_repro_lane.sh`, MUTATE first, then main, sequentially. Each `.out` and results JSON was diffed against the committed copy, ignoring timing. Numeric JSON leaves were compared one by one.

| Lane | Result | Notes |
|---|---|---|
| XR22 | **matched** | Both scripts, both modes: JSON identical. The `.out` differs only in a worker count (3 vs 4) and a timing figure inside a sentence. **The specific risk is cleared:** the outputs match the committed `XR22_common.py`. |
| XR23 | **matched** | Every numeric JSON difference is a `sec` timing field. The `.out` differs in timing only. |
| XR26 | **matched** | `cmb` identical; `linear_equations` differs in timing only. `bbn`'s K3 read `nan` on the first pass, because the batch ran `bbn` before `linear_equations` and K3 reads part 1's results file from its own directory, which did not yet exist in the mirror. Re-run after part 1: `.out` identical, JSON identical except `elapsed_s`. |
| XR28 | **matched** | `controls` and `hot_phase` identical. `outskirts_L`: `.out` identical; the JSON's 1534 line differences are ordering and formatting, with zero numeric differences. **The specific risk is cleared.** |
| XR29 | **matched** | JSON identical. One diagnostic print line appears one line later. |
| XR32 | **matched** | Every `.out` and JSON identical in both modes. |

**The rule for next time:** when a lane reads a sibling part's results file, run the parts in dependency order inside the mirror.

Nothing remains pending from the table above.

## Campaign lanes CFG0, CFG1, CFG4 and CFG6, re-run 2026-09-28: all matched

These were re-run the same way, with `run_repro_cfg.sh`, a mirror of `campaign_fresh_gravity/`. The parts ran in dependency order: CFG4 galaxy_law, switch, clusters, cosmology, target; then CFG6 branches, evidence.

| Lane | Result | Notes |
|---|---|---|
| CFG0 | **matched** | JSON identical apart from `runtime_s`. One `.out` ledger line differs because it quotes the chain's README and CHAIN_STATUS, which were updated after CFG0's commit (b5bdb73e8: the L_Λ window's upper edge now reads ≥ 5, not 4.6). That is source evolution, not a change in CFG0's own numbers. |
| CFG1 | **matched** | The audit's K4 (sources tracked and clean) fails inside a symlink mirror, where git sees type changes. Checked in the real repository: all 47 sources are tracked and clean. Four sources that were "in flight" are now committed (FP24, XR34, XR35, XR24), which is time evolution. Nothing else differs. |
| CFG4 | **matched** | All five parts: numeric JSON identical apart from `seconds`; `.out` identical. |
| CFG6 | **matched** | Both parts: JSON identical; the `.out` differs only in timing. |

**The rule for next time:** a lane that audits git state (CFG1's K4) cannot be reproduced inside a symlink mirror. Run that one check in the real tree.
