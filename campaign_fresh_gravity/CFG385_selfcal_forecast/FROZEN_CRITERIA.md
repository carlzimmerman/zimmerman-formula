# CFG385 FROZEN CRITERIA: self-calibrated a0(z ~ 2.5) forecast. Which sample decides the DE-tracking law vs a0 proportional to H(z)?

Committed alone, before any script. A FORECAST: no data are scored against any law. kappa = 1/2 FITTED. Owner (2026-10-06, chat "Nobel Prize and neutrinos"): "go 1" (scope the decisive a0(z ~ 2.5) data).

**Why.** Absolute baryon calibration (+-0.07 dex) is the wall (CFG217/218/240). CFG240 certified that with ONE common calibration f LEFT FREE, a sample spanning both regimes self-calibrates: the inner Newtonian points fix f, the outer points fix a0. CFG240 tabulated only the 0.1-dex target and did not tabulate the flat-vs-rival one (CFG266 SCOPING). The owner's law: a0 tracks rho_DE. DESI DR2 gives a0(2.5)/a0(0) of about 0.78-0.83 (p13c). The rival a0 proportional to H(z) gives about 3.7-3.9. The separation is 0.67 dex, so 3 sigma needs sigma(log a0) <= 0.22 dex. (Flat vs rival: 0.57 dex, so <= 0.19 dex; reported.)

## Method (CFG240's Fisher model, re-implemented; CFG240's closed forms)
- Parameters (log10 f, log10 a0). Data: log10 g_obs at N points with independent errors sigma dex. b(y) = d log g_obs / d log a0:
  P2 b = 1/(2(1+y)); exponential RAR kernel b = s/(2(e^s - 1)), s = sqrt(y). (This is CFG240's "nu_mono" label; it is the
  exp-RAR form. The ledger names it the same way.)
- F = (1/sigma^2) Sum [(1-b)^2, (1-b) b; (1-b) b, b^2]. sigma(log a0) = sqrt((F^-1)_22). An optional Gaussian prior on log f:
  tau in {none, 0.3, 0.15} dex.
- Design: N points log-uniform in y between y_min and y_max.
- Grid: y_min in {0.05, 0.1, 0.3}, y_max in {2, 5, 10, 30}, N in {10, 20, 40, 80}, sigma in {0.05, 0.1, 0.15, 0.2}.

## Outputs
- Every design meeting 0.22 dex (DE law vs rival) and 0.19 dex (flat vs rival), per kernel.
- Archetype rows, labelled ILLUSTRATIVE (y ranges from the record; N and sigma are stated assumptions, not measurements):
  - KURVS-like: z ~ 1.5, outer y 0.06-0.67; inner y to about 3 assumed; N = 10 discs x 3 points.
  - RC100-like: y 1.1-4.4, no deep points.
  - CRISTAL-like: y about 1-5.
  - A "needed" sample: z ~ 2.5 discs with deep outer points.
- The minimum N at sigma = 0.1 that reaches 0.22 dex with y_min = 0.1, y_max = 5.

## Controls
- C1: the re-implementation reproduces CFG240's committed break-even entry (P2, y_min 0.001, N 20, sigma 0.1: y_max* 5.5,
  sigma(log a0) ~ 0.0999) to 2%.
- C2: the T4 floor sigma(log a0) >= 3 sigma/sqrt(N) holds on every grid cell (b in [0, 1/2]).
- MUTATE: set b to its deep-regime constant 0.5 everywhere (no Newtonian points). F must become singular (f free), and
  sigma(log a0) must diverge or exceed 10 dex. rc 1.

Local compute only. No downloads. The deliverable is the sample specification, plus a list of which data would meet it (each
fetch needs the owner's go).
