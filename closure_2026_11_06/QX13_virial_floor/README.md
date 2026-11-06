# QX13: virial-shock-heated sector with an entropy floor. FAIL (clusters under), class bound for every shock radius and upstream density

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane under SWARM_BRIEF.md: COLD DARK ENERGY, no particle,
no LCDM inputs.
- Criteria: FROZEN_CRITERIA.md (5584787fbd), committed and pushed before any script.
- Script: qx13.py. It runs about 30 s on 4 workers; logs run_main.txt / run_mutate.txt. It reuses QX12 iter_3's hosts
  and grader read-only and replaces only the solver.
- Lean: fable_independent_2026/lean_2026/QX13_virial_floor.lean, 5 theorems, standard axioms only. The MUTATE twin
  fails on exactly its 3 false claims.

## The class

This is the class QX12 left open. The sector has gamma = 5/3 and is isentropic per host, with K = max(K_sh, K_0).
- K_sh comes from the strong-shock jump at r_sh = r_ta/2 for the cold sea falling from rest at r_ta.
- K_0 is an entropy floor, fixed by the galaxy gates alone as c_min, the floor sound speed of the sea today.
- X-COP and groups are then predicted with no cluster input. Both footings.

## Results

| | canonical | alt |
|---|---|---|
| c_min (G5, G6, G7 only) | 132.3 km/s | 132.3 km/s |
| galaxy gates at c_min | G5 2e-4, G6 -0.045, G7 -6e-5: pass | G5 2e-4, G6 -0.050, G7 -6e-5: pass |
| X-COP at c_min (HO1 line) | **+0.463 / 0.472, FAIL (under)** | **+0.430 / 0.440, FAIL (under)** |
| groups band at c_min | [+0.184, +0.341], FAIL (under) | [+0.147, +0.302], FAIL (under) |
| groups strict (>= 16/20) | 0 / 0 | 0 / 1 |
| variant host | FAIL, same numbers | FAIL, same numbers |
| X-COP anywhere on the c_0 scan (0-3000 km/s) | +0.463 to +0.467 | +0.430 to +0.434 |
| CLUSTER-SET c_0 passing X-COP and groups | none | none |

Label: **FAIL** on both footings and both hosts. Clusters and groups miss UNDER: the sector adds almost nothing, and the
plain law's deficit (+0.4675 / +0.4345) is back.

Why:
- The strong-shock jump fixes the post-shock enthalpy at h_2 = (15/32) v^2 = (15/16) H_sh (Lean `shock_identity`),
  whatever the upstream density.
- Inside r_sh the isentropic profile is then rho = 4 rho_sea [1 + (16/15) H_in / H_sh]^(3/2). That is self-similar
  and only a few tens of rho_sea, far below the cosmic share in clusters. Every X-COP host is in the shock case
  (K_sh / K_0 = 15-27) and none reaches the capture cap.
- Galaxies need the floor for the opposite reason. With no floor (c_0 = 0), the shock-heated sector around KiDS lenses
  already shifts G6 by -0.075, against the 0.05 line.

## Class bound (post-result, analytic, Lean-certified)

The frozen M2 control did not bite: with heating off (K = K_0 everywhere) X-COP moves only to +0.460 / +0.427. That is
because M2 is the upper bound on retention for this whole class:
1. The post-shock enthalpy is at most H_sh for any infall from rest at r_ta, any shock radius and any upstream density
   rho_1 (Lean `shock_enthalpy`, `shock_h_le`).
2. In every host K >= K_0 holds.
3. The profile base 2w/(5K) rises with w and falls with K (`base_mono`).
4. Together these give `class_bound`: no shock radius and no upstream compression >= 1 can put more sector in a host
   than M2's open-contact K_0 atmosphere does.
5. More upstream compression also lowers K_sh in galaxies, so their retention can only rise, and c_min can only rise
   with it.

So the FAIL holds for every member of the isentropic-per-host, entropy >= galaxy-floor class, including the
shock-radius and upstream-compression iterations the criteria allowed. Those iterations cannot rescue it and were not
run.

This is a post-result reading of a frozen control, not a new frozen label. What it does NOT cover: non-isentropic
hosts with an entropy profile K(r) >= K_0 (accretion history). A comparison argument suggests they retain no more,
but it is not proved here.

## Rechecks and owed items

- **T1 / J0, CMB coldness:** an adiabatic floor is allowed only for c_0 <= 0.022 km/s (comoving k_J >= 50/Mpc on
  z 10-3400). c_min is 132 km/s, 6,000 times over. The floor cannot be primordial: it would need late injection
  (z < 10) by a mechanism that is OWED (for example QX7's clock switch). Stated, not graded.
- **Bullet-type offsets:** a collisional, shock-heated sector is stopped in a merger like the gas. If it carried the
  cluster's missing mass, the lensing peaks would sit on the gas, while Bullet-type systems show them on the
  galaxies. This class is disfavoured there as well, by argument. Moot here, since it carries almost no cluster mass.
- **Linear growth:** OWED.
- **Sun:** the sector mass inside 1 AU at the sea density is 1.6e-23 Msun, against the ephemeris bound of
  1e-10 Msun: harmless.

## Known answers and controls

- **KA1:** the uniform sea comes back to 3.9e-5 (line 1e-4, set from QX12 iter_3's quadrature floor before running):
  PASS.
- **KA2:** the shock identity holds to 7e-16: PASS.
- **KA3:** R = 0 gives +0.4676 / +0.4347: PASS.
- **M1 (floor off):** fails the galaxy gates (G6 -0.075): BITES.
- **M2 (heating off):** does not bite, as reported above; it is the class bound.
- **M3 (K x 1e-4):** fails the galaxy gates (G6 -0.170): BITES. So the gates have power.

## Convergence (no line was frozen; disclosed)

At c_min, 8 hosts (canonical) and 10 hosts (alt) did not reach the 1e-7 Picard tolerance in 4000 steps
(diag_conv.py / diag_conv.out, post-result diagnostic).
- All are galaxy-side: the ellipticals (all 7 entries share one total mass, 10^11.53 Msun, a fact inherited from the
  QX10 / QX12 host list), one SPARC G5 disc on canonical, and three on alt.
- Every X-COP and group host converged.
- The label is set by X-COP and groups, which sit at the plain law on every c_0 in the scan, so it does not depend on
  the non-converged galaxy hosts. c_min (132.3 km/s) could move by about one grid step if they converged.

## Door label

- **Clusters: FAIL** in this class too, and the closest no-input result is still QX12 iter_2's host-temperature step.
  Virial shock heating, from the jump conditions alone, cannot retain the cosmic share: it sets the post-shock enthalpy
  at the infall energy, so the retained density stays at the sea's scale.
- To retain the cosmic share, a sector needs entropy BELOW the shock value in clusters but ABOVE the galaxy floor.
  Within an isentropic host that is impossible (`class_bound`).
