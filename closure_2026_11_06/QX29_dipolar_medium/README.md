# QX29: gravitationally polarizable (dipolar) cold dark energy medium. FAILS at G8 (Cassini) for every host rule; every host rule also fails T2 or T3; G10 dipole continuum fails

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane: COLD DARK ENERGY sector with a dipole moment field.
No LCDM inputs.
- **Disclosure:** the owner's no-particle rule is relaxed for this TEST lane only. Nothing here is a particle claim,
  and the lane adopts nothing.
- a0 comes only from the two footings (canonical 9.3603e-11, alt 1.1312e-10 m/s^2), with the law's simple mu only.
  KA0 found no standard-MOND a0 string in any QX29 script.
- Criteria: FROZEN_CRITERIA.md (346612b24b), committed and pushed alone before any script or number.
- Scripts, one thread each:
  - qx29.py: static gates, about 8 s.
  - qx29.py --mutate.
  - qx29_growth.py: G6, about 3 s.
- Logs: run_main.txt, run_mutate.txt, run_growth.txt. MUTATE outputs: qx29_MUTATE.json/.out.
- A rerun of qx29.py is byte-identical.

## The class

- **Field equation and W.** The medium has a cold monopole sigma and a polarization Pi = sigma xi. Poisson is
  div g = -4 pi G (rho_b + sigma - div Pi).
  - W is derived by the frozen rule: spherical statics reproduce g_N = g^2/(g + a0) exactly on the full monopole.
  - That gives 4 pi G Pi = a0 g/(g + a0) and W = (a0^2/4 pi G)[-y - ln(1 - y)], with y = 4 pi G Pi/a0.
  - The static field is AQUAL with the law's mu. Pi saturates at a0/(4 pi G).
