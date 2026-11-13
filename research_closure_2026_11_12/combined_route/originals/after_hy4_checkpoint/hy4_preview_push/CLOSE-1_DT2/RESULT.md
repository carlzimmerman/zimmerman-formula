# CLOSE-1 (DT2) RESULT — the engineered kinetic function, graded

**CORRECTION — 2026-11-12.** The old numerical claims below are historical. Correcting the ln(a) growth friction changes K1 from PASS (0.5509) to **FAIL (0.490765)**. The cosmological time map also contained an extra 1/a. The claimed R_set(0)=0 is withdrawn: old raw output disagrees, the force lacks its own homogeneous cosmological limit, and the corrected driver stops at a central cutoff. Physical present-day settling is **UNAVAILABLE**. See [correction record](../../research_closure_2026_11_12/combined_route/dt2_corrections/CORRECTIONS.md). Original files and output are preserved.

Criteria `FROZEN_CRITERIA.md`, pre-registered before any number. TEST lane, quarantined:
adopts nothing, relabels nothing, registers nothing. Footings never pooled.
kappa = 1/2 FITTED; not theory closed.

## Label

**FOLDS / FOLDS** (canonical / alt). Same label on both footings.

K3 fires on both footings. K2 fires on the alt footing. K1 passes. The one thing
MEDIUM_DESIGN §4 said was not computed is the one thing that kills the construction.

## The object, stated explicitly

