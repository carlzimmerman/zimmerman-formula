# QX28 frozen criteria: a two-phase superfluid cold dark energy sector (Berezhiani-Khoury class)

Frozen before any QX28 script or graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

This is a TEST lane. The sector is a scalar condensate field, called the COLD DARK ENERGY sector. The owner's
no-particle rule is relaxed for this lane only, as it was for HF1. The lane adopts nothing, and the README says so.
No LCDM inputs are used. Rules: ../SWARM_BRIEF.md.

Inputs, all reused read-only:
- QX12 iter_3 library: the QX10 iter_2 hosts, r_ta, R and RHO_D0, the A1 hosts, the KiDS lenses, the ellipticals,
  X-COP and the groups.
- QX8: the SPARC exact-field parts and its line.
- QX18: the ellipticals line.
- QX3 iter2: the growth ODE, PR4 lensing and the forest line.
- AX1: the Cassini Q2 grade of AQUAL-class fields.

The background prior, ../LCDM_FRIED_CHICKEN FROZEN_A22 / recipe24, is quarantined and is not used.

## The law, the footings and the a0 check (owner requirement, 11-06)

- The law is the framework's own simple-mu form, g_N = g^2/(g + a0), so g = g_N/2 + sqrt(g_N^2/4 + a0 g_N).
- a0 = kappa c sqrt(G rho_DE) on two footings, graded separately and never pooled:
  - canonical a0 = 9.3603e-11 m/s^2
  - alt a0 = 1.1312e-10 m/s^2
- Standard MOND's a0 is never used, and no other interpolating function is used either. That holds everywhere: in
  calibration, in the known-answer checks and in the phonon-force constants.
- KA0, a check that must pass before any gate:
  - (a) A scan of every QX28 script fails if the literal standard-MOND value (one-point-two times ten to the minus
    ten) appears.
  - (b) The law function and QX8's nu both satisfy g_N = g^2/(g + a0) to 1e-12 (relative) on a grid of g_N, on
    both footings.
  - (c) The a0 values in use equal 9.3603e-11 and 1.1312e-10.

## The class (as posed)

