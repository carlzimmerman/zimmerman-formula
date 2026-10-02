# AMENDMENT 19 — DRAFT, NOT FILED (written 2026-10-01; filing needs the owner's explicit go)

This is a draft. `PREREGISTRATION_DR4.md` and every `*_HASH.txt` are untouched. If the owner approves, the text below the line is appended verbatim (append-only) after Amendment 18, with a new `AMENDMENT19_HASH.txt`.

**Why now.**
- The frozen builder's stage-G correlation fetch (`fetch_correlations`, `catalog_builder/build_catalog.py`) uses the archive's asynchronous job queue. The anonymous async queue was blocked on 2026-09-29/30 (the Q1/Q3 pilots had to use synchronous queries instead).
- If the queue is blocked or congested on release day, the PRIMARY build stalls at stage G.
- A synchronous fallback was built in the release driver only, never in the frozen builder (design 6742d206d; code 795d49285 and e8dce8c78). It runs the SAME SELECT synchronously in chunks of at most 1,999 ids, because a result of exactly 2,000 rows cannot be told apart from silent truncation.
- On DR3 it reproduces the stage-G catalogue byte for byte (test_driver_corr_sync.py 8/8, four MUTATE controls biting; re-run by the orchestrator, outputs identical).
- Using it changes only how the same rows reach stage G. This amendment registers it before the data, so that its use cannot be read as a post-hoc choice.

---

> ### 🚨 AMENDMENT 19 — 2026-10-01, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **THIS AMENDMENT REGISTERS A DATA-TRANSPORT FALLBACK FOR STAGE G'S CORRELATION FETCH. IT CHANGES NO CUT, THRESHOLD, ESTIMATOR SETTING, σ_tot, DECISION ROW, SEED OR ARM.**
> **κ = ½ FITTED, NOT DERIVED.**
>
> **(a) The primary transport is unchanged.** Stage G's correlations are fetched by the frozen builder's own asynchronous query (`fetch_correlations`).
>
> **(b) The fallback.** If the asynchronous fetch fails or stalls on release day, the release driver's synchronous fetch (`dry_run_driver.py --corr-transport sync`, function `fetch_correlations_sync`) may be used instead. It:
> - issues the SAME SELECT on the same table;
> - uses at most 1,999 ids per call;
> - requires every requested id to come back, and stops otherwise;
> - sorts the returned arrays exactly as the builder does.
>
> **(c) Equivalence, required before use.**
> - The fallback may be used only if the release-day manifest records the transport, the number of calls, the number of ids and the largest chunk.
> - On DR3 the two transports gave a byte-identical stage-G catalogue (sha256 prefix 6fff64d964ebaa72) and byte-identical correlation arrays (test_driver_corr_sync.py, 8/8).
> - On release day, if both transports are available for any subset, a byte comparison of that subset is recorded. Any difference is reported, and the asynchronous result is primary.
>
> **(d) Against interest.** The DR3 equivalence used the on-disk caches served by a mock archive; the real server's synchronous and asynchronous endpoints were not compared on identical requests. This amendment does not assume they agree; it requires the manifest record in (c) and reports any difference.
>
> **Untouched:** the estimator; the cut table; the error model and σ_tot; the strictness ladder; the frozen N = 30,000; both a₀ footings; Arms A, B and C; Amendments 10–18 (including Amendment 18's seed rules and label); the primary build's frozen seeds; the pipeline's registered RNG seed. κ = ½ remains fitted.
>
> **Provenance.**
> - `prep_2026/gaia_dr4_prep/AMENDMENT19_DRAFT_NOT_FILED.md`
> - `dr4_ready_1/dry_run_driver.py` (795d49285, e8dce8c78) and `dr4_ready_1/test_driver_corr_sync.py` with its outputs
> - design `6742d206d`
