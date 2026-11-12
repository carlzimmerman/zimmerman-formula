# ELA1 RESULT: ELASTIC SOLID FAILS AT S0 (+S2, B1) / ELASTIC SOLID FAILS AT S0 (+S2, B1)

TEST lane, quarantined. Relabels nothing, adopts nothing, not registered. kappa = 1/2 FITTED; not
theory closed. Footings canonical (a0 = 9.3603e-11) and alt (1.1312e-10) graded separately, never
pooled; both give the same label. Cold dark energy is a gravitating field component, never a
particle; in this lane it was hypothesised to be an isotropic elastic continuum, and that is what
was graded. Criteria committed alone before any script (`FROZEN_CRITERIA.md`); `AMENDMENT_A1.md`
(post hoc, committed alone) corrects two things in the hand estimate, one of them a sign that
changes the outcome of the gate pre-registered as most likely to kill.

## Labels

| item | canonical | alt |
|---|---|---|
| S0 the deformation (strain / density contrast) | **FIRES** | **FIRES** |
| S1 sound speeds (imaginary or superluminal) | holds | holds |
| S2 the energy (W = J) | **FIRES** | **FIRES** |
| B1 the Bullet | **FIRES** | **FIRES** |
| S3 clusters (reported) | melts, 6/6 rows | melts, 6/6 rows |
| S4 recombination (reported) | passes trivially | passes trivially |
| **overall** | **ELASTIC SOLID FAILS AT S0 (+S2, B1)** | **ELASTIC SOLID FAILS AT S0 (+S2, B1)** |

## Answer to the five questions asked

**(1) Is it a solid with a shear modulus proportional to the field, and is that local?**
Yes to the first half, yes to the second. The material Cauchy stress is **sigma = -Pi** (decided by
the force balance, KA9: `div(-Pi)/(rho_c g) = +0.999991` against `div(+Pi)/(rho_c g) = -0.999991`
on all 24 rows). It is an isotropic elastic solid with

    mu_s = +(3/2) J(g) (rho_ref/(3 rho_c))^(1/3)          (deep field; S1c ratio 1.001-1.008 at x=60)

i.e. the shear modulus **is proportional to the field's own energy density J** (which is g^2/8piG in
the deep field), times a factor set by the local density. That is a *local* constitutive relation:
S1c shows the halo-derived mu_s collapses onto this one function of (rho_c, g) across the point
mass, Plummer and Hernquist profiles at all four masses and both footings. So M5's three hypotheses
all hold — local, momentum-conserving (symmetric stress, force density div sigma, no hold),
normally self-gravitating (rho_c in Poisson) — and **M5's NO-GO applies.**

What the solid actually buys: the transverse mode propagates, so **M5's S4 Hadamard ill-posedness
(s^2 = i k g) is cured.** That is a real gain and it was not what the criteria expected.

**(2) Sound speeds.** One longitudinal, one transverse, both **real, positive and subluminal
everywhere on the graded window**:

    c_T^2 = mu_s/rho_c ,  c_L^2 = (lambda + 2 mu_s)/rho_c
    max over all 24 rows:  c_T = 69.3 km/s ,  c_L = 83.9 km/s      (c = 2.998e5 km/s)
    rows with c_T^2 < 0 :  0/24      rows with c_L^2 < 0 :  0/24     rows above c :  0/24

No ghost, no gradient instability, no superluminality. **This gate, pre-registered as the most
likely to kill, did not fire.** (The deep-field scaling is c_T^2 ~ (3/4) v_inf^2 / y with y = R/r;
extrapolated past the halo it would reach c only near 1e8 kpc, far outside any physical halo, and
the halo itself ends where its mean density meets the background at a few Mpc, where c_T ~ 100 km/s.)

**(3) Recombination.** Passes, and vacuously. The medium has no non-gravitational coupling to the
plasma by construction, so the drag bound that killed MEDIUM_DESIGN section 3 never arises. In the
exactly homogeneous background g = 0, so mu_s = 0: the medium is a shear-free dust, and a solid
with zero shear modulus is not a solid. For any perturbed g != 0 the moduli turn on positive and
the elastic Jeans length is 5e-12 to 6e-8 Mpc at z = 1100 — far below the acoustic scales, so
nothing obstructs clustering at recombination. The gate costs nothing and buys nothing.

**(4) The Bullet. FIRES, and this is the sharpest kill.** Two independent routes:
- *Structural.* A solid's map from its reference configuration is a homeomorphism: material
  elements keep their neighbours. The two clusters have passed through each other and RB1 places
  each cluster's cold mass with its galaxies, so at the observed epoch the two media occupy the
  same volume — the map is 2-to-1 there. The interpenetrated cold mass the data require is at least
  the subcluster's 1.47e14 Msun. A homeomorphism cannot deliver any nonzero value.
- *Dynamical.* At v = 4700 km/s the elastic Mach number is 7-22 and the yield parameter
  Y = rho_c v^2/|mu_s| is **76 to 478** across the cluster rows: the impact exceeds the shear
  strength by two orders of magnitude. **Horn picked: the solid yields.** A yielded solid is a
  fluid, and that fluid is local, momentum-conserving and normally self-gravitating — M5's class,
  whose NO-GO already covers it. The candidate's defining property is lost exactly where it is
  needed most.
