# QX12 iter_1: the barotropic no-go does NOT fire. The triangle leaves a depth window (ALIVE, static only)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: ../FROZEN_CRITERIA.md and FROZEN_CRITERIA.md
(7a1afa9b6b), committed alone before any code. Script qx12_i1.py (one thread, about 1 min); MUTATE qx12_i1_MUTATE.*;
post-result checks qx12_i1_post.* (declared after the main output; they cannot change the label).
Lean: fable_independent_2026/lean_2026/QX12_triangle.lean (+ _MUTATE twin).

## The theorem tested

A barotropic sector (p = p(rho, t), any equation of state, any time dependence) in hydrostatic equilibrium with the
cosmic sea has rho_X = H_t(D) at every point of every system. D is the depth below the sea and H is nondecreasing
(Lean `baro_order`). The bounds are galaxy upper bounds u (local <= enclosed mean) against hot-system lower bounds l
(local >= outer shell mean). If a galaxy point at least as deep as a hot point allows less sector than the hot point
needs, the whole class is dead (Lean `baro_nogo`).

## Result (both footings agree)

| | canonical | alt |
|---|---|---|
| allowed points (KiDS 59 + ellipticals 21) | 80 | 80 |
| hot points with l > 0 (X-COP pairs; no group shell has l > 0 at 2 sigma) | 22 / 48 | 22 / 48 |
| conservative depth, galaxies (max) | 1.87e5 (km/s)^2 | 1.87e5 |
| conservative depth, hot points with l > 0 (min) | 6.07e6 | 6.25e6 |
| violating pairs | **0** | **0** |

Label as frozen: **ALIVE**, on both footings and in the same-epoch subset. With the depth measured from the TOTAL
observed mass out to the turnaround radius, X-COP sits 32-33 times deeper than any galaxy point, even with the depths
skewed against the result. So no galaxy is deep enough to contradict a cluster, and a barotropic sector whose density
rises steeply with depth can keep galaxies clean while filling clusters. This differs from QX5 key a and QX6, where
groups overlapped galaxies. Those keys measured depth from the baryons with a fixed acceleration cut. Depth to the sea
through the total mass is a different key, and it separates the two.

What this does NOT say: it is a static, equilibrium statement. It does not test growth (T1 late), which killed QX3
iter3's power-law barotropic family, or the formation history, which killed QX10's n = 1 window. Groups give no
positive lower bound at 2 sigma from a two-radius shell, so this test does not constrain them.

## Known answers and controls

- KA1: inverse of the law exact to 2.2e-16 (Lean `law_inverse`). KA2: zero sector recovered to 3.5e-16. KA3: X-COP plain law
  +0.4675 / +0.4345. PASS.
- M1 (specificity): a planted universal sector (constant H = 1e3 Msun/kpc^3) gives 0 violations. BITES.
- M2 (bounds x1e3): 0 -> 0. **Vacuous as frozen**: with zero violations nothing can drop. The frozen M2 was written
  for a DEAD outcome. On the record as not biting.
- Post-result M3 (power, declared after the main output): scaling every hot depth by s. Violations appear once the
  depths overlap the KiDS points: s = 0.01 gives 8 (max l/u 7.7 / 9.2), s = 0.003 gives 158 / 146. The test can fire;
  here it does not, because the data put the hot systems 30x deeper.
- MUTATE output byte-identical across the post-check run (md5 59bc82ae4496).
- Lean QX12_triangle: 5 theorems (law_inverse, baro_order, baro_nogo, iso_ratio, iso_profile), standard axioms only.
  The MUTATE twin fails on all 3 false claims.

## What it implies for the next iteration

The window points to a specific sector: in clusters the sector must be hot at about the cluster's own temperature (an
extended profile across D of about 5e6-2.5e7 (km/s)^2 needs dh/dln rho of about 3e6, so c_s of about 1800 km/s). In
galaxies (D <= 2e5) it must hold almost nothing. One isothermal sound speed does both:
rho = rho_sea exp(D/c_s^2) (Lean `iso_profile`). That is iter_3, with c_s fixed by galaxies alone and clusters
predicted.
