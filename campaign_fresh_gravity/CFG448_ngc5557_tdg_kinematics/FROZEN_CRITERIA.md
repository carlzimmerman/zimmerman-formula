# CFG448 FROZEN CRITERIA: archival resolved kinematics of the NGC 5557 tidal dwarfs

Frozen 2026-10-07, before any archive query, data product, script or result number of this lane exists.
Standing: kappa = 1/2 is FITTED. Both a0 footings (canonical 9.3603e-11, alt 1.1312e-10 m/s^2) are run everywhere.
No dark-matter particle is added; the framework's cold-fluid mass is still required wherever the law needs it.
Nothing here can say the data favour the framework over LCDM.

## Question
CFG441 found no old (>= 1 Gyr), tidally confirmed TDG with usable kinematics. Its best candidate is NGC 5557-E1
(Duc+2014; ~4 Gyr; in a 200-kpc tidal tail). Forecast F1 (CFG441, reported only): at R = 2 R_e = 4.6 kpc in its host's
field, Newton V_c = 16-24 km/s, law+EFE 28-41, isolated law 45-58 km/s (M_HI bracketed 1-3 x M_*). Does archival
resolved kinematics of E1/E2 (or another NGC 5557 tidal dwarf) exist that can be scored?

## Prior knowledge disclosed (before freezing)
- Everything in CFG441 (README, candidates.csv, F1 numbers above). Duc+2014 says E1 has long-slit H-alpha gradients
  with +-30 km/s errors and a WSRT HI gradient of ~30 km/s along the dwarf that may be tail streaming; E2 has only an
  HI centroid velocity; the WSRT HI maps are those of Serra+2012 (ATLAS3D). I have not looked at any cube.
- General knowledge (unverified, to be checked): ATLAS3D WSRT HI cubes have ~30-45 arcsec beams and ~16 km/s
  channels; E1's R_e = 2.3 kpc is ~12 arcsec at 38.8 Mpc. I therefore expect the WSRT data to fail the beam rule,
  and I freeze the rules below anyway; a pass would be scored exactly as frozen.

## Archives to search (each logged with what exists, resolution, sensitivity, or "nothing found")
NRAO VLA archive; ATLAS3D HI release (Serra+2012) and the WSRT/ASTRON archive (incl. Apertif if covering the field);
ESO archive (MUSE, other IFU); Keck archive (KCWI, OSIRIS not relevant); CFHT archive (SITELLE); Gemini archive
(GMOS-IFU); LOFAR/MeerKAT/FAST/ASKAP-WALLABY coverage (Dec +36: WALLABY does not reach, noted); the ADS/arXiv
literature 2014-2026 for any new kinematics of NGC 5557 dwarfs. Product metadata (beam, channel width, rms, integration
time, file size) are taken from archive records or the products themselves, never from a search-summary.

## U: what counts as usable (all required for a kinematic score)
U1 Resolution: the object's HI or H-alpha extent along the kinematic (else optical) major axis spans >= 2 beam FWHM
   (or >= 2 seeing FWHM for IFU), measured on the data product.
U2 Velocity: channel width <= 10 km/s (HI), or IFU velocity-centroid precision <= 5 km/s per resolved element.
U3 Detection: emission >= 3 sigma per channel in >= 3 channels at >= 2 independent positions on each side of centre.
U4 Inclination: kinematic inclination, or optical axis ratio (intrinsic thickness q0 = 0.2), with i >= 30 deg.
U5 Baryonic mass: M_* from Duc+2014 (1.2e8 Msun, 0.15 dex); M_HI from a measured flux (1.4 x for He); error 10% +
   flux-calibration error as published for the product.
A product failing U1-U3 is NOT usable for kinematics. It may still supply a measured M_HI (U5) for E1/E2, which is
REPORTED as an update of F1's bracket (if the cube is public, < 2 GB and the object is separable from the tail).

## V_c extraction (only if U1-U5 pass)
PV diagram along the major axis; V_rot(R_out) = half the difference of the intensity-weighted centroid velocities at
the outermost positions with >= 3 sigma emission on either side, divided by sin i. Beam smearing: R_out must be >=
1 beam from centre or the point is dropped. Pressure support: V_c = sqrt(V_rot^2 + 2 sigma_v^2) (sigma_v from
second-moment line width minus instrumental, in quadrature); half of the 2 sigma_v^2 term is added as a systematic.
Error budget: centroid errors, channel width / sqrt(12), inclination error, asymmetric-drift systematic, in quadrature.

## Decision rule (CFG441 F1 form; single object; both footings; nu_mono, 1-D EFE, nominal host)
Predictions V_N and V_law+EFE at the measured R_out from M_bar (CFG441's v_newton / v_law, host M = 0.6 L_K at the
projected distance). chi^2_x = (V_obs - V_x)^2 / (e_obs^2 + e_pred,x^2); Delta = chi^2_law+EFE - chi^2_N.
- SETTLING (Newtonian): Delta > +9 on both footings.  - LAW (boosted): Delta < -9 on both.  - else NON-DISCRIMINATING.
If M_HI is not measured, the rule is applied at both ends of the 1-3 x M_* bracket and a verdict needs both ends.
This is a single-object reading; it does NOT replace CFG441's frozen N_A >= 3 rule, and it is labelled as such.
If no usable product exists, the verdict is DATA NOT AVAILABLE and the deliverable is the archive statement plus an
observation specification (instrument, beam, channel, rms, time) derived in the script from the published/measured HI.

## Controls
- C1: reproduce CFG441's F1 numbers with this lane's code (V_N 16.4 / 24.2; law+EFE 28.0/29.1 and 39.6/41.1; iso
  45.0/47.1 and 55.6/58.0 km/s) within 0.1 km/s.
- C2: nu_mono from CFG4_common (deep limit within 2%), footings exact.
- MUTATE (MUTATE=1, outputs suffixed _MUTATE): replace the measured V_c by V_N (or, if no data, a synthetic V_c = V_N
  with a 4 km/s error at both bracket ends); the rule must return SETTLING on both footings, and the script then exits 1.
  A second synthetic case V_c = V_law+EFE must return LAW (reported, part of the same control).
- Main run exits 0 iff C1 and C2 pass (and, if scored, the extraction is reproducible from committed inputs).

Departures, if any, are disclosed in README.md; failed controls are kept as they fell.