- Reported, and worth flagging: DB1's own two tests (`Sigma_c >= 3 x` the swept ICM column, and
  `G Sigma_c^2 >= rho_ICM v^2`) both **PASS** for the solid. They are self-gravity tests and are
  blind to solidity. A component can satisfy every criterion the record currently uses for
  "collisionless in the Bullet" and still be unable to pass through.

**(5) Clusters. Cannot be hot and solid.** c_T^2 in the cluster regime is 4.6e4 to 2.9e5 km^2/s^2
against the sigma_v^2 = 1e6 (1000 km/s) the data require: the elastic sound speed is 2 to 5 times
smaller in speed than the dispersion it must carry, so the medium **melts in 6/6 rows**. "Full
share" is satisfied by construction for any real-mass medium and carries no information here.

## Why S0 fires (the label's first item)

Mass conservation alone, before any constitutive law, fixes the deformation: with rho_ref the
uniform reference density, R(r) = [3 M_c(r)/(4 pi rho_ref)]^(1/3) and

    u_tt = 1 - R/r ,   u_rr = 1 - dR/dr ,   u_rr - u_tt = (R/r)(1 - rho_c/rho_bar_c) > 0

The law's halo needs a density contrast of 1.0e3 to 7.6e6 over the reference (bracketing rho_ref
from z = 0 to z = 10). In the deep field R ~ r^(1/3), so the contrast is y^3/3 with y = R/r: the
strain required is |u_tt| = y - 1, i.e. **11 to 249** (worst row, both footings). Numbers:

| rho_ref | y at r = r_M | max \|u\| over all rows | contrast | map folds |
|---|---|---|---|---|
| z = 0 (33.9 Msun/kpc^3) | 63-126 | 249 | up to 7.6e6 | no |
| z = 10 (4.5e4) | 5.7-11.5 | 21.7 | up to 5.7e3 | no |

A linear elastic solid cannot deliver any of this: with |u| <~ 1 the density contrast is at most of
order 1, against 1e3 to 1e7 required. The map does not fold (good — a solid's map must not), but
the strain is 20 to 250, so the elastic description is inapplicable to its own solution. The
conclusion survives every rho_ref bracket in the frozen range; at the M5 arm's extreme (z = 1100)
the strain does fall below 1 (0.999), which is why M5 exists as a bracket and why the S1 verdict
was not allowed to rest on it.

## Why S2 fires

For a quadratic elastic energy 2W = sigma:u, so with sigma = -Pi and W = J the condition reads
`-Pi_rr u_rr - 2 J u_tt = 2J`. On the mass-conserving strain the left side is (J/2)(5y/3 - 1):

    W/J over the window: 3.6 to 241   (never within 1 % of 1, in any row, either footing)

So C1 (stress = -Pi), C2 (energy = J) and C3 (mass conservation) cannot hold together. W is
positive — there is no negative-energy pathology — but it is 4 to 240 times J, and J itself is the
pressure of FB1's isothermal halo, not a strain energy. Dropping C3 and integrating the C1+C2 ODE
`Pi_rr xi' + 2 J xi/r = -2J` does not repair it: the deep-field family is xi = -2r + C r^2, whose
C = 0 member is a pure dilation against an anisotropic stress (mu_s = infinity) and whose C != 0
member folds and gives a negative, then r^3-growing, density against the law's r^-2.

## Known answers and mutation arms

KA1-KA5, KA7, KA8, KA9 all PASS (KA1 to 1e-4 on the corrected (2/3)u; KA9 to 1e-2 on the sign;
KA3 to 1.7e-14; KA4 to 2.1e-14; KA7 checks the residual falls as a0). All five mutation arms bite:

| arm | mutation | required | result |
|---|---|---|---|
| M1 | sigma sign flipped | equilibrium fails | BITES (div sigma/rho g = -1.000) |
| M2 | Newtonian field | misses the law | BITES (0.915 dex vs 0.066 line) |
| M3 | isotropic P = J (kinetic reading) | mu_s = 0 and misses the law | BITES (0.382 dex vs 0.066) |
| M4 | mu_s forced negative | equilibrium fails | BITES (0.293 off) |
| M5 | rho_ref at z = 1100 | strain < 1 but the sign does not change | BITES (0.999; mu_s > 0 throughout) |

M5 is the arm that shows the two arguments are not the same strength: **S0's strain argument
depends on rho_ref, S1's sign argument does not.**

## What this lane says about MEDIUM_DESIGN's four properties

| property | the elastic solid |
|---|---|
| conserved, cold, 5.41 x baryons, expanding universe | satisfied by construction (real mass, no coupling); the elastic Jeans length is negligible |
| passes through itself and through gas (Bullet offset) | **FAILS** — a homeomorphism cannot interpenetrate; and it yields at 4700 km/s |
| hot and at full share in clusters | **FAILS** — melts (c_T 2-5x too slow); full share is free |
| locked to the baryons in galaxies, no second halo | the stress is forced to -Pi(g), density-blind, so the shape is right; but the state is unreachable (S0) and the energy is not J (S2) |

## Files

`FROZEN_CRITERIA.md` (committed alone first) · `AMENDMENT_A1.md` (post hoc) · `ela1.py` ·
`ela1.out` · `ela1.json` · `ela1_MUTATE_M{1..5}.out/.json` · `RESULT.md`.

One thread, `nice -n 10`, no downloads, runs in about 0.3 s.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
