# SWT1 AMENDMENT A1 (committed alone, before any SWT1 script has run and before any graded number)

Criteria 4d86f4d107. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings never pooled.

**Timing, disclosed.** No SWT1 script exists yet and no SWT1 number has been computed. Both items below were found by hand while
writing the script.

## 1. T3 gate: the carrier's pressure (replaces one clause; carrier, masses and line unchanged)

- **Defect in the frozen text.** "Pressure from the Jeans equation with p(R_h) = 0" makes the carrier's pressure vanish at its
  outer edge. Any wall pressure then exceeds it in the outermost layer, so "the largest r with p_wall >= p_d" is always R_h and the
  gate passes trivially. That is an artefact of truncating the carrier, not physics.
- **Replacement.** The local isothermal pressure, p_d(r) = rho_d(r) v_c^2(r) / 2 with v_c^2 = G (M_b + M_d(<r)) / r. For the
  frozen carrier (R M_b in a singular isothermal sphere out to R_h) this is
  p_d = G R M_b^2 (1 + R r / R_h) / (8 pi R_h r^3).
- **Cleared set.** C = {r in (0, R_h] : p_wall(y(r)) >= p_d(r)}. M_unc is the carrier mass inside min(200 kpc, R_h) at radii not
  in C. Line unchanged: M_unc <= 0.9 M_b. Labels unchanged.

## 2. Correction to my own hand estimate (Section 2 of the criteria), made before any number

The ratios I wrote down (0.03 at R200, 0.13 at 100 kpc, 0.4 at 30 kpc; clearing radius 10-25 kpc; expected label SELF-CLEARING
NO-GO) assumed a halo of about 30 M_b inside 260 kpc. That is not the frozen carrier. For the frozen carrier, which is the record's
cosmic share R M_b spread to R_h, the deep-regime ratio is about (4/3) (R_h / (R r_M)) / (1 + R r / R_h), with r_M the MOND
radius; that is of order 10-20 at small r and stays above 1 out to R_h. **So the expected label on the frozen gate is now NOT A
NO-GO AS FROZEN.** The gate is not changed to rescue the earlier expectation.

## 3. Reported brackets added (never graded)

- **Carrier B, the halo a single-counting reading would need:** a singular isothermal sphere on the law's own Tully-Fisher line,
  v_h^4 = G M_b a0, so M_d(<r) = v_h^2 r / G. Reported: the cleared set and its outer radius in MOND radii.
- **KiDS reach.** The filling needed to keep the law on down to KiDS's lowest tabulated acceleration, g_bar = 1.38e-15 m/s^2, for
  every lens with log M* >= 9.4 (radius proportional to sqrt(M_b)), beside the fixed radii already frozen.
- **Bubbles held by pressure balance.** Radii where p_wall(y(R)) equals the pressure of mean-density component with a dispersion of
  17.5, 35 and 52.5 km/s (SQ1 A2's thresholds), at z 0 and 1; their filling and q_C; their reach as a fraction of KiDS's outermost
  radius per bin.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
