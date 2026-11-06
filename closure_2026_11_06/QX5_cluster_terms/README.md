# QX5: new cluster terms keyed on a cluster-vs-galaxy variable: four classes DEAD, one (a) a post-hoc lead

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No dark-matter particle. No LCDM inputs.
Criteria: FROZEN_CRITERIA.md + iter_*/FROZEN_CRITERIA.md (e3badba22f), committed alone before any code.
Script: qx5.py (one thread, about 2 s). Outputs: qx5.out/.json; MUTATE qx5_MUTATE.*; variant (a, g_cut 0.01 a0)
qx5_gcut001.*. Lean: fable_independent_2026/lean_2026/QX5_monotone_sandwich.lean (+ _MUTATE twin).

Every class adds a phantom multiplier F(k), M = M_b + F(k)(M_law - M_b). F is monotone in a key k that can tell
clusters from galaxies at the same y. Protocol P fits F (weighted isotonic) on non-cluster data only: SPARC,
7 Humphrey ellipticals, and KiDS lensing for keys a and d. It then predicts X-COP and 20 Lovisari groups. Kill check K
adds X-COP to the fit. X-COP needs F = 4.09 median [2.35, 5.67] canonical, 3.66 [2.11, 5.06] alt. The rms of log F
about the median is 0.12 dex, so the shape is fairly tight.

## Labels (as frozen; canonical / alt)

| Class | Key | Key ranges (canonical) | P: X-COP mean/rms | K: X-COP mean/rms | Label |
|---|---|---|---|---|---|
| a | potential depth via khronon norm, \|Phi\|/c^2 = Q-1 | SPARC <= 4.0e-6, ellipticals <= 4.6e-6, lensing <= 7e-7; X-COP 4.5e-5-1.2e-4; groups 1.7e-6-1.5e-5 | +0.222/0.243 (F 2.16, flat from the top calibration block) | **+0.016/0.079 (G-X PASS)**, groups overlap | **DEAD (frozen)**: lensing recheck (canonical, mean +0.142 -> +0.219), SPARC recheck (alt, mean shift 0.037) |
| b | matter pressure w = p/(rho c^2) | SPARC <= 3.1e-7, ellipticals 7.4-7.8e-7; X-COP 3.3e-6-1.6e-5; groups 1.5-5.0e-6 | +0.205/0.229 | +0.043/**0.112** | **DEAD**: shape (rms > 0.10); groups over-boosted in K ([-0.239, -0.092]) |
| c | khronon bulk velocity | analytic | - | - | **DEAD** on provisional literature inputs (LG 627 km/s vs CMB is at or above cluster kSZ peculiar velocities); readings 1 and 2 are classes a and b |
| d | enclosed baryon density / rho_DE (antitone) | SPARC 383-5.9e6, lensing 0.01-3.5e3; X-COP 183-5.3e3 | +0.329/0.343 | +0.177/0.204, SPARC rms 0.265 | **DEAD**: lensing and SPARC sit on both sides of the X-COP keys |
| e | collisional acceleration y_gas (CC as an AC2q term) | SPARC 0-0.18; X-COP 0.088-0.30; groups 0.009-0.038 | +0.476/0.484 | +0.044/0.088 | **DEAD-BY-GROUPS** (canonical) / **DEAD** (alt, SPARC recheck; groups fail too): groups' y_gas is inside SPARC's range, so F = 1 and groups stay +0.22..+0.39 short |

Alt footing: same labels (a, d DEAD; b DEAD; e DEAD). Variant g_cut = 0.01 a0 for class a gives the same picture
(K +0.019/0.088, lensing recheck fails).

## What the frozen labels hide (stated, not re-labelled)

Class a fails only its galaxy-side rechecks. The isotonic fit pools SPARC and lensing points at low keys and pulls
F there off 1. Lensing already sits +0.14 dex above the plain law at F = 1, and that is the move the recheck
penalises. X-COP and groups pass in K. Galaxies (<= 4.6e-6) and X-COP (>= 4.5e-5) are a decade apart in key. So a
step F (1 on every galaxy key, about 4 at cluster keys) is not excluded by these data. It has no native threshold
or amplitude, though, and only clusters set them: at best CLUSTER-SET, which is a FAIL under the no-tuning rule.
The post-hoc reading and its decisive test (galaxies that sit inside cluster potentials, i.e. Coma UDGs) are in
AMENDMENTS.md and iter_a2_member_galaxies/, frozen before that test was computed.

**iter a2 result: LEAD ALIVE, not explained.** With F_med the Coma UDGs move from +1.12 to +0.72 dex (z 4.28 -> 2.76;
alt 4.11 -> 2.65). Zeroing them would need F = 22-26, 5-6x X-COP's. So one F(|Phi|/c^2) does not serve X-COP and Coma's
members together (2.2-2.8 sigma tension), and the threshold and amplitude are still set by clusters alone.

## Door reading after QX5

Clusters stay **FAIL**. Classes b, c, d, e are DEAD. Class a (a phantom multiplier on the khronon clock-rate depth Q - 1)
is the one lead: it passes X-COP and groups only with a cluster-set step (CLUSTER-SET = FAIL by the no-tuning rule).
Coma's members need 5-6x more. Owed before it could become a candidate: a native threshold/amplitude, the Bullet-type
lensing offset (the boost follows the baryons' potential), and lensing = dynamics on its own equations.

## Known answers and controls

- F == 1 reproduces QX2 iteration 1: X-COP mean 0.467499 vs 0.467499 (canonical) and 0.434523 vs 0.434523 (alt),
  differences of 4e-8 (line 1e-3).
- M1 (K has power): with X-COP planted at F_true = 2.8, K returns G-X +0.000/0.000. BITES.
- M2 (P has power): with the ellipticals' F set to 2.8, P moves X-COP's mean by -0.339 / -0.348. BITES.
- Groups isothermal proxy: measured kT/(mu m_p) over V_c^2/2 has median 1.27 (Lovisari).
- Rerun: qx5.json byte-identical (md5 623d5aa0df3d).
- Lean QX5_monotone_sandwich: 5 theorems (mono_cap, mono_dead, anti_dead, mono_between, model_mono), standard
  axioms only. The MUTATE twin fails on all 3 false claims.

## Scope

Statics, spherical symmetry, hydrostatic masses, phantom-multiplier form. Cassini/PPN are unaffected for any
F <= 4.8e7 (phantom only; C6P). Lensing = dynamics and growth for a surviving term are owed.
