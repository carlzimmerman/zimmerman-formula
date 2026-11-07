# SV1: a mechanism inside the action for the hot/cold step? Geometry SHORT (and the wrong sign for lensing); the stiffness charge and the matter-flow keys are a NO-GO in class

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md, iter_1_geometry/FROZEN_CRITERIA.md,
iter_2_kinematic_charge/FROZEN_CRITERIA.md (74a07762ff), committed and pushed alone before any script. Both footings,
never pooled. No new term and no new constant are introduced: both iterations test what the existing v3s / AC2q
equations already do.

## iter_1: source geometry in the action's exact AQUAL field (the lead idea)

Hot systems are analysed spherically: spherical deprojection of the baryons, spherical HSE / Jeans masses, and
orientation-stacked lensing. The law is applied to g_N_sph = G M_b(<r)/r^2. A flattened or elongated source gives an
exact AQUAL field that differs from the law. QX4's solver was run on oblate and prolate Hernquist and Plummer spheroids
(q 0.4 to 2.5) and on exponential discs, over b/r_M 0.03-30: 91 solves of 200x48 cells, about 90 s. The class
placements come from QX20's own loaders. Two statistics:
- O1 = solid-angle shell mean of g_r. This equals the stacked-lensing and unweighted spherical mass.
- O2 = source-weighted shell mean. This equals the spherical HSE / Jeans mass.

**Theorem (LEAN, `fable_independent_2026/lean_2026/SV1_shell_bound.lean`, 5 theorems, 0 sorry, standard axioms; MUTATE twin
fails 3/3).** The premises:
- any source, triaxial included;
- g_r >= 0 on the shell;
- AQUAL's Gauss law, mean of mu(|g|) g_r = g_N.

Under these, the shell mean of g_r is at most the law-S root. So **geometry can only put the stacked-lensing and
unweighted spherical mass at or BELOW the law. That is the opposite sign to the KiDS early-type excess.** NUM check: max
O1 over all 91 solves is +2.0e-4 (line +1e-3), PASS.

| Class | Delta (measured step vs SPARC), canonical / alt | 2 sigma | P, best geometry in bracket (incl. +T_eff) | Label canonical / alt |
|---|---|---|---|---|
| X-ray ellipticals (Kroupa) | +0.183 / +0.189 | 0.316 / 0.310 | +0.026 / +0.026 (prolate q 2.5; oblate q 0.4 gives +0.010) | COMPATIBLE, NOT NEEDED / same (the step is not established at 2 sigma, QX18) |
| X-COP | +0.440 / +0.435 | 0.033 | +0.009 / +0.009 (geometry itself -0.0003 to -0.030) | **SHORT by 0.43 / 0.43** |
| groups (f* 0.5) | +0.236 / +0.227 | 0.165 / 0.164 | +0.009 / +0.009 (geometry -0.0001 to -0.011) | **SHORT by 0.23 / 0.22** |
| bright M31 dSphs | +0.199 / +0.188 | 0.124 / 0.122 | +0.022 / +0.022 (q 0.4, b/r_M 1) | **SHORT by 0.18 / 0.17** |
| KiDS early - late lensing | +0.158 | 0.128 | +0.0002 | **SHORT by 0.16** |

**Label: GEOMETRY SHORT, on both footings.**
- Through spherical HSE / Jeans, the action's own geometry moves a hot class by at most +0.017 dex. That bound comes from
  ellipticals, at a prolate axis ratio of 2.5 that no X-ray giant has.
- For X-COP and groups the geometry term is negative.
- The +0.009 in every P is the most generous disc-side term: the SPARC anchor drop from law to exact field at fixed U
  (QX8).
- Even with all of this, every graded step is short by 0.16-0.43 dex.
- The ellipticals' step is not established at 2 sigma, so geometry is not needed there. After Posacki IMF it is +0.066 /
  +0.075, and P is compatible with it.

Discs do not move: the equations are QX8's, so SPARC/RAR, Cassini/PPN, c_T and galaxy lensing are carried exactly.

Known answers and controls:
- KA1 sphere, |O| <= 9.5e-4: PASS.
- KA3 grid ladder, 1.2e-3: PASS.
- KA4 scale symmetry across footings, 1.8e-12: PASS.
- **KA2 Gauss: FAIL as frozen.** The error is 2.62e-3 against a 2e-3 line. All 23 offending solves sit at the innermost
  graded radius r/b = 0.32 in Plummer cores. That is about 1e-3 dex in O, against shortfalls of at least 0.16 dex, so no
  label depends on it.
- MUTATE M1 Newton moves O by at least 0.34 dex: BITES.
- M2 planted +0.30 flips groups and dSphs to EXPLAINED: BITES.
- M3 forced-sphere changes P by 0.017: BITES.
- A rerun gives a byte-identical sv1_geometry.json.

## iter_2: scalars the action already carries

- **K_Pi, the stiffness charge Pi = D.P + 2X.** In a stationary source D.P = 0 at static order (EQUATIONS 8.3, 9.1). That
  leaves Pi = s^2/N^2, which is monotone in the depth |Phi|/c^2. On QX20's points, SPARC and the hot systems overlap in
  depth: 522 / 535 SPARC points, KA1 PASS. Inside the overlap the hot points sit +0.343 +- 0.026 / +0.322 +- 0.025 above
  SPARC. QX5_monotone_sandwich.mono_dead therefore applies: **DEAD, both footings.**
- **K_v, the khronon's response to T^{0i} / T^{ij} at order v^2/c^2.**
  - Overlap is 48 points, with a step of +0.188 / +0.178 +- 0.025: **DEAD (mono_dead)**.
  - An O(1) coefficient would also need C = 0.9e5 to 3.7e5 to reach the classes (median v^2/c^2 is 1.5e-6 to 2e-5),
    which makes it CLUSTER-SET.
  - QX22's support split (+0.002 +- 0.045 ln) is carried.
- Controls: M1, a cluster-only planted key, removes the overlap: BITES. M2 Newton moves SPARC by +0.40 / +0.43 dex: BITES.
- **Label: NO-GO IN CLASS, both footings.** The class is every term carried by Pi or by matter's T^{0i} / T^{ij} with no new
  constant.

## Reading (post-data, not a label)

The action's static sector cannot make the step:
- its geometry has the wrong sign for lensing (Lean) and is at most about 0.02 dex for dynamics;
- its remaining scalars reduce to keys that are already dead.

A mechanism would need a matter property outside the minimal coupling, or a new field. That is outside this lane.

## Disclosed

- The tracer for O2 is the source density. Gas on equipotentials is rounder, which shrinks O2 further.
- Triaxial shapes are covered by the theorem for O1 only. O2 was not solved in 3D.
- Groups: 20 R500 points sit at the inversion cap (M(<R500) = M_b by QX20's own r_M).
- iter_2 reads "2 sigma of the hot class" as twice the standard error of the median step.
- The theorem's equality case is not certified.

## Files

- iter_1_geometry/: sv1_geometry.py, sv1_geometry.out / .json, table.npz, table_MUTATE_newton.npz, run_*.txt
- iter_2_kinematic_charge/: sv1_kinematic.py, sv1_kinematic.out / .json, run_main.txt
- Lean: fable_independent_2026/lean_2026/SV1_shell_bound{,_MUTATE}.{lean,out}

Kappa = 1/2 FITTED; not theory closed.
