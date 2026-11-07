# NA1: the last two untested FA1 doors. I5 (disformal bulk-motion selector) is DEAD BY REDUCTION and I7 (defect network of the a0 scalar) is DEAD, both footings

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle. Footings graded separately, never pooled.

- Criteria: FROZEN_CRITERIA.md, committed and pushed alone before any script or number (origin a7e267c3c3).
  Amendment A1 (AMENDMENT_A1.md) was committed after the first run and before the rerun. It restates KA7's known
  answer and lowers memory use; nothing graded changed (see "Post-freeze").
- Script: na1.py. SV5's sv5_web is imported read-only and FA3's fa3.json is read-only. It runs on one thread at nice
  15 in about 50 s.
- Outputs: na1.json / na1.out (log run_main.txt) and na1_MUTATE.json / na1_MUTATE.out (log run_mutate.txt). The
  KA-stopped first run is kept as run_main_KAstop.txt.
- Peak RSS: 0.858 GB main and 0.812 GB MUTATE (ru_maxrss; footprint 0.47 GB). Both are under the 1 GB line.

**Label line: I5 DEAD BY REDUCTION / DEAD BY REDUCTION; I7 DEAD / DEAD (canonical / alt).**

## Known answers (all PASS, both footings)

| KA | canonical | alt | line |
|---|---|---|---|
| KA1 web code, F = 1, reproduces SV5 iter_1 r | 74.742402 (rel 0) | 89.362969 (rel 0) | 1e-6 rel |
| KA2 F = 0 gives r = 1 | \|r-1\| 0 | 0 | 1e-9 |
| KA3 sympy: g~(U,U) = -1 + B X gamma^2; light cone of g~ c~/c = sqrt(1 - B X) | True | True | exact |
| KA4 linear velocity parallel to g_N, every ZG | min \|cos\| 1.00000000 | same field | 0.999999 |
| KA5 eta -> rho_DE -> a0 round trip | 0 | 1.1e-16 | 1e-12 |
| KA6 sympy: frozen w -1/3, -2/3 give a^-2, a^-1; scaling rho ~ H^2 gives w_def = w_tot | True | True | exact |
| KA7 (A1-1) solver w_tot vs two-fluid value at z 1e5 / 3400 / 50 | 0.3225 / 0.1674 / 0.0050, \|d\| < 1e-4 | (one background) | 0.003 |

## I5: disformal bulk-motion selector, DEAD BY REDUCTION (both footings)

