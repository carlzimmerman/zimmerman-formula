# NV2 Amendment A2, 2026-11-04: POST-RESULT disclosures, written after controls 3-4, the SPARC and X-COP E1, Step 0 and the coverage / sign-test run, before NV1's base controls (control 1-2) and any fit

No label, tolerance, gate, seed or control changes. Everything below is disclosed as run.

1. **Download mechanics (no change to the cones).**
   - A plain dot-product cone scan timed out on the archive. Each query therefore also carries `dec BETWEEN dec_c ± θ_q`, a band the cone already implies, so the archive can use its dec index. The rows are the same cone.
   - The archive cancelled several queries ("operation was cancelled"). The script retries, and a second run resumed after the first stopped at A3266, keeping the 7 cones already written. Their hashes are recomputed in the log, but their first-run links were not kept.
   - Every cone's row count equals its COUNT(*): 70,879 rows in all, 69,026 unique, 7.09 MB.
2. **Step 0 bug, first run.** The first `lenses` run marked non-isolated lenses by their index inside a 4000-lens chunk instead of their index in the lens list. It gave 769,192 isolated (99.5 %). That run was stopped. Its log is kept as `run_lenses_bugged_first_run.log` (gitignored, like all logs), and its number enters nothing. The fix is one line (`i0 +`).
   - **As run after the fix: 486,584 isolated (62.9 % of 773,192 lens candidates) against B21's 259,383 ± 5 %. Step 0 FAILED.**
   - Lenses are graded NOT COMPUTABLE, as frozen.
3. **Control 4 (photo-z fidelity), as frozen:**
   - Model A (KiDS, σ_z 0.02, every source perturbed) gives Spearman 0.386, so KiDS-bright E1 is **NOISE-DOMINATED**. That alone also makes the lenses NOT COMPUTABLE.
   - Model B (2MPZ) gives 0.998, so 2MPZ E1 is usable.
   - **Model B is weak as frozen.** The 2M++ `ks115` test sources all have Ks ≤ 11.5, where 2MPZ is 99 % spectroscopic, so the test barely perturbs them. 2MPZ's faint sources (Ks 11.5-13.9) have spectroscopic fractions of only 0.30-0.76.
   - An added check, mine, run after the result and reported but not gated: every source perturbed at σ_z = 0.015. It gives Spearman **0.425**, below 0.5. Under that worst case, 2MPZ E1 would read noise-dominated too.
   - The per-cluster Monte Carlo spread on the real cones is small (0.002-0.11 dex), because spectroscopic 2MPZ sources and MCXC clusters carry the field. The gate stands as frozen, and the caveat goes beside every X-COP E1.
4. **X-COP self exclusion uses the observed redshift** (spectroscopic, or photometric), fixed across Monte Carlo draws. The criteria did not say which; this is the choice made.
5. **Lens E1 is computed and reported UNGRADED,** as frozen for a failed Step 0.

κ = ½ FITTED; not theory closed.
