# LMC1 AMENDMENT A3 (2026-11-12, written before run 4; NOT BLIND, see disclosure)

## What happened

Run 3 (`lmc1_run3_K7_FAIL.out`, after A1 and A2) passed K1-K6 and K2 (zero-mass twin bitwise equal) and the
stationarity checks K3, ran the six labelled twins, and stopped at K7: the bootstrap error of q is
0.0054, 0.0089, 0.0162, 0.0224 (canonical, central) and 0.0046, 0.0095, 0.0151, 0.0202 (alt) by bin, against
the frozen limit 0.005. No label was computed.

Disclosure: the q values themselves were printed in run 3 before the stop (all within 0.97 to 1.035, every
footing and mass) and were read before this amendment was written. A rough hand calculation of E1 from them
was made. This amendment is therefore NOT blind with respect to q.

## Why the frozen precision cannot be met

The design study's error estimate (0.12 to 0.36 per cent) used a synthetic offset applied to the SAME particles,
so the twins were perfectly paired. In the real twins the LMC moves particles by about 2 kpc (median, 55-80 kpc)
and changes their velocities by about 9 km/s (median 3-D) over 2 Gyr, so bin and footprint membership changes
for 10 to 15 per cent of the particles and the two dispersions are close to independent samples. A post hoc
test in the scratch area (not kept as a lane output) showed: smooth bin edges reduce the error by about 20 per
cent only; a 0.5 Gyr twin by about 40 per cent; a Lagrangian estimator (membership fixed by the no-LMC twin)
gives errors 0.003 to 0.012 but is biased upward by orbital phase decorrelation (q 1.004 to 1.053), so it does
not measure the dispersion the stars would show. Meeting 0.005 in every bin needs about 20 times more particles
(about 3 million), far beyond this lane's compute budget.

## Changes (nothing else changes)

A3.1 K7 is recorded as FAILED and is no longer a stop. The frozen primary estimator (Eulerian q, footprint) is
     kept; its bootstrap error is carried into h_c as frozen (section 5), so z1 includes it.
A3.2 New robustness test on every labelled word (both footings, all three masses): recompute E1 and z1 with
     the three bins' q moved by 2 err_q in each adverse direction (q2 - 2 e2, q1 + 2 e1, q3 + 2 e3 and the
     opposite). If either shifted word differs, the label carries "FRAGILE (q NOISE)".
A3.3 The result is stated as graded with a failed precision check, and the q per bin is quoted with its error
     everywhere; no per-bin effect smaller than 2 err_q is called detected.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
