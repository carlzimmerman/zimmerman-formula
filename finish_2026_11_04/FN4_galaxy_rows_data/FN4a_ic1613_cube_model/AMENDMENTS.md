# FN4a amendments (each written and committed before any FN4a number)

Criteria: `FROZEN_CRITERIA.md` (a616530a1a). Data: `../_external_data/fn4a_ic1613_2026_11/`, see `fn4a_fetch.json`. These amendments set implementation details the criteria left open, and two departures forced by the data. No tolerance or label line is changed.

**A1, departure: stellar map.** `ic1613_ubvcalib.txt` was not obtainable: every URL on the host returns a 33,529-byte HTML page, not the approved 1,881-byte file. It was not kept. The B image also carries no WCS. So B−V cannot be calibrated, and M/L_V from B−V is not possible. Stars are the V-band light (background-subtracted, then azimuthally averaged with a median in elliptical annuli so foreground stars drop out), scaled to the stated total M★, with constant M/L. Primary M★ 2.88e7 M☉ (Oh+15 SED, IN1); bracket 1.9e8 (X1/LVD).

**A2, S0b like for like.** Oh+15's V(R_max) 16.9 km/s is corrected for asymmetric drift. S0b therefore compares the ring velocity at R_max after the same correction, v_c² = v_rot² − σ² d ln(Σσ²)/d ln R, with σ(R) and Σ(R) the azimuthal means of moment 2 and moment 0 at Oh+15's geometry. The uncorrected value is reported beside it. S0b uses moment 1, rings 13.2″ wide, centre, PA, i and V_sys from Oh+15's Table 1, and D 0.7 Mpc, as Oh+15.

**A3, non-circular terms.** In M_law+nc, the line-of-sight harmonics of order 1 (sin θ, radial flow) and order 2 (cos 2θ, sin 2θ) are added, on the same six radial nodes as σ(R), linearly interpolated, each bounded to ±20 km/s.

**A4, model construction (3DBarolo-style local normalisation).** For each trial model, every pixel gets a Gaussian line at v_los(x, y), with σ_eff² = σ(R)² + σ_inst². Here σ_inst = 2Δv/2.355 = 2.18 km/s for the Hanning-smoothed 2.572 km/s channels. The line is weighted by the observed moment-0 map. Each channel is convolved with the beam (13.19″ × 10.99″, PA −4.95°, from the cube's AIPS CLEAN record). Each pixel's spectrum is then rescaled to the observed integrated flux. The disc is thin for kinematics.

**A5, grid.**
- Crop 30′ × 30′ about Oh+15's centre; bin 4 × 4 to 6″ pixels; keep the channels that hold the 3D mask.
- Mask: the cube smoothed to twice the beam, above 3σ of the smoothed noise, dilated by one beam and two channels.
- χ² grid: every second binned pixel in x and y (12″, about one beam) and every second channel, inside the mask.
- Noise: the standard deviation of the binned cube in the 15 channels at each end of the band (emission-free).

**A6, rings.** M_free's rings are 13.2″ wide, out to R_out, where less than half of a ring's azimuth lies inside the mask. σ(R) is on six nodes spread evenly to R_out, interpolated linearly. Geometry is free in every model: centre, PA, V_sys, i, with i in 15–60°.

**A7, the law's field.** Gas: Σ_HI from the primary-beam-corrected moment 0, T_b = 4178 K per Jy/beam for this beam, N_HI = 1.823e18 ∫T_b dv, × 1.33. Gas and stars are deprojected to a face-on grid at the trial inclination. The in-plane Newtonian field comes from a zero-padded 2D FFT convolution with a kernel softened by 0.2 kpc (0.1 and 0.3 as a bracket). Then g_R is azimuthally averaged, the law applied to it (RQ3 `candidates/law.py`), and v_c² = R g. Distance 0.73 Mpc (UNGC, the record's). S0a and S0b use 0.7 Mpc, as Oh+15.

**A8, mocks (KA1, KA2).**
- The generator is A4's, with M_law's rotation for the real baryon maps at i 35° and σ 9 km/s.
- Centre, PA and V_sys come from the real M_free fit; intensity is the real moment 0.
- Noise is beam-correlated Gaussian noise scaled to the measured σ.
- KA2 multiplies the rotation by 0.505.
- Both mocks go through the same M_free and M_law fits and the same label rule. KA1 uses the canonical footing.

**A9, compute.** The 1.8 GB cube is read one channel plane at a time from the raw file (header-only metadata), cropped and binned. The optimiser is scipy `least_squares` (trf, 2-point Jacobian, fixed `x_scale`), deterministic.
