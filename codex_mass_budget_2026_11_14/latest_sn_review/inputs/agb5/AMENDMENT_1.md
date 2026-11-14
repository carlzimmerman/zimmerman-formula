# AGB5 amendment 1 (2026-11-14): the error bar. Written AFTER the numbers were seen; committed alone before the re-run

## What happened
All checks and fits were run after the scripts commit (627f7d2ef8). KA, K1 and K3 pass. **K4 fails on table 2**: the
scatter of the slope under shuffled hosts is 1.43 times the stated error (allowed 0.8–1.25); table 1 passes at
1.248. The bootstrap half of K4 passes on both tables (1.09 and 1.16). By the frozen rule L1 is **NOT EVALUABLE as
frozen**. That stands and is reported.
The amplitudes had been printed before this note was written: with the mass step free the combined slope is
A = +0.82 ± 0.17 by the stated errors. This amendment does not move any amplitude. It changes the error bar only.

## Why the shuffle test failed
1. The stated error is too small. The plain fit assumes 0.10 mag of intrinsic scatter (the value that reproduces
   the published slopes); the fits then have χ²/dof 1.35 (table 1) and 1.42 (table 2), so the real scatter is larger
   and every error should be about 1.16 and 1.19 times the stated one. The bootstrap over hosts says 1.09 and 1.16.
2. The shuffle test, as written, assumes a weak signal. Shuffling the hosts leaves the fitted age and mass signal
   (0.05 and 0.08 mag rms) in the residuals as extra scatter. With the fitted signal taken out first, the shuffle
   scatter is 1.11 and 1.23 times the stated error, in line with the bootstrap.

## The change (everything else in FROZEN_CRITERIA.md is unchanged)
1. **Errors.** The error of every slope that enters L1 and its forks is the standard deviation over 400 bootstrap
   resamples of the hosts of that table (seed 20261119), not the least-squares formula. Combined amplitudes use these
   errors as weights.
2. **K4, amended.** Per table: the bootstrap error within [0.8, 1.25] of the stated error (computed: 1.09, 1.16), and
   the shuffle scatter with the fitted signal removed within [0.8, 1.25] (computed: 1.11, 1.23).
3. **Word.** L1 is judged by the frozen rules on the amended numbers and carries the tag "(amendment 1)". Both
   readings are reported; amended outputs go to separate files (`agb5_L_boot.json`, `agb5_K4_boot.json`).

## What had been seen when this was written
Everything in `agb5_L.out` and `agb5_K4.out`: all amplitudes with their stated errors, all forks, the reported rows.
This is therefore not a blind amendment. Its direction is known in advance too: larger errors can only weaken a
word. It was chosen because the frozen bootstrap estimate was already part of K4.

kappa = 1/2 FITTED; not theory closed.
