# SRF1 AMENDMENT A2 (2026-11-12): a reported ratio-weighted reading of the forced groups; nothing graded changes

Committed alone, after the first part (z 2.2, seed 0, canonical) landed and before any flux number of this lane was opened.
FROZEN_CRITERIA (fa73352ceb) and AMENDMENT_A1 (88144763e1) are unchanged; the label is computed exactly as they say.

## What I saw (matter level of one part only; no flux array read)

- Known answer (b) on that part: reference and Poisson-only f = inf flux power equal FRZ3R's part exactly (0.0), after the
  summation-order fix (the run before the fix read 1.7e-4 at k_v about 0.55 s/km; that part was deleted).
- The stratified matter-level estimate at z 2.2, seed 0, against the halo model's turnaround-scope expectation R_ta - 1:
  f 1.00: -0.0062 / -0.0198 at k 3 / 5 against -0.0082 / -0.0261 (about 0.76 of it); f 1.30 and 2.00 the same fraction.
  The forced groups of one or two haloes (log M 12.5, 13.0, 13.5) are drawn from bins in proportion to expected count, so
  a single draw can sit low in its group; that is sampling noise of the frozen estimator, which seed 1 partly averages.
- A ratio weight per group, w_g(f) = sum_b E_b s_b(f) / sum_b n_b s_b(f), with s_b(f) the halo model's per-halo one-halo
  difference at k 3 h/Mpc for bin b and n_b the forced counts actually drawn, gives -0.0098 / -0.0321 against the same
  -0.0082 / -0.0261 (about 1.2 of it). The two weights bracket the expectation.

## Change

- **Reported reading R (ratio-weighted forced groups):** flux and matter Delta chi^2 at every grid f and its f_max, computed
  from the same parts with w_g(f) in place of E_g / n_g. It is a reported bracket. It does not replace the frozen weight,
  does not enter the label, and does not change known answer (c1), which is graded on the frozen weight. If reading R moves
  f = 1 across the gate or opens or closes the window, RESULT says so beside the label (the frozen FRAGILE rule covers only
  the brackets of section 8).
- Expectation stated now: if c1 fails on the frozen weight it will be by under-realisation (about 0.6 in Delta chi^2), and
  the label is then NO VERDICT, as frozen; reading R would then be the nearest ungraded number.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
