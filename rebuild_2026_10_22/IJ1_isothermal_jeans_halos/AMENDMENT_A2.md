# IJ1 — AMENDMENT A2 (POST-PRIMARY-RESULT; execution only; committed alone before any further variant number)

**What was seen.** The A1 rerun completed PRIMARY on both footings, then the reported rows (pure NFW, fair-share, no-BCG,
dwarfs by class). PRIMARY canonical numbers equal run 1's printed digits, as A1 required. The verdict line printed IJ FAILS
on both footings; K1 PASS, K3 FAIL (1 of 89 alt dwarfs unconverged, 1.1 % > 1 %). Peak RSS was 1.15 GB, above K5's 1 GB.

It was then stopped by hand (SIGTERM at 5953 s, `_PARTIAL` outputs kept) during the canonical variant calibration. By
then 30 of the 41 coarse points were cached (log₁₀ A from −2.0 to +0.9). These print SPARC A rms 0.0654–0.0674 at median
Υ 0.37–0.43.

**Why it was stopped.**
- Resident memory kept growing during repeated SPARC solves, reaching 1.37 GB.
- Each evaluation slowed as A grew, to 3–4 min. About 5 h of single-thread work remained.

**Change (execution only).**
1. The normal run no longer contains the variant. It writes PRIMARY, the reported rows and the checks to
   `ij1_isothermal_jeans.out` / `_results.json`, as before.
2. `--variant` runs the frozen variant (same coarse grid −2..2 in 0.1, same fine grid ±0.1 in 0.02 around the coarse
   minimum, SPARC background A rms, n kept). Each uncached SPARC evaluation runs in its own child process
   (`--sparc-eval FOOT LOG10A`), so resident memory cannot accumulate. The 30 cached points are reused: they come from the
   same function and the same numerics. The parent then grades all five classes at A_f, using the same rules, labelled
   REPORTED. Outputs go to `ij1_isothermal_jeans_VARIANT.out` / `_results_VARIANT.json`.
3. K5 is reported per invocation. It already failed in PRIMARY (1.15 GB). That is disclosed and not re-thresholded.

**Unchanged.** Every criterion, class rule, threshold, grid, numerical setting and input. No PRIMARY number can change: the
rerun of the normal mode must reproduce the A1 rerun's PRIMARY lines exactly, and the README says whether it does.
