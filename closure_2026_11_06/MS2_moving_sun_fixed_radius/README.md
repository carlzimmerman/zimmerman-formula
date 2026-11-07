# MS2: the moving-Sun door (v3s, AC2q): NO VERDICT, bracketed, with the readout cause removed

Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

- **Criteria:** CRITERIA.md was committed alone (local dfd90815b6) and pushed (origin 92b0894440) before
  any script or run.
- **Script:** ms2_grade.py. The solver copy is hydro_ms2.py; hydro_ms2.diff adds only the `ultra`
  resolution choice.
- **Outputs:** MS2_interim.json and ms2_interim.out. Every number below is in them.
- **Not committed:** the row cache, and the stopped ultra run's state.npz (about 17 MB).

## What MS2 fixed

**Readout (MS1 cause 1): fixed.**
- R1 evaluates the gates at the exact planet radius, splitting the straddling cell by volume.
- Plant recovery is now within 0.615 % on every rung, gate, cell and k (KA2 PASS, line 1 %). On AC24's
  nearest-edge readout it was 4.6 %.
- Under R1 the q reading's grid changes are below 1e-3 of the line everywhere: 168 of 168 q series are
  TINY_ABS, against 28 failing q series in MS1.

**KA1:** reproduces MS1 exactly. 84 rung values, relative difference 0; maxima 0.4964 / 0.5721.

**KA3:** procedure PASS.

**MUTATE k = 2:** PASS (min L 1.956).

## Why it is still NO VERDICT

Label NO VERDICT, as frozen. It does not depend on the fourth rung. Three checks fail:

- **CONV, M490 (ladder coarse / medium / fine, final under the criteria).**
  - 6 q_B series are PRE-ASYMPTOTIC: G1 Earth, p 0.44 against the 0.5 line, rung means 1.93e-2, 1.23e-2,
    7.09e-3.
  - The other 66 + 12 q_B series are MONOTONE or NOISE.
- **MUTATE k = 0.1, M490.** It fails in 3 cells: canonical footing, V = 220, G2 Mars on q_B.
  - The planted series (0.188, 0.180, 0.163) is DIVERGENT, although its base series is MONOTONE.
  - G2 is a max-minus-min of |a| over theta. That is not additive, so the plant and the base grid error
    mix.
  - Under the frozen rule the extrapolated reading therefore lacks shown power for that gate.
- **CONV, M234 (INTERIM ladder).** 23 q_B series are DIVERGENT on coarse / medium / fine.
  - The ultra rung (M234 only) was started and then stopped by the frozen RSS line: it held 2.15 GB
    against 1 GB, while other large runs were live.
  - Its checkpoint is kept and it can resume.
  - It would not change the label: both M490 failures above are on a ladder that ultra does not touch.

## Is the M234 acceleration a pre-asymptotic R_A / bow-shock effect? (diagnostic D, frozen)

No. The verdict is DISTRIBUTED.

- 99.85 % of the medium-to-fine change in the q_B charge lies at r > 100 R_A: the large far-field volume,
  where q_B = 1 + M^2 (Phi + (1 - w^2)/2) turns small velocity errors into charge. Less than 0.003 % lies
  inside 20 R_A. The same split holds for coarse-to-medium and at M490.
- None of MS1's DIVERGENT series became NOISE. 16 became TINY_ABS (the q ones) and 23 stay DIVERGENT.
- Reported beside D: the M234 fine run is not steady at t = 800-1000.
  - Worst-cell q_B G1 Mars on the five snapshots: 0.036, 0.021, 0.023, 0.028, 0.023.
  - Medium on the same snapshots: 0.0404-0.0410.
  - M490 fine is still drifting down, from 0.046 to 0.041.
  - So the rung differences at t = 1000 mix grid error with a far-field flow that is still evolving.

## Bracket

[min L, max U] as a ratio to the line, over cells, brackets and readings:

| Gate | Bracket |
|---|---|
| G1 Saturn | [1.5e-6, 0.297] |
| G2 Saturn | [0, 0.177] |
| G3 Cassini | [1.4e-7, 0.060] |
| G1 Earth, G1 Mars, G2 Earth, G2 Mars | unbounded above, from the M234 q_B DIVERGENT series |

Reported, not the label:

- The largest time-mean value on any rung is 0.147 of the line (M490 q_B G1 Mars, coarse).
- On the q reading every number is at most 1.3e-3 of the line, and converged under R1.

## What would close it (new criteria needed)

The q_B reading's open part is in the far field (r > 100 R_A), and the runs are not steady there at
t = 1000. Two things could close it:

- a t_end long enough for the far field to settle at the fine rung (at least 3x the fine cost);
- a q_B reading restricted to the planets' region, with its far-field part bounded analytically.

Each needs new frozen criteria. A fourth rung at t = 1000 does not, on this evidence, address it.

Scope as in AC15, AC24 and MS1. No PPN alpha_1 or alpha_2 is claimed. AC2q differs by s^2/rho0 ~ 4e-6.