**Condensed phase** (BK superfluid, written as a scalar condensate field):
- Equation of state P = K rho^3, with K = 1/(12 Lambda^2 m^6) (natural units, BK's X^(3/2) phase).
- In a host the condensate sits in Thomas-Fermi hydrostatic equilibrium in the Newtonian potential of the baryons
  plus itself: 1.5 K rho(r)^2 = mu - Phi(r) where Phi < mu, and rho = 0 elsewhere. The condensate feels Newtonian
  gravity only.
- Its phonons mediate the law's force on baryons, sourced by the baryons only (BK structure). Phonon force =
  glaw(g_N,b) - g_N,b, and the total on baryons is g = glaw(g_N,b) + G M_X(<r)/r^2. The condensate's own mass adds
  Newtonian gravity on top.
- Mass: a cold component (T1) gathers the cosmic share, so the host's condensate has total mass M_S = R M_b,tot,
  with R = omega_d/omega_b = 5.562 (QX12 iter_2's T1 amplitude). The equilibrium is solved on a grid out to
  60 r_ta. The host keeps only the part inside r_ta, so M_X(<r) = M_poly(<min(r, r_ta)). The part of the polytrope
  beyond r_ta is not the host's; it is reported, not graded.

**Normal phase** (thermal, non-condensed):
- No phonons, so no law force.
- The sector is ordinary cold collisionless mass at the cosmic share, and its profile traces the baryons, as frozen
  in QX12 iter_2: M_X(<r) = R M_b(<r).
- Gravity is Newtonian: g = G (M_b + M_X)/r^2.

**Phase rule (T_c / coherence condition).** This is BK's virialisation criterion: the sector condenses in a host
if its de Broglie wavelength at the host's virial speed overlaps the interparticle spacing. That gives a host-mass
threshold M_c proportional to m^-4.
- Framework-native form: condensed if and only if V_f = (G M_b,tot a0)^(1/4) < V_c, which is equivalent to
  M_b,tot < M_c on each footing.
- M_c rule: M_c = the largest M_b,tot among the calibration hosts that must be condensed because they need the law.
  These are the 175 SPARC galaxies (M_b = 0.5 L[3.6] + 1.33 M_HI), the KiDS lens bins (QX12 lib LE) and the 8 dSphs.
  This is the lowest threshold galaxies allow, so it is the one most favourable to clusters. The ellipticals, groups
  and X-COP hosts are phased by the rule; none of them sets it.
- Reported: the band of M_c over which no group or X-COP phase changes, and the ellipticals graded with the other
  phase.
- Implied BK constants, reported only and never graded:
  - m from M_c, using m^4 = rho_X/v^3 at the host's sector density (hbar = 1, BK's overlap form), with rho_X the
    mean sector density inside r_ta and v = V_c.
  - Lambda from K and m.
  - The phonon coupling alpha from a0 = alpha^3 Lambda^2 / M_Pl.

## Constants fixed by non-cluster data only

- K per footing:
  - K_min = the smallest value on a 61-point log grid from 1e-8 to 1e4 (km/s)^2 kpc^6 Msun^-2 such that both
    calibration gates pass there and at every larger grid value (retention inside galaxy radii falls with K). This
    is the most condensate galaxies allow.
  - C1 (SPARC G5 list, QX10 line): M_X(<R_opt)/M_b <= 0.3.
  - C2 (KiDS isolated lenses, QX10/QX12 line): |mean shift| <= 0.05 dex, where the shift is mean
    log(g_obs/g_pred) minus the plain law's mean.
- M_c, as above.
- No cluster or group number enters any constant. No scan against cluster data picks anything.

## Gates, graded at (K_min, M_c) on each footing separately

- **G1 SPARC.** QX8's exact-field grade. Each condensed galaxy (exponential-disc host, R_opt = 3.2 Rdisk) gets its
  condensate g_X added outside the law: log g = log(nu(g_bar/a0) g_bar + g_X) + T. Line: rms <= 0.110 and median U
  in [0.50, 0.80].
- **G2 KiDS.** = C2. It passes at K_min by construction; it is reported as a calibration gate, not a prediction.
- **G3 X-ray ellipticals.** QX18's line, |D| <= 0.15 dex. D = mean log(M_obs/M_pred) at 2, 4 and 8 Re, with each
  elliptical in the phase the rule assigns.
- **G4 X-COP.** HO1 line: |mean| <= 0.05 and rms <= 0.10 dex on log(M_obs/M_pred), each host in its assigned phase.
- **G5 groups.** QX5's mean-band rule over the two stellar allowances: the band [f_st 1, f_st 0] must meet 0 within
  0.05. QX10's strict count (>= 16/20) is reported.
- **G6 T1 and growth.** The cosmic background is degenerate (cold, so n lambda_dB^3 >> 1), so as posed the
  condensed equation of state applies at the cosmic mean, with c_s^2 = 3 K rho_bar(a)^2 and
  rho_bar = rho_d0 a^-3 from the growth corner.
  - G6a (T1 as posed): the comoving Jeans length 2 pi (1+z)/k_J, with k_J = sqrt(4 pi G rho_bar)/c_s, must be
    <= 0.42/h Mpc (the record's smallest graded scale) at z = 10, 100 and 1089. The value of w at z = 1089 is
    reported.
  - G6b: the QX3 iter2 growth ODE at iter2's worst corner, with the Jeans term from c_s(a) for z < 10 only. This is
    generous: the sector is held cold for z > 10. Line: Delta chi^2 <= 4 on PR4 lensing against the cold reference.
  - G6c (forest, QX3 iter3 G4'): comoving Jeans length <= 0.42/h Mpc at z = 3.
  - G6 PASS needs G6a, G6b and G6c. If the PR4 package or CLASS cannot run in small compute, G6b is NOT EVALUABLE.
- **G7 dSphs.** The 8 MW classical dSphs (McConnachie 2012), Plummer hosts with M_* = 2 L_V, all condensed by the
  M_c rule. Shift = log10(g_pred/g_law) at r_half. Line: median shift <= 0.05 dex.
- **G8 Solar System / Cassini.** The class's static phonon field is the AQUAL type: BK's
  P(X) ~ X^(3/2) + alpha Lambda theta rho_b / M_Pl gives div(|grad theta| grad theta) ~ rho_b, with the law's
  interpolation. So the record's AX1 grade of AQUAL fields with this law applies: Cassini Q2 2.44-4.55x Hees, FAIL,
  unless the class supplies a screen. BK's EFT-breakdown argument is not derived in this lane. If no derived screen
  exists, G8 = FAIL (inherited from AX1, not recomputed), and the README says it is inherited.
- **G9 Bullet Cluster offset.** This needs a merger run with the phase transition plus the sector's self-interaction
  cross-section, which BK need for thermalisation. That is out of small compute. G9 = NOT EVALUABLE, and the README
  states what is missing.

## Labels

- Each gate gets a label per footing: PASS / FAIL / NOT EVALUABLE.
- PASSES ALL only if G1-G8 pass on both footings. G9 NOT EVALUABLE then makes the overall label NOT EVALUABLE at G9.
- Otherwise the overall label is FAILS at <gates>: every gate that fails on at least one footing. Each failure is
  tied to its triangle corner: T1 (cold for z > 10, growth), T2 (isolated-galaxy lensing) or T3 (clusters/groups).

## Known answers

- KA0: as above (the a0 check).
- KA1: a self-gravitating n = 1/2 polytrope with no baryons. The TF solver's radius and mass match an independent
  Lane-Emden integration (xi_1, omega_1) within 1 %.
- KA2: the plain-law ellipticals D equals QX18's +0.210 / +0.189 within 1e-3. If it does not, that is reported and
  G3 is graded as computed.
- KA3: R = 0 (no sector, all hosts condensed) returns the plain-law X-COP +0.4675 / +0.4345 within 2e-3.
- KA4: G1 with R = 0 returns QX8's exact-field rms 0.0560 @ 0.58 / 0.0558 @ 0.52 within 1e-4.
- KA5: K = 1e4 returns plain-law galaxy shifts (|C2| <= 0.02).

## MUTATE twins (separate outputs)

- M1 (always condensed): every host, groups and X-COP included, is condensed with the same K_min. This twin must
  FAIL at least one of G3-G5 on both footings.
- M2 (always normal): every host is normal-phase Newtonian. This twin must FAIL at least one of G1, C2 or G7 on both
  footings.
- M3: K = 1e-8 must fail C1 or C2, which shows the calibration gates have power.