**The action, made definite.** g~ = g + B(X) d phi d phi = g + B X u u, with phi the khronon. Two placements:
- P1 (Phase 1's text): matter on g, and the extra-gravity weight is F(Y) for any local scalar Y.
- P2 (TeVeS-like): matter on g~.

**R, the reduction (sympy, na1.json `I5.R`).** I built every scalar from (g, g~, u, X, U, T^mn) and checked each one.
They depend on the matter velocity only through |v|, so every one is a function of {gamma = -u.U, X, B, rho, p}:

| scalar | value |
|---|---|
| eigenvalues of g^-1 g~ | {1 - B X, 1, 1, 1} |
| det g~ / det g | 1 - B X |
| g~(U,U) | B X gamma^2 - 1 |
| g~^-1(U,U) | (B X gamma^2 - B X + 1)/(B X - 1) |
| g~_mn T^mn | B X gamma^2 (rho + p) - B X p + 3p - rho |
| tr(T g~ T g~) | polynomial in B X, gamma^2, rho, p |

So F = F(gamma; X, p/rho), and each argument is already on the dead list:
- gamma is the khronon velocity (QX5 iter_c).
- p/rho is a dead key (QX5 iter_b and the record).
- X is the clock depth (QX5 iter_a and QX6).

The gamma-dependent part of g~(U,U) is B X s^2 (1 + s^2) + O(s^6), with s = v/c. That is DX1 D1's (v/c)^2 <= 1.1e-5,
multiplied by B X.

**GW170817.**
- P2: photons ride g~ and gravitons ride g, so dc/c = 1 - sqrt(1 - B X). GW170817 (PROVISIONAL bound) then gives
  B X in [-6.2e-15, +1.3e-15]. The selector's argument can vary by at most 6.8e-20 across all classes, so P2 FAILS as a
  switch. This is the TeVeS failure in AX1.
- P1: photons and gravitons both ride g, so c_T = c_light. PASS (CONDITIONAL on no photon coupling to g~).

**The reduced key, graded anyway.** All low-z hosts share one flow, drawn from SV5's own z 0.25 linear velocity field:
mass-weighted median 456 km/s, p95 829 km/s, growth f 0.681. Each class adds its internal motion: SPARC rotation is the
on-disk max V_obs, and the other motions are PROVISIONAL constants.

| class | speed median (p5 to p95), km/s |
|---|---|
| CMB z 3400 | 15 (1.5 to 28) |
| SPARC | 475 (184 to 865) |
| X-COP ICM | 550 (213 to 997) |
| groups | 480 (186 to 874) |
| M31 dSphs | 480 (185 to 874) |
| Coma UDGs | 1605 (621 to 2912) |

| row | canonical | alt |
|---|---|---|
| **S1**, increasing F: SPARC FOSD CMB (max CDF excess 0.0000), so <F>_CMB <= <F>_SPARC | need CMB >= 1 vs SPARC <= 0.33: **contradiction** | >= 1 vs <= 0.19: **contradiction** |
| **S1**, decreasing F: UDGs FOSD SPARC (excess 0.0000), so <F>_UDG <= <F>_SPARC | need >= 23.6 vs <= 0.33: **contradiction** | >= 20.2 vs <= 0.19: **contradiction** |
| **S1 reading A** (F weights the dust) | **FAIL: no monotone F** | **FAIL** |
| W1 reading A (phantom untouched) | r 74.742, **FAIL** (line 1.072) | r 89.363, **FAIL** |
| **W1 reading B** (F weights the law's phantom), increasing step on for v >= 240.0 / 286.5 km/s (G1 host fraction q 0.883 / 0.816) | r **72.184**, **FAIL** | r **84.635**, **FAIL** |
| **W1 reading B**, decreasing step on for v <= 719.6 / 652.2 km/s | r **74.311**, **FAIL** | r **85.773**, **FAIL** |
| S2 LP (increasing F, CMB row dropped) | **NO VERDICT** (feasible, tail-dependent) | **NO VERDICT** |

- **Reading B on the web.** In linear theory v is parallel to g_N (KA4), and the web's speed distribution is the
  host-tracer distribution. Any step that keeps the law on in a G1-sized fraction of hosts therefore keeps it on in
  0.88 / 0.82 of the z 0.25 web mass. That fraction is still 0.52 / 0.36 at z 5 (increasing step) and 1.00 at z >= 5
  (decreasing step). So r stays at 72-86 against a line of 1.072.
- **S2 is not a pass.** Without the CMB row, the LP finds an increasing F that is zero below 250 km/s and reaches
  F_max ~1e5. It gives X-COP 6.1 / 6.5 and pins SPARC, groups and dSphs to their window edges. It lands only through
  the Monte Carlo tails, and it puts <F>_UDG at 4.5e4 / 5.1e4, about 1900x the UDG need, which has no frozen upper
  line. It fails S1's CMB leg and both W1 readings. Reported as frozen; it does not move the label.

**I5 label: DEAD BY REDUCTION, both footings.** R reduces the selector to dead keys. The reduced key then fails S1
(reading A) and W1 (reading B), and P2 fails GW170817 as a switch.

## I7: defect network of the a0 scalar, DEAD (both footings)

The model is an O(N) scalar whose vacuum scale eta is tied to a0: eta^4 = rho_DE c^2 (hbar c)^3, with
rho_DE = (a0/(kappa c))^2 / G.

| row | canonical | alt | line |
|---|---|---|---|
| eta (rho_DE) | 2.240e-3 eV (5.84e-27 kg/m^3) | 2.463e-3 eV (8.53e-27) | |
| **D0** formation z = eta/kT0 - 1 | **8.54** | **9.49** | >= 3400: **FAIL** (no network at the CMB epoch) |
| **D1** w at z 3400 (eta free) | frozen strings -1/3, walls -2/3; scaling strings, global monopoles, textures w = w_tot = **0.1674**; gauge monopoles 0 | same | \|w\| <= 0.01: **FAIL** (gauge monopoles go to D4) |
| **D2** rho_def/rho_b at z 3400 | strings at the CMB cap (G mu 1.5e-7, zeta 10) **3.7e-4**; at a0's eta (G mu 1.1e-61) 2.6e-58; walls at the isotropy cap (Omega_w <= 1.33e-5) **1.1e-9**; Omega_wall at a0's eta 4.6e-31 | 3.7e-4; 3.2e-58 (G mu 1.3e-61); 1.1e-9; 6.1e-31 | >= 1 (solver od/ob 5.56): **FAIL** |
| **D3** cluster f | strings <= 9.4e-9, walls <= 1.3e-8 | same | need 4.2 / 3.8: **FAIL** |
| **D4** no-particle rule | gauge monopoles are particle-like | same | **DEAD by rule** |
| D5 walls, isotropy | delta T/T = (3/4) Omega_wall <= 1e-5 caps Omega_wall at 1.33e-5 | same | reported with D2 |

- **Why I7 fails twice.** With eta set by a0, the network forms only at z of about 9, so it is absent at z 3400.
- **Freeing eta does not help.** Each defect type then fails a different row:
  - Stretched strings and walls have the wrong w.
  - Scaling networks track the background (w 0.167 at z 3400).
  - The CMB and isotropy caps keep every network 3e3 to 1e9 times short of the dust amount, and by more than 1e8 short
    in clusters, which relativistic networks do not enter.
  - The only w = 0 defect is a particle.
- **I7 label: DEAD, both footings.**

## MUTATE (all bite; separate outputs na1_MUTATE.*)

| M | planted | required | result |
|---|---|---|---|
| M1 | CMB speeds 2000-2030 km/s; UDG sigma 1 km/s, no flow | both S1 contradictions disappear | both gone (CDF excess 1.0), **bites** |
| M2 | F = 1[v <= 1 km/s] on the web | W1 PASS, both footings | r 1.000000 / 1.000000, **bites** (weak: no web cell has v <= 1 km/s, so this equals KA2) |
| M3 | Y = U.U2 with a second, matter-independent vector | R's reduction test must fail | fails, **bites** |
| M4 | non-relativistic network, w 0, rho_def/rho_b = od/ob 5.56, captured | D1, D2, D3 PASS; label DEAD by D4 only | all PASS, D4-only, **bites** (weak: it checks only the row logic on planted inputs) |

In MUTATE, S2 turns infeasible on both footings: once the UDGs lose their speed, no increasing F reaches their need.

## Post-freeze (disclosed)

- **A1-1.** The first run failed KA7: the solver gave w_tot(z 1e5) = 0.3225 against the frozen 1/3 +- 0.01. The frozen
  known answer was wrong, because matter is still 3 % of radiation at that z. The check was restated as the
  two-fluid value to 0.003 at three z, and now passes to < 1e-4.
- **The first run printed every label before the KA7 failure was read.** They were the same labels as now. That run
  is kept in run_main_KAstop.txt.
- **A1-2.** The first run peaked at 1.025 GB RSS, over the 1 GB line. The web loop was restructured with the same
  arithmetic: r and every graded number are identical to the first run's printed values.
- **GW wording.** The criteria wrote the GW window as |B X| <= 1.4e-15 (sign-dependent). The computed window is
  [-6.2e-15, +1.3e-15], and the 6.8e-20 spread quoted above uses the wider side.

## What is not done

- Class velocities other than SPARC rotation are PROVISIONAL constants (ICM turbulence 200, groups 100, M31 orbits 100,
  Coma 1000 km/s), and the flow is SV5's linear, 15.6 Mpc-smoothed field. The S1 legs are first-order stochastic
  dominance between classes. They do not depend on the tails, but they do assume all hosts share one flow.
- GB1 itself was not re-run. No class carries a velocity or defect feature, so by GB1's own rule every G row would be
  NO VERDICT. The SEED needs (taken from GB1's classes) were graded instead.
- The I7 caps (G mu 1.5e-7, delta T/T 1e-5, zeta 10, network speed 0.5 c, cluster baryon overdensity 1e3) are recalled,
  not fetched. Every margin is 3e3 or larger, and D0 does not use them.

Kappa = 1/2 FITTED; not theory closed.
