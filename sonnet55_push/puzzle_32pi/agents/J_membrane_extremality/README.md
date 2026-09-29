# Lane J -- membrane route: can a principle (extremality / BPS / no-force / thresholds / quantisation) fix the one free ratio?

## Bottom line (verdict: SHARP NO-GO on the declared menu; the route stays OPEN with one pi-free coupling)
- In the brief's conventions (verified from the Einstein/Israel equations, `j01`), the puzzle asks of a Brown-Teitelboim wall exactly one thing: its mean proper acceleration `DeltaP/(3 sigma)` equals `sqrt(rho)/2`, i.e. **`sigma E = (2 sqrt2/3) DeltaP`** (no pi anywhere); in the probe limit **`e^2/(G sigma^2) = 9/8`** (`e/sigma = 3/(2 sqrt2) = 1.0607`), equivalently `4 pi G sigma^2/e^2 = 32 pi/9 = Z^2/3`.
- None of the principles I declared beforehand fixes that ratio. The gravitational ones (extremal/BPS/critical wall `B = 0`, no-force `DeltaP = 0`, wall at the horizon) are relations with `beta^2 = 6 pi G sigma^2/DeltaP = 6 pi x/(k^2(1-x/2)) -> 0` in the probe limit (`x = e/E`, `k = e/sigma`): they are **unreachable at any fixed `k`**, so they cannot fix it. Quantisation fixes `x = 1/n`, the Schwinger/thermal threshold fixes `sigma` (through hbar, `sigma/H ~ 1e-122`), the `a = H` crossover is a definition. Every one leaves `k`, hence `a0/H`, free.
- The only declared PAIR that yields a point (critical wall + complete discharge, `x = 1`, `s = 1/sqrt(12 pi)`) gives `a/H = 1/2` (mean) or `1` (side), i.e. `Z_eff = 2` or `1` -- factors 2.89 and 5.79 from the target `1/Z = 0.17275`. The near-hit `P1 + n = 16` (+0.72%) is what 58% of random decoy coefficients also get: no evidence. An EXACT hit of the critical wall with any integer `n` is impossible (rational vs `3/(32 pi)`).
- pi-ledger: every gravity-vs-charge balance in the Heaviside convention carries `4 pi G` (`e^2/(G sigma^2) in 4 pi x rational`), the target `9/8` does not: a principle would have to be a UV Lagrangian relation with a pi-free rational, not a gravitational balance. kappa = 1/2 stays FITTED; nothing derived.

## Hand expectation (disclosed before running)
I expected: no principle fixes `e/sigma`, because the exact junction (`A, B = DeltaP/(3 sigma) +- 2 pi sigma`) makes the gravitational content of a wall sit in the offset `+-2 pi sigma` while the mean acceleration is blind to it. The run confirmed this; the two things I did not expect are the exact identification of the sugra extreme wall with `B = 0` (a useful equivalence) and the `n = 16` near-hit (killed by the decoy control).

## What was done (all numbers recomputed by the committed scripts; exit 0 = all checks incl. controls held)
| script | content | result |
|---|---|---|
| `j01_conventions_and_target.py` (+ `.out`) | conventions verified from first principles (Einstein tensor of S^4 and of the O(4) bounce metric with sympy; four-form stress tensor; Gauss jump from the reduced action; Israel jump `[rho'] = -4 pi sigma rho`; independent numerical root-find of the junction; agreement with the two coefficients quoted in the opened supergravity domain-wall review hep-th/9604090); the target in membrane variables; controls | 22/22 |
| `j02_principles_and_intersections.py` (+ `.out`) | derivation of each declared principle in the same conventions; probe-limit theorem; target-vs-locus intersections; pi-degree ledger; decoy control; probe-dS bounce action; mutation/positive controls | 33/33 |

### Conventions (checked, not assumed)
Heaviside four-form `L = -F^2/(2 4!)`: `T_ab = -(E^2/2) g_ab` (`rho = E^2/2`); `Lambda = 8 pi rho`, `H^2 = 4 pi E^2/3`; Gauss jump `Delta E = e`; wall between `E_out = E` and `E_in = E - e`, `DeltaP = e E - e^2/2 = e (E - e/2)`; Israel `A - B = 4 pi sigma` (`G = 1`), `1/R^2 = H_in^2 + A^2 = H_out^2 + B^2`, so `A, B = DeltaP/(3 sigma) +- 2 pi sigma`. Cross-checks against the review: symmetric-wall acceleration `= sigma/4 = 2 pi G sigma` (with `8 pi G = 1`), extreme Type-I wall: AdS observers accelerate at `chi = sigma/2`.
Controls that must (and do) detect a wrong convention: Gauss jump `e/2` moves the probe target `k*` from 1.0607 to 2.1213 (the kappa = 1 value); `rho = E^2` moves it to 0.75; Israel `8 pi sigma` moves it to 2.1213; Gaussian charge `e_G = e/sqrt(4 pi)` gives `k*_G = 0.2992` (pi-content changes with the unit, the physical `a/H` does not: `a/H = k/(2 sqrt(3 pi)) = k_G/sqrt3`).
`k*` for the kappa alternatives (probe): framework 1/2 -> 1.0607; forced kernel 1 -> 2.1213; Milgrom `cH/2pi` -> 0.9772; `cH/6` -> 1.0233; Nariai-shell `3 sqrt3` -> 1.1816. Each needs a different charge-to-tension ratio, none is singled out by a principle.

