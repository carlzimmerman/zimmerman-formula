# ZN1 AMENDMENT A2 (committed before any ZN1 snapshot exists at z = 0.5, 0.25 or 0)

1. **Kernel.** The continuation uses `../ZK1_fast_force_kernel/`'s compiled force sum, verified against `x48_zoom.accel` by ZK1's K1 and K2, under ZK1's rule: no switched run is graded until ZK1's K3 passes. The six runs that had started with numpy resume from their checkpoints.
2. **More seeds.** ZK1 cuts a run from days to about half an hour, so seeds 1–9 at 10¹³ and 10¹⁴ now run, 18 in all. Argon flagged three seeds as a weak point. All finished seeds enter the stack. A mass with fewer than 6 finished seeds makes the lane UNDECIDED.
3. **[NOISE-LIMITED]** is now: 200 bootstrap draws of the seeds at each mass, regraded on the median shape; appended if the headline class holds in under 68 % of draws. Three separate single-seed grades would no longer be the right test with nine seeds.
4. **10¹² reported, not graded:** seeds 1–9 of A3 continued to z = 0 too, for the same read-outs and for SPARC's path later.

5. **K2 corrected.** The frozen limit, 2 % at x ≥ 0.05 on one sampled NFW, sits below the sampling noise: about 550 particles lie inside x 0.05, which is 4.3 %. The first run read 3.0 % and failed on that. K2 is now the mean over 20 samples within 1 %, with R₂₀₀ within 1 %. It reads no ZN1 data.

6. **No fair-share R₂₀₀.** For a few gas-poor systems, (1 + R_nat) M_b/V never reaches 200 ρ_c, so the frozen rule has no R₂₀₀ for them. They take MA1's budget M₂₀₀ and are counted in the output.

Everything else in `FROZEN_CRITERIA.md` and `AMENDMENT_A1.md` stands.

κ = ½ FITTED. Not theory closed.
