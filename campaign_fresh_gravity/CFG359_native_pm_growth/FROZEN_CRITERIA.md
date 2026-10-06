# CFG359 FROZEN CRITERIA: a framework-native nonlinear particle-mesh run of candidate B with the bound-only switch

Committed alone, before any script. kappa = 1/2 FITTED and fixed. nu_mono. No dark-matter particle: the cold MASS is
still required and is kept. No knob scans. Never "theory closed".

**Question.** Once the CFG354 T1 switch is ON in collapsed regions (halos and dense filament cores), does B's NONLINEAR
growth stay within observational tolerance of the switch-off control?

Owner scope update (2026-10-06, folded in before freezing): "make sure the growth simulations use my framework in all
cases and test both flat a0 and dynamical a0 with dark energy critical density".

## Model (every choice stated)
**Background.** GR Friedmann with Lambda (FP2): H(a) = H0 sqrt(Om a^-3 + OL), OL = 1 - Om. Parameters as L352:
h = 0.6736, omega_b = 0.02237, omega_c = 0.1200, so Om = 0.3138 and f_b = omega_b/(omega_b + omega_c) = 0.157.
Radiation is neglected (at most 3% of H^2 at z = 49, the same in every run, so it cancels in ratios).

**Matter.** Cold component plus baryons as ONE pressureless collisionless fluid (the record specifies no
microphysics, CFG345). Baryons trace the matter field on the mesh: rho_b = f_b rho_m.

