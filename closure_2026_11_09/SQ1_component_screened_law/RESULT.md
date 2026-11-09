# SQ1 RESULT: FAIL / FAIL (criteria 7e8fa69c63), first failing gate Q1 depletion dynamics

## A1 / A2 update: the source's round-23 numbers, checked (reported; the label is unchanged)

Amendments A1 (3f30b2a08e) and A2 (de4b69bca4) were committed alone before these numbers. Script `sq1_a1.py` -> `sq1_a1.json` / `.out`.

**1. U_Q / rho_screen.**
- The source's own formula, (G M_b)^(3/2) a0^(1/2) / (8 pi G rho_screen r^3) at M_b 1e11 and 1 Mpc, gives **5,838 / 5,311 (km/s)^2**
  (canonical / alt), not the claimed 170. Checked by hand: U_Q = 9.5e-18 J/m^3 and rho_screen = 1.63e-27 kg/m^3.
- The frozen F's 4/3 gives 7,783.
- The source's figures sit a constant factor of about 34 low throughout; the UMa 15 kpc value is low by the same factor.
- At the source's 35 km/s threshold, R_dep = 2.12 / 2.05 Mpc at 1e11 (claim 0.652). The scaling R_dep proportional to M_b^(1/2)
  holds.

**2. GSMF.**
- Driver 2022 as in the record: n(M* > 1e10) = 0.0054 (footing h) / 0.0058 (h 0.7), against the claimed 0.0086.
- n(M* > 10^10.5) = 0.0025 / 0.0026, against 0.0041.
- The depletion volume filling with the correct U_Q is **8.3 / 7.6 %**, not 0.68 %. Still far below 1: volume filling is not a
  wall, as Q2 found.

**3. KiDS with the source's environment (C').** Depleted to 0.2 rho_screen inside R_dep (and 0.8 Mpc), with the claimed ambient
0.35 rho_screen to 3 Mpc.
- **FAIL 0.110 / 0.101** (14/59 points, mean -0.03). The deficit relative to the cosmic mean pulls the outer points below the law.
- Against the claim: the record's spherical collapse puts 6-27 rho_screen inside 3 Mpc around an isolated seed of 1e10-1e11, not
  0.35.

**4. Tinker 2008 budget and P(k) / sigma8 claims.** NOT EVALUATED: the record has no halo-model machinery.

**5. Ursa Major and the Local Group** (source form; frozen 4/3 beside).
- sqrt(U_Q / rho_screen) at 15 kpc for M_b 2e10 is 12,400 / 11,900 km/s (claim 2,120), far above sigma_UMa 148.
- R_dep for the UMa group is 4.65 / 4.50 Mpc (claim 1.43). The MW + M31 R_dep sum is 3.8 / 3.6 Mpc against the 0.77 Mpc separation.
- At thresholds 17.5 / 35 / 52.5 km/s: UMa R_dep 7.4 / 4.6 / 3.5 Mpc, and the Local Group is "cleared" in every case.
- These are energetic comparisons only. Q1's dynamics (the stated Lagrangian's attractive sign, and a < 0.1 % effect against
  gravitational collapse with either sign) is what decides, and it is unchanged.

**6. a0_eff(z).** The source's 0.98 / 0.92 / 0.68 at z 0.5 / 1 / 2 is recorded as its frozen prediction. It is NOT EVALUABLE
against the record's a0(z) cells (AT2: every on-disk high-z cell blocked by common modes).

**Reading.** The round-23 numbers are internally consistent with one another, but they are about 34x too small relative to their
own stated formula. Corrected, depletion radii are 3x larger and the filling is about 8 % (still small). Neither change reaches
Q1: the energetics favour clearing, the dynamics do not deliver it.

---

# Original result

