# L22 — the solenoidal (curl) part of the QUMOND field in clusters

`L22_curl_field.py` (**8 controls PASS, 2 FAIL — and the two FAILs are the finding**).
Run: `L22_curl_field.out`, 137 s.

Two things in this directory rested on a piece of QUMOND nobody here had computed. `L2_cluster_inverse.py`
inverted the static law on the corrected X-COP profiles using **Gauss's theorem on a sphere**, i.e. assuming
the solenoidal part of the field is zero, and FINDINGS.md carries that as an untested caveat.
`L1_caustics_and_cap.py` found the algebraic multiplier ν(|g_N|)g_N is not merely approximate on a non-radial
field — it circulates 5.7e-3 of the path integral around a closed loop and unbinds a system within 1 Gyr —
and said the fix is a real QUMOND field solve. This lane builds that solve, twice, and answers both.

## The structural result

QUMOND is `lap(Φ) = div[ν(|grad Φ_N|) grad Φ_N]`. Writing the physical field `a = −grad Φ` and the algebraic
field `W = ν(|a_N|)a_N`, the field equation says `div a = div W`, so the difference

    a_S ≡ a − W        satisfies    div a_S = 0    identically.

Therefore the flux of `a_S` through **any** closed surface vanishes. On a sphere that is `4πr²⟨a_S·r̂⟩`, so

> **⟨a_S·r̂⟩ = 0 exactly, at every radius, for every source geometry, at every axis ratio.**

The sphere-averaged radial field is *precisely* what L2's inversion uses and what a hydrostatic mass estimate
approximates. **Gauss's theorem is the operation that annihilates the solenoidal field.** L2 did not neglect a
small term; it used the one quantity the term cannot touch. Verified numerically to 2.5e-4 (the solver's own
round-trip floor on a spherical control) at q = 1.0 → 0.4 and in four merging configurations.

What geometry *does* change is a different thing: the **nonlinear angular average of W itself**, since
`⟨ν(|a_N|)a_N·r̂⟩ ≠ ν(⟨a_N·r̂⟩)⟨a_N·r̂⟩`. That is real, it is computed here, and it is small.

## The solvers

Two, sharing no code, each validated against closed-form results.

- **A, axisymmetric multipole.** Legendre in μ = cos θ, logarithmic in r, exact interior/exterior Green's-function
  radial integrals evaluated by a geometric-grid recursion (so no radial truncation, no overflow at large l).
  Five decades in radius; handles spheroids, discs and on-axis mergers.
- **B, Cartesian FFT.** Isolated boundaries by zero-padded convolution with a cell-averaged free-space
  Green's function, 4th-order differences, 224³ cells over 10 Mpc. Handles genuinely triaxial a ≠ b ≠ c.
  Solved as `a = W_sph + δa` with `div δa = div δW` so the box truncation only touches the fast-decaying
  non-spherical part. (At L = 6 Mpc the solenoidal fraction at 1200 kpc is depressed by half; at 10 and 16 Mpc
  it is stable — box size, not resolution, is the binding constraint.)

Controls, all PASS: Hernquist Newtonian field to 2.5e-3; Miyamoto–Nagai in-plane Newtonian force to 3.2e-3 for
r > 3b (with the stated limit that a Legendre series resolves a disc poorly inside its own half-thickness —
0.1 between b and 3b, which is why every galaxy model below carries its own version of the check); the spherical
QUMOND source returns the algebraic answer to 1.6e-3 with no solenoidal part; the Newtonian limit returns g_N to
2.3e-3; the two solvers agree on the local solenoidal fraction to 8.4% and on the mass bias to within solver B's
own spherical floor; refining l_max 32 → 56 moves the answers by under 3%.

**Conservativity (V4).** On the same closed loop in a q = 0.6 cluster: the Newtonian field circulates 3.5e-6,
the **solved QUMOND field 4.3e-6** — the two are at the same floor, which is the loop evaluator's cubic-spline
interpolation error, since both are exact gradients — and the **algebraic multiplier 9.4e-3, 2179× larger**.
L1's defect is reproduced independently, at 1.6× the size L1 measured with the g04k rule on a galaxy loop.

## The size of the solenoidal field

Ellipsoidal stratification of the corrected X-COP baryon profile (median of the seven clusters with a stellar
profile), at fixed mass inside every ellipsoid. Axis ratios: the X-ray gas is rounder than the total matter —
roughly 0.7–0.9 for the ICM inside R500, roughly 0.6–0.7 for the total mass in triaxial analyses (Lau, Nagai,
Kravtsov & Zentner 2011; the Limousin et al. 2013 review; Sereno et al. 2018, CLUMP-3D). Rather than lean on one
number the scan brackets all of them; q = 0.7 is quoted as the headline and is **flatter** than the gas is
typically measured to be.

| q = c/a | local \|a_S\|/\|a\| (40–1500 kpc) | ⟨a_S·r̂⟩/⟨a_r⟩ | mass offset, dex | emission-weighted B |
|---|---|---|---|---|
| 1.0 (control) | 0.00% | 1e-4 (floor) | 0.0000 | 1.0001 |
| 0.9 | **0.9%** | 1e-4 | 0.0001 | 1.002–1.003 |
| 0.8 | **2.0%** | 1e-4 | 0.0005 | 1.000–1.005 |
| **0.7** | **3.1%** | 1e-4 | **0.0012** | 0.994–1.003 |
| 0.6 | 4.4% | 1e-4 | 0.0025 | 0.987–0.998 |
| 0.5 | 5.7% | 1e-4 | 0.0044 | 0.978–0.986 |
| 0.4 | 7.1% | 1e-4 | 0.0074 | 0.956–0.967 |

