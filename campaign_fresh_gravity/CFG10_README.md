# CFG10 — what sets the cold component inside the baryons

Script: `CFG10_inner_closure.py`, about 20 s.
- Outputs: `CFG10_inner_closure.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. The closures' a₀ is doubled inside the ODEs, so C3 fails (rc = 1).
- The main run also exits 1, because H1 fails as its declared expectation said it would.

κ = ½ is fitted. Both footings are used.

## The question

CFG9 derived the kernel P2 outside the baryons: a locally virialized cold component whose charge per unit baryonic mass is a₀/4π. It also showed that a *constant* charge overshoots inside real baryons.

Two principles extend the point-mass result into the baryons with no new constant. Both are exact for a point mass. Here u = r²g and u_N = GM_b(<r), with the baryons treated as spherical-equivalent.

| principle | cold density | ODE |
|---|---|---|
| (i) pressure Gauss law: 4πr²P = (a₀/2) M_b(<r) | ρ_c = −a₀ g_N′/(8πG g) | u u′ = u u_N′ + a₀ r u_N − (a₀r²/2) u_N′ |
| (ii) shell theorem for the charge: only baryons inside r count | ρ_c = a₀ g_N/(4πG r g), i.e. ρ_c g = (a₀/3) ρ̄_b(<r) | u u′ = u u_N′ + a₀ r u_N |
| P2 (the declared law), differentiated | — | u u′ = u_N u_N′ + a₀ r u_N + (a₀r²/2) u_N′ |

**Exact identity (C4).** P2's cold density equals (ii)'s plus ρ_b(u_N + a₀r²/2 − u)/u.
- The added term is ≥ 0 (AM–GM).
- It tracks the local baryon density.
- It vanishes wherever the baryons end, and also in the Newtonian limit.

So (i) subtracts that local term, (ii) omits it, and P2 adds it.

## The statistic

The statistic is CFG4 H2's, which is the record's `rar_framework_a0_mlfit` statistic:
- the weighted rms of log₁₀(g_obs/g_pred);
- over all 175 SPARC galaxies;
- at one global Υ_disk (with the bulge at 1.4Υ), on a grid from 0.30 to 1.20.

How a closure is scored:
- **Prediction at a data point.** g_bar(point) + GM_c(<R)/R².
- **Cold mass.** It comes from the closure's ODE, integrated on the monotone envelope of the spherical-equivalent baryonic mass.
- **Inner extension.** Inside the first data radius, V_bar² ∝ r (a declared constant central surface density).
- **Fair baseline.** P2 computed in the same additive-envelope form, labelled "P2-env".

## Results

| check | result |
|---|---|
| C1: CFG4's committed rms and Υ (P2, ν_mono, both footings) | reproduced to 1e-17, Υ exact |
| C2: P2 as an ODE equals P2-env at every data point | 4.1e-7 |
| C3: point mass, both closures equal P2 (0.01–100 r_M) | 1.3e-12 |
| C4: the identity holds at every grid radius of every galaxy | min −3.5e-14 relative |
| **H1: (i) pressure Gauss law** within +0.005 dex of P2-env | **FAILED as expected**, +0.168 / +0.175 dex (canonical / alt). **Kill line (+0.02) crossed: excluded as the inner principle** |
| **H2: (ii) shell-theorem charge** within +0.005 dex of P2-env | **PASS**, +0.0031 / +0.0017 dex |
| R0: data points where a closure's total mass breaks down | (i): 226 / 227; every other law: 0 |
| R1: where (i) demands ρ_c < 0 | a median 25% of the radii, in 116 of 175 galaxies |
| R2: median inner residual at g_bar > a₀ | P2 −0.088 / −0.079; (ii) −0.090 / −0.081; ν_mono −0.063 / −0.061; (i) −0.121 / −0.167 |

Best fits (rms at best Υ):

| law | canonical | alt |
|---|---|---|
| P2 algebraic | 0.1083 (Υ 0.70) | 0.1035 (Υ 0.65) |
| P2-env | 0.1081 | 0.1034 |
| (ii) | 0.1112 (Υ 0.71) | 0.1052 (Υ 0.66) |
| ν_mono | 0.1003 | 0.0991 |

Every law shares the inner offset of about −0.08 dex. That is the single global Υ, not the closure.

## Disclosure

The first run was the MUTATE run. It exposed a singular start in galaxies whose total V_bar² is ≤ 0 at the first radius, which happens with central HI holes at low Υ.

Two fixes were made before the main run:
- **Mass floor.** The enclosed baryonic mass is now floored at the stellar part. The gas's negative V² comes from the disc geometry, not from negative mass.
- **Breakdown points.** A point where a closure's total mass breaks down is penalized (its prediction floored at 1e-3 g_bar) and kept in the statistic. It is never dropped. These points are reported as R0, which was added with the fix.

The hypotheses were not changed.

## Standing

**The inner mechanism CFG7/FG004 asked for is not a separate ingredient.**
- FG004 found that a relaxed cold component overshoots at g_bar > a₀. That overshoot came from assuming a constant charge, which makes the component an isothermal core.
- With a charge obeying a shell theorem, where only the baryons inside r source the cold component at r, the component sits where the galaxy law needs it. Its inner residual equals P2's.

**One statement then generates the galaxy law:** the cold component's weight density is ρ_c g = (a₀/3) ρ̄_b(<r).
- Outside the baryons it is exactly P2, and the component is locally virialized there, as CFG9 showed.
- Inside the baryons it matches P2 on SPARC to 0.002–0.003 dex.
- P2 differs from it only by the non-negative local term in the identity, and the data cannot separate the two at that level.
- ν_mono still fits better than both.

**What stays open:**
- Why the cold component takes this distribution. This needs a dynamical derivation, for example from the dark sector's own field equation.
- The fitted κ.

Nothing here says the theory is closed.