Variant Q: a cold component, with the law's phantom screened by S = 1 / (1 + (rho_chi / rho_screen)^2). TEST lane, quarantined.
Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings never pooled. Reading G (dynamics-consistent) is graded; reading C
(the source's assumed depletion) is reported.

**Screen.**
- rho_screen / rho_crit = 4 a0 / (3 c H0) = **0.1906 / 0.2303** (KA-S1 exact).
- The mean component today is 1.40 / 1.16 rho_screen, so S(mean) = 0.34 / 0.43.
- S(mean) at z 0.3 / 0.5 / 1 / 1.5: 0.096 / 0.043 / 0.008 / 0.002 (canonical).

| gate | canonical | alt |
|---|---|---|
| **Q1 depletion dynamics** (component density inside 3 Mpc at z 0; line <= 0.2 rho_screen) | **FAIL**: 7.2 / 18.3 / 26.7 rho_screen at M_b 1e10 / 1e10.5 / 1e11 | **FAIL**: 6.0 / 15.2 / 22.1 |
| Q-KiDS (G) | FAIL max 0.618 (59/59, mean -0.38) | FAIL 0.658 |
| Q-SPARC (G) | FAIL rms 0.127 (line 0.066) | FAIL 0.127 |
| Q-groups (f_ret, local S) | FAIL 0/0; median +0.36 (v_vir median 388; S median 0.50) | FAIL 0/0 |
| Q-X-COP | FAIL +0.113. Bins -0.02 / +0.17 / +0.22; f_miss 0.99 / 0.59 / 0.48 vs TR1 0.71 / 0.66 / 0.58 (S about 1e-9 to 1e-6: fully screened) | FAIL +0.117 |
| Q2 volume filling (C) | PASS on S8: f_V 0.455 (n(M* > 1e10) = 0.0054 / Mpc^3); 39 % of the component pushed into 55 % of space at 1.7x the mean; sigma_2p(8) 0.080 so S8 +0.3 %. P_2p / P_ref 0.012 / 0.075 / 0.020 at k 0.3 / 1 / 3 h/Mpc | PASS +0.3 % |
| Q-web (G: S at the mean density) | **FAIL on fsigma8 only**, narrowly: ratio 1.028 / 1.011 / 1.005 / 1.002 (BGS to LRG3) vs the record's direction rule <= 1.001. Lensing 8.56, forest 2e-4, S8 +1.0 %: PASS | FAIL (fsigma8 1.044); S8 +1.6 % |
| Q-web (C, reported) | FAIL: fsigma8 1.29-1.03, S8 +8.9 % | FAIL: 1.33-1.04, +9.9 % |
| Q5 Bullet (screened, galaxy-traced Newtonian) | FAIL: M300 Z -2.61 / -4.41 | FAIL |
| Cassini | carried (rho_chi >> rho_screen near the Sun, so S about 0) | |

**Readings.**
- Reading C on KiDS: FAIL 0.081 / 0.073. The pointwise deficit of the depleted component at 1-3 Mpc pulls g below the law.
- Reading C on SPARC: PASS.
- Q3 (reported): the Ursa Major host (M200 3.8e12) has v_vir 222 km/s, below v_stiff, so C would deplete it. Under G, S at the
  host's mean density inside 1.5 Mpc is 0.011 / 0.016: its members are screened.

## Q1: why depletion cannot happen

- **Sign.** The stated Lagrangian L ⊃ -U_Q S(rho_chi) gives the component a chemical potential U_Q S'(rho_chi) < 0, deepest where
  U_Q is largest. Its force is attractive toward luminous galaxies. The source's V_rep = -U_Q dS/drho > 0 has the opposite sign.
- **Size (either sign).** Spherical Lagrangian shells from z 1000 to 0 around isolated galaxies.
  - The component force changes the density inside 3 Mpc by less than 0.1 % relative to the force-off run, for both signs and all
    three masses.
  - The force is strong only where the component is near rho_screen. That happens only at z < 0.5, and its r^-4 fall-off confines
    it to well inside 1 Mpc.
- **Gravity sets the outcome.** Every isolated L* seed has already collapsed its 3 Mpc Lagrangian sphere: the turnaround Lagrangian
  radius is 3.4 Mpc in WL1's convention and 10.7 Mpc with conserved Lagrangian mass. So the component inside 3 Mpc sits at 6-27
  rho_screen, not 0.2.
- **Consequence.** In reading G, KiDS's environment is screened inside R200 (S about 0) and partly screened outside (S 0.34), so
  the law is cut: KiDS -0.4 to -0.6 dex. SPARC galaxies sit in screened halos and fall to Newton + halo.

**Integrator disclosure (post-freeze, before any valid Q1 number).**
- The first run's Q1 lines are void. The inner shells collapsed onto an unsoftened point mass and the integrator stalled (log kept
  in `run_sq1_first_Q1_void.txt`).
