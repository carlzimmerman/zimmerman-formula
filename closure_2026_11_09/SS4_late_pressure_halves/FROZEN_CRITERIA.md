# SS4 (late pressure halves, the outside source's variant K): FROZEN CRITERIA, committed alone before any SS4 script or number

TEST lane, quarantined; registered RUNNING by the orchestrator. Adopts nothing; no particle adopted. kappa = 1/2 FITTED; not
theory closed. Footings canonical and alt, never pooled. SS1 machinery is read-only (imported and monkeypatched inside SS4's own
processes; no SS1 / SS2 / SS3 file is edited).

## 0. Stand-alone known-answer table: option (c), independent of K

The question: the largest fraction f_gal of an isolated lens's cosmic share (5.41 M_b) that may sit in a cored profile
rho = rho0 / (1 + (r/R_c)^2)^2 without failing KiDS or SPARC. That profile's enclosed mass is
M(<r) = M_tot (2/pi)[atan x - x/(1 + x^2)], x = r / R_c.

- **KiDS:** the record's line (QX5 loader, 59 Brouwer+2021 points, pointwise g at R from the enclosed mass, as SS1 gate 1).
  Graded as |shift| <= 0.05 at every point; the 0.3-1.5 Mpc subset (the source's wording) reported beside.
- **SPARC:** the F2 allowance on the retained mass inside the last measured radius (KD1 SPARC_f_max 0.3257 / 0.1937),
  applied to GB1's SPARC galaxies with M_b,sys = M_b(last).
- **Values:** R_c = 0.12, 0.3, 0.6, 1.2, 2.4, 3.0 Mpc; bisection on f_gal in [0, 1] (capped at 1).
- **Comparison:** the source's 0.18 / 0.23 / 0.30 / 0.44 / 1.00 / 1.00 is printed beside. The source's numbers are Delta Sigma
  (projected); the record's line is pointwise. That difference is stated, not converted.

## 1. Construction K, frozen once (as relayed, in the lane's words)

**No conversion.** Mass is conserved, the background is unchanged, a bare Lambda, a0 fixed.

**Two equal halves** (each omega / omega_b = R/2), pressureless before z_dec 0.631 (the record's footing value). After onset:

- **Half 1:** polytropic pressure P ~ rho^(4/3), with a fixed core R_c1 = 2.60 Mpc (physical, as given).
  - Bracket K-formula: the source's R_c1 = (c / (4 pi H0))(v_stiff / c) = v_stiff / (4 pi H0), recomputed per footing
    (about 0.31 / 0.34 Mpc), printed and graded as a bracket.
- **Half 2:** sound speed c_s2 = v_stiff (rho_crit,chi / (rho + rho_crit,chi))^(1/2). In every halo it relaxes to a core
  R_c2 = R500 (v_stiff / v_vir)^3. Bracket K-p2: the power 2.
  - "rho_crit,chi" is not defined in the relay. It is frozen here as 200 rho_crit(z) times the component fraction, i.e. the
    collapse threshold, so the field (rho << rho_crit,chi) has c_s2 = v_stiff.

**Per system, today** (SS1's primary pre-conversion halos: KD1 P3 amount f_cap R M_b, so each half is f_cap (R/2) M_b):
- each half sits in the cored profile above with its own R_c, centred on the system;
- M_chi(<r) = (M_chi0 / 2)[m(r / R_c1) + m(r / R_c2)];
- the profile is taken as reached (equilibrium). Item (4) tests whether that is reachable.

**Members** (Coma UDGs, reported): their own halos, as primary.

**Form choices** recorded beside the label: the 50/50 split, the 4/3 polytrope, the R_c1 value (and its formula), the cube
power, c_s2's form. Fitted: 0.

## 2. Gates (SS2 / SS3 lines) plus cosmic shear

- **Gates 1-10** as SS1 A2: 1 KiDS, 2 groups, 3 X-COP (+ TR1 fraction), 4 UDGs reported, 5 SPARC, 5b UMa, 6 background
  (unchanged: PASS by construction, verified), 7(b) lensing NO VERDICT with the reading reported, 8 forest + fsigma8 (fine
  grid), 9 Bullet, 10 Cassini.
- **Gate 9 Bullet:** both halves are pressured fluids meeting at about 4,700 km/s against c_s <= v_stiff, so they shock.
  Graded with DB1's gas-traced placement (on = "gas", WD1 reading (b)); the amount is each subcluster's K component inside
  R200. The galaxy-traced reading is reported beside.
- **Growth and P(k).** A three-fluid linear ODE (baryons; half 1; half 2), the record's QX3 iter2 Jeans form generalised:
  each pressured half i obeys delta_i'' + (2 + dlnH) delta_i' = (3/2) sum_j Omega_j delta_j - (c_s,i k / (a H))^2 delta_i
  after onset.
  - c_s2 = v_stiff (field).
  - c_s1 is set by its core, k_J1 = pi a / R_c1 (physical R_c1), i.e. c_s1 = R_c1 H sqrt(1.5 Omega_m) / pi.
  - Existing perturbations are not erased instantly; they respond to the pressure.
- **CS, cosmic shear (new).**
  - The model's change in S8 against the unchanged reference must stay inside KiDS-1000's 2 sigma fractional band:
    |S8_K / S8_ref - 1| <= 2 x 0.0225 / 0.759 = 5.9 %. This line is on the change, so the baseline S8 tension does not
    enter.
  - Reported: P_K / P_ref at k = 0.3, 1, 3 h/Mpc at z 0.3 and 0.5.
- **Item (3), the condensate rung:** stated in RESULT against WD1 (a fixed 1.6 Mpc core) and QX27-31. What is new is the
  mass-dependent R_c2; the lane says whether it changes the outcome.
- **Item (4), dynamics:** reported, not a gate.
  - The time to reach each core from a collapsed halo at the half's sound speed, t = (R_c - R_200) / c_s, compared with the
    6 Gyr since onset.
  - Whether an already-collapsed halo re-expands adiabatically (c_s >= v_vir) or not.
  - If a core is unreachable by z 0, the equilibrium assumption in section 1 is named as unphysical for that system class.

**Label.** PASS iff gates 1, 2, 3, 5, 5b, 6, 7(b), 8, CS, 9 and 10 all pass. Otherwise FAIL, naming the first failing gate in
that order.

## 3. Claims to compute, not take (reported)

| quantity | source's claim |
|---|---|
| X-COP retained / M_dyn | 0.70 / 0.65 / 0.56 |
| group f_ret(< R500), M500 2.1e13 to 1.4e14 | 0.31-0.47 |
| KiDS | +0.015..+0.029 dex |
| sigma8, S8, fsigma8 | preserved |

## 4. Known answers

- **KA-K1:** m(x) integrates the profile: numerical quadrature vs the closed form, to 1e-8.
- **KA-K2:** law-only replay (component -> 0) on gates 1-5.
- **KA-K3:** the three-fluid ODE with c_s -> 0 reproduces the reference growth (R = 1 to 1e-6).
- **KA-K4:** Bullet K1.

## 5. MUTATE

- **MK1 (pressure off):** both halves stay in the compact pre-conversion halos (SS1 MG3-like). KiDS must FAIL.
- **MK2 (v_stiff x 2):** R_c2 grows 8x and c_s doubles. Groups, X-COP or CS must move; otherwise NO BITE.

## 6. Hand estimates (before any number)

- **Clusters** (v_vir about 1000): R_c2 about 0.02 R500, compact; half 1 at 2.6 Mpc puts about 6 % of its mass inside
  1.5 Mpc. X-COP holds about half the share, 2 M_b inside R500 against a need of about 4: under-filled, maybe a FAIL.
- **Groups** (v 460): R_c2 about 0.18 R500, so about 2 M_b inside R500 against 3.46 / 1.23. Mixed.
- **Galaxies** (v 130): R_c2 about 8 R500, about 0.9 Mpc. 50 % of the share in a 0.9 Mpc core against option (c)'s allowed
  fraction. Expect a KiDS FAIL at 0.3-1.5 Mpc if option (c) allows < 0.5 at R_c about 1 Mpc.
- **Cosmology:** c_s2 = v_stiff in the field gives a comoving Jeans k about 0.17 / Mpc today, inside sigma8's window. Half the
  component stops growing at k > about 0.2 / Mpc for the last 6 Gyr, so sigma8 drops about 10-20 %. CS likely FAILS
  (expected kill 1).
- **Dynamics:** c_s1 = R_c1 H sqrt(1.5 Omega_m) / pi is about 40 km/s for R_c1 2.6 Mpc. Half 1 cannot reach a 2.6 Mpc core
  in 6 Gyr (it needs about 400 km/s). The frozen equilibrium is unreachable for half 1.

## 7. Operational

- Disk tight: outputs small; primary set only in the local gates (no AM / NFW passes), plus the K-p2 and K-formula brackets.
- Explicit-path commits via a sparse temporary worktree.
- Files: ss4.py, ss4_optc.py, ss4_cosmo.py, ss4_bullet.py, ss4_grade.py, ss4.json / .out, ss4_MUTATE.json / .out, RESULT.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
