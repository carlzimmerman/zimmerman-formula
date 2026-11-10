# GRW1 amendment A1 (POST HOC): two known-answer checks as written could not test what they were meant to test

Criteria 11c19a2c5f. Written after the first run of `grw1_ka.py` printed its known answers, **before any graded number
existed** (no law-on run, no line evaluated). POST HOC: it changes how two known answers are evaluated after their
values were seen. TEST lane; adopts nothing.

## What failed as frozen

- **KA2(b)** (my cold reference against CLASS, P ratio within 1 % at k 0.04-10 / Mpc, z 0-3): max |dev| 0.369 (z 0, k 10;
  0.16 at z 3). The criteria give my engine an IGM temperature of 1.5e4 K after reionization (section 1.5), and CLASS has
  no photoheating (its T_b is 5 K at z 3). So the check compared two different physical inputs, and the gap is the frozen
  baryon pressure at k >= 1 / Mpc. With that heating term set to zero the same engine matches CLASS to 1.8e-3 at every z
  0-3 (scratch check, same code path, the heating constant zeroed).
- **KA5(a)** (1 - c = mu_e (1 + L_e mu^2) at 100 random points, line 1e-12): max relative difference 1.03e-12. The identity is
  algebraic; computing 1 - c in floating point at x = 1e-4 loses about four digits, so 1e-12 sits at the roundoff floor.

**As frozen, the lane is NO VERDICT on both footings** (section 4: a failed known answer). That reading is kept and
reported first in RESULT.md.

## The amendment

- **A1a.** KA2(b) is evaluated with the IGM heating term set to zero (c_b^2 = CLASS's own), i.e. the engine is compared with
  CLASS on CLASS's own physics. Line unchanged (1 %). The frozen value with heating (0.369) is still printed. The graded runs
  are unchanged: they keep the frozen heating, applied to the reference and to every model alike, and every graded line is
  a ratio to that reference. Absolute spectra stay ratio x CLASS's reference P (as frozen).
- **A1b.** KA5(a) is evaluated in exact rational arithmetic (Python `fractions`) at the same 100 random points, converted to
  rationals; the line is exact equality. The float value is still printed. Lean (`GRW1.lean`) certifies the identity too.

Nothing else changes: lines, labels, treatments, MUTATE and every other known answer stay as frozen.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