- Three fixes followed: softening; the radiation term, as in WL1's shell; and the softening made comoving (a physical softening had
  switched off the early-time background gravity).
- The other gates' numbers were unchanged by these fixes.
- **KA-S3 as frozen FAILS:** the multi-shell turnaround finder reads 1.40 Mpc against WL1's 0.784.
  - `sq1_ka_s3.py` shows why. The same equations in WL1's convention (background inside the current radius) reproduce WL1's
    solver exactly: 0.7839 vs 0.7839 Mpc.
  - The conserved-Lagrangian-mass convention used here turns around at 4.71 Mpc physical (q 10.7).
  - The KA failure is the convention difference plus the multi-shell finder (oscillating collapsed shells), not an integrator
    error. Q1's FAIL holds in both conventions: everything inside q 3.4 Mpc has collapsed in either.

## Other checks

- **MS1** (rho_screen x 10): the KiDS (G) maximum is unchanged at 0.618. The worst points sit inside primary halos, where x >> 10,
  so S stays about 0. NO BITE on the maximum (disclosed).
- **MS2** (force off): this is Q1's force-off column, identical to G and R within 0.1 %. The force is dynamically negligible.
- **KA-S2:** the law-only replay of KiDS is exact (5e-17).
- **KA-S4:** F'(y) = 2y(nu - 1) matches the deep form to 5e-4.

## Reading

- **Screening the phantom by the local component density puts the switch exactly where the component is.**
  - The component is dense inside every galaxy halo, so the law is screened in the systems it was built for: SPARC and KiDS fail.
  - The proposed escape (the component's own response drains it from luminous galaxies) has the wrong sign in the stated
    Lagrangian. Even with the source's sign it is too weak by orders of magnitude against gravitational collapse.
- **Volume filling is not the wall:** with the Driver GSMF n(M* > 1e10) is 0.0054 / Mpc^3 and f_V 0.46, and the S8 change is
  +0.3 %.
- **Clusters are screened:** X-COP is under-filled (+0.11) with f_ret's falling profile, and the groups (v_vir about v_stiff) lose
  their component and stay under-predicted with S of about 0.5.

**What a repair would need:**
1. A screening variable that is high in cluster gas and the cosmic web but low inside galaxy halos. Component density does the
   opposite.
2. Or a component that never enters galaxy halos dynamically, which needs a force exceeding gravity at 0.1-3 Mpc around every
   galaxy since z of about 2.

## Files

- Criteria: `FROZEN_CRITERIA.md`.
- Scripts: `sq1.py`, `sq1_cosmo.py` (WM1's cosmo exec'd with patches), `sq1_grade.py`, `sq1_ka_s3.py` (post-run diagnosis,
  disclosed).
- Outputs: `sq1.json` / `sq1.out`, `sq1_grade.json` / `sq1_grade.out`, `sq1_ka_s3.json` / `sq1_ka_s3.out`, `parts/cosmo_SQ{G,C}_*.json`.
- Logs: `run_sq1.txt`, `run_sq1_first_Q1_void.txt`, `run_cosmo_SQ*.txt`.
- Compute: one thread, about 2.5 min for Q1 plus about 1.5 min for the cosmology; 0.5 GB with CLASS.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
