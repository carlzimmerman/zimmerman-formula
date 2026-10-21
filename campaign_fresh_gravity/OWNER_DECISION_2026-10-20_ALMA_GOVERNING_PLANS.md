# Owner decision, 2026-10-20 (dated note; no frozen file edited)

**Decision:** for the two sealed ALMA tests, the ORIGINAL frozen scoring plans govern:
- U4_27928 (public 2026-11-06): `CFG806_u4_27928_scoring/FROZEN_CRITERIA.md`, frozen by commit 1bf70683b (committed alone, before any
  download; sha256 bc56aa71…). Its header line "DRAFT, not yet committed" is stale: the committed file is the frozen plan.
- GS4_24110 (public 2026-11-28): `CFG809_gs4_24110_ci21_scoring/FROZEN_CRITERIA.md`, frozen by commit 966d50a87.

**Consequences, stated now so they are not decided on release day:**
- The later AG5 plan (`argon_push`, FROZEN_SCORING.md, 7ea94d2ae) does NOT govern these two scores. It may be reported alongside as a
  secondary reading, labelled as such, with no verdict weight.
- As in CFG571/CFG806/CFG809, a single disc is a demonstration: no model is excluded by one disc. The THEORY_CANONICAL_2026-10-14 §2
  "kills it" column is read through these plans (no single-disc exclusion).
- Scoring uses the CFG942 harness (`CFG942_alma_scoring_readiness/cfg942_u4.py`, `cfg942_gs4.py`), which reads the frozen plans without
  changing them; its selection-aware G1 noise default (adopted on mock data, before any real data) and the other ambiguities listed in
  CFG942's README NOTE remain open for a separate dated owner decision before 2026-11-06.

κ = ½ fitted; cold energy mass required; not theory closed.
