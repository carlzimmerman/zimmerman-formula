# FS21 pre-registration: public copy (2026-11-11)

A verbatim copy of a pre-registration frozen on 2026-11-11 in the local `project_atomos` repository (criteria commit 8459498,
status-at-freeze commit ea2b1be). That repository has no remote, so this copy is the public timestamp.

**What is frozen.** The claim "Delta m^2_atm / Delta m^2_sol = Z^2 = 32 pi / 3", first committed in this repository on 2026-06-01
(`ai_slop/research/MASTER_VERIFICATION_TABLE.md`, line 96). Two fixed definitions (C31 and C32), a data rule, a kill line, and the
worth of a survival, all set before JUNO's next release.

| file | what it is |
|---|---|
| `FS21_FROZEN_CRITERIA.md` | the pre-registration. FROZEN: never edit. sha256 `b40d18f001095c71edd104e0d0f4601d70bdd095a0f424982857cb6583fbdb1c` |
| `fs21_splitting_ratio.py` | evaluator: applies the frozen reading rule to a data file; nothing tunable |
| `fs21_data_at_freeze_2026-11-11.json` | the data at freeze (NuFIT 6.0 as transcribed, PROVISIONAL; JUNO 59-day Delta m^2_21) |
| `fs21_reading_at_freeze_2026-11-11.out`, `fs21_reading_fs21_data_at_freeze_2026-11-11.json` | the reading at freeze |

**Status at freeze.** C31 OPEN, C32 OPEN; both CONSISTENT, neither decisive (precision 1.6-2.7 %).

**How to add a reading.** Write a new dated data file, run `python3 fs21_splitting_ratio.py <data.json>`, and commit both. Append
only; the frozen file and earlier readings are never changed.

**Limits, stated in the frozen file.** The test can kill the claim; it cannot certify it. A survivor is a curiosity. No mechanism
is offered. A survival does not support the gravity framework and a kill does not damage it. `targets/pmns_2025.py`, named in the
frozen file, is in the local repository; the values it supplied are in the data file here.
