# Owner decision 2026-11-08: run the DR3 code-path check and, if it passes, file the seed-mean NSS-off amendment

Given in the orchestrator session ("Theory completion") on 2026-11-08. The orchestrator put the question "File the DR4
seed-mean amendment after its DR3 code-path check?" Owner's words (verbatim): "Yes, check and file".

What this authorises
- Lane DP7 (`dr4_push_2026_11_05/DP7_seed_mean_check/`, criteria 1b87706e49, committed alone first) runs section 4 of the
  draft `prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-05c_DR4_SEED_MEAN_NSS_OFF_DRAFT.md` (4d8711da63) on DR3 only.
- On CHECK PASSED the orchestrator files the draft: committed alone, retitled "filed", with the owner's words quoted,
  before 2026-12-02 and before any DR4 byte exists. It supersedes only the NSS-off entry of sigma_sys(b) in D8 (a).
- On CHECK FAILED, or if the check is not complete by 2026-12-01, the draft lapses and D8 (a) stands as filed.

What it does not authorise
- No archive query. The DR4 repetition of the sweep runs on release day under the runbook, each archive step on the
  owner's go. DP7 writes the DR4 command and the cost projection only.
- No edit of any frozen file (PREREGISTRATION_DR4.md, the *_HASH.txt files, the owner-decision notes, the frozen pipeline).
- No change to bands, edges, the R rule, Newton 1.000, the Arm A anchor or the primary build's frozen seeds.

NON-SCORING: DR3 numbers are code-path tests, never results. kappa = 1/2 FITTED; footings never pooled; not theory closed.
