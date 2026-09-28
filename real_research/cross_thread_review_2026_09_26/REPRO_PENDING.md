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