### The principles (menu frozen in the header of `j02` before any number was computed) and what each fixes
pi-content first (Heaviside, variables `x = e/E`, `s = sigma/E`; the target locus is pi-free in these variables, `a/H = 1/Z` itself carries `pi^(-1/2)`):

| principle | relation | fixes | pi-degree | a0/H implied (mean) | vs `1/Z = 0.17275` |
|---|---|---|---|---|---|
| target | `DeltaP/(3 sigma) = E/(2 sqrt2)`; probe `e/sigma = 3/(2 sqrt2)` | -- | pi^0 | -- | -- |
| P1 (i)(ii)(iii) critical / BPS-type / equator wall `B = 0` (R = 1/H_out) | `DeltaP = 6 pi G sigma^2`; `k = sqrt(12 pi x/(2-x))`; `A/H = sqrt(x(2-x))`, `mean = A/2` | a curve, not `k` | pi^1 | `sqrt(x(2-x))/2` | depends on `x` |
| P1' the same for the inner vacuum `A = 0` | `DeltaP = -6 pi G sigma^2` | a curve (`x < 0` or `x > 2`) | pi^1 | -- | -- |
| P2 (i) net-force-free wall | `DeltaP = 0`, `x = 2`; `A = -B = 2 pi sigma` | `x` only | pi^0 | 0 (mean), `2 pi sigma/H` (sides): `sigma/H` free | -- |
| P3 (ii) complete discharge | `x = 1`, `H_in = 0` | `x` only | pi^0 | -- | -- |
| P4 (v) flux quantisation `E = n e` | `x = 1/n`; target then needs `k_n = k*/(1 - 1/(2n))` | `x` only, `k` free | pi^0 | -- | -- |
| P5 (iv) Schwinger/thermal threshold | probe-dS bounce `B = 2 pi^2 L^3 sigma f(a/H)`, `f = (1+2phi^2)/sqrt(1+phi^2) - 2 phi`; `B/S_dS = (2 pi sigma/H) f`; `B = hbar b0` | `sigma` (needs hbar; `x ~ 1e-123`), `k` free | pi^-2 in sigma | -- | -- |
| P6 (iii) geometry thresholds | `a = H` crossover: `k = 2 sqrt(3 pi) = 6.14` (ratio to target exactly Z); wall at horizon `R -> 0`: `a -> infinity`; equatorial: `a = 0` | definitions | pi^(1/2) in k, pi^0 in `a/H` | 1 | +479% |
| P1 & P3 (only declared pair giving a point) | `x = 1`, `s = 1/sqrt(12 pi)` | both | -- | `1/2` (mean), `1` (A); `kappa_eff = sqrt(2pi/3) = 1.447`, `sqrt(8pi/3) = 2.894` | +189%, +479% |
| P1 & P4 (family) | `x = 1/n`, `mean/H = sqrt(2n-1)/(2n)`, `k = sqrt(12 pi/(2n-1))` | one integer | -- | n=2: 0.433; 4: 0.331; 8: 0.242; **16: 0.1740 (+0.72%)**; 32: 0.124; 64: 0.088 | see below |

Derivations checked in `j02`: (P1a) `B = 0` gives `DeltaP = 6 pi G sigma^2`, `A = 4 pi G sigma`; (P1b) it is the Coleman-De Luccia critical tension for Minkowski -> AdS (`R -> infinity`); (P1c) it is exactly the extreme (BPS) wall of N=1 supergravity, `sigma_ext = 2 chi` with `|V| = 3 chi^2` (`kappa = 8 pi G = 1`, equations (6.1), (6.3) of hep-th/9604090 as opened): `|V| = (3/4) sigma^2`; (P1d) between two dS vacua there is no real planar static wall (`A^2 = -H_in^2`), positive `V` breaks N=1 supersymmetry (the review states supersymmetric minima have `V <= 0`), so in dS `B = 0` is a geometric threshold (wall on the equator of the outer S^4), not a BPS statement; (P1g) the probe-limit theorem above.

