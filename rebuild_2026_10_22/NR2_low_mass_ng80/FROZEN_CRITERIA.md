# NR2_low_mass_ng80: FROZEN CRITERIA (committed alone, before any run or number; owner's go 11-01)

**Question.** NR1: version N passes SPARC at η(10¹², ng 80) only if η at 10¹⁰ and 10¹¹ stays as measured at ng 64 (Υ 0.72 / 0.75). If they fall by the same 0.83 it fails (0.88 / 0.89). What does ng 80 read at those masses, and does N pass with all three anchors at ng 80?

**Standing.** κ = ½ FITTED. No a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. Not blind to NR1's table.

## Runs
10¹⁰ and 10¹¹, seeds 1–9, ng 80, `x48_fast.py` to z_f only, ε fraction, z_i, η_step and background as X80 and A5. Single thread, nice 15, `--resume`, SIGTERM checkpoints, exit 75. Work directories in this lane. Each grid draws its own field, so per-seed ratios mix resolution and realisation; only medians are compared. Fewer than 6 finished at a mass: UNDECIDED.

## Measurement
X80's converged-cusp η, `x80_converged.py`'s estimator unchanged, with its seeded bootstrap for 68 % bands. 10¹² ng 80 from A5's nine seeds, 21.53.

## Grade
`../NR1_native_n_ng80/nr1.py`'s path: η(10¹²) 21.53, ρ₁₀ = η(10¹⁰)/21.53, ρ₁₁ = η(10¹¹)/21.53, η(10¹³), η(10¹⁴) from CE1's A4.

- **ALL-NG80 PASSES:** rms ≤ 0.110 and Υ 0.50–0.80 on both backgrounds.
- **ALL-NG80 FAILS:** otherwise, with the side stated.
- **[NOISE-LIMITED]** if either band run differs in line from the median: both ρ at their p16, and both at their p84, from the ratio bootstrap.

## Reported, not graded
η(ng 80)/η(ng 64) at each mass with bootstrap bands; slope of η with mass; S against ET1 and Υ by V_flat at the median; groups Z and failing keys.

## Expected, on record before running
ρ₁₀ 0.9–1.5, ρ₁₁ 0.8–1.3, medians move by under 25 %, bands wide. Per-seed η at ng 64 spans 12–38, so [NOISE-LIMITED] is the likeliest tag. Line: no call.

## Checks
- **K1:** the estimator on X80's ng 64 runs returns 29.26 and 24.34, |d| ≤ 0.01.
- **K2:** this path at A4's anchor and X80's ρ reproduces `NF1_NATIVE`, |d| ≤ 1e-9 (NR1's K3).
- **MUTATE:** ρ₁₀, ρ₁₁ × 0.5, separate output: Υ must move more than 0.02.
- Any failure: no verdict, exit 1.

κ = ½ FITTED. Not theory closed.
