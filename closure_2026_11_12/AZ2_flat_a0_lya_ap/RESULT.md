# AZ2 RESULT: flat a0(z) at z 2.33 with the DESI DR2 Lya AP pair replacing CFG681's

**Label, amended reading (A2): FLAT HOLDS / EXPANSION-MODEL DEPENDENT (canonical); FLAT HOLDS / EXPANSION-MODEL DEPENDENT (alt).**
**As frozen: NO VERDICT / NO VERDICT** (KA3 failed in the headline cell; A1 misdiagnosed it, A2 fixed the check; see below).
A FLAT HOLDS is not a pass for the theory: LCDM's constant dark energy gives the same sqrt X = 1, nothing here separates the
framework from LCDM, and no kinematic a0 at z 2.33 is involved. TEST lane. Criteria 8c95369a28; A1 a3d9e9bf28; A2 fbf7814e5d.

## Numbers (CFG681's model and statistic; new pair 39.32 +- 0.33 / 8.600 +- 0.066, r 0.225 in place of 38.988 / 8.632, r -0.431)

sqrt X(2.33) = a0(2.33)/a0(0) at fixed Om. D_band = profile Delta chi^2 (1 dof) at the nearest point of the flat band
[0.90, 1.10]; D_X1 at exactly flat; D_rival at a0 proportional to H(z) (sqrt X = 3.43 at Om 0.30). X5 = X(2.33) intervals are
on a grid of step 0.5 away from the band (resolution-limited).

| cell | canonical sqrt X / a0(2.33) | D_band | D_X1 | D_rival | X5 95 % | label | alt sqrt X / a0(2.33) | D_band | label |
|---|---|---|---|---|---|---|---|---|---|
| **T2 BAO+SN, Om 0.30 (headline)** | **1.320 / 1.235e-10** | **1.76** | 3.47 | 361.8 | [0.96, 2.5] | **FLAT HOLDS** | **1.322 / 1.495e-10** | **1.79** | **FLAT HOLDS** |
| T2, Om 0.25 | 2.026 / 1.897e-10 | 71.3 | 83.4 | 169.1 | [3.5, 4.6] | FLAT FAILS | 2.028 / 2.294e-10 | 71.6 | FLAT FAILS |
| T2, Om 0.35 | 0 (X5 -0.99) | 15.2 | 18.3 | 569.0 | [-1.49, -0.49] | FLAT FAILS | 0 (X5 -0.98) | 15.1 | FLAT FAILS |
| T1 BAO only, Om 0.25 | 1.965 | 3.21 | 3.84 | 7.1 | [0.96, 8.0] | FLAT HOLDS | 1.966 | 3.22 | FLAT HOLDS |
| T1, Om 0.30 | 1.195 | 0.01 | 0.06 | 13.6 | [-1.0, 5.5] | FLAT HOLDS | 1.197 | 0.01 | FLAT HOLDS |
| T1, Om 0.35 | 0 (X5 -1.38) | 1.00 | 1.16 | 19.8 | [-1.88, 3.5] | FLAT HOLDS | 0 (X5 -1.37) | 0.99 | FLAT HOLDS |

Footings differ only through Or(h) (h 0.644-0.692 canonical, 0.778-0.836 alt): <= 0.003 in sqrt X, as expected; the absolute
a0(2.33) differs by the footing's a0. Reported only: Om profiled, T2 Om -> 0.260, sqrt X 1.92, D at X5 = 1 only 0.05; T1 Om runs
to the 0.45 edge (X5 < 0). T1 / T2 Delta chi^2 (X = 1 vs free, 5 dof): 8.14 (p 0.149) / 12.00 (p 0.035), was 7.41 / 12.08.
T3 AP chi^2 7.06 / 5 (p 0.22), Lya pull +0.67 (was 5.98, +0.16). Old pair at the headline cell: sqrt X 1.24 (CFG681).

## What the label rests on

- Expansion model: CFG681's flat piecewise-linear X(z), 5 nodes, r_d free inside q, no CMB, no CPL, no LCDM; Om fixed on
  CFG681's grid. The headline is the Om 0.30 cell; at Om 0.25 and 0.35 the BAO + SN cells FAIL (sqrt X 2.03, or X < 0), hence
  EXPANSION-MODEL DEPENDENT. Raw BAO + SN still do not fix Om (CFG681's dark degeneracy; the Om-profiled row allows flat), so
  the label is conditional on Om near 0.30.
- At the headline cell flat holds only through the +-10 % band: exactly flat sits at Delta chi^2 3.47 (1.9 sigma) from the
  best fit sqrt X 1.32; the new pair moved the central value up from 1.24. The rival a0 proportional to H(z) is excluded in
  this cell (Delta chi^2 362), so the measurement has power against it here.
- Published values: arXiv:2607.27410v3 Eq. 26 (PROVISIONAL, read from https://arxiv.org/html/2607.27410v3); other DESI DR2
  BAO pairs and Pantheon+ exactly as CFG681.

## Known answers

- KA1 PASS: with the old pair the code reproduces CFG681: T1 7.408, T2 12.080, T3 5.976, fixed-Om sqrt X(2.33) 1.929 / 1.140 /
  0.000 and 1.974 / 1.235 / 0.000 (`az2_KA1.out`; re-run with warnings silenced, same digits: the first run printed spurious numpy matmul
  RuntimeWarnings carrying a local path).
- KA2 PASS: flat injection at Om 0.30, D_band 0.00, sqrt X 1.000.
- KA3: FAILED as frozen in the T2 Om 0.30 cell (gap -0.357 / -0.373): the free fit was lower than every grid point because
  the free X5 1.74 lay between grid points. A1 (restart the free fit) was a sign misread and is inert (stopped run
  `az2_canonical_A1_partial_stopped.out` reproduces the frozen cells). A2 added the free X5 +- 0.5 to the grid: KA3 passes in
  every cell (|gap| < 0.001). Frozen and A2 Delta chi^2 values and labels are identical, because every Delta chi^2 was already
  measured from the free minimum.

## Mutation (new D_H/r_d -5 sigma, 8.270; hand estimate sqrt X ~1.2 -> ~1.6)

Headline cell: sqrt X 1.320 -> 1.789 (canonical), 1.322 -> 1.790 (alt); D_band 1.76 -> 22.15 / 1.79 -> 22.27; label FLAT FAILS.
Bites (rule: >= +0.2 and >= +4). Outputs `az2_*_MUTATE*.json/.out`.

## Not checked

The joint covariance between the new Lya pair and the DR2 galaxy/QSO pairs (taken independent, as CFG681); the paper's revised
BAO systematics beyond its quoted errors; other expansion models (CPL, curvature, the native r_d of CFG689); any Om prior; T4
duality (unaffected, not re-run); profile resolution finer than 0.05 near the best fit and 0.5 elsewhere; DESI's own Lya-only
AP numbers (Eq. 24-25, not used).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
