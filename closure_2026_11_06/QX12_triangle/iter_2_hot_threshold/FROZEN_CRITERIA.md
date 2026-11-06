# QX12 iter_2 frozen criteria: a host-temperature-keyed sector, threshold from galaxies, amplitude from T1

Frozen before any script. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane.

## The term

The sector's equation of state is keyed on the host's specific thermal/virial energy, b = p/(rho c^2), the only QX5 key
that separates groups from galaxies (QX5 key b: SPARC <= 3.1e-7, ellipticals 7.4-7.8e-7, groups 1.5-5.0e-6, X-COP
3.3e-6-1.6e-5, canonical). Covariant form: the sector pressure is p_X = rho_X c_hot^2 Theta(b_t - b), with
c_hot -> infinity (absent) below the threshold and 0 (cold, retained) above it, where b is the trace ratio
-T^i_i/(3 T^0_0) of the baryons' stress tensor. Stated cost: this is a non-gravitational coupling of the sector's
equation of state to the baryons' stress. The matter-side force it implies is reported (Sun), not neglected.

## Constants (no cluster input)

- Threshold b_t = the maximum of b over every galaxy-side point (SPARC, ellipticals, and KiDS with
  b = g_obs r/(2 c^2)). This is the lowest threshold that leaves all galaxies untouched, so it gives hot systems the
  most sector that galaxies allow. Galaxy gates are unchanged by construction; that is checked, not assumed.
- Amplitude: where b > b_t, the enclosed sector mass is the cosmic ratio, M_X(<r) = R M_b(<r), R = 5.562 (T1;
  full capture, no free factor). The profile assumption, frozen: the sector traces the baryons. Variant, reported
  only: it traces the gas.
- The early universe: b of the cosmic baryons at z >~ 10 is about kT_cmb/(m_p c^2) <= 1e-9 << b_t, so this term
  alone would make the sector HOT early. T1 then needs the QX7 clock switch on top (cold for z > 10). That is stated
  as a second piece, and the grade does not depend on it.

## Gates (predictions, both footings)

- X-COP: the HO1 line, |mean| <= 0.05 and rms <= 0.10 dex, on log(M_obs / M_law(M_b (1 + R eps))), eps = 1 where
  b > b_t.
- Groups: QX5's mean-band rule (the band [f_st 1, f_st 0] contains 0 within 0.05), plus QX10's strict per-group
  2 sigma count (>= 16/20), reported.
- Galaxy rechecks (SPARC, ellipticals, KiDS): unchanged to 1e-12 (eps = 0 everywhere there).
- Sun: b at the solar centre is about 2.3e-6 > b_t, so the Sun is "hot". Report the sector mass the Sun could hold
  at the local Galactic sector density (galaxies keep none: the local density is <= the cosmic mean), compared with
  the planetary-ephemeris bound on extra mass inside 1 AU (1e-10 M_sun, as in the record's C6P lane).

## Labels

PASS if X-COP and groups (mean-band) pass on both footings with the galaxy rechecks unchanged. FAIL otherwise. Report
which way each misses (over or under).

## Known answers

- KA1: R = 0 reproduces QX2/QX5's plain law (X-COP +0.4675 / +0.4345).
- KA2: b values reproduce QX5's key-b ranges for X-COP, groups, ellipticals and SPARC to 1e-6 relative.

## MUTATE

- M1: b_t = 0 (every system cold) must fail the KiDS recheck (|shift| > 0.05). If not, the gate has no power.
- M2: R x 0 above the threshold returns KA1's numbers (the amplitude is what the prediction rests on).
