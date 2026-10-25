# IC1 AMENDMENT A2 (POST-RESULT, disclosed; touches the IC2 comparator and the K3 check only)

**What happened.** The first full run (`ic1_run_INTERRUPTED_preA2.log`, kept unchanged) failed K3. I stopped it while it was
grading IC2. By then it had already printed every IC1 graded line on both footings: Step 0, the Σ_IC table, SPARC,
clusters, groups, and the per-footing IC1 verdict (IC1 INACTIVE on both). I had believed nothing was graded yet when I
stopped it. That was wrong, and this amendment is therefore post-result.

**The error.** Section 6 K3 froze "sup_x m(x)/x² for NFW equals 0.216217". That number is sup m(x)/x, the peak of the
circular velocity. For NFW, m(x)/x² decreases monotonically from 1/2 at x → 0. The peak self-acceleration is the central
value, g_max = 2πG ρ_s r_s. The script's bounded search (lower bound x = 0.1) returned 0.440 instead.

**The change.**
- IC2 now uses sup m(x)/x² = 1/2 (analytic), so Σ_IC2 = 2π ρ_s r_s / k_B.
- K3 now checks that m(x)/x² → 1/2 at x = 1e-5 (to 1e-4) and is monotone decreasing on [1e-5, 20], alongside the unchanged
  k_B checks.
- Nothing else changes.

**Effect on graded lines: none.** IC1 never uses the NFW constant. The rerun's IC1 lines must equal the interrupted run's
IC1 lines exactly, and I verify this. IC2 is a BORROWED comparator with no verdict weight. Its numbers change by the factor
0.5 / 0.440 = 1.136, upward.