The record's own construction, at `research_closure_2026_11_10/DT2_response_audit/tradeoff_audit.md` §4
(a regular counterexample to DT1's pointwise derivative bound), adopted here as canonical DT2:

    x(q) = (n0/M)(q - 1) + A * B(q),   q = n/n0,   A = L - 26 n0/M,
    B(q) = 0 (q<=2);  S(t), t = (q-2)/24 (2<q<26);  1 (q>=26),   S = 10t^3 - 15t^4 + 6t^5.

**PINNED** (by the record's lines, not free): `M = 400 Mpc^-2` (DT1 §2, "clumping at 20 per Mpc
physical from z = 2 to 5"); `phi = 4e-6` (DT1 §2, deepest spiral); `n_well <= 216 n0` (DT1 §2);
`q1 > 1`; `n0 = 2.1263e-8 Mpc^-2` (DT1's H0 = 70, Omega_c = 0.26; audit §3).
**FREE**: `q1 = 2`, `q2 = 26`, `L = 8.00e-6`, the shape `S`, the extension outside the band.

**The narrow interval of changed compressibility:**

| | value |
|---|---|
| support in density `q` | [2, 26] |
| support in redshift | z in [0.260, 1.968] |
| support in offset `x` | [5.32e-11, 8.00e-6] |
| **CENTRE** (where `n'` is minimal, `B'` maximal) | `q_c = 14`, i.e. `n = 14 n0`, `z_c = 1.412` |
| FWHM (`n' <= M/2`) | `q` in [7.5, 20.5], z in [1.04, 1.74] |
| jump | `L = 8.00e-6 = 2.00 phi` |
| `n'` at the centre | 0.0340234 Mpc^-2, a factor 1.18e4 below `M` |

The audit's identities reproduce exactly: `x(1)=0`, `n'(0)=400`, `x(14)=4.0000e-6`,
`q(4e-6)=14.000`, `x(27)=8.0000e-6`, `x(216)-x(27)=1.00466e-8`, `n'(x(14))=0.0340231`.

## K1 — LINEAR. **PASSES (0.5509 against a line of 0.50).**

Growth factor of the clock's charge, `delta'' + [3 + dlnH/dlna] delta' = 1.5 Omega_m(a) F delta`
with `F(k,a) = Q^2 n'/(Q^2 n' + k_phys^2)` (the record's law-on blend, TPA1 §4.4 epsilon = 1),
z = 6 -> 0, against the pressureless reference:

| k_com [1/Mpc] | k_phys(z=2) | D_DT2 | D_ref | ratio | line >= 0.50 |
|---|---|---|---|---|---|
| 6.667 (= 20/Mpc physical at z = 2) | 20.0 | 1.9254 | 3.4948 | **0.5509** | PASS |
| 2.0 | 6.0 | 2.4724 | 3.4948 | 0.7075 | PASS |
| 0.2 | 0.6 | 2.9605 | 3.4948 | 0.8471 | PASS |
| 0.02 | 0.06 | 3.4676 | 3.4948 | 0.9922 | PASS |

In slices (k_com = 6.667/Mpc): z 6->2 ratio 0.820; the band z 1.968->0.26 ratio 0.804;
z 0.26->0 ratio 0.998. The band costs less than it looks because the mode carries its
velocity through: the source term goes to ~1e-5 but the growth does not stop. So
MEDIUM_DESIGN's "linear check passes" is **confirmed**, by 10 % over the pre-registered line.

Band-centre numbers (z = 1.412): `n' = 0.03402 Mpc^-2`, `c_ad = 887.8 km/s`,
`k_J = 0.1845 Mpc^-1` (Jeans length 34.1 Mpc), `F(20/Mpc) = 1.46e-5`.

## K2 — STATIC. **FIRES on the alt footing.**

Self-consistent static clock (`h = Phi_d`, `g` from the exact form-B root at each r,
`M_pol = (a0 r^2/G) u/(1+u)`), point mass / Plummer / Hernquist, 4 masses, both footings.
`M_d(<4 R_d)/M_b` against KD1's line (0.33 canonical / 0.19 alt), and existence.

| footing | log M_b 9.4 | 10.45 | 10.7 | 10.9 |
|---|---|---|---|---|
| canonical | exists, 1.39e-4 | exists, 8.6e-5 | exists, 6.9e-4 | exists, 3.8e-3 |
| alt | exists, 1.57e-4 | exists, 1.17e-2 | **DIVERGES** | **DIVERGES** |

At log M_b 10.9 alt the iteration runs away to `M_d/M_b ~ 1e12 - 1e17`: this is COL1 Part 0's
"n = 1 Jeans core", and it arrives here because DT2's cold slope `M = 400` sits between
COL1's `mu_K = 3.71` and `mu_K = 198`, the two values at which Part 0 reports divergence.
The dust share itself is far below the line wherever the state exists.

Known answer: with the dust switched off and a point mass, `M_pol(<r)` equals form B's
`M_b X(r/r_M)` to 5.1e-3 for r > 10 kpc (10 softening lengths) and 7.2e-5 for r > 100 kpc.

## K3 — FORMATION AND REACH. **FIRES on both footings. The headline.**

The run: cold dust in Hubble flow at z = 10 at the background density, baryon point mass
(1 kpc Plummer) ramped on over 1 Gyr — COL1's own initial condition. Staggered Lagrangian
scheme on the generalised reduced system; the polarization is the exact Gauss flux of `P`,
so the scheme reproduces both limits exactly (pressureless when `s << a0` because the
polarization's gravity cancels the pressure force term by term; a normal fluid with
`c_ad = c sqrt(n/n')` when `s >> a0`).

| footing | log M_b | first fold [Gyr] | dust `q` when it folds | `c_ad` | infall `|v|` |
|---|---|---|---|---|---|
| canonical | 9.4 / 10.45 / 10.7 / 10.9 | 0.709 / **0.142** / 0.0906 / 0.0622 | 1.3e3 -> 5.3e3 | 80 -> 159 km/s | 2600-2800 km/s |
| alt | 9.4 / 10.45 / 10.7 / 10.9 | 0.669 / **0.140** / 0.0866 / 0.0601 | 1.3e3 -> 5.3e3 | 80 -> 159 km/s | 2600-2800 km/s |

**COL1's cold clock folds at 0.063 to 0.154 Gyr.** DT2 folds at 0.142 Gyr (canonical,
log M_b 10.45) and 0.062 Gyr (log M_b 10.9) — inside and at the bottom of COL1's own range.
The engineered band changes nothing.

**Why, and this is the result: a forming halo never enters the band.**

The band sits at `q` in [2, 26]. Dust in Hubble flow at z = 10 sits at `q = 1331`, already
51 times above the band's top, on the *cold* branch where `n' = M`. Collapse only raises `q`:
the run has the inner shells at `q = 5.3e3` by z = 9.8 and still rising. So the collapsing
material is always on the cold branch, and the changed compressibility — the entire content of
the construction — never acts on it. The band is at densities *below* the z = 10 background;
it is the region dust would cross if it **expanded**, which is what the background does as the
Universe expands, not what a forming halo does. The sound speed the dust actually has when it
folds is 159 km/s against an infall speed of 2604 km/s: it is cold. `DT2.lean` certifies the
two load-bearing steps of this (`dt2_band_unreachable`, `dt2_z10_above_band`).

At z = 0 the run has no settled region at all: inside ~3 Mpc the dust has collapsed to the
centre, outside it is still in Hubble flow (`q = 1.002`, `v > 0`).

**Against FLD1's and COL1's own numbers.**

- COL1: fold at 0.52 R_ta (0.51 R_ta at the shock); first crossings outside 10 kpc at z 4.1-6.2,
  outside 100 kpc at z 2.3-2.8; only 1.0-4.0 % of the law's halo charge turned around by z = 0.
  DT2 matches the fold time and matches the outcome.
- FLD1: R_fold(0) = 62 / 139 / 169 / 197 kpc at log M_b 9.4 / 10.45 / 10.7 / 10.9, and the KiDS
  inner window 1.30 / 1.95 / 2.15 / 2.32 times **beyond** R_fold(0). DT2 adds no new reach: the
  dust is on the same cold branch COL1 and FLD1 graded, so DT2's fold reach is theirs.

## Derived value

**R_set(0) = 0 kpc** at log M_b 10.45 (canonical and alt): no settled region exists. The clock
folds at 0.1420 / 0.1401 Gyr, inside COL1's 0.063-0.154 Gyr; the folding dust is at `q = 5.3e3`
against a band top of 26, with `c_ad = 159 km/s` against `|v| = 2604 km/s`.

`R_set(0) / R_fold(0) = 0 / 139 = 0` (FLD1's canonical 139 kpc), and `R_set(0) / R_KiDS = 0/272`.

## Residual per mass

`|M_settled(<r) - M_b X(x)| / (M_b X(x))` at `r` = the KiDS inner-window edge. The settled
charge is zero at every mass and footing — the run ends in a caustic before any shell settles —
so the residual is **1.0000** at all four masses on both footings:

| footing | 9.4 | 10.45 | 10.7 | 10.9 |
|---|---|---|---|---|
| canonical | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| alt | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

(Static-state requirement `M_b X` at those radii: 41.38 / 41.48 / 41.40 / 41.43 M_b canonical;
45.54 / 45.65 / 45.56 / 45.59 M_b alt. Delivered: 0.)

## Lean

`DT2.lean`: 19 theorems, exit 0 (`DT2.out`). `DT2_MUTATE.lean`: 7 false statements, 7 errors,
exit 1 (`DT2_MUTATE.out`). Load-bearing: `dt2_dxdq_pos` and `dt2_nprime_in_band` (the interval
is exactly `{q : B'(q) > 0}`, and `n' < M` there); `lawon_force_balance` (the cancellation that
makes the clock fall as test particles, for a general kinetic function); `lawon_dispersion` and
`lawon_suppression` (K1's growth source); `polar_gauss` and `polar_is_formB` (the halo is the
Gauss flux of `P` and equals form B's `M_b X` exactly); `dt2_band_unreachable` and
`dt2_z10_above_band` (the decisive point of K3).

## What this does and does not say

It says the specific engineered function the record named does not reach its static state, and
why: its one new ingredient is placed at densities a collapsing halo never visits. It does not
say every kinetic function fails — `q1`, `q2` and `L` are free, and a band placed *above* the
z = 10 background would be visited by collapsing dust. That placement is not DT2 as the record
wrote it, and it was not graded here. It also does not reach a verdict on shells that turn
around after z = 1.97, which do start inside the band: the run's central fold happens long
before, and the single-stream equations give no answer past it.

## Files

`FROZEN_CRITERIA.md`, `dt2_function.py`, `dt2_linear.py` (+`.out`), `dt2_static.py` (+`.out`),
`dt2_form.py`, `dt2_run.py` (+`.out`), `dt2_reach.py` (+`.out`), `DT2.lean` (+`.out`),
`DT2_MUTATE.lean` (+`.out`), `RESULT.md`.
