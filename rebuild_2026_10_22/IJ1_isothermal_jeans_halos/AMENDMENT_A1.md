# IJ1 — AMENDMENT A1 (POST-PARTIAL-RESULT; memory only; committed alone before the rerun's result)

**What was seen.** Run 1 of `ij1_isothermal_jeans.py` was stopped by hand (SIGTERM at 243 s) after printing:
- checks K2, K0, K4a, K4 (all PASS);
- canonical PRIMARY SPARC: A rms 0.0654 @ Υ 0.37, B 0.0653 @ 0.36 → FAILS;
- canonical PRIMARY cluster cells: 14 of 15 fail, all over-predicted (≈ 2× in every band; G-IN-Mall Z −3.48);
- canonical PRIMARY groups: mean +0.0686, Z +1.64 → PASS.

No alt-footing, SLUGGS, dwarf, reported or variant number was printed.

**Why it was stopped.** Peak RSS reached 1.14 GB during the SPARC solve, above the frozen K5 bound (< 1 GB).

**Change.** The SPARC solve is chunked by 5 galaxies instead of 20 (`sparc_ij(..., chunk=5)`). This only changes how many
lanes are held in memory at once. Every lane is solved independently, so no graded number can change.

**Unchanged.** Every criterion, class rule, threshold, numerical setting (grid, steps, tolerances, branch rule) and input.

**Commitment.** The rerun's canonical numbers listed above must be identical (to the printed digits). The README reports
whether they are. If they are not, the README says so and both runs are kept.

**Earlier edits, for the record.** Before run 1, the script was edited twice: once after a crash (a `KeyError` loading GR1's
helper names, at the machinery stage, before any graded number), and once for a units constant (P4's own kpc for the
groups) and the isothermal series start (in `ij1_lib.py`) before any run of the lane script. In those runs only K2, K0 and
K4a had printed.