### Where the target meets each locus (units E = 1; full table in `j02_principles_and_intersections.out`)
- P1 with the mean reading (`H_ref = H_out`): `x_t = 1 - sqrt(1 - 3/(8 pi)) = 0.061579` (`n_t = 16.24`), `s_t = 1/(4 sqrt2 pi) = 0.05627`, `k_t = 1.094`. With the side reading `A = H/Z`: `x_t = 0.015034` (`n_t = 66.5`). Both `x_t`, `s_t` contain pi (transcendental: `pi = 3/(8(1-(1-x_t)^2))`), so no integer `n` can hit them exactly (`(mean/H)^2 = (2n-1)/(4n^2)` is rational, `1/Z^2 = 3/(32 pi)` is not; positive control: a pi-free decoy `(a0/H)^2 = 3/16` IS hit exactly, by `n = 2`).
- P3 (`x = 1`) with the mean reading: `s_t = sqrt2/3 = 0.4714` (pi-free), which differs from the P1 value `0.1629` by the factor `sqrt(8 pi/3) = 2.894`: needs a further principle for `sigma/E` that no declared principle supplies.
- P2 (`x = 2`): the mean is 0; the sides equal `2 pi sigma`, matched to `H/Z` only by choosing `sigma = H/(2 pi Z)` -- a free ratio again.
- Decoy control (1500 random coefficients `Z'` in [3,12], same P1+P4 menu): fraction at least as close as the real near-hit: 0.58 (mean reading, n = 16, +0.72%) and 0.77 (side reading, n = 67, -0.36%). A 1% coincidence is generic because consecutive `n` differ by about `1/(2n)` (3% at n = 16).

### Literature (only what I opened)
- hep-th/9604090 (supergravity domain-wall review, `kappa = 8 pi G = 1`): extreme (static, planar) walls exist only between supersymmetric vacua, `V <= 0` (AdS/Minkowski), tension `sigma = 2 chi` (Minkowski|AdS) or `2(chi_1 -+ chi_2)`; walls with `sigma` above/below `sigma_ext` are the non-static / false-vacuum-decay bubbles. This is the `B = 0` boundary of the Israel solution (P1c), with `chi -> iH` giving an imaginary tension for dS.
- arXiv:1509.06374 (WGC under dimensional reduction): the extremality bound `[alpha^2/2 + p(d-p-2)/(d-2)] T^2 <= e^2 q^2 M^(d-2)` is derived for `1 <= p <= d-3`; the paper says domain walls in 4d (`p = d-1`) "may be worth considering, but we will not discuss it here". So the WGC literature I opened gives no extremality relation for a 4D membrane. **Conditional arithmetic only (`j02` W1)**: if the formula were naively extended to `d = 4, p = 3` the bracket is `(alpha^2 - 3)/2`, negative at `alpha = 0` (no bound), and saturating at the puzzle's ratio would need `alpha^2 = 3 + 9/(32 pi)`, a pi-laden dilaton coupling. This is not a result.

## What is NOT established
- The menu is finite (P1-P6). I did not treat a dilaton/scalar sector, world-volume fields, a bare cosmological constant added to `E^2/2`, several charged species (Bousso-Polchinski), or quantum corrections; each could supply a ratio and would move the free coupling into a new parameter (e.g. the dilaton coupling), not remove it.
- That a wall's proper acceleration is the MOND `a0` is the premise of the route, not something derived here; this lane only asks whether a principle can close the ratio if it is.
- The pi-argument is relative to the variables held natural (in `(x, s)` the target is pi-free, in `a/H` it is not; the addendum's warning applies). I use it only in the two forms verified: exact equality with an algebraic `x` is impossible when the principle relation has pi to the first power, and the Heaviside gravity-charge balances carry `4 pi G`.
- The identification of the P1&P3 point with the marginally embeddable puzzle horizon (`Z_eff = 2`, `r_s = L`) is an observation of equal numbers; I do not claim a mechanism.
- The supergravity relation was checked against the review's stated formulas (equations (6.1), (6.3) and the acceleration statements), not re-derived from supersymmetry.

## Verdict
SHARP NO-GO for "a principle in the declared menu fixes the membrane ratio": extremality/BPS/critical-wall, no-force, dS/Nariai-type thresholds are gravitational relations that vanish in the probe limit where the target lives; quantisation and Schwinger thresholds fix other quantities; the one pair that fixes a point lands at `Z_eff = 2` (a factor 2.89 from the target); near-hits are at the decoy rate and exact hits are excluded by pi-counting. The route remains OPEN in exactly one form: a UV relation `e^2/(G sigma^2) = 9/8` (Heaviside, `rho = E^2/2`) with a pi-free rational that is not a gravitational balance. kappa = 1/2 stays FITTED; nothing here derives it.

Run: `python3 j01_conventions_and_target.py` (22/22) and `python3 j02_principles_and_intersections.py` (33/33, ~10 s).