The genuinely triaxial case (solver B, 1 : 0.85 : 0.65) sits with the oblate q = 0.7 case: 2.6% solenoidal
fraction, B = 0.996–0.997.

**Mergers.** Inside the pair the curl field is large — **14% of the total at 0.3 separations, 27% at 0.14** for
a 1:1 merger, and the mass offset there reaches **−0.14 dex**. Beyond twice the separation it falls below
0.0002 dex. The sphere-averaged radial solenoidal component is still zero (5e-4) throughout. X-COP is a relaxed
sample, so this is an upper bound on what the audited rows can contain, and the large inner numbers are the
nonlinear-averaging effect, not the curl.

## THE TEST — does it move L2?

L2's C5 compares two *measurements* of Δ = (g_obs − g_bar)/a₀ at the same s. The curl field is a *theory* effect:
it says the field predicted from a given baryon distribution is not ν(g_N)g_N. That applies to **discs as well as
clusters**, and discs are far flatter, so both sides are corrected. With `B = g_true/g_alg`,

    Δ_meas = B·Δ(s) + (B−1)s      ⇒      Δ_required = [ Δ_meas + (1−B)s ] / B.

Galaxy side: each of the 144 SPARC galaxies (L2's own selection) gets a Miyamoto–Nagai disc matched to its
baryonic mass and [3.6] disc scale length, b/a = 0.15, with b/a = 0.075 and 0.30 as the systematic — a pure disc
with no bulge and the gas as flat as the stars, which **overstates** the galaxy correction, the direction that
would help the rescue. In-plane B: median 0.978, 16–84 pct [0.928, 0.995]. Each model is checked against the
analytic MN force at its own SPARC radii (95th percentile 1.2e-3; at most 2 of 2681 points left uncorrected).

This script reproduces L2's headline exactly before any correction — ratios 2.25, 3.35, 4.27, 4.34, 4.42, 5.08
and worst |z| = 13, against L2's 2.2–5.1 and |z| = 13.

| cluster q | disc b/a | ratio range after | worst bin move | median move | worst \|z\| |
|---|---|---|---|---|---|
| — (L2) | — | 2.25 – 5.08 | — | — | 13 |
| 0.90 | 0.150 | 2.20 – 4.73 | +8.6% | −3.6% | 12 |
| 0.80 | 0.150 | 2.20 – 4.73 | +8.6% | −3.5% | 14 |
| **0.70** | **0.150** | **2.21 – 4.74** | **+8.4%** | **−3.4%** | 14 |
| 0.70 | 0.075 | 2.21 – 4.75 | +8.4% | −3.4% | 13 |
| 0.70 | 0.300 | 2.21 – 4.76 | +8.0% | −3.3% | 13 |
| 0.60 | 0.150 | 2.21 – 4.75 | +8.2% | −3.1% | 13 |
| 0.50 | 0.150 | 2.22 – 4.77 | +7.9% | −2.7% | 13 |

- **T1 FAIL.** The largest change in any bin, over every axis ratio, both disc thicknesses, both footings and both
  cluster subsets, is **8.6%** — against the 20% the check demanded and the factor of 2 a rescue would need.
  The headline median is **−3.4%**.
- **T2 PASS.** The correction does *reduce* the ratio, by a few per cent, and only because the same effect is
  larger for the flatter discs on the other side.
- **T3 FAIL.** The smallest cluster/galaxy ratio moves from 2.25 to 2.20: **3.9% of the excess over unity removed.**
- Worst |z| does not improve: 13 before, 12–14 after.

**The converse, determined not assumed.** The sign is negative on both sides — the true QUMOND field is *weaker*
than the algebraic multiplier, because ν(|g_N|)|g_N| is concave and the angular spread of |g_N| over a sphere
lowers its mean. So the boost clusters **require goes up**, by +0.27% (median) and +1.16% (worst) across
q = 0.9–0.5. The curl field makes the cluster problem marginally **worse in absolute terms** and marginally
better only in the ratio.

## Verdict

The solenoidal field is a real, few-per-cent field in a flattened cluster and a tens-of-per-cent field inside a
merging pair, and the algebraic multiplier that ignores it is non-conservative at 9.4e-3 per loop — so L1's
warning stands and any future non-radial, orbit-integration or lensing calculation in this programme must solve
for it. But it is invisible to the one quantity L2 used: div a_S = 0 makes its flux through every sphere vanish
identically, so the enclosed-mass inversion is exact against it at any axis ratio and in mergers. Including it
on both sides of L2's comparison, with geometry taken from the measured range rather than tuned, moves the
2.2–5.1× cluster/galaxy discrepancy by at most 8.6% in any bin and −3.4% in the median, closing 3.9% of the gap
while pushing the absolute cluster requirement slightly the wrong way. **L2's stated caveat is discharged and its
impossibility result stands.**

## Untested, stated rather than closed

- The **hydrostatic estimator's own triaxiality bias** — an observer azimuthally averaging X-ray data does not form
  the plain sphere average. The emission-weighted column above gives its size in this model (under a per cent at
  the gas axis ratios, ~1.5–2% at q = 0.5), but a proper treatment needs projection along a line of sight and a
  real emissivity, which this lane does not do. It is a measurement systematic common to every gravity theory,
  not a curl effect.
- **Substructure below the smooth ellipsoid.** Clumps on scales well under 100 kpc are not in these models. They
  raise the local solenoidal fraction; by the same theorem they cannot change the sphere-averaged radial field.
- The galaxy-side correction uses a single Miyamoto–Nagai component per galaxy. A proper treatment would use each
  galaxy's own gas and stellar surface densities. The direction of that refinement is to *reduce* the galaxy
  correction (bulges are round, gas is flared), which would shrink the −3.4% further.