- **Monopole dynamics.** The monopole moves as cold dust. Where that dust sits in hosts is the open piece, so five host
  rules were graded:
  - A: weak clustering (the dipolar literature's hypothesis; assumed).
  - B1 / B2: captured at the cosmic share R = 5.562. B1 traces the baryons; B2 is r^-9/4 infall to r_ta.
  - Bcal: B2 at the largest amplitude that SPARC, KiDS and dSphs allow.
  - C: the minimal medium that can carry Pi with dipoles no longer than the radius (xi = r).
- **Cluster inputs.** None. No cluster number enters any constant.

## Labels (canonical / alt; P = PASS, F = FAIL)

| Gate (line) | A weak clustering | B1 traced, R | B2 infall, R | Bcal (f = 0.0736 R) | C minimal medium |
|---|---|---|---|---|---|
| G1 SPARC exact field + C1 (rms <= 0.110, U 0.50-0.80, C1 <= 0.3) | P / P: 0.0560 @ 0.58, 0.0558 @ 0.52 | F / F: C1 4.61 | F / F: U 0.31 / 0.30, C1 0.34 | P / P: 0.0560 @ 0.56, 0.0563 @ 0.50 | F / F |
| G2 KiDS shift (0.05) | P / P: 0.000 | F / F: -0.43 | **F / F: -0.29** | P / P: -0.044 (calibration gate) | F / F: -1.20 / -1.24 |
| G3 ellipticals \|D\| (0.15) | F / F: +0.210 / +0.189 | F / F: -0.46 / -0.47 | P / P: +0.13 / +0.11 | F / F: +0.203 / +0.182 | P / P |
| G4 X-COP (HO1: \|mean\| 0.05, rms 0.10) | **F / F: +0.467/0.476, +0.434/0.444** | F / F: -0.074/0.110, -0.097/0.127 | F / F: -0.006/0.125, -0.029/0.124 (rms) | **F / F: +0.389/0.396, +0.357/0.365** | F / F: +0.24 / +0.18 |
| G5 groups (QX5 band) | F / F | F / F | P / P | F / F | F / F |
| G6 growth + CMB-lensing shape (QX27 line) | PASS [A-web CONDITIONAL]: Delta chi^2 0 (monopole = cold reference). Footing-independent at linear order. Controls: sigma 0.01 km/s gives 7.5e-5; smooth from z 1089 gives 914.6, so the gate has power. This applies to all five rules | | | | |
| G7 dSphs (median shift 0.05) | P / P: 0.000 | F / F: +0.45 | F / F: +0.10 | P / P: +0.009 | F / F: +0.62 / +0.66 |
| G8 Solar System (E2 AQUAL Q2/Hees, Saturn / 7e-15) | **F / F: Q2 2.44-4.55x / 2.85-5.15x; Saturn 1.34e4x / 1.62e4x**. Identical for every rule: the medium adds no screening | | | | |
| G9 Bullet offset | NOT EVALUABLE for every rule | | | | |
| G10 dipole continuum (xi/r <= 1), max / median | F / F: 1.7e6 / 5.5e3 | F / F: 6.8e4 / 5.3 | F / F: 97 / 10.6 | F / F: 446 / 99 | F / F: 1.8e3 / 1.0 (beyond r_ta only; inside, xi = r by construction) |
| Fails at | G3 G4 G5 G8 G10 | all but G6 | G1 G2 G4 G7 G8 G10 | G3 G4 G5 G8 G10 | G1 G2 G4 G5 G7 G8 G10 |

Reported variants (f_cap R): B1 passes X-COP (-0.003/0.082 / -0.027/0.087) and fails G1, G2 (-0.37), G3 and G7. B2 gives
KiDS -0.25 and X-COP +0.059/0.128. Neither passes.

## Overall: FAILS at G8 on every host rule and both footings

- **G8 kills every host rule.** The class's static field is unscreened AQUAL with the law's mu, which is exactly AX1's
  failed class. A W with the high-g turn-off fixes the planets but not Q2 (E2 R1: 2.45-4.59x / 2.86-5.18x).
- **G10 fails on every host rule.** The medium cannot carry the polarization as a dipole continuum.
- **Without G8 and G10, the class still fails the triangle.**
  - **A (weak clustering) passes T2 and fails T3.** Galaxies see exactly the law, so the plain law's cluster gaps stay:
    X-COP +0.47 / +0.43, ellipticals +0.21, groups. A is also inconsistent with T1. G6 needs the monopole to cluster as
    dust, and nothing in the class stops that clustering at galaxy scales.
  - **B (captured dust) fails T2,** as QX7 / QX10 did. The halo over-predicts KiDS lensing by 0.29 dex (B2; 0.43 for B1)
    and over-boosts dSphs, while X-COP's mean lands close (B2 -0.006 / -0.029, rms 0.125).
  - **The key question:** can galaxies give clusters their missing +0.47 dex without cluster input? No. KiDS, SPARC and
    dSphs allow only f = 0.074 of the cosmic share (Bcal). The same scale-free dust capture then leaves X-COP at
    +0.39 / +0.36: only about 0.08 dex of the 0.47 is recovered.
  - **The polarization makes T2 worse, not better.** Carrying Pi with dipoles no longer than the radius (rule C) needs
    1.0e3-3.1e3 M_b of medium inside r_ta around a KiDS lens (1.2e3-3.7e3 on alt). POST-RESULT, with g from the baryons
    alone, it still needs 74-146 M_b, against a cosmic share of 5.56. KiDS is then over-predicted by 1.2 dex.
  - So the monopole that the polarization needs sits in the halo, and it over-predicts KiDS lensing by more than QX7 /
    QX10 did.
- **Triangle corners.**
  - A dies at **T3**.
  - B, Bcal and C die at **T2**. Bcal passes T2 only because it is fixed there, and then dies at T3.
  - All of them die on the Solar System (G8) and on the class's own dipole consistency (G10).
  - T1 passes only conditionally (A-web).

## G9 Bullet: NOT EVALUABLE

Grading the offset needs three things:
- the 1E 0657-56 convergence map;
- the Chandra gas map;
- a 3D, non-spherical merger solve of a collisionless monopole with AQUAL polarization.

None of these is buildable in small compute here. Qualitative only:
- B-type rules carry a collisionless monopole that follows the galaxies, so the offset has the observed sign.
- Rule A has no monopole, and its offset would come only from the AQUAL nonlinearity.

Not graded.

## MUTATE and controls

- **M1** (polarization off, W = 0, B2 cold mass at R, Newtonian): FAILS G1, G2, G3, G4, G5 and G7 on both footings, so it
  **BITES**. Numbers: G1 rms 0.207 @ U 1.20, KiDS +1.0, X-COP +0.228/0.303, groups +0.46 to +0.71.
- **M2** (polarization off, rule A, Newtonian baryons only): G1 rms 0.256 @ 1.20 FAIL on both footings, so it **BITES**.
  X-COP is +0.94.
- **M3** (B1 at amplitude 0 equals A) was run in the main output as KA5: X-COP +0.467457 / +0.434480, equal to A. The
  amplitude is what the cluster grade rests on.

## Known answers

- KA0: no standard-MOND a0 string, PASS.
- KA0b: footing a0 to 3e-6 and the glaw inverse to 2e-16, PASS.
- KA2: ellipticals +0.2099 / +0.1887, PASS.
- KA3: X-COP +0.4675 / +0.4345, PASS.
- KA4: SPARC 0.0560 @ 0.58 / 0.0558 @ 0.52, equal to QX8, PASS.
- KA5: PASS.
- KA6: Saturn delta g equal to AX1's to 6e-11, PASS.
- **KA1 FAIL as frozen.**
  - Root-solving W returns g^2/(g + a0) to 1.3e-12, and Pi saturates (0.9999 at g/a0 = 1e4). Both pass.
  - The finite-difference dW/dPi check missed its 1e-6 line at 3.3e-5. The step 1e-6 Pi is too coarse near y -> 1,
    where W'' ~ 1/(1 - y)^2.
  - POST-RESULT, with the step scaled by (1 - y), the check gives 6e-8 / 9e-8.
  - The analytic W' = a0 y/(1 - y) is exact, and no label depends on KA1.

## Disclosures

- **Monopole dynamics.** dv/dt = g with the dipole force dropped is this lane's reading of the BLT-type nonrelativistic
  limit. It is not certified, and the relativistic completion is not built.
- **Rule A.** Its zero excess mass in hosts uses the Jeans swindle for the uniform sea.
- **B2 profile.** The r^-9/4 profile is the Newtonian EdS self-similar infall slope, not re-derived with the law on.
- **Rule C.** C holds M_X constant beyond r_ta. That is why G10 fails only beyond r_ta, although the frozen text said
  "passes by construction". C fails six other gates regardless.
- **G1.** G1 uses QX8's exact-field T computed without the sector. The sector's own effect on T is second order and was
  not recomputed.
- **KiDS shifts.** The KiDS line is a shift relative to the plain law, whose own absolute residual is +0.142 / +0.102.
  The absolute residuals are in qx29.out: Bcal +0.098 / +0.057, B2 -0.146 / -0.186.
- **Solar System dipole length.** The local dipole length xi = Pi_s/sigma is 1e9-1e14 AU for every rule (qx29.json). So
  in the Solar System the medium is far outside the dipole-continuum regime. That could in principle change local
  polarization, but no such screening is derived here, and G8 is graded on the class's continuum equations.
- **Read-only reuse.** QX27's grader (hosts from QX12 iter_3 / A1, QX10, QX8 parts, QX18, QX5), QX3 iter2, and E2 /
  AX1 json are reused read-only. The git-ignored KiDS Brouwer+2021 files were read from the existing local copy.