**Gravity.** Comoving PM with canonical momentum p = a^2 dx/dt, units H0 = 1, lengths in Mpc/h.
- Newtonian peculiar potential: lap_x phi_N = (3/2) Om delta / a (FFT Poisson, CIC, periodic; k = 0 mode zero).
- **MOND sector (QUMOND form, the framework's own pieces).**
  - Kernel: nu_mono, copied from L340 lines 104-118 (y_p, h_p derived from nu_RAR; delta = 0.05).
  - Baryon-only source: g_Nb = f_b g_N (comoving), with y = |g_Nb| / (a a0(a)) (physical peculiar acceleration over a0).
  - Phantom: lap_x phi_ph = - f * div[(nu_mono(y) - 1) g_Nb]. The k = 0 mode is set to zero: in a periodic box the mean is
    a uniform background term, and the background is GR's (FP2).
  - The switch f multiplies the phantom density, as the task states.
  - Total kick: -grad(phi_N + phi_ph).
- The heat filter (xi = 0.03-0.15 pc) is irrelevant at Mpc mesh scales (cell size at least 0.5 Mpc/h, about 10^7 xi).
  It is omitted. It is identity at these scales.
- **Physical a0:** a0 = kappa c sqrt(G rho) with kappa = 1/2. Code acceleration unit H0^2 (Mpc/h) = 2.18e-13 m/s^2.

**a0(z) branches.** Scored separately and NEVER pooled.
- **A0-FLAT:** a0 is constant: canonical 9.3603e-11, alt 1.1312e-10 m/s^2 (rho_Lambda footing; the distinctive law).
- **A0-CRIT:** a0(z) = a0_foot E(z), with E = H/H0 (kappa c sqrt(G rho_crit(z)), normalised so that a0(0) is the footing
  value). This is the rival law.
- **A0-DE:** a0(z) = a0_foot sqrt(rho_DE(z)/rho_DE0), with the DESI DR2 CPL fit (w0, wa) = (-0.838, -0.62) (the
  chart_a0z_one.py values): rho_DE/rho_DE0 = a^(-3(1 + w0 + wa)) exp(-3 wa (1 - a)). REPORTED ONLY.
  - The background stays GR + Lambda in every branch. In A0-DE, CPL enters ONLY a0. This inconsistency is disclosed.

**Switches (each run separately).**
- **S0, the Newtonian control:** f = 0. This is the ONLY non-MOND run. It is labelled "Newtonian control", not
  "LCDM". It is also footing- and branch-independent.
- **S1, the bare chassis:** f = 1 everywhere.
- **T1, CFG354's rule on the mesh:**
  - psi with lap psi = delta (total matter, MS1 relaxation = owner decision 10-06), computed on the CIC mesh;
  - t_ij = d_i d_j psi = FFT^-1[k_i k_j delta_k / k^2], with eigenvalues l1 >= l2 >= l3;
  - tau(z) = (Delta_ta(z) - 1)/3, with Delta_ta(z) from CFG353/354's LCDM shell ODE (copied unchanged; checked
    against 11.806 at z = 0 and 6.412 at z = 1, to 1%);
  - f = clip(1/2 + (l2 - tau)/(2 eps), 0, 1): a linear ramp of full width 2 eps, with eps = 0.077 (CFG354 eps_min;
    CFG355's "ramp of full width 2 x" convention). It is not tuned.
  - The mesh cell is the effective smoothing scale. This is disclosed, and the resolution control tests it.
  - Note (a finding, not an edit): MASTER_LAGRANGIAN lines 39/110 label 11.806 / 8.893 as "canonical / alt at
    z = 0". In CFG354 K4 they are Delta_ta at z = 0 / z = 0.25. Delta_ta does not depend on the footing.
- **T1-VETO (diagnostic):** T1 with f = 0 in cells of the T-web filament signature (l3 < 0, lambda_th = 0, Hahn+07).
  By CFG354 Lean S8, isolated-host outskirts near r_ta share this eigenvalue signature (tau, tau, l_r < 0). So the veto
  removes filament cores AND host outskirts, and the T1 minus T1-VETO shift is an upper bound on the filament-core
  contribution.

**Initial conditions: the ONLY LCDM input, flagged.** Zel'dovich at z_i = 49 from the LCDM linear spectrum:
- Eisenstein-Hu no-wiggle transfer function, coded by hand (CFG354's T_eh); n_s = 0.965; sigma8_lin(z = 0) = 0.811;
  D(a) from the GR + Lambda growth integral.
- Justification: B = LCDM linearly with the switch OFF on linear modes (CFG324; CFG354 (a): ON = 0 on the linear
  field).
- The same Gaussian seed (359) is used for every run, so the ratios are paired.

**Box and steps.**
- L = 200 Mpc/h, 128^3 particles, 256^3 mesh (cell 0.78 Mpc/h).
- 150 KDK leapfrog steps in a, log-uniform piecewise over [0.02, 0.5], [0.5, 2/3] and [2/3, 1], so that z = 1, 0.5
  and 0 are hit exactly. Drift and kick factors are exact integrals of da/(a^3 H) and da/(a H).
- At most 8 processes (FFT threads included); os.nice(5).
- Budget: at most 2 h per run. If the resolution run exceeds it, it drops to 96^3/192^3 instead (a different particle
  count either way), and this is stated.

## Measurements at z = 1, 0.5, 0
- **P(k)**: CIC, deconvolved, shot noise subtracted, linear k bins. Reported as a ratio to S0.
- **sigma8** from the nonlinear measured P(k) (top hat at 8 Mpc/h; modes in the box up to Nyquist). Reported as a
  ratio to S0.
- **T1 ON fraction:** volume-weighted <f> and mass-weighted <f>, split by T-web class of the ON cells:
  - knot: l3 >= 0;
  - filament signature: l3 < 0;
  - also split by FoF proximity at z = 0: inside vs outside the r_ta = (3M/(4 pi Delta_ta rho_bar))^(1/3) sphere of
    any FoF halo.
- **Halo mass function proxy:** FoF (b = 0.2, at least 20 particles) at z = 0. Cumulative counts N(> M) in mass bins
  are reported as a ratio to S0.

## Decision (frozen; per a0 branch and per footing, never pooled)
For T1 vs S0 at z = 0:
- **GROWTH OK:** |sigma8 ratio - 1| <= 5% on BOTH footings, AND max over k <= 1 h/Mpc of |P ratio - 1| <= 10% on both
  footings.
- **TENSION:** the larger of the two shifts is in (5%, 20%] for sigma8, or the P shift is above 10% while sigma8 is
  within 20%.
- **FAIL:** the sigma8 shift is above 20% on either footing.

Lane verdict = the A0-FLAT branch (the framework's distinctive law). A0-CRIT is a separate branch verdict. A0-DE is
reported only. The S1 branches are reported.

**Observational tolerances (the reasoning behind the cuts, not ΛCDM-model outputs):**
- KiDS S8 matches Planck to ~2-3 sigma at ~3% precision, so a <= 5% shift in sigma8 is tolerable;
- cluster counts tolerate about 10% (HMF ratio for M >= 1e14 Msun/h, reported);
- filament lensing amplitudes span 0.6-1.9 (SCOPING_filament_constraints, reported).

## Controls (frozen pass conditions)
- **C1, linear growth:** an S0 run with IC amplitude x 0.01. For k <= 0.1 h/Mpc, sqrt(P(a)/P(a_i)) / (D(a)/D(a_i)) is
  within 1% at a = 0.5, 2/3 and 1.
- **C2, S1 fast growth (A0-FLAT):** sigma8(S1)/sigma8(S0) >= 1.5 at z = 0 on both footings, matching L341 /
  AUDIT_SIGMA8 qualitatively.
- **C3, resolution:** 192^3 particles on a 384^3 mesh for S0 and T1 A0-FLAT canonical. PASS if the T1 verdict
  category is unchanged. The size of the change in the sigma8 ratio is reported.
- **C4, MUTATE** (env CFG359_MUTATE=1, outputs *_MUTATE): T1 with Delta_ta := 1, i.e. tau = 0 (any overdensity),
  A0-FLAT, both footings. PASS if its sigma8 ratio exceeds T1's (it moves toward S1) on both footings. The MUTATE run
  writes separate outputs.
- **C5:** the Delta_ta check above (K4 reproduction).

## Lean
Lean 4 + Mathlib, no sorry. The certificates:
- tau(z) > 0 for Delta_ta >= 9 pi^2/16 > 1 (rational lower bound);
- the measured sigma8 ratios lie inside the stated rational intervals;
- each interval sits on the side of the 5% / 20% cuts that the verdict reports.

## Outputs
- Scripts and *.out / *_results.json go in this folder.
- Particle snapshots and work arrays go to ../_external_data/cfg359_work/ (outside the repo).
- No downloads. colossus is installed locally but is NOT used; the EH transfer is coded by hand.
